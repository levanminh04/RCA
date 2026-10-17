# Kiểm đúng đắn và mức kết luận T-036

Bản hiện hành sau sửa R1 theo lời Minh duyệt ngày 15/10/2026. Codex thực hiện sửa và tự kiểm; phiên Codex sạch tiếp theo là phản biện chính thức toàn bộ T-036 theo chỉ định hiện tại của Minh. Phân công lịch sử trong SPEC giữ nguyên. Chưa nghiệm thu hoặc đóng task. Bản trước sửa được giữ tại runs/sua-r1-001/before/results/T-036/. Trung gian hiện hành của các bảng dưới đây ở runs/kiem-r1-after-002/; các lượt cũ được dẫn riêng để giữ lịch sử.

## 1. Nguồn và thứ tự bằng chứng

`runs/chuan-bi-001/input-verification.json#/checks`: 5673 artifact được chọn kiểm hash, tất cả khớp; gồm toàn bộ manifest T-035 và nguồn công khai được dùng ban đầu. `preflight.json` ghi môi trường, base commit, quyền ghi, manifest hash và hash tài liệu bảo vệ. B11-C/B12/B13/B14/B16 ghim revision/hash nội dung trong `nguon.json#/sources`, đều không dirty lúc đọc. Không lấy HEAD làm hash file.

Registry hiện có 15 nguồn. Bổ sung capture metadata đã kiểm hash ở `runs/chuan-bi-001/revision-verification.json`: tách RCAEval code commit, snapshot dataset và tree object Nezha; README Nezha khớp blob trong tree đã lưu. Những revision đó chưa chứng minh revision ứng dụng/deployment sinh dataset. Repo TT/Augmented-OB chỉ là nguồn ứng viên cho task sau, chưa tải.

`fixtures/oracle-before-code.json#/implementation_exists` là false; hash input/expected/definition khớp. Oracle cơ sở literal có trước implementation, không dùng builder để sinh đáp án. Các phép kiểm mở rộng trong checker (hai nguồn, nội bộ sau alias, nút cô lập, default exchange, tích hợp trace builder) được thêm khi tự đọc implementation; không gọi chúng là toàn bộ oracle trước mã. Tính đúng không chỉ dựa vào việc chạy không lỗi.

## 2. Đầu vào → xử lý → trung gian → đầu ra

| Phần kiểm | Bằng chứng và kết quả |
|---|---|
| Inventory/owner/resource | `fixtures/input.json` → `build` → `runs/kiem-r1-after-002/entity.json#/resource_bindings`; DB1/DB2 riêng, một PG chung, owner riêng và metric PG chung. Inventory không là observed_nodes hay tập ứng viên RCA. |
| Quan hệ và phép chiếu | Oracle `expected.json#/entity_edges` và `#/projected_entity_record_ids` → `entity.json`, `operation.json`, `projection.json`. Entity-only được báo exclusion; không tạo operation giả. Nội bộ/span-parent không thành cạnh entity. Callback/scheduler không có caller giả. |
| Messaging | Hai queue cùng consumer, fan-out, republish: queue_metric_address giữ riêng; không event_count tĩnh, không suy logical edge từ broker. `compare-two-queues.json#/views/typed` ghi đủ tập và mẫu số. |
| Tích hợp T-035 | `trace-synthetic-messaging.json` do builder T-035 dựng từ span tổng hợp → `compare-trace-builder-messaging.json`. Các chặng broker khớp; cạnh inferred logical của trace giữ riêng trong trace_only khi nguồn tĩnh không ghi quan hệ ấy. Không coi ví dụ là runtime FT. |
| Alias/kiểu/miền | `compare-unknown.json#/views`: đầu mút khớp nhưng typed loại unknown. Checker kiểm alias thiếu/mơ hồ/chưa xác minh, operation khác owner, cạnh nội bộ sau alias, địa chỉ thiếu cả hai phía, relation domain và interval lỗi. Không đổi nghĩa quan sát theo thiết kế. |
| Tập và mẫu số | `result.json#/checks` đối chiếu danh sách literal cho giao/phần riêng/S/T, unknown/khác kiểu/rỗng. Mẫu số 0 là null, không gọi precision/recall. Members giữ bản ghi tĩnh và cạnh trace riêng. |
| Nhãn và lỗi đầu vào | API thuần; trường lạ/nhãn bị từ chối, provenance thiếu hoặc ID/kiểu mâu thuẫn bị báo. Không nhận tên ca, đường dẫn ca hay mốc tiêm để chọn cạnh. Locator nguồn chỉ truy vết. |
| Graph dev có sẵn | `compatibility.json#/graphs`: 312 graph full/N/A ở hai mức, hai hệ, theo manifest hiện hành. Kiểm hash trước nạp, không sửa đầu vào. Không có mapping nguồn kiến trúc trong phép này nên loại trừ unmapped; chưa là đối chiếu kiến trúc thật. |
| Chiếu graph dev | `trace-projections.json`: 156 cặp thao tác/entity khớp, giữ ngoại lệ span-parent. Dùng graph lưu sẵn; không đọc trace thô/test hoặc chạy lại baseline. |

## 3. Các lượt và chi phí thực đo trước sửa R1

- `runs/kiem-001/failure.json`: dừng vì selector lấy thêm graph lịch sử trong manifest, đường dẫn không thuộc thư mục hiện hành. Các kiểm trước exception được giữ. Sửa selector trong checker, không sửa đầu vào hay oracle để đạt.
- `runs/kiem-002/result.json`: kiểm ban đầu đạt. Sau tự đọc lại code, bổ sung loại nội bộ sau alias và báo nút cô lập; không sửa SPEC.
- `runs/kiem-003/result.json`: kiểm bổ sung đạt. Sau đó thêm phép tích hợp T-035 messaging tổng hợp.
- `runs/kiem-004/result.json` và `runs/kiem-005/result.json`: mỗi lượt 151 kiểm đạt, 0 lỗi. Lượt kiem-005 là 8.754 giây, peak working set khoảng 109.9 MiB; số gốc ở `#/seconds`, `#/peak_working_set_bytes`, Python allocation peak ở `#/python_tracemalloc_peak_bytes`. RAM gồm Python/thư viện và cả checker, không chỉ API. Không chạy việc nặng khác đồng thời.
- Đảo bản ghi ở ba seed trong checker; hai process khác PYTHONHASHSEED giữ mọi graph/kết quả so sánh trung gian giống từng byte, kiểm ở `runs/ket-phien-001/determinism.json#/checks`. Mã đã chạy được lưu ở `runs/kiem-004/code/`, `runs/kiem-005/code/` cùng hash. Các lượt cũ chưa lưu snapshot mã riêng, không dùng chúng thay bằng chứng của hai lượt cuối.


## 3a. Phản biện R1, sửa và kiểm hồi quy

R1 trong chat chỉ ra khóa consume dùng thêm exchange/routing dù chặng nhận chỉ cần broker/scope/queue. Trước sửa, thêm thông tin nguồn phát ở một phía làm mất giao; khóa lưu graph và khóa đối chiếu chưa tách đúng mục đích. Minh duyệt đúng đề xuất sửa; nguyên văn quyền ở runs/sua-r1-001/authorization.txt và LOG Phiên 3. Không suy quyền sửa SPEC, WHY/DECISIONS hoặc nguồn T-035.

fixtures/r1.json và runs/sua-r1-001/oracle-before-fix-002.json giữ oracle trước sửa comparator. kiem-r1-before-001 giữ exception harness mapping_target; harness đã sửa theo mức. kiem-r1-before-002/result.json#/checks giữ 199 kiểm đạt và 22 không đạt; các kiểm cũ đều đạt, phần sai nằm ở R1. Đây là lượt tái lập có chủ ý, không bị bỏ.

Comparator nay chỉ dùng trường địa chỉ theo vai trò trong khóa: publish bốn trường, consume ba trường, logical-message năm trường. Graph và members giữ địa chỉ nguyên bản. Khớp consume không xác minh đường routing/binding hoặc một bản tin runtime; nhiều bản ghi cùng chặng nhận được giữ chung một khóa với đủ members. Không đổi builder, mapping, miền hoặc graph T-035.

runs/kiem-r1-after-001/result.json và runs/kiem-r1-after-002/result.json: mỗi lượt 221 kiểm đạt, 0 lỗi; gồm 70 kiểm R1. R1 kiểm hai phía khác độ chi tiết ở hai mức/hai view; bảo toàn input/member; gộp chặng nhận với nhiều địa chỉ nguồn phát; queue/scope khác hoặc queue thiếu; exchange publish và routing logical vẫn phân biệt. Danh sách gốc tại #/checks; trung gian tại r1-regression.json#/cases. Lượt sau đọc tương thích 312 graph, chiếu 156 cặp; thời gian 16.210 giây, peak working set 110.4 MiB. Đây là chi phí checker/fixture, không là thực nghiệm RCA.

runs/sua-r1-001/determinism-and-preservation.json ghi 10 đầu ra giống từng byte giữa hai process khác hash seed, và 7 đầu ra không chịu tác động giống kiem-005. Các graph nguồn, phép chiếu, so unknown, schema compatibility giữ nguyên. Snapshot code từng lượt được giữ; oracle ban đầu không sửa. Theo tự kiểm, R1 đã được sửa trong các trường hợp này; chưa thay phản biện chính thức toàn task.

## 4. Kết luận theo câu hỏi nguồn

**FACT:** công cụ giữ được các phản ví dụ đã kiểm, truy ngược bản ghi/provenance và phân tách mẫu số đúng hợp đồng. Thiết kế/code, quan sát runtime và lợi ích RCA không bị nâng chung một nhãn. Bộ dựng tĩnh không sinh event_count hoặc tự thêm quan hệ do correlation. Comparator không sửa graph trace.

**Suy luận có giới hạn:** hợp đồng có thể dùng làm đầu vào khảo sát T-037–039 trong các nhu cầu đã kiểm. Chưa chứng minh inventory/quan hệ toàn hệ đầy đủ; chưa có đối chiếu kiến trúc thật TT/OB. Khớp typed của non-messaging không xác nhận transport HTTP/RPC vì T-035 chưa ghi transport; members giữ channel nguồn tĩnh.

**OPEN:** runtime/build/deployment/instrumentation FlashTicket; revision ứng dụng TT/OB sinh dataset; nghĩa host của Node; độc lập metadata ngày; độ đầy đủ telemetry; lợi ích cấu trúc và lựa chọn P6. DB→instance được giữ trong lớp binding tĩnh; T-035 chưa có trường tương đương. Thiếu telemetry/mapping resource không được điền từ tên DB. Phản ví dụ, phương án bổ sung/owner/ảnh hưởng cụ thể tại `ban-giao.md` §2–3; muốn sửa hợp đồng trace hoặc thu thêm phải trình Minh riêng.

T-036 đáp ứng phần hợp đồng/công cụ trong phạm vi kiểm, chưa trả lời xong RQ3/RQ5 hoặc toàn P5b. T-037–040 cần SPEC riêng. P6/P7/P9/P10 nhận nghĩa vụ còn thiếu; dừng phản biện hay nghiệm thu công cụ không tự cho mở test hoặc khẳng định RCA có lợi.

## 5. Tự soát cuối và bàn giao

Bản trước và diff lượt sửa tại runs/sua-r1-001/; kiểm cuối tại final-verification.json trong thư mục đó. LOG chỉ nối thêm, STATE chỉ cập nhật dòng T-036; SPEC và nguồn bảo vệ giữ nguyên. Prompt hiện hành là prompt-codex-clean.txt, chép nguyên văn mẫu ngoài thông tin trung tính, dành cho phiên Codex sạch phản biện chính thức toàn bộ task từ nguồn trước khi đọc kết luận lịch sử. Prompt Claude và các lượt cũ được giữ. Không thêm quyết định khoa học, không tự sửa WHY/DECISIONS, không commit/push.
