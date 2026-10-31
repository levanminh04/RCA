"""E4 — thống kê chung, cố định theo D24 (SPEC T-043 B1.3, B1.8; đặc tả v1 §4).

Đơn vị phân vị: ngưỡng Q0.95, Q0.05 (type 7), biên ±ε|q|, tỷ lệ vượt, cổng một phía tổng hạng (chính xác có điều kiện
khi n_N + n_A <= 100, theo mã B1.8; xấp xỉ có hiệu chỉnh trùng và liên tục khi lớn hơn), e_d = max(0, r_d(A) − r_d(N))
khi qua cổng. Đơn vị đếm: nhị thức chính xác với p0 = T_A/(T_N + T_A), λ = n_N·T_A/T_N; NEW_OP, STOPPED.

Diễn giải (dinh-chinh-cai-dat.md Phần II): cổng qua khi p < α (chặt), như KS-16 pha 2 và E3b ở dinh-nghia-pha2.json.
Điểm e_d tính chính xác (phân số từ số đếm nguyên; λ từ T đã cho) rồi mới đổi sang số thực một lần; kết quả chấm kèm
`e_<hướng>_q` (Fraction) để xếp hạng so khóa chính xác (dinh-chinh-cai-dat.md C6, S20). T4c tính log từ phân số, không tràn.
"""
import math
from fractions import Fraction
from math import comb

import numpy as np
from scipy.stats import binom, mannwhitneyu, rankdata

EPS_MACH = np.finfo(np.float64).eps
MAX_THUC = float(np.finfo(np.float64).max)


def exact_tied_greater(A, N):
    """P(W_A >= w_obs) chính xác có điều kiện; W = tổng hạng trung bình của A; giá trị trùng xử lý theo nhóm.
    Chép nguyên mã SPEC T-043 B1.8."""
    A = np.asarray(A, float); N = np.asarray(N, float)
    x = np.r_[A, N]; nA = len(A)
    vals, counts = np.unique(x, return_counts=True)
    start = np.cumsum(np.r_[0, counts[:-1]])
    mid2 = (2 * start + counts + 1).astype(np.int64)        # 2 × hạng trung bình, là số nguyên
    Wmax = int((mid2 * counts).sum())
    dp = np.zeros((nA + 1, Wmax + 1)); dp[0, 0] = 1.0       # dp[k, w]: trọng số khi đã chọn k phần tử cho A
    for m, w in zip(counts, mid2):
        new = np.zeros_like(dp)
        for k in range(0, min(m, nA) + 1):
            c = float(comb(int(m), k))  # float trước khi nhân; số nguyên quá lớn làm mảng thành object
            if k == 0:
                new += dp * c
                continue
            new[k:, k * w:] += dp[:nA + 1 - k, :Wmax + 1 - k * w] * c
        dp = new
    wobs = int(round(2 * rankdata(x)[:nA].sum()))
    return dp[nA][wobs:].sum() / dp[nA].sum()


def p_cong(A, N, huong, n_exact_max=100):
    """p một phía. 'len': A lớn hơn N; 'xuong': A nhỏ hơn N (đuôi dưới của cùng phép, bằng phép 'len' trên −x)."""
    n = len(A) + len(N)
    if n <= n_exact_max:
        if huong == 'len':
            p = exact_tied_greater(A, N)
        else:
            p = exact_tied_greater([-a for a in A], [-x for x in N])
        return float(min(1.0, p)), 'chinh_xac'
    alt = 'greater' if huong == 'len' else 'less'
    p = mannwhitneyu(A, N, alternative=alt, method='asymptotic', use_continuity=True).pvalue
    return float(p), 'xap_xi'


class CacheCong:
    """Cache kết quả cổng theo khóa nội dung: (khóa đơn vị, mẫu N và A đã sắp, hướng, tham số E4) (B1.3).
    Khóa không chứa config_id hay cờ của thành phần phía sau."""

    def __init__(self):
        self._d = {}
        self.trung = 0
        self.moi = 0

    def p(self, khoa_don_vi, A, N, huong, ts):
        k = (khoa_don_vi, tuple(sorted(float(x) for x in N)), tuple(sorted(float(x) for x in A)), huong,
             tuple(sorted((a, float(b)) for a, b in ts.items())))
        if k in self._d:
            self.trung += 1
            return self._d[k]
        self.moi += 1
        kq = p_cong(A, N, huong, int(ts.get('n_exact_max', 100)))
        self._d[k] = kq
        return kq


def nguong(XN, ts):
    q_hi = float(np.percentile(XN, 100 * ts.get('q_hi', 0.95)))
    q_lo = float(np.percentile(XN, 100 * ts.get('q_lo', 0.05)))
    eps = ts['epsilon']
    # giá trị hữu hạn rất lớn: h, l tràn thành ±inf; chặn ở số thực lớn nhất (cùng kết quả so x > h, x < l)
    h = min(q_hi + eps * abs(q_hi), MAX_THUC)
    l = max(q_lo - eps * abs(q_lo), -MAX_THUC)
    return {'q_hi': q_hi, 'q_lo': q_lo, 'h': h, 'l': l}


def ty_le_vuot(X, h=None, l=None):
    r_len, r_xuong = ty_le_vuot_q(X, h, l)
    return (None if r_len is None else float(r_len)), (None if r_xuong is None else float(r_xuong))


def ty_le_vuot_q(X, h=None, l=None):
    """Tỷ lệ vượt chính xác (Fraction)."""
    n = len(X)
    r_len = Fraction(sum(1 for x in X if x > h), n) if h is not None else None
    r_xuong = Fraction(sum(1 for x in X if x < l), n) if l is not None else None
    return r_len, r_xuong


def cham_phan_vi(N, A, m, ts, huong_cham=('len',), cache=None, khoa_don_vi=None):
    """Chấm một đơn vị phân vị (B1.3). Trả trạng thái, ngưỡng, tỷ lệ vượt, p, e, F_raw theo từng hướng chấm."""
    XN = [float(x) for x in N if x is not None and math.isfinite(float(x))]
    XA = [float(x) for x in A if x is not None and math.isfinite(float(x))]
    out = {'n_N': len(XN), 'n_A': len(XA), 'loai': 'phan_vi'}
    if not XN:
        tt = 'NO_BASELINE' if XA else 'NO_DATA'
    elif not XA:
        tt = 'NO_A'
    elif len(XN) < m or len(XA) < m:
        tt = 'LOW_SUPPORT'
    else:
        tt = 'OK'
    out['trang_thai'] = tt
    out['hop_le'] = tt == 'OK'
    for d in ('len', 'xuong'):
        out[f'e_{d}'] = 0.0
        out[f'e_{d}_q'] = Fraction(0)
        out[f'F_raw_{d}'] = 0
        out[f'p_{d}'] = None
    if tt != 'OK':
        return out
    ng = nguong(XN, ts)
    out.update(ng)
    rA_len, rA_xuong = ty_le_vuot_q(XA, ng['h'], ng['l'])
    rN_len, rN_xuong = ty_le_vuot_q(XN, ng['h'], ng['l'])
    out.update({'r_len_A': float(rA_len), 'r_len_N': float(rN_len), 'r_xuong_A': float(rA_xuong),
                'r_xuong_N': float(rN_xuong)})
    alpha = ts['alpha']
    for d in huong_cham:
        if cache is not None:
            p, cach = cache.p(khoa_don_vi, XA, XN, d, ts)
        else:
            p, cach = p_cong(XA, XN, d, int(ts.get('n_exact_max', 100)))
        cheng = (rA_len - rN_len) if d == 'len' else (rA_xuong - rN_xuong)
        qua = p < alpha
        out[f'p_{d}'] = p
        out[f'cach_cong_{d}'] = cach
        out[f'sat_nguong_{d}'] = (cach == 'xap_xi' and abs(p - alpha) <= 0.002)
        e_q = max(Fraction(0), cheng)
        out[f'e_{d}_tho'] = float(e_q)
        out[f'F_raw_{d}'] = int(qua and cheng > 0)
        out[f'e_{d}_q'] = e_q if qua else Fraction(0)
        out[f'e_{d}'] = float(out[f'e_{d}_q'])
    return out


def p_nhi_thuc(n_A, n, p0, huong):
    if huong == 'len':
        return float(binom.sf(n_A - 1, n, p0)) if n_A > 0 else 1.0
    return float(binom.cdf(n_A, n, p0))


def cham_dem(n_N, n_A, T_N, T_A, ts, trang_thai_ep=None, huong_cham=('len', 'xuong')):
    """Chấm một đơn vị đếm (B1.3; đặc tả v1 §4). trang_thai_ep: NO_BASELINE/NO_A do quy tắc severity (B2 E3)."""
    out = {'n_N': n_N, 'n_A': n_A, 'T_N': T_N, 'T_A': T_A, 'loai': 'dem', 'lam': None}
    for d in ('len', 'xuong'):
        out[f'e_{d}'] = 0.0
        out[f'e_{d}_q'] = Fraction(0)
        out[f'e_{d}_tho'] = 0.0
        out[f'F_raw_{d}'] = 0
        out[f'p_{d}'] = None
    if trang_thai_ep:
        tt = trang_thai_ep
    elif not T_N or T_N <= 0:
        tt = 'NO_BASELINE'
    elif not T_A or T_A <= 0:
        tt = 'NO_A'
    elif n_N == 0 and n_A >= ts['count_min']:
        tt = 'OK'
    elif n_A == 0 and n_N >= ts['count_min']:
        tt = 'OK'
    elif n_N + n_A < ts['count_min']:
        tt = 'LOW_SUPPORT'
    else:
        tt = 'OK'
    out['trang_thai'] = tt
    out['hop_le'] = tt == 'OK'
    out['nhan'] = 'binh_thuong'
    if tt != 'OK':
        out['nhan'] = None
        return out
    n = n_N + n_A
    p0 = T_A / (T_N + T_A)
    lam = Fraction(n_N) * Fraction(T_A) / Fraction(T_N)  # chính xác theo T đã cho
    out['lam'] = float(lam)
    out['p0'] = p0
    alpha = ts['alpha']
    if n_N == 0 and n_A >= ts['count_min'] and 'len' in huong_cham:
        out.update({'nhan': 'NEW_OP', 'F_raw_len': 1, 'e_len': 1.0, 'e_len_q': Fraction(1), 'e_len_tho': 1.0,
                    'p_len': p_nhi_thuc(n_A, n, p0, 'len'), 'p_xuong': p_nhi_thuc(n_A, n, p0, 'xuong')})
        return out
    if n_A == 0 and n_N >= ts['count_min'] and 'xuong' in huong_cham:
        out.update({'nhan': 'STOPPED', 'F_raw_xuong': 1, 'e_xuong': 1.0, 'e_xuong_q': Fraction(1), 'e_xuong_tho': 1.0,
                    'p_len': p_nhi_thuc(n_A, n, p0, 'len'), 'p_xuong': p_nhi_thuc(n_A, n, p0, 'xuong')})
        return out
    e_len = max(Fraction(0), (n_A - lam) / max(n_A, 1))
    e_xuong = max(Fraction(0), (lam - n_A) / max(lam, 1))
    for d, e, cheng in (('len', e_len, n_A - lam), ('xuong', e_xuong, lam - n_A)):
        p = p_nhi_thuc(n_A, n, p0, d)
        out[f'p_{d}'] = p
        out[f'e_{d}_tho'] = float(e)
        qua = (d in huong_cham) and p < alpha and cheng > 0
        out[f'F_raw_{d}'] = int(qua)
        out[f'e_{d}_q'] = e if qua else Fraction(0)
        out[f'e_{d}'] = float(out[f'e_{d}_q'])
    if out['F_raw_len']:
        out['nhan'] = 'tang'
    elif out['F_raw_xuong']:
        out['nhan'] = 'giam'
    return out


def obs_dependent(nhan_theo_the_gioi):
    """OBS_DEPENDENT: đơn vị có nhãn khác nhau giữa ba thế giới (B1.3b)."""
    return len(set(nhan_theo_the_gioi.values())) > 1


def doi_quyet_dinh_khi_T_lech(n_N, n_A, T_N, T_A, ts, ty_le=0.01):
    """Đ5 (Q-209 mục 2): quyết định cổng (F_raw hai hướng) có đổi khi T_N hoặc T_A lệch ±ty_le không. Chỉ báo cáo."""
    def qd(tn, ta):
        k = cham_dem(n_N, n_A, tn, ta, ts)
        return (k['F_raw_len'], k['F_raw_xuong'])
    goc = qd(T_N, T_A)
    for fN in (1 - ty_le, 1.0, 1 + ty_le):
        for fA in (1 - ty_le, 1.0, 1 + ty_le):
            if qd(T_N * fN, T_A * fA) != goc:
                return True
    return False


def diem_z(N, A):
    """Nhánh z (T4b, chỉ báo cáo; SPEC B2 E4): s_lên = max(A − med_N)/c; c = IQR_N nếu IQR_N >= 10·ε_mach, ngược lại 1."""
    XN = np.asarray([float(x) for x in N], float)
    XA = np.asarray([float(x) for x in A], float)
    med = float(np.median(XN))
    iqr = float(np.percentile(XN, 75) - np.percentile(XN, 25))
    c = iqr if iqr >= 10 * EPS_MACH else 1.0
    zl = float(np.max(XA - med) / c)
    zx = float(np.max(med - XA) / c)
    return {'med_N': med, 'IQR': iqr, 'c': c, 'z_len': zl, 'z_xuong': zx,
            'huu_han': math.isfinite(zl) and math.isfinite(zx)}


def _log1p_q(x):
    """log(1 + x) với x là Fraction không âm (S21): log1p của x làm tròn một lần khi x biểu diễn được bằng số thực
    (x bằng nhau cho m bằng nhau); x quá lớn thì tính từ log của tử và mẫu nguyên, không tràn."""
    try:
        return math.log1p(float(x))
    except OverflowError:
        y = 1 + x
        return math.log(y.numerator) - math.log(y.denominator)


def _trung_vi_q(X):
    """Trung vị chính xác (Fraction) của các giá trị hữu hạn; như numpy.median nhưng không cộng số thực."""
    v = sorted(Fraction(float(x)) for x in X)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def m_T4c_phan_vi(N, A):
    """CĐ7: m = log(1 + |trung vị A − trung vị N| / max(|trung vị N|, r_u)); r_u là hiệu dương nhỏ nhất giữa hai giá trị
    khác nhau trong N ∪ A; mọi giá trị bằng nhau thì m = 0. Tính trên phân số nên hữu hạn với mọi đầu vào hữu hạn."""
    v = sorted(set(Fraction(float(x)) for x in list(N) + list(A)))
    if len(v) < 2:
        return 0.0
    r_u = min(b - a for a, b in zip(v, v[1:]))
    mN, mA = _trung_vi_q(N), _trung_vi_q(A)
    return _log1p_q(abs(mA - mN) / max(abs(mN), r_u))


def m_T4c_dem(n_N, n_A, T_N, T_A):
    """CĐ7: λ = n/T; m = log(1 + |λ_A − λ_N| / max(λ_N, r_u)), r_u = 1/T_N."""
    T_N, T_A = Fraction(T_N), Fraction(T_A)
    lN, lA = n_N / T_N, n_A / T_A
    return _log1p_q(abs(lA - lN) / max(lN, 1 / T_N))
