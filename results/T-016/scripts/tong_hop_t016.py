r"""T-016 S7/S8/S10/S11: chấm điểm và tổng hợp giá trị trung gian các khối của harness.

Chạy bằng python của D:\RCA-ext\envs\py312-pin (có RCAEval Evaluator). Chấm bằng hàm cham() của
results/T-006/scripts/cham.py (đúng cách gộp của main.py: service = x.split("_")[0].replace("-db",""), bỏ trùng).
Nhãn (service gốc) chỉ lấy từ tên file kết quả để chấm.

Cách dùng: python tong_hop_t016.py --khoi <tên>=<thư mục khối> [...] --ra <json> [--md <bảng markdown>]
Mỗi khối là thư mục do chay_torai.py tạo, có seed<k>/ chứa <ca>.json và meta.jsonl.
"""
import argparse
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "results" / "T-006" / "scripts"))
from cham import cham  # noqa: E402
from RCAEval.benchmark.evaluation import Evaluator  # noqa: E402
from RCAEval.classes.graph import Node  # noqa: E402


def xep_muc_nghiem_trong(tg):
    """Thứ hạng 'chỉ mức nghiêm trọng' dựng lại từ giá trị trung gian: cụm theo điểm cụm giảm dần, trong cụm theo
    điểm service giảm dần (đúng nhánh dự phòng torai.py:283-293, 330-334). Trả cả thứ hạng SeverityScorer
    (không cụm, chỉ theo trung bình vectơ, như ablation Bảng 9)."""
    sv = tg["service_list"]
    X = np.asarray(tg["X_train"])
    y = X.mean(axis=1)
    yp = np.asarray(tg["y_pred"])
    cum = sorted([(c, float(np.mean(y[yp == c]))) for c in sorted(set(yp.tolist()))], key=lambda t: t[1], reverse=True)
    out = []
    for c, _ in cum:
        idx = np.where(yp == c)[0]
        out += [sv[i] for i, _ in sorted(zip(idx, y[idx]), key=lambda t: t[1], reverse=True)]
    sev = [sv[i] for i, _ in sorted(enumerate(y), key=lambda t: t[1], reverse=True)]
    return out, sev


def cham_ds(ds):
    """ds: {ca: [service,...]} → AVERAGE AC@1, AC@3, Avg@5 (mức service)."""
    ev = Evaluator(max_k=5)
    for ca, r in ds.items():
        ev.add_case(ranks=[Node(x, "unknown") for x in r], answer=Node(ca.split("_")[0], "unknown"))
    return {"AC1": ev.accuracy(1), "AC3": ev.accuracy(3), "Avg5": ev.average(5), "n": ev.num}


def mot_khoi(ten, d):
    d = Path(d)
    seeds = sorted([p for p in d.glob("seed*") if p.is_dir()], key=lambda p: int(p.name[4:]))
    kq = {"ten": ten, "thu_muc": str(d), "seeds": {}}
    thu_hang = {}
    for sd in seeds:
        out, kiem, per_case = cham(str(sd))
        meta = [json.loads(x) for x in open(sd / "meta.jsonl", encoding="utf-8")] if (sd / "meta.jsonl").exists() else []
        giay = [m["giay"] for m in meta if m.get("trang_thai") == "ok"]
        loi = [m["ca"] for m in meta if m.get("trang_thai") == "loi"]
        r = {"diem": out, "kiem": {k: kiem[k] for k in ("so_file", "file_error", "rank_rong", "do_dai_rank")},
             "so_ca_loi": len(loi), "ca_loi": loi[:10],
             "giay_tong": sum(giay), "giay_tb": (sum(giay) / len(giay)) if giay else None,
             "giay_max": max(giay) if giay else None}
        # giá trị trung gian
        cum_ge2 = du_phong = so_ca_trung_mnt = ca_moi_cum_1 = 0
        cot_metric_vao, cot_log_vao, dong_vao, dong0 = [], [], Counter(), 0
        rcd_rong = 0
        ds_mnt, ds_sev = {}, {}
        so_ca_tg = 0
        for m in meta:
            tg = m.get("trung_gian")
            if not tg or "service_list" not in tg:
                continue
            so_ca_tg += 1
            cums = tg.get("cum", [])
            cum_ge2 += len(cums)
            du_phong += sum(1 for c in cums if c["du_phong"])
            rcd_rong += sum(1 for c in cums if not c["rcd_ranks"])
            if not cums:
                ca_moi_cum_1 += 1
            for c in cums:
                rv = c.get("rcd_vao")
                if rv:
                    cot_metric_vao.append(rv["cot_metric"])
                    cot_log_vao.append(rv["cot_log"])
                    dong_vao[(rv["dong_normal"], rv["dong_anomal"])] += 1
                    dong0 += rv["dong_toan_0_normal"] + rv["dong_toan_0_anomal"]
            mnt, sev = xep_muc_nghiem_trong(tg)
            ds_mnt[m["ca"]] = mnt
            ds_sev[m["ca"]] = sev
            f = sd / f"{m['ca']}.json"
            if f.exists():
                ranks = [x.split("_")[0] for x in json.loads(f.read_text())["0"]]
                so_ca_trung_mnt += int(ranks == mnt)
        if so_ca_tg:
            r["trung_gian"] = {
                "so_ca_co_thu_thap": so_ca_tg, "so_cum_chay_rcd": cum_ge2, "so_cum_du_phong": du_phong,
                "ty_le_cum_du_phong": du_phong / cum_ge2 if cum_ge2 else None, "so_cum_rcd_rong": rcd_rong,
                "so_ca_moi_cum_1_service": ca_moi_cum_1,
                "so_ca_thu_hang_trung_chi_muc_nghiem_trong": so_ca_trung_mnt,
                "cot_metric_vao_rcd": {"min": min(cot_metric_vao), "max": max(cot_metric_vao),
                                       "tb": st.mean(cot_metric_vao), "so_cum_0_cot": sum(1 for v in cot_metric_vao if v == 0)}
                if cot_metric_vao else None,
                "cot_log_vao_rcd": {"min": min(cot_log_vao), "max": max(cot_log_vao)} if cot_log_vao else None,
                "dong_vao_rcd": {f"{a}+{b}": n for (a, b), n in dong_vao.most_common(5)},
                "dong_toan_0": dong0,
                "diem_chi_muc_nghiem_trong_co_cum": cham_ds(ds_mnt),
                "diem_severity_scorer_khong_cum": cham_ds(ds_sev),
            }
        kq["seeds"][sd.name] = r
        thu_hang[sd.name] = {p.stem: json.loads(p.read_text())["0"] for p in sd.glob("*.json")
                             if not p.name.endswith("_failed.json") and p.name != "lenh.json"}
    # biến thiên giữa các seed
    ten_seed = list(thu_hang)
    if len(ten_seed) > 1:
        ca_chung = set.intersection(*[set(v) for v in thu_hang.values()])
        khac = sum(1 for c in ca_chung if len({tuple(thu_hang[s][c]) for s in ten_seed}) > 1)
        khac_top1 = sum(1 for c in ca_chung if len({thu_hang[s][c][0] for s in ten_seed}) > 1)
        avg = [kq["seeds"][s]["diem"]["AVERAGE"]["Avg5"] for s in ten_seed]
        ac1 = [kq["seeds"][s]["diem"]["AVERAGE"]["AC1"] for s in ten_seed]
        ac3 = [kq["seeds"][s]["diem"]["AVERAGE"]["AC3"] for s in ten_seed]
        kq["giua_seed"] = {"so_seed": len(ten_seed), "so_ca_chung": len(ca_chung), "so_ca_thu_hang_khac": khac,
                           "so_ca_top1_khac": khac_top1,
                           "Avg5": {"tb": st.mean(avg), "sd": st.stdev(avg), "min": min(avg), "max": max(avg)},
                           "AC1": {"tb": st.mean(ac1), "sd": st.stdev(ac1), "min": min(ac1), "max": max(ac1)},
                           "AC3": {"tb": st.mean(ac3), "sd": st.stdev(ac3), "min": min(ac3), "max": max(ac3)}}
        loi_ds = sorted({k for s in ten_seed for k in kq["seeds"][s]["diem"] if k != "AVERAGE"})
        kq["giua_seed"]["Avg5_theo_loi_tb"] = {k: st.mean([kq["seeds"][s]["diem"][k]["Avg5"] for s in ten_seed])
                                               for k in loi_ds}
    return kq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--khoi", action="append", required=True)
    ap.add_argument("--ra", required=True)
    a = ap.parse_args()
    out = {}
    for k in a.khoi:
        ten, d = k.split("=", 1)
        out[ten] = mot_khoi(ten, d)
        g = out[ten].get("giua_seed")
        s0 = next(iter(out[ten]["seeds"].values()))
        tg = s0.get("trung_gian", {})
        if g:
            print(f"{ten}: Avg5 tb {g['Avg5']['tb']:.3f} sd {g['Avg5']['sd']:.3f} [{g['Avg5']['min']:.3f},{g['Avg5']['max']:.3f}] "
                  f"AC1 tb {g['AC1']['tb']:.3f} AC3 tb {g['AC3']['tb']:.3f}; ca thứ hạng khác giữa seed {g['so_ca_thu_hang_khac']}/{g['so_ca_chung']}")
        else:
            d0 = s0["diem"]["AVERAGE"]
            print(f"{ten}: Avg5 {d0['Avg5']:.3f} AC1 {d0['AC1']:.3f} AC3 {d0['AC3']:.3f} (1 seed)")
        if tg:
            print(f"   dự phòng {tg['so_cum_du_phong']}/{tg['so_cum_chay_rcd']} cụm; ca trùng thứ hạng chỉ-mức-nghiêm-trọng "
                  f"{tg['so_ca_thu_hang_trung_chi_muc_nghiem_trong']}/{tg['so_ca_co_thu_thap']}; cột metric vào RCD {tg['cot_metric_vao_rcd']}")
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
