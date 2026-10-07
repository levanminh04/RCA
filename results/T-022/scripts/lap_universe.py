"""T-022 bước 2: lập universe thực thể RE2-TT dev từ metadata schema (không đọc số đo, không đọc nhãn).

Thực thể = tiền tố trước dấu '_' đầu tiên của tên cột metric (như RCAEval main.py:560, bỏ phần '-db' không áp với TT).
Chạy: py -3 -B results/T-022/scripts/lap_universe.py --run universe-001
"""
import argparse
import collections
import hashlib
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCHEMAS = "results/T-002/local-inspection/run-002/schemas.json"
ALLOW = "results/T-022/allowlist-dev.json"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    args = ap.parse_args()
    run_dir = os.path.join(REPO, "results/T-022/runs", args.run)
    if os.path.exists(run_dir):
        sys.exit("run dir đã có")
    os.makedirs(run_dir)
    allow = json.load(open(os.path.join(REPO, ALLOW), encoding="utf-8"))
    schemas = json.load(open(os.path.join(REPO, SCHEMAS), encoding="utf-8"))
    per_case = {}
    count = collections.Counter()
    for c in allow["cases"]:
        case_name = c["case_dir"].split("/")[-1]  # chỉ để tra schema; không ghi ra đầu ra
        names = [x["name"] for x in schemas[f"{case_name}/metrics.parquet"] if x["name"] != "time"]
        ents = sorted({n.split("_")[0] for n in names})
        per_case[c["opaque_id"]] = ents
        count.update(ents)
    n = len(per_case)
    all_ents = sorted(count)
    ts = [e for e in all_ents if e.startswith("ts-")]
    out = {
        "mo_ta": "Universe thực thể đánh giá RE2-TT dev (CANDIDATE, lua-chon-can-duyet.md mục 3). Chốt từ metadata schema metric của 30 ca dev, không dùng nhãn.",
        "trang_thai": "proposed",
        "quy_tac": "thực thể = tiền tố trước '_' đầu tiên của tên cột metric; U = mọi thực thể bắt đầu bằng 'ts-' xuất hiện ở ít nhất một ca dev",
        "nguon": {SCHEMAS: sha(os.path.join(REPO, SCHEMAS)), ALLOW: sha(os.path.join(REPO, ALLOW))},
        "U": ts,
        "so_thuc_the_U": len(ts),
        "ngoai_U": {e: count[e] for e in all_ents if not e.startswith("ts-")},
        "thuc_the_khong_co_o_moi_ca": {e: count[e] for e in all_ents if count[e] < n},
        "nhom": {
            "service": [e for e in ts if e.endswith("-service")],
            "db": [e for e in ts if e.endswith("-mongo") or e.endswith("-mysql")],
            "khac": [e for e in ts if not (e.endswith("-service") or e.endswith("-mongo") or e.endswith("-mysql"))],
        },
        "so_thuc_the_moi_ca": {k: len(v) for k, v in sorted(per_case.items())},
    }
    os.makedirs(os.path.join(REPO, "results/T-022/mappings"), exist_ok=True)
    with open(os.path.join(REPO, "results/T-022/mappings/universe-re2tt-dev.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    summary = {"so_ca": n, "U": len(ts), "service": len(out["nhom"]["service"]), "db": len(out["nhom"]["db"]),
               "khac": out["nhom"]["khac"], "ngoai_U": out["ngoai_U"], "khong_moi_ca": out["thuc_the_khong_co_o_moi_ca"]}
    with open(os.path.join(run_dir, "tom-tat.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
