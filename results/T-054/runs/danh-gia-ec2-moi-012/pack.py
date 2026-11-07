"""Build a hash-checked package with exactly one authorized TT dev case."""
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
T054 = ROOT / "results/T-054"

def read(path):
    return json.loads(Path(path).read_bytes())

def file_pin(path):
    data = Path(path).read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def require(path, expected):
    actual = file_pin(path)
    assert actual["sha256"] == expected["sha256"], path
    assert actual["bytes"] == expected["bytes"], path
    return actual

def main():
    old_manifest = read(T054 / "manifest-trien-khai-005.json")["outputs"]
    meta_path = "results/T-054/runs/trien-khai-005/dev-metadata.json"
    require(ROOT / meta_path, old_manifest[meta_path])
    old = read(ROOT / meta_path)
    job = copy.deepcopy(old["job"])
    assert job["slot"]["dataset"] == "RE2-TT" and job["slot"]["opaque_id"] == "dev-a915aa2424"
    assert job["kind"] == "m1" and job["evaluation_mode"] == "dev"
    pin_path = "results/T-054/runs/hoan-thien-local-g3-011/current-code-pins.json"
    manifest = read(T054 / "manifest-hoan-thien-local-g3-011.json")["outputs"]
    require(ROOT / pin_path, manifest[pin_path])
    code = read(ROOT / pin_path)["code_pins"]
    pins = {}
    for rel, sha in code.items():
        pin = file_pin(ROOT / rel)
        assert pin["sha256"] == sha, rel
        pins[rel] = pin
    for pin in job["source"]["files"].values():
        rel = pin["path"]
        assert rel.startswith("data/rcaeval/") and len(Path(rel).parts) == 4
        assert Path(rel).name in ("metrics.parquet", "traces.parquet", "logs.parquet")
        pins[rel] = require(ROOT / rel, pin)
    assert len(job["source"]["files"]) == 3
    contract = "results/T-043/hop-dong.json"
    pins[contract] = require(ROOT / contract, job["m1_contract"])
    protocol = "results/T-052/giao-thuc-p7-a-003.json"
    p52 = read(ROOT / "results/T-052/manifest-dinh-chinh-g3-004.json")["outputs"]
    pins[protocol] = require(ROOT / protocol, p52[protocol])
    for pin in read(ROOT / protocol)["snapshots"].values():
        pins[pin["path"]] = require(ROOT / pin["path"], pin)
    fixture = [
        "results/T-043/fixture-dac-ta.json", "results/T-043/fixture/fixture-bo-sung.json",
        "results/T-044/fixture/dap-an-u-h.json", "results/T-044/tests/test_adapter.py",
        "results/T-044/tests/conftest.py", "results/T-044/tests/sinh_trace_S.py",
    ]
    subprocess.run(["git", "--no-optional-locks", "diff", "--quiet", "HEAD", "--", *fixture],
                   cwd=ROOT, check=True)
    for rel in fixture:
        pins[rel] = file_pin(ROOT / rel)

    runner = "results/T-054/runs/checkpoint012-tools/remote_checks.py"
    pins[runner] = file_pin(RUN / "remote_checks.py")
    package = RUN / "dev-and-code.tar.gz"
    with package.open("xb") as f, tarfile.open(fileobj=f, mode="w:gz") as tar:
        for rel in sorted(pins):
            origin = RUN / "remote_checks.py" if rel == runner else ROOT / rel
            tar.add(origin, arcname=rel, recursive=False)
        for rel, value in (("files.json", pins), ("dev-metadata.json", {"job": job, "source": old["source"]})):
            raw = json.dumps(value, sort_keys=True).encode("utf-8")
            member = tarfile.TarInfo(rel)
            member.size = len(raw)
            tar.addfile(member, io.BytesIO(raw))
    saved = {"scope": "code, generated fixture inputs, exactly three approved TT DEV files and phi-label job metadata",
             "files": pins, "archive": file_pin(package), "source_metadata": old_manifest[meta_path],
             "dev_source_files": 3, "dev_source_bytes": sum(pins[x["path"]]["bytes"] for x in job["source"]["files"].values())}
    with (RUN / "package.json").open("x", encoding="utf-8") as f:
        json.dump(saved, f, indent=2)
    print(json.dumps({"files": len(pins), "archive": saved["archive"], "dev_bytes": saved["dev_source_bytes"]}))

if __name__ == "__main__":
    main()
