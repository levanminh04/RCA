# T-046 — Cổng kiểm định, `verdict` và thang điểm của M1 (báo cáo tới điểm dừng D-2, sau sửa phản biện lượt 1)

- **Người làm:** Claude. **Người phản biện:** Codex. **Ngày:** 01/11/2026.
- **SPEC:** `tasks/T-046-cong-verdict-thang-diem/SPEC.md`: bản 2, sửa S1–S10, A1–A7, bản 3 (B1–B6), bản 4 (C1–C3). A3 điểm 3 sửa hai lần: 17:52 (R1) và 20:44 (N4).
- **Trạng thái:** đã xong bước 0–10. D-2 đã duyệt (Q-228, WHY-67–69). `src` cài ở 5 commit `5d93d769`–`c298188e`. Codex kiểm lại không có điểm CHẶN mới. Minh nghiệm thu ngày 02/11/2026 (Q-230), đúng phạm vi tới bước 10; không xác nhận cổng đã hiệu chuẩn, hiệu quả RCA hay quyền mở G3 hoặc test.
- **Ràng buộc đã giữ:** không đọc root, loại lỗi, ô; không tính MRR; không mở dữ liệu khóa. Mọi lần nhìn số dev ghi ở `so-lan-nhin.jsonl`.
- **Mọi số là số dev.** Không có phần kiểm độc lập. C-e chồng lấn dữ liệu với A/A và **đã được xem từ 16:02**, trước hai lần khóa lại. Các lượt sau 16:02 đo lại bằng mã đã sửa, không phải dữ liệu kiểm mới.
- **Bản cũ giữ làm lịch sử:** `bao-cao-truoc-phan-bien-1.md`, các tệp không hậu tố và hậu tố `-sua1`. Số dưới đây lấy từ các tệp hậu tố `-sua2`.

## 1. Tóm tắt

### Quan sát

1. **G0 qua giả nhiều ở A/A.** RE2-TT metric 0,300; op_full 0,070; op_excl 0,115. Nezha-OB 0,08–0,10 (`chan-doan-cong-ban3-sua2.json#/qua_cong_aa/<ô>/G0/ty_le`).
2. **Không cổng nào đạt mức (a) ≤ 2α = 0,02 ở mọi ô**, theo qua cổng hay theo cờ (mục 5).
3. **Theo luật minimax bản 4 (đếm p < α): G3, D1.** Ô tệ nhất G3 0,089 (metric RE2-TT), D1 0,039 (mẫu log thường RE2-TT) (`ung-vien-sua2.json#/minimax`).
4. **Không `verdict` nào đạt cả (b) và (c1)** (`ung-vien-sua2.json#/to_hop`):

   | Quy tắc với (G3, D1) | (b) A/A RE2-TT | (b) A/A Nezha-OB | (c1) thật RE2-TT | (c1) thật Nezha-OB |
   |---|---|---|---|---|
   | V0 | 30/30 | 6/22 | 30/30 | 22/22 |
   | V3 | 30/30 | 2/22 | 30/30 | 21/22 |
   | V1 (p đã tinh) | 30/30 | 1/22 | 30/30 | 18/22 |
   | V4, q* = 0,09 | 6/30 | 1/22 | 22/30 | 4/22 |

   q* chọn trên A/A đổi theo các lượt: 0,085; 0,095; 0,09. Các lượt chỉ khác nhau ở biên khối.
5. **Khóa cặp cổng, không khóa `verdict`.** `ung-vien-sua2.json`, sha256 ở LOG (22:17). Cặp cổng không đổi so với hai khóa trước.
6. **Sau khóa, trên C-e (300 + 300 giây, chỉ báo cáo):**
   - G3 qua cổng: metric lên 0,027, xuống 0,026; op_full 0,029 (`kiem-sau-khoa-sua2.json#/a_phay`).
   - K-đủ: op_excl lên 0,023, xuống **0,171**; cạnh 0,006; mẫu log thường (D1) 0,027 (`#/K_du/ce|RE2-TT|qua_cong_theo_o`).
   - Theo loại kênh: cpu 0,063–0,064; socket 0,035–0,040; error 0,023; diskio 0,007–0,018; latency 0,016–0,019; workload 0,013–0,022; mem 0–0,0005 (`#/qua_cong_ce_theo_hau_to`).
   - CAUSE_FOUND: V0 30/30; V3 30/30; V4:0,09 0/30 (R0), 4/30 (K-đủ) (`#/b_phay|*`, `#/K_du`).
   - Đơn vị có cờ ở cửa sổ thật nhiều hơn C-e ở 29/30 cặp cùng ca. Trung vị 59,5 so với 19; theo tỷ lệ 0,124 so với 0,040 (`#/c2`).
7. **Thang điểm:** tỷ lệ kênh phân vị có cờ đạt rA = 1 là RE2-TT 63/1.877 = 0,034; Nezha-OB 52/192 = 0,271 (metric 43/125, op_full 9/67); gộp 115/2.069 = 0,056. Vì vậy (S) mở (`thang-diem-sua2.json#/bao_hoa_R0_that`).
   - T4c với hòa ở khối đầu: Nezha-OB 1 → 0 cửa sổ; RE2-TT 0 → 0.
   - T4c với thứ hạng (không nhãn): đổi khối đầu RE2-TT 3/30, Nezha-OB 4/22; đổi thực thể đầu 3/30, 3/22; cặp thực thể đổi quan hệ 44/10.277, 12/102 (`#/hoa_khoa_tang1`).

### Suy luận và ứng viên (chưa phân xử)

- **Ứng viên cơ chế qua giả ở metric RE2-TT.** Ba ứng viên có quan sát hỗ trợ, không phép nào tách được phần đóng góp:
  - chuỗi giữ giá trị: 82% số giây lặp giá trị giây trước (`cau-truc-metric-re2.json`);
  - động học bền: latency gần bước ngẫu nhiên ở thang 60 giây;
  - trôi khi hệ khỏe: mem chênh giữa hai nửa N.
- **Bỏ giây lặp** giảm G0 từ 0,30 xuống 0,18 (`bo-giu-metric-re2.json`). Vì bỏ giây lặp cũng làm giảm số điểm, phép này không phân biệt tác dụng của bỏ lặp với tác dụng của ít điểm hơn. Phép "bỏ lặp so với lấy mẫu thưa cùng số điểm" không chạy trong T-046 (OPEN). Lý do: phép chỉ thu hẹp giả thuyết, không tách được cơ chế, và không đổi quyết định cổng.
- **AR(1):** phép làm trắng AR(1) đã thử (G4) chưa đưa tỷ lệ qua giả trên dev về mức mục tiêu (0,272). Chưa loại hết giải thích AR(1). Trên dữ liệu tổng hợp, G4 hiệu chuẩn rõ ở φ ≤ 0,5; ở φ = 0,9 thì trượt (cỡ 150: 0,0415, 0,0375).
- **Mem không phải nguồn cờ sai.** Mem qua cổng nhiều ở A/A (G3 0,368; G0 0,793), nhưng phần lớn nằm trong biên ε = 5% nên không thành cờ: với mem hướng lên, 744 phép qua cổng khi rơi G0 chỉ tạo 3 cờ (LOG, N6). Câu cũ "mem trôi gây qua giả" sai về hậu quả.
- **Chênh A/A với C-e.** Ở A/A metric RE2-TT, phép dùng G3 thật qua 0,039 (562/14.347). Phép rơi G0 vì ít khối qua 0,424 (1.063/2.507), cờ 0,061 (`roi-g0-theo-nhom.txt`). C-e 0,026–0,027. Vậy phần lớn chênh theo qua cổng đến từ rơi G0 ở cửa sổ 150 giây. Phần 0,039 so với 0,027 chưa giải thích.
- **`verdict`.** Ở cùng cỡ cửa sổ, tỷ lệ đơn vị có cờ khác nhau rõ giữa thật và C-e (29/30 cặp). Không có dữ liệu cùng cỡ để chọn ngưỡng mà không dùng C-e. Chênh này cũng có thể gồm chênh giữa hai đoạn thời gian khác nhau của ca, không chỉ tác dụng của lỗi.

### Câu hỏi nguồn trả lời tới đâu

- **C1 (vì sao cổng qua giả):** thu hẹp, không phân xử. Metric RE2-TT có ba ứng viên. Trace, đếm chưa rõ. Metric Nezha-OB OPEN.
- **Chọn cổng:** có lựa chọn theo luật đặt sau khi nhìn số (a). Lựa chọn giảm qua giả, chưa đạt mức.
- **`verdict`:** chưa có. V0 không tách được cửa sổ có lỗi.
- **Thang điểm:** (S) mở theo dữ liệu; S1 theo luật khai trước; tốt hay xấu cần nhãn (T-047).

### OPEN

- Nguyên nhân hướng xuống của op_excl RE2-TT (A/A 0,092; C-e 0,171; thật 0,129).
- Phần qua giả còn lại của đơn vị đếm ở thang dài hơn 10 giây.
- Hai ô log_loi, mau_loi RE2-TT: 30 phép mỗi ô, không đo được.
- Hiệu chuẩn metric Nezha-OB: 5 điểm mỗi phía, G3 rơi G0.
- `verdict` cho bản P7.
- G1 so với G3 về độ nhạy trên dữ liệu thật (mục 5).
- Có hiện tượng giữ giá trị ở FlashTicket không: phụ thuộc nhịp cập nhật, cách xuất và tiền xử lý thực tế; chưa kiểm.
- Hiệu chuẩn bằng lịch sử bình thường dài trên FlashTicket.

## 2. Đầu vào, kiểm hash, môi trường

- Hash T-045 PASS 6.085/6.085 (gồm `src/m1` ở `bbef69dd`); dữ liệu dev PASS (RE2-TT 30 ca, Nezha-OB 22 ca) (`runs/b0-kiem-001`).
- Test T-044 374/374, T-045 16/16 (`runs/b0-test-001`). Test T-046: xem `tests/`.
- Môi trường: `source results/T-045/scripts/moi_truong.sh`.
- Bước 0–8 không sửa `src`: ứng viên cài trong `scripts/cong.py`, `scripts/t046.py`. Bước 9 cài vào `src/m1` sau Q-228. Vì vậy `results/T-045/manifest.json --kiem` nay lệch ở `src/m1`; kiểm T-045 phải dùng checkout `bbef69dd`.
- Bản ghi có móc trùng từng byte T-045: cửa sổ thật 52/52; C-e 30/30.

## 3. Rà SPEC (trước bước 0)

Mười hai điểm R1–R12, sửa S1–S10 (LOG mục "Rà và sửa SPEC"). Không nới tiêu chí nào ở lượt rà. Các nới sau đó là bản 4, do Minh giao quyền và ghi ở LOG.

## 4. Bước 2 — dữ liệu tổng hợp

- `runs/b2-tong-hop-001` (A7 đạt): tái lập SPEC T-043, G0 ra 0,011; 0,073; 0,288; 0,386. Ở φ = 0, G1 và G3 hiệu chuẩn. Ở φ = 0,9: G1 0,05–0,07, G3 0,04–0,06. Ở φ = 0,98: 0,09–0,18.
- `runs/b2b-tong-hop-001` (B4 đạt): G4 hiệu chuẩn rõ ở φ ≤ 0,5; ở φ = 0,9 trượt; không xử lý xu hướng (0,63). D1: Poisson gộp cụm 0,13–0,15 (D0) xuống 0,003–0,024.
- Độ nhạy với bước nhảy 0,5σ (cỡ 300): G0 0,98; G1 0,93; G4 0,87; G3 0,61. Bước 0,25σ: G1 0,38; G3 0,18.

## 5. Bước 3–5 — A/A, luật chọn

Qua cổng ở A/A (`chan-doan-cong-ban3-sua2.json#/qua_cong_aa/<ô>/<cổng>/ty_le`), mức (a) = 0,02:

| Ô | G0 | G1 | G3 | G4 |
|---|---|---|---|---|
| RE2-TT metric | 0,300 | 0,135 | 0,089 | 0,272 |
| RE2-TT op_full | 0,070 | 0,025 | 0,020 | 0,020 |
| RE2-TT op_excl | 0,115 | 0,053 | 0,053 | 0,053 |
| RE2-TT canh | 0,020 | 0,012 | 0,005 | 0,005 |
| Nezha-OB op_full | 0,078 | 0,018 | 0,019 | 0,019 |
| Nezha-OB op_excl | 0,096 | 0,019 | 0,016 | 0,016 |
| Nezha-OB canh | 0,079 | 0,022 | 0,022 | 0,022 |

Cờ F_raw ở A/A (`#/qua_cong_aa/<ô>/<cổng>/co_F_raw/ty_le`):

| Ô | G0 | G1 | G3 | G4 |
|---|---|---|---|---|
| RE2-TT metric | 0,127 | 0,047 | 0,042 | 0,111 |
| RE2-TT op_full | 0,054 | 0,023 | 0,019 | 0,019 |
| RE2-TT op_excl | 0,102 | 0,049 | 0,053 | 0,053 |
| RE2-TT canh | 0,017 | 0,012 | 0,005 | 0,005 |
| Nezha-OB op_full | 0,053 | 0,011 | 0,012 | 0,012 |
| Nezha-OB op_excl | 0,075 | 0,016 | 0,013 | 0,013 |
| Nezha-OB canh | 0,067 | 0,017 | 0,017 | 0,017 |

- Đơn vị đếm (`#/don_vi_dem`): mẫu log thường D0 0,066 → D1 0,039 (RE2-TT); D0 0,052 → D1 0,022 (Nezha-OB).
- **Vì sao có hai bảng (N5).** Luật minimax bản 4 đếm p < α. G0, G1 kiểm hạng, nên có thể qua cổng mà chênh không vượt biên ε. G3 kiểm trên chính thống kê vượt ngưỡng nên gần như qua cổng là có cờ. Vì vậy so qua cổng giữa hai nhóm không cùng nghĩa. Đại lượng đi tiếp xuống chuỗi là cờ.
- **G1 so với G3 theo cờ:**
  - So theo cặp trên cùng phép, bootstrap theo ca (`so-cap-g1-g3.json`). Ô tệ nhất: G1 0,0489; G3 0,0526; hiệu −0,0036, khoảng 95% [−0,0125; 0,0078]. Metric RE2-TT: G3 ít cờ hơn, hiệu +0,0051, khoảng [0,0017; 0,0085]; theo ca G1 ít cờ hơn 10, nhiều hơn 19, bằng 1. Bản trước suy từ hai khoảng Wilson chồng lấn là sai cách (Codex).
  - Trung vị đơn vị có cờ, G1 và G3: A/A RE2-TT 31 và 26; thật RE2-TT 67 và 59,5; C-e 19,5 và 19; thật Nezha-OB 7 và 6 (`so-g1-g3.txt`).
  - G1 nhạy hơn trên dữ liệu tổng hợp (mục 4), không dùng Monte Carlo, chạy nhanh hơn. G3 khớp thống kê của E4 (rA − rN), đi qua cùng biên ε.
  - **Kết luận:** số dev ở A/A không cho căn cứ chọn G1 theo cờ. Độ nhạy trên dữ liệu thật chưa so. Giữ G3 là lựa chọn thực dụng giữ kết quả luật cũ, không phải kết quả của một luật đúng đại lượng (WHY-67, Q-228).

## 6. Khóa và kiểm sau khóa

- Các khóa: `ung-vien.json` (15:49), `ung-vien-sua1.json` (19:20), `ung-vien-sua2.json` (22:17). Hash ở LOG. Cùng cặp (G3, D1), `verdict` null.
- Chạy sau khóa: `runs/b6-sau-khoa-sua2-001` (`ce`, `r0`, `kdu`). Số ở mục 1, ý 6–7.
- K-đủ, V4:0,09: A/A RE2-TT 3/30, Nezha-OB 2/22; thật RE2-TT 12/30, Nezha-OB 0/22; C-e 4/30. V0 khớp chuỗi ở mọi cửa sổ. Bão hòa K-đủ ở cửa sổ thật: Nezha-OB metric 27/49.
- **Điểm người làm tự tìm và sửa:** N4 (bản sửa R1 làm b = 60 rơi G0 vì bao bản ghi H ngắn hơn 300 giây vài mili giây; lượt `-sua1` có lỗi này, giữ làm lịch sử). Xem LOG.

## 7. Đề xuất ở D-2

Đã duyệt và ghi: `docs/WHY.md` WHY-67–69, `docs/DECISIONS.md` Q-225–Q-228. Kế hoạch cài: LOG, mục "D-2 sửa lại" và phiên 1 (tiếp 4).

Phần M: `danh-muc-metric.md`, `danh-muc-metric-m3-sua2.json`. M1, M2 xong. M3 phần không nhãn xong; độ phủ theo thành phần gốc và tác dụng lên RCA chưa kiểm. Danh mục là ứng viên, không thay WHY-59. M4–M5 hoãn.

## 8. Tiêu chí xong (SPEC)

| # | Tiêu chí | Trạng thái |
|---|---|---|
| 1 | Test T-044, T-045 qua ở đầu phiên và sau mỗi commit `src` | Đạt: 374 và 16 passed sau mỗi commit |
| 2 | C1 theo loại đơn vị và nguồn: phân xử hoặc "chưa phân xử" kèm bằng chứng còn thiếu; metric Nezha-OB OPEN | Đạt theo nhánh "chưa phân xử". C1 mới được thu hẹp |
| 3 | Khóa trước C-e có hash; kiểm sau khóa đã báo; hoặc xung đột trình Minh | Đạt một phần: khóa đầu có hash trước C-e; hai khóa lại sau khi C-e đã xem; `verdict` không chọn được |
| 4 | Thang điểm quyết theo (S) | (S) mở; S1; đổi D24 đã duyệt (Q-228) |
| 5 | WHY duyệt trước khi cài; chế độ cũ không đổi hành vi | Đạt: Q-228 trước khi cài; sha256 bản ghi mặc định trùng ở 52 ca × 3 cửa sổ (`kiem-src-mac-dinh.json`) |
| 6 | Bước 10 tái lập số | Đạt: 77.755 phép phân vị, 8.248 phép đếm, 0 lệch; số sau khóa 0 lệch; bất biến seed và xáo hàng đạt (`kiem-src.json`). Chỉ nói `src` tính đúng như bản đo |
| 7 | Không đọc root, không tính MRR, mọi lần nhìn số đã ghi | Đạt; hai dòng đầu của sổ nhìn số chỉ có giờ trong khoảng |

## 9. Lượt chạy (giữ mọi lượt)

- `b0-kiem-001`, `b0-test-001`, `b1-thu-C-001`, `b1-kiem-001`, `b2-tong-hop-001`, `b2b-tong-hop-001`.
- `b3-thu-001`, `b3-aa-001`, `b3b-thu-001`, `b3b-aa-001`, `b5r-tinh-001`, `b6-sau-khoa-001` (có một lượt r0 dừng lúc 16:04, trước khi có ca nào).
- Sau R1: `b3-sua-thu-001`, `b3-sua-aa-001`, `b5r-tinh-sua1-001`, `b6-sau-khoa-sua1-001`.
- Sau N4: `b3-sua2-thu-001`, `b3-sua2-aa-001`, `b5r-tinh-sua2-001`, `b6-sau-khoa-sua2-001`.
- Bước 10: `b10-thu-001` (có lần đầu lỗi lời gọi `soi`, giữ trong `progress.jsonl`), `b10-kiem-src-001`.

## 10. Lệnh dựng lại (bản số cuối)

```
source results/T-045/scripts/moi_truong.sh; export PYTHONHASHSEED=0
S=results/T-046/scripts; R=results/T-046
(cd $R/tests && $PY -B -m pytest -q -p no:cacheprovider)
$PY -B $S/b3_chay.py --luot $R/runs/<lượt b3> --so 4
$PY -B $S/b3b_tong_hop.py --cu $R/runs/<lượt b3> --moi $R/runs/b3b-aa-001 --ra <chẩn đoán>
$PY -B $S/b5c_danh_gia.py --cu $R/runs/<lượt b3> --moi $R/runs/b3b-aa-001 --chan-doan <chẩn đoán> --ra-danh-gia <lượt 1> --ra-khoa <tệp không dùng>
$PY -B $S/b5r_tinh_G3.py --cu $R/runs/<lượt b3> --moi $R/runs/b3b-aa-001 --luot $R/runs/<lượt tinh> --so 4
$PY -B $S/b5c_danh_gia.py … --g3-tinh $R/runs/<lượt tinh>/ca --ra-danh-gia <lượt 2> --ra-khoa <tệp không dùng>
$PY -B $S/b5d_khoa_cong.py --danh-gia <lượt 2> --chan-doan <chẩn đoán> --ra <tệp khóa>
$PY -B $S/b6_sau_khoa.py --ung-vien <tệp khóa> --sha256 <hash> --phan ce|r0|kdu --luot $R/runs/<lượt sau khóa> --so 4
$PY -B $S/b6_tong_hop.py --ung-vien <tệp khóa> --cu $R/runs/<lượt b3> --moi $R/runs/b3b-aa-001 --luot $R/runs/<lượt sau khóa> --ra-kiem <tệp> --ra-thang <tệp>
$PY -B $S/n5_so_g1_g3.py > $R/so-g1-g3.txt; $PY -B $S/n5_roi_g0.py > $R/roi-g0-theo-nhom.txt
$PY -B $S/tao_manifest.py [--kiem]
```

Tên tệp của bản cuối: hậu tố `-sua2`. Lệnh từng lượt nằm trong `tham-so.json` của lượt.
