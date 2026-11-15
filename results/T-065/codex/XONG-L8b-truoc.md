# T-065 L8 — G-c chưa đạt, chặn ở nguồn hash cấu hình

2026-11-14T16:52:24.329Z

- Đã kiểm chỉ mục bản 2 và 83 đầu ra: SHA byte khớp. Manifest trước L8 6.311 mục và LOG khớp.
- CHẶN: chỉ mục/hồ sơ V082 ghi hash byte file cấu hình; 28 đầu ra ghi hash JSON chuẩn hóa theo code M1-FT. Không tự chọn một giá trị để hiển thị. Bằng chứng: [báo cáo L8](kiem/005-gc-cuoi/BAO-CAO.md), [đối chiếu](kiem/005-gc-cuoi/chan-hash-cau-hinh.json).
- Chưa xuất dữ liệu hoặc deploy dashboard L8; chưa kiểm API/Chrome cho bản cuối. Nguồn cả sáu ca dev3 có trên exp-obs, chưa dựng liên kết. Giữ bản G-c thử cũ; 3.019 file máy cũ giữ hash, không restart Grafana.
- Bước tiếp đề xuất: Claude thống nhất trường hash trong nguồn T-064 và bàn giao lại chỉ mục/hash, Codex tiếp L8. Không chạy lại M1 vì khác biệt đang thấy là cách băm serialization. Phương án hiển thị hai loại hash cần Minh xác nhận và hợp đồng nói rõ.
- T-065 vẫn đạt một phần; L6/L7 chờ kiểm lại. Prompt gộp: [prompt-ban-giao.md](prompt-ban-giao.md). Không tự nghiệm thu hoặc đóng câu hỏi RQ5.

Giữ XONG trước lượt tại [codex/XONG-L8-truoc.md](codex/XONG-L8-truoc.md); manifest trước tại [codex/manifest-L8-truoc.json](codex/manifest-L8-truoc.json).
