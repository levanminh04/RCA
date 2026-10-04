"""T-005: chạy MỘT mục đo trong tiến trình riêng. Do `do.py` gọi; chạy được trên Python 3.8 và 3.12.

In ra một dòng `KET_QUA {json}` gồm:
- import_s: thời gian import code phương pháp;
- load_s: thời gian đọc đầu vào;
- method_s: thời gian gọi hàm phương pháp (time.perf_counter), phần chính cần đo;
- peak_ws_mb: working set đỉnh của tiến trình (RAM vật lý đỉnh, theo Windows);
- peak_private_mb: bộ nhớ riêng (commit) đỉnh. Khi máy thiếu RAM, Windows cắt bớt working set,
  nên số này phản ánh nhu cầu bộ nhớ tốt hơn;
- ws_before_method_mb: working set ngay trước khi gọi hàm.

Thứ hạng trả ra được ghi vào D:/RCA-ext/work/T-005/out/ và KHÔNG in ra, không đọc (SPEC T-005).
"""
import argparse
import ctypes
import json
import os
import sys
import time
from ctypes import wintypes

WORK = r"D:\RCA-ext\work\T-005"
INP = os.path.join(WORK, "inputs")
OUT = os.path.join(WORK, "out")
INJ_FILE = r"D:\RCA-ext\dl\rcaeval-inject\re2tt_ts-route-service_socket_1\inject_time.txt"
RCAEVAL = r"D:\RCA-ext\src\RCAEval"
BARO = r"D:\RCA-ext\src\baro"
GDN = r"D:\RCA-ext\src\GDN"


class _PMC(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]


def mem():
    k32 = ctypes.WinDLL("kernel32")
    psapi = ctypes.WinDLL("psapi")
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PMC), wintypes.DWORD]
    c = _PMC()
    c.cb = ctypes.sizeof(_PMC)
    psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    mb = 1024.0 * 1024.0
    return {"peak_ws_mb": round(c.PeakWorkingSetSize / mb, 1), "ws_mb": round(c.WorkingSetSize / mb, 1),
            "peak_private_mb": round(c.PeakPagefileUsage / mb, 1)}


def inject_time():
    with open(INJ_FILE) as f:
        return int(f.readlines()[0].strip())


def run(muc, bien_the):
    """Trả về (import_s, load_s, method_s, ws_before, output, ghi_chu)."""
    t0 = time.perf_counter()
    note = ""

    if muc in ("baro", "nsigma", "circa", "rcd"):
        sys.path.insert(0, RCAEVAL)
        import pandas as pd
        if muc == "baro":
            from RCAEval.e2e.baro import baro as f
        elif muc == "nsigma":
            from RCAEval.e2e import nsigma as f
        elif muc == "circa":
            from RCAEval.e2e.circa import circa as f
        else:
            from RCAEval.e2e.rcd import rcd as f
        t1 = time.perf_counter()
        data = pd.read_csv(os.path.join(INP, "metrics_%s.csv" % bien_the))
        inj = inject_time()
        t2 = time.perf_counter()
        ws = mem()["ws_mb"]
        out = f(data, inj, dataset="re2-tt", anomalies=None, dk_select_useful=False, sli=None, verbose=False)
        t3 = time.perf_counter()
        if muc == "circa" and isinstance(out.get("adj"), list) and len(out["adj"]) == 0:
            note = "CIRCA_THAT_BAI: wrapper @rca bắt lỗi và trả thứ tự cột (xem stderr)"

    elif muc in ("microrank", "tracerca"):
        sys.path.insert(0, RCAEVAL)
        import pandas as pd
        if muc == "microrank":
            from RCAEval.e2e.microrank import microrank as f
        else:
            from RCAEval.e2e.tracerca import tracerca as f
        t1 = time.perf_counter()
        data = pd.read_parquet(os.path.join(INP, "traces_%s.parquet" % bien_the))
        inj = inject_time() * 1000000  # startTime, duration tính bằng micro giây
        t2 = time.perf_counter()
        ws = mem()["ws_mb"]
        out = f(data, inj, dataset="re2-tt")
        t3 = time.perf_counter()

    elif muc == "torai":
        sys.path.insert(0, RCAEVAL)
        import pandas as pd
        from RCAEval.e2e.torai import torai as f
        t1 = time.perf_counter()
        data = {
            "metric": pd.read_csv(os.path.join(INP, "torai_metric_%s.csv" % bien_the)),
            "logts": pd.read_csv(os.path.join(INP, "torai_logts_%s.csv" % bien_the)),
            "tracets_err": pd.read_csv(os.path.join(INP, "torai_tracets_err_%s.csv" % bien_the)),
            "tracets_lat": pd.read_csv(os.path.join(INP, "torai_tracets_lat_%s.csv" % bien_the)),
        }
        inj = inject_time()
        t2 = time.perf_counter()
        ws = mem()["ws_mb"]
        out = f(data, inj, dataset="torai-tt", anomalies=None, dk_select_useful=False, sli=None, verbose=False)
        t3 = time.perf_counter()

    elif muc in ("bocpd", "nsigma_phat_hien"):
        sys.path.insert(0, BARO)
        import pandas as pd
        from baro.anomaly_detection import bocpd, nsigma
        t1 = time.perf_counter()
        data = pd.read_csv(os.path.join(INP, "metrics_raw_full.csv"))
        if bien_the == "win":
            # Cắt như BARO reproducibility.reproduce_bocpd: 300 điểm trước + 300 điểm sau mốc (Minh duyệt 03/10).
            inj = inject_time()
            data = pd.concat([data[data["time"] < inj].tail(300), data[data["time"] >= inj].head(300)],
                             ignore_index=True)
        t2 = time.perf_counter()
        ws = mem()["ws_mb"]
        if muc == "bocpd":
            out = {"anomalies": bocpd(data)}
        else:
            out = {"anomalies": nsigma(data, k=3, startsfrom=100)}
        t3 = time.perf_counter()

    elif muc in ("gdn_hoc", "gdn_suy_luan"):
        # Cấu hình theo GDN/run.sh; report='val' (T-001 mục 8.1). Dựng dữ liệu, mô hình như Main.__init__,
        # rồi gọi train()/test() trực tiếp để đo riêng hai pha và tránh tên file có '|', ':' của Main.get_save_path.
        sys.path.insert(0, GDN)
        os.chdir(os.path.join(WORK, "gdn"))  # GDN đọc ./data/<dataset>/
        import random
        import numpy as np
        import torch
        from main import Main
        from train import train
        from test import test
        from evaluate import get_full_err_scores
        t1 = time.perf_counter()
        seed = 5
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        os.environ["PYTHONHASHSEED"] = str(seed)
        train_config = {"batch": 32, "epoch": 30, "slide_win": 5, "dim": 64, "slide_stride": 1,
                        "comment": "re2tt5", "seed": seed, "out_layer_num": 1, "out_layer_inter_dim": 128,
                        "decay": 0, "val_ratio": 0.2, "topk": 5}
        env_config = {"save_path": "re2tt5", "dataset": "re2tt5", "report": "val", "device": "cpu",
                      "load_model_path": ""}
        m = Main(train_config, env_config, debug=False)
        model_path = os.path.join(WORK, "gdn", "model_re2tt5.pt")
        t2 = time.perf_counter()
        ws = mem()["ws_mb"]
        if muc == "gdn_hoc":
            loss = train(m.model, model_path, config=train_config, train_dataloader=m.train_dataloader,
                         val_dataloader=m.val_dataloader, feature_map=m.feature_map,
                         test_dataloader=m.test_dataloader, test_dataset=m.test_dataset,
                         train_dataset=m.train_dataset, dataset_name="re2tt5")
            out = {"so_buoc": len(loss), "so_epoch_toi_da": 30}
            note = "train windows=%d, val windows=%d" % (len(m.train_dataloader.dataset), len(m.val_dataloader.dataset))
        else:
            m.model.load_state_dict(torch.load(model_path))
            _, test_result = test(m.model, m.test_dataloader)
            _, val_result = test(m.model, m.val_dataloader)
            scores, normal_scores = get_full_err_scores(test_result, val_result)
            out = {"scores_shape": list(np.array(scores).shape)}
            note = "test windows=%d" % len(m.test_dataloader.dataset)
        t3 = time.perf_counter()
    else:
        raise ValueError(muc)

    return t1 - t0, t2 - t1, t3 - t2, ws, out, note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--muc", required=True)
    ap.add_argument("--bien_the", default="full")
    ap.add_argument("--nhan", required=True, help="tên lượt, dùng đặt tên file đầu ra")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    print("python", sys.version.split()[0], "| muc", a.muc, "| bien_the", a.bien_the, flush=True)
    imp, load, meth, ws, out, note = run(a.muc, a.bien_the)
    with open(os.path.join(OUT, a.nhan + ".json"), "w") as f:
        json.dump(out, f, default=str)
    r = {"import_s": round(imp, 3), "load_s": round(load, 3), "method_s": round(meth, 3),
         "ws_before_method_mb": ws, "ghi_chu": note}
    r.update(mem())
    print("KET_QUA " + json.dumps(r, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
