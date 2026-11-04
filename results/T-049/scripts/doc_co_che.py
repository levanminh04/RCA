"""Tách hồ sơ root và chọn đối chứng đúng từ dấu vết đã kiểm."""
import argparse
import json
from collections import Counter
from pathlib import Path

from cham import nap_nhan, save
from chuan_bi import OUT, read
from m1_danh_gia import pha2


def root_profile(world, root):
    channels = [row for row in world['channels'] if row['entity'] == root]
    return {'tier': world['tier'].get(root), 'key': world['keys'].get(root),
            'rr': world['rr'], 'N1': world['N1'], 'channels': channels,
            'max_group': world['max_groups'].get(root),
            'PV': {unit: row for unit, row in world['PV'].items()
                   if unit in {channel['unit'] for channel in channels}},
            'inherited': [row for row in (world['inherited'] or []) if row['thuc_the'] == root]}


def signature(profile, dataset):
    return (dataset, profile['tier'], tuple(sorted({k['unit'].split('|')[0] for k in profile['channels']})),
            tuple(sorted({k['class'] for k in profile['channels']})),
            any(k['F_I'] and k['unit'].startswith('metric|') for k in profile['channels']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scoring', type=Path)
    args = parser.parse_args()
    folder = args.scoring.resolve()
    assert folder.parent == OUT / 'runs'
    seal = read(Path(read(folder / 'so-lan-nhin.json')['seal']))
    stage = seal['stage']
    labels = nap_nhan(False)
    summaries, details, locations, stats = {}, {}, {}, Counter()
    with (folder / 'co-che.jsonl').open(encoding='utf-8') as stream:
        for line_no, line in enumerate(stream, 1):
            row = pha2.giai_ma_json(json.loads(line))
            kind, oid, config = row['kind'], row['id'], row['config']
            for w, world in row['worlds'].items():
                stats[f'{kind}|{config}|{w}|E5_replay'] += world['E5_replay']
            if kind != 'that':
                continue
            root = labels[oid]['root']
            key = config, oid
            summaries[key] = {w: root_profile(world, root) for w, world in row['worlds'].items()}
            details[key] = row['worlds']['P']
            locations[key] = line_no
    compare = pha2.giai_ma_json(read(folder / 'so-sanh-ca.json'))
    results = {}
    for on, value in compare.items():
        off = value['off']
        changes = {oid for oid, worlds in value['windows']['that'].items() if
                   any(r['dRR'] or r['relative_order_changes'] for r in worlds.values())}
        targets = changes | ({'dev-f36d0647d5', 'dev-a915aa2424', 'dev-a5cabe5fa7'} if stage == 'K-b' else set())
        controls = {}
        for oid in sorted(changes):
            sign = signature(summaries[off, oid]['P'], labels[oid]['dataset'])
            candidates = [other for other in labels if other != oid and
                          signature(summaries[off, other]['P'], labels[other]['dataset']) == sign and
                          summaries[off, other]['P']['rr'] == summaries[on, other]['P']['rr'] == 1]
            candidates.sort(key=lambda other: (labels[other]['o'] != labels[oid]['o'], other))
            controls[oid] = candidates[0] if candidates else None
            if candidates:
                targets.add(candidates[0])
        results[on] = {
            'off': off, 'changed': sorted(changes), 'controls': controls,
            'profiles': {oid: {
                'label': labels[oid], 'root_off': summaries[off, oid], 'root_on': summaries[on, oid],
                'world_P_off': details[off, oid], 'world_P_on': details[on, oid],
                'lines': {'off': locations[off, oid], 'on': locations[on, oid]},
            } for oid in sorted(targets)},
        }
    save(folder / 'doc-co-che.json', {'stage': stage, 'pairs': results, 'checks': stats,
                                     'control_definition': 'Cùng dataset, tầng root, nhóm/lớp kênh và cờ metric tự sinh ở vế tắt; cả hai vế RR=1. Không có thì ghi null.'})


if __name__ == '__main__':
    main()
