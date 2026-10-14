"""Transport immutable T-032 SimpleRCA JSON and closed failed-run evidence.

Verify the entire eligible SimpleRCA artifact manifests, including Parquet that
stays on EC2. No adapter or method is imported or called. Failed runs are only
transported; their intermediates never become eligible by this operation.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tarfile
import time
import traceback

BASE = Path('/home/ubuntu/rca/T-032')
STATUS_PIN = '0b9b12c650f06bc210d10cd507f04a208036705ad44db1a4c10406b17c217778'
FAIL_ROOTS = ('tracerca-path-pilots-001', 'tracerca-path-pilots-001-monitor',
              'circa-fixture-001', 'circa-fixture-001-monitor',
              'execution-research-baro-004', 'research-baro-004-monitor')
SUFFIXES = {'.json', '.jsonl', '.txt', '.out', '.err', '.pid'}


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def dump(p, data):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')


def within(p):
    p = Path(p)
    require(not p.is_symlink() and p.resolve().is_relative_to(BASE / 'runs'),
            'input outside T032 runs or symlink: ' + str(p))
    require(not any(x in {'T-033', 'test', 'tests', 'locked'} for x in p.parts),
            'forbidden input')
    return p


def manifest_path(root, rel):
    r = PurePosixPath(rel)
    require(not r.is_absolute() and '..' not in r.parts, 'unsafe artifact path')
    return within(root.joinpath(*r.parts))


def pinned(p, expected, n=None):
    require(p.is_file(), 'missing ' + str(p))
    require(n is None or p.stat().st_size == n, 'size mismatch ' + str(p))
    require(sha(p) == expected, 'hash mismatch ' + str(p))


def prepare(verify):
    status_path = BASE / 'runs/simplerca-batch-001/status.json'
    pinned(status_path, STATUS_PIN)
    status = read(status_path)
    require(status['status'] == 'PASS' and status['n_main_valid'] == 52,
            'SimpleRCA cohort not complete')
    cases = status['completed'] + list(status['reused'].values())
    require(len(cases) == 52 and len({(r['dataset'], r['opaque_id']) for r in cases}) == 52,
            'duplicate or incomplete cases')
    selected = {status_path}
    reports = []
    for r in cases:
        root = within(r['path'])
        audit = 'audit_path' in r
        cp = within(Path(r['audit_path']) / 'check.json') if audit else root / 'check.json'
        pinned(cp, r['audit_check_sha256'] if audit else r['check_sha256'])
        c = read(cp)
        require(c['status'] == 'PASS' and c['intermediates_eligible'] is True
                and c['differences'] == [], 'ineligible SimpleRCA case')
        require(c['dataset'] == r['dataset'] and c['opaque_id'] == r['opaque_id']
                and c['method'] == 'simplerca', 'case identity mismatch')
        require(c['capture_check']['pass'] is True, 'invalid captured formulas')
        if audit:
            require(c['record_exact'] is True and c['original_run'] == str(root), 'bad posthoc audit')
            entries = c['original_artifact_manifest']
        else:
            require(c['compare']['pass'] is True and c['compare']['difference_count'] == 0,
                    'nonexact frozen comparison')
            entries = c['artifact_manifest']
        require(len(entries) == len({x['path'] for x in entries}), 'duplicate manifest entry')
        total = 0
        for e in entries:
            p = manifest_path(root, e['path'])
            require(p.is_file() and p.stat().st_size == e['bytes'], 'missing/size mismatch artifact')
            if verify:
                pinned(p, e['sha256'], e['bytes'])
            total += e['bytes']
            if p.suffix in SUFFIXES:
                selected.add(p)
        pinned(root / 'ban-ghi-0.json', r['record_sha256'])
        selected.add(cp)
        if audit:
            selected.update(p for p in cp.parent.rglob('*') if p.is_file() and p.suffix in SUFFIXES)
        require(root / 'capture/native-result.json' in selected
                and root / 'capture/row-evidence.json' in selected, 'missing actual native/row evidence')
        reports.append({'dataset': r['dataset'], 'opaque_id': r['opaque_id'],
                        'check_path': cp.relative_to(BASE).as_posix(), 'check_sha256': sha(cp),
                        'full_manifest_files': len(entries), 'full_manifest_bytes': total,
                        'full_manifest_hashes_verified': verify, 'audit': audit})
    for name in FAIL_ROOTS:
        root = within(BASE / 'runs' / name)
        require(root.is_dir(), 'missing closed failure directory')
        selected.update(p for p in root.rglob('*') if p.is_file() and p.suffix in SUFFIXES)
    for name in ('tracerca-path-pilots-001-monitor', 'circa-fixture-001-monitor', 'research-baro-004-monitor'):
        c = read(BASE / 'runs' / name / 'status.json')
        require(c['status'] == 'FAIL' and c['exit_code'] != 0, 'failure run still active/changed')
    for p in selected:
        within(p)
    rows = [{'path': p.relative_to(BASE).as_posix(), 'bytes': p.stat().st_size,
             'sha256': sha(p)} for p in sorted(selected)]
    return reports, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['plan', 'export'])
    parser.add_argument('--out')
    parser.add_argument('--max-output-bytes', type=int, default=200 * 2**20)
    args = parser.parse_args()
    started = time.monotonic()
    out = None
    try:
        if args.mode == 'export':
            require(args.out is not None, 'output required')
            out = Path(args.out).expanduser().resolve()
            require(out.parent == BASE / 'runs', 'output outside T032 runs')
            out.mkdir(exist_ok=False)
        reports, before = prepare(args.mode == 'export')
        logical = sum(r['bytes'] for r in before)
        require(logical < args.max_output_bytes, 'export exceeds approved operating reserve')
        result = {'status': 'PLAN' if args.mode == 'plan' else 'PASS',
                  'cases': reports, 'selected_files': len(before), 'selected_logical_bytes': logical,
                  'source_status_sha256': STATUS_PIN, 'methods_executed': False,
                  'failed_intermediates_eligible': False, 'script_sha256': sha(Path(__file__))}
        if out:
            dump(out / 'file-inventory.json', {'files': before, 'cases': reports,
                 'scope': 'Selected JSON/control files; full SimpleRCA manifests checked on EC2, Parquet remains there.'})
            archive = out / 'simple-research-json.tar.gz'
            with tarfile.open(archive, 'x:gz') as tf:
                for r in before:
                    tf.add(BASE / r['path'], arcname=r['path'], recursive=False)
                    require(archive.stat().st_size < args.max_output_bytes, 'archive exceeds reserve')
            for r in before:
                pinned(BASE / r['path'], r['sha256'], r['bytes'])
            result.update(archive=archive.name, archive_bytes=archive.stat().st_size,
                          archive_sha256=sha(archive), inventory_sha256=sha(out / 'file-inventory.json'),
                          closed_bytes_unchanged=True, elapsed_s=time.monotonic() - started)
            dump(out / 'check.json', result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    except BaseException as e:
        if out and not (out / 'check.json').exists():
            dump(out / 'check.json', {'status': 'FAIL_STOP', 'error': str(e),
                 'traceback': traceback.format_exc(), 'methods_executed': False,
                 'failed_intermediates_eligible': False})
        raise


if __name__ == '__main__':
    main()
