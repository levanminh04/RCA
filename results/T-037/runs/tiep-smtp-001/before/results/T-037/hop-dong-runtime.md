# Đầu vào đối chiếu runtime — bản chưa hoàn thiện

PARTIAL. Đây là bàn giao yêu cầu quan sát từ thiết kế; chưa là hợp đồng runtime đã xác minh hoặc đã thu dữ liệu. Graph/fixture đầy đủ dừng vì SMTP. Tên thao tác thiết kế không là span.name/operationName thực.

| Phần | Nơi phải ghi / owner | Trường và kiểm cần |
|---|---|---|
| HTTP/gateway/internal | instrumentation ứng dụng và gateway | build, service/instance/environment, peer, kind, method/route logic, trace/span/parent, requestId; alias có revision; internal không mở qua gateway |
| DB logic/instance/host | config/deployment + instrumentation/metric exporter | owner, database logic, instance/resource ID, hostId đã xác minh và thời gian hiệu lực. Giữ 5 DB logic trên một PG instance; không suy instance từ tên DB |
| Broker/message | ứng dụng outbox/inbox + broker/config | broker/scope/vhost/exchange/routing/queue/binding và message identity scope; logical message, publish/delivery/processing attempts khác nhau; link semantics đã kiểm. Correlation không nối bản tin |
| Queue/shared metric | exporter + P9b | một địa chỉ broker+scope+queue; CPU/RAM/pool đúng service/instance/host. Metric chung operation=null, không nhân theo số cạnh/operation |
| Callback/query | Payment/adapter provider | callback trace mới; attempt/charge liên kết sau verify; provider client span + response/query, không tuyên bố lỗi bên trong provider |
| Scheduler/relay | owner ứng dụng | mỗi item/lần xử lý trace riêng, job/message/lease/retry/outcome; không caller giả, không nối parent bằng correlation |
| Saga/terminal fence | Payment/Booking/Ticket | quyết định trước/sau, reason, accepted charge, command/result, commit/outbox/ACK và terminal failure; timeout không là FAILED |
| SMTP delivery | Ticket/SMTP adapter | transport SMTP, delivery ID/attempt/outcome/latency, trace mới và correlation từ job; timeout có thể đã gửi, không tạo vé/refund. Hợp đồng tĩnh hiện chưa giữ được channel này |
| Check-in | Ticket | mỗi receipt/replay_of và result, trạng thái trước/sau, owner/window; không raw QR/JWT |
| Role-grant/projection | User/Keycloak | operationId/subject/kết quả/query/retry/sourceVersion, nguồn login đúng identity. Quyền Admin API/realm phải kiểm, không log token |
| Kho quan sát/RCA | vận hành/P9b | UTC/observed time/clock offset, sampling/drop/exporter/retention và manifest workload/build; RCA chỉ đọc, không DB nghiệp vụ |

Sau giải quyết hợp đồng: viết oracle và fixture tổng hợp đúng nguồn trước converter; kiểm nhiều queue/shared instance, thiếu mapping/address, callback trace mới, scheduler không caller và correlation không tạo edge. Chưa có các fixture đối chiếu đầy đủ này trong T037. Collector không thể khôi phục trường chưa được nguồn ghi.
