# T-071 — W4a: chuẩn bị DB và thu nền cho luật cảnh báo

- **Trạng thái:** đã duyệt triển khai 20/11/2026 theo quyền Minh cho phiên điều phối (SPEC T-070, nguyên văn ở đó), **trừ** các mục "chờ Minh". Soạn bởi phiên điều phối T-070, trong phạm vi kế hoạch bản 5.
- **Người làm:** Claude (phiên `nen-w4`, mức High).
- **Người phản biện:** Codex.
- **Thuộc gói MRP:** P9, P10 — **Cổng:** chuẩn bị G6.

## Mục tiêu

Kế hoạch giai đoạn 2 §8.2 W4: "Ngưỡng chọn trên đêm nền 1, đo báo động giả trên đêm nền 2 … Báo động giả dưới ngưỡng khai trước". Bản 5 thay "đêm" bằng hai khoảng tải nền E2, E4 (`tasks/T-070-dieu-phoi-giai-doan-2/SPEC.md`). MRP §2.3 (hai mức phát hiện) và Q-28 (phần phát hiện demo ngang phần RCA).

Task này **thu dữ liệu nền và lập mẫu số** cho T-072. Nó trả lời: trong mỗi khoảng, bao nhiêu phút là "khỏe" theo tiêu chí độc lập, ở mức tải nào; các chuỗi luật cần có đủ không. Nó không chọn ngưỡng (T-072) và không kết luận về luật.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác | Phép kiểm | Phần còn mở |
|---|---|---|---|
| Ngày sự kiện ở Ticket/Payment có khớp Event/Booking sau E1 không? | Sửa nhầm dòng; cột khác nghĩa | Lưu giá trị cũ; cập nhật đúng một dòng mỗi bảng theo giá trị đích; đọc lại cả bốn phía | — |
| Sức chứa vé còn đủ cho E2 + E4 + E5? | Vé hết giữa khoảng làm hành trình mua lỗi, bị đếm nhầm là "không khỏe" hoặc báo động | Đọc `configured_capacity`, `held`, `purchased` của ticket type tải; ước nhu cầu từ số đơn/chu kỳ đo ở T-069 | Thiếu → lỗi chặn E2, trình Minh (nâng sức chứa là sửa dữ liệu) |
| Giờ nào khỏe? | "Không tiêm" ≠ khỏe; mất quan sát; quota; suy giảm thật do tải | Tiêu chí khỏe khai trước (I2 `HOP-DONG.md`); phân loại từng phút | Flash chỉ mô tả |
| Các chuỗi luật xuất được suốt hai khoảng? | Nhãn route trống, chuỗi gián đoạn, Prometheus khởi động lại | Xuất theo khúc đúng biểu thức T-072 chốt; đếm mẫu từng phút | — |

## Đầu vào

- Bằng chứng trạng thái: `docs/techstack/ban-giao-dieu-phoi-2026-11-20/README.md` §2; `results/T-069/sua-su-kien/{truoc,sau}.jsonl`, `results/T-069/kiem_db.sh`, `results/T-069/phan-tich/kiem-db.txt`, `results/T-069/thu/t069-chinh/tai-create-order.json` (số đơn/chu kỳ), `results/T-069/thu/t069-chinh/tai-out/t3-124242f0/` (cấu hình flash khỏe).
- Repo lab `407b4f5`: `load/controller/tai_linux.py`, `load/controller/README.md`, `load/scenarios/purchase-journey.js`, `load/profiles/purchase-journey.json`, `campaigns/runner/runner4.py`, `inventory/`. Khóa và cách gọi máy: AGENTS §12, `results/T-058/dem-2026-11-10/remote.ps1`. Không đọc `.env`, `grafana.env`, `~/.bash_history`, `~/.ssh`.
- Hợp đồng `tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md` (I2, I3, I4, I7, I8, I9, I11, I13), lịch `LICH-MAY.md`.

## Đầu ra

- `results/T-071/e0-trang-thai.md`: kiểm chỉ đọc khi mở S0.
- `results/T-071/e1/`: `truoc.jsonl`, `sau.jsonl` (bốn bảng ngày sự kiện), `suc-chua.json` (sức chứa, đã bán, đang giữ, nhu cầu ước, kết luận đủ/thiếu), `moc-db.json` (thời điểm, số dòng thật từng bảng chính, đơn dở theo trạng thái, độ sâu hàng đợi RabbitMQ, trạng thái mock, đường dẫn và sha256 bản dump).
- `results/T-071/khai-truoc-e2.json` (và `khai-truoc-e4.json`): danh sách lượt (tag, mức tải, thời lượng, thứ tự), tiêu chí khỏe, quy tắc biên, phân loại mất quan sát/quota/suy giảm, phút khỏe cần; sha256 ghi LOG trước khi phát.
- `results/T-071/xuat_chuoi.py` + đầu ra xuất mỗi khoảng `results/T-071/e2/`, `e4/` (chuỗi luật, nhãn đầy đủ, số mẫu theo phút), `phan-loai-phut.json` (khỏe / biên / mất quan sát / quota / suy giảm / flash), `SHA256SUMS`.
- `thay-doi-may.md`: mọi thay đổi trên máy, giờ, hoàn tác.

## Phạm vi ghi

Ngoài `LOG.md` của task này và dòng T-071 trong `docs/STATE.md`:
- `results/T-071/`.
- Repo lab: worktree `D:/Project/rca-lab-wt/T-071` nhánh `t071-nen` từ `407b4f5` (I10). Chỉ khi Minh chọn phương án A (R7): `load/controller/chuoi_tai.py` (bộ chuỗi lượt trên server, gọi `tai_linux.py start/get/receive` theo danh sách khai trước, ghi tag từng lượt vào nhật ký trước khi phát, không sửa `tai_linux.py`). Không commit/push khi Minh chưa duyệt.
- exp-app (khung S0, S1, S3): đúng các dòng của sự kiện `3e7c1df9-ada4-4081-94a1-548b80a5da86` trong `ticket_db.tbl_event_access_snapshots` và `payment_db.tbl_event_finance_snapshots` (chỉ các cột ngày lệch giá trị đích); thư mục `/home/ubuntu/t071/` (dump, script tạm).
- Máy tải: `/srv/rca-lab/load-runs/t071-*`; file token `/etc/rca-lab/load-secret/l1-tokens.json` (do `tai_linux.py` cấp mới mỗi lượt).
- exp-obs: `/srv/rca-lab/load-controller/` (do `tai_linux.py` ghi), `/srv/rca-lab/runs/t071-*`; nếu phương án B/C: sổ tiêm qua user `ledger` và `/srv/rca-lab/m1/*` do runner ghi.

**Không sửa:** `tai_linux.py`, `purchase-journey.js`, `runner4.py`, lõi M1, cấu hình V082, image/compose FlashTicket, Grafana, file của task khác.

## Các bước

0. **Mở S0 (chỉ đọc):** exp-app: container và image (bản ghim `36a3725`), không có tiêm lỗi đang bật (`inj3.py verify`), `/opt/rca-lab` commit và cây sạch; máy tải: không có container `rca-tai-`; exp-obs: không có tiến trình `runner4.py`, `chuoi_tai.py`, không có file STOP, `/opt/rca-lab` commit và cây sạch, Prometheus sống. Ghi `e0-trang-thai.md`. **Lệch README theo cách ảnh hưởng an toàn (job không rõ chủ, hash lệch, cây bẩn) → dừng, giữ nguyên, báo điều phối.**
1. **E1a (chỉ đọc):** ngày sự kiện ở bốn DB; sức chứa ticket type `ffb36fc7-e30a-4efe-987f-ca5533520453`; đơn theo trạng thái; hàng đợi; mock. Ước nhu cầu: từ `tai-create-order.json` (đơn tạo/chu kỳ ×1) suy cho 2 khoảng × (380 phút ×1 + 40 phút ×3) + E5 3 chu kỳ, cộng biên 50%. Thiếu → dừng phần E2, báo điều phối (lỗi chặn).
2. **E1b (sửa dữ liệu, Minh cho trong quyền triển khai):** trong một giao dịch mỗi DB: lưu giá trị cũ → `truoc.jsonl`; `UPDATE … WHERE event_id = '3e7c1df9-…'` chỉ các cột ngày lệch, đặt bằng giá trị cùng nghĩa ở Event/Booking; kiểm đúng 1 dòng bị đổi, sai thì `ROLLBACK`; đọc lại bốn phía → `sau.jsonl`. Cột nào không rõ ánh xạ thì không sửa, báo điều phối. Mất kết nối giữa chừng: đọc lại để biết DB nào đã khớp; không cộng thêm.
3. **E1c — mốc DB:** kiểm dung lượng đĩa exp-app; `pg_dump` các DB của FlashTicket vào `/home/ubuntu/t071/db-moc/<UTC>/`, sha256 từng file; ghi `moc-db.json`. Dump > 5 GB hoặc đĩa trống < 2× dump → dừng, báo.
4. **Chuẩn bị E2 (không máy):** sau khi T-072 chốt biểu thức (`results/T-072/bieu-thuc.json`), viết `xuat_chuoi.py` (truy vấn theo khúc ≤ 10 phút, nghỉ 0,3 s, ghi lỗi khúc) và chạy thử trên một cửa sổ cũ đã có (lượt 1 giờ T-067) để chứng minh xuất được; viết `khai-truoc-e2.json`. Nếu Minh chọn A: viết `chuoi_tai.py` ở worktree, kiểm bằng chạy khô (không phát tải), trình diff cho điều phối.
5. **E2 (khi điều phối mở S1 sau cổng E2):** phát danh sách lượt bằng phương án Minh chọn, chạy nền trên server; theo dõi bằng lệnh nền thoát khi lượt cuối kết thúc; mỗi lượt `receive` và kiểm hash; xuất chuỗi ở khoảng chuyển lượt hoặc sau khoảng; phân loại phút. Hết ngân sách thì dừng, không kéo dài.
6. **E4 (S3):** như bước 5 với `khai-truoc-e4.json`; chỉ tính sau giờ luật có hiệu lực (T-072 ghi).
7. **Báo cáo:** LOG mục 7 AGENTS; prompt Codex soát kết quả.

## Kiểm đúng đắn

- Đọc lại dữ liệu sau mỗi lần sửa; đếm đúng số dòng.
- Mỗi lượt: hash hai đầu khớp; `summary.json` (hành trình xong, `dropped_iterations`, 429, lỗi HTTP); trạng thái container (`ExitCode`, `OOMKilled`); Prometheus sống và số mẫu/phút.
- Tách lỗi hạ tầng (tải không khởi động, mất kết nối, Prometheus khởi động lại) khỏi tình trạng hệ thống; không ghi lỗi hạ tầng thành giờ khỏe hay suy giảm.

## Tiêu chí xong

1. E1: ngày khớp bốn phía, có bản trước/sau; sức chứa có kết luận; mốc DB có hash.
2. Mỗi khoảng: đủ lượt theo khai trước hoặc ghi rõ lượt hỏng và lý do; chuỗi xuất có hash; phân loại phút; số phút khỏe ×1 thực (báo "chưa đủ sáu giờ khỏe ×1" nếu < 360).
3. Không ghi ngoài phạm vi; mọi thay đổi máy có ở `thay-doi-may.md`.

## Không làm

Chọn ngưỡng, viết luật (T-072); tiêm lỗi; khôi phục DB (I13); thử tải tối đa; sửa bộ tải.

## Chi phí, chạy nền, xử lý lỗi (luật 8, 19, 21)

- E1: dưới 1 giờ, không tốn giờ tải.
- E2, E4: mỗi khoảng ~7 giờ tải danh nghĩa (380 phút ×1 + 40 phút ×3) + chuyển lượt (chưa đo; đo ở lượt đầu). **Duyệt lượt dài chờ Minh (R7)**.
- **Phương án tải chờ Minh (R7):** A (chuỗi lượt 60 phút, cần `chuoi_tai.py` mới) / B (`runner4.py` `RCA_PHASE=600`, 14 lượt) / C (`runner4.py` `RCA_PHASE=1200`, flash ×3 40 phút chưa từng chạy). B/C kéo theo M1 và `xuat_bo_sung` truy vấn Prometheus sống trong chu kỳ sau (trái I3) và đầu dò `inj3`.
- **Lỗi ở 10%, 50%, 99% của một khoảng 7 giờ:**
  - Lỗi cục bộ một lượt (tải không khởi động, container lỗi): chỉ mất lượt đó (≤ 60 phút); bù bằng lượt mới cuối danh sách nếu còn trong ngân sách; giữ lượt hỏng.
  - Mất kết nối laptop: với A/B/C chạy trên server, 0 phát lại; khi nối lại kiểm tag, container, nhật ký, manifest rồi `receive`.
  - Lỗi nguồn chung (sai biểu thức, mất telemetry, Prometheus khởi động lại dài, sai tiêu chí): phát hiện ở 10% / 50% / 99% ảnh hưởng ~42 phút / ~3 giờ 30 / ~6 giờ 56 đã thu. Phát hiện sớm bằng kiểm số mẫu sau mỗi lượt. Phần hỏng giữ, ghi loại; chạy bù cần điều phối trình Minh chi phí.
  - Sửa tiêu chí sau khi xem dữ liệu: ghi là sửa sau, giữ kết quả lần đầu.

## Rủi ro và điều chưa chắc

- Ánh xạ cột ngày giữa Event và hai bản sao chưa kiểm trên schema thật [chưa kiểm]; nếu không rõ, không sửa.
- DB tích lũy làm p95 trôi giữa E2 và E4 là điều cần đo, không phải lỗi (Q3).
- Hạn bán 02/12 22:16Z: E2–E5 phải xong trước; kiểm lại ở E1.

## Prompt bàn giao

Ở `LOG.md`, mục cuối mỗi lượt (AGENTS §7, §9).
