"""Kết thúc gói đã duyệt sau kiểm đầy đủ; giữ receipt/diff và cập nhật manifest."""
import ast
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
OUT = ROOT / 'results/T-035'


def read(path):
    return json.loads(path.read_text('utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def main():
    pre = read(BASE / 'preflight.json')
    comparison = read(BASE / 'comparison.json')
    assert comparison['pass']
    assert read(BASE / 'full-command-002.json')['returncode'] == 0
    # Tài liệu đã sinh phải tái tạo đúng từ cùng bằng chứng, không viết lại ở kiểm này.
    renderer = runpy.run_path(str(BASE / 'update_docs.py'))['render']
    assert all((OUT / name).read_text('utf-8') == text for name, text in renderer().items())
    receipt = read(BASE / 'oracle-before-code.json')
    for path, expected in receipt['files'].items():
        assert sha(BASE / path) == expected, 'oracle_or_design_changed'
    assert receipt['builder_before'] == sha(BASE / 'before/src/do_thi/builder.py')
    governing = {x['path']: x['sha256'] for x in read(BASE / 'input-verification.json')['governing']}
    for name, expected in governing.items():
        assert sha(ROOT / name) == expected, name
    old_results = [read(BASE / f'fixture-cu-seed{i}-002/result.json') for i in range(3)]
    new_results = [read(BASE / f'fixture-v2-seed{i}-002/result.json') for i in range(3)]
    boundary = [read(BASE / f'boundary-seed{i}-002/result.json') for i in range(3)]
    assert all(x['pass'] for x in boundary)
    assert boundary[0]['cases'] == boundary[1]['cases'] == boundary[2]['cases']
    boundary_receipt = read(BASE / 'boundary-oracle-before-code.json')
    assert sha(BASE / 'check_missing_attributes.py') == boundary_receipt['oracle']
    assert sha(BASE / 'boundary-before/src/do_thi/builder.py') == boundary_receipt['builder_before']
    for name in ['src/do_thi/builder.py', 'results/T-035/scripts/run.py']:
        assert sha(ROOT / name) == sha(BASE / 'day-du-002/code' / name), 'full_run_code_changed'
    assert all(x['builder_sha256'] == sha(ROOT / 'src/do_thi/builder.py') for x in boundary)
    assert all(x['sources'][0]['sha256'] == sha(ROOT / 'src/do_thi/builder.py') for x in new_results)
    assert old_results[0] == old_results[1] == old_results[2]
    assert len({sha(BASE / f'fixture-cu-seed{i}-002/result.json') for i in range(3)}) == 1
    assert new_results[0]['fixtures'] == new_results[1]['fixtures'] == new_results[2]['fixtures']
    assert all(x['pass'] for x in new_results)
    assert all(x['label_rejection'] for x in old_results)
    log = ROOT / 'tasks/T-035-p5-do-thi-tu-trace/LOG.md'
    marker = '**Kết thúc Phiên 7 — sửa hợp đồng và hồi quy:**'
    assert marker not in log.read_text('utf-8'), 'final_log_already_written'
    with log.open('a', encoding='utf-8') as f:
        f.write(f'''\n{marker}

1. **Đã làm:** sửa hợp đồng v2 và bộ dựng để tách địa chỉ phát, queue nhận, phạm vi định danh; giữ địa chỉ qua cạnh/phép chiếu/fingerprint. Thêm diagnostic và điều kiện từ chối nối mâu thuẫn/đa nghĩa. Thiết kế/WHY và oracle được ghi trước code. Đã soạn prompt Codex sạch theo yêu cầu Minh, soát toàn T-035 như lần đầu; Claude vẫn là người phản biện chính thức.
2. **File:** đúng danh sách Q-154/preflight.json, cộng đầu ra dưới results/T-035/runs/sua-n1-001/. LOG chỉ nối, STATE chỉ dòng T-035. Giữ mọi kết quả/lượt cũ; bản trước của file sửa trong before/, bản sau trong after/. Không sửa SPEC, AGENTS, MRP, LESSONS, baseline, src/p3, task khác hoặc hệ FlashTicket. Không commit/push.
3. **Kiểm:** 362 kiểm đầu vào cũ đạt trước chạy; manifest cũ đầy đủ đã kiểm ở preflight. 18 fixture cũ, 33 fixture messaging và 3 ca thiếu toàn attributes/links đạt seed0/1/2; outputs fixture giữa seed giống nhau. Bản v1 chạy trên oracle mới giữ riêng, không gọi số fail schema là số lỗi ngữ nghĩa. Lượt day-du-001 dừng sau tự kiểm để sửa nhánh thiếu dữ liệu; giữ interruption.json và toàn bộ output. Toàn bộ {comparison['case_count']} ca ở day-du-002 chạy mới bằng code cuối (kiểm hash), không reuse, {comparison['window_count']} khoảng K1/K2/K4/K5 đạt; {comparison['graph_count']} graph byte bằng cũ, nội dung ca/vocabulary/Node/coverage/checks bằng cũ ngoài chi phí máy. Nguồn: comparison.json và các result.json trong lượt sửa. Chi phí thực {comparison['seconds']/60:.2f} phút, RAM đỉnh {comparison['peak_rss_bytes']/1024**3:.2f} GiB. Kiểm cuối gồm source/diff/file set, JSON/AST, oracle bất biến, tái sinh tài liệu, hash manifest; receipt tại final-verification.json.
4. **Mức kết luận:** N1 đã được xử lý trong hợp đồng/bộ dựng theo fixture; chưa là kiểm routing hoặc instrumentation FlashTicket thật. Dev không có messaging nên hồi quy không thay bằng chứng fixture. Tiêu chí 1/9 được trình lại ở mức hợp đồng v2, chờ tự soát phiên sạch, phản biện chính thức và Minh nghiệm thu. C1–C9 vẫn là mô tả khả năng dựng/giữ thông tin; chưa trả lời RQ3, chưa chọn P6, chưa hoàn tất P5/G3. Node host, semantics cạnh/thời gian, nguồn sinh metadata mức ngày, nguyên nhân vắng cạnh và trace FlashTicket thật còn OPEN như báo cáo. Không thêm giả thuyết khoa học đã xác nhận.

**Quyết định của Minh trong phiên:** Q-154 ghi nguyên văn lời duyệt gói và yêu cầu prompt Codex sạch. Không đổi vai trò chính thức hoặc nghiệm thu task. Thiết kế kỹ thuật bổ sung WHY-52 ghi đúng mục đích DT18/nhu cầu kỹ thuật, không dựng hạn chế RCA để biện minh.

**Bước tiếp theo chính xác:** Minh mở phiên Codex mới, dán toàn bộ prompt-codex-sach-soat-t035.txt dưới lượt này. Phiên đó chỉ đọc/tự soát toàn task, lập nhận xét trước lịch sử, không phải chỉ kiểm bản sửa. Nguồn đầu: AGENTS, SPEC, mục tiêu MRP/DT18/cô, code và graph/JSON theo manifest. Không chạy lại dev đã có đầu ra hợp lệ hoặc mở locked. Prompt Claude vẫn được soạn để Minh chọn chuyển thủ công; không tự mở/gửi phiên.

**Lệnh đã chạy:** Python D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B. Fixture cũ: results/T-035/fixture/check.py với tên sua-n1-001/fixture-cu-seed0-002, fixture-cu-seed1-002, fixture-cu-seed2-002. Fixture mới: runs/sua-n1-001/check_messaging.py với fixture-v1-001 --builder-path before/src/do_thi/builder.py và fixture-v2-seed0-002, fixture-v2-seed1-002, fixture-v2-seed2-002. Ba ca thiếu thuộc tính: check_missing_attributes.py với boundary-seed0-002, boundary-seed1-002, boundary-seed2-002 trong cùng lượt. Lượt đầy đủ cuối: runs/sua-n1-001/launch_full_final.py gọi scripts/run.py sua-n1-001/day-du-002. Đối chiếu: runs/sua-n1-001/compare_full.py. Tài liệu: scripts/write_docs.py. Mọi đường script tương đối tính từ results/T-035/ nếu chưa có prefix đó. Không dùng lại tên output đã tồn tại.

**Lệnh kết thúc/kiểm cuối:** & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-035/runs/sua-n1-001/finalize.py; sau đó đọc lại hash manifest và trạng thái git chỉ đọc. Các kiểm cuối chỉ xác nhận phạm vi và tính nhất quán đầu ra, không thêm thực nghiệm hoặc cổng.

**Đề xuất commit, chưa thực hiện:** fix: separate messaging identity and queue addresses in T-035. Minh duyệt riêng commit/push; phiên này giữ working tree.

### Prompt Codex sạch — tự soát toàn T-035

```text
''')
        f.write((BASE / 'prompt-codex-sach-soat-t035.txt').read_text('utf-8'))
        f.write('\n```\n\n### Prompt Claude — soát kết quả\n\nMinh chuyển thủ công nếu muốn; chưa cấp quyền ghi REVIEW.\n\n```text\n')
        f.write((BASE / 'prompt-claude-soat-ket-qua.txt').read_text('utf-8'))
        f.write('\n```\n')
    state = ROOT / 'docs/STATE.md'
    lines = state.read_text('utf-8').splitlines()
    row = '| T-035 | P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace | P5 (G3) | Codex | Claude | Đã sửa hợp đồng v2 và kiểm lại theo Q-154 (15/10/2026); chờ phiên Codex sạch tự soát toàn task theo lời Minh, rồi phản biện/nghiệm thu. Kết quả và prompt tại results/T-035/runs/sua-n1-001/, LOG Phiên 7. Chưa chọn P6/đóng task. | `tasks/T-035-p5-do-thi-tu-trace/` |'
    assert sum(x.startswith('| T-035 |') for x in lines) == 1
    state.write_text('\n'.join(row if x.startswith('| T-035 |') else x for x in lines) + '\n', 'utf-8')
    allowed = set(pre['allowed_files'])
    changed, deleted = [], []
    for name, old in pre['files'].items():
        path = ROOT / name
        if not path.is_file():deleted.append(name)
        elif sha(path) != old['sha256']:changed.append(name)
    assert not deleted
    assert set(changed) <= allowed, sorted(set(changed) - allowed)
    for name in ['docs/WHY.md', 'docs/DECISIONS.md', 'tasks/T-035-p5-do-thi-tu-trace/LOG.md']:
        assert (ROOT / name).read_text('utf-8').startswith((BASE / 'before' / name).read_text('utf-8')), name
    strip_row = lambda text: [x for x in text.splitlines() if not x.startswith('| T-035 |')]
    assert strip_row(state.read_text('utf-8')) == strip_row((BASE / 'before/docs/STATE.md').read_text('utf-8'))
    for name in changed:
        if name == 'results/T-035/manifest.json':continue
        target = BASE / 'after' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    current = {}
    for folder in ['src', 'docs', 'tasks', 'results/T-035']:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                current[path.relative_to(ROOT).as_posix()] = path
    added = sorted(set(current) - set(pre['files']))
    prefix = BASE.relative_to(ROOT).as_posix() + '/'
    assert all(x.startswith(prefix) for x in added), [x for x in added if not x.startswith(prefix)]
    parsed = {'python': 0, 'json': 0}
    for name in sorted(set(added) | set(changed)):
        path = ROOT / name
        if path.suffix == '.py':ast.parse(path.read_text('utf-8'), filename=name);parsed['python'] += 1
        elif path.suffix == '.json':read(path);parsed['json'] += 1
    diff = []
    for name in changed:
        if name.endswith('/manifest.json'):continue
        a=(BASE/'before'/name).read_text('utf-8');b=(ROOT/name).read_text('utf-8')
        diff.extend(difflib.unified_diff(a.splitlines(True), b.splitlines(True), fromfile='before/'+name, tofile=name))
    (BASE / 'changes.diff').write_text(''.join(diff), 'utf-8')
    check = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    assert check.returncode == 0, check.stdout + check.stderr
    previous = read(BASE / 'before/results/T-035/manifest.json')
    retained = []
    for item in previous['files']:
        if item['path'] not in allowed:
            assert sha(ROOT / item['path']) == item['sha256'], item['path']
            retained.append(item['path'])
    verification = {'created_utc': datetime.now(timezone.utc).isoformat(), 'pass': True,
                    'changed_existing': sorted(set(changed) | {'results/T-035/manifest.json'}),
                    'added_before_final_receipts': added, 'deleted': deleted,
                    'outside_approved': [], 'retained_old_artifacts': len(retained),
                    'append_only_sources': True, 'state_only_T035_row': True,
                    'SPEC_AGENTS_unchanged': True, 'oracle_design_unchanged': True,
                    'fixture_seed_outputs_equal': True, 'documentation_reproducible': True,
                    'parsed': parsed, 'git_diff_check': check.returncode,
                    'source_hashes': {p: sha(ROOT/p) for p in allowed if p != 'results/T-035/manifest.json'},
                    'comparison': 'comparison.json', 'full_command': 'full-command-002.json',
                    'no_commit_push': True, 'no_test_heldout': True}
    write(BASE / 'final-verification.json', verification)
    # Manifest giữ nguyên tập artifact trước, cập nhật đúng file được duyệt và thêm lượt mới.
    paths = {x['path'] for x in previous['files']}
    paths.update(p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file())
    files=[]
    for name in sorted(paths):
        path=ROOT/name
        files.append({'path':name,'bytes':path.stat().st_size,'sha256':sha(path)})
    manifest = dict(previous, files=files, artifact_count=len(files), total_bytes=sum(x['bytes'] for x in files),
                    created_utc=datetime.now(timezone.utc).isoformat(),
                    final_verification='runs/sua-n1-001/final-verification.json',
                    previous_manifest='runs/sua-n1-001/before/results/T-035/manifest.json',
                    source_verification='runs/sua-n1-001/input-verification.json',
                    scope=pre['allowed_files'] + [pre['allowed_new_directory'] + '/'],
                    decisions_recorded=['Q-154'], design_revision='v2',
                    task_state='awaiting_fresh_codex_self_audit_and_official_review')
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=1), 'utf-8')
    for item in files:
        assert sha(ROOT / item['path']) == item['sha256']
    print(json.dumps({'pass': True, 'manifest_files': len(files), 'changed_existing': verification['changed_existing'],
                      'retained_old_artifacts': len(retained), 'new_directory': pre['allowed_new_directory']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
