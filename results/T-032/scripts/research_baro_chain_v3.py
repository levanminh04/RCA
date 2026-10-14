"""T-032: assemble observed BARO chains on EC2 without executing a method.

The source snapshots, scalers and scores were produced by already exact-checked
replays. This reader verifies their full manifests and exposes the saved chain.
Labels and T-028 graph context are joined only after that chain is verified.
It never imports BARO, a dataset loader, sklearn or the shared RCA adapter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import platform
import sys
import time
import traceback


class StopResearch(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise StopResearch(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_relative(base, relative):
    rel = pathlib.PurePosixPath(relative.replace("\\", "/"))
    require(not rel.is_absolute() and ".." not in rel.parts,
            f"unsafe relative input: {relative}")
    require(not any(x in {"T-033", "locked", "test"} for x in rel.parts),
            f"forbidden input: {relative}")
    out = (base / pathlib.Path(*rel.parts)).resolve()
    require(out == base or base in out.parents, f"input escapes base: {relative}")
    return out


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_pin(path, expected, byte_count=None):
    require(path.is_file(), f"missing file: {path}")
    if byte_count is not None:
        require(path.stat().st_size == byte_count, f"size mismatch: {path}")
    got = digest(path)
    require(got == expected, f"hash mismatch: {path}: {got} != {expected}")
    return {"path": str(path), "sha256": got, "bytes": path.stat().st_size,
            "status": "PASS"}


def write_json(path, value):
    # A new output directory is mandatory; preserve every failed/partial attempt.
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write("\n")


def source_pointer(path, pointer=""):
    return {"path": str(path), "json_pointer": pointer}


def scalar(values, field):
    require(isinstance(values, list) and len(values) == 1, f"not scalar {field}")
    value = values[0]
    require(isinstance(value, (float, int)) and not isinstance(value, bool)
            and math.isfinite(value), f"nonfinite/non-number {field}: {value}")
    return value


def table_columns(table):
    require(isinstance(table, dict) and isinstance(table.get("columns"), list),
            "missing captured table columns")
    return [x["name"] for x in table["columns"]]


def unique_call(calls, function, group=None, column=None):
    matches = [c for c in calls if c["function"] == function
               and (group is None or c.get("group") == group)
               and (column is None or c.get("column") == column)]
    require(len(matches) == 1, f"expected one {function}/{group}/{column}: {len(matches)}")
    return matches[0]


def verify_call_reference(ref, call):
    """Check the stored call against the v1 observer's two field meanings.

    The summary column records BARO/scaler caller context. For entity_mapping
    that context is preparation/None, while _snapshot stores the mapping
    function's actual col argument in the call file (capture_baro.py:293-295).
    These are separate observed values, not conflicting copies of one value.
    All other functions retain the same context column in both artifacts.
    """
    identity = ref.get("id")
    require(isinstance(identity, int) and not isinstance(identity, bool)
            and identity > 0, "invalid observer call id")
    require(ref["path"] == f"calls/{identity:04d}-{ref['function']}.json",
            f"call id/path mismatch: {ref['path']}")
    for field in ("function", "group", "outcome", "exceptions"):
        require(field in ref and field in call and call[field] == ref[field],
                f"call index {field} mismatch: {ref['path']}")
    require("column" in ref and "column" in call,
            f"missing observer column: {ref['path']}")
    if ref["function"] == "entity_mapping":
        require(ref["group"] == "preparation" and ref["column"] is None,
                f"unexpected mapping caller context: {ref['path']}")
        column = call["column"]
        require(isinstance(column, str) and column,
                f"missing actual mapping argument: {ref['path']}")
        require(call.get("return") == column.split("_")[0],
                f"actual entity mapping differs from source rule: {ref['path']}")
    else:
        require(call["column"] == ref["column"],
                f"call index column mismatch: {ref['path']}")


def service_view(chain, entity):
    metrics = [x for x in chain["metric_chains"] if x["entity"] == entity]
    ranking = next((x for x in chain["entity_ranking"] if x["entity"] == entity), None)
    if ranking is None:
        return {"entity": entity, "availability": "absent_after_intersection",
                "score": None, "max_metrics": [],
                "prepared_columns": [x for x in chain["column_stages"]["prepared"]
                                     if x.split("_")[0] == entity],
                "missing_evidence": "No retained metric score for this entity; inspect saved column stages."}
    score = scalar(ranking["key"], "entity key")
    return {"entity": entity, "availability": "available", "score": score,
            "tie_group": ranking["tie_group"],
            "rank_min": 1 + sum(x["key"][0] > score for x in chain["entity_ranking"]),
            "rank_max": sum(x["key"][0] >= score for x in chain["entity_ranking"]),
            "max_metrics": [x for x in metrics if x["signed_max_robust_z"] == score],
            "all_retained_metric_pointers": [x["source"]["score"] for x in metrics]}


def verify_case(plan_case, repo, runs, code_seen):
    started = time.monotonic()
    base = safe_relative(runs, plan_case["run_relative"])
    check_path = base / "check.json"
    pin = check_pin(check_path, plan_case["check_sha256"])
    check = read_json(check_path)
    require(check["status"] == "PASS" and check["intermediates_eligible"] is True,
            f"ineligible capture: {base}")
    require(check.get("differences") == [] and check["compare"]["pass"] is True,
            f"nonexact replay: {base}")
    require(check["method"] == "baro" and check["opaque_id"] == plan_case["opaque_id"]
            and check["dataset"] == plan_case["dataset"], f"case identity mismatch: {base}")
    require(check["capture_check"]["pass"] is True, f"capture audit failed: {base}")
    manifest = check["artifact_manifest"]
    require(len({x["path"] for x in manifest}) == len(manifest), "duplicate artifact path")
    indexed = {x["path"]: x for x in manifest}
    for entry in manifest:
        check_pin(safe_relative(base, entry["path"]), entry["sha256"], entry["bytes"])
    frozen_path = safe_relative(repo, plan_case["frozen_path"])
    frozen_pin = check_pin(frozen_path, plan_case["frozen_sha256"])
    require(check["frozen_sha256"] == frozen_pin["sha256"], "frozen hash disagrees")
    frozen = read_json(frozen_path)
    require(frozen["window"] == plan_case["frozen_window"], "frozen F window changed")
    replay = read_json(base / "ban-ghi-0.json")
    for field in check["exact_fields"]:
        require(frozen[field] == replay[field], f"frozen exact field mismatch: {field}")
    capture_base = base / "capture"
    capture = read_json(capture_base / "capture.json")
    start = read_json(capture_base / "capture-start.json")
    require(not capture["errors"] and capture.get("caller_exception") is None,
            f"capture exceptions: {base}")
    # Actual code locations are copied from the observer, not inferred by imports.
    for name, ref in start["sources"].items():
        expected = plan_case["source_code_hashes"][name]
        require(ref["sha256"] == expected, f"captured code changed: {name}")
        path = pathlib.Path(ref["path"]).resolve()
        require(str(path).startswith("/home/ubuntu/rca/T-032/")
                or str(path).startswith("/home/ubuntu/rca/T-025/"),
                f"unexpected runtime source: {path}")
        pair = (str(path), expected)
        if pair not in code_seen:
            code_seen[pair] = check_pin(path, expected)
    # Read only observer JSON. Parquet arrays remain immutable references whose
    # bytes were checked above and whose content was audited by the exact replay.
    calls = []
    require(len({x["id"] for x in capture["calls"]}) == len(capture["calls"])
            and len({x["path"] for x in capture["calls"]}) == len(capture["calls"]),
            "duplicate observer call identity/path")
    for ref in capture["calls"]:
        p = "capture/" + ref["path"]
        require(p in indexed, f"unmanifested observer call: {p}")
        call = read_json(safe_relative(capture_base, ref["path"]))
        verify_call_reference(ref, call)
        require(call["outcome"] == "return" and not call.get("exceptions"),
                f"call failed: {ref['path']}")
        call["_pointer"] = source_pointer(base / p)
        calls.append(call)
    native = unique_call(calls, "native", "native")
    prepared = unique_call(calls, "prepare", "preparation")
    prep_calls = [x for x in calls if x["function"] == "preprocess"
                  and x["group"] == "native"]
    require(len(prep_calls) == 2, "expected native N/A preprocessing")
    # The observer table paths encode the two actual partitions explicitly.
    n = next((x for x in prep_calls if x["table"]["path"] == "preprocess-native-N.parquet"), None)
    a = next((x for x in prep_calls if x["table"]["path"] == "preprocess-native-A.parquet"), None)
    require(n is not None and a is not None, "partition table metadata absent")
    ncols, acols = table_columns(n["table"]), table_columns(a["table"])
    intersects = [x for x in ncols if x in acols]
    require(intersects == native["intersects"] == native["return"]["node_names"],
            "native intersection differs from actual preprocess columns")
    score_path = capture_base / capture["score_files"]["native"]
    adapter_score_path = capture_base / capture["score_files"]["adapter_keys"]
    scores = read_json(score_path)
    adapter_scores = read_json(adapter_score_path)
    require([(x["column"], x["score"]) for x in scores]
            == [(x["column"], x["score"]) for x in adapter_scores],
            "native vs adapter key score mismatch")
    require([x["column"] for x in scores] == intersects, "scores not in native column order")
    mappings = {x["column"]: x["return"] for x in calls if x["function"] == "entity_mapping"}
    metric_chains = []
    for i, observed in enumerate(scores):
        col = observed["column"]
        fit = unique_call(calls, "fit", "native", col)
        scale = unique_call(calls, "effective_scale", "native", col)
        transform = unique_call(calls, "transform", "native", col)
        median = scalar(fit["scaler"]["center_"], "median")
        raw_iqr = scalar(scale["entry"]["scale"], "raw IQR")
        denominator = scalar(scale["return"], "effective denominator")
        require(denominator == scalar(fit["scaler"]["scale_"], "fit scale")
                and denominator > 0, "denominator mismatch/nonpositive")
        quantiles = fit["locals"]["quantiles"]
        require(len(quantiles) == 2, "unexpected quantile range")
        q25, q75 = scalar(quantiles[0], "Q25"), scalar(quantiles[1], "Q75")
        require(raw_iqr == q75 - q25, "recorded IQR differs from saved quantiles")
        require(fit["scaler"]["with_centering"] is True
                and fit["scaler"]["with_scaling"] is True
                and fit["scaler"]["unit_variance"] is False
                and fit["scaler"]["quantile_range"] == [25.0, 75.0],
                "unexpected RobustScaler configuration")
        require(scale["constant_mask"] in ([True], [False]), "unknown scale fallback state")
        require(col in mappings and mappings[col] == col.split("_")[0],
                f"service mapping mismatch: {col}")
        score = observed["score"]
        require(isinstance(score, (float, int)) and math.isfinite(score), "nonfinite score")
        require(observed["max_positions_A"], "maximum has no saved position")
        require(len(observed["max_positions_A"]) == len(observed["max_preprocessed_values"])
                == len(observed["max_input_indices"]) == len(observed["max_adapter_time_markers"]),
                "saved max positions/values/times disagree")
        require(observed["zscores"]["dense_c_order_sha256"]
                == transform["return"]["dense_c_order_sha256"],
                "transform vs scored z-array mismatch")
        for value in observed["max_preprocessed_values"]:
            require((value - median) / denominator == score,
                    f"saved max arithmetic differs from native score: {col}")
        metric_chains.append({
            "column": col, "entity": mappings[col], "median_N": median,
            "quantiles_N": {"Q25": q25, "Q75": q75}, "raw_IQR_N": raw_iqr,
            "effective_denominator": denominator,
            "scale_fallback_observed": scale["constant_mask"][0],
            "signed_max_robust_z": score,
            "max_positions_A": observed["max_positions_A"],
            "max_input_indices": observed["max_input_indices"],
            "max_adapter_time_markers": observed["max_adapter_time_markers"],
            "max_preprocessed_values": observed["max_preprocessed_values"],
            "numerator_at_max": [x - median for x in observed["max_preprocessed_values"]],
            "z_array": observed["zscores"],
            "sample_sizes": {"N": fit["entry"]["input_signature"]["shape"][0],
                             "A": observed["zscores"]["shape"][0]},
            "source": {"fit": fit["_pointer"], "effective_scale": scale["_pointer"],
                       "transform": transform["_pointer"],
                       "score": source_pointer(score_path, f"/{i}")},
            "fresh_array_recalculation": False,
            "array_content_basis": "Full artifact hash plus source exact-replay/capture audit; no refit."
        })
    # Independent scalar reconstruction of the saved adapter aggregation, without
    # executing the adapter or changing scores. Exact equality is required.
    ordered = sorted(metric_chains, key=lambda x: x["signed_max_robust_z"], reverse=True)
    ranking = [{"item": x["column"], "entity": x["entity"],
                "key": [x["signed_max_robust_z"]]} for x in ordered]
    require(ranking == frozen["ranking"], "saved metric score chain vs frozen ranking mismatch")
    require([x["item"] for x in ranking] == frozen["ranking_native"], "native metric order mismatch")
    best = {}
    for item in ranking:
        best.setdefault(item["entity"], item["key"])
    entity_ranking, previous, group = [], None, -1
    for entity, key in sorted(best.items(), key=lambda x: x[1], reverse=True):
        if key != previous:
            group += 1
        entity_ranking.append({"entity": entity, "key": key, "tie_group": group})
        previous = key
    require(entity_ranking == frozen["entity_ranking"], "max-metric service aggregation mismatch")
    stages = {"prepared": table_columns(prepared["table"]), "preprocess_N": ncols,
              "preprocess_A": acols, "intersects": intersects,
              "removed_from_prepared_N": [x for x in table_columns(prepared["table"]) if x not in ncols],
              "removed_from_prepared_A": [x for x in table_columns(prepared["table"]) if x not in acols],
              "dropped_by_intersection_from_N": [x for x in ncols if x not in intersects],
              "dropped_by_intersection_from_A": [x for x in acols if x not in intersects]}
    return {
        "opaque_id": plan_case["opaque_id"], "dataset": plan_case["dataset"], "method": "baro",
        "unit_id": plan_case["unit_id"], "status": "OBSERVED_CHAIN_EXACT_CHECKED",
        "source": {"frozen": frozen_pin, "check": pin,
                   "n_artifacts_checked": len(manifest), "capture_start": str(capture_base / "capture-start.json")},
        "configuration": {k: frozen[k] for k in ["method_version", "variant", "mode", "seed", "hashseed", "config_id"]},
        "window": frozen["window"], "input_shape": frozen["input_shape"],
        "time_axis_semantics": start["time_axis"], "native_parameters": native["parameters"],
        "column_stages": stages,
        "preprocess_source": {"N": n["_pointer"], "A": a["_pointer"], "prepared": prepared["_pointer"],
                              "native": native["_pointer"]},
        "preparation_calls": [x for x in calls if x["function"] in
                              {"main_preprocess", "rename_latency", "drop_constant", "convert_mem_mb"}
                              and x["group"] != "adapter_keys"],
        "metric_chains": metric_chains, "entity_ranking": entity_ranking,
        "observed_seconds": time.monotonic() - started,
        "method_executed": False, "raw_dataset_read": False,
        "physical_wait": {"status": "not_identified_by_this_chain",
                          "reason": "Metric score chain contains no wait/await semantics; caller context is analysis-only."},
        "graph_benefit": {"status": "not_evaluated", "native_graph_computation": False}}


def join_context(chain, source_row, row_index, source_path):
    require(source_row["method"] == "baro" and source_row["opaque_id"] == chain["opaque_id"]
            and source_row["dataset"] == chain["dataset"], "T-028 context identity mismatch")
    seed = source_row["evidence"]["seed_evidence"]["single"]
    root = service_view(chain, source_row["root"])
    before = seed["certain_before_root"]
    if root["availability"] == "available":
        computed_before = [x["entity"] for x in chain["entity_ranking"] if x["key"][0] > root["score"]]
        require(computed_before == before, "T-028 certain-before-root vs observed service keys mismatch")
    m5_k = [int(k) for k, v in source_row["mechanisms"].items()
            if v["explanation_flags_wrong_seeds"]["M5"]["value"] is True]
    pairs = []
    for caller, relation in seed["caller_relation"].items():
        if not relation["path_to_root"] or caller == source_row["root"]:
            continue
        caller_view = service_view(chain, caller)
        margin = None
        if caller_view["availability"] == root["availability"] == "available":
            denominator = abs(caller_view["score"]) + abs(root["score"])
            margin = (caller_view["score"] - root["score"]) / denominator if denominator else None
        pairs.append({"caller": caller_view, "root": root,
                      "relation_context": relation, "certain_before_root_source": caller in before,
                      "normalized_score_margin": margin,
                      "source": source_pointer(source_path,
                                               f"/main_rows/{row_index}/evidence/seed_evidence/single/caller_relation/{caller}"),
                      "interpretation_status": "OBSERVATION_REQUIRES_MANUAL_DISCRIMINATION",
                      "physical_wait_established": False})
    chain["T028_context"] = {"root": source_row["root"], "fault": source_row["fault"], "cell": source_row["cell"],
                              "source": source_pointer(source_path, f"/main_rows/{row_index}"),
                              "wrong_OK_at_1": source_row["wrong_OK_at_1"], "wrong_OK_at_5": source_row["wrong_OK_at_5"],
                              "source_M5_k": m5_k, "source_certain_before_root": before,
                              "source_by_k": seed["by_k"],
                              "graph_role": source_row["evidence"]["graph_role"],
                              "use": "Post-hoc analysis context; never passed to BARO."}
    chain["root_score_chain"] = root
    chain["caller_root_observations"] = pairs
    chain["explanations_remaining"] = [
        {"candidate": "High caller numerator, narrow N denominator, or max across metrics produces the service key.",
         "status": "Numeric constituents exposed; relative attribution across saved correct controls remains manual."},
        {"candidate": "Input channel/preprocessing/intersection coverage changes root observability.",
         "status": "Actual retained/removed columns exposed; source/input semantics must be read with them."},
        {"candidate": "Caller executes anomalously itself, shares load/common cause, or waits for a downstream service.",
         "status": "Not distinguished by metric z/max; needs trace semantics/coverage and validated wait observation."}]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=pathlib.Path)
    parser.add_argument("--plan-sha256", required=True)
    parser.add_argument("--repo", default="/home/ubuntu/rca/T-032/repo", type=pathlib.Path)
    parser.add_argument("--runs", default="/home/ubuntu/rca/T-032/runs", type=pathlib.Path)
    parser.add_argument("--out", required=True, type=pathlib.Path)
    args = parser.parse_args()
    require(platform.system() == "Linux", "Execute this research reader on EC2, not on Minh's laptop.")
    repo, runs = args.repo.resolve(), args.runs.resolve()
    require(str(repo).startswith("/home/ubuntu/rca/T-032/")
            and str(runs).startswith("/home/ubuntu/rca/T-032/"), "wrong task roots")
    output = args.out.resolve()
    require(runs in output.parents and output.name.startswith("execution-"), "use a new T-032 execution directory")
    require(not output.exists(), "output directory already exists; preserve it and choose a new execution id")
    output.mkdir(parents=True)
    started = time.monotonic()
    progress = output / "progress.jsonl"
    try:
        plan_pin = check_pin(args.plan.resolve(), args.plan_sha256)
        plan = read_json(args.plan)
        require(digest(pathlib.Path(__file__).resolve()) == plan["script_sha256"],
                "research reader differs from the pinned implementation")
        require(plan["task"] == "T-032" and plan["method"] == "baro"
                and len(plan["cases"]) == 52, "not the complete locked BARO cohort")
        require(len({x["opaque_id"] for x in plan["cases"]}) == 52, "duplicate cases")
        input_pins = []
        for pin in plan["repo_inputs"]:
            input_pins.append(check_pin(safe_relative(repo, pin["path"]), pin["sha256"], pin["bytes"]))
        source_path = safe_relative(repo, plan["T028_source_path"])
        rows = read_json(source_path)["main_rows"]
        group_path = safe_relative(repo, plan["group_selection_path"])
        selection = read_json(group_path)
        require(selection["catalog_locked"] is True and selection["manual_sample_locked"] is True,
                "group selection not locked")
        cases, code_seen = [], {}
        for i, entry in enumerate(plan["cases"]):
            chain = verify_case(entry, repo, runs, code_seen)
            join_context(chain, rows[entry["T028_row_index"]], entry["T028_row_index"], source_path)
            cases.append(chain)
            with progress.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"index": i + 1, "of": 52, "opaque_id": entry["opaque_id"],
                                    "status": "PASS", "elapsed_s": time.monotonic() - started}) + "\n")
            print(f"BARO chain {i + 1}/52 {entry['opaque_id']} PASS", flush=True)
        lookup = {c["unit_id"]: i for i, c in enumerate(cases)}
        controls = []
        for i, pair in enumerate(selection["counterpart_pairs"]):
            if "|baro|" not in pair["wrong_unit_id"]:
                continue
            require(pair["wrong_unit_id"] in lookup, "missing wrong unit")
            links = []
            for ctrl in pair["control_classes"]:
                uid = ctrl["selected_correct_unit_id"]
                require(uid in lookup, "missing locked correct control")
                wrong, correct = cases[lookup[pair["wrong_unit_id"]]], cases[lookup[uid]]
                require(wrong["dataset"] == correct["dataset"]
                        and wrong["configuration"] == correct["configuration"],
                        "control mandatory dataset/configuration differs")
                expected_f = pair["mandatory_conditions"]["F"]
                for case in (wrong, correct):
                    window = case["window"]
                    require(expected_f["availability"] == "recorded", "missing locked F window")
                    if case["dataset"] == "RE2-TT":
                        require(expected_f["unit"] == "s", "RE2 F unit differs")
                        boundary, normal, incident = window["t"], window["N"], window["A"]
                    elif case["dataset"] == "Nezha-OB":
                        require(expected_f["unit"] == "ns", "Nezha F unit differs")
                        boundary, normal, incident = window["t_ns"], window["N_ns"], window["A_ns"]
                    else:
                        raise StopResearch("unknown locked dataset window schema")
                    require([x - boundary for x in normal] == expected_f["N_offsets"]
                            and [x - boundary for x in incident] == expected_f["A_offsets"],
                            "control source F-window policy differs")
                require(correct["T028_context"][f"wrong_OK_at_{pair['k']}"] is False,
                        "locked control is wrong at this k")
                links.append({"class_id": ctrl["class_id"], "unit_id": uid,
                              "case_chain_pointer": f"/cases/{lookup[uid]}",
                              "same_cell": ctrl["same_cell"], "same_channels": ctrl["same_channels"],
                              "same_seed_key": ctrl["same_seed_key"],
                              "condition_difference_summary": ctrl["condition_difference_summary"],
                              "equivalence_scope": ctrl["equivalence_scope"],
                              "manual_reading_status": "chưa đọc từng cặp; không suy từ đại diện"})
            controls.append({"source": source_pointer(group_path, f"/counterpart_pairs/{i}"),
                             "wrong_unit_id": pair["wrong_unit_id"], "k": pair["k"],
                             "group_ids": pair["group_ids"], "mandatory_conditions": pair["mandatory_conditions"],
                             "wrong_chain_pointer": f"/cases/{lookup[pair['wrong_unit_id']]}",
                             "control_classes": links,
                             "target_step": pair["target_step"], "selection_recomputed": False})
        m5 = [{"opaque_id": c["opaque_id"], "dataset": c["dataset"], "source_M5_k": c["T028_context"]["source_M5_k"],
               "case_chain_pointer": f"/cases/{i}", "caller_root_observations": c["caller_root_observations"],
               "source": c["T028_context"]["source"], "manual_discrimination": "pending"}
              for i, c in enumerate(cases) if c["T028_context"]["source_M5_k"]]
        require(len(m5) == 10 and sum(c["dataset"] == "RE2-TT" for c in m5) == 3
                and sum(c["dataset"] == "Nezha-OB" for c in m5) == 7, "M5 denominator differs from frozen source")
        payload = {"task": "T-032", "method": "baro", "schema": "T032.BARO.saved_chain.v1",
                   "status": "OBSERVED_CHAIN_ASSEMBLED_MANUAL_RESEARCH_PENDING", "plan": plan_pin,
                   "inputs": input_pins, "runtime_code_pins": list(code_seen.values()),
                   "counts": {"cases": 52, "RE2": 30, "Nezha": 22, "M5_union_cases": 10,
                              "locked_pair_requests": len(controls),
                              "locked_control_class_links": sum(len(x["control_classes"]) for x in controls)},
                   "cases": cases, "M5_caller_root": m5, "locked_controls": controls,
                   "elapsed_s": time.monotonic() - started,
                   "method_executed": False, "raw_dataset_read": False,
                   "physical_wait_established": False, "graph_benefit_evaluated": False,
                   "manual_reading_complete": False}
        target = output / "baro-saved-chains.json"
        write_json(target, payload)
        write_json(output / "manifest.json", {"status": "PASS", "task": "T-032", "plan": plan_pin,
                                               "files": [{"path": target.name, "sha256": digest(target),
                                                          "bytes": target.stat().st_size}],
                                               "counts": payload["counts"], "elapsed_s": payload["elapsed_s"],
                                               "method_executed": False, "manual_research_pending": True})
        write_json(output / "status.json", {"status": "PASS", "pid": os.getpid(),
                                             "elapsed_s": time.monotonic() - started})
        print("BARO 52 saved chains PASS; manual research and physical interpretation remain pending", flush=True)
        return 0
    except Exception as exc:
        write_json(output / "failure.json", {"status": "FAIL_STOP", "pid": os.getpid(), "error": repr(exc),
                                              "traceback": traceback.format_exc(),
                                              "elapsed_s": time.monotonic() - started,
                                              "partial_cases_are_not_evidence": True})
        raise


if __name__ == "__main__":
    sys.exit(main())
