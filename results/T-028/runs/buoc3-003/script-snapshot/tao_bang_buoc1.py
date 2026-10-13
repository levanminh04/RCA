"""Chỉ trình bày số bước 1 đã lưu, không đọc raw hoặc tính đặc trưng P4."""
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
REL = "results/T-028/runs/danh-sach-001/step1.json"


def fmt(value):
    return str(int(value)) if float(value).is_integer() else f"{value:.6f}"


def source(summary):
    s = summary["source"]
    return f'`{s["path"]}` `{s["json_pointer"]}`'


def main():
    doc = json.loads((ROOT / REL).read_text(encoding="utf-8"))
    out = [
        "# Danh sách ca sai — bước 1 T-028",
        "",
        f"Chỉ trích số đã chấm; nguồn tổng hợp: `{REL}`. Không tính đặc trưng hoặc gán cơ chế.",
        "",
        "Ca sai OK@k: status OK và Hit@k kỳ vọng <1. Non-OK báo riêng. Mức trượt kỳ vọng gồm non-OK có Hit=0, không phải số ca sai. TORAI gộp seed theo ca. Số thập phân trong bảng làm tròn sáu chữ số; JSON giữ số nguồn.",
        "",
        "## Bảng chính",
        "",
        "| Dataset | Phương pháp | Tổng ca | OK sai@1 | OK sai@5 | Non-OK | Mức trượt@1 | @5 | Nguồn |",
        "|---|---|---:|---:|---:|---|---:|---:|---|",
    ]
    for s in doc["main_summaries"]:
        counts = "; ".join(f"{n} {st}" for st, n in s["non_OK_by_status"].items() if n) or "0"
        a, b = s["by_k"]["1"], s["by_k"]["5"]
        out.append(f'| {s["dataset"]} | {s["method"]} | {s["n_cases"]} | {a["n_wrong_OK"]} | {b["n_wrong_OK"]} | {counts} | {fmt(a["expected_misses_including_non_OK"])} | {fmt(b["expected_misses_including_non_OK"])} | {source(s)} |')
    out += ["", "CIRCA/TORAI Nezha UNSUPPORTED: chỉ giữ trạng thái và quy tắc mẫu số nguồn, không là kết quả chất lượng xếp hạng hoặc bằng chứng thiếu tín hiệu root.", "", "## Mã ca sai OK và non-OK", ""]
    for s in doc["main_summaries"]:
        out += [f'### {s["dataset"]} — {s["method"]}', "", f'Nguồn: {source(s)}; từng bản ghi/seed và exception ở `main_rows` của `{REL}`.', ""]
        for k in ("1", "5"):
            ids = s["by_k"][k]["wrong_OK_opaque_ids"]
            out.append(f'- Sai OK@{k}: ' + (", ".join(f"`{v}`" for v in ids) if ids else "không có") + ".")
        non_ok = [r for r in doc["main_rows"] if r["dataset"] == s["dataset"] and r["method"] == s["method"] and r["status"] != "OK"]
        for st in sorted({r["status"] for r in non_ok}):
            out.append(f'- {st}: ' + ", ".join(f'`{r["opaque_id"]}`' for r in non_ok if r["status"] == st) + ".")
        out.append("")
    c = doc["circa_dev19_conditional"]
    s = c["summary"]
    out += ["## CIRCA dev19 — dòng có điều kiện", "", f'Nguồn: {source(s)} và `circa_dev19_conditional` trong `{REL}`. Không thay dev30.', ""]
    for k in ("1", "5"):
        b = s["by_k"][k]
        out.append(f'- k={k}: {b["n_wrong_OK"]}/{s["n_cases"]} ca sai OK; mức trượt {fmt(b["expected_misses_including_non_OK"])}; mã: ' + ", ".join(f"`{v}`" for v in b["wrong_OK_opaque_ids"]) + ".")
    out += ["- Nhóm ca lỗi làm tròn đã xác nhận được giữ nguyên ở `excluded_confirmed_rounding11` của JSON; không suy nó giải thích mọi thất bại CIRCA.", "", "## Nezha: dấu đổi từ số đã lưu", "", f'Nguồn: `nezha_saved_sensitivity_flags` trong `{REL}`; mỗi dấu trỏ tới `results/T-026/cham-a.json` và bản ghi nguồn. Không có đặc trưng hoặc cơ chế cho các view này.', "", "| View | Phương pháp | Ca included | Không thuộc cohort | Đổi status | Đổi Hit@1 | Đổi Hit@5 |", "|---|---|---:|---:|---:|---:|---:|"]
    flags = doc["nezha_saved_sensitivity_flags"]
    for view in sorted({f["view"] for f in flags}):
        for method in doc["primary_methods"]:
            part = [f for f in flags if f["view"] == view and f["method"] == method]
            included = [f for f in part if f["cohort_state"] == "included"]
            out.append(f'| {view} | {method} | {len(included)} | {len(part)-len(included)} | {sum(f["status_changed"] for f in included)} | {sum(f["hit@1_changed"] for f in included)} | {sum(f["hit@5_changed"] for f in included)} |')
    out += ["", "## Kiểm bước 1", "", f'`runs/danh-sach-001/validation.json`: đối chiếu đúng tập ca/status/seed/hash nguồn và đẳng thức Σ(1−Hit)=n·(1−Hit bảng). `runs/danh-sach-001/progress.jsonl`: thời gian từng pha. Các trường evidence/mechanisms trong `{REL}` còn null, trạng thái pending_codebook.', ""]
    target = ROOT / "results/T-028/danh-sach-ca-sai.md"
    if target.exists():
        raise FileExistsError(target)
    target.write_text("\n".join(out), encoding="utf-8")
    print(json.dumps({"written": str(target.relative_to(ROOT)), "main_rows": len(doc["main_rows"]), "statuses": dict(Counter(r["status"] for r in doc["main_rows"]))}, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
