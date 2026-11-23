# T-073 — Kết quả E5 (S4): lượt nghiệm thu `PAUSE-PAYMENT`, chế độ (b)

Ngày 23/11/2026. Phiên `rca-w5`, Claude, người làm. Chạy theo `results/T-073/trien-khai-e5.md`, sha256 `0befa4d0…`, các bước S4-1 đến S4-9. Ô `PAUSE-PAYMENT` có hạt `32323232` theo `khoa-boc-e5.json`. Tiêu chí lấy từ `khai-truoc-e5.json` (`T073-khai-e5-khoa-1`). Đây là lần đầu chạy; theo luật đã khai, lần đầu là kết quả chính. Bằng chứng nằm ở `results/T-073/e5/`.

## 1. Ba mốc giờ (UTC)

| Mốc | Giờ | Nguồn |
|---|---|---|
| Tải ×1 bắt đầu | 02:07:30.559Z (1800 s, kết thúc 02:37:31.520Z, exit 0) | `e5/luot/DA-PHAT`, `DA-XONG`, `receive.json` (12 hash khớp) |
| **Gây lỗi** | 02:17:30Z theo nhật ký điều khiển (`toi tiem` 02:17:30.311Z, `tiem rc=0` 02:17:36.185Z). Giờ chính thức nằm trong sổ `/srv/rca-lab/ledger/t073-e5-01.jsonl`; người chấm đọc sổ sau lượt, người làm không đọc. | `e5/luot/nhat-ky.jsonl` |
| Gỡ lỗi | 02:27:40–02:27:44Z; `inj3 verify` sau gỡ: sạch | `e5/luot/verify-sau.txt` |
| **Phát cảnh báo** | t̂ = 02:18:30Z (`startsAt` của `t072-live`); webhook nhận lúc 02:18:30.039Z | `e5/su-co/bbc0a6d44f.json` |
| Ghi chỉ mục G1 (mốc phụ) | 02:32:47.165Z (bước g1 kết thúc). t̂ → G1 = 857,2 s | như trên, `do_tre_giay` |
| **Dashboard hiện ca** | 02:33:16.8Z: lần đầu truy vấn panel "Danh sách ca" (đúng target của panel, bản V082) trả ca `7577dd5b`, nguồn `t073-b`. 02:33:28.8Z: thấy ca trên giao diện. Mở ca được, cửa sổ 02:13:30–02:23:30Z, 27 panel, không panel nào "No data" hay lỗi. | `e5/s49-anh-ca-moi-trong-danh-sach.jpg`, `e5/s49-anh-mo-ca-7577dd5b.jpg`, mục 4 |

Từ t̂ đến lúc dashboard hiện ca: **≈ 886,8 s ≈ 14,8 phút** (tính theo API). Từ t̂ đến lúc thấy ca trên giao diện: 898,8 s. Cả hai đều dưới N = 25 phút.

Giới hạn của mốc "hiện ca": tôi mở dashboard sau khi bộ điều phối báo sự cố kết thúc (02:32:47Z). Mốc này là lúc **người làm thấy** ca, nên chỉ là cận trên. Ca có thể đã xem được từ ngay sau khi G1 ghi xong.

## 2. Tuyến xử lý của sự cố `bbc0a6d44f`

- Cảnh báo, đều lớp `he-thong`, gom chung một sự cố theo `T072-gom-2`:

  | Luật | startsAt | Nhận | Hết |
  |---|---|---|---|
  | `t072-live` | 02:18:30Z | 02:18:30.04Z | 02:27:50Z |
  | `t072-p95-payment` | 02:19:20Z | 02:19:28.20Z | 02:26:00Z |
  | `t072-loi-payment` | 02:19:30Z | 02:19:32.75Z | 02:33:20Z |

  t̂ của sự cố là t̂ của cảnh báo đầu tiên.
- Sự cố khác có cùng khung giờ: chỉ có tin Test `bfa21268f6` (lớp `quan-sat`, không chạy RCA). Spool có 7 dòng.
- Các bước:

  | Bước | Giây | Kết quả |
  |---|---|---|
  | stage | 12,12 | ok; bắt đầu 02:31:03.55Z = t̂ + 753 s |
  | p7 | 33,93 | ok; status OK, không có lỗi "nhiều chuỗi runtime" |
  | bo_sung | 14,67 | ok |
  | v082 | 28,27 | ok |
  | kiem_dau_vao | 0,57 | ok |
  | g1 | 14,04 | ok |

  Tổng thời gian xử lý ≈ 104 s; đo dưới tải ở E3 là 143 s.
- Đầu ra: mã ca M1 `7577dd5b`. V082 trả `CAUSE_FOUND`, nhóm hạng 1 `booking-service`. Đây **không phải** đánh giá độ chính xác (việc đó thuộc W6–W7), và chưa đối chiếu với đáp án.

## 3. Đối chiếu tiêu chí khai trước

| Tiêu chí (`khai-truoc-e5.json` → `tieu_chi`) | Kết quả |
|---|---|
| `ket_qua_chuc_nang.dat` (a): có ≥ 1 sự cố `he-thong` với t̂ ∈ [mốc tiêm, mốc tiêm + 600) | Có: t̂ 02:18:30Z ∈ [02:17:30, 02:27:30) **theo nhật ký điều khiển**. Người chấm cần đối chiếu với sổ. |
| (b) dashboard hiện ca trong N = 25 phút kể từ t̂ | Đạt: 14,8 phút (API), 15,0 phút (giao diện) |
| (c) `che_do_b.kiem_t.t_loi_bang_t_hat = true` | Đạt. Cửa sổ lõi N = [t̂−300, t̂), A = [t̂, t̂+300); `e5/s49-che-do-b.txt` |
| (d) V082 `trung_sha = true` | Đạt; hai lần chạy cùng ra `23b873ae…` |
| **Kết luận chức năng** | **đạt**, với điều kiện sổ tiêm xác nhận mốc gây lỗi |
| `ket_qua_phu_cua_so` | `phu.du_cua_so = false`. Trace đủ: 122780 mẫu, lỗ lớn nhất 0,395 s. Thiếu bắt buộc: 6 metric của `payment-service` (cpu, error, latency-50, latency-90, mem, workload), lỗ lớn nhất 365 s, ngưỡng 40 s. Log chỉ báo: 11114 mẫu. Theo khai trước, ghi là **"đã hiển thị nhưng thiếu phủ"**: không viết "lõi nhận đủ cửa sổ". **Thiếu có thể do chính lỗi**, vì ô này pause container Payment nên Payment ngừng phát metric; chưa phân xử. Không coi là lỗi hạ tầng, không chạy lặp. |
| Quy tắc lặp (`bang-o-e5.md` §5) | Không có lý do lặp. Tải chạy đủ, `inj3 start` thành công, verify trước và sau đều sạch. Prometheus, Collector, Loki, Tempo không restart từ 17/11. Grafana chạy liên tục từ 02:04:38Z, trước cửa sổ [02:07:30, 02:28:30). Dịch vụ T-073 không dừng. |

## 4. Kiểm W5 khi đổi nguồn (S4-4 đến S4-8)

| Bước | Kết quả | Bằng chứng |
|---|---|---|
| S4-1 đến S4-3 | K1, K5, K7, K9, K10 đạt; K6 đạt sau khi có tải (route payment có ~139 request trong 10 phút, đầu dò 8083 cách 7 s). Bộ `t073-e5-001` là bản chép, cây trùng `8b552312…`. Bộ nhận healthy. | `e5/s41*`, `s42`, `s43`, `luot/k6-sau-tai.txt` |
| S4-4, S4-5 | Đổi checkout `ecdeed2` → E5 `81a92736…`. Restart Grafana: health 13.3.0/`6f8ce3c693…`. Không có lỗi `provisioning.alerting`/`provisioning.dashboard`. | `e5/s44`, `s45` |
| S4-6 | Hai integration trong `t072-bo-nhan-nhe` (giả định ở §2 nay đã kiểm). 11 luật trùng `t072-luat.yaml`, hash chuẩn hóa `143d8817…`. Mỗi integration có nút Test riêng. Test `t073-webhook-e5` → spool T-073 nhận đúng 1 dòng, T-072 không đổi. Test `t072-webhook` → T-072 nhận đúng 1 dòng, spool T-073 không đổi. | `e5/s46*` |
| S4-7 | Ba dashboard hiện hành chỉ đọc `t073-e5-001`. Danh sách có 53/28/28 ca, bằng số trong chỉ mục. Ca cũ `eb48d6b3` và trang phát lại mở được. | `e5/s47*` |
| S4-7b | Commit P: 6 trang lưu trữ đều nạp được, có ca, không panel "No data" hay lỗi; trang hiện hành vẫn đọc `t073-e5-001`. Trả về E5: 6 trang đã gỡ, hash dữ liệu lưu trữ trước và sau trùng `c94da63c…`. **Còn 3 thư mục rỗng** (`2026-11-12-g2-v6`, `2026-11-13-l3-p7`, `2026-11-14-l4-temporary`); không xóa tay, trình điều phối. | `e5/s47b-*` |
| S4-8, K8 | Bộ điều phối chạy (pid 1001850). Tin Test được gom thành sự cố lớp `quan-sat`, không chạy RCA. Grafana đang đánh giá luật. | `e5/s48`, `s49-k8.txt` |

## 5. Giới hạn và câu hỏi mở

- Chỉ có **một** lượt, ở tải ×1, cho một ô. Kết quả không suy ra cho các ô khác, tải khác hay độ chính xác.
- Mốc gây lỗi chính thức cần người chấm đọc sổ tiêm.
- Thiếu phủ metric Payment: chưa phân xử có phải do chính lỗi hay không. Muốn phân xử cần đối chiếu mốc mẫu cuối và mẫu đầu của các chuỗi Payment với mốc pause/unpause trong sổ (việc của người chấm).
- Mốc "dashboard hiện ca" chỉ là cận trên, như ghi ở mục 1.
- Ghi chú "Hash do chỉ mục T-064 cấp" trên trang ca mới là chữ của mẫu G1 có sẵn, không đúng với ca `t073-b`. Chỉ ghi lại; không sửa G1 trong E5 (file ghim T-067).
- Liên kết metric `live-down` trên trang ca hỏng: giới hạn đã biết từ CX-13b, không kiểm lại.
- Kiểm "No data" dựa trên chữ hiển thị sau khi cuộn hết trang, không đọc từng phản hồi truy vấn.

## 6. Trạng thái máy sau E5

- exp-obs: `/opt/rca-lab` ở E5 `81a92736…`, cây sạch. Grafana gửi cảnh báo tới hai đích. Bộ điều phối T-073 **vẫn chạy** (pid 1001850, ra `/srv/rca-lab/runs/t073-e5-01`). `flash-ticket-t073-webhook` vẫn chạy.
- exp-app: Payment đã unpause; `inj3 verify` sạch.
- Laptop: tunnel `127.0.0.1:3000` vẫn mở, phiên Grafana của Minh vẫn đăng nhập trong pane.
- Hoàn tác theo §5 (commit H) **chưa** làm; chờ điều phối hoặc Minh quyết.
