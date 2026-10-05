"""T-017: tinh lai vi du doc lap, chi doc dau vao da chuan hoa.

Khong import ban cai SimpleRCA, adapter, raw telemetry hoac file nhan.
Cong thuc va tham so duoc khoa trong tasks/T-017-simplerca/SPEC.md.

Vi du:
  py -3 independent_example.py --self-test
  py -3 independent_example.py --input-dir <normalized> --out <result.json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


FILENAMES = (
    "normal_metrics.csv",
    "incident_metrics.csv",
    "normal_traces.csv",
    "incident_traces.csv",
    "incident_logs.csv",
    "metadata.json",
)
KEYWORDS = ("error", "fail", "exception")


def _service(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Service rong hoac khong phai chuoi.")
    return value


def _finite(values: Any) -> tuple[np.ndarray, int]:
    raw = np.asarray(values, dtype=np.float64)
    finite = raw[np.isfinite(raw)]
    return finite, int(raw.size - finite.size)


def calculate(
    normal_metrics: pd.DataFrame,
    incident_metrics: pd.DataFrame,
    normal_traces: pd.DataFrame,
    incident_traces: pd.DataFrame,
    incident_logs: pd.DataFrame,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Tinh tung gia tri trung gian bang numpy, khong dung loi chinh."""
    for name, frame in (
        ("normal_metrics", normal_metrics),
        ("incident_metrics", incident_metrics),
    ):
        if "time" not in frame:
            raise ValueError(f"{name}: thieu cot time.")
    for name, frame, required in (
        ("normal_traces", normal_traces, {"service", "duration"}),
        ("incident_traces", incident_traces, {"service", "duration"}),
        ("incident_logs", incident_logs, {"service", "message"}),
    ):
        if not required.issubset(frame.columns):
            raise ValueError(f"{name}: thieu cot {sorted(required)}.")

    mapping = metadata.get("metric_services")
    if not isinstance(mapping, dict):
        raise ValueError("metadata.metric_services phai la mapping tuong minh.")
    logs_available = metadata.get("logs_available")
    if not isinstance(logs_available, bool):
        raise ValueError("metadata.logs_available phai la bool.")
    if not logs_available and len(incident_logs):
        raise ValueError("Log co dong nhung metadata ghi modality unavailable.")

    score_parts: dict[str, dict[str, int]] = {}

    def observe(service: str) -> dict[str, int]:
        service = _service(service)
        return score_parts.setdefault(
            service, {"metric_alerts": 0, "trace_alerts": 0, "log_alerts": 0}
        )

    # New normalized inputs retain normal-only log identities, never messages.
    # Older snapshots omit this field and remain readable as historical inputs.
    for service in metadata.get("observed_services", []):
        observe(service)

    metric_details = []
    names = sorted(
        (set(normal_metrics.columns) | set(incident_metrics.columns)) - {"time"}
    )
    for metric in names:
        if metric not in mapping:
            raise ValueError(f"Metric {metric!r} khong co service mapping.")
        service = _service(mapping[metric])
        parts = observe(service)
        normal_raw = normal_metrics[metric] if metric in normal_metrics else []
        incident_raw = incident_metrics[metric] if metric in incident_metrics else []
        normal, normal_missing = _finite(normal_raw)
        incident, incident_missing = _finite(incident_raw)
        available = len(normal) >= 2 and len(incident) >= 1
        mean = float(np.mean(normal)) if len(normal) else None
        std = float(np.std(normal, ddof=0)) if len(normal) else None
        threshold = mean + 3.0 * std if available else None
        alerts = int(np.count_nonzero(incident > threshold)) if available else 0
        parts["metric_alerts"] += alerts
        metric_details.append(
            {
                "metric": metric,
                "service": service,
                "normal_n": int(len(normal)),
                "incident_n": int(len(incident)),
                "normal_nonfinite": normal_missing,
                "incident_nonfinite": incident_missing,
                "mean": mean,
                "std": std,
                "threshold": threshold,
                "alerts": alerts,
                "available": available,
            }
        )

    for frame in (normal_traces, incident_traces):
        for service in frame["service"]:
            observe(_service(service))
        durations, _ = _finite(frame["duration"])
        if np.any(durations < 0):
            raise ValueError("Duration am: khong tinh percentile.")
    trace_services = sorted(
        set(normal_traces["service"]) | set(incident_traces["service"])
    )
    trace_details = []
    for service in trace_services:
        normal, normal_missing = _finite(
            normal_traces.loc[normal_traces["service"] == service, "duration"]
        )
        incident, incident_missing = _finite(
            incident_traces.loc[incident_traces["service"] == service, "duration"]
        )
        normal_p95 = float(np.quantile(normal, 0.95, method="linear")) if len(normal) else None
        incident_p95 = float(np.quantile(incident, 0.95, method="linear")) if len(incident) else None
        available = normal_p95 is not None and incident_p95 is not None
        threshold = 3.0 * normal_p95 if available else None
        alert = int(incident_p95 > threshold) if available else 0
        observe(service)["trace_alerts"] += alert
        trace_details.append(
            {
                "service": service,
                "normal_n": int(len(normal)),
                "incident_n": int(len(incident)),
                "normal_nonfinite": normal_missing,
                "incident_nonfinite": incident_missing,
                "normal_p95": normal_p95,
                "incident_p95": incident_p95,
                "threshold": threshold,
                "alert": alert,
                "available": available,
            }
        )

    error_counts: dict[str, int] = {}
    for row in incident_logs.itertuples(index=False):
        service = _service(row.service)
        observe(service)
        error_counts.setdefault(service, 0)
        message = "" if pd.isna(row.message) else str(row.message).lower()
        if any(keyword in message for keyword in KEYWORDS):
            error_counts[service] += 1
    # Co modality log nhung service khong co dong log: count = 0.
    log_details = []
    for service in sorted(score_parts):
        count = error_counts.get(service, 0)
        alert = int(count > 0) if logs_available else 0
        score_parts[service]["log_alerts"] += alert
        log_details.append(
            {
                "service": service,
                "error_count": count if logs_available else None,
                "threshold": 0,
                "alert": alert,
                "available": logs_available,
            }
        )

    services = []
    for service, parts in score_parts.items():
        services.append({"service": service, **parts, "score": sum(parts.values())})
    services.sort(key=lambda row: (-row["score"], row["service"]))
    tie_groups = []
    for row in services:
        if not tie_groups or row["score"] != tie_groups[-1]["score"]:
            tie_groups.append({"score": row["score"], "services": []})
        tie_groups[-1]["services"].append(row["service"])
    abstained = not services or services[0]["score"] == 0
    return {
        "calculation": "independent_numpy_from_normalized_inputs",
        "parameters": {
            "metric_sigma": 3,
            "std_ddof": 0,
            "metric_min_normal_n": 2,
            "trace_quantile": 0.95,
            "quantile_method": "linear",
            "trace_factor": 3,
            "log_keywords": list(KEYWORDS),
            "log_count_threshold": 0,
            "comparison": "strict_greater_than",
            "metric_vote_unit": "finite_incident_value",
        },
        "metrics": metric_details,
        "traces": trace_details,
        "logs": log_details,
        "services": services,
        "ranking": [] if abstained else [row["service"] for row in services],
        "tie_groups": tie_groups,
        "abstained": abstained,
        "labels_read": False,
    }


def self_test() -> dict[str, Any]:
    """Dap an da tinh tay; khong ghi tep, khong doc ca dev."""
    empty_trace = pd.DataFrame(columns=["service", "duration"])
    empty_log = pd.DataFrame(columns=["service", "message"])
    normal = pd.DataFrame({"time": [0, 1, 2], "b_cpu": [-1.0, 0.0, 1.0], "a_cpu": [0.0, 0.0, 0.0]})
    incident = pd.DataFrame({"time": [3, 4, 5], "b_cpu": [0.0, 3.0, 4.0], "a_cpu": [0.0, 1.0, 2.0]})
    nt = pd.DataFrame({"service": ["a", "a", "b"], "duration": [1.0, 3.0, 2.0]})
    it = pd.DataFrame({"service": ["a", "a", "b"], "duration": [8.7, 8.7, 7.0]})
    logs = pd.DataFrame({"service": ["a", "a", "b"], "message": ["ERROR FAIL exception", "ok", "Failure"]})
    meta = {"metric_services": {"a_cpu": "a", "b_cpu": "b"}, "logs_available": True}
    result = calculate(normal, incident, nt, it, logs, meta)
    metric = {row["metric"]: row for row in result["metrics"]}
    trace = {row["service"]: row for row in result["traces"]}
    log = {row["service"]: row for row in result["logs"]}
    assert math.isclose(metric["b_cpu"]["threshold"], math.sqrt(6.0), abs_tol=1e-12)
    assert metric["a_cpu"]["threshold"] == 0.0
    assert metric["a_cpu"]["alerts"] == metric["b_cpu"]["alerts"] == 2
    assert math.isclose(trace["a"]["normal_p95"], 2.9, abs_tol=1e-12)
    assert trace["a"]["alert"] == 0  # 8.7 bang 3 * 2.9.
    assert trace["b"]["alert"] == 1
    assert log["a"]["error_count"] == log["b"]["error_count"] == 1
    assert result["ranking"] == ["b", "a"]
    assert [row["score"] for row in result["services"]] == [4, 3]
    assert calculate(normal, normal, nt, nt, empty_log, meta)["abstained"]
    assert calculate(normal[list(reversed(normal.columns))], incident[list(reversed(incident.columns))], nt, it, logs, meta) == result
    unavailable = calculate(normal, incident, empty_trace, empty_trace, empty_log, {**meta, "logs_available": False})
    assert all(not row["available"] for row in unavailable["logs"])
    assert unavailable["tie_groups"] == [{"score": 2, "services": ["a", "b"]}]
    normal_only = calculate(normal, incident, nt, it, logs,
                            {**meta, "observed_services": ["normal-only"]})
    assert next(row for row in normal_only['services'] if row['service']=='normal-only')['score']==0
    assert next(row for row in normal_only['logs'] if row['service']=='normal-only')['error_count']==0
    equality = calculate(
        pd.DataFrame({"time": [0, 1], "a_x": [-1.0, 1.0]}),
        pd.DataFrame({"time": [2, 3], "a_x": [3.0, 4.0]}),
        empty_trace, empty_trace, empty_log,
        {"metric_services": {"a_x": "a"}, "logs_available": True},
    )
    assert equality["metrics"][0]["threshold"] == 3.0
    assert equality["metrics"][0]["alerts"] == 1
    nonfinite = calculate(
        pd.DataFrame({"time": [0, 1, 2], "a_x": [0.0, 0.0, np.nan]}),
        pd.DataFrame({"time": [3, 4, 5], "a_x": [1.0, np.inf, np.nan]}),
        empty_trace, empty_trace, empty_log,
        {"metric_services": {"a_x": "a"}, "logs_available": True},
    )
    assert nonfinite["metrics"][0]["alerts"] == 1
    assert nonfinite["metrics"][0]["normal_nonfinite"] == 1
    assert nonfinite["metrics"][0]["incident_nonfinite"] == 2
    no_normal = calculate(
        pd.DataFrame({"time": [0], "a_x": [0.0]}),
        pd.DataFrame({"time": [1], "a_x": [1.0]}),
        empty_trace, empty_trace, empty_log,
        {"metric_services": {"a_x": "a"}, "logs_available": True},
    )
    assert not no_normal["metrics"][0]["available"] and no_normal["abstained"]
    try:
        calculate(normal, incident, pd.DataFrame({"service": ["a"], "duration": [-1.0]}), it, logs, meta)
    except ValueError as error:
        assert "Duration am" in str(error)
    else:
        raise AssertionError("Duration am khong bi tu choi.")
    return {"status": "PASS", "checks": ["manual_metric_score", "linear_p95", "strict_metric_boundary", "strict_trace_boundary", "keyword_once_per_row", "normal_control", "column_permutation", "missing_logs", "ties", "nonfinite", "insufficient_normal", "negative_duration", "normal_only_identity_zero_score"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.input_dir is not None:
        assert args.input_dir.resolve()==Path('D:/RCA-ext/work/T-017/example-input-run-dev-005').resolve()
        assert args.out.resolve()==Path('D:/RCA-flashticket/results/T-020/trung-gian/method_evidence/runs/simplerca-arithmetic-001.json').resolve()

    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, allow_nan=False))
    if args.input_dir is None:
        if args.self_test:
            return
        parser.error("Can --input-dir hoac --self-test.")
    if args.out is None:
        parser.error("Can --out khi tinh dau vao file.")
    paths = {name: args.input_dir / name for name in FILENAMES}
    for path in paths.values():
        if not path.is_file():
            raise FileNotFoundError(path)
    frames = [pd.read_csv(paths[name]) for name in FILENAMES[:4]]
    logs = pd.read_csv(paths["incident_logs.csv"], keep_default_na=False)
    metadata = json.loads(paths["metadata.json"].read_text(encoding="utf-8"))
    result = calculate(*frames, logs, metadata)
    result["input_files"] = [
        {"name": name, "bytes": paths[name].stat().st_size, "sha256": hashlib.sha256(paths[name].read_bytes()).hexdigest()}
        for name in FILENAMES
    ]
    result["runtime"] = {"numpy": np.__version__, "pandas": pd.__version__}
    with args.out.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.out), "services": len(result["services"]), "metrics": len(result["metrics"]), "abstained": result["abstained"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
