"""T-007 E2: MicroRank, TraceRCA trên các ca RE2-OB, cửa sổ 300 s trước + 300 s sau mốc tiêm
(cấu hình `--length 10` như lệnh TORAI trong docs/TORAI.md).

RCAEval không có code đọc trace (main.py chỉ đọc data.csv / simple_metrics.csv). Bộ đọc trace và cách cắt
cửa sổ chép từ T-005 (results/T-005/scripts/chuan_bi_dau_vao.py, chay_mot_luot.py):
- đọc 8 cột traceID, spanID, parentSpanID, serviceName, methodName, operationName, startTime, duration;
- startTime, duration tính bằng micro giây; giữ span có startTime trong [mốc - 300 s, mốc + 300 s);
- gọi f(data, mốc_tiêm_micro_giây, dataset="re2-ob"), như T-005.
Không sửa code phương pháp.

Đầu ra như main.py RCAEval: <out>/<service>_<fault>_<n>.json chứa {"0": ranks}.
Tên ca (nhãn) chỉ dùng đặt tên file đầu ra để chấm sau, không đưa vào phương pháp.
Ca lỗi: ghi <service>_<fault>_<n>_failed.json (kiểu lỗi, thông báo, traceback) rồi chạy tiếp.
Nhật ký tiến độ (jsonl), mỗi ca một dòng: thời điểm bắt đầu, kết thúc, số span, giá trị trung gian, RSS đỉnh.
Giới hạn khối 3 giờ (Q-40): quá thì dừng trước ca kế tiếp, ghi VUOT_NGAN_SACH.
Tùy chọn --tron <seed>: phép kiểm độ nhạy theo thứ tự span (cùng tập span, xáo thứ tự dòng). Mặc định không xáo.
Tùy chọn --length <phút> (phiên 2): cửa sổ length*60//2 s mỗi phía; mặc định 10 (SPEC), 20 là biến thể chẩn đoán.

Chạy: <env>/bin/python chay_e2.py --method microrank --out <thư mục> [--cases ca1,ca2]
"""
import argparse
import glob
import json
import os
import resource
import sys
import time
import traceback

R = os.path.expanduser("~/rca")
RCAEVAL = os.path.join(R, "src", "RCAEval")
DATA = os.path.join(R, "data", "re2ob")
LENGTH = 10                     # phút, như docs/TORAI.md
HALF_US = LENGTH * 60 // 2 * 1_000_000   # 300 s, tính bằng micro giây
NGAN_SACH_S = 3 * 3600          # Q-40
COLS = ["traceID", "spanID", "parentSpanID", "serviceName", "methodName",
        "operationName", "startTime", "duration"]


def ts():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def rss_mb():
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, 1)  # Linux: KB


def ten_ket_qua(case):
    """re2ob_<service>_<fault>_<n> -> <service>_<fault>_<n> (cách đặt tên của main.py)."""
    p = case.split("_")
    return "%s_%s_%s" % ("_".join(p[1:-2]), p[-2], p[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True, choices=["microrank", "tracerca"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--cases", default="", help="danh sách ca, cách nhau dấu phẩy; trống = mọi ca")
    ap.add_argument("--length", type=int, default=LENGTH,
                    help="phút, như --length của main.py RCAEval: cửa sổ length*60//2 s mỗi phía mốc (mặc định 10 = SPEC; "
                         "20 = biến thể chẩn đoán, Minh duyệt phiên 2)")
    ap.add_argument("--tron", type=int, default=None,
                    help="phép kiểm độ nhạy: xáo thứ tự span trong cửa sổ bằng seed này (mặc định không xáo)")
    a = ap.parse_args()

    sys.path.insert(0, RCAEVAL)
    import numpy as np
    import pandas as pd
    if a.method == "microrank":
        from RCAEval.e2e.microrank import microrank as f
    else:
        from RCAEval.e2e.tracerca import tracerca as f

    res_dir = os.path.join(a.out, "results")
    os.makedirs(res_dir, exist_ok=True)
    tien_do = open(os.path.join(a.out, "tien-do.jsonl"), "a")

    cases = sorted(os.path.basename(d) for d in glob.glob(os.path.join(DATA, "re2ob_*")))
    if a.cases:
        chon = a.cases.split(",")
        cases = [c for c in cases if c in chon]
        assert len(cases) == len(chon), "có ca không tồn tại"
    print(ts(), "BAT_DAU", a.method, "| length", a.length, "| tron", a.tron, "| số ca", len(cases), "| python", sys.version.split()[0],
          "| pandas", pd.__version__, "| numpy", np.__version__, flush=True)

    t_khoi = time.time()
    for i, c in enumerate(cases, 1):
        if time.time() - t_khoi > NGAN_SACH_S:
            print(ts(), "VUOT_NGAN_SACH sau", i - 1, "ca", flush=True)
            tien_do.write(json.dumps({"VUOT_NGAN_SACH": True, "so_ca_xong": i - 1}) + "\n")
            break
        rec = {"i": i, "case": c, "bat_dau": ts()}
        t0 = time.time()
        try:
            with open(os.path.join(DATA, c, "inject_time.txt")) as fi:
                inj = int(fi.readlines()[0].strip())
            inj_us = inj * 1_000_000
            tr = pd.read_parquet(os.path.join(DATA, c, "traces.parquet"), columns=COLS)
            rec["span_ca"] = len(tr)
            half_us = a.length * 60 // 2 * 1_000_000   # = HALF_US khi --length 10
            rec["length"] = a.length
            data = tr[(tr["startTime"] >= inj_us - half_us) & (tr["startTime"] < inj_us + half_us)].reset_index(drop=True)
            if a.tron is not None:  # cùng tập span, chỉ khác thứ tự dòng
                data = data.sample(frac=1, random_state=a.tron).reset_index(drop=True)
                rec["tron_seed"] = a.tron
            end = data["startTime"] + data["duration"]
            # giá trị trung gian (QT5): cách hai hàm chia span trước/sau mốc
            rec.update({"span_cua_so": len(data), "span_truoc": int((end < inj_us).sum()),
                        "span_sau": int((end >= inj_us).sum()), "so_trace": int(data["traceID"].nunique()),
                        "so_service": int(data["serviceName"].nunique()),
                        "methodName_trong": int(data["methodName"].isna().sum()),
                        "doc_s": round(time.time() - t0, 2)})
            t1 = time.time()
            out = f(data, inj_us, dataset="re2-ob")
            rec["method_s"] = round(time.time() - t1, 2)
            ranks = list(out.get("ranks"))
            rec["so_hang"] = len(ranks)
            rec["top5"] = ranks[:5]
            with open(os.path.join(res_dir, ten_ket_qua(c) + ".json"), "w") as fo:
                json.dump({"0": ranks}, fo)
            rec["trang_thai"] = "ok" if ranks else "RONG"
        except Exception as e:
            rec["trang_thai"] = "LOI"
            rec["loi"] = "%s: %s" % (type(e).__name__, e)
            with open(os.path.join(res_dir, ten_ket_qua(c) + "_failed.json"), "w") as fo:
                json.dump({"error": rec["loi"], "traceback": traceback.format_exc()}, fo)
        rec.update({"ket_thuc": ts(), "giay": round(time.time() - t0, 2), "rss_dinh_mb": rss_mb()})
        tien_do.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        tien_do.flush()
        print(ts(), "%2d/%d %-45s %-4s %6.1f s hang=%s rss=%s" % (i, len(cases), c, rec["trang_thai"], rec["giay"],
              rec.get("so_hang"), rec["rss_dinh_mb"]), flush=True)
    print(ts(), "XONG %s, %.0f s" % (a.method, time.time() - t_khoi), flush=True)


if __name__ == "__main__":
    main()
