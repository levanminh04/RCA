"""T-018 B4/B7: học và chấm GDN bằng code chính thức (revision 9853899), không sửa file nào của GDN.

Chạy bằng D:/RCA-ext/envs/py38-gdn/Scripts/python.exe. Thư mục làm việc tự đổi về D:/RCA-ext/work/T-018/gdn
(GDN đọc ./data/<dataset>/{train,test,list}).

Giống T-005: dựng dữ liệu và mô hình bằng `Main.__init__`, rồi gọi thẳng `train()` và `test()` (tránh
`Main.get_save_path` đặt tên file có '|', ':' không hợp lệ trên Windows). Điểm bất thường tính bằng
`evaluate.get_full_err_scores` (như `Main.get_score`). Không gọi `get_score` vì cột `attack` toàn 0 (không phải nhãn).

Thêm so với T-005, không đổi hành vi:
- mỗi dòng stdout có giờ (SL25);
- bọc hàm `test` trong module `train` để ghi val loss từng epoch (hàm gốc vẫn được gọi y nguyên);
- tùy chọn --test-none: truyền test_dataloader=None vào train() (train() không dùng tham số này; SPEC B4);
- chấm thêm các đoạn bình thường giữ ngoài ở ./data/<dataset>/ho/*.csv bằng cùng mô hình, cùng tập kiểm định.

Đầu ra: D:/RCA-ext/work/T-018/gdn/runs/<nhan>/ (mô hình, mảng .npy) và tom-tat.json.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import random
import sys
import time

GDN = r"D:\RCA-ext\src\GDN"
WORK = r"D:\RCA-ext\work\T-018\gdn"


class GioStdout:
    def __init__(self, s):
        self.s, self.dau = s, True

    def write(self, x):
        for part in x.splitlines(True):
            if self.dau:
                self.s.write(datetime.datetime.now().strftime("[%H:%M:%S] "))
            self.s.write(part)
            self.dau = part.endswith("\n")
        self.s.flush()

    def flush(self):
        self.s.flush()


def sha_trong_so(sd):
    h = hashlib.sha256()
    for k in sorted(sd):
        h.update(k.encode())
        h.update(sd[k].cpu().numpy().tobytes())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--nhan", required=True)
    ap.add_argument("--seed", type=int, default=5)
    ap.add_argument("--threads", type=int, default=0, help="0 = mặc định của torch")
    ap.add_argument("--epoch", type=int, default=30)
    ap.add_argument("--test-none", action="store_true")
    ap.add_argument("--chi-cham", default="", help="đường dẫn mô hình có sẵn: bỏ qua học, chỉ chấm")
    a = ap.parse_args()

    sys.stdout = GioStdout(sys.stdout)
    out = os.path.join(WORK, "runs", a.nhan)
    os.makedirs(out, exist_ok=True)
    sys.path.insert(0, GDN)
    os.chdir(WORK)

    import numpy as np
    import torch
    from torch.utils.data import DataLoader
    import train as train_mod
    from main import Main
    from evaluate import get_full_err_scores
    from util.preprocess import construct_data
    from datasets.TimeDataset import TimeDataset
    import pandas as pd

    if a.threads > 0:
        torch.set_num_threads(a.threads)
    random.seed(a.seed)
    np.random.seed(a.seed)
    torch.manual_seed(a.seed)
    os.environ["PYTHONHASHSEED"] = str(a.seed)

    # cấu hình nhánh cpu của run.sh (batch 32, win 5, stride 1, dim 64, topk 5, out_layer_num 1, inter 128, val 0.2)
    cfg = {"batch": 32, "epoch": a.epoch, "slide_win": 5, "dim": 64, "slide_stride": 1, "comment": a.data,
           "seed": a.seed, "out_layer_num": 1, "out_layer_inter_dim": 128, "decay": 0, "val_ratio": 0.2, "topk": 5}
    env = {"save_path": a.data, "dataset": a.data, "report": "val", "device": "cpu", "load_model_path": ""}
    t0 = time.perf_counter()
    m = Main(cfg, env, debug=False)
    print("windows: train", len(m.train_dataloader.dataset), "val", len(m.val_dataloader.dataset),
          "test", len(m.test_dataset), "| nodes", len(m.feature_map), "| threads", torch.get_num_threads(), flush=True)
    model_path = os.path.join(out, "model.pt")

    val_loss = []
    goc = train_mod.test

    def test_ghi(model, loader):
        r = goc(model, loader)
        if loader is m.val_dataloader:
            val_loss.append(r[0])
        return r

    so_epoch = None
    t1 = time.perf_counter()
    if a.chi_cham:
        model_path = a.chi_cham
    else:
        train_mod.test = test_ghi
        loss = train_mod.train(m.model, model_path, config=cfg, train_dataloader=m.train_dataloader,
                               val_dataloader=m.val_dataloader, feature_map=m.feature_map,
                               test_dataloader=None if a.test_none else m.test_dataloader,
                               test_dataset=m.test_dataset, train_dataset=m.train_dataset, dataset_name=a.data)
        train_mod.test = goc
        so_epoch = len(val_loss)
    t2 = time.perf_counter()

    sd = torch.load(model_path)
    m.model.load_state_dict(sd)
    _, test_res = goc(m.model, m.test_dataloader)
    _, val_res = goc(m.model, m.val_dataloader)
    scores, normal = get_full_err_scores(test_res, val_res)
    scores, normal = np.asarray(scores, float), np.asarray(normal, float)
    tau = float(np.max(normal))
    A = scores.max(axis=0)
    np.save(os.path.join(out, "test_pred.npy"), np.asarray(test_res[0], float))
    np.save(os.path.join(out, "test_gt.npy"), np.asarray(test_res[1], float))
    np.save(os.path.join(out, "val_pred.npy"), np.asarray(val_res[0], float))
    np.save(os.path.join(out, "val_gt.npy"), np.asarray(val_res[1], float))
    np.save(os.path.join(out, "test_scores.npy"), scores)
    np.save(os.path.join(out, "normal_scores.npy"), normal)
    val_idx = m.val_dataloader.dataset.indices.numpy()
    np.save(os.path.join(out, "val_indices.npy"), val_idx)

    # đoạn bình thường giữ ngoài
    ho_kq = {}
    edge = m.test_dataset.edge_index
    win = {"slide_win": cfg["slide_win"], "slide_stride": cfg["slide_stride"]}
    for f in sorted(glob.glob(os.path.join(WORK, "data", a.data, "ho", "*.csv"))):
        ca = os.path.basename(f)[:-4]
        df = pd.read_csv(f, sep=",", index_col=0)
        ds = TimeDataset(construct_data(df, m.feature_map, labels=df.attack.tolist()), edge, mode="test", config=win)
        _, r = goc(m.model, DataLoader(ds, batch_size=cfg["batch"], shuffle=False, num_workers=0))
        s, _ = get_full_err_scores(r, val_res)
        s = np.asarray(s, float)
        np.save(os.path.join(out, "ho_scores_%s.npy" % ca), s)
        np.save(os.path.join(out, "ho_pred_%s.npy" % ca), np.asarray(r[0], float))
        np.save(os.path.join(out, "ho_gt_%s.npy" % ca), np.asarray(r[1], float))
        Ah = s.max(axis=0)
        ho_kq[ca] = {"n_tick": int(Ah.size), "n_bao_dong": int((Ah > tau).sum()), "A_max": float(Ah.max())}
    t3 = time.perf_counter()

    kq = {"nhan": a.nhan, "data": a.data, "seed": a.seed, "threads": torch.get_num_threads(), "test_none": a.test_none,
          "chi_cham": a.chi_cham, "so_epoch_chay": so_epoch, "val_loss": val_loss,
          "epoch_tot_nhat": (int(np.argmin(val_loss)) if val_loss else None),
          "sha256_trong_so": sha_trong_so(sd),
          "test_scores_shape": list(scores.shape), "huu_han": bool(np.isfinite(scores).all() and np.isfinite(normal).all()),
          "tau": tau, "A_test_max": float(A.max()), "tick_A_max": int(A.argmax()), "n_bao_dong_test": int((A > tau).sum()),
          "giu_ngoai": ho_kq, "s_dung_mo_hinh": round(t1 - t0, 2), "s_hoc": round(t2 - t1, 2), "s_cham": round(t3 - t2, 2)}
    with open(os.path.join(out, "tom-tat.json"), "w", encoding="utf-8") as fh:
        json.dump(kq, fh, ensure_ascii=False, indent=1)
    print("KET_QUA", json.dumps({k: v for k, v in kq.items() if k not in ("giu_ngoai", "val_loss")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
