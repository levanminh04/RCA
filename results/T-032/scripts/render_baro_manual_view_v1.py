"""Copy exact checked BARO values into a compact reading view on EC2.

All cases, caller relationships and locked controls remain linked. This is a
layout projection, not a new sample or a new mechanism classification.
"""
from pathlib import Path
import hashlib
import json

BASE = Path('/home/ubuntu/rca/T-032/runs')
SOURCE = BASE / 'execution-research-baro-006/baro-saved-chains.json'
OUT = BASE / 'research-baro-manual-view-001'
EXPECTED = '225e3680773b0d2d08781fad87a71cba175e7d914bd08064e44fec6b3b43b2ea'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, value):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')


def metric(row):
    fields = ['column', 'entity', 'median_N', 'quantiles_N', 'raw_IQR_N',
              'effective_denominator', 'scale_fallback_observed', 'signed_max_robust_z',
              'max_positions_A', 'max_input_indices', 'max_adapter_time_markers',
              'max_preprocessed_values', 'numerator_at_max', 'sample_sizes', 'source']
    return {key: row[key] for key in fields}


def service(row):
    return {key: [metric(x) for x in value] if key == 'max_metrics' else value
            for key, value in row.items() if key != 'all_retained_metric_pointers'}


def main():
    assert str(SOURCE).startswith('/home/ubuntu/rca/T-032/') and sha(SOURCE) == EXPECTED
    original = json.loads(SOURCE.read_text(encoding='utf-8'))
    assert original['counts']['cases'] == 52 and original['manual_reading_complete'] is False
    OUT.mkdir(exist_ok=False)
    cases = []
    for i, case in enumerate(original['cases']):
        cases.append({'source_pointer': f'/cases/{i}', 'unit_id': case['unit_id'],
            'opaque_id': case['opaque_id'], 'dataset': case['dataset'],
            'configuration': case['configuration'], 'window': case['window'],
            'T028_context': case['T028_context'], 'source': case['source'],
            'column_stages': case['column_stages'], 'time_axis_semantics': case['time_axis_semantics'],
            'root': service(case['root_score_chain']),
            'caller_root': [{key: service(value) if key in ('caller', 'root') else value
                            for key, value in row.items()} for row in case['caller_root_observations']],
            'all_metric_chain_source': f'/cases/{i}/metric_chains',
            'all_ranking_source': f'/cases/{i}/entity_ranking'})
    assert len(cases) == 52 and [c['unit_id'] for c in cases] == [c['unit_id'] for c in original['cases']]
    view = {'status': 'READING_VIEW_NOT_MANUAL_CONCLUSION', 'source': str(SOURCE),
        'source_sha256': EXPECTED, 'counts': original['counts'], 'cases': cases,
        'M5_caller_root': [{'opaque_id': row['opaque_id'], 'dataset': row['dataset'],
                           'case_chain_pointer': row['case_chain_pointer'], 'source_M5_k': row['source_M5_k']}
                          for row in original['M5_caller_root']],
        'locked_controls': original['locked_controls'], 'method_executed': False,
        'raw_dataset_read': False, 'manual_complete': False, 'physical_wait_established': False,
        'projection': 'Values copied without rounding; long array metadata stays linked to full checked chains; no case/control reselection.'}
    target = OUT / 'reading-view.json'
    dump(target, view)
    assert sha(SOURCE) == EXPECTED
    dump(OUT / 'manifest.json', {'status': 'PASS', 'source_sha256': EXPECTED,
        'script_sha256': sha(Path(__file__)), 'files': [{'path': target.name,
        'bytes': target.stat().st_size, 'sha256': sha(target)}], 'counts': original['counts'],
        'manual_complete': False, 'physical_wait_established': False})
    print(json.dumps({'status': 'PASS', 'path': str(target), 'bytes': target.stat().st_size,
                      'sha256': sha(target)}), flush=True)


if __name__ == '__main__':
    main()
