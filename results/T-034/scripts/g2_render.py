"""T-034: dựng `goi-g2.md` và `hai-phep-kiem.md` từ bản mẫu trong `scripts/mau/`.

Bản mẫu là Markdown có hai loại chỗ giữ:
- `{{mã}}` hoặc `{{mã:định dạng}}`: một con số (hoặc chuỗi) trong sổ số liệu, tức (file JSON, con trỏ) → giá trị;
- `@@tên@@` hoặc `@@tên:tham số@@` đứng riêng một dòng: một bảng sinh bởi `g2_blocks.py` (bảng cũng chỉ chứa chỗ giữ `{{mã}}`).

Đầu ra: hai file .md ở `results/T-034/`; trong thư mục lượt: bản mẫu đã mở bảng (`*.expanded.md`), sổ số liệu đã dùng
(`registry.json`, kèm mã băm file nguồn). Phép kiểm V4 (`v4_kiem_so.py`) đọc các file này và tự phân giải lại từ JSON nguồn.

Dùng: python g2_render.py <thư mục lượt>
"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g2_blocks as B  # noqa: E402
import g2_doc_facts  # noqa: E402
from g2_ban_do import register_facts  # noqa: E402
from g2_lib import Facts, ROOT, fmt, load, sha  # noqa: E402

PLACE = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::([^}]+))?\}\}")
BLOCK = re.compile(r"^@@([A-Za-z0-9_]+)(?::([^@]+))?@@[ \t]*$", re.M)
DOCS = {"goi-g2": "results/T-034/goi-g2.md", "hai-phep-kiem": "results/T-034/hai-phep-kiem.md"}


def main():
    run = ROOT / sys.argv[1]
    out_dir = run / "render"
    out_dir.mkdir(parents=True, exist_ok=True)
    F = register_facts(Facts(), run, with_extra=True)
    g2_doc_facts.register(F, run)
    blocks = {"k2_rank": lambda a: B.k2_rank(F, load, a), "k2_cell": lambda a: B.k2_cell(F, load, a), "k2_det": lambda a: B.k2_det(F, load),
              "k2_det_cell": lambda a: B.k2_det_cell(F, load), "k2_modeb": lambda a: B.k2_modeb(F, load), "k2_author": lambda a: B.k2_author(F, load),
              "k2_mrsplit": lambda a: B.k2_mrsplit(F, load), "k3_summary": lambda a: B.k3_summary(F, load), "k3_rows": lambda a: B.k3_rows(F, load),
              "k3_excluded": lambda a: B.k3_excluded(F, load), "k3_p4": lambda a: B.k3_p4(F, load), "appendix_a": lambda a: B.appendix_a(F, load),
              "appendix_b": lambda a: B.appendix_b(F, load), "appendix_c": lambda a: B.appendix_c(F, load), "e1_pairs": lambda a: B.e1_pairs(F, load, a), "e2_chains": lambda a: B.e2_chains(F, load)}
    used, report = {}, {}
    for name, target in DOCS.items():
        tpl = (Path(__file__).resolve().parent / "mau" / f"{name}.md").read_text(encoding="utf-8")
        expanded = BLOCK.sub(lambda m: blocks[m.group(1)](m.group(2)), tpl)
        assert "@@" not in expanded, [line for line in expanded.splitlines() if "@@" in line][:5]
        missing = sorted({m.group(1) for m in PLACE.finditer(expanded) if m.group(1) not in F.items})
        assert not missing, (name, missing)

        def sub(m):
            fid, spec = m.group(1), m.group(2) or ""
            used[fid] = F.items[fid]
            return fmt(F.items[fid]["value"], spec)
        text = PLACE.sub(sub, expanded)
        (out_dir / f"{name}.expanded.md").write_text(expanded, encoding="utf-8", newline="\n")
        (ROOT / target).write_text(text, encoding="utf-8", newline="\n")
        report[name] = {"target": target, "placeholders": len(PLACE.findall(expanded)), "bytes": len(text.encode("utf-8")), "lines": text.count("\n") + 1}
    sources = {p: sha(p) for p in sorted({v["path"] for v in used.values()})}
    (out_dir / "registry.json").write_text(json.dumps({"schema": "T034-registry-v1", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "facts": used, "sources_sha256": sources,
                                                       "documents": report}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False), "facts used", len(used), "sources", len(sources))


if __name__ == "__main__":
    main()
