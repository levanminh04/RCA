"""Independent T-028 saved-ranking, P0 and schema checks (stdlib only).

This file does not import ranking_evidence, P3 evaluation helpers, raw readers or
methods.  It reads the primary run and frozen result records only.  Selection
uses increasing opaque ids, retains every saved seed and never makes seeds into
case units.  The output is immutable: use another preserved run for a correction.
"""

import argparse
import hashlib
import itertools
import json
import math
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
ORDER = ("M1", "M2", "M3", "M4", "M5", "M6")
KS = (1, 5)
TZ = timezone(timedelta(hours=7))


def now():
    return datetime.now(TZ).isoformat(timespec="milliseconds")


def pointer(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def src(path, ptr=""):
    return {"path": str(path).replace("\\", "/"), "json_pointer": ptr}


def path_in_results(relative):
    p = (ROOT / relative).resolve()
    if not p.is_relative_to(ROOT / "results"):
        raise ValueError("Checker reads result artifacts only: " + str(relative))
    return p


def read_json(relative):
    return json.loads(path_in_results(relative).read_text(encoding="utf-8"))


def digest(relative):
    return hashlib.sha256(path_in_results(relative).read_bytes()).hexdigest()


def ratio(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def numeric_equal(actual, expected):
    """Validation arithmetic only; never used for keys, membership or flags."""
    if actual is None or expected is None:
        return actual is expected
    return math.isclose(float(actual), float(expected), rel_tol=1e-12, abs_tol=1e-12)


def raw_structure(record):
    """Build saved full-key/group locations directly, without P3 helpers."""
    O = sorted(set(record.get("sets", {}).get("observed_entities") or []))
    status = record["status"]
    out = {"O": O, "R": [], "n": len(O), "L": 0, "status": status,
           "keys": {}, "locations": {}, "blocks": [], "violations": [],
           "available": False}
    if status != "OK":
        return out
    blocks = record.get("blocks")
    if blocks is None:
        blocks = []
        last_tie = object()
        for row in record.get("entity_ranking") or []:
            key = tuple(float(x) for x in row["key"])
            tie = row["tie_group"]
            if blocks and tie == last_tie:
                if key != blocks[-1]["key"]:
                    out["violations"].append("same_tie_different_key")
                blocks[-1]["groups"][0].append(row["entity"])
            else:
                if blocks and key == blocks[-1]["key"]:
                    out["violations"].append("same_key_different_adjacent_tie")
                blocks.append({"key": key, "groups": [[row["entity"]]]})
            last_tie = tie
    else:
        blocks = [{"key": tuple(float(x) for x in b["key"]),
                   "groups": [list(g) for g in b["groups"]]} for b in blocks]
    for bi, block in enumerate(blocks):
        if not all(math.isfinite(x) for x in block["key"]):
            out["violations"].append("nonfinite_key")
        if bi and block["key"] > blocks[bi - 1]["key"]:
            out["violations"].append("ascending_block_key")
        if not block["groups"] or any(not g for g in block["groups"]):
            out["violations"].append("empty_block_or_group")
        for gi, group in enumerate(block["groups"]):
            for entity in group:
                out["R"].append(entity)
                out["keys"][entity] = block["key"]
                out["locations"][entity] = (bi, gi)
    out["blocks"] = blocks
    out["L"] = len(out["R"])
    if not 0 < out["L"] <= len(O):
        out["violations"].append("invalid_returned_size")
    if len(out["R"]) != len(set(out["R"])):
        out["violations"].append("duplicate_returned_entity")
    if not set(out["R"]).issubset(O):
        out["violations"].append("R_not_subset_O")
    out["available"] = not out["violations"]
    return out


def independent_topk(structure, ks=KS):
    """Enumerate block permutations, integrate group ties analytically.

    For ordinary rankings each key has one block; this reduces to uniform
    membership inside its exact full-key tie.  For TORAI, unequal-sized blocks
    move as complete blocks.  No interval-uniform approximation or saved
    probability is used.
    """
    if not structure["available"]:
        return None
    values = {k: {entity: Fraction(0) for entity in structure["O"]} for k in ks}
    blocks = structure["blocks"]
    prefix = 0
    for _, group_iterator in itertools.groupby(blocks, key=lambda b: b["key"]):
        group = list(group_iterator)
        sizes = [sum(map(len, b["groups"])) for b in group]
        denominator = factorial(len(group))
        for order in itertools.permutations(range(len(group))):
            position = prefix
            for index in order:
                block = group[index]
                for tie in block["groups"]:
                    for k in ks:
                        probability = Fraction(min(max(k - position, 0), len(tie)),
                                               len(tie) * denominator)
                        for entity in tie:
                            values[k][entity] += probability
                    position += len(tie)
        prefix += sum(sizes)
    return values


def independent_before(structure, root):
    if not structure["available"] or root not in structure["R"]:
        return None
    root_key = structure["keys"][root]
    root_block, root_group = structure["locations"][root]
    return [entity for entity in structure["R"] if entity != root and
            (structure["keys"][entity] > root_key or
             (structure["locations"][entity][0] == root_block and
              structure["locations"][entity][1] < root_group))]


def hypergeometric_p0(n, a, b):
    """Sum positive ancestor counts; independent of 1-combination-ratio code."""
    if n < 1 or not 0 <= a <= n - 1 or not 0 <= b <= n - 1:
        raise ValueError("invalid n/a/b")
    denominator = comb(n - 1, b)
    numerator = 0
    for h in range(1, min(a, b) + 1):
        other = b - h
        if other <= n - 1 - a:
            numerator += comb(a, h) * comb(n - 1 - a, other)
    return Fraction(numerator, denominator)


def independent_dice(left, right, p_left, p_right, k):
    if not left["available"] or not right["available"]:
        return None
    oi, oj = set(left["O"]), set(right["O"])
    mi, mj = min(k, left["L"]), min(k, right["L"])
    overlap = sum((p_left[k][e] * p_right[k][e] for e in oi & oj), Fraction(0))
    d = 2 * overlap / (mi + mj)
    d0 = Fraction(2 * mi * mj * len(oi & oj), len(oi) * len(oj) * (mi + mj))
    return {"D": d, "D0": d0, "delta": d - d0, "V": 1 - d}


class Audit:
    def __init__(self):
        self.checks = []

    def check(self, kind, actual, expected, sources, numeric=False, **context):
        passed = numeric_equal(actual, expected) if numeric else actual == expected
        self.checks.append({"kind": kind, "passed": passed, "actual": actual,
                            "expected": expected, "sources": sources, **context})


def merged(values):
    return True if True in values else None if None in values else False


def expected_assignment(flags, wrong):
    if not wrong:
        return {"primary": None, "multi": [], "applicable": False}
    labels = [m for m in ORDER if flags[m] is True]
    return {"primary": labels[0] if labels else "M0", "multi": labels or ["M0"],
            "applicable": True}


def root_local(record, row, seed):
    method, root = row["method"], row["root"]
    if record["status"] != "OK" or method in ("baro", "torai_B"):
        return None
    if method == "simplerca":
        keys = {r["entity"]: tuple(r["key"]) for r in record["entity_ranking"]}
        return keys[root][0] == 0 if root in keys else None
    if method == "circa_ols_da":
        nodes = record.get("diagnostics", {}).get("nodes")
        if nodes is None:
            return None
        scores = [v.get("rht_score") for metric, v in nodes.items()
                  if metric.split("_")[0] == root]
        if not scores or any(v is None or not math.isfinite(v) for v in scores):
            return None
        return all(v < 3 for v in scores)
    # Native span-statistic recomputation is the separate raw-data checker.
    # Here we check its saved local flag is propagated without altering meaning.
    return seed["local_nonpositive"]["value"]


def run_checks(run_id, audit):
    rel = "results/T-028/runs/" + run_id
    analysis_path, concentration_path = rel + "/ca-sai.json", rel + "/concentration.json"
    analysis, concentration = read_json(analysis_path), read_json(concentration_path)
    step1_path = "results/T-028/runs/danh-sach-001/step1.json"
    step1 = read_json(step1_path)
    frozen = read_json("results/T-028/runs/danh-sach-001/manifest.json")
    frozen_records = {item["path"]: item for item in frozen["source_records"]}
    previous = {(r["dataset"], r["method"], r["opaque_id"]): r for r in step1["main_rows"]}
    excluded = {x["opaque_id"] if isinstance(x, dict) else x
                for x in step1["circa_dev19_conditional"]["excluded_confirmed_rounding11"]}
    rows = analysis["main_rows"]
    records, structures, probabilities = {}, {}, {}
    groups = defaultdict(list)
    membership_samples, p0_samples, d_samples = [], [], []
    audit.check("main_row_identity_coverage",
                sorted((r["dataset"], r["method"], r["opaque_id"]) for r in rows),
                sorted(previous), [src(analysis_path, "/main_rows"), src(step1_path, "/main_rows")])
    for index, row in enumerate(rows):
        row_pointer = "/main_rows/" + str(index)
        row["_checker_pointer"] = row_pointer
        groups[(row["dataset"], row["method"])].append(row)
        prior = previous[(row["dataset"], row["method"], row["opaque_id"])]
        audit.check("saved_score_fields_unchanged",
                    {key: row[key] for key in prior if key not in ("evidence", "mechanisms", "analysis_state")},
                    {key: prior[key] for key in prior if key not in ("evidence", "mechanisms", "analysis_state")},
                    [src(analysis_path, row_pointer), src(step1_path, "/main_rows")])
        for sid, seed in row["evidence"]["seed_evidence"].items():
            seed_pointer = row_pointer + "/evidence/seed_evidence/" + pointer(sid)
            record_path = seed["source"]["path"]
            if record_path not in frozen_records:
                raise ValueError("record outside frozen step1 sources: " + record_path)
            audit.check("record_hash", digest(record_path), frozen_records[record_path]["sha256"],
                        [src(record_path), src("results/T-028/runs/danh-sach-001/manifest.json", "/source_records")])
            record = read_json(record_path)
            records[record_path] = record
            structure = raw_structure(record)
            structures[record_path] = structure
            probability = independent_topk(structure)
            probabilities[record_path] = probability
            sources = [src(analysis_path, seed_pointer), src(record_path)]
            ranking = seed["ranking"]
            for name in ("O", "R", "n", "L"):
                audit.check("membership_" + name, ranking[name], structure[name], sources)
            audit.check("ranking_availability", ranking["availability"] == "available", structure["available"], sources)
            if record["status"] == "OK":
                audit.check("native_full_keys", ranking["entity_keys"],
                            {e: list(k) for e, k in structure["keys"].items()}, sources)
                audit.check("ranking_invariant", structure["violations"], [], sources)
            before = independent_before(structure, row["root"])
            audit.check("certain_before", seed["certain_before_root"], before, sources)
            local = root_local(record, row, seed)
            audit.check("local_nonpositive_propagation", seed["local_nonpositive"]["value"], local, sources)
            for k in KS:
                actual = seed["by_k"][str(k)]
                hit = probability[k].get(row["root"], Fraction(0)) if probability is not None else Fraction(0)
                wrong = record["status"] == "OK" and hit < 1
                audit.check("wrong_OK_from_exact_tie", actual["wrong_OK"], wrong, sources, k=k)
                audit.check("seed_Hit_matches_exact_tie", row["seed_metrics"][sid]["hit@" + str(k)], float(hit), sources, numeric=True, k=k)
                if record["status"] != "OK":
                    flags = {m: None for m in ORDER}
                else:
                    relation = seed["caller_relation"]
                    ancestors = seed["ancestors"]["value"]
                    flag5 = None if ancestors is None or before is None else any(
                        relation.get(e, {}).get("path_to_root") is True for e in before)
                    flags = {"M1": row["root"] not in structure["O"],
                             "M2": row["root"] in structure["O"] and row["root"] not in structure["R"],
                             "M3": 0 < hit < 1,
                             "M4": row["method"] == "circa_ols_da" and row["opaque_id"] in excluded,
                             "M5": flag5, "M6": local}
                audit.check("seed_flags", {m: actual["flags"][m]["value"] for m in ORDER}, flags, sources, k=k)
                audit.check("seed_assignment", actual["assignment"], expected_assignment(flags, wrong), sources, k=k)
                if row["method"] == "tracerca" and flags["M6"] is True:
                    audit.check("TraceRCA_M6_implies_M2", flags["M2"], True, sources, k=k)
                if row["method"] == "simplerca" and flags["M6"] is True and k == 1:
                    audit.check("SimpleRCA_M6_implies_wrong_top1", wrong, True, sources)
                if flags["M5"] is True and k == 1:
                    audit.check("M5_implies_wrong_top1", wrong, True, sources)
        seeds = row["evidence"]["seed_evidence"]
        for k in KS:
            all_ok = [s["by_k"][str(k)]["flags"] for s in seeds.values() if s["status"] == "OK"]
            wrong_ok = [s["by_k"][str(k)]["flags"] for s in seeds.values() if s["by_k"][str(k)]["wrong_OK"]]
            base = {m: merged([f[m]["value"] for f in all_ok]) if all_ok else None for m in ORDER}
            explanation = {m: merged([f[m]["value"] for f in wrong_ok]) if wrong_ok else None for m in ORDER}
            mechanism = row["mechanisms"][str(k)]
            sources = [src(analysis_path, row_pointer + "/mechanisms/" + str(k)), src(analysis_path, row_pointer + "/evidence/seed_evidence")]
            audit.check("all_OK_seed_flag_merge", {m: mechanism["base_flags_all_OK_seeds"][m]["value"] for m in ORDER}, base, sources, k=k)
            audit.check("wrong_seed_flag_merge", {m: mechanism["explanation_flags_wrong_seeds"][m]["value"] for m in ORDER}, explanation, sources, k=k)
            audit.check("case_assignment", mechanism["assignment"], expected_assignment(explanation, row["wrong_OK_at_" + str(k)]), sources, k=k)
            for key, eligible in (("base_flags_all_OK_seeds", all_ok), ("explanation_flags_wrong_seeds", wrong_ok)):
                if not eligible:
                    continue
                for m in ORDER:
                    values = [f[m]["value"] for f in eligible]
                    flag = mechanism[key][m]
                    for field, expected in (("n_seed_true", values.count(True)), ("n_seed_NA", values.count(None)), ("n_seed_eligible", len(values))):
                        audit.check("seed_merge_" + field, flag[field], expected, sources, k=k, flag=m)

    concentration_lookup = {(p["dataset"], p["method"], p["k"], p["left"], p["right"]): (i, p)
                            for i, p in enumerate(concentration["case_pairs"])}
    for (dataset, method), cases in sorted(groups.items()):
        cases.sort(key=lambda row: row["opaque_id"])
        eligible = [row for row in cases if any(structures[s["source"]["path"]]["available"]
                                               for s in row["evidence"]["seed_evidence"].values())]
        selected = eligible[:3]
        selection = {"dataset": dataset, "method": method, "opaque_ids": [r["opaque_id"] for r in selected],
                     "availability": "available" if len(selected) == 3 else "N/A",
                     "reason": None if len(selected) == 3 else "fewer_than_three_eligible_cases"}
        membership_samples.append(selection)
        for row in selected:
            for sid, seed in row["evidence"]["seed_evidence"].items():
                path = seed["source"]["path"]
                expected = probabilities[path]
                sources = [src(path, "/blocks" if records[path].get("blocks") is not None else "/entity_ranking"),
                           src(analysis_path, row["_checker_pointer"] + "/evidence/seed_evidence/" + pointer(sid) + "/ranking")]
                if expected is None:
                    continue
                for k in KS:
                    audit.check("sample_topk_exact_probability", seed["ranking"]["p_by_k_exact"][str(k)],
                                {e: ratio(p) for e, p in expected[k].items()}, sources, k=k)
                    audit.check("sample_topk_mass", sum(expected[k].values()), min(k, structures[path]["L"]), sources, k=k)
        for left, right in itertools.combinations(selected, 2):
            for k in KS:
                outputs, combos = [], []
                for (sid_i, seed_i), (sid_j, seed_j) in itertools.product(left["evidence"]["seed_evidence"].items(), right["evidence"]["seed_evidence"].items()):
                    path_i, path_j = seed_i["source"]["path"], seed_j["source"]["path"]
                    expected = independent_dice(structures[path_i], structures[path_j], probabilities[path_i], probabilities[path_j], k)
                    if expected is not None:
                        outputs.append(expected)
                    combos.append({"seed_left": sid_i, "seed_right": sid_j, "availability": "available" if expected is not None else "N/A",
                                   "expected": {key: float(v) for key, v in expected.items()} if expected is not None else None,
                                   "sources": [src(path_i), src(path_j)]})
                ci, saved = concentration_lookup[(dataset, method, k, left["opaque_id"], right["opaque_id"])]
                sources = [src(concentration_path, "/case_pairs/" + str(ci)), src(analysis_path, left["_checker_pointer"]), src(analysis_path, right["_checker_pointer"])]
                audit.check("sample_D_seed_pair_count", saved["n_seed_pair_valid"], len(outputs), sources)
                for name in ("D", "D0", "delta", "V"):
                    expected = float(sum((o[name] for o in outputs), Fraction(0)) / len(outputs)) if outputs else None
                    audit.check("sample_D_" + name, saved[name], expected, sources, numeric=True, k=k)
                d_samples.append({"dataset": dataset, "method": method, "left": left["opaque_id"], "right": right["opaque_id"], "k": k, "seed_pairs": combos})

        for k in KS:
            eligible_p0 = []
            for row in cases:
                for seed in row["evidence"]["seed_evidence"].values():
                    st = structures[seed["source"]["path"]]
                    probability = probabilities[seed["source"]["path"]]
                    if (st["available"] and row["root"] in st["R"] and
                            probability[k].get(row["root"], Fraction(0)) < 1 and
                            seed["ancestors"]["value"] is not None):
                        eligible_p0.append(row)
                        break
            selection = {"dataset": dataset, "method": method, "k": k,
                         "opaque_ids": [r["opaque_id"] for r in eligible_p0[:3]],
                         "availability": "available" if len(eligible_p0) >= 3 else "N/A",
                         "reason": None if len(eligible_p0) >= 3 else "fewer_than_three_eligible_cases"}
            for row in eligible_p0[:3]:
                for sid, seed in row["evidence"]["seed_evidence"].items():
                    path = seed["source"]["path"]
                    st, probability = structures[path], probabilities[path]
                    saved = seed["by_k"][str(k)]["P0"]
                    if not (st["available"] and row["root"] in st["R"] and probability[k].get(row["root"], Fraction(0)) < 1 and seed["ancestors"]["value"] is not None):
                        continue
                    ancestors = {e for e, relrow in seed["caller_relation"].items() if relrow["path_to_root"] is True and e != row["root"]}
                    before = independent_before(st, row["root"])
                    n, a, b = st["n"], len(ancestors & (set(st["O"]) - {row["root"]})), len(before)
                    sources = [src(path, "/blocks" if records[path].get("blocks") is not None else "/entity_ranking"),
                               src(analysis_path, row["_checker_pointer"] + "/evidence/seed_evidence/" + pointer(sid))]
                    audit.check("sample_P0_ancestor_membership", sorted(seed["ancestors"]["value"]), sorted(ancestors), sources)
                    audit.check("sample_P0_availability", saved["availability"], "available", sources, k=k)
                    audit.check("sample_P0_parameters", {key: saved.get(key) for key in ("n", "a", "b")}, {"n": n, "a": a, "b": b}, sources, k=k)
                    audit.check("sample_P0_hypergeometric", saved["value"], float(hypergeometric_p0(n, a, b)), sources, numeric=True, k=k)
            p0_samples.append(selection)

    schema_path = "results/T-024/cham-a.json"
    frozen_input = frozen["inputs"]["re2_score"]
    audit.check("schema_input_hash", digest(schema_path), frozen_input["sha256"], [src(schema_path), src("results/T-028/runs/danh-sach-001/manifest.json", "/inputs/re2_score")])
    schema = schema_recount(read_json(schema_path)["raw_column_audit"], rows, audit, schema_path, analysis_path)
    return {"membership_and_tie_samples": membership_samples, "D_D0_samples": d_samples,
            "P0_samples": p0_samples, "schema_expected": schema,
            "input_sources": {analysis_path: digest(analysis_path), concentration_path: digest(concentration_path),
                              step1_path: digest(step1_path), schema_path: digest(schema_path)}}


def schema_kind(column):
    if column in ("time", "time.1"):
        return column
    suffix = column.rsplit("_", 1)[-1]
    return suffix if suffix in ("cpu", "mem", "diskio", "socket", "workload", "error", "latency-50", "latency-90") else "other"


def schema_recount(raw_audit, analysis_rows, audit, schema_path, analysis_path):
    by_case = raw_audit["by_case"]
    union = sorted(set().union(*(set(v["columns"]) for v in by_case.values())))
    source_union = src(schema_path, "/raw_column_audit/union_columns")
    audit.check("schema_union_columns", raw_audit["union_columns"], union, [source_union, src(schema_path, "/raw_column_audit/by_case")])
    audit.check("schema_union_n", raw_audit["union_n"], len(union), [source_union])
    labels = {row["opaque_id"]: row for row in analysis_rows if row["dataset"] == "RE2-TT"}
    output, cell_rows, root_cross, after_preprocess = [], [], [], []
    cells = defaultdict(list)
    for oid, value in sorted(by_case.items()):
        label = labels[oid]
        columns = set(value["columns"])
        missing = set(union) - columns
        sources = [src(schema_path, "/raw_column_audit/by_case/" + pointer(oid)), src(analysis_path, label["_checker_pointer"])]
        audit.check("schema_case_present_n", value["n_columns"], len(columns), sources)
        audit.check("schema_case_missing_n", value["n_missing"], len(missing), sources)
        audit.check("schema_case_missing_columns", sorted(value["missing_from_union"]), sorted(missing), sources)
        output.append({"opaque_id": oid, "cell": label["cell"], "fault": label["fault"], "root": label["root"],
                       "nhom_loi": label["nhom_loi"], "nhom_vi_tri_p75": label["nhom_vi_tri_p75"],
                       "present_n": len(columns), "missing_n": len(missing), "missing_columns": sorted(missing),
                       "present_by_kind": dict(Counter(schema_kind(c) for c in columns)),
                       "missing_by_kind": dict(Counter(schema_kind(c) for c in missing)), "sources": sources})
        cells[label["cell"]].append(oid)
        for column in union:
            if column.split("_")[0] == label["root"]:
                root_cross.append({"opaque_id": oid, "cell": label["cell"], "root": label["root"],
                                   "column": column, "kind": schema_kind(column), "present": column in columns,
                                   "sources": sources})
    for cell, oids in sorted(cells.items()):
        for column in union:
            present = sum(column in by_case[oid]["columns"] for oid in oids)
            cell_rows.append({"cell": cell, "column": column, "entity_native_mapping": column.split("_")[0],
                              "kind": schema_kind(column), "present_n": present, "missing_n": len(oids) - present,
                              "n_cases": len(oids), "sources": [src(schema_path, "/raw_column_audit/by_case"), source_union]})
    for row in analysis_rows:
        if row["dataset"] != "RE2-TT":
            continue
        for sid, seed in row["evidence"]["seed_evidence"].items():
            after_preprocess.append({"opaque_id": row["opaque_id"], "method": row["method"], "seed": sid,
                                     "O": seed["ranking"]["O"], "R": seed["ranking"]["R"],
                                     "L": seed["ranking"]["L"], "input_shape": seed["native_input_shape"],
                                     "sources": [src(analysis_path, row["_checker_pointer"] + "/evidence/seed_evidence/" + pointer(sid)), src(seed["source"]["path"], "/input_shape")]})
    return {"availability": "available", "union_n": len(union), "union_columns": union,
            "by_case": output, "by_cell_column": cell_rows, "schema_root_cross": root_cross,
            "method_sets_after_preprocessing": after_preprocess,
            "Nezha_raw_schema": {"availability": "N/A", "reason": "no_raw_column_audit_in_saved_source"}}


def json_safe(value):
    if isinstance(value, Fraction):
        return ratio(value)
    if isinstance(value, dict):
        return {key: json_safe(v) for key, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not args.run_id or Path(args.run_id).name != args.run_id or args.run_id in (".", ".."):
        raise ValueError("run-id must be one directory name")
    run = path_in_results("results/T-028/runs/" + args.run_id)
    output_path = run / "independent-ranking.json"
    if output_path.exists():
        raise FileExistsError("Preserve previous independent-ranking.json; do not overwrite")
    if not run.is_dir():
        raise FileNotFoundError(run)
    started = time.perf_counter()
    audit = Audit()
    result = {"task": "T-028", "run_id": args.run_id, "started_at": now(),
              "method_rerun": False, "raw_data_read": False,
              "selection_rule": "three_first_eligible_opaque_ids_in_each_dataset_method; keep_all_saved_seeds",
              "numeric_tolerance_validation_only": {"absolute": 1e-12, "relative": 1e-12}}
    error = None
    try:
        result.update(run_checks(args.run_id, audit))
    except BaseException as exc:
        error = exc
        result.update(error=repr(exc), traceback=traceback.format_exc())
    result.update(status="failed" if error or any(not c["passed"] for c in audit.checks) else "passed",
                  finished_at=now(), elapsed_s=time.perf_counter() - started,
                  n_checks=len(audit.checks), n_failed=sum(not c["passed"] for c in audit.checks), checks=audit.checks)
    output_path.write_text(json.dumps(json_safe(result), ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output_path), "status": result["status"], "n_checks": result["n_checks"],
                      "n_failed": result["n_failed"], "elapsed_s": result["elapsed_s"]}, ensure_ascii=False))
    if error:
        raise error
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
