# Bao phủ nguồn T-039

Đã kiểm cây snapshot ứng dụng, không lấy tập service có trace làm inventory. Toàn cây có 274 entry, gồm 219 blob và 55 tree; phân hoạch từng path nằm ở `bao-phu-nguon.json#/rows`, số theo trạng thái ở `#/counts`. Snapshot/pin/hash nằm trong registry và manifest.

215 blob ứng dụng đã tải; bốn `log.csv` thô bị loại đúng danh sách Minh duyệt. Bốn file ấy là dữ liệu vận hành, không dùng làm nguồn tĩnh; Dockerfile có COPY chúng nên chưa nhận tái lập build image. Cùng nguồn Nezha bổ sung và metadata, acquisition giữ 229 file, payload 37.524.834 byte (`runs/thu-nguon-001/acquisition.json`). Không mở log, test/heldout hoặc giá trị Node/Weight.

Đã xét source/config/deployment, build/template, proto/mã sinh, stash/test source, dependency/JAR manifest, tài sản trình duyệt và hình kiến trúc. `read`, `scan`, `hash` và `excluded` có nghĩa khác nhau. Chiều sâu của từng nhóm, nguồn ngoài và hệ quả ở `runs/doc-nguon-002/bao-phu-lineage.md`, `backend-source-audit.json`, `parts/*-coverage.json`. Không coi scan đủ thư viện là đã xác minh runtime. Không thấy LFS pointer/gitlink trong snapshot đã định danh.

Kết quả tham chiếu có 23 entity, 68 operation, 82 relation, 2 binding logic–instance và 53 khai báo địa chỉ tín hiệu (`doi-chieu/tong-hop.json#/record_counts`). Đây là khai báo nguồn, không phải số luồng telemetry độc lập. Binding trùng Productdb được hợp provenance; metric exporter ở instance không được nhân sang hai DB logic. `fonts.gstatic.com` giữ như resource hint trong inventory; preconnect không được biến thành cạnh HTTP. Exporter variant và browser scope giữ riêng trong context.

Độ đầy đủ inventory deployment vẫn **OPEN**: chưa có source→build→image digest→deployment→dataset, thư viện runtime và collector/export CSV. Nguồn khả dụng đã cho phép dựng/so graph tham chiếu; chưa đủ nhận toàn deployment hoặc quy thiếu cạnh cho telemetry. Phần mục tiêu nguồn đạt một phần, không tự thu hẹp nghĩa inventory để gọi xong. Đầu vào cần bổ sung, owner, chi phí và quyết định phụ thuộc ở `ban-giao.md` và `de-xuat-bo-sung-nguon.md`.

Các lỗi địa chỉ ad/cart, resource hint và thiếu configured exporter edge đã được sửa trong bản ghi hợp nhất, giữ fragments gốc và audit. Source notes cũng giữ README khác code (MySQL/local currency), generated proto khác registered service, email dummy, health/dependency, Node và nguồn phụ. Chưa dùng các khác biệt này làm nguyên nhân dataset.
