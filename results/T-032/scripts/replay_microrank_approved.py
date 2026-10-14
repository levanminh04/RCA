"""Minh-approved T-032 MicroRank exception, in a separate immutable-run wrapper.

one DATASET OPAQUE_ID NEW_RUN_DIRECTORY

Architecture: the unchanged, hash-pinned replay_microrank.one writes observed/
including its original exact PASS/FAIL check. A fresh native-child process runs
the identical job once without an observer. Only measured cost/run_id are
excluded from their exact comparison. The approved comparator and T-028 bridge
are posthoc. No label/bridge/comparator data are passed to either worker.

This wrapper does not override the old comparator, capture hook, method, source
files or previous runs. Capture is performed only once. Native process cost is
independent of the observed process's lifetime RSS. Benchmark guards are 600 s
and 150 MiB of logical output, with polling and possible byte overshoot; these
are operating limits, not diagnosis thresholds or a filesystem quota promise.
"""
from __future__ import annotations

import argparse
import contextlib
import gc
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import resource
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
SCRIPTS = BASE / "scripts"
PACKAGE = BASE / "inputs/package-manifest.json"
PACKAGE_SHA256 = "03919f7895fedfd2aac8affd11d256acc5a4696341fed5812ef73c8ce417dec4"
REPLAY_SHA256 = "193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562"
CAPTURE_SHA256 = "b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b"
COMPARATOR_SHA256 = "7e29b728bbd3c00174b962efd5896a50556d6aa0c68a2dea85e49e2b81ea64a2"
BRIDGE_SHA256 = "1c1205ffedca12a45221e6e7981f92fadf2f341a4918233504b459f03ec44cff"
MAX_WALL_S = 600
MAX_NEW_BYTES = 150 * 2**20
FINAL_LOG_RESERVE = 128 * 2**10
POLL_S = 0.5


class ApprovedReplayError(RuntimeError):
    pass


class OperatingLimit(ApprovedReplayError):
    pass


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    def reject(token):
        raise ApprovedReplayError("nonfinite JSON token: " + token)
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), parse_constant=reject)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def dump(path, value):
    with Path(path).open("xb") as destination:
        destination.write(encoded(value))


def verify(path, expected, authority, audit):
    if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
        raise ApprovedReplayError("missing/invalid dependency hash: " + str(path))
    path = Path(path).resolve()
    actual = sha(path)
    audit.append({"path": str(path), "authority": authority, "expected": expected,
                  "actual": actual, "pass": actual == expected, "bytes": path.stat().st_size})
    if actual != expected:
        raise ApprovedReplayError("hash mismatch: " + str(path))
    return path


def source_path(relative):
    p = PurePosixPath(relative)
    if (not isinstance(relative, str) or "\\" in relative or p.is_absolute()
            or any(part in (".", "..") for part in p.parts)
            or any(part.lower() in ("t-033", "locked", "test", "tests", "heldout", "archive") for part in p.parts)):
        raise ApprovedReplayError("source path outside approved read scope")
    path = (REPO / Path(*p.parts)).resolve()
    if REPO.resolve() not in path.parents:
        raise ApprovedReplayError("source escaped copied repository")
    return path


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def preflight(audit, with_posthoc=True):
    verify(PACKAGE, PACKAGE_SHA256, "frozen T-032 package anchor", audit)
    package = read(PACKAGE)
    entries = {row["path"]: row for row in package["files"]}
    if len(entries) != len(package["files"]):
        raise ApprovedReplayError("duplicate package source path")
    for relative in (
        "results/T-029/runs/compare-rca-preparation-001/manifest.json",
        "results/T-026/runs/session-005/handoff-manifest.json",
        "results/T-024/ban-ghi-dua-vao-cham.json",
        "results/T-026/ban-ghi-dua-vao-cham.json",
        "results/T-022/allowlist-dev.json",
    ):
        verify(source_path(relative), entries[relative]["sha256"], "package#/files", audit)
    replay_path = verify(SCRIPTS / "replay_microrank.py", REPLAY_SHA256, "pinned original replay", audit)
    capture_path = verify(SCRIPTS / "capture_microrank.py", CAPTURE_SHA256, "pinned original observer", audit)
    if with_posthoc:
        verify(SCRIPTS / "compare_microrank_roundoff.py", COMPARATOR_SHA256, "approved comparator handoff", audit)
        verify(SCRIPTS / "check_microrank_t028.py", BRIDGE_SHA256, "verified bridge handoff", audit)
    replay = load_module("t032_approved_original_replay", replay_path)
    actual_capture = Path(sys.modules[replay.MicroRankCapture.__module__].__file__).resolve()
    if actual_capture != capture_path:
        raise ApprovedReplayError("original replay imported a different capture module")
    verify(actual_capture, CAPTURE_SHA256, "actual observer import", audit)
    return replay


def environment_guard():
    if (sys.platform != "linux" or Path.home().resolve() != Path("/home/ubuntu")
            or Path(__file__).resolve().parent != SCRIPTS):
        raise ApprovedReplayError("EC2-only wrapper from the approved T-032 script directory")
    if os.environ.get("PYTHONHASHSEED") != "0":
        raise ApprovedReplayError("launch with frozen PYTHONHASHSEED=0")
    if sys.gettrace() is not None or sys.getprofile() is not None:
        raise ApprovedReplayError("pre-existing trace/profile hook rejected")
    sys.dont_write_bytecode = True
    soft, hard = resource.getrlimit(resource.RLIMIT_FSIZE)
    soft = MAX_NEW_BYTES if soft == resource.RLIM_INFINITY else min(soft, MAX_NEW_BYTES)
    resource.setrlimit(resource.RLIMIT_FSIZE, (soft, hard))


def new_run(raw):
    path = Path(raw).expanduser().resolve()
    if BASE / "runs" not in path.parents or path.exists():
        raise ApprovedReplayError("run must be a new directory below T-032/runs")
    if any(part.lower() in ("t-033", "locked", "test", "heldout", "archive") for part in path.parts):
        raise ApprovedReplayError("run path outside scope")
    path.mkdir(parents=False, exist_ok=False)
    return path


def logical_size(root):
    total = 0
    if Path(root).exists():
        for parent, dirs, names in os.walk(root):
            dirs[:] = [name for name in dirs if not (Path(parent) / name).is_symlink()]
            for name in names:
                path = Path(parent) / name
                if not path.is_symlink():
                    try:
                        total += path.stat().st_size
                    except FileNotFoundError:
                        pass
    return total


class BenchmarkGuard:
    def __init__(self, directory, started):
        self.directory, self.started = directory, started
        self.stop_event = threading.Event()
        self.peak_bytes = 0
        self.last_bytes = 0
        self.failure = None
        self.previous = {}
        self.thread = None

    def measured_bytes(self):
        # Standard stage launcher's monitor/launcher metadata are included when
        # their names correspond to this run. Unrelated existing runs are not.
        total = logical_size(self.directory)
        if self.directory.parent == BASE / "runs":
            total += logical_size(BASE / "runs" / (self.directory.name + "-monitor"))
            for suffix in ("-launcher.out", "-launcher.err", "-launcher.pid"):
                path = BASE / "runs" / (self.directory.name + suffix)
                if path.is_file():
                    total += path.stat().st_size
        self.last_bytes = total
        self.peak_bytes = max(self.peak_bytes, total)
        return total

    def check(self, reserve=0):
        count = self.measured_bytes()
        if count + reserve > MAX_NEW_BYTES:
            raise OperatingLimit("benchmark logical output byte limit exceeded: " + str(count))
        if time.perf_counter() - self.started > MAX_WALL_S:
            raise OperatingLimit("benchmark wall limit exceeded")
        if self.failure:
            raise OperatingLimit(self.failure)
        return count

    def _signal(self, signum, frame):
        raise OperatingLimit(self.failure or ("operating signal " + str(signum)))

    def _watch(self):
        while not self.stop_event.wait(POLL_S):
            try:
                self.check(FINAL_LOG_RESERVE)
            except BaseException as error:
                self.failure = str(error)
                os.kill(os.getpid(), signal.SIGUSR1)
                return

    def start(self):
        for signum in (signal.SIGUSR1, signal.SIGALRM, signal.SIGXFSZ):
            self.previous[signum] = signal.getsignal(signum)
            signal.signal(signum, self._signal)
        signal.setitimer(signal.ITIMER_REAL, max(0.01, MAX_WALL_S - (time.perf_counter() - self.started)))
        self.thread = threading.Thread(target=self._watch, name="T032-byte-guard", daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=2)
        signal.setitimer(signal.ITIMER_REAL, 0)
        for signum, previous in self.previous.items():
            signal.signal(signum, previous)
        self.measured_bytes()

    def report(self):
        return {"max_wall_s": MAX_WALL_S, "max_new_bytes": MAX_NEW_BYTES,
                "elapsed_s": time.perf_counter() - self.started,
                "last_measured_new_bytes": self.last_bytes, "peak_measured_new_bytes": self.peak_bytes,
                "poll_s": POLL_S, "per_file_RLIMIT_FSIZE": MAX_NEW_BYTES, "failure": self.failure,
                "quota_claimed": False,
                "note": "logical file sizes; polling can overshoot; partial failures are retained"}


def function_snapshot():
    import microrank
    pairs = {
        "microrank": microrank.microrank,
        "get_pagerank_graph": microrank.get_pagerank_graph,
        "trace_pagerank": microrank.trace_pagerank,
        "calculate_spectrum_without_delay_list": microrank.calculate_spectrum_without_delay_list,
        "spectrum_cells": microrank.spectrum_cells,
        "pageRank": microrank.official.pageRank,
    }
    return {name: {"identity": id(function), "code_file": function.__code__.co_filename,
                   "function_name": function.__name__} for name, function in pairs.items()}


def expected_job(replay, dataset, opaque_id, entry, frozen, index26, audit):
    """The same source/selector/job construction as the original one()."""
    from p3 import selector
    if dataset == "RE2-TT":
        path = replay.safe_source("results/T-022/allowlist-dev.json")
        allow = selector.nap_allowlist(path)
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
        if wanted != frozen["input_sha256"]:
            raise ApprovedReplayError("RE2 allowlist inputs disagree with frozen")
        files = selector.chon_ca(allow, opaque_id, replay.RE2_RAW_REPO, kiem_hash=True)
        return {"kind": "ranker", "method": "microrank", "t": frozen["window"]["t"],
                "model": None, "files": {name: {"path": path, "sha256": wanted[name]}
                                         for name, path in files.items()}}, None
    from p3 import nezha
    relative = "results/T-026/allowlist-dev.json"
    path = replay.verify(relative, index26["source_hashes"][relative], replay.I26 + "#/source_hashes", audit)
    allow = nezha.nap_allowlist(path)
    if opaque_id not in allow or entry["trace_guard_s"] != 0:
        raise ApprovedReplayError("Nezha case/main guard outside frozen scope")
    wanted = {path: meta["sha256"] for path, meta in allow[opaque_id]["files"].items()}
    if wanted != frozen["input_sha256"]:
        raise ApprovedReplayError("Nezha allowlist inputs disagree with frozen")
    script = "results/T-026/scripts/run_pilot.py" if entry["reused_pilot"] else "results/T-026/scripts/run.py"
    constants = replay.literal_constants(replay.verify(
        script, index26["source_hashes"][script], replay.I26 + "#/source_hashes", audit))
    return {"allowlist_path": str(path), "opaque_id": opaque_id, "repo_root": str(REPO),
            "view": "main", "method": "microrank", "trace_guard_s": 0}, constants


def reconstruct_native(replay, directory, dataset, opaque_id, entry, constants, output, cost):
    """Literal record reconstruction from the original replay's two branches."""
    from p3 import ban_ghi, runner
    if output.get("hashseed") != "0":
        raise ApprovedReplayError("native worker reported different hashseed")
    if dataset == "RE2-TT":
        base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None,
                "hashseed": 0, "detector": None, "detector_columns": None, "config_id": "p3-re2tt-v2"}
        records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "microrank", "a")
        if len(records) != 1:
            raise ApprovedReplayError("native RE2 reconstruction count is not one")
        return replay.read(directory / "ban-ghi-0.json")
    from p3.adapters.nezha import VARIANTS, VERSIONS
    results = output["ket_qua_nhieu"]
    if len(results) != 1:
        raise ApprovedReplayError("native Nezha result count is not one")
    record = ban_ghi.tao("microrank", VERSIONS["microrank"], VARIANTS["microrank"], "a", results[0],
                         output["window"], constants["CONFIG"], constants["WHY"], seed=None, hashseed=0,
                         run_id=directory.name, opaque_id=opaque_id)
    record["cost"] = {**cost, "buoc_s": output.get("buoc_s", {})}
    record["input_sha256"] = output["input_sha256"]
    if entry["reused_pilot"]:
        record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
    else:
        record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
    ban_ghi.kiem(record)
    dump(directory / "ban-ghi-0.json", record)
    return record


def native_child(dataset, opaque_id, raw_directory, job_sha256, frozen_sha256):
    directory = Path(raw_directory).resolve()
    if (BASE / "runs" not in directory.parents or directory.name != "native"
            or not directory.is_dir() or set(p.name for p in directory.iterdir()) != {"job.json"}):
        raise ApprovedReplayError("native child requires the new parent's job-only native directory")
    audit = []
    replay = preflight(audit, with_posthoc=False)
    try:
        entry, frozen, index26, code_hashes = replay.source_for(dataset, opaque_id, audit)
        if entry["sha256"] != frozen_sha256:
            raise ApprovedReplayError("native child frozen binding mismatch")
        verify(directory / "job.json", job_sha256, "parent byte-identical observed job", audit)
        job, constants = expected_job(replay, dataset, opaque_id, entry, frozen, index26, audit)
        if replay.exact_differences(job, read(directory / "job.json")):
            raise ApprovedReplayError("native child job differs from source-verified expected job")
        if dataset == "RE2-TT":
            from p3 import worker
        else:
            from p3 import nezha_worker as worker
        import microrank
        if sys.gettrace() is not None or sys.getprofile() is not None:
            raise ApprovedReplayError("native child has an observer/profile attached")
        imports = replay.loaded_sources(code_hashes)
        dump(directory / "source.json", {"entry": entry, "dataset": dataset, "opaque_id": opaque_id,
             "observer_attached": False, "source_checks": audit, "actual_imports": imports,
             "job_sha256": job_sha256, "frozen_sha256": frozen_sha256,
             "script_sha256": sha(__file__), "python": sys.version, "executable": sys.executable})
        before = function_snapshot()
        started = time.perf_counter()
        with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout:
            with (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    worker.main(str(directory / "job.json"), str(directory / "ket-qua.json"))
        cost = replay.measured_cost(started, 0)
        cost["env"] = "T-032-independent-native-child"
        cost["measurement_note"] = "native worker wall; fresh child process lifetime RSS; no observer; IO not measured"
        dump(directory / "cost.json", cost)
        if sys.gettrace() is not None or sys.getprofile() is not None or function_snapshot() != before:
            raise ApprovedReplayError("native call changed hook/function identities")
        record = reconstruct_native(replay, directory, dataset, opaque_id, entry, constants,
                                    read(directory / "ket-qua.json"), cost)
        if record["input_sha256"] != frozen["input_sha256"]:
            raise ApprovedReplayError("native input hashes disagree with frozen")
        dump(directory / "source-checks.json", {"checks": audit})
        check = {"status": "NATIVE_COMPLETE", "dataset": dataset, "opaque_id": opaque_id,
                 "source_status": frozen["status"], "native_status": record["status"],
                 "observer_attached": False, "job_sha256": job_sha256,
                 "source_checks_passed": True, "actual_imports_after": replay.loaded_sources(code_hashes),
                 "artifact_manifest": replay.artifact_manifest(directory),
                 "intermediates_eligible": False, "cohort_ready": False}
        dump(directory / "check.json", check)
        return 0
    except BaseException as error:
        if not (directory / "source-checks.json").exists():
            dump(directory / "source-checks.json", {"checks": audit})
        dump(directory / "failure.json", {"status": "FAIL_STOP", "error": str(error),
                                         "traceback": traceback.format_exc(), "source_checks": audit,
                                         "intermediates_eligible": False, "cohort_ready": False})
        return 1


def run_native_subprocess(replay, directory, dataset, opaque_id, entry, observed_dir, guard):
    native_dir = directory / "native"
    native_dir.mkdir()
    shutil.copyfile(observed_dir / "job.json", native_dir / "job.json")
    job_sha256 = sha(observed_dir / "job.json")
    if sha(native_dir / "job.json") != job_sha256:
        raise ApprovedReplayError("job copy was not byte-identical")
    command = [sys.executable, "-B", "-X", "utf8", str(Path(__file__).resolve()), "native-child",
               dataset, opaque_id, str(native_dir), job_sha256, entry["sha256"]]
    dump(directory / "native-command.json", {"command": command, "python": sys.executable,
         "environment_inherited_unchanged": True, "observed_job_sha256": job_sha256,
         "native_job_sha256": job_sha256, "observer_attached": False})
    guard.check(FINAL_LOG_RESERVE)
    remaining = MAX_WALL_S - (time.perf_counter() - guard.started)
    process = None
    try:
        with (directory / "native-process-stdout.txt").open("x", encoding="utf-8") as stdout:
            with (directory / "native-process-stderr.txt").open("x", encoding="utf-8") as stderr:
                process = subprocess.Popen(command, cwd=BASE, env=os.environ.copy(), stdout=stdout, stderr=stderr)
                dump(directory / "native-process.json", {"pid": process.pid, "parent_pid": os.getpid(),
                                                         "started_utc": replay.now()})
                code = process.wait(timeout=max(0.01, remaining))
        if code != 0:
            raise ApprovedReplayError("independent native child failed, exit " + str(code))
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
    guard.check(FINAL_LOG_RESERVE)
    return native_dir


def approved_one(directory, dataset, opaque_id, guard, audit):
    replay = preflight(audit)
    entry, frozen, index26, code_hashes = replay.source_for(dataset, opaque_id, audit)
    before = function_snapshot()
    observed_dir = directory / "observed"
    observed_dir.mkdir()
    replay.progress(directory, "OBSERVED_ORIGINAL_REPLAY_START", dataset=dataset, opaque_id=opaque_id,
                    source_status=frozen["status"])
    old_exit = replay.one(observed_dir, dataset, opaque_id)
    if old_exit not in (0, 1):
        raise ApprovedReplayError("original observed replay returned unexpected code")
    old_check = read(observed_dir / "check.json")
    if (old_check.get("capture_status") != "captured_unverified_replay"
            or old_check.get("capture_check", {}).get("pass") is not True
            or old_check.get("frozen_sha256") != entry["sha256"]
            or sys.gettrace() is not None or sys.getprofile() is not None):
        raise ApprovedReplayError("observed source/capture/hook check did not pass")
    after = function_snapshot()
    if before != after:
        raise ApprovedReplayError("observer changed native function identities")
    dump(directory / "observer-integrity.json", {"before": before, "after": after, "function_identities_exact": True,
         "trace_and_profile_restored_to_none": True, "old_check_retained_without_override": True,
         "limits": "function identity and output exactness checks do not reconstruct historical trace partitions"})
    replay.loaded_sources(code_hashes)
    collected = gc.collect()
    replay.progress(directory, "NATIVE_CHILD_START", gc_collected_before_native=collected,
                    observed_exact_check_status=old_check["status"])
    native_dir = run_native_subprocess(replay, directory, dataset, opaque_id, entry, observed_dir, guard)
    observed, native = read(observed_dir / "ban-ghi-0.json"), read(native_dir / "ban-ghi-0.json")
    pair_diff = replay.compare_records(observed, native)
    pair = {"pass": not pair_diff, "differences": pair_diff, "tolerance_used": False,
            "exact_fields": replay.EXACT_FIELDS, "excluded_fields": replay.EXCLUDED_FIELDS,
            "observed_sha256": sha(observed_dir / "ban-ghi-0.json"),
            "native_sha256": sha(native_dir / "ban-ghi-0.json")}
    dump(directory / "native-observed-exact.json", pair)
    if pair_diff:
        raise ApprovedReplayError("native-observed comparison failed exact; no roundoff exception applies")
    comparator_path = verify(SCRIPTS / "compare_microrank_roundoff.py", COMPARATOR_SHA256,
                             "approved comparator immediately before import", audit)
    comparator = load_module("t032_approved_roundoff_comparator", comparator_path)
    comparison = comparator.compare_case(dataset, opaque_id, observed_dir, sha(observed_dir / "check.json"),
                                          native_run=native_dir, native_check_sha256=sha(native_dir / "check.json"))
    dump(directory / "roundoff-comparison.json", comparison)
    if not comparison["record_contract_pass"] or comparison["native_observed_exact"]["pass"] is not True:
        raise ApprovedReplayError("approved frozen comparison failed; threshold is not increased")
    guard.check(FINAL_LOG_RESERVE)
    bridge_path = verify(SCRIPTS / "check_microrank_t028.py", BRIDGE_SHA256,
                         "verified bridge immediately before posthoc import", audit)
    bridge = load_module("t032_approved_T028_bridge", bridge_path)
    trust = {"frozen_record_sha256": entry["sha256"], "observed_record_sha256": pair["observed_sha256"],
             "native_observed_exact": True, "approved_record_comparison_passed": True}
    verdict = bridge.check_t028(repo_root=REPO, dataset=dataset, opaque_id=opaque_id,
        frozen_record_path=replay.safe_source(entry["path"]), frozen_record_sha256=entry["sha256"],
        observed_record_path=observed_dir / "ban-ghi-0.json", observed_record_sha256=pair["observed_sha256"],
        trusted_check=trust)
    dump(directory / "t028-check.json", verdict)
    required = ("passed", "eligibility", "source_verified", "frozen_self_check_passed", "observed_equivalence_passed")
    if any(verdict.get(key) is not True for key in required):
        raise ApprovedReplayError("T-028 frozen-feature/ancestor equivalence bridge did not pass")
    if verdict.get("graph_reconstructed") is not False:
        raise ApprovedReplayError("T-028 bridge did not declare frozen ancestors instead of a reconstructed graph")
    replay.loaded_sources(code_hashes)
    dump(directory / "source-checks.json", {"checks": audit})
    source_checks = read(observed_dir / "source-checks.json")["checks"]
    if any(row.get("pass") is not True for row in source_checks + audit):
        raise ApprovedReplayError("source audit contains a failed check")
    guard.check(FINAL_LOG_RESERVE)
    replay.progress(directory, "ALL_CASE_CHECKS_PASS", classification=comparison["classification"])
    return {"status": "PASS", "dataset": dataset, "opaque_id": opaque_id,
            "frozen_path": entry["path"], "frozen_sha256": entry["sha256"],
            "frozen_status": frozen["status"], "replay_status": observed["status"],
            "observed_original_exact_status": old_check["status"],
            "observed_original_check_sha256": sha(observed_dir / "check.json"),
            "source_job_input_F_checks": True, "capture_check_passed": True,
            "observer_function_identity_check_passed": True, "native_observed_exact": True,
            "approved_record_comparison_passed": True, "t028_bridge_passed": True,
            "classification": comparison["classification"], "numeric_summary": comparison["numeric_summary"],
            "record_bindings": comparison["record_bindings"],
            "checks": {"capture": "observed/check.json#/capture_check",
                       "native_observed": "native-observed-exact.json",
                       "approved_comparator": "roundoff-comparison.json", "T028": "t028-check.json"},
            "intermediates_eligible": True, "cohort_ready": False, "A_prime_authorized": False,
            "report_use_requires_WHY_approval": True,
            "limits": ["Case checks only; not whole-cohort completion or causal interpretation.",
                       "Original observed exact FAIL remains unchanged if the exception was required.",
                       "T028 uses hashed historical features/ancestors; no new graph reconstruction.",
                       "Frozen historical abnormal masks/trace partitions remain unavailable."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    one = commands.add_parser("one")
    one.add_argument("dataset", choices=("RE2-TT", "Nezha-OB"))
    one.add_argument("opaque_id")
    one.add_argument("new_run_dir")
    child = commands.add_parser("native-child", help=argparse.SUPPRESS)
    child.add_argument("dataset", choices=("RE2-TT", "Nezha-OB"))
    child.add_argument("opaque_id")
    child.add_argument("new_native_dir")
    child.add_argument("job_sha256")
    child.add_argument("frozen_sha256")
    args = parser.parse_args()
    environment_guard()
    if args.command == "native-child":
        return native_child(args.dataset, args.opaque_id, args.new_native_dir,
                            args.job_sha256, args.frozen_sha256)
    started = time.perf_counter()
    directory = new_run(args.new_run_dir)
    guard = BenchmarkGuard(directory, started)
    audit = []
    dump(directory / "invocation.json", {"argv": sys.argv, "pid": os.getpid(), "python": sys.version,
         "executable": sys.executable, "script_sha256": sha(__file__), "hashseed": os.environ.get("PYTHONHASHSEED"),
         "architecture": "unchanged original observed one + fresh native child + posthoc comparator/bridge",
         "max_wall_s": MAX_WALL_S, "max_new_bytes": MAX_NEW_BYTES,
         "dependency_hashes": {"replay": REPLAY_SHA256, "capture": CAPTURE_SHA256,
                               "comparator": COMPARATOR_SHA256, "bridge": BRIDGE_SHA256}})
    guard.start()
    result = None
    try:
        result = approved_one(directory, args.dataset, args.opaque_id, guard, audit)
        guard.check(FINAL_LOG_RESERVE)
    except BaseException as error:
        result = {"status": "FAIL_STOP", "dataset": args.dataset, "opaque_id": args.opaque_id,
                  "error_type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc(),
                  "source_checks": audit, "intermediates_eligible": False, "cohort_ready": False,
                  "A_prime_authorized": False, "retained": "all partial observed/native/compare/bridge artifacts",
                  "classification": "blocked", "numeric_summary": None,
                  "no_retry_no_skip_no_tolerance_increase": True}
    finally:
        guard.stop()
    dump(directory / "guard-final.json", guard.report())
    result["guard"] = guard.report()
    if result["status"] != "PASS" and (directory / "roundoff-comparison.json").is_file():
        try:
            partial_comparison = read(directory / "roundoff-comparison.json")
            result["record_comparison_classification"] = partial_comparison["classification"]
            result["classification"] = ("service_order_changed"
                                        if partial_comparison["classification"] == "service_order_changed" else "blocked")
            result["numeric_summary"] = partial_comparison["numeric_summary"]
            result["approved_comparator_report"] = "roundoff-comparison.json"
        except Exception as error:
            result["partial_comparator_report_error"] = {"type": type(error).__name__, "error": str(error)}
    result["artifact_manifest"] = [
        {"path": path.relative_to(directory).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(directory.rglob("*")) if path.is_file() and path != directory / "check.json"]
    result["elapsed_s"] = time.perf_counter() - started
    projected = guard.measured_bytes() + len(encoded(result)) + FINAL_LOG_RESERVE
    if projected > MAX_NEW_BYTES or result["elapsed_s"] > MAX_WALL_S:
        result.setdefault("record_comparison_classification", result["classification"])
        result.update(status="FAIL_STOP", classification="blocked", intermediates_eligible=False, cohort_ready=False,
                      budget_failure=True, projected_bytes_including_check_and_log_reserve=projected)
    dump(directory / "check.json", result)
    print(json.dumps({"status": result["status"], "dataset": args.dataset, "opaque_id": args.opaque_id,
                      "intermediates_eligible": result["intermediates_eligible"], "cohort_ready": False,
                      "elapsed_s": result["elapsed_s"], "logical_new_bytes": guard.measured_bytes(),
                      "output": str(directory)}, ensure_ascii=False), flush=True)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
