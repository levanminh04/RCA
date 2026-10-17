"""Chỉ tra Git metadata; ghi danh sách ĐỀ XUẤT tải, không lưu nguồn mới."""
from collections import Counter, defaultdict
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
REPO = 'FudanSELab/train-ticket'
COMMIT = 'fa8d9efb35b2ed5ec1d18f60510167767c8fb2bf'
BASE = 'https://api.github.com/repos/' + REPO


def main():
    out = ROOT / 'results/T-038/runs' / sys.argv[1]
    out.mkdir(parents=True, exist_ok=False)
    (out / 'prepare_source_proposal.py').write_bytes(Path(__file__).read_bytes())
    audit = []

    def metadata(url):
        # Endpoint Git thuần: không /commits (có thể trả kèm patch), không blob/raw.
        assert '/git/' in url or '/tags?' in url
        row = {'url': url, 'requested_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
        audit.append(row)
        req = urllib.request.Request(url, headers={'User-Agent': 'T038-metadata-only',
                                                   'Accept': 'application/vnd.github+json'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            row.update(status=response.status, body_bytes=len(data),
                       body_sha256=hashlib.sha256(data).hexdigest())
        return json.loads(data)

    try:
        tags = metadata(BASE + '/tags?per_page=100')
        tag = next(x for x in tags if x['name'] == 'v1.0.0')
        assert tag['commit']['sha'] == COMMIT
        commit = metadata(BASE + '/git/commits/' + COMMIT)
        assert commit['sha'] == COMMIT
        tree_sha = commit['tree']['sha']
        tree = metadata(BASE + '/git/trees/' + tree_sha + '?recursive=1')
        assert tree['sha'] == tree_sha and tree['truncated'] is False
        entries = tree['tree']
        assert len({x['path'] for x in entries}) == len(entries)
        by_parent = defaultdict(list)
        dirs = {'': tree_sha}
        for entry in entries:
            path = PurePosixPath(entry['path'])
            assert not path.is_absolute() and '..' not in path.parts
            parent = str(path.parent)
            by_parent['' if parent == '.' else parent].append(entry)
            if entry['type'] == 'tree':
                dirs[entry['path']] = entry['sha']
        checks = []
        for directory, expected in dirs.items():
            payload = b''
            children = sorted(by_parent[directory], key=lambda x:
                              (PurePosixPath(x['path']).name +
                               ('/' if x['type'] == 'tree' else '')).encode())
            for entry in children:
                mode = entry['mode'].lstrip('0')
                name = PurePosixPath(entry['path']).name
                payload += (mode + ' ' + name).encode() + b'\0' + bytes.fromhex(entry['sha'])
            got = hashlib.sha1(b'tree ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
            checks.append({'directory': directory, 'ok': got == expected})
        assert all(x['ok'] for x in checks)
        blobs = [x for x in entries if x['type'] == 'blob']
        groups = defaultdict(lambda: {'files': 0, 'blob_bytes': 0})
        proposed_files = []
        for entry in blobs:
            top = entry['path'].split('/')[0]
            groups[top]['files'] += 1
            groups[top]['blob_bytes'] += entry['size']
            proposed_files.append({'path': entry['path'], 'git_blob': entry['sha'],
                                   'mode': entry['mode'], 'bytes': entry['size'],
                                   'proposed_url': 'https://raw.githubusercontent.com/' + REPO + '/' +
                                                   COMMIT + '/' + urllib.parse.quote(entry['path'], safe='/')})
        result = {
            'task': 'T-038', 'status': 'CANDIDATE; CHUA DUYET TAI',
            'purpose': 'Snapshot tham khao co dieu kien; khong xac nhan sinh RE2-TT',
            'selection_reason': 'Moc release named v1.0.0 duoc repo cong bo; khong chon theo graph',
            'repository': 'https://github.com/' + REPO,
            'tag': 'v1.0.0', 'commit': COMMIT, 'commit_date': commit['committer']['date'],
            'tree': tree_sha, 'metadata_tree_url': audit[-1]['url'],
            'metadata_only': True, 'new_source_bodies_saved': False,
            'full_tree_entries': len(entries), 'full_tree_blob_count': len(blobs),
            'full_tree_blob_bytes': sum(x['size'] for x in blobs),
            'tree_object_checks': checks,
            'gitlinks': [x for x in entries if x['type'] == 'commit'],
            'modes': dict(Counter(x['mode'] for x in entries)),
            'groups': dict(sorted(groups.items())),
            'proposed_files': proposed_files,
            'download_scope': 'all Git blobs in identified tree; no extension whitelist',
            'proposed_destination': 'results/T-038/sources/train-ticket-v1.0.0/',
            'source_download_performed': False,
            'network': {'raw_blob_payload_bytes_without_retries': sum(x['size'] for x in blobs),
                        'requests': len(blobs), 'headers_tls_retries_bytes': None,
                        'compressed_archive_bytes': None, 'archive_requested': False},
            'disk': {'git_blob_contents_bytes': sum(x['size'] for x in blobs),
                     'metadata_and_allocation_overhead_bytes': None,
                     'all_future_runs_intermediates_bytes': None,
                     'archive_expansion_bytes': None},
            'open': ['application_to_dataset_lineage', 'instrumentation_revision',
                     'image_digest', 'deployment_revision', 'external_dependencies',
                     'LFS_pointers_and_embedded_archives', 'single_session_feasibility'],
        }
        (out / 'de-xuat-tai.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({k: result[k] for k in ['tag', 'commit', 'tree', 'full_tree_entries',
                         'full_tree_blob_count', 'full_tree_blob_bytes', 'gitlinks', 'modes']}, ensure_ascii=False))
    except BaseException as exc:
        (out / 'error.txt').write_text(repr(exc), encoding='utf-8')
        raise
    finally:
        (out / 'metadata-requests.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
