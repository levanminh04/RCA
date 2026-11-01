# Nhật ký T-046

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

- SPEC bản 1 do Claude (phiên người làm T-045) soạn trong chat ngày 01/11/2026; Codex rà trong chat cùng ngày: bốn điểm CHẶN (C-e vẫn tham gia chọn và chồng lấn A/A; metric Nezha-OB không làm A/A được; e = 1 không đo đúng bão hòa; ứng viên chưa đặc tả đủ phạm vi). Người soạn nhận cả bốn là đúng, thêm ba điểm tự tìm (N1 tiêu chí phản ứng tầm thường với V0; N2 thứ tự ưu tiên thiếu lý do; N3 chi phí), sửa thành bản 2. Không còn bất đồng giữa hai bên.
- Minh duyệt SPEC bản 2 ngày 01/11/2026 (lời Minh: “duyệt tạo spec luôn, kèm prompt cho phiến claude mới độc lập hoàn toàn yêu cầu triển khai 46, trước khi triển khai cần tự rà soát spec độc lập dựa trên các thông tin đã có, nếu có vấn đề hoặc rủi ro lỗ hỏng, bỏ khó chọn dễ, thì cho phép sửa lại spec rồi mới bắt đầu triển khai task”). Lượt kiểm lại bản 2 của Codex không làm. Dòng DECISIONS cho lời duyệt này và cho phân công (Q-224) chưa ghi.
- Người làm: Claude, một phiên mới độc lập với phiên soạn SPEC. Người phản biện: Codex.
- Prompt triển khai (do phiên soạn SPEC trình trong chat, nguyên văn):

```text
Đọc AGENTS.md, làm task T-046 trong STATE.

Bạn là người làm T-046 (tasks/T-046-cong-verdict-thang-diem/SPEC.md), một phiên Claude mới, độc lập với phiên đã soạn SPEC. Người phản biện là Codex. Nguồn là file trong repo; không dùng lịch sử chat hay bộ nhớ của phiên khác (AGENTS mục 4).

Làm theo thứ tự:
1. Mở phiên theo AGENTS mục 6. Ghi dòng mở phiên vào tasks/T-046-cong-verdict-thang-diem/LOG.md.
2. Trước khi chạy bất cứ thứ gì, tự rà SPEC độc lập: đọc SPEC T-046, SPEC T-043 (B1.3, B1.7, B4, B6, Phụ lục C, D), LOG T-045 phiên 2 (gói quyết định bản sửa theo lượt 2), tasks/T-045-chay-khoi-k-dev/REVIEW-2-claude.md, results/T-045/bao-cao.md, docs/WHY.md (WHY-06, WHY-56, WHY-66), docs/DECISIONS.md (Q-205, Q-211, Q-216–Q-223), docs/LESSONS.md, MRP P6, DT18, hướng dẫn của cô, và code src/m1/e4.py, xep_hang.py, chuoi.py, runner.py. Tìm: chỗ sai hoặc mâu thuẫn với nguồn; rủi ro và lỗ hổng (nhất là đường lọt nhãn, chọn thiết kế theo số dev, dữ liệu dùng hai lần); chỗ SPEC chọn việc dễ bỏ việc khó; phép kiểm không đo được điều nó nói đo; tiêu chí có thể đạt bằng cách làm đầu ra mất tác dụng.
3. Ghi kết quả rà vào LOG mục "Rà và sửa SPEC" trước khi làm bước nào khác. Có vấn đề thì sửa SPEC theo quyền ở đầu SPEC: ghi đoạn cũ → đoạn mới, lý do, ảnh hưởng. Không đổi mục tiêu hay câu hỏi nguồn; không nới tiêu chí hay bỏ phép kiểm cho dễ đạt; không thêm quyền đọc root, tính MRR hay mở dữ liệu khóa; không chọn ứng viên. Sửa nào làm tiêu chí lỏng hơn hoặc thu hẹp phạm vi thì dừng, trình Minh. Nếu không thấy vấn đề, ghi rõ đã rà những gì và vì sao không sửa.
4. Sau đó triển khai SPEC từ bước 0. Dừng ở D-1 và D-2 theo SPEC; dừng khi lượt chạy dự báo quá 1 giờ (luật cứng 8); dừng khi cần sửa src ngoài phạm vi bước 9. Ghi mọi lần nhìn số dev vào results/T-046/so-lan-nhin.jsonl. Khóa tổ hợp cổng × verdict (ghi LOG kèm hash) trước khi xem C-e. Không đọc root, không tính MRR.
5. Commit src chỉ sau khi Minh duyệt WHY ở D-2, mỗi thay đổi một commit. Commit kết quả, LOG, STATE và push chỉ khi Minh duyệt.
6. Ghi tệp bằng chế độ nhị phân hoặc giữ đúng ký tự xuống dòng gốc (Path.write_text trên Windows đổi LF thành CRLF). Giờ trong LOG lấy từ đồng hồ máy (lệnh date), không ước lượng.
7. Cuối mỗi lượt báo đủ bốn mục của AGENTS mục 7; cuối phiên ghi mục kết thúc phiên vào LOG, cập nhật dòng T-046 trong STATE, soạn prompt phản biện cho Codex theo docs/review-prompt.md (Prompt chung + khối "Soát kết quả" + khối G3).
```
