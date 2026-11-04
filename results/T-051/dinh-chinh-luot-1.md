# T-051 — Đính chính sau phản biện lượt 1

Minh duyệt gói sửa ngày 04/11/2026 sau phản biện lượt 1 của Claude và bản đáp của Codex. Codex giữ vai người làm. Bản này bổ sung phạm vi kết luận và hồ sơ còn thiếu của báo cáo T-051. Dữ liệu dùng vẫn là dev chế độ (a), 52 ca thật và 30 cửa sổ giả RE2-TT qua ba thế giới. Báo cáo, manifest và seal gốc giữ làm lịch sử. Nguồn kết quả được kiểm SHA-256 theo manifest gốc trước khi tính các bảng dưới.

## 1. Mức hoàn thành và phần thiếu về thời gian

Khi gửi báo cáo Phiên 1, người làm đã có kết quả T11, T12, KB và các vết theo ca. Tuy nhiên hồ sơ chưa đáp ứng trọn các yêu cầu báo cáo trong SPEC, gồm phạm vi loại cạnh, độ nhạy KB, khả năng kích hoạt của pilot và phép đo chi phí tách theo công đoạn. Vì vậy câu “hoàn tất triển khai” trong LOG Phiên 1 đã báo mức hoàn thành quá sớm.

Khoảng 20 phút từ pilot đầu tới manifest lấy từ mốc file. Khoảng này gồm thao tác, viết hồ sơ và chờ công cụ của agent. Từ mốc file không xác định được mất bao lâu để đọc/hash, giải nén hay xử lý kết quả của lượt cũ.

Các bảng khoa học dưới đây được bổ sung từ kết quả đã ghim. Hồ sơ chi phí gồm số đã có trong log cũ và phép đo bổ sung trên đúng đầu vào, đúng phép tính, đối chiếu với đầu ra gốc. Phân rã thời gian của lượt cũ chưa lưu thì không thể khôi phục. Phép đo mới ghi thời điểm và điều kiện chạy của chính nó.

## 2. Phản hồi từng điểm

| Điểm Claude | Người làm kết luận | Xử lý trong bản này | Minh quyết |
|---|---|---|---|
| 1. Phạm vi cạnh tĩnh | Đúng về phạm vi kết luận. C-d3 có thể duyệt cạnh ngoài U rồi loại đường đó, nên diễn đạt chính xác là cạnh ấy không đóng góp vào điểm, hạng hay vùng. | Bảng loại cạnh, số thêm/trùng, đầu mút ngoài U, nhóm vòng và hệ quả DT18 ở §3. | Duyệt sửa |
| 2. Kết cục gộp chưa nêu chỗ không phân xử | Đúng. E9 ở Nezha-OB chưa đi tới phép xét thời gian. Mask E2 không làm mất cơ hội phủ quyết trên các kênh đã quan sát. | Số theo dataset và cửa sổ, kiểm mask và giới hạn N1 ở §4. | Duyệt sửa |
| 3. KB thiếu bảng độ nhạy | Đúng. Kết cục tái lập trên cùng dev không tạo thêm bằng chứng độc lập. | Bảng đầy đủ về chênh MRR, ô, kiểm dấu, bootstrap, h và δ ở §5. | Duyệt sửa |
| 4. Pilot không chạm nhánh đổi F_I | Đúng. Ba cửa sổ ban đầu chưa có phủ quyết hoặc thay đổi F_I do cạnh tĩnh. | Ghi giới hạn pilot và kiểm bổ sung của Claude ở §6 theo phương án đã trình. | Duyệt sửa |
| 5. Chưa nêu kết quả C-d2 | Đúng về số và phạm vi. δ của T11/T12 không là phép kiểm tương đương cho C-d2. | Bảng C-d2 và nghĩa vụ bàn giao RQ3d ở §7. | Duyệt sửa |
| Nguồn Q-241 | Bản ghi cũ tóm tắt đúng nhưng thiếu trích dẫn trực tiếp. | Nối nguyên văn các đoạn cấp quyền và lời “duyệt sửa” vào DECISIONS. | Duyệt sửa |

## 3. T12 đã kiểm được loại cạnh nào

Hai đồ thị nguồn có các loại cạnh sau. Trong phép tính hiện hành, E5 và E7 làm việc trên đồ thị con gồm các thực thể có kênh thô mang cờ. C-d1 cũng chỉ dùng quan hệ giữa các thực thể có cờ để phân nhóm. Các kênh có cờ đã kiểm đều thuộc U.

| Dataset | Tổng cạnh tĩnh | Loại trong nguồn | Cả hai đầu thuộc U | Cạnh thêm / cạnh trùng | Số thực thể đầu mút ngoài U |
|---|---:|---|---:|---|---:|
| RE2-TT | 170 | 132 gọi đồng bộ, 30 dữ liệu, 6 thông điệp, 2 gọi chưa phân kiểu | 88, đều gọi đồng bộ | 48 cửa sổ có 126/44, 11 có 155/15, 1 có 154/16 | 43 |
| Nezha-OB | 22 | 18 gọi đồng bộ, 4 dữ liệu | 14, đều gọi đồng bộ | 22 cửa sổ có 9/13 | 9 |

RE2-TT có 48 cửa sổ ở nhóm 126/44, gồm 24 thật và 24 giả. Nhóm 155/15 gồm 6 thật và 5 giả. Nhóm 154/16 là một cửa sổ giả. Cạnh thêm được lấy bằng phép hiệu cặp có hướng giữa toàn bộ cạnh tĩnh và cạnh quan sát của cửa sổ. Cạnh trùng là phép giao. “Ngoài U” đếm thực thể phân biệt.

Trong 52 ca thật tại P, cạnh thêm xuất hiện 54 lần trên các đường giải thích của kênh đổi F_I, gồm 50 lần RE2-TT và 4 lần Nezha-OB. Có 32 cặp phân biệt (cửa sổ, cạnh), gồm 30 và 2 tương ứng. Tất cả là gọi đồng bộ. Nhóm vòng không đổi ở cả 82 cửa sổ và ba thế giới. Trên Nezha-OB, cạnh thêm duy nhất có cả hai đầu trong U là checkoutservice → currencyservice. F_I đổi ở cửa sổ 61 và 71.

Loại quan hệ và nguồn gốc vẫn có trong hai mô hình tĩnh đã ghim. Công cụ T12 dùng cặp hướng cho phép tính và không giữ loại trong bản ghi chiếu. Khi diễn giải phải nối lại bằng (source, target) với đúng file nguồn. Theo D8 của T-043, phép tính hiện hành cũng không phân biệt trọng số theo loại cạnh.

Cạnh dữ liệu, thông điệp và gọi chưa phân kiểu của hai nguồn đều có đầu mút ngoài U. Trong điều kiện dev này, chúng không đóng góp vào E5, E7, điểm hay thứ hạng của các đối chứng đã chạy. C-d3 dựng đồ thị đầy đủ và có thể đi qua cạnh ngoài U lúc liệt kê đường, rồi chỉ tính điểm khi mọi nút trên đường có cờ. Vì vậy không nói các cạnh đó hoàn toàn không được duyệt trong mã.

Kết cục T12 chỉ hỗ trợ giữ cạnh quan sát cho nền dev đã thử. Tác dụng chẩn đoán của cạnh thông điệp và dữ liệu còn chưa phân xử. DT18-NV2 và WHY-53 vẫn giữ yêu cầu mô hình và quan sát các quan hệ này. Bước FlashTicket cần dữ liệu quan sát có ánh xạ thực thể ở hai đầu quan hệ, bằng chứng trên thực thể và revision phù hợp để đánh giá phép tính. Việc thu được dữ liệu đó chưa tự xác nhận quy tắc kế thừa hiện hành đúng cho từng loại quan hệ.

Nguồn gồm `results/T-038/do-thi/thuc-the.json#/edges`, `results/T-039/do-thi/thuc-the.json#/edges`, `t12-001/score/mechanisms.json#/*/static`, từng cửa sổ `t12-001/{index}.json#/worlds/{world}/effect`, và `src/m1/{e5,e7,doi_chung}.py`. Tên JSON trong bản này tính tương đối từ results/T-051.

## 4. T11 và T12 tách theo miền có thể phân xử

### T11 tại P

| Dataset / cửa sổ | Số cửa sổ | Kênh không có đề xuất kế thừa | Kênh bị mask E2 | Thiếu khởi phát sau mask | Xét, không phủ quyết | Phủ quyết | Cửa sổ có phủ quyết |
|---|---:|---:|---:|---:|---:|---:|---:|
| RE2-TT thật | 30 | 1.263 | 182 | 14 | 186 | 11 | 5 |
| RE2-TT giả | 30 | 510 | 1 | 4 | 69 | 7 | 6 |
| Nezha-OB thật | 22 | 111 | 15 | 58 | 0 | 0 | 0 |

Đếm theo mã kênh ở mỗi cửa sổ. Cột thiếu khởi phát chỉ gồm các kênh đi qua kiểm mask E2 vì mã xét mask trước. Cả 15 kênh bị mask trên Nezha-OB cũng thiếu khởi phát, nên đủ 73 kênh có đề xuất đều chưa đưa tới phép phân xử thời gian. ΔMRR bằng 0 trên Nezha-OB mô tả nhánh E9 không phát huy được cơ chế trong dữ liệu này.

Trong 182 kênh bị mask ở cửa sổ thật RE2-TT, 131 không đạt bất đẳng thức thời gian và 51 thiếu khởi phát. Kênh duy nhất bị mask ở cửa sổ giả RE2-TT cũng không đạt thứ tự thời gian. Kiểm trên trung gian đã ghim cho thấy không kênh nào trong các nhóm bị mask sẽ được phủ quyết nếu chỉ bỏ kiểm mask. Đây là tính lại điều kiện để phân tích trạng thái, không phải kết quả của một cấu hình E9 mới.

Chỉ cửa sổ 55 trong 5 cửa sổ thật có phủ quyết chạm kênh của root và đổi RR. Bốn cửa sổ còn lại có phủ quyết trên ứng viên khác nhưng RR root giữ nguyên. Phủ quyết ở 6/30 cửa sổ giả với 7 kênh cho thấy trạng thái phủ quyết tự nó chưa đặc hiệu cho cửa sổ có lỗi. Phép T11 kiểm dạng phủ quyết đã đặc tả. Giá trị của thông tin khởi phát trong các cách dùng khác còn cần bằng chứng riêng.

Nguồn `t11-001/score/mechanisms.json#/*/worlds/P/{states,no_proposal}` và `t11-001/{index}.json#/worlds/P/{onset,flagged,effect/1/inherited_by}`. Các cửa sổ giả phủ quyết là 08, 40, 44, 46, 48, 58. Cửa sổ thật phủ quyết là 15, 17, 37, 55, 59.

### T12 và vế mốc giả

T12 có 19 ca thật đổi F_I tại P, gồm 17 RE2-TT và 2 Nezha-OB. Mọi kênh đổi F_I ở cả cửa sổ thật và giả đều đi từ 1 về 0. Trong 30 cửa sổ giả, N1 giữ nguyên ở 18 và giảm ở 12. ΔN1 bằng −7/10.

Vế HẠI của C-e chỉ xét mức tăng N1. Do đó nó không đánh giá được tác hại của việc loại bằng chứng tự sinh trong các thay đổi chỉ làm N1 giảm. Kết cục KHÔNG TÁC DỤNG của T12 đến từ các vế luật trên đầu ra xếp hạng cùng vế C-e có giới hạn đã nêu. C-e không xác nhận việc giảm N1 là đúng.

Nguồn `t12-001/score/mechanisms.json#/*/worlds/P/{changes_F_I,delta}`, `t12-001/score/law.json#/theo_the_gioi/P/moc_gia`, WHY-70 và `src/m1/e5.py`.

## 5. Độ nhạy KB trên cùng dev

Bốn cặp vẫn cho kết cục như T-053. Các trường luật khớp bản /cap tương ứng ở cả ba thế giới. Bảng dưới lấy tại P, các thế giới cho cùng giá trị ở những trường đã nêu.

| Thành phần | Kết cục | ΔMRR gộp | RE2-TT / Nezha-OB | Ô tăng / giảm trong E_X | p kiểm dấu |
|---|---|---|---|---|---|
| E1 | GIÚP | 163/4056 | 163/2340 / 0 | 5 / 2 | 29/64 |
| E2 | TRÁI CHIỀU dataset | 865633/20638800 | −7/180 / 1328683/8731800 | 4 / 0 | 1/8 |
| E3(a) | HẠI | −1/60 | 0 / −13/330 | 0 / 1 | 1 |
| E5 | GIÚP | 29/1560 | −1/60 / 1/15 | 2 / 1 | 1 |

| Thành phần | Khoảng bootstrap 95% của ΔMRR gộp | GIÚP | HẠI | KHÔNG TÁC DỤNG | TRÁI CHIỀU dataset | TRÁI CHIỀU ô |
|---|---|---:|---:|---:|---:|---:|
| E1 | [−0,02921 đến 0,12421] | 654 | 87 | 125 | 110 | 24 |
| E2 | [−0,02580 đến 0,11278] | 413 | 45 | 56 | 486 | 0 |
| E3(a) | [−0,05527 đến 0,00283] | 0 | 1.000 | 0 | 0 | 0 |
| E5 | [−0,01887 đến 0,05755] | 644 | 39 | 270 | 39 | 8 |

Cả bốn khoảng ΔMRR chứa 0. E5 đổi từ GIÚP sang KHÔNG TÁC DỤNG khi δ = 0,02. δ = 0,005 giữ kết cục chính của cả bốn cặp. Đổi h sang 0,5 hoặc 2 cũng giữ kết cục chính. Kết cục HẠI của E3(a) trong mọi mẫu là kết cục của luật tổng hợp có UV-6 và vế N1, nên không dùng tỷ lệ đó như khẳng định riêng về dấu ΔMRR.

| Cặp | C-e hợp lệ | Bị loại | ΔN1 tại P | V0 mỗi vế |
|---|---:|---:|---|---|
| E1 | 30 | 0 | 13/30 | CAUSE_FOUND 30/30 |
| E2 | 30 | 0 | 1/15 | CAUSE_FOUND 30/30 |
| E3(a) | 30 | 0 | 88/15 | CAUSE_FOUND 30/30 |
| E5 | 30 | 0 | −29/15 | CAUSE_FOUND 30/30 |

E3(a) kích hoạt cả UV-6 và vế N1. Việc tái sử dụng được chứng minh cho từng cấu hình ở đúng bối cảnh cuối. Đây là bằng chứng tái lập trên cùng dev, và chưa kiểm tương tác VC × E5 hoặc tạo thêm mẫu độc lập.

Nguồn `kb-002/score/{E1,E2,E3,E5}-law.json#/theo_the_gioi/P/{dMRR,P,M,bao_kem/p_kiem_dau,moc_gia,UV6}`, `*-robustness.json#/{bootstrap,ci95/P,delta,h}`, và `results/T-053/runs/k-cham-001/khoi-k.json#/cap`.

## 6. Pilot và kiểm đường chạy gốc

Pilot ban đầu chọn trước ghép nhãn gồm cửa sổ 19, 60, 06. Cả ba đều không có phủ quyết T11 và không đổi F_I ở T12 qua ba thế giới. Vì thế các biên nhận đó kiểm nhánh nền và trường hợp không đổi phân loại, chưa thực hiện đầy đủ yêu cầu pilot có nhánh cơ chế tác động.

Trong bản phản biện lượt 1 Minh chuyển, Claude báo đã chạy đường gốc trên Python 3.12.10, ở cửa sổ 55 với E9 tắt/bật và cửa sổ 43 với T12 bật. Trích nguyên văn phần kết quả.

> Đầu vào, F_I, m, thứ hạng, V0, vùng, kế thừa và đối chứng đều 0 lệch.

Người làm đã kiểm lại rằng các bản ghi phát lại tại cửa sổ 55 có 2 kênh đổi F_I do E9 và tại cửa sổ 43 có 4 kênh đổi F_I do cạnh tĩnh. Kiểm đường gốc của Claude được ghi nhận theo phương án đã trình và Minh duyệt sửa. Nguồn là lời báo của người phản biện đã được Minh chuyển, chưa có gói biên nhận native của lượt đó được ghim trong repo. Các script scratchpad của Claude vẫn là thông tin truy vết, không dùng làm phụ thuộc để dựng lại dữ liệu trên máy khác.

Phép đo bổ sung dưới đây đối chiếu đủ đầu ra phát lại trên 82 cửa sổ. Nó xác nhận đường phát lại tái lập được, còn kiểm đối chiếu native ở hai ca có cơ chế dựa vào lượt kiểm độc lập Claude đã báo. Đây là giới hạn lưu trữ của bằng chứng native bổ sung.

## 7. C-d2 và phần phải mang sang T-052

| MRR tại P | Gộp | RE2-TT | Nezha-OB |
|---|---|---|---|
| Nền | 1411/1560 | 167/180 | 48/55 |
| C-d2 sớm nhất | 2837/3120 | 11/12 | 1187/1320 |

C-d2 cao hơn nền ở cửa sổ 55, 75, 80 và thấp hơn ở 59, 61, 63, 71. Chênh MRR gộp là +3/624, khoảng +0,00481. Đây là so sánh mô tả trên cùng dev. δ của T11/T12 không là phép kiểm tương đương dành cho C-d2.

C-d2 dùng kênh có cờ đã được E1/E2 tính từ quan hệ, rồi ưu tiên khởi phát và khóa thô thay cho phân loại E5 và tầng của chuỗi. Vì vậy nó vẫn giữ tín hiệu quan hệ. C-d3 có RR bằng 0 trên mẫu số 30 RE2-TT ở cả hai vế, trong đó 20 ca trả UNSUPPORTED_CYCLIC, và suy biến trên Nezha-OB theo Đ12.

T-052 cần giữ C-d2 trong bảng đối chứng cho RQ3d và dùng đủ các đối chứng đã duyệt. Dữ liệu dev hiện tại chưa cho thấy nền hơn quy tắc đơn giản này ở số gộp. Bằng chứng lợi ích độc lập của quan hệ còn OPEN.

Nguồn `t12-001/score/regions-controls.json#/{RE2-TT,Nezha-OB}/{summary,rows}`, `t11-001/score/scores.json#/cau_hinh/off`, và `src/m1/doi_chung.py#cd2_tu_kenh`.

## 8. Số chi phí đã có trong lượt cũ

| Lượt | Tổng log cửa sổ RE2 thật | RE2 C-e | Nezha thật | Tổng lượt |
|---|---:|---:|---:|---:|
| T11 | 22,189 giây | 19,436 giây | 4,391 giây | 46,031 giây |
| T12 | 22,765 giây | 19,703 giây | 5,063 giây | 47,547 giây |

Tổng log từng cửa sổ nhỏ hơn tổng lượt 0,015–0,016 giây do phần chuẩn bị ngoài vòng lặp. C-d3 T12 có tổng 0,047 giây ở ca thật RE2 và 0,016 giây ở C-e. Nhiều giá trị C-d3 bằng 0 do độ phân giải đồng hồ của phép đo cũ.

Pilot native T11 có RAM đỉnh 2.062.708.736 byte, khoảng 1,921 GiB. Pilot T12 có RAM đỉnh 2.029.641.728 byte, khoảng 1,890 GiB. Đây là đỉnh của tiến trình pilot. Lượt phát lại chính cũ không lưu RAM đỉnh và KB không lưu tổng thời gian trong log.

Nguồn `t11-001.log`, `t12-001.log`, `t12-001/{index}.json#/control_seconds`, `pilot-native-001/*-{0,1}.json#/peak_rss` và `pilot-t12-native-002/*-1.json#/peak_rss`.

## 9. Phép đo bổ sung và mức đạt sau sửa

Phép đo bổ sung dùng một tiến trình laptop và các thư viện đã có. Nó đọc/hash và giải nén đúng nguồn đã ghim, gọi lại T11/T12 trên 82 cửa sổ, và thực hiện đường kiểm tái sử dụng KB trên 410 bản ghi trong bộ nhớ. Đầu ra T11 khớp toàn bộ. T12 khớp sau khi bỏ trường đo thời gian C-d3. Ba file dữ liệu chính của KB khớp từng byte.

Biên nhận dưới đây lưu số theo cửa sổ và mã tái lập. Các cột có phần lồng nhau, nên không cộng mọi cột thành tổng. Thời gian luồng gzip gồm đọc file nén, giải nén, giải mã UTF-8 và tách dòng. Phân tích JSON được đo riêng. C-d3 là phần con của hậu xử lý. RAM ghi mức đỉnh của tiến trình từ khi khởi động. Cache hệ điều hành không bị ép xóa, nên phép đo này phản ánh lượt đọc hiện tại.

Hồ sơ báo cáo và phép đo bổ sung đã được ghi trong đính chính. Phân rã thời gian lịch sử của lượt đầu vẫn không thể khôi phục. Đây là sai sót ghi nhận của Phiên 1 cần giữ trong lịch sử nghiệm thu. Các giới hạn khoa học tiếp tục gồm cạnh thông điệp/dữ liệu, chiều đảo PageRank, VC × E5, revision nguồn tĩnh, verdict, nhãn vùng, dữ liệu độc lập, chế độ (b), RE3-OB và FlashTicket. Các câu hỏi này không được đóng bằng việc bổ sung bảng hoặc đo lại thời gian.

Đề xuất giữ nền dev Q-241 cho T-052 với cờ E2, chờ Claude kiểm gói sửa và Minh nghiệm thu.


### Bảng đọc nhanh phép đo bổ sung

Ba bước dưới chạy trong cùng một tiến trình. Thời gian tổng gồm xác minh nguồn và đối chiếu kết quả. Thời gian sau nạp là tổng phần case ngoài loader, gồm kiểm tương đương bên trong case. KB dùng lại kết quả nên phần ngoài loader còn gồm xác minh, lắp bản ghi và kiểm byte trong bộ nhớ.

| Bước | Tổng bước | Sau nạp theo cửa sổ | C-d3, nằm trong phần sau nạp | RAM đỉnh tiến trình từ lúc mở |
|---|---:|---:|---:|---:|
| T11_replay | 61.976 giây | 4.512 giây | 0.000 giây | 0.243 GiB |
| T12_replay | 61.174 giây | 4.616 giây | 0.106 giây | 0.253 GiB |
| KB_reuse | 116.530 giây | Không gọi lại bộ xếp hạng | 0.000 giây | 0.545 GiB |

Đọc/hash và giải nén byte được tách trong một lượt bổ sung riêng trên cùng danh sách file nén. Hash được so với seal ở mọi file. Giải nén dùng bộ đệm byte để tách thời gian giải nén khỏi đọc đĩa và phân tích JSON. Các số sau phản ánh cache tại lần đo này.

| Nguồn của bước | Số lượt đọc file | Đọc file | SHA-256 trên bộ đệm | Giải nén byte |
|---|---:|---:|---:|---:|
| T11_inputs | 164 | 0.425 giây | 0.709 giây | 25.761 giây |
| T12_inputs | 164 | 0.423 giây | 0.745 giây | 26.139 giây |
| KB_inputs | 164 | 0.417 giây | 0.727 giây | 26.164 giây |

Hai bảng là các lượt đo khác nhau nên không cộng các cột của chúng thành tổng thời gian. Chi tiết từng file và cửa sổ được giữ trong các khối JSON phía dưới. Tổng thời gian ba bước phát lại là 239.680 giây. Lượt tách đọc/hash/giải nén riêng là 81.529 giây.

## Biên nhận đo bổ sung lượt 2

```json
{
  "cache": "OS cache uncontrolled",
  "failed_attempt_1": "T11 75.618s PASS, T12 66.885s PASS; KB byte check failed because memory LF vs original Windows CRLF; detailed first-pass metrics not retained",
  "initial_hash_audit_seconds": 0.331430799968075,
  "one_process": true,
  "original_manifest_sha256": "0b9d3fd41e217d71ad7316f0b37a1ea60dfc80cc83745950a68199eead5fba61",
  "original_outputs_checked": 261,
  "platform": "Windows-11-10.0.22631-SP0",
  "python": "3.12.14 (main, Aug 25 2026, 14:01:42) [MSC v.1944 64 bit (AMD64)]",
  "scope": "Same T11/T12 82 windows and KB 410 records, in memory, no raw telemetry or new scoring",
  "semantics": {
    "cd3_seconds": "Subset of postprocessing",
    "elapsed_seconds": "Stage including source verification and equality checks, no output file generation or scoring",
    "gzip_text_seconds": "Compressed file read, gzip decompression, UTF-8 decoding and line iteration",
    "hash_read_seconds": "File read and SHA-256 in original helpers",
    "load_excluding_hash_seconds": "Record loader excluding hash duration",
    "parse_json_seconds": "JSON parsing inside records loader",
    "peak_process_rss_bytes_since_start": "Cumulative Windows process high-water RSS",
    "postprocess_seconds": "Per-case elapsed minus record loader and hash"
  },
  "started_utc": "2026-11-04T03:07:07.002913+00:00"
}
```

### T11_replay

```json
{
  "cd3_seconds": 0.0,
  "elapsed_seconds": 61.97614450001856,
  "gzip_text_seconds": 38.92944310099119,
  "hash_read_seconds": 0.015606500091962516,
  "load_excluding_hash_seconds": 54.41902529989602,
  "parity": "All fields equal, excluding runtime-only control_seconds in T12",
  "parity_check_seconds": 2.5901149000856094,
  "parse_json_seconds": 5.099697199650109,
  "peak_process_rss_bytes_since_start": 261156864,
  "stage": "T11_replay",
  "windows": [
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8355477000004612,
      "gzip_text_seconds": 0.5300377997918986,
      "hash_read_seconds": 0.0,
      "index": 0,
      "load_excluding_hash_seconds": 0.7750424999976531,
      "parse_json_seconds": 0.1083122999407351,
      "postprocess_seconds": 0.060505200002808124,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0009328000014648,
      "gzip_text_seconds": 0.671220599906519,
      "hash_read_seconds": 0.0,
      "index": 1,
      "load_excluding_hash_seconds": 0.9025863999850117,
      "parse_json_seconds": 0.08129699999699369,
      "postprocess_seconds": 0.09834640001645312,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.127532800019253,
      "gzip_text_seconds": 0.8168956999434158,
      "hash_read_seconds": 0.0,
      "index": 2,
      "load_excluding_hash_seconds": 1.0816794999991544,
      "parse_json_seconds": 0.07681489997776225,
      "postprocess_seconds": 0.045853300020098686,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.072094000002835,
      "gzip_text_seconds": 0.7688898001797497,
      "hash_read_seconds": 0.0,
      "index": 3,
      "load_excluding_hash_seconds": 1.0044887000112794,
      "parse_json_seconds": 0.07323319994611666,
      "postprocess_seconds": 0.06760529999155551,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.4510810999781825,
      "gzip_text_seconds": 1.0372507000574842,
      "hash_read_seconds": 0.0,
      "index": 4,
      "load_excluding_hash_seconds": 1.404864100040868,
      "parse_json_seconds": 0.08360730001004413,
      "postprocess_seconds": 0.04621699993731454,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.5067030999925919,
      "gzip_text_seconds": 1.039329899882432,
      "hash_read_seconds": 0.0,
      "index": 5,
      "load_excluding_hash_seconds": 1.3712331999558955,
      "parse_json_seconds": 0.08124010008759797,
      "postprocess_seconds": 0.13546990003669634,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7419952999916859,
      "gzip_text_seconds": 0.4861785997636616,
      "hash_read_seconds": 0.0,
      "index": 6,
      "load_excluding_hash_seconds": 0.6872381999855861,
      "parse_json_seconds": 0.07099539996124804,
      "postprocess_seconds": 0.05475710000609979,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7541342000477016,
      "gzip_text_seconds": 0.4857089000288397,
      "hash_read_seconds": 0.0,
      "index": 7,
      "load_excluding_hash_seconds": 0.6897440000320785,
      "parse_json_seconds": 0.07626039994647726,
      "postprocess_seconds": 0.06439020001562312,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.276262100029271,
      "gzip_text_seconds": 0.8930721002980135,
      "hash_read_seconds": 0.0,
      "index": 8,
      "load_excluding_hash_seconds": 1.2291907999897376,
      "parse_json_seconds": 0.07458409998798743,
      "postprocess_seconds": 0.047071300039533526,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.422082600009162,
      "gzip_text_seconds": 0.9741196001996286,
      "hash_read_seconds": 0.0,
      "index": 9,
      "load_excluding_hash_seconds": 1.3516903000418097,
      "parse_json_seconds": 0.12123270001029596,
      "postprocess_seconds": 0.0703922999673523,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.4054089999990538,
      "gzip_text_seconds": 1.0095626001129858,
      "hash_read_seconds": 0.0,
      "index": 10,
      "load_excluding_hash_seconds": 1.3203643000451848,
      "parse_json_seconds": 0.07079560006968677,
      "postprocess_seconds": 0.08504469995386899,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.3075581999728456,
      "gzip_text_seconds": 0.9441407998674549,
      "hash_read_seconds": 0.0,
      "index": 11,
      "load_excluding_hash_seconds": 1.2379823999945074,
      "parse_json_seconds": 0.07049129996448755,
      "postprocess_seconds": 0.06957579997833818,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.2215897000278346,
      "gzip_text_seconds": 0.856533800077159,
      "hash_read_seconds": 0.0,
      "index": 12,
      "load_excluding_hash_seconds": 1.1668244000175036,
      "parse_json_seconds": 0.07430299994302914,
      "postprocess_seconds": 0.054765300010330975,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.1510384999564849,
      "gzip_text_seconds": 0.7969684001873247,
      "hash_read_seconds": 0.0,
      "index": 13,
      "load_excluding_hash_seconds": 1.0731438000220805,
      "parse_json_seconds": 0.07064930006163195,
      "postprocess_seconds": 0.07789469993440434,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5511472999933176,
      "gzip_text_seconds": 0.3463039000052959,
      "hash_read_seconds": 0.0,
      "index": 14,
      "load_excluding_hash_seconds": 0.4998287999769673,
      "parse_json_seconds": 0.06723899999633431,
      "postprocess_seconds": 0.0513185000163503,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.6021314999670722,
      "gzip_text_seconds": 0.3687117002555169,
      "hash_read_seconds": 0.0,
      "index": 15,
      "load_excluding_hash_seconds": 0.5475038000149652,
      "parse_json_seconds": 0.07737519999500364,
      "postprocess_seconds": 0.05462769995210692,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.2803423999575898,
      "gzip_text_seconds": 0.8925660000531934,
      "hash_read_seconds": 0.0,
      "index": 16,
      "load_excluding_hash_seconds": 1.220374200027436,
      "parse_json_seconds": 0.08320109994383529,
      "postprocess_seconds": 0.05996819993015379,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0254446999751963,
      "gzip_text_seconds": 0.6798032999504358,
      "hash_read_seconds": 0.0,
      "index": 17,
      "load_excluding_hash_seconds": 0.9462980999960564,
      "parse_json_seconds": 0.07674470002530143,
      "postprocess_seconds": 0.07914659997913986,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.041339399991557,
      "gzip_text_seconds": 0.7093418998993002,
      "hash_read_seconds": 0.0,
      "index": 18,
      "load_excluding_hash_seconds": 0.9833167999750003,
      "parse_json_seconds": 0.07996879995334893,
      "postprocess_seconds": 0.05802260001655668,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.2257237000158057,
      "gzip_text_seconds": 0.8490461001638323,
      "hash_read_seconds": 0.0,
      "index": 19,
      "load_excluding_hash_seconds": 1.1544313000631519,
      "parse_json_seconds": 0.09146000002510846,
      "postprocess_seconds": 0.0712923999526538,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.885083700006362,
      "gzip_text_seconds": 0.5731673999107443,
      "hash_read_seconds": 0.0,
      "index": 20,
      "load_excluding_hash_seconds": 0.7900046000140719,
      "parse_json_seconds": 0.08302129997173324,
      "postprocess_seconds": 0.09507909999229014,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0292202000273392,
      "gzip_text_seconds": 0.687875899951905,
      "hash_read_seconds": 0.0,
      "index": 21,
      "load_excluding_hash_seconds": 0.959956000035163,
      "parse_json_seconds": 0.07600910001201555,
      "postprocess_seconds": 0.06926419999217615,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.103274799999781,
      "gzip_text_seconds": 0.7533781998790801,
      "hash_read_seconds": 0.0,
      "index": 22,
      "load_excluding_hash_seconds": 1.0460217000218108,
      "parse_json_seconds": 0.06970960000762716,
      "postprocess_seconds": 0.05725309997797012,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0683645999524742,
      "gzip_text_seconds": 0.7281073001795448,
      "hash_read_seconds": 0.0,
      "index": 23,
      "load_excluding_hash_seconds": 1.0038838000036776,
      "parse_json_seconds": 0.07393849996151403,
      "postprocess_seconds": 0.06448079994879663,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9239830000442453,
      "gzip_text_seconds": 0.6233557999948971,
      "hash_read_seconds": 0.0,
      "index": 24,
      "load_excluding_hash_seconds": 0.8671939999912865,
      "parse_json_seconds": 0.0710153000545688,
      "postprocess_seconds": 0.05678900005295873,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0591322999680415,
      "gzip_text_seconds": 0.7235702999751084,
      "hash_read_seconds": 0.0,
      "index": 25,
      "load_excluding_hash_seconds": 0.9979309000191279,
      "parse_json_seconds": 0.07131979992846027,
      "postprocess_seconds": 0.061201399948913604,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9731146999984048,
      "gzip_text_seconds": 0.623767799756024,
      "hash_read_seconds": 0.0,
      "index": 26,
      "load_excluding_hash_seconds": 0.8714554999605753,
      "parse_json_seconds": 0.0742346000042744,
      "postprocess_seconds": 0.10165920003782958,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9092100000125356,
      "gzip_text_seconds": 0.6022645001066849,
      "hash_read_seconds": 0.0,
      "index": 27,
      "load_excluding_hash_seconds": 0.8486646000528708,
      "parse_json_seconds": 0.0741428000619635,
      "postprocess_seconds": 0.06054539995966479,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8706877999939024,
      "gzip_text_seconds": 0.5725921999546699,
      "hash_read_seconds": 0.0,
      "index": 28,
      "load_excluding_hash_seconds": 0.8173316999454983,
      "parse_json_seconds": 0.07271700003184378,
      "postprocess_seconds": 0.05335610004840419,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9672035000403412,
      "gzip_text_seconds": 0.6343224000302143,
      "hash_read_seconds": 0.0,
      "index": 29,
      "load_excluding_hash_seconds": 0.8694943000446074,
      "parse_json_seconds": 0.0762307999539189,
      "postprocess_seconds": 0.0977091999957338,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0992236000020057,
      "gzip_text_seconds": 0.7590546999126673,
      "hash_read_seconds": 0.0,
      "index": 30,
      "load_excluding_hash_seconds": 1.0430130999884568,
      "parse_json_seconds": 0.07025900000007823,
      "postprocess_seconds": 0.05621050001354888,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.194616799999494,
      "gzip_text_seconds": 0.7811252999817953,
      "hash_read_seconds": 0.0,
      "index": 31,
      "load_excluding_hash_seconds": 1.09031189995585,
      "parse_json_seconds": 0.0851239999756217,
      "postprocess_seconds": 0.10430490004364401,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8413792999926955,
      "gzip_text_seconds": 0.5557902998989448,
      "hash_read_seconds": 0.0,
      "index": 32,
      "load_excluding_hash_seconds": 0.7863305999781005,
      "parse_json_seconds": 0.07302709994837642,
      "postprocess_seconds": 0.05504870001459494,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9830717999720946,
      "gzip_text_seconds": 0.6454316996969283,
      "hash_read_seconds": 0.0,
      "index": 33,
      "load_excluding_hash_seconds": 0.8913976000039838,
      "parse_json_seconds": 0.08000839996384457,
      "postprocess_seconds": 0.09167419996811077,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8322238000109792,
      "gzip_text_seconds": 0.5309852998470888,
      "hash_read_seconds": 0.0,
      "index": 34,
      "load_excluding_hash_seconds": 0.7455171999754384,
      "parse_json_seconds": 0.07423949998337775,
      "postprocess_seconds": 0.08670660003554076,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0364675999735482,
      "gzip_text_seconds": 0.6404849999235012,
      "hash_read_seconds": 0.0,
      "index": 35,
      "load_excluding_hash_seconds": 0.9195812999969348,
      "parse_json_seconds": 0.1023868999327533,
      "postprocess_seconds": 0.11688629997661337,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7448148999828845,
      "gzip_text_seconds": 0.47935110004618764,
      "hash_read_seconds": 0.0,
      "index": 36,
      "load_excluding_hash_seconds": 0.6814559999620542,
      "parse_json_seconds": 0.08018539997283369,
      "postprocess_seconds": 0.06335890002083033,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7969172999728471,
      "gzip_text_seconds": 0.4794668998802081,
      "hash_read_seconds": 0.0,
      "index": 37,
      "load_excluding_hash_seconds": 0.682458899973426,
      "parse_json_seconds": 0.06944309995742515,
      "postprocess_seconds": 0.11445839999942109,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8819446999696083,
      "gzip_text_seconds": 0.5760375999379903,
      "hash_read_seconds": 0.0,
      "index": 38,
      "load_excluding_hash_seconds": 0.8202023000339977,
      "parse_json_seconds": 0.07535250001819804,
      "postprocess_seconds": 0.06174239993561059,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0805008999886923,
      "gzip_text_seconds": 0.6613541999831796,
      "hash_read_seconds": 0.0,
      "index": 39,
      "load_excluding_hash_seconds": 0.9280010999646038,
      "parse_json_seconds": 0.07971689995611086,
      "postprocess_seconds": 0.15249980002408847,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7283482000348158,
      "gzip_text_seconds": 0.4753708998905495,
      "hash_read_seconds": 0.0,
      "index": 40,
      "load_excluding_hash_seconds": 0.671087599999737,
      "parse_json_seconds": 0.06914850004250184,
      "postprocess_seconds": 0.057260600035078824,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8077211000490934,
      "gzip_text_seconds": 0.5107031000661664,
      "hash_read_seconds": 0.0,
      "index": 41,
      "load_excluding_hash_seconds": 0.7264589999685995,
      "parse_json_seconds": 0.0726011999649927,
      "postprocess_seconds": 0.08126210008049384,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.6964790999772958,
      "gzip_text_seconds": 0.4577077000285499,
      "hash_read_seconds": 0.0,
      "index": 42,
      "load_excluding_hash_seconds": 0.6452172000426799,
      "parse_json_seconds": 0.06936710001900792,
      "postprocess_seconds": 0.05126189993461594,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7299931999878027,
      "gzip_text_seconds": 0.4717934000073001,
      "hash_read_seconds": 0.0,
      "index": 43,
      "load_excluding_hash_seconds": 0.6712756999768317,
      "parse_json_seconds": 0.07540520001202822,
      "postprocess_seconds": 0.05871750001097098,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7944454000098631,
      "gzip_text_seconds": 0.52204329991946,
      "hash_read_seconds": 0.0,
      "index": 44,
      "load_excluding_hash_seconds": 0.7413910999894142,
      "parse_json_seconds": 0.0767282999586314,
      "postprocess_seconds": 0.053054300020448864,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0577846000087447,
      "gzip_text_seconds": 0.6536637000972405,
      "hash_read_seconds": 0.0,
      "index": 45,
      "load_excluding_hash_seconds": 0.9543537000427023,
      "parse_json_seconds": 0.11238479998428375,
      "postprocess_seconds": 0.10343089996604249,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7506498000002466,
      "gzip_text_seconds": 0.47215070005040616,
      "hash_read_seconds": 0.0,
      "index": 46,
      "load_excluding_hash_seconds": 0.685851999965962,
      "parse_json_seconds": 0.0747302999952808,
      "postprocess_seconds": 0.06479780003428459,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8754669000045396,
      "gzip_text_seconds": 0.541146200208459,
      "hash_read_seconds": 0.0,
      "index": 47,
      "load_excluding_hash_seconds": 0.7689883999992162,
      "parse_json_seconds": 0.07688330003293231,
      "postprocess_seconds": 0.10647850000532344,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5159635999589227,
      "gzip_text_seconds": 0.318876699951943,
      "hash_read_seconds": 0.0,
      "index": 48,
      "load_excluding_hash_seconds": 0.4681775000062771,
      "parse_json_seconds": 0.06290710001485422,
      "postprocess_seconds": 0.0477860999526456,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5322603999520652,
      "gzip_text_seconds": 0.3257414000108838,
      "hash_read_seconds": 0.0,
      "index": 49,
      "load_excluding_hash_seconds": 0.4754564999602735,
      "parse_json_seconds": 0.06778159999521449,
      "postprocess_seconds": 0.056803899991791695,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.4990851000184193,
      "gzip_text_seconds": 0.3098814999102615,
      "hash_read_seconds": 0.0,
      "index": 50,
      "load_excluding_hash_seconds": 0.4519571999553591,
      "parse_json_seconds": 0.05954889999702573,
      "postprocess_seconds": 0.047127900063060224,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5274960999959148,
      "gzip_text_seconds": 0.3258875999599695,
      "hash_read_seconds": 0.0,
      "index": 51,
      "load_excluding_hash_seconds": 0.4712504000053741,
      "parse_json_seconds": 0.06232720002299175,
      "postprocess_seconds": 0.05624569999054074,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.4851668000337668,
      "gzip_text_seconds": 0.31040720001328737,
      "hash_read_seconds": 0.0,
      "index": 52,
      "load_excluding_hash_seconds": 0.4454248999245465,
      "parse_json_seconds": 0.05915480002295226,
      "postprocess_seconds": 0.039741900109220296,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5638648000312969,
      "gzip_text_seconds": 0.31101360014872625,
      "hash_read_seconds": 0.0,
      "index": 53,
      "load_excluding_hash_seconds": 0.4660450999508612,
      "parse_json_seconds": 0.06522789993323386,
      "postprocess_seconds": 0.09781970008043572,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.4976899000466801,
      "gzip_text_seconds": 0.3028931000153534,
      "hash_read_seconds": 0.0,
      "index": 54,
      "load_excluding_hash_seconds": 0.4534705999540165,
      "parse_json_seconds": 0.06961130001582205,
      "postprocess_seconds": 0.044219300092663616,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.49148119997698814,
      "gzip_text_seconds": 0.30125159985618666,
      "hash_read_seconds": 0.0,
      "index": 55,
      "load_excluding_hash_seconds": 0.44453879992943257,
      "parse_json_seconds": 0.058680899965111166,
      "postprocess_seconds": 0.046942400047555566,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.48935659998096526,
      "gzip_text_seconds": 0.30772510007955134,
      "hash_read_seconds": 0.0,
      "index": 56,
      "load_excluding_hash_seconds": 0.4499258999712765,
      "parse_json_seconds": 0.05887870001606643,
      "postprocess_seconds": 0.039430700009688735,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.504916800011415,
      "gzip_text_seconds": 0.2972566000535153,
      "hash_read_seconds": 0.0,
      "index": 57,
      "load_excluding_hash_seconds": 0.44074560003355145,
      "parse_json_seconds": 0.06024100002832711,
      "postprocess_seconds": 0.06417119997786358,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.48691420000977814,
      "gzip_text_seconds": 0.29375099996104836,
      "hash_read_seconds": 0.0,
      "index": 58,
      "load_excluding_hash_seconds": 0.43615359999239445,
      "parse_json_seconds": 0.05649819999234751,
      "postprocess_seconds": 0.050760600017383695,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.49019089998910204,
      "gzip_text_seconds": 0.2995034002815373,
      "hash_read_seconds": 0.0,
      "index": 59,
      "load_excluding_hash_seconds": 0.44284829997923225,
      "parse_json_seconds": 0.05702219996601343,
      "postprocess_seconds": 0.047342600009869784,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.2342691000085324,
      "gzip_text_seconds": 0.15464820008492097,
      "hash_read_seconds": 0.0,
      "index": 60,
      "load_excluding_hash_seconds": 0.22061360004590824,
      "parse_json_seconds": 0.02828540006885305,
      "postprocess_seconds": 0.013655499962624162,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.21859980002045631,
      "gzip_text_seconds": 0.14213210018351674,
      "hash_read_seconds": 0.0,
      "index": 61,
      "load_excluding_hash_seconds": 0.20206299994606525,
      "parse_json_seconds": 0.024522299994714558,
      "postprocess_seconds": 0.016536800074391067,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22912640002323315,
      "gzip_text_seconds": 0.1503845002152957,
      "hash_read_seconds": 0.0,
      "index": 62,
      "load_excluding_hash_seconds": 0.21508920000633225,
      "parse_json_seconds": 0.025381100014783442,
      "postprocess_seconds": 0.014037200016900897,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23208389995852485,
      "gzip_text_seconds": 0.15415570023469627,
      "hash_read_seconds": 0.0,
      "index": 63,
      "load_excluding_hash_seconds": 0.2194568999693729,
      "parse_json_seconds": 0.02793420001398772,
      "postprocess_seconds": 0.012626999989151955,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23246650001965463,
      "gzip_text_seconds": 0.15281600027810782,
      "hash_read_seconds": 0.0,
      "index": 64,
      "load_excluding_hash_seconds": 0.21898830006830394,
      "parse_json_seconds": 0.026230900024529546,
      "postprocess_seconds": 0.013478199951350689,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23386920004850253,
      "gzip_text_seconds": 0.15003899985458702,
      "hash_read_seconds": 0.0,
      "index": 65,
      "load_excluding_hash_seconds": 0.21766279998701066,
      "parse_json_seconds": 0.029465300031006336,
      "postprocess_seconds": 0.016206400061491877,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.2374201999627985,
      "gzip_text_seconds": 0.15083919983590022,
      "hash_read_seconds": 0.0,
      "index": 66,
      "load_excluding_hash_seconds": 0.2219311999506317,
      "parse_json_seconds": 0.028082899982109666,
      "postprocess_seconds": 0.015489000012166798,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22570800001267344,
      "gzip_text_seconds": 0.14503219991456717,
      "hash_read_seconds": 0.0,
      "index": 67,
      "load_excluding_hash_seconds": 0.21212250005919486,
      "parse_json_seconds": 0.028149399964604527,
      "postprocess_seconds": 0.013585499953478575,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.240270700014662,
      "gzip_text_seconds": 0.15802819997770712,
      "hash_read_seconds": 0.0,
      "index": 68,
      "load_excluding_hash_seconds": 0.22315400006482378,
      "parse_json_seconds": 0.025735799979884177,
      "postprocess_seconds": 0.01711669994983822,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23708229995099828,
      "gzip_text_seconds": 0.15190640010405332,
      "hash_read_seconds": 0.0,
      "index": 69,
      "load_excluding_hash_seconds": 0.2217612000531517,
      "parse_json_seconds": 0.030968000006396323,
      "postprocess_seconds": 0.01532109989784658,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.21362819999922067,
      "gzip_text_seconds": 0.14031959988642484,
      "hash_read_seconds": 0.0,
      "index": 70,
      "load_excluding_hash_seconds": 0.20027899992419407,
      "parse_json_seconds": 0.024786199966911227,
      "postprocess_seconds": 0.013349200075026602,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24144630000228062,
      "gzip_text_seconds": 0.16019400011282414,
      "hash_read_seconds": 0.0,
      "index": 71,
      "load_excluding_hash_seconds": 0.22530580003513023,
      "parse_json_seconds": 0.025187699939124286,
      "postprocess_seconds": 0.01614049996715039,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22656260000076145,
      "gzip_text_seconds": 0.14926769986050203,
      "hash_read_seconds": 0.0,
      "index": 72,
      "load_excluding_hash_seconds": 0.21356379997450858,
      "parse_json_seconds": 0.024918099981732666,
      "postprocess_seconds": 0.012998800026252866,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24077569996006787,
      "gzip_text_seconds": 0.15697739995084703,
      "hash_read_seconds": 0.0,
      "index": 73,
      "load_excluding_hash_seconds": 0.2270699999644421,
      "parse_json_seconds": 0.026130600017495453,
      "postprocess_seconds": 0.013705699995625764,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.25374190002912655,
      "gzip_text_seconds": 0.162121000001207,
      "hash_read_seconds": 0.0,
      "index": 74,
      "load_excluding_hash_seconds": 0.23486109997611493,
      "parse_json_seconds": 0.026879100070800632,
      "postprocess_seconds": 0.018880800053011626,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22798750002402812,
      "gzip_text_seconds": 0.14546480035642162,
      "hash_read_seconds": 0.0,
      "index": 75,
      "load_excluding_hash_seconds": 0.21366590005345643,
      "parse_json_seconds": 0.02663070004200563,
      "postprocess_seconds": 0.014321599970571697,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24120580003364012,
      "gzip_text_seconds": 0.15584720007609576,
      "hash_read_seconds": 0.0,
      "index": 76,
      "load_excluding_hash_seconds": 0.22448530001565814,
      "parse_json_seconds": 0.02684820001013577,
      "postprocess_seconds": 0.016720500017981976,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22863510000752285,
      "gzip_text_seconds": 0.1459737002151087,
      "hash_read_seconds": 0.0,
      "index": 77,
      "load_excluding_hash_seconds": 0.21566980000352487,
      "parse_json_seconds": 0.02779939997708425,
      "postprocess_seconds": 0.012965300003997982,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22718990000430495,
      "gzip_text_seconds": 0.14817219995893538,
      "hash_read_seconds": 0.0,
      "index": 78,
      "load_excluding_hash_seconds": 0.21246099995914847,
      "parse_json_seconds": 0.024850399990100414,
      "postprocess_seconds": 0.014728900045156479,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24148849997436628,
      "gzip_text_seconds": 0.16136839997489005,
      "hash_read_seconds": 0.0,
      "index": 79,
      "load_excluding_hash_seconds": 0.22883720003301278,
      "parse_json_seconds": 0.02554290002444759,
      "postprocess_seconds": 0.0126512999413535,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22322370001347736,
      "gzip_text_seconds": 0.1430185999488458,
      "hash_read_seconds": 0.0,
      "index": 80,
      "load_excluding_hash_seconds": 0.20994460000656545,
      "parse_json_seconds": 0.030975200003013015,
      "postprocess_seconds": 0.013279100006911904,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23873809998622164,
      "gzip_text_seconds": 0.15480309998383746,
      "hash_read_seconds": 0.0,
      "index": 81,
      "load_excluding_hash_seconds": 0.221387300058268,
      "parse_json_seconds": 0.027377900027204305,
      "postprocess_seconds": 0.01735079992795363,
      "window": "that"
    }
  ]
}
```

### T12_replay

```json
{
  "baseline_read_parse_seconds": 0.35089709993917495,
  "cd3_seconds": 0.10620010021375492,
  "elapsed_seconds": 61.17408540000906,
  "gzip_text_seconds": 37.25247039907845,
  "hash_read_seconds": 0.008801400021184236,
  "load_excluding_hash_seconds": 52.728497799427714,
  "parity": "All fields equal, excluding runtime-only control_seconds in T12",
  "parity_check_seconds": 2.981300099985674,
  "parse_json_seconds": 5.069048900215421,
  "peak_process_rss_bytes_since_start": 271597568,
  "stage": "T12_replay",
  "windows": [
    {
      "cd3_seconds": 0.0031103999936021864,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7337211000267416,
      "gzip_text_seconds": 0.4660709001473151,
      "hash_read_seconds": 0.0,
      "index": 0,
      "load_excluding_hash_seconds": 0.6770442000124604,
      "parse_json_seconds": 0.08231239998713136,
      "postprocess_seconds": 0.05667690001428127,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0013543999521061778,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9036486999830231,
      "gzip_text_seconds": 0.5041130998870358,
      "hash_read_seconds": 0.0,
      "index": 1,
      "load_excluding_hash_seconds": 0.7298461000318639,
      "parse_json_seconds": 0.0726270999875851,
      "postprocess_seconds": 0.1738025999511592,
      "window": "that"
    },
    {
      "cd3_seconds": 5.699985194951296e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9972824000287801,
      "gzip_text_seconds": 0.6708544000284746,
      "hash_read_seconds": 0.0,
      "index": 2,
      "load_excluding_hash_seconds": 0.9553531999699771,
      "parse_json_seconds": 0.07149669993668795,
      "postprocess_seconds": 0.04192920005880296,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0012292999308556318,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0151950000436045,
      "gzip_text_seconds": 0.7104900000267662,
      "hash_read_seconds": 0.0,
      "index": 3,
      "load_excluding_hash_seconds": 0.9666575999581255,
      "parse_json_seconds": 0.08469879999756813,
      "postprocess_seconds": 0.04853740008547902,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0009543999913148582,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.271990299981553,
      "gzip_text_seconds": 0.8888464000774547,
      "hash_read_seconds": 0.0,
      "index": 4,
      "load_excluding_hash_seconds": 1.2197562999790534,
      "parse_json_seconds": 0.07971459999680519,
      "postprocess_seconds": 0.05223400000249967,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0012549999519251287,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.403561900020577,
      "gzip_text_seconds": 0.9397897997987457,
      "hash_read_seconds": 0.0,
      "index": 5,
      "load_excluding_hash_seconds": 1.2880585999810137,
      "parse_json_seconds": 0.0758843999938108,
      "postprocess_seconds": 0.11550330003956333,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0024938000715337694,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7118826000369154,
      "gzip_text_seconds": 0.46019759989576414,
      "hash_read_seconds": 0.0,
      "index": 6,
      "load_excluding_hash_seconds": 0.6563681999687105,
      "parse_json_seconds": 0.07364010001765564,
      "postprocess_seconds": 0.05551440006820485,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0038598000537604094,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7318488999735564,
      "gzip_text_seconds": 0.4637146999593824,
      "hash_read_seconds": 0.0,
      "index": 7,
      "load_excluding_hash_seconds": 0.6740315000060946,
      "parse_json_seconds": 0.076621999964118,
      "postprocess_seconds": 0.057817399967461824,
      "window": "that"
    },
    {
      "cd3_seconds": 7.299997378140688e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.1453597000217997,
      "gzip_text_seconds": 0.7863652001251467,
      "hash_read_seconds": 0.0,
      "index": 8,
      "load_excluding_hash_seconds": 1.0895759999402799,
      "parse_json_seconds": 0.07123920001322404,
      "postprocess_seconds": 0.05578370008151978,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0014019000809639692,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.270314099965617,
      "gzip_text_seconds": 0.8679726999253035,
      "hash_read_seconds": 0.0,
      "index": 9,
      "load_excluding_hash_seconds": 1.2015152999665588,
      "parse_json_seconds": 0.0880483000073582,
      "postprocess_seconds": 0.06879879999905825,
      "window": "that"
    },
    {
      "cd3_seconds": 4.800036549568176e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.1681422000401653,
      "gzip_text_seconds": 0.7971005998551846,
      "hash_read_seconds": 0.0,
      "index": 10,
      "load_excluding_hash_seconds": 1.1150046999682672,
      "parse_json_seconds": 0.07640389999141917,
      "postprocess_seconds": 0.0531375000718981,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0012199000339023769,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.2095102000166662,
      "gzip_text_seconds": 0.8270216998062097,
      "hash_read_seconds": 0.0,
      "index": 11,
      "load_excluding_hash_seconds": 1.1358655000221916,
      "parse_json_seconds": 0.08278220001375303,
      "postprocess_seconds": 0.07364469999447465,
      "window": "that"
    },
    {
      "cd3_seconds": 6.199989002197981e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0697320000035688,
      "gzip_text_seconds": 0.7261933000991121,
      "hash_read_seconds": 0.0,
      "index": 12,
      "load_excluding_hash_seconds": 1.0068600000231527,
      "parse_json_seconds": 0.06872280006064102,
      "postprocess_seconds": 0.06287199998041615,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0011630000080913305,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.1242136000073515,
      "gzip_text_seconds": 0.7564589000539854,
      "hash_read_seconds": 0.0,
      "index": 13,
      "load_excluding_hash_seconds": 1.0535471999901347,
      "parse_json_seconds": 0.09433079999871552,
      "postprocess_seconds": 0.0706664000172168,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0009266000124625862,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5328829000354744,
      "gzip_text_seconds": 0.3302598998998292,
      "hash_read_seconds": 0.0,
      "index": 14,
      "load_excluding_hash_seconds": 0.4888857999467291,
      "parse_json_seconds": 0.06948340003145859,
      "postprocess_seconds": 0.043997100088745356,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0011156999389640987,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5450212000287138,
      "gzip_text_seconds": 0.3323041999246925,
      "hash_read_seconds": 0.0,
      "index": 15,
      "load_excluding_hash_seconds": 0.49340530001791194,
      "parse_json_seconds": 0.06867629999760538,
      "postprocess_seconds": 0.05161590001080185,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0029372000135481358,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.2094289000378922,
      "gzip_text_seconds": 0.8233414001297206,
      "hash_read_seconds": 0.0,
      "index": 16,
      "load_excluding_hash_seconds": 1.1535850000218488,
      "parse_json_seconds": 0.07375730009516701,
      "postprocess_seconds": 0.055843900016043335,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0013895000447519124,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9845983000122942,
      "gzip_text_seconds": 0.641621699964162,
      "hash_read_seconds": 0.0,
      "index": 17,
      "load_excluding_hash_seconds": 0.8995655999751762,
      "parse_json_seconds": 0.07319360005203635,
      "postprocess_seconds": 0.08503270003711805,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0020676999702118337,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9579749999684282,
      "gzip_text_seconds": 0.6351843000738882,
      "hash_read_seconds": 0.0,
      "index": 18,
      "load_excluding_hash_seconds": 0.8958107000216842,
      "parse_json_seconds": 0.08198840002296492,
      "postprocess_seconds": 0.062164299946743995,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.001393499958794564,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.2412080999929458,
      "gzip_text_seconds": 0.850736899941694,
      "hash_read_seconds": 0.0,
      "index": 19,
      "load_excluding_hash_seconds": 1.1661256999941543,
      "parse_json_seconds": 0.08096610003849491,
      "postprocess_seconds": 0.07508239999879152,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0047833999851718545,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8347490000305697,
      "gzip_text_seconds": 0.5471338998759165,
      "hash_read_seconds": 0.0,
      "index": 20,
      "load_excluding_hash_seconds": 0.7709508999832906,
      "parse_json_seconds": 0.08384129998739809,
      "postprocess_seconds": 0.06379810004727915,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0013422999763861299,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0229857999947853,
      "gzip_text_seconds": 0.63416680006776,
      "hash_read_seconds": 0.0,
      "index": 21,
      "load_excluding_hash_seconds": 0.910994500038214,
      "parse_json_seconds": 0.09396059991559014,
      "postprocess_seconds": 0.11199129995657131,
      "window": "that"
    },
    {
      "cd3_seconds": 5.900044925510883e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0325489999959245,
      "gzip_text_seconds": 0.6908249999396503,
      "hash_read_seconds": 0.0,
      "index": 22,
      "load_excluding_hash_seconds": 0.9733625000226311,
      "parse_json_seconds": 0.0733598000369966,
      "postprocess_seconds": 0.059186499973293394,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0018628000398166478,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0380789000191726,
      "gzip_text_seconds": 0.7080252000596374,
      "hash_read_seconds": 0.0,
      "index": 23,
      "load_excluding_hash_seconds": 0.9659715000307187,
      "parse_json_seconds": 0.07338240003446117,
      "postprocess_seconds": 0.07210739998845384,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0009988999809138477,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0636128999758512,
      "gzip_text_seconds": 0.7410258001182228,
      "hash_read_seconds": 0.0,
      "index": 24,
      "load_excluding_hash_seconds": 1.0081832999712788,
      "parse_json_seconds": 0.0760335000231862,
      "postprocess_seconds": 0.05542960000457242,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0028202999965287745,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.127548599964939,
      "gzip_text_seconds": 0.7394685000181198,
      "hash_read_seconds": 0.0,
      "index": 25,
      "load_excluding_hash_seconds": 1.0268896000343375,
      "parse_json_seconds": 0.08183689997531474,
      "postprocess_seconds": 0.10065899993060157,
      "window": "that"
    },
    {
      "cd3_seconds": 0.003352800034917891,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9617796000093222,
      "gzip_text_seconds": 0.6358584999106824,
      "hash_read_seconds": 0.0,
      "index": 26,
      "load_excluding_hash_seconds": 0.9024526000139304,
      "parse_json_seconds": 0.08506389998365194,
      "postprocess_seconds": 0.059326999995391816,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.006443699996452779,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.91489149996778,
      "gzip_text_seconds": 0.6146558999316767,
      "hash_read_seconds": 0.0,
      "index": 27,
      "load_excluding_hash_seconds": 0.8570859999745153,
      "parse_json_seconds": 0.0746431999723427,
      "postprocess_seconds": 0.057805499993264675,
      "window": "that"
    },
    {
      "cd3_seconds": 0.002892000018619001,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9289852999499999,
      "gzip_text_seconds": 0.6062909999745898,
      "hash_read_seconds": 0.0,
      "index": 28,
      "load_excluding_hash_seconds": 0.8656649999320507,
      "parse_json_seconds": 0.08323059999383986,
      "postprocess_seconds": 0.0633203000179492,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0013257000246085227,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0542576999869198,
      "gzip_text_seconds": 0.6856764997937717,
      "hash_read_seconds": 0.0,
      "index": 29,
      "load_excluding_hash_seconds": 0.962935000017751,
      "parse_json_seconds": 0.07866100000683218,
      "postprocess_seconds": 0.09132269996916875,
      "window": "that"
    },
    {
      "cd3_seconds": 0.003905000048689544,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0624070999911055,
      "gzip_text_seconds": 0.7249793001683429,
      "hash_read_seconds": 0.0,
      "index": 30,
      "load_excluding_hash_seconds": 1.0064833000069484,
      "parse_json_seconds": 0.07215629995334893,
      "postprocess_seconds": 0.055923799984157085,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0011918000527657568,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.1047994999680668,
      "gzip_text_seconds": 0.7366762000601739,
      "hash_read_seconds": 0.0,
      "index": 31,
      "load_excluding_hash_seconds": 1.0243063000380062,
      "parse_json_seconds": 0.07036269997479394,
      "postprocess_seconds": 0.08049319993006065,
      "window": "that"
    },
    {
      "cd3_seconds": 6.9999368861317635e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8868383999797516,
      "gzip_text_seconds": 0.55972000019392,
      "hash_read_seconds": 0.0,
      "index": 32,
      "load_excluding_hash_seconds": 0.7843548000091687,
      "parse_json_seconds": 0.07458680000854656,
      "postprocess_seconds": 0.10248359997058287,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0014759000041522086,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9467183999950066,
      "gzip_text_seconds": 0.6159183999407105,
      "hash_read_seconds": 0.0,
      "index": 33,
      "load_excluding_hash_seconds": 0.861739200016018,
      "parse_json_seconds": 0.07607040001312271,
      "postprocess_seconds": 0.08497919997898862,
      "window": "that"
    },
    {
      "cd3_seconds": 8.699949830770493e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7927879999624565,
      "gzip_text_seconds": 0.5316727999015711,
      "hash_read_seconds": 0.0,
      "index": 34,
      "load_excluding_hash_seconds": 0.7411753999767825,
      "parse_json_seconds": 0.06840030004968867,
      "postprocess_seconds": 0.051612599985674024,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0023530999897047877,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.006049300020095,
      "gzip_text_seconds": 0.6070299002458341,
      "hash_read_seconds": 0.0,
      "index": 35,
      "load_excluding_hash_seconds": 0.8450108000542969,
      "parse_json_seconds": 0.07689000002574176,
      "postprocess_seconds": 0.1610384999657981,
      "window": "that"
    },
    {
      "cd3_seconds": 6.400048732757568e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7329119999776594,
      "gzip_text_seconds": 0.4808410002151504,
      "hash_read_seconds": 0.0,
      "index": 36,
      "load_excluding_hash_seconds": 0.6745338999899104,
      "parse_json_seconds": 0.0699787000194192,
      "postprocess_seconds": 0.05837809998774901,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0010251000057905912,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7487947999616154,
      "gzip_text_seconds": 0.4881160000222735,
      "hash_read_seconds": 0.0,
      "index": 37,
      "load_excluding_hash_seconds": 0.696671099984087,
      "parse_json_seconds": 0.07247150002513081,
      "postprocess_seconds": 0.052123699977528304,
      "window": "that"
    },
    {
      "cd3_seconds": 6.900052540004253e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.825915299996268,
      "gzip_text_seconds": 0.5446702998597175,
      "hash_read_seconds": 0.0,
      "index": 38,
      "load_excluding_hash_seconds": 0.7742372999782674,
      "parse_json_seconds": 0.07539950002683327,
      "postprocess_seconds": 0.0516780000180006,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0014715000288560987,
      "dataset": "RE2-TT",
      "elapsed_seconds": 1.0598557000048459,
      "gzip_text_seconds": 0.6526555998716503,
      "hash_read_seconds": 0.0,
      "index": 39,
      "load_excluding_hash_seconds": 0.9261296999175102,
      "parse_json_seconds": 0.07702540006721392,
      "postprocess_seconds": 0.1337260000873357,
      "window": "that"
    },
    {
      "cd3_seconds": 6.499991286545992e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7590847000246868,
      "gzip_text_seconds": 0.49568479997105896,
      "hash_read_seconds": 0.0,
      "index": 40,
      "load_excluding_hash_seconds": 0.7060124000418,
      "parse_json_seconds": 0.07179449999239296,
      "postprocess_seconds": 0.05307229998288676,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0013702000142075121,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8326431000023149,
      "gzip_text_seconds": 0.5290249000536278,
      "hash_read_seconds": 0.0,
      "index": 41,
      "load_excluding_hash_seconds": 0.7575459000072442,
      "parse_json_seconds": 0.09413300000596792,
      "postprocess_seconds": 0.0750971999950707,
      "window": "that"
    },
    {
      "cd3_seconds": 0.00222239998402074,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8347470000153407,
      "gzip_text_seconds": 0.5146564000751823,
      "hash_read_seconds": 0.0,
      "index": 42,
      "load_excluding_hash_seconds": 0.730095699953381,
      "parse_json_seconds": 0.07436139998026192,
      "postprocess_seconds": 0.10465130006195977,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.005091899947728962,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.728827100014314,
      "gzip_text_seconds": 0.4709582002251409,
      "hash_read_seconds": 0.0,
      "index": 43,
      "load_excluding_hash_seconds": 0.6664794000098482,
      "parse_json_seconds": 0.0688100999686867,
      "postprocess_seconds": 0.06234770000446588,
      "window": "that"
    },
    {
      "cd3_seconds": 0.003715299942996353,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7981235999614,
      "gzip_text_seconds": 0.5202812000061385,
      "hash_read_seconds": 0.0,
      "index": 44,
      "load_excluding_hash_seconds": 0.7436006999923848,
      "parse_json_seconds": 0.07081429997924715,
      "postprocess_seconds": 0.05452289996901527,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0014962999848648906,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.9818190000369214,
      "gzip_text_seconds": 0.6227754998835735,
      "hash_read_seconds": 0.0,
      "index": 45,
      "load_excluding_hash_seconds": 0.8854030000511557,
      "parse_json_seconds": 0.07364679995225742,
      "postprocess_seconds": 0.09641599998576567,
      "window": "that"
    },
    {
      "cd3_seconds": 4.999979864805937e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.7084024000214413,
      "gzip_text_seconds": 0.4529344999464229,
      "hash_read_seconds": 0.0,
      "index": 46,
      "load_excluding_hash_seconds": 0.6541572000132874,
      "parse_json_seconds": 0.07120589999249205,
      "postprocess_seconds": 0.054245200008153915,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0015014000236988068,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.8371397000155412,
      "gzip_text_seconds": 0.5220055000972934,
      "hash_read_seconds": 0.0,
      "index": 47,
      "load_excluding_hash_seconds": 0.7445680999662727,
      "parse_json_seconds": 0.07527130004018545,
      "postprocess_seconds": 0.09257160004926845,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0016663999995216727,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5417510999832302,
      "gzip_text_seconds": 0.30517169984523207,
      "hash_read_seconds": 0.0,
      "index": 48,
      "load_excluding_hash_seconds": 0.44651399995200336,
      "parse_json_seconds": 0.05854110006475821,
      "postprocess_seconds": 0.09523710003122687,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.004954100062604994,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5204236000427045,
      "gzip_text_seconds": 0.3169318999280222,
      "hash_read_seconds": 0.0,
      "index": 49,
      "load_excluding_hash_seconds": 0.46438299998408183,
      "parse_json_seconds": 0.06527149997418746,
      "postprocess_seconds": 0.05604060005862266,
      "window": "that"
    },
    {
      "cd3_seconds": 5.199981387704611e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5105609999736771,
      "gzip_text_seconds": 0.314689300081227,
      "hash_read_seconds": 0.0,
      "index": 50,
      "load_excluding_hash_seconds": 0.464687799976673,
      "parse_json_seconds": 0.06648740003583953,
      "postprocess_seconds": 0.04587319999700412,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.0048408000147901475,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5376389999873936,
      "gzip_text_seconds": 0.33188210014486685,
      "hash_read_seconds": 0.0,
      "index": 51,
      "load_excluding_hash_seconds": 0.4889024999574758,
      "parse_json_seconds": 0.06350879999808967,
      "postprocess_seconds": 0.048736500029917806,
      "window": "that"
    },
    {
      "cd3_seconds": 5.600042641162872e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5194216000381857,
      "gzip_text_seconds": 0.30397409992292523,
      "hash_read_seconds": 0.0,
      "index": 52,
      "load_excluding_hash_seconds": 0.4742010999470949,
      "parse_json_seconds": 0.08717610000167042,
      "postprocess_seconds": 0.0452205000910908,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.001913099957164377,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5836766999564134,
      "gzip_text_seconds": 0.32315500010736287,
      "hash_read_seconds": 0.0,
      "index": 53,
      "load_excluding_hash_seconds": 0.48037200001999736,
      "parse_json_seconds": 0.07230959995649755,
      "postprocess_seconds": 0.103304699936416,
      "window": "that"
    },
    {
      "cd3_seconds": 5.900044925510883e-06,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.501607200014405,
      "gzip_text_seconds": 0.30809829995268956,
      "hash_read_seconds": 0.0,
      "index": 54,
      "load_excluding_hash_seconds": 0.4454281999496743,
      "parse_json_seconds": 0.05880150001030415,
      "postprocess_seconds": 0.056179000064730644,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.003296000009868294,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.48841799999354407,
      "gzip_text_seconds": 0.29956350004067644,
      "hash_read_seconds": 0.0,
      "index": 55,
      "load_excluding_hash_seconds": 0.44096289994195104,
      "parse_json_seconds": 0.05953100003534928,
      "postprocess_seconds": 0.047455100051593035,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0018782999832183123,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.49203660001512617,
      "gzip_text_seconds": 0.2957507001119666,
      "hash_read_seconds": 0.0,
      "index": 56,
      "load_excluding_hash_seconds": 0.4359064000309445,
      "parse_json_seconds": 0.0608811000129208,
      "postprocess_seconds": 0.05613019998418167,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.002194299944676459,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5302374999737367,
      "gzip_text_seconds": 0.32958449982106686,
      "hash_read_seconds": 0.0,
      "index": 57,
      "load_excluding_hash_seconds": 0.48662560002412647,
      "parse_json_seconds": 0.06256210000719875,
      "postprocess_seconds": 0.04361189994961023,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0023030000156722963,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.4945377999683842,
      "gzip_text_seconds": 0.30698649981059134,
      "hash_read_seconds": 0.0,
      "index": 58,
      "load_excluding_hash_seconds": 0.4459443000378087,
      "parse_json_seconds": 0.05797409999649972,
      "postprocess_seconds": 0.04859349993057549,
      "window": "ce"
    },
    {
      "cd3_seconds": 0.002553100057411939,
      "dataset": "RE2-TT",
      "elapsed_seconds": 0.5129425000050105,
      "gzip_text_seconds": 0.2880218997015618,
      "hash_read_seconds": 0.0,
      "index": 59,
      "load_excluding_hash_seconds": 0.42932830000063404,
      "parse_json_seconds": 0.0626052999868989,
      "postprocess_seconds": 0.08361420000437647,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24628780002240092,
      "gzip_text_seconds": 0.15734869992593303,
      "hash_read_seconds": 0.0,
      "index": 60,
      "load_excluding_hash_seconds": 0.23236920003546402,
      "parse_json_seconds": 0.035458400030620396,
      "postprocess_seconds": 0.013918599986936897,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.2256576999789104,
      "gzip_text_seconds": 0.1442698998725973,
      "hash_read_seconds": 0.0,
      "index": 61,
      "load_excluding_hash_seconds": 0.21074750000843778,
      "parse_json_seconds": 0.024723699956666678,
      "postprocess_seconds": 0.014910199970472604,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22705169999971986,
      "gzip_text_seconds": 0.1446254999609664,
      "hash_read_seconds": 0.0,
      "index": 62,
      "load_excluding_hash_seconds": 0.2103225999744609,
      "parse_json_seconds": 0.025212999957147986,
      "postprocess_seconds": 0.01672910002525896,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.2271269999910146,
      "gzip_text_seconds": 0.1472013999009505,
      "hash_read_seconds": 0.0,
      "index": 63,
      "load_excluding_hash_seconds": 0.21477680001407862,
      "parse_json_seconds": 0.025226199999451637,
      "postprocess_seconds": 0.012350199976935983,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.2281377000035718,
      "gzip_text_seconds": 0.15031850012019277,
      "hash_read_seconds": 0.0,
      "index": 64,
      "load_excluding_hash_seconds": 0.21547789993928745,
      "parse_json_seconds": 0.025853400002233684,
      "postprocess_seconds": 0.012659800064284354,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22716390003915876,
      "gzip_text_seconds": 0.1491244999342598,
      "hash_read_seconds": 0.0,
      "index": 65,
      "load_excluding_hash_seconds": 0.2142921999329701,
      "parse_json_seconds": 0.02488220005761832,
      "postprocess_seconds": 0.012871700106188655,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24680459999945015,
      "gzip_text_seconds": 0.1607111997436732,
      "hash_read_seconds": 0.0,
      "index": 66,
      "load_excluding_hash_seconds": 0.2334065000177361,
      "parse_json_seconds": 0.028006999986246228,
      "postprocess_seconds": 0.01339809998171404,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22533069999190047,
      "gzip_text_seconds": 0.14784160017734393,
      "hash_read_seconds": 0.0,
      "index": 67,
      "load_excluding_hash_seconds": 0.210944099992048,
      "parse_json_seconds": 0.027089999988675117,
      "postprocess_seconds": 0.014386599999852479,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22835140000097454,
      "gzip_text_seconds": 0.14876799995545298,
      "hash_read_seconds": 0.0,
      "index": 68,
      "load_excluding_hash_seconds": 0.2150946000474505,
      "parse_json_seconds": 0.0268942000111565,
      "postprocess_seconds": 0.013256799953524023,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.2561188000254333,
      "gzip_text_seconds": 0.16263689997140318,
      "hash_read_seconds": 0.0,
      "index": 69,
      "load_excluding_hash_seconds": 0.23583809996489435,
      "parse_json_seconds": 0.027223800017964095,
      "postprocess_seconds": 0.020280700060538948,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22646559996064752,
      "gzip_text_seconds": 0.14448030019411817,
      "hash_read_seconds": 0.0,
      "index": 70,
      "load_excluding_hash_seconds": 0.2132839999976568,
      "parse_json_seconds": 0.027755999995861202,
      "postprocess_seconds": 0.013181599962990731,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24589080002624542,
      "gzip_text_seconds": 0.1608938998542726,
      "hash_read_seconds": 0.0,
      "index": 71,
      "load_excluding_hash_seconds": 0.22639860003255308,
      "parse_json_seconds": 0.02670899999793619,
      "postprocess_seconds": 0.01949219999369234,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.22370729997055605,
      "gzip_text_seconds": 0.14439520006999373,
      "hash_read_seconds": 0.0,
      "index": 72,
      "load_excluding_hash_seconds": 0.21066819998668507,
      "parse_json_seconds": 0.025808700011111796,
      "postprocess_seconds": 0.013039099983870983,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.27720559999579564,
      "gzip_text_seconds": 0.17532260005827993,
      "hash_read_seconds": 0.0,
      "index": 73,
      "load_excluding_hash_seconds": 0.25892679998651147,
      "parse_json_seconds": 0.034432000014930964,
      "postprocess_seconds": 0.01827880000928417,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24145289999432862,
      "gzip_text_seconds": 0.15463310008635744,
      "hash_read_seconds": 0.0,
      "index": 74,
      "load_excluding_hash_seconds": 0.2257898999378085,
      "parse_json_seconds": 0.02817269996739924,
      "postprocess_seconds": 0.015663000056520104,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.24304620001930743,
      "gzip_text_seconds": 0.15705529984552413,
      "hash_read_seconds": 0.0,
      "index": 75,
      "load_excluding_hash_seconds": 0.23060710000572726,
      "parse_json_seconds": 0.032434499997179955,
      "postprocess_seconds": 0.012439100013580173,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.250825299997814,
      "gzip_text_seconds": 0.16371689969673753,
      "hash_read_seconds": 0.0,
      "index": 76,
      "load_excluding_hash_seconds": 0.23417740006698295,
      "parse_json_seconds": 0.030504400026984513,
      "postprocess_seconds": 0.016647899930831045,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23256060003768653,
      "gzip_text_seconds": 0.15468040009727702,
      "hash_read_seconds": 0.0,
      "index": 77,
      "load_excluding_hash_seconds": 0.22028920002048835,
      "parse_json_seconds": 0.025435799965634942,
      "postprocess_seconds": 0.012271400017198175,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.26586340001085773,
      "gzip_text_seconds": 0.1487566001014784,
      "hash_read_seconds": 0.0,
      "index": 78,
      "load_excluding_hash_seconds": 0.21051629993598908,
      "parse_json_seconds": 0.025380299950484186,
      "postprocess_seconds": 0.05534710007486865,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.2416298000025563,
      "gzip_text_seconds": 0.15692780015524477,
      "hash_read_seconds": 0.0,
      "index": 79,
      "load_excluding_hash_seconds": 0.22899609996238723,
      "parse_json_seconds": 0.028415300010237843,
      "postprocess_seconds": 0.01263370004016906,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23242359998403117,
      "gzip_text_seconds": 0.15245299990056083,
      "hash_read_seconds": 0.0,
      "index": 80,
      "load_excluding_hash_seconds": 0.2189471999881789,
      "parse_json_seconds": 0.026863699953537434,
      "postprocess_seconds": 0.013476399995852262,
      "window": "that"
    },
    {
      "cd3_seconds": 0.0,
      "dataset": "Nezha-OB",
      "elapsed_seconds": 0.23754050000570714,
      "gzip_text_seconds": 0.15013429993996397,
      "hash_read_seconds": 0.0,
      "index": 81,
      "load_excluding_hash_seconds": 0.21951379993697628,
      "parse_json_seconds": 0.026934500026982278,
      "postprocess_seconds": 0.01802670006873086,
      "window": "that"
    }
  ]
}
```

### KB_reuse

```json
{
  "elapsed_seconds": 116.53011100000003,
  "gzip_text_seconds": 37.517521400295664,
  "hash_read_seconds": 0.1807629992836155,
  "load_excluding_hash_seconds": 110.96014379977714,
  "parity": "Exact bytes ban-ghi.jsonl, ce.json, sources.json; emulate Windows CRLF",
  "parse_json_seconds": 32.80629779933952,
  "peak_process_rss_bytes_since_start": 584794112,
  "rows": 410,
  "stage": "KB_reuse"
}
```

### Kết thúc phép đo

```json
{
  "PASS": true,
  "finished_utc": "2026-11-04T03:11:07.020425+00:00"
}
```

## Mã phép đo để tái lập

```python
import contextlib, gzip, io, json, platform, sys, time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
import psutil
import run_t11 as t11
import run_t12 as t12
import kb, chuan_bi
from m1 import doi_chung
OUT=t11.OUT
target=OUT/"dinh-chinh-luot-1.md"
assert not target.exists()
loads=json.loads
manifest=loads((OUT/"manifest.json").read_bytes())
digest=t11.digest
loader=t11.records
sha=chuan_bi.sha
gzip_open=gzip.open
cd3=doi_chung.cd3
process=psutil.Process()
fence=chr(96)*3
started=datetime.now(timezone.utc).isoformat()
def append(text):
    with target.open("a",encoding="utf-8",newline="\n") as stream:
        stream.write(text)
def json_block(value):
    return fence+"json\n"+json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n"+fence+"\n\n"
with target.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write("# T-051 — Đính chính sau phản biện lượt 1\n\n")
before=time.perf_counter()
for section in ("outputs","sources"):
    for name, expected in manifest[section].items():
        path=Path(name)
        if section=="sources" and name in ("docs/DECISIONS.md","tasks/T-051-t11-t12-va-kb/LOG.md"):
            continue
        assert path.stat().st_size==expected["bytes"] and digest(path)==expected["sha256"], name
append("## Biên nhận đo bổ sung lượt 2\n\n"+json_block({
    "started_utc":started,"python":sys.version,"platform":platform.platform(),
    "original_manifest_sha256":digest(OUT/"manifest.json"),"original_outputs_checked":261,
    "initial_hash_audit_seconds":time.perf_counter()-before,"one_process":True,
    "scope":"Same T11/T12 82 windows and KB 410 records, in memory, no raw telemetry or new scoring",
    "cache":"OS cache uncontrolled",
    "failed_attempt_1":"T11 75.618s PASS, T12 66.885s PASS; KB byte check failed because memory LF vs original Windows CRLF; detailed first-pass metrics not retained",
    "semantics":{
        "hash_read_seconds":"File read and SHA-256 in original helpers",
        "gzip_text_seconds":"Compressed file read, gzip decompression, UTF-8 decoding and line iteration",
        "parse_json_seconds":"JSON parsing inside records loader",
        "load_excluding_hash_seconds":"Record loader excluding hash duration",
        "postprocess_seconds":"Per-case elapsed minus record loader and hash",
        "cd3_seconds":"Subset of postprocessing",
        "peak_process_rss_bytes_since_start":"Cumulative Windows process high-water RSS",
        "elapsed_seconds":"Stage including source verification and equality checks, no output file generation or scoring"
    }}))
metrics=None
inside_loader=False
def timed(key, function):
    def call(*args,**kwargs):
        start=time.perf_counter()
        try: return function(*args,**kwargs)
        finally: metrics[key]+=time.perf_counter()-start
    return call
def parse(*args,**kwargs):
    start=time.perf_counter()
    try: return loads(*args,**kwargs)
    finally:
        if inside_loader: metrics["parse_json_seconds"]+=time.perf_counter()-start
class TextStream:
    def __init__(self,stream): self.stream=stream
    def __enter__(self): return self
    def __exit__(self,*args): self.stream.close()
    def __iter__(self): return self
    def __next__(self):
        start=time.perf_counter()
        try: return next(self.stream)
        finally: metrics["gzip_text_seconds"]+=time.perf_counter()-start
def open_gzip(*args,**kwargs): return TextStream(gzip_open(*args,**kwargs))
def records(*args):
    global inside_loader
    start=time.perf_counter()
    old=metrics["hash_read_seconds"]
    inside_loader=True
    try: return loader(*args)
    finally:
        inside_loader=False
        metrics["load_excluding_hash_seconds"]+=time.perf_counter()-start-(metrics["hash_read_seconds"]-old)
class MemoryFile(io.StringIO):
    def __init__(self,key,memory): super().__init__(); self.key=key; self.memory=memory
    def close(self):
        self.memory[self.key]=self.getvalue().replace("\n","\r\n").encode("utf-8")
        super().close()
class MemoryPath:
    def __init__(self,name,memory): self.name=name; self.memory=memory
    def __truediv__(self,part): return MemoryPath(self.name+"/"+part,self.memory)
    def mkdir(self): pass
    def open(self,mode,encoding=None):
        assert mode=="x" and self.name not in self.memory
        return MemoryFile(self.name,self.memory)
def measure(name,action):
    global metrics
    metrics=defaultdict(float)
    row={"stage":name}
    start=time.perf_counter()
    with contextlib.ExitStack() as stack:
        for module,attribute,replacement in (
            (chuan_bi,"sha",timed("hash_read_seconds",sha)),
            (t11,"digest",timed("hash_read_seconds",digest)),
            (t12,"digest",timed("hash_read_seconds",digest)),
            (kb,"digest",timed("hash_read_seconds",digest)),
            (gzip,"open",open_gzip),(json,"loads",parse),
            (t11,"records",records),(t12,"records",records),(kb,"records",records),
            (doi_chung,"cd3",timed("cd3_seconds",cd3)),
        ): stack.enter_context(patch.object(module,attribute,replacement))
        action(row,stack)
    row.update(metrics)
    row.update(elapsed_seconds=time.perf_counter()-start,
               peak_process_rss_bytes_since_start=process.memory_info().peak_wset)
    append("### "+name+"\n\n"+json_block(row))
    print(name,round(row["elapsed_seconds"],3),"PASS",flush=True)
def replay(row,stack,stage):
    entries,_=t11.source()
    static={}
    if stage=="T12":
        for dataset,(path,expected) in t12.STATIC.items():
            assert t11.digest(path)==expected
            static[dataset]={(e["source"],e["target"]) for e in t11.read(path)["edges"]}
    row["windows"]=[]
    for e in entries:
        filename=f"{e['index']:02d}.json"
        if stage=="T12":
            begin=time.perf_counter()
            baseline=t11.read(OUT/"t11-001"/filename)
            metrics["baseline_read_parse_seconds"]+=time.perf_counter()-begin
        initial=dict(metrics)
        begin=time.perf_counter()
        result=t11.case(e) if stage=="T11" else t12.case(e,baseline,False,static[e["job"]["dataset"]])
        elapsed=time.perf_counter()-begin
        path=OUT/("t11-001" if stage=="T11" else "t12-001")/filename
        assert digest(path)==manifest["outputs"][path.relative_to(t11.ROOT).as_posix()]["sha256"]
        saved=loads(path.read_bytes())
        if stage=="T12": result.pop("control_seconds"); saved.pop("control_seconds")
        check=time.perf_counter()
        assert t11.encoded(result)==t11.encoded(saved)
        metrics["parity_check_seconds"]+=time.perf_counter()-check
        delta={k:metrics[k]-initial.get(k,0) for k in ("hash_read_seconds","load_excluding_hash_seconds","gzip_text_seconds","parse_json_seconds","cd3_seconds")}
        row["windows"].append(dict(index=e["index"],dataset=e["job"]["dataset"],window=e["job"]["window"],
            elapsed_seconds=elapsed,postprocess_seconds=elapsed-delta["hash_read_seconds"]-delta["load_excluding_hash_seconds"],**delta))
        del result,saved
    row["parity"]="All fields equal, excluding runtime-only control_seconds in T12"
def reuse(row,stack):
    memory={}
    def save(path,value):
        assert path.name not in memory
        memory[path.name]=(t11.encoded(value)+"\r\n").encode("utf-8")
    def get_digest(path):
        if isinstance(path,MemoryPath):
            import hashlib
            return hashlib.sha256(memory[path.name]).hexdigest()
        return digest(path)
    stack.enter_context(patch.object(kb,"save",save))
    stack.enter_context(patch.object(kb,"digest",timed("hash_read_seconds",get_digest)))
    stack.enter_context(patch("builtins.print",lambda *a,**k:None))
    kb.phase1(MemoryPath("kb-memory",memory),OUT/"t12-001")
    for name in ("ban-ghi.jsonl","ce.json","sources.json"):
        assert memory["kb-memory/"+name]==(OUT/"kb-002"/name).read_bytes(),name
    row.update(rows=410,parity="Exact bytes ban-ghi.jsonl, ce.json, sources.json; emulate Windows CRLF")
measure("T11_replay",lambda row,stack: replay(row,stack,"T11"))
measure("T12_replay",lambda row,stack: replay(row,stack,"T12"))
measure("KB_reuse",reuse)
append("### Kết thúc phép đo\n\n"+json_block({"finished_utc":datetime.now(timezone.utc).isoformat(),"PASS":True}))
append("## Mã phép đo để tái lập\n\n"+fence+"python\n"+sys.orig_argv[-1]+"\n"+fence+"\n")
print("RECEIPT",target,flush=True)
```

## Tách riêng đọc, SHA-256 và giải nén byte

Lượt profiler phía trên đo đúng tổng lượt và hậu xử lý. Riêng hash_read_seconds chỉ bao các helper đã gắn đồng hồ ở mức module. Hàm sha mà records đã import trực tiếp chưa được bọc, nên cột đó chưa gồm hash bên trong records. load_excluding_hash_seconds thực tế vẫn gồm hash đó. Dùng phép đo trực tiếp dưới đây cho các cột đọc, SHA-256 và giải nén riêng. Giữ biên nhận profiler để truy vết, không cộng chéo hai lượt.

```json
{
  "PASS": true,
  "finish_utc": "2026-11-04T03:13:20.275238+00:00",
  "rows": [
    {
      "elapsed_seconds": 26.90105289994972,
      "file_reads": 164,
      "files": [
        {
          "bytes": 822599,
          "compressed_bytes": 822599,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.024309100001119077,
          "index": 0,
          "path": "results/T-053/runs/k-ec2-001-00/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005735000013373792,
          "sha256": "ed24a93ac64a50ea46a0aad7acc457e7eeb6e26874aabb3c759aa8838b040479",
          "sha256_seconds": 0.0007255999953486025,
          "uncompressed_bytes": 10658924,
          "window": "ce"
        },
        {
          "bytes": 10448405,
          "compressed_bytes": 10448405,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.29771270003402606,
          "index": 0,
          "path": "results/T-053/runs/k-ec2-001-00/trung-gian.jsonl.gz",
          "read_seconds": 0.004624399996828288,
          "sha256": "11e624246795f6810585f9d205d3c5a94ceda032433a994837b060057d58622d",
          "sha256_seconds": 0.00902009999845177,
          "uncompressed_bytes": 129551287,
          "window": "ce"
        },
        {
          "bytes": 1278473,
          "compressed_bytes": 1278473,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04298579995520413,
          "index": 1,
          "path": "results/T-053/runs/k-ec2-001-01/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008374000317417085,
          "sha256": "fedbceed8e99302b10cce269ad8f8b982599a85f8ad3b325952a546ab38096e8",
          "sha256_seconds": 0.00103859999217093,
          "uncompressed_bytes": 20993486,
          "window": "that"
        },
        {
          "bytes": 11200560,
          "compressed_bytes": 11200560,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3093006999697536,
          "index": 1,
          "path": "results/T-053/runs/k-ec2-001-01/trung-gian.jsonl.gz",
          "read_seconds": 0.005192200012970716,
          "sha256": "dc03fced5a2d1e8c29464cf65cd98db8faf4dbccf5c1689d5cac2c6a995c163f",
          "sha256_seconds": 0.011709699989296496,
          "uncompressed_bytes": 134712779,
          "window": "that"
        },
        {
          "bytes": 1029305,
          "compressed_bytes": 1029305,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.048038800014182925,
          "index": 2,
          "path": "results/T-053/runs/k-ec2-001-02/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004998999647796154,
          "sha256": "52800ca5a7bc6c2c54c944799978a6f3b987805aeaebf5c7b84c5152661a5b76",
          "sha256_seconds": 0.0009142000344581902,
          "uncompressed_bytes": 22105346,
          "window": "ce"
        },
        {
          "bytes": 11951000,
          "compressed_bytes": 11951000,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4006112999632023,
          "index": 2,
          "path": "results/T-053/runs/k-ec2-001-02/trung-gian.jsonl.gz",
          "read_seconds": 0.005242199986241758,
          "sha256": "8ce4f7944c842354f3e9dd08220d2b10f9892a9db369ee4314a825f387498c2e",
          "sha256_seconds": 0.00960220000706613,
          "uncompressed_bytes": 202647183,
          "window": "ce"
        },
        {
          "bytes": 1211073,
          "compressed_bytes": 1211073,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04675089998636395,
          "index": 3,
          "path": "results/T-053/runs/k-ec2-001-03/ban-ghi.jsonl.gz",
          "read_seconds": 0.000812100013718009,
          "sha256": "7445df065d08ef178514bfba728a02472507525e956b1ed129924281dd43c546",
          "sha256_seconds": 0.000983299978543073,
          "uncompressed_bytes": 23918820,
          "window": "that"
        },
        {
          "bytes": 12020473,
          "compressed_bytes": 12020473,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3954523000284098,
          "index": 3,
          "path": "results/T-053/runs/k-ec2-001-03/trung-gian.jsonl.gz",
          "read_seconds": 0.00558559998171404,
          "sha256": "337a08cac668ff83bfc10c2c1fc0f78a10bd36a2d91d870179d6c8bb78f5d7bb",
          "sha256_seconds": 0.009829699993133545,
          "uncompressed_bytes": 185688951,
          "window": "that"
        },
        {
          "bytes": 1301350,
          "compressed_bytes": 1301350,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06338529998902231,
          "index": 4,
          "path": "results/T-053/runs/k-ec2-001-04/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008817999623715878,
          "sha256": "716bdcf17af9aa5f5fdd43db5391d9184e5bc9b7df225eda6aeb601ae26f4df9",
          "sha256_seconds": 0.0010847999947145581,
          "uncompressed_bytes": 34024670,
          "window": "ce"
        },
        {
          "bytes": 13506076,
          "compressed_bytes": 13506076,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5657436999608763,
          "index": 4,
          "path": "results/T-053/runs/k-ec2-001-04/trung-gian.jsonl.gz",
          "read_seconds": 0.007091599982231855,
          "sha256": "528d6cf135e22cca572fe748b72cd783e99fa64ae3f1882dcf9b2a3517a4c73f",
          "sha256_seconds": 0.010985500004608184,
          "uncompressed_bytes": 273072439,
          "window": "ce"
        },
        {
          "bytes": 1506511,
          "compressed_bytes": 1506511,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07344369997736067,
          "index": 5,
          "path": "results/T-053/runs/k-ec2-001-05/ban-ghi.jsonl.gz",
          "read_seconds": 0.000994000001810491,
          "sha256": "06046b47c2f8b8573bbe0752d43dc914ff9d22135bdbf3ce98ecb8acad7e459d",
          "sha256_seconds": 0.0013927000109106302,
          "uncompressed_bytes": 39914943,
          "window": "that"
        },
        {
          "bytes": 14205823,
          "compressed_bytes": 14205823,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.6135507000144571,
          "index": 5,
          "path": "results/T-053/runs/k-ec2-001-05/trung-gian.jsonl.gz",
          "read_seconds": 0.006331299955490977,
          "sha256": "7da53b7268a273ca995e20c17dd5022d9cf9a6cbec98c2370147a222f035b21f",
          "sha256_seconds": 0.01229600002989173,
          "uncompressed_bytes": 291571079,
          "window": "that"
        },
        {
          "bytes": 848351,
          "compressed_bytes": 848351,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.025868400000035763,
          "index": 6,
          "path": "results/T-053/runs/k-laptop-001-06/ban-ghi.jsonl.gz",
          "read_seconds": 0.00045309995766729116,
          "sha256": "7d3a62322d7fa81e06f79cf7581c5502c7c9ae0ca1ae28e5e23d5b9cfb9278ec",
          "sha256_seconds": 0.000716600043233484,
          "uncompressed_bytes": 10436336,
          "window": "ce"
        },
        {
          "bytes": 10527125,
          "compressed_bytes": 10527125,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.29818990000057966,
          "index": 6,
          "path": "results/T-053/runs/k-laptop-001-06/trung-gian.jsonl.gz",
          "read_seconds": 0.0051642999751493335,
          "sha256": "2937f20e792bca64705880429da652c20efbdaafd52da542db37d32fe1e62fb9",
          "sha256_seconds": 0.00871189997997135,
          "uncompressed_bytes": 127666383,
          "window": "ce"
        },
        {
          "bytes": 912004,
          "compressed_bytes": 912004,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.026943199976813048,
          "index": 7,
          "path": "results/T-053/runs/k-ec2-001-07/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004971000016666949,
          "sha256": "3513ce7a7e0574d4f88e919de439ceaa8a4c99a956b85dfaa3c17ede8de7b413",
          "sha256_seconds": 0.0007700000423938036,
          "uncompressed_bytes": 11115592,
          "window": "that"
        },
        {
          "bytes": 10626311,
          "compressed_bytes": 10626311,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.30579860002035275,
          "index": 7,
          "path": "results/T-053/runs/k-ec2-001-07/trung-gian.jsonl.gz",
          "read_seconds": 0.005097599991131574,
          "sha256": "91fbf98ffc409b0ec72a7f3406875c91f3e437a566f135201e73f0a147efaef2",
          "sha256_seconds": 0.009878100012429059,
          "uncompressed_bytes": 122695627,
          "window": "that"
        },
        {
          "bytes": 1210453,
          "compressed_bytes": 1210453,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.052935399988200516,
          "index": 8,
          "path": "results/T-053/runs/k-laptop-001-08/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008025999995879829,
          "sha256": "6051c36119c0dd155ca24ff3eae9e13ba75dd39bbcff45271f091d344ec0678e",
          "sha256_seconds": 0.0010186000145040452,
          "uncompressed_bytes": 30070960,
          "window": "ce"
        },
        {
          "bytes": 13235549,
          "compressed_bytes": 13235549,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.48666080000111833,
          "index": 8,
          "path": "results/T-053/runs/k-laptop-001-08/trung-gian.jsonl.gz",
          "read_seconds": 0.007567100052256137,
          "sha256": "a45364647592d150571c8d9f7fb88c716bcfe73788bbcd8e8179f9cb8d43e1f7",
          "sha256_seconds": 0.010905900038778782,
          "uncompressed_bytes": 255235467,
          "window": "ce"
        },
        {
          "bytes": 1529752,
          "compressed_bytes": 1529752,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07321060000685975,
          "index": 9,
          "path": "results/T-053/runs/k-ec2-001-09/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011748000397346914,
          "sha256": "8f4bee30671bebe3b4bdf2da6fa19bb4e1e31827ec1d738e0a09ef82b8293842",
          "sha256_seconds": 0.0018285000114701688,
          "uncompressed_bytes": 38415928,
          "window": "that"
        },
        {
          "bytes": 13632831,
          "compressed_bytes": 13632831,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5257086000056006,
          "index": 9,
          "path": "results/T-053/runs/k-ec2-001-09/trung-gian.jsonl.gz",
          "read_seconds": 0.006555299973115325,
          "sha256": "d7104f3bce70ce239bf581de094f64d29b73e179e3ae84759fec1e57d738970a",
          "sha256_seconds": 0.011042900034226477,
          "uncompressed_bytes": 261436987,
          "window": "that"
        },
        {
          "bytes": 1202287,
          "compressed_bytes": 1202287,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06866310001350939,
          "index": 10,
          "path": "results/T-053/runs/k-laptop-001-10/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008866999996826053,
          "sha256": "fc45a2d498a59663275e97874c9b7162b366ed702deff44747d709acec6aab41",
          "sha256_seconds": 0.0010926999966613948,
          "uncompressed_bytes": 29958852,
          "window": "ce"
        },
        {
          "bytes": 12988601,
          "compressed_bytes": 12988601,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4988273999770172,
          "index": 10,
          "path": "results/T-053/runs/k-laptop-001-10/trung-gian.jsonl.gz",
          "read_seconds": 0.007321399985812604,
          "sha256": "4682bb3ba56c94601ea6029ec7b2c011d4c246e252c5da8b3422d6af92fb5a5b",
          "sha256_seconds": 0.010853799991309643,
          "uncompressed_bytes": 251420055,
          "window": "ce"
        },
        {
          "bytes": 1454832,
          "compressed_bytes": 1454832,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.08145280001917854,
          "index": 11,
          "path": "results/T-053/runs/k-ec2-001-11/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011208000360056758,
          "sha256": "81992f23e8535f8dbb03457e388d89507a687523b6e15cb31df191d96fa46227",
          "sha256_seconds": 0.0014058999950066209,
          "uncompressed_bytes": 34263366,
          "window": "that"
        },
        {
          "bytes": 13258617,
          "compressed_bytes": 13258617,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.46641799999633804,
          "index": 11,
          "path": "results/T-053/runs/k-ec2-001-11/trung-gian.jsonl.gz",
          "read_seconds": 0.006693199975416064,
          "sha256": "3ea36301fb68ea1500138570f3b892e6a3fb90cdd8d2af2ac499b7adb8c9c9ca",
          "sha256_seconds": 0.010994000011123717,
          "uncompressed_bytes": 236970003,
          "window": "that"
        },
        {
          "bytes": 1225981,
          "compressed_bytes": 1225981,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.047435699962079525,
          "index": 12,
          "path": "results/T-053/runs/k-laptop-001-12/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008258000016212463,
          "sha256": "77364ade249f19b3ea86a0ebe18732c97a57d36a5263b5daf3b765b931008549",
          "sha256_seconds": 0.0010110000148415565,
          "uncompressed_bytes": 25913566,
          "window": "ce"
        },
        {
          "bytes": 12796748,
          "compressed_bytes": 12796748,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4832678000093438,
          "index": 12,
          "path": "results/T-053/runs/k-laptop-001-12/trung-gian.jsonl.gz",
          "read_seconds": 0.006611699995119125,
          "sha256": "462f6413a5578f5dd5e5c46eae73ce799167103099a9c80bed8a1f80b159353a",
          "sha256_seconds": 0.014863000018522143,
          "uncompressed_bytes": 217715263,
          "window": "ce"
        },
        {
          "bytes": 1462493,
          "compressed_bytes": 1462493,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05971450003562495,
          "index": 13,
          "path": "results/T-053/runs/k-ec2-001-13/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011211999808438122,
          "sha256": "a9a652093633b37079859a759d4e1c2c331097fd4fa9b62a6e1ecdd9a27920ff",
          "sha256_seconds": 0.0011031999601982534,
          "uncompressed_bytes": 31360092,
          "window": "that"
        },
        {
          "bytes": 13021903,
          "compressed_bytes": 13021903,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.44313299999339506,
          "index": 13,
          "path": "results/T-053/runs/k-ec2-001-13/trung-gian.jsonl.gz",
          "read_seconds": 0.005924800003413111,
          "sha256": "8dc9ac77f7ef04f0d916237a8d026d3e6bcddcd0842a054d3d14b74828ca9227",
          "sha256_seconds": 0.010854699998162687,
          "uncompressed_bytes": 213662183,
          "window": "that"
        },
        {
          "bytes": 577147,
          "compressed_bytes": 577147,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015526600007433444,
          "index": 14,
          "path": "results/T-053/runs/k-laptop-001-14/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003828000044450164,
          "sha256": "1f53468d8c7d30bc4d60c52e6b75d74f00cc3821ba68c24ad0cca89777e42203",
          "sha256_seconds": 0.0004763000179082155,
          "uncompressed_bytes": 4873430,
          "window": "ce"
        },
        {
          "bytes": 8793133,
          "compressed_bytes": 8793133,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21706470003118739,
          "index": 14,
          "path": "results/T-053/runs/k-laptop-001-14/trung-gian.jsonl.gz",
          "read_seconds": 0.004397100012283772,
          "sha256": "b826ba03189af82b66b5c85904a9803184be178c0c6815c74d1ed69e665f69aa",
          "sha256_seconds": 0.007161500048823655,
          "uncompressed_bytes": 86528619,
          "window": "ce"
        },
        {
          "bytes": 697723,
          "compressed_bytes": 697723,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.019065800006501377,
          "index": 15,
          "path": "results/T-053/runs/k-ec2-001-15/ban-ghi.jsonl.gz",
          "read_seconds": 0.00043839996214956045,
          "sha256": "44e06790d2d897a589e11f677813b1f7b10a29443d308703829e04867b2fc6cf",
          "sha256_seconds": 0.0005721999914385378,
          "uncompressed_bytes": 6738444,
          "window": "that"
        },
        {
          "bytes": 9055563,
          "compressed_bytes": 9055563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21888230001786724,
          "index": 15,
          "path": "results/T-053/runs/k-ec2-001-15/trung-gian.jsonl.gz",
          "read_seconds": 0.004233699990436435,
          "sha256": "23b1a85437c84b17676466b4d474b96c7b067a2891a31e644a1dcc079b1806f4",
          "sha256_seconds": 0.007522800005972385,
          "uncompressed_bytes": 87378743,
          "window": "that"
        },
        {
          "bytes": 1210062,
          "compressed_bytes": 1210062,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.053603700012899935,
          "index": 16,
          "path": "results/T-053/runs/k-ec2-001-16/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007937999907881021,
          "sha256": "ce03562948dec6729110e499039c9791a6b0d5acaccab061f555d98b873f261c",
          "sha256_seconds": 0.0009969999664463103,
          "uncompressed_bytes": 30948408,
          "window": "ce"
        },
        {
          "bytes": 13026484,
          "compressed_bytes": 13026484,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4818508999887854,
          "index": 16,
          "path": "results/T-053/runs/k-ec2-001-16/trung-gian.jsonl.gz",
          "read_seconds": 0.005958399968221784,
          "sha256": "dcdababff7ef122b9acbbfb1c541ff20becbf0510384bf0b6e41f758ce6434a3",
          "sha256_seconds": 0.01097559998743236,
          "uncompressed_bytes": 259912347,
          "window": "ce"
        },
        {
          "bytes": 1601811,
          "compressed_bytes": 1601811,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06046619999688119,
          "index": 17,
          "path": "results/T-053/runs/k-ec2-001-17/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009286999702453613,
          "sha256": "2cf9afbac2b3c8cdc4c382aae3032aa0c356032f65912a31792419f474cbfbeb",
          "sha256_seconds": 0.0012879000278189778,
          "uncompressed_bytes": 32437146,
          "window": "that"
        },
        {
          "bytes": 11856068,
          "compressed_bytes": 11856068,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.36848569998983294,
          "index": 17,
          "path": "results/T-053/runs/k-ec2-001-17/trung-gian.jsonl.gz",
          "read_seconds": 0.00548629998229444,
          "sha256": "12ef2bbe14f73b0f7fccbed9ea20666a60ec9642d3461ee1d15a6d29f4e0a933",
          "sha256_seconds": 0.009703300020191818,
          "uncompressed_bytes": 175977559,
          "window": "that"
        },
        {
          "bytes": 1056011,
          "compressed_bytes": 1056011,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04517689999192953,
          "index": 18,
          "path": "results/T-053/runs/k-laptop-001-18/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008455000352114439,
          "sha256": "a58cbe37868ac806fa277eda558df530dd9f29cbfc3d6d7724c6b65db08b5dfa",
          "sha256_seconds": 0.0007757999701425433,
          "uncompressed_bytes": 20764174,
          "window": "ce"
        },
        {
          "bytes": 12047687,
          "compressed_bytes": 12047687,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.38912529998924583,
          "index": 18,
          "path": "results/T-053/runs/k-laptop-001-18/trung-gian.jsonl.gz",
          "read_seconds": 0.00689250003779307,
          "sha256": "d415b17115dde04e3dbcd0b173ae35d2ffb397e835f05d23f2b5f396da4dd058",
          "sha256_seconds": 0.010228700004518032,
          "uncompressed_bytes": 191215491,
          "window": "ce"
        },
        {
          "bytes": 1437712,
          "compressed_bytes": 1437712,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0645896999631077,
          "index": 19,
          "path": "results/T-053/runs/k-laptop-001-19/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008842000388540328,
          "sha256": "d6d49b9203bb9d7b52aeb5b30f9722a616f40c49d2389c5717a21299741636b7",
          "sha256_seconds": 0.001172300020698458,
          "uncompressed_bytes": 32908784,
          "window": "that"
        },
        {
          "bytes": 13174562,
          "compressed_bytes": 13174562,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4526064000092447,
          "index": 19,
          "path": "results/T-053/runs/k-laptop-001-19/trung-gian.jsonl.gz",
          "read_seconds": 0.005832199996802956,
          "sha256": "5e7ce74f99932de6a8485552b3caba2a701b15946a5ef1c1472518f973c3bcc5",
          "sha256_seconds": 0.010625000053551048,
          "uncompressed_bytes": 231525955,
          "window": "that"
        },
        {
          "bytes": 1078891,
          "compressed_bytes": 1078891,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03572589997202158,
          "index": 20,
          "path": "results/T-053/runs/k-laptop-001-20/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008693999843671918,
          "sha256": "44a2c2ca61ee06102b40d97b4105b9fd1871d25c442b06fcbf68be36ec7363f2",
          "sha256_seconds": 0.0008824000251479447,
          "uncompressed_bytes": 17297772,
          "window": "ce"
        },
        {
          "bytes": 11535920,
          "compressed_bytes": 11535920,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3376760999672115,
          "index": 20,
          "path": "results/T-053/runs/k-laptop-001-20/trung-gian.jsonl.gz",
          "read_seconds": 0.005268100008834153,
          "sha256": "7c26270a80ddca65ce9af26d5d3176f5a0fbd0129b8de13c59099379970f078b",
          "sha256_seconds": 0.009284499974455684,
          "uncompressed_bytes": 155876335,
          "window": "ce"
        },
        {
          "bytes": 1308686,
          "compressed_bytes": 1308686,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.049544200010132045,
          "index": 21,
          "path": "results/T-053/runs/k-laptop-001-21/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008496000082232058,
          "sha256": "a93fa7657385f244c979e512cde318a4c77d6adbaf46175b6ce322478a0a7a01",
          "sha256_seconds": 0.00106380000943318,
          "uncompressed_bytes": 25272765,
          "window": "that"
        },
        {
          "bytes": 12247809,
          "compressed_bytes": 12247809,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.38465580000774935,
          "index": 21,
          "path": "results/T-053/runs/k-laptop-001-21/trung-gian.jsonl.gz",
          "read_seconds": 0.006251599988900125,
          "sha256": "02343f06330aeffb2cf02bcceee5bcf31df5fee844643c071684cf7b7e61ae27",
          "sha256_seconds": 0.010750599962193519,
          "uncompressed_bytes": 183184571,
          "window": "that"
        },
        {
          "bytes": 1167638,
          "compressed_bytes": 1167638,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04507009999360889,
          "index": 22,
          "path": "results/T-053/runs/k-ec2-001-22/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008738000178709626,
          "sha256": "2b4c9c639393e2db909054671363d72a3d1344f0b36c921c4307715d6b60d517",
          "sha256_seconds": 0.001000799995381385,
          "uncompressed_bytes": 23457226,
          "window": "ce"
        },
        {
          "bytes": 12337820,
          "compressed_bytes": 12337820,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.43911879998631775,
          "index": 22,
          "path": "results/T-053/runs/k-ec2-001-22/trung-gian.jsonl.gz",
          "read_seconds": 0.006237399997189641,
          "sha256": "c7848f76949bef5f5d0c4c3932c8d61611e2b1108a347eb5530d70c88f008d1a",
          "sha256_seconds": 0.010189900000113994,
          "uncompressed_bytes": 201534451,
          "window": "ce"
        },
        {
          "bytes": 1524153,
          "compressed_bytes": 1524153,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06488379999063909,
          "index": 23,
          "path": "results/T-053/runs/k-laptop-001-23/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008986000320874155,
          "sha256": "84bc08057e635bed81733346a377457e85ffd62fbdd045f8c7a7f5db45e6da19",
          "sha256_seconds": 0.0012320000096224248,
          "uncompressed_bytes": 30628016,
          "window": "that"
        },
        {
          "bytes": 12651563,
          "compressed_bytes": 12651563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3997656000428833,
          "index": 23,
          "path": "results/T-053/runs/k-laptop-001-23/trung-gian.jsonl.gz",
          "read_seconds": 0.005652200023178011,
          "sha256": "825c8cc75c8f7815247112c00369e899cb5bf7352e4fbeae994447f494175434",
          "sha256_seconds": 0.010436300013680011,
          "uncompressed_bytes": 195483455,
          "window": "that"
        },
        {
          "bytes": 1032006,
          "compressed_bytes": 1032006,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03718189999926835,
          "index": 24,
          "path": "results/T-053/runs/k-laptop-001-24/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006113999988883734,
          "sha256": "d4a806c8cc51c8964d06ec88d1624e4e5c20275fbe77eea59a25f40eb5abd4c7",
          "sha256_seconds": 0.0009298999793827534,
          "uncompressed_bytes": 18208454,
          "window": "ce"
        },
        {
          "bytes": 11749340,
          "compressed_bytes": 11749340,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3829498999984935,
          "index": 24,
          "path": "results/T-053/runs/k-laptop-001-24/trung-gian.jsonl.gz",
          "read_seconds": 0.005584899976383895,
          "sha256": "959e3d6c62df4d2206896a7c1090edfcff818a07726a3be1957820e94bfa32e8",
          "sha256_seconds": 0.009719900030177087,
          "uncompressed_bytes": 170164895,
          "window": "ce"
        },
        {
          "bytes": 1120525,
          "compressed_bytes": 1120525,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04886769998120144,
          "index": 25,
          "path": "results/T-053/runs/k-laptop-001-25/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008972000214271247,
          "sha256": "52af893eaa19504b750286bc8ce5122956a0140a21d2b57bca73a65226c700c5",
          "sha256_seconds": 0.0010435999720357358,
          "uncompressed_bytes": 25257224,
          "window": "that"
        },
        {
          "bytes": 12510563,
          "compressed_bytes": 12510563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.43633309996221215,
          "index": 25,
          "path": "results/T-053/runs/k-laptop-001-25/trung-gian.jsonl.gz",
          "read_seconds": 0.005817500001285225,
          "sha256": "750efebe9210bc0fa18e90e469b06fd84731303a7d5880f68d8ac22b91e408e3",
          "sha256_seconds": 0.01066600001649931,
          "uncompressed_bytes": 220682353,
          "window": "that"
        },
        {
          "bytes": 1014977,
          "compressed_bytes": 1014977,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03815179999219254,
          "index": 26,
          "path": "results/T-053/runs/k-ec2-001-26/ban-ghi.jsonl.gz",
          "read_seconds": 0.00048700004117563367,
          "sha256": "866a6e7f15d819eaca48da5afed9fb46c7fd80b6c9b6872b644d1473f93f963f",
          "sha256_seconds": 0.0008211999665945768,
          "uncompressed_bytes": 19463466,
          "window": "ce"
        },
        {
          "bytes": 11785721,
          "compressed_bytes": 11785721,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.41074200003640726,
          "index": 26,
          "path": "results/T-053/runs/k-ec2-001-26/trung-gian.jsonl.gz",
          "read_seconds": 0.00576500000897795,
          "sha256": "c0fb374852e13a403ed0349a3b9234232b2e48eb5c28bb07dfc1de8fc739f64f",
          "sha256_seconds": 0.009746499999891967,
          "uncompressed_bytes": 182660367,
          "window": "ce"
        },
        {
          "bytes": 1021014,
          "compressed_bytes": 1021014,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04804690001765266,
          "index": 27,
          "path": "results/T-053/runs/k-laptop-001-27/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004680999554693699,
          "sha256": "1a330a7886f6957d92f01afbedca6c6af4a6fe196f77d839452ae66016d1dc01",
          "sha256_seconds": 0.0008252999978139997,
          "uncompressed_bytes": 18377695,
          "window": "that"
        },
        {
          "bytes": 11577590,
          "compressed_bytes": 11577590,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.365722700022161,
          "index": 27,
          "path": "results/T-053/runs/k-laptop-001-27/trung-gian.jsonl.gz",
          "read_seconds": 0.005468400020617992,
          "sha256": "429e32bacd9af45367f907b98817bd2290bc3b32aca8ae54de37b2bdf25738ab",
          "sha256_seconds": 0.009851900045759976,
          "uncompressed_bytes": 173121647,
          "window": "that"
        },
        {
          "bytes": 1042539,
          "compressed_bytes": 1042539,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.034618199977558106,
          "index": 28,
          "path": "results/T-053/runs/k-laptop-001-28/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004963999963365495,
          "sha256": "f85eba05d5af1e864791a9fbfb8d2ddd14f3277000874b8c3ad3ad65aff8db0c",
          "sha256_seconds": 0.0008439999655820429,
          "uncompressed_bytes": 16110688,
          "window": "ce"
        },
        {
          "bytes": 11541406,
          "compressed_bytes": 11541406,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.363496900012251,
          "index": 28,
          "path": "results/T-053/runs/k-laptop-001-28/trung-gian.jsonl.gz",
          "read_seconds": 0.005095600034110248,
          "sha256": "afcbead493de06b41b4b10f1c76f6ddefbfe77e75e279d01f9dfc2c8a0780334",
          "sha256_seconds": 0.009288899949751794,
          "uncompressed_bytes": 157105339,
          "window": "ce"
        },
        {
          "bytes": 1624620,
          "compressed_bytes": 1624620,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.062303800019435585,
          "index": 29,
          "path": "results/T-053/runs/k-laptop-001-29/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010831999825313687,
          "sha256": "1af2a35edbe4f969ad057837f5ae2694240764e289ce22d7dfa708818eefec80",
          "sha256_seconds": 0.0013651000335812569,
          "uncompressed_bytes": 32677978,
          "window": "that"
        },
        {
          "bytes": 12330215,
          "compressed_bytes": 12330215,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.37842989998171106,
          "index": 29,
          "path": "results/T-053/runs/k-laptop-001-29/trung-gian.jsonl.gz",
          "read_seconds": 0.005683700030203909,
          "sha256": "a2a38682c2811c22fbd5accb650dcd85f851454936c5bc53b0bd6494b22dae62",
          "sha256_seconds": 0.011333499976899475,
          "uncompressed_bytes": 175000963,
          "window": "that"
        },
        {
          "bytes": 1178865,
          "compressed_bytes": 1178865,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.047074500005692244,
          "index": 30,
          "path": "results/T-053/runs/k-ec2-001-30/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008420999511145055,
          "sha256": "1fbe92925b4fbdee41bb2f79e56bfa89191d7610a47ab3ce5e7597412b714aee",
          "sha256_seconds": 0.0010156999924220145,
          "uncompressed_bytes": 24507156,
          "window": "ce"
        },
        {
          "bytes": 12647668,
          "compressed_bytes": 12647668,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4279596999986097,
          "index": 30,
          "path": "results/T-053/runs/k-ec2-001-30/trung-gian.jsonl.gz",
          "read_seconds": 0.006580600049346685,
          "sha256": "ab446e32a91c9b81972e0b4df052cf0e7ad1a737e553cc4a44d4ce38c939002b",
          "sha256_seconds": 0.010778199997730553,
          "uncompressed_bytes": 214430531,
          "window": "ce"
        },
        {
          "bytes": 1901118,
          "compressed_bytes": 1901118,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.08405519998632371,
          "index": 31,
          "path": "results/T-053/runs/k-laptop-001-31/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010982999810948968,
          "sha256": "f0213ca394440f971a728586edc7ff5fb7e559a50795516e6ec1131033962fd4",
          "sha256_seconds": 0.0015913000097498298,
          "uncompressed_bytes": 44220284,
          "window": "that"
        },
        {
          "bytes": 13015137,
          "compressed_bytes": 13015137,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4185467000352219,
          "index": 31,
          "path": "results/T-053/runs/k-laptop-001-31/trung-gian.jsonl.gz",
          "read_seconds": 0.006211600033566356,
          "sha256": "fbb28c90630eedbce15e40488f38b531b43cfd99ee61057bb75b4acd5243b79e",
          "sha256_seconds": 0.011320699995849282,
          "uncompressed_bytes": 214444619,
          "window": "that"
        },
        {
          "bytes": 1018853,
          "compressed_bytes": 1018853,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.034332700015511364,
          "index": 32,
          "path": "results/T-053/runs/k-laptop-001-32/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004929000278934836,
          "sha256": "ad779224f744eca63e6af5f577a517b6885f83bd9ce9a1b8a133d128b3641dd8",
          "sha256_seconds": 0.0009201000211760402,
          "uncompressed_bytes": 16421004,
          "window": "ce"
        },
        {
          "bytes": 11306390,
          "compressed_bytes": 11306390,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3602778000058606,
          "index": 32,
          "path": "results/T-053/runs/k-laptop-001-32/trung-gian.jsonl.gz",
          "read_seconds": 0.005140000022947788,
          "sha256": "371d2fe7d4a36234213b967d6211a4103a382378c2ba84f858787890bc0395d3",
          "sha256_seconds": 0.009251800016500056,
          "uncompressed_bytes": 154181995,
          "window": "ce"
        },
        {
          "bytes": 1727868,
          "compressed_bytes": 1727868,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06266470003174618,
          "index": 33,
          "path": "results/T-053/runs/k-laptop-001-33/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011557999532669783,
          "sha256": "d4422c480465b5b54d81e115d0e756706b5f5d45ca9a90f1a46f308f0f4ef259",
          "sha256_seconds": 0.0014510000473819673,
          "uncompressed_bytes": 32202962,
          "window": "that"
        },
        {
          "bytes": 12081207,
          "compressed_bytes": 12081207,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.36504310002783313,
          "index": 33,
          "path": "results/T-053/runs/k-laptop-001-33/trung-gian.jsonl.gz",
          "read_seconds": 0.00550570001360029,
          "sha256": "63d0714383e3ecc7ddf60c1c5c0246a28d72d30a0a30d16b1bbab80a13f3c55c",
          "sha256_seconds": 0.010835099965333939,
          "uncompressed_bytes": 161559683,
          "window": "that"
        },
        {
          "bytes": 987783,
          "compressed_bytes": 987783,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03416139999171719,
          "index": 34,
          "path": "results/T-053/runs/k-ec2-001-34/ban-ghi.jsonl.gz",
          "read_seconds": 0.00044329999946057796,
          "sha256": "1deb8b14faeab25e4b6dfc2a3bde4d9730835492dbe7507378e07c5db35d1927",
          "sha256_seconds": 0.000798800028860569,
          "uncompressed_bytes": 16427664,
          "window": "ce"
        },
        {
          "bytes": 11232270,
          "compressed_bytes": 11232270,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.34190130000934005,
          "index": 34,
          "path": "results/T-053/runs/k-ec2-001-34/trung-gian.jsonl.gz",
          "read_seconds": 0.00503900001058355,
          "sha256": "bcb8aa973d34bcd5c2b801fa560784d7c9e43b0c4cd249562fb5791a60814b0e",
          "sha256_seconds": 0.009561600047163665,
          "uncompressed_bytes": 155921331,
          "window": "ce"
        },
        {
          "bytes": 2029706,
          "compressed_bytes": 2029706,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06982709997100756,
          "index": 35,
          "path": "results/T-053/runs/k-laptop-001-35/ban-ghi.jsonl.gz",
          "read_seconds": 0.001126500021200627,
          "sha256": "6fad7d180800c32d3ebb3c771a6b8caa4a1ae3879cac28f3956b523dc6995ac5",
          "sha256_seconds": 0.0016243999707512558,
          "uncompressed_bytes": 36896487,
          "window": "that"
        },
        {
          "bytes": 12213410,
          "compressed_bytes": 12213410,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.35799569997470826,
          "index": 35,
          "path": "results/T-053/runs/k-laptop-001-35/trung-gian.jsonl.gz",
          "read_seconds": 0.005532399984076619,
          "sha256": "14395cac23a72f46fe2d1683b90db30554fe10b683cfb8a926d38a0746c18a8a",
          "sha256_seconds": 0.010196099989116192,
          "uncompressed_bytes": 158345679,
          "window": "that"
        },
        {
          "bytes": 1314711,
          "compressed_bytes": 1314711,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04015409998828545,
          "index": 36,
          "path": "results/T-053/runs/k-laptop-001-36/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008142000297084451,
          "sha256": "598c3a9d6adbe11572162eb56b0df3c9b71ec6f5ecbdccbf6d2d14ecc448a5d7",
          "sha256_seconds": 0.001059899979736656,
          "uncompressed_bytes": 18610066,
          "window": "ce"
        },
        {
          "bytes": 10925820,
          "compressed_bytes": 10925820,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3086498000193387,
          "index": 36,
          "path": "results/T-053/runs/k-laptop-001-36/trung-gian.jsonl.gz",
          "read_seconds": 0.004865099966991693,
          "sha256": "854ea2603f3f2d3fd0b51b039daeda31bb485c7d06affb6774de4d6482c85a8e",
          "sha256_seconds": 0.008674200042150915,
          "uncompressed_bytes": 118188339,
          "window": "ce"
        },
        {
          "bytes": 1216962,
          "compressed_bytes": 1216962,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04429869999876246,
          "index": 37,
          "path": "results/T-053/runs/k-laptop-001-37/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007945999968796968,
          "sha256": "e72f64ab11adf9aad4919b624f614143a6d8eb0815519773397585d515d89b74",
          "sha256_seconds": 0.0009883000166155398,
          "uncompressed_bytes": 16457582,
          "window": "that"
        },
        {
          "bytes": 11071929,
          "compressed_bytes": 11071929,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3130058000097051,
          "index": 37,
          "path": "results/T-053/runs/k-laptop-001-37/trung-gian.jsonl.gz",
          "read_seconds": 0.007747999974526465,
          "sha256": "491707df7e47f765ec4059326b2a4a8b4a976ee3d357c0bcf51ca9e17a5ef03c",
          "sha256_seconds": 0.01098770002136007,
          "uncompressed_bytes": 124267547,
          "window": "that"
        },
        {
          "bytes": 968714,
          "compressed_bytes": 968714,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.034533799975179136,
          "index": 38,
          "path": "results/T-053/runs/k-ec2-001-38/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004743000026792288,
          "sha256": "8bd4dd2c03658b39309474aa68135b5f48d3e13849d012b76bb6ba3b4eacb4eb",
          "sha256_seconds": 0.0007846999797038734,
          "uncompressed_bytes": 15740140,
          "window": "ce"
        },
        {
          "bytes": 11166023,
          "compressed_bytes": 11166023,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3359961000387557,
          "index": 38,
          "path": "results/T-053/runs/k-ec2-001-38/trung-gian.jsonl.gz",
          "read_seconds": 0.005196899990551174,
          "sha256": "b9e9a75d02c5918622abb4652a98748a8264c6ffc328a0049bd26f08b5230d9a",
          "sha256_seconds": 0.009212100005242974,
          "uncompressed_bytes": 153532697,
          "window": "ce"
        },
        {
          "bytes": 2194356,
          "compressed_bytes": 2194356,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.08393470000009984,
          "index": 39,
          "path": "results/T-053/runs/k-laptop-001-39/ban-ghi.jsonl.gz",
          "read_seconds": 0.0012424999731592834,
          "sha256": "56df5f3e5e86728344887a5a3f05bd61b8147223f23444fda4ae088cb4d5df7e",
          "sha256_seconds": 0.0018395999795757234,
          "uncompressed_bytes": 42532030,
          "window": "that"
        },
        {
          "bytes": 12394216,
          "compressed_bytes": 12394216,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.40724240004783496,
          "index": 39,
          "path": "results/T-053/runs/k-laptop-001-39/trung-gian.jsonl.gz",
          "read_seconds": 0.005685799987986684,
          "sha256": "9185ed0b2ff8b1d23ecdec7221183243b348080a088987c665f57dbddbd9bb3a",
          "sha256_seconds": 0.010178500029724091,
          "uncompressed_bytes": 168836655,
          "window": "that"
        },
        {
          "bytes": 1233079,
          "compressed_bytes": 1233079,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.051794699975289404,
          "index": 40,
          "path": "results/T-053/runs/k-laptop-001-40/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008527000318281353,
          "sha256": "622e790f6ca76d3a6034cd87133655d1adee14252f676041abd368154c5284c3",
          "sha256_seconds": 0.0010995999909937382,
          "uncompressed_bytes": 17431184,
          "window": "ce"
        },
        {
          "bytes": 10735191,
          "compressed_bytes": 10735191,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.29539030004525557,
          "index": 40,
          "path": "results/T-053/runs/k-laptop-001-40/trung-gian.jsonl.gz",
          "read_seconds": 0.006070299947168678,
          "sha256": "a35666f870bb42c4373f65d07bd990722a9ce37afaa89a85648d075e395255cf",
          "sha256_seconds": 0.009216000034939498,
          "uncompressed_bytes": 120368383,
          "window": "ce"
        },
        {
          "bytes": 1450045,
          "compressed_bytes": 1450045,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04586640000343323,
          "index": 41,
          "path": "results/T-053/runs/k-laptop-001-41/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010652000200934708,
          "sha256": "3c2570c53e1f84106b07c5fcfcedde3fbb147cd0fb21708c73efee0e2bfa3f9c",
          "sha256_seconds": 0.0012146999943070114,
          "uncompressed_bytes": 22395444,
          "window": "that"
        },
        {
          "bytes": 11305153,
          "compressed_bytes": 11305153,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3047093999921344,
          "index": 41,
          "path": "results/T-053/runs/k-laptop-001-41/trung-gian.jsonl.gz",
          "read_seconds": 0.005045199999585748,
          "sha256": "98631360b15819ef89c13568d0c5b373331e7becb1d15e3b138f877e86db1c88",
          "sha256_seconds": 0.009248599992133677,
          "uncompressed_bytes": 125650075,
          "window": "that"
        },
        {
          "bytes": 1183524,
          "compressed_bytes": 1183524,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03708360000746325,
          "index": 42,
          "path": "results/T-053/runs/k-ec2-001-42/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008781999931670725,
          "sha256": "22297a9a6b4139043ced3a2edfc318d92fa176bc32307ed7c9238aae5839d418",
          "sha256_seconds": 0.0009809000184759498,
          "uncompressed_bytes": 15832522,
          "window": "ce"
        },
        {
          "bytes": 10598076,
          "compressed_bytes": 10598076,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.277933600009419,
          "index": 42,
          "path": "results/T-053/runs/k-ec2-001-42/trung-gian.jsonl.gz",
          "read_seconds": 0.005548099987208843,
          "sha256": "f94fa0f3a23e9a4fb3ec78551db8b1a37fcb49ebb4eb5f8afa3159d7250820e6",
          "sha256_seconds": 0.009112700005061924,
          "uncompressed_bytes": 114154819,
          "window": "ce"
        },
        {
          "bytes": 1158621,
          "compressed_bytes": 1158621,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0387877999455668,
          "index": 43,
          "path": "results/T-053/runs/k-laptop-001-43/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007600000244565308,
          "sha256": "d344459e6c3caef324fe0f4bdcce249391e6c2c3a239a6492946c0687abbf145",
          "sha256_seconds": 0.0009477999992668629,
          "uncompressed_bytes": 15323968,
          "window": "that"
        },
        {
          "bytes": 10915175,
          "compressed_bytes": 10915175,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2933601000113413,
          "index": 43,
          "path": "results/T-053/runs/k-laptop-001-43/trung-gian.jsonl.gz",
          "read_seconds": 0.005153300007805228,
          "sha256": "2fbdd6ac11435f2bdb30edc23b1df1c9ad9e67660a3b45809a242b9bcdfe423c",
          "sha256_seconds": 0.008890099998097867,
          "uncompressed_bytes": 120626663,
          "window": "that"
        },
        {
          "bytes": 994092,
          "compressed_bytes": 994092,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03159819997381419,
          "index": 44,
          "path": "results/T-053/runs/k-laptop-001-44/ban-ghi.jsonl.gz",
          "read_seconds": 0.00046119996113702655,
          "sha256": "d7188f604ff83e2050e287e44ac480a9417ed94439af2051821bceb3aaee19c9",
          "sha256_seconds": 0.0008048000163398683,
          "uncompressed_bytes": 15035692,
          "window": "ce"
        },
        {
          "bytes": 11132791,
          "compressed_bytes": 11132791,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.31800680002197623,
          "index": 44,
          "path": "results/T-053/runs/k-laptop-001-44/trung-gian.jsonl.gz",
          "read_seconds": 0.004992300004232675,
          "sha256": "2e99c2f3b4c8bec35cc6869e7d7871a57d81dbec5508d321c90dd19fd9e3e264",
          "sha256_seconds": 0.009097300004214048,
          "uncompressed_bytes": 146282751,
          "window": "ce"
        },
        {
          "bytes": 1926747,
          "compressed_bytes": 1926747,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.08387580001726747,
          "index": 45,
          "path": "results/T-053/runs/k-laptop-001-45/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011374999885447323,
          "sha256": "be17f0b895a10f2ba14afc3f9c1701587319fe91ef2c23fd326f6ceaa9b77efb",
          "sha256_seconds": 0.0016190000460483134,
          "uncompressed_bytes": 39614488,
          "window": "that"
        },
        {
          "bytes": 12158991,
          "compressed_bytes": 12158991,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.37015119998250157,
          "index": 45,
          "path": "results/T-053/runs/k-laptop-001-45/trung-gian.jsonl.gz",
          "read_seconds": 0.0055939999874681234,
          "sha256": "3b527f41c8e55b250432b65e13f55c5075385a0386ac20914cd97943de1bdd49",
          "sha256_seconds": 0.010190200002398342,
          "uncompressed_bytes": 167014867,
          "window": "that"
        },
        {
          "bytes": 1319500,
          "compressed_bytes": 1319500,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04047050001099706,
          "index": 46,
          "path": "results/T-053/runs/k-ec2-001-46/ban-ghi.jsonl.gz",
          "read_seconds": 0.00094959995476529,
          "sha256": "e6a4f2fc41632fc8b7192e7310296c3e8588e8295e60da6bc04c57bfd0d95f91",
          "sha256_seconds": 0.0012752000475302339,
          "uncompressed_bytes": 18474632,
          "window": "ce"
        },
        {
          "bytes": 10884348,
          "compressed_bytes": 10884348,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.28932999999960884,
          "index": 46,
          "path": "results/T-053/runs/k-ec2-001-46/trung-gian.jsonl.gz",
          "read_seconds": 0.006009500008076429,
          "sha256": "6674d1f342405860d478e4ed5e665da7bc02ca3b01e545725a1bb920f7630fa0",
          "sha256_seconds": 0.010497599956579506,
          "uncompressed_bytes": 116152319,
          "window": "ce"
        },
        {
          "bytes": 1820788,
          "compressed_bytes": 1820788,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07010369998170063,
          "index": 47,
          "path": "results/T-053/runs/k-laptop-001-47/ban-ghi.jsonl.gz",
          "read_seconds": 0.00120449997484684,
          "sha256": "96fe3f9a3e1e9f8291fff869887b7d751ab12bb60137722ab9f414f5fef701d6",
          "sha256_seconds": 0.0015663999947719276,
          "uncompressed_bytes": 31131360,
          "window": "that"
        },
        {
          "bytes": 11466860,
          "compressed_bytes": 11466860,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.30301809997763485,
          "index": 47,
          "path": "results/T-053/runs/k-laptop-001-47/trung-gian.jsonl.gz",
          "read_seconds": 0.005791699979454279,
          "sha256": "bbf9a3017fe5f5aefaafc39ef6097250e7a07c35539ca9b54c8fab8f4e2fb33e",
          "sha256_seconds": 0.009460799978114665,
          "uncompressed_bytes": 122066063,
          "window": "that"
        },
        {
          "bytes": 624009,
          "compressed_bytes": 624009,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.017638099961914122,
          "index": 48,
          "path": "results/T-053/runs/k-ec2-001-48/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005135000101290643,
          "sha256": "b40c636be39819c706644a76167a0b34dfb22c427cdacbf921c01067ac460558",
          "sha256_seconds": 0.0006122000049799681,
          "uncompressed_bytes": 5782950,
          "window": "ce"
        },
        {
          "bytes": 7928531,
          "compressed_bytes": 7928531,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20921860000817105,
          "index": 48,
          "path": "results/T-053/runs/k-ec2-001-48/trung-gian.jsonl.gz",
          "read_seconds": 0.00352759996894747,
          "sha256": "17c0c208f3011b5635ce465e908fe26cbe61d98c6b9ff63fd478dafb2d610865",
          "sha256_seconds": 0.00628349999897182,
          "uncompressed_bytes": 84524647,
          "window": "ce"
        },
        {
          "bytes": 715285,
          "compressed_bytes": 715285,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.019852600002195686,
          "index": 49,
          "path": "results/T-053/runs/k-laptop-001-49/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004120999947190285,
          "sha256": "fc5835b12e7180e6e1748e42b095a47ce4c6a5f16cc132803a901039524ab062",
          "sha256_seconds": 0.0005907000158913434,
          "uncompressed_bytes": 7057958,
          "window": "that"
        },
        {
          "bytes": 7894721,
          "compressed_bytes": 7894721,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.19866529997671023,
          "index": 49,
          "path": "results/T-053/runs/k-laptop-001-49/trung-gian.jsonl.gz",
          "read_seconds": 0.003992399957496673,
          "sha256": "fb7a3eff1679c9e460efd8856a4084471e1f43772153ae5cb7f871a79b2758ca",
          "sha256_seconds": 0.006529800011776388,
          "uncompressed_bytes": 82535995,
          "window": "that"
        },
        {
          "bytes": 604213,
          "compressed_bytes": 604213,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015274500008672476,
          "index": 50,
          "path": "results/T-053/runs/k-laptop-001-50/ban-ghi.jsonl.gz",
          "read_seconds": 0.00036639999598264694,
          "sha256": "dd0aeb82320ca6ba1bf0566c5adae89214ae5ae1e00c2febf2bd013b80157585",
          "sha256_seconds": 0.0004962999955751002,
          "uncompressed_bytes": 5568606,
          "window": "ce"
        },
        {
          "bytes": 7708244,
          "compressed_bytes": 7708244,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20179290004307404,
          "index": 50,
          "path": "results/T-053/runs/k-laptop-001-50/trung-gian.jsonl.gz",
          "read_seconds": 0.003605700039770454,
          "sha256": "bfba05744dc84f3cc9b18bdede4e0854775e148464e37f1a7283310129ab5a6e",
          "sha256_seconds": 0.006489699997473508,
          "uncompressed_bytes": 83261807,
          "window": "ce"
        },
        {
          "bytes": 744984,
          "compressed_bytes": 744984,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0205157000455074,
          "index": 51,
          "path": "results/T-053/runs/k-laptop-001-51/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004999000229872763,
          "sha256": "607ead8ec0586d1acbb5096bcf48246086c8e5477bd2b4074fcd46f807eafcaa",
          "sha256_seconds": 0.0006588000105693936,
          "uncompressed_bytes": 7393906,
          "window": "that"
        },
        {
          "bytes": 8121013,
          "compressed_bytes": 8121013,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.22566689999075606,
          "index": 51,
          "path": "results/T-053/runs/k-laptop-001-51/trung-gian.jsonl.gz",
          "read_seconds": 0.0038809000398032367,
          "sha256": "99ff97a4d0802c105b5d1b1bcafe5dfb41c9c21676da1e53b6f6272e39265710",
          "sha256_seconds": 0.0068786999909207225,
          "uncompressed_bytes": 85003363,
          "window": "that"
        },
        {
          "bytes": 609161,
          "compressed_bytes": 609161,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016101400018669665,
          "index": 52,
          "path": "results/T-053/runs/k-ec2-001-52/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006034000543877482,
          "sha256": "1743bf2b9d257f7c398ea43cd2cddd01edf8bb25c7fc51d2d30100beae63a14f",
          "sha256_seconds": 0.0005366000114008784,
          "uncompressed_bytes": 5541390,
          "window": "ce"
        },
        {
          "bytes": 7610791,
          "compressed_bytes": 7610791,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20049150002887473,
          "index": 52,
          "path": "results/T-053/runs/k-ec2-001-52/trung-gian.jsonl.gz",
          "read_seconds": 0.0035176000092178583,
          "sha256": "4bc2e267f65508d76c21a3cacb459208c16e67f3ed5ad747fe638709b0ae7e56",
          "sha256_seconds": 0.006583100010175258,
          "uncompressed_bytes": 80351715,
          "window": "ce"
        },
        {
          "bytes": 651309,
          "compressed_bytes": 651309,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016044999996665865,
          "index": 53,
          "path": "results/T-053/runs/k-ec2-001-53/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004333999822847545,
          "sha256": "ce9efd08e684b3952690e3e9f40d2a957ff5bd345c4902869cf7e3d2b00453ec",
          "sha256_seconds": 0.0005527999601326883,
          "uncompressed_bytes": 5781838,
          "window": "that"
        },
        {
          "bytes": 7651796,
          "compressed_bytes": 7651796,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.19985889998497441,
          "index": 53,
          "path": "results/T-053/runs/k-ec2-001-53/trung-gian.jsonl.gz",
          "read_seconds": 0.0036564000183716416,
          "sha256": "a69a0a0d395329d5e6fe3df91dd04c6162330b8fae3dadaa7fd038849c80b362",
          "sha256_seconds": 0.0062203999841585755,
          "uncompressed_bytes": 79787459,
          "window": "that"
        },
        {
          "bytes": 527507,
          "compressed_bytes": 527507,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.018960500019602478,
          "index": 54,
          "path": "results/T-053/runs/k-ec2-001-54/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004918000195175409,
          "sha256": "d638b5b01506de9bc9d53b110fbaa7939c0084a23f82aac6cf5e512765294c22",
          "sha256_seconds": 0.0005707999807782471,
          "uncompressed_bytes": 4910364,
          "window": "ce"
        },
        {
          "bytes": 7343955,
          "compressed_bytes": 7343955,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.22442769998451695,
          "index": 54,
          "path": "results/T-053/runs/k-ec2-001-54/trung-gian.jsonl.gz",
          "read_seconds": 0.003570800006855279,
          "sha256": "d641bdf44f146132fae930b0ddb46ba9a5ac93095a31660ce61acd78ee3b2b7a",
          "sha256_seconds": 0.005949900019913912,
          "uncompressed_bytes": 79274723,
          "window": "ce"
        },
        {
          "bytes": 572877,
          "compressed_bytes": 572877,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0139861999778077,
          "index": 55,
          "path": "results/T-053/runs/k-laptop-001-55/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006219000206328928,
          "sha256": "6c249a119428210a042ae5853133d3db83ec6ffef83371bd3d48a7782d200f5b",
          "sha256_seconds": 0.00048779998905956745,
          "uncompressed_bytes": 5250760,
          "window": "that"
        },
        {
          "bytes": 7520043,
          "compressed_bytes": 7520043,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.19840459997067228,
          "index": 55,
          "path": "results/T-053/runs/k-laptop-001-55/trung-gian.jsonl.gz",
          "read_seconds": 0.003668299992568791,
          "sha256": "7409c3ad63a9e14949b7d3b63562224e05bfc0b28b9f5949c821bba46ac17205",
          "sha256_seconds": 0.006036499980837107,
          "uncompressed_bytes": 79770251,
          "window": "that"
        },
        {
          "bytes": 560315,
          "compressed_bytes": 560315,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01857509999535978,
          "index": 56,
          "path": "results/T-053/runs/k-laptop-001-56/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005171999800950289,
          "sha256": "143f30aa2738c4d352e399146bc600264ca2386fe7a8545f51b95e79943dddc3",
          "sha256_seconds": 0.00048069999320432544,
          "uncompressed_bytes": 5087594,
          "window": "ce"
        },
        {
          "bytes": 7484392,
          "compressed_bytes": 7484392,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21870470000430942,
          "index": 56,
          "path": "results/T-053/runs/k-laptop-001-56/trung-gian.jsonl.gz",
          "read_seconds": 0.005131899961270392,
          "sha256": "0172cb54c856a2b07aaf13a9e10ec6f5bb0268e3db7c81cac01c2d061791fdeb",
          "sha256_seconds": 0.008409800007939339,
          "uncompressed_bytes": 79047943,
          "window": "ce"
        },
        {
          "bytes": 709905,
          "compressed_bytes": 709905,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01834400004008785,
          "index": 57,
          "path": "results/T-053/runs/k-ec2-001-57/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004219000111334026,
          "sha256": "5bc0924b893ef1431718708888feac2f162119a237398be81cd6c67bf19de557",
          "sha256_seconds": 0.0005810000002384186,
          "uncompressed_bytes": 6150430,
          "window": "that"
        },
        {
          "bytes": 7826386,
          "compressed_bytes": 7826386,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20480199996381998,
          "index": 57,
          "path": "results/T-053/runs/k-ec2-001-57/trung-gian.jsonl.gz",
          "read_seconds": 0.0038360999897122383,
          "sha256": "4f929b8a8e0c5ba47a61d5a4162c9a2279c5c1de714c2a54c6827b8345b6d2a8",
          "sha256_seconds": 0.007465099974069744,
          "uncompressed_bytes": 80020419,
          "window": "that"
        },
        {
          "bytes": 585130,
          "compressed_bytes": 585130,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01616699999431148,
          "index": 58,
          "path": "results/T-053/runs/k-ec2-001-58/ban-ghi.jsonl.gz",
          "read_seconds": 0.00040909997187554836,
          "sha256": "fe8563d7eb96ea389c229a035e4076b2d15bbee774e4fd3e12fe5fe997975099",
          "sha256_seconds": 0.0005219000158831477,
          "uncompressed_bytes": 5370198,
          "window": "ce"
        },
        {
          "bytes": 7515507,
          "compressed_bytes": 7515507,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20785479998448864,
          "index": 58,
          "path": "results/T-053/runs/k-ec2-001-58/trung-gian.jsonl.gz",
          "read_seconds": 0.0040348999900743365,
          "sha256": "98765466a1be54725f80ca5d31500437b23e32daee0e005e48f3ad0926da75fb",
          "sha256_seconds": 0.007523500011302531,
          "uncompressed_bytes": 79943115,
          "window": "ce"
        },
        {
          "bytes": 584569,
          "compressed_bytes": 584569,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016128399991430342,
          "index": 59,
          "path": "results/T-053/runs/k-laptop-001-59/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003738999948836863,
          "sha256": "24555e3264d14896dab7a0f64d1ad9f748f4a2c0ee4e8b2b6ff04fd20cb14f8a",
          "sha256_seconds": 0.00047969998558983207,
          "uncompressed_bytes": 5339750,
          "window": "that"
        },
        {
          "bytes": 7569096,
          "compressed_bytes": 7569096,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21190940000815317,
          "index": 59,
          "path": "results/T-053/runs/k-laptop-001-59/trung-gian.jsonl.gz",
          "read_seconds": 0.004815799999050796,
          "sha256": "e1f3c45b4149162b699648651d440bdc9cc4fca18183fbf67c29899021ce5636",
          "sha256_seconds": 0.007535099983215332,
          "uncompressed_bytes": 79862367,
          "window": "that"
        },
        {
          "bytes": 305347,
          "compressed_bytes": 305347,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008308100048452616,
          "index": 60,
          "path": "results/T-053/runs/k-laptop-001-60/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004273999948054552,
          "sha256": "0dd7411e9b5658cf3a79c03202de0fc08e270ecb632df11466c13198d63e3c79",
          "sha256_seconds": 0.0002620000159367919,
          "uncompressed_bytes": 2716616,
          "window": "that"
        },
        {
          "bytes": 3974396,
          "compressed_bytes": 3974396,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10391040000831708,
          "index": 60,
          "path": "results/T-053/runs/k-laptop-001-60/trung-gian.jsonl.gz",
          "read_seconds": 0.0023997999960556626,
          "sha256": "2513e6661e0025719df043e6fb1afbfc957133ea227778e13388f3a172440ab7",
          "sha256_seconds": 0.003577299998141825,
          "uncompressed_bytes": 40972501,
          "window": "that"
        },
        {
          "bytes": 341179,
          "compressed_bytes": 341179,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.012568999954964966,
          "index": 61,
          "path": "results/T-053/runs/k-laptop-001-61/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005817000055685639,
          "sha256": "8f5c9382c110ece04b5a72683d77febf1f2893858cd2ff13ee880cb63f91788f",
          "sha256_seconds": 0.0006394999800249934,
          "uncompressed_bytes": 3443758,
          "window": "that"
        },
        {
          "bytes": 3838027,
          "compressed_bytes": 3838027,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09477810002863407,
          "index": 61,
          "path": "results/T-053/runs/k-laptop-001-61/trung-gian.jsonl.gz",
          "read_seconds": 0.0026789999683387578,
          "sha256": "0e327fd9e046caf9fe231cacacdc65124526697e829df1f53ba3f32ffe697cc7",
          "sha256_seconds": 0.004101500031538308,
          "uncompressed_bytes": 39155871,
          "window": "that"
        },
        {
          "bytes": 301761,
          "compressed_bytes": 301761,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008529399987310171,
          "index": 62,
          "path": "results/T-053/runs/k-ec2-001-62/ban-ghi.jsonl.gz",
          "read_seconds": 0.00033950002398341894,
          "sha256": "df43c95a85b060ffd6115ec7d722fe5bf995028bc278cd100d822556f428ca47",
          "sha256_seconds": 0.0002673999988473952,
          "uncompressed_bytes": 2805104,
          "window": "that"
        },
        {
          "bytes": 3786480,
          "compressed_bytes": 3786480,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09836910001467913,
          "index": 62,
          "path": "results/T-053/runs/k-ec2-001-62/trung-gian.jsonl.gz",
          "read_seconds": 0.002402300015091896,
          "sha256": "30cb64e0ec32c68bacce85e7dabad15523fe28e53a13450b1e3e0a68c55c08d1",
          "sha256_seconds": 0.003297499963082373,
          "uncompressed_bytes": 38972687,
          "window": "that"
        },
        {
          "bytes": 287444,
          "compressed_bytes": 287444,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00769550004042685,
          "index": 63,
          "path": "results/T-053/runs/k-laptop-001-63/ban-ghi.jsonl.gz",
          "read_seconds": 0.00032890000147745013,
          "sha256": "8d0f49ad670dcac6aed6d4b5c8f047f013c8b375e1ad57988bb4ef46723d71fa",
          "sha256_seconds": 0.00024850002955645323,
          "uncompressed_bytes": 2729068,
          "window": "that"
        },
        {
          "bytes": 3896093,
          "compressed_bytes": 3896093,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0979137999820523,
          "index": 63,
          "path": "results/T-053/runs/k-laptop-001-63/trung-gian.jsonl.gz",
          "read_seconds": 0.0018919999711215496,
          "sha256": "54be33cde2df3fbf6f4ac2c5475c3b0d7a59e44972737b3dd5ae61c46b2b7ed9",
          "sha256_seconds": 0.003377599990926683,
          "uncompressed_bytes": 39966955,
          "window": "that"
        },
        {
          "bytes": 275083,
          "compressed_bytes": 275083,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007866400002967566,
          "index": 64,
          "path": "results/T-053/runs/k-ec2-001-64/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003299000090919435,
          "sha256": "2fa8d5836feb53e8f11d6b23c9b7fefa65f45c337d640bbb14dde1f791552d13",
          "sha256_seconds": 0.000242499983869493,
          "uncompressed_bytes": 2519221,
          "window": "that"
        },
        {
          "bytes": 3896491,
          "compressed_bytes": 3896491,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09871469996869564,
          "index": 64,
          "path": "results/T-053/runs/k-ec2-001-64/trung-gian.jsonl.gz",
          "read_seconds": 0.0019475999870337546,
          "sha256": "54aa46dd9999cf9b91121994531c9ae2b5004acc65fd86da55369e0dc61c996f",
          "sha256_seconds": 0.00314990000333637,
          "uncompressed_bytes": 40355317,
          "window": "that"
        },
        {
          "bytes": 293276,
          "compressed_bytes": 293276,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007719599991105497,
          "index": 65,
          "path": "results/T-053/runs/k-laptop-001-65/ban-ghi.jsonl.gz",
          "read_seconds": 0.00033389998134225607,
          "sha256": "90367e4fcafebac2912ab7c7c4085e627df1e3989295faf8fbf86fc6d90a8b2f",
          "sha256_seconds": 0.00025179999647662044,
          "uncompressed_bytes": 2772140,
          "window": "that"
        },
        {
          "bytes": 3932031,
          "compressed_bytes": 3932031,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10002210002858192,
          "index": 65,
          "path": "results/T-053/runs/k-laptop-001-65/trung-gian.jsonl.gz",
          "read_seconds": 0.0019174999906681478,
          "sha256": "5f8772ea75ef48ccc38a3f41e650a446d257b889f2b6b2d4c8b1cb7fb5d3ee8b",
          "sha256_seconds": 0.0032039000070653856,
          "uncompressed_bytes": 40484475,
          "window": "that"
        },
        {
          "bytes": 342290,
          "compressed_bytes": 342290,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00985880004009232,
          "index": 66,
          "path": "results/T-053/runs/k-ec2-001-66/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003519000019878149,
          "sha256": "a69a15fb916c3ef8cfeedc6539ca10c9217ee113008c304dc84223b04e26e721",
          "sha256_seconds": 0.00030960002914071083,
          "uncompressed_bytes": 3700480,
          "window": "that"
        },
        {
          "bytes": 3974672,
          "compressed_bytes": 3974672,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10102979996008798,
          "index": 66,
          "path": "results/T-053/runs/k-ec2-001-66/trung-gian.jsonl.gz",
          "read_seconds": 0.002245300041977316,
          "sha256": "789e66c5ce8fee30909f94ef06e688a7504d7a94f9790c678d26b4d9bca72042",
          "sha256_seconds": 0.0034131999709643424,
          "uncompressed_bytes": 40655023,
          "window": "that"
        },
        {
          "bytes": 283317,
          "compressed_bytes": 283317,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007949400052893907,
          "index": 67,
          "path": "results/T-053/runs/k-laptop-001-67/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005116999964229763,
          "sha256": "3d8a4d9f5c52a061f2cbae1cedfa803d04551aac5a3fd98d79d615c85409d7d1",
          "sha256_seconds": 0.0002463000128045678,
          "uncompressed_bytes": 2514478,
          "window": "that"
        },
        {
          "bytes": 3891416,
          "compressed_bytes": 3891416,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09766130003845319,
          "index": 67,
          "path": "results/T-053/runs/k-laptop-001-67/trung-gian.jsonl.gz",
          "read_seconds": 0.002108599990606308,
          "sha256": "72e3b10e7527807301a1b0e5007c4a6e3f3d3ab43f9e9ab43d40fe272a3a8307",
          "sha256_seconds": 0.00325220002559945,
          "uncompressed_bytes": 39976545,
          "window": "that"
        },
        {
          "bytes": 300771,
          "compressed_bytes": 300771,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007995199994184077,
          "index": 68,
          "path": "results/T-053/runs/k-ec2-001-68/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003494000411592424,
          "sha256": "440e83e3a36edc6c8914bc8a3060ca35ed6dbed689eef7e265267705f8140cb5",
          "sha256_seconds": 0.0002614999539218843,
          "uncompressed_bytes": 2998948,
          "window": "that"
        },
        {
          "bytes": 3904340,
          "compressed_bytes": 3904340,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10053559998050332,
          "index": 68,
          "path": "results/T-053/runs/k-ec2-001-68/trung-gian.jsonl.gz",
          "read_seconds": 0.002082899969536811,
          "sha256": "2078a45ac731cad1b749c5e28e3cee5be4085f82092de3ed999df1eee28ad657",
          "sha256_seconds": 0.003212000010535121,
          "uncompressed_bytes": 40318739,
          "window": "that"
        },
        {
          "bytes": 324595,
          "compressed_bytes": 324595,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009546899993438274,
          "index": 69,
          "path": "results/T-053/runs/k-laptop-001-69/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006219000206328928,
          "sha256": "8daa11d32e5a44c3f4fe7cd0bb47233f73f58086f28bbedeab681ea107469320",
          "sha256_seconds": 0.0004225000157020986,
          "uncompressed_bytes": 3629992,
          "window": "that"
        },
        {
          "bytes": 3991223,
          "compressed_bytes": 3991223,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.102461599977687,
          "index": 69,
          "path": "results/T-053/runs/k-laptop-001-69/trung-gian.jsonl.gz",
          "read_seconds": 0.0020239000441506505,
          "sha256": "0939ffed635ef570a23f73502fff1745c5ee29247dc3e183b02143916a44cf97",
          "sha256_seconds": 0.003404199960641563,
          "uncompressed_bytes": 40506131,
          "window": "that"
        },
        {
          "bytes": 312779,
          "compressed_bytes": 312779,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008986199973151088,
          "index": 70,
          "path": "results/T-053/runs/k-laptop-001-70/ban-ghi.jsonl.gz",
          "read_seconds": 0.00037379999412223697,
          "sha256": "c453ef3b06631bdcbd765b13d2bc996f58aa72467fb161cf01da8e3e43b77e6c",
          "sha256_seconds": 0.00029150000773370266,
          "uncompressed_bytes": 3030144,
          "window": "that"
        },
        {
          "bytes": 3751224,
          "compressed_bytes": 3751224,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09555209998507053,
          "index": 70,
          "path": "results/T-053/runs/k-laptop-001-70/trung-gian.jsonl.gz",
          "read_seconds": 0.002319399965927005,
          "sha256": "880b45db415000b3bffc53071202062bd93b5eb5cabfd71109e43651e79e7a82",
          "sha256_seconds": 0.0034100000048056245,
          "uncompressed_bytes": 38824207,
          "window": "that"
        },
        {
          "bytes": 328632,
          "compressed_bytes": 328632,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.010945199988782406,
          "index": 71,
          "path": "results/T-053/runs/k-ec2-001-71/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003952999832108617,
          "sha256": "52b561930012f392ee09a1e5560b7ef7f3b773b4aa8ca0baca9c8a08bcd1e4da",
          "sha256_seconds": 0.00028249999741092324,
          "uncompressed_bytes": 3299322,
          "window": "that"
        },
        {
          "bytes": 3853950,
          "compressed_bytes": 3853950,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0985470000305213,
          "index": 71,
          "path": "results/T-053/runs/k-ec2-001-71/trung-gian.jsonl.gz",
          "read_seconds": 0.0019521000212989748,
          "sha256": "85507e9707851e673f9cb6e7a669feff476b15ab65d56e9c78f84c41e7a983a5",
          "sha256_seconds": 0.0031113000004552305,
          "uncompressed_bytes": 39563907,
          "window": "that"
        },
        {
          "bytes": 266522,
          "compressed_bytes": 266522,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007533300027716905,
          "index": 72,
          "path": "results/T-053/runs/k-laptop-001-72/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003364000003784895,
          "sha256": "2a3c4dccd2ae3cac1a3162333a6048c318d8e98a1f98e74e0cc61e494bb50c36",
          "sha256_seconds": 0.00023030000738799572,
          "uncompressed_bytes": 2577062,
          "window": "that"
        },
        {
          "bytes": 3691929,
          "compressed_bytes": 3691929,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09478099999250844,
          "index": 72,
          "path": "results/T-053/runs/k-laptop-001-72/trung-gian.jsonl.gz",
          "read_seconds": 0.0018774999771267176,
          "sha256": "308ae6d97bf5bfbecb31c8f01d6b31eb6f4d6ef894d4410381ef85b592420466",
          "sha256_seconds": 0.0030968000064603984,
          "uncompressed_bytes": 39419215,
          "window": "that"
        },
        {
          "bytes": 291264,
          "compressed_bytes": 291264,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007334900030400604,
          "index": 73,
          "path": "results/T-053/runs/k-ec2-001-73/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003499999875202775,
          "sha256": "36f94634e75a29376fa771fca1c813479707f9660aa29a1818331ee136983dcf",
          "sha256_seconds": 0.00025400001322850585,
          "uncompressed_bytes": 2516770,
          "window": "that"
        },
        {
          "bytes": 3869047,
          "compressed_bytes": 3869047,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09570559998974204,
          "index": 73,
          "path": "results/T-053/runs/k-ec2-001-73/trung-gian.jsonl.gz",
          "read_seconds": 0.00197789998492226,
          "sha256": "6fa3d8223c742bb850a72de12c8eb8fbdad1e770444bbf0b2115e26f6976b9b9",
          "sha256_seconds": 0.0033076999825425446,
          "uncompressed_bytes": 39967175,
          "window": "that"
        },
        {
          "bytes": 343078,
          "compressed_bytes": 343078,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.010175900009926409,
          "index": 74,
          "path": "results/T-053/runs/k-laptop-001-74/ban-ghi.jsonl.gz",
          "read_seconds": 0.000338299956638366,
          "sha256": "cdadcf7688a087977cdc9586b2f1b63c09be39d8231cbcff3718240fad056943",
          "sha256_seconds": 0.0002914000069722533,
          "uncompressed_bytes": 4028666,
          "window": "that"
        },
        {
          "bytes": 4034224,
          "compressed_bytes": 4034224,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11005309998290613,
          "index": 74,
          "path": "results/T-053/runs/k-laptop-001-74/trung-gian.jsonl.gz",
          "read_seconds": 0.0020449000294320285,
          "sha256": "2b010aadc67fd9ad063108aa8789311929aed0b1fdc509342db4b1b85edc7345",
          "sha256_seconds": 0.0033777999924495816,
          "uncompressed_bytes": 41238355,
          "window": "that"
        },
        {
          "bytes": 289346,
          "compressed_bytes": 289346,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.011277000012341887,
          "index": 75,
          "path": "results/T-053/runs/k-ec2-001-75/ban-ghi.jsonl.gz",
          "read_seconds": 0.00042310002027079463,
          "sha256": "2db978ca1d8b19086bb2dba1a149c0eda9d80bb0b7668b6a53ceea7431da3a7f",
          "sha256_seconds": 0.00035529996966943145,
          "uncompressed_bytes": 2795152,
          "window": "that"
        },
        {
          "bytes": 3868648,
          "compressed_bytes": 3868648,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11430580000160262,
          "index": 75,
          "path": "results/T-053/runs/k-ec2-001-75/trung-gian.jsonl.gz",
          "read_seconds": 0.002924300031736493,
          "sha256": "c11f613f0718904f556007e0a1fa87cf793ce1f7fa65d30162e12cf02838752f",
          "sha256_seconds": 0.005373899999540299,
          "uncompressed_bytes": 40323611,
          "window": "that"
        },
        {
          "bytes": 355753,
          "compressed_bytes": 355753,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009586900006979704,
          "index": 76,
          "path": "results/T-053/runs/k-laptop-001-76/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003212000010535121,
          "sha256": "82276f61a538cd31e7e3b4b0b550a02ab9fd9e7f3782eb280a9e8a0a53befbfa",
          "sha256_seconds": 0.00029990001348778605,
          "uncompressed_bytes": 3487352,
          "window": "that"
        },
        {
          "bytes": 4010532,
          "compressed_bytes": 4010532,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.13388989999657497,
          "index": 76,
          "path": "results/T-053/runs/k-laptop-001-76/trung-gian.jsonl.gz",
          "read_seconds": 0.0022537000477313995,
          "sha256": "60a72f36ef04432d9dc9283fc35fe19d3e117d1f46659a55c1a0e9ac736af1ca",
          "sha256_seconds": 0.0035478000063449144,
          "uncompressed_bytes": 40133007,
          "window": "that"
        },
        {
          "bytes": 287307,
          "compressed_bytes": 287307,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.013823200017213821,
          "index": 77,
          "path": "results/T-053/runs/k-ec2-001-77/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005507000023499131,
          "sha256": "cc354213a397dde3eebf754db6286f684fdd369affb1c27292089af1be7ac20c",
          "sha256_seconds": 0.00048589997459203005,
          "uncompressed_bytes": 2969390,
          "window": "that"
        },
        {
          "bytes": 3736657,
          "compressed_bytes": 3736657,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09945049998350441,
          "index": 77,
          "path": "results/T-053/runs/k-ec2-001-77/trung-gian.jsonl.gz",
          "read_seconds": 0.0029310000245459378,
          "sha256": "cdc86defe3a4b7b45c0650041d604db39fb552882da20966645beb9ad750964c",
          "sha256_seconds": 0.0047357999719679356,
          "uncompressed_bytes": 39325551,
          "window": "that"
        },
        {
          "bytes": 327110,
          "compressed_bytes": 327110,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.011612399946898222,
          "index": 78,
          "path": "results/T-053/runs/k-laptop-001-78/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003845000173896551,
          "sha256": "0e3d2a2dd4c946315ae16e35ece45f936d787f2a91272bc6d7db7cd334452a8c",
          "sha256_seconds": 0.0003332000342197716,
          "uncompressed_bytes": 4341406,
          "window": "that"
        },
        {
          "bytes": 3727958,
          "compressed_bytes": 3727958,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09984460001578555,
          "index": 78,
          "path": "results/T-053/runs/k-laptop-001-78/trung-gian.jsonl.gz",
          "read_seconds": 0.001902199990581721,
          "sha256": "5a04689d118a2d809facc41594a1e4971b999d1e8a8e0369910ec6a28d00c99e",
          "sha256_seconds": 0.003168799972627312,
          "uncompressed_bytes": 39169783,
          "window": "that"
        },
        {
          "bytes": 292508,
          "compressed_bytes": 292508,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00819030002458021,
          "index": 79,
          "path": "results/T-053/runs/k-ec2-001-79/ban-ghi.jsonl.gz",
          "read_seconds": 0.00032729998929426074,
          "sha256": "1f7443e4993e51a4c0c8de3f06a1c21039fb51e614f0f1144573b7363424a214",
          "sha256_seconds": 0.0002592999953776598,
          "uncompressed_bytes": 2791138,
          "window": "that"
        },
        {
          "bytes": 3646720,
          "compressed_bytes": 3646720,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.1111992999794893,
          "index": 79,
          "path": "results/T-053/runs/k-ec2-001-79/trung-gian.jsonl.gz",
          "read_seconds": 0.0019271000055596232,
          "sha256": "6b0b92b8339f237192fb2e190883aa6b403abc02fb553094c14319082675112c",
          "sha256_seconds": 0.003111199999693781,
          "uncompressed_bytes": 38971479,
          "window": "that"
        },
        {
          "bytes": 283078,
          "compressed_bytes": 283078,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007505599991418421,
          "index": 80,
          "path": "results/T-053/runs/k-laptop-001-80/ban-ghi.jsonl.gz",
          "read_seconds": 0.00033439998514950275,
          "sha256": "8f2a4ec826191007574a0a2af4e915b9ac53afa04e68f9915d002ba513d93f72",
          "sha256_seconds": 0.0002440999960526824,
          "uncompressed_bytes": 2748956,
          "window": "that"
        },
        {
          "bytes": 3771582,
          "compressed_bytes": 3771582,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10214329999871552,
          "index": 80,
          "path": "results/T-053/runs/k-laptop-001-80/trung-gian.jsonl.gz",
          "read_seconds": 0.0017955999937839806,
          "sha256": "d2bd73949f5c621e6b625cfb92ea9c2263a83deef4775a8cf024de2666217415",
          "sha256_seconds": 0.0030866999877616763,
          "uncompressed_bytes": 40029691,
          "window": "that"
        },
        {
          "bytes": 328933,
          "compressed_bytes": 328933,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.012535600049886853,
          "index": 81,
          "path": "results/T-053/runs/k-laptop-001-81/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004827000084333122,
          "sha256": "6ced253bdc2c0dbfa8e1a995d85c86ab0457dabd35092b2babaa4d366988a50f",
          "sha256_seconds": 0.00044999999227002263,
          "uncompressed_bytes": 3596202,
          "window": "that"
        },
        {
          "bytes": 3682667,
          "compressed_bytes": 3682667,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09452370001235977,
          "index": 81,
          "path": "results/T-053/runs/k-laptop-001-81/trung-gian.jsonl.gz",
          "read_seconds": 0.001957499946001917,
          "sha256": "3ec6ae7e2d6a99221831e247fa1a64f9f3e84e81aa328e400cfd65cc33885194",
          "sha256_seconds": 0.0030217000166885555,
          "uncompressed_bytes": 39155415,
          "window": "that"
        }
      ],
      "peak_process_rss_bytes_since_start": 151556096,
      "stage": "T11_inputs",
      "totals": {
        "compressed_bytes": 821183851.0,
        "gzip_inflate_seconds": 25.760700600105338,
        "read_seconds": 0.42467799986479804,
        "sha256_seconds": 0.7094414003076963,
        "uncompressed_bytes": 11553367561.0
      }
    },
    {
      "elapsed_seconds": 27.31335479998961,
      "file_reads": 164,
      "files": [
        {
          "bytes": 822599,
          "compressed_bytes": 822599,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0245411999640055,
          "index": 0,
          "path": "results/T-053/runs/k-ec2-001-00/ban-ghi.jsonl.gz",
          "read_seconds": 0.002076999982818961,
          "sha256": "ed24a93ac64a50ea46a0aad7acc457e7eeb6e26874aabb3c759aa8838b040479",
          "sha256_seconds": 0.0008306999807246029,
          "uncompressed_bytes": 10658924,
          "window": "ce"
        },
        {
          "bytes": 10448405,
          "compressed_bytes": 10448405,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.30824919999577105,
          "index": 0,
          "path": "results/T-053/runs/k-ec2-001-00/trung-gian.jsonl.gz",
          "read_seconds": 0.0048183000180870295,
          "sha256": "11e624246795f6810585f9d205d3c5a94ceda032433a994837b060057d58622d",
          "sha256_seconds": 0.008958199992775917,
          "uncompressed_bytes": 129551287,
          "window": "ce"
        },
        {
          "bytes": 1278473,
          "compressed_bytes": 1278473,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.044727600004989654,
          "index": 1,
          "path": "results/T-053/runs/k-ec2-001-01/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009308999869972467,
          "sha256": "fedbceed8e99302b10cce269ad8f8b982599a85f8ad3b325952a546ab38096e8",
          "sha256_seconds": 0.0011299000470899045,
          "uncompressed_bytes": 20993486,
          "window": "that"
        },
        {
          "bytes": 11200560,
          "compressed_bytes": 11200560,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3481638000230305,
          "index": 1,
          "path": "results/T-053/runs/k-ec2-001-01/trung-gian.jsonl.gz",
          "read_seconds": 0.005770699994172901,
          "sha256": "dc03fced5a2d1e8c29464cf65cd98db8faf4dbccf5c1689d5cac2c6a995c163f",
          "sha256_seconds": 0.009213099954649806,
          "uncompressed_bytes": 134712779,
          "window": "that"
        },
        {
          "bytes": 1029305,
          "compressed_bytes": 1029305,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0414390999940224,
          "index": 2,
          "path": "results/T-053/runs/k-ec2-001-02/ban-ghi.jsonl.gz",
          "read_seconds": 0.00048559997230768204,
          "sha256": "52800ca5a7bc6c2c54c944799978a6f3b987805aeaebf5c7b84c5152661a5b76",
          "sha256_seconds": 0.000832799996715039,
          "uncompressed_bytes": 22105346,
          "window": "ce"
        },
        {
          "bytes": 11951000,
          "compressed_bytes": 11951000,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4196840000222437,
          "index": 2,
          "path": "results/T-053/runs/k-ec2-001-02/trung-gian.jsonl.gz",
          "read_seconds": 0.005485100031364709,
          "sha256": "8ce4f7944c842354f3e9dd08220d2b10f9892a9db369ee4314a825f387498c2e",
          "sha256_seconds": 0.009733099956065416,
          "uncompressed_bytes": 202647183,
          "window": "ce"
        },
        {
          "bytes": 1211073,
          "compressed_bytes": 1211073,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04640699998708442,
          "index": 3,
          "path": "results/T-053/runs/k-ec2-001-03/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008037000079639256,
          "sha256": "7445df065d08ef178514bfba728a02472507525e956b1ed129924281dd43c546",
          "sha256_seconds": 0.0010162999969907105,
          "uncompressed_bytes": 23918820,
          "window": "that"
        },
        {
          "bytes": 12020473,
          "compressed_bytes": 12020473,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.372107999981381,
          "index": 3,
          "path": "results/T-053/runs/k-ec2-001-03/trung-gian.jsonl.gz",
          "read_seconds": 0.005350799998268485,
          "sha256": "337a08cac668ff83bfc10c2c1fc0f78a10bd36a2d91d870179d6c8bb78f5d7bb",
          "sha256_seconds": 0.009838700003456324,
          "uncompressed_bytes": 185688951,
          "window": "that"
        },
        {
          "bytes": 1301350,
          "compressed_bytes": 1301350,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05878840002696961,
          "index": 4,
          "path": "results/T-053/runs/k-ec2-001-04/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008125000167638063,
          "sha256": "716bdcf17af9aa5f5fdd43db5391d9184e5bc9b7df225eda6aeb601ae26f4df9",
          "sha256_seconds": 0.001073499966878444,
          "uncompressed_bytes": 34024670,
          "window": "ce"
        },
        {
          "bytes": 13506076,
          "compressed_bytes": 13506076,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5007151000318117,
          "index": 4,
          "path": "results/T-053/runs/k-ec2-001-04/trung-gian.jsonl.gz",
          "read_seconds": 0.0062546999542973936,
          "sha256": "528d6cf135e22cca572fe748b72cd783e99fa64ae3f1882dcf9b2a3517a4c73f",
          "sha256_seconds": 0.01166309998370707,
          "uncompressed_bytes": 273072439,
          "window": "ce"
        },
        {
          "bytes": 1506511,
          "compressed_bytes": 1506511,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06927209999412298,
          "index": 5,
          "path": "results/T-053/runs/k-ec2-001-05/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009054000256583095,
          "sha256": "06046b47c2f8b8573bbe0752d43dc914ff9d22135bdbf3ce98ecb8acad7e459d",
          "sha256_seconds": 0.001211599970702082,
          "uncompressed_bytes": 39914943,
          "window": "that"
        },
        {
          "bytes": 14205823,
          "compressed_bytes": 14205823,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.53795780002838,
          "index": 5,
          "path": "results/T-053/runs/k-ec2-001-05/trung-gian.jsonl.gz",
          "read_seconds": 0.006232500018086284,
          "sha256": "7da53b7268a273ca995e20c17dd5022d9cf9a6cbec98c2370147a222f035b21f",
          "sha256_seconds": 0.011589799949433655,
          "uncompressed_bytes": 291571079,
          "window": "that"
        },
        {
          "bytes": 848351,
          "compressed_bytes": 848351,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.02537539997138083,
          "index": 6,
          "path": "results/T-053/runs/k-laptop-001-06/ban-ghi.jsonl.gz",
          "read_seconds": 0.00041909998981282115,
          "sha256": "7d3a62322d7fa81e06f79cf7581c5502c7c9ae0ca1ae28e5e23d5b9cfb9278ec",
          "sha256_seconds": 0.0007170999888330698,
          "uncompressed_bytes": 10436336,
          "window": "ce"
        },
        {
          "bytes": 10527125,
          "compressed_bytes": 10527125,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.291033299989067,
          "index": 6,
          "path": "results/T-053/runs/k-laptop-001-06/trung-gian.jsonl.gz",
          "read_seconds": 0.004966399981640279,
          "sha256": "2937f20e792bca64705880429da652c20efbdaafd52da542db37d32fe1e62fb9",
          "sha256_seconds": 0.009775199985597283,
          "uncompressed_bytes": 127666383,
          "window": "ce"
        },
        {
          "bytes": 912004,
          "compressed_bytes": 912004,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.02584370004478842,
          "index": 7,
          "path": "results/T-053/runs/k-ec2-001-07/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004675000091083348,
          "sha256": "3513ce7a7e0574d4f88e919de439ceaa8a4c99a956b85dfaa3c17ede8de7b413",
          "sha256_seconds": 0.0007736000115983188,
          "uncompressed_bytes": 11115592,
          "window": "that"
        },
        {
          "bytes": 10626311,
          "compressed_bytes": 10626311,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2848987000179477,
          "index": 7,
          "path": "results/T-053/runs/k-ec2-001-07/trung-gian.jsonl.gz",
          "read_seconds": 0.00491889996919781,
          "sha256": "91fbf98ffc409b0ec72a7f3406875c91f3e437a566f135201e73f0a147efaef2",
          "sha256_seconds": 0.008568299992475659,
          "uncompressed_bytes": 122695627,
          "window": "that"
        },
        {
          "bytes": 1210453,
          "compressed_bytes": 1210453,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05648789997212589,
          "index": 8,
          "path": "results/T-053/runs/k-laptop-001-08/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008464999846182764,
          "sha256": "6051c36119c0dd155ca24ff3eae9e13ba75dd39bbcff45271f091d344ec0678e",
          "sha256_seconds": 0.0010732000228017569,
          "uncompressed_bytes": 30070960,
          "window": "ce"
        },
        {
          "bytes": 13235549,
          "compressed_bytes": 13235549,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.48435699997935444,
          "index": 8,
          "path": "results/T-053/runs/k-laptop-001-08/trung-gian.jsonl.gz",
          "read_seconds": 0.00652639998588711,
          "sha256": "a45364647592d150571c8d9f7fb88c716bcfe73788bbcd8e8179f9cb8d43e1f7",
          "sha256_seconds": 0.01106599997729063,
          "uncompressed_bytes": 255235467,
          "window": "ce"
        },
        {
          "bytes": 1529752,
          "compressed_bytes": 1529752,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06630140001652762,
          "index": 9,
          "path": "results/T-053/runs/k-ec2-001-09/ban-ghi.jsonl.gz",
          "read_seconds": 0.000957300013396889,
          "sha256": "8f4bee30671bebe3b4bdf2da6fa19bb4e1e31827ec1d738e0a09ef82b8293842",
          "sha256_seconds": 0.001409499964211136,
          "uncompressed_bytes": 38415928,
          "window": "that"
        },
        {
          "bytes": 13632831,
          "compressed_bytes": 13632831,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5221606999984942,
          "index": 9,
          "path": "results/T-053/runs/k-ec2-001-09/trung-gian.jsonl.gz",
          "read_seconds": 0.006115500000305474,
          "sha256": "d7104f3bce70ce239bf581de094f64d29b73e179e3ae84759fec1e57d738970a",
          "sha256_seconds": 0.010858199966605753,
          "uncompressed_bytes": 261436987,
          "window": "that"
        },
        {
          "bytes": 1202287,
          "compressed_bytes": 1202287,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06856059998972341,
          "index": 10,
          "path": "results/T-053/runs/k-laptop-001-10/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011041000252589583,
          "sha256": "fc45a2d498a59663275e97874c9b7162b366ed702deff44747d709acec6aab41",
          "sha256_seconds": 0.0015896999975666404,
          "uncompressed_bytes": 29958852,
          "window": "ce"
        },
        {
          "bytes": 12988601,
          "compressed_bytes": 12988601,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5302971000201069,
          "index": 10,
          "path": "results/T-053/runs/k-laptop-001-10/trung-gian.jsonl.gz",
          "read_seconds": 0.00634859997080639,
          "sha256": "4682bb3ba56c94601ea6029ec7b2c011d4c246e252c5da8b3422d6af92fb5a5b",
          "sha256_seconds": 0.016181599989067763,
          "uncompressed_bytes": 251420055,
          "window": "ce"
        },
        {
          "bytes": 1454832,
          "compressed_bytes": 1454832,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06189690000610426,
          "index": 11,
          "path": "results/T-053/runs/k-ec2-001-11/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010444999788887799,
          "sha256": "81992f23e8535f8dbb03457e388d89507a687523b6e15cb31df191d96fa46227",
          "sha256_seconds": 0.0011928000021725893,
          "uncompressed_bytes": 34263366,
          "window": "that"
        },
        {
          "bytes": 13258617,
          "compressed_bytes": 13258617,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4759726999909617,
          "index": 11,
          "path": "results/T-053/runs/k-ec2-001-11/trung-gian.jsonl.gz",
          "read_seconds": 0.0061083000036887825,
          "sha256": "3ea36301fb68ea1500138570f3b892e6a3fb90cdd8d2af2ac499b7adb8c9c9ca",
          "sha256_seconds": 0.010630599979776889,
          "uncompressed_bytes": 236970003,
          "window": "that"
        },
        {
          "bytes": 1225981,
          "compressed_bytes": 1225981,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06045049999374896,
          "index": 12,
          "path": "results/T-053/runs/k-laptop-001-12/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010850999969989061,
          "sha256": "77364ade249f19b3ea86a0ebe18732c97a57d36a5263b5daf3b765b931008549",
          "sha256_seconds": 0.001524799969047308,
          "uncompressed_bytes": 25913566,
          "window": "ce"
        },
        {
          "bytes": 12796748,
          "compressed_bytes": 12796748,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4654220000375062,
          "index": 12,
          "path": "results/T-053/runs/k-laptop-001-12/trung-gian.jsonl.gz",
          "read_seconds": 0.007528499991167337,
          "sha256": "462f6413a5578f5dd5e5c46eae73ce799167103099a9c80bed8a1f80b159353a",
          "sha256_seconds": 0.016313900006935,
          "uncompressed_bytes": 217715263,
          "window": "ce"
        },
        {
          "bytes": 1462493,
          "compressed_bytes": 1462493,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06409619998885319,
          "index": 13,
          "path": "results/T-053/runs/k-ec2-001-13/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009363000281155109,
          "sha256": "a9a652093633b37079859a759d4e1c2c331097fd4fa9b62a6e1ecdd9a27920ff",
          "sha256_seconds": 0.0012089000083506107,
          "uncompressed_bytes": 31360092,
          "window": "that"
        },
        {
          "bytes": 13021903,
          "compressed_bytes": 13021903,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.46241350000491366,
          "index": 13,
          "path": "results/T-053/runs/k-ec2-001-13/trung-gian.jsonl.gz",
          "read_seconds": 0.0069889999576844275,
          "sha256": "8dc9ac77f7ef04f0d916237a8d026d3e6bcddcd0842a054d3d14b74828ca9227",
          "sha256_seconds": 0.014745799999218434,
          "uncompressed_bytes": 213662183,
          "window": "that"
        },
        {
          "bytes": 577147,
          "compressed_bytes": 577147,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.014950399985536933,
          "index": 14,
          "path": "results/T-053/runs/k-laptop-001-14/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004346999921835959,
          "sha256": "1f53468d8c7d30bc4d60c52e6b75d74f00cc3821ba68c24ad0cca89777e42203",
          "sha256_seconds": 0.00047610001638531685,
          "uncompressed_bytes": 4873430,
          "window": "ce"
        },
        {
          "bytes": 8793133,
          "compressed_bytes": 8793133,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.22173230000771582,
          "index": 14,
          "path": "results/T-053/runs/k-laptop-001-14/trung-gian.jsonl.gz",
          "read_seconds": 0.004167299950495362,
          "sha256": "b826ba03189af82b66b5c85904a9803184be178c0c6815c74d1ed69e665f69aa",
          "sha256_seconds": 0.009193100035190582,
          "uncompressed_bytes": 86528619,
          "window": "ce"
        },
        {
          "bytes": 697723,
          "compressed_bytes": 697723,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.017403799982275814,
          "index": 15,
          "path": "results/T-053/runs/k-ec2-001-15/ban-ghi.jsonl.gz",
          "read_seconds": 0.00046220002695918083,
          "sha256": "44e06790d2d897a589e11f677813b1f7b10a29443d308703829e04867b2fc6cf",
          "sha256_seconds": 0.0005707999807782471,
          "uncompressed_bytes": 6738444,
          "window": "that"
        },
        {
          "bytes": 9055563,
          "compressed_bytes": 9055563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21625050000147894,
          "index": 15,
          "path": "results/T-053/runs/k-ec2-001-15/trung-gian.jsonl.gz",
          "read_seconds": 0.004055100027471781,
          "sha256": "23b1a85437c84b17676466b4d474b96c7b067a2891a31e644a1dcc079b1806f4",
          "sha256_seconds": 0.0073654999723657966,
          "uncompressed_bytes": 87378743,
          "window": "that"
        },
        {
          "bytes": 1210062,
          "compressed_bytes": 1210062,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06427910004276782,
          "index": 16,
          "path": "results/T-053/runs/k-ec2-001-16/ban-ghi.jsonl.gz",
          "read_seconds": 0.001215199998114258,
          "sha256": "ce03562948dec6729110e499039c9791a6b0d5acaccab061f555d98b873f261c",
          "sha256_seconds": 0.00133350002579391,
          "uncompressed_bytes": 30948408,
          "window": "ce"
        },
        {
          "bytes": 13026484,
          "compressed_bytes": 13026484,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.48631160001968965,
          "index": 16,
          "path": "results/T-053/runs/k-ec2-001-16/trung-gian.jsonl.gz",
          "read_seconds": 0.005867799976840615,
          "sha256": "dcdababff7ef122b9acbbfb1c541ff20becbf0510384bf0b6e41f758ce6434a3",
          "sha256_seconds": 0.010752399975899607,
          "uncompressed_bytes": 259912347,
          "window": "ce"
        },
        {
          "bytes": 1601811,
          "compressed_bytes": 1601811,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06128500000340864,
          "index": 17,
          "path": "results/T-053/runs/k-ec2-001-17/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009802000131458044,
          "sha256": "2cf9afbac2b3c8cdc4c382aae3032aa0c356032f65912a31792419f474cbfbeb",
          "sha256_seconds": 0.0013087000115774572,
          "uncompressed_bytes": 32437146,
          "window": "that"
        },
        {
          "bytes": 11856068,
          "compressed_bytes": 11856068,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3870360000291839,
          "index": 17,
          "path": "results/T-053/runs/k-ec2-001-17/trung-gian.jsonl.gz",
          "read_seconds": 0.00553240004228428,
          "sha256": "12ef2bbe14f73b0f7fccbed9ea20666a60ec9642d3461ee1d15a6d29f4e0a933",
          "sha256_seconds": 0.014721899991855025,
          "uncompressed_bytes": 175977559,
          "window": "that"
        },
        {
          "bytes": 1056011,
          "compressed_bytes": 1056011,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04561610001837835,
          "index": 18,
          "path": "results/T-053/runs/k-laptop-001-18/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008501000120304525,
          "sha256": "a58cbe37868ac806fa277eda558df530dd9f29cbfc3d6d7724c6b65db08b5dfa",
          "sha256_seconds": 0.0010092000011354685,
          "uncompressed_bytes": 20764174,
          "window": "ce"
        },
        {
          "bytes": 12047687,
          "compressed_bytes": 12047687,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.38186449999921024,
          "index": 18,
          "path": "results/T-053/runs/k-laptop-001-18/trung-gian.jsonl.gz",
          "read_seconds": 0.00550859997747466,
          "sha256": "d415b17115dde04e3dbcd0b173ae35d2ffb397e835f05d23f2b5f396da4dd058",
          "sha256_seconds": 0.010036899999249727,
          "uncompressed_bytes": 191215491,
          "window": "ce"
        },
        {
          "bytes": 1437712,
          "compressed_bytes": 1437712,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06597170000895858,
          "index": 19,
          "path": "results/T-053/runs/k-laptop-001-19/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008983999723568559,
          "sha256": "d6d49b9203bb9d7b52aeb5b30f9722a616f40c49d2389c5717a21299741636b7",
          "sha256_seconds": 0.0011677000438794494,
          "uncompressed_bytes": 32908784,
          "window": "that"
        },
        {
          "bytes": 13174562,
          "compressed_bytes": 13174562,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5032022999948822,
          "index": 19,
          "path": "results/T-053/runs/k-laptop-001-19/trung-gian.jsonl.gz",
          "read_seconds": 0.0077343000448308885,
          "sha256": "5e7ce74f99932de6a8485552b3caba2a701b15946a5ef1c1472518f973c3bcc5",
          "sha256_seconds": 0.011173499980941415,
          "uncompressed_bytes": 231525955,
          "window": "that"
        },
        {
          "bytes": 1078891,
          "compressed_bytes": 1078891,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04597879998618737,
          "index": 20,
          "path": "results/T-053/runs/k-laptop-001-20/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010771999950520694,
          "sha256": "44a2c2ca61ee06102b40d97b4105b9fd1871d25c442b06fcbf68be36ec7363f2",
          "sha256_seconds": 0.0011422000243328512,
          "uncompressed_bytes": 17297772,
          "window": "ce"
        },
        {
          "bytes": 11535920,
          "compressed_bytes": 11535920,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3569559000316076,
          "index": 20,
          "path": "results/T-053/runs/k-laptop-001-20/trung-gian.jsonl.gz",
          "read_seconds": 0.005292999965604395,
          "sha256": "7c26270a80ddca65ce9af26d5d3176f5a0fbd0129b8de13c59099379970f078b",
          "sha256_seconds": 0.0102024000370875,
          "uncompressed_bytes": 155876335,
          "window": "ce"
        },
        {
          "bytes": 1308686,
          "compressed_bytes": 1308686,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05011050001485273,
          "index": 21,
          "path": "results/T-053/runs/k-laptop-001-21/ban-ghi.jsonl.gz",
          "read_seconds": 0.001012900029309094,
          "sha256": "a93fa7657385f244c979e512cde318a4c77d6adbaf46175b6ce322478a0a7a01",
          "sha256_seconds": 0.0013066999963484704,
          "uncompressed_bytes": 25272765,
          "window": "that"
        },
        {
          "bytes": 12247809,
          "compressed_bytes": 12247809,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.38170379999792203,
          "index": 21,
          "path": "results/T-053/runs/k-laptop-001-21/trung-gian.jsonl.gz",
          "read_seconds": 0.005796200013719499,
          "sha256": "02343f06330aeffb2cf02bcceee5bcf31df5fee844643c071684cf7b7e61ae27",
          "sha256_seconds": 0.010399999970104545,
          "uncompressed_bytes": 183184571,
          "window": "that"
        },
        {
          "bytes": 1167638,
          "compressed_bytes": 1167638,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04587649996392429,
          "index": 22,
          "path": "results/T-053/runs/k-ec2-001-22/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008201999589800835,
          "sha256": "2b4c9c639393e2db909054671363d72a3d1344f0b36c921c4307715d6b60d517",
          "sha256_seconds": 0.0009730000165291131,
          "uncompressed_bytes": 23457226,
          "window": "ce"
        },
        {
          "bytes": 12337820,
          "compressed_bytes": 12337820,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4033960000379011,
          "index": 22,
          "path": "results/T-053/runs/k-ec2-001-22/trung-gian.jsonl.gz",
          "read_seconds": 0.005638300033751875,
          "sha256": "c7848f76949bef5f5d0c4c3932c8d61611e2b1108a347eb5530d70c88f008d1a",
          "sha256_seconds": 0.009921999997459352,
          "uncompressed_bytes": 201534451,
          "window": "ce"
        },
        {
          "bytes": 1524153,
          "compressed_bytes": 1524153,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0573731999611482,
          "index": 23,
          "path": "results/T-053/runs/k-laptop-001-23/ban-ghi.jsonl.gz",
          "read_seconds": 0.0012051000376231968,
          "sha256": "84bc08057e635bed81733346a377457e85ffd62fbdd045f8c7a7f5db45e6da19",
          "sha256_seconds": 0.0012967000366188586,
          "uncompressed_bytes": 30628016,
          "window": "that"
        },
        {
          "bytes": 12651563,
          "compressed_bytes": 12651563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.41259880003053695,
          "index": 23,
          "path": "results/T-053/runs/k-laptop-001-23/trung-gian.jsonl.gz",
          "read_seconds": 0.006050699972547591,
          "sha256": "825c8cc75c8f7815247112c00369e899cb5bf7352e4fbeae994447f494175434",
          "sha256_seconds": 0.010622100031469017,
          "uncompressed_bytes": 195483455,
          "window": "that"
        },
        {
          "bytes": 1032006,
          "compressed_bytes": 1032006,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.050650899996981025,
          "index": 24,
          "path": "results/T-053/runs/k-laptop-001-24/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005044999998062849,
          "sha256": "d4a806c8cc51c8964d06ec88d1624e4e5c20275fbe77eea59a25f40eb5abd4c7",
          "sha256_seconds": 0.0009788000024855137,
          "uncompressed_bytes": 18208454,
          "window": "ce"
        },
        {
          "bytes": 11749340,
          "compressed_bytes": 11749340,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.38063029997283593,
          "index": 24,
          "path": "results/T-053/runs/k-laptop-001-24/trung-gian.jsonl.gz",
          "read_seconds": 0.006191799999214709,
          "sha256": "959e3d6c62df4d2206896a7c1090edfcff818a07726a3be1957820e94bfa32e8",
          "sha256_seconds": 0.014069699973333627,
          "uncompressed_bytes": 170164895,
          "window": "ce"
        },
        {
          "bytes": 1120525,
          "compressed_bytes": 1120525,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.052319000009447336,
          "index": 25,
          "path": "results/T-053/runs/k-laptop-001-25/ban-ghi.jsonl.gz",
          "read_seconds": 0.000915899989195168,
          "sha256": "52af893eaa19504b750286bc8ce5122956a0140a21d2b57bca73a65226c700c5",
          "sha256_seconds": 0.0011761999921873212,
          "uncompressed_bytes": 25257224,
          "window": "that"
        },
        {
          "bytes": 12510563,
          "compressed_bytes": 12510563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4702922999858856,
          "index": 25,
          "path": "results/T-053/runs/k-laptop-001-25/trung-gian.jsonl.gz",
          "read_seconds": 0.005894000001717359,
          "sha256": "750efebe9210bc0fa18e90e469b06fd84731303a7d5880f68d8ac22b91e408e3",
          "sha256_seconds": 0.013675700000021607,
          "uncompressed_bytes": 220682353,
          "window": "that"
        },
        {
          "bytes": 1014977,
          "compressed_bytes": 1014977,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03888639999786392,
          "index": 26,
          "path": "results/T-053/runs/k-ec2-001-26/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004800999886356294,
          "sha256": "866a6e7f15d819eaca48da5afed9fb46c7fd80b6c9b6872b644d1473f93f963f",
          "sha256_seconds": 0.0008543999865651131,
          "uncompressed_bytes": 19463466,
          "window": "ce"
        },
        {
          "bytes": 11785721,
          "compressed_bytes": 11785721,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3779911999590695,
          "index": 26,
          "path": "results/T-053/runs/k-ec2-001-26/trung-gian.jsonl.gz",
          "read_seconds": 0.0053678000112995505,
          "sha256": "c0fb374852e13a403ed0349a3b9234232b2e48eb5c28bb07dfc1de8fc739f64f",
          "sha256_seconds": 0.009942599979694933,
          "uncompressed_bytes": 182660367,
          "window": "ce"
        },
        {
          "bytes": 1021014,
          "compressed_bytes": 1021014,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0365983999799937,
          "index": 27,
          "path": "results/T-053/runs/k-laptop-001-27/ban-ghi.jsonl.gz",
          "read_seconds": 0.00046170002315193415,
          "sha256": "1a330a7886f6957d92f01afbedca6c6af4a6fe196f77d839452ae66016d1dc01",
          "sha256_seconds": 0.000825700000859797,
          "uncompressed_bytes": 18377695,
          "window": "that"
        },
        {
          "bytes": 11577590,
          "compressed_bytes": 11577590,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.34889650001423433,
          "index": 27,
          "path": "results/T-053/runs/k-laptop-001-27/trung-gian.jsonl.gz",
          "read_seconds": 0.005221800005529076,
          "sha256": "429e32bacd9af45367f907b98817bd2290bc3b32aca8ae54de37b2bdf25738ab",
          "sha256_seconds": 0.011199499946087599,
          "uncompressed_bytes": 173121647,
          "window": "that"
        },
        {
          "bytes": 1042539,
          "compressed_bytes": 1042539,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0339500000118278,
          "index": 28,
          "path": "results/T-053/runs/k-laptop-001-28/ban-ghi.jsonl.gz",
          "read_seconds": 0.00047769997036084533,
          "sha256": "f85eba05d5af1e864791a9fbfb8d2ddd14f3277000874b8c3ad3ad65aff8db0c",
          "sha256_seconds": 0.0008424000116065145,
          "uncompressed_bytes": 16110688,
          "window": "ce"
        },
        {
          "bytes": 11541406,
          "compressed_bytes": 11541406,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.33836799999698997,
          "index": 28,
          "path": "results/T-053/runs/k-laptop-001-28/trung-gian.jsonl.gz",
          "read_seconds": 0.005233600037172437,
          "sha256": "afcbead493de06b41b4b10f1c76f6ddefbfe77e75e279d01f9dfc2c8a0780334",
          "sha256_seconds": 0.009211700002197176,
          "uncompressed_bytes": 157105339,
          "window": "ce"
        },
        {
          "bytes": 1624620,
          "compressed_bytes": 1624620,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06500800000503659,
          "index": 29,
          "path": "results/T-053/runs/k-laptop-001-29/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009904999751597643,
          "sha256": "1af2a35edbe4f969ad057837f5ae2694240764e289ce22d7dfa708818eefec80",
          "sha256_seconds": 0.0013648000312969089,
          "uncompressed_bytes": 32677978,
          "window": "that"
        },
        {
          "bytes": 12330215,
          "compressed_bytes": 12330215,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4214794999570586,
          "index": 29,
          "path": "results/T-053/runs/k-laptop-001-29/trung-gian.jsonl.gz",
          "read_seconds": 0.005494600045494735,
          "sha256": "a2a38682c2811c22fbd5accb650dcd85f851454936c5bc53b0bd6494b22dae62",
          "sha256_seconds": 0.010422400024253875,
          "uncompressed_bytes": 175000963,
          "window": "that"
        },
        {
          "bytes": 1178865,
          "compressed_bytes": 1178865,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05157189996680245,
          "index": 30,
          "path": "results/T-053/runs/k-ec2-001-30/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010821999749168754,
          "sha256": "1fbe92925b4fbdee41bb2f79e56bfa89191d7610a47ab3ce5e7597412b714aee",
          "sha256_seconds": 0.0014979999978095293,
          "uncompressed_bytes": 24507156,
          "window": "ce"
        },
        {
          "bytes": 12647668,
          "compressed_bytes": 12647668,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.41996269999071956,
          "index": 30,
          "path": "results/T-053/runs/k-ec2-001-30/trung-gian.jsonl.gz",
          "read_seconds": 0.005798900034278631,
          "sha256": "ab446e32a91c9b81972e0b4df052cf0e7ad1a737e553cc4a44d4ce38c939002b",
          "sha256_seconds": 0.01068680000025779,
          "uncompressed_bytes": 214430531,
          "window": "ce"
        },
        {
          "bytes": 1901118,
          "compressed_bytes": 1901118,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.09681019996060058,
          "index": 31,
          "path": "results/T-053/runs/k-laptop-001-31/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011166000040248036,
          "sha256": "f0213ca394440f971a728586edc7ff5fb7e559a50795516e6ec1131033962fd4",
          "sha256_seconds": 0.001589899999089539,
          "uncompressed_bytes": 44220284,
          "window": "that"
        },
        {
          "bytes": 13015137,
          "compressed_bytes": 13015137,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4512064000009559,
          "index": 31,
          "path": "results/T-053/runs/k-laptop-001-31/trung-gian.jsonl.gz",
          "read_seconds": 0.005909900006372482,
          "sha256": "fbb28c90630eedbce15e40488f38b531b43cfd99ee61057bb75b4acd5243b79e",
          "sha256_seconds": 0.010941300017293543,
          "uncompressed_bytes": 214444619,
          "window": "that"
        },
        {
          "bytes": 1018853,
          "compressed_bytes": 1018853,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03656560002127662,
          "index": 32,
          "path": "results/T-053/runs/k-laptop-001-32/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004890999989584088,
          "sha256": "ad779224f744eca63e6af5f577a517b6885f83bd9ce9a1b8a133d128b3641dd8",
          "sha256_seconds": 0.0008614999824203551,
          "uncompressed_bytes": 16421004,
          "window": "ce"
        },
        {
          "bytes": 11306390,
          "compressed_bytes": 11306390,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3506574999773875,
          "index": 32,
          "path": "results/T-053/runs/k-laptop-001-32/trung-gian.jsonl.gz",
          "read_seconds": 0.005288599990308285,
          "sha256": "371d2fe7d4a36234213b967d6211a4103a382378c2ba84f858787890bc0395d3",
          "sha256_seconds": 0.009229300019796938,
          "uncompressed_bytes": 154181995,
          "window": "ce"
        },
        {
          "bytes": 1727868,
          "compressed_bytes": 1727868,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06832319998648018,
          "index": 33,
          "path": "results/T-053/runs/k-laptop-001-33/ban-ghi.jsonl.gz",
          "read_seconds": 0.000979500007815659,
          "sha256": "d4422c480465b5b54d81e115d0e756706b5f5d45ca9a90f1a46f308f0f4ef259",
          "sha256_seconds": 0.001595199981238693,
          "uncompressed_bytes": 32202962,
          "window": "that"
        },
        {
          "bytes": 12081207,
          "compressed_bytes": 12081207,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.38416170002892613,
          "index": 33,
          "path": "results/T-053/runs/k-laptop-001-33/trung-gian.jsonl.gz",
          "read_seconds": 0.00619009998627007,
          "sha256": "63d0714383e3ecc7ddf60c1c5c0246a28d72d30a0a30d16b1bbab80a13f3c55c",
          "sha256_seconds": 0.010121300001628697,
          "uncompressed_bytes": 161559683,
          "window": "that"
        },
        {
          "bytes": 987783,
          "compressed_bytes": 987783,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03877899999497458,
          "index": 34,
          "path": "results/T-053/runs/k-ec2-001-34/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005210000090301037,
          "sha256": "1deb8b14faeab25e4b6dfc2a3bde4d9730835492dbe7507378e07c5db35d1927",
          "sha256_seconds": 0.0009174000006169081,
          "uncompressed_bytes": 16427664,
          "window": "ce"
        },
        {
          "bytes": 11232270,
          "compressed_bytes": 11232270,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.33940029999939725,
          "index": 34,
          "path": "results/T-053/runs/k-ec2-001-34/trung-gian.jsonl.gz",
          "read_seconds": 0.004958199977409095,
          "sha256": "bcb8aa973d34bcd5c2b801fa560784d7c9e43b0c4cd249562fb5791a60814b0e",
          "sha256_seconds": 0.009357600007206202,
          "uncompressed_bytes": 155921331,
          "window": "ce"
        },
        {
          "bytes": 2029706,
          "compressed_bytes": 2029706,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07588020002003759,
          "index": 35,
          "path": "results/T-053/runs/k-laptop-001-35/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011354000307619572,
          "sha256": "6fad7d180800c32d3ebb3c771a6b8caa4a1ae3879cac28f3956b523dc6995ac5",
          "sha256_seconds": 0.0017662000027485192,
          "uncompressed_bytes": 36896487,
          "window": "that"
        },
        {
          "bytes": 12213410,
          "compressed_bytes": 12213410,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4126896999659948,
          "index": 35,
          "path": "results/T-053/runs/k-laptop-001-35/trung-gian.jsonl.gz",
          "read_seconds": 0.005603900004643947,
          "sha256": "14395cac23a72f46fe2d1683b90db30554fe10b683cfb8a926d38a0746c18a8a",
          "sha256_seconds": 0.010133999981917441,
          "uncompressed_bytes": 158345679,
          "window": "that"
        },
        {
          "bytes": 1314711,
          "compressed_bytes": 1314711,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.060754099977202713,
          "index": 36,
          "path": "results/T-053/runs/k-laptop-001-36/ban-ghi.jsonl.gz",
          "read_seconds": 0.0012809999752789736,
          "sha256": "598c3a9d6adbe11572162eb56b0df3c9b71ec6f5ecbdccbf6d2d14ecc448a5d7",
          "sha256_seconds": 0.0017555999802425504,
          "uncompressed_bytes": 18610066,
          "window": "ce"
        },
        {
          "bytes": 10925820,
          "compressed_bytes": 10925820,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.40474840003298596,
          "index": 36,
          "path": "results/T-053/runs/k-laptop-001-36/trung-gian.jsonl.gz",
          "read_seconds": 0.005390900012571365,
          "sha256": "854ea2603f3f2d3fd0b51b039daeda31bb485c7d06affb6774de4d6482c85a8e",
          "sha256_seconds": 0.014926199975889176,
          "uncompressed_bytes": 118188339,
          "window": "ce"
        },
        {
          "bytes": 1216962,
          "compressed_bytes": 1216962,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05665519996546209,
          "index": 37,
          "path": "results/T-053/runs/k-laptop-001-37/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011030000168830156,
          "sha256": "e72f64ab11adf9aad4919b624f614143a6d8eb0815519773397585d515d89b74",
          "sha256_seconds": 0.0008542999858036637,
          "uncompressed_bytes": 16457582,
          "window": "that"
        },
        {
          "bytes": 11071929,
          "compressed_bytes": 11071929,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2988916999893263,
          "index": 37,
          "path": "results/T-053/runs/k-laptop-001-37/trung-gian.jsonl.gz",
          "read_seconds": 0.007470100012142211,
          "sha256": "491707df7e47f765ec4059326b2a4a8b4a976ee3d357c0bcf51ca9e17a5ef03c",
          "sha256_seconds": 0.011100000003352761,
          "uncompressed_bytes": 124267547,
          "window": "that"
        },
        {
          "bytes": 968714,
          "compressed_bytes": 968714,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0540865000220947,
          "index": 38,
          "path": "results/T-053/runs/k-ec2-001-38/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006791999912820756,
          "sha256": "8bd4dd2c03658b39309474aa68135b5f48d3e13849d012b76bb6ba3b4eacb4eb",
          "sha256_seconds": 0.0013554999604821205,
          "uncompressed_bytes": 15740140,
          "window": "ce"
        },
        {
          "bytes": 11166023,
          "compressed_bytes": 11166023,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3736710000084713,
          "index": 38,
          "path": "results/T-053/runs/k-ec2-001-38/trung-gian.jsonl.gz",
          "read_seconds": 0.004946900007780641,
          "sha256": "b9e9a75d02c5918622abb4652a98748a8264c6ffc328a0049bd26f08b5230d9a",
          "sha256_seconds": 0.009018099983222783,
          "uncompressed_bytes": 153532697,
          "window": "ce"
        },
        {
          "bytes": 2194356,
          "compressed_bytes": 2194356,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0841138000250794,
          "index": 39,
          "path": "results/T-053/runs/k-laptop-001-39/ban-ghi.jsonl.gz",
          "read_seconds": 0.001645199954509735,
          "sha256": "56df5f3e5e86728344887a5a3f05bd61b8147223f23444fda4ae088cb4d5df7e",
          "sha256_seconds": 0.0024391000042669475,
          "uncompressed_bytes": 42532030,
          "window": "that"
        },
        {
          "bytes": 12394216,
          "compressed_bytes": 12394216,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3872401000116952,
          "index": 39,
          "path": "results/T-053/runs/k-laptop-001-39/trung-gian.jsonl.gz",
          "read_seconds": 0.00580789998639375,
          "sha256": "9185ed0b2ff8b1d23ecdec7221183243b348080a088987c665f57dbddbd9bb3a",
          "sha256_seconds": 0.010440700047183782,
          "uncompressed_bytes": 168836655,
          "window": "that"
        },
        {
          "bytes": 1233079,
          "compressed_bytes": 1233079,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.044437200005631894,
          "index": 40,
          "path": "results/T-053/runs/k-laptop-001-40/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008088999893516302,
          "sha256": "622e790f6ca76d3a6034cd87133655d1adee14252f676041abd368154c5284c3",
          "sha256_seconds": 0.0009957000147551298,
          "uncompressed_bytes": 17431184,
          "window": "ce"
        },
        {
          "bytes": 10735191,
          "compressed_bytes": 10735191,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3265209000092,
          "index": 40,
          "path": "results/T-053/runs/k-laptop-001-40/trung-gian.jsonl.gz",
          "read_seconds": 0.006641699990723282,
          "sha256": "a35666f870bb42c4373f65d07bd990722a9ce37afaa89a85648d075e395255cf",
          "sha256_seconds": 0.0112263000337407,
          "uncompressed_bytes": 120368383,
          "window": "ce"
        },
        {
          "bytes": 1450045,
          "compressed_bytes": 1450045,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04674650001106784,
          "index": 41,
          "path": "results/T-053/runs/k-laptop-001-41/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009396999957971275,
          "sha256": "3c2570c53e1f84106b07c5fcfcedde3fbb147cd0fb21708c73efee0e2bfa3f9c",
          "sha256_seconds": 0.0012224999954923987,
          "uncompressed_bytes": 22395444,
          "window": "that"
        },
        {
          "bytes": 11305153,
          "compressed_bytes": 11305153,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3168039000011049,
          "index": 41,
          "path": "results/T-053/runs/k-laptop-001-41/trung-gian.jsonl.gz",
          "read_seconds": 0.005190500000026077,
          "sha256": "98631360b15819ef89c13568d0c5b373331e7becb1d15e3b138f877e86db1c88",
          "sha256_seconds": 0.009470199991483241,
          "uncompressed_bytes": 125650075,
          "window": "that"
        },
        {
          "bytes": 1183524,
          "compressed_bytes": 1183524,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.035898600006476045,
          "index": 42,
          "path": "results/T-053/runs/k-ec2-001-42/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008280000183731318,
          "sha256": "22297a9a6b4139043ced3a2edfc318d92fa176bc32307ed7c9238aae5839d418",
          "sha256_seconds": 0.0009549000533297658,
          "uncompressed_bytes": 15832522,
          "window": "ce"
        },
        {
          "bytes": 10598076,
          "compressed_bytes": 10598076,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.30548590002581477,
          "index": 42,
          "path": "results/T-053/runs/k-ec2-001-42/trung-gian.jsonl.gz",
          "read_seconds": 0.0054979000124149024,
          "sha256": "f94fa0f3a23e9a4fb3ec78551db8b1a37fcb49ebb4eb5f8afa3159d7250820e6",
          "sha256_seconds": 0.008487099956255406,
          "uncompressed_bytes": 114154819,
          "window": "ce"
        },
        {
          "bytes": 1158621,
          "compressed_bytes": 1158621,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.033480499987490475,
          "index": 43,
          "path": "results/T-053/runs/k-laptop-001-43/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008254999993368983,
          "sha256": "d344459e6c3caef324fe0f4bdcce249391e6c2c3a239a6492946c0687abbf145",
          "sha256_seconds": 0.0009417000110261142,
          "uncompressed_bytes": 15323968,
          "window": "that"
        },
        {
          "bytes": 10915175,
          "compressed_bytes": 10915175,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.29456110001774505,
          "index": 43,
          "path": "results/T-053/runs/k-laptop-001-43/trung-gian.jsonl.gz",
          "read_seconds": 0.005118299974128604,
          "sha256": "2fbdd6ac11435f2bdb30edc23b1df1c9ad9e67660a3b45809a242b9bcdfe423c",
          "sha256_seconds": 0.008986799977719784,
          "uncompressed_bytes": 120626663,
          "window": "that"
        },
        {
          "bytes": 994092,
          "compressed_bytes": 994092,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03666280000470579,
          "index": 44,
          "path": "results/T-053/runs/k-laptop-001-44/ban-ghi.jsonl.gz",
          "read_seconds": 0.00045089999912306666,
          "sha256": "d7188f604ff83e2050e287e44ac480a9417ed94439af2051821bceb3aaee19c9",
          "sha256_seconds": 0.0008046000148169696,
          "uncompressed_bytes": 15035692,
          "window": "ce"
        },
        {
          "bytes": 11132791,
          "compressed_bytes": 11132791,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.34024789999239147,
          "index": 44,
          "path": "results/T-053/runs/k-laptop-001-44/trung-gian.jsonl.gz",
          "read_seconds": 0.005499299964867532,
          "sha256": "2e99c2f3b4c8bec35cc6869e7d7871a57d81dbec5508d321c90dd19fd9e3e264",
          "sha256_seconds": 0.009499299980234355,
          "uncompressed_bytes": 146282751,
          "window": "ce"
        },
        {
          "bytes": 1926747,
          "compressed_bytes": 1926747,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07564130000537261,
          "index": 45,
          "path": "results/T-053/runs/k-laptop-001-45/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010575000196695328,
          "sha256": "be17f0b895a10f2ba14afc3f9c1701587319fe91ef2c23fd326f6ceaa9b77efb",
          "sha256_seconds": 0.001546700019389391,
          "uncompressed_bytes": 39614488,
          "window": "that"
        },
        {
          "bytes": 12158991,
          "compressed_bytes": 12158991,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3634500000043772,
          "index": 45,
          "path": "results/T-053/runs/k-laptop-001-45/trung-gian.jsonl.gz",
          "read_seconds": 0.006270300014875829,
          "sha256": "3b527f41c8e55b250432b65e13f55c5075385a0386ac20914cd97943de1bdd49",
          "sha256_seconds": 0.01176850002957508,
          "uncompressed_bytes": 167014867,
          "window": "that"
        },
        {
          "bytes": 1319500,
          "compressed_bytes": 1319500,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04130560002522543,
          "index": 46,
          "path": "results/T-053/runs/k-ec2-001-46/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008929999894462526,
          "sha256": "e6a4f2fc41632fc8b7192e7310296c3e8588e8295e60da6bc04c57bfd0d95f91",
          "sha256_seconds": 0.0011133999796584249,
          "uncompressed_bytes": 18474632,
          "window": "ce"
        },
        {
          "bytes": 10884348,
          "compressed_bytes": 10884348,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.28607080003712326,
          "index": 46,
          "path": "results/T-053/runs/k-ec2-001-46/trung-gian.jsonl.gz",
          "read_seconds": 0.004856100014876574,
          "sha256": "6674d1f342405860d478e4ed5e665da7bc02ca3b01e545725a1bb920f7630fa0",
          "sha256_seconds": 0.009192400029860437,
          "uncompressed_bytes": 116152319,
          "window": "ce"
        },
        {
          "bytes": 1820788,
          "compressed_bytes": 1820788,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07115209999028593,
          "index": 47,
          "path": "results/T-053/runs/k-laptop-001-47/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010036000167019665,
          "sha256": "96fe3f9a3e1e9f8291fff869887b7d751ab12bb60137722ab9f414f5fef701d6",
          "sha256_seconds": 0.0014617000124417245,
          "uncompressed_bytes": 31131360,
          "window": "that"
        },
        {
          "bytes": 11466860,
          "compressed_bytes": 11466860,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.28451040002983063,
          "index": 47,
          "path": "results/T-053/runs/k-laptop-001-47/trung-gian.jsonl.gz",
          "read_seconds": 0.005519099999219179,
          "sha256": "bbf9a3017fe5f5aefaafc39ef6097250e7a07c35539ca9b54c8fab8f4e2fb33e",
          "sha256_seconds": 0.009241099993232638,
          "uncompressed_bytes": 122066063,
          "window": "that"
        },
        {
          "bytes": 624009,
          "compressed_bytes": 624009,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016824499994982034,
          "index": 48,
          "path": "results/T-053/runs/k-ec2-001-48/ban-ghi.jsonl.gz",
          "read_seconds": 0.000416700029745698,
          "sha256": "b40c636be39819c706644a76167a0b34dfb22c427cdacbf921c01067ac460558",
          "sha256_seconds": 0.000512500002514571,
          "uncompressed_bytes": 5782950,
          "window": "ce"
        },
        {
          "bytes": 7928531,
          "compressed_bytes": 7928531,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.19607310002902523,
          "index": 48,
          "path": "results/T-053/runs/k-ec2-001-48/trung-gian.jsonl.gz",
          "read_seconds": 0.0035881000221706927,
          "sha256": "17c0c208f3011b5635ce465e908fe26cbe61d98c6b9ff63fd478dafb2d610865",
          "sha256_seconds": 0.006411799986381084,
          "uncompressed_bytes": 84524647,
          "window": "ce"
        },
        {
          "bytes": 715285,
          "compressed_bytes": 715285,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0265343000064604,
          "index": 49,
          "path": "results/T-053/runs/k-laptop-001-49/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004081000224687159,
          "sha256": "fc5835b12e7180e6e1748e42b095a47ce4c6a5f16cc132803a901039524ab062",
          "sha256_seconds": 0.0005839000223204494,
          "uncompressed_bytes": 7057958,
          "window": "that"
        },
        {
          "bytes": 7894721,
          "compressed_bytes": 7894721,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20950019999872893,
          "index": 49,
          "path": "results/T-053/runs/k-laptop-001-49/trung-gian.jsonl.gz",
          "read_seconds": 0.004518400004599243,
          "sha256": "fb7a3eff1679c9e460efd8856a4084471e1f43772153ae5cb7f871a79b2758ca",
          "sha256_seconds": 0.007156600011512637,
          "uncompressed_bytes": 82535995,
          "window": "that"
        },
        {
          "bytes": 604213,
          "compressed_bytes": 604213,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015163699979893863,
          "index": 50,
          "path": "results/T-053/runs/k-laptop-001-50/ban-ghi.jsonl.gz",
          "read_seconds": 0.00045469996985048056,
          "sha256": "dd0aeb82320ca6ba1bf0566c5adae89214ae5ae1e00c2febf2bd013b80157585",
          "sha256_seconds": 0.0005574999959208071,
          "uncompressed_bytes": 5568606,
          "window": "ce"
        },
        {
          "bytes": 7708244,
          "compressed_bytes": 7708244,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.22421070002019405,
          "index": 50,
          "path": "results/T-053/runs/k-laptop-001-50/trung-gian.jsonl.gz",
          "read_seconds": 0.0035587000311352313,
          "sha256": "bfba05744dc84f3cc9b18bdede4e0854775e148464e37f1a7283310129ab5a6e",
          "sha256_seconds": 0.009363899996969849,
          "uncompressed_bytes": 83261807,
          "window": "ce"
        },
        {
          "bytes": 744984,
          "compressed_bytes": 744984,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0203406999935396,
          "index": 51,
          "path": "results/T-053/runs/k-laptop-001-51/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005683000199496746,
          "sha256": "607ead8ec0586d1acbb5096bcf48246086c8e5477bd2b4074fcd46f807eafcaa",
          "sha256_seconds": 0.0008889999589882791,
          "uncompressed_bytes": 7393906,
          "window": "that"
        },
        {
          "bytes": 8121013,
          "compressed_bytes": 8121013,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21294529997976497,
          "index": 51,
          "path": "results/T-053/runs/k-laptop-001-51/trung-gian.jsonl.gz",
          "read_seconds": 0.003632500011008233,
          "sha256": "99ff97a4d0802c105b5d1b1bcafe5dfb41c9c21676da1e53b6f6272e39265710",
          "sha256_seconds": 0.006626899994444102,
          "uncompressed_bytes": 85003363,
          "window": "that"
        },
        {
          "bytes": 609161,
          "compressed_bytes": 609161,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.018647699966095388,
          "index": 52,
          "path": "results/T-053/runs/k-ec2-001-52/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005858000367879868,
          "sha256": "1743bf2b9d257f7c398ea43cd2cddd01edf8bb25c7fc51d2d30100beae63a14f",
          "sha256_seconds": 0.0005031999899074435,
          "uncompressed_bytes": 5541390,
          "window": "ce"
        },
        {
          "bytes": 7610791,
          "compressed_bytes": 7610791,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2402824999880977,
          "index": 52,
          "path": "results/T-053/runs/k-ec2-001-52/trung-gian.jsonl.gz",
          "read_seconds": 0.004796599969267845,
          "sha256": "4bc2e267f65508d76c21a3cacb459208c16e67f3ed5ad747fe638709b0ae7e56",
          "sha256_seconds": 0.0078025999828241765,
          "uncompressed_bytes": 80351715,
          "window": "ce"
        },
        {
          "bytes": 651309,
          "compressed_bytes": 651309,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01593619998311624,
          "index": 53,
          "path": "results/T-053/runs/k-ec2-001-53/ban-ghi.jsonl.gz",
          "read_seconds": 0.00038819998735561967,
          "sha256": "ce9efd08e684b3952690e3e9f40d2a957ff5bd345c4902869cf7e3d2b00453ec",
          "sha256_seconds": 0.0005332999862730503,
          "uncompressed_bytes": 5781838,
          "window": "that"
        },
        {
          "bytes": 7651796,
          "compressed_bytes": 7651796,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20230120001360774,
          "index": 53,
          "path": "results/T-053/runs/k-ec2-001-53/trung-gian.jsonl.gz",
          "read_seconds": 0.003510700014885515,
          "sha256": "a69a0a0d395329d5e6fe3df91dd04c6162330b8fae3dadaa7fd038849c80b362",
          "sha256_seconds": 0.0065793999820016325,
          "uncompressed_bytes": 79787459,
          "window": "that"
        },
        {
          "bytes": 527507,
          "compressed_bytes": 527507,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0138810999924317,
          "index": 54,
          "path": "results/T-053/runs/k-ec2-001-54/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005709999823011458,
          "sha256": "d638b5b01506de9bc9d53b110fbaa7939c0084a23f82aac6cf5e512765294c22",
          "sha256_seconds": 0.0006978000164963305,
          "uncompressed_bytes": 4910364,
          "window": "ce"
        },
        {
          "bytes": 7343955,
          "compressed_bytes": 7343955,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.1968083999818191,
          "index": 54,
          "path": "results/T-053/runs/k-ec2-001-54/trung-gian.jsonl.gz",
          "read_seconds": 0.0037240000092424452,
          "sha256": "d641bdf44f146132fae930b0ddb46ba9a5ac93095a31660ce61acd78ee3b2b7a",
          "sha256_seconds": 0.006415999960154295,
          "uncompressed_bytes": 79274723,
          "window": "ce"
        },
        {
          "bytes": 572877,
          "compressed_bytes": 572877,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.014356900006532669,
          "index": 55,
          "path": "results/T-053/runs/k-laptop-001-55/ban-ghi.jsonl.gz",
          "read_seconds": 0.00036780000664293766,
          "sha256": "6c249a119428210a042ae5853133d3db83ec6ffef83371bd3d48a7782d200f5b",
          "sha256_seconds": 0.0004726999904960394,
          "uncompressed_bytes": 5250760,
          "window": "that"
        },
        {
          "bytes": 7520043,
          "compressed_bytes": 7520043,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.19413519999943674,
          "index": 55,
          "path": "results/T-053/runs/k-laptop-001-55/trung-gian.jsonl.gz",
          "read_seconds": 0.003543300030287355,
          "sha256": "7409c3ad63a9e14949b7d3b63562224e05bfc0b28b9f5949c821bba46ac17205",
          "sha256_seconds": 0.006271899968851358,
          "uncompressed_bytes": 79770251,
          "window": "that"
        },
        {
          "bytes": 560315,
          "compressed_bytes": 560315,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016740999999456108,
          "index": 56,
          "path": "results/T-053/runs/k-laptop-001-56/ban-ghi.jsonl.gz",
          "read_seconds": 0.000520200002938509,
          "sha256": "143f30aa2738c4d352e399146bc600264ca2386fe7a8545f51b95e79943dddc3",
          "sha256_seconds": 0.0006847999757155776,
          "uncompressed_bytes": 5087594,
          "window": "ce"
        },
        {
          "bytes": 7484392,
          "compressed_bytes": 7484392,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2448856999981217,
          "index": 56,
          "path": "results/T-053/runs/k-laptop-001-56/trung-gian.jsonl.gz",
          "read_seconds": 0.004967999993823469,
          "sha256": "0172cb54c856a2b07aaf13a9e10ec6f5bb0268e3db7c81cac01c2d061791fdeb",
          "sha256_seconds": 0.009815500001423061,
          "uncompressed_bytes": 79047943,
          "window": "ce"
        },
        {
          "bytes": 709905,
          "compressed_bytes": 709905,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01709929999196902,
          "index": 57,
          "path": "results/T-053/runs/k-ec2-001-57/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004092000308446586,
          "sha256": "5bc0924b893ef1431718708888feac2f162119a237398be81cd6c67bf19de557",
          "sha256_seconds": 0.0006068000220693648,
          "uncompressed_bytes": 6150430,
          "window": "that"
        },
        {
          "bytes": 7826386,
          "compressed_bytes": 7826386,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.1978446000139229,
          "index": 57,
          "path": "results/T-053/runs/k-ec2-001-57/trung-gian.jsonl.gz",
          "read_seconds": 0.0035294999834150076,
          "sha256": "4f929b8a8e0c5ba47a61d5a4162c9a2279c5c1de714c2a54c6827b8345b6d2a8",
          "sha256_seconds": 0.006308500014711171,
          "uncompressed_bytes": 80020419,
          "window": "that"
        },
        {
          "bytes": 585130,
          "compressed_bytes": 585130,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015397400013171136,
          "index": 58,
          "path": "results/T-053/runs/k-ec2-001-58/ban-ghi.jsonl.gz",
          "read_seconds": 0.00036369997542351484,
          "sha256": "fe8563d7eb96ea389c229a035e4076b2d15bbee774e4fd3e12fe5fe997975099",
          "sha256_seconds": 0.00048019998939707875,
          "uncompressed_bytes": 5370198,
          "window": "ce"
        },
        {
          "bytes": 7515507,
          "compressed_bytes": 7515507,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2155485999537632,
          "index": 58,
          "path": "results/T-053/runs/k-ec2-001-58/trung-gian.jsonl.gz",
          "read_seconds": 0.0035611999919638038,
          "sha256": "98765466a1be54725f80ca5d31500437b23e32daee0e005e48f3ad0926da75fb",
          "sha256_seconds": 0.006465899990871549,
          "uncompressed_bytes": 79943115,
          "window": "ce"
        },
        {
          "bytes": 584569,
          "compressed_bytes": 584569,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016795200004708022,
          "index": 59,
          "path": "results/T-053/runs/k-laptop-001-59/ban-ghi.jsonl.gz",
          "read_seconds": 0.00038270000368356705,
          "sha256": "24555e3264d14896dab7a0f64d1ad9f748f4a2c0ee4e8b2b6ff04fd20cb14f8a",
          "sha256_seconds": 0.0005029999883845448,
          "uncompressed_bytes": 5339750,
          "window": "that"
        },
        {
          "bytes": 7569096,
          "compressed_bytes": 7569096,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20988050004234537,
          "index": 59,
          "path": "results/T-053/runs/k-laptop-001-59/trung-gian.jsonl.gz",
          "read_seconds": 0.0048399000079371035,
          "sha256": "e1f3c45b4149162b699648651d440bdc9cc4fca18183fbf67c29899021ce5636",
          "sha256_seconds": 0.007923100027255714,
          "uncompressed_bytes": 79862367,
          "window": "that"
        },
        {
          "bytes": 305347,
          "compressed_bytes": 305347,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009311500005424023,
          "index": 60,
          "path": "results/T-053/runs/k-laptop-001-60/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004065000102855265,
          "sha256": "0dd7411e9b5658cf3a79c03202de0fc08e270ecb632df11466c13198d63e3c79",
          "sha256_seconds": 0.0003409999771974981,
          "uncompressed_bytes": 2716616,
          "window": "that"
        },
        {
          "bytes": 3974396,
          "compressed_bytes": 3974396,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10379439999815077,
          "index": 60,
          "path": "results/T-053/runs/k-laptop-001-60/trung-gian.jsonl.gz",
          "read_seconds": 0.0020450999727472663,
          "sha256": "2513e6661e0025719df043e6fb1afbfc957133ea227778e13388f3a172440ab7",
          "sha256_seconds": 0.003360999980941415,
          "uncompressed_bytes": 40972501,
          "window": "that"
        },
        {
          "bytes": 341179,
          "compressed_bytes": 341179,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00885270000435412,
          "index": 61,
          "path": "results/T-053/runs/k-laptop-001-61/ban-ghi.jsonl.gz",
          "read_seconds": 0.00033000000985339284,
          "sha256": "8f5c9382c110ece04b5a72683d77febf1f2893858cd2ff13ee880cb63f91788f",
          "sha256_seconds": 0.0002896999940276146,
          "uncompressed_bytes": 3443758,
          "window": "that"
        },
        {
          "bytes": 3838027,
          "compressed_bytes": 3838027,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0949166000355035,
          "index": 61,
          "path": "results/T-053/runs/k-laptop-001-61/trung-gian.jsonl.gz",
          "read_seconds": 0.001844200014602393,
          "sha256": "0e327fd9e046caf9fe231cacacdc65124526697e829df1f53ba3f32ffe697cc7",
          "sha256_seconds": 0.0030745999538339674,
          "uncompressed_bytes": 39155871,
          "window": "that"
        },
        {
          "bytes": 301761,
          "compressed_bytes": 301761,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00756960001308471,
          "index": 62,
          "path": "results/T-053/runs/k-ec2-001-62/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003622999647632241,
          "sha256": "df43c95a85b060ffd6115ec7d722fe5bf995028bc278cd100d822556f428ca47",
          "sha256_seconds": 0.00026519998209550977,
          "uncompressed_bytes": 2805104,
          "window": "that"
        },
        {
          "bytes": 3786480,
          "compressed_bytes": 3786480,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10317720001330599,
          "index": 62,
          "path": "results/T-053/runs/k-ec2-001-62/trung-gian.jsonl.gz",
          "read_seconds": 0.001999799977056682,
          "sha256": "30cb64e0ec32c68bacce85e7dabad15523fe28e53a13450b1e3e0a68c55c08d1",
          "sha256_seconds": 0.0032854999881237745,
          "uncompressed_bytes": 38972687,
          "window": "that"
        },
        {
          "bytes": 287444,
          "compressed_bytes": 287444,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007830599963199347,
          "index": 63,
          "path": "results/T-053/runs/k-laptop-001-63/ban-ghi.jsonl.gz",
          "read_seconds": 0.00031619996298104525,
          "sha256": "8d0f49ad670dcac6aed6d4b5c8f047f013c8b375e1ad57988bb4ef46723d71fa",
          "sha256_seconds": 0.00024880003184080124,
          "uncompressed_bytes": 2729068,
          "window": "that"
        },
        {
          "bytes": 3896093,
          "compressed_bytes": 3896093,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.12958180002169684,
          "index": 63,
          "path": "results/T-053/runs/k-laptop-001-63/trung-gian.jsonl.gz",
          "read_seconds": 0.0018666000105440617,
          "sha256": "54be33cde2df3fbf6f4ac2c5475c3b0d7a59e44972737b3dd5ae61c46b2b7ed9",
          "sha256_seconds": 0.0031216999632306397,
          "uncompressed_bytes": 39966955,
          "window": "that"
        },
        {
          "bytes": 275083,
          "compressed_bytes": 275083,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008173100010026246,
          "index": 64,
          "path": "results/T-053/runs/k-ec2-001-64/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003228000132367015,
          "sha256": "2fa8d5836feb53e8f11d6b23c9b7fefa65f45c337d640bbb14dde1f791552d13",
          "sha256_seconds": 0.0002521999995224178,
          "uncompressed_bytes": 2519221,
          "window": "that"
        },
        {
          "bytes": 3896491,
          "compressed_bytes": 3896491,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11212760000489652,
          "index": 64,
          "path": "results/T-053/runs/k-ec2-001-64/trung-gian.jsonl.gz",
          "read_seconds": 0.0021749999723397195,
          "sha256": "54aa46dd9999cf9b91121994531c9ae2b5004acc65fd86da55369e0dc61c996f",
          "sha256_seconds": 0.0035841999924741685,
          "uncompressed_bytes": 40355317,
          "window": "that"
        },
        {
          "bytes": 293276,
          "compressed_bytes": 293276,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.011678099981509149,
          "index": 65,
          "path": "results/T-053/runs/k-laptop-001-65/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004973000031895936,
          "sha256": "90367e4fcafebac2912ab7c7c4085e627df1e3989295faf8fbf86fc6d90a8b2f",
          "sha256_seconds": 0.00043020001612603664,
          "uncompressed_bytes": 2772140,
          "window": "that"
        },
        {
          "bytes": 3932031,
          "compressed_bytes": 3932031,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.12654029997065663,
          "index": 65,
          "path": "results/T-053/runs/k-laptop-001-65/trung-gian.jsonl.gz",
          "read_seconds": 0.0021792000043205917,
          "sha256": "5f8772ea75ef48ccc38a3f41e650a446d257b889f2b6b2d4c8b1cb7fb5d3ee8b",
          "sha256_seconds": 0.0035502000246196985,
          "uncompressed_bytes": 40484475,
          "window": "that"
        },
        {
          "bytes": 342290,
          "compressed_bytes": 342290,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.015465600008610636,
          "index": 66,
          "path": "results/T-053/runs/k-ec2-001-66/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004591000033542514,
          "sha256": "a69a15fb916c3ef8cfeedc6539ca10c9217ee113008c304dc84223b04e26e721",
          "sha256_seconds": 0.0004918000195175409,
          "uncompressed_bytes": 3700480,
          "window": "that"
        },
        {
          "bytes": 3974672,
          "compressed_bytes": 3974672,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10221329994965345,
          "index": 66,
          "path": "results/T-053/runs/k-ec2-001-66/trung-gian.jsonl.gz",
          "read_seconds": 0.00282689998857677,
          "sha256": "789e66c5ce8fee30909f94ef06e688a7504d7a94f9790c678d26b4d9bca72042",
          "sha256_seconds": 0.00431300001218915,
          "uncompressed_bytes": 40655023,
          "window": "that"
        },
        {
          "bytes": 283317,
          "compressed_bytes": 283317,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0075533000053837895,
          "index": 67,
          "path": "results/T-053/runs/k-laptop-001-67/ban-ghi.jsonl.gz",
          "read_seconds": 0.00031590001890435815,
          "sha256": "3d8a4d9f5c52a061f2cbae1cedfa803d04551aac5a3fd98d79d615c85409d7d1",
          "sha256_seconds": 0.0003106999793089926,
          "uncompressed_bytes": 2514478,
          "window": "that"
        },
        {
          "bytes": 3891416,
          "compressed_bytes": 3891416,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11004270002013072,
          "index": 67,
          "path": "results/T-053/runs/k-laptop-001-67/trung-gian.jsonl.gz",
          "read_seconds": 0.0019161999807693064,
          "sha256": "72e3b10e7527807301a1b0e5007c4a6e3f3d3ab43f9e9ab43d40fe272a3a8307",
          "sha256_seconds": 0.003156099992338568,
          "uncompressed_bytes": 39976545,
          "window": "that"
        },
        {
          "bytes": 300771,
          "compressed_bytes": 300771,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.012679299979936332,
          "index": 68,
          "path": "results/T-053/runs/k-ec2-001-68/ban-ghi.jsonl.gz",
          "read_seconds": 0.00044949998846277595,
          "sha256": "440e83e3a36edc6c8914bc8a3060ca35ed6dbed689eef7e265267705f8140cb5",
          "sha256_seconds": 0.000388299988117069,
          "uncompressed_bytes": 2998948,
          "window": "that"
        },
        {
          "bytes": 3904340,
          "compressed_bytes": 3904340,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10731709998799488,
          "index": 68,
          "path": "results/T-053/runs/k-ec2-001-68/trung-gian.jsonl.gz",
          "read_seconds": 0.002359400037676096,
          "sha256": "2078a45ac731cad1b749c5e28e3cee5be4085f82092de3ed999df1eee28ad657",
          "sha256_seconds": 0.0035655999672599137,
          "uncompressed_bytes": 40318739,
          "window": "that"
        },
        {
          "bytes": 324595,
          "compressed_bytes": 324595,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009083900018595159,
          "index": 69,
          "path": "results/T-053/runs/k-laptop-001-69/ban-ghi.jsonl.gz",
          "read_seconds": 0.00035370001569390297,
          "sha256": "8daa11d32e5a44c3f4fe7cd0bb47233f73f58086f28bbedeab681ea107469320",
          "sha256_seconds": 0.0002788000274449587,
          "uncompressed_bytes": 3629992,
          "window": "that"
        },
        {
          "bytes": 3991223,
          "compressed_bytes": 3991223,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0980507000349462,
          "index": 69,
          "path": "results/T-053/runs/k-laptop-001-69/trung-gian.jsonl.gz",
          "read_seconds": 0.0019301000284031034,
          "sha256": "0939ffed635ef570a23f73502fff1745c5ee29247dc3e183b02143916a44cf97",
          "sha256_seconds": 0.003197499958332628,
          "uncompressed_bytes": 40506131,
          "window": "that"
        },
        {
          "bytes": 312779,
          "compressed_bytes": 312779,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008090199960861355,
          "index": 70,
          "path": "results/T-053/runs/k-laptop-001-70/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003200999926775694,
          "sha256": "c453ef3b06631bdcbd765b13d2bc996f58aa72467fb161cf01da8e3e43b77e6c",
          "sha256_seconds": 0.0002823999966494739,
          "uncompressed_bytes": 3030144,
          "window": "that"
        },
        {
          "bytes": 3751224,
          "compressed_bytes": 3751224,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10094149998622015,
          "index": 70,
          "path": "results/T-053/runs/k-laptop-001-70/trung-gian.jsonl.gz",
          "read_seconds": 0.0018099999870173633,
          "sha256": "880b45db415000b3bffc53071202062bd93b5eb5cabfd71109e43651e79e7a82",
          "sha256_seconds": 0.0030074999667704105,
          "uncompressed_bytes": 38824207,
          "window": "that"
        },
        {
          "bytes": 328632,
          "compressed_bytes": 328632,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009177600033581257,
          "index": 71,
          "path": "results/T-053/runs/k-ec2-001-71/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003752000047825277,
          "sha256": "52b561930012f392ee09a1e5560b7ef7f3b773b4aa8ca0baca9c8a08bcd1e4da",
          "sha256_seconds": 0.000291300006210804,
          "uncompressed_bytes": 3299322,
          "window": "that"
        },
        {
          "bytes": 3853950,
          "compressed_bytes": 3853950,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09566910000285134,
          "index": 71,
          "path": "results/T-053/runs/k-ec2-001-71/trung-gian.jsonl.gz",
          "read_seconds": 0.0022013999987393618,
          "sha256": "85507e9707851e673f9cb6e7a669feff476b15ab65d56e9c78f84c41e7a983a5",
          "sha256_seconds": 0.003219400008674711,
          "uncompressed_bytes": 39563907,
          "window": "that"
        },
        {
          "bytes": 266522,
          "compressed_bytes": 266522,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0070371999754570425,
          "index": 72,
          "path": "results/T-053/runs/k-laptop-001-72/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003141000051982701,
          "sha256": "2a3c4dccd2ae3cac1a3162333a6048c318d8e98a1f98e74e0cc61e494bb50c36",
          "sha256_seconds": 0.00023070001043379307,
          "uncompressed_bytes": 2577062,
          "window": "that"
        },
        {
          "bytes": 3691929,
          "compressed_bytes": 3691929,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0948740000021644,
          "index": 72,
          "path": "results/T-053/runs/k-laptop-001-72/trung-gian.jsonl.gz",
          "read_seconds": 0.0017585000023245811,
          "sha256": "308ae6d97bf5bfbecb31c8f01d6b31eb6f4d6ef894d4410381ef85b592420466",
          "sha256_seconds": 0.0029529999592341483,
          "uncompressed_bytes": 39419215,
          "window": "that"
        },
        {
          "bytes": 291264,
          "compressed_bytes": 291264,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0075255000265315175,
          "index": 73,
          "path": "results/T-053/runs/k-ec2-001-73/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003268999862484634,
          "sha256": "36f94634e75a29376fa771fca1c813479707f9660aa29a1818331ee136983dcf",
          "sha256_seconds": 0.00025189999723806977,
          "uncompressed_bytes": 2516770,
          "window": "that"
        },
        {
          "bytes": 3869047,
          "compressed_bytes": 3869047,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09753309999359772,
          "index": 73,
          "path": "results/T-053/runs/k-ec2-001-73/trung-gian.jsonl.gz",
          "read_seconds": 0.001896300003863871,
          "sha256": "6fa3d8223c742bb850a72de12c8eb8fbdad1e770444bbf0b2115e26f6976b9b9",
          "sha256_seconds": 0.003225899999961257,
          "uncompressed_bytes": 39967175,
          "window": "that"
        },
        {
          "bytes": 343078,
          "compressed_bytes": 343078,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009956499969121069,
          "index": 74,
          "path": "results/T-053/runs/k-laptop-001-74/ban-ghi.jsonl.gz",
          "read_seconds": 0.00039219995960593224,
          "sha256": "cdadcf7688a087977cdc9586b2f1b63c09be39d8231cbcff3718240fad056943",
          "sha256_seconds": 0.0002938000252470374,
          "uncompressed_bytes": 4028666,
          "window": "that"
        },
        {
          "bytes": 4034224,
          "compressed_bytes": 4034224,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10934439999982715,
          "index": 74,
          "path": "results/T-053/runs/k-laptop-001-74/trung-gian.jsonl.gz",
          "read_seconds": 0.0021803000126965344,
          "sha256": "2b010aadc67fd9ad063108aa8789311929aed0b1fdc509342db4b1b85edc7345",
          "sha256_seconds": 0.0032500000088475645,
          "uncompressed_bytes": 41238355,
          "window": "that"
        },
        {
          "bytes": 289346,
          "compressed_bytes": 289346,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.0077606000122614205,
          "index": 75,
          "path": "results/T-053/runs/k-ec2-001-75/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003331000334583223,
          "sha256": "2db978ca1d8b19086bb2dba1a149c0eda9d80bb0b7668b6a53ceea7431da3a7f",
          "sha256_seconds": 0.00025049998657777905,
          "uncompressed_bytes": 2795152,
          "window": "that"
        },
        {
          "bytes": 3868648,
          "compressed_bytes": 3868648,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10136819997569546,
          "index": 75,
          "path": "results/T-053/runs/k-ec2-001-75/trung-gian.jsonl.gz",
          "read_seconds": 0.001875300018582493,
          "sha256": "c11f613f0718904f556007e0a1fa87cf793ce1f7fa65d30162e12cf02838752f",
          "sha256_seconds": 0.003099000023212284,
          "uncompressed_bytes": 40323611,
          "window": "that"
        },
        {
          "bytes": 355753,
          "compressed_bytes": 355753,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009978100017178804,
          "index": 76,
          "path": "results/T-053/runs/k-laptop-001-76/ban-ghi.jsonl.gz",
          "read_seconds": 0.00038139999378472567,
          "sha256": "82276f61a538cd31e7e3b4b0b550a02ab9fd9e7f3782eb280a9e8a0a53befbfa",
          "sha256_seconds": 0.0003151999553665519,
          "uncompressed_bytes": 3487352,
          "window": "that"
        },
        {
          "bytes": 4010532,
          "compressed_bytes": 4010532,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10386329999892041,
          "index": 76,
          "path": "results/T-053/runs/k-laptop-001-76/trung-gian.jsonl.gz",
          "read_seconds": 0.0022740999702364206,
          "sha256": "60a72f36ef04432d9dc9283fc35fe19d3e117d1f46659a55c1a0e9ac736af1ca",
          "sha256_seconds": 0.0034733000211417675,
          "uncompressed_bytes": 40133007,
          "window": "that"
        },
        {
          "bytes": 287307,
          "compressed_bytes": 287307,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00860499998088926,
          "index": 77,
          "path": "results/T-053/runs/k-ec2-001-77/ban-ghi.jsonl.gz",
          "read_seconds": 0.00037839997094124556,
          "sha256": "cc354213a397dde3eebf754db6286f684fdd369affb1c27292089af1be7ac20c",
          "sha256_seconds": 0.00025590002769604325,
          "uncompressed_bytes": 2969390,
          "window": "that"
        },
        {
          "bytes": 3736657,
          "compressed_bytes": 3736657,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10258880001492798,
          "index": 77,
          "path": "results/T-053/runs/k-ec2-001-77/trung-gian.jsonl.gz",
          "read_seconds": 0.0018621999770402908,
          "sha256": "cdc86defe3a4b7b45c0650041d604db39fb552882da20966645beb9ad750964c",
          "sha256_seconds": 0.0030285000102594495,
          "uncompressed_bytes": 39325551,
          "window": "that"
        },
        {
          "bytes": 327110,
          "compressed_bytes": 327110,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.014136900019366294,
          "index": 78,
          "path": "results/T-053/runs/k-laptop-001-78/ban-ghi.jsonl.gz",
          "read_seconds": 0.00045200000749900937,
          "sha256": "0e3d2a2dd4c946315ae16e35ece45f936d787f2a91272bc6d7db7cd334452a8c",
          "sha256_seconds": 0.0004556000349111855,
          "uncompressed_bytes": 4341406,
          "window": "that"
        },
        {
          "bytes": 3727958,
          "compressed_bytes": 3727958,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09694839996518567,
          "index": 78,
          "path": "results/T-053/runs/k-laptop-001-78/trung-gian.jsonl.gz",
          "read_seconds": 0.0023734000278636813,
          "sha256": "5a04689d118a2d809facc41594a1e4971b999d1e8a8e0369910ec6a28d00c99e",
          "sha256_seconds": 0.003582799981813878,
          "uncompressed_bytes": 39169783,
          "window": "that"
        },
        {
          "bytes": 292508,
          "compressed_bytes": 292508,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007924500037916005,
          "index": 79,
          "path": "results/T-053/runs/k-ec2-001-79/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005714999861083925,
          "sha256": "1f7443e4993e51a4c0c8de3f06a1c21039fb51e614f0f1144573b7363424a214",
          "sha256_seconds": 0.00029280001763254404,
          "uncompressed_bytes": 2791138,
          "window": "that"
        },
        {
          "bytes": 3646720,
          "compressed_bytes": 3646720,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09132519998820499,
          "index": 79,
          "path": "results/T-053/runs/k-ec2-001-79/trung-gian.jsonl.gz",
          "read_seconds": 0.0017680999590083957,
          "sha256": "6b0b92b8339f237192fb2e190883aa6b403abc02fb553094c14319082675112c",
          "sha256_seconds": 0.002920700004324317,
          "uncompressed_bytes": 38971479,
          "window": "that"
        },
        {
          "bytes": 283078,
          "compressed_bytes": 283078,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007515000004786998,
          "index": 80,
          "path": "results/T-053/runs/k-laptop-001-80/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003361999988555908,
          "sha256": "8f2a4ec826191007574a0a2af4e915b9ac53afa04e68f9915d002ba513d93f72",
          "sha256_seconds": 0.00025179999647662044,
          "uncompressed_bytes": 2748956,
          "window": "that"
        },
        {
          "bytes": 3771582,
          "compressed_bytes": 3771582,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10354520002147183,
          "index": 80,
          "path": "results/T-053/runs/k-laptop-001-80/trung-gian.jsonl.gz",
          "read_seconds": 0.0017691999673843384,
          "sha256": "d2bd73949f5c621e6b625cfb92ea9c2263a83deef4775a8cf024de2666217415",
          "sha256_seconds": 0.0032310999813489616,
          "uncompressed_bytes": 40029691,
          "window": "that"
        },
        {
          "bytes": 328933,
          "compressed_bytes": 328933,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00906869996106252,
          "index": 81,
          "path": "results/T-053/runs/k-laptop-001-81/ban-ghi.jsonl.gz",
          "read_seconds": 0.00035669998032972217,
          "sha256": "6ced253bdc2c0dbfa8e1a995d85c86ab0457dabd35092b2babaa4d366988a50f",
          "sha256_seconds": 0.00028310000197961926,
          "uncompressed_bytes": 3596202,
          "window": "that"
        },
        {
          "bytes": 3682667,
          "compressed_bytes": 3682667,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09423220000462607,
          "index": 81,
          "path": "results/T-053/runs/k-laptop-001-81/trung-gian.jsonl.gz",
          "read_seconds": 0.0019020999898202717,
          "sha256": "3ec6ae7e2d6a99221831e247fa1a64f9f3e84e81aa328e400cfd65cc33885194",
          "sha256_seconds": 0.0029566999874077737,
          "uncompressed_bytes": 39155415,
          "window": "that"
        }
      ],
      "peak_process_rss_bytes_since_start": 151638016,
      "stage": "T12_inputs",
      "totals": {
        "compressed_bytes": 821183851.0,
        "gzip_inflate_seconds": 26.138835500110872,
        "read_seconds": 0.4232927999109961,
        "sha256_seconds": 0.7448349994956516,
        "uncompressed_bytes": 11553367561.0
      }
    },
    {
      "elapsed_seconds": 27.314823399996385,
      "file_reads": 164,
      "files": [
        {
          "compressed_bytes": 1278473,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.047232999990228564,
          "path": "results/T-053/runs/k-ec2-001-01/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008306000381708145,
          "sha256": "fedbceed8e99302b10cce269ad8f8b982599a85f8ad3b325952a546ab38096e8",
          "sha256_seconds": 0.0013652999768964946,
          "uncompressed_bytes": 20993486,
          "window": "that"
        },
        {
          "compressed_bytes": 11200560,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3164707000250928,
          "path": "results/T-053/runs/k-ec2-001-01/trung-gian.jsonl.gz",
          "read_seconds": 0.005757100007031113,
          "sha256": "dc03fced5a2d1e8c29464cf65cd98db8faf4dbccf5c1689d5cac2c6a995c163f",
          "sha256_seconds": 0.00888520001899451,
          "uncompressed_bytes": 134712779,
          "window": "that"
        },
        {
          "compressed_bytes": 1211073,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04441279999446124,
          "path": "results/T-053/runs/k-ec2-001-03/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008104000007733703,
          "sha256": "7445df065d08ef178514bfba728a02472507525e956b1ed129924281dd43c546",
          "sha256_seconds": 0.0009791000047698617,
          "uncompressed_bytes": 23918820,
          "window": "that"
        },
        {
          "compressed_bytes": 12020473,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3779189999913797,
          "path": "results/T-053/runs/k-ec2-001-03/trung-gian.jsonl.gz",
          "read_seconds": 0.005414200015366077,
          "sha256": "337a08cac668ff83bfc10c2c1fc0f78a10bd36a2d91d870179d6c8bb78f5d7bb",
          "sha256_seconds": 0.009785800008103251,
          "uncompressed_bytes": 185688951,
          "window": "that"
        },
        {
          "compressed_bytes": 1506511,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07314600003883243,
          "path": "results/T-053/runs/k-ec2-001-05/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011146999895572662,
          "sha256": "06046b47c2f8b8573bbe0752d43dc914ff9d22135bdbf3ce98ecb8acad7e459d",
          "sha256_seconds": 0.0013825000496581197,
          "uncompressed_bytes": 39914943,
          "window": "that"
        },
        {
          "compressed_bytes": 14205823,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5466974999872036,
          "path": "results/T-053/runs/k-ec2-001-05/trung-gian.jsonl.gz",
          "read_seconds": 0.0068174999905750155,
          "sha256": "7da53b7268a273ca995e20c17dd5022d9cf9a6cbec98c2370147a222f035b21f",
          "sha256_seconds": 0.011561699968297035,
          "uncompressed_bytes": 291571079,
          "window": "that"
        },
        {
          "compressed_bytes": 912004,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.026561100035905838,
          "path": "results/T-053/runs/k-ec2-001-07/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004496999899856746,
          "sha256": "3513ce7a7e0574d4f88e919de439ceaa8a4c99a956b85dfaa3c17ede8de7b413",
          "sha256_seconds": 0.0007391000399366021,
          "uncompressed_bytes": 11115592,
          "window": "that"
        },
        {
          "compressed_bytes": 10626311,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.288621699961368,
          "path": "results/T-053/runs/k-ec2-001-07/trung-gian.jsonl.gz",
          "read_seconds": 0.004819699970539659,
          "sha256": "91fbf98ffc409b0ec72a7f3406875c91f3e437a566f135201e73f0a147efaef2",
          "sha256_seconds": 0.008571700018364936,
          "uncompressed_bytes": 122695627,
          "window": "that"
        },
        {
          "compressed_bytes": 1529752,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06639480002922937,
          "path": "results/T-053/runs/k-ec2-001-09/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009995000436902046,
          "sha256": "8f4bee30671bebe3b4bdf2da6fa19bb4e1e31827ec1d738e0a09ef82b8293842",
          "sha256_seconds": 0.001301499956753105,
          "uncompressed_bytes": 38415928,
          "window": "that"
        },
        {
          "compressed_bytes": 13632831,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5073681999929249,
          "path": "results/T-053/runs/k-ec2-001-09/trung-gian.jsonl.gz",
          "read_seconds": 0.00604510004632175,
          "sha256": "d7104f3bce70ce239bf581de094f64d29b73e179e3ae84759fec1e57d738970a",
          "sha256_seconds": 0.011262899963185191,
          "uncompressed_bytes": 261436987,
          "window": "that"
        },
        {
          "compressed_bytes": 1454832,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.061409000016283244,
          "path": "results/T-053/runs/k-ec2-001-11/ban-ghi.jsonl.gz",
          "read_seconds": 0.000880700012203306,
          "sha256": "81992f23e8535f8dbb03457e388d89507a687523b6e15cb31df191d96fa46227",
          "sha256_seconds": 0.001337599998805672,
          "uncompressed_bytes": 34263366,
          "window": "that"
        },
        {
          "compressed_bytes": 13258617,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.47060110000893474,
          "path": "results/T-053/runs/k-ec2-001-11/trung-gian.jsonl.gz",
          "read_seconds": 0.006002400012221187,
          "sha256": "3ea36301fb68ea1500138570f3b892e6a3fb90cdd8d2af2ac499b7adb8c9c9ca",
          "sha256_seconds": 0.010718200006522238,
          "uncompressed_bytes": 236970003,
          "window": "that"
        },
        {
          "compressed_bytes": 1462493,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06454469996970147,
          "path": "results/T-053/runs/k-ec2-001-13/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011340999626554549,
          "sha256": "a9a652093633b37079859a759d4e1c2c331097fd4fa9b62a6e1ecdd9a27920ff",
          "sha256_seconds": 0.001431700016837567,
          "uncompressed_bytes": 31360092,
          "window": "that"
        },
        {
          "compressed_bytes": 13021903,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4438510999898426,
          "path": "results/T-053/runs/k-ec2-001-13/trung-gian.jsonl.gz",
          "read_seconds": 0.006385799963027239,
          "sha256": "8dc9ac77f7ef04f0d916237a8d026d3e6bcddcd0842a054d3d14b74828ca9227",
          "sha256_seconds": 0.012583000003360212,
          "uncompressed_bytes": 213662183,
          "window": "that"
        },
        {
          "compressed_bytes": 697723,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.018187000008765608,
          "path": "results/T-053/runs/k-ec2-001-15/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004191999905742705,
          "sha256": "44e06790d2d897a589e11f677813b1f7b10a29443d308703829e04867b2fc6cf",
          "sha256_seconds": 0.0005704000359401107,
          "uncompressed_bytes": 6738444,
          "window": "that"
        },
        {
          "compressed_bytes": 9055563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.24461649998556823,
          "path": "results/T-053/runs/k-ec2-001-15/trung-gian.jsonl.gz",
          "read_seconds": 0.004668599984142929,
          "sha256": "23b1a85437c84b17676466b4d474b96c7b067a2891a31e644a1dcc079b1806f4",
          "sha256_seconds": 0.0076966999913565814,
          "uncompressed_bytes": 87378743,
          "window": "that"
        },
        {
          "compressed_bytes": 1601811,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06460029998561367,
          "path": "results/T-053/runs/k-ec2-001-17/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009963999618776143,
          "sha256": "2cf9afbac2b3c8cdc4c382aae3032aa0c356032f65912a31792419f474cbfbeb",
          "sha256_seconds": 0.00133790000109002,
          "uncompressed_bytes": 32437146,
          "window": "that"
        },
        {
          "compressed_bytes": 11856068,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3916437000152655,
          "path": "results/T-053/runs/k-ec2-001-17/trung-gian.jsonl.gz",
          "read_seconds": 0.005793899996206164,
          "sha256": "12ef2bbe14f73b0f7fccbed9ea20666a60ec9642d3461ee1d15a6d29f4e0a933",
          "sha256_seconds": 0.01275519997579977,
          "uncompressed_bytes": 175977559,
          "window": "that"
        },
        {
          "compressed_bytes": 1437712,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0603646999807097,
          "path": "results/T-053/runs/k-laptop-001-19/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009715999476611614,
          "sha256": "d6d49b9203bb9d7b52aeb5b30f9722a616f40c49d2389c5717a21299741636b7",
          "sha256_seconds": 0.0010464999941177666,
          "uncompressed_bytes": 32908784,
          "window": "that"
        },
        {
          "compressed_bytes": 13174562,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.5494796999846585,
          "path": "results/T-053/runs/k-laptop-001-19/trung-gian.jsonl.gz",
          "read_seconds": 0.0063532000058330595,
          "sha256": "5e7ce74f99932de6a8485552b3caba2a701b15946a5ef1c1472518f973c3bcc5",
          "sha256_seconds": 0.010517699993215501,
          "uncompressed_bytes": 231525955,
          "window": "that"
        },
        {
          "compressed_bytes": 1308686,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05815940001048148,
          "path": "results/T-053/runs/k-laptop-001-21/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008064999710768461,
          "sha256": "a93fa7657385f244c979e512cde318a4c77d6adbaf46175b6ce322478a0a7a01",
          "sha256_seconds": 0.0010792000102810562,
          "uncompressed_bytes": 25272765,
          "window": "that"
        },
        {
          "compressed_bytes": 12247809,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3947313000098802,
          "path": "results/T-053/runs/k-laptop-001-21/trung-gian.jsonl.gz",
          "read_seconds": 0.005705400020815432,
          "sha256": "02343f06330aeffb2cf02bcceee5bcf31df5fee844643c071684cf7b7e61ae27",
          "sha256_seconds": 0.012605099997017533,
          "uncompressed_bytes": 183184571,
          "window": "that"
        },
        {
          "compressed_bytes": 1524153,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06018879998009652,
          "path": "results/T-053/runs/k-laptop-001-23/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010933000012300909,
          "sha256": "84bc08057e635bed81733346a377457e85ffd62fbdd045f8c7a7f5db45e6da19",
          "sha256_seconds": 0.0012861000141128898,
          "uncompressed_bytes": 30628016,
          "window": "that"
        },
        {
          "compressed_bytes": 12651563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.41337880003266037,
          "path": "results/T-053/runs/k-laptop-001-23/trung-gian.jsonl.gz",
          "read_seconds": 0.005788100010249764,
          "sha256": "825c8cc75c8f7815247112c00369e899cb5bf7352e4fbeae994447f494175434",
          "sha256_seconds": 0.010108900023624301,
          "uncompressed_bytes": 195483455,
          "window": "that"
        },
        {
          "compressed_bytes": 1120525,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.048238700022920966,
          "path": "results/T-053/runs/k-laptop-001-25/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007825999637134373,
          "sha256": "52af893eaa19504b750286bc8ce5122956a0140a21d2b57bca73a65226c700c5",
          "sha256_seconds": 0.0009094999986700714,
          "uncompressed_bytes": 25257224,
          "window": "that"
        },
        {
          "compressed_bytes": 12510563,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.46681230003014207,
          "path": "results/T-053/runs/k-laptop-001-25/trung-gian.jsonl.gz",
          "read_seconds": 0.0055472999811172485,
          "sha256": "750efebe9210bc0fa18e90e469b06fd84731303a7d5880f68d8ac22b91e408e3",
          "sha256_seconds": 0.01096680003684014,
          "uncompressed_bytes": 220682353,
          "window": "that"
        },
        {
          "compressed_bytes": 1021014,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.037918100017122924,
          "path": "results/T-053/runs/k-laptop-001-27/ban-ghi.jsonl.gz",
          "read_seconds": 0.000464299984741956,
          "sha256": "1a330a7886f6957d92f01afbedca6c6af4a6fe196f77d839452ae66016d1dc01",
          "sha256_seconds": 0.000826300005428493,
          "uncompressed_bytes": 18377695,
          "window": "that"
        },
        {
          "compressed_bytes": 11577590,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.36913549999007955,
          "path": "results/T-053/runs/k-laptop-001-27/trung-gian.jsonl.gz",
          "read_seconds": 0.006855899991933256,
          "sha256": "429e32bacd9af45367f907b98817bd2290bc3b32aca8ae54de37b2bdf25738ab",
          "sha256_seconds": 0.011879699944984168,
          "uncompressed_bytes": 173121647,
          "window": "that"
        },
        {
          "compressed_bytes": 1624620,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06963350001024082,
          "path": "results/T-053/runs/k-laptop-001-29/ban-ghi.jsonl.gz",
          "read_seconds": 0.001032100000884384,
          "sha256": "1af2a35edbe4f969ad057837f5ae2694240764e289ce22d7dfa708818eefec80",
          "sha256_seconds": 0.001568300009239465,
          "uncompressed_bytes": 32677978,
          "window": "that"
        },
        {
          "compressed_bytes": 12330215,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.396484499971848,
          "path": "results/T-053/runs/k-laptop-001-29/trung-gian.jsonl.gz",
          "read_seconds": 0.0056108999997377396,
          "sha256": "a2a38682c2811c22fbd5accb650dcd85f851454936c5bc53b0bd6494b22dae62",
          "sha256_seconds": 0.010200999968219548,
          "uncompressed_bytes": 175000963,
          "window": "that"
        },
        {
          "compressed_bytes": 1901118,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.09090770001057535,
          "path": "results/T-053/runs/k-laptop-001-31/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010862999479286373,
          "sha256": "f0213ca394440f971a728586edc7ff5fb7e559a50795516e6ec1131033962fd4",
          "sha256_seconds": 0.0015913000097498298,
          "uncompressed_bytes": 44220284,
          "window": "that"
        },
        {
          "compressed_bytes": 13015137,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4419023999944329,
          "path": "results/T-053/runs/k-laptop-001-31/trung-gian.jsonl.gz",
          "read_seconds": 0.006001500005368143,
          "sha256": "fbb28c90630eedbce15e40488f38b531b43cfd99ee61057bb75b4acd5243b79e",
          "sha256_seconds": 0.010555399989243597,
          "uncompressed_bytes": 214444619,
          "window": "that"
        },
        {
          "compressed_bytes": 1727868,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06294850003905594,
          "path": "results/T-053/runs/k-laptop-001-33/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010124000255018473,
          "sha256": "d4422c480465b5b54d81e115d0e756706b5f5d45ca9a90f1a46f308f0f4ef259",
          "sha256_seconds": 0.0014664000482298434,
          "uncompressed_bytes": 32202962,
          "window": "that"
        },
        {
          "compressed_bytes": 12081207,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4050717999925837,
          "path": "results/T-053/runs/k-laptop-001-33/trung-gian.jsonl.gz",
          "read_seconds": 0.0054499999969266355,
          "sha256": "63d0714383e3ecc7ddf60c1c5c0246a28d72d30a0a30d16b1bbab80a13f3c55c",
          "sha256_seconds": 0.010297700006049126,
          "uncompressed_bytes": 161559683,
          "window": "that"
        },
        {
          "compressed_bytes": 2029706,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07365669996943325,
          "path": "results/T-053/runs/k-laptop-001-35/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011693999986164272,
          "sha256": "6fad7d180800c32d3ebb3c771a6b8caa4a1ae3879cac28f3956b523dc6995ac5",
          "sha256_seconds": 0.0016246999730356038,
          "uncompressed_bytes": 36896487,
          "window": "that"
        },
        {
          "compressed_bytes": 12213410,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.34466230001999065,
          "path": "results/T-053/runs/k-laptop-001-35/trung-gian.jsonl.gz",
          "read_seconds": 0.005813499970827252,
          "sha256": "14395cac23a72f46fe2d1683b90db30554fe10b683cfb8a926d38a0746c18a8a",
          "sha256_seconds": 0.01062750001437962,
          "uncompressed_bytes": 158345679,
          "window": "that"
        },
        {
          "compressed_bytes": 1216962,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03598190000047907,
          "path": "results/T-053/runs/k-laptop-001-37/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008871000027284026,
          "sha256": "e72f64ab11adf9aad4919b624f614143a6d8eb0815519773397585d515d89b74",
          "sha256_seconds": 0.001019700022879988,
          "uncompressed_bytes": 16457582,
          "window": "that"
        },
        {
          "compressed_bytes": 11071929,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.32631790003506467,
          "path": "results/T-053/runs/k-laptop-001-37/trung-gian.jsonl.gz",
          "read_seconds": 0.004937999998219311,
          "sha256": "491707df7e47f765ec4059326b2a4a8b4a976ee3d357c0bcf51ca9e17a5ef03c",
          "sha256_seconds": 0.009145099960733205,
          "uncompressed_bytes": 124267547,
          "window": "that"
        },
        {
          "compressed_bytes": 2194356,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.09138609998626634,
          "path": "results/T-053/runs/k-laptop-001-39/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011904000421054661,
          "sha256": "56df5f3e5e86728344887a5a3f05bd61b8147223f23444fda4ae088cb4d5df7e",
          "sha256_seconds": 0.0017529999604448676,
          "uncompressed_bytes": 42532030,
          "window": "that"
        },
        {
          "compressed_bytes": 12394216,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4084124999935739,
          "path": "results/T-053/runs/k-laptop-001-39/trung-gian.jsonl.gz",
          "read_seconds": 0.005556000047363341,
          "sha256": "9185ed0b2ff8b1d23ecdec7221183243b348080a088987c665f57dbddbd9bb3a",
          "sha256_seconds": 0.010090100055094808,
          "uncompressed_bytes": 168836655,
          "window": "that"
        },
        {
          "compressed_bytes": 1450045,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0480348999844864,
          "path": "results/T-053/runs/k-laptop-001-41/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008916000369936228,
          "sha256": "3c2570c53e1f84106b07c5fcfcedde3fbb147cd0fb21708c73efee0e2bfa3f9c",
          "sha256_seconds": 0.001172299962490797,
          "uncompressed_bytes": 22395444,
          "window": "that"
        },
        {
          "compressed_bytes": 11305153,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2932633000309579,
          "path": "results/T-053/runs/k-laptop-001-41/trung-gian.jsonl.gz",
          "read_seconds": 0.0053378999582491815,
          "sha256": "98631360b15819ef89c13568d0c5b373331e7becb1d15e3b138f877e86db1c88",
          "sha256_seconds": 0.009811000025365502,
          "uncompressed_bytes": 125650075,
          "window": "that"
        },
        {
          "compressed_bytes": 1158621,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03497219999553636,
          "path": "results/T-053/runs/k-laptop-001-43/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008991000358946621,
          "sha256": "d344459e6c3caef324fe0f4bdcce249391e6c2c3a239a6492946c0687abbf145",
          "sha256_seconds": 0.0009772999910637736,
          "uncompressed_bytes": 15323968,
          "window": "that"
        },
        {
          "compressed_bytes": 10915175,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2885628000367433,
          "path": "results/T-053/runs/k-laptop-001-43/trung-gian.jsonl.gz",
          "read_seconds": 0.004943100037053227,
          "sha256": "2fbdd6ac11435f2bdb30edc23b1df1c9ad9e67660a3b45809a242b9bcdfe423c",
          "sha256_seconds": 0.009480400010943413,
          "uncompressed_bytes": 120626663,
          "window": "that"
        },
        {
          "compressed_bytes": 1926747,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.07397430000128224,
          "path": "results/T-053/runs/k-laptop-001-45/ban-ghi.jsonl.gz",
          "read_seconds": 0.0010704000014811754,
          "sha256": "be17f0b895a10f2ba14afc3f9c1701587319fe91ef2c23fd326f6ceaa9b77efb",
          "sha256_seconds": 0.0016219999524764717,
          "uncompressed_bytes": 39614488,
          "window": "that"
        },
        {
          "compressed_bytes": 12158991,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3782731000101194,
          "path": "results/T-053/runs/k-laptop-001-45/trung-gian.jsonl.gz",
          "read_seconds": 0.005730100034270436,
          "sha256": "3b527f41c8e55b250432b65e13f55c5075385a0386ac20914cd97943de1bdd49",
          "sha256_seconds": 0.011004399973899126,
          "uncompressed_bytes": 167014867,
          "window": "that"
        },
        {
          "compressed_bytes": 1820788,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06671390001429245,
          "path": "results/T-053/runs/k-laptop-001-47/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011505999718792737,
          "sha256": "96fe3f9a3e1e9f8291fff869887b7d751ab12bb60137722ab9f414f5fef701d6",
          "sha256_seconds": 0.0017508000019006431,
          "uncompressed_bytes": 31131360,
          "window": "that"
        },
        {
          "compressed_bytes": 11466860,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2985157999792136,
          "path": "results/T-053/runs/k-laptop-001-47/trung-gian.jsonl.gz",
          "read_seconds": 0.00549680000403896,
          "sha256": "bbf9a3017fe5f5aefaafc39ef6097250e7a07c35539ca9b54c8fab8f4e2fb33e",
          "sha256_seconds": 0.009783000044990331,
          "uncompressed_bytes": 122066063,
          "window": "that"
        },
        {
          "compressed_bytes": 715285,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.019276800041552633,
          "path": "results/T-053/runs/k-laptop-001-49/ban-ghi.jsonl.gz",
          "read_seconds": 0.00044380000326782465,
          "sha256": "fc5835b12e7180e6e1748e42b095a47ce4c6a5f16cc132803a901039524ab062",
          "sha256_seconds": 0.0005842000246047974,
          "uncompressed_bytes": 7057958,
          "window": "that"
        },
        {
          "compressed_bytes": 7894721,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21943280001869425,
          "path": "results/T-053/runs/k-laptop-001-49/trung-gian.jsonl.gz",
          "read_seconds": 0.004239599977154285,
          "sha256": "fb7a3eff1679c9e460efd8856a4084471e1f43772153ae5cb7f871a79b2758ca",
          "sha256_seconds": 0.008908700023312122,
          "uncompressed_bytes": 82535995,
          "window": "that"
        },
        {
          "compressed_bytes": 744984,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01983440003823489,
          "path": "results/T-053/runs/k-laptop-001-51/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005649999948218465,
          "sha256": "607ead8ec0586d1acbb5096bcf48246086c8e5477bd2b4074fcd46f807eafcaa",
          "sha256_seconds": 0.000632000039331615,
          "uncompressed_bytes": 7393906,
          "window": "that"
        },
        {
          "compressed_bytes": 8121013,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2207740999874659,
          "path": "results/T-053/runs/k-laptop-001-51/trung-gian.jsonl.gz",
          "read_seconds": 0.0037175000179558992,
          "sha256": "99ff97a4d0802c105b5d1b1bcafe5dfb41c9c21676da1e53b6f6272e39265710",
          "sha256_seconds": 0.006537800014484674,
          "uncompressed_bytes": 85003363,
          "window": "that"
        },
        {
          "compressed_bytes": 651309,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016378000029362738,
          "path": "results/T-053/runs/k-ec2-001-53/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006393999792635441,
          "sha256": "ce9efd08e684b3952690e3e9f40d2a957ff5bd345c4902869cf7e3d2b00453ec",
          "sha256_seconds": 0.0005582000012509525,
          "uncompressed_bytes": 5781838,
          "window": "that"
        },
        {
          "compressed_bytes": 7651796,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20078579999972135,
          "path": "results/T-053/runs/k-ec2-001-53/trung-gian.jsonl.gz",
          "read_seconds": 0.00359879998723045,
          "sha256": "a69a0a0d395329d5e6fe3df91dd04c6162330b8fae3dadaa7fd038849c80b362",
          "sha256_seconds": 0.00709100003587082,
          "uncompressed_bytes": 79787459,
          "window": "that"
        },
        {
          "compressed_bytes": 572877,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.014623600000049919,
          "path": "results/T-053/runs/k-laptop-001-55/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003940000315196812,
          "sha256": "6c249a119428210a042ae5853133d3db83ec6ffef83371bd3d48a7782d200f5b",
          "sha256_seconds": 0.0005149999633431435,
          "uncompressed_bytes": 5250760,
          "window": "that"
        },
        {
          "compressed_bytes": 7520043,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20153889997163787,
          "path": "results/T-053/runs/k-laptop-001-55/trung-gian.jsonl.gz",
          "read_seconds": 0.0036240999470464885,
          "sha256": "7409c3ad63a9e14949b7d3b63562224e05bfc0b28b9f5949c821bba46ac17205",
          "sha256_seconds": 0.005981800029985607,
          "uncompressed_bytes": 79770251,
          "window": "that"
        },
        {
          "compressed_bytes": 709905,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.017721999960485846,
          "path": "results/T-053/runs/k-ec2-001-57/ban-ghi.jsonl.gz",
          "read_seconds": 0.00044430000707507133,
          "sha256": "5bc0924b893ef1431718708888feac2f162119a237398be81cd6c67bf19de557",
          "sha256_seconds": 0.000582900014705956,
          "uncompressed_bytes": 6150430,
          "window": "that"
        },
        {
          "compressed_bytes": 7826386,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.1983662000275217,
          "path": "results/T-053/runs/k-ec2-001-57/trung-gian.jsonl.gz",
          "read_seconds": 0.0039056999958120286,
          "sha256": "4f929b8a8e0c5ba47a61d5a4162c9a2279c5c1de714c2a54c6827b8345b6d2a8",
          "sha256_seconds": 0.007672499981708825,
          "uncompressed_bytes": 80020419,
          "window": "that"
        },
        {
          "compressed_bytes": 584569,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01596290001180023,
          "path": "results/T-053/runs/k-laptop-001-59/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005735000013373792,
          "sha256": "24555e3264d14896dab7a0f64d1ad9f748f4a2c0ee4e8b2b6ff04fd20cb14f8a",
          "sha256_seconds": 0.0004993999609723687,
          "uncompressed_bytes": 5339750,
          "window": "that"
        },
        {
          "compressed_bytes": 7569096,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20578600000590086,
          "path": "results/T-053/runs/k-laptop-001-59/trung-gian.jsonl.gz",
          "read_seconds": 0.0036906999885104597,
          "sha256": "e1f3c45b4149162b699648651d440bdc9cc4fca18183fbf67c29899021ce5636",
          "sha256_seconds": 0.006167499988805503,
          "uncompressed_bytes": 79862367,
          "window": "that"
        },
        {
          "compressed_bytes": 305347,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008382300031371415,
          "path": "results/T-053/runs/k-laptop-001-60/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003545999643392861,
          "sha256": "0dd7411e9b5658cf3a79c03202de0fc08e270ecb632df11466c13198d63e3c79",
          "sha256_seconds": 0.0002618000144138932,
          "uncompressed_bytes": 2716616,
          "window": "that"
        },
        {
          "compressed_bytes": 3974396,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10123109997948632,
          "path": "results/T-053/runs/k-laptop-001-60/trung-gian.jsonl.gz",
          "read_seconds": 0.0019285999587737024,
          "sha256": "2513e6661e0025719df043e6fb1afbfc957133ea227778e13388f3a172440ab7",
          "sha256_seconds": 0.0034503000206314027,
          "uncompressed_bytes": 40972501,
          "window": "that"
        },
        {
          "compressed_bytes": 341179,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00930149998748675,
          "path": "results/T-053/runs/k-laptop-001-61/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003462000167928636,
          "sha256": "8f5c9382c110ece04b5a72683d77febf1f2893858cd2ff13ee880cb63f91788f",
          "sha256_seconds": 0.00030559999868273735,
          "uncompressed_bytes": 3443758,
          "window": "that"
        },
        {
          "compressed_bytes": 3838027,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09549460001289845,
          "path": "results/T-053/runs/k-laptop-001-61/trung-gian.jsonl.gz",
          "read_seconds": 0.0018505000043660402,
          "sha256": "0e327fd9e046caf9fe231cacacdc65124526697e829df1f53ba3f32ffe697cc7",
          "sha256_seconds": 0.003130699973553419,
          "uncompressed_bytes": 39155871,
          "window": "that"
        },
        {
          "compressed_bytes": 301761,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007729700009804219,
          "path": "results/T-053/runs/k-ec2-001-62/ban-ghi.jsonl.gz",
          "read_seconds": 0.00033389998134225607,
          "sha256": "df43c95a85b060ffd6115ec7d722fe5bf995028bc278cd100d822556f428ca47",
          "sha256_seconds": 0.0002660999889485538,
          "uncompressed_bytes": 2805104,
          "window": "that"
        },
        {
          "compressed_bytes": 3786480,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09464719996321946,
          "path": "results/T-053/runs/k-ec2-001-62/trung-gian.jsonl.gz",
          "read_seconds": 0.0018283999525010586,
          "sha256": "30cb64e0ec32c68bacce85e7dabad15523fe28e53a13450b1e3e0a68c55c08d1",
          "sha256_seconds": 0.003038400027435273,
          "uncompressed_bytes": 38972687,
          "window": "that"
        },
        {
          "compressed_bytes": 287444,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008026499999687076,
          "path": "results/T-053/runs/k-laptop-001-63/ban-ghi.jsonl.gz",
          "read_seconds": 0.00037640001391991973,
          "sha256": "8d0f49ad670dcac6aed6d4b5c8f047f013c8b375e1ad57988bb4ef46723d71fa",
          "sha256_seconds": 0.00025019998429343104,
          "uncompressed_bytes": 2729068,
          "window": "that"
        },
        {
          "compressed_bytes": 3896093,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10824349999893457,
          "path": "results/T-053/runs/k-laptop-001-63/trung-gian.jsonl.gz",
          "read_seconds": 0.0018479000427760184,
          "sha256": "54be33cde2df3fbf6f4ac2c5475c3b0d7a59e44972737b3dd5ae61c46b2b7ed9",
          "sha256_seconds": 0.0033106000046245754,
          "uncompressed_bytes": 39966955,
          "window": "that"
        },
        {
          "compressed_bytes": 275083,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007475999998860061,
          "path": "results/T-053/runs/k-ec2-001-64/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003372000064700842,
          "sha256": "2fa8d5836feb53e8f11d6b23c9b7fefa65f45c337d640bbb14dde1f791552d13",
          "sha256_seconds": 0.0002367999986745417,
          "uncompressed_bytes": 2519221,
          "window": "that"
        },
        {
          "compressed_bytes": 3896491,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11172149999765679,
          "path": "results/T-053/runs/k-ec2-001-64/trung-gian.jsonl.gz",
          "read_seconds": 0.001950100006069988,
          "sha256": "54aa46dd9999cf9b91121994531c9ae2b5004acc65fd86da55369e0dc61c996f",
          "sha256_seconds": 0.003203700005542487,
          "uncompressed_bytes": 40355317,
          "window": "that"
        },
        {
          "compressed_bytes": 293276,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007673000043723732,
          "path": "results/T-053/runs/k-laptop-001-65/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003565000370144844,
          "sha256": "90367e4fcafebac2912ab7c7c4085e627df1e3989295faf8fbf86fc6d90a8b2f",
          "sha256_seconds": 0.0002533000078983605,
          "uncompressed_bytes": 2772140,
          "window": "that"
        },
        {
          "compressed_bytes": 3932031,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11283369996817783,
          "path": "results/T-053/runs/k-laptop-001-65/trung-gian.jsonl.gz",
          "read_seconds": 0.001833299989812076,
          "sha256": "5f8772ea75ef48ccc38a3f41e650a446d257b889f2b6b2d4c8b1cb7fb5d3ee8b",
          "sha256_seconds": 0.003122100024484098,
          "uncompressed_bytes": 40484475,
          "window": "that"
        },
        {
          "compressed_bytes": 342290,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.009554999996908009,
          "path": "results/T-053/runs/k-ec2-001-66/ban-ghi.jsonl.gz",
          "read_seconds": 0.00038270000368356705,
          "sha256": "a69a15fb916c3ef8cfeedc6539ca10c9217ee113008c304dc84223b04e26e721",
          "sha256_seconds": 0.000292200013063848,
          "uncompressed_bytes": 3700480,
          "window": "that"
        },
        {
          "compressed_bytes": 3974672,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.12481519998982549,
          "path": "results/T-053/runs/k-ec2-001-66/trung-gian.jsonl.gz",
          "read_seconds": 0.0020345000084489584,
          "sha256": "789e66c5ce8fee30909f94ef06e688a7504d7a94f9790c678d26b4d9bca72042",
          "sha256_seconds": 0.003309599997010082,
          "uncompressed_bytes": 40655023,
          "window": "that"
        },
        {
          "compressed_bytes": 283317,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.010011399979703128,
          "path": "results/T-053/runs/k-laptop-001-67/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005140999564900994,
          "sha256": "3d8a4d9f5c52a061f2cbae1cedfa803d04551aac5a3fd98d79d615c85409d7d1",
          "sha256_seconds": 0.0003902000025846064,
          "uncompressed_bytes": 2514478,
          "window": "that"
        },
        {
          "compressed_bytes": 3891416,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.1058138000080362,
          "path": "results/T-053/runs/k-laptop-001-67/trung-gian.jsonl.gz",
          "read_seconds": 0.002666399988811463,
          "sha256": "72e3b10e7527807301a1b0e5007c4a6e3f3d3ab43f9e9ab43d40fe272a3a8307",
          "sha256_seconds": 0.005257599987089634,
          "uncompressed_bytes": 39976545,
          "window": "that"
        },
        {
          "compressed_bytes": 300771,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008120999962557107,
          "path": "results/T-053/runs/k-ec2-001-68/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003522000042721629,
          "sha256": "440e83e3a36edc6c8914bc8a3060ca35ed6dbed689eef7e265267705f8140cb5",
          "sha256_seconds": 0.00026000000070780516,
          "uncompressed_bytes": 2998948,
          "window": "that"
        },
        {
          "compressed_bytes": 3904340,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09727959998417646,
          "path": "results/T-053/runs/k-ec2-001-68/trung-gian.jsonl.gz",
          "read_seconds": 0.0019286000169813633,
          "sha256": "2078a45ac731cad1b749c5e28e3cee5be4085f82092de3ed999df1eee28ad657",
          "sha256_seconds": 0.003332899999804795,
          "uncompressed_bytes": 40318739,
          "window": "that"
        },
        {
          "compressed_bytes": 324595,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008927699993364513,
          "path": "results/T-053/runs/k-laptop-001-69/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003559999749995768,
          "sha256": "8daa11d32e5a44c3f4fe7cd0bb47233f73f58086f28bbedeab681ea107469320",
          "sha256_seconds": 0.0002761000068858266,
          "uncompressed_bytes": 3629992,
          "window": "that"
        },
        {
          "compressed_bytes": 3991223,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09744729998055845,
          "path": "results/T-053/runs/k-laptop-001-69/trung-gian.jsonl.gz",
          "read_seconds": 0.0019942999933846295,
          "sha256": "0939ffed635ef570a23f73502fff1745c5ee29247dc3e183b02143916a44cf97",
          "sha256_seconds": 0.003191599971614778,
          "uncompressed_bytes": 40506131,
          "window": "that"
        },
        {
          "compressed_bytes": 312779,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008070799987763166,
          "path": "results/T-053/runs/k-laptop-001-70/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003277999931015074,
          "sha256": "c453ef3b06631bdcbd765b13d2bc996f58aa72467fb161cf01da8e3e43b77e6c",
          "sha256_seconds": 0.00027870002668350935,
          "uncompressed_bytes": 3030144,
          "window": "that"
        },
        {
          "compressed_bytes": 3751224,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09370089997537434,
          "path": "results/T-053/runs/k-laptop-001-70/trung-gian.jsonl.gz",
          "read_seconds": 0.0017597000114619732,
          "sha256": "880b45db415000b3bffc53071202062bd93b5eb5cabfd71109e43651e79e7a82",
          "sha256_seconds": 0.002985099970828742,
          "uncompressed_bytes": 38824207,
          "window": "that"
        },
        {
          "compressed_bytes": 328632,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008573299972340465,
          "path": "results/T-053/runs/k-ec2-001-71/ban-ghi.jsonl.gz",
          "read_seconds": 0.00031109998235478997,
          "sha256": "52b561930012f392ee09a1e5560b7ef7f3b773b4aa8ca0baca9c8a08bcd1e4da",
          "sha256_seconds": 0.0002785000251606107,
          "uncompressed_bytes": 3299322,
          "window": "that"
        },
        {
          "compressed_bytes": 3853950,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10486940003465861,
          "path": "results/T-053/runs/k-ec2-001-71/trung-gian.jsonl.gz",
          "read_seconds": 0.0019478999893181026,
          "sha256": "85507e9707851e673f9cb6e7a669feff476b15ab65d56e9c78f84c41e7a983a5",
          "sha256_seconds": 0.0031817000126466155,
          "uncompressed_bytes": 39563907,
          "window": "that"
        },
        {
          "compressed_bytes": 266522,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00896830001147464,
          "path": "results/T-053/runs/k-laptop-001-72/ban-ghi.jsonl.gz",
          "read_seconds": 0.000304599991068244,
          "sha256": "2a3c4dccd2ae3cac1a3162333a6048c318d8e98a1f98e74e0cc61e494bb50c36",
          "sha256_seconds": 0.00023070001043379307,
          "uncompressed_bytes": 2577062,
          "window": "that"
        },
        {
          "compressed_bytes": 3691929,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09701660001883283,
          "path": "results/T-053/runs/k-laptop-001-72/trung-gian.jsonl.gz",
          "read_seconds": 0.0027497000410221517,
          "sha256": "308ae6d97bf5bfbecb31c8f01d6b31eb6f4d6ef894d4410381ef85b592420466",
          "sha256_seconds": 0.0045779000502079725,
          "uncompressed_bytes": 39419215,
          "window": "that"
        },
        {
          "compressed_bytes": 291264,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007410099962726235,
          "path": "results/T-053/runs/k-ec2-001-73/ban-ghi.jsonl.gz",
          "read_seconds": 0.00036860001273453236,
          "sha256": "36f94634e75a29376fa771fca1c813479707f9660aa29a1818331ee136983dcf",
          "sha256_seconds": 0.0002607000060379505,
          "uncompressed_bytes": 2516770,
          "window": "that"
        },
        {
          "compressed_bytes": 3869047,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10608900000806898,
          "path": "results/T-053/runs/k-ec2-001-73/trung-gian.jsonl.gz",
          "read_seconds": 0.0019314999808557332,
          "sha256": "6fa3d8223c742bb850a72de12c8eb8fbdad1e770444bbf0b2115e26f6976b9b9",
          "sha256_seconds": 0.0032167999888770282,
          "uncompressed_bytes": 39967175,
          "window": "that"
        },
        {
          "compressed_bytes": 343078,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00990449998062104,
          "path": "results/T-053/runs/k-laptop-001-74/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003326000296510756,
          "sha256": "cdadcf7688a087977cdc9586b2f1b63c09be39d8231cbcff3718240fad056943",
          "sha256_seconds": 0.0002954999799840152,
          "uncompressed_bytes": 4028666,
          "window": "that"
        },
        {
          "compressed_bytes": 4034224,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11669240001356229,
          "path": "results/T-053/runs/k-laptop-001-74/trung-gian.jsonl.gz",
          "read_seconds": 0.0019410999957472086,
          "sha256": "2b010aadc67fd9ad063108aa8789311929aed0b1fdc509342db4b1b85edc7345",
          "sha256_seconds": 0.0032432000152766705,
          "uncompressed_bytes": 41238355,
          "window": "that"
        },
        {
          "compressed_bytes": 289346,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007954899978358299,
          "path": "results/T-053/runs/k-ec2-001-75/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003872000379487872,
          "sha256": "2db978ca1d8b19086bb2dba1a149c0eda9d80bb0b7668b6a53ceea7431da3a7f",
          "sha256_seconds": 0.00029420002829283476,
          "uncompressed_bytes": 2795152,
          "window": "that"
        },
        {
          "compressed_bytes": 3868648,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.11212169995997101,
          "path": "results/T-053/runs/k-ec2-001-75/trung-gian.jsonl.gz",
          "read_seconds": 0.0018177999882027507,
          "sha256": "c11f613f0718904f556007e0a1fa87cf793ce1f7fa65d30162e12cf02838752f",
          "sha256_seconds": 0.003095499996561557,
          "uncompressed_bytes": 40323611,
          "window": "that"
        },
        {
          "compressed_bytes": 355753,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.010765699960757047,
          "path": "results/T-053/runs/k-laptop-001-76/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004835999570786953,
          "sha256": "82276f61a538cd31e7e3b4b0b550a02ab9fd9e7f3782eb280a9e8a0a53befbfa",
          "sha256_seconds": 0.00033950002398341894,
          "uncompressed_bytes": 3487352,
          "window": "that"
        },
        {
          "compressed_bytes": 4010532,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.13441729999613017,
          "path": "results/T-053/runs/k-laptop-001-76/trung-gian.jsonl.gz",
          "read_seconds": 0.0028087000246159732,
          "sha256": "60a72f36ef04432d9dc9283fc35fe19d3e117d1f46659a55c1a0e9ac736af1ca",
          "sha256_seconds": 0.005316800030414015,
          "uncompressed_bytes": 40133007,
          "window": "that"
        },
        {
          "compressed_bytes": 287307,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007765499991364777,
          "path": "results/T-053/runs/k-ec2-001-77/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003136999439448118,
          "sha256": "cc354213a397dde3eebf754db6286f684fdd369affb1c27292089af1be7ac20c",
          "sha256_seconds": 0.0002460000105202198,
          "uncompressed_bytes": 2969390,
          "window": "that"
        },
        {
          "compressed_bytes": 3736657,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10250839998479933,
          "path": "results/T-053/runs/k-ec2-001-77/trung-gian.jsonl.gz",
          "read_seconds": 0.0017903000116348267,
          "sha256": "cdc86defe3a4b7b45c0650041d604db39fb552882da20966645beb9ad750964c",
          "sha256_seconds": 0.0031083999783731997,
          "uncompressed_bytes": 39325551,
          "window": "that"
        },
        {
          "compressed_bytes": 327110,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.010515699977986515,
          "path": "results/T-053/runs/k-laptop-001-78/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003247999702580273,
          "sha256": "0e3d2a2dd4c946315ae16e35ece45f936d787f2a91272bc6d7db7cd334452a8c",
          "sha256_seconds": 0.00027950003277510405,
          "uncompressed_bytes": 4341406,
          "window": "that"
        },
        {
          "compressed_bytes": 3727958,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.12226380000356585,
          "path": "results/T-053/runs/k-laptop-001-78/trung-gian.jsonl.gz",
          "read_seconds": 0.002304399968124926,
          "sha256": "5a04689d118a2d809facc41594a1e4971b999d1e8a8e0369910ec6a28d00c99e",
          "sha256_seconds": 0.004454799985978752,
          "uncompressed_bytes": 39169783,
          "window": "that"
        },
        {
          "compressed_bytes": 292508,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.008973599993623793,
          "path": "results/T-053/runs/k-ec2-001-79/ban-ghi.jsonl.gz",
          "read_seconds": 0.00041939999209716916,
          "sha256": "1f7443e4993e51a4c0c8de3f06a1c21039fb51e614f0f1144573b7363424a214",
          "sha256_seconds": 0.0003407999756745994,
          "uncompressed_bytes": 2791138,
          "window": "that"
        },
        {
          "compressed_bytes": 3646720,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10191430000122637,
          "path": "results/T-053/runs/k-ec2-001-79/trung-gian.jsonl.gz",
          "read_seconds": 0.0017528000171296299,
          "sha256": "6b0b92b8339f237192fb2e190883aa6b403abc02fb553094c14319082675112c",
          "sha256_seconds": 0.002920099999755621,
          "uncompressed_bytes": 38971479,
          "window": "that"
        },
        {
          "compressed_bytes": 283078,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.007961900031659752,
          "path": "results/T-053/runs/k-laptop-001-80/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003847999614663422,
          "sha256": "8f2a4ec826191007574a0a2af4e915b9ac53afa04e68f9915d002ba513d93f72",
          "sha256_seconds": 0.00028799998108297586,
          "uncompressed_bytes": 2748956,
          "window": "that"
        },
        {
          "compressed_bytes": 3771582,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.09612030000425875,
          "path": "results/T-053/runs/k-laptop-001-80/trung-gian.jsonl.gz",
          "read_seconds": 0.0020708999945782125,
          "sha256": "d2bd73949f5c621e6b625cfb92ea9c2263a83deef4775a8cf024de2666217415",
          "sha256_seconds": 0.0030024999869056046,
          "uncompressed_bytes": 40029691,
          "window": "that"
        },
        {
          "compressed_bytes": 328933,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.00913700001547113,
          "path": "results/T-053/runs/k-laptop-001-81/ban-ghi.jsonl.gz",
          "read_seconds": 0.00033840001560747623,
          "sha256": "6ced253bdc2c0dbfa8e1a995d85c86ab0457dabd35092b2babaa4d366988a50f",
          "sha256_seconds": 0.00029200001154094934,
          "uncompressed_bytes": 3596202,
          "window": "that"
        },
        {
          "compressed_bytes": 3682667,
          "dataset": "Nezha-OB",
          "gzip_inflate_seconds": 0.10154270002385601,
          "path": "results/T-053/runs/k-laptop-001-81/trung-gian.jsonl.gz",
          "read_seconds": 0.0020423000096343458,
          "sha256": "3ec6ae7e2d6a99221831e247fa1a64f9f3e84e81aa328e400cfd65cc33885194",
          "sha256_seconds": 0.003339999995660037,
          "uncompressed_bytes": 39155415,
          "window": "that"
        },
        {
          "compressed_bytes": 822599,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.023748099978547543,
          "path": "results/T-053/runs/k-ec2-001-00/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004256999818608165,
          "sha256": "ed24a93ac64a50ea46a0aad7acc457e7eeb6e26874aabb3c759aa8838b040479",
          "sha256_seconds": 0.0006685000262223184,
          "uncompressed_bytes": 10658924,
          "window": "ce"
        },
        {
          "compressed_bytes": 10448405,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3036171999992803,
          "path": "results/T-053/runs/k-ec2-001-00/trung-gian.jsonl.gz",
          "read_seconds": 0.004728899977635592,
          "sha256": "11e624246795f6810585f9d205d3c5a94ceda032433a994837b060057d58622d",
          "sha256_seconds": 0.00873840000713244,
          "uncompressed_bytes": 129551287,
          "window": "ce"
        },
        {
          "compressed_bytes": 1029305,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04988910001702607,
          "path": "results/T-053/runs/k-ec2-001-02/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004705000319518149,
          "sha256": "52800ca5a7bc6c2c54c944799978a6f3b987805aeaebf5c7b84c5152661a5b76",
          "sha256_seconds": 0.0008477000519633293,
          "uncompressed_bytes": 22105346,
          "window": "ce"
        },
        {
          "compressed_bytes": 11951000,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.421052299963776,
          "path": "results/T-053/runs/k-ec2-001-02/trung-gian.jsonl.gz",
          "read_seconds": 0.006131799949798733,
          "sha256": "8ce4f7944c842354f3e9dd08220d2b10f9892a9db369ee4314a825f387498c2e",
          "sha256_seconds": 0.012088000017683953,
          "uncompressed_bytes": 202647183,
          "window": "ce"
        },
        {
          "compressed_bytes": 1301350,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06590270000742748,
          "path": "results/T-053/runs/k-ec2-001-04/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009365000296384096,
          "sha256": "716bdcf17af9aa5f5fdd43db5391d9184e5bc9b7df225eda6aeb601ae26f4df9",
          "sha256_seconds": 0.0011078000534325838,
          "uncompressed_bytes": 34024670,
          "window": "ce"
        },
        {
          "compressed_bytes": 13506076,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.526502900000196,
          "path": "results/T-053/runs/k-ec2-001-04/trung-gian.jsonl.gz",
          "read_seconds": 0.005956599954515696,
          "sha256": "528d6cf135e22cca572fe748b72cd783e99fa64ae3f1882dcf9b2a3517a4c73f",
          "sha256_seconds": 0.011930200038477778,
          "uncompressed_bytes": 273072439,
          "window": "ce"
        },
        {
          "compressed_bytes": 848351,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.026833699957933277,
          "path": "results/T-053/runs/k-laptop-001-06/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005601999582722783,
          "sha256": "7d3a62322d7fa81e06f79cf7581c5502c7c9ae0ca1ae28e5e23d5b9cfb9278ec",
          "sha256_seconds": 0.0007227000314742327,
          "uncompressed_bytes": 10436336,
          "window": "ce"
        },
        {
          "compressed_bytes": 10527125,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.307496799970977,
          "path": "results/T-053/runs/k-laptop-001-06/trung-gian.jsonl.gz",
          "read_seconds": 0.004977000004146248,
          "sha256": "2937f20e792bca64705880429da652c20efbdaafd52da542db37d32fe1e62fb9",
          "sha256_seconds": 0.009004399995319545,
          "uncompressed_bytes": 127666383,
          "window": "ce"
        },
        {
          "compressed_bytes": 1210453,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05252289999043569,
          "path": "results/T-053/runs/k-laptop-001-08/ban-ghi.jsonl.gz",
          "read_seconds": 0.0009199999622069299,
          "sha256": "6051c36119c0dd155ca24ff3eae9e13ba75dd39bbcff45271f091d344ec0678e",
          "sha256_seconds": 0.0010380999883636832,
          "uncompressed_bytes": 30070960,
          "window": "ce"
        },
        {
          "compressed_bytes": 13235549,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.49180090002482757,
          "path": "results/T-053/runs/k-laptop-001-08/trung-gian.jsonl.gz",
          "read_seconds": 0.005980100017040968,
          "sha256": "a45364647592d150571c8d9f7fb88c716bcfe73788bbcd8e8179f9cb8d43e1f7",
          "sha256_seconds": 0.010911300021689385,
          "uncompressed_bytes": 255235467,
          "window": "ce"
        },
        {
          "compressed_bytes": 1202287,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0533467999775894,
          "path": "results/T-053/runs/k-laptop-001-10/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008002999820746481,
          "sha256": "fc45a2d498a59663275e97874c9b7162b366ed702deff44747d709acec6aab41",
          "sha256_seconds": 0.0009881000150926411,
          "uncompressed_bytes": 29958852,
          "window": "ce"
        },
        {
          "compressed_bytes": 12988601,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4704486000118777,
          "path": "results/T-053/runs/k-laptop-001-10/trung-gian.jsonl.gz",
          "read_seconds": 0.005825400003232062,
          "sha256": "4682bb3ba56c94601ea6029ec7b2c011d4c246e252c5da8b3422d6af92fb5a5b",
          "sha256_seconds": 0.010545299970544875,
          "uncompressed_bytes": 251420055,
          "window": "ce"
        },
        {
          "compressed_bytes": 1225981,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.052705599984619766,
          "path": "results/T-053/runs/k-laptop-001-12/ban-ghi.jsonl.gz",
          "read_seconds": 0.000804400013294071,
          "sha256": "77364ade249f19b3ea86a0ebe18732c97a57d36a5263b5daf3b765b931008549",
          "sha256_seconds": 0.0010039000189863145,
          "uncompressed_bytes": 25913566,
          "window": "ce"
        },
        {
          "compressed_bytes": 12796748,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4829130000434816,
          "path": "results/T-053/runs/k-laptop-001-12/trung-gian.jsonl.gz",
          "read_seconds": 0.005850599962286651,
          "sha256": "462f6413a5578f5dd5e5c46eae73ce799167103099a9c80bed8a1f80b159353a",
          "sha256_seconds": 0.0107533999835141,
          "uncompressed_bytes": 217715263,
          "window": "ce"
        },
        {
          "compressed_bytes": 577147,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015285100031178445,
          "path": "results/T-053/runs/k-laptop-001-14/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004883999936282635,
          "sha256": "1f53468d8c7d30bc4d60c52e6b75d74f00cc3821ba68c24ad0cca89777e42203",
          "sha256_seconds": 0.0006476000417023897,
          "uncompressed_bytes": 4873430,
          "window": "ce"
        },
        {
          "compressed_bytes": 8793133,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.22876369999721646,
          "path": "results/T-053/runs/k-laptop-001-14/trung-gian.jsonl.gz",
          "read_seconds": 0.00401059997966513,
          "sha256": "b826ba03189af82b66b5c85904a9803184be178c0c6815c74d1ed69e665f69aa",
          "sha256_seconds": 0.007078399998135865,
          "uncompressed_bytes": 86528619,
          "window": "ce"
        },
        {
          "compressed_bytes": 1210062,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05349139997269958,
          "path": "results/T-053/runs/k-ec2-001-16/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008029000018723309,
          "sha256": "ce03562948dec6729110e499039c9791a6b0d5acaccab061f555d98b873f261c",
          "sha256_seconds": 0.0009867000044323504,
          "uncompressed_bytes": 30948408,
          "window": "ce"
        },
        {
          "compressed_bytes": 13026484,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.49718089995440096,
          "path": "results/T-053/runs/k-ec2-001-16/trung-gian.jsonl.gz",
          "read_seconds": 0.006005900038871914,
          "sha256": "dcdababff7ef122b9acbbfb1c541ff20becbf0510384bf0b6e41f758ce6434a3",
          "sha256_seconds": 0.012403099972289056,
          "uncompressed_bytes": 259912347,
          "window": "ce"
        },
        {
          "compressed_bytes": 1056011,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.038975599978584796,
          "path": "results/T-053/runs/k-laptop-001-18/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007960000075399876,
          "sha256": "a58cbe37868ac806fa277eda558df530dd9f29cbfc3d6d7724c6b65db08b5dfa",
          "sha256_seconds": 0.0008617999847047031,
          "uncompressed_bytes": 20764174,
          "window": "ce"
        },
        {
          "compressed_bytes": 12047687,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.40371699997922406,
          "path": "results/T-053/runs/k-laptop-001-18/trung-gian.jsonl.gz",
          "read_seconds": 0.005405300005804747,
          "sha256": "d415b17115dde04e3dbcd0b173ae35d2ffb397e835f05d23f2b5f396da4dd058",
          "sha256_seconds": 0.01004069996997714,
          "uncompressed_bytes": 191215491,
          "window": "ce"
        },
        {
          "compressed_bytes": 1078891,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03867699997499585,
          "path": "results/T-053/runs/k-laptop-001-20/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006984000210650265,
          "sha256": "44a2c2ca61ee06102b40d97b4105b9fd1871d25c442b06fcbf68be36ec7363f2",
          "sha256_seconds": 0.0008779999916441739,
          "uncompressed_bytes": 17297772,
          "window": "ce"
        },
        {
          "compressed_bytes": 11535920,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.34405539999715984,
          "path": "results/T-053/runs/k-laptop-001-20/trung-gian.jsonl.gz",
          "read_seconds": 0.005473199998959899,
          "sha256": "7c26270a80ddca65ce9af26d5d3176f5a0fbd0129b8de13c59099379970f078b",
          "sha256_seconds": 0.011484399961773306,
          "uncompressed_bytes": 155876335,
          "window": "ce"
        },
        {
          "compressed_bytes": 1167638,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04592780000530183,
          "path": "results/T-053/runs/k-ec2-001-22/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007698000408709049,
          "sha256": "2b4c9c639393e2db909054671363d72a3d1344f0b36c921c4307715d6b60d517",
          "sha256_seconds": 0.0009488999494351447,
          "uncompressed_bytes": 23457226,
          "window": "ce"
        },
        {
          "compressed_bytes": 12337820,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4525553999701515,
          "path": "results/T-053/runs/k-ec2-001-22/trung-gian.jsonl.gz",
          "read_seconds": 0.005623199976980686,
          "sha256": "c7848f76949bef5f5d0c4c3932c8d61611e2b1108a347eb5530d70c88f008d1a",
          "sha256_seconds": 0.010135499993339181,
          "uncompressed_bytes": 201534451,
          "window": "ce"
        },
        {
          "compressed_bytes": 1032006,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03799409995554015,
          "path": "results/T-053/runs/k-laptop-001-24/ban-ghi.jsonl.gz",
          "read_seconds": 0.00047800003085285425,
          "sha256": "d4a806c8cc51c8964d06ec88d1624e4e5c20275fbe77eea59a25f40eb5abd4c7",
          "sha256_seconds": 0.0009160999907180667,
          "uncompressed_bytes": 18208454,
          "window": "ce"
        },
        {
          "compressed_bytes": 11749340,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.39741820003837347,
          "path": "results/T-053/runs/k-laptop-001-24/trung-gian.jsonl.gz",
          "read_seconds": 0.005235399992670864,
          "sha256": "959e3d6c62df4d2206896a7c1090edfcff818a07726a3be1957820e94bfa32e8",
          "sha256_seconds": 0.010096500045619905,
          "uncompressed_bytes": 170164895,
          "window": "ce"
        },
        {
          "compressed_bytes": 1014977,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.05697399994824082,
          "path": "results/T-053/runs/k-ec2-001-26/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007826999644748867,
          "sha256": "866a6e7f15d819eaca48da5afed9fb46c7fd80b6c9b6872b644d1473f93f963f",
          "sha256_seconds": 0.0014001000090502203,
          "uncompressed_bytes": 19463466,
          "window": "ce"
        },
        {
          "compressed_bytes": 11785721,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.41357350000180304,
          "path": "results/T-053/runs/k-ec2-001-26/trung-gian.jsonl.gz",
          "read_seconds": 0.007605699996929616,
          "sha256": "c0fb374852e13a403ed0349a3b9234232b2e48eb5c28bb07dfc1de8fc739f64f",
          "sha256_seconds": 0.01577159995213151,
          "uncompressed_bytes": 182660367,
          "window": "ce"
        },
        {
          "compressed_bytes": 1042539,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03545530000701547,
          "path": "results/T-053/runs/k-laptop-001-28/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005255999858491123,
          "sha256": "f85eba05d5af1e864791a9fbfb8d2ddd14f3277000874b8c3ad3ad65aff8db0c",
          "sha256_seconds": 0.0009250000002793968,
          "uncompressed_bytes": 16110688,
          "window": "ce"
        },
        {
          "compressed_bytes": 11541406,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3723306999891065,
          "path": "results/T-053/runs/k-laptop-001-28/trung-gian.jsonl.gz",
          "read_seconds": 0.006298499996773899,
          "sha256": "afcbead493de06b41b4b10f1c76f6ddefbfe77e75e279d01f9dfc2c8a0780334",
          "sha256_seconds": 0.009562799998093396,
          "uncompressed_bytes": 157105339,
          "window": "ce"
        },
        {
          "compressed_bytes": 1178865,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04762150003807619,
          "path": "results/T-053/runs/k-ec2-001-30/ban-ghi.jsonl.gz",
          "read_seconds": 0.0011314000003039837,
          "sha256": "1fbe92925b4fbdee41bb2f79e56bfa89191d7610a47ab3ce5e7597412b714aee",
          "sha256_seconds": 0.0014124999870546162,
          "uncompressed_bytes": 24507156,
          "window": "ce"
        },
        {
          "compressed_bytes": 12647668,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.4870257000438869,
          "path": "results/T-053/runs/k-ec2-001-30/trung-gian.jsonl.gz",
          "read_seconds": 0.005795600009150803,
          "sha256": "ab446e32a91c9b81972e0b4df052cf0e7ad1a737e553cc4a44d4ce38c939002b",
          "sha256_seconds": 0.01111940003465861,
          "uncompressed_bytes": 214430531,
          "window": "ce"
        },
        {
          "compressed_bytes": 1018853,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03427720000036061,
          "path": "results/T-053/runs/k-laptop-001-32/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005513000069186091,
          "sha256": "ad779224f744eca63e6af5f577a517b6885f83bd9ce9a1b8a133d128b3641dd8",
          "sha256_seconds": 0.0008239999879151583,
          "uncompressed_bytes": 16421004,
          "window": "ce"
        },
        {
          "compressed_bytes": 11306390,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3405907999840565,
          "path": "results/T-053/runs/k-laptop-001-32/trung-gian.jsonl.gz",
          "read_seconds": 0.0051006999565288424,
          "sha256": "371d2fe7d4a36234213b967d6211a4103a382378c2ba84f858787890bc0395d3",
          "sha256_seconds": 0.009205900016240776,
          "uncompressed_bytes": 154181995,
          "window": "ce"
        },
        {
          "compressed_bytes": 987783,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03686940000625327,
          "path": "results/T-053/runs/k-ec2-001-34/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004501999937929213,
          "sha256": "1deb8b14faeab25e4b6dfc2a3bde4d9730835492dbe7507378e07c5db35d1927",
          "sha256_seconds": 0.0011959000257775187,
          "uncompressed_bytes": 16427664,
          "window": "ce"
        },
        {
          "compressed_bytes": 11232270,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.33314469998003915,
          "path": "results/T-053/runs/k-ec2-001-34/trung-gian.jsonl.gz",
          "read_seconds": 0.006718199991155416,
          "sha256": "bcb8aa973d34bcd5c2b801fa560784d7c9e43b0c4cd249562fb5791a60814b0e",
          "sha256_seconds": 0.01028980000410229,
          "uncompressed_bytes": 155921331,
          "window": "ce"
        },
        {
          "compressed_bytes": 1314711,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.04370590002508834,
          "path": "results/T-053/runs/k-laptop-001-36/ban-ghi.jsonl.gz",
          "read_seconds": 0.000839599990285933,
          "sha256": "598c3a9d6adbe11572162eb56b0df3c9b71ec6f5ecbdccbf6d2d14ecc448a5d7",
          "sha256_seconds": 0.0010711999493651092,
          "uncompressed_bytes": 18610066,
          "window": "ce"
        },
        {
          "compressed_bytes": 10925820,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.30789609998464584,
          "path": "results/T-053/runs/k-laptop-001-36/trung-gian.jsonl.gz",
          "read_seconds": 0.006763999990653247,
          "sha256": "854ea2603f3f2d3fd0b51b039daeda31bb485c7d06affb6774de4d6482c85a8e",
          "sha256_seconds": 0.009528399968985468,
          "uncompressed_bytes": 118188339,
          "window": "ce"
        },
        {
          "compressed_bytes": 968714,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.06164099997840822,
          "path": "results/T-053/runs/k-ec2-001-38/ban-ghi.jsonl.gz",
          "read_seconds": 0.0006233000312931836,
          "sha256": "8bd4dd2c03658b39309474aa68135b5f48d3e13849d012b76bb6ba3b4eacb4eb",
          "sha256_seconds": 0.0011957999668084085,
          "uncompressed_bytes": 15740140,
          "window": "ce"
        },
        {
          "compressed_bytes": 11166023,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.35235739999916404,
          "path": "results/T-053/runs/k-ec2-001-38/trung-gian.jsonl.gz",
          "read_seconds": 0.007568799948785454,
          "sha256": "b9e9a75d02c5918622abb4652a98748a8264c6ffc328a0049bd26f08b5230d9a",
          "sha256_seconds": 0.014162100036628544,
          "uncompressed_bytes": 153532697,
          "window": "ce"
        },
        {
          "compressed_bytes": 1233079,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03973089996725321,
          "path": "results/T-053/runs/k-laptop-001-40/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008208000217564404,
          "sha256": "622e790f6ca76d3a6034cd87133655d1adee14252f676041abd368154c5284c3",
          "sha256_seconds": 0.0010337000130675733,
          "uncompressed_bytes": 17431184,
          "window": "ce"
        },
        {
          "compressed_bytes": 10735191,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.35347719996934757,
          "path": "results/T-053/runs/k-laptop-001-40/trung-gian.jsonl.gz",
          "read_seconds": 0.005463199981022626,
          "sha256": "a35666f870bb42c4373f65d07bd990722a9ce37afaa89a85648d075e395255cf",
          "sha256_seconds": 0.009026399988215417,
          "uncompressed_bytes": 120368383,
          "window": "ce"
        },
        {
          "compressed_bytes": 1183524,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.035812699992675334,
          "path": "results/T-053/runs/k-ec2-001-42/ban-ghi.jsonl.gz",
          "read_seconds": 0.0007631999906152487,
          "sha256": "22297a9a6b4139043ced3a2edfc318d92fa176bc32307ed7c9238aae5839d418",
          "sha256_seconds": 0.0009610999841243029,
          "uncompressed_bytes": 15832522,
          "window": "ce"
        },
        {
          "compressed_bytes": 10598076,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2956939000287093,
          "path": "results/T-053/runs/k-ec2-001-42/trung-gian.jsonl.gz",
          "read_seconds": 0.0058397999964654446,
          "sha256": "f94fa0f3a23e9a4fb3ec78551db8b1a37fcb49ebb4eb5f8afa3159d7250820e6",
          "sha256_seconds": 0.010167400003410876,
          "uncompressed_bytes": 114154819,
          "window": "ce"
        },
        {
          "compressed_bytes": 994092,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.03502959996694699,
          "path": "results/T-053/runs/k-laptop-001-44/ban-ghi.jsonl.gz",
          "read_seconds": 0.00045440002577379346,
          "sha256": "d7188f604ff83e2050e287e44ac480a9417ed94439af2051821bceb3aaee19c9",
          "sha256_seconds": 0.0008387999841943383,
          "uncompressed_bytes": 15035692,
          "window": "ce"
        },
        {
          "compressed_bytes": 11132791,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.3369990999926813,
          "path": "results/T-053/runs/k-laptop-001-44/trung-gian.jsonl.gz",
          "read_seconds": 0.004975700052455068,
          "sha256": "2e99c2f3b4c8bec35cc6869e7d7871a57d81dbec5508d321c90dd19fd9e3e264",
          "sha256_seconds": 0.009465099952649325,
          "uncompressed_bytes": 146282751,
          "window": "ce"
        },
        {
          "compressed_bytes": 1319500,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.0472412999952212,
          "path": "results/T-053/runs/k-ec2-001-46/ban-ghi.jsonl.gz",
          "read_seconds": 0.0008545000455342233,
          "sha256": "e6a4f2fc41632fc8b7192e7310296c3e8588e8295e60da6bc04c57bfd0d95f91",
          "sha256_seconds": 0.00106819998472929,
          "uncompressed_bytes": 18474632,
          "window": "ce"
        },
        {
          "compressed_bytes": 10884348,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2682558000087738,
          "path": "results/T-053/runs/k-ec2-001-46/trung-gian.jsonl.gz",
          "read_seconds": 0.005185799964237958,
          "sha256": "6674d1f342405860d478e4ed5e665da7bc02ca3b01e545725a1bb920f7630fa0",
          "sha256_seconds": 0.009932400018442422,
          "uncompressed_bytes": 116152319,
          "window": "ce"
        },
        {
          "compressed_bytes": 624009,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.01639860001159832,
          "path": "results/T-053/runs/k-ec2-001-48/ban-ghi.jsonl.gz",
          "read_seconds": 0.0004327999777160585,
          "sha256": "b40c636be39819c706644a76167a0b34dfb22c427cdacbf921c01067ac460558",
          "sha256_seconds": 0.0005136000108905137,
          "uncompressed_bytes": 5782950,
          "window": "ce"
        },
        {
          "compressed_bytes": 7928531,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.20172569999704137,
          "path": "results/T-053/runs/k-ec2-001-48/trung-gian.jsonl.gz",
          "read_seconds": 0.003667499986477196,
          "sha256": "17c0c208f3011b5635ce465e908fe26cbe61d98c6b9ff63fd478dafb2d610865",
          "sha256_seconds": 0.006432699970901012,
          "uncompressed_bytes": 84524647,
          "window": "ce"
        },
        {
          "compressed_bytes": 604213,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.016064800031017512,
          "path": "results/T-053/runs/k-laptop-001-50/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003785000299103558,
          "sha256": "dd0aeb82320ca6ba1bf0566c5adae89214ae5ae1e00c2febf2bd013b80157585",
          "sha256_seconds": 0.0004971999442204833,
          "uncompressed_bytes": 5568606,
          "window": "ce"
        },
        {
          "compressed_bytes": 7708244,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2166457999846898,
          "path": "results/T-053/runs/k-laptop-001-50/trung-gian.jsonl.gz",
          "read_seconds": 0.0035531999892555177,
          "sha256": "bfba05744dc84f3cc9b18bdede4e0854775e148464e37f1a7283310129ab5a6e",
          "sha256_seconds": 0.006332100019790232,
          "uncompressed_bytes": 83261807,
          "window": "ce"
        },
        {
          "compressed_bytes": 609161,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.020360699971206486,
          "path": "results/T-053/runs/k-ec2-001-52/ban-ghi.jsonl.gz",
          "read_seconds": 0.0005601999582722783,
          "sha256": "1743bf2b9d257f7c398ea43cd2cddd01edf8bb25c7fc51d2d30100beae63a14f",
          "sha256_seconds": 0.0008057000231929123,
          "uncompressed_bytes": 5541390,
          "window": "ce"
        },
        {
          "compressed_bytes": 7610791,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.200561799982097,
          "path": "results/T-053/runs/k-ec2-001-52/trung-gian.jsonl.gz",
          "read_seconds": 0.003646700002718717,
          "sha256": "4bc2e267f65508d76c21a3cacb459208c16e67f3ed5ad747fe638709b0ae7e56",
          "sha256_seconds": 0.006064699962735176,
          "uncompressed_bytes": 80351715,
          "window": "ce"
        },
        {
          "compressed_bytes": 527507,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015272599994204938,
          "path": "results/T-053/runs/k-ec2-001-54/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003816999960690737,
          "sha256": "d638b5b01506de9bc9d53b110fbaa7939c0084a23f82aac6cf5e512765294c22",
          "sha256_seconds": 0.00045419996604323387,
          "uncompressed_bytes": 4910364,
          "window": "ce"
        },
        {
          "compressed_bytes": 7343955,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.2021489999606274,
          "path": "results/T-053/runs/k-ec2-001-54/trung-gian.jsonl.gz",
          "read_seconds": 0.0034349000197835267,
          "sha256": "d641bdf44f146132fae930b0ddb46ba9a5ac93095a31660ce61acd78ee3b2b7a",
          "sha256_seconds": 0.0061916999984532595,
          "uncompressed_bytes": 79274723,
          "window": "ce"
        },
        {
          "compressed_bytes": 560315,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015114500012714416,
          "path": "results/T-053/runs/k-laptop-001-56/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003779000253416598,
          "sha256": "143f30aa2738c4d352e399146bc600264ca2386fe7a8545f51b95e79943dddc3",
          "sha256_seconds": 0.00047909998102113605,
          "uncompressed_bytes": 5087594,
          "window": "ce"
        },
        {
          "compressed_bytes": 7484392,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.1883043999550864,
          "path": "results/T-053/runs/k-laptop-001-56/trung-gian.jsonl.gz",
          "read_seconds": 0.003803500032518059,
          "sha256": "0172cb54c856a2b07aaf13a9e10ec6f5bb0268e3db7c81cac01c2d061791fdeb",
          "sha256_seconds": 0.006449699983932078,
          "uncompressed_bytes": 79047943,
          "window": "ce"
        },
        {
          "compressed_bytes": 585130,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.015223700029309839,
          "path": "results/T-053/runs/k-ec2-001-58/ban-ghi.jsonl.gz",
          "read_seconds": 0.0003799000405706465,
          "sha256": "fe8563d7eb96ea389c229a035e4076b2d15bbee774e4fd3e12fe5fe997975099",
          "sha256_seconds": 0.0004811999970115721,
          "uncompressed_bytes": 5370198,
          "window": "ce"
        },
        {
          "compressed_bytes": 7515507,
          "dataset": "RE2-TT",
          "gzip_inflate_seconds": 0.21530430001439527,
          "path": "results/T-053/runs/k-ec2-001-58/trung-gian.jsonl.gz",
          "read_seconds": 0.00340919999871403,
          "sha256": "98765466a1be54725f80ca5d31500437b23e32daee0e005e48f3ad0926da75fb",
          "sha256_seconds": 0.005954899999778718,
          "uncompressed_bytes": 79943115,
          "window": "ce"
        }
      ],
      "peak_process_rss_bytes_since_start": 151732224,
      "stage": "KB_inputs",
      "totals": {
        "compressed_bytes": 821183851.0,
        "gzip_inflate_seconds": 26.16448459966341,
        "read_seconds": 0.4168915996560827,
        "sha256_seconds": 0.7274103001109324,
        "uncompressed_bytes": 11553367561.0
      }
    }
  ],
  "scope": "Isolate physical file read, buffer SHA256 and gzip inflation of pinned compressed sources",
  "start_utc": "2026-11-04T03:11:58.745719+00:00"
}
```

### Mã tách thời gian để tái lập

```python
import gzip, hashlib, io, json, sys, time
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import psutil
import run_t11 as t11
OUT=t11.OUT
entries,_=t11.source()
kb=json.loads((OUT/"kb-002/sources.json").read_bytes())
groups={
 "T11_inputs":[dict(e[k],index=e["index"],dataset=e["job"]["dataset"],window=e["job"]["window"])
               for e in entries for k in ("native","trace")],
 "T12_inputs":[dict(e[k],index=e["index"],dataset=e["job"]["dataset"],window=e["job"]["window"])
               for e in entries for k in ("native","trace")],
 "KB_inputs":[{"path":e["path"][kind],"sha256":e["path"][hashkey],
               "dataset":e["job"]["dataset"],"window":e["job"]["window"]}
              for e in kb for kind,hashkey in (("path","sha256"),("trace","trace_sha256"))],
}
receipt={"start_utc":datetime.now(timezone.utc).isoformat(),"scope":"Isolate physical file read, buffer SHA256 and gzip inflation of pinned compressed sources","rows":[]}
process=psutil.Process()
for stage,items in groups.items():
 start=time.perf_counter()
 totals=defaultdict(float)
 rows=[]
 for item in items:
  path=t11.ROOT/item["path"]
  begin=time.perf_counter()
  data=path.read_bytes()
  reading=time.perf_counter()-begin
  begin=time.perf_counter()
  sha=hashlib.sha256(data).hexdigest()
  hashing=time.perf_counter()-begin
  assert sha==item["sha256"],path
  count=0
  begin=time.perf_counter()
  with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
   while block:=stream.read(1024*1024):
    count+=len(block)
  inflation=time.perf_counter()-begin
  row=dict(item,read_seconds=reading,sha256_seconds=hashing,gzip_inflate_seconds=inflation,
           compressed_bytes=len(data),uncompressed_bytes=count)
  rows.append(row)
  for name in ("read_seconds","sha256_seconds","gzip_inflate_seconds","compressed_bytes","uncompressed_bytes"):
   totals[name]+=row[name]
  del data,block
 receipt["rows"].append({"stage":stage,"file_reads":len(items),"totals":dict(totals),
                         "elapsed_seconds":time.perf_counter()-start,"files":rows,
                         "peak_process_rss_bytes_since_start":process.memory_info().peak_wset})
 print(stage,round(time.perf_counter()-start,3),"PASS",flush=True)
receipt["finish_utc"]=datetime.now(timezone.utc).isoformat()
receipt["PASS"]=True
fence=chr(96)*3
with (OUT/"dinh-chinh-luot-1.md").open("a",encoding="utf-8",newline="\n") as stream:
 stream.write("\n## Tách riêng đọc, SHA-256 và giải nén byte\n\n")
 stream.write("Lượt profiler phía trên đo đúng tổng lượt và hậu xử lý. Riêng hash_read_seconds chỉ bao các helper đã gắn đồng hồ ở mức module. Hàm sha mà records đã import trực tiếp chưa được bọc, nên cột đó chưa gồm hash bên trong records. load_excluding_hash_seconds thực tế vẫn gồm hash đó. Dùng phép đo trực tiếp dưới đây cho các cột đọc, SHA-256 và giải nén riêng. Giữ biên nhận profiler để truy vết, không cộng chéo hai lượt.\n\n")
 stream.write(fence+"json\n"+json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n"+fence+"\n\n")
 stream.write("### Mã tách thời gian để tái lập\n\n"+fence+"python\n"+sys.orig_argv[-1]+"\n"+fence+"\n")
```
