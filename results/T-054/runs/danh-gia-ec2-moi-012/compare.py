"""Verify received dev snapshots and compare the same job against the pinned old run."""
import json
from pathlib import Path
import sys

from pack import ROOT, RUN, T054, file_pin, read, require
sys.path.insert(0, str(T054 / "scripts"))
from bien_nhan import read_pin, receive_paths
from cham import verify_snapshot

HOSTS = ("ec2-large-disk", "ec2-small-disk")
REMOTE = "/home/ubuntu/rca-p7/T-054/checkpoint012/work"
OUTPUT = Path("results/T-054/runs/checkpoint012-results")
REFERENCE = T054 / "runs/trien-khai-005/received-cloud-001/results/T-054/queue"
MANIFEST = read(T054 / "manifest-trien-khai-005.json")["outputs"]

def old_attempt():
    attempt, = REFERENCE.glob("*/attempt-001")
    result = {}
    for name in ("invocation", "result", "cost"):
        path = attempt / (name + ".json")
        require(path, MANIFEST[path.relative_to(ROOT).as_posix()])
        result[name] = read(path)
    result["path"] = attempt.relative_to(ROOT).as_posix()
    return result

def differences(left, right, path=""):
    if left == right:
        return
    if isinstance(left, dict) and isinstance(right, dict) and left.keys() == right.keys():
        for key in sorted(left):
            yield from differences(left[key], right[key], path + "/" + key.replace("~", "~0").replace("/", "~1"))
    elif isinstance(left, list) and isinstance(right, list) and len(left) == len(right):
        for index, (a, b) in enumerate(zip(left, right)):
            yield from differences(a, b, path + "/" + str(index))
    else:
        kind = "float" if type(left) is float and type(right) is float else "other"
        example = {"path": path, "kind": kind}
        if kind == "float":
            example.update(reference=left, observed=right, abs_delta=abs(left-right))
        yield example

def compare(ref, observed):
    rows = list(differences(ref["result"]["records"], observed["records"]))
    numeric = [d for d in rows if d["kind"] == "float"]
    other = [d for d in rows if d["kind"] == "other"]
    return {"records_exact": not rows, "float_differences": len(numeric),
            "non_float_differences": len(other),
            "max_abs_float_difference": max((d["abs_delta"] for d in numeric), default=0),
            "examples": (other + numeric)[:20]}

def receive(host, reference):
    archive = RUN / (host + "-received.tar.gz")
    transfer = read(RUN / (host + "-receive.json"))
    assert transfer["exit"] == 0
    require(archive, transfer)
    folder = RUN / "received" / host
    out = folder / OUTPUT
    progress = read(out / "progress.json")
    result = {"progress": progress, "environment": read(out / "environment.json"),
              "archive": file_pin(archive), "attempt": None, "fixture_score": None}
    if progress.get("fixture_report", {}).get("PASS"):
        result["fixture_score"] = {
            "a4": file_pin(out / "fixture-report/report/a4.json"),
            "tables": file_pin(out / "fixture-report/report/tables.json"),
        }
    if not progress["tt_dev"]["PASS"]:
        return result, None
    plan = read(out / "dev-plan.json")
    snapshot = read(out / "dev-snapshot.json")
    assert plan["mode"] == "dev" and len(plan["jobs"]) == 1
    assert plan["jobs"][0]["slot"]["opaque_id"] == "dev-a915aa2424"
    receive_paths({REMOTE: str(folder)})
    try:
        verified = verify_snapshot(snapshot, plan["jobs"])
        entry, = snapshot["slots"].values()
        receipt = read_pin(entry["receipt"])
        envelope = read_pin(receipt["result"])
        invocation = read_pin(receipt["invocation"])
        assert list(verified.values()) == [envelope["records"]]
    finally:
        receive_paths({})
    attempt = next((out / "dev-queue").glob("*/attempt-001"))
    cost = read(attempt / "cost.json")
    runtime = read(attempt / "monitor.json") if (attempt / "monitor.json").exists() else {}
    reference_invocation = reference["invocation"]
    for field in ("source_sha256", "config_sha256", "window", "seed"):
        assert invocation[field] == reference_invocation[field], field
    result["attempt"] = {"status": envelope["records"][0]["status"],
                         "wall_s": cost["wall_s"], "monitor": runtime,
                         "input_exact_old": invocation["normalized_input_sha256"] == reference_invocation["normalized_input_sha256"],
                         "comparison_old": compare(reference, envelope)}
    return result, (invocation, envelope)

def main():
    reference = old_attempt()
    hosts = {}
    observed = {}
    for host in HOSTS:
        hosts[host], observed[host] = receive(host, reference)
    first, second = (observed[k] for k in HOSTS)
    cross = None
    if first is not None and second is not None:
        cross = {"input_exact": first[0]["normalized_input_sha256"] == second[0]["normalized_input_sha256"],
                 "records_exact": first[1]["records"] == second[1]["records"]}
    outputs = {"scope": "one TT dev case in M1, synthetic fixtures and report",
               "reference": {"attempt": reference["path"], "wall_s": reference["cost"]["wall_s"]},
               "hosts": hosts, "between_hosts": cross}
    with (RUN / "comparison.json").open("x", encoding="utf-8") as f:
        json.dump(outputs, f, ensure_ascii=False, indent=2)
    for host, result in hosts.items():
        print(host, {k: x["PASS"] for k, x in result["progress"].items()}, result["attempt"])
    print("Cross host:", cross)

if __name__ == "__main__":
    main()
