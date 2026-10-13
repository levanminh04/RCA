"""Verify the approved repair using saved outputs only; no methods/raw inputs."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
OLD = ROOT / 'results/T-028/runs/buoc3-005'
sys.path.insert(0, str(ROOT / 'results/T-028/scripts'))
sys.dont_write_bytecode = True
from thuc_hien_buoc3_6 import merge_flags

read = lambda p: json.loads(p.read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
identity = lambda r: (r['dataset'], r['method'], r['opaque_id'])


def differences(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            pp = path + '/' + str(k)
            out += [pp] if k not in a or k not in b else differences(a[k], b[k], pp)
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [p for i, (x, y) in enumerate(zip(a, b)) for p in differences(x, y, path + '/' + str(i))]
    return [] if a == b else [path]


def main():
    old, new = read(OLD / 'ca-sai.json'), read(RUN / 'ca-sai.json')
    diffs = differences(old, new)
    pattern = re.compile(r'^/main_rows/\d+/mechanisms/[15]/(?:base_flags_all_OK_seeds|explanation_flags_wrong_seeds)/M[1-6]/reason$')
    assert all(p in ('/run', '/review_metadata_repaired_from') or pattern.fullmatch(p) for p in diffs), diffs
    reason_paths = [p for p in diffs if pattern.fullmatch(p)]
    changes = read(RUN / 'metadata-changes.json')
    assert len(reason_paths) == len(changes)
    # The original document is equal after restoring only the recorded reasons/run provenance.
    clean = copy.deepcopy(new)
    for change in changes:
        target = clean
        for part in change['pointer'].strip('/').split('/'):
            target = target[int(part)] if isinstance(target, list) else target[part]
        target.clear()
        target.update(change['old'])
    clean['run'] = old['run']
    clean.pop('review_metadata_repaired_from')
    assert clean == old
    # Cases exercise common, mixed and partial N/A; never convert N/A into False.
    def flag(value, reason=None):
        return {'value': value, 'availability': 'available' if value is not None else 'N/A', 'reason': reason}
    assert merge_flags([flag(None, 'no_native_activation_threshold')])['reason'] == 'no_native_activation_threshold'
    assert merge_flags([flag(None, 'root_not_returned')] * 3)['reason'] == 'root_not_returned'
    mixed = merge_flags([flag(None, 'missing_channel'), flag(None, 'root_not_returned')])
    assert mixed['value'] is None and len(mixed['seed_NA_reasons']) == 2
    partial = merge_flags([flag(False), flag(None, 'missing_channel')])
    assert partial['value'] is None and partial['seed_NA_reasons'][0]['seed_index'] == 1
    assert merge_flags([flag(True), flag(None, 'missing_channel')])['value'] is True
    assert merge_flags([flag(False), flag(False)])['value'] is False
    # Verify every case-level reason directly from the eligible seed evidence.
    for r in new['main_rows']:
        for k in ('1', '5'):
            for field, seeds in (
                ('base_flags_all_OK_seeds', [s for s in r['evidence']['seed_evidence'].values() if s['status'] == 'OK']),
                ('explanation_flags_wrong_seeds', [s for s in r['evidence']['seed_evidence'].values() if s['by_k'][k]['wrong_OK']])):
                for m, result in r['mechanisms'][k][field].items():
                    ff = [s['by_k'][k]['flags'][m] for s in seeds]
                    if ff and all(f['value'] is None for f in ff):
                        reasons = {f['reason'] for f in ff}
                        if len(reasons) == 1:
                            assert result['reason'] == next(iter(reasons))
    lookup = {identity(r): r for r in new['main_rows']}
    for name in ('manual-selection.json', 'manual-excerpts.json', 'manual-re2.json', 'manual-reading.json'):
        a, b = read(OLD / name), read(RUN / name)
        aa, bb = (a, b) if isinstance(a, list) else (a['cases'], b['cases'])
        assert len(aa) == len(bb)
        for x, y in zip(aa, bb):
            assert identity(x) == identity(y)
            row = lookup[identity(y)]
            if 'row' in y:
                assert y['row'] == row
                assert {k:v for k,v in x.items() if k != 'row'} == {k:v for k,v in y.items() if k != 'row'}
            elif 'mechanisms' in y:
                assert y['mechanisms'] == row['mechanisms']
                assert {k:v for k,v in x.items() if k != 'mechanisms'} == {k:v for k,v in y.items() if k != 'mechanisms'}
            else:
                assert x['reading_note'] == y['reading_note'] and x['requirements'] == y['requirements']
                if 'mechanisms' in y.get('observed_values', {}):
                    assert y['observed_values']['mechanisms'] == row['mechanisms']
    # Exact source comparisons and complete root/ancestor/native-service coverage.
    proxy = read(RUN / 'caller-root-proxy.json')['records']
    expected = {(identity(r), sid) for r in new['main_rows'] for sid in r['evidence']['seed_evidence']}
    assert len(proxy) == len(expected)
    assert {(identity(r), r['seed']) for r in proxy} == expected
    cache = {}
    n_obs = 0
    for rec in proxy:
        row = lookup[identity(rec)]
        s = row['evidence']['seed_evidence'][rec['seed']]
        path = row['evidence']['source']['path']
        if path not in cache:
            cache[path] = read(ROOT / path)['aggregate']
        traces = cache[path]['trace_' + rec['split']]
        entities = {row['root']} | set(s['ancestors']['value'] or [])
        assert {v['entity'] for v in rec['observations']} == entities
        for entity in entities:
            names = {name for name, v in traces.items() if v['entity'] == entity}
            assert {v['native_service'] for v in rec['observations'] if v['entity'] == entity} == (names or {None})
        for v in rec['observations']:
            n_obs += 1
            assert v['source']['path'] == path
            if v['native_service'] is not None:
                raw = traces[v['native_service']]
                assert all(v[key] == raw[key] for key in ('nN', 'nA', 'P95N', 'P95A', 'latency_up', 'availability', 'reason'))
            else:
                assert v['availability'] == 'N/A'
            if v['role'] == 'caller' and s['certain_before_root'] is not None:
                assert v['certain_before_root'] == (v['entity'] in s['certain_before_root'])
    sd = read(RUN / 'structure-description.json')
    assert sd['M0_top1']['n'] == 50 and sd['M0_top1']['n_no_ancestor'] == 23
    assert sd['Nezha_degree_summaries']['n_cases'] == 22 and sd['Nezha_degree_summaries']['n_distinct'] == 1
    mic = sd['Nezha_OK_records']['microrank_full']
    assert len(mic) == 22 and all(r['M5']['1'] == (r['root'] != 'frontend') for r in mic)
    assert sum(r['wrong']['5'] and r['M5']['5'] is True for r in mic) == 14
    assert all(sorted(set(r['ancestors']) & set(r['before'])) == ['frontend'] for r in mic if r['M5']['1'] is True)
    # Reused measurement values are byte-identical, not recomputed checks or metrics.
    reused = read(RUN / 'manifest.json')['reused_files']
    assert all(sha(ROOT / r['new_path']) == r['sha256'] == sha(ROOT / r['path']) for r in reused)
    # Old table rows remain unchanged; new descriptions add rows only.
    before_map = (RUN / 'before-root/ban-do-han-che-xep-hang.md').read_text(encoding='utf-8')
    after_map = (ROOT / 'results/T-028/ban-do-han-che-xep-hang.md').read_text(encoding='utf-8')
    old_tables = [line for line in before_map.splitlines() if line.startswith('|')]
    new_tables = iter(line for line in after_map.splitlines() if line.startswith('|'))
    assert all(any(v == old_line for v in new_tables) for old_line in old_tables)
    assert 'caller-root-proxy.md' in after_map
    assert all('Đối chiếu tác giả' in after_map.split('### ' + code + ' — ', 1)[1].split('### ', 1)[0]
               for code in ('M1','M2','M3','M4','M5','M6','M0'))
    for name in ('thuc_hien_buoc3_6.py','tong_hop_bao_cao.py','xuat_ban_do.py'):
        ast.parse((ROOT / 'results/T-028/scripts' / name).read_text(encoding='utf-8'))
    baseline = read(RUN / 'before-inventory.json')
    old_run_entries = [r for r in baseline if r['path'].startswith('results/T-028/runs/')]
    assert all(sha(ROOT / r['path']) == r['sha256'] for r in old_run_entries)
    result = {'status':'passed','verified_at':datetime.now(timezone(timedelta(hours=7))).isoformat(),
        'case_document_diff_paths':diffs,'case_NA_reason_fields_repaired':len(reason_paths),
        'reason_counts':dict(Counter(c['new']['reason'] for c in changes)),
        'all_other_case_data_identical':True,'labels_Hit_P0_D_D0_unchanged':True,
        'merge_NA_common_mixed_partial_and_OR_tests':6,'manual_notes_and_selection_preserved':True,
        'caller_seed_records':len(proxy),'native_source_observations_compared':n_obs,
        'all_saved_root_and_ancestor_native_services_reported':True,'original_run_files_hash_checked':len(old_run_entries),
        'reused_files_hash_checked':len(reused),'original_report_table_rows_unchanged':True,
        'AST_scripts_checked':3,'method_rerun':False,'raw_read':False,'new_signal_computation':False,
        'limits':'Source-statistic equality, not a new raw/causal check. Old independent measurement checks retained with original provenance.'}
    (RUN / 'review-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Review repair verification passed:',len(reason_paths),'reason fields;',len(proxy),'seed records;',n_obs,'source observations')


if __name__ == '__main__':
    main()
