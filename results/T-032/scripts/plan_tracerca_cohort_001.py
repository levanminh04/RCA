"""Authenticated frozen metadata and pilot-based estimates; no native calls."""
from pathlib import Path
import hashlib
import json
import math

REPO = Path('D:/RCA-flashticket')
OUT = REPO / 'results/T-032/runs/tracerca-cohort-proposal-001'
PILOTS = REPO / 'results/T-032/runs/tracerca-path-pilots-002'
PINS = {
    'results/T-024/ban-ghi-dua-vao-cham.json': '2d8a11fa8beb83e07989d89f08fc604dff9bd85d1856acc707326a52e9f2e285',
    'results/T-026/ban-ghi-dua-vao-cham.json': 'c2926067fbbc9c227c735a5d22a44b849c7bcfd44fa7de57d249aeef486511d6',
    'results/T-029/runs/compare-rca-preparation-001/manifest.json': '51498845f1e070017ec52c3b6550b84c444882af7c09aa31564d93c58972c2a8',
    'results/T-026/runs/session-005/handoff-manifest.json': '675092feac86d62908fb6a83f1356a2fc1ab128c717c4018f50433710abb7366',
    'results/T-032/runs/tracerca-pilots-root-001/closed-inventory.json': 'a9019b899c3e0c095878767e4c917ea77c5672f7048ec1d5c5ef46ca26a9a6bf',
}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def dump(name, doc):
    with (OUT / name).open('x', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')

def main():
    for rel, expected in PINS.items():
        assert sha(REPO / rel) == expected, rel
    source24 = read(REPO / 'results/T-029/runs/compare-rca-preparation-001/manifest.json')['source_hashes']
    assert source24['results/T-024/ban-ghi-dua-vao-cham.json'] == PINS['results/T-024/ban-ghi-dua-vao-cham.json']
    h26 = read(REPO / 'results/T-026/runs/session-005/handoff-manifest.json')['files']
    assert h26['results/T-026/ban-ghi-dua-vao-cham.json']['sha256'] == PINS['results/T-026/ban-ghi-dua-vao-cham.json']
    inventory = read(REPO / 'results/T-032/runs/tracerca-pilots-root-001/closed-inventory.json')
    # Receipt structure is inspected below; all closed files are authenticated.
    for r in inventory['files']:
        p = REPO / 'results/T-032' / r['path']
        assert p.stat().st_size == r['bytes'] and sha(p) == r['sha256'], r['path']
    state = read(PILOTS / 'status.json')
    assert state['status'] == 'PASS_DTYPE_FIXTURE_ERROR_AUDIT_AND_TWO_PILOTS'
    completed = {x['phase']: x for x in state['completed']}
    pilots = {}
    for ds, phase in [('RE2-TT', 're2-ok'), ('Nezha-OB', 'nezha-ok')]:
        r = read(PILOTS / phase / 'ban-ghi-0.json')
        pilots[ds] = {'dataset': ds, 'opaque_id': r['opaque_id'],
            'spans': r['input_shape']['spans'], 'operations': r['input_shape']['operations'],
            'child_elapsed_s': completed[phase]['cost']['elapsed_s'],
            'worker_wall_s': r['cost']['wall_s'], 'worker_peak_rss_MiB': r['cost']['peak_rss_mb'],
            'closed_child_bytes': sum(p.stat().st_size for p in (PILOTS / phase).rglob('*') if p.is_file()),
            'source': {'path': (PILOTS / phase / 'ban-ghi-0.json').relative_to(REPO).as_posix(), 'sha256': sha(PILOTS / phase / 'ban-ghi-0.json')}}
    reuse = {('RE2-TT', 'dev-03d4910932'): 'posthoc', ('RE2-TT', 'dev-12a1a88069'): 're2-ok',
             ('Nezha-OB', 'dev-14701a3bbb'): 'nezha-ok'}
    rows = []
    for ds, rel, key in [('RE2-TT', 'results/T-024/ban-ghi-dua-vao-cham.json', 'records'),
                         ('Nezha-OB', 'results/T-026/ban-ghi-dua-vao-cham.json', 'unique_records')]:
        doc = read(REPO / rel)
        for i, entry in enumerate(doc[key]):
            if entry['method'] != 'tracerca' or entry.get('seed') is not None or entry.get('source_view', 'main') != 'main':
                continue
            record_path = REPO / entry['path']
            assert sha(record_path) == entry['sha256']
            r = read(record_path)
            assert r['opaque_id'] == entry['opaque_id'] and r['method'] == 'tracerca' and r['mode'] == 'a' and r['hashseed'] == 0
            p = pilots[ds]
            span_ratio = r['input_shape']['spans'] / p['spans']
            ops = r['input_shape'].get('operations')
            # ERROR does not have operation count; explicitly uncertain route.
            op_ratio = 1.0 if ops is None else max(1.0, ops / p['operations'])
            scale = max(1.0, span_ratio * op_ratio)
            completed_phase = reuse.get((ds, r['opaque_id']))
            rows.append({'dataset': ds, 'opaque_id': r['opaque_id'], 'source_status': r['status'],
                'frozen_path': entry['path'], 'frozen_sha256': entry['sha256'],
                'source_index': rel, 'source_pointer': f'/{key}/{i}',
                'code_route': 'reused_pilot' if entry.get('reused_pilot') else 'full',
                'config_id': r['config_id'], 'window': r['window'],
                'spans': r['input_shape']['spans'], 'operations': ops, 'source_worker_wall_s': r['cost']['wall_s'],
                'replay_phase_already_valid': completed_phase,
                'new_method_needed': completed_phase is None,
                'scale_vs_dataset_pilot': scale,
                'estimate_wall_s': 0 if completed_phase else 1.5 * scale * p['child_elapsed_s'],
                'estimate_new_bytes': 0 if completed_phase else math.ceil(1.5 * max(1.0, span_ratio) * p['closed_child_bytes']),
                'estimate_status': 'UNMEASURED_LINEAR_SCALE_WITH_50_PERCENT_MARGIN_NOT_UPPER_BOUND',
                'non_OK_note': None if r['status'] == 'OK' else 'Exact non-OK replay required; no OK mechanism scores; operation count unknown until original route captured'})
    assert len(rows) == len({(r['dataset'], r['opaque_id']) for r in rows}) == 52
    assert sum(r['dataset'] == 'RE2-TT' for r in rows) == 30 and sum(r['dataset'] == 'Nezha-OB' for r in rows) == 22
    assert sum(r['new_method_needed'] for r in rows) == 49
    OUT.mkdir(parents=True, exist_ok=False)
    dump('plan-52.json', {'status': 'AUTHENTICATED_SOURCE_METADATA_ONLY', 'rows': rows,
        'locked_order': 'dataset then opaque_id', 'method_calls': 0, 'cohort_authorized': False})
    forecast = {'status': 'CANDIDATE_NOT_MEASURED_COHORT_NOT_AUTHORIZED', 'pilots': pilots,
        'plan_sha256': sha(OUT / 'plan-52.json'), 'remaining_case_count': 49,
        'estimated_wall_s': sum(r['estimate_wall_s'] for r in rows),
        'estimated_new_bytes': sum(r['estimate_new_bytes'] for r in rows),
        'per_dataset': {ds: {'remaining': sum(r['new_method_needed'] and r['dataset'] == ds for r in rows),
                            'wall_s': sum(r['estimate_wall_s'] for r in rows if r['dataset'] == ds),
                            'bytes': sum(r['estimate_new_bytes'] for r in rows if r['dataset'] == ds)} for ds in pilots},
        'limits': ['one OK pilot per dataset does not bound future latency/RAM/bytes',
                   'three unrun ERROR routes have unknown operation count; retained with conservative OK-route estimate',
                   '50 percent margin is a forecast convention, not measured confidence or scientific tolerance',
                   'no new method/fixture/audit executed; closed prior results retained and reused',
                   'fresh total task inventory and per-case runtime limits required before any proposed launch'],
        'sources': PINS, 'closed_prior_files_checked': len(inventory['files'])}
    dump('forecast.json', forecast)
    dump('manifest.json', {'status': forecast['status'], 'files': [
        {'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(OUT.iterdir()) if p.is_file()]})
    print(json.dumps({k:forecast[k] for k in ('status','remaining_case_count','estimated_wall_s','estimated_new_bytes','per_dataset')}))

if __name__ == '__main__':
    main()
