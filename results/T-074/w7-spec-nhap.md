# T-0xx — W7: đợt đánh giá FlashTicket (NHÁP SPEC)

- **Trạng thái:** NHÁP do người làm T-074 soạn (24/11/2026), chưa duyệt. Mã task do điều phối cấp khi Minh duyệt tạo task. Chưa tạo file trong `tasks/`.
- **Người làm:** Claude. **Người phản biện:** Codex.
- **Thuộc gói MRP:** P10 (và P9b phần đóng gói) — **Cổng:** chuẩn bị G6.
- **Căn cứ thiết kế:** W6 bản 5 (`results/T-074/thiet-ke-w6-5.md` + bảng hiệu lực ở `thiet-ke-w6-4.md` §0), quyết định của Minh: `docs/DECISIONS.md` khối 23–24/11 (A1 K0; B1 phương án A; B2 G = 370 s chính, 120 s phụ, không kéo dài tải; B3–B7; sức chứa giữ 100.000; phương án C), câu hỏi mở W6 (`results/T-074/con-mo-w6.md`, gồm W-5, W-6 là hai giới hạn H5 chính thức). Kế hoạch giai đoạn 2 §8.3 (W7).

## Mục tiêu

- **Nguồn:** DT18-NV3 ("áp dụng thử nghiệm trên hệ thống bán vé … đánh giá bằng các độ đo phù hợp … phân tích các trường hợp hiệu quả hoặc còn hạn chế"); hướng dẫn cô bước 4 (Precision, Recall, F1, MRR, NDCG; so với RCA cơ sở); MRP RQ5 (kết quả có giữ trên hệ khác, lỗi tự tiêm, tải thay đổi) và RQ3a/b/c trên FlashTicket; kế hoạch §8.3 W7 ("thu trước, chạy RCA và baseline sau trên gói đã đóng; chấm sau khi đã băm đầu ra").
- **Loại task:** đánh giá (thu dữ liệu đánh giá mới, chạy phương pháp đã khóa, chấm). Gồm phần code và pilot cần để thu đúng (pha 0–2), có cổng khóa trước khi thu (pha 3).
- **Bao phủ:** 3 ô đánh giá vị trí mới (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE) × 2 mức tải (×1, ×3 cả chu kỳ) × 3 lần lặp + 9 chu kỳ đối chứng; chế độ (a) và (b); D14 (P7 chạy thẳng, V082, V082 che G-live, V082 che G-inst); đối chứng quan hệ (DC-bo-quan-he, C-d1–C-d3); baseline M4 (SimpleRCA) và BARO. Nhóm "đã phát triển": 17 gói T-069, chế độ (a), chỉ tính toán (B7).
- **Không bao phủ (ghi vào hồ sơ G6):** ô cạnh mạng/dữ liệu/cache, lỗi phụ thuộc đích, bù trừ Saga, CPU-EVENT (ứng viên), tải tăng trong ca lỗi; báo động giả mỗi giờ khỏe ×3 (OPEN, B3); vùng ảnh hưởng chỉ "đồ thị con nghi ngờ" (B5 không làm đầu dò endpoint); RQ5 chỉ mô tả theo ô (3 ô).
- **Đạt task cho phép kết luận:** mô tả theo ô/ca/chế độ/mức tải của P7, V082, baseline trên 3 vị trí mới; tác dụng các bước dùng quan hệ trong **xếp hạng** (RQ3d giới hạn §12 bản 4); độ đo phát hiện của luật W4 trên lỗi tiêm. Không cho phép: kết luận tổng quát RQ5, lợi ích của topology thật, độ đúng vùng ảnh hưởng.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn / giải thích khác | Phép kiểm và bằng chứng | Kết quả có thể | Còn thiếu / quyết định phụ thuộc |
|---|---|---|---|---|
| RQ5 "chuyển thẳng" (B1.9, D14) | — | P7 trên 3 ô mới: AC@1/3, Hit@k, MRR, NDCG@5, K theo ô, mức tải, chế độ (bảng diễn giải bản 4 §7); ở (b) giữ ca không có cảnh báo trong mẫu số, báo thêm điểm trên nhóm có cảnh báo (kế hoạch §8.3) | mô tả; không "giữ/tụt" so dev | 3 ô ít; DB trôi (K0) |
| RQ5 "sau thích nghi" | thành phần V082 có kích hoạt không | V082 vs P7 theo ca: cải thiện/giữ/tụt + trung gian (`kenh_co`, khóa, `chet_im`, nối chuỗi) | mô tả | W-5 (H5 không kích hoạt cho thành phần sinh t̂ ở (b)) ghi trạng thái nền H5 mỗi ca |
| Thông tin nào mang thay đổi (D14) | che G-live (`live-down`+`live-ms`), che G-inst (hành vi P7, B4) | V082 vs V082-che theo ca + trung gian | mô tả | G-inst có thể không phân xử (không ca tạo lại container) |
| So baseline (cô bước 4) | M4 + BARO (B6) | theo ca, theo ô; BARO chỉ xếp hạng, K = UNSUPPORTED | mô tả | không baseline trace độc lập |
| RQ3a phát hiện | G1 = 370 s chính, G2 = 120 s phụ | P/R/F1 theo cửa sổ; trùng; độ trễ từ mốc tiêm theo lịch + lệch bộ tiêm (B5); FP/giờ khỏe ×1; sự cố/giờ quan sát ×3 (B3) | số đo trên lỗi tiêm | 7 luật lần đầu kiểm dương |
| RQ3d | DC-bo-quan-he, C-d1–C-d3 | theo ca; trạng thái C-d3 | tác dụng trong xếp hạng | không đối chứng đồ thị ngẫu nhiên |
| Giá của tự phát hiện | (a) vs (b) | cùng phương pháp; nhóm `giay_N_nhiem` (bản 5 §1) | mô tả | — |

## Đầu vào

- Bản ghim FlashTicket `36a3725` (image `arm64-t067-36a3725d`, Keycloak `arm64-776d9c9e`; Id/digest lấy ở E6 bước 7 `results/T-074/e6/khoa-ban.json`, chưa có).
- Repo lab: `main` hiện `1bb40ca` (exp-obs), exp-app `407b4f5`; code W7 trên nhánh mới (worktree `D:/Project/rca-lab-wt/T-0xx`), commit Minh duyệt.
- Bản chụp lõi M1 `b0f79a4d…`; cấu hình V082 (hash ở `results/T-064/cau-hinh-de-xuat.json`); RCAEval `259ea41`; `src/simplerca`, `src/p3`.
- Luật W4 (T-072, commit luật E3), bộ chấm W4 v2 (`results/T-072/v2/cham_offline_v2d.py`, DECISIONS 24/11 mục 2); bộ gom/chụp W5 (T-073, lab `t073-e5*`).
- Trạng thái DB sau E6 (hạn bán 30/12; sức chứa 100.000; mốc `results/T-074/e6/moc-w7.json`, chưa có).
- Dữ liệu dev cho kiểm adapter/suy biến: 17 gói T-069 (`results/T-069/`, manifest), gói T-063.

## Đầu ra

`results/T-0xx/`: `khoa-w7.json` (mọi hash/commit/digest/cấu hình/seed); `lich-w7.json` (3 khối, thứ tự, seed); `pilot/` (xác nhận can thiệp, cường độ, ×3 thực); `quet-suy-bien.json`; `thu/<khối>/` (sổ, gói niêm, manifest); `dong-dot.json` (danh sách gói + sha256, băm trước RCA); `rca/` (đầu ra mọi bản × chế độ, băm); `cham/` (bảng theo §9 bản 2–5); `bao-cao.md`; `thay-doi-may.md`; LOG.

## Phạm vi ghi

`results/T-0xx/`; worktree lab nhánh W7 (code runner/bộ tiêm/adapter/cấu hình che); máy: `/srv/rca-lab/runs/t0xx-*`, `/srv/rca-lab/load-runs/t0xx-*`, `/home/ubuntu/t0xx/` (I9); `LOG.md` và dòng STATE của task. Không sửa lõi M1/V082, luật W4, FlashTicket.

## Các bước (pha; mỗi pha có cổng)

**Phụ thuộc thật (SL32).** Pha 0 chia hai nhóm: 0a (mục 1–3: runner, `inj3`, `chay_d2`) và 0b (mục 4–6: adapter, cấu hình che, bộ chấm). Pha 1 cần 0b; pha 2 cần 0a và khung exp-app không trùng E6, diễn tập. Pha 1 và pha 2 không cần đầu ra của nhau → chạy song song. Pha 0, pha 1 không cần máy app, không chờ E6. Pha 2 xếp sau E6 pha ghi (phương án C: E6 là khung máy đầu tiên; pilot tạo đơn mới, nếu chạy trước E6 thì điều kiện yên của E6 phải kiểm lại). Pha 3 cần Cổng 1, Cổng 2, digest E6 bước 7, seed Minh cấp, WHY. Pha 4 cần Cổng 3. Pha 5 sau đêm cuối; pha 6 sau băm pha 5; pha 7 sau băm pha 6.

**Pha 0 — code (laptop, worktree lab; không máy).** Theo W6 bản 2 §8, bản 4–5:
1. Runner thu–niêm: chụp gói **mọi** chu kỳ đã phát tải (kể cả `fault_ok=False`), trạng thái tiêm ghi riêng; `safe_export case-input`; T1b dùng bộ gom/chụp W5 ở chế độ **chỉ chụp** (stage + gói bổ sung → niêm, không gọi P7/V082/G1); không chạy M1 trong đợt.
2. `inj3`: mục ô SLOW-EVENT (`http.delay` Event), POOL-BOOK (`pool.hold` Booking), TICKET-PAUSE (`docker pause` Ticket); `trang_thai_sach`/`verify` kiểm **mọi** container có thể pause (thêm Ticket); ghi giai đoạn lỗi (trước/sau lệnh tác động) để quy tắc bù ca (bản 5 §5).
3. `chay_d2` nhận mức tải; kiểm hệ số tải thực từ đầu ra k6.
4. Adapter FlashTicket cho M4/BARO (bản 4 §5, bản 5 §4): cắt native nửa mở, lưới 15 s neo t/t̂, hợp nhất alias trước `prepare`, giữ tên chuẩn sau `diagnose`, `LOI_ADAPTER_DA_CHUOI`.
5. Cấu hình V082-che G-live (gói bổ sung đúng schema/mốc, hai kênh `result` rỗng), G-inst (hành vi P7).
6. Bộ chấm W7 (§9 bản 2–5): G1/G2, đoạn K/N/L/D/H, `giay_N_nhiem` hai loại, mẫu số giao phút Grafana đánh giá, ba bảng xếp hạng, mô tả theo ca.
Kiểm bằng: unit test không nhãn; chạy lại cùng kết quả. **Cổng 0:** Minh duyệt commit lab.

**Pha 1 — kiểm trên dev và quét suy biến (SL38; chỉ tính toán, laptop hoặc EC2 theo luật 19).** Trên 17 gói T-069 (+ T-063): mọi bản × (a); đếm và ghi `quet-suy-bien.json`: BARO cột hằng/IQR 0/< 2 mẫu nền, cột rơi ở `drop_constant`/giao; SimpleRCA σ = 0, thiếu modality, `abstain`; V082-che G-live chạy được khi kênh rỗng (bản 3 §E); G-inst ở RECREATE-PAY (lỗi P7 đúng như khai); trạng thái nền H5 (W-5) và chuỗi cổng 8761 (W-6); C-d3 `NO_TARGET`/`UNSUPPORTED_CYCLIC`; mô phỏng (b) bằng t̂ giả định cuối dung sai (A vượt biên) — kiểm bộ chấm. Kèm B7 (đếm khóa thứ hai mẫu nền; phân loại phút 10 phút đầu E4). Mỗi điều kiện suy biến có **quy tắc phân loại khai trước**, tách khỏi vân tay code tính toán (luật 21b). **Cổng 1:** bảng suy biến + quy tắc, Codex soát.

**Pha 2 — pilot xác nhận can thiệp (máy, ban ngày hoặc đầu đêm 1; không RCA).** `chay_d2` cho 3 ô × {×1, ×3}: đầu dò độc lập, cường độ theo điều kiện xác nhận khai trước (T-059), không xem đầu ra RCA; đo `flush_F` và độ trễ bộ chụp ở ×3; kiểm bộ chụp (b) với một tín hiệu dương ngoài khoảng chấm. Trên gói pilot, quét điều kiện suy biến **phía đầu vào** (luật 21c; không chạy phương pháp, không xem hạng): số mẫu nền mỗi kênh, cột hằng/IQR 0, kênh mất khi `docker pause` Ticket, operation mới so với 17 gói dev; thêm quy tắc phân loại nếu gặp điều kiện chưa khai ở pha 1. Gói pilot không vào mẫu đánh giá. **Cổng 2:** ô nào không xác nhận được → không vào lịch (trình Minh).

**Pha 3 — khóa (trước mọi chu kỳ đánh giá).** `khoa-w7.json`: commit lab, digest image (E6 bước 7), cấu hình V082/che/baseline, commit luật W4, bộ chấm (sha256), cường độ ô, lịch + seed, tiêu chí gói hợp lệ, quy tắc suy biến, bảng diễn giải (bản 4 §7). WHY W6 Minh duyệt ghi `docs/WHY.md` (luật 3). **Cổng 3:** Minh duyệt khóa; Codex soát.

**Pha 4 — thu theo khối (đêm; phương án C).** Lịch: 3 khối × 9 chu kỳ (mỗi khối: SLOW-EVENT, POOL-BOOK, TICKET-PAUSE × {×1, ×3} = 6, + BINH-THUONG ×1 ở **vị trí cố định đầu khối** (ô mốc K0), BINH-THUONG-X3, FLASH-HEALTHY), thứ tự trong khối trộn theo seed khai trước (phần còn lại). Mỗi khối ≈ 9 × 31,4 = 4,7 giờ; **một khối mỗi đêm, 3 đêm**. Đầu mỗi đêm: bước 0 chỉ đọc (như `results/T-074/e6/v2/b0-v2.sh`), Prometheus sống, luật W4 đang đánh giá, bộ chụp (b) chạy, kích thước bảng chính. Sau mỗi chu kỳ: kiểm gói hợp lệ (bản 3 §B.1, bản 2 §8.4) và đường thu (bằng chứng độc lập). **Sau đêm 1 (đề xuất, luật 12):** kiểm đóng gói thử trên gói khối 1 — chạy adapter/stage tạo đầu vào cho mọi bản và baseline, **không** chạy phương pháp, không chấm, không ghép nhãn; lỗi đóng gói lộ ra sau 4,7 giờ thu thay vì sau 14,1 giờ. Cuối đêm: trả exp-app, máy tải cho diễn tập (W9a) với điều kiện bàn giao §Rủi ro.

**Pha 5 — đóng đợt.** `dong-dot.json` (mọi gói (a), (b), sự cố giả; sha256), băm danh sách, ghi LOG **trước** RCA.

**Pha 6 — RCA và baseline (batch, không máy app).** Mọi bản (P7, V082, V082-che ×2, DC-bo-quan-he, C-d1–C-d3) × (a), (b) + M4, BARO × (a), (b); D13 chỉ nơi `SUPPORTED` (con-mo W-1). Đầu ra băm. Máy: exp-obs hoặc EC2 (luật 19).

**Pha 7 — chấm.** Ghép nhãn sau băm đầu ra; bảng §9; báo cáo theo ô/ca; giữ kết quả lần đầu; mọi sửa sau xem kết quả báo riêng (C-15 B).

## Kiểm đúng đắn

Phép kiểm không nhãn cho mọi phương pháp (chạy lại trùng; cột/thực thể vào–ra; điểm/hạng dựng lại khớp; BARO không dùng tiêu chí "hạng ≠ thứ tự cột"); đối chiếu P7/V082 trên 17 gói T-069 với đầu ra đã băm (trùng byte); phép thử giả: hai cửa sổ khỏe; soi trung gian ca sai và ca đúng cùng ô (luật 15); tách lỗi hạ tầng khỏi lỗi phương pháp (bằng chứng độc lập); kết quả quá đẹp → kiểm rò nhãn (sổ chỉ bộ chấm đọc).

## Tiêu chí xong

Đợt thu đủ hoặc có lý do (ô thiếu lặp ghi rõ); `dong-dot.json` băm trước RCA; mọi slot (ca × bản × chế độ) có đầu ra hoặc trạng thái lỗi đã phân loại; bảng §9 đủ; báo cáo nêu phạm vi kết luận và phần không bao phủ (§Mục tiêu). Không yêu cầu V082 thắng.

## Không làm

Sửa lõi M1/V082, luật W4 (sửa sau thì báo riêng, kiểm trên khoảng mới); CPU-EVENT, ô hạng B/C; đầu dò onset; LLM (W8 hoãn); khôi phục DB (K0); thêm ô sau khi xem kết quả.

## Chi phí ước lượng (CHƯA-KIỂM; số chu kỳ từ `results/T-074/du-toan-4.json#/phuong_an/0`)

| Pha | Máy | Giờ |
|---|---|---|
| 0 code | laptop | 1,5–3 ngày công (ước) |
| 1 dev + suy biến | laptop/EC2 | 2–4 giờ tính |
| 2 pilot | exp-app, máy tải, exp-obs | ~2 |
| 4 thu | exp-app, máy tải, exp-obs | 14,1 thu + 3 × ~0,5 kiểm đầu đêm ≈ 15,6 (3 đêm) |
| 6 RCA batch | exp-obs/EC2 | ~27 ca × 2 chế độ × ~5 phút cho mọi bản + baseline ≈ 4,5 + sự cố (b) giả. Thời gian mỗi ca **chưa đo** (T-069 không ghi thời gian batch); đo ở pha 1 trên 17 gói, cập nhật khi trình khóa |
| 7 chấm | laptop | 1–2 |

Một lượt > 1 giờ (luật 8): mỗi đêm 4,7 giờ thu → trình Minh khi duyệt khóa. Đơn: 35.640 bảo thủ, vé còn ≈ 58.295 (sức chứa 100.000, E6).

## Lỗi giữa chừng (luật 21; slot = một chu kỳ, khối = một đêm)

| Khi | Loại lỗi | Ảnh hưởng | Xử lý | Chạy lại |
|---|---|---|---|---|
| bất kỳ % | cục bộ một chu kỳ (tiêm không khởi động có bằng chứng phía đích chưa tác động; tải lỗi một lần) | slot đó | bù 1 lần bằng lịch con **cuối khối cùng đêm** (nếu đủ giờ) hoặc đầu đêm sau | 31 phút |
| bất kỳ % | can thiệp chưa xác nhận / mất phản hồi | slot giữ, nhóm riêng | không bù; kiểm sạch đúng container trước chu kỳ kế | 0 |
| bất kỳ % | đường thu hỏng có bằng chứng độc lập | slot không hợp lệ | bù 1 lần như trên | 31 phút |
| 10% đêm (~chu kỳ 1) | nguồn chung (Prometheus khởi động lại, Collector, sai cấu hình) bắt được bởi kiểm mỗi chu kỳ | ≤ 2 chu kỳ | dừng khối, sửa, bù ≤ 2 chu kỳ rồi chạy tiếp 8 chu kỳ còn lại; sửa quá ~1 giờ thì phần còn lại sang đêm sau | ≤ 1 giờ chạy lại; có thể thêm 1 đêm |
| 50% đêm (~chu kỳ 5) | như trên | ≤ 2 chu kỳ | như trên; phần còn lại ~2,4 giờ | ≤ 1 giờ; có thể thêm 1 đêm |
| 99% đêm (chu kỳ 9) | như trên | ≤ 2 chu kỳ | bù đầu đêm sau | ≤ 1 giờ |
| sau đêm 1 (kiểm đóng gói thử) | sai code đóng gói không bắt được bởi kiểm mỗi chu kỳ | khối 1 | dừng; sửa (commit mới, Minh duyệt); chạy lại khối 1 chỉ khi gói mất thông tin không dựng lại được | 4,7 giờ |
| pha 5–7 (≈ 99% đợt) | lỗi đóng gói/thu chỉ lộ khi chạy phương pháp | tới cả đợt | dừng; trình Minh; chạy lại khối/đợt chỉ khi lỗi ảnh hưởng tính đúng | 4,7 giờ/khối, tối đa 14,1 giờ |
| pha 6 | lỗi phương pháp chưa phân loại | slot (ca × bản × chế độ) | thêm quy tắc phân loại không buộc chạy lại slot đã xong | phút tính |
| pha 7 | lỗi chấm | — | chấm lại, đầu ra giữ hash | — |
| máy treo/mất mạng laptop | — | khối đang chạy giao server; mất mạng laptop 0 | khi lại: kiểm tag, sổ, gói; không gọi lại nguyên lịch | lịch con phần thiếu |

## Rủi ro và điều chưa chắc

- **Diễn tập W9a giữa khối dùng chung exp-app:** diễn tập tiêm lỗi (ô dev), tạo đơn, dùng bộ điều phối W5 đầy đủ (P7/V082/G1). Điều kiện bàn giao trước mỗi đêm W7: bước 0 đạt; không tiêm/pause/lease/toxic; bộ điều phối W5 về chế độ **chỉ chụp** W7 (hoặc dừng và bộ chụp W7 chạy) — đổi chế độ là đổi cấu hình/checkout (I7), cần quy định; kích thước bảng ghi lại (diễn tập làm DB tăng, K0 đã chấp nhận, nay thêm nguồn trôi giữa khối).
- Ô chưa được đầu dò xác nhận trên bản ghim (pha 2 có thể loại ô → còn < 3 ô).
- Logic SQL/adapter/che chỉ kiểm ở pha 1 trên dev; chế độ (b) chưa chạy ở ×3.
- Lịch khối trộn trong khối chỉ cân bằng số lần, không bảo đảm vị trí trung bình (con-mo W-3).
- H5 ở (b) (W-5) và tên cổng 8761 (W-6) có thể làm V082 kém vì giới hạn đã biết, không vì phương pháp — báo riêng.
- Khi trễ, cắt theo kế hoạch §8.4: LLM (W8 đã hoãn) → số baseline → số lần lặp; không cắt D14.

## Cần Minh quyết (mỗi mục: đề xuất · lý do · mặt trái)

1. **Một task W7 nhiều pha có cổng, hay tách W7a (code + dev + pilot) và W7b (khóa + thu + RCA + chấm).** Đề xuất: **tách**. Lý do: W7a không dùng dữ liệu đánh giá, chạy song song diễn tập; W7b có phạm vi máy/khóa rõ. Mặt trái: thêm một vòng duyệt SPEC.
2. **Một khối mỗi đêm (3 đêm) hay hai khối đêm đầu.** Đề xuất: **một khối/đêm**. Lý do: 4,7 giờ + kiểm còn dư cho bù slot trong đêm; diễn tập ban ngày. Mặt trái: kéo dài 3 đêm; DB trôi giữa đêm (diễn tập).
3. **Chế độ (b) khi thu:** bộ chụp W5 chế độ "chỉ chụp" (code mới, chạy riêng vùng ghi W7) hay giữ bộ điều phối W5 nguyên trạng và bỏ đầu ra online. Đề xuất: **chỉ chụp**. Lý do: niêm gói trước P7 (bản 5 §3); không tạo ca demo trong đợt đánh giá. Mặt trái: code mới; chuyển chế độ giữa diễn tập và đêm W7.
4. **Điều kiện bàn giao exp-app giữa diễn tập và W7** (Rủi ro mục 1). Đề xuất: bước 0 chỉ đọc + chế độ bộ chụp + ghi kích thước bảng, do điều phối ghi `LICH-MAY.md`. Mặt trái: thêm thao tác mỗi ngày.
5. **Seed lịch:** Minh cấp hạt (như E5). Đề xuất: Minh cấp trước pha 3. Mặt trái: không.
6. **Ghi WHY W6 vào `docs/WHY.md` trước thu** (luật 3): các mục W6-A…N theo bản 2–5. Đề xuất: điều phối gom bản hợp nhất, Minh duyệt ở pha 3. Mặt trái: một bản WHY dài.
7. **Ô không xác nhận được ở pilot:** loại khỏi lịch (còn < 3 ô) hay thêm ô hạng B. Đề xuất: **loại, ghi giới hạn**; không thêm ô sau khi thấy pilot. Mặt trái: RQ5 hẹp hơn nữa.

## Prompt bàn giao

Khi Minh cho phép tạo task, người làm chép prompt theo `docs/review-prompt.md` (khối "Soát SPEC" + G3) vào LOG task mới; lúc này prompt nằm ở LOG T-074 phiên 8.
