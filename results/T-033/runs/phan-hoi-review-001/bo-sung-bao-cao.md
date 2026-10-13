# T-033 — Bổ sung sau phản biện, phiên 10

Ngày 11/10/2026. Codex là người làm; Claude là người phản biện. Minh duyệt thực hiện gói bổ sung trong chat. Bản này đi cùng `session9-report-002`, giữ bản cũ để bảo toàn lịch sử. Khi tổng hợp T-034/G2, dùng các câu thay ở mục 6 dưới đây, không lấy riêng câu cũ. Minh đã duyệt dừng phản biện và nghiệm thu T-033 sau hoàn tất mục1–3. Số đã khớp; bốn dòng DECISIONS đã được duyệt chữ và ghi (Q-137–Q-140). T-033 được nghiệm thu ngày11/10/2026 với các giới hạn OPEN ở mục8. Không đóng RQ2/G2 hoặc chọn thiết kế P6.

## 1. Kết quả dễ hiểu và phạm vi

Đã làm phần đối chiếu còn thiếu trên dữ liệu đã lưu. Python chạy trên EC2; không chạy lại detector, không mở dữ liệu khóa, không thêm điểm hoặc cửa sổ. Số và nguồn nằm trong `doi-chieu-review.json` (gọi tắt là D). Lệnh đầy đủ, thời gian, hash, ledger và lỗi của các lần thử nằm trong `manifest.json` (gọi tắt là M). Đường dẫn `runs/...` trong D là đường dẫn tương đối từ `/home/ubuntu/rca/T-033`; `source-catalog.json` của report002 ánh xạ sang bản local đã kiểm hash.

**Câu đã trả lời được:** một cờ BOCPD không nhất thiết cần metric ở giây đó thay đổi. Có 8 cặp điểm mà toàn bộ vector đầu vào hiện tại giống nhau, kể cả các giá trị raw tương ứng, nhưng điểm đối chứng không có cờ và điểm đang xét có cờ. Bốn cặp ở trước proxy và bốn ở sau proxy. Ở những cặp này, bước posterior → chọn run length MAP → luật `|Δm| > 1` đổi quyết định trong khi trạng thái tích lũy của mô hình khác nhau. Chưa tách ảnh hưởng riêng của prior, covariance và từng bước tích lũy. Nguồn: D#/step7/summary và các cặp ở mục 2.

Ví dụ dev-03: tại chỉ số 723 và 724, tất cả metric BOCPD đang đọc đều giống nhau. Ở 723 mô hình còn chọn đoạn dài 724 điểm. Đến 724 nó chọn đoạn dài 105 điểm và bật cờ. Giống người xem cùng một ảnh nhưng đưa ra nhận xét khác sau khi đã xem thêm cả chuỗi ảnh trước đó. Cờ chỉ nói mô hình đổi cách chia chuỗi; nó không tự nói hệ thống vừa hỏng ở giây 724. Nguồn: D#/R1/rows/0/first_post; cặp BOCPD post của dev-03 trong D#/step7/locked_pairs.

**Câu vẫn chưa trả lời chắc:** trước proxy có sự cố thật hay báo giả? Dữ liệu đã xem không có chuẩn độc lập xác nhận hệ thống khỏe ở các điểm đối chứng, thời điểm sự cố thật bắt đầu, hoặc kết quả lỗi của request tại các điểm này. Tải, duration và log có thể mô tả hiện tượng; chúng chưa đủ kết luận hệ thống thật sự khỏe hay hỏng. Không gán tất cả báo trước proxy là báo giả. Không lấy sự đồng ý giữa hai agent làm bằng chứng.

Phần làm thêm bao phủ 210 đơn vị, 968 điểm khóa và 64 nhóm đã chọn. Chỉ 177 cặp là cặp alarm/no-alarm đóng băng phục vụ phép so này, không gọi toàn bộ 487 điểm ca × chỉ số là 487 đối chứng. Có 57 cặp BOCPD hợp lệ và 112 cặp N-Sigma cùng cột hợp lệ; 8 cặp N-Sigma thiếu đối chứng. Nguồn: D#/step7/summary. Những nhóm trùng ca/điểm không phải các phép thử độc lập.

## 2. Quy tắc đọc và phần phân xử của bước 7

Quy tắc đã trình trước khi thực hiện: BOCPD đọc toàn bộ vector native, N-Sigma đọc mọi cột native kích hoạt tại điểm khóa. Nối thực thể theo đúng tiền tố tên cột với thực thể workload hiện có; không dùng root theo nhãn để chọn kênh, không đoán bí danh cho database. Đối chứng là điểm no-alarm, ca đối chứng và nhánh factorial đã khóa. Giữ nguyên điểm thiếu. Việc phân tích dùng proxy và nhóm hậu kiểm; đây không phải đầu vào của một detector mới. Nguồn: D#/reading_rule.

| Kết quả quan sát | Kết luận được phép |
|---|---|
| Toàn bộ X hiện tại bằng nhau, cờ khác, cấu hình giữ nguyên | Bác giả thuyết cần có thay đổi X hiện tại để có cờ trong cặp này; trạng thái mô hình phải được xét |
| Cùng x nhưng thống kê lịch sử/ngưỡng làm cờ khác | Xác nhận tác động gói thống kê lịch sử trong điều kiện so; không chứng minh nền sạch hoặc báo nào đúng |
| X và trạng thái cùng khác | Chưa cô lập tác động của từng phần |
| Trace/log/tải cùng thay đổi hoặc cùng giữ nguyên | Mô tả đồng xuất hiện; chưa xác nhận nguyên nhân vật lý |
| Đối chứng ở sau alarm, không có span hoặc không ánh xạ được thực thể | Khai hạn chế; không gọi là nền khỏe trước sự kiện |

Các phản ví dụ đầu vào BOCPD bằng nhau:

| Ca | Pha | Đối chứng → cờ (chỉ số) | m ở đối chứng → m ở cờ | Con trỏ |
|---|---|---|---|---|
| dev-03d4910932 | post | 723 → 724 | 724 → 105 | D#/step7/locked_pairs/1 |
| dev-1e6d61b5ec | pre | 118 → 119 | 119 → 111 | D#/step7/locked_pairs/30 |
| dev-1e6d61b5ec | post | 733 → 734 | 381 → 396 | D#/step7/locked_pairs/31 |
| dev-4e68956051 | pre | 674 → 675 | 675 → 179 | D#/step7/locked_pairs/59 |
| dev-59f696a169 | pre | 161 → 162 | 162 → 158 | D#/step7/locked_pairs/77 |
| dev-8017c6dc70 | post | 725 → 726 | 306 → 17 | D#/step7/locked_pairs/96 |
| dev-b8bd0abf60 | pre | 501 → 502 | 502 → 2 | D#/step7/locked_pairs/124 |
| dev-f9a8e05ed7 | post | 823 → 824 | 657 → 350 | D#/step7/locked_pairs/166 |

Đây là so cùng mẫu đầu vào hiện tại trong một cấu hình đã lưu, không giữ nguyên toàn bộ quá khứ hoặc can thiệp riêng từng tham số. Ở dev-03 post, MAP posterior đổi từ 0,977388 sang 0,544362; mass của nhánh thắng và normalizer cũng đổi. Hai giá trị posterior thuộc hai giả thuyết run length khác nhau, không là hai điểm bất thường để đem so độ lớn. Nguồn: cặp dev-03 post trong bảng trên.

**Đối chứng N-Sigma:** mọi cột kích hoạt và đối chứng cùng cột có giá trị x, n, mean, std, khoảng cách và ngưỡng lưu trong D#/step7/locked_pairs/*/same_column_values. Đã đối chiếu các giá trị với 120 bản ghi đối chứng gốc. Điểm no-alarm hợp lệ được kiểm bằng luật native, không chỉ tin nhãn mô tả. Có 48 đối chứng nằm sau alarm, 121 trước alarm và 8 thiếu đối chứng, tính chung hai detector. So với điểm sau alarm vẫn trả lời phép bất đẳng thức ở hai trạng thái, nhưng không chứng minh nền trước sự cố. Nguồn: D#/step7/summary; /control_direction_limit; mỗi cặp có /control_relative_position.

**Tải:** tái tính nhận xét của Claude: 4.027/4.968 ô hữu hạn bằng nhau trong 183 cặp cách 1 giây; 10.289/92.790 ô bằng nhau trong 3.399 cặp cách ít nhất 15 giây giữa những điểm đã khóa. Đây là tỷ lệ ô của các cặp, không số ca và không mẫu độc lập. Nhịp lấy mẫu hoặc cửa sổ rate là giải thích chưa kiểm; không kết luận từ tỷ lệ này rằng tải thực tế không đổi. Các cặp xa chỉ dùng kiểm nhận xét về độ lặp của số workload, không thêm đối chứng nguyên nhân hoặc thay điểm khóa. Nguồn: D#/step7/workload_equality.

**Trace:** đọc các thực thể ánh xạ được ở điểm đối chứng/cờ, ghi span count và duration mean raw. Không chuẩn hóa duration sang ms vì đơn vị chưa xác minh; không gọi thiếu span là service không hoạt động. Không có statusCode đủ để dựng chuẩn lỗi request. Với N-Sigma rộng, một số cột database/tài nguyên không có thực thể trace/workload tương ứng; giữ `unmapped_columns` thay vì mượn trace của service khác. Nguồn: D#/step7/units/*/points và /locked_pairs/*/context_comparison; /groups/*/observed_specific/unmapped_columns; `session9-report-002/nsigma-trung-gian/index.json`; thẻ ST2 trong `docs/knowledge/K2-du-lieu.md`.

**Log:** đã đọc lại mẫu first/last lưu ở các điểm khóa và đối chiếu digest. 915 message mẫu được kiểm, với 724 lần có từ INFO và không thấy token tên lớp Java Exception trong bộ mẫu ấy. Đây không là toàn bộ log, không là bộ phát hiện lỗi mới và không chứng minh không có lỗi. D#/step7/log_samples giữ nguồn và digest. Lệnh `read-log-program-metadata` trong M#/commands ghi metadata của 59 mẫu dạng thông điệp, ví dụ truy vấn order, lấy route/trip, số vé còn lại và tra station/train; 191 message không parse được logger bằng quy tắc trích này. Không đổi tên các dạng này thành trạng thái vận hành.

Ở dev-03 trước điểm N-Sigma security, mẫu TokenService có chữ `null`; chưa xác minh đây là lỗi xác thực hay request không mang token. Ở cặp BOCPD post dev-03 có log RouteController; chỉ biết đang có hoạt động ghi log về route, không biết toàn bộ request thành công. Mẫu SeatService có chữ `success` chỉ nói nhánh ghi message ấy; không là chuẩn sạch cho tất cả dịch vụ. Nguồn: M#/commands (name `read-log-program-metadata`, các dòng template 5, 36–40 trong stdout); D#/step7/log_samples; các source_pointer dẫn tới `tai-log.json#/log_excerpts/.../samples/...`.

Bước 7 đã được bổ sung đối chiếu đầy đủ trên điểm/nhóm hiện hữu và có những giả thuyết tính toán bị bác. Câu hỏi 4 về sự cố thật trước proxy vẫn OPEN. Không nhận là đã phân xử nguyên nhân riêng cho mọi thành viên của 64 nhóm. Đọc thêm cùng mẫu INFO hoặc đo lại cùng detector không tự tạo chuẩn vật lý còn thiếu.

### 2.1. Bối cảnh trên toàn bộ đầu vào BOCPD full — Codex tái tính trên EC2

Phần này bổ sung hai điểm Claude nêu ở lượt3, được nhắc lại trong lượt4. Số dưới là Codex tự tính từ X và CP_flags native đã lưu của toàn bộ30ca full. Không chạy detector hoặc phép thử tác động. D#/input_repetition_full; M#/commands (name `recompute-full-input-repetition`). Nguồn và chỉ số từng ca có ở D#/input_repetition_full/cases.

| Quan sát | Tử số / mẫu số | Tỷ lệ |
|---|---:|---:|
| CP ở giây toàn bộ X trùng giây trước | 74 / 437 điểm đổi | 16.9336% |
| Nền: giây toàn bộ X trùng giây trước | 6602 / 43200 giây có giây trước | 15.2824% |
| Ô X trùng giá trị ô cùng cột ở giây trước | 1086942 / 1290240 ô kề nhau theo thời gian | 84.2434% |

Mỗi ca bỏ chỉ số0 vì chưa có giây trước. Kiểm times cách đúng1giây; X hữu hạn; mọi cột native được tính; equality là bằng nhau chính xác, không tolerance. Cờ tại chỉ số0 là sentinel False đã kiểm; CP tính lại từ `abs(diff(m))>1` khớp CP_flags lưu. Mẫu số nền gồm cả giây có/không CP. Tỷ lệ ô gộp tử/mẫu số theo số chiều thực từng ca, không lấy trung bình tỷ lệ ca. Đây là BOCPD processed X thực sự vào engine, không workload và không gộp tỷ lệ với N-Sigma. Nguồn: D#/input_repetition_full/population, /input_semantics, /denominators, /summary.

Tám cặp ở bảng mục2 là tập điểm đọc khóa, không phải toàn bộ sự kiện X lặp có CP. Trên toàn full có 74 điểm loại đó, còn tỷ lệ nền là 15.28%. Số tái tính khớp74/437 và các tỷ lệ Claude công bố ở mức làm tròn tương ứng. Không suy chênh hai tỷ lệ là tác động có ý nghĩa thống kê hoặc detector thiên về đầu vào lặp. Những giây/ô liên tiếp phụ thuộc nhau, không là mẫu độc lập.

**Tác động của đầu vào dạng bậc thang lên detector: chưa kiểm.** Câu mở cho P6: mức lặp, độ phân giải thời gian hoặc cách ghi/tiền xử lý có ảnh hưởng tới cờ, thời điểm báo và độ tin cậy khi giữ các điều kiện khác không? Giả định tương tác với cập nhật lịch sử có thể sai nếu mức lặp chỉ phản ánh lấy mẫu/aggregation bình thường. Minh không duyệt phép kiểm tác động trong T033; không chạy can thiệp/resampling hoặc detector mới. Lựa chọn xử lý đầu vào cho P6 vẫn OPEN. Nguồn: D#/input_repetition_full/staircase_effect.

## 3. R1 — Phân biệt thời điểm cờ và đoạn được MAP chọn

Đã tính trên EC2 từ R đã lưu: `m[i] = argmax R[:, i+1]`; chỉ số bắt đầu đoạn suy ra là `i - m[i] + 1`. Đây là giả thuyết của mô hình trên dữ liệu đã tiền xử lý nhìn trước, không onset thật và không thay độ đo P3/WHY-35.

Có 30/30 ca có cờ sau proxy, offset 2–317 s. Cờ đầu sau proxy ở 13 ca trỏ tới đoạn bắt đầu sau proxy (+13 đến +54 s), còn 17 ca trỏ trước proxy (−630 đến −7 s). Trong 17 ca có 5 ca chỉ cách proxy 7–52 s; không gọi chúng không liên quan sự cố. Có 28 ca có một cờ sau proxy trỏ tới đoạn sau proxy, với thời điểm cờ 13–656 s. dev-143 và dev-f81 không có cờ loại đó trong bản ghi. Nguồn: D#/R1/first_post_MAP_start_relation; /cases_with_later_MAP_start_after_proxy; /summary_ranges; /rows.

Bảng dưới giữ độ lệch từng ca. Mọi cột là giây so proxy, trừ m. Dấu “—” là không có sự kiện trong bản ghi. Cột cuối là thời điểm cờ, không thời điểm bắt đầu đoạn. Nguồn từng hàng: D#/R1/rows/{hàng, bắt đầu 0}.

| Ca | Cờ đầu trước | Bắt đầu MAP tại cờ trước | m tại cờ trước | Cờ đầu sau | Bắt đầu MAP tại cờ sau | Cờ đầu sau trỏ đoạn sau proxy |
|---|---:|---:|---:|---:|---:|---:|
| dev-03d4910932 | -36 | -460 | 425 | 4 | -100 | 122 |
| dev-12a1a88069 | -592 | -658 | 67 | 62 | -561 | 122 |
| dev-14372e1209 | -468 | -688 | 221 | 98 | -566 | — |
| dev-16597725c1 | -481 | -711 | 231 | 2 | -7 | 38 |
| dev-16870e660c | -106 | -106 | 1 | 34 | 34 | 34 |
| dev-1e6d61b5ec | -601 | -711 | 111 | 14 | -381 | 114 |
| dev-20acb4402d | -440 | -440 | 1 | 6 | -203 | 172 |
| dev-260d332c8d | -594 | -712 | 119 | 196 | -222 | 289 |
| dev-3ae0a6c15a | -71 | -680 | 610 | 35 | 23 | 35 |
| dev-3defe3d34b | — | — | — | 28 | -384 | 84 |
| dev-4e68956051 | -45 | -223 | 179 | 23 | 23 | 23 |
| dev-4f8a844308 | -502 | -707 | 206 | 13 | 13 | 13 |
| dev-57546fd87b | -305 | -604 | 300 | 23 | -402 | 431 |
| dev-59f696a169 | -558 | -715 | 158 | 43 | -51 | 127 |
| dev-746fd74313 | -618 | -619 | 2 | 31 | 26 | 31 |
| dev-7f1b6b071d | -365 | -365 | 1 | 26 | 24 | 26 |
| dev-8017c6dc70 | -449 | -595 | 147 | 6 | -10 | 223 |
| dev-98bc73c499 | — | — | — | 41 | 27 | 41 |
| dev-a505ab3f65 | -336 | -707 | 372 | 39 | 39 | 39 |
| dev-a5cabe5fa7 | -249 | -677 | 429 | 93 | -52 | 217 |
| dev-a915aa2424 | -41 | -41 | 1 | 177 | -25 | 262 |
| dev-b8bd0abf60 | -218 | -219 | 2 | 18 | -219 | 135 |
| dev-ba831dbeb8 | -172 | -173 | 2 | 30 | 25 | 30 |
| dev-bcbd4f46ae | -515 | -684 | 170 | 39 | 39 | 39 |
| dev-db293894ab | -508 | -651 | 144 | 43 | -510 | 187 |
| dev-de89e2f9e9 | -255 | -255 | 1 | 54 | 54 | 54 |
| dev-f36d0647d5 | — | — | — | 32 | 26 | 32 |
| dev-f81f88234e | -541 | -698 | 158 | 317 | -630 | — |
| dev-f9a8e05ed7 | -603 | -714 | 112 | 104 | -245 | 656 |
| dev-fbc45b0c67 | -431 | -431 | 1 | 34 | 34 | 34 |

Ví dụ dev-f81: cờ ở +317 s đổi m từ 955 sang 948, dịch điểm bắt đầu giả thuyết từ chỉ số 82 sang 90. Đây là đổi cách hiểu đoạn cũ, chưa là bằng chứng phát hiện một đoạn mới sau proxy. dev-03 cờ ở +4 s trỏ về −100 s; cờ đầu trỏ tới đoạn sau proxy nằm ở +122 s. Nguồn: D#/R1/rows/27/first_post và /rows/0. Diễn giải “chưa phân xử” trước đây bỏ sót loại đổi giả thuyết đoạn cũ mà trung gian đã phân biệt được.

## 4. R2 — Hướng tác động của tiền xử lý

M_F/M_P là nguồn mask full/prefix; S_F/S_P là nguồn scale full/prefix. Gói mask đổi cả cột, số chiều và prior native, không là can thiệp prior riêng. Số dưới tính a − b. “Không định nghĩa” vì a không có CP đầu, không gán shift bằng 0.

| Contrast | CP đầu muộn hơn / bằng / sớm hơn / không định nghĩa | Số CP ít hơn / bằng / nhiều hơn |
|---|---|---|
| FF − FP; giữ M_F | 26 / 1 / 0 / 3 | 22 / 3 / 5 |
| PF − PP; giữ M_P | 29 / 1 / 0 / 0 | 22 / 4 / 4 |
| FF − PF; giữ S_F | 9 / 18 / 0 / 3 | 8 / 20 / 2 |
| FP − PP; giữ S_P | 11 / 19 / 0 / 0 | 12 / 18 / 0 |

Tổng CP tiền tố: FF 143, FP 273, PF 159, PP 338. Nguồn: D#/R2/summary; /rows/*/rows/*/signed_first_CP_shift và /signed_CP_count_difference; /prefix_CP_totals. Đổi nguồn từ prefix sang full không lần nào làm CP đầu sớm hơn trong các contrast có định nghĩa này. Không suy scaler online sẽ tốt hơn: PP vẫn nhìn trước trong tiền tố; CP nhiều hơn chưa là phát hiện đúng hơn.

Ba ca S của P3 không có CP trước proxy ở FF. FP/PF/PP lần lượt có 7/4/12 CP ở dev-3def, 6/5/11 ở dev-98b, 12/3/16 ở dev-f36. Đổi riêng một trong hai yếu tố sang nguồn prefix đã đủ tạo CP trước proxy ở cả ba ca này. Nhóm S theo cờ không bảo đảm hệ thống khỏe trước proxy hoặc phát hiện đúng onset. Nguồn: D#/R2/rows và `session9-report-002/phan-ra-tien-xu-ly.json#/cases/{9,17,26}/branches`.

## 5. R3 — Phép freeze N-Sigma có thông tin ở đâu

First-post native/fixed bằng nhau ở cả 60 đơn vị. Nhưng tại i_proxy, hai nhánh dùng cùng thống kê `[:720]`, đã kiểm mask NaN và giá trị hữu hạn bằng nhau. Bộ rộng báo ngay proxy ở 30 ca; bộ hẹp báo ngay proxy ở 11 ca. 41 đơn vị bằng nhau theo cấu tạo đối với thời điểm báo đầu. Chỉ 19 đơn vị hẹp có first-post ở sau proxy và cho phép so việc cập nhật thống kê giữa proxy và báo đầu. Ở 19 đơn vị này vẫn bằng nhau. Nguồn: D#/R3/rows; /first_time_informative_units; /first_time_structural_equal_units.

Không bác mọi tác động của lịch sử. Tập cờ toàn hậu proxy khác ở 30 ca hẹp và 18 ca rộng. Đây là kết quả tính toán về tập cờ; không có nhãn để nói frozen tốt hơn. Nguồn: D#/R3/full_flag_set_different_by_detector. Không gọi toàn bộ 41 đơn vị là vô thông tin: hạn chế chỉ áp dụng phép so thời điểm báo đầu.

## 6. Câu cũ → câu thay để dùng trong tổng hợp

Các câu dưới nằm trong `session9-report-002`; không sửa bản đó. “Thay” là cách dùng bản bổ sung khi tổng hợp, không thay số P3 hoặc sửa quyết định WHY.

| Nguồn / câu cũ nguyên văn | Câu thay hoặc giới hạn bổ sung |
|---|---|
| Báo cáo §4: “Scale có tác động trên cùng mask:” và “cả hai contrast scale khác m/CP ở 30/30 ca.” | Giữ quan sát khác m/CP, thêm bảng có dấu ở mục 4. Trong contrast có định nghĩa, nguồn full không làm CP đầu sớm hơn nguồn prefix. CP nhiều/ít không là đúng/sai vận hành. |
| Báo cáo §5: “Mọi full ca đều có báo sau proxy. N-Sigma hẹp có offset0–54 giây, rộng0; BOCPD2–317.” | Đây là độ lệch thời điểm cờ so proxy. BOCPD có 13/17 ca với bắt đầu MAP sau/trước proxy; bảng từng ca ở mục 3. Không dùng 30/30 hoặc 2–317 s làm bằng chứng khả năng phát hiện đoạn mới hoặc độ trễ thật. |
| Báo cáo §5: “Không đủ tách “tín hiệu sự cố xuất hiện muộn” với “mô hình phản ứng muộn” khi thiếu chuẩn onset độc lập.” | Onset thật vẫn thiếu chuẩn. Trung gian đã phân biệt cờ đổi giả thuyết đoạn cũ với cờ trỏ đoạn sau proxy; không gom tất cả cờ vào hai giải thích cũ. |
| Báo cáo §5: “First-post gộp fixed/native bằng nhau30/30 ở mỗi bộ cột.” | Giữ số; thời điểm báo đầu chỉ cho phép phân xử ở 19/60 đơn vị. 41/60 còn lại bằng nhau tại proxy theo cấu tạo. Tập cờ về sau vẫn có thông tin. |
| Báo cáo §7: “History mean/std ảnh hưởng cặp cùng x; scale ảnh hưởng likelihood/posterior trên cùng mask; mask/d/prior và tương tác có effect có điều kiện.” | Giữ các contrast có điều kiện, bổ sung 8 cặp toàn bộ X hiện tại bằng nhau nhưng m/cờ khác; không gọi đây là prior riêng hoặc nguyên nhân vật lý riêng của cả nhóm E/S. |
| kiem-tiep.md K2: “Freeze tại proxy không làm first-post sớm hơn ở tập hiện hữu, nhưng đổi tập cờ.” | Không thấy đổi first-post ở 19 đơn vị có cơ hội phân xử; 41 đơn vị bằng nhau theo cấu tạo ở proxy. Tập cờ khác ở 30 ca hẹp, 18 ca rộng. Chưa chọn causal baseline. |
| doc-tay-root-notes.md: “Nó bác cách diễn giải rằng cứ workload raw riêng route tăng mới có CP ở các cặp này.” | Rút căn cứ suy ra tải thực: workload raw riêng route giữ nguyên ở những cặp ấy, nhưng số workload lặp phổ biến ở giây liền kề. Cách chọn route của bản cũ không được dùng để đại diện toàn vector BOCPD. Phép bác giả thuyết cần X hiện tại đổi dựa vào toàn bộ X ở mục 2, không dựa vào workload route. |

Đối với R1–R3: đồng ý nội dung và đã viết bổ sung, chờ Claude kiểm bản thực tế. Với R4: đồng ý thiếu diễn giải bước 7 của bản cũ; phần đọc điểm/nhóm hiện hữu đã bổ sung ở mục 2 và 7, câu hỏi vật lý vẫn OPEN. Với R5: đúng về giới hạn workload lặp và lựa chọn route chưa được khai; không thấy nhãn vào engine và không kết luận động cơ lựa chọn cũ. Quy tắc mới xét toàn vector/cột kích hoạt và khai khả năng bác/hỗ trợ trước khi làm. Bất đồng còn cần kiểm là mức đủ của phần bổ sung, không tự nói reviewer đã đồng ý.

## 7. Diễn giải riêng từng nhóm đã khóa

Mỗi hàng chỉ diễn giải đại diện và đối chứng đã khóa của nhóm đó. Các con trỏ D dẫn đến điểm full/raw, trace, log, tải, các cột kích hoạt và điều kiện không khớp. Thiếu cùng ô, số chiều hoặc coverage giới hạn suy rộng qua hai ca. Không gọi ca đối chứng là ca vật lý khỏe chỉ vì no-alarm. B2/B4/N1/N2/N3 là mô tả hậu kiểm, không nguyên nhân độc lập; N4 xác nhận std=0 tại cột nhưng chưa xác nhận vì sao.

| Nhóm và ca đại diện / đối chứng | Quan sát và mức phân xử | Bằng chứng |
|---|---|---|
| 0: D0/bocpd<br>dev-14372e1209 / dev-4f8a844308 | Cả hai ca có X đổi tại cờ đầu trước proxy; coverage và chiều khác. So sánh này không cô lập nguyên nhân D0; D0 chỉ là chưa gán được mô tả sơ cấp. | D#/step7/groups/0; units 18,81; pairs 12,13,65,66 |
| 1: multi-label/bocpd/B2/10<br>dev-12a1a88069 / dev-7f1b6b071d | Ở dev-12, nhiều cột X và workload đổi tại cặp trước cờ; dev-7f1 cũng có biến động nhưng khác ô/coverage. Mã B2/10 không đủ quy nguồn trễ hoặc báo sớm. | D#/step7/groups/1; units 11,109; pairs 6,7,89,90 |
| 2: multi-label/bocpd/B2/2<br>dev-03d4910932 / dev-16870e660c | Dev-03 có cặp post toàn X bằng nhau nhưng cờ đổi; dev-168 cặp pre có X đổi. Phản ví dụ bác yêu cầu đổi X hiện tại, không biến toàn nhóm B2/2 thành cùng nguyên nhân. | D#/step7/groups/2; units 4,32; pairs 0,1,24,25 |
| 3: multi-label/bocpd/B2/5<br>dev-03d4910932 / dev-b8bd0abf60 | Dev-b8 có cặp pre toàn X bằng nhau nhưng m đổi sang 2; dev-03 cũng có phản ví dụ ở post. Dimension/coverage hai ca khác nên chưa so được mức tác động từng kênh. | D#/step7/groups/3; units 4,151; pairs 0,1,124,125 |
| 4: multi-label/bocpd/B4/w15/k2<br>dev-12a1a88069 / dev-f36d0647d5 | Đối chứng dev-f36 không có CP tiền tố FF nên mô tả B4 ở điểm CP tiền tố không hợp lệ. Thiếu phép so này không là bằng chứng phủ định cơ chế cho dev-12. | D#/step7/groups/4; units 11,186; pairs 6,7,154 |
| 5: multi-label/bocpd/B4/w15/k3<br>dev-12a1a88069 / dev-1e6d61b5ec | Dev-1e6 có phản ví dụ X bằng nhau cả pre và post, dev-12 không giữ X hiện tại. B4/w15/k3 không chỉ ra đâu là tín hiệu hệ thống thật. | D#/step7/groups/5; units 11,39; pairs 6,7,30,31 |
| 6: multi-label/bocpd/B4/w15/k5<br>dev-12a1a88069 / dev-1e6d61b5ec | Cùng đại diện/đối chứng với nhóm k3, nhưng nhãn B4 k5 là mô tả khác trên chuỗi đã có; không là lần chạy detector độc lập hoặc can thiệp đổi k BOCPD. | D#/step7/groups/6; units 11,39; pairs 6,7,30,31 |
| 7: multi-label/bocpd/B4/w30/k2<br>dev-12a1a88069 / dev-f36d0647d5 | Đối chứng dev-f36 vẫn thiếu điểm CP tiền tố để so B4/w30/k2. Cửa sổ mô tả không tự tạo điểm đối chứng hoặc nhãn nền khỏe. | D#/step7/groups/7; units 11,186; pairs 6,7,154 |
| 8: multi-label/bocpd/B4/w30/k3<br>dev-12a1a88069 / dev-7f1b6b071d | Đối chứng dev-7f1 có cặp pre X đổi; cả đầu vào và trạng thái khác. B4/w30/k3 không cô lập tác động riêng của biến động raw. | D#/step7/groups/8; units 11,109; pairs 6,7,89,90 |
| 9: multi-label/bocpd/B4/w30/k5<br>dev-12a1a88069 / dev-1e6d61b5ec | Đối chứng dev-1e6 có X lặp nhưng cờ đổi; cùng bằng chứng như w15, không tăng số phản ví dụ độc lập khi đổi nhãn cửa sổ B4. | D#/step7/groups/9; units 11,39; pairs 6,7,30,31 |
| 10: multi-label/bocpd/B4/w60/k2<br>dev-12a1a88069 / dev-f36d0647d5 | Dev-f36 thiếu mô tả hợp lệ tại CP tiền tố; không lấp khoảng trống w60/k2 bằng cách lấy cờ sau proxy làm cùng điều kiện. | D#/step7/groups/10; units 11,186; pairs 6,7,154 |
| 11: multi-label/bocpd/B4/w60/k3<br>dev-12a1a88069 / dev-f36d0647d5 | Với w60/k3 vẫn là dev-12 so dev-f36 không có pre-CP FF. Kết luận chỉ là chưa có đối chứng đáp ứng phép so đã khóa. | D#/step7/groups/11; units 11,186; pairs 6,7,154 |
| 12: multi-label/bocpd/B4/w60/k5<br>dev-12a1a88069 / dev-7f1b6b071d | Dev-7f1 pre có X đổi cùng cờ. Đổi nhãn w60/k5 không giữ trạng thái hoặc biến động để xác nhận riêng cơ chế B4. | D#/step7/groups/12; units 11,109; pairs 6,7,89,90 |
| 13: multi-label/nsigma/N1/1.5<br>dev-12a1a88069 / dev-a505ab3f65 | Cột kích hoạt pre của dev-12 là latency UI; dev-a505 là latency price. UI không có trace tại các điểm đang so, price có span; không mượn trace price để giải thích alarm UI. | D#/step7/groups/13; units 12,131; pairs 8,9,108,109 |
| 14: multi-label/nsigma/N1/2.0<br>dev-12a1a88069 / dev-1e6d61b5ec | Cột pre dev-12 khác auth latency của dev-1e6; chiều/coverage khác. N1 mô tả mật độ cờ ở đầu chuỗi, chưa xác nhận warmup là nguyên nhân riêng. | D#/step7/groups/14; units 12,40; pairs 8,9,32,33 |
| 15: multi-label/nsigma/N1/3.0<br>dev-14372e1209 / dev-16870e660c | Dev-143 pre kích hoạt preserve latency, không có trace ghép; dev-168 kích hoạt order latency có span. Tỷ lệ tail bằng 0 trong nhãn N1 không chứng minh lịch sử sạch hoặc nguyên nhân riêng. | D#/step7/groups/15; units 19,33; pairs 14,15,26,27 |
| 16: multi-label/nsigma/N2/10<br>dev-3ae0a6c15a / dev-98bc73c499 | Dev-3ae dùng đối chứng N-Sigma sau alarm, kích hoạt inside-payment/order-other; dev-98b có đối chứng trước alarm cho order-other. Không gọi đối chứng tương lai là nền trước sự kiện N2/10. | D#/step7/groups/16; units 61,124; pairs 50,51,102,103 |
| 17: multi-label/nsigma/N2/20<br>dev-746fd74313 / dev-57546fd87b | Dev-746 và dev-575 đều có đối chứng sau alarm tại cặp pre; các cột kích hoạt khác nhau. N2/20 đo mật độ báo, chưa cô lập tải hoặc phân phối. | D#/step7/groups/17; units 103,89; pairs 73,74,85,86 |
| 18: multi-label/nsigma/N2/5<br>dev-12a1a88069 / dev-8017c6dc70 | Dev-12 kích hoạt UI, dev-801 kích hoạt station; chỉ station có span tại điểm so. N2/5 không làm hai cột có điều kiện quan sát tương đương. | D#/step7/groups/18; units 12,117; pairs 8,9,97,98 |
| 19: multi-label/nsigma/N3/10<br>dev-03d4910932 / dev-f81f88234e | Dev-03 kích hoạt security latency, dev-f81 kích hoạt contacts latency; các cặp cùng cột có đối chứng trước alarm nhưng không có trace ghép đủ. Bất đẳng thức native được xác nhận, nguyên nhân vật lý chưa biết. | D#/step7/groups/19; units 5,194; pairs 2,3,161,162 |
| 20: multi-label/nsigma/N3/20<br>dev-03d4910932 / dev-f81f88234e | N3/20 dùng lại đại diện/đối chứng của N3/10; không có bằng chứng độc lập thêm chỉ vì đổi ngưỡng mô tả hậu kiểm. | D#/step7/groups/20; units 5,194; pairs 2,3,161,162 |
| 21: multi-label/nsigma/N3/5<br>dev-03d4910932 / dev-16870e660c | Dev-03 security không có trace ghép, dev-168 order có span. N3/5 không xác nhận báo trước proxy là false alarm và không cô lập lịch sử qua hai ca. | D#/step7/groups/21; units 5,33; pairs 2,3,26,27 |
| 22: multi-label/nsigma_doi_chung/N1/1.5<br>dev-12a1a88069 / dev-1e6d61b5ec | Bộ rộng dev-12 kích hoạt cả CPU, memory database và latency; dev-1e6 cũng có cột database không ánh xạ trace/load. Đối chứng pre nằm sau alarm; không dùng một latency service giải thích mọi cột OR. | D#/step7/groups/22; units 13,41; pairs 10,11,34,35 |
| 23: multi-label/nsigma_doi_chung/N1/2.0<br>dev-14372e1209 / dev-16870e660c | Dev-143 có memory và workload UI kích hoạt; một số cột database không có thực thể ghép. Dev-168 không khớp điều kiện mọi cột; N1/2 không cho chuẩn vận hành sạch. | D#/step7/groups/23; units 20,34; pairs 16,17,28,29 |
| 24: multi-label/nsigma_doi_chung/N2/10<br>dev-03d4910932 / dev-bcbd4f46ae | Dev-03 kích hoạt config/rebook CPU và cancel memory, cùng assurance latency; dev-bc kích hoạt tập khác. Có cột không ánh xạ; trace của assurance không phân xử CPU/database còn lại. | D#/step7/groups/24; units 6,167; pairs 4,5,140,141 |
| 25: multi-label/nsigma_doi_chung/N2/20<br>dev-12a1a88069 / dev-a505ab3f65 | Dev-12 so dev-a505 có đối chứng pre dev-a505 ở chỉ số 998, sau alarm 100. Điểm xa tương lai chỉ kiểm cờ/ngưỡng, không là nền cạnh sự kiện cho N2/20. | D#/step7/groups/25; units 13,132; pairs 10,11,110,111 |
| 26: multi-label/nsigma_doi_chung/N2/5<br>dev-03d4910932 / không có ca ngoài nhóm | Không có ca ngoài nhóm làm đối chứng. Các cặp cùng ca dev-03 vẫn kiểm được cột/ngưỡng; chưa có so qua ca để quy N2/5 hoặc chọn feature. | D#/step7/groups/26; units 6; pairs 4,5 |
| 27: multi-label/nsigma_doi_chung/N3/10<br>dev-bcbd4f46ae / dev-03d4910932 | Dev-bc so dev-03 có các cột database không ánh xạ. N3/10 rộng không thể được giải thích bằng trace service đã có mà bỏ các cột còn kích hoạt. | D#/step7/groups/27; units 167,6; pairs 4,5,140,141 |
| 28: multi-label/nsigma_doi_chung/N3/20<br>dev-03d4910932 / dev-b8bd0abf60 | Dev-b8 có nhiều cột CPU/memory database và đối chứng pre sau alarm. N3/20 không xác nhận hệ thống khỏe; thiếu thực thể ghép được ghi riêng thay vì gán collector lỗi. | D#/step7/groups/28; units 6,153; pairs 4,5,128,129 |
| 29: multi-label/nsigma_doi_chung/N4<br>dev-3defe3d34b / dev-16597725c1 | Dev-3def có cột ts-admin-route-service_socket với std=0 và vượt strict threshold; dev-165 không có điều kiện std=0 tương ứng. Xác nhận nhánh ngưỡng native ở đại diện; chưa biết std=0 là lượng hóa, thiếu đầu vào hay hành vi thật. | D#/step7/groups/29; units 69,27; pairs 22,23,57,58 |
| 30: native-status/bocpd/OK<br>dev-03d4910932 / không có ca ngoài nhóm | Native OK chỉ xác nhận kết quả tính hợp lệ. Dev-03 post có X bằng nhau và cờ khác; OK không chứng minh CP tương ứng một sự cố thật. | D#/step7/groups/30; units 4; pairs 0,1 |
| 31: native-status/nsigma/OK<br>dev-03d4910932 / không có ca ngoài nhóm | Native OK của N-Sigma hẹp giữ hành vi các cột security/route tại các pha đã khóa. Tính đúng bất đẳng thức không là chuẩn đúng/sai vận hành. | D#/step7/groups/31; units 5; pairs 2,3 |
| 32: native-status/nsigma_doi_chung/OK<br>dev-03d4910932 / không có ca ngoài nhóm | Native OK rộng của dev-03 chứa nhiều loại cột kích hoạt từ đầu warmup. Hợp lệ về tính toán không chứng minh nhiều báo là nhiều sự cố độc lập. | D#/step7/groups/32; units 6; pairs 4,5 |
| 33: proxy-first/bocpd/E-gần<br>dev-03d4910932 / dev-bcbd4f46ae | E-gần dev-03 so dev-bc: cả hai có cờ trước proxy nhưng đầu chuỗi/đầu vào khác. Nhãn E theo proxy không xác nhận operational false alarm. | D#/step7/groups/33; units 4,165; pairs 0,1,136,137 |
| 34: proxy-first/bocpd/E-xa<br>dev-12a1a88069 / dev-f36d0647d5 | E-xa dev-12 so dev-f36 không có pre-CP FF. Khác nhãn S/E và không khớp điều kiện CP khiến phép so nguyên nhân riêng còn thiếu. | D#/step7/groups/34; units 11,186; pairs 6,7,154 |
| 35: proxy-first/bocpd/S<br>dev-3defe3d34b / dev-59f696a169 | S dev-3def có cờ post trỏ đoạn bắt đầu trước proxy 384 giây; dev-59 cờ đầu post cũng trỏ trước proxy. S chỉ theo thời điểm cờ, không bảo đảm định vị đoạn mới sau proxy. | D#/step7/groups/35; units 67,95; pairs 54,77,78 |
| 36: proxy-first/nsigma/E-gần<br>dev-f81f88234e / dev-57546fd87b | N-Sigma E-gần dev-f81 kích hoạt contacts muộn hơn đầu chuỗi; dev-575 báo từ đầu với đối chứng sau alarm. Không giữ lịch sử/cột để gọi chung warmup hoặc tải là nguyên nhân. | D#/step7/groups/36; units 194,89; pairs 73,74,161,162 |
| 37: proxy-first/nsigma/E-xa<br>dev-03d4910932 / dev-f81f88234e | E-xa N-Sigma dev-03 so dev-f81 dùng cùng điểm như nhóm N3. Diễn giải theo proxy không bổ sung nhãn lỗi request cho các cặp đó. | D#/step7/groups/37; units 5,194; pairs 2,3,161,162 |
| 38: proxy-first/nsigma_doi_chung/E-xa<br>dev-03d4910932 / không có ca ngoài nhóm | E-xa bộ rộng dev-03 không có ca ngoài nhóm làm đối chứng; báo đầu từ chỉ số 100 và first-post tại proxy. Phép freeze first-time ở đây bằng nhau theo cấu tạo. | D#/step7/groups/38; units 6; pairs 4,5 |
| 39: unexplained-primary/bocpd<br>dev-14372e1209 / dev-4f8a844308 | D0/unexplained dev-143 so dev-4f8 lặp đại diện nhóm 0. Không gán cờ mô tả không có nghĩa không thể có cơ chế posterior; bước tính toán có thật, phần quy nguyên nhân còn thiếu. | D#/step7/groups/39; units 18,81; pairs 12,13,65,66 |
| 40: contrast/interaction/different<br>dev-16597725c1 / dev-59f696a169 | Dev-165 firstCP FF/FP/PF/PP là 239/177/230/170; tương tác first-time bằng 2. Dev-59 gói mask không đổi first-time. Có tác động kết hợp có điều kiện, không là prior riêng. | D#/step7/groups/40; units 21,22,23,24,91,92,93,94; pairs — |
| 41: contrast/interaction/no-difference<br>dev-03d4910932 / dev-16597725c1 | Dev-03 gói mask không đổi kết quả, nhưng scale đổi firstCP 684/235; dev-165 có tương tác first-time. Không gọi mọi ca khác input đều có tương tác hoặc mỗi nhánh đóng góp tuyến tính. | D#/step7/groups/41; units 0,1,2,3,21,22,23,24; pairs — |
| 42: contrast/mask_d_prior_with_S_F/different<br>dev-16597725c1 / dev-59f696a169 | Giữ S_F, dev-165 đổi mask làm firstCP 239→230, dev-59 không đổi. Gói cột/d/prior có effect phụ thuộc ca; không cô lập bỏ cột hoặc prior. | D#/step7/groups/42; units 21,22,23,24,91,92,93,94; pairs — |
| 43: contrast/mask_d_prior_with_S_F/no-difference<br>dev-03d4910932 / dev-16597725c1 | Giữ S_F, FF/PF dev-03 có input và output trùng, đối chứng dev-165 có shift. Kết quả bằng 0 hợp lệ, không là phép kiểm thất bại. | D#/step7/groups/43; units 0,1,2,3,21,22,23,24; pairs — |
| 44: contrast/mask_d_prior_with_S_P/different<br>dev-16597725c1 / dev-59f696a169 | Giữ S_P, dev-165 đổi mask làm firstCP 177→170, dev-59 không đổi. Effect gói khác điều kiện S_F; không cộng hai shift thành hiệu ứng prior. | D#/step7/groups/44; units 21,22,23,24,91,92,93,94; pairs — |
| 45: contrast/mask_d_prior_with_S_P/no-difference<br>dev-03d4910932 / dev-16597725c1 | Giữ S_P, FP/PP dev-03 trùng, dev-165 khác. Đây là đối chứng identity của gói mask trong một ca, không bác effect ở ca khác. | D#/step7/groups/45; units 0,1,2,3,21,22,23,24; pairs — |
| 46: contrast/scale_with_M_F/different<br>dev-03d4910932 / không có ca ngoài nhóm | Giữ M_F, dev-03 đổi nguồn scale làm firstCP 684→235. Cả lịch sử processed khác; không quy 449 chỉ số cho riêng một mẫu route tại điểm 235. | D#/step7/groups/46; units 0,1,2,3; pairs — |
| 47: contrast/scale_with_M_P/different<br>dev-03d4910932 / không có ca ngoài nhóm | Giữ M_P, dev-03 đổi scale cũng làm firstCP 684→235. Cùng số shift với M_F ở ca này không cho kết luận hai mask luôn tương đương. | D#/step7/groups/47; units 0,1,2,3; pairs — |
| 48: contrast/total_full_preprocessing_vs_prefix/different<br>dev-03d4910932 / không có ca ngoài nhóm | Dev-03 FF→PP tổng shift 449, trong khi mask identity trong ca này. Không dùng đường phân rã thuận lợi này gán tổng mọi ca cho scale. | D#/step7/groups/48; units 0,1,2,3; pairs — |
| 49: factorial/FF/CP-present<br>dev-03d4910932 / dev-f36d0647d5 | FF dev-03 có pre-CP, dev-f36 không có pre-CP. Nhánh không có CP vẫn là output hợp lệ; absence không tự là nền khỏe hoặc adapter lỗi. | D#/step7/groups/49; units 0,182; pairs — |
| 50: factorial/FF/no-CP<br>dev-3defe3d34b / dev-16597725c1 | FF dev-3def không CP trước proxy; FP/PF/PP có firstCP 277/421/246. Đổi riêng từng yếu tố đã tạo cờ trước proxy, không xác nhận cờ mới là đúng. | D#/step7/groups/50; units 63,21; pairs — |
| 51: factorial/FF/valid<br>dev-03d4910932 / không có ca ngoài nhóm | FF valid dev-03 giữ chuỗi đã lưu và có phản ví dụ X lặp ở post. Valid chỉ là trung gian tính hợp lệ, không bảo đảm định vị onset. | D#/step7/groups/51; units 0; pairs — |
| 52: factorial/FF/valid-collapse<br>dev-12a1a88069 / dev-16870e660c | FF valid-collapse dev-12 và dev-168 cùng có nhánh xử lý range0 hợp lệ nhưng firstCP khác. Không gán collapse là nguyên nhân riêng của mỗi cờ vì cùng có nhiều trạng thái khác. | D#/step7/groups/52; units 7,28; pairs — |
| 53: factorial/FP/CP-present<br>dev-03d4910932 / không có ca ngoài nhóm | FP dev-03 cờ đầu ở 235, điểm 234 không có cờ; khác scale so FF. CP-present không là nhãn sự cố hoặc đối chứng vận hành. | D#/step7/groups/53; units 1; pairs — |
| 54: factorial/FP/valid<br>dev-03d4910932 / không có ca ngoài nhóm | FP valid dùng cùng chuỗi nhóm CP-present, không tăng mẫu độc lập. Xác nhận điều kiện có thể tính contrast dù không có nhãn vận hành. | D#/step7/groups/54; units 1; pairs — |
| 55: factorial/FP/valid-collapse<br>dev-12a1a88069 / dev-16870e660c | FP valid-collapse dev-12 firstCP 116, dev-168 196. Range0 đi qua fill native; không chữa epsilon và không loại các contrast hợp lệ khỏi bảng. | D#/step7/groups/55; units 8,29; pairs — |
| 56: factorial/PF/CP-present<br>dev-03d4910932 / không có ca ngoài nhóm | PF dev-03 firstCP 684, điểm 683 không cờ. Gói mask trong ca này identity với FF, không chứng minh mask không ảnh hưởng các ca còn lại. | D#/step7/groups/56; units 2; pairs — |
| 57: factorial/PF/valid<br>dev-03d4910932 / không có ca ngoài nhóm | PF valid lặp cùng chuỗi PF, kiểm được cờ/đầu vào; trạng thái valid không giải quyết onset và thiếu trace của cột khác. | D#/step7/groups/57; units 2; pairs — |
| 58: factorial/PF/valid-collapse<br>dev-12a1a88069 / dev-16870e660c | PF valid-collapse dev-12 firstCP 128, dev-168 614. Cùng nhãn collapse không giữ nguyên các giá trị còn lại hoặc posterior để quy nguyên nhân chung. | D#/step7/groups/58; units 9,30; pairs — |
| 59: factorial/PP/CP-present<br>dev-03d4910932 / không có ca ngoài nhóm | PP dev-03 firstCP 235, điểm 234 không cờ. Prefix scaler vẫn nhìn trước trong prefix, không gọi PP là baseline online. | D#/step7/groups/59; units 3; pairs — |
| 60: factorial/PP/valid<br>dev-03d4910932 / không có ca ngoài nhóm | PP valid giữ output prefix hợp lệ; không dùng validation tính toán làm bằng chứng PP có ít false alarm hơn FF. | D#/step7/groups/60; units 3; pairs — |
| 61: factorial/PP/valid-collapse<br>dev-12a1a88069 / dev-16870e660c | PP valid-collapse dev-12 firstCP 116, dev-168 196. So FF/PF cùng ca cho thấy nguồn scale làm shift trong điều kiện ấy, chưa cô lập riêng đường range0. | D#/step7/groups/61; units 10,31; pairs — |
| 62: input-identical/FF_vs_PF<br>dev-03d4910932 / dev-16597725c1 | FF/PF dev-03 trùng toàn input/output trong phần đã so, dev-165 đổi firstCP. Identity đúng có điều kiện; không loại gói mask khỏi nguyên nhân ở toàn tập. | D#/step7/groups/62; units 0,1,2,3,21,22,23,24; pairs — |
| 63: input-identical/FP_vs_PP<br>dev-03d4910932 / dev-16597725c1 | FP/PP dev-03 trùng toàn input/output, dev-165 đổi firstCP. Giữ các contrast 0 trong tổng hợp; không chọn chỉ những ca có effect. | D#/step7/groups/63; units 0,1,2,3,21,22,23,24; pairs — |

## 8. Phần đã làm, phần thiếu và quyết định phụ thuộc

| Loại | Đã xác nhận trong điều kiện đã so | Giới hạn / bước phụ thuộc |
|---|---|---|
| Giao thức | Thời điểm cờ khác vị trí đoạn MAP; có cờ chuyển giữa giả thuyết về đoạn trước proxy | Không thay WHY-35 hoặc chấm lại P3; dùng bảng mục 3 để giới hạn giải thích G2 |
| Cách tính BOCPD | Toàn bộ mẫu X hiện tại bằng nhau vẫn có thể đổi posterior/MAP/cờ khi trạng thái tích lũy khác | Không tách prior/covariance; không quy mọi E/S cùng nguyên nhân |
| Cách tính N-Sigma | Có cột/ngưỡng kích hoạt được kiểm; std=0 ở đại diện N4; first-time freeze có mẫu số 19/60 | Không xác nhận nền khỏe, lượng hóa là nguyên nhân, hoặc frozen tốt hơn |
| Tiền xử lý | Signed contrast scale và gói mask/d/prior có hướng, identity và tương tác có điều kiện | Prefix còn nhìn trước; chưa chọn preprocessing causal/scaler/prior cho P6 |
| Thiếu quan sát/metadata | Ở điểm/cột đã so: thiếu trace/status hoặc thiếu ánh xạ database; đơn vị và completeness chưa đủ dùng làm chuẩn onset | Không gán lỗi collector hoặc cả dataset; collector tương lai không sửa được dữ liệu chưa ghi |
| Adapter/cài đặt | Các phép đối chiếu hiện hữu chưa cho bằng chứng lỗi adapter mới | Chưa kiểm trong lượt này không được chuyển thành đã xác nhận toàn bộ cài đặt |

DT18 và hướng dẫn cô yêu cầu nghiên cứu sâu, chỉ ra hạn chế rồi xây dựng phương pháp có vai trò đồ thị. Kết quả này bổ sung hạn chế về cách diễn giải cờ; cờ gộp OR phải đi cùng danh sách cột kích hoạt để đọc được nguồn báo; nó không xác nhận lợi ích của cạnh hoặc thiết kế bất thường tự sinh/kế thừa. Có thể đề xuất ứng viên giữ cột kích hoạt, lịch sử/ngưỡng và giả thuyết đoạn, hoặc quan sát theo quan hệ gọi; chưa đủ chọn ứng viên vì chưa có phép tính dùng cạnh, đối chứng và kiểm dev của thiết kế ấy. Không lấy yêu cầu đồ thị của DT18 làm bằng chứng rằng đồ thị chữa được cờ trước proxy. Nguồn: docs/MRP.md §3/P4/G2; DT18; advisor-2026-09-23.md; D#/reading_rule.

**Quyết định của Minh ngày11/10/2026:** chấp nhận dừng câu hỏi4 của SPEC, ghi OPEN do giới hạn dữ liệu: RE2-TT không có nền sạch và không có thời điểm lỗi có tác động được xác nhận độc lập. Không chạy so theo cửa sổ trong T033. Đây là chấp nhận giới hạn, không xác nhận hệ thống khỏe/hỏng trước proxy và không đóng RQ2/G2. Nguồn: lời duyệt năm mục của Minh; D#/closure_instruction/question4. Quyết định đã ghi tại DECISIONS Q-140 sau Minh duyệt chữ.

### Kiểm tiếp K1 — Chuẩn nền sạch và thời điểm lỗi có tác động

Chuyển nhu cầu còn thiếu thành yêu cầu quan sát cho FlashTicket: ghi run không tiêm với kết quả request/giao dịch đủ kiểm lỗi nền; ghi riêng thời điểm bật fault và thời điểm lỗi bắt đầu có tác động, có bằng chứng độc lập với detector; nối request/outcome với service/trace và đồng hồ. Ghi workload generator timestamp/rate, clock offset và sampling/drop counters để đánh giá độ phủ/alignment. Không lấy thời điểm detector vượt ngưỡng làm onset, không gọi run không tiêm tự động sạch. Đây là yêu cầu quan sát, chưa cài hay xác nhận runtime của FlashTicket. Nguồn: D#/kiem_tiep_bo_sung/K1; bản K1 gốc giữ nguyên ở session9-report-002/kiem-tiep.md.

### Kiểm tiếp K1/K5 — So theo cửa sổ trên mảng đã lưu

**Có thể làm, chưa chạy và không chạy trong T033.** Các mảng workload_raw, trace_grid_span_count, trace_group_duration_* và log_grid_row_count hiện hữu cho30ca có thể dùng để mô tả thay đổi tải, số span/log và duration qua đoạn thời gian quanh các điểm đã khóa. Đã kiểm danh mục/schema, không gọi đó là đã tính kết quả cửa sổ. Phép này có thể cho biết biến động quan sát có kéo dài hoặc đồng xuất hiện theo đoạn thời gian; không tạo nền sạch, onset hoặc kết quả lỗi request độc lập, không tự xác nhận sự cố hay nguyên nhân. Khi được duyệt ở gói khác, phải khai trước cửa sổ, thực thể/đối chứng, aggregation/missing và khả năng hỗ trợ/bác bỏ. Nguồn: D#/kiem_tiep_bo_sung/K1/window_option, /K5; source-catalog report002 ánh xạ runs/channel-pilot-001 và runs/channel-rest-001.

Không lấy trung bình các mean/median theo giây làm duration toàn cửa sổ một cách mặc định; cần count/semantics hoặc raw spans phù hợp. Tổng distinct trace từng giây không tự là distinct của cả cửa sổ. Số log không là số lỗi. Đơn vị và độ phủ vẫn cần xác minh; thiếu span không xác nhận không có request. Không sửa kiem-tiep.md của report002: các đoạn này bổ sung K1/K5 và ghi đúng quyết định mới để T034 dùng cùng bản hiện hành.

Còn OPEN: câu hỏi4, onset thật, báo giả vận hành, ảnh hưởng riêng của prior, tác động đầu vào bậc thang, lợi ích đồ thị và D. T033 không chạy thêm cửa sổ, prior, D hoặc phép thử bậc thang. Các quan sát tính toán đã xác nhận vẫn dùng được trong giới hạn đã khai; không dùng chúng chọn thành phần P6.

## 9. Tự kiểm và bàn giao

Hash nguồn được kiểm trước dùng: gói report002 29/29; nguồn bổ sung 12/12; source-catalog 1.186/1.186. EC2 kiểm 190/190 nguồn trực tiếp và kiểm lại sau tính. Các so R/m/cờ từ NPZ, đối chứng cùng cột, hướng/mẫu số và giữ raw input đã thực hiện bằng Python qua stdin trên EC2. Source không đổi. D#/source_verification; /source_unchanged_at_end; M#/source_verification; /commands.

Hai lần đầu của lệnh đối chiếu gặp khác biệt schema (log placeholder không có index; None trong mảng JSON). Chưa tạo output ở hai lần ấy. Lần sau đã xử lý đúng missing schema và tái kiểm. Một phiên bản JSON dùng tên trường “before” cho đối chứng sau alarm được sửa thành “control” và thêm hướng thời gian; bản trước giữ nén trong M#/output_history. Không thay detector, thống kê hoặc điểm khóa để có kết quả thuận lợi. Lỗi và thời gian đều giữ trong M#/commands.

Ba file kết quả hiện hữu được cập nhật, bản trước giữ trong lịch sử manifest; LOG nối thêm và chỉ dòng T-033 STATE được cập nhật. Không sửa báo cáo cũ, code, SPEC hoặc WHY. DECISIONS đã nối đúng bốn dòng Q-137–Q-140 sau Minh duyệt chữ; không thay các dòng cũ. Không commit/push hoặc tự gửi Claude. Manifest chứa ledger cập nhật với thời gian từng lệnh EC2; ngân sách lịch sử chưa đo đủ vẫn OPEN, không gọi ledger cũ là thời gian thực tế chính xác.

Theo lời duyệt mới, **dừng phản biện và nghiệm thu T-033 ngày11/10/2026**: các số Codex tái tính khớp Claude và mục1–3 đã hoàn tất, gồm ghi đúng Q-137–Q-140 sau Minh duyệt chữ. Đã xác nhận chuỗi tính toán N-Sigma/BOCPD, hướng tác động tiền xử lý nhìn trước, thời điểm cờ khác bắt đầu đoạn MAP và mẫu số freeze19/60. Câu hỏi4, onset thật, báo giả vận hành, prior riêng, tác động đầu vào bậc thang, lợi ích đồ thị và D vẫn OPEN; không chạy thêm cửa sổ hay phép kiểm tác động trong T033. T034 dùng các câu thay mục6, không lấy câu cũ report002. Nghiệm thu T033 không đóng RQ2/G2 và không chọn thành phần P6.
