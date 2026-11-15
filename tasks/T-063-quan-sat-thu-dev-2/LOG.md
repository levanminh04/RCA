# Nhật ký T-063

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 0 — 13/11/2026 — Claude — laptop Minh — vai trò: người soạn SPEC (phiên điều phối T-062)

- Minh duyệt SPEC ngày 13/11/2026 (chat: "tổng thể đề xuất đã ổn … tạo ghi đầy đủ tài liệu …"; nguyên lời ở `docs/DECISIONS.md` mục chiến dịch M1-FlashTicket). SPEC ghi 12/11 ~19:20Z.
- Chưa làm bước nào của task. Bối cảnh và quyền: `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`. Trạng thái sống: `tasks/T-062-dem-chang-1-4/CHECKPOINT-CHIEN-DICH.md`.
- Bước tiếp theo chính xác: theo mục "Các bước" của SPEC và danh sách việc trong checkpoint.

---

## Phiên 1 — 13/11/2026 (bắt đầu 12/11 21:16Z) — Claude (Opus 5.5, desktop) — laptop Minh — vai trò: người làm; đồng thời điều phối chiến dịch

- Mở phiên theo `tasks/T-062-dem-chang-1-4/PROMPT-PHIEN-MOI.md`. Tiếp quản sau khi kiểm phiên cũ đã dừng; bằng chứng ở `CHECKPOINT-CHIEN-DICH.md`, mục "Tiếp quản 21:16Z".
- Kiểm `results/T-062/ca/_metric-bo-sung/`: đủ (213 + 4 metric, 0 lỗi, phủ trọn cửa sổ), không xuất bù.
- **CPU-BOOK (21:48Z).** `results/T-063/cpu-book/PHAN-TICH.md`: CPU từng container (9 ca) + phép thử phân xử trên `exp-app` 21:42–21:47Z (nền / 2 luồng / 1 luồng). Cùng ~0,95 lõi Booking, 2 luồng: throttle 84% chu kỳ, PSI máy ×6, p99 đường không qua Booking 22→69 ms; 1 luồng: throttle 3%, p99 26 ms. Kết luận mức đã kiểm: nhiễu hàng xóm qua CPU máy (CFS theo cụm), không lan qua lời gọi; chưa đo trực tiếp lịch CPU theo ms. Đề xuất hai ô dev CPU-BOOK-1/CPU-BOOK-2.
- **Ca nền (21:50Z).** `results/T-063/ca-nen/PHAN-TICH.md`: thời gian độc quyền E1 theo 10 s bằng code M1 — vượt ngưỡng không dồn quanh t+63 (H1 không được ủng hộ); thay đổi có cấu trúc (đợt Keycloak DELETE Outbox 99→204 µs trong [t+60, t+240); xu hướng tăng ở job/outbox), < 0,2 ms; cơ chế từng đợt chưa phân xử (thiếu metric theo bảng — có từ TD-02 — và log hạ tầng). Phát hiện: metric PostgreSQL mức bảng trước TD-02 cho tốc độ âm (gộp chuỗi). Lịch đầu dò mới: đối xứng N/A.
- **Span gốc (21:53Z).** `results/T-063/span-goc/PHAN-TICH.md` (+ `phan_loai.py`, `phan-loai.json`): 9 ca; gốc không phải điểm vào/job Spring đều là tác vụ nền xác định theo `thread.name` (Keycloak job nội bộ không có span bọc 30.946; Hikari/Eureka/JGroups/health indicator — nguồn của span `*_db` gốc ở Spring); mồ côi Booking ~10/ca do `filter/health` bỏ span cha `/actuator/health` (đầu dò bộ chạy). CONSUMER gốc 0 (tải đọc). Đề xuất: bọc tác vụ Keycloak bằng `OTEL_INSTRUMENTATION_METHODS_INCLUDE` (chưa kiểm tên lớp), đầu dò không gọi health app trong cửa sổ.
- **H5 (22:04Z).** `results/T-063/h5/PHAN-TICH.md`: `docker pause` user-service 60 s → mọi metric của nó (docker_stats khe 70 s, JVM khe 63 s) mất cùng lúc; chưa có nguồn sống/chết độc lập. Đề xuất receiver `httpcheck` liveness (cùng lượt đổi Collector cách A).
- Ghi chú 22:16Z: các mốc giờ ở tiêu đề tài liệu phiên này đã chỉnh theo thời điểm ghi file thực tế (trước đó ghi theo ước lượng, lệch tới ~20 phút).
- **B16 bản 2 (phiên phụ L4, xong 22:46Z).** `results/T-063/b16-ban-2.md` (257 dòng): 11 điểm thiếu đặc tả, 9 điểm triển khai chưa đạt, 6 điểm chưa rõ cơ chế, bảng 17 đề xuất, 53 dẫn nguồn. Phiên phụ chỉ ghi file này, không SSH, repo FlashTicket sạch. Là tài liệu đề xuất cho Minh; khuyến nghị chưa kiểm trên máy. Chưa qua phản biện Codex.
- **Bảo trì exp-app lượt 1 xong (23:41Z).** TD-04..TD-08 ở `results/T-063/quan-sat/thay-doi-may.md`: Collector cách A (log 12 dịch vụ, gồm hạ tầng), httpcheck 8 đích, lọc health theo url.path, proxy AMQP Booking, Postgres log autovacuum/checkpoint/lock, span bọc job Keycloak (đạt ở lần thử 3). Chuẩn tải L1 (hai lượt v2: gateway 3.097/3.092, chênh 0,161%, chỉ ở poll) được Claude chấp nhận làm chuẩn cho đợt thu; phản biện chính thức L1 sẽ ghi riêng. L1b đã phát (đổi bậc tải, độ bền tunnel/mock, kiểm lại sau bảo trì).
- **Kiểm R trên tải mua vé (02:20Z).** `results/T-063/kiem-r/BAO-CAO.md`: gói `krb4a3d5` (cửa sổ v2a, trước bảo trì): R-04 ĐẠT lần đầu (1.561/1.561), R-09 0 mồ côi, R-02/03/06/08 đạt, R-01 thiếu (chỉ thao tác điều khiển AMQP), R-05 một phần (instance id log ≠ trace). Còn kiểm lại sau bảo trì.
- **D2 bản 2 (03:03Z).** `results/T-063/chay/D2B-KET-QUA.md`: đạt 7 ô (EVENT-DB-LAT, REDIS-BOOK, NET-GW-BOOK, HTTP5-EVENT, CPU-BOOK-1, CPU-BOOK-2, PAUSE-PAYMENT); CONSUMER-BOOK-SLOW chưa đạt (latency không tạo tồn queue) → đổi toxic bandwidth 2 KB/s trong `inj2.py` (sha256 `5cb5824d…`, đã tải lên), chờ xác nhận lại; POOL-EVENT không thử được (hook pool.hold khóa cứng cho Booking trong `RcaFaults.java` của Event). Sửa kênh `live-down` sang `httpcheck_error` (gói bổ sung bản 3). Tunnel L1 chết sau phiên Codex, Claude dựng lại 02:20Z.
- **Khóa đợt thu (03:41Z).** CONSUMER-BOOK-SLOW lần 3 (bandwidth 1 KB/s) không đạt → loại (§5a); danh mục ô chốt trong `results/T-063/chay/D2B-KET-QUA.md`. `lich-2.json` 13 chu kỳ sha256 `9bc6a3298cffdaf25bee41ebb5c53067e86b436a2d0c43f68b5094b57b606dbb`; hồ sơ đóng băng `results/T-063/dong-bang.md` + `dong-bang/dong-bang.json` (sha256 `993dc85b…`); `HO-SO-LUOT.md` chốt. Theo luật 21, giao Codex (người phản biện) soát trước khi phát (`results/T-063/codex/R1-brief.md`, ghi `REVIEW.md`).
- **Kiểm tích hợp R2 (04:13Z).** Lần 1 (gói `kte4878e`, cửa sổ pilot L1 03:09Z): P7 lỗi adapter `Log service outside the fixed source inventory` → TD-09. Lần 2 (tải `kt2-9e85b4` 03:57–04:08Z, t 04:03:28Z, gói `kteb5f6d`): vẫn lỗi vì stage-m1 đóng gói ±600 s (`stage-m1.py:61`) nên còn log tên cũ trước TD-09, adapter kiểm tên trên mọi log của gói. Lần 3 đặt t = 04:07:30Z (gói sau TD-09) đang chạy. Đợt thu chính không bị ảnh hưởng (mọi chu kỳ sau 04:07Z). SSH tới máy tải chập chờn 04:09Z (Minh mất mạng) → thêm `ps_thu_lai` cho Get/Receive-Tai; tunnel laptop cũ chết (không còn dùng — L1 đã chuyển tunnel lên exp-app).
- **R2 đóng (05:07Z).** `results/T-063/kiem-tich-hop/BAO-CAO.md`: gói `kt57fcd7` trên cấu hình cuối chạy trọn (P7 OK, trùng SHA, 39 pin, chốt thư mục trùng, đóng gói + bổ sung bản 3 khớp hash); R-04 đạt, R-09 0; R-08 thiếu 120 = đầu dò liveness Gateway (routeId unmatched, span lọc đúng thiết kế). Mạng laptop mất ~04:19–05:00Z: máy chủ không ảnh hưởng.
- **Tự gỡ lỗi trên máy (05:08Z).** `inj2.py` (sha256 `d76a0186…`, đã tải lên): toxic/pause có tiến trình hẹn giờ tách phiên trên exp-app tự `stop` ở hạn + 5 s (độc lập laptop); dừng sớm hủy hẹn giờ. Kiểm thật `results/T-063/tiem-loi/kiem-het-han/ket-qua.txt` (toxic EVENT-DB-LAT 20 s tự gỡ; dừng sớm hủy hẹn giờ; verify sạch). Hai toxic thử 05:07:31–05:07:56Z và 05:08:06–05:08:07Z trên event-jdbc, không có lượt thu.
- **Phản hồi REVIEW T-063 (05:20Z).** Bảng "Phản hồi của người làm" trong `REVIEW.md` đã điền: R1 và R2 đúng, đã sửa hoặc bổ sung; R3 đúng, chọn hậu kiểm; R4 đúng, ghi giới hạn và thêm PSI máy.
- **Chuyển bộ chạy lên `exp-obs` (05:10–06:15Z, Minh quyết, DECISIONS 13/11).**
  - `results/T-063/chay/runner3.py` sinh từ runner2 bằng `tao_runner3.py`, chỉ đổi vận chuyển. Có `RCA_DP_OUT` cho lượt thử; `tai()` dùng stdin DEVNULL.
  - Tải qua `results/T-062/tai-2/tai_linux.py` (Codex L1d, phản biện `tasks/T-062-dem-chang-1-4/REVIEW-PL2-2.md`).
  - Lượt thử một chu kỳ HTTP5-EVENT-FLASH, mã `865c8e93`, không phải ca RCA, 05:43–06:15Z: sổ 12 sự kiện, chuỗi hash đúng; M1 OK tất định; gói + bổ sung; k6 ExitCode 0. Hành trình lỗi 2.159 = số lần hook chạy. Bộ chạy sống khi ngắt SSH laptop. Đầu ra ở `results/T-063/chay/thu-ngan/obs/`.
  - Phát hiện: đầu dò audit đếm 2000 dòng đuôi, đã bão hòa → hậu kiểm ô hook bằng file audit đầy đủ theo `timestamp` (`HO-SO-LUOT.md`, phụ lục).
- **Hết hạn mức Claude ~06:20–07:10Z.** Không phiên nào tiếp quản (lượt lịch 06:21Z lỗi hạn mức). Máy chủ không ảnh hưởng.
- **Đóng băng bản 2 (07:13Z).** `results/T-063/dong-bang/dong-bang-2.json`, mục bản 2 trong `results/T-063/dong-bang.md`. Bản 1 giữ nguyên.
- **ĐỢT THU CHÍNH PHÁT 07:13:46Z** trên `exp-obs`: `setsid -f nohup python3 -B runner3.py thu --lich lich-2.json`. Sổ `~/rca-dieu-phoi/tiem-loi/so-thu2.jsonl`, nhật ký `~/rca-dieu-phoi/chay/nhat-ky-2.jsonl`, trạng thái `chay/trang-thai-2.json`, gói ca `~/rca-dieu-phoi/ca/`. 13 chu kỳ, dự kiến xong ~13:50Z, M1 ca cuối ~14:00Z. Dừng khẩn: `touch ~/rca-dieu-phoi/STOP` trên `exp-obs`.
- **Bước tiếp theo chính xác:**
  1. Theo dõi sổ, nhịp tim ≤30 phút trong `CHECKPOINT-CHIEN-DICH.md`.
  2. Sau `thu2-end`, chép về `results/T-063/thu2/`: `tiem-loi/so-thu2.jsonl`, `chay/`, `ca/`, `tai-out/t2-*`, và `executions.jsonl` (Event/Booking) từ `exp-app`. Kiểm hash.
  3. Hậu kiểm từng mã mờ → `results/T-063/chay/xac-nhan-ca.json`.
  4. T-064 khai tập chọn rồi chấm.
- Lệnh cuối: phát `runner3.py thu` (ở trên).

---

## Phiên 2 — 14/11/2026 giờ VN (bắt đầu 13/11 19:24Z) — Claude (Fable 5.2, desktop, lịch `m1ft-tiep-nhan`) — laptop Minh — vai trò: người làm; đồng thời điều phối chiến dịch

- Tiếp nhận từ phiên 1 (Claude, cùng vai trò). Bằng chứng tiếp quản: `CHECKPOINT-CHIEN-DICH.md`, mục "Tiếp quản 19:24Z". Không có người thật theo dõi.
- **Dựng lại phần phiên 1 chưa ghi vào LOG này** (phiên 1 ghi ở checkpoint và STATE; LOG dừng ở lúc phát đợt thu). Kiểm trên file 19:37Z:
  - `results/T-063/thu2/`: `sha256sum -c SHA256SUMS` 214/214 khớp; 13 gói `ca/<mã>.tgz`, 13 `prometheus-bo-sung.json`; sổ `tiem-loi/so-thu2.jsonl` 127 dòng; nhật ký `chay/nhat-ky-2.jsonl` 40 dòng, dòng cuối "Lượt thu xong" 14:01:17Z.
  - Hậu kiểm: `chay/xac-nhan-ca.json` 12/13 `xac_nhan` (PAUSE-PAYMENT không đạt điều kiện khai trước); `chay/xac-nhan-ca-2.json` 13/13 ("Sửa sau 1").
  - Không chắc: phép kiểm chuỗi hash của sổ do phiên 1 báo đúng, phiên này chưa chạy lại.
- **Báo cáo:** `results/T-063/bao-cao.md` (mới). Đếm lại 24 kênh của gói bổ sung trên 13 ca. Truy vấn Prometheus `exp-obs` 19:38Z (chỉ đọc): `jvm_thread_count` không có trạng thái `blocked`, nên kênh `threads-blocked` rỗng ở 13/13 ca.
- **Báo cáo theo mục 7.**
  1. Đã làm: kiểm toàn vẹn đợt thu, viết báo cáo, soạn brief phản biện lượt 2.
  2. File đổi: `results/T-063/bao-cao.md`, `results/T-063/codex/R2-brief.md`, LOG này.
  3. Kiểm đã chạy: `sha256sum -c` (214/214); đếm kênh gói bổ sung; một truy vấn Prometheus.
  4. Chưa chắc / còn mở:
     - Task đạt: đợt thu 13 ca có băm và đầu ra P7; tín hiệu H1–H8 có trong gói.
     - Câu hỏi nguồn mới trả lời một phần: H3 và H4 không có ô lỗi (POOL-EVENT, CONSUMER-BOOK-SLOW không vào đợt thu); span gốc chưa phân loại lại trên tải mới; cơ chế cờ ở ca nền chưa phân xử.
     - Thiếu so với SPEC: `manifest.json`, `o-dev-bo-sung.json`.
     - Chờ Minh: "Sửa sau 1" (tập 12 hay 13 ca); FLASH-HEALTHY tính là ca không lỗi hay báo riêng; cách lưu 1,3 GB `thu2/` khi commit.
- **Bước tiếp theo chính xác:** (1) đọc `tasks/T-063-quan-sat-thu-dev-2/REVIEW-2.md` khi Codex xong, điền bảng phản hồi; (2) `span-goc/phan_loai.py` cần bản chạy trên `results/T-063/thu2/ca/` (script hiện ghim đường dẫn T-062 và ghi đè `phan-loai.json` — viết bản mới, không sửa bản cũ); (3) `manifest.json`; (4) ô H4 (tải message cao hơn) trong quyền; ô H3 cần Minh cho phép sửa hook thử — xem mục 6 của báo cáo.
- **Prompt phản biện (soát kết quả, lượt 2):** `results/T-063/codex/R2-brief.md` — chép nguyên văn Prompt chung và khối "Soát kết quả" của `docs/review-prompt.md`, chỉ điền thông tin trung tính. Theo quyền điều phối chiến dịch, Claude phát cho Codex bằng `results/T-063/dieu-phoi/goi_codex.py --che-do sandbox`.
- Lệnh cuối: phát Codex R2 (dưới).
- **Bổ sung 19:43Z (cùng phiên 2, sau khi đã phát Codex R2 lúc ~19:40Z).** Phân loại span gốc trên 13 ca mới: `results/T-063/span-goc/phan_loai_dev2.py` (chạy nguyên `phan_loai.py`, chỉ đổi nơi đọc và file ra) → `phan-loai-dev2.json`, `phan-loai-dev2.log`. Số trung bình mỗi ca đã đưa vào `bao-cao.md` mục 3. Lưu ý cho người phản biện: `bao-cao.md` được sửa ở mục 3, 5, 6 sau thời điểm phát R2; nội dung trước sửa ghi "chưa chạy lại trên 13 ca mới". Việc (2) ở "Bước tiếp theo" đã xong.
- **Tự soát trước khi mở `REVIEW-2.md` (19:57Z).** Điểm tự tìm được trong báo cáo và đầu ra:
  - N1 (KHÔNG CHẶN): chuỗi hash của sổ `thu2/tiem-loi/so-thu2.jsonl` chỉ dẫn lại lời phiên 1, phiên 2 chưa chạy lại.
  - N2 (KHÔNG CHẶN): đầu ra `dieu-phoi/` của SPEC bước 1 đòi "một lần thử gọi lại thành công"; mới có mô phỏng và `exec resume` thật, chưa có lần hết hạn → chờ → tự gọi lại chạy trọn trên Codex thật.
  - N3 (KHÔNG CHẶN): nhóm gốc CLIENT không phải DB tăng 360 → 634 mỗi ca trên tải mới, chưa lần.
  - N4 (KHÔNG CHẶN, ảnh hưởng T-064): cột "P7 OK 13/13, hai lần trùng" lấy từ nhật ký của bộ chạy, phiên 2 chưa đối chiếu lại `summary.json` trong từng gói.
  - N5: `bao-cao.md` bị sửa ba lần sau khi phát R2 (span gốc, `threads-blocked`, quyền sửa hook H3); người phản biện có thể đã đọc bản trước sửa.
- **Đáp phản biện lượt 2 (19:58Z).** Codex R2 xong 19:56Z (`REVIEW-2.md`): R5 (chặn nghiệm thu phần phân loại trace), R6 (không chặn). Kiểm từng điểm trên file: số của người phản biện khớp. Cả hai **đúng**. Đã sửa trong quyền: `results/T-063/bao-cao.md` (câu mục 3, thêm mục 7), đính chính Q4 ở `results/T-064/phan-tich/ghi-chu-co-che-dev2.md`; điền bảng phản hồi (R5, R6, N1, N2, N4).
  - Còn mở sau sửa: bước làm thiếu 11 span cha của Payment ở ca PAUSE-PAYMENT; đích của nhóm `PUT`/`GET`; cơ chế cờ ở ca nền.
  - Đề xuất của người phản biện về các việc chờ Minh (tập 13 ca, giữ nhãn FLASH-HEALTHY và báo tách, sửa hook H3, kho artifact cho `thu2/`): người làm đồng ý cả bốn; chưa phải Minh duyệt.
  - Prompt kiểm lại cho người phản biện: sẽ soạn `results/T-063/codex/R3-brief.md` (khối "Kiểm lại phản hồi và sửa") và phát cùng lượt phản biện T-064, để Codex không chạy hai lượt nặng chồng nhau.

---

## Phiên 3 — 14/11/2026 giờ VN (13/11 22:28Z) — Claude (Fable 5.2, desktop, lịch `m1ft-tiep-nhan`) — laptop Minh — vai trò: người làm; đồng thời điều phối chiến dịch

- Tiếp nhận từ phiên 2 (dừng 21:08Z vì hết hạn mức). Bằng chứng tiếp quản: `tasks/T-062-dem-chang-1-4/CHECKPOINT-CHIEN-DICH.md`, mục "Tiếp quản 22:24Z".
- Phát lượt kiểm lại cho người phản biện (22:28Z): `results/T-063/codex/R3-brief.md` (khối "Kiểm lại phản hồi và sửa" của `docs/review-prompt.md`, nguyên văn, thông tin trung tính; dựng bằng `results/T-064/kiem/dung_brief_phan_bien.py`). Codex ghi `tasks/T-063-quan-sat-thu-dev-2/REVIEW-3.md`. Lệnh nền `b7qdk2s8w`, trạng thái `results/T-063/codex/R3-trang-thai.json`.
- Phiên này chưa làm việc nào khác của T-063. Còn thiếu như mục cuối phiên 2: `manifest.json`, `o-dev-bo-sung.json`, ô H4.
- **Đáp phản biện lượt 3 (22:42Z).** Codex R3 xong 22:40Z: `tasks/T-063-quan-sat-thu-dev-2/REVIEW-3.md`. Không có finding mới; R5 và R6 được xác nhận đã xử lý; người phản biện đề xuất dừng phần này, chưa nghiệm thu task. Người làm đồng ý, đã điền bảng phản hồi. Sửa trong quyền: thêm một câu dẫn nguồn về đích Eureka của nhóm `PUT`/`GET` vào `results/T-063/bao-cao.md` (người làm chưa tự đếm lại).
- **Báo cáo theo mục 7.**
  1. Đã làm: phát lượt kiểm lại, đọc kết quả, đáp từng điểm.
  2. File đổi: `results/T-063/codex/R3-*`, `results/T-063/bao-cao.md` (một câu), bảng phản hồi cuối `REVIEW-3.md`, LOG này, dòng T-063 trong STATE.
  3. Kiểm đã chạy: không chạy phép kiểm mới; số trong bảng phản hồi lấy từ `REVIEW-3.md`.
  4. Còn mở:
     - Task đạt: đợt thu 13 ca đã kiểm toàn vẹn qua hai bên; phần phản hồi R1–R6 không còn bất đồng.
     - Chưa đạt SPEC: `manifest.json`, `o-dev-bo-sung.json`, phép thử "hết hạn → chờ → tự gọi lại" trên Codex thật.
     - Câu hỏi nguồn còn mở: bước làm thiếu 11 span cha của Payment; cơ chế cờ ở ca nền; H3, H4 chưa có ô lỗi.
     - Chờ Minh: tập 12 hay 13 ca; FLASH-HEALTHY; sửa hook thử H3; nơi lưu `thu2/`.
- **Bước tiếp theo chính xác:** (1) dựng `results/T-063/manifest.json` và `o-dev-bo-sung.json`; (2) rà ô H4 trong quyền (tải message cao hơn hoặc consumer chậm) và trình chi phí; (3) đọc bản sao snapshot/log exporter trên `exp-obs` để phân xử span Payment nếu còn.
- **Prompt cho người phản biện:** hai bên đều đề xuất dừng phần này; prompt bàn giao do người phản biện soạn nằm trong `REVIEW-3.md` mục "Prompt bàn giao cho người làm". Lượt kiểm tiếp chỉ cần khi có đầu ra mới (manifest, ô H4); khi đó dựng brief bằng `results/T-064/kiem/dung_brief_phan_bien.py` (khối "Soát kết quả").
- Lệnh cuối: sửa `bao-cao.md` và điền bảng phản hồi (script Python trong phiên).
- **Quyết định của Minh trong phiên (ghi 23:21Z).** Nguồn: `docs/DECISIONS.md`, mục "Tập chọn dev bản 2: nhận "Sửa sau 1", dùng 13 ca, 13/11/2026" (Minh trả lời ~23:19Z trong phiên `ed8b9c01…`: "Đồng ý, dùng 13 ca"; phiên đó ghi DECISIONS và báo sang phiên điều phối này). Phiên này không trực tiếp nhận lời Minh; căn cứ là dòng đã ghi trong DECISIONS.
  - Hệ quả cho T-063: hậu kiểm dùng `results/T-063/chay/xac-nhan-ca-2.json` (13/13); mục "chờ Minh: tập 12 hay 13 ca" đã có lời đáp. Còn chờ Minh: FLASH-HEALTHY, sửa hook thử H3, nơi lưu `thu2/`.

---

## Phiên B — 14/11/2026 (05:05Z) — Claude (Opus 5.5, desktop, phiên phụ) — laptop Minh — vai trò: người làm (thu bù H3/H4)

- Phiên B (Claude, `local_33bac1e1-ae7b-4f28-8e8d-90e7b195a1de`) mở ngày 14/11/2026 05:05Z, do phiên điều phối `local_370653c4…` mở theo duyệt của Minh. Việc: thu bù ô lỗi H3 (POOL-EVENT, hook thử đã duyệt ở DECISIONS 14/11 "Hook thử H3…") và H4 (consumer chậm), kèm ô đối chứng trên bản build mới. Brief: `tasks/T-062-dem-chang-1-4/PHIEN-B-BRIEF.md`. Đầu ra ở `results/T-063/thu3/`; checkpoint `thu3/CHECKPOINT.md`, trạng thái `thu3/TRANG-THAI.json`.
- 05:08–06:20Z: rà, kế hoạch `results/T-063/thu3/KE-HOACH.md` (bản 1 ghi trước khi chạm máy, bổ sung 1–5 ghi theo từng số đo). Sửa hook H3: commit `e557307` trên `rca/quan-sat-log` (`RcaFaults.java` Event dòng 69, 163; thêm phép thử pool), đã push nhánh. Build riêng Event trên `exp-app` từ `6b21ed55` + bản vá (test `RcaFaults*` 8/8), triển khai 05:21–05:22Z. Đo H4 (×1 469 B/s, ×3 1.393 B/s); thử pool (chọn 5); thử toxic H4 dưới ×3 (đạt); thêm RECREATE-PAY theo `results/T-064/phien-c/YEU-CAU-O.md`; chạy thử `runner4` một chu kỳ rút ngắn (đạt); chốt `dieu-kien-xac-nhan-3.md` 06:14Z; đóng băng bản 3.
- 07:24–10:33Z: lượt chính `runner4.py thu --lich lich-3.json` trên `exp-obs`, 6/6 chu kỳ. Nhận, hậu kiểm, đặt gói cho T-064, so ô cũ, báo cáo.

### Kết thúc phiên B — 14/11/2026 ~11:05Z

1. **Đã làm:** thu bù 3 trên bản 3 (Event có hook H3): POOL-EVENT (H3), CONSUMER-BOOK-SLOW-X3 (H4, tải ×3), đối chứng BINH-THUONG, EVENT-DB-LAT, BINH-THUONG-X3, và RECREATE-PAY (H8-adapter, yêu cầu phiên C). Nhận về `results/T-063/thu3/thu/`, hậu kiểm, gói bổ sung cho T-064 ở `exp-obs:/opt/rca-m1ft/bo-sung-dev3/`.
2. **File đã đổi (repo RCA):** mới `results/T-063/thu3/**` (KE-HOACH, CHECKPOINT, TRANG-THAI, thay-doi-may, dieu-kien-xac-nhan-3, lich-3, lich-thu3-ngan, xac-nhan-ca-3*.json, so-sanh-o-cu.json, de-xuat-WHY, BAN-GIAO-B, PROMPT-PHAN-BIEN, manifest.json, do/, thu/, thu-ngan/, scripts/); `results/T-063/dong-bang/dong-bang-3.json`, `dong-bang-3-truoc-chot.json`; thêm mục cuối ở `results/T-063/o-dev-bo-sung.md`, `bao-cao.md`, `dong-bang.md`; LOG này. **Repo FlashTicket:** commit `e557307` nhánh `rca/quan-sat-log`, đã push. **Máy:** `results/T-063/thu3/thay-doi-may.md` T3-01…T3-15 (Event trên `exp-app` vẫn chạy bản 3).
3. **Kiểm đã chạy:** `nhan_thu3.sh` (5/5 gói khớp hash, sổ 60 dòng, chuỗi hash đúng); P7 5/5 OK hai lần trùng SHA; hậu kiểm khai trước 4/6, sau hai "Sửa sau" 6/6 (chạy không cờ trùng bản chốt ở mọi ca, mọi điều kiện); so ô cũ bản 2 ↔ bản 3 (`thu3/so-sanh-o-cu.json`); lần ra lỗi bộ chặn rò mã ở ca H4 (trùng ngẫu nhiên với spanId, không phải nhãn lọt).
4. **Chưa chắc / cần quyết:**
   - Task (phần thu bù) đạt: H3 và H4 mỗi hướng có một ô lỗi được đầu dò độc lập xác nhận; có đối chứng bản 3 và đối chứng cùng bậc tải cho H4. Câu hỏi nguồn: mới có dữ liệu để T-064 phân xử H3/H4; chưa trả lời H3/H4 có ích hay không (việc của T-064).
   - **Chờ Minh:** nhận "Sửa sau 1" (sửa script, không đổi điều kiện) và "Sửa sau 2" (sửa điều kiện httpcheck sau khi xem) — `thu3/dieu-kien-xac-nhan-3.md`; đề xuất nhận cả hai, phương án khác thu lại hai ô (~1 giờ máy). Chưa nhận thì T-064 chỉ dùng 4 ca.
   - Chờ điều phối: chép `thu3/de-xuat-WHY.md` vào `docs/WHY.md` trước khi T-064 dùng; quyết tập nút chấp nhận ô H4 có thêm `broker` (BAN-GIAO-B mục 5); giữ hay hoàn tác bản 3 trên `exp-app`; gỡ khóa SSH trên `exp-obs` khi hết thu bù.
   - Còn mở: ca RECREATE-PAY không có `.tgz` (dữ liệu thô giữ trên `exp-obs`, có hash); PSI CPU máy ở bản 3 cao hơn chút (15,3–16,5% so với 11,8–15,6%), chưa phân xử nguyên nhân; mỗi ô một lần thu; `manifest.json` gốc của T-063 vẫn thiếu (đã có `thu3/manifest.json`).
- **Bước tiếp theo chính xác:** (1) điều phối đọc `results/T-063/thu3/BAN-GIAO-B.md`; (2) phát lượt phản biện Codex bằng `results/T-063/thu3/PROMPT-PHAN-BIEN.md` (Prompt chung + khối "Soát kết quả" nguyên văn, chỉ điền thông tin trung tính; ghi `REVIEW-4.md`) qua `results/T-063/dieu-phoi/goi_codex.py --che-do sandbox`; (3) T-064 chạy M1-FT trên các mã gói ở BAN-GIAO-B mục 4, dùng `bo-sung-dev3`.
- **Prompt cho người phản biện:** `results/T-063/thu3/PROMPT-PHAN-BIEN.md` (bản đầy đủ để dán; dựng bằng `results/T-063/thu3/scripts/dung_prompt_phan_bien.py`, kiểm ba khối chép nguyên văn khớp `docs/review-prompt.md`).
- **Lệnh cuối:** `py -3 -B results/T-063/thu3/scripts/tao_manifest_thu3.py` (→ `results/T-063/thu3/manifest.json`).

### Điều phối 16:00Z — Codex R4 phản biện thu bù 3 xong
- R4 (`results/T-063/codex/R4-*`, 15:33:36–15:55:55Z, rc 0) ghi `REVIEW-4.md`: không có điểm CHẶN; R7 KHÔNG CHẶN (manifest thu3 chưa bao phủ dòng duyệt nối thêm). Điều phối tự kiểm hash: đúng. Điền bảng phản hồi, để trống "Minh quyết". Chưa tạo manifest-2.
- 16:05Z Minh duyệt sửa R7 ("duyệt, sau đó chạy phiên codex phản biện tiếp theo"). Tạo `results/T-063/thu3/manifest-2.json` (87 file) và `results/T-063/manifest-2.json` (195 file) bằng `thu3/scripts/tao_manifest_thu3_2.py`, `dong-goi/tao_manifest_t063_2.py`; manifest cũ giữ nguyên byte (a0cad230…, e410fd6a…). Kiểm 0 lệch. Dựng `results/T-063/codex/R5-brief.md` (Prompt chung + "Kiểm lại phản hồi và sửa", script `thu3/scripts/dung_prompt_kiem_lai_r7.py`); phát Codex R5 (gpt-6.1-sol, max), ghi REVIEW-5.md.
- 16:18Z Codex R5 xong (16:00:18–16:17:52Z, rc 0; `results/T-063/codex/R5-*`), ghi `REVIEW-5.md`: R7 đã sửa đúng (87/87, 195/195, 337/337 mục khớp); không finding mới đáng kể; đề xuất dừng phản biện phần thu3/sửa R7, chưa nghiệm thu toàn T-063. Chờ Minh quyết dừng.
- 16:19Z Đính chính mốc giờ (REVIEW-5, giới hạn đối chiếu giờ duyệt): dòng LOG trên và dòng "R7 (sửa)" trong bảng REVIEW-4 ghi Minh duyệt "~16:05Z" là ước lượng sai. Lời duyệt "duyệt, sau đó chạy phiên codex phản biện tiếp theo" đến sau báo cáo R4 (R4 xong 15:55:55Z) và trước file đầu tiên của việc sửa (`thu3/scripts/tao_manifest_thu3_2.py`, ghi 15:58:34Z); manifest-2 lập 15:59:52–54Z; R5 phát 16:00:18Z. Thứ tự: duyệt → sửa → phát R5. Không đổi utc manifest.
