import pathlib, datetime, hashlib, json
ROOT=pathlib.Path(__file__).resolve().parents[4]; RUN=pathlib.Path(__file__).parent
stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
targets=['docs/DECISIONS.md','docs/WHY.md','docs/STATE.md','tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md']
before=RUN/'control-before'; before.mkdir(exist_ok=False)
rows=[]
for rel in targets:
 p=ROOT/rel;b=p.read_bytes(); q=before/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 rows.append({'path':rel,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
(RUN/'control-before.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
def append(rel,text):
 with (ROOT/rel).open('a',encoding='utf-8',newline='') as f:f.write(text)
assert '| Q-144 |' not in (ROOT/'docs/DECISIONS.md').read_text(encoding='utf-8')
append('docs/DECISIONS.md','\n| Q-144 | 12/10/2026 | Minh trực tiếp cho phép Codex lập và thực hiện trong cùng phiên một gói bổ sung toàn bộ câu còn kiểm được và có giá trị P5/P6 của T-032 và T-033, kể cả T-033 đã đóng; không tạo task mới, không chờ duyệt riêng từng bước. Minh giao Codex quyết cách làm/phân phối phần độc lập song song, phần phụ thuộc tuần tự trên hai EC2/laptop, ưu tiên EC2; cho laptop khi môi trường tái lập hoặc chuyển dữ liệu lớn gây chờ. Cho dùng tối đa subagent, kiểm hỗ trợ GPT 6.1 Sol ultra; chạy dài/qua đêm phải báo thời gian trực tiếp và yêu cầu giữ laptop khi có tiến trình. Giữ mọi kết quả cũ, chỉ thêm kết quả và văn bản nối; không mở test/heldout, commit/push hoặc xóa file cũ. Chỉ dừng hỏi nếu tải lớn thực sự cần, phải thay/xóa kết quả quan trọng và không có phương án giữ an toàn. Báo cáo cuối minh bạch mọi câu nguồn, phép kiểm, giới hạn dữ liệu/phương pháp và phần còn có thể kiểm; không bỏ khó vì task đã đóng. Quyền này thay riêng các yêu cầu chờ duyệt/tách task/laptop của gói bổ sung, không thay luật chung hay nghiệm thu lịch sử. Phạm vi: hai thư mục runs/bo-sung-toan-dien-20261012-001 dưới results/T-032 và results/T-033; LOG hai task chỉ nối; DECISIONS/WHY chỉ nối lựa chọn gói; STATE chỉ hai dòng task. | Lời Minh trong chat12/10/2026 bắt đầu “CHỐT gom một gói bổ sung”; README gói chung |\n')
assert '## WHY-49 ' not in (ROOT/'docs/WHY.md').read_text(encoding='utf-8')
append('docs/WHY.md','''
## WHY-49 — Phân xử các câu còn giá trị T-032 trong gói bổ sung chung

Minh cho thực hiện theo Q-144. Thiết kế chi tiết trước kết quả: results/T-032/runs/bo-sung-toan-dien-20261012-001/t32/design.md và README gói; file cũ chỉ đọc.

**Chọn:** matched windows/đại lượng nền và sau mốc cho return/exception, tính mọi dịch vụ trước nối nhãn; MicroRank lưu đầy đủ partition→graph→W→counts→DStar→service-max, can thiệp W×counts ở cùng support đủ điều kiện, đối chiếu native/M-D/nhánh ghép và ca đúng; CIRCA giữ tập nút và cha để tách độ dài học khỏi vị trí học/phân phối và giai đoạn chấm; probe định vị tín hiệu trên cạnh so owner-span, giữ dấu và báo missing; kiểm mã tác giả TraceRCA và TORAI A nếu dữ liệu cho phép. Phép cũ đã hợp lệ tái dùng.

**Vì sao:** các nhánh trước đổi nhóm trace hoặc cửa sổ nên chưa quy riêng trọng số/đếm, đáp ứng do lỗi, nguyên nhân độ nhạy hoặc thông tin quan hệ. Không hạng1 không chứng minh không có tín hiệu. Mỗi phép cần chuỗi trung gian và đối chứng tương ứng; thiếu support không biến thành số0.

**Phương án khác:** chỉ so hạng/đếm cờ (không phân xử); loại return hoặc ca thiếu cạnh (bỏ nhóm quan trọng); chạy baseline mới và thay bảng P3 (trái mục tiêu giữ nguồn); coi bản một đặc trưng là tái lập đầy đủ tác giả (sai đầu vào); dùng data giữ ngoài/test (chưa được phép). Các kiểm physical host/network/clock không có trường cần thiết được chứng minh giới hạn thay vì dựng nguyên nhân.

**Bằng chứng trước phép mới:** SPEC, kiem-tiep hiện tại, đầu ra T032 và MRP RQ2/P4/P5/P6, DT18/cô, LESSONS. Mọi kết quả mới CHƯA KIỂM khi ghi mục này; các giả thuyết có thể sai khi tín hiệu yếu/coverage không tương đương/support đổi hoặc nhánh khác cùng tạo chênh lệch.

**Kết luận phụ thuộc:** phân loại D/G/A/M; căn cứ đề xuất thành phần/quan sát P5/P6. Không khóa phương pháp mới, không chứng minh graph thắng/test hoặc định nghĩa nhãn lan vật lý. Lựa chọn chi tiết và các nhánh phát sinh được ghi thiết kế trước kết quả trong gói, cập nhật lý do chính thức khi khác nội dung này.

## WHY-50 — Phân xử các câu còn giá trị T-033 trong gói bổ sung chung

Minh cho thực hiện theo Q-144. Thiết kế trước kết quả nằm trong results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/; nguồn/cấu hình/số P3 cũ giữ nguyên.

**Chọn:** native sham từng ca trước nhánh mới; kiểm công thức NIW/Student-t và marginal nhất quán giữa các chiều bằng covariance principal submatrix, không dùng submatrix precision hay zero-padding. Fixed-X/d xét riêng dof=d+1→d+3, kappa1→4, precision I→4I như độ nhạy, không coi đó là lựa chọn tối ưu hay lời giải contrast mask cũ. Tiền xử lý causal: schema cung cấp độc lập nhãn, ffill quá khứ, fixed-scale sau100quan sát và expanding prequential, kiểm suffix invariance, zero-range/missing/state semantics. Đầu vào lặp: compress các vector lặp và ánh xạ elapsed-time, so hazard theo hàng và theo khoảng thời gian để tách đồng hồ khỏi đếm quan sát. N-Sigma đối chiếu history rolling100/expanding cùng raw/k/cột và joint flags của OR, std0/NaN; chấm đường nhạy endpointD trên cờ cũ; đọc toàn message/coverage của vùng khóa và probe vai trò quan hệ.

**Vì sao:** νnative=d+1 chưa tự là prior khác ở common dimensions; cùngX/cờkhác cần xét state. Lookahead đã xác nhận không tự chọn được pipeline online. Lặp84%ô chưa chứng minh tác động. Mốc/endpointproxy không phải onset/end thật. Causal contract không tự bảo đảm nhất quán tọa độ posterior khi scale đổi; nếu không đạt thì giữ đúng lỗi mô hình/diagnostic, không chọn P6.

**Phương án khác:** gán effect mask cho prior (không cô lập); zero-padding (mô hình khác); sweep tham số theo accuracy (thiên vị); gọi compressed row là một giây (sai đồng hồ); gọi INFO/success là nền sạch (không có chuẩn); đograph với feature/budget khác (không cô lập cấu trúc). Mức100/4/d+3 là diagnostic khai trước, phải nói giới hạn và kiểm độ nhạy cần thiết khi kết luận đổi dấu, không thêm ngưỡng theo điểm đẹp.

**Bằng chứng trước phép mới:** nguồn BARO/code frozen, SPEC, report002/kiem-tiep, bo-sung-bao-cao hiện tại, MRP/DT18/cô/LESSONS. Các nhánh mới CHƯA KIỂM; có thể không tách tác động hoặc không đủ chuẩn vật lý. Prior/state phép tính và fixture được agent ultra kiểm độc lập trước dùng số.

**Kết luận phụ thuộc:** căn cứ P6 về preprocessing/history/prior/clock và yêu cầu quan sát FlashTicket. Accuracy thật, onset/recovery, báo giả vận hành và lợi ích graph chỉ khẳng định khi có dữ liệu/đối chứng thích hợp; gói này không tự đóng RQ2/G2 hay mở test. Giữ mọi lỗi/non-OK, mẫu số/coverage riêng, không coi thời điểm phụ thuộc là quan sát độc lập.
''')
opening=f'''\n### Gói bổ sung chung 12/10/2026 — mở phiên {stamp}\n\nIntent EXECUTE; USER_CONFIRMED Q-144: Minh trực tiếp giao Codex thực hiện mọi câu còn kiểm được và có giá trị P5/P6 của T032/T033, không tạo task mới, không chờ duyệt, giữ kết quả cũ. Codex là người làm gói bổ sung; giữ SPEC/vai trò lịch sử. Ba subagent hỗ trợ, không mở vòng phản biện chính thức. Thiết kế/lựa chọn WHY49–50 trước dùng số. Phạm vi và phân công ở results/T-032/runs/bo-sung-toan-dien-20261012-001/README.md. EC2 kết nối được, T32 disk19GB/T33disk1.4GB, mỗi máyRAM~7.1GB; chỉ outputm/CP/thống kê nhỏ ở T33. T32laptop một worker tuần tự MicroRank/CIRCA, ETA ban đầu25–50phút; Minh đã được báo giữ máy. Mọi file cũ/results/native/code/env/test giữ nguyên; LOG này chỉ nối. Snapshot kiểm toàn vẹn đang chạy, không là phép nghiên cứu. Không commit/push.\n'''
for rel in targets[3:]:append(rel,opening)
p=ROOT/'docs/STATE.md';s=p.read_text(encoding='utf-8');lines=s.splitlines(keepends=True)
for i,l in enumerate(lines):
 if l.startswith('| T-032 |') or l.startswith('| T-033 |'):
  cols=l.rstrip('\r\n').split('|'); cols[6]=cols[6].rstrip()+'; bổ sung chung Q-144 đang chạy12/10, giữ kết quả/nghiệm thu cũ; xem LOG và runs/bo-sung-toan-dien-20261012-001/ '
  lines[i]='|'.join(cols)+'\n'
p.write_text(''.join(lines),encoding='utf-8',newline='')
print(json.dumps({'timestamp':stamp,'changed':targets,'decision':'Q-144','why':['WHY-49','WHY-50']},ensure_ascii=False))
