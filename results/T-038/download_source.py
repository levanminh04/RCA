"""Tải đúng blob plan Minh duyệt; giữ mọi lỗi, không thực thi nguồn."""
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/T-038'
PLAN = OUT / 'runs/metadata-de-xuat-001/de-xuat-tai.json'
TARGET = OUT / 'sources/train-ticket-v1.0.0'


def main():
    run = OUT / 'runs' / sys.argv[1]
    run.mkdir(parents=True, exist_ok=False)
    (run / 'download_source.py').write_bytes(Path(__file__).read_bytes())
    (run / 'plan.json').write_bytes(PLAN.read_bytes())
    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    assert hashlib.sha256(PLAN.read_bytes()).hexdigest() == '30028aa7dcb577c007072e6f18dccb3c64902d967fc2445c91885f1156ca7429'
    assert not TARGET.exists()
    TARGET.mkdir(parents=True)
    groups = {}
    for row in plan['proposed_files']:
        path = PurePosixPath(row['path'])
        assert not path.is_absolute() and '..' not in path.parts
        groups.setdefault(row['git_blob'], []).append(row)
    lock = threading.Lock()
    received = 0
    all_rows, failures = [], []
    start = time.monotonic()

    def log(row):
        with lock:
            with (run / 'progress.jsonl').open('a', encoding='utf-8') as f:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')

    def get_group(item):
        nonlocal received
        expected, paths = item
        assert len({x['bytes'] for x in paths}) == 1
        source = paths[0]
        for attempt in range(1, 4):
            audit = {'path': source['path'], 'url': source['proposed_url'], 'attempt': attempt,
                     'start_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
            try:
                request = urllib.request.Request(source['proposed_url'], headers={'User-Agent': 'T038-approved-source'})
                with urllib.request.urlopen(request, timeout=30) as response:
                    data = response.read()
                    audit.update(status=response.status, resolved_url=response.url,
                                 payload_bytes=len(data), content_encoding=response.headers.get('Content-Encoding'))
                with lock:
                    received += len(data)
                blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                if blob != expected or len(data) != source['bytes']:
                    bad = run / 'failed-payloads' / (expected + '-' + str(attempt) + '.bin')
                    bad.parent.mkdir(exist_ok=True)
                    bad.write_bytes(data)
                    raise ValueError('source_blob_or_size_mismatch')
                checksum = hashlib.sha256(data).hexdigest()
                records = []
                for row in paths:
                    dest = TARGET / row['path']
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)  # symlink mode được giữ trong manifest, không tạo symlink thật.
                    records.append({'path': dest.relative_to(ROOT).as_posix(), 'source_path': row['path'],
                                    'mode': row['mode'], 'bytes': len(data), 'sha256': checksum,
                                    'git_blob': blob, 'url': source['proposed_url'], 'attempt': attempt})
                audit.update(ok=True, materialized_paths=len(paths), sha256=checksum, git_blob=blob)
                log(audit)
                return records
            except Exception as exc:
                audit.update(ok=False, error=repr(exc))
                log(audit)
                if isinstance(exc, ValueError) or attempt == 3:
                    raise
                time.sleep(attempt)

    try:
        with cf.ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(get_group, item): item[0] for item in groups.items()}
            for count, future in enumerate(cf.as_completed(futures), 1):
                try:
                    all_rows.extend(future.result())
                except Exception as exc:
                    failures.append({'git_blob': futures[future], 'error': repr(exc)})
                if count % 100 == 0 or count == len(futures):
                    print(json.dumps({'done_unique': count, 'total_unique': len(futures),
                                      'materialized': len(all_rows), 'failed_groups': len(failures)}), flush=True)
        # Metadata sau duyệt: chỉ Git metadata, không endpoint trả patch.
        metadata_rows = []
        for name, url in [('tag', 'https://api.github.com/repos/FudanSELab/train-ticket/tags?per_page=100'),
                          ('commit', 'https://api.github.com/repos/FudanSELab/train-ticket/git/commits/' + plan['commit']),
                          ('tree', plan['metadata_tree_url'])]:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'T038-approved-metadata'}), timeout=30) as response:
                body = response.read()
            dest = TARGET / ('_acquisition-' + name + '.json')
            dest.write_bytes(body)
            metadata_rows.append({'path': dest.relative_to(ROOT).as_posix(), 'url': url,
                                  'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()})
        manifest = {'task': 'T-038', 'commit': plan['commit'], 'tree': plan['tree'],
                    'client_date': '2026-10-16', 'file_count': len(all_rows), 'unique_blobs': len(groups),
                    'files': sorted(all_rows, key=lambda x: x['source_path']), 'metadata': metadata_rows,
                    'errors': failures, 'payload_received_bytes': received,
                    'metadata_received_bytes': sum(x['bytes'] for x in metadata_rows),
                    'materialized_blob_bytes': sum(x['bytes'] for x in all_rows),
                    'http_headers_tls_bytes': None, 'metadata_and_allocation_overhead_bytes': None,
                    'elapsed_acquisition_seconds': time.monotonic() - start,
                    'cost_condition': 'acquisition elapsed accounting, not isolated CPU/RAM benchmark',
                    'ok': len(all_rows) == plan['full_tree_blob_count'] and not failures,
                    'symlinks_literal_not_materialized': True}
        (run / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({k: manifest[k] for k in ['ok', 'file_count', 'unique_blobs', 'payload_received_bytes',
                          'metadata_received_bytes', 'materialized_blob_bytes', 'elapsed_acquisition_seconds']}, ensure_ascii=False))
        if not manifest['ok']:
            raise RuntimeError('incomplete_source_acquisition')
    except BaseException as exc:
        (run / 'terminal-error.json').write_text(json.dumps({'error': repr(exc), 'files_so_far': len(all_rows),
                                                          'failed_groups': failures}, indent=2), encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
