"""Hồi quy điểm nối cũ và vế N1: so toàn bộ cấu trúc, có phản ví dụ ở biên."""
import copy
from fractions import Fraction as F

import pytest

from m1_danh_gia import luat_c, moc_gia, pha2, rr
import luat_c_t047 as lc
from conftest import ce_rec, pair_data


OLD = [((0, 30), (4, 30)), ((0, 30), (3, 30)), ((27, 30), (30, 30)), ((0, 0), (0, 0))]


@pytest.mark.parametrize('tp,special', [('E1', False), ('E3', False), ('E3', True), ('E5', False),
                                        ('E5', True), (luat_c.NHIEU_THANH_PHAN, True)])
@pytest.mark.parametrize('old', OLD)
@pytest.mark.parametrize('pattern', ['worlds', 'flat'])
def test_wrapper_cu_toan_bo(tp, special, old, pattern):
    kq, a, b = pair_data(tp, special, pattern)
    ex = {f'cell{i}' for i in range(8)}
    weights = {f'fake{i:02}': [2, 0, 1, 1, 3, 1, 1, 1][i // 2] for i in range(16)}
    before = copy.deepcopy(kq)
    ve = moc_gia.ve_tu_dem(*old)
    expected = pha2.ket_cuc_cap(kq, a, b, ex, tp, 'khoi_K', moc_gia=old, trong_so=weights,
                               delta_d_co_dinh=lc.DD)
    actual = lc._cap_voi_ve(kq, a, b, ex, tp, 'khoi_K', ve, weights, lc.DD)
    assert actual == expected  # gồm khong_moc_gia, ket_hop, toàn bộ từng thế giới/bao_kem
    assert kq == before
    for x in actual['theo_the_gioi'].values():
        assert x['ly_do_hai_rieng'].count('M_cong_M_phay') <= 1
    if special and tp == 'E5':
        assert actual['theo_the_gioi']['P']['dieu_kien_E5'] == 'HAI'
    if special and tp == 'E3':
        # P có sửa lỗi mã, S_hi không có sửa; UV-6 phải phân biệt thế giới.
        assert actual['theo_the_gioi']['S_hi']['UV6'] == 'HAI'
    if tp == luat_c.NHIEU_THANH_PHAN:
        assert all(x['dieu_kien_E5'] == x['UV6'] == 'KHONG_AP' for x in actual['theo_the_gioi'].values())


@pytest.mark.parametrize('pattern', ['help', 'harm', 'flat', 'worlds'])
@pytest.mark.parametrize('old', OLD)
def test_gan_ve_cu_bang_ap_dung_truc_tiep(pattern, old):
    kq, a, b = pair_data(pattern=pattern)
    ca = kq['cau_hinh'][a]['ca']
    ds = [{'ma': o, 'dataset': c['dataset'], 'o': c['o']} for o, c in ca.items()]
    ex = {f'cell{i}' for i in range(6)}
    for w in lc.WORLDS:
        tat = {o: c['theo_the_gioi'][w]['RR'] for o, c in ca.items()}
        bat = {o: c['theo_the_gioi'][w]['RR'] for o, c in kq['cau_hinh'][b]['ca'].items()}
        base = luat_c.ap_dung(ds, tat, bat, ex, 'E1', delta_d_co_dinh=lc.DD)
        got = lc._gan_ve(base, moc_gia.ve_tu_dem(*old))
        assert got == luat_c.ap_dung(ds, tat, bat, ex, 'E1', moc_gia=old, delta_d_co_dinh=lc.DD)


def test_the_gioi_khac_va_M_khong_lap():
    kq, a, b = pair_data()
    result = lc._cap_voi_ve(kq, a, b, {f'cell{i}' for i in range(8)}, 'E1', 'khoi_K',
                           moc_gia.ve_tu_dem((0, 30), (0, 30)), delta_d_co_dinh=lc.DD)
    assert result['ket_hop']['theo_the_gioi'] == {'P': 'GIUP', 'S_lo': 'HAI', 'S_hi': 'KHONG_TAC_DUNG'}
    assert result['ket_hop']['phu_thuoc_quan_sat'] is True
    assert result['theo_the_gioi']['S_lo']['ly_do_hai_rieng'] == ['M_cong_M_phay']


@pytest.mark.parametrize('total,expected', [(29, 'KHONG_KICH_HOAT'), (30, 'KHONG_KICH_HOAT'), (31, 'HAI')])
def test_n1_strict_bien_30(total, expected):
    a = {str(i): ce_rec(1) for i in range(30)}  # V0 luôn CAUSE_FOUND, không dùng luật trần cũ
    b = copy.deepcopy(a)
    b['0'] = ce_rec(1 + total)
    ve = lc.ve_n1(a, b)
    assert ve['ve'] == expected and ve['tang'] == F(total, 30)
    assert ve['trung_binh_tat'] == 1 and ve['trung_binh_bat'] == 1 + F(total, 30)
    assert ve['n'] == 30 and ve['so_bi_loai'] == 0


@pytest.mark.parametrize('h,total,expected', [(F(1, 2), 15, 'KHONG_KICH_HOAT'), (F(1, 2), 16, 'HAI'),
                                           (F(2), 60, 'KHONG_KICH_HOAT'), (F(2), 61, 'HAI')])
def test_bien_do_nhay(h, total, expected):
    a = {str(i): ce_rec(0) for i in range(30)}
    b = copy.deepcopy(a); b['0'] = ce_rec(total)
    assert lc.ve_n1(a, b, h=h)['ve'] == expected


def test_loai_cap_trong_so_va_mau_so_khong():
    a = {'a': ce_rec(2), 'b': ce_rec(0), 'c': ce_rec(0, True), 'd': ce_rec(0)}
    b = {'a': ce_rec(5), 'b': ce_rec(30), 'c': ce_rec(10), 'd': ce_rec(0, True)}
    got = lc.ve_n1(a, b, {'a': 3, 'b': 0, 'c': 2, 'd': 4})
    assert got['n'] == 3 and got['tang'] == 3 and got['trung_binh_tat'] == 2
    assert got['trung_binh_bat'] == 5 and got['so_cua_so_hop_le'] == 2
    assert got['so_bi_loai'] == 2 and got['boi_so_bi_loai'] == 6
    assert [x['ly_do'] for x in got['cua_so']] == [None, None, 'INSUFFICIENT_EVIDENCE', 'INSUFFICIENT_EVIDENCE']
    for weights in ({'a': 0, 'b': 0, 'c': 3, 'd': 1},):
        empty = lc.ve_n1(a, b, weights)
        assert empty['ve'] == 'CHUA_KIEM_DUOC' and empty['n'] == 0
        assert empty['tang'] is empty['trung_binh_tat'] is empty['trung_binh_bat'] is None
    assert lc.ve_n1({'x': ce_rec(0, True)}, {'x': ce_rec(0)})['ve'] == 'CHUA_KIEM_DUOC'
    assert lc.ve_n1({'x': ce_rec(0)}, {'x': ce_rec(0)})['tang'] == 0


@pytest.mark.parametrize('bad', [0.1, True, '1'])
def test_h_phai_chinh_xac(bad):
    with pytest.raises(TypeError):
        lc.ve_n1({'x': ce_rec()}, {'x': ce_rec()}, h=bad)


@pytest.mark.parametrize('bad', [True, -1, F(1, 2), 1.0, '2'])
def test_boi_so_sai(bad):
    with pytest.raises(ValueError):
        lc.ve_n1({'x': ce_rec()}, {'x': ce_rec()}, {'x': bad})


@pytest.mark.parametrize('bad', [
    {'status': 'ERROR'}, {'status': 'UNSUPPORTED'}, {'status': 'OTHER'}, {},
    {'status': 'OK', 'verdict': 'CAUSE_FOUND', 'extra': {}},
    {'status': 'OK', 'verdict': 'CAUSE_FOUND', 'extra': {'tang_P': {}}},
    {'status': 'OK', 'verdict': 'NO_INTRINSIC_ANOMALY', 'extra': {'tang_P': {'e': 1}}},
    {'status': 'OK', 'verdict': 'INSUFFICIENT_EVIDENCE', 'extra': {'tang_P': {'e': True}}},
    {'status': 'OK', 'verdict': 'INSUFFICIENT_EVIDENCE', 'extra': {'tang_P': {'e': 4}}}])
def test_ce_loi_khong_thanh_0_ke_ca_w0(bad):
    with pytest.raises(ValueError):
        lc.ve_n1({'x': bad}, {'x': ce_rec()}, {'x': 0})


def test_tap_cap_va_map_thieu_bi_chan():
    for a, b, weights in [({}, {}, None), ({'a': ce_rec()}, {'b': ce_rec()}, None),
                           ({'x': ce_rec()}, {'x': ce_rec()}, {})]:
        with pytest.raises(ValueError):
            lc.ve_n1(a, b, weights)


def test_ce_hai_dung_o_buoc1_truoc_cac_ve_thu_hang():
    kq, a, b = pair_data(pattern='help')
    ce = {a: {'x': ce_rec(0)}, b: {'x': ce_rec(2)}}
    got = lc.ket_cuc_cap(kq, a, b, {f'cell{i}' for i in range(8)}, 'E1', ce)
    assert got['khong_moc_gia'] == {w: 'GIUP' for w in lc.WORLDS}
    for w in lc.WORLDS:
        g = got['theo_the_gioi'][w]
        assert (g['ket_cuc'], g['buoc'], g['ly_do_hai_rieng']) == ('HAI', 1, ['moc_gia'])
        assert g['bao_kem']['ket_cuc_delta_0005'] == g['bao_kem']['ket_cuc_delta_002'] == 'HAI'
    assert got['ket_hop']['can_cu_loai'] is True


def test_cap_sai_giu_kiem_cua_pha2():
    kq, a, b = pair_data()
    ce = {a: {'x': ce_rec()}, b: {'x': ce_rec()}}
    with pytest.raises(ValueError, match='thanh_phan'):
        lc.ket_cuc_cap(kq, a, b, {'cell0'}, 'E5', ce)


@pytest.mark.parametrize('scenario,expected,step', [('dataset', 'TRAI_CHIEU_DATASET', 2),
    ('hai_gop', 'HAI', 3), ('it_ca', 'KHONG_DU_CA', 4), ('giup', 'GIUP', 5),
    ('phang', 'KHONG_TAC_DUNG', 6), ('trai_o', 'TRAI_CHIEU_O', 7)])
def test_gan_giu_cac_buoc_thu_hang(scenario, expected, step):
    ds = [{'ma': str(i), 'dataset': 'RE2-TT' if i < 4 else 'Nezha-OB', 'o': str(i)} for i in range(8)]
    tat = {str(i): F(1, 2) for i in range(8)}
    delta = {
        'dataset': [F(1, 3)] * 4 + [-F(1, 3)] * 4,
        'hai_gop': [-F(1, 10)] * 4 + [F(1, 100)] * 4,
        'it_ca': [F(1, 10)] * 8, 'giup': [F(1, 10)] * 8,
        'phang': [F(1, 200)] * 8,
        'trai_o': [-F(1, 1000)] * 6 + [F(1, 10)] * 2}[scenario]
    bat = {str(i): tat[str(i)] + delta[i] for i in range(8)}
    ex = set(tat) if scenario != 'it_ca' else {'0'}
    base = luat_c.ap_dung(ds, tat, bat, ex)
    assert (base['ket_cuc'], base['buoc']) == (expected, step)
    unchanged = lc._gan_ve(base, moc_gia.ve_tu_dem((0, 30), (0, 30)))
    assert unchanged == luat_c.ap_dung(ds, tat, bat, ex, moc_gia=((0, 30), (0, 30)))
    harm = lc._gan_ve(base, moc_gia.ve_tu_dem((0, 30), (4, 30)))
    assert harm == luat_c.ap_dung(ds, tat, bat, ex, moc_gia=((0, 30), (4, 30)))
    assert harm['buoc'] == 1
