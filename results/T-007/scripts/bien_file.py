"""T-007: biên file so với mốc tiêm (điểm R1 trong REVIEW T-002), trên đúng dữ liệu T-007 đã chạy.

- fse-ob (BOCPD): cột `time` của simple_data.csv: time_min − mốc, time_max − mốc, số dòng trước mốc, số dòng từ mốc.
- RE2-OB (MicroRank, TraceRCA): `startTime` của traces.parquet: startTime_min − mốc, startTime_max − mốc (giây);
  với ca có trace kết thúc trước +700 s: số span trước/sau mốc trong cửa sổ ±300 s và ±600 s.
Chỉ đọc dữ liệu, không chạy phương pháp. Ghi JSON.

Chạy: <env>/bin/python bien_file.py --out <file json>
"""
import argparse
import collections
import glob
import json
import os

import pandas as pd

R = os.path.expanduser("~/rca")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {"fse_ob": {}, "re2ob": {}, "re2ob_trace_ket_thuc_som": []}
    c = collections.Counter()
    for p in sorted(glob.glob(os.path.join(R, "data/fse/fse-ob/*/*/simple_data.csv"))):
        d = os.path.dirname(p)
        inj = int(open(os.path.join(d, "inject_time.txt")).readline().strip())
        t = pd.read_csv(p, usecols=["time"])["time"]
        c[(int(t.min() - inj), int(t.max() - inj), int((t < inj).sum()), int((t >= inj).sum()))] += 1
    out["fse_ob"] = {"khoa": "(time_min - moc, time_max - moc, so_dong_truoc_moc, so_dong_tu_moc)",
                     "dem": {str(k): v for k, v in sorted(c.items())}}
    c2 = collections.Counter()
    for d in sorted(glob.glob(os.path.join(R, "data/re2ob/re2ob_*"))):
        inj = int(open(os.path.join(d, "inject_time.txt")).readline().strip()) * 1_000_000
        s = pd.read_parquet(os.path.join(d, "traces.parquet"), columns=["startTime"])["startTime"]
        lo, hi = round((s.min() - inj) / 1e6), round((s.max() - inj) / 1e6)
        c2[(lo, hi)] += 1
        if hi < 700:
            rec = {"case": os.path.basename(d), "startTime_min_tru_moc_s": lo, "startTime_max_tru_moc_s": hi}
            for half in (300, 600):
                w = s[(s >= inj - half * 1e6) & (s < inj + half * 1e6)]
                rec["cua_so_%d" % half] = {"span_truoc_moc": int((w < inj).sum()), "span_tu_moc": int((w >= inj).sum())}
            out["re2ob_trace_ket_thuc_som"].append(rec)
    out["re2ob"] = {"khoa": "(startTime_min - moc, startTime_max - moc) giay", "dem": {str(k): v for k, v in sorted(c2.items())}}
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
