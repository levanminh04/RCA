"""Kiểm đáp án biết trước của G1, G3 (SPEC T-046 A7): phân vị theo hàng khớp numpy; thống kê gốc của G3 khớp e4;
G3 duyệt hết khớp tính tay bằng phân số; G1 khớp p_cong trên trung bình khối tính tay; chuỗi hằng cho p = 1; cùng
seed cho cùng p; không đổi theo PYTHONHASHSEED; ô, khối canh đúng biên."""
import itertools
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

import cong
from m1 import e4

TS = {'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05, 'n_exact_max': 100}
NS = cong.NS


def test_nguong_hang_khop_numpy_tung_bit():
    rng = np.random.default_rng(1)
    for n in list(range(1, 40)) + [100, 301]:
        for _ in range(30):
            x = np.round(rng.normal(size=n) * rng.choice([1, 1e-3, 1e6]), rng.integers(0, 4))
            for q in (0.95, 0.05):
                Xs = np.sort(np.r_[x, np.full(5, np.nan)])[None, :]
                got = cong._nguong_hang(Xs, np.array([n]), q)[0]
                ref = float(np.percentile(x, 100 * q))
                assert got == ref, (n, q)


def _bien(t_ns, N, A, b):
    mocN = [t_ns - (i + 1) * NS + NS // 2 for i in range(len(N))]
    mocA = [t_ns + i * NS + NS // 2 for i in range(len(A))]
    return mocN, mocA


def test_o_va_khoi_canh_bien():
    t = 1000 * NS
    assert cong.o_1s([t - 1], [1.0], t, 'N') == {0: 1.0}
    assert cong.o_1s([t - NS], [1.0], t, 'N') == {0: 1.0}
    assert cong.o_1s([t - NS - 1], [1.0], t, 'N') == {1: 1.0}
    assert cong.o_1s([t], [1.0], t, 'A') == {0: 1.0}
    assert cong.o_1s([t + NS], [1.0], t, 'A') == {1: 1.0}
    assert cong.o_1s([t - 300 * NS], [1.0], t, 'N') == {299: 1.0}
    assert cong.o_1s([t - 300 * NS - 1], [1.0], t, 'N') == {}
    # b = 7: 42 khối trọn (294 giây); khối dở ở đầu xa bị bỏ
    k = cong.chia_khoi([t - 294 * NS, t - 294 * NS - 1], [1.0, 2.0], t, 7, 'N')
    assert k == {41: [1.0]}
    k = cong.chia_khoi([t + 293 * NS, t + 294 * NS], [1.0, 2.0], t, 7, 'A')
    assert k == {41: [1.0]}


def test_do_dai_khoi():
    assert cong.do_dai_khoi({k: (0.9 if k < 12 else 0.1) for k in range(1, 61)}) == (12, False)
    assert cong.do_dai_khoi({k: (0.1) for k in range(1, 61)}) == (5, False)
    assert cong.do_dai_khoi({k: 0.5 for k in range(1, 61)}) == (60, True)
    assert cong.do_dai_khoi({k: (None if k < 30 else 0.1) for k in range(1, 61)}) == (30, False)
    assert cong.do_dai_khoi({k: (0.5 if k < 60 else 0.1) for k in range(1, 61)}) == (60, True)


def test_tu_tuong_quan_tinh_tay():
    o = {j: float(v) for j, v in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])}
    rho, ly = cong.tu_tuong_quan(o)
    x = np.arange(1, 13, dtype=float)
    m, v = x.mean(), ((x - x.mean()) ** 2).mean()
    tay = np.mean((x[:-1] - m) * (x[1:] - m)) / v
    assert ly is None and abs(rho[1] - tay) < 1e-12
    assert rho[3] is None  # 9 cặp < 10
    assert cong.tu_tuong_quan({j: 1.0 for j in range(20)}) == (None, 'phuong_sai_0')
    assert cong.tu_tuong_quan({j: float(j) for j in range(9)}) == (None, 'it_o')


def test_G1_bang_p_cong_tren_trung_binh_khoi():
    rng = np.random.default_rng(2)
    t = 10_000 * NS
    N = list(rng.normal(size=300))
    A = list(rng.normal(size=300) + 0.3)
    mocN, mocA = _bien(t, N, A, None)
    kb = cong.chuan_bi_khoi(N, mocN, A, mocA, t)
    assert kb['roi_G0'] is None
    b = kb['b']
    mN = [np.mean([N[i] for i in range(300) if i // b == j]) for j in range(300 // b)]
    mA = [np.mean([A[i] for i in range(300) if i // b == j]) for j in range(300 // b)]
    for d in ('len', 'xuong'):
        assert cong.p_G1(kb, d, TS) == e4.p_cong(mA, mN, d, 100)


def _p_G3_tay(kN, kA, huong):
    """Duyệt hết bằng e4.nguong và phân số."""
    blocks = list(kN) + list(kA)
    nbA = len(kA)
    def T(idxA):
        XA = [x for i in idxA for x in blocks[i]]
        XN = [x for i in range(len(blocks)) if i not in idxA for x in blocks[i]]
        ng = e4.nguong(XN, TS)
        rA = e4.ty_le_vuot_q(XA, ng['h'], ng['l'])
        rN = e4.ty_le_vuot_q(XN, ng['h'], ng['l'])
        return (rA[0] - rN[0]) if huong == 'len' else (rA[1] - rN[1])
    T0 = T(tuple(range(len(kN), len(blocks))))
    cs = list(itertools.combinations(range(len(blocks)), nbA))
    return Fraction(sum(1 for c in cs if T(c) >= T0), len(cs))


@pytest.mark.parametrize('seed', [3, 4, 5])
def test_G3_duyet_het_khop_tinh_tay(seed):
    rng = np.random.default_rng(seed)
    kN = [list(np.round(rng.normal(size=rng.integers(1, 5)), 1)) for _ in range(5)]
    kA = [list(np.round(rng.normal(size=rng.integers(1, 5)) + 0.8, 1)) for _ in range(5)]
    kb = {'khoi_N': dict(enumerate(kN)), 'khoi_A': dict(enumerate(kA))}
    for d in ('len', 'xuong'):
        p, cach, ct = cong.p_G3(kb, d, TS, 'u')
        assert ct['cach'] == 'duyet_het' and ct['so_cach'] == 252
        assert Fraction(p).limit_denominator(1000) == _p_G3_tay(kN, kA, d)


def test_G3_thong_ke_goc_khop_e4():
    rng = np.random.default_rng(6)
    kN = [list(rng.normal(size=8)) for _ in range(10)]
    kA = [list(rng.normal(size=8) + 0.5) for _ in range(10)]
    kb = {'khoi_N': dict(enumerate(kN)), 'khoi_A': dict(enumerate(kA))}
    XN = [x for b in kN for x in b]
    XA = [x for b in kA for x in b]
    ng = e4.nguong(XN, TS)
    rA = e4.ty_le_vuot_q(XA, ng['h'], ng['l'])
    rN = e4.ty_le_vuot_q(XN, ng['h'], ng['l'])
    for d, i in (('len', 0), ('xuong', 1)):
        _, _, ct = cong.p_G3(kb, d, TS, 'u', B=50)
        cA, nA, cN, nN = ct['T']
        assert Fraction(cA, nA) == rA[i] and Fraction(cN, nN) == rN[i]


def test_chuoi_hang_cho_p_bang_1():
    t = 1000 * NS
    N = [5.0] * 300
    A = [5.0] * 300
    mocN, mocA = _bien(t, N, A, None)
    for g in ('G1', 'G3'):
        for d in ('len', 'xuong'):
            r = cong.p_theo_cong(g, N, mocN, A, mocA, t, d, TS, 'u')
            assert r['p'] == 1.0 and r['roi_G0'] == 'phuong_sai_0'
    kb = {'khoi_N': {j: [5.0] * 10 for j in range(30)}, 'khoi_A': {j: [5.0] * 10 for j in range(30)}}
    assert cong.p_G3(kb, 'len', TS, 'u')[0] == 1.0


def test_G3_cung_seed_cung_p_va_doi_seed_doi_mau():
    rng = np.random.default_rng(7)
    kb = {'khoi_N': {j: list(rng.normal(size=10)) for j in range(30)},
          'khoi_A': {j: list(rng.normal(size=10) + 0.1) for j in range(30)}}
    a = cong.p_G3(kb, 'len', TS, 'op|x|y')
    b = cong.p_G3(kb, 'len', TS, 'op|x|y')
    assert a == b and a[2]['cach'] == 'ngau_nhien' and a[2]['B'] == 2000
    assert cong.seed_cua('op|x|y', 'len') != cong.seed_cua('op|x|y', 'xuong')


def test_G3_khong_doi_theo_PYTHONHASHSEED():
    ma = r"""
import sys, json, numpy as np
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2])
import cong
rng = np.random.default_rng(8)
kb = {'khoi_N': {j: list(rng.normal(size=6)) for j in range(25)}, 'khoi_A': {j: list(rng.normal(size=6)) for j in range(25)}}
print(json.dumps(cong.p_G3(kb, 'len', {'alpha': 0.01, 'epsilon': 0.05}, 'metric|a_cpu')[0]))
"""
    root = Path(__file__).resolve().parents[3]
    out = set()
    for hs in ('0', '1', '12345'):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        r = subprocess.run([sys.executable, '-B', '-c', ma, str(root / 'src'), str(root / 'results/T-046/scripts')],
                           capture_output=True, text=True, env=env, check=True)
        out.add(r.stdout.strip())
    assert len(out) == 1


def test_chia_khoi_bien_bo_khoi_do():
    # R1: A/A 150 giây, b = 37: chỉ 4 khối trọn (148 giây); khối thứ năm chứa 2 giây không được giữ
    t = 1000 * NS
    moc = [t - i * NS - NS // 2 for i in range(150)]
    k_cu = cong.chia_khoi(moc, [1.0] * 150, t, 37, 'N')
    k_moi = cong.chia_khoi(moc, [1.0] * 150, t, 37, 'N', bien=t - 150 * NS)
    assert sorted(k_cu) == [0, 1, 2, 3, 4] and len(k_cu[4]) == 2
    assert sorted(k_moi) == [0, 1, 2, 3]
    mA = [t + i * NS + NS // 2 for i in range(150)]
    assert sorted(cong.chia_khoi(mA, [1.0] * 150, t, 37, 'A', bien=t + 150 * NS)) == [0, 1, 2, 3]
    kb = cong.chuan_bi_khoi(list(np.random.default_rng(1).normal(size=150).cumsum()), moc[::-1],
                            [0.0] * 150, mA, t, t - 150 * NS, t + 150 * NS)
    assert kb['b'] is None or kb['b'] * 4 <= 150 or kb['roi_G0'] == 'it_khoi'


def test_bien_don_vi_lam_tron_o_10_giay():
    import t046
    t = 100000 * NS
    p = {'nguon_metric': {}}
    rec = {'coverage': {'trace': {'H': [t - 299 * NS - 5, t + 299 * NS], 'F': [t - 900 * NS, t + 900 * NS]}}}
    assert t046.bien_don_vi(rec, p, 'op|a|b', t) == (t - 300 * NS, t + 300 * NS)  # N4: mép lệch nhỏ không bớt khối
    rec = {'coverage': {'trace': {'H': [t - 95 * NS, t + 92 * NS], 'F': [t - 900 * NS, t + 900 * NS]}}}
    assert t046.bien_don_vi(rec, p, 'op|a|b', t) == (t - 100 * NS, t + 100 * NS)
    rec = {'coverage': {'trace': {'H': [t - 145 * NS, t + 145 * NS], 'F': [t - 150 * NS, t + 147 * NS]}}}
    assert t046.bien_don_vi(rec, p, 'op|a|b', t) == (t - 150 * NS, t + 147 * NS)  # chặn bởi F
