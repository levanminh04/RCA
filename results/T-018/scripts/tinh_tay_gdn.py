"""T-018 B5 + một phần B6: tính lại GDN bằng numpy, độc lập với code của tác giả.

Không import module nào của repo GDN. torch chỉ dùng để nạp file trọng số (.pt) rồi chuyển sang numpy.
So với đầu ra chính thức do chay_gdn.py lưu (test_pred.npy, val_pred.npy, test_scores.npy, normal_scores.npy).

Chạy: D:/RCA-ext/envs/py38-gdn/Scripts/python.exe tinh_tay_gdn.py --run r1-re2tt5-seed5 --data re2tt5
Đầu ra: results/T-018/runs/<run>-tinh-tay.json và in bảng giải thích cho t* và t0.

Công thức (ký hiệu theo bài, Eq. 2–13; chỗ code khác bài ghi ở hồ sơ):
  e_ji = v_i·v_j / (|v_i||v_j|);  J_i = TopK_j(e_ji) (code: j chạy trên MỌI nút, kể cả i)
  S_i = (J_i \\ {i}) ∪ {i}
  h_i = W x_i;  π(i,j) = LeakyReLU_0.2( [h_i, v_i]·[a_i, a_em_i] + [h_j, v_j]·[a_j, a_em_j] )
  α_ij = softmax_{j∈S_i} π(i,j);  z_i = ReLU( BN1( Σ_{j∈S_i} α_ij h_j + b ) )
  ŝ_i = w·ReLU( BN2( z_i ∘ v_i ) ) + c
  Err_i(t) = |s_i(t) − ŝ_i(t)|;  a_i(t) = (Err_i(t) − med_i) / (|IQR_i| + 0.01)
  a~_i(t) = mean(a_i(t−3..t)) với t ≥ 3, bằng 0 với t < 3;  A(t) = max_i a~_i(t);  báo động khi A(t) > τ
  τ = max_{i,t} a~_i^val(t), trong đó a^val chuẩn hóa bằng med/IQR của chính tập kiểm định.
  Code: med_i, IQR_i lấy từ chính tập test (evaluate.py:52). Biến thể b (SPEC R-chuẩn-hóa-b): lấy từ tập kiểm định.
"""
import argparse
import json
import os

import numpy as np
import pandas as pd
import torch

WORK = r"D:\RCA-ext\work\T-018\gdn"
RES = r"D:\RCA-flashticket\results\T-018\runs"
W = 5          # slide_win (run.sh)
EPS_BN = 1e-5  # mặc định BatchNorm1d
EPS_IQR = 1e-2
K = 5          # topk (run.sh)


def nap(run, data, model=None):
    model = model or os.path.join(WORK, "runs", run, "model.pt")
    sd = {k: v.cpu().numpy().astype(np.float64) for k, v in torch.load(model).items()}
    feats = [l.strip() for l in open(os.path.join(WORK, "data", data, "list.txt")) if l.strip()]
    tr = pd.read_csv(os.path.join(WORK, "data", data, "train.csv"), index_col=0)[feats].to_numpy(np.float64)
    te = pd.read_csv(os.path.join(WORK, "data", data, "test.csv"), index_col=0)[feats].to_numpy(np.float64)
    return sd, feats, tr, te


def cua_so(X):
    """X: T×N. Trả về x (M×N×W), y (M×N) với M = T − W; đầu vào ép float32 như test() (`item.float()`)."""
    X32 = X.astype(np.float32).astype(np.float64)
    idx = np.arange(W, X.shape[0])
    x = np.stack([X32[i - W:i].T for i in idx])
    y = X32[idx]
    return x, y


class GDNNumpy:
    def __init__(self, sd):
        self.E = sd["embedding.weight"]
        g = "gnn_layers.0."
        self.Wl = sd[g + "gnn.lin.weight"]                  # 64 × W
        self.ai, self.aj = sd[g + "gnn.att_i"].reshape(-1), sd[g + "gnn.att_j"].reshape(-1)
        self.aei, self.aej = sd[g + "gnn.att_em_i"].reshape(-1), sd[g + "gnn.att_em_j"].reshape(-1)
        self.b = sd[g + "gnn.bias"]
        self.bn1 = [sd[g + "bn." + k] for k in ("weight", "bias", "running_mean", "running_var")]
        self.bn2 = [sd["bn_outlayer_in." + k] for k in ("weight", "bias", "running_mean", "running_var")]
        self.wo, self.bo = sd["out_layer.mlp.0.weight"].reshape(-1), sd["out_layer.mlp.0.bias"].reshape(-1)[0]
        E = self.E
        nrm = np.linalg.norm(E, axis=1)
        self.cos = (E @ E.T) / np.outer(nrm, nrm)
        N = E.shape[0]
        # TopK theo hàng; lấy K chỉ số lớn nhất (thứ tự trong J_i không ảnh hưởng tổng)
        self.J = np.argsort(-self.cos, axis=1, kind="stable")[:, :K]
        self.S = [sorted(set(self.J[i]) - {i}) + [i] for i in range(N)]
        self.ei_term = E @ self.aei
        self.ej_term = E @ self.aej

    @staticmethod
    def bn(z, p):
        w, b, m, v = p
        return (z - m) / np.sqrt(v + EPS_BN) * w + b

    def forward(self, x, chi_tiet_nut=None):
        """x: N×W (một cửa sổ). Trả về ŝ (N,), và nếu chi_tiet_nut=i thì kèm α_i, S_i, h, z."""
        h = x @ self.Wl.T                                   # N × 64
        pi_i = h @ self.ai + self.ei_term
        pi_j = h @ self.aj + self.ej_term
        N = h.shape[0]
        z = np.empty_like(h)
        alphas = {}
        for i in range(N):
            S = self.S[i]
            p = pi_i[i] + pi_j[S]
            p = np.where(p > 0, p, 0.2 * p)
            a = np.exp(p - p.max())
            a /= a.sum()
            z[i] = a @ h[S] + self.b
            if chi_tiet_nut is not None and i == chi_tiet_nut:
                alphas = dict(zip(S, a))
        z = np.maximum(self.bn(z, self.bn1), 0)
        o = np.maximum(self.bn(z * self.E, self.bn2), 0)
        s_hat = o @ self.wo + self.bo
        if chi_tiet_nut is not None:
            return s_hat, alphas, h, z
        return s_hat


def diem(pred, gt, ref_pred=None, ref_gt=None):
    """a~ theo công thức trên; med/IQR lấy từ (ref_pred, ref_gt) nếu có, ngược lại từ chính (pred, gt)."""
    err = np.abs(pred - gt)                                 # M × N
    base = err if ref_pred is None else np.abs(ref_pred - ref_gt)
    med = np.median(base, axis=0)
    iqr = np.percentile(base, 75, axis=0) - np.percentile(base, 25, axis=0)
    a = (err - med) / (np.abs(iqr) + EPS_IQR)
    sm = np.zeros_like(a)
    for t in range(3, a.shape[0]):
        sm[t] = a[t - 3:t + 1].mean(axis=0)
    return sm, med, iqr, a, err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--t0", type=int, default=100)
    ap.add_argument("--model", default=None, help="mặc định <run>/model.pt (lượt chỉ chấm thì truyền mô hình gốc)")
    a = ap.parse_args()
    out = os.path.join(WORK, "runs", a.run)
    sd, feats, tr, te = nap(a.run, a.data, a.model)
    g = GDNNumpy(sd)
    N = len(feats)

    # ---- dự báo trên test và val ----
    xt, yt = cua_so(te)
    xtr, ytr = cua_so(tr)
    vidx = np.load(os.path.join(out, "val_indices.npy"))
    xv, yv = xtr[vidx], ytr[vidx]
    pt = np.stack([g.forward(x) for x in xt])
    pv = np.stack([g.forward(x) for x in xv])

    o_pt, o_gt = np.load(os.path.join(out, "test_pred.npy")), np.load(os.path.join(out, "test_gt.npy"))
    o_pv, o_gv = np.load(os.path.join(out, "val_pred.npy")), np.load(os.path.join(out, "val_gt.npy"))
    o_sc, o_ns = np.load(os.path.join(out, "test_scores.npy")), np.load(os.path.join(out, "normal_scores.npy"))

    sm_t, med_t, iqr_t, a_t, err_t = diem(pt, yt)
    sm_v, med_v, iqr_v, a_v, err_v = diem(pv, yv)
    tau = sm_v.max()
    A = sm_t.max(axis=1)
    o_A = o_sc.max(axis=0)
    o_tau = o_ns.max()
    tol_a = 1e-3 + 1e-5 * np.abs(o_sc.T)
    lech_a = np.abs(sm_t - o_sc.T)
    am_tay, am_code = sm_t.argmax(axis=1), o_sc.argmax(axis=0)
    # tick mà hai cột đứng đầu chênh dưới dung sai: argmax có thể đổi mà không phải lỗi
    s2 = np.sort(o_sc, axis=0)
    sat = (s2[-1] - s2[-2]) < 2 * tol_a.max(axis=1)
    bd_tay, bd_code = A > tau, o_A > o_tau
    sat_tau = np.abs(o_A - o_tau) < 2 * tol_a.max(axis=1)
    kq = {
        "so_tick_test": int(len(A)), "so_cot": N, "so_cua_so_val": int(len(vidx)),
        "max_lech_pred_test": float(np.abs(pt - o_pt).max()), "max_lech_pred_val": float(np.abs(pv - o_pv).max()),
        "max_lech_gt_test": float(np.abs(yt - o_gt).max()), "max_lech_gt_val": float(np.abs(yv - o_gv).max()),
        "max_lech_diem_test": float(lech_a.max()), "so_o_vuot_dung_sai_diem": int((lech_a > tol_a).sum()),
        "max_lech_normal": float(np.abs(sm_v - o_ns.T).max()),
        "tau_tay": float(tau), "tau_code": float(o_tau),
        "argmax_khac": int((am_tay != am_code).sum()), "argmax_khac_ngoai_tick_sat": int(((am_tay != am_code) & ~sat).sum()),
        "bao_dong_khac": int((bd_tay != bd_code).sum()), "bao_dong_khac_ngoai_tick_sat": int(((bd_tay != bd_code) & ~sat_tau).sum()),
        "so_bao_dong_code": int(bd_code.sum()),
    }

    # ---- soi giá trị trung gian (E2, E10) ----
    kq["nut_co_chinh_no_trong_topk"] = int(sum(i in g.J[i] for i in range(N)))
    kq["so_lang_gieng_that_trung_binh"] = float(np.mean([len(s) - 1 for s in g.S]))
    kq["iqr_test_duoi_1e-6"] = int((np.abs(iqr_t) < 1e-6).sum())
    kq["iqr_val_duoi_1e-6"] = int((np.abs(iqr_v) < 1e-6).sum())
    hang_hoc = (tr.max(axis=0) - tr.min(axis=0)) == 0
    kq["cot_hang_trong_tap_hoc"] = int(hang_hoc.sum())
    dem = np.bincount(am_code, minlength=N)
    top = np.argsort(-dem)[:5]
    kq["cot_hay_la_argmax"] = [{"cot": feats[i], "so_tick": int(dem[i]), "iqr_test": float(iqr_t[i]),
                                "hang_trong_tap_hoc": bool(hang_hoc[i])} for i in top]
    kq["ty_le_tick_argmax_la_cot_iqr0_test"] = float(np.isin(am_code, np.flatnonzero(np.abs(iqr_t) < 1e-6)).mean())

    # ---- biến thể b: chuẩn hóa test bằng med/IQR của tập kiểm định ----
    sm_b, *_ = diem(pt, yt, pv, yv)
    A_b = sm_b.max(axis=1)
    kq["bien_the_b"] = {"so_bao_dong": int((A_b > tau).sum()), "A_max": float(A_b.max()), "tick_A_max": int(A_b.argmax()),
                        "cot_A_max": feats[int(sm_b[A_b.argmax()].argmax())]}
    np.save(os.path.join(out, "A_bien_the_b.npy"), A_b)

    # ---- hoán vị nút (B6 ii): v' = v[p], x' = x[p] -> ŝ' phải bằng ŝ[p] ----
    p = np.random.RandomState(1).permutation(N)
    sd2 = dict(sd)
    sd2["embedding.weight"] = sd["embedding.weight"][p]
    g2 = GDNNumpy(sd2)
    pt2 = np.stack([g2.forward(x[p]) for x in xt[:200]])
    kq["hoan_vi_nut_max_lech"] = float(np.abs(pt2 - pt[:200][:, p]).max())

    # ---- giải thích hai tick ----
    def giai_thich(t, nhan):
        f = int(sm_t[t].argmax())
        s_hat, alpha, h, z = g.forward(xt[t], chi_tiet_nut=f)
        top5 = np.argsort(-sm_t[t])[:5]
        return {
            "nhan": nhan, "tick": int(t), "dong_tho": int(t + W), "A": float(A[t]), "tau": float(tau), "bao_dong": bool(A[t] > tau),
            "cot_dau": feats[f],
            "cua_so_vao_chuan_hoa": [round(float(v), 6) for v in xt[t][f]],
            "lang_gieng_va_alpha": {feats[j]: round(float(w), 4) for j, w in sorted(alpha.items(), key=lambda kv: -kv[1])},
            "cos_lang_gieng": {feats[j]: round(float(g.cos[f, j]), 4) for j in g.J[f]},
            "du_bao": float(s_hat[f]), "thuc_te": float(yt[t][f]), "err": float(err_t[t][f]),
            "med_test": float(med_t[f]), "iqr_test": float(iqr_t[f]), "a_t-3..t": [round(float(v), 3) for v in a_t[t - 3:t + 1, f]],
            "a_lam_tron": float(sm_t[t][f]),
            "med_val": float(med_v[f]), "iqr_val": float(iqr_v[f]), "a_lam_tron_bien_the_b": float(sm_b[t][f]),
            "top5": [{"cot": feats[i], "a_lam_tron": round(float(sm_t[t][i]), 3)} for i in top5],
        }
    t_star = int(o_A.argmax())
    kq["giai_thich"] = [giai_thich(t_star, "t*"), giai_thich(a.t0, "t0")]
    np.save(os.path.join(out, "A_tay.npy"), A)
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, a.run + "-tinh-tay.json"), "w", encoding="utf-8") as fh:
        json.dump(kq, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in kq.items() if k != "giai_thich"}, ensure_ascii=False, indent=1))
    for gt_ in kq["giai_thich"]:
        print(json.dumps(gt_, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
