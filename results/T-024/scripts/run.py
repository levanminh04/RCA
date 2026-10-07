"""T-024: kiểm đầu vào, test, ba cohort tuần tự; chốt bản ghi trước khi nối nhãn."""
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-024'
WORK = OUT / 'work'
EXPECTED = '8d4cc8196c87ee566d717cab184c3177a5d5d6685550b232f8b08b932420a12c'
REUSED = ['circa-ols-h0-001', 'circa-svr-h0-lan1-001', 'torai-B-ec2-001',
          'torai-A-ec2-001', 'microrank-30-001']
PYTHON = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'src'))


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def code_hash():
    h, per = hashlib.sha256(), {}
    for p in sorted((ROOT / 'src/p3').rglob('*.py'), key=lambda p: p.relative_to(ROOT).as_posix()):
        b = p.read_bytes()
        h.update(b)
        per[p.relative_to(ROOT).as_posix()] = hashlib.sha256(b).hexdigest()
    if h.hexdigest() != EXPECTED:
        raise RuntimeError('src/p3 đã đổi: dừng; không dùng lại T-031')
    return {'tong': h.hexdigest(), 'tep': per}


def setup():
    WORK.mkdir(parents=True, exist_ok=True)
    for name in ('matplotlib', 'tmp'):
        (WORK / name).mkdir(exist_ok=True)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    os.environ['MPLCONFIGDIR'] = str(WORK / 'matplotlib')
    os.environ['TMP'] = os.environ['TEMP'] = str(WORK / 'tmp')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONPATH'] = os.pathsep.join([
        'D:/RCA-ext/src/RCAEval', 'D:/RCA-ext/src/baro',
        'D:/RCA-ext/work/T-014/CIRCA', str(ROOT / 'src')])


def inputs():
    from p3 import nhan, selector
    al = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    moc = nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')
    if len(al) != 30 or set(al) != set(moc):
        raise RuntimeError('cohort/mốc không đúng 30 ca')
    return al, moc


def preflight():
    import psutil
    ch = code_hash()
    ref = load(ROOT / 'results/T-031/moi-truong.json')['src_p3_sau_sua_1']
    assert ch == ref
    al, _ = inputs()
    verified, start = [], time.perf_counter()
    from p3 import selector
    for i, oid in enumerate(sorted(al), 1):
        files = selector.chon_ca(al, oid, ROOT, kiem_hash=True)
        verified.append({'opaque_id': oid, 'files': sorted(files)})
        print(f'HASH [{i}/30] {oid}', flush=True)
    runs = {}
    for name in REUSED:
        rd = ROOT / 'results/T-031/runs' / name
        cfg = load(rd / 'cau-hinh.json')
        assert cfg['src_p3']['tong'] == EXPECTED
        recs = [load(p) for p in sorted((rd / 'luot').rglob('ban-ghi-*.json'))]
        groups = {}
        for r in recs:
            groups.setdefault((r['variant'], r['seed']), []).append(r['opaque_id'])
            assert r['mode'] == 'a' and r['hashseed'] == 0
            for key, value in r['input_sha256'].items():
                if key in al[r['opaque_id']]['files']:
                    assert value == al[r['opaque_id']]['files'][key]['sha256']
        for ids in groups.values():
            assert len(ids) == 30 and set(ids) == set(al)
        runs[name] = {'records': len(recs), 'status': dict(Counter(r['status'] for r in recs)),
                      'config': str((rd / 'cau-hinh.json').relative_to(ROOT).as_posix()),
                      'config_sha256': sha(rd / 'cau-hinh.json')}
    for name in REUSED[:-1]:
        assert set(runs[name]['status']) == {'OK'}
    assert runs[REUSED[-1]]['status'] == {'OK': 26, 'ERROR': 4}
    paths = [ROOT / 'AGENTS.md', ROOT / 'tasks/T-024-cham-che-do-a/SPEC.md',
             ROOT / 'docs/WHY.md', ROOT / 'docs/DECISIONS.md', ROOT / 'docs/LESSONS.md']
    paths += [p for directory in ('src', 'results/T-022', 'results/T-031', 'results/T-030/tests')
              for p in (ROOT / directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    protected = {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}
    write(WORK / 'protected-before.json', protected)
    proc = [{'pid': p.pid, 'name': p.info['name']} for p in psutil.process_iter(['name'])
            if (p.info['name'] or '').lower() in ('python.exe', 'pythonw.exe') and p.pid != os.getpid()]
    env = {key: importlib.metadata.version(key) for key in ('numpy', 'pandas', 'scikit-learn', 'scipy',
                                                               'pyarrow', 'psutil', 'networkx')}
    obj = {'at': now(), 'src_p3': ch, 'python': platform.python_version(), 'packages': env,
           'available_ram_gb': round(psutil.virtual_memory().available / 2**30, 3),
           'disk_free_gb': round(psutil.disk_usage('D:/').free / 2**30, 3), 'other_python': proc,
           'data_hash_verified': verified, 'reused': runs, 'hash_check_wall_s': time.perf_counter() - start}
    write(OUT / 'kiem-truoc-chay.json', obj)
    print(json.dumps({k: v for k, v in obj.items() if k not in ('src_p3', 'data_hash_verified', 'reused')},
                     ensure_ascii=False), flush=True)
    if proc:
        raise RuntimeError('Có Python khác: kiểm T-025 trước khi chạy nặng')


def tests():
    setup()
    code_hash()
    td = OUT / 'test-chay-lai'
    td.mkdir(exist_ok=True)
    rows = []
    for name, expected in [('test_buoc1', 14), ('test_buoc2', 19), ('test_buoc34', 24)]:
        dest = td / (name + '.txt')
        if dest.exists():
            raise RuntimeError('Không ghi đè lượt test đã có')
        start = time.perf_counter()
        with dest.open('w', encoding='utf-8') as f:
            p = subprocess.run([PYTHON, '-B', '-W', 'ignore', str(ROOT / 'results/T-030/tests' / (name + '.py'))],
                               cwd=ROOT, env=dict(os.environ), stdout=f, stderr=subprocess.STDOUT)
        txt = dest.read_text(encoding='utf-8')
        ok = p.returncode == 0 and f'Ran {expected} tests' in txt and '\nOK\n' in txt
        rows.append({'test': name, 'expected': expected, 'exit_code': p.returncode, 'pass': ok,
                     'wall_s': time.perf_counter() - start, 'source': dest.relative_to(ROOT).as_posix()})
        write(td / 'tom-tat.json', {'at': now(), 'tests': rows, 'pass': all(x['pass'] for x in rows)})
        print(f'TEST {name}: {ok}, wall={rows[-1]["wall_s"]:.1f}s', flush=True)
        if not ok:
            raise RuntimeError('Test không đạt; giữ output, dừng trước chấm')


def run(method):
    import psutil
    from p3 import ban_ghi, runner
    if method not in ('baro', 'simplerca', 'tracerca'):
        raise ValueError(method)
    setup()
    ch = code_hash()
    al, moc = inputs()
    runsdir = OUT / 'runs'
    runsdir.mkdir(exist_ok=True)
    existing = sorted(runsdir.glob(method + '-30-*'))
    for rd in existing:
        if (rd / 'tom-tat.json').exists() and load(rd / 'tom-tat.json').get('xong'):
            print('Dùng lại cohort T-024 hợp lệ: ' + rd.name, flush=True)
            return
    paused = [p for p in existing if (p / 'dung-theo-minh.json').exists() and (p / 'tom-tat.json').exists()
              and not load(p / 'tom-tat.json').get('xong')]
    if paused:
        assert len(paused) == 1
        rd = paused[0]
        cfg = load(rd / 'cau-hinh.json')
        assert cfg['src_p3'] == ch and cfg['method'] == method and cfg['mode'] == 'a'
        assert cfg['timeout_s'] == 3600 and cfg['opaque_ids'] == sorted(al)
        rows = load(rd / 'tom-tat.json')['luot']
        for row in rows:
            assert sha(ROOT / row['path']) == row['sha256']
            r = load(ROOT / row['path'])
            ban_ghi.kiem(r)
            assert r['opaque_id'] == row['opaque_id'] and r['method'] == method
        assert len({row['opaque_id'] for row in rows}) == len(rows)
        write(rd / 'tiep-sau-dieu-phoi.json', {'at': now(), 'reused_completed': len(rows),
                                             'keep_interrupted_jobs': True, 'src_p3_sha256': EXPECTED})
        print(f'RESUME {method}: dùng lại {len(rows)} ca hợp lệ; giữ lượt bị ngắt', flush=True)
    else:
        rd = runsdir / f'{method}-30-{len(existing)+1:03d}'
        rd.mkdir()
        write(rd / 'cau-hinh.json', {'at': now(), 'src_p3': ch, 'method': method, 'mode': 'a',
                                     'hashseed': 0, 'seed': None, 'timeout_s': 3600, 'opaque_ids': sorted(al),
                                     'protocol': 'results/T-022/giao-thuc-v2.md',
                                     'config': 'results/T-022/cau-hinh/p3-re2tt-v2.json'})
        rows = []
    completed = {row['opaque_id'] for row in rows}
    start = time.perf_counter()
    for i, oid in enumerate(sorted(al), 1):
        if oid in completed:
            continue
        ram = psutil.virtual_memory().available / 2**30
        text = f'{now()} START [{i}/30] {method} {oid} RAM={ram:.2f}GB'
        print(text, flush=True)
        with (rd / 'tien-do.txt').open('a', encoding='utf-8') as f:
            f.write(text + '\n')
        try:
            recs = runner.chay_luot(al, oid, method, 'a', moc[oid], rd / 'luot', 3600, hashseed=0)
            if len(recs) != 1:
                raise RuntimeError('Số bản ghi sai')
            r = recs[0]
            ban_ghi.kiem(r)
            if r['status'] == 'TIMEOUT' or 'observed_entities' not in r['sets']:
                raise RuntimeError('Bản ghi thiếu tập quan sát O: dừng báo Minh trước chấm')
            if method == 'baro' and r['status'] == 'OK':
                assert r['diagnostics']['key_check'] == 'pass'
            if method == 'tracerca':
                import math
                assert all(math.isfinite(x) for q in r['ranking'] for x in q['key'])
            rp = rd / 'luot' / r['run_id'] / 'ban-ghi-0.json'
            row = {'opaque_id': oid, 'path': rp.relative_to(ROOT).as_posix(), 'sha256': sha(rp),
                   'status': r['status'], 'error': r['error'], 'cost': r['cost'],
                   'diagnostics': r['diagnostics'], 'window': r['window'],
                   'input_shape': {k: v for k, v in r['input_shape'].items() if k != 'metric_columns'},
                   'ram_before_gb': ram}
            rows.append(row)
        except Exception as exc:
            write(rd / 'dung-loi.json', {'at': now(), 'opaque_id': oid, 'error': repr(exc), 'completed': len(rows)})
            raise
        write(rd / 'tom-tat.json', {'src_p3_sha256': EXPECTED, 'method': method, 'xong': False,
                                    'luot': rows, 'status': dict(Counter(x['status'] for x in rows))})
        text = f'{now()} END [{i}/30] {method} {oid} {r["status"]} wall={r["cost"]["wall_s"]}s RSS={r["cost"]["peak_rss_mb"]}MB'
        print(text, flush=True)
        with (rd / 'tien-do.txt').open('a', encoding='utf-8') as f:
            f.write(text + '\n')
    write(rd / 'tom-tat.json', {'src_p3_sha256': EXPECTED, 'method': method, 'xong': True, 'luot': rows,
                                'status': dict(Counter(x['status'] for x in rows)),
                                'total_wall_s': time.perf_counter() - start,
                                'sum_worker_wall_s': sum(x['cost']['wall_s'] for x in rows),
                                'peak_rss_mb': max(x['cost']['peak_rss_mb'] for x in rows), 'at': now()})
    print('COHORT DONE ' + method, flush=True)


def freeze():
    code_hash()
    test_result = load(OUT / 'test-chay-lai/tom-tat.json')
    assert test_result['pass'] and len(test_result['tests']) == 3
    dest = OUT / 'ban-ghi-dua-vao-cham.json'
    if dest.exists():
        raise RuntimeError('Manifest đã chốt; không ghi đè')
    al, _ = inputs()
    dirs = [ROOT / 'results/T-031/runs' / name for name in REUSED]
    for method in ('baro', 'simplerca', 'tracerca'):
        ds = [p for p in sorted((OUT / 'runs').glob(method + '-30-*'))
              if (p / 'tom-tat.json').exists() and load(p / 'tom-tat.json').get('xong')]
        assert len(ds) == 1
        dirs += ds
    records, groups = [], {}
    for rd in dirs:
        cfg = rd / 'cau-hinh.json'
        assert load(cfg)['src_p3']['tong'] == EXPECTED
        for p in sorted((rd / 'luot').rglob('ban-ghi-*.json')):
            r = load(p)
            assert r['mode'] == 'a' and r['hashseed'] == 0
            assert 'observed_entities' in r['sets']
            item = {k: r[k] for k in ('method', 'variant', 'seed', 'opaque_id')}
            item.update(path=p.relative_to(ROOT).as_posix(), sha256=sha(p), source_run=rd.relative_to(ROOT).as_posix(),
                        source_config=cfg.relative_to(ROOT).as_posix(), source_config_sha256=sha(cfg), src_p3_sha256=EXPECTED)
            records.append(item)
            groups.setdefault((r['method'], r['variant'], r['seed']), []).append(r['opaque_id'])
    assert len(records) == 420
    for ids in groups.values():
        assert len(ids) == 30 and set(ids) == set(al)
    obj = {'task': 'T-024', 'frozen_at': now(), 'src_p3_sha256': EXPECTED,
           'protocol': 'results/T-022/giao-thuc-v2.md', 'configuration': 'results/T-022/cau-hinh/p3-re2tt-v2.json',
           'records': records,
           'preserved_interrupted_attempts': [{'source_run': p.parent.relative_to(ROOT).as_posix(),
                                               'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
                                               'reason': 'Dừng theo Minh để điều phối; chưa có bản ghi chấm, giữ job/stdout/stderr'}
                                              for p in sorted((OUT / 'runs').glob('*/dung-theo-minh.json'))],
           'derived': [{'id': 'microrank_top11', 'source_variant': 'full',
                        'rule': 'service_ranks_top11 giữ thứ tự, khóa từ full; chỉ chấm sau khóa manifest'}]}
    write(dest, obj)
    line = f'\n- {obj["frozen_at"]} — **CHỐT DANH SÁCH BẢN GHI** trước lượt evaluator thật đầu tiên: `results/T-024/ban-ghi-dua-vao-cham.json`, 420 bản ghi nguồn + MicroRank top11 dẫn xuất từ full đã chốt. Mọi bản ghi giữ hash nguồn; không thêm/bỏ/chạy lại vì số chấm. Manifest SHA-256 ghi trong `results/T-024/work/freeze.json`.\n'
    with (ROOT / 'tasks/T-024-cham-che-do-a/LOG.md').open('a', encoding='utf-8') as f:
        f.write(line)
    write(WORK / 'freeze.json', {'at': obj['frozen_at'], 'sha256': sha(dest), 'records': len(records)})
    print(f'FROZEN {len(records)} records at {obj["frozen_at"]}', flush=True)


def cohorts():
    """Giữ một tiến trình T-024 để script T-025 tiếp tục nhường laptop trong cả ba cohort."""
    while True:
        tp = OUT / 'test-chay-lai/tom-tat.json'
        if tp.exists():
            result = load(tp)
            if not result['pass']:
                raise RuntimeError('Test không đạt')
            if len(result['tests']) == 3:
                break
        time.sleep(5)
    for method in ('baro', 'simplerca', 'tracerca'):
        run(method)


if __name__ == '__main__':
    setup()
    command = sys.argv[1]
    if command == 'run':
        run(sys.argv[2])
    else:
        {'preflight': preflight, 'tests': tests, 'freeze': freeze, 'cohorts': cohorts}[command]()
