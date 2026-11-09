"""B0 T-057: kiểm sha256 các file đầu vào theo manifest đã ghim. Chỉ đọc.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/b0_kiem_hash.py results/T-057/b0-kiem-hash.json
Với mỗi manifest, lấy mọi mục {đường dẫn: {sha256, bytes}} (đệ quy). Một file đạt khi sha256 hiện tại
trùng pin ở manifest MỚI NHẤT có ghim nó (thứ tự manifest theo danh sách dưới). Bỏ qua tài liệu sống
(docs/, tasks/, AGENTS.md, CLAUDE.md), vì manifest cũ ghim bản tại thời điểm đó.
"""
import hashlib
import json
import os
import sys

MANIFESTS = [
    # T-034: bản cuối
    "results/T-034/runs/manifest-cuoi-007/manifest.json",
    # T-052: theo thứ tự thời gian
    "results/T-052/manifest.json",
    "results/T-052/manifest-thuc-thi-001.json",
    "results/T-052/manifest-dap-phan-bien-001.json",
    "results/T-052/manifest-dap-phan-bien-002.json",
    "results/T-052/manifest-f3-001.json",
    "results/T-052/manifest-sua-f2-f4-003.json",
    "results/T-052/manifest-dinh-chinh-g3-004.json",
    # T-054 báo cáo p7a-013-v2
    "results/T-054/reports/p7a-013-v2/manifest.json",
    "results/T-054/reports/p7a-013-v2/manifest-002.json",
    "results/T-054/reports/p7a-013-v2/manifest-003.json",
    "results/T-054/reports/p7a-013-v2/manifest-004.json",
    "results/T-054/reports/p7a-013-v2/manifest-005.json",
    "results/T-054/reports/p7a-013-v2/manifest-006.json",
    # T-055, T-056
    "results/T-055/manifest-002.json",
    "results/T-056/manifest-003.json",
]
SONG = ("docs/", "tasks/", "AGENTS.md", "CLAUDE.md")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def walk(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, dict) and isinstance(v.get("sha256"), str) and ("/" in k or "\\" in k):
                out.append((k.replace("\\", "/"), v["sha256"]))
            elif isinstance(v, dict) and isinstance(v.get("sha256"), str) and isinstance(v.get("path"), str):
                out.append((v["path"].replace("\\", "/"), v["sha256"]))
            walk(v, out)
    elif isinstance(o, list):
        for v in o:
            if isinstance(v, dict) and isinstance(v.get("sha256"), str) and isinstance(v.get("path"), str):
                out.append((v["path"].replace("\\", "/"), v["sha256"]))
            walk(v, out)


def main(outp):
    pins = {}  # path -> (manifest, sha) của manifest mới nhất
    mf_info = []
    for m in MANIFESTS:
        if not os.path.exists(m):
            mf_info.append({"manifest": m, "ton_tai": False})
            continue
        ent = []
        walk(json.load(open(m, encoding="utf-8")), ent)
        mf_info.append({"manifest": m, "ton_tai": True, "so_muc": len(ent), "sha256": sha(m)})
        for p, s in ent:
            if p.startswith(SONG):
                continue
            pins[p] = (m, s)
    rows, lech, thieu = [], [], []
    for p in sorted(pins):
        m, s = pins[p]
        if not os.path.exists(p):
            thieu.append(p)
            rows.append({"path": p, "manifest": m, "trang_thai": "KHONG_CO_FILE"})
            continue
        a = sha(p)
        ok = a == s
        if not ok:
            lech.append(p)
        rows.append({"path": p, "manifest": m, "trang_thai": "KHOP" if ok else "LECH", "sha256": a})
    res = {
        "lenh": "py -3 -B results/T-057/scripts/b0_kiem_hash.py " + outp,
        "manifests": mf_info,
        "so_file_kiem": len(rows),
        "so_khop": sum(r["trang_thai"] == "KHOP" for r in rows),
        "lech": lech,
        "khong_co_file": thieu,
        "rows": rows,
    }
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: res[k] for k in ("so_file_kiem", "so_khop", "lech", "khong_co_file")}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
