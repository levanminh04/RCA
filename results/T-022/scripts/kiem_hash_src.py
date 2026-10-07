"""T-022 bước 1: so hash code dùng chung trong src/ với hash các task trước đã ghi (T-015, T-016, T-017, T-014).

Mục đích: biết artifact P1 còn ứng với code hiện tại không. Chỉ đọc.
Chạy: py -3 -B results/T-022/scripts/kiem_hash_src.py --run hash-src-001
"""
import argparse
import glob
import hashlib
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
NGUON = [
    "results/T-015/manifest-ban-giao.json",
    "results/T-017/runs/close-docs-001/before.json",
    "results/T-017/runs/fix-n1n2-001/before.json",
    "results/T-017/runs/fix-n1n2-001/change-manifest.json",
]
# Lượt hash-src-001 gộp cả bản chép "source-before" (bản trước sửa) nên có dòng không khớp giả.
# Từ hash-src-002: bỏ đường dẫn chứa "source-before"; với change-manifest đọc khóa sha256_after.


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def norm(p):
    q = str(p).replace("\\", "/")
    i = q.find("src/")
    return q[i:] if i >= 0 else None


def walk(o, acc):
    if isinstance(o, dict):
        p = o.get("path") or o.get("file") or o.get("duong_dan") or o.get("source")
        h = o.get("sha256") or o.get("sha256_after")
        if isinstance(p, str) and isinstance(h, str) and "source-before" not in p.replace("\\", "/"):
            acc.append((p, h))
        for k, v in o.items():
            if isinstance(v, str) and len(v) == 64 and isinstance(k, str) and ("src/" in k.replace("\\", "/")):
                acc.append((k, v))
            walk(v, acc)
    elif isinstance(o, list):
        for v in o:
            walk(v, acc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    args = ap.parse_args()
    run_dir = os.path.join(REPO, "results/T-022/runs", args.run)
    if os.path.exists(run_dir):
        sys.exit("run dir đã có")
    os.makedirs(run_dir)
    cur = {}
    for p in glob.glob(os.path.join(REPO, "src", "**", "*.py"), recursive=True):
        cur[norm(os.path.relpath(p, REPO))] = sha(p)
    out = {"hash_hien_tai": cur, "doi_chieu": []}
    for f in NGUON:
        fp = os.path.join(REPO, f)
        if not os.path.exists(fp):
            out["doi_chieu"].append({"nguon": f, "loi": "không có file"})
            continue
        acc = []
        walk(json.load(open(fp, encoding="utf-8")), acc)
        for p, h in acc:
            q = norm(p)
            if q and q in cur:
                out["doi_chieu"].append({"nguon": f, "file": q, "khop": cur[q] == h})
    with open(os.path.join(run_dir, "kiem-hash-src.json"), "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    tom = {}
    for d in out["doi_chieu"]:
        if "file" in d:
            tom.setdefault(d["file"], set()).add(d["khop"])
    print(json.dumps({k: sorted(v) for k, v in sorted(tom.items())}, ensure_ascii=False))
    print("khong_doi_chieu_duoc:", sorted(set(cur) - set(tom)))


if __name__ == "__main__":
    main()
