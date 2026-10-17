"""Kiểm diff/phạm vi và manifest của bước trước triển khai; không chạy RCA."""
import ast
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/T-038'
RUN = OUT / 'runs/ket-phien-001'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def diff(before, after, name):
    return ''.join(difflib.unified_diff(before.decode('utf-8-sig').splitlines(keepends=True),
                                      after.decode('utf-8-sig').splitlines(keepends=True),
                                      fromfile=name + ':before-session', tofile=name + ':after-session'))


def main():
    assert not (OUT / 'manifest.json').exists(), 'Do not overwrite prior manifest/run'
    checks = {}
    baseline_dir = OUT / 'runs/kiem-dau-vao-001'
    baseline = load(baseline_dir / 'baseline.json')
    log = ROOT / 'tasks/T-038-p5b-trainticket/LOG.md'
    old_log = (baseline_dir / 'LOG-before.md').read_bytes()
    checks['log_append_only'] = log.read_bytes().startswith(old_log)
    protected = {}
    for name, value in baseline.items():
        if name not in {'docs/STATE.md', 'tasks/T-038-p5b-trainticket/LOG.md'}:
            protected[name] = sha(ROOT / name) == value['sha256']
    checks['protected_preexisting_files_unchanged'] = all(protected.values())
    before = (RUN / 'STATE-immediate-before.md').read_bytes()
    after = (RUN / 'STATE-immediate-after.md').read_bytes()
    row = re.compile(rb'(?m)^\| T-038 \|[^\r\n]*')
    checks['state_exactly_one_row'] = (len(row.findall(before)) == len(row.findall(after)) == 1 and
                                         row.sub(b'T038_ROW', before) == row.sub(b'T038_ROW', after))
    # File chung có thể được nhánh khác cập nhật sau khi mình nhả lock. Không ghi lại nó.
    state_now = (ROOT / 'docs/STATE.md').read_bytes()
    checks['own_state_row_still_present'] = row.findall(state_now) == row.findall(after)
    state_external_changes = row.sub(b'T038_ROW', state_now) != row.sub(b'T038_ROW', after)
    inputs = load(OUT / 'runs/kiem-dau-vao-002/input-verification.json')
    checks['input_manifests_still_pinned'] = all(sha(ROOT / p) == v['sha256']
                                                   for p, v in inputs['input_manifests'].items())
    checks['pinned_code_still_matches'] = all(sha(ROOT / p['path']) == p['expected']
                                                for p in inputs['pinned_code'])
    proposal = load(OUT / 'runs/metadata-de-xuat-001/de-xuat-tai.json')
    files = proposal['proposed_files']
    checks['download_plan_partitions_and_bytes'] = (
        len({x['path'] for x in files}) == len(files) == proposal['full_tree_blob_count'] and
        sum(x['bytes'] for x in files) == proposal['full_tree_blob_bytes'] and
        sum(x['blob_bytes'] for x in proposal['groups'].values()) == proposal['full_tree_blob_bytes'] and
        all(x['ok'] for x in proposal['tree_object_checks']))
    checks['candidate_not_downloaded'] = not (OUT / 'sources').exists() and not proposal['source_download_performed']
    checks['preflight_and_graph_checks_passed'] = inputs['ok'] and load(OUT / 'runs/mien-graph-002/graph-scope.json')['ok']
    checks['failed_runs_preserved'] = all((OUT / p).is_file() for p in [
        'runs/kiem-dau-vao-001/preflight.py', 'runs/kiem-dau-vao-001/input-verification.json',
        'runs/mien-graph-001/audit_graph_scope.py', 'runs/mien-graph-001/graph-scope.json'])
    source = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    prompt = (OUT / 'prompt-claude.txt').read_text(encoding='utf-8')

    def block(section):
        return re.search(r'```text\n(.*?)\n```', source[source.index(section):], re.S).group(1)

    body = block('## Prompt chung').split('\nKhông sửa ngoài phạm vi trên,', 1)[1]
    checks['prompt_template_verbatim'] = (
        '\nKhông sửa ngoài phạm vi trên,' + body in prompt and
        prompt.endswith(block('### Soát SPEC') + '\n\n' + block('### G3 —') + '\n') and
        prompt.rstrip() in log.read_text(encoding='utf-8-sig'))
    json_files = list(OUT.rglob('*.json'))
    for path in json_files:
        load(path)
    py_files = list(OUT.rglob('*.py'))
    for path in py_files:
        ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    checks['all_existing_json_parse'] = True
    checks['all_python_sources_parse'] = True
    checks['no_bytecode_generated'] = not list(OUT.rglob('__pycache__'))
    (RUN / 'STATE.diff').write_text(diff(before, after, 'docs/STATE.md'), encoding='utf-8')
    result = {'task': 'T-038', 'client_date': '2026-10-16',
              'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'checks': checks,
              'protected_files': protected, 'shared_state_changed_after_release': state_external_changes,
              'review_prompt_sha256': sha(ROOT / 'docs/review-prompt.md'),
              'command': 'py -3 -X utf8 -B results/T-038/finalize.py',
              'json_files_parsed_before_finalize': len(json_files), 'python_sources_parsed': len(py_files),
              'scientific_task_complete': False, 'application_download_authorized': False,
              'spec_or_decision_changed': False, 'commit_push': False,
              'ok': all(checks.values())}
    if not result['ok']:
        (RUN / 'final-verification-failed.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        raise AssertionError([key for key, value in checks.items() if not value])
    addition = ('\n\n**Bổ sung kiểm cuối Phiên 2 — 16/10/2026:** finalize.py kiểm append-only LOG, '
                'diff STATE chỉ dòng T-038, nguồn bảo vệ/pin hiện hành, phân hoạch/byte đề xuất, '
                'prompt nguyên văn, mọi JSON và cú pháp Python, không sinh bytecode: đạt. '
                'Giữ các lượt lỗi và toàn bộ file kết quả, ghi diff và manifest riêng T-038; '
                'không đổi SPEC/quyết định khoa học hoặc tự nghiệm thu. Lệnh cuối đã chạy: '
                '`py -3 -X utf8 -B results/T-038/finalize.py`. Bước tiếp vẫn chờ Minh quyết '
                'đúng các nội dung ở đề xuất; không tự tải hoặc mở phần B.\n')
    with log.open('ab') as handle:
        handle.write(addition.encode('utf-8'))
    (RUN / 'LOG.diff').write_text(diff(old_log, log.read_bytes(), 'tasks/T-038-p5b-trainticket/LOG.md'), encoding='utf-8')
    result['external_mutations'] = [
        {'path': 'tasks/T-038-p5b-trainticket/LOG.md', 'change': 'append-only', 'sha256': sha(log)},
        {'path': 'docs/STATE.md', 'change': 'only T-038 row in immediate before/after',
         'written_sha256': hashlib.sha256(after).hexdigest(), 'current_sha256': sha(ROOT / 'docs/STATE.md')}]
    (RUN / 'final-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    artifact_files = sorted(p for p in OUT.rglob('*') if p.is_file())
    artifacts = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                  'sha256': sha(p)} for p in artifact_files]
    manifest = {'task': 'T-038', 'client_date': '2026-10-16',
                'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'status': 'preflight done; pending source approval and feasibility/scope decision',
                'current_input_verification': 'runs/kiem-dau-vao-002/input-verification.json',
                'current_graph_scope': 'runs/mien-graph-002/graph-scope.json',
                'source_proposal': 'runs/metadata-de-xuat-001/de-xuat-tai.json',
                'input_manifests': inputs['input_manifests'], 'shared_T036_pin': inputs['pin'],
                'file_count': len(artifacts), 'total_artifact_bytes': sum(x['bytes'] for x in artifacts),
                'files': artifacts, 'excludes': 'manifest self; external LOG/STATE hashes in final-verification',
                'scientific_task_complete': False, 'new_source_payload_saved': False,
                'commit_push': False}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    assert all(sha(ROOT / entry['path']) == entry['sha256'] and
               (ROOT / entry['path']).stat().st_size == entry['bytes'] for entry in artifacts)
    assert log.read_bytes().startswith(old_log)
    print(json.dumps({'ok': True, 'checks': checks, 'file_count': len(artifacts),
                      'artifact_bytes': manifest['total_artifact_bytes'],
                      'external_changes': [x['path'] for x in result['external_mutations']],
                      'state_changed_by_other_session_after_release': state_external_changes}, ensure_ascii=False))


if __name__ == '__main__':
    main()
