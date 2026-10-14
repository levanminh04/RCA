"""T-032: SimpleRCA fixtures or one exact frozen main/F replay on approved EC2.

Verifier v4 restores pandas logical extension dtypes; native/source/exact comparison unchanged. CLI: fixture <new_run_dir> or one RE2-TT|Nezha-OB <opaque_id> <new_run_dir>.
No laptop method run, new source/configuration, tolerance, labels or fallback.
T028 totals remain reusable; this observer adds missing native/channel evidence.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import importlib
import json
import os
from pathlib import Path
import re
import sys
import time
import traceback

from capture_simplerca import SimpleRcaCapture
from replay_microrank import (
    REPO, RE2_RAW_REPO, M24, I24, M26, I26, EXACT_FIELDS, EXCLUDED_FIELDS,
    ReplayError, now, sha, read, dump, safe_source, new_directory, progress,
    verify, verified_index26, loaded_sources, literal_constants, exact_differences,
    compare_records, decode, table_columns, verify_capture, measured_cost, artifact_manifest,
)


from audit_simplerca_output_v3 import table_columns


def source_for(dataset, opaque_id, audit):
    if not re.fullmatch(r"dev-[0-9a-f]{10}", opaque_id):
        raise ReplayError("invalid opaque dev ID")
    index26 = verified_index26(audit)
    if dataset == "RE2-TT":
        manifest = read(safe_source(M24))
        index = read(verify(I24, manifest["source_hashes"][I24], M24 + "#/source_hashes", audit))
        entries = [entry for entry in index["records"] if entry["method"] == "simplerca"
                   and entry["variant"] == "native" and entry["opaque_id"] == opaque_id]
        authority = I24 + "#/records"
    else:
        entries = [entry for entry in index26["unique_records"] if entry["worker_method"] == "simplerca"
                   and entry["source_view"] == "main" and entry["opaque_id"] == opaque_id]
        authority = I26 + "#/unique_records"
    if len(entries) != 1:
        raise ReplayError("expected one frozen SimpleRCA main record")
    entry = entries[0]
    frozen = read(verify(entry["path"], entry["sha256"], authority, audit))
    if dataset == "RE2-TT":
        direct = manifest["source_hashes"].get(entry["path"])
        if direct is not None and direct != entry["sha256"]:
            raise ReplayError("direct T-029 record hash contradicts verified T-024 index")
        config = read(verify(entry["source_config"], entry["source_config_sha256"], authority, audit))
        code_hashes = dict(config["src_p3"]["tep"])
    else:
        code_hashes = {path: value for path, value in index26["source_hashes"].items()
                       if path.startswith("src/p3/") and path.endswith(".py")}
    for path, value in index26["source_hashes"].items():
        if path.startswith("src/simplerca/") and path.endswith(".py") and "/tests/" not in path:
            if path in code_hashes and code_hashes[path] != value:
                raise ReplayError("frozen source authorities disagree for " + path)
            code_hashes[path] = value
    for path, expected in sorted(code_hashes.items()):
        verify(path, expected, "frozen configuration / " + I26 + "#/source_hashes", audit)
    expected_variant = "native" if dataset == "RE2-TT" else "M4"
    if any((frozen["opaque_id"] != opaque_id, frozen["method"] != "simplerca", frozen["variant"] != expected_variant,
            frozen["mode"] != "a", frozen["seed"] is not None, frozen["hashseed"] != 0)):
        raise ReplayError("record outside declared SimpleRCA main/a/h0 scope")
    if frozen["status"] not in ("OK", "NO_EVIDENCE", "ERROR", "UNSUPPORTED"):
        raise ReplayError("unrecognized frozen status; retain source without invoking a new path")
    if frozen["window"] is None and frozen["status"] != "UNSUPPORTED":
        raise ReplayError("source has no replayable window")
    if os.environ.get("PYTHONHASHSEED") != "0":
        raise ReplayError("launch with PYTHONHASHSEED=0; do not change it after startup")
    return entry, frozen, index26, code_hashes


def loaded_simple_sources(code_hashes):
    result = loaded_sources(code_hashes)
    for name, module in sorted(sys.modules.copy().items()):
        if name != "simplerca" and not name.startswith("simplerca."):
            continue
        path = Path(module.__file__).resolve()
        try:
            relative = path.relative_to(REPO.resolve()).as_posix()
        except ValueError as error:
            raise ReplayError("SimpleRCA import resolved outside copied source repository: " + name) from error
        if relative not in code_hashes or sha(path) != code_hashes[relative]:
            raise ReplayError("actual imported SimpleRCA source is not frozen: " + name)
        result.append({"module": name, "path": relative, "sha256": code_hashes[relative]})
    return result


def internal_sources(audit):
    index = verified_index26(audit)
    rows = []
    for name, relative in (("simplerca", "src/simplerca/__init__.py"),
                           ("simplerca.core", "src/simplerca/core.py"),
                           ("simplerca.adapter", "src/simplerca/adapter.py")):
        expected = index["source_hashes"][relative]
        copied = verify(relative, expected, I26 + "#/source_hashes", audit)
        path = Path(importlib.import_module(name).__file__).resolve()
        row = {"module": name, "path": str(path), "expected": expected, "actual": sha(path),
               "pass": path == copied.resolve() and sha(path) == expected, "authority": I26}
        audit.append(row)
        if not row["pass"]:
            raise ReplayError("actual imported SimpleRCA source is not frozen: " + name)
        rows.append(row)
    import numpy as np
    import pandas as pd
    versions = {"numpy": np.__version__, "pandas": pd.__version__}
    if versions != {"numpy": "1.26.4", "pandas": "2.2.3"}:
        raise ReplayError("SimpleRCA numerical package versions differ from source environment")
    return {"modules": rows, "versions": versions, "native": "internal frozen src/simplerca; no external RCAEval method"}


def verify_simplerca(directory, summary):
    """Restore inputs, match their original preparation and all native components.

    Derived positions/witnesses are explicitly marked. They do not replace the
    actual native return or claim physical waiting/causal mechanisms.
    """
    import numpy as np
    import pandas as pd
    basic = verify_capture(directory, summary)
    if not summary["trace_restored"] or not summary["profile_restored"]:
        raise ReplayError("observer did not restore original hooks")
    serializer = SimpleRcaCapture.__new__(SimpleRcaCapture)
    serializer.np, serializer.pd = np, pd
    calls = [read(directory / call["path"]) for call in summary["calls"]]
    metadata = {}

    def collect(value):
        if isinstance(value, dict):
            if {"path", "signature", "columns", "index_levels", "rows"} <= set(value):
                if value["path"] in metadata and metadata[value["path"]] != value:
                    raise ReplayError("conflicting table metadata")
                metadata[value["path"]] = value
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    for call in calls:
        collect(call)
    tables, checked = {}, []
    for relative, meta in metadata.items():
        columns = [decode(column["name"]) for column in meta["columns"]]
        if meta["index_levels"] != 1 or len(columns) != len(set(columns)):
            raise ReplayError("SimpleRCA restoration requires one index and unique columns")
        values = table_columns(directory, meta)
        stored = pd.read_parquet(directory / relative, use_threads=False)
        frame = pd.DataFrame({column: values[column] for column in columns})
        frame.index = pd.Index([decode(json.loads(value)) for value in stored["index_0"]], name=decode(meta["index_names"])[0])
        frame.columns.name = decode(meta["columns_name"])
        if exact_differences(meta["signature"], serializer._table_signature(frame)):
            raise ReplayError("restored table is not value/type/order exact: " + relative)
        tables[relative] = frame
        checked.append({"path": relative, "rows": len(frame), "pass": True})

    def table(meta):
        return None if meta.get("unavailable") else tables[meta["path"]]

    def groups(meta):
        if meta["unavailable"]:
            return None
        frame = table(meta["table"])
        channels = decode(meta["channels"])
        if len(channels) != len(meta["lengths"]) or len(channels) != len(set(channels)):
            raise ReplayError("native channel metadata has duplicate/missing lengths")
        result = {}
        expected_rows = []
        for channel, count in zip(channels, meta["lengths"]):
            part = frame[frame["channel"] == channel]
            if part["position"].tolist() != list(range(count)):
                raise ReplayError("native channel positions missing/reordered")
            result[channel] = part["value"].tolist()
            expected_rows.extend((channel, pos) for pos in range(count))
        if list(frame[["channel", "position"]].itertuples(index=False, name=None)) != expected_rows:
            raise ReplayError("native channel order/coverage differs from metadata")
        return result

    def core_inputs(value):
        return {**{key: groups(value[key]) for key in
                   ("normal_metrics", "incident_metrics", "normal_traces", "incident_traces", "incident_logs")},
                "metric_services": decode(value["metric_services"]), "observed_services": decode(value["observed_services"])}

    def same(wanted, actual, message):
        if exact_differences(serializer._encode(wanted), serializer._encode(actual)):
            raise ReplayError(message)

    adapter = next(call for call in calls if call["function"] == "adapter")
    adapter_threw = adapter["outcome"] == "exception" and bool(adapter["exceptions"])
    adapter_exception = ({key: adapter["exceptions"][-1][key] for key in ("type", "message")} if adapter_threw else None)
    adapter_return = adapter["return"]
    returned_status = adapter_return.get("status") if isinstance(adapter_return, dict) else None
    status = "ERROR" if adapter_threw else returned_status
    if (summary["adapter_threw"] != adapter_threw or summary["adapter_exception"] != adapter_exception
            or summary["adapter_outcome"] != adapter["outcome"] or summary["adapter_returned_status"] != returned_status
            or summary["adapter_status"] != status
            or summary["adapter_status_source"] != ("observed_adapter_exception" if adapter_threw else "adapter_return")):
        raise ReplayError("adapter summary does not preserve actual return/exception")
    inputs = {key: table(meta) for key, meta in adapter["entry"]["tables"].items()}
    for key, meta in adapter["entry"]["tables"].items():
        wanted = {"unavailable": True} if inputs[key] is None else meta["signature"]
        same(wanted, adapter["input_after_signatures"][key], "adapter input projection changed: " + key)
    native = next((call for call in calls if call["function"] == "native"), None)
    if native is None:
        if status != "ERROR" or not (adapter_threw or adapter["exceptions"]):
            raise ReplayError("missing native call without observed preparation error")
        return {**basic, "tables_reconstructed": checked, "hooks_restored": True,
                "adapter_input_projections_unchanged": True, "native_called": False,
                "native_formula_exact": False, "adapter_status": status, "adapter_exception": adapter_exception,
                "reason": "native not reached; observed original adapter/preparation error retained"}
    values = core_inputs(native["entry"]["inputs"])
    same(values, core_inputs(native["inputs_after"]), "native mutated original measurement inputs")
    config = decode(native["entry"]["config"])
    wanted_config = {"metric_rule": "sigma", "sigma": 3.0, "metric_quantile": 0.95,
        "trace_quantile": 0.95, "trace_factor": 3.0, "log_threshold": 0,
        "metric_aggregation": "events", "min_normal_metric": 2, "keywords": ["ERROR", "FAIL", "EXCEPTION"]}
    same(wanted_config, config, "native configuration differs from frozen M4 defaults")
    spans, logs = inputs["spans"], inputs["logs"]
    if summary["dataset"] == "RE2-TT":
        prepare = next(call for call in calls if call["function"] == "prepare")
        core = next(call for call in calls if call["function"] == "core_input")
        if prepare["outcome"] != "return" or core["outcome"] != "return":
            raise ReplayError("native reached without returned preparation/core_input")
        same(values, core_inputs(core["return"]), "core_input return differs from native entry")
        parameters = decode(prepare["entry"]["parameters"])
        boundary, half, aliases = parameters["boundary"], parameters["half"], parameters["aliases"] or {}
        if boundary != decode(adapter["entry"]["t_seconds"]) or half != 300:
            raise ReplayError("unexpected RE2 boundary/window")
        metrics = inputs["metric"]
        mt = pd.to_numeric(metrics["time"], errors="raise").to_numpy()
        keys = [column for column in metrics if column not in ("time", "time.1")]
        mappings = {column: aliases.get(column.rsplit("_", 1)[0], column.rsplit("_", 1)[0]) for column in keys}
        same(mappings, decode(prepare["metric_services"]), "prepare metric mapping differs")
        expected = {}
        for key, mask in (("normal_metrics", (mt >= boundary-half) & (mt < boundary)),
                          ("incident_metrics", (mt >= boundary) & (mt < boundary+half))):
            frame = metrics.loc[mask, keys].copy()
            frame.insert(0, "time", mt[mask])
            expected[key] = frame
        if spans is None:
            nt = at = pd.DataFrame(columns=["service", "duration"])
        else:
            starts = pd.to_numeric(spans["startTime"], errors="raise").to_numpy() / 1e6
            traces = spans[["serviceName", "duration"]].rename(columns={"serviceName": "service"}).copy()
            traces["service"] = traces["service"].map(lambda s: aliases.get(s, s))
            nt = traces.loc[(starts >= boundary-half) & (starts < boundary)].reset_index(drop=True)
            at = traces.loc[(starts >= boundary) & (starts < boundary+half)].reset_index(drop=True)
        expected.update(normal_traces=nt, incident_traces=at)
        observed = set(mappings.values()) | set(nt["service"]) | set(at["service"])
        al = None
        if logs is not None:
            times = pd.to_numeric(logs["timestamp"], errors="raise").to_numpy()
            observed.update(aliases.get(s, s) for s in logs.loc[(times >= boundary-half) & (times < boundary+half), "container_name"])
            al = logs.loc[(times >= boundary) & (times < boundary+half), ["container_name", "message"]].rename(columns={"container_name": "service"}).copy()
            al["service"] = al["service"].map(lambda s: aliases.get(s, s))
            al["message"] = al["message"].fillna("").astype(str)
        expected["incident_logs"] = al
        for key, frame in expected.items():
            actual = prepare["prepared"][key]
            if frame is None:
                if actual != {"unavailable": True}:
                    raise ReplayError("unavailable logs became available")
            else:
                same(serializer._table_signature(frame), actual["signature"], "actual prepare return differs from original source rows: " + key)
        def grouped(frame, column):
            return {service: part[column].tolist() for service, part in frame.groupby("service", sort=True)}
        wanted = {"normal_metrics": {key: expected["normal_metrics"][key].tolist() for key in mappings},
                  "incident_metrics": {key: expected["incident_metrics"][key].tolist() for key in mappings},
                  "normal_traces": grouped(nt, "duration"), "incident_traces": grouped(at, "duration"),
                  "incident_logs": None if al is None else grouped(al, "message"),
                  "metric_services": mappings, "observed_services": sorted(observed)}
        same(wanted, values, "prepared measurement groups differ from actual native inputs")
    else:
        for key, meta in adapter["entry"]["metric_arrays"].items():
            same(groups(meta), values[key], "Nezha source arrays were aligned/filled/changed")
            same(groups(meta), groups(adapter["metric_arrays_after"][key]), "Nezha source arrays changed after call")
        marker, guard = decode(adapter["entry"]["t_ns"]), decode(adapter["entry"]["guard"])
        before, after = spans["_start_ns"] < marker, spans["_start_ns"] >= marker
        if guard:
            before &= spans["_end_ns"] < marker - guard * 1_000_000_000
        for key, mask in (("before", before), ("after", after)):
            same(np.flatnonzero(mask.to_numpy()).tolist(), adapter["membership_positions"][key], "Nezha membership differs")
        wanted = dict(values)
        wanted["metric_services"] = {column: column.rsplit("_", 1)[0] for column in values["normal_metrics"]}
        for key, mask in (("normal_traces", before), ("incident_traces", after)):
            wanted[key] = {str(service): part["duration"].tolist() for service, part in spans.loc[mask].groupby("serviceName", sort=True)}
        observed = set(wanted["metric_services"].values()) | set(spans.loc[before | after, "serviceName"])
        wanted["incident_logs"] = None
        if logs is not None:
            observed.update(logs["container_name"])
            times = logs["_timestamp_ns"] if "_timestamp_ns" in logs else logs["timestamp"]
            wanted["incident_logs"] = {str(service): part["message"].tolist() for service, part in logs.loc[times >= marker].groupby("container_name", sort=True)}
        wanted["observed_services"] = sorted(observed)
        same(wanted, values, "Nezha source membership/grouping differs from native inputs")
    if native["outcome"] != "return":
        if not native["exceptions"] or not (adapter_threw or returned_status == "ERROR"):
            raise ReplayError("native exception not preserved by original adapter return/exception")
        return {**basic, "tables_reconstructed": checked, "hooks_restored": True,
                "adapter_input_projections_unchanged": True, "native_inputs_unchanged": True,
                "native_called": True, "native_outcome": "exception", "native_formula_exact": False,
                "preparation_exact": True, "adapter_status": status, "adapter_exception": adapter_exception,
                "native_exceptions": native["exceptions"], "reason": "partial native state retained; no fabricated score/rank"}
    metrics, traces, log_rows = {}, {}, {}
    services = set(values["observed_services"]) | set(values["metric_services"].values())
    services |= set(values["normal_traces"]) | set(values["incident_traces"]) | set(values["incident_logs"] or {})
    totals = {service: {"metric": 0, "trace": 0, "log": 0, "score": 0} for service in sorted(services)}
    evidence = {"kind": "derived diagnostic positions from captured native inputs and actual native config",
                "indexing": "zero-based position within captured native channel, not a unique trace count",
                "metrics": {}, "traces": {}, "logs": {}}
    usable = 0
    for key in sorted(values["normal_metrics"]):
        n0, a0 = (np.asarray(values[field][key], dtype=float) for field in ("normal_metrics", "incident_metrics"))
        nf, af = np.isfinite(n0), np.isfinite(a0)
        n, a = n0[nf], a0[af]
        row = {"service": values["metric_services"][key], "n_normal": len(n), "n_incident": len(a),
               "missing_normal": int((~nf).sum()), "missing_incident": int((~af).sum()),
               "status": "unavailable", "count": 0, "vote": 0}
        positions = {"finite_N": np.flatnonzero(nf).tolist(), "finite_A": np.flatnonzero(af).tolist(),
                     "excluded_N": np.flatnonzero(~nf).tolist(), "excluded_A": np.flatnonzero(~af).tolist(),
                     "event_positions_A": [], "availability": "unavailable"}
        if len(n) >= config["min_normal_metric"] and len(a):
            mean, std = float(n.mean()), float(n.std(ddof=0))
            threshold = mean + config["sigma"] * std
            count = int(np.sum(a > threshold))
            row.update(mean=mean, std=std, threshold=threshold, count=count, vote=count,
                       max_incident=float(a.max()), status="ok")
            totals[row["service"]]["metric"] += count
            usable += 1
            positions.update(event_positions_A=np.flatnonzero(af)[a > threshold].tolist(), availability="ok")
        metrics[key], evidence["metrics"][key] = row, positions
    for service in sorted(set(values["normal_traces"]) | set(values["incident_traces"])):
        n0, a0 = (np.asarray(values[field].get(service, []), dtype=float) for field in ("normal_traces", "incident_traces"))
        nf, af = np.isfinite(n0), np.isfinite(a0)
        n, a = n0[nf], a0[af]
        if np.any(n < 0) or np.any(a < 0):
            raise ReplayError("returned native call retained a negative finite duration")
        row = {"n_normal": len(n), "n_incident": len(a), "missing_normal": int((~nf).sum()),
               "missing_incident": int((~af).sum()), "status": "unavailable", "vote": 0}
        positions = {"finite_N": np.flatnonzero(nf).tolist(), "finite_A": np.flatnonzero(af).tolist(),
                     "excluded_N": np.flatnonzero(~nf).tolist(), "excluded_A": np.flatnonzero(~af).tolist(),
                     "availability": "unavailable"}
        if len(n) and len(a):
            qn, qa = (float(np.quantile(array, config["trace_quantile"], method="linear")) for array in (n, a))
            threshold = config["trace_factor"] * qn
            row.update(p95_normal=qn, p95_incident=qa, threshold=threshold, vote=int(qa > threshold), status="ok")
            totals[service]["trace"] += row["vote"]
            usable += 1
            positions["availability"] = "ok"
            for part, array, mask, quantile in (("N", n, nf, qn), ("A", a, af, qa)):
                order = np.argsort(array, kind="stable")
                h = (len(array)-1) * config["trace_quantile"]
                lo, hi = int(np.floor(h)), int(np.ceil(h))
                positions["quantile_" + part] = {"h": h, "weight": h-lo, "value": quantile,
                    "lower_value": float(array[order[lo]]), "upper_value": float(array[order[hi]]),
                    "lower_channel_position": int(np.flatnonzero(mask)[order[lo]]),
                    "upper_channel_position": int(np.flatnonzero(mask)[order[hi]]),
                    "ties": "representative matching rows; native quantile does not return row identities"}
        traces[service], evidence["traces"][service] = row, positions
    keyword = re.compile("|".join(re.escape(value) for value in config["keywords"]), re.IGNORECASE)
    for service in sorted(services):
        if values["incident_logs"] is None:
            row = {"status": "unavailable", "count": None, "vote": 0}
            evidence["logs"][service] = {"availability": "unavailable", "keyword_positions_A": None}
        else:
            entries = values["incident_logs"].get(service, [])
            hits = [position for position, message in enumerate(entries) if keyword.search(message)]
            count, vote = len(hits), int(len(hits) > config["log_threshold"])
            row = {"status": "ok", "count": count, "threshold": config["log_threshold"], "vote": vote}
            totals[service]["log"] += vote
            usable += 1
            evidence["logs"][service] = {"availability": "ok", "rows_A": len(entries), "keyword_positions_A": hits,
                                         "unit": "at most one keyword hit per message row"}
        log_rows[service] = row
        totals[service]["score"] = sum(totals[service][key] for key in ("metric", "trace", "log"))
    if usable == 0:
        raise ReplayError("returned native call had no usable channel")
    ranks = sorted(totals, key=lambda service: (-totals[service]["score"], service))
    tie_groups = []
    for service in ranks:
        if not tie_groups or tie_groups[-1]["score"] != totals[service]["score"]:
            tie_groups.append({"score": totals[service]["score"], "services": []})
        tie_groups[-1]["services"].append(service)
    native_status = "abstain" if tie_groups[0]["score"] == 0 else "heuristic_alerts"
    expected = {"config": config, "status": native_status, "ranks": ranks, "tie_groups": tie_groups,
                "scores": totals, "metrics": metrics, "traces": traces, "logs": log_rows,
                "fallback": False, "interpretation": "candidate ranking; scores do not establish a causal root"}
    same(expected, decode(read(directory / "native-result.json")), "full actual native return differs from exact restored channel formulas")
    for key, value in (("metrics", metrics), ("traces", traces), ("logs", log_rows), ("totals", totals), ("usable", usable)):
        same(value, decode(native["locals"][key]), "native local stage differs from full actual return: " + key)
    expected_status = "NO_EVIDENCE" if native_status == "abstain" else "OK"
    if returned_status != expected_status or decode(adapter_return["method_status_raw"]) != native_status:
        raise ReplayError("native abstain/heuristic status changed in adapter")
    if decode(adapter_return["ranking_native"]) != ranks:
        raise ReplayError("adapter native ranks changed")
    expected_items = [] if native_status == "abstain" else [[service,
        service.split("_", 1)[0] if summary["dataset"] == "RE2-TT" else service,
        [float(totals[service]["score"])]] for service in ranks]
    same(expected_items, decode(adapter_return["items"]), "adapter score/service-to-entity mapping differs")
    observed_entities = sorted({service.split("_", 1)[0] for service in values["observed_services"]}) if summary["dataset"] == "RE2-TT" else sorted(values["observed_services"])
    same(observed_entities, decode(adapter_return["observed_entities"]), "observed entities differ")
    dump(directory / "row-evidence.json", serializer._encode(evidence))
    return {**basic, "tables_reconstructed": checked, "hooks_restored": True,
            "adapter_input_projections_unchanged": True, "native_inputs_unchanged": True,
            "preparation_exact": True, "native_called": True, "native_outcome": "return",
            "native_formula_exact": True, "full_native_return_exact": True,
            "native_status": native_status, "adapter_status": status, "adapter_mapping_exact": True,
            "usable_channels": usable, "row_evidence": "row-evidence.json",
            "limits": "native computation evidence only; no waiting/physical-cause claim; frozen equality still required"}


def one(directory, dataset, opaque_id):
    audit = []
    progress(directory, "SOURCE_CHECK_START", method="simplerca", dataset=dataset, opaque_id=opaque_id)
    try:
        entry, frozen, index26, code_hashes = source_for(dataset, opaque_id, audit)
        if frozen["status"] == "UNSUPPORTED":
            dump(directory / "source.json", {"entry": entry, "frozen": frozen, "method_called": False})
            dump(directory / "check.json", {"status": "PASS", "method": "simplerca", "dataset": dataset,
                "opaque_id": opaque_id, "frozen_status": "UNSUPPORTED", "replay_status": None,
                "method_called": False, "intermediates_eligible": False,
                "compare": {"pass": None, "status": "not_replayed"},
                "interpretation": "authenticated UNSUPPORTED source retained; no supported path fabricated"})
            return 0
        from p3 import ban_ghi, runner, selector, worker
        environment = internal_sources(audit)
        if dataset == "RE2-TT":
            allow_path = safe_source("results/T-022/allowlist-dev.json")
            allow = selector.nap_allowlist(allow_path)
            wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
            if wanted != frozen["input_sha256"]:
                raise ReplayError("selected allowlist hashes differ from frozen inputs")
            files = selector.chon_ca(allow, opaque_id, RE2_RAW_REPO, kiem_hash=True)
            job = {"kind": "ranker", "method": "simplerca", "t": frozen["window"]["t"], "model": None,
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
                   "view": "main", "method": "simplerca", "trace_guard_s": 0}
            invoke = nezha_worker.main
        dump(directory / "source.json", {"dataset": dataset, "opaque_id": opaque_id, "entry": entry,
             "source_run_id": frozen["run_id"], "source_status": frozen["status"], "environment": environment,
             "actual_imports": loaded_simple_sources(code_hashes), "allowlist_path": str(allow_path),
             "allowlist_sha256": sha(allow_path), "selected_allowlist_hashes_equal_frozen_inputs": True,
             "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS,
             "reuse": "frozen ranking/status/keys are comparison source; T028 aggregate totals/rankings reused; actual full native return and row/channel evidence are newly captured"})
        dump(directory / "job.json", job)
        progress(directory, "WORKER_START", method="simplerca", source_status=frozen["status"])
        started = time.perf_counter()
        with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout:
            with (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    with SimpleRcaCapture(directory / "capture", dataset) as capture:
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
            records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "simplerca", "a")
            if len(records) != 1:
                raise ReplayError("SimpleRCA reconstruction did not return one record")
        else:
            if len(output["ket_qua_nhieu"]) != 1:
                raise ReplayError("SimpleRCA worker did not return one result")
            result = output["ket_qua_nhieu"][0]
            record = ban_ghi.tao("simplerca", VERSIONS["simplerca"], VARIANTS["simplerca"], "a", result, output["window"],
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
        capture_check = verify_simplerca(directory / "capture", summary)
        imports_after = loaded_simple_sources(code_hashes)
        internal_sources(audit)
        dump(directory / "source-checks.json", {"checks": audit})
        progress(directory, "FINISHED", status="PASS" if not differences else "FAIL")
        dump(directory / "check.json", {"status": "PASS" if not differences else "FAIL", "method": "simplerca",
            "dataset": dataset, "opaque_id": opaque_id, "frozen_path": entry["path"], "frozen_sha256": entry["sha256"],
            "frozen_status": frozen["status"], "replay_status": replay["status"],
            "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS, "differences": differences,
            "compare": {"pass": not differences, "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS,
                        "difference_count": len(differences)}, "capture_status": summary["status"], "capture_check": capture_check,
            "actual_imports_after": imports_after, "intermediates_eligible": not differences,
            "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
            "interpretation": "exact replay of one SimpleRCA record only; metric/trace/log components and mapping observed; no causal or wait-semantics claim"})
        return 0 if not differences else 1
    finally:
        if not (directory / "source-checks.json").exists():
            dump(directory / "source-checks.json", {"checks": audit})


def fixture_data(name, dataset):
    import numpy as np
    import pandas as pd
    boundary = 1_700_000_000
    services = ("db", "db_replica") if name == "underscore_mapping" else ("alpha", "beta")
    times = [boundary-2, boundary-1, boundary, boundary+1]
    metric_values = [1.0, 1.0, 2.0, 1.0]
    if name in ("strict_equality", "zero_abstain"):
        metric_values = [1.0] * 4
    elif name == "all_unavailable":
        metric_values = [np.nan] * 4
    elif name == "finite_dropped":
        metric_values = [1.0, np.nan, 2.0, np.inf]
    metrics = pd.DataFrame({"time": times, **{service + "_cpu": metric_values for service in services}})
    rows = []
    if name not in ("zero_abstain", "all_unavailable"):
        for service in services:
            normal = (1000.0, np.nan) if name == "finite_dropped" else (1000.0, 1000.0)
            anomalous = (3000.0, 3000.0) if name == "strict_equality" else (-1.0, 4000.0) if name == "negative_trace" else (4000.0, 1000.0)
            for start, duration in zip(times, (*normal, *anomalous)):
                rows.append((service, start*1_000_000, duration, start*1_000_000_000,
                             start*1_000_000_000 + (0 if not np.isfinite(duration) else int(duration*1000))))
    spans = pd.DataFrame(rows, columns=("serviceName", "startTime", "duration", "_start_ns", "_end_ns"))
    spans["traceID"], spans["spanID"], spans["parentSpanID"] = "same-trace", [str(i) for i in range(len(spans))], ""
    logs = None
    if name in ("scalar", "ties"):
        logs = pd.DataFrame([(boundary, services[0], "ERROR FAIL in one row")], columns=("timestamp", "container_name", "message"))
        if name == "ties":
            logs = logs.iloc[:0].copy()
    if dataset == "RE2-TT":
        return {"metric_win": metrics, "spans": spans, "logs": logs, "t": boundary}
    if logs is not None:
        logs["timestamp"] = logs["timestamp"] * 1_000_000_000
        logs["_timestamp_ns"] = logs["timestamp"]
    return {"metric_arrays": {service + "_cpu": {"normal": metric_values[:2], "anomalous": metric_values[2:]} for service in services},
            "spans": spans, "logs": logs, "t_ns": boundary*1_000_000_000,
            "window": {"t_ns": boundary*1_000_000_000, "trace_guard_s": 0}}


def fixtures(directory):
    import numpy as np
    import pandas as pd
    from p3 import ban_ghi
    from p3.adapters import simplerca, nezha
    audit = []
    environment = internal_sources(audit)
    dump(directory / "source-checks.json", {"checks": audit, "environment": environment})
    checks = []
    serializer = SimpleRcaCapture.__new__(SimpleRcaCapture)
    serializer.np, serializer.pd = np, pd

    def fingerprint(value):
        return {key: {"table_signature": serializer._table_signature(item)} if isinstance(item, pd.DataFrame)
                else serializer._encode(item) for key, item in value.items()}

    def invoke(dataset, value):
        return simplerca.chay(**value) if dataset == "RE2-TT" else nezha.chay("simplerca", value, trace_guard_s=0)[0]

    for dataset in ("RE2-TT", "Nezha-OB"):
        for name in ("scalar", "ties", "strict_equality", "zero_abstain", "finite_dropped", "all_unavailable", "negative_trace", "underscore_mapping"):
            case_dir = directory / (dataset + "-" + name)
            case_dir.mkdir()
            values = fixture_data(name, dataset)
            original_values = copy.deepcopy(values)
            before = fingerprint(values)
            progress(directory, "FIXTURE_START", dataset=dataset, name=name)
            prior_trace, prior_profile = sys.gettrace(), sys.getprofile()
            def existing_profile(_frame, _event, _arg):
                return None
            original = observed = None
            original_exception = observed_exception = None
            sys.setprofile(existing_profile)
            try:
                try:
                    original = invoke(dataset, values)
                except Exception as error:
                    original_exception = {"type": type(error).__name__, "message": str(error)}
                try:
                    with SimpleRcaCapture(case_dir / "capture", dataset) as capture:
                        observed = invoke(dataset, values)
                except Exception as error:
                    observed_exception = {"type": type(error).__name__, "message": str(error)}
                existing_profile_preserved = sys.getprofile() is existing_profile
            finally:
                sys.setprofile(prior_profile)
            summary = capture.require_complete()
            input_differences = exact_differences(before, fingerprint(values))
            if input_differences or exact_differences(before, fingerprint(original_values)):
                raise ReplayError("fixture method input changed")
            original = json.loads(json.dumps(original, allow_nan=False))
            observed = json.loads(json.dumps(observed, allow_nan=False))
            original_outcome = {"outcome": "exception" if original_exception else "return", "return": original, "exception": original_exception}
            observed_outcome = {"outcome": "exception" if observed_exception else "return", "return": observed, "exception": observed_exception}
            dump(case_dir / "original-adapter.json", original_outcome)
            dump(case_dir / "observed-adapter.json", observed_outcome)
            differences = exact_differences(original_outcome, observed_outcome)
            record = None
            if original_exception is None and observed_exception is None:
                kwargs = {"method": "simplerca", "method_version": "synthetic fixture only", "variant": "native" if dataset == "RE2-TT" else "M4",
                          "mode": "a", "window": {"t": 1_700_000_000}, "config_id": "T-032-fixture", "why_ids": [], "hashseed": 0}
                record = ban_ghi.tao(ket_qua=observed, **kwargs)
                differences.extend(exact_differences(ban_ghi.tao(ket_qua=original, **kwargs), record))
            expected_status = "NO_EVIDENCE" if name in ("strict_equality", "zero_abstain") else "ERROR" if name in (
                "all_unavailable", "negative_trace") or name == "underscore_mapping" and dataset == "Nezha-OB" else "OK"
            actual_status = "ERROR" if observed_exception else observed["status"]
            invariants = {"expected_status": actual_status == expected_status,
                "trace_restored": sys.gettrace() is prior_trace, "profile_restored": sys.getprofile() is prior_profile,
                "existing_profile_preserved": existing_profile_preserved,
                "adapter_outcome_preserved": summary["adapter_outcome"] == observed_outcome["outcome"],
                "adapter_exception_preserved": summary["adapter_exception"] == observed_exception,
                "adapter_status_preserved": summary["adapter_status"] == actual_status}
            native = read(case_dir / "capture" / "native-result.json") if (case_dir / "capture" / "native-result.json").exists() else None
            if name == "scalar":
                invariants.update(component_sum=native["scores"]["alpha"] == {"metric": 1, "trace": 1, "log": 1, "score": 3},
                                  one_keyword_per_row=native["logs"]["alpha"]["count"] == 1)
            elif name == "ties":
                invariants.update(exact_ties=native["tie_groups"] == [{"score": 2, "services": ["alpha", "beta"]}],
                                  adapter_ties=len(record["entity_ranking"]) == 2 and all(row["tie_group"] == 0 for row in record["entity_ranking"]))
            elif name in ("strict_equality", "zero_abstain"):
                invariants.update(native_abstain=native["status"] == "abstain", zero_score=all(row["score"] == 0 for row in native["scores"].values()),
                                  nonempty_native_ranks=bool(observed["ranking_native"]), empty_adapter_items=observed["items"] == [])
            elif name == "finite_dropped":
                invariants.update(metric_unavailable=native["metrics"]["alpha_cpu"]["status"] == "unavailable",
                                  trace_nan_dropped=native["traces"]["alpha"]["missing_normal"] == 1 and native["traces"]["alpha"]["vote"] == 1)
            elif name == "all_unavailable":
                invariants.update(native_error=summary["native_outcome"] == "exception",
                                  not_abstain=actual_status == "ERROR" and (observed is None or observed.get("method_status_raw") != "abstain"))
            elif name == "negative_trace":
                invariants.update(native_error=summary["native_outcome"] == "exception", negative_error="negative duration" in (
                    observed_exception["message"] if observed_exception else observed["error"]))
            elif name == "underscore_mapping":
                if dataset == "RE2-TT":
                    invariants.update(native_services_kept=set(native["scores"]) == {"db", "db_replica"},
                                      p3_entity_max=len(record["entity_ranking"]) == 1 and record["entity_ranking"][0]["entity"] == "db"
                                      and record["entity_ranking"][0]["key"] == [2.0])
                else:
                    invariants.update(mapping_rejected=summary["native_outcome"] is None and observed_exception is not None
                                      and "metric mapping Nezha" in observed_exception["message"])
            capture_check = verify_simplerca(case_dir / "capture", summary)
            check = {"dataset": dataset, "name": name, "expected_status": expected_status, "actual_status": actual_status,
                     "status_source": "observed_adapter_exception" if observed_exception else "adapter_return",
                     "original_adapter_exception": original_exception, "observed_adapter_exception": observed_exception,
                     "input_unchanged": True, "differences": differences, "invariants": invariants,
                     "capture_check": capture_check, "pass": not differences and all(invariants.values())}
            dump(case_dir / "check.json", check)
            checks.append(check)
            progress(directory, "FIXTURE_DONE", dataset=dataset, name=name, status="PASS" if check["pass"] else "FAIL")
            if not check["pass"]:
                dump(directory / "check.json", {"status": "FAIL", "fixtures": checks,
                     "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"]})
                return 1
    dump(directory / "check.json", {"status": "PASS", "fixtures": checks,
         "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
         "limits": "synthetic observer/status/component/mapping checks only; no real frozen replay or mechanism claim"})
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
            ("capture_simplerca.py", "replay_simplerca_v4.py", "audit_simplerca_output_v3.py", "replay_simplerca.py", "capture_microrank.py", "replay_microrank.py")},
        "python": sys.version, "hashseed": os.environ.get("PYTHONHASHSEED"), "source_repo": str(REPO)})
    try:
        return fixtures(directory) if args.command == "fixture" else one(directory, args.dataset, args.opaque_id)
    except Exception as error:
        failure = {"status": "FAIL", "method": "simplerca", "type": type(error).__name__, "error": str(error),
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
