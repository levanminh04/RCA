"""T-034 V4: đối chiếu mọi số trong `goi-g2.md` và `hai-phep-kiem.md` với JSON nguồn. Chỉ đọc.

Script này không nhập mã dựng văn bản. Nó tự:
1. kiểm mã băm từng file nguồn so với sổ số liệu của lượt dựng;
2. phân giải lại từng số từ (file, con trỏ JSON) và so với giá trị ghi trong sổ (bằng tuyệt đối);
3. tự định dạng lại và thay vào bản mẫu đã mở bảng, rồi so từng byte với file .md đã phát hành;
4. quét phần chữ của bản mẫu (sau khi bỏ mọi chỗ giữ số và đoạn mã) để tìm chữ số không đi qua sổ; mỗi chữ số còn lại phải
   thuộc một lớp được khai dưới đây (mã định danh, số mục, ngày, tên độ đo, tham số giao thức có nguồn), nếu không thì V4 hỏng.

Giới hạn: số viết bằng chữ ("ba ca", "một nửa") không được quét; phần đó thuộc phép đọc V5.

Dùng: python v4_kiem_so.py <thư mục lượt dựng>
"""
import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = {"goi-g2": "results/T-034/goi-g2.md", "hai-phep-kiem": "results/T-034/hai-phep-kiem.md"}
PLACE = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::([^}]+))?\}\}")

# (lớp, biểu thức, giải thích/nguồn). Thứ tự có ý nghĩa: lớp cụ thể trước.
ALLOW = [
    ("mã ca dev", r"dev-[0-9a-f]{10}", "định danh ca trong nhãn dev"),
    ("ngày tháng", r"\b\d{1,2}/\d{1,2}/\d{4}\b|[Nn]gày \d{1,2}/\d{1,2}(?:/\d{4})?\b|tháng \d{1,2}/\d{4}\b", "ngày của tài liệu và quyết định"),
    ("tên độ đo", r"(?:Hit|AC|Avg|NDCG|Retrieval|Rerank)@\d+|\(K=\d+\)", "tên độ đo của giao thức (WHY-06, WHY-23)"),
    ("mã dataset", r"\bRE[123](?:-(?:TT|OB|SS))?\b", "tên bộ dữ liệu RCAEval"),
    ("mã tài liệu và task", r"\b(?:G2-H\d+|T-\d{3}|WHY-\d+|Q-\d+|HP-\d+|UV-\d+|KT-?\d+|KQ\d+|SL\d+|QT\d+|DT18|B16|EC2|NV\d)\b", "mã dòng, task, quyết định, lý do, bài học; tên loại máy"),
    ("mã câu hỏi, cổng, gói, cờ, phép", r"\bRQ\d[a-d]?\b|\b[GP]\d+[ab]?\b|\b[EVKFRNIHMDB]\d+\b|\b[MTSBK]-[A-Z]?\d\b|\btl\d\b|\bmo\d+(?:p\d+)?\b", "mã RQ, cổng G, gói P, phép E/V/K/F, cờ M/H/D/N/B/I, nhánh đổi của T-032"),
    ("số mục, bước, tầng, bảng, hình", r"(?:[Mm]ục|§|[Bb]ước|[Tt]ầng|[Bb]ảng|Hình|[Cc]âu|[Đđ]iểm|seed|[Nn]hóm) ?\d+(?:\.\d+)*(?:(?:, | và |[–\-]| đến )(?:§)?\d+(?:\.\d+)*)*", "dẫn chiếu tới mục của tài liệu, bước, tầng"),
    ("đánh số tiêu đề và danh sách", r"(?m)^#{1,6} \d+(?:\.\d+)*\.? |^\s*\d+\. |^\*\*\d+\. ", "số thứ tự của tiêu đề, danh sách, câu hỏi"),
    ("thuật ngữ: hạng 1", r"[Hh]ạng 1\b", "vị trí đầu của bảng xếp hạng (như trong Hit@1), không phải số đo"),
    ("tham số: cửa sổ chấm phát hiện", r"cửa sổ 60 giây", "WHY-35: Precision/Recall/F1 theo cửa sổ 60 giây"),
    ("tham số: mức bootstrap", r"mức 95%", "WHY-28: khoảng bootstrap 95% theo ô"),
    ("tham số: ngưỡng lời gọi chậm", r"phân vị 95", "results/T-032/thiet-ke-bang-mo-ta-004.md mục 5b"),
    ("tham số: số thực mở rộng", r"80 bit", "results/T-034/thiet-ke-hai-phep-kiem.md, Mục nối 3"),
]


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def resolve(doc, pointer):
    cur = doc
    if pointer in ("", "/"):
        return cur
    for raw in pointer.lstrip("/").split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        cur = cur[int(key)] if isinstance(cur, list) else cur[key]
    return cur


def apply(value, op):
    if op is None:
        return value
    return {"len": len, "sum": sum, "count_true": lambda v: sum(bool(x) for x in v)}[op](value)


def fmt(value, spec):
    if spec == "x" or isinstance(value, str):
        return str(value)
    if value is None:
        return "N/A"
    if spec.startswith("pct"):
        return f"{value * 100:.{int(spec[3:] or 0)}f}".replace(".", ",") + "%"
    if spec.startswith("."):
        return format(value, spec).replace(".", ",")
    if spec == "e":
        return f"{value:.1e}".replace(".", ",")
    if isinstance(value, bool):
        return "có" if value else "không"
    if isinstance(value, int):
        return f"{value:,}".replace(",", ".") if abs(value) >= 1000 else str(value)
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.4g}".replace(".", ",")


def same(a, b):
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return type(a) is type(b) and a == b


def stray(expanded):
    text = re.sub(r"```.*?```", " ", expanded, flags=re.S)
    spans = sorted({m.group(0) for m in re.finditer(r"`[^`\n]*`", text) if re.search(r"\d", m.group(0))})
    text = re.sub(r"`[^`\n]*`", " ⟦mã⟧ ", text)
    text = PLACE.sub("⟦số⟧", text)
    counts = {}
    for name, pattern, _why in ALLOW:
        text, n = re.subn(pattern, lambda m: re.sub(r"\d", "#", m.group(0)), text)
        counts[name] = n
    left = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"\d[\d.,]*", line):
            left.append({"line": i, "token": m.group(0), "context": line[max(0, m.start() - 40):m.end() + 25]})
    return counts, left, spans


def main():
    run = ROOT / sys.argv[1]
    reg = json.loads((run / "render" / "registry.json").read_text(encoding="utf-8"))
    facts, cache, problems = reg["facts"], {}, []
    for path, digest in reg["sources_sha256"].items():
        if not (ROOT / path).is_file():
            problems.append({"kind": "thiếu file nguồn", "path": path})
        elif sha(path) != digest:
            problems.append({"kind": "file nguồn đổi sau khi dựng", "path": path})
    for fid, f in facts.items():
        try:
            if f["path"] not in cache:
                cache[f["path"]] = json.loads((ROOT / f["path"]).read_text(encoding="utf-8"))
            value = apply(resolve(cache[f["path"]], f["pointer"]), f["op"])
        except Exception as e:  # noqa: BLE001
            problems.append({"kind": "không phân giải được", "fact": fid, "path": f["path"], "pointer": f["pointer"], "error": repr(e)})
            continue
        if not same(value, f["value"]):
            problems.append({"kind": "giá trị lệch sổ", "fact": fid, "source": value, "registry": f["value"]})
    docs = {}
    for name, target in DOCS.items():
        expanded = (run / "render" / f"{name}.expanded.md").read_text(encoding="utf-8")
        published = (ROOT / target).read_text(encoding="utf-8")
        ids = [m.group(1) for m in PLACE.finditer(expanded)]
        unknown = sorted({i for i in ids if i not in facts})
        for i in unknown:
            problems.append({"kind": "chỗ giữ không có trong sổ", "doc": name, "fact": i})
        rendered = PLACE.sub(lambda m: fmt(facts[m.group(1)]["value"], m.group(2) or "") if m.group(1) in facts else m.group(0), expanded)
        if rendered != published:
            a, b = rendered.splitlines(), published.splitlines()
            first = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            problems.append({"kind": "văn bản phát hành khác bản tự dựng lại", "doc": name, "line": first + 1})
        if "{{" in published or "@@" in published:
            problems.append({"kind": "còn chỗ giữ chưa thay", "doc": name})
        counts, left, spans = stray(expanded)
        for item in left:
            problems.append(dict(item, kind="chữ số không qua sổ số liệu", doc=name))
        docs[name] = {"target": target, "sha256": sha(target), "placeholders": len(ids), "distinct_facts": len(set(ids)), "allowed_literal_classes": counts, "stray_numeric_tokens": len(left),
                      "code_spans_with_digits_not_scanned": spans}
    out = {"schema": "T034-V4-v1", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "run": sys.argv[1], "status": "PASS" if not problems else "FAIL",
           "facts_checked": len(facts), "sources_checked": len(reg["sources_sha256"]), "documents": docs, "n_problems": len(problems), "problems": problems,
           "allow_classes": [{"class": n, "pattern": p, "why": w} for n, p, w in ALLOW],
           "limit": "Số viết bằng chữ không được quét; thuộc phép đọc V5. Chữ số trong đoạn mã (`...`) là đường dẫn, tên lượt, tên trường hoặc tham số khai trước; "
                    "không quét, liệt kê ở code_spans_with_digits_not_scanned."}
    (run / "v4.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("V4", out["status"], "facts", len(facts), "problems", len(problems))
    for p in problems[:60]:
        print("  ", json.dumps(p, ensure_ascii=False)[:260])


if __name__ == "__main__":
    main()
