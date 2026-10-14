"""Prepare/run the approved MicroRank record contract over 30 RE2 + 22 Nezha.

prepare reads verified frozen metadata and completed pilot artifacts. It runs
only the pure comparator/T028 bridge, never a method. It creates a 52-row
not_run table and an explicit, unverified 2x resource estimate for root review.
run requires the reviewed plan's byte hash and an explicit overall wall limit.
It rechecks both pilots, then launches one unchanged approved wrapper at a time.
No case, source ERROR, failed run or raw difference is removed or overwritten.

Pilot CLI bindings are supplied by root, not inferred from a remembered hash.
The RE2 comparison and bridge may share a posthoc stage and its monitor. Its
old observed exact FAIL can be reused only after capture, exact native/observed,
the approved frozen contract and the full T028 bridge all pass independently.
Every new case has one observed and one independent native worker in its child.
Case contract completion is not whole-core/A-prime or causal authorization.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
import traceback

BASE = Path("/home/ubuntu/rca/T-032")
SCRIPTS = BASE / "scripts"
WRAPPER_SHA256 = "e988952c402ba9f0a6ce52c1c79835594af68bebee99ba687d229ba6a9250be5"
DIAGNOSTIC_SHA256 = "c6c64b348a7990ad1b74d60f41246765017435da29194e9dd207b18befd98437"
COHORT_SIZES = {"RE2-TT": 30, "Nezha-OB": 22}
CLASSES = ("exact", "numeric_only", "operation_order", "service_order_changed", "blocked", "not_run")
TASK_MAX_BYTES = 8 * 2**30
PER_CASE_MAX_S = 600
PER_CASE_MAX_BYTES = 150 * 2**20
POLL_S = 0.5
CONTROLLER_RESERVE_BYTES = 4 * 2**20
SCHEMA = "T032-MicroRank-approved-cohort-v1"


class BatchError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise BatchError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    def reject(value):
        raise BatchError("nonfinite JSON token: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), parse_constant=reject)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def serialized(value):
    """Compare report JSON representations; never change either input record."""
    return json.loads(encoded(value))


def dump(path, value):
    with Path(path).open("xb") as stream:
        stream.write(encoded(value))


def snapshot(path, value):
    temporary = Path(path).with_suffix(Path(path).suffix + ".tmp")
    with temporary.open("wb") as stream:
        stream.write(encoded(value))
    temporary.replace(path)


def emit(directory, event, **fields):
    row = {"at_utc": now(), "event": event, **fields}
    with (directory / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps(row, ensure_ascii=False, allow_nan=False), flush=True)


def run_path(raw):
    path = Path(raw).expanduser().resolve()
    require(BASE / "runs" in path.parents, "artifact is outside T032/runs")
    require(not any(part.lower() in ("t-033", "locked", "test", "tests", "heldout", "archive")
                    for part in path.parts), "artifact path outside approved scope")
    return path


def new_output(raw):
    path = run_path(raw)
    require(path.parent == BASE / "runs" and not path.exists(), "output must be a new direct run directory")
    path.mkdir(exist_ok=False)
    return path


def verify(path, expected, audit, authority):
    path = Path(path).resolve()
    require(isinstance(expected, str) and len(expected) == 64
            and all(c in "0123456789abcdef" for c in expected), "missing trusted hash")
    actual = sha(path)
    audit.append({"path": str(path), "sha256": actual, "expected_sha256": expected,
                  "bytes": path.stat().st_size, "authority": authority, "passed": actual == expected})
    require(actual == expected, "source/artifact hash changed: " + str(path))
    return path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def preflight(audit):
    require(sys.platform == "linux" and Path.home().resolve() == Path("/home/ubuntu")
            and Path(__file__).resolve().parent == SCRIPTS, "EC2-only T032 controller")
    require(os.environ.get("PYTHONHASHSEED") == "0", "frozen hashseed 0 required")
    require(sys.gettrace() is None and sys.getprofile() is None, "unexpected observer/profile in controller")
    sys.dont_write_bytecode = True
    path = verify(SCRIPTS / "replay_microrank_approved_v2.py", WRAPPER_SHA256, audit, "approved wrapper handoff")
    wrapper = load("t032_batch_approved_wrapper", path)
    wrapper.environment_guard()
    replay = wrapper.preflight(audit)
    require(wrapper.MAX_WALL_S == PER_CASE_MAX_S and wrapper.MAX_NEW_BYTES == PER_CASE_MAX_BYTES,
            "approved child operating bounds changed")
    comparator = load("t032_batch_comparator", verify(SCRIPTS / "compare_microrank_roundoff.py",
        wrapper.COMPARATOR_SHA256, audit, "approved comparator pin"))
    bridge = load("t032_batch_bridge", verify(SCRIPTS / "check_microrank_t028_v2.py",
        wrapper.BRIDGE_SHA256, audit, "approved T028 bridge pin"))
    return wrapper, replay, comparator, bridge


def scripts(wrapper):
    expected = {"replay_microrank_approved_v2.py": WRAPPER_SHA256,
                "diagnose_microrank.py": DIAGNOSTIC_SHA256,
                "replay_microrank.py": wrapper.REPLAY_SHA256,
                "capture_microrank.py": wrapper.CAPTURE_SHA256,
                "compare_microrank_roundoff.py": wrapper.COMPARATOR_SHA256,
                "check_microrank_t028_v2.py": wrapper.BRIDGE_SHA256}
    for name, digest in expected.items():
        require(sha(SCRIPTS / name) == digest, "pinned script changed: " + name)
    # The controller and launcher are bound to this reviewed plan, not silently
    # substituted on run. Launcher accounting remains the existing 8 GiB guard.
    return {**expected, Path(__file__).name: sha(__file__),
            "start_script.sh": sha(SCRIPTS / "start_script.sh"),
            "run_guarded.py": sha(SCRIPTS / "run_guarded.py")}


def environment():
    keys = ("PYTHONHASHSEED", "PYTHONPATH", "PYTHONDONTWRITEBYTECODE", "PYTHONIOENCODING",
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "TMPDIR",
            "XDG_CACHE_HOME", "MPLCONFIGDIR", "MPLBACKEND")
    packages = {}
    for name in ("numpy", "pandas", "scipy", "pyarrow", "psutil"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {"python": sys.version, "executable": str(Path(sys.executable).resolve()),
            "platform": platform.platform(), "cwd": str(Path.cwd().resolve()),
            "packages": packages, "variables": {key: os.environ.get(key) for key in keys}}


def inventory(replay, audit):
    manifest = replay.read(replay.safe_source(replay.M24))
    index24 = replay.read(replay.verify(replay.I24, manifest["source_hashes"][replay.I24],
                                       replay.M24 + "#/source_hashes", audit))
    index26 = replay.verified_index26(audit)
    ids = {"RE2-TT": sorted(row["opaque_id"] for row in index24["records"]
                          if row["method"] == "microrank" and row["variant"] == "full"),
           "Nezha-OB": sorted(row["opaque_id"] for row in index26["unique_records"]
                             if row["worker_method"] == "microrank" and row["source_view"] == "main")}
    package = replay.read(BASE / "inputs/package-manifest.json")
    package_entries = {row["path"]: row for row in package["files"]}
    allows = {}
    for dataset, relative in (("RE2-TT", "results/T-022/allowlist-dev.json"),
                              ("Nezha-OB", "results/T-026/allowlist-dev.json")):
        path = replay.verify(relative, package_entries[relative]["sha256"], "pinned package#/files", audit)
        cases = replay.read(path)["cases"]
        require(isinstance(cases, list), "allowlist case schema changed")
        allows[dataset] = {case["opaque_id"]: case for case in cases}
        require(len(allows[dataset]) == len(cases) == COHORT_SIZES[dataset], "allowlist duplicate/cardinality changed")
    rows = []
    for dataset, cohort in ids.items():
        require(len(cohort) == len(set(cohort)) == COHORT_SIZES[dataset], "frozen cohort cardinality changed")
        require(set(cohort) == set(allows[dataset]), "allowlist/frozen cohort membership changed")
        for opaque_id in cohort:
            entry, frozen, _index, _code = replay.source_for(dataset, opaque_id, audit)
            files = allows[dataset][opaque_id]["files"]
            selected = {name: meta["sha256"] for name, meta in files.items() if meta is not None}
            require(selected == frozen["input_sha256"], "allowlist/frozen input hashes changed")
            require(all(type(meta["bytes"]) is int and meta["bytes"] >= 0
                        for meta in files.values() if meta is not None), "unknown allowlist file bytes")
            trace_bytes = sum(meta["bytes"] for name, meta in files.items() if meta is not None
                              and (name == "traces.parquet" if dataset == "RE2-TT" else "/trace/" in name))
            rows.append({"dataset": dataset, "opaque_id": opaque_id, "entry": entry,
                         "source_status": frozen["status"], "input_shape": frozen["input_shape"],
                         "window": frozen["window"], "input_sha256": frozen["input_sha256"],
                         "source_cost": frozen["cost"],
                         "source_input_bytes": sum(meta["bytes"] for meta in files.values() if meta is not None),
                         "source_trace_bytes": trace_bytes})
    require(len(rows) == 52, "expected all 52 source cases")
    return rows


def initial_rows(sources):
    return [{"dataset": source["dataset"], "opaque_id": source["opaque_id"],
             "source_status": source["source_status"], "source_sha256": source["entry"]["sha256"],
             "classification": "not_run", "case_status": "not_run", "intermediates_eligible": False,
             "max_ulp_distance": None, "max_relative": None, "max_relative_exact": None,
             "numeric_summary": None, "reused": False, "blocked_reasons": [],
             "record_comparison_classification": None, "artifacts": None} for source in sources]


def table(rows, status):
    def counts(subset):
        classifications = Counter(row["classification"] for row in subset)
        return {"denominator": len(subset),
                "classification_counts": {key: classifications[key] for key in CLASSES},
                "passed": sum(row["case_status"] == "PASS" for row in subset),
                "blocked": sum(row["case_status"] == "FAIL_STOP" for row in subset),
                "not_run": sum(row["case_status"] == "not_run" for row in subset)}
    return {"schema": SCHEMA, "status": status, "updated_utc": now(), "rows": rows,
            "overall": counts(rows),
            "by_dataset": {dataset: counts([row for row in rows if row["dataset"] == dataset])
                           for dataset in COHORT_SIZES},
            "all_case_contracts_passed": len(rows) == 52 and all(row["case_status"] == "PASS" for row in rows),
            "cohort_ready": False, "A_prime_authorized": False,
            "limits": "Record/capture/bridge contracts only; no historical partition or causal certification."}


def report_agrees(replay, saved, fresh, description):
    require(isinstance(saved, dict) and set(fresh) <= set(saved), description + " report schema incomplete")
    differences = replay.exact_differences(serialized(fresh), {key: saved[key] for key in fresh})
    require(not differences, description + " saved/current pure verdict differs: " + json.dumps(differences[:3]))


def verified_pair(wrapper, replay, comparator, dataset, opaque_id, bindings, audit):
    require(set(("frozen", "observed", "native")) <= set(bindings), "record binding missing")
    observed = bindings["observed"]
    native = bindings["native"]
    observed_dir, native_dir = run_path(observed["path"]).parent, run_path(native["path"]).parent
    comparison = comparator.compare_case(dataset, opaque_id, observed_dir, observed["trusted_check_sha256"],
        native_run=native_dir, native_check_sha256=native["trusted_check_sha256"], source_audit=[])
    require(comparison["record_contract_pass"] is True, "approved frozen contract did not pass")
    require(comparison["native_observed_exact"]["pass"] is True
            and not comparison["native_observed_exact"]["differences"], "native/observed not exact")
    observed_check = read(observed_dir / "check.json")
    native_source = read(native_dir / "source.json")
    native_script_sha = native_source.get("script_sha256")
    require(native_source.get("observer_attached") is False
            and native_script_sha in (WRAPPER_SHA256, DIAGNOSTIC_SHA256),
            "native run is not an approved observer-free execution")
    if native_script_sha == DIAGNOSTIC_SHA256:
        verify(SCRIPTS / "diagnose_microrank.py", DIAGNOSTIC_SHA256, audit, "retained native diagnostic source")
    require(observed_check.get("capture_status") == "captured_unverified_replay"
            and observed_check.get("capture_check", {}).get("pass") is True, "original capture check incomplete")
    require(sha(observed_dir / "job.json") == sha(native_dir / "job.json"), "pilot native/observed jobs differ")
    for name, binding in comparison["record_bindings"].items():
        require(binding["sha256"] == bindings[name]["sha256"], "record byte binding changed: " + name)
    audit.extend(comparison["source_checks"])
    return comparison, observed_dir, native_dir, observed_check


def pure_bridge(replay, bridge, comparison, saved, audit):
    bindings = comparison["record_bindings"]
    verdict = bridge.check_t028(repo_root=BASE / "repo", dataset=comparison["dataset"],
        opaque_id=comparison["opaque_id"], frozen_record_path=replay.safe_source(bindings["frozen"]["path"]),
        frozen_record_sha256=bindings["frozen"]["sha256"],
        observed_record_path=bindings["observed"]["path"], observed_record_sha256=bindings["observed"]["sha256"],
        trusted_check={"frozen_record_sha256": bindings["frozen"]["sha256"],
                       "observed_record_sha256": bindings["observed"]["sha256"],
                       "native_observed_exact": True, "approved_record_comparison_passed": True})
    for field in ("passed", "eligibility", "source_verified", "frozen_self_check_passed", "observed_equivalence_passed"):
        require(verdict.get(field) is True, "T028 bridge prerequisite/semantic self-check failed: " + field)
    require(verdict.get("graph_reconstructed") is False and verdict.get("record_inputs_mutated") is False,
            "T028 bridge graph/mutation declaration invalid")
    report_agrees(replay, saved, verdict, "T028")
    audit.extend(verdict["read_set"])
    return verdict


def verify_artifacts(wrapper, directory, check):
    manifest = check.get("artifact_manifest")
    require(isinstance(manifest, list) and manifest, "approved wrapper artifact manifest absent")
    seen = set()
    for row in manifest:
        require(row["path"] not in seen, "duplicate case artifact path")
        seen.add(row["path"])
        path = (directory / row["path"]).resolve()
        require(directory in path.parents and not path.is_symlink(), "case artifact escaped")
        require(path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], "case artifact bytes changed")
    actual = {path.relative_to(directory).as_posix() for path in directory.rglob("*")
              if path.is_file() and path != directory / "check.json"}
    require(seen == actual, "case artifact manifest missing/extra file")


def validate_approved(wrapper, replay, comparator, bridge, directory, expected_sha, audit):
    directory = run_path(directory)
    check = read(verify(directory / "check.json", expected_sha, audit, "approved case top-check"))
    require(check["status"] == "PASS" and check["intermediates_eligible"] is True, "approved case did not pass")
    for field in ("source_job_input_F_checks", "capture_check_passed", "observer_function_identity_check_passed",
                  "native_observed_exact", "approved_record_comparison_passed", "t028_bridge_passed"):
        require(check.get(field) is True, "approved case gate missing: " + field)
    require(check["cohort_ready"] is False and check["A_prime_authorized"] is False, "case overclaims cohort/A-prime")
    verify_artifacts(wrapper, directory, check)
    invocation = read(directory / "invocation.json")
    require(invocation["script_sha256"] == WRAPPER_SHA256 and invocation["python"] == sys.version
            and invocation["executable"] == sys.executable and invocation["hashseed"] == "0", "case source/environment changed")
    require(invocation["dependency_hashes"] == {"replay": wrapper.REPLAY_SHA256, "capture": wrapper.CAPTURE_SHA256,
            "comparator": wrapper.COMPARATOR_SHA256, "bridge": wrapper.BRIDGE_SHA256}, "case dependency pins changed")
    require(check["guard"]["failure"] is None and check["elapsed_s"] <= PER_CASE_MAX_S
            and wrapper.logical_size(directory) <= PER_CASE_MAX_BYTES, "approved case operating bounds failed")
    dataset, opaque_id = check["dataset"], check["opaque_id"]
    comparison, observed, native, old_check = verified_pair(wrapper, replay, comparator, dataset, opaque_id,
                                                           check["record_bindings"], audit)
    require(observed == directory / "observed" and native == directory / "native", "approved pair path differs")
    report_agrees(replay, read(directory / "roundoff-comparison.json"), comparison, "approved comparison")
    pure_bridge(replay, bridge, comparison, read(directory / "t028-check.json"), audit)
    require(check["classification"] == comparison["classification"]
            and check["numeric_summary"] == comparison["numeric_summary"], "case summary differs from full comparison")
    require(check["frozen_sha256"] == comparison["record_bindings"]["frozen"]["sha256"], "case frozen reference changed")
    return comparison, {"path": str(directory), "check_sha256": expected_sha,
                        "original_exact_status": old_check["status"], "logical_bytes": wrapper.logical_size(directory)}


def monitor(directory, audit, open_items, *, allow_old_exact_fail=False):
    directory = run_path(directory)
    if directory.parent != BASE / "runs":
        open_items.append({"input": str(directory), "needed": "standard stage monitor; direct run directory required"})
        return None
    path = BASE / "runs" / (directory.name + "-monitor") / "status.json"
    if not path.is_file():
        open_items.append({"input": str(path), "needed": "completed monitored elapsed_s/peak_tree_rss_bytes"})
        return None
    digest = sha(path)
    verify(path, digest, audit, "completed pilot process monitor, bound into plan")
    value = read(path)
    accepted = (value.get("status") == "PASS" and value.get("exit_code") == 0
                or allow_old_exact_fail and value.get("status") == "FAIL" and value.get("exit_code") == 1)
    require(accepted and not value.get("error"), "pilot process did not finish normally: " + str(path))
    require(type(value.get("elapsed_s")) in (int, float) and math.isfinite(value["elapsed_s"]) and value["elapsed_s"] > 0
            and type(value.get("peak_tree_rss_bytes")) is int and value["peak_tree_rss_bytes"] > 0,
            "pilot monitor missing actual elapsed/RAM")
    return {"path": str(path), "sha256": digest, "status": value["status"], "exit_code": value["exit_code"],
            "elapsed_s": value["elapsed_s"], "peak_tree_rss_bytes": value["peak_tree_rss_bytes"]}


def bundle_bytes(wrapper, directories):
    unique = {}
    for directory in directories:
        directory = run_path(directory)
        unique[str(directory)] = wrapper.logical_size(directory)
        if directory.parent == BASE / "runs":
            monitor_dir = BASE / "runs" / (directory.name + "-monitor")
            if monitor_dir.is_dir():
                unique[str(monitor_dir)] = wrapper.logical_size(monitor_dir)
            for suffix in ("-launcher.out", "-launcher.err", "-launcher.pid"):
                path = BASE / "runs" / (directory.name + suffix)
                if path.is_file():
                    unique[str(path)] = path.stat().st_size
    return {"logical_bytes": sum(unique.values()), "components": unique}


def pilots(wrapper, replay, comparator, bridge, inputs, audit):
    open_items = []
    comparison_path = run_path(inputs["re2_comparison"])
    saved = read(verify(comparison_path, inputs["re2_comparison_sha256"], audit, "root RE2 comparator report"))
    require(saved.get("dataset") == "RE2-TT" and saved.get("script_sha256") == wrapper.COMPARATOR_SHA256,
            "RE2 pilot comparator source/identity invalid")
    comparison, observed, native, old_check = verified_pair(wrapper, replay, comparator, "RE2-TT",
                                                           saved["opaque_id"], saved["record_bindings"], audit)
    report_agrees(replay, saved, comparison, "RE2 comparison")
    bridge_path = run_path(inputs["re2_t028"])
    saved_bridge = read(verify(bridge_path, inputs["re2_t028_sha256"], audit, "root RE2 T028 report"))
    pure_bridge(replay, bridge, comparison, saved_bridge, audit)
    require(old_check["status"] in ("PASS", "FAIL"), "old observed replay did not complete its exact comparison")
    stage_dirs = {observed, native, comparison_path.parent, bridge_path.parent}
    measurements = [monitor(path, audit, open_items,
                            allow_old_exact_fail=(path == observed and old_check["status"] == "FAIL"))
                    for path in sorted(stage_dirs)]
    measured = [row for row in measurements if row is not None]
    peak_by_dir = {str(path): value["peak_tree_rss_bytes"] for path, value in zip(sorted(stage_dirs), measurements)
                   if value is not None}
    other_peaks = [value for path, value in peak_by_dir.items() if path != str(observed)]
    re2_peak = (peak_by_dir[str(observed)] + max(other_peaks)
                if not open_items and str(observed) in peak_by_dir and other_peaks else None)
    re2_bytes = bundle_bytes(wrapper, stage_dirs)
    re2 = {"dataset": "RE2-TT", "opaque_id": comparison["opaque_id"], "validated": True,
           "binding_inputs": {key: value for key, value in inputs.items() if key.startswith("re2_")},
           "record_bindings": comparison["record_bindings"], "comparison": comparison,
           "old_observed_exact_status": old_check["status"], "old_exact_check_retained": True,
           "native_observed_exact": True, "t028_bridge_passed": True, "monitors": measured,
           "elapsed_s": sum(row["elapsed_s"] for row in measured) if not open_items else None,
           "peak_rss_estimate_anchor_bytes": re2_peak, "output": re2_bytes,
           "benchmark_kind": "separate completed observed/native/posthoc stages; no new method run",
           "RAM_limit": "CANDIDATE observed peak + max other stage peaks; combined wrapper peak not measured.",
           "capture_cost": read(observed / "ban-ghi-0.json")["cost"],
           "native_cost": read(native / "ban-ghi-0.json")["cost"]}
    nezha_dir = run_path(inputs["nezha_pilot_run"])
    fresh, binding = validate_approved(wrapper, replay, comparator, bridge, nezha_dir,
                                     inputs["nezha_pilot_check_sha256"], audit)
    require(fresh["dataset"] == "Nezha-OB", "approved second pilot is not Nezha")
    measured_nezha = monitor(nezha_dir, audit, open_items)
    nezha = {"dataset": "Nezha-OB", "opaque_id": fresh["opaque_id"], "validated": True,
             "binding_inputs": {key: value for key, value in inputs.items() if key.startswith("nezha_")},
             "record_bindings": fresh["record_bindings"], "comparison": fresh, "case": binding,
             "monitors": [measured_nezha] if measured_nezha else [],
             "elapsed_s": measured_nezha["elapsed_s"] if measured_nezha else None,
             "peak_rss_estimate_anchor_bytes": measured_nezha["peak_tree_rss_bytes"] if measured_nezha else None,
             "output": bundle_bytes(wrapper, [nezha_dir]), "benchmark_kind": "actual approved wrapper tree",
             "capture_cost": read(nezha_dir / "observed/ban-ghi-0.json")["cost"],
             "native_cost": read(nezha_dir / "native/ban-ghi-0.json")["cost"]}
    return {"RE2-TT": re2, "Nezha-OB": nezha}, open_items


def estimate(sources, pilot_rows, open_items):
    estimates = []
    for source in sources:
        anchor = pilot_rows[source["dataset"]]
        baseline = next((row for row in sources if (row["dataset"], row["opaque_id"]) ==
                         (anchor["dataset"], anchor["opaque_id"])), None)
        require(baseline is not None, "pilot is not in the frozen 52-case cohort")
        if source["opaque_id"] == anchor["opaque_id"]:
            continue
        ratios = {"minimum": 1.0}
        cost, base_cost = source["source_cost"].get("wall_s"), baseline["source_cost"].get("wall_s")
        if (type(cost) in (int, float) and type(base_cost) in (int, float)
                and math.isfinite(cost) and math.isfinite(base_cost) and cost >= 0 and base_cost > 0):
            ratios["source_wall"] = cost / base_cost
        else:
            open_items.append({"input": source["entry"]["path"], "needed": "finite positive frozen source wall cost"})
        for key in ("spans", "operations"):
            value, base_value = source["input_shape"].get(key), baseline["input_shape"].get(key)
            if type(value) is int and type(base_value) is int and base_value > 0:
                ratios[key] = value / base_value
        for key in ("source_input_bytes", "source_trace_bytes"):
            if baseline[key] > 0:
                ratios[key] = source[key] / baseline[key]
        factor = max(ratios.values())
        require(math.isfinite(factor) and factor >= 1, "invalid extrapolation factor")
        estimates.append({"dataset": source["dataset"], "opaque_id": source["opaque_id"],
                          "source_status": source["source_status"], "ratios": ratios, "factor": factor,
                          "seconds": 2 * factor * anchor["elapsed_s"] if anchor["elapsed_s"] is not None else None,
                          "new_bytes": math.ceil(2 * factor * anchor["output"]["logical_bytes"]),
                          "peak_rss_bytes": math.ceil(2 * factor * anchor["peak_rss_estimate_anchor_bytes"])
                              if anchor["peak_rss_estimate_anchor_bytes"] is not None else None})
    require(len(estimates) == 50, "exactly two distinct dataset pilots and 50 new cases required")
    complete = not open_items and all(row["seconds"] is not None and row["peak_rss_bytes"] is not None for row in estimates)
    return {"status": "CANDIDATE_UNVERIFIED_FULL_COHORT" if complete else "OPEN",
            "remaining_cases": 50, "remaining_s": sum(row["seconds"] for row in estimates) if complete else None,
            "remaining_bytes": sum(row["new_bytes"] for row in estimates) + CONTROLLER_RESERVE_BYTES,
            "estimated_peak_rss_bytes": max(row["peak_rss_bytes"] for row in estimates) if complete else None,
            "controller_reserve_bytes": CONTROLLER_RESERVE_BYTES, "cases": estimates,
            "note": "Unverified 2x allowance from pilot stage costs, source wall/input shape and allowlist byte ratios.",
            "limits": ["No speedup or full-cohort measurement inferred.",
                       "Null operation counts on source ERROR remain null; case is still scheduled.",
                       "Trace/PageRank size and native branches can make these extrapolations wrong.",
                       "RE2 concurrent-process RAM is an explicit candidate, not a measured combined peak.",
                       "4 MiB controller/log reserve is an operating allowance, not a measured output size."]}


def resources(wrapper):
    import psutil
    return {"remote_task_logical_bytes": wrapper.logical_size(BASE),
            "available_ram_bytes": psutil.virtual_memory().available,
            "free_disk_bytes": shutil.disk_usage(BASE).free}


def row_result(source, comparison, artifacts, *, reused):
    numeric = comparison["numeric_summary"]
    require(comparison["classification"] in CLASSES and comparison["classification"] not in
            ("blocked", "service_order_changed", "not_run"), "successful comparison classification invalid")
    return {"dataset": source["dataset"], "opaque_id": source["opaque_id"],
            "source_status": source["source_status"], "source_sha256": source["entry"]["sha256"],
            "case_status": "PASS", "classification": comparison["classification"],
            "record_comparison_classification": comparison["classification"], "intermediates_eligible": True,
            "reused": reused, "max_ulp_distance": numeric["max_ulp_distance"],
            "max_relative": numeric["max_relative"], "max_relative_exact": numeric["max_relative_exact"],
            "numeric_summary": numeric, "blocked_reasons": [], "artifacts": artifacts,
            "record_bindings": comparison["record_bindings"], "native_observed_exact": True,
            "capture_check_passed": True, "approved_record_comparison_passed": True, "t028_bridge_passed": True}


def prepare(args, output, wrapper, replay, comparator, bridge, audit):
    sources = inventory(replay, audit)
    rows = initial_rows(sources)
    snapshot(output / "52-cases.json", table(rows, "PREPARE_NOT_RUN"))
    inputs = {key: getattr(args, key) for key in ("re2_comparison", "re2_comparison_sha256",
        "re2_t028", "re2_t028_sha256", "nezha_pilot_run", "nezha_pilot_check_sha256")}
    pilot_rows, open_items = pilots(wrapper, replay, comparator, bridge, inputs, audit)
    candidate = estimate(sources, pilot_rows, open_items)
    measured = resources(wrapper)
    plan = {"schema": SCHEMA, "status": "PREPARED_OPEN" if open_items else "PREPARED_NOT_STARTED",
            "sources": sources, "pilot_inputs": inputs, "pilots": pilot_rows,
            "scripts": scripts(wrapper), "environment": environment(), "source_checks": audit,
            "estimate": candidate, "resources": measured, "open_items": open_items,
            "local_reserve_bytes": args.local_reserve_bytes, "task_budget_bytes": TASK_MAX_BYTES,
            "projected_combined_new_bytes": measured["remote_task_logical_bytes"] + args.local_reserve_bytes
                                            + candidate["remaining_bytes"],
            "per_case_max_wall_s": PER_CASE_MAX_S, "per_case_max_new_bytes": PER_CASE_MAX_BYTES,
            "root_review_required_before_launch": True, "cohort_ready": False, "A_prime_authorized": False}
    dump(output / "plan.json", plan)
    emit(output, plan["status"], plan_sha256=sha(output / "plan.json"),
         estimate=candidate, resources=measured, open_items=open_items,
         projected_combined_new_bytes=plan["projected_combined_new_bytes"])
    return 0 if not open_items else 1


def terminate(process):
    if process is not None and process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)


def run_child(wrapper, output, source, state, save, total_started, total_limit):
    directory = output / "cases" / source["dataset"] / source["opaque_id"]
    directory.parent.mkdir(parents=True, exist_ok=True)
    log_dir = output / "logs" / source["dataset"]
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path, stderr_path = (log_dir / (source["opaque_id"] + suffix) for suffix in (".stdout.txt", ".stderr.txt"))
    command = [sys.executable, "-B", "-X", "utf8", str(SCRIPTS / "replay_microrank_approved_v2.py"),
               "one", source["dataset"], source["opaque_id"], str(directory)]
    process = None
    started = time.perf_counter()
    peak = 0
    import psutil
    try:
        with stdout_path.open("x", encoding="utf-8") as stdout, stderr_path.open("x", encoding="utf-8") as stderr:
            process = subprocess.Popen(command, cwd=BASE, env=os.environ.copy(), stdout=stdout, stderr=stderr,
                                       start_new_session=True)
            state["child_pid"] = process.pid
            save()
            while process.poll() is None:
                if time.perf_counter() - total_started > total_limit:
                    raise BatchError("reviewed overall wall limit exceeded")
                if time.perf_counter() - started > PER_CASE_MAX_S:
                    raise BatchError("child 600 s limit exceeded; no retry/skip")
                count = wrapper.logical_size(directory) + stdout_path.stat().st_size + stderr_path.stat().st_size
                require(count <= PER_CASE_MAX_BYTES, "child/log output exceeded 150 MiB; no retry/skip")
                try:
                    parent = psutil.Process(process.pid)
                    peak = max(peak, sum(p.memory_info().rss for p in [parent] + parent.children(recursive=True)
                                         if p.is_running()))
                except psutil.NoSuchProcess:
                    pass
                time.sleep(POLL_S)
        result = {"exit_code": process.returncode, "elapsed_s": time.perf_counter() - started,
                  "peak_tree_rss_bytes": peak if peak > 0 else None, "logical_bytes": wrapper.logical_size(directory)
                    + stdout_path.stat().st_size + stderr_path.stat().st_size,
                  "pid": process.pid, "command": command,
                  "limits": "Polling can overshoot; cleanup time counted; no filesystem quota promise."}
        dump(log_dir / (source["opaque_id"] + ".process.json"), result)
        return directory, result
    finally:
        error = sys.exc_info()[1]
        terminate(process)
        process_path = log_dir / (source["opaque_id"] + ".process.json")
        if not process_path.exists():
            dump(process_path, {"exit_code": process.poll() if process is not None else None,
                 "elapsed_s": time.perf_counter() - started, "peak_tree_rss_bytes": peak if peak > 0 else None,
                 "logical_bytes": wrapper.logical_size(directory)
                    + sum(path.stat().st_size for path in (stdout_path, stderr_path) if path.is_file()),
                 "pid": process.pid if process is not None else None, "command": command,
                 "operating_failure": str(error) if error is not None else None,
                 "retained": "all partial child files/stdout/stderr; no retry or skip",
                 "limits": "Polling may overshoot; cleanup wall included; no quota promise."})


def failed_row(wrapper, source, directory, error):
    row = initial_rows([source])[0]
    row.update(case_status="FAIL_STOP", classification="blocked", blocked_reasons=[str(error)],
               artifacts={"path": str(directory), "partial_files_retained": True})
    comparison_path = directory / "roundoff-comparison.json"
    if comparison_path.is_file():
        try:
            comparison = read(comparison_path)
            row["record_comparison_classification"] = comparison["classification"]
            row["classification"] = ("service_order_changed"
                                     if comparison["classification"] == "service_order_changed" else "blocked")
            row["numeric_summary"] = comparison["numeric_summary"]
            row["blocked_reasons"].extend(comparison["blocked_reasons"])
            for key in ("max_ulp_distance", "max_relative", "max_relative_exact"):
                row[key] = comparison["numeric_summary"][key]
            row["artifacts"]["approved_comparison_sha256"] = sha(comparison_path)
        except Exception as report_error:
            row["blocked_reasons"].append("partial comparator report: " + str(report_error))
    if (directory / "check.json").is_file():
        row["artifacts"]["check_sha256"] = sha(directory / "check.json")
    return row


def run(args, output, wrapper, replay, comparator, bridge, audit):
    plan_path = run_path(args.plan)
    plan = read(verify(plan_path, args.plan_sha256, audit, "root reviewed plan hash"))
    rows = initial_rows(plan["sources"])
    state = {"schema": SCHEMA, "status": "VALIDATING", "pid": os.getpid(), "started_utc": now(),
             "active": None, "child_pid": None, "plan_sha256": args.plan_sha256,
             "cohort_ready": False, "A_prime_authorized": False, "completed": []}
    started = time.perf_counter()
    def save():
        state["elapsed_s"] = time.perf_counter() - started
        snapshot(output / "status.json", state)
        snapshot(output / "52-cases.json", table(rows, state["status"]))
    save()
    active_source = None
    active_directory = None
    try:
        require(plan["schema"] == SCHEMA and plan["status"] == "PREPARED_NOT_STARTED" and not plan["open_items"],
                "plan remains OPEN/not reviewed preparation")
        require(plan["scripts"] == scripts(wrapper) and plan["environment"] == environment(), "plan scripts/environment changed")
        require(plan["task_budget_bytes"] == TASK_MAX_BYTES and plan["per_case_max_wall_s"] == PER_CASE_MAX_S
                and plan["per_case_max_new_bytes"] == PER_CASE_MAX_BYTES, "plan operating budget changed")
        require(inventory(replay, audit) == plan["sources"], "source inventory changed after plan")
        pilot_rows, open_items = pilots(wrapper, replay, comparator, bridge, plan["pilot_inputs"], audit)
        require(not open_items and serialized(pilot_rows) == plan["pilots"], "pilot source/artifact/benchmark changed after plan")
        require(resources(wrapper)["remote_task_logical_bytes"] + plan["local_reserve_bytes"]
                + plan["estimate"]["remaining_bytes"] < TASK_MAX_BYTES, "projected combined 8 GiB budget exceeded")
        for dataset, pilot in pilot_rows.items():
            index = next(i for i, source in enumerate(plan["sources"]) if
                         (source["dataset"], source["opaque_id"]) == (dataset, pilot["opaque_id"]))
            rows[index] = row_result(plan["sources"][index], pilot["comparison"],
                                     {"pilot_inputs": pilot["binding_inputs"], "pilot_monitors": pilot["monitors"]}, reused=True)
            emit(output, "PILOT_REUSED_PASS", dataset=dataset, opaque_id=pilot["opaque_id"])
        state["status"] = "RUNNING"
        save()
        for index, source in enumerate(plan["sources"]):
            if rows[index]["case_status"] == "PASS":
                continue
            active_source = source
            active_directory = output / "cases" / source["dataset"] / source["opaque_id"]
            state["active"] = {"dataset": source["dataset"], "opaque_id": source["opaque_id"],
                               "source_status": source["source_status"]}
            require(scripts(wrapper) == plan["scripts"], "scripts changed mid-cohort")
            require(time.perf_counter() - started < args.max_wall_s, "overall wall limit reached")
            save()
            emit(output, "CASE_START", **state["active"])
            directory, process = run_child(wrapper, output, source, state, save, started, args.max_wall_s)
            require(process["exit_code"] == 0 and process["elapsed_s"] <= PER_CASE_MAX_S
                    and process["logical_bytes"] <= PER_CASE_MAX_BYTES, "approved child failed operating checks")
            comparison, binding = validate_approved(wrapper, replay, comparator, bridge, directory,
                                                    sha(directory / "check.json"), audit)
            require((comparison["dataset"], comparison["opaque_id"]) == (source["dataset"], source["opaque_id"])
                    and comparison["record_bindings"]["frozen"]["sha256"] == source["entry"]["sha256"],
                    "new case record/frozen identity changed")
            rows[index] = row_result(source, comparison, {**binding, "process": process}, reused=False)
            state["completed"].append({"dataset": source["dataset"], "opaque_id": source["opaque_id"],
                                       "check_sha256": binding["check_sha256"]})
            state["active"] = None
            state["child_pid"] = None
            active_source = None
            active_directory = None
            save()
            emit(output, "CASE_PASS", dataset=source["dataset"], opaque_id=source["opaque_id"],
                 classification=comparison["classification"], numeric_summary=comparison["numeric_summary"])
        require(time.perf_counter() - started <= args.max_wall_s, "reviewed overall wall limit exceeded")
        require(table(rows, "CHECK")["all_case_contracts_passed"] is True, "not all 52 contracts passed")
        state["status"] = "PASS_COHORT_RECORD_CONTRACTS"
        state["all_case_contracts_passed"] = True
        save()
        emit(output, state["status"], denominator=52, new_cases=50, reused_cases=2, cohort_ready=False)
        return 0
    except BaseException as error:
        if active_source is not None:
            index = next(i for i, source in enumerate(plan["sources"]) if
                         (source["dataset"], source["opaque_id"]) == (active_source["dataset"], active_source["opaque_id"]))
            rows[index] = failed_row(wrapper, active_source, active_directory, error)
        state.update(status="FAIL_STOP", error_type=type(error).__name__, error=str(error),
                     all_case_contracts_passed=False, no_retry_no_skip_no_tolerance_increase=True)
        save()
        dump(output / "failure.json", {"state": state, "traceback": traceback.format_exc(),
                                      "remaining_not_run": sum(row["case_status"] == "not_run" for row in rows)})
        emit(output, "FAIL_STOP", error=str(error), active=state["active"])
        return 1
    finally:
        dump(output / "source-checks.json", {"checks": audit})
        save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    for name in ("re2-comparison", "re2-comparison-sha256", "re2-t028", "re2-t028-sha256",
                 "nezha-pilot-run", "nezha-pilot-check-sha256"):
        prepare_parser.add_argument("--" + name, required=True)
    prepare_parser.add_argument("--local-reserve-bytes", required=True, type=int)
    prepare_parser.add_argument("--out", required=True)
    run_parser = commands.add_parser("run")
    run_parser.add_argument("--plan", required=True)
    run_parser.add_argument("--plan-sha256", required=True)
    run_parser.add_argument("--max-wall-s", required=True, type=float)
    run_parser.add_argument("--out", required=True)
    args = parser.parse_args()
    audit = []
    wrapper, replay, comparator, bridge = preflight(audit)
    if args.command == "prepare":
        require(args.local_reserve_bytes >= 0, "negative local reserve")
    else:
        require(math.isfinite(args.max_wall_s) and args.max_wall_s > 0, "invalid reviewed wall budget")
    output = new_output(args.out)
    dump(output / "invocation.json", {"argv": sys.argv, "started_utc": now(), "pid": os.getpid(),
         "script_sha256": sha(__file__), "scripts": scripts(wrapper), "environment": environment(),
         "methods_executed_in_prepare": False, "cohort_ready": False, "A_prime_authorized": False})
    def interrupted(signum, frame):
        raise BatchError("controller received signal " + str(signum))
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    if args.command == "run":
        signal.signal(signal.SIGALRM, interrupted)
        signal.setitimer(signal.ITIMER_REAL, args.max_wall_s)
    try:
        result = (prepare(args, output, wrapper, replay, comparator, bridge, audit) if args.command == "prepare"
                  else run(args, output, wrapper, replay, comparator, bridge, audit))
    except BaseException as error:
        if not (output / "failure.json").exists():
            dump(output / "failure.json", {"status": "FAIL_STOP", "error_type": type(error).__name__,
                 "error": str(error), "traceback": traceback.format_exc(), "source_checks": audit,
                 "cohort_ready": False, "A_prime_authorized": False})
        emit(output, "FAIL_STOP", error=str(error))
        result = 1
    finally:
        if args.command == "run":
            signal.setitimer(signal.ITIMER_REAL, 0)
        files = [{"path": path.relative_to(output).as_posix(), "sha256": sha(path), "bytes": path.stat().st_size}
                 for path in sorted(output.rglob("*")) if path.is_file() and path != output / "manifest.json"]
        dump(output / "manifest.json", {"schema": SCHEMA, "script_sha256": sha(__file__),
                                       "files": files, "cohort_ready": False, "A_prime_authorized": False})
    return result


if __name__ == "__main__":
    raise SystemExit(main())
