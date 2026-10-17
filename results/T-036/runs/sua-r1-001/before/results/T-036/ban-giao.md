# Bàn giao T-036 — hợp đồng nguồn tĩnh và đối chiếu

Codex là người làm; Claude là người phản biện chính thức. Đầu ra chờ phản biện và Minh nghiệm thu. SPEC giữ nguyên. Không tự đóng P5/RQ3/RQ5/G3 hoặc chọn P6.

## 1. Đầu vào dùng tiếp

- `hop-dong.md`, `nguon.json`: mô hình bản ghi, inventory/operation/resource binding/signal, quy tắc alias/miền/kiểu/địa chỉ/mẫu số. Registry khởi đầu có revision/hash; không thay khảo sát đầy đủ từng hệ.
- `src/do_thi_tinh/{__init__.py,build.py,compare.py,README.md}`: API thuần. Bộ dựng chỉ chuyển bản ghi đã đọc nguồn, không tự phân tích code. Phép chiếu operation chỉ giữ phần có bằng chứng, báo entity-only; không tạo thao tác giả.
- `fixtures/input.json`, `expected.json`, `oracle-before-code.json`: ví dụ tổng hợp và đáp án literal trước mã. `check.py` chứa cả biến thể bổ sung sau khi tự đọc lại implementation; không gọi mọi kiểm bổ sung là oracle trước code.
- `kiem-dung-dan.md`, `runs/`: bằng chứng kiểm và mọi lượt, gồm lượt lỗi. Kiểm hash theo `manifest.json` trước sử dụng. Mã/hash nguồn T-035 giữ nguyên; T-035 chưa được nghiệm thu từ việc dùng trong T-036.

## 2. Phần đã kiểm và phản ví dụ còn phải giữ

**FACT:** fixture giữ được hai logical DB khác owner cùng một instance PG; mapping ở `runs/kiem-005/entity.json#/resource_bindings`, metric chung ở `#/signals`. Graph cạnh dữ liệu vẫn hướng tới DB logic. T-035 chưa có trường DB→instance tương đương; comparator không biến lớp mapping thành cạnh quan sát hoặc kết quả khớp runtime.

Phản ví dụ: DB1 thuộc A, DB2 thuộc B, cả hai hosted_on PG. Gộp DB1/DB2 thành PG làm mất ownership; dùng hai PG riêng làm mất tài nguyên chung. Giữ hai DB + một PG + hai binding là biểu diễn nguồn tĩnh v1. Các phương án chuyển tiếp cho trace: adapter xác minh endpoint logic và instance/resource ID hoặc bảng mapping có revision/build/time scope từ deployment. Muốn thêm loại cạnh/namespace/adapter T-035 phải trình Minh riêng; chưa có quyền sửa trong task này. P6 có thể đề xuất dùng mapping để nhận diện tập cùng tài nguyên, nhưng phép lan điểm/gộp metric chưa chọn và chưa kiểm lợi ích. P9 phải ghi ID nguồn, không suy lại instance từ tên DB.

**FACT:** graph T-035 v2.1 đã lưu đọc được và không bị sửa; các cặp phép chiếu khớp. Đây là tương thích schema/phép chiếu, không là đối chiếu kiến trúc TT/OB. Trong lượt tương thích không có alias được xác minh nên cạnh được báo unmapped, không tạo matching giả.

**FACT:** mẫu số và tập giao/phần riêng đúng oracle tổng hợp; unknown chỉ có thể khớp đầu mút, không thành sync. Nhiều source/republish không thành nhiều sự kiện; mỗi queue vẫn có địa chỉ riêng. Không suy message/callback từ cùng broker/correlation. Chưa phân xử độ đầy đủ/routing thực hay chất lượng telemetry.

## 3. Nơi nhận, bằng chứng thiếu và ảnh hưởng

| Nơi nhận / owner | Việc cần làm, đầu vào và phép phân xử | Quyết định phụ thuộc |
|---|---|---|
| T-037 / người làm theo SPEC riêng | Ghim B11–B16 bản được dùng; inventory đầy đủ và từng quan hệ/thao tác/điểm quan sát có nguồn. Bao phủ HTTP/RPC, DB/cache/ownership/resource, outbox/inbox, fan-out/retry/dedup, callback/query, scheduler, Saga/bù trừ/terminal fence, delivery/check-in, role-grant/projection và hỗ trợ/vận hành. Ghi operation runtime_name OPEN khi chưa instrumentation. | Độ đầy đủ thiết kế FT; không dùng vài fixture thay bảng coverage toàn hệ. |
| T-038 / người làm theo SPEC riêng | Truy Train Ticket từ RCAEval snapshot và repo ứng dụng chính thức; nối manifest/image/instrumentation với dataset đang dùng. So hai chiều từng graph/cửa sổ dev bằng mapping có nguồn; đọc cả khác biệt và trường hợp khớp tương ứng. Tải nguồn cần trình danh sách/revision/byte riêng. | Chưa có nối revision thì chỉ đối chiếu tham khảo có điều kiện; chưa quy chênh lệch cho thiếu instrumentation. |
| T-039 / người làm theo SPEC riêng | Truy Nezha/Augmented-OnlineBoutique; phân biệt tree/code RCA/dataset/deployment. Không dùng metadata mức ngày chọn P6. Miền toàn tập chỉ dev-adapter, không cả ngày. | Độc lập nguồn tĩnh, revision sinh dữ liệu, nghĩa Node/host còn phải có bằng chứng. |
| T-040 / người làm theo SPEC riêng | Kiểm chung revision hợp đồng, ID/alias, phép chiếu, miền/mẫu số, provenance và các nhóm thiếu. Tổng hợp P5b sau ba hệ. | Nghiệm thu P5b và đầu vào thiết kế P6/P9, chưa tự đóng câu nghiên cứu. |
| P6 / Minh và người làm thiết kế | Chọn tín hiệu/mức/thuật toán bằng SPEC; nêu phép tính dùng cạnh/resource mapping. Static chỉ khả năng phụ thuộc; cây span và thời gian từng lần vẫn cần khi phân rã chờ/nội bộ. Metric shared là một chuỗi, không nhân theo operation. | Chọn thiết kế và đánh giá RCA; T-036 không chứng minh cơ chế hoặc khắc phục P4. |
| P9a / nhóm hệ thống và Minh | Xác minh tên service/instance/host, DB logic/instance, kind/endpoint, broker/scope/exchange/routing/queue, message identity namespace, semantics link. Kiểm retry/fan-out/batch/collision/callback/scheduler/đứt context bằng instrumentation/config/broker, không giao collector phục hồi dữ liệu chưa ghi. | Địa chỉ và độ đầy đủ quan sát runtime; yêu cầu gửi sang hệ thống cần duyệt riêng. |
| P9b / nhóm chuẩn hóa | Export trace/log/metric cùng build/deployment/source versions, clock offset, sampling/drop/retention, namespace và manifest. Adapter kiểm nghĩa trước điền. Nối log theo trace/span, thiếu thì entity/time; metric đúng scope. | Đối chiếu FT thật bằng SPEC sau, không tự thêm cạnh static vào trace. |
| P7/P10 / thực nghiệm | Thiết kế khóa, đối chứng tương ứng, workload/nhánh và nhãn giao thức riêng; Minh duyệt mở test. | Khẳng định lợi ích quan hệ và khả năng áp dụng FT. |

Các giải thích chênh lệch chưa được task này phân xử: revision, alias, miền/cửa sổ, nhánh chưa chạy, nguồn tĩnh thiếu, telemetry thiếu, lỗi chuyển đổi. Không cộng cờ thành tỷ lệ nguyên nhân. Chưa làm khảo sát toàn hệ khác với không thể phân xử bằng dữ liệu hiện có.

## 4. Đề xuất bước tiếp

Minh chuyển prompt Claude ở cuối LOG T-036 để phản biện kết quả. Phản biện không tự là lệnh sửa. Sau Minh quyết nghiệm thu hoặc yêu cầu sửa, mới soạn/duyệt SPEC các nhánh tiếp theo. Không tải repo, bật EC2, mở test, commit/push từ bàn giao này.

Nội dung có thể đưa vào báo cáo đồ án: phân biệt nguồn thiết kế và quan sát, logical DB/instance, địa chỉ message và metric queue, alias có nguồn và mẫu số khớp cấu trúc có điều kiện. Không viết các kiểm tổng hợp là bằng chứng runtime hoặc hiệu quả RCA.
