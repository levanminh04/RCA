r"""T-016 S0/S10: chứng minh hai bản dữ liệu là cùng một ca, trước khi dùng (prompt T-016, gioi_han).

So:
  (1) mốc tiêm: inject_time.txt của bản torai (nếu bản RCAEval có inject_time.txt thì so trực tiếp; nếu không,
      so với thời điểm đầu + 720 s, vì RCAEval cắt file đối xứng ±720 s quanh mốc tiêm, REVIEW T-002 R1);
  (2) metric: simple_metrics.csv (torai) với metrics.parquet (RCAEval): cùng tập cột, cùng cột time,
      mọi giá trị bằng nhau (NaN coi là bằng NaN). Vì CSV của torai ghi 16 chữ số có nghĩa, "trùng" nghĩa là
      mọi ô lệch không quá ngưỡng làm tròn (rtol 1e-12, atol 1e-15); báo kèm số ô lệch chính xác và sai số
      tương đối lớn nhất.
Chạy bằng envs/T-016-cong-cu (có pyarrow).
Cách dùng: python kiem_cung_ca.py --cap <thư mục torai>=<thư mục RCAEval> [...] --ra <file json>
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def so_ca(d_torai, d_re):
    d_torai, d_re = Path(d_torai), Path(d_re)
    a = pd.read_csv(d_torai / "simple_metrics.csv")
    b = pd.read_parquet(d_re / "metrics.parquet")
    kq = {"torai": str(d_torai), "rcaeval": str(d_re)}
    it_a = int(open(d_torai / "inject_time.txt").read().strip())
    kq["moc_tiem_torai"] = it_a
    if (d_re / "inject_time.txt").exists():
        it_b = int(open(d_re / "inject_time.txt").read().strip())
        kq["moc_tiem_rcaeval"] = it_b
        kq["moc_tiem_trung"] = it_a == it_b
        kq["cach_so_moc"] = "inject_time.txt hai bên"
    else:
        kq["moc_tiem_rcaeval"] = None
        kq["moc_tiem_trung"] = it_a == int(b["time"].min()) + 720
        kq["cach_so_moc"] = "torai inject_time == time.min() RCAEval + 720"
    ca, cb = set(a.columns), set(b.columns)
    kq["so_cot_torai"], kq["so_cot_rcaeval"] = len(ca), len(cb)
    kq["cot_chi_torai"], kq["cot_chi_rcaeval"] = sorted(ca - cb), sorted(cb - ca)
    kq["so_dong_torai"], kq["so_dong_rcaeval"] = len(a), len(b)
    chung = sorted(ca & cb)
    m = a[chung].reset_index(drop=True).merge(b[chung].reset_index(drop=True), on="time", how="outer",
                                               suffixes=("_a", "_b"), indicator=True)
    kq["dong_chi_mot_ben"] = int((m["_merge"] != "both").sum())
    lech = lech_tol = 0
    o = 0
    rel_max = 0.0
    for c in chung:
        if c == "time":
            continue
        x, y = m[c + "_a"].to_numpy(dtype=float), m[c + "_b"].to_numpy(dtype=float)
        nan_x, nan_y = np.isnan(x), np.isnan(y)
        bang = (x == y) | (nan_x & nan_y)
        # CSV của torai ghi số thực 16 chữ số có nghĩa; parquet giữ float64 đầy đủ.
        gan = (nan_x & nan_y) | (~nan_x & ~nan_y & np.isclose(x, y, rtol=1e-12, atol=1e-15))
        lech += int((~bang).sum())
        lech_tol += int((~gan).sum())
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.abs(x - y) / np.abs(y)
        r = r[np.isfinite(r)]
        if r.size:
            rel_max = max(rel_max, float(r.max()))
        o += len(bang)
    kq["so_o_so"], kq["so_o_lech_chinh_xac"], kq["so_o_lech_qua_lam_tron"] = o, lech, lech_tol
    kq["sai_so_tuong_doi_lon_nhat"] = rel_max
    kq["trung"] = bool(kq["moc_tiem_trung"] and not kq["cot_chi_torai"] and not kq["cot_chi_rcaeval"]
                       and kq["dong_chi_mot_ben"] == 0 and lech_tol == 0)
    return kq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", action="append", required=True)
    ap.add_argument("--ra", required=True)
    a = ap.parse_args()
    out = [so_ca(*c.split("=", 1)) for c in a.cap]
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in out:
        print(("TRUNG " if k["trung"] else "KHONG-TRUNG ") + k["torai"], "lech chinh xac", k["so_o_lech_chinh_xac"],
              "lech qua lam tron", k["so_o_lech_qua_lam_tron"], "/", k["so_o_so"], "rel max", k["sai_so_tuong_doi_lon_nhat"],
              k["cach_so_moc"])


if __name__ == "__main__":
    main()
