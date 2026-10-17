"""Lập results/T-040/manifest.json: mọi tệp dưới results/T-040/ trừ chính manifest; LOG/STATE ghi hash riêng.

Ghi xong thì đọc lại và băm lại toàn bộ để tự kiểm.
Lệnh: py -3 -X utf8 -B results/T-040/runs/tong-hop-011/lap_manifest.py
"""
import hashlib
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
BASE = os.path.join(ROOT, "results", "T-040")
MAN = os.path.join(BASE, "manifest.json")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest(), os.path.getsize(path)


def listing():
    files = []
    for dp, dn, fn in os.walk(BASE):
        dn.sort()
        for name in sorted(fn):
            path = os.path.join(dp, name)
            if os.path.abspath(path) == os.path.abspath(MAN) or "__pycache__" in dp:
                continue
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            h, n = sha(path)
            files.append({"path": rel, "bytes": n, "sha256": h})
    return files


files = listing()
ext = {}
for rel in ["tasks/T-040-p5b-tong-hop/LOG.md", "tasks/T-040-p5b-tong-hop/SPEC.md", "docs/STATE.md"]:
    ext[rel] = sha(os.path.join(ROOT, rel))[0]
man = {
    "task": "T-040",
    "created_local": time.strftime("%Y-%m-%d %H:%M:%S"),
    "current_run": "runs/tong-hop-011",
    "state": "DA_SUA_THEO_PHAN_BIEN_CHO_KIEM_BAN_SUA; số TT có điều kiện: T-038 chưa nghiệm thu (gói sửa R1 dừng phản biện theo Q-171)",
    "task_accepted": False,
    "commit_push": False,
    "tests_or_heldout_opened": False,
    "downloads_bytes": 0,
    "external_hashes_not_artifacts": ext,
    "excludes": "manifest tự thân; __pycache__ (không sinh do chạy với -B)",
    "file_count": len(files),
    "total_bytes": sum(f["bytes"] for f in files),
    "files": files,
}
with open(MAN, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
# tự kiểm: băm lại và so
again = {f["path"]: (f["sha256"], f["bytes"]) for f in listing()}
saved = {f["path"]: (f["sha256"], f["bytes"]) for f in json.load(open(MAN, encoding="utf-8"))["files"]}
print("files", len(saved), "bytes", man["total_bytes"], "verify", again == saved)
