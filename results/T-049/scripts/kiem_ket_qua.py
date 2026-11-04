"""Kiểm độc lập RR/hòa, tổng hợp luật và mẫu độ bền từ các tệp đã đóng."""
import argparse
import gzip
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

from cham import nap_nhan, save
from chuan_bi import OUT, ROOT, read, sha
from dong_pha1 import read_row
from m1_danh_gia.pha2 import giai_ma_json


def rr_direct(blocks, root):
    start = 1
    for block in blocks:
        assert len(block['groups']) == 1
        group = block['groups'][0]
        if root in group:
            return sum((Fraction(1, r) for r in range(start, start + len(group))), Fraction(0)) / len(group)
        start += len(group)
    return Fraction(0)


def expected(kq, off, on, cells, fake, world, weights, h, delta):
    a, b = (kq['cau_hinh'][cid]['ca'] for cid in (off, on))
    weight = weights or {oid: 1 for oid in a}
    means, cell_values = {}, defaultdict(list)
    for dataset in ('RE2-TT', 'Nezha-OB', 'gop'):
        ids = [oid for oid in a if dataset == 'gop' or a[oid]['dataset'] == dataset]
        den = sum(weight[oid] for oid in ids)
        assert den
        means[dataset] = sum((weight[oid] * (b[oid]['theo_the_gioi'][world]['RR'] -
                                            a[oid]['theo_the_gioi'][world]['RR']) for oid in ids), Fraction(0)) / den
    for oid in a:
        if weight[oid]:
            cell_values[a[oid]['o']].append((weight[oid], b[oid]['theo_the_gioi'][world]['RR'] -
                                                          a[oid]['theo_the_gioi'][world]['RR']))
    P = M = Pp = Mp = 0
    for cell, values in cell_values.items():
        avg = sum((w * value for w, value in values), Fraction(0)) / sum(w for w, _ in values)
        multiplier = values[0][0]
        assert all(w == multiplier for w, _ in values)
        if cell in cells:
            P += multiplier * (avg > Fraction(1, 10**12))
            M += multiplier * (avg < -Fraction(1, 10**12))
        else:
            Pp += multiplier * (avg > Fraction(1, 10**12))
            Mp += multiplier * (avg < -Fraction(1, 10**12))
    n = total = 0
    for oid in fake[off]:
        x, y = fake[off][oid], fake[on][oid]
        if 'INSUFFICIENT_EVIDENCE' in (x['verdict'], y['verdict']):
            continue
        w = weight[oid]
        n += w
        total += w * (sum(t == 1 for t in y['extra']['tang_P'].values()) -
                      sum(t == 1 for t in x['extra']['tang_P'].values()))
    ce = 'CHUA_KIEM_DUOC' if not n else 'HAI' if Fraction(total, n) > h else 'KHONG_KICH_HOAT'
    if ce == 'HAI' or (M + Mp >= 3 and P + Pp == 0):
        verdict = 'HAI'
    elif (means['RE2-TT'] > Fraction(1, 30) and means['Nezha-OB'] < -Fraction(1, 22)) or (
            means['Nezha-OB'] > Fraction(1, 22) and means['RE2-TT'] < -Fraction(1, 30)):
        verdict = 'TRAI_CHIEU_DATASET'
    elif means['gop'] < -delta:
        verdict = 'HAI'
    elif len(cells) < 6:
        verdict = 'KHONG_DU_CA'
    elif means['gop'] > delta and P > M and means['RE2-TT'] >= -Fraction(1, 30) and means['Nezha-OB'] >= -Fraction(1, 22):
        verdict = 'GIUP'
    elif abs(means['gop']) <= delta:
        verdict = 'KHONG_TAC_DUNG'
    else:
        verdict = 'TRAI_CHIEU_O'
    return verdict, means, (P, M, Pp, Mp), ce


def check_pair(kq, off, on, cells, fake, stage, weights, settings, got):
    h = {'h=0.5': Fraction(1, 2), 'h=2': Fraction(2)}.get(settings, Fraction(1))
    delta = {'delta=0.005': Fraction(5, 1000), 'delta=0.02': Fraction(2, 100)}.get(settings, Fraction(1, 100))
    result = {w: expected(kq, off, on, cells, fake, w, weights, h, delta) for w in ('P', 'S_lo', 'S_hi')}
    outcomes = {w: value[0] for w, value in result.items()}
    dependent = len(set(outcomes.values())) > 1
    main = outcomes['P']
    if stage == 'K-b':
        action = ('GIU_C_CHO_MINH' if dependent or main.startswith('TRAI_CHIEU') or
                  (main == 'GIUP' and result['P'][3] == 'CHUA_KIEM_DUOC') else
                  'THAY_BANG_VC' if main == 'GIUP' else 'GIU_C')
    else:
        action = ('GIU_BAT_CHUA_PHAN_XU' if dependent else 'TRINH_MINH' if main.startswith('TRAI_CHIEU') else
                  {'HAI': 'BO', 'GIUP': 'GIU_BAT', 'KHONG_DU_CA': 'GIU_BAT_CHUA_PHAN_XU',
                   'KHONG_TAC_DUNG': 'DE_XUAT_BO'}[main])
    assert got['hanh_dong'] == action, (on, settings, 'action')
    assert got['ket_hop']['theo_the_gioi'] == outcomes, (on, settings, 'worlds')
    assert got['ket_hop']['phu_thuoc_quan_sat'] == dependent
    assert got['dMRR'] == {w: result[w][1] for w in result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scoring', type=Path)
    args = parser.parse_args()
    folder = args.scoring.resolve()
    receipt = read(folder / 'so-lan-nhin.json')
    path = ROOT / receipt['seal']
    assert sha(path) == receipt['seal_sha256']
    seal = read(path)
    kq = giai_ma_json(read(folder / 'kq.json'))
    robustness = giai_ma_json(read(folder / 'do-ben.json'))
    labels = nap_nhan(False)
    checked = 0
    for cid, config in kq['cau_hinh'].items():
        records = [json.loads(line) for line in (folder / cid / 'ban-ghi.jsonl').read_bytes().splitlines()]
        assert len(records) == 52
        for rec in records:
            for world in ('P', 'S_lo', 'S_hi'):
                value = rr_direct(rec['worlds'][world]['blocks'], labels[rec['opaque_id']]['root'])
                score = config['ca'][rec['opaque_id']]['theo_the_gioi'][world]
                assert value == score['RR']
                checked += 1
    fake = defaultdict(dict)
    for entry in seal['entries']['ce']:
        rec = read_row(entry['native'], entry['source_config'])
        fake[entry['config']][entry['job']['opaque_id']] = rec
    cells = set(read(OUT / 'o-cham.json')['E_X']['E2-VC' if seal['stage'] == 'K-b' else 'E3b'])
    pairs = [('K-thang-C', 'K-thang-VC'), ('K-day-du-C', 'K-day-du-VC')] if seal['stage'] == 'K-b' else [tuple(seal['configs'])]
    for off, on in pairs:
        for setting, value in robustness['do_nhay'][on].items():
            check_pair(kq, off, on, cells, fake, seal['stage'], None, setting, value)
    rng = np.random.default_rng(20261102)
    total = 0
    with gzip.open(folder / 'bootstrap.jsonl.gz', 'rt', encoding='utf-8') as stream:
        for i, line in enumerate(stream):
            row = giai_ma_json(json.loads(line))
            assert row['i'] == i
            counts = Counter()
            for dataset in sorted({x['dataset'] for x in labels.values()}):
                options = sorted({x['o'] for x in labels.values() if x['dataset'] == dataset})
                counts.update(options[int(j)] for j in rng.integers(0, len(options), size=len(options)))
            weights = {oid: counts[label['o']] for oid, label in labels.items()}
            assert row['weights'] == weights
            for off, on in pairs:
                for setting, value in row['result'][on].items():
                    check_pair(kq, off, on, cells, fake, seal['stage'], weights, setting, value)
                    total += 1
    assert i == 999 and robustness['n'] == 1000
    for cell, row in robustness['bo_tung_o'].items():
        weights = {oid: int(label['o'] != cell) for oid, label in labels.items()}
        for off, on in pairs:
            for setting, value in row[on].items():
                check_pair(kq, off, on, cells, fake, seal['stage'], weights, setting, value)
    save(folder / 'kiem-doc-lap.json', {'PASS': True, 'RR_checks': checked, 'bootstrap_comparisons': total,
                                       'seed': 20261102, 'leave_one_cell_out': len(robustness['bo_tung_o'])})
    print('PASS independent RR, law and sensitivity/bootstrap/leave-one-cell', checked, total, flush=True)


if __name__ == '__main__':
    main()
