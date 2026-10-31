"""Khối 14: gói sửa sau kiểm lại lượt 5 (dinh-chinh-cai-dat.md mục C8): luật chọn khối theo thế giới (S36), MRR theo bội
số và lấy mẫu ô (S37), cache cổng theo ca (S38), giá trị tham_so_E4 (S39), các vùng có đột biến sống sót của phiên kiểm
lại (S40), G_N hai cách (S41), đủ độ đo ở pha 2 (S42). S34, S35 ở test_k13_luot5.py (CE1, XH1). Đáp án tự lập ở
fixture/dap-an-thanh-phan.json."""
import json
import random
from fractions import Fraction

import numpy as np
import pytest

from conftest import tu_lap, DAP_AN_THANH_PHAN


def _q(x):
    return Fraction(x)


# ---- S36: luật chọn khối theo thế giới ----

def _cap_CW1(d):
    from m1_danh_gia import luat_c
    from test_k13_luot5 import _du_cap
    cap = {k: luat_c.ket_hop_the_gioi(d['cap_khac'], 'khoi_K') for k in _du_cap(d['thanh_phan'], None)}
    for k, v in d['cap'].items():
        cap[k] = luat_c.ket_hop_the_gioi(v, 'khoi_K')
    return cap


def test_CW1_chon_theo_the_gioi(ma):
    from m1_danh_gia import chon_khoi
    m = tu_lap(DAP_AN_THANH_PHAN, 'CW1')
    d, da = m['dau_vao'], m['dap_an']
    ma('CW1')
    cap = _cap_CW1(d)
    MRR = {k: _q(v) for k, v in d['MRR'].items()}
    ra = {w: chon_khoi.chon(d['thanh_phan'], d['it_ca'], d['do_thi'], MRR, cap, the_gioi=w)['chon']
          for w in ('P', 'S_lo', 'S_hi')}
    assert ra == da['chon']
    chuoi_cap = {k: v['ket_cuc_dung'] for k, v in cap.items()}
    for kw in ({'cap': chuoi_cap, 'the_gioi': 'S_lo'}, {'cap': cap, 'the_gioi': 'X'}):
        with pytest.raises(ValueError):
            chon_khoi.chon(d['thanh_phan'], d['it_ca'], d['do_thi'], MRR, **kw)


# ---- S37: MRR theo bội số, lấy mẫu ô ----

def test_MB1_mrr_cau_hinh(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'MB1')
    d, da = m['dau_vao'], m['dap_an']
    ma('MB1')
    ca = {o: {'dataset': ds, 'theo_the_gioi': {w: {'RR': _q(d['RR_T'][o])} for w in pha2.WORLDS}} for o, ds in d['ca']}
    kq = {'cau_hinh': {'T': {'ca': ca}}}
    assert pha2.mrr_cau_hinh(kq)['T'] == {k: _q(v) for k, v in da['khong_boi_so'].items()}
    assert pha2.mrr_cau_hinh(kq, d['boi_so'], 'S_lo')['T'] == {k: _q(v) for k, v in da['boi_so'].items()}
    with pytest.raises(ValueError):
        pha2.mrr_cau_hinh(kq, None, 'X')


def test_LM1_lay_mau_o(ma):
    from m1_danh_gia import rr
    m = tu_lap(DAP_AN_THANH_PHAN, 'LM1')
    d, da = m['dau_vao'], m['dap_an']
    ma('LM1')
    ds = [{'ma': a, 'dataset': b, 'o': c} for a, b, c in d['ca']]
    for seed in d['seed']:
        w = rr.lay_mau_o(ds, np.random.default_rng(seed))
        assert (set(w) == {c['ma'] for c in ds}) is da['du_moi_ca']
        theo_o = {}
        for c in ds:
            theo_o.setdefault((c['dataset'], c['o']), set()).add(w[c['ma']])
        assert all(len(v) == 1 for v in theo_o.values()) is da['ca_cung_o_cung_boi_so']
        tong = {}
        for (dsn, _), v in theo_o.items():
            tong[dsn] = tong.get(dsn, 0) + next(iter(v))
        assert tong == da['tong_boi_so_o']
        assert (rr.lay_mau_o(ds, np.random.default_rng(seed)) == w) is da['cung_seed_cung_mau']
        xao = list(ds)
        random.Random(seed).shuffle(xao)
        assert (rr.lay_mau_o(xao, np.random.default_rng(seed)) == w) is da['khong_phu_thuoc_thu_tu_vao']
    with pytest.raises(ValueError):
        rr.lay_mau_o(ds + [dict(ds[0])], np.random.default_rng(0))


# ---- S38: cache cổng theo ca ----

def test_RN1_cache_theo_ca(ma, tmp_path, monkeypatch):
    from m1 import chuoi, e4, runner
    import sinh_trace_S
    from conftest import FIXTURE
    m = tu_lap(DAP_AN_THANH_PHAN, 'RN1')
    da = m['dap_an']
    ma('RN1')
    ca = []
    for i, s in enumerate(('S1', 'S2'), 1):
        spans, logs = sinh_trace_S.sinh(s, t=1000, mau=FIXTURE['trace_mau_S'])
        ca.append({'opaque_id': f'gia-00{i}', 'spans': spans, 'metrics': [], 'logs': logs,
                   'inventory': ['A', 'B', 'F', 'I', 'R', 'X'], 'aliases': {}})
    moc = {c['opaque_id']: 1000 for c in ca}
    cau_hinh = [{'config_id': 'R0', 'params': sinh_trace_S.params({})},
                {'config_id': 'C1', 'params': sinh_trace_S.params({'E1': 'U'})}]
    dem = []

    class Dem(e4.CacheCong):
        def __init__(self):
            super().__init__()
            dem.append(1)
    monkeypatch.setattr(e4, 'CacheCong', Dem)
    runner.pha1(ca[::-1], moc, cau_hinh[::-1], tmp_path / 'l1')
    assert len(dem) == da['so_cache_moi']
    dong = []
    for ch in sorted(cau_hinh, key=lambda x: x['config_id']):
        for c in sorted(ca, key=lambda x: x['opaque_id']):
            chuoi.CACHE = e4.CacheCong()
            rec = chuoi.chay(c['spans'], [], c['logs'], c['inventory'], {}, 1000, runner._params(ch, c))
            dong.append(runner._json(dict(rec, opaque_id=c['opaque_id'])))
    that = (tmp_path / 'l1' / 'ban-ghi.jsonl').read_text(encoding='utf-8').splitlines()
    assert (that == dong) is da['ban_ghi_khop_tung_lan_goi']
    with pytest.raises(ValueError):
        runner.pha1(ca, moc, cau_hinh + [dict(cau_hinh[0])], tmp_path / 'l2')


# ---- S39: giá trị tham_so_E4 ----

def test_BT3_gia_tri_tham_so_E4(ma):
    from m1 import chuoi
    from test_k12_luot4 import _ca_metric
    m = tu_lap(DAP_AN_THANH_PHAN, 'BT3')
    ma('BT3')
    sua = [{}, {'alpha': True}, {'alpha': 1.5}, {'m_span': 20.0}, {'count_min': 0}, {'q_lo': 0.5, 'q_hi': 0.5},
           {'epsilon': 0.0}]
    ra = []
    for s in sua:
        rows, p = _ca_metric([0.0] * 20, [10.0] * 20)
        p['tham_so_E4'] = dict(p['tham_so_E4'], **s)
        ra.append(chuoi.chay([], rows, [], ['S'], {}, 1000, p)['status'])
    assert ra == m['dap_an']['status']


# ---- S40: vùng có đột biến sống sót của phiên kiểm lại ----

def test_MG3_moc_gia_ban_ghi_loi(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'MG3')
    da = m['dap_an']
    ma('MG3')
    kq = {'cau_hinh': {'T': {'ca': {o: {'verdict': a} for o, a, _ in m['dau_vao']['ca']}},
                       'B': {'ca': {o: {'verdict': b} for o, _, b in m['dau_vao']['ca']}}}}
    tat, bat, phu = pha2.dem_moc_gia(kq, 'T', 'B')
    assert (list(tat), list(bat), phu['bi_loai']) == (da['tat'], da['bat'], da['bi_loai'])


def test_T4C2_m_K_I_theo_F_I(ma):
    from m1 import chuoi
    import sinh_trace_S
    from test_k08_e5_e6_e7_e9 import _ca_km3
    m = tu_lap(DAP_AN_THANH_PHAN, 'T4C2')
    da = m['dap_an']
    ma('T4C2')
    r = chuoi.chay(_ca_km3('cpu'), [], [], ['S', 'B'], {}, 1000, sinh_trace_S.params(m['dau_vao']['bat_tat']))
    kS = [k for k in r['extra']['kenh_co'] if k['thuc_the'] == 'S']
    assert (bool(kS) and all(k['F_I'] == 0 for k in kS)) is da['S_chi_ke_thua']
    mS = r['extra']['T4c']['m_thuc_the']['S']
    assert mS[1] == da['m_K_I_S'] and (mS[0] > 0) is da['m_K_raw_S_duong']


def test_M5W_M5_theo_the_gioi(ma, tmp_path):
    from m1_danh_gia import pha2
    from test_k13_luot5 import _pha1
    m = tu_lap(DAP_AN_THANH_PHAN, 'M5W')
    d = m['dau_vao']
    ma('M5W')
    kh = {w: [{'key': [float(len(g) - i)], 'groups': [g]} for i, g in enumerate(bl)] for w, bl in d['blocks'].items()}
    rec = {'config_id': 'C', 'opaque_id': 'x', 'status': 'OK', 'verdict': 'CAUSE_FOUND', 'blocks': kh['P'],
           'worlds': {w: {'blocks': kh[w]} for w in ('S_lo', 'S_hi')}, 'extra': {'G_N': d['G_N']}}
    h = _pha1(tmp_path, [rec])
    kq = pha2.cham(tmp_path, h, {'x': {'root': d['root'], 'dataset': 'RE2-TT', 'o': 'o1'}})
    tw = kq['cau_hinh']['C']['ca']['x']['theo_the_gioi']
    assert {w: tw[w]['M5'] for w in pha2.WORLDS} == m['dap_an']['M5']


def _ca_E2V():
    rows = []
    for ben, nua in (('A', False), ('B', True)):
        for phia in ('N', 'A'):
            for i in range(20):
                st = (700 + i * 10 if phia == 'N' else 1010 + i * 10) * 10 ** 6 + (0 if ben == 'A' else 3 * 10 ** 6)
                g = 5000 if phia == 'N' or (nua and i % 2) else 15000
                tid = f'{ben}{phia}{i}'
                rows += [{'traceID': tid, 'spanID': 'r', 'parentSpanID': '', 'owner': ben, 'operation': 'vao',
                          'start_us': st, 'duration_us': g + 7000},
                         {'traceID': tid, 'spanID': 'w', 'parentSpanID': 'r', 'owner': ben, 'operation': 'goi',
                          'start_us': st + 1000, 'duration_us': g + 5000},
                         {'traceID': tid, 'spanID': 'c', 'parentSpanID': 'w', 'owner': 'V', 'operation': 'xu_ly',
                          'start_us': st + 1000, 'duration_us': 5000}]
    return rows


def test_E2V_canh_diem_cao_nhat(ma):
    from m1 import chuoi
    import sinh_trace_S
    m = tu_lap(DAP_AN_THANH_PHAN, 'E2V')
    da = m['dap_an']
    ma('E2V')
    r = chuoi.chay(_ca_E2V(), [], [], ['A', 'B', 'V'], {}, 1000, sinh_trace_S.params(m['dau_vao']['bat_tat']))
    k = [x for x in r['extra']['kenh_co'] if x['ten'] == da['kenh']]
    assert [(x['s'], x['don_vi']) for x in k] == [(da['s'], da['don_vi'])]


def test_WD5_theo_phan_bo(ma):
    from m1_danh_gia import the_gioi
    m = tu_lap(DAP_AN_THANH_PHAN, 'WD5')
    d, da = m['dau_vao'], m['dap_an']
    ma('WD5')
    bw = {w: [{'key': [float(10 - i)], 'groups': [g]} for i, g in enumerate(d[w])] for w in ('P', 'S_lo', 'S_hi')}
    kq = the_gioi.world_dependent(bw, d['root'])
    assert kq['WORLD_DEPENDENT'] is da['WORLD_DEPENDENT']
    assert kq['hang_ky_vong'] == {w: _q(v) for w, v in da['hang_ky_vong'].items()}


def _ca_CD3A():
    rows = []
    for i in range(20):
        st = (700 + i * 10) * 10 ** 6
        rows += [{'traceID': f'N{i}', 'spanID': 'x', 'parentSpanID': '', 'owner': 'X', 'operation': 'vao',
                  'start_us': st, 'duration_us': 30000},
                 {'traceID': f'N{i}', 'spanID': 's', 'parentSpanID': 'x', 'owner': 'S', 'operation': 'op',
                  'start_us': st + 1000, 'duration_us': 10000}]
        st = (1010 + i * 10) * 10 ** 6
        rows.append({'traceID': f'A{i}', 'spanID': 's', 'parentSpanID': '', 'owner': 'S', 'operation': 'op',
                     'start_us': st, 'duration_us': 20000})
    return rows


def test_CD3A_dich_phia_A(ma):
    from m1 import chuoi
    import sinh_trace_S
    m = tu_lap(DAP_AN_THANH_PHAN, 'CD3A')
    ma('CD3A')
    r = chuoi.chay(_ca_CD3A(), [], [], ['S', 'X'], {}, 1000, sinh_trace_S.params({}))
    assert r['extra']['doi_chung']['C-d3']['dich'] == m['dap_an']['dich']


def test_GN3_G_N_ca_hai_phia_N(ma):
    from m1 import chuoi
    import sinh_trace_S
    m = tu_lap(DAP_AN_THANH_PHAN, 'GN3')
    ma('GN3')
    t = 1000 * 10 ** 6
    rows = [{'traceID': 't1', 'spanID': 'p', 'parentSpanID': '', 'owner': 'P', 'operation': 'a',
             'start_us': t - 10 * 10 ** 6, 'duration_us': 20 * 10 ** 6},
            {'traceID': 't1', 'spanID': 'c', 'parentSpanID': 'p', 'owner': 'C', 'operation': 'b',
             'start_us': t - 9 * 10 ** 6, 'duration_us': 10 ** 6},
            {'traceID': 't2', 'spanID': 'q', 'parentSpanID': '', 'owner': 'Q', 'operation': 'a',
             'start_us': t - 20 * 10 ** 6, 'duration_us': 15 * 10 ** 6},
            {'traceID': 't2', 'spanID': 'd', 'parentSpanID': 'q', 'owner': 'D', 'operation': 'b',
             'start_us': t - 19 * 10 ** 6, 'duration_us': 10 ** 6}]
    r = chuoi.chay(rows, [], [], ['P', 'C', 'Q', 'D'], {}, 1000, sinh_trace_S.params({}))
    assert r['extra']['G_N'] == m['dap_an']['G_N']


def test_E9O_o_10_giay(ma):
    from m1 import chuoi
    from test_k12_luot4 import _ca_metric
    m = tu_lap(DAP_AN_THANH_PHAN, 'E9O')
    ma('E9O')
    rows, p = _ca_metric([0.0] * 20, [0.0, 0.0] + [10.0] * 18)
    r = chuoi.chay([], rows, [], ['S'], {}, 1000, p)
    assert [k['khoi_phat'] for k in r['extra']['kenh_co']] == [m['dap_an']['khoi_phat_ns']]


def test_E9E2B_canh_E2_hai_chieu(ma):
    from m1 import e5
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_THANH_PHAN, 'E9E2B')
    da = m['dap_an']
    ma('E9E2B')
    kenh = [Kenh('e', 'k', 'len', 'lan_nguoc', 0.5, khoi_phat=0), Kenh('b', 'k', 'len', 'khong_lan', 0.5, khoi_phat=100)]
    p = e5.phan_loai(kenh, [('e', 'b')], bat=True,
                     e9={'bat': True, 'o_s': 10, 'tau': 0.001,
                         'canh_E2_bat_thuong': {tuple(c) for c in m['dau_vao']['canh_E2_bat_thuong']}})
    assert [(x['trang_thai'], x['ly_do_E9']) for x in p['inherited_by']] == [(da['trang_thai'], da['ly_do_E9'])]


# ---- S41: G_N hai cách ----

@pytest.mark.parametrize('s', ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'])
def test_GN2_hai_cach_dung_G_N(s, ma):
    from m1 import chuoi
    from m1_danh_gia import m5
    import sinh_trace_S
    from conftest import FIXTURE
    m = tu_lap(DAP_AN_THANH_PHAN, 'GN2')
    ma(f'GN2-{s}')
    spans, logs = sinh_trace_S.sinh(s, t=1000, mau=FIXTURE['trace_mau_S'])
    r = chuoi.chay(spans, [], logs, ['A', 'B', 'F', 'I', 'R', 'X'], {}, 1000, sinh_trace_S.params({}))
    lo, hi = (1000 - 300) * 10 ** 6, (1000 + 300) * 10 ** 6
    trong = [x for x in spans if x['start_us'] >= lo and x['start_us'] + x['duration_us'] < hi]
    hai = sorted(list(c) for c in m5.G_N_tu_span(trong, 1000 * 10 ** 6))
    assert (r['extra']['G_N'] == hai) is m['dap_an']['giong_nhau']


# ---- S42: đủ độ đo ở pha 2 ----

def test_DO1_du_do_do(ma, tmp_path):
    from m1_danh_gia import pha2
    from test_k13_luot5 import _pha1
    m = tu_lap(DAP_AN_THANH_PHAN, 'DO1')
    d, da = m['dau_vao'], m['dap_an']
    ma('DO1')
    b = [{'key': [1.0], 'groups': d['blocks']}]
    rec = {'config_id': 'C', 'opaque_id': 'x', 'status': 'OK', 'verdict': 'CAUSE_FOUND', 'blocks': b,
           'worlds': {w: {'blocks': b} for w in ('S_lo', 'S_hi')}, 'extra': {'G_N': []}}
    h = _pha1(tmp_path, [rec])
    do = pha2.cham(tmp_path, h, {'x': {'root': d['root'], 'dataset': 'RE2-TT', 'o': 'o1'}})[
        'cau_hinh']['C']['ca']['x']['theo_the_gioi']['P']['do']
    for k, v in da.items():
        assert abs(do[k] - v) <= 1e-12, k
    json.dumps(pha2.ma_hoa_json(do), allow_nan=False)
