"""T-032: lock the frozen group catalogue, not an unverified manual sample.

Run only on EC2. This reads source metadata/results, never raw data. All seeds
remain separate until replay establishes their intermediate processing paths.
No nearest-neighbour distance, coverage threshold, or matching tolerance is
invented here. Non-equivalent candidate pairs remain selection_pending.
"""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import time
import traceback

sys.dont_write_bytecode = True
BASE = Path.home() / "rca/T-032"
T28 = "results/T-028/runs/phan-hoi-review-001"
FLAGS = ("M1", "M2", "M3", "M4", "M5", "M6", "M0")
METHODS = {
    "baro": "baro", "simplerca": "simplerca", "microrank_full": "microrank",
    "tracerca": "tracerca", "circa_ols_da": "circa", "torai_B": "torai",
}
SOURCE_TASKS = {"T-022", "T-024", "T-026", "T-028", "T-029", "T-031"}


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def parse(path):
    return json.loads(path.read_text(encoding="utf-8-sig"),
                      object_pairs_hook=unique_object)


def reference(path, pointer=""):
    return {"path": path, "json_pointer": pointer}


def flatten(value, prefix=""):
    """Metadata differences only; no distance/ranking across unequal values."""
    if isinstance(value, dict):
        output = {}
        for key, child in sorted(value.items()):
            output.update(flatten(child, prefix + "/" + key))
        return output
    return {prefix: value}


def differences(left, right):
    a, b = flatten(left), flatten(right)
    missing = {"availability": "field_absent"}
    return [{"field": key, "wrong": a.get(key, missing),
             "correct": b.get(key, missing)}
            for key in sorted(a.keys() | b.keys()) if a.get(key, missing) != b.get(key, missing)]


def compact_shape(shape):
    """Keep counts and exact column-set fingerprints, not ranking values."""
    output = {}
    for key, value in shape.items():
        if isinstance(value, list):
            output[key] = {"length": len(value), "ordered_values_sha256":
                           hashlib.sha256(canonical(value).encode()).hexdigest()}
        elif isinstance(value, dict):
            output[key] = compact_shape(value)
        else:
            output[key] = value
    return output


def window_condition(record):
    window = record["window"]
    if "t_ns" in window:
        t, nk, ak, unit = window["t_ns"], "N_ns", "A_ns", "ns"
    elif "t" in window:
        t, nk, ak, unit = window["t"], "N", "A", "s"
    else:
        return {"availability": "missing_window_origin", "window": window}
    return {"availability": "recorded", "unit": unit,
            "N_offsets": [x - t for x in window[nk]],
            "A_offsets": [x - t for x in window[ak]],
            "trace_guard_s": window.get("trace_guard_s", 0),
            "mode": record.get("mode"), "config_id": record.get("config_id")}


def feature_metadata(feature):
    aggregate = feature["aggregate"]
    graph_fields = ("availability", "reason", "input_rows_N", "unique_effective_spans_N",
                    "duplicate_rows_outer", "duplicate_rows_N", "conflict_keys_outer",
                    "conflict_keys_with_N", "orphan_rows", "missing_parent_rows",
                    "unresolved_parent_rows", "edges_to_conflicts_removed")
    coverage = {}
    for split in ("start", "end"):
        graph = aggregate.get("graph_" + split, {})
        coverage["graph_" + split] = {k: graph[k] for k in graph_fields if k in graph}
    # Preserve availability/counts from saved per-channel observations. Neither
    # signal strength, abnormality, caller relations, nor ranks enter matching.
    coverage["metrics"] = {column: {k: values[k] for k in
                           ("nN", "nA", "missing_N", "missing_A", "availability", "reason")
                           if k in values}
                           for column, values in aggregate.get("metrics", {}).items()}
    sources = aggregate.get("provenance", {}).get("sources", {})
    return {
        "raw_channels_recorded": sorted(sources),
        "window_counts": {k: v for k, v in aggregate.get("window", {}).items()
                          if "rows" in k or "spans" in k},
        "coverage": coverage,
        "source": reference("", "/aggregate"),
        "coverage_limit": "Saved observations only; no threshold or physical-wait semantics established.",
    }


class Reader:
    def __init__(self, root, package):
        self.root = root
        self.inputs = []
        self.verified = {}
        self.package = {x["path"]: x["sha256"] for x in parse(package)["files"]}
        self.inputs.append({"path": str(package), "sha256": sha(package),
                            "provenance": "authorized transferred package inventory"})

    def path(self, name):
        relative = PurePosixPath(name)
        if (relative.is_absolute() or ".." in relative.parts or "\\" in name or
                len(relative.parts) < 3 or relative.parts[0] != "results" or
                relative.parts[1] not in SOURCE_TASKS or relative.suffix != ".json"):
            raise ValueError("outside source-result metadata scope: " + name)
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("source escaped root: " + name)
        return path

    def read(self, name, expected=None, provenance="package-manifest.json#/files"):
        path = self.path(name)
        wanted = expected or self.package.get(name)
        if wanted is None:
            raise ValueError("no frozen hash for " + name)
        actual = self.verified.get(name)
        if actual is None:
            actual = sha(path)
            self.verified[name] = actual
            self.inputs.append({"path": name, "sha256": actual, "expected": wanted,
                                "bytes": path.stat().st_size, "provenance": provenance})
        if actual != wanted:
            raise ValueError("frozen source hash mismatch: " + name)
        return parse(path)


def prepare(reader):
    manifest_name = T28 + "/manifest.json"
    manifest = reader.read(manifest_name)
    outputs = {x["path"]: x["sha256"] for x in manifest["outputs"]}
    cases_name, summary_name = T28 + "/ca-sai.json", T28 + "/summary-tables.json"
    cases = reader.read(cases_name, outputs[cases_name], manifest_name + "#/outputs")
    summary = reader.read(summary_name, outputs[summary_name], manifest_name + "#/outputs")
    features_name = T28 + "/features-no-label-index.json"
    features = reader.read(features_name, outputs[features_name], manifest_name + "#/outputs")
    index24_name = "results/T-024/ban-ghi-dua-vao-cham.json"
    index26_name = "results/T-026/ban-ghi-dua-vao-cham.json"
    comparison_name = "results/T-029/runs/compare-rca-preparation-001/manifest.json"
    comparison = reader.read(comparison_name)
    index24 = reader.read(index24_name, comparison["source_hashes"][index24_name],
                          comparison_name + "#/source_hashes")
    index26 = reader.read(index26_name)
    record_refs = {x["path"]: x for x in index24["records"] + index26["tables"]["main"]["records"]}
    units, feature_cache, config_cache = {}, {}, {}
    config_by_row = {}
    for ri, row in enumerate(cases["main_rows"]):
        ds, method, oid = row["dataset"], row["method"], row["opaque_id"]
        if ds not in ("RE2-TT", "Nezha-OB") or method not in METHODS:
            raise ValueError("unexpected main dataset/method")
        feature_ref = features["cases"][ds][oid]
        feature_name = feature_ref["path"]
        if feature_name != row["evidence"]["source"]["path"]:
            raise ValueError("feature source mismatch")
        if feature_name not in feature_cache:
            feature = reader.read(feature_name, feature_ref["sha256"], features_name + "#/cases")
            feature_cache[feature_name] = feature_metadata(feature)
            feature_cache[feature_name]["source"]["path"] = feature_name
        row_ref_hashes = {x["path"]: x["sha256"] for x in row["source"]["records"]}
        row_configs = set()
        for sid, seed in row["evidence"]["seed_evidence"].items():
            source = seed["source"]["path"]
            ref = record_refs[source]
            if ref["sha256"] != row_ref_hashes[source]:
                raise ValueError("frozen record indices disagree: " + source)
            record = reader.read(source, ref["sha256"], cases_name + f"#/main_rows/{ri}/source/records")
            expected_sid = "single" if record["seed"] is None else str(record["seed"])
            if (sid != expected_sid or record["opaque_id"] != oid or record["status"] != seed["status"] or
                    record["method"] != METHODS[method]):
                raise ValueError("seed identity mismatch: " + source)
            if ds == "RE2-TT":
                cfgname = ref["source_config"]
                if cfgname not in config_cache:
                    config_cache[cfgname] = reader.read(cfgname, ref["source_config_sha256"], index24_name + "#/records")
                source_code = config_cache[cfgname]["src_p3"]["tep"]
                adapter = {"entry": "src/p3/worker.py", "entry_sha256": source_code["src/p3/worker.py"],
                           "method_adapter": "src/p3/adapters/" + record["method"] + ".py",
                           "method_adapter_sha256": source_code["src/p3/adapters/" + record["method"] + ".py"]}
            else:
                source_code = index26["source_hashes"]
                adapter = {"entry": "src/p3/nezha_worker.py", "entry_sha256": source_code["src/p3/nezha_worker.py"],
                           "method_adapter": "src/p3/adapters/nezha.py",
                           "method_adapter_sha256": source_code["src/p3/adapters/nezha.py"],
                           "adapter_config_sha256": source_code["results/T-026/config/adapter-config.json"]}
            configuration = {k: record.get(k) for k in ("method", "variant", "config_id", "method_version", "hashseed")}
            config_key = canonical(configuration)
            row_configs.add(config_key)
            uid = "|".join((ds, method, oid, "seed=" + sid))
            if uid in units:
                raise ValueError("duplicate unit: " + uid)
            features_meta = feature_cache[feature_name]
            units[uid] = {
                "unit_id": uid, "dataset": ds, "method": method, "opaque_id": oid,
                "seed": record["seed"], "seed_key": sid, "configuration": configuration,
                "source": reference(source), "source_row": reference(cases_name, f"/main_rows/{ri}"),
                "source_seed": reference(cases_name, f"/main_rows/{ri}/evidence/seed_evidence/{sid}"),
                "status": seed["status"], "cell": row["cell"], "groups": [],
                "by_k": {k: {"wrong_OK": v["wrong_OK"], "assignment": v["assignment"]}
                         for k, v in seed["by_k"].items()},
                "mandatory_conditions": {"dataset": ds, "configuration": configuration,
                                         "F": window_condition(record), "adapter": adapter},
                "preferred_conditions": {
                    "cell": row["cell"], "raw_channels_recorded": features_meta["raw_channels_recorded"],
                    "native_input_shape": compact_shape(record["input_shape"]),
                    "window_counts": features_meta["window_counts"],
                    "coverage": features_meta["coverage"]},
                "condition_source": features_meta["source"],
                "processing_path": {"status": "OPEN", "saved_status": record["status"],
                                    "error": record.get("error"),
                                    "saved_diagnostics": reference(source, "/diagnostics"),
                                    "saved_extra": reference(source, "/extra"),
                                    "missing": "Replay intermediate path, fallback/branch audit, and exact match verification."},
                "selected_for_manual_reading": False,
                "seed_merge_status": "kept_separate_until_intermediate_equivalence_is_verified",
            }
        if len(row_configs) != 1:
            raise ValueError("main row contains more than one configuration; needs explicit catalogue split: " + oid)
        config_by_row[ri] = json.loads(next(iter(row_configs)))
    return cases, summary, units, config_by_row


def catalogue(cases, summary, units, config_by_row):
    groups = {}
    counts = Counter()
    statuses = Counter()
    cohorts = Counter()
    for ri, row in enumerate(cases["main_rows"]):
        ds, method = row["dataset"], row["method"]
        row_unit_ids = ["|".join((ds, method, row["opaque_id"], "seed=" + sid))
                        for sid in row["evidence"]["seed_evidence"]]
        for k, mechanism in row["mechanisms"].items():
            cohorts[(ds, method, int(k))] += 1
            statuses[(ds, method, int(k), row["status"])] += 1
            members = list(mechanism["assignment"]["multi"])
            # A non-OK seed must not disappear behind an aggregate row status.
            members.extend("status:" + status for status in sorted({
                units[uid]["status"] for uid in row_unit_ids} - {"OK"}))
            for flag in members:
                if not flag.startswith("status:") and flag not in FLAGS:
                    raise ValueError("unknown flag " + flag)
                counts[(ds, method, int(k), flag)] += 1
                gid = "|".join((ds, method, "k=" + k, flag))
                group = groups.setdefault(gid, {
                    "group_id": gid, "dataset": ds, "method": method, "k": int(k), "flag_or_status": flag,
                    "configuration": config_by_row[ri], "source_rows": [], "candidate_wrong_unit_ids": [],
                    "selected_wrong_unit_id": None, "selection_status": "selection_pending",
                    "selection_reasons": ["Processing paths not yet verified; sample must be expanded for distinct paths."]})
                if group["configuration"] != config_by_row[ri]:
                    raise ValueError("group contains different configurations; explicit split required: " + gid)
                group["source_rows"].append(reference(T28 + "/ca-sai.json", f"/main_rows/{ri}"))
                for uid in row_unit_ids:
                    unit = units[uid]
                    matches = (unit["status"] == flag[7:]) if flag.startswith("status:") else (
                        flag in unit["by_k"][k]["assignment"]["multi"])
                    if matches:
                        group["candidate_wrong_unit_ids"].append(uid)
                        unit["groups"].append(gid)
    checks = []
    overall_keys = set()
    for si, table in enumerate(summary["mechanism_tables"]):
        if table["group_field"] != "overall":
            continue
        ds, method, k = table["dataset"], table["method"], int(table["k"])
        key = (ds, method, k)
        if key in overall_keys:
            raise ValueError("duplicate overall summary")
        overall_keys.add(key)
        actual_status = {status: n for (d, m, kk, status), n in statuses.items() if (d, m, kk) == key}
        check = {"key": list(key), "cohort": cohorts[key], "status_counts": actual_status,
                 "multi": {flag: counts[(*key, flag)] for flag in FLAGS},
                 "source": reference(T28 + "/summary-tables.json", f"/mechanism_tables/{si}")}
        if (check["cohort"] != table["n_cohort"] or actual_status != table["status_counts"] or
                check["multi"] != table["multi"]):
            raise ValueError("catalogue/summary mismatch: " + canonical(check))
        checks.append(check)
    if overall_keys != set(cohorts):
        raise ValueError("summary/case cohort keys differ")
    for group in groups.values():
        group["candidate_wrong_unit_ids"].sort()
        if not group["candidate_wrong_unit_ids"]:
            group["selection_reasons"].append("Aggregate flag has no same-flag seed witness; inspect seed aggregation before selection.")
        group["n_source_cases"] = len(group["source_rows"])
    return list(groups.values()), checks


def matching_inventory(groups, units):
    """Enumerate, do not rank candidates that differ in unspecified ways."""
    pairs, examples, seen = [], [], set()
    for group in groups:
        k = str(group["k"])
        for uid in group["candidate_wrong_unit_ids"]:
            pair_key = (uid, k)
            if pair_key in seen:
                continue
            seen.add(pair_key)
            wrong = units[uid]
            correct_pool = [u for u in units.values() if u["dataset"] == wrong["dataset"] and
                            u["method"] == wrong["method"] and u["status"] == "OK" and
                            not u["by_k"][k]["wrong_OK"]]
            eligible, rejected = [], []
            for correct in sorted(correct_pool, key=lambda x: (x["opaque_id"], x["seed_key"])):
                mandatory = differences(wrong["mandatory_conditions"], correct["mandatory_conditions"])
                if mandatory:
                    rejected.append({"unit_id": correct["unit_id"], "condition_differences": mandatory})
                    continue
                preferred = differences(wrong["preferred_conditions"], correct["preferred_conditions"])
                eligible.append({"unit_id": correct["unit_id"], "same_cell": wrong["cell"] == correct["cell"],
                                 "saved_preferred_metadata_equal": not preferred,
                                 "difference_count": len(preferred),
                                 "first_differences": preferred[:16],
                                 "full_condition_source": "unit-universe.json#/units (both unit_ids)",
                                 "processing_path_equivalent": None})
            item = {"wrong_unit_id": uid, "k": int(k),
                    "group_ids": [g for g in wrong["groups"] if "|k=" + k + "|" in g],
                    "selected_correct_unit_id": None, "eligible_candidates": eligible,
                    "rejected_correct_candidates": rejected,
                    "selection_status": "selection_pending" if eligible else "no_mandatory_match",
                    "reason": ("Runtime path equivalence not verified; unequal metadata have no approved distance/tolerance."
                               if eligible else "No correct seed has the recorded same dataset/configuration/F/adapter conditions."),
                    "no_match_is_data_impossibility": False}
            pairs.append(item)
            if eligible and len(examples) < 12:
                representative = next((c for c in eligible if c["same_cell"]), eligible[0])
                examples.append({"group_ids": item["group_ids"], "wrong_unit_id": uid,
                                 "candidate_correct_unit_id": representative["unit_id"],
                                 "example_is_selection": False, "same_cell": representative["same_cell"],
                                 "difference_count": representative["difference_count"],
                                 "first_differences": representative["first_differences"][:12],
                                 "all_differences_source": "counterpart-candidates.json"})
    return pairs, examples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rootPath", type=Path, default=BASE / "repo")
    parser.add_argument("--outPath", type=Path, default=BASE / "runs/groups-001")
    parser.add_argument("--packageManifest", type=Path, default=BASE / "inputs/package-manifest.json")
    args = parser.parse_args()
    if os.name != "posix":
        raise RuntimeError("Research metadata computation is authorized on EC2 only.")
    root, out = args.rootPath.resolve(), args.outPath.resolve()
    if not out.is_relative_to(BASE.resolve()) or out == BASE.resolve():
        raise ValueError("output must be a new run under ~/rca/T-032/")
    if not root.is_relative_to(BASE.resolve()):
        raise ValueError("rootPath must be under ~/rca/T-032/")
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    reader = None
    try:
        reader = Reader(root, args.packageManifest.resolve())
        cases, summary, units, configurations = prepare(reader)
        groups, checks = catalogue(cases, summary, units, configurations)
        pairs, examples = matching_inventory(groups, units)
        write(out / "catalog.json", {"task": "T-032", "catalog_status": "frozen_source_groups_locked",
                                   "manual_selection_status": "pending", "groups": groups,
                                   "counts_checked_against_frozen_summary": checks})
        write(out / "unit-universe.json", {"units": list(units.values()),
              "unit_definition": "case x main configuration x seed; runtime paths remain OPEN",
              "reading_order_not_selection": sorted(units),
              "deduplication": "Each frozen seed record occurs once; a unit may cover multiple k/flags. No seed equivalence inferred."})
        write(out / "counterpart-candidates.json", {"pairs": pairs,
              "ordering": "opaque_id then seed only for display; not a scientific preference among unequal metadata",
              "prohibited_match_inputs": ["score margin", "caller above root", "intervention result", "rank improvement"],
              "pending_examples": examples})
        write(out / "selection-open.json", {"status": "OPEN", "examples": examples,
              "required_runtime_evidence": "Verified replay processing paths/branches for units, including successful counterparts and non-OK paths.",
              "required_selection_definition": "Where candidates differ: decide which saved scale/coverage quantities define equivalence and how to prioritize incomparable differences. Do not invent thresholds.",
              "core_replay_blocked": False,
              "blocked_claims": ["final manual sample locked", "all processing paths represented", "same-condition counterpart established"],
              "preserved_sensitivity_sources": [reference(T28 + "/ca-sai.json", "/circa_dev19_conditional"),
                                                 reference(T28 + "/ca-sai.json", "/nezha_saved_sensitivity_flags")],
              "sensitivity_is_additional_main_configuration": False})
        outputs = [{"path": p.name, "sha256": sha(p), "bytes": p.stat().st_size}
                   for p in sorted(out.iterdir()) if p.is_file()]
        write(out / "manifest.json", {"task": "T-032", "status": "PASS_CATALOG_SELECTION_PENDING",
              "at": now(), "elapsed_s": time.perf_counter() - started, "script_sha256": sha(Path(__file__)),
              "command": sys.argv, "inputs": reader.inputs, "outputs": outputs,
              "n_groups": len(groups), "n_units": len(units), "n_pair_requests": len(pairs),
              "raw_data_read": False, "method_rerun": False, "manual_sample_locked": False})
        print(canonical({"status": "PASS_CATALOG_SELECTION_PENDING", "groups": len(groups),
                         "units": len(units), "pair_requests": len(pairs), "outPath": str(out)}), flush=True)
    except BaseException as exc:
        write(out / "failure.json", {"status": "FAIL", "at": now(), "error": str(exc),
              "traceback": traceback.format_exc(), "elapsed_s": time.perf_counter() - started,
              "verified_inputs": reader.inputs if reader else [], "do_not_use_partial_outputs": True})
        raise


if __name__ == "__main__":
    main()
