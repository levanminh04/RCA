"""T-053. Verify only allowlisted dev bytes and probe the two machines."""

import argparse
import gzip
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3] if __name__ == "__main__" else Path.cwd()
REMOTE = "ubuntu@3.107.156.186"
REMOTE_PY = "/home/ubuntu/rca/T-031/envs/main/bin/python"
INSTANCE = "i-06c1d9173fb30932e"
DATASETS = {
    "RE2-TT": {
        "list": "results/T-022/allowlist-dev.json",
        "prefix": "data/rcaeval/re2tt_",
        "cases": 30,
        "remote_root": "/home/ubuntu/rca-t048/staging",
    },
    "Nezha-OB": {
        "list": "results/T-026/allowlist-dev.json",
        "prefix": "data/ngoai-rcaeval/nezha/online-boutique/rca_data/",
        "cases": 22,
        "remote_root": "/home/ubuntu/rca/T-032/repo",
    },
}
PRICE = (
    "https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/"
    "ec2-ondemand-without-sec-sel/Asia%20Pacific%20%28Sydney%29/Linux/index.json"
)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inputs(root):
    manifest = root / "results/T-048/manifest.json"
    expected = {i["path"]: i for i in json.loads(manifest.read_bytes())["files"]}
    source = {}
    for dataset, spec in DATASETS.items():
        allowlist = spec["list"]
        raw = (root / allowlist).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if (len(raw), digest) != (expected[allowlist]["bytes"], expected[allowlist]["sha256"]):
            raise ValueError(f"Allowlist differs from T-048 manifest: {allowlist}")
        cases = json.loads(raw)["cases"]
        if len(cases) != spec["cases"] or len({c["opaque_id"] for c in cases}) != len(cases):
            raise ValueError(f"Unexpected dev case inventory: {allowlist}")
        files = {}
        for case in cases:
            for item in case["files"].values():
                if item is None:
                    continue
                path = item["path"]
                if not path.startswith(spec["prefix"]) or ".." in Path(path).parts:
                    raise ValueError(f"Invalid dev path in {allowlist}")
                if path in files and files[path] != item:
                    raise ValueError(f"Conflicting dev file metadata: {path}")
                files[path] = item
        source[dataset] = {"allowlist": allowlist, "sha256": digest, "files": files}
    return source


def verify(root, files):
    root = root.resolve()
    summary = {"root": str(root), "matched": 0, "missing": [], "mismatch": [], "bytes_verified": 0}
    for relative, expected in files.items():
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or "locked" in path.parts:
            raise ValueError(f"Invalid resolved dev path: {relative}")
        if not path.is_file():
            summary["missing"].append(relative)
            continue
        size = path.stat().st_size
        digest = sha(path)
        if (size, digest) == (expected["bytes"], expected["sha256"]):
            summary["matched"] += 1
            summary["bytes_verified"] += size
        else:
            summary["mismatch"].append({"path": relative, "bytes": size, "sha256": digest})
    return summary


def runtime():
    return {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "versions": {name: version(name) for name in ("numpy", "pandas", "pyarrow", "scipy", "psutil")},
    }


def laptop(root):
    command = """
$osInfo = Get-CimInstance Win32_OperatingSystem
$cpuInfo = Get-CimInstance Win32_Processor
@{ ram_total_bytes = 1024 * $osInfo.TotalVisibleMemorySize
   ram_available_bytes = 1024 * $osInfo.FreePhysicalMemory
   cpu_name = $cpuInfo.Name
   cores = $cpuInfo.NumberOfCores
   logical_cpus = $cpuInfo.NumberOfLogicalProcessors
   load_percent = $cpuInfo.LoadPercentage
   top_processes = @(Get-Process | Sort-Object WorkingSet64 -Descending |
      Select-Object -First 8 Name,Id,WorkingSet64) } | ConvertTo-Json -Depth 3 -Compress
"""
    report = json.loads(subprocess.check_output(["powershell", "-NoProfile", "-Command", command]))
    report.update(runtime(), disk_free_bytes=shutil.disk_usage(root).free)
    return report


def instance_identity():
    base = "http://169.254.169.254/latest"
    token_req = Request(base + "/api/token", method="PUT",
                        headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"})
    with urlopen(token_req, timeout=4) as response:
        token = response.read().decode("ascii")
    request = Request(base + "/dynamic/instance-identity/document",
                      headers={"X-aws-ec2-metadata-token": token})
    with urlopen(request, timeout=4) as response:
        data = json.load(response)
    keep = ("instanceId", "instanceType", "availabilityZone", "region", "architecture")
    identity = {field: data[field] for field in keep}
    if (identity["instanceId"], identity["instanceType"], identity["availabilityZone"]) != (
        INSTANCE, "m7i-flex.large", "ap-southeast-2b"
    ):
        raise ValueError(f"Unexpected EC2 identity: {identity}")
    return identity


def ec2_probe(source):
    identity = instance_identity()
    wanted = ("MemTotal", "MemAvailable", "SwapTotal")
    mem = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, value = line.split(":", 1)
        if key in wanted:
            mem[key + "_bytes"] = int(value.split()[0]) * 1024
    report = runtime()
    report.update(
        identity=identity, logical_cpus=os.cpu_count(), load_avg=os.getloadavg(),
        memory=mem, disk_free_bytes=shutil.disk_usage(Path.home()).free,
        uptime_seconds=float(Path("/proc/uptime").read_text().split()[0]),
        top_processes=subprocess.check_output(
            ["ps", "-eo", "pid,comm,pcpu,rss", "--sort=-pcpu"], text=True
        ).splitlines()[:9],
        dev={
            dataset: verify(Path(DATASETS[dataset]["remote_root"]), meta["files"])
            for dataset, meta in source.items()
        },
    )
    return report


def aws_price():
    with urlopen(PRICE, timeout=15) as response:
        raw = response.read()
    decoded = gzip.decompress(raw) if raw.startswith(b"\x1f\x8b") else raw
    price = json.loads(decoded)
    matching = [
        offer for entries in price["regions"].values() for offer in entries.values()
        if offer.get("Instance Type") == "m7i-flex.large"
        and offer.get("Location") == "Asia Pacific (Sydney)"
        and offer.get("Operating System") == "Linux"
    ]
    if len(matching) != 1:
        raise ValueError("AWS Linux On-Demand price lookup is ambiguous")
    return {
        "url": PRICE, "rate_code": matching[0]["rateCode"],
        "usd_per_hour": matching[0]["price"],
        "billing_scope": "public compute rate, excluding account adjustments, storage and IP",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--key", default="D:/RCA-ext/keys/key2.pem")
    args = parser.parse_args()
    source = inputs(ROOT)
    started = datetime.now(timezone.utc).isoformat()
    command = [
        "ssh", "-i", args.key, "-o", "HostKeyAlias=3.26.62.217",
        "-o", "StrictHostKeyChecking=yes", "-o", "UpdateHostKeys=no",
        "-o", "BatchMode=yes", "-o", "ConnectTimeout=7", REMOTE, REMOTE_PY, "-B", "-",
    ]
    module = Path(__file__).read_text(encoding="utf-8")
    remote = f"__name__ = 't053_remote_probe'\n{module}\nprint(json.dumps(ec2_probe({source!r})))\n"
    report = {"started_at_utc": started, "laptop": laptop(ROOT)}
    report["laptop"]["dev"] = {k: verify(ROOT, v["files"]) for k, v in source.items()}
    report["ec2"] = json.loads(subprocess.check_output(command, input=remote.encode("utf-8")))
    report["price"] = aws_price()
    report["allowlists"] = {k: {field: v[field] for field in ("allowlist", "sha256")}
                            for k, v in source.items()}
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
    for machine in ("laptop", "ec2"):
        for dataset, summary in report[machine]["dev"].items():
            print(machine, dataset, summary["matched"], summary["bytes_verified"])
            if summary["missing"] or summary["mismatch"]:
                raise SystemExit(f"Dev verification failed: {machine} {dataset}")


if __name__ == "__main__":
    main()
