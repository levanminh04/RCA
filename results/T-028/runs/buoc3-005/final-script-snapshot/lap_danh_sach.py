"""T-028 bước 1: trích số đã chấm, không chạy phương pháp hay tính bằng chứng.

Chạy từ repo: py -3 -B results/T-028/scripts/lap_danh_sach.py \
    --run-dir results/T-028/runs/danh-sach-001
Thư mục lượt phải chưa tồn tại. Mọi lượt lỗi được giữ tại thư mục đã tạo.
Chỉ đọc sáu JSON nguồn cố định và bản ghi kết quả đã có trong manifest.
"""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
SAIGON = timezone(timedelta(hours=7), "Asia/Saigon")
METHODS = ("baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B")
STATUSES = ("OK", "NO_EVIDENCE", "ERROR", "TIMEOUT", "UNSUPPORTED")
INPUTS = {
    "re2_score": "results/T-024/cham-a.json",
    "re2_manifest": "results/T-024/ban-ghi-dua-vao-cham.json",
    "re2_labels": "results/T-022/nhan-dev.json",
    "nezha_score": "results/T-026/cham-a.json",
    "nezha_manifest": "results/T-026/ban-ghi-dua-vao-cham.json",
    "nezha_labels": "results/T-026/nhan-dev.json",
}
# Tolerance chỉ kiểm tổng số thực đã lưu; không dùng để xác định hòa hay ca sai.
ABS_TOL = REL_TOL = 1e-10
EXPECTED_METHOD = {
    "baro": "baro", "simplerca": "simplerca", "microrank_full": "microrank",
    "tracerca": "tracerca", "circa_ols_da": "circa", "torai_B": "torai",
}
VARIANTS = {
    "RE2-TT": {"baro": "native", "simplerca": "native", "microrank_full": "full",
               "tracerca": "native", "circa_ols_da": "ols+rht_da", "torai_B": "B"},
    "Nezha-OB": {"baro": "native", "simplerca": "M4", "microrank_full": "full",
                 "tracerca": "finite", "circa_ols_da": "ols+rht_da", "torai_B": "B"},
}


def now():
    return datetime.now(SAIGON).isoformat(timespec="milliseconds")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("Khóa JSON trùng: " + key)
        out[key] = value
    return out


def write_json(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


class Extraction:
    def __init__(self, run_dir):
        self.run_dir = run_dir
        self.started = now()
        self.clock = time.perf_counter()
        self.inputs = {}
        self.records = {}
        self.checks = []
        self.progress("started", scope="step1_saved_scores_only")

    def progress(self, phase, **fields):
        event = {"timestamp_asia_saigon": now(),
                 "elapsed_s": round(time.perf_counter() - self.clock, 6),
                 "phase": phase, **fields}
        with (self.run_dir / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")

    def require(self, condition, name, **details):
        self.checks.append({"name": name, "passed": bool(condition), **details})
        if not condition:
            raise ValueError(name + ": " + str(details))

    def close(self, a, b):
        return math.isclose(a, b, rel_tol=REL_TOL, abs_tol=ABS_TOL)

    def load_input(self, name):
        relative = INPUTS[name]
        raw = (ROOT / relative).read_bytes()
        value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object)
        self.inputs[name] = {"path": relative, "sha256": digest(raw), "bytes": len(raw)}
        return value

    def load_record(self, metadata):
        relative = metadata["path"]
        # Manifest chỉ được dẫn tới bản ghi kết quả; không đọc telemetry hay locator của job.
        parts = PurePosixPath(relative).parts
        safe = (isinstance(relative, str) and "\\" not in relative
                and not PurePosixPath(relative).is_absolute()
                and not any(p in (".", "..") for p in relative.split("/"))
                and len(parts) > 3 and parts[0] == "results"
                and parts[1] in ("T-024", "T-026", "T-031")
                and parts[-1] == "ban-ghi-0.json")
        self.require(safe, "source_record_path_allowed", path=relative)
        path = (ROOT / relative).resolve()
        self.require(path.is_relative_to(ROOT / "results" / parts[1]),
                     "source_record_resolve_allowed", path=relative)
        if relative not in self.records:
            raw = path.read_bytes()
            record = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object)
            self.records[relative] = {"document": record, "path": relative,
                                      "sha256": digest(raw), "bytes": len(raw)}
        cached = self.records[relative]
        self.require(cached["sha256"] == metadata["sha256"],
                     "source_record_hash", path=relative)
        return cached["document"]

    def labels(self, doc, expected):
        cases = doc["cases"]
        labels = {row["opaque_id"]: row for row in cases}
        self.require(len(cases) == len(labels) == doc["so_ca"] == expected,
                     "labels_unique_and_count", expected=expected)
        return labels

    def manifest_index(self, rows):
        index = {row["path"]: row for row in rows}
        self.require(len(index) == len(rows), "manifest_source_paths_unique", n=len(rows))
        return index

    def value_checks(self, case, context):
        self.require(case["status"] in STATUSES, "saved_status_known", **context)
        for k in (1, 5):
            value = case[f"hit@{k}"]
            self.require(isinstance(value, (int, float)) and not isinstance(value, bool)
                         and math.isfinite(value) and 0 <= value <= 1,
                         "saved_hit_valid", k=k, **context)
        self.require(case["hit@1"] <= case["hit@5"], "saved_hit_monotone", **context)
        a, b = case["rank_min"], case["rank_max"]
        self.require((a is None and b is None) or
                     (type(a) is int and type(b) is int and 1 <= a <= b),
                     "saved_rank_bounds_valid", **context)
        if case["status"] != "OK":
            self.require(case["hit@1"] == case["hit@5"] == 0 and a is None and b is None,
                         "saved_nonOK_zero_and_null_rank", **context)

    def source_checks(self, dataset, method, oid, case, source_rows, manifest):
        expected_seeds = {0, 1, 2} if dataset == "RE2-TT" and method == "torai_B" else {None}
        self.require(len(source_rows) == len(expected_seeds)
                     and {row["seed"] for row in source_rows} == expected_seeds,
                     "source_seed_coverage", dataset=dataset, method=method, opaque_id=oid)
        paths, statuses = [], Counter()
        for source in sorted(source_rows, key=lambda x: -1 if x["seed"] is None else x["seed"]):
            path = source["path"]
            self.require(path in manifest, "source_in_frozen_manifest", path=path)
            frozen = manifest[path]
            identity = ("opaque_id", "method", "variant", "seed", "sha256")
            self.require(all(source[key] == frozen[key] for key in identity),
                         "score_source_matches_manifest", path=path)
            record = self.load_record(frozen)
            self.require(record["opaque_id"] == source["opaque_id"] == oid
                         and record["method"] == source["method"] == EXPECTED_METHOD[method]
                         and record["variant"] == source["variant"] == VARIANTS[dataset][method]
                         and record["seed"] == source["seed"] and record["mode"] == "a",
                         "source_record_identity_and_mode", path=path)
            seed_key = "single" if source["seed"] is None else str(source["seed"])
            if dataset == "RE2-TT":
                saved_seed = case["seed_metrics"][seed_key]
                self.value_checks(saved_seed, {"path": path, "seed_key": seed_key})
                self.require(saved_seed["status"] == record["status"],
                             "saved_seed_status_matches_record", path=path)
            else:
                self.require(case["status"] == record["status"],
                             "saved_case_status_matches_record", path=path)
                self.require(case["source_sha256"] == source["sha256"]
                             and case["source_view"] == source["source_view"],
                             "nezha_saved_source_matches_metadata", path=path)
            statuses[record["status"]] += 1
            paths.append({"path": path, "sha256": source["sha256"], "seed": source["seed"],
                          "status": record["status"], "method_status_raw": record.get("method_status_raw"),
                          "error": record.get("error")})
        if dataset == "RE2-TT":
            metrics = case["seed_metrics"]
            self.require(set(metrics) == {"single" if x is None else str(x) for x in expected_seeds},
                         "saved_seed_metric_coverage", method=method, opaque_id=oid)
            self.require(dict(statuses) == case["status_by_seed_counts"],
                         "saved_status_by_seed_counts", method=method, opaque_id=oid)
            for k in (1, 5):
                mean = math.fsum(v[f"hit@{k}"] for v in metrics.values()) / len(metrics)
                self.require(self.close(mean, case[f"hit@{k}"]), "saved_seed_mean_hit",
                             method=method, opaque_id=oid, k=k)
            self.require(set(case["source_paths"]) == {row["path"] for row in paths},
                         "saved_case_source_paths", method=method, opaque_id=oid)
            if len(statuses) == 1:
                self.require(case["status"] == next(iter(statuses)),
                             "saved_case_status_single_seed_status", method=method, opaque_id=oid)
        else:
            self.require(case["source_path"] == paths[0]["path"],
                         "saved_case_source_path", method=method, opaque_id=oid)
        return paths

    def extract_method(self, dataset, cohort, method, method_doc, case_ids, labels,
                       score_name, manifest, include_rows=True):
        cases = method_doc["per_case"]
        # RE2 dev19 is a subset of the same saved dev30 per_case document.
        self.require(set(case_ids) <= set(cases), "saved_case_coverage", dataset=dataset,
                     cohort=cohort, method=method, n=len(case_ids))
        self.require(set(cases) == set(labels), "saved_method_dev_coverage", dataset=dataset,
                     method=method, n=len(cases))
        by_case = {}
        for source in method_doc["source_records"]:
            by_case.setdefault(source["opaque_id"], []).append(source)
        self.require(set(by_case) == set(cases), "source_case_coverage", dataset=dataset, method=method)
        rows = []
        base_pointer = f"/methods/{method}/per_case" if dataset == "RE2-TT" else f"/tables/{cohort}/methods/{method}/per_case"
        label_name = "re2_labels" if dataset == "RE2-TT" else "nezha_labels"
        for oid in case_ids:
            case, label = cases[oid], labels[oid]
            context = {"dataset": dataset, "cohort": cohort, "method": method, "opaque_id": oid}
            self.value_checks(case, context)
            self.require(all(case["label"][key] == label[key]
                             for key in ("root", "fault", "cell", "nhom_vi_tri_p75")),
                         "saved_label_matches_label_file", **context)
            sources = self.source_checks(dataset, method, oid, case, by_case[oid], manifest)
            row = {**context, "status": case["status"], "rank_min": case["rank_min"],
                   "rank_max": case["rank_max"], "hit@1": case["hit@1"], "hit@5": case["hit@5"],
                   "wrong_OK_at_1": case["hit@1"] < 1 if case["status"] == "OK" else None,
                   "wrong_OK_at_5": case["hit@5"] < 1 if case["status"] == "OK" else None,
                   "root": label["root"], "fault": label["fault"], "cell": label["cell"],
                   "nhom_loi": label.get("nhom_loi"), "nhom_vi_tri_p75": label["nhom_vi_tri_p75"],
                   "analysis_state": "pending_codebook", "evidence": None, "mechanisms": None,
                   "ranking_quality_interpretation": "N/A_UNSUPPORTED" if case["status"] == "UNSUPPORTED" else
                       "OK_ranking" if case["status"] == "OK" else "non_OK_separate",
                   "source": {"score_path": INPUTS[score_name], "json_pointer": base_pointer + "/" + oid,
                              "labels_path": INPUTS[label_name], "label_opaque_id": oid,
                              "records": sources}}
            if dataset == "RE2-TT":
                row["seed_metrics"] = case["seed_metrics"]
                row["status_by_seed_counts"] = case["status_by_seed_counts"]
                row["rank_distribution_by_seed"] = case["rank_distribution_by_seed"]
            rows.append(row)
        summary_source = (method_doc["summaries"][cohort]["main"] if dataset == "RE2-TT"
                          else method_doc["summary"]["main"])
        pointer = (f"/methods/{method}/summaries/{cohort}/main" if dataset == "RE2-TT"
                   else f"/tables/{cohort}/methods/{method}/summary/main")
        summary = self.summarize(rows, summary_source, INPUTS[score_name], pointer)
        return rows if include_rows else [], summary

    def summarize(self, rows, saved, source_path, pointer):
        n = len(rows)
        statuses = {status: sum(row["status"] == status for row in rows) for status in STATUSES}
        self.require(n == saved["n"] and statuses == saved["trang_thai"],
                     "summary_count_and_status_matches", source=source_path, json_pointer=pointer)
        out = {"dataset": rows[0]["dataset"], "cohort": rows[0]["cohort"],
               "method": rows[0]["method"], "n_cases": n, "status_counts": statuses,
               "n_non_OK": n - statuses["OK"],
               "non_OK_by_status": {s: statuses[s] for s in STATUSES if s != "OK"},
               "source": {"path": source_path, "json_pointer": pointer}, "by_k": {}}
        for k in (1, 5):
            misses = math.fsum(1 - row[f"hit@{k}"] for row in rows)
            from_table = n * (1 - saved[f"hit@{k}"])
            ok = self.close(misses, from_table)
            self.require(ok, "expected_misses_matches_saved_table", source=source_path,
                         json_pointer=pointer, k=k, expected_misses_sum=misses,
                         n_times_one_minus_table_hit=from_table, abs_difference=abs(misses - from_table))
            out["by_k"][str(k)] = {
                "n_wrong_OK": sum(row["status"] == "OK" and row[f"hit@{k}"] < 1 for row in rows),
                "n_correct_OK": sum(row["status"] == "OK" and row[f"hit@{k}"] == 1 for row in rows),
                "wrong_OK_opaque_ids": [row["opaque_id"] for row in rows
                                        if row["status"] == "OK" and row[f"hit@{k}"] < 1],
                "expected_misses_including_non_OK": misses,
                "saved_table_hit": saved[f"hit@{k}"], "n_times_one_minus_saved_table_hit": from_table,
                "identity_validated": ok,
            }
        return out

    def extract(self):
        self.progress("read_fixed_inputs_started")
        docs = {name: self.load_input(name) for name in INPUTS}
        self.progress("read_fixed_inputs_finished", n_inputs=len(docs))
        re2, nezha = docs["re2_score"], docs["nezha_score"]
        re2_ids = re2["cohorts"]["dev30"]["case_ids"]
        nezha_ids = nezha["tables"]["main"]["case_ids"]
        re2_labels = self.labels(docs["re2_labels"], 30)
        nezha_labels = self.labels(docs["nezha_labels"], 22)
        self.require(len(re2_ids) == len(set(re2_ids)) == 30 and set(re2_ids) == set(re2_labels),
                     "RE2_dev30_exact_labels")
        self.require(len(nezha_ids) == len(set(nezha_ids)) == 22 and set(nezha_ids) == set(nezha_labels),
                     "Nezha_main22_exact_labels")
        self.require(set(re2["definitions"]["main_methods"]) == set(METHODS)
                     and set(nezha["definitions"]["primary_methods"]) == set(METHODS),
                     "six_primary_methods_match")
        re2_manifest = self.manifest_index(docs["re2_manifest"]["records"])
        nezha_manifest = self.manifest_index(docs["nezha_manifest"]["unique_records"])
        rows, summaries = [], []
        self.progress("extract_main_started")
        for dataset, cohort, method_docs, ids, labels, score_name, manifest in (
            ("RE2-TT", "dev30", re2["methods"], re2_ids, re2_labels, "re2_score", re2_manifest),
            ("Nezha-OB", "main", nezha["tables"]["main"]["methods"], nezha_ids,
             nezha_labels, "nezha_score", nezha_manifest),
        ):
            for method in METHODS:
                part, summary = self.extract_method(dataset, cohort, method, method_docs[method],
                                                     ids, labels, score_name, manifest)
                rows.extend(part)
                summaries.append(summary)
                self.progress("extract_main_method_finished", dataset=dataset, method=method, n=len(part))
        self.require(len(rows) == 312 and len({(r["dataset"], r["method"], r["opaque_id"]) for r in rows}) == 312,
                     "main312_unique_method_case_rows")
        self.progress("extract_circa_dev19_started")
        dev19 = re2["cohorts"]["dev19"]
        ids19, excluded = dev19["case_ids"], dev19["excluded_case_ids"]
        self.require(len(ids19) == len(set(ids19)) == 19 and len(excluded) == len(set(excluded)) == 11
                     and not set(ids19) & set(excluded) and set(ids19) | set(excluded) == set(re2_ids),
                     "CIRCA_dev19_and_excluded11_partition_dev30")
        conditional_rows, conditional_summary = self.extract_method(
            "RE2-TT", "dev19", "circa_ols_da", re2["methods"]["circa_ols_da"], ids19,
            re2_labels, "re2_score", re2_manifest)
        excluded_rows = [dict(row, conditional_group="excluded_confirmed_rounding11") for row in rows
                         if row["dataset"] == "RE2-TT" and row["method"] == "circa_ols_da"
                         and row["opaque_id"] in excluded]
        self.progress("extract_circa_dev19_finished", n=19, n_excluded=11)
        self.progress("extract_nezha_saved_sensitivity_started")
        flags = []
        baseline = {(r["method"], r["opaque_id"]): r for r in rows if r["dataset"] == "Nezha-OB"}
        for view in ("sensitivity_A", "sensitivity_B", "trace_guard"):
            table = nezha["tables"][view]
            view_ids = table["case_ids"]
            frozen_table = docs["nezha_manifest"]["tables"][view]
            self.require(len(view_ids) == len(set(view_ids)) == table["n_cases"]
                         and set(view_ids) == set(frozen_table["case_ids"]) and set(view_ids) <= set(nezha_ids),
                         "Nezha_saved_sensitivity_cohort", view=view)
            if view == "sensitivity_B":
                self.require(set(view_ids) == set(docs["nezha_labels"]["sensitivity_B_opaque_ids"]),
                             "Nezha_B_matches_label_cohort")
            table_manifest = self.manifest_index(frozen_table["records"])
            for method in METHODS:
                method_doc = table["methods"][method]
                cases = method_doc["per_case"]
                self.require(set(cases) == set(view_ids), "Nezha_sensitivity_method_coverage",
                             view=view, method=method)
                by_case = {}
                for source in method_doc["source_records"]:
                    by_case.setdefault(source["opaque_id"], []).append(source)
                self.require(set(by_case) == set(view_ids), "Nezha_sensitivity_source_coverage",
                             view=view, method=method)
                for oid in nezha_ids:
                    base = baseline[(method, oid)]
                    item = {"dataset": "Nezha-OB", "view": view, "method": method, "opaque_id": oid,
                            "main_status": base["status"], "main_hit@1": base["hit@1"],
                            "main_hit@5": base["hit@5"], "main_source": base["source"],
                            "evidence_computed": False, "mechanisms": None}
                    if oid not in cases:
                        item.update(cohort_state="not_in_cohort", status=None,
                                    **{"hit@1": None, "hit@5": None, "status_changed": None,
                                       "hit@1_changed": None, "hit@5_changed": None, "source": None})
                    else:
                        case = cases[oid]
                        self.value_checks(case, {"view": view, "method": method, "opaque_id": oid})
                        source_rows = by_case[oid]
                        for source in source_rows:
                            self.require(source["path"] in table_manifest and source == table_manifest[source["path"]],
                                         "sensitivity_source_matches_frozen_table", path=source["path"], view=view)
                        sources = self.source_checks("Nezha-OB", method, oid, case, source_rows, nezha_manifest)
                        item.update(cohort_state="included", status=case["status"],
                                    **{"hit@1": case["hit@1"], "hit@5": case["hit@5"],
                                       "status_changed": case["status"] != base["status"],
                                       "hit@1_changed": case["hit@1"] != base["hit@1"],
                                       "hit@5_changed": case["hit@5"] != base["hit@5"],
                                       "source": {"score_path": INPUTS["nezha_score"],
                                                  "json_pointer": f"/tables/{view}/methods/{method}/per_case/{oid}",
                                                  "records": sources}})
                    flags.append(item)
            self.progress("extract_nezha_saved_sensitivity_view_finished", view=view, n_cases=len(view_ids))
        self.require(len(flags) == 396, "Nezha_sensitivity_flags396_including_missing_cohort")
        return {"schema_version": 1, "task": "T-028", "step": 1,
                "analysis_state": "pending_codebook", "started_at_asia_saigon": self.started,
                "generated_at_asia_saigon": now(),
                "scope": "saved_scores_only_no_new_evidence_no_mechanism_assignment",
                "definitions": {"main_rows": "method × case; six methods per dataset",
                                "wrong_OK_at_k": "status == OK and saved expected Hit@k < 1; exact comparison",
                                "non_OK": "reported separately; saved Hit=0 remains in expected-miss denominator",
                                "expected_misses": "sum over cases of 1-saved Hit@k; TORAI saved seed mean per case",
                                "unsupported": "denominator rule only, not ranking-quality evidence",
                                "rank_bounds": "copied from saved score; null remains null",
                                "sensitivity": "saved status/Hit changes only; not_in_cohort is not a failure"},
                "primary_methods": list(METHODS), "main_rows": rows, "main_summaries": summaries,
                "circa_dev19_conditional": {"rows": conditional_rows, "summary": conditional_summary,
                                            "excluded_confirmed_rounding11": excluded_rows,
                                            "selection_source": {"path": INPUTS["re2_score"],
                                                                 "json_pointer": "/cohorts/dev19"}},
                "nezha_saved_sensitivity_flags": flags}

    def manifest(self, status):
        outputs = {}
        for name in ("step1.json", "validation.json", "progress.jsonl"):
            path = self.run_dir / name
            if path.is_file():
                raw = path.read_bytes()
                outputs[name] = {"sha256": digest(raw), "bytes": len(raw)}
        return {"schema_version": 1, "task": "T-028", "step": 1, "status": status,
                "started_at_asia_saigon": self.started, "finished_at_asia_saigon": now(),
                "elapsed_s": round(time.perf_counter() - self.clock, 6),
                "script": {"path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
                           "sha256": digest(Path(__file__).read_bytes())},
                "inputs": self.inputs,
                "source_records": [{key: value for key, value in record.items() if key != "document"}
                                   for _, record in sorted(self.records.items())],
                "outputs": outputs,
                "no_method_execution": True, "no_raw_data_read": True,
                "no_new_evidence_or_concentration_computed": True,
                "no_codebook_or_mechanism_assignment": True}

    def run(self):
        try:
            result = self.extract()
            self.progress("validation_finished", n_checks=len(self.checks), n_main_rows=len(result["main_rows"]))
            write_json(self.run_dir / "step1.json", result)
            write_json(self.run_dir / "validation.json", {
                "schema_version": 1, "status": "passed", "checked_at_asia_saigon": now(),
                "numeric_tolerance_for_validation_only": {"absolute": ABS_TOL, "relative": REL_TOL},
                "checks": self.checks})
            self.progress("finished", status="passed", n_main_rows=312,
                          n_source_records=len(self.records))
            write_json(self.run_dir / "manifest.json", self.manifest("passed"))
            print(json.dumps({"status": "passed", "run_dir": self.run_dir.relative_to(ROOT).as_posix(),
                              "n_main_rows": 312, "n_conditional_circa_rows": 19,
                              "n_nezha_sensitivity_flags": 396, "n_checks": len(self.checks),
                              "n_source_records": len(self.records)}, ensure_ascii=False))
            return 0
        except Exception as exc:
            error = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
            self.progress("failed", error=error)
            validation = self.run_dir / "validation.json"
            if not validation.exists():
                write_json(validation, {"schema_version": 1, "status": "failed",
                                        "checked_at_asia_saigon": now(), "error": error, "checks": self.checks})
            manifest = self.run_dir / "manifest.json"
            if not manifest.exists():
                write_json(manifest, self.manifest("failed"))
            print(json.dumps({"status": "failed", "run_dir": str(self.run_dir), "error": error},
                             ensure_ascii=False), file=sys.stderr)
            return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="results/T-028/runs/<id>; phải chưa tồn tại")
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    run_dir = (run_dir if run_dir.is_absolute() else ROOT / run_dir).resolve()
    base = (ROOT / "results" / "T-028" / "runs").resolve()
    if run_dir.parent != base or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}", run_dir.name):
        parser.error("--run-dir phải là thư mục con trực tiếp results/T-028/runs/<id>")
    try:
        run_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error("Lượt đã tồn tại; chọn run-id mới để giữ mọi lượt")
    return Extraction(run_dir).run()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
