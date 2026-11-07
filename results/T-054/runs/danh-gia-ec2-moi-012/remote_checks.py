"""Exercise the pinned T054 worker, generated fixtures and scorer on a new host."""
import json
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "results/T-054"
sys.path.insert(0, str(OUT / "scripts"))
from bien_nhan import atomic, fingerprint, ref
from cham import snapshot_from_status, verify_snapshot
from dieu_phoi import status
from lap_ho_so import preflight, stable_environment
from p7 import load_plan
from nguon import authorize

host = sys.argv[1]
work = OUT / "runs/checkpoint012-results"
work.mkdir(exist_ok=False)
steps = {}
def step(name, fn):
    started = time.monotonic()
    try:
        steps[name] = {"PASS": True, **fn()}
    except Exception:
        steps[name] = {"PASS": False, "traceback": traceback.format_exc()}
    steps[name]["seconds"] = time.monotonic() - started
    atomic(work / "progress.json", steps)
    print(json.dumps({"step": name, **steps[name]}), flush=True)

def dev():
    source = json.loads((ROOT / "dev-metadata.json").read_bytes())
    job = source["job"]
    slot = job["slot"]
    assert slot["opaque_id"] == "dev-a915aa2424" and job["evaluation_mode"] == "dev"
    job.update(data_root=str(ROOT), pythonpath=[], executable=sys.executable,
               code_pins={p: v["sha256"] for p, v in json.loads((ROOT / "files.json").read_bytes()).items()
                          if p.startswith(("src/", "results/T-052/scripts/", "results/T-054/scripts/")) and p.endswith(".py")})
    assert len(job["code_pins"]) >= 100
    runtime = {"dataset": slot["dataset"], "g1_revision": job["g1_revision"], "inventory": job["inventory"],
               "cases": {slot["opaque_id"]: job["source"]}}
    job["runtime_ref"] = atomic(work / "dev-runtime.json", runtime)
    job["independent_source_ref"] = atomic(work / "dev-original-source.json", source["source"])
    job["m1_contract"] = ref(ROOT / "results/T-043/hop-dong.json")
    job["static_snapshot"] = ref(ROOT / "results/T-038/do-thi/thuc-the.json")
    slot["environment_sha256"] = fingerprint(stable_environment())
    plan = {"schema": "T054-PLAN-1", "mode": "dev", "host_role": host, "workers": 1,
            "directory": str(work / "dev-queue"), "jobs": [job],
            "monitor": {"poll_s": 0.1, "max_monitor_gap_s": 5, "score_phases": []},
            "budget": {"wall_s": 900, "method_dataset_s": {"RE2-TT|M1": 900}}, "open_before_run": []}
    plan_ref = atomic(work / "dev-plan.json", plan)
    authority_source = atomic(work / "dev-authority-source.json", {
        "source": "Minh: Duyệt gói chuẩn bị 012 trên hai EC2 mới.",
        "scope": "one TT DEV job and generated fixture; no test or main"})
    authority = {"pilot_grant": True, "source": authority_source, "plan_sha256": fingerprint(plan), "g3": False, "test_grant": False}
    authority_ref = atomic(work / "dev-authority.json", authority)
    authorize(load_plan(plan_ref["path"], plan_ref["sha256"]), authority, "run")
    cli = OUT / "scripts/p7.py"
    done = subprocess.run([sys.executable, "-B", str(cli), "_supervise", "--plan", plan_ref["path"],
                           "--sha256", plan_ref["sha256"], "--authority", authority_ref["path"],
                           "--authority-sha256", authority_ref["sha256"]], capture_output=True, timeout=960)
    (work / "dev.stdout").write_bytes(done.stdout)
    (work / "dev.stderr").write_bytes(done.stderr)
    assert done.returncode == 0, done.stderr.decode(errors="replace")
    state = status(Path(plan["directory"]))
    assert state["counts"] == {"VERIFIED": 1}, state
    snapshot = snapshot_from_status(plan, state)
    records = verify_snapshot(snapshot, plan["jobs"])
    assert list(records.values())[0][0]["status"] == "OK"
    atomic(work / "dev-snapshot.json", snapshot)
    return {"counts": state["counts"]}

def fixture():
    args = [sys.executable, "-B", str(OUT / "scripts/fixtures.py"), str(work / "fixture")]
    done = subprocess.run(args, capture_output=True, timeout=390)
    (work / "fixture.stdout").write_bytes(done.stdout)
    (work / "fixture.stderr").write_bytes(done.stderr)
    assert done.returncode == 0, done.stderr.decode(errors="replace")[-3500:]
    return {"summary": json.loads((work / "fixture/summary.json").read_bytes())}

def fixture_report():
    args = [sys.executable, "-B", str(OUT / "scripts/fixtures.py"), str(work / "fixture-report"),
            "--reports-from", str(work / "fixture")]
    done = subprocess.run(args, capture_output=True, timeout=120)
    (work / "fixture-report.stdout").write_bytes(done.stdout)
    (work / "fixture-report.stderr").write_bytes(done.stderr)
    assert done.returncode == 0, done.stderr.decode(errors="replace")[-3500:]
    return {"summary": json.loads((work / "fixture-report/summary.json").read_bytes())}

atomic(work / "environment.json", preflight())
step("tt_dev", dev)
step("fixture", fixture)
if steps["fixture"]["PASS"]:
    step("fixture_report", fixture_report)
if not all(s["PASS"] for s in steps.values()):
    raise SystemExit(1)
