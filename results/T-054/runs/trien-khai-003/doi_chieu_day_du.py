"""Parity với bản dev đã có; khai trường thay metadata, không nới sai khác khoa học."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path[:0] = [str(OUT / 'scripts'), str(RUN)]
from bien_nhan import atomic, fingerprint, read_pin, ref
from dieu_phoi import status, verify_attempt
from pilot import comparable, reference
from doi_chieu_pilot import MAP, differences

dest = RUN / (sys.argv[1] if len(sys.argv) > 1 else 'pilot-local-007')
plan = read_pin(ref(dest / 'plan.json')); state = status(dest / 'queue')
assert state['controller'] is None and len(state['jobs']) == len(plan['jobs'])
candidates = read_pin(ref(RUN / 'before-files/pilot-plan.json'))['candidates']
proposal = read_pin(ref(OUT / 'runs/trien-khai-002/pilot-proposal.json'))
tt_ref = proposal['input_metadata_refs'][0]
tt_tables = read_pin(tt_ref)
ob_tables = read_pin(proposal['input_metadata_refs'][1])
baseline_refs = proposal['baseline_jobs']
m51 = read_pin(ref(ROOT / 'results/T-051/manifest.json'))
results = []
for job in plan['jobs']:
    s = job['slot']; key = fingerprint(s); old = state['jobs'][key]
    rows = verify_attempt(Path(old['attempt']), job, old['token'])
    result = {'dataset': s['dataset'], 'opaque_id': s['opaque_id'], 'arm': s['arm'], 'seed': s['seed'],
              'statuses': [r['status'] for r in rows]}
    if s['arm'] in MAP:
        candidate = next(c for c in candidates if c['opaque_id'] == s['opaque_id'] and c['window'] == 'that')
        before = comparable(reference(candidate['native_record'], MAP[s['arm']]), control=s['arm'] in ('C-a0','C-a1'))
        after = comparable(rows[0], control=s['arm'] in ('C-a0','C-a1'))
        result.update(reference=candidate['native_record'], fields='all comparable scientific record fields',
                      exact=before == after, differences=differences(before, after))
    elif s['arm'] == 'T12-on':
        candidate = next(c for c in candidates if c['opaque_id'] == s['opaque_id'] and c['window'] == 'that')
        index = int(Path(candidate['native_record']['path']).parent.name.rsplit('-', 1)[1])
        path = f'results/T-051/t12-001/{index:02d}.json'
        expected = read_pin(dict(m51['outputs'][path], path=path))
        assert expected['job']['opaque_id'] == s['opaque_id'] and expected['job']['dataset'] == s['dataset']
        before = {'world_blocks': {w: expected['worlds'][w]['rank'][1]['blocks'] for w in ('P','S_lo','S_hi')},
                  'P_tiers': expected['worlds']['P']['rank'][1]['tang'],
                  'P_region': expected['worlds']['P']['region'][1],
                  'edges': sorted(set(tuple(e) for e in expected['edges']) |
                                  set(tuple(e) for e in expected['static']['added']))}
        after = {'world_blocks': {w: rows[0]['worlds'][w]['blocks'] for w in ('P','S_lo','S_hi')},
                 'P_tiers': rows[0]['extra']['tang_P'], 'P_region': rows[0]['region'],
                 'edges': sorted(tuple(e) for e in rows[0]['extra']['canh'])}
        result.update(reference=ref(ROOT / path), fields='three world rankings, P tiers/two regions and used edges',
                      exact=before == after, differences=differences(before, after))
    elif job['kind'] in ('baseline', 'torai_pipeline'):
        if s['arm'] == 'torai_A':
            candidates_A = tt_tables['methods']['torai_A']['source_records']
            matches = [p for p in candidates_A if p['opaque_id'] == s['opaque_id'] and p['seed'] == s['seed']]
        else:
            matches = [b['source_ref'] for b in baseline_refs if all(b[k] == s[k] for k in ('dataset','opaque_id','arm','seed'))]
            if not matches:
                table = tt_tables['methods'] if s['dataset'] == 'RE2-TT' else ob_tables['tables']['main']['methods']
                method_key = {'microrank': 'microrank_full', 'circa': 'circa_ols_da'}.get(s['arm'], s['arm'])
                matches = [p for p in table[method_key]['source_records']
                           if p['opaque_id'] == s['opaque_id'] and read_pin(p).get('seed') == s['seed']]
        assert len(matches) == 1
        expected = read_pin(matches[0])
        fields = ('method','mode','seed','status','error','window','blocks','entity_ranking','ranking_native','observed_entities','diagnostics')
        before = {k: expected.get(k) for k in fields}; after = {k: rows[0].get(k) for k in fields}
        # metric_columns do runner cũ gắn để audit. Envelope mới pin nguồn/đầu vào riêng.
        before['input_shape'] = {k:v for k,v in (expected.get('input_shape') or {}).items() if k != 'metric_columns'}
        after['input_shape'] = {k:v for k,v in (rows[0].get('input_shape') or {}).items() if k != 'metric_columns'}
        provenance_extra = {'information_boundary','pilot_only','pilot_view','source_view','source_provenance_file'}
        before['extra'] = {k:v for k,v in (expected.get('extra') or {}).items() if k not in provenance_extra}
        after['extra'] = {k:v for k,v in (rows[0].get('extra') or {}).items() if k not in provenance_extra}
        if s['arm'] in ('torai_A','torai_B') and s['dataset'] == 'RE2-TT':
            before['prep_details'] = expected.get('extra',{}).get('chuan_bi')
            after['prep_details'] = rows[0].get('extra',{}).get('chuan_bi')
        result.update(reference=matches[0], fields='status/error/window/shape/diagnostics/full ranking and TORAI prep details',
                      exact=before == after, differences=differences(before,after),
                      metadata_differences='run/config IDs, provenance/input hashes and cost move to envelope/attempt; old extra pilot_only/pilot_view/source_view/source_provenance_file are driver metadata; information_boundary added to new TORAI. All scientific extra fields incl M4 votes compared. method_version is wrapper label; variants checked by verify_attempt, historical error variant may be native')
        if s['arm'] == 'circa' and s['dataset'] == 'RE2-TT':
            aux = [p for p in tt_tables['methods']['circa_ols_rht']['source_records'] if p['opaque_id'] == s['opaque_id']]
            assert len(aux) == 1
            ar = read_pin(aux[0]); a = {k:ar.get(k) for k in fields}; b = {k:rows[1].get(k) for k in fields}
            result['CIRCA_aux_exact'] = a == b
            result['CIRCA_aux_differences'] = differences(a,b)
    else:
        candidate = next(c for c in candidates if c['opaque_id'] == s['opaque_id'] and c['window'] == 'that')
        index = int(Path(candidate['native_record']['path']).parent.name.rsplit('-',1)[1])
        path = f'results/T-051/t12-001/{index:02d}.json'
        expected_row = read_pin(dict(m51['outputs'][path], path=path))
        assert expected_row['job']['opaque_id'] == s['opaque_id']
        expected = expected_row['controls'][0]['C-d3']
        before = {k: expected[k] for k in ('trang_thai','blocks','diem_ung_vien')}
        after = {k: rows[0][k] for k in ('trang_thai','blocks','diem_ung_vien')}
        result.update(reference=ref(ROOT/path), fields='C-d3 status/full ranking/exact candidate points, sealed main input unchanged',
                      exact=before==after, differences=differences(before,after),
                      note='Same-case reference found in T051 T12 observed-edge controls; earlier progress note lacked this reference. Real case only covers its observed solver branch.')
    results.append(result)
atomic(dest / (sys.argv[2] if len(sys.argv)>2 else 'parity.json'), {'status': 'FIELDWISE_EXACT_COMPARISONS_NO_TOLERANCE_ADDED', 'rows': results,
       'all_compared_exact': all(r['exact'] is not False and r.get('CIRCA_aux_exact') is not False for r in results),
       'test_opened': False, 'source_files_verified_before_method': True,
       'limitations': ['C-d3 real case covers its observed branch; other branches exercised by generated fixtures', 'small DEV packet does not prove whole cohort parity or branch coverage',
                       'runtime metadata differences declared separately; not inferred away as numerical tolerance']})
print(json.dumps({'compared': len(results), 'not_exact': [r for r in results if r.get('exact') is False or r.get('CIRCA_aux_exact') is False]},ensure_ascii=False))
