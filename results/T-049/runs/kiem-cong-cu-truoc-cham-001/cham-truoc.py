"""Ghép nhãn dev sau seal và chấm các cặp K-b hoặc T6."""
import argparse
import gzip
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

from chuan_bi import OUT, ROOT, read, sha
from dong_pha1 import native_and_trace
from luat_t049 import danh_gia
from m1_danh_gia import pha2, rr

sys.path.insert(0, str(ROOT / 'results/T-045/scripts'))
from pha2_khoi_k import nap_nhan


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(pha2.ma_hoa_json(value), stream, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def prepare(seal, out):
    states = {kind: defaultdict(dict) for kind in ('that', 'ce')}
    ce = defaultdict(dict)
    groups = defaultdict(list)
    for kind, entries in seal['entries'].items():
        for entry in entries:
            rec, sidecar = native_and_trace(entry)
            cid, oid = rec['config_id'], rec['opaque_id']
            assert oid not in states[kind][cid]
            state = {}
            for w, detail in sidecar['trace']['world_state'].items():
                blocks = rec['worlds'][w]['blocks']
                n1 = sum(len(g) for b in blocks if b['key'][0] == 2 for g in b['groups'])
                assert detail['N1'] == n1
                assert (detail['V0'] == 'CAUSE_FOUND') == (n1 > 0)
                if w == 'P':
                    assert rec['verdict'] == detail['V0']
                state[w] = {key: detail[key] for key in ('N1', 'V0', 'valid_units')}
            states[kind][cid][oid] = state
            if kind == 'ce':
                ce[cid][oid] = {'status': rec['status'], 'verdict': rec['verdict'],
                                'extra': {'tang_P': rec['extra']['tang_P']}}
                continue
            projected = {k: rec[k] for k in ('opaque_id', 'config_id', 'status', 'verdict', 'blocks')}
            projected['extra'] = {k: rec['extra'][k] for k in ('G_N', 'kenh_co_the_gioi')}
            projected['worlds'] = {w: {'blocks': rec['worlds'][w]['blocks']} for w in pha2.WORLDS}
            groups[cid].append(projected)
    for cid in seal['configs']:
        assert len(states['that'][cid]) == 52 and len(states['ce'][cid]) == 30
        part = out / cid
        part.mkdir()
        file = part / 'ban-ghi.jsonl'
        with file.open('x', encoding='utf-8') as stream:
            for row in sorted(groups[cid], key=lambda v: v['opaque_id']):
                print(json.dumps(row, ensure_ascii=False, allow_nan=False), file=stream)
        save(part / 'pha1.json', {'tep': file.name, 'sha256': sha(file), 'so_ban_ghi': 52,
                                  'so_ca': 52, 'cau_hinh': [cid]})
    return states, ce


def decision_summary(result):
    return {'ket_hop': result['ket_hop'], 'hanh_dong': result['hanh_dong'],
            'dMRR': {w: value['dMRR'] for w, value in result['theo_the_gioi'].items()}}


def robust(kq, ce, ex, pairs, stage, out):
    base = next(iter(kq['cau_hinh'].values()))['ca']
    ds = [dict(ma=oid, dataset=row['dataset'], o=row['o']) for oid, row in sorted(base.items())]
    seed, n = 20261102, 1000
    rng = np.random.default_rng(seed)
    frequencies = {b: Counter() for _, b in pairs}
    variants = [('main', {}), ('h=0.5', {'h': Fraction(1, 2)}), ('h=2', {'h': Fraction(2)}),
                ('delta=0.005', {'delta': Fraction(5, 1000)}), ('delta=0.02', {'delta': Fraction(2, 100)})]

    def run(weights):
        return {b: {name: decision_summary(danh_gia(kq, a, b, ex, ce, buoc=stage,
                                                    trong_so=weights, **settings))
                    for name, settings in variants} for a, b in pairs}

    base_sensitivity = run(None)
    assert run({row['ma']: 1 for row in ds}) == base_sensitivity
    with gzip.open(out / 'bootstrap.jsonl.gz', 'xt', encoding='utf-8') as stream:
        for i in range(n):
            weights = rr.lay_mau_o(ds, rng)
            result = run(weights)
            for _, b in pairs:
                frequencies[b][result[b]['main']['hanh_dong']] += 1
            print(json.dumps(pha2.ma_hoa_json(dict(i=i, weights=weights, result=result)),
                             ensure_ascii=False, allow_nan=False), file=stream)
    cells = sorted({row['o'] for row in ds})
    return {'seed': seed, 'n': n, 'frequencies': frequencies, 'do_nhay': base_sensitivity,
            'bo_tung_o': {cell: run({row['ma']: int(row['o'] != cell) for row in ds}) for cell in cells}}


def metrics(kq, states, labels, out_folder):
    out = {}
    for cid, cfg in kq['cau_hinh'].items():
        part = out_folder / cid
        _, native = pha2.doc(part, read(part / 'pha1.json')['sha256'])
        ranks = {}
        for rec in native:
            oid = rec['opaque_id']
            ranks[oid] = {}
            for w in pha2.WORLDS:
                blocks = rec['worlds'][w]['blocks'] if rec['status'] == 'OK' else []
                order = [entity for block in blocks for group in block['groups'] for entity in group]
                root = labels[oid]['root']
                ranks[oid][w] = order.index(root) + 1 if root in order else None
        out[cid] = {}
        for kind, all_configs in states.items():
            by_id = all_configs[cid]
            groups = defaultdict(list)
            for oid in sorted(by_id):
                for tag in ('gop', labels[oid]['dataset'], labels[oid]['o']):
                    groups[tag].append(oid)
            result = {}
            for group, ids in groups.items():
                result[group] = {}
                for w in pha2.WORLDS:
                    summary = {}
                    summary['V0'] = Counter(by_id[oid][w]['V0'] for oid in ids)
                    support = [by_id[oid][w]['N1'] for oid in ids if
                               by_id[oid][w]['V0'] != 'INSUFFICIENT_EVIDENCE']
                    summary['N1'] = {'n': len(support), 'sum': sum(support),
                                     'mean': Fraction(sum(support), len(support)) if support else None}
                    if kind == 'that':
                        rows = [cfg['ca'][oid]['theo_the_gioi'][w] for oid in ids]
                        summary['MRR'] = sum(row['RR'] for row in rows) / len(rows)
                        summary['M5'] = sum(row['M5'] for row in rows)
                        for key in rows[0]['do']:
                            values = [row['do'][key] for row in rows]
                            if all(isinstance(v, (int, float)) for v in values):
                                summary[key] = sum(values) / len(values)
                        summary['Retrieval5'] = summary['hit@5']
                        summary['Rerank1_K5'] = summary['hit@1'] / summary['hit@5'] if summary['hit@5'] else None
                        shown = [ranks[oid][w] for oid in ids]
                        ac = {k: Fraction(sum(r is not None and r <= k for r in shown), len(shown))
                              for k in range(1, 6)}
                        summary.update({f'AC@{k}': ac[k] for k in (1, 3, 5)})
                        summary['Avg@5_AC'] = sum(ac.values()) / 5
                    result[group][w] = summary
            out[cid][kind] = result
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seal', type=Path)
    parser.add_argument('run')
    args = parser.parse_args()
    path = args.seal.resolve()
    digest = sha(path)
    rel = path.relative_to(ROOT).as_posix()
    pin = f'- `{rel}`: `{digest}`'
    assert pin in (ROOT / 'tasks/T-049-k-b-va-t6/LOG.md').read_text(encoding='utf-8').splitlines()
    seal = read(path)
    assert seal['matrix_sha256'] == sha(OUT / 'ma-tran.json')
    out = (OUT / 'runs' / args.run).resolve()
    assert out.parent == OUT / 'runs'
    out.mkdir()
    states, ce = prepare(seal, out)
    assert sha(path) == digest
    cells = read(OUT / 'o-cham.json')
    assert sha(ROOT / cells['source_E_X']) == cells['source_E_X_sha256']
    stage = seal['stage']
    if stage == 'K-b':
        pairs = [('K-thang-C', 'K-thang-VC'), ('K-day-du-C', 'K-day-du-VC')]
        ex = set(cells['E_X']['E2-VC'])
    else:
        branch = seal['branch']
        pairs = [(f'K-thang-{branch}', f'T6-{branch}-E3b')]
        ex = set(cells['E_X']['E3b'])
    save(out / 'so-lan-nhin.json', dict(stage=stage, seal=rel, seal_sha256=digest, scoring='dev'))
    labels = nap_nhan(False)
    assert len(labels) == 52 and len({item['o'] for item in labels.values()}) == 23
    kq = {'cau_hinh': {}}
    for cid in seal['configs']:
        part = out / cid
        assert set(states['that'][cid]) == set(labels)
        kq['cau_hinh'][cid] = pha2.cham(part, read(part / 'pha1.json')['sha256'], labels)['cau_hinh'][cid]
    result = {b: danh_gia(kq, a, b, ex, ce, buoc=stage) for a, b in pairs}
    save(out / 'ket-cuc.json', result)
    save(out / 'kq.json', kq)
    save(out / 'chi-so.json', metrics(kq, states, labels, out))
    save(out / 'do-ben.json', robust(kq, ce, ex, pairs, stage, out))
    print({key: value['hanh_dong'] for key, value in result.items()}, flush=True)


if __name__ == '__main__':
    main()
