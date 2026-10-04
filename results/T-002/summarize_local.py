"""Derive card numbers from a specified completed inspection run; no telemetry."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent


def write_table(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["no_rows"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run")
    args = parser.parse_args()
    run = Path(args.run).resolve(strict=True)
    assert run.is_relative_to(HERE.resolve())
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    cases = json.loads((run / "cases.json").read_text(encoding="utf-8"))
    rates = pd.read_csv(run / "symptom-entity-rates.csv")
    # Annotation/filtering here serves descriptions, never changes upstream bands.
    other = rates.loc[~rates.is_root & rates.business_name_heuristic]
    by_case = []
    for key, group in other.groupby(["case", "dataset", "root", "fault", "repeat", "q", "signal_group"]):
        result = dict(zip(["case", "dataset", "root", "fault", "repeat", "q", "signal_group"], key))
        result.update({"n_other_services_with_channels": len(group),
                       "control_mean_service_rate": float(group.control_exceed_rate.mean()),
                       "post_mean_service_rate": float(group.post_exceed_rate.mean()),
                       "control_max_service_rate": float(group.control_exceed_rate.max()),
                       "post_max_service_rate": float(group.post_exceed_rate.max()),
                       "delta_mean_rate": float(group.post_exceed_rate.mean() - group.control_exceed_rate.mean())})
        by_case.append(result)
    write_table(run / "probe-case-summary.csv", by_case)
    probe_cases = pd.DataFrame(by_case)
    by_cell = []
    for key, group in probe_cases.groupby(["dataset", "root", "fault", "q", "signal_group"]):
        result = dict(zip(["dataset", "root", "fault", "q", "signal_group"], key))
        result.update({"n_repeats": len(group), "control_rate_mean": float(group.control_mean_service_rate.mean()),
                       "post_rate_mean": float(group.post_mean_service_rate.mean()),
                       "delta_min": float(group.delta_mean_rate.min()), "delta_max": float(group.delta_mean_rate.max())})
        by_cell.append(result)
    write_table(run / "probe-cell-summary.csv", by_cell)
    positions = []
    summaries = {}
    for dataset in ("re2tt", "re2ob", "re3tt", "re3ob"):
        group = [c for c in cases if c["dataset"] == dataset]
        traces = [c["trace"] for c in group if "trace" in c]
        logs = [c["log"] for c in group if "log" in c]
        ref = sum(t["parent_reference_count"] for t in traces)
        resolved = sum(t["parent_resolved_count"] for t in traces)
        topology = {}
        for window in ("pre_injection", "full"):
            signatures = {}
            for c in group:
                if "trace" not in c:
                    continue
                graph = c["trace"]["graphs"][window]
                signature = json.dumps([graph["nodes"], graph["edges"]], sort_keys=True)
                row = signatures.setdefault(signature, {"nodes": len(graph["nodes"]), "edges": len(graph["edges"]), "n_cases": 0})
                row["n_cases"] += 1
                for degree in graph["degrees"]:
                    positions.append({"dataset": dataset, "case": c["case"], "window": window, **degree})
            topology[window] = list(signatures.values())
        summaries[dataset] = {
            "n_inspected": len(group), "n_trace_cases": len(traces), "n_log_cases": len(logs),
            "n_spans": sum(t["n_spans"] for t in traces), "parent_reference_count": ref,
            "parent_resolved_count": resolved, "parent_unresolved_count": ref - resolved,
            "root_or_empty_parent_count": sum(t["root_or_empty_parent_count"] for t in traces),
            "parent_resolution_fraction": resolved / ref if ref else None,
            "parent_fraction_min": min((t["parent_resolution_fraction"] for t in traces), default=None),
            "parent_fraction_max": max((t["parent_resolution_fraction"] for t in traces), default=None),
            "duplicate_key_rows": sum(t["duplicate_key_rows"] for t in traces),
            "conflicting_service_keys": sum(t["conflicting_service_keys"] for t in traces),
            "duration_negative": sum(t["duration_negative"] for t in traces),
            "duration_null": sum(t["duration_null"] for t in traces),
            "status_nonnull": sum(t["status_nonnull"] for t in traces), "status_nonzero": sum(t["status_nonzero"] for t in traces),
            "n_services_min": min((t["n_services"] for t in traces), default=None),
            "n_services_max": max((t["n_services"] for t in traces), default=None),
            "n_logs": sum(t["n_logs"] for t in logs), "id_key_mentions": sum(t["id_key_mentions"] for t in logs),
            "recognized_id_pattern_rows": sum(t["recognized_id_pattern_rows"] for t in logs),
            "direct_trace_id_columns": sorted(set(k for t in logs for k in t["trace_or_span_id_columns"])),
            "normal_rows_min": min((c["normal_rows"] for c in group), default=None),
            "normal_rows_max": max((c["normal_rows"] for c in group), default=None),
            "post_rows_min": min((c["post_rows"] for c in group), default=None),
            "post_rows_max": max((c["post_rows"] for c in group), default=None),
            "metric_columns_min": min((c["n_metric_columns"] for c in group), default=None),
            "metric_columns_max": max((c["n_metric_columns"] for c in group), default=None),
            "metric_missing_values": sum(c["metric_missing_values"] for c in group),
            "metric_duplicate_times": sum(c["metric_duplicate_times"] for c in group),
            "metric_steps": sorted(set(step for c in group for step in c["metric_step_seconds"])),
            "inspected_bytes": sum(i["bytes"] for i in manifest["inputs"] if i["path"].split("/")[2].startswith(dataset + "_")),
            "topology": topology,
        }
    (run / "summary.json").write_text(json.dumps(summaries, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    write_table(run / "all-service-positions.csv", positions)
    assert len(cases) == 35, "full run must contain 30 dev + 5 auxiliary cases"
    assert summaries["re2tt"]["n_inspected"] == 30
    assert len(probe_cases) == 32 * 3 * 2
    assert all(s["duplicate_key_rows"] == 0 and s["conflicting_service_keys"] == 0 for s in summaries.values())
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
