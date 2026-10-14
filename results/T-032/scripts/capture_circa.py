"""Observe unchanged CIRCA OLS/RHT/DA; never perform an extra fit or load.

The caller must verify the actual import closure and both frozen records before
using this capture. ``sys.settrace`` observes only registered code objects. The
native scoring.py profile hook remains installed/restored by native code. Raw
ANM residuals are distinct from scoring.py's existing diagnostic refit. Graph
snapshots read existing storage, never the lazy topological_sort property.
"""
from __future__ import annotations

import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import platform
import sys
import threading
import time
import traceback


SERIALIZER_SHA256 = "b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b"
_serializer_path = Path(__file__).resolve().with_name("capture_microrank.py")
if hashlib.sha256(_serializer_path.read_bytes()).hexdigest() != SERIALIZER_SHA256:
    raise RuntimeError("frozen T-032 serialization helper hash mismatch")
from capture_microrank import CaptureError, MicroRankCapture, _sha256
if Path(sys.modules[MicroRankCapture.__module__].__file__).resolve() != _serializer_path:
    raise RuntimeError("serialization helper import resolved to a different file")


MAX_CAPTURE_BYTES = 32 * 1024 * 1024
DATA_BYTE_LIMIT = MAX_CAPTURE_BYTES - 2 * 1024 * 1024


class CircaCapture(MicroRankCapture):
    """One adapter/native entry, or one focused native fixture entry.

    entry is adapter|score_graph|regressor|da|unsupported. A method exception
    propagates unchanged. Observer errors only make require_complete fail.
    Neither a successful capture nor a fixture certifies a mechanism.
    """

    def __init__(self, output_directory, entry="adapter"):
        super().__init__(output_directory)
        if entry not in ("adapter", "score_graph", "regressor", "da", "unsupported"):
            raise ValueError("unknown CIRCA observation entry")
        self.entry = entry
        self._bytes = 0
        self._array_content = {}
        self._table_content = {}

    def __enter__(self):
        if self._installed or self._closed or sys.gettrace() is not None:
            raise CaptureError("CIRCA capture cannot be reused/nested with a trace hook")
        self.np = importlib.import_module("numpy")
        self.pd = importlib.import_module("pandas")
        functions = {}
        if self.entry == "unsupported":
            adapter = importlib.import_module("p3.adapters.nezha")
            functions["unsupported"] = adapter.chay
        else:
            adapter = importlib.import_module("p3.adapters.circa")
            builder = importlib.import_module("circa_kien_truc.builder")
            scoring = importlib.import_module("circa_kien_truc.scoring")
            rht = importlib.import_module("RCAEval.graph_heads.rht")
            data = importlib.import_module("RCAEval.classes.data")
            graph = importlib.import_module("RCAEval.classes.graph")
            functions.update({
                "adapter": adapter.chay, "prepare": adapter.chuan_bi,
                "adapter_graph": adapter.do_thi, "adapter_score": adapter.cham,
                "service_calls": builder.service_calls, "build_graph": builder.build_graph,
                "mapping": builder.metric_mapping, "score_graph": scoring.score_graph,
                "load_data": data.CaseData.load_data,
                "rht_score": rht.DecomposableScorer.score,
                "split_data": rht.RHTScorer.split_data,
                "score_node": rht.RHTScorer.score_node,
                "regressor": rht.Regressor.score, "anm": rht.ANMRegressor._score,
                "zscore": rht.zscore, "confidence": rht.zscore_conf,
                "da": rht.DAScorer.score,
                "parents": graph.MemoryGraph.parents, "children": graph.MemoryGraph.children,
            })
        self._targets = {function.__code__: name for name, function in functions.items()}
        self._markers = {}
        for name in ("load_data", "da"):
            if name in functions:
                function = functions[name]
                lines = Path(function.__code__.co_filename).read_text(encoding="utf-8").splitlines()
                start = function.__code__.co_firstlineno
                # Exact source is authenticated by the replay caller. These
                # markers identify pre-execution lines, not alternate arithmetic.
                needles = (["if self._prune:"] if name == "load_data" else
                    ["for index, nodes in enumerate(sorted_nodes):", "score = scores[node]",
                     "child_score: Dict[Node, float] = {}", "child_scores[node] = child_score",
                     "if score.score >= self._threshold:"])
                for needle in needles:
                    matches = [i + 1 for i, line in enumerate(lines[start - 1:], start - 1)
                               if line.strip() == needle]
                    # Each selected line occurs once in its authenticated function.
                    matches = [line for line in matches if line < start + 100]
                    if len(matches) != 1:
                        raise CaptureError("missing/ambiguous native observation marker: " + needle)
                    self._markers[(name, matches[0])] = needle
        self.directory.mkdir(parents=True, exist_ok=False)
        self._owner_thread = threading.get_ident()
        self._started = time.perf_counter()
        self._old_trace, self._old_profile = sys.gettrace(), sys.getprofile()
        self._write_json("capture-start.json", {
            "schema": "T-032.circa-observation.v1", "entry": self.entry,
            "sources": {name: {"path": str(Path(fn.__code__.co_filename).resolve()),
                "sha256": _sha256(fn.__code__.co_filename), "first_line": fn.__code__.co_firstlineno}
                for name, fn in functions.items()},
            "python": sys.version, "platform": platform.platform(),
            "thread_environment": {key: os.environ.get(key) for key in
                ("PYTHONHASHSEED", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")},
            "scope": "observe existing calls only; no diagnostic refit/load/predict added",
            "profile_policy": "existing profile preserved; native score_graph installs its own DA profile",
            "graph_policy": "read existing _node/_adj/_nodes/_sorted_nodes; never request lazy topology",
            "diagnostic_refit_policy": "full score_graph return is preserved; its official_* residual labels belong to an existing diagnostic refit, not the native ANM fit",
            "maximum_capture_bytes": MAX_CAPTURE_BYTES,
            "finite_encoding": "tagged JSON specials; numeric arrays exact .npy bytes; tables use pinned T-032 tagged parquet serializer",
        })
        self._hook = self._trace
        self._installed = True
        sys.settrace(self._hook)
        return self

    def _context(self, frame):
        parent = frame
        while parent is not None:
            name = self._targets.get(parent.f_code)
            if name == "score_node":
                return "native_rht", parent.f_locals.get("node")
            if name == "da":
                return "native_da", parent.f_locals.get("node")
            if name == "rht_score":
                return "native_rht_load", None
            if name == "score_graph":
                return "existing_diagnostic_refit", parent.f_locals.get("node")
            parent = parent.f_back
        return "focused_native_fixture", None

    @staticmethod
    def _node(value):
        state = vars(value)
        return {"entity": state["_entity"], "metric": state["_metric"],
                "name": str(state["_entity"]) + "_" + str(state["_metric"])}

    def _value(self, value):
        if isinstance(value, self.np.ndarray):
            return self._encode(value.tolist())
        if hasattr(value, "__dict__"):
            state = vars(value)
            if {"_entity", "_metric"} <= set(state):
                return {"__node__": self._node(value)}
            if {"_score", "_key", "_info"} <= set(state):
                return {"__score__": self._value({"score": state["_score"],
                    "explicit_key": state["_key"], "info": state["_info"]})}
        if isinstance(value, dict):
            if all(isinstance(key, str) for key in value):
                return {key: self._value(item) for key, item in value.items()}
            return {"__mapping_items__": [[self._value(key), self._value(item)] for key, item in value.items()]}
        if isinstance(value, (list, tuple)):
            return [self._value(item) for item in value]
        if isinstance(value, (set, frozenset)):
            return {"__set_iteration__": [self._value(item) for item in value]}
        return self._encode(value)

    def _graph(self, graph):
        state = vars(graph)
        if "_graph" in state:
            return {"stored_graph": self._graph(state["_graph"]),
                "node_set_iteration": self._value(list(state["_nodes"])),
                "cached_topological_groups": self._value(state["_sorted_nodes"])}
        if "_node" not in state or "_adj" not in state:
            raise CaptureError("unknown native graph storage; no property-based fallback")
        return {"nodes_in_storage_order": self._value(list(state["_node"])),
            "edges_in_storage_order": self._value([(a, b) for a, children in state["_adj"].items() for b in children]),
            "parent_storage_order": self._value([(node, list(parents)) for node, parents in state.get("_pred", {}).items()])}

    def _array(self, name, value, sparse=False):
        array = self.np.asarray(value)
        if array.dtype.hasobject:
            raise CaptureError("CIRCA numeric snapshot has object dtype")
        dense = self.np.ascontiguousarray(array)
        digest = hashlib.sha256(dense.tobytes(order="C")).hexdigest()
        key = (array.dtype.str, tuple(array.shape), digest)
        if key not in self._array_content:
            self._array_sequence += 1
            relative = "arrays/{:04d}.npy".format(self._array_sequence)
            if self._bytes + dense.nbytes + 256 > DATA_BYTE_LIMIT:
                raise CaptureError("CIRCA capture byte budget exceeded; no truncation")
            path = self._new_path(relative)
            with path.open("xb") as output:
                self.np.save(output, dense, allow_pickle=False)
            self._register(relative)
            self._array_content[key] = relative
        return {"__array__": self._array_content[key], "shape": list(array.shape), "dtype": array.dtype.str,
            "dense_c_order_sha256": digest, "original_strides": list(array.strides),
            "original_c_contiguous": bool(array.flags.c_contiguous),
            "original_f_contiguous": bool(array.flags.f_contiguous), "original_writeable": bool(array.flags.writeable)}

    def _save_table(self, name, table):
        signature = self._table_signature(table)
        key = json.dumps(signature, sort_keys=True)
        if key not in self._table_content:
            meta = self._table(name, table)
            meta["signature"] = signature
            self._table_content[key] = meta
        return self._table_content[key]

    def _table(self, relative, table):
        """Pinned helper's exact tagged columns, with a bounded output sink.

        Buffering is serialization only. It prevents one parquet write from
        exceeding the remaining task output budget before _register can check.
        No source/native table, missing cell, special float or dtype is changed.
        """
        stored = self.pd.DataFrame(index=self.pd.RangeIndex(len(table)))
        columns = []
        for position in range(table.index.nlevels):
            key = "index_{}".format(position)
            stored[key] = [self._scalar_json(value) for value in table.index.get_level_values(position)]
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
        maximum = DATA_BYTE_LIMIT - self._bytes
        class BoundedSink(io.BytesIO):
            def write(self, value):
                if self.tell() + len(value) > maximum:
                    raise CaptureError("CIRCA parquet exceeds remaining byte budget; no truncation")
                return super().write(value)
        with BoundedSink() as buffer:
            stored.to_parquet(buffer, engine="pyarrow", index=False, compression="zstd")
            data = buffer.getvalue()
        path = self._new_path(relative)
        with path.open("xb") as output:
            output.write(data)
        self._register(relative)
        return {"path": relative, "rows": len(table), "columns": columns,
            "index_names": self._encode(list(table.index.names)), "index_levels": table.index.nlevels,
            "index_encoding": "tagged_json_scalar", "columns_name": self._encode(table.columns.name)}

    def _series(self, series):
        return [{"node": self._value(node), "values": self._array("series", values)} for node, values in series.items()]

    def _case(self, case):
        state = vars(case)
        return {key: self._value(state[key]) for key in
            ("_sli", "_detect_time", "_train_window", "_test_window", "_lookup_window", "_prune")} | {
            "interval_seconds": state["_interval"].total_seconds()}

    def _register(self, relative):
        super()._register(relative)
        self._bytes += (self.directory / relative).stat().st_size
        if self._bytes > MAX_CAPTURE_BYTES:
            raise CaptureError("CIRCA capture byte budget exceeded; partial files retained")

    def _write_json(self, relative, value):
        data = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        limit = MAX_CAPTURE_BYTES if relative == "capture.json" else DATA_BYTE_LIMIT
        if self._bytes + len(data.encode("utf-8")) > limit:
            raise CaptureError("CIRCA capture JSON exceeds remaining byte budget; no truncation")
        path = self._new_path(relative)
        path.write_text(data, encoding="utf-8", newline="\n")
        self._register(relative)

    def _trace(self, frame, event, arg):
        if self.errors:
            # A failed observation is never made eligible by dropping fields.
            # Stop collecting after that explicit failure, leave the original
            # computation running, and retain all already written partial files.
            return None
        name = self._targets.get(frame.f_code)
        if name is None:
            return None
        # These helpers may also be used outside this one native graph call.
        group, node = self._context(frame)
        if name in ("parents", "children", "mapping") and self.entry == "adapter":
            parent = frame
            in_scope = False
            while parent is not None:
                if self._targets.get(parent.f_code) in ("adapter", "score_graph"):
                    in_scope = True
                    break
                parent = parent.f_back
            if not in_scope:
                return None
        began = time.perf_counter()
        try:
            if event == "call":
                frame.f_trace_lines = name in ("load_data", "da")
                frame.f_trace_opcodes = False
                self._sequence += 1
                call = {"id": self._sequence, "function": name, "group": group,
                    "node": self._value(node), "exceptions": [], "entry": self._entry(name, frame), "journal": []}
                self._active[id(frame)] = call
            elif event == "line":
                self._line(name, frame, self._active[id(frame)])
            elif event == "exception":
                kind, value, _ = arg
                self._active[id(frame)]["exceptions"].append({"type": kind.__name__, "message": str(value), "line": frame.f_lineno})
            elif event == "return":
                call = self._active.pop(id(frame))
                call["outcome"] = "exception" if arg is None and call["exceptions"] else "return"
                snapshot = {**call, "exit": self._exit(name, frame, arg, call)}
                relative = "calls/{:04d}-{}.json".format(call["id"], name)
                self._write_json(relative, snapshot)
                summary = {key: value for key, value in call.items() if key not in ("entry", "journal")}
                summary["path"] = relative
                if name in ("adapter", "unsupported"):
                    summary["adapter_statuses"] = [item.get("status") for item in arg] if isinstance(arg, list) else None
                self._calls.append(summary)
        except BaseException as error:
            self.errors.append({"stage": "observer", "function": name, "event": event,
                "type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc()})
        finally:
            self._callback_seconds += time.perf_counter() - began
        return self._hook

    def _entry(self, name, frame):
        local = frame.f_locals
        if name == "adapter":
            return {"metric_win": self._save_table("input-metric.parquet", local["metric_win"]),
                "spans": self._save_table("input-spans.parquet", local["spans"]),
                "t": self._value(local["t"]), "model": local["mo_hinh"]}
        if name == "unsupported":
            if local["method"] != "circa" or local["payload"] is not None or local["trace_guard_s"] != 0:
                raise CaptureError("unsupported path received payload/changed method or guard")
            return {"method": local["method"], "payload": None, "trace_guard_s": local["trace_guard_s"]}
        if name == "score_graph":
            return {"frame": self._save_table("score-frame.parquet", local["frame"]),
                "original_graph_before_prune": self._graph(local["graph"]),
                **{key: self._value(local[key]) for key in ("detect_time", "current", "da_threshold")}}
        if name == "build_graph":
            return {"columns": self._value(local["columns"]), "call_graph": self._graph(local["call_graph"]),
                "circa_source_argument": local["circa_source"], "retain_isolates": local["retain_isolates"]}
        if name == "service_calls":
            return {"traces": self._save_table("graph-spans.parquet", local["traces"]),
                "cutoff_seconds": self._value(local["cutoff_seconds"])}
        if name == "load_data":
            return {"graph": self._graph(local["graph"]), "case": self._case(local["self"]),
                "current": self._value(local["current"])}
        if name in ("rht_score", "da"):
            return {"graph": self._graph(local["graph"]), "case": self._case(local["data"]),
                "current": self._value(local["current"]), "scores": self._value(local["scores"]),
                "threshold": self._value(vars(local["self"]).get("_threshold")),
                "tau_max": self._value(vars(local["self"]).get("_tau_max")),
                "use_confidence": self._value(vars(local["self"]).get("_use_confidence")),
                "aggregator": getattr(vars(local["self"])["_aggregator"], "__name__", None)}
        if name == "score_node":
            return {"node": self._value(local["node"]), "case": self._case(local["data"])}
        if name == "split_data":
            return {"node": self._value(local["node"]), "parents_in_actual_argument_order": self._value(local["parents"]),
                "effective_parent_order": self._value([p for p in local["parents"] if p in local["data"]]),
                "case": self._case(local["case_data"])}
        if name in ("regressor", "anm"):
            return {key: self._array(name + key, local[key]) for key in ("train_x", "test_x", "train_y", "test_y")}
        if name == "zscore":
            return {key: self._array(key, local[key]) for key in ("train_y", "test_y")}
        if name == "adapter_graph":
            return {"columns": self._value(local["columns"]), "t": self._value(local["t"]), "circa_src": local["circa_src"]}
        if name in ("parents", "children", "mapping", "confidence"):
            key = "node" if name in ("parents", "children") else "columns" if name == "mapping" else "score"
            return {key: self._value(local[key])}
        return {}

    def _line(self, name, frame, call):
        marker = self._markers.get((name, frame.f_lineno))
        if marker is None:
            return
        local = frame.f_locals
        if name == "load_data":
            values = local["node_data"]
            call["journal"].append({"step": "loaded_before_native_prune", "node": self._value(local["node"]),
                "values": self._value(None) if values is None else self._array("loaded", values)})
        elif marker == "for index, nodes in enumerate(sorted_nodes):":
            call["journal"].append({"step": "topological_groups_after_native_cache", "groups": self._value([list(g) for g in local["sorted_nodes"]])})
        elif marker == "score = scores[node]":
            call["journal"].append({"step": "index_visit", "node": self._value(local["node"]), "index": local["index"]})
        elif marker == "child_score: Dict[Node, float] = {}":
            call["journal"].append({"step": "descendant_visit", "node": self._value(local["node"])})
        elif marker == "child_scores[node] = child_score":
            call["journal"].append({"step": "child_map_before_assignment", "node": self._value(local["node"]),
                "child_score": self._value(local["child_score"])})
        elif marker == "if score.score >= self._threshold:":
            call["journal"].append({"step": "adjustment_before_mutation", "node": self._value(local["node"]),
                "score": self._value(local["score"]), "child_map": self._value(local["child_scores"][local["node"]])})

    def _exit(self, name, frame, result, call):
        local = frame.f_locals
        special = ("service_calls", "build_graph", "adapter_graph", "prepare",
                   "load_data", "split_data", "zscore", "regressor", "anm", "parents", "children")
        out = {"return": self._value(result)} if name not in special else {}
        if name in ("service_calls", "build_graph", "adapter_graph"):
            if result is not None:
                out = {"graph": self._graph(result[0]), "report": self._value(result[1])}
            if name == "build_graph" and "source" in local:
                out["inserted_path_literal_resolved"] = str(local["source"])
        if name == "prepare" and result is not None:
            out = {"table": self._save_table("prepared.parquet", result)}
        if name == "score_graph":
            out["native_full_return"] = out.pop("return")
            if "mg" in local:
                out["memory_graph_existing_state"] = self._graph(local["mg"])
                out["node_name_bindings"] = self._value(local["byname"])
                out["case"] = self._case(local["case"])
            if "series" in local:
                out["initial_loaded_series"] = self._series(local["series"])
            if "scores" in local:
                out["unadjusted_native_scores"] = self._value(local["scores"])
        if name == "load_data":
            out = {"series": None if result is None else self._series(result),
                **{key: self._value(local[key]) for key in ("start", "length", "current") if key in local}}
        if name == "split_data":
            out = {"train_test": None if result is None else
                {key: self._array(key, value) for key, value in zip(("train_x", "test_x", "train_y", "test_y"), result)}}
        if name == "rht_score" and "series" in local:
            out.update(series=self._series(local["series"]), candidates=self._value(local["candidates"]))
        if name == "score_node":
            for key in ("parents", "z_score", "confidence"):
                if key in local:
                    out[key] = self._value(local[key])
            for key in ("train_x", "test_x", "train_y", "test_y", "z_scores"):
                if key in local:
                    out[key] = self._array(key, local[key])
        if name in ("regressor", "anm", "zscore"):
            out["z_scores"] = None if result is None else self._array("z_scores", result)
        if name == "regressor":
            out["route"] = ("no_effective_parents" if len(local["train_x"]) == 0 else
                "value_error_fallback" if any(e["type"] == "ValueError" for e in call["exceptions"]) else "linear_regression")
        if name == "anm":
            state = vars(vars(local["self"])["_regressor"])
            out["fitted_model_state"] = {key: self._value(state[key]) for key in
                ("coef_", "intercept_", "rank_", "singular_", "n_features_in_") if key in state}
            for key in ("train_err", "test_err"):
                if key in local:
                    out[key] = self._array(key, local[key])
        if name == "zscore" and "scaler" in local:
            state = vars(local["scaler"])
            out["scaler_state"] = {key: self._value(state[key]) for key in
                ("mean_", "var_", "scale_", "n_samples_seen_", "n_features_in_") if key in state}
        if name == "da":
            for key in ("sorted_nodes", "child_scores"):
                if key in local:
                    out[key] = self._value(local[key])
            out["graph_existing_state"] = self._graph(local["graph"])
        if name in ("parents", "children"):
            out = {"returned_set_iteration_order": self._value(list(result))} if result is not None else {"return": self._value(None)}
        return out

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._installed:
            if threading.get_ident() != self._owner_thread or sys.gettrace() is not self._hook:
                self.errors.append({"stage": "exit", "error": "thread or trace hook changed"})
            sys.settrace(self._old_trace)
            self._installed = False
        self._closed = True
        try:
            if sys.getprofile() is not self._old_profile:
                self.errors.append({"stage": "exit", "error": "existing profile was not restored by native code"})
            expected_entry = self.entry
            entries = [call for call in self._calls if call["function"] == expected_entry]
            if len(entries) != 1 or self._active:
                self.errors.append({"stage": "completeness", "error": "one entry and no active frames required", "entry_count": len(entries)})
            statuses = entries[0].get("adapter_statuses") if len(entries) == 1 else None
            counts = {name: sum(call["function"] == name for call in self._calls) for name in set(self._targets.values())}
            if self.entry == "adapter" and statuses and all(s in ("OK", "NO_EVIDENCE") for s in statuses):
                if len(statuses) != 2 or any(counts.get(n) != 1 for n in ("prepare", "adapter_graph", "service_calls", "build_graph", "adapter_score", "score_graph")):
                    self.errors.append({"stage": "completeness", "error": "successful OLS pair lacks critical graph/scoring stage", "counts": counts})
            if self.entry == "unsupported" and (statuses != ["UNSUPPORTED"] or len(self._calls) != 1):
                self.errors.append({"stage": "completeness", "error": "UNSUPPORTED must not call/load CIRCA native"})
            self.summary = {"schema": "T-032.circa-observation.v1", "entry": self.entry,
                "status": "capture_failed" if self.errors else "captured_unverified_replay",
                "adapter_statuses": statuses, "calls": self._calls, "counts": counts, "errors": self.errors,
                "caller_exception": None if exc_type is None else {"type": exc_type.__name__, "message": str(exc_value)},
                "elapsed_seconds": time.perf_counter() - self._started, "observer_callback_seconds": self._callback_seconds,
                "profile_restored": sys.getprofile() is self._old_profile,
                "artifact_bytes": self._bytes, "artifacts": list(self._artifacts),
                "replay_check": "OPEN until source, capture, native/observed and both frozen record comparisons pass"}
            self._write_json("capture.json", self.summary)
        except BaseException as error:
            self.errors.append({"stage": "finalize", "type": type(error).__name__, "error": str(error)})
        finally:
            self._active.clear()
            self._array_cache.clear()
        return False

    def require_complete(self):
        if not self._closed or self.summary is None or self.errors:
            raise CaptureError("CIRCA observation incomplete: " + repr(self.errors))
        return self.summary
