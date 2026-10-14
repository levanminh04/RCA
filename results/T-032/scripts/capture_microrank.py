"""Observe one unchanged MicroRank call for T-032; no replay or intervention.

API (the caller selects/loads inputs and performs the frozen-record check)::

    with MicroRankCapture(new_output_directory) as capture:
        adapter_result = p3.adapters.microrank.chay(spans, t)
    capture.require_complete()
    # Compare adapter_result with the frozen status, item keys/order and
    # entity ranking/ties through the original p3.ban_ghi functions.

Alternatively ``result, capture = capture_call(directory, callable, *args,
**kwargs)`` makes the same single callable invocation and checks capture
completeness. A valid capture can contain an original native exception; this
is evidence of the ERROR path, not an OK diagnosis or a replay match.

This module neither substitutes a method function nor changes include_graph.
It observes Python call/exception/return events using sys.settrace. A trace
already installed by the caller is rejected before the method starts. The
original method return and exception are untouched. Observer failures are
recorded, never injected into the method; require_complete() is mandatory
before evidence is used. Use one worker process and one native call per scope.

Native before/after rows are stored once in Parquet. Graph inputs reference
positions in the native after table, with their exact ordered-row digest.
Large PageRank matrices are stored as exact sparse coordinates, plus dense
byte digests, dtype and shape; zero entries are implicit. Small vectors stay
dense in Parquet. JSON uses explicit tags for NaN/+inf/-inf and missing values.
Object/index cells in Parquet use the same tagged JSON scalar encoding so
None, pandas.NA, string IDs and floating NaN are not silently conflated.
No label, outcome selection, new seed or A-prime calculation is introduced.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import threading
import time
import traceback
import weakref


class CaptureError(RuntimeError):
    """The observational artifact is incomplete and must not be used."""


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class MicroRankCapture:
    """Context manager for a new directory below results/T-032 or rca/T-032.

    ``module`` optionally supplies the exact imported microrank module used
    by the caller. Imports and file serialization use its existing environment;
    no packages are installed. ``summary`` and ``errors`` remain available
    after exit. A method exception still propagates if the caller did not catch
    it (the P3 adapter normally catches native errors itself).
    """

    _GRAPH_COLUMNS = ("traceID", "spanID", "parentSpanID", "operation")

    def __init__(self, output_directory, module=None):
        self.directory = Path(output_directory).expanduser().resolve()
        allowed = [parent for parent in self.directory.parents
                   if parent.name == "T-032" and parent.parent.name in ("results", "rca")]
        if not allowed:
            raise ValueError("capture directory must be below results/T-032 or rca/T-032")
        self.module = module
        self.errors = []
        self.summary = None
        self._calls = []
        self._active = {}
        self._artifacts = []
        self._array_cache = {}
        self._sequence = 0
        self._array_sequence = 0
        self._callback_seconds = 0.0
        self._installed = False
        self._closed = False

    def __enter__(self):
        if self._installed or self._closed:
            raise CaptureError("capture scopes cannot be reused")
        if sys.gettrace() is not None:
            raise CaptureError("another Python trace hook is active; method has not started")
        self.np = importlib.import_module("numpy")
        self.pd = importlib.import_module("pandas")
        self.module = self.module or importlib.import_module("microrank")
        official = self.module.official
        functions = {
            "microrank": self.module.microrank,
            "get_pagerank_graph": self.module.get_pagerank_graph,
            "trace_pagerank": self.module.trace_pagerank,
            "pageRank": official.pageRank,
            "calculate_spectrum_without_delay_list": self.module.calculate_spectrum_without_delay_list,
            "spectrum_cells": self.module.spectrum_cells,
        }
        self._targets = {function.__code__: name for name, function in functions.items()}
        sources = {}
        for name, function in functions.items():
            path = Path(function.__code__.co_filename).resolve()
            sources[name] = {"path": str(path), "sha256": _sha256(path),
                             "first_line": function.__code__.co_firstlineno}
        self.directory.mkdir(parents=True, exist_ok=False)
        self._owner_thread = threading.get_ident()
        self._started = time.perf_counter()
        self._write_json("capture-start.json", {
            "schema": "T-032.microrank-observation.v1", "status": "started",
            "sources": sources, "python": sys.version, "platform": platform.platform(),
            "numpy": self.np.__version__, "pandas": self.pd.__version__,
            "thread_environment": {key: os.environ.get(key) for key in (
                "PYTHONHASHSEED", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")},
            "scope": "one original native call; observation only; no method replacement",
            "finite_encoding": {
                "json": "{__nonfinite__: NaN|+inf|-inf}; finite values remain numbers",
                "missing": "{__missing__: None|pandas.NA|pandas.NaT}",
                "parquet_objects": "tagged JSON scalar in every object/index cell",
                "parquet_float_special": "sidecar state column: 0 finite, 1 NaN, 2 +inf, 3 -inf",
            },
        })
        self._hook = self._trace
        self._installed = True
        sys.settrace(self._hook)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._installed:
            if threading.get_ident() != self._owner_thread:
                self.errors.append({"stage": "exit", "error": "thread changed inside capture scope"})
            if sys.gettrace() is not self._hook:
                self.errors.append({"stage": "exit", "error": "trace hook replaced inside scope"})
            sys.settrace(None)
            self._installed = False
        self._closed = True
        try:
            native_calls = [call for call in self._calls if call["function"] == "microrank"]
            if len(native_calls) != 1:
                self.errors.append({"stage": "completeness", "error": "expected exactly one native call",
                                    "observed": len(native_calls)})
            elif native_calls[0].get("native_status") == "ok":
                expected = {"microrank": 1, "get_pagerank_graph": 2, "trace_pagerank": 2,
                            "pageRank": 2, "calculate_spectrum_without_delay_list": 2,
                            "spectrum_cells": 1}
                observed = {name: sum(call["function"] == name for call in self._calls)
                            for name in expected}
                if observed != expected:
                    self.errors.append({"stage": "completeness", "error": "OK native call has missing/extra observed stages",
                                        "expected": expected, "observed": observed})
                if any(call["outcome"] != "return" for call in self._calls):
                    self.errors.append({"stage": "completeness", "error": "OK native call has an unwound stage"})
            if self._active:
                self.errors.append({"stage": "completeness", "error": "observed frames did not return",
                                    "calls": list(self._active.values())})
            self.summary = {
                "schema": "T-032.microrank-observation.v1",
                "status": "capture_failed" if self.errors else "captured_unverified_replay",
                "native_outcome": native_calls[0]["outcome"] if len(native_calls) == 1 else None,
                "calls": self._calls, "errors": self.errors,
                "caller_exception": None if exc_type is None else {
                    "type": exc_type.__name__, "message": str(exc_value)},
                "elapsed_seconds": time.perf_counter() - self._started,
                "observer_callback_seconds": self._callback_seconds,
                "artifacts": list(self._artifacts),
                "replay_check": "OPEN: caller must compare frozen status, keys, ties and order",
            }
            self._write_json("capture.json", self.summary)
        except BaseException as error:
            # Never replace the method/caller's original exception with an I/O
            # or serialization error. require_complete() catches this on success.
            self.errors.append({"stage": "finalize", "type": type(error).__name__, "error": str(error)})
        finally:
            self._array_cache.clear()
            self._active.clear()
        return False

    def require_complete(self):
        """Fail closed after context exit; does not claim frozen replay equality."""
        if not self._closed or self.summary is None or self.errors:
            raise CaptureError("MicroRank observation incomplete: " + repr(self.errors))
        return self.summary

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
                group = self._group(frame)
                call = {"id": self._sequence, "function": name, "group": group,
                        "exceptions": []}
                self._active[id(frame)] = call
            elif event == "exception":
                call = self._active[id(frame)]
                kind, value, _tb = arg
                call["exceptions"].append({"type": kind.__name__, "message": str(value),
                                           "line": frame.f_lineno})
            elif event == "return":
                call = self._active.pop(id(frame))
                call["outcome"] = "exception" if arg is None and call["exceptions"] else "return"
                self._calls.append(call)
                capture = self._snapshot(name, frame, arg, call)
                path = "calls/{:03d}-{}.json".format(call["id"], name)
                self._write_json(path, capture)
                call["path"] = path
        except BaseException as error:
            # Observer errors must not affect native control flow or arithmetic.
            self.errors.append({"stage": "observer", "function": name, "event": event,
                                "type": type(error).__name__, "error": str(error),
                                "traceback": traceback.format_exc()})
        finally:
            self._callback_seconds += time.perf_counter() - began
        return self._hook

    def _group(self, frame):
        current = frame
        while current is not None:
            if current.f_code in self._targets:
                local = current.f_locals
                if "anomaly" in local and isinstance(local["anomaly"], (bool, self.np.bool_)):
                    return "anomaly" if local["anomaly"] else "normal"
                if local.get("name") in ("normal", "anomaly"):
                    return local["name"]
            current = current.f_back
        return None

    def _snapshot(self, name, frame, returned, call):
        local = frame.f_locals
        stem = "{:03d}-{}".format(call["id"], name)
        out = {"function": name, "group": call["group"], "outcome": call["outcome"],
               "exceptions": call["exceptions"]}
        if name == "microrank":
            if local.get("include_graph", False) is not False:
                self.errors.append({"stage": "configuration", "error": "include_graph was not the native default False"})
            data = local["data"]
            native_columns = [column for column in self.module.COLS if column in data.columns]
            out["input_signature"] = self._table_signature(data[native_columns])
            out["input_signature"]["all_passed_columns"] = self._encode(list(data.columns))
            out["input_signature"]["scope"] = "only native COLS values are hashed; unused columns are listed, not serialized"
            call["native_status"] = returned.get("status") if isinstance(returned, dict) else None
            out["locals"] = {key: self._encode(local[key]) for key in (
                "incident_time_us", "include_graph", "missing", "newops", "op_services",
                "all_traces", "abnormal", "normal", "raw_normal") if key in local}
            out["tables"] = {}
            for key in ("before", "after", "stats"):
                if key in local:
                    out["tables"][key] = self._table("native-" + key + ".parquet", local[key])
            if "before" not in local and "df" in local:
                out["tables"]["partial_working_spans"] = self._table("native-partial-spans.parquet", local["df"])
            self._write_json("native-result.json", self._encode(returned))
            out["return"] = {"path": "native-result.json"}
            if not isinstance(returned, dict) and call["outcome"] != "exception":
                raise CaptureError("unexpected native return type")
            if isinstance(returned, dict) and returned.get("status") == "ok":
                if "after" not in local or "abnormal" not in local["after"].columns:
                    raise CaptureError("OK native call lacks the native after flags")
        elif name == "get_pagerank_graph":
            out["input_rows"] = self._graph_input(frame, local["rows"], stem)
            out["return"] = self._encode(returned)
            out["partial_audit"] = {key: self._encode(local[key]) for key in
                                    ("missing", "explicit_roots", "degree") if key in local}
        elif name == "trace_pagerank":
            # The four graph dictionaries are already serialized by graph().
            out["graph_source_call"] = self._previous_call("get_pagerank_graph", call["group"])
            out["locals"] = {key: self._encode(local[key]) for key in (
                "anomaly", "node_list", "trace_list", "operation_length", "trace_length",
                "num_sum_trace", "kind_sum_trace", "sum", "weight", "trace_num_list") if key in local}
            out["arrays"] = {key: self._array(stem + "-" + key, local[key], sparse=key in ("p_ss", "p_sr", "p_rs"))
                             for key in ("p_ss", "p_sr", "p_rs", "pr", "kind_list", "result") if key in local}
            out["matrix_aliases"] = {"p_srt": "transpose(p_sr), not a separate input"}
            out["return"] = self._encode(returned)
        elif name == "pageRank":
            out["locals"] = {key: self._encode(local[key]) for key in (
                "operation_length", "trace_length", "d", "alpha", "iteration", "i") if key in local}
            names = ("p_ss", "p_sr", "p_rs", "v", "service_ranking_vector", "request_ranking_vector",
                     "updated_service_ranking_vector", "updated_request_ranking_vector",
                     "normalized_service_ranking_vector")
            out["arrays"] = {key: self._array(stem + "-" + key, local[key], sparse=key in ("p_ss", "p_sr", "p_rs"))
                             for key in names if key in local}
            out["return"] = None if returned is None else self._array(stem + "-return", returned)
        else:
            out["locals"] = {key: self._encode(value) for key, value in local.items()
                             if key in ("anomaly_result", "normal_result", "anomaly_list_len", "normal_list_len",
                                        "top_max", "normal_num_list", "anomaly_num_list", "spectrum_method",
                                        "spectrum", "result", "cells", "anomaly_count", "normal_count",
                                        "anomaly_nums", "normal_nums")}
            out["return"] = self._encode(returned)
        return out

    def _previous_call(self, function, group):
        matches = [call for call in self._calls if call["function"] == function and call["group"] == group]
        return matches[-1].get("path") if matches else None

    def _graph_input(self, frame, rows, stem):
        parent = frame.f_back
        if parent is None or self._targets.get(parent.f_code) != "microrank":
            raise CaptureError("graph call did not come from the observed native frame")
        local = parent.f_locals
        after, traces = local["after"], local["traces"]
        positions = self.np.flatnonzero(after["traceID"].astype(str).isin(traces).to_numpy())
        rebuilt = after.iloc[positions][list(self._GRAPH_COLUMNS)].itertuples(index=False, name=None)
        expected_digest, expected_length = self._rows_digest(rows)
        actual_digest, actual_length = self._rows_digest(rebuilt)
        if (actual_digest, actual_length) != (expected_digest, expected_length):
            raise CaptureError("graph input does not exactly match referenced native after rows")
        return {"table": "native-after.parquet", "columns": list(self._GRAPH_COLUMNS),
                "row_positions": self._array(stem + "-after-positions", positions),
                "ordered_rows_sha256": expected_digest, "row_count": expected_length,
                "reference_check": "exact tagged-row digest matched", "indexing": "zero-based physical row positions"}

    def _rows_digest(self, rows):
        digest, count = hashlib.sha256(), 0
        for row in rows:
            encoded = json.dumps(self._encode(tuple(row)), ensure_ascii=False,
                                 separators=(",", ":"), allow_nan=False).encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
            count += 1
        return digest.hexdigest(), count

    def _table_signature(self, table):
        row_hash, length = self._rows_digest(table.itertuples(index=True, name=None))
        return {"rows": length, "columns": self._encode(list(table.columns)),
                "dtypes": [str(dtype) for dtype in table.dtypes],
                "index_names": self._encode(list(table.index.names)),
                "ordered_rows_including_index_sha256": row_hash,
                "raw_input_not_copied": "caller retains source and input provenance"}

    def _table(self, relative, table):
        # Positional storage columns avoid collisions with any source column or
        # index name; metadata maps them back without guessing names or dtypes.
        stored = self.pd.DataFrame(index=self.pd.RangeIndex(len(table)))
        columns = []
        for position in range(table.index.nlevels):
            key = "index_{}".format(position)
            values = table.index.get_level_values(position)
            stored[key] = [self._scalar_json(value) for value in values]
        for position, column in enumerate(table.columns):
            key = "column_{}".format(position)
            values = table.iloc[:, position]
            meta = {"storage": key, "name": self._encode(column), "dtype": str(values.dtype)}
            if self.pd.api.types.is_bool_dtype(values.dtype) and not values.isna().any():
                stored[key] = values.to_numpy()
                meta["encoding"] = "native"
            elif self.pd.api.types.is_integer_dtype(values.dtype) and not values.isna().any():
                stored[key] = values.to_numpy()
                meta["encoding"] = "native"
            elif self.pd.api.types.is_float_dtype(values.dtype) and not self.pd.api.types.is_extension_array_dtype(values.dtype):
                array = values.to_numpy()
                stored[key] = array
                state = self.np.zeros(len(array), dtype=self.np.uint8)
                state[self.np.isnan(array)] = 1
                state[self.np.isposinf(array)] = 2
                state[self.np.isneginf(array)] = 3
                meta["encoding"] = "native_float"
                if state.any():
                    stored[key + "_special"] = state
                    meta["special_state_column"] = key + "_special"
            else:
                stored[key] = [self._scalar_json(value) for value in values]
                meta["encoding"] = "tagged_json_scalar"
            columns.append(meta)
        path = self._new_path(relative)
        stored.to_parquet(path, engine="pyarrow", index=False, compression="zstd")
        self._register(relative)
        return {"path": relative, "rows": len(table), "columns": columns,
                "index_names": self._encode(list(table.index.names)),
                "index_levels": table.index.nlevels, "index_encoding": "tagged_json_scalar",
                "columns_name": self._encode(table.columns.name)}

    def _array(self, name, value, sparse=False):
        array = self.np.asarray(value)
        if array.dtype.hasobject:
            raise CaptureError("object array requires explicit scalar serialization")
        cache = self._array_cache.get(id(array))
        if cache is not None and cache[0]() is array:
            return cache[1]
        self._array_sequence += 1
        relative = "arrays/{:03d}-{}.parquet".format(self._array_sequence, name)
        contiguous = self.np.ascontiguousarray(array)
        meta = {"shape": list(array.shape), "dtype": array.dtype.str,
                "dense_c_order_sha256": hashlib.sha256(memoryview(contiguous).cast("B")).hexdigest()}
        if sparse:
            if array.ndim != 2:
                raise CaptureError("only matrices use sparse serialization")
            r, c = self.np.nonzero(array)
            table = self.pd.DataFrame({"row": r, "column": c, "value": array[r, c]})
            meta["encoding"] = "sparse_coordinates; omitted cells are exactly zero"
        else:
            table = self.pd.DataFrame({"value": contiguous.reshape(-1)})
            meta["encoding"] = "dense_c_order"
        meta["table"] = self._table(relative, table)
        self._array_cache[id(array)] = (weakref.ref(array), meta)
        return meta

    def _scalar_json(self, value):
        return json.dumps(self._encode(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)

    def _encode(self, value):
        if value is None:
            return {"__missing__": "None"}
        if value is self.pd.NA:
            return {"__missing__": "pandas.NA"}
        if value is self.pd.NaT:
            return {"__missing__": "pandas.NaT"}
        if isinstance(value, self.np.generic):
            return self._encode(value.item())
        if isinstance(value, float):
            if not math.isfinite(value):
                return {"__nonfinite__": "NaN" if math.isnan(value) else "+inf" if value > 0 else "-inf"}
            return value
        if isinstance(value, (str, bool, int)):
            return value
        if isinstance(value, dict):
            if all(isinstance(key, str) for key in value):
                return {key: self._encode(item) for key, item in value.items()}
            return {"__mapping_items__": [[self._encode(key), self._encode(item)] for key, item in value.items()]}
        if isinstance(value, (list, tuple)):
            return [self._encode(item) for item in value]
        if isinstance(value, (set, frozenset)):
            items = [self._encode(item) for item in value]
            return {"__set__": sorted(items, key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True))}
        if isinstance(value, Path):
            return str(value)
        raise CaptureError("unsupported value type: " + type(value).__name__)

    def _new_path(self, relative):
        path = (self.directory / relative).resolve()
        if self.directory not in path.parents:
            raise CaptureError("artifact path escapes capture directory")
        if path.exists():
            raise CaptureError("refusing to replace existing artifact: " + relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _register(self, relative):
        path = self.directory / relative
        self._artifacts.append({"path": relative, "bytes": path.stat().st_size, "sha256": _sha256(path)})

    def _write_json(self, relative, value):
        path = self._new_path(relative)
        with path.open("x", encoding="utf-8", newline="\n") as destination:
            json.dump(value, destination, ensure_ascii=False, indent=2, allow_nan=False)
            destination.write("\n")
        self._register(relative)


def capture_call(output_directory, call, *args, **kwargs):
    """Invoke callable once; return its original result and the checked observer.

    This does not select inputs, alter method kwargs, invoke a second method,
    compare P3 records, or claim a native ERROR is a successful diagnosis.
    """
    with MicroRankCapture(output_directory) as capture:
        result = call(*args, **kwargs)
    capture.require_complete()
    return result, capture
