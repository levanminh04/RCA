# Đính chính 002 — báo cáo P7(a) main013-v2 (sau phản biện Codex lượt 2)

Ngày 08/11/2026. Claude, người làm phần chạy/chấm/báo cáo T-054. Minh duyệt gói sửa: "Duyệt cả gói".
Không ghi đè `bao-cao.md` hay `dinh-chinh-001.md`. Đính chính này thay các câu nêu dưới đây; phần còn lại giữ nguyên.

Nguồn số: `kiem-toan-ven/so-khoi.json`, tạo bằng lệnh từ gốc repo:
`py -3 -B results/T-054/reports/p7a-013-v2/kiem-toan-ven/so_khoi.py`.
Script chỉ đọc `result.json` đã xác minh (đường dẫn trong `phan-tich-nhom.json#/trung_gian_theo_ca`), không chạy phương pháp.

## Đ6 — "Không đổi hạng" phải ghi rõ đại lượng (Codex lượt 2; N2)

`phan-tich-nhom.json#/doi_top_khi_bo` chỉ so **khối đầu** và **RR của root**, không so cả danh sách khối.
Vì vậy các câu "không đổi hạng", "trùng M1" trong báo cáo chỉ đúng với hai đại lượng đó.

| Cặp | Ca đổi RR root | Ca đổi khối đầu | Ca đổi thứ tự 5 thực thể đầu | Ca đổi cả danh sách khối |
|---|---|---|---|---|
| TT M1 vs bo-E5 | 1/60 | 1/60 | 21/60 | 59/60 |
| OB M1 vs bo-E5 | 0/34 | 0/34 | 7/34 | 7/34 |
| TT M1 vs T12-on | 0/60 | 0/60 | 1/60 | 24/60 |
| OB M1 vs T12-on | 0/34 | 0/34 | 0/34 | 0/34 |
| TT M1 vs bo-E2 | 0/60 | 0/60 | 32/60 | 40/60 |

Cột RR root lấy từ `doi_top_khi_bo`; ba cột sau từ `so-khoi.json#/so_khoi`.

Câu thay thế:

- §0, RQ3d OB: "Bước xếp hạng trên đồ thị (E5) không đổi RR của root và khối đầu ở ca nào; E5 vẫn đổi thứ tự phía dưới ở 7/34 ca."
- §5 dòng 185: "RR của root và khối đầu không đổi ở 94/94 ca; danh sách khối đổi ở 24/60 ca TT, chủ yếu ở vị trí sâu (5 thực thể đầu đổi 1/60)."
- §7.2 dòng 235: "E2 không đổi RR của root ở ca nào (danh sách khối đổi 40/60)."
- §7.4 dòng 264: "bo-E5 trùng M1 về RR root và khối đầu ở 34/34 ca; danh sách khối đổi 7/34."
- §9 dòng 360: "E5 và T12 không đổi RR của root ở 93/94 và 94/94 ca."

Hệ quả: kết luận RQ3d chỉ nói về RR root/khối đầu. Không suy E5/T12 không tác động lên xếp hạng nói chung hay lên vùng nghi ngờ.

## Đ7 — Cơ chế E1×E5 trên TT (§7.3) mạnh hơn bằng chứng (Codex lượt 2; N3)

**Quan sát** (`so-khoi.json#/E1xE5_TT_ca_boE1_doi_RR`), 10 ca bỏ E1 làm RR kém đi:

- `test-327ac2a20e`: kênh op của root không bị E5 giải thích (op_full mạnh nhất F_I = 1). Ca này kém đi vì mất kênh self-time của E1, không do E5.
- 8 ca: kênh op của root bị giải thích bởi **cả** kênh E2 lẫn kênh khác (metric/op của bên được gọi).
- 1 ca (`test-5e8f996191`): chỉ bởi kênh E2.

**Thiếu vế:** ma trận không có E1 tắt + E2 bật + E5 tắt, cũng không có E1 tắt + E2 tắt + E5 bật. Không tách được vai trò E2.

**Câu thay thế cho phần "Suy luận (cơ chế)" §7.3:** "Khi tắt E1, ở 9/10 ca kém đi, E5 giải thích các kênh thời lượng toàn phần của root (lớp lan ngược) bằng kênh của bên được gọi, nên root mất kênh mạnh nhất có F_I. Ở 8/9 ca này, bên giải thích gồm cả kênh E2 và kênh không phải E2. Vai trò riêng của E2 chưa phân xử: nếu bỏ E2 mà các giải thích khác vẫn áp dụng, E2 không cần cho tác dụng phụ này (chưa kiểm; muốn kiểm phải chạy phương pháp trên test). Ca 327a cho thấy E1 cũng thêm thông tin self-time ở một ca."

Câu "E1 trong M1 chủ yếu chặn tác dụng phụ của E2+E5" đổi thành "chủ yếu chặn tác dụng phụ của E5; phần của E2 chưa tách".

## Đ8 — E2-C trên OB network_delay (§7.4): tách cơ chế tính toán và định vị vật lý (Codex lượt 2)

- `src/m1/span.py:156–159`: span bọc là span của bên gọi có đúng một con thuộc dịch vụ khác; `g` = thời lượng span bọc trừ hợp khoảng các con. `g` gồm mạng, xử lý phía client và thời gian trước khi span phía nhận bắt đầu.
- `so-khoi.json#/OB_network_delay_C-a0`: `test-7bb21d627d` (shippingservice) có hai kênh op_full mang F_I ở root ngay trong C-a0 (`QuoteByCount` s 643,7; `CreateQuote…` s 226,1). Đây là phản ví dụ cho câu "span phía nhận của X không dài ra" nếu đọc là đúng mọi ca.

**Câu thay thế cho "Suy luận (cơ chế)" ở mục E2:** "Ở 9/10 ca network_delay, root không có kênh trace F_I nào ở C-a0 (4 ca không kênh F_I, 5 ca chỉ metric); ca 7bb21 có. Không có E2, bên gọi đứng đầu ở 6/8 ca sai. E2-C tính `g` trên cạnh bên gọi → X và gán bằng chứng cho X, tạo kênh không lan rộng 0,898–0,946 ở 7/10 ca. Đây là cơ chế tính toán có trung gian hỗ trợ. `g` không tách được trễ mạng với phía client hay hàng đợi trước span nhận; nếu trễ nằm ở bên gọi, E2-C cũng gán cho mọi bên được gọi. Định vị vật lý của độ trễ chưa phân xử bằng dữ liệu hiện có."

## Trạng thái

- A4 (RQ3b) không đổi.
- RQ3d chỉ còn ở mức RR root/khối đầu; cơ chế E1×E5 (vai trò E2) và định vị trễ của E2-C OPEN.
- C-d3 OB (0/34 dòng mô tả) và TORAI A (174 slot BLOCKED, 2 ca thiếu seed) chờ Minh quyết; không sửa trong đính chính này.
