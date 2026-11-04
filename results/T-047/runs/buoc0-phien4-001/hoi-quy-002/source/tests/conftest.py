"""Dữ liệu tự lập T-047; không nạp dataset hoặc nhãn trên đĩa."""
import copy
from fractions import Fraction as F
from itertools import combinations

import pytest

from m1 import runner
from m1_danh_gia import pha2


def ce_rec(n=0, insufficient=False):
    return {'status': 'OK', 'verdict': 'INSUFFICIENT_EVIDENCE' if insufficient else
            ('CAUSE_FOUND' if n else 'NO_INTRINSIC_ANOMALY'),
            'extra': {'tang_P': {**{f'e{i}': 1 for i in range(n)}, 'idle': 3}}}


def scored(r=F(1, 2), m5=False):
    return {'RR': r, 'hit1': F(int(r == 1)), 'hang': 1 / r if r else None, 'M5': m5}


def case(i, worlds=None):
    return {'dataset': 'RE2-TT' if i < 8 else 'Nezha-OB', 'o': f'cell{i // 2}',
            'loai_loi': 'cpu' if i < 8 else 'return', 'status': 'OK',
            'theo_the_gioi': worlds or {w: scored() for w in pha2.WORLDS}}


def pair_data(tp='E1', special=False, pattern='worlds'):
    a, b = {}, {}
    for i in range(16):
        aw, bw = {}, {}
        for w in pha2.WORLDS:
            r = {'help': F(1), 'harm': F(1, 3), 'flat': F(1, 2)}.get(pattern)
            if r is None:
                r = {'P': F(1), 'S_lo': F(1, 3), 'S_hi': F(1, 2)}[w]
            aw[w], bw[w] = scored(), scored(r)
            if special and tp == 'E3' and i < 2:
                aw[w], bw[w] = scored(F(1)), scored(F(1, 2))
            if special and tp == 'E5' and i < 2:
                bw[w]['M5'] = True
        a[f'fake{i:02}'], b[f'fake{i:02}'] = case(i, aw), case(i, bw)
    name = 'E1+E2' if tp == 'R0,c' else tp
    return {'cau_hinh': {'K-R0': {'ca': a}, 'K-' + name: {'ca': b}}}, 'K-R0', 'K-' + name


@pytest.fixture
def block_data():
    configs, ce = {}, {}
    for n in range(5):
        for comb in combinations(('E1', 'E2', 'E3', 'E5'), n):
            s = set(comb)
            cid = 'K-' + ('+'.join(comb) if comb else 'R0')
            ca, fake = {}, {}
            for i in range(16):
                worlds = {}
                for w in pha2.WORLDS:
                    rank = 4 - int('E1' in s) - int('E2' in s)
                    if 'E3' in s and w != 'S_hi':
                        rank += 1 if i < 8 else -1
                    worlds[w] = scored(F(1, rank), 'E5' in s and i < 2)
                ca[f'fake{i:02}'] = case(i, worlds)
                if i < 8:
                    fake[f'fake{i:02}'] = ce_rec(2 + 2 * int('E2' in s) +
                                                (i % 3) * int('E1' in s) +
                                                int('E3' in s) - int('E5' in s))
            configs[cid], ce[cid] = {'ca': ca}, fake
    ex = {x: {f'cell{i}' for i in range(8 if x != 'E3' else 4)} for x in ('E1', 'E2', 'E3', 'E5')}
    return {'cau_hinh': configs}, ce, ex


@pytest.fixture
def matrix():
    return {'co_dinh_moi_buoc': {'tham_so_E4': {}}, 'buoc': [
        {'ma': 'T13', 'so_sanh': ['C-a0', 'C-a1', 'C-d1', 'C-d2', 'C-d3', 'C-c', 'C-g', 'C-e', 'C-h']} ]}


@pytest.fixture
def synthetic_input():
    # Hai phía thời gian, một service; không có tên ca/dataset trong đầu vào phương pháp.
    spans = []
    for side in (0, 1):
        for i in range(20):
            spans.append({'traceID': f't{side}-{i}', 'spanID': 's', 'parentSpanID': '', 'owner': 'A',
                          'operation': 'handle', 'start_us': (800 + side * 200 + i * 5) * 10**6,
                          'duration_us': (1000 if side == 0 else 100000)})
    c = {'opaque_id': 'synthetic-case', 'case_dir': 'private-case-folder', 'spans': spans,
         'metrics': [], 'logs': [], 'inventory': ['A'], 'aliases': {}, 'params_ca': {
             'don_vi_thoi_gian': {'spans.start_us': 'us', 'metrics.time': 's', 'logs.timestamp': 'ns'},
             'coverage': {'trace': {'khoang': [[280 * 10**9, 1720 * 10**9]], 'r_ns': 1000},
                          'log': {'khoang': [], 'r_ns': 10**9}, 'metric': {'khoang': [], 'r_ns': 10**9}},
             'ho_so_nguon': {'kenh_metric': {'kieu': 'hau_to', 'bang': {}},
                            'quy_tac_log': {'kieu': 'tu_khoa', 'tu_khoa': ['ERROR']},
                            'nguon_khoi_phat': []}}}
    return c, {c['opaque_id']: 1000}


@pytest.fixture
def sandbox_adapter(tmp_path, monkeypatch):
    import adapter_t047 as ad
    monkeypatch.setattr(ad, 'ROOT', tmp_path)
    monkeypatch.setattr(ad, 'OUT', tmp_path / 'results/T-047')
    return ad
