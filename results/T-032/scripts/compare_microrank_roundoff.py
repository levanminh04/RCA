"""Separate T-032 MicroRank output comparator; never runs a ranking method.

The Minh-approved exception is restricted to operation/service score floats
and near-score inversions within one service. Source records and the old
exact comparator are not overwritten. All unmodified exact differences are
retained in the report. A record-contract PASS is not cohort authorization:
the T-028 flags/P0 bridge remains an explicitly missing external check.

EC2 CLI (both commands require a new output directory):
  fixture --out /home/ubuntu/rca/T-032/runs/<new>
  one --dataset RE2-TT --opaque-id dev-... --replay-run <existing-run>
      --replay-check-sha256 <trusted-check-hash> [--native-run <existing-run>
      --native-check-sha256 <trusted-check-hash>] --out <new-run>

Pure API:
  compare_records(frozen, observed, aggregator=verified_ban_ghi.xep_thuc_the,
                  evaluator=verified_danh_gia.cham_ca)
The caller must verify the two records and injected source functions. The API
has no file access, mutation of records, method execution or tolerance options.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path, PurePosixPath
import re
import struct
import sys
import traceback

BASE = Path("/home/ubuntu/rca/T-032")
REPO = BASE / "repo"
PACKAGE = BASE / "inputs/package-manifest.json"
PACKAGE_SHA256 = "03919f7895fedfd2aac8affd11d256acc5a4696341fed5812ef73c8ce417dec4"
INDEX24 = "results/T-024/ban-ghi-dua-vao-cham.json"
INDEX26 = "results/T-026/ban-ghi-dua-vao-cham.json"
MAX_ULP = 16
RELATIVE_LIMIT = Fraction(16, 1 << 52)
EXACT_FIELDS = (
    "opaque_id", "method", "method_version", "variant", "mode", "detector",
    "detector_columns", "seed", "hashseed", "config_id", "why_ids", "window",
    "input_shape", "status", "method_status_raw", "error", "ranking_native",
    "ranking", "entity_ranking", "blocks", "sets", "diagnostics", "extra",
    "input_sha256",
)
EXCLUDED_FIELDS = ("run_id", "cost")
RANK_FIELDS = ("ranking_native", "ranking", "entity_ranking")
KNOWN_STATUS = ("OK", "NO_EVIDENCE", "ERROR", "TIMEOUT", "UNSUPPORTED")


class ContractError(ValueError):
    pass


def binary64_bits(value):
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def ordered_binary64(value):
    bits = binary64_bits(value)
    return (~bits & ((1 << 64) - 1)) if bits >> 63 else bits | (1 << 63)


def float_check(left, right):
    """No absolute floor; exact rational relative comparison avoids underflow."""
    out = {"pass": False, "exact": False, "ulp_distance": None,
           "relative": None, "relative_exact": None, "reason": None}
    if type(left) is not float or type(right) is not float:
        out["reason"] = "score_not_binary64_float"
        return out
    out.update(expected_hex=left.hex(), actual_hex=right.hex())
    if not math.isfinite(left) or not math.isfinite(right):
        out["reason"] = "nonfinite_score"
        return out
    exact = binary64_bits(left) == binary64_bits(right)
    ulps = abs(ordered_binary64(left) - ordered_binary64(right))
    magnitude = max(abs(left), abs(right))
    rel = (abs(Fraction.from_float(left) - Fraction.from_float(right))
           / Fraction.from_float(magnitude)) if magnitude else Fraction(0)
    out.update(exact=exact, ulp_distance=ulps, relative=float(rel),
               relative_exact={"numerator": rel.numerator, "denominator": rel.denominator})
    if exact:
        out["pass"] = True
    elif left == 0.0 or right == 0.0:
        out["reason"] = "zero_requires_exact_bits"
    elif (binary64_bits(left) >> 63) != (binary64_bits(right) >> 63):
        out["reason"] = "sign_requires_exact"
    elif ulps > MAX_ULP:
        out["reason"] = "ulp_limit_exceeded"
    elif rel > RELATIVE_LIMIT:
        out["reason"] = "relative_limit_exceeded"
    else:
        out["pass"] = True
    return out


def exact_differences(left, right, pointer=""):
    """Typed values and original sequence order; no matching or normalization."""
    if type(left) is not type(right):
        return [{"pointer": pointer, "kind": "type", "expected": left, "actual": right}]
    differences = []
    if isinstance(left, dict):
        for key in sorted(set(left) | set(right)):
            child = pointer + "/" + str(key).replace("~", "~0").replace("/", "~1")
            if key not in left or key not in right:
                differences.append({"pointer": child, "kind": "key_presence",
                                    "expected_present": key in left, "actual_present": key in right})
            else:
                differences.extend(exact_differences(left[key], right[key], child))
    elif isinstance(left, list):
        if len(left) != len(right):
            differences.append({"pointer": pointer, "kind": "length",
                                "expected": len(left), "actual": len(right)})
        for index, (a, b) in enumerate(zip(left, right)):
            differences.extend(exact_differences(a, b, pointer + "/" + str(index)))
    elif isinstance(left, float):
        if binary64_bits(left) != binary64_bits(right):
            differences.append({"pointer": pointer, "kind": "float_exact", "expected": left,
                                "actual": right, "expected_hex": left.hex(), "actual_hex": right.hex(),
                                "expected_bits": f"{binary64_bits(left):016x}",
                                "actual_bits": f"{binary64_bits(right):016x}"})
    elif left != right:
        differences.append({"pointer": pointer, "kind": "value", "expected": left, "actual": right})
    return differences


def _record_fields(record):
    if type(record) is not dict or set(record) != set(EXACT_FIELDS) | set(EXCLUDED_FIELDS):
        raise ContractError("record_schema_changed")
    if record["method"] != "microrank" or record["variant"] != "full":
        raise ContractError("not_microrank_full")
    if record["mode"] != "a" or record["seed"] is not None or record["hashseed"] != 0:
        raise ContractError("not_main_mode_a_single_seed_hashseed_zero")
    if record["status"] not in KNOWN_STATUS:
        raise ContractError("unknown_status")
    if record["blocks"] is not None:
        raise ContractError("microrank_blocks_must_be_none")
    for name in RANK_FIELDS:
        if type(record[name]) is not list:
            raise ContractError("ranking_field_not_list:" + name)


def _ranking(record, aggregator):
    """Validate a record independently using its own exact native score keys."""
    _record_fields(record)
    ops, order = {}, []
    for index, row in enumerate(record["ranking"]):
        if type(row) is not dict or set(row) != {"item", "entity", "key"}:
            raise ContractError("operation_row_schema_changed")
        op, service, key = row["item"], row["entity"], row["key"]
        if type(op) is not str or type(service) is not str or not op or not service:
            raise ContractError("operation_or_service_not_string")
        if op in ops:
            raise ContractError("duplicate_operation_id:" + op)
        if type(key) is not list or len(key) != 1 or type(key[0]) is not float:
            raise ContractError("operation_score_not_single_float:" + op)
        if not math.isfinite(key[0]):
            raise ContractError("nonfinite_operation_score:" + op)
        ops[op] = {"entity": service, "score": key[0], "index": index}
        order.append(op)
    if exact_differences(order, record["ranking_native"]):
        raise ContractError("ranking_native_not_identical_to_operation_order")
    if any(ops[a]["score"] < ops[b]["score"] for a, b in zip(order, order[1:])):
        raise ContractError("operation_ranking_not_descending_by_own_score")
    expected = aggregator([(op, ops[op]["entity"], [ops[op]["score"]]) for op in order])
    differences = exact_differences(expected, record["entity_ranking"])
    if differences:
        raise ContractError("entity_ranking_not_exact_own_max_aggregation:" + differences[0]["pointer"])
    services = {}
    representatives = {}
    for index, row in enumerate(record["entity_ranking"]):
        if type(row) is not dict or set(row) != {"entity", "key", "tie_group"}:
            raise ContractError("service_row_schema_changed")
        if type(row["tie_group"]) is not int:
            raise ContractError("tie_group_not_int")
        service = row["entity"]
        services[service] = {"score": row["key"][0], "tie_group": row["tie_group"], "index": index}
        representatives[service] = [op for op in order if ops[op]["entity"] == service
                                    and ops[op]["score"] == row["key"][0]]
    sets = record["sets"]
    if (type(sets) is not dict or set(sets) != {"observed", "observed_entities", "returned"}
            or type(sets["observed_entities"]) is not list
            or any(type(s) is not str for s in sets["observed_entities"])
            or sets["observed_entities"] != sorted(set(sets["observed_entities"]))
            or type(sets["observed"]) is not int or type(sets["returned"]) is not int
            or sets["observed"] != len(sets["observed_entities"])
            or sets["returned"] != len(services)
            or not set(services) <= set(sets["observed_entities"])):
        raise ContractError("observed_returned_sets_invalid")
    if record["status"] == "OK" and not order:
        raise ContractError("OK_without_operations")
    if record["status"] != "OK" and (order or services):
        raise ContractError("non_OK_has_rankings")
    return {"operations": ops, "order": order, "services": services,
            "representatives": representatives}


def _numeric_summary(rows):
    finite = [row for row in rows if row["check"]["ulp_distance"] is not None]
    maximum = max((row["check"]["ulp_distance"] for row in finite), default=None)
    relative = max((Fraction(row["check"]["relative_exact"]["numerator"],
                             row["check"]["relative_exact"]["denominator"]) for row in finite),
                   default=Fraction(0))
    return {"status": "COMPUTED" if finite else "NO_MATCHED_SCORE_PAIRS",
            "matched_score_count": len(rows),
            "nonexact_score_count": sum(not row["check"]["exact"] for row in rows),
            "max_ulp_distance": maximum,
            "max_ulp_rows": [{"kind": row["kind"], "identity": row["identity"]} for row in finite
                             if row["check"]["ulp_distance"] == maximum],
            "max_relative": float(relative) if finite else None,
            "max_relative_exact": ({"numerator": relative.numerator, "denominator": relative.denominator}
                                   if finite else None),
            "max_relative_rows": [{"kind": row["kind"], "identity": row["identity"]} for row in finite
                                  if Fraction(row["check"]["relative_exact"]["numerator"],
                                              row["check"]["relative_exact"]["denominator"]) == relative],
            "beyond_threshold_count": sum(not row["check"]["pass"] for row in rows)}


def compare_records(frozen, observed, *, aggregator, evaluator):
    """Pure comparison; an external verified T-028 bridge is still required."""
    reasons = []
    report = {
        "classification": "blocked", "record_contract_pass": False,
        "threshold": {"max_ulp_distance": MAX_ULP, "relative_numerator": 16,
                      "relative_denominator": 1 << 52, "combination": "AND",
                      "absolute_floor": None, "zero_and_sign": "exact"},
        "excluded_fields": {"run_id": "new execution identifier", "cost": "new measured cost"},
        "raw_exact_differences": [], "outside_whitelist_differences": [],
        "score_checks": [], "operation_inversions": [], "representatives": {},
        "numeric_summary": _numeric_summary([]),
        "hit_metrics": {"pass": False, "entities": [], "differences": []},
        "t028_flags": {"status": "NOT_PERFORMED", "pass": None,
                      "required": ["M1-M6", "M0/primary/multi", "wrong_OK", "P0", "N/A/reason"],
                      "k": [1, 5],
                      "reason": "pure_record_comparator_has_no_verified_T028_graph_feature_row_bridge"},
        "native_observed_exact": {"status": "NOT_PROVIDED", "pass": None},
        "source_verification": "pure_API_caller_must_verify_records_and_injected_source_functions",
        "API_record_bindings": {
            "encoding": "canonical JSON digest for object binding only; not a replacement record",
            "frozen": _object_digest(frozen), "observed": _object_digest(observed)},
        "intermediates_eligible": False, "cohort_ready": False, "blocked_reasons": reasons,
        "limits": ["No frozen historical abnormal masks/trace memberships are reconstructed.",
                   "Output roundoff equivalence does not identify the cause of drift.",
                   "Record-contract PASS does not certify T-028 flags or cohort/A-prime eligibility."],
    }
    if type(frozen) is dict and type(observed) is dict:
        report["raw_exact_differences"] = exact_differences(
            {k: v for k, v in frozen.items() if k not in EXCLUDED_FIELDS},
            {k: v for k, v in observed.items() if k not in EXCLUDED_FIELDS})
    try:
        _record_fields(frozen)
        _record_fields(observed)
        metadata = [field for field in EXACT_FIELDS if field not in RANK_FIELDS]
        outside = exact_differences({k: frozen[k] for k in metadata}, {k: observed[k] for k in metadata})
        report["outside_whitelist_differences"] = outside
        if outside:
            reasons.append("metadata_outside_whitelist_changed")
        a, b = _ranking(frozen, aggregator), _ranking(observed, aggregator)
        report["aggregation"] = {"frozen_selfconsistent": True, "observed_selfconsistent": True,
                                 "function": "verified src/p3/ban_ghi.py::xep_thuc_the",
                                 "comparison": "exact own-output aggregation"}
        report["representatives"] = {
            service: {"frozen": a["representatives"].get(service),
                      "observed": b["representatives"].get(service),
                      "changed": a["representatives"].get(service) != b["representatives"].get(service)}
            for service in sorted(set(a["services"]) | set(b["services"]))}
        if set(a["operations"]) != set(b["operations"]):
            reasons.append("operation_set_changed")
        shared = sorted(set(a["operations"]) & set(b["operations"]))
        mapping_changed = [op for op in shared if a["operations"][op]["entity"] != b["operations"][op]["entity"]]
        report["operation_mapping"] = {"source": "explicit ranking item/entity pairs; ID is never parsed",
                                       "exact": set(a["operations"]) == set(b["operations"]) and not mapping_changed,
                                       "changed_ids": mapping_changed}
        if mapping_changed:
            reasons.append("operation_service_mapping_changed")
        same_service_order = ([r["entity"] for r in frozen["entity_ranking"]]
                              == [r["entity"] for r in observed["entity_ranking"]])
        tie_a = [(r["entity"], r["tie_group"]) for r in frozen["entity_ranking"]]
        tie_b = [(r["entity"], r["tie_group"]) for r in observed["entity_ranking"]]
        report["service_order_exact"] = same_service_order
        report["service_tie_partition_exact"] = tie_a == tie_b
        if not same_service_order:
            reasons.append("service_order_changed")
        if tie_a != tie_b:
            reasons.append("service_tie_partition_changed")
        for kind, left, right in (("operation", a["operations"], b["operations"]),
                                  ("service", a["services"], b["services"])):
            for identity in sorted(set(left) & set(right)):
                check = float_check(left[identity]["score"], right[identity]["score"])
                report["score_checks"].append({"kind": kind, "identity": identity, "check": check})
                if not check["pass"]:
                    reasons.append(kind + "_score_outside_contract:" + identity + ":" + str(check["reason"]))
        report["numeric_summary"] = _numeric_summary(report["score_checks"])
        if set(a["operations"]) == set(b["operations"]):
            for i, op in enumerate(a["order"]):
                for later in a["order"][i + 1:]:
                    if b["operations"][op]["index"] > b["operations"][later]["index"]:
                        same = (a["operations"][op]["entity"] == a["operations"][later]["entity"]
                                == b["operations"][op]["entity"] == b["operations"][later]["entity"])
                        near_a = float_check(a["operations"][op]["score"], a["operations"][later]["score"])
                        near_b = float_check(b["operations"][op]["score"], b["operations"][later]["score"])
                        passed = same and near_a["pass"] and near_b["pass"]
                        report["operation_inversions"].append(
                            {"first": op, "second": later, "same_service": same,
                             "frozen_pair_check": near_a, "observed_pair_check": near_b, "pass": passed})
                        if not passed:
                            reasons.append("operation_inversion_outside_contract:" + op + ":" + later)
        entities = sorted(set(frozen["sets"]["observed_entities"]) | set(observed["sets"]["observed_entities"])
                          | set(a["services"]) | set(b["services"]))
        hit_rows = []
        for service in entities:
            metrics_a, metrics_b = evaluator(frozen, service), evaluator(observed, service)
            diff = exact_differences(metrics_a, metrics_b)
            hit_rows.append({"entity": service, "frozen": metrics_a, "observed": metrics_b,
                             "exact": not diff, "differences": diff})
        report["hit_metrics"] = {"pass": all(row["exact"] for row in hit_rows), "entities": hit_rows,
                                "scope": "old cham_ca, every observed/returned service; all metrics including Hit@1..10",
                                "labels_read": False}
        if not report["hit_metrics"]["pass"]:
            reasons.append("old_evaluator_metrics_changed")
        report["record_contract_pass"] = not reasons
        if not same_service_order:
            report["classification"] = "service_order_changed"
        elif reasons:
            report["classification"] = "blocked"
        elif not report["raw_exact_differences"]:
            report["classification"] = "exact"
        elif report["operation_inversions"]:
            report["classification"] = "operation_order"
        else:
            report["classification"] = "numeric_only"
    except (ContractError, ValueError, TypeError, KeyError, OverflowError, ArithmeticError) as error:
        reasons.append(str(error))
    report["missing_eligibility_checks"] = [
        "verified T-028 graph/features/rows bridge and exact flags/P0 at k=1,5",
        "native-observed exact comparison if not supplied",
        "current run source/capture/selfconsistency checks outside a record comparator",
        "WHY approval before using results in a report",
    ]
    return report


def _sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _read(path):
    def invalid(token):
        raise ContractError("nonfinite_JSON_token:" + token)
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), parse_constant=invalid)


def _safe_child(root, relative):
    if type(relative) is not str or "\\" in relative:
        raise ContractError("invalid_relative_source_path")
    p = PurePosixPath(relative)
    if (p.is_absolute() or re.match(r"^[A-Za-z]:", relative)
            or any(x in (".", "..") for x in p.parts)
            or any(x.lower() in ("t-033", "locked", "test", "tests", "heldout", "archive") for x in p.parts)
            or "flash-ticket-rca-research" in relative.lower()):
        raise ContractError("source_path_outside_scope")
    resolved = (root / Path(*p.parts)).resolve()
    if root.resolve() not in resolved.parents:
        raise ContractError("source_path_escaped_root")
    return resolved


def _verify(path, expected, authority, audit, expected_bytes=None):
    if type(expected) is not str or not re.fullmatch("[0-9a-f]{64}", expected):
        raise ContractError("invalid_expected_sha256")
    actual = _sha(path)
    size = Path(path).stat().st_size
    passed = actual == expected and (expected_bytes is None or size == expected_bytes)
    audit.append({"path": str(path), "authority": authority, "expected": expected, "actual": actual,
                  "bytes": size, "pass": passed})
    if not passed:
        raise ContractError("source_hash_or_size_mismatch:" + str(path))
    return Path(path)


def verified_helpers(audit):
    _verify(PACKAGE, PACKAGE_SHA256, "T-032 frozen package anchor", audit)
    package = _read(PACKAGE)
    entries = {row["path"]: row for row in package["files"]}
    if len(entries) != len(package["files"]):
        raise ContractError("duplicate_package_paths")
    modules = []
    for name, relative in (("t032_frozen_ban_ghi", "src/p3/ban_ghi.py"),
                           ("t032_frozen_danh_gia", "src/p3/danh_gia.py")):
        entry = entries[relative]
        path = _verify(_safe_child(REPO, relative), entry["sha256"], "package#/files", audit)
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _verify(path, entry["sha256"], "source after import", audit)
        modules.append(module)
    return entries, modules[0].xep_thuc_the, modules[1].cham_ca


def frozen_record(dataset, opaque_id, entries, audit):
    if dataset not in ("RE2-TT", "Nezha-OB"):
        raise ContractError("dataset_outside_approved_main_cohorts")
    if not re.fullmatch(r"dev-[0-9a-f]{10}", opaque_id):
        raise ContractError("invalid_opaque_dev_id")
    relative = INDEX24 if dataset == "RE2-TT" else INDEX26
    meta = entries[relative]
    index = _read(_verify(_safe_child(REPO, relative), meta["sha256"], "package#/files", audit))
    if dataset == "RE2-TT":
        found = [entry for entry in index["records"] if entry["method"] == "microrank"
                 and entry["variant"] == "full" and entry["opaque_id"] == opaque_id]
    else:
        found = [entry for entry in index["unique_records"] if entry["worker_method"] == "microrank"
                 and entry["source_view"] == "main" and entry["opaque_id"] == opaque_id]
    if len(found) != 1:
        raise ContractError("frozen_main_full_source_not_unique")
    entry = found[0]
    source = _verify(_safe_child(REPO, entry["path"]), entry["sha256"], relative + "#/records", audit)
    if entry["path"] in entries and entries[entry["path"]]["sha256"] != entry["sha256"]:
        raise ContractError("package_index_record_hash_disagreement")
    record = _read(source)
    if (record["opaque_id"] != opaque_id or record["mode"] != "a" or record["seed"] is not None
            or record["hashseed"] != 0):
        raise ContractError("frozen_record_outside_main_full_h0")
    if dataset == "RE2-TT":
        config = _read(_verify(_safe_child(REPO, entry["source_config"]),
                              entry["source_config_sha256"], relative + "#/source_config", audit))
        code_hashes = config["src_p3"]["tep"]
    else:
        code_hashes = index["source_hashes"]
    for relative in ("src/p3/ban_ghi.py", "src/p3/danh_gia.py"):
        if code_hashes[relative] != entries[relative]["sha256"]:
            raise ContractError("frozen_source_helper_revision_disagrees:" + relative)
    return record, entry


def verified_run(raw_directory, check_sha256, audit):
    directory = Path(raw_directory).expanduser().resolve()
    if BASE.resolve() / "runs" not in directory.parents:
        raise ContractError("run_outside_T032_runs")
    if any(x.lower() in ("t-033", "locked", "test", "heldout", "archive") for x in directory.parts):
        raise ContractError("run_path_outside_scope")
    check_path = _verify(directory / "check.json", check_sha256, "caller trusted run-check hash", audit)
    check = _read(check_path)
    artifacts = check.get("artifact_manifest")
    if type(artifacts) is not list:
        raise ContractError("run_check_has_no_artifact_manifest")
    seen = set()
    for entry in artifacts:
        if entry["path"] in seen:
            raise ContractError("duplicate_run_artifact_path")
        seen.add(entry["path"])
        _verify(_safe_child(directory, entry["path"]), entry["sha256"],
                str(check_path) + "#/artifact_manifest", audit, entry["bytes"])
    if not {"ban-ghi-0.json", "source.json"} <= seen:
        raise ContractError("run_check_does_not_authenticate_record_and_source")
    record = _read(directory / "ban-ghi-0.json")
    source = _read(directory / "source.json")
    # The original observed replay kept its audit in an authenticated sidecar;
    # the native-only diagnostic kept the same audit inline in source.json.
    checks = source.get("source_checks")
    if checks is None and "source-checks.json" in seen:
        checks = _read(directory / "source-checks.json").get("checks")
    if not checks or any(row.get("pass") is not True for row in checks):
        raise ContractError("run_source_checks_missing_or_failed")
    return record, source, check


def verify_actual_imports(source, check, entries, audit):
    initial = source.get("actual_imports")
    if type(initial) is not list or not initial:
        raise ContractError("actual_imports_missing_from_run_source")
    lists = [initial]
    if "actual_imports_after" in check:
        if type(check["actual_imports_after"]) is not list:
            raise ContractError("actual_imports_after_not_list")
        lists.append(check["actual_imports_after"])
    for imports in lists:
        for row in imports:
            relative = row.get("path")
            if (relative not in entries or row.get("sha256") != entries[relative]["sha256"]
                    or not relative.startswith(("src/p3/", "src/microrank/"))):
                raise ContractError("actual_import_not_same_frozen_source:" + str(relative))
            _verify(_safe_child(REPO, relative), row["sha256"], "authenticated run actual imports", audit)


def compare_case(dataset, opaque_id, replay_run, replay_check_sha256, *,
                 native_run=None, native_check_sha256=None, source_audit=None):
    audit = source_audit if source_audit is not None else []
    entries, aggregator, evaluator = verified_helpers(audit)
    frozen, entry = frozen_record(dataset, opaque_id, entries, audit)
    observed, source, observed_check = verified_run(replay_run, replay_check_sha256, audit)
    verify_actual_imports(source, observed_check, entries, audit)
    report = compare_records(frozen, observed, aggregator=aggregator, evaluator=evaluator)
    report.update(dataset=dataset, opaque_id=opaque_id, frozen_entry=entry,
                  source_checks=audit, source_verification="CLI/package/index/run-artifact hashes verified",
                  script_sha256=_sha(__file__),
                  observed_original_check_status=observed_check.get("status"),
                  record_bindings={
                      "frozen": {"path": entry["path"], "sha256": entry["sha256"]},
                      "observed": {"path": str(Path(replay_run).expanduser().resolve() / "ban-ghi-0.json"),
                                   "sha256": _sha(Path(replay_run).expanduser().resolve() / "ban-ghi-0.json"),
                                   "trusted_check_sha256": replay_check_sha256}})
    source_entry = source.get("entry", source.get("frozen_entry"))
    if (source_entry is None or source_entry.get("path") != entry["path"]
            or source_entry.get("sha256") != entry["sha256"]):
        report["blocked_reasons"].append("observed_source_reference_disagrees_with_frozen")
        report["record_contract_pass"] = False
        report["classification"] = "blocked"
    if native_run is not None:
        if native_check_sha256 is None:
            raise ContractError("native_run_requires_trusted_check_sha256")
        native, native_source, native_check = verified_run(native_run, native_check_sha256, audit)
        verify_actual_imports(native_source, native_check, entries, audit)
        _record_fields(native)
        report["record_bindings"]["native"] = {
            "path": str(Path(native_run).expanduser().resolve() / "ban-ghi-0.json"),
            "sha256": _sha(Path(native_run).expanduser().resolve() / "ban-ghi-0.json"),
            "trusted_check_sha256": native_check_sha256}
        differences = exact_differences({k: observed[k] for k in EXACT_FIELDS},
                                        {k: native[k] for k in EXACT_FIELDS})
        report["native_observed_exact"] = {"status": "PASS" if not differences else "FAIL",
                                           "pass": not differences, "differences": differences,
                                           "tolerance_used": False}
        native_entry = native_source.get("entry", native_source.get("frozen_entry"))
        if (native_entry is None or native_entry.get("path") != entry["path"]
                or native_entry.get("sha256") != entry["sha256"]):
            report["blocked_reasons"].append("native_source_reference_disagrees_with_frozen")
        if native_source.get("observer_attached") is not False:
            report["blocked_reasons"].append("native_source_does_not_declare_observer_absent")
        if differences:
            report["blocked_reasons"].append("native_observed_not_exact")
        if report["blocked_reasons"]:
            report["record_contract_pass"] = False
            report["classification"] = "blocked"
    return report


def _fixture_record(items, aggregator, status="OK"):
    ranking = [{"item": op, "entity": service, "key": [float(score)]} for op, service, score in items]
    order = [row["item"] for row in ranking]
    top = order[:11]
    mapping = {row["item"]: row["entity"] for row in ranking}
    observed = sorted(set(mapping.values()))
    return {
        "run_id": "synthetic", "opaque_id": "dev-0000000000", "method": "microrank",
        "method_version": "synthetic", "variant": "full", "mode": "a", "detector": None,
        "detector_columns": None, "seed": None, "hashseed": 0, "config_id": "synthetic",
        "why_ids": [], "window": {"t": 1.0}, "input_shape": {}, "status": status,
        "method_status_raw": "ok" if status == "OK" else "synthetic_error", "error": None,
        "ranking_native": order, "ranking": ranking,
        "entity_ranking": aggregator([(row["item"], row["entity"], row["key"]) for row in ranking]),
        "blocks": None, "sets": {"observed": len(observed), "observed_entities": observed,
                                "returned": len(set(mapping.values()))},
        "diagnostics": {"counts": {"normal": 2, "anomaly": 2}},
        "extra": {"top11_ranks": top, "service_ranks_top11": list(dict.fromkeys(mapping[op] for op in top))},
        "cost": {}, "input_sha256": {},
    }


def _fixture_replace(record, scores, aggregator):
    changed = copy.deepcopy(record)
    for row in changed["ranking"]:
        if row["item"] in scores:
            row["key"] = [float(scores[row["item"]])]
    changed["ranking"].sort(key=lambda row: row["key"][0], reverse=True)
    changed["ranking_native"] = [row["item"] for row in changed["ranking"]]
    changed["entity_ranking"] = aggregator([(row["item"], row["entity"], row["key"])
                                          for row in changed["ranking"]])
    top = changed["ranking_native"][:11]
    mapping = {row["item"]: row["entity"] for row in changed["ranking"]}
    changed["extra"] = {"top11_ranks": top,
                        "service_ranks_top11": list(dict.fromkeys(mapping[op] for op in top))}
    return changed


def fixture_report(aggregator, evaluator):
    cases = []
    def check(name, a, b, expected, reason=None):
        before_a, before_b = copy.deepcopy(a), copy.deepcopy(b)
        result = compare_records(a, b, aggregator=aggregator, evaluator=evaluator)
        unchanged = not exact_differences(before_a, a) and not exact_differences(before_b, b)
        passed = result["record_contract_pass"] is expected and unchanged
        if reason is not None:
            passed = passed and any(reason in value for value in result["blocked_reasons"])
        cases.append({"name": name, "pass": passed, "expected_contract_pass": expected,
                      "inputs_unchanged": unchanged, "report": result})
    one = _fixture_record([("opaque op!", "service A", 1.0), ("other opaque", "service B", 0.5)], aggregator)
    check("exact_and_direct_mapping_without_parsing_ID", one, copy.deepcopy(one), True)
    up16 = struct.unpack(">d", struct.pack(">Q", binary64_bits(1.0) + 16))[0]
    up17 = struct.unpack(">d", struct.pack(">Q", binary64_bits(1.0) + 17))[0]
    check("16_ULP_boundary", one, _fixture_replace(one, {"opaque op!": up16}, aggregator), True)
    check("17_ULP_rejected", one, _fixture_replace(one, {"opaque op!": up17}, aggregator),
          False, "ulp_limit_exceeded")
    small = _fixture_record([("tiny", "tiny service", 1e-280)], aggregator)
    check("near_zero_normal_one_ULP", small,
          _fixture_replace(small, {"tiny": math.nextafter(1e-280, math.inf)}, aggregator), True)
    zero = _fixture_record([("zero", "zero service", 0.0)], aggregator)
    check("zero_to_smallest_subnormal_no_absolute_floor", zero,
          _fixture_replace(zero, {"zero": math.ulp(0.0)}, aggregator), False, "zero_requires_exact_bits")
    check("signed_zero_changed", zero, _fixture_replace(zero, {"zero": -0.0}, aggregator),
          False, "zero_requires_exact_bits")
    subnormal = _fixture_record([("sub", "sub service", math.ulp(0.0))], aggregator)
    check("adjacent_subnormal_relative_limit", subnormal,
          _fixture_replace(subnormal, {"sub": 2 * math.ulp(0.0)}, aggregator),
          False, "relative_limit_exceeded")
    check("opposite_nonzero_sign", subnormal,
          _fixture_replace(subnormal, {"sub": -math.ulp(0.0)}, aggregator),
          False, "sign_requires_exact")
    for value, label in ((math.inf, "positive_inf"), (-math.inf, "negative_inf"), (math.nan, "NaN")):
        changed = copy.deepcopy(one)
        changed["ranking"][0]["key"][0] = value
        check("nonfinite_" + label, one, changed, False, "nonfinite_operation_score")
    close = math.nextafter(1.0, math.inf)
    padding = [(f"high opaque {i}", "padding service", float(30 - i)) for i in range(11)]
    inverted = _fixture_record(padding + [("second opaque", "same service", close),
                                         ("first opaque", "same service", 1.0),
                                         ("low opaque", "last service", 0.5)], aggregator)
    swapped = _fixture_replace(inverted, {"second opaque": 1.0, "first opaque": close}, aggregator)
    check("same_service_inversion_below_top11_and_representative_change", inverted, swapped, True)
    cross = _fixture_record(padding + [("cross a", "service X", close), ("cross b", "service Y", 1.0)], aggregator)
    check("cross_service_near_inversion", cross,
          _fixture_replace(cross, {"cross a": 1.0, "cross b": close}, aggregator),
          False, "operation_inversion_outside_contract")
    far = _fixture_record(padding + [("far a", "same service", 2.0), ("far b", "same service", 1.0)], aggregator)
    check("same_service_far_inversion", far,
          _fixture_replace(far, {"far a": 1.0, "far b": 2.0}, aggregator),
          False, "operation_inversion_outside_contract")
    tied = _fixture_record([("tie a", "service A", 1.0), ("tie b", "service B", 1.0)], aggregator)
    check("service_exact_tie_partition_changed", tied,
          _fixture_replace(tied, {"tie a": close}, aggregator), False, "service_tie_partition_changed")
    check("service_order_changed", cross,
          _fixture_replace(cross, {"cross a": 1.0, "cross b": close}, aggregator),
          False, "service_order_changed")
    metadata = copy.deepcopy(one)
    metadata["diagnostics"]["counts"]["anomaly"] += 1
    check("metadata_counts_changed", one, metadata, False, "metadata_outside_whitelist_changed")
    mapping = copy.deepcopy(one)
    mapping["ranking"][0]["entity"] = "service B"
    mapping["entity_ranking"] = aggregator([(row["item"], row["entity"], row["key"]) for row in mapping["ranking"]])
    mapping["sets"]["returned"] = len(mapping["entity_ranking"])
    check("direct_operation_service_mapping_changed", one, mapping,
          False, "operation_service_mapping_changed")
    wrong_aggregate = copy.deepcopy(one)
    wrong_aggregate["entity_ranking"][0]["key"][0] = close
    check("one_ULP_tampered_own_aggregation", one, wrong_aggregate,
          False, "entity_ranking_not_exact_own_max_aggregation")
    top_swap = _fixture_record([("top a", "same service", close), ("top b", "same service", 1.0)], aggregator)
    check("same_service_top11_extra_is_still_exact", top_swap,
          _fixture_replace(top_swap, {"top a": 1.0, "top b": close}, aggregator),
          False, "metadata_outside_whitelist_changed")
    schema = copy.deepcopy(one)
    schema["unreviewed_field"] = 1
    check("unknown_record_field_rejected", one, schema, False, "record_schema_changed")
    error = _fixture_record([], aggregator, status="ERROR")
    check("exact_ERROR_preserved_not_skipped", error, copy.deepcopy(error), True)
    return {"status": "PASS" if all(case["pass"] for case in cases) else "FAIL",
            "fixture_count": len(cases), "fixtures": cases,
            "methods_executed": False, "raw_data_read": False,
            "cohort_ready": False, "intermediates_eligible": False}


def _json_safe(value):
    """Tag invalid synthetic float values only in output JSON, never in inputs."""
    if isinstance(value, float) and not math.isfinite(value):
        return {"__nonfinite__": value.hex(), "__binary64_bits__": f"{binary64_bits(value):016x}"}
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def _object_digest(value):
    # Binding makes the root's external flag bridge refer to the exact objects
    # compared here. This does not substitute for byte hashes or source checks.
    encoded = json.dumps(_json_safe(value), sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _write(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as destination:
        json.dump(_json_safe(value), destination, ensure_ascii=False, indent=2, allow_nan=False)
        destination.write("\n")


def _guard_output(raw):
    if (sys.platform != "linux" or Path.home().resolve() != Path("/home/ubuntu")
            or Path(__file__).resolve().parent != BASE / "scripts"):
        raise ContractError("EC2_only_from_approved_T032_script_location")
    output = Path(raw).expanduser().resolve()
    if output.parent != BASE / "runs" or not output.name or output.exists():
        raise ContractError("output_must_be_new_direct_child_of_T032_runs")
    output.mkdir(exist_ok=False)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    fixture = commands.add_parser("fixture")
    fixture.add_argument("--out", required=True)
    one = commands.add_parser("one")
    one.add_argument("--dataset", required=True, choices=("RE2-TT", "Nezha-OB"))
    one.add_argument("--opaque-id", required=True)
    one.add_argument("--replay-run", required=True)
    one.add_argument("--replay-check-sha256", required=True)
    one.add_argument("--native-run")
    one.add_argument("--native-check-sha256")
    one.add_argument("--out", required=True)
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    output = _guard_output(args.out)
    audit = []
    started = datetime.now(timezone.utc).isoformat()
    try:
        if args.command == "fixture":
            _, aggregator, evaluator = verified_helpers(audit)
            result = fixture_report(aggregator, evaluator)
            result.update(source_checks=audit, script_sha256=_sha(__file__))
            passed = result["status"] == "PASS"
        else:
            result = compare_case(args.dataset, args.opaque_id, args.replay_run,
                                  args.replay_check_sha256, native_run=args.native_run,
                                  native_check_sha256=args.native_check_sha256, source_audit=audit)
            result["status"] = "RECORD_CONTRACT_PASS" if result["record_contract_pass"] else "FAIL_STOP"
            passed = result["record_contract_pass"]
        result.update(started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
                      methods_executed=False, tolerance_options_available=False)
        _write(output / "comparison.json", result)
        _write(output / "manifest.json", {"files": [{"path": "comparison.json",
                                                    "sha256": _sha(output / "comparison.json"),
                                                    "bytes": (output / "comparison.json").stat().st_size}],
                                         "script_sha256": _sha(__file__)})
        print(json.dumps({"status": result["status"], "classification": result.get("classification"),
                          "cohort_ready": False, "output": str(output)}, ensure_ascii=False), flush=True)
        return 0 if passed else 1
    except BaseException as error:
        _write(output / "failure.json", {"status": "FAIL_STOP", "error": str(error),
                                         "traceback": traceback.format_exc(), "source_checks": audit,
                                         "script_sha256": _sha(__file__), "cohort_ready": False,
                                         "started_at": started})
        raise


if __name__ == "__main__":
    sys.exit(main())
