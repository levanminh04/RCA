"""Reproduce T-015 review diagnostics from three saved dev snapshots only.

No raw data, labels, or author function is read/called for the calculations.
The two independent arithmetic functions are selected as AST definitions;
independent_math.main and its file-writing path are never executed.
25/26/50/100/101 are fixed before the probe, not selected by any root rank.

Usage: python -B check_review_diagnostics.py --repo D:/RCA-flashticket
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import csv
import datetime
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import time

# Pin summation runtime before NumPy is imported. These are task-local process
# settings; neither the shared environment nor system configuration is changed.
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import numpy as np


FIXED_TURNS = (25, 26, 50, 100, 101)
CASES = (
    ("re2tt_ts-auth-service_cpu_1", "auth"),
    ("re2tt_ts-route-service_mem_1", "re2tt_ts-route-service_mem_1"),
    ("re2tt_ts-route-service_socket_1", "re2tt_ts-route-service_socket_1"),
)
AUTH_SERVICE = "ts-auth-service"
STATION_OPERATION = "ts-station-service_find ts.station"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_independent_functions(path: Path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {"recompute_group", "recompute_spectrum"}
    selected = [node for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name in names]
    if {node.name for node in selected} != names:
        raise ValueError("Both independent arithmetic definitions are required")
    namespace = {"np": np, "Counter": Counter}
    module = ast.fix_missing_locations(ast.Module(body=selected, type_ignores=[]))
    exec(compile(module, str(path), "exec"), namespace)
    return namespace["recompute_group"], namespace["recompute_spectrum"], {
        "source_path": path.as_posix(), "source_sha256": sha256(path),
        "selected_function_ast_sha256": hashlib.sha256(
            ast.dump(module, include_attributes=False).encode("utf-8")).hexdigest(),
        "functions": [{"name": node.name, "line": node.lineno}
                      for node in selected],
        "author_function_called": False,
    }


def scalar_stats(payload: dict, case: str, source: str, source_hash: str) -> list[dict]:
    counts = payload["counts"]
    total = counts["all"]
    if counts["normal"] + counts["anomaly"] != total or counts["overlap"] != 0:
        raise ValueError("Snapshots must have two disjoint, exhaustive groups")
    length_sets = {}
    for name in ("normal", "anomaly"):
        repeated = payload["groups"][name]["graph"]["pr_trace"]
        length_sets[name] = {trace for trace, ops in repeated.items() if len(ops) >= 100}
    long_total = len(length_sets["normal"]) + len(length_sets["anomaly"])
    conditional_long = len(length_sets["anomaly"]) / long_total
    conditional_short = (counts["anomaly"] - len(length_sets["anomaly"])) / (total - long_total)
    rows = []
    for name in ("normal", "anomaly"):
        group = payload["groups"][name]
        graph = group["graph"]
        lengths = [len(ops) for ops in graph["pr_trace"].values()]
        n = len(lengths)
        if n != group["trace_count"] or n != counts[name]:
            raise ValueError("Length census and source trace counts disagree")
        source_spans = sum(lengths)
        auth_ops = [op for op in graph["trace_operation"]
                    if payload["operation_services"][op] == AUTH_SERVICE]
        auth_traces = set().union(*(set(graph["trace_operation"][op]) for op in auth_ops))
        station = set(graph["trace_operation"].get(STATION_OPERATION, []))
        long = length_sets[name]
        rows.append({
            "case": case, "sample": "primary", "group": name,
            "source_path": source, "source_sha256": source_hash,
            "trace_count": n, "span_occurrence_count": source_spans,
            "mean_span_count": statistics.mean(lengths),
            "median_span_count": statistics.median(lengths),
            "ge100_trace_count": len(long), "ge100_trace_proportion": len(long) / n,
            "auth_operation_count": len(auth_ops), "auth_union_trace_count": len(auth_traces),
            "ge100_and_auth_union_count": len(long & auth_traces),
            "ge100_without_auth_union_count": len(long - auth_traces),
            "station_trace_count": len(station),
            "station_and_ge100_trace_count": len(station & long),
            "ge100_without_station_count": len(long - station),
            "station_without_ge100_count": len(station - long),
            "station_and_ge100_sets_equal": station == long,
            "current_span_count": counts["spans_after"],
            "flagged_span_count": counts["abnormal_spans"],
            "flagged_span_proportion": counts["abnormal_spans"] / counts["spans_after"],
            "current_trace_count": total, "anomaly_trace_count": counts["anomaly"],
            "anomaly_trace_proportion": counts["anomaly"] / total,
            "anomaly_proportion_given_ge100": conditional_long,
            "anomaly_proportion_given_lt100": conditional_short,
        })
    if sum(row["span_occurrence_count"] for row in rows) != counts["spans_after"]:
        raise ValueError("pr_trace occurrence lengths do not conserve current spans")
    return rows


def iteration_probe(payload: dict, recompute_group, recompute_spectrum) -> list[dict]:
    baseline = None
    rows = []
    saved = payload["scores"]
    normal_count = payload["groups"]["normal"]["trace_count"]
    anomaly_count = payload["groups"]["anomaly"]["trace_count"]
    for turn in FIXED_TURNS:
        options = {**payload["options"], "iterations": turn}
        groups = {name: recompute_group(payload["groups"][name], name == "anomaly", options)
                  for name in ("normal", "anomaly")}
        _, scores = recompute_spectrum(groups["normal"], groups["anomaly"], normal_count, anomaly_count)
        ranks = sorted(scores, key=lambda operation: (-scores[operation], operation))
        if baseline is None:
            baseline = (groups, scores, ranks)
            if set(scores) != set(saved):
                raise ValueError("25-turn score keys differ from saved snapshot")
            absolute_error = max(abs(float(scores[op]) - float(saved[op])) for op in saved)
            relative_error = max(
                0.0 if scores[op] == saved[op] else
                abs(float(scores[op]) - float(saved[op])) / max(abs(float(saved[op])), abs(float(scores[op])), np.finfo(float).tiny)
                for op in saved)
            if absolute_error > 1e-10 or relative_error > 1e-10:
                raise ValueError("25-turn diagnostic failed to match saved arithmetic")
            if ranks != payload["full_ranks"] or ranks[:11] != payload["ranks"]:
                raise ValueError("25-turn ranking failed to match saved snapshot")
        base_groups, base_scores, base_ranks = baseline
        rows.append({
            "iterations": turn,
            "op_max_delta_last": {name: groups[name]["iteration_rows"][-1]["operation_max_absolute_change"]
                                  for name in groups},
            "trace_max_delta_last": {name: groups[name]["iteration_rows"][-1]["trace_max_absolute_change"]
                                     for name in groups},
            "op_vector_max_delta_vs25": {name: max(
                abs(float(value) - float(base_groups[name]["operation_pagerank"][operation]))
                for operation, value in groups[name]["operation_pagerank"].items()) for name in groups},
            "full_ranks_changed_vs25": ranks != base_ranks,
            "top11_changed_vs25": ranks[:11] != base_ranks[:11],
            "max_score_absolute_delta_vs25": max(abs(float(scores[op]) - float(base_scores[op])) for op in scores),
            **({"max_score_delta_vs_saved": absolute_error,
                "max_score_relative_delta_vs_saved": relative_error} if turn == 25 else {}),
        })
        print(json.dumps({"event": "iteration_end", "iterations": turn}, ensure_ascii=True), flush=True)
    return rows


def source_checks(repo: Path) -> dict:
    manifest = json.loads((repo / "results/T-015/manifest-inputs.json").read_bytes())
    source = next(item for item in manifest["sources"] if Path(item["repo"]).name == "MicroRank")
    path = Path(source["repo"]) / "preprocess_data.py"
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "get_operation_slo")
    if_nodes = {node.lineno: node for node in ast.walk(function) if isinstance(node, ast.If)}
    # Read the pinned branch structure only. Author definitions are not executed.
    missing_refs = if_nodes[210]
    parent_use = if_nodes[218]
    assigned_on_missing = any(isinstance(node, ast.Name) and node.id == "parentId"
                              and isinstance(node.ctx, ast.Store)
                              for stmt in missing_refs.body for node in ast.walk(stmt))
    used_after_missing = any(isinstance(node, ast.Name) and node.id == "parentId"
                            and isinstance(node.ctx, ast.Load) for node in ast.walk(parent_use.test))
    if assigned_on_missing or not used_after_missing:
        raise ValueError("Pinned missing-reference control flow differs from reviewed source")

    def independent_binding_example(has_prior_parent: bool):
        # Minimal state counterexample, not a call to get_operation_slo. A
        # frontend/server first trace takes no parentId assignment. A later
        # non-frontend first span with refs=[] reaches parentId membership use.
        bindings = {"parentId": "parent-from-previous-trace"} if has_prior_parent else {}
        references = []
        if references:
            bindings["parentId"] = references[0]
        return {"result": "stale_parent_read" if "parentId" in bindings else "unbound_parent_read",
                "parent_read": bindings.get("parentId"), "missing_refs": True}

    p = 0.01
    return {
        "source_path": path.as_posix(), "source_revision": source["revision"],
        "source_sha256": sha256(path), "author_function_called": False,
        "missing_refs_parent_binding": {
            "missing_refs_if_line": 210, "later_parent_use_line": 218,
            "missing_branch_assigns_parentId": assigned_on_missing,
            "later_test_loads_parentId": used_after_missing,
            "independent_counterexamples": [independent_binding_example(False), independent_binding_example(True)],
            "exact_author_ast_execution_evidence": "tasks/T-015-ho-so-microrank/LOG.md, Phien 2, N2",
            "scope": "Static pinned AST plus minimal independent binding-state examples; not an author-function execution in this run.",
        },
        "opportunity_illustration": {
            "assumed_independent_equal_span_flag_probability": p,
            "trace_flag_probability": {str(n): 1 - (1 - p) ** n for n in (5, 179)},
            "scope": "Illustration only: observed span flags may be correlated and operation mix differs. No fitted detector or causal estimate.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = repo / "results/T-015/runs/review-response"
    files = ("trace-length-stats.csv", "iteration-probe.json", "toy-source-checks.json")
    if any((output / name).exists() for name in files):
        raise FileExistsError("Preserve existing review diagnostics; do not overwrite outputs")
    start = time.monotonic()
    print(json.dumps({"event": "start", "fixed_turns_before_probe": FIXED_TURNS}), flush=True)
    independent_path = repo / "results/T-015/scripts/independent_math.py"
    recompute_group, recompute_spectrum, implementation = load_independent_functions(independent_path)
    rows, input_manifest = [], []
    probe = None
    for case, folder in CASES:
        relative = f"results/T-015/runs/tt-local/{folder}/example.json"
        path = repo / relative
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        payload = json.loads(raw)
        rows.extend(scalar_stats(payload, case, relative, digest))
        input_manifest.append({"path": relative, "sha256": digest})
        if folder == "auth":
            probe = {"input": relative, "input_sha256": digest,
                     "fixed_turns_before_probe": list(FIXED_TURNS),
                     "options_fixed_except_iterations": {key: payload["options"][key] for key in ("d", "alpha")},
                     "rows": iteration_probe(payload, recompute_group, recompute_spectrum)}
        print(json.dumps({"event": "snapshot_end", "case": case}), flush=True)
        del raw, payload
        gc.collect()
    control_relative = "results/T-015/runs/tt-local/auth/two-normal-summary.json"
    control_path = repo / control_relative
    control = json.loads(control_path.read_bytes())["counts"]
    control_hash = sha256(control_path)
    for name in ("normal", "anomaly"):
        row = {field: "" for field in rows[0]}
        row.update(case=CASES[0][0], sample="two_normal_control", group=name,
                   source_path=control_relative, source_sha256=control_hash,
                   trace_count=control[name], current_span_count=control["spans_after"],
                   flagged_span_count=control["abnormal_spans"],
                   flagged_span_proportion=control["abnormal_spans"] / control["spans_after"],
                   current_trace_count=control["all"], anomaly_trace_count=control["anomaly"],
                   anomaly_trace_proportion=control["anomaly"] / control["all"])
        rows.append(row)
    input_manifest.append({"path": control_relative, "sha256": control_hash})
    static_checks = source_checks(repo)
    output.mkdir(parents=True, exist_ok=True)
    with (output / files[0]).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    common = {"created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "python": platform.python_version(), "numpy": np.__version__,
              "blas_threads": {key: os.environ[key] for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
              "script_sha256": sha256(Path(__file__)),
              "input_manifest": input_manifest, "no_raw_or_label_read": True,
              "elapsed_observation_seconds": time.monotonic() - start, "timing_official": False}
    probe.update(common)
    probe.update(independent_implementation=implementation,
                 interpretation="Sensitivity diagnostic on one frozen graph snapshot; keep default 25. No convergence proof, new root prediction, or hyperparameter selection.")
    (output / files[1]).write_text(json.dumps(probe, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    checks = {**common, **static_checks}
    (output / files[2]).write_text(json.dumps(checks, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"event": "done", "stats_rows": len(rows), "iteration_rows": len(probe["rows"]),
                      "score_error_25": probe["rows"][0]["max_score_delta_vs_saved"],
                      "author_function_called": False}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
