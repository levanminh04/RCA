"""Khối 15: gói sửa sau kiểm lại gói C8 (dinh-chinh-cai-dat.md mục C9): khóa ghi ra giảm dần (S43), số lần gộp của T4c
và theo thế giới (S44), các ca làm mạnh test của C8 (S45: khong_moc_gia, MRR theo thế giới, lấy mẫu ô, cache theo ca,
số lần gộp). CW1, BT3, DO1 mở rộng ở test_k14_luot5b.py. Đáp án tự lập ở fixture/dap-an-thanh-phan.json."""
import json
import os
import random
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from conftest import tu_lap, DAP_AN_THANH_PHAN


def _k(e, u, s):
    from m1.kieu import Kenh
    return Kenh(e, 'x', 'len', 'khong_lan', float(s), s_q=Fraction(s), don_vi=u)


def _giam_dan(blocks):
    k = [b['key'] for b in blocks]
    return all(a >= b for a, b in zip(k, k[1:]))


# ---- S43: khóa ghi ra giảm dần ----

def test_FX1_khoa_ghi_ra_giam(ma):
    from m1 import xep_hang
    from m1_danh_gia import rr
    m = tu_lap(DAP_AN_THANH_PHAN, 'FX1')
    da = m['dap_an']
    ma('FX1')
    e = Fraction(1, 10 ** 18)
    x = xep_hang.xep([_k('A', 'a', Fraction(1, 2) + e), _k('B', 'b1', Fraction(1, 2)), _k('B', 'b2', Fraction(1, 10)),
                      _k('C', 'c', Fraction(1, 2) - e)])
    assert [b['groups'][0] for b in x['blocks']] == da['E6a_blocks'] and x['gop_khoa_ghi_ra'] == da['E6a_gop']
    assert _giam_dan(x['blocks']) is da['khoa_ghi_ra_giam']
    assert rr.rr_ca(x['blocks'], 'A') == Fraction(da['RR_A'])
    x = xep_hang.xep([_k('A', 'a', Fraction(1, 2)), _k('C', 'c', Fraction(1, 2) + e)],
                     khoa_T4c={'A': (0.9, 0.9), 'C': (0.1, 0.1)})
    assert [b['groups'][0] for b in x['blocks']] == da['T4c_blocks'] and _giam_dan(x['blocks'])
    x = xep_hang.xep([_k('A', 'a', Fraction(1, 2) + e), _k('B', 'b1', Fraction(1, 2)), _k('B', 'b2', Fraction(1, 10)),
                      _k('C', 'c', Fraction(1, 2) - e)], che_do='E6b', canh=())
    assert _giam_dan(x['blocks'])


# ---- S44: số lần gộp theo thế giới và của T4c đi vào bản ghi ----

def test_GK1_so_gop_vao_ban_ghi(ma, monkeypatch):
    from m1 import chuoi, xep_hang
    from test_k12_luot4 import _ca_metric
    ma('GK1')
    goc, dem = xep_hang.xep, []

    def xep(*a, **k):
        out = goc(*a, **k)
        dem.append(1)
        out['gop_khoa_ghi_ra'] = len(dem)  # lần gọi thứ n: P, S_lo, S_hi rồi T4c
        return out
    monkeypatch.setattr(chuoi.xep_hang, 'xep', xep)
    rows, p = _ca_metric([0.0] * 20, [10.0] * 20)
    r = chuoi.chay([], rows, [], ['S'], {}, 1000, p)
    assert r['diagnostics']['gop_khoa_ghi_ra'] == {'P': 1, 'S_lo': 2, 'S_hi': 3}
    assert r['diagnostics']['gop_khoa_ghi_ra_T4c'] == 4 == r['extra']['T4c']['gop_khoa_ghi_ra']


def test_XH1_so_gop(ma):
    from m1 import xep_hang
    m = tu_lap(DAP_AN_THANH_PHAN, 'XH1')
    da = m['dap_an']
    ma('XH1-gop')
    x = xep_hang.xep([_k(e, e, Fraction(1, 2)) for e in 'ABC'], thuc_the_co_kenh_OK=set('ABC'), che_do='E6b', canh=())
    assert x['gop_khoa_ghi_ra'] == da['pi_3_gop']
    x = xep_hang.xep([_k('A', 'a', Fraction(1, 2) + Fraction(1, 10 ** 18)), _k('B', 'b', Fraction(1, 2)),
                      _k('C', 'c', Fraction(1, 2))])
    assert ([b['groups'][0] for b in x['blocks']], x['gop_khoa_ghi_ra']) == \
        (da['ba_thuc_the']['blocks'], da['ba_thuc_the']['gop_khoa_ghi_ra'])


# ---- S45: khong_moc_gia ----

def _kq(ca_tat, ca_bat, a, b):
    from m1_danh_gia import pha2

    def cfg(ca):
        return {o: {'dataset': v['dataset'], 'o': v['o'], 'loai_loi': v.get('loai_loi'), 'verdict': 'CAUSE_FOUND',
                    'theo_the_gioi': {w: {'RR': v['RR'][w] if isinstance(v['RR'], dict) else v['RR'],
                                          'hit1': v['RR'][w] if isinstance(v['RR'], dict) else v['RR'],
                                          'hang': Fraction(1), 'M5': v['M5'][w] if isinstance(v.get('M5'), dict)
                                          else v.get('M5', False)} for w in pha2.WORLDS}} for o, v in ca.items()}
    return {'cau_hinh': {a: {'ca': cfg(ca_tat)}, b: {'ca': cfg(ca_bat)}}}


def test_CE1_E3_dM0(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'CE1')
    d, da = m['dau_vao']['ca_E3_dM0'], m['dap_an']['ca_E3_dM0']
    ma('CE1-E3-dM0')
    a, b = d['cap']
    tat = {'a': {'dataset': 'Nezha-OB', 'o': 'c1', 'loai_loi': 'exception', 'RR': Fraction(1)},
           'b': {'dataset': 'Nezha-OB', 'o': 'c2', 'loai_loi': 'cpu', 'RR': Fraction(0)}}
    bat = {'a': dict(tat['a'], RR=Fraction(0)), 'b': dict(tat['b'], RR=Fraction(1))}
    r = pha2.ket_cuc_cap(_kq(tat, bat, a, b), a, b, set(d['E_X']), 'E3', 'khoi_K',
                         moc_gia=tuple(tuple(x) for x in d['moc_gia']))
    for w in pha2.WORLDS:
        t = r['theo_the_gioi'][w]
        assert (t['ket_cuc'], t['ly_do_hai_rieng']) == (da['ket_cuc'], da['ly_do'])
    assert r['khong_moc_gia'] == {w: da['khong_moc_gia'] for w in pha2.WORLDS}


def test_CE1_E5_theo_the_gioi(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'CE1')
    d, da = m['dau_vao']['ca_E5_the_gioi'], m['dap_an']['ca_E5_the_gioi']
    ma('CE1-E5-the-gioi')
    a, b = d['cap']
    tat = {'a': {'dataset': 'RE2-TT', 'o': 'c1', 'RR': Fraction(1, 2), 'M5': False}}
    bat = {'a': {'dataset': 'RE2-TT', 'o': 'c1', 'RR': Fraction(1), 'M5': {'P': True, 'S_lo': False, 'S_hi': True}}}
    r = pha2.ket_cuc_cap(_kq(tat, bat, a, b), a, b, {'c1'}, 'E5', 'khoi_K',
                         moc_gia=tuple(tuple(x) for x in d['moc_gia']))
    assert r['khong_moc_gia'] == da['khong_moc_gia']


# ---- S45: MRR theo thế giới ----

def test_MB1_the_gioi(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'MB1')
    d, da = m['dau_vao'], m['dap_an']
    ma('MB1-the-gioi')
    ca = {o: {'dataset': ds, 'theo_the_gioi': {w: {'RR': Fraction(d['RR_T_S_lo' if w == 'S_lo' else 'RR_T'][o])}
                                               for w in pha2.WORLDS}} for o, ds in d['ca']}
    kq = {'cau_hinh': {'T': {'ca': ca}}}
    assert pha2.mrr_cau_hinh(kq, d['boi_so'], 'S_lo')['T'] == {k: Fraction(v) for k, v in da['S_lo_boi_so'].items()}
    assert pha2.mrr_cau_hinh(kq, d['boi_so'], 'P')['T'] == {k: Fraction(v) for k, v in da['boi_so'].items()}


# ---- S45: lấy mẫu ô ----

def _ds_LM1(m):
    return [{'ma': a, 'dataset': b, 'o': c} for a, b, c in m['dau_vao']['ca']]


def _mau_theo_SPEC(ds, seed):
    """Cách lấy viết lại độc lập theo SPEC T-045 bước 7: trong từng dataset (theo tên), lấy có hoàn lại đúng số ô trên
    danh sách ô đã sắp."""
    rng = np.random.default_rng(seed)
    dem = {}
    for d in sorted({c['dataset'] for c in ds}):
        o = sorted({c['o'] for c in ds if c['dataset'] == d})
        for i in rng.integers(0, len(o), size=len(o)):
            dem[o[int(i)]] = dem.get(o[int(i)], 0) + 1
    return {c['ma']: dem.get(c['o'], 0) for c in ds}


MA_LM1 = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from m1_danh_gia import rr
ds = json.loads(sys.argv[2])
print(json.dumps(rr.lay_mau_o(ds, np.random.default_rng(3)), sort_keys=True))
'''


def test_LM1_mo_rong(ma):
    from m1_danh_gia import rr
    m = tu_lap(DAP_AN_THANH_PHAN, 'LM1')
    d, da = m['dau_vao'], m['dap_an']
    ma('LM1-mo-rong')
    ds = _ds_LM1(m)
    assert all(rr.lay_mau_o(ds, np.random.default_rng(s)) == _mau_theo_SPEC(ds, s) for s in d['seed']) is \
        da['khop_cach_lay_theo_SPEC']
    duoc_lay = set()
    for s in range(d['nhieu_seed']):
        duoc_lay |= {c['o'] for c in ds if rr.lay_mau_o(ds, np.random.default_rng(s))[c['ma']] > 0}
    assert (duoc_lay == {c['o'] for c in ds}) is da['moi_o_duoc_lay_qua_50_seed']
    src = str(Path(__file__).resolve().parents[3] / 'src')
    ra = set()
    for hs in d['hash_seed']:
        xao = list(ds)
        random.Random(hs).shuffle(xao)
        ra.add(subprocess.run([sys.executable, '-B', '-c', MA_LM1, src, json.dumps(xao)],
                              env=dict(os.environ, PYTHONHASHSEED=str(hs)), capture_output=True, text=True,
                              check=True).stdout)
    assert (len(ra) == 1) is da['khong_phu_thuoc_hash_seed']
    with pytest.raises(ValueError):
        rr.lay_mau_o(ds + [{'ma': 'x', 'dataset': 'Nezha-OB', 'o': 'o1'}], np.random.default_rng(0))


# ---- S45: cache theo ca, mã mờ trùng ----

def test_RN1_mo_rong(ma, tmp_path, monkeypatch):
    from m1 import chuoi, e4, runner
    import sinh_trace_S
    from conftest import FIXTURE
    m = tu_lap(DAP_AN_THANH_PHAN, 'RN1')
    da = m['dap_an']
    ma('RN1-mo-rong')
    spans, logs = sinh_trace_S.sinh('S1', t=1000, mau=FIXTURE['trace_mau_S'])
    ca = [{'opaque_id': f'gia-00{i}', 'spans': spans, 'metrics': [], 'logs': logs,
           'inventory': ['A', 'B', 'F', 'I', 'R', 'X'], 'aliases': {}} for i in (1, 2)]
    moc = {c['opaque_id']: 1000 for c in ca}
    cau_hinh = [{'config_id': 'R0', 'params': sinh_trace_S.params({})}]
    tao = []

    class Dem(e4.CacheCong):
        def __init__(self):
            super().__init__()
            tao.append(self)
    monkeypatch.setattr(e4, 'CacheCong', Dem)
    runner.pha1(ca, moc, cau_hinh, tmp_path / 'l1')
    assert (chuoi.CACHE is tao[-1] and len(tao) == 2) is da['cache_la_doi_tuong_moi_nhat']
    with pytest.raises(ValueError):
        runner.pha1(ca + [dict(ca[0])], moc, cau_hinh, tmp_path / 'l2')
