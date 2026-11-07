"""Chốt hồ sơ T-052; --verify chỉ đọc manifest và kiểm hash/phạm vi."""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

from common import ROOT, RUN, digest, read, save
from m1_danh_gia import pha2

LOG = ROOT / 'tasks/T-052-t13-va-ho-so-g3/LOG.md'
STATE = ROOT / 'docs/STATE.md'
MANIFEST = ROOT / 'results/T-052/manifest-thuc-thi-001.json'
BEFORE = read(RUN / 'truoc-khi-chay.json')


def guard(final=False):
    checked = []
    for name, expected in BEFORE['files'].items():
        raw = (ROOT / name).read_bytes()
        if name == 'docs/STATE.md' and final:
            old = (RUN / 'STATE-truoc-chot.md').read_bytes()
            assert hashlib.sha256(old).hexdigest() == expected['sha256']
            a, b = old.splitlines(keepends=True), raw.splitlines(keepends=True)
            assert len(a) == len(b)
            changed = [(x, y) for x, y in zip(a, b) if x != y]
            assert len(changed) == 1 and all(b'**T-052' in x for x in changed[0])
            checked.append({'path': name, 'PASS': True, 'only_T052_row': True})
            continue
        if name.endswith('/LOG.md'):
            raw = raw[:expected['bytes']]
        assert len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'], name
        checked.append({'path': name, 'PASS': True, 'append_only_prefix': name.endswith('/LOG.md')})
    return checked


def validate_science():
    data = pha2.giai_ma_json(read('results/T-052/ket-qua-dev.json'))
    extra = read('results/T-052/do-do-bo-sung.json')
    for world, datasets in data['worlds'].items():
        for ds, n in [('RE2-TT', 30), ('Nezha-OB', 22)]:
            table = datasets[ds]
            assert len(table['summary']) == (18 if world == 'P' else 13)
            assert set(table['summary']) == set(table['per_case'])
            for name, rows in table['per_case'].items():
                assert len(rows) == n == table['summary'][name]['n']
                assert sum(table['summary'][name]['status'].values()) == n
                assert abs(float(table['summary'][name]['MRR']) - sum(float(r['RR']) for r in rows.values()) / n) < 1e-14
                metrics = extra['expected_ties'][world][ds][name]['metrics']
                for k in (5, 10):
                    den = sum(r[f'hit@{k}'] for r in rows.values())
                    assert abs(metrics[f'retrieval@{k}'] - den / n) < 1e-14
                    if den == 0:
                        assert metrics[f'rerank@1(K={k})'] is None
                    else:
                        assert abs(metrics[f'rerank@1(K={k})'] - sum(r['hit@1'] for r in rows.values()) / den) < 1e-14
    assert len(data['controls_graph_parity']) == 52
    assert read(RUN / 'prepared-seal.json')['labels_read'] is False
    assert read(RUN / 'prepared-seal.json')['KB_compact_comparisons'] == 328
    ec2 = read(RUN / 'ec2-pilot-002/received/output/summary.json')
    assert ec2['PASS'] and ec2['native_comparisons'] == 15
    assert all(not r['mismatches'] for r in ec2['comparisons'])
    fixture_counts = {}
    for name in ('fixture-a4-001.json', 'fixture-p7-001.json', 'fixture-cd3-001.json',
                 'fixture-cd3-malformed-001.json', 'baseline-local-001/summary.json',
                 'ob-local-002/summary.json', 'torai-entrypoint-001/summary.json'):
        d = read(RUN / name)
        assert d['PASS'], name
        fixture_counts[name] = len(d['checks']) if 'checks' in d else True
    assert read(RUN / 'fixture-p7-001.json')['raw_test_opened'] is False
    return {'PASS': True, 'worlds': ['P', 'S_lo', 'S_hi'], 'P_methods': 18,
            'S_methods': 13, 'real_cases': 52, 'native_windows': 82,
            'prepared_records': 492, 'graph_controls': 52, 'fixtures': fixture_counts}


def source_checks():
    m = read('results/T-052/manifest.json')
    rows = []
    for key in ('upstream_inputs_verified', 'upstream_manifest_snapshots', 'historical_G1_sources_git_pinned'):
        for record in m[key]:
            p = ROOT / record['path']
            assert p.stat().st_size == record['bytes'] and digest(p) == record['sha256'], record['path']
            rows.append({'path': record['path'], 'sha256': record['sha256'], 'group': key, 'PASS': True})
    return rows


def budget():
    paths = ['ec2-pilot-002/received/output/summary.json', 'ec2-pilot-002/launch.json',
             'ec2-pilot-001/receive-summary.json', 'ec2-pilot-002/receive-summary.json',
             'prepared-seal.json', 'bang-doc-lap-summary.json', 'vung-ce-summary.json',
             'baseline-local-001/summary.json', 'ob-local-002/summary.json',
             'torai-entrypoint-001/summary.json', 'score-all-summary.json',
             'fixture-a4-001.json', 'fixture-p7-001.json', 'fixture-cd3-001.json',
             'do-do-bo-sung-summary.json']
    timers = [{'path': str((RUN / p).relative_to(ROOT).as_posix()),
               'seconds': read(RUN / p)['elapsed_seconds']} for p in paths]
    bounds = []
    for name in ('pilot-001', 'pilot-002', 'pilot-003', 'ec2-pilot-001', 'ob-local-001'):
        files = [p for p in (RUN / name).rglob('*') if p.is_file()]
        lo, hi = min(p.stat().st_mtime for p in files), max(p.stat().st_mtime for p in files)
        bounds.append({'directory': name, 'seconds_upper': hi - lo,
                       'lo_utc': datetime.fromtimestamp(lo, timezone.utc).isoformat(),
                       'hi_utc': datetime.fromtimestamp(hi, timezone.utc).isoformat(),
                       'kind': 'filesystem_interval_including_idle_not_exact_CPU_or_runtime'})
    total = sum(x['seconds'] for x in timers) + sum(x['seconds_upper'] for x in bounds)
    assert total < 3600
    return {'limit_seconds': 3600, 'measured_stage_wall_seconds': timers,
            'failed_phase_upper_intervals': bounds, 'conservative_sum_seconds': total,
            'PASS_within_initial_experiment_budget': True,
            'accounting': 'Cộng thời gian tầng trên không cộng lần nữa từng phương pháp con. Khoảng lỗi từ mốc file bao gồm chờ/viết công cụ; EC2-001 còn bao phủ phần lượt002 nên tổng cố ý đếm dư. Không giả số đo chính xác cho lượt lỗi. Đọc nguồn, viết công cụ/hồ sơ và kiểm hồ sơ tách khỏi ngân sách chạy pilot/chấm dev. Không có lệnh thực nghiệm mới nào dài hơn một giờ.'}


def prompt():
    template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8')

    def block(header):
        return re.search(r'```text\n(.*?)\n```', template.split(header, 1)[1], re.S).group(1)

    common = block('## Prompt chung')
    values = [
        'T-052, tasks/T-052-t13-va-ho-so-g3/SPEC.md',
        'soát kết quả', 'P6/P7, G3(a)', 'Codex người làm, Claude người phản biện',
        'AGENTS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/KE-HOACH-SAU-T047.md; tasks/T-052-t13-va-ho-so-g3/SPEC.md',
        'tasks/T-052-t13-va-ho-so-g3/LOG.md theo thứ tự thời gian; results/T-052/manifest.json phần review_received; chưa có file REVIEW của task',
        'src/m1/; src/m1_danh_gia/; src/p3/; results/T-052/manifest-thuc-thi-001.json; results/T-052/scripts/; results/T-052/runs/; kết quả và nguồn được dẫn trong manifest; lệnh kiểm chỉ đọc: python -B -S results/T-052/scripts/finalize.py --verify theo môi trường ghi trong LOG',
        'chỉ đọc và trả lời trong chat; chỉ ghi bản phản biện khi Minh cấp rõ đường dẫn cho lượt này',
    ]
    slots = list(re.finditer(r'<[^>]+>', common))
    assert len(slots) == len(values)
    for slot, value in reversed(list(zip(slots, values))):
        common = common[:slot.start()] + value + common[slot.end():]
    return '\n\n'.join([common, block('### Soát kết quả'), block('### G3 — Khóa thiết kế trước khi mở test')])


def build():
    assert not MANIFEST.exists(), 'Không ghi đè manifest đã chốt'
    protected = guard()
    sources = source_checks()
    for p in (ROOT / 'results/T-052/scripts').glob('*.py'):
        compile(p.read_text(encoding='utf-8'), str(p), 'exec')
    parsed = 0
    for p in (ROOT / 'results/T-052').rglob('*.json'):
        read(p)
        parsed += 1
    scientific = validate_science()
    costs = budget()
    save(RUN / 'machine-budget.json', costs)
    for path, code_key in [('results/T-052/ma-tran-va-nguon.json', 'code'),
                           ('results/T-052/giao-thuc-p7-a.json', 'source_code')]:
        p = ROOT / path
        d = read(p)
        for src in (ROOT / 'results/T-052/scripts').glob('*.py'):
            d[code_key][src.relative_to(ROOT).as_posix()] = digest(src)
        d['metric_supplement'] = 'results/T-052/do-do-bo-sung.json'
        p.write_text(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n', encoding='utf-8')
    old_state = STATE.read_bytes()
    (RUN / 'STATE-truoc-chot.md').write_bytes(old_state)
    lines = old_state.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if b'**T-052' in line]
    assert len(matches) == 1
    i = matches[0]
    new_row = '- **T-052 — T13 dev và hồ sơ G3(a): người làm hoàn tất phần dev, chờ phản biện/Minh nghiệm thu 04/11/2026.** Codex làm, Claude phản biện. Pilot EC2/local và chấm dev đã xong theo quyền có điều kiện Minh cấp; [kết quả](../results/T-052/bao-cao-t13.md), [manifest thực thi](../results/T-052/manifest-thuc-thi-001.json), [LOG và prompt](../tasks/T-052-t13-va-ho-so-g3/LOG.md). G3 chưa khóa; P7/test/RE3, ngân sách toàn đợt và commit/push chưa được duyệt.'
    ending = b'\r\n' if lines[i].endswith(b'\r\n') else b'\n'
    old_row = lines[i].decode('utf-8').rstrip('\r\n')
    lines[i] = new_row.encode('utf-8') + ending
    STATE.write_bytes(b''.join(lines))
    handoff = prompt()
    text = '''
### Kết thúc Phiên 5 — tự soát, triển khai T13 dev và hồ sơ G3(a)

1. **Đã làm:** tự soát từ nguồn, đối chiếu SPEC rồi kết quả/phản biện cũ; không phải lượt mù vì đã thấy SPEC/LOG ở lượt trước. Giữ nền/câu hỏi nguồn, không sửa nhỏ SPEC. Sau quyền có điều kiện của Minh, đã triển khai pilot native EC2 15/15; TT local sáu baseline; OB local M1/T12/sáu tuyến; TORAI worker mới so raw với tuyến cũ; seal 492 bản ghi từ 82 cửa sổ và kiểm 328 compact KB; chấm đủ T13 dev, 52 graph-control, nhóm/ca, vùng/C-e. Không chạy native toàn ma trận.
2. **File:** thêm scripts/runs và kết quả/hồ sơ trong results/T-052/, nối LOG này, đổi đúng một dòng T-052 STATE. Hai file src và các sổ có thay đổi từ trước phiên được giữ nguyên theo dấu vân tay lúc nhận việc. Không sửa SPEC/src, không ghi DECISIONS/WHY, không mở locked/RE3, không commit/push/cấp máy/đổi ACL khóa.
3. **Kiểm:** hash 29 đầu vào, 13 manifest upstream, 5 nguồn G1 và lineage 003; input/sample/native parity; chấm lại 372 bản ghi baseline; 16 fixture A4, 21 kiểm điểm vào P7 dữ liệu giả; C-d3 thật/error/timeout/JSON hỏng giữ seal chính. Bổ sung Retrieval/Rerank theo evaluator và bảng native RCAEval baseline tách kỳ vọng hòa. Cột Rerank mẫu số0 ghi null. Đã kiểm JSON, compile công cụ, số/mẫu số/trạng thái và dấu vân tay protected. Biên nhận kiểm và thời gian: runs/trien-khai-001/{final-checks,machine-budget}.json; manifest-thuc-thi-001.json ghim file cuối.
4. **Kết luận/phần mở:** T13 đạt mô tả dev và hồ sơ để Minh xem, không nghiệm thu thay Minh hoặc khóa G3. M1−C-a0 âm TT/dương OB; C-d2 hơn M1 OB, không xác nhận lợi ích đồ thị chung. Chuỗi E2/E5 có bằng chứng tính toán và phản ví dụ, không chứng minh lỗi vật lý hoặc cơ chế chung. E5 thiếu matched control đầy đủ; VC×E5, chiều PageRank đảo, log–span, revision snapshot và nền lành độc lập giữ OPEN. RQ3a/(b), nhãn vùng/P10, LLM/P8 và FlashTicket/P9/P10 chưa được task này trả lời. Quyết định nền hiện hành không đổi. Minh còn quyết phản biện/nghiệm thu, khóa G3, ma trận/worker/timeout/tổng ngân sách và private map trong SPEC P7, quyền dữ liệu; RE3 cần hợp đồng nguồn/U/adapter/schema và quyền riêng trước một lượt mở cuối. Không chạy thêm để tự đóng các câu này.

**Lỗi và cách xử lý:** giữ local001 lỗi gộp params, local002 lưu set, local003 lệch số thực cực nhỏ; không nới comparator, chuyển sang nguồn EC2 cùng nền số và đạt exact. EC2-001 thiếu module observer, SSH điều khiển hết giờ; kiểm worker qua kết nối mới trước nhận, giữ lỗi. EC2-002 thêm đúng phụ thuộc và launch tách PID/timeout, PASS. Một lỗi bookkeeping khi thêm vế chấm giữ script cũ/failure rồi sửa wrapper. OB-local001 thiếu thư mục log, giữ record/failure; hash snapshot bổ sung sau đọc được ghi rõ hậu kiểm. OB-local002 kiểm trước, lưu timing từng bước, PASS. Không gọi lỗi công cụ là lỗi khoa học của phương pháp. Mỗi lỗi thuộc wrapper khác nhau; không thử cùng một lỗi quá ba lần.

**Chi phí:** machine-budget.json ghi tầng đo thời gian và cận trên riêng cho pha hỏng, gồm khoảng chờ nên cố ý đếm dư, vẫn dưới 60 phút ngân sách thực nghiệm. Không thay mốc chưa ghi bằng số thời gian chính xác giả. Chi phí đọc nguồn/làm công cụ/viết hồ sơ tách riêng. Pilot local là lát cắt, không là trần thời gian toàn test.

**Đầu ra chính:** bao-cao-t13.md (tự đánh giá, đối chiếu, thực thi, cơ chế, kết quả, giới hạn, chi phí, phần mở); ho-so-g3.md; ket-qua-dev.json; do-do-bo-sung.json; vung-ce-va-vi-tri-001.json; ma-tran-va-nguon.json; ke-hoach-tap-test.json; giao-thuc-p7-a.json. Bản độc lập trước C-a parity giữ nhãn PARTIAL lịch sử, không là kết quả hiện hành. Giao thức là ứng viên để Minh khóa, không phải giấy phép mở test.

**Nội dung cần ghi sổ sau khi Minh duyệt:** quyền tự soát/triển khai có điều kiện và quyền dùng EC2 hiện có do Minh cấp. Đề xuất dòng ghi ở ho-so-g3.md, chưa tự ghi ngoài phạm vi. Không thay quyết định phương pháp.

**Bước kế tiếp chính xác:** dùng môi trường Python ở lệnh dưới kiểm manifest chỉ đọc; đọc bao-cao-t13.md, ho-so-g3.md và giao-thuc-p7-a.json. Minh có thể copy prompt bên dưới cho Claude; không tự gửi, không chờ Claude để làm phần đã được giao. Khi Minh duyệt G3/quyền chạy, mới trình SPEC P7 đầy đủ ma trận và trần, không dùng task này tự mở test. Do ngữ cảnh đã nén, công việc mới nên mở phiên mới theo AGENTS 5a.2, không chạy lại đầu ra hợp lệ.

Lệnh chốt phiên đang chạy: `& 'C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B -S results/T-052/scripts/finalize.py`.
Lệnh kiểm cuối phải chạy ngay sau chốt (chỉ đọc): `& 'C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B -S results/T-052/scripts/finalize.py --verify`.
Commit đề xuất, chưa thực hiện: `feat(T-052): hoàn tất T13 dev và hồ sơ chuẩn bị G3(a)`.

### Prompt bàn giao Claude — soát kết quả/G3

```text
''' + handoff + '\n```\n'
    with LOG.open('ab') as f:
        f.write(text.replace('\n', '\r\n').encode('utf-8'))
    scope = guard(final=True)
    diff = subprocess.run(['git', '--no-optional-locks', 'diff', '--check'], cwd=ROOT,
                          capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    tracked = subprocess.check_output(['git', '--no-optional-locks', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines()
    assert set(tracked) == set(BEFORE['tracked_diff_before']), tracked
    assert handoff in LOG.read_text(encoding='utf-8')
    save(RUN / 'state-row-change.json', {'before': old_row, 'after': new_row, 'PASS': True})
    save(RUN / 'final-checks.json', {'PASS': True, 'created_utc': datetime.now(timezone.utc).isoformat(),
         'protected': scope, 'upstream': sources, 'scientific': scientific,
         'json_files_parsed_before_closeout': parsed, 'git_diff_check': 'PASS',
         'tracked_diff_preserved': tracked, 'prompt_verbatim_blocks_with_neutral_slots': True,
         'new_source_decisions': [], 'SPEC_changed': False,
         'mutation_scope': ['results/T-052/', 'tasks/T-052-t13-va-ho-so-g3/LOG.md append only', 'docs/STATE.md T-052 row only']})
    files = [p for p in (ROOT / 'results/T-052').rglob('*') if p.is_file() and p != MANIFEST]
    files += [LOG, STATE]
    save(MANIFEST, {'schema': 'T052-execution-001', 'created_utc': datetime.now(timezone.utc).isoformat(),
         'status': 'WORKER_DEV_HANDOFF_NOT_MINH_ACCEPTANCE_NOT_G3',
         'base_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
         'authority': 'tasks/T-052-t13-va-ho-so-g3/LOG.md Phiên 5, nguyên văn quyền có điều kiện và IP EC2 do Minh cấp',
         'before': {'path': 'results/T-052/runs/trien-khai-001/truoc-khi-chay.json', 'sha256': digest(RUN / 'truoc-khi-chay.json')},
         'previous_manifest': {'path': 'results/T-052/manifest.json', 'sha256': digest(ROOT / 'results/T-052/manifest.json')},
         'outputs': {p.relative_to(ROOT).as_posix(): {'bytes': p.stat().st_size, 'sha256': digest(p)} for p in sorted(files)},
         'checks': 'results/T-052/runs/trien-khai-001/final-checks.json',
         'budget': costs, 'files_changed_in_session': ['results/T-052/scripts/', 'results/T-052/runs/',
            'results/T-052/{ket-qua-dev*,do-do-bo-sung,vung-ce-va-vi-tri-001,ma-tran-va-nguon,ke-hoach-tap-test,giao-thuc-p7-a}.json',
            'results/T-052/bao-cao-t13.md', 'results/T-052/ho-so-g3.md',
            'tasks/T-052-t13-va-ho-so-g3/LOG.md append only', 'docs/STATE.md T-052 row only'],
         'self_hash_policy': 'Manifest không băm chính nó. --verify kiểm mọi output và guard. Không sửa manifest nguồn/lượt hỏng.',
         'not_authorized': ['G3 lock', 'test/RE3 data opening', 'new EC2 instance', 'P7 full run', 'src changes', 'commit/push']})
    print(json.dumps({'PASS': True, 'manifest_outputs': len(files),
                      'budget_conservative_seconds': costs['conservative_sum_seconds']}))


def verify():
    m = read(MANIFEST)
    for name, row in m['outputs'].items():
        p = ROOT / name
        assert p.stat().st_size == row['bytes'] and digest(p) == row['sha256'], name
    guard(final=True)
    source_checks()
    validate_science()
    assert prompt() in LOG.read_text(encoding='utf-8')
    for path, field in [('results/T-052/ma-tran-va-nguon.json', 'code'),
                        ('results/T-052/giao-thuc-p7-a.json', 'source_code')]:
        for name, value in read(path)[field].items():
            assert digest(ROOT / name) == value, name
    result = subprocess.run(['git', '--no-optional-locks', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    print(json.dumps({'PASS': True, 'outputs_hash_bytes_checked': len(m['outputs']),
                      'SPEC_src_original_LOG_prefix_protected': True, 'STATE_one_T052_row': True,
                      'pilot_and_dev_complete': True, 'P7_test_run': False, 'git_diff_check': 'PASS'}))


if __name__ == '__main__':
    verify() if '--verify' in sys.argv else build()
