"""T-007: soi giá trị trung gian của MicroRank (QT5) trên vài ca RE2-OB. Không đổi phép tính.

Vì sao: ở lượt chính, 87/90 ca có cùng 4 service đầu bất kể lỗi. Script này ghi lại các đại lượng bên trong
để biết vì sao, bằng cách bọc (không sửa) hai hàm trong module RCAEval.e2e.microrank:
- trace_pagerank: số thao tác, số trace của đồ thị "bình thường" và "bất thường", trọng số PageRank từng thao tác;
- calculate_spectrum_without_delay_list: số trace bất thường / bình thường (anomaly_list_len, normal_list_len),
  ef, ep, nf của từng thao tác, điểm Dstar2 (tính lại đúng công thức trong hàm), 11 thao tác trả về và điểm.
Đầu vào và cách gọi giống chay_e2.py (cửa sổ 300 s + 300 s, mốc tiêm micro giây). Thứ hạng trả về được so với
file kết quả của lượt chính để chắc việc bọc không đổi kết quả.

Chạy: <env>/bin/python trung_gian_microrank.py --cases ca1,ca2 --ket-qua-chinh <thư mục results> --out <file jsonl>
"""
import argparse
import json
import os
import sys

R = os.path.expanduser("~/rca")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "src", "RCAEval"))
from chay_e2 import COLS, DATA, HALF_US, ten_ket_qua  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--ket-qua-chinh", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    import importlib
    import pandas as pd
    # Không dùng "import RCAEval.e2e.microrank as M": RCAEval/e2e/__init__.py gán tên microrank của gói thành hàm,
    # nên cách đó trả về hàm. import_module trả đúng module trong sys.modules (lượt hỏng 10:41 UTC vì lỗi này).
    M = importlib.import_module("RCAEval.e2e.microrank")

    bat = {}
    pr_goc, sp_goc = M.trace_pagerank, M.calculate_spectrum_without_delay_list

    def pr_boc(operation_operation, operation_trace, trace_operation, pr_trace, anomaly):
        kq, num = pr_goc(operation_operation, operation_trace, trace_operation, pr_trace, anomaly)
        bat["bat_thuong" if anomaly else "binh_thuong"] = {
            "so_thao_tac": len(operation_operation), "so_trace": len(operation_trace),
            "trong_so": {k: float(v) for k, v in kq.items()}, "so_trace_qua": {k: int(v) for k, v in num.items()}}
        return kq, num

    def sp_boc(anomaly_result, normal_result, anomaly_list_len, normal_list_len, top_max, normal_num_list,
               anomaly_num_list, spectrum_method):
        top, score = sp_goc(anomaly_result=anomaly_result, normal_result=normal_result,
                            anomaly_list_len=anomaly_list_len, normal_list_len=normal_list_len, top_max=top_max,
                            normal_num_list=normal_num_list, anomaly_num_list=anomaly_num_list,
                            spectrum_method=spectrum_method)
        # ef, ep, nf như trong hàm gốc (nhánh dstar2), chép nguyên công thức, chỉ để ghi lại
        pho = {}
        for node in anomaly_result:
            ef = anomaly_result[node] * anomaly_num_list[node]
            nf = anomaly_result[node] * (anomaly_list_len - anomaly_num_list[node])
            if node in normal_result:
                ep = normal_result[node] * normal_num_list[node]
            else:
                ep = 0.0000001
            pho[node] = {"ef": float(ef), "ep": float(ep), "nf": float(nf), "dstar2": float(ef * ef / (ep + nf)),
                         "so_trace_qua_sau": int(anomaly_num_list[node]),
                         "so_trace_qua_truoc": int(normal_num_list.get(node, 0))}
        bat["pho"] = {"anomaly_list_len": int(anomaly_list_len), "normal_list_len": int(normal_list_len),
                      "top_max": top_max, "phuong_phap": spectrum_method,
                      "top": list(top), "diem": [float(s) for s in score], "tung_thao_tac": pho,
                      "so_nf_am": sum(1 for v in pho.values() if v["nf"] < 0)}
        return top, score

    M.trace_pagerank, M.calculate_spectrum_without_delay_list = pr_boc, sp_boc
    with open(a.out, "w") as fo:
        for c in a.cases.split(","):
            bat.clear()
            with open(os.path.join(DATA, c, "inject_time.txt")) as fi:
                inj_us = int(fi.readlines()[0].strip()) * 1_000_000
            tr = pd.read_parquet(os.path.join(DATA, c, "traces.parquet"), columns=COLS)
            data = tr[(tr["startTime"] >= inj_us - HALF_US) & (tr["startTime"] < inj_us + HALF_US)].reset_index(drop=True)
            out = M.microrank(data, inj_us, dataset="re2-ob")
            sau = data[data["startTime"] + data["duration"] >= inj_us]
            with open(os.path.join(a.ket_qua_chinh, ten_ket_qua(c) + ".json")) as f:
                chinh = json.load(f)["0"]
            rec = {"case": c, "so_trace_sau_moc": int(sau["traceID"].nunique()),
                   "giong_luot_chinh": list(out["ranks"]) == chinh}
            rec.update(bat)
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            p = bat["pho"]
            print(c, "| trace sau mốc:", rec["so_trace_sau_moc"], "| bất thường:", p["anomaly_list_len"],
                  "| bình thường:", p["normal_list_len"], "| thao tác có nf<0:", p["so_nf_am"], "/", len(p["tung_thao_tac"]),
                  "| giống lượt chính:", rec["giong_luot_chinh"], flush=True)


if __name__ == "__main__":
    main()
