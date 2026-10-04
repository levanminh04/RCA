"""T-015: one predetermined Train Ticket dev case, serial MicroRank checks.

Only this script and results/T-015/runs/tt-local are written. Parquet I/O is
direct in a pinned EC2 environment, or delegated to existing Windows py312 via
a pipe while all model code runs in py312-pin.
Fresh worker processes release graphs/matrices between checks. Timing on the
shared laptop is observation, never an official benchmark.
"""
from __future__ import annotations

import argparse
import csv
import ctypes
import gc
import hashlib
import io
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/T-015/runs/tt-local"
CASE = "re2tt_ts-auth-service_cpu_1"
ALLOWED_CASES = {CASE, "re2tt_ts-route-service_mem_1", "re2tt_ts-route-service_socket_1"}
SOURCE = None
INJECT_FILE = None
COLS = ["traceID", "spanID", "parentSpanID", "serviceName", "methodName",
        "operationName", "startTime", "duration"]
PIN_PYTHON = "D:/RCA-ext/envs/py312-pin/Scripts/python.exe"
IO_PYTHON = "D:/RCA-ext/envs/py312/Scripts/python.exe"
STEPS = ["primary", "columns_reversed", "rows_shuffled", "seed1_repeat", "half300", "two_normal"]
GUARD_ONE = 25 * 60
GUARD_AGGREGATE = 45 * 60
FREE_MIN_MIB = 3000


def timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def memory():
    if os.name != "nt":
        values = {}
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, value = line.split(":", 1)
            values[key] = int(value.strip().split()[0])
        return {"free_mib": round(values["MemAvailable"] / 1024, 1),
                "total_mib": round(values["MemTotal"] / 1024, 1),
                "load_percent": round(100 * (1 - values["MemAvailable"] / values["MemTotal"]), 1)}
    class MemoryStatus(ctypes.Structure):
        _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                    ("total", ctypes.c_ulonglong), ("available", ctypes.c_ulonglong),
                    ("total_page", ctypes.c_ulonglong), ("available_page", ctypes.c_ulonglong),
                    ("total_virtual", ctypes.c_ulonglong), ("available_virtual", ctypes.c_ulonglong),
                    ("available_extended", ctypes.c_ulonglong)]
    status = MemoryStatus()
    status.length = ctypes.sizeof(MemoryStatus)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise OSError("Cannot inspect free physical memory")
    return {"free_mib": round(status.available / 2**20, 1),
            "total_mib": round(status.total / 2**20, 1), "load_percent": status.load}


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def save_json(path, result):
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, allow_nan=False, indent=2)
        stream.write("\n")


def event(step, phase, **fields):
    record = {"utc": timestamp(), "step": step, "phase": phase, **fields}
    with open(OUT / "progress.jsonl", "a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps(record, ensure_ascii=False, allow_nan=False), flush=True)


def load_window(step):
    import pandas as pd
    source = SOURCE or ROOT / "data/rcaeval" / CASE / "traces.parquet"
    incident_file = INJECT_FILE or source.parent / "inject_time.txt"
    incident = int(incident_file.read_text().strip()) * 1_000_000
    half = 300 if step == "half300" else 600
    event(step, "io_start", source=str(source), half_seconds=half, memory=memory())
    io_code = """import json, pandas as pd, pyarrow.parquet as pq, sys
source, marker, half = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])*1000000
cols = json.loads(sys.argv[4])
raw = pd.read_parquet(source, columns=cols)
win = raw.loc[(raw.startTime>=marker-half)&(raw.startTime<marker+half)]
full_counts=raw.groupby('traceID').size()
window_counts=win.groupby('traceID').size()
cut=int((full_counts.reindex(window_counts.index)>window_counts).sum())
metric_names=pq.ParquetFile(sys.argv[5]).schema.names
meta={'raw_spans':len(raw),'window_spans':len(win),'window_trace_count':len(window_counts),
      'traces_missing_spans_due_to_window':cut,
      'spans_ending_after_window_upper':int((win.startTime+win.duration>=marker+half).sum()),
      'metric_columns':metric_names,'io_python':sys.version,'io_pandas':pd.__version__}
print(json.dumps(meta),file=sys.stderr)
win.to_csv(sys.stdout,index=False)
"""
    started = time.monotonic()
    try:
        import pyarrow.parquet as pq
        raw = pd.read_parquet(source, columns=COLS)
        data = raw.loc[(raw.startTime >= incident-half*1_000_000) &
                       (raw.startTime < incident+half*1_000_000)].reset_index(drop=True)
        raw_counts = raw.groupby("traceID").size()
        window_counts = data.groupby("traceID").size()
        metric_path = source.parent / "metrics.parquet"
        metric_names = pq.ParquetFile(metric_path).schema.names if metric_path.exists() else []
        meta = {"raw_spans":len(raw), "window_spans":len(data), "window_trace_count":len(window_counts),
                "traces_missing_spans_due_to_window":int((raw_counts.reindex(window_counts.index)>window_counts).sum()),
                "spans_ending_after_window_upper":int((data.startTime+data.duration>=incident+half*1_000_000).sum()),
                "metric_columns":metric_names,"io_python":sys.version,"io_pandas":pd.__version__,
                "io_mode":"direct parquet in pinned environment"}
        del raw, raw_counts, window_counts
    except ImportError:
        if os.name != "nt":
            raise  # Portable EC2 environment must explicitly include its parquet engine.
        read = subprocess.run([IO_PYTHON, "-B", "-c", io_code, str(source), str(incident), str(half),
                               json.dumps(COLS), str(source.parent / "metrics.parquet")],
                              capture_output=True, text=True, check=True, timeout=GUARD_ONE)
        meta = json.loads(read.stderr.strip().splitlines()[-1])
        data = pd.read_csv(io.StringIO(read.stdout), dtype={column: str for column in COLS[:-2]})
        meta["io_mode"] = "py312 I/O through CSV pipe; calculation in py312-pin"
        del read
    gc.collect()
    if step == "two_normal":
        # Both starts and ends must precede the injection. Otherwise a long
        # pre-injection span could contain post-injection observations.
        data = data.loc[(data.startTime < incident) &
                        (data.startTime + data.duration < incident)].reset_index(drop=True)
        boundary = incident - 300_000_000
    else:
        boundary = incident
    if step == "columns_reversed":
        data = data.loc[:, list(reversed(COLS))]
    elif step == "rows_shuffled":
        data = data.sample(frac=1, random_state=2026).reset_index(drop=True)
    meta.update(source=str(source), source_sha256=digest(source), incident_time_us=incident,
                boundary_used_us=boundary, half_seconds=half, scoring_input_spans=len(data),
                io_elapsed_observed_seconds=round(time.monotonic() - started, 3))
    event(step, "io_complete", spans=len(data), trace_count=meta["window_trace_count"], memory=memory())
    return data, boundary, meta


def graph_inventory(result, io_meta):
    service_set = set(result.get("operation_services", {}).values())
    current_services = set()
    edges = set()
    operation_edge_services = set()
    groups = result.get("groups", {})
    for group in groups.values():
        graph = group.get("graph", {})
        for parent, children in graph.get("operation_operation", {}).items():
            left = result["operation_services"][parent]
            current_services.add(left)
            for child in children:
                right = result["operation_services"][child]
                operation_edge_services.update([left, right])
                if left != right:
                    edges.add((left, right))
    involved = {service for pair in edges for service in pair}
    metric_services = {column.split("_", 1)[0] for column in io_meta["metric_columns"] if column.startswith("ts-") and "_" in column}
    full_services = result.get("service_ranks_full", [])
    top_services = result.get("service_ranks_top11", [])
    return {"metric_services": sorted(metric_services), "observed_span_services": sorted(service_set),
            "current_graph_services": sorted(current_services), "service_edges": [list(pair) for pair in sorted(edges)],
            "services_without_interservice_edge": sorted(current_services - involved),
            "services_without_any_operation_edge": sorted(current_services - operation_edge_services),
            "metric_services_absent_in_trace": sorted(metric_services - service_set),
            "ranked_services_absent_in_trace": sorted(set(full_services) - service_set),
            "isolated_services_in_full_rank": sorted((current_services - involved) & set(full_services)),
            "isolated_services_in_top11_rank": sorted((current_services - involved) & set(top_services)),
            "services_removed_only_by_top11": sorted(set(full_services) - set(top_services))}


def census(data, boundary, step):
    import pandas as pd
    event(step, "census_start", memory=memory())
    frame = data.loc[:, COLS]
    span_keys = pd.MultiIndex.from_frame(frame[["traceID", "spanID"]])
    parent_keys = pd.MultiIndex.from_arrays([frame.traceID, frame.parentSpanID])
    resolved = parent_keys.isin(span_keys)
    root_tokens = frame.parentSpanID.isna() | frame.parentSpanID.isin(["", "0", "0000000000000000", "None", "nan"])
    unresolved = ~resolved & ~root_tokens
    observed_roots = ~resolved
    root_counts = pd.Series(root_tokens.to_numpy(), index=frame.traceID).groupby(level=0).sum()
    observed_root_counts = pd.Series(observed_roots, index=frame.traceID).groupby(level=0).sum()
    end = frame.startTime + frame.duration
    before_ids = set(frame.loc[end < boundary, "traceID"])
    after_ids = set(frame.loc[end >= boundary, "traceID"])
    answer = {"spans": len(frame), "trace_count": int(frame.traceID.nunique()),
              "duplicate_trace_span_pairs": int(span_keys.duplicated().sum()),
              "spanID_reused_across_traces": int(frame.spanID.duplicated().sum()),
              "resolved_parent_spans": int(resolved.sum()),
              "explicit_root_spans": int(root_tokens.sum()), "unknown_parent_spans": int(unresolved.sum()),
              "traces_with_multiple_explicit_roots": int((root_counts > 1).sum()),
              "traces_with_multiple_observed_roots_including_unknown_parent": int((observed_root_counts > 1).sum()),
              "traceIDs_on_both_sides_of_boundary": len(before_ids & after_ids),
              "span_start_before_boundary_end_after": int(((frame.startTime < boundary) & (end >= boundary)).sum()),
              "interpretation": "unknown parent may mean missing instrumentation or window truncation; not a guessed original root/kind policy"}
    event(step, "census_complete", memory=memory())
    return answer


def compare(primary, current):
    checks = {"status": primary["status"] == current["status"],
              "counts": primary.get("counts") == current.get("counts"),
              "ranks_top11": primary["ranks"] == current["ranks"],
              "full_ranks": primary.get("full_ranks") == current.get("full_ranks"),
              "scores": primary.get("scores") == current.get("scores"),
              "spectrum": primary.get("spectrum") == current.get("spectrum"),
              "baseline_slo_ms": primary.get("baseline_slo_ms") == current.get("baseline_slo_ms")}
    for name in ["normal", "anomaly"]:
        original_group = primary.get("groups", {}).get(name, {})
        current_group = current.get("groups", {}).get(name, {})
        checks[name + "_weights"] = original_group.get("official", {}).get("weights") == current_group.get("official", {}).get("weights")
        checks[name + "_tracecounts"] = original_group.get("official", {}).get("tracecounts") == current_group.get("official", {}).get("tracecounts")
        checks[name + "_audit"] = original_group.get("audit") == current_group.get("audit")
    assert all(checks.values()), checks
    return checks


def worker(step):
    stopped = threading.Event()
    def heartbeat():
        start = time.monotonic()
        while not stopped.wait(10):
            rss = None
            if os.name != "nt":
                for line in Path("/proc/self/status").read_text().splitlines():
                    if line.startswith("VmRSS:"):
                        rss = round(int(line.split()[1])/1024, 1)
            event(step, "heartbeat", elapsed_seconds=round(time.monotonic() - start, 1),
                  rss_mib=rss, memory=memory())
    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    started = time.monotonic()
    path = OUT / (step + ".json")
    meta = None
    try:
        data, boundary, meta = load_window(step)
        sys.path.insert(0, str(ROOT / "src"))
        from microrank import microrank
        event(step, "method_start", python=sys.version, hash_seed=os.environ.get("PYTHONHASHSEED"), memory=memory())
        method_start = time.monotonic()
        with open(OUT / (step + "-method.log"), "w", encoding="utf-8") as method_log:
            import contextlib
            with contextlib.redirect_stdout(method_log):
                result = microrank(data, boundary, include_graph=step == "primary")
        method_seconds = round(time.monotonic() - method_start, 3)
        assert result.get("variant") == "MicroRank-RCAEval sửa đầu vào"
        assert result.get("counts", {}).get("overlap", 0) == 0
        assert all(math.isfinite(v) and v >= 0 for cells in result.get("spectrum", {}).values() for v in cells.values())
        if result["status"] == "ok":
            assert result["ranks"] and result.get("scores") and result.get("full_ranks")
            assert all(math.isfinite(value) for value in result["scores"].values())
        else:
            assert not result["ranks"]
        result["io_metadata"] = meta
        result["run_metadata"] = {"step": step, "case": CASE, "hash_seed": os.environ.get("PYTHONHASHSEED"),
                                  "method_elapsed_observed_seconds": method_seconds,
                                  "timing_is_official": False, "fallback": False,
                                  "reason": "a" if step == "seed1_repeat" else "b",
                                  "purpose": step, "source": meta["source"]}
        save_json(path, result)
        if step == "primary":
            # Complete primary result, including prior/vector/graphs, is the
            # hand-example snapshot. No duplicate serialization or huge copy.
            path.replace(OUT / "example.json")
            event(step, "example_ready", path=str(OUT / "example.json"), method_seconds=method_seconds,
                  status=result["status"], counts=result.get("counts"), memory=memory())
            inventory = graph_inventory(result, meta)
            summary = {"io_metadata": meta, "inventory": inventory, "census": census(data, boundary, step),
                       "counts": result.get("counts"), "status": result["status"],
                       "service_ranks_full": result.get("service_ranks_full", []),
                       "service_ranks_top11": result.get("service_ranks_top11", [])}
            assert inventory["ranked_services_absent_in_trace"] == []
            # Label is read for explanation only AFTER ranking/example are saved.
            root = CASE[len("re2tt_"):].rsplit("_", 2)[0]
            ranks_full = result.get("service_ranks_full", [])
            ranks_top11 = result.get("service_ranks_top11", [])
            summary["label_after_ranking"] = {"root_service": root,
                "rank_full": ranks_full.index(root)+1 if root in ranks_full else None,
                "rank_top11": ranks_top11.index(root)+1 if root in ranks_top11 else None,
                "coverage_ceiling_full_for_this_case": int(root in ranks_full),
                "coverage_ceiling_top11_for_this_case": int(root in ranks_top11)}
            save_json(OUT / "primary-summary.json", summary)
        elif step in ["columns_reversed", "rows_shuffled", "seed1_repeat"]:
            primary = json.loads((OUT / "example.json").read_text(encoding="utf-8"))
            save_json(OUT / (step + "-comparison.json"), compare(primary, result))
        elif step == "two_normal":
            save_json(OUT / "two-normal-summary.json", {"status": result["status"], "counts": result.get("counts"),
                "returned_operations": len(result["ranks"]), "interpretation": "If any ranking is returned, it is a false alarm on pre-injection windows, not a meaningful root cause"})
        event(step, "complete", status=result["status"], method_seconds=method_seconds,
              elapsed_seconds=round(time.monotonic()-started,3), memory=memory())
    except Exception as error:
        save_json(OUT / (step + "-failed.json"), {"step": step, "case": CASE, "exception": repr(error),
                   "traceback": traceback.format_exc(), "io_metadata": meta,
                   "elapsed_observed_seconds": round(time.monotonic()-started,3)})
        event(step, "failed", error=repr(error), elapsed_seconds=round(time.monotonic()-started,3))
        raise
    finally:
        stopped.set(); thread.join(timeout=2)


def orchestrate(selected_steps):
    aggregate_started = time.monotonic()
    attempt = time.strftime("%Y%m%dT%H%M%SZ",time.gmtime())
    records = []
    if (OUT / "run-ledger.csv").exists():
        with open(OUT / "run-ledger.csv",encoding="utf-8-sig",newline="") as stream:
            records = list(csv.DictReader(stream))
    save_json(OUT / ("plan-"+attempt+".json"), {"case": CASE, "steps": selected_steps,
        "estimate_before_scores": "6 serial checks x <=5min plus <=3min I/O = <=33min; shared-laptop timing is not official",
        "guard_per_worker_seconds": GUARD_ONE, "aggregate_guard_seconds": GUARD_AGGREGATE,
        "minimum_free_mib_before_worker": FREE_MIN_MIB, "no_heavy_parallel_worker": True,
        "code_hashes": {str(path.relative_to(ROOT)): digest(path) for path in sorted((ROOT/'src/microrank').glob('*.py'))},
        "script_sha256": digest(Path(__file__))})
    for step in selected_steps:
        expected = OUT / ("example.json" if step == "primary" else step+".json")
        if expected.exists():
            event(step,"not_rerun_existing_output",path=str(expected))
            continue
        if any((OUT / (step + suffix)).exists()
               for suffix in ["-failed.json", "-timeout.json", "-worker.log"]):
            event(step,"not_started_preserve_previous_attempt",
                  interpretation="Use a new output directory for a retry; previous failed logs/results are retained")
            break
        if step in ["columns_reversed", "rows_shuffled", "seed1_repeat"] and not (OUT / "example.json").exists():
            raise ValueError("primary example.json is required before invariance/repetition checks")
        elapsed = time.monotonic()-aggregate_started
        if elapsed >= GUARD_AGGREGATE:
            event(step, "not_started_aggregate_guard", elapsed_seconds=round(elapsed,3))
            break
        available = memory()
        if available["free_mib"] < FREE_MIN_MIB:
            event(step, "not_started_insufficient_memory", memory=available)
            save_json(OUT / (step + "-not-started-"+attempt+".json"), {"step":step,"reason":"insufficient free physical memory","memory":available})
            break
        env = dict(os.environ)
        cache = str((OUT / "cache").resolve()); temporary = str((OUT / "tmp").resolve())
        Path(cache).mkdir(exist_ok=True); Path(temporary).mkdir(exist_ok=True)
        env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="1" if step == "seed1_repeat" else "0",
                   XDG_CACHE_HOME=cache, MPLCONFIGDIR=str(OUT/"cache/mpl"),
                   TMP=temporary,TEMP=temporary,TMPDIR=temporary,
                   OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
        event(step, "launch", memory=available, hash_seed=env["PYTHONHASHSEED"])
        started = time.monotonic()
        with open(OUT / (step + "-worker.log"), "w", encoding="utf-8") as log:
            command = [PIN_PYTHON if os.name == "nt" else sys.executable,"-B",str(Path(__file__)),"--worker",step,
                       "--code-root",str(ROOT),"--out",str(OUT),"--case",CASE]
            if SOURCE: command += ["--input-parquet",str(SOURCE)]
            if INJECT_FILE: command += ["--inject-file",str(INJECT_FILE)]
            process = subprocess.Popen(command, cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            try:
                code = process.wait(timeout=min(GUARD_ONE, GUARD_AGGREGATE-elapsed))
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    # Kill only this runner's own worker tree, including the
                    # Windows venv forwarding child. Never touch other jobs.
                    subprocess.run(["taskkill","/PID",str(process.pid),"/T","/F"],capture_output=True)
                else:
                    process.kill()
                process.wait()
                code = -1
                save_json(OUT / (step + "-timeout.json"), {"step":step,"case":CASE,"status":"timeout","elapsed_seconds":time.monotonic()-started})
        records.append({"case":CASE,"file_source":str(SOURCE or ROOT/'data/rcaeval'/CASE/'traces.parquet'),
                        "method":"MicroRank-RCAEval sửa đầu vào","purpose":step,
                        "reason":"a" if step == "seed1_repeat" else "b",
                        "exit_code":code,"elapsed_observed_seconds":round(time.monotonic()-started,3),
                        "timing_is_official":False})
        with open(OUT / "run-ledger.csv","w",encoding="utf-8-sig",newline="") as stream:
            writer=csv.DictWriter(stream,list(records[0]));writer.writeheader();writer.writerows(records)
        event(step,"worker_finished",exit_code=code,elapsed_seconds=records[-1]["elapsed_observed_seconds"],memory=memory())
        if code != 0:
            break
    save_json(OUT / ("orchestrator-summary-"+attempt+".json"), {"records":records,"aggregate_elapsed_observed_seconds":round(time.monotonic()-aggregate_started,3),
                                                  "timing_is_official":False,"completed_steps":len(records)})


def main():
    global ROOT, OUT, CASE, SOURCE, INJECT_FILE
    parser=argparse.ArgumentParser()
    parser.add_argument("--worker",choices=STEPS)
    parser.add_argument("--steps",default=",".join(STEPS))
    parser.add_argument("--input-parquet",type=Path)
    parser.add_argument("--inject-file",type=Path)
    parser.add_argument("--out",type=Path)
    parser.add_argument("--code-root",type=Path)
    parser.add_argument("--case",choices=sorted(ALLOWED_CASES))
    args=parser.parse_args()
    if args.code_root:ROOT=args.code_root.resolve()
    elif not (ROOT/"src/microrank/__init__.py").exists():
        ROOT=next(parent for parent in Path(__file__).resolve().parents if (parent/"src/microrank/__init__.py").exists())
    OUT=args.out.resolve() if args.out else ROOT / "results/T-015/runs/tt-local"
    if args.input_parquet:SOURCE=args.input_parquet.resolve()
    if args.inject_file:INJECT_FILE=args.inject_file.resolve()
    if args.case:CASE=args.case
    elif SOURCE:CASE=SOURCE.parent.name
    assert CASE in ALLOWED_CASES,"not an allowed predetermined dev case"
    assert SOURCE is None or SOURCE.parent.name==CASE,"case/path mismatch"
    source_path=SOURCE or ROOT / "data/rcaeval" / CASE / "traces.parquet"
    assert INJECT_FILE is None or INJECT_FILE.parent==source_path.parent,"inject source mismatch"
    OUT.mkdir(parents=True,exist_ok=True)
    if args.worker:
        worker(args.worker)
    else:
        selected=args.steps.split(",")
        assert all(step in STEPS for step in selected)
        orchestrate(selected)


if __name__ == "__main__":
    main()
