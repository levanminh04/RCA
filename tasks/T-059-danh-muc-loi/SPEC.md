# T-059 — Danh mục lỗi FlashTicket: định nghĩa (chặng 1c)

- **Trạng thái:** đã duyệt (11/11/2026). Minh (chat 11/11): "t59 codex làm, t61 claude làm, ... nếu không có bất đồng quản điểm thì duyệt ghi". Phản biện SPEC: Codex lượt 1 và lượt 2, Claude đáp (chat 11/11); điểm CHẶN cuối về nhãn đã sửa theo lời Codex.
- **Người làm:** Codex
- **Người phản biện:** Claude
- **Thuộc gói MRP:** P10 (FlashTicket), trước đợt phát triển — **Cổng:** chưa có cổng riêng; dẫn tới khóa thiết kế FlashTicket.
- **Mã task:** T-059 giữ cho B4 theo PLAN Q8 (Minh "đồng ý"). SPEC này chỉ phủ phần định nghĩa danh mục. Phần dựng bộ tiêm, sổ tiêm lỗi, kiểm telemetry và các đêm chạy nền (chặng 3) sẽ thêm bằng một lần sửa SPEC trình Minh ở chặng 3.

## Mục tiêu

- `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.9, luật chống thiên lệch 1: khai danh mục kịch bản và quy tắc nhãn trước khi chạy.
- MRP §4 và WHY-04: chia đợt phát triển và đánh giá theo ô (vị trí × họ lỗi).
- D.11: trả lời được câu hội đồng "hệ tự thiết kế có thiên vị không".
- `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` chặng 1c: bảng này quyết định nhóm phải viết code gì (việc 2i ở `VIEC-CHO-QUYET-VA-LAM.md`).

Task là **thiết kế trên giấy**. Không tiêm lỗi, không kết luận phương pháp phát hiện được lỗi nào. Đạt task này đủ căn cứ để giao việc 2i và để dựng bộ tiêm ở chặng 3; chưa đủ căn cứ về chi phí đợt phát triển.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Cần phân xử | Phép kiểm, bằng chứng | Phần thiếu, quyết định phụ thuộc |
|---|---|---|---|
| 1. Mỗi họ lỗi trong 11 kịch bản của D.9 có vị trí hợp lệ nào (D.9 "kiểm kê vị trí có ý nghĩa", "không tạo vị trí giả") | Vị trí có thật trong luồng gọi hay không | Đọc code, compose của repo nhóm (chỉ đọc). Mỗi vị trí ghi: file và dòng, revision của service (đối chiếu revision đang chạy trên `exp-app`, R-10), thao tác trong kịch bản tải kích hoạt nó, chiều gọi | Vị trí cần mock hoặc cần thêm luồng tải: ghi thành yêu cầu 2i; ô chỉ được tính dùng được khi yêu cầu đó xong. Ví dụ VNPay: dựng URL thanh toán hay có mock chưa chứng minh tải đi qua cạnh `payment-service → VNPay`; lời gọi đi có ở thao tác hoàn tiền và truy vấn hoàn tiền |
| 2. Tách cơ chế ở cùng hoặc gần vị trí (D.9: pool, DB, đường mạng là can thiệp riêng) | Hai cơ chế ở cùng chỗ có tách được không | Mỗi ô ghi riêng: vị trí tiêm, cơ chế dự định, kết quả đầu dò độc lập | Xem quy tắc nhãn dưới bảng |
| 3. Telemetry hiện có có thấy lỗi không (R-01–R-10; sổ khắc phục T-058) | Ô nào thiếu quan sát | Đối chiếu từng ô với R-01–R-10 và các mục KP | Thiếu quan sát thì ghi giới hạn; không đổi nhãn thật (D.9) |
| 4. Cần code, cấu hình gì | Phần việc cho nhóm | Theo từng ô: cờ lỗi, chuỗi kết nối qua Toxiproxy, mock VNPay, quyền `NET_ADMIN` cho netem | Gửi nhóm qua `yeu-cau-code-nhom.md` |
| 5. Nhãn và thời lượng chu kỳ | Quy tắc nhãn khai trước; độ dài pha nền, lỗi, hồi phục | Nhãn cạnh: tách đáp án thật, tập đáp án chấp nhận chung cho mọi phương pháp, bảng định vị cạnh. Nếu tác động chỉ đo ở endpoint thì ghi đúng "ảnh hưởng endpoint". Độ dài pha căn vào khoảng lấy mẫu thật trên `exp-obs` (đọc chỉ đọc), cửa sổ ±300 giây của M1, thời gian luật cảnh báo cần | Số lấy mẫu thật chưa kiểm khi viết SPEC |
| 6. Chia đợt | Ô nào thuộc phát triển, ô nào thuộc đánh giá | Mặc định chia theo ô (MRP §4, WHY-04, D.9). Họ chỉ có một vị trí: dành cho đánh giá hoặc khai giới hạn, theo D.9. Đợt phát triển phải có đủ: tải tăng mà hệ khỏe; lỗi ở tải cố định; cùng lỗi dưới tải khác | M7 (cho lặp ô ở cả hai phía) vẫn là ngoại lệ OPEN trong `VIEC-CHO-QUYET-VA-LAM.md`; task không cần M7 để bắt đầu |
| 7. Xác nhận can thiệp | Lần tiêm có thật sự tạo ra cơ chế dự định không | Mỗi cơ chế ghi: thao tác cụ thể; đầu dò độc lập (không thuộc tín hiệu RCA, ví dụ thống kê Toxiproxy, `docker inspect`, k6); kết quả nào xác nhận; khi nào ghi "chưa xác nhận". Tách số đo đầu dò khỏi dấu hiệu RCA dự kiến thấy | — |

**Quy tắc nhãn khi hai cơ chế khó tách.** Giữ riêng vị trí tiêm, cơ chế dự định và kết quả đầu dò độc lập. Nếu đầu dò chưa xác nhận được cơ chế, ghi "can thiệp chưa xác nhận". Nếu đầu dò đã xác nhận nhưng telemetry của RCA không phân biệt được hai cơ chế, giữ nguyên nhãn thật và ghi giới hạn ở trường "đáp án có thể phân biệt".

**Ca đối chứng flash sale không lỗi.** Cho phép `root = null`. Ghi lịch tải và tiêu chí độc lập để xác nhận hệ còn khỏe. Nếu tăng tải làm hệ suy giảm thật, ghi nhận tình trạng đó trước khi chấm báo động giả.

## Đầu vào

- `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.1, D.9, D.11; `docs/MRP.md` §4; `docs/WHY.md` WHY-04.
- `docs/techstack/PLAN-TRIEN-KHAI.md` §5 (sổ tiêm lỗi), §7; `docs/techstack/KE-HOACH-GIAI-DOAN-2.md`; `docs/techstack/VIEC-CHO-QUYET-VA-LAM.md`.
- `tasks/T-043-thiet-ke-rca-m1/SPEC.md` B1.9 (hợp đồng P10).
- `results/T-040/yeu-cau-quan-sat-p9.md` (kiểm hash theo `results/T-040/manifest.json`); `results/T-058/` (sổ khắc phục, `dem-2026-11-10/`, kiểm hash theo `artifacts-sha256.json`).
- Repo `D:/Project/flash-ticket-platform`: chỉ đọc.
- `exp-app`, `exp-obs`: chỉ lệnh đọc (cổng, kết nối, quyền container, cấu hình lấy mẫu). Khóa và cách vào: `results/T-058/may-chu-va-truy-cap.md`.

## Đầu ra

`results/T-059/`:
- `danh-muc-loi.md`: bảng ô, trả lời câu 1–7, quy tắc nhãn, ca đối chứng, phương án chia đợt.
- `danh-muc-loi.json`: cùng nội dung dạng máy đọc; làm khung cho sổ tiêm lỗi ở chặng 3.
- `yeu-cau-code-nhom.md`: phần gửi nhóm cho việc 2i.

## Phạm vi ghi

- `results/T-059/`
- `tasks/T-059-danh-muc-loi/LOG.md`
- Dòng T-059 trong `docs/STATE.md`

## Các bước

1. Liệt kê vị trí của từng họ lỗi, có dẫn chứng code, revision, thao tác kích hoạt, chiều gọi — kiểm: mọi vị trí có đủ bốn trường.
2. Tách cơ chế, ghi đầu dò độc lập và quy tắc xác nhận cho từng cơ chế — kiểm: hai cơ chế cùng chỗ có đầu dò phân biệt, hoặc áp đúng quy tắc nhãn ở trên.
3. Đối chiếu quan sát với R-01–R-10 và các mục KP.
4. Ghi nhãn, ca đối chứng, thời lượng pha (có số lấy mẫu thật) và phương án chia đợt.
5. Soạn yêu cầu gửi nhóm.

## Kiểm đúng đắn

- Đối chiếu hash đầu vào cũ theo manifest; lệch thì dừng phần phụ thuộc.
- Mỗi vị trí kiểm được trên code ở đúng revision đang chạy.
- Không đưa nhãn vào phương pháp: bảng này là đầu vào của bộ tiêm và bộ chấm, không là đầu vào của M1 ở chế độ tự phát hiện (luật cứng 6).

## Tiêu chí xong

- 11 kịch bản D.9 đều có dòng, kể cả ca đối chứng `root = null`.
- Mỗi ô có: vị trí (file, dòng, revision, thao tác kích hoạt, chiều gọi), cách tiêm, cơ chế dự định, đầu dò xác nhận, đáp án thật, tập chấp nhận và bảng định vị khi là cạnh, quan sát mong đợi và chỗ thiếu, phần code cần thêm.
- Họ một vị trí được đánh dấu theo D.9.
- Minh duyệt bảng.

## Không làm

Tiêm lỗi; dựng Toxiproxy, Pumba; sửa FlashTicket; quyết M7; tính chi phí đợt phát triển (chặng 3, OPEN theo D.9).

## Chi phí ước lượng

Khoảng 1–1,5 ngày agent. Không chạy máy, không tải dữ liệu. Không thuộc luật cứng 8.

## Rủi ro và điều chưa chắc

- Chưa kiểm: Pumba, Toxiproxy chạy trên ARM; netem cần `NET_ADMIN`.
- Cạn CPU trên một máy dùng chung ảnh hưởng mọi service; đáp án có thể không phân biệt được — áp quy tắc nhãn, không đổi nhãn thật.

## Prompt bàn giao

Người làm soạn theo `docs/review-prompt.md` sau lượt báo cáo.
