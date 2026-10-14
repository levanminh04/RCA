"""T-032: observe one original SimpleRCA call without invoking diagnosis again.

Only exact adapter/prepare/core_input/diagnose code objects are traced. Store
actual grouped inputs and the full native return, including unavailable rows,
abstain, partial state and exceptions. Existing profile hooks remain untouched.
Serializer reuse does not import or execute the MicroRank method.
"""
from __future__ import annotations

from dataclasses import asdict
import importlib
import json
import os
from pathlib import Path
import platform
import sys
import threading
import time
import traceback

from capture_microrank import CaptureError, MicroRankCapture, _sha256


class SimpleRcaCapture(MicroRankCapture):
    def __init__(self, output_directory, dataset):
        super().__init__(output_directory)
        if dataset not in ("RE2-TT", "Nezha-OB"):
            raise ValueError("unknown SimpleRCA adapter dataset")
        self.dataset = dataset

    def __enter__(self):
        if self._installed or self._closed or sys.gettrace() is not None:
            raise CaptureError("capture cannot be reused or nested with another trace hook")
        self.np = importlib.import_module("numpy")
        self.pd = importlib.import_module("pandas")
        native = importlib.import_module("simplerca.core")
        prepared = importlib.import_module("simplerca.adapter")
        adapter = importlib.import_module("p3.adapters.simplerca" if self.dataset == "RE2-TT" else "p3.adapters.nezha")
        functions = {"adapter": adapter.chay if self.dataset == "RE2-TT" else adapter._simple,
                     "native": native.diagnose}
        if self.dataset == "RE2-TT":
            functions.update(prepare=prepared.prepare, core_input=prepared.core_input)
        self._targets = {fn.__code__: name for name, fn in functions.items()}
        self._prior_trace, self._prior_profile = sys.gettrace(), sys.getprofile()
        self._owner_thread = threading.get_ident()
        self._table_content = {}
        self.directory.mkdir(parents=True, exist_ok=False)
        self._started = time.perf_counter()
        self._write_json("capture-start.json", {
            "schema": "T-032.simplerca-observation.v1", "status": "started", "dataset": self.dataset,
            "python": sys.version, "platform": platform.platform(),
            "packages": {"numpy": self.np.__version__, "pandas": self.pd.__version__},
            "sources": {name: {"path": str(Path(fn.__code__.co_filename).resolve()),
                "sha256": _sha256(fn.__code__.co_filename), "first_line": fn.__code__.co_firstlineno}
                for name, fn in functions.items()},
            "thread_environment": {key: os.environ.get(key) for key in
                ("PYTHONHASHSEED", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")},
            "scope": "one original adapter/diagnose call; no replacement or second method call",
            "reuse": "T028 totals/rankings remain reusable; these files add absent full native return and row evidence",
            "row_positions": "zero-based positions within the observed adapter projection or native channel; ordered indexes retained",
            "finite_encoding": "capture_microrank tagged JSON and parquet special-state columns",
        })
        self._hook = self._trace
        self._installed = True
        sys.settrace(self._hook)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._installed:
            if threading.get_ident() != self._owner_thread or sys.gettrace() is not self._hook:
                self.errors.append({"stage": "exit", "error": "owner thread or trace hook changed"})
            sys.settrace(self._prior_trace)
            self._installed = False
        self._closed = True
        try:
            profile_restored = sys.getprofile() is self._prior_profile
            if not profile_restored:
                self.errors.append({"stage": "exit", "error": "profile hook changed"})
            counts = {name: sum(call["function"] == name for call in self._calls) for name in self._targets.values()}
            adapters = [call for call in self._calls if call["function"] == "adapter"]
            natives = [call for call in self._calls if call["function"] == "native"]
            adapter = adapters[0] if len(adapters) == 1 else {}
            threw = adapter.get("outcome") == "exception" and bool(adapter.get("exceptions"))
            returned_status = adapter.get("adapter_status")
            status = "ERROR" if threw else returned_status
            if counts.get("adapter") != 1 or any(value > 1 for value in counts.values()) or self._active:
                self.errors.append({"stage": "completeness", "error": "extra/missing adapter or unfinished frames", "counts": counts})
            if status in ("OK", "NO_EVIDENCE"):
                expected = {"adapter": 1, "native": 1}
                if self.dataset == "RE2-TT":
                    expected.update(prepare=1, core_input=1)
                if counts != expected or any(call["outcome"] != "return" for call in self._calls):
                    self.errors.append({"stage": "completeness", "error": "successful adapter missing returned stages", "counts": counts})
            self.summary = {
                "schema": "T-032.simplerca-observation.v1", "dataset": self.dataset,
                "status": "capture_failed" if self.errors else "captured_unverified_replay",
                "adapter_status": status, "adapter_returned_status": returned_status,
                "adapter_status_source": "observed_adapter_exception" if threw else "adapter_return",
                "adapter_outcome": adapter.get("outcome"), "adapter_threw": threw,
                "adapter_exception": ({key: adapter["exceptions"][-1][key] for key in ("type", "message")} if threw else None),
                "native_outcome": natives[0]["outcome"] if len(natives) == 1 else None,
                "native_status": natives[0].get("native_status") if len(natives) == 1 else None,
                "calls": self._calls, "call_counts": counts, "errors": self.errors,
                "profile_restored": profile_restored, "trace_restored": sys.gettrace() is self._prior_trace,
                "caller_exception": None if exc_type is None else {"type": exc_type.__name__, "message": str(exc_value)},
                "elapsed_seconds": time.perf_counter() - self._started,
                "observer_callback_seconds": self._callback_seconds, "artifacts": list(self._artifacts),
                "replay_check": "OPEN: full exact frozen comparison and native intermediate restoration required before use",
            }
            self._write_json("capture.json", self.summary)
        except BaseException as error:
            self.errors.append({"stage": "finalize", "type": type(error).__name__, "error": str(error)})
        finally:
            self._active.clear()
            self._array_cache.clear()
            self._table_content.clear()
        return False

    def require_complete(self):
        if not self._closed or self.summary is None or self.errors:
            raise CaptureError("SimpleRCA observation incomplete: " + repr(self.errors))
        return self.summary

    def _save_table(self, relative, value):
        signature = self._table_signature(value)
        key = json.dumps(signature, sort_keys=True)
        if key not in self._table_content:
            meta = self._table(relative, value)
            meta["signature"] = signature
            self._table_content[key] = meta
        return self._table_content[key]

    def _groups(self, stem, mapping):
        if mapping is None:
            return {"unavailable": True}
        rows = [(channel, position, value) for channel, values in mapping.items() for position, value in enumerate(values)]
        frame = self.pd.DataFrame({
            "channel": self.pd.Series([row[0] for row in rows], dtype=object),
            "position": self.pd.Series([row[1] for row in rows], dtype="int64"),
            "value": self.pd.Series([row[2] for row in rows], dtype=object),
        })
        return {"unavailable": False, "channels": self._encode(list(mapping)),
                "lengths": [len(values) for values in mapping.values()],
                "table": self._save_table(stem + ".parquet", frame)}

    def _core_input(self, stem, values):
        return {**{key: self._groups(stem + "-" + key, values[key]) for key in
                    ("normal_metrics", "incident_metrics", "normal_traces", "incident_traces", "incident_logs")},
                "metric_services": self._encode(values["metric_services"]),
                "observed_services": self._encode(values["observed_services"])}

    def _projections(self, local):
        if self.dataset == "RE2-TT":
            source = {"metric": local["metric_win"], "spans": local["spans"], "logs": local["logs"]}
            columns = {"metric": None, "spans": ("serviceName", "startTime", "duration", "traceID", "spanID", "parentSpanID"),
                       "logs": ("timestamp", "container_name", "message")}
        else:
            payload = local["payload"]
            source = {"spans": payload["spans"], "logs": payload["logs"]}
            columns = {"spans": ("serviceName", "startTime", "duration", "_start_ns", "_end_ns", "traceID", "spanID", "parentSpanID"),
                       "logs": ("timestamp", "_timestamp_ns", "container_name", "message")}
        return {key: None if frame is None else frame if columns[key] is None else frame[
                [column for column in columns[key] if column in frame]] for key, frame in source.items()}

    def _trace(self, frame, event, arg):
        name = self._targets.get(frame.f_code)
        if name is None:
            return None
        began = time.perf_counter()
        try:
            if event == "call":
                frame.f_trace_lines = False
                frame.f_trace_opcodes = False
                self._sequence += 1
                call = {"id": self._sequence, "function": name, "exceptions": [], "entry": {}}
                self._active[id(frame)] = call
                local, entry = frame.f_locals, call["entry"]
                if name == "adapter":
                    entry["tables"] = {key: {"unavailable": True} if value is None else
                        self._save_table("adapter-" + key + ".parquet", value) for key, value in self._projections(local).items()}
                    if self.dataset == "RE2-TT":
                        entry["t_seconds"] = self._encode(local["t"])
                    else:
                        payload = local["payload"]
                        entry["t_ns"], entry["guard"] = self._encode(payload["t_ns"]), self._encode(local["guard"])
                        entry["metric_arrays"] = {key: self._groups("adapter-" + key,
                            {column: values[field] for column, values in payload["metric_arrays"].items()})
                            for key, field in (("normal_metrics", "normal"), ("incident_metrics", "anomalous"))}
                        entry["window"] = self._encode(payload.get("window"))
                elif name == "native":
                    entry["inputs"] = self._core_input("native-input", local)
                    entry["config"] = self._encode(asdict(local["config"]))
                elif name == "prepare":
                    entry["parameters"] = {key: self._encode(local[key]) for key in ("boundary", "half", "aliases")}
            elif event == "exception":
                kind, value, _ = arg
                self._active[id(frame)]["exceptions"].append({"type": kind.__name__, "message": str(value), "line": frame.f_lineno})
            elif event == "return":
                call = self._active.pop(id(frame))
                call["outcome"] = "exception" if arg is None and call["exceptions"] else "return"
                snapshot = self._snapshot(name, frame, arg, call)
                relative = "calls/{:03d}-{}.json".format(call["id"], name)
                self._write_json(relative, snapshot)
                call["path"] = relative
                call.pop("entry", None)
                self._calls.append(call)
        except BaseException as error:
            self.errors.append({"stage": "observer", "function": name, "event": event,
                "type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc()})
        finally:
            self._callback_seconds += time.perf_counter() - began
        return self._hook

    def _snapshot(self, name, frame, returned, call):
        local = frame.f_locals
        out = {"function": name, "entry": call["entry"], "outcome": call["outcome"], "exceptions": call["exceptions"]}
        if name == "adapter":
            call["adapter_status"] = returned.get("status") if isinstance(returned, dict) else None
            out["return"] = self._encode(returned)
            out["input_after_signatures"] = {key: {"unavailable": True} if value is None else
                self._table_signature(value) for key, value in self._projections(local).items()}
            if self.dataset == "Nezha-OB":
                out["metric_arrays_after"] = {key: self._groups("adapter-after-" + key,
                    {column: values[field] for column, values in local["payload"]["metric_arrays"].items()})
                    for key, field in (("normal_metrics", "normal"), ("incident_metrics", "anomalous"))}
                out["membership_positions"] = {key: self.np.flatnonzero(local[key].to_numpy()).tolist()
                                               for key in ("before", "after") if key in local}
            out["locals"] = {key: self._encode(local[key]) for key in ("shape", "obs", "observed", "mappings") if key in local}
        elif name == "native":
            call["native_status"] = returned.get("status") if isinstance(returned, dict) else None
            out["inputs_after"] = self._core_input("native-input-after", local)
            out["locals"] = {key: self._encode(local[key]) for key in
                ("metrics", "traces", "logs", "totals", "usable", "ranks", "groups", "status", "key", "service", "row") if key in local}
            self._write_json("native-result.json", self._encode(returned))
            out["return"] = {"path": "native-result.json"}
            if call["outcome"] == "return" and not isinstance(returned, dict):
                raise CaptureError("unexpected SimpleRCA native return type")
        elif name == "prepare":
            if returned is not None:
                out["prepared"] = {key: {"unavailable": True} if getattr(returned, key) is None else
                    {"signature": self._table_signature(getattr(returned, key)),
                     "storage": "signature only; exact values joined from saved adapter/native input rows"} for key in
                    ("normal_metrics", "incident_metrics", "normal_traces", "incident_traces", "incident_logs")}
                out["metric_services"] = self._encode(returned.metric_services)
                out["observed_services"] = self._encode(returned.observed_services)
            else:
                out["return"] = self._encode(returned)
        else:
            out["return"] = self._encode(returned) if returned is None else self._core_input("core-input-return", returned)
        return out
