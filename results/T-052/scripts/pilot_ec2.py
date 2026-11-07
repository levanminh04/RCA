"""Worker độc lập trên EC2; chỉ dữ liệu dev, không nhãn, so nguồn cùng máy."""
import copy
import gzip
import hashlib
import json
import os
import pathlib
import platform
import sys
import time
import traceback

ROOT = pathlib.Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / x) for x in ('src', 'results/T-048/scripts', 'results/T-045/scripts')]
from chay import capture, dump
from chay_pha1 import tat_ha_toc
from m1 import adapter, chuoi, e4, runner
from p3 import nezha, selector
import psutil


def read(path):
    return json.loads(pathlib.Path(path).read_bytes())


def save(path, value):
    with pathlib.Path(path).open('x', encoding='utf-8') as f:
        f.write(dump(value) + '\n')


def sha(path):
    with pathlib.Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def comparable(rec, control):
    r = copy.deepcopy(rec)
    for name in ('opaque_id', 'config_id', 'variant'):
        r.pop(name, None)
    if control:
        r['region'] = None
    r['extra'].pop('dau_vao_cd3', None)
    r['extra']['doi_chung'].pop('C-d3', None)
    return r


def main():
    start = time.perf_counter()
    tat_ha_toc()
    plan = read(ROOT / 'plan.json')
    target = ROOT.parent / 'output'
    target.mkdir()
    for path, expected in plan['stage_files'].items():
        assert sha(ROOT / path) == expected, path
    save(target / 'environment.json', {'python': sys.version, 'platform': platform.platform(),
         'available_ram': psutil.virtual_memory().available, 'pid': os.getpid(), 'started_epoch': time.time(),
         'stage_files_checked': len(plan['stage_files']), 'labels_read': False})
    contract = read(ROOT / 'results/T-043/hop-dong.json')
    tt = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    ob = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
    universe = read(ROOT / 'results/T-022/mappings/universe-re2tt-dev.json')['U']
    rows = []
    for job in plan['jobs']:
        index, dataset, window = job['index'], job['job']['dataset'], job['job']['window']
        print(json.dumps({'stage': 'start', 'index': index, 'dataset': dataset, 'window': window}), flush=True)
        tick = time.perf_counter()
        j = job['job']
        if dataset == 'RE2-TT':
            t = j['t']
            case = adapter.ca_re2tt(tt, j['opaque_id'], t, pathlib.Path('/home/ubuntu/rca-t048/staging'), contract, universe)
        else:
            case = adapter.ca_nezha(ob, j['opaque_id'], pathlib.Path('/home/ubuntu/rca/T-032/repo'), contract)
            t = case['t']
        normal = {k: case.get(k) for k in ('spans', 'metrics', 'logs', 'inventory', 'aliases', 'params_ca')}
        input_sha = hashlib.sha256(dump(dict(normal, t=t)).encode()).hexdigest()
        expected = read(ROOT / job['expected'])
        assert input_sha == expected['normalized_input_sha256']
        chuoi.CACHE = e4.CacheCong()
        for name, cid in plan['configs'].items():
            conf = copy.deepcopy(job['configurations'][cid])
            conf['config_id'] = name
            conf['params'] = runner._params(conf, {})
            conf['params']['tach_cd3'] = True
            if name != 'M1':
                conf['params']['doi_chung'] = name
            conf = {'config_id': name, 'params': conf['params']}
            begin = time.perf_counter()
            rec, trace, clocks, effective = capture(case, t, conf, compact=True, input_sha256=input_sha)
            assert rec['status'] in ('OK', 'NO_EVIDENCE'), rec.get('error')
            assert not trace['capture_errors'], trace['capture_errors']
            actual_samples = {k: v['mau_sha256'] for k, v in trace['phan_vi'].items()}
            assert actual_samples == expected['samples'][cid]
            path = target / f'{index:02d}-{name}.json.gz'
            path.write_bytes(gzip.compress(dump({'record': rec, 'trace': trace,
                             'timing': clocks, 'effective': effective}).encode(), mtime=0))
            save(target / f'{index:02d}-{name}-seal.json', {'sha256': sha(path), 'input_sha256': input_sha,
                 'main_sealed_before_cd3': True, 'labels_read': False})
            left, right = comparable(rec, name != 'M1'), comparable(expected['records'][cid], name != 'M1')
            mismatches = [k for k in set(left) | set(right) if dump(left.get(k)) != dump(right.get(k))]
            row = {'index': index, 'dataset': dataset, 'window': window, 'config': name,
                   'elapsed_seconds': time.perf_counter() - begin, 'mismatches': mismatches,
                   'rss_bytes': psutil.Process().memory_info().rss, 'input_sha256': input_sha}
            save(target / f'{index:02d}-{name}-comparison.json', row)
            rows.append(row)
            print(json.dumps(row), flush=True)
            if mismatches:
                save(target / f'{index:02d}-{name}-mismatch.json', {'actual': left, 'expected': right})
                raise ValueError((index, name, mismatches))
        print(json.dumps({'stage': 'window_done', 'index': index, 'seconds': time.perf_counter() - tick}), flush=True)
    save(target / 'summary.json', {'PASS': True, 'comparisons': rows, 'labels_read': False,
          'elapsed_seconds': time.perf_counter() - start, 'native_comparisons': len(rows)})


if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        out = ROOT.parent / 'output'
        out.mkdir(exist_ok=True)
        save(out / 'failure.json', {'error': repr(exc), 'traceback': traceback.format_exc()})
        raise
