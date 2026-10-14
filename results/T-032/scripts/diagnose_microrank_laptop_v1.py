"""One approved laptop diagnostic, with a historical-thread evidence gate.

The source thread environment is OPEN. This preparation cannot start either
method call until that evidence/exception has been separately approved and
recorded in a new reviewed wrapper version. Current unset values are not a
claim about the historical frozen run. No CLI switch bypasses this gate.

Only the declared case is supported: native -> frozen exact, then observed
only if native passed. The original comparator and capture verifier are used
without numerical tolerance; Windows cost measurement is wrapper metadata.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import traceback

REPO = Path("D:/RCA-flashticket")
SCRIPTS = REPO / "results/T-032/scripts"
OUT = REPO / "results/T-032/runs/microrank-laptop-diagnostic-001"
PYTHON = Path("D:/RCA-ext/envs/T-014-main/Scripts/python.exe")
OID = "dev-3defe3d34b"
DATASET = "RE2-TT"
MAX_WALL_S = 600
MAX_NEW_BYTES = 150 * 1024 * 1024
MAX_TASK_BYTES = 8 * 1024 * 1024 * 1024
MAX_TREE_RSS = 2 * 2143158272
MIN_AVAILABLE_RAM = MAX_TREE_RSS + 256 * 1024 * 1024
MIN_REMAINING_RAM = 256 * 1024 * 1024
RESERVE_BYTES = 64 * 1024
POLL_S = 0.5
THREAD_NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
# Missing historical recording is not equivalent to historically unset.
SOURCE_THREAD_ENV = None
SOURCE_THREAD_AUTHORITY = None
SOURCE_EVIDENCE_SEARCHED = (
    "results/T-031/moi-truong.json",
    "results/T-031/scripts/chay.py",
    "results/T-031/runs/microrank-30-001/cau-hinh.json",
    "results/T-031/runs/microrank-30-001/luot/microrank-a-dev-3defe3d34b-sNone-h0-d38dd0/ban-ghi-0.json",
    "results/T-024: *.json and *.py, excluding tests/test/test_*.py",
    "results/T-022: *.json and *.py, excluding tests/test/test_*.py",
)
PACKAGES = {"numpy": "1.26.4", "pandas": "2.2.3", "scikit-learn": "1.6.0",
            "scipy": "1.14.1", "pyarrow": "18.1.0", "psutil": "6.1.1", "networkx": "2.8.8"}
PINS = {
    "results/T-032/scripts/replay_microrank.py": "193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562",
    "results/T-032/scripts/capture_microrank.py": "b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b",
    "results/T-031/moi-truong.json": "52e08f0d1d169b504716a246d3404bb9ec124dea46505fbaa8c0bb474f591e2d",
    "results/T-022/allowlist-dev.json": "fec512d7dbf059b86c7049127c9fd7a899f3e6508d8ba472b160867b74e32ac3",
    "results/T-029/runs/compare-rca-preparation-001/manifest.json": "51498845f1e070017ec52c3b6550b84c444882af7c09aa31564d93c58972c2a8",
    "results/T-026/runs/session-005/handoff-manifest.json": "675092feac86d62908fb6a83f1356a2fc1ab128c717c4018f50433710abb7366",
}


class DiagnosticError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise DiagnosticError(message)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    def reject(token):
        raise DiagnosticError("nonfinite JSON token: " + token)
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), parse_constant=reject)


def dump_new(path, value):
    path = Path(path)
    require(OUT.resolve() in path.resolve().parents, "output escaped the one approved run")
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def logical_size(directory):
    total = 0
    for parent, dirs, names in os.walk(directory):
        require(not Path(parent).is_symlink(), "symlink in diagnostic output")
        for name in dirs:
            require(not (Path(parent) / name).is_symlink(), "symlink directory in diagnostic output")
        for name in names:
            path = Path(parent) / name
            require(not path.is_symlink(), "symlink file in diagnostic output")
            try:
                total += path.stat().st_size
            except FileNotFoundError:
                pass
    return total


def progress(stage, **fields):
    event = {"at_utc": now(), "stage": stage, **fields}
    with (OUT / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps(event, ensure_ascii=False, allow_nan=False), flush=True)


def immutable_manifest(directory, excluded=()):
    excluded = set(excluded)
    return [{"path": path.relative_to(directory).as_posix(), "bytes": path.stat().st_size,
             "sha256": sha(path)} for path in sorted(directory.rglob("*"))
            if path.is_file() and path.relative_to(directory).as_posix() not in excluded]


def verify_manifest(directory, manifest):
    listed = set()
    for row in manifest:
        relative = row["path"]
        path = (directory / relative).resolve()
        require(directory.resolve() in path.parents and not path.is_symlink(), "unsafe artifact manifest path")
        require(relative not in listed, "duplicate artifact manifest path")
        listed.add(relative)
        require(path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], "artifact changed: " + relative)
    actual = {path.relative_to(directory).as_posix() for path in directory.rglob("*") if path.is_file()}
    require(actual == listed | {"check.json"}, "artifact manifest is incomplete")


def source_pins():
    audit = []
    for relative, expected in sorted(PINS.items()):
        path = (REPO / relative).resolve()
        require(REPO.resolve() in path.parents and path.is_file() and not path.is_symlink(), "unsafe/missing pinned source")
        actual = sha(path)
        audit.append({"path": relative, "expected_sha256": expected, "actual_sha256": actual,
                      "bytes": path.stat().st_size, "pass": actual == expected})
        require(actual == expected, "pinned source changed: " + relative)
    return audit


def environment_metadata():
    versions = {name: importlib.metadata.version(name) for name in PACKAGES}
    return {"at_utc": now(), "python": sys.version, "version_tuple": list(sys.version_info[:3]),
            "executable": sys.executable, "prefix": sys.prefix, "base_prefix": sys.base_prefix,
            "packages": versions, "hashseed": os.environ.get("PYTHONHASHSEED"),
            "pythonpath": os.environ.get("PYTHONPATH"),
            "thread_environment_current": {name: os.environ.get(name) for name in THREAD_NAMES},
            "threadpool_status": "not initialized during historical-thread preflight",
            "source_thread_environment": SOURCE_THREAD_ENV,
            "source_thread_authority": SOURCE_THREAD_AUTHORITY,
            "source_thread_status": "OPEN" if SOURCE_THREAD_ENV is None else "RECORDED",
            "current_values_are_historical_evidence": False}


def environment_guard(metadata):
    require(os.name == "nt", "approved diagnostic is restricted to the source Windows laptop")
    require(Path(sys.executable).resolve() == PYTHON.resolve(), "different Python executable")
    require(tuple(sys.version_info[:3]) == (3, 12, 10), "source requires Python 3.12.10")
    require(metadata["packages"] == PACKAGES, "source package versions differ")
    require(os.environ.get("PYTHONHASHSEED") == "0", "hashseed must be zero at process startup")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1" and sys.dont_write_bytecode,
            "bytecode must be disabled")
    require(sys.gettrace() is None and sys.getprofile() is None, "pre-existing trace/profile hook")
    require(SOURCE_THREAD_ENV is not None and SOURCE_THREAD_AUTHORITY is not None,
            "source_thread_env is OPEN: FAIL_STOP before native; current unset is not historical evidence")
    require(isinstance(SOURCE_THREAD_ENV, dict) and set(SOURCE_THREAD_ENV) == set(THREAD_NAMES),
            "historical thread environment schema is incomplete")
    require(metadata["thread_environment_current"] == SOURCE_THREAD_ENV,
            "current thread variables differ from the recorded source")


def replay_module():
    # Path binding only: original helper files and computation remain unchanged.
    replay = importlib.import_module("replay_microrank")
    require(Path(replay.__file__).resolve() == (SCRIPTS / "replay_microrank.py").resolve(), "wrong replay import")
    require(sha(replay.__file__) == PINS["results/T-032/scripts/replay_microrank.py"], "replay import hash differs")
    capture = importlib.import_module("capture_microrank")
    require(Path(capture.__file__).resolve() == (SCRIPTS / "capture_microrank.py").resolve(), "wrong capture import")
    require(sha(capture.__file__) == PINS["results/T-032/scripts/capture_microrank.py"], "capture import hash differs")
    replay.REPO = REPO
    replay.RE2_RAW_REPO = REPO
    return replay


def expected_job(replay, frozen):
    from p3 import selector
    allow = selector.nap_allowlist(replay.safe_source("results/T-022/allowlist-dev.json"))
    require(OID in allow, "case is not in the approved dev allowlist")
    wanted = {name: meta["sha256"] for name, meta in allow[OID]["files"].items() if meta is not None}
    require(wanted == frozen["input_sha256"], "allowlist input hashes differ from frozen")
    selected = selector.chon_ca(allow, OID, REPO, kiem_hash=True)
    return {"kind": "ranker", "method": "microrank", "t": frozen["window"]["t"],
            "model": None, "files": {name: {"path": path, "sha256": wanted[name]}
                                      for name, path in selected.items()}}


def verify_inputs(job, frozen):
    result = []
    require({name: meta["sha256"] for name, meta in job["files"].items()} == frozen["input_sha256"],
            "job inputs differ from frozen")
    raw_root = (REPO / "data/rcaeval").resolve()
    for name, meta in job["files"].items():
        path = Path(meta["path"]).resolve()
        require(raw_root in path.parents and not path.is_symlink(), "input escaped approved raw dev root")
        require(not any(part.lower() in ("test", "tests", "locked", "t-033") for part in path.parts), "forbidden input")
        actual = sha(path)
        require(actual == meta["sha256"], "input hash changed: " + name)
        result.append({"name": name, "sha256": actual, "bytes": path.stat().st_size, "pass": True})
    return result


def function_snapshot():
    import microrank
    functions = {"microrank": microrank.microrank,
                 "get_pagerank_graph": microrank.get_pagerank_graph,
                 "trace_pagerank": microrank.trace_pagerank,
                 "calculate_spectrum_without_delay_list": microrank.calculate_spectrum_without_delay_list,
                 "spectrum_cells": microrank.spectrum_cells, "pageRank": microrank.official.pageRank}
    return {name: {"identity": id(function), "code_file": function.__code__.co_filename,
                   "function_name": function.__name__} for name, function in functions.items()}


def measured_windows_cost(started):
    import psutil
    process = psutil.Process()
    memory = process.memory_info()
    io = process.io_counters()
    return {"wall_s": round(time.perf_counter() - started, 6),
            "peak_rss_mb": getattr(memory, "peak_wset", memory.rss) / (1024.0 * 1024.0),
            "read_bytes": io.read_bytes, "write_bytes": io.write_bytes,
            "exit_code": 0, "timed_out": False, "env": "T-032-laptop-single-case",
            "hashseed": 0, "measurement_note": "Windows process lifetime peak working set/IO; worker wall includes observation only in observed child"}


def child(mode, directory, job_sha256, frozen_sha256):
    require(mode in ("native", "observed"), "unsupported child mode")
    directory = Path(directory).resolve()
    require(directory == OUT.resolve() / mode, "child output outside exact approved run")
    require(directory.is_dir() and {path.name for path in directory.iterdir()} == {"job.json"}, "child requires a new job-only directory")
    require(sha(directory / "job.json") == job_sha256, "parent job bytes changed")
    # Guard applies to direct child invocation too; no method import before it.
    source_pins()
    metadata = environment_metadata()
    environment_guard(metadata)
    replay = replay_module()
    audit = []
    try:
        entry, frozen, _index, code_hashes = replay.source_for(DATASET, OID, audit)
        require(entry["sha256"] == frozen_sha256, "child frozen binding changed")
        job = expected_job(replay, frozen)
        require(not replay.exact_differences(job, read(directory / "job.json")), "child job differs from verified expected job")
        before_inputs = verify_inputs(job, frozen)
        from p3 import worker, runner
        import microrank
        before = function_snapshot()
        imports_before = replay.loaded_sources(code_hashes)
        from threadpoolctl import threadpool_info
        dump_new(directory / "source.json", {"entry": entry, "source_checks": audit,
                 "input_checks_before": before_inputs, "actual_imports_before": imports_before,
                 "job_sha256": job_sha256, "frozen_sha256": frozen_sha256,
                 "observer_attached": mode == "observed", "environment": metadata,
                 "threadpools_current_before": threadpool_info(), "functions_before": before})
        started = time.perf_counter()
        capture_summary = None
        with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout:
            with (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    if mode == "native":
                        worker.main(str(directory / "job.json"), str(directory / "ket-qua.json"))
                    else:
                        # The frozen observer context, without method replacement.
                        with replay.MicroRankCapture(directory / "capture") as capture:
                            worker.main(str(directory / "job.json"), str(directory / "ket-qua.json"))
                        capture_summary = capture.require_complete()
        cost = measured_windows_cost(started)
        dump_new(directory / "cost.json", cost)
        require(sys.gettrace() is None and sys.getprofile() is None, "worker left a trace/profile hook")
        require(function_snapshot() == before, "worker changed method function identities")
        output = read(directory / "ket-qua.json")
        require(output.get("hashseed") == "0", "worker hashseed differs")
        base = {"run_id": directory.name, "opaque_id": OID, "mode": "a", "seed": None,
                "hashseed": 0, "detector": None, "detector_columns": None, "config_id": "p3-re2tt-v2"}
        records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "microrank", "a")
        require(len(records) == 1, "RE2 reconstruction did not return exactly one record")
        record = read(directory / "ban-ghi-0.json")
        require(record["input_sha256"] == frozen["input_sha256"], "worker input hashes differ from frozen")
        differences = replay.compare_records(frozen, record)
        capture_check = None
        if mode == "observed":
            require(capture_summary["status"] == "captured_unverified_replay", "observer summary did not complete")
            capture_check = replay.verify_capture(directory / "capture", capture_summary)
            require(capture_check["pass"] is True, "capture verification failed")
        after_inputs = verify_inputs(job, frozen)
        _entry_after, _frozen_after, _index_after, after_hashes = replay.source_for(DATASET, OID, audit)
        require(after_hashes == code_hashes, "source code binding changed")
        require(not replay.exact_differences(frozen, _frozen_after), "frozen record changed")
        pin_after = source_pins()
        imports_after = replay.loaded_sources(code_hashes)
        dump_new(directory / "source-checks.json", {"checks": audit, "pin_checks_after": pin_after,
                 "input_checks_after": after_inputs, "actual_imports_after": imports_after,
                 "functions_unchanged": True, "hooks_restored": True,
                 "threadpools_current_after": threadpool_info()})
        dump_new(directory / "check.json", {"status": "PASS" if not differences else "FAIL_STOP",
                 "mode": mode, "dataset": DATASET, "opaque_id": OID,
                 "frozen_sha256": frozen_sha256, "job_sha256": job_sha256,
                 "exact_fields": replay.EXACT_FIELDS, "excluded_fields": replay.EXCLUDED_FIELDS,
                 "differences": differences, "native_observer_absent": mode == "native",
                 "capture_status": None if capture_summary is None else capture_summary["status"],
                 "capture_check": capture_check, "source_checks_passed": True,
                 "artifact_manifest": immutable_manifest(directory),
                 "intermediates_eligible": False, "cohort_resume_authorized": False, "a_prime_authorized": False})
        return 0 if not differences else 1
    except BaseException as error:
        if not (directory / "failure.json").exists():
            dump_new(directory / "failure.json", {"status": "FAIL_STOP", "type": type(error).__name__,
                     "error": str(error), "traceback": traceback.format_exc(), "source_checks": audit,
                     "intermediates_eligible": False, "retained": "no retry; all partial artifacts retained"})
        return 1


class Guard:
    def __init__(self, started, other_task_bytes):
        import psutil
        self.psutil = psutil
        self.started = started
        self.other_task_bytes = other_task_bytes
        self.peak_bytes = 0
        self.peak_tree_rss = 0
        self.child = None
        self.interrupted = None

    def check(self, reserve_seconds=20):
        require(self.interrupted is None, "interrupted: " + str(self.interrupted))
        require(time.perf_counter() - self.started <= MAX_WALL_S - reserve_seconds, "group wall budget reached")
        size = logical_size(OUT)
        self.peak_bytes = max(self.peak_bytes, size)
        require(size <= MAX_NEW_BYTES - RESERVE_BYTES, "150 MiB new-byte budget reached")
        require(self.other_task_bytes + size <= MAX_TASK_BYTES - RESERVE_BYTES, "8 GiB combined task-byte budget reached")
        require(shutil.disk_usage(OUT).free >= MAX_NEW_BYTES - size + RESERVE_BYTES, "insufficient disk for remaining diagnostic budget")
        require(self.psutil.virtual_memory().available >= MIN_REMAINING_RAM, "remaining laptop RAM below guard reserve")
        if self.child is not None and self.child.poll() is None:
            try:
                process = self.psutil.Process(self.child.pid)
                processes = [process] + process.children(recursive=True)
                rss = sum(process.memory_info().rss for process in processes if process.is_running())
                self.peak_tree_rss = max(self.peak_tree_rss, rss)
                require(rss <= MAX_TREE_RSS, "method child RSS exceeded approved RAM estimate")
            except self.psutil.NoSuchProcess:
                pass

    def interrupt(self, signum, _frame):
        self.interrupted = signum

    def stop_child(self):
        if self.child is None or self.child.poll() is not None:
            return
        try:
            parent = self.psutil.Process(self.child.pid)
            processes = parent.children(recursive=True) + [parent]
            for process in processes:
                try:
                    process.terminate()
                except self.psutil.NoSuchProcess:
                    pass
            _gone, alive = self.psutil.wait_procs(processes, timeout=5)
            for process in alive:
                try:
                    process.kill()
                except self.psutil.NoSuchProcess:
                    pass
            self.child.wait(timeout=5)
        except self.psutil.NoSuchProcess:
            pass

    def report(self):
        return {"max_wall_s": MAX_WALL_S, "max_new_bytes": MAX_NEW_BYTES,
                "elapsed_s": time.perf_counter() - self.started, "new_bytes_now": logical_size(OUT),
                "peak_measured_new_bytes": self.peak_bytes, "peak_tree_rss": self.peak_tree_rss,
                "other_task_bytes": self.other_task_bytes, "poll_s": POLL_S,
                "quota_claimed": False, "polling_can_overshoot": True}


def run_child(guard, replay, mode, job, entry, frozen):
    guard.check()
    directory = OUT / mode
    directory.mkdir(exist_ok=False)
    if mode == "native":
        dump_new(directory / "job.json", job)
    else:
        shutil.copyfile(OUT / "native/job.json", directory / "job.json")
        require(sha(directory / "job.json") == sha(OUT / "native/job.json"), "observed job copy not byte-identical")
    job_sha256 = sha(directory / "job.json")
    command = [str(PYTHON), "-B", "-W", "ignore", "-X", "utf8", str(Path(__file__).resolve()),
               "child", mode, str(directory), job_sha256, entry["sha256"]]
    dump_new(OUT / (mode + "-command.json"), {"argv": command, "at_utc": now(), "mode": mode,
             "wrapper_sha256": sha(__file__), "job_sha256": job_sha256, "frozen_sha256": entry["sha256"]})
    with (OUT / (mode + "-stdout.txt")).open("x", encoding="utf-8") as stdout:
        with (OUT / (mode + "-stderr.txt")).open("x", encoding="utf-8") as stderr:
            started = time.perf_counter()
            guard.child = subprocess.Popen(command, cwd=str(REPO), env=os.environ.copy(), stdout=stdout,
                    stderr=stderr, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            dump_new(OUT / (mode + "-pid.json"), {"pid": guard.child.pid, "at_utc": now(), "argv": command})
            progress("CHILD_STARTED", mode=mode, pid=guard.child.pid)
            while guard.child.poll() is None:
                guard.check()
                time.sleep(POLL_S)
            exit_code = guard.child.wait()
            dump_new(OUT / (mode + "-process-cost.json"), {"mode": mode, "wall_s": time.perf_counter() - started,
                     "exit_code": exit_code, "tree_peak_rss_so_far": guard.peak_tree_rss})
    guard.check()
    require(exit_code == 0, mode + " child failed; no next child or retry")
    check = read(directory / "check.json")
    require(check["status"] == "PASS" and check["differences"] == [], mode + " frozen exact check failed")
    require(check["job_sha256"] == job_sha256 and check["frozen_sha256"] == entry["sha256"], "child source/job binding differs")
    require(check["source_checks_passed"] is True, "child source check did not pass")
    verify_manifest(directory, check["artifact_manifest"])
    record = read(directory / "ban-ghi-0.json")
    require(not replay.compare_records(frozen, record), "parent exact frozen check differs")
    if mode == "observed":
        require(check["capture_status"] == "captured_unverified_replay" and check["capture_check"]["pass"] is True, "observed capture check did not pass")
        require(not replay.compare_records(read(OUT / "native/ban-ghi-0.json"), record), "observed/native exact comparison failed")
    else:
        require(check["native_observer_absent"] is True, "native observer absence check failed")
    progress("CHILD_VALIDATED", mode=mode, exact=True)
    return check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--other-task-bytes", type=int, required=True,
                     help="root measured combined local+EC2 T-032 bytes excluding this new diagnostic")
    inner = sub.add_parser("child")
    inner.add_argument("mode", choices=("native", "observed"))
    inner.add_argument("directory")
    inner.add_argument("job_sha256")
    inner.add_argument("frozen_sha256")
    args = parser.parse_args()
    if args.command == "child":
        return child(args.mode, args.directory, args.job_sha256, args.frozen_sha256)
    # Only the approved launcher may bootstrap this exact new directory.
    require(OUT.is_dir() and not OUT.is_symlink(), "launcher must create the exact approved output")
    allowed_bootstrap = {"launcher.json", "launcher.pid", "controller-stdout.txt", "controller-stderr.txt"}
    require({path.name for path in OUT.iterdir()} <= allowed_bootstrap and (OUT / "launcher.json").is_file(),
            "run contains old/non-launcher artifacts; reuse/retry rejected")
    started = time.perf_counter()
    guard = None
    launched = []
    audit = []
    try:
        require(0 <= args.other_task_bytes <= MAX_TASK_BYTES - MAX_NEW_BYTES, "combined task byte budget insufficient")
        audit = source_pins()
        metadata = environment_metadata()
        dump_new(OUT / "environment.json", metadata)
        dump_new(OUT / "source_thread_evidence.json", {"status": "OPEN" if SOURCE_THREAD_ENV is None else "RECORDED",
                 "source_thread_env": SOURCE_THREAD_ENV, "source_thread_authority": SOURCE_THREAD_AUTHORITY,
                 "searched": list(SOURCE_EVIDENCE_SEARCHED), "historical_values_recovered": False,
                 "current_values": metadata["thread_environment_current"],
                 "current_values_are_historical_evidence": False,
                 "consequence": "FAIL_STOP before native until source evidence or separate exception is approved"})
        dump_new(OUT / "invocation.json", {"at_utc": now(), "argv": sys.argv, "pid": os.getpid(),
                 "script_sha256": sha(__file__), "source_pin_checks": audit,
                 "limits": {"max_wall_s": MAX_WALL_S, "max_new_bytes": MAX_NEW_BYTES,
                            "min_available_ram": MIN_AVAILABLE_RAM, "max_tree_rss": MAX_TREE_RSS},
                 "other_task_bytes": args.other_task_bytes, "native_calls_allowed": 1,
                 "observed_calls_allowed_only_after_native_exact": 1})
        progress("PREFLIGHT_STARTED", source_thread_status=metadata["source_thread_status"])
        environment_guard(metadata)
        import psutil
        require(psutil.virtual_memory().available >= MIN_AVAILABLE_RAM, "available laptop RAM below 4,554,752,000 bytes; no native launch")
        guard = Guard(started, args.other_task_bytes)
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, guard.interrupt)
        guard.check()
        for directory in (OUT / "tmp", OUT / "cache", OUT / "cache/mpl"):
            directory.mkdir(exist_ok=False)
        replay = replay_module()
        entry, frozen, _index, code_hashes = replay.source_for(DATASET, OID, audit)
        job = expected_job(replay, frozen)
        dump_new(OUT / "source.json", {"entry": entry, "source_status": frozen["status"], "source_checks": audit,
                 "actual_imports": replay.loaded_sources(code_hashes), "input_checks_before": verify_inputs(job, frozen),
                 "exact_fields": replay.EXACT_FIELDS, "excluded_fields": replay.EXCLUDED_FIELDS,
                 "replay_path_binding_only": {"REPO": str(REPO), "RE2_RAW_REPO": str(REPO)}})
        launched.append("native")
        native_check = run_child(guard, replay, "native", job, entry, frozen)
        # No catch/continue: any failed native/hash/cost check prevents observer.
        launched.append("observed")
        observed_check = run_child(guard, replay, "observed", job, entry, frozen)
        _entry_after, frozen_after, _index_after, after_hashes = replay.source_for(DATASET, OID, audit)
        require(after_hashes == code_hashes and not replay.exact_differences(frozen, frozen_after), "final frozen/code binding changed")
        dump_new(OUT / "final-source-checks.json", {"checks": audit, "pins_after": source_pins(),
                 "input_checks_after": verify_inputs(job, frozen), "actual_imports_after": replay.loaded_sources(code_hashes)})
        guard.check()
        progress("DIAGNOSTIC_EXACT_COMPLETE", native_observed_frozen_exact=True)
        dump_new(OUT / "check.json", {"status": "PASS_SINGLE_CASE_EXACT_DIAGNOSTIC", "dataset": DATASET,
                 "opaque_id": OID, "native_frozen_exact": native_check["differences"] == [],
                 "observed_frozen_exact": observed_check["differences"] == [], "native_observed_exact": True,
                 "calls_launched": launched, "guard": guard.report(),
                 "intermediates_eligible": False, "cohort_resume_authorized": False, "a_prime_authorized": False,
                 "report_use_requires_approved_why_addendum": True,
                 "interpretation": "single-case current-laptop exactness only; no cause of platform drift or historical partition inferred",
                 "artifact_manifest": immutable_manifest(OUT, ("check.json", "controller-stdout.txt", "controller-stderr.txt")),
                 "manifest_excludes": ["check.json", "controller-stdout.txt", "controller-stderr.txt"]})
        return 0
    except BaseException as error:
        if guard is not None:
            guard.stop_child()
        failure = {"status": "FAIL_STOP", "type": type(error).__name__, "error": str(error),
                   "traceback": traceback.format_exc(), "calls_launched": launched, "source_checks": audit,
                   "guard": None if guard is None else guard.report(), "intermediates_eligible": False,
                   "cohort_resume_authorized": False, "a_prime_authorized": False,
                   "retained": "all partial artifacts retained; no retry, tolerance or case fallback"}
        if not (OUT / "check.json").exists():
            dump_new(OUT / "check.json", failure)
        else:
            dump_new(OUT / "failure-after-check.json", failure)
        progress("FAIL_STOP", error=str(error), calls_launched=launched)
        return 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
