"""Laptop-only immutable checkpoint: metadata, hashes, ledger, LOG and own STATE row."""
import datetime
import difflib
import hashlib
import json
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
OPEN = ROOT / 'results/T-033/runs/session8-open-001'
OUT = ROOT / 'results/T-033/runs/session8-compute-evidence-checkpoint-001'
LOG_REL = 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'
STATE_REL = 'docs/STATE.md'
LOG = ROOT / LOG_REL
STATE = ROOT / STATE_REL
STAMP = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def text(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value)


def meta(path):
    return {'bytes': path.stat().st_size, 'sha256': sha(path)}


def without_task(text_value):
    return [line for line in text_value.splitlines() if not line.startswith('| T-033 |')]


# Validate before any checkpoint/LOG/STATE mutation. Do not confuse historical
# LOG/STATE pins with authorized live appends.
baseline = read(OPEN / 'baseline.json')
old_bad = [rel for rel, pin in baseline['old_t033_files'].items()
           if not (ROOT / rel).is_file() or meta(ROOT / rel) != pin]
protected_bad = [rel for rel, pin in baseline['protected'].items()
                 if not (ROOT / rel).is_file() or meta(ROOT / rel) != pin]
assert not old_bad, old_bad
assert not protected_bad, protected_bad
assert LOG.read_bytes().startswith((OPEN / 'LOG.md.before').read_bytes())
state_before = STATE.read_text(encoding='utf-8-sig')
assert without_task(state_before) == without_task((OPEN / 'STATE.md.before').read_text(encoding='utf-8-sig'))
assert len([line for line in state_before.splitlines() if line.startswith('| T-033 |')]) == 1
assert not OUT.exists()

receive_checks = []
for run in ['session8-extraction-001', 'session8-evidence-receive-001', 'session8-stats-receive-001']:
    base = ROOT / 'results/T-033/runs' / run
    inventory = read(base / 'artifact-inventory.json')
    entries = inventory.get('files', inventory)
    if isinstance(entries, list):
        entries = {item.get('path', item.get('relative_path')): item for item in entries}
    bad = [rel for rel, pin in entries.items()
           if not (base / 'artifacts' / rel).is_file() or meta(base / 'artifacts' / rel) != pin]
    assert not bad, (run, bad)
    verification = read(base / 'receive-verification.json')
    assert verification['status'] == 'PASS' and verification['two_end_hashes_verified']
    receive_checks.append({'run': run, 'files': len(entries), 'bytes': sum(p['bytes'] for p in entries.values()),
                           'hash_status': 'PASS', 'inventory': meta(base / 'artifact-inventory.json')})

final_preflight = read(OPEN / 'session8-final-preflight-001.stdout')
assert final_preflight['status'] == 'PASS' and not final_preflight['worker_candidates']
assert not final_preflight['tmux'].strip()
assert final_preflight['logical_bytes'] < 5 * 2**30
pilot_verify = read(OPEN / 'session8-verify-pilot-001.stdout')
rest_verify = read(OPEN / 'session8-verify-rest-001.stdout')
assert pilot_verify['status'] == rest_verify['status'] == 'PASS'
counts = {key: pilot_verify['counts'][key] + rest_verify['counts'][key]
          for key in pilot_verify['counts']}
assert counts['units'] == 210 and counts['points'] == 968
stats_base = ROOT / 'results/T-033/runs/session8-stats-receive-001/artifacts/runs/session8-stats-001'
stats = read(stats_base / 'stats.json')
assert stats['units'] == counts['units'] and stats['points'] == counts['points']

previous = ROOT / 'results/T-033/runs/session7-storage-approval-checkpoint-001/ledger.json'
ledger = read(previous)
charges = []
for path in sorted(OPEN.glob('*.timer.json')):
    timer = read(path)
    charges.append({'source': str(path.relative_to(ROOT)).replace('\\', '/'), 'sha256': sha(path),
                    'charged_processing_s': timer['charged_processing_s'], 'basis': timer['basis'],
                    'exit_code': timer['exit_code']})
assert len(charges) == len({item['source'] for item in charges})
ledger['charges'] += charges
ledger['new_processing_charged_s'] += sum(item['charged_processing_s'] for item in charges)
ledger['approved_total_processing_s'] = ledger['approved_prior_processing_s'] + ledger['new_processing_charged_s']
ledger['remaining_approved_s'] = ledger['approved_max_new_processing_s'] - ledger['new_processing_charged_s']
ledger['at'] = STAMP
ledger['previous_snapshot'] = {'path': str(previous.relative_to(ROOT)).replace('\\', '/'), 'sha256': sha(previous)}
ledger['next_run_requirements'] = [
    'Measure every EC2 command, including verification, transport and failed commands.',
    'Build and pin a fresh cumulative snapshot before next processing.',
    'Preserve prior snapshots; do not restart any PASS detector; do not delete further files.'
]
assert ledger['accounting_valid_for_next_run'] and ledger['remaining_approved_s'] > 0
assert ledger['approved_prior_processing_s'] == 28800 and ledger['approved_max_new_processing_s'] == 14400

OUT.mkdir(exist_ok=False)
shutil.copyfile(STATE, OUT / 'STATE.md.before')
write(OUT / 'ledger.json', ledger)
write(OUT / 'integrity.json', {
    'status': 'PASS', 'at': STAMP,
    'protected_files': len(baseline['protected']), 'protected_mismatch': protected_bad,
    'old_t033_files': len(baseline['old_t033_files']), 'old_t033_mismatch': old_bad,
    'receive_checks': receive_checks,
    'opening_integrity': str((OPEN / 'integrity.json').relative_to(ROOT)).replace('\\', '/'),
    'old_LOG_prefix_unchanged': True, 'all_other_STATE_lines_unchanged_since_open': True
})
write(OUT / 'checkpoint.json', {
    'status': 'CHECKPOINT_CONTEXT_COMPACTION', 'at': STAMP,
    'task': 'T-033', 'worker': 'Codex', 'reviewer': 'Claude',
    'task_complete': False, 'manual_interpretation': 'OPEN',
    'approved_storage_bytes': 5 * 2**30,
    'ec2_final_observation': {
        'source': 'results/T-033/runs/session8-open-001/session8-final-preflight-001.stdout',
        'timer': 'results/T-033/runs/session8-open-001/session8-final-preflight-001.timer.json',
        'logical_bytes': final_preflight['logical_bytes'], 'disk_free_bytes': final_preflight['disk_free_bytes'],
        'ram_available_bytes': final_preflight['ram_available_bytes'], 'worker_candidates': [],
        'source_native_raw_environment': 'PASS', 'raw_files': len(final_preflight['raw'])
    },
    'extraction': {'status': 'PASS', 'pilot_cases': 1, 'rest_cases': 29, 'counts': counts,
                   'detectors_reexecuted': False,
                   'source_scalars_and_readback': 'PASS', 'receive': receive_checks[0]},
    'saved_evidence': receive_checks[1], 'saved_stats_workload': receive_checks[2],
    'ledger': {'source': 'ledger.json', 'new_processing_charged_s': ledger['new_processing_charged_s'],
               'remaining_approved_s': ledger['remaining_approved_s'], 'session8_timers': len(charges),
               'session8_failed_timers': [item for item in charges if item['exit_code'] != 0],
               'old_actual_processing': 'OPEN; 8h administrative reserve is unverified'},
    'local_failures': [
        'Second invocation of session8_open.py stopped on existing output directory; no second append or EC2.',
        'Initial stream escalation was rejected before process by automatic approval review; same action later approved after exact payload/destination/provenance check.'
    ],
    'open_work': [
        'Worker manual reading and matching/point controls for every mandatory frozen group and every unit path; partial point reading is not whole coverage.',
        'Same-column N-Sigma noalarm values must come from full pinned gzip; reduced chain may choose another column.',
        'Duration arrays exist in session6 context NPZ but are omitted by v2 projection; inspect at locked indices without detector rerun. Workload projection was supplemented.',
        'Theta absence, range0 collapse, input-identical/changed factorial contrasts and interactions retain their actual denominators; do not turn null group denominators into zero.',
        'Physical onset, workload causality, clean normal controls, trace/log collection completeness and duration physical units are unresolved.',
        'Complete all named SPEC outputs and five P4 categories with source pointers, competing explanations, minimum follow-up evidence and P6 dependencies.',
        'Official Claude review handoff is not started; no source decision, design selection, task closure, test access or commit approval is inferred.'
    ]
})

prompt = '''Đọc AGENTS.md, tiếp T-033 trong STATE. Codex làm, Claude phản biện. Phiên8 đã checkpoint theo AGENTS §5a.2 vì ngữ cảnh nén; chưa hoàn thành task. Ghi mở phiên trong LOG đúng phạm vi SPEC.

Đọc toàn SPEC và LOG, checkpoint mới results/T-033/runs/session8-compute-evidence-checkpoint-001/README.md, checkpoint.json, ledger.json, integrity.json, scope-verification.json, manifest.json. Kiểm byte/hash theo manifest/inventory trước dùng. LOG/STATE trong manifest là snapshot lịch sử: sau khi đã nối hoặc thay dòng khác, đối chiếu LOG.md.after/STATE.md.after của checkpoint, không so bản lịch sử với nội dung hiện hành. Đọc checkpoint session7-storage-approval-checkpoint-001, session7-storage-checkpoint-001 và phiên6 theo LOG. TrầnEC2 5GiB và bản tríchv2/pilot/rest đã được Minh duyệt, không xin lại.

Pilot1/rest29 và readback/scalar/source đã PASS, không chạy lại detector PASS hoặc trích lại đơn vị hợp lệ. Ba kho nhận: session8-extraction-001 (gzip đầy đủ), session8-evidence-receive-001 (chuỗi/contrast/độ lệch/fixed/log/coverage), session8-stats-receive-001 (stats và workload-at-locked-points). Mỗi kho có artifact-inventory.json và receive-verification.json; các nguồn phiên6/nguồn gốc/khóa điểm theo LOG giữ nguyên. Laptop chỉ đọc kết quả/hash/tài liệu; mọi tính nghiên cứu vẫn trên EC2 pin có ledger/timer.

Tiếp đọc tay và tổng hợp toàn SPEC; chưa giao Claude phản biện chính thức. Đọc trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor§1, LESSONS, WHY-41 và quyết định liên quan. Tự đọc code native/adapter và saved intermediates, các nhóm gốc/nhóm mới, đối chứng ca/điểm và thông tin matching. Ghi chuỗi đầu vào→xử lý→trung gian→cờ/CP→chấm; xét giải thích cạnh tranh, phân biệt dữ liệu/giao thức/cài đặt/phương pháp, quan sát/suy luận/ứng viên/quyết định/OPEN. Số có đường dẫn và con trỏ JSON/NPZ; không dùng ghi nhớ hoặc trợ lý thay bằng chứng.

Đọc notes hỗ trợ trong session8-open-001/helper-readonly-notes.md sau tự soát gốc. Đây không là Claude review hay kết luận được duyệt. Reduced N-Sigma noalarm có thể giữ cột khác: lấy cùng cột từ gzip full point_source. Workload đã bổ sung trên EC2 ở stats receive; duration còn ở trace_group_duration_* trong context NPZ phiên6, tra second/entity chính xác tại điểm khóa. Thiếu projection không đồng nghĩa thiếu instrumentation. Không suy log đầu/cuối bao trùm mọi lỗi; không công bố token/userID. Kiểm mọi theta-absent/NaN/range0/input-identical/interaction và mẫu số từ nguồn thật; null group_denominators không là0. Không đổi khóa/tiêu chí/tham số theo kết quả.

Hoàn thiện mọi đầu ra SPEC trong results/T-033/, gồm báo cáo nguyên nhân, chuỗi bằng chứng, bao phủ, phân rã tiền xử lý, độ lệch sau mốc, N-Sigma fixed, đối chiếu, tải/log, đọc tay và kiểm tiếp. Không giảm câu hỏi xuống bảng tỷ lệ; tách chuỗi tính toán đã phân xử với nguyên nhân vật lý/onset/coverage còn OPEN; nêu đúng bằng chứng còn cần, chi phí/phạm vi và quyết định P6 phụ thuộc. Đọc bài/code chính thức ở revision phù hợp trước dẫn hạn chế tác giả; không gán quan sát của mình cho tác giả. Nếu thiếu quyền/khả năng phân xử, trình phần bổ sung cho Minh, không chạy vượt quyền hoặc loại nhóm quan trọng.

Ledger cuối ở checkpoint mới. 8h cũ là dự phòng chưa kiểm, actual cũ OPEN; tối đa4h xử lý mới giữ nguyên. Mọi EC2 mới, kể cả process/hash/transport/lỗi, phải có timer và snapshot cumulative mới pin trước chạy. Controller phiên8 giữ snapshot base phiên7 cộng toàn timer phiên8; phiên mới phải nối checkpoint mới và timer chỉ của phiên mới, tránh cộng đôi. Không dùng lịch/status subtotal. Quan sát cuối không worker là lịch sử; trước EC2 mới kiểm process/source/hash có đo. Không xóa thêm, cài package, bật/tắt EC2, mở test/locked/heldout, sửa nguồn cũ, SPEC, WHY/DECISIONS/MRP/T-032; không commit/push. Phạm vi ghi: results/T-033/ lượt mới, LOG chỉ nối, duy nhất dòngT-033 STATE đọc ngay trước sửa, EC2 ~/rca/T-033/.

Khi toàn task hoàn tất, tự kiểm toàn diff/nguồn/số/chuỗi và mục tiêu nguồn; cập nhật đúng trạng thái rồi soạn prompt Claude nguyên văn Prompt chung + Soát kết quả + G2 trong docs/review-prompt.md, chỉ điền trung tính. Minh chuyển thủ công; không tự mở/gửi review. Ngữ cảnh nén thì checkpoint ngay; cuối phiên báo đủ4mục, LOG/lệnh cuối/bước tiếp/STATE và trạng thái EC2.
'''
text(OUT / 'prompt-next-session.md', prompt)

new_charged = ledger['new_processing_charged_s']
remaining = ledger['remaining_approved_s']
readme = f'''# Checkpoint phiên8 — T-033

Checkpoint do ngữ cảnh nén theo AGENTS §5a.2. Codex người làm, Claude người phản biện. Task chưa hoàn tất; đọc tay toàn nhóm, tổng hợp SPEC và câu hỏi nguồn vẫn OPEN. Không cần duyệt lại trần5GiB hoặc bản tríchv2.

1. **Đã đạt:** pilot1/rest29 có {counts['units']} đường ca/{counts['points']} điểm khóa; readback/scalar/time/post_indices/NaN/flags/BO-MAP/CP/theta/source-after PASS. Không chạy detector. Các kho nhận mới có hash hai đầu PASS: extraction40file, evidence10file, stats+workload4file. Nguồn/raw89/native/env cuối PASS; không worker T-033 hay tmux ở thời điểm final-preflight.
2. **Đã ghi:** script phiên8, runs/metadata/receiver mới trong results/T-033; LOG chỉ nối; chỉ dòngT-033 STATE. Danh sách chính xác trong manifest.json. File cũ và tài liệu bảo vệ không đổi so baseline mở phiên. Không xóa thêm/commit/push, không thay nguồn/phương pháp/SPEC hay quyết định.
3. **Kiểm/ngân sách:** dùng ledger.json, integrity.json, scope-verification.json và manifest.json. Charged mới cumulative {new_charged!r}s; còn {remaining!r}s/14400s. Bao gồm lỗi SSH, kiểm, tính từ saved arrays và transport; fullSSH elapsed là upper bound bảo thủ. 28800s cũ chỉ là dự phòng chưa kiểm, actual cũ OPEN. EC2 logical {final_preflight['logical_bytes']}byte <5368709120byte; diskfree {final_preflight['disk_free_bytes']}byte. Lệnh cuối EC2 có timer/ledger là session8-final-preflight-001, chỉ đọc. Không xử lý EC2 sau đó khi chốt.
4. **Còn làm:** đọc tay toàn64nhóm/210đường theo khóa, đối chứng cùng cột/điểm/ca, cạnh tranh giải thích, duration còn trongNPZ, kiểm các thiếu theta/NaN/input-identical/range0/interaction, mọi đầu ra SPEC và năm loại kết quảP4. Nguồn vật lý/onset/tải/collector và lợi ích/chọn thiết kế đồ thị không tự được xác nhận. Ghi đúng bằng chứng thiếu và phụ thuộcP6; không giảm nghĩa vụ nghiên cứu cho vừa phiên.

## Đường dẫn tiếp nhận

- results/T-033/runs/session8-extraction-001/artifacts/runs/session7-manual-pilot-001 và session7-manual-rest-001: gzip full point_source. Inventory/hash ở thư mục receiver.
- results/T-033/runs/session8-evidence-receive-001/artifacts/runs/session8-evidence-001: chuoi-bang-chung.json, bao-phu-nhom.json, phan-ra-tien-xu-ly.json, do-tre-sau-moc.json, nsigma-nguong-co-dinh.json, doi-chieu.json, tai-log.json, digest.json, source-verification.json, manifest.json. Đây là quan sát tính từ dữ liệu đã lưu; manual_interpretation OPEN. Root bao-phu-nhom.json cũ chưa thay.
- results/T-033/runs/session8-stats-receive-001/artifacts/runs/session8-stats-001: stats.json, workload-at-locked-points.json, verification.json, manifest.json. Workload là telemetry quan sát, không là bằng chứng tải ngoài/coverage đầy đủ.
- session8-open-001: input/payload/stdout/stderr/timer, kiểm extraction, baseline và helper-readonly-notes.md. Notes trợ lý không thay tự soát của người làm. Native/source/điểm được kiểm và giữ nguyên. Chuỗi rút gọn không có đầy đủ cột noalarm/duration; đọc gzip/NPZ đầy đủ theo notes, không gọi là thiếu dữ liệu nguồn.
- session6-compute-checkpoint-001/artifacts: nguồn context/factorial/delay/fixed và nhóm đã khóa; checkpoint-handoff-001/artifacts: nguồn gốc/core. Kiểm inventory tương ứng trước dùng. Nhóm/matching/point locks phiên7 giữ nguyên.

## Thực hiện phiên mới

Mở phiên Codex mới trong D:/RCA-flashticket bằng prompt-next-session.md. Đầu tiên đọc các nguồn và kiểm hash, không mở thêm run detector. Runtime laptop metadata/tài liệu: C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8. Python EC2/SSH pin trong scripts/session8_control.py; controller đó chỉ đúng với base/timer phiên8, không gọi lại nguyên trạng ở phiên9. Nối ledger checkpoint mới + timer phiên mới trước bất kỳ EC2 mới; quan sát process/hash cuối là lịch sử, cần kiểm mới có đo nếu dùng EC2.

Manifest pin cả LOG/STATE tại checkpoint; các bản LOG.md.after và STATE.md.after là snapshot bất biến cho kiểm lịch sử ở phiên sau. Không so pin lịch sử với live LOG đã nối hoặc STATE có dòng khác đổi. Lệnh cuối laptop: python bundled -B -X utf8 results/T-033/scripts/finish_session8.py (metadata/hash/tài liệu, không nghiên cứu/SSH). Kiểm toàn phạm vi nằm trong scope-verification.json.

Lượt lỗi local do gọi lại session8_open đã dừng mkdir, không EC2. Lượt SSH sandbox lỗi255 được đo. Stream lần đầu bị automatic approval review từ chối trước process; đã đọc quyền nhận đúngpayload/đích và provenance công khai, retry cùng hành động được duyệt rồi PASS. Giữ mọi timer/lượt lỗi và các bản lỗi phiên7; không xóa thêm.

Chưa prompt Claude chính thức vì task chưa xong. Minh không cần quyết lại dung lượng/thời gian; cần mở phiên tiếp theo do nén ngữ cảnh. Chưa có quyết định khoa học chính thức mới. Nội dung nghiên cứu cần đưa vào tài liệu chính thức sau tự kiểm/đủ chuỗi vẫn chưa tổng hợp. Đề xuất commit sau khi hoàn thiện và phản biện: T-033: trích trung gian đã lưu, phân xử cơ chế và tổng hợp P4; chưa commit/push.
'''
text(OUT / 'README.md', readme)

entry = f'''

### Kết thúc phiên8 — {STAMP} — checkpoint vì ngữ cảnh nén

1. Đã làm: tiếp đúng lời duyệt trầnEC2 5GiB và v2; pilot1 rồi kiểm đạt mới rest29, không trùng. Trích210đường/968điểm đã khóa, kiểm scalar/time/post_indices/finite-null/flags/BO-MAP/CP/theta và nguồn trước/sau. Nhận40file extraction rồi10file evidence và4file stats/workload, hash hai đầu PASS. Tính evidence/contrast/fixed/độ lệch/log ở điểm chỉ từ dữ liệu đã lưu trên EC2 có ledger/timer. Đã đọc một phần chuỗiBO và trợ lý đọc N-Sigma đại diện/cặp cùng cột; không nhận đã đọc tay đủ nhóm hay hoàn thành RQ2. Ngữ cảnh nén, checkpoint theo AGENTS§5a.2, dừng nghiên cứu trong phiên.
2. File đổi: chỉ thêm scripts/session8_*.py, finish_session8.py, runs/session8-* theo manifest checkpoint; LOG chỉ nối và chỉ dòngT-033 STATE. EC2 chỉ thêm run pilot/rest v2, evidence/stats và các snapshot ledger trong ~/rca/T-033/. Mọi file trước mở phiên và tài liệu bảo vệ giữ nguyên, không xóa thêm/nguồn/native/env/raw/SPEC/WHY/DECISIONS/MRP/AGENTS/T-032/test/locked/heldout/cài package/commit/push/bật-tắtEC2. Không quyết định chính thức mới.
3. Kiểm: integrity mở phiên theo checkpoint7/storage/approval/6 và825+299 nguồn cũ PASS; pilot/rest readback exact PASS; final EC2 source/raw89/native/env/process PASS, khôngworker/tmux. Nhận và tái kiểm54file hash PASS. Toàn oldT033/protected/prefixLOG/STATEngoàiT033/diff/fileset tại integrity/scope/manifest checkpoint PASS. Một SSHsandbox lỗi255 có timer; initialstream bị automatic approval review chặn trước process rồi cùngaction được duyệt sau đọc quyền/provenance; local mở phiên lần2 dừng mkdir, khôngEC2. Giữ mọi lỗi. Projection workload bị thiếu vì tênmảng, đã bổ sung từ nguồn context; duration còn trongNPZ chứ không phải mất instrumentation. Reducednoalarm không luôn giữ cùngcột; không dùng nó làm đối chứng cùngcột.
4. OPEN: chặng trích/kiểm/nhận đạt; task, đọc tay toàn64nhóm/210đường, báo cáo và mọi đầu ra SPEC chưa hoàn tất. RQ2/P4/G2/P6 cần chuỗi phân xử theo nhóm, nguyên nhân cạnh tranh và phần bằng chứng thiếu. Không suy trướcproxy là báo giả vận hành, offsetproxy là trễ vật lý, đồngxuấthiện workload/log/trace là nhân quả, hoặc graph có lợi. Nguồn physicalonset/collector/cleannegative/đơnvịduration còn OPEN. Theta-absent/range0/input-identical/interaction/matching thiếu phải giữ đúng mẫu số; null không là0. Kiểm scalar ở điểm và số tổng không tự chọn phương pháp/SLI/ngưỡng hay đóng câu hỏi nguồn. Actualthờigiancũ OPEN; dựphòng28800s chưa kiểm. Ledgercumulative mới {new_charged!r}s, còn{remaining!r}s/14400s, gồm mọi EC2mới/lỗi/kiểm/transport; không dùng lịch hay status subtotal. Không xin duyệt lại storage/time.

EC2 cuối: session8-final-preflight-001 PASS, logical{final_preflight['logical_bytes']}byte dưới5GiB, diskfree{final_preflight['disk_free_bytes']}byte, khôngworker/tmux tại thời điểm timer. Không xử lý EC2 mới khi chốt checkpoint. Giữ EC2, không bật/tắt; laptop có thể đóng vì không jobT033 đang chạy. Minh cần mở phiên Codex mới theo prompt checkpoint; Claude vẫn phản biện chính thức sau khi toàn task hoàn tất. Không tự mở/gửi review.

Bước tiếp chính xác: đọc results/T-033/runs/session8-compute-evidence-checkpoint-001/README.md, checkpoint.json, ledger.json, integrity.json, scope-verification.json và manifest.json; kiểm hash với snapshot LOG/STATE lịch sử. Đọc cả3receiver inventories và artifacts; tự soát nguồn/code/nhóm/pointmatching trước đọc helper-readonly-notes.md. Tiếp đọc tay/trung gian/fullgzip/NPZduration rồi tổng hợp toànSPEC và MRP/DT18/advisor/LESSONS/WHYliênquan, mọi số có con trỏ. Không có lệnh detector cần chạy lại. Nếu EC2 mới, nối ledgercheckpoint này với timerphiênmới trước run, process/source/hash mới cóđo; không gọi nguyêncontroller8 rồi cộng đôi timer8.

Lệnh EC2 cuối: session8_control.py remote-readonly session8-final-preflight-001 results/T-033/scripts/session6_preflight.py; stdin Python pin, payload/stdout/stderr/timer tại session8-open-001, snapshot trước lệnh tại session8-final-preflight-001--budget/ledger.json; thời gian đã cộng checkpointledger. Lệnh laptop chốt cuối: C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8 results/T-033/scripts/finish_session8.py, chỉ metadata/hash/tài liệu. Danh sách file và fullscope ở checkpoint. Đề xuất commit sau toàntask/tựkiểm/phảnbiện: T-033: trích trung gian đã lưu, phân xử cơ chế và tổng hợpP4. Chưa commit/push.

#### Prompt tiếp nhận phiên đọc tay/tổng hợp — Minh copy sang Codex mới

{prompt}
'''
with LOG.open('a', encoding='utf-8', newline='\n') as stream:
    stream.write(entry)
new_row = ('| T-033 | Lần theo cơ chế báo động trước mốc | P4 | Codex | Claude | '
           'Đang thực hiện (phiên8, 11/10): v2 pilot1/rest29 và kiểm/nhận PASS, 210 đường/968 điểm; '
           'không rerun detector, giữ mọi lỗi. Evidence/stats/workload đã lưu, đọc tay toàn nhóm/tổng hợp SPEC/RQ2/G2 còn OPEN. '
           'Checkpoint ngay vì ngữ cảnh nén: session8-compute-evidence-checkpoint-001; ledger cuối ở đó, '
           'trần5GiB đã duyệt, không xin lại; EC2 cuối không worker, trước dùng mới phải kiểm có đo | '
           '`tasks/T-033-g2-nguyen-nhan-phat-hien/` |')
state_after = '\n'.join(new_row if line.startswith('| T-033 |') else line for line in state_before.split('\n'))
assert without_task(state_after) == without_task(state_before)
STATE.write_text(state_after, encoding='utf-8', newline='\n')
assert LOG.read_bytes().startswith((OPEN / 'LOG.md.before').read_bytes())
assert without_task(STATE.read_text(encoding='utf-8-sig')) == without_task(state_before)
shutil.copyfile(LOG, OUT / 'LOG.md.after')
shutil.copyfile(STATE, OUT / 'STATE.md.after')
text(OUT / 'STATE.diff', ''.join(difflib.unified_diff(state_before.splitlines(keepends=True),
                                                   state_after.splitlines(keepends=True),
                                                   fromfile='STATE.before', tofile='STATE.after')))
text(OUT / 'LOG.append.md', LOG.read_bytes()[len((OPEN / 'LOG.md.before').read_bytes()):].decode('utf-8'))

status = subprocess.run(['git', 'status', '--short', '-uno'], cwd=ROOT, capture_output=True)
text(OUT / 'git-status.txt', status.stdout.decode('utf-8', errors='replace') + status.stderr.decode('utf-8', errors='replace'))
old_paths = {str((ROOT / rel).resolve()) for rel in baseline['old_t033_files']}
# The opening writer itself was created just before it captured this baseline.
# Keep its pin check, and explicitly include it in the session file set.
old_paths.discard(str((ROOT / 'results/T-033/scripts/session8_open.py').resolve()))
new_paths = [path for path in (ROOT / 'results/T-033').rglob('*')
             if path.is_file() and str(path.resolve()) not in old_paths]
write(OUT / 'scope-verification.json', {
    'status': 'PASS', 'at': STAMP, 'old_result_files_unchanged': len(baseline['old_t033_files']),
    'protected_files_unchanged': list(baseline['protected']), 'LOG_append_only': True,
    'STATE_changed_rows': ['T-033'], 'other_STATE_lines_unchanged': True,
    'new_result_files': sorted([str(path.relative_to(ROOT)).replace('\\', '/') for path in new_paths] +
                              [str((OUT / 'scope-verification.json').relative_to(ROOT)).replace('\\', '/'),
                               str((OUT / 'manifest.json').relative_to(ROOT)).replace('\\', '/')]),
    'opening_writer_created_before_baseline': 'results/T-033/scripts/session8_open.py',
    'allowed_mutations': ['results/T-033/ new files', LOG_REL + ' append only', STATE_REL + ' T-033 row only'],
    'scientific_compute_location': 'EC2 only; laptop checkpoint metadata and saved result reading',
    'committed': False, 'pushed': False, 'deleted_additional_files': False,
    'task_complete': False, 'final_result_reports': 'OPEN'
})
new_paths = [path for path in (ROOT / 'results/T-033').rglob('*')
             if path.is_file() and str(path.resolve()) not in old_paths]
manifest = {str(path.relative_to(ROOT)).replace('\\', '/'): meta(path) for path in new_paths}
manifest[LOG_REL] = meta(LOG)
manifest[STATE_REL] = meta(STATE)
write(OUT / 'manifest.json', {
    'files': manifest,
    'historical_snapshot_for_mutable_paths': {LOG_REL: str((OUT / 'LOG.md.after').relative_to(ROOT)).replace('\\', '/'),
                                             STATE_REL: str((OUT / 'STATE.md.after').relative_to(ROOT)).replace('\\', '/')},
    'scope_file_covers_manifest_except_manifest_itself': True
})
assert all(meta(ROOT / rel) == pin for rel, pin in manifest.items())
assert all(meta(ROOT / rel) == pin for rel, pin in baseline['old_t033_files'].items())
assert all(meta(ROOT / rel) == pin for rel, pin in baseline['protected'].items())
print(json.dumps({'status': 'PASS', 'checkpoint': str(OUT.relative_to(ROOT)), 'manifest_files': len(manifest),
                  'old_files_unchanged': len(baseline['old_t033_files']), 'timers': len(charges),
                  'new_processing_charged_s': new_charged, 'remaining_approved_s': remaining,
                  'logical_bytes': final_preflight['logical_bytes'], 'workers': [], 'task_complete': False}, ensure_ascii=False))
