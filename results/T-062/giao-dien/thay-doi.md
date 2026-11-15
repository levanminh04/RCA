# Thay đổi trên máy — phiên giao diện G1 (T-062)

Chỉ ghi thay đổi trên `exp-obs` (Grafana và `rca-ket-qua`). Giờ là UTC (đồng hồ `exp-obs`). Không đọc `grafana.env`, không in mật khẩu.

| Giờ UTC | Máy | Lệnh / việc | Kết quả |
|---|---|---|---|
| 18:39 | exp-obs | Chỉ đọc: `docker ps`, `free -m`, `ls` thư mục `pinned/` và `rca-ket-qua/`, đọc phần `grafana` của `compose.json` (bỏ `env_file`), tên biến `GF_*` (không đọc giá trị mật khẩu) | Grafana 13.3.0 chạy, cổng `10.0.0.215:3000`; chưa có `provisioning/dashboards/`; `GF_AUTH_ANONYMOUS_ENABLED=false`; `compose.json` sha256 `684d39bd…` (= sau T-061) |
| 18:42 | exp-obs | Chỉ đọc: nhãn Prometheus (`service_name`), nhãn Loki, cấu hình Tempo | Để đặt truy vấn Explore đúng nhãn |
| 18:50:00–18:50:05 | exp-obs | `scp -r mau → /opt/flash-ticket-obs/rca-ket-qua/mau` (thư mục mới, trước đó không có); `chmod -R a+rX mau` | Bản sao mẫu T-061 (2 ca, chỉ mục, 2 bản phát lại) + chỉ mục phát lại mới; sha256 từng file trùng `results/T-062/giao-dien/rca-ket-qua-mau/mau/` và (với file chép) trùng `results/T-061/mau/`. Không sửa file cũ ở `rca-ket-qua/` |
| 18:58:19 | exp-obs | `scp` ghi đè `rca-ket-qua/mau/phat-lai/chi-muc/danh-sach-phat-lai.json` (file do phiên này tạo lúc 18:50; thêm trường `so_thuc_the_quan_sat`, `so_thuc_the_co_hang`) | sha256 `360b9aa7…`, trùng bản trong repo |
| 18:59:47 | exp-obs | `mkdir /opt/flash-ticket-obs/pinned/provisioning/dashboards` (trước đó không có) | thư mục mới, nằm trong bind mount `provisioning:/etc/grafana/provisioning:ro` đã có; **không sửa `compose.json`** |
| 18:59:48 | exp-obs | `scp provider.yaml rca-g2-chinh.json rca-g2-phat-lai.json → pinned/provisioning/dashboards/`; `chmod 644` | sha256 lần 1: provider `97facb72…`, chính `bd75c88b…`, phát lại `8f2bf6cb…` (= `grafana/dashboards/` trong repo lúc đó) |
| 18:59:49 | exp-obs | `docker restart flash-ticket-obs-grafana` | Up lại sau ~3 s; log 18:59:53 "starting to provision dashboards" → "finished to provision dashboards", không lỗi dashboard. Hai lỗi `provisioning/plugins`, `provisioning/alerting` không tồn tại là lỗi cũ (đã có từ T-061). `/api/health` 13.3.0 ok. Prometheus, Loki, Tempo, Collector không khởi động lại |
| 19:05:13 | exp-obs | `scp` ghi đè `rca-g2-chinh.json`, `rca-g2-phat-lai.json` (bản 2: bố cục mới, vị trí nút cố định theo tầng gọi, chữ trạng thái) | sha256 chính `ec06258c…`, phát lại `5b032914…` |
| 19:05:14 | exp-obs | `docker restart flash-ticket-obs-grafana` | 19:05:17–18 "starting/finished to provision dashboards", không lỗi |
| 19:06:42 | exp-obs | `scp` ghi đè `rca-g2-chinh.json`, `rca-g2-phat-lai.json` (bản 3: đổi nhãn ô *Nguồn kết quả* thành "Thư mục chính rca-ket-qua…") | sha256 chính `77897006…`, phát lại `b81c8086…`, provider `97facb72…` (= `grafana/dashboards/` trong repo) |
| 19:06:43 | exp-obs | `docker restart flash-ticket-obs-grafana` | 19:06:47 "finished to provision dashboards"; một dòng `job cleanup controller failed … context canceled` lúc container cũ tắt (không ảnh hưởng). Up |
| 21:13:08 | exp-obs | Chỉ đọc: `sha256sum` thư mục `pinned/provisioning/dashboards/` | còn đúng bản 3 (`77897006…`, `b81c8086…`) |
| 21:13:16 | exp-obs | `scp` ghi đè `rca-g2-chinh.json`, `rca-g2-phat-lai.json` (bản 4, sau khi xem ca thật `a5539fba`: menu nút rút gọn dòng *Bằng chứng* — tối đa 3 kênh, bỏ tiền tố gói Java của tên thao tác, cắt 48 ký tự; bảng *Bằng chứng* và *Vì sao … kéo theo* có câu thay "No data"); `chmod 644` | sha256 chính `2039e109…`, phát lại `0393fb3e…`, provider `97facb72…` (= `grafana/dashboards/` trong repo) |
| 21:13:17 | exp-obs | `docker restart flash-ticket-obs-grafana` | 21:13:20 "starting/finished to provision dashboards", không lỗi dashboard (hai lỗi cũ `plugins`/`alerting`); `/api/health` 13.3.0 ok |

## Hoàn tác

```bash
rm -r /opt/flash-ticket-obs/pinned/provisioning/dashboards
rm -r /opt/flash-ticket-obs/rca-ket-qua/mau
docker restart flash-ticket-obs-grafana
```

Không đụng: `compose.json` (vẫn `684d39bd…`), datasources, Prometheus, Loki, Tempo, Collector, `/opt/rca-tai`, container `rca-tai-*`, `exp-app`, máy tải.

## Ngoài `exp-obs` (laptop, chỉ để kiểm)

Grafana 13.3.0 bản Windows (tải từ `dl.grafana.com`, sha256 khớp file `.sha256` của nguồn) + Infinity 4.1.6, chạy trong thư mục scratchpad của phiên, cổng `127.0.0.1:3062`, ẩn danh. Nguồn Prometheus/Loki/Tempo trỏ qua đường hầm SSH tới `127.0.0.1:9090/3100/3200` của `exp-obs` (chỉ đọc); Infinity đọc file qua đường hầm tới `public/rca` của Grafana `exp-obs`. Lý do: Grafana `exp-obs` cần đăng nhập bằng mật khẩu, Claude không nhập mật khẩu (SPEC T-062 luật 8). Đã tắt sau khi kiểm.

Lần 2 (kiểm ca thật `a5539fba`, khoảng 21:05–21:20 UTC): bật lại bản thử và đường hầm (thêm `127.0.0.1:3000 → 10.0.0.215:3000` để Infinity đọc `public/rca`). Lần khởi động đầu, bản thử tự cập nhật plugin Prometheus 13.2.5 → 13.2.6 và hỏng giữa chừng (Windows giữ file), nên các panel Prometheus báo lỗi "Plugin not registered". Đây là lỗi của bản thử, không phải của dashboard hay `exp-obs`. Đã xóa thư mục plugin hỏng trong scratchpad, thêm `[plugins] preinstall_auto_update = false` vào `custom.ini` của bản thử rồi khởi động lại; sau đó truy vấn Prometheus chạy. Đã tắt bản thử và đường hầm sau khi kiểm.

## Bản 5 (sửa sau phản biện Codex, 12/11/2026) — đã triển khai 02:01 UTC

Sửa trong repo lúc ~01:30–01:50 UTC ngày 12/11 theo F1′–F5 đã chốt (`tasks/T-062-dem-chang-1-4/REVIEW-G1-3.md`). Ban đầu chưa đẩy vì phiên điều phối đề nghị chờ lượt Codex kiểm Grafana thật (~01:30–01:49Z). Phiên điều phối đẩy chỉ mục phát lại thật mới lúc 01:52Z. Codex lượt 4 (`REVIEW-G1-4.md`) xác nhận bản 5 trong repo; triển khai như bảng dưới.

File G1 khác snapshot `results/T-062/manifest.json` (`tao_luc_utc` 2026-11-12T01:23:11Z), đo lúc ~01:50Z. G1 không sửa manifest; phiên điều phối quyết ghi nhận snapshot mới. File này (`thay-doi.md`) cũng đổi sau snapshot.

| File | sha256 trong manifest | sha256 hiện tại |
|---|---|---|
| `giao-dien/chi-muc-phat-lai.py` | `77723ff46c0f…` | `b0fb373643f6…` |
| `giao-dien/dinh-dang-chi-muc.md` | `591e8b7b6237…` | `59f15ad02341…` |
| `giao-dien/dung-dashboard.py` | `6652443a9650…` | `e901627b50da…` |
| `giao-dien/grafana/dashboards/rca-g2-chinh.json` | `2039e1096836…` | `473e276347ab…` |
| `giao-dien/grafana/dashboards/rca-g2-phat-lai.json` | `0393fb3e295a…` | `59d205f4d8e5…` |
| `giao-dien/phan-hoi-g1.md` | `3c215e25e31d…` | `a2124e0a476b…` |
| `giao-dien/rca-ket-qua-mau/mau/phat-lai/chi-muc/danh-sach-phat-lai.json` | `360b9aa7f7b2…` | `15fb2f4fa2d5…` |
| `giao-dien/XONG.md` | `0f0770b21dcb…` | (đổi tiếp khi triển khai) |
| `giao-dien/anh/16-…`, `17-…`, `18-…` | (mới) | `ee076d2f…`, `d333c89e…`, `5c096cfe…` |
| `giao-dien/prompt-phan-bien-g1-luot3.md` | (mới) | `ab71da7544a4…` |

Việc triển khai khi được báo (Codex lượt 3 khuyến nghị chỉ mục mới trước dashboard mới):
1. Phiên điều phối: `py -3 -B results/T-062/giao-dien/chi-muc-phat-lai.py results/T-062/ket-qua/phat-lai`, đẩy `phat-lai/chi-muc/danh-sach-phat-lai.json` lên `exp-obs:/opt/flash-ticket-obs/rca-ket-qua/phat-lai/chi-muc/`.
2. G1: `scp` chỉ mục mẫu mới → `rca-ket-qua/mau/phat-lai/chi-muc/`; `scp` hai dashboard → `pinned/provisioning/dashboards/`; `docker restart flash-ticket-obs-grafana`; ghi giờ và hash vào bảng trên.

| Giờ UTC | Máy | Lệnh / việc | Kết quả |
|---|---|---|---|
| 02:01:29 | exp-obs | `scp` chỉ mục mẫu mới → `rca-ket-qua/mau/phat-lai/chi-muc/danh-sach-phat-lai.json` (file do G1 tạo lúc 18:50); `scp` `rca-g2-chinh.json`, `rca-g2-phat-lai.json` → `pinned/provisioning/dashboards/`; `chmod 644` | sha256 chỉ mục mẫu `15fb2f4f…`, chính `473e2763…`, phát lại `59d205f4…`, provider `97facb72…` (= repo) |
| 02:01:30 | exp-obs | `docker restart flash-ticket-obs-grafana` | 02:01:34 "starting/finished to provision dashboards", không lỗi dashboard (hai lỗi cũ plugins/alerting); `/public/rca/mau/phat-lai/chi-muc/danh-sach-phat-lai.json` HTTP 200 |

## Bản 6 (F6–F8 sau lượt kiểm Grafana thật và Codex lượt 5) — đã triển khai 02:20 UTC

F6: liên kết bảng *Bằng chứng* dùng `${__data.fields.url:raw}` (trước đó mã hóa hai lần). F7: mô tả có điều kiện cho panel 5xx và log (nguyên văn phương án Codex lượt 5; không thay chữ "No data", không đổi truy vấn). F8: trang chính bỏ chữ "đáp án" ở liên kết và mô tả; bộ sinh chặn chữ này và `tap_chap_nhan` ở trang chính. Kiểm trên bản thử trước khi đẩy: bấm liên kết Tempo (trang chính, `e8661e0a`) và Prometheus (trang phát lại, `a89954d1`) trong bảng → Explore đúng truy vấn và cửa sổ, không lỗi parse, Tempo có trace (ảnh 19).

| Giờ UTC | Máy | Lệnh / việc | Kết quả |
|---|---|---|---|
| 02:19:55 | exp-obs | `scp` `rca-g2-chinh.json`, `rca-g2-phat-lai.json` → `pinned/provisioning/dashboards/`; `chmod 644` | sha256 chính `2eba7714…`, phát lại `553cf1d8…`, provider `97facb72…` (= repo); `dung-dashboard.py` `76a51caa…` |
| 02:19:56 | exp-obs | `docker restart flash-ticket-obs-grafana` | 02:20:00 "starting/finished to provision dashboards", không lỗi dashboard (hai lỗi cũ plugins/alerting) |

