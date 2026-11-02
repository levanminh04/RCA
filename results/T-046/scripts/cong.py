"""T-046: ứng viên cổng G1, G3 cho đơn vị phân vị (SPEC T-046 mục Ứng viên; Đặc tả bổ sung A3). Chỉ dùng trong
results/T-046 trước điểm dừng D-2; không sửa src.

- Chuỗi 1 giây canh theo t: N lùi từ t (ô j = [t − (j+1) s, t − j s)), A tiến từ t (ô j = [t + j s, t + (j+1) s)).
  Giá trị ô là trung bình mẫu trong ô; ô rỗng là thiếu (A3 điểm 1).
- ρ(k), k = 1…60, trên các cặp ô của N cùng có giá trị cách k giây; trung bình, phương sai (chia cho số ô) trên mọi ô
  có giá trị; cần ít nhất 10 cặp. b = k nhỏ nhất có ρ(k) xác định và < 0,2, chặn về [5; 60]; không có thì 60.
  N dưới 10 ô có giá trị hoặc phương sai 0: rơi về G0 (A3 điểm 2).
- Khối dài b canh theo t, chỉ giữ khối nằm trọn trong phía 300 giây, bỏ khối rỗng; cần ít nhất 5 khối có mẫu mỗi
  phía, thiếu thì rơi về G0 (A3 điểm 3).
- G1: `e4.p_cong` trên trung bình khối (A3 điểm 4).
- G3: T = r_d(A) − r_d(N) trên mẫu gốc của khối được giữ; h, l tính lại từ phần N của từng cách chia (`e4.nguong`);
  so T* ≥ T bằng số nguyên chính xác. Duyệt hết khi C(nN + nA, nA) ≤ B; ngược lại B hoán vị ngẫu nhiên,
  p = (1 + #{T* ≥ T}) / (B + 1); seed = 20261101 + int(sha256('mã|hướng')[:16], 16) (A3 điểm 5).
Thời gian tính bằng ns (số nguyên), như chuỗi M1.
"""
import hashlib
import itertools
import math

import numpy as np

from m1 import e4

NS = 10 ** 9
W = 300            # độ dài mỗi phía (giây)
K_MAX = 60         # độ trễ lớn nhất và trần của b
B_MIN = 5          # sàn của b
NGUONG_RHO = 0.2
CAP_TOI_THIEU = 10  # số cặp tối thiểu cho ρ(k); cũng là số ô có giá trị tối thiểu của N
KHOI_TOI_THIEU = 5
B_HOAN_VI = 2000
SEED_GOC = 20261101


def o_1s(moc_ns, gia_tri, t_ns, phia):
    """{chỉ số ô: trung bình} của một phía. moc_ns: mốc mẫu (int ns)."""
    tong, dem = {}, {}
    for x, v in zip(moc_ns, gia_tri):
        if phia == 'N':
            if x >= t_ns:
                raise ValueError('mẫu N có mốc >= t')
            j = (t_ns - x - 1) // NS
        else:
            if x < t_ns:
                raise ValueError('mẫu A có mốc < t')
            j = (x - t_ns) // NS
        if j >= W:
            continue
        tong[j] = tong.get(j, 0.0) + float(v)
        dem[j] = dem.get(j, 0) + 1
    return {j: tong[j] / dem[j] for j in tong}


def tu_tuong_quan(o):
    """ρ(k), k = 1…K_MAX trên ô có giá trị (dict chỉ số → giá trị); None khi không xác định. Trả (rho, ly_do)."""
    if len(o) < CAP_TOI_THIEU:
        return None, 'it_o'
    x = np.array(list(o.values()), float)
    m = float(x.mean())
    v = float(((x - m) ** 2).mean())
    if v <= 0:
        return None, 'phuong_sai_0'
    rho = {}
    for k in range(1, K_MAX + 1):
        cap = [(o[j] - m) * (o[j + k] - m) for j in o if (j + k) in o]
        rho[k] = (sum(cap) / len(cap)) / v if len(cap) >= CAP_TOI_THIEU else None
    return rho, None


def do_dai_khoi(rho):
    """b theo A3 điểm 2. Trả (b, cham_tran): cham_tran khi không có k nào có ρ(k) < 0,2 (b = 60) hoặc k = 60."""
    for k in range(1, K_MAX + 1):
        r = rho.get(k)
        if r is not None and r < NGUONG_RHO:
            b = min(max(k, B_MIN), K_MAX)
            return b, b == K_MAX
    return K_MAX, True


def chia_khoi(moc_ns, gia_tri, t_ns, b, phia, bien=None):
    """{chỉ số khối: [giá trị]} của khối nằm trọn trong phía, bỏ khối rỗng. bien (sửa R1, SPEC A3 điểm 3): mốc xa nhất
    của phía, ns (N: max(t − 300, H₀); A: min(t + 300, H₁)); None: 300 giây (bản cũ)."""
    bns = b * NS
    if bien is None:
        so_khoi = W // b
    else:
        do_dai = (t_ns - bien) if phia == 'N' else (bien - t_ns)
        so_khoi = max(0, do_dai // bns)
    out = {}
    for x, v in zip(moc_ns, gia_tri):
        j = (t_ns - x - 1) // bns if phia == 'N' else (x - t_ns) // bns
        if 0 <= j < so_khoi:
            out.setdefault(j, []).append(float(v))
    return out


def chuan_bi_khoi(N, mocN, A, mocA, t_ns, bien_N=None, bien_A=None):
    """Tính b trên N và chia khối hai phía. Trả dict có 'roi_G0' (None hoặc lý do), b, cham_tran, khối."""
    oN = o_1s(mocN, N, t_ns, 'N')
    rho, ly_do = tu_tuong_quan(oN)
    if rho is None:
        return {'roi_G0': ly_do, 'b': None, 'cham_tran': None, 'so_o_N': len(oN), 'rho1': None}
    b, cham_tran = do_dai_khoi(rho)
    kN = chia_khoi(mocN, N, t_ns, b, 'N', bien_N)
    kA = chia_khoi(mocA, A, t_ns, b, 'A', bien_A)
    out = {'roi_G0': None, 'b': b, 'cham_tran': cham_tran, 'so_o_N': len(oN), 'so_khoi_N': len(kN),
           'so_khoi_A': len(kA), 'khoi_N': kN, 'khoi_A': kA,
           'rho_b': rho.get(b), 'rho1': rho.get(1)}
    if len(kN) < KHOI_TOI_THIEU or len(kA) < KHOI_TOI_THIEU:
        out['roi_G0'] = 'it_khoi'
    return out


def p_G0(N, A, huong, ts):
    return e4.p_cong(A, N, huong, int(ts.get('n_exact_max', 100)))


def p_G1(kb, huong, ts):
    """G1 trên trung bình khối (kb từ chuan_bi_khoi, roi_G0 là None)."""
    mN = [float(np.mean(kb['khoi_N'][j])) for j in sorted(kb['khoi_N'])]
    mA = [float(np.mean(kb['khoi_A'][j])) for j in sorted(kb['khoi_A'])]
    return e4.p_cong(mA, mN, huong, int(ts.get('n_exact_max', 100)))


def seed_cua(ma, huong):
    h = hashlib.sha256(f'{ma}|{huong}'.encode('utf-8')).hexdigest()
    return SEED_GOC + int(h[:16], 16)


def _nguong_hang(Xs, n, q):
    """Phân vị type 7 theo từng hàng, đúng từng phép tính của numpy 1.26 `percentile(method='linear')`
    (`numpy/lib/function_base.py`: chỉ số ảo (n − 1)·q; chỉ số >= n − 1 lấy phần tử cuối; nội suy `_lerp` đổi công
    thức khi gamma >= 0,5). Xs đã sắp tăng, NaN ở cuối; n là số phần tử hữu hạn mỗi hàng (>= 1). q là phân số (0,95),
    lấy như numpy nhận từ e4.nguong: (100·q)/100."""
    qq = np.true_divide(100 * q, 100)
    vi = (n - 1) * qq
    prev = np.floor(vi)
    gamma = vi - prev
    lo = prev.astype(np.int64)
    hi = lo + 1
    tren = vi >= n - 1
    lo = np.where(tren, n - 1, lo)
    hi = np.where(tren, n - 1, hi)
    r = np.arange(Xs.shape[0])
    a = Xs[r, lo]
    c = Xs[r, hi]
    d = c - a
    y = a + d * gamma
    return np.where(gamma >= 0.5, c - d * (1 - gamma), y)


def p_G3(kb, huong, ts, ma, B=B_HOAN_VI, khoi_lo=None, tra_dem=False):
    """G3 (A3 điểm 5). kb: kết quả chuan_bi_khoi (roi_G0 None). Trả (p, cach, chi_tiet).
    khoi_lo: số hoán vị mỗi lô (giới hạn bộ nhớ)."""
    eps = ts['epsilon']
    qh, ql = ts.get('q_hi', 0.95), ts.get('q_lo', 0.05)
    blocks = [kb['khoi_N'][j] for j in sorted(kb['khoi_N'])] + [kb['khoi_A'][j] for j in sorted(kb['khoi_A'])]
    nbN, nbA = len(kb['khoi_N']), len(kb['khoi_A'])
    nb = nbN + nbA
    v = np.concatenate([np.asarray(x, float) for x in blocks])
    bid = np.concatenate([np.full(len(x), i, np.int64) for i, x in enumerate(blocks)])
    sz = np.array([len(x) for x in blocks], np.int64)

    def thong_ke(inA):
        """inA: (R, nb) bool. Trả (cA, nA, cN, nN) theo hàng (int64)."""
        R = inA.shape[0]
        mA = inA[:, bid]                               # (R, M)
        nA = (inA * sz).sum(1)
        nN = v.size - nA
        XN = np.where(mA, np.nan, v)                   # phần N của từng cách chia
        XN.sort(axis=1)                                # NaN ở cuối
        if huong == 'len':
            q = _nguong_hang(XN, nN, qh)
            h = np.minimum(q + eps * np.abs(q), e4.MAX_THUC)
            vuot = v[None, :] > h[:, None]
        else:
            q = _nguong_hang(XN, nN, ql)
            l = np.maximum(q - eps * np.abs(q), -e4.MAX_THUC)
            vuot = v[None, :] < l[:, None]
        cA = (vuot & mA).sum(1)
        cN = (vuot & ~mA).sum(1)
        return cA.astype(np.int64), nA.astype(np.int64), cN.astype(np.int64), nN.astype(np.int64)

    goc = np.zeros((1, nb), bool)
    goc[0, nbN:] = True
    cA0, nA0, cN0, nN0 = (int(x[0]) for x in thong_ke(goc))
    # T = cA/nA − cN/nN; so T* >= T bằng nhân chéo số nguyên (mẫu số dương)
    T0_tu, T0_mau = cA0 * nN0 - cN0 * nA0, nA0 * nN0
    so_cach = math.comb(nb, nbA)
    khoi_lo = khoi_lo or max(1, min(B, int(4e6 // max(v.size, 1))))
    if so_cach <= B:
        dem = 0
        tong = 0
        lo_ = []
        for comb in itertools.combinations(range(nb), nbA):
            row = np.zeros(nb, bool)
            row[list(comb)] = True
            lo_.append(row)
            if len(lo_) >= khoi_lo:
                d, n = _dem_vuot(thong_ke, np.array(lo_), T0_tu, T0_mau)
                dem += d
                tong += n
                lo_ = []
        if lo_:
            d, n = _dem_vuot(thong_ke, np.array(lo_), T0_tu, T0_mau)
            dem += d
            tong += n
        p = dem / tong
        ct = {'cach': 'duyet_het', 'so_cach': so_cach, 'dem_vuot': dem}
    else:
        rng = np.random.default_rng(seed_cua(ma, huong))
        dem = 0
        con = B
        while con > 0:
            r = min(con, khoi_lo)
            keys = rng.random((r, nb))
            idx = np.argsort(keys, axis=1)[:, :nbA]     # nbA khối ngẫu nhiên cho A, giữ số khối mỗi phía
            inA = np.zeros((r, nb), bool)
            np.put_along_axis(inA, idx, True, axis=1)
            d, _ = _dem_vuot(thong_ke, inA, T0_tu, T0_mau)
            dem += d
            con -= r
        p = (1 + dem) / (B + 1)
        ct = {'cach': 'ngau_nhien', 'so_cach': so_cach, 'dem_vuot': dem, 'B': B}
    ct.update({'T': [cA0, nA0, cN0, nN0]})
    return float(p), 'G3', ct


def _dem_vuot(thong_ke, inA, T0_tu, T0_mau):
    cA, nA, cN, nN = thong_ke(inA)
    tu = cA * nN - cN * nA
    mau = nA * nN
    # tu/mau >= T0_tu/T0_mau  <=>  tu·T0_mau >= T0_tu·mau (mẫu số dương); dùng số nguyên Python để tránh tràn
    dem = sum(1 for a, b in zip(tu.tolist(), mau.tolist()) if a * T0_mau >= T0_tu * b)
    return dem, len(tu)


def p_theo_cong(cong, N, mocN, A, mocA, t_ns, huong, ts, ma, kb=None):
    """p của một phép theo cổng 'G0' | 'G1' | 'G3'. Trả dict: p, cach, roi_G0, b, cham_tran, so_khoi_N, so_khoi_A,
    chi_tiet (G3)."""
    if cong == 'G0':
        p, cach = p_G0(N, A, huong, ts)
        return {'p': p, 'cach': cach}
    if kb is None:
        kb = chuan_bi_khoi(N, mocN, A, mocA, t_ns)
    meta = {k: kb.get(k) for k in ('roi_G0', 'b', 'cham_tran', 'so_o_N', 'so_khoi_N', 'so_khoi_A', 'rho_b')}
    if kb['roi_G0']:
        p, cach = p_G0(N, A, huong, ts)
        return dict(meta, p=p, cach='G0:' + cach)
    if cong == 'G1':
        p, cach = p_G1(kb, huong, ts)
        return dict(meta, p=p, cach='G1:' + cach)
    p, cach, ct = p_G3(kb, huong, ts, ma)
    return dict(meta, p=p, cach=cach, chi_tiet=ct)


# ---------------------------------------------------------------- G4 (bản 3, B1): làm trắng AR(1) cho đơn vị metric

G4_MIN_DU_N = 30
G4_MIN_DU_A = 5


def phan_du_AR1(oN, oA, phi):
    """Phần dư r_s = x_s − φ·x_{s−1} trên chuỗi 1 giây (dict chỉ số ô → giá trị) của hai phía. Ô N j là giây
    [t − (j+1), t − j); ô liền trước của ô N j là ô N j+1; ô liền trước của ô A k là ô A k−1, của ô A 0 là ô N 0.
    φ = 0: phần dư là giá trị, dùng mọi ô."""
    if phi == 0:
        return [oN[j] for j in sorted(oN, reverse=True)], [oA[k] for k in sorted(oA)]
    rN = [oN[j] - phi * oN[j + 1] for j in sorted(oN, reverse=True) if (j + 1) in oN]
    rA = []
    for k in sorted(oA):
        truoc = oA.get(k - 1) if k > 0 else oN.get(0)
        if truoc is not None:
            rA.append(oA[k] - phi * truoc)
    return rN, rA


def p_G4_metric(N, mocN, A, mocA, t_ns, huong, ts):
    """G4 cho đơn vị metric. Trả dict p, cach, phi, so_du_N, so_du_A, roi_G0."""
    oN = o_1s(mocN, N, t_ns, 'N')
    oA = o_1s(mocA, A, t_ns, 'A')
    rho, ly_do = tu_tuong_quan(oN)
    if rho is None or rho.get(1) is None:
        p, cach = p_G0(N, A, huong, ts)
        return {'p': p, 'cach': 'G0:' + cach, 'roi_G0': ly_do or 'rho1', 'phi': None}
    phi = max(0.0, rho[1])
    rN, rA = phan_du_AR1(oN, oA, phi)
    if len(rN) < G4_MIN_DU_N or len(rA) < G4_MIN_DU_A:
        p, cach = p_G0(N, A, huong, ts)
        return {'p': p, 'cach': 'G0:' + cach, 'roi_G0': 'it_phan_du', 'phi': phi, 'so_du_N': len(rN),
                'so_du_A': len(rA)}
    p, cach = e4.p_cong(rA, rN, huong, int(ts.get('n_exact_max', 100)))
    return {'p': p, 'cach': 'G4:' + cach, 'roi_G0': None, 'phi': phi, 'so_du_N': len(rN), 'so_du_A': len(rA)}


# ---------------------------------------------------------------- D1 (bản 3, B2): nhị thức có hiệu chỉnh phân tán

O_DEM_S = 10
O_DEM_MIN = 3


def he_so_phan_tan(moc_N, h0_ns, t_ns):
    """φ̂_d = max(1; s²/ȳ) trên ô 10 giây trọn của [h0, t), canh lùi từ t. Trả (phi, so_o)."""
    if h0_ns is None or h0_ns >= t_ns:
        return 1.0, 0
    w = O_DEM_S * NS
    so_o = (t_ns - h0_ns) // w
    if so_o < O_DEM_MIN:
        return 1.0, int(so_o)
    dem = [0] * so_o
    for x in moc_N:
        if x >= t_ns:
            raise ValueError('sự kiện N có mốc >= t')
        j = (t_ns - x - 1) // w
        if j < so_o:
            dem[j] += 1
    y = np.array(dem, float)
    m = float(y.mean())
    if m <= 0:
        return 1.0, int(so_o)
    s2 = float(y.var(ddof=1))
    return max(1.0, s2 / m), int(so_o)


def p_D1(n_N, n_A, T_N, T_A, phi, huong):
    """Đuôi nhị thức mở rộng cho số đếm chia φ (B2). Khi phi = 1 trùng p_nhi_thuc của e4."""
    from scipy.special import betainc
    p0 = T_A / (T_N + T_A)
    k = n_A / phi
    n = (n_N + n_A) / phi
    if huong == 'len':
        return 1.0 if n_A <= 0 else float(betainc(k, n - k + 1, p0))
    # P(X <= k) = I_{1−p0}(n − k, k + 1): tránh trừ hai số gần nhau khi p nhỏ
    return 1.0 if n - k <= 0 else float(betainc(n - k, k + 1, 1 - p0))
