"""Tổng hợp nhóm điểm và kênh tần suất theo định nghĩa đã khai trước T6."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from cham import nap_nhan, save
from chuan_bi import OUT, read
from m1_danh_gia import pha2


def group_name(kinds):
    return {'phan_vi': 'PV', 'dem': 'DEM'}.get(kinds[0], 'NONE') if len(kinds) == 1 else 'BOTH' if kinds else 'NONE'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scoring', type=Path)
    args = parser.parse_args()
    folder = args.scoring.resolve()
    assert folder.parent == OUT / 'runs'
    receipt = read(folder / 'so-lan-nhin.json')
    seal = read(Path(receipt['seal']))
    stage = seal['stage']
    labels = nap_nhan(False)
    counts, profiles, freq = Counter(), {}, Counter()
    with (folder / 'co-che.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            row = pha2.giai_ma_json(json.loads(line))
            kind, oid, cid = row['kind'], row['id'], row['config']
            summary = {}
            for w, detail in row['worlds'].items():
                maximum = {entity: group_name(value['kinds']) for entity, value in detail['max_groups'].items()}
                counts.update(f'{cid}|{kind}|{w}|max={name}' for name in maximum.values())
                root = labels[oid]['root'] if kind == 'that' else ''
                root_channels = [x for x in detail['channels'] if x['entity'] == root]
                effective_root = [x for x in root_channels if detail['tier'].get(root) != 1 or x['F_I']]
                mixed = bool(any(x['unit'].startswith(('op|', 'metric|', 'canh|')) for x in effective_root) and
                             any(x['unit'].startswith(('log|', 'tan_suat|')) for x in effective_root))
                if kind == 'that':
                    counts[f'{cid}|{kind}|{w}|root_mixed'] += mixed
                saturated = []
                for channel in root_channels:
                    unit = detail['PV'].get(channel['unit'])
                    if unit and unit['e4'].get('r_' + ('len' if '|len' in channel['id'][-4:] else 'xuong') + '_A') == 1:
                        saturated.append(channel['id'])
                if kind == 'that':
                    counts[f'{cid}|{kind}|{w}|root_saturated_channels'] += len(saturated)
                if stage == 'T6':
                    frequency = detail['tan_suat']
                    for item in frequency:
                        score = item['cham']
                        freq[f'{cid}|{kind}|{w}|status={score["trang_thai"]}'] += 1
                        freq[f'{cid}|{kind}|{w}|label={score.get("nhan")}'] += 1
                        for d in ('len', 'xuong'):
                            freq[f'{cid}|{kind}|{w}|F_raw_{d}'] += bool(score.get(f'F_raw_{d}'))
                    for channel in detail['channels']:
                        if channel['unit'].startswith('tan_suat|'):
                            freq[f'{cid}|{kind}|{w}|FI={channel["F_I"]}|class={channel["class"]}'] += 1
                summary[w] = {'max': maximum, 'root_mixed': mixed, 'root_saturation': saturated,
                              'tier': detail['tier'], 'N1': detail['N1'], 'V0': detail['V0'],
                              'frequency': detail.get('tan_suat') if kind == 'ce' else None}
            profiles[kind, oid, cid] = summary
    changes, windows = Counter(), {}
    pairs = [('K-thang-C', 'K-thang-VC'), ('K-day-du-C', 'K-day-du-VC')] if stage == 'K-b' else [tuple(seal['configs'])]
    for off, on in pairs:
        for kind, oid, cid in sorted(profiles):
            if cid != on:
                continue
            per_world = {}
            for w in ('P', 'S_lo', 'S_hi'):
                a, b = profiles[kind, oid, off][w], profiles[kind, oid, on][w]
                for entity in a['max'].keys() & b['max'].keys():
                    changes[f'{on}|{kind}|{w}|{a["max"][entity]}->{b["max"][entity]}'] += 1
                if a['N1'] != b['N1'] or a['tier'] != b['tier']:
                    per_world[w] = {
                        'N1_off': a['N1'], 'N1_on': b['N1'],
                        'tier1_added': sorted(e for e, t in b['tier'].items() if t == 1 and a['tier'].get(e) != 1),
                        'tier1_removed': sorted(e for e, t in a['tier'].items() if t == 1 and b['tier'].get(e) != 1),
                        'frequency': b['frequency'],
                    }
            if per_world:
                windows[f'{on}|{kind}|{oid}'] = per_world
    save(folder / 'nhom-kenh.json', {'counts': counts, 'max_transitions': changes,
                                    'frequency': freq, 'changed_tier_windows': windows})


if __name__ == '__main__':
    main()
