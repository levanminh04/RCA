# T-049 — K-b và T6 trên nền z+S1

Codex là người làm. Claude là người phản biện chính thức. Phần chạy, kiểm và phân tích trong SPEC đã hoàn thành ngày 04/11/2026. Hồ sơ chờ phản biện và nghiệm thu của Minh.

## Kết quả và nền đề nghị

- K-b giữ E2-C theo luật. ΔMRR gộp là 14603/2358720, khoảng 0,006191. Cả ba thế giới cho KHONG_TAC_DUNG tại ngưỡng đã khóa. VC có tác động trên từng ca nhưng chưa đạt điều kiện thay C tại điểm chính.
- T6 có ΔMRR gộp 1/390, khoảng 0,002564. Cả ba thế giới cho KHONG_TAC_DUNG, hành động DE_XUAT_BO. Đề nghị giữ E3b tắt cho T-050. Minh chốt đề nghị sau phản biện.
- Nền đề nghị giữ z+S1, epsilon=0,05, alpha=0,01, E1-U, E2-C, E5 bật, E3(a)/E3b/E9/T12 tắt, E6a và cạnh quan sát. Chi tiết ở [nền đề nghị](nen-de-nghi-T050.json). G3 và test vẫn chưa mở.

Ngoại lệ ở Phụ lục C bước 6 đã được đối chiếu: E3b không phải phần cuối cùng đáp ứng P6 tầng 2/DT18, vì nền đề nghị vẫn có E1-U dùng cấu trúc cha–con, E2-C gán bằng chứng cạnh và E5 dùng quan hệ tách tự sinh/kế thừa. Vì vậy đề nghị bỏ E3b không làm mất phần tính toán dùng quan hệ này. Điều đó chưa xác nhận hiệu quả của đồ thị.

Nguồn ở [K-b](k-b.json) nhánh /K-thang-VC và [T6](t6.json) nhánh /T6-C-E3b, các mục /ket_hop, /hanh_dong và /theo_the_gioi/P. Đây là lựa chọn thiết kế trên dev. RQ3 và hiệu quả trên dữ liệu độc lập còn mở.

## Phạm vi và tính đúng

DT18 §2 và hướng dẫn cô §1 yêu cầu ánh xạ dữ liệu lên đồ thị, thực nghiệm, đánh giá và phân tích trường hợp. T-049 kiểm gán cạnh E2-VC và tần suất E3b. Nút là service/owner, cạnh là lời gọi cha–con. Metric và log gắn vào nút. E1 dùng cấu trúc span tạo thời gian độc quyền. E2 gán bằng chứng khoảng ngoài span trên cạnh. E5 dùng cạnh và lớp kênh phân loại tự sinh/kế thừa. E6a dùng khóa cục bộ.

K-b giữ E5 bật, chỉ đổi C/VC. T6 giữ các thành phần khác và thêm tần suất. Chưa kiểm đủ tương tác VC × E5, đối chứng bỏ quan hệ hoặc quy tắc đơn giản trên cùng đồ thị. Các phần đó và thử nghiệm FlashTicket thuộc bước sau. Nguồn trực tiếp ở [SPEC T-049](../../tasks/T-049-k-b-va-t6/SPEC.md), [MRP](../../docs/MRP.md) P6/P7, [DT18](../../docs/reference/sources/DT18-de-tai-va-nhiem-vu.md) §2, [hướng dẫn cô](../../docs/reference/sources/advisor-2026-09-23.md) §1 và WHY-67/70–72.

Đã tích hợp phục hồi trung gian tràn vào src/m1/e4.py theo Q-237, giữ đường native trên mẫu thường. Điểm cuối thật sự ngoài miền giữ hợp đồng S21. Tổng khóa thật sự tràn vẫn cho lỗi native. Runner dừng khi gặp đơn vị z ngoài miền. T1 T-053 được kiểm để dùng lại đủ 238 bản ghi, gồm seed và xáo. Nguồn ở [tái sử dụng](tai-su-dung.json) nhánh /T1.

374 phép T-044 và 16 phép T-049 đạt. Oracle số học và đường chuỗi được đối chiếu giữa bản trước sửa, candidate và bản tích hợp. Helper K-b/T6 ghi hành động cho trái chiều, phụ thuộc quan sát và C-e chưa kiểm được. Đã sửa lỗi tóm tắt độ nhạy lấy kết cục ngưỡng chính trong khi hành động dùng ngưỡng khác, trước khi chấm T-049. Hồi quy ΔMRR=0,007 phân biệt δ=0,005 và δ=0,01 đạt. Nguồn ở [hồi quy T-044](runs/hoi-quy-001/pytest.log) và [hồi quy T-049](runs/kiem-cong-cu-truoc-cham-001/pytest-002.log).

E_X giữ từ T0 đã ghim, E2-VC có 17 ô và E3b có 12 ô. CP không đủ điều kiện ở cả hai dataset theo tỷ lệ cha có con chồng lấn hơn 1 ms. Số ở [ô chấm](o-cham.json), nhánh /CP và /E_X.

## Lượt chạy

Hai pha đủ 52 cửa sổ thật và 30 cửa sổ giả, mỗi bản ghi có P/S_lo/S_hi. K-b chạy thêm hai cấu hình VC, dùng lại hai nền C. T6 chạy thêm một cấu hình trên nền C, dùng lại vế tắt. Tổng có 246 bản ghi phương pháp mới. Hai pha chấm có 492 lượt cấu hình–cửa sổ do nền C xuất hiện ở cả hai pha.

Mỗi cặp giữ cùng máy theo cửa sổ. Pilot hai máy khớp hash đầu vào, cờ, tầng, khóa và nhóm hòa trong dung sai đã khai. Đơn vị chung và tập U được kiểm trước seal. Hai seal được ghi vào LOG trước ghép nhãn. T6 ghi rõ đã nhìn kết cục K-b.

| Pha | Thời gian controller | Cửa sổ laptop | Cửa sổ EC2 | Bản ghi mới |
|---|---:|---:|---:|---:|
| K-b | 70,97 phút | 47 | 35 | 164 |
| T6 | 37,66 phút | 47 | 35 | 82 |

Nguồn ở [thời gian](thoi-gian.json), nhánh /K-b/wall_seconds và /T6/wall_seconds. Số vận hành gồm capture/oracle và chia sẻ cache. Seal, chấm, phân tích và báo cáo có log riêng, nên đây chưa là benchmark cô lập của thuật toán. Phân bổ theo máy của nền cũ chưa tối ưu thời gian, bộ điều phối chưa cân lại hàng đợi khi EC2 rảnh. Điểm này đã báo Minh.

## Bảng xếp hạng

MRR dưới đây ở P. Kết cục và ΔMRR của hai phép chính giống nhau ở ba thế giới.

| Cấu hình | RE2-TT | Nezha-OB | Gộp |
|---|---:|---:|---:|
| K-thang-C | 0,927778 | 0,872727 | 0,904487 |
| K-thang-VC | 0,966667 | 0,834330 | 0,910678 |
| K-day-du-C | 0,927778 | 0,833333 | 0,887821 |
| K-day-du-VC | 0,966667 | 0,792012 | 0,892774 |
| T6-C-E3b | 0,927778 | 0,878788 | 0,907051 |

| Cấu hình | Hit@1 | Hit@3 | Hit@5 | NDCG@5 | Avg@5 kỳ vọng | Rerank@1, K=5 |
|---|---:|---:|---:|---:|---:|---:|
| K-thang-C | 0,826923 | 0,980769 | 1,000000 | 0,928911 | 0,950000 | 0,826923 |
| K-thang-VC | 0,846154 | 0,965812 | 0,973291 | 0,924357 | 0,943376 | 0,869374 |
| K-day-du-C | 0,807692 | 0,961538 | 1,000000 | 0,916287 | 0,938462 | 0,807692 |
| K-day-du-VC | 0,826923 | 0,942308 | 0,983974 | 0,914166 | 0,927564 | 0,840391 |
| T6-C-E3b | 0,826923 | 1,000000 | 1,000000 | 0,931087 | 0,957692 | 0,826923 |

Retrieval@5 bằng Hit@5. Rerank@1 dùng tổng Hit@1 chia tổng Hit@5. Bảng AC báo kèm dùng thứ tự hiển thị, có thể khác độ đo kỳ vọng khi hòa.

| Cấu hình | AC@1 | AC@3 | AC@5 | Avg@5 theo AC |
|---|---:|---:|---:|---:|
| K-thang-C | 0,826923 | 0,980769 | 1,000000 | 0,950000 |
| K-thang-VC | 0,846154 | 0,961538 | 0,961538 | 0,938462 |
| K-day-du-C | 0,807692 | 0,961538 | 1,000000 | 0,938462 |
| K-day-du-VC | 0,826923 | 0,942308 | 0,980769 | 0,926923 |
| T6-C-E3b | 0,826923 | 1,000000 | 1,000000 | 0,957692 |

Nguồn ở [chỉ số K-b](runs/kb-001-cham/chi-so.json) và [chỉ số T6](runs/t6-001-cham/chi-so.json), đường dẫn /<cấu hình>/that/<dataset hoặc gop>/P. Từng ca, ô, thế giới có trong kq.json và chi-so.json cùng thư mục. M5 tăng từ 0 lên 2 khi đổi C→VC ở cả hai bối cảnh, giữ 0 ở hai vế T6. Điều kiện riêng E5 chỉ áp khi cặp đang đảo E5, nên M5 này được báo kèm trong K-b.

## K-b và cơ chế

Cặp chính có ba ca tăng RR, hai ca giảm, 47 ca bằng. ΔMRR RE2 là 7/180, Nezha là -38317/997920. Hai chiều ngược nhau nhưng vế Nezha chưa thấp hơn -1/22, nên luật không trả TRAI_CHIEU_DATASET. C-e không tăng N1. Nhánh đầy đủ cũng KHONG_TAC_DUNG và chỉ báo kèm.

VC định danh ở 26/52 ca thật, không định danh ở 10 ca, đồ thị cạnh có cờ rỗng ở 16 ca. Không có dự phòng do vượt 25 đỉnh. Mốc giả có 25 đồ thị rỗng, 5 trường hợp không định danh. Kết cục không được giải thích bằng việc VC chủ yếu rơi về C. Số ở [đếm cơ chế](runs/kb-001-cham/co-che-dem.json), khóa theo cấu hình, cửa sổ và thế giới.

Trong 26 ca định danh của cặp chính tại P, root thuộc tập định danh ở 19 ca và không thuộc ở 7 ca. Trong 7 ca sau có hai ca Nezha bị hỏng, bốn ca ts-route-service và một ca ts-auth-service. Ba ca route giữ RR=1, một ca route giữ RR=1/2; ca auth giữ RR=1. Việc root không được định danh không tự làm hỏng thứ hạng khi còn bằng chứng khác. Có 21/26 ca đã có RR=1 ở C, chỉ 5 ca còn chỗ tăng RR. Điều này giới hạn khả năng quan sát lợi ích thêm của VC; vẫn có thể quan sát tác hại. Số theo ca ở [đối chiếu phản biện](runs/dap-phan-bien-001/doi-chieu.json), nhánh /R2/cases và /R2/root_not_identified_cases. Đây là phân tích sau nhãn, không dùng để chọn lại tập ca.

- dev-f36d0647d5 có ba cạnh có cờ quanh ts-order-service. VC đưa cạnh ra tới ts-station-service về đỉnh định danh ts-order-service, lấy max tất cả cạnh được phủ. Max root tăng từ 1442,520858 lên 1501,039305. F_I của latency-90 đổi từ 0 sang 1. RR từ 1/2 lên 1. Phép đổi tác động cả root và thực thể cạnh tranh.
- dev-a915aa2424 định danh ts-travel-service. Max root từ 3881,562205 lên 4834,194981, RR từ 1/3 lên 1. Ca đối chiếu dev-a5cabe5fa7 cũng định danh ts-travel-service nhưng điểm thao tác 5256,929688 đã lớn hơn mọi cạnh, RR giữ 1. Ca này có thêm tín hiệu tài nguyên, chưa khớp toàn chữ ký. Hai ca RE2 không có đối chứng đúng khớp toàn chữ ký.
- dev-607751ac0a có frontend→cartservice và frontend→checkoutservice. Phủ tối thiểu duy nhất là frontend. Root checkoutservice mất kênh cạnh duy nhất, từ tầng1 xuống tầng3, RR từ 1 xuống 2131/15120.
- dev-63c30faf34 tương tự với frontend→adservice và frontend→recommendationservice. Root xuống tầng3, RR từ 1/2 xuống 4861/22680.
- dev-9b9397a4dc định danh recommendationservice. Điểm cạnh nhận từ recommendationservice→productcatalogservice, max root từ 2,108773 lên 22,855399, RR từ 1/5 lên 1/2.
- Đối chứng dev-6c9afc9822 có root emailservice chỉ mang kênh cạnh. Đồ thị có một cạnh checkoutservice→emailservice, hai phủ tối thiểu, không định danh. Kênh root được giữ, RR=1 ở hai vế. Trường hợp này phân biệt tác động định danh với chỉ sự có mặt của kênh cạnh.

Hai ca RE2 được VC sửa chính là hai ca bị E2-C làm hỏng trong T-053. Trên nền E1+E5, cả hai có RR=1; thêm E2-C làm dev-f36d0647d5 xuống 1/2 và dev-a915aa2424 xuống 1/3. VC đưa cả hai về 1, khôi phục toàn bộ phần giảm MRR RE2 7/180 đã ghi trong WHY-72. MRR RE2 của E1+E5 và K-thang-VC cùng bằng 29/30. Đây là đánh đổi cụ thể: sửa phần hại đã biết trên RE2 nhưng làm hỏng hai ca Nezha. Nguồn ở results/T-053/runs/k-cham-001/kq.json, nhánh /cau_hinh/K-E1+E5/ca/<mã ca>/theo_the_gioi/P/RR và /cau_hinh/K-E1+E2+E5/ca/<mã ca>/theo_the_gioi/P/RR; đối chiếu T-049 tại [bằng chứng R1](runs/dap-phan-bien-001/doi-chieu.json), nhánh /R1. Không đổi cặp so, luật hoặc nền vì quan sát sau này.

Ở dev-63c30faf34 còn thấy một đường tương tác VC→E5 cụ thể. Khi bằng chứng cạnh bị chuyển khỏi adservice và recommendationservice, ba kênh latency lan ngược của frontend mất các giải thích E5, F_I đổi 0→1; frontend từ tầng2 lên tầng1. Ở dev-607751ac0a, frontend vốn ở tầng1; kênh E2VC được gán thuộc lớp khong_lan, không được E5 giải thích. M5 đổi 0→1 đúng ở hai ca này. Root của hai ca vẫn mất kênh cạnh duy nhất như chuỗi đã mô tả. Nguồn ở [hồ sơ K-b](runs/kb-001-cham/doc-co-che.json), nhánh /pairs/K-thang-VC/profiles/<mã ca>/world_P_off và /world_P_on; bản trích tại [bằng chứng R2](runs/dap-phan-bien-001/doi-chieu.json), nhánh /R2/VC_E5_paths. Đây là chuỗi tính toán trên hai ca, chưa phải phép 2×2 phân xử đầy đủ tương tác VC/E5.

Đã tái lập chuỗi tính toán trên. Nguyên nhân vật lý của khoảng ngoài span và vì sao hai cạnh ra từ frontend cùng có cờ còn mở. Nhãn không đi vào phép phủ. Giả định phủ bằng ít đỉnh nhất phù hợp một số ca và làm hỏng một số ca. Chưa kiểm đủ tương tác VC × E5.

Nguồn ở [hồ sơ K-b](runs/kb-001-cham/doc-co-che.json), nhánh /pairs/K-thang-VC/profiles/<mã ca>, [so sánh](runs/kb-001-cham/so-sanh-ca.json) và [replay cặp](runs/kb-001-cham/replay-cap.json). Replay dựng lại toàn bộ phép gán/gộp max, E5/FI, khóa, tầng và nhóm hòa trên 492 vế.

## T6 và cơ chế

T6 chỉ tăng RR ở dev-9b9397a4dc, từ 1/5 lên 1/3, 51 ca giữ RR. Khóa root recommendationservice giữ nguyên. Hai kênh tần suất giảm của root có F_I=0. Lợi ích đến qua thực thể cạnh tranh.

Khi E3b bật, frontend và checkoutservice có các kênh giảm tần suất thuộc lớp lan xuôi. Cạnh frontend→currencyservice tạo giải thích E5 cho NetworkTransmitBytes của currencyservice. Cạnh checkoutservice→emailservice tạo giải thích cho SyscallRead của emailservice. Hai thực thể từ tầng1 xuống tầng2. Root giữ tầng1 nên lên hạng. Thông tin đếm có tác động dù không thắng max của root.

Đối chứng cùng chữ ký ở vế tắt là dev-607751ac0a, root checkoutservice có kênh cạnh tự sinh và RR=1 ở hai vế T6. Đây là phép so khác với K-b. Nguồn ở [hồ sơ T6](runs/t6-001-cham/doc-co-che.json), nhánh /pairs/T6-C-E3b.

Ở P trên ca thật có 5286 đơn vị tần suất–cửa sổ đủ hỗ trợ, 4 thấp hỗ trợ. Có 84 cờ tăng và 690 cờ giảm, gồm 4 NEW_OP và 22 STOPPED. Sau E5 còn 134 kênh tần suất tự sinh và 640 kế thừa. Những số này có thể cùng phản ánh một luồng request.

Nhóm max giữ PV ở 825 thực thể–cửa sổ thật, NONE→DEM ở 81, PV→DEM ở 6, DEM→PV bằng 0. Nhóm tính trên kênh hiệu lực của tầng đang xếp nên có thể phản ánh đổi F_I hoặc tầng. Định nghĩa đã khai ở [định nghĩa phân tích](dinh-nghia-phan-tich.json), số ở [nhóm kênh T6](runs/t6-001-cham/nhom-kenh.json), nhánh /frequency và /max_transitions.

Tần suất giữ kiểm nhị thức như phạm vi đã cài và nghiệm thu T-046. D1 hiệu chỉnh phân tán áp vào log có mốc N. Điểm đếm giữ thang E4. Kết quả còn phụ thuộc thang trộn, quy tắc kế thừa và quan sát A0.

## Mốc giả và độ bền

N1 trung bình ở 30 mốc giả tăng từ 147/10 lên 77/5, tăng 7/10 thực thể/cửa sổ. Có 25 thực thể–cửa sổ vào tầng1 và 4 ra, tăng ròng 21. Tổng N1 đổi ở 14 cửa sổ, tập tầng1 đổi ở 21 cửa sổ. V0 vẫn CAUSE_FOUND 30/30 ở hai vế. N1 không kích hoạt HẠI tại h=1 nhưng kích hoạt tại h=0,5.

Ví dụ dev-3ae0a6c15a ở mốc giả tăng từ 13 lên 17 thực thể tầng1. Kênh đếm preserve giảm, route/station/train tăng, qua cổng và giữ F_I=1. Điểm đếm thấp vẫn đủ đưa thực thể từ tầng3 lên tầng1. Bỏ E3b và replay khớp vế tắt. Số ở [nhóm kênh](runs/t6-001-cham/nhom-kenh.json), nhánh /changed_tier_windows/T6-C-E3b|ce|dev-3ae0a6c15a/P và dòng 6 của [dấu vết](runs/t6-001-cham/co-che.jsonl).

N1 là mức hại tương đối chưa hiệu chuẩn. Chưa xác nhận an toàn báo động hoặc nguyên nhân biến động tần suất. Muốn phân biệt thay đổi tải, lỗi xử lý và thay đổi thu thập cần đầu vào độc lập tương ứng. Không quy thiếu quan sát từ riêng cờ bất thường.

Bootstrap theo ô dùng 1000 mẫu, seed đã ghim, δ_d gốc và E_X. K-b chính có 382 mẫu giữ C, 374 thay VC, 244 chờ Minh. T6 có 965 mẫu đề xuất bỏ, 27 HẠI/bỏ và 8 giữ bật. Đây là độ bền trên dev đã dùng để thiết kế.

Riêng C-e của VC không phân xử được tác hại khi VC có đỉnh định danh: 25/30 đồ thị cạnh có cờ rỗng và 5/30 không có đỉnh định danh, nên phép gán VC trùng C theo cấu tạo. Đã đối chiếu cả ba thế giới: kênh, F_I, khóa, tầng, nhóm hòa và N1 đều trùng; N1 trung bình hai vế cùng 147/10. Trạng thái luật KHONG_KICH_HOAT được giữ vì chênh N1 bằng 0, nhưng không đọc là bằng chứng an toàn. Vì vậy 374 mẫu bootstrap chọn VC chỉ là hành động của luật trên mốc giả không kích hoạt nhánh định danh, chưa xác nhận an toàn cho trường hợp VC thực sự chuyển bằng chứng. Nguồn ở [bằng chứng R3](runs/dap-phan-bien-001/doi-chieu.json), nhánh /R3. Không đổi mã kết cục hoặc ngưỡng sau khi xem số.

K-b đổi sang GIÚP ở δ=0,005, giữ C ở δ=0,02 và h=0,5/2. T6 giữ đề xuất bỏ ở δ=0,005/0,02 và h=2, đổi sang HẠI ở h=0,5. Bỏ từng ô làm hành động K-b khác điểm chính ở 3/23 lượt, T6 đề xuất bỏ ở 23/23 lượt. Nguồn ở [độ bền](do-ben.json), nhánh /K-b và /T6. Không chọn lại ngưỡng từ độ nhạy.

## Kiểm cuối và giới hạn

Kiểm độc lập đạt 624 RR và 10000 tình huống bootstrap/độ nhạy K-b, 312 RR và 5000 tình huống T6. Seed và các lượt bỏ từng ô được tái lập. Nguồn ở kiem-doc-lap.json trong thư mục chấm từng pha. Replay cặp đạt 492 vế K-b và 246 vế T6.

Lượt lỗi công cụ được giữ. Pilot EC2 đầu dùng nhầm môi trường T-031 thiếu networkx, sau sửa sang T-025 đã ghim. Hai phép so pilot đầu lỗi đọc trường job, sau sửa và kiểm lại trên bản ghi đã lưu. Kiểm replay đầu xét cả owner của metric không có cờ ngoài U, sau sửa đúng tập kênh E5 dùng. Một lượt test T-044 tạo fixture tạm ngoài phạm vi trong thư mục pytest mặc định, đã ghi LOG. Các lượt sau đặt thư mục tạm trong T-049.

Đã giữ bản trước sửa, lịch sử lỗi và bản ghi phương pháp. Code dùng chung chỉ sửa e4.py. SPEC giữ bản Minh đã duyệt. Hồ sơ ở [manifest](manifest.json), [LOG và prompt Claude](../../tasks/T-049-k-b-va-t6/LOG.md).

Đã đối chiếu phản biện Claude ngày 04/11/2026. R1 đúng, R2 đúng về hai thống kê và chuỗi cơ chế nhưng sai chi tiết rằng cả bốn ca route đều RR=1, R3 đúng về giới hạn phân xử. Các bổ sung ở trên dùng trung gian đã lưu, không chạy lại phương pháp. Bản báo cáo/manifest trước sửa và nguyên văn phản biện được giữ dưới runs/dap-phan-bien-001/.

Đầu ra đủ để phản biện việc giữ C và đề xuất bỏ E3b trong phạm vi dev đã kiểm. Còn mở việc Minh chốt nền T-050, phản biện Claude, hiệu quả độc lập, tương tác VC/E5 đầy đủ, đối chứng dùng quan hệ, verdict, chế độ (b), RE3-OB và FlashTicket. Dừng phản biện không thay bằng chứng còn thiếu.
