# Hồ sơ G3(a) — ứng viên checkpoint013

Chuẩn bị013 đã làm theo Minh duyệt; chờ Claude kiểm bản cài và Minh duyệt chạy. Gói hiện hành là `runs/chuan-bi-main-013/`, thay các plan/helper ứng viên011 cho lần chạy sắp tới. Không dùng `protocol.json` ở gốc T054 hoặc helper006/011 để phát013. Các gói đó giữ làm lịch sử.

[Báo cáo013](runs/chuan-bi-main-013/bao-cao.md) · [Nội dung duyệt cuối](runs/chuan-bi-main-013/de-nghi-duyet-main.md) · [Runbook](runbook.md) · [Manifest013](runs/chuan-bi-main-013/manifest.json).

| Phần trước G3 | Bằng chứng hiện tại | Trạng thái |
|---|---|---|
| Nguồn/B1 | TT60+OB34 metadata đối chiếu nguồn riêng; R1 locator mờ; full cohort giữ nguyên | PREPARATION; attestation/kiểm byte test mới sau quyền |
| A/B2/C | Mỗi EC2101fixture mã cuối; Windows transport68; báo cáo thiếu A/partial seed89hàng; kích hoạt sinh giả11kiểm | Đạt trong phạm vi fixture; không gọi là main |
| Tuyến DEV thay đổi | 15đối chiếu mới;14khớp nghiêm ngặt, một C-e sai khác số học đã được Minh chấp nhận riêng; M1 chính tái dùng012 | Ghi rõ ở parity-disposition, không đổi tolerance chung |
| Môi trường/code/phân lô |106pin code, runtime3.12/3.8 và4file vá trên hai EC2 mới;30TT mỗi máy, laptopOB/CIRCA/MicroRank/A | Kiểm cuối đạt; tài nguyên động kiểm lại trước phát |
| D1–D4/R3 | DECISIONS/WHY ngày07/11, OB-group-decision | Minh đã chốt; H1 RE3 vẫn OPEN theo D2 |
| Quyền test/nguồn/chuyển/run/chấm | grant-template có mọi cờfalse | Chờ Minh sau phản biện bản cài013 |

Tổng1.640job+2vị trí C-e thiếu hỗ trợ, gồm68UNSUPPORTED đã khai; bảng từng máy và group ở `candidate-validation.json#/hosts`. D4 báo chênh Hit@5 M1–M4 trên34/30/4OB, đủba world, mô tả; giữ A4 và mức thống kê. TORAI A là bảng phụ, một plan laptop, phát sau non-A của plan đó VERIFIED, preflight theo quyền/pin và không bình quân seed sống. Nguồn A cho main chưa được cấp. Hành vi thật của ca logts thiếu N và nhánh OB lệch số mẫu vẫn OPEN.

## Tiếp xúc trước G3 và ảnh hưởng lên giao thức

- **TT test, 006:** đã kiểm schema, byte/hash, mốc native, timestamp và cột `duration` của span để tính mốc kết thúc; đã chuyển bản sao TT theo lệnh chuẩn bị. Dùng thời gian để kiểm cửa sổ và phân loại trước chấm 58 ca C-e có lịch sử, 2 ca thiếu hỗ trợ theo A0. [Nguồn và đếm C-e](runs/chuan-bi-main-006/checkpoint-01-sources.json) · [Cột đọc](runs/chuan-bi-main-006/prepare_sources.py) · [Kiểm thời gian](runs/chuan-bi-main-006/source-temporal-final-check.json) · [Biên nhận chuyển](runs/chuan-bi-main-006/checkpoint-02-transfer.json)
- **Nezha-OB test, 006 → 008:** đã xem header, metadata sự kiện native và cột Time của 11 nguồn trên 34 ca. Có 30/374 cặp ca–nguồn thuộc bốn ca không thỏa guard cũ 5N/5A. Lần đọc này dẫn đến bản vá adapter `source_native` trước khóa. Bản vá giữ mẫu/thời gian theo từng nguồn, giữ cả 34 ca và mốc gốc. Hai ca có 2 hoặc 3 mẫu N. Kiểm hành vi M1/BARO trên đầu vào lệch số mẫu hiện dựa trên fixture (dữ liệu giả); đối chiếu dev thật chỉ có một ca 5N/5A, đầu vào và bản ghi khớp byte theo biên nhận. Audit T-026 xác nhận cả 22 ca dev và một dòng độ nhạy đều có 5 mẫu N và 5 mẫu A ở mỗi nguồn metric, theo cửa sổ đã kiểm. Tập dev này không có đầu vào cho nhánh lệch số mẫu. Khi báo kết quả OB phải khai rằng cấu trúc thời gian của chính cohort đã được dùng để sửa adapter. [Time, `/issues` và `/case_sources_checked`](runs/chuan-bi-main-006/OB-metric-time-window-check.json) · [Phép kiểm bản vá](runs/cai-ob-source-native-008/bao-cao.md) · [Dev, `/normalized_input_exact`, `/records_exact`](runs/cai-ob-source-native-008/dev-ob-001/parity.json) · [Audit dev T-026, bảng số hàng theo ca](../T-026/kiem-dau-vao.md#bảng-số-hàng-theo-ca)
- **TORAI A, 006:** giải nén đúng 180 CSV tác giả của cohort TT, xem header/thời gian. Audit cho thấy một logts thiếu toàn phần N; giữ đầu vào và ca. A là bảng phụ ngoài A4. Grant một ca dev là lịch sử; receipt 006 ghi phạm vi chuẩn bị cohort. Main A cần quyền riêng. [Nguồn, `/A_csv_files`](runs/chuan-bi-main-006/checkpoint-01-sources.json) · [Hạn chế A](runs/chuan-bi-main-006/A-input-limitation.json) · [Receipt chuẩn bị](runs/chuan-bi-main-006/preparation-grant.json)
- **RE3-OB:** TX0 là phân loại lịch sử tại G1. Đã xem metadata/schema; 011 có quyền B riêng và đọc hai cột owner của bản ghim để kiểm kê tên toàn cohort. Kết quả nêu phần còn thiếu cho U/alias/r, chưa chốt profile. [Schema](runs/chuan-bi-re3-009/inventory-schema.json) · [Quyền B](runs/hoan-thien-local-g3-011/checkpoint.json) · [Biên nhận, `/completed_column_reads` và `/measured_signals_or_times_read`](runs/hoan-thien-local-g3-011/inventory-owner-global.json)

**D1 đã chốt ngày07/11/2026:** giữ nguyên lịch sử phạm vi quyền006 chưa rõ, không diễn giải thành quyền hồi tố. Minh duyệt cách khai giới hạn tính độc lập của việc dùng cấu trúc thời gian cohort OB sửa adapter. Chưa có hạng/độ đo main. Quyền chạy/chấm hiện tại vẫn cần cấp riêng. [Quyết định](../../docs/DECISIONS.md) · [Nguồn lời chuẩn bị](runs/chuan-bi-main-013/preparation-permission.json).

## Sáu câu G3 và giới hạn nguồn

1. Câu hỏi chính là RQ3b và phần can thiệp tính toán RQ3d theo MRP, DT18 và hướng dẫn cô; chưa có kết quả test.
2. Cohort TT/OB, cửa sổ, U/alias, cấu hình, seed/world, policy lỗi/mẫu số và thống kê ghim trong protocol-candidate/contract/source-bundle013. Tiếp xúc OB ở trên giới hạn diễn giải độc lập; nhóm34/30/4 không phân xử riêng tác động adapter.
3. TT dùng TORAI B ba seed trong A4, OB dùng SimpleRCA M4 với giới hạn tái lập đã khai; A là bảng phụ. Không chọn lại baseline sau nhìn điểm.
4. Nút là service/thành phần; cạnh caller→callee. Log/metric gắn owner, trace giữ cha–con. E1 dùng hợp khoảng con; E2-C gán cạnh về callee; E5 dùng cạnh/SCC; E6a xếp tầng; E7 duyệt cạnh tạo vùng. T12-on có đúng hai snapshot ghim. C-a1 còn E1, nên không gọi mọi vế bỏ thành phần là bỏ mọi quan hệ.
5. Sau grant, báo theo dataset/ca/ô/world/support, giữ ERROR/TIMEOUT/UNSUPPORTED và lượt đầu đúng policy. Không có đối chứng đồ thị ngẫu nhiên thì không suy riêng lợi ích cấu trúc thật.
6. B6 được khóa vào đúng byte code/gói/config/env/cohort và quyết định cuối. H1 RE3 chưa đóng, D2 cho trình main TT/Nezha riêng; RE3 cần nguồn/profile/quyền riêng cho bản cuối. RQ3c chỉ mô tả vùng vì thiếu nhãn; RQ3a/M1(b), LLM và áp dụng FlashTicket còn lại, không coi xong T054 là xong đề tài.

Claude đã góp ý và thống nhất phần kế hoạch trước triển khai, chưa kiểm các output013 mới. Đồng thuận không thay bằng chứng. Chưa commit/push, chưa mở test hoặc phát main.
