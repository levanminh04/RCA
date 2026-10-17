# Đề xuất tải nguồn T-039 — CHƯA ĐƯỢC DUYỆT

Danh sách từng đối tượng, blob, byte và URL ở [de-xuat-tai.json](de-xuat-tai.json). Đây là bảng đề xuất từ metadata đọc trong bộ nhớ, chưa là snapshot nguồn đã tải hoặc coverage đã kiểm nội dung.

1. **Augmented-OnlineBoutique của IntelligentDDS:** lấy đúng root commit và tree trong JSON. Metadata có một commit, không có parent; chưa chứng minh revision ứng dụng sinh Nezha-OB. Toàn cây có 274 entry, 219 blob. Đề nghị lấy 215 blob, **37.082.513 byte**, vào `results/T-039/sources/augmented-ob-94a01ba4/` bằng raw URL ghim commit. Không clone, lấy branch mới nhất hoặc chuyển upstream.

| Nhóm đề nghị | File | Byte | Cần để làm gì |
|---|---:|---:|---|
| Tài liệu, sơ đồ và ảnh trong docs | 6 | 6.308.257 | Kiến trúc, mô tả instrumentation; kiểm nội dung/loại trừ sau tải |
| Build/release/SQL | 6 | 12.495 | Nguồn gián tiếp, template và dependency dữ liệu |
| Deployment/runtime | 17 | 30.591 | Service, endpoint, biến môi trường, image tag và script khởi động |
| Interface gốc | 2 | 6.769 | Tên service/method và đầu vào sinh binding |
| Code ứng dụng và phụ thuộc | 124 | 643.530 | Client/handler, owner/nhánh, build/config, workload và unit-test code của ứng dụng |
| JAR công cụ/instrumentation | 2 | 25.814.047 | Định danh công cụ/instrumentation; kiểm ZIP directory/manifest trong bộ nhớ, không chạy |
| Binding đã sinh | 8 | 520.016 | Đối chiếu với proto, script sinh và handler; không tự bỏ generated |
| Template | 10 | 27.489 | Route/endpoint có thể xuất phát từ template |
| Static asset frontend | 40 | 3.719.319 | Kiểm nguồn gián tiếp và phân xử loại trừ trên toàn tree, không chỉ mã service có trace |

Nhóm là phân loại sơ bộ theo path, **chưa kiểm bằng nội dung**. Giữ mọi đường dẫn trong cây đề xuất, không gọi các tệp chưa đọc là không liên quan. Toàn cây không có gitlink; LFS/pointer, nội dung JAR và nguồn ngoài build/image vẫn OPEN tới sau khi được lấy và đọc. Không tự tải phụ thuộc hoặc image ngoài danh sách.

**Loại bốn `src/*/log.csv`**, tổng 15.379.723 byte, gồm checkoutservice, frontend, productcatalogservice, shippingservice. Lý do là giới hạn quyền không mở telemetry thô và tránh dùng log/case định hình mapping. Chưa đọc chúng để khẳng định chúng không có tên/nhánh bổ sung. Hệ quả: coverage là toàn nguồn tĩnh/code/config của snapshot được phân hoạch, không phải xác nhận đầy đủ nội dung runtime trong mọi blob. Nếu việc phân xử một quan hệ cần các log này thì giữ OPEN, trình phép kiểm đúng phạm vi; không mở bằng quyền tải code.

2. **Nezha cùng revision đã lưu T-008:** đề nghị thêm đúng tám file trong JSON, **20.124 byte**, vào `results/T-039/sources/nezha-d8140101/`: INSTALL, STATUS, log.py, log_parsing.py, pattern_miner.py, requirements, .gitignore và cấu hình drain3_hipster. Dùng commit có cùng thành viên cây với snapshot đã kiểm. Cần đọc phần import/pipeline/config/tài liệu còn thiếu để truy lineage. Không chạy code Nezha. Dùng lại README/paper/code/LICENSE đã kiểm theo manifest cuối T-003; không tải lại chúng.

Không lấy construct_data, rca_data, log kết quả, metric_threshold, labels, model template .bin hoặc config TT. Các nguồn ấy không cần cho khảo sát code OB được giao và có thể chứa dữ liệu/đầu ra phụ thuộc telemetry. Chưa chứng minh chúng không ảnh hưởng lineage; kết luận độc lập của nguồn phụ và Node/host vẫn OPEN khi không có mã sinh/schema tương ứng. Không xin phép đọc Weight/chuỗi số/log thô trong đề xuất này.

3. **Metadata để lưu chứng cứ sau duyệt:** sáu endpoint, URL và kích thước body đã quan sát trong JSON, tổng **422.197 byte**. Lưu tại `results/T-039/sources/metadata/`. Ref/commit list chỉ để ghi provenance; không được thay commit đề nghị nếu branch di chuyển. Nếu payload hoặc identity thay đổi thì giữ lượt lỗi và báo lại, không sửa hash cũ.

**Tổng:** 37.524.834 byte payload cho một lần thu thành công, khoảng 35,8 MiB; byte wire thật còn OPEN do HTTP/TLS/retry. Không có archive ứng dụng để giải nén. JAR không giải nén ra đĩa; kích thước entry nén chưa được đọc nên peak bộ nhớ khi mở còn chưa đo. Tổng lưu mọi lượt theo kịch bản trong JSON là khoảng 373 MB, gồm ba lượt thu, ba lượt so và phần log/trung gian; số lượt thực tế còn OPEN và mọi lượt được giữ.

Đề nghị duyệt đúng nguồn/commit/file/đường dẫn trên, sau khi Minh quyết phần khả thi/tách. Không đề nghị tải dataset mới, dependency package, Docker image, sửa data/README.md hoặc ghi ngoài T-039. Nếu cần các phần đó sẽ trình riêng. Đây chưa phải quyền chạy P6/RCA, mở test, đổi pin chung hoặc commit/push.
