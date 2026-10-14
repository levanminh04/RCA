"""Append handoff prose and verbatim review templates; no experiment execution."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LOG = REPO / 'tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md'
template = (REPO / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')

def block(heading):
    section = template.split(heading + '\n', 1)[1]
    match = re.search(r'```text\n(.*?)\n```', section, re.S)
    assert match
    return match.group(1)

common = block('## Prompt chung')
result_block = block('### Soát kết quả')
spec_block = block('### Soát SPEC')
gate = block('### G2 — Baseline và phân tích hạn chế')
slots = re.findall(r'<[^<>]+>', common)
assert len(slots) == 8

def prompt(values, stage):
    assert len(values) == 8
    value = common
    for key, item in zip(slots, values):
        value = value.replace(key, item, 1)
    assert not re.search(r'<[^<>]+>', value)
    return value + '\n\n' + stage + '\n\n' + gate

repair = prompt([
    'T-032, tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md; lượt sửa bộ kiểm theo results/T-032/de-xuat-microrank-bridge-003.md',
    'soát kết quả của lượt sửa bộ kiểm',
    'P4, G2',
    'Codex người làm, Claude người phản biện theo SPEC',
    'tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md; results/T-032/de-xuat-microrank-bridge-003.md; results/T-028/runs/phan-hoi-review-001/manifest.json và scripts-final/tong_hop_bao_cao.py; nguồn được các manifest T-024/T-026/T-028/T-029 dẫn',
    'không có bản phản biện chính thức cho kết quả lượt sửa này; lịch sử đề xuất và thực hiện ở LOG của T-032',
    'results/T-032/scripts/check_microrank_t028_v3.py, replay_microrank_approved_v3.py, audit_microrank_posthoc_v3.py, batch_microrank_approved_v3.py; các bản trước cùng thư mục; results/T-032/scripts/compare_microrank_roundoff.py; results/T-032/runs/tiep-tuc-003/bridge003-transfer.json, bridge003-transfer-check.json, bridge003-repair-check.json; results/T-032/runs/thu-ec2-003/microrank-t028-fixture-005-monitor/, microrank-re2-posthoc-002/ và microrank-re2-posthoc-002-monitor/; môi trường/revision và invocation tại các file lượt, LOG và results/T-031/moi-truong.json',
    'chỉ đọc và trả lời trong chat; Minh chọn gửi prompt; chưa có quyền tạo bản REVIEW hay chạy thực nghiệm',
], result_block)
proposal = prompt([
    'T-032, đề xuất results/T-032/de-xuat-microrank-laptop-001.md và tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md',
    'soát SPEC của đề xuất chẩn đoán',
    'đề xuất bổ sung của P4, G2',
    'Codex người làm, Claude người phản biện theo SPEC; vai trò này giữ cho đề xuất bổ sung',
    'results/T-032/de-xuat-microrank-laptop-001.md; tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md; results/T-032/de-xuat-microrank-001.md; results/T-031/moi-truong.json; các nguồn T-024/T-026/T-028/T-029 được SPEC dẫn',
    'không có bản phản biện chính thức của đề xuất này',
    'results/T-032/runs/microrank-cohort-failure-001/transport-check.json, cohort/52-cases.json, failed-case/check.json, failed-case/roundoff-comparison.json, failed-case/native-observed-exact.json; results/T-032/scripts/replay_microrank_approved_v3.py, batch_microrank_approved_v3.py và compare_microrank_roundoff.py; revision/môi trường/lệnh nguồn tại results/T-031/moi-truong.json và invocation của lượt',
    'chỉ đọc và trả lời trong chat; chưa có quyền chạy chẩn đoán hoặc sửa SPEC/code/WHY/DECISIONS',
], spec_block)

marker = '### Kết thúc phiên 3 — checkpoint bàn giao 10/10/2026, 11:31 (+07)'
assert marker not in LOG.read_text(encoding='utf-8-sig'), 'Do not append duplicate session ending'
ending = r'''

### Kết thúc phiên 3 — checkpoint bàn giao 10/10/2026, 11:31 (+07)

1. **Đã làm:** hoàn tất bridge-003 theo Minh duyệt và nối đúng Q-96 sau đọc lại DECISIONS. Kiểm sửa đạt; benchmark MicroRank Nezha đạt rồi lập dự toán/khởi cohort riêng theo quyền ngoại lệ. Cohort đã tự dừng đúng ngưỡng, không chạy tiếp trên ca lỗi. Đã thu 15 tệp control/verdict với hash trước/sau remote và local PASS; lập `runs/microrank-cohort-failure-001/comparison-summary.json` và bảng `52-cases.md`, không giả kết quả cho ca chưa chạy. BARO/coverage/SimpleRCA đủ phạm vi kiểm phát lại; chưa gọi đây là kết luận cơ chế.
2. **File thay đổi trong phiên:** bốn script bridge/wrapper/audit/controller v3 ở `results/T-032/scripts/`; script/đầu ra chuẩn bị và kiểm CIRCA (gồm replay_circa_v2.py, check_circa_source_bytes.py, source-closure/inventory/historical snapshot); wrapper/audit/controller và output kiểm SimpleRCA; các output BARO/coverage/transport và MicroRank ở các thư mục lượt T-032 đã liệt kê trong LOG. Checkpoint cuối tạo `collect_microrank_failure_001.ps1`, `write_microrank_failure_summary_001.py`, script nối prompt này, `runs/microrank-cohort-failure-001/` và `de-xuat-microrank-laptop-001.md`. Docs: đã nối Q-95/Q-96 đúng lời duyệt vào DECISIONS, nối WHY-42 đúng đoạn Minh duyệt trước đó, chỉ sửa dòng T-032 của STATE; LOG chỉ nối. Giữ SPEC thiết kế/code chung/baseline/nguồn/dữ liệu và mọi lượt cũ; không commit/push. Không truy cập T-033 trong công việc T-032 này.
3. **Kiểm và kết quả:** bridge-003 có 14 fixture và self-check đủ 52 hàng frozen PASS; audit RE2 đã lưu PASS, tổng 20,729 giây và dưới trần 15 MiB. Frozen-only không cấp eligibility cho ca chưa phát lại. MicroRank Nezha pilot exact, 69 artifact local khớp manifest; SimpleRCA status toàn 52 PASS đã kiểm hash hai đầu, full trung gian còn EC2. CIRCA source utility PASS 120/120 byte hash cùng historical snapshot; local `runs/circa-source-001/remote-byte-check-001.json` khớp SHA remote, source counts không missing/drift. Historical launcher được tái dựng đúng byte hash, không tìm thấy artifact lịch sử; utility không chạy launcher/method. Wrapper CIRCA v2 mới đã đọc diff/pin/AST nhưng chưa chuyển/fixture/import/native/pilot. Metadata bảng MicroRank đủ 30 RE2 +22 Nezha, không trùng ca; khớp mọi count. RE2: exact2 (ERROR, không có score pairs), numeric_only5, operation_order2, blocked1, not_run20. Nezha: exact1, not_run21. Ca lỗi max41 ULP/relative4,731118408006869e-15, 107 điểm operation và19 điểm service vượt ngưỡng; service order/ties/Hit và native–observed exact, T-028 flags NOT_PERFORMED vì dừng trước bridge. Không gọi guard lỗi tài nguyên. Kiểm metadata kiểm lại hash 15 tệp PASS; chưa thu all artifact/full capture của cohort về laptop.
4. **Còn mở/cần Minh:** chưa xác định thành phần môi trường gây drift, membership lịch sử hoặc cơ chế caller/root. MicroRank và A′ bị chặn; không tăng ngưỡng. Đề xuất chẩn đoán laptop riêng tại `de-xuat-microrank-laptop-001.md` đã trình, chưa duyệt/chưa chạy/chưa nối Q-97. Nếu dữ kiện mới thay phần bằng chứng của WHY-42, phải trình đoạn bổ sung và chờ Minh duyệt; không tự sửa WHY cũ. CIRCA/TORAI/TraceRCA và khóa đối chứng/đọc tay còn thiếu nên task vẫn đang thực hiện, chưa chuyển chờ phản biện toàn task, chưa nghiệm thu P4/G2 hoặc cơ chế. TraceRCA path chờ lời duyệt riêng. Mọi bước độc lập hợp lệ được tiếp ở phiên sau.

**EC2/laptop:** kiểm trực tiếp khoảng 11:30 (+07), các PID SimpleRCA/source utility/MicroRank/pilot đã kết thúc (ps chỉ còn header); không có worker T-032 của các lượt này chạy. Remote T-032 3.124.362.990 byte, available RAM 7.485.521.920 byte; local reserve 1,6 GB vẫn bao phần đã đo và metadata nhỏ, tổng hiện tại dưới 8 GiB. Remeasure trước output/transfer lớn; không coi reserve là ngân sách cho các nhánh chưa đo. Đã thu bằng chứng/checkpoint xong: Minh có thể tắt laptop, không cần giữ cho lượt đang chạy nào. Thông báo “ổn định” và ETA 12:32 trước đó đã hết hiệu lực do FAIL_STOP; không có ETA hoàn thành cohort mới. EC2 còn cần cho phần T-032 còn lại; chưa đề nghị tắt EC2, không tự bật/tắt.

**Bước tiếp theo chính xác:**

- Đọc AGENTS, riêng dòng T-032 của STATE, SPEC và đoạn cuối LOG này; kiểm `runs/microrank-cohort-failure-001/transport-check.json` và chạy metadata-only `py -3 -B -X utf8 results/T-032/scripts/write_microrank_failure_summary_001.py` để kiểm hash/đếm lại nếu nhận tiếp. Không khởi lại cohort đã FAIL_STOP và không retry ca lỗi.
- Kiểm EC2 chỉ đọc: `ssh -i D:/RCA-ext/keys/key2.pem -o BatchMode=yes -o StrictHostKeyChecking=yes ubuntu@3.26.62.217 "cat ~/rca/T-032/runs/microrank-approved-cohort-001-monitor/status.json; cat ~/rca/T-032/runs/microrank-approved-cohort-001/status.json"`. Tail stdout chỉ xem lịch sử, không là lượt còn chạy. PID/command/stdout/stderr/progress đầy đủ trong control đã thu.
- Nếu Minh duyệt laptop: đọc đúng đề xuất, đọc lại DECISIONS rồi nối đúng một dòng mới đã duyệt; dựng wrapper/launcher mới, soát code/hash/môi trường/RAM trước một native; chỉ native exact mới một observed. Chưa có quyền thì giữ phần này dừng. Không tự dùng các script EC2 có đường dẫn hard-coded trên laptop.
- Phần độc lập: CIRCA đọc `scripts/capture_circa.py`, `replay_circa_v2.py` và `runs/circa-source-001/{source-closure,source-inventory,remote-byte-check-001}.json`; transfer wrapper được SPEC cho phép phải có inventory/hash hai đầu, rồi fixture mới trước actual imports/native/pilot. Giữ exact CIRCA, không dùng ngoại lệ MicroRank. Chưa có lệnh native/CIRCA nào khởi ở checkpoint này; không đoán CLI trước đọc script.
- Đo lại global bytes/RAM trước export full SimpleRCA/MicroRank hoặc lượt dài mới; nguồn export closed chạy `export_verified_outputs.py` theo CLI thực trong script, kiểm all inventory hashes trước dùng. Kiểm hash năm metadata `runs/groups-003` trước khóa cặp/đọc tay. TORAI còn lấy trung gian; TraceRCA sửa path phải đợi duyệt riêng. Chỉ sau lõi/nhóm/kiểm J0 đúng điều kiện mới xét A′.

**Lệnh kiểm EC2 cuối đã chạy:** `ssh -i D:/RCA-ext/keys/key2.pem -o BatchMode=yes -o StrictHostKeyChecking=yes ubuntu@3.26.62.217 'ps -o pid,ppid,stat,args -p 141782,141784,145488,145490,145642,145644,146055,144059,144061; free -b; du -sb ~/rca/T-032/'` — exit0, các PID không còn, số tài nguyên ghi trên. Sau nối checkpoint sẽ kiểm diff/phạm vi lần cuối và ghi kết quả ngay dưới.

**Đề xuất nội dung commit khi Minh muốn lưu checkpoint:** `T-032: kiểm bridge MicroRank và ghi checkpoint phát lại dev`. Đây chỉ là đề xuất, chưa commit/push.

### Prompt để Minh chuyển Claude — soát kết quả lượt sửa bộ kiểm

Prompt dưới đây theo nguyên văn Prompt chung + Soát kết quả + G2. Minh chọn chuyển; không tự mở/gửi phiên. Không phải prompt nghiệm thu toàn T-032.

```text
'''
ending += repair + '\n```\n\n### Prompt để Minh chuyển Claude — soát đề xuất chẩn đoán\n\nPrompt theo nguyên văn Prompt chung + Soát SPEC + G2; quyền thực hiện vẫn chờ Minh.\n\n```text\n' + proposal + '\n```\n'
with LOG.open('a', encoding='utf-8', newline='') as stream:
    stream.write(ending)
print('APPENDED checkpoint and two neutral prompts; original template bodies preserved')
