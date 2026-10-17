"""T-038: kiểm đầu vào có sẵn; không mạng, không raw telemetry, không bytecode."""
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/T-038'


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def verify(row):
    got = digest(ROOT / row['path'])
    return {'path': row['path'], **got,
            'ok': got['sha256'] == row['sha256'] and
            ('bytes' not in row or got['bytes'] == row['bytes'])}


def main():
    run = OUT / 'runs' / sys.argv[1]
    run.mkdir(parents=True, exist_ok=False)
    (run / 'preflight.py').write_bytes(Path(__file__).read_bytes())
    start = time.monotonic()
    result = {'task': 'T-038', 'client_date': '2026-10-15',
              'captured_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'command': 'py -3 -X utf8 -B results/T-038/preflight.py ' + sys.argv[1],
              'environment': {'python': sys.version, 'platform': platform.platform(),
                              'device': os.environ.get('COMPUTERNAME'),
                              'bytecode_disabled': bool(sys.dont_write_bytecode)},
              'cost_note': 'Kiểm tính toàn vẹn, không là benchmark thời gian/RAM.'}
    try:
        baseline = {}
        names = subprocess.check_output(['git', 'ls-files', '-m', '-z'], cwd=ROOT).decode().split('\0')
        for name in names:
            if name and (ROOT / name).is_file():
                baseline[name] = digest(ROOT / name)
        for name in ['tasks/T-038-p5b-trainticket/SPEC.md',
                     'tasks/T-038-p5b-trainticket/LOG.md',
                     'docs/STATE.md', 'docs/review-prompt.md']:
            baseline[name] = digest(ROOT / name)
        (run / 'baseline.json').write_text(json.dumps(baseline, indent=2), encoding='utf-8')
        for name, target in [('docs/STATE.md', 'STATE-before.md'),
                             ('tasks/T-038-p5b-trainticket/LOG.md', 'LOG-before.md')]:
            (run / target).write_bytes((ROOT / name).read_bytes())
        manifest36 = read('results/T-036/manifest.json')
        result['pin'] = {key: manifest36[key] for key in ['created_utc', 'current_run']}
        assert result['pin'] == {'created_utc': '2026-10-15T13:45:08.305188+00:00',
                                 'current_run': 'runs/kiem-r1-after-002'}
        result['t036_files'] = [verify(x) for x in manifest36['files']]
        assert all(x['ok'] for x in result['t036_files'])
        pin = 'results/T-036/runs/kiem-r1-after-002/'
        hashes = read(pin + 'code-hashes.json')
        result['pinned_code'] = []
        for name, expected in hashes.items():
            current = digest(ROOT / name)
            snapshot = digest(ROOT / pin / 'code' / Path(name).name)
            row = {'path': name, 'expected': expected, 'current': current, 'snapshot': snapshot,
                   'ok': current['sha256'] == snapshot['sha256'] == expected}
            result['pinned_code'].append(row)
        assert all(x['ok'] for x in result['pinned_code'])
        registry = read('results/T-036/nguon.json')
        manifest2 = read('results/T-002/handoff-manifest.json')
        old = {x['path']: x for x in manifest2['artifacts']}
        result['rcaeval_sources'] = []
        for source in registry['sources']:
            if source['system'] != 'RE2-TT':
                continue
            got = verify(source)
            got['source_id'] = source['id']
            got['handoff_ok'] = old[source['path']]['sha256'] == got['sha256']
            result['rcaeval_sources'].append(got)
        assert all(x['ok'] and x['handoff_ok'] for x in result['rcaeval_sources'])
        result['t002_public_metadata'] = [verify(x) for x in manifest2['artifacts']
                                         if x['path'].startswith('results/T-002/public-metadata/run-002/')]
        assert all(x['ok'] for x in result['t002_public_metadata'])
        manifest35 = read('results/T-035/manifest.json')
        prefix = 'results/T-035/do-thi/RE2-TT/'
        files = [x for x in manifest35['files'] if x['path'].startswith(prefix)]
        assert files and len({x['path'] for x in files}) == len(files)
        result['graphs'] = [verify(x) for x in files]
        assert all(x['ok'] for x in result['graphs'])
        result['t035_documents'] = [verify(x) for x in manifest35['files'] if x['path'] in {
            'results/T-035/dac-ta-do-thi.md', 'results/T-035/thong-tin-theo-quan-he.md',
            'results/T-035/input-verification.json', 'results/T-035/prepare.py',
            'results/T-035/plan.json'}]
        assert all(x['ok'] for x in result['t035_documents'])
        counts = collections.Counter()
        dev_ids = set()
        for entry in files:
            tail = entry['path'][len(prefix):].split('/')
            assert len(tail) == 3 and tail[0].startswith('dev-')
            dev_ids.add(tail[0])
            family = tail[-1].split('-')[0].removesuffix('.json')
            counts[(tail[1], family)] += 1
        result['graph_selection'] = {
            'manifest': 'results/T-035/manifest.json', 'prefix': prefix,
            'exclude_history': True, 'count': len(files),
            'bytes': sum(x['bytes'] for x in files), 'opaque_dev_ids': sorted(dev_ids),
            'by_level_family': [{'level': a, 'family': b, 'count': n}
                                for (a, b), n in sorted(counts.items())]}
        result['input_manifests'] = {p: digest(ROOT / p) for p in [
            'results/T-036/manifest.json', 'results/T-036/nguon.json',
            pin + 'code-hashes.json', 'results/T-035/manifest.json',
            'results/T-002/handoff-manifest.json']}
        result['ok'] = True
    except BaseException as exc:
        result['ok'] = False
        result['error'] = repr(exc)
        raise
    finally:
        result['integrity_check_wall_seconds'] = time.monotonic() - start
        (run / 'input-verification.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'ok': result['ok'], 'run': str(run),
                          'graph_selection': result.get('graph_selection'),
                          'error': result.get('error')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
