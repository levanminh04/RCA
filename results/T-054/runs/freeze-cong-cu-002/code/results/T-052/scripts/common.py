"""T-052: I/O đã ghim, không đọc nhãn trong phần pilot."""
import gzip
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-052'
RUN = OUT / 'runs/trien-khai-001'
sys.path[:0] = [str(ROOT / x) for x in (
    'src', 'results/T-048/scripts', 'results/T-045/scripts', 'results/T-049/scripts',
    'results/T-051', 'results/T-050')]
for x in ('D:/RCA-ext/envs/py312-pin/Lib/site-packages',
          'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages'):
    if pathlib.Path(x).is_dir():
        sys.path.append(x)
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from m1_danh_gia import pha2


def read(path):
    return json.loads((ROOT / path).read_bytes())


def digest(path):
    with (ROOT / path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def dump(value):
    return json.dumps(pha2.ma_hoa_json(value), ensure_ascii=False, sort_keys=True,
                      allow_nan=False, separators=(',', ':'))


def save(path, value):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(dump(value) + '\n')


def pin(path, expected):
    path = ROOT / path
    assert path.stat().st_size == expected.get('bytes', path.stat().st_size), str(path)
    assert digest(path) == expected['sha256'], str(path)
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size,
            'sha256': digest(path)}


def event(stage, **fields):
    row = dict(utc=datetime.now(timezone.utc).isoformat(), stage=stage, **fields)
    with (RUN / 'progress.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(dump(row) + '\n')
    print(dump(row), flush=True)


def metadata():
    """Nguồn lịch sử giữ nguyên; chỉ hai file sửa 003 có lineage riêng."""
    m50 = read('results/T-050/manifest.json')
    path = 'results/T-049/runs/t6-001-seal.json'
    pin(path, m50['upstream'][path])
    seal = read(path)
    matrix_path = 'results/T-049/ma-tran.json'
    assert digest(matrix_path) == seal['matrix_sha256']
    matrix = read(matrix_path)
    fix = read('results/T-052/manifest-ra-soat-ke-hoach-003.json')
    lineage = []
    for name, sha in matrix['sources'].items():
        if digest(name) == sha:
            continue
        assert name in ('src/m1/chuoi.py', 'src/m1/doi_chung.py'), name
        assert fix['before'][name]['sha256'] == sha, name
        old = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)
        forms = {'git_blob': old, 'git_blob_CRLF': old.replace(b'\n', b'\r\n')}
        matches = [k for k, v in forms.items() if hashlib.sha256(v).hexdigest() == sha]
        assert matches, (name, 'historical code not reconstructed')
        pin(name, fix['outputs'][name])
        lineage.append({'path': name, 'historical_representation': matches,
                        'before_sha256': sha, 'after_sha256': digest(name),
                        'authority_manifest': 'results/T-052/manifest-ra-soat-ke-hoach-003.json'})
    entries = sorted((e for rows in seal['entries'].values() for e in rows
                      if e['config'] == 'K-thang-C'), key=lambda e: e['index'])
    assert [e['index'] for e in entries] == list(range(82))
    assert all(e['job'] == matrix['jobs'][e['index']] for e in entries)
    return entries, matrix['K-b']['K-thang-C'], lineage


def native_index():
    m = read('results/T-053/manifest.json')
    path = m['canonical']['phase1_seal']
    pin(path, m['outputs'][path])
    out = {}
    for window, entries in read(path).items():
        for item in entries:
            command_path = item['path'].rsplit('/', 1)[0] + '/command.json'
            pin(command_path, m['outputs'][command_path])
            command = read(command_path)
            job = command['job']
            assert job['window'] == window
            out[(job['opaque_id'], window)] = (item, command)
    assert len(out) == 82
    return m, out


def native_rows(item, manifest, configs):
    path = item['path']
    pin(path, manifest['outputs'][path])
    assert item['sha256'] == manifest['outputs'][path]['sha256']
    found = {}
    with gzip.open(ROOT / path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            row = json.loads(line)
            if row['config_id'] in configs:
                found[row['config_id']] = row
    assert set(found) == set(configs), (path, configs)
    return found


def timing(stage, started, **extra):
    import psutil
    proc = psutil.Process()
    return dict(stage=stage, elapsed_seconds=time.perf_counter() - started,
                peak_rss_bytes=getattr(proc.memory_info(), 'peak_wset', proc.memory_info().rss), **extra)
