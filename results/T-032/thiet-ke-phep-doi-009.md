# T-032 — Thiết kế bản 009: bộ chia trace theo công thức của bài MicroRank gốc, với span đầu do ta quy ước (việc 4)

Viết ngày 11/10/2026, trước khi đếm và trước khi chạy. Người viết: Claude. Căn cứ: gói bổ sung 007 việc 4 và bản sửa việc 4 (Q-134, Q-135; nguyên văn ở cuối `goi-bo-sung-007.md`). Tên gọi dùng trong mọi kết quả: **"công thức của bài gốc với span đầu do ta quy ước"**. Không gọi là MicroRank gốc.

## 1. Câu hỏi

Bản MicroRank đang dùng (biến thể "MicroRank-RCAEval sửa đầu vào") xếp một trace vào nhóm bất thường khi có **bất kỳ span nào** vượt mức nền cộng 3 lần độ lệch chuẩn. Khoảng một nửa trace sau mốc rơi vào nhóm bất thường (KQ9 mục 2), và phần lớn các trace đó không gắn với dịch vụ gốc (`ket-qua-phien-11.md` mục 2.2). Bài gốc chia theo cách khác: so thời gian của **cả yêu cầu** với mức dự kiến. Câu cần trả lời: hạn chế lớn nhất của MicroRank trên hai dataset thuộc bước chia trace của bản thư viện, hay thuộc cách tính của bài.

## 2. Nguồn, đã đọc trực tiếp

Code `IntelligentDDS/MicroRank` bản ghim `efd85e8e` (đọc ở phiên 11, dòng mã ghi ở `goi-bo-sung-007.md` phần "Bản sửa việc 4" mục 2); bản chữ của bài; `results/T-015/ho-so-microrank.md`; hai luật đã cài sẵn và đã kiểm ở `src/microrank/detectors.py`.

- Thời gian cả yêu cầu: tổng thời lượng các span của `frontend` có nhãn server. Trace không có span như vậy bị bỏ khỏi cả hai nhóm.
- Mức dự kiến: tổng, qua mọi span của trace, của (mức nền của thao tác + k lần độ lệch chuẩn). Bài và hàm báo động mức hệ thống: k = 1,5. Hàm chia nhóm của code: k = 1, cộng thêm 50 ms cho mỗi trace.
- Mức nền của thao tác: trung bình và độ lệch chuẩn tổng thể của "thời lượng span trừ tổng thời lượng các span con trực tiếp", tính theo mili giây, làm tròn 4 chữ số; học trên đoạn bình thường; bỏ trace có span thiếu cha; bỏ trace mà span đầu sau khi trừ dài hơn 1 giây.

## 3. Điều tôi đã thấy trước khi viết

- Toàn bộ KQ9, KQ10 và `ket-qua-phien-11.md` mục 1–2.
- Tôi đã mở bảng span của hai ca (một ca mỗi dataset) để xem trường span cha, vì thiết kế phụ thuộc cách dữ liệu đánh dấu span đầu. RE2-TT ca `dev-12a1a88069`: span đầu có trường cha trống; 2.728/2.731 trace có đúng một span đầu; 3 trace không có span đầu và có span mất cha; span đầu thuộc nhiều dịch vụ khác nhau (không có dịch vụ tên `frontend`). Nezha-OB ca `dev-14701a3bbb`: span đầu có trường cha ghi chữ `root`; 1.481 span như vậy trên 1.478 trace, tất cả thuộc dịch vụ `frontend`. Vì đã thấy hai ca này, tôi dự đoán mốc 90% ở mục 5 sẽ đạt; mốc vẫn giữ như đã duyệt.
- Bảng span mà phương pháp nhận không có cột loại span (server, client) ở cả hai dataset.

## 4. Quy ước (chỗ thay cho thứ dữ liệu không có)

- **Span đầu:** span khai báo không có cha: trường cha trống (RE2-TT) hoặc ghi `root` (Nezha-OB). Ở Nezha-OB mọi span đầu thấy được thuộc `frontend`, nên quy ước gần với luật gốc; ở RE2-TT span đầu thuộc dịch vụ mà bộ sinh tải gọi vào, không có `frontend`.
- **Span mất cha:** trường cha có giá trị nhưng không tìm thấy span đó trong bảng của ca. Span mất cha **không** được coi là span đầu.
- **Thao tác:** giữ định danh của biến thể đang dùng (tên dịch vụ + tên phương thức), không đổi sang cách cắt tên của code gốc, để chỉ đổi đúng bước chia trace.

## 5. Bước đếm, làm trước, không chạy phương pháp

Script `scripts/trace_root_census_v1.py` trên EC2, đọc đúng 52 bảng span của lượt `chain-spanpass-001`. Mỗi ca ghi:

- số trace sau mốc (có ít nhất một span kết thúc từ mốc trở đi) có 0, 1, từ 2 span đầu; số trace có span mất cha; số trace có span ở cả hai phía của mốc;
- với trace có đúng một span đầu: tỷ lệ trace mà span đầu bao trọn mọi span khác về thời gian; tỷ lệ trace đủ span (không mất cha) mà tổng "thời lượng trừ tổng span con" của mọi span bằng đúng thời lượng span đầu (đẳng thức phải đúng 100% nếu cài đúng);
- dịch vụ của span đầu;
- số span mà "trừ tổng thời lượng span con" khác "trừ phần được span con che";
- đoạn nền: số trace nằm trọn trước mốc, số bị bỏ vì mất cha hoặc không có span đầu, số bị bỏ vì span đầu sau trừ dài hơn 1 giây; số thao tác xuất hiện ở trace sau mốc mà không có mức nền theo cách học này.

**Mốc dừng (đã duyệt, Q-135):** ca có dưới 90% trace sau mốc mang đúng một span đầu thì ghi N/A cho hai nhánh ở mục 6. Dataset có hơn một nửa số ca N/A thì dừng cả dataset và ghi là hạn chế của dữ liệu. Đơn vị "từng ca" và quy tắc "hơn một nửa" là lựa chọn của người làm.

## 6. Hai nhánh, chạy sau khi bước đếm đạt

Chạy trên laptop như phép M-D (lý do nơi chạy: WHY-43), bằng `scripts/laptop_contrast_v5.py` tạo từ bản v4. Bước duy nhất bị đổi: hai tập trace "bất thường" và "bình thường" đưa vào phần sau của phương pháp. Mọi phần sau (đồ thị, PageRank, đếm phủ, spectrum, ánh xạ sang dịch vụ) giữ nguyên.

| Nhánh | Luật | Nguồn |
|---|---|---|
| `shamp` | giữ nguyên hai tập của bản đang dùng, đi qua đúng chỗ móc | phải khớp bản đóng băng từng bit ở 52/52 ca |
| `mo15` | thời gian cả yêu cầu > tổng (mức nền + 1,5 lần độ lệch chuẩn) | bài; hàm báo động của code |
| `mo1p50` | thời gian cả yêu cầu > tổng (mức nền + 1 lần độ lệch chuẩn) + 50 ms | hàm chia nhóm của code |

Chi tiết cài đặt, theo code gốc trừ chỗ ghi rõ:

- Thời gian cả yêu cầu = tổng thời lượng các span đầu của trace (code gốc cộng). Trace sau mốc không có span đầu: bỏ khỏi cả hai nhóm (như code gốc).
- Số lần xuất hiện của thao tác trong trace đếm trên mọi span của trace có trong bảng của ca, kể cả span kết thúc trước mốc. *Lựa chọn của người làm:* code gốc đếm trong cửa sổ phát hiện của nó; ở đây đếm đủ trace để mức dự kiến không bị hụt với trace nằm vắt qua mốc.
- Mức nền học trên các trace nằm trọn trước mốc, với ba chi tiết của code gốc ở mục 2. Đoạn nền chỉ dài 300 giây (RE2-TT) và 41–97 giây (Nezha-OB), trong khi tác giả khuyên khoảng một giờ.
- Hai luật gọi nguyên hàm `expected_duration` của `src/microrank/detectors.py`. Thao tác của trace sau mốc không có mức nền: hàm báo lỗi, bản ghi thành ERROR (code gốc cũng hỏng ở chỗ này). Không lấp giá trị.
- Nếu một trong hai nhóm rỗng, phương pháp trả trạng thái không có trace bất thường hoặc không có trace bình thường như bản đang dùng; ghi nguyên trạng thái, không ép xếp hạng.

## 7. Dự đoán khai trước và cách đọc

- **Nếu hạn chế thuộc bước chia của bản thư viện:** tỷ lệ trace bất thường giảm mạnh so với bản đang dùng (trung vị 0,50 ở RE2-TT, 0,33 ở Nezha-OB), các trace bất thường còn lại phần lớn chứa root, và root lên hạng ở phần lớn ca sai.
- **Nếu hạn chế thuộc cách tính của bài (đếm phủ, trọng số):** dù nhóm bất thường sạch hơn, thứ hạng của root gần như không đổi.
- **Nếu công thức không áp được trên dữ liệu này:** nhiều ca ERROR vì thiếu mức nền, hoặc một nhóm rỗng. Khi đó ghi là hạn chế của dữ liệu và của quy ước, không kết luận về bài gốc.
- Báo: số ca root tăng hạng, không đổi, giảm hạng; Hit@1 và Hit@5 tính bi quan khi hòa; tỷ lệ trace bất thường; số cặp (thực thể đứng trên root, root) còn và mất; số ca theo từng trạng thái. Mẫu số giữ đủ 52 ca; ca N/A, ERROR, nhóm rỗng nằm trong mẫu số và được đếm riêng.
- Hai luật báo riêng, không chọn luật theo kết quả.

## 8. Giới hạn

- Kết quả chỉ nói về "công thức của bài gốc với span đầu do ta quy ước" trên dev. Nó không tái lập MicroRank gốc: thiếu nhãn loại span, định danh thao tác khác, đoạn nền ngắn hơn nhiều, bộ lọc 1 giây đặt cho hệ khác.
- Hai nhánh được nghĩ ra sau khi đã xem kết quả dev của bản đang dùng; chỉ là bằng chứng trên dev cho một ứng viên.
- Phép đổi làm đổi cả tập trace lẫn số trace của hai nhóm, nên là tác động tổng của bước chia.

## 9. Đầu ra

- EC2 `~/rca/T-032/runs/trace-root-census-001/` (bước đếm); laptop `results/T-032/runs/microrank-partition-001/` (ba nhánh) và `collect-001/summary.json`.
- Script: `scripts/trace_root_census_v1.py`, `scripts/laptop_contrast_v5.py`, `scripts/laptop_contrast_collect_v4.py`.
- Diễn giải: `ket-qua-phien-11.md` mục 4.
