"""Build the storage and resource comparison from pinned 011 metadata and 012 measurements."""
import concurrent.futures
import json
import subprocess

from cloud import HOSTS, REMOTE, ssh
from pack import RUN, ROOT, T054, read, require, file_pin

MIB = 2**20
GIB = 2**30
OUT = "results/T-054/runs/checkpoint012-results"
PREFIX = "results/T-054/runs/hoan-thien-local-g3-011"
MANIFEST = read(T054 / "manifest-hoan-thien-local-g3-011.json")["outputs"]

def pinned(rel):
    path = ROOT / rel
    require(path, MANIFEST[rel])
    return read(path)

def cloud_resources(host):
    name = host[0]
    result, out, err = ssh(host, "python3 -B -c 'import json,shutil; print(json.dumps({\"free_disk_bytes\":shutil.disk_usage(\"" + REMOTE + "\").free}))'", timeout=30)
    assert result["exit"] == 0, err.decode(errors="replace")
    samples_path, = (RUN / "received" / name / OUT / "dev-queue").glob("*/attempt-001/monitor.jsonl")
    samples = [json.loads(line) for line in samples_path.read_bytes().splitlines()]
    assert samples and all(not row["clock_anomaly"] for row in samples)
    return {"ip": host[1], **json.loads(out),
            "monitor": {"file": samples_path.relative_to(RUN).as_posix(), **file_pin(samples_path),
                        "sample_count": len(samples),
                        "peak_tree_rss": max(r["peak_tree_rss"] for r in samples),
                        "max_monitor_gap_s": max(r["max_monitor_gap_s"] for r in samples)}}

def laptop():
    command = (
        "$os=Get-CimInstance Win32_OperatingSystem; "
        "[pscustomobject]@{utc=[DateTime]::UtcNow.ToString('o');"
        "free_ram_bytes=$os.FreePhysicalMemory*1KB;"
        "disk_free_bytes=(Get-PSDrive D).Free} | ConvertTo-Json -Compress"
    )
    result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command],
                            text=True, encoding="utf-8", capture_output=True, check=True)
    measurement = json.loads(result.stdout)
    policy = pinned(PREFIX + "/local-checks.json")["checks"][6]["observation"]
    threshold = policy["largest_slot_RAM_request_bytes"] + policy["reserve_bytes"]
    measurement.update(largest_slot_plus_reserve_bytes=threshold,
                       headroom_bytes=measurement["free_ram_bytes"] - threshold)
    return measurement

def partition(role, storage):
    rel = PREFIX + "/prepared/" + role + "-plan.json"
    plan = pinned(rel)
    sources = {}
    for job in plan["jobs"]:
        for value in job.get("source", {}).get("files", {}).values():
            sources.setdefault(job["slot"]["dataset"], {})[value["path"]] = value["bytes"]
    data = {dataset: {"files": len(pins), "bytes": sum(pins.values())} for dataset, pins in sources.items()}
    src_total = sum(row["bytes"] for row in data.values())
    outputs = storage["by_host"][role]
    native_4x = 4 * outputs["single_copy_empirical_bytes"]
    archive_4x = 4 * outputs["compressed_empirical_bytes"]
    headroom = storage["corrected_components"]["operational_headroom"]
    return {"source_files": data, "raw_source_bytes": src_total,
            "native_4x_bytes": native_4x, "archive_4x_bytes": archive_4x,
            "operational_headroom_bytes": headroom,
            "scenario_without_runtime_or_active_temp_bytes": src_total + native_4x + archive_4x + headroom}

def main():
    storage = pinned(PREFIX + "/storage-copy-accounting.json")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        measurements = list(pool.map(cloud_resources, HOSTS))
    assessment = {host[0]: m for host, m in zip(HOSTS, measurements)}
    role_candidates = {"ec2_1": "ec2-small-disk", "ec2_2": "ec2-large-disk"}
    scenario = {}
    for role, host in role_candidates.items():
        entry = partition(role, storage)
        entry["candidate_host"] = host
        entry["measured_free_disk_bytes"] = assessment[host]["free_disk_bytes"]
        entry["scenario_headroom_bytes"] = entry["measured_free_disk_bytes"] - entry["scenario_without_runtime_or_active_temp_bytes"]
        scenario[role] = entry
    audit = "results/T-054/runs/chuan-bi-main-006/OB-metric-time-window-check.json"
    m006 = read(T054 / "manifest-chuan-bi-main-006.json")["outputs"]
    require(ROOT / audit, m006[audit])
    issues = read(ROOT / audit)["issues"]
    affected = sorted({row["opaque_id"] for row in issues})
    assert len(issues) == 30 and len(affected) == 4
    out = {
        "scope": "host measurements and a planning scenario. Source counts from prepared plan metadata only.",
        "cloud": assessment,
        "laptop": laptop(),
        "old_35_25_provisional_mapping": scenario,
        "ob_sensitivity_candidate": {"scope": "fixed mask from checkpoint006; suggested descriptive only; pending Minh",
                                     "source": audit, "affected_opaque_ids": affected, "retained_count": 30},
    }
    with (RUN / "resources.json").open("x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for name, entry in assessment.items():
        print(name, "free GiB", round(entry["free_disk_bytes"]/GIB, 3), "M1 peak MiB", round(entry["monitor"]["peak_tree_rss"]/MIB, 1))
    for role, entry in scenario.items():
        print(role, "scenario GiB", round(entry["scenario_without_runtime_or_active_temp_bytes"]/GIB, 3), "margin GiB", round(entry["scenario_headroom_bytes"]/GIB, 3))
    print("laptop RAM margin MiB", round(out["laptop"]["headroom_bytes"]/MIB, 1))

if __name__ == "__main__":
    main()
