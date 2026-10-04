# Tự phản biện SPEC trước triển khai

04/10/2026. Tự soát như người chưa làm; chưa đọc telemetry mới.

| Điểm kiểm | Lỗ hổng đã tránh hoặc sửa trong SPEC | Hệ quả |
|---|---|---|
| SL25 | Mỗi script có progress và thời gian; mỗi bước append LOG | Không mất trạng thái nếu tải dừng |
| SL26 và T003 R1 | Ghi phép không chạy vì cấm và kết luận yếu; no-trace không phải chờ quyền | Không bàn giao kiểm metadata thành quality/runtime đã kiểm |
| SL27 | Chi phí cộng toàn SS và OB, trần byte mạng gồm retry/source | Không ước lượng một ca thành toàn corpus |
| SL31 | Prompt cuối sẽ trích template bằng máy rồi kiểm equality, chỉ thay slot trung tính | Không neo Claude bằng finding |
| SL32 | Bước nguồn và lineage chạy độc lập census/tải; inspection chờ hash | Không bắt mọi nhánh chờ thứ tự đọc |
| T003 R2 | Biên từng modality, ID payload và tên đường dẫn đều có bước kiểm | Không bỏ lộ injection qua cấu trúc file |
| Ghi đè WHY16 | Không ghi source chung; STATE chỉ splice đoạn dòng sau đọc mới | Giữ nội dung tám phiên khác |
| Hash format | LFS dùng SHA256; file nhỏ dùng git blob SHA1, không SHA1 raw | Không nhầm revision khớp chỉ vì hash tự tính |
| Identity ca | Injection chỉ là chứng cứ yếu; cần nội dung với CSV/parquet và run manifest | Không đánh dấu test sạch từ tên khác |
| Thiếu trace | Kiểm trên toàn metadata trước; không tạo causal graph từ metric hoặc giả 0-degree root | Giữ giới hạn RQ1/RQ3 đúng |

SPEC ban đầu đã bao gồm các sửa này trước khi tự duyệt; không có bản SPEC đã duyệt nào bị thay nội dung khóa. Thêm edge case clock, band zero, tải truncated, alias và concurrency ngoài sáu tối thiểu. Không lựa chọn phương pháp/dataset mới cần WHY.
