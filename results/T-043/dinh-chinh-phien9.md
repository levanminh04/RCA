# Đính chính phiên 9 — T-043

- **Ngày:** 29/10/2026. **Người làm:** Claude. **Trạng thái:** đã ghi theo Q-207 (lời Minh: “Giữ luật hiện tại”, rồi “Duyệt gói”). Codex chưa kiểm bản đã ghi.
- **Nguồn:** ba lượt Codex kiểm kết quả T-043 và ba lượt người làm đáp, ngày 28–29/10/2026. Nguyên văn ở LOG T-043 phiên 9.
- **Nguyên tắc:**
  - không sửa 10 file đóng băng ở phiên 7;
  - không sửa `dinh-chinh-phien8.md`, để giữ lịch sử;
  - bản này thay đúng các câu nêu dưới đây. Câu nào của phiên 8 không được nêu thì vẫn giữ.
- **Thời điểm nhìn dữ liệu:** mọi sửa đặt sau khi đã có pha 2 có nhãn (cả v1 lẫn v1.1) và kết quả baseline P3, và trước mọi kết quả M1. Không sửa nào đổi tập ô kích hoạt hay số T0 của ma trận.

## Đ9. Luật khoảng ghi F, phương án (a) (Q-207)

**Lý do:** biên thu thật không xác định được từ bản ghi.
- Khoảng cách giữa hai bản ghi đầu không chặn được khoảng từ lúc bắt đầu xuất tới bản ghi đầu.
- Khe không có bản ghi giữa hai file có thể là:
  - lúc không có sự kiện;
  - đệm khi xuất;
  - mất bản ghi ở biên file;
  - phần không được xuất.

  Dữ liệu hiện có không phân xử được các khả năng này.
- 58/88 chỗ nối giữa hai file là chồng nhau (`runs/bien-F-001/ket-qua.json#/cases/*/*/khe_giua_file_s`). Điều đó chỉ bác cách chia file thành các khoảng không chồng lấn theo đúng mốc mà F dùng (end của span, mốc của log); nó không bác mọi cách chia theo thời gian (xem Đ14).
- Chênh giữa v1 (gộp khe) và v1.1 (loại khe) là **độ nhạy** của kết quả với luật F, không là sai số so với sự thật.

**Thay đặc tả v1 §2.2:**
- **Điểm 2** (câu cũ: "F_s là hợp các khoảng của từng file. Khe giữa hai file dài hơn 10 giây nằm ngoài F_s."). Câu mới:
  > "Mỗi file của nguồn s phủ [bản ghi đầu, bản ghi cuối + r). Bao F_s là [bản ghi đầu của mọi file, bản ghi cuối của mọi file + r). Khe K_s là phần của F_s không thuộc file nào, tức khe dương giữa hai file liền nhau."
- **Điểm 4.** Câu mới:
  > "Ngoài F_s: XÁC NHẬN THIẾU THU, khi có căn cứ phía xuất (Nezha-OB: chỉ có ba file phút quanh mốc tiêm, `results/T-008/the-dataset.md` §8; RE2-TT: một file mỗi nguồn mỗi ca). Trong K_s: OPEN. Trong F_s ∩ H_s, ngoài K_s: QUAN SÁT THEO A0. Trong F_s, ngoài H_s: OPEN."
- **Điểm 7.** Câu mới:
  > "T^chắc = |(F ∩ H) \ K ∩ phía|; T^max = |F ∩ phía|."

  Công thức ba thế giới giữ nguyên: P = (T_N^chắc, T_A^chắc), S_lo = (T_N^max, T_A^chắc), S_hi = (T_N^chắc, T_A^max).
- **Giới hạn** (thêm):
  > "Mép ngoài của F_s lấy theo bản ghi đầu và cuối. Đây là giả định chưa kiểm, không có cận sai số. Giả định sai khi việc xuất bắt đầu trước bản ghi đầu, hoặc kết thúc sau bản ghi cuối, mà không có sự kiện; khi đó T bị đánh giá thấp. Dev có khoảng không bản ghi dài tới 1,212 s giữa hai file, nên mật độ bản ghi ở mép không loại được một khoảng cỡ đó. Ba thế giới chỉ quét phần bất định đã đưa vào T (khe và phần F ngoài H), không bao bất định ở mép ngoài."
- **`hop-dong.json#/quan_sat/khe_file_toi_da_s` = 10:** hiểu là "khe giữa file: OPEN" (không nối khe vào A0, không loại khe khỏi T^max). Không sửa file hợp đồng.

**Rút hoặc thay câu ở `dinh-chinh-phien8.md`:**

| Chỗ | Câu cũ | Thay bằng |
|---|---|---|
| Đ1, dòng 19, cột "Phân loại đúng" | XÁC NHẬN THIẾU THU (khe dương giữa hai file) | OPEN |
| Đ1, dòng 20 | "Phần chưa biết bị chặn bởi khoảng cách hai bản ghi đầu: ≤ 3,6 ms…"; "sai số không đáng kể" | Rút. Mép ngoài là giả định chưa kiểm, không có cận |
| Đ1, dòng 37–42 (luật v1.1 và câu mới cho đặc tả) | Khe dương nằm ngoài F_s; "sai số ≤ 3,6 ms"; `khe_file_toi_da_s`: 10 → 0 | Thay bằng luật (a) ở trên |
| Đ3, câu mới | "Ở Nezha-OB, ba thế giới trùng P vì trace và log không có phần OPEN." | "Theo (a), ở Nezha-OB, S_lo và S_hi khác P ở 12/22 ca có khe; 4 đơn vị đếm đại diện đổi nhãn giữa ba thế giới. Ở RE2-TT, 5 đơn vị đổi nhãn do phần OPEN ở đầu, cuối cửa sổ." |
| Đ5, dòng 104 | "Lỗi của v1 có tác động thật… Nezha-OB mang sai lệch này." | "Chênh giữa v1 và v1.1 là độ nhạy: 4/1.420 quyết định cổng của đơn vị đếm đại diện Nezha-OB đổi. Không bản nào được coi là sự thật." |
| Đ5, dòng 107 | "Sai số mép ngoài của F trên Nezha-OB (≤ 3,6 ms) nhỏ hơn mức này nhiều lần." | Rút |
| Đ6, dòng 122 | "nếu không, Nezha-OB mang sai lệch ở Đ5" | "Task cài đặt dùng luật (a) theo Q-207" |

**Còn giữ từ phiên 8:** văn bản, hợp đồng và code v1 hiểu luật F theo ba cách khác nhau (Đ1). Đây vẫn là lỗi của bản v1, độc lập với câu hỏi bản nào đúng.

**Kết quả theo (a)** (lượt `runs/khe-open-002`, script `scripts/the_gioi_khe_open.py`; không nhãn; kiểm hash hai đầu vào pha 1 theo manifest trước khi dùng):

| Dataset | Đơn vị đếm đại diện được xét | Phụ thuộc quan sát có sẵn (v1.1) | Phụ thuộc quan sát theo (a) | Phát sinh thêm do khe |
|---|---:|---:|---:|---:|
| RE2-TT | 5.388 | 5 | 5 | 0 |
| Nezha-OB | 1.420 | 0 | 4 | 4 |

- Con trỏ: `runs/khe-open-002/ket-qua.json#/tong_hop`; danh sách đơn vị ở `#/don_vi_phu_thuoc`.
- Bốn đơn vị Nezha-OB đúng là bốn đơn vị lật giữa v1 và v1.1 (`runs/so-v1-v11-004/ket-qua.json#/don_vi_dem_doi_quyet_dinh`).
- Tính đơn điệu theo T_A/T_N chỉ bảo đảm bốn đơn vị lật bị gắn cờ. Việc không có đơn vị nào khác là kết quả đếm trên dữ liệu này, không suy ra từ tính đơn điệu.
- Ví dụ phụ thuộc có sẵn ở RE2-TT (`#/don_vi_phu_thuoc/0`; `ks16/dem-khong-nhan.json#/cases/4/op_rows/66`): 1.184/1.074 sự kiện, nhãn DOWN / NORMAL / DOWN ở P / S_lo / S_hi. Chỉ so hai bản tại thế giới P thì bỏ sót loại phụ thuộc này.
- Lượt `runs/khe-open-001` hỏng và được giữ lại: bản đầu của script ghép thừa tiền tố đường dẫn khi đối chiếu manifest, nên dừng ở bước kiểm hash và không ghi kết quả.
- Thế giới P theo (a) trùng số của v1.1 (`ks16/runs/pha1-002`). Ô kích hoạt, O1–O4 và số T0 của ma trận không đổi (`runs/so-v1-v11-004/ket-qua.json#/pha2_kich_hoat_giong_nhau_moi_ca`).
- Đây là đơn vị đếm đại diện của KS-16, không phải điểm M1.

**Fixture:** B1 (`fixture/fixture-bo-sung.json`).

## Đ10. Ô kích hoạt và cách luật C dùng E_X (Q-207)

**Lý do:**
- Hạng của root là đại lượng tương đối, nên một thành phần có thể đổi hạng root qua điểm của thực thể khác.
- Ví dụ E6b, tính trong bộ nhớ theo đúng đặc tả (lệnh ghi ở LOG phiên 9):
  - điểm A 0,8; R 0,6; B 0,1, với R là root đứng độc lập;
  - thêm cạnh A → B: π = (0,3273; 0,4000; 0,2727), R lên hạng 1;
  - với điểm (0,5; 0,6; 0,55), thêm A → B làm R tụt từ hạng 1 xuống hạng 2.
- Trên dev (tính trong bộ nhớ từ `ks16/dem-khong-nhan.json#/cases/*/call_rows`, `entities`, `metric_rows` và `ks16/dem-sau-ghep-nhan.json#/cases/*/kich_hoat`):
  - 6/30 ca RE2-TT nằm ngoài E_X của E6b, mỗi ca vẫn có 55 cạnh giữa các thực thể khác;
  - 16/22 ca Nezha-OB nằm ngoài E_X của T12, mỗi ca vẫn có cạnh tĩnh mới không chạm root.

**Thay câu trong `dinh-nghia-pha2.json`** (không sửa file):

| Con trỏ | Câu cũ | Câu mới |
|---|---|---|
| `#/nguyen_tac/3` | "Điều kiện ca là điều kiện cần để cơ chế của X có thể đổi hạng root. Không là bằng chứng X sẽ giúp." | "E_X là nhóm ca mục tiêu khai trước. Không là điều kiện cần để hạng root đổi; X có thể đổi hạng root ở ca ngoài E_X. Không là bằng chứng cơ chế, lợi ích hay khả năng chuyển sang FlashTicket." |
| `#/o_kich_hoat/E6b/co_che` | "PageRank chỉ đổi điểm của nút có cạnh (KS-10)" | "PageRank chỉ đổi điểm của nút có cạnh (KS-10); hạng của root vẫn đổi được khi điểm của nút khác đổi" |
| `#/o_kich_hoat/E9/co_che` | "E9 chỉ có việc khi kênh của root có thể bị bên được gọi giải thích (E5)" | "Nhóm nhắm trường hợp kênh lan ngược của root bị bên được gọi giải thích (E5). Nhóm không bao đường qua cạnh đi vào: kênh lan xuôi của root bị bên gọi giải thích (SPEC E5). E9 cũng tác động lên kênh của thực thể khác." |
| `#/o_kich_hoat/T12/co_che` | "phép hợp cạnh chỉ đổi E5, E6b, E7, C-d1, C-d3 khi thêm cạnh chạm root (D8)" | "Phép hợp cạnh dùng ở E5, E6b, E7, C-d1, C-d3 (D8). Nhóm nhắm cạnh tĩnh chạm root; cạnh tĩnh giữa các thực thể khác cũng đổi được hạng root." |

**Cách luật C dùng E_X (Q-207, SPEC không đổi):**
- Kết cục GIÚP đòi ba điều: ΔMRR gộp > δ; P > M trong E_X; không dataset nào có ΔMRR_d < −δ_d.
- P > M trong E_X là yêu cầu ưu tiên lợi ích trong nhóm ca mục tiêu đã khai trước. Đây là chính sách chọn trên dev.
- Tư cách trong hay ngoài nhóm không cho biết lợi ích đúng cơ chế, ngẫu nhiên hay chuyển được sang FlashTicket. Câu hỏi cơ chế xét bằng trung gian từng ca (B4: dấu vết E5 theo ca và kênh). Chuyển giao xét ở P10.
- Ca có ΔMRR gộp > δ nhưng P ≤ M (lợi ích chỉ có ngoài nhóm) đi tới bước 7: TRÁI CHIỀU theo ô, Minh quyết.
- Chiều ngược lại có thể đạt GIÚP: P > M trong nhóm nhưng ngoài nhóm hại nhiều ô hơn (M′ > P′). Phần hại này chỉ vào ΔMRR gộp, ΔMRR_d và các điều kiện HẠI đứng trước (bước 1, 3; với E5 là điều kiện M5 riêng, với E3 là UV-6). Các điều kiện ấy không bảo đảm bắt mọi trường hợp.
- Luôn báo P′, M′ cạnh P, M.
- **Phụ thuộc:**
  - task (1), khối K: chính sách này chỉ đổi được nhãn kết cục và báo xung đột ở bước 8; không đổi cấu hình bị loại hay cấu hình thắng;
  - task (2): quyết định giữ hoặc bỏ ở T6, T9, T11, T12 và việc thay biến thể ở K-b.

## Đ11. Khởi phát của E9 và thứ tự C-d2

**Thay đặc tả v1 §7.11 điểm 3:**
> "Khởi phát chỉ xác định cho đơn vị phân vị: đầu ô 10 giây đầu tiên trong A mà tỷ lệ mẫu vượt ngưỡng hướng d trong ô lớn hơn r_d(N). Đơn vị đếm (tần suất, NEW_OP, STOPPED, log) không có khởi phát. Gọi B(e) là tập mọi đơn vị mà E5 dùng để giải thích kênh e. E9 phủ quyết khi và chỉ khi e có khởi phát, mọi b ∈ B(e) có khởi phát, và khởi phát của e sớm hơn khởi phát của từng b quá 2 ô cộng τ = 1 ms."

**Thay đặc tả v1 §7.11 điểm 6:**
> "e hoặc bất kỳ b ∈ B(e) không có khởi phát thì không phủ quyết. `inherited_by` ghi lý do 'không đủ khởi phát', tách khỏi 'đã xét, không phủ quyết'. Nezha-OB chỉ dùng trace."

Giữ nguyên "tắt trên cạnh có E2 bất thường" (SPEC B2 E9).

**Thay ghi chú C-d2 ở đặc tả v1 §8:** thêm
> "Thực thể xếp theo khởi phát sớm nhất trong các đơn vị phân vị bất thường của nó; cùng khởi phát thì K_raw lớn hơn đứng trước. Thực thể không có khởi phát xếp sau mọi thực thể có khởi phát, hòa theo K_raw."

**Mặt trái:**
- Luật nghiêng về giữ kết luận kế thừa của E5. Lớp lan ngược của bên được gọi gồm cả thao tác mới và log lỗi, đều là đơn vị đếm, nên khi E3 hoặc E3b bật, E9 có thể ít khi phủ quyết.
- Nếu T11 ra KHÔNG TÁC DỤNG, kết quả đó không có nghĩa thứ tự thời gian vô ích.
- C-d2 luôn đặt cuối các thực thể chỉ có bất thường ở kênh đếm.

**Fixture:** B2–B6.

## Đ12. C-d3 suy biến trên Nezha-OB

- **Dữ kiện:** Nezha-OB có 0 span gốc ở 22/22 ca dev, với 32.584 span mồ côi (`ks16/dem-khong-nhan.json#/cases/*/trace/root_spans`, `#/cases/*/trace/orphans`). RE2-TT có span gốc ở 30/30 ca, tổng 81.095.
- **Hệ quả:** theo SPEC B2, ở chế độ (a) đích của C-d3 là thực thể sở hữu span gốc. Trên Nezha-OB không có đích, nên C-d3 trả `NO_TARGET` ở mọi ca.
- **Luật:** áp quy tắc "Suy biến: bỏ, ghi lý do" của bảng ứng viên SPEC.
  - C-d3 chỉ chạy trên RE2-TT.
  - Trên Nezha-OB, C-d3 ghi "suy biến: không có span gốc".
  - Không diễn giải việc M1 hơn C-d3 trên Nezha-OB.
  - Không đổi đích sang chủ của span mồ côi.
  - Tập test có cùng tình trạng không thì chưa biết; không mở.
- **Ghi chú:** số này có sẵn từ lượt pha 1 (phiên 7) nhưng chưa được nêu trước phiên 9.
- **Fixture:** B7.

## Đ13. Số STOPPED ở Đ4 phiên 8

- **Câu cũ:** "22 STOPPED là 11 thao tác của luồng checkout … trong 2 ca, mỗi thao tác n_N = 16."
- **Câu mới:**
  > "22 STOPPED là 11 thao tác của luồng checkout ở mỗi ca trong 2 ca: n_N = 16 ở dev-55f99f3e0a và n_N = 12 ở dev-b0f8b2e3ac, n_A = 0 (`ks16/dem-khong-nhan.json#/cases/39/op_rows`, `#/cases/51/op_rows`). cartservice, checkoutservice và shippingservice vẫn có 703–1.160 span ở A (`#/cases/39/entities`, `#/cases/51/entities`, trường `spans_A`), nên loại được việc mất toàn bộ trace của ba dịch vụ đó; chưa loại được việc mất riêng thao tác hay luồng checkout. emailservice và paymentservice chỉ có đúng thao tác bị ngừng. Nguyên nhân vẫn OPEN."

## Đ14. Câu về file chồng nhau

- **Câu được sửa** (người làm nêu trong chat, chưa ghi vào file nào): "file không chia theo thời điểm sự kiện".
- **Câu đúng:** "58/88 chỗ nối chồng nhau chỉ bác cách chia file thành các khoảng không chồng lấn theo đúng mốc mà F dùng. Ví dụ, file có thể chia theo thời điểm bắt đầu của span, còn F dùng thời điểm kết thúc. Biên thu vẫn chưa xác định được từ bản ghi."

## Đầu ra bị ảnh hưởng

| Đầu ra | Xử lý |
|---|---|
| `dac-ta-phuong-phap-v1.md` §2.2 (2, 4, 7), §7.11 (3, 6), §8 C-d2, C-d3 | Theo Đ9, Đ11, Đ12; không sửa file |
| `hop-dong.json#/quan_sat/khe_file_toi_da_s` | Theo Đ9 |
| `dinh-nghia-pha2.json` | Theo Đ10; tập ô kích hoạt giữ nguyên |
| `ma-tran-thu.json` | Số T0 không đổi. Câu ba thế giới theo Đ3 phiên 8, được Đ9 thay tiếp |
| `dinh-chinh-phien8.md` | Các câu nêu ở Đ9, Đ13 bị thay |
| `why-de-xuat.md` | WHY-M1-03, 08, 09 sửa trong phiên 9 |
| `bao-cao.md` | §2.7, §5, §11, §12 sửa trong phiên 9 |
| Task cài đặt (1), (2), (3) | Dùng luật (a), luật E9 và C-d2 mới, C-d3 chỉ trên RE2-TT, luật C theo Q-207 |
