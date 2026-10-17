# Bao phủ nguồn T-037 — phần đã làm, chưa hoàn tất

**Trạng thái: PARTIAL / chờ Minh quyết chặn SMTP.** Không phải inventory/graph toàn phạm vi đã kiểm.

Đã đọc năm nguồn thiết kế chính, 10 sơ đồ và bốn README baseline. Nguồn cùng hash, revision, dirty state và bản nội dung ghim ở nguon.json; snapshot ở runs/nguon-001/. Năm nguồn chính: 2.237 dòng / 192.902 byte. Sơ đồ: 743 dòng / 23.050 byte. Đọc nguồn không tự chứng minh mọi yêu cầu đã ánh xạ đúng.

Lưu 347 đơn vị nguồn và 32 thực thể, 60 thao tác có tên thiết kế, 79 bản ghi quan hệ, 14 binding, 58 địa chỉ tín hiệu dự thảo. Số lấy từ bao-phu-nguon.json#/counts và #/units. Không có event_count hoặc observed_nodes/tập ứng viên runtime được suy từ các số này.

| Nhóm bắt buộc | Bằng chứng đã lưu | Phần còn thiếu / ảnh hưởng |
|---|---|---|
| HTTP/RPC/gateway | B13 buyer API, freeze/probe/financial summary; records-flow | Không có nguồn RPC riêng để tự thêm; graph/chiếu chưa kiểm |
| DB logic/instance chung | B12 §2/§12/§13, năm ERD; records-data | 47 bảng/467 cột SQL, 4 collection được giữ theo datastore; không tạo 467 operation. Endpoint/process/host runtime OPEN |
| Cache | B11-C-02 Booking→cache; records-infra | Công nghệ/địa chỉ/tên thao tác chưa có nguồn; không tự điền Redis từ bối cảnh cũ |
| Messaging/queue/fan-out/retry | B13 §5; routes giữ exchange/routing/consumer có nguồn | Queue và broker scope vẫn null; chưa thể đối chiếu địa chỉ runtime hoặc coi fan-out đã chạy |
| Outbox/inbox | Mỗi SQL owner có bảng riêng; B13/B14 ghi transaction/confirm/ACK/dedup | Không suy bảng tồn tại là worker chạy đúng; relay/processing/attempt phải kiểm fixture sau |
| Callback/query | B13 §5.3/B16 §3; thiết kế callback mới và provider query | Không nối trace từ correlation; chưa có telemetry hoặc toàn fixture đối chiếu |
| Scheduler | B14 expiry/refund/delivery/relay; B13 role-grant/projection | Không tạo caller; tên runtime/frequency/lease còn phải kiểm triển khai |
| Saga/bù trừ/terminal fence | B13 commands và B14 §3–§5 | Không Ticket→Booking giả. Chưa graph/chiếu/fixture terminal fence đầy đủ |
| Delivery/check-in | B13 §6/B14 §6/B14-03 | **SMTP không biểu diễn được theo channel hiện hành; chặn graph đầy đủ** |
| Role-grant/projection | B12 §4.5/§6, B13 §9, B16 §5 | Admin API quyền/tên endpoint/token/realm runtime OPEN; không bịa Keycloak→User message |
| Hỗ trợ/vận hành | B11-C §5/§6, B16 stack/resource/retention/quyền | Inventory riêng; chưa chọn tập ứng viên P6. Địa chỉ metric thật và transport pipeline chưa xác minh |

Các status `covered_design` trong coverage-data.json chỉ nói đoạn dữ liệu được dẫn vào bản ghi nguồn, không là toàn graph hay cơ chế đã kiểm. Các status `represented_design_partial` ở coverage-flow cũng là phần trích nguồn chưa được converter/graph kiểm. Tổng không phải tỷ lệ hoàn thành task.

Nguồn dẫn xuất SQL/Mongo/realm chỉ thống kê metadata trong nguon.json#/derived_scope; chưa đọc nội dung test. Chưa gọi nguồn đóng đầy đủ. Phần legacy/archive và URL bên ngoài được loại có lý do/ảnh hưởng, không tự tải để bù.
