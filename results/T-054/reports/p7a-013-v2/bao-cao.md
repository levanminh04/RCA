# Báo cáo P7(a) — main013-v2: kết quả, đối chứng và phân tích nhóm giúp/hại

T-054. Người làm phần chạy/chấm/báo cáo: Claude. Người phản biện: Codex. Ngày lập: 08/11/2026.
Trạng thái: **chờ phản biện**. Báo cáo không duyệt G4, không mở RE3, không chọn lại thiết kế.

Ký hiệu nguồn (đường dẫn tính từ `results/T-054/`):

- **A** = `reports/main-013-v2/a4.json` (sha256 dca9610d…, khớp `runs/chuan-bi-main-013-v2/received-main-002/report-receipt.json#/A4`).
- **T** = `reports/main-013-v2/tables.json` (sha256 5e886646…, khớp `report-receipt.json#/tables`).
- **PT** = `reports/p7a-013-v2/phan-tich-nhom.json`, sinh bởi `reports/p7a-013-v2/phan_tich.py` (chỉ đọc A, T và `result.json` của vế M1-family; hash ở manifest cùng thư mục).

Số trong báo cáo lấy từ ba file trên. Con trỏ JSON có dấu `|` trong khóa là đúng tên khóa.

---

## 0. Tóm tắt theo ba mức

**Đã chạy xong gì.** Snapshot 1640 slot đã đăng ký (`runs/chuan-bi-main-013-v2/received-main-002/verified-before-labels.json#/slots`): 898 VERIFIED trên hai EC2 (EC2_1 448, EC2_2 450 theo LOG), 568 VERIFIED trên laptop (562 non-A, 6 TORAI A), 174 TORAI A BLOCKED (173 A_QUEUE_HALTED_BEFORE_DISPATCH, 1 lỗi kiểm danh tính tiến trình). Minh tạm dừng A. Seal đạt trước ghép nhãn.

**Đủ bảng hợp lệ gì.** Đủ A4 (60 TT, 34 OB, ba seed TORAI B) và mọi bảng mô tả của ma trận chính. Thiếu bảng phụ TORAI A: 174 slot BLOCKED và 2 ca thiếu seed (`T#/missing`).

**Câu hỏi MRP trả lời tới đâu.**

- RQ3b, TT: M1 **đạt E-04 theo công thức** so với TORAI B; CI chứa 0 nên **chưa phân biệt hơn/kém**.
- RQ3b, OB: Hit@5 M1−M4 dương nhưng **không đạt** mức 0,05. Với 3 ô hữu hiệu, p nhỏ nhất có thể là 1/8, nên phép này không thể bác bỏ ở 0,05 trên dữ liệu này.
- RQ3d, TT: không có bằng chứng việc dùng quan hệ thêm gì. M1 bằng nhánh bỏ quan hệ C-a0 về MRR (2 thắng/2 thua).
- RQ3d, OB: M1 hơn C-a0 về mô tả. Phần hơn đến từ cách dựng bằng chứng có dùng quan hệ cha–con của span: E2 ở lỗi network_delay, E1 ở lỗi CPU. Bước xếp hạng trên đồ thị (E5) không đổi kết quả nào. M1 không hơn quy tắc đơn giản C-d2 (khởi phát sớm nhất), dù C-d2 dùng cùng kênh. Theo bảng diễn giải đã khóa: giới hạn theo cặp, không khẳng định lợi ích quan hệ chung.
- RQ3a (P/R/F1 phát hiện) chưa trả lời (Q-245). RQ3c chỉ có vùng nghi ngờ, không có nhãn vùng.

---

## 1. Toàn vẹn nguồn và tiếp xúc test

Kiểm trước khi dùng số, phiên 08/11/2026:

| Kiểm | Kết quả |
|---|---|
| `runs/chuan-bi-main-013-v2/verify_manifest.py --documents` | PASS, 515 mục, 0 lệch |
| sha256 manifest v2 / grant v2 | a0fb1f5c… / 2f73e52d…, khớp LOG |
| A, T, snapshot so với `report-receipt.json` | khớp sha256 và số byte |
| `result.json` của 716 slot M1-family (gồm 58 C-e) so với `verified.json` cùng attempt | khớp hết (`PT#/verified_results_checked`) |
| Hạng root tính lại từ khối `worlds/P/blocks` so với RR trong T | 658/658 khớp (`PT#/rr_blocks_vs_table`) |
| `exposure.jsonl` LABEL_JOIN 2026-11-07T19:03:51Z | `snapshot_sha256` = fingerprint của `verified-before-labels.json` (tính lại bằng `cham.fingerprint`, 0fbf5b45…) |
| Chạy `phan_tich.py` hai lần | cùng sha256 (tất định) |

Tiếp xúc test trong phiên này: đọc trung gian M1-family của 94 ca sau khi ghép nhãn, để phân tích báo cáo. **Đã xem, chưa dùng để thiết kế bản khóa.** Nếu sau này dùng các quan sát ở §7 để sửa thiết kế, bản sửa phải khai C-15 B và báo riêng.

---

## 2. Khai báo về lượt chạy

1. **v1 → v2 là bản sửa sau khi mở test, theo C-15 B.** v1 dừng ở lỗi phương pháp chưa phân loại: TraceRCA và MicroRank TT gặp operation chỉ có 1 span bình thường. v2 thêm quy tắc INSUFFICIENT_NORMAL_SPANS (kiểm lại từ đầu vào thật) và cho supervisor chạy tiếp slot độc lập. Sửa trước khi xem điểm hay nhãn. Minh duyệt tính các slot này là trượt (`runs/chuan-bi-main-013-v2/grants/minh-v2.txt`). Code chỉ đổi `scripts/bien_nhan.py` và `scripts/dieu_phoi.py`; slot, cấu hình, seed, nguồn và cửa sổ giữ nguyên.
2. **So v1↔v2:** 740 slot trùng, 740 giống hệt, 0 khác (`runs/chuan-bi-main-013-v2/execution-receipts/v1-v2-compare.json#/total_same`, `#/total_diff`). So trên các trường status, ranking, entity_ranking, sets, error, extra và ranking_native.
3. **Wrapper import khi nhận/chấm.** Lượt nhận 001 dừng ở import, trước khi đọc dữ liệu hay nhãn: `cham` bị lấy nhầm từ `results/T-048/scripts`. Lượt 002 gọi đúng `receive_main.py` v2 qua `execution-receipts/run_receive.py`. Wrapper này nạp trước module T-054 rồi chạy bằng runpy. Mọi module repo thực nạp đều nằm trong code-pins, trừ chính wrapper (`execution-receipts/receive-002-modules.json#/not_in_code_pins`).
4. **Laptop ngủ 00:35:18–00:41:02 (+07)** do hết pin. Máy không khởi động lại. Lúc đó chỉ một job đang chạy: TORAI A `test-cda8dfc162` seed 1, với monitor gap 342,3 s. Mọi job non-A đã VERIFIED trước đó; EC2 chạy độc lập. Nguồn: LOG mục "Laptop ngủ do hết pin". Ca này là ca TORAI A duy nhất đủ ba seed (`T#/rows`, arm=torai_A). Nếu bảng A được dùng, phải khai khoảng mất quan sát này.
5. **TORAI A tạm dừng.** Slot `torai_A test-2a0c838e6b seed 2` BLOCKED ở bước kiểm danh tính tiến trình. Theo policy A, hàng A dừng. Minh: "tạm dừng A. sau khi xong hết thì tính tiếp nếu thấy cần thiết". Bảng phụ A thiếu (`T#/missing`: 174 BLOCKED_NO_VERIFIED_RESULT, 2 INCOMPLETE_THREE_SEEDS). A nằm ngoài A4, nên không ảnh hưởng A4.
6. **D3.** AC sleep giữ 0 trong lượt main, khôi phục 2700 s sau khi chấm (`received-main-002/power-restored.json`). Hết pin vẫn kích hoạt ngủ, như mục 4.
7. **D1, giới hạn độc lập của OB.** Adapter OB đã được sửa sau khi đọc cấu trúc thời gian của cohort OB (lần đọc 006). OB có TX1 34/34, và cả 34 ca từng được dò triệu chứng (`runs/chuan-bi-main-013-v2/activated-001/protocol.json#/exposure`). Kết quả OB không là phép kiểm độc lập hoàn toàn. D4 chưa tách được tác động của adapter khỏi độ khó ca (§3.2).

---

## 3. A4 / E-04

### 3.1 TT — MRR M1 − TORAI B, 60 ca, world P

| Đại lượng | Giá trị | Nguồn |
|---|---|---|
| ΔMRR | 317/7200 ≈ 0,0440 | `A#/TT/P/delta` |
| CI bootstrap cặp theo ô (10.000 mẫu, seed 20261005) | [−0,033333333333; 0,148750000000] | `A#/TT/P/E04/lo_12`, `hi_12` |
| E-04 (lo > −0,05, strict) | đạt theo công thức; CI không suy biến | `A#/TT/P/E04/pass_formula`, `degenerate` |
| Thắng/hòa/thua theo ca | 7/50/3 | `A#/TT/P/counts` |
| Ô tổng khác 0 / ô M1 thua / ca cả hai trượt | 6 / 2 / 0 (trên 20 ô) | `A#/TT/P/counts` |
| Bản loại lỗi | không loại ca nào, n = 60 | `A#/TT/P/error_excluded/excluded` |
| Hoán vị ca (độ nhạy) | p = 1906/10001 | `A#/TT/P/case_permutation/p` |
| Đảo dấu theo ô tại 0 (độ nhạy) | p = 1/4, 6 ô hữu hiệu | `A#/TT/P/cell_sign_at_zero` |
| McNemar chắc hạng 1 (phụ): đa số / cả ba seed | M1-only 6, TORAI-only 3, p = 65/128 / M1-only 7, TORAI-only 3, p = 11/32 | `A#/TT/P/McNemar_majority`, `McNemar_all` |
| S_lo, S_hi | trùng P ở delta, CI và đếm | `A#/TT/S_lo`, `A#/TT/S_hi` |

**Câu đọc theo bảng diễn giải đã khóa** (`protocol.json#/interpretation`): "đạt E-04 theo công thức; 6 ô tổng khác 0, 2 ô M1 thua, 0 ca cả hai trượt". CI chứa 0, nên "chưa phân biệt hơn/kém; đọc E-04 riêng theo cận dưới". CI là danh nghĩa. Với 20 ô, trong đó chỉ 6 ô khác 0, bootstrap có thể undercoverage (`A#/TT/P/E04/caveat`). WHY-06 ghi power của câu (1) khoảng 0,19 theo giả định khai trước. Kết quả đạt không chứng minh M1 không thua quá 0,05 ngoài giả định ấy.

### 3.2 OB — Hit@5 kỳ vọng M1 − SimpleRCA M4, 34 ca, world P

| Đại lượng | Giá trị | Nguồn |
|---|---|---|
| ΔHit@5 | 3/34 ≈ 0,088 | `A#/OB/P/delta` |
| Thắng/hòa/thua | 3/31/0; 3 ô hữu hiệu trên 20 | `A#/OB/P/counts` |
| Đảo dấu nguyên ô một phía tại 0 | p = 1/8 | `A#/OB/P/cell_sign_at_zero/p_exact` |
| Mức chuyển từ TT (E-04 tại P qua, lo < hi) | 1/20 | `A#/OB/P/alpha_from_TT_P` |
| Đạt | không | `A#/OB/P/pass_formula` |
| CI bootstrap (mô tả) | [0; 0,1935] | `A#/OB/P/CI` |
| D4: all34 / remaining30 / affected4 | 3/34 / 1/10 / 0 | `A#/OB_group_description/rows` |

**Câu đọc theo bảng khóa:** "Chưa phân xử; báo cỡ chênh/CI, ô hữu hiệu và giới hạn M4." p = 1/8 là p nhỏ nhất có thể với 3 ô hữu hiệu (2⁻³), vì đảo dấu ô có tổng 0 không đổi thống kê. Nghĩa là dữ liệu OB không đủ sức phân xử Hit@5 ở mức 0,05. Ngoài ra Hit@5 của M1 bằng 1 ở cả 34 ca (`PT#/bang_theo_ve_P/Nezha-OB|M1/Hit5_Q`) nên độ đo đã chạm trần. Giới hạn tái lập M4 theo Q-192 giữ nguyên. Bốn ca bị ảnh hưởng bởi sửa adapter (D1) có Δ = 0, nên ΔHit@5 dương đến từ 30 ca còn lại. D4 chỉ là mô tả.

---

## 4. Bảng chính theo vế, world P

MRR lấy từ `PT#/bang_theo_ve_P/<dataset>|<vế>/MRR`. Các độ đo khác lấy cùng nút. Hit@5 là kỳ vọng hòa (`Hit5_Q`).

**RE2-TT, 60 ca**

| Vế | MRR | Hit@1 | Hit@3 | Hit@5 | NDCG@5 | Trạng thái |
|---|---:|---:|---:|---:|---:|---|
| M1 | 0,975 | 0,950 | 1,000 | 1,000 | 0,982 | OK 60 |
| TORAI B (ba seed, gộp trong ca) | 0,931 | 0,894 | 0,950 | 0,983 | 0,942 | OK 180 |
| SimpleRCA (M4) | 0,876 | 0,800 | 0,950 | 0,983 | 0,902 | OK 60 |
| TraceRCA | 0,850 | 0,783 | 0,917 | 0,917 | 0,867 | OK 55, ERROR 5 |
| BARO | 0,806 | 0,733 | 0,867 | 0,867 | 0,811 | OK 60 |
| CIRCA (RHT+DA) | 0,673 | 0,567 | 0,667 | 0,867 | 0,709 | OK 60 |
| CIRCA RHT, phụ | 0,629 | 0,400 | 0,850 | 0,867 | 0,680 | OK 60 |
| MicroRank | 0,296 | 0,100 | 0,483 | 0,483 | 0,311 | OK 55, ERROR 5 |
| C-a0 (bỏ E1/E2/E5/E7) | 0,975 | 0,950 | 1,000 | 1,000 | 0,982 | OK 60 |
| C-a1 (còn E1) | 0,967 | 0,933 | 1,000 | 1,000 | 0,975 | OK 60 |
| bỏ E1 / bỏ E2 / bỏ E5 | 0,882 / 0,975 / 0,967 | — | — | — | — | OK 60 |
| C-d1 (sâu nhất) | 0,655 | 0,633 | 0,633 | 0,633 | 0,633 | OK 60 |
| C-d2 (khởi phát sớm nhất) | 0,964 | 0,933 | 1,000 | 1,000 | 0,973 | OK 60 |
| C-d3 (đường tới đích) | 0,050 | 0,050 | 0,050 | 0,050 | 0,050 | OK 13, UNSUPPORTED_CYCLIC 46, NO_EVIDENCE 1 |
| C-c (RRF ba baseline) | 0,944 | 0,900 | 0,983 | 0,983 | 0,953 | OK 60 |
| C-g (SimpleRCA + E6b) | 0,778 | 0,683 | 0,817 | 0,917 | 0,804 | OK 60 |
| T12-on | 0,975 | 0,950 | 1,000 | 1,000 | 0,982 | OK 60 |

**Nezha-OB, 34 ca**

| Vế | MRR | Hit@1 | Hit@3 | Hit@5 | NDCG@5 | Trạng thái |
|---|---:|---:|---:|---:|---:|---|
| M1 | 0,875 | 0,794 | 0,912 | 1,000 | 0,906 | OK 34 |
| SimpleRCA (M4) | 0,689 | 0,529 | 0,765 | 0,912 | 0,735 | OK 34 |
| BARO | 0,534 | 0,324 | 0,706 | 0,765 | 0,570 | OK 34 |
| TraceRCA | 0,493 | 0,265 | 0,618 | 0,765 | 0,539 | OK 34 |
| MicroRank | 0,392 | 0,206 | 0,353 | 0,706 | 0,439 | OK 34 |
| CIRCA, TORAI B | — | — | — | — | — | UNSUPPORTED 34 mỗi vế (thiết kế) |
| C-a0 | 0,711 | 0,559 | 0,853 | 0,905 | 0,751 | OK 34 |
| C-a1 | 0,760 | 0,647 | 0,866 | 0,925 | 0,794 | OK 34 |
| bỏ E1 / bỏ E2 / bỏ E5 | 0,745 / 0,760 / 0,875 | — | — | — | — | OK 34 |
| C-d1 | 0,716 | 0,618 | 0,706 | 0,824 | 0,721 | OK 34 |
| C-d2 | 0,877 | 0,794 | 0,941 | 1,000 | 0,908 | OK 34 |
| C-c | 0,643 | 0,471 | 0,794 | 0,794 | 0,663 | OK 34 |
| C-g | 0,645 | 0,529 | 0,721 | 0,794 | 0,659 | OK 34 |
| T12-on | 0,875 | 0,794 | 0,912 | 1,000 | 0,906 | OK 34 |

**Trạng thái lỗi/hỗ trợ.** 10 ERROR ở TT gồm TraceRCA và MicroRank trên cùng 5 ca: `test-0e0bdcd10b`, `test-541642b59e`, `test-5e8f996191`, `test-cda8dfc162`, `test-f9d046a28e`. Mỗi lỗi có biên nhận `method-failure.json` và được phân loại theo quy tắc khóa: operation mới hoặc dưới 2 span bình thường. Các slot này tính trượt trong bảng chính. Bản loại lỗi của A4 không loại ca nào, vì hai vế A4 không có lỗi. CIRCA và TORAI B UNSUPPORTED trên OB theo thiết kế; không import và không chạy lõi. C-d3 TT: 46/60 UNSUPPORTED_CYCLIC, vì đồ thị con bất thường có chu trình nên phép đường dài nhất không xác định. Các ca này giữ ở mẫu số với RR 0.

---

## 5. Đối chứng theo cặp, MRR, world P

Δ = vế trái − vế phải. Thắng/hòa/thua theo ca. CI là bootstrap cặp theo ô, chỉ để mô tả (`PT#/so_cap/<khóa>/CI_bootstrap_cell`). Khóa ghi trong bảng.

| Khóa `so_cap` | Δ MRR | T/H/T | Ô ≠0 / ô âm | CI rr |
|---|---:|---|---|---|
| `RE2-TT\|M1-torai_B\|RR` | +0,044 | 7/50/3 | 6/2 | [−0,033; 0,149] |
| `RE2-TT\|M1-C-a0\|RR` | 0 | 2/56/2 | 3/2 | [−0,033; 0,042] |
| `RE2-TT\|C-a0-torai_B\|RR` | +0,044 | 7/50/3 | 6/2 | [−0,033; 0,149] |
| `RE2-TT\|M1-C-a1\|RR` | +0,008 | 1/59/0 | 1/0 | [0; 0,025] |
| `RE2-TT\|C-a1-C-a0\|RR` | −0,008 | 1/57/2 | 3/2 | [−0,033; 0,017] |
| `RE2-TT\|M1-bo-E1\|RR` | +0,093 | 10/50/0 | 7/0 | [0,031; 0,169] |
| `RE2-TT\|M1-bo-E2\|RR` | 0 | 0/60/0 | 0 | [0; 0] |
| `RE2-TT\|M1-bo-E5\|RR` | +0,008 | 1/59/0 | 1/0 | [0; 0,025] |
| `RE2-TT\|M1-C-d2\|RR` | +0,011 | 1/59/0 | 1/0 | [0; 0,033] |
| `RE2-TT\|M1-C-d1\|RR` | +0,320 | 22/38/0 | 8/0 | [0,149; 0,505] |
| `RE2-TT\|M1-C-c\|RR` | +0,031 | 5/53/2 | 4/1 | [−0,008; 0,088] |
| `RE2-TT\|M1-C-g\|RR` | +0,197 | 18/41/1 | 10/1 | [0,082; 0,324] |
| `RE2-TT\|M1-T12-on\|RR` | 0 | 0/60/0 | 0 | [0; 0] |
| `Nezha-OB\|M1-simplerca\|RR` | +0,186 | 16/12/6 | 14/3 | [0,011; 0,364] |
| `Nezha-OB\|M1-C-a0\|RR` | +0,164 | 11/20/3 | 12/3 | [0,054; 0,282] |
| `Nezha-OB\|C-a0-simplerca\|RR` | +0,021 | 12/12/10 | 15/7 | [−0,132; 0,175] |
| `Nezha-OB\|C-a1-C-a0\|RR` | +0,049 | 10/21/3 | 13/3 | [−0,013; 0,115] |
| `Nezha-OB\|M1-bo-E1\|RR` | +0,130 | 8/25/1 | 7/1 | [0,030; 0,256] |
| `Nezha-OB\|M1-bo-E2\|RR` | +0,115 | 7/25/2 | 7/2 | [0,026; 0,220] |
| `Nezha-OB\|M1-bo-E5\|RR` | 0 | 0/34/0 | 0 | [0; 0] |
| `Nezha-OB\|M1-C-d2\|RR` | −0,0025 | 1/31/2 | 3/2 | [−0,043; 0,040] |
| `Nezha-OB\|M1-C-d1\|RR` | +0,159 | 8/26/0 | 5/0 | [0,032; 0,313] |
| `Nezha-OB\|M1-C-c\|RR` | +0,232 | 16/15/3 | 13/2 | [0,048; 0,406] |
| `Nezha-OB\|M1-C-g\|RR` | +0,230 | 16/16/2 | 12/1 | [0,086; 0,384] |
| `Nezha-OB\|M1-T12-on\|RR` | 0 | 0/34/0 | 0 | [0; 0] |

**Thông tin cấu trúc còn giữ ở từng đối chứng** (luật 18, WHY-07):

- C-a0 bỏ E1, E2, E5, E7 nhưng vẫn giữ kênh trace theo operation (thời lượng toàn phần), metric, log và xếp tầng E6a trên kênh. Nó không dùng cạnh trong phép tính hạng (`src/m1/chuoi.py:37`).
- C-a1 còn E1. E1 dùng quan hệ cha–con của span để trừ thời gian span con.
- C-d2 dùng **đúng các kênh của M1**, gồm E1 và E2, nhưng sắp theo khởi phát sớm nhất thay cho E5/E6a (`src/m1/doi_chung.py:64`). So M1 với C-d2 chỉ nói về bước xếp hạng, không nói về việc dùng quan hệ khi dựng kênh.
- C-d1 dùng cạnh để chọn thực thể có cờ mà không bên được gọi nào có cờ (sâu nhất).
- C-g thêm PageRank E6b vào SimpleRCA.
- T12-on thêm cạnh tĩnh từ snapshot: TT +126 cạnh ở 54 ca và +155 ở 6 ca; OB +9 cạnh ở 34 ca (`PT#/trung_gian_theo_ca/*/T12-on/n_edges_observed`, so với M1). Hạng không đổi ở 94/94 ca (`PT#/doi_top_khi_bo`).

---

## 6. Tách theo loại lỗi và vị trí N

MRR theo nhóm (`PT#/tach_MRR`). Số ca mỗi nhóm nhỏ; một nhóm không là mẫu hình (QT15).

**TT theo loại lỗi:** M1 thắng/thua TORAI B: cpu 0/0, delay 1/1, disk 0/0, loss 3/0, mem 0/0, socket 3/2. Ở loss, TORAI B có MRR 0,725 còn M1, C-a0 và C-d2 đều 1,0. Ở delay, C-d2 0,870 thấp hơn M1 0,944.

**TT theo vị trí N (p75):** bậc 0 có 13 ca. M1 thắng TORAI B 5/0 (M1 1,0, TORAI B 0,733); C-a0 và C-d2 cũng 1,0. Hub có 21 ca: M1 0,952, TORAI B 0,976, M1 thắng/thua 1/2.

**OB theo loại lỗi:** network_delay có 10 ca: M1 0,900, C-a0 0,408, M4 0,380, C-d2 0,950. Exception có 4 ca: M1 0,688, M4 0,938, M1 thắng/thua 0/2.

**OB theo vị trí N:** nguồn có 6 ca, đều là frontend: M1 0,708, M4 0,958, M1 thắng/thua 0/3. Lá có 24 ca: M1 0,927, M4 0,612, M1 thắng/thua 14/2.

---

## 7. Phân tích nhóm giúp/hại (luật 14, 15, 17, 18)

Cách đọc trung gian (code `src/m1/xep_hang.py`, `src/m1/e5.py`, `src/m1/e4.py`):

- Mỗi kênh có cờ mang điểm `s` = z của E4 = (max(A) − trung vị N)/IQR N (`src/m1/e4.py:276`).
- Khóa xếp E6a là (3 − tầng, max s, m của T4c, số kênh, Σs) (`src/m1/xep_hang.py:117–145`).
- Tầng 1 = có kênh F_I = 1; tầng 2 = mọi kênh có cờ đã bị E5 giải thích.
- "Độ rộng" của một kênh trace/metric là r_len_A − r_len_N: phần mẫu trong A vượt ngưỡng trên trừ phần đó trong N, lấy từ đơn vị phân vị cùng mã (`PT#/doi_chieu_sai_dung`).

Mỗi nhóm tách: **Quan sát** (số trên file), **Suy luận** (từ code và trung gian), **Ứng viên** (chưa kiểm), **Câu hỏi mở**.

### 7.1 TT: M1 so với TORAI B

**Quan sát.** Có 7 ca M1 thắng và 3 ca thua (`PT#/so_cap/RE2-TT|M1-torai_B|RR/cases`).

- Ba ca thua `test-053c028c65`, `test-5e8f996191`, `test-7a22c1c7ba` cũng là ba ca duy nhất M1 không đặt root ở hạng 1. Ở cả ba, M1 xếp root hạng 2 (RR 0,5); TORAI B xếp hạng 1 ở mọi seed (`PT#/ho_so_tang_root_M1/RE2-TT`).
- Ca thắng tập trung ở ts-auth-service loss: 3 ca, TORAI B RR 0,2/0,2/0,125, M1 1,0. Thêm auth socket, order delay và train socket ×2.
- Ở các ca auth loss, TORAI B đặt ts-seat-service, ts-payment-service hoặc ts-order-other-service lên đầu. Nguồn: `result.json` của job torai_pipeline trong queue EC2. Đây là đọc trực tiếp, không nằm trong PT.

**Suy luận.** Cả 12 ca root auth thuộc nhóm bậc 0 theo vị trí N (`T#/position_N`; LESSONS ST3: auth không có cạnh). M1 và C-a0 vẫn xếp đúng ở nhóm này, vì xếp tầng theo kênh không cần cạnh. TORAI B yếu hơn ở nhóm bậc 0 (§6).

**Câu hỏi mở.** Chưa đọc trung gian nội bộ của TORAI B, nên chưa xác định bước nào của TORAI làm mất thông tin ở auth loss. Đây là phân tích baseline, không cần để đọc A4.

### 7.2 TT: M1 so với C-a0 — bỏ cả E1, E2, E5

**Quan sát.** 2 thắng, 2 thua, Δ MRR = 0 (`PT#/so_cap/RE2-TT|M1-C-a0|RR`). Chỉ 4/60 ca đổi khối đầu (`PT#/doi_top_khi_bo/RE2-TT|M1 vs C-a0`). Từng ca (`PT#/trung_gian_theo_ca/RE2-TT|<ca>/<vế>`):

- `test-327ac2a20e` (route cpu), M1 thắng. Ở C-a0, root có max s 326,679, sau ts-train-service 328,518. Ở M1, kênh self-time E1 của root đạt s 1085,715. C-a1, chỉ có E1, cũng thắng. **Trong điều kiện CPU của route-service làm tăng chính phần tự thực hiện của span, bước E1 (trừ hợp span con) giữ thông tin độ lệch self-time mà thời lượng toàn phần làm loãng.**
- `test-e9dc7064cc` (route cpu), M1 thắng. Ở C-a0 và C-a1, ts-travel-service (bên gọi root) có s 4365,83, cao hơn root. Ở bo-E5 root vẫn hạng 2. Ở M1, travel-service xuống tầng 2: E5 giải thích kênh "error" của nó theo quy tắc nhóm vòng, dựa vào kênh của config, order-other, order và route (`PT#/E5_ca_quyet_dinh/RE2-TT|test-e9dc7064cc`). Đây là ca duy nhất trong 94 ca mà E5 đổi RR của root. Phần giải thích dựa cả vào thực thể ngoài đường gọi trực tiếp với root, qua nhóm vòng (SCC co vòng).
- `test-7a22c1c7ba` (travel delay), M1 thua. Ở C-a0, kênh lớn nhất của root là thời lượng toàn phần `TripRepository.findByTripId`, s 7445,873. Ở M1, đơn vị self-time của chính operation đó không có cờ: r_len_A 0,043 so với r_len_N 0,030 (`extra/don_vi_phan_vi` trong `result.json` của M1, ca này). Kênh lớn nhất của root còn s 1341,539 (`find ts.trip`). ts-train-service (bên được gọi) giữ s 2287,673 qua mọi vế, nên vượt lên. **Trong điều kiện trễ của root nằm trong span con của chính nó (truy vấn DB), bước E1 chuyển độ lệch từ span cha sang span con, làm mất điểm lớn nhất của root.** Kênh của train là metric latency-90 với N rất hẹp: h 0,0095, l 0,0084, r_len_A 0,883. Train là bên được gọi, nên E5 không giải thích kênh lan ngược này bằng root. Vì sao latency của train tăng khi travel bị trễ thì chưa biết.
- `test-5e8f996191` (order socket), M1 thua. Ở C-a0, root 811,69 đứng trên ts-auth-service 562,27. Với E1, root lên 942,06 nhưng auth lên 1438,655 (`UserRepository.findByUsername`, độ rộng 0,061). C-a1 cũng thua, nên bước gây đổi là E1.

**Suy luận.** Trên TT, E1, E2 và E5 gộp lại không đổi MRR. E1 vừa giúp vừa hại; E2 không đổi ca nào (bo-E2 trùng M1 ở 60/60 ca); E5 quyết định 1 ca.

### 7.3 TT: tương tác E1×E5 (bỏ E1 nhưng giữ E2, E5)

**Quan sát.** Bỏ E1 làm 10 ca kém đi và không ca nào tốt hơn (`PT#/so_cap/RE2-TT|M1-bo-E1|RR`). Thế nhưng C-a0, bỏ cả E1 lẫn E5, lại bằng M1. Ở các ca bỏ E1:

- Kênh thời lượng toàn phần của root (lớp lan ngược) mất F_I. Ví dụ: `test-547d46b5ce` có 9 kênh op_full có cờ thì 0 kênh còn F_I; số dòng giải thích của root tăng từ 86 lên 473.
- Root bị giải thích bởi kênh E2 hoặc metric của bên được gọi: ts-station, ts-train, ts-route, ts-ticketinfo (`PT#/trung_gian_theo_ca/RE2-TT|test-547d46b5ce/bo-E1`).

**Suy luận (cơ chế).** **Khi tắt E1, kênh trace của root thuộc lớp lan ngược. E2-C gán bằng chứng của cạnh root→bên được gọi cho bên được gọi. E5 dùng kênh đó để giải thích kênh lan ngược của root. Kết quả: root mất phần lớn kênh F_I, và bên được gọi vượt lên.** Với E1 bật, kênh self-time thuộc lớp không lan nên không bị giải thích, và root được giữ lại. Vì vậy E1 trong M1 chủ yếu chặn tác dụng phụ của E2+E5 trên TT. Nó không thêm thông tin so với C-a0.

**Câu hỏi mở.** Bằng chứng cạnh root→bên được gọi tăng vì root chậm hay vì đường mạng? Cả hai đều có thể. E2-C gán về bên được gọi trong mọi trường hợp. Dữ liệu hiện có chưa phân xử được.

### 7.4 OB: M1 so với M4 và C-a0; vai trò E1, E2, E5, C-d2

**E2 ở network_delay.**

- **Quan sát.** Bỏ E2 làm 7 ca kém đi, 2 ca tốt hơn (`PT#/so_cap/Nezha-OB|M1-bo-E2|RR`). 7/9 ca đổi thuộc network_delay.
- Ở C-a0, trong 10 ca network_delay: root của 4 ca không có kênh F_I nào (`kenh_s_max` = null), 5 ca chỉ có kênh metric, 1 ca có kênh op_full (`PT#/doi_chieu_sai_dung/Nezha-OB|C-a0`). C-a0 sai 8/10 ca này. Ở 6/8 ca sai, thực thể đứng đầu là bên gọi trực tiếp của root (frontend, checkout hoặc recommendation; cạnh có trong `canh_root_doi_thu`), với kênh op_full rộng 0,898–0,944.
- Ở M1, kênh mạnh nhất của root là E2_edge rộng 0,898–0,946 ở 7/10 ca network_delay. MRR network_delay: M1 0,900, C-a0 0,408 (`PT#/tach_MRR/Nezha-OB|fault/network_delay`).
- **Suy luận (cơ chế).** **Trong lỗi network_delay ở service X, span phía nhận của X không dài ra. Độ trễ nằm giữa span bọc của bên gọi và span nhận của X. Không có E2, X không có cờ trace riêng; trễ chỉ hiện ở span client của bên gọi, nên bên gọi đứng đầu. E2-C so span bọc với span nhận rồi gán bằng chứng cạnh cho X, nên X có kênh không lan, rộng.** Đây là việc dùng quan hệ cha–con của span (luật 18: nút X, cạnh bên gọi→X, phép tính là chênh lệch hai span cùng cuộc gọi).

**E1 ở lỗi CPU.**

- **Quan sát.** Bỏ E1 làm 8 ca kém đi, 1 ca tốt hơn. Các ca chủ yếu là frontend cpu_consumed/cpu_contention, checkout cpu và recommendation cpu (`PT#/so_cap/Nezha-OB|M1-bo-E1|RR`).
- Ở `test-3a1afd6d4f` và `test-2a10521c83`, kênh mạnh nhất của root là self-time `Frontend/Recv.` với độ rộng 0,465 và 0,603 (`PT#/doi_chieu_sai_dung/Nezha-OB|M1`). C-a1 hơn C-a0 với Hit@5 4/30/0, CI [0,0035; 0,043] (`PT#/so_cap/Nezha-OB|C-a1-C-a0|Hit5`).

**E5 trên OB.**

- **Quan sát.** bo-E5 trùng M1 ở 34/34 ca, kể cả khối đầu. E5 vẫn hoạt động: 14/34 ca có thực thể tầng 2, tổng 21 thực thể, 1418 dòng giải thích áp dụng (`PT#/E5_tac_dung_M1/Nezha-OB`). Trên TT có 59/60 ca có thực thể tầng 2, 14.905 dòng, nhưng chỉ 1 ca đổi RR.
- **Suy luận.** Thực thể bị E5 hạ tầng hầu như đã đứng dưới root theo max s. Vì vậy E5 thường không quyết định hạng. Ca `test-88dc4b2c47` (frontend exception) có root ở tầng 2: log lỗi của frontend bị giải thích bởi kênh E2 của recommendationservice và kênh op của checkoutservice. Nhưng ở bo-E5, ba thực thể có s lớn hơn vẫn đứng trên, nên RR không đổi (0,25).

**C-d2.**

- **Quan sát.** M1 thua C-d2 2 ca (`test-3eca4ed46f`, `test-d46d61c932`), thắng 1 ca (`test-6ea21f2759`), Δ −0,0025 (`PT#/so_cap/Nezha-OB|M1-C-d2|RR`). Theo bảng khóa: "M1 hơn baseline nhưng thua C-a hoặc C-d2 → giới hạn theo cặp, không khẳng định lợi ích quan hệ chung."
- **Suy luận.** C-d2 có cùng kênh E1/E2. Phần OB hơn C-a0 vì vậy nằm ở **bước dựng kênh có dùng quan hệ**, không ở **bước xếp hạng trên đồ thị** (E5/E6a).

### 7.5 Ca sai của M1 (10/94) so với ca đúng có điều kiện tương ứng

**Quan sát** (`PT#/doi_chieu_sai_dung/<ds>|M1`, nhóm "sai"). Có 10 ca root không đứng riêng ở khối đầu: TT 3, OB 7.

- Ở 6/10 ca (TT `053c`, `5e8f`; OB `07fef`, `3218`, `4dbc`, `d46d`), thực thể đứng đầu thắng nhờ một kênh có s rất lớn nhưng hẹp, độ rộng 0,015–0,16. Kênh rộng nhất của root rộng 0,43–1,0. Ví dụ OB `test-3218391218`: adservice `GetAds` self-time có s 11715,7, độ rộng 0,16; root frontend có s 2318,4, độ rộng 0,43. OB `test-d46d61c932`: productcatalogservice `sql.rows` có s 4063,6, độ rộng 0,016; root có E2 s 119,0, độ rộng 0,946.
- Bốn ca còn lại khác nhau:
  - `7a22`: cả hai kênh đều rộng (§7.2).
  - `3eca`: cả hai đều hẹp; root rộng 0,046.
  - `88dc`: root không còn kênh F_I (§7.4).
  - `fd2c`: root chỉ có kênh log s 1,0.
- Ở TT, 2/3 ca sai có đối thủ là ts-auth-service, không có cạnh với root. Ở OB, adservice đứng đầu 3/7 ca sai; productcatalogservice 2/7.

**Đối chiếu ca đúng** (luật 15):

- Trong ca đúng, đối thủ hạng 2 cũng thường có kênh mạnh nhất hẹp (độ rộng < 0,2): 43/57 ca TT và 12/27 ca OB.
- Root của ca đúng cũng thường thắng nhờ chính kênh hẹp của nó: 30/57 TT, 5/27 OB. Ví dụ `test-c5520b6a87`: root s 19732,3, độ rộng 0,083.
- Trong ô có cả ca đúng và ca sai: `test-fdcc43a676` (order socket, đúng) có root s 8421,0, lớn hơn mọi đối thủ. Ở hai ca sai cùng ô, s của root là 508,0 và 942,1, nhỏ hơn s của auth.

**Suy luận.** **Trong điều kiện một thực thể khác có kênh với z cực trị (từ max(A)) lớn hơn z lớn nhất của root, bước E6a đặt max s ngay sau tầng sẽ đặt thực thể đó lên trên. Thông tin độ rộng lệch, đang có lợi cho root ở 6/10 ca sai, không được dùng ở vị trí khóa đó.** Cùng đặc tính này cũng giúp root ở nhiều ca đúng. Vì vậy đây là điều kiện làm max-z sai, không phải nguyên nhân riêng của mọi ca sai. Cũng chưa suy được rằng một khóa khác sẽ hơn tổng thể.

**Ứng viên (chưa kiểm).**

1. Kênh hẹp có s cực lớn ở thực thể không phải root là bất thường nền, có cả ngoài cửa sổ lỗi; chẳng hạn adservice (Java) hoặc auth.
   - Giả định: kênh đó cũng lệch trong cửa sổ không có lỗi.
   - Sai khi: kênh chỉ lệch trong A, tức là lan truyền thật.
   - Bằng chứng cần: điểm của cùng kênh ở cửa sổ bình thường. Trên TT có thể đọc vế C-e (t′ = t − 300) đã chạy. Trên OB không có vế tương ứng.
   - Kết luận phụ thuộc: có nên đổi khóa xếp hay chuẩn hóa z.
2. Một khóa ưu tiên độ rộng, hoặc z robust không dựa max(A), sẽ giảm ca sai.
   - Không kiểm trên 94 ca này: tính lại hạng trên test để chọn khóa là thiết kế theo test (C-15 B).
   - Phải kiểm trên dev trước. Nếu dùng, kiểm độc lập trên dữ liệu chưa dùng sau khóa (RE3 bản cuối hoặc FlashTicket).

**Câu hỏi mở.**

- Vì sao latency-90 của ts-train-service tăng ở `7a22`.
- Vì sao frontend exception (2/2 sai) yếu: root là nút nguồn, nên E2 không gán bằng chứng cho root.
- TORAI B làm mất thông tin gì ở auth loss.

### 7.6 Phân biệt nguồn hạn chế (luật 17)

| Nguồn | Đã xác nhận | Chưa phân xử |
|---|---|---|
| Dữ liệu/đầu vào | 5 ca TT có operation 1 span bình thường hoặc operation mới, làm TraceRCA/MicroRank lỗi | Bất thường nền ở adservice/auth (ứng viên 1) |
| Giao thức | OB chỉ 3 ô hữu hiệu → không phân xử được Hit@5 ở 0,05; TT 6 ô khác 0; Hit@5 chạm trần | — |
| Adapter/cài đặt | D1: adapter OB sửa sau khi đọc cấu trúc thời gian cohort; D4 không tách được | Tác động của D1 lên 30 ca còn lại |
| Giả định/cách tính của phương pháp | E6a đặt max z trước độ rộng; E2-C gán cạnh về bên được gọi; E1 làm mất độ lệch span cha khi trễ ở span con | Hướng gán E2 khi root là bên gọi; lợi ích của khóa khác |

Không cộng các cờ trên thành tỷ lệ nguyên nhân. Một ca có thể thuộc nhiều dòng.

---

## 8. Mô tả ngoài A4

- **C-e TT** (`PT#/ce_tom_tat`): 58 OK, 2 INSUFFICIENT_EVIDENCE (ngoài mẫu số).
  - Cửa sổ t′ = t − 300: V0 là CAUSE_FOUND ở 58/58 ca; trung bình 476/29 ≈ 16,4 thực thể tầng 1 mỗi ca.
  - RR của root tương lai trung bình ≈ 0,130; mức ngẫu nhiên trên tập trả về ≈ 0,071. Root tương lai đứng hạng 1 ở 3/58 ca.
  - Giới hạn: trước tiêm chưa xác nhận lành, nên đây không phải hiệu chuẩn detector. Nhưng nó cho thấy M1 luôn trả "có nguyên nhân" khi chưa có lỗi được tiêm. Thứ hạng trong cửa sổ lỗi vì vậy dựa vào độ lớn tương đối, không dựa vào một ngưỡng phát hiện.
- **Vùng nghi ngờ E7** (`PT#/regions`). Đây không phải vùng ảnh hưởng đã kiểm; chưa có nhãn vùng.
  - TT: cách 1 chứa root với tỷ lệ kỳ vọng 0,95, cỡ kỳ vọng 3,9, bằng 0,057 số thực thể quan sát; cách 2 chứa root 0,967, cỡ 12,0, tức 0,177.
  - OB: cách 1 chứa 0,824, cỡ 1,38; cách 2 chứa 0,912, cỡ 3,62.
  - T12-on làm vùng cách 2 lớn hơn: TT 12,0 → 17,9, tỷ lệ chứa root 0,967 → 0,983; OB 3,62 → 3,82.
- **Vị trí N** (`PT#/position_N_p75`): TT có bậc 0 13, lá 23, hub 21, giữa 3; OB có lá 24, nguồn 6, hub 2, giữa 2.
- **TORAI A, bảng phụ.** Chỉ `test-cda8dfc162` đủ ba seed (RR 1,0); seed 1 có khoảng mất quan sát 342 s (§2). Bảng phụ chưa dùng được.

---

## 9. Kết quả trả lời câu hỏi MRP tới đâu

| Câu | Trả lời được | Giới hạn |
|---|---|---|
| RQ3b TT | Đạt E-04 theo công thức; chưa phân biệt hơn/kém TORAI B | 6/20 ô khác 0; CI danh nghĩa; Hit@5 gần trần; C-a0 cho cùng kết quả |
| RQ3b OB | Chênh Hit@5 dương; không đạt mức đã khóa; MRR mô tả dương so M4 | 3 ô hữu hiệu không thể đạt 0,05; D1; giới hạn M4 (Q-192) |
| RQ3d — bỏ quan hệ | TT: không thấy lợi ích. OB: lợi ích mô tả từ E2 (network_delay) và E1 (cpu), là bước dựng kênh dùng quan hệ cha–con của span | Không có đồ thị ngẫu nhiên (WHY-07): không kết luận về cấu trúc phụ thuộc thật. Mô tả, không phải phép kiểm khai trước |
| RQ3d — quy tắc đơn giản cùng đồ thị | OB: M1 ≈ C-d2 (−0,0025). TT: M1 hơn C-d2 1 ca | Bước xếp hạng E5/E6a chưa chứng tỏ hơn quy tắc khởi phát sớm nhất |
| RQ3c | Chỉ vùng nghi ngờ: tỷ lệ chứa root và cỡ vùng | Không có P/R/F1 vùng |
| RQ3a | Chưa có (Q-245) | G4 phải khai |
| "Vì sao" (MRP: hoàn thành nghĩa là gì) | Có cơ chế cho E2/network_delay, E1/cpu, E1×E5 trên TT và điều kiện của max-z ở 6/10 ca sai | Nguồn của các kênh hẹp cực trị chưa biết; TORAI B chưa lần |

DT18 và cô yêu cầu "phân tích các trường hợp phương pháp hoạt động hiệu quả hoặc còn hạn chế" (DT18 §2) và so sánh với baseline. Báo cáo đã có cả hai, theo ca và theo ô. Việc áp dụng lên FlashTicket, LLM và P/R/F1 thuộc P8–P10.

---

## 10. Căn cứ cho quyết định kế tiếp: giữ M1 hay sửa trước khi khóa bản cuối cho RE3

Đây là đề xuất để Minh quyết. Agent không tự chọn.

**Căn cứ đã có.**

1. Kết quả chính của bản khóa giữ nguyên: TT đạt E-04 theo công thức, OB không đạt (C-15 B).
2. Trên TT, mọi phần có dùng quan hệ (E1, E2, E5, T12) không đổi MRR so với C-a0. Trên OB, phần hơn đến từ E1/E2. E5 và T12 không đổi hạng ở 93/94 và 94/94 ca.
3. Cơ chế sai chính (max-z hẹp) cũng là cơ chế đúng ở nhiều ca. Chưa có bằng chứng một khóa khác hơn tổng thể.
4. RE3 chỉ mở một lần cho bản cuối. H1 RE3 còn OPEN (D2): nguồn, profile và quyền riêng chưa có.

**Phương án.**

| Phương án | Lợi | Hại / rủi ro |
|---|---|---|
| (a) Giữ M1 nguyên cho RE3 | RE3 là kiểm độc lập sạch của đúng bản khóa; không thiết kế theo test | Nếu sau này sửa khóa xếp, chỉ còn FlashTicket để kiểm độc lập bản sửa |
| (b) Sửa nhỏ có nguyên lý, ví dụ bỏ E5 hoặc đổi khóa/chuẩn hóa z: thiết kế trên dev rồi khóa lại; RE3 kiểm bản sửa | Có thể giảm ca sai kiểu max-z | Quan sát lấy từ test → phải khai C-15 B; cần bằng chứng dev đủ; tốn thêm một vòng khóa và chạy |
| (c) Đơn giản hóa về C-a0 hoặc C-d2 làm bản cuối | Bằng M1 trên TT và gần bằng trên OB, ít thành phần hơn | Chọn theo kết quả test, vi phạm tinh thần QT4/QT6; mất E2 làm giảm OB |

**Đề xuất của người làm:** (a), kèm một bước rẻ trước khi Minh chốt.

- Bước 1, chỉ đọc. Dùng bản ghi dev đã có ở `results/T-051/kb-002/ban-ghi.jsonl`: 260 bản ghi = 52 ca × 5 cấu hình khối K, trong đó có `K-E1+E2+E5`, gồm khối, tầng và `kenh_co_the_gioi`. Trước khi dùng phải kiểm cấu hình này có khớp tham số M1 đã khóa không; chưa kiểm. Dùng nó để đếm ca dev mà root thua vì đối thủ có max s cao hơn, và ca dev mà E5 quyết định hạng. Các bản ghi này **không có** độ rộng từng kênh (`don_vi_phan_vi`). Bản ghi đầy đủ theo kênh chỉ có ở vài ca fixture/pilot (ví dụ `runs/trien-khai-001/fixtures-003/`). Laptop, dự kiến dưới 30 phút, không chạy phương pháp. Ước lượng chưa kiểm.
- Bước 2, chỉ khi bước 1 cho thấy kiểu sai này trên dev và Minh duyệt. Chạy lại M1 nền trên 52 ca dev, ghi đủ trung gian, để đo độ rộng. Đây là chạy phương pháp trên dev, theo luật 19 ưu tiên hai EC2 cho 30 TT và laptop cho 22 OB. Ước lượng chưa kiểm: 0,5–1,5 giờ thời gian trôi, gồm chuyển và kiểm. Nếu vượt 1 giờ thì cần quyền theo luật 8; hồ sơ phải có mục luật 21.
- Nếu dev có cùng kiểu sai với tần suất đáng kể: trình phương án (b) có nguyên lý từ dev, khai rõ là đã thấy trên test.
- Nếu không: giữ (a).
- Kết luận phụ thuộc: chọn bản cuối cho RE3, và câu RQ3d ở G4.
- Việc RE3 vẫn cần đóng H1 và cấp quyền riêng trước.

---

## 11. OPEN và phần thiếu

- Bảng phụ TORAI A: thiếu 176 slot. Minh quyết có chạy bù không. Chạy bù sau mốc xem phải gắn nhãn "chạy sau khi đã xem".
- Trung gian TORAI B ở ca auth loss: chưa lần.
- Nguồn kênh hẹp cực trị (ứng viên 1, §7.5): cần đọc C-e TT; OB không có vế tương ứng.
- Hướng gán E2-C khi root là bên gọi (§7.3): chưa phân xử được bằng dữ liệu hiện có.
- D1/D4: tác động adapter OB chưa tách.
- RQ3a, độ đúng vùng, LLM, FlashTicket, quan hệ messaging/data: thuộc P8–P10; G4 phải khai.
- RE3: H1 OPEN, chưa có quyền.

## 12. Tái lập

```text
py -3 -B results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents
py -3 -B results/T-054/reports/p7a-013-v2/phan_tich.py <đường-dẫn-ra-ngoài-repo.json>
```

Chạy từ gốc repo. Không đối số thì script ghi `phan-tich-nhom.json` và dừng nếu file đã có. Script chỉ đọc A, T, `report-receipt.json`, `verified.json`/`job.json`/`result.json` trong ba queue main-013-v2; không đọc telemetry và không chạy phương pháp.
