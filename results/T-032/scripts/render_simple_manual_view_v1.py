"""Copy checked saved SimpleRCA scalars, retaining every case and control.

EC2 only. Long row-position witnesses remain linked to the pinned full chain.
No method, new selection, numerical threshold or mechanism label is executed.
"""
from pathlib import Path
import hashlib
import json
import platform

BASE = Path('/home/ubuntu/rca/T-032/runs')
SOURCE = BASE / 'execution-research-simple-004/simplerca-saved-chains.json'
OUT = BASE / 'research-simple-manual-view-001'
EXPECTED = '17c2964a5a1e8677d690bd87ad7ae1e706acd13ba1bb588fa6fe18d3be6a256b'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def dump(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def channel(row, pointer):
    # Keep every already checked scalar. The complete witness stays pinned.
    result = {key: value for key, value in row.items() if key != 'row_witness'}
    result['full_chain_pointer'] = pointer
    if 'quantile_N' in row.get('row_witness', {}):
        result['quantile_witness_N'] = row['row_witness']['quantile_N']
        result['quantile_witness_A'] = row['row_witness']['quantile_A']
    return result


def main():
    assert platform.system() == 'Linux'
    assert sha(SOURCE) == EXPECTED
    original = json.loads(SOURCE.read_text(encoding='utf-8'))
    assert original['counts']['cases'] == 52
    assert original['manual_reading_complete'] is False
    OUT.mkdir(exist_ok=False)
    cases = []
    for i, case in enumerate(original['cases']):
        copied = {key: value for key, value in case.items()
                  if key not in ('metrics', 'traces', 'logs')}
        copied['source_pointer'] = f'/cases/{i}'
        for kind in ('metrics', 'traces', 'logs'):
            copied[kind] = [channel(row, f'/cases/{i}/{kind}/{j}')
                            for j, row in enumerate(case[kind])]
            assert len(copied[kind]) == len(case[kind])
        cases.append(copied)
    assert [c['unit_id'] for c in cases] == [c['unit_id'] for c in original['cases']]
    view = {
        'status': 'READING_VIEW_NOT_MANUAL_CONCLUSION',
        'source': str(SOURCE), 'source_sha256': EXPECTED,
        'counts': original['counts'], 'cases': cases,
        'M5_caller_root': original['M5_caller_root'],
        'locked_controls': original['locked_controls'],
        'method_executed': False, 'raw_dataset_read': False,
        'manual_complete': False, 'physical_wait_established': False,
        'projection': 'All checked channel scalars, cases and controls retained without rounding; full row witnesses linked; no reselection.'
    }
    target = OUT / 'reading-view.json'
    dump(target, view)
    assert sha(SOURCE) == EXPECTED
    receipt = {'status': 'PASS', 'source_sha256': EXPECTED,
               'script_sha256': sha(Path(__file__)),
               'files': [{'path': target.name, 'bytes': target.stat().st_size,
                          'sha256': sha(target)}],
               'counts': original['counts'], 'manual_complete': False,
               'physical_wait_established': False}
    dump(OUT / 'manifest.json', receipt)
    print(json.dumps(receipt), flush=True)


if __name__ == '__main__':
    main()
