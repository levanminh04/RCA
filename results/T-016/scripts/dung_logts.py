r"""T-016 S9: dựng logts.csv, tracets_err.csv, tracets_lat.csv từ log và trace thô (định dạng RCAEval RE2),
rồi so với bản Figshare của TORAI (đã chứng minh cùng ca ở S0).

Chạy bằng D:\RCA-ext\envs\T-016-cong-cu (pandas, pyarrow, drain3, scipy). Không gọi code TORAI/RCAEval.

Cách dùng:
  python dung_logts.py --tho <thư mục ca RCAEval: logs.parquet, traces.parquet>
                       --mau <thư mục ca torai: logts.csv, tracets_*.csv> --ra <thư mục ra> [--che-do-log A|B|C ...]

Đặc tả đã dò ra (xem dung-logts-tracets.md):
- Lưới thời gian: bin 15 s, bắt đầu ở t0 = thời điểm nhỏ nhất của log (giây Unix); bin k = [t0+15k, t0+15k+15).
- tracets: cột = "<service>_<method>", với operationName dạng "[/][pkg.]Service/Method" thì service = Service viết
  thường (ví dụ hipstershop.CartService/GetCart → cartservice_GetCart; grpc.health.v1.Health/Check → health_Check);
  ngược lại cột = "<serviceName>_<operationName>" (span gốc "frontend" của frontendservice → frontendservice_frontend).
  Thời điểm span = startTime (micro giây) // 1e6.
  tracets_err[bin, cột] = TỔNG statusCode của các span (mã gRPC: 0 = OK, 14 = UNAVAILABLE, ...).
  tracets_lat[bin, cột] = SỐ span có duration > mean + 3·std của chính cột đó, mean/std tính trên TOÀN file
  (kể cả sau mốc tiêm; std của pandas, ddof = 1).
- logts: Drain (drain3) tách mẫu log; ô = số dòng log của mẫu đó trong bin. Ba chế độ thử:
  A: một Drain cho mọi service, cột = "<container>_<id cụm>", id theo thứ tự cụm được tạo;
  B: Drain riêng cho từng service, id toàn cục tăng dần theo thứ tự mẫu mới xuất hiện (theo thời gian);
  C: một Drain cho mọi service trên chuỗi "<container> <message>" (tương đương B về tách theo service).
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

BIN = 15


def ten_cot_trace(op, svc):
    m = re.match(r"^/?(?:[\w]+\.)*([A-Za-z]+)/(\w+)$", op)
    return f"{m.group(1).lower()}_{m.group(2)}" if m else f"{svc}_{op}"


def dung_tracets(traces, t0, t_cuoi):
    t = traces.copy()
    t["cot"] = [ten_cot_trace(o, s) for o, s in zip(t["operationName"], t["serviceName"])]
    t["giay"] = t["startTime"] // 1_000_000
    t = t[(t["giay"] >= t0) & (t["giay"] < t_cuoi)]
    t["bin"] = t0 + ((t["giay"] - t0) // BIN) * BIN
    err = t.groupby(["bin", "cot"])["statusCode"].sum().unstack()
    st = t.groupby("cot")["duration"].agg(["mean", "std"])
    nguong = t["cot"].map(st["mean"] + 3 * st["std"])
    lat = t[t["duration"] > nguong].groupby(["bin", "cot"]).size().unstack()
    cot = sorted(t["cot"].unique())
    idx = np.arange(t0, t_cuoi, BIN)
    err = err.reindex(index=idx, columns=cot).fillna(0)
    lat = lat.reindex(index=idx, columns=cot).fillna(0)
    err.index.name = lat.index.name = "time"
    return err, lat


def dung_logts(logs, t0, t_cuoi, che_do, sim_th=0.4, depth=4):
    from drain3 import TemplateMiner
    from drain3.template_miner_config import TemplateMinerConfig

    def miner():
        c = TemplateMinerConfig()
        c.drain_sim_th = sim_th
        c.drain_depth = depth
        c.profiling_enabled = False
        return TemplateMiner(config=c)

    lg = logs[(logs["timestamp"] >= t0) & (logs["timestamp"] < t_cuoi)].sort_values("timestamp", kind="stable")
    cot = []
    if che_do == "A":
        tm = miner()
        for svc, msg in zip(lg["container_name"], lg["message"]):
            cot.append(f"{svc}_{tm.add_log_message(str(msg))['cluster_id']}")
    elif che_do == "B":
        tms, map_id, dem = {}, {}, 0
        for svc, msg in zip(lg["container_name"], lg["message"]):
            tm = tms.setdefault(svc, miner())
            cid = tm.add_log_message(str(msg))["cluster_id"]
            if (svc, cid) not in map_id:
                dem += 1
                map_id[(svc, cid)] = dem
            cot.append(f"{svc}_{map_id[(svc, cid)]}")
    elif che_do == "C":
        tm = miner()
        for svc, msg in zip(lg["container_name"], lg["message"]):
            cot.append(f"{svc}_{tm.add_log_message(f'{svc} {msg}')['cluster_id']}")
    else:
        raise ValueError(che_do)
    lg = lg.assign(cot=cot, bin=t0 + ((lg["timestamp"] - t0) // BIN) * BIN)
    out = lg.groupby(["bin", "cot"]).size().unstack()
    out = out.reindex(index=np.arange(t0, t_cuoi, BIN)).fillna(0)
    out.index.name = "time"
    return out


def so_theo_ten(mine, mau):
    """tracets: ghép cột theo tên. Ô trùng = bằng nhau sau khi coi NaN của bản mẫu là 0 (torai ffill rồi điền 0)."""
    idx = mau.index
    m = mine.reindex(index=idx, columns=mau.columns).fillna(0).to_numpy(float)
    g = mau.to_numpy(float)
    nan = np.isnan(g)
    trung = np.isclose(m, np.nan_to_num(g))
    return {"so_o": int(g.size), "o_trung": int(trung.sum()), "ty_le": float(trung.mean()),
            "o_nan_ban_mau": int(nan.sum()), "o_lech_ngoai_nan": int((~trung & ~nan).sum()),
            "cot_chi_ban_dung": sorted(set(mine.columns) - set(mau.columns)),
            "cot_chi_ban_mau": sorted(set(mau.columns) - set(mine.columns))}


def so_hungarian(mine, mau):
    """logts: trong từng service, ghép cột một-một bằng phép gán cực đại số ô bằng nhau (luật ghi trong SPEC S9).
    Cột không ghép được tính là sai toàn bộ. Tỉ lệ là cận trên vì phép gán chọn cách ghép có lợi nhất."""
    idx = mau.index
    mine = mine.reindex(index=idx).fillna(0)
    svc = lambda c: c.rsplit("_", 1)[0]  # noqa: E731
    tong_o = int(mau.size)
    trung = 0
    chi_tiet = {}
    ghep = {}
    for s in sorted({svc(c) for c in mau.columns} | {svc(c) for c in mine.columns}):
        a = [c for c in mau.columns if svc(c) == s]
        b = [c for c in mine.columns if svc(c) == s]
        if not a:
            chi_tiet[s] = {"cot_mau": 0, "cot_dung": len(b), "o_trung": 0}
            continue
        if not b:
            chi_tiet[s] = {"cot_mau": len(a), "cot_dung": 0, "o_trung": 0}
            continue
        M = np.zeros((len(a), len(b)))
        for i, ca in enumerate(a):
            x = mau[ca].to_numpy(float)
            for j, cb in enumerate(b):
                M[i, j] = np.isclose(x, mine[cb].to_numpy(float)).sum()
        r, c = linear_sum_assignment(-M)
        tr = int(M[r, c].sum())
        trung += tr
        for i, j in zip(r, c):
            ghep[a[i]] = {"cot_dung": b[j], "o_trung": int(M[i, j]), "so_dong": len(idx)}
        chi_tiet[s] = {"cot_mau": len(a), "cot_dung": len(b), "o_trung": tr, "o_mau": len(a) * len(idx)}
    cot_khop_hoan_toan = sum(1 for v in ghep.values() if v["o_trung"] == v["so_dong"])
    # Chỉ số phụ (thêm sau khi thấy lệch do mốc thời gian, xem SPEC "Thay đổi trong lúc làm"): ghép lại trong từng
    # service bằng phép gán cực đại tương quan theo bin, rồi đếm cặp có TỔNG bằng nhau (kiểm phần tách mẫu Drain,
    # không phụ thuộc biên bin) và tương quan trung bình.
    cap_tong_bang, tuong_quan = 0, []
    for s in sorted({svc(c) for c in mau.columns}):
        a = [c for c in mau.columns if svc(c) == s]
        b = [c for c in mine.columns if svc(c) == s]
        if not a or not b:
            continue
        C = np.zeros((len(a), len(b)))
        for i, ca in enumerate(a):
            x = mau[ca].to_numpy(float)
            for j, cb in enumerate(b):
                y = mine[cb].to_numpy(float)
                C[i, j] = np.corrcoef(x, y)[0, 1] if x.std() > 0 and y.std() > 0 else (1.0 if np.allclose(x, y) else 0.0)
                if np.isclose(x.sum(), y.sum()):
                    C[i, j] += 10.0  # ưu tiên cặp cùng tổng
        r, c = linear_sum_assignment(-C)
        for i, j in zip(r, c):
            tong_bang = np.isclose(mau[a[i]].sum(), mine[b[j]].sum())
            cap_tong_bang += int(tong_bang)
            tuong_quan.append(C[i, j] - (10.0 if tong_bang else 0.0))
    # R1 (REVIEW T-016): tỉ lệ toàn bảng theo SPEC S9 — mẫu số tính cả cột thừa của bản dựng:
    # số dòng × Σ_service max(cột mẫu, cột dựng). Tỉ lệ cũ (mẫu số = bảng mẫu) chỉ là độ phủ bảng mẫu.
    mau_so_toan_bang = len(idx) * sum(max(v["cot_mau"], v["cot_dung"]) for v in chi_tiet.values())
    return {"ty_le_toan_bang": trung / mau_so_toan_bang if mau_so_toan_bang else None,
            "mau_so_toan_bang": mau_so_toan_bang, "cap_cung_tong": cap_tong_bang, "tuong_quan_tb": float(np.mean(tuong_quan)) if tuong_quan else None,
            "so_o": tong_o, "o_trung": trung, "do_phu_bang_mau": trung / tong_o if tong_o else None,
            "so_cot_mau": int(mau.shape[1]), "so_cot_dung": int(mine.shape[1]),
            "so_cot_khop_hoan_toan": cot_khop_hoan_toan, "theo_service": chi_tiet, "ghep": ghep}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tho", required=True)
    ap.add_argument("--mau", required=True)
    ap.add_argument("--ra", required=True)
    ap.add_argument("--che-do-log", default="A,B,C")
    ap.add_argument("--sim-th", default="0.4")
    a = ap.parse_args()
    tho, mau, ra = Path(a.tho), Path(a.mau), Path(a.ra)
    ra.mkdir(parents=True, exist_ok=True)
    logs = pd.read_parquet(tho / "logs.parquet")
    traces = pd.read_parquet(tho / "traces.parquet")
    lt_mau = pd.read_csv(mau / "logts.csv").set_index("time")
    te_mau = pd.read_csv(mau / "tracets_err.csv").set_index("time")
    tl_mau = pd.read_csv(mau / "tracets_lat.csv").set_index("time")
    t0 = int(logs["timestamp"].min())
    t_cuoi = t0 + BIN * (int((max(logs["timestamp"].max(), traces["startTime"].max() // 1_000_000) - t0) // BIN) + 1)
    kq = {"t0": t0, "t0_ban_mau_logts": int(lt_mau.index.min()), "t0_ban_mau_tracets": int(te_mau.index.min()),
          "so_dong_ban_mau": {"logts": len(lt_mau), "tracets": len(te_mau)}, "bin_s": BIN}
    err, lat = dung_tracets(traces, t0, t_cuoi)
    err.to_csv(ra / "tracets_err.csv")
    lat.to_csv(ra / "tracets_lat.csv")
    kq["tracets_err"] = so_theo_ten(err, te_mau)
    kq["tracets_lat"] = so_theo_ten(lat, tl_mau)
    kq["logts"] = {}
    for sim in [float(x) for x in a.sim_th.split(",")]:
        for cd in a.che_do_log.split(","):
            lt = dung_logts(logs, t0, t_cuoi, cd, sim_th=sim)
            lt.to_csv(ra / f"logts_{cd}_sim{sim}.csv")
            r = so_hungarian(lt, lt_mau)
            kq["logts"][f"{cd}_sim{sim}"] = r
            print(f"logts che_do={cd} sim={sim}: cột dựng {r['so_cot_dung']} / mẫu {r['so_cot_mau']}, "
                  f"cột khớp hoàn toàn {r['so_cot_khop_hoan_toan']}, tỉ lệ ô toàn bảng {r['ty_le_toan_bang']:.4f} "
                  f"(độ phủ bảng mẫu {r['do_phu_bang_mau']:.4f}), "
                  f"cặp cùng tổng {r['cap_cung_tong']}, tương quan TB {r['tuong_quan_tb']:.3f}")
    print("tracets_err", round(kq["tracets_err"]["ty_le"], 4), "lệch ngoài NaN", kq["tracets_err"]["o_lech_ngoai_nan"])
    print("tracets_lat", round(kq["tracets_lat"]["ty_le"], 4), "lệch ngoài NaN", kq["tracets_lat"]["o_lech_ngoai_nan"])
    (ra / "so-sanh.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
