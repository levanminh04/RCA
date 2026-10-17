"""Bàn giao lượt sửa R1 đã duyệt; không chạy thực nghiệm hoặc sửa nguồn ngoài task."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'results/T-036'
OUT = BASE / 'runs/sua-r1-001'
TASK = ROOT / 'tasks/T-036-p5b-hop-dong-chung'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write('\n')


def permitted(path):
    return path.startswith('results/T-036/') or path in {
        'src/do_thi_tinh/compare.py', 'docs/STATE.md',
        'tasks/T-036-p5b-hop-dong-chung/LOG.md'}


def outside_status(text):
    return sorted(line for line in text.splitlines() if not permitted(line[3:]))


def block(template, heading):
    return re.search(r'```text\n(.*?)\n```', template.split(heading, 1)[1], re.S).group(1)


def main():
    if (OUT / 'final-verification.json').exists():
        raise RuntimeError('final_verification_already_exists')
    pre = read(OUT / 'preflight.json')
    previous = read(OUT / 'before/results/T-036/manifest.json')
    final_dir = BASE / 'runs/kiem-r1-after-002'
    final = read(final_dir / 'result.json')
    before = read(BASE / 'runs/kiem-r1-before-002/result.json')
    assert final['all_pass'] and final['failed'] == 0
    assert len([x for x in final['checks'] if x['name'].startswith('r1_')]) == 70
    assert all(c['ok'] for c in before['checks'] if not c['name'].startswith('r1_'))
    assert sum(not c['ok'] for c in before['checks']) == 22
    protected = [{'path': p, 'unchanged': sha(ROOT / p) == digest}
                 for p, digest in pre['protected_hashes'].items()]
    assert all(r['unchanged'] for r in protected)
    history = [{'path': p, 'unchanged': sha(ROOT / p) == digest}
               for p, digest in pre['historical_artifact_hashes'].items()]
    assert all(r['unchanged'] for r in history)
    source_checks = []
    for row in read(BASE / 'nguon.json')['sources']:
        path = Path(row['path'])
        path = path if path.is_absolute() else ROOT / path
        source_checks.append(dict(id=row['id'], ok=sha(path) == row['sha256']))
    assert all(r['ok'] for r in source_checks)
    assert all(sha(ROOT / p) == digest for p, digest in previous['input_manifests'].items())
    receipt = read(OUT / 'oracle-before-fix-002.json')
    assert sha(BASE / 'fixtures/r1.json') == receipt['fixture_sha256']
    assert sha(OUT / 'before/src/do_thi_tinh/compare.py') == receipt['comparator_before_sha256']
    stable = read(OUT / 'determinism-and-preservation.json')
    assert all(r['byte_equal'] for values in stable.values() if isinstance(values, list) for r in values)
    outside_diff = subprocess.check_output(
        ['git', 'diff', '--binary', '--', '.', ':(exclude)docs/STATE.md'], cwd=ROOT)
    outside_path = OUT / 'outside-tracked-before.diff'
    if outside_path.exists():
        assert outside_path.read_bytes() == outside_diff
    else:
        with outside_path.open('xb') as stream:
            stream.write(outside_diff)

    template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    common = block(template, '## Prompt chung')
    placeholders = re.findall(r'<[^>]+>', common)
    values = [
        'toàn bộ T-036; D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md',
        'soát kết quả toàn bộ task trong một phiên Codex sạch',
        'P5; chuẩn bị G3',
        'người làm là Codex ở các phiên triển khai và sửa T-036; người phản biện chính thức là Codex '
        'trong một phiên mới độc lập, thay Claude theo chỉ định trực tiếp của Minh. Minh đã cho phép '
        'ngoại lệ hai phiên Codex giữ hai vai trò này. SPEC/LOG/STATE còn giữ phân công lịch sử; '
        'chưa có quyền sửa SPEC hoặc các sổ phân công. Phiên nhận prompt này là người phản biện chính thức',
        'D:/RCA-flashticket/AGENTS.md; D:/RCA-flashticket/docs/STATE.md; '
        'D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md và LOG.md; '
        'D:/RCA-flashticket/docs/MRP.md; D:/RCA-flashticket/docs/WHY.md; '
        'D:/RCA-flashticket/docs/DECISIONS.md; D:/RCA-flashticket/docs/LESSONS.md; '
        'D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; '
        'D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md; '
        'D:/RCA-flashticket/results/T-036/nguon.json và các nguồn được registry liệt kê',
        'lịch sử các phiên và các lượt của task tại '
        'D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/LOG.md và '
        'D:/RCA-flashticket/results/T-036/runs/; chưa có file REVIEW chính thức. '
        'Nhận xét và phản hồi lịch sử được đọc sau khi đã lập nhận xét độc lập từ nguồn và đầu ra gốc',
        'D:/RCA-flashticket/results/T-036/manifest.json; hop-dong.md; nguon.json; fixtures/; runs/; '
        'kiem-dung-dan.md; ban-giao.md; D:/RCA-flashticket/src/do_thi_tinh/README.md và toàn bộ code; '
        'D:/RCA-flashticket/results/T-035/manifest.json và các đầu vào SPEC liệt kê. '
        'Diff các phiên tại D:/RCA-flashticket/results/T-036/runs/ket-phien-001/changes.diff và '
        'D:/RCA-flashticket/results/T-036/runs/sua-r1-001/changes.diff. '
        'Windows/PowerShell; môi trường Python và cách chạy theo README',
        'chỉ đọc và trả lời bản phản biện chính thức trong chat; chưa có quyền ghi REVIEW, LOG, '
        'STATE, SPEC, DECISIONS, code hoặc kết quả. Không thực hiện quyền triển khai của người làm từ SPEC',
    ]
    assert len(values) == len(placeholders)
    for placeholder, value in zip(placeholders, values):
        common = common.replace(placeholder, value, 1)
    stage = block(template, '### Soát kết quả')
    gate = block(template, '### G3 — Khóa thiết kế trước khi mở test')
    prompt = '\n\n'.join([common, stage, gate]) + '\n'
    assert not re.search(r'<[^>]+>', prompt)
    assert not re.search(r'\bR1\b|221|151|đã đạt|không có lỗi|đã xử lý', '\n'.join(values))
    (BASE / 'prompt-codex-clean.txt').write_text(prompt, encoding='utf-8')
    save(OUT / 'prompt-check.json', dict(
        template_sha256=sha(ROOT / 'docs/review-prompt.md'),
        common_exact_outside_metadata=True, stage_exact=stage in prompt, gate_exact=gate in prompt,
        scope='whole_task', official_reviewer='Codex fresh independent session per Minh',
        contains_no_finding_or_result_hint=True))

    report_path = BASE / 'kiem-dung-dan.md'
    report = report_path.read_text(encoding='utf-8-sig')
    start = report.index('\n\n')
    first = report.index('\n\n## 1.', start)
    report = report[:start] + (
        '\n\nBản hiện hành sau sửa R1 theo lời Minh duyệt ngày 15/10/2026. Codex thực hiện sửa và tự kiểm; '
        'phiên Codex sạch tiếp theo là phản biện chính thức toàn bộ T-036 theo chỉ định hiện tại của Minh. '
        'Phân công lịch sử trong SPEC giữ nguyên. Chưa nghiệm thu hoặc đóng task. '
        'Bản trước sửa được giữ tại runs/sua-r1-001/before/results/T-036/. '
        'Trung gian hiện hành của các bảng dưới đây ở runs/kiem-r1-after-002/; các lượt cũ được dẫn riêng để giữ lịch sử.'
    ) + report[first:]
    report = report.replace('`runs/kiem-005/entity.json#/resource_bindings`',
                            '`runs/kiem-r1-after-002/entity.json#/resource_bindings`')
    report = report.replace('## 3. Các lượt và chi phí thực đo', '## 3. Các lượt và chi phí thực đo trước sửa R1')
    report = report.replace('Lượt cuối 8.754 giây', 'Lượt kiem-005 là 8.754 giây')
    marker = '\n## 4. Kết luận theo câu hỏi nguồn'
    section = f'''
## 3a. Phản biện R1, sửa và kiểm hồi quy

R1 trong chat chỉ ra khóa consume dùng thêm exchange/routing dù chặng nhận chỉ cần broker/scope/queue. Trước sửa, thêm thông tin nguồn phát ở một phía làm mất giao; khóa lưu graph và khóa đối chiếu chưa tách đúng mục đích. Minh duyệt đúng đề xuất sửa; nguyên văn quyền ở runs/sua-r1-001/authorization.txt và LOG Phiên 3. Không suy quyền sửa SPEC, WHY/DECISIONS hoặc nguồn T-035.

fixtures/r1.json và runs/sua-r1-001/oracle-before-fix-002.json giữ oracle trước sửa comparator. kiem-r1-before-001 giữ exception harness mapping_target; harness đã sửa theo mức. kiem-r1-before-002/result.json#/checks giữ {before['passed']} kiểm đạt và {before['failed']} không đạt; các kiểm cũ đều đạt, phần sai nằm ở R1. Đây là lượt tái lập có chủ ý, không bị bỏ.

Comparator nay chỉ dùng trường địa chỉ theo vai trò trong khóa: publish bốn trường, consume ba trường, logical-message năm trường. Graph và members giữ địa chỉ nguyên bản. Khớp consume không xác minh đường routing/binding hoặc một bản tin runtime; nhiều bản ghi cùng chặng nhận được giữ chung một khóa với đủ members. Không đổi builder, mapping, miền hoặc graph T-035.

runs/kiem-r1-after-001/result.json và runs/kiem-r1-after-002/result.json: mỗi lượt {final['passed']} kiểm đạt, {final['failed']} lỗi; gồm 70 kiểm R1. R1 kiểm hai phía khác độ chi tiết ở hai mức/hai view; bảo toàn input/member; gộp chặng nhận với nhiều địa chỉ nguồn phát; queue/scope khác hoặc queue thiếu; exchange publish và routing logical vẫn phân biệt. Danh sách gốc tại #/checks; trung gian tại r1-regression.json#/cases. Lượt sau đọc tương thích {final['compatibility_graph_count']} graph, chiếu {final['trace_projection_pair_count']} cặp; thời gian {final['seconds']:.3f} giây, peak working set {final['peak_working_set_bytes']/1024**2:.1f} MiB. Đây là chi phí checker/fixture, không là thực nghiệm RCA.

runs/sua-r1-001/determinism-and-preservation.json ghi 10 đầu ra giống từng byte giữa hai process khác hash seed, và 7 đầu ra không chịu tác động giống kiem-005. Các graph nguồn, phép chiếu, so unknown, schema compatibility giữ nguyên. Snapshot code từng lượt được giữ; oracle ban đầu không sửa. Theo tự kiểm, R1 đã được sửa trong các trường hợp này; chưa thay phản biện chính thức toàn task.
'''
    assert report.count(marker) == 1
    report = report.replace(marker, '\n' + section + marker, 1)
    tail = report.index('\n## 5. Tự soát cuối và bàn giao')
    report = report[:tail] + '''
## 5. Tự soát cuối và bàn giao

Bản trước và diff lượt sửa tại runs/sua-r1-001/; kiểm cuối tại final-verification.json trong thư mục đó. LOG chỉ nối thêm, STATE chỉ cập nhật dòng T-036; SPEC và nguồn bảo vệ giữ nguyên. Prompt hiện hành là prompt-codex-clean.txt, chép nguyên văn mẫu ngoài thông tin trung tính, dành cho phiên Codex sạch phản biện chính thức toàn bộ task từ nguồn trước khi đọc kết luận lịch sử. Prompt Claude và các lượt cũ được giữ. Không thêm quyết định khoa học, không tự sửa WHY/DECISIONS, không commit/push.
'''
    report_path.write_text(report, encoding='utf-8')

    handoff_path = BASE / 'ban-giao.md'
    handoff = handoff_path.read_text(encoding='utf-8-sig')
    old = 'Codex là người làm; Claude là người phản biện chính thức. Đầu ra chờ phản biện và Minh nghiệm thu. SPEC giữ nguyên.'
    new = ('Codex đã thực hiện lượt sửa theo Minh giao; tự kiểm phần sửa không thay phản biện chính thức. '
           'Phiên Codex sạch tiếp theo phản biện chính thức toàn bộ task theo ngoại lệ Minh chỉ định. '
           'Phân công lịch sử trong SPEC giữ nguyên. Đầu ra chờ phản biện và Minh nghiệm thu.')
    assert handoff.count(old) == 1
    handoff = handoff.replace(old, new, 1)
    handoff = handoff.replace('runs/kiem-005/entity.json', 'runs/kiem-r1-after-002/entity.json')
    marker = '\n## 3. Nơi nhận, bằng chứng thiếu và ảnh hưởng'
    paragraph = ('\nKhóa đối chiếu messaging hiện hành theo vai trò tại hop-dong.md §3; khóa lưu graph nguồn vẫn đủ năm trường. '
                 'Khớp consume là khớp broker/scope/queue, chưa xác nhận exchange/routing, binding hoặc bản tin. '
                 'Địa chỉ nguồn đầy đủ và nhiều thành viên cùng chặng nhận được giữ riêng trong members. '
                 'Bằng chứng sửa/tự kiểm ở runs/kiem-r1-after-002/r1-regression.json và result.json; '
                 'bản trước và lượt lỗi được giữ tại runs/sua-r1-001/ và runs/kiem-r1-before-*/. '
                 'Chưa là nghiệm thu của phiên phản biện sạch.\n')
    assert handoff.count(marker) == 1
    handoff = handoff.replace(marker, paragraph + marker, 1)
    handoff = handoff.replace('Minh chuyển prompt Claude ở cuối LOG T-036 để phản biện kết quả.',
        'Minh chuyển prompt-codex-clean.txt cho phiên Codex mới hoàn toàn để phản biện chính thức toàn bộ T-036 từ nguồn như lần đầu.')
    handoff_path.write_text(handoff, encoding='utf-8')

    state_path = ROOT / 'docs/STATE.md'
    state_before = state_path.read_text(encoding='utf-8-sig')
    lines = state_before.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if line.startswith('| T-036 |')]
    assert len(matches) == 1
    row = lines[matches[0]].split('|')
    row[6] = (' Đã sửa và tự kiểm theo Minh duyệt 15/10/2026; chờ phiên Codex sạch phản biện chính thức '
              'toàn bộ task từ nguồn theo chỉ định hiện tại của Minh. Prompt: results/T-036/prompt-codex-clean.txt; '
              'kết quả và bản trước tại results/T-036/runs/sua-r1-001/. Phân công lịch sử giữ nguyên. '
              'Chưa nghiệm thu, đóng task hoặc chọn P6. ')
    lines[matches[0]] = '|'.join(row)
    state_path.write_text(''.join(lines), encoding='utf-8')
    state_after = state_path.read_text(encoding='utf-8-sig')
    assert [x for x in state_before.splitlines() if not x.startswith('| T-036 |')] == [
        x for x in state_after.splitlines() if not x.startswith('| T-036 |')]

    summary = f'''
**Kết thúc Phiên 3 / kiểm sửa theo Minh duyệt:**
1. Đã sửa khóa đối chiếu theo vai trò, giữ địa chỉ đầy đủ trong nguồn/members; đồng bộ hợp đồng và tự kiểm hồi quy. R1 đạt trong các trường hợp đã kiểm; chưa là phản biện chính thức mới, chưa nghiệm thu toàn task. Không thêm quyết định khoa học.
2. File hiện hành sửa: src/do_thi_tinh/compare.py; results/T-036/check.py, hop-dong.md, kiem-dung-dan.md, ban-giao.md, manifest.json. Thêm fixtures/r1.json, các run mới, thư mục sửa có bản trước/oracle/diff/audit, prompt-codex-clean.txt; LOG chỉ nối và STATE chỉ dòng T-036. Không sửa SPEC/WHY/DECISIONS/T-035/platform hoặc oracle ban đầu. Giữ mọi lượt và thay đổi có sẵn.
3. Kiểm: hai lượt sau sửa đều {final['passed']}/{final['passed']} đạt, 0 lỗi; {final['compatibility_graph_count']} graph và {final['trace_projection_pair_count']} cặp chiếu. 10 trung gian xác định giữa hai process; 7 đầu ra không chịu tác động khớp trước sửa. Trước sửa giữ một exception harness và lượt tái lập {before['failed']} kiểm R1 không đạt. Số/hash ở result.json, r1-regression.json, determinism-and-preservation.json và final-verification.json. Không chạy baseline hoặc trace thô/test.
4. Task có hợp đồng/công cụ và bằng chứng tự kiểm hiện hành; câu nguồn P5/RQ3/RQ5 chưa hoàn tất. Inventory/đối chiếu đầy đủ ba hệ, revision ứng dụng, runtime FT và lợi ích RCA vẫn cần các task đã bàn giao. Khớp consume không xác nhận routing/binding runtime. Minh quyết nghiệm thu sau phản biện toàn task; quyền sửa đã lưu nguyên văn authorization.txt. Không suy đồng thuận thành quyền G3/test.

**Bước tiếp chính xác:** Minh mở phiên Codex mới tại D:/RCA-flashticket và dán results/T-036/prompt-codex-clean.txt. Phiên đó là người phản biện chính thức độc lập theo chỉ định Minh, đọc toàn nguồn/code/đầu ra như lần đầu trước nhận xét lịch sử; chỉ trả lời chat, chưa có quyền ghi REVIEW. Không tự tạo/gửi phiên. Nội dung báo cáo cần giữ: phân biệt khóa lưu thông tin với khóa đo chặng theo vai trò và giới hạn của khớp consume.

**Lệnh kiểm hành vi cuối:** PYTHONHASHSEED=1 với D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B results/T-036/check.py kiem-r1-after-002; đã chạy qua subprocess đặt biến cho process con. **Lệnh cuối của bước bàn giao:** py -3 -X utf8 -B results/T-036/runs/sua-r1-001/finalize-r1.py. Script có guard không ghi đè audit đã có; đọc audit và manifest trước tiếp tục, không chạy lại run cũ.

**Đề xuất commit, chưa thực hiện:** fix: compare messaging addresses by role in T-036. Chỉ commit/push khi Minh yêu cầu hoặc duyệt.

### Prompt Codex sạch — phản biện chính thức toàn bộ T-036 (Minh chuyển thủ công)

```text
{prompt.rstrip()}
```
'''
    with (TASK / 'LOG.md').open('a', encoding='utf-8') as stream:
        stream.write('\n' + summary)
    log_before = (OUT / 'before/tasks/T-036-p5b-hop-dong-chung/LOG.md').read_bytes()
    assert (TASK / 'LOG.md').read_bytes().startswith(log_before)

    diff_paths = ['src/do_thi_tinh/compare.py', 'results/T-036/check.py', 'results/T-036/hop-dong.md',
                  'results/T-036/kiem-dung-dan.md', 'results/T-036/ban-giao.md',
                  'docs/STATE.md', 'tasks/T-036-p5b-hop-dong-chung/LOG.md',
                  'results/T-036/fixtures/r1.json', 'results/T-036/prompt-codex-clean.txt']
    diff = []
    for name in diff_paths:
        old_path = OUT / 'before' / name
        old_text = old_path.read_text(encoding='utf-8-sig') if old_path.exists() else ''
        new_text = (ROOT / name).read_text(encoding='utf-8-sig')
        diff.extend(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                    fromfile=name if old_path.exists() else '/dev/null', tofile=name))
    with (OUT / 'changes.diff').open('x', encoding='utf-8') as stream:
        stream.writelines(diff)
    assert all(sha(ROOT / r['path']) == pre['protected_hashes'][r['path']] for r in protected)
    assert all(sha(ROOT / r['path']) == pre['historical_artifact_hashes'][r['path']] for r in history)
    status_now = subprocess.check_output(['git', 'status', '--porcelain=v1', '--untracked-files=all'],
                                         cwd=ROOT, text=True, encoding='utf-8')
    assert outside_status(status_now) == outside_status(pre['git_status_before'])
    assert subprocess.check_output(['git', 'diff', '--binary', '--', '.', ':(exclude)docs/STATE.md'], cwd=ROOT) == outside_diff
    save(OUT / 'final-verification.json', dict(
        task='T-036', authorization='authorization.txt', current_run='runs/kiem-r1-after-002',
        current_checks=final['passed'], failed_checks=final['failed'], r1_checks=70,
        before_fix_failed_checks=before['failed'], protected=protected, historical_artifacts=history,
        sources=source_checks, dependency_manifests_unchanged=True, state_only_task_row=True,
        log_append_only=True, log_sha256=sha(TASK / 'LOG.md'), state_sha256=sha(state_path),
        outside_git_status_unchanged=True, outside_tracked_diff_unchanged=True,
        changed_current_files=diff_paths, current_determinism_and_prior_output_preservation=True,
        original_fixture_oracle_unchanged=True, prompt_template_exact=True,
        official_clean_full_review_pending=True, commit_push=False, test_opened=False))
    files = [ROOT / 'src/do_thi_tinh' / p for p in ['__init__.py', 'build.py', 'compare.py', 'README.md']]
    files += sorted(p for p in BASE.rglob('*') if p.is_file() and p != BASE / 'manifest.json')
    rows = [dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size, sha256=sha(p)) for p in files]
    manifest = dict(previous, created_utc=datetime.now(timezone.utc).isoformat(),
                    files=rows, count=len(rows), total_bytes=sum(r['bytes'] for r in rows),
                    final_verification='runs/sua-r1-001/final-verification.json',
                    previous_manifest='runs/sua-r1-001/before/results/T-036/manifest.json',
                    previous_manifest_sha256=pre['manifest_before'],
                    current_run='runs/kiem-r1-after-002', current_prompt='prompt-codex-clean.txt',
                    state='awaiting_official_clean_full_review_and_Minh_acceptance')
    (BASE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    assert all(sha(ROOT / row['path']) == row['sha256'] for row in rows)
    print(json.dumps(dict(artifacts=len(rows), passed=final['passed'], failed=final['failed'],
                          official_clean_full_review_pending=True), ensure_ascii=False))


if __name__ == '__main__':
    main()
