"""T-026: kiểm toàn vẹn/phạm vi và bất biến các bảng; không chạy phương pháp."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import ast

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-026'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evaluate as ev

def read(p):
    return ev.read_json(p)

def verify(final=False):
    base = read(OUT / 'runs/session-005/baseline.json')
    mutable = {'docs/STATE.md', 'tasks/T-026-nezha-ob-che-do-a/LOG.md',
               'results/T-026/cham-a.md', 'results/T-026/chi-phi.md'}
    changed = [p for p, h in base['files'].items() if not (ROOT / p).is_file() or ev.sha(ROOT / p) != h]
    unexpected = sorted(set(changed) - mutable)
    if unexpected:
        raise ValueError('unexpected baseline change: ' + str(unexpected))
    log_path = 'tasks/T-026-nezha-ob-che-do-a/LOG.md'
    log_bytes = (ROOT / log_path).read_bytes()
    marker = '\n\n## Phiên 5 —'.encode('utf-8')
    cut = log_bytes.find(marker)
    if cut < 0 or hashlib.sha256(log_bytes[:cut]).hexdigest() != base['files'][log_path]:
        raise ValueError('LOG initial prefix changed')
    initial_row = read(OUT / 'runs/session-005/state-initial-row.json')['initial_row']
    state = (ROOT / 'docs/STATE.md').read_text(encoding='utf-8')
    restored = ''.join(initial_row + '\n' if line.startswith('| T-026 |') else line
                       for line in state.splitlines(True))
    if hashlib.sha256(restored.encode('utf-8')).hexdigest() != base['files']['docs/STATE.md']:
        raise ValueError('STATE changed outside T026 row')
    original = read(OUT / 'runs/session-004/final-verification.json')
    for p, h in original['src_p3']['tep'].items():
        if ev.sha(ROOT / p) != h:
            raise ValueError('src/p3 changed since valid regression: ' + p)
    cache = read(OUT / 'runs/session-004/t030-synthetic-work-manifest.json')
    for directory in cache['directories']:
        for meta in directory['files']:
            if ev.sha(ROOT / meta['path']) != meta['sha256']:
                raise ValueError('T030 retained cache changed')
    allow = read(OUT / 'allowlist-dev.json')
    ids = {c['opaque_id'] for c in allow['cases']}
    if len(ids) != 22:
        raise ValueError('cohort not22')
    plan = read(OUT / 'runs/full-001/plan.json')
    unique = {e['path']: read(ROOT / e['path']) for e in plan['unique_records']}
    authorization = read(OUT / 'runs/full-001/continuation-authorization-001.json')
    for name, expected in authorization['retained_records'].items():
        if ev.sha(ROOT / name) != expected:
            raise ValueError('continuation changed a historical record')
    for name, expected in authorization['historical_files'].items():
        if name.endswith('progress.jsonl'):
            data = (ROOT / name).read_bytes()
            end = 0
            for line in data.splitlines(keepends=True):
                end += len(line)
                if json.loads(line)['event'] == 'FULL_DONE':
                    break
            if hashlib.sha256(data[:end]).hexdigest() != expected:
                raise ValueError('progress historical prefix changed')
        elif ev.sha(ROOT / name) != expected:
            raise ValueError('continuation changed historical output')
    completed = read(OUT / 'runs/full-001/summary-continued-001.json')
    if not completed['complete'] or not completed['continuation_authorized'] or len(completed['runs']) != 248:
        raise ValueError('conditional continuation incomplete')
    for e in plan['unique_records']:
        rec = unique[e['path']]
        job = read((ROOT / e['path']).parent / 'job.json')
        if set(job) != {'allowlist_path', 'opaque_id', 'repo_root', 'view', 'method', 'trace_guard_s'}:
            raise ValueError('job unexpected fields')
        if job['opaque_id'] not in ids or job['opaque_id'] != rec['opaque_id']:
            raise ValueError('job outside dev')
        expected_view = 'sensitivity_A' if e['source_view'] == 'sensitivity_A' else 'main'
        if job['view'] != expected_view or job['trace_guard_s'] != e['trace_guard_s']:
            raise ValueError('job view/guard differs')
    refs = {name: {(m['worker_method'], m['opaque_id']): m['path'] for m in t['records']}
            for name, t in plan['tables'].items()}
    coverage = read(OUT / 'runs/session-005/trace-N-coverage.json')
    if len(coverage['cases']) != 22 or {c['opaque_id'] for c in coverage['cases']} != ids:
        raise ValueError('coverage cohort differs')
    for case in coverage['cases']:
        oid = case['opaque_id']
        main_rec = unique[refs['main']['microrank', oid]]
        cut_rec = unique[refs['trace_guard']['microrank', oid]]
        for rec, field in ((main_rec, 'main_N_observed'), (cut_rec, 'cut_N_observed')):
            if case[field]['spans'] != rec['diagnostics']['trace_rows_N_end']:
                raise ValueError('coverage differs from saved N count')
        if (case['A_rows_main'] != main_rec['diagnostics']['trace_rows_A_end'] or
                case['A_rows_cut'] != cut_rec['diagnostics']['trace_rows_A_end'] or
                case['microrank_guard_status'] != cut_rec['status']):
            raise ValueError('coverage differs from saved A/status')
    invariant_checks = []
    for oid in sorted(ids):
        for method in ('simplerca', 'microrank', 'tracerca'):
            main = unique[refs['main'][method, oid]]
            guard = unique[refs['trace_guard'][method, oid]]
            if 'TIMEOUT' in (main['status'], guard['status']):
                invariant_checks.append({'opaque_id': oid, 'method': method, 'pass': None,
                                         'reason': 'TIMEOUT has no output to verify A; retained in denominator'})
                continue
            if main['window'] != {**guard['window'], 'trace_guard_s': 0}:
                raise ValueError('guard changed outer window/A counts')
            main_output = read((ROOT / refs['main'][method, oid]).parent / 'ket-qua.json')
            guard_output = read((ROOT / refs['trace_guard'][method, oid]).parent / 'ket-qua.json')
            if main_output['provenance'] != guard_output['provenance'] or main_output['input_sha256'] != guard_output['input_sha256']:
                raise ValueError('guard changed source/provenance/channel/clock')
            if method == 'simplerca':
                keys = ('trace_rows_A_start',)
                for key in ('metric_rows_N_per_channel', 'metric_rows_A_per_channel', 'log_rows_A'):
                    if main['input_shape'][key] != guard['input_shape'][key]:
                        raise ValueError('guard changed Simple metric/log input')
            else:
                keys = ('trace_rows_A_end',)
            for key in keys:
                if main['diagnostics'][key] != guard['diagnostics'][key]:
                    raise ValueError('guard changed A membership')
            invariant_checks.append({'opaque_id': oid, 'method': method, 'pass': True})
    source = read(OUT / 'runs/full-001/source-integrity-final.json')
    for meta in source['files']:
        p = ROOT / meta['path']
        if p.stat().st_size != meta['bytes'] or ev.sha(p) != meta['sha256']:
            raise ValueError('source data changed')
    payload = [ev.rel(p) for p in OUT.rglob('*') if p.is_file() and p.suffix.lower() in ('.csv', '.parquet', '.npy', '.npz', '.pkl')]
    work = [ev.rel(p) for p in (OUT / 'work').rglob('*') if p.is_file()]
    if payload or work:
        raise ValueError('derived payload/work remains')
    strict_count = 0
    for p in OUT.rglob('*.json'):
        read(p)
        strict_count += 1
    for p in (OUT / 'scripts').glob('*.py'):
        ast.parse(p.read_text(encoding='utf-8'))
    if ev.code_hash() != original['src_p3']['tong']:
        raise ValueError('code hash differs')
    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pass': True,
              'baseline_changed': changed, 'unexpected_changes': unexpected,
              'src_p3_sha256': ev.code_hash(), 'source_files_verified': len(source['files']),
              'retained_T030_cache_dirs': cache['directory_count'], 'unique_records': len(unique),
              'job_ids_dev_only': True, 'LOG_prefix_preserved': True, 'STATE_only_T026_row': True,
              'guard_invariant_checks': invariant_checks,
              'coverage_N_A_saved_record_checks': 22,
              'json_strict_count': strict_count, 'payload_files': payload, 'work_files': work,
              'full_counts': plan['counts'], 'phase': 'final' if final else 'before_freeze'}
    if final:
        manifest = read(OUT / 'ban-ghi-dua-vao-cham.json')
        ev.load_manifest(OUT / 'ban-ghi-dua-vao-cham.json')
        scoring = read(OUT / 'cham-a.json')
        if not scoring['validation']['non_OK_in_denominator'] or scoring['validation']['n_independent_case_checks'] != 609:
            raise ValueError('evaluation verification incomplete')
        log = (ROOT / 'tasks/T-026-nezha-ob-che-do-a/LOG.md').read_text(encoding='utf-8')
        if manifest['frozen_at'] not in log or scoring['generated_at_utc'] <= manifest['frozen_at']:
            raise ValueError('freeze not before actual evaluator')
        result.update(frozen_at=manifest['frozen_at'], first_evaluator_at=scoring['generated_at_utc'], independent_case_checks=609,
                      cohort_sizes={n: t['n_cases'] for n, t in scoring['tables'].items()},
                      cell_sizes={n: t['cell_sizes'] for n, t in scoring['tables'].items()})
    return result

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--final', action='store_true')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    doc = verify(args.final)
    ev.dump(args.output, doc)
    print(json.dumps({'pass': True, 'phase': doc['phase'], 'records': doc['unique_records'], 'jsons': doc['json_strict_count']}, ensure_ascii=True))
