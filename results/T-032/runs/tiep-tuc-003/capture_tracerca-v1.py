"""T-032: observe one unchanged TraceRCA adapter call and its native state.

The P3 adapter already uses sys.setprofile to capture ji. This observer only
uses sys.settrace on three exact Python code objects. It neither replaces a
function nor suppresses native DataFrame mutation/exception. Serialize native
normal/A rows and the actual SLO/support/confidence/ji dictionaries; derived
counts explicitly reference those observed flags, not MicroRank trace groups.
Evidence remains ineligible until the caller verifies the full frozen record.
"""
from __future__ import annotations

import importlib
import os
from pathlib import Path
import platform
import sys
import threading
import time
import traceback

from capture_microrank import CaptureError, MicroRankCapture, _sha256


class TraceRcaCapture(MicroRankCapture):
    """Serializer reuse only; no MicroRank code is imported or executed."""

    def __enter__(self):
        if self._installed or self._closed or sys.gettrace() is not None:
            raise CaptureError("capture cannot be reused or nested with another trace hook")
        self.np = importlib.import_module("numpy")
        self.pd = importlib.import_module("pandas")
        adapter = importlib.import_module("p3.adapters.tracerca")
        self.module = importlib.import_module("RCAEval.e2e.tracerca")
        functions = {"adapter": adapter.chay, "native": self.module.tracerca,
                     "operation_slo": self.module.get_operation_slo}
        self._targets = {fn.__code__: name for name, fn in functions.items()}
        self._prior_trace = sys.gettrace()
        self._prior_profile = sys.getprofile()
        self._owner_thread = threading.get_ident()
        self._table_content = {}
        self.directory.mkdir(parents=True, exist_ok=False)
        self._started = time.perf_counter()
        self._write_json("capture-start.json", {
            "schema": "T-032.tracerca-observation.v1", "status": "started",
            "python": sys.version, "platform": platform.platform(),
            "packages": {"numpy": self.np.__version__, "pandas": self.pd.__version__},
            "sources": {name: {"path": str(Path(fn.__code__.co_filename).resolve()),
                "sha256": _sha256(fn.__code__.co_filename), "first_line": fn.__code__.co_firstlineno}
                for name, fn in functions.items()},
            "thread_environment": {key: os.environ.get(key) for key in
                ("PYTHONHASHSEED", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")},
            "scope": "one original adapter/native/SLO call; trace hook only; existing adapter profile hook untouched",
            "counts_unit": "span rows, as used by native code; no grouping by traceID",
            "finite_encoding": "capture_microrank tagged JSON and parquet special-state columns",
            "native_mutation": "preserved; native input is the adapter's original deep copy",
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
                self.errors.append({"stage": "exit", "error": "original profile hook was not restored by adapter"})
            counts = {name: sum(call["function"] == name for call in self._calls) for name in self._targets.values()}
            if counts != {"adapter": 1, "native": 1, "operation_slo": 1} or self._active:
                self.errors.append({"stage": "completeness", "error": "missing/extra or unfinished frames", "counts": counts})
            adapters = [call for call in self._calls if call["function"] == "adapter"]
            natives = [call for call in self._calls if call["function"] == "native"]
            status = adapters[0].get("adapter_status") if len(adapters) == 1 else None
            self.summary = {
                "schema": "T-032.tracerca-observation.v1",
                "status": "capture_failed" if self.errors else "captured_unverified_replay",
                "adapter_status": status,
                "native_outcome": natives[0]["outcome"] if len(natives) == 1 else None,
                "calls": self._calls, "errors": self.errors, "profile_restored": profile_restored,
                "trace_restored": sys.gettrace() is self._prior_trace,
                "caller_exception": None if exc_type is None else {"type": exc_type.__name__, "message": str(exc_value)},
                "elapsed_seconds": time.perf_counter() - self._started,
                "observer_callback_seconds": self._callback_seconds, "artifacts": list(self._artifacts),
                "replay_check": "OPEN: full exact frozen comparison and intermediate restoration required before use",
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
            raise CaptureError("TraceRCA observation incomplete: " + repr(self.errors))
        return self.summary

    def _save_table(self, relative, value):
        import json
        signature = self._table_signature(value)
        key = json.dumps(signature, sort_keys=True)
        if key in self._table_content:
            return self._table_content[key]
        meta = self._table(relative, value)
        meta["signature"] = signature
        self._table_content[key] = meta
        return meta

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
                local = frame.f_locals
                if name == "adapter":
                    call["entry"]["input"] = self._save_table("adapter-input.parquet", local["spans"])
                    call["entry"]["t_seconds"] = self._encode(local["t"])
                elif name == "native":
                    call["entry"]["input_signature"] = self._table_signature(local["data"])
                    call["entry"]["inject_time_us"] = self._encode(local["inject_time"])
                    call["entry"]["dataset"] = self._encode(local["dataset"])
                    call["entry"]["kwargs"] = self._encode(local["kwargs"])
                else:
                    call["entry"]["input_signature"] = self._table_signature(local["span_df"])
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
        if name == "operation_slo":
            out["return"] = self._encode(returned)
            out["ordered_slo"] = self._encode(list((local.get("operation_slo") or {}).items()))
        elif name == "adapter":
            call["adapter_status"] = returned.get("status") if isinstance(returned, dict) else None
            out["return"] = self._encode(returned)
            out["locals"] = {key: self._encode(local[key]) for key in
                ("ji", "svc", "huu_han", "co_nan", "items", "shape", "obs") if key in local}
            if "amb" in local:
                out["ambiguous_pairs"] = self._encode(list(local["amb"].itertuples(index=False, name=None)))
            if "ji" in local and local["ji"] is not None:
                out["filter"] = [{"operation": self._encode(op), "ji": self._encode(value),
                    "kept": bool(self.np.isfinite(float(value))),
                    "reason": "finite" if self.np.isfinite(float(value)) else "nonfinite ji"}
                    for op, value in local["ji"].items()]
            out["input_after_signature"] = self._table_signature(local["spans"])
        else:
            for key in ("normal_slo", "operations", "support_dict", "confidence_dict", "ji_dict", "sorted_ji", "ranks", "op", "ji"):
                if key in local:
                    out[key] = self._encode(local[key])
            out["ordered_mappings"] = {key: self._encode(list(local[key].items())) for key in
                ("normal_slo", "support_dict", "confidence_dict", "ji_dict") if key in local}
            out["tables"] = {key: self._save_table("native-" + key + ".parquet", local[key])
                for key in ("normal_df", "anomal_df") if key in local}
            data = local["data"]
            out["native_input_after"] = self._save_table("native-input-after.parquet", data)
            ends = data["startTime"] + data["duration"]
            out["partition_positions"] = {"normal_df": self.np.flatnonzero((ends < local["inject_time"]).to_numpy()).tolist(),
                "anomal_df": self.np.flatnonzero((ends >= local["inject_time"]).to_numpy()).tolist(),
                "indexing": "zero-based physical positions in native-input-after; order/index retained"}
            anomalous = local.get("anomal_df")
            if anomalous is not None and "abnormal" in anomalous:
                flags = anomalous["abnormal"]
                out["count_operands_from_observed_flags"] = {
                    "unit": "span rows; derived diagnostic read of native flags, not a separate method result",
                    "total_abnormal_spans_A": int(flags.sum()),
                    "operations": [{"operation": self._encode(op),
                        "abnormal_spans_A": int(anomalous[anomalous["operation"] == op]["abnormal"].sum()),
                        "operation_spans_A": int(anomalous[anomalous["operation"] == op]["operation"].count())}
                        for op in anomalous.operation.unique()],
                }
            self._write_json("native-result.json", self._encode(returned))
            out["return"] = {"path": "native-result.json"}
            if call["outcome"] == "return" and not isinstance(returned, dict):
                raise CaptureError("unexpected native return type")
            if call["outcome"] == "return" and not all(key in local for key in
                    ("normal_slo", "support_dict", "confidence_dict", "ji_dict", "sorted_ji", "ranks")):
                raise CaptureError("returned native call is missing score stages")
        return out
