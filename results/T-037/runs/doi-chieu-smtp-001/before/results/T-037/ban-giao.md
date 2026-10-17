# Bàn giao T-037 — mô hình thiết kế và hợp đồng quan sát

**Chờ Claude phản biện kết quả; Minh quyết nghiệm thu.** Phần hỗ trợ SMTP đã được sửa/kiểm theo lời giao. Không đổi pin/SPEC/đầu ra T-038/T-039 hoặc snapshot/manifest T036; không đóng task/G3.

## Kết quả dùng để kiểm tiếp

- nguon.json:34nguồn local đã đọc/ghim, revision/hash/dirty/snapshot/phạm vi loại trừ. Giữ lịch sử nguồn trước đó trong runs/.
- ban-ghi.json và do-thi/:32thực thể,65tên thao tác,115bản ghi quan hệ; graph72cạnh thực thể/55cạnh thao tác/17cạnh chiếu;14binding,153địa chỉ/schema tín hiệu. Số tại runs/graph-003/result.json#/stats. Inventory không là observed nodes/tập ứng viên P6; tên thiết kế có thể là nhiều nhãn của cùng thao tác runtime.
- bao-phu-nguon.json:652đơnvị; raw source quote/ledger, classification, owner/input và references. Chuỗi từng unit→record→graph index/binding/signal trong runs/graph-003/requirement-record-graph-matrix.json. quan-he-nguon-chua-dinh-kieu.json giữ các arrow chưa đủ protocol/call semantics, không dùng chúng làm cạnh runtime.
- hop-dong-smtp.md: pin nền T036 + bổ sung đã duyệt; graph-003/code/ là snapshot actual. typed/endpoints comparison không xác minh transport. Nguồn SMTP không chứng minh span CLIENT/SERVER nên FT giữ gọi-chưa-phân-kiểu.
- dia-chi-tin-hieu.json và hop-dong-runtime.md: từng operation/schema keys/nơi ghi/owner/phép kiểm cho P9.
- kiem-dung-dan.md, manifest.json và runs/: oracle trước converter, kiểm từng bản ghi/chiếu/signal/binding, fixture boundaries, môi trường/thời gian/RAM/mọi lượt lỗi.

## Câu hỏi nguồn đã trả lời tới đâu

**FACT từ nguồn và phép kiểm:** có thể giữ owner/datastore, mộtPGinstance chung, địa chỉ message còn thiếu đúng trường, thao tác có tên thiết kế và SMTP trong graph tĩnh với bổ sung được duyệt. Quan hệ async có3chặng giữ riêng; operation thiếu được báo entity-only. Cạnh được dùng tính gộp/projection/đối chiếu cấu trúc, chưa dùng anomaly/ranking.

**Suy luận có điều kiện:** inventory đủ ở phạm vi selected design sources; source graph giữ các quan hệ đủ type/address. Không suy mọi arrow kiến trúc là endpoint trực tiếp. B11-C §1 giao endpoint/sequence cho B13/B14, vì vậy không tạo Ticket→Booking trực tiếp từ diagram. B14 Gateway là payment provider theo ngữ cảnh, khác API Gateway. Source-gap OPEN không là lỗi dataset/cơ chế RCA.

**Chưa phân xử:** process/operationName/queue/scope/host/endpoint thật, đủ telemetry/nhánh chạy, hiệu quả RCA. Lý do: task được giao nguồn thiết kế, không có quyền/đầu vào runtime. Cần P9 export/config/build và SPEC đối chiếu sau; không thể chứng minh bằng collector hoặc fixture tổng hợp. RQ3/RQ5/G3 vẫn mở; T040 tổng hợp và P6 chọn thiết kế chưa được làm.

## Nơi nhận và bằng chứng thiếu

| Nơi nhận | Đầu vào cụ thể và quyết định phụ thuộc |
|---|---|
| Claude/Minh | Soát nguồn gốc/graph/coverage/kiểm, đọc source trước lịch sử. Xác định mô hình thiết kế có điều kiện có đạt SPEC; chưa là nghiệm thu runtime |
| T040 | Pin nền+delta SMTP/hash code actual cùng schema/namespace. T038/T039 giữ pin gốc; không tự chuyển. Kiểm khả năng ghép theo delta/hồi quy khi được giao tổng hợp, chưa nhận ba nhánh đều đủ |
| P6 | Node/type/cạnh/operation/context/provenance, entity-only, shared-resource bindings và signal namespace. Nếu dùng tài nguyên chung phải nêu phép tính dùng binding; T035 chưa so DB→instance. Cây/timing span phải nhận riêng; không suy từ graph gộp |
| P9a/nhóm hệ thống | Mỗi operation tại dia-chi-tin-hieu.json có writer/owner/keys/test. Cần broker config/vhost/queue, DBlogic→instance→host, runtime names/alias, SMTP adapter, logs3tínhiệu và sampling/drop/clock/retention; kiểm thật theo từng biên |
| P9b | Graph/trace tách, manifest build/config/time, aliases có nguồn, queue metric đúng scope, label riêng. Không sửa trace từ nguồn static, không nối bằng correlation |
| P10 | Workload/nhánh/tiêm lỗi/nhãn giao thức riêng và quyền đánh giá; chưa được mở test hoặc dùng số cấu trúc làm bằng chứng lợi ích |

Các7nhóm OPEN có owner/input/hệ quả ở bao-phu-nguon.json#/open_items. Không có chặn cài đặt SMTP còn lại theo bộ kiểm hiện tại; source gaps vẫn giữ OPEN. Hai agent đồng ý không thay bằng chứng khoa học.

## Quyết định cần ghi sổ chính thức — trình riêng, chưa ghi

Phạm vi cần duyệt riêng: nối docs/DECISIONS.md và docs/WHY.md. Nội dung quyết định nguyên tử đề nghị: “Minh giao sửa hỗ trợ SMTP và kiểm lại; sau khi kiểm đạt tiếp tục T-037; giữ nguyên T-038/T-039 và không tự đổi pin hai nhánh.” Nguồn: nguyên văn LOG T037 Phiên3. Không gộp nghiệm thu hoặc lựa chọn P6 vào quyết định này.

WHY đề nghị ghi: bổ sung channel smtp cho quan hệ gọi để giữ đúng B13/B14; phương án ép http/rpc/internal làm đổi nghĩa, trường transport mới rộng hơn delta tối thiểu; điều kiện thất bại/protocol comparison caveat và kết quả kiểm dẫn file. Đây là lý do kỹ thuật cùng WHY52/53, chưa là bằng chứng lợi ích RCA. Không tự sửa hai sổ trong lượt này.

Nội dung đưa vào báo cáo đồ án: ranh giới thiết kế/quan sát/lợi ích, DBlogic/instance/host dùng chung, message/correlation/trace khác nhau, protocol chưa biết không tự điền, nguồn+oracle/phép chiếu có kiểm và các OPEN ảnh hưởng tích hợp. Không biến inventory/fixture thành runtime measurement.
