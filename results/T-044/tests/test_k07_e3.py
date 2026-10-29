"""Khối 7: E3 và nhánh tắt (fixture 55, 73); che token, chuỗi vào Drain, ba cách khớp (CĐ4, ca tự lập); E3b."""
import pytest

from conftest import fx, gan_bang, tu_lap, DAP_AN_THANH_PHAN

TS = {'m_span': 20, 'm_metric': 5, 'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05,
      'n_exact_max': 100, 'count_min': 10}
TU_KHOA = {'kieu': 'tu_khoa', 'tu_khoa': ['ERROR', 'FAIL', 'EXCEPTION']}


def test_55_nhanh_tat(ma):
    """E3 tắt: một đơn vị đếm số dòng log lỗi mỗi thực thể; không có mẫu mới, không có log thường giảm."""
    from fractions import Fraction
    from m1 import kenh, e4
    f = fx(55)
    ma('55')
    d, da = f['dau_vao'], f['dap_an']
    T_N, T_A = d['T']['P']
    N = [{'moc': i, 'thuc_the': 'X', 'noi_dung': f'ERROR job {i} failed', 'lop': None} for i in range(d['n_N'])]
    A = [{'moc': 400 + i, 'thuc_the': 'X', 'noi_dung': f'ERROR job {i} failed', 'lop': None} for i in range(d['n_A'])]
    dv = kenh.don_vi_log(N, A, quy_tac=TU_KHOA, E3_bat=False)
    assert [u['nhom'] for u in dv] == ['log_loi']
    u = dv[0]
    assert (u['n_N'], u['n_A']) == (d['n_N'], d['n_A'])
    kq = e4.cham_dem(u['n_N'], u['n_A'], T_N, T_A, TS)
    assert kq['nhan'] == da['P']['nhan']
    assert gan_bang(kq['e_len'], da['P']['e'])
    assert abs(kq['p_len'] - float(Fraction(*da['P']['p']))) <= 1e-12
    for k in da['khong_co']:
        assert k not in [x['nhom'] for x in dv]


def test_73_huong_xuong(ma):
    from m1 import kenh
    from m1.kieu import Kenh
    from m1 import xep_hang
    f = fx(73)
    ma('73')
    d, da = f['dau_vao'], f['dap_an']
    (ten, huong, s), = d['kenh']['A']
    for e3_bat, nhanh in ((True, 'E3_bat'), (False, 'E3_tat')):
        huong_cham = kenh.huong_cham('op_full', E3_bat=e3_bat)
        cham = huong in huong_cham
        assert cham == da[nhanh]['cham']
        ds = [Kenh('A', ten, huong, kenh.lop('op_full', huong), s)] if cham else []
        if cham:
            assert ds[0].lop == da[nhanh]['lop']
        xh = xep_hang.xep(ds, thuc_the_co_kenh_OK={'A'})
        assert list(xh['K_raw']['A']) == da[nhanh]['K_raw']


@pytest.mark.parametrize('muc', ['MASK1', 'MASK2', 'MASK3', 'MASK4', 'MASK5', 'MASK6', 'MASK7'])
def test_che_token(muc, ma):
    from m1 import e3
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    assert e3.che_token(m['dau_vao']) == m['dap_an']


@pytest.mark.parametrize('muc', ['NEZ1', 'NEZ2', 'NEZ3', 'NEZ4'])
def test_chuoi_nezha(muc, ma):
    from m1 import e3
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    assert e3.chuoi_vao_drain_nezha(m['dau_vao']) == m['dap_an']


@pytest.mark.parametrize('muc', ['KHOP1', 'KHOP2'])
@pytest.mark.parametrize('khop', ['hoan_toan', 'nguong', 'nguong_cung_lop'])
def test_ba_cach_khop(muc, khop, ma):
    from m1 import e3
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(f'{muc}-{khop}')
    d = m['dau_vao']
    kq = e3.hoc_va_dem(d['N'], d['A'], {'khop': khop, 'sim_th': 0.4, 'do_sau': 4},
                       {'kieu': 'severity', 'loi': ['ERROR'], 'khong_loi': ['INFO']})
    assert kq['mau_moi'].get(d['thuc_the'], 0) == m['dap_an'][khop]['mau_moi']


def test_E3b_tan_suat(ma):
    """E3b: đơn vị đếm theo thao tác; NEW_OP, STOPPED (đặc tả v1 §4, §7.4)."""
    from m1 import kenh, e4
    m = tu_lap(DAP_AN_THANH_PHAN, 'E3B1')
    ma('E3B1')
    from m1 import span
    d = m['dau_vao']
    t = 1000
    rows, k = [], 0
    for op, (n_N, n_A) in d['ops'].items():
        chu, ten = op.split('|')
        for phia, n in (('N', n_N), ('A', n_A)):
            for i in range(n):
                st = (t - 290 + i) if phia == 'N' else (t + 10 + i)
                rows.append({'traceID': f'T{k}', 'spanID': 's', 'parentSpanID': '', 'owner': chu, 'operation': ten,
                             'start_us': st, 'duration_us': 0.5})
                k += 1
    dem = kenh.dem_thao_tac(span.chuan_bi(rows, t=t, tau=1))
    for op, dap in m['dap_an'].items():
        n_N, n_A = dem[tuple(op.split('|'))]
        kq = e4.cham_dem(n_N, n_A, d['T'][0], d['T'][1], TS)
        assert kq['nhan'] == dap['nhan'], op
        assert gan_bang(kq['e_' + dap['huong']], dap['e']), op
