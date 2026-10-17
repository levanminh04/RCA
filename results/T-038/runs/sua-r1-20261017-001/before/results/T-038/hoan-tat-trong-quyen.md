# Mức hoàn tất T-038 sau lượt làm tiếp

Đã hoàn tất phần triển khai và tự kiểm đang được phép; không còn dừng ở nhãn OPEN chung. Chưa nhận toàn task đủ biểu diễn/nghiệm thu: **phần tiếp nhận SMTP ở T038, đổi comparator và common pin còn chờ Minh duyệt gói V2**. Bản ghi, graph và phép so hiện hành vẫn giữ pin T-036 v1 đã giao.

| Tiêu chí SPEC | Kết quả và bằng chứng |
|---|---|
| Snapshot/coverage/lineage | Đủ cây/hash; 2.783 read, 43 excluded, 1 body PDF open. Đã rà hết 27 mục cũ. PDF offline không chặn module inventory hiện hành. Không nhận semantic/runtime completeness. Metadata đã truy tiếp và kết luận có điều kiện. |
| Quan hệ/địa chỉ/biểu diễn | Nguồn và hai graph đã kiểm; 9 cờ initializer đã đóng bằng source. SMTP có counterexample, patch preview và 29 checks V2; chưa áp dụng shared nên chưa nhận đủ mọi relation. |
| Toàn graph/cửa sổ dev | Đủ 1.069, cùng pin/mapping/input; tập/members/exclusions/mẫu số/interval/lặp/đảo hợp lệ. Dùng lại output theo hash, không chạy lại khi không cần thiết. |
| Chênh lệch và cơ chế | Có mismatch/match và chuỗi code→record→mapping→key→set; đã phân loại đủ 151 tracking row. Không quy nguyên nhân runtime hoặc chọn P6 từ absence nguồn. |
| Bàn giao | Có đầu vào T-040/P6/P9, giới hạn nguồn riêng và gói SMTP/filelist/chi phí để Minh duyệt; prompt chuẩn để chuyển thủ công. |

Các giới hạn về runtime lineage, input dynamic và nội dung PDF không biến thành yêu cầu mở raw hoặc dừng phép so tham khảo đã được SPEC cho phép. Chúng chỉ giới hạn kết luận tương ứng. Gói SMTP là thay đổi ngoài quyền T-038; không thể tự áp dụng bằng cách đổi enum riêng hoặc bỏ quan hệ đó cho task có vẻ xong.

Xem chi tiết từng tiêu chí và con trỏ tại `hoan-tat-trong-quyen.json`. Bước cần Minh quyết hiện tại là `goi-sua-SMTP.md`; không cần giao lại phần T-038 đã được làm.


Cập nhật16/10/2026: T037 đã hỗ trợ SMTP/full model; T039 đã so132graph dùng snapshot gốc. GóiV2 tại runs/cap-nhat-goi-smtp-001/package/plan.md xin đổi semantics comparator và phiên bản chung; dùng nguyên builder T037. Preview29 đạt, chưa replay1069TT/132OB bằng comparator mới. Kế hoạch hồi quy đầy đủ cả ba nhánh và dự trù37phút/600MB thay góiV1; không đổi model/so/pin hiện hành hoặc nghiệm thu.
