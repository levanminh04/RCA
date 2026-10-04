"""Extract a readable worked example from already saved, verified predictions.

This is reporting, not another MicroRank run. It imports no author module.
The representative operation is the highest scoring operation present in BOTH
groups; representative traces are lexicographically first in each group.
Neither selection uses the fault label. Root service is inspected afterwards.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import struct


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--math-dir", type=Path, required=True)
    parser.add_argument("--primary-summary", type=Path, required=True)
    parser.add_argument("--inputs-dir", type=Path, required=True)
    parser.add_argument("--root-service", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.snapshot.read_bytes()
    snapshot = json.loads(raw)
    arithmetic = load(args.math_dir / "summary.json")
    if hashlib.sha256(raw).hexdigest() != arithmetic["input_sha256"]:
        raise ValueError("Snapshot differs from the snapshot independently calculated")
    if not arithmetic["all_passed"] or not arithmetic["spectrum_nonnegative"]:
        raise ValueError("Arithmetic verification did not pass")
    primary = load(args.primary_summary)
    inputs = load(args.inputs_dir / "comparison.json")
    if not inputs["all_passed"] or not all(inputs["checks"].values()):
        raise ValueError("Independent raw-input reconstruction did not pass")
    operation_services = snapshot["operation_services"]

    def f32(value):
        return struct.unpack("f", struct.pack("f", value))[0]
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError("Keep prior extraction: output is not empty")
    args.output.mkdir(parents=True, exist_ok=True)

    score_rows = csv_rows(args.math_dir / "spectrum-scores.csv")
    normal_ops = snapshot["groups"]["normal"]["graph"]["operation_operation"]
    anomaly_ops = snapshot["groups"]["anomaly"]["graph"]["operation_operation"]
    representative = next(row["operation"] for row in score_rows
                          if row["operation"] in normal_ops and row["operation"] in anomaly_ops)
    extracted = {
        "snapshot_path": str(args.snapshot),
        "snapshot_sha256": arithmetic["input_sha256"],
        "prediction_saved_before_root_inspection": True,
        "representative_operation_rule": "highest saved score among operations present in both groups; no fault label",
        "representative_operation": representative,
        "snapshot_keys": list(snapshot), "primary_summary_keys": list(primary),
        "primary_summary": primary,
        "inventory_count_summary": {key: len(value) for key, value in primary["inventory"].items()
                                    if isinstance(value, list)},
        "independent_inputs_check": inputs,
        "arithmetic": {key: arithmetic[key] for key in (
            "n_comparisons", "all_passed", "max_absolute_error", "max_relative_error", "spectrum_nonnegative")},
        "groups": {}, "top11": score_rows[:11],
    }
    for name in ("normal", "anomaly"):
        group = snapshot["groups"][name]
        graph = group["graph"]
        calls = graph["operation_operation"]
        traces = graph["operation_trace"]
        op_traces = graph["trace_operation"]
        spans = graph["pr_trace"]
        signature_counts = Counter(tuple(sorted(ops)) for ops in traces.values())
        kind_count = {trace: signature_counts[tuple(sorted(ops))] for trace, ops in traces.items()}
        inverse_kind_sum = sum(1 / kind_count[trace] for trace in spans)
        inverse_scope_sum = sum(1 / len(spans[trace]) for trace in spans)
        selected_trace = min(traces)
        iteration = csv_rows(args.math_dir / f"{name}-iterations.csv")
        operation_rows = csv_rows(args.math_dir / f"{name}-operations.csv")
        trace_rows = csv_rows(args.math_dir / f"{name}-traces.csv")
        selected_op = next(row for row in operation_rows if row["operation"] == representative)
        selected_trace_row = next(row for row in trace_rows if row["trace"] == selected_trace)
        selected_trace_row["preference_float32_full"] = arithmetic["group_intermediates"][name]["prior"][selected_trace]
        initial = 1 / (len(calls) + len(traces))
        coverage_column_sum = sum(f32(1 / len(traces[trace])) for trace in op_traces[representative])
        incoming = [source for source, targets in calls.items() if representative in targets]
        call_row_sum = sum(f32(1 / len(calls[source])) for source in incoming)
        first_operation_numerator = .85 * initial * (coverage_column_sum + .01 * call_row_sum)
        first_operation_normalized = first_operation_numerator / float(iteration[0]["operation_max_before_normalization"])
        first_trace_numerator = .85 * initial * sum(f32(1 / len(op_traces[op])) for op in traces[selected_trace]) + (1-.85) * selected_trace_row["preference_float32_full"]
        first_trace_normalized = first_trace_numerator / float(iteration[0]["trace_max_before_normalization"])
        edges = [{"source": source, "target": target, "source_out_degree": len(targets),
                  "A_entry_before_float32_quantization": 1 / len(targets)}
                 for source, targets in calls.items() for target in targets]
        write_csv(args.output / f"{name}-operation-edges.csv", edges)
        extracted["groups"][name] = {
            "operation_count": len(calls), "trace_count": len(traces),
            "edge_count": len(edges), "span_occurrence_count": sum(map(len, spans.values())),
            "kind_count": len(signature_counts), "inverse_kind_sum_K": inverse_kind_sum,
            "inverse_span_count_sum_S": inverse_scope_sum,
            "representative_trace": selected_trace_row,
            "representative_trace_operations": traces[selected_trace],
            "representative_operation": selected_op,
            "representative_operation_children": calls[representative],
            "representative_operation_parents": incoming,
            "representative_first_iteration": {
                "initial_each_entry": initial, "B_row_sum": coverage_column_sum,
                "A_row_sum": call_row_sum,
                "operation_before_normalization": first_operation_numerator,
                "operation_after_normalization": first_operation_normalized,
                "trace_before_normalization": first_trace_numerator,
                "trace_after_normalization": first_trace_normalized,
                "note": "Matrix entries quantized float32 before summing; displayed first-round algebra may differ at final floating-point bits from BLAS dot order. All exact final points are certified in comparison.csv"},
            "iteration1": iteration[0], "iteration25": iteration[-1],
            "normalization": arithmetic["group_intermediates"][name]["normalization"],
            "audit": group.get("audit"),
        }

    # Label is used here only, after all saved predictions have been verified.
    root_rows = [row for row in score_rows if operation_services[row["operation"]] == args.root_service]
    service_order = []
    for row in score_rows:
        service = operation_services[row["operation"]]
        if service not in service_order:
            service_order.append(service)
    extracted["after_prediction_root_inspection"] = {
        "root_service": args.root_service,
        "root_operations": root_rows,
        "full_service_rank": service_order.index(args.root_service) + 1 if args.root_service in service_order else None,
        "top11_service_order": list(dict.fromkeys(operation_services[row["operation"]] for row in score_rows[:11])),
    }
    (args.output / "example-extract.json").write_text(json.dumps(extracted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"representative_operation": representative, "arithmetic": extracted["arithmetic"],
                      "root_inspection": extracted["after_prediction_root_inspection"]}, ensure_ascii=True))


if __name__ == "__main__":
    main()
