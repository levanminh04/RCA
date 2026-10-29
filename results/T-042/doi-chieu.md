# Đối chiếu bài, code tác giả và pipeline repo

T-042, 24/10/2026. Đây là kết quả của người làm, chờ Claude phản biện và Minh quyết. Hash và revision đầy đủ tại `nguon.json` và `runs/reuse-audit-001/micro-source-checks.json`; không lấy tên phương pháp làm bằng chứng hai chương trình tương đương.

## 1. Phạm vi so sánh

| Thành phần | Bài/nguồn tác giả | Code và đầu vào repo | Mức đối chiếu được phép |
|---|---|---|---|
| SimpleRCA | FSE 2026, §3.1.2; Table 2 Nezha-OB Top@1/3/5 = 0,91. Luật metric nêu ví dụ 3σ hoặc P95; chưa khóa đơn vị alert, thời gian gộp và log threshold | M4 độc lập theo mô tả, WHY-17/33; 22 dev, S0 sigma/events, trace P95×3, log keyword >0 | Độ nhạy M4 và khác biệt đã định danh. Chưa tái lập chương trình sinh Table 2 |
| MicroRank | Nezha FSE 2023 §5.1–5.3.1, Table 3: service AS@1/3/5 = 41,07/48,21/62,5% trên 56 lỗi OB | Bản RCAEval sửa đầu vào, WHY-31: span3σ, nhóm trace rời nhau; PageRank/spectrum trích chính thức; full operation rồi max theo service | Lõi và can thiệp dev đã lưu. Chưa định danh code/config/normal source sinh Table 3 |
| BARO | Không có dòng BARO trên Nezha-OB trong hai bảng công bố đang đối chiếu | RCAEval `baro()`, RobustScaler fit trên N, max signed robust z của A; ordinal 5N+5A, max theo service | Đối chiếu hợp đồng/code và bảng dev. Không có mốc Nezha-OB tương ứng để nói tái lập |
| TraceRCA | Không có TraceRCA trong Table 3 Nezha; TraceAnomaly là phương pháp khác | RCAEval, `ji` từ support/confidence của span vượt 3σ; lọc hữu hạn trước sắp, max theo service, WHY-32 | Không mượn số TraceAnomaly làm mốc. Giữ phân biệt bản thư viện và pipeline tác giả khác ở T-034 |
| CIRCA | Không có mốc Nezha-OB tương ứng trong nguồn đang dùng | UNSUPPORTED theo Q-85: nền chỉ 1–2 phép đo thật, loader nội suy trước chia; nguy cơ đuôi train lấy anchor A ở 19/22 ca | Trạng thái đầu vào, không phải kết quả chạy CIRCA trên OB |
| TORAI B | Không có mốc Nezha-OB tương ứng trong nguồn đang dùng | UNSUPPORTED theo Q-85: thiếu statusCode, metric cadence khoảng 60s không hợp stride 15 hàng | Không giả status, đổi stride hoặc lấy đầu vào TT để cứu |

Nguồn số công bố: `results/T-017/sources/fse26-pages.txt` trang PDF 5 và 7; `results/T-008/sources/FSE2023_Nezha.pdf` trang 8–9, đã đọc trực tiếp. Nguồn baseline dev và UNSUPPORTED: `results/T-034/bang-baseline.json#/ranking_mode_a/Nezha-OB_main/methods`; hợp đồng Q-84/85 và WHY-37. Nội dung ghi trong khảo sát chỉ dùng như nhận định cần kiểm.

## 2. Tập ca, phiên bản, thời gian và đầu vào

| Trục | Nguồn công bố/code tác giả | Repo T-026 và T-042 | Kết luận |
|---|---|---|---|
| Cohort | Nezha báo 56 lỗi OB (42 resource, 14 code); FSE 2026 cũng mô tả 56. Chưa có danh sách đúng ca/chạy sinh bảng | 22 dev allowlist; 34 test không mở. Cùng toàn bộ 22 ca cho bốn nhánh | Cùng số lượng toàn bộ không chứng minh danh tính cohort hoặc release |
| Thời điểm | Code Nezha dùng inject_time; bài mô tả mỗi lỗi kéo dài 3 phút | Main theo Q-84; một ca có mốc metadata lệch, ba bảng độ nhạy cũ được giữ. Cửa sổ bao ngoài ±300s; không khẳng định mốc tiêm là onset vật lý | Khác thời gian/đồng hồ có thể góp phần; không tự dịch hoặc kéo cửa sổ |
| Metric | CSV Nezha có các nguồn, nhịp không đồng bộ và Node*; preprocessing chương trình sinh hai bảng chưa định danh | Time, không dùng TimeStamp; 11 nguồn/165 kênh, 5N+5A mỗi nguồn; 16/pod và 5 front. Alias tường minh, bỏ Node* vì chưa có ownership | Khác biệt có chủ đích Q-85. Chưa đo tác động riêng của bỏ Node* hay của nền dài |
| Trace | MicroRank gốc cần instance/operation, references, span.kind và nguồn SLO; code sinh Table 3 chưa có | CSV theo start/end ns, Duration µs; chỉ trả span start≥t−300 và end<t+300. M4 chia N/A theo start; MicroRank/TraceRCA theo end | Biên bao ngoài chung không đồng nghĩa membership N/A của các phương pháp giống nhau |
| Log | Ngưỡng và preprocessing sinh số SimpleRCA chưa khóa; Nezha dùng cấu trúc log/trace cho phương pháp riêng | TimeUnixNano và RFC3339 đối chiếu; alias PodName; chỉ keyword ERROR/FAIL/EXCEPTION, một count/dòng, một phiếu/service khi count>0 | Không tự coi là phát hiện spike đã hiệu chỉnh |
| Bản lặp, thiếu | Cách xử lý trong pipeline sinh bảng còn chưa biết | Giữ bản lặp, không nội suy/dedup chung; M4 bỏ nonfinite theo từng kênh, thiếu thì unavailable | Không đồng nhất số hàng với số quan sát độc lập |
| Nền | MicroRank bài/code gốc có hợp đồng normal/SLO riêng; chưa biết tác giả Nezha dùng bản/cấu hình nào | Metric N tối đa 300s nhưng chỉ 5 mẫu; trace/log thu quanh phút tiêm. Guard trace N là độ nhạy riêng ở T-026 | Chưa xác nhận N sạch, recovery hoặc tải ổn định. Không lấy construct_data thay normal |

Kiểm T-042: `runs/*/<opaque>-input-audit.json` so độc lập giá trị metric trong cửa sổ, membership/mapping/unit của trace và log, giữ bản lặp. Cả 22 ca đạt; `nguon.json#/scope` ghi miền nguồn. Không mở nguyên CSV ngày ra cho người phân tích; không lưu span/log/payload trong kết quả T-042.

## 3. SimpleRCA cùng tên nhưng khác đường chạy

Ba snapshot `orig`, `rcaeval`, `rcaeval_re3_ss` tại `D:/RCA-ext/work/T-017/sources-audit/github/` được pin trong download-manifest. Ba CLI đều đăng ký NezhaRCA. `orig` yêu cầu Python≥3.13 và rcabench-platform; adapter nhận sáu parquet N/A. Chưa định danh chuỗi CSV Nezha → sáu parquet → lượt sinh Table 2.

Ở `orig/src/simplerca/nezha_rca.py`, fusion top5 có trọng số (69–93), metric P95×1,19 cùng điều kiện tuyệt đối (139–162), trace P90>100ms (215–228). Fallback còn dùng parent-child (260–281). Chúng khác M4; chưa đo tác động bằng một phép giữ nguyên đầu vào. Không gọi mọi code cùng tên SimpleRCA là không dùng quan hệ.

M4 `src/simplerca/core.py:61` trở đi tính metric mean+3std(ddof0) hoặc P95 tuyến tính; mỗi giá trị A vượt ngưỡng là event, hoặc mỗi kênh có ít nhất một event là một channel vote. Trace/log mỗi service tối đa một phiếu mỗi nguồn. Tập ứng viên là union quan sát; score 0 vẫn có ở đáy khi có bằng chứng dương ở nơi khác; tổng toàn 0 thì abstain. Đây là chương trình cụ thể T-042 kiểm.

Code Nezha, RCAEval, BARO và hàm MicroRank trích có LICENSE MIT local. Ba tree SimpleRCA không có LICENSE/COPYING; không suy giấy phép root của artifact áp cho vendor. T-042 chỉ đọc các snapshot, không chép vào src hoặc phát hành lại.

## 4. Độ đo, hòa và mẫu số

Nezha định nghĩa AS@k ở mức service là root có trong top-k. FSE định nghĩa Top@K tương tự ở mức mô tả. Cả hai chỗ chưa khóa cách xử lý hòa đủ để đồng nhất evaluator. `pattern_ranker.py:601–622` dùng fault_number cho evaluator Nezha; nó không chứng minh MicroRank của Table 3 dùng đúng evaluator đó.

P3 giữ mọi trạng thái trong mẫu số; chấm kỳ vọng trong exact tie. T-042 gọi lại P3 và tính độc lập đủ 88 bản ghi. S0 có top1 native/lạc quan/bi quan đều 7/22, nên phá hòa không thể tự sửa top1 của S0 trên cùng danh sách. Cả bốn baseline chạy được trên bảng main OB đều 22 OK: bỏ ca ERROR không làm đổi mẫu số bảng này. CIRCA/TORAI giữ UNSUPPORTED riêng, không bị bỏ lặng.

Không quy riêng cho chấm phần chênh giữa chương trình chưa định danh. Cận SimpleRCA `(7+34)/56=0,7321` chỉ bác giải thích “chỉ khác tập ca” nếu dev là tập con đúng full56 và cùng Top@1. Với MicroRank, 23/56 làm tròn thành 41,07%; 23 ca đúng có thể nằm trong 34 ca còn lại về số học. Đây không là quan sát test hoặc lời giải cohort thực tế.

## 5. MicroRank: phần đã phân xử và phần còn thiếu

`src/microrank/__init__.py:45–61` học thống kê operation trước mốc theo end, làm tròn mean/std về ms và gán span ≥mean+3std; trace có ít nhất một span mang cờ vào nhóm A. Hai nhóm rời nhau đi vào đồ thị operation–operation/trace–operation, PageRank và DStar2 (85–103); operation cùng service lấy score cao nhất. Đồ thị có vai trò tính trọng số, không chỉ là hình minh họa.

Hàm PageRank/spectrum trích nguyên nguồn đúng PROVENANCE còn local. Clone đầy đủ ở scratchpad cũ không còn; không nhận là đã đọc lại toàn preprocessing upstream. T-032 đã thử bộ chia khác, đếm phủ và trọng số trên dev. `runs/reuse-audit-001/micro-source-checks.json` giữ pin và 465 kiểm file (các pin lõi, 88 observed, 352 metadata, 22 case analysis); không chạy lại phương pháp.

G2-H01/H02: nhánh bộ chia thay thế giúp một phần ca Nezha; quy ước lấy span đầu và công thức thay thế không phải toàn MicroRank gốc. Các phép đếm/trọng số dựa trên nhóm trace nhất định, không cộng hiệu ứng từ những nhánh khác đầu vào. Code/config, normal source, preprocessing, danh sách dự đoán từng ca và evaluator đúng lượt tạo Table 3 vẫn cần tác giả cung cấp.

## 6. Nhận định khảo sát được dùng

| Nhận định | Sau kiểm nguồn |
|---|---|
| §1.1: baseline repo lệch số công bố | Đúng về hai số được trích; chưa là so sánh cùng program/cohort/evaluator |
| A.1: chỉ cohort không đủ giải thích SimpleRCA | Đúng có điều kiện; S0 đã xác nhận 7 top1 chắc, không phải số xấp xỉ lấy từ 0,318 |
| A.1: chạy code tác giả chỉ vài phút theo 5s/ca | Không dùng làm ngân sách. Chưa định danh preprocessing; môi trường và schema khác. Chi phí dựng pipeline cần đo riêng |
| A.3: chưa có xử lý/giải thích MicroRank | Cần thu hẹp: T-032/G2 đã có can thiệp và giải thích một phần trong repo. Chưa giải thích đủ chênh Table 3 |
| KS-15: đối chiếu trước thiết kế | T-042 cung cấp phần đối chiếu hiện có và M4; pipeline tác giả còn là nghĩa vụ nối tiếp cần Minh quyết |
| Type III=0% nên không có chỗ cho quan hệ | Không suy ra được. Luật Type chưa đủ để gán từng ca dev; tỷ lệ công bố không phải nhãn đã kiểm hoặc phép đo lợi ích đồ thị |

T-042 không sửa khảo sát, G2, baseline hay kế hoạch hạ tầng. Bảng này là đề xuất diễn đạt khi dùng các nguồn đó cho P6/P7.
