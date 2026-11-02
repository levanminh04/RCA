"""Chế độ mới cài trong src (WHY-67, WHY-69): cùng số với bản đo ở results/T-046/scripts; tất định; mặc định không đổi."""
import copy
import json

import numpy as np
import pytest

import cong as cong_do
import t046
from m1 import chuoi, cong, e4, runner

TS = {'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05, 'n_exact_max': 100}
NS = cong.NS
BAT = {'cong_phan_vi': 'G3', 'cong_dem': 'D1', 'thang': 'E4+T4c'}
CA_NEZHA = 'dev-14701a3bbb'


@pytest.mark.parametrize('seed', [1, 2, 3])
def test_p_G3_khop_ban_do(seed):
    rng = np.random.default_rng(seed)
    t = 10_000 * NS
    N = list(rng.normal(size=300).cumsum())
    A = list(rng.normal(size=300).cumsum())
    mN = [t - (i + 1) * NS + NS // 2 for i in range(300)]
    mA = [t + i * NS + NS // 2 for i in range(300)]
    lo, hi = t - 300 * NS, t + 300 * NS
    kb = cong_do.chuan_bi_khoi(N, mN, A, mA, t, lo, hi)
    for d in ('len', 'xuong'):
        p, cach = cong.p_theo_G3(N, mN, A, mA, t, lo, hi, d, TS, 'metric|a_cpu')
        if kb['roi_G0']:
            assert cach.startswith('G0:') and p == cong_do.p_G0(N, A, d, TS)[0]
        else:
            assert cach == 'G3' and p == cong_do.p_G3(kb, d, TS, 'metric|a_cpu')[0]


def test_roi_G0_khi_it_khoi():
    t = 1000 * NS
    N = [float(i % 7) for i in range(20)]
    A = [float(i % 5) for i in range(20)]
    mN = [t - (i + 1) * NS for i in range(20)]
    mA = [t + i * NS for i in range(20)]
    p, cach = cong.p_theo_G3(N, mN, A, mA, t, t - 20 * NS, t + 20 * NS, 'len', TS, 'u')
    assert cach.startswith('G0:') and p == e4.p_cong(A, N, 'len', 100)[0]


@pytest.mark.parametrize('H,F,mong', [
    (([-299, 0], [299, 0]), ((-900, 0), (900, 0)), (-300, 300)),
    (([-95, 0], [92, 0]), ((-900, 0), (900, 0)), (-100, 100)),
    (([-145, 0], [145, 0]), ((-150, 0), (147, 0)), (-150, 147)),
])
def test_bien_phia_khop_ban_do(H, F, mong):
    t = 100_000 * NS
    q = {'H': [t + H[0][0] * NS, t + H[1][0] * NS], 'F': [t + F[0][0] * NS, t + F[1][0] * NS]}
    assert cong.bien_phia(q, t) == (t + mong[0] * NS, t + mong[1] * NS)
    rec = {'coverage': {'trace': q}}
    assert t046.bien_don_vi(rec, {'nguon_metric': {}}, 'op|a|b', t) == cong.bien_phia(q, t)
    assert cong.bien_phia(None, t) == (t - 300 * NS, t + 300 * NS)


def test_D1_khop_ban_do_va_phi_1_la_nhi_thuc():
    for nN, nA, TN, TA, phi in ((50, 90, 300.0, 300.0, 1.0), (50, 90, 300.0, 300.0, 3.2), (200, 40, 280.5, 299.0, 7.5)):
        for d in ('len', 'xuong'):
            assert e4.p_D1(nN, nA, TN, TA, phi, d) == cong_do.p_D1(nN, nA, TN, TA, phi, d)
    assert e4.p_D1(50, 90, 300.0, 300.0, 1.0, 'len') == pytest.approx(e4.p_nhi_thuc(90, 140, 0.5, 'len'), rel=1e-9)
    moc = [1000 * NS - (i * 7 + 1) * NS for i in range(30)]
    assert cong.he_so_phan_tan(moc, 700 * NS, 1000 * NS) == cong_do.he_so_phan_tan(moc, 700 * NS, 1000 * NS)[0]


def test_cham_dem_phi_giu_NEW_OP_va_mac_dinh():
    ts = {'alpha': 0.01, 'count_min': 10}
    assert e4.cham_dem(0, 50, 300.0, 300.0, ts, phi_d=5.0)['nhan'] == 'NEW_OP'
    a, b = e4.cham_dem(50, 90, 300.0, 300.0, ts), e4.cham_dem(50, 90, 300.0, 300.0, ts, phi_d=1.0)
    assert a['F_raw_len'] == b['F_raw_len'] == 1
    c = e4.cham_dem(50, 90, 300.0, 300.0, ts, phi_d=20.0)
    assert c['F_raw_len'] == 0 and c['nhan'] == 'binh_thuong' and c['e_len_q'] == 0


def test_che_do_sai_la_ERROR():
    mt = t046.moi_truong()
    ca, t, _ = t046.nap('Nezha-OB', CA_NEZHA, 'that', mt)
    ch = dict(t046.cau_hinh('R0'))
    for sai in ({'cong_phan_vi': 'G3'}, dict(BAT, cong_dem='D9'), dict(BAT, them=1), 'G3'):
        p = runner._params(dict(ch, che_do={'x': 1}), ca)
        p['che_do'] = sai
        rec = chuoi.chay(ca['spans'], ca['metrics'], ca['logs'], ca['inventory'], ca['aliases'], t, p)
        assert rec['status'] == 'ERROR' and 'che_do' in rec['error']


@pytest.fixture(scope='module')
def ban_ghi():
    mt = t046.moi_truong()
    ca, t, _ = t046.nap('Nezha-OB', CA_NEZHA, 'that', mt)
    ch = t046.cau_hinh('R0')

    def chay(che_do=None):
        chuoi.CACHE = e4.CacheCong()
        p = runner._params(dict(ch, che_do=che_do) if che_do else ch, ca)
        return chuoi.chay(ca['spans'], ca['metrics'], ca['logs'], ca['inventory'], ca['aliases'], t, p)
    return chay, ca, t, ch


def test_mac_dinh_trung_T045(ban_ghi):
    chay, *_ = ban_ghi
    rec = chay()
    moc = t046.T045 if hasattr(t046, 'T045') else None
    assert rec['method_version'] == chuoi.PHIEN_BAN and 'che_do' not in rec['extra'] and moc is None
    tep = t046.ROOT / 'results/T-045/runs/b2-t1-nezha-seed0-001/ban-ghi.jsonl'
    dong = [x for x in tep.read_text(encoding='utf-8').splitlines()
            if json.loads(x)['opaque_id'] == CA_NEZHA and json.loads(x)['config_id'] == rec['config_id']]
    assert len(dong) == 1 and dong[0] == t046.json_ban_ghi(rec, CA_NEZHA)


def test_tat_dinh_va_cache(ban_ghi):
    chay, *_ = ban_ghi
    a = t046.json_ban_ghi(chay(BAT), CA_NEZHA)
    b = t046.json_ban_ghi(chay(BAT), CA_NEZHA)
    assert a == b
    # gọi lại trong cùng CACHE: p lấy từ cache, bản ghi không đổi
    chay2, ca, t, ch = ban_ghi
    p = runner._params(dict(ch, che_do=BAT), ca)
    c = chuoi.chay(ca['spans'], ca['metrics'], ca['logs'], ca['inventory'], ca['aliases'], t, copy.deepcopy(p))
    assert t046.json_ban_ghi(c, CA_NEZHA) == a and chuoi.CACHE.trung > 0


def test_p_cu_the_khop_bang_do(ban_ghi):
    """p G3 của src trùng từng số với lượt đo; cờ D1 trùng."""
    chay, ca, t, ch = ban_ghi
    rec = chay(BAT)
    do = json.loads((t046.ROOT / f'results/T-046/runs/b3-sua2-aa-001/ca/{CA_NEZHA}.json').read_text(encoding='utf-8'))
    bang = do['cua_so']['that|R0']['bang']
    pv = {x['ma']: x for x in rec['extra']['don_vi_phan_vi']}
    n = 0
    for u in bang['pv']:
        for d, h in u['huong'].items():
            assert pv[u['ma']][f'p_{d}'] == h['p_G3'], (u['ma'], d)
            n += 1
    assert n > 0
    dem = {x['ma']: x for x in rec['worlds']['P']['don_vi_dem']}
    for u in bang['dem']:
        if 'p_D1_len' in u:
            for d in u['huong_cham']:
                assert dem[u['ma']][f'p_{d}'] == u[f'p_D1_{d}']


def test_thang_T4c_o_moi_the_gioi(ban_ghi):
    chay, *_ = ban_ghi
    rec = chay(BAT)
    assert rec['method_version'] == chuoi.PHIEN_BAN_CHE_DO and rec['extra']['che_do'] == BAT
    assert rec['blocks'] == rec['extra']['T4c']['blocks']
    assert all(len(b['key']) == 5 for b in rec['blocks'])
    for w in chuoi.WORLDS:
        assert all(len(b['key']) == 5 for b in rec['worlds'][w]['blocks'])
    rec0 = chay(dict(BAT, thang='E4'))
    assert all(len(b['key']) == 4 for b in rec0['blocks'])
    assert rec0['extra']['T4c']['blocks'] == rec['extra']['T4c']['blocks']
