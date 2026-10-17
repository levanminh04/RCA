"""Chốt bằng chứng, LOG/STATE và manifest trong phạm vi gói Q-155."""
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


def snapshot():
    return {p.relative_to(ROOT).as_posix(): p
            for folder in ['src', 'docs', 'tasks', 'results/T-035']
            for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def main():
    pre = read(BASE / 'preflight.json')
    allowed = set(pre['allowed_files'])
    previous = read(BASE / 'before/results/T-035/manifest.json')
    c = read(BASE / 'comparison.json')
    assert c['pass'] and c['reused_cases'] == 0
    assert read(BASE / 'full-command.json')['returncode'] == 0
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == pre['HEAD']
    rendered = runpy.run_path(str(BASE / 'update_docs.py'))['render']()
    assert all((OUT / name).read_text('utf-8') == value for name, value in rendered.items())
    for item in read(BASE / 'input-verification.json')['governing']:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']
    original_oracle = read(BASE / 'oracle-before-code.json')
    for item in original_oracle['files']:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']
    assert sha(BASE / 'before/src/do_thi/builder.py') == original_oracle['before_builder_sha256']
    # Oracle sửa chỉ phép so container; toàn hàm tạo literal phải giống bản đóng băng.
    oracle_ast = ast.parse((BASE / 'oracle.py').read_text('utf-8'))
    revised_ast = ast.parse((BASE / 'oracle_json.py').read_text('utf-8'))
    factory = lambda tree: next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'fixture_cases')
    assert ast.dump(factory(oracle_ast)) == ast.dump(factory(revised_ast))
    revision = read(BASE / 'oracle-revision-002.json')
    assert sha(BASE / 'oracle_json.py') == revision['revised_oracle_sha256']
    assert revision['literal_cases_sha256_after'] == revision['literal_cases_sha256_before'] == original_oracle['literal_cases_sha256']
    frozen = read(BASE / 'frozen-code.json')['files']
    for name, expected in frozen.items():
        assert sha(ROOT / name) == expected == sha(BASE / 'day-du-001/code' / name), name
    oracle = [read(BASE / f'fixture-oracle-seed{i}-001/result.json') for i in range(3)]
    legacy = [read(BASE / f'fixture-cu-seed{i}-001/result.json') for i in range(3)]
    messaging = [read(BASE / f'fixture-messaging-seed{i}-001/result.json') for i in range(3)]
    missing = [read(BASE / f'fixture-missing-seed{i}-001/result.json') for i in range(3)]
    assert all(x['pass'] and x['case_count'] == x['passed'] == 129 for x in oracle)
    assert all(x['builder_sha256'] == frozen['src/do_thi/builder.py'] for x in oracle + missing)
    assert oracle[0]['cases'] == oracle[1]['cases'] == oracle[2]['cases']
    assert all(len(x['fixtures']) == 18 and x['label_rejection'] and all(y['pass'] for y in x['fixtures']) for x in legacy)
    assert len({sha(BASE / f'fixture-cu-seed{i}-001/result.json') for i in range(3)}) == 1
    assert all(x['pass'] and x['passed'] == 33 for x in messaging)
    assert messaging[0]['fixtures'] == messaging[1]['fixtures'] == messaging[2]['fixtures']
    assert all(x['pass'] and len(x['cases']) == 3 for x in missing)
    assert missing[0]['cases'] == missing[1]['cases'] == missing[2]['cases']
    for name in ['legacy-commands-001.json', 'oracle-commands-001.json']:
        assert read(BASE / name)['pass'] and read(BASE / name)['builder_sha256'] == frozen['src/do_thi/builder.py']
    retained = [item for item in previous['files'] if item['path'] not in allowed]
    for item in retained:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']
    current = snapshot()
    assert not set(pre['files']) - set(current), 'deleted_preexisting_file'
    changed = sorted(name for name, old in pre['files'].items() if sha(current[name]) != old['sha256'])
    assert set(changed) <= allowed, set(changed) - allowed
    added = sorted(set(current) - set(pre['files']))
    prefix = pre['allowed_new_directory'] + '/'
    assert all(name.startswith(prefix) for name in added), 'new_file_outside_scope'
    for name in sorted(set(added) | set(changed)):
        p = ROOT / name
        if p.suffix == '.py': ast.parse(p.read_text('utf-8'), filename=name)
        elif p.suffix == '.json': read(p)
    check = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    assert check.returncode == 0, check.stdout + check.stderr
    prompt_receipt = read(BASE / 'prompt-template-check.json')
    assert sha(ROOT / 'docs/review-prompt.md') == prompt_receipt['template_sha256']
    assert sha(BASE / 'prompt-codex-sach-soat-t035.txt') == prompt_receipt['codex_prompt_sha256']
    assert sha(BASE / 'prompt-claude-kiem-lai.txt') == prompt_receipt['claude_prompt_sha256']
    log = ROOT / 'tasks/T-035-p5-do-thi-tu-trace/LOG.md'
    marker = '**Kết thúc Phiên 8 — sửa bốn lỗi hợp đồng:**'
    assert marker not in log.read_text('utf-8')
    with log.open('a', encoding='utf-8') as f:
        f.write(f'''
{marker}

1. **Đã làm:** chuẩn hóa operationName thiếu về None ở mọi dtype; từ chối identifier_collision giữa thực thể quan sát/endpoint với thao tác ở Prepared/build/project; kiểm số nguyên/thời gian không âm và giới hạn trước ép/cộng/nhân int64; gộp unknown/known và từ chối kiểu đã biết mâu thuẫn. Nguồn chính sách v2.1 được ghi trước code. Không đổi định dạng ID/graph hợp lệ hoặc thiết kế RCA.
2. **File:** đúng 11 file trong preflight.json và đầu ra mới dưới runs/sua-hop-dong-001/. WHY/DECISIONS/LOG nối thêm; STATE chỉ dòng T-035. Giữ mọi artifact/lượt cũ, kể cả các lượt checker fail. Bản trước/sau ở before/ và after/. Không sửa SPEC, AGENTS, MRP, LESSONS, baseline, hệ FlashTicket; không commit/push hoặc mở test.
3. **Kiểm:** 4.310 artifact cũ và362nguồn khớp trước sửa. Oracle129ca ghi trước builder; giữ oracle.py, bản sửa comparator oracle_json.py chỉ chuẩn hóa JSON, literal/digest không đổi (receipt trước mã và revision002). 129ca mới+18ca gốc+33messaging+3biên cũ đạt seed0/1/2; outputs giữa seed giống nhau. Lượt đầy đủ {c['case_count']} ca/{c['window_count']} khoảng chạy mới không reuse, K1/K2/K4/K5 đạt; {c['graph_count']} graph byte bằng bản đã lưu, mọi nội dung ca trừ chi phí máy khớp bản v2. Nguồn comparison.json và các command/result trong lượt sửa. Chi phí {c['seconds']/60:.2f} phút, RAM đỉnh {c['peak_rss_bytes']/1024**3:.2f}GiB. Kiểm cuối: tái sinh tài liệu, hash code đóng băng/snapshot, AST/JSON, diff và tập file, bảo toàn artifact cũ; biên nhận final-verification.json và manifest.
4. **Mức kết luận / còn mở:** cả bốn nhận xét đúng, đã xử lý theo oracle và hồi quy trong miền đã kiểm. Hai phép chiếu cùng khớp không đủ chứng minh đúng đích; fixture đích literal là bằng chứng bổ sung. ID va chạm bị từ chối rõ, không gọi là đã hỗ trợ ID tùy ý trùng nhau. Chưa xác nhận nghĩa vật lý cạnh/Node, routing/instrumentation FlashTicket thật, lợi ích RCA hoặc chọn P6. Chưa tự nghiệm thu/đóng T-035/P5/G3/RQ3. Chờ phiên Codex sạch soát toàn task như lần đầu, rồi phản biện chính thức và Minh nghiệm thu; Claude vẫn phản biện chính thức.

**Phản hồi từng nhận xét Minh chuyển:** (1) Đúng: NaN/pd.NA trước sửa làm lỗi khóa/JSON; v2.1 giữ null và missing count/vocabulary. (2) Đúng: ID component có thể bị đọc như thao tác; v2.1 từ chối va chạm ở cả API dựng/chiếu, oracle có đích literal và đối chứng. (3) Đúng: trước sửa nhận âm/wrap; v2.1 từ chối trước tính và giữ ưu tiên ns. (4) Đúng: kiểu phụ thuộc thứ tự; v2.1 cùng quy tắc gộp inventory/span/endpoint, không quyết kiểu nào đúng khi mâu thuẫn. Minh quyết sửa cả bốn qua Q-155; chưa là nghiệm thu bản sửa. Bản nhận xét gốc giữ nguyên trong nhan-xet-duoc-minh-chuyen.txt.

**Quyết định Minh trong phiên:** Q-155 ghi nguyên văn lời duyệt gói và yêu cầu prompt Codex sạch. Bổ sung WHY-52 ghi lựa chọn kỹ thuật, phương án namespace thay thế và giới hạn. Không thêm giả thuyết khoa học đã xác nhận.

**Bước tiếp theo chính xác:** Minh mở phiên Codex mới, dán toàn prompt-codex-sach-soat-t035.txt ở lượt này. Phiên đó đọc yêu cầu nguồn/SPEC/hợp đồng/code/graph/JSON trước; ghi nhận xét độc lập rồi mới đối chiếu lịch sử, không chỉ kiểm bốn điểm vừa sửa. Phạm vi chỉ đọc trong chat; không chạy lại lượt dev hợp lệ hoặc mở locked. Prompt Claude kiểm lại cũng kèm để Minh chọn chuyển thủ công, không tự mở/gửi phiên.

**Lệnh đã chạy:** Python D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B; start.py; oracle.py fixture-before-001 --builder-path before/src/do_thi/builder.py, oracle.py fixture-after-001; oracle_json.py fixture-before-002 --builder-path before/src/do_thi/builder.py; run_fixtures.py legacy, run_fixtures.py oracle; launch_full.py gọi results/T-035/scripts/run.py sua-hop-dong-001/day-du-001; compare_full.py; results/T-035/scripts/write_docs.py. Các script không có prefix đầy đủ tính từ results/T-035/runs/sua-hop-dong-001/; --builder-path thực tế dùng đường từ repo như command/output. Không ghi đè tên output cũ.

**Lệnh cuối / kiểm kết thúc:** & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-035/runs/sua-hop-dong-001/finalize.py; sau đó đọc lại hash manifest và trạng thái git. Đề xuất commit (chưa làm): fix: enforce T-035 graph input and identity contracts.

### Prompt Codex sạch — tự soát toàn T-035

```text
''')
        f.write((BASE / 'prompt-codex-sach-soat-t035.txt').read_text('utf-8'))
        f.write('\n```\n\n### Prompt Claude — kiểm lại\n\nMinh chuyển thủ công nếu muốn; chưa cấp quyền ghi REVIEW.\n\n```text\n')
        f.write((BASE / 'prompt-claude-kiem-lai.txt').read_text('utf-8'))
        f.write('\n```\n')
    state = ROOT / 'docs/STATE.md'
    lines = state.read_text('utf-8').splitlines()
    row = '| T-035 | P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace | P5 (G3) | Codex | Claude | Đã sửa bốn lỗi hợp đồng v2.1 và kiểm hồi quy theo Q-155 (15/10/2026); chờ phiên Codex sạch tự soát toàn task như lần đầu, rồi phản biện/nghiệm thu. Kết quả và prompt tại results/T-035/runs/sua-hop-dong-001/, LOG Phiên 8. Chưa chọn P6/đóng task. | `tasks/T-035-p5-do-thi-tu-trace/` |'
    assert sum(x.startswith('| T-035 |') for x in lines) == 1
    state.write_text('\n'.join(row if x.startswith('| T-035 |') else x for x in lines) + '\n', 'utf-8')
    for name in ['docs/WHY.md', 'docs/DECISIONS.md', 'tasks/T-035-p5-do-thi-tu-trace/LOG.md']:
        assert (ROOT / name).read_text('utf-8').startswith((BASE / 'before' / name).read_text('utf-8')), name
    without_row = lambda value: [x for x in value.splitlines() if not x.startswith('| T-035 |')]
    assert without_row(state.read_text('utf-8')) == without_row((BASE / 'before/docs/STATE.md').read_text('utf-8'))
    current = snapshot()
    changed = sorted(name for name, old in pre['files'].items() if sha(current[name]) != old['sha256'])
    assert set(changed) <= allowed
    diff = []
    for name in changed:
        if name == 'results/T-035/manifest.json': continue
        target = BASE / 'after' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
        diff.extend(difflib.unified_diff((BASE / 'before' / name).read_text('utf-8').splitlines(True),
                    (ROOT / name).read_text('utf-8').splitlines(True), fromfile='before/' + name, tofile=name))
    (BASE / 'changes.diff').write_text(''.join(diff), 'utf-8')
    verification = {'created_utc': datetime.now(timezone.utc).isoformat(), 'pass': True,
        'changed_existing': sorted(set(changed) | {'results/T-035/manifest.json'}),
        'approved_files': pre['allowed_files'], 'new_directory': pre['allowed_new_directory'],
        'outside_approved': [], 'deleted': [], 'retained_old_artifacts': len(retained),
        'append_only_sources': True, 'state_only_T035_row': True, 'SPEC_AGENTS_unchanged': True,
        'oracle_literal_unchanged': True, 'fixture_seed_outputs_equal': True,
        'new_fixture_cases': 129, 'existing_fixture_cases': 54, 'seed_count': 3,
        'documentation_reproducible': True, 'AST_JSON_pass': True, 'git_diff_check': check.returncode,
        'source_hashes': {name: sha(ROOT / name) for name in allowed if name != 'results/T-035/manifest.json'},
        'comparison': 'comparison.json', 'full_command': 'full-command.json',
        'no_commit_push': True, 'no_test_heldout': True}
    write(BASE / 'final-verification.json', verification)
    paths = {item['path'] for item in previous['files']}
    paths.update(p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file())
    files = [{'path': name, 'bytes': (ROOT / name).stat().st_size, 'sha256': sha(ROOT / name)} for name in sorted(paths)]
    manifest = dict(previous, files=files, artifact_count=len(files), total_bytes=sum(x['bytes'] for x in files),
        created_utc=datetime.now(timezone.utc).isoformat(), final_verification='runs/sua-hop-dong-001/final-verification.json',
        previous_full_verification=previous['final_verification'],
        previous_manifest='runs/sua-hop-dong-001/before/results/T-035/manifest.json',
        source_verification='runs/sua-hop-dong-001/input-verification.json',
        scope=pre['allowed_files'] + [pre['allowed_new_directory'] + '/'],
        decisions_recorded=list(dict.fromkeys(previous.get('decisions_recorded', []) + ['Q-155'])), design_revision='v2.1',
        task_state='awaiting_fresh_codex_self_audit_and_official_review')
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=1), 'utf-8')
    assert all(sha(ROOT / item['path']) == item['sha256'] for item in files)
    print(json.dumps({'pass': True, 'manifest_files': len(files), 'changed_existing': verification['changed_existing'],
                      'retained_old_artifacts': len(retained)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
