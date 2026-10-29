"""Khối 10: đối chứng C-d3 (17–20; B7), C-g (33, 68), C-e (32, 43, 56), C-d2 (B6), C-a0, C-a1, C-d1, C-c (tự lập)."""
from fractions import Fraction

import pytest

from conftest import fx, bx, gan_bang, tu_lap, DAP_AN_DOI_CHUNG


@pytest.mark.parametrize('i', [17, 18, 19, 20])
def test_Cd3(i, ma):
    from m1 import doi_chung
    f = fx(i)
    ma(str(i))
    d, da = f['dau_vao'], f['dap_an']
    kq = doi_chung.cd3([tuple(c) for c in d['canh_goi']], d['diem'], d['dich'])
    assert kq['trang_thai'] == da['trang_thai']
    if 'diem_ung_vien' in da:
        assert {k: round(v, 12) for k, v in kq['diem_ung_vien'].items()} == \
            {k: round(v, 12) for k, v in da['diem_ung_vien'].items()}
    if 'root_tra_ve' in da:
        assert (d['root'] in kq['diem_ung_vien']) == da['root_tra_ve']


def test_B7_khong_span_goc(ma):
    from m1 import doi_chung
    f = bx('B7')
    ma('B7')
    d, da = f['dau_vao'], f['dap_an']
    dich = doi_chung.dich_cd3(d['spans_A'], set(d['bat_thuong_lan_nguoc']))
    assert dich == da['dich']
    kq = doi_chung.cd3([], {e: 1.0 for e in d['bat_thuong_lan_nguoc']}, dich)
    assert kq['trang_thai'] == da['trang_thai']
    assert kq.get('blocks', []) == [] and da['RR'] == 0


@pytest.mark.parametrize('i', [33, 68])
def test_Cg(i, ma):
    from m1 import doi_chung
    from m1_danh_gia import rr
    f = fx(i)
    ma(str(i))
    d, da = f['dau_vao'], f['dap_an']
    kq = doi_chung.cg(d['phieu'], d['thu_tu_SimpleRCA'], [tuple(c) for c in d['canh']])
    assert [g for b in kq['blocks'] for g in b['groups']] == da['danh_sach']
    if 'rr' in da:
        assert gan_bang(rr.rr_ca(kq['blocks'], d['root']), da['rr'])


def test_32_moc_gia(ma):
    from m1_danh_gia import moc_gia
    f = fx(32)
    ma('32')
    kq = moc_gia.ve_moc_gia([tuple(c) for c in f['dau_vao']['cap']])
    da = f['dap_an']
    assert kq['mau_so'] == da['mau_so'] and kq['bi_loai'] == da['bi_loai']
    assert gan_bang(kq['ty_le_tat'], da['ty_le_tat']) and gan_bang(kq['ty_le_bat'], da['ty_le_bat'])
    assert kq['HAI'] == da['HAI']


def test_43_mau_so_0(ma):
    from m1_danh_gia import moc_gia
    f = fx(43)
    ma('43')
    kq = moc_gia.ve_moc_gia([tuple(c) for c in f['dau_vao']['cap']])
    assert kq['mau_so'] == f['dap_an']['mau_so']
    assert kq['ve'] == f['dap_an']['ve_C_e'] and kq['HAI'] == f['dap_an']['HAI']


@pytest.mark.parametrize('ma_ca', ['56a', '56b'])
def test_56_tran(ma_ca, ma):
    from m1_danh_gia import moc_gia
    ca = next(c for c in fx(56)['ca'] if c['ma'] == ma_ca)
    ma(f'56-{ma_ca}')
    kq = moc_gia.ve_tu_dem(tuple(ca['tat']), tuple(ca['bat']))
    assert kq['ve'] == ca['dap_an']['ve']
    if 'tang' in ca['dap_an']:
        assert gan_bang(kq['tang'], ca['dap_an']['tang'])


def test_B6_Cd2(ma):
    from m1 import doi_chung
    f = bx('B6')
    ma('B6')
    tt = [(x['ten'], x['khoi_phat'], (x['K_raw'],)) for x in f['dau_vao']['thuc_the']]
    kq = doi_chung.cd2(tt)
    assert [e for b in kq['blocks'] for g in b['groups'] for e in g] == f['dap_an']['thu_tu']


@pytest.mark.parametrize('muc', ['CA1-S1', 'CA1-S2', 'CA1-S2b', 'CA1-S3', 'CA1-S7'])
def test_Ca1(muc, ma):
    """C-a1: chuỗi cuối bỏ E2, E5, E6b, E7; giữ E1 (SPEC B2). Đáp án tự lập từ fixture 1."""
    from m1 import chuoi
    from m1_danh_gia import rr
    from test_k09_chuoi import _don_vi_co
    m = tu_lap(DAP_AN_DOI_CHUNG, muc)
    ma(muc)
    ca = next(c for c in fx(1)['ca'] if c['ma'] == m['dau_vao']['S'])
    chuoi_cuoi = m['dau_vao']['chuoi_cuoi']
    ch = chuoi.doi_chung_cau_hinh('C-a1', chuoi_cuoi)
    assert ch == m['dap_an']['cau_hinh']
    kq = chuoi.xep_tu_don_vi(_don_vi_co(ca['don_vi']), [tuple(c) for c in ca['canh']], set(ca['quan_sat']), ch)
    assert sorted(kq['blocks'][0]['groups'][0]) == m['dap_an']['dau']
    r = rr.rr_ca(kq['blocks'], ca['root']) if ca['root'] in ca['quan_sat'] else Fraction(0)
    assert gan_bang(r, m['dap_an']['rr'])


def test_Ca0_cau_hinh(ma):
    """C-a0 (D18): E1 tắt, giữ span bọc; không E2, E5, E6b, E7; tín hiệu của chuỗi cuối; K_I = K_raw."""
    from m1 import chuoi
    m = tu_lap(DAP_AN_DOI_CHUNG, 'CA0')
    ma('CA0')
    assert chuoi.doi_chung_cau_hinh('C-a0', m['dau_vao']['chuoi_cuoi']) == m['dap_an']['cau_hinh']


@pytest.mark.parametrize('muc', ['CD1-1', 'CD1-2'])
def test_Cd1(muc, ma):
    from m1 import doi_chung
    from test_k08_e5_e6_e7_e9 import kenh_tu_fixture
    m = tu_lap(DAP_AN_DOI_CHUNG, muc)
    ma(muc)
    d = m['dau_vao']
    kq = doi_chung.cd1(kenh_tu_fixture(d['kenh']), [tuple(c) for c in d['canh']], set(d['quan_sat']))
    assert [g for b in kq['blocks'] for g in b['groups']] == m['dap_an']['danh_sach']


@pytest.mark.parametrize('muc', ['CC1', 'CC2'])
def test_Cc(muc, ma):
    from m1 import doi_chung
    m = tu_lap(DAP_AN_DOI_CHUNG, muc)
    ma(muc)
    d = m['dau_vao']
    kq = doi_chung.cc(d['danh_sach'], k=60)
    got = {e: float(v) for e, v in kq['diem'].items()}
    for e, v in m['dap_an']['diem'].items():
        assert abs(got[e] - v) <= 1e-12, e
    assert [g for b in kq['blocks'] for g in b['groups']] == m['dap_an']['danh_sach']


def test_Cd2_khoi_phat_thuc_the(ma):
    """C-d2: khởi phát của thực thể là khởi phát sớm nhất trong các đơn vị phân vị bất thường (Đ11)."""
    from m1 import doi_chung
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_DOI_CHUNG, 'CD2-1')
    ma('CD2-1')
    kenh = [Kenh(k[0], k[1], 'len', 'lan_nguoc', k[2], loai=k[3], khoi_phat=k[4]) for k in m['dau_vao']['kenh']]
    kq = doi_chung.cd2_tu_kenh(kenh, set(m['dau_vao']['quan_sat']))
    assert [g for b in kq['blocks'] for g in b['groups']] == m['dap_an']['danh_sach']
