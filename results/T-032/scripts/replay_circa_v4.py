"""T-032 CIRCA OLS/a/h0 v4: exact native/observed and frozen-pair replay.

Run only on the approved EC2, with the original environment and PYTHONPATH.
CLI: fixture NEW_DIR --source-closure FILE --source-closure-sha256 SHA
     one RE2-TT|Nezha-OB OPAQUE_ID NEW_DIR --source-closure FILE ...
     audit-fixture NEW_DIR --old-run CLOSED_FAILED_RUN --transport-inventory FILE
         --transport-inventory-sha256 SHA --source-closure FILE ...

The coordinator supplies an independently anchored, byte-hashed source closure
for the frozen revisions. No T-014 manifest is copied or assumed to exist on
EC2. CIRCA_SRC is not patched. Native child and observed worker see the same job
and startup imports. No tolerance, replacement score, new fit, label input or
intervention is used. Fixtures test observation, not research mechanisms.
Verifier v2 restores pandas logical extension dtypes before exact table checks.
Values, scalar missing states, row/column order and logical dtype stay exact.
The v1 capture did not record pandas string storage backend identity; this
wrapper does not claim backend identity or alter native/source/pair criteria.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback


HELPER_HASHES = {
    "capture_microrank.py": "b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b",
    "replay_microrank.py": "193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562",
    "capture_circa_v2.py": "707c98617e9b61efaa4672a9f54d46d22c8d0dc0d4cd9497d6bee944960eab60",
}
for _name, _expected in HELPER_HASHES.items():
    _path = Path(__file__).resolve().with_name(_name)
    if hashlib.sha256(_path.read_bytes()).hexdigest() != _expected:
        raise RuntimeError("frozen T-032 helper hash mismatch: " + _name)
import replay_microrank as shared
from capture_circa_v2 import CircaCapture, nodeview_source_pin
from replay_microrank import (
    ReplayError, EXACT_FIELDS, EXCLUDED_FIELDS, sha, read, dump, safe_source,
    new_directory, progress, verify, verified_index26, literal_constants,
    exact_differences, compare_records, decode, measured_cost,
    artifact_manifest,
)
for _name in HELPER_HASHES:
    if Path(sys.modules[_name[:-3]].__file__).resolve() != Path(__file__).resolve().with_name(_name):
        raise RuntimeError("helper import resolved to a different file: " + _name)


ANCHOR_M24_SHA256 = "51498845f1e070017ec52c3b6550b84c444882af7c09aa31564d93c58972c2a8"
ANCHOR_M26_SHA256 = "675092feac86d62908fb6a83f1356a2fc1ab128c717c4018f50433710abb7366"
CORE_HASHES = {
    # T014 manifest-files.csv, local authority; never required on EC2.
    "circa_kien_truc": "4d15f238f545d3e6b69a5669c896542e709d1676e123cee27ab8a09ab6b37881",
    "circa_kien_truc.builder": "3ff4d10ad8df685750961e5d884db61ebf9102c3c48fd0980bc785b70b3f4e13",
    "circa_kien_truc.scoring": "f198cee2dbf0d254026955b5dc94659793d37392d0d198a850b581e440bece3f",
    "circa.graph.structural": "0a78529c36487d3531671c5ee3ec70f9f8025a1970b6023c5c6944065a69a4dc",
    "circa.graph.base": "41674e02daad708fa0fcdadd2010d94b887dd51f2164ef620f1e420cf1378d63",
    "circa.model.case": "efdf74e643a5b3cfdc8fa8c0d39967dc353f252e5617b0d0e03c3f275383fcac",
    "circa.model.graph": "aafab30e6a775c56797e7a30227d073062c27ddb05f382b40e19a9921f46e632",
    "circa.model.data_loader": "6e1ea7292406076a164d0327a979c68672edcb7e68b1b6407391b8d3945d0de3",
    "circa.utils": "ac7a2af906a3314aec1c7e6e58fe6cccabef2b2ef7a49e6eef244f07f2e4297c",
    # T024 kiem-code-torai-ec2.json dependency_files / import_evidence.files.
    "RCAEval.classes.data": "52f38e34fe9e8c3afc42e2d605c0c24d211b339ba3cb0329cf950117653edd27",
    "RCAEval.classes.graph": "6e32cca5198fa0aff32b6a4dd7976d97e06ea347ec76fd79f9e576ad50ab6f87",
    "RCAEval.graph_heads.rht": "6d408323ae3f180ea2ed171ed6f43058d202b7655f0d85ec6a4b768980998110",
    "RCAEval.graph_heads.random_walk": "a2487db860e9e8961698a6f09fa8792266d1a87bc0686de373ac401fe8f70912",
    "RCAEval.io.time_series": "37cc5223f99d241f091484851d0d9933ef6a42f4e124e0f2e0a85356eab2b1cd",
}
EXPECTED_PACKAGES = {"numpy": "1.26.4", "pandas": "2.2.3", "sklearn": "1.6.0",
    "scipy": "1.14.1", "networkx": "2.8.8", "pyarrow": "18.1.0"}
SOURCE_PREFIXES = ("p3", "circa_kien_truc", "RCAEval", "circa")


def historical_snapshot(meta):
    path = Path(meta["path"]).expanduser().resolve()
    approved = Path("/home/ubuntu/rca/T-032/sources").resolve()
    if approved not in path.parents or not path.is_file() or path.suffix != ".py":
        raise ReplayError("historical launcher snapshot must be strictly below T032/sources")
    if not meta.get("authority") or not re.fullmatch(r"[0-9a-f]{64}", str(meta.get("sha256", ""))):
        raise ReplayError("historical launcher lacks hash/source-proof authority")
    if sha(path) != meta["sha256"]:
        raise ReplayError("historical launcher byte hash mismatch")
    return path


def closure_path_guard(raw):
    path = Path(raw).expanduser().resolve()
    if any(part.lower() in ("locked", "test", "tests", "t-033", "heldout") for part in path.parts):
        raise ReplayError("closure path outside T032 read scope")
    if "flash-ticket-rca-research" in str(path).lower():
        raise ReplayError("archived source rejected")
    approved = (shared.REPO.resolve() / "src", Path("/home/ubuntu/rca/T-025/src").resolve())
    if not any(root == path or root in path.parents for root in approved):
        raise ReplayError("closure code must be in copied T032 src or approved T025 source root")
    if not path.is_file() or path.suffix != ".py":
        raise ReplayError("closure source is not an existing Python file")
    return path


def load_closure(path, expected_sha256, audit):
    """The injected SHA is the trusted binding, not a hash calculated as trust."""
    path = Path(path).expanduser().resolve()
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256) or sha(path) != expected_sha256:
        raise ReplayError("trusted source-closure byte hash mismatch")
    closure = read(path)
    if closure.get("schema") != "T-032.circa-source-closure.v1":
        raise ReplayError("unsupported source-closure schema")
    revisions = closure.get("revisions", {})
    if not str(revisions.get("RCAEval", "")).startswith("259ea41") or not str(revisions.get("CIRCA", "")).startswith("0215e18"):
        raise ReplayError("closure is not bound to the frozen method revisions")
    files = closure.get("files")
    if not isinstance(files, dict) or not set(CORE_HASHES) <= set(files):
        raise ReplayError("source closure lacks mandatory native modules")
    for name, meta in files.items():
        if not isinstance(meta, dict) or not meta.get("authority") or not re.fullmatch(r"[0-9a-f]{64}", str(meta.get("sha256", ""))):
            raise ReplayError("closure entry lacks expected hash/authority: " + name)
        source = closure_path_guard(meta["path"])
        actual = sha(source)
        row = {"module": name, "path": str(source), "expected": meta["sha256"],
            "actual": actual, "authority": meta["authority"], "pass": actual == meta["sha256"]}
        audit.append(row)
        if not row["pass"] or (name in CORE_HASHES and actual != CORE_HASHES[name]):
            raise ReplayError("frozen closure source hash mismatch: " + name)
    historical = closure.get("historical_launchers", {})
    if not isinstance(historical, dict):
        raise ReplayError("historical_launchers must be a logical-path mapping")
    for logical_path, meta in historical.items():
        safe_source(logical_path)
        snapshot = historical_snapshot(meta)
        audit.append({"logical_path": logical_path, "snapshot": str(snapshot), "sha256": meta["sha256"],
            "authority": meta["authority"], "origin": "reconstructed_exact_bytes", "historical_artifact_found": False,
            "launcher_executed_by_wrapper": False, "pass": True})
    audit.append({"path": str(path), "sha256": expected_sha256, "authority": "caller injected trusted source-closure SHA", "pass": True})
    return closure


def check_imports(closure, audit, p3_hashes=None):
    result = []
    for name, module in sorted(sys.modules.copy().items()):
        if not any(name == prefix or name.startswith(prefix + ".") for prefix in SOURCE_PREFIXES):
            continue
        raw = getattr(module, "__file__", None)
        if raw is None:
            raise ReplayError("unanchored namespace module in source closure: " + name)
        meta = closure["files"].get(name)
        if meta is None:
            raise ReplayError("actual imported module missing from closure: " + name)
        path = Path(raw).resolve()
        if path != Path(meta["path"]).resolve() or sha(path) != meta["sha256"]:
            raise ReplayError("actual import path/hash differs from closure: " + name)
        if p3_hashes is not None and (name == "p3" or name.startswith("p3.")):
            relative = path.relative_to(shared.REPO.resolve()).as_posix()
            if p3_hashes.get(relative) != meta["sha256"]:
                raise ReplayError("actual p3 import not frozen by source config/index: " + name)
        result.append({"module": name, "path": str(path), "sha256": meta["sha256"]})
    audit.append({"actual_imports": result, "pass": True})
    return result


def prepare_imports(closure, audit, unsupported=False, p3_hashes=None):
    for name in ("p3.worker", "p3.runner", "p3.selector"):
        importlib.import_module(name)
    if unsupported:
        for name in ("p3.nezha_worker", "p3.adapters.nezha", "p3.ban_ghi"):
            importlib.import_module(name)
    else:
        # Pre-import exactly the same modules for native and observed workers.
        # StructuralGraph stays the original imported implementation; the default
        # CIRCA_SRC and builder's sys.path insertion remain untouched.
        for name in ("p3.adapters.circa", *CORE_HASHES):
            importlib.import_module(name)
    versions = {name: importlib.import_module(name).__version__ for name in EXPECTED_PACKAGES}
    if versions != EXPECTED_PACKAGES:
        raise ReplayError("numerical package versions differ from frozen CIRCA environment")
    return {"packages": versions, "imports": check_imports(closure, audit, p3_hashes)}


def source_for(dataset, opaque_id, audit, closure):
    if not re.fullmatch(r"dev-[0-9a-f]{10}", opaque_id) or os.environ.get("PYTHONHASHSEED") != "0":
        raise ReplayError("opaque dev ID / launch PYTHONHASHSEED=0 required")
    if dataset == "RE2-TT":
        manifest = read(verify(shared.M24, ANCHOR_M24_SHA256, "T032 pinned source manifest", audit))
        index = read(verify(shared.I24, manifest["source_hashes"][shared.I24], shared.M24 + "#/source_hashes", audit))
        entries = [e for e in index["records"] if e["method"] == "circa" and e["opaque_id"] == opaque_id
            and e["variant"] in ("ols+rht_da", "ols+rht") and e["seed"] is None]
        entries.sort(key=lambda e: 0 if e["variant"] == "ols+rht_da" else 1)
        if len(entries) != 2 or [e["variant"] for e in entries] != ["ols+rht_da", "ols+rht"]:
            raise ReplayError("expected exactly one OLS DA/RHT frozen pair")
        authority = shared.I24 + "#/records"
        if len({(e["source_config"], e["source_config_sha256"]) for e in entries}) != 1:
            raise ReplayError("frozen pair configuration differs")
        config = read(verify(entries[0]["source_config"], entries[0]["source_config_sha256"], authority, audit))
        if config.get("model") != "ols" or config.get("hashseeds") != [0] or config.get("mode") != "a" or config.get("seeds") != [None]:
            raise ReplayError("source configuration outside frozen OLS/a/h0 scope")
        code_hashes = config["src_p3"]["tep"]
        launcher = closure.get("historical_launchers", {}).get(config["script"])
        if launcher is None or launcher.get("sha256") != config["script_sha256"]:
            raise ReplayError("exact historical launcher must be bound to frozen config script_sha256")
        snapshot = historical_snapshot(launcher)
        current = safe_source(config["script"])
        current_sha = sha(current) if current.is_file() else None
        audit.append({"logical_path": config["script"], "copied_current_path": str(current),
            "copied_current_sha256": current_sha, "current_matches_historical_hash": current_sha == config["script_sha256"],
            "snapshot": str(snapshot), "reconstructed_exact_sha256": sha(snapshot),
            "expected_historical_sha256": config["script_sha256"],
            "authority": entries[0]["source_config"] + "#/script_sha256", "source_proof": launcher["authority"],
            "origin": "reconstructed_exact_bytes", "historical_artifact_found": False,
            "launcher_executed_by_wrapper": False, "pass": True})
        verify("results/T-031/scripts/chung.py", config["chung_sha256"], entries[0]["source_config"] + "#/chung_sha256", audit)
        index26 = None
    else:
        verify(shared.M26, ANCHOR_M26_SHA256, "T032 pinned T026 source manifest", audit)
        index26 = verified_index26(audit)
        entries = [e for e in index26["unique_records"] if e["worker_method"] == "circa"
            and e["opaque_id"] == opaque_id and e["source_view"] == "main"]
        if len(entries) != 1:
            raise ReplayError("expected one frozen Nezha UNSUPPORTED record")
        authority = shared.I26 + "#/unique_records"
        code_hashes = {p: h for p, h in index26["source_hashes"].items() if p.startswith("src/p3/") and p.endswith(".py")}
    frozen = [read(verify(e["path"], e["sha256"], authority, audit)) for e in entries]
    for record in frozen:
        expected_hashseed = 0 if dataset == "RE2-TT" else None
        if any((record["opaque_id"] != opaque_id, record["method"] != "circa", record["mode"] != "a",
                record["seed"] is not None, record["hashseed"] != expected_hashseed, record["window"] is None)):
            raise ReplayError("frozen record metadata/window outside declared scope")
        if dataset == "RE2-TT" and record["status"] not in ("OK", "ERROR", "NO_EVIDENCE"):
            raise ReplayError("frozen status needs another authorized replay path")
        if dataset == "Nezha-OB" and record["status"] != "UNSUPPORTED":
            raise ReplayError("Nezha CIRCA must remain UNSUPPORTED without native method")
    for relative, expected in sorted(code_hashes.items()):
        verify(relative, expected, "frozen configuration / T026 source index", audit)
    if len(frozen) == 2 and any(frozen[0][key] != frozen[1][key] for key in ("input_sha256", "window", "config_id", "why_ids")):
        raise ReplayError("frozen pair input/window/config differs")
    return entries, frozen, index26, code_hashes


def table_columns(directory, meta):
    """Restore recorded logical dtype without treating it as a NumPy dtype.

    StringDtype/Int64/boolean/Float64 belong to pandas. Tagged scalar decoding
    preserves the recorded missing/nonfinite values; the caller still checks
    the complete ordered table signature against the original native snapshot.
    String storage backend identity was not recorded by capture v1 and remains
    unverified. This helper reads capture artifacts and never touches a method.
    """
    import numpy as np
    import pandas as pd
    path = (directory / meta["path"]).resolve()
    if directory.resolve() not in path.parents:
        raise ReplayError("capture table reference escaped its directory")
    stored = pd.read_parquet(path, use_threads=False)
    if len(stored) != meta["rows"]:
        raise ReplayError("capture table row count mismatch")
    result = {}
    for column in meta["columns"]:
        values = stored[column["storage"]]
        dtype = pd.api.types.pandas_dtype(column["dtype"])
        extension = pd.api.types.is_extension_array_dtype(dtype)
        if column["encoding"] == "tagged_json_scalar":
            decoded = [decode(json.loads(value)) for value in values]
            array = pd.array(decoded, dtype=dtype) if extension else np.asarray(decoded, dtype=dtype)
        else:
            array = pd.array(values.tolist(), dtype=dtype) if extension else values.to_numpy(dtype=dtype, copy=True)
        if "special_state_column" in column:
            state = stored[column["special_state_column"]].to_numpy()
            if not np.isin(state, [0, 1, 2, 3]).all():
                raise ReplayError("unknown nonfinite state")
            array[state == 1], array[state == 2], array[state == 3] = np.nan, np.inf, -np.inf
        result[decode(column["name"])] = array
    return result


def final_manifest(directory, excluded):
    """Seal all run files after the terminal log/source writes, including logs."""
    directory = Path(directory).resolve()
    excluded = set(excluded)
    result = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ReplayError("run artifact symlink cannot be sealed")
        if path.is_file():
            relative = path.relative_to(directory).as_posix()
            if relative not in excluded:
                result.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha(path)})
    return result


def verify_final_manifest(directory, check_name="check.json"):
    directory = Path(directory).resolve()
    check = read(directory / check_name)
    if check.get("manifest_excludes") != [check_name]:
        raise ReplayError("final check does not declare its precise self exclusion")
    expected = check.get("artifact_manifest")
    if not isinstance(expected, list) or exact_differences(expected, final_manifest(directory, [check_name])):
        raise ReplayError("closed final run artifact set/byte hash mismatch")
    return {"pass": True, "check": check_name, "files_checked": len(expected),
        "progress_in_manifest": any(row["path"] == "progress.jsonl" for row in expected),
        "source_checks_in_manifest": any(row["path"] == "source-checks.json" for row in expected)}


def finalize_check(directory, payload, terminal, terminal_fields=None, check_name="check.json"):
    """This is the last wrapper write; the current check cannot hash itself."""
    if (directory / check_name).exists():
        raise ReplayError("refusing to overwrite a closed check")
    if not (directory / "source-checks.json").is_file():
        raise ReplayError("source checks must be written before the final manifest")
    progress(directory, terminal, **(terminal_fields or {}))
    value = {**payload, "artifact_manifest": final_manifest(directory, [check_name]),
        "manifest_excludes": [check_name], "terminal_event_before_manifest": terminal}
    dump(directory / check_name, value)
    return verify_final_manifest(directory, check_name)


def da_journal_check(call):
    """Join every DA line event in native order; never discard repeat headers."""
    def require(condition, message):
        if not condition:
            raise ReplayError(message)
    def same(left, right, message):
        require(not exact_differences(left, right), message)
    journals = call["journal"]
    if call["outcome"] == "exception":
        # The explicitly declared pre-loop fixture is scores=None on a nonempty
        # graph: the native list comprehension raises before sorted_nodes exists.
        # Other incomplete DA calls remain failures, never completed traversals.
        require(call["entry"]["scores"] == {"__missing__": "None"}
            and not journals and "sorted_nodes" not in call["exit"]
            and call["exit"]["return"] == {"__missing__": "None"}
            and bool(call["exceptions"])
            and all(item["type"] == "TypeError" and item["line"] in (254, 255, 256)
                for item in call["exceptions"]),
            "DA exception is not the declared pre-loop scores=None path; incomplete journal")
        return {"pass": True, "completed": False, "native_outcome": "pre_loop_exception",
            "groups": None, "header_count": 0, "mechanism_evidence": False}
    require(call["outcome"] == "return" and not call["exceptions"],
        "completed DA must return without an original exception")
    headers = [item for item in journals if item["step"] == "topological_groups_after_native_cache"]
    require(bool(headers), "actual DA groups not observed")
    groups = headers[0]["groups"]
    require(isinstance(groups, list) and all(isinstance(group, list) for group in groups),
        "DA group snapshot schema is not ordered groups")
    require(len(headers) == len(groups) + 1, "DA header count must be exact G+1 for a completed loop")
    for item in headers:
        same(groups, item["groups"], "DA group snapshot changed while assigning native indexes")
    stored_groups = call["exit"]["sorted_nodes"]
    require(isinstance(stored_groups, list)
        and all(isinstance(group, dict) and set(group) == {"__set_iteration__"} for group in stored_groups),
        "native exit DA groups do not preserve set iteration")
    same(groups, [group["__set_iteration__"] for group in stored_groups],
        "DA header and native exit groups differ in node/group order")
    scores = call["entry"]["scores"]
    if scores == {}:
        score_items = []
    else:
        require(isinstance(scores, dict) and set(scores) == {"__mapping_items__"},
            "DA entry score mapping lacks native item order")
        score_items = scores["__mapping_items__"]
        require(all(isinstance(item, list) and len(item) == 2 for item in score_items),
            "DA entry score item schema differs")
    score_nodes = [item[0] for item in score_items]
    grouped_nodes = [node for group in groups for node in group]
    require(len(grouped_nodes) == len(score_nodes)
        and len({json.dumps(node, sort_keys=True) for node in grouped_nodes}) == len(grouped_nodes),
        "DA groups duplicate or omit scored nodes")
    require({json.dumps(node, sort_keys=True) for node in grouped_nodes}
        == {json.dumps(node, sort_keys=True) for node in score_nodes},
        "DA group and input score candidate sets differ")
    position = 0
    def take(step, node=None, index=None):
        nonlocal position
        require(position < len(journals), "DA chronology is missing a native step: " + step)
        item = journals[position]
        position += 1
        require(item["step"] == step, "DA chronology has an extra/reordered step: " + step)
        if node is not None:
            same(node, item["node"], "DA chronology node differs: " + step)
        if index is not None:
            same(index, item["index"], "DA native index differs from its group position")
        return item
    for index, group in enumerate(groups):
        same(groups, take("topological_groups_after_native_cache")["groups"],
            "DA chronology header changed")
        for node in group:
            take("index_visit", node, index)
    same(groups, take("topological_groups_after_native_cache")["groups"],
        "DA terminal loop header changed")
    for group in reversed(groups):
        for node in group:
            take("descendant_visit", node)
            take("child_map_before_assignment", node)
    for node in score_nodes:
        take("adjustment_before_mutation", node)
    require(position == len(journals), "DA chronology has trailing/duplicate native steps")
    return {"pass": True, "completed": True, "native_outcome": "return", "groups": groups,
        "header_count": len(headers), "group_count": len(groups), "chronology_steps": position,
        "entry_score_order": score_nodes, "empty_scored_candidates": not score_nodes}


def capture_checks(directory, summary):
    """Byte checks and joins of actual native stages; no refit or alternate RHT."""
    import numpy as np
    import pandas as pd
    if summary["status"] != "captured_unverified_replay" or summary["errors"] or not summary["profile_restored"]:
        raise ReplayError("CIRCA observation incomplete/profile changed")
    for artifact in summary["artifacts"]:
        path = (directory / artifact["path"]).resolve()
        if directory.resolve() not in path.parents or not path.is_file() or sha(path) != artifact["sha256"] or path.stat().st_size != artifact["bytes"]:
            raise ReplayError("capture artifact escaped/missing/hash mismatch")
    calls = [read(directory / call["path"]) for call in summary["calls"]]
    array_meta, table_meta = [], {}
    def collect(value):
        if isinstance(value, dict):
            if "__array__" in value:
                array_meta.append(value)
            if {"path", "signature", "columns", "index_levels", "rows"} <= set(value):
                table_meta[value["path"]] = value
            for item in value.values():
                collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)
    for call in calls:
        collect(call)
    def array(meta):
        path = (directory / meta["__array__"]).resolve()
        if directory.resolve() not in path.parents:
            raise ReplayError("array path escaped capture")
        result = np.load(path, allow_pickle=False)
        if list(result.shape) != meta["shape"] or result.dtype.str != meta["dtype"] or hashlib.sha256(result.tobytes(order="C")).hexdigest() != meta["dense_c_order_sha256"]:
            raise ReplayError("array reconstruction differs from native snapshot")
        return result
    for meta in array_meta:
        array(meta)
    serializer = CircaCapture.__new__(CircaCapture)
    serializer.np, serializer.pd = np, pd
    for meta in table_meta.values():
        values = table_columns(directory, meta)
        table = pd.read_parquet(directory / meta["path"])
        if meta["index_levels"] != 1:
            raise ReplayError("CIRCA table index schema needs explicit reconstruction")
        columns = [decode(m["name"]) for m in meta["columns"]]
        if len(set(columns)) != len(columns):
            raise ReplayError("duplicate CIRCA columns need explicit reconstruction")
        reconstructed = pd.DataFrame({column: pd.Series(values[column], dtype=m["dtype"])
            for column, m in zip(columns, meta["columns"])})
        reconstructed.index = pd.Index([decode(json.loads(v)) for v in table["index_0"]], name=decode(meta["index_names"])[0])
        reconstructed.columns.name = decode(meta["columns_name"])
        if serializer._table_signature(reconstructed) != meta["signature"]:
            raise ReplayError("CIRCA table values/dtypes/index/column order changed in serialization")
    by_function = {}
    for call in calls:
        by_function.setdefault(call["function"], []).append(call)
    def require(condition, message):
        if not condition:
            raise ReplayError(message)
    def name(node):
        return node["__node__"]["name"]
    def names(nodes):
        return [name(node) for node in nodes]
    def mapping(value):
        if value == {}:
            return {}
        return {name(node): item for node, item in value["__mapping_items__"]}
    def same(left, right, message):
        require(not exact_differences(left, right), message)
    def same_array(left, right, message):
        require(left["shape"] == right["shape"] and left["dtype"] == right["dtype"] and
            left["dense_c_order_sha256"] == right["dense_c_order_sha256"], message)
    critical = {"pass": True, "arrays_checked": len(array_meta), "tables_reconstructed": len(table_meta),
        "files_checked": len(summary["artifacts"]), "diagnostic_refit_distinguished": True}
    if summary["entry"] == "unsupported":
        require(len(calls) == 1 and by_function["unsupported"][0]["exit"]["return"][0]["status"] == "UNSUPPORTED", "unsupported path invoked native stages")
        return {**critical, "native_called": False, "mechanism_evidence": False}
    score_graph_calls = by_function.get("score_graph", [])
    if score_graph_calls:
        require(len(score_graph_calls) == 1, "expected one score_graph call")
        graph_call = score_graph_calls[0]
        full = decode(graph_call["exit"]["native_full_return"])
        if graph_call["outcome"] == "exception":
            require(bool(graph_call["exceptions"]), "exception path lacks original exception")
            return {**critical, "native_graph_outcome": "exception", "mechanism_evidence": "partial ERROR path only"}
        require(isinstance(full, dict) and {"meta", "graph", "nodes", "da", "ranks"} <= set(full), "native full scoring return schema missing")
        original_graph = graph_call["entry"]["original_graph_before_prune"]
        same(sorted(original_graph["nodes_in_storage_order"]), full["graph"]["nodes"], "original graph nodes lost before prune")
        same(sorted(original_graph["edges_in_storage_order"]), full["graph"]["edges"], "original graph edges lost before prune")
        if full["meta"].get("empty"):
            require(not full["nodes"] and not by_function.get("score_node"), "empty graph has scoring stages")
            return {**critical, "scored_nodes": 0, "original_graph_preserved": True}
        require(len(by_function.get("load_data", [])) == 2 and len(by_function.get("rht_score", [])) == 1
            and len(by_function.get("da", [])) == 1, "load/RHT/DA stages missing or extra")
        loads = sorted(by_function["load_data"], key=lambda c: c["id"])
        left = {name(v["node"]): v["values"] for v in loads[0]["exit"]["series"]}
        right = {name(v["node"]): v["values"] for v in loads[1]["exit"]["series"]}
        require(set(left) == set(right) == set(full["nodes"]), "actual loaded/pruned/scored nodes differ")
        for node in left:
            same_array(left[node], right[node], "two native load_data calls differ: " + node)
        for load in loads:
            visits = load["journal"]
            require(len(visits) == len(original_graph["nodes_in_storage_order"]) and len({name(v["node"]) for v in visits}) == len(visits), "missing actual pre-prune loaded node")
            pre_prune = {name(v["node"]): v["values"] for v in visits}
            for node, values in left.items():
                loaded = array(pre_prune[node])
                selected = array(values)
                require(np.array_equal(loaded[:load["exit"]["length"]], selected, equal_nan=True), "native loaded/pruned values differ")
        same(sorted(set(original_graph["nodes_in_storage_order"]) - set(left)), full["meta"]["dropped_constant_or_missing"], "native prune report differs from actual loaded data")
        require(len(by_function.get("score_node", [])) == len(left), "missing/extra native score_node")
        raw_scores = mapping(graph_call["exit"]["unadjusted_native_scores"])
        for node, score in raw_scores.items():
            same(score["__score__"]["score"], full["nodes"][node]["rht_score"], "native RHT differs from existing diagnostic report")
        native_node_calls = {name(c["entry"]["node"]): c for c in by_function["score_node"]}
        require(set(native_node_calls) == set(left), "duplicate/missing native node frame")
        scorer_entry = by_function["rht_score"][0]["entry"]
        require(scorer_entry["tau_max"] == 0 and scorer_entry["use_confidence"] is False and scorer_entry["aggregator"] == "max", "native RHT configuration changed")
        for node, call in native_node_calls.items():
            matches = lambda function: [c for c in by_function.get(function, []) if c["group"] == "native_rht" and name(c["node"]) == node]
            for function in ("split_data", "regressor", "zscore", "confidence"):
                require(len(matches(function)) == 1, "missing native stage " + function + ": " + node)
            split, reg, z = matches("split_data")[0], matches("regressor")[0], matches("zscore")[0]
            same(call["exit"]["parents"], split["entry"]["parents_in_actual_argument_order"], "RHT parent argument order changed")
            for key in ("train_x", "test_x", "train_y", "test_y"):
                same_array(call["exit"][key], split["exit"]["train_test"][key], "native split/node input differs")
                same_array(reg["entry"][key], split["exit"]["train_test"][key], "regressor input differs from split")
            loaded_y = array(right[node])
            case_state = split["entry"]["case"]
            require(np.array_equal(array(reg["entry"]["train_y"]), loaded_y[:case_state["_train_window"]], equal_nan=True)
                and np.array_equal(array(reg["entry"]["test_y"]), loaded_y[-case_state["_test_window"]:], equal_nan=True), "native y split does not match actual loaded series")
            parent_order = names(split["entry"]["effective_parent_order"])
            train_x, test_x = array(reg["entry"]["train_x"]), array(reg["entry"]["test_x"])
            if parent_order:
                require(train_x.shape[1] == test_x.shape[1] == len(parent_order), "effective parent count differs from actual matrix")
                for index, parent in enumerate(parent_order):
                    values = array(right[parent])
                    require(np.array_equal(train_x[:, index], values[:case_state["_train_window"]], equal_nan=True)
                        and np.array_equal(test_x[:, index], values[-case_state["_test_window"]:], equal_nan=True), "native parent matrix column order differs from loaded parent order")
            same_array(call["exit"]["z_scores"], reg["exit"]["z_scores"], "native regressor/node z differs")
            same_array(reg["exit"]["z_scores"], z["exit"]["z_scores"], "native scaler/regressor z differs")
            require({"mean_", "var_", "scale_", "n_samples_seen_", "n_features_in_"} <= set(z["exit"]["scaler_state"]), "native scaler state incomplete")
            route = reg["exit"]["route"]
            anm = matches("anm")
            if route == "linear_regression":
                require(len(anm) == 1 and anm[0]["outcome"] == "return", "native ANM fit missing")
                require({"coef_", "intercept_", "rank_", "singular_", "n_features_in_"} <= set(anm[0]["exit"]["fitted_model_state"]), "native OLS model state incomplete")
                for residual, target in (("train_err", "train_y"), ("test_err", "test_y")):
                    same_array(anm[0]["exit"][residual], z["entry"][target], "native residual/scaler input differs")
            elif route in ("no_effective_parents", "value_error_fallback"):
                for target in ("train_y", "test_y"):
                    same_array(reg["entry"][target], z["entry"][target], "fallback did not use native raw y")
                require((not anm) if route == "no_effective_parents" else len(anm) == 1 and anm[0]["outcome"] == "exception", "fallback native ANM exception/absence not observed")
            else:
                raise ReplayError("unknown native regression route")
            score = call["exit"]["return"]["__score__"]
            same(score["score"], full["nodes"][node]["rht_score"], "node score differs from full native return")
            same(score["info"]["Confidence"], full["nodes"][node]["confidence"], "native confidence differs from diagnostic report")
            same(call["exit"]["confidence"], matches("confidence")[0]["exit"]["return"], "native confidence function return missing")
            require(float(np.max(np.abs(array(call["exit"]["z_scores"])))).hex() == float(decode(score["score"])).hex(), "native z aggregation differs")
        critical.update(scored_nodes=len(left), original_graph_preserved=True, native_prune_observed=True,
            native_regression_chain_joined=True, both_loaded_series_exact=True)
    da_calls = by_function.get("da", [])
    if da_calls:
        require(len(da_calls) == 1, "expected exactly one DA call")
        call = da_calls[0]
        journals = call["journal"]
        journal_check = da_journal_check(call)
        if not journal_check["completed"]:
            require(summary["entry"] == "da" and not score_graph_calls,
                "pre-loop DA exception cannot stand in for a successful adapter/score graph")
            return {**critical, "native_da_outcome": journal_check["native_outcome"],
                "completed_da_journal": False, "da_journal": journal_check, "mechanism_evidence": False}
        groups = journal_check["groups"]
        for step, expected in (("index_visit", [n for g in groups for n in g]),
                ("descendant_visit", [n for g in reversed(groups) for n in g])):
            same([j["node"] for j in journals if j["step"] == step], expected, "actual DA traversal differs from native groups")
        maps = {name(j["node"]): j["child_score"] for j in journals if j["step"] == "child_map_before_assignment"}
        same(maps, mapping(call["exit"]["child_scores"]), "DA propagation map before score mutation missing")
        final_scores = mapping(call["exit"]["return"])
        before = [j for j in journals if j["step"] == "adjustment_before_mutation"]
        require(len(before) == len(final_scores) and len(maps) == len(final_scores), "DA mutation journal missing scored nodes")
        for item in before:
            node = name(item["node"])
            same(item["child_map"], maps[node], "DA child map changed before adjustment")
            score = final_scores[node]["__score__"]
            native_group_index = next(index for index, group in enumerate(groups)
                if any(name(member) == node for member in group))
            same(score["info"]["index"], native_group_index,
                "DA final score index differs from the recorded native group/index visit")
            require(isinstance(score["explicit_key"], list) and len(score["explicit_key"]) == 3, "DA key incomplete")
            same(score["explicit_key"], [score["score"], -score["info"]["index"], score["info"].get("z-score", 0)], "native DA key chain differs")
        if score_graph_calls:
            same([names(g) for g in groups], full["graph"]["da_iteration_order"], "trace DA order differs from native profile order")
            for node, score in final_scores.items():
                state = score["__score__"]
                same(state["score"], full["da"][node]["score"], "DA final score differs from native full return")
                same(state["explicit_key"], full["da"][node]["key"], "DA final key differs from native full return")
        critical.update(da_traversal_observed=True, da_propagation_before_mutation=True,
            da_native_keys_joined=True, completed_da_journal=True, da_journal=journal_check)
    if summary["entry"] == "adapter" and summary["adapter_statuses"] and all(s in ("OK", "NO_EVIDENCE") for s in summary["adapter_statuses"]):
        require(len(score_graph_calls) == 1 and len(by_function.get("build_graph", [])) == 1, "successful adapter lacks graph/native full return")
        adapter = by_function["adapter"][0]["exit"]["return"]
        require([v["variant"] for v in adapter] == ["ols+rht_da", "ols+rht"], "adapter pair order changed")
        same(adapter[0]["ranking_native"], [r[0] for r in full["ranks_da"]], "adapter DA rank differs from full native return")
        same(adapter[1]["ranking_native"], [r[0] for r in full["ranks"]], "adapter RHT rank differs from full native return")
        build = by_function["build_graph"][0]["exit"]
        require({"mapping", "unknown", "original_missing_nodes", "isolated", "retain_isolates", "assumptions", "source_revision"} <= set(build["report"]), "complete original builder report missing")
        critical.update(adapter_pair_joined=True, full_builder_report_preserved=True)
    return critical


def make_job(dataset, opaque_id, frozen, entries, index26, audit):
    from p3 import selector
    if dataset == "RE2-TT":
        path = safe_source("results/T-022/allowlist-dev.json")
        allow = selector.nap_allowlist(path)
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
        if wanted != frozen[0]["input_sha256"]:
            raise ReplayError("allowlist input hashes differ from frozen pair")
        files = selector.chon_ca(allow, opaque_id, shared.RE2_RAW_REPO, kiem_hash=True)
        job = {"kind": "ranker", "method": "circa", "t": frozen[0]["window"]["t"], "model": "ols",
            "files": {name: {"path": value, "sha256": wanted[name]} for name, value in files.items()}}
        constants = None
    else:
        from p3 import nezha
        relative = "results/T-026/allowlist-dev.json"
        path = verify(relative, index26["source_hashes"][relative], shared.I26 + "#/source_hashes", audit)
        allow = nezha.nap_allowlist(path)
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items()}
        if wanted != frozen[0]["input_sha256"] or entries[0]["trace_guard_s"] != 0:
            raise ReplayError("Nezha main input hashes/guard differ")
        script = "results/T-026/scripts/run_pilot.py" if entries[0]["reused_pilot"] else "results/T-026/scripts/run.py"
        constants = literal_constants(verify(script, index26["source_hashes"][script], shared.I26 + "#/source_hashes", audit))
        job = {"allowlist_path": str(path), "opaque_id": opaque_id, "repo_root": str(shared.REPO),
            "view": "main", "method": "circa", "trace_guard_s": 0}
    return job, constants, {"allowlist_path": str(path), "allowlist_sha256": sha(path), "selected_input_hashes_equal_frozen": True}


def reconstruct(directory, dataset, frozen, entries, constants, cost):
    from p3 import ban_ghi, runner
    result = read(directory / "ket-qua.json")
    if result.get("hashseed") != "0":
        raise ReplayError("worker returned another hashseed")
    if dataset == "RE2-TT":
        base = {"run_id": directory.name, "opaque_id": frozen[0]["opaque_id"], "mode": "a", "seed": None,
            "hashseed": 0, "detector": None, "detector_columns": None, "config_id": frozen[0]["config_id"]}
        records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "circa", "a", model="ols")
        if len(records) != 2:
            raise ReplayError("original record reconstruction did not return both OLS variants")
    else:
        from p3.adapters.nezha import VERSIONS, VARIANTS
        if len(result["ket_qua_nhieu"]) != 1:
            raise ReplayError("unsupported Nezha worker returned another record count")
        record = ban_ghi.tao("circa", VERSIONS["circa"], VARIANTS["circa"], "a", result["ket_qua_nhieu"][0],
            result["window"], constants["CONFIG"], constants["WHY"], seed=None, hashseed=None,
            run_id=directory.name, opaque_id=frozen[0]["opaque_id"])
        record["cost"] = {**cost, "buoc_s": result.get("buoc_s", {})}
        record["input_sha256"] = result["input_sha256"]
        if entries[0]["reused_pilot"]:
            record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
        else:
            record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
        ban_ghi.kiem(record)
        dump(directory / "ban-ghi-0.json", record)
    return [read(directory / ("ban-ghi-" + str(i) + ".json")) for i in range(len(frozen))]


def native_child(args):
    audit = []
    directory = Path(args.directory).resolve()
    if not directory.is_dir() or not any(parent.name == "T-032" and parent.parent.name in ("rca", "results") for parent in directory.parents):
        raise ReplayError("native child output directory outside approved T032 runs")
    job_path = Path(args.job).resolve()
    if directory.parent not in job_path.parents:
        raise ReplayError("native child job must belong to the same parent run")
    closure = load_closure(args.source_closure, args.source_closure_sha256, audit)
    prepare_imports(closure, audit, unsupported=args.dataset == "Nezha-OB")
    from p3 import worker
    if args.dataset == "Nezha-OB":
        from p3 import nezha_worker
        invoke = nezha_worker.main
    else:
        invoke = worker.main
    started = time.perf_counter()
    invoke(args.job, str(directory / "ket-qua.json"))
    cost = measured_cost(started, 0)
    cost["env"] = "T-032-native-child-unobserved"
    dump(directory / "cost.json", cost)
    check_imports(closure, audit)
    dump(directory / "native-check.json", {"status": "PASS", "source_verified": True,
        "profile_unchanged": sys.getprofile() is None, "trace_unchanged": sys.gettrace() is None,
        "checks": audit, "worker_sha256": sha(directory / "ket-qua.json")})
    return 0


def one(directory, dataset, opaque_id, closure_path, closure_sha256):
    audit = []
    progress(directory, "SOURCE_CHECK_START", method="circa", dataset=dataset, opaque_id=opaque_id)
    try:
        closure = load_closure(closure_path, closure_sha256, audit)
        entries, frozen, index26, p3_hashes = source_for(dataset, opaque_id, audit, closure)
        actual = prepare_imports(closure, audit, unsupported=dataset == "Nezha-OB", p3_hashes=p3_hashes)
        job, constants, input_source = make_job(dataset, opaque_id, frozen, entries, index26, audit)
        dump(directory / "source.json", {"dataset": dataset, "opaque_id": opaque_id, "entries": entries,
            "frozen_statuses": [r["status"] for r in frozen], "source_run_ids": [r["run_id"] for r in frozen],
            "closure_path": str(Path(closure_path).resolve()), "closure_sha256": closure_sha256,
            "actual_imports_before": actual, "input": input_source,
            "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS,
            "CIRCA_SRC_policy": "unchanged native literal; verify actual imported closure; no path patch",
            "intermediate_policy": "original graph and actual native fit retained separately from existing diagnostic refit"})
        dump(directory / "job.json", job)
        from p3 import worker
        invoke = worker.main
        if dataset == "Nezha-OB":
            from p3 import nezha_worker
            invoke = nezha_worker.main
        progress(directory, "OBSERVED_WORKER_START")
        started = time.perf_counter()
        with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout, (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                with CircaCapture(directory / "capture", entry="unsupported" if dataset == "Nezha-OB" else "adapter") as capture:
                    invoke(str(directory / "job.json"), str(directory / "ket-qua.json"))
        summary = capture.require_complete()
        cost = measured_cost(started, 0)
        dump(directory / "cost.json", cost)
        observed = reconstruct(directory, dataset, frozen, entries, constants, cost)
        capture_check = capture_checks(directory / "capture", summary)
        imports_after = check_imports(closure, audit, p3_hashes)
        native_dir = directory / "native"
        native_dir.mkdir()
        progress(directory, "NATIVE_WORKER_START")
        command = [sys.executable, "-B", "-X", "utf8", str(Path(__file__).resolve()), "native", dataset,
            str(directory / "job.json"), str(native_dir), "--source-closure", str(Path(closure_path).resolve()),
            "--source-closure-sha256", closure_sha256, "--repo-root", str(shared.REPO)]
        dump(native_dir / "command.json", {"argv": command})
        with (native_dir / "stdout.txt").open("x", encoding="utf-8") as stdout, (native_dir / "stderr.txt").open("x", encoding="utf-8") as stderr:
            child = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=3600, check=False)
        if child.returncode != 0:
            raise ReplayError("native child failed; preserve stdout/stderr; no eligible intermediates")
        native_check = read(native_dir / "native-check.json")
        if (native_check.get("status") != "PASS" or native_check.get("source_verified") is not True
                or native_check.get("profile_unchanged") is not True or native_check.get("trace_unchanged") is not True
                or native_check.get("worker_sha256") != sha(native_dir / "ket-qua.json")):
            raise ReplayError("native child source/result verification failed")
        native = reconstruct(native_dir, dataset, frozen, entries, constants, read(native_dir / "cost.json"))
        differences = []
        comparisons = []
        for i, (reference, actual_record, native_record) in enumerate(zip(frozen, observed, native)):
            native_diff = compare_records(native_record, actual_record)
            frozen_diff = compare_records(reference, actual_record)
            comparisons.append({"variant": reference["variant"], "frozen_path": entries[i]["path"],
                "frozen_sha256": entries[i]["sha256"], "frozen_status": reference["status"],
                "observed_status": actual_record["status"], "native_status": native_record["status"],
                "native_observed_exact": not native_diff, "frozen_observed_exact": not frozen_diff,
                "native_differences": native_diff, "frozen_differences": frozen_diff})
            differences.extend(native_diff + frozen_diff)
        # Recheck every closure byte and every actual import after the method.
        load_closure(closure_path, closure_sha256, audit)
        check_imports(closure, audit, p3_hashes)
        passed = not differences and capture_check["pass"] is True
        dump(directory / "source-checks.json", {"checks": audit})
        finalize_check(directory, {"status": "PASS" if passed else "FAIL", "method": "circa",
            "dataset": dataset, "opaque_id": opaque_id, "source_verified": True,
            "source_closure_sha256": closure_sha256, "compare": comparisons,
            "native_observed_exact": all(c["native_observed_exact"] for c in comparisons),
            "frozen_observed_exact": all(c["frozen_observed_exact"] for c in comparisons),
            "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS, "differences": differences,
            "capture_status": summary["status"], "capture_check": capture_check, "actual_imports_after": imports_after,
            "intermediates_eligible": passed and dataset == "RE2-TT",
            "unsupported_status_preserved": passed and dataset == "Nezha-OB",
            "interpretation": "exact source/capture/replay checks only; no causal claim; OLS numeric drift is FAIL; Nezha native is never called"},
            "FINISHED", {"status": "PASS" if passed else "FAIL"})
        return 0 if passed else 1
    finally:
        if not (directory / "source-checks.json").exists():
            dump(directory / "source-checks.json", {"checks": audit})


def fixture_inputs(kind):
    import networkx as nx
    import numpy as np
    import pandas as pd
    t = 1000
    ts = np.arange(t - 130, t + 16)
    x = np.arange(len(ts), dtype=float)
    a = 1. + (x % 11) + (x % 3) / 10.
    b = 2. + (x % 7) + (x % 5) / 7.
    frame = pd.DataFrame({"time": ts, "caller_cpu": a, "root_cpu": b})
    frame.loc[frame.time >= t, "root_cpu"] += 4.
    graph = nx.DiGraph()
    graph.add_nodes_from(["caller_cpu", "root_cpu"])
    if kind != "no_effective_parents":
        graph.add_edge("caller_cpu", "root_cpu")
    if kind == "prune_and_isolate":
        frame["constant_cpu"] = 2.
        frame["isolate_mem"] = b * 1e6
        graph.add_nodes_from(["constant_cpu", "isolate_mem", "missing_cpu"])
        graph.add_edges_from([("constant_cpu", "root_cpu"), ("missing_cpu", "root_cpu")])
    if kind == "empty_graph":
        graph = nx.DiGraph()
    if kind == "all_pruned_no_evidence":
        frame["caller_cpu"] = 1.
        frame["root_cpu"] = 2.
    return frame, graph, t, int(ts[-1])


def serializer_table_fixtures(directory):
    """Round-trip actual capture table format, including extension/native paths."""
    import numpy as np
    import pandas as pd
    run = directory / "serializer_tables"
    run.mkdir()
    serializer = CircaCapture(run / "capture")
    serializer.np, serializer.pd = np, pd
    serializer.directory.mkdir()
    checks = []
    cases = (
        ("string", "string", ["plain", "", "tiếng Việt"]),
        ("string_NA", "string", ["x", pd.NA, None]),
        ("Int64", "Int64", [1, 0, -2]),
        ("Int64_NA", "Int64", [1, pd.NA, None]),
        ("boolean", "boolean", [True, False, True]),
        ("boolean_NA", "boolean", [True, pd.NA, None]),
        ("Float64", "Float64", [1.0, -0.0, 2.5]),
        ("Float64_NA", "Float64", [1.0, pd.NA, None]),
        ("native_float_special", "float64", [np.nan, np.inf, -np.inf, -0.0, 1.25]),
        ("object_missing_special", "object", [None, pd.NA, np.nan, np.inf, -np.inf, -0.0, "", "tiếng Việt"]),
    )
    for name, dtype, values in cases:
        progress(directory, "FIXTURE_START", name="serializer_" + name)
        frame = pd.DataFrame({"value": pd.Series(values, dtype=dtype)})
        frame.index = pd.Index(list(range(100 + len(frame), 100, -1)), name="position")
        frame.columns.name = "channel"
        before = frame.copy(deep=True)
        original = serializer._table_signature(frame)
        meta = serializer._save_table(name + ".parquet", frame)
        stored = pd.read_parquet(serializer.directory / meta["path"], use_threads=False)
        columns = [decode(m["name"]) for m in meta["columns"]]
        restored_values = table_columns(serializer.directory, meta)
        restored = pd.DataFrame({column: pd.Series(restored_values[column], dtype=m["dtype"])
            for column, m in zip(columns, meta["columns"])})
        restored.index = pd.Index([decode(json.loads(v)) for v in stored["index_0"]], name=decode(meta["index_names"])[0])
        restored.columns.name = decode(meta["columns_name"])
        actual = serializer._table_signature(restored)
        differences = exact_differences(original, actual)
        pd.testing.assert_frame_equal(frame, before, check_exact=True)
        pd.testing.assert_frame_equal(frame, restored, check_exact=True)
        # Reject changes through the same full signature used by capture_checks.
        reordered = serializer._table_signature(restored.iloc[::-1])
        order_rejected = bool(exact_differences(original, reordered))
        changed = restored.copy(deep=True)
        changed.index = pd.Index([int(v) + 1 for v in changed.index], name=changed.index.name)
        index_rejected = bool(exact_differences(original, serializer._table_signature(changed)))
        logical_dtype_rejected = None
        if dtype != "object":
            logical_dtype_rejected = bool(exact_differences(original,
                serializer._table_signature(restored.astype("object"))))
        passed = not differences and order_rejected and index_rejected and logical_dtype_rejected is not False
        if not passed:
            raise ReplayError("CIRCA serializer fixture failed: " + name)
        item = {"name": "serializer_" + name, "entry": "serializer_only", "passed": passed,
            "differences": differences, "recorded_logical_dtype": meta["columns"][0]["dtype"],
            "recorded_encoding": meta["columns"][0]["encoding"], "order_mutation_rejected": order_rejected,
            "index_mutation_rejected": index_rejected, "logical_dtype_mutation_rejected": logical_dtype_rejected,
            "capture_table": meta, "meaning": "serialization interoperability only; no method or mechanism evidence",
            "string_storage_backend_identity": "not recorded by capture v1; not claimed"}
        dump(run / (name + "-check.json"), item)
        checks.append(item)
    dump(run / "check.json", {"status": "PASS", "fixtures": checks,
        "methods_executed": False, "artifact_manifest": artifact_manifest(run), "manifest_excludes": ["check.json"]})
    return checks



def nodeview_fixture(directory):
    """Snapshot only the inspected NodeView storage without mutation/sorting."""
    import copy
    import networkx as nx
    import numpy as np
    import pandas as pd
    from networkx.classes.reportviews import NodeView
    from RCAEval.classes.graph import Node
    from capture_microrank import CaptureError
    run = directory / "serializer_nodeview"
    run.mkdir()
    progress(directory, "FIXTURE_START", name="serializer_nodeview")
    source = nodeview_source_pin()
    serializer = CircaCapture.__new__(CircaCapture)
    serializer.np, serializer.pd = np, pd
    cases = []
    for label, node_order in (
            ("empty", []),
            ("string_storage_order", ["root_mem", "caller_cpu", "root_cpu"]),
            ("native_node_storage_order", [Node("root", "mem"), Node("caller", "cpu"), Node("root", "cpu")])):
        graph = nx.DiGraph()
        graph.add_nodes_from((node, {"position": index, "nested": {"kept": [index, "value"]}})
            for index, node in enumerate(node_order))
        if len(node_order) > 1:
            graph.add_edges_from([(node_order[0], node_order[-1]), (node_order[1], node_order[0])])
        view = graph.nodes
        if type(view) is not NodeView or object.__getattribute__(view, "_nodes") is not graph._node:
            raise ReplayError("fixture does not use the inspected live NodeView storage")
        before_graph = serializer._graph(graph)
        before_nodes = copy.deepcopy(graph._node)
        before_edges = copy.deepcopy(graph._succ)
        before_parents = copy.deepcopy(graph._pred)
        before_keys = tuple(vars(graph))
        before_storage = object.__getattribute__(view, "_nodes")
        native_order = [serializer._value(node) for node in view]
        expected = [serializer._value(node) for node in node_order]
        actual = serializer._value(view)
        differences = exact_differences(expected, actual) + exact_differences(native_order, actual)
        if (differences or before_graph != serializer._graph(graph)
                or before_nodes != graph._node or before_edges != graph._succ or before_parents != graph._pred
                or before_keys != tuple(vars(graph)) or object.__getattribute__(view, "_nodes") is not before_storage):
            raise ReplayError("NodeView snapshot changed storage, order, node values or graph state: " + label)
        # Demonstrate sensitivity to order corruption using the same exact
        # comparison, rather than silently normalizing/sorting node lists.
        order_mutation_rejected = None if len(node_order) < 2 else bool(exact_differences(expected, actual[::-1]))
        if order_mutation_rejected is False:
            raise ReplayError("NodeView fixture is insensitive to storage order")
        cases.append({"name": label, "passed": True, "snapshot": actual,
            "native_view_iteration": native_order, "storage_order_exact": True,
            "graph_state_unchanged": True, "storage_identity_unchanged": True,
            "order_mutation_rejected": order_mutation_rejected, "differences": differences})
    # Unknown iterators and a different NetworkX view remain unsupported. Their
    # rejection must not consume a generator or broaden the approved serializer.
    graph = nx.DiGraph()
    graph.add_nodes_from(["root_cpu", "caller_cpu"])
    unknown = (value for value in ["first", "second"])
    rejected = []
    for label, value in (("generator", unknown), ("NodeDataView", graph.nodes(data=True))):
        try:
            serializer._value(value)
        except CaptureError as error:
            rejected.append({"type": label, "rejected": True, "error": str(error)})
        else:
            raise ReplayError("NodeView-only serializer broadened support to " + label)
    if next(unknown) != "first":
        raise ReplayError("unsupported generator was consumed while serializing")
    item = {"name": "serializer_nodeview", "entry": "serializer_only", "passed": True,
        "source_pin": source, "cases": cases, "unsupported_types": rejected,
        "unsupported_generator_not_consumed": True, "graph_state_unchanged": True,
        "meaning": "NodeView storage/order/nonmutation fixture only; no mechanism evidence"}
    dump(run / "check.json", item)
    return item


def adapter_table_fixture(directory):
    """Exercise both native OLS adapter outputs with real extension table paths."""
    import numpy as np
    import pandas as pd
    from p3.adapters.circa import chay
    run = directory / "adapter_extension_tables"
    run.mkdir()
    progress(directory, "FIXTURE_START", name="adapter_extension_tables")
    frame, _graph, t, _current = fixture_inputs("scalar_ols")
    spans = pd.DataFrame({
        "traceID": pd.array(["trace-a", "trace-a", "trace-b", "trace-b"], dtype="string"),
        "spanID": pd.array(["span-1", "span-2", "span-3", "span-4"], dtype="string"),
        "parentSpanID": pd.array([pd.NA, "span-1", None, "span-3"], dtype="string"),
        "serviceName": pd.array(["caller", "root", "caller", "root"], dtype="string"),
        "methodName": pd.array(["GET", "", "GET", "tiếng Việt"], dtype="string"),
        "operationName": pd.array(["operation-a", "", "operation-b", "tiếng Việt"], dtype="string"),
        "startTime": pd.array([(t - 60) * 1000000, (t - 60) * 1000000 + 1,
            (t - 50) * 1000000, (t - 50) * 1000000 + 1], dtype="Int64"),
        "duration": pd.array([1000, 100, 1000, 100], dtype="Int64"),
        "unused_integer": pd.array([1, pd.NA, -2, None], dtype="Int64"),
        "unused_boolean": pd.array([True, False, pd.NA, None], dtype="boolean"),
        "unused_float": pd.array([1.5, pd.NA, np.inf, -0.0], dtype="Float64"),
        "unused_object": pd.Series([None, pd.NA, np.nan, "kept"], dtype="object"),
    })
    frame_before, spans_before = frame.copy(deep=True), spans.copy(deep=True)
    def outcome():
        try:
            return chay(frame, spans, t, "ols"), None
        except Exception as error:
            return None, {"type": type(error).__name__, "message": str(error)}
    def pure(value):
        serializer = CircaCapture.__new__(CircaCapture)
        serializer.np, serializer.pd = np, pd
        return serializer._value(value)
    def profile(frame, event, arg):
        return None
    old_profile = sys.getprofile()
    sys.setprofile(profile)
    try:
        original, original_exception = outcome()
        pd.testing.assert_frame_equal(frame, frame_before, check_exact=True)
        pd.testing.assert_frame_equal(spans, spans_before, check_exact=True)
        with CircaCapture(run / "capture", entry="adapter") as capture:
            observed, observed_exception = outcome()
        summary = capture.require_complete()
        check = capture_checks(run / "capture", summary)
        differences = exact_differences(pure(original), pure(observed)) + exact_differences(original_exception, observed_exception)
        if original_exception is not None or observed_exception is not None:
            raise ReplayError("adapter extension table fixture unexpectedly raised")
        if len(original) != 2 or [r["variant"] for r in original] != ["ols+rht_da", "ols+rht"] or [r["status"] for r in original] != ["OK", "OK"]:
            raise ReplayError("adapter table fixture did not exercise both successful native OLS outputs")
        if sys.getprofile() is not profile or sys.gettrace() is not None:
            raise ReplayError("adapter table fixture trace/profile restore failed")
        pd.testing.assert_frame_equal(frame, frame_before, check_exact=True)
        pd.testing.assert_frame_equal(spans, spans_before, check_exact=True)
        adapter_calls = [read(run / "capture" / c["path"]) for c in summary["calls"] if c["function"] == "adapter"]
        if len(adapter_calls) != 1:
            raise ReplayError("adapter table fixture lacks one actual entry")
        captured_types = {decode(m["name"]): m["dtype"] for m in adapter_calls[0]["entry"]["spans"]["columns"]}
        expected_types = {str(column): str(dtype) for column, dtype in spans_before.dtypes.items()}
        if captured_types != expected_types or not check.get("adapter_pair_joined") or check["tables_reconstructed"] < 3:
            raise ReplayError("adapter table fixture did not reconstruct native input/prepared/graph table paths")
        item = {"name": "adapter_extension_tables", "entry": "adapter", "passed": not differences,
            "differences": differences, "original_exception": original_exception, "observed_exception": observed_exception,
            "adapter_variants": [r["variant"] for r in observed], "native_observed_exact_both_outputs": not differences,
            "captured_input_logical_dtypes": captured_types, "inputs_unchanged": True,
            "capture": check, "profile_restored": True,
            "meaning": "observation and serializer fixture only; no mechanism evidence",
            "string_storage_backend_identity": "not recorded by capture v1; not claimed"}
        dump(run / "check.json", item)
        if differences:
            raise ReplayError("adapter extension table native/observed outputs differ")
        return item
    finally:
        sys.setprofile(old_profile)


def audit_stored_fixture(directory, old_run, transport_inventory, transport_sha256,
        closure_path, closure_sha256):
    """Read authenticated closed FAILED artifacts; no method or old file write."""
    old_run = Path(old_run).expanduser().resolve()
    task_root = Path("/home/ubuntu/rca/T-032").resolve()
    if old_run != task_root / "runs" / "circa-nodeview-fixture-001":
        raise ReplayError("stored audit must use the approved closed CIRCA NodeView fixture")
    inventory_path = Path(transport_inventory).expanduser().resolve()
    if task_root not in inventory_path.parents or sha(inventory_path) != transport_sha256:
        raise ReplayError("stored audit transport inventory path/hash mismatch")
    inventory = read(inventory_path)
    if inventory.get("eligibility") is not False or not isinstance(inventory.get("files"), list):
        raise ReplayError("stored audit lacks an explicitly ineligible closed transport inventory")
    prefixes = ("runs/circa-nodeview-fixture-001/", "runs/circa-nodeview-fixture-001-monitor/")
    rows = inventory["files"]
    if len({row["path"] for row in rows}) != len(rows) or not rows:
        raise ReplayError("stored audit transport has duplicate/missing files")
    def verify_closed_transport():
        for row in rows:
            relative = row["path"]
            if not isinstance(relative, str) or not relative.startswith(prefixes):
                raise ReplayError("stored audit transport file outside the closed fixture/monitor")
            path = (task_root / relative).resolve()
            if task_root not in path.parents or path.is_symlink() or not path.is_file():
                raise ReplayError("closed audit artifact path escaped/missing/symlink")
            if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
                raise ReplayError("closed audit artifact current hash mismatch: " + relative)
        actual_paths = set()
        for prefix in prefixes:
            base = task_root / prefix.rstrip("/")
            for path in base.rglob("*"):
                if path.is_symlink():
                    raise ReplayError("closed transport contains a symlink")
                if path.is_file():
                    actual_paths.add(path.relative_to(task_root).as_posix())
        if actual_paths != {row["path"] for row in rows}:
            raise ReplayError("closed transport inventory is not the complete current artifact set")
    verify_closed_transport()
    progress(directory, "CLOSED_FAILED_TRANSPORT_VERIFIED", files=len(rows), eligible=False)
    original = read(old_run / "check.json")
    if original.get("status") != "FAIL" or original.get("intermediates_eligible") is not False:
        raise ReplayError("old fixture was not the declared ineligible FAILED run")
    if original.get("source_closure_sha256") != closure_sha256:
        raise ReplayError("old fixture source closure binding differs")
    # Preserve the exact old manifest failure. Authenticate all ordinary old
    # artifacts and the pinned prefix plus terminal append of progress.jsonl.
    mismatches = []
    for row in original["artifact_manifest"]:
        path = (old_run / row["path"]).resolve()
        if old_run not in path.parents or not path.is_file():
            raise ReplayError("original failed manifest path escaped or disappeared")
        if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            mismatches.append(row)
    if len(mismatches) != 1 or mismatches[0]["path"] != "progress.jsonl":
        raise ReplayError("closed failed manifest mismatch is not the declared terminal progress append")
    row = mismatches[0]
    data = (old_run / "progress.jsonl").read_bytes()
    if hashlib.sha256(data[:row["bytes"]]).hexdigest() != row["sha256"]:
        raise ReplayError("old failed progress prefix differs from the original manifest")
    suffix = data[row["bytes"]:].decode("utf-8")
    lines = suffix.splitlines()
    if len(lines) != 1:
        raise ReplayError("old failed progress has more than the declared terminal append")
    terminal = json.loads(lines[0])
    if terminal.get("stage") != "FAILED" or terminal.get("error") != original.get("error"):
        raise ReplayError("old failed progress suffix does not preserve the original failure")
    audit = []
    closure = load_closure(closure_path, closure_sha256, audit)
    imports = prepare_imports(closure, audit)
    capture_dir = old_run / "adapter_extension_tables" / "capture"
    captured_sources = read(capture_dir / "capture-start.json")["sources"]
    expected_by_path = {str(Path(meta["path"]).resolve()): meta["sha256"]
        for meta in closure["files"].values()}
    for name, meta in captured_sources.items():
        path = Path(meta["path"]).resolve()
        expected = expected_by_path.get(str(path))
        if expected != meta["sha256"] or sha(path) != expected:
            raise ReplayError("old captured native source differs from the pinned closure: " + name)
    summary = read(capture_dir / "capture.json")
    result = capture_checks(capture_dir, summary)
    if not result.get("pass") or not result.get("completed_da_journal") or not result.get("adapter_pair_joined"):
        raise ReplayError("posthoc stored adapter capture did not pass every declared stage/journal join")
    load_closure(closure_path, closure_sha256, audit)
    check_imports(closure, audit)
    verify_closed_transport()
    dump(directory / "source-checks.json", {"checks": audit})
    finalize_check(directory, {"status": "PASS_STORED_CAPTURE_AUDIT", "method": "circa",
        "source_verified": True, "source_closure_sha256": closure_sha256,
        "transport_inventory_path": str(inventory_path), "transport_inventory_sha256": transport_sha256,
        "closed_transport_files_verified_before_after": len(rows), "old_run": str(old_run),
        "actual_imports": imports, "capture_check": result,
        "original_full_manifest_pass": False, "original_failed_progress_prefix_verified": True,
        "original_failure_preserved": original["error"], "methods_executed": False,
        "old_files_written": False, "intermediates_eligible": False,
        "native_observed_original_comparison_recovered": False,
        "meaning": "posthoc integrity/stage/journal audit only; no new native call and no eligibility for the failed old fixture"},
        "AUDIT_FINISHED", {"status": "PASS_STORED_CAPTURE_AUDIT"})
    return 0


def focused_da_fixtures(directory):
    """Declared empty/SCC/pre-loop paths, original versus observed exactly."""
    import copy
    from datetime import timedelta
    import networkx as nx
    import numpy as np
    import pandas as pd
    from RCAEval.classes.data import CaseData, MemoryDataLoader
    from RCAEval.classes.graph import Node, MemoryGraph
    from RCAEval.graph_heads.rht import DAScorer
    from RCAEval.graph_heads.random_walk import Score
    checks = []
    for kind in ("da_empty_groups", "da_scc_with_tail", "da_preloop_exception"):
        run = directory / kind
        run.mkdir()
        progress(directory, "FIXTURE_START", name=kind)
        nodes = [Node("a", "cpu"), Node("b", "cpu"), Node("c", "cpu")]
        graph = nx.DiGraph()
        if kind != "da_empty_groups":
            graph.add_nodes_from(nodes)
            graph.add_edges_from([(nodes[0], nodes[1]), (nodes[1], nodes[0]), (nodes[1], nodes[2])])
        base_scores = ({node: Score(value, info={"z-score": value, "Confidence": 0.5})
            for node, value in zip(nodes, (4., 2., 5.))} if kind == "da_scc_with_tail" else
            None if kind == "da_preloop_exception" else {})
        old_profile = sys.getprofile()
        def profile(frame, event, arg):
            return None
        def invoke():
            candidate_graph = graph.copy()
            before_graph = (list(candidate_graph.nodes), list(candidate_graph.edges), copy.deepcopy(vars(candidate_graph)))
            scores = copy.deepcopy(base_scores)
            memory = MemoryGraph(candidate_graph)
            case = CaseData(MemoryDataLoader({}), nodes[0], 1000, interval=timedelta(seconds=1))
            try:
                value = DAScorer(threshold=3).score(memory, case, 1001, scores)
                if value is not scores:
                    raise ReplayError("declared DA return identity changed")
                error = None
            except Exception as failure:
                value = None
                error = {"type": type(failure).__name__, "message": str(failure)}
            if (before_graph[0:2] != (list(candidate_graph.nodes), list(candidate_graph.edges))
                    or before_graph[2] != vars(candidate_graph)):
                raise ReplayError("declared focused DA fixture mutated its original graph")
            return value, error
        def pure(value):
            serializer = CircaCapture.__new__(CircaCapture)
            serializer.np, serializer.pd = np, pd
            return serializer._value(value)
        sys.setprofile(profile)
        try:
            original, original_error = invoke()
            with CircaCapture(run / "capture", entry="da") as capture:
                observed, observed_error = invoke()
            summary = capture.require_complete()
            check = capture_checks(run / "capture", summary)
            differences = exact_differences(pure(original), pure(observed)) + exact_differences(original_error, observed_error)
            if differences or sys.getprofile() is not profile or sys.gettrace() is not None:
                raise ReplayError("focused DA fixture changed result/exception/hook: " + kind)
            journal = check["da_journal"]
            if kind == "da_empty_groups":
                if original_error is not None or journal["group_count"] != 0 or journal["header_count"] != 1:
                    raise ReplayError("focused DA empty fixture did not exercise exact G=0/header=1")
            elif kind == "da_scc_with_tail":
                if original_error is not None or journal["group_count"] < 2 or not any(len(group) == 2 for group in journal["groups"]):
                    raise ReplayError("focused DA cycle fixture did not exercise SCC plus tail groups")
            elif (original_error is None or original_error["type"] != "TypeError"
                    or journal["completed"] is not False or journal["header_count"] != 0):
                raise ReplayError("focused DA exception fixture was mistaken for completed traversal")
            item = {"name": kind, "entry": "da", "passed": True, "differences": differences,
                "original_exception": original_error, "observed_exception": observed_error,
                "capture": check, "profile_restored": True, "graph_state_unchanged": True,
                "meaning": "declared observer/journal fixture only; no research mechanism evidence"}
            dump(run / "check.json", item)
            checks.append(item)
        finally:
            sys.setprofile(old_profile)
    return checks


def terminal_manifest_fixture(directory):
    """Both terminal statuses are sealed with their final source/log bytes."""
    run = directory / "terminal_manifest"
    run.mkdir()
    progress(directory, "FIXTURE_START", name="terminal_manifest")
    branches = []
    for label in ("PASS", "FAIL"):
        branch = run / label.lower()
        branch.mkdir()
        dump(branch / "source-checks.json", {"checks": [], "fixture_only": True})
        progress(branch, "FIXTURE_INPUT", branch=label)
        verified = finalize_check(branch, {"status": label, "fixture_only": True,
            "intermediates_eligible": False}, "FINISHED" if label == "PASS" else "FAILED", {"status": label})
        if not verified["progress_in_manifest"] or not verified["source_checks_in_manifest"]:
            raise ReplayError("terminal manifest fixture omitted progress/source checks")
        copied = run / (label.lower() + "-tamper-copy")
        shutil.copytree(branch, copied)
        with (copied / "progress.jsonl").open("a", encoding="utf-8") as output:
            output.write('{"stage":"UNEXPECTED_POST_SEAL_APPEND"}\n')
        try:
            verify_final_manifest(copied)
        except ReplayError:
            rejected = True
        else:
            raise ReplayError("terminal manifest fixture accepted modified sealed progress")
        verify_final_manifest(branch)
        branches.append({"status": label, "final_manifest": verified, "post_seal_append_rejected": rejected})
    item = {"name": "terminal_manifest", "entry": "tool_integrity_only", "passed": True,
        "branches": branches, "methods_executed": False,
        "meaning": "terminal/source/log integrity fixture only; no mechanism evidence"}
    dump(run / "check.json", item)
    return item


def fixtures(directory, closure_path, closure_sha256):
    import copy
    import numpy as np
    import pandas as pd
    audit = []
    closure = load_closure(closure_path, closure_sha256, audit)
    prepare_imports(closure, audit)
    dump(directory / "source-checks.json", {"checks": audit})
    from circa_kien_truc.scoring import score_graph
    from RCAEval.classes.graph import Node, MemoryGraph
    from RCAEval.graph_heads.rht import ANMRegressor, DAScorer
    from RCAEval.graph_heads.random_walk import Score
    import networkx as nx
    checks = []
    checks.extend(serializer_table_fixtures(directory))
    checks.append(nodeview_fixture(directory))
    checks.append(adapter_table_fixture(directory))
    def outcome(call):
        try:
            return call(), None
        except Exception as error:
            return None, {"type": type(error).__name__, "message": str(error)}
    def pure(value):
        serializer = CircaCapture.__new__(CircaCapture)
        serializer.np, serializer.pd = np, pd
        return serializer._value(value)
    def profile(frame, event, arg):
        return None
    for kind in ("scalar_ols", "no_effective_parents", "prune_and_isolate", "all_pruned_no_evidence", "empty_graph", "value_error_fallback", "da_order"):
        run = directory / kind
        run.mkdir()
        progress(directory, "FIXTURE_START", name=kind)
        old_profile = sys.getprofile()
        sys.setprofile(profile)
        try:
            if kind in ("scalar_ols", "no_effective_parents", "prune_and_isolate", "all_pruned_no_evidence", "empty_graph"):
                frame, graph, t, current = fixture_inputs(kind)
                frame_before = frame.copy(deep=True)
                graph_before = (list(graph.nodes), list(graph.edges))
                call = lambda: score_graph(frame, graph, t, current)
                entry = "score_graph"
            elif kind == "value_error_fallback":
                train_x = np.array([[1.], [np.nan], [3.]])
                test_x = np.array([[2.], [4.]])
                train_y, test_y = np.array([0., 1., 2.]), np.array([3., 4.])
                arrays_before = [a.copy() for a in (train_x, test_x, train_y, test_y)]
                call = lambda: ANMRegressor().score(train_x, test_x, train_y, test_y)
                entry = "regressor"
            else:
                nodes = [Node("a", "cpu"), Node("b", "cpu"), Node("c", "cpu"), Node("isolate", "cpu")]
                dag = nx.DiGraph()
                dag.add_nodes_from(nodes)
                dag.add_edges_from([(nodes[0], nodes[1]), (nodes[1], nodes[2])])
                base_scores = {n: Score(v, info={"z-score": v, "Confidence": 0.5}) for n, v in zip(nodes, (4., 2., 5., 3.))}
                def call():
                    scores = copy.deepcopy(base_scores)
                    mg = MemoryGraph(dag.copy())
                    # data/current are unused by DA. Capture expects the native
                    # CaseData fields; supply an actual native CaseData object.
                    from RCAEval.classes.data import CaseData, MemoryDataLoader
                    from datetime import timedelta
                    case = CaseData(MemoryDataLoader({}), nodes[0], 1000, interval=timedelta(seconds=1))
                    returned = DAScorer(threshold=3).score(mg, case, 1001, scores)
                    if returned is not scores:
                        raise ReplayError("native DA mutation/return identity changed")
                    return returned
                entry = "da"
            original, original_exception = outcome(call)
            with CircaCapture(run / "capture", entry=entry) as capture:
                observed, observed_exception = outcome(call)
            summary = capture.require_complete()
            check = capture_checks(run / "capture", summary)
            differences = exact_differences(pure(original), pure(observed)) + exact_differences(original_exception, observed_exception)
            if sys.getprofile() is not profile or sys.gettrace() is not None:
                raise ReplayError("fixture trace/profile restore failed")
            if entry == "score_graph":
                pd.testing.assert_frame_equal(frame, frame_before, check_exact=True)
                if graph_before != (list(graph.nodes), list(graph.edges)):
                    raise ReplayError("observer/native changed fixture graph")
                if kind == "prune_and_isolate":
                    if observed["meta"]["dropped_constant_or_missing"] != ["constant_cpu", "missing_cpu"] or "isolate_mem" not in observed["nodes"]:
                        raise ReplayError("native prune/isolate fixture did not exercise declared path")
                if kind == "all_pruned_no_evidence" and (observed["nodes"] or observed["ranks"] or observed["ranks_da"]):
                    raise ReplayError("native all-pruned fixture unexpectedly returned evidence")
            if kind == "value_error_fallback":
                for before, after in zip(arrays_before, (train_x, test_x, train_y, test_y)):
                    np.testing.assert_array_equal(before, after)
                reg = [read(run / "capture" / c["path"]) for c in summary["calls"] if c["function"] == "regressor"]
                if original_exception is not None or observed_exception is not None or reg[0]["exit"]["route"] != "value_error_fallback":
                    raise ReplayError("fixture did not observe original ValueError fallback")
            if kind == "da_order":
                if observed[nodes[0]].score != 9. or observed[nodes[1]].score != 2.:
                    raise ReplayError("native DA fixture failed to exercise below-threshold descendant propagation")
                if check["da_journal"]["group_count"] < 2:
                    raise ReplayError("native DA order fixture did not exercise multiple topological groups")
            item = {"name": kind, "entry": entry, "passed": not differences, "differences": differences,
                "original_exception": original_exception, "observed_exception": observed_exception,
                "capture": check, "profile_restored": True, "meaning": "observation fixture only; no mechanism evidence"}
            dump(run / "check.json", item)
            checks.append(item)
        finally:
            sys.setprofile(old_profile)
    checks.extend(focused_da_fixtures(directory))
    checks.append(terminal_manifest_fixture(directory))
    if len(checks) != 23:
        raise ReplayError("all 19 preserved and four declared new CIRCA fixtures are required")
    load_closure(closure_path, closure_sha256, audit)
    check_imports(closure, audit)
    dump(directory / "source-checks.json", {"checks": audit})
    passed = all(c["passed"] for c in checks)
    finalize_check(directory, {"status": "PASS" if passed else "FAIL", "fixtures": checks,
        "source_verified": True, "source_closure_sha256": closure_sha256, "mechanism_evidence": False,
        "preserved_fixture_count": 19, "new_fixture_count": 4},
        "FIXTURES_FINISHED", {"status": "PASS" if passed else "FAIL"})
    return 0 if passed else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("one", "fixture", "native", "audit-fixture"):
        p = sub.add_parser(command)
        if command in ("one", "native"):
            p.add_argument("dataset", choices=("RE2-TT", "Nezha-OB"))
            p.add_argument("opaque_id" if command == "one" else "job")
        p.add_argument("directory")
        p.add_argument("--source-closure", required=True)
        p.add_argument("--source-closure-sha256", required=True)
        p.add_argument("--repo-root", default=str(shared.REPO))
        if command == "audit-fixture":
            p.add_argument("--old-run", required=True)
            p.add_argument("--transport-inventory", required=True)
            p.add_argument("--transport-inventory-sha256", required=True)
    args = parser.parse_args()
    shared.REPO = Path(args.repo_root).expanduser().resolve()
    if os.environ.get("PYTHONHASHSEED") != "0":
        raise ReplayError("PYTHONHASHSEED=0 must be set before starting Python")
    if args.command == "native":
        return native_child(args)
    directory = new_directory(args.directory)
    try:
        if args.command == "audit-fixture":
            audit_dir = new_directory(directory / "audit")
            progress(directory, "STORED_CAPTURE_AUDIT_START")
            code = audit_stored_fixture(audit_dir, args.old_run, args.transport_inventory,
                args.transport_inventory_sha256, args.source_closure, args.source_closure_sha256)
            audit_check = read(audit_dir / "check.json")
            verify_final_manifest(audit_dir)
            if code != 0 or audit_check.get("status") != "PASS_STORED_CAPTURE_AUDIT" or audit_check.get("intermediates_eligible") is not False:
                raise ReplayError("stored capture audit did not pass; no fresh fixture/native may start")
            progress(directory, "STORED_CAPTURE_AUDIT_PASS", eligible_old_capture=False)
            fixture_dir = new_directory(directory / "fixtures")
            progress(directory, "FULL_FRESH_FIXTURES_START")
            code = fixtures(fixture_dir, args.source_closure, args.source_closure_sha256)
            fixture_check = read(fixture_dir / "check.json")
            verify_final_manifest(fixture_dir)
            if code != 0 or fixture_check.get("status") != "PASS" or len(fixture_check.get("fixtures", [])) != 23:
                raise ReplayError("full fresh CIRCA fixture did not pass all 23 declared fixtures")
            combined_sources = read(audit_dir / "source-checks.json")["checks"] + read(fixture_dir / "source-checks.json")["checks"]
            dump(directory / "source-checks.json", {"checks": combined_sources})
            finalize_check(directory, {"status": "PASS_AUDIT_AND_FIXTURES", "method": "circa",
                "source_verified": True, "source_closure_sha256": args.source_closure_sha256,
                "audit_check_path": "audit/check.json", "audit_check_sha256": sha(audit_dir / "check.json"),
                "fixture_check_path": "fixtures/check.json", "fixture_check_sha256": sha(fixture_dir / "check.json"),
                "fixtures_passed": 23, "old_capture_intermediates_eligible": False,
                "pilot_started": False, "mechanism_evidence": False},
                "AUDIT_AND_FIXTURES_FINISHED", {"status": "PASS_AUDIT_AND_FIXTURES"})
            return 0
        if args.command == "fixture":
            # Authenticate source bytes before importing any native module.
            closure = load_closure(args.source_closure, args.source_closure_sha256, [])
            prepare_imports(closure, [])
            return fixtures(directory, args.source_closure, args.source_closure_sha256)
        return one(directory, args.dataset, args.opaque_id, args.source_closure, args.source_closure_sha256)
    except BaseException as error:
        if not (directory / "source-checks.json").exists():
            available = [path for path in (directory / "audit" / "source-checks.json",
                directory / "fixtures" / "source-checks.json") if path.is_file()]
            dump(directory / "source-checks.json", {"checks": [item for path in available
                for item in read(path).get("checks", [])],
                "status": "partial failure audit; not a source verification PASS",
                "available_child_source_checks": [path.relative_to(directory).as_posix() for path in available]})
        check_name = "failure-after-check.json" if (directory / "check.json").exists() else "check.json"
        failure = {"status": "FAIL", "method": "circa", "error_type": type(error).__name__, "error": str(error),
            "traceback": traceback.format_exc(), "intermediates_eligible": False,
            "source_closure_sha256": args.source_closure_sha256}
        if check_name != "check.json":
            failure["superseded_check"] = {"path": "check.json", "sha256": sha(directory / "check.json"),
                "earlier_result_usable": False}
        finalize_check(directory, failure, "FAILED", {"error": str(error)}, check_name)
        return 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
