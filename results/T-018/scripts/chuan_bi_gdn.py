"""T-018 B3: dựng dữ liệu cho GDN, độc lập với script T-005 (không import, viết lại theo mô tả trong SPEC).

Chạy bằng D:/RCA-ext/envs/py312 (cùng môi trường T-005 dùng để dựng dữ liệu, để so được từng byte).

Đầu ra ở D:/RCA-ext/work/T-018/gdn/data/<tên>/:
  re2tt5/        lặp đúng T-005: học trên 720 dòng trước mốc của 5 ca, test là toàn ca R-ca, 333 cột = giao 5 ca học và ca test.
  re2tt5/ho/     19 đoạn bình thường giữ ngoài (720 dòng trước mốc), cùng bộ cột và bộ chuẩn hóa của re2tt5;
                 cột thiếu điền trung vị tập học (thang thô) theo R-thiếu-cột.
  lstar_n1, lstar_n5, lstar_n10, lstar_n5_hoanvi/   bộ cột L* (giao 30 ca dev), học trên 1/5/10 ca;
                 mỗi thư mục có test.csv = toàn ca R-ca và ho/ = 19 đoạn giữ ngoài.
Tóm tắt (kích thước, cột hằng, cột điền, SHA-256) ghi ra results/T-018/runs/b3-chuan-bi.json.

Mốc tiêm chỉ dùng để: (1) lấy đoạn bình thường cho tập học, như T-005; (2) cắt đoạn bình thường giữ ngoài để chấm
phép kiểm "bình thường vs bình thường". Không đưa vào mô hình khi chấm ca test.
"""
import hashlib
import json
import os

import numpy as np
import pandas as pd

REPO = r"D:\RCA-flashticket"
DATA = os.path.join(REPO, "data", "rcaeval")
OUT = r"D:\RCA-ext\work\T-018\gdn\data"
SUMMARY = os.path.join(REPO, "results", "T-018", "runs", "b3-chuan-bi.json")

CA_RCA = "re2tt_ts-route-service_socket_1"            # R-ca
HOC_T005 = [                                          # danh sách học của T-005, giữ đúng thứ tự
    "re2tt_ts-order-service_loss_1",
    "re2tt_ts-travel-service_loss_2",
    "re2tt_ts-auth-service_cpu_1",
    "re2tt_ts-auth-service_delay_1",
    "re2tt_ts-order-service_disk_1",
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


MOC = r"D:\RCA-ext\work\T-018\nguon\rcaeval-inject"   # tải bằng tai_moc_tiem.py, đã kiểm git blob oid với HF


def moc_tiem(ca):
    with open(os.path.join(MOC, ca, "inject_time.txt")) as f:
        return int(f.readline().strip())


def doc_sach(ca):
    """Làm sạch như T-005/`main.py`: bỏ time.1, bỏ *_latency-50, inf->NaN, ffill, fillna(0), đổi *_latency-90 -> *_latency."""
    df = pd.read_parquet(os.path.join(DATA, ca, "metrics.parquet"))
    if "time.1" in df:
        df = df.drop(columns=["time.1"])
    df = df.loc[:, ~df.columns.str.endswith("_latency-50")]
    df = df.replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
    df = df.rename(columns={c: c.replace("_latency-90", "_latency") for c in df.columns if c.endswith("_latency-90")})
    return df


def truoc_moc(ca, df):
    return df[df["time"] < moc_tiem(ca)].reset_index(drop=True)


def ghi(thu_muc, train, test, feats, ho):
    """train/test: DataFrame đã chuẩn hóa, cột theo feats. ho: dict ca -> DataFrame đã chuẩn hóa."""
    os.makedirs(os.path.join(thu_muc, "ho"), exist_ok=True)
    train.to_csv(os.path.join(thu_muc, "train.csv"))
    t = test.copy()
    t["attack"] = 0  # code GDN bắt buộc có cột này; không phải nhãn
    t.to_csv(os.path.join(thu_muc, "test.csv"))
    with open(os.path.join(thu_muc, "list.txt"), "w") as f:
        f.write("\n".join(feats) + "\n")
    for ca, d in ho.items():
        d = d.copy()
        d["attack"] = 0
        d.to_csv(os.path.join(thu_muc, "ho", ca + ".csv"))


def chuan_hoa(train_raw, feats):
    lo, hi = train_raw[feats].min(), train_raw[feats].max()
    rng = (hi - lo).replace(0, 1)          # như T-005 và sklearn MinMaxScaler: khoảng 0 thì chia cho 1
    return lo, rng


def ap(df_raw, feats, lo, rng, med):
    d = pd.DataFrame(index=range(len(df_raw)))
    thieu = []
    for c in feats:
        if c in df_raw.columns:
            d[c] = df_raw[c].values
        else:
            d[c] = med[c]                  # R-thiếu-cột
            thieu.append(c)
    return (d[feats] - lo) / rng, thieu


def main():
    tom = {}
    dev = sorted(c for c in os.listdir(DATA) if c.startswith("re2tt_"))
    assert len(dev) == 30, len(dev)
    sach = {c: doc_sach(c) for c in dev}

    # ---- R-giữ-ngoài ----
    con_lai = [c for c in dev if c not in HOC_T005 and c != CA_RCA]
    theo_sha = sorted(con_lai, key=lambda c: hashlib.sha256(c.encode()).hexdigest())
    hoc10 = HOC_T005 + theo_sha[:5]
    giu_ngoai = theo_sha[5:]
    assert len(giu_ngoai) == 19
    tom["hoc_1"] = HOC_T005[:1]
    tom["hoc_5"] = HOC_T005
    tom["hoc_10"] = hoc10
    tom["giu_ngoai"] = giu_ngoai

    # ---- re2tt5: lặp T-005 ----
    trains = [truoc_moc(c, sach[c]) for c in HOC_T005]
    test = sach[CA_RCA]
    feats = [c for c in test.columns if c != "time" and all(c in t.columns for t in trains)]
    train_raw = pd.concat([t[feats] for t in trains], ignore_index=True)
    lo, rng = chuan_hoa(train_raw, feats)
    med = train_raw[feats].median()
    train = (train_raw - lo) / rng
    test_x = (test[feats].reset_index(drop=True) - lo) / rng
    ho, thieu = {}, {}
    for c in giu_ngoai:
        ho[c], thieu[c] = ap(truoc_moc(c, sach[c]), feats, lo, rng, med)
    d = os.path.join(OUT, "re2tt5")
    ghi(d, train, test_x, feats, ho)
    tom["re2tt5"] = {
        "train_shape": list(train.shape), "test_shape": list(test_x.shape), "n_feats": len(feats),
        "rows_per_case": [len(t) for t in trains],
        "cot_hang_trong_tap_hoc": int(((train_raw.max() - train_raw.min()) == 0).sum()),
        "max_abs_test_sau_chuan_hoa": float(np.abs(test_x.values).max()),
        "cot_max_abs_test": str(np.abs(test_x).max().idxmax()),
        "so_cot_test_vuot_khoang_0_1": int(((test_x.min() < 0) | (test_x.max() > 1)).sum()),
        "cot_dien_moi_ca_giu_ngoai": {c: len(v) for c, v in thieu.items()},
        "sha256": {f: sha(os.path.join(d, f)) for f in ["train.csv", "test.csv", "list.txt"]},
    }

    # ---- L*: giao 30 ca dev, sắp theo tên ----
    lstar = sorted(set.intersection(*[set(sach[c].columns) - {"time"} for c in dev]))
    tom["lstar_n_cot"] = len(lstar)
    tom["hop_30_ca_n_cot"] = len(set.union(*[set(sach[c].columns) - {"time"} for c in dev]))
    hoan_vi = list(np.array(lstar)[np.random.RandomState(0).permutation(len(lstar))])
    for ten, hoc, thu_tu in [("lstar_n1", HOC_T005[:1], lstar), ("lstar_n5", HOC_T005, lstar),
                             ("lstar_n10", hoc10, lstar), ("lstar_n5_hoanvi", HOC_T005, hoan_vi)]:
        tr_raw = pd.concat([truoc_moc(c, sach[c])[thu_tu] for c in hoc], ignore_index=True)
        lo, rng = chuan_hoa(tr_raw, thu_tu)
        tr = (tr_raw - lo) / rng
        te = (sach[CA_RCA][thu_tu].reset_index(drop=True) - lo) / rng
        ho = {c: (truoc_moc(c, sach[c])[thu_tu] - lo) / rng for c in giu_ngoai}
        d = os.path.join(OUT, ten)
        ghi(d, tr, te, list(thu_tu), ho)
        tom[ten] = {
            "train_shape": list(tr.shape), "test_shape": list(te.shape),
            "cot_hang_trong_tap_hoc": int(((tr_raw.max() - tr_raw.min()) == 0).sum()),
            "max_abs_test_sau_chuan_hoa": float(np.abs(te.values).max()),
            "max_abs_giu_ngoai_sau_chuan_hoa": float(max(np.abs(v.values).max() for v in ho.values())),
            "so_cua_so_cat_ngang_ranh_gioi": (len(hoc) - 1) * 5,
        }
    os.makedirs(os.path.dirname(SUMMARY), exist_ok=True)
    with open(SUMMARY, "w", encoding="utf-8") as f:
        json.dump(tom, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in tom.items() if k.startswith(("re2tt5", "lstar"))}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
