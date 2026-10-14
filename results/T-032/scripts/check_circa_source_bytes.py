"""EC2-only, metadata/byte audit for the pinned T-032 CIRCA source closure.

No method code is imported, executed, copied or modified. All 120 declared
sources are checked even when an individual file is missing or differs. PASS
certifies these byte bindings only, not actual imports or numerical replay.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys


BASE = Path("/home/ubuntu/rca/T-032")
SOURCE_DIRECTORY = BASE / "sources/circa-source-001"
CLOSURE_SHA256 = "6d9f39dc6da49f15176caa7e59aa18b43f2664a4124dd048aa976d68cfce409f"
INVENTORY_SHA256 = "e67ab2364054c871d3264adb8b5c3e3ccf74ef46357c945efe970a942a37db6b"
HISTORICAL_PATH = BASE / "sources/T031/chay-5602e60b.py"
HISTORICAL_SHA256 = "5602e60b51a01ddd38e27ed86d6144636e73d08931c83d0342931b260dd7ac2f"
HISTORICAL_LF_SHA256 = "0b87d9166f9433ad748798078baf125ce3155c03f59ec83c76c0b5782f74623d"
HISTORICAL_BYTES = 9813
LOGICAL_LAUNCHER = "results/T-031/scripts/chay.py"
CODE_ROOTS = (BASE / "repo/src", Path("/home/ubuntu/rca/T-025/src"))
SOURCE_PREFIXES = ("p3", "circa_kien_truc", "RCAEval", "circa")
FORBIDDEN_PARTS = {"locked", "test", "tests", "heldout", "archive", "t-033", "t033"}
REVISIONS = {"RCAEval": "259ea4167160256a74ad30004aa3d96a998c846e",
             "CIRCA": "0215e1880096aa02a305c697f1c23cac4600ebd2"}


class SourceCheckError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise SourceCheckError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path_guard(raw, roots, suffix):
    require(isinstance(raw, (str, Path)), "source path must be text")
    original = Path(raw).expanduser()
    require(original.is_absolute(), "absolute source/artifact path required")
    require(not any(part.lower() in FORBIDDEN_PARTS for part in original.parts),
            "path contains excluded task/data scope")
    require("flash-ticket-rca-research" not in str(original).lower(), "archive path rejected")
    resolved = original.resolve()
    require(not any(part.lower() in FORBIDDEN_PARTS for part in resolved.parts),
            "resolved path contains excluded task/data scope")
    require("flash-ticket-rca-research" not in str(resolved).lower(), "resolved archive path rejected")
    require(any(root in resolved.parents for root in roots), "resolved path outside approved roots")
    require(resolved.suffix == suffix, "unexpected source/artifact suffix")
    return resolved


def parse_json(data):
    def reject_constant(token):
        raise SourceCheckError("nonfinite JSON token: " + token)
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(data.decode("utf-8-sig"), parse_constant=reject_constant,
                      object_pairs_hook=unique_object)


def metadata(raw_path, expected, audit):
    row = {"requested_path": str(raw_path), "expected_sha256": expected, "status": "FAIL"}
    audit.append(row)
    path = path_guard(raw_path, (BASE / "sources",), ".json")
    row["resolved_path"] = str(path)
    require(path.is_file(), "metadata is missing: " + str(path))
    data = path.read_bytes()
    row.update(actual_sha256=digest(data), bytes=len(data))
    require(row["actual_sha256"] == expected, "pinned metadata byte hash mismatch: " + str(path))
    value = parse_json(data)
    row["status"] = "PASS"
    return value, data


def source_row(module, meta, inventory):
    row = {"module": module, "expected_path": meta.get("path") if isinstance(meta, dict) else None,
           "expected_sha256": meta.get("sha256") if isinstance(meta, dict) else None,
           "expected_bytes": meta.get("bytes") if isinstance(meta, dict) else None,
           "status": "INVALID_METADATA"}
    try:
        require(any(module == prefix or module.startswith(prefix + ".") for prefix in SOURCE_PREFIXES),
                "module outside the four approved namespaces")
        require(isinstance(meta, dict) and isinstance(inventory, dict), "source binding schema invalid")
        expected = meta.get("sha256")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
                "source expected hash invalid")
        require(type(meta.get("bytes")) is int and meta["bytes"] >= 0, "source expected bytes invalid")
        require(meta["path"] == inventory.get("runtime_path")
                and expected == inventory.get("sha256") and meta["bytes"] == inventory.get("bytes"),
                "closure/inventory module binding differs")
        require(bool(meta.get("authority")) and bool(inventory.get("evidence")), "source authority absent")
        row["authority_category"] = inventory.get("authority_category")
        row["status"] = "INVALID_PATH"
        path = path_guard(meta["path"], CODE_ROOTS, ".py")
        row["resolved_path"] = str(path)
        row["status"] = "MISSING"
        if not path.is_file():
            row["reason"] = "declared source is missing or not a regular file"
            return row
        row["status"] = "READ_ERROR"
        data = path.read_bytes()
        row.update(actual_sha256=digest(data), actual_bytes=len(data),
                   sha256_matches=digest(data) == expected, bytes_match=len(data) == meta["bytes"])
        row["status"] = "PASS" if row["sha256_matches"] and row["bytes_match"] else "DRIFT"
        if row["status"] == "DRIFT":
            row["reason"] = "actual raw bytes differ from the pinned closure; no normalization or replacement"
    except Exception as error:
        row.update(error_type=type(error).__name__, reason=str(error))
    return row


def historical_row(closure, inventory):
    row = {"logical_path": LOGICAL_LAUNCHER, "expected_path": str(HISTORICAL_PATH),
           "expected_sha256": HISTORICAL_SHA256, "expected_lf_sha256": HISTORICAL_LF_SHA256,
           "expected_bytes": HISTORICAL_BYTES, "status": "INVALID_METADATA",
           "origin": "reconstructed_exact_bytes", "historical_artifact_found": False,
           "launcher_executed_by_utility": False}
    try:
        meta = closure.get("historical_launchers", {}).get(LOGICAL_LAUNCHER)
        proof = inventory.get("historical_launcher")
        require(isinstance(meta, dict) and isinstance(proof, dict), "historical snapshot binding missing")
        require(meta.get("path") == str(HISTORICAL_PATH)
                and meta.get("sha256") == HISTORICAL_SHA256 and meta.get("bytes") == HISTORICAL_BYTES,
                "closure historical snapshot binding changed")
        require(proof.get("snapshot_runtime_path") == str(HISTORICAL_PATH)
                and proof.get("sha256") == HISTORICAL_SHA256
                and proof.get("sha256_lf") == HISTORICAL_LF_SHA256
                and proof.get("bytes") == HISTORICAL_BYTES and proof.get("logical_path") == LOGICAL_LAUNCHER,
                "inventory historical snapshot binding changed")
        require(meta.get("authority") and proof.get("authorities")
                and proof.get("origin") == "reconstructed_exact_bytes"
                and proof.get("historical_artifact_found") is False
                and proof.get("launcher_executed_by_wrapper") is False
                and proof.get("original_source_mutated") is False,
                "historical snapshot provenance declaration invalid")
        row["status"] = "INVALID_PATH"
        path = path_guard(HISTORICAL_PATH, (BASE / "sources",), ".py")
        require(path == HISTORICAL_PATH, "historical snapshot resolved to a different path")
        row["resolved_path"] = str(path)
        row["status"] = "MISSING"
        if not path.is_file():
            row["reason"] = "historical snapshot is missing or not a regular file"
            return row
        row["status"] = "READ_ERROR"
        data = path.read_bytes()
        row.update(actual_sha256=digest(data), actual_lf_sha256=digest(data.replace(b"\r\n", b"\n")),
                   actual_bytes=len(data))
        row["status"] = ("PASS" if row["actual_sha256"] == HISTORICAL_SHA256
                         and row["actual_lf_sha256"] == HISTORICAL_LF_SHA256
                         and row["actual_bytes"] == HISTORICAL_BYTES else "DRIFT")
        if row["status"] == "DRIFT":
            row["reason"] = "historical snapshot raw/LF hash or length differs; file is retained unchanged"
    except Exception as error:
        row.update(error_type=type(error).__name__, reason=str(error))
    return row


def check(source_closure, source_inventory):
    report = {"schema": "T-032.circa-source-byte-check.v1", "status": "FAIL",
              "checked_at_utc": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(),
              "script_path": str(Path(__file__).resolve()),
              "script_sha256": digest(Path(__file__).read_bytes()),
              "metadata_checks": [], "expected_source_count": 120, "source_rows": [],
              "full_source_table_checked": False, "source_code_imported": False,
              "method_executed": False, "source_files_modified": False,
              "actual_import_paths_verified": False, "full_historical_hash_claimed": False,
              "cohort_ready": False, "A_prime_authorized": False,
              "limits": ["PASS binds current raw source bytes to the independently pinned metadata only.",
                         "The inventory separately identifies files without historical raw-hash authority.",
                         "Actual imports, fixtures, numerical replay and research mechanisms remain unchecked.",
                         "No alternative path, copied replacement or normalized source byte hash is accepted."]}
    try:
        closure, closure_data = metadata(source_closure, CLOSURE_SHA256, report["metadata_checks"])
        inventory, inventory_data = metadata(source_inventory, INVENTORY_SHA256, report["metadata_checks"])
        require(closure.get("schema") == "T-032.circa-source-closure.v1"
                and inventory.get("schema") == "T-032.circa-source-inventory.v1", "metadata schema changed")
        require(closure.get("revisions") == REVISIONS, "method revision declaration changed")
        binding = closure.get("source_inventory", {})
        require(binding.get("sha256") == INVENTORY_SHA256 and binding.get("bytes") == len(inventory_data),
                "closure inventory byte binding changed")
        files, proofs = closure.get("files"), inventory.get("files")
        require(isinstance(files, dict) and isinstance(proofs, dict)
                and len(files) == len(proofs) == 120 and set(files) == set(proofs),
                "metadata does not bind the same complete 120 modules")
        report["metadata_byte_hashes_verified"] = True
        report["source_inventory_binding"] = {"path": binding.get("path"), "sha256": INVENTORY_SHA256,
                                               "bytes": len(inventory_data)}
        report["closure_bytes"] = len(closure_data)
        report["source_rows"] = [source_row(module, files[module], proofs[module]) for module in sorted(files)]
        report["full_source_table_checked"] = True
        counts = Counter(row["status"] for row in report["source_rows"])
        report["source_counts"] = {status: counts[status] for status in
                                   ("PASS", "MISSING", "DRIFT", "READ_ERROR", "INVALID_PATH", "INVALID_METADATA")}
        report["historical_snapshot"] = historical_row(closure, inventory)
        report["status"] = ("PASS" if counts["PASS"] == 120
                            and report["historical_snapshot"]["status"] == "PASS" else "FAIL")
    except Exception as error:
        report.update(error_type=type(error).__name__, error=str(error),
                      status="FAIL_METADATA_CLOSED", metadata_byte_hashes_verified=False)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-closure", default=str(SOURCE_DIRECTORY / "source-closure.json"))
    parser.add_argument("--source-inventory", default=str(SOURCE_DIRECTORY / "source-inventory.json"))
    parser.add_argument("--out", required=True, help="new JSON file strictly below T032/runs; parent must exist")
    args = parser.parse_args()
    require(sys.platform == "linux" and Path.home().resolve() == Path("/home/ubuntu")
            and Path(__file__).resolve().parent == BASE / "scripts", "EC2-only T032 byte-check utility")
    output = path_guard(args.out, (BASE / "runs",), ".json")
    require(not output.exists() and output.parent.is_dir(), "output must be new with an existing approved parent")
    report = check(args.source_closure, args.source_inventory)
    data = (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    with output.open("xb") as stream:
        stream.write(data)
    print(json.dumps({"status": report["status"], "source_counts": report.get("source_counts"),
                      "full_source_table_checked": report["full_source_table_checked"],
                      "historical_status": report.get("historical_snapshot", {}).get("status"),
                      "output": str(output), "output_sha256": digest(data)}, ensure_ascii=False), flush=True)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SourceCheckError as error:
        print("FAIL_CLOSED: " + str(error), file=sys.stderr)
        raise SystemExit(1)
