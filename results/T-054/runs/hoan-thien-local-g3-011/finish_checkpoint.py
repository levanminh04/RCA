"""Publish authorized local-preparation outputs and append a durable handoff."""
from pathlib import Path
from datetime import datetime,timezone
import difflib
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(path):
    data=path.read_bytes();return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def text(path,value):path.write_text(value,encoding='utf-8')

assert read(RUN/'local-checks.json')['PASS']and read(RUN/'packet-validation.json')['PASS']
assert not (RUN/'activated-001').exists()
resource=read(RUN/'local-checks.json')['checks'][-1]['observation']
storage=read(RUN/'storage-copy-accounting.json')

# Same approved content, with spacing restored for a human reader.
spec=ROOT/'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md'
s=spec.read_text(encoding='utf-8');start=s.index('**Bổ sung Minh duyệt07/11/2026:**');end=s.index('\n\n',start)
s=s[:start]+'''**Bổ sung Minh duyệt ngày 07/11/2026:** phần A trong `results/T-054/runs/hoan-thien-local-g3-011/h1-bo-sung-xin-duyet.md` cho sửa `src/p3/re3.py` và `results/T-054/scripts/worker.py` để nhận nghĩa mã gRPC tường minh, giữ kernel/tổng mã native và mặc định TT/Nezha; nối WHY/DECISIONS. Phần B cho đọc duy nhất column chunk (khối cột) `serviceName` của 30 trace và `container_name` của 30 log RE3 HF đúng revision; tổng metadata và chunk không quá 16 MiB. Chỉ xuất hợp tên toàn cohort, không phân bố theo ca hoặc tín hiệu/thời gian/message/ID/operation/statusCode. Đây là quyền metadata inventory riêng, không mở đánh giá RE3/G3/main. Snapshot và biên nhận ở checkpoint011.'''+s[end:];text(spec,s)
why=ROOT/'docs/WHY.md';s=why.read_text(encoding='utf-8');start=s.index('## T-054 — gRPC status và metadata inventory, 07/11/2026')
s=s[:start]+'''## T-054 — gRPC status và metadata inventory, 07/11/2026

Nguồn tác giả mới `CONVERT.md`, ghim riêng trong checkpoint011, nói benchmark phát hành lưu mã gRPC, 0 là OK; `tracets_err` gốc cộng mã thay vì đếm span lỗi. Guard H2 chỉ nhận 0/1 là giả định. Minh duyệt profile gRPC khai rõ và giữ nguyên giá trị/kernel; không chuyển thành 0/1. Code benchmark đã chọn không nâng phiên bản; converter mới chỉ làm bằng chứng hợp đồng nguồn. Gọi tổng mã là số lỗi sai nghĩa; đổi sang đếm lỗi sẽ đổi baseline. Đã kiểm fixture về miền mã, tổng và tuyến worker; chưa đọc statusCode RE3 thật.

Minh cấp quyền riêng đọc tên owner như metadata toàn cohort. Không dùng nhãn root hoặc phân bố theo fault để chọn U. Hợp tên quan sát không chứng minh deployment hay alias; nguồn thiếu giữ OPEN. Không áp đơn vị của converter mới cho release cũ khi schema khác. Lựa chọn này ảnh hưởng profile/khả năng hỗ trợ RE3 và hồ sơ G3, không chứng minh hiệu quả RCA hay cấp quyền main.
''';text(why,s)
dec=ROOT/'docs/DECISIONS.md';s=dec.read_text(encoding='utf-8');start=s.index('## T-054 — hoàn thiện local, guard gRPC và metadata owner, 07/11/2026')
s=s[:start]+'''## T-054 — hoàn thiện local, guard gRPC và metadata owner, 07/11/2026

Minh: “làm toàn bộ các phần còn lại, trừ phần kiểm ec2 ra vì hiện chưa vào được”. Tiếp tục chuẩn bị local; không kiểm/SSH/sync EC2, không phát main hoặc mở đánh giá RE3.

Sau đề xuất `results/T-054/runs/hoan-thien-local-g3-011/h1-bo-sung-xin-duyet.md`, Minh: “Duyệt sửa guard theo phần A” và “Duyệt đọc hai cột như metadata inventory”. A: sửa đúng `src/p3/re3.py` và `results/T-054/scripts/worker.py` cùng SPEC/WHY/sổ để hỗ trợ profile gRPC khai rõ, giữ mã/kernel cộng mã native. B: chỉ chunk `serviceName` của 30 trace và `container_name` của 30 log ở revision đã ghim, tổng metadata và chunk tối đa 16 MiB; chỉ xuất hợp tên toàn cục, không phân bố theo ca. Không đọc thời gian/metric/duration/message/ID/operation/statusCode hoặc chạy phương pháp trên RE3. Alias thiếu nguồn vẫn OPEN; không suy thành quyền đánh giá RE3/G3/main hoặc commit/push.
''';text(dec,s)

h1='''# RE3 trước G3 — bằng chứng và phần chưa phân xử, checkpoint011

Đây là chuẩn bị nguồn và adapter. Chưa đánh giá RE3; chưa có profile thật đủ điều kiện sử dụng. Không lấy việc cài H2 xong làm bằng chứng dataset đã được diễn giải đúng.

| Mục | Phân loại và bằng chứng | Hệ quả |
|---|---|---|
| Metric time | FACT: card HF đã ghim ghi Unix seconds. Guide tác giả mới mô tả bước lấy mẫu 1 giây cho RE2/RE3 | Không kiểm cadence thực bằng giá trị; không suy r từ mô tả chung |
| Trace startTime/duration | CANDIDATE cho release cũ: microseconds, phù hợp Jaeger và guide converter mới | Chưa có chứng cứ nối exporter lịch sử với đúng HF revision đủ rõ để đóng toàn bộ hợp đồng |
| Log timestamp | OPEN: converter mới xuất timestamp ns và time seconds; release HF có schema 3 cột | Không gán ns cho release cũ chỉ vì converter mới làm vậy |
| Status code | FACT theo lời tác giả: released datasets dùng gRPC, 0 OK; tracets_err cộng mã | Guard đã cho khai miền mã rõ; không tự nhị phân hóa hoặc gọi tổng mã là số span lỗi |
| Inventory quan sát | FACT: hợp serviceName/container_name của đúng 30 ca đã ghim có 11 tên | Không là deployment manifest hoặc bằng chứng đủ alias |
| Metric owner | FACT schema: 28 prefix; 17 tên ngoài hợp owner trace/log quan sát | Không tự xóa prefix hoặc ghép frontend-external vào frontend; cần nguồn/policy có lý do |
| U, alias, r | OPEN ở profile thật | Reader chặn profile thiếu; mọi kết luận RE3 phụ thuộc |

Hợp owner toàn cục: adservice, cartservice, checkoutservice, currencyservice, emailservice, frontend, paymentservice, productcatalogservice, recommendationservice, redis, shippingservice. Không công bố membership hoặc số dòng theo ca.

Quyền B: đúng hai cột owner, 60 lần đọc cột, tổng 1.380.569 byte trong giới hạn 16 MiB. Biên nhận ở `inventory-owner-global.json`: `/completed_column_reads`, `/budget/received`, `/union`, `/measured_signals_or_times_read`. Không lưu raw page/owner rows. Directory ZIP chỉ đọc metadata; không có deployment/collector manifest trong danh sách entry. Không mở file telemetry từ ZIP.

Nguồn chính: [phản hồi tác giả](https://github.com/phamquiluan/RCAEval/issues/64#issuecomment-6659996848), guide và converter ghim revision ở `upstream-main-ref.json`; dữ liệu HF giữ revision ở `hf-current-metadata.json`. Code benchmark đóng băng không nâng theo main upstream. Guide mới tự nói có khác biệt với scripts release cũ; không dùng sự giống tên cột thay provenance.

Khả năng hỗ trợ: M1, BARO, SimpleRCA, TraceRCA, MicroRank, CIRCA có tuyến RE3 trong H2 và kiểm bằng dữ liệu tổng hợp010. TORAI B có thêm kiểm gRPC011; TORAI A và các nhánh không khai trong ma trận RE3 không tự được bật. Chạy thật còn phụ thuộc profile/native units/owner policy, giao thức, ma trận vế, nguồn và quyền RE3 riêng. ERROR chưa biết giữ BLOCKED; không tự tính 0. Đây là hỗ trợ cài đặt có điều kiện, chưa xác nhận trên dữ liệu giữ ngoài.

Cần tác giả/người giữ nguồn trả lời: đơn vị từng cột của đúng HF revision; collector/exporter và cách lọc namespace của metrics; deployment/inventory gốc, ánh xạ frontend-external và các prefix khác; cách xác định độ phân giải quan sát r. Chưa gửi câu hỏi mới ra ngoài.

Hệ quả trước G3: chưa hoàn tất H1 theo điều kiện đã nêu. Có thể tiếp tục xin căn cứ nguồn. Nếu Minh muốn main TT/Nezha trước khi đóng H1, cần quyết định rõ việc để các mục trên OPEN tới trước đánh giá RE3 cuối; đây là thay đổi điều kiện trước G3 đang xin xét, chưa được tự coi là đã duyệt. Không có trở ngại này trong code main TT/Nezha đã tự kiểm, nhưng điều kiện quản trị nghiên cứu vẫn còn.
'''
text(RUN/'re3-h1-status.md',h1)
write(RUN/'re3-profile-open.json',{'schema':'T054-H1-PREPARATION-NOT-EXECUTABLE','status':'OPEN',
    'not_a_RE3_OB_PROFILE_1':True,'native_log_unit':'OPEN','trace_historical_exporter_provenance':'OPEN',
    'observation_r_ns':'OPEN','inventory_alias_metric_owner_policy':'OPEN','evaluation_granted':False})

storage_note=f'''# Đính chính dự toán dung lượng

27,5 GiB là dự toán bảo thủ đã cộng chồng các bản sao; không phải dung lượng đã sinh, không là yêu cầu bắt buộc. Dự toán cũ còn ở `storage-forecast.json` để giữ lịch sử và được thay bằng `storage-copy-accounting.json`.

Đã đo 41 attempt DEV hợp lệ, kiểm hash trước khi dùng, đo nén trong bộ nhớ. Ngoại suy một bản kết quả khoảng {storage['single_copy_empirical_bytes']/2**30:.3f} GiB; nhóm chưa có mẫu riêng dùng max cùng dataset và được đánh dấu fallback. Không chạy main/pilot test để ước tính.

| Mục cần giữ | Dự toán GiB |
|---|---:|
| Kết quả/trung gian native một lần, gồm bản nhận từ cloud; dự phòng 4 lần mức DEV | {storage['corrected_components']['native_once_local_or_received_4x']/2**30:.3f} |
| Archive nén truyền từ hai cloud; cùng dự phòng 4 lần | {storage['corrected_components']['retained_cloud_archives_4x']/2**30:.3f} |
| Tệp tạm của hai attempt đang chạy | {storage['corrected_components']['two_active_attempt_temp_4x']/2**30:.3f} |
| M1 seal cho 94 ca | {storage['corrected_components']['M1_seal_all94_4x']/2**30:.3f} |
| Báo cáo/metadata | 0.500 |
| Khoảng trống vận hành | 2.000 |
| Tổng | {storage['corrected_planning_bytes']/2**30:.3f} |

Mục đích là phân tích cơ chế từ trung gian, kiểm nguồn–attempt–receipt, nhận kết quả từ cloud và dựng bảng; không cần một clone toàn bộ kết quả chỉ để viết báo cáo. Không cấp thêm cả cohort retry khi chưa có quyền retry. Mọi attempt thật, kể cả hỏng, vẫn giữ. Dữ liệu nguồn hiện có đã nằm trên đĩa và không được tính thêm lần nữa vào dung lượng mới.

D còn khoảng {resource['D_free_bytes']/2**30:.2f} GiB tại lần đo cuối. Kịch bản khoảng 10,1 GiB vừa ổ D. Rút đề xuất tạo C:/RCA-artifacts/T-054/main-011/; chưa tạo đường dẫn đó, không xóa/di chuyển dữ liệu. Hệ số 4 là kịch bản, không phải cận trên đã chứng minh. Ca phức tạp hoặc retry được duyệt sau này có thể cần thêm; khi đó xét số thực, không tự xóa kết quả để ép vừa ổ.
'''
text(RUN/'storage-explained.md',storage_note)
text(RUN/'de-xuat-noi-nhan-ket-qua.md',(RUN/'de-xuat-noi-nhan-ket-qua.md').read_text(encoding='utf-8')+
    '\n\n## Rút đề xuất sau câu hỏi của Minh\n\nChưa được duyệt, chưa tạo đường dẫn C. Dự toán cũ cộng chồng bản sao; thay bằng `storage-explained.md` và `storage-copy-accounting.json`. Tiếp tục dùng D theo kịch bản mới, không cần duyệt thêm nơi lưu lúc này.\n')

dossier='''# Hồ sơ chuẩn bị G3 hiện hành — checkpoint011

**Chưa sẵn sàng phát main.** Phần local đã chuẩn bị và tự kiểm trong phạm vi được cấp; cloud tạm dừng theo Minh. H1 RE3 còn thiếu nguồn và cần Minh xét cách xử lý trước G3. Mọi quyền G3/main vẫn false. Hồ sơ này thay trạng thái vận hành006/008, giữ các bản lịch sử trong thư mục run và snapshot011/before.

Đọc `runs/hoan-thien-local-g3-011/bao-cao.md`, `re3-h1-status.md`, `storage-explained.md`, `prepared-validation.json`, `local-checks.json` và manifest011. Kế hoạch/mã nguồn hiện hành nằm trong checkpoint011; không dùng activation helper006 hay materialize_main005 cho plan011.

| Máy | Phân công ứng viên | Job | C-e thiếu hỗ trợ |
|---|---|---:|---:|
| EC2_1 | 35 TT: cùng họ M1, baseline và TORAI B | 523 | 2 |
| EC2_2 | 25 TT còn lại và toàn bộ 34 Nezha-OB | 817 | 0 |
| Laptop | TT: CIRCA, MicroRank và TORAI A | 300 | 0 |

Tổng 1.640 job và 2 vị trí C-e thiếu hỗ trợ; 68 UNSUPPORTED đã khai, tối đa 1.572 lần gọi được hỗ trợ. Không nhân world thành số lần học. Nguồn/ca/seed/cửa sổ/cấu hình/độ đo khoa học không đổi theo việc đóng gói011. Bản vá OB008 đã giải quyết guard mẫu cứng 5N/5A; không còn dùng điểm chặn006 ấy như lỗi hiện hành. Không suy từ đó ra hiệu quả RCA trên test.

Đã kiểm lại hash 406 tệp TT/OB và 180 CSV A bằng cách đọc byte, không giải mã tín hiệu. Các binding trước G3 vẫn là PREPARATION, không phải G3 attestation. Có 105 pin code; ba plan chặn WAIT_G3. Packet code/metadata đã tạo và kiểm nội dung ở local, chưa chuyển. Môi trường cloud trong contract là lịch sử008, phải kiểm lại khi AWS hoạt động.

## Nội dung Minh cần xét trong G3

1. H1: tiếp tục chờ nguồn để đóng units/U/alias/r; hoặc cho phép main TT/Nezha khi H1 còn OPEN, giữ cấm đánh giá RE3 đến khi hoàn tất nguồn và được cấp riêng. Phương án sau sửa điều kiện trước G3, chưa được coi là đã duyệt. H2/gRPC đã cài không thay quyết định này.
2. Policy ứng viên hiện có: timeout method 600 giây, C-d3 60 giây; tối đa hai worker khi RAM cho phép; một luồng số học; monitor 0,1 giây, gap phải nhỏ hơn 5 giây. Không trần cộng dồn theo quyết định đã có; lỗi chưa biết BLOCKED, dừng phát và báo; không retry tự động. Giữ một ca A thiếu toàn phần N của logts như hạn chế đầu vào đã khai006, không bỏ/bù/dịch ca. Quyền dùng A riêng phải được ghi rõ cùng nguồn.
3. Khi nguồn cloud/môi trường hiện tại được xác minh và phản biện/Minh xét hồ sơ xong: quyền khóa G3, mở đúng test TT/Nezha và phát main phải chỉ đúng candidate protocol/source bundle. Lệnh chuẩn bị local không thay các quyền này. RE3 giữ ngoài cho bản cuối; commit/push riêng.

Đây là các mục của G3 đã có, không thêm cổng nghiên cứu mới. Mẫu nguồn quyết định trong runbook chỉ là cấu trúc đề nghị, không phải quyền thật. `activate_after_g3.py` là helper ứng viên; chỉ kiểm đường chặn khi thiếu quyền, chưa chạy nhánh kích hoạt do chưa có grant thật. Không nhận nó là một lần main hay G3 đã thành công.

## Phần cloud còn lại, đang tạm dừng

Xác nhận máy/IP/identity; pin môi trường và upstream đã đóng băng; code packet; RAM/đĩa; dữ liệu thực có và phần thiếu theo phân vùng35/25/OB. TT cũ đã từng chuyển30/30 không tự đủ cho35/25; OB cần đúng226tệp trên EC2_2 nếu chưa có. Dùng lại tệp/hash hợp lệ, chỉ chuyển phần thiếu; không rerun baseline diện rộng. Không SSH/check/sync trong checkpoint011.

T-048 đã xong và kết quả tổng hợp local đã lưu; không phải chờ raw T-048 trên EC2 để cấp đầu vào main. Mất cloud ảnh hưởng khả năng tái kiểm toàn bộ raw lịch sử chưa sao lưu và phải dựng lại môi trường/nguồn còn thiếu; không đồng nghĩa mọi dữ liệu mất đều chặn main. Không mở lại nghiệm thu T-048 hay chạy lại vì đổi máy/phiên.

## Giới hạn câu hỏi nghiên cứu

Gói này chuẩn bị đánh giá RQ3b và phần can thiệp tính toán của RQ3d, chưa có kết quả test. RQ3c chỉ mô tả vùng; chưa có nhãn vùng độc lập. RQ3a/M1(b), Precision/Recall/F1 phát hiện công khai chưa được trả lời theo phạm vi đã quyết. LLM, quan hệ messaging/data đầy đủ và áp dụng FlashTicket thuộc các phần tiếp theo. DT18/cô vẫn yêu cầu chúng; chuẩn bị hoặc hoàn thành T054 không tự hoàn tất đề tài.
'''
text(OUT/'ho-so-g3.md',dossier)
runbook='''# Vận hành hiện hành — checkpoint011, chưa phát main

Đọc `runs/hoan-thien-local-g3-011/bao-cao.md`, `checkpoint.json`, `re3-h1-status.md` và `ho-so-g3.md`. EC2 tạm dừng theo Minh; không SSH/sync/kiểm trong phiên này. Không dùng plan/helper006 với pin011. H2/gRPC và OB source-native đã cài, nhưng H1, cloud và G3 còn mở.

Kiểm checkpoint chỉ đọc, từ repo D:/RCA-flashticket:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/hoan-thien-local-g3-011/verify_manifest.py
```

Plan ứng viên trong `011/prepared/` theo đường dẫn đầy đủ `runs/hoan-thien-local-g3-011/`; packet trong `packets/`. Không chạy lại prepare_local.py/package_candidates.py/check_local.py vào cùng thư mục: đầu ra create-only đã có. Không có queue main hoặc auto-resume nền. Tái dùng pin và kết quả kiểm hợp lệ; chỉ kiểm phần thay đổi hoặc trạng thái động trước chạy.

Đĩa: đọc storage-copy-accounting.json; khoảng10,1GiB là kịch bản có dự phòng, không cận trên. D đủ cho kịch bản tại lần đo. Đề xuất C rút lại, chưa tạo thư mục. Giữ mọi attempt/hỏng và raw kết quả; báo cáo không clone cả cohort. Mỗi lần nhận giữ archive truyền và một bản nhận có hash/receipt.

RAM: snapshot cuối thiếu cho slot lớn. Không giảm reservation để ép chạy và không tự tắt ứng dụng của Minh. Trước main đo lại; driver giữ reserve và chỉ phát khi đủ RAM, tối đa2worker. AC sleep đã đổi45phút thànhkhôngngủ; DC45phút giữ nguyên. Lệnh hoàn tác ở `011/restore-ac-sleep.ps1`; không tự khôi phục khi đang chạy cần thức.

Sau AWS hoạt động, chỉ tiếp tục kiểm/staging cloud khi Minh cho phép: kiểm identity, code, nguồn, môi trường, RAM/đĩa cho candidate011; dùng lại dữ liệu đã đúng, chuyển phần thiếu. Không suy haiIP lịch sử vẫn đúng. Lưu biên nhận current cloud gắn candidate protocol và packet hash. Không dùng receipt008 như current verification.

Sau Minh xét H1/policy và cấp G3/main/A nguồn riêng: lưu đúng lời quyết định, pin exact candidate protocol/sourcebundle và source quyết định. Grant cần g3/test_grant/main_dispatch/torai_A_source_grant=true; cloud_readiness_refs cho haihost; pre_G3_decisions_ref chỉ rõ policy được duyệt và H1 đã có nguồn hoặc được Minh chấp nhận OPEN cho main TT/Nezha. Không tự tạo true hoặc thay missing bằng lời tóm tắt.

Helper ứng viên011/activate_after_g3.py nhận --grant <filequyềnthật> --sha256 <hashđúng>; chỉ tạo metadata LOCKED/attestation/plan, khôngSSH hoặcphátqueue. Nhánh có quyền thật chưa được chạy; khi có quyền phải kiểm output và full locked validator, dừng nếu lỗi, giữ lượt hỏng và trình sửa ngoài quyền. Không gọi thành công kích hoạt chỉ từ kiểm đường chặn. Phần metadata khóa cuối và nguồn quyền phải được đưa/kiểm đúng từnghost trước lệnh run riêng theo CLI p7.py --help; không phát lệnh từ plan candidate.

Vận hành đã khai: per-method600s, C-d360s; một luồng số học, poll0,1s, gap<5s. Không trầncộngdồn, không tựretry. DRAIN dừng phát mới, giữ active đóng/ghi; resume cùng plan/root saukiểm PID/token, không suy SSHngắt là workerchết. Lỗi/chưa rõ nguồn/clock/monitor/RAMđĩa/khôngtiếntriển thìdừng/báo; lượtchưachạy khôngTIMEOUT. KhôngtạoScheduledTask/restartsaureboot.

Nhận/merge theo các receipt/phân vùng đã kiểm005: hash archive và từngtệp, giữ path/lineage và ánhxạ receive_paths, chỉmerge khiđủ union; nhãn evaluator ghép sau. M1sealtrướcC-d3; không phân bổ trùng. RE3 grant/profile/ma trận và bảng cuối riêng, không mở từ quyềnmainTT/Nezha. Khôngcommit/push hoặcxóaresult khi chưaMinhduyệt. PromptClaude trongLOG/011/prompt-claude.md đểMinhchuyểnthủcông.
'''
text(OUT/'runbook.md',runbook)

report='''# Báo cáo hoàn thiện local trước G3 — checkpoint011, 07/11/2026

Đã làm phần local được giao, không kiểm EC2. Chưa thể nói “chỉ còn cloud”: H1 RE3 vẫn thiếu căn cứ units/owner/alias/r; cần Minh xét trước G3. RAM tại lần đo cuối cũng thiếu cho slot lớn, là trạng thái động phải kiểm lại trước chạy. Không main, không đánh giá RE3 và không commit/push.

## Đã làm và tự kiểm

- Đọc nguồn tác giả mới, ghim tài liệu riêng; không nâng code benchmark đã đóng băng. Guard gRPC sửa đúng re3.py/worker.py sau duyệt A; 17 phép kiểm fixture đạt, gồm tổng mã native và prep worker. Kiểm profile/domain bằng Python 3.8 thật đạt. Không đọc mã status RE3 thật.
- Quyền B: 60 lần đọc cột owner, 1.380.569 byte; hợp 11 tên toàn cục. Không đọc tín hiệu/thời gian, không lưu raw pages hay phân bố theo ca. Hợp đồng H1/khả năng hỗ trợ và phần OPEN ở re3-h1-status.md.
- Kiểm 340 output010 còn đúng hash; 9 file code H2 khác không đổi. Dựng 105 pin hiện hành, cập nhật 3 plan có 523/817/300 job; 2 vị trí thiếu hỗ trợ giữ riêng. Nguồn 406 tệp main và 180 CSV A khớp byte/hash. Ba plan đều WAIT_G3, chưa có queue.
- Ba gói code/metadata local đã kiểm vòng đóng/mở archive và từng hash: 122/125/122 tệp. Không có raw data/nhãn evaluator, không gửi cloud. Có môi trường local đo mới; cloud chỉ có snapshot lịch sử với trạng thái chờ kiểm.
- Đổi AC sleep 2700s→0 và kiểm; DC không đổi, có script hoàn tác. Dự toán storage đã đính chính, không tạo thư mục C. Kiểm local 7 nhóm đạt về hợp đồng/pin/quyền; tài nguyên ghi WAIT_RESOURCE, không nhận sẵn sàng chạy.

Số liệu và con trỏ: grpc-check-001/summary.json#/checks; inventory-owner-global.json#/budget/received và /union; prepared-validation.json#/hosts; local-source-hash-validation.json#/main_files và /author_A_files; packet-validation.json#/packets; local-checks.json#/checks; storage-copy-accounting.json#/corrected_components. Hash/mã nguồn ở manifest, không chép từ trí nhớ.

## Dung lượng trả lời Minh

27,5 GiB trước đó là cách cộng chồng bản sao, không phải dung lượng bắt buộc. Đã đo nén 41 attempt DEV hợp lệ; ngoại suy một bản khoảng 1,713 GiB. Giữ dự phòng 4 lần, archive cloud, tệp tạm của 2 attempt, M1 seal, metadata và 2 GiB trống: tổng 10,062 GiB. D còn khoảng 15,52 GiB ở lần đo cuối, vừa kịch bản này. Chi tiết, mục đích và giới hạn ở storage-explained.md. Không clone toàn bộ kết quả cho report, không dành sẵn một cohort retry chưa được duyệt. Vẫn giữ mọi attempt thật/hỏng. Đề xuất C rút lại; chưa tạo, không cần duyệt đường dẫn này lúc này. Dự toán không phải cận trên đã chứng minh; có phát sinh thật sẽ báo.

## Quyết định và phần còn lại

DECIDED/USER_CONFIRMED: tiếp tục local, dừng kiểm EC2; A/B theo đúng lời Minh, ghi vào SPEC/WHY/DECISIONS. Không có quyết định mới về profile thật, G3 hoặc main. Nguồn statusCode gRPC được xác nhận bởi tác giả; hiệu quả RCA và diễn giải release cũ không tự được xác nhận theo đó.

OPEN: nguồn lịch sử RE3 và chính sách owner metric; Minh xét tiếp tục chờ căn cứ hoặc cho main TT/Nezha khi H1 còn OPEN tới trước RE3 cuối. Phương án sau chưa duyệt. Cloud trở lại phải kiểm/staging thật; RAM local đo lại. Policy/bản khóa/quyền G3/test/main/A riêng cần Minh xét; RE3 cuối có quyền riêng. Chuẩn bị không thay hiệu quả nghiên cứu: chưa có test để trả lời RQ3b/RQ3d; vùng/ngưỡng phát hiện và FlashTicket giữ phạm vi nguồn ở ho-so-g3.md.

Không tự mở task phản biện. Prompt trung tính chép mẫu ở prompt-claude.md và LOG để Minh chuyển Claude khi muốn. T054 vẫn đang chuẩn bị/chờ quyết định, không đóng task. Đề xuất nội dung commit sau khi Minh duyệt: “T054: refresh local G3 candidates, RE3 source contract and storage accounting”; chưa commit/push.

## File và tiếp nhận

Hai code: src/p3/re3.py; results/T-054/scripts/worker.py. Nối quyền/lý do trong SPEC/WHY/DECISIONS; LOG và đúng dòng T054 STATE. Sáu metadata hiện hành protocol/source-manifest/authorization/environment/ho-so-g3/runbook trong results/T-054; outputs011 và manifest. Snapshot trước và diff đủ để soát, không động file user ngoài phạm vi.

Chạy verify_manifest.py chỉ đọc trước dùng lại. Không chạy lại prepare_local/package/check_local vào output đã có. Bước tiếp: đọc H1+ho-so-g3 và xin Minh quyết phần OPEN; không SSH cho đến khi được resume. Không chạy activation/dispatch nếu chưa có quyền thật. Lệnh kiểm cuối lưu ở LOG; manifest liệt kê từng file/pin.
'''
text(RUN/'bao-cao.md',report)

# Exact common/stage/G3 blocks, replacing neutral placeholders only.
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
def block(section):return re.search(r'```text\n(.*?)\n```',template[template.index(section):],re.S).group(1)
common=block('## Prompt chung')
replacements=['T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md','soát kết quả','P7, G3(a)',
              'Codex làm; Claude phản biện theo SPEC',
              'AGENTS.md; docs/MRP.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; SPEC T-054 và các tài liệu được dẫn',
              'các bản REVIEW trong tasks/T-054-khoa-g3-chay-p7-a/ theo thứ tự; liệt kê trước khi đọc',
              'results/T-054/runs/hoan-thien-local-g3-011/; results/T-054/manifest-hoan-thien-local-g3-011.json; chạy verify_manifest.py bằng D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B',
              'chỉ đọc và trả lời trong chat; chưa được cấp file phản biện mới']
for value in replacements:common=re.sub(r'<[^>]+>',lambda _:value,common,count=1)
assert not re.search(r'<[^>]+>',common)
prompt=common+'\n\n'+block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n'
text(RUN/'prompt-claude.md',prompt)

checkpoint=read(RUN/'checkpoint.json')
checkpoint.update(status='LOCAL_CHECKPOINT_COMPLETE_H1_DECISION_CLOUD_AND_G3_PENDING',
    checkpoint_utc=datetime.now(timezone.utc).isoformat(),
    next='Read report/H1/G3 dossier and obtain unresolved source/Minh disposition; cloud remains paused. Verify manifest before reuse.',
    storage={'C_proposal':'WITHDRAWN_NOT_CREATED','planning_bytes':storage['corrected_planning_bytes'],'status':'SCENARIO_FITS_D_NOT_PROVEN_BOUND'},
    local_RAM_status=resource['RAM_status'],prepared_jobs=1640,positions=1642,main_started=False,cloud_checked=False)
write(RUN/'checkpoint.json',checkpoint)

state=ROOT/'docs/STATE.md';s=state.read_text(encoding='utf-8');lines=s.splitlines(True)
idx=next(i for i,line in enumerate(lines)if line.startswith('- **T-054'))
end=idx+1
while end<len(lines)and not lines[end].startswith('- **')and lines[end].strip():end+=1
lines[idx:end]=['- **T-054 — checkpoint011: local đã chuẩn bị/tự kiểm; H1, cloud và G3 còn mở.** Codex làm, Claude phản biện. Guard gRPC theo duyệt A; inventory owner theo B; pin/3 plan/packet và hash nguồn đã cập nhật. Dự toán10,1GiB vừa kịch bản ổD; rút đề xuấtC, chưa tạo. RAM lúc đo thiếu, cần kiểm lại trước chạy. H1 units/U/alias/r chưa đủ nguồn; cần Minh xét. Cloud tạm dừng, chưa main/đánh giáRE3. [011](../results/T-054/runs/hoan-thien-local-g3-011/bao-cao.md), [LOG](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md).\n']
text(state,''.join(lines))
log=ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md'
with log.open('a',encoding='utf-8')as f:
    f.write('''

### Kết thúc checkpoint011 — 07/11/2026 — Codex, người làm, Windows

1. Đã hoàn thiện chuẩn bị local được giao: nguồn H1 đã rà và ghi phần OPEN; A gRPC/B owner metadata theo duyệt; pin/plan/packet hiện hành; hash nguồn; storage/resource/sleep; hồ sơ G3/runbook/prompt. Không EC2/main/đánh giá RE3/commit/push. Báo cáo011 nêu đúng mức đạt, không tự nghiệm thu T054.
2. File: hai code re3.py/worker.py; SPEC/WHY/DECISIONS đúng quyền A/B; sáu metadata hiện hành của T054; outputs011/manifest; nối LOG, đúng dòng T054 STATE. Không sửa file user ngoài phạm vi. Quyết định của Minh trong phiên đã ghi sổ: tiếp tục local trừ EC2 và duyệt A/B. Câu hỏi27GB không duyệt đườngC; rút đề xuất, chưa tạo.
3. Kiểm:340outputs010 khớp;105pin hiện hành;406main+180A source hash; ba plan WAIT_G3;17fixture gRPC đạt và profile Python3.8 đạt; ba packet roundtrip đạt; ba grant thiếu bị chặn. Localchecks7nhóm đạt, RAM ghi WAIT_RESOURCE và storage chỉ SCENARIO_FITS_D. Nhánh activation có quyền thật chưa chạy; chưa thể nhận readiness toàn tuyến/cloud. Lượt hỏng lịch sử giữ nguyên. Diff011 so trước snapshot và manifest cuối nằm trong run.
4. Nguồn nghiên cứu: chưa có kết quả test trả lời RQ3b/RQ3d; H1 units/owner/U/alias/r còn thiếu nguồn. Minh cần quyết tiếp tục chờ nguồn hoặc thay điều kiện cho main TT/Nezha khi H1 còn OPEN; chưa tự áp phương án sau. Cloud chỉ kiểm sau resume; RAM phải đo lại. G3/main/A/RE3 grant riêng, không suy từ chuẩn bị. Các nghĩa vụ detector/vùng/LLM/FlashTicket còn như hồ sơ, không bị xóa vì task này.

Bước tiếp chính xác: tại D:/RCA-flashticket, chạy `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/hoan-thien-local-g3-011/verify_manifest.py`; đọc 011/bao-cao.md, re3-h1-status.md, storage-explained.md và results/T-054/ho-so-g3.md; trình phần OPEN cho Minh. Không chạy lại scripts create-only, không SSH hoặc activation/main nếu chưa có quyền thật. Không cần chạy lại baseline hợp lệ. Lệnh cuối dự kiến kiểm nhận checkpoint: chính lệnh verify_manifest.py trên; kết quả in trực tiếp, không sửa manifest sau kiểm. Lệnh trước khi ghi mục này: check_local.py, exit0.

Đề xuất commit khi Minh muốn: T054: refresh local G3 candidates, RE3 source contract and storage accounting. Chưa commit/push. Prompt bàn giao dưới đây để Minh chuyển thủ công; không tự mở/gửi phản biện.

```text
'''+prompt+'```\n')

# Complete approved diff, preserving the original pre-change snapshots.
diff=[]
mutable=list(checkpoint['before'])
for rel in mutable:
    before=(RUN/'before'/rel).read_text(encoding='utf-8-sig').splitlines(True)
    after=(ROOT/rel).read_text(encoding='utf-8-sig').splitlines(True)
    diff.extend(difflib.unified_diff(before,after,fromfile='before/'+rel,tofile=rel))
text(RUN/'complete-011.diff',''.join(diff))
log_before=(RUN/'before/tasks/T-054-khoa-g3-chay-p7-a/LOG.md').read_bytes()
assert log.read_bytes().startswith(log_before),'LOG must remain append-only'
outputs={p.relative_to(ROOT).as_posix():pin(p)for p in sorted(RUN.rglob('*'))if p.is_file()}
manifest={'schema':'T054-LOCAL-PREPARATION-011','outputs':outputs,
          'mutable_current':{rel:pin(ROOT/rel)for rel in mutable},
          'previous_manifest':{'path':'results/T-054/manifest-cai-re3-h2-010.json',**pin(OUT/'manifest-cai-re3-h2-010.json')},
          'main_started':False,'cloud_checked':False,'RE3_measured_signals_or_times_read':False,
          'H1_status':'OPEN_SOURCE_OR_MINH_DISPOSITION_REQUIRED','C_path_created':False}
write(OUT/'manifest-hoan-thien-local-g3-011.json',manifest)
print(json.dumps({'PASS':True,'outputs':len(outputs),'mutable_current':len(mutable),'main_started':False}),flush=True)
