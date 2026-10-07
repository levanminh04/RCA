"""T-022 bước 1: đối chiếu SHA-256 trong allowlist-dev.json với hash nguồn T-017 đã ghi (run-dev-005).

Hai lần băm độc lập (T-017 ngày 04/10, T-022 ngày 05/10) phải trùng nếu dữ liệu không đổi.
Chạy: py -3 -B results/T-022/scripts/doi_chieu_hash.py --run allowlist-001
"""
import argparse
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--out-name", default="doi-chieu-hash-T017-v2.json")
    args = ap.parse_args()
    allow = json.load(open(os.path.join(REPO, "results/T-022/allowlist-dev.json"), encoding="utf-8"))
    t017 = json.load(open(os.path.join(REPO, "results/T-017/runs/run-dev-005/summary.json"), encoding="utf-8"))
    ref = {}
    for row in t017:
        for p, v in row["source_hashes"].items():
            key = p.replace("\\", "/").split("data/rcaeval/")[-1] if "data/rcaeval" in p.replace("\\", "/") else None
            if key:
                ref["data/rcaeval/" + key] = v
    so, khop, lech, khong_co = 0, 0, [], []
    khop_theo_loai = {}
    for c in allow["cases"]:
        for fn, f in c["files"].items():
            if f is None:
                continue
            so += 1
            r = ref.get(f["path"])
            if r is None:
                khong_co.append(f["path"])
            elif r["sha256"] == f["sha256"] and r["bytes"] == f["bytes"]:
                khop += 1
                khop_theo_loai[fn] = khop_theo_loai.get(fn, 0) + 1
            else:
                lech.append(f["path"])
    out = {"so_file_allowlist": so, "co_hash_T017": so - len(khong_co), "khop": khop,
           "khop_theo_loai_file": khop_theo_loai, "lech": lech, "khong_co_trong_T017": khong_co}
    run_dir = os.path.join(REPO, "results/T-022/runs", args.run)
    out_path = os.path.join(run_dir, args.out_name)
    if os.path.exists(out_path):
        sys.exit(f"không ghi đè {out_path}")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False))
    return 0 if not lech else 1


if __name__ == "__main__":
    sys.exit(main())
