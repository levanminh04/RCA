# -*- coding: utf-8 -*-
"""Kiểm cham.phan_bo_hang_tap bằng vét cạn hoán vị trong nhóm hòa; m=1 trùng danh_gia.phan_bo_hang."""
import itertools, random, sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.m1_ft import cham
from src.p3 import danh_gia


def vet_can(rows, tap):
    groups = []
    for e, tg in rows:
        if groups and groups[-1][0] == tg: groups[-1][1].append(e)
        else: groups.append((tg, [e]))
    dist, n = {}, 0
    for perm in itertools.product(*[list(itertools.permutations(g)) for _, g in groups]):
        order = [e for g in perm for e in g]
        r = min(i + 1 for i, e in enumerate(order) if e in tap); dist[r] = dist.get(r, 0) + 1; n += 1
    return {r: Fraction(c, n) for r, c in dist.items()}


def test_ngau_nhien():
    rnd = random.Random(20261113)
    for _ in range(300):
        ents = [f'e{i}' for i in range(rnd.randint(1, 7))]
        rows, tg = [], 0
        for e in ents:
            rows.append((e, tg)); tg += rnd.random() < 0.5
        rec = {'status': 'OK', 'entity_ranking': [{'entity': e, 'key': [-t], 'tie_group': t} for e, t in rows]}
        blocks = danh_gia.khoi_tu_ban_ghi(rec)
        tap = set(rnd.sample(ents, rnd.randint(1, len(ents))))
        assert cham.phan_bo_hang_tap(blocks, tap) == vet_can(rows, tap)
        if len(tap) == 1:
            assert cham.phan_bo_hang_tap(blocks, tap) == danh_gia.phan_bo_hang(blocks, next(iter(tap)))


def test_trang_thai_va_vang():
    rec = {'status': 'ERROR', 'entity_ranking': []}
    assert cham.cham_ca_loi(rec, ['a'])['p1'] == 0.0
    rec = {'status': 'OK', 'entity_ranking': [{'entity': 'b', 'key': [1], 'tie_group': 0}]}
    r = cham.cham_ca_loi(rec, ['a']); assert r['trong_tra_ve'] is False and r['hang_cat'] == 6.0
    assert cham.cham_ca_khong_loi({'status': 'OK', 'verdict': 'NO_INTRINSIC_ANOMALY'})['k'] == 0
    assert cham.cham_ca_khong_loi({'status': 'OK', 'verdict': 'INSUFFICIENT_EVIDENCE'})['k'] == 1
    assert cham.cham_ca_khong_loi({'status': 'ERROR'})['k'] == 1




def test_chieu_va_canh():
    rec = {'status': 'OK', 'entity_ranking': [{'entity': 'a', 'key': [3], 'tie_group': 0}, {'entity': 'x', 'key': [2], 'tie_group': 1},
                                              {'entity': 'y', 'key': [1], 'tie_group': 2}, {'entity': 'z', 'key': [0], 'tie_group': 3}],
           'extra': {'m1_ft': {'canh_xep_hang': [
               {'nguon': 'a', 'dich': 'z', 'loai': 'data', 'co': 1, 'diem': .9, 'hang': 1, 'tie_group': 0},
               {'nguon': 'x', 'dich': 'y', 'loai': 'http', 'co': 1, 'diem': .5, 'hang': 2, 'tie_group': 1},
               {'nguon': 'y', 'dich': 'z', 'loai': 'http', 'co': 0, 'diem': 0, 'hang': 3, 'tie_group': 2}]}}}
    p = cham.chieu_canh_ve_nut(rec)
    assert [(r['entity'], r['tie_group']) for r in p['entity_ranking']] == [('a', 0), ('z', 0), ('x', 1), ('y', 1)]
    assert cham.cham_ca_loi(p, ['z'])['hang_ky_vong'] == 1.5
    c = cham.cham_canh(rec, ('a', 'z', 'data')); assert c['hang_ky_vong'] == 1 and c['top3'] == 1
    assert cham.cham_canh(rec, ('a', 'z', 'http'))['trang_thai'] == 'VANG'
    assert cham.cham_canh({'extra': {}}, ('a', 'z', 'data'))['trang_thai'] == 'UNSUPPORTED'


if __name__ == '__main__':
    test_ngau_nhien(); test_trang_thai_va_vang(); test_chieu_va_canh(); print('test_cham: OK')
