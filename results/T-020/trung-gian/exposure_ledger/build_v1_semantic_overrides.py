"""Replay a manually read semantic audit. Read source prose; write only this lane."""
from pathlib import Path
import collections
import csv
import hashlib
import json
import time
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def main():
    started = time.perf_counter()
    plan = json.loads((BASE / "v1-semantic-review-plan.json").read_text(encoding="utf-8"))
    snapshot = BASE / "v1-review-input.csv"
    assert digest(snapshot.read_bytes()) == plan["input_sha256"]
    with snapshot.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == plan["rows"] == 877
    assert len({row["id"] for row in rows}) == len(rows)
    by_id = {row["id"]: row for row in rows}
    source_cache = {}

    def source_line(ref):
        path, raw_line = ref.rsplit(":", 1)
        assert path.startswith(("results/", "tasks/", "docs/")), ref
        assert "/locked/" not in path and not path.startswith("data/"), ref
        absolute = (ROOT / path).resolve()
        assert absolute.is_relative_to(ROOT.resolve()), ref
        if path not in source_cache:
            blob = absolute.read_bytes()
            source_cache[path] = {
                "path": path,
                "sha256": digest(blob),
                "bytes": len(blob),
                "lines": blob.decode("utf-8-sig", errors="replace").splitlines(),
            }
        line = int(raw_line)
        lines = source_cache[path]["lines"]
        assert 1 <= line <= len(lines), ref
        return lines[line - 1]

    for row in rows:
        assert source_line(row["nguon"]) == row["noi_dung"], row["id"]

    manual = {}
    for item in plan["plans"]:
        representative = by_id[item["representative_id"]]
        assert representative["nguon"] == item["source"]
        assert representative["noi_dung"] == item["content"]
        assert digest(item["content"].encode()) == item["content_sha256"]
        for ref in filter(None, item["evidence"].split(";")):
            source_line(ref)
        manual[item["content_sha256"]] = item

    overrides = []
    merged = []
    for row in rows:
        changed = dict(row)
        item = manual.get(digest(row["noi_dung"].encode()))
        if item and row["loai"] not in ("a", "b"):
            changed.update(loai=item["newclass"], trang_thai=item["newstatus"], the_quyet_dinh=item["card"])
            assert changed["loai"] in ("c", "d", "e")
            evidence = row["nguon"] + " — " + row["noi_dung"]
            if item["evidence"]:
                evidence += " | Đối chiếu: " + item["evidence"]
            evidence += " | Kiểm nội dung: " + item["newstatus"]
            overrides.append({
                "id": row["id"],
                "source": row["nguon"],
                "oldclass": row["loai"],
                "newclass": item["newclass"],
                "newstatus": item["newstatus"],
                "card": item["card"],
                "evidence": evidence,
            })
        merged.append(changed)

    gates = [row for row in rows if row["loai"] in ("a", "b")]
    assert len(gates) == 4
    assert all(row == next(x for x in merged if x["id"] == row["id"]) for row in gates)
    assert len({row["id"] for row in overrides}) == len(overrides)
    assert len(merged) == len(rows)
    assert sum(row["id"].startswith("G1-") and row["id"][3:].isdigit() for row in merged) == 533
    assert sum(row["id"].startswith("PENDING-") for row in merged) == 322
    assert sum(row["id"].startswith("STATE-") for row in merged) == 18
    for data in source_cache.values():
        assert digest((ROOT / data["path"]).read_bytes()) == data["sha256"], data["path"]

    target = BASE / "v1-semantic-overrides.csv"
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "source", "oldclass", "newclass", "newstatus", "card", "evidence"])
        writer.writeheader()
        writer.writerows(overrides)
    transitions = collections.Counter(row["oldclass"] + "→" + row["newclass"] for row in overrides)
    result = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.perf_counter() - started,
        "input_path": plan["input_path"],
        "input_sha256": plan["input_sha256"],
        "input_rows": len(rows),
        "manual_content_plans": len(manual),
        "override_rows": len(overrides),
        "retained_rows": len(rows) - len(overrides),
        "class_before": dict(collections.Counter(row["loai"] for row in rows)),
        "class_after_if_applied": dict(collections.Counter(row["loai"] for row in merged)),
        "transitions": dict(transitions),
        "sources": [{k: v for k, v in data.items() if k != "lines"} for data in source_cache.values()],
        "checks": {name: True for name in ["877_rows_preserved", "533_G1_matches_preserved", "322_pending_rows_preserved", "18_STATE_provenance_preserved", "4_gate_rows_unchanged", "all_source_lines_match", "citation_lines_exist", "all_sources_rehashed", "unique_override_ids", "no_root_final_write", "no_raw_locked_or_method_run"]},
        "coverage_meaning": "Source-line/count checks are mechanical; semantic decisions were manually read by exact content and captured in the review plan. Repeated content is expanded to every original occurrence, never by filename/task blanket.",
        "root_merge": "Match id and source, compare content to v1-review-input.csv; oldclass describes this frozen snapshot and can differ after root reruns classifier. Do not discard occurrence rows; preserve a/b gates. Reclassification does not select/approve policy.",
    }
    (BASE / "v1-semantic-assertions.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# T020 — audit ngữ nghĩa V1", "", "FACT: đọc 877 dòng theo nội dung nguồn; 510 nội dung c khác nhau được đọc theo nhóm exact-content, các occurrence vẫn giữ riêng. Các dòng e/d, STATE và bốn gate được kiểm riêng. Không phân loại blanket theo task/tên file.", "", f"Đầu vào snapshot: `{plan['input_path']}`; hash trong JSON. Có {len(overrides)} overrides và {len(rows)-len(overrides)} dòng giữ nguyên. Các override c→c thường sửa thẻ hoặc trạng thái, không phải thêm quyết định.", "", "Giữ nguyên 533 match G1, 322 paragraph pending, 18 provenance STATE và bốn gate a/b. Mọi dòng và citation đã kiểm exact source line; các file được đọc được rehash cuối lượt. Thời gian script chỉ là replay/assert, không phải toàn thời gian đọc ngữ nghĩa.", "", "Các điểm trọng yếu: T001 dataset không đóng cùng danh sách Q37/Q38; permission code không license là mệnh đề riêng OPEN. T015 variant/full-vs-top11/finite-tie/window vẫn G1 dù task đóng. Q55 ghi M4/WHY17 và đính chính nhưng không chọn P3. Q56 áp từng mục, E2 chuyển G1 và E6/D3 không áp. Q57 ghi WHY19/20 với trạng thái Đề xuất G1; không coi là lỗi chưa ghi common hoặc tự chọn window/seed từ context. Chi phí Q40/phạm vi bổ sung được ghi riêng, không biến thành D5.", "", "Tiêu đề, fences, câu lệnh, progress và số kiểm đã làm là tham chiếu/evidence; nháp common V9 có trạng thái pending/applied riêng. Việc P3/P4 kiểm tiếp không bị dùng để cấp quyền mở raw/locked trong T020.", "", "| Chuyển loại | Số occurrence |", "|---|---:|"]
    lines += [f"| {kind} | {count} |" for kind, count in sorted(transitions.items())]
    lines += ["", "OPEN/giới hạn: đây là đầu vào tự kiểm nội bộ để root đối chiếu độc lập, không thay Claude review; không chứng minh 533 coverage cơ học bằng 533 quyết định khoa học. Một dòng có nhiều mệnh đề giữ trạng thái hỗn hợp và card liên quan; các thao tác common/quyền chi phí nằm trong evidence riêng. Không chọn baseline/dataset/split/label/window/retrieval hoặc thêm gate.", "", "Tái lập bằng `py -3 -X utf8 results/T-020/trung-gian/exposure_ledger/build_v1_semantic_overrides.py`. Script chỉ đọc prose/snapshot/citation và ghi trong luồng này. Root hợp nhất theo id+source, kiểm nội dung gốc trong snapshot; không dựa oldclass sau rerun classifier."]
    (BASE / "v1-semantic-audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("sources", "root_merge", "coverage_meaning")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
