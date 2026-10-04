r"""T-016 S3: harness chạy TORAI (gốc, sửa) và RCD trên từng ca, dựng đầu vào đúng như main.py RCAEval 259ea41.

Chạy bằng python của D:\RCA-ext\envs\py38-rcdlock (hoặc môi trường Python 3.8 cùng bộ gói trên EC2).

Đầu vào dựng như main.py:268-417 (không đổi gì):
- đọc simple_metrics.csv; bỏ cột "time.1"; bỏ cột *_latency-50; với torai-TT chỉ giữ cột bắt đầu bằng "ts-" (+ time);
- thay inf bằng NaN, ffill, điền 0;
- mốc tiêm = dòng đầu inject_time.txt (+ tdelta = 0);
- metric: L*30 dòng trước mốc (tail) + L*30 dòng từ mốc (head), L = --length (phút);
- đổi tên *_latency-90 → *_latency;
- torai: logts.csv, tracets_err.csv, tracets_lat.csv (nếu có), mỗi bảng L*2 dòng trước + L*2 dòng từ mốc;
- gọi phương pháp với dataset=<tên dataset>, anomalies=None, dk_select_useful=False, sli=None, verbose=False.
  (main.py truyền sli suy từ tên service gốc; torai và rcd không đọc sli, xem T-006 mục 2.4. Ở đây truyền None.)

Khác main.py, chỉ ở phần điều khiển chạy:
- --seeds: trước MỖI lời gọi phương pháp, np.random.seed(seed). main.py không đặt seed (kết quả T-006 không lặp lại được).
- Mỗi ca chạy trong try/except: lỗi thì ghi <ca>_failed.json, không dừng cả lượt, không chấm như dự đoán (MRP P3).
  main.py thì `raise e` (dừng cả lượt).
- --thu-thap: cài wrapper CHỈ QUAN SÁT (không đổi đối số, không tiêu số ngẫu nhiên) để ghi giá trị trung gian.
- --hoan-vi-cot <seed>: hoán vị thứ tự cột metric, logts, tracets (giữ cột time) trước khi gọi phương pháp.
- --placebo: mốc giả = mốc tiêm - (L*30 + 15) giây; cả hai nửa cửa sổ đều trước mốc tiêm thật (phép thử giả).
- --khong-trace: không nạp tracets (cấu hình Metric+Log).
- --thu-tu-ca <file>: chạy theo danh sách ca trong file (mỗi dòng một đường dẫn tương đối "dịch_vụ_lỗi/số").

Nhãn: tên thư mục ca (service gốc, loại lỗi) chỉ dùng để đặt tên file kết quả, như main.py; phương pháp không nhận.

Đầu ra trong --ra:
  <service>_<lỗi>_<ca>.json         {"0": ranks}   (đúng định dạng main.py, để chấm bằng results/T-006/scripts/cham.py)
  <service>_<lỗi>_<ca>_failed.json  {"error": ...}
  tien-do.log                       mỗi ca một dòng: giờ, số thứ tự, ca, seed, giây của ca, giây cộng dồn, trạng thái
  meta.jsonl                        mỗi (ca, seed) một dòng: thời gian, RSS, số cột, lỗi, giá trị trung gian (nếu --thu-thap)
Mỗi seed ghi vào thư mục con seed<k>/.
"""
import argparse
import datetime as dt
import glob
import inspect
import json
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

import importlib  # noqa: E402

# Gói RCAEval.e2e có thuộc tính `torai`, `rcd` là HÀM (che tên module con), nên phải lấy module qua importlib.
rcd_mod = importlib.import_module("RCAEval.e2e.rcd")
torai_mod = importlib.import_module("RCAEval.e2e.torai")
sua_mod = importlib.import_module("src.torai.torai_sua")

try:
    import psutil
except Exception:  # pragma: no cover
    psutil = None


def bay_gio():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------- dựng đầu vào (main.py:268-417)
def dung_dau_vao(data_path, method, length, placebo=False, khong_trace=False, hoan_vi=None):
    data_dir = os.path.dirname(data_path)
    data = pd.read_csv(data_path)
    if "time.1" in data:
        data = data.drop(columns=["time.1"])
    data = data.loc[:, ~data.columns.str.endswith("_latency-50")]
    if "mm-tt" in data_path or "torai-TT" in data_path:
        time_col = data["time"]
        data = data.loc[:, data.columns.str.startswith("ts-")]
        data["time"] = time_col
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.ffill()
    data = data.fillna(0)
    with open(os.path.join(data_dir, "inject_time.txt")) as f:
        inject_time = int(f.readlines()[0].strip())
    if placebo:
        inject_time = inject_time - (length * 60 // 2 + 15)
    normal_df = data[data["time"] < inject_time].tail(length * 60 // 2)
    anomal_df = data[data["time"] >= inject_time].head(length * 60 // 2)
    data = pd.concat([normal_df, anomal_df], ignore_index=True)
    data = data.rename(columns={c: c.replace("_latency-90", "_latency") for c in data.columns if c.endswith("_latency-90")})
    rng = np.random.RandomState(hoan_vi) if hoan_vi is not None else None

    def hv(df):
        if rng is None or df is None or len(df.columns) == 0:
            return df
        cols = [c for c in df.columns if c != "time"]
        cols = list(rng.permutation(cols))
        return df[(["time"] if "time" in df.columns else []) + cols]

    if method == "rcd":
        return hv(data), inject_time
    logts = pd.read_csv(os.path.join(data_dir, "logts.csv"))
    traces_err = pd.DataFrame()
    traces_lat = pd.DataFrame()
    if not khong_trace:
        try:
            traces_err = pd.read_csv(os.path.join(data_dir, "tracets_err.csv"))
            traces_lat = pd.read_csv(os.path.join(data_dir, "tracets_lat.csv"))
        except FileNotFoundError:
            pass
    n = length * 4 // 2 if length else 20
    a = logts[logts["time"] < inject_time].tail(n)
    b = logts[logts["time"] >= inject_time].head(n)
    logts = pd.concat([a, b], ignore_index=True)
    if traces_err.shape[0] > 0:
        a = traces_err[traces_err["time"] < inject_time].tail(n)
        b = traces_err[traces_err["time"] >= inject_time].head(n)
        traces_err = pd.concat([a, b], ignore_index=True)
    if traces_lat.shape[0] > 0:
        a = traces_lat[traces_lat["time"] < inject_time].tail(n)
        b = traces_lat[traces_lat["time"] >= inject_time].head(n)
        traces_lat = pd.concat([a, b], ignore_index=True)
    d = {"metric": hv(data.copy(deep=True)), "logts": hv(logts), "tracets_err": hv(traces_err),
         "tracets_lat": hv(traces_lat)}
    return d, inject_time


# ---------------------------------------------------------------- thu giá trị trung gian (chỉ quan sát)
GHI = {}


def _goi_thu_thap(module_ten):
    """Wrapper quan sát. Không đổi đối số, không gọi np.random, chỉ đọc biến cục bộ của hàm gọi."""
    tm = torai_mod if module_ten == "goc" else sua_mod
    goc_rcd_multi = tm._rcd_multimodal
    goc_gmm = tm.GaussianMixture
    goc_run_pc = rcd_mod.run_pc
    goc_chunks = rcd_mod.create_chunks
    goc_rmp = tm.run_multi_phase

    class GMMGhi(goc_gmm):
        def predict(self, X):
            p = super().predict(X)
            f = inspect.currentframe().f_back.f_locals
            GHI["service_list"] = list(f.get("service_list", []))
            GHI["X_train"] = np.asarray(f.get("X_train")).tolist() if f.get("X_train") is not None else None
            GHI["bic"] = [float(x) for x in f.get("bic_score_all", [])]
            GHI["n_comp"] = int(self.n_components)
            GHI["y_pred"] = [int(x) for x in p]
            return p

    def rcd_multi_ghi(data, inject_time, **kw):
        f = inspect.currentframe().f_back.f_locals
        cum = {"services": list(f.get("services_of_this_cluster", [])),
               "aa": [(a, float(s)) for a, s in f.get("aa", [])],
               "cot_metric_vao": len([c for c in data["metric"].columns if c != "time"]),
               "cot_log_vao": len([c for c in data["logts"].columns if c != "time"])}
        GHI.setdefault("cum", []).append(cum)
        GHI["_cum_hien_tai"] = cum
        cum["pc"] = []
        out = goc_rcd_multi(data, inject_time, **kw)
        tmp = [s.split("_")[0] for s in out["ranks"]]
        inn = []
        if tmp:
            inn = [tmp[0]] + [s for i, s in enumerate(tmp) if i > 0 and s not in tmp[:i]]
        cum["rcd_ranks"] = list(out["ranks"])
        cum["noi_bo"] = inn
        cum["du_phong"] = len(inn) != len(cum["services"])
        return out

    def run_pc_ghi(data, alpha, **kw):
        cg = goc_run_pc(data, alpha, **kw)
        cum = GHI.get("_cum_hien_tai")
        if cum is not None and len(cum["pc"]) < 400:
            fchild = [*cg.nx_graph.successors("F-node")] if "F-node" in cg.nx_graph else []
            rec = {"alpha": float(alpha), "cot": list(data.columns), "so_dong": int(len(data)), "f_con": fchild}
            if os.environ.get("T016_GHI_DU_LIEU"):
                # chỉ cho ví dụ tính tay: dữ liệu đã rời rạc hóa và mọi p-value đã ghi ở hàng F-node
                rec["du_lieu"] = data.to_numpy().tolist()
                rec["p_values_F"] = [None if v is None else [float(x) for x in v] for v in cg.p_values[-1]]
                rec["so_ci"] = int(cg.no_ci_tests)
            cum["pc"].append(rec)
        return cg

    def create_chunks_ghi(df, gamma):
        ch = goc_chunks(df, gamma)
        cum = GHI.get("_cum_hien_tai")
        if cum is not None:
            cum.setdefault("so_cot_level", []).append(int(df.shape[1]))
        return ch

    def rmp_ghi(normal_df, anomal_df, *a, **k):
        cum = GHI.get("_cum_hien_tai")
        if cum is not None:
            cols = list(normal_df.columns)
            la_log = [c for c in cols if c.rsplit("_", 1)[-1].isdigit()]
            cum["rcd_vao"] = {"dong_normal": int(len(normal_df)), "dong_anomal": int(len(anomal_df)),
                              "cot": len(cols), "cot_log": len(la_log), "cot_metric": len(cols) - len(la_log),
                              "dong_toan_0_normal": int((normal_df == 0).all(axis=1).sum()),
                              "dong_toan_0_anomal": int((anomal_df == 0).all(axis=1).sum())}
        return goc_rmp(normal_df, anomal_df, *a, **k)

    def install():
        tm.run_multi_phase = rmp_ghi
        tm._rcd_multimodal = rcd_multi_ghi
        tm.GaussianMixture = GMMGhi
        rcd_mod.run_pc = run_pc_ghi
        rcd_mod.create_chunks = create_chunks_ghi

    def uninstall():
        tm.run_multi_phase = goc_rmp
        tm._rcd_multimodal = goc_rcd_multi
        tm.GaussianMixture = goc_gmm
        rcd_mod.run_pc = goc_run_pc
        rcd_mod.create_chunks = goc_chunks

    return install, uninstall


# ---------------------------------------------------------------- chạy
def goi_phuong_phap(method, data, inject_time, dataset):
    kw = dict(dataset=dataset, anomalies=None, dk_select_useful=False, sli=None, verbose=False)
    if method == "torai":
        return torai_mod.torai(data, inject_time, **kw)
    if method == "torai_sua":
        return sua_mod.torai(data, inject_time, sua_giam_mau=True, sua_ghep=True, **kw)
    if method == "torai_sua_a":
        return sua_mod.torai(data, inject_time, sua_giam_mau=True, sua_ghep=False, **kw)
    if method == "rcd":
        return rcd_mod.rcd(data, inject_time, **kw)
    raise ValueError(method)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="thư mục dataset, ví dụ D:/RCA-ext/data/torai-OB")
    ap.add_argument("--dataset", required=True, help="tên dataset truyền cho phương pháp, như main.py: torai-ob ...")
    ap.add_argument("--method", required=True, choices=["torai", "torai_sua", "torai_sua_a", "rcd"])
    ap.add_argument("--length", type=int, default=10)
    ap.add_argument("--seeds", default="0")
    ap.add_argument("--ra", required=True)
    ap.add_argument("--thu-thap", action="store_true")
    ap.add_argument("--hoan-vi-cot", type=int, default=None)
    ap.add_argument("--placebo", action="store_true")
    ap.add_argument("--khong-trace", action="store_true")
    ap.add_argument("--thu-tu-ca", default=None)
    ap.add_argument("--chi-ca", default=None, help="chỉ chạy các ca có chuỗi này trong đường dẫn (phân cách bằng ,)")
    ap.add_argument("--toi-da-ca", type=int, default=None)
    ap.add_argument("--ngan-sach-s", type=int, default=3 * 3600, help="dừng khi tổng thời gian vượt (Q-40)")
    a = ap.parse_args()

    if a.thu_tu_ca:
        rels = [x.strip() for x in open(a.thu_tu_ca, encoding="utf-8") if x.strip()]
        paths = [os.path.join(a.data, r, "simple_metrics.csv") for r in rels]
    else:
        paths = list(glob.glob(os.path.join(a.data, "**/data.csv"), recursive=True))
        if not paths:
            paths = list(glob.glob(os.path.join(a.data, "**/simple_metrics.csv"), recursive=True))
        paths = sorted(paths)
    if a.chi_ca:
        keys = a.chi_ca.split(",")
        paths = [p for p in paths if any(k in p.replace("\\", "/") for k in keys)]
    if a.toi_da_ca:
        paths = paths[: a.toi_da_ca]

    seeds = [int(s) for s in a.seeds.split(",")]
    goc_hay_sua = "goc" if a.method == "torai" else "sua"
    install = uninstall = None
    if a.thu_thap and a.method != "rcd":
        install, uninstall = _goi_thu_thap(goc_hay_sua)
    if a.thu_thap and a.method == "rcd":
        install, uninstall = _goi_thu_thap("goc")  # chỉ dùng run_pc / create_chunks

    out_root = Path(a.ra)
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "lenh.json").write_text(json.dumps({"argv": sys.argv, "bat_dau": bay_gio(), "so_ca": len(paths),
                                                    "python": sys.version, "cwd": os.getcwd()},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
    proc = psutil.Process() if psutil else None
    t_bat_dau = time.perf_counter()
    dung = False
    for seed in seeds:
        od = out_root / f"seed{seed}"
        od.mkdir(exist_ok=True)
        tdl = open(od / "tien-do.log", "a", encoding="utf-8")
        meta = open(od / "meta.jsonl", "a", encoding="utf-8")
        tdl.write(f"{bay_gio()} BAT-DAU method={a.method} length={a.length} seed={seed} so_ca={len(paths)}\n")
        tdl.flush()
        t_seed = time.perf_counter()
        for i, data_path in enumerate(paths, 1):
            data_dir = os.path.dirname(data_path)
            service, fault = os.path.basename(os.path.dirname(data_dir)).split("_")
            case = os.path.basename(data_dir)
            ten = f"{service}_{fault}_{case}"
            rp = od / f"{ten}.json"
            if rp.exists() or (od / f"{ten}_failed.json").exists():
                continue  # tiếp tục lượt bị ngắt; không chạy đè
            data, inject_time = dung_dau_vao(data_path, a.method, a.length, a.placebo, a.khong_trace, a.hoan_vi_cot)
            GHI.clear()
            rec = {"ca": ten, "seed": seed, "method": a.method, "length": a.length, "placebo": a.placebo,
                   "hoan_vi_cot": a.hoan_vi_cot, "khong_trace": a.khong_trace}
            if isinstance(data, dict):
                rec["kich_thuoc"] = {k: list(v.shape) for k, v in data.items()}
                lt = data["logts"]["time"].to_numpy() if "time" in data["logts"] else np.array([])
                rec["buoc_logts"] = sorted({int(x) for x in np.diff(lt)}) if len(lt) > 1 else []
                rec["lech_pha_logts_s"] = int((inject_time - lt[0]) % 15) if len(lt) else None
            else:
                rec["kich_thuoc"] = {"metric": list(data.shape)}
            if install:
                install()
            np.random.seed(seed)
            t0 = time.perf_counter()
            try:
                out = goi_phuong_phap(a.method, data, inject_time, a.dataset)
                dt_s = time.perf_counter() - t0
                ranks = out.get("ranks")
                rp.write_text(json.dumps({0: ranks}), encoding="utf-8")
                rec.update({"trang_thai": "ok", "giay": dt_s, "do_dai": len(ranks) if ranks is not None else None})
            except Exception as e:  # ghi ca lỗi là lỗi, không chấm như dự đoán
                dt_s = time.perf_counter() - t0
                (od / f"{ten}_failed.json").write_text(json.dumps({"error": f"{type(e).__name__}: {e}",
                                                                   "traceback": traceback.format_exc()}),
                                                        encoding="utf-8")
                rec.update({"trang_thai": "loi", "giay": dt_s, "loi": f"{type(e).__name__}: {e}"})
            finally:
                if uninstall:
                    uninstall()
            if proc:
                rec["rss_mb"] = proc.memory_info().rss / 2**20
            if GHI:
                rec["trung_gian"] = {k: v for k, v in GHI.items() if not k.startswith("_")}
            meta.write(json.dumps(rec, ensure_ascii=False) + "\n")
            meta.flush()
            tong = time.perf_counter() - t_bat_dau
            tdl.write(f"{bay_gio()} {i}/{len(paths)} {ten} seed={seed} {dt_s:.2f}s cong_don={tong:.0f}s {rec['trang_thai']}\n")
            tdl.flush()
            if tong > a.ngan_sach_s:
                tdl.write(f"{bay_gio()} VUOT-NGAN-SACH {tong:.0f}s > {a.ngan_sach_s}s\n")
                dung = True
                break
        tdl.write(f"{bay_gio()} XONG seed={seed} {time.perf_counter() - t_seed:.0f}s\n")
        tdl.close()
        meta.close()
        if dung:
            break


if __name__ == "__main__":
    main()
