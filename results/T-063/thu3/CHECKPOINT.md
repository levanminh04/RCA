# T-063 thu3 — Checkpoint (phiên B, `local_33bac1e1-ae7b-4f28-8e8d-90e7b195a1de`)

Mỗi mục ghi giờ UTC, bước, đầu ra, tiến trình đang chạy, bước tiếp. Mục mới nhất ở cuối. Đủ để agent khác làm tiếp không cần lịch sử chat: đọc brief `tasks/T-062-dem-chang-1-4/PHIEN-B-BRIEF.md`, `thu3/KE-HOACH.md`, rồi mục cuối file này.

Cách gọi máy (không in khóa): khóa ở `D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key`, `D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key`; `-o BatchMode=yes -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts`; `ubuntu@213.35.116.128` (exp-obs), `ubuntu@129.221.208.47` (exp-app). Tải: trên exp-obs `cd ~/rca-dieu-phoi && python3 -B tai_linux.py start|get|stop|receive --tag …`.

## 05:16Z — rà xong, kế hoạch bản 1, đo H4 đang chạy

- Đầu ra: `thu3/KE-HOACH.md` (bản 1), `thu3/TRANG-THAI.json`; dòng mở phiên trong `tasks/T-063-quan-sat-thu-dev-2/LOG.md`.
- Repo FlashTicket: commit `e557307` trên `rca/quan-sat-log` (sửa `RcaFaults.java` Event dòng 69, 163; thêm phép thử pool vào `RcaFaultsTests.java` Event). **Chưa push.** Bản vá dạng diff: `thu3/scripts/h3-pool-event.patch`.
- Script đã viết (chưa chạy trên máy): `thu3/scripts/build-t063-event.sh`, `deploy-t063-event.sh`, `inj3.py`, `tao_runner4.py` → `runner4.py` (+ `runner4.diff`).
- Đang chạy: tải thử `t3do-h4a` (máy tải, 420 s, ×1 rồi ×3 từ giây 180; bắt đầu 05:10:56Z); đầu dò `exp-app:~/t063/thu3/do_h4.py` → `~/t063/thu3/do-h4a.jsonl` (540 s). Không đổi cấu hình máy nào.
- Bước tiếp: nhận `t3do-h4a` (`tai_linux.py receive`), chép `do-h4a.jsonl` về `thu3/do/`, tính byte/s broker→Booking theo bậc; rồi build Event (`build-t063-event.sh`).

## 05:24Z — Event bản mới đã triển khai; chạy thử cường độ pool

- Đo H4 xong: `do/do-h4a.jsonl`, tóm tắt `do/do-h4a-tom-tat.json` (byte broker→Booking: ×1 tb 469 B/s, ×3 tb 1.393 B/s; tồn queue max 2). Theo quy tắc khai trước (KE-HOACH §5: ≥ 1,5 KB/s) → **chưa đạt ngưỡng khả thi**. Bước tiếp cho H4: thử trực tiếp toxic 1 KB/s dưới ×3 trên bản mới (ghi là lệch quy tắc khai trước, lý do ở KE-HOACH mục Bổ sung).
- Build và triển khai Event: `thay-doi-may.md` T3-04, T3-05. Image `ft-local/event-service:arm64-t063h3-76b34d5e`. Hoàn tác: `bash ~/t063/thu3/deploy-t063-event.sh ft-local/event-service:arm64-t062-6b21ed55` trên exp-app.
- Đang chạy: tải `t3do-pool` (05:23:28Z, 600 s) + `exp-app:~/t063/thu3/thu_pool.sh` → `~/t063/thu3/thu-pool.jsonl` (POOL-EVENT-4 từ ~05:25:28Z, POOL-EVENT-5 từ ~05:30:30Z). Nếu phiên dừng: chờ hết, `python3 ~/inj3.py verify` trên exp-app phải `sach: true`; nhận tải `t3do-pool`; đọc Prometheus pool Event trong hai pha.
- Bước tiếp: chọn cường độ theo KE-HOACH §4; thử toxic H4 dưới ×3; push nhánh FlashTicket; lịch `lich-3.json`, `dieu-kien-xac-nhan-3.md`, đóng băng 3, chạy thử runner4.

## 05:53Z — hai ô đã chốt; chạy thử runner4 đang chạy

- Chốt: POOL-EVENT = `pool.hold` 5 (KE-HOACH bổ sung 2); CONSUMER-BOOK-SLOW-X3 = bandwidth 1 KB/s trên `booking-amqp` dưới ×3 (bổ sung 3, thử đạt: tồn 0 → 109, về 0). Lịch `lich-3.json` (5 chu kỳ, sha256 `e9a28c53…`, chưa chép lên exp-obs).
- Đã viết: `dieu-kien-xac-nhan-3.md` (bản nháp, chưa có dòng "Chốt"), `scripts/xac_nhan_ca_3.py` (+ `tao_xac_nhan_ca_3.py`), `scripts/nhan_thu3.sh`, `scripts/dong_bang_3.py`, `de-xuat-WHY.md`. Nhánh FlashTicket đã push (`e557307`).
- Đang chạy trên exp-obs: chạy thử `runner4.py` (`RCA_DP_OUT=~/rca-dieu-phoi/thu3-thu-ngan RCA_PHASE=360`, lịch `lich-thu3-ngan.json`, mã thử `69845d29`, tải `t3-69845d29` ×3), bắt đầu 05:47:51Z, chu kỳ xong ~06:07Z, M1 ca thử sau đó. Không phải ca RCA.
- Bước tiếp: kiểm sổ/nhật ký/gói của chạy thử; chạy `xac_nhan_ca_3.py` trên chạy thử (đối chiếu điều kiện với đầu ra thật); chốt `dieu-kien-xac-nhan-3.md`; chép `lich-3.json` lên exp-obs; đóng băng 3 (`py -3 -B results/T-063/thu3/scripts/dong_bang_3.py dong-bang-3.json`); chờ exp-obs yên (lô phiên C ngừng phát 07:25Z) rồi phát lượt chính ~07:35Z: `cd ~/rca-dieu-phoi && RCA_DP_OUT=/home/ubuntu/rca-dieu-phoi/thu3 setsid -f nohup python3 -B runner4.py thu --lich lich-3.json > thu3-runner4.out 2>&1 < /dev/null`.

## 06:20Z — sẵn sàng phát lượt chính; chờ exp-obs yên

- Xong: chạy thử runner4 (đạt; nhận về `thu3/thu-ngan/`, hậu kiểm `thu-ngan/xac-nhan-thu.json`); thêm RECREATE-PAY (KE-HOACH bổ sung 4) và chạy thử riêng (T3-13); điều kiện xác nhận chốt (`dieu-kien-xac-nhan-3.md`, sha256 `9dbdca16…`); đóng băng bản 3 (`results/T-063/dong-bang/dong-bang-3.json` `1200ffe0…`, mục Bản 3 ở `dong-bang.md`); `o-dev-bo-sung.md` thêm mục thu bù 3.
- Máy: exp-app chạy Event `arm64-t063h3-76b34d5e`, `~/inj3.py` `ba8f1341…`; exp-obs có `runner4.py` `088cdf6c…`, `lich-3.json` `c0d4581b…`. Không còn can thiệp (`verify` sạch 06:12Z).
- Bước tiếp: khi `py -3 -B results/T-063/thu3/scripts/kiem_truoc_phat.py` trả `duoc_phat: true` (dự kiến sau 07:28Z), phát trên exp-obs: `cd ~/rca-dieu-phoi && RCA_DP_OUT=/home/ubuntu/rca-dieu-phoi/thu3 setsid -f nohup python3 -B runner4.py thu --lich lich-3.json > thu3-runner4.out 2>&1 < /dev/null`; đặt `TRANG-THAI.json` `dang_thu: true`. Theo dõi nhẹ: `tail -1 ~/rca-dieu-phoi/thu3/tiem-loi/so-thu3.jsonl`, `cat ~/rca-dieu-phoi/thu3/chay/trang-thai-3.json`.

## 07:25Z — LƯỢT CHÍNH ĐANG CHẠY trên exp-obs (không phụ thuộc phiên này)

- Phát 07:24:01Z: `runner4.py thu --lich lich-3.json`, `RCA_DP_OUT=~/rca-dieu-phoi/thu3` (PID 634924). 6 chu kỳ × ~30 phút → xong chu kỳ ~10:25Z, M1 ca cuối ~10:30Z. `TRANG-THAI.json` `dang_thu: true`.
- Theo dõi nhẹ (exp-obs): `tail -1 ~/rca-dieu-phoi/thu3/tiem-loi/so-thu3.jsonl | cut -c1-200`; `cat ~/rca-dieu-phoi/thu3/chay/trang-thai-3.json`; `grep -c "M1 xong" ~/rca-dieu-phoi/thu3/chay/nhat-ky-3.jsonl`. Không truy vấn Prometheus nặng.
- Khi sổ có `thu3-end` và không còn `runner4.py thu`: (1) `bash results/T-063/thu3/scripts/nhan_thu3.sh` (→ `thu3/thu/`, kiểm hash gói và chuỗi sổ); (2) `PYTHONIOENCODING=utf-8 py -3 -B results/T-063/thu3/scripts/xac_nhan_ca_3.py results/T-063/thu3/thu results/T-063/thu3/xac-nhan-ca-3.json`; (3) ca RECREATE-PAY: nếu `M1 LỖI` thì đóng gói tay (KE-HOACH bổ sung 5); (4) đặt `prometheus-bo-sung.json` từng ca vào `/opt/rca-m1ft/bo-sung-dev3/<mã>/` (như `bo-sung-dev2`); (5) `py -3 -B results/T-063/thu3/scripts/so_sanh_o_cu.py`; (6) viết `BAN-GIAO-B.md`, mục "Thu bù 3" trong `bao-cao.md`, LOG kết phiên; `TRANG-THAI.json` `dang_thu: false`.
- Nếu lượt chết giữa chừng: theo KE-HOACH §8 và bổ sung 5 (lỗi tự hết; phát lại lịch các chu kỳ còn lại với `RCA_DP_OUT` mới, giữ thư mục cũ).

## 11:05Z — XONG phần phiên B; còn lại chờ Minh/điều phối

- Lượt chính xong 10:32:34Z (6/6). Nhận `thu/` (hash khớp). Hậu kiểm: bản chốt 4/6 (`xac-nhan-ca-3.json`), sau hai "Sửa sau" 6/6 (`xac-nhan-ca-3-sua-sau.json`) — chờ Minh. P7 5/5 OK hai lần trùng; RECREATE-PAY P7 lỗi adapter (dự kiến).
- Gói cho T-064: `/opt/flash-ticket-rca/cases|outputs/<mã gói>`, `/opt/rca-m1ft/bo-sung-dev3/<mã gói>/`; mã gói ô H4 là `659a9dfb1ab0`. Chi tiết, đáp án, hash: `BAN-GIAO-B.md`.
- Bàn giao: `BAN-GIAO-B.md`; mục kết thúc phiên B trong `tasks/T-063-quan-sat-thu-dev-2/LOG.md`; prompt phản biện `PROMPT-PHAN-BIEN.md`; manifest `manifest.json`.
- Không còn tiến trình nào của phiên B trên máy. `exp-app` vẫn chạy Event bản 3; `~/inj3.py` còn; khóa SSH trên `exp-obs` chưa gỡ (chờ điều phối).
