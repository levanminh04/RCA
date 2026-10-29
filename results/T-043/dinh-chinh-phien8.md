# Đính chính phiên 8 — T-043

- **Ngày:** 28/10/2026. **Người làm:** Claude. **Trạng thái:** đề xuất, chờ Codex phản biện và Minh quyết.
- **Nguyên tắc:** không sửa file đã đóng băng ở phiên 7: `dac-ta-phuong-phap-v1.md`, `hop-dong.json`, `dinh-nghia-pha2.json`, `ma-tran-thu.json`, `ks16/dem-khong-nhan.json`, `ks16/dem-sau-ghep-nhan.json`. File này ghi từng chỗ cần sửa (câu cũ → câu mới), bằng chứng, thời điểm đã nhìn dữ liệu, các đầu ra phải tính lại, và kết quả tính lại.
- **Kết quả tính lại theo luật sửa** nằm ở lượt mới. Các lượt cũ giữ nguyên:
  - `ks16/runs/pha1-002/` (script `ks16/ks16_pha1_v11.py`);
  - `ks16/runs/pha2-002/` (script `ks16/ks16_pha2_v11.py`).
- **Thời điểm:** mọi sửa dưới đây đặt sau khi đã có kết quả pha 2 của phiên 7, tức sau khi đã nhìn nhãn và số ô kích hoạt. Không sửa nào động tới định nghĩa ô kích hoạt (`dinh-nghia-pha2.json` giữ nguyên, hash kiểm lại khi chạy `pha2-002`).

## Đ1. Căn cứ của khoảng ghi của file F_s (nhận xét của Codex)

**Nhận xét của Codex** (Minh chuyển ở đầu phiên 8): F_s được dựng từ thời điểm bản ghi đầu và cuối của file; phần ngoài F_s gán XÁC NHẬN THIẾU THU. Câu hỏi: bằng chứng xác nhận khoảng thu thập thực tế, hay chỉ cho biết khoảng có sự kiện được ghi.

**Kiểm độc lập** (`scripts/kiem_bien_F.py`, lượt `runs/bien-F-001`, chỉ đọc, không nhãn, 152 giây):

| Phần thời gian | Bằng chứng hiện có | Phân loại đúng | v1 xử lý |
|---|---|---|---|
| Nezha-OB, ngoài ba file phút của ca (khoảng 4 phút trong cửa sổ 10 phút) | (1) Điều kiện xuất dữ liệu: trên cả 101 bản ghi Nezha, `rca_data` chỉ có ba file phút [phút nhãn tiêm, +1, +2]; không có file phút giữa các lần tiêm (`results/T-008/the-dataset.md` §8, lượt `runs/sampling-leakage-001`). Đây là bằng chứng phía thu/xuất, không suy từ việc không thấy bản ghi. (2) Hỗ trợ: metric theo ngày phủ cả cửa sổ; 740/740 điểm `PodWorkload` trước F_s dương ở 22/22 ca (`runs/bien-F-001/ket-qua.json#/tong_hop`). Hệ đang chạy, nên "không có sự kiện" không giải thích được | XÁC NHẬN THIẾU THU | Đúng; văn bản v1 không nêu căn cứ |
| Nezha-OB, khe dương giữa hai file phút liền nhau | Nằm ngoài khoảng bản ghi của mọi file: 30 khe ở 12/22 ca, dài 0,055–1,212 s; 58 chỗ nối còn lại là hai file chồng nhau. Mép file dày: 100 bản ghi đầu nằm trong ≤ 1,12 s, 100 bản ghi cuối trong ≤ 1,38 s. Vì vậy khe cỡ 1 s mà không có bản ghi nào của mọi dịch vụ khó giải thích bằng "không có sự kiện". Khe ngắn cỡ vài chục ms thì mật độ không phân biệt được (`#/tong_hop/max_mep_*`, `#/cases/*/*/khe_giua_file_s`) | XÁC NHẬN THIẾU THU theo tiêu chí "ngoài khoảng ghi của file" (B1.3b); với khe ngắn, phân loại là xấp xỉ như ở mép ngoài | **Sai:** code v1 gộp khe vào F, coi là quan sát theo A0 |
| Nezha-OB, mép ngoài: từ mốc xuất thật tới bản ghi đầu (hoặc từ bản ghi cuối tới mốc xuất) | Không có. Tên file phút lệch khoảng 30 giây so với thời điểm bản ghi, nên không dùng làm khoảng khai báo. Phần chưa biết bị chặn bởi khoảng cách hai bản ghi đầu: ≤ 3,6 ms (trace), ≤ 0,44 ms (log) | Không biết (đúng ra là OPEN), độ dài cỡ ms | Gán thiếu thu; sai số không đáng kể |
| RE2-TT, mọi nguồn | Một file mỗi nguồn mỗi ca, phủ ít nhất [t−719, t+719]; cửa sổ chính [t−300, t+300) và mốc giả [t−600, t) nằm trọn trong F (`ks16/dem-khong-nhan.json#/cases/*/quan_sat/*/F_rel_t`) | Luật F không tác động trong cửa sổ | Đúng |
| RE2-TT, ca dev-3defe3d34b không có file log | File vắng ở mức dataset (allowlist T-022 ghi `logs.parquet` vắng; RCAEval có log ở 89/90 ca, LESSONS ST2) | XÁC NHẬN THIẾU THU (không có file) | Đúng; điểm không đổi vì 0 sự kiện cho LOW_SUPPORT ở mọi cách |

**Kết luận về nhận xét:**
- **Đúng một phần.** Văn bản v1 định nghĩa F_s là bao bản ghi của file và gọi đó là "khoảng ghi của file" mà không nêu căn cứ thu/xuất. Với Nezha-OB, căn cứ thật là điều kiện xuất dữ liệu đã kiểm ở T-008 §8, không phải việc không thấy bản ghi.
- Phần lớn phân loại vẫn đứng, nhờ bằng chứng đó.
- Phần mép ngoài thì chỉ là xấp xỉ (cỡ ms).
- **Phát hiện thêm của người làm:** khe giữa hai file bị v1 gộp vào F, trái tiêu chí "ngoài khoảng ghi của file" của B1.3b. Câu "khe giữa hai file dài hơn 10 giây nằm ngoài F_s" của v1 cũng không được cài: code chỉ liệt kê khe, không loại khe khỏi F. Trên dev khe dài nhất là 1,212 s, nên câu về khe trên 10 giây không có tác động số.

**Văn bản, hợp đồng và code v1 không cùng một nghĩa:**
- Văn bản đặc tả v1 §2.2 điểm 2 mơ hồ. "F_s là hợp các khoảng của từng file" theo nghĩa đen đã loại mọi khe. Câu sau, "khe dài hơn 10 giây nằm ngoài F_s", và trường `hop-dong.json#/quan_sat/khe_file_toi_da_s` = 10 lại ngầm cho phép nối khe ≤ 10 s.
- Code v1 lấy bao của mọi bản ghi: nối mọi khe, chỉ liệt kê khe > 10 s. Định nghĩa ghi trong đầu ra v1 khớp code: "hợp ba file phút, kiểm khe > 10 s" (`ks16/dem-khong-nhan.json#/dinh_nghia/khoang_ghi_file_F`).
- Dev không có khe > 10 s, nên số v1 trùng cách đọc "nối khe ≤ 10 s", không trùng cách đọc nghĩa đen. Số v1.1 trùng cách đọc nghĩa đen.
- Báo cáo ghi rõ mỗi số thuộc bản nào.

**Sửa đề xuất (luật v1.1):**
- F_s là hợp các khoảng [bản ghi đầu, bản ghi cuối + r) của **từng file**. Khe dương giữa hai file nằm ngoài F_s.
- Mép ngoài lấy theo bản ghi đầu và cuối. Đây là xấp xỉ có sai số chặn bởi mật độ bản ghi ở mép; ghi rõ là xấp xỉ.
- Thay đặc tả v1 mục 2.2 điểm 2:
  - câu cũ: "F_s là hợp các khoảng của từng file. Khe giữa hai file dài hơn 10 giây nằm ngoài F_s."
  - câu mới: "F_s là hợp các khoảng [bản ghi đầu, bản ghi cuối + r) của từng file; mọi khe dương giữa hai file nằm ngoài F_s. Mép ngoài là xấp xỉ theo bản ghi đầu/cuối; trên Nezha-OB dev, sai số ≤ 3,6 ms. Căn cứ phân loại 'thiếu thu' cho phần ngoài file của Nezha-OB là điều kiện xuất dữ liệu (results/T-008/the-dataset.md §8), không phải việc không thấy bản ghi."
- `hop-dong.json#/quan_sat/khe_file_toi_da_s`: 10 → 0 (không gộp khe).

**Hậu quả và tính lại:** điền ở mục Đ5 sau khi chạy `pha1-002`, `pha2-002`.

## Đ2. Thông tin khoảng ghi phải vào phương pháp qua đâu; giới hạn rò nhãn ở Nezha-OB

- **Mâu thuẫn trong SPEC:** API chỉ nhận `spans, metrics, logs, inventory, aliases, t, params` (SPEC, Kiểm đúng đắn). Nhưng B1.3b cần siêu dữ liệu thu thập (khoảng ghi file, chỉ số collector, manifest) để phân loại ô. `hop-dong.json` v1 không nói siêu dữ liệu này đi vào bằng đường nào. KS-16 tính F từ file, ở phía runner.
- **Sửa đề xuất:** khai `params.coverage = {nguồn: [khoảng ghi]}` do runner cung cấp.
  - Trên dev: lấy từ khoảng bản ghi của file theo Đ1.
  - Trên FlashTicket: lấy từ manifest và chỉ số collector (B16 mục 8).
  - Không đổi chữ ký API, vì `params` đã nằm trong danh sách.
- **Giới hạn rò nhãn:** T-008 §8 ghi việc file tồn tại mang thông tin suy từ nhãn (phút tiêm). Ở chế độ (a), runner đã cấp t (Q-66), nên F_s của Nezha-OB không thêm thông tin nhãn nào ngoài t; nó không cho biết root hay loại lỗi. Ở chế độ (b), dùng F_s của Nezha-OB là rò mốc tiêm. Vì vậy chế độ (b) trên Nezha-OB không được dùng `params.coverage` dựng từ file phút. D16 hiện chỉ đặt RCA chế độ (b) trên RE2-TT, nên chưa có phép nào bị ảnh hưởng.

## Đ3. Câu về ba thế giới trong `ma-tran-thu.json`

- **Câu cũ** (`#/co_dinh_moi_buoc/the_gioi`): "mọi ca dev có ô biên chứa phần OPEN dưới 1,4 giây, nên chạy ba thế giới cho cả 52 ca".
- **Kiểm** (lượt `pha1-001`, T^max − T^chắc theo ca và nguồn):
  - RE2-TT trace: 30/30 ca có phần OPEN (≤ 0,90 s ở N, ≤ 1,40 s ở A);
  - RE2-TT log: 3/30 ca (≤ 1,0 s ở N);
  - RE2-TT metric: 0/30;
  - Nezha-OB trace, log: **0/22**;
  - Nezha-OB metric: 22/22 (≤ 60 s), nhưng metric không tham gia T.
- **Câu mới:** "Với đơn vị đếm, S_lo và S_hi chỉ khác P ở RE2-TT: trace ở 30/30 ca, log ở 3/30 ca, mỗi ca dưới 1,4 giây. Ở Nezha-OB, ba thế giới trùng P vì trace và log không có phần OPEN."
- **Hậu quả:** không đổi luật hay quyết định. Chạy ba thế giới cho Nezha-OB vô hại nhưng không cần.

## Đ4. Câu về 22 STOPPED ở Nezha-OB trong đặc tả v1 mục 7.4

- **Câu cũ:** "thao tác gần biên file phút có thể ngừng vì khoảng ghi bị cắt. KS-16 pha 1 thấy 22 STOPPED ở Nezha-OB, 0 ở RE2-TT; nguyên nhân chưa phân xử."
- **Kiểm:** 22 STOPPED là 11 thao tác của luồng checkout (EmptyCart, ShipOrder, Charge, SendOrderConfirmation…) trong 2 ca, mỗi thao tác n_N = 16 (`ks16/dem-khong-nhan.json#/cases/*/op_rows`). Không phân bố như nhiễu ở biên file.
- **Câu mới:** "KS-16 pha 1 thấy 22 STOPPED ở Nezha-OB: 11 thao tác luồng checkout trong 2 ca; 0 ở RE2-TT. Nguyên nhân chưa phân xử; không có dấu hiệu là nhiễu biên file."

## Đ5. Tính lại theo luật v1.1

**Lượt chạy** (giữ mọi lượt; hash ở `manifest.json`):
- Pha 1, không nhãn: `ks16/runs/pha1-002` (script `ks16/ks16_pha1_v11.py`). 52/52 ca, 0 lỗi, 556,4 giây (`progress.jsonl`, sự kiện `end`). Lượt thử nhanh trước đó: `ks16/runs/thu-nhanh-002` (2 ca).
- Pha 2: `ks16/runs/pha2-002` (script `ks16/ks16_pha2_v11.py`), 10,1 giây. Trước khi ghép nhãn, script kiểm hash mọi đầu vào ghi trong script: pha 1 v1.1, `dinh-nghia-pha2.json`, hai file nhãn, bản ghi baseline, đồ thị tĩnh.
- So sánh: `scripts/so_v1_v11.py`, lượt `runs/so-v1-v11-004`. Ba lượt trước giữ lại: 001 chưa tách khác kiểu số; 002 còn tính thời gian chạy theo ca là khác giá trị; 003 chưa có phần điểm. Phần chung của 003 và 004 trùng nhau.

**Thời điểm nhìn dữ liệu:** luật v1.1 sinh từ nhận xét của Codex và phép kiểm không nhãn `runs/bien-F-001`. Lúc sửa, người làm đã thấy kết quả pha 2 v1 (có nhãn). Định nghĩa ô kích hoạt không đổi.

**Kết quả** (con trỏ trong `runs/so-v1-v11-004/ket-qua.json` trừ khi ghi khác):

| Mục | v1 (`pha1-001`, `pha2-001`) | v1.1 (`pha1-002`, `pha2-002`) | Con trỏ |
|---|---|---|---|
| RE2-TT, mọi nguồn | — | Không đổi giá trị. Chỉ đổi kiểu số (300 thành 300,0) và dạng F (một khoảng thành danh sách một khoảng) | `#/so_sanh/pha1/nhom/kieu` |
| Nezha-OB, ca có giá trị đổi | — | 12/22 ca, đúng 12 ca có khe dương | `#/so_sanh/pha1/ca_co_khac_gia_tri` |
| T^chắc giảm (trace; log tương tự) | — | 13 cặp (ca, phía): 9 ở A, 4 ở N. Giảm nhiều nhất 1,212 s (1,01%) ở dev-27252dca60 phía A | `#/T_Nezha_OB_theo_ca_khac`, `#/T_Nezha_OB_giam_tuong_doi_lon_nhat` |
| Khoảng T^chắc của Nezha-OB trace | N 41,4–96,9 s; A 84,2–140,4 s | N 41,4–96,9 s; A 84,2–140,1 s | `#/quan_sat_tong_hop/v1/Nezha-OB/trace/T`, `#/quan_sat_tong_hop/v1_1/Nezha-OB/trace/T` |
| Ô của Nezha-OB (trace; log giống) | N: A0 150, biên 22, thiếu thu 488. A: A0 228, biên 22, thiếu thu 410 | N: A0 145, biên 27, thiếu thu 488. A: A0 216, biên 34, thiếu thu 410 | `#/quan_sat_tong_hop/*/Nezha-OB/trace/o` |
| OPEN, ba thế giới | Nezha-OB trace, log không có phần OPEN; P = S_lo = S_hi | Như v1 | `#/quan_sat_tong_hop/*/Nezha-OB/*/ca_co_o_OPEN` |
| Ô kích hoạt, O1–O4, hình dạng xếp hạng | Mục 2.6 của báo cáo | Giống hệt từng ca | `#/pha2_kich_hoat_giong_nhau_moi_ca` = true; `#/so_sanh/pha2/nhom/gia_tri` |
| Lý do E3b ở pha 2 | — | p của 30 mục ở 4 ca đổi, lệch tối đa 7,5 × 10⁻⁶. Số mục mỗi ca không đổi; dài nhất 9, dưới trần cắt 20 | `#/so_sanh/pha2/nhom/gia_tri`, `#/pha2_do_dai_ly_do_E3b` |
| Đơn vị đếm đổi quyết định cổng | — | RE2-TT 0/5.388. Nezha-OB 4/1.420: tần suất thao tác 1/1.188 (v1 không cờ, v1.1 có cờ); số dòng log theo thực thể 3/220 (v1 có cờ, v1.1 không); log lỗi 0/12. Ba thế giới cho cùng kết quả | `#/don_vi_dem_doi_quyet_dinh` |
| Điểm sau cổng của đơn vị đếm (thế giới P) | — | RE2-TT không đổi. Nezha-OB: tần suất thao tác 95/1.188 đơn vị đổi điểm, e thô lệch ≤ 0,0101, điểm sau cổng lệch ≤ 0,063; số dòng log theo thực thể 45/220, ≤ 0,0091 và ≤ 0,105; log lỗi 0/12. Hai lệch lớn nhất đều do cổng đổi kết quả | `#/don_vi_dem_doi_diem_the_gioi_P` |

**Phạm vi của hai hàng cuối:**
- Đơn vị là đại diện ở mức KS-16: tần suất thao tác (E3b) và số dòng log theo thực thể. Số dòng log theo thực thể thô hơn đơn vị mẫu Drain của E3.
- Cổng là phép nhị thức hai hướng của KS-16 pha 2 (p₀ = T_A / (T_N + T_A), α = 0,01, tổng ≥ 10). Điểm theo SPEC B1.3 (λ = n_N · T_A / T_N). Chưa áp hướng chấm của từng kênh (B1.4).
- Đây không phải điểm của M1. M1 chưa được cài.

**Hệ quả:**
- Số ô T0 trong `ma-tran-thu.json` và các khai trước dựa trên chúng không đổi: E3 ít ca; E1-CP KHÔNG ĐỦ CA. Không cần đóng băng lại số trong ma trận; chỉ còn câu sai ở Đ3.
- Lỗi của v1 có tác động thật ở mức đơn vị đếm Nezha-OB: 4/1.420 quyết định cổng và điểm của 140 đơn vị. Nếu task cài đặt dùng luật v1, Nezha-OB mang sai lệch này. RE2-TT không bị ảnh hưởng.
- **Quan sát thêm (chưa kiểm ngoài phép đếm trên):** quyết định cổng của đơn vị đếm có n lớn đổi khi T đổi dưới 1,1%.
  - Ví dụ: productcatalogservice ở dev-396c8dbf7d có 14.568 và 18.578 dòng log; T_N của log giảm 0,35 s (0,43%) thì mất cờ.
  - Sai số mép ngoài của F trên Nezha-OB (≤ 3,6 ms) nhỏ hơn mức này nhiều lần.
  - Quyết định phụ thuộc: task cài đặt (1) có cần báo số đơn vị đếm nằm sát ngưỡng hay không. Minh quyết.

## Đ6. Đầu ra bị ảnh hưởng

| Đầu ra | Ảnh hưởng | Xử lý |
|---|---|---|
| `dac-ta-phuong-phap-v1.md` §2.2 điểm 2, 9; §7.4 | Văn bản | Đ1, Đ3, Đ4, Đ8; chờ duyệt |
| `hop-dong.json` | `khe_file_toi_da_s`; thiếu `params.coverage` | Đ1, Đ2; chờ duyệt |
| `ks16/dem-khong-nhan.json` (bản chốt v1) | T, trạng thái ô của Nezha-OB trace và log ở 12 ca | Số v1.1 ở lượt `pha1-002` (Đ5). Bản chốt v1 giữ nguyên tới khi Minh quyết Đ1 |
| `ks16/dem-sau-ghep-nhan.json` (bản chốt v1) | p trong lý do E3b ở 4 ca; ô kích hoạt không đổi | Lượt `pha2-002` (Đ5) |
| `ma-tran-thu.json` | Câu ba thế giới (Đ3); câu trỏ mục của báo cáo (Đ7). Số ô T0 không đổi (Đ5) | Đ3, Đ7; không đóng băng lại số |
| `why-de-xuat.md` WHY-M1-03 | Lý do luật F | Đã sửa trong phiên 8 (file đề xuất, chưa đóng băng) |
| `bao-cao.md` | Số quan sát của Nezha-OB | Ghi số của cả hai bản, nêu rõ bản nào |
| `fixture-dac-ta.json` | Fixture 21 dùng một file liên tục, không có khe | Không đổi. Chưa có fixture cho khe giữa hai file; đề xuất thêm khi duyệt Đ1 |
| Task cài đặt (1) | Luật F mà code M1 dùng | Dùng v1.1 nếu Minh duyệt Đ1; nếu không, Nezha-OB mang sai lệch ở Đ5 |

## Đ7. Câu trỏ mục của báo cáo trong `ma-tran-thu.json`

- **Câu cũ** (`#/ngan_sach/thoi_gian`): "chưa đo; ước lượng ở bao-cao.md mục 6".
- **Kiểm:** `bao-cao.md` đặt dự toán ở mục 9; mục 6 là bảng bao phủ nguồn. Ma trận đóng băng ở phiên 7, trước khi báo cáo có bố cục cuối.
- **Câu mới:** "chưa đo; ước lượng ở bao-cao.md mục 9".
- **Hậu quả:** chỉ là chữ; không đổi luật, số hay quyết định.

## Đ8. Số làm tròn trong đặc tả v1 §2.2 điểm 9

- **Câu cũ:** "RE2-TT: trace, log, metric phủ [t−720, t+720] ở mọi ca, trừ ca không có file log"; "Nezha-OB: trace và log chỉ phủ 42–97 giây ở N và 84–140 giây ở A".
- **Kiểm** (`ks16/dem-khong-nhan.json`):
  - RE2-TT: đầu F trong [t−720, t−719], cuối F trong [t+719, t+722] (`#/cases/*/quan_sat/*/F_rel_t`). Cửa sổ chính và mốc giả vẫn nằm trọn trong F;
  - Nezha-OB: T^chắc nhỏ nhất ở N là 41,4 s (trace) và 41,5 s (log) (`#/tong_hop/Nezha-OB/quan_sat/*/T/N/chac_min`). Số 42 lấy từ phép đo nhanh ở bước tự rà soát (R7-1), trước KS-16.
- **Câu mới:** "RE2-TT: trace, log, metric phủ ít nhất [t−719, t+719] ở mọi ca có file"; "Nezha-OB: trace và log chỉ phủ 41–97 giây ở N và 84–140 giây ở A".
- **Hậu quả:** chỉ là chữ; không đổi luật, số hay quyết định.
