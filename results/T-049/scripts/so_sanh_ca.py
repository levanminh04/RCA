"""Gộp đối chiếu theo ca, ô, thế giới và chọn ví dụ có dấu vết để đọc."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from cham import save
from chuan_bi import OUT, read
from m1_danh_gia import pha2


def rank_keys(frame):
    return {e: (index, b['key']) for index, b in enumerate(frame['blocks'])
            for group in b['groups'] for e in group}


def case_pair(before, after, root, stage):
    a, b = rank_keys(before), rank_keys(after)
    root_a, root_b = a.get(root), b.get(root)
    tier_one_a = {e for e, t in before['tier'].items() if t == 1}
    tier_one_b = {e for e, t in after['tier'].items() if t == 1}
    opponents = {}
    if root_a and root_b:
        for e in sorted(a.keys() & b.keys() - {root}):
            first, second = a[e][0] - root_a[0], b[e][0] - root_b[0]
            if (first > 0) - (first < 0) != (second > 0) - (second < 0):
                opponents[e] = {'off': a[e], 'on': b[e]}
    out = {'dRR': after['rr'] - before['rr'], 'dN1': after['N1'] - before['N1'],
           'tier1_added': sorted(tier_one_b - tier_one_a), 'tier1_removed': sorted(tier_one_a - tier_one_b),
           'root_key_off': root_a, 'root_key_on': root_b, 'relative_order_changes': opponents}
    if stage == 'K-b':
        out['VC'] = after['VC']['status']
        out['identified'] = (after['VC'].get('phu_nho_nhat') or {}).get('dinh_danh', [])
    else:
        frequency = [x['cham'] for x in after['tan_suat']]
        out['E3b'] = dict(units=len(frequency), supported=sum(bool(x['hop_le']) for x in frequency),
                          flagged=sum(bool(x.get('F_raw_len') or x.get('F_raw_xuong')) for x in frequency))
    return out


def summarize(folder, stage, ex, pairs, labels):
    evidence = {}
    with (folder / 'co-che.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            row = pha2.giai_ma_json(json.loads(line))
            slim = {}
            for world, detail in row['worlds'].items():
                value = {k: detail[k] for k in ('blocks', 'tier', 'rr', 'N1')}
                if stage == 'K-b':
                    value['VC'] = {k: detail['VC'].get(k) for k in ('status', 'phu_nho_nhat')}
                else:
                    value['tan_suat'] = [{'cham': {k: item['cham'].get(k) for k in
                                                 ('hop_le', 'F_raw_len', 'F_raw_xuong')}}
                                         for item in detail['tan_suat']]
                slim[world] = value
            evidence[row['kind'], row['id'], row['config']] = slim
    output = {}
    for off, on in pairs:
        rows = {}
        counts = defaultdict(Counter)
        for kind in ('that', 'ce'):
            records = {}
            for _, oid, _ in sorted(k for k in evidence if k[0] == kind and k[2] == on):
                lab = labels[oid]
                records[oid] = {}
                for w in pha2.WORLDS:
                    a, b = (evidence[kind, oid, cid][w] for cid in (off, on))
                    row = case_pair(a, b, lab['root'] if kind == 'that' else '', stage)
                    records[oid][w] = dict(row, dataset=lab['dataset'], cell=lab['o'], in_EX=lab['o'] in ex)
                    direction = 'tang' if row['dRR'] > 0 else 'giam' if row['dRR'] < 0 else 'bang'
                    for group in ('gop', lab['dataset'], lab['o'], 'trong_EX' if lab['o'] in ex else 'ngoai_EX'):
                        counts[f'{kind}|{w}|{group}'][direction] += 1
            rows[kind] = records
        output[on] = {'off': off, 'counts': dict(counts), 'windows': rows}
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scoring', type=Path)
    args = parser.parse_args()
    from cham import nap_nhan

    folder = args.scoring.resolve()
    assert folder.parent == OUT / 'runs'
    seal = read(Path(read(folder / 'so-lan-nhin.json')['seal']))
    cells = read(OUT / 'o-cham.json')['E_X']
    if seal['stage'] == 'K-b':
        pairs = [('K-thang-C', 'K-thang-VC'), ('K-day-du-C', 'K-day-du-VC')]
        ex = set(cells['E2-VC'])
    else:
        pairs = [tuple(seal['configs'])]
        ex = set(cells['E3b'])
    save(folder / 'so-sanh-ca.json', summarize(folder, seal['stage'], ex, pairs, nap_nhan(False)))


if __name__ == '__main__':
    main()
