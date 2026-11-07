"""Báo cáo/checkpoint chuẩn bị; không khóa G3, không phát main."""
from pathlib import Path
import sys,json,collections,re,difflib
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import *
def pin(path):
    p=ref(path)
    if Path(path).resolve().is_relative_to(ROOT):p['path']=Path(path).resolve().relative_to(ROOT).as_posix()
    return p
def md(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(text.encode('utf-8'))
sources=read_pin(pin(RUN/'checkpoint-01-sources.json'));plans=read_pin(pin(RUN/'checkpoint-01-plans.json'));preflight=read_pin(pin(RUN/'checkpoint-03-preflight.json'))
placement=read_pin(pin(OUT/'runs/trien-khai-005/placement-005.json'))
listing=dict(status='PREPARED_NOT_DISPATCHED',hosts=plans['hosts'],source_grant=pin(RUN/'preparation-grant.json'),placement=pin(OUT/'runs/trien-khai-005/placement-005.json'),
    plans=plans['plan_refs'],aggregate=plans['aggregate'],commands=pin(RUN/'commands-prepared.json'),TT_transfer_bytes=placement['TT_transfer_bytes'],
    jobs=1640,Ce_insufficient=2,positions=1642,unsupported_OB_jobs=68,maximum_supported_method_calls=1572,
    dependencies=['Mỗi ca: prep trước TORAI; M1 seal trước C-d3.','Lô độc lập hai EC2+laptop chạy đồng thời khi được phát; tối đa2worker/máy khi RAM đủ.','Snapshot đủ và kiểm binding trước ghép điểm/nhãn; A phụ ngoài A4.'])
atomic(RUN/'bo-tri-du-kien.json',listing)
atomic(RUN/'private-artifact-pins.json',{p.as_posix():ref(p)for p in Path('D:/RCA-ext/private/T-054/prepare-main-006').rglob('*')if p.is_file()})
report='''# T-054 — chuẩn bị nguồn thật và ba máy, checkpoint006

Đã làm xong ba phần Minh giao: nguồn thật/danh sách; chuyển TT; kiểm trước chạy và chuẩn bị lệnh. **Dừng báo Minh, chưa chạy main hoặc chấm điểm.** Chưa tự khóa G3. RE3 không thuộc ba phần lần này, giữ trạng thái chưa triển khai adapter thực.

## Quyền và mức tiếp xúc

Minh cấp đúng ba bước chuẩn bị tại quyen-minh.txt, diễn giải trong preparation-grant.json. Lượt này đã dùng nguồn test để chuẩn bị theo quyền: băm byte, đọc schema/header và timestamp cần cho mốc/cửa sổ/C-e; đã giải nén ba CSV tác giả đúng60ca. Không nói “test chưa từng được mở” sau lượt này. Không đọc giá trị metric/log message/operation để phân tích, không gọi phương pháp RCA, không tạo ranking, không ghép nhãn với kết quả hoặc xem độ đo. Code phương pháp/cấu hình/cohort/cửa sổ/seed không đổi từ ứng viên005.

Phạm vi nguồn A là chuẩn bị cohort theo gói đã trình, không còn chỉ dev. Quyền này không cho phát method A hay main94. Nguồn nhãn G1 được quản lý riêng để chuẩn bị evaluator; không vào packet cloud hoặc method. Không mở RE3, không commit/push, không bật/tắt máy hoặc dọn thêm.

## Phần1 — nguồn thật và danh sách

TT60 giữ180parquet/1.309.388.082byte, từng ca/tệp đúng SHA256/byte của HF revision đã pin. Mốc inject_time lấy từ gói tác giả có sẵn và khớp Git blob từng inject_time.txt trên HF cho đủ60ca; không tải dữ liệu mới. Ba CSV tác giả chỉ được giải nén cho đúng60ca vào vùng private mới:180CSV, **9.244.910byte**. Gói torai-data.zip91.262.227byte đúng SHA256 và biên nhận Figshare cũ. Thư mục cũ chỉ có DEV; không chép/ghi đè vào nó. Nguồn: checkpoint-01-sources.json, TT-injection-source-metadata.json/A-author-source.json trong vùng private được pin.

OB34 đúng G1 và fault_list native đã ghim. Dùng inject_time chính, không đổi sang inject_timestamp độ nhạy. Mỗi ca giữ đúng11nguồn metric và3minute-file trace+3log của giao thức baseline Q85/T026; không mở rộng theo cửa sổ10phút. Tổng226tệp nguồn khác nhau/1.598.103.311byte, hash Git blob và byte khớp cây nguồn Nezha revision d8140101fdb4e7dfb60d3ef9f64706f382b68470. Chỉ hash/header, không dựng payload tín hiệu. Nguồn: checkpoint-01-sources.json và OB-file-source-pins.json private.

C-e: **58ca verified,2ca insufficient** từ timestamp/cậnF/A0 cùng định nghĩa adapter và quan_sat. Đây là hỗ trợ thời gian quan sát, không chứng minh nền khỏe. Không chạy M1 để phân loại;2ca thiếu giữ dòng hỗ trợ gắn sourcehash, không gán0 hoặc bỏ khỏi mẫu số khai. Chứng cứ temporal riêng giữ r, F/H, ô và lý do, không coi hai trạng thái là kết quả khoa học. Nguồn: TT-Ce-temporal-evidence.json private, checkpoint-01-sources.json#/Ce_support.

Danh sách thật giữ đủ1.642vị trí=1.640job+2support. Đã kiểm cấu hình/seed/cửa sổ/env và các phụ thuộc. Chuẩn bị metadata runtime và nguồn riêng gắn đầy đủ thành viên G1; nhãn evaluator ở vùng private, tách khỏi lô phương pháp. Receipt hiện là PREPARATION-BINDING, không giả attest_runtime hoặc LOCKED_G3. Nguồn: checkpoint-01-plans.json và prepared/*.json.

## Danh sách bố trí dự kiến

| Máy | Phần việc | Job trong danh sách | Dòng hỗ trợ C-e | TT raw đã đặt |
|---|---|---:|---:|---:|
| EC2_1 ·13.211.127.97 |30TT: M1-family210, TORAI B90, C-d3 30, C-e28 |358|2|654.702.162byte/90tệp|
| EC2_2 ·3.107.156.186 |30TT còn lại: family210, B90, C-d3 30, C-e30 |360|0|654.685.920byte/90tệp|
| Laptop |OB442job; TT5baseline300; TORAI A phụ180 |922|0|Giữ nguyên bản gốc|

Trong OB442 có68job trảUNSUPPORTED theo giao thức đã khai; không chế đầu vào cho CIRCA/TORAI. Vì vậy tối đa1.572lượt phương pháp được hỗ trợ, không coi1.640job là1.640lượt học. C-c/C-g/C-d1/2 được dẫn xuất từ đầu ra đã khai, không chạy lại baseline để tạo chúng. Danh sách mã mờ từng TT/máy, cơ cấu vế và pin plan tại bo-tri-du-kien.json; đầy đủ từng job tại prepared/ec2_1-plan.json, ec2_2-plan.json, local-plan.json.

EC2 nhận TT nặng theo ưu tiên Minh; laptop giữ nguồn OB ngày dùng chung và các adapter/baseline phù hợp môi trường hiện có. Không cần mọi việc đều cloud. Mỗi host tối đa2worker và1luồng số học/phương pháp khi RAM cho phép; một slot/method×dataset cùng lúc. Prep→TORAI và M1seal→C-d3 phải tuần tự; hai EC2 và lô laptop độc lập song song. Không thêm cache liên vế hoặc lô pilot mặc định.

## Phần2 — chuyển và bảo toàn

Hai luồng SSH chuyển đồng thời, EC2_1~108,80s và EC2_2~109,36s kể từ sau kiểm nguồn đầu gửi; không cộng thành giờ trôi. Mỗi máy đúng90tệp. Kiểm SHA256/byte trước gửi, trong stream và đọc lại đĩa đích. Chỉ rename vùng partial thành data-root khi đủtệp/hash. Bản gốc laptop giữ nguyên. Không chuyển nhãn, OB raw hoặc CSV A lên EC2; không xóa nguồn/kết quả cũ. Nguồn: checkpoint-02-transfer.json và ec2_*-TT-transfer.json.

Đích dữ liệu là /home/ubuntu/rca-p7/T-054/ec2_1/main-005/data-root và ec2_2/main-005/data-root. Code từng host ở cùng parent/code, tiền tố khác nhau để không nhầm receipt khi nhận. “main-005” là tên vùng đã khai ở contract005, chưa có main queue hoặc phương pháp chạy trong đó. Packet128tệp mỗi máy có code đóng băng và metadata TT/plan chuẩn bị, tất cả được hash trước dùng; không chứa nhãn evaluator/A source/OB map. Không cần dựng lại môi trường T025 đã kiểm.

## Phần3 — kiểm trước chạy và lệnh

Cả ba host PASS:103pin code hiện hành, môi trường main đúng fingerprint, executable/PYTHONPATH, source selector/hash, mapping/cohort, config, seed, window, phụ thuộc, partition và policy ứng viên. Candidateauthority bị từ chối đúng WAIT_G3 trên cả ba máy; quyền chuẩn bị không phát được main. Không chạy thêm RCA hoặc baseline. Nguồn: checkpoint-03-preflight.json; ec2_*-preflight.json và local-preflight.json.

Sau staging, free disk EC2_1~8,816GB; EC2_2~13,884GB; laptop~16,791GB tại lúc kiểm. RAM khả dụng tương ứng~7,40/~7,37/~3,26GB; theo ước lượng reserve hiện tại có thể nhận2slot, nhưng không phải bảo đảm peak mọi ca. Driver vẫn kiểm RAM động, không đổi slot chưa chạy thànhTIMEOUT. Output/temp chưa có upper bound toàncohort, cần theo dõi đĩa/DRAIN khi thiếu. Lô nhận giữ pin/receipt/envelope gốc và phân vùng; union đủ/khôngtrùng trước nhãn như runbook005.

Laptop đang cắm điện, pin100%, nhưng sleep khi AC sau45phút; hibernateAC=0. **Phải giữ laptop thức trong main.** Chỉ đọc thiết lập, chưa tự đổi nguồn điện, chưa cài Scheduled Task. Nguồn: laptop-power-readonly.json.

commands-prepared.json chứa lệnh plan/status chính xác cho ba host và lệnh run candidate được giữ chặn. Không hướng dẫn dùng plan DEV/giả làm main. Sau Minh xét G3/cho main, activate_prepared.py nhận quyết định có pin đúng protocol/bundle, mới tạo bảnLOCKED, attest runtime v3 thật, khóa scope policy rồi biên dịch plan/authority cuối bằng compiler đã kiểm. Helper **không phát run**. Cần đưa metadata khóa cuối vào code_root từng host và kiểm pin trước phát. Đây là phần đóng metadata phụ thuộc quyết định cuối, không là vòng thiết kế/pilot mới. Đã kiểm preparation-grant không thể kích hoạt, không sinh activated-001. Không có main grant giả.

## Điểm dừng và giới hạn

Ba bước chuẩn bị đã xong; dừng báo Minh. Để phát main còn Minh xét G3/quyền chạy, đóng metadata/authority cuối đúng quyết định và giữ laptop thức. Không xin lại quyền nguồn/transfer đã được cấp trong lượt này. RE3 adapter chưa làm, không được tính là đã hoàn tất toàn bộ P7/giữ ngoài. Công việc chuẩn bị không trả lời RQ3 hoặc chứng minh phương pháp hiệu quả.

Giữ lỗi chuẩn bị: import datetime bị wildcard che tên; chọn OBminute ban đầu suy11file theo cửa sổ nhưng phát hiện không có trước khi đọc telemetry và sửa về đúng3file baseline. Giữ sources-failure.json và sources-failure-r2.json. TT/A đã dựng được dùng lại khi tiếp nhận, không giải nén lại hoặc đọc lại timestamp để sửa OB. Validator005 chạy trong lúc LOG đang được nối nên cuối báo lệchLOG; toàn kiểm nội bộ trước bước manifest đạt. Giữ LOG trước phiên và kiểm prefix, không phục hồi hash cũ để che thay đổi hợp lệ.

Không có ETA main mới từ chuẩn bị hash/transfer. Kịch bản0055–9giờ vẫn có điều kiện, chưa phải ETA bảo đảm hoặc toàntask; không đặt trần cố định. Không đánh đổi đủcohort/seed/nhánh để vừa giờ, không bắt đầu main trong phiên chuẩn bị này.
'''
md(OUT/'reports/chuan-bi-main-006/bao-cao.md',report)
md(OUT/'ho-so-g3.md','# Hồ sơ trình G3 hiện hành — chuẩn bị006\n\n'+report[report.index('Đã làm xong'):])
runbook='''# Vận hành hiện hành — chuẩn bị006, dừng trước main

Đọc reports/chuan-bi-main-006/bao-cao.md, runs/chuan-bi-main-006/bo-tri-du-kien.json và LOG phiên7. Ba checkpoint01nguồn/danh sách,02transfer,03preflight đã có. Nguồn và TT transfer được Minh cấp riêng cho chuẩn bị; không còn chờ grantchuẩn bị/Acohort cũ. Chưa G3/main, chưa RE3 hoặc commit.

Chỉ đọc để tiếp nhận:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-006/verify_checkpoint.py --manifest results/T-054/manifest-chuan-bi-main-006.json
```

commands-prepared.json có lệnh plan/status theo đúng3host và pin hiện có. Run candidate bị WAIT_G3 trên cả ba máy. Không chạy lại prepare_sources/prepare_plans/stage/transfer/finish: đầu ra create-only đã có, không dùng lại tênrun. Các script hỗ trợ đã được chạy, không có auto-resume/main nền.

Protocol.json/root và freeze007 giữ bản khoa học ứng viên005 đúng byte để plan đã pin tiếp tục kiểm được. Tình trạng vận hành/nguồn mới xem006, không lấy open_choices cũ trong protocol ứng viên làm lời từ chối grantchuẩn bị mới. Source-manifest005 trong bundle là ảnh chụp khoa học, metadataTT/plan006 kèm theo có manifest riêng. Code103pin/9script worker không đổi sau đọc metadata test.

Sau Minh xétG3 và cho main riêng, ghi nguồn quyền đúng lờiMinh trong vùng006; main-grant phải pin approved_candidate_protocol_sha256 và approved_source_bundle_sha256, cấp g3/test_grant/main_dispatch/torai_A_source_grant. Chạy activate_prepared.py --grant <đườngdẫnquyền> --sha256 <pinguồnquyền>. Helper không phát main; xuất activated-001/activation-receipt.json, sourcebundle/bindingv3/policyLOCKED và plan/authority cuối. Không dùng receiptPREPARATION làm bindingv3, không đổi rootprotocol ứng viên đang được pin.

Đưa đúng metadata khóa cuối+nguồnquyền vào code_root mỗihost, giữ mọi filecandidate cũ; privateTT refs cần path tương đối code root, OB/A/labels ởlaptop. Kiểm pin/môi trường/ownership/data/đĩa và no-main-queue trước lệnh run. Runtime/independentTT đầyđủ60member nhưng rawmỗiEC2 chỉ30caseđượcgiao; không cấp labelOB/Amap cho cloud. Không tự đổi chủ lô hoặc chạy dự phòng trùng. Chỉ phát main khi Minh yêu cầu.

Trước main giữ laptop thức: hiện ACsleep45phút; chưa đổi profile điện. Worker2 chỉ khi RAMđủ. Status chỉđọc; DRAIN ngừngphát mới và để activeđóng; resume phải cùng plan/root, kiểm PID/token để không chạyđôi. SSHngắt không tự coi workerđãchết; cloudsupervisor độc lậpSSH. Không tự restart sau reboot hoặc ScheduledTask.

Nhận/hash/snapshot/merge giữ nguyên cơ chế đãkiểm ở checkpoint005: remote prefixes riêng theo ec2_1/ec2_2; giữ nguyên receipt/path, receive_paths ánhxạ bảnnhận trong cùngprocess; compare parts với planrefs; merge_partitions đủuniontrướcnhãn. Gói code/source metadata và dữ liệu ởđích giữ đến khi Minh duyệt dọn. Bản gốc laptop và mọi attempt/hỏng giữ nguyên. Đĩa/output chưa có worstcase; thiếuRAMđĩa/lỗinguồn/clock/phânloạichưarõ thìDRAIN vàbáo, unrun khôngTIMEOUT. Lỗi/khôngtiếntriển/lặpvôtận/hàngchụcgiờchưaxong thìbáo; khôngtrầncộngdồn.

RE3 schema/adapter/quyền cuối riêng chưa triểnkhai trong006; không mở telemetry bằng grantchuẩn bị94. PromptClaude trungtính ở LOG, Minh tự chọnchuyển. Không commit/push.
'''
md(OUT/'runbook.md',runbook)
auth=read_pin(pin(OUT/'authorization.json'));auth.update(preparation006=pin(RUN/'preparation-grant.json'),
    source_preparation_completed=True,TT_cloud_transfer_completed=pin(RUN/'checkpoint-02-transfer.json'),
    torai_A_source_grant='PREPARATION_COHORT_GRANTED_AND_EXTRACTED; main method execution still requires main grant',
    current_read_scope='TT timestamps/schema+opaque bytes; OB native metadata/opaque hash/header; author3CSV exactcohort extracted/header. No method/score.',
    g3=False,test_grant=False,main_dispatch=False,stop_before_main=True,RE3_telemetry=False,commit_push=False)
(OUT/'authorization.json').write_bytes(canonical(auth)+b'\n')
sm=read_pin(pin(OUT/'source-manifest.json'));sm['preparation006']={k:pin(RUN/v)for k,v in [('source_grant','preparation-grant.json'),('sources','checkpoint-01-sources.json'),('plans','checkpoint-01-plans.json'),('transfer','checkpoint-02-transfer.json'),('preflight','checkpoint-03-preflight.json')]};(OUT/'source-manifest.json').write_bytes(canonical(sm)+b'\n')
state=ROOT/'docs/STATE.md';raw=state.read_bytes();replacement='- **T-054 — P7(a): chuẩn bị006 nguồn thật/ba máy đã xong; DỪNG trước main, chờ Minh xét G3 và cho chạy.** Codex làm, Claude phản biện. TT60/OB34 đúng nguồn; A180CSV/9,245MB dùng zip cũ; C-e58đủ+2thiếu. TT180tệp/1,309GB đã chuyển song song và khớp hash: EC2_1 358job+2support, EC2_2 360job; laptop922job (OB/TTbaseline/A,68UNSUPPORTED). Preflight cả3PASS, guardWAIT_G3; chưa RCA/chấm. Laptop ACsleep45phút cần giữ thức khi main. Binding/policy/authority cuối đóng sau quyết địnhG3, không pilot mới. RE3adapter chưa làm. [Báo cáo006](../results/T-054/reports/chuan-bi-main-006/bao-cao.md), [LOG phiên7](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md).'
state.write_bytes(b''.join(replacement.encode()+ (b'\r\n'if line.endswith(b'\r\n')else b'\n')if line.startswith('- **T-054'.encode())else line for line in raw.splitlines(keepends=True)))
print(json.dumps({'reported':True,'source_and_transfer_and_preflight':'PASS','main':False,'RE3':False}))
