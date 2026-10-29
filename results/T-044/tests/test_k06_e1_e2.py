"""Khối 6: E1-U, E1-CP (fixture 2–5; ca tự lập CP1 của CĐ1); E2-C, E2-VC (fixture 9–13). Đơn vị ms; τ = 1 ms."""
import pytest

from conftest import fx, gan_bang, tu_lap, DAP_AN_THANH_PHAN


@pytest.mark.parametrize('i', [2, 3])
def test_U_CP(i, ma):
    from m1 import span
    f = fx(i)
    ma(str(i))
    cha, con = tuple(f['dau_vao']['cha']), [tuple(c) for c in f['dau_vao']['con']]
    assert gan_bang(span.doc_quyen_U(cha, con), f['dap_an']['U'])
    assert gan_bang(span.doc_quyen_CP(cha, con, tau=1), f['dap_an']['CP'])


@pytest.mark.parametrize('i', [4, 5])
def test_cat_con(i, ma):
    from m1 import span
    f = fx(i)
    ma(str(i))
    cha, con = tuple(f['dau_vao']['cha']), [tuple(c) for c in f['dau_vao']['con']]
    cat, vuot = span.cat_con(cha, con, nguong_vuot=1)
    assert [list(c) for c in cat] == f['dap_an']['con_cat']
    assert vuot == f['dap_an']['vuot_bien_qua_1ms']
    assert gan_bang(span.doc_quyen_U(cha, con), f['dap_an']['U'])


def test_CP_tu_lap(ma):
    """CĐ1: ca tự lập, cha có ba con, hai con chồng lấn."""
    from m1 import span
    m = tu_lap(DAP_AN_THANH_PHAN, 'CP1')
    ma('CP1')
    cha, con = tuple(m['dau_vao']['cha']), [tuple(c) for c in m['dau_vao']['con']]
    assert gan_bang(span.doc_quyen_CP(cha, con, tau=1), m['dap_an']['CP'])
    assert gan_bang(span.doc_quyen_U(cha, con), m['dap_an']['U'])
    assert [list(c) for c in span.duong_gang(cha, con, tau=1)] == m['dap_an']['duong_gang']


@pytest.mark.parametrize('i', [9, 10, 11, 12, 13])
def test_phu_dinh(i, ma):
    from m1 import e2
    f = fx(i)
    ma(str(i))
    kq = e2.gan_canh([tuple(c) for c in f['dau_vao']['canh_co']], che_do='VC')
    assert kq['dinh_danh'] == f['dap_an']['dinh_danh']
    assert [list(g) for g in kq['gan']] == f['dap_an']['gan']


def test_E2C_gan_ben_duoc_goi(ma):
    """E2-C: mọi cạnh gán cho bên được gọi (SPEC B2 E2); dùng lại đầu vào fixture 13."""
    from m1 import e2
    ma('E2C1')
    m = tu_lap(DAP_AN_THANH_PHAN, 'E2C1')
    kq = e2.gan_canh([tuple(c) for c in m['dau_vao']['canh_co']], che_do='C')
    assert [list(g) for g in kq['gan']] == m['dap_an']['gan']
    assert sorted([list(k) for k in kq['kenh']]) == m['dap_an']['kenh']


def test_E2VC_kenh_dinh_danh(ma):
    """Đỉnh định danh nhận một kênh với điểm lớn nhất của các cạnh nó phủ (fixture-dac-ta.json#/trace_mau_S)."""
    from m1 import e2
    ma('E2VC1')
    m = tu_lap(DAP_AN_THANH_PHAN, 'E2VC1')
    kq = e2.gan_canh([tuple(c) for c in m['dau_vao']['canh_co']], che_do='VC')
    assert sorted([list(k) for k in kq['kenh']]) == m['dap_an']['kenh']


def test_E2VC_qua_25_dinh(ma):
    """S có hơn 25 đỉnh: dùng E2-C cho mọi cạnh và đếm số lần dự phòng."""
    from m1 import e2
    ma('E2VC2')
    canh = [(f'a{i}', f'b{i}', 1.0) for i in range(13)]  # 26 đỉnh
    kq = e2.gan_canh(canh, che_do='VC')
    assert kq['du_phong'] is True
    assert all(g[2] == g[1] and g[3] == 'khong_dinh_danh' for g in kq['gan'])
