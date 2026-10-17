# Bao phủ snapshot và lineage — T-039

Báo cáo nguồn phục vụ người làm tích hợp. **Đã phân hoạch hết cây nguồn được định danh; chưa xác nhận đầy đủ ngữ nghĩa runtime, deployment hoặc instrumentation.** Đây chưa là nghiệm thu task hoặc bằng chứng lợi ích đồ thị. Số lấy từ `results/T-039/bao-phu-nguon.json`, acquisition và `backend-source-audit.json` đã kiểm hash, không từ trí nhớ.

## 1. Cây và phạm vi tải

Metadata tree ứng dụng không truncated. `/entry_count` và `/rows` có 274 mục duy nhất: 219 blob và 55 tree nodes. `/counts` cộng 274; danh sách path giữa bảng và tree metadata khớp khi kiểm. Acquisition có 215 tệp ứng dụng, 8 nguồn Nezha mới và 6 metadata; cả 229 SHA256 khớp. Bốn blob log thô bị loại theo quyền tải; tổng 15.379.723 byte lấy từ metadata tree, không tải hoặc đọc nội dung. Tổng 219 blob = 215 đã tải + 4 loại có lý do. Đó là bảng phân hoạch snapshot, không phải toàn nguồn phụ thuộc của image/triển khai.

| Trạng thái tại `/counts` | Số mục |
| --- | ---: |
| `read_source` | 28 |
| `tree` | 55 |
| `read_visual` | 3 |
| `read_exclusion_rule` | 14 |
| `source_screened_with_specialist_scope` | 94 |
| `read_metadata_binary` | 2 |
| `read_build_entrypoint` | 2 |
| `test_source_scan_only` | 7 |
| `read_generated_interface` | 8 |
| `excluded_unread` | 4 |
| `read_alternate_source` | 4 |
| `read_dependency_structure` | 3 |
| `read_template` | 10 |
| `excluded_body_after_type_check` | 15 |
| `read_asset_structure` | 25 |

Các nhóm không là số entity/operation hoặc tỷ lệ nguyên nhân. `/completeness` hiện giữ `semantic_coverage_fully_verified=false` và `all_runtime_or_external_sources_complete=false`. Metadata hai snapshot không cho gitlink/symlink hoặc .gitmodules/.gitattributes; điều này không chứng minh mọi dependency nằm nội bộ. Dependency build/image/template vẫn có nguồn ngoài.

## 2. Độ sâu thực tế

Backend phần được giao có 67 tệp đọc ngữ nghĩa, 8 scan cấu trúc, 5 chỉ hash (`parts/backend-coverage.json#/files`). Bốn generated Python được parse AST/descriptor/URI/registration và đối chiếu registration thật; chưa đọc mọi message field hoặc serializer semantics. Hai lock JSON được parse toàn cấu trúc/versions/resolved, chưa đọc code dependency; hai launcher scan entrypoint/JVM path. Hai JAR backend chỉ hash; root có ZIP manifest/mục lục, audit xem lại manifest và tên class instrumentation. Đây chưa là phân tích hết bytecode/agent filter/final span names.

Bảy Python Nezha được đọc đường consumer/producer liên quan và scan AST/literal, không chạy. Producer Source/Target/Node chưa tìm trong đúng scope ấy; không kết luận toàn repo/deployment không có producer. Code consumer đọc CSV và tạo EventGraph/support, chưa là nguồn tĩnh độc lập. Exact source/locator, lineage và giải thích cạnh tranh ở `lineage.md` và `backend-source-audit.json#/lineage`.

Test source được phân loại nhưng audit không đọc/chạy nội dung test hoặc dataset. Các mức kiểm hình/asset, template/config/build được ghi trong bảng nguồn và báo cáo chuyên phần. Nhận dạng type, xem pixel, đọc SVG cấu trúc, scan generated hay đọc semantic không được đổi nghĩa thành toàn bộ runtime inventory đã xác minh. Nhánh Go/frontend và graph runner do root/chuyên phần phụ trách; audit này không thay việc kiểm của họ.

## 3. Điều source đã phân xử

- Code URL/DSN và MYSQL_ADDR của hai app chứng minh logical addatabase/Productdb nhắm cùng configured mysql endpoint. Source binding có điều kiện, chưa actual initialization/host runtime. Giữ DB logic và instance riêng.
- Mysqld-exporter config có sidecar/target localhost mysql; Redis exporter mới image/port trong source đã đọc. Script exporter và script mặc định chọn manifests khác nhau. Collector endpoint app chưa cho producer CSV dataset.
- Ad/cart dùng biến endpoint khác JS/Python. Generated Python có AdsService/CreateOrder khác proto. Registration và actual call phân biệt binding đang dùng với phần chưa dùng; không tự alias prefix/owner để tăng khớp.
- Email selected dummy không gửi mail thật; Recommendation actual call ListProducts đã giữ. Client/example không là server process ownership. Node dataset và Health Watch active còn cần nguồn đúng lớp.

Audit có bốn điểm chỉnh thực chất A1–A4: endpoint ad/cart, capability mysql exporter, provenance DB binding và gstatic preconnect không chứng minh HTTP resource call. Root nhận xử lý khi tích hợp; audit không sửa parts hoặc xác nhận bản sửa chưa đọc. Header gstatic là resource hint; external CSS response chưa có nguồn nên không suy synchronous HTTP edge từ URL ấy.

## 4. Bổ sung, owner, chi phí và quyết định

| Phần thiếu | Input cần thu/đọc | Owner | Chi phí/giới hạn | Quyết định phụ thuộc |
| --- | --- | --- | --- | --- |
| Image–source–dataset | Image digests, build commit, effective manifests, collection version đúng miền dev | Tác giả dataset/deployment qua Minh | CHƯA ĐO: chưa artifact list/bytes; không điền payload giả, chưa tải | P6 source graph conditional, chưa runtime ground truth |
| Producer daily Source/Target/Node | Code/config input→transform→CSV, revision, aggregation/time domain | Tác giả Nezha/collector; Minh duyệt phạm vi | 7 local Python và tree metadata đã khảo sát, 0 byte mạng; ngoài scope chưa định danh/đo byte | Chưa coi nguồn phụ độc lập; P9 identity/host semantics |
| Auto instrumentation/Health binding | Exact versions, selected binding/span-name/filter paths, binary-to-build identity | Maintainer nguồn; root/Minh | Dự toán CHƯA KIỂM 30–90 phút công cho selected paths; có thể sai nếu build mơ hồ; payload/máy chưa biết, không tải/chạy | Runtime aliases/prefixes/Watch active giữ unverified |
| Init datastore và metric schema | Actual init/image, scrape/exporter config, Redis target/default source, labels/schema | Tác giả triển khai/collector qua Minh | Local source đủ configured binding/mysql capability; supplement payload/giờ CHƯA ĐO | P9 logical DB→instance→host/shared signals; collector không phục hồi lịch sử chưa ghi |
| Tích hợp và kiểm graph | Áp A1–A4, union provenance, independent oracle, pinned-snapshot build/compare | Root trong T039 | Root đo total runs/retained disk/RAM riêng; audit không chạy build/compare | Task validation không thể suy từ tree partition |

Dự toán chưa kiểm không là cam kết chi phí. Nguồn ngoài cần đề xuất file/revision/dung lượng trước tải; thao tác tốn kém cần duyệt theo luật repo. Báo cáo không tự cấp quyền mở test, tải dependency, chọn P6 hoặc sửa hợp đồng chung.

## 5. Hệ quả P6/P9

P6 có thể dùng bản ghi nguồn làm **ứng viên đồ thị có điều kiện**, giữ giới hạn revision/branch/library; mapping thiếu bằng chứng phải báo unverified. Khớp với trace không chọn nguồn thành ground truth, không chứng minh RCA benefit hoặc phân xử mọi missing edge thành telemetry loss.

P9 cần service/pod/instance/host identity, logical DB/shared instance, schema log/metric/span và hiệu lực thời gian. NodeName của app manifest chưa xác nhận cột Node dataset; metric tính từ trace không tự là đối chứng độc lập. Cần producer/lineage để quyết; không cần mở raw values/test từ quyền khảo sát nguồn hiện hành.

Đầu ra hỗ trợ là ba file mới ở `runs/doc-nguon-002/`. Không sửa parts/shared/T037/T038/LOG/STATE, không tải nguồn, không mở nhãn/dataset/giá trị chuỗi, không chạy app/build/compare. Minh duyệt root dùng snapshot T036 cũ là quyền triển khai có sẵn; quyền đó không thay bằng chứng source semantics hoặc dataset lineage.
