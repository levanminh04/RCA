"""Chốt tài liệu và quyền bàn giao; chỉ xử lý metadata trên laptop."""
import ast
import difflib
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[3]
home = root / 'results/T-033'
task = root / 'tasks/T-033-g2-nguyen-nhan-phat-hien'
run = home / 'runs/checkpoint-handoff-001'
art = run / 'artifacts'
baseline = home / 'runs/handoff-open-001'


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(2**20), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_new(path, content):
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(content)


snapshot = read(run / 'snapshot.json')
receive = read(run / 'receive-status.json')
inventory = read(run / 'artifact-inventory.json')
assert receive['status'] == 'PASS' and receive['archive_sha256'] == snapshot['archive']['sha256']
assert set(read(run / 'received-files.json')) == set(inventory)
for relative, info in inventory.items():
    path = (art / relative).resolve()
    assert art.resolve() in path.parents
    assert path.stat().st_size == info['bytes'] and sha(path) == info['sha256'], relative
source = read(art / 'inputs/source.json')
assert sha(art / 'inputs/source.json') == sha(home / 'runs/prepare-001/inputs/source.json')
native_manifest = {}
for name, expected in dict(source['native_hash'], **{'phat_hien.py': source['adapter_sha256']}).items():
    path = run / 'source-native' / name
    assert sha(path) == expected, name
    native_manifest[name] = {'sha256': expected, 'bytes': path.stat().st_size}
write_new(run / 'native-source-manifest.json', json.dumps(native_manifest, indent=2))
audit = read(art / 'runs/core-audit-002/verification.json')
assert audit['status'] == 'PASS' and audit['core_records'] == 120
statuses = snapshot['statuses']
assert statuses['bocpd-factorial-rest-001']['status'] == 'PASS'

locator = {'root': 'artifacts/', 'core': audit['rows'], 'FF': [], 'factorial': [], 'fixed': []}
for path in sorted((art / 'runs').glob('*/dev-*--FF-check.json')):
    locator['FF'].append({'record': path.relative_to(art).as_posix()})
for oid, case in statuses['bocpd-factorial-rest-001']['cases'].items():
    for branch, entry in case['branches'].items():
        relative = entry.get('reused_record', 'runs/bocpd-factorial-rest-001/' + oid + '--' + branch + '.json')
        record = read(art / relative)
        locator['factorial'].append({'opaque_id': oid, 'branch': branch, 'record': relative,
                                     'npz': (Path(relative).parent / record['npz']).as_posix(),
                                     'sha256': record['sha256'], 'checks': record['checks']})
for name in ['nsigma-frozen-first-001', 'nsigma-frozen-rest-001']:
    for oid, case in statuses[name]['cases'].items():
        for branch, entry in case.items():
            locator['fixed'].append({'opaque_id': oid, 'detector': branch,
                                     'record': 'runs/' + name + '/' + entry['record'],
                                     'npz': 'runs/' + name + '/' + entry['output_npz'],
                                     'sha256': entry['sha256'], 'checks': entry['checks']})
assert len(locator['core']) == 120 and len(locator['factorial']) == len(locator['fixed']) == 60
write_new(run / 'artifact-locator.json', json.dumps(locator, ensure_ascii=False, indent=2))

output_names = ['nguyen-nhan-phat-hien.md', 'chuoi-bang-chung.json', 'bao-phu-nhom.json',
                'phan-ra-tien-xu-ly.json', 'do-tre-sau-moc.json', 'nsigma-nguong-co-dinh.json',
                'nsigma-trung-gian', 'bocpd-trung-gian', 'doi-chieu.json', 'tai-log.json',
                'doc-tay.md', 'kiem-tiep.md']
output_presence = {name: (home / name).exists() for name in output_names}
write_new(run / 'output-presence.json', json.dumps({'task_complete': False,
           'note': 'Existence of top-level outputs only; arrays/branch records are in artifacts/runs. Presence is not completion.',
           'outputs': output_presence}, ensure_ascii=False, indent=2))

now = datetime.now(timezone(timedelta(hours=7))).isoformat()
readme = f'''# T-033 — Checkpoint hiện trạng để Claude kiểm độc lập

Chốt ngày {now}. Task đang thực hiện, chưa nghiệm thu. Codex là người làm; Claude là người phản biện. Minh yêu cầu chốt đầy đủ hiện trạng để kiểm; chưa duyệt sửa guard hoặc chặng tính tiếp trong lượt này.

## Điểm vào và cách tìm bằng chứng

1. Đọc `AGENTS.md`, `tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md`, mục phiên 3 của `LOG.md`, dòng T-033 trong `docs/STATE.md`.
2. Đối chiếu mục tiêu RQ2/P4 trong `docs/MRP.md`, DT18 §2 NV2/NV3, advisor-2026-09-23.md §1 và các nguồn lý do/quyết định trực tiếp. File chỉ mục không thay đọc các nguồn đó.
3. `snapshot.json`: trạng thái EC2 cuối, `/statuses`, `/manifests_verified`, `/factorial_reuse`, `/run_durations_from_status`, `/resources`. `artifact-inventory.json`: SHA và byte từng file gốc trong gói. `receive-status.json`: hash toàn archive khi truyền, trạng thái nhận. `local-verification.json`: kiểm lại file trên laptop và phạm vi ghi.
4. `artifact-locator.json`: tìm record/NPZ theo ca và nhánh; các đường dẫn trong locator tính từ `artifacts/`. `artifacts/` là bản nhận nguyên file EC2, không sửa số hoặc đường dẫn bên trong. Một số record mang đường dẫn EC2, dùng locator để tìm bản cùng SHA trong checkpoint.
5. `source-native/` chứa code native/adapter đúng hash input nguồn; `native-source-manifest.json` khóa SHA. Dùng để đọc, không thay môi trường triển khai. `artifacts/scripts/` là script từng chạy trên EC2; `results/T-033/scripts/` có thêm script chuẩn bị chưa chạy. Các snapshot script lịch sử trong `artifacts/runs/prepare-001/` vẫn giữ.
6. Prompt trung tính theo mẫu ở `prompt-claude.md`, cũng được chép trong LOG phiên 3. Phạm vi hiện tại: chỉ đọc và trả lời trong chat; chưa cấp quyền ghi REVIEW. Thư mục task được liệt kê trước chốt và chưa có REVIEW.

## Trạng thái các chặng — FACT từ file

| Chặng | Bằng chứng hiện có | Phần chưa làm |
|---|---|---|
| Chuẩn bị | Source/allowlist/env/index và nhóm ban đầu: `artifacts/runs/preflight-002/`, `artifacts/inputs/`; `results/T-033/bao-phu-nhom.json` | Độ phủ đọc tay thực tế và nhóm bổ sung sau factorial |
| N-Sigma lõi | Hai bộ cột, 60 record; `artifacts/runs/nsigma-first-001/`, `nsigma-rest-001/`; mean/std/count/flags và nguồn đã tự kiểm | Diễn giải ca/điểm có đối chứng |
| BOCPD lõi | Full và PP của 30 ca, FF kiểm prefix; `bocpd-first-001`, `full-metadata-recheck-001`, `bocpd-first-002`, `bocpd-rest-001`; tự kiểm chung `core-audit-002/verification.json` gồm 120 record N-Sigma/BOCPD | Phân tích đường likelihood/posterior/MAP tới báo sau proxy |
| FP/PF | Pilot và rest đều PASS; 30 ca × 2 hybrid, có 29 ca mới và tái dùng pilot. Rest kết thúc 10:27:24 ngày 10/10 +07, exit 0; `artifacts/runs/bocpd-factorial-rest-001/status.json`, manifest và `*--factorial.json` | Diễn giải các contrasts, khóa nhóm/đối chứng mới và chuỗi tính tay |
| N-Sigma nền cố định | Pilot/rest đủ 60 đơn vị; thống kê được đối chiếu độc lập từ Series gốc; `artifacts/runs/nsigma-frozen-*/` | Diễn giải nguyên nhân chênh ngưỡng theo ca/điểm |
| Độ trễ/kênh/đọc tay | Có trung gian lõi và script chuẩn bị; chưa có run delay/channel | Phần độ trễ, mật độ/chuỗi cờ, trace/log/workload, đọc tay/đối chứng theo SPEC |
| Tổng hợp | Checkpoint kỹ thuật hiện trạng | Báo cáo năm đầu ra P4, căn cứ P6, kiểm tiếp và nghiệm thu |

Các trạng thái PASS trên là kết quả tự kiểm phát lại, driver và manifest. Câu hỏi cơ chế, nguồn vật lý, quyết định P6 và G2 vẫn OPEN. `output-presence.json` liệt kê từng đầu ra SPEC đã/chưa tồn tại ở cấp gốc; không tạo báo cáo nghiên cứu để giả hoàn tất task.

## Lượt lỗi và con trỏ tái dùng

- `bocpd-first-001` STOPPED vì metadata cột wrapper; nguyên trung gian giữ lại. `full-metadata-recheck-001` kiểm hash và dựng metadata đúng từ nguyên R/maxes; `bocpd-first-002` dùng full đã xác minh, không viết lại lượt lỗi. Đọc record và LOG để phân biệt schema với số/CP.
- `core-audit-001` STOPPED do giải nén ma trận predictive trong vòng lặp; giữ stdout/stderr/progress. `core-audit-002` đưa đọc array ra ngoài loop, giữ assert, PASS. Không chạy lại detector trong phép tự kiểm này.
- Hai branch của ca pilot trong factorial rest có `reused_record`; NPZ nằm trong `bocpd-factorial-first-001`, không phải rest. `artifact-locator.json#/factorial` nối đúng record/NPZ này.
- `bao-phu-nhom.json` hiện chỉ khóa nhóm ban đầu; trạng thái NOT_YET_REPLAYED_OR_READ trong bảng là lịch sử khóa, chưa được cập nhật thành bằng chứng cơ chế.

## Guard và ngân sách — OPEN

SPEC dòng 195 dự trù 4–12 giờ máy và ghi "Đây không là timeout". Guard Codex cài lấy thời gian lịch từ `nsigma-first-001/status.json#/started_utc`, gồm khoảng nghỉ, thành hạn 11:46:29 ngày 10/10 +07. Mốc này không phải thời hạn Minh đặt và không chứng minh đã dùng hết giờ xử lý. Các câu trong LOG phiên 1/2 gọi đây là giới hạn đã duyệt được đính chính bởi phiên 3; lịch sử không bị sửa.

Đề xuất chuyển sang tổng thời gian các lượt xử lý, tính cả lượt hỏng/kiểm, giữ trần 12 giờ và 4 GiB: CANDIDATE, chưa Minh duyệt. Code và input budget chưa đổi. `/sum_available_run_wall_s` trong snapshot chỉ là tổng wall của các run có status; có phần chạy song song, chưa bao quát mọi audit/preflight/khoảng EC2 chờ và không là hóa đơn AWS. Chưa dùng nó để cấp giờ còn lại hoặc khởi run.

Đóng gói tạo thêm archive EC2 và bản nhận laptop; nhận trực tiếp không giữ archive thứ hai trên laptop. `local-verification.json#/storage` ghi dung lượng thực tế cả hai nơi sau chốt. Giữ archive/lượt cũ; nếu phần tiếp theo làm vượt 4 GiB thì checkpoint và trình Minh, không tự xóa hoặc nới giới hạn. Guard thời gian hiện chưa sửa.

## EC2 và cách kiểm lại chỉ đọc

Không còn worker T-033 hoặc tmux session T-033; lô cuối đã PASS trước mốc guard. EC2 vẫn bật, chưa tự tắt. Bản gói đầy đủ đã có trên laptop để Claude kiểm code/metadata/trung gian; nguồn dữ liệu dev và môi trường tính vẫn ở EC2. Task còn cần EC2 nếu tiếp các chặng chưa làm. Minh có thể tắt laptop sau khi nhận xong; chưa có công việc nghiên cứu mới chạy nền.

```powershell
ssh -i D:/RCA-ext/keys/keys.pem -o UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts -o StrictHostKeyChecking=yes -o BatchMode=yes ubuntu@3.107.246.249 'cat ~/rca/T-033/runs/bocpd-factorial-rest-001.exit; tail -n 20 ~/rca/T-033/trang-thai.txt'
```

Nguồn được phép: allowlist trong `artifacts/inputs/source.json`; raw dev tại `/home/ubuntu/rca/T-025/repo/data/rcaeval/`. Code native tại `/home/ubuntu/rca/T-025/src/baro`, adapter tại `/home/ubuntu/rca/T-025/repo/src/p3/`; Python `/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8`, NumPy 1.26.4, pandas 2.2.3. Đọc version/provenance trong `artifacts/runs/preflight-002/environment.json` và từng status. Laptop chỉ xử lý tài liệu/metadata/nhận file; tính toán nghiên cứu trên EC2. Không thực nghiệm mới, không nguồn khóa/test/giữ ngoài, không vùng kết quả T-032, không sửa nguồn cũ.

## Sau lượt kiểm hiện trạng

Minh chuyển prompt thủ công cho Claude; Claude trả lời trong chat nếu chưa có quyền REVIEW riêng. Codex giữ vai trò người làm, nhận các nhận xét để kiểm và trình phương án. Chỉ tiếp nghiên cứu/sửa guard theo quyền Minh quyết; không tự coi yêu cầu chốt checkpoint là duyệt đề xuất trước đó. Chưa nghiệm thu T-033 hoặc đóng RQ2/G2.
'''
write_new(run / 'README.md', readme)

template = (root / 'docs/review-prompt.md').read_text(encoding='utf-8')


def block(header):
    return template.split(header + '\n', 1)[1].split('```text\n', 1)[1].split('\n```', 1)[0]


common = block('## Prompt chung')
replacements = {
    '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>': 'T-033 — tasks/T-033-g2-nguyen-nhan-phat-hien/',
    '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>': 'soát kết quả',
    '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>': 'P4 / G2',
    '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>': 'Codex là người làm; Claude là người phản biện chính thức theo SPEC',
    '<danh sách đường dẫn và git diff từ commit gốc nếu có>': 'AGENTS.md; docs/STATE.md; tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md và LOG.md; results/T-033/runs/checkpoint-handoff-001/README.md; phần trực tiếp chi phối của docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; diff phạm vi tại results/T-033/runs/checkpoint-handoff-001/own-diff.txt',
    '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>': 'Không có bản REVIEW trên file trong thư mục task tại lần liệt kê để chốt checkpoint',
    '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>': 'results/T-033/scripts/; results/T-033/runs/checkpoint-handoff-001/artifacts/; artifact-inventory.json, artifact-locator.json và native-source-manifest.json trong cùng checkpoint; source-native/ trong checkpoint; src/p3/; results/T-025/ và results/T-029/ theo manifest nguồn; BARO revision e35f4ec; results/T-031/moi-truong.json; môi trường và lệnh EC2 chỉ đọc theo README của checkpoint',
    '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>': 'Chỉ đọc và trả lời trong chat; không sửa file',
}
for key, value in replacements.items():
    assert common.count(key) == 1, key
    common = common.replace(key, value)
prompt = common + '\n\n' + block('### Soát kết quả') + '\n\n' + block('### G2 — Baseline và phân tích hạn chế') + '\n'
assert all(key not in prompt for key in replacements)
write_new(run / 'prompt-claude.md', prompt)

ast_checks = {}
for directory in [home / 'scripts', art / 'scripts', run / 'source-native']:
    for path in directory.glob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        ast_checks[path.relative_to(home).as_posix()] = True

for name in ['AGENTS.md', 'docs/review-prompt.md', 'tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md']:
    assert (root / name).read_bytes() == (baseline / name).read_bytes(), name
read_only_docs = {name: {'sha256_at_open': sha(baseline / name), 'sha256_at_close': sha(root / name),
                         'written_by_this_checkpoint': False}
                  for name in ['docs/WHY.md', 'docs/DECISIONS.md']}

# Re-read immediately before editing only T-033.
state = root / 'docs/STATE.md'
state_before = state.read_bytes()
write_new(run / 'STATE.md.before-close', state_before.decode('utf-8'))
lines = state_before.splitlines(keepends=True)
indexes = [i for i, line in enumerate(lines) if line.startswith(b'| T-033 |')]
assert len(indexes) == 1
i = indexes[0]
parts = lines[i].decode('utf-8').split('|')
parts[6] = ' Đang thực hiện: lõi và nền cố định đạt; FP/PF đủ 30 ca PASS, không còn worker. Đã chốt checkpoint-handoff-001 để Claude kiểm hiện trạng; guard chờ Minh quyết. Chưa độ trễ/kênh/đọc tay/tổng hợp, chưa nghiệm thu '
lines[i] = '|'.join(parts).encode('utf-8')
state.write_bytes(b''.join(lines))
assert [l for l in state_before.splitlines(keepends=True) if not l.startswith(b'| T-033 |')] == [l for l in state.read_bytes().splitlines(keepends=True) if not l.startswith(b'| T-033 |')]

log = task / 'LOG.md'
log_before = log.read_bytes()
entry = f'''

### Kết thúc phiên 3 — checkpoint hiện trạng mới nhất — {now}

1. Đã làm: chốt `results/T-033/runs/checkpoint-handoff-001/README.md` để Claude kiểm độc lập. Snapshot EC2 lúc {snapshot['utc']}: FP/PF đủ 30 ca, pilot được tái dùng, kết thúc 10:27:24 ngày 10/10 +07, exit 0; không còn worker/tmux T-033. N-Sigma nền cố định đủ 60 đơn vị; core-audit-002 đã kiểm 120 record lõi. Đóng gói và nhận nguyên {snapshot['payload_files']} file / {snapshot['payload_bytes']} byte, gồm trung gian NPZ, JSON, scripts, stdout/stderr/progress/exit và lượt lỗi; không chạy lại detector hoặc chặng mới.
2. File thay đổi: scripts/checkpoint mới trong `results/T-033/`; LOG chỉ nối; chỉ ô trạng thái dòng T-033 STATE. SPEC/AGENTS/review-prompt giữ nguyên; WHY/DECISIONS không được phiên này ghi. Code/data/env nguồn cũ chỉ đọc; nhận bốn file native/adapter làm bản đọc cùng hash. Không test/locked/heldout, không vùng kết quả T-032, không commit/push, không bật/tắt EC2. Yêu cầu chốt hiện trạng không được coi là duyệt sửa guard.
3. Kiểm: toàn bộ {len(snapshot['manifests_verified'])} manifest/lô và logs trên EC2 khớp; nguyên {len(inventory)} file nhận cùng SHA/byte với inventory; hash toàn tar stream khớp hai đầu; bốn code native/adapter khớp nguồn pin; con trỏ tái dùng pilot được kiểm; AST code đạt. `artifact-locator.json` chỉ mục core/FF/hybrid/fixed, `output-presence.json` ghi đầu ra còn thiếu. Kiểm phạm vi/diff và hash tài liệu ở `local-verification.json`, `own-diff.txt`, `handoff-manifest.json`. Prompt soát kết quả bên dưới chép nguyên văn Prompt chung + Soát kết quả + G2, chỉ điền trường trung tính.
4. OPEN: T-033 chưa hoàn tất, chưa có kết luận cơ chế hoặc căn cứ nghiệm thu RQ2/P4/G2/P6. Còn độ trễ/mật độ/chuỗi cờ, trace/log/workload, khóa nhóm mới, đọc tay/đối chứng, tổng hợp/kiểm tiếp. Guard lịch 12 giờ là cách cài của Codex; mốc 11:46 không phải thời hạn Minh đặt. Đính chính các câu LOG trước coi là giới hạn đã duyệt; đề xuất tính giờ xử lý cộng dồn còn CANDIDATE, chưa sửa hoặc Minh duyệt. `/run_durations_from_status` chỉ là thời gian các run có status, không phải số giờ AWS/đủ tổng mọi bước. Dung lượng gồm archive EC2 và bản nhận được kiểm theo `/storage` của local-verification; còn cần cân lại trước chạy tiếp, không tự xóa/archive cũ hoặc tăng trần.

EC2: mọi lô T-033 hiện đã kết thúc; chưa có tiến trình mới. Minh có thể tắt laptop sau chốt. Giữ EC2 nếu Claude cần môi trường/raw dev để kiểm sâu hoặc Minh cho tiếp chặng chưa làm. Bản nhận đủ code/trung gian hiện có trên laptop; không cần giữ worker cũ. Không tự tắt EC2, task vẫn còn phần cần máy.

Bước tiếp theo chính xác: Minh mở Claude và copy `results/T-033/runs/checkpoint-handoff-001/prompt-claude.md`, hoặc khối dưới đây. Claude đọc README/manifest/locator rồi đầu ra/code/nguồn gốc, trả lời trong chat; chưa cấp quyền REVIEW riêng và không tự chạy thực nghiệm mới. Codex giữ vai người làm, sau đó kiểm nhận xét và trình Minh xử lý. Nếu Minh cho tiếp, trước hết giải quyết ngân sách/guard theo quyền được duyệt, kiểm nguồn/hash, không làm lại đơn vị PASS. Lệnh chỉ đọc EC2 và path môi trường nằm trong README.

Lệnh cuối chốt phiên: `Python -B -X utf8 results/T-033/scripts/finalize_handoff.py` trên laptop (chỉ hash/metadata/AST/tài liệu). Lệnh EC2 đóng gói: `T033_HOME=/home/ubuntu/rca/T-033 ... python -B -X utf8 .../scripts/package_handoff.py`; sau đó receiver dùng SSH `cat .../artifacts.tar` để nhận trực tiếp, không giữ archive thứ hai trên laptop. Lệnh kiểm tiến độ gốc: SSH `tail -n 20 ~/rca/T-033/trang-thai.txt`. Không khởi run mới.

### Prompt Claude kiểm hiện trạng T-033 — Minh chuyển thủ công

```text
{prompt.rstrip()}
```
'''
with log.open('ab') as handle:
    handle.write(entry.encode('utf-8'))
assert log.read_bytes().startswith(log_before)
assert log.read_bytes().startswith((baseline / 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md').read_bytes())
diff = []
for label, before, after in [('STATE: only T033 close', state_before, state.read_bytes()),
                            ('LOG: checkpoint session', (baseline / 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md').read_bytes(), log.read_bytes())]:
    diff.extend(difflib.unified_diff(before.decode('utf-8').splitlines(True), after.decode('utf-8').splitlines(True),
                                    fromfile=label + ' before', tofile=label + ' after'))
write_new(run / 'own-diff.txt', ''.join(diff))

local_bytes = sum(p.stat().st_size for p in home.rglob('*') if p.is_file())
remote_bytes = snapshot['resources']['new_bytes_including_archive'] + (run / 'snapshot.json').stat().st_size + (run / 'artifact-inventory.json').stat().st_size + 1024
assert remote_bytes + local_bytes + 2 * 2**20 < 4 * 2**30
verification = {'status': 'PASS', 'utc': now, 'payload_files_verified': len(inventory),
                'payload_bytes': snapshot['payload_bytes'], 'archive_stream_SHA_match': True,
                'native_source_SHA_match': True, 'core_audit_records': 120,
                'factorial_records': len(locator['factorial']), 'fixed_records': len(locator['fixed']),
                'STATE_only_T033': True, 'LOG_append_only': True, 'SPEC_unchanged': True,
                'AGENTS_unchanged': True, 'prompt_template_unchanged': True,
                'read_only_documents': read_only_docs, 'script_AST': ast_checks,
                'task_complete': False, 'research_questions_closed': False, 'guard_changed': False,
                'storage': {'local_results_bytes': local_bytes, 'remote_bytes_estimate_with_metadata': remote_bytes,
                            'combined_bytes_estimate': remote_bytes + local_bytes,
                            'limit_bytes': 4 * 2**30, 'archive_kept_on_EC2': True,
                            'local_archive_copy': False}}
write_new(run / 'local-verification.json', json.dumps(verification, ensure_ascii=False, indent=2))
handoff_manifest = {p.relative_to(run).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
                    for p in run.rglob('*') if p.is_file() and art not in p.parents and p.name != 'handoff-manifest.json'}
handoff_manifest['external-documents'] = {p.relative_to(root).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
                                        for p in [log, state, task / 'SPEC.md']}
write_new(run / 'handoff-manifest.json', json.dumps(handoff_manifest, ensure_ascii=False, indent=2))
print(json.dumps({k: verification[k] for k in ['status', 'payload_files_verified', 'factorial_records',
                  'fixed_records', 'task_complete', 'guard_changed', 'storage']}))
