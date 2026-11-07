"""Update only the approved preparation documents, preserving append-only records."""
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
TASK = ROOT / 'tasks/T-054-khoa-g3-chay-p7-a'


def write(path, text, create=False):
    with path.open('x' if create else 'w', encoding='utf-8', newline='') as out:
        out.write(text.strip()+'\n')


def main():
    checks = json.loads((RUN/'candidate-validation.json').read_bytes())
    assert checks['PASS'] and checks['jobs']==1640
    for host in ('ec2_1','ec2_2'):
        current = json.loads((RUN/(host+'-fixture-current-received.json')).read_bytes())
        assert current['PASS'] and current['checks']==101
    report = '''# Chuẩn bị main 013 — chờ Claude kiểm và Minh duyệt chạy

Minh duyệt chuẩn bị013 và D1–D4/R3 ngày07/11/2026; sau đó duyệt ngoại lệ đúng một phép đối chiếu C-e. Codex là người làm, Claude là người phản biện. Đây là đầu ra chuẩn bị, chưa là nghiệm thu G3, lần chạy test hoặc kết quả nghiên cứu main. Quyền tại `preparation-permission.json` vẫn có g3/test_grant/main_dispatch=false.

## Kế hoạch thực chạy ứng viên

| Máy | Phần việc | Job | C-e thiếu hỗ trợ | Worker tối đa |
|---|---|---:|---:|---:|
| EC2_1, 16.176.181.251 | 30 TT: họ M1, T12, baseline BARO/SimpleRCA/TraceRCA và TORAI B | 448 | 2 | 2 |
| EC2_2, 13.236.44.106 | 30 TT còn lại, cùng các vế trên | 450 | 0 | 1 |
| Laptop | 34 OB và TT CIRCA/MicroRank/TORAI A | 742 | 0 | 2 |

Nguồn: `candidate-validation.json#/hosts`, `/jobs`, `/positions`; vị trí chi tiết trong `placement.json` và `prepared/`. Tổng1.640job+2vị trí C-e thiếu hỗ trợ, không bỏ ca. Trong đó 68slot OB UNSUPPORTED đã khai không gọi lõi; tối đa1.572lần gọi được hỗ trợ. Không dùng bảng35/25/OB của011 để phát013. Hai EC2 cũ giữ nguyên bản sao và nằm ngoài lịch này.

Các tuyến giữ local dùng lại bằng chứng hợp lệ thay vì dựng thêm môi trường. CIRCA/MicroRank và OB đã có tuyến Windows ghim; TORAI A cần ba CSV tác giả và metric, giữ nguồn riêng ở laptop. Việc chuyển chúng sang cloud sẽ cần thêm parity và truyền nguồn, chưa có bằng chứng giảm tổng thời gian. Hai EC2 mới xử lý phần TT nặng. Laptop tối đa2worker theo bằng chứng004; scheduler chỉ phát khi reservation×1,25 cộng reserve vừa RAM. Cả hai EC2 cùng loại máy, 2vCPU; chưa có bằng chứng mọi tải đều nhanh hơn hoặc hai worker luôn tăng tốc.

## Bằng chứng tuyến và sửa lỗi môi trường

`cloud-verification.json#/hosts` lưu15đối chiếu mới trên nguồn DEV đã được cấp. M1 TT chính dùng lại checkpoint012 sau kiểm pin; không chạy lại. Sáu vế C-a0/C-a1/bo-E1/bo-E2/bo-E5/T12-on đã đối chiếu đầu vào và kết quả theo trường phù hợp. C-d3 đọc một seal M1 thật từ012, trả UNSUPPORTED_CYCLIC đúng tham chiếu; ba nhánh DAG/cyclic/no-target vẫn có fixture. BARO, SimpleRCA, TraceRCA nhánh OK và ERROR, TORAI B đủ seed0/1/2 đi qua prep3.12 và method3.8. Các hàng có invocation/result/reference ghim, RSS, wall và maxgap. T12 kiểm world-block/tầng/vùng/cạnh ở đúng tham chiếu, không chỉ kiểm mã thoát.

14/15đối chiếu khớp nghiêm ngặt. C-e của dev-a5cabe5fa7 lệch30trường float, tối đa1ULP; đầu vào chuẩn hóa, thứ tự, nhóm hòa và trường rời rạc khớp. Minh duyệt ngoại lệ đúng phép này. `numeric-parity-Ce-audit.json` và `cloud-verification.json` giữ nguyên trạng thái lúc kiểm; `numeric-parity-Ce-decision.json`, `numeric-parity-Ce-lineage.json` và `parity-disposition.json` ghi quyết định tiếp theo. Không thêm tolerance vào phương pháp hoặc các lượt khác; không gọi toàn bộ15phép là khớp byte.

Các lỗi và sửa tối thiểu được giữ đầy đủ: lượt lớn đầu dừng vì event lặp utc; r2 chỉ chạy phần còn thiếu. TraceRCA trên Linux cần gốc có chữ lowercase rcaeval theo bộ phân loại hiện hành; đổi gốc đóng gói, không sửa code khoa học. TORAI cần bốn file causal-learn đã vá từ cùng revision RCAEval như môi trường gốc; chép vào env013, giữ .pre013. Hai lượt repair chỉ bổ sung Trace ERROR và ba seed TORAI chưa hợp lệ. Pilot/repair có exit1 do bước fixture thiếu metadata dù các job nêu trên đã có seal; lượt fixture riêng sau đó và lượt mã cuối đều đạt. Giữ các output/error/archive cũ, không dùng exit0 của một script để thay đối chiếu.

Mã cuối trên mỗi EC2 đạt101fixture (`ec2_1-fixture-current-received.json`, `ec2_2-fixture-current-received.json`). Gồm quyền run/resume, quyền chấm riêng, hai worker và hàng rào A, nguồn A sai pin/thiếu quyền, lỗi A chưa phân loại dừng phần còn lại, snapshot/A4 và các biên worker/monitor. Nhánh kích hoạt dương dùng cohort sinh giả60TT+34OB, đạt11kiểm ở `fixture-activation-003/summary.json`; không tạo LOCKED hoặc grant cho cohort thật. Hai fixture báo cáo thiếu A và chỉ có một seed A đều tạo89hàng, giữ A4 và không bình quân seed sống (`report-A-*/summary.json`). Fixture Windows đầu lỗi PID-parent ở worker giả ngắn, lần002 thiếu site-path; giữ cả hai. Lần003 dùng basePython và đúng site-packages đạt68kiểm transport. Linux đã kiểm trọn bộ mã cuối nên không rerun phương pháp thật vì sửa wrapper.

## Nguồn, quyền và vận hành

R1: runtime TT và bản chiếu nguồn đối chiếu được dựng riêng từ hai ref đã ghim; đủ60thành viên, giữ byte/hash/mốc/support, chỉ thay locator bằng mã mờ. OB đủ34. `R1-projection-check.json` và `sources/` ghi bằng chứng metadata; không là runtime attestation G3. Bản đồ gốc/nhãn chỉ nằm ở vùng private hiện có, không vào packet worker. Chưa tạo hardlink test hoặc chuyển byte test mới. Main sau duyệt sẽ materialize TT mờ trên laptop bằng hardlink, và chuyển đúng90tệp/30ca sang mỗi EC2; OB ở laptop dùng226tệp nguồn dùng chung đã có. Theo `launch-conditions.json`, nguồn TT mỗi máy khoảng0,59/0,63GiB; nguồn local406tệp đã có, không nhân bản cohort để viết báo cáo.

`main-packet.json` kê188tệp code/metadata, archive `main-code-metadata.tar.gz` không chứa raw test, nhãn evaluator hoặc bản đồ nguồn thật. Đã stage189tệp gồm chính bản kê lên mỗi máy và kiểm lại106pin code, hai runtime cùng bốn file vá (`ec2_*-final-environment.json`). Runtime main dùng Python3.12.3; TORAI dùng3.8.20. Interpreter main trỏ về bản Python ở checkpoint012, vì vậy phải giữ012. Snapshot packages và executable ghim ở `environments.json`, upstream revision/pins ở `upstream-pins.json`. Bootstrap có freeze/pip-check và log tải; không có bộ đếm network tuyệt đối để tuyên bố tổng byte tải chính xác. Các thư viện lớn khai kích thước trong log, không cài torch/CUDA; gói DEV khoảng56MiB. Mỗi lượt fixture/dev bị giới hạn timeout, tổng các lượt trên mỗi máy còn dưới giới hạn60phút của gói.

Lần kiểm cuối cloud còn23,7/24,1GiB, RAM khả dụng khoảng7GiB. Laptop còn15,17GiB và RAM khả dụng2,23GiB, đạt slot lớn nhất cộng reserve. Xem `ec2_*-final-environment.json#/resources`, `local-final-resource.json`. Điều kiện ứng viên: cloud còn8GiB theo kịch bản bảo thủ đã có; laptop còn10,062GiB cho nhận/giữ/chấm. Đây là kịch bản, không phải cận trên dung lượng đã chứng minh. RAM/đĩa/identity kiểm lại trước main; thiếu thì chờ, không giảm reservation hoặc xóa kết quả. AC=0, DC=2700giây tại lần đọc; D3 giữ AC đến xong nhận/kiểm/chấm rồi khôi phục2700giây.

Timeout và monitor giữ hợp đồng: method600giây, C-d3=60giây, một luồng số học, poll0,1giây, gap<5giây, không trần cộng dồn, không tựretry. Lỗi vận hành/nguồn/clock/mất quan sát giữ attempt, dừng và báo; chưa chạy không thành TIMEOUT. TORAI A một plan laptop, chỉ phát sau mọi non-A trong plan đó VERIFIED. Thiếu quyền/sai pin A preflight ghi BLOCKED đúng slot, không chạy; lỗi A chưa rõ giữ quy tắc dừng, ghi BLOCKED cho A chưa phát. A thiếu đủba seed thì chỉ khai thiếu. Toàn snapshot và A4 hợp lệ mới ghép nhãn/chấm; thiếu A không làm mất bảng chính đã đủ điều kiện.

Chạy chính dài hơn1giờ và cần Minh duyệt riêng. `cost-scenario.json` lặp thời gian DEV cho TT cho khoảng6,9giờ tuần tự mỗi EC2; giả sử hai worker chồng hoàn hảo thì EC2_1 khoảng3,45giờ. Đây chưa là ETA, chưa tính local/chuyển/nhận/chấm và giả định sai nếu ca test nặng hơn hoặc RAM/CPU gây chờ. Không hứa xong trong một đêm. Agent theo dõi tới hoàn tất hoặc điểm chặn; không tạo lịch tự động hay tắt máy.

## D1–D4/R3 và câu hỏi còn mở

D1 giữ nguyên sự không rõ của quyền đọc thời gian006, khai đúng cấu trúc thời gian cohort OB đã được dùng sửa adapter source_native. Không cấp quyền hồi tố bằng câu duyệt chuẩn bị. D2 cho trình main TT/Nezha khi H1 RE3 OPEN, không mở RE3. D4 thêm mô tả chênh Hit@5 cặp M1–M4 all34/remaining30/affected4 theo audit006, đủba world; A4/mức thống kê không đổi. Bảng nhóm không tách được tác động adapter khỏi độ khó ca. Quyết định nằm trong DECISIONS/WHY ngày07/11, chi tiết `OB-group-decision.json`. R3 giữ máy cũ ngoài lịch.

Nhánh OB lệch số mẫu chỉ có fixture; dev đã audit không có ca thật loại này, nên không thể bổ sung parity ca thật trước G3 bằng tập dev hiện có. Một ca A có logts thiếu N, giữ nguồn/mốc/ba seed; hành vi thật vẫn OPEN. H1 units/U/alias/r cần nguồn và quyền RE3 riêng. C-e ngoại lệ được chấp nhận cho một phép, không chứng minh mọi nguồn/môi trường đều tương đương.

013 làm cụ thể điều kiện đánh giá RQ3b và phần can thiệp tính toán RQ3d, chưa có hạng/độ đo test và chưa chứng minh lợi ích quan hệ. Nút là service/thành phần; trace tạo cạnh hướng caller→callee, log/metric gắn owner. E1 dùng quan hệ cha–con trừ hợp khoảng con, E2-C gán bằng chứng cạnh về callee, E5 dùng cạnh/SCC, E6a xếp tầng, E7 tạo vùng. C-a1 còn quan hệ qua E1; các vế bỏ thành phần phải được đọc theo tín hiệu còn giữ. Không có đối chứng đồ thị ngẫu nhiên nên không kết luận riêng lợi ích do cấu trúc thật. RQ3c chỉ mô tả vùng vì thiếu nhãn vùng độc lập; RQ3a/M1(b), LLM và đánh giá FlashTicket vẫn thuộc các phần tiếp theo của DT18/cô. Đồng thuận review không thay bằng chứng khoa học.

## Bước tiếp

Claude cần kiểm trên code/diff và output đã ghim; bản cài013 này chưa được Claude kiểm. Phần kế hoạch hai bên đã thống nhất gồm một plan A, A cuối/preflight và một lượt C-d3 từ seal thật; ngoại lệ C-e được Minh duyệt sau khi chạy. Đọc `de-nghi-duyet-main.md`, `../../runbook.md`, `wrappers-013.patch`, manifest và bằng chứng gốc. Chưa commit/push. Danh sách commit sẽ được kê riêng, loại raw/archives/private mapping, và chỉ thực hiện nếu Minh duyệt.
'''
    write(RUN/'bao-cao.md', report, create=True)
    proposal = '''# Gói Minh duyệt để phát main 013

Trạng thái: đề nghị sau Claude kiểm, chưa có quyền chạy. Một câu “Duyệt chạy main013 theo hồ sơ đã kiểm” sẽ được Codex ghi nguyên văn thành nguồn quyết định, với đúng protocol/source-bundle/manifest của gói này. Nếu code hoặc gói đổi, không dùng lại câu duyệt cho bản khác.

Câu duyệt đó cấp cùng lần nhưng ghi riêng từng quyền sau:

1. Khóa G3(a) cho đúng ứng viên013, cấu hình, ma trận1.640job+2vị trí C-e thiếu hỗ trợ, môi trường, phân lô30/30 và policy trong hồ sơ.
2. Mở đúng60TT+34Nezha-OB test, giữ cửa sổ, U/alias, seed/world/mẫu số; không gồm RE3.
3. Codex làm người quản lý nguồn và evaluator: dùng các bản đồ nguồn/nhãn độc lập hiện có theo ref `source-bundle.json`; kiểm byte nguồn, tạo TT locator mờ bằng hardlink trong `data/locked/rcaeval-re2tt-60/<test-id>/`, ghép nhãn chỉ sau verify snapshot. Không sửa nguồn thô.
4. Chuyển đúng nguồn TT vào `/home/ubuntu/rca-p7/T-054/checkpoint013/data-root/` của từng EC2 theo bảng90tệp/30ca mỗi máy; metadata đủ60ca vẫn giữ toàn cohort. Chỉ code/metadata, grant và đúng phân lô được chuyển, không bản đồ thật/nhãn.
5. Phát và theo dõi main tới hết cohort, có thể dài hơn1giờ, không trần cộng dồn; giữ giới hạn method/monitor hiện hành. DRAIN/resume cùng plan/token/root theo runbook; không retry slot đã hỏng, không sửa thiết kế sau điểm hoặc tắt máy.
6. Cấp nguồn TORAI A đúng cohort60TT và180CSV tác giả cùng metric đã ghim, chạy seed0/1/2 sau phần chính của laptop. Thiếu/sai pin giữ BLOCKED; ca logts thiếu N giữ nguyên; lỗi chưa phân loại giữ attempt và dừng A. A là bảng phụ, không điều khiển A4.
7. Nhận, kiểm toàn snapshot/seal và chấm các bảng/độ nhạy/diễn giải đã khóa, gồm D4, sau đủ A4; giữ kết quả đầu. D1–D4/R3 đã chốt, H1 RE3 vẫn OPEN, RE3 giữ quyền riêng cho bản cuối.

Phạm vi ghi của lượt chạy sau duyệt: `results/T-054/runs/chuan-bi-main-013/{grants,activated-001,execution-receipts,received-main-*}/`, `results/T-054/runs/main-013/`, `results/T-054/reports/main-013/`; nối LOG và DECISIONS/WHY để lưu quyết định đúng lời Minh, cập nhật đúng dòng T-054 trong STATE. Trên EC2 chỉ vùng checkpoint013. Tạo hardlink TT theo công thức trên, không xóa dữ liệu hoặc đổi file thô. Lưu mọi attempt và archive nhận, kể cả hỏng.

Codex sẽ tự ghi nguồn lời duyệt và grant thật, kiểm lại hash/tài nguyên/identity, kích hoạt metadata, kiểm nguồn/chuyển và phát CLI; Minh không phải tự sửa JSON hoặc gõ lệnh. `grant-template.json` hiện có tất cả cờ quyền=false. Một bước bị chặn thì dừng đúng phần phụ thuộc và báo, không tự đổi gói để ép chạy.

Commit/push cần Minh duyệt riêng theo danh sách file. Nó không là điều kiện tự tạo thêm trước main: provenance thực chạy được khóa bằng manifest và code/env pins theo SPEC. Có thể Minh duyệt commit kèm câu duyệt cuối nếu muốn; khi chưa có thì giữ working tree và không commit. Không dùng quyền main để hợp thức hóa quyền lịch sử006.
'''
    write(RUN/'de-nghi-duyet-main.md',proposal,create=True)
    bundle = json.loads((RUN/'source-bundle.json').read_bytes())
    import hashlib
    sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    grant=dict(g3=False,test_grant=False,main_dispatch=False,materialize_source_grant=False,transfer_test_grant=False,
               score_grant=False,torai_A_source_grant=False,main_operating_policy_approved=False,
               RE3_preparation_disposition='OPEN_ACCEPTED_FOR_MAIN_ONLY',source=dict(path='FILL_ONLY_AFTER_MINH_DECISION',sha256=''),
               approved_candidate_protocol_sha256=sha(RUN/'protocol-candidate.json'),
               approved_source_bundle_sha256=sha(RUN/'source-bundle.json'),
               approved_preparation_manifest_sha256='FILL_AFTER_REVIEW_OF_MANIFEST',
               torai_A_source_sha256=bundle['author_source_ref']['sha256'])
    write(RUN/'grant-template.json',json.dumps(grant,ensure_ascii=False,indent=2),create=True)
    old=(RUN/'before/results/T-054/ho-so-g3.md').read_text(encoding='utf-8')
    exposure=old[old.index('## Tiếp xúc trước G3'):old.index('## Bằng chứng A/B1/B2/C')]
    a=exposure.index('**Quyền 006 còn OPEN')
    exposure=exposure[:a]+'''**D1 đã chốt ngày07/11/2026:** giữ nguyên lịch sử phạm vi quyền006 chưa rõ, không diễn giải thành quyền hồi tố. Minh duyệt cách khai giới hạn tính độc lập của việc dùng cấu trúc thời gian cohort OB sửa adapter. Chưa có hạng/độ đo main. Quyền chạy/chấm hiện tại vẫn cần cấp riêng. [Quyết định](../../docs/DECISIONS.md) · [Nguồn lời chuẩn bị](runs/chuan-bi-main-013/preparation-permission.json).
'''
    dossier='''# Hồ sơ G3(a) — ứng viên checkpoint013

Chuẩn bị013 đã làm theo Minh duyệt; chờ Claude kiểm bản cài và Minh duyệt chạy. Gói hiện hành là `runs/chuan-bi-main-013/`, thay các plan/helper ứng viên011 cho lần chạy sắp tới. Không dùng `protocol.json` ở gốc T054 hoặc helper006/011 để phát013. Các gói đó giữ làm lịch sử.

[Báo cáo013](runs/chuan-bi-main-013/bao-cao.md) · [Nội dung duyệt cuối](runs/chuan-bi-main-013/de-nghi-duyet-main.md) · [Runbook](runbook.md) · [Manifest013](runs/chuan-bi-main-013/manifest.json).

| Phần trước G3 | Bằng chứng hiện tại | Trạng thái |
|---|---|---|
| Nguồn/B1 | TT60+OB34 metadata đối chiếu nguồn riêng; R1 locator mờ; full cohort giữ nguyên | PREPARATION; attestation/kiểm byte test mới sau quyền |
| A/B2/C | Mỗi EC2101fixture mã cuối; Windows transport68; báo cáo thiếu A/partial seed89hàng; kích hoạt sinh giả11kiểm | Đạt trong phạm vi fixture; không gọi là main |
| Tuyến DEV thay đổi | 15đối chiếu mới;14khớp nghiêm ngặt, một C-e sai khác số học đã được Minh chấp nhận riêng; M1 chính tái dùng012 | Ghi rõ ở parity-disposition, không đổi tolerance chung |
| Môi trường/code/phân lô |106pin code, runtime3.12/3.8 và4file vá trên hai EC2 mới;30TT mỗi máy, laptopOB/CIRCA/MicroRank/A | Kiểm cuối đạt; tài nguyên động kiểm lại trước phát |
| D1–D4/R3 | DECISIONS/WHY ngày07/11, OB-group-decision | Minh đã chốt; H1 RE3 vẫn OPEN theo D2 |
| Quyền test/nguồn/chuyển/run/chấm | grant-template có mọi cờfalse | Chờ Minh sau phản biện bản cài013 |

Tổng1.640job+2vị trí C-e thiếu hỗ trợ, gồm68UNSUPPORTED đã khai; bảng từng máy và group ở `candidate-validation.json#/hosts`. D4 báo chênh Hit@5 M1–M4 trên34/30/4OB, đủba world, mô tả; giữ A4 và mức thống kê. TORAI A là bảng phụ, một plan laptop, phát sau non-A của plan đó VERIFIED, preflight theo quyền/pin và không bình quân seed sống. Nguồn A cho main chưa được cấp. Hành vi thật của ca logts thiếu N và nhánh OB lệch số mẫu vẫn OPEN.

'''+exposure+'''
## Sáu câu G3 và giới hạn nguồn

1. Câu hỏi chính là RQ3b và phần can thiệp tính toán RQ3d theo MRP, DT18 và hướng dẫn cô; chưa có kết quả test.
2. Cohort TT/OB, cửa sổ, U/alias, cấu hình, seed/world, policy lỗi/mẫu số và thống kê ghim trong protocol-candidate/contract/source-bundle013. Tiếp xúc OB ở trên giới hạn diễn giải độc lập; nhóm34/30/4 không phân xử riêng tác động adapter.
3. TT dùng TORAI B ba seed trong A4, OB dùng SimpleRCA M4 với giới hạn tái lập đã khai; A là bảng phụ. Không chọn lại baseline sau nhìn điểm.
4. Nút là service/thành phần; cạnh caller→callee. Log/metric gắn owner, trace giữ cha–con. E1 dùng hợp khoảng con; E2-C gán cạnh về callee; E5 dùng cạnh/SCC; E6a xếp tầng; E7 duyệt cạnh tạo vùng. T12-on có đúng hai snapshot ghim. C-a1 còn E1, nên không gọi mọi vế bỏ thành phần là bỏ mọi quan hệ.
5. Sau grant, báo theo dataset/ca/ô/world/support, giữ ERROR/TIMEOUT/UNSUPPORTED và lượt đầu đúng policy. Không có đối chứng đồ thị ngẫu nhiên thì không suy riêng lợi ích cấu trúc thật.
6. B6 được khóa vào đúng byte code/gói/config/env/cohort và quyết định cuối. H1 RE3 chưa đóng, D2 cho trình main TT/Nezha riêng; RE3 cần nguồn/profile/quyền riêng cho bản cuối. RQ3c chỉ mô tả vùng vì thiếu nhãn; RQ3a/M1(b), LLM và áp dụng FlashTicket còn lại, không coi xong T054 là xong đề tài.

Claude đã góp ý và thống nhất phần kế hoạch trước triển khai, chưa kiểm các output013 mới. Đồng thuận không thay bằng chứng. Chưa commit/push, chưa mở test hoặc phát main.
'''
    write(ROOT/'results/T-054/ho-so-g3.md',dossier)
    runbook='''# Vận hành — ứng viên checkpoint013

Đọc [báo cáo013](runs/chuan-bi-main-013/bao-cao.md), [nội dung duyệt cuối](runs/chuan-bi-main-013/de-nghi-duyet-main.md) và manifest. Gói011/006 là lịch sử. Chuẩn bị013 đã được duyệt, G3/test/main/chấm chưa được cấp; mọi lệnh phát/nhận/chấm dưới đây chỉ dùng sau lời duyệt cuối đúng gói.

Từ `D:/RCA-flashticket`, kiểm manifest chỉ đọc:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/verify_manifest.py
```

Phân lô: EC2_1=16.176.181.251/key4,448job+2support,2worker; EC2_2=13.236.44.106/key3,450job,1worker; local742job,2worker tối đa. Mỗi EC230TT, toànOB/CIRCA/MicroRank/A ở laptop. Khóa SSH chỉ đọc từ `D:/RCA-ext/keys/`, không chép vào repo. Giữ strict host key/instance ID; không bật/tắt máy. Code=`checkpoint013/work`, data=`checkpoint013/data-root`, output=`work/results/T-054/runs/main-013/queue`. Python main trên EC2 phụ thuộc interpreter ở012: giữ012.

Sau Minh duyệt, Codex lưu nguyên văn lời duyệt ở `013/grants/minh-main.txt`, dựng grant thật `013/grants/main-grant.json` từ mẫu và ghi các quyền riêng theo đề nghị. Ghim protocol/source-bundle/manifest và nguồn quyết định; A giữ pin riêng. Nối DECISIONS/WHY/LOG và dòng STATE đúng quyền cuối; không sửa đầu ra chuẩn bị đã ghim. Minh không cần tự điền JSON. Dùng hash thật của file grant, không dùng chuỗi ví dụ dưới đây làm giá trị.

```powershell
$grant013 = 'results/T-054/runs/chuan-bi-main-013/grants/main-grant.json'
$grant013Sha = (Get-FileHash -LiteralPath $grant013 -Algorithm SHA256).Hash.ToLowerInvariant()
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/main.py --grant $grant013 --sha256 $grant013Sha
```

Entry kiểm toàn vẹn gói/tài nguyên/identity, tạo metadata LOCKED và attestation đầy đủ cohort, kiểm plan/union, stage đúng code và grant, kiểm môi trường, kiểm nguồn/chuyển đúng phân lô, materialize hardlink local rồi phát CLI ba máy. Truyền qua stdin với kê byte/hash, đích mờ; không đóng gói bản đồ thật/nhãn. Giữ biên nhận và đầu ra; bước lỗi không tự bỏ qua. Không tự gọi lại helper create-only khi đã có output dở: đọc receipt/queue trước, giữ lỗi và trình đúng sửa cần thiết.

Theo dõi `p7.py status --plan <activated-host-plan> --sha256 <pin-thật>` trên đúng host/root. Lệnh status chỉ đọc. Lần trả launcher_pid không chứng minh supervisor còn sống: kiểm status.controller và tiến độ/monitor. Mất SSH không nghĩa worker chết. DRAIN bằng `p7.py drain` với cùng plan/pin; giữ active đóng. Resume bằng `p7.py resume --plan ... --sha256 ... --authority ... --authority-sha256 ...` trên đúng runtime/host/root, một luồng số học như khi phát; đối chiếu PID/token trước, không retry hỏng hoặc phát bản sao.

Monitor poll0,1giây, maxgap<5giây, method600giây/C-d3=60giây; không trần cộng dồn, không tựretry. Theo dõi RAM/đĩa và nhóm ERROR/BLOCKED; thiếu nguồn, clock, mất monitor hoặc không tiến triển thì dừng/báo. Chưa chạy không gán TIMEOUT. TORAI A preflight nguồn theo grant, chỉ phát sau mọi non-A của laptop VERIFIED; thiếu quyền/sai pinA giữ BLOCKED, lỗi lạ dừngA và ghi phần chưa phát. Không bình quân A thiếu seed. Không sửa thiết kế sau dùng test; giữ kết quả đầu và khai riêng mọi bản sửa theo C-15 B.

Sau cả ba queue dừng và có đủ snapshot, nhận và chấm từ laptop (thư mục nhận mới):

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/receive_main.py --grant $grant013 --sha256 $grant013Sha --destination D:/RCA-flashticket/results/T-054/runs/chuan-bi-main-013/received-main-001
```

Helper giữ archive và bản nhận, xác minh receipt/seal, union đủ từng slot rồi mới đọc nhãn evaluator. A4 còn thiếu/chặn thì chưa tạo bảng; thiếuA ngoài A4 được khai trong bảng thiếu, không bình quân seed sống. Báo cáo ở `results/T-054/reports/main-013/`, D4 trong a4.json#/OB_group_description. Nếu bước nhận/kiểm/chấm lỗi thì giữ output, chọn tên lượt mới khi được phép sửa; không ghi đè report.

D3: main giữ AC sleep0, DC giữ hiện hành; chỉ khôi phục AC2700giây sau nhận/kiểm/chấm thành công. receive_main làm và ghi receipt. Nếu bị chặn trước đó, giữ máy thức, báo Minh; không tự khôi phục giữa lượt cần laptop. Không tạo ScheduledTask hoặc tựresume sau reboot. RE3 không thuộc grant main TT/OB. Commit/push chỉ sau Minh duyệt riêng danh sách đã rà, không dùng packet cũ có mapping thật hoặc archive/raw data.
'''
    write(ROOT/'results/T-054/runbook.md',runbook)
    spec=TASK/'SPEC.md';text=spec.read_text(encoding='utf-8')
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('- **Trạng thái:**'):
            lines[i]='- **Trạng thái hiện hành 07/11/2026:** chuẩn bị013 theo Minh duyệt đã có output, chờ Claude kiểm bản cài và Minh duyệt G3/test/nguồn/chuyển/main/chấm. D1–D4/R3 đã chốt; H1 RE3 OPEN theo D2. Không commit/push. Các lịch local/005/011 bên dưới giữ lịch sử; nguồn vận hành sắp trình khóa là hồ sơ/runbook và protocol-candidate013.'
            break
    marker='**Bổ sung Minh duyệt 07/11/2026 — chuẩn bị013.**'
    text='\n'.join(lines)+'\n'
    at=text.index('\n',text.index(marker))
    add='''

**Đầu ra chuẩn bị013, chờ phản biện bản cài:** `runs/chuan-bi-main-013/candidate-validation.json` kê EC2_1=448job+2support/2worker, EC2_2=450job/1worker, laptop=742job/2worker tối đa. Hai EC2 mới30TT/máy; laptopOB/CIRCA/MicroRank/A. `protocol-candidate.json`, source-bundle, contract và placement013 thay ứng viên011 cho lần xin khóa tiếp theo, vẫn CANDIDATE. Mỗi EC2101fixture mã cuối;15đối chiếuDEV mới với14khớp nghiêm ngặt và một C-e sai khác số học Minh đã duyệt đúng phép. D1/D2/D4 theo DECISIONS ngày07/11 và báo cáo013; H1 chưa có nguồn, không mở RE3. Mọi điều kiện nguồn/quyền main vẫn chờ quyết định cuối, kể cả nguồnA và truyền test. Không lấy mã003/005/011 để phát013.
'''
    text=text[:at]+add+text[at:]
    spec.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
    state=ROOT/'docs/STATE.md';lines=state.read_text(encoding='utf-8').splitlines()
    for i,line in enumerate(lines):
        if line.startswith('- **T-054'):
            lines[i]='- **T-054 — chuẩn bị013 xong phía người làm, chờ Claude kiểm.** Codex làm, Claude phản biện. D1–D4/R3 và ngoại lệ đúng phép C-e đã duyệt; mỗi EC2101fixture, gói30TT/máy và laptopOB/CIRCA/MicroRank/A. Chưa G3/test/main/chấm/commit. [Hồ sơ](../results/T-054/runs/chuan-bi-main-013/bao-cao.md), [LOG](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md).'
    state.write_bytes(('\r\n'.join(lines)+'\r\n').encode('utf-8'))
    print('Wrote approved 013 report, final proposal, false grant template, dossier/runbook, SPEC and one STATE row')


if __name__=='__main__':
    main()
