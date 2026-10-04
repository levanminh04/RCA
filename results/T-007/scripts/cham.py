"""T-007: chấm thứ hạng MicroRank, TraceRCA theo đúng cách của main.py RCAEval (259ea41, dòng 504-660).

- Mỗi file <service>_<fault>_<n>.json chứa {"0": ranks}; ranks là thao tác "<service>_<method>".
- Đổi về service: x.split("_")[0].replace("-db", ""); bỏ trùng, giữ lần xuất hiện đầu (như main.py).
- Evaluator(max_k=5) của RCAEval cho từng loại lỗi; đáp án Node(service, "unknown"). Tên ca chỉ dùng để chấm.
- Báo AC@1, AC@3, AC@5, Avg@5 cho từng loại lỗi; AVERAGE = trung bình 6 loại lỗi (cách đọc cột AVERAGE của bài,
  chưa kiểm); thêm "ALL" = chấm gộp mọi ca (bằng AVERAGE khi mỗi loại lỗi đủ ca).
- Ca lỗi (<...>_failed.json): main.py bỏ qua file có khóa "error" khi chấm. Báo hai cách:
  "bo_ca_loi" (bỏ khỏi mẫu số, như main.py) và "ca_loi_la_truot" (tính là trượt, thứ hạng rỗng).

Chạy bằng môi trường có RCAEval: python cham.py <thư mục results> [<thư mục results> ...] --json <file ra>
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.expanduser("~/rca/src/RCAEval"))
from RCAEval.benchmark.evaluation import Evaluator  # noqa: E402
from RCAEval.classes.graph import Node  # noqa: E402

LOI6 = ["cpu", "mem", "disk", "socket", "delay", "loss"]


def service_ranks(ranks):
    s = [Node(x.split("_")[0].replace("-db", ""), "unknown") for x in ranks]
    return [s[0]] + [s[i] for i in range(1, len(s)) if s[i] not in s[:i]] if s else []


def cham(res_dir):
    files = sorted(glob.glob(os.path.join(res_dir, "*.json")))
    theo_loi = {cach: {f: Evaluator(max_k=5) for f in LOI6 + ["ALL"]} for cach in ["bo_ca_loi", "ca_loi_la_truot"]}
    dem = {"ok": 0, "loi": 0, "rong": 0}
    ca_loi = []
    for fp in files:
        b = os.path.basename(fp)[:-5]
        failed = b.endswith("_failed")
        service, fault = b.split("_")[:2]
        with open(fp) as f:
            d = json.load(f)
        if failed or "error" in d:
            dem["loi"] += 1
            ca_loi.append(b)
            ranks = None
        else:
            ranks = d["0"]
            dem["ok"] += 1
            dem["rong"] += int(len(ranks) == 0)
        ans = Node(service, "unknown")
        for cach, ev in theo_loi.items():
            if ranks is None and cach == "bo_ca_loi":
                continue
            sr = service_ranks(ranks or [])
            ev[fault].add_case(ranks=sr, answer=ans)
            ev["ALL"].add_case(ranks=sr, answer=ans)
    out = {"thu_muc": res_dir, "so_file": len(files), "dem": dem, "ca_loi": ca_loi}
    for cach, ev in theo_loi.items():
        bang = {}
        for f in LOI6 + ["ALL"]:
            e = ev[f]
            bang[f] = None if e.num == 0 else {"n": e.num, "AC@1": e.accuracy(1), "AC@3": e.accuracy(3),
                                                "AC@5": e.accuracy(5), "Avg@5": e.average(5)}
        co = [bang[f] for f in LOI6 if bang[f]]
        bang["AVERAGE"] = None if not co else {k: sum(x[k] for x in co) / len(co) for k in ["AC@1", "AC@3", "AC@5", "Avg@5"]}
        out[cach] = bang
    return out


def in_bang(o):
    print("==", o["thu_muc"], "| file:", o["so_file"], "|", o["dem"], "| ca lỗi:", o["ca_loi"])
    for cach in ["bo_ca_loi", "ca_loi_la_truot"]:
        if cach == "ca_loi_la_truot" and not o["ca_loi"]:
            continue
        print("  cách:", cach)
        print("   %-8s %3s %6s %6s %6s %6s" % ("loi", "n", "AC@1", "AC@3", "AC@5", "Avg@5"))
        for f in LOI6 + ["AVERAGE", "ALL"]:
            r = o[cach][f]
            if r:
                print("   %-8s %3s %6.2f %6.2f %6.2f %6.2f" % (f, r.get("n", ""), r["AC@1"], r["AC@3"], r["AC@5"], r["Avg@5"]))


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # Windows mặc định cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--json")
    a = ap.parse_args()
    outs = [cham(d) for d in a.dirs]
    for o in outs:
        in_bang(o)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(outs, f, indent=1)


if __name__ == "__main__":
    main()
