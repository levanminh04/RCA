# Bao phủ nguồn và mô hình thiết kế FlashTicket

**Chờ Claude phản biện kết quả.** Inventory đủ thực thể tìm được trong phạm vi nguồn thiết kế ghim; graph giữ các quan hệ có đủ căn cứ về loại/địa chỉ. Những quan hệ nguồn chưa xác định đủ transport hoặc hành vi được giữ nguyên ở bảng OPEN, không bị xóa khỏi phạm vi nghiên cứu.

Nguồn: 5 tài liệu B11-C/B12/B13/B14/B16, 10 sơ đồ trực tiếp, 4 README baseline, 10 định nghĩa SQL/Mongo/realm và 5 nguồn quản trị/phạm vi. Tổng 34 nguồn, 4.585 dòng theo runs/assemble-002/coverage-resolution.json. Đây là phạm vi **thiết kế đích được liệt kê**, không là toàn bộ cây platform hay runtime. Revision/hash/dirty state và snapshot ở nguon.json; 10 baseline definitions đã đọc nội dung và đối chiếu, không còn chỉ metadata. Tests/runners/legacy/archive/remote tham khảo không làm nguồn sinh mô hình; lý do/ảnh hưởng ở registry.

652 đơn vị nguồn tại bao-phu-nguon.json#/units. B13/B14/B16 có ledger 562 dòng giữ nguyên văn; 239 đoạn trích được kiểm lại khớp snapshot tại runs/assemble-002/semantic-source-audit.json. B12 và năm ERD có đơn vị theo bảng/đoạn; 47 bảng SQL đối chiếu tên với dictionary đủ 12/15/13/7, bốn collection User giữ owner/source version. Số dòng/đơn vị chỉ là điều hướng; bằng chứng nghĩa nằm trong từng đoạn, bản ghi và chuỗi truy vết.

| Nhóm | Kết quả mô hình / nguồn | Điều kiện và phần mở |
|---|---|---|
| HTTP/RPC/gateway | Buyer/API hỗ trợ/seat-map/check-in, freeze/probe/financial summary theo B13. Không tìm thấy hợp đồng RPC riêng để tự thêm | B13 User §9 có path nhóm chưa method; không tự tách handler runtime. Prefix/method rút gọn cần P9 kiểm |
| DB/cache/shared instance | Sáu service/identity→DB logic; Booking→cache; năm DB trên một PG instance qua binding; Mongo User riêng theo B12 | DB/instance/host mục tiêu, chưa là địa chỉ triển khai thật. Cache technology/operation OPEN |
| Messaging/fan-out | 9 message type, 11 tuyến logical gồm cancellation ba consumer; publish→broker và broker→consume giữ riêng | Exchange flash-ticket.v1/routing có nguồn; queue/scope null, không bịa tên queue hoặc đếm bản tin từ tài liệu |
| Outbox/inbox/retry | DB đúng owner, relay, confirm rồi published_at; commit rồi ACK; hash/dedup/attempt giữ trong context/coverage | Bảng có mặt không chứng minh worker chạy đúng; retry không tạo operation/cạnh logic mới |
| Callback/query | Payment verify/create/query/refund và tra cứu hoàn; callback có quan hệ thiết kế provider→Payment | Fixture giữ trace callback mới; correlation không tạo parent hay message edge |
| Scheduler | Expiry/refund/relay/delivery/role-grant/projection có owner và nguồn | Root không cần caller. Frequency/lease/tên span runtime còn cần triển khai |
| Saga/bù trừ/fence | Chỉ một Saga Payment; kết quả phát vé/quyết định Booking/hoàn theo B13/B14 | Không đảo cạnh bù trừ, không Ticket→Booking giả. Timeout chưa là terminal FAILED; source state không bị graph thay thế |
| Delivery/check-in | SMTP được giữ đúng channel, kiểu gọi chưa phân kiểu; QR/read/claim/audit/replay giữ nguồn | Email timeout có thể gửi trùng; không thêm vé/refund. Không runtime claim; không raw QR/JWT |
| Role-grant/projection | User API + Admin API request/query, worker nguồn application/version; Mongo local | Không Keycloak→User message giả hoặc Saga thứ hai; quyền/client realm runtime OPEN |
| Hỗ trợ/vận hành | Gateway/identity/config-discovery/chatbot/kho quan sát/RCA/Gemini/host có inventory; data dependencies đọc kho giữ riêng | Arrow kiến trúc chưa đủ caller/transport được giữ ở quan-he-nguon-chua-dinh-kieu.json; không lấy local JWT verify thành HTTP request mỗi lần |

Mô hình đã kiểm: 32 thực thể, 65 tên thao tác thiết kế, 115 bản ghi quan hệ → 72 cạnh thực thể; 55 cạnh thao tác, 17 cạnh chiếu; 14 binding và 153 địa chỉ/schema tín hiệu, trong đó 23 dùng chung. Con trỏ: runs/graph-003/result.json#/stats. Không có observed nodes hoặc tập ứng viên P6 được suy từ inventory. Các nhãn B16 và endpoint có thể mô tả cùng thực thi; không cộng số tên thành số request hoặc độ phân giải runtime.

DB instance có thể không có dependency edge nhưng vẫn nằm trong inventory/binding/signal. P6 cần đề xuất phép dùng binding riêng nếu tính ảnh hưởng tài nguyên chung. Lớp operation không thay cây/thời gian span; phần entity-only là hợp lệ, không tạo operation giả để ép phép chiếu bằng graph đầy đủ.

Các OPEN còn lại được định danh tại bao-phu-nguon.json#/open_items: queue/scope, runtime operation mapping, deployment/resource, config/identity protocol, pipeline/export, quyền/UI/retention và đánh giá RCA. Mỗi mục có owner/input/hệ quả. Không còn chặn hỗ trợ SMTP trong phạm vi đã kiểm; chưa có quyền coi OPEN là quyết định đã chốt.
