# T-037 — bàn giao phần dừng do chặn hợp đồng

**Cần Minh quyết gói sửa chung. Task chưa hoàn tất, chưa chờ nghiệm thu.** Người làm Codex; Claude phản biện kết quả. Không tự mở lại T-036 đã đóng, không đổi pin hoặc gửi sang chat khác.

Đã có pin/hash và snapshot nguồn, bản ghi thiết kế một phần, coverage một phần và phản ví dụ SMTP tái lập. Xem kiem-dung-dan.md, bao-phu-nguon.json và runs/smtp-002/result.json. Chưa có graph/chiếu/binding/signal được kiểm toàn phạm vi hoặc oracle đúng đầy đủ sau chặn. Các bản ghi hiện có không được dùng như đầu vào P6 đã nghiệm thu.

## Vấn đề và phương án cần duyệt

Nguồn B13 §6/B14 §6 đòi Ticket→SMTP. T036 chỉ cho channel gọi http/rpc/internal. Không có channel vừa giữ đúng SMTP vừa được builder nhận. Chữ trong context/provenance không thay được transport ở cấu trúc; gán rpc/internal/http hoặc bỏ cạnh đều làm đổi nghĩa/phạm vi. Đây là lỗi thiết kế hợp đồng trong trường hợp mới được khảo sát, không là bằng chứng phương pháp RCA thất bại.

**CANDIDATE khuyến nghị:** bổ sung channel `smtp` tường minh cho quan hệ gọi, giữ type là vấn đề riêng phải đối chiếu nguồn. Giữ nguyên ID/provenance và phép chiếu; không tạo broker/email queue giả. Chỉ phần mới có channel SMTP; đầu vào cũ phải giữ kết quả. Comparator non-messaging hiện so đầu mút/type không xác nhận transport, vì vậy phải khai giới hạn HTTP/RPC/SMTP tương ứng; không đổi typed agreement thành xác minh protocol. Chưa chọn hoặc thực hiện phương án này.

Phương án khác: trường transport riêng với channel chung. Nó tổng quát hơn nhưng đổi schema/địa chỉ và phạm vi hồi quy rộng hơn; cần thiết kế và duyệt riêng. Giữ nguyên hợp đồng và ghi unsupported là trạng thái dừng hiện tại, không đủ để nhận mô hình FT đầy đủ hoặc bỏ delivery khỏi nghiên cứu.

## Phạm vi sửa đề nghị — chưa được phép làm

| File/phạm vi | Cũ → mới dự kiến; lý do/ảnh hưởng |
|---|---|
| src/do_thi_tinh/build.py | CHANNELS và guard gọi chỉ http/rpc/internal → nhận smtp theo phương án được Minh chọn; không sửa nghĩa internal/rpc để lách |
| results/T-036/hop-dong.md | Mô tả channel/kiểu/chiếu và giới hạn so transport → bổ sung SMTP/điều kiện loại gọi; không tự thay đổi quy tắc messaging |
| results/T-036/fixtures/smtp-input.json, smtp-expected.json | Thêm phản ví dụ literal/đáp án trước mã, cả hai mức, entity-only, shared signal và projection; chưa là fixture runtime |
| results/T-036/check.py | Thêm kiểm representation SMTP và hồi quy đầu vào cũ; không chạy lại vào tên run cũ |
| results/T-036/kiem-dung-dan.md, ban-giao.md, manifest.json và runs/<tên mới được giao>/ | Giữ mọi lượt, đo/kiểm/diff, snapshot/code-hashes/manifest mới; pin cũ giữ nguyên lịch sử |
| tasks/T-036-p5b-hop-dong-chung/LOG.md và đúng dòng T036 trong docs/STATE.md | Chỉ khi Minh quyết mở gói sửa; không tự mở lại từ T037 |
| docs/WHY.md, docs/DECISIONS.md | Trình và lưu riêng lựa chọn cùng quyền sửa/pin mới sau Minh duyệt; không ghi trong lượt này |
| tasks/T-037-p5b-flashticket/SPEC.md, tasks/T-038-p5b-trainticket/SPEC.md, tasks/T-039-p5b-online-boutique/SPEC.md | Pin hiện hành bị khóa. Sau sửa chung, trình cập nhật đúng đoạn pin ở cả ba SPEC và dòng tương ứng STATE theo quyền riêng; chưa đổi bất kỳ pin nào |
| results/T-037/oracle-v2.json và outputs/runs T037 tiếp theo | Viết oracle đúng đầy đủ trước converter, kiểm lại coverage/graph/chiếu/runtime fixture và bàn giao; không xóa oracle sai/lượt lỗi cũ |

Đây là bản đồ tác động để Minh chọn/duyệt gói cụ thể, không là lệnh mở task hoặc quyền sửa. T036 đã đóng: cần Minh quyết cách ghi nhận gói sửa và phạm vi, không tự đổi trạng thái vật chất của quyết định. Không đề nghị sửa platform/B13/B14 vì SMTP là nhu cầu thiết kế hiện có.

## Ảnh hưởng ba nhánh và nơi nhận

- T037: dừng graph/phép chiếu/khẳng định coverage đầy đủ; giữ nguồn/records độc lập. Không thu hẹp tiêu chí vì SMTP.
- T038/T039: không khẳng định hai hệ này có SMTP vì chưa khảo sát trong phiên này. Có thể tiếp tục phần độc lập với pin cũ; phần cần transport ngoài enum phải dừng. Không tự chuyển pin, không tự gửi cảnh báo sang chat khác. Sau gói sửa chung phải thống nhất một pin trước kết luận tổng hợp.
- T040: chưa được làm; tổng hợp không được gọi hợp đồng đã phủ FT từ kết quả T036 cũ.
- P6: phép dùng cạnh/binding/shared metric còn phải thiết kế trên dev; chưa chọn thuật toán/mức/tín hiệu. T037 không chứng minh sửa hạn chế P4 hoặc lợi ích đồ thị.
- P9a/P9b/nhóm hệ thống: cần địa chỉ/transport/message scope/host/instance và build/export/sampling/clock; riêng SMTP phải ghi tại Ticket/adapter, không giao collector tái tạo. Hợp đồng runtime hiện chỉ bàn giao phần chưa hoàn thiện.
- RQ3/RQ5/G3 vẫn OPEN; chưa kiểm hiệu quả trên public test hoặc FlashTicket. Không mở dữ liệu khóa.

## Nội dung cần lưu chính thức sau duyệt riêng

Đề nghị thêm một mục DECISIONS (không tự cấp mã): “Minh giao Codex triển khai T-037 theo SPEC hiện hành sau tự rà và kiểm khả thi một phiên; Claude phản biện kết quả; phạm vi ghi results/T-037/, nối LOG và đúng dòng T037 trong STATE; chưa duyệt tải nguồn mới.” Nguồn là nguyên văn lời giao tại LOG Phiên2, không gộp suy luận hay chấp thuận sửa hợp đồng SMTP vào quyết định này.

Vật liệu báo cáo đồ án: phân biệt nguồn thiết kế/quan sát/runtime/lợi ích; DB logic khác instance; shared metric không nhân bằng chứng; protocol/channel phải giữ đúng nghĩa. Các OPEN, record counts và phản ví dụ hiện tại không phải kết quả hiệu quả RCA.
