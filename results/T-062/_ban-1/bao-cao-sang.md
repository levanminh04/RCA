# T-062 — Báo cáo sáng 12/11/2026

Người viết: Claude (phiên điều phối tiếp quản, nhận 18:30Z 11/11). Nguồn số: các file dẫn trong bài. Mọi thứ chưa commit vào repo RCA.

## 1. Tóm tắt một phút

- **FlashTicket bản quan sát mới đang chạy trên `exp-app`**: nhánh `rca/quan-sat-log`, commit `6b21ed55`. PR **nháp** [levanminh04/flash-ticket-platform#17](https://github.com/levanminh04/flash-ticket-platform/pull/17) có **CI xanh** (14 check đạt), **chưa merge**.
- **Dữ liệu tốt hơn rõ** so với T-058:
  - Log nối được span: 7.500/7.500 dòng (T-058: 0).
  - Gateway ghi log mọi request.
  - 7 service cùng một commit.
  - Chi tiết: `kiem-du-lieu/bao-cao-B1.md`.
- **Lượt phát triển đầu (E1) với M1 bản khóa P7, không chỉnh:** 9 chu kỳ 10/10/10 phút, gồm 5 ô lỗi, 3 ca bình thường và 1 FLASH-HEALTHY.
  - **5/5 ô lỗi: thành phần đáp án ở hạng 1.**
  - **4/4 ca không lỗi: M1 vẫn kết luận "có nguyên nhân".** Đây là báo động giả, theo định nghĩa đề xuất.
  - n = 1 mỗi ô, chỉ để định hướng chặng 4.
- **Giao diện G2 dùng được trên Grafana `exp-obs`:** 9 sự cố thật, trang phát lại có đáp án tách riêng.
- **REDIS-BOOK bị bỏ:** hỗn hợp tải không đi qua Redis của Booking.
- **Nhiều việc chờ Minh** (mục 8).

## 2. Kết quả từng ô (M1 bản khóa P7, chế độ a)

Bảng sinh tự động từ `ket-qua/phat-lai/bang-cham.json` (`bang-ket-qua.py`). Đáp án chỉ được ghép **sau** khi đã băm cả 9 kết quả (`ket-qua/manifest-ket-qua.json`).

| Ca (mã mờ) | Ô lỗi | Đáp án T-059 (tập chấp nhận) | M1: kết luận | M1: hạng 1 | Hạng tốt nhất của đáp án | Vai trò M1 gán cho đáp án |
|---|---|---|---|---|---|---|
| `1ad3afeb` | EVENT-DB-LAT | event-service → event_db (event-service, event_db) | CAUSE_FOUND | event-service | **#1** | event-service: nghi là nguồn; event_db: bình thường |
| `a89954d1` | HTTP5-EVENT | event-service | CAUSE_FOUND | event-service | **#1** | nghi là nguồn |
| `2e2a5541` | SLOW-BOOK | booking-service | CAUSE_FOUND | booking-service | **#1** | nghi là nguồn |
| `f728fce2` | NET-GW-BOOK | api-gateway → booking-service (api-gateway, booking-service) | CAUSE_FOUND | booking-service | **#1** | booking: nghi là nguồn; gateway: bị kéo theo |
| `bf17acbf` | CPU-BOOK | booking-service | CAUSE_FOUND | booking-service | **#1** | nghi là nguồn |
| `a5539fba` | bình thường | root = null | CAUSE_FOUND | keycloak | — | — |
| `6c1a9fd8` | bình thường | root = null | CAUSE_FOUND | event-service | — | — |
| `e8661e0a` | bình thường | root = null | CAUSE_FOUND | event-service | — | — |
| `00eaea92` | FLASH-HEALTHY (5→15→5 req/s) | root = null | CAUSE_FOUND | payment-service | — | — |

Cả 9 ca: M1 trạng thái OK, hai lần chạy trùng SHA, adapter và config khớp hash khóa T-058 (`ca/_nguon/`).

**Can thiệp có thật trong E1** (số phía k6, độc lập với M1; `chay/k6-theo-pha.md`; nền là khoảng 250 ms trễ mạng AWS→Oracle):

| Ô | Thay đổi so với pha nền |
|---|---|
| EVENT-DB-LAT | GET event p50 264 → 602 ms |
| HTTP5-EVENT | 1.498 lỗi 5xx ở GET event, 0 ở route khác |
| SLOW-BOOK | GET order p50 260 → 1.261 ms |
| NET-GW-BOOK | GET order p50 248 → 549 ms |
| CPU-BOOK | +9–14 ms (nhẹ); cgroup Booking bị throttle (đầu dò trong sổ) |
| FLASH-HEALTHY | 8.360 request so với khoảng 3.000, không có 5xx/429, 3 lượt rơi |
| Ca bình thường | không đổi |

**Đọc kết quả thế nào** (quan sát → suy luận → còn mở):

- **Quan sát.** Trên ca lỗi, thành phần đáp án luôn đứng hạng 1. Trên 4 ca không lỗi, M1 vẫn gán một thành phần "nghi là nguồn" (keycloak, event-service ×2, payment-service).
- **Suy luận (chưa kiểm).** Ở chế độ a, bộ điều phối đưa sẵn mốc t nên M1 luôn đi tìm nguyên nhân. Bản P7 không phân biệt được nhiễu nền với lỗi thật trên dữ liệu FlashTicket. Do đó "hạng 1 ở ca lỗi" chưa đủ nói M1 tốt: chưa so độ nổi bật của thành phần hạng 1 giữa ca lỗi và ca bình thường. Bằng chứng cần thêm: khóa xếp hạng (`khoa_m1`) và số bằng chứng trên ca lỗi so với ca bình thường; thêm lặp mỗi ô.
- **NET-GW-BOOK.** Root là một cạnh (trễ mạng giữa Gateway và Booking). M1 đổ cho Booking, phía bị gọi, trong khi phía server Booking xử lý gần mức nền. M1 không biểu diễn được "lỗi nằm trên cạnh". Đây là đúng loại câu hỏi đồ thị mà chặng 4 cần.
- **CPU-BOOK.** Tác động lên người dùng rất nhỏ nhưng M1 vẫn chỉ đúng. Có thể nhờ kênh CPU container; chưa xác định kênh nào quyết định.
- n = 1 mỗi ô: không kết luận hiệu quả, không dùng để chọn biến thể.

## 3. Cách mở giao diện

1. Mở đường hầm (PowerShell hoặc Git Bash trên laptop):

```bash
ssh -i "D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key" -N -L 3000:10.0.0.215:3000 ubuntu@213.35.116.128
```

2. Trình duyệt: `http://localhost:3000` → đăng nhập Grafana như thường.
   - **Trang chính** (không đáp án): `http://localhost:3000/d/rca-g2` — "RCA — xem sự cố (G2)".
   - **Trang phát lại** (có đáp án): `http://localhost:3000/d/rca-g2-phat-lai`.
3. Chọn sự cố ở bảng danh sách (9 ca T-062, mới nhất trước). Bấm một nút trên đồ thị để xem chi tiết và liên kết sang Tempo/Loki/Prometheus đúng cửa sổ.

Chi tiết panel, ảnh chụp (gồm 4 ảnh ca thật `a5539fba`) và giới hạn ở `giao-dien/XONG.md`. Phiên giao diện **chưa xem được trực tiếp trên exp-obs**, vì cần mật khẩu Grafana mà Claude không nhập. Bản kiểm dùng Grafana thử cùng phiên bản trên laptop, đọc đúng file và dữ liệu exp-obs. **Việc đầu tiên sáng nay: Minh mở và nói giao diện có ổn không.**

## 4. Đã làm (theo bước SPEC)

| Bước | Kết quả | File |
|---|---|---|
| A1 | Review diff 78 file sửa + 62 file mới, không thấy lỗi chặn (ghi chú 6 điểm). 6 commit nhóm + 1 merge `origin/main` (PR bị xung đột vì `main` có 15 commit mới; gỡ 4 xung đột). CI xanh. | `ha-tang/A1-review.md` |
| A2 | Build ARM trên exp-app, 2 lượt (lượt 2 = `6b21ed55` đang dùng). 7 service health, telemetry tới exp-obs. Keycloak giữ image cũ. | `ha-tang/A2-kiem.md`, `ha-tang/thay-doi.md` |
| B1 | Bộ kiểm R-01–R-10 chạy trên gói ca, so với T-058 | `kiem-du-lieu/bao-cao-B1.md` |
| C1 (Codex) | Máy tải AWS: Docker, k6 1.4.2 ghim digest, chrony, token PKCE tự làm mới, bộ lệnh Start/Stop/Receive. Chạy thử 5 phút: 1.501 request, 0×401, 0 rơi. | `tai/bao-cao-C1.md` |
| D1 | Toxiproxy cố định (JDBC Event, Redis Booking, Gateway→Booking qua cổng Eureka 18082), hook `rca-test`, đốt CPU trong cgroup Booking (quota 1 CPU ở mọi pha) | `tiem-loi/o-loi.md`, `tiem-loi/scripts/` |
| D2 | 5 ô đạt, REDIS-BOOK không đạt → bỏ; EVENT-DB-LAT hạ 200 → 30 ms (200 ms làm GET event +6,3 s và k6 rơi 197 lượt) | `tiem-loi/d2-tong-hop.md` |
| E1 | 9 chu kỳ 20:39–01:20Z, bộ chạy tự động, sổ hash nối dòng | `chay/`, `tiem-loi/so.jsonl`, `chay/HO-SO-LUOT-E1.md` |
| E2 | Chuyển 0.2 (bộ chuyển T-061 không sửa), băm đợt, chỉ mục, phát lại, đẩy lên exp-obs | `e2.py`, `ket-qua/` |
| G1 (phiên Claude riêng) | Dashboard G2 + trang phát lại | `giao-dien/` |
| H1 | Báo cáo này, đề xuất SPEC chặng 4 | `bao-cao-sang.md`, `spec-chang-4-de-xuat.md` |

## 5. Sự cố trong đêm và cách xử lý

1. **Bộ phân loại an toàn của ứng dụng** chặn mở iptables, gọi Codex bỏ sandbox và mở phiên G1. Minh bật chế độ bỏ qua quyền lúc khoảng 18:37Z.
2. **PR xung đột với `main`.** Bản triển khai đầu dựng trên `main` cũ hơn cả bản T-058. Đã merge `origin/main` vào nhánh, build và triển khai lại.
3. **D2 lần 1 không có tải:** token có BOM, k6 thoát ngay. Bộ chạy không phát hiện. Đã sửa (gỡ BOM, kiểm k6 còn sống sau 20 s) và chạy lại D2.
4. **Collector exp-app ghim log theo ID container cũ (KP-19).** Từ 18:50Z không thu log của container mới; phát hiện nhờ bộ kiểm R-06/R-08. Đã dừng E1 lượt đầu bằng STOP, sửa `include`, chạy lại E1. Lúc đọc bù, một số lô log trước E1 bị từ chối vì quá 4 MB.
5. **Thử M1 trên cửa sổ có recreate container:** adapter P7 dừng vì "nhiều chuỗi metric cho một thực thể". Các chu kỳ E1 không recreate nên không gặp (`chay/thu-ong-M1.md`).

## 6. Dữ liệu nằm đâu

- Laptop `results/T-062/`:
  - Gói ca + đầu ra M1: `ca/<mã>/<mã>.tgz` (đã giải nén bên cạnh).
  - Kết quả 0.2: `ket-qua/`; phát lại: `ket-qua/phat-lai/`.
  - Tải k6: `tai/out/<tag>/`.
  - Sổ tiêm lỗi: `tiem-loi/so.jsonl`.
  - Hash toàn bộ: `manifest.json`.
- exp-obs:
  - `/opt/flash-ticket-rca/cases|outputs/<mã>` (gói gốc, chủ `rca`).
  - `/opt/flash-ticket-obs/rca-ket-qua/` (dữ liệu dashboard).
  - Capture thô của Collector: `/opt/flash-ticket-obs/pinned/data/capture/`.
- exp-app:
  - `/opt/flash-ticket-app/{env-t062,compose-t062,rca-faults,rca-toxiproxy}`; bản cũ `env/`, `compose-exp/` giữ nguyên.
  - Hoàn tác về bản trước T-062: `bash ~/rollback-t062.sh`.

## 7. Chưa làm / chưa xác nhận

- **REDIS-BOOK:** không xác nhận được với hỗn hợp tải cố định (cần GET availability, phải đổi kịch bản tải chuẩn).
- **Tải chỉ đọc**, không đặt vé/thanh toán: R-04 (thông điệp) và R-09 chưa kiểm được. Chặng 2 §5 yêu cầu tải có đặt vé, chưa làm.
- **FLASH-HEALTHY** chưa có ngưỡng khỏe khóa (T-059 OPEN); chỉ là khám phá.
- **Lớp thao tác từ M1** (hướng 2), tô vùng nghi ngờ trên đồ thị, ô LLM: chưa làm (`giao-dien/XONG.md` §3).
- **Phản biện T-062:** chưa có người phản biện.
- **Lịch tự tiếp nhận `t062-tiep-nhan`:** không tồn tại trên tài khoản mới, không có gì để tắt.
- Laptop chưa kiểm test đầy đủ cần DB/MQ; CI trên PR đã chạy đầy đủ và xanh.

## 8. Việc chờ Minh duyệt

1. **Xem giao diện** và nói đạt hay không (G2 phương án A).
2. **PR #17:** giữ nhánh hay merge. Merge = triển khai production máy 84; trước đó phải dọn secret `ENV_*` (`deploy/app/README.md`). Claude không merge.
3. **Lỗi `tickets` 500:** sửa `@Order` cho `TicketApiExceptionHandler` hay giữ làm điều kiện nền (`ha-tang/A1-review.md` ghi chú 4).
4. **Collector exp-app:** đổi filelog sang cách không ghim ID container, để recreate không làm mất log (KP-19).
5. **REDIS-BOOK:** thêm GET availability vào hỗn hợp tải chuẩn, hay bỏ ô khỏi dev.
6. **Tải có đặt vé/thanh toán** (chặng 2), để kiểm R-04/R-09 và các ô Saga.
7. **Đề xuất SPEC chặng 4** (`spec-chang-4-de-xuat.md`): tiêu chí chọn, số lặp, cách tính báo động giả ở chế độ a.
8. **Ghi DECISIONS:** hướng tiêm lỗi đã bàn 11–12/11 (BOI-CANH), đính chính T-059 2i-B/2i-D theo cách tiêm mới, đổi cường độ EVENT-DB-LAT.
9. **Chỉ định người phản biện T-062.**
10. **Commit repo RCA.** Đề xuất: commit mã, báo cáo, sổ, `ket-qua/`, `tasks/T-062-*` và dòng STATE. Để ngoài git, chỉ giữ hash trong `manifest.json`: gói ca `ca/` (9 tgz 114 MB, giải nén 1,6 GB) và `tai/out/` (347 MB). Minh quyết.
11. **Tắt hay giữ máy:** iptables 8081 trên exp-app (không bền, mất khi khởi động lại); Toxiproxy và quota CPU Booking vẫn đang bật trên exp-app.

## 9. Xem mọi thay đổi

```bash
git -C D:/RCA-flashticket status --short
```

```bash
git -C D:/RCA-flashticket diff -- docs/STATE.md tasks/T-062-dem-chang-1-4
```

```bash
git -C D:/Project/flash-ticket-platform log --oneline main..rca/quan-sat-log
```

Thay đổi trên máy: `ha-tang/thay-doi.md` (exp-app), `tai/thay-doi-may-tai.md` (máy tải), `giao-dien/thay-doi.md` (exp-obs Grafana).
