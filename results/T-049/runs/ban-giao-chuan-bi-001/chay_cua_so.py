"""Chạy một cửa sổ từ ma trận T-049, lưu native và trung gian không ghép nhãn."""
import argparse
import gzip
import hashlib
import json
import os
import platform
import shutil
import sys
import time
from importlib.metadata import version
from pathlib import Path

from chuan_bi import OUT, ROOT, read, sha

sys.path[:0] = [str(ROOT / path) for path in ('results/T-048/scripts', 'results/T-045/scripts')]

import psutil
from chay import capture, dump
from chay_pha1 import tat_ha_toc, xao
from m1 import adapter, chuoi, e4
from p3 import nezha, selector


def run(args, folder):
    tat_ha_toc()
    matrix_path = OUT / 'ma-tran.json'
    matrix = read(matrix_path)
    for name, expected in matrix['sources'].items():
        if sha(ROOT / name) != expected:
            raise ValueError(f'Nguồn chạy lệch: {name}')
    if os.environ.get('PYTHONHASHSEED') != str(args.seed):
        raise ValueError('PYTHONHASHSEED không khớp')
    job = matrix['jobs'][args.job]
    configs = matrix['K-b']
    if args.pilot:
        configs = {**configs, **{branch['on']['config_id']: branch['on']
                                for branch in matrix['T6_conditional'].values()}}
    rows = [configs[name] for name in args.config]
    process = psutil.Process()
    resource = {'ram_available': psutil.virtual_memory().available, 'logical_cpu': psutil.cpu_count(),
                'disk_free': shutil.disk_usage(OUT).free}
    command = {'argv': sys.argv, 'job': job, 'matrix_sha256': sha(matrix_path), 'configs': rows,
               'host': platform.node(), 'platform': platform.platform(), 'resource': resource,
               'versions': {n: version(n) for n in ('numpy', 'scipy', 'pandas', 'pyarrow', 'drain3', 'psutil')}}
    (folder / 'command.json').write_text(dump(command) + '\n', encoding='utf-8')
    oid = job['opaque_id']
    start = time.monotonic()
    contract = read(ROOT / 'results/T-043/hop-dong.json')
    with (folder / 'progress.jsonl').open('x', encoding='utf-8') as progress:
        def emit(record):
            progress.write(dump(record) + '\n')
            progress.flush()

        emit({'event': 'load', 'rss': process.memory_info().rss})
        if job['dataset'] == 'RE2-TT':
            allow = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
            universe = read(ROOT / 'results/T-022/mappings/universe-re2tt-dev.json')['U']
            t = job['t']
            case = adapter.ca_re2tt(allow, oid, t, args.re_root, contract, universe)
        else:
            allow = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
            case = adapter.ca_nezha(allow, oid, args.nz_root, contract)
            t = case['t']
        if args.shuffle is not None:
            xao(case, args.shuffle)
        normalized = {key: case.get(key) for key in ('spans', 'metrics', 'logs', 'inventory', 'aliases', 'params_ca')}
        input_sha = hashlib.sha256(dump(dict(normalized, t=t)).encode()).hexdigest()
        del normalized
        emit({'event': 'loaded', 'seconds': time.monotonic() - start, 'input_sha256': input_sha,
              'rss': process.memory_info().rss})
        cache = e4.CacheCong()
        native, trace = [folder / f'{name}.jsonl.gz' for name in ('ban-ghi', 'trung-gian')]
        with gzip.open(native, 'xt', encoding='utf-8', compresslevel=3) as n, \
                gzip.open(trace, 'xt', encoding='utf-8', compresslevel=3) as d:
            for row in rows:
                chuoi.CACHE = e4.CacheCong() if args.no_cache else cache
                begin, cpu = time.monotonic(), time.process_time()
                record, evidence, phases, effective = capture(case, t, row, compact=True, input_sha256=input_sha)
                n.write(dump(dict(record, opaque_id=oid)) + '\n')
                d.write(dump(dict(job, config_id=row['config_id'], effective_sha256=effective, trace=evidence)) + '\n')
                ram = process.memory_info()
                emit({'event': 'record', 'config_id': row['config_id'], 'status': record['status'],
                      'seconds': time.monotonic() - begin, 'cpu_seconds': time.process_time() - cpu,
                      'phases': phases, 'rss': ram.rss, 'peak_rss': getattr(ram, 'peak_wset', ram.rss)})
                invalid_z = [unit for unit, check in evidence['phan_vi'].items()
                             if 'z' in check and not check['z']['huu_han']]
                if record['status'] not in ('OK', 'NO_EVIDENCE') or evidence['capture_errors'] or invalid_z:
                    emit({'event': 'invalid', 'config_id': row['config_id'], 'units_z': invalid_z})
                    raise ValueError(f'Bản ghi không hợp lệ: {row["config_id"]}')
    result = {'records': len(rows), 'wall_seconds': time.monotonic() - start,
              'files': {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in (native, trace)}}
    (folder / 'kiem.json').write_text(json.dumps(result) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('job', type=int)
    parser.add_argument('run')
    parser.add_argument('config', nargs='+')
    parser.add_argument('--pilot', action='store_true')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--shuffle', type=int)
    parser.add_argument('--no-cache', action='store_true')
    parser.add_argument('--re-root', type=Path, default=ROOT)
    parser.add_argument('--nz-root', type=Path, default=ROOT)
    args = parser.parse_args()
    folder = (OUT / 'runs' / args.run).resolve()
    if folder.parent != (OUT / 'runs').resolve():
        raise ValueError('Thư mục chạy ngoài phạm vi')
    folder.mkdir()
    run(args, folder)


if __name__ == '__main__':
    main()
