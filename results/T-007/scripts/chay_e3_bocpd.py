"""T-007 E3: tái lập BOCPD của BARO trên fse-ob qua script bọc mỏng (Minh duyệt 03/10/2026).

Gọi đúng baro.reproducibility.reproduce_bocpd(dataset="fse-ob", saved=False), tức điều
`python main.py --dataset OnlineBoutique --anomaly-detection` làm. Không sửa code BARO.
Chỉ thay hai tên trong module baro.reproducibility để ghi thêm, không đổi phép tính:
- tqdm: bọc vòng lặp các ca, biết ca đang chạy, ghi thời điểm bắt đầu và kết thúc từng ca;
- find_cps: gọi hàm gốc, giữ kết quả (danh sách điểm đổi) của ca đang chạy, trả nguyên kết quả.
Mỗi ca một dòng jsonl: đường dẫn ca, thời gian, điểm đổi tính được, điểm đổi tác giả lưu (naive_bocpd.json),
hai bên giống nhau không, và đóng góp vào TP/FP như reproduce_bocpd tính.
P/R/F1 do reproduce_bocpd in ra, giữ nguyên.

Giới hạn khối 3 giờ (Q-40): quá thì dừng trước ca kế tiếp, ghi VUOT_NGAN_SACH; P/R/F1 khi đó tính lại từ jsonl.
Chạy với thư mục làm việc chứa data/fse-ob:
  cd <thư mục làm việc> && <env>/bin/python chay_e3_bocpd.py --log tien-do.jsonl
"""
import argparse
import json
import os
import sys
import time

BARO = os.path.expanduser("~/rca/src/baro")
NGAN_SACH_S = 3 * 3600


class VuotNganSach(Exception):
    pass


def ts():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def chuan(cps):
    """Đưa danh sách điểm đổi về list[[int, float]] để so và ghi JSON."""
    return [[int(a), float(b)] for a, b in cps]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    a = ap.parse_args()

    sys.path.insert(0, BARO)  # như main.py của BARO chạy từ thư mục repo
    import numpy as np
    import pandas as pd
    import scipy
    import baro.reproducibility as R
    print(ts(), "BAT_DAU E3 | python", sys.version.split()[0], "| numpy", np.__version__, "| pandas", pd.__version__,
          "| scipy", scipy.__version__, "| baro tu", R.__file__, "| cwd", os.getcwd(), flush=True)

    f_log = open(a.log, "a")
    st = {"t_khoi": time.time()}
    tqdm_goc, find_cps_goc = R.tqdm, R.find_cps

    def ghi_ca():
        p = st["case"]
        d = os.path.dirname(p)
        luu = chuan(R.load_json(os.path.join(d, "naive_bocpd.json")))
        tinh = chuan(st["cps"]) if st.get("cps") is not None else None
        rec = {"i": st["i"], "case": os.path.relpath(d, "data"), "bat_dau": st["bat_dau"], "ket_thuc": ts(),
               "giay": round(time.time() - st["t0"], 2), "so_diem_doi": None if tinh is None else len(tinh),
               "cps": tinh, "cps_tac_gia": luu, "giong_tac_gia": tinh == luu,
               "tp": None if tinh is None else int(len(tinh) > 0),
               "fp": None if not tinh else int(tinh[0][0] < 300)}
        f_log.write(json.dumps(rec) + "\n")
        f_log.flush()
        print(ts(), "%3d %-35s %7.1f s cps=%s giong_tac_gia=%s" % (rec["i"], rec["case"], rec["giay"],
              rec["so_diem_doi"], rec["giong_tac_gia"]), flush=True)

    def tqdm_ghi(iterable, **kw):
        for i, x in enumerate(tqdm_goc(iterable, **kw), 1):
            if time.time() - st["t_khoi"] > NGAN_SACH_S:
                raise VuotNganSach("sau %d ca" % (i - 1))
            st.update({"i": i, "case": x, "cps": None, "t0": time.time(), "bat_dau": ts()})
            yield x
            ghi_ca()  # chạy khi vòng lặp xin ca kế tiếp, tức thân vòng của ca này đã xong

    def find_cps_ghi(maxes):
        cps = find_cps_goc(maxes)
        st["cps"] = cps
        return cps

    R.tqdm, R.find_cps = tqdm_ghi, find_cps_ghi
    try:
        R.reproduce_bocpd(dataset="fse-ob", saved=False)
    except VuotNganSach as e:
        print(ts(), "VUOT_NGAN_SACH", e, flush=True)
        f_log.write(json.dumps({"VUOT_NGAN_SACH": str(e)}) + "\n")
    except Exception as e:
        print(ts(), "LOI o ca", st.get("case"), type(e).__name__, e, flush=True)
        f_log.write(json.dumps({"LOI": "%s: %s" % (type(e).__name__, e), "case": st.get("case")}) + "\n")
        raise
    print(ts(), "XONG E3, %.0f s" % (time.time() - st["t_khoi"]), flush=True)


if __name__ == "__main__":
    main()
