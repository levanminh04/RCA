# Hợp đồng đối chiếu runtime FlashTicket — đầu vào cho P9

Đây là **yêu cầu địa chỉ và phép kiểm** rút từ nguồn thiết kế, chưa là telemetry hoặc nghiệm thu instrumentation. Tên thao tác trong ban-ghi.json là nhãn thiết kế; runtime_name=null. Bảng chi tiết từng65thao tác/signalID/owner/nơi ghi/keys ở dia-chi-tin-hieu.json#/operations. Không dùng tên thiết kế tự điền operationName/span.name.

| Nhóm / nguồn | Trường bắt buộc để chuẩn hóa | Nơi ghi / owner | Phép kiểm trước đối chiếu thật |
|---|---|---|---|
| Identity chung — B16 §4 | environment, serviceName/service.name mapping, serviceVersion/build, instanceId, hostId đã xác minh, timestamp UTC/observed time | ứng dụng+deployment/P9b | Cùng service ở3tínhiệu có alias rõ; host logic khác host runtime |
| HTTP/API — B13/B16 | kind, method/route, peer entity/type, trace/span/parent/request IDs; code/outcome/duration monotonic | gateway/resource server/client instrumentation | Probe freeze/issuance/financial summary và lỗi timeout; không lộ internal route hoặc credential |
| DB/cache — B12/B16 | db.entity/type, DB logic/schema, instance/resource ID, host/time scope | ứng dụng/deployment/exporter | Giữ5DBlogic chungPG, UserMongo riêng; đối chiếu client span→DBlogic→instance→host, không suy từ tên |
| Message — B13 §5/B16 §3 | broker/scope(vhost)/exchange/routing/queue, producer/consumer role; messageId/identity namespace, attempt, correlation/causation, verified creation link khi có | outbox/relay/inbox/broker config | Publish confirm rồi published_at, consumer commit rồi ACK; fan-out nhiều queue; duplicate/collision/batch/retry. Cùng correlation không đủ nối |
| Queue/shared metric — B16 §5/§7 | broker+scope+queue hoặc resource/instance/host ID; metric name/unit/labels hữu hạn/sampling interval | exporter+P9b | Hai queue cùng consumer vẫn2địa chỉ. MộtPGresource metric dùng chung, operation=null; không sao thành evidence độc lập mỗi operation |
| Callback/query — B13 §5.3/B16 §3 | attempt/charge được verify, request/trace mới, provider outcome/query/deadline | Payment/provider adapter | Callback trace mới không ghép parent từ correlation; timeout UNKNOWN/query cùng ID; không claim nội bộ VNPay |
| Scheduler/relay — B14/B16 | job/item/attempt/lease, trace mới, correlation từ bản ghi bền, duration/outcome | service owner | Restart/retry cùng job; batch mỗi item đúng correlation; không caller giả |
| Saga/bù trừ/fence — B13/B14 | saga/order/command/message/charge IDs, stateBefore/After/reason, input hash/fence decision, outbox/inbox | Payment/Booking/Ticket | Timeout≠FAILED; failed terminal chặn phát muộn; bù trừ giữ đúng chiều thiết kế, kiểm cả thành công/lặp |
| SMTP — B13 §6/B14 §6 | transport SMTP, delivery/job/attempt, new trace/outcome/duration; provider response nếu có | Ticket/SMTP adapter | Gửi ngoài DB TX; timeout có thể đã gửi; retry không tạo vé/refund; static channel smtp không xác minh span kind runtime |
| Delivery/check-in/QR — B13 §6 | receipt/replay_of, actor đúng quyền, owner/window/state/outcome, delivery input hash | Ticket | Một success/vé, mỗi receipt/replay có audit; email lỗi không VOID/refund; không raw QR/JWT |
| Role-grant/projection — B13 §9 | operationId/subject/request/result/query/retry, sourceApplicationId/sourceVersion | User/Keycloak | ACTIVE chỉ sau role confirm; retry/rebuild projection từ nguồn; realm fixture không chứng minh quyền Admin API |
| Pipeline — B16 §2/§6/§7 | receiver/exporter endpoint/protocol/config version, dropped/export failures, clock offsets, sampling/retention | vận hành/P9a/P9b | Một đường xuất mỗi tín hiệu, kiểm allow/deny RCA API backend; collector không khôi phục dữ liệu chưa ghi |

Address hiện tại là namespace/schema thiết kế, chưa phải địa chỉ truy vấn runtime. Queue/scope hoặc endpoint chưa biết phải null/OPEN trong adapter mapping; không dùng placeholder symbolic như queue thật. Log dùng trace/span khi hợp lệ, thiếu thì entity+time; operation chỉ gắn khi mapping rõ. Label không chứa orderId/traceId/messageId/email/URL cóID.

Ví dụ dưới **tổng hợp** để minh họa biên, không là schema OTel đã ban hành:

```json
{"serviceName":"payment-service","operation":"verifyNotification(rawRequest)","runtime_name":null,"traceId":"synthetic-callback-trace","parentSpanId":null,"correlationId":"synthetic-order","outcome":"UNKNOWN"}
```

Request trước đó có traceId khác, cùng correlationId. Không thêm edge cha–con hoặc message từ ví dụ này. Khi đối chiếu thật, trace/span IDs phải đúng định dạng nguồn và alias/runtime operationName phải được P9 xác minh; ví dụ không dùng làm log B16 hợp lệ để thu dataset.

Fixture đã chạy: fixtures-runtime-v2.json và runs/graph-003/fixture-*; SMTP fixture/typed protocol caveat tại runs/smtp-regression-001/. Chúng là phép kiểm hợp đồng tổng hợp, không chứng minh telemetry FT đủ.

Manifest thực nghiệm sau phải ghim build/image/config, workload/nhánh, khoảng thu, seed, sampling/drop/retention, clock offset và export hashes. Nhãn lỗi/mốc tiêm nằm riêng cho chấm; không đưa vào graph builder. P9b nhận graph trace riêng, không thêm cạnh tĩnh vào trace để tăng khớp. P6/P10 cần SPEC và quyền riêng cho lựa chọn/đánh giá/mở test.
