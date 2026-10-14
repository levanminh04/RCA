"""Q-124 source-laptop MicroRank replay: exact records, then capture/T-028 audit.

Importing this module performs no I/O, heavy imports, method or fixture calls.
Only the child command invokes a real method, exactly once. The independent
controller must guard every command, seal streams/PIDs and stop on any error.
No cohort loop, retry, numeric tolerance, label-to-method payload or A-prime.
All output directories are new below the approved laptop cohort. Old diagnostic
artifacts are read-only; new retrospective verdicts never edit old eligibility.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import copy
import hashlib
import importlib
import importlib.metadata
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import struct
import sys
import time
import traceback
from fractions import Fraction

REPO = Path("D:/RCA-flashticket")
SCRIPTS = REPO / "results/T-032/scripts"
COHORT = REPO / "results/T-032/runs/microrank-laptop-cohort-001"
DIAGNOSTIC = REPO / "results/T-032/runs/microrank-laptop-diagnostic-001"
PYTHON = Path("D:/RCA-ext/envs/T-014-main/Scripts/python.exe")
DATASETS = ("RE2-TT", "Nezha-OB")
MAX_WALL_S = 600
MAX_NEW_BYTES = 150 * 1024 * 1024
MAX_TASK_BYTES = 12 * 1024 * 1024 * 1024
MAX_LOCAL_BYTES = 4 * 1024 * 1024 * 1024
MAX_COHORT_BYTES = 5 * 1024 * 1024 * 1024 // 2
MAX_COHORT_WALL_S = 3 * 60 * 60
MAX_TREE_RSS = 2 * 2143158272
MIN_AVAILABLE_RAM = MAX_TREE_RSS + 256 * 1024 * 1024
THREAD_NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
SOURCE_THREAD_ENV = None
SOURCE_THREAD_AUTHORITY = "Historical values not recorded; Q-124/Q-100 authorize current unset values only"
CURRENT_THREAD_ENV = {name: None for name in THREAD_NAMES}
PACKAGES = {"numpy": "1.26.4", "pandas": "2.2.3", "scikit-learn": "1.6.0",
            "scipy": "1.14.1", "pyarrow": "18.1.0", "psutil": "6.1.1", "networkx": "2.8.8"}
CATALOG = "results/T-032/runs/microrank-cohort-failure-001/cohort/52-cases.json"
TRANSPORT = "results/T-032/runs/microrank-cohort-failure-001/transport-check.json"
PINS = {
    "results/T-032/scripts/replay_microrank.py": "193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562",
    "results/T-032/scripts/capture_microrank.py": "b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b",
    "results/T-032/scripts/diagnose_microrank_laptop_v2.py": "3f9eb062d72b2a3316b6208d33cd9168b42a097de873c26e20bb1b6e96e2de10",
    "results/T-032/scripts/check_microrank_t028_v3.py": "324807b59d7b6cbe5062915949b2bd958e0b3ad520cc7e8d1e7dcbff6568a144",
    "results/T-032/scripts/compare_microrank_roundoff.py": "7e29b728bbd3c00174b962efd5896a50556d6aa0c68a2dea85e49e2b81ea64a2",
    "results/T-031/moi-truong.json": "52e08f0d1d169b504716a246d3404bb9ec124dea46505fbaa8c0bb474f591e2d",
    "results/T-022/allowlist-dev.json": "fec512d7dbf059b86c7049127c9fd7a899f3e6508d8ba472b160867b74e32ac3",
    "results/T-029/runs/compare-rca-preparation-001/manifest.json": "51498845f1e070017ec52c3b6550b84c444882af7c09aa31564d93c58972c2a8",
    "results/T-026/runs/session-005/handoff-manifest.json": "675092feac86d62908fb6a83f1356a2fc1ab128c717c4018f50433710abb7366",
    CATALOG: "9208b29b1a123a8ff3eff97b5159d83389eba94eada36a3efff63aa1af5125bf",
    TRANSPORT: "21098b72ee3823ab096557538273458bc531440ee50e91dba546b6d023815612",
}
RETROSPECTIVE_PINS = {
    "results/T-032/runs/microrank-laptop-diagnostic-001/launcher-closed.json": "c8bc901febaea33210f4dd63ca8d714b560e900ee14c5516a395aace34607377",
    "results/T-032/runs/microrank-laptop-diagnostic-verification-001/check.json": "558c7b1f7eee39063fefc47f751087315df86e6eb2878a0bc7964f6ea488633c",
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


def safe_relative(root, relative):
    require(isinstance(relative, str) and relative and "\\" not in relative, "relative POSIX path required")
    parts = PurePosixPath(relative)
    require(not parts.is_absolute() and not re.match(r"^[A-Za-z]:", relative)
            and not any(x in ("", ".", "..") for x in relative.split("/")), "unsafe relative path")
    require(not any(x.lower() in ("locked", "test", "tests", "t-033") for x in parts.parts)
            and "flash-ticket-rca-research" not in relative.lower(), "forbidden source")
    path = Path(root).joinpath(*parts.parts)
    # Reject symlinks before resolve, including every ancestor within the root.
    parent = path
    while parent != Path(root):
        require(not parent.is_symlink(), "symlink in source/artifact path")
        parent = parent.parent
    resolved = path.resolve()
    require(Path(root).resolve() in resolved.parents, "path escaped root")
    return resolved


def output_path(raw):
    path = Path(raw).resolve()
    require(COHORT.resolve() in path.parents and not path.is_symlink() and not COHORT.is_symlink(), "output escaped approved new cohort")
    parent = Path(raw)
    while parent.resolve() != COHORT.resolve():
        require(not parent.is_symlink(), "symlink in output path")
        parent = parent.parent
    return path


def new_directory(raw):
    path = output_path(raw)
    path.mkdir(parents=True, exist_ok=False)
    return path


def dump_new(path, value):
    path = output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def progress(directory, stage, **fields):
    event = {"at_utc": now(), "stage": stage, **fields}
    with output_path(Path(directory) / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps(event, ensure_ascii=False, allow_nan=False), flush=True)


def immutable_manifest(directory, excluded=("check.json",)):
    directory = Path(directory).resolve()
    excluded = set(excluded)
    rows = []
    for path in sorted(directory.rglob("*")):
        require(not path.is_symlink(), "symlink in artifact tree")
        if path.is_file() and path.relative_to(directory).as_posix() not in excluded:
            rows.append({"path": path.relative_to(directory).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)})
    return rows


def verify_manifest(directory, manifest, excluded=("check.json",)):
    directory = Path(directory).resolve()
    listed = set()
    for row in manifest:
        relative = row["path"]
        require(relative not in listed, "duplicate manifest entry")
        listed.add(relative)
        path = safe_relative(directory, relative)
        require(path.is_file() and path.stat().st_size == row["bytes"] and sha(path) == row["sha256"],
                "artifact changed: " + relative)
    actual = {row["path"] for row in immutable_manifest(directory, ())}
    require(actual == listed | set(excluded), "manifest incomplete or has extra artifacts")
    require(not (listed & set(excluded)), "manifest includes excluded/self path")
    return {"pass": True, "files_checked": len(listed), "manifest_excludes": list(excluded)}


def verify_closed_manifest(directory, check=None):
    check = read(Path(directory) / "check.json") if check is None else check
    require(check.get("manifest_excludes") == ["check.json"], "unsupported child manifest exclusions")
    require(not (Path(directory) / "failure-after-check.json").exists(), "failure after check invalidates previous PASS")
    return verify_manifest(directory, check["artifact_manifest"])


def close_check(directory, value):
    require(not (Path(directory) / "check.json").exists(), "check already exists; retry/rewrite rejected")
    progress(directory, "TERMINAL", status=value["status"], passed=value.get("passed", False))
    value = {**value, "artifact_manifest": immutable_manifest(directory), "manifest_excludes": ["check.json"]}
    dump_new(Path(directory) / "check.json", value)
    verify_closed_manifest(directory, value)
    return value


def failure_check(directory, error):
    failure = {"status": "FAIL_STOP", "passed": False, "error_type": type(error).__name__,
               "error": str(error), "traceback": traceback.format_exc(), "intermediates_eligible": False,
               "a_prime_authorized": False, "retry_authorized": False, "retained": "all partial files retained"}
    directory = Path(directory)
    if not (directory / "check.json").exists():
        return close_check(directory, failure)
    progress(directory, "FAILED_AFTER_CHECK", error=str(error))
    failure["superseded_check_sha256"] = sha(directory / "check.json")
    failure["artifact_manifest"] = immutable_manifest(directory, ("failure-after-check.json",))
    failure["manifest_excludes"] = ["failure-after-check.json"]
    dump_new(directory / "failure-after-check.json", failure)
    return failure


def source_pins(extra=None):
    audit = []
    for relative, expected in sorted({**PINS, **(extra or {})}.items()):
        path = safe_relative(REPO, relative)
        actual = verify_pinned_file(path, expected)
        audit.append({"path": relative, "expected_sha256": expected, "actual_sha256": actual,
                      "bytes": path.stat().st_size, "pass": actual == expected})
        require(actual == expected, "pinned source changed: " + relative)
    return audit


def verify_pinned_file(path, expected):
    require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None, "invalid source pin")
    actual = sha(path)
    require(actual == expected, "pinned bytes changed: " + str(path))
    return actual


def tool_module(filename):
    relative = "results/T-032/scripts/" + filename
    path = safe_relative(REPO, relative)
    require(sha(path) == PINS[relative], "tool source changed: " + filename)
    name = "_t032_q124_" + path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(Path(module.__file__).resolve() == path and sha(path) == PINS[relative], "tool import binding changed")
    return module


def replay_module():
    replay = importlib.import_module("replay_microrank")
    require(Path(replay.__file__).resolve() == (SCRIPTS / "replay_microrank.py").resolve(), "wrong replay import")
    require(sha(replay.__file__) == PINS["results/T-032/scripts/replay_microrank.py"], "replay import hash differs")
    capture = importlib.import_module("capture_microrank")
    require(Path(capture.__file__).resolve() == (SCRIPTS / "capture_microrank.py").resolve(), "wrong capture import")
    require(sha(capture.__file__) == PINS["results/T-032/scripts/capture_microrank.py"], "capture import hash differs")
    replay.REPO = REPO
    replay.RE2_RAW_REPO = REPO
    return replay


def environment_metadata():
    import numpy, scipy.linalg
    from threadpoolctl import threadpool_info
    versions = {name: importlib.metadata.version(name) for name in PACKAGES}
    return {"at_utc": now(), "python": sys.version, "version_tuple": list(sys.version_info[:3]),
            "executable": sys.executable, "prefix": sys.prefix, "base_prefix": sys.base_prefix,
            "packages": versions, "hashseed": os.environ.get("PYTHONHASHSEED"),
            "pythonpath": os.environ.get("PYTHONPATH"),
            "thread_environment_current": {name: os.environ.get(name) for name in THREAD_NAMES},
            "threadpool_status": "current measurement only, not historical evidence",
            "threadpools_current": threadpool_info(),
            "source_thread_environment": SOURCE_THREAD_ENV,
            "source_thread_authority": SOURCE_THREAD_AUTHORITY,
            "source_thread_status": "OPEN" if SOURCE_THREAD_ENV is None else "RECORDED",
            "current_values_are_historical_evidence": False}


def startup_guard(ram=False):
    require(os.name == "nt" and Path(sys.executable).resolve() == PYTHON.resolve(), "source laptop Python required")
    require(tuple(sys.version_info[:3]) == (3, 12, 10), "source requires Python 3.12.10")
    require(os.environ.get("PYTHONHASHSEED") == "0", "hashseed must be zero at process startup")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1" and sys.dont_write_bytecode, "bytecode must be disabled")
    require({name: os.environ.get(name) for name in THREAD_NAMES} == CURRENT_THREAD_ENV, "Q-124 current five threads must remain unset")
    require(sys.gettrace() is None and sys.getprofile() is None, "pre-existing trace/profile hook")
    require({name: importlib.metadata.version(name) for name in PACKAGES} == PACKAGES, "source package versions differ")
    if ram:
        import psutil
        require(psutil.virtual_memory().available >= MIN_AVAILABLE_RAM, "RAM below 4,554,752,000-byte gate; no heavy work")


def environment_guard(metadata):
    startup_guard()
    require(metadata["packages"] == PACKAGES and metadata["hashseed"] == "0", "source environment differs")
    require(metadata["thread_environment_current"] == CURRENT_THREAD_ENV, "current thread environment differs")
    require(metadata["source_thread_status"] == "OPEN" and metadata["current_values_are_historical_evidence"] is False,
            "historical threads must remain OPEN")


def stored_environment_guard(before, after):
    for metadata in (before, after):
        require(metadata["version_tuple"] == [3, 12, 10] and Path(metadata["executable"]).resolve() == PYTHON.resolve(),
                "saved worker Python differs")
        require(metadata["packages"] == PACKAGES and metadata["hashseed"] == "0", "saved package/hashseed differs")
        require(metadata["thread_environment_current"] == CURRENT_THREAD_ENV, "saved current threads differ")
        require(metadata["source_thread_status"] == "OPEN" and metadata["current_values_are_historical_evidence"] is False,
                "saved historical thread claim differs")
    replay = replay_module()
    for field in ("packages", "version_tuple", "executable", "prefix", "base_prefix", "pythonpath", "hashseed",
                  "thread_environment_current", "threadpools_current"):
        require(not replay.exact_differences(before[field], after[field]), "saved environment changed: " + field)


def catalog():
    """Authenticate only source metadata; old EC2 verdicts are not laptop verdicts."""
    source_pins()
    replay = replay_module()
    transfer = read(REPO / TRANSPORT)
    require(transfer["status"] == "PASS" and transfer["no_method_executed"] is True, "catalog transport not closed PASS")
    references = [x for x in transfer["files"] if Path(x["local"]).resolve() == (REPO / CATALOG).resolve()]
    require(len(references) == 1 and references[0]["pass"] is True
            and references[0]["sha256"] == PINS[CATALOG]
            and references[0]["bytes"] == (REPO / CATALOG).stat().st_size, "catalog transport binding differs")
    rows = read(REPO / CATALOG)["rows"]
    identities = [(x["dataset"], x["opaque_id"]) for x in rows]
    require(len(identities) == len(set(identities)) == 52, "catalog duplicate/missing identities")
    require({ds: sum(x[0] == ds for x in identities) for ds in DATASETS} == {"RE2-TT": 30, "Nezha-OB": 22}, "catalog dataset coverage differs")
    result = []
    for old in sorted(rows, key=lambda x: (DATASETS.index(x["dataset"]), x["opaque_id"])):
        audit = []
        entry, frozen, index26, code_hashes = replay.source_for(old["dataset"], old["opaque_id"], audit)
        require(entry["sha256"] == old["source_sha256"] and frozen["status"] == old["source_status"], "catalog frozen source differs")
        result.append({"dataset": old["dataset"], "opaque_id": old["opaque_id"], "source_status": frozen["status"],
                       "frozen_path": entry["path"], "source_sha256": entry["sha256"],
                       "source_entry": entry, "input_shape": frozen["input_shape"], "window": frozen["window"],
                       "case_status": "not_run", "intermediates_eligible": False})
    return result


def source_case(dataset, opaque_id):
    require(dataset in DATASETS and re.fullmatch(r"dev-[0-9a-f]{10}", opaque_id) is not None, "case outside cohort scope")
    pins = source_pins()
    replay = replay_module()
    rows = read(REPO / CATALOG)["rows"]
    selected = [x for x in rows if (x["dataset"], x["opaque_id"]) == (dataset, opaque_id)]
    require(len(selected) == 1, "case missing/duplicated in pinned catalog")
    audit = []
    entry, frozen, index26, code_hashes = replay.source_for(dataset, opaque_id, audit)
    require(entry["sha256"] == selected[0]["source_sha256"] and frozen["status"] == selected[0]["source_status"], "catalog/source disagreement")
    return replay, entry, frozen, index26, code_hashes, audit, pins


def job_metadata(dataset, opaque_id, replay, entry, frozen, index26, audit):
    allow_relative = "results/T-022/allowlist-dev.json" if dataset == "RE2-TT" else "results/T-026/allowlist-dev.json"
    expected = PINS[allow_relative] if dataset == "RE2-TT" else index26["source_hashes"][allow_relative]
    allow_path = replay.verify(allow_relative, expected, "approved allowlist/source index", audit)
    doc = read(allow_path)
    require(doc["so_ca"] == len(doc["cases"]) == (30 if dataset == "RE2-TT" else 22), "allowlist coverage changed")
    entries = [x for x in doc["cases"] if x["opaque_id"] == opaque_id]
    require(len(entries) == 1 and len({x["opaque_id"] for x in doc["cases"]}) == len(doc["cases"]), "allowlist identity duplicate/missing")
    selection = entries[0]
    files = selection["files"]
    wanted = {name: meta["sha256"] for name, meta in files.items() if meta is not None}
    require(not replay.exact_differences(wanted, frozen["input_sha256"]), "allowlist input hashes differ from frozen")
    checked_inputs = []
    root = REPO / ("data/rcaeval" if dataset == "RE2-TT" else "data/ngoai-rcaeval/nezha/online-boutique/rca_data")
    for name, meta in files.items():
        if meta is None:
            continue
        path = safe_relative(REPO, meta["path"])
        require(root.resolve() in path.parents, "raw dev input outside dataset allowlist root")
        require(type(meta["bytes"]) is int and meta["bytes"] > 0 and re.fullmatch(r"[0-9a-f]{64}", meta["sha256"]), "invalid input size/hash")
        if dataset == "Nezha-OB":
            require(name == meta["path"] and doc["dataset"] == dataset, "Nezha file-key/dataset differs")
        checked_inputs.append({"name": name, "path": str(path), "sha256": meta["sha256"], "bytes": meta["bytes"]})
    constants = None
    if dataset == "RE2-TT":
        job = {"kind": "ranker", "method": "microrank", "t": frozen["window"]["t"], "model": None,
               "files": {row["name"]: {"path": row["path"], "sha256": row["sha256"]} for row in checked_inputs}}
        require(frozen["config_id"] == "p3-re2tt-v2", "RE2 source config differs")
        provenance = {"worker": "p3.worker.main", "reconstruction": "p3.runner._ket_thuc",
                      "source_config": entry["source_config"], "source_config_sha256": entry["source_config_sha256"]}
    else:
        require(type(entry["reused_pilot"]) is bool and entry["source_view"] == "main" and entry["trace_guard_s"] == 0,
                "Nezha main provenance/guard differs")
        require(frozen["window"]["t_ns"] == selection["t_ns"] == entry["expected_t_ns"]
                and frozen["window"]["trace_guard_s"] == 0, "Nezha boundary/guard differs")
        job = {"allowlist_path": str(allow_path), "opaque_id": opaque_id, "repo_root": str(REPO),
               "view": "main", "method": "microrank", "trace_guard_s": 0}
        script = "results/T-026/scripts/run_pilot.py" if entry["reused_pilot"] else "results/T-026/scripts/run.py"
        source = replay.verify(script, index26["source_hashes"][script], "T026 actual reconstruction provenance", audit)
        constants = replay.literal_constants(source)
        require(frozen["config_id"] == constants["CONFIG"] and frozen["why_ids"] == constants["WHY"], "Nezha source CONFIG/WHY differs")
        provenance = {"worker": "p3.nezha_worker.main", "reconstruction": script, "sha256": sha(source),
                      "reused_pilot": entry["reused_pilot"], "constants": constants}
    return job, checked_inputs, constants, provenance


def verify_inputs(input_checks):
    verified = []
    for row in input_checks:
        path = Path(row["path"])
        require(path.is_file() and not path.is_symlink() and path.stat().st_size == row["bytes"] and sha(path) == row["sha256"],
                "raw input changed: " + row["name"])
        verified.append({**row, "pass": True})
    return verified


def prepare_job(dataset, opaque_id):
    startup_guard()
    replay, entry, frozen, index26, code_hashes, audit, pins = source_case(dataset, opaque_id)
    require(frozen["status"] != "TIMEOUT", "TIMEOUT source needs separately approved reconstruction; no method call")
    job, inputs, constants, provenance = job_metadata(dataset, opaque_id, replay, entry, frozen, index26, audit)
    verified = verify_inputs(inputs)
    source_pins()
    return {"dataset": dataset, "opaque_id": opaque_id, "job": job, "entry": entry, "frozen": frozen,
            "source_checks": audit, "input_checks": verified, "code_hashes": code_hashes,
            "pin_checks": pins, "constants": constants, "provenance": provenance,
            "excluded_fields": replay.EXCLUDED_FIELDS, "exact_fields": list(replay.EXACT_FIELDS)}


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


def reconstruct(directory, dataset, opaque_id, entry, output, constants, cost):
    """The two frozen reconstruction branches; never a RE2 fallback for Nezha."""
    if dataset == "RE2-TT":
        from p3 import runner
        base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None,
                "hashseed": 0, "detector": None, "detector_columns": None, "config_id": "p3-re2tt-v2"}
        records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "microrank", "a")
        require(len(records) == 1, "RE2 reconstruction did not return exactly one record")
    else:
        from p3 import ban_ghi
        from p3.adapters.nezha import VARIANTS, VERSIONS
        results = output["ket_qua_nhieu"]
        require(len(results) == 1, "Nezha worker did not return exactly one result")
        result = results[0]
        record = ban_ghi.tao("microrank", VERSIONS["microrank"], VARIANTS["microrank"], "a", result,
                             output["window"], constants["CONFIG"], constants["WHY"], seed=None,
                             hashseed=0, run_id=directory.name, opaque_id=opaque_id)
        record["cost"] = {**cost, "buoc_s": output.get("buoc_s", {})}
        record["input_sha256"] = output["input_sha256"]
        if entry["reused_pilot"]:
            record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
        else:
            record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
        ban_ghi.kiem(record)
        dump_new(directory / "ban-ghi-0.json", record)
    return read(directory / "ban-ghi-0.json")


def child(mode, dataset, opaque_id, directory, job_sha256, frozen_sha256):
    require(mode in ("native", "observed") and dataset in DATASETS, "unsupported child scope")
    directory = output_path(directory)
    require(directory == (COHORT / "cases" / dataset / opaque_id / mode).resolve(), "child directory binding differs")
    require(directory.is_dir() and {p.name for p in directory.iterdir()} == {"job.json"}, "child requires a new job-only directory")
    require(sha(directory / "job.json") == job_sha256, "parent job bytes changed")
    startup_guard(ram=True)
    prepared = prepare_job(dataset, opaque_id)
    replay = replay_module()
    entry, frozen, code_hashes = prepared["entry"], prepared["frozen"], prepared["code_hashes"]
    require(entry["sha256"] == frozen_sha256, "child frozen binding changed")
    require(not replay.exact_differences(prepared["job"], read(directory / "job.json")), "child job differs from source job")
    native_binding = None
    if mode == "observed":
        native_directory = directory.parent / "native"
        native_binding = validate_child(dataset, opaque_id, "native", native_directory, job_sha256, frozen_sha256)
        require(sha(native_directory / "job.json") == job_sha256, "native/observed job bytes not identical")
    metadata = environment_metadata()
    environment_guard(metadata)
    if dataset == "RE2-TT":
        from p3 import worker, runner
        invoke_worker = worker.main
    else:
        from p3 import nezha_worker
        from p3.adapters.nezha import VARIANTS, VERSIONS
        invoke_worker = nezha_worker.main
    import microrank
    before = function_snapshot()
    imports_before = replay.loaded_sources(code_hashes)
    from threadpoolctl import threadpool_info
    dump_new(directory / "invocation.json", {"at_utc": now(), "argv": sys.argv, "pid": os.getpid(),
             "wrapper_sha256": sha(__file__), "native_calls_allowed": 1 if mode == "native" else 0,
             "observed_calls_allowed": 1 if mode == "observed" else 0,
             "native_gate_check": native_binding, "externally_guarded_required": True})
    dump_new(directory / "source.json", {"dataset": dataset, "opaque_id": opaque_id, "entry": entry,
             "source_checks": prepared["source_checks"], "pin_checks_before": prepared["pin_checks"],
             "input_checks_before": prepared["input_checks"], "actual_imports_before": imports_before,
             "job_sha256": job_sha256, "frozen_sha256": frozen_sha256,
             "observer_attached": mode == "observed", "environment": metadata,
             "threadpools_current_before": threadpool_info(), "functions_before": before,
             "provenance": prepared["provenance"], "native_observer_absent": mode == "native"})
    progress(directory, "WORKER_START", mode=mode, source_status=frozen["status"])
    started = time.perf_counter()
    capture_summary = None
    with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout:
        with (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                if mode == "native":
                    invoke_worker(str(directory / "job.json"), str(directory / "ket-qua.json"))
                else:
                    with replay.MicroRankCapture(directory / "capture") as capture:
                        invoke_worker(str(directory / "job.json"), str(directory / "ket-qua.json"))
                    capture_summary = capture.require_complete()
    cost = measured_windows_cost(started)
    dump_new(directory / "cost.json", cost)
    require(sys.gettrace() is None and sys.getprofile() is None, "worker left a trace/profile hook")
    require(function_snapshot() == before, "worker changed method function identities")
    output = read(directory / "ket-qua.json")
    require(output.get("hashseed") == "0", "worker hashseed differs")
    record = reconstruct(directory, dataset, opaque_id, entry, output, prepared["constants"], cost)
    differences = replay.compare_records(frozen, record)
    capture_check = None
    differences_native = []
    if mode == "observed":
        require(capture_summary["status"] == "captured_unverified_replay", "observer did not complete")
        capture_check = replay.verify_capture(directory / "capture", capture_summary)
        require(capture_check["pass"] is True, "capture verification failed")
        differences_native = replay.compare_records(read(directory.parent / "native/ban-ghi-0.json"), record)
    after = prepare_job(dataset, opaque_id)
    require(after["code_hashes"] == code_hashes and not replay.exact_differences(frozen, after["frozen"]), "source/frozen binding changed")
    metadata_after = environment_metadata()
    environment_guard(metadata_after)
    require(not replay.exact_differences(metadata["threadpools_current"], metadata_after["threadpools_current"]), "child BLAS/threadpool changed")
    require(metadata_after["thread_environment_current"] == metadata["thread_environment_current"], "child threads changed")
    dump_new(directory / "source-checks.json", {"checks": after["source_checks"], "pin_checks_after": source_pins(),
             "input_checks_after": after["input_checks"], "actual_imports_after": replay.loaded_sources(code_hashes),
             "functions_unchanged": True, "functions_after": function_snapshot(), "hooks_restored": True,
             "threadpools_current_after": threadpool_info(), "environment_after": metadata_after,
             "provenance_after": after["provenance"]})
    passed = not differences and not differences_native
    numeric = score_pair_summary(frozen, record)
    difference_groups = classify_differences(differences, frozen, record)
    check = close_check(directory, {"status": "PASS" if passed else "FAIL_STOP", "passed": passed,
             "mode": mode, "dataset": dataset, "opaque_id": opaque_id, "source_status": frozen["status"],
             "record_status": record["status"], "record_sha256": sha(directory / "ban-ghi-0.json"),
             "worker_pid": os.getpid(), "frozen_sha256": frozen_sha256, "job_sha256": job_sha256,
             "exact_fields": list(replay.EXACT_FIELDS), "excluded_fields": replay.EXCLUDED_FIELDS,
             "differences": differences, "native_observed_differences": differences_native,
             "numeric_summary": numeric, **difference_groups, "native_observer_absent": mode == "native",
             "frozen_exact": not differences, "native_frozen_exact": (not differences) if mode == "native" else None,
             "observed_frozen_exact": (not differences) if mode == "observed" else None,
             "native_observed_exact": (not differences_native) if mode == "observed" else None,
             "capture_status": None if capture_summary is None else capture_summary["status"],
             "capture_check": capture_check, "source_checks_passed": True,
             "worker_streams_closed": True, "external_streams_closed": "controller seals after child exits",
             "intermediates_eligible": False, "a_prime_authorized": False, "wrapper_sha256": sha(__file__)})
    return 0 if check["passed"] else 1


def classify_differences(differences, frozen, observed):
    """Describe exact failures without mistaking mapping/inventory for order."""
    def identities(record, field, key):
        values = record.get(field)
        if type(values) is not list or any(type(row) is not dict or type(row.get(key)) is not str for row in values):
            return None
        sequence = [row[key] for row in values]
        return sequence if len(sequence) == len(set(sequence)) else None
    operation_a, operation_b = identities(frozen, "ranking", "item"), identities(observed, "ranking", "item")
    service_a, service_b = identities(frozen, "entity_ranking", "entity"), identities(observed, "entity_ranking", "entity")
    operation_order = (operation_a is not None and operation_b is not None
                       and set(operation_a) == set(operation_b) and operation_a != operation_b)
    service_order = (service_a is not None and service_b is not None
                     and set(service_a) == set(service_b) and service_a != service_b)
    numeric, order, other = [], [], []
    for row in differences:
        pointer = row.get("pointer", "")
        if row.get("kind") == "float_exact":
            numeric.append(row)
        elif ((operation_order and (pointer.startswith("/ranking_native") or re.fullmatch(r"/ranking/[0-9]+/item", pointer)))
              or (service_order and re.fullmatch(r"/entity_ranking/[0-9]+/entity", pointer))
              or re.fullmatch(r"/entity_ranking/[0-9]+/tie_group", pointer)):
            order.append(row)
        else:
            other.append(row)
    return {"numeric_differences": numeric, "service_order_tie_differences": order, "other_differences": other}


def score_pair_summary(frozen, observed):
    """Report actual matched operation/service floats; never accept a difference."""
    rows, missing, nonfinite = [], [], []
    for field, identity_key, kind in (("ranking", "item", "operation"), ("entity_ranking", "entity", "service")):
        mappings = []
        for record in (frozen, observed):
            mapping = {}
            values = record.get(field)
            if not isinstance(values, list):
                return {"status": "SCORE_SCHEMA_UNSUPPORTED", "matched_score_count": None,
                        "max_ulp_distance": None, "max_relative": None, "policy": "exact only; no threshold"}
            for row in values:
                identity = row.get(identity_key) if isinstance(row, dict) else None
                if not isinstance(identity, str) or identity in mapping:
                    return {"status": "SCORE_IDENTITY_UNSUPPORTED", "matched_score_count": None,
                            "max_ulp_distance": None, "max_relative": None, "policy": "exact only; no threshold"}
                mapping[identity] = row
            mappings.append(mapping)
        left, right = mappings
        missing.extend({"kind": kind, "identity": identity} for identity in sorted(set(left) ^ set(right)))
        for identity in sorted(set(left) & set(right)):
            a, b = left[identity].get("key"), right[identity].get("key")
            if not (type(a) is list and type(b) is list and len(a) == len(b) == 1 and type(a[0]) is type(b[0]) is float):
                nonfinite.append({"kind": kind, "identity": identity, "reason": "not_single_float"}); continue
            a, b = a[0], b[0]
            if not math.isfinite(a) or not math.isfinite(b):
                nonfinite.append({"kind": kind, "identity": identity, "reason": "nonfinite"}); continue
            bits_a, bits_b = (struct.unpack(">Q", struct.pack(">d", value))[0] for value in (a, b))
            ordered_a = (~bits_a & ((1 << 64) - 1)) if bits_a >> 63 else bits_a | (1 << 63)
            ordered_b = (~bits_b & ((1 << 64) - 1)) if bits_b >> 63 else bits_b | (1 << 63)
            magnitude = max(abs(a), abs(b))
            relative = abs(Fraction.from_float(a) - Fraction.from_float(b)) / Fraction.from_float(magnitude) if magnitude else Fraction(0)
            rows.append({"kind": kind, "identity": identity, "expected_hex": a.hex(), "actual_hex": b.hex(),
                         "exact": bits_a == bits_b, "ulp_distance": abs(ordered_a - ordered_b),
                         "relative": float(relative), "relative_exact": {"numerator": relative.numerator, "denominator": relative.denominator}})
    maximum_ulp = max((row["ulp_distance"] for row in rows), default=None)
    maximum_relative = max((Fraction(row["relative_exact"]["numerator"], row["relative_exact"]["denominator"]) for row in rows), default=None)
    return {"status": "COMPUTED" if rows else "NO_MATCHED_SCORE_PAIRS", "matched_score_count": len(rows),
            "nonexact_score_count": sum(not row["exact"] for row in rows), "max_ulp_distance": maximum_ulp,
            "max_relative": float(maximum_relative) if maximum_relative is not None else None,
            "max_relative_exact": {"numerator": maximum_relative.numerator, "denominator": maximum_relative.denominator} if maximum_relative is not None else None,
            "score_pairs": rows, "missing_score_identities": missing, "nonfinite_or_type_pairs": nonfinite,
            "policy": "exact only; differences never accepted"}


def saved_checks_pass(rows):
    require(isinstance(rows, list) and rows, "missing source check rows")
    for row in rows:
        require(row.get("pass") is True, "stored source/input/import check failed")
        if "expected" in row:
            require(row["actual"] == row["expected"], "stored source expected/actual differs")
        if "expected_sha256" in row:
            require(row["actual_sha256"] == row["expected_sha256"], "stored pin expected/actual differs")


def child_exact_gate(check):
    require(check.get("status") == "PASS" and check.get("differences") == [] and check.get("source_checks_passed") is True,
            "child did not pass exact/source; no observed/next case")


def validate_child(dataset, opaque_id, mode, directory, job_sha256, frozen_sha256, legacy=False):
    """Read/hash only stdlib validation; raw inputs/capture arrays are audited in guarded commands."""
    directory = Path(directory).resolve()
    permitted = (DIAGNOSTIC / mode).resolve() if legacy else (COHORT / "cases" / dataset / opaque_id / mode).resolve()
    require(directory == permitted, "stored child output scope differs")
    check = read(directory / "check.json")
    if legacy:
        require(not (directory / "failure.json").exists(), "old child failure present")
        verify_manifest(directory, check["artifact_manifest"])
    else:
        verify_closed_manifest(directory, check)
        require(check["wrapper_sha256"] == sha(__file__) and check["worker_streams_closed"] is True, "new child wrapper/streams binding differs")
    child_exact_gate(check)
    require((check["dataset"], check["opaque_id"], check["mode"]) == (dataset, opaque_id, mode), "child identity differs")
    require(check["job_sha256"] == job_sha256 == sha(directory / "job.json") and check["frozen_sha256"] == frozen_sha256, "child job/frozen hashes differ")
    replay, entry, frozen, index26, code_hashes, audit, pins = source_case(dataset, opaque_id)
    require(entry["sha256"] == frozen_sha256, "frozen source binding changed")
    job, inputs, constants, provenance = job_metadata(dataset, opaque_id, replay, entry, frozen, index26, audit)
    require(not replay.exact_differences(job, read(directory / "job.json")), "saved job differs from source")
    require(not replay.compare_records(frozen, read(directory / "ban-ghi-0.json")), "independent child/frozen exact failed")
    source = read(directory / "source.json")
    after = read(directory / "source-checks.json")
    require(source["entry"] == entry and source["frozen_sha256"] == frozen_sha256 and source["job_sha256"] == job_sha256,
            "saved source binding differs")
    saved_checks_pass(source["source_checks"])
    saved_checks_pass(after["checks"])
    saved_checks_pass(after["pin_checks_after"])
    saved_checks_pass(source["input_checks_before"])
    saved_checks_pass(after["input_checks_after"])
    for values in (source["input_checks_before"], after["input_checks_after"]):
        # Legacy diagnostic inputs did not serialize paths or source byte expectations.
        if legacy:
            require({row["name"]: row["sha256"] for row in values} == frozen["input_sha256"], "legacy input binding differs")
            require({row["name"]: row["bytes"] for row in values} == {row["name"]: row["bytes"] for row in inputs}, "legacy input sizes differ")
        else:
            projection = [{key: row[key] for key in inputs[0]} for row in values] if inputs else []
            require(not replay.exact_differences(inputs, projection), "saved input binding differs")
    require(source["observer_attached"] is (mode == "observed") and after["functions_unchanged"] is True and after["hooks_restored"] is True,
            "saved hook/function observer checks differ")
    stored_environment_guard(source["environment"], after["environment_after"])
    require(not replay.exact_differences(source["threadpools_current_before"], after["threadpools_current_after"]), "saved worker BLAS pools changed")
    for key in ("actual_imports_before", "actual_imports_after"):
        values = source[key] if key.endswith("before") else after[key]
        require(values and any(x["module"] == "microrank" for x in values), "missing actual MicroRank import")
        for row in values:
            require(row["path"] in code_hashes and row["sha256"] == code_hashes[row["path"]]
                    and sha(safe_relative(REPO, row["path"])) == row["sha256"], "actual source import changed")
    for row in source["functions_before"].values():
        path = Path(row["code_file"]).resolve()
        relative = path.relative_to(REPO.resolve()).as_posix()
        require(relative in code_hashes and sha(path) == code_hashes[relative], "native function source differs")
    if not legacy:
        require(not replay.exact_differences(source["functions_before"], after["functions_after"]), "saved function identity changed")
        require(not replay.exact_differences(provenance, source["provenance"])
                and not replay.exact_differences(provenance, after["provenance_after"]), "saved reconstruction provenance differs")
    cost = read(directory / "cost.json")
    require(cost["exit_code"] == 0 and cost["timed_out"] is False and cost["hashseed"] == 0,
            "child cost indicates exit/timeout/hashseed failure")
    if mode == "native":
        require(check["native_observer_absent"] is True and not (directory / "capture").exists(), "native observer present")
    else:
        require(check["capture_status"] == "captured_unverified_replay" and check["capture_check"]["pass"] is True,
                "observed capture check failed")
    return {"status": "PASS", "passed": True, "mode": mode, "dataset": dataset, "opaque_id": opaque_id,
            "frozen_sha256": frozen_sha256, "job_sha256": job_sha256, "check_sha256": sha(directory / "check.json"),
            "record_sha256": sha(directory / "ban-ghi-0.json"), "record_path": str(directory / "ban-ghi-0.json"),
            "native_frozen_exact": True, "source_checks_passed": True, "manifest_pass": True,
            "pid_and_external_streams_closure_required_by_controller": True}


def pure_helpers(code_hashes):
    """Original source AST only; no evaluator top-level numpy or ranking method."""
    def definitions(relative, functions, classes=()):
        path = safe_relative(REPO, relative)
        require(sha(path) == code_hashes[relative], "pure helper source differs")
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        chosen = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
                  and node.name in set(functions) | set(classes)]
        require({node.name for node in chosen} == set(functions) | set(classes), "pure helper definitions missing")
        return tree, chosen
    aggregator = {"__builtins__": __builtins__, "math": math}
    _tree, nodes = definitions("src/p3/ban_ghi.py", ("_khoa", "xep_thuc_the"))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "src/p3/ban_ghi.py", "exec"), aggregator)
    evaluator = {"__builtins__": __builtins__, "math": math, "Fraction": Fraction, "comb": math.comb}
    tree, nodes = definitions("src/p3/danh_gia.py", ("_khoa", "khoi_tu_ban_ghi", "phan_bo_hang", "do_ca", "cham_ca"), ("LoiBanGhi",))
    constants = {target.id: ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                 for target in node.targets if isinstance(target, ast.Name) and target.id == "TRANG_THAI"}
    evaluator.update(constants)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "src/p3/danh_gia.py", "exec"), evaluator)
    comparator_path = SCRIPTS / "compare_microrank_roundoff.py"
    require(sha(comparator_path) == PINS["results/T-032/scripts/compare_microrank_roundoff.py"], "ranking invariant helper changed")
    tree = ast.parse(comparator_path.read_text(encoding="utf-8-sig"))
    names = {"_record_fields", "_ranking", "ContractError"}
    nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names]
    constants = {target.id: ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                 for target in node.targets if isinstance(target, ast.Name) and target.id in ("EXACT_FIELDS", "EXCLUDED_FIELDS", "RANK_FIELDS", "KNOWN_STATUS")}
    rank = {"__builtins__": __builtins__, "math": math, "exact_differences": replay_module().exact_differences, **constants}
    require({node.name for node in nodes} == names, "ranking helper definition set differs")
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(comparator_path), "exec"), rank)
    return aggregator["xep_thuc_the"], evaluator["cham_ca"], rank["_ranking"]


def exact_contract(frozen, observed, code_hashes):
    replay = replay_module()
    differences = replay.compare_records(frozen, observed)
    require(not differences, "full exact record comparison failed")
    aggregator, evaluator, ranking = pure_helpers(code_hashes)
    original = copy.deepcopy((frozen, observed))
    a, b = ranking(frozen, aggregator), ranking(observed, aggregator)
    require(not replay.exact_differences(a, b), "mapping/count/order/tie/max invariant differs")
    entities = sorted(set(frozen["sets"]["observed_entities"]) | set(a["services"]))
    metrics = []
    for entity in entities:
        left, right = evaluator(frozen, entity), evaluator(observed, entity)
        require(not replay.exact_differences(left, right), "Hit@1..10/rank metric differs")
        metrics.append({"entity": entity, "frozen": left, "observed": right, "exact": True})
    require(not replay.exact_differences(original[0], frozen) and not replay.exact_differences(original[1], observed), "pure contract mutated records")
    count = len(a["operations"]) + len(a["services"])
    return {"passed": True, "exact": True, "operation_service_mapping_exact": True,
            "operation_order_exact": True, "service_order_exact": True, "service_tie_partition_exact": True,
            "counts_and_inventory_exact": True, "own_max_aggregation_exact": True, "hit_metrics": metrics,
            "numeric_summary": {"status": "COMPUTED_EXACT" if count else "NO_MATCHED_SCORE_PAIRS",
                "matched_score_count": count, "nonexact_score_count": 0, "max_ulp_distance": 0 if count else None,
                "max_relative": 0.0 if count else None,
                "max_relative_exact": {"numerator": 0, "denominator": 1} if count else None,
                "policy": "exact only; no threshold"}}


def audit_case(dataset, opaque_id, native_dir, observed_dir, out_dir, legacy=False):
    directory = new_directory(out_dir)
    try:
        startup_guard(ram=True)
        prepared = prepare_job(dataset, opaque_id)
        replay = replay_module()
        frozen, entry = prepared["frozen"], prepared["entry"]
        native_dir, observed_dir = Path(native_dir).resolve(), Path(observed_dir).resolve()
        job_sha256 = sha(native_dir / "job.json")
        require(job_sha256 == sha(observed_dir / "job.json"), "native/observed jobs not byte-identical")
        native = validate_child(dataset, opaque_id, "native", native_dir, job_sha256, entry["sha256"], legacy)
        observed = validate_child(dataset, opaque_id, "observed", observed_dir, job_sha256, entry["sha256"], legacy)
        native_record, observed_record = read(native_dir / "ban-ghi-0.json"), read(observed_dir / "ban-ghi-0.json")
        contracts = {"native_frozen": exact_contract(frozen, native_record, prepared["code_hashes"]),
                     "observed_native": exact_contract(native_record, observed_record, prepared["code_hashes"]),
                     "observed_frozen": exact_contract(frozen, observed_record, prepared["code_hashes"])}
        dump_new(directory / "exact-comparison.json", contracts)
        capture_summary = read(observed_dir / "capture/capture.json")
        require(capture_summary["status"] == "captured_unverified_replay", "capture summary status differs")
        capture_check = replay.verify_capture(observed_dir / "capture", capture_summary)
        require(capture_check["pass"] is True, "capture audit failed")
        dump_new(directory / "capture-check.json", capture_check)
        # Root information joins only here, after independent three-way exactness.
        bridge = tool_module("check_microrank_t028_v3.py")
        trust = {"frozen_record_sha256": entry["sha256"], "observed_record_sha256": observed["record_sha256"],
                 "native_observed_exact": True, "approved_record_comparison_passed": True}
        verdict = bridge.check_t028(repo_root=REPO, dataset=dataset, opaque_id=opaque_id,
                 frozen_record_path=REPO / entry["path"], frozen_record_sha256=entry["sha256"],
                 observed_record_path=observed_dir / "ban-ghi-0.json", observed_record_sha256=observed["record_sha256"], trusted_check=trust)
        dump_new(directory / "t028-check.json", verdict)
        require(all(verdict.get(key) is True for key in ("passed", "eligibility", "source_verified", "frozen_self_check_passed", "observed_equivalence_passed")),
                "T028 bridge failed; stop whole method")
        after = prepare_job(dataset, opaque_id)
        require(not replay.exact_differences(prepared, after), "source/job/input/provenance changed during audit")
        validate_child(dataset, opaque_id, "native", native_dir, job_sha256, entry["sha256"], legacy)
        validate_child(dataset, opaque_id, "observed", observed_dir, job_sha256, entry["sha256"], legacy)
        dump_new(directory / "source-checks.json", {"before": prepared, "after": after, "pin_checks_after": source_pins(),
                 "native": native, "observed": observed, "methods_executed": False})
        if legacy:
            retrospective_pins = source_pins(RETROSPECTIVE_PINS)
            closed = read(DIAGNOSTIC / "launcher-closed.json")
            require(closed["all_controller_streams_closed"] is True and len(closed["files"]) == 77, "old closure changed")
            closed_check = verify_manifest(DIAGNOSTIC, closed["files"], ("launcher-closed.json",))
            dump_new(directory / "retrospective-source-check.json", {"methods_executed": False, "old_files_edited": False,
                     "old_closed_manifest": {"path": str(DIAGNOSTIC / "launcher-closed.json"), "sha256": sha(DIAGNOSTIC / "launcher-closed.json")},
                     "old_root_receipt": {"path": "results/T-032/runs/microrank-laptop-diagnostic-verification-001/check.json",
                                          "sha256": RETROSPECTIVE_PINS["results/T-032/runs/microrank-laptop-diagnostic-verification-001/check.json"]},
                     "closed_77_rechecked_before_final_audit_manifest": closed_check, "pins": retrospective_pins})
        return close_check(directory, {"status": "PASS", "passed": True, "dataset": dataset, "opaque_id": opaque_id,
                 "source_status": frozen["status"], "laptop_status": observed_record["status"],
                 "classification": "exact" if frozen["status"] == "OK" else "non_OK_exact",
                 "native_frozen_exact": True, "observed_frozen_exact": True, "native_observed_exact": True,
                 "capture_pass": True, "t028_pass": True, "source_checks_passed": True,
                 "numeric_summary": contracts["observed_frozen"]["numeric_summary"],
                 "numeric_differences": [], "service_order_tie_differences": [], "other_differences": [],
                 "source": {"path": entry["path"], "sha256": entry["sha256"]}, "native": native, "observed": observed,
                 "comparison_sha256": sha(directory / "exact-comparison.json"), "t028_sha256": sha(directory / "t028-check.json"),
                 "intermediates_eligible": frozen["status"] == "OK", "non_OK_exact_observation_valid": frozen["status"] != "OK",
                 "non_OK_mechanism_NA_reason": None if frozen["status"] == "OK" else "native_non_OK_branch_no_OK_scores",
                 "methods_executed": False, "historical_trace_partition": "OPEN", "a_prime_authorized": False,
                 "research_limits": "current replay exactness only; no historical membership/physical waiting or causal claim"})
    except BaseException as error:
        return failure_check(directory, error)


def audit_retrospective(out_dir):
    startup_guard(ram=True)
    source_pins(RETROSPECTIVE_PINS)
    closed = read(DIAGNOSTIC / "launcher-closed.json")
    verification = read(REPO / "results/T-032/runs/microrank-laptop-diagnostic-verification-001/check.json")
    require(closed["status"] == verification["status"] == "PASS_SINGLE_CASE_EXACT_DIAGNOSTIC"
            and closed["exit_code"] == 0 and closed["timed_out"] is False
            and closed["all_controller_streams_closed"] is True, "old diagnostic not closed PASS")
    require(len(closed["files"]) == 77 and closed["manifest_excludes"] == ["launcher-closed.json"], "old closed artifact coverage differs")
    verify_manifest(DIAGNOSTIC, closed["files"], ("launcher-closed.json",))
    require(verification["closed_sha256"] == RETROSPECTIVE_PINS["results/T-032/runs/microrank-laptop-diagnostic-001/launcher-closed.json"]
            and verification["controller_sha256"] == sha(DIAGNOSTIC / "check.json")
            and verification["native_observed_frozen_exact"] is True
            and verification["source_input_import_function_hook_checks_passed"] is True, "old root receipt binding differs")
    old = read(DIAGNOSTIC / "check.json")
    require(old["calls_launched"] == ["native", "observed"] and old["native_frozen_exact"] is True
            and old["observed_frozen_exact"] is True and old["native_observed_exact"] is True, "old controller prerequisites differ")
    verify_manifest(DIAGNOSTIC, old["artifact_manifest"], tuple(old["manifest_excludes"]) + ("launcher-closed.json",))
    # Old root receipt establishes gone-at-closure. Reused PID numbers do not
    # identify an old worker; a currently live matching diagnostic command does.
    import psutil
    for pid in verification["pids_checked_gone"]:
        if psutil.pid_exists(pid):
            process = psutil.Process(pid)
            try:
                command = " ".join(process.cmdline()).replace("\\", "/").lower()
            except (psutil.NoSuchProcess, psutil.AccessDenied) as error:
                raise DiagnosticError("cannot establish reused diagnostic PID identity") from error
            require("microrank-laptop-diagnostic-001" not in command and "diagnose_microrank_laptop_v2.py" not in command,
                    "old diagnostic PID still active; no audit")
    return audit_case("RE2-TT", "dev-3defe3d34b", DIAGNOSTIC / "native", DIAGNOSTIC / "observed", out_dir, legacy=True)


def binding_fixtures(replay, directory):
    """Small exactness/manifest/job-path failures; no real method calls."""
    checks = []
    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
        require(condition, "wrapper binding fixture failed: " + name)
    base = {key: None for key in replay.EXACT_FIELDS}
    base.update(run_id="fixture", cost={}, opaque_id="fixture", method="microrank", variant="full", mode="a", seed=None,
                hashseed=0, status="OK", ranking_native=["caller_op", "root_op"],
                ranking=[{"item": "caller_op", "entity": "caller", "key": [2.0]}, {"item": "root_op", "entity": "root", "key": [1.0]}],
                entity_ranking=[{"entity": "caller", "key": [2.0], "tie_group": 0}, {"entity": "root", "key": [1.0], "tie_group": 1}],
                sets={"observed": 2, "observed_entities": ["caller", "root"], "returned": 2}, diagnostics={"counts": {"caller_op": 1}}, blocks=None)
    mutations = []
    def mutation(name, fn):
        value = copy.deepcopy(base); fn(value); mutations.append((name, value))
    mutation("one_bit_float", lambda x: x["ranking"][0]["key"].__setitem__(0, math.nextafter(2.0, math.inf)))
    mutation("float_type", lambda x: x["ranking"][0]["key"].__setitem__(0, 2))
    mutation("nonfinite_tag", lambda x: x["ranking"][0]["key"].__setitem__(0, {"__nonfinite__": "NaN"}))
    mutation("counts", lambda x: x["diagnostics"]["counts"].__setitem__("caller_op", 2))
    mutation("mapping", lambda x: x["ranking"][0].__setitem__("entity", "root"))
    mutation("candidate_inventory", lambda x: x["sets"]["observed_entities"].append("other"))
    mutation("operation_order", lambda x: x["ranking"].reverse())
    mutation("native_order", lambda x: x["ranking_native"].reverse())
    mutation("service_order", lambda x: x["entity_ranking"].reverse())
    mutation("service_tie", lambda x: x["entity_ranking"][1].__setitem__("tie_group", 0))
    mutation("schema", lambda x: x.__setitem__("unexpected", None))
    for name, changed in mutations:
        try:
            rejected = bool(replay.compare_records(base, changed))
        except replay.ReplayError:
            rejected = True
        check(name, rejected)
    zero_a, zero_b = copy.deepcopy(base), copy.deepcopy(base)
    zero_a["ranking"][0]["key"][0] = 0.0; zero_b["ranking"][0]["key"][0] = -0.0
    check("signed_zero", bool(replay.compare_records(zero_a, zero_b)))
    for token in ("NaN", "Infinity", "-Infinity"):
        path = directory / ("reject-json-" + token.replace("-", "minus") + ".json")
        with path.open("x", encoding="utf-8") as stream:
            stream.write('{"x":' + token + '}')
        try:
            read(path); rejected = False
        except DiagnosticError:
            rejected = True
        check("reject_literal_" + token, rejected)
    for relative in ("../source.json", "data/locked/x", "results/T-033/x", "test/x", "C:/x", "results\\T-032\\x"):
        try:
            safe_relative(REPO, relative); rejected = False
        except DiagnosticError:
            rejected = True
        check("reject_path_" + relative, rejected)
    branch = directory / "manifest-fixture"; branch.mkdir()
    dump_new(branch / "source.json", {"fixture": True})
    verdict = close_check(branch, {"status": "PASS", "passed": True, "intermediates_eligible": False})
    verify_closed_manifest(branch, verdict)
    tamper = directory / "manifest-tamper-copy"
    shutil.copytree(branch, tamper)
    with (tamper / "progress.jsonl").open("a", encoding="utf-8") as stream:
        stream.write('{"fixture":"terminal changed"}\n')
    try:
        verify_closed_manifest(tamper); rejected = False
    except DiagnosticError:
        rejected = True
    check("terminal_manifest_corruption_fail_stop", rejected)
    pinned_copy = directory / "pinned-source-fixture.txt"
    pinned_copy.write_text("fixture bytes\n", encoding="utf-8")
    actual_pin = sha(pinned_copy)
    verify_pinned_file(pinned_copy, actual_pin)
    try:
        verify_pinned_file(pinned_copy, "0" * 64); rejected = False
    except DiagnosticError:
        rejected = True
    check("changed_source_pin_fail_stop", rejected)
    for name, failed in (("failed_child", {"status": "FAIL_STOP", "differences": [], "source_checks_passed": True}),
                         ("exact_mismatch", {"status": "PASS", "differences": [{"kind": "float_exact"}], "source_checks_passed": True}),
                         ("source_failed", {"status": "PASS", "differences": [], "source_checks_passed": False})):
        try:
            child_exact_gate(failed); rejected = False
        except DiagnosticError:
            rejected = True
        check(name + "_cannot_gate_observed_or_next", rejected)
    return {"status": "PASS", "passed": True, "checks": checks, "methods_executed": False}


def fixtures(out_dir):
    directory = new_directory(out_dir)
    try:
        startup_guard(ram=True)
        source_pins()
        replay = replay_module()
        rows = catalog()
        dump_new(directory / "catalog-source-check.json", {"status": "PASS", "rows": rows, "scope": "source metadata only; no new replay"})
        sample = rows[0]
        _r, _entry, _frozen, _index, fixture_hashes, _audit, _pins = source_case(sample["dataset"], sample["opaque_id"])
        environment_before = environment_metadata()
        environment_guard(environment_before)
        functions_before = function_snapshot()
        imports_before = replay.loaded_sources(fixture_hashes)
        observer = directory / "original-observer-fixtures"; observer.mkdir()
        require(replay.fixtures(observer) == 0, "original observer/record fixtures failed")
        original = read(observer / "check.json")
        require(original["status"] == "PASS" and len(original["fixtures"]) == 4, "old observer fixture coverage changed")
        verify_manifest(observer, original["artifact_manifest"])
        aggregator, evaluator, _ranking = pure_helpers(fixture_hashes)
        comparator = tool_module("compare_microrank_roundoff.py")
        original_comparator_fixtures = comparator.fixture_report(aggregator, evaluator)
        # Original CLI tags invalid synthetic floats in fixture reports only.
        # This does not transform any real frozen/native/observed record.
        dump_new(directory / "original-comparator-fixtures.json", comparator._json_safe(original_comparator_fixtures))
        require(original_comparator_fixtures["status"] == "PASS", "original comparator fixtures failed")
        dump_new(directory / "original-comparator-fixture-policy.json", {
                 "scope": "preserved old comparator tool fixtures only; no real-case numeric acceptance",
                 "real_laptop_gate": "independent replay.compare_records exact before bridge",
                 "threshold_applied_to_laptop_records": False, "real_case_methods_executed": False})
        bridge = tool_module("check_microrank_t028_v3.py")
        bridge_fixture = bridge.fixtures(REPO)
        dump_new(directory / "bridge-fixtures.json", bridge_fixture)
        require(bridge_fixture["passed"] is True, "bridge fixtures failed")
        frozen52 = bridge.frozen_self_check_all(REPO)
        dump_new(directory / "frozen-52-self-check.json", frozen52)
        require(frozen52["passed"] is True and frozen52["checked_count"] == frozen52["passed_count"] == 52
                and frozen52["not_run_count"] == 0, "full52 frozen self-check failed")
        binding = binding_fixtures(replay, directory)
        dump_new(directory / "binding-fixtures.json", binding)
        # Validate both Nezha provenance branches without reading raw telemetry
        # or invoking a method. Source record hashes/CONFIG/WHY/extra are bound.
        provenance = []
        for dataset, reused in (("RE2-TT", None), ("Nezha-OB", False), ("Nezha-OB", True)):
            candidates = [x for x in rows if x["dataset"] == dataset and (reused is None or x["source_entry"]["reused_pilot"] is reused)]
            require(candidates, "missing source provenance branch")
            selected = min(candidates, key=lambda x: x["opaque_id"])
            r, entry, frozen, index26, hashes, audit, pins = source_case(dataset, selected["opaque_id"])
            job, inputs, constants, route = job_metadata(dataset, selected["opaque_id"], r, entry, frozen, index26, audit)
            if dataset == "Nezha-OB":
                expected = {"pilot_view": "main", "pilot_only": True, "source_provenance_file": "ket-qua.json"} if reused else {
                    "source_view": "main", "pilot_only": False, "source_provenance_file": "ket-qua.json"}
                require(all(key in frozen["extra"] and type(frozen["extra"][key]) is type(value) and frozen["extra"][key] == value
                            for key, value in expected.items()), "Nezha provenance extra differs")
                require("kind" not in job and "config_id" not in job and constants["CONFIG"] != "p3-re2tt-v2", "Nezha RE2 fallback detected")
            provenance.append({"dataset": dataset, "opaque_id": selected["opaque_id"], "reused_pilot": reused,
                               "source": {"path": entry["path"], "sha256": entry["sha256"]}, "route": route, "passed": True})
        dump_new(directory / "two-dataset-provenance-fixtures.json", {"status": "PASS", "rows": provenance, "methods_executed": False})
        require(sys.gettrace() is None and sys.getprofile() is None, "fixtures left hook")
        require(function_snapshot() == functions_before, "fixtures changed native function identities")
        environment_after = environment_metadata()
        environment_guard(environment_after)
        stored_environment_guard(environment_before, environment_after)
        dump_new(directory / "fixture-source-checks.json", {"code_hashes": fixture_hashes,
                 "environment_before": environment_before, "environment_after": environment_after,
                 "functions_before": functions_before, "functions_after": function_snapshot(),
                 "actual_imports_before": imports_before, "actual_imports_after": replay.loaded_sources(fixture_hashes),
                 "hooks_restored": True, "functions_unchanged": True, "pin_checks_after": source_pins()})
        source_pins()
        return close_check(directory, {"status": "PASS", "passed": True, "observer_fixture_count": 4,
                 "original_comparator_fixtures_pass": True, "bridge_pass": True, "frozen52_pass": True,
                 "binding_pass": True, "provenance_pass": True,
                 "frozen52_checked_count": 52, "frozen_self_check_count": 52, "all_fixture_checks_passed": True,
                 "intermediates_eligible": False, "a_prime_authorized": False,
                 "real_case_methods_executed": False, "synthetic_observer_methods_executed": True})
    except BaseException as error:
        return failure_check(directory, error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inner = sub.add_parser("child")
    inner.add_argument("mode", choices=("native", "observed")); inner.add_argument("dataset", choices=DATASETS)
    inner.add_argument("opaque_id"); inner.add_argument("directory")
    inner.add_argument("--job-sha256", required=True); inner.add_argument("--frozen-sha256", required=True)
    prepare = sub.add_parser("prepare"); prepare.add_argument("dataset", choices=DATASETS); prepare.add_argument("opaque_id"); prepare.add_argument("directory")
    fixture = sub.add_parser("fixture"); fixture.add_argument("directory")
    audit = sub.add_parser("audit"); audit.add_argument("dataset", choices=DATASETS); audit.add_argument("opaque_id")
    audit.add_argument("native_dir"); audit.add_argument("observed_dir"); audit.add_argument("directory")
    retrospective = sub.add_parser("audit-retrospective"); retrospective.add_argument("directory")
    args = parser.parse_args()
    directory = None
    try:
        if args.command == "child":
            requested = output_path(args.directory)
            require(requested == (COHORT / "cases" / args.dataset / args.opaque_id / args.mode).resolve()
                    and requested.is_dir() and {path.name for path in requested.iterdir()} == {"job.json"},
                    "child must begin in the exact new job-only directory; no rewrite/retry")
            directory = requested
            return child(args.mode, args.dataset, args.opaque_id, directory, args.job_sha256, args.frozen_sha256)
        if args.command == "prepare":
            directory = new_directory(args.directory)
            startup_guard(ram=True)
            prepared = prepare_job(args.dataset, args.opaque_id)
            dump_new(directory / "prepare.json", prepared)
            result = close_check(directory, {"status": "PASS", "passed": True, "dataset": args.dataset, "opaque_id": args.opaque_id,
                     "source_checks_passed": True, "prepare_sha256": sha(directory / "prepare.json"),
                     "frozen_sha256": prepared["entry"]["sha256"], "methods_executed": False, "intermediates_eligible": False})
        elif args.command == "fixture":
            result = fixtures(args.directory)
        elif args.command == "audit":
            result = audit_case(args.dataset, args.opaque_id, args.native_dir, args.observed_dir, args.directory)
        else:
            result = audit_retrospective(args.directory)
        return 0 if result.get("status") == "PASS" and result.get("passed") is True else 1
    except BaseException as error:
        if directory is not None and directory.is_dir():
            failure_check(directory, error)
        print(json.dumps({"status": "FAIL_STOP", "error_type": type(error).__name__, "error": str(error),
                          "intermediates_eligible": False}, ensure_ascii=False), file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
