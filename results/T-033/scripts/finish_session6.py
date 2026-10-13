"""Technical checkpoint only: local metadata/hash/docs; no EC2 or research work."""
import json, pathlib, difflib, datetime
from session6_control import ROOT, OPEN, sha, write, stamp
from session6_launch import ledger

C = ROOT / 'results/T-033/runs/session6-compute-checkpoint-001'
LOG = ROOT / 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'
STATE = ROOT / 'docs/STATE.md'
RUNS = ['nsigma-delay-pilot-001', 'nsigma-delay-rest-001',
        'bocpd-delay-pilot-001', 'bocpd-delay-rest-001',
        'channel-pilot-001', 'channel-rest-001']
PY = 'C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
COMMAND = PY + ' -B -X utf8 results/T-033/scripts/finish_session6.py'

def rel(p):
    return p.relative_to(ROOT).as_posix()

def entry(p):
    return {'sha256': sha(p), 'bytes': p.stat().st_size}

def new_text(name, text):
    p = C / name
    assert not p.exists(), 'Refuse overwriting checkpoint'
    p.write_text(text, encoding='utf-8')

def main():
    assert not (C / 'checkpoint.json').exists(), 'Checkpoint already closed'
    inv = json.loads((C / 'artifact-inventory.json').read_text())
    assert inv['status'] == 'PASS' and not inv['worker_candidates']
    for name, expected in inv['files'].items():
        assert entry(C / 'artifacts' / name) == expected, name
    received = json.loads((C / 'receive-verification.json').read_text())
    assert received['status'] == 'PASS' and received['files'] == len(inv['files'])
    baseline = json.loads((OPEN / 'baseline.json').read_text())
    protected = {}
    for name, expected in baseline.items():
        if name not in [rel(LOG), rel(STATE)]:
            assert entry(ROOT / name) == expected, name
            protected[name] = expected
    old_log = (OPEN / 'before' / rel(LOG)).read_bytes()
    assert LOG.read_bytes().startswith(old_log)
    old_state = (OPEN / 'before' / rel(STATE)).read_bytes()
    assert STATE.read_bytes() == old_state, 'Unexpected concurrent STATE change'
    for p in (OPEN / 'scripts').iterdir():
        assert p.read_bytes() == (ROOT / 'results/T-033/scripts' / p.name).read_bytes()
    approval = json.loads((ROOT / 'results/T-033/runs/session5-approval-checkpoint-001/approved-accounting.json').read_text())
    assert sha(ROOT / approval['historical_ledger']) == approval['historical_ledger_sha256']
    final = json.loads((OPEN / 'final-preflight-001.stdout').read_text())
    assert final['status'] == 'PASS' and not final['worker_candidates'] and not final['archive_exists']
    observations = {}
    run_records = []
    for name in RUNS:
        obs = json.loads((OPEN / (name + '.observation.json')).read_text())
        assert obs['control']['status'] == 'PASS' and obs['validation']['status'] == 'PASS'
        assert obs['control']['child_exit_code'] == 0 and obs['control']['source_hash_after']
        observations[name] = obs
        timer = json.loads((OPEN / (name + '.processing-timer.json')).read_text())
        assert timer['exit_code'] == 0
        control = obs['control']
        run_records.append({'run': name, 'status': 'PASS',
            'observation': rel(OPEN / (name + '.observation.json')),
            'processing_timer': rel(OPEN / (name + '.processing-timer.json')),
            'whole_job_processing_s': (timer['end_ns'] - timer['start_ns']) / 1e9,
            'max_sampled_child_tree_rss_bytes': control['max_tree_rss_bytes'],
            'supervisor_peak_rss_bytes': control['rss_peak_bytes'],
            'min_ram_available_bytes': control['min_ram_available_bytes'],
            'output_bytes': control['output_bytes']})
    groups_path = C / 'artifacts/runs/session6-groups-001/bao-phu-nhom.json'
    groups = json.loads(groups_path.read_text())
    group_check = json.loads((groups_path.parent / 'verification.json').read_text())
    assert group_check['status'] == 'PASS' and group_check['full_30_factorial_and_context']
    lp = ledger('session6-final-budget-001')
    account = json.loads(lp.read_text())
    write(C / 'final-ledger.json', account)
    write(C / 'coverage-resources.json', {'status': 'PASS', 'runs': run_records,
        'coverage': {'nsigma_case_columnset_units': 60, 'bocpd_cases': 30, 'channel_cases': 30},
        'coverage_basis': [rel(OPEN / (n + '.observation.json')) + '#/validation' for n in RUNS],
        'new_groups': len(groups['new_groups']), 'groups': rel(groups_path),
        'group_denominators': group_check['separate_denominators'],
        'manual_reading': 'OPEN', 'point_control_selection_and_coverage_assessment': 'OPEN',
        'mechanism_and_RQ2_G2': 'OPEN', 'received': received,
        'final_ec2_status_source': rel(OPEN / 'final-preflight-001.stdout'),
        'final_ec2_timing_source': rel(OPEN / 'final-preflight-001.timer.json')})
    checkpoint = {'at': stamp(), 'task': 'T-033', 'worker': 'Codex', 'reviewer': 'Claude',
        'reason': 'CONTEXT_COMPRESSED_AGENTS_5A_2',
        'status': 'COMPUTATION_PHASE_VERIFIED_MANUAL_SYNTHESIS_OPEN',
        'computation_phase_complete': True, 'task_complete': False,
        'new_formal_decisions': [], 'accounting': rel(lp),
        'charged_new_processing_s': account['new_processing_charged_s'],
        'remaining_approved_new_processing_s': account['remaining_approved_s'],
        'historical_actual_processing_status': 'OPEN',
        'accounting_note': '28800s prior administrative reserve is unchecked, not actual historical measurement. New charges include conservative full SSH bounds and complete autonomous job times; overlapping control charges are not subtracted.',
        'old_artifact_locator': 'results/T-033/runs/checkpoint-handoff-001/artifact-locator.json',
        'new_artifact_inventory': rel(C / 'artifact-inventory.json'),
        'new_artifact_root': rel(C / 'artifacts'), 'group_lock': rel(groups_path),
        'ec2': {'worker_candidates': [], 'observed_during': json.loads((OPEN / 'final-preflight-001.timer.json').read_text())['ended'],
                'status_source': rel(OPEN / 'final-preflight-001.stdout'),
                'logical_bytes': final['logical_bytes'], 'disk_free_bytes': final['disk_free_bytes'],
                'ram_available_bytes': final['ram_available_bytes'], 'archive_exists': False,
                'laptop_may_close': True, 'active_run': None},
        'open': [
            {'part': 'Manual representative/control chains and point controls', 'owner': 'Codex next session',
             'needed': 'Read all required locked groups against saved code/intermediates; lock point selection before interpretation; record matching and missing coverage.'},
            {'part': 'Mechanism versus competing explanations; RQ2/P4/DT18 NV2/NV3 and G2', 'owner': 'Codex / Minh',
             'needed': 'Manual evidence and source-aligned synthesis; any missing intermediate or discriminating intervention needs a precise proposal and authorization.'},
            {'part': 'Historical actual processing time', 'owner': 'Minh / original evidence',
             'needed': 'Historical full process/SSH timing; Q-132 resolves administration only.'}],
        'next': 'Read README and prompt-next-session.md; verify manifests and evidence; continue manual reading/synthesis in a new session. Reuse PASS units by source hash.',
        'last_checkpoint_command': COMMAND,
        'last_ec2_command': {'controller': 'results/T-033/scripts/session6_control.py remote --name final-preflight-001 --code results/T-033/scripts/session6_preflight.py',
            'payload': 'results/T-033/scripts/session6_preflight.py',
            'timer': rel(OPEN / 'final-preflight-001.timer.json')}}
    write(C / 'checkpoint.json', checkpoint)
    new_text('README.md', f'''# T-033 — Checkpoint sau chặng tính, phiên 6

Ngữ cảnh bị nén; dừng nghiên cứu và chuyển phiên theo AGENTS §5a.2. Codex làm, Claude phản biện. Chặng tính đã tự kiểm đạt; task, đọc tay, tổng hợp và RQ2/G2 còn OPEN. Đây là bàn giao kỹ thuật, không là báo cáo cơ chế.

## Kết quả và nơi đọc

- Sáu run pilot/rest PASS: N-Sigma 60 đơn vị ca × bộ cột; BOCPD 30 ca; kênh 30 ca. Chi tiết cùng time/RAM/byte ở coverage-resources.json và ../session6-open-001/*.observation.json. Pilot được kiểm đạt trước rest; đơn vị PASS không khởi lại.
- 299 file mới, {received['bytes']} byte: artifact-inventory.json chỉ đường trong artifacts/. Hash hai đầu PASS, stream trực tiếp; không tạo archive EC2 hoặc xóa thêm.
- Nguồn và trung gian cũ: ../checkpoint-handoff-001/artifact-locator.json, artifact-inventory.json, artifacts/. Tự kiểm đầu phiên 825 file cũ và native/raw có bằng chứng ../session6-open-001/fresh-laptop-integrity.json, fresh-preflight-002.stdout; kiểm EC2 cuối ở final-preflight-001.stdout. Không thay native, tham số hoặc tiêu chí.
- Khóa nhóm mới: artifacts/runs/session6-groups-001/bao-phu-nhom.json; bản nhóm gốc được giữ trong đó và file gốc không đổi. Nhóm/ca đã khóa trước diễn giải; chọn điểm đối chứng và đánh giá điều kiện ghép/coverage cần làm trước đọc tay. Mẫu số từng loại ở verification.json; input trùng là quan hệ theo cặp, không cộng cờ chồng lấn thành nguyên nhân. Không kênh/lỗi/contrast không định nghĩa giữ riêng.
- Script staged session6-001 giữ nguyên. Prep đã làm đổi line ending của core; phát hiện trước pilot. session6-002 dùng core bytes chính xác bản cũ; stage002-verification.json và unchanged-computation-ast.json xác minh. Giữ các diff/payload. Bộ lọc worker đã sửa đúng thư mục và quan sát lặp dùng tên mới trước khi có poll lặp; không có bằng chứng bị ghi đè hoặc worker trùng.

## Hạch toán và EC2

Q-132: 28800 giây cũ là dự phòng chưa kiểm, thời gian thực tế cũ OPEN. Trần xử lý mới 14400 giây. Snapshot cuối: ../session6-final-budget-001/ledger.json, bản sao final-ledger.json. Đã cộng {account['new_processing_charged_s']:.12f} giây mới; còn {account['remaining_approved_s']:.12f} giây. Tất cả lệnh kiểm/lượt hỏng/truyền và toàn bộ job shell được đo; bounds SSH gồm cả mạng/IO, overlap điều khiển tính riêng theo hướng bảo thủ. Không coi số này là thời gian CPU nghiên cứu, không lấy subtotal status hay lịch để cấp giờ. Không sửa ledger lịch sử.

Kiểm EC2 cuối {checkpoint['ec2']['observed_during']}: không worker T-033/tmux, archive không tồn tại, byte/RAM/disk ghi trong checkpoint.json cùng bằng chứng. Laptop có thể đóng; không có run đang chờ xong. Agent không bật/tắt EC2. Trạng thái này có mốc kiểm, không thay kiểm mới nếu phiên sau cần dùng EC2.

Mọi xử lý EC2 tiếp theo, kể cả đọc kiểm/hash, phải đo và cộng từ snapshot cuối trước run tiếp. SSH: ubuntu@3.107.246.249, key D:/RCA-ext/keys/keys.pem; known_hosts results/T-033/runs/prepare-001/known_hosts, StrictHostKeyChecking=yes, BatchMode=yes. Python pin /home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8; native/env/T-025 chỉ đọc. Lệnh xem nếu cần: `tail -n 20 ~/rca/T-033/trang-thai.txt`; thời gian toàn SSH vẫn phải ghi ledger.

## Bước tiếp

Minh mở phiên mới bằng prompt-next-session.md. Đọc AGENTS, STATE, toàn SPEC và LOG cuối; trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, LESSONS, WHY-41. Kiểm manifest checkpoint và inventory trước dùng đầu ra. Tiếp đọc tay có đối chứng, rồi tổng hợp đủ nguồn/SPEC. Những câu chưa phân xử giữ OPEN, trình đúng bằng chứng thiếu/phạm vi/chi phí; không tự đổi thiết kế hoặc chạy vượt quyền. Chưa soạn prompt phản biện Claude vì task chưa hoàn tất.

Manifest.json pin các file mới và bằng chứng phiên 6; scope-verification.json kiểm LOG chỉ nối, STATE duy nhất T-033, nguồn/ledger/script gốc giữ nguyên. approved-docs.diff là toàn diff hai file tài liệu so baseline mở phiên. Lệnh chốt laptop: `{COMMAND}`. Lệnh EC2 cuối và payload/timer ở checkpoint.json. Không cần Minh quyết ngân sách cho chặng đã làm; Minh cần mở phiên mới do nén ngữ cảnh.
''')
    prompt = '''Đọc AGENTS.md, tiếp T-033 trong STATE. Codex là người làm, Claude là người phản biện. Phiên mới chỉ dùng repo; ghi dòng mở phiên vào LOG. Phiên 6 đã checkpoint ngay vì ngữ cảnh nén theo AGENTS §5a.2.

Đọc toàn SPEC T-033, LOG phiên 3–6 và bổ sung cuối phiên 5; các checkpoint-handoff-001, session4-checkpoint-001, session5-open-001, session5-budget-001, session5-checkpoint-001 và session5-approval-checkpoint-001 theo đường dẫn trong LOG. Đọc checkpoint mới results/T-033/runs/session6-compute-checkpoint-001/README.md, checkpoint.json, coverage-resources.json, artifact-inventory.json, receive-verification.json, final-ledger.json, scope-verification.json và manifest.json; session6-open-001/ bằng chứng nguồn, fixture, guard, AST, pilot/rest, các timer; session6-final-budget-001/ledger.json. Kiểm hash theo manifest/inventory trước dùng. Đọc trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, toàn LESSONS và WHY-41 trước diễn giải.

Chặng tính đã tự kiểm đạt, không là task hoàn tất. Tái dùng đơn vị PASS theo hash: nguồn cũ ở checkpoint-handoff-001/artifacts và locator; N-Sigma/BOCPD/channel pilot+rest, mã và kết quả mới ở session6-compute-checkpoint-001/artifacts. Sáu run có fixture/source/time/flags/CP/schema/readback/resource và exit PASS. Không khởi lại run PASS. Giữ mọi bản cũ; không xóa gì thêm. Laptop chỉ điều khiển/tài liệu/nhận/kiểm hash; tính nghiên cứu trên EC2 pin.

Làm tiếp đọc tay và tổng hợp đúng SPEC. Đọc code native và saved intermediates trước đề xuất chạy thêm; lần theo ca báo và ca/điểm không báo với điều kiện tương ứng. Đọc nhóm gốc và khóa mới artifacts/runs/session6-groups-001/bao-phu-nhom.json, verification.json; kiểm lựa chọn/coverage rồi khóa điểm đối chứng trước diễn giải, giữ mọi nhóm bắt buộc và ánh xạ mọi đường ca. Input trùng, collapse hợp lệ, không kênh, lỗi và contrast không định nghĩa giữ riêng cùng mẫu số. Nối đầu vào → xử lý → thống kê/phân phối → cờ/CP → chấm, xét giải thích cạnh tranh. Không gọi trước proxy là false alarm vận hành, độ lệch proxy là trễ vật lý, đồng xuất hiện trace/log là nguyên nhân hay các kênh là độc lập thống kê. Phân biệt dữ liệu, giao thức, adapter/cài đặt và giả định phương pháp. Đủ số/đủ file không thay bằng chứng phân xử. Thiếu trung gian/thiết kế không phân xử được thì giữ OPEN, trình đúng phép kiểm, chi phí và quyết định phụ thuộc; không tự chạy vượt quyền hoặc đổi SPEC/tham số/tiêu chí.

Q-128/Q-129/Q-132 đã lưu; không ghi quyết định mới. Hạch toán cũ 8 giờ là dự phòng chưa kiểm, actual cũ OPEN; không còn chờ duyệt ngân sách. Tổng charged mới và phần còn lại lấy snapshot cuối session6-final-budget-001/ledger.json, có timer mọi xử lý từ sau lời duyệt. Nếu cần bất kỳ xử lý EC2 mới, kể cả process/hash/kiểm và lỗi, đo toàn lượt và cộng dồn từ snapshot cuối; dựng/pin snapshot mới trước run. Không dùng lịch hoặc subtotal status thay ledger. Giữ ledger lịch sử. Bằng chứng EC2 cuối không có worker; trước dùng EC2 kiểm process/source/hash mới có đo, không khởi trùng. Không cài package, bật/tắt EC2 hay xóa thêm. Lệnh/pin/SSH tại README. Hash hoặc CP lệch/sắp vượt trần thì checkpoint, dừng phần phụ thuộc và trình Minh.

Phạm vi ghi: results/T-033/ thư mục lượt mới, LOG chỉ nối, duy nhất dòng T-033 STATE (đọc ngay trước sửa), EC2 ~/rca/T-033/. Không sửa nguồn cũ, SPEC, DECISIONS, WHY, test/locked/heldout, T-032; không commit/push. Không tự thêm quy trình/cổng. Khi hoàn thành đọc tay/tổng hợp, tự kiểm toàn diff, chuỗi bằng chứng/số/nguồn/phạm vi và mục tiêu MRP/DT18/advisor, ghi rõ kết luận được phân xử và OPEN. Chỉ khi toàn task hoàn tất mới soạn prompt Claude nguyên văn Common + Soát kết quả + G2 trong docs/review-prompt.md; Minh chuyển thủ công, không tự gửi/mở review. Ngữ cảnh nén thì checkpoint ngay và đề nghị phiên mới. Cuối phiên LOG đủ AGENTS §7, lệnh cuối/bước tiếp chính xác, STATE đúng T-033 và trạng thái EC2/việc Minh cần làm.
'''
    new_text('prompt-next-session.md', prompt)
    end = f'''

### Kết thúc phiên 6 — {stamp()} — checkpoint do ngữ cảnh nén

1. Đã làm: tự kiểm nguồn/process/hash mới; hoàn thiện lifecycle/pilot-rest/provenance/fixture trong phạm vi SPEC. Guard dùng snapshot accounting hợp lệ trước mỗi run, giữ staged cũ. Ba pilot đạt rồi mới rest; sáu run PASS, N-Sigma60/BOCPD30/kênh30. Khóa nhóm sau phân rã và trước diễn giải trong run mới, giữ nhóm gốc, input trùng/collapse hợp lệ/không kênh/lỗi và mẫu số riêng. Nhận299 file mới bằng stream/hash hai đầu. Ngữ cảnh bị nén, dừng nghiên cứu theo AGENTS §5a.2; không bắt đầu đọc tay hay viết cơ chế/tổng hợp. Không thêm/thay quyết định chính thức.
2. File thay đổi: chỉ thêm results/T-033/scripts/session6_*.py, finish_session6.py, scripts/session6-001/ và session6-002/, runs/session6-open-001/, sáu snapshot/run pilot/rest, session6-groups-budget-001/, session6-final-budget-001/ và session6-compute-checkpoint-001/; tên đầy đủ/hash trong manifest checkpoint. LOG chỉ nối; duy nhất dòng T-033 STATE. EC2 chỉ thêm trong ~/rca/T-033/ các bản staged/run/config/ledger/nhóm, cập nhật progress; không xóa/archive mới. Không sửa nguồn/native/adapter/env/raw, SPEC/WHY/DECISIONS/MRP/LESSONS/AGENTS/review-prompt, script gốc, T-032 hoặc test/locked/heldout; không cài package/commit/push/bật/tắt EC2.
3. Kiểm: laptop825 file cũ/hash PASS đầu phiên; raw89 file và pin native/env EC2 PASS đầu/cuối. Pilot fixture scalar/native, valid-accounting guards, time/flags/CP/schema và readback/resource PASS; sáu quan sát độc lập PASS, exit0/source-after PASS. Nhận299 file/{received['bytes']} byte và kiểm lại toàn hash PASS. Script prep stage001 đổi line ending core làm lệch pin: phát hiện trước pilot, giữ bản001; stage002 core exact byte/hash, AST phần tính giữ nguyên. Bộ lọc worker đã sửa đúng đường staged và evidence observe được chống ghi đè trước poll lặp, không worker trùng/timer mất. Trợ lý chỉ đọc hỗ trợ, không thay tự kiểm/Claude. Bằng chứng tại session6-open-001 và checkpoint/coverage-resources.json; scope và manifest kiểm toàn diff/file set phiên. Không suy cơ chế từ các kiểm kỹ thuật.
4. OPEN: chặng tính đạt, nhưng đọc tay/điểm đối chứng/đánh giá coverage và tổng hợp các đầu ra SPEC chưa làm. RQ2/P4/G2/DT18 NV2–NV3 chưa phân xử bằng chuỗi có đối chứng; không xác nhận cơ chế riêng ca hoặc nguyên nhân vật lý, onset thật hay lựa chọn P6. Phải đọc toàn nhóm gốc/nhóm mới và trung gian, lập các giải thích cạnh tranh và đúng phần cần kiểm tiếp. Thiếu bằng chứng thì trình phạm vi/chi phí/decision phụ thuộc, không loại nghĩa vụ vì ngoài phiên. Thời gian thực tế cũ không tái dựng vẫn OPEN; Q-132 là mức dự phòng chưa kiểm và không còn chờ hạch toán. Tổng charged mới {account['new_processing_charged_s']:.12f}s, còn {account['remaining_approved_s']:.12f}s/14400s; đã gồm lượt hỏng/kiểm/transport/job, SSH bounds bảo thủ và overlap điều khiển cộng riêng. Không dùng lịch/status subtotal. Ledger lịch sử giữ nguyên, snapshot cuối session6-final-budget-001/ledger.json, bản sao final-ledger.json.

EC2 cuối {checkpoint['ec2']['observed_during']}: không worker T-033/tmux, archive không tồn tại; logical byte/RAM/disk ở final-preflight-001.stdout và checkpoint.json. Sáu run hoàn tất, không còn ước lượng chờ xong. Đã báo ổn định sau pilot đạt và đo tài nguyên/ngân sách/lỗi tự dừng; hiện Minh có thể tắt laptop. Không bật/tắt EC2. Việc Minh cần làm: mở phiên mới bằng prompt-next-session.md do nén ngữ cảnh; không còn yêu cầu duyệt ngân sách cho chặng tính đã làm.

Bước tiếp chính xác: đọc results/T-033/runs/session6-compute-checkpoint-001/README.md và prompt-next-session.md; kiểm manifest/inventory bằng byte/hash trước dùng; đọc khóa nhóm artifacts/runs/session6-groups-001/bao-phu-nhom.json cùng verification.json, nguồn cũ locator và các intermediates mới. Sang phiên mới mới tiếp đọc tay có đối chứng rồi tổng hợp theo SPEC và nguồn MRP/DT18/advisor. Không launch lại PASS. Nếu cần EC2 đọc/kiểm mới, đo toàn SSH và dựng ledger snapshot từ snapshot cuối trước run tiếp; process/source/hash phải mới. Lệnh tiến độ `tail -n 20 ~/rca/T-033/trang-thai.txt` qua SSH pin có đo; lệnh chạy không còn cần ở checkpoint này. Prompt phiên sau chép dưới đây; chưa là phản biện Claude vì toàn task chưa hoàn tất.

Lệnh chốt cuối laptop: `{COMMAND}` (chỉ metadata/hash/tài liệu, tự kiểm nội bộ). Lệnh EC2 cuối: controller `session6_control.py remote --name final-preflight-001 --code results/T-033/scripts/session6_preflight.py`; Python pin qua SSH stdin, payload đầy đủ session6_preflight.py, stdout/stderr/timer ở session6-open-001/final-preflight-001.*. Giờ xử lý của lệnh này đã cộng trong snapshot cuối. Không có lệnh EC2 mới khi chốt checkpoint.

#### Prompt tiếp nhận phiên đọc tay và tổng hợp (Minh copy sang phiên Codex mới)

{prompt}
'''
    with LOG.open('ab') as f:
        f.write(end.encode('utf-8'))
    # Read immediately before mutation; preserve every byte outside the exact task row.
    state_now = STATE.read_bytes()
    assert state_now == old_state
    lines = state_now.splitlines(keepends=True)
    indices = [i for i, line in enumerate(lines) if line.startswith(b'| T-033 |')]
    assert len(indices) == 1
    i = indices[0]
    fields = lines[i].decode('utf-8').split('|')
    fields[6] = ' Đang thực hiện (phiên 6, 11/10): chặng tính pilot/rest N-Sigma60/BOCPD30/kênh30, nguồn/fixture/resource/hash đạt; khóa nhóm mới trước diễn giải. Không worker EC2. Ngữ cảnh nén → checkpoint session6-compute-checkpoint-001; mở phiên mới đọc tay và tổng hợp. RQ2/G2 và thời gian thực tế cũ OPEN; snapshot ngân sách cuối session6-final-budget-001 '
    lines[i] = '|'.join(fields).encode('utf-8')
    STATE.write_bytes(b''.join(lines))
    assert LOG.read_bytes().startswith(old_log)
    changed = [n for n, (a, b) in enumerate(zip(old_state.splitlines(keepends=True), STATE.read_bytes().splitlines(keepends=True))) if a != b]
    assert changed == [i]
    for name, expected in protected.items():
        assert entry(ROOT / name) == expected
    diff = ''
    for name in [rel(LOG), rel(STATE)]:
        before = (OPEN / 'before' / name).read_text(encoding='utf-8').splitlines(keepends=True)
        after = (ROOT / name).read_text(encoding='utf-8').splitlines(keepends=True)
        diff += ''.join(difflib.unified_diff(before, after, fromfile=name+' (session6 baseline)', tofile=name+' (after)'))
    new_text('approved-docs.diff', diff)
    write(C / 'scope-verification.json', {'status': 'PASS', 'at': stamp(),
        'log_prefix_unchanged': True, 'state_changed_rows_1based': [i+1],
        'state_changed_task': 'T-033', 'protected_sources_unchanged': protected,
        'original_scripts_byte_unchanged': {p.name: entry(p) for p in (OPEN/'scripts').iterdir()},
        'historical_ledger_unchanged': True, 'new_formal_decisions': [],
        'received_all_rehashed': len(inv['files']), 'complete_session_diff': rel(C/'approved-docs.diff'),
        'source_and_remote_checks': rel(OPEN/'final-preflight-001.stdout'),
        'no_ec2_command_during_close': True})
    selected = list(OPEN.rglob('*')) + list(C.rglob('*'))
    selected += list((ROOT/'results/T-033/scripts/session6-001').rglob('*'))
    selected += list((ROOT/'results/T-033/scripts/session6-002').rglob('*'))
    selected += list((ROOT/'results/T-033/scripts').glob('session6_*.py'))
    selected += [ROOT/'results/T-033/scripts/finish_session6.py']
    for name in RUNS:
        selected += list((ROOT/'results/T-033/runs'/(name+'--budget')).rglob('*'))
    for name in ['session6-groups-budget-001', 'session6-final-budget-001']:
        selected += list((ROOT/'results/T-033/runs'/name).rglob('*'))
    selected += [LOG, STATE]
    files = {rel(p): entry(p) for p in sorted(set(selected)) if p.is_file() and p.name != 'manifest.json'}
    # Child manifests are governed by the received inventory and should also be pinned here.
    for p in (C/'artifacts').rglob('manifest.json'):
        files[rel(p)] = entry(p)
    write(C/'manifest.json', {'status':'PASS', 'at':stamp(), 'path_basis':'repository root',
        'scope':'session6 scripts/evidence/budgets/checkpoint and append LOG/T033 STATE; excludes this self manifest',
        'files':files})
    for name, expected in files.items():
        assert entry(ROOT/name) == expected, name
    print(json.dumps({'status':'PASS', 'checkpoint':rel(C), 'manifest_files':len(files),
        'new_charged_s':account['new_processing_charged_s'], 'remaining_s':account['remaining_approved_s'],
        'ec2_worker_candidates':[], 'task_complete':False}, ensure_ascii=False))

if __name__ == '__main__':
    main()
