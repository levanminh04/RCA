"""Reverify received envelopes, compare pinned DEV records and preserve environment provenance."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
from unittest.mock import patch

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
OUT = ROOT / 'results/T-054'
sys.path[:0] = [str(OUT / 'scripts'), str(ROOT / 'src')]
from bien_nhan import atomic, digest, fingerprint, read_pin, ref, receive_paths, resolve_path, events
from dieu_phoi import verify_attempt
from pilot import comparable


def projection(record):
    fields = ('method', 'mode', 'seed', 'status', 'error', 'window', 'blocks', 'entity_ranking',
              'ranking_native', 'observed_entities', 'diagnostics')
    result = {k: record.get(k) for k in fields}
    result['input_shape'] = {k: v for k, v in (record.get('input_shape') or {}).items() if k != 'metric_columns'}
    excluded = {'information_boundary', 'pilot_only', 'pilot_view', 'source_view', 'source_provenance_file'}
    result['extra'] = {k: v for k, v in (record.get('extra') or {}).items() if k not in excluded}
    return result


def main():
    upstream = Path('D:/RCA-ext/src/RCAEval')
    entries = subprocess.check_output(['git', '-C', str(upstream), 'ls-files', 'RCAEval', 'lib'], text=True).splitlines()
    upstream_pins = {}
    for name in entries:
        if not name.endswith('.py'):
            continue
        target = RUN / 'upstream/rcaeval' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        data = (upstream / name).read_bytes()
        if target.exists():
            assert target.read_bytes() == data
        else:
            target.open('xb').write(data)
        upstream_pins[name] = dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    if not (RUN / 'upstream-pins.json').exists():
        atomic(RUN / 'upstream-pins.json', dict(revision='259ea4167160256a74ad30004aa3d96a998c846e', files=upstream_pins))
    with tarfile.open(RUN / 'dev-package.tar.gz') as archive:
        metadata = json.load(archive.extractfile('dev-metadata.json'))
    expected = {(e['job']['slot']['opaque_id'], e['job']['slot']['arm'], e['job']['slot']['view'], e['job']['slot']['seed']):
                 metadata['references'][e['reference_key']] for e in metadata['jobs']}
    output = {'hosts': {}, 'test_opened': False, 'main_started': False}
    locations = {
        'ec2-large-disk': [('ec2-large-disk-r2', 'checkpoint013-results-002'), ('ec2-large-disk-repair', 'checkpoint013-results-repair')],
        'ec2-small-disk': [('ec2-small-disk-initial', 'checkpoint013-results'), ('ec2-small-disk-repair', 'checkpoint013-results-repair')],
    }
    for host, attempts in locations.items():
        combined = {}
        peaks = defaultdict(int)
        last_environment = None
        for folder, directory in attempts:
            local = RUN / 'received' / folder
            work = local / 'results/T-054/runs' / directory
            environment = json.loads((work / 'environments.json').read_bytes())
            last_environment = {name: environment[name] for name in ('main', 'py38')}
            plan = json.loads((work / 'plan.json').read_bytes())
            receive_paths({
                '/home/ubuntu/rca-p7/T-054/checkpoint013/work': str(local),
                '/home/ubuntu/rca-p7/T-054/checkpoint013/work/src': str(ROOT / 'src'),
                '/home/ubuntu/rca-p7/T-054/checkpoint013/work/upstream/rcaeval': str(RUN / 'upstream/rcaeval'),
                '/home/ubuntu/rca-p7/T-054/checkpoint012/work': str(OUT / 'runs/danh-gia-ec2-moi-012/received' / host),
            })
            try:
                for job in plan['jobs']:
                    s = job['slot']
                    key = (s['opaque_id'], s['arm'], s['view'], s['seed'])
                    if s['arm'] == 'M1' and s['view'] == 'main':
                        continue
                    path = work / 'queue' / fingerprint(s) / 'attempt-001'
                    if not (path / 'result.json').exists():
                        continue
                    envelope = json.loads((path / 'result.json').read_bytes())
                    if envelope['records'][0]['status'] in ('ERROR', 'TIMEOUT') and not (path / 'dev-error-reproduction.json').exists():
                        continue  # preserved failed environment; use the repaired route below
                    invocation = json.loads((path / 'invocation.json').read_bytes())
                    def received_digest(path):
                        value = str(path).replace('\\', '/')
                        if value.startswith(ROOT.drive + '/home/'):
                            value = value[len(ROOT.drive):]
                        return digest(resolve_path(value))
                    # The historical DEV classifier constructs Path directly for code evidence.
                    # Resolve its immutable remote locator to the byte-checked received source.
                    with patch('bien_nhan.digest', side_effect=received_digest):
                        records = verify_attempt(path, job, envelope['token'])
                    observed = records[0]
                    if key in expected:
                        before = expected[key]
                        if before['kind'] == 'M1':
                            a, b = comparable(before['record'], before.get('control', False)), comparable(observed, before.get('control', False))
                        elif before['kind'] == 'T12':
                            a = before['fields']
                            b = dict(world_blocks={w: observed['worlds'][w]['blocks'] for w in ('P', 'S_lo', 'S_hi')},
                                     P_tiers=observed['extra']['tang_P'], P_region=observed['region'],
                                     edges=sorted(map(tuple, observed['extra']['canh'])))
                        else:
                            a, b = projection(before['record']), projection(observed)
                        exact = fingerprint(a) == fingerprint(b)
                        if not exact:
                            difference_path = RUN / 'comparison-differences' / (host + '-' + fingerprint(s) + '.json')
                            difference = dict(expected=a, observed=b)
                            if difference_path.exists():
                                assert read_pin(ref(difference_path)) == difference
                            else:
                                atomic(difference_path, difference)
                        reference = before['origin']
                    else:
                        assert s['arm'] == 'C-d3'
                        a = {k: observed[k] for k in ('trang_thai', 'blocks', 'diem_ung_vien')}
                        m51 = json.loads((ROOT / 'results/T-051/manifest.json').read_bytes())['outputs']
                        reference = dict(m51['results/T-051/t12-001/05.json'], path='results/T-051/t12-001/05.json')
                        old = read_pin(reference)['controls'][0]['C-d3']
                        exact = a == {k: old[k] for k in a}
                    samples = []
                    for log in path.rglob('monitor.jsonl'):
                        samples.extend(events(log))
                    peak = max((r.get('tree_rss', 0) for r in samples), default=0)
                    group = s['dataset'] + '|' + s['arm']
                    peaks[group] = max(peaks[group], peak)
                    row = dict(slot=s, PASS=exact, status=observed['status'], reference=reference,
                               result=ref(path / 'result.json'), invocation=ref(path / 'invocation.json'),
                               wall_s=read_pin(ref(path / 'cost.json'))['wall_s'], peak_rss=peak,
                               max_gap=max((r.get('max_monitor_gap_s', 0) for r in samples), default=None),
                               normalized_input_sha256=invocation['normalized_input_sha256'])
                    combined[key] = row
            finally:
                receive_paths({})
        fixture = RUN / 'received' / (host + '-fixture-final') / 'results/T-054/runs/checkpoint013-fixture-final/summary.json'
        fixture_summary = json.loads(fixture.read_bytes())
        stage = json.loads((RUN / (host + '-stage.json')).read_bytes())
        identity = json.loads(stage['stdout'])['instance_id']
        output['hosts'][host] = dict(PASS=all(row['PASS'] for row in combined.values()) and fixture_summary['PASS'],
              instance_id=identity, environments=last_environment, peaks=dict(peaks),
              rows=list(combined.values()), fixture=ref(fixture), fixture_count=fixture_summary['count'])
    got = {(r['slot']['opaque_id'], r['slot']['arm'], r['slot']['view'], r['slot']['seed'])
           for host in output['hosts'].values() for r in host['rows']}
    assert got == set(expected) | {('dev-a915aa2424', 'C-d3', 'main', None)}, (got - set(expected), set(expected) - got)
    output['PASS'] = all(host['PASS'] for host in output['hosts'].values())
    atomic(RUN / 'cloud-verification.json', output)
    print(json.dumps(dict(PASS=output['PASS'], hosts={k: dict(rows=len(v['rows']), fixture_count=v['fixture_count'], PASS=v['PASS'])
                                                   for k, v in output['hosts'].items()})))


if __name__ == '__main__':
    main()
