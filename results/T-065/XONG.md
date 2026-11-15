# T-065 — nghiệm thu theo M4; G-a, G-b, G-c đạt

2026-11-15T06:29:45.805Z. Minh quyết tại docs/DECISIONS.md mục “M4 chiến dịch M1-FlashTicket: trả lời 9 câu hỏi”: nghiệm thu sau khi lưu ảnh S1 và bổ sung ảnh U1. Hai điều kiện ảnh đã đáp ứng: [S1](kiem/009-s1-anh-minh/GHI-CHU.md) và [U1](kiem/011-u1-anh-minh/GHI-CHU.md) được lưu nguyên byte, ghim manifest. Đây là ghi nhận quyết định đã có, không là quyết định mới của Codex.

- **G-a đạt:** điều hướng, cửa sổ, phát lại và lời diễn giải; giữ các giới hạn quan sát lịch sử.
- **G-b đạt:** lớp thao tác, bằng chứng và quan hệ quan sát đã kiểm; span link message chưa hỗ trợ.
- **G-c đạt:** P7/V082/V071 dùng chỉ mục bản 3; dữ liệu/API L11b và ảnh U1 bổ sung. Ảnh không có bảng đủ 64 cờ hoặc chuỗi bấm từ Mục lục; dùng đúng bằng chứng dữ liệu/API và luồng L8c ở phần không đổi.
- **L12 hoàn tất:** S2 thêm description panel 5 ở hai UID hiện hành, ghi rõ V082 vẫn dùng E1/E2/E5 trong lõi P7; target/query giữ. S4 nối nguyên khối L9 ở hai báo cáo. U2 nối đính chính nguồn brief L11b do điều phối soạn, Minh chuyển. **R4 đã được Minh xác nhận hồi tố** việc xóa folder RCA rỗng; không thêm thao tác folder.

[Báo cáo L12 và OPEN](kiem/012-s2-s4-u2/BAO-CAO.md), [đối chiếu](kiem/012-s2-s4-u2/doi-chieu.json), [hoàn tác](kiem/012-s2-s4-u2/HOAN-TAC.md), [prompt bàn giao](prompt-ban-giao.md). Grafana đã GET khớp hai description mới; giữ lượt kiểm nạp đầu hết thời gian, sau đó xác nhận chỉ đọc. Không restart.

**OPEN còn lại:** S3 — nguyên nhân booking-service vắng log, thiếu nguồn ứng dụng/Collector/nhãn/lưu giữ đúng giờ; cơ chế các quan sát (iii)/Start time lịch sử, thiếu request/response và trạng thái hiển thị đúng giờ; URL/breadcrumb khác nhau ở ảnh U1 đầu, chưa có dữ kiện phân xử. Hash cấp bản P7 null đúng nguồn; dev chưa cấp đáp án ở lớp phát lại; span link chưa có dữ liệu; bookmark thời gian số cũ cần chọn ca lại/link ISO. Đọc phần OPEN trong báo cáo để thấy giả thuyết, bằng chứng thiếu và hệ quả.

T-065 hoàn thành phần giao diện minh họa/truy vết của DT18-NV3; hiệu quả phương pháp và RQ5/P10 không được đóng bằng nghiệm thu giao diện. Không có quyết định nghiên cứu mới; không ghi STATE/docs/SPEC/REVIEW/T-064. Chưa commit/push.
