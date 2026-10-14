"""T-032 saved SimpleRCA evidence reader; EC2 only, no native method execution.

All old artifacts (including Parquet) are hashed before JSON is used. This
reader exposes previously audited channel values/witnesses and reconstructs
only saved scalar votes and service aggregation. It never loads a raw dataset,
imports a ranking method, refits a model or changes a scientific threshold.
Physical waiting and causal mechanisms remain OPEN for manual discrimination.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import sys
import time
import traceback


EXACT_FIELDS = (
    "opaque_id", "method", "method_version", "variant", "mode", "detector",
    "detector_columns", "seed", "hashseed", "config_id", "why_ids", "window",
    "input_shape", "status", "method_status_raw", "error", "ranking_native",
    "ranking", "entity_ranking", "blocks", "sets", "diagnostics", "extra", "input_sha256",
)
EXCLUDED_FIELDS = {"run_id", "cost"}
CONFIG = {"metric_rule": "sigma", "sigma": 3.0, "metric_quantile": 0.95,
          "trace_quantile": 0.95, "trace_factor": 3.0, "log_threshold": 0,
          "metric_aggregation": "events", "min_normal_metric": 2,
          "keywords": ["ERROR", "FAIL", "EXCEPTION"]}


class StopResearch(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise StopResearch(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def safe(base, relative):
    rel = PurePosixPath(relative.replace("\\", "/"))
    require(not rel.is_absolute() and ".." not in rel.parts, f"unsafe reference: {relative}")
    require(not any(x in {"T-033", "test", "tests", "locked"} for x in rel.parts),
            f"forbidden reference: {relative}")
    path = (base / Path(*rel.parts)).resolve()
    require(base == path or base in path.parents, f"reference escaped base: {relative}")
    return path


def pin(path, expected, size=None):
    require(path.is_file(), f"missing artifact: {path}")
    require(size is None or path.stat().st_size == size, f"size mismatch: {path}")
    actual = digest(path)
    require(actual == expected, f"hash mismatch: {path}")
    return {"path": str(path), "sha256": actual, "bytes": path.stat().st_size, "status": "PASS"}


def pointer(path, at=""):
    return {"path": str(path), "json_pointer": at}


def escape(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def same(left, right, message):
    """No numerical tolerance, integer/float coercion, or signed-zero relaxation."""
    if type(left) is not type(right):
        raise StopResearch(message + " (type)")
    if isinstance(left, dict):
        require(set(left) == set(right), message + " (keys)")
        for key in left:
            same(left[key], right[key], message + "/" + str(key))
    elif isinstance(left, list):
        require(len(left) == len(right), message + " (length)")
        for index, (a, b) in enumerate(zip(left, right)):
            same(a, b, message + f"/{index}")
    elif isinstance(left, float):
        require(left.hex() == right.hex(), message + " (float)")
    else:
        require(left == right, message)


def number(value, name):
    require(type(value) in (int, float) and math.isfinite(value), f"nonfinite scalar: {name}")
    return value


def integer(value, name):
    require(type(value) is int and value >= 0, f"invalid nonnegative integer: {name}")
    return value


def channel_sizes(meta):
    if meta["unavailable"]:
        return None
    channels, lengths = meta["channels"], meta["lengths"]
    require(isinstance(channels, list) and len(channels) == len(lengths)
            and len(set(channels)) == len(channels), "invalid observed channel lengths")
    return {key: integer(size, "channel length") for key, size in zip(channels, lengths)}


def positions(part, row, n_length, a_length):
    for label, length, count, missing in (
        ("N", n_length, row["n_normal"], row["missing_normal"]),
        ("A", a_length, row["n_incident"], row["missing_incident"]),
    ):
        finite, excluded = part["finite_" + label], part["excluded_" + label]
        require(len(finite) == count and len(excluded) == missing
                and count + missing == length, "finite/missing position counts disagree")
        require(all(type(x) is int for x in finite + excluded)
                and finite == sorted(set(finite)) and excluded == sorted(set(excluded))
                and set(finite).isdisjoint(excluded)
                and sorted(finite + excluded) == list(range(length)),
                "finite/excluded positions do not partition the native channel")
    require(part["availability"] == row["status"], "availability differs from actual native return")


def verify_sources(source, source_checks, start, plan, repo, code_seen):
    require(source["selected_allowlist_hashes_equal_frozen_inputs"] is True,
            "source input hashes were not matched to frozen record")
    require(source_checks["checks"] and all(x.get("pass") is True for x in source_checks["checks"]),
            "saved source check did not pass")
    expected = plan["code_hashes"]
    for ref in source["actual_imports"]:
        require(ref["path"] in expected and ref["sha256"] == expected[ref["path"]],
                "actual imported source not pinned by frozen authorities")
        path = safe(repo, ref["path"])
        key = (str(path), ref["sha256"])
        if key not in code_seen:
            code_seen[key] = pin(path, ref["sha256"])
    for name, ref in start["sources"].items():
        relative = plan["capture_source_names"][name]
        require(ref["sha256"] == expected[relative], f"observed {name} source hash differs")
        path = Path(ref["path"]).resolve()
        require(path == safe(repo, relative), f"observed {name} resolved outside frozen task copy")
        key = (str(path), ref["sha256"])
        if key not in code_seen:
            code_seen[key] = pin(path, ref["sha256"])


def verify_case(entry, plan, repo, runs, code_seen):
    started = time.monotonic()
    base = safe(runs, entry["run_relative"])
    check_base = safe(runs, entry["audit_relative"]) if entry.get("audit_relative") else base
    check_pin = pin(check_base / "check.json", entry["check_sha256"])
    check = read(check_base / "check.json")
    require(check["status"] == "PASS" and check["intermediates_eligible"] is True,
            f"ineligible SimpleRCA capture: {base}")
    require(check["method"] == "simplerca" and check["opaque_id"] == entry["opaque_id"]
            and check["dataset"] == entry["dataset"], "capture identity differs from plan")
    require(check["differences"] == [], "frozen comparison has differences")
    if entry.get("audit_relative"):
        require(check["record_exact"] is True and check["methods_executed"] is False
                and Path(check["original_run"]).resolve() == base,
                "retained RE2 pilot not exactly verified by separate audit")
        manifest = check["original_artifact_manifest"]
    else:
        require(check["compare"]["pass"] is True and check["compare"]["difference_count"] == 0,
                "direct frozen compare failed")
        manifest = check["artifact_manifest"]
        same(check["exact_fields"], list(EXACT_FIELDS), "saved exact-field coverage differs")
    audit = check["capture_check"]
    require(all(audit.get(field) is True for field in (
        "pass", "hooks_restored", "adapter_input_projections_unchanged", "native_inputs_unchanged",
        "preparation_exact", "native_called", "native_formula_exact", "full_native_return_exact",
        "adapter_mapping_exact")), "full input/native/mapping audit incomplete")
    require(audit["native_outcome"] == "return", "native did not return")
    require(len({x["path"] for x in manifest}) == len(manifest), "duplicate artifact path")
    indexed = {x["path"]: x for x in manifest}
    for ref in manifest:
        pin(safe(base, ref["path"]), ref["sha256"], ref["bytes"])
    required = ("source.json", "source-checks.json", "ban-ghi-0.json", "capture/capture.json",
                "capture/capture-start.json", "capture/native-result.json", "capture/row-evidence.json")
    require(all(path in indexed for path in required), "saved chain lacks a manifested component")
    frozen_path = safe(repo, entry["frozen_path"])
    frozen_pin = pin(frozen_path, entry["frozen_sha256"])
    require(check["frozen_sha256"] == entry["frozen_sha256"]
            and check["frozen_path"] == entry["frozen_path"], "frozen source binding differs")
    frozen, replay = read(frozen_path), read(base / "ban-ghi-0.json")
    pin(base / "ban-ghi-0.json", entry["record_sha256"])
    require(set(frozen) == set(EXACT_FIELDS) | EXCLUDED_FIELDS
            and set(replay) == set(frozen), "record schema comparison scope changed")
    for field in EXACT_FIELDS:
        same(frozen[field], replay[field], "frozen exact field " + field)
    same(frozen["window"], entry["frozen_window"], "source F window changed")
    capture_base = base / "capture"
    capture, start = read(capture_base / "capture.json"), read(capture_base / "capture-start.json")
    require(capture["status"] == "captured_unverified_replay" and not capture["errors"]
            and capture["caller_exception"] is None and capture["trace_restored"] is True
            and capture["profile_restored"] is True, "capture incomplete or hooks changed")
    require(start["dataset"] == entry["dataset"], "capture dataset differs")
    method_plan = {**plan, "capture_source_names": plan["capture_source_names"][entry["dataset"]]}
    verify_sources(read(base / "source.json"), read(base / "source-checks.json"),
                   start, method_plan, repo, code_seen)
    calls = []
    for ref in capture["calls"]:
        require("capture/" + ref["path"] in indexed, "unmanifested observed call")
        call = read(safe(capture_base, ref["path"]))
        require(call["function"] == ref["function"] and call["outcome"] == ref["outcome"]
                and call["exceptions"] == ref["exceptions"] and call["outcome"] == "return",
                "actual call/index disagreement")
        call["_pointer"] = pointer(safe(capture_base, ref["path"]))
        calls.append(call)
    natives = [c for c in calls if c["function"] == "native"]
    adapters = [c for c in calls if c["function"] == "adapter"]
    require(len(natives) == len(adapters) == 1, "expected one original native/adapter call")
    native_call, adapter_call = natives[0], adapters[0]
    inputs = native_call["entry"]["inputs"]
    native_path, witness_path = capture_base / "native-result.json", capture_base / "row-evidence.json"
    native, witness = read(native_path), read(witness_path)
    same(native["config"], CONFIG, "native configuration differs from frozen main M4")
    same(native_call["entry"]["config"], CONFIG, "observed native config differs")
    require(native["fallback"] is False, "native fallback used")
    n_metric, a_metric = channel_sizes(inputs["normal_metrics"]), channel_sizes(inputs["incident_metrics"])
    n_trace, a_trace = channel_sizes(inputs["normal_traces"]), channel_sizes(inputs["incident_traces"])
    n_trace, a_trace = n_trace or {}, a_trace or {}
    log_sizes = channel_sizes(inputs["incident_logs"])
    require(set(n_metric) == set(a_metric) == set(inputs["metric_services"])
            == set(native["metrics"]) == set(witness["metrics"]), "metric channel coverage differs")
    totals = {service: {"metric": 0, "trace": 0, "log": 0, "score": 0}
              for service in native["scores"]}
    metrics, traces, logs = [], [], []
    for key, row in native["metrics"].items():
        require(row["service"] == inputs["metric_services"][key] and row["service"] in totals,
                "metric mapping changed")
        ev = witness["metrics"][key]
        positions(ev, row, n_metric[key], a_metric[key])
        sufficient = row["n_normal"] >= CONFIG["min_normal_metric"] and row["n_incident"] > 0
        require((row["status"] == "ok") == sufficient, "metric availability does not follow native sample rule")
        integer(row["count"], "metric count"); integer(row["vote"], "metric vote")
        if sufficient:
            for field in ("mean", "std", "threshold", "max_incident"):
                number(row[field], field)
            same(row["mean"] + CONFIG["sigma"] * row["std"], row["threshold"], "saved sigma threshold differs")
            require(row["std"] >= 0 and row["count"] == row["vote"] == len(ev["event_positions_A"]),
                    "events aggregation differs from actual native count")
            require(ev["event_positions_A"] == sorted(set(ev["event_positions_A"]))
                    and set(ev["event_positions_A"]) <= set(ev["finite_A"]), "event witness positions invalid")
            require((row["max_incident"] > row["threshold"]) == (row["count"] > 0),
                    "maximum/event threshold relation differs")
        else:
            require(row["count"] == row["vote"] == 0 and ev["event_positions_A"] == [],
                    "unavailable metric has invented vote")
        totals[row["service"]]["metric"] += row["vote"]
        metrics.append({"metric": key, "service": row["service"], "native": row,
                        "row_witness": ev, "source": pointer(native_path, "/metrics/" + escape(key)),
                        "witness_source": pointer(witness_path, "/metrics/" + escape(key)),
                        "native_input_source": pointer(Path(native_call["_pointer"]["path"]), "/entry/inputs"),
                        "event_unit": "one vote per finite anomalous metric sample; not one vote per metric channel"})
    require(set(native["traces"]) == set(n_trace) | set(a_trace)
            and set(witness["traces"]) == set(native["traces"]), "trace channel coverage differs")
    for service, row in native["traces"].items():
        ev = witness["traces"][service]
        positions(ev, row, n_trace.get(service, 0), a_trace.get(service, 0))
        sufficient = row["n_normal"] > 0 and row["n_incident"] > 0
        require((row["status"] == "ok") == sufficient, "trace availability differs from native rule")
        if sufficient:
            for field in ("p95_normal", "p95_incident", "threshold"):
                number(row[field], field)
            require(row["p95_normal"] >= 0 and row["p95_incident"] >= 0, "negative saved duration quantile")
            same(CONFIG["trace_factor"] * row["p95_normal"], row["threshold"], "saved trace threshold differs")
            require(type(row["vote"]) is int and row["vote"] == int(row["p95_incident"] > row["threshold"]),
                    "strict trace inequality/vote differs")
            for label, value in (("N", row["p95_normal"]), ("A", row["p95_incident"])):
                q = ev["quantile_" + label]
                same(q["value"], value, "quantile witness differs from native result")
                require(q["lower_channel_position"] in ev["finite_" + label]
                        and q["upper_channel_position"] in ev["finite_" + label]
                        and q["lower_value"] <= value <= q["upper_value"], "quantile witness rows invalid")
        else:
            require(row["vote"] == 0, "unavailable trace has invented vote")
        totals[service]["trace"] += row["vote"]
        traces.append({"service": service, "native": row, "row_witness": ev,
                       "source": pointer(native_path, "/traces/" + escape(service)),
                       "witness_source": pointer(witness_path, "/traces/" + escape(service)),
                       "vote_unit": "at most one trace vote per service; service duration p95, not request-count or waiting time",
                       "quantile_recomputed": False})
    require(set(native["logs"]) == set(witness["logs"]) == set(totals), "log/candidate coverage differs")
    for service, row in native["logs"].items():
        ev = witness["logs"][service]
        require(ev["availability"] == row["status"], "log availability differs")
        if log_sizes is None:
            require(row["status"] == "unavailable" and row["count"] == {"__missing__": "None"}
                    and row["vote"] == 0 and ev["keyword_positions_A"] == {"__missing__": "None"},
                    "unavailable logs changed to zero observed rows")
        else:
            hits = ev["keyword_positions_A"]
            require(row["status"] == "ok" and ev["rows_A"] == log_sizes.get(service, 0)
                    and hits == sorted(set(hits)) and all(type(x) is int and 0 <= x < ev["rows_A"] for x in hits)
                    and row["count"] == len(hits) and row["threshold"] == CONFIG["log_threshold"]
                    and type(row["vote"]) is int and row["vote"] == int(row["count"] > row["threshold"]),
                    "log keyword/count/binary vote differs")
        totals[service]["log"] += row["vote"]
        logs.append({"service": service, "native": row, "row_witness": ev,
                     "source": pointer(native_path, "/logs/" + escape(service)),
                     "witness_source": pointer(witness_path, "/logs/" + escape(service)),
                     "vote_unit": "at most one vote per service; keyword count is at most one hit per message row"})
    for row in totals.values():
        row["score"] = row["metric"] + row["trace"] + row["log"]
    same(totals, native["scores"], "per-service saved evidence sum differs")
    ranks = sorted(totals, key=lambda service: (-totals[service]["score"], service))
    same(ranks, native["ranks"], "service sorting keys differ")
    groups = []
    for service in ranks:
        if not groups or groups[-1]["score"] != totals[service]["score"]:
            groups.append({"score": totals[service]["score"], "services": []})
        groups[-1]["services"].append(service)
    same(groups, native["tie_groups"], "exact score tie groups differ")
    require(native["status"] == ("abstain" if groups[0]["score"] == 0 else "heuristic_alerts"),
            "native abstain state differs")
    items = [] if native["status"] == "abstain" else [
        {"item": service, "entity": service.split("_", 1)[0] if entry["dataset"] == "RE2-TT" else service,
         "key": [float(totals[service]["score"])]} for service in ranks]
    same(items, frozen["ranking"], "saved components to frozen protocol ranking differs")
    same(ranks, frozen["ranking_native"], "saved native ranks to frozen record differs")
    best = {}
    for item in items:
        best.setdefault(item["entity"], item["key"])
    entities, prior, group_id = [], None, -1
    for entity, key in sorted(best.items(), key=lambda pair: pair[1], reverse=True):
        if key != prior:
            group_id += 1
        entities.append({"entity": entity, "key": key, "tie_group": group_id})
        prior = key
    same(entities, frozen["entity_ranking"], "max-per-entity protocol aggregation differs")
    for name, value in (("metrics", native["metrics"]), ("traces", native["traces"]),
                        ("logs", native["logs"]), ("totals", native["scores"])):
        same(native_call["locals"][name], value, "actual observed local/return chain " + name)
    return {"unit_id": entry["unit_id"], "dataset": entry["dataset"], "opaque_id": entry["opaque_id"],
            "method": "simplerca", "status": "OBSERVED_CHAIN_EXACT_CHECKED",
            "configuration": {key: frozen[key] for key in
                              ("method_version", "variant", "mode", "seed", "hashseed", "config_id")},
            "window": frozen["window"], "input_shape": frozen["input_shape"], "native_status": native["status"],
            "source": {"check": check_pin, "frozen": frozen_pin, "n_artifacts_checked": len(manifest),
                       "actual_native": pointer(native_path), "derived_row_evidence": pointer(witness_path)},
            "native_config": native["config"], "observed_input_meta": inputs,
            "metrics": metrics, "traces": traces, "logs": logs, "service_scores": native["scores"],
            "native_tie_groups": native["tie_groups"], "entity_ranking": entities,
            "sort_key": "descending summed evidence count, then native service name ascending; exact score groups",
            "entity_mapping": "RE2: first underscore prefix, per-entity maximum; Nezha: identity, per-entity maximum",
            "preparation_call_pointers": [c["_pointer"] for c in calls],
            "adapter_projection_meta": adapter_call["entry"]["tables"],
            "arithmetic_reconstruction": "saved scalar thresholds, votes, integer sum/rank only; old full-array exact audit retained",
            "method_executed": False, "raw_dataset_read": False, "fresh_array_recalculation": False,
            "physical_wait_established": False, "graph_benefit_evaluated": False,
            "observed_seconds": time.monotonic() - started}


def service_view(chain, entity):
    members = [service for service in chain["service_scores"]
               if (service.split("_", 1)[0] if chain["dataset"] == "RE2-TT" else service) == entity]
    ranking = next((row for row in chain["entity_ranking"] if row["entity"] == entity), None)
    score = ranking["key"][0] if ranking else None
    return {"entity": entity, "availability": "ranked" if ranking else "absent_from_protocol_ranking",
            "native_candidate_members": members, "score": score,
            "native_components": {service: chain["service_scores"][service] for service in members},
            "rank_min": 1 + sum(row["key"][0] > score for row in chain["entity_ranking"]) if ranking else None,
            "rank_max": sum(row["key"][0] >= score for row in chain["entity_ranking"]) if ranking else None,
            "tie_group": ranking["tie_group"] if ranking else None,
            # Keep all witnesses once in the case; views retain native scalars
            # and exact pointers rather than multiplying long row-position lists.
            "metric_chains": [{key: row[key] for key in ("metric", "service", "native", "source", "witness_source")}
                              for row in chain["metrics"] if row["service"] in members],
            "trace_chains": [{key: row[key] for key in ("service", "native", "source", "witness_source")}
                             for row in chain["traces"] if row["service"] in members],
            "log_chains": [{key: row[key] for key in ("service", "native", "source", "witness_source")}
                           for row in chain["logs"] if row["service"] in members]}


def join_context(chain, row, index, path):
    require(row["method"] == "simplerca" and row["dataset"] == chain["dataset"]
            and row["opaque_id"] == chain["opaque_id"], "post-hoc context identity differs")
    seed = row["evidence"]["seed_evidence"]["single"]
    root = service_view(chain, row["root"])
    before = seed["certain_before_root"]
    if root["availability"] == "ranked":
        calculated = [x["entity"] for x in chain["entity_ranking"] if x["key"][0] > root["score"]]
        same(calculated, before, "T-028 certain-before-root differs from exact saved scores")
    m5_k = [int(k) for k, entry in row["mechanisms"].items()
            if entry["explanation_flags_wrong_seeds"]["M5"]["value"] is True]
    observations = []
    for caller, relation in seed["caller_relation"].items():
        if caller == row["root"] or relation["path_to_root"] is not True:
            continue
        caller_view = service_view(chain, caller)
        difference, denominator, margin = None, None, None
        if caller_view["score"] is not None and root["score"] is not None:
            difference = caller_view["score"] - root["score"]
            denominator = abs(caller_view["score"]) + abs(root["score"])
            margin = difference / denominator if denominator else None
        observations.append({"caller": caller_view, "root": root,
                             "relation_context": relation, "certain_before_root_source": caller in before,
                             "score_difference": difference, "normalized_score_margin": margin,
                             "margin_denominator": denominator,
                             "source": pointer(path, f"/main_rows/{index}/evidence/seed_evidence/single/caller_relation/{escape(caller)}"),
                             "computational_status": "components_and_sort_exact; competing interpretation pending manual controls",
                             "caller_own_rule_evidence": {"metric_positive_votes": [x["metric"] for x in caller_view["metric_chains"] if x["native"]["vote"] > 0],
                                                          "trace_positive_votes": [x["service"] for x in caller_view["trace_chains"] if x["native"]["vote"] > 0],
                                                          "log_positive_votes": [x["service"] for x in caller_view["log_chains"] if x["native"]["vote"] > 0],
                                                          "meaning": "native rule crosses on a channel attributed to caller; not proof of physical work at caller"},
                             "physical_wait_established": False,
                             "missing_for_physical_discrimination": "synchronous wait semantics, comparable clocks/coverage and competing own/shared-load explanation"})
    chain["T028_context"] = {"root": row["root"], "fault": row["fault"], "cell": row["cell"],
                              "source": pointer(path, f"/main_rows/{index}"), "source_M5_k": m5_k,
                              "wrong_OK_at_1": row["wrong_OK_at_1"], "wrong_OK_at_5": row["wrong_OK_at_5"],
                              "source_certain_before_root": before, "source_by_k": seed["by_k"],
                              "graph_role": row["evidence"]["graph_role"],
                              "labels_use": "post-hoc only; no native call made by reader"}
    chain["root_score_chain"] = root
    chain["caller_root_observations"] = observations
    chain["explanations_remaining"] = [
        {"candidate": "Caller has more event votes because more finite anomalous samples/channels or thresholds crossing; trace/log each at most one service vote.",
         "status": "exact constituents exposed; conditional comparison with locked correct controls pending"},
        {"candidate": "Root missing/unavailable channel, entity mapping, or score tie changes candidate/rank interpretation.",
         "status": "actual channel availability, candidate set and exact score groups exposed; manual input-chain reading pending"},
        {"candidate": "Caller waits for downstream work, executes own anomalous work, or shares load/resource causes.",
         "status": "not distinguished by service duration p95, event votes or parent-child topology alone"}]


def F_policy(window, expected):
    if expected["unit"] == "ns":
        marker, n, a = window["t_ns"], window["N_ns"], window["A_ns"]
    else:
        require(expected["unit"] == "s", "unknown source F time unit")
        marker, n, a = window["t"], window["N"], window["A"]
    same([x - marker for x in n], expected["N_offsets"], "N source window policy differs")
    same([x - marker for x in a], expected["A_offsets"], "A source window policy differs")
    require(window.get("trace_guard_s", 0) == expected["trace_guard_s"], "source trace guard differs")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--plan-sha256", required=True)
    parser.add_argument("--repo", type=Path, default="/home/ubuntu/rca/T-032/repo")
    parser.add_argument("--runs", type=Path, default="/home/ubuntu/rca/T-032/runs")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    require(platform.system() == "Linux", "Research reader must execute on approved EC2, not laptop")
    repo, runs, output = args.repo.resolve(), args.runs.resolve(), args.out.resolve()
    require(repo == Path("/home/ubuntu/rca/T-032/repo") and runs == Path("/home/ubuntu/rca/T-032/runs"), "wrong task roots")
    require(runs in output.parents and output.name.startswith("execution-") and not output.exists(), "use new T-032 execution directory")
    output.mkdir(parents=True)
    started = time.monotonic()
    try:
        plan_pin = pin(args.plan.resolve(), args.plan_sha256)
        plan = read(args.plan)
        require(plan["task"] == "T-032" and plan["method"] == "simplerca", "wrong saved chain plan")
        pin(Path(__file__).resolve(), plan["script_sha256"])
        require(len(plan["cases"]) == 52 and len({x["unit_id"] for x in plan["cases"]}) == 52, "not full52unique cohort")
        input_pins = [pin(safe(repo, ref["path"]), ref["sha256"], ref["bytes"]) for ref in plan["repo_inputs"]]
        source_path = safe(repo, plan["T028_source_path"])
        rows = read(source_path)["main_rows"]
        selection_path = safe(repo, plan["group_selection_path"])
        selection = read(selection_path)
        require(selection["catalog_locked"] is True and selection["manual_sample_locked"] is True, "group catalog/sample not locked")
        cases, code_seen = [], {}
        for index, entry in enumerate(plan["cases"]):
            chain = verify_case(entry, plan, repo, runs, code_seen)
            join_context(chain, rows[entry["T028_row_index"]], entry["T028_row_index"], source_path)
            cases.append(chain)
            progress = {"index": index + 1, "of": 52, "opaque_id": entry["opaque_id"],
                        "status": "PASS", "elapsed_s": time.monotonic() - started}
            with (output / "progress.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(progress, ensure_ascii=False) + "\n")
            print(f"SimpleRCA saved chain {index + 1}/52 {entry['opaque_id']} PASS", flush=True)
        lookup = {case["unit_id"]: index for index, case in enumerate(cases)}
        controls = []
        for index, pair in enumerate(selection["counterpart_pairs"]):
            if "|simplerca|" not in pair["wrong_unit_id"]:
                continue
            require(pair["wrong_unit_id"] in lookup, "locked wrong unit missing")
            wrong = cases[lookup[pair["wrong_unit_id"]]]
            F_policy(wrong["window"], pair["mandatory_conditions"]["F"])
            links = []
            for ctrl in pair["control_classes"]:
                uid = ctrl["selected_correct_unit_id"]
                require(uid in lookup, "locked control unit missing")
                correct = cases[lookup[uid]]
                same(wrong["configuration"], correct["configuration"], "control configuration differs")
                require(wrong["dataset"] == correct["dataset"] == pair["mandatory_conditions"]["dataset"], "control dataset differs")
                F_policy(correct["window"], pair["mandatory_conditions"]["F"])
                require(correct["T028_context"][f"wrong_OK_at_{pair['k']}"] is False, "locked control wrong at source k")
                links.append({"class_id": ctrl["class_id"], "unit_id": uid, "case_chain_pointer": f"/cases/{lookup[uid]}",
                              "same_cell": ctrl["same_cell"], "same_channels": ctrl["same_channels"],
                              "same_seed_key": ctrl["same_seed_key"], "condition_difference_summary": ctrl["condition_difference_summary"],
                              "equivalence_scope": ctrl["equivalence_scope"], "manual_reading_status": "chưa đọc từng cặp"})
            controls.append({"source": pointer(selection_path, f"/counterpart_pairs/{index}"),
                             "wrong_unit_id": pair["wrong_unit_id"], "k": pair["k"], "group_ids": pair["group_ids"],
                             "wrong_chain_pointer": f"/cases/{lookup[pair['wrong_unit_id']]}",
                             "control_classes": links, "mandatory_conditions": pair["mandatory_conditions"],
                             "target_step": pair["target_step"], "missing_control_reason": pair["missing_control_reason"],
                             "selection_recomputed": False})
        m5 = [{"opaque_id": case["opaque_id"], "dataset": case["dataset"], "source_M5_k": case["T028_context"]["source_M5_k"],
               "case_chain_pointer": f"/cases/{index}", "caller_root_observations": case["caller_root_observations"],
               "source": case["T028_context"]["source"], "manual_discrimination": "pending"}
              for index, case in enumerate(cases) if case["T028_context"]["source_M5_k"]]
        counts = {"cases": len(cases), "RE2": sum(case["dataset"] == "RE2-TT" for case in cases),
                  "Nezha": sum(case["dataset"] == "Nezha-OB" for case in cases), "M5_union_cases": len(m5),
                  "M5_RE2": sum(case["dataset"] == "RE2-TT" for case in m5),
                  "M5_Nezha": sum(case["dataset"] == "Nezha-OB" for case in m5),
                  "locked_pair_requests": len(controls), "locked_control_class_links": sum(len(pair["control_classes"]) for pair in controls)}
        same(counts, plan["counts"], "cohort/M5/control denominators differ from pinned source plan")
        payload = {"schema": "T032.SimpleRCA.saved_chain.v1", "task": "T-032", "method": "simplerca",
                   "status": "OBSERVED_CHAIN_ASSEMBLED_MANUAL_RESEARCH_PENDING", "plan": plan_pin,
                   "inputs": input_pins, "runtime_code_pins": list(code_seen.values()), "counts": counts,
                   "cases": cases, "M5_caller_root": m5, "locked_controls": controls,
                   "method_executed": False, "raw_dataset_read": False, "fresh_array_recalculation": False,
                   "physical_wait_established": False, "graph_benefit_evaluated": False,
                   "manual_reading_complete": False, "elapsed_s": time.monotonic() - started}
        target = output / "simplerca-saved-chains.json"
        write(target, payload)
        write(output / "manifest.json", {"status": "PASS", "task": "T-032", "plan": plan_pin,
                                         "files": [{"path": target.name, "bytes": target.stat().st_size, "sha256": digest(target)}],
                                         "counts": counts, "elapsed_s": payload["elapsed_s"],
                                         "method_executed": False, "manual_research_pending": True})
        write(output / "status.json", {"status": "PASS", "pid": os.getpid(), "elapsed_s": payload["elapsed_s"]})
        print("SimpleRCA full52 saved chains PASS; manual controls and physical interpretation remain pending", flush=True)
        return 0
    except Exception as error:
        failure = {"status": "FAIL_STOP", "pid": os.getpid(), "error": repr(error),
                   "traceback": traceback.format_exc(), "elapsed_s": time.monotonic() - started,
                   "partial_cases_are_not_evidence": True, "method_executed": False}
        write(output / "failure.json", failure)
        write(output / "status.json", failure)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
