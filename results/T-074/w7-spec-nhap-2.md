# T-0xx — W7: đợt đánh giá FlashTicket (NHÁP SPEC, bản 2)

- **Trạng thái:** NHÁP, chưa duyệt. Bản 2 = bản 1 (`w7-spec-nhap.md`, hash `SHA256SUMS-9`) sửa theo CX-43 (R1–R8), CX-43b (N1, N2) và tự soát S1–S9 (LOG T-074 phiên 11). Mã task do điều phối cấp khi Minh duyệt. Chưa tạo file trong `tasks/`.
- **Người làm:** Claude. **Người phản biện:** Codex.
- **Thuộc gói MRP:** P10 (P9b phần đóng gói) — **Cổng:** chuẩn bị G6.
- **Cấu trúc đề xuất (Minh quyết, mục Q1):** hai task. **W7a** = pha 0–3 (code, kiểm dev, pilot, khóa); **W7b** = pha 4–7 (thu đêm, đóng đợt, RCA batch, chấm). Nếu Minh chọn một task, giữ nguyên các pha và cổng.
- **Căn cứ:** W6 bản 5 (+ §0 bản 4); DECISIONS 23–24/11 (K0; B1 phương án A; B2 G = 370 s chính, 120 s phụ, không kéo dài tải; sức chứa 100.000; bộ chấm W4 v2d khi lưới đủ, lưới khuyết "chưa phân xử" đếm riêng; phương án C); câu hỏi mở `con-mo-w6.md` (W-1…W-6); kế hoạch giai đoạn 2 §8.3–8.4.

## Mục tiêu

- **Nguồn:** DT18-NV3 (thử nghiệm trên hệ bán vé, độ đo phù hợp, phân tích trường hợp hiệu quả/hạn chế); hướng dẫn cô bước 4 (Precision, Recall, F1, MRR, NDCG; so RCA cơ sở); MRP RQ5, RQ3a/b/c; kế hoạch §8.3 W7 (thu trước, RCA và baseline sau trên gói đã đóng, chấm sau khi băm đầu ra).
- **Loại task:** đánh giá; kèm code và pilot cần để thu đúng.
- **Bao phủ:** 3 ô (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE) × {×1, ×3} × 3 lặp + 9 chu kỳ đối chứng (phương án A); chế độ (a), (b); D14 (P7, V082, V082-che G-live, V082-che G-inst); DC-bo-quan-he, C-d1–C-d3; M4, BARO.
- **Không bao phủ (ghi hồ sơ G6):** ô mạng/dữ liệu/cache, lỗi phụ thuộc đích, bù trừ Saga, CPU-EVENT, tải tăng trong ca lỗi; báo động giả mỗi giờ khỏe ×3 (OPEN, B3; ×3 chỉ có giờ quan sát đủ điều kiện, không có nhãn giờ khỏe độc lập); vùng ảnh hưởng chỉ "đồ thị con nghi ngờ" (RQ3c: chưa có cặp dự đoán–nhãn cùng cấp endpoint; phương án phân tích offline `raw.json` T-069 ước 0,5–1 ngày, chưa đo, chỉ làm nếu Minh cần cho G6); RQ5 chỉ mô tả theo ô; K0 cùng diễn tập không tách được trôi do DB với thời điểm/tải nền.
- **Đạt task cho phép kết luận:** mô tả theo ô/ca/chế độ/mức tải của P7, V082, baseline; **tác dụng gộp của các bước dùng quan hệ lên hạng cuối** (R7: DC-bo-quan-he đổi đặc trưng `op_excl`→`op_full`, bỏ đơn vị cạnh trước khi tạo cờ, rồi đổi lan truyền và khóa hạng; chênh có thể xuất hiện từ đặc trưng, cờ, tập thực thể có bằng chứng — không tách được từng bước); C-d1 (cạnh gọi), C-d2 (khởi phát), C-d3 (đích, đường có hướng; `NO_TARGET`/`UNSUPPORTED_CYCLIC` báo riêng); độ đo phát hiện của luật W4 trên lỗi tiêm. **Không** cho phép: kết luận tổng quát RQ5; lợi ích của cấu trúc phụ thuộc thật (không có đối chứng đồ thị ngẫu nhiên); độ đúng vùng ảnh hưởng.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn / giải thích khác | Phép kiểm và bằng chứng | Kết quả có thể | Còn thiếu / quyết định phụ thuộc |
|---|---|---|---|---|
| RQ5 "chuyển thẳng" (B1.9, D14) | — | P7 trên 3 ô: AC@1/3, Hit@k, MRR, NDCG@5, K theo ô, mức tải, chế độ; (b) giữ ca không cảnh báo trong mẫu số, báo thêm nhóm có cảnh báo | mô tả | 3 ô; DB trôi (K0) |
| RQ5 "sau thích nghi" | thành phần V082 có kích hoạt không | V082 vs P7 theo ca + trung gian; **H5:** ghi theo thực thể, từng ca, cả (a) và (b), kể cả ca hạng đúng: số mẫu `live-down` khác 0 trong N, chuỗi A, thời lượng, kết quả `_chet_im` (R7) | mô tả | chỉ quy đổi hạng cho H5 khi có chuỗi tín hiệu → khóa trước/sau H5; W-5 (E5: H5 không kích hoạt vì N đã chứa mẫu lỗi đầu dò — nhận định của **ca E5**, không phải thuộc tính của (b)); W-6 tên cổng 8761 chỉ có hệ quả khi thực thể đó thỏa điều kiện chết im và tên không khớp lúc áp hạng |
| Thông tin nào mang thay đổi (D14) | che G-live, che G-inst | V082 vs V082-che theo ca + trung gian | mô tả | G-inst có thể không phân xử |
| So baseline (cô bước 4) | M4 + BARO | theo ca, theo ô; BARO chỉ xếp hạng, K = UNSUPPORTED; D13 của M4 chỉ khi dựng riêng N′ và giữ A gốc (W-4) | mô tả | không baseline trace độc lập |
| RQ3a phát hiện | G1 = 370 s, G2 = 120 s | v2d trên lưới đủ; lưới khuyết "chưa phân xử" đếm riêng (R5); P/R/F1, trùng, độ trễ theo mốc tiêm + lệch bộ tiêm; FP/giờ khỏe ×1 trong đợt chỉ mô tả (R5 chính thức vẫn từ E4); ×3: sự cố/giờ quan sát | số đo trên lỗi tiêm | 7 luật lần đầu kiểm dương |
| RQ3d | DC-bo-quan-he, C-d1–C-d3 | theo ca | tác dụng **gộp** lên hạng cuối | không đối chứng đồ thị ngẫu nhiên |
| Giá của tự phát hiện | (a) vs (b) | cùng phương pháp; nhóm `giay_N_nhiem` | mô tả | — |

## Đầu vào

- Bản ghim FlashTicket `36a3725` (image `arm64-t067-36a3725d`, Keycloak `arm64-776d9c9e`); Id/digest từ E6 bước 7 (`results/T-074/e6/khoa-ban.json`, chưa có).
- **Revision lab (R3):** gốc nhánh W7 = `main` laptop `4b6c4b2` (= `1bb40ca` + chỉ `README.md`); exp-obs `1bb40ca`, exp-app `407b4f5` (đọc ở `results/T-074/e6/b0-*.out`, kiểm lại ở bước 0 mỗi đêm). Commit W7 (chưa có) là revision triển khai lên **cả hai** máy; Minh duyệt ở Cổng 0.
- Bản chụp lõi M1, cấu hình V082 (`results/T-064/cau-hinh-de-xuat.json`), RCAEval `259ea41`, `src/simplerca`, `src/p3`.
- Luật W4 (T-072), bộ chấm v2d (`results/T-072/v2/cham_offline_v2d.py`), quy tắc gom `results/T-072/quy-tac-gom.json`; bộ gom/chụp W5 (`campaigns/online/`).
- Trạng thái DB sau E6 (hạn bán 30/12; sức chứa 100.000; mốc `results/T-074/e6/moc-w7.json`, chưa có).
- Dữ liệu dev: 17 gói T-069 (`results/T-069/`, manifest; `bang-theo-o-2.json`), gói T-063; thời gian V082 cũ `results/T-069/thu/t069-chinh/chay/nhat-ky-3.jsonl` (`msg == "V082 xong"`: 16 bản ghi, trung bình 49,92 s cho hai lần V082 mỗi ca).

## Đầu ra

`results/T-0xx/`: `khoa-w7.json`; `lich-w7.json`; `pilot/`; `quet-suy-bien.json`; `thu/<khối>/` (sổ, gói niêm, manifest); `dong-dot.json` (băm trước RCA); `rca/`; `cham/` (bảng §9 W6 bản 2–5 + bảng lưới khuyết + bảng ghép sự cố); `bao-cao.md`; `thay-doi-may.md`; LOG.

## Phạm vi ghi (R3, S1 — trình Minh duyệt từng dòng, mục Q4)

| Nơi | Đích ghi / thao tác | Tài khoản | Ghi chú |
|---|---|---|---|
| laptop | `results/T-0xx/`; worktree lab nhánh W7; LOG, dòng STATE | — | |
| exp-obs | `/opt/rca-lab` → commit W7 (git checkout) | ubuntu | đổi revision là thao tác máy; mỗi đêm kiểm HEAD |
| exp-obs | `/srv/rca-lab/runs/<tiền tố W7>-*` (runner hiện cứng `t3-`, `d2b-`: pha 0 cho cấu hình tiền tố `w7-`/`w7p-`; nếu không đổi được thì ghi đúng tiền tố cứng) | rca | |
| exp-obs | `/srv/rca-lab/ledger/<tag>.jsonl` (sổ tiêm) | **ledger** (qua `sudo -u ledger ledger_append.py`) | tiến trình RCA không đọc được sổ; chỉ bộ chấm đọc sau băm |
| exp-obs | vùng gói bổ sung `RCA_M1_ROOT/bo-sung/` của bộ chụp → đặt `RCA_M1_ROOT` riêng W7 (`/srv/rca-lab/w7/m1`) nếu code cho phép | rca | |
| exp-obs | Grafana provisioning: thêm contact point/route gửi luật W4 tới bộ nhận W7 (R2); gỡ sau đợt | ubuntu (file provisioning, khởi động lại Grafana) | đổi cấu hình nhận cảnh báo |
| exp-obs | spool `canh-bao-*.jsonl` của bộ nhận W7; trạng thái bộ gom/chụp W7 | rca | |
| exp-app | `/home/ubuntu/t063/inj/` (trạng thái bộ tiêm, deadline/pid); lease điều khiển hook Event/Booking (`rca-faults/<svc>/`) | ubuntu/sudo | |
| exp-app | tác động: `docker pause/unpause` Ticket; hook `pool.hold` Booking, `http.delay` Event | ubuntu | |
| exp-app | DB nghiệp vụ: đơn mới do tải (K0) | — | |
| máy tải | `/srv/rca-lab/load-runs/<tag>`; container `rca-tai-*` (k6) | qua khóa bộ điều khiển | |

Không sửa lõi M1/V082, luật W4, FlashTicket. Chủ khung mỗi đêm ghi ở `LICH-MAY.md` (điều phối).

## Các bước

**Phụ thuộc thật.** 0a (đầu dò, runner, bộ tiêm, tải) → pha 2. 0b (adapter, che, bộ chấm, đường nhận (b)) → pha 1 và phần (b) của pha 2. Pha 1 ∥ pha 2 (D2). Pha 2 sau E6 pha ghi. Pha 3 cần Cổng 1, 2, digest E6, seed, WHY. Pha 4 cần Cổng 3.

**Pha 0a — đầu dò và thu (laptop, worktree lab).**
1. **Đầu dò đúng đích từng ô (R1).** Mỗi ô một hàm đầu dò, trường xác nhận khai trước (theo `results/T-059/danh-muc-loi.md`), không gọi HTTP ứng dụng:
   - POOL-BOOK (T-059 dòng 146): pool kết nối **Booking** đầy và có request chờ — đọc chỉ số Hikari của Booking (`active = max`, `pending > 0`) tại +45/+140 s, `pending = 0` sau +30 s; nguồn chỉ số (Prometheus đã scrape hay actuator trong container) xác định ở pha 0 trên `36a3725` (**chưa kiểm** tên chỉ số).
   - TICKET-PAUSE (dòng 210): `State.Paused` Ticket = true lúc tác động, false sau; hàng đợi Ticket tiêu thụ: `consumers`, `messages_ready`/backlog tăng khi pause và về 0 sau phục hồi, ACK tiếp tục (`rabbitmqctl list_queues name messages_ready messages_unacknowledged consumers` cho queue của Ticket).
   - SLOW-EVENT (dòng 274): bản ghi thực thi hook `http.delay` của Event + thời gian chờ trên **đúng request** bị trễ, đối chiếu phía origin (Event) với gateway.
   - Giữ đầu dò chung cũ (toxics, cgroup, PSI, RTT).
2. Runner thu–niêm: chụp gói **mọi** chu kỳ đã phát tải (kể cả `fault_ok=False`), trạng thái tiêm ghi riêng, `safe_export case-input`; tiền tố tag cấu hình được (R3).
3. `inj3`: ô SLOW-EVENT, POOL-BOOK, TICKET-PAUSE; kiểm sạch **mọi** container có thể pause (thêm Ticket); ghi giai đoạn lỗi.
4. Tải: `runner4.start_load` nhận ×3 cố định; **kiểm tải thực bằng nhịp bắt đầu hành trình và `dropped_iterations`** (không dùng số HTTP hoàn tất, vì can thiệp làm giảm số này) (R1).

**Pha 0b — tính toán và (b).**
5. Adapter M4/BARO (bản 4 §5, bản 5 §4); D13 của M4 chỉ với N′ dựng riêng, A gốc giữ (W-4).
6. Cấu hình V082-che G-live, G-inst.
7. **Đường (b) chế độ chỉ chụp (R2):** luật W4 thật → contact point W7 → bộ nhận W7 ghi spool `canh-bao-*.jsonl` (định dạng có `seq` mà `incidents.py` đọc) → bộ gom W5 (`incidents.py`, giữ quy tắc của nó) → bộ chụp **chỉ chụp** (stage + gói bổ sung → niêm; không gọi P7/V082/G1) → hai gói niêm trong vùng W7. Ghi mã sự cố W5 và `t̂` đã dùng cho từng gói.
8. **Bộ chấm W7 (R5, N1):**
   - Phát hiện: gọi logic v2d (import hàm, không sửa file v2d) trên phần lưới đủ; ghi vào `results/T-0xx/cham/` (CLI v2d từ chối `--ra` ngoài `v2/ra/`). Khóa nguồn mỗi đêm: lịch sử đánh giá Grafana (phút luật thực sự được đánh giá), chuỗi xuất, phạm vi. Lưới khuyết: số bước/phút, kết luận "chưa phân xử", bảng riêng (DECISIONS 24/11 mục 2). Không dùng v2e trừ khi Minh duyệt riêng.
   - Ba nhóm ca tách riêng: **không cảnh báo** (bỏ sót); **có Alerting trong lịch sử Grafana nhưng thiếu gói** (giao nhận/chụp hỏng — không tính là bỏ sót của luật); **thiếu bằng chứng Grafana** (chưa phân xử).
   - **Nguồn sự cố cho từng bảng (N1):** Recall/Precision/báo trùng/độ trễ dùng sự cố gom offline theo `quy-tac-gom.json` (T-072; sắp theo giờ bắt đầu). Xếp hạng (b) dùng gói của sự cố W5 (đã chụp theo `t̂` của W5). Ghi bảng ghép một–nhiều sự cố T-072 ↔ sự cố W5. Với một chu kỳ lỗi có nhiều gói W5 trong cửa sổ ghép: hạng chính lấy gói có `t̂` sớm nhất trong `[t, t+600+G)`; các gói còn lại báo "gói trùng" riêng (khai trước, chưa xem kết quả).
   - Xếp hạng: ba bảng (nhãn thật, tập nút chấp nhận, định vị cạnh — `UNSUPPORTED` cho V082), mô tả theo ca.
Kiểm: unit test không nhãn; chạy lại cùng kết quả. **Cổng 0:** Minh duyệt commit lab W7 (revision ghi ở `khoa-w7.json`).

**Pha 1 — dev và quét suy biến (chỉ tính toán; laptop/EC2 theo luật 19).** Trên 17 gói T-069 (+ T-063), mọi bản × (a):
- **Hồi quy (R6):** so byte bản ghi phương pháp **có hash** (P7 16 ô `OK`, V082 17 ô) với đầu ra đã băm; RECREATE-PAY P7 (`#/hang/16/moi/P7/status = ERROR`, `loi-chay.json`): so đúng bước lỗi, loại lỗi, cách tính trượt. BARO: dựng lại điểm từng cột (RobustScaler, max), kiểm thứ tự và hòa với `ranks` chính thức (API chỉ trả `node_names`, `ranks`). Dùng lại kết quả đã khớp; chỉ chạy lại đường dựng đầu vào/adapter mới.
- Quét suy biến (SL38) như bản 1 + đếm theo thực thể điều kiện H5 (R7). Quy tắc phân loại khai trước, tách khỏi vân tay code tính toán (luật 21b).
- **Đo thời gian (R8):** mọi bản × baseline trên 17 gói, ghi thời gian từng bước từ đầu; V082 dùng lại số cũ (≈ 25 s/lần).
**Cổng 1:** bảng suy biến + quy tắc + thời gian, Codex soát.

**Pha 2 — pilot (máy; không RCA).** Hai phần:
- **2a D2 ngắn (chọn cường độ, xác nhận can thiệp):** `chay_d2` 3 ô × {×1, ×3} với đầu dò mới; ước 2 × (180 + 260 × 3 + 60) s ≈ 34 phút.
- **2b chu kỳ đủ (kiểm thu, không chọn cường độ):** ít nhất 1 chu kỳ W7 đầy đủ ×3 (nền 300 s, tải 1800 s, đuôi) với đường (b) bật; một **tín hiệu dương** ngoài khoảng chấm để chứng minh đường luật → spool → gom → hai gói niêm (R2). Đo: `flush_F`, độ trễ bộ chụp, **thời gian đuôi** từ hết tải tới gói cuối niêm (R4), độ phủ, suy biến phía đầu vào. ≈ 31,4 + đuôi (~10–15) phút mỗi chu kỳ (CHƯA-KIỂM).
- Quét suy biến phía đầu vào trên gói pilot; gói pilot không vào mẫu đánh giá.
- **Cổng 2:** bảng xác nhận từng ô. Ô chỉ đề nghị **loại** khi đầu dò đúng đích đã hoạt động mà can thiệp vẫn không xác nhận được; nếu nguyên nhân là thiếu/sai đầu dò → ô ở trạng thái "chưa đo được", trình chi phí sửa đầu dò trước khi thu hẹp A (mục Q8).

**Pha 3 — khóa.** `khoa-w7.json`: commit lab, digest, cấu hình V082/che/baseline, luật W4, bộ chấm (sha256), nguồn sự cố từng bảng, cường độ, lịch + seed, tiêu chí gói hợp lệ, quy tắc suy biến, bảng diễn giải, **ngưỡng vé**, **trần bù**, **mốc đóng khoảng nhận sự cố của khối**, **quy tắc phiên bản khi sửa sau khối 1** (dưới). WHY ghi `docs/WHY.md` (luật 3) bằng bản có hiệu lực: bỏ lý do "trộn làm vị trí trung bình bằng nhau" (trộn chỉ cân bằng số lần; một ô có thể đứng cuối cả ba đêm), bỏ tiêu chí "khác P7 nghĩa là còn dẫn xuất". **Cổng 3:** Minh duyệt khóa; Codex soát. Quyền phát lượt > 1 giờ (luật 8) xin cùng lúc cho: mỗi đêm thu, pilot 2b nếu > 1 giờ, RCA batch.

**Pha 4 — thu theo khối (đêm; phương án C).**
- Lịch: 3 khối × 9 chu kỳ (6 lỗi + BINH-THUONG ×1 **cố định đầu khối** + BINH-THUONG-X3 + FLASH-HEALTHY), thứ tự còn lại trộn theo seed. Một khối mỗi đêm (Q2).
- **Đầu đêm, theo thứ tự (R4):** (1) bước 0 chỉ đọc, bộ lọc tiến trình cấm gồm `orchestrator` → phải sạch; (2) kiểm HEAD hai máy = commit W7, Grafana đánh giá luật, contact point W7 có; (3) **sau đó** khởi động bộ nhận + bộ gom/chụp W7 và xác nhận sống; (4) đếm `purchased`/`held`: vé còn ≥ nhu cầu đêm (4 × 648 + 4 × 1.944 + 1.512 = 11.880 đơn bảo thủ; `du-toan-4.json` dòng 16–24) + dự phòng 1 chu kỳ ×3 (1.944), nếu không → không phát đêm, trình Minh (S2).
- Sau mỗi chu kỳ: kiểm gói hợp lệ và đường thu (bằng chứng độc lập).
- **Cuối khối (R4):** đóng khoảng nhận sự cố của khối tại mốc khai trước = hết tải chu kỳ cuối (S₉ + 1800 s); cảnh báo đang cháy vắt biên ghi trạng thái; chờ mọi gói thuộc khối **niêm xong hoặc có trạng thái lỗi xác định** (đuôi đo ở pilot 2b; với cảnh báo sát biên G1, bộ chụp bắt đầu gần S + 2320 s ≈ 520 s sau hết tải, chưa gồm hàng chờ và thời gian xuất). Rồi mới dừng bộ chụp W7 và bàn giao.
- **Bàn giao theo máy:** máy tải trả ngay sau khi tải chu kỳ cuối dừng và kiểm sạch; exp-app sau khi bộ tiêm sạch (không pause/lease/toxic); exp-obs sau khi gói khối niêm xong và bộ W7 dừng. Ghi kích thước bảng chính để mô tả K0.
- **Sau đêm 1:** kiểm đóng gói thử trên gói khối 1 (dựng đầu vào mọi bản/baseline, không chạy phương pháp, không chấm). Nếu lỗi đóng gói: **ưu tiên dựng lại từ gói đã niêm**; chỉ thu lại khi thông tin không có trong gói niêm.
- **Quy tắc phiên bản (R4, W6 bản 2 §1):** sửa sau khối 1 chỉ ở phần **đóng gói/dựng đầu vào** mà gói niêm còn đủ thông tin → dựng lại khối 1, cùng phiên bản. Sửa ảnh hưởng **cái được thu** (tiêm, tải, đường (b), mục đã khóa) → khối trước và sau là hai phiên bản; báo riêng, chỉ so trong cùng phiên bản; thu lại đúng số khối bị ảnh hưởng nếu Minh duyệt.

**Pha 5 — đóng đợt.** `dong-dot.json` (mọi gói (a), (b), sự cố giả; sha256) băm, ghi LOG **trước** RCA.

**Pha 6 — RCA và baseline (batch).** Mọi bản × (a), (b) + M4, BARO; D13 chỉ nơi `SUPPORTED` (W-1, W-4). Ghi trung gian H5 theo thực thể (R7). Đầu ra băm. Máy: exp-obs hoặc EC2 (luật 19).

**Pha 7 — chấm.** Ghép nhãn sau băm đầu ra; bảng theo pha 0b mục 8; giữ kết quả lần đầu (C-15 B).

## Kiểm đúng đắn

Như bản 1, thay "đối chiếu trùng byte trên 17 gói" bằng tiêu chí R6 (pha 1). Phép thử giả: hai cửa sổ khỏe; soi trung gian ca sai và ca đúng cùng ô (luật 15); tách lỗi hạ tầng/giao nhận khỏi lỗi phương pháp; kết quả quá đẹp → kiểm rò nhãn.

## Tiêu chí xong (S4)

- Mỗi ô × mức tải có **≥ 2/3 lặp hợp lệ** thì báo kết quả ô đó; ít hơn → "thiếu", ghi lý do và giới hạn, không gộp.
- `dong-dot.json` băm trước RCA; mọi slot (ca × bản × chế độ) có đầu ra hoặc trạng thái lỗi đã phân loại; bảng phát hiện có phần lưới đủ và phần "chưa phân xử" riêng; bảng ghép sự cố T-072 ↔ W5.
- Báo cáo nêu phạm vi kết luận, phần không bao phủ, phiên bản (nếu có hai). Không yêu cầu V082 thắng.

## Không làm

Sửa lõi M1/V082, luật W4; CPU-EVENT, ô hạng B/C; đầu dò onset; LLM (W8 hoãn); khôi phục DB (K0); thêm ô sau khi xem kết quả; dùng v2e khi chưa được duyệt.

## Chi phí ước lượng (CHƯA-KIỂM trừ chỗ ghi nguồn)

| Pha | Máy | Giờ |
|---|---|---|
| 0 code | laptop | 2–4 ngày công (thêm đầu dò, đường (b), bộ chấm) |
| 1 dev + suy biến + đo thời gian | laptop/EC2 | 2–4 |
| 2a D2 | exp-app, máy tải, exp-obs | ≈ 0,6 |
| 2b chu kỳ đủ (1–3 chu kỳ) | như trên | 0,7–2,3 |
| 4 thu | như trên | 14,1 (`du-toan-4.json#/phuong_an/0/gio_thu_co_so`) + 3 × (0,5 đầu đêm + đuôi đo ở 2b, ước 0,2–0,3) ≈ 16–16,5 trong 3 đêm |
| 4 bù | như trên | ≤ 3 × 0,52 + đuôi (trần, S3) |
| 6 RCA batch | exp-obs/EC2 | V082: ≈ 25 s/lần (T-069); phần khác đo ở pha 1. Số slot (b) phụ thuộc số sự cố thực (gồm báo giả, bỏ sót) |
| 7 chấm | laptop | 1–2 |

**Vé (R8, S2):** 58.295 là tồn ở **pha đọc E6** (`100.000 − 41.705`, `results/T-074/e6/gia-tri-dich.json`); đọc lại ở E6 pha ghi và đầu W7a. Nhu cầu (đơn bảo thủ/chu kỳ: ×1 648, ×3 1.944, flash 1.512 — `du-toan-4.json`): thu 35.640 (`#/phuong_an/0/K0_don_ca_dot_bao_thu`); pilot 2a ≈ 1.020 s ở ×1 + 1.020 s ở ×3 theo nhịp 648 và 1.944 đơn/1.800 s ≈ 370 + 1.100 ≈ 1.470 (ước); 2b ≈ 1.944/chu kỳ, 1–3 chu kỳ; bù ≤ 3 × 1.944; diễn tập W9a (chưa ước — điều phối cung cấp). Tổng không kể diễn tập ≈ 35.640 + 1.470 + 1.944–5.832 + ≤ 5.832 ≈ 39.100–48.800 < 58.295; dư ≈ 9.500–19.200 cho diễn tập. Nếu vượt → Minh quyết (giảm pilot/bù, hoặc nâng sức chứa — đổi quyết định 24/11).

## Lỗi giữa chừng (luật 21; slot = một chu kỳ, khối = một đêm)

| Khi | Loại lỗi | Ảnh hưởng | Xử lý | Chạy lại / mất |
|---|---|---|---|---|
| bất kỳ % | cục bộ một chu kỳ (tiêm không khởi động có bằng chứng phía đích; tải lỗi một lần; đường thu hỏng có bằng chứng độc lập) | slot đó | bù 1 lần, **ở cuối đợt** (sau khối 3; N2, Q5); tổng ≤ 3 bù/đợt (S3), quá → dừng, trình Minh | 31 phút + đuôi mỗi bù |
| bất kỳ % | can thiệp chưa xác nhận / mất phản hồi | slot giữ, nhóm riêng | không bù; kiểm sạch đúng container trước chu kỳ kế | 0 |
| bất kỳ % | Grafana có Alerting nhưng thiếu gói (giao nhận/chụp) | slot (b) của ca đó | nhóm "giao nhận hỏng"; sửa đường nhận trước chu kỳ kế; (a) vẫn dùng | 0 thu; sửa |
| 10% / 50% / 99% đêm | nguồn chung (Prometheus, Collector, cấu hình) bắt bởi kiểm mỗi chu kỳ | ≤ 2 chu kỳ | dừng khối, sửa, chạy tiếp phần còn lại; ≤ 2 chu kỳ hỏng vào danh sách bù cuối đợt; sửa quá ~1 giờ → phần còn lại sang đêm sau | ≤ 1 giờ bù; có thể +1 đêm |
| sau đêm 1 | lỗi đóng gói (kiểm đóng gói thử) | khối 1 | dựng lại từ gói niêm; thu lại chỉ khi thiếu thông tin (quy tắc phiên bản) | 0 hoặc 4,7 + đuôi |
| pha 5–7 | lỗi chỉ lộ khi chạy phương pháp | tới cả đợt | như trên; trình Minh trước khi thu lại | tới 14,1 + đuôi |
| pha 6 | lỗi phương pháp chưa phân loại | slot (ca × bản × chế độ) | thêm quy tắc không buộc chạy lại slot đã xong | phút |
| pha 7 | lỗi chấm | — | chấm lại; đầu ra giữ hash | — |
| máy treo/mất mạng laptop | — | khối đang chạy trên server | khi lại: kiểm tag, sổ, gói; lịch con phần thiếu | lịch con |

## Rủi ro và điều chưa chắc

- Đầu dò mới (tên chỉ số Hikari, queue Ticket, request Event) **chưa kiểm** trên `36a3725`.
- Đường (b) W7 là đường mới (contact point, bộ nhận ghi spool) — chỉ chứng minh ở pilot 2b.
- Diễn tập W9a dùng chung exp-app/exp-obs: đổi bộ điều phối W5 đầy đủ ↔ W7 chỉ chụp là đổi cấu hình/checkout (I7); DB tăng thêm giữa đêm (K0).
- Trộn khối chỉ cân bằng số lần, không cân bằng vị trí (W-3).
- Ngân sách vé: dư 9.500–19.200 đơn cho diễn tập (mục Chi phí); diễn tập chưa ước.
- Khi trễ (kế hoạch §8.4): LLM (đã hoãn) → số baseline → số lần lặp; không cắt D14.

## Cần Minh quyết (mỗi mục: đề xuất · lý do · mặt trái)

1. **Tách W7a/W7b.** Đề xuất: tách. Lý do: R1–R3 quyết định pilot có tạo đúng bằng chứng hay không; W7a không dùng dữ liệu đánh giá. Mặt trái: thêm một lần duyệt SPEC.
2. **Một khối mỗi đêm.** Đề xuất: có. Lý do: 4,7 giờ thu + đầu đêm + đuôi (R4) ≈ 5,5 giờ; đường nhận/chụp còn mới. Mặt trái: 3 đêm (+1 nếu bù), DB trôi giữa đêm.
3. **(b) chế độ chỉ chụp với đường nhận W7 mới (R2).** Đề xuất: có. Lý do: niêm gói trước P7; không tạo ca demo trong đợt. Mặt trái: code + đổi cấu hình Grafana; phải chứng minh ở pilot 2b.
4. **Phạm vi ghi trên máy (bảng Phạm vi ghi).** Đề xuất: duyệt từng dòng; sổ giữ user `ledger`; đổi tiền tố và `RCA_M1_ROOT` riêng nếu code cho phép. Mặt trái: thêm việc pha 0.
5. **Vị trí bù (N2).** Đề xuất: **cuối đợt** (sau khối 3) như W6 bản 2 §8.4. Lý do: ô mốc K0 đầu mỗi khối không nhận DB/dư âm của ca bù. Mặt trái: có thể thêm một đêm ngắn. Nếu Minh chọn bù sớm để tiết kiệm đêm: chốt vị trí cụ thể và ghi giới hạn khi so ba ô mốc.
6. **Seed:** Minh cấp trước pha 3.
7. **WHY W6 trước thu:** điều phối gom bản có hiệu lực (bỏ hai lý do đã sai ở pha 3), Minh duyệt ở Cổng 3.
8. **Ô không xác nhận ở pilot.** Đề xuất: loại chỉ khi đầu dò đúng đích hoạt động mà can thiệp vẫn không xác nhận; thiếu đầu dò → "chưa đo được", trình chi phí sửa. Không thêm ô hạng B (đổi hạ tầng và phạm vi đã chọn). Mặt trái: có thể trễ thu.
9. **Nguồn sự cố từng bảng (N1).** Đề xuất: phát hiện theo gom T-072; xếp hạng (b) theo gói W5, gói sớm nhất là chính, bảng ghép một–nhiều. Mặt trái: hai số "sự cố" cùng tồn tại, phải giải thích trong báo cáo.
10. **Trần bù (≤ 3/đợt) và ngưỡng vé đầu đêm.** Đề xuất như trên. Mặt trái: có thể dừng đợt sớm khi hạ tầng hỏng nhiều.

## Prompt bàn giao

Ở LOG T-074 phiên 11 (đáp CX-43/43b). Khi Minh cho tạo task, chép sang LOG task mới.
