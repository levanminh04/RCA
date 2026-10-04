"""T-018: tải inject_time.txt của 30 ca dev RE2-TT từ HF (revision ghim), kiểm git blob oid, đối chiếu điểm giữa file metric.

Chỉ lấy đúng 30 tên thư mục re2tt_* đang có trong data/rcaeval/ (ca dev). Không đụng ca khác.
Chạy: py -3 results/T-018/scripts/tai_moc_tiem.py  (chỉ cần thư viện chuẩn + pyarrow để đọc cột time; dùng env py312)
Ghi: D:/RCA-ext/work/T-018/nguon/rcaeval-inject/<ca>/inject_time.txt và results/T-018/runs/tai-moc-tiem.json
"""
import hashlib
import json
import os
import urllib.parse
import urllib.request

import pyarrow.parquet as pq

REV = "afeacb11bcc94dadfd1c8f483ee4377b2b8b614e"
REPO = r"D:\RCA-flashticket"
DATA = os.path.join(REPO, "data", "rcaeval")
OUT = r"D:\RCA-ext\work\T-018\nguon\rcaeval-inject"
LOG = os.path.join(REPO, "results", "T-018", "runs", "tai-moc-tiem.json")


def git_oid(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def main():
    dev = sorted(c for c in os.listdir(DATA) if c.startswith("re2tt_"))
    assert len(dev) == 30
    paths = [f"{c}/inject_time.txt" for c in dev]
    body = urllib.parse.urlencode([("paths", p) for p in paths]).encode()
    req = urllib.request.Request(f"https://huggingface.co/api/datasets/phamquiluan/RCAEval/paths-info/{REV}", data=body)
    info = {d["path"]: d for d in json.load(urllib.request.urlopen(req))}
    kq = {}
    for c in dev:
        p = f"{c}/inject_time.txt"
        url = f"https://huggingface.co/datasets/phamquiluan/RCAEval/resolve/{REV}/{p}"
        b = urllib.request.urlopen(url).read()
        os.makedirs(os.path.join(OUT, c), exist_ok=True)
        with open(os.path.join(OUT, c, "inject_time.txt"), "wb") as f:
            f.write(b)
        t = pq.read_table(os.path.join(DATA, c, "metrics.parquet"), columns=["time"]).column("time").to_pylist()
        moc = int(b.decode().strip())
        local = os.path.join(DATA, c, "inject_time.txt")
        kq[c] = {
            "oid_hf": info[p]["oid"], "oid_tai": git_oid(b), "khop_oid": info[p]["oid"] == git_oid(b),
            "size": len(b), "moc": moc, "diem_giua_time": (min(t) + max(t)) / 2,
            "so_dong_truoc_moc": sum(1 for x in t if x < moc), "so_dong_tu_moc": sum(1 for x in t if x >= moc),
            "trung_ban_trong_data": (open(local, "rb").read() == b) if os.path.exists(local) else None,
        }
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(kq, f, ensure_ascii=False, indent=1)
    print("so ca:", len(kq), "| khop oid:", sum(v["khop_oid"] for v in kq.values()),
          "| moc == diem giua:", sum(v["moc"] == v["diem_giua_time"] for v in kq.values()),
          "| truoc/tu moc:", sorted({(v["so_dong_truoc_moc"], v["so_dong_tu_moc"]) for v in kq.values()}),
          "| trung ban trong data:", [v["trung_ban_trong_data"] for v in kq.values() if v["trung_ban_trong_data"] is not None])


if __name__ == "__main__":
    main()
