"""Cổng của chế độ mới (WHY-67; SPEC T-046 A3, B2): G3 cho đơn vị phân vị, hệ số phân tán của D1 cho đơn vị đếm.
Bật bằng `params.che_do`; chuỗi ở chế độ mặc định không gọi tệp này. Chép từ `results/T-046/scripts/cong.py`.

- Chuỗi 1 giây canh theo t: N lùi từ t (ô j = [t − (j+1) s, t − j s)), A tiến từ t (ô j = [t + j s, t + (j+1) s)).
  Giá trị ô là trung bình mẫu trong ô; ô rỗng là thiếu.
- ρ(k), k = 1…60, trên các cặp ô của N cùng có giá trị cách k giây; trung bình, phương sai (chia cho số ô) trên mọi ô
  có giá trị; cần ít nhất 10 cặp. b = k nhỏ nhất có ρ(k) xác định và < 0,2, chặn về [5; 60]; không có thì 60.
  N dưới 10 ô có giá trị hoặc phương sai 0: rơi về G0.
- Khối dài b canh theo t, chỉ giữ khối nằm trọn trong phía (`bien_phia`), bỏ khối rỗng; cần ít nhất 5 khối có mẫu mỗi
  phía, thiếu thì rơi về G0.
- G3: T = r_d(A) − r_d(N) trên mẫu gốc của khối được giữ; h, l tính lại từ phần N của từng cách chia (`e4.nguong`);
  so T* ≥ T bằng số nguyên chính xác. Duyệt hết khi C(nN + nA, nA) ≤ B; ngược lại B hoán vị ngẫu nhiên,
  p = (1 + #{T* ≥ T}) / (B + 1); seed = 20261101 + int(sha256('mã|hướng')[:16], 16).
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
O_BIEN_S = 10      # ô 10 giây của B1.3b
O_DEM_S = 10
O_DEM_MIN = 3


def bien_phia(q, t_ns):
    """Biên hai phía cho chia khối (SPEC T-046 A3 điểm 3): N từ max(t − 300, H₀ làm tròn xuống ô 10 giây, F₀), A tới
    min(t + 300, H₁ làm tròn lên ô 10 giây, F₁). q: trạng thái quan sát của nguồn của đơn vị; không có H, F thì 300
    giây. Làm tròn vì mép bản ghi lệch vài mili giây không được bớt khối."""
    lo, hi = t_ns - W * NS, t_ns + W * NS
    q = q or {}
    H, F = q.get('H'), q.get('F')
    goc = lo
    o = O_BIEN_S * NS
    if H:
        lo2 = goc + ((int(H[0]) - goc) // o) * o
        hi2 = goc + -((goc - int(H[1])) // o) * o
        lo, hi = max(lo, lo2), min(hi, hi2)
    if F:
        lo, hi = max(lo, int(F[0])), min(hi, int(F[1]))
    return lo, hi


def o_1s(moc_ns, gia_tri, t_ns, phia):
    """{chỉ số ô: trung bình} của một phía. moc_ns: mốc mẫu (int ns)."""
    samples = {}
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
        samples.setdefault(j, []).append(float(v))
    return {j: math.fsum(sorted(samples[j])) / len(samples[j]) for j in sorted(samples, reverse=True)}


def tu_tuong_quan(o):
    """ρ(k), k = 1…K_MAX trên ô có giá trị (dict chỉ số → giá trị); None khi không xác định. Trả (rho, ly_do)."""
    if len(o) < CAP_TOI_THIEU:
        return None, 'it_o'
    order = sorted(o, reverse=True)  # thứ tự thời gian tăng, không theo thứ tự chèn dict
    x = np.array([o[j] for j in order], float)
    m = float(x.mean())
    v = float(((x - m) ** 2).mean())
    if v <= 0:
        return None, 'phuong_sai_0'
    rho = {}
    for k in range(1, K_MAX + 1):
        cap = [(o[j] - m) * (o[j + k] - m) for j in order if (j + k) in o]
        rho[k] = (sum(cap) / len(cap)) / v if len(cap) >= CAP_TOI_THIEU else None
    return rho, None


def do_dai_khoi(rho):
    """b. Trả (b, cham_tran): cham_tran khi không có k nào có ρ(k) < 0,2 (b = 60) hoặc k = 60."""
    for k in range(1, K_MAX + 1):
        r = rho.get(k)
        if r is not None and r < NGUONG_RHO:
            b = min(max(k, B_MIN), K_MAX)
            return b, b == K_MAX
    return K_MAX, True


def chia_khoi(moc_ns, gia_tri, t_ns, b, phia, bien):
    """{chỉ số khối: [giá trị]} của khối nằm trọn trong phía, bỏ khối rỗng. bien: mốc xa nhất của phía, ns."""
    bns = b * NS
    do_dai = (t_ns - bien) if phia == 'N' else (bien - t_ns)
    so_khoi = max(0, do_dai // bns)
    out = {}
    for x, v in zip(moc_ns, gia_tri):
        j = (t_ns - x - 1) // bns if phia == 'N' else (x - t_ns) // bns
        if 0 <= j < so_khoi:
            out.setdefault(j, []).append(float(v))
    return out


def chuan_bi_khoi(N, mocN, A, mocA, t_ns, bien_N, bien_A):
    """Tính b trên N và chia khối hai phía. Trả dict có 'roi_G0' (None hoặc lý do), b, khối."""
    oN = o_1s(mocN, N, t_ns, 'N')
    rho, ly_do = tu_tuong_quan(oN)
    if rho is None:
        return {'roi_G0': ly_do, 'b': None}
    b, cham_tran = do_dai_khoi(rho)
    kN = chia_khoi(mocN, N, t_ns, b, 'N', bien_N)
    kA = chia_khoi(mocA, A, t_ns, b, 'A', bien_A)
    out = {'roi_G0': None, 'b': b, 'cham_tran': cham_tran, 'khoi_N': kN, 'khoi_A': kA}
    if len(kN) < KHOI_TOI_THIEU or len(kA) < KHOI_TOI_THIEU:
        out['roi_G0'] = 'it_khoi'
    return out


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


def _dem_vuot(thong_ke, inA, T0_tu, T0_mau):
    cA, nA, cN, nN = thong_ke(inA)
    tu = cA * nN - cN * nA
    mau = nA * nN
    # tu/mau >= T0_tu/T0_mau  <=>  tu·T0_mau >= T0_tu·mau (mẫu số dương); dùng số nguyên Python để tránh tràn
    dem = sum(1 for a, b in zip(tu.tolist(), mau.tolist()) if a * T0_mau >= T0_tu * b)
    return dem, len(tu)


def p_G3(kb, huong, ts, ma, B=B_HOAN_VI):
    """G3. kb: kết quả chuan_bi_khoi (roi_G0 None). Trả p."""
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
    khoi_lo = max(1, min(B, int(4e6 // max(v.size, 1))))  # giới hạn bộ nhớ
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
        return float(dem / tong)
    rng = np.random.default_rng(seed_cua(ma, huong))
    dem = 0
    con = B
    while con > 0:
        r = min(con, khoi_lo)
        keys = rng.random((r, nb))
        idx = np.argsort(keys, axis=1)[:, :nbA]         # nbA khối ngẫu nhiên cho A, giữ số khối mỗi phía
        inA = np.zeros((r, nb), bool)
        np.put_along_axis(inA, idx, True, axis=1)
        d, _ = _dem_vuot(thong_ke, inA, T0_tu, T0_mau)
        dem += d
        con -= r
    return float((1 + dem) / (B + 1))


def p_theo_G3(N, mocN, A, mocA, t_ns, bien_N, bien_A, huong, ts, ma):
    """p của một phép theo G3, rơi về G0 khi không đủ khối hoặc ô. Trả (p, cách): cách là 'G3' hoặc 'G0:<cách của G0>'."""
    kb = chuan_bi_khoi(N, mocN, A, mocA, t_ns, bien_N, bien_A)
    if kb['roi_G0']:
        p, cach = e4.p_cong(A, N, huong, int(ts.get('n_exact_max', 100)))
        return p, 'G0:' + cach
    return p_G3(kb, huong, ts, ma), 'G3'


def he_so_phan_tan(moc_N, h0_ns, t_ns):
    """φ̂_d của D1 = max(1; s²/ȳ) trên ô 10 giây trọn của [h0, t), canh lùi từ t; dưới 3 ô thì 1."""
    if h0_ns is None or h0_ns >= t_ns:
        return 1.0
    w = O_DEM_S * NS
    so_o = (t_ns - h0_ns) // w
    if so_o < O_DEM_MIN:
        return 1.0
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
        return 1.0
    s2 = float(y.var(ddof=1))
    return max(1.0, s2 / m)
