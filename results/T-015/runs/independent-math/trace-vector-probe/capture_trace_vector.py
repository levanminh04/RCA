"""Observe official pageRank's final trace vector without changing its code.

This comparison runs only pageRank on saved matrices. The independent result
was calculated previously without importing the author's functions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", type=Path, required=True)
    ap.add_argument("--independent-dir", type=Path, required=True)
    ap.add_argument("--official", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    raw = a.snapshot.read_bytes()
    saved = json.loads(raw)
    independent = json.loads((a.independent_dir / "summary.json").read_text(encoding="utf-8"))
    assert independent["all_passed"]
    assert hashlib.sha256(raw).hexdigest() == independent["input_sha256"]
    assert not a.out.exists(), "Keep previous probes"
    a.out.mkdir(parents=True)
    start = time.monotonic()
    def progress(event, **extra):
        with (a.out / "progress.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"event": event, "elapsed_observed_seconds": time.monotonic()-start,
                                     "timing_official": False, **extra}) + "\n")
    progress("start")
    source_before = hashlib.sha256(a.official.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location("t015_official_trace_probe", a.official)
    official = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(official)
    rows = []
    for name in ("normal", "anomaly"):
        g = saved["groups"][name]
        graph = g["graph"]
        operations = list(graph["operation_operation"])
        traces = list(graph["operation_trace"])
        oi = {op: i for i, op in enumerate(operations)}
        ti = {trace: i for i, trace in enumerate(traces)}
        m, n = len(operations), len(traces)
        A = np.zeros((m, m), dtype=np.float32)
        B = np.zeros((m, n), dtype=np.float32)
        C = np.zeros((n, m), dtype=np.float32)
        for parent, children in graph["operation_operation"].items():
            for child in children: A[oi[child], oi[parent]] = 1 / len(children)
        for trace, ops in graph["operation_trace"].items():
            for op in ops: B[oi[op], ti[trace]] = 1 / len(ops)
        for op, containing in graph["trace_operation"].items():
            for trace in containing: C[ti[trace], oi[op]] = 1 / len(containing)
        prior = np.asarray([g["official"]["prior"][trace] for trace in traces], dtype=np.float32).reshape(n, 1)
        captured = {}
        def observe(frame, event, arg):
            if event == "return" and frame.f_code is official.pageRank.__code__:
                captured["trace"] = frame.f_locals["request_ranking_vector"].copy()
                captured["operation"] = arg.copy()
        previous_profile = sys.getprofile()
        try:
            sys.setprofile(observe)
            official.pageRank(A, B, C, prior, m, n)
        finally:
            sys.setprofile(previous_profile)
        assert set(captured) == {"trace", "operation"}
        for side, nodes, filename, key, valuekey in (
                ("trace", traces, f"{name}-traces.csv", "trace", "trace_pagerank"),
                ("operation", operations, f"{name}-operations.csv", "operation", "operation_pagerank")):
            with (a.independent_dir / filename).open(encoding="utf-8", newline="") as stream:
                expected = {row[key]: float(row[valuekey]) for row in csv.DictReader(stream)}
            assert set(nodes) == set(expected)
            for i, node in enumerate(nodes):
                actual, ref = float(captured[side][i, 0]), expected[node]
                error = abs(actual-ref)
                relative = 0 if error == 0 else error / max(abs(actual), abs(ref), sys.float_info.min)
                rows.append({"group": name, "vector": side, "node": node,
                             "official": actual, "independent": ref,
                             "absolute_error": error, "relative_error": relative,
                             "passed": bool(np.isfinite(actual) and np.isfinite(ref) and error <= 1e-10 and relative <= 1e-10)})
        progress("group_end", group=name, operations=m, traces=n)
    source_after = hashlib.sha256(a.official.read_bytes()).hexdigest()
    assert source_before == source_after
    with (a.out / "comparison.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    summary = {"snapshot_sha256": independent["input_sha256"], "official_source_sha256_before": source_before,
               "official_source_sha256_after": source_after, "source_unchanged": True,
               "n_comparisons": len(rows), "trace_comparisons": sum(r["vector"] == "trace" for r in rows),
               "operation_comparisons": sum(r["vector"] == "operation" for r in rows),
               "all_passed": all(r["passed"] for r in rows),
               "max_absolute_error": max(r["absolute_error"] for r in rows),
               "max_relative_error": max(r["relative_error"] for r in rows),
               "scope": "Observe return locals of unchanged official.pageRank on saved matrices; no complete-method rerun",
               "python": sys.version, "numpy": np.__version__, "timing_official": False}
    (a.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    progress("end", all_passed=summary["all_passed"])
    print(json.dumps(summary))
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
