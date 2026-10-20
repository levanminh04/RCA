"""T-032: BARO observation fixtures or one exact frozen main/F replay.

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

from capture_baro import BaroCapture
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
        entries = [entry for entry in index["records"] if entry["method"] == "baro"
                   and entry["variant"] == "native" and entry["opaque_id"] == opaque_id]
        authority = I24 + "#/records"
    else:
        entries = [entry for entry in index26["unique_records"] if entry["worker_method"] == "baro"
                   and entry["source_view"] == "main" and entry["opaque_id"] == opaque_id]
        authority = I26 + "#/unique_records"
    if len(entries) != 1:
        raise ReplayError("expected one frozen BARO main/native record")
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
    if any((frozen["opaque_id"] != opaque_id, frozen["method"] != "baro", frozen["variant"] != "native",
            frozen["mode"] != "a", frozen["seed"] is not None, frozen["hashseed"] != 0)):
        raise ReplayError("record outside declared BARO main/native/a/h0 scope")
    if frozen["status"] not in ("OK", "NO_EVIDENCE", "ERROR") or frozen["window"] is None:
        raise ReplayError("source status/window needs a different replay path")
    if os.environ.get("PYTHONHASHSEED") != "0":
        raise ReplayError("launch with PYTHONHASHSEED=0; do not change it after startup")
    return entry, frozen, index26, code_hashes


def external_sources(audit):
    manifest = read(safe_source(M26))
    relative = "results/T-026/runs/session-005/external-code-manifest.json"
    external = read(verify(relative, manifest["files"][relative]["sha256"], M26 + "#/files", audit))
    result = []
    for module_name, suffix in (("RCAEval.e2e.baro", "RCAEval/RCAEval/e2e/baro.py"),
                                ("RCAEval.io.time_series", "RCAEval/RCAEval/io/time_series.py")):
        expected = external["external_source_hashes"]["D:/RCA-ext/src/" + suffix]
        path = Path(importlib.import_module(module_name).__file__).resolve()
        allowed = Path("/home/ubuntu/rca/T-025/src") / suffix
        actual = sha(path)
        row = {"module": module_name, "path": str(path), "expected": expected, "actual": actual,
               "pass": path == allowed.resolve() and actual == expected, "authority": relative}
        audit.append(row)
        if not row["pass"]:
            raise ReplayError("actual imported external source is not frozen: " + module_name)
        result.append(row)
    import numpy as np
    import pandas as pd
    import sklearn
    versions = {"numpy": np.__version__, "pandas": pd.__version__, "sklearn": sklearn.__version__}
    if versions != {"numpy": "1.26.4", "pandas": "2.2.3", "sklearn": "1.6.0"}:
        raise ReplayError("BARO numerical package versions differ from source environment")
    return {"modules": result, "versions": versions}


def verify_baro(directory, summary):
    """Verify bytes, restore tables/arrays, and join native scores to key reconstruction."""
    import numpy as np
    import pandas as pd
    basic = verify_capture(directory, summary)
    serializer = BaroCapture.__new__(BaroCapture)
    serializer.np, serializer.pd = np, pd
    tables, calls = {}, []
    for call in summary["calls"]:
        value = read(directory / call["path"])
        calls.append(value)
        def collect(item):
            if isinstance(item, dict):
                if {"path", "signature", "columns", "index_levels", "rows"} <= set(item):
                    tables[item["path"]] = item
                for child in item.values():
                    collect(child)
            elif isinstance(item, list):
                for child in item:
                    collect(child)
        collect(value)
    checked_tables = []
    for relative, meta in tables.items():
        values = table_columns(directory, meta)
        storage = pd.read_parquet(directory / relative)
        columns = [decode(column["name"]) for column in meta["columns"]]
        indexes = [[decode(json.loads(value)) for value in storage["index_" + str(level)]]
                   for level in range(meta["index_levels"])]
        if meta["index_levels"] != 1 or len(columns) != len(set(columns)):
            raise ReplayError("BARO table restoration requires one index and unique columns")
        rows = ((indexes[0][i], *(values[column][i] for column in columns)) for i in range(meta["rows"]))
        digest, count = serializer._rows_digest(rows)
        if count != meta["signature"]["rows"] or digest != meta["signature"]["ordered_rows_including_index_sha256"]:
            raise ReplayError("restored table not value-exact: " + relative)
        checked_tables.append({"path": relative, "rows": count, "pass": True})
    native = read(directory / "scores-native.json")
    keys = read(directory / "scores-adapter_keys.json")
    # JSON lists let the exact comparison inspect every scalar and float.hex.
    score_differences = exact_differences([[row["column"], row["score"]] for row in native],
                                         [[row["column"], row["score"]] for row in keys])
    if summary["adapter_status"] in ("OK", "NO_EVIDENCE") and score_differences:
        raise ReplayError("observed native and adapter reconstructed keys differ")
    successful_scalers = [call for call in calls if call["function"] == "fit" and call["outcome"] == "return"]
    for call in successful_scalers:
        params = call["scaler"]
        if (params.get("with_centering") is not True or params.get("with_scaling") is not True
                or params.get("unit_variance") is not False or params.get("copy") is not True
                or params.get("quantile_range") != [25.0, 75.0]):
            raise ReplayError("observed RobustScaler parameters differ from native defaults")
        if not np.isfinite(np.asarray(params["center_"] + params["scale_"], dtype=float)).all():
            raise ReplayError("nonfinite fitted center/effective scale")
    return {**basic, "tables_reconstructed": checked_tables, "native_adapter_keys_exact": not score_differences,
            "scalers_checked": len(successful_scalers), "score_count": len(native)}


def one(directory, dataset, opaque_id):
    audit = []
    progress(directory, "SOURCE_CHECK_START", method="baro", dataset=dataset, opaque_id=opaque_id)
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
            job = {"kind": "ranker", "method": "baro", "t": frozen["window"]["t"], "model": None,
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
                   "view": "main", "method": "baro", "trace_guard_s": 0}
            invoke = nezha_worker.main
        dump(directory / "source.json", {"dataset": dataset, "opaque_id": opaque_id, "entry": entry,
             "source_run_id": frozen["run_id"], "source_status": frozen["status"], "external": external,
             "actual_imports": loaded_sources(code_hashes), "allowlist_path": str(allow_path),
             "allowlist_sha256": sha(allow_path), "selected_allowlist_hashes_equal_frozen_inputs": True,
             "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS,
             "reuse": "frozen ranking/status/keys are comparison source; T028 mu/std/votes cannot replace absent native median/IQR/z"})
        dump(directory / "job.json", job)
        progress(directory, "WORKER_START", method="baro", source_status=frozen["status"])
        started = time.perf_counter()
        with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout:
            with (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    with BaroCapture(directory / "capture") as capture:
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
            records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "baro", "a")
            if len(records) != 1:
                raise ReplayError("BARO reconstruction did not return one record")
        else:
            if len(output["ket_qua_nhieu"]) != 1:
                raise ReplayError("BARO worker did not return one result")
            result = output["ket_qua_nhieu"][0]
            record = ban_ghi.tao("baro", VERSIONS["baro"], VARIANTS["baro"], "a", result, output["window"],
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
        capture_check = verify_baro(directory / "capture", summary)
        imports_after = loaded_sources(code_hashes)
        external_sources(audit)
        dump(directory / "source-checks.json", {"checks": audit})
        progress(directory, "FINISHED", status="PASS" if not differences else "FAIL")
        dump(directory / "check.json", {"status": "PASS" if not differences else "FAIL", "method": "baro",
            "dataset": dataset, "opaque_id": opaque_id, "frozen_path": entry["path"], "frozen_sha256": entry["sha256"],
            "frozen_status": frozen["status"], "replay_status": replay["status"],
            "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS, "differences": differences,
            "compare": {"pass": not differences, "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS,
                        "difference_count": len(differences)}, "capture_status": summary["status"], "capture_check": capture_check,
            "actual_imports_after": imports_after, "intermediates_eligible": not differences,
            "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
            "interpretation": "exact replay of one record only; no causal claim; Nezha metric axis is ordinal, consult worker provenance"})
        return 0 if not differences else 1
    finally:
        if not (directory / "source-checks.json").exists():
            dump(directory / "source-checks.json", {"checks": audit})


def fixture_data(name):
    import numpy as np
    import pandas as pd
    time_axis = list(range(95, 105))
    values = [0., 1., 2., 3., 4., 3., 4., 5., 6., 7.]
    if name == "zero_iqr":
        values = [0., 0., 0., 0., 4., 1., 2., 3., 4., 5.]
    elif name == "near_zero_iqr":
        values = [0., 1e-18, 2e-18, 3e-18, 4e-18, 1., 2., 3., 4., 5.]
    elif name == "finiteness":
        values = [np.nan, 1., np.inf, -np.inf, 4., np.nan, 3., np.inf, 5., 6.]
    elif name == "no_evidence":
        values = [1.] * 10
    data = pd.DataFrame({"time": time_axis, "svc_cpu": values})
    if name == "mapping_and_filter":
        data["svc_latency-90"] = values
        data["ts-assurance-mongo_mem"] = np.asarray(values) * 1e6
        data["svc_latency-50"] = np.arange(10)
        data["time.1"] = time_axis
        data["onlyN_cpu"] = [0., 1., 2., 3., 4.] + [1.] * 5
        data["onlyA_cpu"] = [1.] * 5 + [0., 1., 2., 3., 4.]
    return data, (90 if name == "missing_N_error" else 100)


def fixtures(directory):
    import pandas as pd
    from p3 import ban_ghi
    from p3.adapters.baro import chay
    audit = []
    external_sources(audit)
    dump(directory / "source-checks.json", {"checks": audit})
    checks = []
    for name in ("scalar", "zero_iqr", "near_zero_iqr", "finiteness", "mapping_and_filter", "no_evidence", "missing_N_error"):
        case_dir = directory / name
        case_dir.mkdir()
        frame, boundary = fixture_data(name)
        original_frame = frame.copy(deep=True)
        progress(directory, "FIXTURE_START", name=name)
        original = chay(frame, boundary)
        with BaroCapture(case_dir / "capture") as capture:
            observed = chay(frame, boundary)
        summary = capture.require_complete()
        pd.testing.assert_frame_equal(frame, original_frame, check_exact=True)
        original = json.loads(json.dumps(original, allow_nan=False))
        observed = json.loads(json.dumps(observed, allow_nan=False))
        dump(case_dir / "original-adapter.json", original)
        dump(case_dir / "observed-adapter.json", observed)
        differences = exact_differences(original, observed)
        kwargs = {"method": "baro", "method_version": "synthetic fixture only", "variant": "native", "mode": "a",
                  "window": {"t": boundary}, "config_id": "T-032-fixture", "why_ids": [], "hashseed": 0}
        record = ban_ghi.tao(ket_qua=observed, **kwargs)
        differences.extend(exact_differences(ban_ghi.tao(ket_qua=original, **kwargs), record))
        expected_status = "NO_EVIDENCE" if name == "no_evidence" else "ERROR" if name == "missing_N_error" else "OK"
        invariants = {"expected_status": observed["status"] == expected_status}
        scores = read(case_dir / "capture/scores-native.json")
        calls = [read(case_dir / "capture" / call["path"]) for call in summary["calls"]]
        fits = [call for call in calls if call["function"] == "fit" and call["group"] == "native"]
        scales = [call for call in calls if call["function"] == "effective_scale" and call["group"] == "native"]
        if name == "scalar":
            invariants.update(score=scores[0]["score"] == 2.5, center=fits[0]["scaler"]["center_"] == [2.],
                              scale=fits[0]["scaler"]["scale_"] == [2.], max_time=scores[0]["max_adapter_time_markers"] == [104])
        elif name in ("zero_iqr", "near_zero_iqr", "finiteness"):
            raw = scales[0]["entry"]["scale"][0]
            invariants.update(raw_iqr=raw == 0. if name != "near_zero_iqr" else 0. < raw < 1e-15,
                              effective_scale=scales[0]["return"] == [1.], score=scores[0]["score"] == 5.)
        elif name == "mapping_and_filter":
            invariants.update(columns=[row["column"] for row in scores] == ["svc_cpu", "svc_latency", "ts-assurance-mongo_mem"],
                entity_order=[row["entity"] for row in record["entity_ranking"]] == ["svc", "ts-assurance-mongo"],
                ties=[row["tie_group"] for row in record["entity_ranking"]] == [0, 0],
                scores=all(row["score"] == 2.5 for row in scores))
        capture_check = verify_baro(case_dir / "capture", summary)
        check = {"name": name, "expected_status": expected_status, "actual_status": observed["status"],
                 "input_unchanged": True, "differences": differences, "invariants": invariants,
                 "capture_check": capture_check, "pass": not differences and all(invariants.values())}
        dump(case_dir / "check.json", check)
        checks.append(check)
        progress(directory, "FIXTURE_DONE", name=name, status="PASS" if check["pass"] else "FAIL")
        if not check["pass"]:
            dump(directory / "check.json", {"status": "FAIL", "fixtures": checks})
            return 1
    dump(directory / "check.json", {"status": "PASS", "fixtures": checks,
        "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
        "limits": "synthetic observer/preprocessing/scale/mapping checks; no frozen real-data replay or causal conclusion"})
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
            ("capture_baro.py", "replay_baro.py", "capture_microrank.py", "replay_microrank.py")},
        "python": sys.version, "hashseed": os.environ.get("PYTHONHASHSEED"), "source_repo": str(REPO)})
    try:
        return fixtures(directory) if args.command == "fixture" else one(directory, args.dataset, args.opaque_id)
    except Exception as error:
        failure = {"status": "FAIL", "method": "baro", "type": type(error).__name__, "error": str(error),
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
