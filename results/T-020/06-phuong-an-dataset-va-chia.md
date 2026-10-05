# Ba cấu trúc dataset và cách chia — CANDIDATE, chờ WHY/chưa duyệt

Các phương án được tạo sau bảng chín tiêu chí, không chọn theo kết quả method. Không gói nào hiện chứng minh đủ tiêu chí9 cả ba trục. “Giữ ngoài ứng viên” trong CSV chỉ giữ dữ liệu chưa đọc; **không xác nhận bộ đó đủ điều kiện**. Chọn gói khác không tự cho phép mở test.

## Quy tắc tái lập

Seed 20261004 đã ghi trong SPEC trước triển khai. Hash `seed|dataset|root|fault` sắp thứ tự ô; ô TX2 ép dev, một phần ba ô còn lại làm dev (làm tròn lên), phần còn lại test. Không phân tầng bằng topology suy từ đo. RE2-TT giữ nguyên10 ô/30 ca dev và20 ô/60ca test từ allowlist v1; không mở khóa. Giữ ngoài nguyên bộ. Dùng public-census nhãn đã cứu trong results, không raw.

Chạy `py -3 -X utf8 -B results/T-020/scripts/chia_theo_o.py`. [Assertions](runs/split-assertions.json) kiểm cùng ô một phía, identity/cell census bằng nhau, không TX2 ở test/giữ ngoài, v1 30/60 còn nguyên. CSV có từng identity và nguồn. TX1-test là lựa chọn **chờ D3**; phương ánC tránh TX1-test.

## A-da-tin-hieu (chờ WHY)

[CSV theo ca](chia-theo-o/A-da-tin-hieu.csv)

| Dataset | Phía | Ô | Ca/đơn vị nhãn | Ô chỉ1repeat | Repeat min–max | Tiếp xúc |
|---|---|---:|---:|---:|---|---|
| RE2-TT | dev | 10 | 30 | 0 | 3–3 | {'TX2': 30} |
| RE2-TT | test | 20 | 60 | 0 | 3–3 | {'TX0': 60} |
| RE2-OB | dev | 30 | 90 | 0 | 3–3 | {'TX2': 90} |
| RE3-TT | dev | 3 | 10 | 0 | 3–4 | {'TX0': 9, 'TX1': 1} |
| RE3-TT | test | 5 | 20 | 0 | 3–6 | {'TX0': 20} |
| Nezha-OB | dev | 11 | 18 | 4 | 1–2 | {'TX1': 18} |
| Nezha-OB | test | 22 | 38 | 6 | 1–2 | {'TX1': 38} |
| Eadro-SN | dev | 12 | 12 | 12 | 1–1 | {'TX1': 12} |
| Eadro-SN | test | 24 | 24 | 24 | 1–1 | {'TX1': 24} |
| OpenRCA-Bank | giu-ngoai-ung-vien | 52 | 136 | 15 | 1–6 | {'TX0': 136} |

Mục đích: so nhiều nguồn tín hiệu và hệ khác nhau; RE2-TT là bộ đa tín hiệu có nhãn/clock đã kiểm, RE2-OB dev là hệ nhỏ hơn, RE3-TT thêm lỗi code. Nezha-OB bổ sung10 root và33 ô khác nguồn; Eadro-SN bổ sung12 root/36 ô ở hệ khác, normal riêng. Hai họ ngoài RCAEval còn OPEN giấy phép áp dataset; vai trò **đề xuất có điều kiện**, không phê duyệt chạy. Bank136 nhãn/52 ô chỉ dự phòng metadata; C9, header thực và bất biến revision chưa đủ. Nezha-TT không dùng test trong A vì45 label records còn xung độtclock, không được gọi45 physical injections.

RQ1 và RQ3b có cấu trúc so theo fault/root/candidate, chưa đo hiệu quả. RQ3a b vẫn chưa có protocol continuous sạch được xác lập. RQ3d kiểm đồ thị thật/ngẫu nhiên/no-graph được nếu adapters/graph coverage đủ; static TT một mình không phân xử. RQ3c cần FlashTicket. Phương pháp metric/RCD/CIRCA cần adapter; MicroRank/TraceRCA cần trace; TORAI/SimpleRCA cần modality xác định; GDN cần normal calibration mới. Chi tiết variant ở V5. Mất: test Nezha/Eadro đã TX1, bộ giữ ngoài chưa đủC9, Eadro mỗi ô một repeat.

## B-kien-truc-khong-trace (chờ WHY)

[CSV theo ca](chia-theo-o/B-kien-truc-khong-trace.csv)

| Dataset | Phía | Ô | Ca/đơn vị nhãn | Ô chỉ1repeat | Repeat min–max | Tiếp xúc |
|---|---|---:|---:|---:|---|---|
| RE2-TT | dev | 10 | 30 | 0 | 3–3 | {'TX2': 30} |
| RE2-TT | test | 20 | 60 | 0 | 3–3 | {'TX0': 60} |
| RE1-SS | dev | 22 | 110 | 0 | 5–5 | {'TX2': 100, 'TX1': 10} |
| RE1-SS | test | 3 | 15 | 0 | 5–5 | {'TX1': 15} |
| RE2-SS | dev | 30 | 90 | 0 | 3–3 | {'TX2': 90} |
| RE3-SS | dev | 3 | 10 | 0 | 3–4 | {'TX1': 10} |
| RE3-SS | test | 6 | 20 | 0 | 3–4 | {'TX1': 20} |
| RE3-OB | giu-ngoai-ung-vien | 10 | 30 | 0 | 3–3 | {'TX0': 30} |

Mục đích: so graph dựng từ kiến trúc khi trace vắng với graph trace của TT. RE1/2/3-SS có trace 0 trên census đã kiểm, không phải adapter thiếu. BARO/NSigma/RCD và CIRCA kiến trúc chạy có điều kiện; TORAI thiếu log RE1 phải ghi fallback; SimpleRCA reduced-modality riêng; MicroRank/TraceRCA không chạy ở SS. RE3-SS bổ sung code. RE3-OB chưa đọc đo nhưng cùng họ nên **không đạt C9 độc lập**, chỉ dự phòng ngoài thiết kế. LEMMA-PR/Cloud là nhánh kiến trúc phụ **chưa chia/không chạy**: census incident×root×fault OPEN, Original schema OPEN, NC/ND và clock xung đột; không biến4/6 date captures thành ô. Chọn nhánh LEMMA cần Minh quyết D2 và input tác giả.

RQ1/RQ3b hỏi được tác động thiếu trace theo cấu hình rõ; không suy đây là paired causal effect của bỏ trace giữa hai hệ khác nhau. RQ3a modeb vẫn chưa; RQ3d kiến trúc có điều kiện graph independentlyspecified; RQ3c chỉ FlashTicket. Mất: bộSS cùng họ, RE1SS chỉ3testcells nên bootstrap lặp đi lặp lại rất ít support; nhiềuTX2 chỉ dùngdev/tái lập, không test. LEMMA không đủ nhãn/schema/licensing để làm dataset RCA chính.

## C-test-TX0 (chờ WHY)

[CSV theo ca](chia-theo-o/C-test-TX0.csv)

| Dataset | Phía | Ô | Ca/đơn vị nhãn | Ô chỉ1repeat | Repeat min–max | Tiếp xúc |
|---|---|---:|---:|---:|---|---|
| RE2-TT | dev | 10 | 30 | 0 | 3–3 | {'TX2': 30} |
| RE2-TT | test | 20 | 60 | 0 | 3–3 | {'TX0': 60} |
| RE1-TT | dev | 9 | 45 | 0 | 5–5 | {'TX0': 45} |
| RE1-TT | test | 16 | 80 | 0 | 5–5 | {'TX0': 80} |
| RE3-OB | dev | 4 | 12 | 0 | 3–3 | {'TX0': 12} |
| RE3-OB | test | 6 | 18 | 0 | 3–3 | {'TX0': 18} |
| Eadro-SN | dev | 36 | 36 | 36 | 1–1 | {'TX1': 36} |
| Nezha-OB | dev | 33 | 56 | 10 | 1–2 | {'TX1': 56} |
| OpenRCA-Bank | giu-ngoai-ung-vien | 52 | 136 | 15 | 1–6 | {'TX0': 136} |

Mục đích: test chỉ TX0, đổi độ rộng đa tín hiệu test lấy độ sạch tiếp xúc. Nezha/Eadro chỉ dev để hiểu cơ chế (license vẫnOPEN); RE1-TT metric-only đánh graph kiến trúc, RE3-OB code chưa đọc; Bank dự phòng chưa đủheldout. RE1-OB **không** đưa vào test: localRE1OB125đã TX2 có40copyproven FSE và85identitylocal↔HF OPEN; không suy safe từ125HFcộtTX0/TX1. Không dùng raw giải alias ởtask này.

RQ1/RQ3b test rộng cell hơn nhưng chưa mởschemaRE3OB/RE1TT; multi-signal test chủ yếuTT, giới hạnRCAEval-family. RQ3a/b không tăng độ hợp lệ chỉ nhờTX0. RQ3d graph-family generalization chưa phân xử đủ; RQ3c chỉ FlashTicket. Mất: nguồn khác nhóm ngoàiRCAEval chỉ dev, khó kết luận chuyển hệ mới, C9 vẫnOPEN.

## Vai trò những ứng viên còn lại

RE1-SS gồm 100 ca TX2 và 25 ca TX1; RE2-SS/RE2-OB và BARO-FSE-OB đã TX2. Các ô có TX2 chỉ dùng dev hoặc tái lập, không giữ ngoài; vai trò các ô còn lại theo từng CSV. Benchmark FSE propagation có 10 event (8 valid, 2 invalid), AnoMod có 26 captures, DeepTraLog có 132485 trace labels; không suy F-code để tạo ô RCA service. Chỉ dùng tác vụ phụ/tái lập có điều kiện nhãn và quyền sử dụng. TRCA và Nezha chung byte-lineage, không là hai dataset độc lập. LEMMA Original và Preprocessed chung lineage; Preprocessed đã TX1. LEMMA OT đã loại theo Q-47, không mở lại.

OpenRCA Telecom/Market, OpenRCA2.0 ba hệ, TrainTicketTrace, LO2v1/v2 còn metadata/schema/census/task hoặc quyền công bố OPEN như bảng V2; không tự chọn vì khác tên. LO2 trace classification một-span không thay service-root RCA. Xem [C9 từng trục](trung-gian/dataset_evidence/independence-axes.csv) và [schema giữ ngoài](trung-gian/dataset_evidence/heldout-schema-provenance.md) nếu có; các nguồn chính đã ghi trong CSV V2. Mọi ứng viên đều đánh bằng cùng C1–C9.

## Độ chắc của bootstrap theo ô

Ô root×fault là đơn vị gom cụm đề xuất để resampling, chưa được chứng minh độc lập thống kê. Không dùng ca, span hay file-minute như các đơn vị độc lập. RE3-TT có 5 ô test, RE3-SS có 6, RE3-OB có 6/10 và RE1-SS có 3: báo từng ô, khoảng tin cậy chỉ thăm dò. Eadro-SN có 24 ô test nhưng mỗi ô một repeat, không ước lượng được biến thiên trong ô. Nezha có 22 ô test, 6 ô một repeat; Bank có 52 ô census, 15 ô một repeat và nhãn theo 9 ngày. Chung session/workload có thể gây phụ thuộc. P7 cần nêu giả định gom cụm và sensitivity; không trộn các chế độ nhãn.

## Khuyến nghị và phản chứng (chờ WHY)

Đề nghịA làm cấu trúc dự kiến đa nguồn phù hợp yêu cầu mở rộng dataset public, kèm trạng thái **chưa đủ đóngG1** do license/schema/C9. Nếu Minh muốn test chỉ TX0 thìC; nếu câu hỏi chính cần đồ thị kiến trúc khôngtrace thìB. Lập luận chốngA mạnh nhất: TX1 đã ảnh hưởng thiết kế và nguồn khác họ chưa đủpermission/heldout; nhiềuroot không tự chứng minh topology lan truyền. Đổi khuyến nghị khi inputimmutable/license/provenance chứng minh bộ ngoài có nhãn/candidates/normal thích hợp và ba trục độc lập, hoặc khi Minh chọn định nghĩatestnghiêm hơn ởD3. Không chọn theo accuracy hoặc công adapter.

V7 đã cho phép đọc đúng dòng tiêu đề nếu bảo đảm dừng ngay sau dòng đầu và không giải nén. Artifact Bank hiện không có local, đường Drive/ZIP chưa có cơ chế đáp ứng điều kiện đó. Vì vậy chỉ có schema từ bài, chưa kiểm tiêu đề thật. Cần nguồn bất biến có dòng tiêu đề truy cập được theo V7; không tải dữ liệu đo hoặc giải nén để lấp chỗ trống.
