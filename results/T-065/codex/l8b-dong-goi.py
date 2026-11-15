"""Chốt hash trên exp-obs và tạo gói nhỏ để nhận; không đổi kho/dữ liệu cũ."""
import importlib.util
import json
import pathlib
import tarfile

spec = importlib.util.spec_from_file_location('l8b_export', pathlib.Path(__file__).with_name('l8b-xuat.py'))
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)
R = X.ROOT
X.stop()
before = X.read(R / 'kiem/may-truoc.json')
after = X.inventory()
changed = [p for p, v in before['files'].items() if after['files'].get(p) != v]
assert not changed, changed
new_pinned = [p for p in after['files'] if p not in before['files']]
assert {pathlib.Path(p).name for p in new_pinned} == {X.UID + '.json', X.REPLAY + '.json'}
assert before['machine']['started_at'] == after['machine']['started_at']
assert before['machine']['restart_count'] == after['machine']['restart_count']
old_l8 = R.parent / 't065-l8-001'
expected = X.read(R / 'old-l8-expected.json')
for rel, v in expected.items():
    p = old_l8 / rel
    assert X.sha(p) == v['sha256'] and p.stat().st_size == v['bytes'], str(p)
X.write(R / 'kiem/may-sau.json', {
    'utc': X.now(), 'before_machine': before['machine'], 'after_machine': after['machine'],
    'old_files_checked': len(before['files']), 'old_files_changed': [], 'old_L8_history_checked': len(expected),
    'new_dashboards': {p: after['files'][p] for p in new_pinned}, 'restart_by_agent': False,
    'compose_provider_datasource_unchanged': True,
    'rollback': 'Chỉ hai file dashboard mới và thư mục t065-l8b-001; giữ bản trước fix01 trong rollback/fix01. Chưa hoàn tác.'})
manifest_path = R / 'kiem/manifest-may.json'
files = {}
for p in sorted(R.rglob('*')):
    if p.is_file() and p != manifest_path and p.suffix != '.tgz':
        files[str(p.relative_to(R))] = {'sha256': X.sha(p), 'bytes': p.stat().st_size}
X.write(manifest_path, {'utc': X.now(), 'files': files, 'excluded': ['kiem/manifest-may.json (self hash)', '*.tgz (transport archives)']})
archive = R / 'ban-giao-001.tgz'
assert not archive.exists(), 'Giữ archive trước; lượt mới phải dùng tên mới'
with tarfile.open(archive, 'w:gz') as tar:
    for rel in files:
        tar.add(R / rel, arcname=rel, recursive=False)
    tar.add(manifest_path, arcname=str(manifest_path.relative_to(R)), recursive=False)
print(json.dumps({'utc': X.now(), 'archive': str(archive), 'archive_bytes': archive.stat().st_size, 'archive_sha256': X.sha(archive),
                  'manifest_sha256': X.sha(manifest_path), 'files': len(files), 'uncompressed_bytes': sum(x['bytes'] for x in files.values()),
                  'old_files_unchanged': len(before['files']), 'old_L8_history_unchanged': len(expected), 'new_dashboards': list(after['files'][p]['sha256'] for p in new_pinned)}, ensure_ascii=False))
