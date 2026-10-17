"""Thu đúng danh sách Minh duyệt; không clone hoặc lấy telemetry."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import datetime as dt
import hashlib
import json
import shutil
import sys
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
RUN = BASE / 'runs' / sys.argv[1]
RUN.mkdir(parents=True, exist_ok=False)
START = time.perf_counter()
LOCK = threading.Lock()
PROPOSAL = json.loads((BASE / 'de-xuat-tai.json').read_text(encoding='utf-8'))
AUTH = json.loads((BASE / 'authorization-20261016.json').read_text(encoding='utf-8'))
assert hashlib.sha256((BASE / 'de-xuat-tai.json').read_bytes()).hexdigest() == AUTH['approved_proposal_sha256']
assert AUTH['download_approved'] and AUTH['keep_full_task'] and AUTH['keep_shared_pin']
shutil.copyfile(BASE / 'manifest.json', RUN / 'manifest-before-precheck.json')
shutil.copyfile(BASE / 'de-xuat-tai.json', RUN / 'approved-proposal.json')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def event(value):
    value = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
             'elapsed_seconds': round(time.perf_counter() - START, 3), **value}
    with LOCK:
        with (RUN / 'progress.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(value, ensure_ascii=False) + '\n')


def fetch(url):
    request = urllib.request.Request(url, headers={
        'User-Agent': 'RCA-T039-approved-sources', 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read(), {'url': url, 'status': response.status,
                                'content_type': response.headers.get('Content-Type')}


def safe_destination(relative):
    target = (ROOT / relative).resolve()
    assert target.is_relative_to((BASE / 'sources').resolve())
    return target


def get_file(item, source_root):
    target = safe_destination(source_root + '/' + item['path'])
    data = None
    try:
        if target.exists():
            data = target.read_bytes()
            receipt = {'url': item['url'], 'reused': True, 'network_body_bytes': 0}
        else:
            data, receipt = fetch(item['url'])
            receipt['network_body_bytes'] = len(data)
        actual_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if len(data) != item['size'] or actual_blob != item['sha']:
            raise ValueError('size_or_git_blob_mismatch')
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            with target.open('xb') as f:
                f.write(data)
        result = {'path': target.relative_to(ROOT).as_posix(), 'source_path': item['path'],
                  'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                  'git_blob': actual_blob, 'ok': True, **receipt}
        event({'kind': 'source_file', **result})
        return result
    except BaseException as error:
        identifier = hashlib.sha256((source_root + '/' + item['path']).encode()).hexdigest()[:16]
        if data is not None:
            (RUN / (identifier + '.failed-payload')).write_bytes(data)
        result = {'source_path': item['path'], 'url': item['url'], 'ok': False,
                  'error': repr(error), 'network_body_bytes': len(data) if data is not None else None}
        event({'kind': 'failure', **result})
        return result


try:
    event({'kind': 'start', 'approved_source_files': 223, 'workers': 4})
    before = hashlib.sha256((ROOT / 'results/T-036/manifest.json').read_bytes()).hexdigest()
    previous = json.loads((BASE / 'runs/tien-kiem-001/input-verification.json').read_text(encoding='utf-8'))
    assert before == next(e['sha256'] for e in previous['manifest_pins'] if e['path'] == 'results/T-036/manifest.json')
    names = ['ob-repository.json', 'ob-commits.json', 'ob-tree.json',
             'nezha-ref.json', 'nezha-commit.json', 'nezha-tree.json']
    metadata = []
    parsed = []
    for entry, name in zip(PROPOSAL['metadata_to_fetch_after_approval'], names):
        data, receipt = fetch(entry['url'])
        value = json.loads(data)
        target = safe_destination('results/T-039/sources/metadata/' + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise ValueError('metadata_path_exists_use_separate_approved_capture_path')
        with target.open('xb') as f:
            f.write(data)
        metadata.append({'path': target.relative_to(ROOT).as_posix(), 'bytes': len(data),
                         'sha256': hashlib.sha256(data).hexdigest(), **receipt})
        parsed.append(value)
    assert any(c['sha'] == PROPOSAL['ob_commit']['sha'] for c in parsed[1])
    expected = sorted((e['path'], e['type'], e['sha'], e.get('size')) for e in PROPOSAL['whole_tree_proposal'])
    actual = sorted((e['path'], e['type'], e['sha'], e.get('size')) for e in parsed[2]['tree'])
    assert expected == actual and not parsed[2]['truncated']
    assert parsed[3]['object']['sha'] == PROPOSAL['nezha_selection']['commit']
    assert parsed[4]['tree']['sha'] == PROPOSAL['nezha_selection']['tree']
    old_nezha = json.loads((ROOT / 'results/T-008/sources/tree.json').read_text(encoding='utf-8-sig'))
    members = lambda v: sorted((e['path'], e['type'], e['sha'], e.get('size')) for e in v['tree'])
    assert members(parsed[5]) == members(old_nezha) and not parsed[5]['truncated']
    save(RUN / 'metadata-receipts.json', metadata)
    items = [(e, PROPOSAL['ob_selection']['target_root'].rstrip('/'))
             for e in PROPOSAL['whole_tree_proposal'] if e['action'] == 'proposed_fetch']
    items += [(e, PROPOSAL['nezha_selection']['target_root'].rstrip('/'))
              for e in PROPOSAL['nezha_selection']['files']]
    assert len(items) == 223 and not any(e['path'].endswith('/log.csv') for e, _ in items)
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(get_file, e, folder) for e, folder in items]
        for future in as_completed(futures):
            results.append(future.result())
            if len(results) % 25 == 0:
                print(json.dumps({'completed': len(results), 'of': len(items),
                                  'failed': sum(not r['ok'] for r in results)}), flush=True)
    results.sort(key=lambda r: r.get('path', r['source_path']))
    summary = {'all_ok': all(r['ok'] for r in results), 'file_count': len(results),
               'files': results, 'metadata': metadata,
               'source_disk_bytes': sum(r.get('bytes', 0) for r in results),
               'network_body_bytes': sum(r.get('network_body_bytes') or 0 for r in results) + sum(e['bytes'] for e in metadata),
               'elapsed_seconds_not_isolated_benchmark': time.perf_counter() - START,
               'raw_telemetry_fetched': False, 'pin_changed': False}
    save(RUN / 'acquisition.json', summary)
    event({'kind': 'finish', 'all_ok': summary['all_ok'], 'files': len(results)})
    print(json.dumps({k: v for k, v in summary.items() if k not in ['files', 'metadata']}), flush=True)
    if not summary['all_ok']:
        sys.exit(2)
except BaseException as error:
    if not isinstance(error, SystemExit):
        save(RUN / 'failure.json', {'type': type(error).__name__, 'message': str(error)})
    raise
