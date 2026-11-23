# Nhật ký T-072

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 0 — 20/11/2026 — Claude (phiên điều phối T-070) — laptop Minh — vai trò: điều phối, khởi tạo task

- Tạo SPEC theo kế hoạch bản 5 (`tasks/T-070-dieu-phoi-giai-doan-2/SPEC.md`) và quyền Minh cho phiên điều phối (chat 20/11/2026, nguyên văn ở SPEC T-070): "… nếu là lỗi nhỏ có thể sửa ngay sau đó duyệt triển khai task luôn, lỗi chặn thì dừng trình". Phần "chờ Minh" trong SPEC chưa được duyệt.
- Hợp đồng giữa phiên: `tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md`; lịch máy: `LICH-MAY.md`. Phiên làm việc báo về điều phối khi kết thúc mỗi lượt (I15).
- Prompt Codex soát SPEC: ở LOG T-070 (gom cho T-070–T-075), Minh chuyển.

---

## Phiên 1 — 20/11/2026 — Claude Opus 5.5 (phiên `luat-w4`, local_fbf468fa) — laptop Minh — vai trò: người làm T-072

- 12:52Z (đồng hồ laptop `date -u`): mở phiên. Đã đọc AGENTS, STATE, SPEC T-072, HOP-DONG/LICH-MAY/SPEC/TRANG-THAI T-070, MRP §2.3 và P9–P10, WHY-99, `thong-nhat.md` §1.3 và CHẶN 3. Lượt này: SPEC bước 1 (`bieu-thuc.json`, `quy-tac-gom.json`), báo điều phối, rồi bước 2–4 ở lượt sau.
- 12:55Z: khảo sát file đã có. `results/T-069/thu/` chỉ có đầu ra k6 và sổ chạy; `results/T-067/tai-1-gio/` có tiêu chí k6/collector. **Không có chuỗi histogram gateway theo route trong dữ liệu đã lưu** (bộ xuất M1 có p50/p90 theo service; `xuat_bo_sung.py` có `route-rate`, `route-5xx`, không có bucket). Đọc thêm: `application.yaml` gateway (FlashTicket `36a3725d`: 7 id route), `purchase-journey.js` (lab `407b4f5`: chỉ gọi route `event`, `booking`, `payment`, `ticket`), cấu hình Prometheus (OTLP, lookback mặc định), receiver httpcheck (8 đích, 10 s).
- 12:57Z, 13:01Z, 13:05Z: kiểm `LICH-MAY.md`/`TRANG-THAI.json` ngay trước mỗi đợt truy vấn: chỉ S0 mở, E2/E4 chưa mở. Truy vấn nhẹ, chỉ đọc, Prometheus exp-obs (`khao-sat/khao-sat-1..3.sh`, đầu ra `.out`): instant query, cửa sổ trong biểu thức ≤ 10 phút, nghỉ 0,5 s. Thời điểm: lượt 1 giờ T-067 (18/11 08:30Z), ca khỏe ×1 `1e5debb6`, ×3 `0bec9eca`, flash `124242f0` (pha ×3), PAUSE-PAYMENT `81af0b51` (chỉ để xem dạng chuỗi khi đầu dò lỗi; giờ lấy từ sổ T-069, không dùng cho phương pháp), và hiện tại (nhàn rỗi).
  - Quan sát: `http_route` của gateway có 5 id route có tải + `user` + health + chuỗi không nhãn (401); mã 5xx có ở `event` (500/503/504), `payment` (503/504); 409, 429 ở `booking`. Bucket: 14 mốc 0,005–10 s. Mẫu histogram và đầu dò mỗi 10 s. Khi dò lỗi: `httpcheck_error` mỗi 30 s; `httpcheck_status` vẫn ghi 5 lớp giá trị 0, **không có** nhãn `http_status_code`; các đích khác cũng chỉ được dò ≈ 30 s/lần lúc treo. `timestamp()` trên selector trả giờ mẫu.
- 13:06Z: `sinh_bieu_thuc.py` → `bieu-thuc.json` (`T072-bieu-thuc-1`): 11 luật (p95 ×4 route, lỗi 5xx ×4, liveness đa chiều, 2 luật mất quan sát), tham số cố định, liveness ba trạng thái, danh sách chuỗi cho T-071 xuất (24 chuỗi `tin-hieu/*` + `phu/*`, query_range step 10 s; mẫu thô khuyến nghị), phần không phủ. Ngưỡng chỉ có tên tham số.
- 13:06–13:08Z: **kiểm xuất được** (`khao-sat/kiem-xuat-1.sh`, đầu ra `kiem-xuat-1.jsonl`): query_range step 10 s mọi chuỗi trong `xuat_cho_T071.bat_buoc` trên 6 khúc 10 phút. Kết quả: ở 5 khúc có tải, mọi chuỗi p95, liveness, mất quan sát, `phu/*` có **61/61 điểm**; luật lỗi không có điểm khi < 3 lỗi 5xx (đúng thiết kế), có 50 điểm ở PAUSE-PAYMENT (tỷ lệ tới 1); p95 `ticket` còn 25 điểm ở PAUSE-PAYMENT vì lưu lượng `ticket` tụt về 0 (guard). Khúc nhàn rỗi: p95/lỗi không có chuỗi (NoData → OK), liveness 8 đích = 0, `t072-mat-gw` ≈ 9,5 s. Mỗi truy vấn ≤ 0,032 s. Lượt hỏng trước đó (13:06Z): chạy qua `Invoke-Oracle` (PowerShell) trả về 1 dòng là chuỗi base64 của script, không có kết quả truy vấn; file đầu ra đã bị lượt chạy lại bằng `ssh … 'bash -s' <` ghi đè (vi phạm luật cứng 10 về giữ lượt hỏng; nội dung lượt hỏng chỉ là base64 của chính `kiem-xuat-1.sh`). Nguyên nhân chưa xác định.
- 13:08Z: `quy-tac-gom.json` (`T072-gom-1`): t̂ = lần đánh giá đầu ở Alerting; gom khoảng cháy lớp hệ thống ghép khi cách ≤ 300 s; lớp quan sát gom riêng; quy về phút chứa t̂; vắt qua biên đếm một lần theo phút bắt đầu; tỷ lệ = sự cố / (phút khỏe ×1 / 360), < 360 phút → "chưa đủ sáu giờ khỏe ×1"; E4 đếm chính từ lịch sử trạng thái Grafana, offline đối chiếu.
- 13:08Z: `de-xuat-why.md` (WHY-a…g, chờ Minh qua điều phối; không ghi `docs/WHY.md`). sha256 bước 1: `results/T-072/SHA256SUMS-buoc1` (`bieu-thuc.json` `1a4aee67…`, `quy-tac-gom.json` `bf32a574…`).

### Kết thúc lượt 1 (13:10Z)

1. **Đã làm:** SPEC bước 1: `bieu-thuc.json`, `quy-tac-gom.json`, đề xuất WHY, khảo sát và kiểm xuất được trên Prometheus exp-obs (chỉ đọc, ngoài E2/E4).
2. **File đã đổi:** tạo `results/T-072/` (`sinh_bieu_thuc.py`, `bieu-thuc.json`, `quy-tac-gom.json`, `de-xuat-why.md`, `SHA256SUMS-buoc1`, `khao-sat/*`); LOG này; dòng T-072 `docs/STATE.md`. Không đổi máy, repo lab, Grafana.
3. **Kiểm:** JSON hợp lệ; 61/61 điểm mỗi chuỗi ở 5 khúc có tải; đối chứng dương PAUSE-PAYMENT (lỗi payment, liveness 8083 = 1, về 0 khi có phản hồi lại ở +576 s); khúc nhàn rỗi không sinh NaN.
4. **Chưa chắc / cần quyết:** (a) R5 ngưỡng báo động giả, WHY-a…g (đặc biệt "theo route" = id route gateway; tham số 5 phút, ≥ 30 request, ≥ 3 lỗi 5xx, tuổi dò 60 s, `for`) chờ Minh; Minh có thể đổi tham số **trước** E2. (b) Nhãn route chỉ kiểm ở 5 thời điểm 18–20/11. (c) Chưa kiểm trên Grafana: bội 10 s của nhịp đánh giá, cách Grafana ghi t̂ (Pending→Alerting), độ trễ nạp mẫu lúc đánh giá — kiểm ở E3. (d) Che lấp trong route gộp nhiều API chưa đo. (e) T-071 cần chứng minh xuất được đúng `xuat_cho_T071.bat_buoc` suốt E2/E4 (cổng E2 điều kiện 3, phần T-071).
- **Tài nguyên đang giữ:** không. Job server: không.
- **Bước tiếp (lượt 2):** SPEC bước 2 `cham_offline.py` đọc `bieu-thuc.json` + `quy-tac-gom.json`, chạy trên dữ liệu xuất dạng `kiem-xuat` (cần xuất thêm 1 giờ T-067 theo khúc nếu điều phối cho, ngoài E2/E4), phép thử giả chèn bước nhảy; bước 3 `quy-tac-chon-nguong.json`, `i1-schema.json`; bước 4 worktree lab `D:/Project/rca-lab-wt/T-072`.
- **Lệnh cuối:** `sha256sum … | tee results/T-072/SHA256SUMS-buoc1`.
- 13:23Z: mở lượt 2 theo tin điều phối T-070 (bước 2–4; ưu tiên quy-tac-chon-nguong.json, i1-schema.json).
- 13:23Z: đọc `results/T-073/thiet-ke.md` §5 (giả định I1 của T-073: t̂ từ `startsAt`, t_hết từ `endsAt` webhook resolved, `DatasourceError`/`DatasourceNoData` → quan sát, gom theo `T072-gom-1`).
- 13:24Z: lượt hỏng (chỉ ở laptop): `xuat_tin_hieu.py dung` lỗi mã hóa cp1252 khi in script; ssh không chạy (chuỗi `&&`), không truy vấn nào tới server. Sửa: ghi stdout dạng UTF-8.
- 13:25–13:27Z: kiểm `TRANG-THAI.json` ngay trước: chỉ S0 mở. Xuất chỉ đọc bằng `xuat_tin_hieu.py` (24 chuỗi `bat_buoc`, query_range step 10 s, khúc ≤ 600 s, nghỉ 0,3 s): T-067 18/11 07:50–09:05Z, ca khỏe `1e5debb6` 19/11 09:30–10:06Z, PAUSE-PAYMENT `81af0b51` [t−900, t+1500] → `results/T-072/kiem-code/*.json`, 0 lỗi khúc. Chỉ để kiểm code (SPEC bước 2), không chọn ngưỡng.
- 13:27Z: `quy-tac-chon-nguong.json` (`T072-chon-nguong-1`): chỉ E2, chỉ bước thuộc phút khỏe ×1 (phân loại T-071); S(t) = min trong [t−for, t]; M = max S; θ_p95 = ceil₀.₀₀₁(max(1,5·M, M + 0,05 s)); θ_lỗi = ceil₀.₀₀₁(max(2·M, 0,05)); cần ≥ 120 bước/route, thiếu thì dừng trình. Không chứa con số R5. Hằng số k, sàn chờ Minh (đổi được trước E2).
- 13:28Z: `i1-schema.json` (`T072-i1-0`, JSON Schema): bản ghi một khoảng cháy; `t_hat.nguon` ∈ {lịch sử trạng thái, webhook-startsAt, offline}; mục `doi_chieu_T073` ghi trùng và khác (nguồn t̂ chuẩn của T-072 là lịch sử trạng thái; nhãn `t072_uid`; annotation `t072_eval_interval_s`, `t072_for_s`, `t072_nguong`, `t072_nguong_phien_ban`, `t072_bieu_thuc`; resolved có thể tới muộn so với `endsAt`).
- 13:29Z: `cham_offline.py` (cham / chon-nguong / tu-kiem). Phép thử giả tổng hợp `tu-kiem`: 21 ca đạt, 0 sai (`kiem-code/tu-kiem.json`): nền 0 sự cố; bước nhảy 120 s bắt ở +60 s; 50 s không bắt; hai bước cách 200 s gộp, 400 s tách; hai route chồng gộp; guard không điểm không cháy; liveness 30 s bắt, 15 s không; mất quan sát vào lớp quan sát; vắt qua biên đếm một lần; bắt đầu trong biên → lớp biên; cờ cửa sổ lấn; khúc xuất lỗi đặt lại; đang cháy lúc bắt đầu; chọn ngưỡng (gai 30 s không vào M; θ_p95 = 0,1, θ_lỗi = 0,05); thiếu dữ liệu → không tính; Poisson 0 → [0; 3,689].
- 13:30Z: kiểm trên dữ liệu thật với **ngưỡng thử** (`kiem-code/nguong-thu.json`, tính bằng chính `chon-nguong` trên T-067 + `1e5debb6` với phân loại phút tạm theo giờ lượt `kiem-code/phut-kiem-code.json`; chỉ kiểm code, không phải nguong.json): M p95 booking 0,048, event 0,047, payment 0,156, ticket 0,045 s → θ thử 0,098 / 0,097 / 0,235 / 0,095; lỗi M = 0 → 0,05. Nền: 0 sự cố trên 88 phút "khỏe" tạm, 113 phút có dữ liệu. Chèn bước nhảy giả p95 booking 0,5 s 120 s → 1 sự cố ở +60 s; chèn liveness 8084 = 1 trong 30 s → 1 sự cố ở +20 s. Đối chứng dương PAUSE-PAYMENT: 1 sự cố hệ thống, t̂ = t+30 s, gộp `t072-live`, `t072-loi-payment`, `t072-p95-payment`, hết ở t+930 s.
- 13:30Z: tạo worktree `D:/Project/rca-lab-wt/T-072` nhánh `t072-luat` từ `407b4f5`. Ghi: `observability/grafana/provisioning/alerting/README.md` (chưa có file luật `.yaml`: sinh sau E2), `observability/t072-bo-nhan/bo_nhan.py` (bộ nhận nhẹ, thư viện chuẩn; giờ nhận đo trước khi đọc thân). Chưa commit.
- 13:31Z: `sinh_luat_grafana.py` (repo RCA) sinh YAML provisioning từ `bieu-thuc.json` + `nguong.json`: 11 luật, nhóm `t072-w4` 10 s, A = PromQL instant, C = threshold; nhãn `t072_uid`; định tuyến theo từng luật (`notification_settings`, group_by mọi nhãn, group_wait 0 s, group_interval 10 s), không đổi cây chính sách. Mẫu với ngưỡng thử: `kiem-code/luat-mau-nguong-thu.yaml` (chỉ kiểm cú pháp; không nạp). Kiểm: YAML đọc lại được, 11 luật, điều kiện gt/lt đúng. **Không kiểm được bằng Grafana**: Docker Desktop trên laptop không chạy; tên trường provisioning (`notification_settings`, `group_wait: 0s`) theo tài liệu Grafana, [chưa kiểm trên 13.3] → kiểm ở E3. Bộ nhận thử trên laptop 127.0.0.1:19172: nhận 1 POST, ghi đúng 1 dòng (`kiem-code/bo-nhan-thu.jsonl`), đã tắt.
- 13:31Z: sha256: `results/T-072/SHA256SUMS-buoc2-4` — `quy-tac-chon-nguong.json` `a708c2bf…`, `i1-schema.json` `b0eabeab…`, `cham_offline.py` `bde294fb…`, `bieu-thuc.json` `1a4aee67…` (không đổi), `quy-tac-gom.json` `bf32a574…` (không đổi). Worktree: `bo_nhan.py` `99555896…`, `README.md` `a4cb5503…`.

### Kết thúc lượt 2 (13:32Z)

1. **Đã làm:** SPEC bước 2–4: `quy-tac-chon-nguong.json`, `i1-schema.json`, `cham_offline.py` + phép thử giả, `xuat_tin_hieu.py`, `sinh_luat_grafana.py`, worktree lab (README luật, bộ nhận nhẹ).
2. **File đã đổi:** `results/T-072/` (các file trên, `SHA256SUMS-buoc2-4`, `kiem-code/*`); worktree `D:/Project/rca-lab-wt/T-072` (2 file mới, chưa commit); LOG này; dòng T-072 STATE.
3. **Kiểm:** tu-kiem 21/21; dữ liệu thật: nền 0 sự cố, hai bước nhảy giả bắt được, PAUSE-PAYMENT 1 sự cố; YAML đọc lại; bộ nhận nhận 1 POST.
4. **Chưa chắc / cần quyết:** (a) Minh: R5, WHY-a…g, và hằng số chọn ngưỡng (k_p95 1,5, sàn 0,05 s, k_lỗi 2, sàn 5%) — đổi được trước E2. (b) Điều phối: chốt I1 (`i1-schema.json` mục `doi_chieu_T073`). (c) Đường mạng Grafana → bộ nhận (T-073 §10: INPUT chặn mạng bridge) chưa có; cần chọn phương án trước E3. (d) Cú pháp provisioning chưa kiểm bằng Grafana; t̂ (`startsAt` so với lịch sử trạng thái) kiểm ở E3. (e) Ngưỡng thử cho thấy p95 payment dao động lớn nhất (M 0,156 s ở `1e5debb6` so với ≈ 0,09 ở T-067) — chỉ quan sát, không dùng chọn.
- **Tài nguyên đang giữ:** không (chỉ worktree lab của mình). Job server: không.
- **Bước tiếp:** sau E2: `py -3 results/T-072/cham_offline.py chon-nguong --xuat <chuỗi E2> --phut <phân loại phút E2 của T-071> --ra results/T-072/nguong.json`, rồi `py -3 results/T-072/sinh_luat_grafana.py --nguong results/T-072/nguong.json --webhook <url đã chốt> --ra D:/Project/rca-lab-wt/T-072/observability/grafana/provisioning/alerting/t072-luat.yaml`; trình diff + commit qua điều phối.
- **Lệnh cuối:** `sha256sum … | tee results/T-072/SHA256SUMS-buoc2-4`.

**Quyết định của Minh trong phiên** (chuyển qua điều phối T-070, 20/11 ~13:33Z; nguyên văn Minh 13:25Z: "Duyệt theo đề xuất"; nguồn LOG T-070 "Lượt 3 — Minh quyết R1–R9"; DECISIONS đã ghi 13:26Z, mục "Điều phối giai đoạn 2: quyết định R1, R5, R7, R9 (T-070, 20/11/2026)"):
- R5: ngưỡng báo động giả chấp nhận ≤ 1 sự cố / 6 giờ khỏe ×1.
- R7: phương án tải A; mỗi khoảng 8 lượt = 6 lượt ×1 3600 s + 2 lượt flash 1800 s, bậc ×3 ở 600 s. Lượt bù không nằm trong duyệt.
- WHY đề xuất của T-072 (WHY-a…g) và hằng số chọn ngưỡng: **chưa duyệt**, giữ ở `results/T-072/`.

- 13:33Z: **làm rõ lượt 1** (điều phối đếm lại `khao-sat/kiem-xuat-1.jsonl`): câu "mỗi chuỗi … 61/61" ở báo cáo lượt 1 nói rộng hơn dữ liệu. Đúng là: ở 4 khúc có tải khỏe, 20/24 chuỗi đủ 61 điểm; 4 chuỗi `tin-hieu/t072-loi-*` có 0 điểm (đúng thiết kế, < 3 lỗi 5xx). `t072-loi-booking`, `t072-loi-event`, `t072-loi-ticket` 0 điểm ở mọi khúc, kể cả PAUSE-PAYMENT; chỉ `loi-payment` có điểm (50) → lúc đó ba luật này chưa từng được kiểm dương.
- 13:34Z: kiểm `TRANG-THAI.json` (S0). Xuất chỉ đọc ca HTTP5-EVENT `30ae6ac0` (19/11 17:00–17:25Z; lỗi theo sổ 17:05:39–17:15:39Z) bằng `xuat_tin_hieu.py` → `kiem-code/t069-http5-event.json`, 0 lỗi khúc. `t072-loi-event`: 89 điểm, tỷ lệ 0,004–0,50; chấm với ngưỡng thử: 1 sự cố, t̂ = tiêm + 101 s, hết = gỡ + 271 s, chỉ `t072-loi-event` → **loi-event đã kiểm dương**. `phu/5xx-booking`, `phu/5xx-ticket` = 0 ở khúc này; chưa có ca đã ghi nào sinh 5xx ở `booking`/`ticket` (khảo sát 20/11: không có chuỗi 5xx cho hai route này) → `loi-booking`, `loi-ticket` **chưa kiểm dương trên dữ liệu thật**.
- 13:35Z: `cham_offline.py tu-kiem` thêm ca cho **cả bốn luật lỗi và bốn luật p95** (mỗi route: lỗi 0,4 bắt ở +60 s; lỗi 0,04 dưới ngưỡng không bắt; p95 0,3 bắt), và ca "bằng ngưỡng không cháy". 33 ca, 0 sai. Phép đột biến (bản sao ở scratchpad): ghép 100 s thay 300 s, `>` thay `>=` ở `for`, `>=` thay `>` ở điều kiện, tắt cờ cửa sổ lấn → cả 4 đột biến làm `tu-kiem` sai (lần lượt 2, 21, 1, 1 ca).
- 13:35Z: `quy-tac-chon-nguong.json` → `T072-chon-nguong-2`: thêm `tieu_chi_E4_R5` (R5 chỉ dùng để kết luận E4; không vào công thức θ). `quy-tac-gom.json` → `T072-gom-2`: thêm `co_cau_phuong_an_A` (600 s đầu lượt flash là ×1, khớp 380 phút ×1/khoảng ở `thong-nhat.md` CHẶN 3; bốn trường hợp vắt qua biên theo cơ cấu 8 lượt); quy tắc gom không đổi so với gom-1 (T-073 không phải sửa bộ gom). `ke-hoach-e3-duong.md`: bảng dương thật theo từng luật và đề xuất E3 (luật thử `vector(1)` kiểm đường ống Grafana/webhook; ghi rõ 7 luật còn chưa kiểm dương sau E3).
- sha256 `results/T-072/SHA256SUMS-luot2b`: `quy-tac-chon-nguong.json` `c49fdabc…`, `quy-tac-gom.json` `64fc491c…`, `cham_offline.py` `23ed4f9f…`, `ke-hoach-e3-duong.md` `b7fcc101…` (thay các hash cũ của ba file đầu trong `SHA256SUMS-buoc2-4`).

### Kết thúc lượt 2b (13:36Z)

1. **Đã làm:** ghi quyết định R5/R7; làm rõ câu 61/61; kiểm dương `loi-event`; thử giả phủ 4 luật lỗi + 4 luật p95, có phép đột biến; R5 vào quy tắc chọn ngưỡng; cơ cấu phương án A vào quy tắc gom; kế hoạch dương E3.
2. **File đã đổi:** `results/T-072/` (`quy-tac-chon-nguong.json`, `quy-tac-gom.json`, `cham_offline.py`, `ke-hoach-e3-duong.md`, `SHA256SUMS-luot2b`, `kiem-code/t069-http5-event.*`, `kiem-code/cham-thu-http5-event.json`, `kiem-code/tu-kiem.json`); LOG này.
3. **Kiểm:** JSON hợp lệ; tu-kiem 33/33; 4/4 đột biến bị bắt; dương thật: `loi-event`, `loi-payment`, `p95-payment`, `live`.
4. **Chưa chắc / cần quyết:** 7 luật chưa có dương thật (`p95-booking`, `p95-event`, `p95-ticket`, `loi-booking`, `loi-ticket`, `mat-do`, `mat-gw`); E3 không có tải nên không kiểm được; muốn kiểm trước E4 phải đổi khung S2 (điều phối/Minh). WHY và hằng số chọn ngưỡng chưa duyệt. Đường mạng webhook chưa có.
- **Tài nguyên đang giữ:** không (worktree lab của mình). Job server: không.
- **Lệnh cuối:** `sha256sum … > results/T-072/SHA256SUMS-luot2b`.

### Lượt 3 — I1 bản `T072-i1-1` (20/11, theo chốt của điều phối, HOP-DONG I1 "Chốt 20/11/2026 ~14:05Z")

- 14:02Z: lưu bản cũ `results/T-072/i1-schema-T072-i1-0.json` (sha256 `b0eabeab…`, trùng `i1-schema.json` cũ). Ra `i1-schema.json` bản `T072-i1-1`: (a) `luat.t072_tin_hieu` thêm `khong-ro`, `allOf` buộc `khong-ro` → `t072_loai = quan-sat`; (c) `ma` = sha256 utf-8 của `"<fingerprint>|<floor(t_hat.epoch_s)>"` (số nguyên thập phân), 16 hex đầu, kèm `pattern`; (b) enum `t_hat.nguon` vốn không có `webhook-annotation:*` (i1-0 cũng không), giữ `lich-su-trang-thai`, `webhook-startsAt`, `offline-luoi-xuat`; mô tả ghi dịch vụ chỉ dùng `webhook-startsAt`, chấm dùng lịch sử trạng thái, E3 đo lệch (d); bỏ mục `doi_chieu_T073`, thay bằng mục `chot` (nguồn, thay đổi (a)–(e)).
- 14:03Z: kiểm bằng `jsonschema` 4.23.0 (`Draft202012Validator`, có kiểm format): schema hợp lệ; mẫu lớp hệ thống (`t072-loi-payment`) hợp lệ; mẫu DatasourceError thiếu nhãn (`khong-ro`, `quan-sat`) hợp lệ. Ba đối chứng âm đều bị từ chối: `khong-ro` mà `he-thong`; `ma` sai dạng; nguồn `webhook-annotation:…`. Mẫu và kết quả: `kiem-code/i1-mau.json`. Ví dụ: `ma` của mẫu 1 = sha256(`3f2a9c1d0b7e4a55|1795100409`)[:16] = `44fb99bfac36c7a5`.
- sha256 (`results/T-072/SHA256SUMS-i1-1`): `i1-schema.json` **`02f779b09bbc8b6989e38f5da3f47a3f598507bd22cdd28020b702f7fb7efd39`**; `i1-schema-T072-i1-0.json` `b0eabeab…`; `kiem-code/i1-mau.json` `91883e3a…`.
- Kết thúc lượt 3 (14:04Z): file đổi: `results/T-072/i1-schema.json`, `i1-schema-T072-i1-0.json` (mới), `kiem-code/i1-mau.json`, `SHA256SUMS-i1-1`, LOG này. Tài nguyên giữ: không (worktree lab của mình). Job server: không. Lệnh cuối: `sha256sum … | tee results/T-072/SHA256SUMS-i1-1`.

### Lượt 4 — chuẩn bị E3 (20/11, theo giao việc điều phối; Minh duyệt (a), (b) ở LOG T-070 "Lượt 4"; không dùng máy, E2 đang chạy)

- 21:43Z: kiểm `cham_offline.py`, `quy-tac-chon-nguong.json` (ứng dụng báo "đổi trên đĩa"): sha256 `23ed4f9f…`, `c49fdabc…` trùng hash ghi ở lượt 2b; mtime 13:34Z — không ai sửa sau lượt 2b. Ghi nhận: `/opt/rca-lab` exp-obs đang ở `e9a0857` (`t071-nen`), nhánh `t072-luat` tách từ `407b4f5`.
- 21:5xZ: `sinh_luat_thu_e3.py` (mới): `nap` → 4 luật thử `t072-thu-p95-{booking,event,payment,ticket}` (bản sao PromQL luật p95, kiểm trùng chuỗi: đúng; ngưỡng thử 0,005 s, for 60 s, nhịp 10 s, nhãn `t072_loai = thu`, thư mục/nhóm riêng, gửi `t072-bo-nhan-nhe`); `go` → `deleteRules` cho 4 uid. Ghi ở worktree dưới đuôi `.mau` (Grafana không nạp): `observability/grafana/provisioning/alerting/t072-thu-e3.yaml.mau`, `t072-thu-e3-go.yaml.mau`; đổi tên khi làm commit N/G.
- 21:46Z: `ke-hoach-e3.md`: điều kiện mở S2 (chon-nguong → nguong.json; sinh luật thật; commit N nạp và G gỡ, gốc phải chứa `e9a0857`), 11 bước E3, cách đọc trạng thái/lịch sử trạng thái qua DB Grafana chỉ đọc (cần đồng ý), yêu cầu compose bộ nhận cho T-073, kiểm `startsAt`/`endsAt` (|Δ| ≤ 10 s), E3 chứng minh gì/không, xử lý lỗi. sha256: `results/T-072/SHA256SUMS-e3-chuan-bi`.
- Kết thúc lượt 4: file đổi: `results/T-072/ke-hoach-e3.md`, `sinh_luat_thu_e3.py`, `SHA256SUMS-e3-chuan-bi` (mới); worktree: 2 file `.mau` (mới, chưa commit); LOG này. Tài nguyên giữ: không (worktree của mình). Job server: không. Bước tiếp: khi T-071 báo có chuỗi E2 + phân loại phút → `py -3 results/T-072/cham_offline.py chon-nguong --xuat <…> --phut <…> --ra results/T-072/nguong.json`. Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-e3-chuan-bi`.

### Lượt 5 — sửa theo Codex CX-07 (20/11, điều phối giao; không dùng máy)

- 21:55Z: đọc `results/T-071/xuat_chuoi.py` (mỗi chuỗi một `chuoi/<ten>.json.gz` {ten, loai, promql, step_s, result[{metric, values}]}, `tom-tat.json` có `bat_dau`, `ket_thuc`, `khuc_loi` ISO) và `phan_loai_phut.py` (`{tom_tat, phut[{phut, luot, muc, nhan, co}]}`, nhãn `khoe_x1` …). Đúng là khác định dạng `cham_offline.py` (CHẶN 1 của CX-07).
- 22:0xZ: `chuyen_dinh_dang.py` (mới; chỉ đọc file T-071): `xuat` → T072-xuat-1 (giữ mốc, chỉ đổi số thực nguyên → nguyên, mốc không nguyên thì dừng; giữ nhãn, giá trị nguyên văn; khúc lỗi [a, b] → [a, b − 10]; kiểm số điểm khớp `tom-tat.json`); `phut` → `khoang` với nhãn `_` → `-`, kèm đối chiếu đếm.
- Kiểm `xuat` trên lượt xuất thử của T-071 `results/T-071/xuat-thu/thu-001.tgz` (giải nén vào scratchpad): 24 chuỗi, 14.708 điểm, 0 khúc lỗi; so với bản T-072 tự xuất cùng giờ T-067 (`kiem-code/t067-1gio.json`, lượt 2): **14.318 điểm chung, 0 lệch giá trị** (so chuỗi nguyên văn). `cham` và `chon-nguong` chạy trọn trên file đã chuyển (`kiem-code/chuyen/`).
- Kiểm `phut` bằng tệp giả đúng dạng `phan_loai_phut.py` (62 phút, chỉ để kiểm bộ chuyển; chưa có phân loại E2 thật): `khoe-x1` 55 trước = 55 sau = `tom_tat.khoe_x1_phut`; mẫu số `cham` = 55. Đối chứng âm: `tom_tat.khoe_x1_phut` = 54 → thoát 1.
- 22:0xZ: `sinh_luat_thu_e3.py hoan-tac` (CHẶN 2): `t072-hoan-tac-n.yaml.mau` ở worktree, `deleteRules` 15 uid + `deleteContactPoints` `t072-webhook`. `nap`, `go` sinh lại trùng byte bản cũ.
- 21:58Z: `ke-hoach-e3.md` sửa: mục 1.1 lệnh chuyển định dạng + chon-nguong; mục 1.2 `<dns-bo-nhan>` chờ T-073; mục 1.3 commit H (con của P, gỡ mọi đối tượng N); bước 10 chỉ sau khi lượt `t071-e3-duong-01` và phép đo T-073 đã thoát, kiểm không job, ghi commit trước/sau; mục 7 quy trình hoàn tác và kiểm đối tượng đã mất trước khi trả khung; điểm chưa kiểm của `deleteRules`. sha256: `results/T-072/SHA256SUMS-cx07`.
- Kết thúc lượt 5: file đổi: `chuyen_dinh_dang.py` (mới), `sinh_luat_thu_e3.py`, `ke-hoach-e3.md`, `kiem-code/chuyen/*`, `SHA256SUMS-cx07`; worktree `t072-hoan-tac-n.yaml.mau` (mới, chưa commit); LOG này. File T-071: không sửa. Tài nguyên giữ: không (worktree của mình). Job server: không. Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-cx07`.

### Lượt 6 — DNS bộ nhận, D1, D4 (20/11, điều phối chuyển; không dùng máy)

**Quyết định của Minh trong phiên** (chat 20/11, nguyên văn "Duyệt cả năm"; điều phối chuyển ~22:03Z, nguồn LOG T-070):
- D1: E4 có 9 lượt = 8 lượt như E2 + 1 lượt ×1 1800 s, cùng quy tắc phân loại phút.
- D4: điều phối ghi `results/T-072/de-xuat-why.md` vào `docs/WHY.md` trước khi T-072 chạy `chon-nguong`.
- (Thông tin từ T-073, không phải quyết định của Minh) DNS bộ nhận E3 của T-072: `t072-bo-nhan`, cổng 9172, đường dẫn `/t072`.

- 22:04Z: `ke-hoach-e3.md` mục 1.2 và 4: URL `http://t072-bo-nhan:9172/t072` vào lệnh sinh luật.
- 22:05Z: `quy-tac-gom.json` → `T072-gom-3` (bản cũ `quy-tac-gom-T072-gom-2.json`): thêm `co_cau_E4` (9 lượt; lượt ×1 1800 s thêm phân loại như mọi phút ×1; mẫu số tối đa 410 phút khỏe ×1 ở E4, 380 ở E2; chỉ tính từ giờ hiệu lực E4). Quy tắc gom, t̂, cách tính tỷ lệ không đổi. **Không sửa** `quy-tac-chon-nguong.json` (`c49fdabc…`, khóa trước E2): `tieu_chi_E4_R5` không có số lượt, dùng mẫu số theo `quy-tac-gom.json`.
- 22:04Z: soát `de-xuat-why.md` trước D4 → bản 2 (bản 1 `de-xuat-why.v1.md`): WHY-g bỏ câu "R5 vẫn chờ Minh" (đã duyệt 13:25Z), thêm cơ cấu lượt E2/E4 và cách đếm cửa sổ lấn; **thêm WHY-h** (quy tắc chọn ngưỡng và các hằng số 1,5 / 0,05 s / 2 / 5%, lý do, phương án đã xét, bằng chứng chỉ kiểm code, điều kiện thất bại), vì hằng số này là lựa chọn quan trọng (luật cứng 3) mà bản 1 chưa có mục. sha256: `results/T-072/SHA256SUMS-d1-d4`.
- Kết thúc lượt 6: file đổi: `ke-hoach-e3.md`, `quy-tac-gom.json`, `de-xuat-why.md`; mới `quy-tac-gom-T072-gom-2.json`, `de-xuat-why.v1.md`, `SHA256SUMS-d1-d4`; LOG này. Tài nguyên giữ: không (worktree của mình). Job server: không. Chờ: T-071 phân loại phút E2 thật. Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-d1-d4`.

### Lượt 7 — ngưỡng từ E2, file luật, đề xuất commit lab (21/11, điều phối giao; không dùng máy)

- 03:00Z: hash file của T-072 không đổi (`cham_offline.py` `23ed4f9f…`, `quy-tac-chon-nguong.json` `c49fdabc…`, `bieu-thuc.json` `1a4aee67…`, `quy-tac-gom.json` `9354b611…`). `results/T-071/e2/SHA256SUMS`: ra.tgz, ra-SHA256SUMS, xuat.out OK (các file kiểm khác điều phối đã kiểm 13/13).
- 03:01Z: giải nén `results/T-071/e2/ra.tgz` (`bb52963a…`) vào `results/T-072/e2/ra/` (bản sao; file T-071 không đổi); `ra-SHA256SUMS` 377/377 OK.
- 03:01Z: `chuyen_dinh_dang.py xuat` 8 lượt → `results/T-072/e2/xuat/*.t072.json`: 24 chuỗi mỗi lượt, 0 khúc lỗi; số điểm 14.752 / 15.300 ×4 / 9.180 / 9.214 / 15.250. Phần chồng giữa file lượt kề: 19.210 điểm, 0 lệch giá trị; lưới liền suốt E2.
- 03:01Z: `chuyen_dinh_dang.py phut results/T-071/e2/phan-loai-phut.json` (`2e8ebbb2…`) → `e2/phut.json`: trước = sau = {`khoe-x1` 356, `bien` 38, `flash` 38}; `khoe_x1_phut` của T-071 = 356; 0 phút trùng → **khớp**.
- 03:02Z: `cham_offline.py chon-nguong` (quy tắc khóa `T072-chon-nguong-2`, không sửa) → `results/T-072/nguong.json` (`c8f44854…`). Mỗi route đủ bước (≥ 120):

  | route | bước (gồm / bỏ `lan_cua_so`) | M p95 gồm / bỏ (s) | θ p95 (s) | M lỗi gồm / bỏ | θ lỗi |
  |---|---|---|---|---|---|
  | booking | 2136 / 1896 | 0,04748 / 0,04414 | 0,098 | 0 / 0 | 0,05 |
  | event | 2136 / 1896 | 0,04617 / 0,04529 | 0,097 | 0 / 0 | 0,05 |
  | payment | 2129 / 1896 | 0,12250 / 0,12250 | 0,184 | 0 / 0 | 0,05 |
  | ticket | 2129 / 1896 | 0,06125 / 0,06125 | 0,112 | 0 / 0 | 0,05 |

  (nguồn: `nguong.json#/chi_tiet/theta_*`). θ p95 booking, event = M + 0,05 s; payment, ticket = 1,5 × M. Soi vô lý (QT5): θ cùng bậc với p95 khỏe đã thấy ở T-067/T-069 (0,02–0,16 s), không cực lớn.
- 03:02Z: **trong mẫu E2** (`cham_offline.py cham` với θ trên E2, `e2/cham-trong-mau.json`): **0 sự cố** ở mọi lớp (hệ thống và quan sát; khỏe ×1, biên, flash), 2.676 bước, 447 phút có dữ liệu; mẫu số khỏe ×1 bộ chấm đếm = 356 = T-071 (mọi phút khỏe có chuỗi xuất). Đây là số trong mẫu, không so R5.
- 03:03Z: `sinh_luat_grafana.py` → worktree `observability/grafana/provisioning/alerting/t072-luat.yaml`, contact point `http://t072-bo-nhan:9172/t072`; kiểm 11 luật khớp PromQL `bieu-thuc.json` và ngưỡng `nguong.json`. Luật thử giữ `.mau`. README worktree cập nhật (file luật đã có).
- 03:03Z: phát hiện YAML do Python sinh trên Windows ở dạng CRLF (repo lab LF). Sửa `sinh_luat_grafana.py`, `sinh_luat_thu_e3.py` ghi `newline='\n'` (hai lần sửa đầu hỏng cú pháp do chèn ký tự xuống dòng thật, phát hiện bằng `py_compile`, sửa ở lần 3); sinh lại 4 YAML, giờ đều LF; nội dung luật kiểm lại khớp.
- 03:03Z: `de-xuat-commit-lab.md` (6 file mới, diff `de-xuat-commit-lab.diff` 991 dòng, sha256 + blob git `de-xuat-commit-lab.tsv`, thông điệp commit, 3 điểm cần quyết: gốc nhánh `e9a0857`, `.mau` hay đổi tên luật thử ở commit này, dịch vụ `t072-bo-nhan` phải có trong compose cùng commit). Chưa commit.
- sha256: `results/T-072/SHA256SUMS-e2-nguong` (gồm đầu vào T-071 `ra.tgz` `bb52963a…`, `phan-loai-phut.json` `2e8ebbb2…`, `ra-SHA256SUMS` `0cdfb3c3…`; `nguong.json` `c8f44854…`; `t072-luat.yaml` `132eafc0…`).
- Kết thúc lượt 7: file đổi: `results/T-072/` (`nguong.json`, `e2/*`, `de-xuat-commit-lab.{md,diff,tsv}`, `sinh_luat_grafana.py`, `sinh_luat_thu_e3.py`, `SHA256SUMS-e2-nguong`); worktree (`t072-luat.yaml` mới, README, 3 `.mau` sinh lại LF); LOG này. File T-071: không sửa. Tài nguyên giữ: không (worktree của mình). Job server: không. Bước tiếp: điều phối gom commit; E3 theo `ke-hoach-e3.md`. Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-e2-nguong`.

### Lượt 8 — sửa theo Codex CX-09 (21/11, điều phối giao; không dùng máy)

- 03:09Z: đọc `results/T-070/codex/CX-09-tin-cuoi.md` (Q1 đúng: `t072-luat.yaml` khớp `nguong.json`, 11/11 uid; hai CHẶN, một KHÔNG CHẶN) và `results/T-073/trien-khai-bo-nhan.md` (project riêng `t073-webhook`, file env `$E`, lệnh `rm -s -f t072-bo-nhan`).
- 03:1xZ: **CHẶN 1:** worktree: `t072-thu-e3.yaml.mau` → `t072-thu-e3.yaml` (sinh lại bằng `sinh_luat_thu_e3.py nap`, chỉ đổi dòng đầu "gỡ bằng … (commit G)"); `t072-thu-e3-go.yaml.mau`, `t072-hoan-tac-n.yaml.mau` giữ đuôi. Kiểm 4 uid của file thử = 4 uid trong `deleteRules` của file gỡ. README worktree sửa theo. `de-xuat-commit-lab.md` bản 2 (bản 1 `de-xuat-commit-lab.v1.md`): commit N (6 file, gốc `e9a0857`), commit G (xóa file thử, kích hoạt file gỡ, giữ phần còn lại), commit H. Diff mới 993 dòng.
- 03:1xZ: **CHẶN 2:** `ke-hoach-e3.md` bước 3 dùng project riêng của T-073 (`docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml up -d t072-bo-nhan`); mục 7 hoàn tác theo thứ tự: `rm -s -f t072-bo-nhan` cùng `$E` khi còn ở N → checkout H, khởi động lại Grafana → kiểm 15 uid, contact point `t072-webhook`, container bộ nhận đã mất → về P. Mục 1.3 ghi H không chứa compose của T-073.
- 03:2xZ: **KHÔNG CHẶN — đính chính** `results/T-072/nguong.json` (`c8f44854…`, không sửa, không chạy lại): trường `quy_tac` ghi `T072-chon-nguong-1` là **sai nhãn**; đúng là `T072-chon-nguong-2` — file quy tắc dùng có sha256 `c49fdabc…` (ghi trong `nguong.json#/dau_vao_sha256`), là bản 2. Nguyên nhân: `cham_offline.py` ghi cứng tên bản. Sửa code: `quy_tac` lấy từ `phien_ban` của file quy tắc; docstring bỏ tên bản cứng. Bản code đã dùng tính `nguong.json` lưu nguyên ở `cham_offline-23ed4f9f.py`. Kiểm code mới: `tu-kiem` 33/33; chạy `chon-nguong` một lần ra file riêng `kiem-code/nguong-kiem-ban-moi.json` chỉ để kiểm: `quy_tac = T072-chon-nguong-2`, `nguong` và `chi_tiet` trùng hệt `nguong.json`.
- 03:11Z: sha256 `results/T-072/SHA256SUMS-cx09`. Kết thúc lượt 8: file đổi: `ke-hoach-e3.md`, `de-xuat-commit-lab.{md,diff,tsv}`, `cham_offline.py`, `sinh_luat_thu_e3.py`; mới `de-xuat-commit-lab.v1.md`, `cham_offline-23ed4f9f.py`, `kiem-code/nguong-kiem-ban-moi.json`, `SHA256SUMS-cx09`; worktree: `t072-thu-e3.yaml` (đổi tên), README; LOG này. Tài nguyên giữ: không (worktree của mình). Job server: không. Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-cx09`.

### Lượt 9 — E3 bước 1–4 (22/11, khung S2; điều phối giao 05:14Z)

**Quyết định của Minh trong phiên** (nguồn LOG T-070 dòng 256, nguyên văn): "Anh duyệt commit và push gói E3 (nhánh `t070-e3`) để mở E3". Commit N = lab `d677244` (`d6772444e0177a2bee484e6fc79ebc32182524c5`, cha `e9a0857`, 15 file T-072 + T-073; điều phối so byte). Chưa được phép: đọc `grafana.db` (điều phối đang hỏi Minh). S2 mở cho T-072 (Grafana, `/opt/rca-lab` exp-obs) theo `LICH-MAY.md` 21/11 03:17:05Z, bắt đầu 22/11 05:14:06Z.

- 05:14Z: hash file T-072 khớp `SHA256SUMS-cx09` (0 lệch).
- 05:15:07Z **bước 1** (chỉ đọc, `e3/b1-truoc.{sh,txt}`): `/opt/rca-lab` exp-obs `e9a0857`, cây sạch, không job, không STOP; 5 container quan sát Up 4 ngày; Grafana 13.3.0 (`api/health` database ok), StartedAt 18/11 02:21:46Z; biến lịch sử trạng thái rỗng (mặc định); chưa có image python; `runs/` ubuntu 700, uid ubuntu 1001.
- 05:15:25Z → 05:15:26Z **bước 2** (`e3/b2-checkout.{sh,txt}`): `git fetch origin t070-e3` (FETCH_HEAD = `d6772444…`); checkout **trước `e9a0857` → sau `d677244`**; cây sạch; 15 file thêm so với `e9a0857`; 6 file của T-072 trên máy khớp sha256 `de-xuat-commit-lab.tsv` (6/6).
- 05:16:01–05:16:39Z **bước 3** (`e3/b3-bo-nhan.{sh,txt}`): tạo `/srv/rca-lab/runs/t072-e3-01` (đầu ra bộ nhận) và `t072-e3-01-cfg` (file env, 600) — đặt file env trong vùng T-072 (I9) thay vì `runs/t073-<lượt>/` như ví dụ của T-073; `T073_SPOOL_DIR` đặt giá trị không tồn tại vì dịch vụ `t073-webhook` không bật ở E3. `docker pull python:3.12-slim` (5 s; image 202,8 MB giải nén). **Digest: `python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`.** `docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml up -d t072-bo-nhan` 05:16:06Z → healthy 05:16:38Z; user 1001:1001, rootfs chỉ đọc, không cổng host, `/app` chỉ đọc, `/ra` đọc-ghi; 5 container `flash-ticket-obs-*` giữ nguyên StartedAt. Tin thử tay từ container cùng mạng tới `/t072-tay`: HTTP 200, bộ nhận ghi 1 dòng (`nhan_webhook_utc` 05:16:39.26Z). Dòng này không tính là Grafana phát.
- 05:17:04Z **bước 4** (`e3/b4-restart.{sh,txt}`, `b4-log-them.txt`, `b4-trang-thai-truy-van.txt`; log đầy đủ trên máy `runs/t072-e3-01-cfg/grafana-log-sau-restart.txt` sha256 `d620e8f5…`): kiểm lại HEAD `d677244` sạch, không job; **restart 05:17:04Z**, StartedAt 05:17:06.12Z; **health ok 05:17:16Z** (database ok, 13.3.0). `docker logs`:
  - `provisioning.alerting`: bỏ qua `README.md`, `t072-hoan-tac-n.yaml.mau`, `t072-thu-e3-go.yaml.mau` (đuôi không hợp lệ, đúng thiết kế); "starting to provision alerting" 05:17:14.18Z → "finished to provision alerting" 05:17:14.58Z, **không có lỗi/cảnh báo provisioning alerting**.
  - `ngalert.state.manager` 05:17:14.65Z: **"State cache has been initialized" rules=15 states=0** — tổng số luật cảnh báo của tổ chức = 15 = 11 luật thật + 4 luật thử. Log **không in UID từng luật**, nên không xác nhận được từng UID bằng log; nếu trước N đã có luật khác trong Grafana thì con số 15 sẽ lệch — chỉ DB/API phân xử được.
  - `ngalert.scheduler`: tick đầu 05:17:20Z, nhịp 10 s. `plugin.prometheus` (uname `grafana_scheduler`, dsUid prometheus): 15 truy vấn mỗi 10 s từ 05:17:20Z; tới 05:19:19Z **180/180 status=ok** (khớp 15 luật × 12 tick, mỗi luật một truy vấn A).
  - `ngalert.notifier`: áp cấu hình Alertmanager 05:17:12Z và 05:18:14Z.
  - 2 dòng level=error, cả hai không liên quan alerting: "job cleanup controller failed: context canceled" lúc tắt (05:17:05Z), và thiếu thư mục `provisioning/plugins` (có từ trước, không thuộc T-072).
  - Bộ nhận tới 05:19:19Z vẫn 1 dòng (tin thử tay): không có tin Grafana, đúng kỳ vọng khi không tải (luật thật Normal; luật thử NoData → OK).
- **Giờ hiệu lực E3 (đề xuất, theo log):** 05:17:20Z, tick đầu có đủ 15 truy vấn ok. Theo định nghĩa ở `ke-hoach-e3.md` bước 5 (cả 11 luật thật đã đánh giá, không luật nào Error) cần đọc trạng thái theo từng UID; chưa làm vì chưa được đọc `grafana.db`.
- 05:19:41Z: **dừng trước bước 5** theo giao việc. Máy đang ở: `/opt/rca-lab` exp-obs `d677244`; Grafana chạy với 15 luật; container `flash-ticket-t072-bo-nhan` chạy (project `t073-webhook`). sha256: `results/T-072/SHA256SUMS-e3-b1-4`. Lệnh cuối: `sha256sum e3/* > SHA256SUMS-e3-b1-4`.

**Quyết định của Minh trong phiên** (nguồn LOG T-070 dòng 262, 22/11 05:16Z, nguyên văn): "Cho phép" — cho T-072 đọc chỉ đọc 3 bảng luật/trạng thái trong `grafana.db`. Phạm vi (điều phối chuyển): `file:…grafana.db?mode=ro` bằng sqlite3 thư viện chuẩn; chỉ `alert_rule`, `alert_instance`, `annotation` (và `sqlite_master`/cấu trúc bảng để biết tên cột); chỉ cột cần; không chép DB ra khỏi máy; không đọc bảng người dùng, khóa, token, data source.
- 05:20:3xZ **bước 5a** (`e3/b5-cau-truc.{sh,txt}`): `sudo -n python3`, sqlite3 `file:…grafana.db?mode=ro`; chỉ `sqlite_master` và `pragma table_info` của `alert_rule`, `alert_instance`, `annotation`: cả ba bảng có; tên cột ghi trong file đầu ra. Không đọc bảng khác, không chép DB.
- 05:20:52Z, 05:21:07Z, 05:21:22Z **bước 5b** (`e3/b5-trang-thai.{sh,jsonl}`; mã thoát 1 chỉ do dòng `[ $lan -lt 3 ] && sleep` ở lần cuối): ba lần đọc chỉ các cột cần.
  - `alert_rule`: **15 luật, đúng tập 15 UID mong đợi** (11 uid của `bieu-thuc.json` + 4 `t072-thu-p95-*`), 0 thừa, 0 thiếu; cả ba lần như nhau. Không có luật nào khác trong tổ chức → con số `rules=15` trong log đúng là 15 luật này. Cấu hình từng luật khớp `bieu-thuc.json` (0 lệch): nhóm `t072-w4`/`t072-e3-thu`, `interval_seconds` 10, `for` 60 s (20 s cho `t072-live`), NoData OK (Alerting cho `t072-mat-do`, `t072-mat-gw`), exec_err Error, `is_paused` 0; thư mục "T-072 W4 cảnh báo", "T-072 E3 thử (gỡ trước E4)"; `updated` 2026-11-22 05:17:14 (= lúc provisioning).
  - `alert_instance`: **0 dòng** ở cả ba lần; `annotation` (`alert_id` > 0, từ 05:17:04Z): **0 dòng**. Cùng với log lúc khởi động "State cache has been initialized rules=15 states=0": Grafana bản này không ghi trạng thái Normal vào `alert_instance` và không ghi lịch sử khi không có chuyển trạng thái [suy luận từ quan sát; chưa thấy tài liệu]. Vì vậy DB **không** cho xác nhận theo từng UID rằng luật đã được đánh giá, chừng nào mọi luật còn Normal.
  - Bằng chứng đánh giá hiện có (gộp): log `plugin.prometheus` có 15 truy vấn `grafana_scheduler` mỗi tick 10 s, 180/180 ok tới 05:19:19Z; mỗi luật có đúng một truy vấn A; tổ chức có đúng 15 luật → **suy luận** mỗi luật được đánh giá mỗi tick, không luật nào lỗi truy vấn. Phân xử trực tiếp theo UID: ở bước 6, khi 4 luật thử chuyển Pending → Alerting thì `alert_instance`/`annotation` phải có dòng; luật thật vẫn chỉ có bằng chứng gián tiếp nếu chúng giữ Normal.
- **Giờ hiệu lực E3 (đề xuất):** **05:17:20Z** = tick đầu của bộ lập lịch có đủ 15 truy vấn ok, sau khi DB xác nhận 15 luật đã nạp lúc 05:17:14Z. Định nghĩa trong `ke-hoach-e3.md` bước 5 (từng luật thật được đánh giá ít nhất một lần, không Error) được đáp ứng ở mức suy luận như trên, không ở mức đọc trạng thái theo UID.
- 05:22:11Z: **dừng trước bước 6** (lượt tải `t071-e3-duong-01` của T-071). sha256 `results/T-072/SHA256SUMS-e3-b5`. Máy không đổi so với bước 4: `/opt/rca-lab` `d677244`, Grafana 15 luật, `flash-ticket-t072-bo-nhan` chạy. Lệnh cuối: `sha256sum e3/b5-* > SHA256SUMS-e3-b5`.
- 05:24:21Z **bước 6–7** (điều phối giao T-071 phát `t071-e3-duong-01`, T-073 đo dưới tải): lệnh nền trên laptop `results/T-072/e3/b7-cho.sh` (mỗi 60 s chạy `b7-mot-lan.sh` qua SSH, chỉ đọc: mốc `/srv/rca-lab/runs/t071-e3/DA-PHAT`, đếm tin `firing`/`resolved` theo `t072_uid` trong `runs/t072-e3-01/webhook.jsonl`, `tai_linux.py get --tag t071-e3-duong-01`). Thoát khi [4 luật thử có `firing` hoặc quá 25 phút từ DA-PHAT] **và** [lượt xong (Running=false) + 7 phút]; giới hạn cứng 75 phút. Nhật ký `e3/b7-theo-doi.jsonl`. Lúc 05:24:04Z: chưa có DA-PHAT, `get` lỗi (lượt chưa phát), bộ nhận 1 dòng (tin tay).
- 05:24:21Z → 06:03:07Z **bước 7**: lệnh nền chạy 38 lần đọc (`e3/b7-theo-doi.jsonl`), thoát "du_dieu_kien" lúc 06:03:07Z. DA-PHAT (mtime) 05:25:29Z; lượt `t071-e3-duong-01` StartedAt **05:25:26.48Z**, FinishedAt **05:55:27.46Z** (`tai_linux.py get`, Running=false từ ~05:56Z).
- 06:03:3xZ **bước 8** (`e3/b8-webhook.jsonl` = bản sao `runs/t072-e3-01/webhook.jsonl`, sha256 hai đầu khớp `b6f0de26…`): 9 dòng = 1 tin tay `/t072-tay` + 8 tin Grafana `/t072`. **Cả 4 luật thử có đúng 1 tin `firing` và 1 tin `resolved`** → nghiệm thu (b) của Minh đạt cho đường Grafana → bộ nhận: Grafana phát, bộ nhận lưu thân tin và giờ nhận, có cả resolved. Tin firing có `values` A (p95 lúc kích hoạt: booking 0,0495, event 0,0443, payment 0,0738, ticket 0,0362 s) và `endsAt` = 0001-01-01 (chỉ có nghĩa ở tin resolved); tin resolved `values` A = C = −1 (NoData). Trễ gửi (`nhan_webhook_utc` − `startsAt`): firing 7,35–9,35 s, resolved 7,49–9,46 s.
- 06:03:4xZ **bước 9** (`e3/b9-lich-su.{sh,json}`, chỉ đọc `alert_rule` id→uid, `annotation` từ 05:17:04Z, `alert_instance`; phân tích `e3/b9_phan_tich.py` → `e3/b9-doi-chieu.json`): 12 dòng lịch sử trạng thái, đều của 4 luật thử, mỗi luật Normal → Pending → Alerting → Normal (NoData).

  | luật thử | Pending | Alerting = `startsAt` | hết Alerting = `endsAt` | Pending sau load-start | hết sau load-end |
  |---|---|---|---|---|---|
  | booking | 05:25:50 | 05:26:50 | 06:00:20 | +23,5 s | +292,5 s |
  | event | 05:25:50 | 05:26:50 | 06:00:20 | +23,5 s | +292,5 s |
  | payment | 05:27:40 | 05:28:40 | 05:58:30 | +133,5 s | +182,5 s |
  | ticket | 05:27:40 | 05:28:40 | 05:58:30 | +133,5 s | +182,5 s |

  - **`startsAt` − giờ Pending→Alerting = 0,000 s; `endsAt` − giờ Alerting→Normal = 0,000 s, cả 4 luật → `da_doi_chieu_E3 = true`** (|Δ| ≤ 10 s, HOP-DONG I1 (d)). Soi trung gian vì kết quả "quá đẹp": cả hai giá trị là cùng thời điểm đánh giá của Grafana, nằm đúng lưới tick 10 s (…:50.000), nên Δ = 0 là điều cơ chế dự báo chứ không phải trùng hợp; Pending → Alerting đúng 60,0 s = `for`; payment/ticket vào Pending muộn hơn vì cần ≥ 30 request trong 5 phút (≈ 14/phút ×1); hết cháy sau load-end 3–5 phút do cửa sổ 5 phút và chặn 30 request. Mọi điểm khớp thiết kế `bieu-thuc.json`.
  - **11 luật thật: 0 chuyển trạng thái** trong suốt lượt ×1 1800 s (không cảnh báo nào; lượt ngoài mẫu số, chỉ là quan sát, không tính vào E4). Bằng chứng luật thật được đánh giá vẫn gián tiếp (log 15 truy vấn ok/tick), vì Normal không ghi vào DB.
  - `alert_instance`: vẫn 0 dòng lúc đọc (06:03Z, sau khi mọi luật về Normal).
  - Chưa làm: so t̂ offline (`cham_offline.py` với ngưỡng thử 0,005 s) với lịch sử trạng thái — cần T-071 xuất chuỗi `tin-hieu/*` của lượt E3 (`lenh-e3-duong-01.md` mục 4); không chặn bước 10.
- 06:04:31Z: **dừng trước bước 10** (checkout G) theo giao việc: chờ T-071 báo đã nhận lượt, T-073 báo job đo đã thoát, điều phối tạo commit G. Máy: `/opt/rca-lab` `d677244`, Grafana 15 luật (4 luật thử đang Normal), `flash-ticket-t072-bo-nhan` chạy. sha256 `results/T-072/SHA256SUMS-e3-b6-9`. Lệnh cuối: `py -3 e3/b9_phan_tich.py`.
- 06:05:35–06:05:36Z **bước 10a** (điều phối cho phép; kiểm 06:05Z không job, T-071 đã nhận lượt 05:55:27Z, job T-073 thoát 05:55:43Z; `e3/b10-checkout-g.{sh,txt}`): kiểm lại không job, cây sạch; fetch `origin t070-e3` → FETCH_HEAD `ecdeed2500bac813390ed372cb9f8f34b492653c`, cha `d677244`; diff N..G đúng 2 thay đổi (R100 `t072-thu-e3-go.yaml.mau` → `.yaml`, sha256 `f8b9523b…`; D `t072-thu-e3.yaml`). Checkout **trước `d677244` → sau `ecdeed2`**, cây sạch.
- 06:05:54Z **bước 10b** (`e3/b10-restart-g.{sh,txt}`): restart Grafana 06:05:54Z, health ok 06:06:01Z. Log: provisioning alerting 06:05:59Z xong, không lỗi (bỏ qua README, `t072-hoan-tac-n.yaml.mau`); "State cache has been initialized" **rules=11** states=18; tick đầu 06:06:00Z; mỗi tick 11 truy vấn `grafana_scheduler`, 86/86 ok (2 truy vấn lúc 06:05:5x thuộc tiến trình cũ trước khi tắt).
- 06:07:37Z, 06:07:59Z **bước 10c** (`e3/b10-db.{sh,jsonl}` = `b9-lich-su.sh` với mốc 06:05:54Z; `e3/b10-uid.txt`; chỉ đọc): `alert_rule` 11 UID = đúng tập `bieu-thuc.json`, 0 `t072-thu-*`; `alert_instance` 0 dòng; `annotation` từ 06:05:54Z: 0 dòng. Không kiểm được "giờ đánh giá của từng instance tăng" (bảng không có dòng; Normal không được ghi) → bằng chứng đánh giá 11 luật thật là suy luận từ log (11 truy vấn ok/tick, đúng 11 luật).
- Lỗi thao tác 06:06Z: một lệnh `sed` lỡ sửa `e3/b9-lich-su.sh` (file đã có hash trong `SHA256SUMS-e3-b6-9`); hoàn tác ngay, kiểm lại sha256 `98ecd1bb…` khớp bản đã ghi; script bước 10 chép ra file mới `b10-db.sh`.
- **Giờ hiệu lực E4 = 2026-11-22T06:06:00Z** (tick đầu sau G có đủ 11 truy vấn ok; DB đúng 11 luật thật). Giờ hiệu lực E3 = 05:17:20Z.
- **Bước 11:** bộ nhận `flash-ticket-t072-bo-nhan` chạy tiếp qua E4 (healthy, 9 dòng lúc 06:07Z), chỉ ghi `runs/t072-e3-01/`.
- 06:08:53Z: `results/T-072/e3.md` (tóm tắt E3, mốc, giới hạn, trạng thái máy). sha256 `results/T-072/SHA256SUMS-e3-b10` (`e3.md` trong đó). Kết thúc phần T-072 của S2: `/opt/rca-lab` exp-obs `ecdeed2` sạch; Grafana 11 luật. Tài nguyên còn giữ: container bộ nhận (tới hết E4), worktree. Lệnh cuối: `sha256sum e3/b10-* e3.md > SHA256SUMS-e3-b10`.
- 16:42:31Z **lượt 10** (điều phối giao theo CX-12: đối chiếu bộ chấm offline với Grafana trên E3; không dùng máy). Đầu vào: `results/T-071/e3/xuat-tin-hieu.json` (SHA256SUMS T-071 5/5 OK; định dạng T072-xuat-1, `bieu_thuc_sha256` `1a4aee67…`, 24 chuỗi, 0 khúc lỗi; điểm ở pha …6 s, tick Grafana ở …0 s) và `results/T-072/e3/b9-lich-su.json` (lịch sử trạng thái Grafana, `124622904e…`).
- 22/11 ~16:43Z: lượt 10 bị dừng nhầm (Minh, theo điều phối) sau khi đã ghi `e3_doi_chieu_offline.py` và `e3-doi-chieu-offline.json`. 23/11: làm tiếp từ checkpoint; kiểm lại script (dùng đúng code `cham_offline.py`, luật thử = bản sao p95 ngưỡng 0,005 s cùng chuỗi) và JSON (15 UID; mốc từng UID) → đúng, không chạy lại.
- 19:06:55Z: **đối chiếu offline ↔ Grafana trên E3** (`results/T-072/e3-doi-chieu-offline.md`): 4 luật thử: khoảng cháy 1 = 1, Pending/Alerting/hết cháy lệch **−4 s** cả 12 phép so (lưới xuất pha …6 s, tick Grafana …0 s; Alerting = Pending + 60 s hai phía; hết = NoData hai phía); không có dấu hiệu nạp mẫu trễ. 11 luật thật: 0 = 0 (chỉ khớp âm). Chưa có so dương offline ↔ Grafana cho luật lỗi, liveness, mất quan sát; 7 luật vẫn "chưa kiểm dương". sha256 `results/T-072/SHA256SUMS-e3-offline`.
- 19:07:16Z (giờ máy exp-obs) **tự kiểm E4 phía Grafana** (`e4/k1-kiem.{sh,txt}`, `e4/grafana-dem.json`; chỉ đọc; không truy vấn Prometheus): bộ nhận 9 dòng, dòng cuối 06:00:28Z, sha256 `b6f0de26…` = bản E3 → **0 tin trong E4**; bộ nhận running/healthy, Restart 0. Grafana StartedAt 06:05:55Z, RestartCount 0; `/opt/rca-lab` `ecdeed2`. DB: 11 luật đúng tập; `annotation` từ 06:05:54Z: **0 dòng** (không luật nào vào Pending); `alert_instance` 0. Log (`runs/t072-e3-01-cfg/grafana-log-e4.txt` `8c9303ca…`, 54.462 dòng): 781/781 phút 06:06–19:06Z đủ 66 truy vấn bộ lập lịch (6 tick × 11 luật), 51.566/51.566 ok; phút khác 66 chỉ 06:05 (tiến trình cũ) và 19:07 (đang đọc) → **không có phút Grafana bỏ đánh giá trong E4**; 1 dòng error (thiếu `provisioning/plugins`, có từ trước). Kết quả thô phía Grafana: 0 sự cố hệ thống, 0 sự cố quan sát. Chưa kết luận R5: cần phân loại phút E4 của T-071 (mẫu số) và chấm offline song song (kiểm rằng "0" không do biểu thức trả rỗng). sha256 `results/T-072/SHA256SUMS-e4-grafana`.

### Lượt 11 — chấm E4 so với R5 (23/11, điều phối giao 19:21Z; S3 đã đóng; không đổi máy)

- 19:21Z: `results/T-071/e4/SHA256SUMS` 14/14 OK; `phan-loai-phut.json` (`2fd1f9c4…`, bản khóa E4 `463cf596…`): 464 phút = khỏe ×1 383 + biên 43 + flash 38; cửa sổ 10:13–17:57Z 22/11 (sau giờ hiệu lực E4 06:06:00Z).
- 19:2xZ: giải nén `ra.tgz` (`e0b01d85…`) vào `results/T-072/e4/ra/`; `ra-SHA256SUMS` 424/424 OK. `chuyen_dinh_dang.py xuat` 9 lượt → `e4/xuat/` (24 chuỗi/lượt, 0 khúc lỗi; lưới pha …0 s); `phut` → `e4/phut.json`: trước = sau = {khoe-x1 383, bien 43, flash 38}, = tóm tắt T-071 → khớp. Điểm chồng giữa file lượt 21.862, 0 lệch.
- 19:2xZ: **offline** `cham_offline.py cham` (`nguong.json`, gom `T072-gom-3`) → `e4/cham-offline.json`: 0 khoảng cháy, 0 sự cố mọi lớp; mẫu số khỏe ×1 = 383 (= T-071), ≥ 360; 0 / 6 giờ, CI95 [0; 3,47].
- 19:22:00Z: **Grafana lúc chấm** (`e4/k2-grafana-luc-cham.{sh,txt}`, chỉ đọc): bộ nhận 9 dòng (`b6f0de26…` = E3); Grafana Restart 0; `ecdeed2`; `annotation` từ G: 0; log 10:00–18:09Z: 490/490 phút đủ 66 truy vấn, 32.340/32.340 ok → 0 phút khỏe bị loại vì Grafana không đánh giá. Ba nguồn (offline, lịch sử trạng thái, webhook) đều 0.
- 19:2xZ: **giải thích khác** (`e4_giai_thich_khac.py` → `e4/giai-thich-khac.json`): p95 4 route, liveness 8 đích, mat-do, mat-gw có điểm ở 100% bước khỏe ×1 và flash; không bước thô nào vượt ngưỡng; luật lỗi 0 điểm vì 5xx = 0 mọi bước (không thử thách luật lỗi). p95 duy trì 60 s lớn nhất / ngưỡng: booking 0,48, event 0,46, payment **0,84**, ticket **0,84**; so với M của E2: payment 1,26, ticket 1,53 (trôi hay dao động đuôi: chưa phân xử).
- 19:23:07Z: `results/T-072/bang-bao-dong-gia.{md,json}`: **R5 đạt** theo phép so đã khai (0 sự cố / 383 phút khỏe ×1); ghi rõ độ tin thấp, không chứng minh độ nhạy, 7 luật chưa kiểm dương, luật lỗi chưa bị thử thách. sha256 `results/T-072/SHA256SUMS-e4`. Bộ nhận vẫn chạy (chưa gỡ, theo giao việc). Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-e4`.

### Lượt 12 — mô tả trôi p95 payment/ticket E2 → E4 (23/11, điều phối giao 01:42Z; không máy, không Prometheus)

- 01:41Z: kiểm hash: `results/T-071/e2` 13/13, `e3` 7/7, `e4` 14/14; `ra` E2 377/377, E4 424/424; bản chuyển E2/E4 khớp `SHA256SUMS-e2-nguong` và `SHA256SUMS-e4` (4 mục lệch trong `SHA256SUMS-e2-nguong` là file đề xuất commit đã sửa ở lượt 8, đã ghi hash mới ở `SHA256SUMS-cx09`; không phải dữ liệu).
- 01:4xZ: `troi_p95.py` → `troi-p95-e2-e4.json`: phân bố thời gian request theo lượt từ counter bucket thô (`tho/gw-bucket`), đỉnh S và số request chậm tại đỉnh, tần suất vượt 0,5/0,7/0,84/1 × ngưỡng, độ phân tán số request > 0,1 s mỗi cửa sổ 5 phút. Kết quả chính: payment E4 không chậm hơn E2 ở mức cả lượt (tỷ lệ > 0,1 s tb 1,70% → 1,67%, p50 hơi giảm); ticket tb 0,64% → 0,58%, không đơn điệu theo lượt, lượt E4-06 1,28%; đỉnh S do 3–5 request chậm trong ≈ 72 request; ticket vượt 0,7θ ở E4 dồn 11/16 bước vào 10 phút đầu lượt; phân tán payment 0,79/0,84, ticket 1,12/1,29.
- 01:5xZ: `troi_p95_rui_ro.py` → `troi-p95-rui-ro.json` (mô hình Poisson, suy luận): request chậm tối thiểu trong 5 phút để p95 > θ: payment 9, ticket 4; kỳ vọng / 6 giờ: payment ≤ 0,009; ticket 0,07–0,09 ở tỷ lệ chậm trung bình, ≈ 1,0 nếu tỷ lệ như lượt E4-06 kéo dài.
- 01:44:27Z: `results/T-072/troi-p95-e2-e4.md`: trôi DB **không được dữ liệu hỗ trợ** ở độ phân giải bucket (chưa loại trừ); dao động đuôi do ít request là ứng viên chính; ticket là điểm yếu (4 request chậm đủ vượt); rủi ro E5 quanh pha phục hồi, demo ở các phút đầu sau khi bật tải; phép đo phân xử còn thiếu (độ trễ DB theo service, CPU/GC lượt E4-06, khoảng khỏe dài hơn). Không đổi ngưỡng, quy tắc. sha256 `results/T-072/SHA256SUMS-troi-p95`. Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-troi-p95`.

### Lượt 13 — tự soát W4, kiểm phần Codex `v2/`, đáp CX-19/19b (23/11, điều phối giao; không máy, không commit)

**Tự soát trước khi đọc kết luận phản biện** (AGENTS §5.7; chỉ dựa trên code và đầu ra của T-072):
- S1. `cham_offline.py::quy_ve`: lớp "đang cháy lúc bắt đầu" so `tp == t_dau` với `t_dau` = bước đầu **lưới xuất**, không phải đầu khoảng chấm (giờ hiệu lực E4 hoặc lượt đầu). Ở E2/E4 lưới mỗi lượt bắt đầu 600 s trước tải, nên lớp này gần như không bao giờ kích hoạt đúng nghĩa của `quy-tac-gom.json#/quy_ve_phut/dang_chay_luc_bat_dau`. Không làm sai E2/E4 (0 sự cố) nhưng là lỗi cài đặt.
- S2. Ca tự kiểm `dang-chay-luc-bat-dau` chỉ kiểm trường hợp chuỗi đúng ngay từ bước đầu lưới (t̂ = t0 + 60), tức kiểm đúng cài đặt lỗi ở S1, không kiểm nghĩa của quy tắc.
- S3. Pending: offline lấy `tp` = bước đúng đầu tiên của dãy đúng; nếu dãy bắt đầu trước khoảng chấm thì không phân biệt được "Pending trước giờ hiệu lực". Chưa có bằng chứng cho trường hợp luật đã cháy trước đầu khoảng (cả Grafana và offline).
- S4. Giờ hiệu lực E4 06:06:00Z: lấy từ "tick đầu 06:06:00" và đếm truy vấn gom theo 10 giây (06:06:0x có 11). Không có giờ đánh giá theo từng UID (Normal không ghi DB); con số 06:06:00 là mốc tick, chưa chắc là lúc truy vấn hoàn tất — cần đối chiếu dòng log thật.
- S5. Câu "lệch −4 s" trong `e3-doi-chieu-offline.md` đúng phạm vi bốn luật thử; nhưng STATE ghi gọn "4 luật thử lệch −4 s, 11 luật thật 0/0" — phải tránh đọc thành "bộ chấm khớp Grafana" cho luật thật.
- S6. Luật lỗi 5xx: chặn ≥ 3 lỗi/5 phút cộng ngưỡng 5% → tỷ lệ lỗi thấp kéo dài (ví dụ 2%) không bao giờ cháy; E4 không thử thách luật lỗi (0 lỗi 5xx). Lập luận ở WHY-d chỉ nói về lỗi lẻ.
- S7. WHY-110 (từ WHY-h): còn nói "θ ≥ max S(t) bảo đảm 0 cảnh báo trong mẫu E2 (trên lưới xuất)" — đúng với lưới E2 cùng pha; E3 cho thấy pha lưới khác Grafana tới 4–6 s, nên "bảo đảm" chỉ trên lưới xuất.
- 10:02Z: tiếp lượt 13 sau khi bị cắt (hạn mức); tự soát S1–S7 đã ghi.
- 10:03Z: đọc CX-19 F1–F6, CX-19b (thêm N1, N2, K1), `v2/README.md`, `dinh-chinh-cx19-co-hoc.md`.
- 10:03Z: kiểm phần Codex `v2/`: diff với `cham_offline.py` (0f94e459) chỉ gồm N1 (thoát 1 khi thiếu ngưỡng, trước khi ghi), cờ `chong-quan-sat` (giao nửa mở; chưa hết = vô hạn), `gia_tri_duy_tri` (max trong cửa sổ cho luật <), `--ra` giới hạn trong `v2/ra/`, `if __name__`; ba vị trí của T-072 chỉ đánh dấu. Chạy: `tu-kiem` 33/33, `thu_ca_gia.py` 9/9 ĐẠT. Điểm yếu xác nhận: `thu_ca_gia.py:34` chỉ kiểm `bool(khoang_chay)`, không kiểm đúng số khoảng. Hash 4 file Codex khớp README.
- 10:06Z: **phần của T-072 trong v2** (file mới, không sửa file Codex; `cham_offline_v2.py` vẫn `39f56bde…`): `v2/cham_offline_v2_claude.py` sinh bởi `v2/tao_v2_claude.py` (thay chuỗi có kiểm đúng 1 lần). Thay đổi: (1) `quy_ve(…, bat_dau)`: t̂ < đầu khoảng chấm → `dang-chay-luc-bat-dau` nếu còn cháy tại đầu khoảng (nửa mở), `truoc-khoang` nếu đã hết; không đếm; bỏ cách so `tp` với bước đầu lưới. (2) Cờ `pending-truoc-khoang` (Pending trước, Alerting từ đầu khoảng: vẫn đếm theo t̂, đúng quy tắc) và `pending-tu-dau-luoi` (dãy đúng từ bước đầu lưới: offline không thấy lịch sử trước). (3) Cờ `cua-so-lan` so với lớp phút, không với lớp đầu khoảng. (4) Mẫu số chỉ đếm phút trọn từ `bat_dau`. (5) `--bat-dau` cho lệnh `cham`. Pending giữ nguyên logic (chú thích). Ca giả: thay ca cũ "Pending ở t0 → đang cháy" bằng 9 ca (dãy đúng từ đầu lưới; Pending trước/Alerting sau đầu khoảng; Alerting đúng đầu khoảng; Pending đúng đầu khoảng; đang cháy; hết trước; hết đúng đầu khoảng nửa mở; mẫu số sau đầu khoảng; mất dò đúng 1 khoảng — kiểm số khoảng chính xác, sửa điểm yếu `thu_ca_gia.py:34`). `tu-kiem` 0 sai; đột biến 5/5 bị bắt (`>`→`>=` ở t_het, `<`→`<=` ở Pending, bỏ lọc mẫu số, tắt nhánh đầu khoảng, so cờ lấn với lớp mới).
- Không đổi phép chấm đã khóa: thay đổi làm cài đặt khớp đúng chữ `quy-tac-gom.json#/quy_ve_phut` (đã khóa); E2 và E4 có 0 khoảng cháy nên kết quả không đổi; **không chấm lại E4** (giao việc).
- **F5, bằng chứng "cháy trước đầu khoảng" cho E4:** lịch sử trạng thái Grafana (`annotation`, alert_id > 0) từ 06:05:54Z tới 19:22Z: 0 dòng (`e4/k1-kiem.txt`, `e4/k2-grafana-luc-cham.txt`) → không luật nào vào Pending/Alerting quanh giờ hiệu lực hay đầu cửa sổ E4 (10:13Z); trước G, 4 luật thử đã về Normal 06:00:20Z và bị gỡ ở G. Lớp `dang-chay-luc-bat-dau` của E4 = 0 theo bằng chứng trực tiếp, không theo cài đặt cũ.
- 10:07Z: `results/T-072/dap-cx19.md` (đính chính −4 s, N2, K1, chữ sửa WHY-110, tóm tắt v2_claude). sha256 `results/T-072/SHA256SUMS-dap-cx19` (gồm hash 3 file Codex trong `v2/`, không đổi).

**Bảng đáp CX-19 / CX-19b** (tự soát S1–S7 ghi trước khi đọc; cột "Minh quyết" để trống):

| Điểm | Kết luận của người làm | Bằng chứng / việc đã làm | Còn lại | Minh quyết |
|---|---|---|---|---|
| F1 giờ hiệu lực E4 | **Đúng** | Kế hoạch bước 5/10: đánh giá **sau** health; health thấy ok 06:06:01Z (dò 2 s), tick 06:06:00 chạy trước đó → mốc theo định nghĩa là 06:06:10Z. Trùng tự soát S4. Đính chính cơ học của Codex (`dinh-chinh-cx19-co-hoc.md`) đúng vị trí; R5 không đổi (E4 bắt đầu 10:13Z) | Điều phối áp đính chính vào các file | |
| F2 offline ↔ Grafana | **Đúng** | 12 số không độc lập; xuất trước khi cửa sổ kết thúc; so âm bắt đầu trước giờ hiệu lực E3; booking 0,0931 < 0,098 → câu "không giữ 60 s" sai. Đính chính ở `dap-cx19.md` §1, rút lại "≤ 10 s" và "không thấy nạp trễ" | Không tách được pha với nạp trễ bằng dữ liệu có | |
| F3 lý do loại phương án WHY-110 | **Đúng** (độc lập E4); **đúng một phần** (phân vị: "cho phép" vượt bước là lý do hợp lệ, "tất yếu sinh cảnh báo" là sai) | Chữ sửa ở `dap-cx19.md` §4 | Minh duyệt chữ WHY-110 | |
| F4 phạm vi B2 | **Đúng**, thuộc T-071 | Văn bản T-072 không có câu về B2; `bang-bao-dong-gia.md` chỉ dẫn "phân loại phút T-071" | T-071 ghi phạm vi 12 container | |
| F5 ba nhánh khi có cảnh báo | **Đúng cả ba** | (a) đầu khoảng: sửa trong `v2/cham_offline_v2_claude.py` (trùng S1–S3), 9 ca giả, đột biến 5/5; (b) cờ `chong-quan-sat`: Codex sửa trong v2, tôi kiểm 6 ca giao khoảng đạt — tự soát của tôi **không** tìm ra điểm này; (c) `<` lấy max trong cửa sổ: Codex sửa, kiểm 2 ca đạt. E4 = 0 khoảng cháy nên không đổi kết quả; bằng chứng "cháy trước đầu khoảng" E4 = 0 dòng lịch sử | Tích hợp v2_claude làm bộ chấm cho lần chấm sau cần Minh/điều phối chọn | |
| F6 bàn giao máy | **Đúng**, thuộc điều phối; phần T-072: LOG thiếu prompt soát kết quả ở mục cuối | Prompt kiểm lại ở cuối lượt này | Điều phối đồng bộ `TRANG-THAI` | |
| K1 ghi file trên exp-obs | **Đúng** | `k1-kiem.sh` mô tả "CHỈ ĐỌC" nhưng ghi `grafana-log-e4.txt` vào vùng `t072-*` (I9); không đổi Grafana/Prometheus. Vị trí scratchpad: `dap-cx19.md` §3 | — | |
| N1 thiếu ngưỡng vẫn thoát 0 | **Đúng** | Codex sửa trong v2 (thoát 1, báo route, không ghi JSON); tôi chạy ca giả của Codex: đạt. E2 thật đủ 8/8 ngưỡng | — | |
| N2 "khi và chỉ khi" cho 5xx | **Đúng** | Chỉ là điều kiện đủ (chặn ≥ 3 lỗi); `dap-cx19.md` §2; trùng một phần tự soát S6. M lỗi E2 = 0 nên θ không đổi | Chữ sửa WHY-110 | |
| CX-24b: `thu_ca_gia.py:34` chỉ kiểm `bool` | **Đúng** | Ca `mat-do-dung-mot-khoang` và tham số `so_khoang` trong v2_claude kiểm đúng số khoảng | Không sửa file Codex | |

**Điểm tự soát chưa có trong phản biện:** S5 (dòng STATE đọc gọn "4 luật thử lệch −4 s, 11 luật thật 0/0" dễ hiểu thành "khớp") — đã sửa ở dòng STATE lượt này; S6 phần "tỷ lệ lỗi thấp kéo dài không cháy" — ghi giới hạn ở `dap-cx19.md` §2.

### Kết thúc lượt 13 (10:07Z)

1. **Đã làm:** tự soát; kiểm phần Codex `v2/` (đạt, một điểm yếu ca giả); viết `v2/cham_offline_v2_claude.py` (quy_ve đầu khoảng, cờ Pending, ca giả, đột biến); đính chính −4 s, N2, K1; soạn chữ sửa WHY-110; bảng đáp.
2. **File đã đổi:** mới `results/T-072/dap-cx19.md`, `v2/cham_offline_v2_claude.py`, `v2/tao_v2_claude.py`, `v2/ra/tu-kiem-v2-claude.json`, `v2/ra/tu-kiem-kiem-claude.json`, `SHA256SUMS-dap-cx19`; LOG này; dòng T-072 STATE. Không sửa file Codex, `e3-doi-chieu-offline.md`, `docs/WHY.md`, file khóa.
3. **Kiểm:** `tu-kiem` v2 (Codex) 0 sai, `thu_ca_gia.py` 9/9; `tu-kiem` v2_claude 0 sai; đột biến 5/5.
4. **Còn mở / cần quyết:** Minh duyệt chữ WHY-110; chọn bộ chấm cho lần sau (v2_claude); điều phối áp đính chính 06:06:10Z và đồng bộ TRANG-THAI; 7 luật chưa kiểm dương; trôi p95 ticket chưa phân xử (`troi-p95-e2-e4.md`). Tài nguyên giữ: container bộ nhận, worktree. Lệnh cuối: `sha256sum … > results/T-072/SHA256SUMS-dap-cx19`.

**Prompt cho Codex kiểm lại** (Minh chuyển; chép nguyên văn Prompt chung và khối "Kiểm lại phản hồi và sửa" của `docs/review-prompt.md`; không có khối trọng tâm cổng cho G6 trong mẫu):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-072 (tasks/T-072-w4b-luat-canh-bao/), phản hồi của người làm cho CX-19/CX-19b và phần sửa bộ chấm v2.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10 (W4 luật cảnh báo), chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-072-w4b-luat-canh-bao/SPEC.md; tasks/T-070-dieu-phoi-giai-doan-2/{SPEC.md,HOP-DONG.md}; docs/WHY.md WHY-103…WHY-110; results/T-072/{quy-tac-gom.json,quy-tac-chon-nguong.json,nguong.json,ke-hoach-e3.md,e3.md,e3-doi-chieu-offline.md,bang-bao-dong-gia.md,troi-p95-e2-e4.md}.
- Phản biện và phản hồi trước: results/T-070/codex/CX-19-tin-cuoi.md, CX-19b-tin-cuoi.md, CX-24/CX-24b (results/T-072/v2/README.md), CX-25/CX-25b (results/T-072/dinh-chinh-cx19-co-hoc.md); phản hồi người làm: tasks/T-072-w4b-luat-canh-bao/LOG.md lượt 13 và results/T-072/dap-cx19.md.
- Code và kết quả liên quan: results/T-072/v2/ (cham_offline_v2.py của Codex, cham_offline_v2_claude.py và tao_v2_claude.py của người làm, ra/), results/T-072/cham_offline.py, SHA256SUMS-dap-cx19; lệnh: py -3 -X utf8 -B results/T-072/v2/cham_offline_v2_claude.py tu-kiem --ra <tên>.json.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc file được phép>.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.
```

```text
Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.
```
