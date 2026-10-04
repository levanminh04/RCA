"""Recompute MicroRank intermediates without importing any author function.

Input is an adapter snapshot. Dictionary insertion order defines the official
operation/trace order; no label or path-derived service enters the computation.
The historical graph names are retained: operation_trace maps TRACE to OPERATION,
trace_operation maps OPERATION to TRACE. Matrices/prior are float32 because the
official source quantizes them; evolving vectors are float64.

Usage:
  python -B independent_math.py snapshot.json --output runs/independent-math/case
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import datetime
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("khong co\n", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def jsonable(value):
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [jsonable(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def recompute_group(group: dict, anomalous: bool, options: dict) -> dict:
    """Build incidence matrices, trace preference, both ranking vectors, weights."""
    graph = group["graph"]
    calls = graph["operation_operation"]
    trace_cover = graph["operation_trace"]
    operation_cover = graph["trace_operation"]
    span_operations = graph["pr_trace"]
    operations, traces = list(calls), list(trace_cover)
    if not operations or not traces:
        raise ValueError("Independent PageRank requires a nonempty group")
    op_index = {name: i for i, name in enumerate(operations)}
    trace_index = {name: i for i, name in enumerate(traces)}
    m, n = len(operations), len(traces)
    if set(operations) != set(operation_cover):
        raise ValueError("Operation node sets disagree across graph dictionaries")
    if set(traces) != set(span_operations):
        raise ValueError("Trace node sets disagree between coverage and pr_trace")

    # Columns are sources and rows are destinations, independently indexed.
    call_matrix = np.zeros((m, m), dtype=np.float32)
    trace_to_op = np.zeros((m, n), dtype=np.float32)
    op_to_trace = np.zeros((n, m), dtype=np.float32)
    for source, targets in calls.items():
        if len(targets) != len(set(targets)):
            raise ValueError("Duplicate operation edge")
        for target in targets:
            call_matrix[op_index[target], op_index[source]] = 1 / len(targets)
    for trace, covered in trace_cover.items():
        if not covered or len(covered) != len(set(covered)):
            raise ValueError("Trace coverage must be nonempty and deduplicated")
        for operation in covered:
            trace_to_op[op_index[operation], trace_index[trace]] = 1 / len(covered)
            if trace not in operation_cover[operation]:
                raise ValueError("Missing inverse coverage incidence")
    for operation, covered in operation_cover.items():
        if not covered or len(covered) != len(set(covered)):
            raise ValueError("Operation coverage must be nonempty and deduplicated")
        for trace in covered:
            op_to_trace[trace_index[trace], op_index[operation]] = 1 / len(covered)
            if operation not in trace_cover[trace]:
                raise ValueError("Spurious inverse coverage incidence")
    for trace, repeated_ops in span_operations.items():
        if not repeated_ops or set(repeated_ops) != set(trace_cover[trace]):
            raise ValueError("pr_trace disagrees with coverage or is empty")

    # Equal columns define the trace kind in the source implementation. Counting
    # signatures avoids its quadratic equality loop without changing definition.
    signatures = [trace_to_op[:, i].tobytes() for i in range(n)]
    counts = Counter(signatures)
    kinds = np.asarray([counts[key] for key in signatures], dtype=np.float64)
    preference = np.zeros((n, 1), dtype=np.float32)
    inverse_kind_sum = np.float64(0)
    inverse_span_sum = np.float64(0)
    for trace in span_operations:
        inverse_kind_sum += 1 / kinds[trace_index[trace]]
        inverse_span_sum += 1 / len(span_operations[trace])
    for trace, repeated_ops in span_operations.items():
        i = trace_index[trace]
        if anomalous:
            # This is the pinned CODE expression. Paper eq7 instead adds two
            # normalized inverses, and is deliberately not substituted here.
            inverse_denominator = 0.5 * kinds[i] / inverse_kind_sum + 1 / len(repeated_ops)
            preference[i, 0] = 0.5 / inverse_denominator / inverse_span_sum
        else:
            preference[i, 0] = 1 / kinds[i] / inverse_kind_sum

    damping = float(options.get("d", options.get("damping", 0.85)))
    alpha = float(options.get("alpha", 0.01))
    iterations = int(options.get("iterations", 25))
    op_vector = np.full((m, 1), 1 / (m + n), dtype=np.float64)
    trace_vector = np.full((n, 1), 1 / (m + n), dtype=np.float64)
    iteration_rows = []
    for turn in range(1, iterations + 1):
        # Synchronous updates use BOTH previous vectors before normalization.
        next_op = damping * (trace_to_op @ trace_vector + alpha * (call_matrix @ op_vector))
        next_trace = damping * (op_to_trace @ op_vector) + (1 - damping) * preference
        op_max, trace_max = float(next_op.max()), float(next_trace.max())
        if op_max <= 0 or trace_max <= 0:
            raise ValueError("Zero/negative max during ranking update")
        next_op /= op_max
        next_trace /= trace_max
        iteration_rows.append({
            "iteration": turn,
            "operation_max_before_normalization": op_max,
            "trace_max_before_normalization": trace_max,
            "operation_max_absolute_change": float(np.max(np.abs(next_op - op_vector))),
            "trace_max_absolute_change": float(np.max(np.abs(next_trace - trace_vector))),
        })
        op_vector, trace_vector = next_op, next_trace

    op_vector /= op_vector.max()
    op_sum = np.float64(0)
    for i in range(m):
        op_sum += op_vector[i, 0]
    weights = {operation: op_vector[i, 0] * op_sum / m for i, operation in enumerate(operations)}
    tracecounts = {operation: int(np.count_nonzero(trace_to_op[i])) for i, operation in enumerate(operations)}
    trace_rows = [{
        "trace": trace,
        "kind_count": kinds[i],
        "unique_operation_count": len(trace_cover[trace]),
        "span_operation_count": len(span_operations[trace]),
        "preference_float32": preference[i, 0],
        "trace_pagerank": trace_vector[i, 0],
    } for i, trace in enumerate(traces)]
    operation_rows = [{
        "operation": operation,
        "operation_pagerank": op_vector[i, 0],
        "operation_weight": weights[operation],
        "trace_count": tracecounts[operation],
        "operation_out_degree": len(calls[operation]),
    } for i, operation in enumerate(operations)]
    return {"weights": weights, "tracecounts": tracecounts,
            "prior": {trace: preference[i, 0] for i, trace in enumerate(traces)},
            "operation_pagerank": {op: op_vector[i, 0] for i, op in enumerate(operations)},
            "trace_pagerank": {trace: trace_vector[i, 0] for i, trace in enumerate(traces)},
            "operation_rows": operation_rows, "trace_rows": trace_rows,
            "iteration_rows": iteration_rows,
            "matrix_shapes": {"call": [m, m], "trace_to_op": [m, n], "op_to_trace": [n, m]},
            "matrix_nonzeros": {"call": int(np.count_nonzero(call_matrix)),
                                "trace_to_op": int(np.count_nonzero(trace_to_op)),
                                "op_to_trace": int(np.count_nonzero(op_to_trace))},
            "normalization": {"operation_pagerank_sum": op_sum,
                              "weight_scale": op_sum / m,
                              "prior_sum": float(preference.sum())}}


def recompute_spectrum(normal: dict, anomaly: dict, normal_total: int, anomaly_total: int):
    """Pinned Dstar2 spectrum including the source's asymmetric absent branches."""
    epsilon = 0.0000001
    spectrum = {}
    for operation, weight in anomaly["weights"].items():
        covered = anomaly["tracecounts"][operation]
        cells = {"ef": weight * covered, "nf": weight * (anomaly_total - covered)}
        if operation in normal["weights"]:
            normal_weight = normal["weights"][operation]
            normal_covered = normal["tracecounts"][operation]
            cells.update(ep=normal_weight * normal_covered,
                         np=normal_weight * (normal_total - normal_covered))
        else:
            cells.update(ep=epsilon, np=epsilon)
        spectrum[operation] = cells
    for operation, weight in normal["weights"].items():
        if operation not in spectrum:
            covered = normal["tracecounts"][operation]
            spectrum[operation] = {"ep": (1 + weight) * covered,
                                   "np": normal_total - covered,
                                   "ef": epsilon, "nf": epsilon}
    scores = {operation: cells["ef"] ** 2 / (cells["ep"] + cells["nf"])
              for operation, cells in spectrum.items()}
    return spectrum, scores


def compare_mapping(actual: dict, expected: dict, section: str, rows: list, tolerance: float):
    if set(actual) != set(expected):
        raise ValueError(f"{section} keys differ: actual-only={set(actual)-set(expected)}, expected-only={set(expected)-set(actual)}")
    for key, value in actual.items():
        if isinstance(value, dict):
            compare_mapping(value, expected[key], f"{section}.{key}", rows, tolerance)
        else:
            reference = float(expected[key])
            error = abs(float(value) - reference)
            relative = 0.0 if error == 0 else error / max(abs(reference), abs(float(value)), sys.float_info.min)
            finite = bool(np.isfinite(value) and np.isfinite(reference))
            rows.append({"section": section, "key": key, "independent": float(value),
                         "official": reference, "absolute_error": error,
                         "relative_error": relative,
                         "passed": finite and error <= tolerance and relative <= tolerance})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=1e-10)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    payload = json.loads(raw)
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError(f"Preserve prior run: output is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()

    def progress(event: str, **details):
        record = {"event": event, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  "elapsed_seconds": time.monotonic() - start, "timing_official": False, **details}
        with (args.output / "progress.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    progress("independent_math_start", case_id=payload.get("case_id"), input_sha256=hashlib.sha256(raw).hexdigest())
    groups, comparisons = {}, []
    for name in ("normal", "anomaly"):
        progress("group_start", group=name)
        group = payload["groups"][name]
        independent = recompute_group(group, name == "anomaly", payload.get("options", {}))
        groups[name] = independent
        for field in ("weights", "tracecounts"):
            compare_mapping(independent[field], group["official"][field], f"{name}.{field}", comparisons, args.tolerance)
        for field in ("prior", "operation_pagerank", "trace_pagerank"):
            if field in group["official"]:
                compare_mapping(independent[field], group["official"][field], f"{name}.{field}", comparisons, args.tolerance)
        if "service_vector" in group["official"]:
            compare_mapping(independent["operation_pagerank"], group["official"]["service_vector"],
                            f"{name}.operation_pagerank", comparisons, args.tolerance)
        write_csv(args.output / f"{name}-operations.csv", independent["operation_rows"])
        write_csv(args.output / f"{name}-traces.csv", independent["trace_rows"])
        write_csv(args.output / f"{name}-iterations.csv", independent["iteration_rows"])
        progress("group_end", group=name, matrix_shapes=independent["matrix_shapes"])
    spectrum, scores = recompute_spectrum(
        groups["normal"], groups["anomaly"],
        int(payload["groups"]["normal"]["trace_count"]),
        int(payload["groups"]["anomaly"]["trace_count"]))
    compare_mapping(spectrum, payload["spectrum"], "spectrum", comparisons, args.tolerance)
    compare_mapping(scores, payload["scores"], "scores", comparisons, args.tolerance)
    write_csv(args.output / "comparison.csv", comparisons)
    ordered = sorted(scores, key=lambda name: (-scores[name], name))
    write_csv(args.output / "spectrum-scores.csv", [{"operation": name, **spectrum[name],
                                                   "score": scores[name], "rank": i}
                                                  for i, name in enumerate(ordered, 1)])
    summary = {
        "case_id": payload.get("case_id"), "variant": payload.get("variant"),
        "input_path": str(args.input.resolve()), "input_sha256": hashlib.sha256(raw).hexdigest(),
        "tolerance_absolute_and_relative": args.tolerance,
        "n_comparisons": len(comparisons),
        "all_passed": all(row["passed"] for row in comparisons),
        "max_absolute_error": max(row["absolute_error"] for row in comparisons),
        "max_relative_error": max(row["relative_error"] for row in comparisons),
        "no_author_function_imported": True,
        "group_intermediates": {name: {k: v for k, v in group.items()
                                      if k not in ("operation_rows", "trace_rows", "iteration_rows")}
                               for name, group in groups.items()},
        "scores": scores, "spectrum": spectrum,
        "spectrum_nonnegative": all(value >= 0 for cells in spectrum.values() for value in cells.values()),
        "scope": "Exact pinned code arithmetic given adapter graphs; does not independently certify graph/partition correctness.",
    }
    (args.output / "summary.json").write_text(json.dumps(jsonable(summary), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    progress("independent_math_end", all_passed=summary["all_passed"], n_comparisons=summary["n_comparisons"])
    # ASCII console metadata avoids Windows cp1252 failures; all artifact files
    # remain UTF-8 and preserve the Vietnamese variant name.
    print(json.dumps({k: summary[k] for k in ("case_id", "variant", "n_comparisons", "all_passed", "max_absolute_error", "max_relative_error")}, ensure_ascii=True))
    return 0 if summary["all_passed"] and summary["spectrum_nonnegative"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
