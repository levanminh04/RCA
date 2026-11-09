"""H5 + H7 T-057: sức phân xử của dữ liệu và trạng thái phát hiện (RQ3a). Chỉ đọc đầu ra đã lưu.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h5_h7_phan_xu.py results/T-057/kha-nang-phan-xu.json
Nguồn: A = results/T-054/reports/main-013-v2/a4.json; PT; R; K2 = results/T-056/ket-qua-002.json; T (Hit@5 trần).
Power ≈ 0,19: docs/WHY.md:77 (WHY-06), chép nguyên văn số; không tính lại.
"""
import json
import sys

CAP = {"RE2-TT": ["M1-torai_B", "M1-simplerca", "M1-C-a0", "M1-C-a1", "M1-bo-E1", "M1-bo-E2", "M1-bo-E5", "M1-C-d1", "M1-C-d2", "M1-C-g", "M1-C-c"],
       "Nezha-OB": ["M1-simplerca", "M1-C-a0", "M1-C-a1", "M1-bo-E1", "M1-bo-E2", "M1-bo-E5", "M1-C-d1", "M1-C-d2", "M1-C-g", "M1-C-c"]}
CAP_R = ["M1-simplerca", "M1-torai_B", "M1-C-a0", "M1-C-a1", "M1-bo-E1", "M1-bo-E2", "M1-bo-E5", "M1-C-d1", "M1-C-d2", "M1-C-g", "M1-circa"]


def main(outp):
    a = json.load(open("results/T-054/reports/main-013-v2/a4.json", encoding="utf-8"))
    pt = json.load(open("results/T-054/reports/p7a-013-v2/phan-tich-nhom.json", encoding="utf-8"))
    r3 = json.load(open("results/T-055/reports/re3/phan-tich-re3.json", encoding="utf-8"))
    k2 = json.load(open("results/T-056/ket-qua-002.json", encoding="utf-8"))
    t = json.load(open("results/T-054/reports/main-013-v2/tables.json", encoding="utf-8"))
    g = json.load(open("results/T-054/reports/re3-ban-cuoi-001/re3-tables.json", encoding="utf-8"))
    out = {"lenh": "py -3 -B results/T-057/scripts/h5_h7_phan_xu.py " + outp, "A4": {}, "cap_MRR": {}, "tran": {}, "R1": {}}
    out["A4"]["TT"] = {"o_tong": a["TT"]["P"]["counts"]["n_cells"], "o_khac_0": a["TT"]["P"]["counts"]["cells_total_nonzero"],
                       "TWL": [a["TT"]["P"]["counts"][k] for k in ("win", "tie", "loss")],
                       "CI_12": [a["TT"]["P"]["E04"]["lo_12"], a["TT"]["P"]["E04"]["hi_12"]],
                       "p_dao_dau_o": a["TT"]["P"]["cell_sign_at_zero"], "power_WHY06": "≈0,19 (docs/WHY.md:77)",
                       "nguon": "a4.json#/TT/P/counts, /E04, /cell_sign_at_zero"}
    out["A4"]["OB"] = {"o_tong": a["OB"]["P"]["counts"]["n_cells"], "o_khac_0": a["OB"]["P"]["counts"]["cells_total_nonzero"],
                       "TWL": [a["OB"]["P"]["counts"][k] for k in ("win", "tie", "loss")],
                       "p_dao_dau_o": a["OB"]["P"].get("cell_sign_at_zero"), "pass": a["OB"]["P"].get("pass_formula"),
                       "p_nho_nhat_co_the": "2^-3 = 1/8 với 3 ô hữu hiệu", "nguon": "a4.json#/OB/P/counts, /cell_sign_at_zero"}
    for ds, caps in CAP.items():
        out["cap_MRR"][ds] = {}
        for c in caps:
            x = pt["so_cap"].get(f"{ds}|{c}|RR")
            if x:
                out["cap_MRR"][ds][c] = {"delta": x["delta_mean"]["xap_xi"], "TWL": [x["win"], x["tie"], x["loss"]],
                                         "o_khac_0": x["cells_nonzero"], "o_am": x["cells_negative"],
                                         "khoa": f"PT#/so_cap/{ds}|{c}|RR"}
    out["cap_MRR"]["RE3-OB"] = {}
    for c in CAP_R:
        x = r3["so_cap"].get(f"{c}|rr")
        if x:
            out["cap_MRR"]["RE3-OB"][c] = {"delta": float(x["delta"]), "TWL": [int(x["win"]), int(x["tie"]), int(x["loss"])],
                                           "o_khac_0": int(x["cells_nonzero"]), "o_am": int(x["cells_negative"]),
                                           "CI_o": x.get("CI_o"), "khoa": f"R#/so_cap/{c}|rr"}
    for ds in ("RE2-TT", "Nezha-OB"):
        m = [r["metrics"]["hit@5"] for r in t["rows"] if r["dataset"] == ds and r["world"] == "P" and r["arm"] == "M1"]
        out["tran"][ds] = {"M1_hit5_bang_1": sum(1 for x in m if x == 1.0), "n": len(m)}
    m = [r["metrics"]["hit@5"] for r in g["per_case"] if r["world"] == "P" and r["arm"] == "M1"]
    out["tran"]["RE3-OB"] = {"M1_hit5_bang_1": sum(1 for x in m if x == 1.0), "n": len(m)}
    for b in ("RE2-TT", "RE3-OB"):
        tt = k2["tom_tat"][b]
        out["R1"][b] = {"root_events_hon_moi_service_khac": tt.get("root_events_hon_moi_service_khac"),
                        "MRR": tt.get("MRR"), "khoa": f"K2#/tom_tat/{b}"}
    out["R1"]["Nezha-OB"] = "Chưa tính: dữ liệu metric thô OB test không có trên EC2; đọc lại trên laptop cần quyền H11."
    ce = pt["ce_tom_tat"]
    out["H7"] = {
        "RQ3a": "Không có P/R/F1 phát hiện của M1 trong đợt P7 (Q-245, docs/DECISIONS.md: hoãn chế độ (b)).",
        "C_e_TT": {"n_OK": ce["n_OK"], "V0": ce["V0"], "N1_mean": ce["N1_mean"]["xap_xi"],
                   "future_root_MRR": ce["future_root_MRR"]["xap_xi"], "chance_returned_MRR": ce["chance_returned_MRR"]["xap_xi"],
                   "future_root_hit1_count": ce["future_root_hit1_count"], "khoa": "PT#/ce_tom_tat"},
        "doc": "Ở cửa sổ t−300 (trước tiêm, nền lành chưa xác nhận), M1 trả CAUSE_FOUND ở mọi ca OK; M1 không có ngưỡng phát hiện mức hệ thống đã hiệu chuẩn.",
        "P3_baseline_phat_hien": "results/T-034/goi-g2.md §2.5–2.6 (BOCPD, N-Sigma, chế độ (b), dev)."}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("A4", "tran", "R1")}, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main(sys.argv[1])
