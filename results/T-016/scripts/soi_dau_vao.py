r"""T-016 S4/S8: soi giá trị trung gian của bước dựng đầu vào và SeverityScorer, không chạy RCD, không đọc nhãn.

Với mỗi ca (đầu vào dựng như main.py bằng dung_dau_vao của harness), mỗi cửa sổ L:
- tập ứng viên của TORAI = tiền tố trước "_" của mọi cột metric, log, trace (sau đổi frontendservice→frontend ở trace);
  đánh dấu ứng viên không phải service ứng dụng (redis, frontend-external, traceservice, health, ...);
- va chạm tiền tố: service A là tiền tố của tên cột thuộc service B ≠ A (str.startswith ở torai.py:295-310);
- số cột trace_err bị nhân 1e9 (trung bình và phương sai normal đều 0, torai.py:162-163);
- số nguồn có tổng điểm = 0 (chia 0 → NaN, torai.py:132/149/166/181);
- bước thời gian của logts trong cửa sổ, lệch pha (mốc tiêm − đầu lưới logts) mod 15 s;
- số dòng metric sau một và hai lần giảm mẫu, số dòng normal/anomal sau hai lần; số cột metric sống sót sau
  drop_constant ở nửa anomal khi giảm mẫu hai lần (giả lập đúng _rcd_multimodal trên TOÀN bộ metric, không theo cụm).
Chạy bằng py38-rcdlock. Cách dùng: python soi_dau_vao.py --data <dataset> --length 10 --ra <file jsonl>
"""
import argparse
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chay_torai import dung_dau_vao  # noqa: E402


def bo_hang_so(df):
    return df.loc[:, (df != df.iloc[0]).any()] if len(df) else df.loc[:, []]


def z_max(a, b):
    sd = a.std()
    return np.max(np.abs((b - a.mean()) / (sd if sd != 0 else 1.0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--length", type=int, default=10)
    ap.add_argument("--ra", required=True)
    a = ap.parse_args()
    paths = sorted(glob.glob(os.path.join(a.data, "**/simple_metrics.csv"), recursive=True))
    out = open(a.ra, "w", encoding="utf-8")
    for p in paths:
        d, it = dung_dau_vao(p, "torai", a.length)
        ten = "_".join([os.path.basename(os.path.dirname(os.path.dirname(p))), os.path.basename(os.path.dirname(p))])
        m, lg, te, tl = d["metric"], d["logts"], d["tracets_err"], d["tracets_lat"]
        pre = lambda df: [c.split("_")[0] for c in df.columns if c != "time"]  # noqa: E731
        pm, pl = set(pre(m)), set(pre(lg))
        pt = {("frontend" if x == "frontendservice" else x) for x in (pre(te) + pre(tl))} if len(te) else set()
        ung_vien = sorted(pm | pl | pt)
        cot_tat_ca = [c for df in (m, lg, te, tl) for c in df.columns if c != "time"]
        va_cham = sorted({(s, c) for s in ung_vien for c in cot_tat_ca if c.startswith(s) and c.split("_")[0] != s
                          and not (s == "frontend" and c.split("_")[0] == "frontendservice")})
        rec = {"ca": ten, "length": a.length, "so_ung_vien": len(ung_vien), "ung_vien": ung_vien,
               "ung_vien_chi_metric": sorted(pm - pl - pt), "ung_vien_chi_log": sorted(pl - pm - pt),
               "ung_vien_chi_trace": sorted(pt - pm - pl), "va_cham_tien_to": [list(x) for x in va_cham][:20],
               "so_va_cham": len(va_cham)}
        # logts lưới
        lt = lg["time"].to_numpy()
        rec["buoc_logts"] = sorted({int(x) for x in np.diff(lt)}) if len(lt) > 1 else []
        rec["lech_pha_s"] = int((it - lt[0]) % 15) if len(lt) else None
        rec["so_dong_logts"] = [int((lg["time"] < it).sum()), int((lg["time"] >= it).sum())]
        # trace_err nhân 1e9, NaN do tổng 0
        nhan = 0
        tong0 = []
        if len(te):
            e = bo_hang_so(te.ffill().fillna(0))
            ne, ae = e[e["time"] < it].drop(columns=["time"]), e[e["time"] >= it].drop(columns=["time"])
            sc = []
            for c in ne.columns:
                x = ne[c].to_numpy()[:-2]
                s = z_max(x, ae[c].to_numpy())
                if x.mean() == 0 and x.var() == 0:
                    s *= 1e9
                    nhan += 1
                sc.append(s)
            if sc and sum(sc) == 0:
                tong0.append("trace_err")
            rec["diem_trace_err_max"] = float(max(sc)) if sc else None
        rec["so_cot_trace_err_nhan_1e9"] = nhan
        # giảm mẫu: một lần (torai.py:81) và hai lần (_rcd_multimodal:29), toàn bộ metric
        m1 = m.iloc[::15, :]
        m2 = m1.iloc[::15, :]
        an2 = bo_hang_so(m2[m2["time"] >= it].drop(columns=["time"]))
        nn2 = bo_hang_so(m2[m2["time"] < it].drop(columns=["time"]))
        rec["dong_metric"] = {"goc": len(m), "giam1": len(m1), "giam2": len(m2),
                              "giam2_normal": int((m2["time"] < it).sum()), "giam2_anomal": int((m2["time"] >= it).sum()),
                              "giam1_normal": int((m1["time"] < it).sum()), "giam1_anomal": int((m1["time"] >= it).sum())}
        rec["cot_metric_song_sot_giam2"] = len([c for c in nn2.columns if c in an2.columns])
        an1 = bo_hang_so(m1[m1["time"] >= it].drop(columns=["time"]))
        nn1 = bo_hang_so(m1[m1["time"] < it].drop(columns=["time"]))
        rec["cot_metric_song_sot_giam1"] = len([c for c in nn1.columns if c in an1.columns])
        rec["cot_metric_khong_hang"] = int(bo_hang_so(m.drop(columns=["time"])).shape[1])
        # chỉ số dòng: metric sau giảm hai lần và logts sau cắt
        rec["chi_so_metric_giam2"] = [int(i) for i in m2.index[:8]]
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    out.close()


if __name__ == "__main__":
    main()
