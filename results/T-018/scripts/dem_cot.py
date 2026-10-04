"""T-018 B2: thống kê bộ cột metric của 30 ca dev RE2-TT (không chạy phương pháp, không dùng nhãn khi đếm).

Chạy bằng D:/RCA-ext/envs/py312/Scripts/python.exe. Chỉ đọc metrics.parquet. Mốc tiêm dùng để tách đoạn trước mốc
(đoạn mà GDN dùng làm dữ liệu bình thường), như T-005.

Đầu ra results/T-018/cot-re2tt/:
  ca.csv    mỗi ca: số cột thô, số cột sau làm sạch, số cột thiếu so với L*, bước thời gian, ô thiếu
  cot.csv   mỗi cột (sau làm sạch): số ca có cột, số ca cột hằng trước mốc, tỷ lệ bước đổi giá trị (trung vị qua ca),
            độ dài đoạn giá trị lặp (trung vị), số ô thiếu đầu file (trung vị)
  loai.csv  theo loại metric (phần sau dấu '_' cuối): tổng hợp các chỉ số trên
  cot-khong-du-30-ca.csv  cột không có ở đủ 30 ca và các ca thiếu nó (để phân tích sau, B2b)
"""
import json
import os

import numpy as np
import pandas as pd

REPO = r"D:\RCA-flashticket"
DATA = os.path.join(REPO, "data", "rcaeval")
MOC = r"D:\RCA-ext\work\T-018\nguon\rcaeval-inject"
OUT = os.path.join(REPO, "results", "T-018", "cot-re2tt")


def moc(ca):
    return int(open(os.path.join(MOC, ca, "inject_time.txt")).readline().strip())


def loai(c):
    return c.rsplit("_", 1)[-1] if "_" in c else c


def main():
    os.makedirs(OUT, exist_ok=True)
    dev = sorted(c for c in os.listdir(DATA) if c.startswith("re2tt_"))
    rows, per_col = [], {}
    sets = {}
    for ca in dev:
        raw = pd.read_parquet(os.path.join(DATA, ca, "metrics.parquet"))
        t = raw["time"].to_numpy()
        dt = np.diff(t)
        df = raw.drop(columns=[c for c in ["time.1"] if c in raw])
        df = df.loc[:, ~df.columns.str.endswith("_latency-50")]
        df = df.rename(columns={c: c.replace("_latency-90", "_latency") for c in df.columns if c.endswith("_latency-90")})
        cols = [c for c in df.columns if c != "time"]
        sets[ca] = set(cols)
        pre = df[df["time"] < moc(ca)][cols].replace([np.inf, -np.inf], np.nan)
        n_inf = int(np.isinf(raw.drop(columns=["time"]).select_dtypes("number").to_numpy()).sum())
        rows.append({"ca": ca, "n_cot_tho": raw.shape[1] - 1, "n_cot_sach": len(cols), "n_dong": len(raw),
                     "buoc_time_khac_1s": int((dt != 1).sum()), "o_thieu": int(df[cols].isna().sum().sum()),
                     "o_inf": n_inf})
        filled = pre.ffill().fillna(0)
        for c in cols:
            x = pre[c].to_numpy(dtype=float)
            ok = ~np.isnan(x[1:]) & ~np.isnan(x[:-1])
            doi = (np.diff(x)[ok] != 0) if ok.any() else np.array([])
            # độ dài các đoạn giá trị lặp (trên chuỗi đã ffill, như GDN thấy)
            y = filled[c].to_numpy(dtype=float)
            ranh = np.flatnonzero(np.diff(y) != 0)
            runs = np.diff(np.concatenate([[-1], ranh, [len(y) - 1]]))
            lead = int(np.argmax(~np.isnan(x))) if (~np.isnan(x)).any() else len(x)
            d = per_col.setdefault(c, {"so_ca": 0, "hang_truoc_moc": 0, "ty_le_doi": [], "doan_lap_trung_vi": [],
                                       "o_thieu_dau": []})
            d["so_ca"] += 1
            d["hang_truoc_moc"] += int(np.nanmax(y) == np.nanmin(y))
            d["ty_le_doi"].append(float(doi.mean()) if doi.size else np.nan)
            d["doan_lap_trung_vi"].append(float(np.median(runs)))
            d["o_thieu_dau"].append(lead)
    lstar = set.intersection(*sets.values())
    hop = set.union(*sets.values())
    for r in rows:
        r["n_cot_thieu_so_voi_hop"] = len(hop - sets[r["ca"]])
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "ca.csv"), index=False)
    cr = []
    for c, d in sorted(per_col.items()):
        cr.append({"cot": c, "loai": loai(c), "so_ca": d["so_ca"], "hang_truoc_moc_so_ca": d["hang_truoc_moc"],
                   "ty_le_buoc_doi_trung_vi": float(np.nanmedian(d["ty_le_doi"])) if not np.all(np.isnan(d["ty_le_doi"])) else np.nan,
                   "doan_lap_trung_vi_s": float(np.median(d["doan_lap_trung_vi"])),
                   "o_thieu_dau_trung_vi": float(np.median(d["o_thieu_dau"]))})
    cdf = pd.DataFrame(cr)
    cdf.to_csv(os.path.join(OUT, "cot.csv"), index=False)
    g = cdf.groupby("loai").agg(so_cot=("cot", "count"), co_du_30_ca=("so_ca", lambda s: int((s == 30).sum())),
                                ty_le_doi_trung_vi=("ty_le_buoc_doi_trung_vi", "median"),
                                doan_lap_trung_vi_s=("doan_lap_trung_vi_s", "median"),
                                cot_hang_o_moi_ca=("hang_truoc_moc_so_ca", lambda s: int((s == cdf.loc[s.index, "so_ca"]).sum())),
                                o_thieu_dau_trung_vi=("o_thieu_dau_trung_vi", "median"))
    g.to_csv(os.path.join(OUT, "loai.csv"))
    thieu = [{"cot": c, "so_ca_co": per_col[c]["so_ca"], "ca_thieu": ";".join(sorted(ca for ca in dev if c not in sets[ca]))}
             for c in sorted(hop - lstar)]
    pd.DataFrame(thieu).to_csv(os.path.join(OUT, "cot-khong-du-30-ca.csv"), index=False)
    tom = {"so_ca": len(dev), "n_cot_tho_min_max": [int(min(r["n_cot_tho"] for r in rows)), int(max(r["n_cot_tho"] for r in rows))],
           "n_cot_sach_min_max": [int(min(r["n_cot_sach"] for r in rows)), int(max(r["n_cot_sach"] for r in rows))],
           "giao_L*": len(lstar), "hop": len(hop), "cot_khong_du_30_ca": len(hop - lstar),
           "ca_co_buoc_time_khac_1s": int(sum(r["buoc_time_khac_1s"] > 0 for r in rows)),
           "tong_o_thieu": int(sum(r["o_thieu"] for r in rows)), "tong_o_inf": int(sum(r["o_inf"] for r in rows))}
    json.dump(tom, open(os.path.join(OUT, "tom-tat.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(tom, ensure_ascii=False))
    print(g.to_string())


if __name__ == "__main__":
    main()
