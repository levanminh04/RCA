"""T-032: TraceRCA observation fixtures or one exact frozen main/F replay.

CLI: ``fixture <new_run_dir>`` or ``one RE2-TT|Nezha-OB <opaque_id> <new_run_dir>``.
Use the approved EC2 interpreter/PYTHONPATH and PYTHONHASHSEED=0. No laptop
research, altered source, intervention, numerical tolerance or source overwrite.
Shared serialization/comparison helpers are imported from replay_microrank;
its method runner is never called. A PASS does not imply a causal conclusion.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import sys
import time
import traceback

from capture_tracerca import TraceRcaCapture
from replay_microrank import (
    REPO, RE2_RAW_REPO, M24, I24, M26, I26, EXACT_FIELDS, EXCLUDED_FIELDS,
    ReplayError, now, sha, read, dump, safe_source, new_directory, progress,
    verify, verified_index26, loaded_sources, literal_constants, exact_differences,
    compare_records, decode, table_columns, verify_capture, measured_cost, artifact_manifest,
)


def source_for(dataset, opaque_id, audit):
    if not re.fullmatch(r"dev-[0-9a-f]{10}", opaque_id):
        raise ReplayError("invalid opaque dev ID")
    index26 = verified_index26(audit)
    if dataset == "RE2-TT":
        manifest = read(safe_source(M24))
        index = read(verify(I24, manifest["source_hashes"][I24], M24 + "#/source_hashes", audit))
        entries = [entry for entry in index["records"] if entry["method"] == "tracerca"
                   and entry["variant"] == "native" and entry["opaque_id"] == opaque_id]
        authority = I24 + "#/records"
    else:
        entries = [entry for entry in index26["unique_records"] if entry["worker_method"] == "tracerca"
                   and entry["source_view"] == "main" and entry["opaque_id"] == opaque_id]
        authority = I26 + "#/unique_records"
    if len(entries) != 1:
        raise ReplayError("expected one frozen TraceRCA main record with its original dataset variant")
    entry = entries[0]
    frozen = read(verify(entry["path"], entry["sha256"], authority, audit))
    if dataset == "RE2-TT":
        direct = manifest["source_hashes"].get(entry["path"])
        if direct is not None and direct != entry["sha256"]:
            raise ReplayError("direct T-029 record hash contradicts verified T-024 index")
        config = read(verify(entry["source_config"], entry["source_config_sha256"], authority, audit))
        code_hashes = config["src_p3"]["tep"]
    else:
        code_hashes = {path: value for path, value in index26["source_hashes"].items()
                       if path.startswith("src/p3/") and path.endswith(".py")}
    for path, expected in sorted(code_hashes.items()):
        verify(path, expected, "frozen configuration / " + I26 + "#/source_hashes", audit)
    expected_variant = "native" if dataset == "RE2-TT" else "finite"
    if any((frozen["opaque_id"] != opaque_id, frozen["method"] != "tracerca", frozen["variant"] != expected_variant,
            frozen["mode"] != "a", frozen["seed"] is not None, frozen["hashseed"] != 0)):
        raise ReplayError("record outside declared TraceRCA main/a/h0 scope or wrong dataset variant")
    if frozen["status"] not in ("OK", "NO_EVIDENCE", "ERROR") or frozen["window"] is None:
        raise ReplayError("source status/window needs a different replay path")
    if os.environ.get("PYTHONHASHSEED") != "0":
        raise ReplayError("launch with PYTHONHASHSEED=0; do not change it after startup")
    return entry, frozen, index26, code_hashes



LOWERCASE_PARENT = Path("/home/ubuntu/rca/T-032/sources/rcaeval")
LOWERCASE_INVENTORY = Path("/home/ubuntu/rca/T-032/sources/tracerca-path-002-inventory.json")
LOWERCASE_INVENTORY_SHA256 = "c07cbd357b860d164a8d4eef0177015e8620928107192a2b98301e79b3ad0bd5"
LOWERCASE_REVISION = "259ea4167160256a74ad30004aa3d96a998c846e"


def lowercase_file(path, expected, authority, audit):
    path = Path(path)
    task_sources = Path("/home/ubuntu/rca/T-032/sources")
    if task_sources not in path.parents or path.resolve() != path or path.is_symlink():
        raise ReplayError("lowercase code/metadata escaped or redirected")
    actual = sha(path)
    audit.append({"path": str(path), "authority": authority, "expected": expected,
                  "actual": actual, "pass": actual == expected, "bytes": path.stat().st_size})
    if actual != expected:
        raise ReplayError("lowercase source/metadata hash differs: " + str(path))
    return path


def lowercase_closure(audit):
    metadata = read(lowercase_file(LOWERCASE_INVENTORY, LOWERCASE_INVENTORY_SHA256,
                                  "approved byte-identical TraceRCA lowercase closure", audit))
    if metadata.get("revision") != LOWERCASE_REVISION or metadata.get("remote_parent") != str(LOWERCASE_PARENT):
        raise ReplayError("lowercase closure revision/root changed")
    if LOWERCASE_PARENT.resolve() != LOWERCASE_PARENT or LOWERCASE_PARENT.is_symlink():
        raise ReplayError("lowercase closure root redirected")
    rows = metadata["files"]
    if len(rows) != metadata["file_count"] or sum(row["bytes"] for row in rows) != metadata["total_bytes"]:
        raise ReplayError("lowercase closure inventory count/size changed")
    if metadata["total_bytes"] > 5 * 1024 * 1024:
        raise ReplayError("lowercase closure exceeds approved 5 MiB")
    expected_modules = {}
    for row in rows:
        relative = Path(row["package_relative"])
        if (relative.is_absolute() or ".." in relative.parts or relative.parts[0] != "RCAEval"
                or relative.suffix != ".py" or row["module"] in expected_modules):
            raise ReplayError("invalid/duplicate lowercase closure row")
        path = LOWERCASE_PARENT / relative
        if path.resolve() != path or path.is_symlink():
            raise ReplayError("lowercase code redirected: " + str(path))
        lowercase_file(path, row["sha256"], "RCAEval@" + LOWERCASE_REVISION + ":" + relative.as_posix(), audit)
        if path.stat().st_size != row["bytes"]:
            raise ReplayError("lowercase source byte size differs")
        expected_modules[row["module"]] = row
    for name, module in sorted(sys.modules.items()):
        if name != "RCAEval" and not name.startswith("RCAEval."):
            continue
        row = expected_modules.get(name)
        imported_file = getattr(module, "__file__", None)
        if row is None or imported_file is None:
            raise ReplayError("unknown/namespace RCAEval import: " + name)
        path = Path(imported_file).resolve()
        allowed = LOWERCASE_PARENT / row["package_relative"]
        if path != allowed or sha(path) != row["sha256"]:
            raise ReplayError("RCAEval import fell back or changed: " + name)
        audit.append({"module": name, "path": str(path), "expected": row["sha256"],
                      "actual": sha(path), "pass": True, "authority": "lowercase closure actual import"})
    return metadata


def external_sources(audit):
    manifest = read(safe_source(M26))
    relative = "results/T-026/runs/session-005/external-code-manifest.json"
    external = read(verify(relative, manifest["files"][relative]["sha256"], M26 + "#/files", audit))
    suffix = "RCAEval/RCAEval/e2e/tracerca.py"
    module_name = "RCAEval.e2e.tracerca"
    expected = external["external_source_hashes"]["D:/RCA-ext/src/" + suffix]
    closure = lowercase_closure(audit)
    path = Path(importlib.import_module(module_name).__file__).resolve()
    lowercase_closure(audit)
    allowed = LOWERCASE_PARENT / "RCAEval/e2e/tracerca.py"
    actual = sha(path)
    row = {"module": module_name, "path": str(path), "expected": expected, "actual": actual,
           "pass": path == allowed.resolve() and actual == expected, "authority": relative}
    audit.append(row)
    if not row["pass"]:
        raise ReplayError("actual imported external source is not frozen: " + module_name)
    import numpy as np
    import pandas as pd
    versions = {"numpy": np.__version__, "pandas": pd.__version__}
    if versions != {"numpy": "1.26.4", "pandas": "2.2.3"}:
        raise ReplayError("TraceRCA numerical package versions differ from source environment")
    return {"modules": [row], "versions": versions, "closure_inventory_sha256": LOWERCASE_INVENTORY_SHA256,
            "closure_count": closure["file_count"], "closure_revision": LOWERCASE_REVISION}

def verify_tracerca(directory, summary):
    """Restore observed rows, verify native formulas/filter, and retain ERROR state.

    Recomputed count operands are diagnostics from captured flags. SLO and ji
    evidence are actual native locals; this check never calls a method function.
    """
    import numpy as np
    import pandas as pd
    basic = verify_capture(directory, summary)
    if not summary["trace_restored"] or not summary["profile_restored"]:
        raise ReplayError("observer/adapter did not restore original hooks")
    serializer = TraceRcaCapture.__new__(TraceRcaCapture)
    serializer.np, serializer.pd = np, pd
    calls = [read(directory / call["path"]) for call in summary["calls"]]
    tables = {}

    def collect(value):
        if isinstance(value, dict):
            if {"path", "signature", "columns", "index_levels", "rows"} <= set(value):
                previous = tables.get(value["path"])
                if previous is not None and previous != value:
                    raise ReplayError("conflicting table metadata")
                tables[value["path"]] = value
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    for call in calls:
        collect(call)
    restored, checked_tables = {}, []
    for relative, meta in tables.items():
        values = table_columns(directory, meta)
        storage = pd.read_parquet(directory / relative)
        columns = [decode(column["name"]) for column in meta["columns"]]
        if meta["index_levels"] != 1 or len(columns) != len(set(columns)):
            raise ReplayError("TraceRCA table requires one index and unique columns")
        indexes = [decode(json.loads(value)) for value in storage["index_0"]]
        frame = pd.DataFrame({column: values[column] for column in columns})
        frame.index = pd.Index(indexes, name=decode(meta["index_names"])[0])
        frame.columns.name = decode(meta["columns_name"])
        differences = exact_differences(meta["signature"], serializer._table_signature(frame))
        if differences:
            raise ReplayError("restored table is not value/type/order-exact: " + relative + " " + repr(differences[:3]))
        restored[relative] = frame
        checked_tables.append({"path": relative, "rows": len(frame), "pass": True})
    native = next(call for call in calls if call["function"] == "native")
    adapter = next(call for call in calls if call["function"] == "adapter")
    slo_call = next(call for call in calls if call["function"] == "operation_slo")
    adapter_threw = adapter["outcome"] == "exception" and bool(adapter["exceptions"])
    adapter_exception = ({key: adapter["exceptions"][-1][key] for key in ("type", "message")}
                         if adapter_threw else None)
    returned_status = adapter["return"].get("status") if isinstance(adapter["return"], dict) else None
    if (summary["adapter_outcome"] != adapter["outcome"] or summary["adapter_threw"] != adapter_threw
            or summary["adapter_exception"] != adapter_exception
            or summary["adapter_returned_status"] != returned_status
            or summary["adapter_status"] != ("ERROR" if adapter_threw else returned_status)
            or summary["adapter_status_source"] != ("observed_adapter_exception" if adapter_threw else "adapter_return")):
        raise ReplayError("adapter summary does not preserve actual return/exception outcome")
    original = restored[adapter["entry"]["input"]["path"]]
    after = restored[native["native_input_after"]["path"]]
    if exact_differences(adapter["entry"]["input"]["signature"], native["entry"]["input_signature"]):
        raise ReplayError("native entry differs from original adapter input")
    if exact_differences(adapter["entry"]["input"]["signature"], adapter["input_after_signature"]):
        raise ReplayError("original adapter input changed")
    expected_after = original.copy(deep=True)
    expected_after["methodName"] = expected_after["methodName"].fillna(expected_after["operationName"])
    expected_after["operation"] = expected_after["serviceName"] + "_" + expected_after["methodName"]
    pd.testing.assert_frame_equal(after, expected_after, check_exact=True)
    partition = native["partition_positions"]
    normal = restored[native["tables"]["normal_df"]["path"]]
    anomalous = restored[native["tables"]["anomal_df"]["path"]]
    boundary = decode(native["entry"]["inject_time_us"])
    ends = after["startTime"] + after["duration"]
    wanted_positions = {"normal_df": np.flatnonzero((ends < boundary).to_numpy()).tolist(),
                        "anomal_df": np.flatnonzero((ends >= boundary).to_numpy()).tolist()}
    for name, positions in wanted_positions.items():
        if partition[name] != positions:
            raise ReplayError("native partition positions mismatch: " + name)
        frame = normal if name == "normal_df" else anomalous
        pd.testing.assert_frame_equal(frame[list(after.columns)], after.iloc[positions], check_exact=True)
    slo = {op: {"mean": round(normal[normal["operation"] == op]["duration"].mean() / 1000, 2),
                "std": round(normal[normal["operation"] == op]["duration"].std() / 1000, 2)}
           for op in normal["operation"].dropna().unique()}
    if (exact_differences(serializer._encode(slo), native.get("normal_slo"))
            or exact_differences(serializer._encode(slo), slo_call["return"])
            or exact_differences(serializer._encode(list(slo.items())), slo_call["ordered_slo"])):
        raise ReplayError("native SLO does not match restored normal Series mean/std/built-in round")
    formula_checked = False
    if native["outcome"] == "return":
        operations = list(anomalous.operation.unique())
        if native["operations"] != serializer._encode(operations):
            raise ReplayError("native operation order differs from A row order")
        expected_mean = anomalous["operation"].apply(lambda op: slo[op]["mean"])
        expected_std = anomalous["operation"].apply(lambda op: slo[op]["std"])
        pd.testing.assert_series_equal(anomalous["mean"], expected_mean.rename("mean"), check_exact=True)
        pd.testing.assert_series_equal(anomalous["std"], expected_std.rename("std"), check_exact=True)
        expected_flags = anomalous["duration"] / 1000 >= anomalous["mean"] + 3 * anomalous["std"]
        pd.testing.assert_series_equal(anomalous["abnormal"], expected_flags.rename("abnormal"), check_exact=True)
        total = anomalous["abnormal"].sum()
        support, confidence, ji = {}, {}, {}
        operands = []
        for op in operations:
            selected = anomalous[anomalous["operation"] == op]
            flags = selected["abnormal"].sum()
            count = selected["operation"].count()
            support[op] = flags / total
            confidence[op] = flags / count
            operands.append({"operation": serializer._encode(op), "abnormal_spans_A": int(flags),
                             "operation_spans_A": int(count)})
        for op in operations:
            ji[op] = 2 * support[op] * confidence[op] / (support[op] + confidence[op])
        for name, value in (("support_dict", support), ("confidence_dict", confidence), ("ji_dict", ji)):
            if (exact_differences(serializer._encode(value), native[name])
                    or exact_differences(serializer._encode(list(value.items())), native["ordered_mappings"][name])):
                raise ReplayError("native " + name + " differs from exact restored pandas count operands")
        observed_operands = native["count_operands_from_observed_flags"]
        if observed_operands["total_abnormal_spans_A"] != int(total) or observed_operands["operations"] != operands:
            raise ReplayError("captured span count operands differ from restored flags")
        official = [op for op, score in sorted(ji.items(), key=lambda row: row[1], reverse=True) if not np.isnan(score)]
        native_return = read(directory / "native-result.json")
        if native_return["ranks"] != official:
            raise ReplayError("native return differs from its original sort-then-NaN-filter path")
        finite = sorted([(op, float(value)) for op, value in ji.items() if np.isfinite(float(value))],
                        key=lambda row: row[1], reverse=True)
        if returned_status in ("OK", "NO_EVIDENCE"):
            if adapter["return"]["ranking_native"] != [op for op, _ in finite]:
                raise ReplayError("adapter finite ranking differs from native ji finite filter")
            if exact_differences(adapter["locals"]["huu_han"], serializer._encode(finite)):
                raise ReplayError("adapter keys differ from native ji")
        formula_checked = True
    else:
        if not native["exceptions"] or not (adapter_threw or returned_status == "ERROR"):
            raise ReplayError("unwound native call did not preserve native exception and adapter return/exception")
    return {**basic, "tables_reconstructed": checked_tables, "hooks_restored": True,
            "native_mutation_preserved": True, "adapter_input_unchanged": True,
            "partition_restored": True, "native_slo_exact": True,
            "native_count_and_score_formulas_exact": formula_checked,
            "native_outcome": native["outcome"], "adapter_status": summary["adapter_status"],
            "adapter_outcome": adapter["outcome"], "adapter_threw": adapter_threw,
            "adapter_exception": adapter_exception, "adapter_status_source": summary["adapter_status_source"]}

def one(directory, dataset, opaque_id):
    audit = []
    progress(directory, "SOURCE_CHECK_START", method="tracerca", dataset=dataset, opaque_id=opaque_id)
    try:
        entry, frozen, index26, code_hashes = source_for(dataset, opaque_id, audit)
        from p3 import ban_ghi, runner, selector, worker
        external = external_sources(audit)
        if dataset == "RE2-TT":
            allow_path = safe_source("results/T-022/allowlist-dev.json")
            allow = selector.nap_allowlist(allow_path)
            wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
            if wanted != frozen["input_sha256"]:
                raise ReplayError("selected allowlist hashes differ from frozen inputs")
            files = selector.chon_ca(allow, opaque_id, RE2_RAW_REPO, kiem_hash=True)
            job = {"kind": "ranker", "method": "tracerca", "t": frozen["window"]["t"], "model": None,
                   "files": {name: {"path": path, "sha256": wanted[name]} for name, path in files.items()}}
            invoke = worker.main
        else:
            from p3 import nezha, nezha_worker
            from p3.adapters.nezha import VARIANTS, VERSIONS
            allow_relative = "results/T-026/allowlist-dev.json"
            allow_path = verify(allow_relative, index26["source_hashes"][allow_relative], I26 + "#/source_hashes", audit)
            allow = nezha.nap_allowlist(allow_path)
            wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items()}
            if wanted != frozen["input_sha256"] or entry["trace_guard_s"] != 0:
                raise ReplayError("Nezha input hashes/main guard differ from source")
            script = "results/T-026/scripts/run_pilot.py" if entry["reused_pilot"] else "results/T-026/scripts/run.py"
            constants = literal_constants(verify(script, index26["source_hashes"][script], I26 + "#/source_hashes", audit))
            job = {"allowlist_path": str(allow_path), "opaque_id": opaque_id, "repo_root": str(REPO),
                   "view": "main", "method": "tracerca", "trace_guard_s": 0}
            invoke = nezha_worker.main
        dump(directory / "source.json", {"dataset": dataset, "opaque_id": opaque_id, "entry": entry,
             "source_run_id": frozen["run_id"], "source_status": frozen["status"], "external": external,
             "actual_imports": loaded_sources(code_hashes), "allowlist_path": str(allow_path),
             "allowlist_sha256": sha(allow_path), "selected_allowlist_hashes_equal_frozen_inputs": True,
             "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS,
             "reuse": "frozen ranking/status/keys are comparison source; T028 aggregate counts cannot replace absent native SLO/flags/support/confidence/ji"})
        dump(directory / "job.json", job)
        progress(directory, "WORKER_START", method="tracerca", source_status=frozen["status"])
        started = time.perf_counter()
        with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout:
            with (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    with TraceRcaCapture(directory / "capture") as capture:
                        invoke(str(directory / "job.json"), str(directory / "ket-qua.json"))
        summary = capture.require_complete()
        cost = measured_cost(started, 0)
        dump(directory / "cost.json", cost)
        output = read(directory / "ket-qua.json")
        if output.get("hashseed") != "0":
            raise ReplayError("worker reported wrong hashseed")
        if dataset == "RE2-TT":
            base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None,
                    "hashseed": 0, "detector": None, "detector_columns": None, "config_id": "p3-re2tt-v2"}
            records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "tracerca", "a")
            if len(records) != 1:
                raise ReplayError("TraceRCA reconstruction did not return one record")
        else:
            if len(output["ket_qua_nhieu"]) != 1:
                raise ReplayError("TraceRCA worker did not return one result")
            result = output["ket_qua_nhieu"][0]
            record = ban_ghi.tao("tracerca", VERSIONS["tracerca"], VARIANTS["tracerca"], "a", result, output["window"],
                constants["CONFIG"], constants["WHY"], seed=None, hashseed=0, run_id=directory.name, opaque_id=opaque_id)
            record["cost"] = {**cost, "buoc_s": output.get("buoc_s", {})}
            record["input_sha256"] = output["input_sha256"]
            if entry["reused_pilot"]:
                record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
            else:
                record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
            ban_ghi.kiem(record)
            dump(directory / "ban-ghi-0.json", record)
        replay = read(directory / "ban-ghi-0.json")
        differences = compare_records(frozen, replay)
        progress(directory, "FROZEN_COMPARE_DONE", match=not differences)
        capture_check = verify_tracerca(directory / "capture", summary)
        imports_after = loaded_sources(code_hashes)
        external_sources(audit)
        dump(directory / "source-checks.json", {"checks": audit})
        progress(directory, "FINISHED", status="PASS" if not differences else "FAIL")
        dump(directory / "check.json", {"status": "PASS" if not differences else "FAIL", "method": "tracerca",
            "dataset": dataset, "opaque_id": opaque_id, "frozen_path": entry["path"], "frozen_sha256": entry["sha256"],
            "frozen_status": frozen["status"], "replay_status": replay["status"],
            "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS, "differences": differences,
            "compare": {"pass": not differences, "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS,
                        "difference_count": len(differences)}, "capture_status": summary["status"], "capture_check": capture_check,
            "actual_imports_after": imports_after, "intermediates_eligible": not differences,
            "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
            "interpretation": "exact replay of one TraceRCA record only; counts are native span counts; no causal or wait-semantics claim"})
        return 0 if not differences else 1
    finally:
        if not (directory / "source-checks.json").exists():
            dump(directory / "source-checks.json", {"checks": audit})


def fixture_data(name):
    import pandas as pd
    rows = []
    for service, durations in (("alpha", (1000, 2000, 3000)), ("beta", (2000, 2000, 2000))):
        if name == "single_baseline_std_nan" and service == "alpha":
            durations = (1000,)
        for duration in durations:
            rows.append((service, None, "work", 90_000_000, duration))
    for service, durations in (("alpha", (6000, 1000)), ("beta", (2000, 1000))):
        if name == "zero_abnormal" or name == "zero_support" and service == "beta":
            durations = (1000, 1000)
        for duration in durations:
            rows.append((service, None, "work", 100_000_000, duration))
    if name == "new_operation_error":
        rows.append(("new", None, "work", 100_000_000, 2000))
    if name == "mapping_collision_error":
        rows = [(service, method, method, start, duration)
                for service, method in (("a_b", "c"), ("a", "b_c"))
                for start, duration in ((90_000_000, 1000), (91_000_000, 1000), (100_000_000, 2000))]
    frame = pd.DataFrame(rows, columns=("serviceName", "methodName", "operationName", "startTime", "duration"))
    # Duplicate IDs demonstrate that native counts are rows, not unique traces.
    frame["traceID"] = "one-shared-trace"
    frame["spanID"] = [str(i) for i in range(len(frame))]
    frame["parentSpanID"] = ""
    return frame, 100


def fixtures(directory):
    import pandas as pd
    from p3 import ban_ghi
    from p3.adapters.tracerca import chay
    audit = []
    external_sources(audit)
    dump(directory / "source-checks.json", {"checks": audit})
    checks = []
    for name in ("scalar", "zero_support", "zero_abnormal", "single_baseline_std_nan", "new_operation_error", "mapping_collision_error"):
        case_dir = directory / name
        case_dir.mkdir()
        frame, boundary = fixture_data(name)
        original_frame = frame.copy(deep=True)
        progress(directory, "FIXTURE_START", name=name)
        prior_trace, prior_profile = sys.gettrace(), sys.getprofile()
        # A pre-existing profile hook must survive both the adapter's own
        # profile hook and this observer; it is never used as an oracle.
        def existing_profile(_frame, _event, _arg):
            return None
        sys.setprofile(existing_profile)
        original = observed = None
        original_exception = observed_exception = None
        try:
            try:
                original = chay(frame, boundary)
            except Exception as error:
                original_exception = {"type": type(error).__name__, "message": str(error)}
            try:
                with TraceRcaCapture(case_dir / "capture") as capture:
                    observed = chay(frame, boundary)
            except Exception as error:
                observed_exception = {"type": type(error).__name__, "message": str(error)}
            existing_profile_preserved = sys.getprofile() is existing_profile
        finally:
            sys.setprofile(prior_profile)
        summary = capture.require_complete()
        pd.testing.assert_frame_equal(frame, original_frame, check_exact=True)
        original = json.loads(json.dumps(original, allow_nan=False))
        observed = json.loads(json.dumps(observed, allow_nan=False))
        original_outcome = {"outcome": "exception" if original_exception else "return",
                            "return": original, "exception": original_exception}
        observed_outcome = {"outcome": "exception" if observed_exception else "return",
                            "return": observed, "exception": observed_exception}
        dump(case_dir / "original-adapter.json", original_outcome)
        dump(case_dir / "observed-adapter.json", observed_outcome)
        differences = exact_differences(original_outcome, observed_outcome)
        kwargs = {"method": "tracerca", "method_version": "synthetic fixture only", "variant": "finite", "mode": "a",
                  "window": {"t": boundary}, "config_id": "T-032-fixture", "why_ids": [], "hashseed": 0}
        record = None
        if original_exception is None and observed_exception is None:
            record = ban_ghi.tao(ket_qua=observed, **kwargs)
            differences.extend(exact_differences(ban_ghi.tao(ket_qua=original, **kwargs), record))
        observed_status = "ERROR" if observed_exception else observed["status"]
        expected_status = "NO_EVIDENCE" if name == "zero_abnormal" else "ERROR" if name.endswith("error") else "OK"
        invariants = {"expected_status": observed_status == expected_status,
                      "adapter_outcome_preserved": summary["adapter_outcome"] == observed_outcome["outcome"],
                      "adapter_exception_preserved": summary["adapter_exception"] == observed_exception,
                      "adapter_status_preserved": summary["adapter_status"] == observed_status,
                      "trace_restored": sys.gettrace() is prior_trace,
                      "profile_restored": sys.getprofile() is prior_profile,
                      "existing_profile_preserved": existing_profile_preserved}
        calls = [read(case_dir / "capture" / call["path"]) for call in summary["calls"]]
        native = next(call for call in calls if call["function"] == "native")
        if name == "scalar":
            counts = native["count_operands_from_observed_flags"]
            invariants.update(span_count_total=counts["total_abnormal_spans_A"] == 2,
                equal_support=native["support_dict"] == {"alpha_work": 0.5, "beta_work": 0.5},
                equal_confidence=native["confidence_dict"] == {"alpha_work": 0.5, "beta_work": 0.5},
                equal_ji=native["ji_dict"] == {"alpha_work": 0.5, "beta_work": 0.5},
                tied_keys=[row["key"] for row in record["entity_ranking"]] == [[0.5], [0.5]])
        elif name == "zero_support":
            invariants.update(nonfinite_operation=native["ji_dict"]["beta_work"] == {"__nonfinite__": "NaN"},
                              finite_ranking=observed["ranking_native"] == ["alpha_work"])
        elif name == "zero_abnormal":
            invariants.update(zero_count=native["count_operands_from_observed_flags"]["total_abnormal_spans_A"] == 0,
                              empty_finite_ranking=observed["ranking_native"] == [])
        elif name == "single_baseline_std_nan":
            invariants.update(std_nan=native["normal_slo"]["alpha_work"]["std"] == {"__nonfinite__": "NaN"},
                              nan_baseline_filtered="alpha_work" not in observed["ranking_native"])
        elif name == "new_operation_error":
            invariants.update(native_exception=native["outcome"] == "exception",
                              key_error=any(exc["type"] == "KeyError" for exc in native["exceptions"]))
        elif name == "mapping_collision_error":
            error_message = observed_exception["message"] if observed_exception else observed["error"]
            invariants.update(native_returned=native["outcome"] == "return", ambiguous_error="operation" in error_message)
        capture_check = verify_tracerca(case_dir / "capture", summary)
        check = {"name": name, "expected_status": expected_status, "actual_status": observed_status,
                 "status_source": "observed_adapter_exception" if observed_exception else "adapter_return",
                 "original_adapter_outcome": original_outcome["outcome"],
                 "observed_adapter_outcome": observed_outcome["outcome"],
                 "original_adapter_exception": original_exception, "observed_adapter_exception": observed_exception,
                 "input_unchanged": True, "differences": differences, "invariants": invariants,
                 "capture_check": capture_check, "pass": not differences and all(invariants.values())}
        dump(case_dir / "check.json", check)
        checks.append(check)
        progress(directory, "FIXTURE_DONE", name=name, status="PASS" if check["pass"] else "FAIL")
        if not check["pass"]:
            dump(directory / "check.json", {"status": "FAIL", "fixtures": checks,
                 "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"]})
            return 1
    dump(directory / "check.json", {"status": "PASS", "fixtures": checks,
        "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
        "limits": "synthetic observer/count/filter/mutation/error checks; no real frozen replay or mechanism claim"})
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    fixture = commands.add_parser("fixture")
    fixture.add_argument("new_run_dir")
    single = commands.add_parser("one")
    single.add_argument("dataset", choices=("RE2-TT", "Nezha-OB"))
    single.add_argument("opaque_id")
    single.add_argument("new_run_dir")
    args = parser.parse_args()
    directory = new_directory(args.new_run_dir)
    dump(directory / "invocation.json", {"at_utc": now(), "argv": sys.argv, "command": args.command,
        "scripts": {name: sha(Path(__file__).with_name(name)) for name in
            ("capture_tracerca.py", "replay_tracerca_v2.py", "capture_microrank.py", "replay_microrank.py")},
        "python": sys.version, "hashseed": os.environ.get("PYTHONHASHSEED"), "source_repo": str(REPO)})
    try:
        return fixtures(directory) if args.command == "fixture" else one(directory, args.dataset, args.opaque_id)
    except Exception as error:
        failure = {"status": "FAIL", "method": "tracerca", "type": type(error).__name__, "error": str(error),
            "traceback": traceback.format_exc(), "intermediates_eligible": False,
            "retained": "all partial artifacts remain; no automatic retry/fallback"}
        if args.command == "one":
            failure.update(dataset=args.dataset, opaque_id=args.opaque_id)
        dump(directory / ("failure-after-check.json" if (directory / "check.json").exists() else "check.json"), failure)
        progress(directory, "FAILED", error=str(error))
        return 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
