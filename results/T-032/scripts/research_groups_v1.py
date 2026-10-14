"""T-032: assemble checked metadata; never import a ranker or read raw telemetry."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/T-032"
CHECKS: list[dict] = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def checked(path: Path, expected: str, authority: str):
    digest = sha(path)
    CHECKS.append({"path": rel(path), "sha256": digest, "expected": expected,
                   "authority": authority, "passed": digest == expected})
    if digest != expected:
        raise ValueError(f"Source hash drift: {rel(path)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_ref(path: Path, pointer: str = ""):
    return {"path": rel(path), "json_pointer": pointer, "sha256": sha(path)}


def validate_sources():
    group_dir = OUT / "runs/groups-003"
    gm = json.loads((group_dir / "manifest.json").read_text(encoding="utf-8"))
    groups = {item["path"]: checked(group_dir / item["path"], item["sha256"],
                                      rel(group_dir / "manifest.json") + "#/outputs")
              for item in gm["outputs"]}
    source_manifest = ROOT / "results/T-028/runs/phan-hoi-review-001/manifest.json"
    source_manifest_pin = next(x["sha256"] for x in gm["inputs"]
                               if x["path"] == rel(source_manifest))
    sm = checked(source_manifest, source_manifest_pin,
                 rel(group_dir / "manifest.json") + "#/inputs")
    source_rows_path = source_manifest.parent / "ca-sai.json"
    source_rows_pin = next(x["sha256"] for x in sm["outputs"] if x["path"] == rel(source_rows_path))
    source_rows = checked(source_rows_path, source_rows_pin, rel(source_manifest) + "#/outputs")
    return gm, groups, source_rows


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def locked_groups():
    gm, source, _ = validate_sources()
    units = source["unit-universe.json"]["units"]
    by_id = {u["unit_id"]: u for u in units}
    assert len(by_id) == len(units) == 372
    unit_positions = {u["unit_id"]: i for i, u in enumerate(units)}
    mandatory_keys = {u["unit_id"]: canonical(u["mandatory_conditions"]) for u in units}
    equivalence_keys = {u["unit_id"]: canonical({"mandatory": u["mandatory_conditions"],
                                               "preferred": u["preferred_conditions"],
                                               "seed_key": u["seed_key"]}) for u in units}
    pins = {item["path"]: item["sha256"] for item in gm["inputs"]}
    for unit in units:
        p = ROOT / unit["source"]["path"]
        checked(p, pins[rel(p)], "results/T-032/runs/groups-003/manifest.json#/inputs")
    wrong_ids = {unit_id for group in source["catalog.json"]["groups"]
                 for unit_id in group["candidate_wrong_unit_ids"]}
    selected_correct: set[str] = set()
    pairs = []
    for original in source["counterpart-candidates.json"]["pairs"]:
        wrong = by_id[original["wrong_unit_id"]]
        classes: dict[str, list[dict]] = {}
        for candidate in original["eligible_candidates"]:
            control = by_id[candidate["unit_id"]]
            assert mandatory_keys[wrong["unit_id"]] == mandatory_keys[control["unit_id"]]
            assert not control["by_k"][str(original["k"])]["wrong_OK"]
            assert control["status"] == "OK"
            # A seed is retained as a separate unit even when saved metadata happen to match.
            key = equivalence_keys[control["unit_id"]]
            classes.setdefault(key, []).append(candidate)
        class_rows = []
        wrong_channels = wrong["preferred_conditions"]["method_inputs"].get("channels_consumed_by_method")
        for key, members in classes.items():
            members = sorted(members, key=lambda x: (by_id[x["unit_id"]]["opaque_id"], x["unit_id"]))
            chosen = members[0]
            control = by_id[chosen["unit_id"]]
            same_channels = wrong_channels == control["preferred_conditions"]["method_inputs"].get("channels_consumed_by_method")
            class_rows.append({
                "class_id": hashlib.sha256(key.encode("utf-8")).hexdigest(),
                "selected_correct_unit_id": chosen["unit_id"],
                "same_cell": wrong["cell"] == control["cell"],
                "same_channels": same_channels,
                "same_seed_key": wrong["seed_key"] == control["seed_key"],
                "equivalent_saved_metadata_member_ids": [x["unit_id"] for x in members],
                "equivalence_scope": "Mandatory + full saved preferred metadata + seed_key exact; actual runtime paths remain separately to inspect.",
                "wrong_condition_source": {"path": "results/T-032/runs/groups-003/unit-universe.json",
                                           "json_pointer": f"/units/{unit_positions[wrong['unit_id']]}/preferred_conditions"},
                "correct_condition_source": {"path": "results/T-032/runs/groups-003/unit-universe.json",
                                             "json_pointer": f"/units/{unit_positions[control['unit_id']]}/preferred_conditions"},
                "source": control["source"],
                "source_sha256": pins[control["source"]["path"]],
                "condition_difference_summary": {
                    "saved_metadata_equal_to_wrong": chosen["saved_preferred_metadata_equal"],
                    "difference_count": chosen["difference_count"],
                    "first_differences": chosen["first_differences"],
                    "interpretation": "Descriptive differences only; no distance, cutoff, nearest selection or inference of matching runtime paths.",
                },
                "reading_status": "chưa diễn giải",
            })
            selected_correct.add(chosen["unit_id"])
        # Same cell and channel are preferences, not exclusions. Keep every distinct class.
        class_rows.sort(key=lambda x: (not x["same_cell"], not x["same_channels"],
                                       by_id[x["selected_correct_unit_id"]]["opaque_id"],
                                       x["selected_correct_unit_id"]))
        pairs.append({
            "wrong_unit_id": original["wrong_unit_id"], "k": original["k"],
            "group_ids": original["group_ids"],
            "selection_status": "locked_all_distinct_saved_condition_classes" if class_rows else "no_correct_control_in_frozen_cohort",
            "mandatory_conditions": wrong["mandatory_conditions"],
            "target_step": ({"baro": "median/IQR -> robust-z -> metric max per service",
                             "simplerca": "metric/trace/log evidence -> per-channel votes -> service score"}.get(
                                 wrong["method"], "Lần theo bước native tương ứng sau khi lõi phương pháp được kiểm")),
            "target_property_may_differ": True,
            "control_classes": class_rows,
            "same_cell_class_count": sum(x["same_cell"] for x in class_rows),
            "same_channel_class_count": sum(x["same_channels"] for x in class_rows),
            "reading_status": "chưa đọc",
            "missing_control_reason": (None if class_rows else
                                      "Không có bản ghi OK đúng tại k cùng dataset/config/F/adapter trong tập nguồn; không thay bằng phương pháp khác."),
            "scope_of_absence": "frozen authorized cohort only",
            "cross_method_control_substitution": False,
        })
    selected_ids = wrong_ids | selected_correct
    locked_units = []
    for index, unit in enumerate(units):
        roles = []
        if unit["unit_id"] in wrong_ids:
            roles.append("wrong_or_non_OK")
        if unit["unit_id"] in selected_correct:
            roles.append("correct_control")
        locked_units.append({
            "unit_id": unit["unit_id"], "dataset": unit["dataset"], "method": unit["method"],
            "opaque_id": unit["opaque_id"], "seed": unit["seed"], "seed_key": unit["seed_key"],
            "configuration": unit["configuration"], "status": unit["status"], "cell": unit["cell"],
            "selected_for_manual_reading": bool(roles), "roles": roles,
            "source": unit["source"], "source_sha256": pins[unit["source"]["path"]],
            "source_row": unit["source_row"], "source_seed": unit["source_seed"],
            "metadata_source": {"path": "results/T-032/runs/groups-003/unit-universe.json",
                                "json_pointer": f"/units/{index}"},
            "groups": unit["groups"],
            "reading_status": "chưa đọc",
            "phase": ("BARO/SimpleRCA lõi đủ52; sẵn cho lần theo có đối chứng" if unit["method"] in ["baro", "simplerca"]
                      else "Giữ nguyên nhóm; chưa đọc trong chặng BARO/SimpleRCA, lõi phương pháp chưa đủ"),
            "runtime_path_status": "chưa xác lập theo bước; giữ seed riêng và mở rộng đọc khi tìm thấy nhánh mới",
            "mechanism_established": False,
        })
    groups = []
    for original in source["catalog.json"]["groups"]:
        ids = original["candidate_wrong_unit_ids"]
        assert ids and set(ids) <= wrong_ids
        selected_pairs = [i for i, pair in enumerate(pairs) if original["group_id"] in pair["group_ids"]]
        groups.append({
            "group_id": original["group_id"], "dataset": original["dataset"], "method": original["method"],
            "k": original["k"], "flag_or_status": original["flag_or_status"],
            "configuration": original["configuration"], "source_rows": original["source_rows"],
            "n_source_cases": original["n_source_cases"],
            "selected_wrong_unit_ids": ids,
            "pair_pointers": [f"/counterpart_pairs/{i}" for i in selected_pairs],
            "selection_status": "locked_all_source_wrong_units",
            "reading_status": "chưa đọc", "mechanism_established": False,
            "coverage_after_reading": "Chưa xác nhận; lựa chọn không thay chuỗi bằng chứng/đối chứng, không suy mọi ca từ một đại diện.",
        })
    result = {
        "task": "T-032", "status": "CATALOG_AND_READING_SELECTION_LOCKED_RESEARCH_PENDING",
        "catalog_locked": True, "manual_sample_locked": True,
        "runtime_path_coverage_locked": False,
        "lock_scope": "Khóa mọi nhóm/đơn vị sai nguồn và đại diện mọi lớp điều kiện đã lưu; chưa khóa đường xử lý chưa đọc hoặc kết luận cơ chế.",
        "selection_rule": {
            "mandatory": "Cùng dataset, cấu hình, quy tắc F và adapter; kiểm theo mandatory_conditions đã có nguồn hash.",
            "preferred": "Đọc samecell trước, rồi samechannels; mọi lớp scale/coverage khác nhau vẫn giữ thành đối chứng riêng.",
            "equivalence": "Chỉ gộp control khi full saved preferred/mandatory metadata và seed_key bằng nhau; opaque_id nhỏ nhất trong lớp này.",
            "no_equivalence_claim": "Metadata bằng nhau không chứng minh trung gian/đường native bằng nhau; nếu khác khi đọc thì tách lớp và giữ lượt trước.",
            "wrong_selection": "Giữ mọi wrong/non-OK unit nguồn; không giảm mẫu để vừa phiên.",
            "forbidden_inputs": ["chênh điểm", "caller đứng trên root", "kết quả can thiệp", "ngưỡng tương đồng tự đặt"],
            "target_property": "Thuộc tính đang phân xử có thể khác; không ép ca đúng mang cờ chỉ có ở ca sai.",
            "seed": "Mọi seed giữ riêng; không suy tương đương seed từ số cuối hay metadata.",
        },
        "counts": {
            "n_groups": len(groups), "n_source_seed_units": len(units),
            "n_wrong_or_non_OK_units": len(wrong_ids),
            "n_selected_correct_control_units": len(selected_correct),
            "n_selected_unique_units": len(selected_ids),
            "n_counterpart_requests": len(pairs),
            "n_control_class_links": sum(len(x["control_classes"]) for x in pairs),
            "n_requests_without_correct_control": sum(not x["control_classes"] for x in pairs),
            "ready_phase_unique_units": sum(x["unit_id"] in selected_ids and x["method"] in ["baro", "simplerca"] for x in units),
            "groups_by_method": dict(Counter(x["method"] for x in groups)),
            "selected_units_by_method": dict(Counter(x["method"] for x in units if x["unit_id"] in selected_ids)),
        },
        "groups": groups, "units": locked_units, "counterpart_pairs": pairs,
        "reading_plan": {
            "ready_methods": ["baro", "simplerca"],
            "order": "Trong mỗi phương pháp: nhóm bắt buộc M5 cùng nhóm sai khác; mỗi cặp đọc samecell/channels trước, giữ đối chứng khác điều kiện riêng.",
            "what_to_record": "Đầu vào -> lọc/bước tính -> trung gian -> thành phần điểm/max -> hạng/hòa; so đúng/sai và giải thích cạnh tranh.",
            "additional_paths": "Bảng toàn bộ và mọi seed giữ lại; nhánh mới/ phản ví dụ phát hiện khi đọc phải có unit bổ sung, không tự suy tính đồng nhất.",
            "completion_is_not_selection": "Nhóm được khóa chưa đồng nghĩa đã đọc hoặc đã trả lời RQ2.",
        },
        "source_hash_checks": CHECKS,
        "preserved_sensitivity_sources": source["selection-open.json"]["preserved_sensitivity_sources"],
        "raw_read": False, "method_executed": False,
    }
    write_json(OUT / "bao-phu-nhom.json", result)
    write_json(OUT / "runs/research-004/group-selection-assembly.json", {
        "status": "PASS", "script_sha256": sha(Path(__file__)),
        "outputs": [{"path": "results/T-032/bao-phu-nhom.json", "sha256": sha(OUT / "bao-phu-nhom.json")}],
        "source_hash_checks": CHECKS, "counts": result["counts"],
        "manual_reading_done": False, "raw_read": False, "method_executed": False,
    })
    print(json.dumps({"status": "PASS", "counts": result["counts"]}, ensure_ascii=False))


def capability():
    validate_sources()
    archive_dir = OUT / "runs/thu-ec2-003/coverage-export-001"
    transport = json.loads((OUT / "runs/thu-ec2-003/transport-check.json").read_text(encoding="utf-8"))
    tr = next(x for x in transport["stages"] if x["stage"] == "coverage-export-001")
    inventory_path = archive_dir / "file-inventory.json"
    inventory = checked(inventory_path, tr["inventory_sha256"],
                        "results/T-032/runs/thu-ec2-003/transport-check.json#/stages/1")
    archive_path = archive_dir / "coverage-verified.tar.gz"
    digest = sha(archive_path)
    assert digest == tr["archive_sha256"], "Coverage archive drift"
    CHECKS.append({"path": rel(archive_path), "sha256": digest,
                   "expected": tr["archive_sha256"], "passed": True,
                   "authority": "results/T-032/runs/thu-ec2-003/transport-check.json#/stages/1"})
    base = OUT / "runs/thu-ec2-003/verified"
    for item in inventory["files"]:
        p = base / item["path"]
        digest = sha(p)
        assert digest == item["sha256"] and p.stat().st_size == item["bytes"], rel(p)
        CHECKS.append({"path": rel(p), "sha256": digest, "expected": item["sha256"],
                       "bytes": p.stat().st_size, "passed": True,
                       "authority": rel(inventory_path) + "#/files"})
    records: dict[tuple[str, str], tuple[Path, dict]] = {}
    for stage in ["trace-coverage-re2-first-001", "trace-coverage-nezha-first-001", "trace-coverage-batch-001"]:
        directory = base / "runs" / stage
        mpath = directory / "manifest.json"
        m = json.loads(mpath.read_text(encoding="utf-8"))
        assert m["status"] == "PASS_OBSERVATION_AUDIT_ONLY", stage
        for item in m["outputs"]:
            if "dataset" not in item or "opaque_id" not in item:
                continue
            p = directory / item["path"]
            d = checked(p, item["sha256"], rel(mpath) + "#/outputs")
            key = d["dataset"], d["opaque_id"]
            assert key not in records, f"Duplicate case {key}"
            assert all(x["passed"] for x in d["frozen_method_facing_count_checks"].values()), key
            records[key] = p, d
    assert Counter(ds for ds, _ in records) == {"RE2-TT": 30, "Nezha-OB": 22}
    rows = []
    for (dataset, oid), (p, d) in sorted(records.items()):
        raw_fields = sorted({x["name"] for fields in d["schemas"].values() for x in fields})
        f = d["profiles"]["main/F"]
        counts = f["counts"]
        geom_n = counts.get("geometry_edge_keys", 0)
        partial = geom_n > 0
        missing = {
            "span_kind_and_synchronous_async_semantics": {
                "status": "not_recorded_in_raw_schema",
                "observed_absent_fields": [name for name in ["SpanKind", "spanKind", "kind", "attributes", "events"]
                                           if name not in raw_fields],
                "source": source_ref(p, "/schemas"),
                "why": "Quan hệ parent và interval không xác nhận caller đang await/blocking trên root.",
            },
            "explicit_await_start_end_or_blocking_state": {
                "status": "no_explicit_wait_interval_in_checked_schema",
                "source": source_ref(p, "/schemas"),
                "why": "Không tách được xử lý caller, chờ đồng bộ và tác vụ song song từ Duration riêng lẻ.",
            },
            "complete_sampling_or_loss_denominator": {
                "status": "not_established_by_authorized_source_set",
                "source": source_ref(p, "/definitions/coverage_limit"),
                "why": "Đã đếm span có trong file; chưa biết số span/request thực sự phát sinh hay bị mất.",
            },
            "cross_host_clock_error_bound": {
                "status": "not_established",
                "source": source_ref(p, "/definitions/clock_limit"),
                "why": "Thứ tự và độ dài dùng timestamp ghi lại; chưa có cận lỗi đồng hồ giữa host.",
            },
            "instrumentation_revision_and_exporter_lineage": {
                "status": "not_identified_in_case_payload",
                "source": source_ref(p, "/wait_capability/needed"),
                "why": "Cần nguồn instrumentation để biết span mô tả client/server/task gì và trường nào bị mất trước corpus.",
            },
        }
        row = {
            "dataset": dataset, "opaque_id": oid,
            "capability": "đo được một phần" if partial else "không đo được",
            "question": "Phân biệt caller chờ root với xử lý tại caller/async/thiếu span trong cửa sổ F",
            "classification_reason": (
                "Có quan hệ cùng trace và interval đã kiểm để đo chồng lấn quan sát; thiếu semantics chờ, sampling và cận clock."
                if partial else "Không có cạnh parent-child hợp lệ cho geometry trong F; các thiếu semantics/clock vẫn còn."),
            "raw_schema": d["schemas"],
            "raw_field_nonempty_row_counts": d["raw_field_nonempty_row_counts"],
            "raw_source_counts": d["profiles"]["raw_source"]["counts"],
            "F_counts": counts,
            "F_parent_resolution_rows": f["parent_resolution_rows"],
            "F_interval_statistics": f["interval_statistics"],
            "scope_counts": {name: profile["counts"] for name, profile in d["profiles"].items()},
            "observed_services_in_F": f["observed_services"],
            "raw_integrity_and_units": {
                "duplicate_identical_raw_rows": d["duplicate_identical_raw_rows"],
                "conflicting_raw_rows": d["conflicting_raw_rows"],
                "conflict_unique_keys": d["conflict_unique_keys"],
                "raw_checks": d["raw_checks"],
                "precision_residual_ns": d["precision_residual_ns"],
                "source_unit": d["definitions"]["source_unit"],
            },
            "adapter_and_method_payload": d["payload_field_contract"],
            "method_facing_counts_exact": d["frozen_method_facing_count_checks"],
            "frozen_window_source": d["frozen_F_source"],
            "frozen_count_source": d["frozen_count_source"],
            "missing_for_wait_inference": missing,
            "additional_observation_required": {
                "instrumentation": "Ghi mốc await/blocking hoặc xác minh semantics đồng bộ theo operation/span; giữ IDs và liên kết parent.",
                "clock_and_collection": "Cận lỗi đồng hồ giữa host, sampling policy và bộ đếm spans/requests phát sinh/mất.",
                "validation": "Đối chiếu interval chờ đo trực tiếp với trace dưới ca sync, async và span thiếu được biết.",
                "historical_limit": "Collector không khôi phục mốc chờ/semantics chưa từng được instrumentation ghi.",
            },
            "not_inferred": ["thời gian chờ", "self-time", "nguyên nhân vật lý", "nhãn/tỷ lệ lan", "lợi ích đồ thị"],
            "source": source_ref(p),
            "relevant_pointers": ["/schemas", "/profiles/main~1F", "/profiles/raw_source", "/payload_field_contract", "/definitions", "/wait_capability"],
        }
        rows.append(row)
    by_dataset = {}
    for dataset in ["RE2-TT", "Nezha-OB"]:
        cases = [x for x in rows if x["dataset"] == dataset]
        by_dataset[dataset] = {
            "denominator": len(cases),
            "capability_counts": dict(Counter(x["capability"] for x in cases)),
            "wait_cause_established": 0,
            "schema_sets": sorted({tuple(sorted({field["name"] for fields in x["raw_schema"].values()
                                                   for field in fields})) for x in cases}),
            "scope": "Toàn dev allowlist; capability thuộc câu hỏi chờ, không đánh giá chất lượng trace cho mọi bài toán.",
        }
    result = {
        "task": "T-032", "status": "CHECKED_OBSERVABILITY_PARTIAL_PHYSICAL_WAIT_OPEN",
        "assembly": "Metadata/JSON đã đo trên EC2; không parse raw, không tính ranker, không thêm ngưỡng.",
        "definitions": {
            "đo được": "Cần semantics/interval chờ đồng bộ và clock/coverage đủ để phân biệt các giải thích.",
            "đo được một phần": "Có quan hệ/interval hợp lệ; chỉ đo chồng lấn và coverage của phần đã quan sát.",
            "không đo được": "Thiếu relation/interval hợp lệ cho câu hỏi trong phạm vi tương ứng.",
            "union": "Hợp interval con trực tiếp đã resolve và clip vào interval cha; không gọi wait hoặc self-time.",
            "denominator": "Đếm ca trong allowlist; mỗi ca một dòng, không cộng span/cờ chồng lấn thành nguyên nhân.",
        },
        "by_dataset": by_dataset, "cases": rows,
        "source_hash_checks": CHECKS,
        "research_consequences": {
            "physical_caller_root_wait": "OPEN: không đủ semantics/await/clock/sampling để quy duration cho chờ root.",
            "computational_mechanism": "Có thể lần theo metric/vote/score và tín hiệu trace phương pháp nhận; capability không thay kiểm chuỗi/đối chứng.",
            "P9a": "Phân biệt yêu cầu instrumentation, clock và collection như trong mỗi ca; chưa chứng minh bổ sung trường sẽ tăng accuracy.",
        },
    }
    write_json(OUT / "kha-nang-do-trace.json", result)
    receipt = {"status": "PASS", "raw_read": False, "method_executed": False,
               "n_cases": len(rows), "by_dataset": by_dataset,
               "source_hash_checks": CHECKS,
               "outputs": [{"path": "results/T-032/kha-nang-do-trace.json",
                            "sha256": sha(OUT / "kha-nang-do-trace.json")} ]}
    write_json(OUT / "runs/research-004/trace-capability-assembly.json", receipt)
    print(json.dumps({"status": "PASS", "n_cases": len(rows), "by_dataset": by_dataset}, ensure_ascii=False))


if __name__ == "__main__":
    capability()
    CHECKS.clear()
    locked_groups()
