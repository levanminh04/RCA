"""Tiền kiểm T-039 từ nguồn cục bộ. Không tải hoặc đọc telemetry thô."""
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
OUT = ROOT / 'results/T-039/runs' / sys.argv[1]
OUT.mkdir(parents=True, exist_ok=False)
START = time.perf_counter()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def digest(path):
    b = (ROOT / path).read_bytes()
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def verify(entry):
    p = entry['path']
    if p.startswith(('data/', 'D:/Project/flash-ticket-rca-research')):
        raise ValueError('forbidden_input:' + p)
    if not (ROOT / p).is_file():
        return {'path': p, 'ok': False, 'reason': 'missing'}
    actual = digest(p)
    return {**actual, 'expected_sha256': entry['sha256'],
            'ok': actual['sha256'] == entry['sha256'] and
            ('bytes' not in entry or actual['bytes'] == entry['bytes'])}


try:
    protected = ['AGENTS.md', 'docs/MRP.md', 'docs/WHY.md', 'docs/DECISIONS.md',
                 'docs/LESSONS.md', 'docs/review-prompt.md',
                 'tasks/T-039-p5b-online-boutique/SPEC.md',
                 'results/T-035/manifest.json', 'results/T-036/manifest.json',
                 'results/T-036/nguon.json', 'src/do_thi_tinh/__init__.py',
                 'src/do_thi_tinh/build.py', 'src/do_thi_tinh/compare.py',
                 'src/do_thi_tinh/README.md']
    save('protected-before.json', [digest(p) for p in protected])
    (OUT / 'STATE-before.md').write_bytes((ROOT / 'docs/STATE.md').read_bytes())
    log = (ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md').read_bytes()
    marker = '\n\n## Phiên 2 — 15/10/2026'.encode()
    if marker not in log:
        raise ValueError('session_marker_missing')
    (OUT / 'LOG-before.md').write_bytes(log.split(marker, 1)[0])
    for filename, command in [('tracked-before.diff', ['git', 'diff', '--no-ext-diff']),
                              ('status-before.txt', ['git', 'status', '--short'])]:
        p = subprocess.run(command, cwd=ROOT, capture_output=True)
        (OUT / filename).write_bytes(p.stdout)
        (OUT / (filename + '.stderr')).write_bytes(p.stderr)

    m36 = read('results/T-036/manifest.json')
    pin_ok = (m36['created_utc'] == '2026-10-15T13:45:08.305188+00:00' and
              m36['current_run'] == 'runs/kiem-r1-after-002')
    rows36 = [verify(e) for e in m36['files']]
    codes = read('results/T-036/runs/kiem-r1-after-002/code-hashes.json')
    code_rows = []
    for p, wanted in codes.items():
        snapshot = 'results/T-036/runs/kiem-r1-after-002/code/' + Path(p).name
        code_rows.append({'path': p, 'snapshot': snapshot,
                          'ok': digest(p)['sha256'] == wanted == digest(snapshot)['sha256']})
    m3 = read('results/T-003/runs/final-review-003/artifact-manifest.json')
    local_names = ['README.md', 'repository.json', 'tree.json', 'zenodo.json',
                   'LICENSE', 'FSE2023_Nezha.pdf', 'main.py', 'data_integrate.py',
                   'alarm.py', 'pattern_ranker.py']
    required8 = ['results/T-008/sources/' + s for s in local_names]
    required8.append('results/T-008/runs/run-001/manifest.json')
    idx3 = {e['path']: e for e in m3['files']}
    rows8 = [verify(idx3[p]) for p in required8]
    tree = read('results/T-008/sources/tree.json')
    treeidx = {e['path']: e for e in tree['tree']}
    git_blobs = []
    for name in local_names:
        if name not in treeidx:
            continue
        b = (ROOT / 'results/T-008/sources' / name).read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        git_blobs.append({'path': name, 'ok': actual == treeidx[name]['sha'],
                          'expected_blob': treeidx[name]['sha'], 'actual_blob': actual})
    m35 = read('results/T-035/manifest.json')
    entries = [e for e in m35['files'] if e['path'].startswith('results/T-035/do-thi/Nezha-OB/')]
    graph_hashes = [verify(e) for e in entries]
    sources35 = [e for e in m35['files'] if e['path'] in [
        'results/T-035/dac-ta-do-thi.md', 'results/T-035/thong-tin-theo-quan-he.md',
        'results/T-035/cot-node-nezha.json', 'results/T-035/cot-node-nezha.md',
        'results/T-035/thong-ke-do-thi.json', 'results/T-035/thong-ke-do-thi.md']]
    sources35 = [verify(e) for e in sources35]
    all_ok = pin_ok and all(x['ok'] for x in rows36 + code_rows + rows8 + git_blobs + graph_hashes + sources35)
    save('input-verification.json', {
        'pin_ok': pin_ok, 't036': rows36, 'code_snapshot': code_rows,
        't008_final_manifest': rows8, 't008_git_blobs': git_blobs,
        't035_documents': sources35, 't035_graph_hashes': graph_hashes,
        'all_ok': all_ok,
        'manifest_pins': [digest(p) for p in [
            'results/T-003/runs/final-review-003/artifact-manifest.json',
            'results/T-035/manifest.json', 'results/T-036/manifest.json']]})
    if not all_ok:
        raise ValueError('input_hash_or_pin_mismatch')
    graph_rows = []
    for e in entries:
        g = read(e['path'])
        p = Path(e['path'])
        graph_rows.append({'path': e['path'], 'opaque_id': p.parts[-3],
                           'level': g['level'], 'window': p.stem,
                           'interval_ns': g['interval_ns'], 'bytes': e['bytes'],
                           'node_count': len(g['nodes']), 'edge_count': len(g['edges'])})
    canonical = read('results/T-035/thong-ke-do-thi.json')['canonical_graph_files']
    canonical_nezha = sorted(p for p in canonical if '/Nezha-OB/' in p)
    assert sorted(e['path'] for e in entries) == canonical_nezha
    save('graph-inventory.json', {
        'domain': 'dev-adapter', 'graph_count': len(graph_rows),
        'opaque_id_count': len({r['opaque_id'] for r in graph_rows}),
        'bytes': sum(r['bytes'] for r in graph_rows),
        'canonical_paths_match': True, 'snapshot_60_300_count': 0,
        'full_semantics': 'union of authorized adapter domain; interval null; not whole day',
        'rows': graph_rows})
    save('environment.json', {'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
         'timezone_user': 'Asia/Saigon', 'device': platform.node(),
         'python': sys.version, 'platform': platform.platform(),
         'bytecode_disabled': sys.dont_write_bytecode, 'benchmark': False,
         'network_download_in_this_script_bytes': 0,
         'seconds_local_preflight_not_performance_pilot': time.perf_counter() - START})
    print(json.dumps({'all_ok': True, 't036_artifacts': len(rows36),
                      'graphs': len(graph_rows), 'graph_bytes': sum(r['bytes'] for r in graph_rows),
                      'run': OUT.relative_to(ROOT).as_posix()}, ensure_ascii=False))
except BaseException as error:
    save('failure.json', {'type': type(error).__name__, 'message': str(error),
                         'seconds': time.perf_counter() - START})
    raise
