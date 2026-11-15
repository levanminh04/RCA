# Thay đổi trên `exp-obs`: cài Infinity cho G2 (T-061, 11/11/2026)

Minh duyệt việc 4 ngày 11/11/2026 ("duyệt việc 4"; "Claude làm luôn, không gọi lại Codex T58 nữa"). Claude thực hiện qua SSH khóa `D:/RCA-ext/keys/exp-obs/…` (ngoài repo), host key đã ghim trong `D:/RCA-ext/overnight-T058/out/known_hosts`. Không đọc `grafana.env`.

## Đã thay đổi

| Trên máy | Trước | Sau |
|---|---|---|
| `/opt/flash-ticket-obs/pinned/compose.json` | sha256 `c6be32e0…` (= bản T-058 `results/T-058/dem-2026-11-10/config-public/obs/compose.json`) | sha256 `684d39bd…` = [`compose-sau.json`](compose-sau.json). Chỉ dịch vụ `grafana` đổi: thêm `environment.GF_PLUGINS_PREINSTALL_SYNC = yesoreyeram-infinity-datasource@4.1.6`; thêm volume `/opt/flash-ticket-obs/rca-ket-qua:/usr/share/grafana/public/rca:ro` |
| Sao lưu | — | `pinned/compose.json.bak-T061-20261111` (= bản trước, `c6be32e0…`) |
| `pinned/provisioning/datasources/infinity.yaml` | không có | mới, = [`infinity.yaml`](infinity.yaml), uid `infinity-rca`. `sources.yaml` không đổi (`8979f4b3…`) |
| `/opt/flash-ticket-obs/rca-ket-qua/` | không có | hai mẫu 0.2 và `chi-muc/danh-sach-su-co.json`, hash trùng `results/T-061/mau/`. **Không chép bản phát lại** (có đáp án) |
| Container `flash-ticket-obs-grafana` | chạy 13 giờ | tạo lại 14:50:57Z; Prometheus, Loki, Tempo, Collector **không** khởi động lại |

Hash đầy đủ: [`truoc.txt`](truoc.txt), [`sau.txt`](sau.txt), bản trước [`compose-truoc.json`](compose-truoc.json).

## Kết quả kiểm sau cài (14:51–14:52Z)

- `/api/health`: Grafana 13.3.0, database ok.
- Plugin `yesoreyeram-infinity-datasource` 4.1.6, tệp chạy `gpx_infinity_linux_arm64`; log "Plugin successfully installed".
- Log "inserting datasource from configuration name=Infinity uid=infinity-rca".
- Trong container: `wget http://localhost:3000/public/rca/f4a8c021.json` và `…/chi-muc/danh-sach-su-co.json` trả đúng file.
- Bộ nhớ Grafana 340,6/768 MB (trước 371,8 MB; số đo tức thời sau khởi động, chưa đo dài hạn).
- Log có ba dòng `level=error` về thư mục provisioning `dashboards`, `plugins`, `alerting` không tồn tại — các thư mục tùy chọn, không liên quan Infinity.
- Grafana tự cài thêm `stackdriver`, `grafana-advisor-app` qua bộ cài nền mặc định của bản 13 khi container mới tạo; không do cấu hình này.
- **Chưa kiểm:** truy vấn Infinity thật trên `exp-obs` (API cần đăng nhập; Claude không đăng nhập bằng mật khẩu). Minh kiểm trên giao diện: nguồn "Infinity", URL `http://localhost:3000/public/rca/<mã ca>.json` và `…/public/rca/chi-muc/danh-sach-su-co.json`; cấu hình truy vấn giống dashboard thử `results/T-061/grafana/provisioning/dashboards/t061-infinity.json` (đổi `public/t061` thành `public/rca`, uid nguồn `infinity-rca`).

## Sự cố trong lúc làm (giữ để truy vết)

Lần chạy `docker compose -f compose.json up -d grafana` đầu tiên (14:50:31Z) thiếu `-p`, nên compose dùng tên project `pinned` thay vì `flash-ticket-obs-pinned`. Nó tạo network rỗng `pinned_default` rồi dừng vì trùng tên container; container cũ không bị đụng. Đã xóa network đó (0 container) và chạy lại với `-p flash-ticket-obs-pinned` (14:50:57Z).

## Hoàn tác

```bash
cd /opt/flash-ticket-obs/pinned
cp -p compose.json.bak-T061-20261111 compose.json
rm provisioning/datasources/infinity.yaml
docker compose -p flash-ticket-obs-pinned -f compose.json up -d grafana
```

Thư mục plugin nằm trong volume `grafana-data`; nếu muốn xóa hẳn: `docker exec flash-ticket-obs-grafana rm -rf /var/lib/grafana/plugins/yesoreyeram-infinity-datasource` rồi khởi động lại Grafana.

## Quan hệ với hash của T-058

Hash `c6be32e0…` trong hồ sơ T-058 là ảnh chụp cấu hình **lúc lượt đêm 10–11/11**, vẫn đúng cho lượt đó. Từ 14:50:57Z ngày 11/11, cấu hình `exp-obs` đang chạy là `684d39bd…`. Ai dùng `exp-obs` cho lượt chạy mới phải lấy hash hiện tại (bảng trên), không so với hồ sơ T-058. Thay đổi chỉ chạm Grafana (lớp hiển thị); không đổi Prometheus, Loki, Tempo, Collector, nên không đổi dữ liệu M1 đọc.

## Minh kiểm trên giao diện — 11/11/2026

Minh gửi ảnh dashboard "T-061 thử Infinity" sau khi đăng nhập Grafana (đã đăng nhập, sidebar đầy đủ): bảng danh sách sự cố hiện đúng 2 dòng (`f4a8c021` CAUSE_FOUND, nghi nguồn api-gateway, 16 có hạng; `c12e47ab` NO_INTRINSIC_ANOMALY, 17), bản ghi sự cố, đồ thị và bảng hạng của ca `c12e47ab` đúng như mẫu. Nếu ảnh chụp trên `exp-obs` (qua đường hầm) thì truy vấn Infinity trên máy thật đã đạt; ảnh không hiện thanh địa chỉ nên Claude chưa tự xác nhận được máy nào. Thử trong Explore chưa ra dữ liệu vì Parser để `JSONata` và URL mặc định của plugin (hướng dẫn của Claude thiếu chỉ dẫn mở mục "Parsing options & Result fields").
