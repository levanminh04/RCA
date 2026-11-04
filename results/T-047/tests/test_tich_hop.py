"""Một đường tính cho pha 2, bootstrap, độ nhạy và đầy đủ bộ chọn."""
import copy
from fractions import Fraction as F
from itertools import combinations

import numpy as np
import pytest

import adapter_t047 as ad
import luat_c_t047 as lc
from m1_danh_gia import chon_khoi, luat_c, pha2, rr, uv6
from conftest import ce_rec


def test_dung_43_cap():
    names = [chon_khoi.ten(s, lc.TP) for n in range(5) for s in combinations(lc.TP, n)]
    want = {f'R0|{c}' for c in names if c != 'R0'}
    for c in names:
        want |= {chon_khoi.ten(chon_khoi.tap(c) - {x}, lc.TP) + '|' + c for x in chon_khoi.tap(c)}
    assert len(want) == 43 and set(lc.cac_cap()) == want


@pytest.mark.parametrize('weighted', [False, True])
def test_cung_trong_so_cho_RR_UV6_M5_Ce_va_chon(block_data, weighted):
    kq, ce, ex = block_data
    ca = kq['cau_hinh']['K-R0']['ca']
    weights = {o: [0, 3, 1, 2, 2, 0, 3, 1][int(c['o'][4:])] if weighted else 1 for o, c in ca.items()}
    before = copy.deepcopy(block_data)
    got = ad.pha2_khoi(kq, ce, ex, weights)
    assert got == ad.mau_do_ben(kq, ce, ex, weights)
    assert block_data == before
    for key, (a, b, tp, comps) in lc.cac_cap().items():
        cid_a, cid_b = 'K-' + a, 'K-' + b
        xset = set().union(*(ex[x] for x in comps))
        base = pha2.ket_cuc_cap(kq, cid_a, cid_b, xset, tp, 'khoi_K', trong_so=weights,
                                delta_d_co_dinh=lc.DD)
        denom = sum(weights[o] for o in ce[cid_a])
        def n1(rec):
            return list(rec['extra']['tang_P'].values()).count(1)
        diff = F(sum(weights[o] * (n1(ce[cid_b][o]) - n1(ce[cid_a][o])) for o in ce[cid_a]), denom)
        for w in lc.WORLDS:
            r = got['cap'][key]['theo_the_gioi'][w]
            assert r['moc_gia']['tang'] == diff and r['moc_gia']['n'] == denom
            assert r['moc_gia']['ve'] == ('HAI' if diff > 1 else 'KHONG_KICH_HOAT')
            for f in ['MRR_tat', 'MRR_bat', 'dMRR', 'P', 'M', 'P_phay', 'M_phay', 'huong_o', 'so_o_E_X',
                      'dieu_kien_E5', 'UV6', 'delta_d']:
                assert r[f] == base['theo_the_gioi'][w][f]
            assert got['cap'][key]['khong_moc_gia'][w] == base['theo_the_gioi'][w]['ket_cuc']
        # Đếm điều kiện riêng độc lập với helper; ô lấy 0/3 lần phải tác động thật.
        if tp == 'E5':
            for w in lc.WORLDS:
                a5 = sum(weights[o] * kq['cau_hinh'][cid_a]['ca'][o]['theo_the_gioi'][w]['M5'] for o in ca)
                b5 = sum(weights[o] * kq['cau_hinh'][cid_b]['ca'][o]['theo_the_gioi'][w]['M5'] for o in ca)
                assert got['cap'][key]['theo_the_gioi'][w]['dieu_kien_E5'] == ('HAI' if b5 > a5 else 'KHONG_HAI')
    hop = {k: v['ket_hop'] for k, v in got['cap'].items()}
    for w in lc.WORLDS:
        mrr = {cid[2:]: v['gop'] for cid, v in pha2.mrr_cau_hinh(kq, weights, w).items()}
        plain = chon_khoi.chon(lc.TP, lc.IT_CA, lc.DO_THI, mrr, hop, the_gioi=w)
        assert all(got['chon_khoi'][w][k] == v for k, v in plain.items())
        wcap = hop if w == 'P' else {k: v['theo_the_gioi'][w] for k, v in hop.items()}
        assert got['buoc8'][w] == chon_khoi.kiem_cau_hinh_thang(plain['chon'], lc.TP, wcap, lc.IT_CA)
    if not weighted:
        assert got == ad.pha2_khoi(kq, ce, ex)  # toàn bộ kết quả và lựa chọn chính
    else:
        assert got != ad.pha2_khoi(kq, ce, ex)


def test_uv6_doi_theo_boi_so():
    from conftest import pair_data
    kq, a, b = pair_data('E3', True)
    weights0 = {f'fake{i:02}': (0 if i < 2 else 1) for i in range(16)}
    weights2 = {f'fake{i:02}': (2 if i < 2 else 1) for i in range(16)}
    ce = {a: {f'fake{i:02}': ce_rec(0) for i in range(8)}, b: {f'fake{i:02}': ce_rec(0) for i in range(8)}}
    ex = {f'cell{i}' for i in range(8)}
    r0 = lc.ket_cuc_cap(kq, a, b, ex, 'E3', ce, weights0)
    r2 = lc.ket_cuc_cap(kq, a, b, ex, 'E3', ce, weights2)
    assert r0['theo_the_gioi']['S_hi']['UV6'] == 'KHONG_HAI'
    assert r2['theo_the_gioi']['S_hi']['UV6'] == 'HAI'


def test_chua_kiem_giu_toi_thang_va_bootstrap(block_data):
    kq, ce, ex = block_data
    for recs in ce.values():
        for o in recs:
            recs[o] = ce_rec(0, True)
    result = ad.pha2_khoi(kq, ce, ex)
    for w in lc.WORLDS:
        ch = result['chon_khoi'][w]
        assert len(ch['cap_Ce_chua_kiem']) == 43 and ch['cap_Ce_chua_kiem_o_thang']
        assert ch['can_Minh_truoc_task2'] and ch['trinh_Minh']
        assert 'Ce_chua_kiem_o_thang' in ch['ly_do_trinh_Minh']
        assert all(ch['chon'] in key.split('|') for key in ch['cap_Ce_chua_kiem_o_thang'])
    boot = ad.do_ben(kq, ce, ex, seed=20261102, n=3)
    assert boot['mau_goc'] == result and len(boot['mau']) == 3
    assert all(x['chon_khoi']['P']['cap_Ce_chua_kiem'] for x in boot['mau'])


def test_bootstrap_mau_o_ghep_cap_khong_bo_mau(block_data):
    kq, ce, ex = block_data
    seed, n = 20261102, 4
    out = ad.do_ben(kq, ce, ex, seed, n)
    assert out['mau_goc'] == ad.pha2_khoi(kq, ce, ex)
    ca = kq['cau_hinh']['K-R0']['ca']
    ds = [{'ma': o, 'dataset': c['dataset'], 'o': c['o']} for o, c in sorted(ca.items())]
    rng = np.random.default_rng(seed)
    for i, row in enumerate(out['mau']):
        weights = rr.lay_mau_o(ds, rng)
        assert row['i'] == i and row['trong_so'] == weights
        for cell in {c['o'] for c in ca.values()}:
            assert len({weights[o] for o, c in ca.items() if c['o'] == cell}) == 1
        expected = ad.pha2_khoi(kq, ce, ex, weights)
        assert row['chon_khoi'] == expected['chon_khoi'] and row['buoc8'] == expected['buoc8']
    assert len(out['mau']) == n


def test_do_nhay_chay_lai_day_du_bo_chon(block_data):
    kq, ce, ex = block_data
    got = ad.do_nhay(kq, ce, ex)
    assert set(got) == {'1', '1/2', '2'}
    for h in (F(1), F(1, 2), F(2)):
        assert got[str(h)] == lc.danh_gia_khoi(kq, ce, ex, h=h)
        assert len(got[str(h)]['cap']) == 43 and set(got[str(h)]['chon_khoi']) == set(lc.WORLDS)
    assert got['1']['cap'] != got['2']['cap']


def test_thieu_cau_hinh_Ce_bi_chan(block_data):
    kq, ce, ex = block_data
    ce.pop('K-R0')
    with pytest.raises(ValueError):
        ad.pha2_khoi(kq, ce, ex)
