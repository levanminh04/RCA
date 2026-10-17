# Gói SMTP V2 chờ Minh duyệt

T037 **đã hỗ trợ SMTP và dựng full model có điều kiện**; T039 **đã đối chiếu132graph** bằng snapshot R1. Hai task vẫn chờ phản biện, chưa nghiệm thu. T038 vẫn dùng pin R1 và chưa đưa quan hệ SMTP vào model.

[Gói hiện hành](runs/cap-nhat-goi-smtp-001/package/plan.md) đề xuất **đổi phép đối chiếu SMTP và hợp nhất phiên bản dùng chung**, dùng nguyên builder T037, patch chỉ comparator và cập nhật README/hợp đồng/pin theo filelist. Đây là thay đổi semantics (cả endpoints), không chỉ thêm hỗ trợ SMTP. Giữ lựa chọn so cấu trúc hiện tại là phương án hợp lệ nếu Minh chọn chấp nhận giới hạn đó.

Có29checks preview đạt, gồm rebuild nguyên full model T037/T039 và phản ví dụ semantics; chưa là full comparator replay. Sau duyệt phải hồi quy T036/R1/SMTP, full model/fixture T037, **1069TT và132OB** bằng runner/pin mới, tách ảnh hưởng comparator khỏi deltaTT. Kế hoạch dự trù37phút máy/600MB, chưa đo; thay dự toán V1.

Xem plan.json, docs-before-after.json, input-state.json, patch và package-manifest trong thư mục V2 để duyệt cụ thể. BảnV1 giữ tại runs/cap-nhat-goi-smtp-001/before/package-v1/. Chưa sửa shared/SPEC/WHY/DECISIONS hay chuyển pin; không suy nghiệm thu/G3/test/commit. Runtime lineage, authority/TLS/delivery và các OPEN nguồn vẫn giữ nguyên.
