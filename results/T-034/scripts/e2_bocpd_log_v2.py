"""T-034 E2 (bản v2): BOCPD của BARO với posterior và chuẩn hóa hoàn toàn trong miền log.

Bản v2 khác bản v1 (e2_bocpd_log.py, giữ nguyên cho lượt e2-001) ở phần ĐO và SO, không ở phép tính:
  - tách các trạng thái vùng bình thường (R gốc >= 1e-290) theo lịch sử dòng dõi: dòng dõi từng xuống dưới ngưỡng chuẩn hóa
    (R < 2,2e-308) hay chưa. Lý do: lượt e2-001 cho thấy trạng thái đi qua vùng dưới chuẩn hóa rồi lớn lên lại mang sai số làm tròn
    lớn trong bản gốc; gộp chúng với trạng thái sạch làm tiêu chí 1e-9 mất nghĩa (thiết kế, Mục nối 2);
  - thêm chế độ determinism để kiểm bản gốc chạy lại có trùng bản lưu từng bit không, theo cấu hình luồng BLAS.
Hàm log_run, LogLikelihood, quy tắc m/CP, fixture và dung sai đã khai giữ nguyên từng dòng.

Thiết kế: results/T-034/thiet-ke-hai-phep-kiem.md, phần E2 (viết trước khi chạy).
Giữ nguyên: X, prior, hazard 1/50, update_theta của lớp gốc, quy ước m[i] = argmax R[:, i+1], quy tắc CP |m[i] - m[i-1]| > 1.
Yếu tố duy nhất bị đổi: miền số học của posterior (log thay cho tuyến tính). Mật độ dự báo là logpdf của cùng phân phối,
gọi với đúng các đối số mà mã gốc dựng cho pdf.

Dùng:
  python e2_bocpd_log.py fixtures <thư mục ra> <thư mục gốc BARO>
  python e2_bocpd_log.py chain <npz nguồn> <thư mục ra> <nhãn chuỗi> <thư mục gốc BARO> [zero-lineage-summary.json]
"""
import hashlib
import json
import os
import platform
import sys
import time
from functools import partial
from itertools import islice
from pathlib import Path

import numpy as np
import scipy
import scipy.stats as ss
from numpy.linalg import inv
from scipy.special import logsumexp

BOCPD_SHA = "4a57fde3bce6ff8daf89eea08630e030b136fa3bc1a7e5c86d7bba44a1ea9f8e"      # BARO e35f4ec, bản T-033 đã ghim
HAZARD_LAM = 50
TINY = 2.2250738585072014e-308      # số chuẩn hóa dương nhỏ nhất của float64
NORMAL_ZONE = 1e-290                # trên mức này R gốc còn đủ độ chính xác để so log
NEAR_TIE = 1e-9

try:
    import psutil
    _PROC = psutil.Process()

    def rss():
        return int(_PROC.memory_info().rss)
except Exception:                   # pragma: no cover
    def rss():
        return -1


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_native(baro_root):
    path = Path(baro_root) / "baro" / "_bocpd.py"
    got = sha(path)
    if got != BOCPD_SHA:
        raise SystemExit(f"_bocpd.py không khớp bản ghim: {got}")
    sys.path.insert(0, str(baro_root))
    import baro._bocpd as nb
    assert Path(nb.__file__).resolve() == path.resolve()
    return nb, got


# ---------------------------------------------------------------------------------------------------------------------
# Quy tắc m và CP (chép từ src/p3/adapters/phat_hien.py::diem_doi_tu_R; kiểm tương đương ở fixture)
# ---------------------------------------------------------------------------------------------------------------------
def m_and_cps(matrix):
    """matrix: R tuyến tính hoặc logR; cột 1..T. Trả (m, danh sách chỉ số CP)."""
    T = matrix.shape[1] - 1
    m = matrix[:, 1:T + 1].argmax(axis=0)
    cps = [i for i in range(1, T) if abs(int(m[i]) - int(m[i - 1])) > 1]
    return m, cps


def diem_doi_tu_R(R):
    """Bản chép nguyên văn hàm của src/p3/adapters/phat_hien.py để đối chiếu chỉ số."""
    T = R.shape[1] - 1
    sub = R[:, 1:T + 1]
    bad = ~np.isfinite(sub).all(axis=0)
    if bad.any():
        return None, int(np.argmax(bad)) + 1
    m = sub.argmax(axis=0)
    cps = [i for i in range(1, T) if abs(int(m[i]) - int(m[i - 1])) > 1]
    return cps, m


# ---------------------------------------------------------------------------------------------------------------------
# Lớp bọc: cùng trạng thái tham số và cùng update_theta của lớp gốc; chỉ trả log-density thay cho density.
# ---------------------------------------------------------------------------------------------------------------------
class LogLikelihood:
    def __init__(self, native):
        self.native = native

    def logpdf(self, data):
        nat = self.native
        nat.t += 1
        # ba dòng dưới chép đúng biểu thức của MultivariateT.pdf
        t_dof = nat.dof - nat.dims + 1
        expanded = np.expand_dims((nat.kappa * t_dof) / (nat.kappa + 1), (1, 2))
        ret = np.empty(nat.t)
        for i, (df, loc, shape) in islice(enumerate(zip(t_dof, nat.mu, inv(expanded * nat.scale))), nat.t):
            ret[i] = ss.multivariate_t.logpdf(x=data, df=df, loc=loc, shape=shape)
        return ret

    def update_theta(self, data, **kwargs):
        self.native.update_theta(data, **kwargs)


class ScriptedLikelihood:
    """Chỉ cho fixture F3: bảng log-density đặt sẵn; pdf = exp(bảng). Không có tham số."""
    def __init__(self, log_table):
        self.log_table = log_table
        self.t = 0

    def pdf(self, data):
        self.t += 1
        return np.exp(self.log_table[self.t - 1][: self.t])

    def logpdf(self, data):
        self.t += 1
        return np.array(self.log_table[self.t - 1][: self.t], dtype=float)

    def update_theta(self, data, **kwargs):
        pass


def log_run(X, hazard_function, likelihood, tick=None):
    """Đệ quy BOCPD trong miền log; cùng thứ tự bước với online_changepoint_detection gốc."""
    T = len(X)
    logR = np.full((T + 1, T + 1), -np.inf)
    logR[0, 0] = 0.0
    log_normalizer = np.empty(T)
    for t, x in enumerate(X):
        logp = likelihood.logpdf(x)
        H = hazard_function(np.array(range(t + 1)))            # cùng lời gọi như mã gốc
        a = logR[0:t + 1, t] + logp
        logR[1:t + 2, t + 1] = a + np.log(1 - H)
        logR[0, t + 1] = logsumexp(a + np.log(H))
        z = logsumexp(logR[:t + 2, t + 1])
        logR[:t + 2, t + 1] -= z
        log_normalizer[t] = z
        likelihood.update_theta(x, t=t)
        if tick:
            tick(t)
    return logR, log_normalizer


# ---------------------------------------------------------------------------------------------------------------------
# Tham chiếu độ chính xác cao (mpmath): bản cài độc lập của cùng mô hình, đệ quy tuyến tính, không underflow.
# ---------------------------------------------------------------------------------------------------------------------
def mp_reference_model(X, lam, dps=50):
    import mpmath as mp
    mp.mp.dps = dps
    T, d = X.shape
    Hf = float(1 / lam * np.ones(1)[0])
    H, G = mp.mpf(Hf), mp.mpf(1 - Hf)
    eye = mp.eye(d)
    prior = (mp.mpf(d + 1), mp.mpf(1), mp.zeros(d, 1), eye.copy())      # dof, kappa, mu, P = inv(scale)
    states = [prior]

    def logpdf(x, state):
        dof, kappa, mu, P = state
        df = dof - d + 1
        e = kappa * df / (kappa + 1)
        c = x - mu
        y = mp.lu_solve(P, c)
        maha = e * (c.T * y)[0]
        logdet_shape = mp.log(mp.det(P)) - d * mp.log(e)        # shape = P / e
        return (mp.loggamma((df + d) / 2) - mp.loggamma(df / 2) - mp.mpf(d) / 2 * mp.log(df * mp.pi)
                - logdet_shape / 2 - (df + d) / 2 * mp.log(1 + maha / df))

    def pdf_fn(t):
        x = mp.matrix([mp.mpf(float(v)) for v in X[t]])
        return [mp.exp(logpdf(x, s)) for s in states], x

    def update(x):
        new = [prior]
        for dof, kappa, mu, P in states:
            c = x - mu
            new.append((dof + 1, kappa + 1, (kappa * mu + x) / (kappa + 1), P + (kappa / (kappa + 1)) * (c * c.T)))
        states[:] = new

    return mp_recursion(T, H, G, pdf_fn, update)


def mp_reference_scripted(log_table, lam, dps=50):
    import mpmath as mp
    mp.mp.dps = dps
    Hf = float(1 / lam * np.ones(1)[0])
    H, G = mp.mpf(Hf), mp.mpf(1 - Hf)
    T = len(log_table)

    def pdf_fn(t):
        return [mp.mpf(float(np.exp(v))) for v in log_table[t][: t + 1]], None

    return mp_recursion(T, H, G, pdf_fn, lambda x: None)


def mp_recursion(T, H, G, pdf_fn, update):
    import mpmath as mp
    R = [mp.mpf(1)]
    logR = np.full((T + 1, T + 1), -np.inf)
    logR[0, 0] = 0.0
    m = np.empty(T, dtype=int)
    gap = np.empty(T)
    for t in range(T):
        pdf, x = pdf_fn(t)
        grown = [R[r] * pdf[r] * G for r in range(t + 1)]
        reset = sum(R[r] * pdf[r] * H for r in range(t + 1))
        new = [reset] + grown
        total = sum(new)
        R = [v / total for v in new]
        logs = [mp.log(v) for v in R]
        order = sorted(range(len(R)), key=lambda r: (-R[r], r))
        m[t] = order[0]
        gap[t] = float(logs[order[0]] - logs[order[1]]) if len(order) > 1 else np.inf
        logR[: t + 2, t + 1] = [float(v) for v in logs]
        update(x)
    cps = [i for i in range(1, T) if abs(int(m[i]) - int(m[i - 1])) > 1]
    return {"logR": logR, "m": m, "cps": cps, "gap": gap}


# ---------------------------------------------------------------------------------------------------------------------
# So bản gốc với bản miền log trên toàn chuỗi
# ---------------------------------------------------------------------------------------------------------------------
def top_states(column, k=5):
    order = np.argsort(-column, kind="stable")[:k]
    return order.astype(int), column[order]


def lineage_dipped(R):
    """dipped[r, t] = True nếu dòng dõi của trạng thái (r, t) từng có R gốc < TINY ở một cột trước đó (kể cả bằng 0)."""
    T = R.shape[1] - 1
    dipped = np.zeros(R.shape, dtype=bool)
    for t in range(1, T + 1):
        dipped[1:t + 1, t] = dipped[0:t, t - 1] | (R[0:t, t - 1] < TINY)
    return dipped


def compare_full(R, logR, times=None, slices=()):
    T = R.shape[1] - 1
    rows = np.arange(T + 1)[:, None]
    cols = np.arange(T + 1)[None, :]
    reach = rows <= cols
    with np.errstate(divide="ignore"):
        logN = np.where(R > 0, np.log(np.where(R > 0, R, 1.0)), -np.inf)
    zero = reach & (R == 0)
    denorm = reach & (R > 0) & (R < TINY)
    finite_log = np.isfinite(logR)
    out = {"T": int(T), "reachable_states": int(reach[:, 1:].sum()),
           "native_exact_zero_states": int(zero[:, 1:].sum()), "native_subnormal_states": int(denorm[:, 1:].sum()),
           "log_domain_nonfinite_reachable": int((reach & ~finite_log)[:, 1:].sum()),
           "log_domain_nan": int(np.isnan(logR).sum()), "log_domain_posinf": int(np.isposinf(logR).sum())}

    def first(mask):
        idx = np.argwhere(mask[:, 1:].T)                 # sắp theo cột rồi hàng
        return None if len(idx) == 0 else {"column": int(idx[0][0]) + 1, "run_length": int(idx[0][1])}

    out["first_native_exact_zero"] = first(zero)
    out["first_native_subnormal"] = first(denorm)
    # khối lượng (theo bản miền log) nằm ở các trạng thái mà bản gốc cho bằng 0, và ở các trạng thái dưới chuẩn hóa
    lost = np.full(T + 1, -np.inf)
    lost_sub = np.full(T + 1, -np.inf)
    for t in range(1, T + 1):
        zc = zero[:, t]
        if zc.any():
            lost[t] = logsumexp(logR[zc, t])
        dc = denorm[:, t]
        if dc.any():
            lost_sub[t] = logsumexp(logR[dc, t])
    tmax = int(np.argmax(lost))
    out["lost_mass_log_max"] = float(lost[tmax]) if np.isfinite(lost[tmax]) else None
    out["lost_mass_log_max_column"] = tmax if np.isfinite(lost[tmax]) else None
    out["columns_with_native_zero"] = int(np.isfinite(lost).sum())
    # chênh posterior ở vùng bản gốc còn đủ chính xác
    normal = reach & (R >= NORMAL_ZONE)
    err = np.where(normal, np.abs(logN - np.where(finite_log, logR, 0.0)), 0.0)
    err_col = err.max(axis=0)
    out["posterior_log_abs_error_max_normal_zone"] = float(err_col[1:].max())
    out["posterior_log_abs_error_max_column"] = int(np.argmax(err_col[1:])) + 1
    out["normal_zone_states"] = int(normal[:, 1:].sum())
    dipped = lineage_dipped(R)
    clean = normal & ~dipped
    dirty = normal & dipped
    err_clean = np.where(clean, err, 0.0)
    err_dirty = np.where(dirty, err, 0.0)
    out["normal_zone_states_lineage_never_subnormal"] = int(clean[:, 1:].sum())
    out["normal_zone_states_lineage_was_subnormal"] = int(dirty[:, 1:].sum())
    out["posterior_log_abs_error_max_lineage_never_subnormal"] = float(err_clean[:, 1:].max())
    out["posterior_log_abs_error_max_lineage_was_subnormal"] = float(err_dirty[:, 1:].max())
    bad = dirty & (err > 1e-9)
    out["states_error_gt_1e-9_lineage_was_subnormal"] = int(bad[:, 1:].sum())
    out["states_error_gt_1e-9_lineage_never_subnormal"] = int((clean & (err > 1e-9))[:, 1:].sum())
    out["max_log_mass_of_states_error_gt_1e-9"] = (float(np.max(np.where(bad, np.where(finite_log, logR, -np.inf), -np.inf)[:, 1:]))
                                                    if bad[:, 1:].any() else None)
    with np.errstate(under="ignore", over="ignore"):
        tv = 0.5 * np.abs(R - np.where(finite_log, np.exp(np.where(finite_log, logR, 0.0)), 0.0)).sum(axis=0)
    out["total_variation_max"] = float(tv[1:].max())
    out["total_variation_max_column"] = int(np.argmax(tv[1:])) + 1
    out["log_normalization_abs_max"] = float(max(abs(float(logsumexp(logR[: t + 1, t]))) for t in range(1, T + 1)))
    # hai trạng thái đầu theo cột, hai bản
    m_nat, cps_nat = m_and_cps(R)
    m_log, cps_log = m_and_cps(logR)
    gap_nat = np.empty(T)
    gap_log = np.empty(T)
    top5_nat_i = np.zeros((T, 5), dtype=int)
    top5_nat_v = np.full((T, 5), -np.inf)
    top5_log_i = np.zeros((T, 5), dtype=int)
    top5_log_v = np.full((T, 5), -np.inf)
    for i in range(T):
        t = i + 1
        k = min(5, t + 1)
        idx, val = top_states(logN[: t + 1, t], k)
        top5_nat_i[i, :k], top5_nat_v[i, :k] = idx, val
        gap_nat[i] = val[0] - val[1]
        idx, val = top_states(logR[: t + 1, t], k)
        top5_log_i[i, :k], top5_log_v[i, :k] = idx, val
        gap_log[i] = val[0] - val[1]
    out["m_equal_all"] = bool(np.array_equal(m_nat, m_log))
    differ = np.flatnonzero(m_nat != m_log)
    out["m_differences"] = int(len(differ))
    out["m_first_difference_index"] = int(differ[0]) if len(differ) else None
    classes = {"underflow": 0, "rounding_or_near_tie": 0, "other": 0}
    detail = []
    for i in differ:
        t = i + 1
        r_log = int(m_log[i])
        native_value_at_log_map = float(R[r_log, t])
        if native_value_at_log_map == 0 or native_value_at_log_map < TINY:
            kind = "underflow"
        elif min(gap_nat[i], gap_log[i]) <= NEAR_TIE:
            kind = "rounding_or_near_tie"
        else:
            kind = "other"
        classes[kind] += 1
        if len(detail) < 200:
            detail.append({"index": int(i), "m_native": int(m_nat[i]), "m_log": r_log, "native_R_at_log_map": native_value_at_log_map,
                           "gap_native": float(gap_nat[i]), "gap_log": float(gap_log[i]), "class": kind})
    out["m_difference_classes"] = classes
    out["m_difference_detail"] = detail
    out["cp_equal"] = cps_nat == cps_log
    out["cp_native"] = [int(i) for i in cps_nat]
    out["cp_log"] = [int(i) for i in cps_log]
    out["cp_only_native"] = sorted(set(cps_nat) - set(cps_log))
    out["cp_only_log"] = sorted(set(cps_log) - set(cps_nat))
    if times is not None:
        out["cp_native_timestamps"] = [int(times[i]) for i in cps_nat]
        out["cp_log_timestamps"] = [int(times[i]) for i in cps_log]
        out["cp_only_native_timestamps"] = [int(times[i]) for i in out["cp_only_native"]]
        out["cp_only_log_timestamps"] = [int(times[i]) for i in out["cp_only_log"]]
    for name, cps in (("native", cps_nat), ("log", cps_log)):
        before = [i for i in cps if i < 720]
        after = [i for i in cps if i >= 720]
        out["first_cp_" + name] = int(cps[0]) if cps else None
        out["first_cp_before_720_" + name] = int(before[0]) if before else None
        out["first_cp_from_720_" + name] = int(after[0]) if after else None
        out["n_cp_before_720_" + name] = len(before)
        out["n_cp_from_720_" + name] = len(after)
    out["gap_native_min"] = float(gap_nat.min())
    out["gap_native_min_index"] = int(np.argmin(gap_nat))
    out["gap_log_min"] = float(gap_log.min())
    out["gap_log_min_index"] = int(np.argmin(gap_log))
    out["gap_abs_difference_max"] = float(np.nanmax(np.abs(np.where(np.isfinite(gap_nat) & np.isfinite(gap_log), gap_nat - gap_log, 0.0))))
    out["columns_near_tie_native"] = int((gap_nat <= NEAR_TIE).sum())
    out["columns_near_tie_log"] = int((gap_log <= NEAR_TIE).sum())
    arrays = {"m_native": m_nat, "m_log": m_log, "cp_native": np.array(cps_nat, dtype=int), "cp_log": np.array(cps_log, dtype=int),
              "gap_native": gap_nat, "gap_log": gap_log, "lost_mass_log": lost, "lost_mass_subnormal_log": lost_sub,
              "posterior_log_abs_error_by_column": err_col, "total_variation_by_column": tv,
              "native_zero_count_by_column": zero.sum(axis=0), "native_subnormal_count_by_column": denorm.sum(axis=0),
              "top5_native_index": top5_nat_i, "top5_native_log": top5_nat_v, "top5_log_index": top5_log_i, "top5_log_value": top5_log_v}
    for t in slices:
        if 0 < t <= T:
            arrays[f"slice_logR_col{t}"] = logR[: t + 1, t].copy()
            arrays[f"slice_nativeR_col{t}"] = R[: t + 1, t].copy()
    return out, arrays


# ---------------------------------------------------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------------------------------------------------
def fixture_data():
    rng = np.random.default_rng(20261013)
    f1 = np.vstack([rng.normal(0.0, 0.3, size=(35, 3)), rng.normal(1.0, 0.3, size=(25, 3))])
    # F2 bản đầu (30/25/25 điểm, mức 0/5/-3) không tạo underflow trong bản gốc: đuôi Student-t nặng nên một lần nhảy chỉ phạt cỡ
    # -(df+d)/2*log(1+z^2/df); với df khoảng 30 khối lượng nhỏ nhất chỉ tới e^-126 (lượt e2-fixtures-laptop-001-fail). Bản này kéo đoạn
    # đầu lên 200 điểm để df lớn tại lần nhảy; bản gốc khi đó có trạng thái bằng đúng 0. Chỉ đổi dữ liệu fixture, không đổi phép tính.
    rng2 = np.random.default_rng(20261013)
    f2 = np.vstack([rng2.normal(0.0, 0.01, size=(200, 2)), rng2.normal(40.0, 0.01, size=(15, 2)), rng2.normal(-40.0, 0.01, size=(15, 2))])
    T3 = 12
    f3 = [[0.0] * (t + 1) for t in range(T3)]
    for t in (4, 5):
        f3[t][t] = float(np.log(1e-200))          # dòng dõi già nhất bị phạt hai bước: khối lượng xuống cỡ 1e-400
    for t in (6, 7):
        f3[t][t] = float(np.log(1e250))           # rồi được thưởng hai bước: theo số học chính xác nó thành MAP
    return f1, f2, f3


def compare_to_reference(logR, ref, tol_abs, tol_rel):
    T = logR.shape[1] - 1
    reach = np.arange(T + 1)[:, None] <= np.arange(T + 1)[None, :]
    diff = np.zeros_like(logR)
    diff[reach] = np.abs(logR[reach] - ref["logR"][reach])
    bound = tol_abs + tol_rel * np.abs(np.where(reach, ref["logR"], 0.0))
    m, cps = m_and_cps(logR)
    clear = ref["gap"] > 1e-6
    return {"max_abs_log_difference": float(np.nanmax(diff)), "within_tolerance": bool((diff <= bound).all()),
            "m_equal_where_reference_gap_clear": bool(np.array_equal(m[clear], ref["m"][clear])), "steps_reference_near_tie": int((~clear).sum()),
            "m_equal_all": bool(np.array_equal(m, ref["m"])), "cps": [int(i) for i in cps], "cps_reference": [int(i) for i in ref["cps"]],
            "cp_equal": cps == ref["cps"], "reference_gap_min": float(ref["gap"].min())}


def run_fixtures(out, nb, bocpd_sha):
    hazard = partial(nb.constant_hazard, HAZARD_LAM)
    f1, f2, f3 = fixture_data()
    result = {"schema": "T034-E2-fixtures-v1", "bocpd_sha256": bocpd_sha, "tolerances": {
        "F1_native_log_abs": 1e-9, "F1_pdf_relative": 1e-12, "F1_normalization_abs": 1e-12, "F1_reference_abs": 1e-7,
        "F2_reference": "1e-6 + 1e-9*|log R_tc|", "F3_reference": "1e-9 + 1e-12*|log R_tc|", "reference_near_tie_gap": 1e-6}}
    began = time.perf_counter()

    # ---- F1: không underflow ----
    d = f1.shape[1]
    R, maxes = nb.online_changepoint_detection(f1, hazard, nb.MultivariateT(dims=d))
    lik = LogLikelihood(nb.MultivariateT(dims=d))
    logR, _ = log_run(f1, hazard, lik)
    plain = nb.MultivariateT(dims=d)
    probe = LogLikelihood(nb.MultivariateT(dims=d))
    pdf_bit_equal, pdf_rel_max = True, 0.0
    for x in f1:                                    # density: exp(logpdf) so với pdf gốc, cùng trạng thái
        p = plain.pdf(x)
        lp = probe.logpdf(x)
        e = np.exp(lp)
        pdf_bit_equal &= bool(np.array_equal(e, p))
        pdf_rel_max = max(pdf_rel_max, float(np.max(np.abs(e - p) / p)))
        plain.update_theta(x)
        probe.update_theta(x)
    state_equal = all(np.array_equal(getattr(plain, k), getattr(lik.native, k)) for k in ("dof", "kappa", "mu", "scale"))
    cmp1, _arr = compare_full(R, logR)
    cps_p3, m_p3 = diem_doi_tu_R(np.where(np.isfinite(logR), np.exp(np.where(np.isfinite(logR), logR, 0.0)), 0.0))
    m_log, cps_log = m_and_cps(logR)
    cps_nat_p3, m_nat_p3 = diem_doi_tu_R(R)
    T = len(f1)
    reach = np.arange(T + 1)[:, None] <= np.arange(T + 1)[None, :]
    min_native = float(R[reach & (np.arange(T + 1)[None, :] >= 1)].min())
    ref1 = mp_reference_model(f1, HAZARD_LAM)
    r1 = compare_to_reference(logR, ref1, 1e-7, 0.0)
    f1_checks = {
        "fixture hợp lệ: mọi trạng thái đạt được có R gốc > 1e-290": min_native > NORMAL_ZONE,
        "exp(logpdf) trùng pdf gốc từng bit hoặc lệch tương đối <= 1e-12": pdf_bit_equal or pdf_rel_max <= 1e-12,
        "posterior: |logR_log - log R_gốc| <= 1e-9": cmp1["posterior_log_abs_error_max_normal_zone"] <= 1e-9,
        "MAP trùng bản gốc ở mọi bước": cmp1["m_equal_all"],
        "CP trùng bản gốc": cmp1["cp_equal"],
        "chuẩn hóa: |logsumexp mỗi cột| <= 1e-12": cmp1["log_normalization_abs_max"] <= 1e-12,
        "mọi trạng thái đạt được hữu hạn": cmp1["log_domain_nonfinite_reachable"] == 0 and cmp1["log_domain_nan"] == 0,
        "tham số sau cùng trùng đối tượng gốc từng bit": state_equal,
        "chỉ số: diem_doi_tu_R trên exp(logR) cho cùng m, CP": cps_p3 == cps_log and np.array_equal(m_p3, m_log),
        "chỉ số: m_and_cps trùng diem_doi_tu_R trên R gốc": cps_nat_p3 == cmp1["cp_native"] and np.array_equal(m_nat_p3, m_and_cps(R)[0]),
        "tham chiếu mpmath: |logR_log - log R_tc| <= 1e-7": r1["within_tolerance"],
        "tham chiếu mpmath: MAP và CP trùng": r1["m_equal_where_reference_gap_clear"] and r1["cp_equal"],
    }
    result["F1"] = {"T": T, "d": d, "pdf_bit_equal": pdf_bit_equal, "pdf_relative_max": pdf_rel_max, "min_native_reachable_R": min_native,
                    "native_vs_log": {k: v for k, v in cmp1.items() if k != "m_difference_detail"}, "reference": r1,
                    "n_cp": len(cmp1["cp_native"]), "checks": f1_checks, "pass": all(f1_checks.values())}

    # ---- F2: underflow thật trong bản gốc ----
    d = f2.shape[1]
    with np.errstate(all="ignore"):
        R2, _ = nb.online_changepoint_detection(f2, hazard, nb.MultivariateT(dims=d))
    logR2, _ = log_run(f2, hazard, LogLikelihood(nb.MultivariateT(dims=d)))
    cmp2, _arr = compare_full(R2, logR2)
    ref2 = mp_reference_model(f2, HAZARD_LAM)
    r2 = compare_to_reference(logR2, ref2, 1e-6, 1e-9)
    T2 = len(f2)
    reach2 = np.arange(T2 + 1)[:, None] <= np.arange(T2 + 1)[None, :]
    zero_where_ref_positive = int((reach2 & (R2 == 0) & np.isfinite(ref2["logR"]))[:, 1:].sum())
    m_native2, cps_native2 = m_and_cps(R2)
    f2_checks = {
        "fixture hợp lệ: bản gốc có trạng thái bằng 0 trong khi tham chiếu dương": zero_where_ref_positive > 0,
        "bản gốc hữu hạn (không NaN)": bool(np.isfinite(R2).all()),
        "bản miền log hữu hạn ở mọi trạng thái đạt được": cmp2["log_domain_nonfinite_reachable"] == 0 and cmp2["log_domain_nan"] == 0,
        "tham chiếu: |logR_log - log R_tc| <= 1e-6 + 1e-9|log R_tc|": r2["within_tolerance"],
        "tham chiếu: MAP và CP trùng": r2["m_equal_where_reference_gap_clear"] and r2["cp_equal"],
        "chuẩn hóa: |logsumexp mỗi cột| <= 1e-12": cmp2["log_normalization_abs_max"] <= 1e-12,
    }
    result["F2"] = {"T": T2, "d": d, "native_zero_states_where_reference_positive": zero_where_ref_positive,
                    "native_vs_log": {k: v for k, v in cmp2.items() if k != "m_difference_detail"}, "reference": r2,
                    "native_m_equal_reference": bool(np.array_equal(m_native2, ref2["m"])), "native_cp_equal_reference": cps_native2 == ref2["cps"],
                    "reference_min_log_mass": float(np.min(ref2["logR"][reach2])), "checks": f2_checks, "pass": all(f2_checks.values())}

    # ---- F3: đối chứng dương cho phép toán (bảng mật độ đặt sẵn) ----
    T3 = len(f3)
    dummy = np.zeros((T3, 1))
    with np.errstate(all="ignore"):
        R3, _ = nb.online_changepoint_detection(dummy, hazard, ScriptedLikelihood(f3))
    logR3, _ = log_run(dummy, hazard, ScriptedLikelihood(f3))
    ref3 = mp_reference_scripted(f3, HAZARD_LAM)
    r3 = compare_to_reference(logR3, ref3, 1e-9, 1e-12)
    m_native3, cps_native3 = m_and_cps(R3)
    cmp3, _arr = compare_full(R3, logR3)
    f3_checks = {
        "bản gốc khác tham chiếu về MAP ở ít nhất một bước": not np.array_equal(m_native3, ref3["m"]),
        "bản gốc khác tham chiếu về CP": cps_native3 != ref3["cps"],
        "bản miền log trùng tham chiếu về MAP ở mọi bước": r3["m_equal_all"],
        "bản miền log trùng tham chiếu về CP": r3["cp_equal"],
        "tham chiếu: |logR_log - log R_tc| <= 1e-9 + 1e-12|log R_tc|": r3["within_tolerance"],
        "phép so toàn chuỗi xếp các chỗ khác vào lớp underflow": cmp3["m_differences"] > 0 and cmp3["m_difference_classes"]["underflow"] == cmp3["m_differences"],
    }
    result["F3"] = {"T": T3, "m_native": [int(v) for v in m_native3], "m_log": [int(v) for v in m_and_cps(logR3)[0]], "m_reference": [int(v) for v in ref3["m"]],
                    "cp_native": [int(i) for i in cps_native3], "cp_log": r3["cps"], "cp_reference": r3["cps_reference"], "reference": r3,
                    "native_vs_log": {k: v for k, v in cmp3.items() if k != "m_difference_detail"},
                    "m_difference_detail": cmp3["m_difference_detail"], "checks": f3_checks, "pass": all(f3_checks.values())}
    result["pass"] = bool(result["F1"]["pass"] and result["F2"]["pass"] and result["F3"]["pass"])
    result["wall_s"] = round(time.perf_counter() - began, 3)
    result["rss_bytes"] = rss()
    return result


def environment(bocpd_sha, baro_root):
    return {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__, "platform": platform.platform(), "machine": platform.node(),
            "cpu_count": os.cpu_count(), "threads_env": {k: os.environ.get(k) for k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
            "PYTHONPATH": os.environ.get("PYTHONPATH"), "argv": sys.argv, "bocpd_sha256": bocpd_sha, "baro_root": str(baro_root),
            "self_sha256": sha(__file__), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def main():
    mode = sys.argv[1]
    if mode == "fixtures":
        out, baro_root = Path(sys.argv[2]), sys.argv[3]
        out.mkdir(parents=True, exist_ok=False)
        nb, bocpd_sha = load_native(baro_root)
        (out / "environment.json").write_text(json.dumps(environment(bocpd_sha, baro_root), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        result = run_fixtures(out, nb, bocpd_sha)
        (out / "fixtures.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for name in ("F1", "F2", "F3"):
            print(name, "PASS" if result[name]["pass"] else "FAIL", json.dumps(result[name]["checks"], ensure_ascii=False), flush=True)
        print("FIXTURES", "PASS" if result["pass"] else "FAIL", result["wall_s"], "s", flush=True)
        raise SystemExit(0 if result["pass"] else 1)

    if mode == "determinism":
        npz_path, out_json, baro_root = Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
        nb, bocpd_sha = load_native(baro_root)
        z = np.load(npz_path, allow_pickle=False)
        X = z["X"]
        T, d = X.shape
        t0 = time.perf_counter()
        nat = nb.MultivariateT(dims=d)
        stored_pdf = z["predictive_density"]
        first_pdf_diff, pdf_bit_equal_rows, pdf_rel_max = None, 0, 0.0
        R = np.zeros((T + 1, T + 1))
        R[0, 0] = 1
        hazard = partial(nb.constant_hazard, HAZARD_LAM)
        for t, x in enumerate(X):                      # chép đúng vòng lặp gốc để soi density từng bước
            predprobs = nat.pdf(x)
            row = stored_pdf[t, : t + 1]
            if np.array_equal(predprobs, row):
                pdf_bit_equal_rows += 1
            else:
                if first_pdf_diff is None:
                    j = int(np.flatnonzero(predprobs != row)[0])
                    first_pdf_diff = {"step": int(t), "run_length": j, "now": float(predprobs[j]), "stored": float(row[j])}
                ok = row > 0
                pdf_rel_max = max(pdf_rel_max, float(np.max(np.abs(predprobs[ok] - row[ok]) / row[ok])))
            H = hazard(np.array(range(t + 1)))
            R[1:t + 2, t + 1] = R[0:t + 1, t] * predprobs * (1 - H)
            R[0, t + 1] = np.sum(R[0:t + 1, t] * predprobs * H)
            R[:, t + 1] = R[:, t + 1] / np.sum(R[:, t + 1])
            nat.update_theta(x, t=t)
        m, cps = m_and_cps(R)
        res = {"schema": "T034-E2-determinism-v1", "npz": str(npz_path), "npz_sha256": sha(npz_path), "T": int(T), "d": int(d),
               "environment": environment(bocpd_sha, baro_root), "wall_s": round(time.perf_counter() - t0, 3),
               "pdf_rows_bit_equal_stored": pdf_bit_equal_rows, "pdf_rows": int(T), "pdf_first_difference": first_pdf_diff,
               "pdf_relative_difference_max": pdf_rel_max,
               "R_bit_equal_stored": bool(np.array_equal(R, z["R"])), "R_bit_equal_fraction": float((R == z["R"]).mean()),
               "m_equal_stored": bool(np.array_equal(m, z["m"])), "R_sha256": hashlib.sha256(np.ascontiguousarray(R).tobytes()).hexdigest()}
        try:
            from threadpoolctl import threadpool_info
            res["threadpools"] = threadpool_info()
        except Exception as exc:                        # pragma: no cover
            res["threadpools"] = repr(exc)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in res.items() if k not in ("environment", "threadpools")}, ensure_ascii=False), flush=True)
        return

    assert mode == "chain"
    npz_path, out, label, baro_root = Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
    lineage_path = Path(sys.argv[6]) if len(sys.argv) > 6 else None
    out.mkdir(parents=True, exist_ok=True)
    nb, bocpd_sha = load_native(baro_root)
    hazard = partial(nb.constant_hazard, HAZARD_LAM)
    began_all = time.perf_counter()
    z = np.load(npz_path, allow_pickle=False)
    X, times = z["X"], z["times"]
    T, d = X.shape
    progress_path = out / f"{label}--progress.jsonl"

    def note(**kw):
        kw.update(utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), elapsed_s=round(time.perf_counter() - began_all, 3), rss_bytes=rss())
        with progress_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(kw, ensure_ascii=False) + "\n")
        print(label, json.dumps(kw, ensure_ascii=False), flush=True)

    env = environment(bocpd_sha, baro_root)
    env.update(npz=str(npz_path), npz_sha256=sha(npz_path), T=int(T), d=int(d))
    (out / f"{label}--environment.json").write_text(json.dumps(env, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    note(stage="start", T=int(T), d=int(d), npz_sha256=env["npz_sha256"])

    # ---- native sham: mã gốc, lớp con chỉ đếm bước để ghi tiến độ, không đổi phép tính ----
    class Counted(nb.MultivariateT):
        def update_theta(self, data, **kwargs):
            super().update_theta(data, **kwargs)
            step = kwargs.get("t", -1)
            if step % 100 == 0 or step == T - 1:
                note(stage="sham", step=int(step))

    t0 = time.perf_counter()
    R, maxes = nb.online_changepoint_detection(X, hazard, Counted(dims=d))
    sham_s = time.perf_counter() - t0
    R_stored, m_stored, cp_stored = z["R"], z["m"], z["CP_flags"]
    m_sham, cps_sham = m_and_cps(R)
    flags_sham = np.zeros(T, dtype=bool)
    flags_sham[cps_sham] = True
    normal = R_stored >= NORMAL_ZONE
    rel = np.abs(R[normal] - R_stored[normal]) / R_stored[normal]
    finite_both = np.isfinite(R) & np.isfinite(R_stored)
    sham = {"m_equal_stored": bool(np.array_equal(m_sham, m_stored)), "cp_flags_equal_stored": bool(np.array_equal(flags_sham, cp_stored)),
            "maxes_equal_stored": bool(np.array_equal(maxes, z["maxes"])), "R_bit_equal_stored": bool(np.array_equal(R, R_stored)),
            "R_bit_equal_fraction": float((R == R_stored).mean()), "R_relative_error_max_normal_zone": float(rel.max()) if rel.size else 0.0,
            "R_abs_error_max": float(np.abs(R[finite_both] - R_stored[finite_both]).max()), "R_all_finite": bool(np.isfinite(R).all()),
            "cp_indices": [int(i) for i in cps_sham], "cp_indices_stored": [int(i) for i in np.flatnonzero(cp_stored)], "wall_s": round(sham_s, 3)}
    dipped_stored = lineage_dipped(R_stored) | lineage_dipped(R)
    clean = normal & ~dipped_stored
    dirty = normal & dipped_stored
    rel_all = np.zeros_like(R)
    rel_all[normal] = np.abs(R[normal] - R_stored[normal]) / R_stored[normal]
    sham["R_relative_error_max_lineage_never_subnormal"] = float(rel_all[clean].max()) if clean.any() else 0.0
    sham["R_relative_error_max_lineage_was_subnormal"] = float(rel_all[dirty].max()) if dirty.any() else 0.0
    sham["normal_zone_states_lineage_never_subnormal"] = int(clean.sum())
    sham["normal_zone_states_lineage_was_subnormal"] = int(dirty.sum())
    # tiêu chí đã khai trong thiết kế (giữ nguyên): m, CP trùng tuyệt đối; R lệch tương đối <= 1e-9 trên mọi phần tử >= 1e-290
    sham["pass"] = bool(sham["m_equal_stored"] and sham["cp_flags_equal_stored"] and sham["R_relative_error_max_normal_zone"] <= 1e-9 and sham["R_all_finite"])
    # báo riêng (Mục nối 2, sau khi đã thấy lượt e2-001): phần bắt buộc m/CP; và tiêu chí R chỉ trên dòng dõi chưa từng dưới chuẩn hóa
    sham["pass_m_cp_exact"] = bool(sham["m_equal_stored"] and sham["cp_flags_equal_stored"] and sham["R_all_finite"])
    sham["pass_R_1e-9_lineage_never_subnormal"] = bool(sham["R_relative_error_max_lineage_never_subnormal"] <= 1e-9)
    note(stage="sham_done", **{k: v for k, v in sham.items() if k not in ("cp_indices", "cp_indices_stored")})

    # ---- miền log ----
    lik = LogLikelihood(nb.MultivariateT(dims=d))
    first_logpdf_check = {}

    def tick(step):
        if step % 100 == 0 or step == T - 1:
            note(stage="log", step=int(step))

    t0 = time.perf_counter()
    logR, log_norm = log_run(X, hazard, lik, tick)
    log_s = time.perf_counter() - t0
    # mật độ: so logpdf dùng trong lượt log với density đã lưu của bản gốc, tại vài bước (chạy lại riêng để không giữ cả bảng)
    pred = z["predictive_density"]
    probe = LogLikelihood(nb.MultivariateT(dims=d))
    dens_abs_max, dens_bit_equal, dens_checked = 0.0, True, 0
    for step, x in enumerate(X[: min(T, 200)]):
        lp = probe.logpdf(x)
        stored = pred[step, : step + 1]
        e = np.exp(lp)
        dens_bit_equal &= bool(np.array_equal(e, stored))
        ok = stored > 0
        dens_abs_max = max(dens_abs_max, float(np.max(np.abs(lp[ok] - np.log(stored[ok])))))
        dens_checked += int(ok.sum())
        probe.update_theta(x, t=step)
    first_logpdf_check = {"steps": int(min(T, 200)), "values": dens_checked, "exp_logpdf_bit_equal_stored_pdf": dens_bit_equal,
                          "logpdf_abs_error_max_vs_stored": dens_abs_max}
    stored_pdf_zero = int((pred[np.tril_indices(T)] == 0).sum())
    slices = set()
    lineage_checks = []
    lineage = None
    if lineage_path and lineage_path.is_file():
        lineage = json.loads(lineage_path.read_text(encoding="utf-8"))
        case_id = label.split("--")[0]
        branch = label.split("--")[1]
        for c in lineage["cases"]:
            if c["opaque_id"] != case_id:
                continue
            idx = c["index"]
            slices.update([idx, idx + 1])
            for ln in c[branch + "_lineages"]:
                lineage_checks.append({"what": "parent", "column": idx, "run_length": ln["parent"], "old_frozen_normalizer_log": ln["log_parent_R_frozen_normalizer_lineage"],
                                       "native_R_old": ln["native_parent_R"]})
                fz = ln.get("first_native_zero")
                if fz:
                    slices.update([fz["index"], fz["index"] + 1])
                    lineage_checks.append({"what": "first_zero_child", "column": fz["index"] + 1, "run_length": fz["parent"] + 1,
                                           "old_frozen_normalizer_log": fz["log_child_frozen_normalizer_lineage"], "native_R_old": fz["native_child_R"]})
    result, arrays = compare_full(R, logR, times, sorted(slices))
    for row in lineage_checks:
        t, r = row["column"], row["run_length"]
        if t <= T and r <= t:
            row["log_domain_value"] = float(logR[r, t])
            row["native_R_now"] = float(R[r, t])
            row["difference"] = float(logR[r, t] - row["old_frozen_normalizer_log"])
            row["map_log_value_same_column"] = float(logR[: t + 1, t].max())
            row["distance_to_map_log"] = float(logR[: t + 1, t].max() - logR[r, t])
    param_state_equal = None
    summary = {"schema": "T034-E2-chain-v1", "label": label, "npz": str(npz_path), "npz_sha256": env["npz_sha256"], "T": int(T), "d": int(d),
               "columns": [str(c) for c in z["columns"]], "hazard": 1 / HAZARD_LAM, "sham": sham, "log_wall_s": round(log_s, 3),
               "density_check": first_logpdf_check, "stored_pdf_exact_zero_values": stored_pdf_zero,
               "comparison_native_vs_log": result, "lineage_cross_check": lineage_checks,
               "interpretable": bool(sham["pass"]), "interpretable_by_m_cp_exact": bool(sham["pass_m_cp_exact"]), "wall_s_total": round(time.perf_counter() - began_all, 3), "rss_peak_observed_bytes": rss()}
    arrays.update(m_stored=m_stored, cp_flags_stored=cp_stored, times=times, log_normalizer=log_norm)
    np.savez_compressed(out / f"{label}--compact.npz", **arrays)
    summary["compact_npz_sha256"] = sha(out / f"{label}--compact.npz")
    summary["compact_npz_bytes"] = (out / f"{label}--compact.npz").stat().st_size
    (out / f"{label}--summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    note(stage="done", sham_pass=sham["pass"], m_equal=result["m_equal_all"], cp_equal=result["cp_equal"], zeros=result["native_exact_zero_states"],
         lost_mass_log_max=result["lost_mass_log_max"], sham_s=round(sham_s, 1), log_s=round(log_s, 1))


if __name__ == "__main__":
    main()
