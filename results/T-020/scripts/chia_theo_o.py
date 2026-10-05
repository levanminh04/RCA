"""Draft G1 packages, label metadata only. No telemetry/data/locked access."""
from pathlib import Path
import csv
import hashlib
import json
import math
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-020'
SEED = '20261004'
PACKAGES = {
    'A-da-tin-hieu': {
        'RE2-TT': 'split', 'RE2-OB': 'dev', 'RE3-TT': 'split',
        'Nezha-OB': 'split', 'Eadro-SN': 'split', 'OpenRCA-Bank': 'holdout-candidate',
    },
    'B-kien-truc-khong-trace': {
        'RE2-TT': 'split', 'RE1-SS': 'split', 'RE2-SS': 'dev',
        'RE3-SS': 'split', 'RE3-OB': 'holdout-candidate',
    },
    'C-test-TX0': {
        'RE2-TT': 'split', 'RE1-TT': 'split', 'RE3-OB': 'split',
        'Eadro-SN': 'dev', 'Nezha-OB': 'dev', 'OpenRCA-Bank': 'holdout-candidate',
    },
}


def main():
    with (OUT/'trung-gian/exposure_ledger/public-census.csv').open(encoding='utf-8-sig', newline='') as f:
        catalog = list(csv.DictReader(f))
    assert len({x['identity'] for x in catalog}) == len(catalog)
    (OUT/'chia-theo-o').mkdir(exist_ok=True)
    reports = {}
    for package, selection in PACKAGES.items():
        output = []
        for dataset, strategy in selection.items():
            rows = [x for x in catalog if x['dataset'] == dataset]
            assert rows and all(x['root'] and x['fault'] for x in rows)
            cells = defaultdict(list)
            for row in rows:
                cells[(row['root'], row['fault'])].append(row)
            cell_roles = {}
            ordered = sorted(cells, key=lambda k: hashlib.sha256(f'{SEED}|{dataset}|{k[0]}|{k[1]}'.encode()).hexdigest())
            if dataset == 'RE2-TT':
                dev = {k for k, rs in cells.items() if any(x['dev_v1_allowlist'] == 'True' for x in rs)}
                assert len(dev) == 10 and sum(len(cells[k]) for k in dev) == 30
                assert all(all(x['dev_v1_allowlist'] == 'True' for x in cells[k]) for k in dev)
                cell_roles = {k: 'dev' if k in dev else 'test' for k in cells}
            elif strategy == 'dev':
                cell_roles = {k: 'dev' for k in cells}
            elif strategy == 'holdout-candidate':
                assert all(x['factual_seen'] == 'TX0' for x in rows)
                cell_roles = {k: 'giu-ngoai-ung-vien' for k in cells}
            else:
                # Preregistered: TX2 forced dev; then one third of remaining cells, ceil.
                forced = {k for k, rs in cells.items() if any(x['factual_seen'] == 'TX2' for x in rs)}
                remaining = [k for k in ordered if k not in forced]
                dev = forced | set(remaining[:math.ceil(len(remaining)/3)])
                cell_roles = {k: 'dev' if k in dev else 'test' for k in cells}
            for key, rs in cells.items():
                role = cell_roles[key]
                assert role == 'dev' or all(x['factual_seen'] != 'TX2' for x in rs)
                if package == 'C-test-TX0' and role == 'test':
                    assert all(x['factual_seen'] == 'TX0' for x in rs)
                for row in rs:
                    output.append({
                        'phuong_an': package, 'dataset': dataset, 'identity': row['identity'],
                        'case': row['case'], 'root': row['root'], 'fault': row['fault'],
                        'repeat': row['repetition'], 'unit': row['unit'], 'TX': row['factual_seen'],
                        'vai_tro': role,
                        'tinh_trang': 'CANDIDATE, chờ WHY/chưa duyệt; giữ ngoài chưa đủ C9/schema/license' if role == 'giu-ngoai-ung-vien' else 'CANDIDATE, chờ WHY/chưa duyệt',
                        'nguon': row['identity_evidence'], 'seed': SEED,
                    })
        assert len({x['identity'] for x in output}) == len(output)
        sides = defaultdict(set)
        for row in output:
            sides[(row['dataset'], row['root'], row['fault'])].add(row['vai_tro'])
        assert all(len(v) == 1 for v in sides.values())
        summary = []
        for dataset in selection:
            for role in sorted({x['vai_tro'] for x in output if x['dataset'] == dataset}):
                rs = [x for x in output if x['dataset'] == dataset and x['vai_tro'] == role]
                counts = Counter((x['root'], x['fault']) for x in rs)
                summary.append({'dataset':dataset,'role':role,'cells':len(counts),'cases':len(rs),
                    'single_repeat_cells':sum(v==1 for v in counts.values()),
                    'TX':dict(Counter(x['TX'] for x in rs)), 'min_repeat':min(counts.values()), 'max_repeat':max(counts.values())})
            chosen = [x for x in output if x['dataset'] == dataset]
            expected = [x for x in catalog if x['dataset'] == dataset]
            assert {x['identity'] for x in chosen} == {x['identity'] for x in expected}
            assert len({(x['root'],x['fault']) for x in chosen}) == len({(x['root'],x['fault']) for x in expected})
        with (OUT/'chia-theo-o'/f'{package}.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(output[0])); w.writeheader(); w.writerows(output)
        reports[package] = {'seed':SEED,'assertions':{'one_side_per_cell':True,'no_TX2_test_or_holdout':True,'census_identity_and_cell_equality':True,'RE2TT_v1_30_60_retained':True},'summary':summary}
    (OUT/'runs/split-assertions.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(reports,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
