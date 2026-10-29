"""Khối 4: E4 — ngưỡng, tỷ lệ vượt, cổng chính xác/xấp xỉ, cache, nhánh z.

Fixture 25–27, 41, 75, 76, 81. Cổng chính xác so oracle phân số, sai số ≤ 1e−12 (SPEC T-044 bước 3).
"""
from fractions import Fraction
from math import comb

import pytest

from conftest import fx, mau, gan_bang, gan_lam_tron, tu_lap, DAP_AN_THANH_PHAN

TS = {'m_span': 20, 'm_metric': 5, 'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05,
      'n_exact_max': 100, 'count_min': 10}


def _m(loai):
    return TS['m_metric'] if loai == 'metric' else TS['m_span']


def _oracle(da):
    if 'p' in da and isinstance(da['p'], list):
        return Fraction(da['p'][0], da['p'][1])
    if 'p_ti_so_to_hop' in da:
        (a, b), (c, d) = da['p_ti_so_to_hop']
        return Fraction(comb(a, b), comb(c, d))
    if 'p_dem' in da:
        k, (n, r) = da['p_dem']
        return Fraction(k, comb(n, r))
    return None


@pytest.mark.parametrize('i', [25, 26, 27])
def test_cong_oracle(i, ma):
    from m1 import e4
    f = fx(i)
    ma(f'{i}-cong-oracle')
    d = f['dau_vao']
    N = mau(d['N']) if isinstance(d['N'], str) else d['N']
    A = mau(d['A']) if isinstance(d['A'], str) else d['A']
    p = e4.exact_tied_greater(A, N)
    assert abs(p - float(_oracle(f['dap_an']))) <= 1e-12


@pytest.mark.parametrize('i', [25, 26, 27])
def test_cong_nguong_diem(i, ma):
    from m1 import e4
    f = fx(i)
    ma(f'{i}-{i}')
    d, da = f['dau_vao'], f['dap_an']
    N = mau(d['N']) if isinstance(d['N'], str) else d['N']
    A = mau(d['A']) if isinstance(d['A'], str) else d['A']
    kq = e4.cham_phan_vi(N, A, _m(d['loai_don_vi']), TS, huong_cham=('len',))
    assert gan_bang(kq['h'], da['h'])
    assert gan_bang(kq['r_len_A'], da['r_up_A'])
    assert gan_bang(kq['r_len_N'], da['r_up_N'])
    assert abs(kq['p_len'] - float(_oracle(da))) <= 1e-12
    assert gan_bang(kq['e_len'], da['e_up'])
    assert kq['F_raw_len'] == da['F_raw_len']


def test_41a(ma):
    from m1 import e4
    ca = fx(41)['ca'][0]
    ma('41-41a')
    N, A = mau(ca['N']), mau(ca['A'])
    kq = e4.cham_phan_vi(N, A, TS['m_span'], TS, huong_cham=('len',))
    assert abs(kq['p_len'] - 1.0) <= 1e-12 and ca['dap_an']['p'] == [1, 1]
    assert gan_bang(kq['e_len'], ca['dap_an']['e_up'])


def test_41_oracle(ma):
    """41a: p = 1 (A = N = 50 số 0), so oracle phân số 1/1."""
    from m1 import e4
    ca = fx(41)['ca'][0]
    ma('41-cong-oracle')
    assert abs(e4.exact_tied_greater(mau(ca['A']), mau(ca['N'])) - float(Fraction(*ca['dap_an']['p']))) <= 1e-12


def test_41b_oracle(ma):
    from m1 import e4
    ca = fx(41)['ca'][1]
    ma('41-41b-oracle')
    assert abs(e4.exact_tied_greater(mau(ca['A']), mau(ca['N'])) - float(_oracle(ca['dap_an']))) <= 1e-12


def test_41b(ma):
    from m1 import e4
    ca = fx(41)['ca'][1]
    ma('41-41b')
    kq = e4.cham_phan_vi(mau(ca['N']), mau(ca['A']), TS['m_span'], TS, huong_cham=('len',))
    assert gan_lam_tron(kq['p_len'], ca['dap_an']['p_thap_phan'])
    assert gan_bang(kq['e_len'], ca['dap_an']['e_up'])


def test_75_oracle(ma):
    from m1 import e4
    d, da = fx(75)['dau_vao'], fx(75)['dap_an']
    ma('75-oracle')
    assert abs(e4.exact_tied_greater(mau(d['A']), mau(d['N'])) - float(_oracle(da))) <= 1e-12


def test_75_co_va_diem(ma):
    from m1 import e4
    d, da = fx(75)['dau_vao'], fx(75)['dap_an']
    ma('75-75')
    kq = e4.cham_phan_vi(mau(d['N']), mau(d['A']), TS['m_span'], TS, huong_cham=('len',))
    assert gan_bang(kq['h'], da['h'])
    assert gan_lam_tron(kq['p_len'], da['p_thap_phan'])
    assert gan_bang(kq['e_len'], da['e_up']) and kq['F_raw_len'] == da['F_raw_len']
    z = e4.diem_z(mau(d['N']), mau(d['A']))
    assert gan_bang(z['z_len'], da['z_max'])
    assert (kq['F_raw_len'] == 1) == da['z_dung']


def test_76a_z_tho(ma):
    from m1 import e4
    ca = fx(76)['ca'][0]
    ma('76-76a')
    dv, da = ca['don_vi'], ca['dap_an']
    z = {k: e4.diem_z(mau(v['N']), mau(v['A']))['z_len'] for k, v in dv.items()}
    assert gan_bang(z['A_ms'], da['z_A_ms']) and gan_bang(z['A_us'], da['z_A_us']) and gan_bang(z['B'], da['z_B'])
    ms = sorted(['A', 'B'], key=lambda k: -z['A_ms' if k == 'A' else 'B'])
    us = sorted(['A', 'B'], key=lambda k: -z['A_us' if k == 'A' else 'B'])
    assert ms == da['thu_tu_ms'] and us == da['thu_tu_us']


def test_76b_e4_khong_doi_don_vi(ma):
    """76b dùng đơn vị của 76a: E4 cho e = 1 và cùng p ở cả A_ms, A_us, B, nên hòa."""
    from m1 import e4
    ca_a, ca_b = fx(76)['ca'][0], fx(76)['ca'][1]
    ma('76-76b')
    dv, da = ca_a['don_vi'], ca_b['dap_an']
    kq = {k: e4.cham_phan_vi(mau(v['N']), mau(v['A']), TS['m_span'], TS, huong_cham=('len',)) for k, v in dv.items()}
    p_oracle = float(Fraction(*da['p']))
    for k in ('A_ms', 'A_us', 'B'):
        assert abs(kq[k]['p_len'] - p_oracle) <= 1e-12
    assert gan_bang(kq['A_ms']['e_len'], da['e_A']) and gan_bang(kq['A_us']['e_len'], da['e_A'])
    assert gan_bang(kq['B']['e_len'], da['e_B'])
    assert (kq['A_ms']['e_len'] == kq['B']['e_len']) == da['hoa']


def test_76c_iqr_nho(ma):
    from m1 import e4
    ca = fx(76)['ca'][2]
    ma('76-76c')
    z = e4.diem_z(mau(ca['don_vi']['N']), mau(ca['don_vi']['A']))
    da = ca['dap_an']
    assert gan_lam_tron(z['IQR'], da['IQR'])
    assert z['c'] == da['c']
    assert gan_lam_tron(z['z_len'], da['z'])


def test_81_p_xap_xi(ma):
    from m1 import e4
    d, da = fx(81)['dau_vao'], fx(81)['dap_an']
    ma('81-p')
    kq = e4.cham_phan_vi(mau(d['N']), mau(d['A']), TS['m_metric'], TS, huong_cham=('len',))
    assert kq['cach_cong_len'] == 'xap_xi'
    assert abs(kq['p_len'] / da['p_xap_xi'] - 1) <= 0.01


def test_81_e_theo_bien_doi(ma):
    from m1 import e4
    d, da = fx(81)['dau_vao'], fx(81)['dap_an']
    ma('81-e')
    N0, A0 = mau(d['N']), mau(d['A'])
    bien_doi = {'eps_0.05': (lambda x: x, 0.05), 'eps_0': (lambda x: x, 0.0), 'nhan_10': (lambda x: 10 * x, 0.05),
                'tru_2000': (lambda x: x - 2000, 0.05), 'cong_10000': (lambda x: x + 10000, 0.05)}
    for ten, (f, eps) in bien_doi.items():
        ts = dict(TS, epsilon=eps)
        kq = e4.cham_phan_vi([f(x) for x in N0], [f(x) for x in A0], TS['m_metric'], ts, huong_cham=('len',))
        assert gan_lam_tron(kq['e_len'], da['e_up'][ten]), ten


def test_cache_theo_noi_dung(ma):
    """B1.3: cache cổng theo khóa nội dung, không phụ thuộc config_id; mẫu đổi thì là đơn vị khác."""
    from m1 import e4
    ma('cache')
    c = e4.CacheCong()
    N, A = mau('20x0'), mau('13x0+7x1')
    p1 = c.p(('op', 'A', 'x'), A, N, 'len', TS)
    p2 = c.p(('op', 'A', 'x'), list(reversed(A)), list(reversed(N)), 'len', TS)
    assert p1 == p2 and c.trung == 1 and c.moi == 1
    c.p(('op', 'A', 'x'), mau('14x0+6x1'), N, 'len', TS)
    assert c.moi == 2


def test_VB_392_dem_tai_tang(ma):
    """Đáp án trong văn bản: SPEC T-043 dòng 392 — 100 → 200 sự kiện, hai khoảng bằng nhau: e_up = 0,5; p ≈ 4,0 × 10⁻⁹."""
    from m1 import e4
    from conftest import tu_lap, DAP_AN_VAN_BAN
    m = tu_lap(DAP_AN_VAN_BAN, 'VB-392')
    ma('VB-392')
    d = m['dau_vao']
    kq = e4.cham_dem(d['n_N'], d['n_A'], d['T_N'], d['T_A'], TS)
    assert gan_bang(kq['e_len'], m['dap_an']['e_up'])
    assert gan_lam_tron(kq['p_len'], m['dap_an']['p'])


def _p_nhi_thuc_chinh_xac(k, n, p0):
    """Oracle phân số: P(X >= k), X ~ Bin(n, p0)."""
    p0 = Fraction(p0).limit_denominator(10 ** 12)
    return sum(Fraction(comb(n, j)) * p0 ** j * (1 - p0) ** (n - j) for j in range(k, n + 1))


def test_D5_quyet_dinh_doi_khi_T_lech(ma):
    """Đ5 (Q-209 mục 2): báo đơn vị đếm có quyết định cổng đổi khi T lệch ±1%. Oracle: nhị thức phân số."""
    from m1 import e4
    ma('D5-1')
    n_N, n_A, T = 100, 135, 300.0
    doi_oracle = False
    goc = _p_nhi_thuc_chinh_xac(n_A, n_N + n_A, Fraction(1, 2)) < Fraction(1, 100)
    for fN in (Fraction(99, 100), 1, Fraction(101, 100)):
        for fA in (Fraction(99, 100), 1, Fraction(101, 100)):
            p0 = (T * fA) / (T * fN + T * fA)
            doi_oracle |= ((_p_nhi_thuc_chinh_xac(n_A, n_N + n_A, p0) < Fraction(1, 100)) != goc)
    assert e4.doi_quyet_dinh_khi_T_lech(n_N, n_A, T, T, TS, ty_le=0.01) == doi_oracle
    assert e4.doi_quyet_dinh_khi_T_lech(10, 40, T, T, TS, ty_le=0.01) is False


@pytest.mark.parametrize('muc', ['T4C-1', 'T4C-2', 'T4C-3', 'T4C-4', 'T4C-5'])
def test_T4c_m(muc, ma):
    """CĐ7: m của đơn vị phân vị và đơn vị đếm (đáp án tự lập)."""
    from m1 import e4
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    d = m['dau_vao']
    if 'N' in d:
        got = e4.m_T4c_phan_vi(d['N'], d['A'])
    else:
        got = e4.m_T4c_dem(d['n_N'], d['n_A'], d['T_N'], d['T_A'])
    assert abs(got - m['dap_an']['m']) <= 1e-12


def test_T4c_khoa(ma):
    """CĐ7: khóa T4c (max s, max m, số kênh, Σs) so với E6a."""
    from m1 import xep_hang
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_THANH_PHAN, 'T4C-6')
    ma('T4C-6')
    kenh = [Kenh(e, t, 'len', 'lan_nguoc', s) for e, t, s, _ in m['dau_vao']['kenh']]
    mm = {}
    for e, _, _, x in m['dau_vao']['kenh']:
        mm[e] = max(mm.get(e, 0.0), x)
    kT = {e: (v, v) for e, v in mm.items()}
    a = xep_hang.xep(kenh, thuc_the_co_kenh_OK=set(mm))
    b = xep_hang.xep(kenh, thuc_the_co_kenh_OK=set(mm), khoa_T4c=kT)
    assert [g for bl in a['blocks'] for g in bl['groups']] == m['dap_an']['E6a']
    assert [g for bl in b['blocks'] for g in bl['groups']] == m['dap_an']['T4c']
