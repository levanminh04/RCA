"""F1/F8: phân tích hậu kiểm từ bản ghi dev đã seal, không gọi phương pháp."""
import gzip
import json
from collections import Counter, defaultdict
from fractions import Fraction

from common import OUT, RUN, dump, pin, read, save
from m1_danh_gia import pha2
from p3 import danh_gia


def top_mass(record):
    blocks = danh_gia.khoi_tu_ban_ghi(record)
    if record['status'] != 'OK' or not blocks:
        return {}
    entities = {entity for block in blocks for group in block['groups'] for entity in group}
    mass = {e: danh_gia.phan_bo_hang(blocks, e).get(1, Fraction()) for e in entities}
    assert sum(mass.values()) == 1
    return {e: q for e, q in mass.items() if q}


def ce_table(windows, labels, regions, inventory):
    methods = {}
    for name, cases in windows.items():
        assert set(cases) == set(windows['M1']) and len(cases) == 30
        rows, mass = {}, Counter()
        for oid, rec in cases.items():
            root = labels[oid]['root']
            blocks = danh_gia.khoi_tu_ban_ghi(rec)
            ranks = danh_gia.phan_bo_hang(blocks, root) if rec['status'] == 'OK' else {}
            returned = {e for b in blocks for g in b['groups'] for e in g} if rec['status'] == 'OK' else set()
            top = top_mass(rec)
            mass.update(top)
            rows[oid] = {'status': rec['status'], 'V0': rec['verdict'], 'top_mass': top,
                         'top_blocks': blocks[:1], 'returned': len(returned),
                         'O': rec['sets']['observed'], 'U': len(inventory),
                         'coverage': rec['coverage'], 'future_root_returned': root in returned,
                         'future_root_RR': sum((p / rank for rank, p in ranks.items()), Fraction()),
                         'chance_returned_RR': sum((Fraction(1, i) for i in range(1, len(returned) + 1)), Fraction()) / len(returned) if root in returned else None,
                         'chance_U_RR': sum((Fraction(1, i) for i in range(1, len(inventory) + 1)), Fraction()) / len(inventory) if root in inventory else None,
                         'N1': sum(t == 1 for t in rec['extra']['tang_P'].values())}
        methods[name] = {'n_declared': len(rows), 'rows': rows, 'status': Counter(r['status'] for r in rows.values()),
                         'V0': Counter(r['V0'] for r in rows.values()), 'top_mass': mass,
                         'distinct_top_entities': len(mass), 'top_two_mass': sum(v for _, v in mass.most_common(2)),
                         'mean_N1': Fraction(sum(r['N1'] for r in rows.values()), len(rows))}
    comparisons = {}
    for name, method in methods.items():
        if name == 'M1':
            continue
        valid = {oid: methods['M1']['rows'][oid]['N1'] - row['N1']
                 for oid, row in method['rows'].items()
                 if row['status'] == methods['M1']['rows'][oid]['status'] == 'OK'}
        comparisons[name] = {'n_valid': len(valid), 'excluded': sorted(set(method['rows']) - set(valid)),
                             'delta_N1': valid, 'mean_delta_N1': Fraction(sum(valid.values()), len(valid)) if valid else None}
    old = regions['ce_summary']
    assert methods['M1']['mean_N1'] == old['mean_N1'] and methods['M1']['distinct_top_entities'] == old['unique_top_entities']
    return {'methods': methods, 'M1_minus': comparisons,
            'limit': 'Cửa sổ trước tiêm, chưa xác nhận nền lành; root tương lai chỉ ghép trong evaluator.'}


def rank_evidence(record, blocks, root):
    top = blocks[:3]
    entities = {root} | {e for b in top for group in b['groups'] for e in group}
    return {'top_blocks': top, 'root_block': next((b for b in blocks if any(root in g for g in b['groups'])), None),
            'tiers': {e: record['extra']['tang_P'].get(e) for e in sorted(entities)},
            'channels': [c for c in record['extra']['kenh_co'] if c['thuc_the'] in entities]}


def paired_evidence(dev, real, region_index):
    labels = dev['labels']
    results = {}
    for dataset, table in dev['worlds']['P'].items():
        results[dataset] = {}
        for name in ('bo-E1', 'bo-E2', 'bo-E5', 'C-a0', 'C-a1', 'C-d2'):
            delta = table['pairs_M1_minus'][name]['delta_RR']
            groups = {'fault': defaultdict(list), 'position_N_p75': defaultdict(list)}
            rows = {}
            for oid, change in delta.items():
                label = labels[oid]
                groups['fault'][label['fault']].append(change)
                groups['position_N_p75'][region_index[oid]['N_position_p75']['group']].append(change)
                if not change:
                    continue
                candidates = [o for o, d in delta.items() if o != oid and d * change <= 0
                              and (labels[o]['root'], labels[o]['fault']) == (label['root'], label['fault'])]
                evidence = {}
                for case in [oid] + sorted(candidates):
                    base = real['M1'][case]
                    alt = base if name == 'C-d2' else real[name][case]
                    blocks = base['controls'][name]['blocks'] if name == 'C-d2' else alt['blocks']
                    evidence[case] = {'delta_RR': delta[case], 'M1': rank_evidence(base, base['blocks'], label['root']),
                                      'other': rank_evidence(alt, blocks, label['root'])}
                rows[oid] = {'root': label['root'], 'fault': label['fault'], 'evidence': evidence,
                             'same_root_fault_nonmatching_effect': sorted(candidates),
                             'limit': 'Ghép root/fault hậu kiểm; chưa giữ cố định tải, coverage, topology hay điểm tiêm.'}
            results[dataset][name] = {'cases': rows, 'groups': {
                kind: {k: {'n': len(v), 'sum_delta': sum(v), 'win': sum(x > 0 for x in v),
                           'tie': sum(x == 0 for x in v), 'loss': sum(x < 0 for x in v)} for k, v in by.items()}
                for kind, by in groups.items()}}
    return results


def region_changes(real, region_index):
    result = {}
    for oid, row in real['M1'].items():
        off, on = row['region'], row['T12_on_region']
        keys = ('T', 'cach_1', 'cach_2', 'hop_cach_1', 'hop_cach_2')
        if all(off[key] == on[key] for key in keys):
            continue
        p = region_index[oid]
        result[oid] = {'dataset': p['dataset'], 'position_N': p['N_position_p75'],
                       'off': {k: off[k] for k in keys}, 'on': {k: on[k] for k in keys},
                       'summary_off': p['regions'], 'summary_on': p['T12_on_regions'],
                       'source': row['T12_source']}
    return result


def main():
    manifest = read(OUT / 'manifest-dap-phan-bien-001.json')['outputs']
    dev_path, region_path = OUT / 'ket-qua-dev.json', OUT / 'vung-ce-va-vi-tri-001.json'
    seal_path = RUN / 'prepared-seal.json'
    cohort_path = OUT / 'ke-hoach-tap-test.json'
    refs = [pin(p, manifest[p.relative_to(OUT.parents[1]).as_posix()]) for p in (dev_path, region_path, seal_path, cohort_path)]
    seal = read(seal_path)
    refs.append(pin(seal['output']['path'], seal['output']))
    real, ce = defaultdict(dict), defaultdict(dict)
    with gzip.open(RUN / 'prepared.jsonl.gz', 'rt', encoding='utf-8') as stream:
        for line in stream:
            item = pha2.giai_ma_json(json.loads(line))
            job = item['job']
            destination = real if job['window'] == 'that' else ce
            cases = destination[item['configuration']]
            assert job['opaque_id'] not in cases
            cases[job['opaque_id']] = item['record']
    assert len(real) == len(ce) == 6 and all(len(v) == 52 for v in real.values())
    dev = pha2.giai_ma_json(read(dev_path))
    regions = pha2.giai_ma_json(read(region_path))
    position = {row['opaque_id']: row for row in regions['real']}
    result = {'sources': refs, 'C_e': ce_table(ce, dev['labels'], regions, read(cohort_path)['inventory']['RE2-TT']),
              'mechanisms': paired_evidence(dev, real, position), 'T12_region_changes': region_changes(real, position)}
    save(OUT / 'phan-tich-bo-sung-002.json', result)
    print(dump({'PASS': True, 'C_e': {k: [v['mean_N1'], v['distinct_top_entities']]
                                     for k, v in result['C_e']['methods'].items()},
                'T12_region_changes': len(result['T12_region_changes'])}))


if __name__ == '__main__':
    main()
