# T-048 — Độ nhạy tham số và thang điểm trong G3/D1

Codex đã hoàn tất phần triển khai, chạy, kiểm và phân tích trong SPEC. Claude đã phản biện và kiểm lại bản sửa qua hai lượt. Giữ ε=0,05, α=0,01 theo B1. Luật C cho GIÚP với z+S1 ở cả R0 và E1+E2 trên dev; D24 hiện hành chưa đổi. Quyền chạy lại K, dùng nền T-049 và mở G3/test được quyết riêng.

## 1. Nguồn, phạm vi và tái lập

Chỉ dùng 30 ca dev RE2-TT, 22 ca dev Nezha-OB và 30 cửa sổ giả RE2-TT theo hai allowlist, đủ 23 ô. Code phương pháp và hợp đồng ghim ở [manifest](manifest.json). Nhãn được ghép sau khi đóng hash pha 1. Native (bản ghi gốc) của các lượt lỗi và phần điều phối tái chia được giữ. Không sửa src hoặc SPEC.

243 file dev laptop khớp nguồn. EC2 dùng tại chỗ 154 file Nezha đã khớp hash và nhận đúng 89 file RE2, 656.358.942 byte; giữ bản gốc laptop. Không chuyển file Nezha trộn dev/ngoài dev. Không dọn tài nguyên, thu hồi 0 byte.

R0 đủ 52 thật + 30 giả đã đối chiếu T1/K-R0 của T-047: không đổi cờ, hợp lệ, tầng, gán cạnh, thứ tự, hòa hoặc kết quả chấm. 77 cửa sổ EC2 lệch số thực tại p và m; đã tái lập cùng đối số để định vị backend số học, không qua alpha. Bản E1+E2 E4+S1 mới cũng được đối chiếu đủ 82 với T-047: 24 cửa sổ lệch p/m, không lệch trường quyết định hoặc phần chưa giải thích. [R0](runs/kiem-r0-ec2-001/kiem.json) `/checks`, [số học](runs/kiem-so-hoc-hai-may-001/kiem.json), [E1+E2](runs/kiem-e1e2-t047-001/kiem.json).

## 2. Chạy song song và thời gian thực

Pilot (lượt thử) cùng 36 cấu hình–cửa sổ trên mỗi máy: laptop 1.626,406 giây, EC2 916,236 giây. EC2 nhanh hơn khoảng 1,78 lần ở lát cắt này. Sau đo RAM và thời gian, EC2 giữ 12 RE2 nặng nhất với 2 worker (tiến trình tính), laptop nhận 18 RE2 và 22 Nezha. T4b dùng 3 worker chung trên laptop. Mọi vế của cùng ca/cửa sổ được chạy cùng máy. [Pilot](pilot.json) `/comparison`, `/completion`.

| Pha | EC2 | Laptop |
|---|---:|---:|
| R0 đủ 82 trên EC2 | 34.59 phút | Tái lập đúng 58 cửa sổ được phân cho laptop |
| T4 ngoài mặc định | 64.98 phút, 24 cửa sổ × 8 | Nezha 10.28 phút; RE2 giữ 13 cửa sổ, phần còn lại 26.48 phút |
| T4b mới | 37.26 phút, 24 × 5 | 28.86 phút, 58 × 5 |

Các dòng máy chạy đồng thời; không cộng chúng thành thời gian chờ. T4b hoàn tất trong khoảng 37 phút của controller EC2, thay cho dự báo một worker ban đầu. Trần dự phòng toàn gói 16 giờ không phải thời gian tối thiểu. Tổng ma trận phân tích có 1.148 tổ hợp duy nhất, gồm 738 ở T4 và thêm 410 ở T4b; R0 được dùng lại. Các lần tái lập/pilot/kiểm được ghi riêng.

Giá Linux On-Demand công khai đã ghim là 0,1197 USD/giờ. Riêng thời gian controller EC2 pilot + R0 + T4 + T4b khoảng 9.126 giây, tương đương khoảng 0,30 USD tiền máy; chuẩn bị/chờ, lưu trữ và IP tính riêng. Máy vẫn giữ nguyên để đọc trung gian khi phản biện. [Nguồn giá và dấu vết lượt](manifest.json).

Cache (tái dùng) p chỉ bỏ alpha khỏi phần tham số của khóa G3, giữ mẫu/mốc/biên/hướng/seed và mọi tham số ảnh hưởng p; D1 được tính lại. Bật/tắt cùng phiên bản trùng hash native và trung gian. Trên C-e đủ 9 điểm, thời gian cả đợt 260,296 → 104,203 giây. Đối chiếu lại 15 bản ghi với T4 chính: native exact, mọi giá trị trung gian chung exact; bản mới chỉ thêm source_bytes, oracle và cực trị A. [Kiểm đầu](runs/cache-ce-check-001/kiem.json), [kiểm lượt chính](runs/kiem-cache-main-002/kiem.json). Cache m đã thử nhưng không áp vào lượt chính vì lợi ích phụ thuộc workload.

RSS là cực đại quan sát theo chu kỳ 2 giây, cộng cả cây tiến trình; không phải phép đo đỉnh liên tục. T4b laptop quan sát 3,90 GB. Cold/warm của bộ đệm đĩa OS chưa được đo có đối chứng; progress có thời gian load, từng cấu hình, CPU và các hàm chấm/xếp/m, chưa tách độc lập toàn bộ phần trích đặc trưng/khởi tạo/ghi. Các giới hạn đo thời gian không được dùng làm căn cứ về chất lượng RCA.

## 3. T4 — giữ tham số mặc định

P/S_lo/S_hi cùng hướng điều kiện B1. Bảng là P; toàn bộ độ đo, ca và cửa sổ giả ở [t4.json](t4.json) `/summary`, `/scored`, `/ce`. Hòa được chấm theo kỳ vọng, đủ mẫu số 52 và 30.

| ε | α | MRR gộp | RE2-TT | Nezha-OB | M5 gộp | N1 giả trung bình |
|---|---|---:|---:|---:|---:|---:|
| 0 | 0.001 | 0.482263 | 0.459403 | 0.513436 | 23 | 16.6667 |
| 0 | 0.01 | 0.394857 | 0.254001 | 0.586932 | 23 | 45.1667 |
| 0 | 0.05 | 0.400618 | 0.254001 | 0.600550 | 23 | 54.7000 |
| 0.05 | 0.001 | 0.629903 | 0.709916 | 0.520795 | 19 | 9.0333 |
| 0.05 | 0.01 | 0.681309 | 0.765000 | 0.567186 | 17 | 16.9000 |
| 0.05 | 0.05 | 0.669311 | 0.765000 | 0.538827 | 18 | 30.4000 |
| 0.2 | 0.001 | 0.635830 | 0.725346 | 0.513763 | 21 | 5.3333 |
| 0.2 | 0.01 | 0.680087 | 0.738333 | 0.600660 | 20 | 10.0000 |
| 0.2 | 0.05 | 0.674538 | 0.738333 | 0.587544 | 20 | 19.2667 |

Cả tám điểm khác đều không tăng MRR gộp so mặc định, không có ứng viên qua B1. Điểm ε=0,2, α=0,01 gần mặc định về MRR gộp nhưng RE2 giảm, Nezha tăng và M5 gộp tăng 17 → 20. Giữ mặc định là nhánh đã duyệt của SPEC, không khẳng định tối ưu ngoài dev. [Điều kiện](t4.json) `/candidates`; [bootstrap theo ô và bỏ từng ô](runs/phan-tich-t4-001/kiem.json) `/fragility`.

Đã lần theo 656 lượt ngoài mặc định. Input chuẩn hóa, hash mẫu N/A, mốc và biên thời gian G3 giữ nguyên; lưu thay đổi p, biên trị số, cờ, tầng, khóa root/đối thủ theo từng ca. [Tổng hợp](runs/tong-hop-duong-t4-001/kiem.json) `/results`; bản chi tiết tại `runs/duong-t4-{laptop,ec2}-001/trung-gian.jsonl`.

Ví dụ `dev-7d3c2fe6d1` Nezha: giảm ε từ 0,05 xuống 0 ở α=0,01 làm RR 1 → 1/2. Hai kênh memory của đối thủ có p giữ khoảng 0,003968 nhưng tỷ phần A vượt biên dưới đổi 0 → 1. Đối thủ từ tầng 3 lên tầng 1, max điểm 1 thắng max 0,8 của root; m đứng sau max điểm. Con trỏ `duong-t4-laptop-001/trung-gian.jsonl:66#/worlds/P`. Ca `dev-03d4910932` tăng α lên 0,05 đổi cờ 38 đơn vị và tầng 11 thực thể nhưng RR vẫn 1/2: phần đầu khóa root và quan hệ với đối thủ giữ nguyên. Con trỏ dòng 253 cùng file. Không quy mọi cờ đổi thành nguyên nhân đổi hạng.

Ở RE2, ca `dev-f81f88234e` minh họa chênh lớn khi ε giảm từ 0,05 về 0 ở α=0,01. Với metric bộ nhớ của ts-admin-basic-info-service, tỷ phần A vượt biên trên tăng từ 0 lên 1 và p giảm từ 1 xuống khoảng 0,003968. Kênh nhận cờ, đối thủ lên tầng 1 và max điểm 0,96 vượt max 0,953333 của root. Cả ca có 20 đối thủ vượt root, RR từ 1 xuống 1/21. Đây là một đường tính trong ca, không quy toàn bộ chênh RE2 cho kênh bộ nhớ. Nguồn: `runs/duong-t4-laptop-001/trung-gian.jsonl:282#/worlds/P`, `t4.json#/scored`.

## 4. Công thức, hữu hạn và điều kiện phép đổi điểm

E4 của kênh hợp lệ thuộc [0,1]: tỷ phần vượt biên ở [0,1], phần tăng dương cũng ở [0,1], rồi áp cổng; nhánh đếm được kiểm theo D1 và NEW_OP/STOPPED. Miền này không áp cho số kênh hoặc tổng điểm trong khóa. r_A=1 không đồng nghĩa e=1 vì còn trừ r_N.

Đủ 492 bản ghi ghép của T4b, 164 tổ hợp nền–cửa sổ. Có 70.752 lượt đơn vị PV, trong đó 65.556 đủ điều kiện tính z; các đơn vị thiếu hỗ trợ giữ trong bản ghi, không bỏ ca khỏi mẫu số. Oracle độc lập kiểm tỷ phần, công thức E4/z và nhánh đếm. Đã kiểm riêng med_N, IQR, c, hai hướng z và tổng khóa, trước khi đọc N1/V0. Trên dev không có ngoại lệ số học, đổi cờ, độ hợp lệ, ứng viên, tầng, điểm kênh đếm hoặc gán E2 khi thay thang. z+S1/z+S0 có cùng kênh và điểm, chỉ khác khóa m. m của E4+S1/z+S1 giữ nguyên. [Công thức](co-che.json) `/formula`; [đối chiếu mẫu và E4 trước thay điểm](runs/shared-pv-t4b-laptop-001/kiem.json), [EC2](runs/shared-pv-t4b-ec2-001/kiem.json).

15.982 lượt đơn vị trong tham chiếu R0 cũ thiếu trường oracle. Phân tích dùng oracle của bản z mới sau khi chứng minh exact toàn bộ hash mẫu và kết quả E4 trước thay điểm; không sửa bản gốc. Phân bố z tách IQR=0, IQR dương dưới sàn và IQR trên sàn theo dataset/nền/cửa sổ; tách z thô hai hướng với z thực dùng trong kênh xếp hạng. Max z thực dùng khoảng 640.830,484 trên diskio, cực trị A lặp ba lần. z>1 riêng lẻ chưa chứng minh lấn át. [Phân bố](co-che.json) `/formula/distribution`, `/formula/largest_used_z`.

Fixture cực trị xác nhận các giới hạn thật: một hướng z không hữu hạn có thể xóa cờ hướng hữu hạn; mất hợp lệ có thể đổi verdict dù N1 vẫn 0. Trung vị/phép chia có thể tràn; IQR vô hạn còn có thể cho z=0 và huu_han=True. Hai kênh z hữu hạn 1e308 có thể làm tổng khóa tràn và native trả ERROR. Giữ nguyên mọi bản lỗi; không thay NaN/Inf, không sửa src hoặc chọn điểm dự phòng. Các phản ví dụ này chặn tuyên bố đúng trên mọi mẫu hữu hạn; chưa xảy ra trong dev đã chạy. [Fixture toàn chuỗi](runs/kiem-cuc-tri-z-001/kiem.json).

## 5. T4b và luật C

Phép so chính giữ S1 ở từng nền. z+S0 chỉ báo kèm. Số ở [t4b.json](t4b.json) `/summary`; RR/Hit/M5/hạng/độ đo theo ca và thế giới ở `/scored`, C-e ở `/ce`.

| Nền/biến thể | MRR gộp | RE2-TT | Nezha-OB | M5 gộp |
|---|---:|---:|---:|---:|
| R0-E4-S1-e0.05-a0.01 | 0.681309 | 0.765000 | 0.567186 | 17 |
| R0-z-S1 | 0.847335 | 0.983333 | 0.661883 | 7 |
| R0-z-S0 | 0.852143 | 0.983333 | 0.673247 | 6 |
| E1+E2-E4-S1 | 0.799359 | 0.822222 | 0.768182 | 8 |
| E1+E2-z-S1 | 0.885897 | 0.944444 | 0.806061 | 3 |
| E1+E2-z-S0 | 0.890705 | 0.944444 | 0.817424 | 2 |

| Phép so chính | ΔMRR | Ô tăng/giảm | Kết cục ba thế giới | Bootstrap gộp 2,5–97,5% |
|---|---:|---:|---|---|
| E1+E2: E4+S1 → z+S1 | +0.086538 | 8/5 | GIÚP/GIÚP/GIÚP | [0.007711; 0.190258] |
| R0: E4+S1 → z+S1 | +0.166026 | 11/1 | GIÚP/GIÚP/GIÚP | [0.075472; 0.285398] |

Helper gọi đúng buoc=luat_C, đủ E_X=23, δ=0,01 và δ_d=1/30, 1/22. UV-6/M5 của E3/E5 không áp; không đưa C-e không phân xử vào HẠI riêng. Hồi quy có ba thế giới trái nhau để phân biệt luat_C với khoi_K. Kết cục vẫn GIÚP khi δ=0,005/0,02. Kiểm dấu theo ô: R0 13/2048, E1+E2 595/1024; báo kèm, không dùng thay luật. Bootstrap lấy lại ô trong dataset, 1.000 mẫu, seed khai trước. Nezha của E1+E2 có khoảng bootstrap qua 0. Bỏ một ô giữ ΔMRR gộp dương: R0 khoảng 0,12415–0,18267; E1+E2 khoảng 0,05612–0,10204. [Luật và độ bền](luat-c.json) `/comparisons`.

Cả hai nền có đủ 23 ô có cờ nội sinh. R0 có 19 ô đổi thứ tự/hòa bất kỳ, 13 ô đổi quan hệ root/đối thủ; E1+E2 tương ứng 20 và 14. Tập ô luật C vẫn giữ 23, không lấy riêng các ô thay đổi. [Kiểm tập ô](runs/kiem-o-luat-c-001/kiem.json).

C-e đủ 30 cặp hợp lệ mỗi nền, cùng N1/V0 ở cả ba biến thể và ba thế giới. Cả 30 đều CAUSE_FOUND. N1 trung bình R0 là 16,9; E1+E2 là 499/30. Khi đã chứng minh cùng cờ/hợp lệ/tầng, vế này **không phân xử được do cấu tạo phép thử**. Nó không xác nhận báo động giả đã đạt chuẩn. [t4b.json](t4b.json) `/summary/R0-E4-S1-e0.05-a0.01/P/C-e`, `/summary/E1+E2-E4-S1/P/C-e`; [B2](luat-c.json) `/gate_checks`.

So mô tả **E1+E2 trừ R0 khi giữ cùng thang**, tính lại từ RR từng ca. Cả ba thế giới cho cùng bảng.

| Thang | ΔMRR RE2-TT | ΔMRR Nezha-OB | ΔMRR gộp | Ô tăng / giảm |
|---|---:|---:|---:|---:|
| E4+S1 | +0,0572 | +0,2010 | +0,1180 | 8 / 0 |
| z+S1 | −0,0389 | +0,1442 | +0,0386 | 5 / 6 |

Nguồn: `t4b.json#/scored` và `/E_X`. Kiểm bằng helper trên 23 ô với `moc_gia=None` cho GIÚP dưới E4 và TRÁI_CHIỀU_DATASET dưới z ở cả ba thế giới. Dưới z, hai dataset vượt ngưỡng δ_d theo hai hướng. [Kết quả helper](runs/kiem-lai-phan-bien-002/kiem.json) `/comparisons`. Đây là chẩn đoán trên hai cấu hình cố định. Việc chọn nền vẫn cần lượt K theo giao thức riêng. Chênh lệch này gộp E1-U và E2-C, nên chưa đo tác dụng riêng của quan hệ đồ thị.

## 6. Điều gì làm đổi hạng

Phát lại khóa giữ cờ/U/gán E2 đã khớp native hai chiều trên đủ 104 cặp ca–nền, ba thế giới. R0: 16 ca tăng RR, 2 giảm, 34 giữ. E1+E2: 12 tăng, 6 giảm, 34 giữ. Các số dưới là cặp root–đối thủ tại P, không là ca độc lập hay tỷ lệ nguyên nhân; nhóm có thể chồng lấn. Hai thế giới phụ có cùng số đếm trong lần này. [Bằng chứng đầy đủ](co-che.json) `/groups`, `/cases`.

| Chẩn đoán cặp đảo hạng | R0 | E1+E2 |
|---|---:|---:|
| Cặp đổi quan hệ, gồm chuyển hòa | 47 | 34 |
| Chỉ đổi nhóm r_A=1 tái lập được chuyển quan hệ | 4 | 10 |
| Chỉ đổi nhóm r_A<1 tái lập được chuyển quan hệ | 46 | 33 |
| Cả hai nhóm riêng lẻ đều tái lập được | 3 | 9 |
| Max E4 hòa, có max PV r_A=1, và đổi nhóm bão hòa tái lập được | 0 | 1 |
| Max PV z thắng đối thủ max thuần đếm, trả nhóm PV về E4 phục hồi quan hệ | 4 | 4 |
| Vừa thuộc nhánh đổi nhóm r_A=1 vừa thuộc nhánh PV/đếm | 1 | 1 |

Bão hòa không giải thích chung cho lợi ích z: phần lớn cặp được tái lập bằng nhóm chưa bão hòa. Cặp max E4 hòa duy nhất có bằng chứng nhóm bão hòa ở E1+E2 vốn đã được m phân biệt; z làm hỏng quan hệ ấy. Đây là bằng chứng về đường tính trong ca, không xác nhận nguyên nhân duy nhất của mọi lỗi E4.

Ví dụ PV–PV chưa bão hòa: `dev-fbc45b0c67`, R0, root ts-train-service có RR 1/8 → 1. So với ts-basic-service, max E4 là 0,961313 < 0,968944; sau thay điểm, z là 18.498,856 > 1.063,611. Tầng/cờ giữ nguyên và max là thành phần đầu tiên đảo khóa; nhóm chưa bão hòa tái lập được chuyển quan hệ.

Ví dụ PV thắng kênh đếm và gây hại: `dev-5ada15752d`, root frontend đúng hạng 1 dưới E4, max đếm=1. shippingservice có max PV E4=0,8; z=3,983333 làm nó vượt frontend dù m nhỏ hơn. Trả nhóm PV về E4 phục hồi quan hệ cũ, RR toàn ca 1 → 1/2 ở cả hai nền. Không có hòa max E4 ở đây, nên không gọi là E4 hòa vì bão hòa.

Có hướng giúp tương ứng: `dev-27252dca60`, root PV 0,041301 dưới E4 thua frontend max đếm=1; z=142,888889 thắng và trả điểm lại phục hồi quan hệ cũ. Nhưng không được lấy một cặp thắng để giải thích ΔRR toàn ca: ở `dev-b0f8b2e3ac`, root thắng frontend nhờ z ở cả hai nền, trong khi RR toàn ca R0 1/2 → 1 và E1+E2 1/2 → 1/5 do còn các đối thủ PV khác.

Control (ca đối chiếu) được đọc từ toàn bộ tập, không chỉ ca đổi hạng. P có 11 cặp R0 và 6 cặp E1+E2 giữ quan hệ trong điều kiện max E4 hòa với max PV r_A=1; trong đó 4 và 3 cặp đúng top-1 ở cả hai vế. Không có control giữ quan hệ thỏa điều kiện max PV–đếm trong tập này; việc khái quát điều kiện không đảo hạng của nhóm đó còn thiếu đối chiếu ngoài các ca quan sát. Đã có cả hướng giúp và hại để kiểm đường tính trên các cặp thật. [Controls](co-che.json) `/controls`, `/control_groups`.

Khóa m đã giúp RR của 4 ca và hại 1 ca ở R0 dưới E4; ở E1+E2 giúp 1, hại 1. Dưới z, S1 chỉ làm RR đổi ở `dev-8ecd9880ed`: checkoutservice và frontend đều max đếm=1, số kênh=1, tổng=1; m frontend 3,940672 > 3,266774 của root. S1 làm root đứng thứ 2 (RR=1/2), S0 giữ hòa hạng 1–2 (RR=3/4). Hiện tượng giống ở E4 và z; MRR z+S1 thấp hơn z+S0 đúng 1/208 ở mỗi nền. S0 vẫn chỉ báo kèm theo SPEC.

Phát lại cùng lúc bỏ một cực trị A mỗi đơn vị, giữ cờ/gán/m, làm RR đổi ở 2 ca R0 và 4 ca E1+E2. Đây là độ nhạy của điểm cực trị trong ca, không là một cấu hình phương pháp mới hoặc phép đánh giá lại cổng. [Ví dụ có input–cổng–cờ–điểm–khóa](runs/ca-minh-hoa-001/kiem.json) `/examples`; [độ nhạy](co-che.json) `/groups/R0/P/case_membership/remove_one_extreme_changes_RR`, `/groups/E1+E2/P/case_membership/remove_one_extreme_changes_RR`.

**Nhóm kênh tạo max của bên đứng trước sau đổi thang.** Đếm cặp root–đối thủ đổi quan hệ ở P, theo hướng có lợi hay bất lợi cho root. Kênh tạo max là dấu vết để chọn ca soi khóa. Một cặp có lợi cho root vẫn có thể nằm trong ca RR giảm.

| Nền | Dataset | Có lợi cho root | Bất lợi cho root |
|---|---|---|---|
| R0 | RE2-TT | latency-90: 27, latency-50: 1, thao tác: 5 | thao tác: 1 |
| R0 | Nezha-OB | thao tác: 9, metric khác: 2 | thao tác: 1, metric khác: 1 |
| E1+E2 | RE2-TT | latency-90: 5, latency-50: 1, thao tác: 9 | cạnh: 3, thao tác: 1 |
| E1+E2 | Nezha-OB | thao tác: 5, cạnh: 1, metric khác: 2 | thao tác: 1, cạnh: 1, metric khác: 5 |

Nguồn: `co-che.json#/cases`, dùng `mechanism/worlds/P/flips`, `after_relation`, `pair_favors_root` và `max_channels` của bên thắng. RE2 trên R0 có 34 cặp đổi quan hệ, trong đó 33 có lợi cho root. Latency-90 đứng đầu ở 27/33 cặp có lợi. Ghép hash trung gian B2 laptop và EC2 theo mã ca, nền và đơn vị cho toàn bộ 81 cặp đổi quan hệ ở P. Cả 81 cặp có bên đứng trước sau khi đổi điểm. Trong 6 cặp, bên đứng sau có kênh PV tạo max dùng nhánh dự phòng `c=1` do IQR dưới sàn. Số cặp có kênh PV tạo max của bên thắng dùng nhánh này là 0/81. Ảnh hưởng của các kênh khác và độ nhạy khi đổi đơn vị đo còn mở. [Kiểm nhánh dự phòng](runs/kiem-lai-phan-bien-002/kiem.json) `/PV_fallback`.

Ba chuyển quan hệ bất lợi do max kênh cạnh ở RE2/E1+E2 nằm trong hai ca. Ở `dev-f36d0647d5`, E2-C gán tín hiệu cạnh từ ts-order-service cho ts-station-service. Đối thủ từ max E4 0,2756 lên z 1.501,04 và vượt max z 1.442,52 của root trong cùng tầng. Ở `dev-a915aa2424`, hai cạnh từ ts-travel-service gán cho ts-order-service và ts-train-service, cho max z 4.708,99 và 4.834,19 vượt 3.881,56 của root. Root đồng thời vượt ts-ui-dashboard, nên cần đọc RR toàn ca cùng các cặp. Cả ba chuyển bất lợi tái lập khi chỉ thay nhóm chưa bão hòa. Đây là đường tính dưới E1+E2 cố định, còn tác dụng riêng của E2 khi bật/tắt dưới z cần đối chứng. Nguồn: `co-che.json#/cases`, hai mã ca trên, nền E1+E2, `mechanism/worlds/P/flips`.

**OPEN về nhóm chưa bão hòa.** E4 đo phần tăng tỷ lệ vượt biên. Khi các giá trị A đã vượt biên, độ xa của chúng không đi vào tỷ lệ đó. z đưa khoảng cách của cực trị A tới trung vị N vào khóa và chia theo độ phân tán nền. Các ví dụ xác nhận đổi thứ tự tại max, nhưng bảng nhóm chưa tách đóng góp của tử số, IQR và riêng latency-90. Muốn quy lợi ích cho độ lớn của tín hiệu độ trễ, cần replay chẩn đoán chỉ đổi nhóm latency-90 rồi chỉ đổi phần còn lại, giữ cờ/gán/khóa phụ. Muốn tách khoảng cách với độ phân tán, cần đối chiếu trung gian và trình phép bổ sung trước khi chạy. Nếu kết luận sau đó phụ thuộc latency-90, cần kiểm nguồn quan sát tương đương trước khi chuyển sang FlashTicket.

## 7. Đồ thị, giới hạn và quyết định tiếp theo

Nút là service; cạnh từ quan hệ gọi cha–con của trace. E1-U trừ hợp khoảng span con khỏi thời gian thao tác cha, E2-C lấy tín hiệu trên cạnh và gán cho bên được gọi. Metric/log đặt tại thực thể tương ứng. Trong mỗi cặp chính, quan hệ và đường gán giữ cố định; chênh giữa hai nền mô tả tương tác với cả gói E1+E2. Task trả lời phần chọn thang trên dev của RQ3b, chưa hoàn tất đối chứng cấu trúc RQ3d hay đánh giá FlashTicket/RQ5.

Tách nguồn hạn chế: chênh p/m hai máy thuộc số học backend; tràn z thuộc cách biểu diễn/tính; C-e không phân xử thuộc cấu tạo phép so; thiếu z+S1 ở G0/D0 thuộc bằng chứng giao thức; dev nhìn nhiều lần thuộc giới hạn đánh giá. Không quy các điểm này thành lỗi dataset hoặc collector. Vai trò cổng không đổi trong cặp chính, nhưng tương tác gói cổng × điểm còn OPEN. Phép bổ sung tối thiểu theo B4 là z+S1 ghép E4+S1 ở G0/D0 trên cùng revision/ca/khóa; phải trình phạm vi và chi phí riêng, chưa chạy trong task.

Hành động theo B5 trên R0 là đưa z+S1 vào danh sách đề xuất đối chứng QT7. Sức mạnh của đối chứng còn cần so với baseline công bố cùng giao thức. R0 vẫn dựng cạnh từ trace và có chẩn đoán dùng cạnh. Xếp hạng chính E6a ở cấu hình này dùng các kênh theo thực thể, với E1/E2/E5 tắt. Vì vậy, phạm vi đối chứng là thứ hạng chính, còn các đầu ra chẩn đoán được xét riêng.

Minh có ba phương án để cân nhắc cho D24. **E4+S1** là nền đang áp dụng. **z+S1** là ứng viên được luật C hỗ trợ trên dev trong phép so chính, nơi S1 được giữ cố định để tách tác động của điểm. **z+S0** là phương án báo kèm. S0 cao hơn S1 đúng 1/208 ở mỗi nền do cùng một ca. Chênh lệch này chưa đủ chọn S0, và WHY-69 lập luận cho S1 trên E4 nên giữ S1 dưới z cũng cần căn cứ riêng. Nguồn: `luat-c.json#/secondary_z_S1_vs_S0` và `co-che.json#/groups`.

Nếu Minh chọn đổi D24, cần SPEC chạy lại K, kiểm điểm/khóa/bất biến hạng và phần T1 chịu ảnh hưởng. Cần quyết cách xử lý ngoại lệ số học của z trước khi khóa thiết kế. Nền T-049 và quyền mở G3/test do Minh quyết riêng.

## 8. Gián đoạn, lỗi phân tích và bàn giao

Hết usage làm chậm theo dõi/tổng hợp thủ công; các controller M1 vẫn chạy tới đích. B4 có lỗi riêng do trace R0 cũ thiếu oracle. Đã giữ phần dở, kiểm hash trước dùng lại 36 cặp hoàn chỉnh của laptop, rồi tiếp bằng oracle mới với mẫu và E4 trước thay điểm exact. Helper controls cũ thiếu điều kiện source đóng; phần đó bị loại khỏi kết luận, bản mới buộc closed/hash/số ca. Các lượt chuẩn bị/download lỗi được giữ và ghi LOG; không mất hoặc loại ca phương pháp. [LOG](../../tasks/T-048-thang-diem-tham-so-e4/LOG.md), [lịch sử kiểm controls](runs/kiem-controls-history-001/kiem.json).

Kết quả hiện là mô tả dev, kiểm công thức và đường tính trong những ca đã quan sát. Claude đã kiểm lại các phản hồi và đề xuất dừng phản biện. Lượt đáp bổ sung bằng chứng tái lập ở §5–6. Nghiệm thu task và quyết định đổi thiết kế vẫn chờ Minh. Prompt trung tính để Minh chuyển Claude nằm ở mục kết phiên cuối LOG. Không commit/push.
