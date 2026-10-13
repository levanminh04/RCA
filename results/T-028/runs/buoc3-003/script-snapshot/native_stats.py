"""T-028 label-free measurement summaries, independent of all rankers.

Only allowlisted dev inputs are read. Nezha payload and graph adjacency stay
in memory. The first return of compute_case is safe to serialize; the second
must remain in RAM until the caller has written all label-free summaries.
"""
from __future__ import annotations

import math
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

KEYWORD = re.compile(r"ERROR|FAIL|EXCEPTION", re.IGNORECASE)
DATASETS = {"RE2-TT", "Nezha-OB"}


def feature(value=None, reason=None):
    return {"value": value if reason is None else None, "availability": "available" if reason is None else "N/A",
            "reason": reason}


def _native_imports(repo):
    source = str(Path(repo).resolve() / "src")
    if source not in sys.path:
        sys.path.insert(0, source)
    from p3 import selector, cua_so, nezha
    return selector, cua_so, nezha


def _time_extrema(values):
    if not len(values):
        return {"rows": 0, "first": None, "last": None}
    return {"rows": int(len(values)), "first": int(min(values)), "last": int(max(values))}


def _strip_time_vectors(value):
    """Reader provenance includes time vectors; never expose those on disk."""
    if isinstance(value, dict):
        return {k: _strip_time_vectors(v) for k, v in value.items()
                if k not in {"timestamps_ns"}}
    if isinstance(value, (list, tuple)):
        return [_strip_time_vectors(v) for v in value]
    return value


def load_case(repo, dataset, oid, t=None):
    """Return guarded measurements on RAM; does not load labels or rankings.

    RE2's mode-(a) boundary t must be supplied from a saved native record.
    Nezha's boundary comes from its label-free allowlist, main, guard zero.
    """
    if dataset not in DATASETS:
        raise ValueError("dataset outside T-028 main cohorts")
    repo = Path(repo).resolve()
    selector, cua_so, nezha = _native_imports(repo)
    start = time.perf_counter()
    if dataset == "RE2-TT":
        if isinstance(t, bool) or t is None or not float(t).is_integer():
            raise ValueError("RE2 requires integer native record window.t")
        allow_path = repo / "results/T-022/allowlist-dev.json"
        allowlist = selector.nap_allowlist(allow_path)
        paths = selector.chon_ca(allowlist, oid, repo, kiem_hash=True)
        read_start = time.perf_counter()
        metrics = pd.read_parquet(paths["metrics.parquet"])
        spans = pd.read_parquet(paths["traces.parquet"]) if "traces.parquet" in paths else None
        logs = pd.read_parquet(paths["logs.parquet"]) if "logs.parquet" in paths else None
        full_rows = {"metrics.parquet": len(metrics),
                     "traces.parquet": None if spans is None else len(spans),
                     "logs.parquet": None if logs is None else len(logs)}
        payload, window = cua_so.cat_ca(metrics, spans, logs, int(t))
        payload["spans"] = payload.pop("traces")
        payload["window"] = window
        payload["t_seconds"] = int(t)
        payload["time_unit"] = {"metric": "s", "trace": "us", "log": "s"}
        arrays = {}
        before = payload["metric"]["time"] < int(t)
        for column in payload["metric"]:
            if column in {"time", "time.1"}:
                continue
            if "_" not in column or not all(column.rsplit("_", 1)):
                raise ValueError("ambiguous_mapping: metric requires service_suffix")
            arrays[column] = {
                "normal": payload["metric"].loc[before, column].to_numpy(dtype=float),
                "anomalous": payload["metric"].loc[~before, column].to_numpy(dtype=float)}
        payload["metric_arrays"] = arrays
        sources = {}
        for name, meta in allowlist[oid]["files"].items():
            if meta is None:
                sources[name] = {"availability": "N/A", "reason": "missing_channel"}
                continue
            entry = dict(meta, full_file_rows=full_rows[name])
            if name == "metrics.parquet":
                tm = payload["metric"]["time"]
                entry.update(window=_time_extrema(tm), N=_time_extrema(tm[tm < t]),
                             A=_time_extrema(tm[tm >= t]), time_unit="s")
            elif name == "traces.parquet":
                tr = payload["spans"]
                if tr is not None:
                    st, en = tr["startTime"], tr["startTime"] + tr["duration"]
                    entry.update(window_rows=len(tr), start_window=_time_extrema(st),
                                 end_window=_time_extrema(en), time_unit="us")
            elif name == "logs.parquet":
                lg = payload["logs"]
                if lg is not None:
                    ts = lg["timestamp"]
                    entry.update(window=_time_extrema(ts), N=_time_extrema(ts[ts < t]),
                                 A=_time_extrema(ts[ts >= t]), time_unit="s")
            sources[name] = entry
        payload["provenance_safe"] = {"allowlist": str(allow_path.relative_to(repo)).replace("\\", "/"),
                                      "allowlist_sha256": selector.sha256_file(allow_path),
                                      "sources": sources}
    else:
        allow_path = repo / "results/T-026/allowlist-dev.json"
        allowlist = nezha.nap_allowlist(allow_path)
        selection = nezha.chon_ca(allowlist, oid, repo, view="main")
        read_start = time.perf_counter()
        payload = nezha.doc_cua_so(selection, trace_guard_s=0)
        if t is not None and int(t) * nezha.NS != payload["t_ns"]:
            raise ValueError("Nezha native record boundary differs from allowlist main")
        payload["t_seconds"] = payload["t_ns"] // nezha.NS
        payload["time_unit"] = {"metric": "ns, per-source arrays", "trace": "us with ns membership", "log": "ns"}
        payload["provenance_safe"] = _strip_time_vectors(payload["provenance"])
        payload["provenance_safe"]["allowlist"] = str(allow_path.relative_to(repo)).replace("\\", "/")
        payload["provenance_safe"]["allowlist_sha256"] = selector.sha256_file(allow_path)
    payload["read_cost"] = {"selection_hash_seconds": read_start - start,
                            "read_and_window_seconds": time.perf_counter() - read_start}
    return payload


def metric_stats(normal, anomalous):
    """SimpleRCA convention: finite values only, population std, strict >."""
    n0, a0 = np.asarray(normal, dtype=float), np.asarray(anomalous, dtype=float)
    n, a = n0[np.isfinite(n0)], a0[np.isfinite(a0)]
    reason = "insufficient_N" if len(n) < 2 else "empty_A" if not len(a) else None
    out = {"nN": len(n), "nA": len(a), "missing_N": int((~np.isfinite(n0)).sum()),
           "missing_A": int((~np.isfinite(a0)).sum()), "ddof": 0,
           "availability": "available" if reason is None else "N/A", "reason": reason}
    # These component descriptions are meaningful when their own inputs exist.
    out["muN"] = feature(float(n.mean()), None) if len(n) else feature(reason="insufficient_N")
    out["sigmaN"] = feature(float(n.std(ddof=0)), None) if len(n) >= 2 else feature(reason="insufficient_N")
    if reason is not None:
        out.update(theta=feature(reason=reason), events=feature(reason=reason), vote=feature(reason=reason))
    else:
        mean, std = float(n.mean()), float(n.std(ddof=0))
        threshold = mean + 3 * std
        events = int(np.sum(a > threshold))
        out.update(theta=feature(threshold), events=feature(events), vote=feature(events))
    return out


def trace_stats(normal, anomalous):
    """Finite P95s and tau=2/3/4 proxy, with invalid duration kept N/A."""
    n0, a0 = np.asarray(normal, dtype=float), np.asarray(anomalous, dtype=float)
    n, a = n0[np.isfinite(n0)], a0[np.isfinite(a0)]
    invalid = bool((~np.isfinite(n0)).any() or (~np.isfinite(a0)).any()
                   or (n < 0).any() or (a < 0).any())
    reason = "nonfinite" if invalid else "insufficient_N" if not len(n) else "empty_A" if not len(a) else None
    out = {"nN": len(n), "nA": len(a), "rows_N": len(n0), "rows_A": len(a0),
           "missing_N": int((~np.isfinite(n0)).sum()), "missing_A": int((~np.isfinite(a0)).sum()),
           "negative_N": int((n < 0).sum()), "negative_A": int((a < 0).sum()),
           "quantile": 0.95, "quantile_method": "linear", "duration_unit": "us",
           "availability": "available" if reason is None else "N/A", "reason": reason}
    out["P95N"] = feature(float(np.quantile(n, .95, method="linear"))) if len(n) and not invalid else feature(reason=reason)
    out["P95A"] = feature(float(np.quantile(a, .95, method="linear"))) if len(a) and not invalid else feature(reason=reason)
    out["latency_up"] = {str(tau): feature(reason=reason) if reason else
                         feature(bool(out["P95A"]["value"] > tau * out["P95N"]["value"]))
                         for tau in (2, 3, 4)}
    out["vote"] = out["latency_up"]["3"].copy()
    return out


def _span_splits(spans, t_seconds, dataset):
    if spans is None:
        return None, None
    required = {"serviceName", "startTime", "duration"}
    if not required <= set(spans):
        raise ValueError("missing trace fields")
    if dataset == "Nezha-OB":
        required |= {"_start_ns", "_end_ns"}
        if not required <= set(spans):
            raise ValueError("missing ns/us membership fields")
        t_ns, t_us = int(t_seconds) * 1_000_000_000, int(t_seconds) * 1_000_000
        start_before, end_before = spans["_start_ns"] < t_ns, spans["_end_ns"] < t_ns
        if not (start_before == (spans["startTime"] < t_us)).all():
            raise ValueError("ns/us changes start membership")
        if not (end_before == ((spans["startTime"] + spans["duration"]) < t_us)).all():
            raise ValueError("ns/us changes end membership")
    else:
        t_us = int(t_seconds) * 1_000_000
        start_before = spans["startTime"] < t_us
        end_before = (spans["startTime"] + spans["duration"]) < t_us
    return start_before, end_before


def operation_stats(spans, before, convention="microrank"):
    """Native span arithmetic; no PageRank, ji, graph weight or ranker call."""
    empty = {"operations": {}, "services": {}, "total_abnormal_spans_A": feature(reason="missing_channel"),
             "trace_A_count": feature(reason="missing_channel"), "trace_A_abnormal_count": feature(reason="missing_channel")}
    if spans is None:
        return empty
    if convention not in {"microrank", "tracerca"}:
        raise ValueError("unknown native span convention")
    columns = ["traceID", "spanID", "parentSpanID", "serviceName", "methodName", "operationName", "startTime", "duration"]
    if set(columns) - set(spans):
        return dict(empty, reason="missing_channel")
    df = spans[columns].copy()
    conflict_keys = df.drop_duplicates().duplicated(["traceID", "spanID"], keep=False)
    conflicting = int(df.drop_duplicates().loc[conflict_keys, ["traceID", "spanID"]].drop_duplicates().shape[0])
    invalid_times = (df[["startTime", "duration"]].isna().any().any()
                     or not np.isfinite(df[["startTime", "duration"]].to_numpy(dtype=float)).all()
                     or bool((df["duration"] < 0).any()))
    df["methodName"] = df["methodName"].fillna(df["operationName"])
    invalid_names = bool(df[["traceID", "spanID", "serviceName", "methodName"]].isna().any().any())
    if invalid_names:
        return dict(empty, reason="ambiguous_mapping", id_conflict_keys=conflicting)
    df["operation"] = df["serviceName"] + "_" + df["methodName"]
    pairs = df[["operation", "serviceName", "methodName"]].drop_duplicates()
    ambiguous_ops = set(pairs.loc[pairs.duplicated("operation", keep=False), "operation"])
    if convention == "microrank":
        df = df.sort_values(["traceID", "startTime", "spanID"], kind="mergesort")
    # Align to original outer row index after MicroRank's stable sort.
    pre, post = df.loc[before.reindex(df.index)], df.loc[~before.reindex(df.index)]
    pre_groups = {op: part for op, part in pre.groupby("operation", sort=False)}
    post_groups = {op: part for op, part in post.groupby("operation", sort=False)}
    empty_part = df.iloc[:0]
    baseline = pre.groupby("operation", sort=True)["duration"].agg(["mean", "std", "count"])
    rounded_mean = (baseline["mean"] / 1000).round(2)
    rounded_std = (baseline["std"] / 1000).round(2)
    if convention == "tracerca":
        # Native TraceRCA uses each original-order Series, then built-in
        # round on the scalar returned by pandas; no helper is invoked.
        rounded_mean = pd.Series({op: round(part["duration"].mean() / 1000, 2)
                                  for op, part in pre_groups.items()}, dtype=float)
        rounded_std = pd.Series({op: round(part["duration"].std(ddof=1) / 1000, 2)
                                 for op, part in pre_groups.items()}, dtype=float)
    operations, flags_by_index = {}, {}
    for op, group in df.groupby("operation", sort=True):
        service = str(group["serviceName"].iloc[0])
        normal = pre_groups.get(op, empty_part)
        anomalous = post_groups.get(op, empty_part)
        reason = ("ambiguous_mapping" if (conflicting and convention == "microrank") or op in ambiguous_ops else
                  "nonfinite" if invalid_times else "insufficient_N" if len(normal) < 2 else None)
        if op in baseline.index and math.isfinite(float(rounded_mean[op])):
            mean = feature(float(rounded_mean[op]))
        else:
            mean = feature(reason="insufficient_N")
        std = feature(float(rounded_std[op])) if op in baseline.index and math.isfinite(float(rounded_std[op])) else feature(reason="insufficient_N")
        threshold = feature(float(rounded_mean[op] + 3 * rounded_std[op])) if reason is None else feature(reason=reason)
        if reason is None:
            flags = anomalous["duration"] / 1000 >= threshold["value"]
            flags_by_index.update({index: bool(flag) for index, flag in flags.items()})
            count = feature(int(flags.sum()))
        else:
            count = feature(reason=reason)
        operations[str(op)] = {"native_service": service, "entity": service,
                               "nN": len(normal), "nA": len(anomalous), "ddof": 1,
                               "round_decimals": 2, "duration_unit": "ms", "comparison": ">=",
                               "native_convention": convention,
                               "round_implementation": "pandas groupby then Series.round" if convention == "microrank" else "original-order Series.mean/std then built-in round",
                               "muN_round": mean, "sigmaN_round": std, "threshold": threshold,
                               "abnormal_spans_A": count, "availability": "available" if reason is None else "N/A", "reason": reason}
    all_traces = set(post["traceID"].astype(str))
    abnormal_traces = set(post.loc[[i for i in post.index if flags_by_index.get(i) is True], "traceID"].astype(str))
    all_A_eligible = all(operations[op]["abnormal_spans_A"]["availability"] == "available" for op in set(post["operation"]))
    total_reason = None if all_A_eligible else "ambiguous_mapping" if conflicting and convention == "microrank" else "insufficient_N"
    for op, row in operations.items():
        op_traces = set(post_groups.get(op, empty_part)["traceID"].astype(str))
        row["trace_A_contains_operation"] = feature(len(op_traces))
        row["trace_A_abnormal_contains_operation"] = feature(len(op_traces & abnormal_traces)) if total_reason is None else feature(reason=total_reason)
    services = {}
    for service in sorted(set(df["serviceName"])):
        rows = [row for row in operations.values() if row["native_service"] == service]
        a_rows = [row for row in rows if row["nA"]]
        bad = next((row["reason"] for row in a_rows if row["reason"]), None)
        reason = bad or ("empty_A" if not a_rows else None)
        n_abnormal = sum(row["abnormal_spans_A"]["value"] for row in a_rows) if reason is None else None
        services[str(service)] = {"native_service": str(service), "entity": str(service),
                                  "nN": sum(row["nN"] for row in rows), "nA": sum(row["nA"] for row in rows),
                                  "operations_N": sum(bool(row["nN"]) for row in rows),
                                  "operations_A": len(a_rows), "baseline_unavailable_operations_A": sum(bool(row["reason"]) for row in a_rows),
                                  "abnormal_spans_A": feature(n_abnormal, reason),
                                  "local_nonpositive": feature(n_abnormal == 0, reason) if reason is None else feature(reason=reason)}
    return {"operations": operations, "services": services, "id_conflict_keys": conflicting,
            "native_convention": convention, "id_conflict_invalidates_baseline": convention == "microrank",
            "ambiguous_operations": sorted(ambiguous_ops), "rows_N": len(pre), "rows_A": len(post),
            "duplicates_retained": True, "total_abnormal_spans_A": feature(len([v for v in flags_by_index.values() if v]), total_reason),
            "trace_A_count": feature(len(all_traces)),
            "trace_A_abnormal_count": feature(len(abnormal_traces), total_reason),
            "trace_A_normal_count": feature(len(all_traces - abnormal_traces), total_reason)}


def graph_stats(spans, before):
    """Return (serializable counts, RAM-only adjacency), caller -> callee.

    Conflicts are found on the full outer window and removed before N is
    selected. Identity signature is exactly service,parent,start,duration.
    No edge, span identifier or timestamp vector is in the first return.
    """
    reason = "missing_channel"
    if spans is None or set(["traceID", "spanID", "parentSpanID", "serviceName", "startTime", "duration"]) - set(spans):
        return {"availability": "N/A", "reason": reason}, None
    keys, conflict, duplicate_rows, signature_by_key = {}, set(), 0, {}
    conflict_N = set()
    duplicate_N = 0
    measurements = spans[["traceID", "spanID", "parentSpanID", "serviceName", "startTime", "duration"]].itertuples(index=False, name=None)
    for (tid, sid, parent, service, start, duration), in_N in zip(measurements, before.to_numpy(dtype=bool)):
        if pd.isna(tid) or pd.isna(sid) or pd.isna(service) or not isinstance(service, str) or not service:
            return {"availability": "N/A", "reason": "ambiguous_mapping"}, None
        if not math.isfinite(float(start)) or not math.isfinite(float(duration)) or float(duration) < 0:
            return {"availability": "N/A", "reason": "nonfinite"}, None
        key = (str(tid), str(sid))
        parent = None if pd.isna(parent) else str(parent)
        signature = (service, parent, int(start), int(duration))
        if key in signature_by_key:
            if signature_by_key[key] == signature:
                duplicate_rows += 1
                duplicate_N += int(in_N)
            else:
                conflict.add(key)
                if in_N or keys[key][1]:
                    conflict_N.add(key)
        else:
            signature_by_key[key] = signature
            keys[key] = (signature, bool(in_N))
    surviving = {key: row[0] for key, row in keys.items() if row[1] and key not in conflict}
    audit = {"availability": "available", "reason": None, "input_rows_N": int(before.sum()),
             "unique_effective_spans_N": len(surviving), "duplicate_rows_outer": duplicate_rows,
             "duplicate_rows_N": duplicate_N, "conflict_keys_outer": len(conflict), "conflict_keys_with_N": len(conflict_N),
             "orphan_rows": 0, "missing_parent_rows": 0, "unresolved_parent_rows": 0,
             "edges_to_conflicts_removed": 0, "self_loop_span_rows": 0,
             "signature_fields": ["serviceName", "parentSpanID", "startTime", "duration"],
             "conflict_policy": "remove full outer key before selecting N"}
    if not surviving:
        audit.update(availability="N/A", reason="insufficient_N")
        return audit, None
    adjacency = {row[0]: set() for row in surviving.values()}
    self_loop_pairs = set()
    for key, (service, parent, _start, _duration) in surviving.items():
        parent_key = (key[0], parent)
        if parent_key not in surviving:
            audit["orphan_rows"] += 1
            if parent is None or parent == "":
                audit["missing_parent_rows"] += 1
            else:
                audit["unresolved_parent_rows"] += 1
            audit["edges_to_conflicts_removed"] += int(parent_key in conflict)
            continue
        caller = surviving[parent_key][0]
        if caller == service:
            audit["self_loop_span_rows"] += 1
            self_loop_pairs.add((caller, service))
            continue
        adjacency[caller].add(service)
    incoming = {node: set() for node in adjacency}
    for caller, children in adjacency.items():
        for child in children:
            incoming[child].add(caller)
    audit.update(nodes=len(adjacency), effective_edges=sum(map(len, adjacency.values())),
                 isolated_services=sum(not adjacency[n] and not incoming[n] for n in adjacency),
                 self_loop_service_edges_removed=len(self_loop_pairs),
                 services={node: {"indegree": len(incoming[node]), "outdegree": len(adjacency[node]),
                                  "isolated": not adjacency[node] and not incoming[node]}
                           for node in sorted(adjacency)})
    return audit, adjacency


def compute_case(repo, dataset, oid, t=None, return_payload=False):
    """Compute every observed channel before any analytical root is joined."""
    began = time.perf_counter()
    payload = load_case(repo, dataset, oid, t=t)
    spans, logs = payload["spans"], payload["logs"]
    native_metric_services = {column: column.rsplit("_", 1)[0] for column in payload["metric_arrays"]}
    # P3 entity mapping is first underscore; native aggregation is last.
    metric_entities = {column: column.split("_", 1)[0] for column in native_metric_services}
    native_services = set(native_metric_services.values())
    if spans is not None:
        native_services.update(str(x) for x in spans["serviceName"])
    if logs is not None:
        native_services.update(str(x) for x in logs["container_name"])
    metrics = {}
    for column, arrays in sorted(payload["metric_arrays"].items()):
        row = metric_stats(arrays["normal"], arrays["anomalous"])
        row.update(native_service=native_metric_services[column], entity=metric_entities[column],
                   source_channel=column)
        if dataset == "Nezha-OB":
            channel_prov = payload["provenance_safe"]["channels"][column]
            row["source"] = {"path": channel_prov["source"], "column": channel_prov["source_column"]}
        else:
            row["source"] = {"path": payload["provenance_safe"]["sources"]["metrics.parquet"]["path"], "column": column}
        metrics[column] = row
    start_before, end_before = _span_splits(spans, payload["t_seconds"], dataset)
    traces_by_split = {}
    for split, mask in (("start", start_before), ("end", end_before)):
        rows = {}
        for service in sorted(native_services):
            if spans is None:
                row = trace_stats([], [])
                row.update(availability="N/A", reason="missing_channel")
                for name in ("P95N", "P95A", "vote"):
                    row[name] = feature(reason="missing_channel")
                row["latency_up"] = {str(tau): feature(reason="missing_channel") for tau in (2, 3, 4)}
            else:
                selected = spans["serviceName"] == service
                row = trace_stats(spans.loc[selected & mask, "duration"], spans.loc[selected & ~mask, "duration"])
            row.update(native_service=service, entity=service.split("_", 1)[0] if dataset == "RE2-TT" else service, split=split)
            rows[service] = row
        traces_by_split[split] = rows
    log_stats = {}
    boundary = payload["t_ns"] if dataset == "Nezha-OB" else payload["t_seconds"]
    for service in sorted(native_services):
        if logs is None:
            row = {"rows_A": feature(reason="missing_channel"), "keyword_count_A": feature(reason="missing_channel"),
                   "vote": feature(reason="missing_channel"), "availability": "N/A", "reason": "missing_channel"}
        else:
            after = logs.loc[(logs["timestamp"] >= boundary) & (logs["container_name"] == service)]
            count = sum(bool(KEYWORD.search(message)) for message in after["message"].fillna("").astype(str))
            row = {"rows_A": feature(len(after)), "keyword_count_A": feature(count), "vote": feature(int(count > 0)),
                   "availability": "available", "reason": None}
        row.update(native_service=service, entity=service.split("_", 1)[0] if dataset == "RE2-TT" else service,
                   keyword_regex="ERROR|FAIL|EXCEPTION; IGNORECASE; at most once per row")
        log_stats[service] = row
    native_totals = {}
    for service in sorted(native_services):
        mrows = [row for row in metrics.values() if row["native_service"] == service]
        unavailable_metrics = sum(row["vote"]["availability"] != "available" for row in mrows)
        metric_votes = sum(row["vote"]["value"] for row in mrows if row["vote"]["availability"] == "available")
        tr, lg = traces_by_split["start"][service]["vote"], log_stats[service]["vote"]
        # Missing channels contribute no native vote, but their absence is explicit.
        trace_vote = int(tr["value"]) if tr["availability"] == "available" else 0
        log_vote = int(lg["value"]) if lg["availability"] == "available" else 0
        score = metric_votes + trace_vote + log_vote
        native_totals[service] = {"native_service": service, "entity": service.split("_", 1)[0] if dataset == "RE2-TT" else service,
                                  "metric_events": metric_votes, "trace_vote": trace_vote, "log_vote": log_vote,
                                  "score_reconstructed": score, "local_nonpositive_reconstructed": feature(score == 0),
                                  "metric_channels": len(mrows), "metric_channels_unavailable": unavailable_metrics,
                                  "trace_available": tr["availability"] == "available", "log_available": lg["availability"] == "available",
                                  "channels_unavailable": unavailable_metrics + int(tr["availability"] != "available") + int(lg["availability"] != "available")}
    entity_max = {}
    for service, row in native_totals.items():
        entity = row["entity"]
        if entity not in entity_max:
            entity_max[entity] = {"entity": entity, "native_services": [], "score_reconstructed": row["score_reconstructed"]}
        entity_max[entity]["native_services"].append(service)
        entity_max[entity]["score_reconstructed"] = max(entity_max[entity]["score_reconstructed"], row["score_reconstructed"])
    operations = operation_stats(spans, end_before)
    operations_tracerca = operation_stats(spans, end_before, convention="tracerca")
    operation_differences = []
    for operation in operations["operations"]:
        left, right = operations["operations"][operation], operations_tracerca["operations"][operation]
        changed = {key: {"microrank": left[key], "tracerca": right[key]}
                   for key in ("muN_round", "sigmaN_round", "threshold", "abnormal_spans_A")
                   if left[key] != right[key]}
        if changed:
            operation_differences.append({"operation": operation, "differences": changed})
    graph_audit, graphs = {}, {}
    for split, mask in (("start", start_before), ("end", end_before)):
        audit, adjacency = graph_stats(spans, mask)
        audit["split"] = split
        graph_audit[split], graphs[split] = audit, adjacency
    aggregate = {"opaque_id": oid, "dataset": dataset, "label_free": True,
                 "window": payload["window"], "time_units": payload["time_unit"],
                 "provenance": payload["provenance_safe"], "metrics": metrics,
                 "trace_start": traces_by_split["start"], "trace_end": traces_by_split["end"],
                 "logs_A": log_stats, "simple_native_services": native_totals,
                 "simple_entity_max": entity_max, "operations_end": operations,
                 "operations_end_tracerca": operations_tracerca,
                 "operation_native_convention_differences": operation_differences,
                 "graph_start": graph_audit["start"], "graph_end": graph_audit["end"],
                 "cost": dict(payload["read_cost"], whole_case_seconds=time.perf_counter() - began)}
    if return_payload:
        return aggregate, graphs, payload
    return aggregate, graphs
