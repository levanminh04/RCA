"""T-002: schema, observed graph and exploratory metric excursions.

Only data/rcaeval is readable. This is dataset inspection, not an RCA method.
Root/fault names are attached to reporting only, after signal-only calculations.
Every invocation creates a new run directory, including on failure.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import re
import sys
import traceback
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data" / "rcaeval"
OUT = Path(__file__).resolve().parent / "local-inspection"
REVISION = "afeacb11bcc94dadfd1c8f483ee4377b2b8b614e"
QUANTILES = (0.95, 0.99, 0.995)
TARGETS = ("re2tt", "re2ob", "re3tt", "re3ob")


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def table(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def safe_file(path):
    path = path.resolve(strict=True)
    if not path.is_relative_to(DATA.resolve()) or "locked" in path.parts:
        raise ValueError(f"Not an allowed input: {path}")
    return path


def injection(case, run):
    local = case / "inject_time.txt"
    if local.exists():
        raw = safe_file(local).read_bytes()
        source = str(local.relative_to(REPO)).replace("\\", "/")
    else:
        source = f"https://huggingface.co/datasets/phamquiluan/RCAEval/resolve/{REVISION}/{case.name}/inject_time.txt"
        with urlopen(Request(source, headers={"User-Agent": "T-002-dataset-inspection"}), timeout=45) as response:
            raw = response.read(1024)
        (run / "injection-metadata" / f"{case.name}.txt").write_bytes(raw)
    value = int(raw.decode().strip())
    return value, {"case": case.name, "source": source, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def inspect_trace(path, inject_time):
    schema = pq.read_schema(safe_file(path))
    names = schema.names
    cols = [c for c in ("traceID", "spanID", "parentSpanID", "serviceName", "operationName", "startTime", "startTimeMillis", "duration", "statusCode") if c in names]
    frame = pd.read_parquet(path, columns=cols)
    keys = frame[["traceID", "spanID"]]
    valid_key = keys.notna().all(axis=1) & keys.ne("").all(axis=1)
    duplicates = int(keys.loc[valid_key].duplicated(keep=False).sum())
    service_conflicts = frame.loc[valid_key].groupby(["traceID", "spanID"])["serviceName"].nunique()
    ambiguous_keys = service_conflicts[service_conflicts > 1].index
    parent_lookup = frame.loc[valid_key, ["traceID", "spanID", "serviceName"]].drop_duplicates(["traceID", "spanID"])
    parent_lookup = parent_lookup.set_index(["traceID", "spanID"])["serviceName"]
    parent_text = frame["parentSpanID"].fillna("").astype(str)
    reference = ~parent_text.str.fullmatch(r"(?:|0+|None|null)", case=False)
    parent_pairs = pd.MultiIndex.from_arrays([frame["traceID"], frame["parentSpanID"]])
    resolved = reference & parent_pairs.isin(parent_lookup.index)
    unambiguous = resolved & ~parent_pairs.isin(ambiguous_keys)
    parent_service = parent_lookup.reindex(parent_pairs).reset_index(drop=True)
    child_service = frame["serviceName"].reset_index(drop=True)
    epoch = frame["startTimeMillis"] / 1000 if "startTimeMillis" in names else frame["startTime"] / 1_000_000
    graphs = {}
    for window, mask in (("full", np.ones(len(frame), dtype=bool)), ("pre_injection", np.asarray(epoch < inject_time))):
        nodes = sorted(child_service.loc[mask].dropna().unique().tolist())
        edge_mask = mask & unambiguous & parent_service.notna() & child_service.notna() & parent_service.ne(child_service)
        edges = sorted(set(zip(parent_service.loc[edge_mask], child_service.loc[edge_mask])))
        degrees = [{"service": node, "in_degree": sum(dst == node for src, dst in edges), "out_degree": sum(src == node for src, dst in edges)} for node in nodes]
        graphs[window] = {"nodes": nodes, "edges": [list(e) for e in edges], "degrees": degrees}
    status = frame["statusCode"] if "statusCode" in names else pd.Series(dtype=float)
    nonempty_parent = int(reference.sum())
    start_relation = None
    if "startTime" in names and "startTimeMillis" in names:
        difference = (frame["startTime"] // 1000 - frame["startTimeMillis"])
        start_relation = {"startTime_div_1000_minus_startTimeMillis_min": int(difference.min()), "max": int(difference.max())}
    return {
        "n_spans": len(frame), "n_services": frame["serviceName"].nunique(),
        "n_operations": int(frame[["serviceName", "operationName"]].drop_duplicates().shape[0]),
        "parent_reference_count": nonempty_parent, "root_or_empty_parent_count": int((~reference).sum()),
        "parent_resolved_count": int(resolved.sum()), "parent_unresolved_count": int((reference & ~resolved).sum()),
        "parent_resolution_fraction": float(resolved.sum() / nonempty_parent) if nonempty_parent else None,
        "duplicate_key_rows": duplicates, "conflicting_service_keys": len(ambiguous_keys),
        "status_nonnull": int(status.notna().sum()), "status_nonzero": int((status.fillna(0) != 0).sum()),
        "duration_null": int(frame["duration"].isna().sum()), "duration_negative": int((frame["duration"] < 0).sum()),
        "epoch_min": float(epoch.min()), "epoch_max": float(epoch.max()),
        "start_field_relation": start_relation, "graphs": graphs,
        "typed_span_kind_column": any(c.lower() in ("spankind", "span_kind", "kind") for c in names),
    }


def inspect_log(path):
    frame = pd.read_parquet(safe_file(path))
    direct_columns = [c for c in frame if re.sub(r"[_-]", "", c.lower()) in ("traceid", "spanid", "traceparent")]
    messages = frame["message"].fillna("").astype(str) if "message" in frame else pd.Series(dtype=str)
    # Counts mention vs recognizable ID separately. Neither certifies a request join.
    mention = messages.str.contains(r"trace[_-]?id|span[_-]?id|traceparent", case=False, regex=True)
    id_pattern = r"(?:trace[_-]?id|span[_-]?id)[\"']?\s*[:=]\s*[\"']?[0-9a-f]{16,32}\b|traceparent[\"']?\s*[:=]\s*[\"']?\d{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}"
    id_like = messages.str.contains(id_pattern, case=False, regex=True)
    return {"n_logs": len(frame), "trace_or_span_id_columns": direct_columns,
            "id_key_mentions": int(mention.sum()), "recognized_id_pattern_rows": int(id_like.sum()),
            "entities": sorted(frame["container_name"].dropna().unique().tolist()) if "container_name" in frame else [],
            "timestamp_min": int(frame["timestamp"].min()) if "timestamp" in frame and len(frame) else None,
            "timestamp_max": int(frame["timestamp"].max()) if "timestamp" in frame and len(frame) else None}


def metric_excursions(frame, boundary):
    """No root, fault, case name, graph, or dataset label is accepted here.

    Known injection boundary separates two descriptive regimes; this does not
    detect onset. First 2/3 of pre-injection rows fit metric bands; last 1/3 are
    a normal control. All channels use the same rule before reporting roots.
    """
    ordered = frame.sort_values("time")
    before = ordered.loc[ordered.time < boundary]
    after = ordered.loc[ordered.time >= boundary]
    cut = 2 * len(before) // 3
    reference, control = before.iloc[:cut], before.iloc[cut:]
    rows, diagnostics = [], []
    if len(reference) < 30 or len(control) < 10 or len(after) < 10:
        return rows, diagnostics, {"status": "chưa kiểm: thiếu hàng ở một cửa sổ"}
    numeric = [c for c in frame.select_dtypes(include="number") if c != "time"]
    entities = defaultdict(list)
    for col in numeric:
        if "_" in col:
            entities[col.rsplit("_", 1)[0]].append(col)
    for q in QUANTILES:
        flags_control, flags_after = {}, {}
        for col in numeric:
            valid = reference[col].replace([np.inf, -np.inf], np.nan).dropna()
            if len(valid) < 30:
                continue
            center = float(valid.median())
            band = float((valid - center).abs().quantile(q))
            flags_control[col] = (control[col] - center).abs() > band
            flags_after[col] = (after[col] - center).abs() > band
            diagnostics.append({"metric": col, "q": q, "reference_valid_rows": len(valid),
                                "median": center, "absolute_deviation_band": band,
                                "flat_band": band == 0, "control_valid_rows": int(control[col].notna().sum()),
                                "post_valid_rows": int(after[col].notna().sum()),
                                "control_exceed_rows": int(flags_control[col].sum()), "post_exceed_rows": int(flags_after[col].sum())})
        for entity, cols in entities.items():
            for group, selected in (("all_metrics", cols), ("latency90", [c for c in cols if c.endswith("_latency-90")])):
                selected = [c for c in selected if c in flags_after]
                if not selected:
                    continue
                cflags = pd.concat([flags_control[c] for c in selected], axis=1).any(axis=1)
                aflags = pd.concat([flags_after[c] for c in selected], axis=1).any(axis=1)
                # Exclude rows missing every selected channel from rate denominators.
                cvalid = control[selected].notna().any(axis=1)
                avalid = after[selected].notna().any(axis=1)
                rows.append({"q": q, "signal_group": group, "entity": entity, "channels": len(selected),
                             "control_valid_rows": int(cvalid.sum()), "post_valid_rows": int(avalid.sum()),
                             "control_exceed_rows": int((cflags & cvalid).sum()), "post_exceed_rows": int((aflags & avalid).sum()),
                             "control_exceed_rate": float(cflags[cvalid].mean()) if cvalid.any() else None,
                             "post_exceed_rate": float(aflags[avalid].mean()) if avalid.any() else None})
    return rows, diagnostics, {"status": "exploratory_only", "normal_rows": len(before), "post_rows": len(after),
                              "reference_rows": len(reference), "control_rows": len(control)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="smoke check; never overwrites a previous run")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    run = OUT / f"run-{1 + len(list(OUT.glob('run-*'))):03d}"
    run.mkdir()
    (run / "injection-metadata").mkdir()
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
                "pandas": pd.__version__, "pyarrow": pa.__version__, "numpy": np.__version__,
                "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "hf_revision": REVISION, "argv": sys.argv, "inputs": [], "injections": [], "status": "running"}
    dump(run / "manifest.json", manifest)
    schemas, cases, entities, channel_rows, graph_rows = {}, [], [], [], []
    try:
        directories = sorted(p for p in DATA.iterdir() if p.is_dir())
        if args.limit:
            directories = directories[:args.limit]
        for directory in directories:
            safe_file(directory)
            case_name = directory.name
            dataset, root, fault, repeat = case_name.split("_", 3)
            inject_time, injection_manifest = injection(directory, run)
            manifest["injections"].append(injection_manifest)
            record = {"case": case_name, "dataset": dataset, "root": root, "fault": fault, "repeat": int(repeat), "inject_time": inject_time}
            for modality in ("metrics", "traces", "logs"):
                path = directory / f"{modality}.parquet"
                record[f"has_{modality}"] = path.exists()
                if not path.exists():
                    continue
                safe_file(path)
                parquet = pq.ParquetFile(path)
                manifest["inputs"].append({"path": str(path.relative_to(REPO)).replace("\\", "/"), "bytes": path.stat().st_size, "rows": parquet.metadata.num_rows})
                schemas[f"{case_name}/{modality}.parquet"] = [{"name": field.name, "type": str(field.type)} for field in parquet.schema_arrow]
                record[f"{modality}_bytes"] = path.stat().st_size
            metrics = pd.read_parquet(directory / "metrics.parquet")
            before = metrics.time < inject_time
            record.update({"n_metric_rows": len(metrics), "n_metric_columns": len(metrics.columns) - 1,
                           "metric_missing_values": int(metrics.drop(columns="time").isna().sum().sum()),
                           "metric_time_min": int(metrics.time.min()), "metric_time_max": int(metrics.time.max()),
                           "normal_rows": int(before.sum()), "post_rows": int((~before).sum()),
                           "normal_duration_to_injection_seconds": int(inject_time - metrics.time.min()),
                           "metric_duplicate_times": int(metrics.time.duplicated().sum()),
                           "metric_step_seconds": sorted(metrics.time.sort_values().diff().dropna().unique().tolist())})
            if record["has_traces"]:
                trace = inspect_trace(directory / "traces.parquet", inject_time)
                record["trace"] = trace
                for window, graph in trace["graphs"].items():
                    for degree in graph["degrees"]:
                        graph_rows.append({"case": case_name, "dataset": dataset, "root": root, "fault": fault,
                                           "window": window, "is_root": degree["service"] == root, **degree})
            if record["has_logs"]:
                record["log"] = inspect_log(directory / "logs.parquet")
            if dataset in TARGETS:
                signal_rows, diagnostics, window = metric_excursions(metrics, inject_time)
                record["probe_window"] = window
                for row in signal_rows:
                    # This reporting annotation cannot affect upstream scores or bands.
                    entity = row["entity"]
                    business = entity.endswith("service") or entity == "frontend"
                    entities.append({"case": case_name, "dataset": dataset, "root": root, "fault": fault,
                                     "repeat": int(repeat), "is_root": entity == root,
                                     "business_name_heuristic": business, **row})
                channel_rows.extend({"case": case_name, **row} for row in diagnostics)
            cases.append(record)
            dump(run / "cases.json", cases)
            print(f"{case_name}: schema/graph/windows inspected", flush=True)
        dump(run / "schemas.json", schemas)
        table(run / "graph-degrees.csv", graph_rows)
        table(run / "symptom-entity-rates.csv", entities)
        table(run / "symptom-channel-bands.csv", channel_rows)
        flat = [{k: v for k, v in r.items() if k not in ("trace", "log", "probe_window")} for r in cases]
        table(run / "case-summary.csv", flat)
        manifest["status"] = "complete"
    except Exception:
        manifest["status"] = "failed"
        (run / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        dump(run / "manifest.json", manifest)
    print(f"Outputs: {run}", flush=True)


if __name__ == "__main__":
    main()
