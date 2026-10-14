"""T-032 sequential RE2 BARO queue; prepare never launches research workers.

CLI: prepare <new_plan_dir> | run <plan_dir> <new_batch_dir>
Run on the approved EC2 interpreter/environment under run_guarded.py. Each
child inherits the controller's process group. No retry, new session, labels,
case selection by results, tolerance, environment installation, or source edit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import signal
import subprocess
import sys
import time
import traceback

sys.dont_write_bytecode = True

import replay_baro as replay

BASE = Path.home() / "rca/T-032"
SCRIPTS = BASE / "scripts"
PILOT = BASE / "runs/baro-re2-first-001"
PILOT_MONITOR = BASE / "runs/baro-re2-first-001-monitor/status.json"
PILOT_ID = "dev-03d4910932"
SCRIPT_NAMES = ("batch_baro.py", "capture_baro.py", "replay_baro.py",
                "capture_microrank.py", "replay_microrank.py", "run_guarded.py")
ENV_KEYS = ("PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "PYTHONIOENCODING", "PYTHONPATH",
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
            "TMPDIR", "XDG_CACHE_HOME", "MPLCONFIGDIR", "MPLBACKEND")


class BatchError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise BatchError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def json_hash(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def ref(path, pointer=""):
    return {"path": str(path), "json_pointer": pointer}


def inside_run(path):
    path = Path(path).expanduser().resolve()
    allowed = (BASE / "runs").resolve()
    require(path.is_relative_to(allowed) and path != allowed, "output/input plan must be below T-032/runs")
    return path


def new_run(path):
    path = inside_run(path)
    path.mkdir(parents=True, exist_ok=False)
    return path


def file_row(path):
    path = Path(path)
    stat = path.stat()
    return {"path": str(path), "sha256": replay.sha(path), "bytes": stat.st_size,
            "allocated_bytes": getattr(stat, "st_blocks", 0) * 512}


def relative_artifact(directory, name):
    relative = PurePosixPath(name)
    require(not relative.is_absolute() and ".." not in relative.parts and "\\" not in name,
            "invalid artifact path: " + name)
    path = (directory / relative).resolve()
    require(path.is_relative_to(directory) and path != directory, "artifact escaped run")
    require(path.is_file() and not (directory / relative).is_symlink(), "artifact absent or symlink: " + name)
    return path


def scripts_now():
    return {name: file_row(SCRIPTS / name) for name in SCRIPT_NAMES}


def verify_scripts(expected):
    actual = scripts_now()
    require(set(actual) == set(expected), "script set differs from plan")
    for name in expected:
        require(actual[name]["path"] == expected[name]["path"] and
                actual[name]["sha256"] == expected[name]["sha256"], "script changed: " + name)
    return actual


def environment():
    return {"python": sys.version, "executable": sys.executable,
            "executable_resolved": str(Path(sys.executable).resolve()),
            "prefix": sys.prefix, "base_prefix": sys.base_prefix,
            "environment": {key: os.environ.get(key) for key in ENV_KEYS}}


def source_signature(entry, record, code_hashes):
    return {"opaque_id": record["opaque_id"], "entry": entry, "code_hashes": code_hashes,
            "frozen_status": record["status"], "input_shape": record["input_shape"],
            "window": record["window"], "source_cost": record["cost"],
            "input_sha256": record["input_sha256"], "config_id": record["config_id"],
            "method_version": record["method_version"], "seed": record["seed"],
            "hashseed": record["hashseed"],
            "source_pointers": {name: ref(entry["path"], "/" + name)
                                for name in ("input_shape", "window", "cost", "input_sha256")}}


def source_case(opaque_id, audit):
    started = time.perf_counter()
    entry, record, index26, code_hashes = replay.source_for("RE2-TT", opaque_id, audit)
    return source_signature(entry, record, code_hashes), record, time.perf_counter() - started


def verified_main_ids(audit):
    manifest = replay.read(replay.safe_source(replay.M24))
    index = replay.read(replay.verify(replay.I24, manifest["source_hashes"][replay.I24],
                                     replay.M24 + "#/source_hashes", audit))
    entries = [entry for entry in index["records"]
               if entry["method"] == "baro" and entry["variant"] == "native"]
    ids = [entry["opaque_id"] for entry in entries]
    require(len(ids) == len(set(ids)) == 30, "expected exactly all 30 unique RE2 BARO native main records")
    require(PILOT_ID in ids, "approved pilot missing from main index")
    return sorted(ids)


def verify_output(directory, source, frozen, script_hashes):
    """Verify bytes of the existing PASS, whose worker already checked capture."""
    started = time.perf_counter()
    directory = inside_run(directory)
    check_path = directory / "check.json"
    check = replay.read(check_path)
    require(check.get("status") == "PASS" and check.get("intermediates_eligible") is True,
            "worker check/intermediate eligibility is not PASS")
    require(check.get("dataset") == "RE2-TT" and check.get("method") == "baro" and
            check.get("opaque_id") == source["opaque_id"], "worker check identity differs")
    require(check.get("frozen_path") == source["entry"]["path"] and
            check.get("frozen_sha256") == source["entry"]["sha256"], "worker comparison source differs")
    require(check.get("differences") == [] and check.get("compare", {}).get("pass") is True and
            check["compare"].get("difference_count") == 0 and check.get("capture_check", {}).get("pass") is True,
            "worker exact comparison/capture did not pass")
    require(check["capture_check"].get("native_adapter_keys_exact") is True, "native/adapter keys did not pass")
    require(check.get("manifest_excludes") == ["check.json"], "unexpected worker manifest exclusions")
    declared = check["artifact_manifest"]
    names = [row["path"] for row in declared]
    require(len(names) == len(set(names)), "duplicate worker manifest artifact")
    for name in names:
        relative_artifact(directory, name)
    require(replay.artifact_manifest(directory) == declared,
            "worker artifact hash/size/file set changed, including possible failure output")
    logical = sum(row["bytes"] for row in declared) + check_path.stat().st_size
    allocated = sum(getattr(p.stat(), "st_blocks", 0) * 512 for p in directory.rglob("*") if p.is_file())
    invocation = replay.read(directory / "invocation.json")
    for name in ("capture_baro.py", "replay_baro.py", "capture_microrank.py", "replay_microrank.py"):
        require(invocation["scripts"][name] == script_hashes[name]["sha256"], "pilot/worker wrapper changed: " + name)
    require(invocation["python"] == sys.version and invocation["hashseed"] == "0",
            "pilot/worker Python/hashseed differs from controller")
    for item in replay.read(directory / "source-checks.json")["checks"]:
        require(item.get("pass") is True, "saved source check did not pass")
    reconstructed = replay.read(directory / "ban-ghi-0.json")
    require(not replay.compare_records(frozen, reconstructed), "independent frozen comparison differs")
    capture = replay.read(directory / "capture/capture.json")
    require(capture["status"] == "captured_unverified_replay" and capture.get("errors") == [] and
            capture["adapter_status"] == frozen["status"], "capture status/errors differ")
    start_meta = replay.read(directory / "capture/capture-start.json")
    for key, value in start_meta["thread_environment"].items():
        require(value == os.environ.get(key), "pilot/worker thread environment changed: " + key)
    return {"status": "PASS", "directory": str(directory), "source": source["entry"],
            "check": file_row(check_path), "artifact_manifest_sha256": json_hash(declared),
            "n_artifacts_including_check": len(declared) + 1, "logical_bytes": logical,
            "allocated_file_bytes": allocated, "verification_s": time.perf_counter() - started,
            "capture_check": {"pass": True, "native_adapter_keys_exact": True,
                              "scalers_checked": check["capture_check"]["scalers_checked"],
                              "score_count": check["capture_check"]["score_count"],
                              "basis": "existing worker check plus full byte-manifest verification; no duplicate restoration"}}


def positive(value, field):
    require(isinstance(value, (int, float)) and math.isfinite(value) and value > 0,
            "missing/nonpositive estimate input: " + field)
    return value


def scale_inputs(source):
    shape, window = source["input_shape"], source["window"]
    rows = positive(window["rows_N"], "rows_N") + positive(window["rows_A"], "rows_A")
    columns = positive(shape["metric_cols"], "metric_cols")
    kept = shape.get("metric_cols_after_preprocess")
    kept = positive(kept, "metric_cols_after_preprocess") if kept is not None else columns
    return {"raw_metric_cells": rows * columns, "processed_metric_cells": rows * kept,
            "metric_cols": columns, "processed_metric_cols": kept,
            "frozen_wall_s": positive(source["source_cost"]["wall_s"], "cost/wall_s")}


def estimates(sources, pilot_check, monitor, source_checks_s):
    import psutil
    pilot = scale_inputs(next(s for s in sources if s["opaque_id"] == PILOT_ID))
    wall = positive(monitor["elapsed_s"], "supervisor/elapsed_s")
    peak = positive(monitor["peak_tree_rss_bytes"], "supervisor/peak_tree_rss_bytes")
    controller = psutil.Process().memory_info().rss
    source_overhead = source_checks_s / len(sources)
    rows = []
    for source in sources:
        if source["opaque_id"] == PILOT_ID:
            continue
        size = scale_inputs(source)
        shape_factor = max(1.0, *(size[k] / pilot[k] for k in
                                  ("raw_metric_cells", "processed_metric_cells", "processed_metric_cols")))
        time_factor = max(shape_factor, size["frozen_wall_s"] / pilot["frozen_wall_s"])
        rows.append({"opaque_id": source["opaque_id"], "source_pointers": source["source_pointers"],
                     "scale_inputs": size, "shape_factor": shape_factor, "time_factor": time_factor,
                     "estimated_worker_and_verification_s": (wall + pilot_check["verification_s"]) * time_factor + source_overhead,
                     "estimated_logical_bytes": math.ceil(pilot_check["logical_bytes"] * shape_factor),
                     "estimated_allocated_file_bytes": math.ceil(pilot_check["allocated_file_bytes"] * shape_factor),
                     "estimated_worker_peak_rss_bytes": math.ceil(peak * shape_factor)})
    base_seconds = sum(r["estimated_worker_and_verification_s"] for r in rows)
    base_logical = sum(r["estimated_logical_bytes"] for r in rows)
    base_allocated = sum(r["estimated_allocated_file_bytes"] for r in rows)
    tree_peak = controller + max(r["estimated_worker_peak_rss_bytes"] for r in rows)
    return {"status": "ESTIMATE_NOT_MEASURED_QUEUE", "basis": {
                "pilot_check": pilot_check, "pilot_monitor": ref(PILOT_MONITOR),
                "pilot_supervisor_elapsed_s": wall, "pilot_supervisor_peak_tree_rss_bytes": peak,
                "controller_rss_observed_during_prepare_bytes": controller,
                "source_verification_s_measured": source_checks_s, "pilot_scale_inputs": pilot},
            "formula": "time=max(1, raw/processed metric-cell ratios, kept-column ratio, frozen-cost ratio) * (pilot supervisor wall + independent artifact verification) + average source-check time; bytes/worker RSS scale by shape ratios",
            "base_remaining": {"cases": len(rows), "wall_s": base_seconds, "logical_bytes": base_logical,
                               "allocated_file_bytes": base_allocated, "estimated_controller_plus_worker_rss_bytes": tree_peak},
            "operating_envelope_estimate": {"factor": 2, "wall_s": base_seconds * 2,
                       "logical_bytes": base_logical * 2, "allocated_file_bytes": base_allocated * 2,
                       "controller_plus_worker_rss_bytes": tree_peak * 2,
                       "note": "A declared unverified 2x engineering allowance, not a guaranteed bound or a method threshold; root reviews before launch."},
            "limits": ["One pilot cannot establish worst-case runtime/RAM or failure probability.",
                       "Captured file allocated bytes exclude directory-block overhead; controller logs/plans add bytes.",
                       "Frozen source cost was measured elsewhere and may scale differently on EC2.",
                       "Local result copies also consume the 8 GiB new-byte budget; supervisor applies root's local reservation.",
                       "No hard budget is set here; the outer run_guarded process enforces the authorized wall/disk/RAM limits."],
            "cases": rows}


def close_plan(directory, status):
    outputs = [file_row(p) for p in sorted(directory.iterdir()) if p.is_file() and p.name != "manifest.json"]
    for row in outputs:
        row["path"] = Path(row["path"]).name
    replay.dump(directory / "manifest.json", {"task": "T-032", "status": status, "at_utc": replay.now(),
                                               "outputs": outputs, "manifest_excludes": ["manifest.json"]})


def prepare(directory):
    audit = []
    started = time.perf_counter()
    replay.progress(directory, "PREPARE_START", pid=os.getpid())
    try:
        scripts = scripts_now()
        require(Path(__file__).resolve() == (SCRIPTS / "batch_baro.py").resolve(), "unexpected batch script location")
        ids = verified_main_ids(audit)
        sources, frozen_pilot, source_check_s = [], None, 0.0
        for oid in ids:
            source, frozen, elapsed = source_case(oid, audit)
            sources.append(source)
            source_check_s += elapsed
            if oid == PILOT_ID:
                frozen_pilot = frozen
            replay.progress(directory, "SOURCE_VERIFIED", opaque_id=oid, elapsed_s=elapsed)
        replay.external_sources(audit)
        pilot_source = next(s for s in sources if s["opaque_id"] == PILOT_ID)
        pilot = verify_output(PILOT, pilot_source, frozen_pilot, scripts)
        monitor = replay.read(PILOT_MONITOR)
        require(monitor.get("status") == "PASS" and monitor.get("exit_code") == 0, "pilot supervisor is not PASS")
        require(monitor.get("python") == sys.executable, "pilot supervisor interpreter differs")
        expected_command = [sys.executable, "-B", "-X", "utf8", str(SCRIPTS / "replay_baro.py"),
                            "one", "RE2-TT", PILOT_ID, str(PILOT)]
        require(monitor.get("command") == expected_command, "pilot supervisor command differs")
        cost_estimates = estimates(sources, pilot, monitor, source_check_s)
        remaining = [s["opaque_id"] for s in sources if s["opaque_id"] != PILOT_ID]
        require(len(remaining) == 29, "expected 29 remaining main records")
        plan = {"schema": "T-032.baro-batch-plan.v1", "task": "T-032", "dataset": "RE2-TT",
                "method": "baro", "variant": "native", "at_utc": replay.now(),
                "selection": "All 30 main/native index IDs; ascending opaque_id for queue order only.",
                "main_ids": ids, "remaining_ids": remaining, "reuse_ids": [PILOT_ID], "sources": sources,
                "scripts": scripts, "environment": environment(), "pilot": pilot,
                "pilot_monitor": file_row(PILOT_MONITOR),
                "sources_authority": {name: file_row(replay.safe_source(name))
                                      for name in (replay.M24, replay.I24, replay.M26, replay.I26)},
                "execution": {"workers": 1, "child_new_session": False, "retry": False,
                              "fail_stop": True, "guard": "Root launches run via run_guarded.py.",
                              "core_eligibility": "each worker check PASS, exact frozen fields, all byte hashes and capture restoration PASS"}}
        replay.dump(directory / "plan.json", plan)
        replay.dump(directory / "estimates.json", cost_estimates)
        replay.dump(directory / "source-checks.json", {"checks": audit})
        replay.progress(directory, "PREPARE_PASS", main=30, reused=1, remaining=29,
                        elapsed_s=time.perf_counter() - started, research_workers_launched=0)
        close_plan(directory, "PASS_PREPARED_NOT_STARTED")
        print(canonical({"status": "PASS_PREPARED_NOT_STARTED", "plan": str(directory),
                         "remaining": 29, "estimate": cost_estimates["operating_envelope_estimate"]}), flush=True)
        return 0
    except BaseException as exc:
        replay.dump(directory / "failure.json", {"status": "FAIL", "at_utc": replay.now(), "error": str(exc),
                    "traceback": traceback.format_exc(), "verified_checks": audit, "workers_launched": 0})
        replay.progress(directory, "PREPARE_FAILED", error=str(exc))
        close_plan(directory, "FAIL")
        return 1


def verified_plan(directory):
    directory = inside_run(directory)
    manifest = replay.read(directory / "manifest.json")
    require(manifest.get("status") == "PASS_PREPARED_NOT_STARTED", "plan preparation was not PASS")
    require(manifest.get("manifest_excludes") == ["manifest.json"], "unexpected plan exclusions")
    names = {row["path"] for row in manifest["outputs"]}
    require(len(names) == len(manifest["outputs"]), "duplicate plan artifact")
    require({p.name for p in directory.iterdir() if p.is_file()} == names | {"manifest.json"},
            "unlisted/missing plan artifact")
    for row in manifest["outputs"]:
        path = relative_artifact(directory, row["path"])
        require(path.stat().st_size == row["bytes"] and replay.sha(path) == row["sha256"], "plan hash/size mismatch")
    plan = replay.read(directory / "plan.json")
    require(plan["schema"] == "T-032.baro-batch-plan.v1" and plan["dataset"] == "RE2-TT" and
            plan["method"] == "baro" and plan["variant"] == "native", "wrong batch-plan scope")
    require(plan["reuse_ids"] == [PILOT_ID] and len(plan["main_ids"]) == 30 and
            len(set(plan["main_ids"])) == 30 and len(plan["remaining_ids"]) == 29 and
            sorted(plan["remaining_ids"] + plan["reuse_ids"]) == plan["main_ids"], "invalid complete-main queue")
    require(environment() == plan["environment"], "controller environment differs from prepared plan")
    verify_scripts(plan["scripts"])
    for item in plan["sources_authority"].values():
        require(replay.sha(Path(item["path"])) == item["sha256"], "frozen source authority changed")
    return plan


def atomic_status(directory, state):
    temporary = directory / "status.tmp"
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(directory / "status.json")


def run(plan_directory, directory):
    started, child, audit = time.perf_counter(), None, []
    state = {"status": "STARTING", "at_utc": replay.now(), "controller_pid": os.getpid(),
             "process_group": os.getpgrp(), "plan_dir": str(plan_directory), "batch_dir": str(directory),
             "completed_ids": [], "reused_ids": [], "active_opaque_id": None, "active_child_pid": None}
    replay.dump(directory / "invocation.json", {"argv": sys.argv, "python": sys.executable,
                "at_utc": replay.now(), "pid": os.getpid(), "process_group": os.getpgrp(),
                "batch_script_sha256": replay.sha(Path(__file__)), "automatic_retry": False})
    (directory / "controller.pid").write_text(str(os.getpid()) + "\n", encoding="ascii")

    def event(stage, **fields):
        state.update(updated_utc=replay.now(), elapsed_s=time.perf_counter() - started)
        atomic_status(directory, state)
        replay.progress(directory, stage, **fields, state=state)

    def interrupted(number, frame):
        raise BatchError("controller received signal " + str(number))

    def stop_child():
        if child is not None and child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=8)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    event("BATCH_START")
    try:
        plan = verified_plan(plan_directory)
        ids = verified_main_ids(audit)
        require(ids == plan["main_ids"], "main cohort changed after plan")
        source_by_id = {row["opaque_id"]: row for row in plan["sources"]}
        require(set(source_by_id) == set(ids) and len(plan["sources"]) == 30, "missing/duplicate plan source")
        replay.external_sources(audit)
        source, frozen, _ = source_case(PILOT_ID, audit)
        require(source == source_by_id[PILOT_ID], "pilot frozen source changed after plan")
        reuse = verify_output(PILOT, source, frozen, plan["scripts"])
        require(reuse["check"]["sha256"] == plan["pilot"]["check"]["sha256"] and
                reuse["artifact_manifest_sha256"] == plan["pilot"]["artifact_manifest_sha256"], "pilot changed after plan")
        require(replay.sha(PILOT_MONITOR) == plan["pilot_monitor"]["sha256"], "pilot supervisor changed after plan")
        replay.dump(directory / "reuse-pilot.json", reuse)
        state.update(status="RUNNING", reused_ids=[PILOT_ID], plan_sha256=replay.sha(plan_directory / "plan.json"),
                     plan_manifest_sha256=replay.sha(plan_directory / "manifest.json"), planned_remaining=29)
        event("PILOT_REUSE_VERIFIED", opaque_id=PILOT_ID, check_sha256=reuse["check"]["sha256"])
        (directory / "logs").mkdir()
        (directory / "cases").mkdir()
        (directory / "verified").mkdir()
        for index, oid in enumerate(plan["remaining_ids"]):
            verify_scripts(plan["scripts"])
            source, frozen, source_elapsed = source_case(oid, audit)
            require(source == source_by_id[oid], "frozen code/config/record changed: " + oid)
            case_dir = directory / "cases" / oid
            require(not case_dir.exists(), "case directory already exists; no retry/resume")
            command = [sys.executable, "-B", "-X", "utf8", str(SCRIPTS / "replay_baro.py"),
                       "one", "RE2-TT", oid, str(case_dir)]
            launch_path = directory / "logs" / (oid + ".launch.json")
            stdout_path = directory / "logs" / (oid + ".stdout.txt")
            stderr_path = directory / "logs" / (oid + ".stderr.txt")
            state.update(active_opaque_id=oid, active_child_pid=None, queue_index=index,
                         stdout=str(stdout_path), stderr=str(stderr_path), case_dir=str(case_dir))
            event("CASE_SOURCE_VERIFIED", opaque_id=oid, source_sha256=source["entry"]["sha256"])
            case_start = time.perf_counter()
            with stdout_path.open("x", encoding="utf-8") as stdout, stderr_path.open("x", encoding="utf-8") as stderr:
                child = subprocess.Popen(command, cwd=BASE, env=dict(os.environ), stdout=stdout, stderr=stderr,
                                         stdin=subprocess.DEVNULL, start_new_session=False)
                child_group = os.getpgid(child.pid)
                require(child_group == os.getpgrp(), "worker unexpectedly left controller process group")
                state["active_child_pid"] = child.pid
                replay.dump(launch_path, {"at_utc": replay.now(), "command": command, "pid": child.pid,
                            "process_group": child_group, "start_new_session": False,
                            "source_sha256": source["entry"]["sha256"], "stdout": str(stdout_path), "stderr": str(stderr_path)})
                (directory / "logs" / (oid + ".pid")).write_text(str(child.pid) + "\n", encoding="ascii")
                event("CASE_STARTED", opaque_id=oid, child_pid=child.pid)
                while child.poll() is None:
                    try:
                        child.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        event("CASE_RUNNING", opaque_id=oid, worker_elapsed_s=time.perf_counter() - case_start)
            worker_elapsed = time.perf_counter() - case_start
            require(child.returncode == 0, "worker exited nonzero; stop queue at " + oid)
            checked = verify_output(case_dir, source, frozen, plan["scripts"])
            verify_scripts(plan["scripts"])
            case_summary = {"status": "PASS", "opaque_id": oid, "queue_index": index,
                            "source": source["entry"], "source_sha256": source["entry"]["sha256"],
                            "source_verification_s": source_elapsed, "worker_elapsed_s": worker_elapsed,
                            "total_case_elapsed_s": time.perf_counter() - case_start,
                            "worker_pid": child.pid, "worker_exit_code": child.returncode,
                            "output": checked, "stdout": file_row(stdout_path), "stderr": file_row(stderr_path),
                            "new_measured_cost": replay.read(case_dir / "cost.json")}
            replay.dump(directory / "verified" / (oid + ".json"), case_summary)
            with (directory / "completed-cases.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(canonical(case_summary) + "\n")
            state["completed_ids"].append(oid)
            state.update(active_opaque_id=None, active_child_pid=None)
            event("CASE_PASS", opaque_id=oid, worker_elapsed_s=worker_elapsed,
                  check_sha256=checked["check"]["sha256"], logical_bytes=checked["logical_bytes"])
            child = None
        require(state["completed_ids"] == plan["remaining_ids"], "incomplete batch")
        replay.dump(directory / "source-checks.json", {"checks": audit})
        state.update(status="PASS", remaining_ids=[], n_main_valid=30)
        event("BATCH_PASS", reused=1, newly_verified=29)
        replay.dump(directory / "manifest.json", {"status": "PASS", "task": "T-032", "at_utc": replay.now(),
                    "plan": file_row(plan_directory / "plan.json"), "pilot_reuse": file_row(directory / "reuse-pilot.json"),
                    "completed_cases": file_row(directory / "completed-cases.jsonl"),
                    "source_checks": file_row(directory / "source-checks.json"),
                    "n_main_valid": 30, "reused": 1, "newly_verified": 29,
                    "evidence": "Each completed-cases row links a checked full artifact manifest; this is replay completeness, not mechanism confirmation."})
        return 0
    except BaseException as exc:
        stop_child()
        state.update(status="STOPPED", error=str(exc),
                     child_exit_code=None if child is None else child.returncode,
                     active_child_pid=None)
        replay.dump(directory / "failure.json", {"status": "STOPPED", "at_utc": replay.now(), "error": str(exc),
                    "traceback": traceback.format_exc(), "verified_source_checks": audit,
                    "no_retry": True, "remaining_work": "Resume only with a separately reviewed new plan/run; keep this failed run."})
        event("BATCH_STOPPED", error=str(exc))
        return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("new_plan_dir")
    execution = sub.add_parser("run")
    execution.add_argument("plan_dir")
    execution.add_argument("new_batch_dir")
    args = parser.parse_args()
    require(os.name == "posix" and BASE == Path("/home/ubuntu/rca/T-032"), "research batch may run only in approved EC2 layout")
    require(sys.executable == "/home/ubuntu/rca/T-025/envs/main/bin/python", "use the pilot's approved interpreter")
    require(os.environ.get("PYTHONHASHSEED") == "0" and os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "launch with the approved hashseed and bytecode-disabled environment")
    return prepare(new_run(args.new_plan_dir)) if args.command == "prepare" else run(
        inside_run(args.plan_dir), new_run(args.new_batch_dir))


if __name__ == "__main__":
    raise SystemExit(main())
