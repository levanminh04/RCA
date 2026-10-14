"""T-032 observational BARO capture; leave native/adapter arithmetic untouched.

Use ``with BaroCapture(new_directory) as capture: result = original_call()``
then ``capture.require_complete()`` and the frozen-record replay check. The
adapter already invokes native BARO and its own diem_lai reconstruction;
both are observed, never called again by this module. Tables and arrays use
the explicit finite/tagged representation in capture_microrank. No labels,
new configuration, tolerance, alternate scaler or intervention is introduced.
"""
from __future__ import annotations

import hashlib
import importlib
import inspect
import os
from pathlib import Path
import platform
import sys
import threading
import time
import traceback

from capture_microrank import CaptureError, MicroRankCapture, _sha256


class BaroCapture(MicroRankCapture):
    """Reuse only serialization helpers; install an independent BARO trace hook."""

    def __enter__(self):
        if self._installed or self._closed or sys.gettrace() is not None:
            raise CaptureError("capture cannot be reused or nested with another trace hook")
        self.np = importlib.import_module("numpy")
        self.pd = importlib.import_module("pandas")
        sklearn = importlib.import_module("sklearn")
        adapter = importlib.import_module("p3.adapters.baro")
        native = importlib.import_module("RCAEval.e2e.baro")
        series = importlib.import_module("RCAEval.io.time_series")
        scaler = importlib.import_module("sklearn.preprocessing._data")
        mapping = importlib.import_module("p3.ban_ghi")
        funcs = {
            "adapter": adapter.chay, "prepare": adapter.chuan_bi,
            "main_preprocess": adapter.tien_xu_ly_main, "rename_latency": adapter.doi_ten_latency,
            "native": native.baro, "adapter_keys": adapter.diem_lai,
            "preprocess": series.preprocess, "drop_constant": series.drop_constant,
            "convert_mem_mb": series.convert_mem_mb,
            "fit": inspect.unwrap(scaler.RobustScaler.fit),
            "transform": inspect.unwrap(scaler.RobustScaler.transform),
            "effective_scale": scaler._handle_zeros_in_scale,
            "entity_mapping": mapping.thuc_the_metric,
        }
        self._targets = {function.__code__: name for name, function in funcs.items()}
        self._array_content = {}
        self._table_content = {}
        self._scores = {"native": [], "adapter_keys": []}
        self._preprocess_counts = {"native": 0, "adapter_keys": 0}
        self._owner_thread = threading.get_ident()
        self.directory.mkdir(parents=True, exist_ok=False)
        self._started = time.perf_counter()
        self._write_json("capture-start.json", {
            "schema": "T-032.baro-observation.v1", "status": "started",
            "python": sys.version, "platform": platform.platform(),
            "packages": {"numpy": self.np.__version__, "pandas": self.pd.__version__, "sklearn": sklearn.__version__},
            "sources": {name: {"path": str(Path(fn.__code__.co_filename).resolve()),
                "sha256": _sha256(fn.__code__.co_filename), "first_line": fn.__code__.co_firstlineno}
                for name, fn in funcs.items()},
            "thread_environment": {key: os.environ.get(key) for key in
                ("PYTHONHASHSEED", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")},
            "scope": "one original adapter call; its native and built-in key reconstruction are both observed",
            "time_axis": "actual adapter marker; Nezha metric rows are ordinal 5N+5A, not simultaneous source samples",
            "finite_encoding": "same tagged JSON / parquet state columns as capture_microrank.v1",
        })
        self._hook = self._trace
        self._installed = True
        sys.settrace(self._hook)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._installed:
            if threading.get_ident() != self._owner_thread or sys.gettrace() is not self._hook:
                self.errors.append({"stage": "exit", "error": "owner thread or trace hook changed"})
            sys.settrace(None)
            self._installed = False
        self._closed = True
        try:
            adapters = [call for call in self._calls if call["function"] == "adapter"]
            natives = [call for call in self._calls if call["function"] == "native"]
            if len(adapters) != 1 or len(natives) != 1 or self._active:
                self.errors.append({"stage": "completeness", "error": "expected one adapter/native and no unfinished frames"})
            status = adapters[0].get("adapter_status") if len(adapters) == 1 else None
            if status in ("OK", "NO_EVIDENCE"):
                count = len(self._scores["native"])
                expected = {"adapter_keys": 1, "preprocess": 4, "fit": 2 * count,
                            "transform": 2 * count, "effective_scale": 2 * count}
                actual = {name: sum(call["function"] == name for call in self._calls) for name in expected}
                if actual != expected or len(self._scores["adapter_keys"]) != count:
                    self.errors.append({"stage": "completeness", "expected": expected, "actual": actual,
                                        "error": "missing feature or preprocessing stage"})
                if status == "OK" and count == 0:
                    self.errors.append({"stage": "completeness", "error": "OK adapter with no observed feature scores"})
            for group, scores in self._scores.items():
                self._write_json("scores-" + group + ".json", scores)
            self.summary = {
                "schema": "T-032.baro-observation.v1",
                "status": "capture_failed" if self.errors else "captured_unverified_replay",
                "adapter_status": status, "calls": self._calls, "errors": self.errors,
                "score_files": {group: "scores-" + group + ".json" for group in self._scores},
                "caller_exception": None if exc_type is None else {"type": exc_type.__name__, "message": str(exc_value)},
                "elapsed_seconds": time.perf_counter() - self._started,
                "observer_callback_seconds": self._callback_seconds,
                "artifacts": list(self._artifacts),
                "replay_check": "OPEN: compare frozen record and verify serialized intermediates before use",
            }
            self._write_json("capture.json", self.summary)
        except BaseException as error:
            self.errors.append({"stage": "finalize", "type": type(error).__name__, "error": str(error)})
        finally:
            self._active.clear()
            self._array_cache.clear()
        return False

    def _context(self, frame):
        while frame is not None:
            name = self._targets.get(frame.f_code)
            if name in ("native", "adapter_keys"):
                return name, frame.f_locals.get("col" if name == "native" else "c")
            frame = frame.f_back
        return "preparation", None

    def _trace(self, frame, event, arg):
        name = self._targets.get(frame.f_code)
        if name is None:
            return None
        # Observe sklearn helpers only when reached by this BARO call.
        group, column = self._context(frame)
        if name in ("fit", "transform", "effective_scale") and group == "preparation":
            return None
        began = time.perf_counter()
        try:
            if event == "call":
                frame.f_trace_lines = name in ("native", "adapter_keys")
                frame.f_trace_opcodes = False
                self._sequence += 1
                call = {"id": self._sequence, "function": name, "group": group,
                        "column": column, "exceptions": [], "entry": {}}
                self._active[id(frame)] = call
                local = frame.f_locals
                if name == "adapter":
                    call["entry"]["input"] = self._save_table("adapter-input.parquet", local["metric_win"])
                    call["entry"]["t"] = self._value(local["t"])
                elif name in ("main_preprocess", "rename_latency", "preprocess", "drop_constant", "convert_mem_mb"):
                    table = local.get("data", local.get("df"))
                    call["entry"]["input_signature"] = self._table_signature(table)
                    if name == "preprocess":
                        self._preprocess_counts[group] += 1
                        call["partition"] = "N" if self._preprocess_counts[group] == 1 else "A"
                        call["entry"]["parameters"] = {key: self._value(local[key]) for key in ("dataset", "dk_select_useful")}
                elif name == "effective_scale":
                    # copy=False mutates this array in sklearn; preserve pre-change values now.
                    call["entry"] = {key: self._value(local[key]) for key in ("scale", "copy", "constant_mask")}
                elif name == "fit":
                    call["entry"]["input_signature"] = self._array_signature(local["X"])
                elif name == "transform":
                    call["entry"]["input_signature"] = self._array_signature(local["X"])
            elif event == "line":
                self._capture_appended_score(frame, name)
            elif event == "exception":
                kind, value, _ = arg
                self._active[id(frame)]["exceptions"].append({"type": kind.__name__, "message": str(value), "line": frame.f_lineno})
            elif event == "return":
                if name in ("native", "adapter_keys"):
                    self._capture_appended_score(frame, name)
                call = self._active.pop(id(frame))
                call["outcome"] = "exception" if arg is None and call["exceptions"] else "return"
                snapshot = self._snapshot(name, frame, arg, call)
                path = "calls/{:04d}-{}.json".format(call["id"], name)
                self._write_json(path, snapshot)
                call["path"] = path
                # Entry table metadata are kept in the call file once, not repeated in summary.
                call.pop("entry", None)
                self._calls.append(call)
        except BaseException as error:
            self.errors.append({"stage": "observer", "function": name, "event": event,
                "type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc()})
        finally:
            self._callback_seconds += time.perf_counter() - began
        return self._hook

    def _value(self, value):
        if isinstance(value, self.np.ndarray):
            return self._encode(value.tolist())
        return self._encode(value)

    def _array_signature(self, value):
        array = self.np.ascontiguousarray(value)
        return {"shape": list(array.shape), "dtype": array.dtype.str,
                "dense_c_order_sha256": hashlib.sha256(array.tobytes(order="C")).hexdigest()}

    def _array(self, name, value, sparse=False):
        # Content cache, never identity cache: RobustScaler mutates some arrays.
        signature = self._array_signature(value)
        key = (tuple(signature["shape"]), signature["dtype"], signature["dense_c_order_sha256"])
        if key in self._array_content:
            return self._array_content[key]
        self._array_cache.clear()
        meta = super()._array(name, value, sparse=sparse)
        self._array_content[key] = meta
        return meta

    def _save_table(self, name, value):
        import json
        signature = self._table_signature(value)
        key = json.dumps(signature, sort_keys=True)
        if key in self._table_content:
            return self._table_content[key]
        meta = self._table(name, value)
        meta["signature"] = signature
        self._table_content[key] = meta
        return meta

    def _capture_appended_score(self, frame, name):
        if name not in self._scores:
            return
        local = frame.f_locals
        sequence = local.get("ranks" if name == "native" else "out")
        if not sequence or not isinstance(sequence[-1], tuple) or len(sequence[-1]) != 2:
            return
        captured = self._scores[name]
        if len(sequence) <= len(captured):
            return
        if len(sequence) != len(captured) + 1:
            raise CaptureError("missed a BARO feature score append")
        column, score = sequence[-1]
        z = local["zscores" if name == "native" else "z"]
        anomalous = local["anomal_df" if name == "native" else "a"]
        # adapter_keys 'a' is the whole anomalous table, unlike native's array 'a'.
        if name == "native":
            anomalous = local["anomal_df"]
        positions = self.np.flatnonzero(z == score)
        if not self.np.isfinite(z).all() or not self.np.isfinite(score):
            raise CaptureError("nonfinite BARO score/vector; keep capture, do not use intermediates")
        parent = frame.f_back
        prepared = parent.f_locals.get("data") if parent is not None else None
        index = anomalous.index.to_numpy()
        max_indices = [index[int(pos)] for pos in positions]
        times = None if prepared is None else [prepared.loc[idx, "time"] for idx in max_indices]
        captured.append({"column": column, "score": self._value(score),
            "zscores": self._array(name + "-z-" + str(len(captured)), z),
            "max_positions_A": positions.tolist(), "max_input_indices": self._value(max_indices),
            "max_adapter_time_markers": self._value(times),
            "max_preprocessed_values": self._value([anomalous.iloc[int(pos)][column] for pos in positions]),
            "source_raw_reference": "adapter-input.parquet via index and latency rename; prepared and preprocess tables retain each transformation",
            "aggregation": "built-in max of signed robust-z; all exact maximizing positions retained"})

    def _snapshot(self, name, frame, returned, call):
        local = frame.f_locals
        out = {"function": name, "group": call["group"], "column": call["column"],
               "entry": call["entry"], "outcome": call["outcome"], "exceptions": call["exceptions"]}
        stem = str(call["id"]) + "-" + name
        if name == "adapter":
            call["adapter_status"] = returned.get("status") if isinstance(returned, dict) else None
            out["return"] = self._value(returned)
        elif name == "native":
            out["return"] = self._value(returned)
            out["scores"] = self._scores["native"]
            out["parameters"] = {key: self._value(local[key]) for key in ("inject_time", "dataset", "anomalies", "kwargs")}
            out["intersects"] = self._value(local.get("intersects"))
            out["tables_after_intersection"] = {key: self._table_signature(local[key]) for key in ("normal_df", "anomal_df") if key in local}
        elif name == "adapter_keys":
            out["return"] = self._value(returned)
            out["scores"] = self._scores["adapter_keys"]
            out["cols"] = self._value(local.get("cols"))
        elif name in ("prepare", "preprocess"):
            if isinstance(returned, self.pd.DataFrame):
                label = "prepared" if name == "prepare" else "preprocess-" + call["group"] + "-" + call["partition"]
                out["table"] = self._save_table(label + ".parquet", returned)
            else:
                out["return"] = self._value(returned)
        elif name in ("main_preprocess", "rename_latency", "drop_constant", "convert_mem_mb"):
            out["return_signature"] = self._table_signature(returned) if isinstance(returned, self.pd.DataFrame) else None
        elif name == "fit":
            instance = local["self"]
            out["scaler"] = {key: self._value(getattr(instance, key)) for key in
                ("with_centering", "with_scaling", "quantile_range", "unit_variance", "copy", "center_", "scale_") if hasattr(instance, key)}
            out["locals"] = {key: self._value(local[key]) for key in ("q_min", "q_max", "quantiles", "adjust") if key in local}
            if returned is not None and "quantiles" not in local:
                raise CaptureError("fit returned without quantile locals")
        elif name == "transform":
            out["return"] = None if returned is None else self._array(stem + "-z", returned)
        elif name == "effective_scale":
            out["return"] = self._value(returned)
            out["constant_mask"] = self._value(local.get("constant_mask"))
            out["meaning"] = "entry.scale is raw IQR; return is sklearn effective denominator, not necessarily IQR"
        elif name == "entity_mapping":
            out["column"] = local["col"]
            out["return"] = self._value(returned)
        return out
