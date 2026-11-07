# Hồ sơ G3(a) — T-052

Trạng thái: hồ sơ dev để phản biện và Minh quyết, chưa khóa G3 hoặc mở dữ liệu. Nguồn quyết định là sổ và LOG; file này không chọn lại thiết kế.

## Sáu câu của cổng

1. Phục vụ DT18-NV2/NV3, bước 2–4 của cô, RQ3b/d và mô tả RQ3c. Hoãn RQ3a/(b) theo quyền đã ghi; P8–P10 còn nghĩa vụ riêng.
2. Dev phân xử được các can thiệp đã khai và một số cơ chế tính toán; chưa tách topology thật, lỗi vật lý, nhãn vùng hoặc khái quát hóa. TT ít topology/root; OB ít ô hữu hiệu; dev chọn lặp.
3. Đủ sáu baseline, giữ variant mạnh đã duyệt và lỗi/mẫu số. C-a0 đạt điểm dev cao hơn SimpleRCA ở hai bộ; M1 không hơn chung C-a0/C-d2. M4 OB có giới hạn tái lập, không che bằng đồng thuận reviewer.
4. Đã kiểm native/frame/flag/khóa/tầng/hạng, 15 đối chiếu EC2, pilot local TT/OB, 52 đối chiếu graph control, kiểm thống kê và firewall. Lượt lỗi và giới hạn của phép kiểm ghi báo cáo/LOG.
5. Có bảng theo dataset/fault/cell/vị trí N p75/p90/ca và ba worlds đúng phạm vi nguồn; cặp thắng/hòa/thua và vùng/C-e giữ riêng. Không cộng cờ thành tỷ lệ nguyên nhân.
6. Căn cứ các thành phần ở bảng dưới. Những câu thiếu bằng chứng giữ OPEN kèm phụ thuộc, không thay bằng mã WHY.

## Căn cứ thành phần

| Thành phần/trạng thái | Mục đích | Nguồn | Phương án và bằng chứng | Điều kiện thất bại/chưa phân xử |
|---|---|---|---|---|
| Ánh xạ/quan sát | DT18 + kỹ thuật | T043 hợp đồng/Đ19, m1.adapter và quan_sat | Tín hiệu mỗi nguồn, không dùng marker frontend thay timestamp thật; A0/worlds có điều kiện | Thiếu instrumentation/coverage không được collector khôi phục tự động |
| E1-U bật | Ứng viên giữ thông tin request + DT18 | WHY-55/58/72–76; native/ablation | TT bỏ E1 giảm; OB bằng. Giữ full/exclusive và nhánh CP đã không đạt điều kiện thử | Thiếu con, bất đồng bộ, clock, span bọc; exclusive không là CPU time |
| E2-C bật | Gán bằng chứng quan hệ; lựa chọn dev | WHY-72/73; K-b/KB/T13 | C giữ theo luật trên nền E5 bật, E2 đánh đổi giữa hai bộ; VC là phương án đã thử | Chưa định danh đầu lỗi mạng; VC×E5 chưa phân xử |
| E5 bật | Tách bằng chứng kế thừa theo cạnh/SCC | WHY-62/72/76 và T13 bo-E5 | Bỏ E5 giúp TT/hại OB; giữ quyết định nền, không chọn lại theo test | Phân lớp/quan hệ không xác nhận lan vật lý; thiếu matched control đầy đủ ở nhóm quan trọng |
| z+S1/G3-D1 | Thang/cổng lựa chọn dev | WHY-67/69/71; T048/T053 | Cổng quyết cờ, z đổi độ lớn, S1 phá hòa; đủ T4/T4b đã có, không lặp | c=1 phụ thuộc đơn vị; cực trị/max; không quy mọi ca hại cho IQR |
| E6a/E7 | Hạng/vùng đáp ứng DT18 | WHY-74/75; code xep_hang/e7 | E6b chiều đã thử hại; E7 hai cách mô tả đã kiểm | Chưa đo P/R/F1 vùng; PageRank đảo còn OPEN |
| E3(a)/E3b tắt | Kết cục lựa chọn dev | WHY-66/72/73 và T6 | Giữ kênh log lỗi gộp; không đồng nghĩa bỏ log | Drain/direction có thể đổi thông tin; nối log–span ưu tiên phạm vi, chưa bác lợi ích |
| E9/T12 tắt | Lựa chọn nền, đối chiếu snapshot | WHY-76; T051/T13 | Giữ cặp T12 mô tả, không chọn snapshot theo test | Revision runtime chưa nối chắc; messaging/data thiếu hai đầu |
| E8/P8/(b)/G-H | Nhu cầu đề tài và các gói sau | MRP P8–P10, Q-245 | Không vào đợt hiện tại; G4 khai thiếu P/R/F1 M1 công khai | Không nhận nhiệm vụ nguồn đã hoàn tất |

## B6 và điều kiện trước P7

- Code, config có nhanh_z/che_do và dấu vân tay: ma-tran-va-nguon.json. Chưa có commit khóa được Minh duyệt.
- Cổng/ε/α/m/δ/δ_d, lớp kênh, SCC/phủ đỉnh, ba worlds/A0 và trạng thái: giữ T043 với đính chính/WHY hiện hành; T13 không thay luật chọn.
- U/alias, hòa/lỗi/fallback, vùng/verdict, cohort/nhãn và thống kê: giao-thuc-p7-a.json và ke-hoach-tap-test.json. U TT68, OB10; không lấy danh sách root làm U. Nhãn chỉ ở evaluator sau seal.
- V0 chỉ truy vết, không quyết mở sự cố hoặc mức tin cậy root cho LLM. Chưa có nhãn lan độc lập dùng để phân tầng; không tự tạo nhãn vòng lặp.
- C-15 B giữ kết quả đầu, bản sửa dùng test báo riêng và kiểm bằng dữ liệu phù hợp mới. RE3 nguyên bộ một lần cho bản cuối, khóa hợp đồng/adapter/U/schema trước lần đó, chưa tải/mở.
- Máy P7 local theo Q-42. Đã có pilot TT/OB, C-e nặng và tuyến TORAI đúng env; số đo lát cắt không là cận tổng. Chốt tổng ma trận, worker theo RAM, 60 C-e/3 seed, timeout và trần trước chạy; chạy >1h cần Minh duyệt riêng.
- Runtime allowlist/hash data/private map thật chỉ materialize sau quyền; cơ chế/fixture và hash thành viên G1 đã có. Vị trí private map chốt trong SPEC P7.

Đây là các mục cần Minh quyết/hoàn tất khi khóa và giao SPEC P7, không phải giấy phép do agent tự cấp. Task T-052 mô tả có thể bàn giao, nhưng chưa đủ để tự mở test.

## Chuyển giao FlashTicket và các câu mở

P9/P10 nhận: hai đầu quan hệ DB/cache/messaging, trace/span/time/membership, alias service ổn định, log trace_id/span_id, quan sát nền lành nhiều tải, nhãn vùng độc lập. Collector không bổ sung được sự kiện chưa được instrumentation ghi. Cần dữ liệu mới sau khóa để kiểm tương tác E5/VC, hướng lan, log–span và độ bền điểm/đơn vị nếu Minh mở phạm vi đó. P8 đánh giá giải thích trung thành riêng. Không tuyên bố đã giải hết RQ2/RQ3/RQ5.

## Đề xuất ghi sổ quyền

Ngoài phạm vi ghi hiện tại: đề xuất nối docs/DECISIONS.md một mục theo đúng lời Minh, ghi Codex tự soát/triển khai có điều kiện T-052, phạm vi LOG/results/đúng dòng STATE và sửa nhỏ SPEC, pilot/chấm dev tối đa60 phút máy; EC2 hiện có tại IP Minh cấp, không cấp máy/mở test/commit/push. LOG đã giữ nguyên quyền; chưa tự ghi sổ ngoài phạm vi.
