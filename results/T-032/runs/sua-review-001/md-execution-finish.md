## Kết thúc từ file đã lưu, 12/10/2026

Lượt001 dùng extract.py, giữ failure.json (127,961giây); lượt002 dùng extract-v2.py, giữ failure.json (2,284giây); lượt003 dùng extract-v3.py, summary.json PASS (157,055giây). Hai lỗi là thiếu liên kết capture ở ca dev-3defe3d34b, không phải lỗi số tính toán. Lượt003 truy liên kết hồi cứu qua audit/check.json và kiểmhash; giữ nguồn/script/lượt cũ. Summary hoàn chỉnh và progress ở attempt-003/.

Sau khi usage limit ngắt trợ lý, Codex chính đã đọc thiết kế, scriptv3, failure, summary và từng manifest; tính lại từ bảng trace đã lưu bằng verify_md_saved.py (không gọi ranker). Kết quả kiem-md-doc-lap.json: mọi hash/đếmOR/tổngcờ/chuyểnnhóm/coverage được kiểm đều khớp. Các số cohort và ví dụ trong báo cáo lấy từ chính kết quả này.
