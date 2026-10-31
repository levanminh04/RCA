"""Khối 13: gói sửa sau phản biện lượt 5 (dinh-chinh-cai-dat.md mục C7): đủ cấu hình cho luật chọn khối (G1), số chính
xác ở luật C (G2), E_X và mã ca (G3), nhãn thành phần của cặp (G4), bước 8 với thành phần không ít ca (G5, Q1), mã nội
dung (G6), trùng mã đơn vị (S27), phạm vi verdict (S28), ngưỡng E4 (S29), NEW_OP/STOPPED (S30), khóa params (S31), E1-CP
(S32), báo kèm khi chưa áp mốc giả (S33); ca biên cho các đột biến sống sót của lượt 5. Đáp án tự lập ở
fixture/dap-an-thanh-phan.json."""
import hashlib
import itertools
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from conftest import tu_lap, DAP_AN_THANH_PHAN

KHOI_K = ('E1', 'E2', 'E3', 'E5')


def _q(x):
    return Fraction(x)


def _du_cap(thanh_phan, mac_dinh):
    """Mọi cặp (R0, c) và (c bỏ x, c) của 2^n cấu hình, cùng một kết cục."""
    from m1_danh_gia import chon_khoi
    cap = {}
    for r in range(1, len(thanh_phan) + 1):
        for s in itertools.combinations(thanh_phan, r):
            c = chon_khoi.ten(set(s), thanh_phan)
            cap[f'R0|{c}'] = mac_dinh
            for x in s:
                cap[f'{chon_khoi.ten(set(s) - {x}, thanh_phan)}|{c}'] = mac_dinh
    return cap


def _du_mrr(thanh_phan, mac_dinh):
    from m1_danh_gia import chon_khoi
    return {chon_khoi.ten(set(s), thanh_phan): _q(mac_dinh)
            for r in range(len(thanh_phan) + 1) for s in itertools.combinations(thanh_phan, r)}


# ---- G1: luật chọn khối ----

@pytest.mark.parametrize('i', range(6))
def test_CK10_du_cau_hinh(i, ma):
    from m1_danh_gia import chon_khoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'CK10')
    d, da = m['dau_vao'], m['dap_an']
    ma(f'CK10-{i}')
    MRR = {k: _q(v) for k, v in d['MRR'].items()}
    cap, it_ca, do_thi = dict(d['cap']), list(d['it_ca']), list(d['do_thi'])
    if i == 0:
        kq = chon_khoi.chon(d['thanh_phan'], it_ca, do_thi, MRR, cap)
        assert {k: kq[k] for k in ('co_dinh', 'loai_luot_hai', 'chon')} == da['du']
        return
    if i == 1:
        MRR.pop('E1+E3')
        cap = {k: v for k, v in cap.items() if not k.endswith('|E1+E3')}
    elif i == 2:
        it_ca = 'E3'
    elif i == 3:
        it_ca = ['E3b']
    elif i == 4:
        do_thi = ['E2']
    if i == 5:
        cap.pop('E3|E1+E3')
        with pytest.raises(ValueError):
            chon_khoi.kiem_cau_hinh_thang('E1+E3', d['thanh_phan'], cap, it_ca)
        return
    assert da['bien_the_khac'] == 'ValueError'
    with pytest.raises(ValueError):
        chon_khoi.chon(d['thanh_phan'], it_ca, do_thi, MRR, cap)


# ---- G2, G3: luật C ----

def _ds_LC1():
    ds = [{'ma': f'r{j}', 'dataset': 'RE2-TT', 'o': f'or{j}'} for j in range(1, 31)] + \
         [{'ma': f'n{j}', 'dataset': 'Nezha-OB', 'o': f'on{j}'} for j in range(1, 23)]
    tat = {c['ma']: Fraction(1 if c['ma'] in ('n1', 'n2') else 0) for c in ds}
    bat = {c['ma']: Fraction(1 if c['ma'] == 'r1' else 0) for c in ds}
    return ds, tat, bat


def test_LC1_so_chinh_xac(ma):
    from m1_danh_gia import luat_c, rr, uv6
    m = tu_lap(DAP_AN_THANH_PHAN, 'LC1')
    da = m['dap_an']
    ma('LC1')
    ds, tat, bat = _ds_LC1()
    E_X = {c['o'] for c in ds}
    dd = {k: _q(v) for k, v in m['dau_vao']['delta_d'].items()}
    kq = luat_c.ap_dung(ds, tat, bat, E_X, thanh_phan='X', delta_d_co_dinh=dd)
    assert kq['dMRR'] == {k: _q(v) for k, v in da['dMRR'].items()}
    assert (kq['P'], kq['M'], kq['ket_cuc'], kq['buoc']) == (da['P'], da['M'], da['ket_cuc'], da['buoc'])
    with pytest.raises(TypeError):
        luat_c.ap_dung(ds, tat, bat, E_X, thanh_phan='X', delta_d_co_dinh={'RE2-TT': 1 / 30, 'Nezha-OB': 1 / 22})
    with pytest.raises(TypeError):
        luat_c.ap_dung(ds, tat, dict(bat, r1=1.0), E_X, thanh_phan='X', delta_d_co_dinh=dd)
    for w in ('2', 2.5, True, -1):
        with pytest.raises(ValueError):
            rr.boi_so({'a': w}, 'a')
    ca = [{'dataset': 'RE2-TT', 'loai_loi': None, 'hit1_tat': Fraction(1), 'hit1_bat': Fraction(0),
           'hang_tat': None, 'hang_bat': None}]
    with pytest.raises(ValueError):
        uv6.dem([dict(ca[0], trong_so=0.5)])
    with pytest.raises(TypeError):
        uv6.dem([dict(ca[0], hit1_bat=0.5)])


@pytest.mark.parametrize('bien_the', [None, 0, 1, 2])
def test_LC2_E_X_va_ma_ca(bien_the, ma):
    from m1_danh_gia import luat_c
    m = tu_lap(DAP_AN_THANH_PHAN, 'LC2')
    da = m['dap_an']
    ma(f'LC2-{bien_the}')
    ds = [{'ma': f'c{i}', 'dataset': 'RE2-TT', 'o': i} for i in range(8)]
    tat = {c['ma']: Fraction(1, 2) for c in ds}
    bat = {c['ma']: Fraction(1) for c in ds}
    E_X = set(m['dau_vao']['E_X'])
    if bien_the is None:
        kq = luat_c.ap_dung(ds, tat, bat, E_X, thanh_phan='X')
        assert (kq['ket_cuc'], kq['buoc'], kq['P'], kq['M']) == (da['ket_cuc'], da['buoc'], da['P'], da['M'])
        return
    if bien_the == 0:
        E_X = {str(o) for o in E_X}
    elif bien_the == 1:
        E_X = 'o1'
    else:
        ds = ds + [dict(ds[0])]
    assert da['bien_the'] == 'ValueError'
    with pytest.raises(ValueError):
        luat_c.ap_dung(ds, tat, bat, E_X, thanh_phan='X')


# ---- G4: nhãn thành phần của cặp ----

@pytest.mark.parametrize('i', range(7))
def test_P2K_nhan_thanh_phan(i, ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'P2K')
    a, b, tp = m['dau_vao']['bien_the'][i]
    ma(f'P2K-{i}')
    ca = lambda h: {'o1': {'dataset': 'Nezha-OB', 'o': 'c1', 'loai_loi': 'exception', 'verdict': 'CAUSE_FOUND',
                           'theo_the_gioi': {w: {'RR': Fraction(h), 'hit1': Fraction(h), 'hang': Fraction(1),
                                                 'M5': False} for w in pha2.WORLDS}}}
    kq = {'cau_hinh': {a: {'ca': ca(1)}, b: {'ca': ca(0)}}}
    mong = m['dap_an']['ket_qua'][i]
    if mong == 'ValueError':
        with pytest.raises(ValueError):
            pha2.ket_cuc_cap(kq, a, b, set(m['dau_vao']['E_X']), tp, 'khoi_K')
        return
    r = pha2.ket_cuc_cap(kq, a, b, set(m['dau_vao']['E_X']), tp, 'khoi_K')['theo_the_gioi']['P']
    assert [r['ket_cuc'], r['buoc'], r['UV6']] == mong


# ---- G5: bước 8 với thành phần không ít ca ---- (CK8 ở test_k11_danh_gia.py)

# ---- G6: mã nội dung ----

def test_MND1_ma_noi_dung(ma):
    from m1 import runner
    from conftest import T043, _doc
    m = tu_lap(DAP_AN_THANH_PHAN, 'MND1')
    da = m['dap_an']
    ma('MND1')
    mt = runner.ap_dinh_chinh(_doc(T043 / 'ma-tran-thu.json'))
    ch = runner.sinh_cau_hinh(mt, dict(m['dau_vao']['thang']), dict(runner.R0, E1='U'))
    theo_ma = {}
    for ds in ch.values():
        for c in ds:
            if 'ma_noi_dung' in c:
                theo_ma.setdefault(c['ma_noi_dung'], []).append(c['config_id'])
    ma_cua = {c['config_id']: c['ma_noi_dung'] for ds in ch.values() for c in ds if 'ma_noi_dung' in c}
    assert sorted(theo_ma[ma_cua['T13-C-a0']]) == da['cung_ma_T13-C-a0']
    assert sorted(theo_ma[ma_cua['T13-C-a1']]) == da['cung_ma_T13-C-a1']
    assert (ma_cua['T1-R0'] == ma_cua['K-R0']) is da['T1-R0_cung_ma_K-R0']


# ---- S27: trùng mã đơn vị ----

def _ca_KM4(op):
    rows = []
    for phia in ('N', 'A'):
        for i in range(20):
            st = (800 + i * 10 if phia == 'N' else 1010 + i * 10) * 10 ** 6
            rows.append({'traceID': f'a{phia}{i}', 'spanID': 's', 'parentSpanID': '', 'owner': 'A', 'operation': op,
                         'start_us': st, 'duration_us': 10000})
            rows.append({'traceID': f'b{phia}{i}', 'spanID': 's', 'parentSpanID': '', 'owner': 'A|x', 'operation': 'y',
                         'start_us': st + 2000, 'duration_us': 10000 if phia == 'N' else 30000})
    return rows


def test_KM4_trung_ma_don_vi(ma):
    from m1 import chuoi
    import sinh_trace_S
    m = tu_lap(DAP_AN_THANH_PHAN, 'KM4')
    da = m['dap_an']
    ma('KM4')
    r = chuoi.chay(_ca_KM4('x|y'), [], [], ['A', 'A|x'], {}, 1000, sinh_trace_S.params({}))
    assert r['status'] == da['goc'] and 'trùng' in r['error']
    r = chuoi.chay(_ca_KM4('x/y'), [], [], ['A', 'A|x'], {}, 1000, sinh_trace_S.params({}))
    assert r['status'] == da['bien_the']['status'] and r['region']['T'] == da['bien_the']['T']


# ---- S28, S29, S30, S31 ----

def test_CU1_verdict_trong_U(ma):
    from m1 import chuoi
    from test_k12_luot4 import _ca_metric
    m = tu_lap(DAP_AN_THANH_PHAN, 'CU1')
    da = m['dap_an']
    ma('CU1')
    ra = []
    for U in m['dau_vao']['inventory']:
        rows, p = _ca_metric([0.0] * 20, [0.0] * 20)
        r = chuoi.chay([], rows, [], U, {}, 1000, p)
        ra.append((r['verdict'], r['diagnostics']['so_cham_hop_le']))
    assert ra == list(zip(da['verdict'], da['so_cham_hop_le']))


def test_E4T_nguong_khong_tran(ma):
    from m1 import chuoi, e4, runner
    from test_k12_luot4 import _ca_metric
    m = tu_lap(DAP_AN_THANH_PHAN, 'E4T')
    ma('E4T')
    ng = e4.nguong([1.75e308] * 20, dict(runner.TS_HOP_DONG))
    assert ng['h'] == sys.float_info.max and (abs(ng['l']) < float('inf')) is m['dap_an']['l_huu_han']
    rows, p = _ca_metric([1.75e308] * 20, [1.75e308] * 19 + [1.0])
    assert chuoi.chay([], rows, [], ['S'], {}, 1000, p)['status'] == m['dap_an']['status']


def test_STP1_huong_cham(ma):
    from m1 import e4, runner
    m = tu_lap(DAP_AN_THANH_PHAN, 'STP1')
    d, da = m['dau_vao'], m['dap_an']
    ma('STP1')
    ra = [e4.cham_dem(nN, nA, d['T_N'], d['T_A'], dict(runner.TS_HOP_DONG), huong_cham=tuple(h))
          for nN, nA, h in d['don_vi']]
    assert [x['nhan'] for x in ra] == da['nhan']
    assert [x['F_raw_len'] for x in ra] == da['F_raw_len'] and [x['F_raw_xuong'] for x in ra] == da['F_raw_xuong']


def test_BT2_khoa_params(ma):
    from m1 import chuoi, runner
    from test_k12_luot4 import _ca_metric
    m = tu_lap(DAP_AN_THANH_PHAN, 'BT2')
    ma('BT2')
    sua = [lambda p: None, lambda p: p.update(nhanh_z='false'), lambda p: p['tham_so_E4'].pop('q_hi'),
           lambda p: p['tham_so_E4'].update(x=1)]
    ra = []
    for f in sua:
        rows, p = _ca_metric([0.0] * 20, [10.0] * 20)
        p['tham_so_E4'] = dict(p['tham_so_E4'])
        f(p)
        ra.append(chuoi.chay([], rows, [], ['S'], {}, 1000, p)['status'])
    assert ra == m['dap_an']['status']
    ch = {'config_id': 'C1', 'bat_tat': dict(runner.R0), 'tham_so_E4': dict(runner.TS_HOP_DONG)}
    with pytest.raises(ValueError):
        runner._params(ch, {'opaque_id': 'x', 'params_ca': {'doi_chung': 'C-a0'}})


# ---- S32, CP4: E1-CP ----

@pytest.mark.parametrize('k', range(6))
def test_CP3_con_long_trong_LFC(k, ma):
    from m1 import span
    m = tu_lap(DAP_AN_THANH_PHAN, 'CP3')
    d, da = m['dau_vao'], m['dap_an']
    ma(f'CP3-{k}')
    con = [tuple(c) for c in list(itertools.permutations(d['con']))[k]]
    cha = tuple(d['cha'])
    assert [list(x) for x in span.duong_gang(cha, con, d['tau'])] == da['duong_gang']
    assert span.doc_quyen_CP(cha, con, d['tau']) == da['u_CP'] and span.doc_quyen_U(cha, con) == da['u_U']


def test_CP4_bien_E1CP(ma):
    from m1 import span
    m = tu_lap(DAP_AN_THANH_PHAN, 'CP4')
    ma('CP4')
    for c, u, dg in zip(m['dau_vao']['ca'], m['dap_an']['u_CP'], m['dap_an']['duong_gang']):
        con = [tuple(x) for x in c['con']]
        assert span.doc_quyen_CP(tuple(c['cha']), con, c['tau']) == u
        assert [list(x) for x in span.duong_gang(tuple(c['cha']), con, c['tau'])] == dg


# ---- S33: báo kèm khi chưa áp mốc giả ----

def test_CE1_khong_moc_gia(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'CE1')
    da = m['dap_an']
    ma('CE1')
    ca = lambda r: {'a': {'dataset': 'RE2-TT', 'o': 'c1', 'loai_loi': None, 'verdict': 'CAUSE_FOUND',
                          'theo_the_gioi': {w: {'RR': r, 'hit1': r, 'hang': None, 'M5': False} for w in pha2.WORLDS}}}
    kq = {'cau_hinh': {'T': {'ca': ca(Fraction(1, 2))}, 'B': {'ca': ca(Fraction(1))}}}
    mg = tuple(tuple(x) for x in m['dau_vao']['moc_gia'])
    r = pha2.ket_cuc_cap(kq, 'T', 'B', {'c1'}, 'X', 'khoi_K', moc_gia=mg)
    assert all((r['theo_the_gioi'][w]['ket_cuc'], r['theo_the_gioi'][w]['buoc']) == (da['ket_cuc'], da['buoc'])
               for w in pha2.WORLDS)
    assert r['khong_moc_gia'] == {w: da['khong_moc_gia'] for w in pha2.WORLDS}
    r0 = pha2.ket_cuc_cap(kq, 'T', 'B', {'c1'}, 'X', 'khoi_K')
    assert ('khong_moc_gia' not in r0) is da['khong_co_moc_gia_thi_khong_co_truong']


@pytest.mark.parametrize('tp', ['E5', 'E3'])
def test_CE1_giu_dieu_kien_rieng(tp, ma):
    """S34 (C8): khong_moc_gia giữ M5, UV-6 của cặp, chỉ bỏ vế mốc giả."""
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'CE1')
    d, da = m['dau_vao'][f'ca_{tp}'], m['dap_an'][f'ca_{tp}']
    ma(f'CE1-{tp}')
    if tp == 'E5':
        ca = lambda r, m5: {'a': {'dataset': 'RE2-TT', 'o': 'c1', 'loai_loi': None, 'verdict': 'CAUSE_FOUND',
                                  'theo_the_gioi': {w: {'RR': r, 'hit1': r, 'hang': None, 'M5': m5}
                                                    for w in pha2.WORLDS}}}
        tat, bat = ca(Fraction(1, 2), False), ca(Fraction(1), True)
    else:
        ca = lambda h: {'a': {'dataset': 'Nezha-OB', 'o': 'c1', 'loai_loi': 'exception', 'verdict': 'CAUSE_FOUND',
                              'theo_the_gioi': {w: {'RR': h, 'hit1': h, 'hang': Fraction(1), 'M5': False}
                                                for w in pha2.WORLDS}}}
        tat, bat = ca(Fraction(1)), ca(Fraction(0))
    a, b = d['cap']
    kq = {'cau_hinh': {a: {'ca': tat}, b: {'ca': bat}}}
    r = pha2.ket_cuc_cap(kq, a, b, {'c1'}, tp, 'khoi_K', moc_gia=tuple(tuple(x) for x in d['moc_gia']))
    for w in pha2.WORLDS:
        t = r['theo_the_gioi'][w]
        assert (t['ket_cuc'], t['ly_do_hai_rieng'], t['moc_gia']['ve']) == (da['ket_cuc'], da['ly_do'], da['moc_gia'])
    assert r['khong_moc_gia'] == {w: da['khong_moc_gia'] for w in pha2.WORLDS}


# ---- ca biên luật C, mốc giả ----

def test_BC1_bien_luat_C(ma):
    from m1_danh_gia import luat_c
    m = tu_lap(DAP_AN_THANH_PHAN, 'BC1')
    ma('BC1')
    dd = {k: _q(v) for k, v in m['dau_vao']['delta_d'].items()}
    ra = []
    for c in m['dau_vao']['ca']:
        t = dict(c, dMRR={k: _q(v) for k, v in c['dMRR'].items()})
        kc = luat_c.ket_cuc_tu_tong_hop(t, delta_d={k: dd[k] for k in t['dMRR'] if k != 'gop'})
        ra.append([kc['ket_cuc'], kc['buoc']])
    assert ra == m['dap_an']['ket_cuc']


def test_BC2_P_M_trong_E_X(ma):
    from m1_danh_gia import luat_c
    m = tu_lap(DAP_AN_THANH_PHAN, 'BC2')
    d, da = m['dau_vao'], m['dap_an']
    ma('BC2')
    ds = [{'ma': a, 'dataset': b, 'o': c} for a, b, c in d['ca']]
    t = luat_c.tong_hop(ds, {k: _q(v) for k, v in d['RR_tat'].items()}, {k: _q(v) for k, v in d['RR_bat'].items()},
                        set(d['E_X']))
    assert {k: t[k] for k in ('P', 'M', 'P_phay', 'M_phay')} == da


def test_MG2_bien_moc_gia(ma):
    from m1_danh_gia import moc_gia
    m = tu_lap(DAP_AN_THANH_PHAN, 'MG2')
    ma('MG2')
    assert [moc_gia.ve_tu_dem(tuple(a), tuple(b))['ve'] for a, b in m['dau_vao']['cap']] == m['dap_an']['ve']


# ---- ca biên luật chọn khối ----

def _ca_CB(c):
    from m1_danh_gia import luat_c
    tp = c['thanh_phan']
    MRR = _du_mrr(tp, c.get('MRR_khac', '1/2'))
    MRR.update({k: _q(v) for k, v in c['MRR'].items()})
    cap = _du_cap(tp, c['cap_khac'])
    cap.update(c.get('cap', {}))
    for k, v in c.get('cap_phu_thuoc_quan_sat', {}).items():
        cap[k] = luat_c.ket_hop_the_gioi(v, 'khoi_K')
    return tp, MRR, cap


@pytest.mark.parametrize('i', range(6))
def test_CB1_luat_chon_khoi(i, ma):
    from m1_danh_gia import chon_khoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'CB1')
    da = m['dap_an']
    c = m['dau_vao']['ca'][i]
    ma(f'CB1-{i}')
    tp, MRR, cap = _ca_CB(c)
    kq = chon_khoi.chon(tp, c['it_ca'], c['do_thi'], MRR, cap)
    assert kq['chon'] == da['chon'][i]
    if i == 0:
        assert kq['loai_luot_mot'] == da['loai_luot_mot_N49']
        assert kq['cau_hinh_do_thi_tot_nhat'] == da['do_thi_tot_nhat_N49']
    if i == 5:
        assert kq['ly_do_trinh_Minh'] == da['ly_do_trinh_Minh_N48']


def test_CB1_buoc8_tat_khong_tac_dung(ma):
    from m1_danh_gia import chon_khoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'CB1')
    d = m['dau_vao']['buoc8_N47']
    ma('CB1-buoc8')
    kq = chon_khoi.kiem_cau_hinh_thang(d['thang'], d['thanh_phan'], d['cap'], d['it_ca'])
    assert {k: kq[k] for k in ('nhat_quan', 'xung_dot')} == m['dap_an']['buoc8_N47']


# ---- khóa xếp hạng ----

def test_XH1_khoa_xep_hang(ma):
    from m1 import xep_hang
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_THANH_PHAN, 'XH1')
    da = m['dap_an']
    ma('XH1')
    k = lambda e, ten, s, s_q=None: Kenh(e, ten, 'len', 'khong_lan', s, s_q=s_q)
    x = xep_hang.xep([k('A', 'u1', 0.5), k('A', 'u2', 0.5), k('B', 'u1', 0.5)], thuc_the_co_kenh_OK={'A', 'B'},
                     che_do='E6b', canh=())
    assert [b['groups'][0] for b in x['blocks']] == da['E6b']
    x = xep_hang.xep([k('A', 'u', 0.1, Fraction(1, 10)), k('B', 'u', 0.1, Fraction(1, 10) + Fraction(1, 10 ** 30))],
                     thuc_the_co_kenh_OK={'A', 'B'})
    assert [b['groups'][0] for b in x['blocks']] == da['chinh_xac'] and x['gop_khoa_ghi_ra'] == da['gop_khoa_ghi_ra']
    x = xep_hang.xep([k(e, 'u', 0.5) for e in 'ABC'], thuc_the_co_kenh_OK=set('ABC'), che_do='E6b', canh=())
    assert x['blocks'][0]['key'][0] == da['pi_3_khoa_dau'] and [b['groups'][0] for b in x['blocks']] == da['pi_3_nhom']


# ---- pha 2 ----

def _pha1(tmp_path, recs, so_ca=None):
    du_lieu = (''.join(json.dumps(r, sort_keys=True) + '\n' for r in recs)).encode('utf-8')
    (tmp_path / 'ban-ghi.jsonl').write_bytes(du_lieu)
    h = hashlib.sha256(du_lieu).hexdigest()
    meta = {'tep': 'ban-ghi.jsonl', 'sha256': h, 'so_ban_ghi': len(recs)}
    if so_ca is not None:
        meta['so_ca'] = so_ca
    (tmp_path / 'pha1.json').write_text(json.dumps(meta), encoding='utf-8')
    return h


@pytest.mark.parametrize('bien_the', [0, 1])
def test_P2D2_ban_ghi_pha2(bien_the, ma, tmp_path):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'P2D2')
    ma(f'P2D2-{bien_the}')
    b = [{'key': [1.0], 'groups': [['R']]}]
    rec = lambda c, o: {'config_id': c, 'opaque_id': o, 'status': 'OK', 'verdict': 'CAUSE_FOUND', 'blocks': b,
                        'worlds': {w: {'blocks': b} for w in ('S_lo', 'S_hi')}, 'extra': {'G_N': []}}
    du = [rec(c, o) for c in ('C1', 'C2') for o in ('x', 'y')]
    if bien_the == 0:
        h = _pha1(tmp_path, [r for r in du if (r['config_id'], r['opaque_id']) != ('C2', 'x')] + [rec('C1', 'x')])
    else:
        h = _pha1(tmp_path, du, so_ca=3)
    nhan = {o: {'root': 'R', 'dataset': 'RE2-TT', 'o': o} for o in ('x', 'y')}
    try:
        pha2.cham(tmp_path, h, nhan)
        kq = 'OK'
    except pha2.LoiDuLieuPha2:
        kq = 'LoiDuLieuPha2'
    assert kq == m['dap_an']['ket_qua'][bien_the]


# ---- E4, UV-6, E5, E9, RR ----

def test_E4B_bien_E4(ma, monkeypatch):
    from m1 import e4, runner
    m = tu_lap(DAP_AN_THANH_PHAN, 'E4B')
    da = m['dap_an']
    ma('E4B')
    ts = dict(runner.TS_HOP_DONG)
    N = [10 + 0.1 * i for i in range(20)]
    A = [1 + 0.1 * i for i in range(20)]
    co = e4.cham_phan_vi(N, A, 5, ts, huong_cham=('len', 'xuong'), cache=e4.CacheCong(), khoa_don_vi='u')
    khong = e4.cham_phan_vi(N, A, 5, ts, huong_cham=('len', 'xuong'))
    for k in ('F_raw_len', 'F_raw_xuong', 'e_len_q', 'e_xuong_q'):
        assert co[k] == khong[k], k
    assert (co['F_raw_len'], co['F_raw_xuong'], co['e_xuong_q']) == \
        (da['phan_vi']['F_raw_len'], da['phan_vi']['F_raw_xuong'], _q(da['phan_vi']['e_xuong_q']))
    for (nN, nA, TN, TA), (nhan, F) in zip(m['dau_vao']['dem'], da['dem']):
        x = e4.cham_dem(nN, nA, TN, TA, ts)
        assert (x['nhan'] if x['trang_thai'] == 'OK' else x['trang_thai'], x['F_raw_len']) == (nhan, F)
    ra, ra_pv = [], []
    for p in (ts['alpha'], 0.0099):
        monkeypatch.setattr(e4, 'p_nhi_thuc', lambda n_A, n, p0, huong, p=p: p)
        ra.append(e4.cham_dem(10, 30, 300, 300, ts)['F_raw_len'])
        monkeypatch.setattr(e4, 'p_cong', lambda A, N, huong, n_exact_max=100, p=p: (p, 'chinh_xac'))
        ra_pv.append(e4.cham_phan_vi([0.0] * 20, [10.0] * 20, 5, ts)['F_raw_len'])
    assert ra == da['p_bang_alpha'] and ra_pv == da['p_bang_alpha_phan_vi']


def test_UV6_4_sua_phan_so(ma):
    from m1_danh_gia import uv6
    m = tu_lap(DAP_AN_THANH_PHAN, 'UV6-4')
    ma('UV6-4')
    ca = [dict(c, **{k: _q(c[k]) for k in ('hit1_tat', 'hit1_bat', 'hang_tat', 'hang_bat')})
          for c in m['dau_vao']['ca']]
    kq = uv6.dem(ca)
    assert {k: kq[k] for k in ('hong', 'sua', 'vi_pham')} == m['dap_an']


def test_E5X_lan_xuoi(ma):
    from m1 import e5
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_THANH_PHAN, 'E5X')
    ma('E5X')
    kenh = [Kenh(e, ten, h, lop, 0.5) for e, ten, h, lop in m['dau_vao']['kenh']]
    p = e5.phan_loai(kenh, [tuple(c) for c in m['dau_vao']['canh']], bat=True)
    assert p['F_I'] == m['dap_an']['F_I']


def test_E9X_phu_quyet(ma):
    from m1 import e9
    m = tu_lap(DAP_AN_THANH_PHAN, 'E9X')
    d = m['dau_vao']
    ma('E9X')
    assert [e9.phu_quyet(e, B, o_s=d['o_s'], tau=d['tau'])[0] for e, B in d['ca']] == m['dap_an']['phu_quyet']
    # qua E5: mọi bên giải thích đều được xét, không chỉ bên đầu
    from m1 import e5
    from m1.kieu import Kenh
    kenh = [Kenh('e', 'k', 'len', 'lan_nguoc', 0.5, khoi_phat=0), Kenh('b1', 'k', 'len', 'khong_lan', 0.5, khoi_phat=30),
            Kenh('b2', 'k', 'len', 'khong_lan', 0.5, khoi_phat=5)]
    p = e5.phan_loai(kenh, [('e', 'b1'), ('e', 'b2')], bat=True,
                     e9={'bat': True, 'o_s': d['o_s'], 'tau': d['tau'], 'canh_E2_bat_thuong': set()})
    da = m['dap_an']['qua_E5']
    assert p['F_I']['e||k|len'] == da['F_I_e']
    assert {x['trang_thai'] for x in p['inherited_by'] if x['thuc_the'] == 'e'} == {da['trang_thai']}


def test_RR_tong_boi_so_0(ma):
    from m1_danh_gia import rr
    ma('RR0')
    with pytest.raises(ValueError):
        rr.mrr({'a': Fraction(1)}, trong_so={'a': 0})


# ---- tất định: đường E5 qua hash seed, log trùng mốc ----

MA_TD2 = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from m1 import e5
from m1.kieu import Kenh
canh = json.loads(sys.argv[2])
if sys.argv[3] == 'dao':
    canh = canh[::-1]
kenh = [Kenh('e', 'k', 'len', 'lan_nguoc', 0.5)] + [Kenh(x, 'k', 'len', 'khong_lan', 0.5) for x in ('Mk1', 'Mk2', 'm')]
if sys.argv[3] == 'dao':
    kenh = kenh[::-1]
p = e5.phan_loai(kenh, [tuple(c) for c in canh], bat=True)
print(json.dumps([x['duong'] for x in p['inherited_by'] if x['giai_thich'][0] == 'm']))
'''


def test_TD2_duong_E5_qua_hash_seed(ma):
    m = tu_lap(DAP_AN_THANH_PHAN, 'TD2')
    d = m['dau_vao']
    ma('TD2')
    src = str(Path(__file__).resolve().parents[3] / 'src')
    ra = set()
    for hs in d['hash_seed']:
        for thu_tu in ('goc', 'dao'):
            env = dict(os.environ, PYTHONHASHSEED=str(hs))
            out = subprocess.run([sys.executable, '-B', '-c', MA_TD2, src, json.dumps(d['canh']), thu_tu], env=env,
                                 capture_output=True, text=True, check=True).stdout
            ra.add(out.strip())
    assert ra == {json.dumps([m['dap_an']['duong_m']])}


def test_TD2_log_trung_moc(ma):
    from m1 import e3
    m = tu_lap(DAP_AN_THANH_PHAN, 'TD2')
    ma('TD2-log')
    dong = [{'moc': 5, 'thuc_the': 'A', 'noi_dung': 'payment failed for order 17', 'lop': None, 'severity_raw': None},
            {'moc': 5, 'thuc_the': 'A', 'noi_dung': 'cache refreshed in 3 ms', 'lop': None, 'severity_raw': None}]
    ts3 = {'khop': 'hoan_toan', 'sim_th': 0.4, 'do_sau': 4}
    ql = {'kieu': 'tu_khoa', 'tu_khoa': ['FAIL']}
    a = e3.hoc_va_dem(dong, dong, ts3, ql)
    b = e3.hoc_va_dem(dong[::-1], dong[::-1], ts3, ql)
    assert (a == b) is m['dap_an']['log_giong_nhau']


MA_TD3 = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from fractions import Fraction
import test_k13_luot5 as t
from conftest import tu_lap, DAP_AN_THANH_PHAN
from m1_danh_gia import chon_khoi, luat_c
dao = sys.argv[2] == 'dao'
ra = []
for c in tu_lap(DAP_AN_THANH_PHAN, 'CB1')['dau_vao']['ca']:
    tp, MRR, cap = t._ca_CB(c)
    if dao:
        MRR, cap = dict(reversed(list(MRR.items()))), dict(reversed(list(cap.items())))
    ra.append(chon_khoi.chon(tp, c['it_ca'], c['do_thi'], MRR, cap))
ds, tat, bat = t._ds_LC1()
if dao:
    ds = ds[::-1]
ra.append(luat_c.ap_dung(ds, tat, bat, {x['o'] for x in ds}, thanh_phan='X'))
print(json.dumps(ra, sort_keys=True, default=str))
'''


def test_TD3_bo_danh_gia_qua_hash_seed(ma):
    """Đầu ra của luật chọn khối và luật C giống hệt qua hash seed và thứ tự khóa của đầu vào (C7)."""
    ma('TD3')
    tests = str(Path(__file__).resolve().parent)
    ra = set()
    for hs in (0, 1, 2, 3):
        for thu_tu in ('goc', 'dao'):
            env = dict(os.environ, PYTHONHASHSEED=str(hs))
            ra.add(subprocess.run([sys.executable, '-B', '-c', MA_TD3, tests, thu_tu], env=env, capture_output=True,
                                  text=True, check=True, encoding='utf-8').stdout)
    assert len(ra) == 1
