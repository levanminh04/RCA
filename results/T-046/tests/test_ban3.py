"""Kiểm đáp án biết trước của ứng viên bản 3 (SPEC T-046 B4): G4 (làm trắng AR(1)), D1 (nhị thức có hiệu chỉnh
phân tán), chọn ngưỡng GE/DE."""
import numpy as np
from scipy.stats import binom

import cong
import t046
from m1 import e4

TS = {'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05, 'n_exact_max': 100}
NS = cong.NS


def _moc(t, n_N, n_A):
    return [t - (n_N - i) * NS + NS // 2 for i in range(n_N)], [t + i * NS + NS // 2 for i in range(n_A)]


def test_phan_du_phi_0_la_gia_tri():
    oN = {0: 3.0, 1: 2.0, 5: 1.0}
    oA = {0: 4.0, 2: 5.0}
    rN, rA = cong.phan_du_AR1(oN, oA, 0.0)
    assert rN == [1.0, 2.0, 3.0] and rA == [4.0, 5.0]


def test_phan_du_tinh_tay():
    oN = {0: 3.0, 1: 2.0, 2: 1.0, 4: 9.0}
    oA = {0: 4.0, 1: 6.0, 3: 7.0}
    rN, rA = cong.phan_du_AR1(oN, oA, 0.5)
    assert rN == [2.0 - 0.5 * 1.0, 3.0 - 0.5 * 2.0]   # ô 4, ô 2 thiếu ô trước; ô 1 dùng ô 2; ô 0 dùng ô 1
    assert rA == [4.0 - 0.5 * 3.0, 6.0 - 0.5 * 4.0]   # ô A 0 dùng ô N 0; ô A 3 thiếu ô 2


def test_G4_bang_p_cong_tren_phan_du():
    rng = np.random.default_rng(11)
    t = 50_000 * NS
    x = np.empty(600)
    x[0] = rng.standard_normal()
    for i in range(1, 600):
        x[i] = 0.8 * x[i - 1] + rng.standard_normal()
    N, A = list(x[:300]), list(x[300:])
    mN, mA = _moc(t, 300, 300)
    r = cong.p_G4_metric(N, mN, A, mA, t, 'len', TS)
    oN, oA = cong.o_1s(mN, N, t, 'N'), cong.o_1s(mA, A, t, 'A')
    rho, _ = cong.tu_tuong_quan(oN)
    phi = max(0.0, rho[1])
    rN = [N[i] - phi * N[i - 1] for i in range(1, 300)]
    rA = [A[0] - phi * N[-1]] + [A[i] - phi * A[i - 1] for i in range(1, 300)]
    assert r['roi_G0'] is None and abs(r['phi'] - phi) < 1e-15
    assert sorted(rN) == sorted(cong.phan_du_AR1(oN, oA, phi)[0])
    assert r['p'] == e4.p_cong(rA, rN, 'len', 100)[0]


def test_G4_N_hang_roi_G0():
    t = 1000 * NS
    mN, mA = _moc(t, 100, 100)
    r = cong.p_G4_metric([1.0] * 100, mN, [1.0] * 99 + [2.0], mA, t, 'len', TS)
    assert r['roi_G0'] == 'phuong_sai_0' and r['p'] == cong.p_G0([1.0] * 100, [1.0] * 99 + [2.0], 'len', TS)[0]


def test_D1_phi_1_trung_nhi_thuc():
    rng = np.random.default_rng(12)
    for _ in range(500):
        nN, nA = int(rng.integers(0, 200)), int(rng.integers(0, 200))
        if nN + nA == 0:
            continue
        TN, TA = float(rng.uniform(50, 300)), float(rng.uniform(50, 300))
        p0 = TA / (TN + TA)
        n = nN + nA
        for d in ('len', 'xuong'):
            ref = e4.p_nhi_thuc(nA, n, p0, d)
            got = cong.p_D1(nN, nA, TN, TA, 1.0, d)
            assert abs(got - ref) <= 1e-12, (nN, nA, d, got, ref)


def test_D1_phan_tan_lam_p_lon_hon():
    assert cong.p_D1(10, 40, 300, 300, 4.0, 'len') > cong.p_D1(10, 40, 300, 300, 1.0, 'len')


def test_he_so_phan_tan():
    t = 1000 * NS
    h0 = t - 60 * NS
    moc = [t - 5 * NS] * 6 + [t - 15 * NS] * 0 + [t - 25 * NS] * 2
    phi, so_o = cong.he_so_phan_tan(moc, h0, t)
    y = np.array([6, 0, 2, 0, 0, 0], float)
    assert so_o == 6 and abs(phi - max(1.0, y.var(ddof=1) / y.mean())) < 1e-12
    assert cong.he_so_phan_tan(moc, t - 25 * NS, t) == (1.0, 2)
    assert cong.he_so_phan_tan([], h0, t) == (1.0, 6)


def test_chon_nguong():
    ps = [0.5] * 990 + [0.003] * 10 + [0.0004] * 5
    # p < 0,01 và p < 0,005: 15/1005 > 0,01; p < 0,002: 5/1005 <= 0,01
    assert t046.chon_nguong(ps, 0.01) == 0.002
    assert t046.chon_nguong([0.0] * 10, 0.01) is None and t046.chon_nguong([], 0.01) is None


def _bang_dem(p_len_D1, chenh=True, F0=0):
    return {'pv': [], 'alpha': 0.01, 'so_cham_hop_le': 1,
            'dem': [{'ma': 'log|a|mau:1', 'e': 'a', 'trong_U': True, 'nhom': 'mau_loi', 'hop_le': True,
                     'huong_cham': ['len'], 'nhan': 'tang', 'p_len': 1e-6, 'p_xuong': 1.0, 'F_raw_len': F0,
                     'F_raw_xuong': 0, 'p_D1_len': p_len_D1, 'p_D1_xuong': 1.0, 'chenh_len_duong': chenh,
                     'chenh_xuong_duong': False}]}


def test_cong_dem_D0_D1_DE():
    b = _bang_dem(0.005, F0=1)
    assert t046.verdict_R0(b, 'G0', 'V0', c='D0') == 'CAUSE_FOUND'
    assert t046.verdict_R0(b, 'G0', 'V0', c='D1') == 'CAUSE_FOUND'
    assert t046.verdict_R0(b, 'G0', 'V0', c='DE', nguong={('mau_loi', 'len'): 0.001}) == 'NO_INTRINSIC_ANOMALY'
    assert t046.verdict_R0(_bang_dem(0.005, chenh=False), 'G0', 'V0', c='D1') == 'NO_INTRINSIC_ANOMALY'


def test_GE_dung_p_G4_va_nguong_theo_o():
    u = {'ma': 'metric|a_cpu', 'e': 'a', 'trong_U': True, 'nhom': 'metric', 'hop_le': True,
         'huong': {'len': {'p_G0': 1e-9, 'p_G4': 0.003, 'chenh_duong': True}}}
    b = {'pv': [u], 'dem': [], 'alpha': 0.01, 'so_cham_hop_le': 1}
    assert t046.verdict_R0(b, 'G4', 'V0') == 'CAUSE_FOUND'
    assert t046.verdict_R0(b, 'GE', 'V0', nguong={('metric', 'len'): 0.002}) == 'NO_INTRINSIC_ANOMALY'
    assert t046.verdict_R0(b, 'GE', 'V0', nguong={('metric', 'xuong'): 0.002}) == 'CAUSE_FOUND'
