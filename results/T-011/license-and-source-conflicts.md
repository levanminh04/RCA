# Các nguồn còn mâu thuẫn — chưa giải quyết thay tác giả

Kiểm 03/10/2026, cập nhật theo Q-47. URL chính xác, thời điểm lấy, revision và hash nằm trong [manifest cũ](runs/run-001/manifest.json) và [nguồn hiện hành](runs/source-final-001/manifest.json). **Không có quyết định chọn license.** Kiểm nội bộ phi thương mại có giao quyền cả NC/ND theo [báo cáo mới](xac-minh-nguon-va-doc-lap.md); không chia sẻ dataset/payload đã biến đổi. OT bỏ khỏi phạm vi mới; các dòng OT dưới đây chỉ giữ bằng chứng lịch sử.

| Nguồn đã lưu | Phát biểu quan sát | Phạm vi/giới hạn |
|---|---|---|
| Bốn `*__README.md` HF | Frontmatter `license: cc-by-nc-4.0`; cuối `cc-by-nd-4.0: NoDerivatives` | Hai điều khoản khác nhau ngay trong cùng card, không chỉ HF tag tự sinh |
| `code__README.md` | Intro NC; mục License ND | Không tự chọn câu ở cuối vì “cụ thể hơn” |
| `code__LICENSE` | Creative Commons Attribution-NonCommercial 4.0 | Không đủ xóa mâu thuẫn với tuyên bố dataset ở nguồn khác; baseline vendored có thể có license riêng |
| `paper-v4.html`, Appendix F; `author-site.html`/`author-catalog.html` | CC BY-ND 4.0 cho dataset | Paper có ký hiệu license bài riêng; không trộn với license dữ liệu |
| `itrust-terms.html` | Yêu cầu attribution/thông báo công bố; không chia sẻ dataset cho người khác dù public/private | Terms upstream SWaT/WADI không bị license LEMMA ghi đè |

**Tác động hiện hành:** tiêu chí 1 về license chính xác vẫn OPEN. Hai legalcode đều cấp quyền sao chép và kiểm nội bộ phi thương mại; ND không cấm tạo bản chuyển đổi nội bộ nhưng hạn chế chia sẻ bản chuyển đổi. Vì vậy có thể làm hành động kiểm hẹp đã được Q-47 duyệt sau ghi lý do, không chọn một license. Quyền phân phối dataset/phái sinh không được suy từ phép kiểm này; nguồn mâu thuẫn vẫn cần tác giả làm rõ. Bốn HF PR sửa license còn OPEN và theo hai hướng khác nhau, không phải xác nhận chủ dữ liệu. Xem snapshot/đối chiếu đầy đủ trong báo cáo mới. Không gửi email/form trong task.

Các chênh nguồn khác cần giữ đúng phạm vi:

- Product Review: tên fault trong HF card khác cách gọi ngắn của paper §3.1; cần mapping từng ngày, không đoán nhóm resource/network/code từ tên.
- WADI: catalog LEMMA ghi 9 faults; nguồn iTrust A1 ghi 15 attacks; code có 14 khoảng và 14 nhóm root, trong đó 6 nhóm nhiều root. Appendix D nói chọn single-target. Có thể là release/subset/phạm vi đánh giá khác; chưa có mapping chứng minh, không coi chúng là cùng census rồi chọn một số.
- SWaT: iTrust A1 41 attacks; LEMMA catalog 16 faults. Có thể là lọc subset; cần danh sách mapping, không gọi 16 là toàn bản gốc.
- Dung lượng: site LEMMA ghi PR 765G, Cloud 540G, SWaT 236M, WADI 848M; paper Table 2 ghi OT 4.47G/5.67G. ZIP HF đo bằng file metadata là đại lượng khác. Không suy tỷ lệ nén, thiếu file hoặc lỗi tác giả khi chưa cùng revision/đơn vị.
- `www.lemmarca.info` được paper v4 dẫn nhưng request trong run-001 lỗi SSL; lỗi giữ trong manifest. Trang `lemma-rca.github.io` và repo chính thức truy cập được. Chưa coi site mới chết vĩnh viễn hoặc tự thay nội dung.
- Nhãn riêng Cloud 20240124: epoch quy đổi thành 09:10:51 UTC; `inject_time` là 03:10:51 không kèm timezone. Chênh 6 giờ nếu giả sử chuỗi UTC; giả sử đó chưa xác minh. [label-time-check.json](runs/run-001/label-time-check.json) ghi phép tính, không đổi nhãn. Quy tắc JST→UTC trong HF card áp cho PPTX, không tự áp cho JSON này.

Không thay MRP/WHY/K3 từ các phát hiện này. Nội dung cần đưa vào tài liệu chính thức sau duyệt: phạm vi license và nhãn, timezone, trace còn OPEN, và khác biệt giữa census file với census incident.
