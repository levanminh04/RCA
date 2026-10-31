"""Khối 12: gói sửa sau phản biện lượt 4 (dinh-chinh-cai-dat.md mục C6): điểm chính xác (S20), giá trị không hữu hạn
(S21), bat_tat (S22), π gốc E6b (S23), mốc metric (S24), map bội số (S25), bản ghi pha 2 (S26), E7 ở C-a0/C-a1 (S14),
thiếu cặp (S17). Đáp án tự lập ở fixture/dap-an-thanh-phan.json."""
import hashlib
import json
from fractions import Fraction

import pytest

from conftest import tu_lap, DAP_AN_THANH_PHAN
from test_k02_quan_sat import _params


def _ts():
    from m1 import runner
    return dict(runner.TS_HOP_DONG)


def _kenh(e, kq, d='len', ten='u'):
    from m1.kieu import Kenh
    return Kenh(e, ten, d, 'khong_lan', kq[f'e_{d}'], F_raw=kq[f'F_raw_{d}'], s_q=kq[f'e_{d}_q'], don_vi=f'x|{e}|{ten}')


# ---- S20: điểm chính xác ----

def test_SS1_phan_vi_hoa(ma):
    from m1 import e4, xep_hang
    from m1_danh_gia import rr
    m = tu_lap(DAP_AN_THANH_PHAN, 'SS1')
    ma('SS1')
    da = m['dap_an']
    a = e4.cham_phan_vi([0] * 19 + [100], [1] * 17 + [200] * 3, 5, _ts())
    b = e4.cham_phan_vi([100] * 20, [101] * 18 + [200] * 2, 5, _ts())
    assert a['F_raw_len'] == b['F_raw_len'] == 1
    assert a['e_len_q'] == b['e_len_q'] == Fraction(da['e_len_q'])
    assert (a['e_len'] == b['e_len']) is da['hai_e_len_bang_nhau']
    xh = xep_hang.xep([_kenh('A', a), _kenh('B', b)], thuc_the_co_kenh_OK={'A', 'B'})
    assert [[x['key'], x['groups'][0]] for x in xh['blocks']] == da['blocks']
    assert rr.rr_ca(xh['blocks'], m['dau_vao']['root']) == Fraction(da['RR_A'])


@pytest.mark.parametrize('T', ['590,310', '610,290', '7,3', '600,300'])
def test_SS2_dem_hoa(T, ma):
    from m1 import e4, xep_hang
    m = tu_lap(DAP_AN_THANH_PHAN, 'SS2')
    ma(f'SS2-{T}')
    da = m['dap_an']
    T_N, T_A = (int(x) for x in T.split(','))
    (n1, a1), (n2, a2) = m['dau_vao']['don_vi']
    x = e4.cham_dem(n1, a1, T_N, T_A, _ts())
    y = e4.cham_dem(n2, a2, T_N, T_A, _ts())
    assert x['F_raw_len'] == y['F_raw_len'] == 1
    assert x['e_len_q'] == y['e_len_q'] == Fraction(da['e_len_q'][T])
    assert (x['e_len'] == y['e_len']) is da['hai_e_len_bang_nhau']
    xh = xep_hang.xep([_kenh('A', x), _kenh('B', y)], thuc_the_co_kenh_OK={'A', 'B'})
    assert (len(xh['blocks']) == 1) is da['mot_khoi']


def test_SS3_tong_chinh_xac(ma):
    from m1 import xep_hang
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_THANH_PHAN, 'SS3')
    ma('SS3')
    d, da = m['dau_vao'], m['dap_an']
    ks = [Kenh(e, f'k{i}', 'len', 'khong_lan', float(Fraction(v)), s_q=Fraction(v), don_vi=f'x|{e}|{i}')
          for e in ('A', 'B') for i, v in enumerate(d[e])]
    for e in ('A', 'B'):
        K = xep_hang.khoa_q([k for k in ks if k.thuc_the == e])
        assert K == (Fraction(da['K'][0]), da['K'][1], Fraction(da['K'][2]))
    xh = xep_hang.xep(ks, thuc_the_co_kenh_OK={'A', 'B'})
    assert (len(xh['blocks']) == 1) is da['mot_khoi']


# ---- S21: giá trị không hữu hạn ----

def test_T4C1_log_huu_han(ma):
    import math
    from m1 import e4
    m = tu_lap(DAP_AN_THANH_PHAN, 'T4C1')
    ma('T4C1')
    for c, v in zip(m['dau_vao']['ca'], m['dap_an']['m']):
        r = e4.m_T4c_phan_vi(c['N'], c['A'])
        assert math.isfinite(r) and abs(r - v) <= 1e-9


def _ca_metric(N, A, **them):
    t = 1000
    rows = [{'time': t - 200 + 5 * i, 'S_cpu': v} for i, v in enumerate(N)] + \
           [{'time': t + 5 + 5 * i, 'S_cpu': v} for i, v in enumerate(A)]
    p = _params(nguon_metric={'S_cpu': 'S'}, thoi_gian_nguon={'S': 'metrics.time'}, **them)
    p['coverage'] = dict(p['coverage'], S={'khoang': [[0, 2000 * 10 ** 9]], 'r_ns': 10 ** 9})
    return rows, p


def test_Z1_nhanh_z_khong_huu_han(ma):
    from m1 import chuoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'Z1')
    ma('Z1')
    da = m['dap_an']
    rows, p = _ca_metric([-1e308] * 20, [1e308] * 20, nhanh_z=True)
    r = chuoi.chay([], rows, [], ['S'], {}, 1000, p)
    assert r['extra']['kenh_co'] == da['kenh_co']
    assert r['verdict'] == da['verdict']
    try:  # C7: phép cũ `json.dumps(...) is not None` luôn đúng
        json.dumps(r, allow_nan=False)
        json_chuan = True
    except ValueError:
        json_chuan = False
    assert json_chuan is da['json_chuan']


def test_Z1_ban_ghi_khong_ghi_duoc_la_ERROR(ma, monkeypatch):
    """Bản ghi có giá trị không ghi được JSON chuẩn thì chuỗi trả ERROR, không để pha 1 dừng (S21)."""
    from m1 import chuoi, e4
    ma('Z1-ERROR')
    rows, p = _ca_metric([0.0] * 20, [10.0] * 20)
    monkeypatch.setattr(e4, 'm_T4c_phan_vi', lambda N, A: float('inf'))
    r = chuoi.chay([], rows, [], ['S'], {}, 1000, p)
    assert r['status'] == 'ERROR' and 'JSON' in r['error']


# ---- S22: bat_tat ----

def test_BT1_bat_tat(ma):
    from m1 import chuoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'BT1')
    ma('BT1')
    sua = [lambda b: None, lambda b: b.update(E1='typo'), lambda b: b.pop('E5'), lambda b: b.update(E5='false'),
           lambda b: b.update(E6='c'), lambda b: b.update(E3=1), lambda b: b.update(E7=False)]
    rows, _ = _ca_metric([0.0] * 20, [10.0] * 20)
    ra = []
    for f in sua:
        _, p = _ca_metric([0.0] * 20, [10.0] * 20)
        f(p['bat_tat'])
        ra.append(chuoi.chay([], rows, [], ['S'], {}, 1000, p)['status'])
    assert ra == m['dap_an']['status']


# ---- S23: π gốc ----

def test_PI1_pi_goc(ma):
    from m1 import chuoi
    import sinh_trace_S
    from test_k08_e5_e6_e7_e9 import _ca_km3
    m = tu_lap(DAP_AN_THANH_PHAN, 'PI1')
    ma('PI1')
    p = sinh_trace_S.params({'E5': True, 'E6': 'b'})
    r = chuoi.chay(_ca_km3('cpu'), [], [], ['S', 'B'], {}, 1000, p)
    pi = r['extra']['E6b_pi']
    assert (set(pi) == {'P', 'S_lo', 'S_hi'} and all(pi.values())) is m['dap_an']['E6b_pi_co_ca_ba_the_gioi']
    # làm tròn 12 chữ số có nghĩa theo đặc tả, không gọi hàm của code (C7)
    khop = all(b['key'][0] == float(f"{pi['P'][e]:.12g}") for b in r['blocks'] for e in b['groups'][0])
    assert khop is m['dap_an']['pi_lam_tron_khop_key']


# ---- S24: mốc metric ----

def test_MET3_moc_lech_so_hang(ma):
    from m1 import chuoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'MET3')
    ma('MET3')
    rows, p = _ca_metric([0.0] * 5, [10.0] * 5)
    p['thoi_gian_nguon'] = {'S': [r['time'] * 10 ** 9 for r in rows[:5]]}
    p['don_vi_thoi_gian'] = dict(p['don_vi_thoi_gian'])
    assert chuoi.chay([], rows, [], ['S'], {}, 1000, p)['status'] == m['dap_an']['status']


# ---- S25: map bội số ----

def test_BS1_map_boi_so(ma):
    from m1_danh_gia import rr, uv6
    m = tu_lap(DAP_AN_THANH_PHAN, 'BS1')
    ma('BS1')
    d, da = m['dau_vao'], m['dap_an']
    RR = {k: Fraction(v) for k, v in d['RR'].items()}
    assert rr.mrr(RR, trong_so=d['bien_the']['du']) == Fraction(da['du_MRR'])
    with pytest.raises(ValueError):
        rr.mrr(RR, trong_so=d['bien_the']['thua'])
    with pytest.raises(ValueError):
        rr.rr_o(RR, {'a': 'o1', 'b': 'o2'}, d['bien_the']['thua'])
    ca = [{'dataset': 'RE2-TT', 'loai_loi': 'cpu', 'hit1_tat': 1, 'hit1_bat': 0, 'hang_tat': 1, 'hang_bat': 2,
           'trong_so': 2},
          {'dataset': 'RE2-TT', 'loai_loi': 'cpu', 'hit1_tat': 1, 'hit1_bat': 1, 'hang_tat': 1, 'hang_bat': 1}]
    with pytest.raises(ValueError):
        uv6.dem(ca)


def test_BS1_luat_c_map_thua(ma):
    from m1_danh_gia import luat_c
    ma('BS1-luat-c')
    ds = [{'ma': 'a', 'dataset': 'RE2-TT', 'o': 'o1'}, {'ma': 'b', 'dataset': 'RE2-TT', 'o': 'o2'}]
    tat = {'a': Fraction(1, 2), 'b': Fraction(1, 2)}
    bat = {'a': Fraction(1), 'b': Fraction(0)}
    with pytest.raises(ValueError):
        luat_c.ap_dung(ds, tat, bat, {'o1', 'o2'}, thanh_phan='X', trong_so={'a': 2})
    kq = luat_c.ap_dung(ds, tat, bat, {'o1', 'o2'}, thanh_phan='X', trong_so={'a': 2, 'b': 0})
    assert kq['dMRR']['gop'] == Fraction(1, 2)


# ---- S26: bản ghi pha 2 ----

def _pha1(tmp_path, recs, so=None):
    du_lieu = (''.join(json.dumps(r, sort_keys=True) + '\n' for r in recs)).encode('utf-8')
    (tmp_path / 'ban-ghi.jsonl').write_bytes(du_lieu)
    h = hashlib.sha256(du_lieu).hexdigest()
    meta = {'tep': 'ban-ghi.jsonl', 'sha256': h, 'so_ban_ghi': len(recs) if so is None else so}
    (tmp_path / 'pha1.json').write_text(json.dumps(meta), encoding='utf-8')
    return h


@pytest.mark.parametrize('bien_the', [0, 1, 2, 3])
def test_P2D_ban_ghi_pha2(bien_the, ma, tmp_path):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'P2D')
    ma(f'P2D-{bien_the}')
    b = [{'key': [1.0], 'groups': [['R']]}]
    rec = lambda c, o: {'config_id': c, 'opaque_id': o, 'status': 'OK', 'verdict': 'CAUSE_FOUND', 'blocks': b,
                        'worlds': {w: {'blocks': b} for w in ('S_lo', 'S_hi')}, 'extra': {'G_N': []}}
    du = [rec(c, o) for c in ('C1', 'C2') for o in ('x', 'y')]
    recs, so = {0: (du, None), 1: (du + [rec('C1', 'x')], None), 2: (du[:3], None), 3: (du, 99)}[bien_the]
    h = _pha1(tmp_path, recs, so)
    nhan = {o: {'root': 'R', 'dataset': 'RE2-TT', 'o': o} for o in ('x', 'y')}
    try:
        pha2.cham(tmp_path, h, nhan)
        kq = 'OK'
    except pha2.LoiDuLieuPha2:
        kq = 'LoiDuLieuPha2'
    assert kq == m['dap_an']['ket_qua'][bien_the]


# ---- S14: E7 ở C-a0/C-a1 ----

@pytest.mark.parametrize('i', [0, 1, 2])
def test_CA0E7_khong_vung(i, ma):
    from m1 import chuoi
    import sinh_trace_S
    from test_k08_e5_e6_e7_e9 import _ca_km3
    m = tu_lap(DAP_AN_THANH_PHAN, 'CA0E7')
    dc = m['dau_vao']['doi_chung'][i]
    ma(f'CA0E7-{dc}')
    p = sinh_trace_S.params({'E5': False})
    if dc:
        p['doi_chung'] = dc
    r = chuoi.chay(_ca_km3('cpu'), [], [], ['S', 'B'], {}, 1000, p)
    assert r['status'] == 'OK'
    assert (r['region'] is None) is m['dap_an']['region_none'][i]


def test_CA0E7_doi_chung_la_va_runner(ma):
    from m1 import chuoi, runner
    import sinh_trace_S
    from test_k08_e5_e6_e7_e9 import _ca_km3
    m = tu_lap(DAP_AN_THANH_PHAN, 'CA0E7')
    ma('CA0E7-la-runner')
    p = sinh_trace_S.params({})
    p['doi_chung'] = 'X'
    assert chuoi.chay(_ca_km3('cpu'), [], [], ['S', 'B'], {}, 1000, p)['status'] == m['dap_an']['doi_chung_la']
    ch = {'config_id': 'T13-C-a0', 'bat_tat': dict(runner.R0), 'tham_so_E4': dict(runner.TS_HOP_DONG),
          'doi_chung': 'C-a0', 'chay_M1': True}
    assert (runner._params(ch, {}).get('doi_chung') == 'C-a0') is m['dap_an']['runner_truyen_doi_chung']


# ---- S17: thiếu cặp ----

def test_CK9_thieu_cap(ma):
    from m1_danh_gia import chon_khoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'CK9')
    ma('CK9')
    d = m['dau_vao']
    loi = {'ValueError': ValueError}[m['dap_an']['ket_qua']]  # C7: không tự so đáp án với chính nó
    with pytest.raises(loi, match='thiếu cặp'):
        chon_khoi.chon(d['thanh_phan'], it_ca=[], do_thi=['E1'], MRR={k: Fraction(v) for k, v in d['MRR'].items()},
                       cap=d['cap'])
