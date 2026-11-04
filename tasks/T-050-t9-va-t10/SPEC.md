# T-050 — Chọn cách xếp hạng T9 và mô tả vùng T10

- **Trạng thái** P1 và nền đã chốt ngày 04/11/2026 (Q-239, Q-240). Bản SPEC đã cập nhật theo nội dung thống nhất, chờ Minh cho phép chạy với ngân sách ở mục Chi phí ước lượng.
- **Người làm** Codex. **Người phản biện** Claude.
- **Thuộc gói** P6, chuẩn bị P7. **Cổng** G3 chưa mở.

## Mục tiêu

T9 chọn cách xếp hạng nguyên nhân trên dev chế độ (a). T10 mô tả hai cách dựng vùng nghi ngờ trên đồ thị. Nguồn trực tiếp là `docs/MRP.md` §2.3, P6 tầng 3–4 và RQ3; `docs/WHY.md` WHY-02, WHY-69–72; `tasks/T-043-thiet-ke-rca-m1/SPEC.md` Q9–Q10, B2–B4 và Phụ lục C; mục T-050 của `docs/KE-HOACH-SAU-T047.md`; DT18 §2 và hướng dẫn của cô ngày 23/09/2026, bước 2 và 4.

Nút là thực thể dịch vụ. Cạnh là lời gọi quan sát từ span cha–con trong N ∪ A. E1/E2/E5 chuyển log, trace và metric thành bằng chứng tự sinh hoặc kế thừa trước xếp hạng. E6a sắp theo tầng và khóa cục bộ trên bằng chứng đó. E6b thêm PageRank cá nhân hóa trên đồ thị con bất thường, dùng `max(s)` của K_I làm khối lượng. E7 dùng hướng cạnh hoặc liên thông vô hướng theo hai cách đã đặc tả. E6b là ứng viên để đáp ứng hướng phương pháp của cô và MRP, chưa có bằng chứng T9 về lợi ích.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Phép kiểm | Diễn giải và giới hạn |
|---|---|---|
| Trên cùng nền đã chốt, E6b có cải thiện xếp hạng so với E6a+S1 không? | T9 áp luật C lên cùng tập ca, điểm trước E6 và ba thế giới. Báo RR theo ca, MRR gộp/từng dataset và độ bền theo ô. | T9 phân xử lựa chọn xếp hạng trên nền này. Phép chính đồng thời đổi khóa xếp hạng. |
| Điều gì làm đổi thứ hạng? | Báo kèm E6a+S0. Theo vết ca tăng, giảm và ca đúng có điều kiện tương ứng từ K_I/K_raw → v → cạnh chuyển khối lượng → π → khóa/hòa → RR. | S0 là xếp theo điểm cục bộ không dùng S1. E6b còn dùng K_raw để phá hòa khi π và K_I bằng nhau. Khi cần phân biệt tác dụng cạnh với phá hòa, đối chiếu khóa E6b khi thay π bằng v và giữ các phần khóa khác. Đây là chẩn đoán từ trung gian, không tham gia chọn cấu hình. |
| Vùng nghi ngờ chứa root đến đâu và rộng thế nào? | T10 mô tả hai cách E7 ở P, dùng mỗi ứng viên trong nhóm đầu T và kỳ vọng đều theo D20. | Báo độ chứa root và độ rộng của vùng nghi ngờ. Nhãn vùng ảnh hưởng đầy đủ còn thiếu. Cập nhật trên cấu hình cuối ở T-052. |

Trên nền K-thang-C, 43/52 ca thật có RR=1 tại P, nên cả ca được sửa lẫn ca đang đúng bị hỏng đều quan trọng. Trên 52 ca thật, tỷ trọng lớn nhất của v có trung vị khoảng 0,9233. Trong 45 ca có ít nhất hai nút dương, 27 ca có tỷ lệ điểm lớn nhất/nhì > 10. Bảy ca chỉ có một nút dương. Khối lượng khởi tạo tập trung có thể hạn chế tác dụng lan truyền dưới thang z hiện tại. Cần dùng π, chuyển khối lượng và khóa thực tế để phân biệt giả thuyết này với ảnh hưởng của cạnh hoặc phá hòa.

## Đầu vào

- Nền đã chốt theo Q-239 và WHY-73, với cấu hình lưu ở `results/T-049/nen-de-nghi-T050.json`, là E1-U, E2-C, E5 bật, z+S1, epsilon 0,05, alpha 0,01, chế độ cổng G3/D1 và cạnh quan sát. E3(a), E3b, E9, T12 tắt. Cờ đánh đổi theo dataset của E2 theo WHY-72 vẫn là giới hạn khi diễn giải.
- `results/T-049/manifest.json` và `results/T-049/runs/t6-001-seal.json`. Chọn entry `config=K-thang-C`, dùng `source_config` và mã ca để đọc bản ghi/dấu vết đúng. Tập gồm 52 ca thật và 30 cửa sổ giả, mỗi cửa sổ có P, S_lo, S_hi. Kiểm manifest, kích thước, SHA-256, mã ca, mốc, cấu hình và revision trước khi dùng. Dùng `trace.xep[0:3]`, giữ nguyên điểm chính xác `s_q`, cờ, F_I, `co_OK`, m, tập U. Dùng `extra.canh`, `inherited_by` và metadata E7 từ bản ghi native. Kiểm nguồn lịch sử bằng `results/T-050/ban-giao-T049/kiem-nguon.py` và manifest bàn giao cùng thư mục. Hồ sơ này giữ byte của nguồn quản trị đã được băm ở mốc T-049.
- E_X(E6b) lấy từ `results/T-043/ks16/dem-sau-ghep-nhan.json#/o_kich_hoat/E6b`, kiểm theo manifest T-043. Có 21 ô, gồm 8 RE2-TT và 13 Nezha-OB. Tập E_X nằm ở pha đánh giá, tách khỏi phương pháp và pilot.
- C-c/C-g dùng `results/T-024/ban-ghi-dua-vao-cham.json` theo `results/T-024/work/danh-sach-tep-cuoi.json` và bảng `main` của `results/T-026/ban-ghi-dua-vao-cham.json` theo `results/T-026/runs/session-005/handoff-manifest.json`. RE2 lấy `native` của BARO, SimpleRCA M4 và TraceRCA lọc hữu hạn. Nezha lấy `native`, `M4`, `finite` tương ứng. Ghép theo mã ca, mốc, đơn vị, cửa sổ, mapping, giao thức và nguồn nhãn ở pha 2. Kiểm khóa phiếu SimpleRCA ở `entity_ranking[].key`, tập trả về và nhóm hòa.
- Dùng code `src/m1/xep_hang.py`, `src/m1/e7.py`, `src/m1/doi_chung.py`, `src/m1_danh_gia/` và lớp giải mã `Kenh` từ đường kiểm T-049. Xác nhận hash và môi trường trước pilot. Môi trường đề nghị là Python ghim ở `results/T-049/manifest.json#/runtime`, với `OPENBLAS_NUM_THREADS=1` và `-B`.

## Ma trận và bảng hành động

| Phần | Cấu hình | Vai trò |
|---|---|---|
| T9 chính | E6a+S1 ↔ E6b, 82 cửa sổ × ba thế giới | Chọn theo luật C, chỉ đổi E6 ở cấu hình. S1 không áp trong nhánh E6b theo `src/m1/chuoi.py:566`. |
| T9 báo kèm | E6a+S0 ↔ E6b, cùng đầu vào | Đọc ảnh hưởng của cách xếp và phá hòa. Giữ thang điểm z. |
| C-c | RRF k=60 của ba baseline, 52 ca thật | Chỉ báo cáo, dùng hạng trung bình cho nhóm hòa và Fraction. ERROR của một baseline đóng góp 0. |
| C-g | SimpleRCA + E6b, 52 ca thật | Chỉ báo cáo. Giữ đúng tập SimpleRCA trả về, nhóm điểm 0 và nhánh dự phòng. |
| T10 | Hai cách E7, thế giới P | Mô tả vùng của cấu hình sau T9. Nếu lựa chọn còn OPEN thì ghi mô tả theo ứng viên, chưa gọi là vùng của nền đã chọn. |

T9 dùng `buoc=luat_C`, thành phần `E6b`, số học Fraction, ngưỡng δ=0,01, δ_d=1/30 cho RE2-TT, 1/22 cho Nezha-OB và dung sai N1 h=1 theo luật hiện hành. Giữ δ_d gốc trong các lượt độ bền. UV-6 và điều kiện riêng E5 không áp cho cặp chỉ đổi E6. Giữ mẫu số, trạng thái lỗi/thiếu bằng chứng và quy tắc tie-aware của bộ chấm. Ghi ba kết cục riêng và trạng thái C-e. N1/V0 dự kiến bất biến do F_I/tầng không đổi, nên C-e không phân xử an toàn báo động của E6b. Mẫu số C-e bằng 0 ghi chưa kiểm được. Dùng kết cục sau khi kết hợp thế giới để đọc bảng hành động, đồng thời giữ kết cục riêng của P.

| Kết cục T9 | Hành động |
|---|---|
| GIÚP | Giữ E6b theo luật. |
| HẠI | Giữ E6a+S1 theo luật. |
| KHÔNG ĐỦ CA hoặc phụ thuộc quan sát | Giữ E6b theo mặc định D2a/D2f và ghi chưa phân xử. Báo kết cục từng thế giới, gồm vế P có HẠI nếu phát sinh, để Minh xem cờ trước bước phụ thuộc. |
| TRÁI CHIỀU theo ô/dataset | Trình Minh, nền sau T9 còn OPEN. |
| KHÔNG TÁC DỤNG | Đề xuất giữ E6a+S1 và tắt E6b theo P1 đã duyệt (Q-240, WHY-74). E1/E2/E5 vẫn tác động đến thứ hạng qua bằng chứng và tầng. E6a sắp theo khóa cục bộ. |

Nếu kết cục là KHÔNG TÁC DỤNG, giới hạn phát biểu ở lợi ích chưa đạt ngưỡng trên nền z hiện hành. Cách hiểu P1 không thay hành động HẠI và không xác nhận hiệu quả độc lập. Căn cứ đọc nguồn và bản đáp lưu trong LOG.

## Các bước và kiểm đúng đắn

1. Kiểm nguồn, ghim đầu vào và tạo gói trung gian một lần. Tái tạo đúng E6a+S1 trên 246 khung, so K_I/K_raw, F_I, tập ứng viên, tầng, khóa, nhóm hòa, N1/V0. Giữ riêng metadata ghép ca và đầu vào hàm phương pháp. Khi hash hoặc trường bắt buộc lệch, dừng phần phụ thuộc để xác định nguồn.
2. Pilot bốn cửa sổ từ nhóm có dấu vết gốc EC2. Chọn trước theo dataset, loại thật/giả, độ nặng, điểm chính xác và cấu trúc, chưa dùng nhãn hoặc điểm T9. So native và phát lại ngay trên EC2 để cô lập đường dùng lại. So cả π, khóa, nhóm hòa, nhóm đầu, vùng E7, trạng thái và đầu vào chịu ảnh hưởng. Dùng fixture E6b/E7 hiện có cho nhánh `NO_POSITIVE_MASS` và biên vùng. Dự phòng native của E6b dùng E6a không truyền S1. Đo phần dư `||F(π) − π||₁` bằng một bước cập nhật kiểm tra, phân biệt với sai số dừng nội bộ. Tận dụng bản ghi pilot hợp lệ trong lượt chính.
3. Mặc định chạy lượt phát lại chính trên EC2 cùng máy với pilot. Có thể chọn laptop nếu đo được lợi ích vận hành và đối chiếu cùng khung pilot giữa hai máy đạt về khóa/hòa, với đủ RAM. Chọn một máy trước khi nhìn kết quả T9. Ưu tiên một đợt, một tiến trình khi phát lại đủ nhanh, tối đa hai tiến trình trên EC2 nếu pilot cho thấy nhanh hơn. Khi phải chạy lại chuỗi nặng trên EC2 dùng tối đa hai tiến trình. Nếu phép phát lại lệch native, sửa phần chiếu nếu được phép hoặc tính lại đúng phạm vi thiếu sau khi kiểm quyền. Không lấy kết quả gần đúng để thay bản ghi gốc.
4. Tạo C-c và C-g bằng adapter trong kết quả task. Áp tiêu chí C-g suy biến đã ghi theo T-043 dòng 922. Sau khi đủ đầu vào hợp lệ và xử lý đúng mọi trạng thái, nếu không có ca nào C-g thực sự chạy với khối lượng dương và làm đổi thứ tự hoặc nhóm hòa so với SimpleRCA thì báo C-g suy biến cho phép phân xử xếp hạng trên tập này. Tách số ca `NO_EVIDENCE`, số ca dự phòng tổng bằng 0, số ca chạy và số ca đổi hạng/hòa, giữ mẫu số 52 và lưu đầu ra. So nhóm hòa theo tập thành viên có thứ tự giữa nhóm. Thiếu nguồn/lỗi adapter là tình trạng riêng cần xử lý. Tiêu chí dùng đầu ra trước ghép nhãn, không dùng RR/MRR để loại C-g.
5. Seal pha 1 trước ghép nhãn. Chấm bằng bộ chấm P3/M1, tính luật T9, độ nhạy δ=0,005 và 0,02, bootstrap 1000 theo ô với seed 20261102 và bỏ từng ô. Các lựa chọn độ bền này trình cùng SPEC. Tái dùng RR đã chấm, không chạy lại PageRank trong từng mẫu. Chỉ suy độ nhạy h=0,5/2 từ chênh N1 bằng 0 khi đã xác nhận bất biến và có mẫu số hợp lệ. Báo hành động theo luật tách với quan sát và giới hạn.
6. Phân tích ca theo bảng câu hỏi. T10 dùng hàm `src/m1_danh_gia/e7.py` sau ghép nhãn để tính kỳ vọng chứa root, độ rộng và vùng hợp. Báo hai cách E7 theo ca, tổng hợp theo dataset, ghi ca root ngoài U/ngoài đồ thị con khi liên quan. Đối chiếu trung gian, xếp hạng gốc và phiếu nguồn C-c/C-g. Đóng manifest, báo cáo, LOG và STATE trong phạm vi được duyệt.

## Đầu ra và phạm vi ghi

- SPEC và LOG ghi các lựa chọn đã duyệt về T-049, nền và P1. Quyền chạy T-050 chờ Minh cấp theo ngân sách ở mục Chi phí ước lượng.
- Sau duyệt triển khai, `results/T-050/` chứa script/kiểm, đầu vào rút gọn có nguồn, pilot, bản ghi pha 1, seal, chấm, luật, độ bền, phân tích cơ chế, vùng và đối chứng. Báo cáo dẫn đường dẫn và con trỏ JSON. Giữ mọi lượt kể cả hỏng.
- `LOG.md` của T-050 chỉ nối thêm. Cập nhật đúng dòng T-050 trong `docs/STATE.md` khi mở task hoặc bàn giao theo quyền được duyệt.
- Nghiệm thu T-049, nền và P1 có nguồn ở Q-239/Q-240, WHY-73/WHY-74 và hai LOG. Phần thực nghiệm dùng code dùng chung đã có. Nếu phát hiện lỗi phải sửa `src`, trình phạm vi và ảnh hưởng cụ thể.

## Tiêu chí xong

- Phép phát lại đạt đối chiếu hoặc có đầu ra native hợp lệ cho phần cần thay. Bản ghi T9 truy được nguồn và cùng miền giữa hai vế. Phép chấm đủ tập đã khai, báo đúng lỗi, thiếu bằng chứng và fallback.
- Bảng luật/độ bền tách quan sát, kết cục, hành động và lựa chọn chính thức. Có phân tích cơ chế với ca tăng/giảm và ca đối chiếu đúng, hoặc ghi phần chưa phân xử và bằng chứng thiếu. Kết luận về PageRank giới hạn theo thang, nền và cặp so hiện có.
- Hai cách E7 được mô tả ở P. C-c/C-g có kết quả hoặc tình trạng có căn cứ theo hợp đồng. Khi T9 đủ điều kiện chọn, đề xuất nền cho T-051. Khi kết cục còn yêu cầu Minh, ghi đúng nhánh OPEN.
- Hồ sơ đủ để Claude kiểm độc lập. Quyết định về T-051, nghiệm thu và G3 theo thẩm quyền tương ứng.

## Không làm

Phạm vi T9/T10 dùng dev chế độ (a). Kiểm T11/T12/KB và vùng cuối thuộc các task sau. Hiệu chuẩn verdict, chế độ (b), RE3-OB, test/G3, FlashTicket, hiệu quả độc lập, VC×E5 đầy đủ và phân xử tác dụng quan hệ cho cả chuỗi còn mở. T-050 cung cấp bằng chứng chọn bước xếp hạng và mô tả vùng trung gian cho các việc đó.

## Chi phí ước lượng

Đề xuất trước phản biện dự trù trung tâm 205 phút. Bổ sung 20–40 phút làm adapter P3 và kiểm ghép, thành **3 giờ 45 phút–4 giờ 05 phút** ở dự trù trung tâm và **2 giờ 50 phút–5 giờ 05 phút** theo khoảng kế hoạch, tính cả soạn SPEC, công cụ, pilot, chấm, phân tích và hồ sơ. Thời gian chờ Minh/Claude tính riêng. Đây là dự toán, chưa đo chạy E6b đủ tập.

Lượt phân tích chỉ đọc trước đó đã đọc/hash 82 bản ghi native khoảng 8,73 giây. Đọc/hash 246 khung và nén phép chiếu trong bộ nhớ mất 66,15 giây, RAM đỉnh khoảng 218 MiB. Phép chiếu nén khoảng 4,87 MB trước khi bổ sung đồ thị và metadata. Tham chiếu T-049 về đường chạy lại là ngoại suy 35–50 phút cho toàn bộ 82 cửa sổ trên EC2 hai tiến trình. Kiểm ngân sách tuần tự từng dataset theo Q-40 bằng pilot và số đo thực; ngoại suy chạy song song không thay phép kiểm đó.

Đề nghị trần 6 giờ thời gian thực của gói triển khai, tổng 2 giờ EC2 và tối đa 90 phút cho một lượt dài nếu phải dùng đường tính lại. Giữ instance hiện có. Đây là trần đề nghị chờ Minh duyệt theo AGENTS mục 3.8. Đo thời gian và bộ nhớ ngay từ pilot, cập nhật dự toán nếu phát sinh.

## Rủi ro và điều chưa chắc

- Đã xác nhận đủ trường đầu vào đã lưu. Tương đương E6b/E7 từ đường dùng lại còn chờ pilot. Số liệu RAM đọc khung chưa đo peak của toàn lượt phát lại.
- Điểm z có thể tập trung mạnh và làm đổi ý nghĩa thực tế của khối lượng PageRank so với thang E4 lúc thiết kế. T9 giữ trọng số hiện hành. Bất đồng về cơ chế phải phân xử bằng vết chuyển khối lượng/khóa trước khi quy nguyên nhân.
- Ở P, nguồn đã lưu có 3/52 ca thật và 2/30 cửa sổ giả có nút tầng 1 hòa K_I nhưng khác K_raw. Điều đó giới hạn cách gọi vế S0. Phản ví dụ và phép đếm chỉ đọc ghi trong LOG.
- Tiêu chí C-g suy biến xét khả năng phân xử thay đổi thứ hạng trên tập dev đã khai. Hiệu quả trên dữ liệu độc lập còn OPEN.

## Prompt bàn giao

Prompt soát bản SPEC nằm cuối LOG để Minh chọn chuyển Claude.
