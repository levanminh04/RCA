"""Transport closed T-032 runs with complete before/after byte inventories."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import time

BASE = Path('/home/ubuntu/rca/T-032')
ROOTS = {
    'baro-nezha': ('baro-nezha-first-001', 'baro-nezha-plan-001',
                   'baro-nezha-batch-001', 'baro-nezha-audit-001'),
    'coverage': ('trace-coverage-re2-first-001', 'trace-coverage-nezha-first-001',
                 'trace-coverage-plan-001', 'trace-coverage-batch-001'),
}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')


def inventory(paths):
    rows = []
    for root in paths:
        if not root.is_dir() or root.is_symlink():
            raise RuntimeError('Missing/symlinked closed run: ' + str(root))
        for p in sorted(root.rglob('*')):
            if p.is_symlink():
                raise RuntimeError('Symlink in output tree')
            if p.is_file():
                rows.append({'path': p.relative_to(BASE).as_posix(), 'bytes': p.stat().st_size,
                             'sha256': digest(p)})
    return sorted(rows, key=lambda r: r['path'])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('kind', choices=ROOTS)
    p.add_argument('new_output')
    args = p.parse_args()
    out = Path(args.new_output).expanduser().resolve()
    if out.parent != BASE / 'runs':
        raise RuntimeError('Output outside approved T032 runs')
    out.mkdir(exist_ok=False)
    start = time.perf_counter()
    names = ROOTS[args.kind]
    for name in names:
        monitor = read(BASE / 'runs' / (name + '-monitor') / 'status.json')
        if monitor['status'] != 'PASS' or monitor['exit_code'] != 0:
            raise RuntimeError('Cannot export incomplete run: ' + name)
    if args.kind == 'baro-nezha':
        audit = read(BASE / 'runs/baro-nezha-audit-001/checks.json')
        if audit['status'] != 'PASS' or audit['n_main_valid'] != 22:
            raise RuntimeError('BARO audit not complete')
        for row in audit['cases']:
            cp = Path(row['check_path']).resolve()
            if not cp.is_relative_to(BASE / 'runs') or digest(cp) != row['check_sha256']:
                raise RuntimeError('Audit case binding changed')
    else:
        status = read(BASE / 'runs/trace-coverage-batch-001/status.json')
        if status['status'] != 'PASS' or len(status['completed']) + len(status['reused']) != 52:
            raise RuntimeError('Coverage not complete')
    paths = [BASE / 'runs' / name for name in names]
    paths += [BASE / 'runs' / (name + '-monitor') for name in names]
    before = inventory(paths)
    dump(out / 'file-inventory.json', {'files': before, 'kind': args.kind,
        'note': 'Transport byte inventory; substantive checks remain in the included run checks.'})
    archive = out / (args.kind + '-verified.tar.gz')
    with tarfile.open(archive, 'x:gz') as tar:
        for row in before:
            tar.add(BASE / row['path'], arcname=row['path'], recursive=False)
    after = inventory(paths)
    if before != after:
        raise RuntimeError('Closed output changed while archiving; retain archive but do not use')
    dump(out / 'check.json', {'status': 'PASS', 'kind': args.kind,
        'closed_run_bytes_unchanged': True, 'n_files': len(before),
        'logical_bytes': sum(r['bytes'] for r in before),
        'inventory_sha256': digest(out / 'file-inventory.json'),
        'archive': archive.name, 'archive_bytes': archive.stat().st_size,
        'archive_sha256': digest(archive), 'elapsed_s': time.perf_counter() - start,
        'methods_executed': False, 'script_sha256': digest(Path(__file__))})
    print(json.dumps(read(out / 'check.json')), flush=True)


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        raise
