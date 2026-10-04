r"""T-016 S12: ví dụ tính tay TORAI và lõi RCD trên một ca, bằng script ĐỘC LẬP.

Không gọi hàm nào của TORAI, RCD, RCAEval hay causal-learn; không gọi KBinsDiscretizer, KMeans.
Chỉ dùng numpy, pandas, scipy.stats.chi2.sf (hàm phân phối) và sklearn.mixture.GaussianMixture (thư viện, với đúng
tham số của torai.py:244-261; BIC và log-likelihood được tính lại bằng tay từ tham số đã khớp).
Đầu vào dựng bằng dung_dau_vao() của harness T-016 (code của nhóm, chép đúng main.py), không phải code tác giả.

Cách dùng (python của py38-rcdlock, để cùng numpy/pandas/sklearn với lượt chính thức):
  python tinh_tay.py --ca D:/RCA-ext/data/torai-OB/checkoutservice_cpu/1 --dataset torai-ob --length 10 --seed 0
                     --bien-the goc|sua --meta <meta.jsonl của lượt chính thức có T016_GHI_DU_LIEU=1>
                     --ket-qua <file <ca>.json của lượt chính thức> --ra <file json>
"""
import argparse
import itertools
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.mixture import GaussianMixture

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chay_torai import dung_dau_vao  # noqa: E402  (code của nhóm, chép main.py)

F = "F-node"
GAMMA, BINS = 5, 5
ALPHA_PHA1, ALPHA_PHA2, BUOC, TRAN = 0.01, 0.001, 0.1, 1.0


# ============================================================ tiền xử lý (viết lại theo hành vi đã đọc)
def bo_hang_so(df):
    """Giữ cột có ít nhất một giá trị khác dòng đầu."""
    if len(df) == 0:
        return df.loc[:, []]
    return df.loc[:, (df != df.iloc[0]).any()]


def doi_mem_mb(df):
    df = df.copy()
    for c in df.columns:
        if c.endswith("_mem"):
            df[c] = df[c] / 1e6
    return df


def tien_xu_ly(df):
    """preprocess(dataset != None): bỏ time, bỏ cột hằng, đổi _mem sang MB."""
    df = df.drop(columns=[c for c in ("time.1", "time") if c in df.columns])
    return doi_mem_mb(bo_hang_so(df))


# ============================================================ SeverityScorer
def z_max(a, b):
    """StandardScaler: trung bình và độ lệch chuẩn (ddof=0) của a; độ lệch chuẩn 0 thì thang = 1."""
    mu = a.mean()
    sd = a.std()
    sd = 1.0 if sd == 0 else sd
    return float(np.max(np.abs((b - mu) / sd))), float(mu), float(a.var())


def chuan_hoa(lst):
    tong = sum(s for _, s in lst)
    return [(c, s / tong) for c, s in lst]


def muc_nghiem_trong(d, inject_time, giam_mau_metric=True):
    metric = d["metric"]
    if giam_mau_metric:
        metric = metric.iloc[::15, :]
    nm = tien_xu_ly(metric[metric["time"] < inject_time])
    am = tien_xu_ly(metric[metric["time"] >= inject_time])
    chung = [c for c in nm.columns if c in am.columns]
    nm, am = nm[chung], am[chung]
    logts = bo_hang_so(d["logts"])
    nl = logts[logts["time"] < inject_time].drop(columns=["time"])
    al = logts[logts["time"] >= inject_time].drop(columns=["time"])
    te, tl = d.get("tracets_err", pd.DataFrame()), d.get("tracets_lat", pd.DataFrame())
    co_trace = te is not None and len(te) > 0
    chi_tiet = {"metric": [], "log": [], "trace_err": [], "trace_lat": [], "nhan_1e9": []}
    m_r = sorted([(c, z_max(nm[c].to_numpy(), am[c].to_numpy())[0]) for c in nm.columns], key=lambda x: x[1], reverse=True)
    chi_tiet["metric"] = m_r
    l_r = []
    for c in nl.columns:
        a, b = nl[c].to_numpy(), al[c].to_numpy()
        if a.size == 0:
            continue
        l_r.append((c, z_max(a, b)[0]))
    l_r = sorted(l_r, key=lambda x: x[1], reverse=True)
    chi_tiet["log"] = l_r
    e_r, t_r = [], []
    if co_trace:
        te = bo_hang_so(te.ffill().fillna(0))
        tl = bo_hang_so(tl.ffill().fillna(0))
        ne, ae = te[te["time"] < inject_time].drop(columns=["time"]), te[te["time"] >= inject_time].drop(columns=["time"])
        nlat, alat = tl[tl["time"] < inject_time].drop(columns=["time"]), tl[tl["time"] >= inject_time].drop(columns=["time"])
        for c in ne.columns:
            s, mu, var = z_max(ne[c].to_numpy()[:-2], ae[c].to_numpy())
            if mu == 0 and var == 0:
                s = s * 1e9
                chi_tiet["nhan_1e9"].append(c)
            e_r.append((c, s))
        e_r = sorted(e_r, key=lambda x: x[1], reverse=True)
        for c in nlat.columns:
            t_r.append((c, z_max(nlat[c].to_numpy(), alat[c].to_numpy())[0]))
        t_r = sorted(t_r, key=lambda x: x[1], reverse=True)
    chi_tiet["trace_err"], chi_tiet["trace_lat"] = e_r, t_r
    return chuan_hoa(m_r), chuan_hoa(l_r), chuan_hoa(e_r), chuan_hoa(t_r), chi_tiet


def gop_cong(lst):
    dd = {}
    for c, s in lst:
        k = c.split("_")[0]
        dd[k] = dd.get(k, 0.0) + s
    return sorted(dd.items(), key=lambda x: x[1], reverse=True)


def gop_cao_nhat(lst):
    if not lst:
        return []
    lst = sorted(lst, key=lambda x: x[1], reverse=True)
    out = []
    for c, s in lst:
        k = c.split("_")[0]
        if k not in [x for x, _ in out]:
            out.append((k, s))
    tong = sum(s for _, s in out)
    return [(k, s / tong) for k, s in out]


# ============================================================ BIC tự tính
def loglik_gmm(X, g):
    n, d = X.shape
    tong = np.zeros(n)
    for k in range(g.n_components):
        mu, cov, w = g.means_[k], g.covariances_[k], g.weights_[k]
        L = np.linalg.cholesky(cov)
        z = np.linalg.solve(L, (X - mu).T)
        logdet = 2 * np.sum(np.log(np.diag(L)))
        tong = tong + w * np.exp(-0.5 * np.sum(z * z, axis=0) - 0.5 * (d * np.log(2 * np.pi) + logdet))
    return float(np.sum(np.log(tong)))


def bic_tay(X, g):
    n, d = X.shape
    k = g.n_components
    p = k * d * (d + 1) / 2 + k * d + (k - 1)
    return -2 * loglik_gmm(X, g) + p * np.log(n)


# ============================================================ RCD (viết lại)
def kmeans_1d(x, init, max_iter=300, tol_rel=1e-4):
    """Lloyd 1 chiều theo đúng trình tự của sklearn 1.2.2 (_kmeans_single_lloyd, lloyd_iter_chunked_dense):
    trừ trung bình; khoảng cách = c^2 - 2xc; cụm rỗng dời tới điểm xa tâm nhất (argpartition); hội tụ khi nhãn
    không đổi hoặc tổng bình phương dịch tâm <= tol*var."""
    x = x.astype(float)
    tol = np.var(x) * tol_rel
    xm = x.mean()
    X = x - xm
    c = init.astype(float).copy() - xm
    k = len(c)
    nhan_cu = np.full(len(X), -1)
    hoi_tu_chat = False
    for _ in range(max_iter):
        dist = (c ** 2)[None, :] - 2 * X[:, None] * c[None, :]
        nhan = np.argmin(dist, axis=1)
        tong = np.zeros(k)
        w = np.zeros(k)
        for i, l in enumerate(nhan):
            tong[l] += X[i]
            w[l] += 1
        rong = np.where(w == 0)[0]
        if len(rong):
            # sklearn 1.2.2 (_relocate_empty_clusters_dense): dời cả khi mọi khoảng cách bằng 0 (chưa có điều kiện
            # max == 0 như bản sau); thứ tự điểm "xa nhất" theo np.argpartition.
            kc = (X - c[nhan]) ** 2
            xa = np.argpartition(kc, -len(rong))[:-len(rong) - 1:-1]
            for idx in range(len(rong)):
                moi, fi = rong[idx], xa[idx]
                cu = nhan[fi]
                tong[cu] -= X[fi]
                tong[moi] = X[fi]
                w[moi] = 1
                w[cu] -= 1
        # _average_centers của sklearn: chia tổng cho trọng số khi trọng số > 0; cụm trọng số 0 giữ nguyên "tổng"
        # (thường bằng 0 trên dữ liệu đã trừ trung bình), không giữ tâm cũ.
        # Nhân với nghịch đảo (alpha = 1/trọng số) như sklearn, không chia trực tiếp: làm tròn khác nhau đổi kết
        # quả khi có hòa (kiểm trên 2 995 cột thử, runs/s12-kiem-kmeans.txt).
        c_moi = tong.copy()
        for j in range(k):
            if w[j] > 0:
                c_moi[j] = tong[j] * (1.0 / w[j])
        dich = (c_moi - c) ** 2
        c = c_moi
        if np.array_equal(nhan, nhan_cu):
            hoi_tu_chat = True
            break
        if dich.sum() <= tol:
            break
        nhan_cu = nhan
    return c + xm


def roi_rac_hoa(df_khong_F):
    out = {}
    so_bin = {}
    for col in df_khong_F.columns:
        x = df_khong_F[col].to_numpy(float)
        lo, hi = x.min(), x.max()
        if lo == hi:
            out[col] = np.zeros(len(x), dtype=int)
            so_bin[col] = 1
            continue
        u = np.linspace(lo, hi, BINS + 1)
        init = (u[1:] + u[:-1]) * 0.5
        c = np.sort(kmeans_1d(x, init))
        e = np.r_[lo, (c[1:] + c[:-1]) * 0.5, hi]
        mask = np.ediff1d(e, to_begin=np.inf) > 1e-8
        e = e[mask]
        so_bin[col] = len(e) - 1
        out[col] = np.searchsorted(e[1:-1], x, side="right").astype(int)
    return pd.DataFrame(out, columns=list(df_khong_F.columns)), so_bin


def kiem_chi2(D, card, x, y, S):
    """Chi-square độc lập có điều kiện X ⊥ Y | S trên dữ liệu mã hóa 0..card-1 (cách đếm của causal-learn 0.1.2.3)."""
    S = list(S)
    cx, cy = card[x], card[y]
    if not S:
        bang = np.zeros((1, cx, cy))
        np.add.at(bang, (np.zeros(D.shape[0], dtype=int), D[:, x], D[:, y]), 1)
    else:
        cs = card[S]
        idx = np.zeros(D.shape[0], dtype=np.int64)
        for k_, s in enumerate(S):
            idx = idx * cs[k_] + D[:, s]
        bang = np.zeros((int(np.prod(cs)), cx, cy))
        np.add.at(bang, (idx, D[:, x], D[:, y]), 1)
        bang = bang[bang.sum(axis=(1, 2)) != 0]
    nS = bang.sum(axis=(1, 2))
    kv = bang.sum(axis=2)[:, :, None] * bang.sum(axis=1)[:, None, :] / nS[:, None, None]
    zero = kv == 0
    kv1 = kv.copy()
    kv1[zero] = 1
    stat = np.sum((bang - kv) ** 2 / kv1)
    hang0 = zero.all(axis=2).sum(axis=1)
    cot0 = zero.all(axis=1).sum(axis=1)
    df = np.sum((bang.shape[1] - 1 - hang0) * (bang.shape[2] - 1 - cot0))
    return 1.0 if df == 0 else float(chi2.sf(stat, df)), float(stat), int(df)


def psi_pc_cuc_bo(D_full, alpha, ghi):
    """Ψ-PC cục bộ: đồ thị đầy đủ; chỉ kiểm cạnh nối F-node (cột cuối) với từng nút y, điều kiện trên các nút vừa kề
    y vừa kề F; độ sâu tăng dần. Trả: danh sách hàng xóm của F (theo chỉ số tăng), p-value đã ghi theo từng y."""
    # mã hóa lại từng cột thành 0..k-1 theo giá trị có mặt (np.unique return_inverse)
    D = np.column_stack([np.unique(D_full[:, j], return_inverse=True)[1] for j in range(D_full.shape[1])]).astype(np.int64)
    card = D.max(axis=0) + 1
    n = D.shape[1]
    x = n - 1
    ke = np.ones((n, n), dtype=bool)
    np.fill_diagonal(ke, False)
    pv = {}
    nhat_ky = []
    depth = -1
    while ke.sum(axis=1).max() - 1 > depth:
        depth += 1
        hang_xom = np.random.permutation(np.where(ke[x])[0])
        for y in hang_xom:
            ny = [s for s in np.where(ke[y])[0] if s != x]
            nyf = [s for s in ny if ke[x, s]] if depth > 0 else []
            for S in itertools.combinations(nyf, depth):
                p, stat, df = kiem_chi2(D, card, x, y, S)
                nhat_ky.append({"y": int(y), "S": [int(s) for s in S], "p": p, "chi2": stat, "df": df,
                                "doc_lap": p > alpha})
                if p > alpha:
                    ke[x, y] = ke[y, x] = False
                    break
                pv.setdefault(int(y), []).append(p)
    con = [int(j) for j in np.where(ke[x])[0]]
    ghi.append({"alpha": float(alpha), "depth_max": depth, "f_con_chi_so": con, "kiem": nhat_ky})
    return con, pv


def sap_theo_p(moi, pv):
    """Lấy lần lượt phần tử có danh sách p-value LỚN nhất (so như list Python, gặp hòa lấy cái đầu), đẩy xuống đáy."""
    a = list(moi)
    ds = [pv[i] for i in moi]
    ngan_xep = []
    while a:
        i_max = 0
        for i in range(1, len(ds)):
            if ds[i] > ds[i_max]:
                i_max = i
        ngan_xep = [a[i_max]] + ngan_xep
        del a[i_max]
        del ds[i_max]
    return ngan_xep


def run_psi_pc(n_df, a_df, alpha0, min_nodes, ghi_pc):
    if 0 in (len(n_df.columns), len(a_df.columns)):
        return []
    cot = list(n_df.columns)
    roi, so_bin = roi_rac_hoa(pd.concat([n_df, a_df]))
    Fcol = np.r_[np.zeros(len(n_df)), np.ones(len(a_df))].astype(int)
    D = np.column_stack([roi.to_numpy(), Fcol])
    nhan = cot + [F]
    if min_nodes == -1:
        min_nodes = len(cot)
    assert min_nodes < D.shape[0], "assert min_nodes < len(data) (rcd.py:168)"
    rc = []
    for alpha in np.arange(alpha0, TRAN, BUOC):
        ghi = []
        con, pv = psi_pc_cuc_bo(D, alpha, ghi)
        ten_con = [nhan[i] for i in con]
        ghi_pc.append({"alpha": float(alpha), "cot": nhan, "so_dong": int(D.shape[0]), "du_lieu": D.tolist(),
                       "so_bin": so_bin, "f_con": ten_con,
                       "p_values_F": [pv.get(i) for i in range(len(nhan))], "kiem": ghi[0]["kiem"]})
        moi = [i for i in con if nhan[i] not in rc]
        if not moi:
            continue
        rc += [nhan[i] for i in sap_theo_p(moi, pv)]
        if len(rc) == min_nodes:
            break
    return rc


def rcd_nhieu_pha(n_df, a_df, ghi_pc, ghi_level):
    f = list(n_df.columns)
    prev = len(f)
    while True:
        cot = np.random.permutation(np.array(f, dtype=object))
        khoi = [cot[i * GAMMA:(i * GAMMA) + GAMMA] for i in range(len(cot) // GAMMA + 1)]
        if len(khoi[-1]) == 0:
            khoi.pop()
        ghi_level.append({"so_cot": len(f), "khoi": [list(k) for k in khoi]})
        hop = []
        for k in khoi:
            hop += run_psi_pc(n_df.loc[:, list(k)], a_df.loc[:, list(k)], ALPHA_PHA1, 1, ghi_pc)
        f = hop
        if len(f) <= GAMMA or len(f) == prev:
            break
        prev = len(f)
    return run_psi_pc(n_df.loc[:, f], a_df.loc[:, f], ALPHA_PHA2, -1, ghi_pc)


def rcd_trong_cum(metric, logts, inject_time, sua):
    if not sua:
        metric = metric.iloc[::15, :]
    nm = tien_xu_ly(metric[metric["time"] < inject_time])
    am = tien_xu_ly(metric[metric["time"] >= inject_time])
    chung = [c for c in nm.columns if c in am.columns]
    nd, ad = nm[chung], am[chung]
    lg = bo_hang_so(logts)
    nl = lg[lg["time"] < inject_time].drop(columns=["time"])
    al = lg[lg["time"] >= inject_time].drop(columns=["time"])
    if sua:
        nn, na = min(len(nd), len(nl)), min(len(ad), len(al))
        nd, nl = nd.tail(nn).reset_index(drop=True), nl.tail(nn).reset_index(drop=True)
        ad, al = ad.head(na).reset_index(drop=True), al.head(na).reset_index(drop=True)
    nd = pd.concat([nd, nl], axis=1)  # ghép theo chỉ số dòng, như pandas.concat(axis=1)
    ad = pd.concat([ad, al], axis=1)
    nd = nd.loc[:, ~nd.columns.duplicated()].fillna(0)
    ad = ad.loc[:, ~ad.columns.duplicated()].fillna(0)
    nd = doi_mem_mb(bo_hang_so(nd.drop(columns=[c for c in ("time",) if c in nd.columns])))
    ad = doi_mem_mb(bo_hang_so(ad.drop(columns=[c for c in ("time",) if c in ad.columns])))
    chung = [c for c in nd.columns if c in ad.columns]
    return nd[chung], ad[chung]


# ============================================================ toàn bộ TORAI
def torai_tay(d, inject_time, sua):
    m_r, l_r, e_r, t_r, chi_tiet = muc_nghiem_trong(d, inject_time)
    s_m, s_l = gop_cong(m_r), gop_cao_nhat(l_r)
    s_lat = [("frontend", s) if i == "frontendservice" else (i, s) for i, s in gop_cong(t_r)]
    s_err = [("frontend", s) if i == "frontendservice" else (i, s) for i, s in gop_cong(e_r)]
    m = pd.DataFrame({"metric": pd.Series(dict(s_m)), "log": pd.Series(dict(s_l)),
                      "trace_lat": pd.Series(dict(s_lat)), "trace_err": pd.Series(dict(s_err))}).fillna(0)
    ds_service = m.index.to_list()
    X = m.to_numpy()
    bic, bic_tu_tinh = [], []
    for k in range(1, X.shape[0] + 1):
        g = GaussianMixture(n_components=k, covariance_type="full", max_iter=50, random_state=0).fit(X)
        bic.append(float(g.bic(X)))
        bic_tu_tinh.append(float(bic_tay(X, g)))
    k_tot = int(np.argmin(bic)) + 1
    g = GaussianMixture(n_components=k_tot, covariance_type="full", max_iter=50, random_state=0).fit(X)
    y_pred = g.predict(X)
    y_tb = X.mean(axis=1)
    cum = []
    for ci in sorted(set(y_pred)):
        idx = np.where(y_pred == ci)[0]
        cum.append((int(ci), float(np.mean(y_tb[idx]))))
    cum.sort(key=lambda x: x[1], reverse=True)
    metric15 = d["metric"].iloc[::15, :]
    logts = d["logts"]
    xep, cac_cum = [], []
    for ci, diem in cum:
        idx = np.where(y_pred == ci)[0]
        sv = [ds_service[i] for i in idx]
        diem_sv = y_tb[idx]
        rec = {"cum": ci, "diem_cum": diem, "services": sv, "diem_service": [float(v) for v in diem_sv]}
        if len(sv) == 1:
            xep.append(sv[0])
            rec["rcd"] = None
            cac_cum.append(rec)
            continue
        aa = sorted(zip(sv, diem_sv), key=lambda x: x[1], reverse=True)
        tm = metric15.loc[:, metric15.columns.str.startswith(tuple(sv))].copy()
        tm["time"] = metric15["time"]
        tl = logts.loc[:, logts.columns.str.startswith(tuple(sv))].copy()
        tl["time"] = logts["time"]
        n_df, a_df = rcd_trong_cum(tm, tl, inject_time, sua)
        ghi_pc, ghi_level = [], []
        rc = rcd_nhieu_pha(n_df, a_df, ghi_pc, ghi_level)
        tmp = [s.split("_")[0] for s in rc]
        noi_bo = [tmp[0]] + [s for i, s in enumerate(tmp) if i > 0 and s not in tmp[:i]] if tmp else []
        du_phong = len(noi_bo) != len(sv)
        xep += [a for a, _ in aa] if du_phong else noi_bo
        rec.update({"aa": [(a, float(s)) for a, s in aa], "rcd_vao": {"dong_normal": len(n_df), "dong_anomal": len(a_df),
                    "cot": list(n_df.columns)}, "level": ghi_level, "pc": ghi_pc, "rcd_ranks": rc, "noi_bo": noi_bo,
                    "du_phong": du_phong})
        cac_cum.append(rec)
    return {"chi_tiet_diem": chi_tiet, "service_list": ds_service, "X_train": X.tolist(), "bic": bic,
            "bic_tu_tinh": bic_tu_tinh, "n_comp": k_tot, "y_pred": [int(v) for v in y_pred],
            "cum_xep": cum, "cac_cum": cac_cum, "ranks": [f"{s}_A" for s in xep]}


# ============================================================ so với lượt chính thức
def sai_lech_tuong_doi(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.shape != b.shape:
        return float("inf")
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.abs(a - b) / np.maximum(np.abs(b), 1e-300)
    r[(a == b)] = 0
    return float(np.nanmax(r)) if r.size else 0.0


def so_sanh(tay, meta, ket_qua):
    tg = meta["trung_gian"]
    out = {}
    out["service_list"] = tay["service_list"] == tg["service_list"]
    out["X_train_sai_lech_tuong_doi_max"] = sai_lech_tuong_doi(tay["X_train"], tg["X_train"])
    out["bic_sai_lech_tuong_doi_max"] = sai_lech_tuong_doi(tay["bic"], tg["bic"])
    out["bic_tu_tinh_vs_sklearn_max"] = sai_lech_tuong_doi(tay["bic_tu_tinh"], tay["bic"])
    out["n_comp"] = tay["n_comp"] == tg["n_comp"]
    out["y_pred"] = tay["y_pred"] == tg["y_pred"]
    cum_tay = [c for c in tay["cac_cum"] if c.get("rcd") is not False and len(c["services"]) > 1]
    cum_ct = tg.get("cum", [])
    out["so_cum_chay_rcd"] = [len(cum_tay), len(cum_ct)]
    ds = []
    for a, b in zip(cum_tay, cum_ct):
        r = {"services": a["services"] == b["services"], "aa": sai_lech_tuong_doi([s for _, s in a["aa"]], [s for _, s in b["aa"]]),
             "rcd_ranks": a["rcd_ranks"] == b["rcd_ranks"], "du_phong": a["du_phong"] == b["du_phong"],
             "so_lan_pc": [len(a["pc"]), len(b["pc"])]}
        cot_ok = du_ok = fcon_ok = True
        p_max = 0.0
        for pa, pb in zip(a["pc"], b["pc"]):
            cot_ok &= pa["cot"] == pb["cot"]
            fcon_ok &= pa["f_con"] == pb["f_con"]
            if "du_lieu" in pb:
                du_ok &= np.array_equal(np.asarray(pa["du_lieu"]).astype(int), np.asarray(pb["du_lieu"]).astype(int))
            if "p_values_F" in pb:
                for va, vb in zip(pa["p_values_F"], pb["p_values_F"]):
                    if (va is None) != (vb is None):
                        p_max = float("inf")
                    elif va is not None:
                        p_max = max(p_max, sai_lech_tuong_doi(va, vb))
        r.update({"cot_moi_lan_pc": cot_ok, "du_lieu_roi_rac": du_ok, "f_con": fcon_ok, "p_value_sai_lech_max": p_max})
        ds.append(r)
    out["cum"] = ds
    out["ranks_cuoi"] = tay["ranks"] == ket_qua
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ca", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--length", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--bien-the", choices=["goc", "sua"], default="goc")
    ap.add_argument("--meta", required=True)
    ap.add_argument("--ket-qua", required=True)
    ap.add_argument("--ra", required=True)
    a = ap.parse_args()
    d, inject_time = dung_dau_vao(os.path.join(a.ca, "simple_metrics.csv"), "torai", a.length)
    np.random.seed(a.seed)
    tay = torai_tay(d, inject_time, a.bien_the == "sua")
    ten = Path(a.ket_qua).stem
    meta = [json.loads(x) for x in open(a.meta, encoding="utf-8") if json.loads(x)["ca"] == ten][0]
    kq = json.loads(Path(a.ket_qua).read_text(encoding="utf-8"))["0"]
    ss = so_sanh(tay, meta, kq)
    Path(a.ra).write_text(json.dumps({"so_sanh": ss, "tinh_tay": tay, "inject_time": inject_time}, ensure_ascii=False,
                                     indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)),
                          encoding="utf-8")
    print(json.dumps(ss, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
