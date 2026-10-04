"""T-015: independent span detector/TraceRCA calculation and saved-artifact audit.

The independent calculation never calls author functions. A separate comparison
loads the fixed RCAEval source to capture its published score and raw ranking.
Only the fixed dev case auth_cpu_1 is readable through the TT command.
"""
from __future__ import annotations

import argparse
import ast
import builtins
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[3]
CASE = "re2tt_ts-auth-service_cpu_1"
COLS = ["traceID", "spanID", "parentSpanID", "serviceName", "methodName",
        "operationName", "startTime", "duration"]
OFFICIAL = Path("D:/RCA-ext/src/RCAEval/RCAEval/e2e/tracerca.py")
ORIGINAL = Path("C:/Users/84583/AppData/Local/Temp/claude/D--RCA-flashticket/"
                "faa9e437-da55-49ba-b763-6e8484c8c9a6/scratchpad/ext/MicroRank")
ORIGINAL_TR = ORIGINAL.parent / "TraceRCA"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_safe(value):
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_json(path, data):
    path.write_text(json.dumps(json_safe(data), ensure_ascii=False, indent=2,
                               allow_nan=False) + "\n", encoding="utf-8")


def stable_finite_ranks(items):
    """Adapter candidate: remove nonfinite scores BEFORE sorting; stable key tie.

    It retains RCAEval's candidate rule (positive abnormal evidence), and never
    adds absent services. The independent caller reports NO_ANOMALY separately.
    """
    finite = [(str(op), float(score)) for op, score in items
              if score is not None and math.isfinite(float(score))]
    return [op for op, score in sorted(finite, key=lambda pair: (-pair[1], pair[0]))]


def legacy_ranks(items):
    converted = [(op, float("nan") if score is None else float(score))
                 for op, score in items]
    return [op for op, score in sorted(converted, key=lambda pair: pair[1], reverse=True)
            if not math.isnan(score)]


def service_ranks(operations, op_to_service=None):
    result = []
    for operation in operations:
        service = (op_to_service[operation] if op_to_service else operation.split("_", 1)[0])
        service = service.removesuffix("-db")
        if service not in result:
            result.append(service)
    return result


def independent_spans(data, marker_us):
    """Sample std (ddof=1), milliseconds, round(.,2), and >=: exact RE semantics."""
    if not math.isfinite(marker_us):
        raise ValueError("marker must be finite microseconds")
    records = data.loc[:, COLS].to_dict(orient="records")
    baseline = {}
    post = []
    identity = {}
    collision = []
    for row in records:
        service = row["serviceName"]
        method = row["methodName"]
        if method is None or isinstance(method, float) and math.isnan(method):
            method = row["operationName"]
        if not isinstance(service, str) or not isinstance(method, str):
            raise ValueError("service/method must be nonmissing strings")
        op = service + "_" + method
        pair = (service, method)
        if op in identity and identity[op] != pair:
            collision.append(op)
        identity[op] = pair
        duration = float(row["duration"])
        if not math.isfinite(duration) or duration < 0:
            raise ValueError("duration must be finite, nonnegative microseconds")
        start = float(row["startTime"])
        if not math.isfinite(start) or not math.isfinite(start + duration):
            raise ValueError("startTime and span end must be finite microseconds")
        if start + duration < marker_us:
            baseline.setdefault(op, []).append(duration)
        elif start + duration >= marker_us:
            post.append((op, duration))
    if collision:
        raise ValueError("ambiguous service_method key: " + ",".join(sorted(set(collision))))
    stats = {}
    for op, values in baseline.items():
        n = len(values)
        mean_us = math.fsum(values) / n
        sd_us = math.sqrt(math.fsum((v - mean_us) ** 2 for v in values) / (n - 1)) if n > 1 else float("nan")
        stats[op] = {"n_normal": n, "mean_ms": round(mean_us / 1000, 2),
                     "std_ms": round(sd_us / 1000, 2)}
    counts = {}
    total_abnormal = 0
    bad_baseline = []
    for op, duration in post:
        if op not in stats:
            raise ValueError("no baseline for post operation " + op)
        threshold = stats[op]["mean_ms"] + 3 * stats[op]["std_ms"]
        if not math.isfinite(threshold):
            bad_baseline.append(op)
        abnormal = int(duration / 1000 >= threshold)
        counts.setdefault(op, [0, 0])
        counts[op][0] += 1
        counts[op][1] += abnormal
        total_abnormal += abnormal
    details = {}
    items = []
    for op, (n, a) in counts.items():
        support = a / total_abnormal if total_abnormal else float("nan")
        confidence = a / n
        denominator = support + confidence
        score = 2 * support * confidence / denominator if denominator else float("nan")
        details[op] = dict(stats[op], n_after=n, abnormal=a, support=support,
                           confidence=confidence, score=score,
                           threshold_ms=stats[op]["mean_ms"] + 3 * stats[op]["std_ms"])
        items.append((op, score))
    status = "INVALID_BASELINE" if bad_baseline else "NO_ANOMALY" if not total_abnormal else "EVIDENCE"
    # Guarded adapter returns no diagnosis when any used reference is undefined.
    corrected = stable_finite_ranks(items) if status == "EVIDENCE" else []
    return {"status": status, "normal_spans": sum(map(len, baseline.values())),
            "after_spans": len(post), "abnormal_spans": total_abnormal,
            "undefined_baseline_operations": sorted(set(bad_baseline)),
            "items": items, "details": details, "legacy_ranks": legacy_ranks(items),
            "adapter_ranks": corrected,
            "op_to_service": {op: pair[0] for op, pair in identity.items()}}


def official_spans(data, marker_us):
    spec = importlib.util.spec_from_file_location("t015_official_tracerca", OFFICIAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    captured = {}
    def capture_sorted(items, *args, **kwargs):
        items = list(items)
        captured["items"] = [(op, float(score)) for op, score in items]
        return builtins.sorted(items, *args, **kwargs)
    module.sorted = capture_sorted
    result = module.tracerca(data.copy(deep=True), marker_us, dataset="re2-tt")
    return {"items": captured["items"], "ranks": result["ranks"]}


def score_difference(left, right):
    a, b = dict(left), dict(right)
    assert a.keys() == b.keys(), "operation set mismatch"
    absolute = 0.0
    relative = 0.0
    finite_count = 0
    nan_count = 0
    for op in a:
        x, y = a[op], b[op]
        if math.isnan(x) and math.isnan(y):
            nan_count += 1
            continue
        assert math.isfinite(x) and math.isfinite(y), "nonfinite mismatch: " + op
        finite_count += 1
        absolute = max(absolute, abs(x - y))
        relative = max(relative, abs(x - y) / max(abs(x), abs(y), 1e-300))
    assert absolute <= 1e-10 and relative <= 1e-10
    return {"max_abs": absolute, "max_rel": relative,
            "finite_scores": finite_count, "matching_nan": nan_count}


def artifact_audit(out):
    archive = REPO / "results/T-007/runs/py312-pin/tracerca-hoa3.tar.gz"
    with tarfile.open(archive, "r:gz") as tf:
        member = next(m for m in tf.getmembers() if m.isfile() and m.name.endswith("/hoa.jsonl"))
        rows = [json.loads(line) for line in tf.extractfile(member) if line.strip()]
    counters = {k: 0 for k in ["cases", "legacy_rebuilt_original", "legacy_rebuilt_shuffled",
                               "cases_with_nan", "cases_not_descending", "canonical_original_equals_shuffled",
                               "operation_ranking_changed", "service_ranking_changed", "root_service_rank_changed"]}
    output_rows = []
    for row in rows:
        # This artifact is exclusively RE2-OB, checked from T-007's fixed runner.
        assert row["case"].startswith("re2ob_"), "disallowed case in OB-only artifact"
        original = row["dau_vao_sorted_goc"]
        shuffled = row["dau_vao_sorted_xao"]
        raw = legacy_ranks(original)
        raw_shuffled = legacy_ranks(shuffled)
        canonical = stable_finite_ranks(original)
        canonical_shuffled = stable_finite_ranks(shuffled)
        scores = {op: score for op, score in original if score is not None}
        descending = all(scores[a] >= scores[b] for a, b in zip(raw, raw[1:]))
        counters["cases"] += 1
        counters["legacy_rebuilt_original"] += raw == row["ranks_goc"]
        counters["legacy_rebuilt_shuffled"] += raw_shuffled == row["ranks_xao"]
        counters["cases_with_nan"] += any(score is None for _, score in original)
        counters["cases_not_descending"] += not descending
        counters["canonical_original_equals_shuffled"] += canonical == canonical_shuffled
        counters["operation_ranking_changed"] += raw != canonical
        raw_services, canonical_services = service_ranks(raw), service_ranks(canonical)
        counters["service_ranking_changed"] += raw_services != canonical_services
        # Labels used only after both rankings have been constructed.
        target = row["case"][len("re2ob_"):].rsplit("_", 2)[0]
        before = raw_services.index(target) + 1 if target in raw_services else None
        after = canonical_services.index(target) + 1 if target in canonical_services else None
        counters["root_service_rank_changed"] += before != after
        output_rows.append({"case": row["case"], "nan_count": sum(score is None for _, score in original),
                            "legacy_rebuilt": raw == row["ranks_goc"], "descending": descending,
                            "legacy_services": json.dumps(raw_services),
                            "canonical_services": json.dumps(canonical_services),
                            "root_rank_legacy": before, "root_rank_canonical": after,
                            "canonical_equal_after_shuffle": canonical == canonical_shuffled})
    assert counters["cases"] == counters["legacy_rebuilt_original"] == counters["legacy_rebuilt_shuffled"] == 90
    assert counters["canonical_original_equals_shuffled"] == 90
    write_json(out / "t007-audit.json", {"source": str(archive), "source_sha256": sha256(archive),
               "calculation": "saved scores only; no baseline rerun", "counts": counters})
    with open(out / "t007-tung-ca.csv", "w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output_rows[0]))
        writer.writeheader(); writer.writerows(output_rows)
    return counters


def toy_checks(out):
    import pandas as pd
    import numpy as np
    def make(normal, after):
        rows = []
        for i, (operation, duration) in enumerate(normal + after):
            start = -1_000_000 if i < len(normal) else 1_000_000
            rows.append([str(i), str(i), "", "svc", operation, operation, start, duration])
        return pd.DataFrame(rows, columns=COLS)
    data = make([("a", 90000), ("a", 100000), ("a", 110000),
                 ("b", 50000), ("b", 60000), ("b", 70000)],
                [("a", 120000), ("a", 140000), ("b", 60000)])
    r = independent_spans(data, 0)
    official = official_spans(data, 0)
    match = score_difference(r["items"], official["items"])
    assert r["legacy_ranks"] == official["ranks"]
    assert r["details"]["svc_a"]["mean_ms"] == 100
    assert r["details"]["svc_a"]["std_ms"] == 10
    assert r["details"]["svc_a"]["score"] == 2 / 3
    normal_only = independent_spans(make([("a", 9000), ("a", 10000), ("a", 11000)],
                                         [("a", 10000), ("a", 11000)]), 0)
    assert normal_only["status"] == "NO_ANOMALY" and normal_only["adapter_ranks"] == []
    constant = independent_spans(make([("a", 10000), ("a", 10000)], [("a", 10000)]), 0)
    assert constant["abnormal_spans"] == 1  # >= makes an exactly constant normal trace abnormal.
    single = independent_spans(make([("a", 10000)], [("a", 11000)]), 0)
    assert single["status"] == "INVALID_BASELINE" and not single["adapter_ranks"]
    column = independent_spans(data.loc[:, list(reversed(COLS))], 0)
    reverse = independent_spans(data.iloc[::-1].copy(), 0)
    assert r["adapter_ranks"] == column["adapter_ranks"] == reverse["adapter_ranks"]
    score_difference(r["items"], column["items"]); score_difference(r["items"], reverse["items"])
    boundary = independent_spans(make([("a", 90000), ("a", 100000), ("a", 110000)],
                                      [("a", 130000)]), 0)
    assert boundary["abnormal_spans"] == 1  # >=, not >.
    roots = data.copy(deep=True)
    roots["traceID"] = "shared"
    roots["parentSpanID"] = ["", "missing", "", "missing", "", "", "missing", "", ""]
    altered_parents = independent_spans(roots, 0)
    score_difference(r["items"], altered_parents["items"])
    assert r["adapter_ranks"] == altered_parents["adapter_ranks"]
    try:
        independent_spans(make([("a", 9000), ("a", 10000)], [("new", 10000)]), 0)
    except ValueError as error:
        missing_reference = str(error)
    else:
        raise AssertionError("missing baseline was not detected")
    barrier = [("low", 0.2), ("undefined", None), ("high", 0.9)]
    assert legacy_ranks(barrier) == ["low", "high"]
    assert stable_finite_ranks(barrier) == ["high", "low"]
    # Independent original detector arithmetic; call isolated author AST only to compare.
    count = {str(i): {"a": 1, "b": 1, "duration": 35000} for i in range(9)}
    slo = {"a": [10., 1.], "b": [20., 2.]}
    expected_alarm = 10 + 1.5 * 1 + 20 + 1.5 * 2
    expected_partition = 10 + 1 + 20 + 2 + 50
    own_alarm = sum(v["duration"] / 1000 > expected_alarm for v in count.values()) > 8
    own_anomaly = [k for k, v in count.items() if v["duration"] / 1000 > expected_partition]
    tree = ast.parse((ORIGINAL / "anormaly_detector.py").read_text(encoding="utf-8"))
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in
                {"system_anormaly_detect", "trace_anormaly_detect", "trace_list_partition"}]
    namespace = {"get_span": lambda *args, **kwargs: [1],
                 "get_operation_duration_data": lambda *args, **kwargs: count}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "author-detector-isolated", "exec"), namespace)
    with contextlib.redirect_stdout(io.StringIO()):
        author_alarm = namespace["system_anormaly_detect"](0, 1, slo, ["a", "b"])
    author_abnormal, author_normal = namespace["trace_list_partition"](count, slo)
    assert author_alarm == own_alarm and author_abnormal == own_anomaly
    # TraceRCA original function's NAME does not set a 3-sigma multiplier.
    orig_tr_file = ORIGINAL_TR / "run_anomaly_detection_invo.py"
    tr_tree = ast.parse(orig_tr_file.read_text(encoding="utf-8"))
    tr_selected = [node for node in tr_tree.body if isinstance(node, ast.FunctionDef)
                   and node.name == "anomaly_detection_3sigma"]
    tr_namespace = {"np": np, "threshold": 1.0}
    exec(compile(ast.Module(body=tr_selected, type_ignores=[]), "author-tracerca-isolated", "exec"), tr_namespace)
    invocations = pd.DataFrame({"source": ["src", "src"], "target": ["tgt", "tgt"],
                                "latency": [12., 10.]})
    invocations = invocations.set_index(["source", "target"], drop=False)
    reference = {"reference-src-tgt-latency-mean-variance": {"mean": 10., "std": 1.}}
    prediction = tr_namespace["anomaly_detection_3sigma"](
        invocations, "predict", None, {("src", "tgt"): ["latency"]}, reference)["predict"].tolist()
    assert prediction == [1., 0.]
    result = {"span_example": r, "official_match": match,
              "normal_only": normal_only, "constant_normal_false_alarm": constant,
              "single_baseline": single, "missing_reference": missing_reference,
              "boundary_equal_mu_plus3sigma_is_anomalous": boundary["abnormal_spans"] == 1,
              "missing_parent_multi_root_and_shared_traceID_no_score_change": True,
              "column_and_row_permutation": "PASS",
              "nan_barrier": {"items": barrier, "legacy": legacy_ranks(barrier),
                              "adapter": stable_finite_ranks(barrier)},
              "original_detector": {"root_duration_ms": 35, "alarm_expected_ms": expected_alarm,
                                    "partition_expected_with_50ms": expected_partition,
                                    "trace_count": 9, "system_alarm": own_alarm,
                                    "partition_abnormal": len(own_anomaly), "author_match": True},
              "original_tracerca_named_3sigma_default_threshold1":
                  {"empirical": [12., 10.], "reference_mean": 10., "reference_std": 1.,
                   "prediction_threshold1": prediction, "prediction_if_threshold3": [False, False],
                   "source": str(orig_tr_file), "source_sha256": sha256(orig_tr_file)}}
    write_json(out / "toy-checks.json", result)
    return {"span_score_match": match, "checks": "PASS"}


def tt_checks(out, repeat_only=False):
    import pandas as pd
    source = REPO / "data/rcaeval" / CASE / "traces.parquet"
    marker = int((source.parent / "inject_time.txt").read_text().strip()) * 1_000_000
    io_runtime = "same pinned environment"
    try:
        raw = pd.read_parquet(source, columns=COLS)
        raw_count = len(raw)
    except ImportError:
        # py312-pin lacks a parquet engine on Windows. Read/serialize only in
        # the existing py312 runtime; all scoring still uses pinned py312-pin.
        # Bytes pass through pipes: no temp/input files, no new dependency.
        io_code = """import json, pandas as pd, sys
source, marker = sys.argv[1], int(sys.argv[2])
cols = json.loads(sys.argv[3])
raw = pd.read_parquet(source, columns=cols)
print(json.dumps({'raw_count':len(raw)}),file=sys.stderr)
raw.loc[(raw.startTime>=marker-600000000)&(raw.startTime<marker+600000000)].to_csv(sys.stdout,index=False)
"""
        result = subprocess.run(["D:/RCA-ext/envs/py312/Scripts/python.exe", "-B", "-c", io_code,
                                 str(source), str(marker), json.dumps(COLS)],
                                capture_output=True, text=True, check=True)
        raw_count = json.loads(result.stderr.strip().splitlines()[-1])["raw_count"]
        raw = pd.read_csv(io.StringIO(result.stdout),
                          dtype={column: str for column in COLS[:-2]})
        io_runtime = "py312 parquet I/O through CSV pipe; calculation in py312-pin"
    data = raw.loc[(raw.startTime >= marker - 600_000_000) &
                   (raw.startTime < marker + 600_000_000)].reset_index(drop=True)
    started = time.monotonic()
    independent = independent_spans(data, marker)
    write_json(out / "tt-independent-before-label.json", independent)
    official = official_spans(data, marker)
    diff = score_difference(independent["items"], official["items"])
    assert independent["legacy_ranks"] == official["ranks"]
    checks = []
    permutations = [] if repeat_only else [("columns_reversed", data.loc[:, list(reversed(COLS))]),
                                          ("rows_reversed", data.iloc[::-1].copy())]
    for name, variant in permutations:
        other = independent_spans(variant, marker)
        err = score_difference(independent["items"], other["items"])
        assert independent["adapter_ranks"] == other["adapter_ranks"]
        other_official = official_spans(variant, marker)
        err_official = score_difference(independent["items"], other_official["items"])
        checks.append({"permutation": name, "independent_match": err,
                       "official_scores_match": err_official,
                       "official_raw_ranking_same": other_official["ranks"] == official["ranks"],
                       "adapter_ranking_same": True})
    # Two pre-injection windows. A finding here is a false alarm for this check,
    # never an identified cause of the later injected event.
    pre = raw.loc[(raw.startTime >= marker - 600_000_000) &
                  (raw.startTime < marker)].reset_index(drop=True)
    normal_split = independent_spans(pre, marker - 300_000_000)
    write_json(out / "tt-two-normal-windows.json", normal_split)
    mapping = independent["op_to_service"]
    service_rank = service_ranks(independent["adapter_ranks"], mapping)
    # Label explanation starts only after independent ranking has been saved.
    target = CASE[len("re2tt_"):].rsplit("_", 2)[0]
    summary = {"case": CASE, "source": str(source), "source_sha256": sha256(source),
               "method": "TraceRCA RCAEval plus independent stable-sort adapter candidate",
               "purpose": "hash seed/repetition" if repeat_only else "new TT scale, hand example, invariance and normal-window check",
               "reason": "a" if repeat_only else "b",
               "reference_window_seconds": 600, "official_source_sha256": sha256(OFFICIAL),
               "raw_spans": raw_count, "window_spans": len(data), "io_runtime": io_runtime,
               "status": independent["status"], "normal_spans": independent["normal_spans"],
               "after_spans": independent["after_spans"], "abnormal_spans": independent["abnormal_spans"],
               "official_score_match": diff, "official_raw_ranks": official["ranks"],
               "adapter_ranks": independent["adapter_ranks"], "adapter_service_ranks": service_rank,
               "root_service": target, "root_service_rank": service_rank.index(target)+1 if target in service_rank else None,
               "root_in_trace": target in set(data.serviceName), "permutation_checks": checks,
               "two_normal_windows": {"status": normal_split["status"],
                                      "normal_spans": normal_split["normal_spans"],
                                      "after_spans": normal_split["after_spans"],
                                      "false_alarm_abnormal_spans": normal_split["abnormal_spans"],
                                      "returned_operations": len(normal_split["adapter_ranks"]),
                                      "interpretation": "false alarm, no meaningful injected root cause"},
               "elapsed_observed_seconds": round(time.monotonic()-started,3),
               "timing_is_official": False, "python": sys.version, "pandas": pd.__version__,
               "hash_seed": os.environ.get("PYTHONHASHSEED", "unset")}
    canonical_scores = json_safe({op: score for op, score in sorted(independent["items"])})
    summary["canonical_score_sha256"] = hashlib.sha256(json.dumps(canonical_scores, sort_keys=True).encode()).hexdigest()
    write_json(out / "tt-summary.json", summary)
    fields = ["operation", "service", "n_normal", "mean_ms", "std_ms", "threshold_ms",
              "n_after", "abnormal", "support", "confidence", "score"]
    with open(out / "tt-operation-scores.csv", "w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fields); writer.writeheader()
        for op in sorted(independent["details"]):
            writer.writerow(json_safe({"operation": op, "service": mapping[op], **independent["details"][op]}))
    return {"status": summary["status"], "spans": len(data), "scores": diff,
            "root_service_rank": summary["root_service_rank"], "normal_windows": summary["two_normal_windows"]}


def normal_boundary_audit(out):
    """Light I/O census; strict control deduced from saved independent counts.

    Only spans starting before but ending at/after injection are read into
    memory. Baseline values from the earlier independently checked control
    remain unchanged, so subtracting these spans gives the strict control.
    This does not call the official method or rerun the case pipeline.
    """
    source = REPO / "data/rcaeval" / CASE / "traces.parquet"
    marker = int((source.parent / "inject_time.txt").read_text().strip()) * 1_000_000
    io_code = """import json, pyarrow.parquet as pq, sys
source, marker, cols = sys.argv[1], int(sys.argv[2]), json.loads(sys.argv[3])
before = 0
crossing = []
for batch in pq.ParquetFile(source).iter_batches(columns=cols,batch_size=65536):
    f=batch.to_pandas()
    select=(f.startTime>=marker-600000000)&(f.startTime<marker)
    before+=int(select.sum())
    cross=f.loc[select&(f.startTime+f.duration>=marker)]
    crossing.extend(json.loads(cross.to_json(orient='records')))
print(json.dumps({'pre_start_spans':before,'crossing_rows':crossing}))
"""
    read = subprocess.run(["D:/RCA-ext/envs/py312/Scripts/python.exe", "-B", "-c", io_code,
                           str(source),str(marker),json.dumps(COLS)],capture_output=True,
                          text=True,check=True,timeout=60)
    census = json.loads(read.stdout)
    old_path = REPO / "results/T-015/runs/tracerca-audit/seed0/tt-two-normal-windows.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    details = old["details"]
    removed = []
    removed_abnormal = 0
    for row in census["crossing_rows"]:
        method = row["methodName"] if row["methodName"] is not None else row["operationName"]
        op = row["serviceName"] + "_" + method
        assert row["startTime"] + row["duration"] >= marker > marker-300_000_000
        cell = details[op]
        flag = int(row["duration"]/1000 >= cell["threshold_ms"])
        cell["n_after"] -= 1
        cell["abnormal"] -= flag
        assert cell["n_after"] >= cell["abnormal"] >= 0
        removed_abnormal += flag
        removed.append({"operation":op,"traceID":row["traceID"],"spanID":row["spanID"],
                        "startTime":row["startTime"],"duration":row["duration"],
                        "threshold_ms":cell["threshold_ms"],"abnormal_under_saved_reference":flag})
    total = old["abnormal_spans"] - removed_abnormal
    items = []
    for op, cell in details.items():
        n, a = cell["n_after"], cell["abnormal"]
        if not n: continue
        support, confidence = a/total if total else float("nan"),a/n
        score = 2*support*confidence/(support+confidence) if support+confidence else float("nan")
        cell.update(support=support,confidence=confidence,score=score)
        items.append((op,score))
    strict = {"status":"EVIDENCE" if total else "NO_ANOMALY",
              "normal_spans":old["normal_spans"],
              "after_spans":old["after_spans"]-len(removed),"abnormal_spans":total,
              "items":items,"details":details,"adapter_ranks":stable_finite_ranks(items) if total else [],
              "op_to_service":old["op_to_service"],
              "calculation":"Saved independently calculated baseline and counts minus every span ending at/after injection; scores recomputed without author functions",
              "source":str(source),"source_sha256":sha256(source),
              "saved_control":str(old_path),"saved_control_sha256":sha256(old_path),
              "reason":"c","purpose":"correct normal-window control crossing injection boundary"}
    audit = {"case":CASE,"pre_start_spans":census["pre_start_spans"],
             "pre_end_spans":census["pre_start_spans"]-len(removed),
             "crossing_injection_spans":len(removed),"removed_abnormal_spans":removed_abnormal,
             "original_abnormal_spans":old["abnormal_spans"],"strict_abnormal_spans":total,
             "strict_after_spans":strict["after_spans"],"strict_finite_operation_count":len(strict["adapter_ranks"]),
             "reference_unchanged":True,"removed_rows":removed,
             "source":str(source),"source_sha256":sha256(source),
             "interpretation":"All strict control observations end before injection; remaining flags are pre-injection deviations, without an injected meaningful root cause"}
    write_json(out/"strict-normal-boundary-audit.json",audit)
    write_json(out/"strict-two-normal-windows.json",strict)
    return {key:audit[key] for key in ["crossing_injection_spans","removed_abnormal_spans",
                                     "strict_abnormal_spans","strict_after_spans","strict_finite_operation_count"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["artifact", "toy", "tt", "tt-repeat", "normal-boundary", "all"])
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    allowed = (REPO / "results/T-015/runs/tracerca-audit").resolve()
    args.out = args.out.resolve()
    assert args.out == allowed or allowed in args.out.parents, "output outside delegated scope"
    args.out.mkdir(parents=True, exist_ok=True)
    with open(args.out / "progress.jsonl", "a", encoding="utf-8") as progress:
        actions = [("artifact", artifact_audit), ("toy", toy_checks), ("tt", tt_checks),
                   ("tt-repeat", lambda target: tt_checks(target, repeat_only=True)),
                   ("normal-boundary",normal_boundary_audit)]
        for name, action in actions:
            if name == "tt-repeat" and args.mode != name:
                continue
            if name == "normal-boundary" and args.mode != name:
                continue
            if args.mode not in (name, "all"):
                continue
            t0 = time.monotonic()
            rec = {"step": name, "start_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "status": "START"}
            progress.write(json.dumps(rec)+"\n"); progress.flush()
            print(json.dumps(rec), flush=True)
            try:
                result = action(args.out)
            except Exception as error:
                progress.write(json.dumps({"step": name, "status": "FAILED", "error": repr(error),
                                           "elapsed_seconds": time.monotonic()-t0})+"\n")
                progress.flush()
                raise
            rec = {"step": name, "status": "PASS", "result": result,
                   "elapsed_seconds": round(time.monotonic()-t0,3)}
            progress.write(json.dumps(rec)+"\n"); progress.flush()
            print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
