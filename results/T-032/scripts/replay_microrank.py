"""T-032: observational MicroRank fixtures or one frozen main-cohort replay.

Usage (existing EC2 environment and PYTHONPATH are supplied by the launcher)::

    python -B -X utf8 replay_microrank.py fixture <new_run_dir>
    python -B -X utf8 replay_microrank.py one RE2-TT <opaque_id> <new_run_dir>
    python -B -X utf8 replay_microrank.py one Nezha-OB <opaque_id> <new_run_dir>

Run directories must be new and below ~/rca/T-032 or results/T-032. All
artifacts, partial failures and worker output are retained. check.json PASS
means the declared exact fields and capture/matrix checks passed. It is not
a causal conclusion, a successful diagnosis, or permission to run A-prime.

Source roots are fixed to the approved EC2 layout. Workers are called once in
this process under the observational context; this preserves their original
loading/window/adapter code. RE2 records are reconstructed by runner._ket_thuc.
Nezha records follow run.py or the actual reused run_pilot.py provenance branch.
Only run_id and measured cost are excluded from frozen record comparison;
all remaining fields, including error/diagnostics/extra, are compared exactly.
No numerical tolerance, ranking normalization, result replacement or fallback
to another case/machine is applied. TIMEOUT sources require separate handling.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
import time
import traceback

from capture_microrank import MicroRankCapture


REPO = Path("/home/ubuntu/rca/T-032/repo")
RE2_RAW_REPO = Path("/home/ubuntu/rca/T-031/repo")
M24 = "results/T-029/runs/compare-rca-preparation-001/manifest.json"
I24 = "results/T-024/ban-ghi-dua-vao-cham.json"
M26 = "results/T-026/runs/session-005/handoff-manifest.json"
I26 = "results/T-026/ban-ghi-dua-vao-cham.json"
EXACT_FIELDS = (
    "opaque_id", "method", "method_version", "variant", "mode", "detector",
    "detector_columns", "seed", "hashseed", "config_id", "why_ids", "window",
    "input_shape", "status", "method_status_raw", "error", "ranking_native",
    "ranking", "entity_ranking", "blocks", "sets", "diagnostics", "extra", "input_sha256",
)
EXCLUDED_FIELDS = {
    "run_id": "new execution identifier; source identifier is preserved in source.json",
    "cost": "new measured execution cost including observation; never copied from source",
}


class ReplayError(RuntimeError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as destination:
        json.dump(value, destination, ensure_ascii=False, indent=2, allow_nan=False)
        destination.write("\n")


def safe_source(relative):
    if not isinstance(relative, str) or "\\" in relative:
        raise ReplayError("source path must be a relative POSIX path")
    path = PurePosixPath(relative)
    if path.is_absolute() or re.match(r"^[A-Za-z]:", relative) or any(part in (".", "..") for part in path.parts):
        raise ReplayError("absolute/traversing source path rejected")
    if any(part.lower() in ("locked", "t-033", "test", "tests") for part in path.parts):
        raise ReplayError("source path outside this task's read scope")
    if "flash-ticket-rca-research" in relative.lower():
        raise ReplayError("archived repository is outside scope")
    resolved = (REPO / Path(*path.parts)).resolve()
    if REPO.resolve() not in resolved.parents:
        raise ReplayError("source path escaped copied repository")
    return resolved


def new_directory(raw):
    path = Path(raw).expanduser().resolve()
    if not any(parent.name == "T-032" and parent.parent.name in ("rca", "results") for parent in path.parents):
        raise ReplayError("new run must be below rca/T-032 or results/T-032")
    path.mkdir(parents=True, exist_ok=False)
    return path


def progress(directory, stage, **fields):
    event = {"at_utc": now(), "stage": stage, **fields}
    with (directory / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as destination:
        destination.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps(event, ensure_ascii=False), flush=True)


def verify(relative, expected, authority, audit):
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ReplayError("missing/invalid expected hash for " + relative)
    path = safe_source(relative)
    actual = sha(path)
    audit.append({"path": relative, "authority": authority, "expected": expected,
                  "actual": actual, "pass": actual == expected, "bytes": path.stat().st_size})
    if actual != expected:
        raise ReplayError("source hash mismatch: " + relative)
    return path


def verified_index26(audit):
    manifest = read(safe_source(M26))
    path = verify(I26, manifest["files"][I26]["sha256"], M26 + "#/files", audit)
    return read(path)


def source_for(dataset, opaque_id, audit):
    if not re.fullmatch(r"dev-[0-9a-f]{10}", opaque_id):
        raise ReplayError("invalid opaque dev ID")
    i26 = verified_index26(audit)
    if dataset == "RE2-TT":
        manifest = read(safe_source(M24))
        index = read(verify(I24, manifest["source_hashes"][I24], M24 + "#/source_hashes", audit))
        entries = [entry for entry in index["records"] if entry["method"] == "microrank"
                   and entry["variant"] == "full" and entry["opaque_id"] == opaque_id]
        authority = I24 + "#/records"
    else:
        index = i26
        entries = [entry for entry in index["unique_records"] if entry["worker_method"] == "microrank"
                   and entry["source_view"] == "main" and entry["opaque_id"] == opaque_id]
        authority = I26 + "#/unique_records"
    if len(entries) != 1:
        raise ReplayError("expected exactly one frozen main/full record for the requested ID")
    entry = entries[0]
    record = read(verify(entry["path"], entry["sha256"], authority, audit))
    if dataset == "RE2-TT":
        expected_in_manifest = manifest["source_hashes"].get(entry["path"])
        # T-029 directly lists only a subset of P3 records. The complete T-024
        # index is itself frozen there and authenticates each record/config.
        # Cross-check a direct record entry when one exists, without treating
        # an absent optional entry as a hash mismatch.
        if expected_in_manifest is not None and expected_in_manifest != entry["sha256"]:
            raise ReplayError("T-024 record hash disagrees with compare-rca source manifest")
        config = read(verify(entry["source_config"], entry["source_config_sha256"], authority, audit))
        code_hashes = config["src_p3"]["tep"]
    else:
        code_hashes = {path: value for path, value in i26["source_hashes"].items()
                       if path.startswith("src/p3/") and path.endswith(".py")}
    # The shared native implementation is frozen in T-026's source manifest;
    # the RE2 run configuration independently freezes its own adapter/runner.
    code_hashes = dict(code_hashes)
    code_hashes.update({path: value for path, value in i26["source_hashes"].items()
                        if path.startswith("src/microrank/") and path.endswith(".py")})
    for path, expected in sorted(code_hashes.items()):
        verify(path, expected, "source configuration / " + I26 + "#/source_hashes", audit)
    if (record["opaque_id"] != opaque_id or record["method"] != "microrank"
            or record["variant"] != "full" or record["mode"] != "a"
            or record["seed"] is not None or record["hashseed"] != 0):
        raise ReplayError("source metadata is outside the declared main/full/h0 replay scope")
    if record["status"] not in ("OK", "NO_EVIDENCE", "ERROR") or record["window"] is None:
        raise ReplayError("source requires a different replay path (for example TIMEOUT)")
    if os.environ.get("PYTHONHASHSEED") != str(record["hashseed"]):
        raise ReplayError("launch Python with the frozen PYTHONHASHSEED; changing it after startup is not valid")
    return entry, record, i26, code_hashes


def loaded_sources(code_hashes):
    """Check actual imports, not just a matching unused copy of source files."""
    result = []
    for name, module in sorted(sys.modules.copy().items()):
        if name != "p3" and not name.startswith("p3.") and name != "microrank" and not name.startswith("microrank."):
            continue
        raw = getattr(module, "__file__", None)
        if raw is None:
            continue
        path = Path(raw).resolve()
        try:
            relative = path.relative_to(REPO.resolve()).as_posix()
        except ValueError as error:
            raise ReplayError("import resolved outside copied source repository: " + name) from error
        if relative not in code_hashes or sha(path) != code_hashes[relative]:
            raise ReplayError("actual imported source is not frozen: " + name)
        result.append({"module": name, "path": relative, "sha256": code_hashes[relative]})
    return result


def literal_constants(path):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ("WHY", "CONFIG"):
                    values[target.id] = ast.literal_eval(node.value)
    if set(values) != {"WHY", "CONFIG"}:
        raise ReplayError("source script did not contain literal WHY and CONFIG")
    return values


def exact_differences(expected, actual, pointer=""):
    """Full differences: exact values/types and sequence order, no tolerance."""
    differences = []
    if type(expected) is not type(actual):
        return [{"pointer": pointer, "kind": "type", "expected": expected, "actual": actual}]
    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(actual)):
            child = pointer + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in expected or key not in actual:
                differences.append({"pointer": child, "kind": "key_presence",
                                    "expected_present": key in expected, "actual_present": key in actual})
            else:
                differences.extend(exact_differences(expected[key], actual[key], child))
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            differences.append({"pointer": pointer, "kind": "length", "expected": len(expected), "actual": len(actual)})
        for index, (left, right) in enumerate(zip(expected, actual)):
            differences.extend(exact_differences(left, right, pointer + "/" + str(index)))
    elif isinstance(expected, float):
        if expected.hex() != actual.hex():
            differences.append({"pointer": pointer, "kind": "float_exact", "expected": expected,
                                "actual": actual, "expected_hex": expected.hex(), "actual_hex": actual.hex()})
    elif expected != actual:
        differences.append({"pointer": pointer, "kind": "value", "expected": expected, "actual": actual})
    return differences


def compare_records(frozen, replay):
    fields = set(EXACT_FIELDS) | set(EXCLUDED_FIELDS)
    if set(frozen) != fields or set(replay) != fields:
        raise ReplayError("record schema changed; explicit field list must be reviewed before comparison")
    return exact_differences({key: frozen[key] for key in EXACT_FIELDS},
                             {key: replay[key] for key in EXACT_FIELDS})


def decode(value):
    if isinstance(value, list):
        return [decode(item) for item in value]
    if isinstance(value, dict):
        if set(value) == {"__nonfinite__"}:
            return {"NaN": math.nan, "+inf": math.inf, "-inf": -math.inf}[value["__nonfinite__"]]
        if set(value) == {"__missing__"}:
            import pandas as pd
            return {"None": None, "pandas.NA": pd.NA, "pandas.NaT": pd.NaT}[value["__missing__"]]
        if set(value) == {"__set__"}:
            return set(decode(item) for item in value["__set__"])
        return {key: decode(item) for key, item in value.items()}
    return value


def table_columns(directory, meta):
    import numpy as np
    import pandas as pd
    path = (directory / meta["path"]).resolve()
    if directory.resolve() not in path.parents:
        raise ReplayError("capture table reference escaped its directory")
    stored = pd.read_parquet(path)
    if len(stored) != meta["rows"]:
        raise ReplayError("capture table row count mismatch")
    result = {}
    for column in meta["columns"]:
        values = stored[column["storage"]]
        if column["encoding"] == "tagged_json_scalar":
            array = np.asarray([decode(json.loads(value)) for value in values], dtype=column["dtype"])
        else:
            array = values.to_numpy(dtype=column["dtype"], copy=True)
        if "special_state_column" in column:
            state = stored[column["special_state_column"]].to_numpy()
            if not np.isin(state, [0, 1, 2, 3]).all():
                raise ReplayError("unknown nonfinite state")
            array[state == 1], array[state == 2], array[state == 3] = np.nan, np.inf, -np.inf
        result[decode(column["name"])] = array
    return result


def verify_capture(directory, summary):
    """Check all captured files and exact reconstruction of every saved array."""
    import numpy as np
    arrays, checked_files = {}, []
    for artifact in summary["artifacts"]:
        path = (directory / artifact["path"]).resolve()
        if directory.resolve() not in path.parents:
            raise ReplayError("capture manifest path escaped directory")
        actual = sha(path)
        if actual != artifact["sha256"] or path.stat().st_size != artifact["bytes"]:
            raise ReplayError("captured artifact hash/size mismatch: " + artifact["path"])
        checked_files.append(artifact["path"])

    def collect(value):
        if isinstance(value, dict):
            if {"dense_c_order_sha256", "dtype", "shape", "table"} <= set(value):
                key = value["table"]["path"]
                if key in arrays and arrays[key] != value:
                    raise ReplayError("conflicting array metadata for the same file")
                arrays[key] = value
            for item in value.values():
                collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)

    for call in summary["calls"]:
        collect(read(directory / call["path"]))
    checked_arrays = []
    for path, meta in arrays.items():
        columns = table_columns(directory, meta["table"])
        dtype = np.dtype(meta["dtype"])
        if meta["encoding"].startswith("sparse_coordinates"):
            matrix = np.zeros(meta["shape"], dtype=dtype)
            rows, cols = columns["row"], columns["column"]
            if (np.any(rows < 0) or np.any(cols < 0) or np.any(rows >= matrix.shape[0])
                    or np.any(cols >= matrix.shape[1])):
                raise ReplayError("sparse matrix coordinate out of bounds")
            coordinates = np.stack([rows, cols], axis=1)
            if len(np.unique(coordinates, axis=0)) != len(rows):
                raise ReplayError("duplicate sparse matrix coordinates")
            matrix[rows, cols] = columns["value"].astype(dtype, copy=False)
        elif meta["encoding"] == "dense_c_order":
            matrix = columns["value"].astype(dtype, copy=False).reshape(meta["shape"])
        else:
            raise ReplayError("unknown array representation")
        actual = hashlib.sha256(np.ascontiguousarray(matrix).tobytes(order="C")).hexdigest()
        if actual != meta["dense_c_order_sha256"]:
            raise ReplayError("restored array is not byte-exact: " + path)
        checked_arrays.append({"path": path, "shape": meta["shape"], "dtype": meta["dtype"], "pass": True})
        del matrix, columns
    return {"pass": True, "artifact_files_checked": checked_files, "arrays_reconstructed": checked_arrays}


def measured_cost(start, hashseed):
    import resource
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {"wall_s": round(time.perf_counter() - start, 6),
            "peak_rss_mb": usage.ru_maxrss / 1024.0, "read_bytes": 0, "write_bytes": 0,
            "exit_code": 0, "timed_out": False, "env": "T-032-current-process-observed",
            "hashseed": hashseed, "measurement_note": "wall includes capture; RSS is process lifetime peak; IO not measured"}


def artifact_manifest(directory):
    """Run-local immutable files; check.json cannot hash itself."""
    return [{"path": path.relative_to(directory).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
            for path in sorted(directory.rglob("*")) if path.is_file()
            and path != directory / "check.json"]


def one(directory, dataset, opaque_id):
    audit = []
    progress(directory, "SOURCE_CHECK_START", dataset=dataset, opaque_id=opaque_id)
    try:
        entry, frozen, i26, code_hashes = source_for(dataset, opaque_id, audit)
        from p3 import ban_ghi, runner, selector, worker
        from p3.adapters import microrank as adapter
        import microrank
        if dataset == "RE2-TT":
            allow_path = safe_source("results/T-022/allowlist-dev.json")
            allow = selector.nap_allowlist(allow_path)
            if opaque_id not in allow:
                raise ReplayError("requested source case not in allowlist")
            wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
            if wanted != frozen["input_sha256"]:
                raise ReplayError("selected allowlist hashes do not equal frozen input hashes")
            # Only selector touches raw paths; it checks allowlist membership,
            # containment and all bytes. The unchanged worker verifies again.
            files = selector.chon_ca(allow, opaque_id, RE2_RAW_REPO, kiem_hash=True)
            job = {"kind": "ranker", "method": "microrank", "t": frozen["window"]["t"],
                   "model": None, "files": {name: {"path": path, "sha256": wanted[name]}
                                             for name, path in files.items()}}
            constants = None
            invoke_worker = worker.main
        else:
            from p3 import nezha, nezha_worker
            from p3.adapters.nezha import VARIANTS, VERSIONS
            allow_relative = "results/T-026/allowlist-dev.json"
            allow_path = verify(allow_relative, i26["source_hashes"][allow_relative], I26 + "#/source_hashes", audit)
            allow = nezha.nap_allowlist(allow_path)
            if opaque_id not in allow or entry["trace_guard_s"] != 0:
                raise ReplayError("requested main case or guard outside scope")
            wanted = {path: meta["sha256"] for path, meta in allow[opaque_id]["files"].items()}
            if wanted != frozen["input_sha256"]:
                raise ReplayError("selected Nezha allowlist hashes do not equal frozen input hashes")
            job = {"allowlist_path": str(allow_path), "opaque_id": opaque_id, "repo_root": str(REPO),
                   "view": "main", "method": "microrank", "trace_guard_s": 0}
            script = "results/T-026/scripts/run_pilot.py" if entry["reused_pilot"] else "results/T-026/scripts/run.py"
            constants = literal_constants(verify(script, i26["source_hashes"][script], I26 + "#/source_hashes", audit))
            invoke_worker = nezha_worker.main
        actual_imports = loaded_sources(code_hashes)
        dump(directory / "source.json", {"dataset": dataset, "opaque_id": opaque_id,
             "entry": entry, "source_run_id": frozen["run_id"], "source_status": frozen["status"],
             "allowlist_path": str(allow_path), "allowlist_sha256": sha(allow_path),
             "selected_allowlist_hashes_equal_frozen_inputs": True, "actual_imports": actual_imports,
             "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS})
        dump(directory / "job.json", job)
        progress(directory, "WORKER_START", source_status=frozen["status"])
        started = time.perf_counter()
        with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout:
            with (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    with MicroRankCapture(directory / "capture") as capture:
                        invoke_worker(str(directory / "job.json"), str(directory / "ket-qua.json"))
        capture_summary = capture.require_complete()
        cost = measured_cost(started, frozen["hashseed"])
        dump(directory / "cost.json", cost)
        output = read(directory / "ket-qua.json")
        if output.get("hashseed") != str(frozen["hashseed"]):
            raise ReplayError("worker reported a different hashseed")
        if dataset == "RE2-TT":
            base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None,
                    "hashseed": 0, "detector": None, "detector_columns": None, "config_id": "p3-re2tt-v2"}
            records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, "microrank", "a")
            if len(records) != 1:
                raise ReplayError("RE2 MicroRank reconstruction did not return exactly one record")
        else:
            results = output["ket_qua_nhieu"]
            if len(results) != 1:
                raise ReplayError("Nezha MicroRank worker did not return exactly one result")
            result = results[0]
            record = ban_ghi.tao("microrank", VERSIONS["microrank"], VARIANTS["microrank"], "a", result,
                                 output["window"], constants["CONFIG"], constants["WHY"], seed=None,
                                 hashseed=0, run_id=directory.name, opaque_id=opaque_id)
            record["cost"] = {**cost, "buoc_s": output.get("buoc_s", {})}
            record["input_sha256"] = output["input_sha256"]
            if entry["reused_pilot"]:
                record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
            else:
                record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
            ban_ghi.kiem(record)
            dump(directory / "ban-ghi-0.json", record)
            records = [record]
        # Compare serialized record values, including type/float.hex equality.
        replay = read(directory / "ban-ghi-0.json")
        differences = compare_records(frozen, replay)
        progress(directory, "FROZEN_COMPARE_DONE", match=not differences)
        matrix_check = verify_capture(directory / "capture", capture_summary)
        imports_after = loaded_sources(code_hashes)
        dump(directory / "source-checks.json", {"checks": audit})
        progress(directory, "FINISHED", status="PASS" if not differences else "FAIL")
        check = {"status": "PASS" if not differences else "FAIL", "dataset": dataset, "opaque_id": opaque_id,
                 "frozen_path": entry["path"], "frozen_sha256": entry["sha256"],
                 "frozen_status": frozen["status"], "replay_status": replay["status"],
                 "exact_fields": EXACT_FIELDS, "excluded_fields": EXCLUDED_FIELDS, "differences": differences,
                 "compare": {"pass": not differences, "exact_fields": EXACT_FIELDS,
                             "excluded_fields": EXCLUDED_FIELDS, "difference_count": len(differences)},
                 "capture_status": capture_summary["status"], "capture_check": matrix_check,
                 "actual_imports_after": imports_after, "intermediates_eligible": not differences,
                 "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
                 "interpretation": "exact replay of this record only; native ERROR remains ERROR; no causal conclusion"}
        dump(directory / "check.json", check)
        return 0 if not differences else 1
    finally:
        if not (directory / "source-checks.json").exists():
            dump(directory / "source-checks.json", {"checks": audit})


def fixture_spans(kind):
    import pandas as pd
    t = 1_700_000_000
    boundary = t * 1_000_000
    rows = []
    for trace, offset, caller, child in (
        ("n0", -20_000_000, 1_000, 500), ("n1", -10_000_000, 2_000, 1_000),
        ("a0", 10_000_000, 1_000, 500), ("a1", 20_000_000, 20_000, 10_000),
    ):
        if trace.startswith("a") and kind == "no_anomalous":
            caller, child = 1_000, 500
        if trace.startswith("a") and kind == "no_normal":
            caller, child = 20_000, 10_000
        for span, parent, service, duration, delta in (
            ("caller", "0", "caller", caller, 0), ("child", "caller", "child", child, 100),
        ):
            rows.append((trace, span, parent, service, "operation", "operation", boundary + offset + delta, duration))
    if kind == "new_operation_error":
        rows.append(("a1", "new", "caller", "newservice", "new", "new", boundary + 20_000_200, 500))
    return pd.DataFrame(rows, columns=("traceID", "spanID", "parentSpanID", "serviceName",
                                      "methodName", "operationName", "startTime", "duration")), t


def fixtures(directory):
    import pandas as pd
    from p3 import ban_ghi
    from p3.adapters.microrank import chay
    cases = (("ok", "OK", "ok"), ("no_anomalous", "NO_EVIDENCE", "no_anomalous_traces"),
             ("no_normal", "NO_EVIDENCE", "no_normal_traces"), ("new_operation_error", "ERROR", None))
    checks = []
    for name, expected_status, expected_native in cases:
        case_dir = directory / name
        case_dir.mkdir()
        spans, t = fixture_spans(name)
        retained_input = spans.copy(deep=True)
        progress(directory, "FIXTURE_START", name=name)
        with (case_dir / "stdout.txt").open("x", encoding="utf-8") as stdout:
            with (case_dir / "stderr.txt").open("x", encoding="utf-8") as stderr:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    original = chay(spans, t)
                    with MicroRankCapture(case_dir / "capture") as capture:
                        observed = chay(spans, t)
        summary = capture.require_complete()
        pd.testing.assert_frame_equal(spans, retained_input, check_exact=True)
        # JSON serialization supplies the same list/number representation used
        # by the real worker and avoids comparing tuples to saved JSON lists.
        original = json.loads(json.dumps(original, allow_nan=False))
        observed = json.loads(json.dumps(observed, allow_nan=False))
        dump(case_dir / "original-adapter.json", original)
        dump(case_dir / "observed-adapter.json", observed)
        diffs = exact_differences(original, observed)
        status_ok = original["status"] == expected_status and original.get("method_status_raw") == expected_native
        kwargs = {"method": "microrank", "method_version": "synthetic fixture only", "variant": "full",
                  "mode": "a", "window": {"t": t}, "config_id": "T-032-fixture", "why_ids": [], "hashseed": 0}
        original_record = ban_ghi.tao(ket_qua=original, **kwargs)
        observed_record = ban_ghi.tao(ket_qua=observed, **kwargs)
        record_diffs = exact_differences(original_record, observed_record)
        matrix_check = verify_capture(case_dir / "capture", summary)
        check = {"name": name, "expected_status": expected_status, "actual_status": observed["status"],
                 "expected_native_status": expected_native, "actual_native_status": observed.get("method_status_raw"),
                 "input_unchanged": True, "adapter_differences": diffs, "record_differences": record_diffs,
                 "capture_check": matrix_check, "pass": status_ok and not diffs and not record_diffs}
        dump(case_dir / "check.json", check)
        checks.append(check)
        if not check["pass"]:
            dump(directory / "check.json", {"status": "FAIL", "fixtures": checks})
            return 1
        progress(directory, "FIXTURE_DONE", name=name, status="PASS")
    dump(directory / "check.json", {"status": "PASS", "fixtures": checks,
         "artifact_manifest": artifact_manifest(directory), "manifest_excludes": ["check.json"],
         "limits": "synthetic observer/output serialization checks; no frozen real-data replay or A-prime"})
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    fixture_parser = commands.add_parser("fixture")
    fixture_parser.add_argument("new_run_dir")
    one_parser = commands.add_parser("one")
    one_parser.add_argument("dataset", choices=("RE2-TT", "Nezha-OB"))
    one_parser.add_argument("opaque_id")
    one_parser.add_argument("new_run_dir")
    args = parser.parse_args()
    directory = new_directory(args.new_run_dir)
    dump(directory / "invocation.json", {"at_utc": now(), "argv": sys.argv,
         "script_sha256": sha(__file__), "capture_script_sha256": sha(Path(__file__).with_name("capture_microrank.py")),
         "python": sys.version, "hashseed": os.environ.get("PYTHONHASHSEED"),
         "command": args.command, "source_repo": str(REPO), "re2_raw_repo": str(RE2_RAW_REPO)})
    try:
        return fixtures(directory) if args.command == "fixture" else one(directory, args.dataset, args.opaque_id)
    except Exception as error:
        failure = {"status": "FAIL", "type": type(error).__name__, "error": str(error),
                   "traceback": traceback.format_exc(), "intermediates_eligible": False,
                   "retained": "all partial artifacts remain; no automatic retry or fallback"}
        if not (directory / "check.json").exists():
            dump(directory / "check.json", failure)
        else:
            dump(directory / "failure-after-check.json", failure)
        progress(directory, "FAILED", error=str(error))
        return 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
