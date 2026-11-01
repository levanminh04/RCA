# T-045 — Chạy T1, T4, T4b và khối K của M1 trên 52 ca dev (báo cáo)

- **Người làm:** Claude, laptop Windows local. **Người phản biện chính thức:** một phiên Claude mới, độc lập với phiên người làm, theo lời Minh ngày 01/11/2026 (LOG mục "Đổi người phản biện chính thức"; dòng DECISIONS Q-219 chờ ghi). SPEC dòng 4 và Q-215 còn ghi Codex. **Ngày:** 31/10–01/11/2026.
- **SPEC:** `tasks/T-045-chay-khoi-k-dev/SPEC.md` (duyệt 29/10/2026). **Nhật ký:** `tasks/T-045-chay-khoi-k-dev/LOG.md`, phiên 1 (chạy) và phiên 2 (đáp phản biện lượt 1). **Phản biện:** `tasks/T-045-chay-khoi-k-dev/REVIEW.md` (lượt 1).
- **Code M1:** mốc nghiệm thu T-044 `69ef90b6`, cộng ba sửa Minh duyệt ở T-045 (ĐC1 `ec10087a`, ĐC2 `eb14262a`, ĐC3 `bbef69dd`). Lượt khối K, T4, T4b và mọi lượt RE2-TT chạy trên `bbef69dd`, `src/` sạch (`runs/d17-002/nguon.json`, `runs/d45-001/nguon.json`). Các lượt Nezha-OB của T1 (`b2-t1-nezha-*`), D1 (`b2-d1-kE1E2-nezha-001`) và D3 (`b2b-d3-*-nezha-001`) chạy trên `69ef90b6`, trước ba sửa. Ba sửa chỉ đổi adapter RE2-TT và thời gian tính, nên không đổi bản ghi Nezha-OB. Đã so: bản ghi K-E1, K-E2, K-E3 và R0 của các lượt này trùng bản ghi chạy sau sửa (`b5-k16-nezha-001`) ở 22/22 ca, sau khi bỏ `config_id`, `variant` (LOG phiên 2).
- **Trạng thái:** xong bước 0–8 theo SPEC; phiên 2 đã sửa theo phản biện lượt 1 (A1–A3, A5–A8; LOG phiên 2); chờ Minh. **Số dev, không là bằng chứng hiệu quả trên dữ liệu chưa dùng để thiết kế** (SPEC T-043 B4). MRR dev của cấu hình được chọn lạc quan, vì được chọn trong 16 cấu hình (xem thêm mục 9 ý 8).

## 1. Tóm tắt

**Quan sát (có số, có con trỏ):**
1. Code M1 chạy được trên dữ liệu thật sau ba sửa. ĐC1: adapter RE2-TT dừng ở 30/30 ca vì `pd.NA`. ĐC2: `message` rỗng thành chuỗi `'<NA>'`. ĐC3: đường găng E1-CP được tính ở mọi cấu hình, làm chậm 5 lần (`dinh-chinh-cai-dat.md`).
2. T1: bất biến theo hash seed 0, 1, 2 và thứ tự hàng đạt ở 52/52 ca (`t1.json#/RE2-TT/bat_bien`, `#/Nezha-OB/bat_bien`). Số đếm trung gian khớp KS-16; chỗ lệch đều giải thích được (`doi-chieu-ks16.json`).
3. **R0 cho `CAUSE_FOUND` ở 30/30 cửa sổ giả RE2-TT** (`t1.json#/RE2-TT/moc_gia`). Mọi cấu hình khối K và mọi cấu hình T4 cũng 30/30 (`khoi-k.json#/cau_hinh/*/moc_gia`, `t4.json#/cau_hinh/*/moc_gia`). Tỷ lệ qua cổng ở mốc giả: metric hướng lên 31,6%, xuống 20,0%, thao tác trace 11,9%, với α = 0,01. Tính lại độc lập 90 đơn vị: trùng 90/90. Tự tương quan bậc 1 trung vị 0,94 (`runs/b2-t1-re2-mocgia-001/kiem-doc-lap-metric.json`).
4. D2 tái lập 12/12 MRR baseline và số ca có cờ M5 (`tai-lap-baseline.json#/tong_hop`).
5. **Luật chọn khối chọn E1+E2** (E1-U thời gian độc quyền; E2-C khoảng ngoài span bên được gọi). MRR gộp 0,7885; RE2-TT 0,8056; Nezha-OB 0,7652. R0: 0,6385; 0,7178; 0,5304 (`khoi-k.json#/chon_khoi/P`, `#/cau_hinh/K-E1+E2/MRR/P`). Không tình huống dừng nào của SPEC xảy ra. Bước 8 nhất quán ở cả bốn thành phần. S_lo, S_hi chọn giống P.
6. Kết cục theo luật C (dev) tại cấu hình thắng: E1 GIÚP, E2 GIÚP, E3 HẠI (UV-6), E5 HẠI (HẠI gộp, −0,0594) (`khoi-k.json#/cap/E2|E1+E2`, `E1|E1+E2`, `E1+E2|E1+E2+E3`, `E1+E2|E1+E2+E5`).
7. Phép độ bền, 1.000 mẫu ô: E1+E2 thắng 767 lần, E2+E5 190; E2 được bật 979, E1 779, E5 203, E3 0 (`do-ben.json`).
8. T4b (nhánh z, chỉ báo cáo): MRR 0,8005; RE2-TT 0,983; Nezha-OB 0,551 (`t4b.json#/MRR_z`). T4c: 0,6385 → 0,6794 (`t4.json#/T4c`).

**Suy luận (chưa phân xử, có giải thích khác):**
- `verdict` hiện không phân biệt cửa sổ có lỗi và không lỗi trên RE2-TT dev. Code tính đúng thiết kế. Có hai ứng viên, đều thuộc cách tính của phương pháp gặp dữ liệu, không phải lỗi code (luật cứng 17). Phần đóng góp của từng ứng viên vào kết quả 30/30 chưa tách được (sửa ở phiên 2 tiếp theo REVIEW-2 U5):
  - **Quy tắc `verdict`:** CAUSE_FOUND khi tầng 1 có ít nhất một thực thể (`src/m1/xep_hang.py`, hàm `verdict`); quy tắc không xét số phép chấm. Giới hạn này đã khai ở SPEC T-043 dòng 290. Mỗi cửa sổ giả có khoảng 767 phép chấm (23.013 trên 30 cửa sổ; `t1.json#/RE2-TT/moc_gia/cong`). Kể cả khi p đúng danh nghĩa, α = 0,01 vẫn cho kỳ vọng khoảng 7,7 đơn vị qua cổng mỗi cửa sổ; một đơn vị qua cổng và vượt biên ε là đủ CAUSE_FOUND. Số phép chấm không tự chứng minh xác suất báo động gần 1: xác suất có ít nhất một cờ phụ thuộc mức tương quan giữa các đơn vị (khoảng 0,9996 nếu 767 phép độc lập, chỉ 0,01 nếu luôn trùng nhau; minh họa theo giả định, chưa đo trên M1).
  - **Cổng từng đơn vị qua giả nhiều hơn α (đã quan sát; nguyên nhân chưa phân xử):** ở α = 0,001 vẫn còn 1.829 kênh có cờ trên 30 cửa sổ giả, khoảng 61 mỗi cửa sổ (`t4.json#/cau_hinh/T4-e0.05-a0.001/moc_gia/kenh_co_theo_nhom`); mức danh nghĩa chỉ khoảng 0,77 phép qua cổng mỗi cửa sổ. Ứng viên chính: giả định hai mẫu độc lập của cổng (B1.3) gặp metric 1 giây tự tương quan. Mô phỏng AR(1) đã có ở SPEC T-043 dòng 415 (300 + 300 điểm, không lỗi) cho tỷ lệ qua cổng 28,8% ở hệ số 0,9 và 38,6% ở 0,98. T-045 đo hệ số bậc 1 trung vị 0,935 trên 90 đơn vị có cờ (`runs/b2-t1-re2-mocgia-001/kiem-doc-lap-metric.json#/ac1_N_trung_vi`; mẫu chọn theo cờ nên có thể thiên cao) và tỷ lệ metric hướng lên qua cổng 31,6%. Giải thích khác chưa loại được: trôi nền thật giữa hai đoạn 5 phút; mẫu 300 + 300 điểm nhạy với chênh nhỏ.
- E3 không vào bản P7 **ở bản hiện tại** theo luật C trên dev (HẠI, UV-6). Nếu cổng hoặc thang điểm đổi và khối K chạy lại, kết cục của E3, E5 theo lượt mới và phép kiểm bối cảnh KB (mục 9 ý 3, 4). Đường làm root tụt hạng được quan sát nhiều nhất là ô "mẫu mới": ô này gán điểm 1 cho thực thể có từ 10 dòng A không khớp mẫu học từ N (mục 6.4). Nội dung các dòng đó: mục 6.7 (A8). Nguyên nhân chưa phân xử hết.
- E5 tại E1+E2 làm root tụt ở 8 ca và lên ở 7 ca. Phần hại ròng chia gần đều giữa hai đường: quy tắc nhóm vòng C′ (3 ca tụt, cùng ô `ts-travel-service|loss`; 1 ca lên; ròng −1,47) và quy tắc lan thường (5 ca tụt ở 3 ô; 6 ca lên; ròng −1,62) (`co-che-bo-sung.json#/A1_E5_theo_ca/rong_theo_quy_tac`). Cơ chế còn OPEN (mục 6.4). E5 đạt mục tiêu hẹp của nó (ca có cờ M5 giảm từ 8 xuống 5) nhưng vẫn HẠI gộp.
- E4 bão hòa (B1.3) là một ứng viên giải thích vì sao nhánh z và T4c cao hơn R0 trên RE2-TT; chưa chứng minh là nguyên nhân chính. R0 và nhánh z dùng cùng cờ, tầng và tập ứng viên; nhánh z chỉ thay điểm của đơn vị phân vị bằng z không bị chặn (`src/m1/chuoi.py`, khối E4, `nhanh_z`), nên đổi luôn cách ghép đơn vị phân vị với kênh đếm (vẫn trong [0; 1]). Điều số này hỗ trợ: với cùng cờ, đổi cách chấm cho thứ hạng rất khác (RE2-TT 0,718 → 0,983; `t4b.json#/MRR_R0`, `#/MRR_z`), nên cổng hiện tại không làm thứ hạng tốt thành bất khả thi trên RE2-TT dev. Chưa có phép E1, E2 trên nền z.
- **Bằng chứng dev của E1, E2 không độc lập**, vì hai lẽ: cấu hình được chọn trong 16 cấu hình; và E1, E2 được thiết kế từ phép đo P4 trên chính các ca dev này (mục 9 ý 8). 81% phần RR mà E2 thêm ở bối cảnh E1 (3,91 trên 4,83) và 52% phần tăng của E1+E2 so với R0 (4,04 trên 7,80) đến từ 3 ô trễ mạng Nezha-OB (`co-che-bo-sung.json#/A5_dRR_theo_o`). Dev không phân biệt "cơ chế thật" với "khớp dev".

## 2. Đầu vào, kiểm hash, môi trường, sửa code

- Hash T-043 PASS (69/69 tệp; 10/10 hash đóng băng), T-044 PASS (2133/2133), dữ liệu dev PASS (RE2-TT 89 tệp; Nezha-OB 374 tệp) (`runs/b0-kiem-hash-001/`).
- Test T-044: 374/374 qua trên local trước sửa (`runs/b0-test-t044-001/stdout.txt`), và sau mỗi sửa ĐC1–ĐC3. Test riêng của T-045: 16/16 (`tests/`).
- `tat_dinh.py` sau ĐC3: 104 bản ghi × 4 thứ tự × seed 0, 1, 2 giống hệt `results/T-044/runs/tat-dinh-012` (`runs/sua-dc-001/`).
- Môi trường: `D:/RCA-ext/envs/py312-pin`, `PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages`; Python 3.12.10; numpy 1.26.4, scipy 1.14.1, pandas 2.2.3, pyarrow 18.1.0, networkx 2.5, drain3 0.9.11 (`scripts/moi_truong.sh`).
- Chạy song song 4 tiến trình (Minh duyệt). Bộ điều phối v2 kiểm từng đơn vị ngay khi xong: hash, seed, tham số, số bản ghi, status. Nó dừng ngay ở lỗi đầu tiên và chặn khi RAM thấp (`scripts/chay_song_song.py`). Bản ghi từng ca được ghép theo (cấu hình, ca), cho đúng từng byte như chạy chung (Đ-1). Hai đợt chính: `runs/d17-002` (510/510 đạt) và `runs/d45-001` (156/156 đạt).
- Đối chiếu chéo trong đợt (`scripts/kiem_dot.py`): K-R0 và T4-e0.05-a0.01 cho bản ghi trùng T1-R0 (sau khi bỏ `config_id`, `variant`) ở mọi ca, cả cửa sổ thật và mốc giả.

## 3. T1 — kiểm cài đặt trên dữ liệu thật

| Kiểm | RE2-TT | Nezha-OB | Con trỏ |
|---|---|---|---|
| Hash seed 0/1/2, xáo hàng | đạt 30/30 | đạt 22/22 | `t1.json#/*/bat_bien` |
| Status | 30 OK | 22 OK | `#/*/tong_hop/status` |
| Điểm > 1 / > 1e6, toàn hòa, ngưỡng cực lớn, gộp khóa | 0 | 0 | `#/*/tong_hop/QT5` |
| Cột metric chưa khai nguồn, nguồn UNSUPPORTED, OBS_DEPENDENT, RANK_CHANGED | 0 | 0 | như trên |
| Ca có một nhóm kênh > 90% | 6 (metric) | 5 (ít kênh) | như trên |
| Đ5: đơn vị đếm đổi quyết định khi T lệch ±1% | 0/46 | 0/12 | `#/*/tong_hop/D5_T_lech_1pt` |
| Biên p = α | 0 trên 1.299.105 giá trị p | | LOG 23:02 |

- QT5 "một nhóm kênh chiếm gần hết": metric chiếm 76% kênh có cờ ở RE2-TT. Đã soi (mục 1, ý 3 và phần suy luận): code đúng; cổng từng đơn vị qua giả nhiều hơn α là quan sát; ứng viên nguyên nhân là giả định độc lập của cổng (B1.3) gặp dữ liệu tự tương quan, cùng trôi nền và cỡ mẫu, chưa phân xử; quy tắc `verdict` không xét số phép chấm là ứng viên thứ hai, phần đóng góp chưa tách. Chưa sửa; Minh hoãn theo D17 (Q-b).
- D1 (`doi-chieu-ks16.json`): mọi số đếm span, bỏ lặp, mồ côi, gốc, bọc, vượt biên, thao tác (E1 tắt và bật), cạnh E2, metric, log khớp KS-16 ở 52/52 ca. Lệch đã giải thích:
  - Nezha-OB: trường quan sát khớp luật F phương án (a) của Q-207 ở 22/22 ca, với sai khác ≤ 2 µs do cắt mốc về µs.
  - RE2-TT: 7 ca lệch 3–12 ms ở đầu H của trace phía N, do định nghĩa bản ghi trong cửa sổ khác nhau.
  - Một ca RE2-TT không có tệp log.

## 4. D3, D4, D5 và D17

- **D3** (`e3-khong-nhan.json`):
  - RE2-TT: ba cách khớp gần như trùng. 0/997 dòng lỗi A rơi vào mẫu thường. Thực thể có cờ "mẫu mới" ở mốc giả: 83 với (a), 81 với (b) và (c), trong 24/30 cửa sổ.
  - Nezha-OB, ngưỡng 0,4: dòng lỗi A rơi vào mẫu thường (a) 1.706/4.128, (b) 2.833, (c) 0. Ngưỡng 0,9: 0 ở mọi cách.
- **D4** (`e1-cp.json`): 444 cha (khớp KS-16); u_CP ≠ u_U ở 4 cha (lớn nhất 1.272 µs).
- **D5** (`nhom-vong.json`): tính lại từ bản ghi, 960/960 bản ghi đạt kiểm tái lập. Cách đọc C′ và A khác nhau tối đa 1 kênh ở 1 ca mỗi cấu hình (RE2-TT); Nezha-OB 0.
- **D17 (Minh quyết 01/11/2026, sau khi xem số dev T1):**
  - không đặt mức tuyệt đối, ghi giới hạn;
  - chạy tiếp khối K và mở mục thiết kế riêng cho cổng và `verdict` sau;
  - đo thêm mốc giả cho T4;
  - giữ cách khớp (a);
  - dùng lại lượt khối K RE2-TT làm bước 5 (LOG mục "D17 đã quyết").

## 5. T4, T4b (chỉ báo cáo)

| ε \\ α | 0,001 | 0,01 | 0,05 |
|---|---|---|---|
| 0 | 0,330 | 0,359 | 0,365 |
| 0,05 | 0,625 | **0,6385 (R0)** | 0,623 |
| 0,2 | 0,624 | 0,637 | 0,632 |

MRR gộp (`t4.json#/cau_hinh/*/MRR_P`). Tỷ lệ `CAUSE_FOUND` ở mốc giả là 1,0 ở cả 9 cấu hình (`#/cau_hinh/*/moc_gia`): siết α hoặc ε không làm giảm báo nhầm.

- T4c (`t4.json#/T4c`): MRR 0,6385 → 0,6794 (RE2-TT 0,718 → 0,765; Nezha-OB 0,530 → 0,563); 4 ca tăng, 0 ca giảm.
- T4b (`t4b.json`): MRR 0,8005 (RE2-TT 0,983; Nezha-OB 0,551). So với R0: Hit@1 sửa 16 ca, hỏng 4 ca.
  - Vế (1) của Q5 đạt: điểm E4 hữu hạn và trong [0; 1] ở mọi lượt R0, T4, khối K; điểm z hữu hạn.
  - Phân bố z: trung vị 4,5; p99 3.907; lớn nhất 640.830.
  - Vế (2) chỉ mô tả; không đổi nền khối K (D24).

## 6. Khối K

### 6.1 D2 trước luật C
12/12 (baseline, dataset) có MRR khớp bảng G2 và KS-16; số ca có cờ M5 khớp KS-16 theo cả quy tắc của M1 và của KS-16; 0 bản ghi P3 lệch hash (`tai-lap-baseline.json`).

### 6.2 MRR từng cấu hình (P; `khoi-k.json#/cau_hinh/*/MRR/P`)

| Cấu hình | Gộp | RE2-TT | Nezha-OB | Ca có cờ M5 | Hit@1 |
|---|---|---|---|---|---|
| **E1+E2** | **0,7885** | 0,8056 | 0,7652 | 8 | 33 |
| E2+E5 | 0,7350 | 0,7181 | 0,7580 | 5 | 32 |
| E1+E2+E5 | 0,7290 | 0,7122 | 0,7519 | 5 | 32 |
| E2 | 0,7109 | 0,7261 | 0,6902 | 17 | 29 |
| E1 | 0,6955 | 0,7750 | 0,5871 | 12 | 27,1 |
| E5 | 0,6510 | 0,6969 | 0,5884 | 11 | 26 |
| R0 | 0,6385 | 0,7178 | 0,5304 | 21 | 24 |
| Có E3 (8 cấu hình) | 0,4282–0,6849 | 0,3558–0,6204 | 0,5270–0,7727 | 10–28 | 11–27 |

### 6.3 Luật C và luật chọn khối
- 43 cặp; tại P: 22 GIÚP, 15 HẠI, 2 KHÔNG TÁC DỤNG, 4 TRÁI CHIỀU theo dataset (đều là cặp (R0, c) có E3). 0 cặp phụ thuộc quan sát (`khoi-k.json#/cap`).
- **Vế mốc giả: "không phân xử được" ở 43/43 cặp**, vì nhánh tắt đã 30/30. Bỏ vế này thì kết cục không đổi ở cặp nào (`#/cap/*/khong_moc_gia`).
- HẠI riêng: UV-6 ở 8 cặp E3; M + M′ ≥ 3 với P + P′ = 0 ở cặp E2+E5 → E1+E2+E5 (chênh MRR chỉ −0,006).
- Báo kèm, không dùng để quyết:
  - kết cục đổi ở 1 cặp với δ = 0,005 và ở 4 cặp với δ = 0,02;
  - kiểm dấu tại cấu hình thắng: E1 p = 7/64 (cặp E2|E1+E2), E2 p = 1/8 (cặp E1|E1+E2) (không đạt mức thường dùng).
- Vết luật chọn khối (`#/chon_khoi/P`):
  - lượt một loại 10 cấu hình (8 cấu hình có E3; E1+E5; E1+E2+E5);
  - tập cố định {R0, E1, E2, E5, E1+E2, E2+E5};
  - lượt hai không loại thêm;
  - tập gần tốt nhất chỉ còn {E1+E2};
  - cờ TRÁI CHIỀU nằm ở 4 cặp (R0, c có E3), không ở cấu hình thắng hay cấu hình có MRR cao hơn.
- Bước 8 (`#/buoc8`): nhất quán ở E1, E2 (đang bật, GIÚP) và E3, E5 (đang tắt, HẠI). Bước 10: S_lo, S_hi cũng chọn E1+E2. Bảng mặc định: không mục nào kích hoạt (`#/mac_dinh_ap`).
- Ca hỏng / sửa theo Hit@1 (`#/ca_hong_sua_P`):
  - R0 → E1+E2: hỏng 1, sửa 10;
  - R0 → E3: hỏng 17 (RE2-TT 13), sửa 4;
  - E1+E2 → E1+E2+E5: hỏng 5, sửa 4.

### 6.4 Lần theo cơ chế (`co-che-khoi-k.json`; quan sát cộng suy luận, chưa phân xử)
- **E3:**
  - Quan sát: ở R0 → E3, root tụt RR ở 33/52 ca. Trong 94 lượt thực thể mới vượt lên trên root, kênh mạnh nhất là ô "mẫu mới" 68 lượt, mẫu thường giảm 24 lượt.
  - Điều kiện và bước: có từ 10 dòng A không khớp mẫu học từ N. Ô "mẫu mới" có n_N = 0, nên e = 1, mức tối đa, và thực thể nhảy lên đầu khóa.
  - D3 cho thấy ô này có cờ cả ở 24/30 cửa sổ không lỗi.
  - Giải thích khác chưa loại: một phần mẫu mới là triệu chứng lan thật từ root lên bên gọi. Cặp E3 → E3+E5 phục hồi +0,154, khớp một phần với giải thích này.
  - Nội dung các dòng rơi vào ô "mẫu mới" và phân loại theo luật khai trước: mục 6.7 (phiên 2, A8).
- **E5 khi đã có E1+E2** (sửa ở phiên 2 theo phản biện R1, A1; `co-che-bo-sung.json#/A1_E5_theo_ca`):
  - Quan sát: root tụt ở 8 ca, lên ở 7 ca, không đổi ở 37 ca. E5 chỉ xóa kênh, nên root chỉ tụt khi chính root mất kênh, và chỉ lên khi thực thể đứng trước root mất kênh.
  - Theo ca và quy tắc (mỗi ca thuộc đúng một nhóm quy tắc, nên các phần không cộng chồng):

    | Đường | Ca tụt | ΔRR ca tụt | Ca lên | ΔRR ca lên | Ròng |
    |---|---|---|---|---|---|
    | Nhóm vòng C′ | 3, cùng ô `ts-travel-service\|loss` | −1,72 | 1 (`ts-train-service\|cpu`) | +0,25 | −1,47 |
    | Lan ngược, lan xuôi thường | 5, ở 3 ô (`ts-order-service\|loss` 2, `frontend\|return` 2, `checkoutservice\|return` 1) | −3,87 | 6 | +2,25 | −1,62 |

    Tổng −3,09/52 = −0,0594, khớp `khoi-k.json#/cap/E1+E2|E1+E2+E5/theo_the_gioi/P/dMRR/gop`. Nezha-OB không có nhóm vòng nào (`nhom-vong.json`), nhưng có 3/8 ca tụt.
  - Số cũ "428/461 lần xóa qua nhóm vòng" đếm theo cặp (kênh bị xóa, bên giải thích), chỉ ở 8 ca tụt (`co-che-khoi-k.json#/E5_E1+E2/quy_tac`). Số đó đúng, nhưng 428 cặp đến từ 3 ca của một ô. Câu cũ "E5 hại chủ yếu qua quy tắc nhóm vòng" sai khi tính theo ca, theo ô và theo RR; đã bỏ. Ví dụ vòng {seat, travel, travel2} chỉ đúng cho ô `ts-travel-service|loss`.
  - Đối chiếu ca có điều kiện tương ứng (SPEC T-045 dòng 115): root mất ít nhất một kênh ở 26 ca. RR tụt ở 8 ca (root còn kênh tự sinh ở 4), không đổi ở 14 ca (root còn kênh tự sinh ở cả 14), lên ở 4 ca (`#/A1_E5_theo_ca/doi_chieu_root_mat_kenh`). Mất hết kênh tự sinh chỉ xảy ra ở ca tụt; nhưng 4 ca tụt vẫn còn kênh tự sinh, trong đó có 3 ca nhóm vòng. Điều kiện "còn kênh tự sinh" không tách được ca tụt với ca không đổi.
  - Cờ M5 (`#/A1_M5_doi_chieu`): ca có điều kiện "có thực thể có kênh tự sinh và có đường tới root trong G_N" chiếm 37/52 ca ở E1+E2; cờ M5 bật ở 8 ca trong số đó (RR trung bình 0,40), không bật ở 29 ca (0,84). Ở E1+E2+E5: 33 ca có điều kiện; M5 bật ở 5 (0,125), không bật ở 28 (0,76). E5 giảm số ca có cờ M5 từ 8 xuống 5 (mục tiêu hẹp của E5) nhưng vẫn HẠI gộp. Các số này chỉ mô tả, không xác nhận cơ chế.
  - Cơ chế còn OPEN. Bỏ cách nói "đúng điều kiện thất bại CĐ3" khỏi vai trò giải thích chính: quy tắc nhóm vòng chỉ giải thích khoảng một nửa phần hại ròng, ở một ô.
  - Dấu vết E5 (`khoi-k.json#/dau_vet_E5/E1+E2|E1+E2+E5`): root mất kênh ở 26/52 ca, mất hết bằng chứng tự sinh ở 4 ca. Ở mốc giả, 518/1.256 kênh lớp lan bị coi là kế thừa.

### 6.5 Đối chứng (chỉ báo cáo)
- C-d1 tại cấu hình thắng: MRR 0,4924 (R0: 0,4782) (`#/cau_hinh/K-E1+E2/doi_chung`).
- **C-d3 suy biến trên dev:** MRR 0 ở mọi cấu hình. Có 24 ca RE2-TT UNSUPPORTED_CYCLIC (đồ thị con có chu trình), 22 ca Nezha-OB NO_TARGET (Nezha-OB không có span gốc), 6 ca OK nhưng không xếp được root, vì ở cả 6 ca root nằm trong tập đích nên không là ứng viên (`#/cau_hinh/*/doi_chung_trang_thai`; kiểm trên bản ghi K-R0 và K-E1+E2, trường `extra.doi_chung.C-d3.dich`, `ung_vien` so với root; LOG phiên 2). C-d3 suy biến không là bằng chứng M1 vượt một đối chứng mạnh. Theo bảng ứng viên SPEC T-043, "suy biến: bỏ, ghi lý do"; quyết ở task (3).

### 6.6 E3, E5: ô mục tiêu, ngoài mục tiêu và hai phép không nhãn của E5 (phiên 2, theo phản biện A7; `co-che-bo-sung.json`)

Chỉ mô tả và tìm nguyên nhân; không dùng để chọn lại. E_X là tập ô kích hoạt khai ở T0 (E3: 4 ô lỗi mã Nezha-OB; E5: 20 ô).

| Cặp | P | M | P′ | M′ | Kết cục | ΣΔRR trong E_X | ΣΔRR ngoài E_X |
|---|---|---|---|---|---|---|---|
| R0 → E3 | 3 | 1 | 2 | 15 | HẠI | +1,33 (Nezha-OB) | −12,27 (RE2-TT −10,86; Nezha-OB −1,41) |
| E1+E2 → E1+E2+E3 | 3 | 1 | 0 | 17 | HẠI | +0,67 (Nezha-OB) | −18,19 (RE2-TT −13,30; Nezha-OB −4,88) |
| R0 → E5 | 11 | 4 | 0 | 1 | GIÚP | +1,95 (RE2-TT −0,63; Nezha-OB +2,58) | −1,30 (Nezha-OB) |
| E1+E2 → E1+E2+E5 | 6 | 3 | 0 | 1 | HẠI | −1,49 (RE2-TT −2,80; Nezha-OB +1,31) | −1,60 (Nezha-OB) |

(`#/A7_o_muc_tieu`.)
- **E3:** trong ô mục tiêu, E3 có lợi nhỏ; phần hại nằm ngoài mục tiêu, chủ yếu ở RE2-TT, nơi không có lỗi mã.
- **E5 tại E1+E2:** khác E3. Số ô tăng nhiều hơn số ô giảm (P = 6, M = 3), nhưng tổng ΔRR trong ô mục tiêu vẫn âm (−1,49), do các ô RE2-TT (−2,80). 6/8 ca tụt nằm trong ô mục tiêu (`#/A1_E5_theo_ca/ca/*/o_trong_E_X_E5`). Câu "phần hại nằm ở chỗ khác" chỉ đúng với E3.

**Hai phép không nhãn của E5** (cấu hình E1+E2+E5, thế giới P; dựng lại kênh và cạnh từ bản ghi, kiểm tái lập trước: 52/52 ca cửa sổ thật và 30/30 cửa sổ giả tái lập đúng F_I và `inherited_by`):
1. **E9 sẽ phủ quyết bao nhiêu lần xóa** (Đ11, CĐ9; o_s = 10 giây, τ = 1 ms) (`#/A7_E9_phu_quyet`):
   - cửa sổ thật: 1.055 kênh bị xóa; E9 phủ quyết 17. Còn lại: 345 kênh được miễn vì đường giải thích đi qua cạnh E2 bất thường (CĐ9), 83 kênh thiếu khởi phát, 610 kênh đã xét và không phủ quyết;
   - kênh của root ở 8 ca tụt (20 kênh): E9 phủ quyết 0. Bỏ cả miễn trừ CĐ9 (cận trên, vì tập cạnh E2 dựng lại chỉ xấp xỉ) vẫn 0;
   - cửa sổ giả: 518 kênh bị xóa; E9 phủ quyết 46.
2. **Kênh giải thích có cờ ở cửa sổ giả cùng ca không** (RE2-TT; cùng mã kênh, cùng cấu hình) (`#/A7_giai_thich_co_o_moc_gia`): 1.802/16.912 cặp (kênh bị xóa, kênh giải thích), tức 10,7%; riêng các lần xóa kênh root ở ca tụt: 18/446 cặp, tức 4,0%.

Đọc: hai phép này **không** giải thích phần lớn các lần xóa gây hại. Thiếu thứ tự thời gian (E9) không phải đường chính: E9 không cứu kênh root nào ở ca tụt. Kênh giải thích của các lần xóa gây hại hiếm khi có cờ ở cửa sổ giả; đây là phép thay thế thô cho giả thuyết "cổng qua giả tạo bên giải thích giả", nên chưa bác bỏ hẳn giả thuyết đó (một kênh có thể qua giả ở cửa sổ thật mà không qua giả ở cửa sổ t − 300). Hệ quả cho task (2): E9 (T11) chỉ có việc khi E5 bật (`results/T-043/dinh-nghia-pha2.json#/o_kich_hoat/E9/co_che`); trên dev, kể cả khi E5 bật, E9 chỉ đổi 17/1.055 lần xóa.

### 6.7 E3: nội dung các dòng rơi vào ô "mẫu mới" (phiên 2, theo phản biện A8; `e3-noi-dung-mau.json`)

Chỉ để tìm nguyên nhân và thiết kế E3 cho chặng sau; không dùng để chọn lại E3. Cách làm: dựng lại riêng bước Drain của E3 (cách khớp (a), ngưỡng 0,4, độ sâu 4) trên 33 ca có root tụt ở cặp (R0, E3) và 24 cửa sổ giả của các ca RE2-TT trong số đó; 57/57 cửa sổ tái lập đúng bản ghi K-E3. Luật chọn ca và phân loại khai trước trong docstring `scripts/kiem_mau_e3.py`: (a) có tên lỗi rõ; (b) có mẫu cùng số token nhưng nội dung khác; (c) khác số token với mọi mẫu đã biết của thực thể (với cách khớp (a), Drain chỉ so mẫu cùng số token, nên dòng này không thể khớp); (d) hỏng. Lượt `a8-mau-e3-002` thêm hai mô tả sau khi xem lượt 001: tách root khỏi nhóm "khác"; đếm dòng khung ngăn xếp Java.

| Dataset, cửa sổ, nhóm thực thể | Số dòng | (a) | (b) | (c) | (d) | Dòng khung ngăn xếp |
|---|---|---|---|---|---|---|
| RE2-TT thật, root | 3.983 | 4,1% | 0,0% | 93,9% | 2,0% | 3.602 (90%) |
| RE2-TT thật, bên gọi root | 6.234 | 2,7% | 1,1% | 95,2% | 1,0% | 3.452 (55%) |
| RE2-TT thật, thực thể khác | 20.590 | 0,6% | 8,8% | 90,5% | 0,2% | 2.034 (10%) |
| RE2-TT thật, thực thể vượt mới root qua ô mẫu mới | 20.120 | 0,4% | 9,0% | 90,5% | 0,1% | 1.492 (7%) |
| RE2-TT cửa sổ giả, mọi thực thể có cờ | 24.329 | 0,2% | 6,3% | 93,5% | 0,0% | 636 (3%) |
| Nezha-OB thật, root | 1.072 | 99,8% | 0,2% | 0,0% | 0,0% | 0 |
| Nezha-OB thật, bên gọi root | 173 | 0,0% | 72,8% | 27,2% | 0,0% | 0 |
| Nezha-OB thật, thực thể khác | 176 | 0,0% | 82,4% | 17,6% | 0,0% | 0 |
| Nezha-OB thật, thực thể vượt mới root qua ô mẫu mới | 130 | 0,0% | 79,2% | 20,8% | 0,0% | 0 |

(`#/ti_le_theo_loai`, `#/khung_ngan_xep_theo_loai`; dạng dòng nhiều nhất ở `#/dang_nhieu_nhat`.)

Quan sát:
- **Dòng của chính root** có tên lỗi hoặc là ngoại lệ: Nezha-OB 99,8% dòng có tên lỗi (dạng `TraceID: …, SpanID: … Request error`); RE2-TT 90% là dòng khung ngăn xếp Java (`at org.springframework…`), tức một ngoại lệ nhiều dòng bị tách thành từng dòng log. E3 có bắt được triệu chứng lỗi của root.
- **Dòng của thực thể vượt lên trên root** hiếm khi có tên lỗi theo luật phân loại (RE2-TT 0,4%; Nezha-OB 0%); RE2-TT 92% có tiền tố ngày giờ và 7% là khung ngăn xếp (`#/tien_to/RE2-TT|that|vuot_moi_mau_moi`, `#/khung_ngan_xep_theo_loai`). Các dạng dòng nhiều nhất (`#/dang_nhieu_nhat`) gộp mọi thực thể có cờ mẫu mới, không riêng thực thể vượt mới: RE2-TT gồm dòng INFO có danh sách dài thay đổi (ví dụ `Left ticket info is: LeftTicketInfo{soldTickets=[…]}`) và dòng khung ngăn xếp; Nezha-OB (ngoài root) gồm dòng nghiệp vụ mang mã sản phẩm không bị che (ví dụ `product_id:"0PUK6V6EV0"`). Không có từ khóa lỗi không tự chứng minh dòng không mang triệu chứng lỗi.
- **Cửa sổ giả** có cùng dạng dòng và cùng tỷ lệ loại (c) như dòng của thực thể vượt mới (93,5% so với 90,5%); khung ngăn xếp chỉ 3%.
- Bên gọi root ở RE2-TT có 55% dòng khung ngăn xếp: một phần là ngoại lệ lan thật từ root.
- 24 cặp (ca, thực thể) vượt mới root qua kênh mẫu Drain (không phải ô mẫu mới), 45 kênh, đều là mẫu lớp thường, hướng xuống (`#/khuon_thuc_the_vuot_moi`): số dòng của một dòng log bình thường giảm ở A.

Suy luận (chưa phân xử; mức bằng chứng: mô tả, chưa xác nhận nguyên nhân gây hại): trên dev, ô "mẫu mới" có vẻ phần lớn phản ánh việc dòng log khác số token hoặc mang mã không bị che, hơn là sự kiện lỗi mới; khớp việc nó bật cả ở cửa sổ không lỗi. Ứng viên nguyên nhân: cách tách mẫu (che token, Drain nhóm theo số token, khớp chặt (a)) gặp định dạng log của dataset (ngoại lệ nhiều dòng, danh sách dài, mã sản phẩm), cộng cách chấm ô "mẫu mới" không có nền (n_N = 0 cho e = 1). "Dataset kém" chỉ đúng một phần: định dạng log là của dataset, nhưng FlashTicket cũng có thể có ngoại lệ nhiều dòng. Phân loại theo luật từ khóa có thể sót tên lỗi viết khác. Hướng sửa, nếu thử lại E3 (Minh quyết): gom ngoại lệ nhiều dòng thành một sự kiện, che thêm mã định danh, và có nền cho ô "mẫu mới", theo công trình trước; ghi WHY trước khi dùng.

## 7. Phép độ bền (chỉ báo cáo; `do-ben.json`)
- Seed 20261101, ghi ở LOG trước khi chạy; 1.000 mẫu ô. Mẫu gốc chọn lại E1+E2.
- Không mẫu nào rơi vào tình huống dừng. Cấu hình thắng: E1+E2 767, E2+E5 190, E2 22, E5 9, E1 8, E1+E5 4.
- Tần suất được bật: E2 979, E1 779, E5 203, E3 0.
- Cờ ở cấu hình thắng: TRÁI CHIỀU 12 (đếm khi cờ TRÁI CHIỀU nằm ở cấu hình thắng hoặc ở cấu hình có MRR cao hơn, tức điều kiện trình Minh của luật chọn khối bước 6; `scripts/do_ben.py`, hàm `mot_mau`), phụ thuộc quan sát 0, xung đột bước 8 là 0.
- Diễn giải: lựa chọn E2 rất ổn định trên dev; giữa E1 và E5 còn mong manh (khoảng 1/5 mẫu chọn E2+E5).

## 8. Theo loại lỗi (mô tả; `theo-loai-loi.json`)

| Dataset, loại lỗi | R0 | E1+E2 | z (T4b) | TORAI B | SimpleRCA | BARO |
|---|---|---|---|---|---|---|
| RE2-TT, tất cả (30) | 0,718 | 0,806 | 0,983 | 0,917 | 0,891 | 0,768 |
| RE2-TT, delay | 0,464 | 0,597 | 1,000 | 1,000 | 0,806 | 0,575 |
| RE2-TT, cpu | 0,639 | 0,792 | 0,917 | 0,778 | 1,000 | 0,792 |
| Nezha-OB, tất cả (22) | 0,530 | 0,765 | 0,551 | không chạy được | 0,538 (M4) | 0,527 |
| Nezha-OB, network_delay | 0,243 | 0,917 | 0,230 | không chạy được | 0,333 | 0,295 |

- Baseline chỉ để định vị, không dùng để chọn (QT4). Biên E-04 là "không thua TORAI B" trên test RE2-TT, đo bằng khoảng tin cậy của chênh MRR với Δ = 0,05 (WHY-06, Q-211); số dev ở đây không là phép kiểm E-04.
- Thứ tự trên số gộp nhạy với nhóm ca (phép mô tả hậu nghiệm, theo REVIEW-2 U7). Bỏ 6 ca trễ mạng Nezha-OB, trên 46 ca: E1+E2 0,772; SimpleRCA (native ở RE2-TT, M4 ở Nezha-OB) 0,795; R0+z 0,875. Trên 16 ca Nezha-OB còn lại: E1+E2 0,708; SimpleRCA M4 0,614; R0+z 0,672. Cách tính: cộng n × MRR theo dòng loại lỗi của `theo-loai-loi.json` (`#/thang E1+E2`, `#/z (T4b)`, `#/baseline simplerca~1native`, `#/baseline simplerca~1M4`), bỏ dòng `tat_ca` và `Nezha-OB|network_delay`. Không là lý do loại 6 ca khỏi đánh giá chính hay chọn lại cấu hình.
- TORAI B không chạy được trên Nezha-OB: UNSUPPORTED ở 22/22 ca (Q-85; `results/T-034/bang-baseline.json#/ranking_mode_a/Nezha-OB_main/methods/torai_B/status`). `theo-loai-loi.json` ghi MRR 0 vì ca UNSUPPORTED được chấm là trượt (WHY-28); số 0 đó không có nghĩa TORAI B xếp sai mọi ca.
- Các dòng theo loại lỗi của RE2-TT có 6 ca (cpu, delay, disk, loss) hoặc 3 ca (mem, socket) (`theo-loai-loi.json#/R0/RE2-TT|mem/n`). Ở dòng 3 ca, một ca đổi hạng làm MRR dòng đổi tới 1/3. Mỗi ô (root, loại lỗi) của RE2-TT có 3 ca.

## 9. Điều chưa phân xử, giới hạn, quyết định cho task (2)

**Chưa phân xử / giới hạn:**
1. Báo nhầm của `verdict` (mục 1, 3): hai ứng viên, chưa tách được phần đóng góp. (i) Quy tắc `verdict` không xét số phép chấm (khoảng 767 phép mỗi cửa sổ, không hiệu chỉnh; SPEC T-043 dòng 290). (ii) Cổng từng đơn vị qua giả nhiều hơn α; ứng viên chính là giả định độc lập (B1.3) gặp metric tự tương quan (mô phỏng SPEC T-043 dòng 415 cùng bậc với số đo); trôi nền và cỡ mẫu chưa loại được. Nếu chỉ sửa (ii), `verdict` vẫn có thể báo nhầm nhiều ở cửa sổ giả; mức độ phụ thuộc tương quan giữa các đơn vị, chưa đo. Vế mốc giả của luật C không hoạt động trên dev. Minh đã chọn mở mục thiết kế riêng (Q-b).
2. Thang điểm: nhánh z và T4c cao hơn R0 trên RE2-TT; E4 bão hòa là một ứng viên, chưa là nguyên nhân đã xác lập; nhánh z còn đổi cách ghép đơn vị phân vị với kênh đếm (mục 1). D24 giữ E4 làm nền khối K; đổi thang điểm là đổi thiết kế sau khi nhìn số dev, Minh quyết. Nhánh z mới thử trên R0, chưa thử cùng E1+E2. **Giới hạn đối chứng (QT7, MRP §6):** R0 (0,718 trên RE2-TT) thấp hơn SimpleRCA (0,891), nên E1+E2 hơn R0 chưa đủ cho khẳng định rộng về lợi ích dùng quan hệ; nghĩa vụ đối chứng mạnh xử lý trước khi khóa danh sách so sánh ở G3 (B6), không phải yêu cầu đồ thị phải thắng.
3. E3: không vào bản P7 **ở bản hiện tại** theo luật C trên dev (HẠI, UV-6; HẠI xét trước KHÔNG ĐỦ CA nên thành phần ít ca bị HẠI không được giữ). Đường làm root tụt được quan sát nhiều nhất là ô "mẫu mới" (n_N = 0 cho e = 1); nội dung dòng ở mục 6.7. Phần hại nằm ngoài ô mục tiêu (mục 6.6). Nguyên nhân chưa phân xử hết. Nếu khối K chạy lại sau khi đổi cổng hoặc thang điểm, kết cục của E3 theo lượt mới và KB; ngoài ra E3 còn là ứng viên cho chặng sau, chưa có quyết định thử lại (Minh quyết). Ngưỡng Drain 0,4 và cách khớp (a) đã dùng để sinh kết quả khối K; lý do và phương án khác có ở `results/T-044/de-xuat-why.md` (mục cách khớp và Đề xuất 3), chờ Minh duyệt ghi WHY (luật cứng 3).
4. E5: không vào bản P7 **ở bản hiện tại** theo luật C trên dev (HẠI gộp tại E1+E2). Hai đường gây hại gần ngang nhau: nhóm vòng C′ (một ô) và quy tắc lan thường (mục 6.4). Phần hại nằm cả trong ô mục tiêu (mục 6.6). Hai phép không nhãn (E9, kênh giải thích ở cửa sổ giả) không giải thích phần lớn các lần xóa gây hại. Nguyên nhân chưa phân xử. Nếu khối K chạy lại sau khi đổi cổng hoặc thang điểm, kết cục của E5 theo lượt mới và KB; kiểm trên FlashTicket chỉ là đề xuất có điều kiện (Minh quyết).
5. Kết cục luật C trên 52 ca dễ đổi khi đổi mẫu: phép độ bền cho E1+E2 76,7%, E2+E5 19%.
6. C-d3 suy biến trên dev (chu trình, không có span gốc).
7. Mọi kết luận ghi kèm: "dưới A0; ô OPEN bị loại ở cả hai phía; độ nhạy chỉ gồm S_lo và S_hi". Trong lượt này, MRR ở S_lo, S_hi trùng P ở cả 16 cấu hình và cả hai dataset (`khoi-k.json#/cau_hinh/*/MRR`), 0 cặp phụ thuộc quan sát: RE2-TT dev không có ô OPEN; Nezha-OB có khe OPEN nhưng không đổi MRR. Không suy ra bước 10 luôn mất khả năng phân biệt.
8. **Bằng chứng dev của E1, E2 không độc lập** (theo phản biện A5). Hai lẽ:
   - cấu hình được chọn trong 16 cấu hình (SPEC T-043 B4);
   - E1, E2 được thiết kế từ phép đo P4 trên chính các ca dev này. E2 từ G2-H06 và UV-1, đo trên 6 ca trễ mạng Nezha-OB dev (`results/T-034/goi-g2.md:356`; gói G2 ghi "định nghĩa vị trí đặt sau khi xem dev", dòng 360). E1 từ UV-2: "tách được root ở 26/26 ca RE2-TT" (`goi-g2.md:708`).
   - Phần lợi rơi đúng vào các ca đó: 81% phần RR mà E2 thêm ở bối cảnh E1 (3,91 trên 4,83) và 52% phần tăng của E1+E2 so với R0 (4,04 trên 7,80) đến từ 3 ô trễ mạng Nezha-OB (`co-che-bo-sung.json#/A5_dRR_theo_o`). Phần lợi của E1 ở bối cảnh E2 nằm chủ yếu ở các ô RE2-TT dev (`#/A5_dRR_theo_o/E2 → E1+E2/theo_o`).
   - Cả "cơ chế thật" lẫn "khớp dev" đều dự đoán mẫu hình này; dev không phân xử được. Giải thích khác, chưa kiểm: E1, E2 bù cho điểm E4 bão hòa (mục 9 ý 2).
   - Điều làm giảm lo: E1, E2 dựa trên ý của công trình trước; không tham số nào chỉnh theo MRR dev; luật chọn và ma trận đóng băng trước khi có số của M1. Rủi ro nằm ở "chọn thành phần theo lỗi đã thấy trên dev", không ở "chỉnh tham số theo điểm".
   - Phân xử cần dữ liệu chưa dùng để thiết kế: test sau G3, dataset giữ ngoài, FlashTicket. Cách đọc khai trước thuộc hồ sơ G3 (task (3)); Minh quyết.

**Quyết định cho task (2) (đề xuất, chờ Minh):**
- Nền cho K-b, T6, T9, T11, T12, KB: cấu hình thắng E1+E2. K-b chỉ hoán E2-VC tại E1+E2 và tại cấu hình đầy đủ (E1-CP đã khai trước KHÔNG ĐỦ CA).
- Trước task (2), Minh quyết có xử lý vấn đề cổng/`verdict` (mục 9.1) và thang điểm (9.2) trước hay không. Đổi một trong hai sau này có thể làm lựa chọn khối K phải chạy lại, và khi đó kết cục của E1, E2, E3, E5 theo lượt mới (mục 9 ý 3, 4).
- Vị trí so với baseline (chỉ định vị, không dùng để chọn; mục 8): trên RE2-TT dev, E1+E2 (0,806) thấp hơn SimpleRCA (0,891) và TORAI B (0,917); R0+z đạt 0,983. Thứ tự này nhạy với nhóm ca.

## 10. Tiêu chí xong (SPEC T-045)

| # | Tiêu chí | Trạng thái |
|---|---|---|
| 1 | Test T-044 qua local đầu phiên | Đạt (374/374; và sau mỗi sửa) |
| 2 | T1 bất biến; QT5 không còn giá trị vô lý hoặc đã sửa | Bất biến đạt. Vấn đề QT5 chưa sửa; Minh cho tiếp tục theo D17 (Q-b), nên tiêu chí này đạt với ngoại lệ đã duyệt, không phải đạt đầy đủ. Chi tiết: cờ QT5 "nhóm metric chiếm gần hết" đi cùng cổng qua giả nhiều hơn α; ứng viên nguyên nhân (giả định độc lập gặp dữ liệu tự tương quan, trôi nền, cỡ mẫu; quy tắc `verdict` không xét số phép chấm) chưa phân xử; chưa sửa; Minh hoãn theo D17 (Q-b) |
| 3 | D17 quyết và ghi LOG trước T4b | Đạt (LOG "D17 đã quyết") |
| 4 | Khối K đủ 16 × 52; hash pha 1 ghi trước pha 2 | Đạt (LOG 01:29) |
| 5 | Luật chọn khối bước 1–8 và 10, có vết | Đạt (`khoi-k.json#/chon_khoi`, `#/buoc8`) |
| 6 | Phép độ bền, Đ5, D1–D5; D1, D2 khớp hoặc xử lý | Đạt. Lệch D1 lúc đầu chỉ được giải thích ở LOG và `doi-chieu-ks16*.json`; ở phiên 2 (tiếp) đã ghi qua đính chính (`dinh-chinh-cai-dat.md` mục D1, phân loại không phải lỗi cài đặt) |
| 7 | Mọi lần nhìn số dev được ghi | Đạt sau bổ sung: phiên 1 thiếu vài lần xem (status, hash; lượt đo giờ phép độ bền), đã nối muộn ở phiên 2 (tiếp), ghi rõ là ghi muộn; một số mốc giờ ước sai, đã đính chính trong sổ |
| 8 | Báo cáo tách kết cục, quan sát, chưa phân xử, quyết định task (2) | Đạt (mục 1, 6, 9) |

## 11. Các lượt chạy (giữ cả lượt hỏng)

- Bước 0: `b0-kiem-hash-001`, `b0-test-t044-001`.
- Bước 1: `b1-r0-thu-001` (hỏng, ĐC1); `b1-r0-thu-002-nezha`; `b1-kiem-ghep-nezha-001`; `b1-r0-re2-003` (sau sửa).
- T1 Nezha-OB: `b2-t1-nezha-*`. D3, D4, D1 Nezha-OB: `b2b-d3-*-nezha-001`, `b2-d1-kE1E2-nezha-001`.
- Sửa ĐC: `sua-dc-001`. Thử bộ điều phối: `thu-ss-001`, `thu-ss-002` (hỏng, lỗi cú pháp của script), `thu-ss-003`–`thu-ss-007`, `thu-toc-do-001`.
- Đợt `d17-001` (v1, chết lúc 18:21 khi console bị đóng; 17 đơn vị OK được dùng lại); `d17-002`; `d45-001`.
- Pha 2: `pha2-thu-nhan-gia-001` (thử code bằng nhãn giả, không đọc nhãn); `do-ben-do-gio-001` (đo giờ, seed 1).
- Chẩn đoán ngoài repo (scratchpad của phiên; không là kết quả): bản sao `src/` vá ĐC1–ĐC3 trước khi Minh duyệt.
- Phiên 2 (sau phản biện lượt 1; chỉ đọc bản ghi đã băm, không chạy lại chuỗi): `co-che-bo-sung-001` (A1, A5, A7; chạy hai lần, lần 1 giữ ở `co-che-bo-sung-lan-1.json`, khóa cũ trùng lần 2); `a8-mau-e3-001` (A8 theo luật khai trước), `a8-mau-e3-002` (thêm hai mô tả sau khi xem lượt 001: tách root, đếm dòng khung ngăn xếp). Lượt thử trong scratchpad (không là kết quả): một lượt `co_che_bo_sung.py`, một lượt A8 trên 2 ca, và các script kiểm R1, R3(d), B7, C1.

## 12. Lệnh dựng lại

```
source results/T-045/scripts/moi_truong.sh
pythonw.exe -B results/T-045/scripts/chay_song_song.py --dot <đợt> --bo d17|d45 --so 4   # pha 1, không nhãn
bash results/T-045/scripts/theo_doi.sh <đợt> 60 15                                       # theo dõi
$PY -B results/T-045/scripts/kiem_dot.py --dot <đợt>
$PY -B results/T-045/scripts/tach_cau_hinh.py results/T-045/runs/<lượt nhiều cấu hình>
$PY -B results/T-045/scripts/t1_tong_hop.py …; d1_doi_chieu_ks16.py …; d3_e3_khong_nhan.py …; d4_e1_cp.py …; d5_tinh_lai.py …
$PY -B results/T-045/scripts/d2_baseline.py --ra results/T-045/tai-lap-baseline.json
$PY -B results/T-045/scripts/pha2_khoi_k.py --ra results/T-045/khoi-k.json
$PY -B results/T-045/scripts/bo_sung_khoi_k.py results/T-045/khoi-k.json
$PY -B results/T-045/scripts/co_che_khoi_k.py --ra results/T-045/co-che-khoi-k.json
$PY -B results/T-045/scripts/t4_bao_cao.py --ra-t4 results/T-045/t4.json --ra-t4b results/T-045/t4b.json
$PY -B results/T-045/scripts/theo_loai_loi.py --thang E1+E2 --ra results/T-045/theo-loai-loi.json
$PY -B results/T-045/scripts/do_ben.py --kq results/T-045/khoi-k --seed 20261101 --n 1000 --ra results/T-045/do-ben.json
$PY -B results/T-045/scripts/co_che_bo_sung.py --ra results/T-045/co-che-bo-sung.json              # phiên 2: A1, A5, A7
$PY -B results/T-045/scripts/kiem_mau_e3.py --luot results/T-045/runs/a8-mau-e3-002 --ra results/T-045/e3-noi-dung-mau.json   # phiên 2: A8
$PY -B results/T-045/scripts/tao_manifest.py [--kiem]
```
Lệnh đầy đủ của từng lượt nằm trong `tham-so.json` hoặc `nguon.json` của lượt, docstring từng script và LOG.
