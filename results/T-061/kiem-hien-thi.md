# Kiểm hiển thị trên Grafana cục bộ (T-061, câu 4)

Ngày 11/11/2026, laptop Windows 11, Docker Desktop 28.3.2. Không chạm `exp-obs`, `exp-app`.

## 1. Cách chạy lại

```bash
cd results/T-061 && bash chay-tat-ca.sh
docker pull grafana/grafana:13.3.0
MSYS_NO_PATHCONV=1 docker run -d --name t061-grafana -p 127.0.0.1:3061:3000 -e GF_AUTH_ANONYMOUS_ENABLED=true -e GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer -e GF_ANALYTICS_REPORTING_ENABLED=false -e GF_ANALYTICS_CHECK_FOR_UPDATES=false -e GF_NEWS_NEWS_FEED_ENABLED=false -e GF_PLUGINS_PREINSTALL_SYNC=yesoreyeram-infinity-datasource -v "D:/RCA-flashticket/results/T-061/grafana/provisioning:/etc/grafana/provisioning:ro" -v "D:/RCA-flashticket/results/T-061/mau:/usr/share/grafana/public/t061:ro" grafana/grafana:13.3.0
cd results/T-061 && py -3 -B infinity-thu.py && docker restart t061-grafana
```

Mở `http://127.0.0.1:3061/d/t061-mau/t-061-mau-ket-qua-rca?kiosk` (Raw frames) hoặc `http://127.0.0.1:3061/d/t061-infinity/t-061-thu-infinity?var-ca=c12e47ab` (Infinity). Lệnh `docker run` trên là bản gói C (bản phiên 1 không có plugin và thư mục `public/t061`). Sửa khung rồi thì `docker restart t061-grafana` (Grafana không tự nạp lại file gắn qua bind mount của Docker Desktop trong lượt thử). Xóa: `docker rm -f t061-grafana`.

- Image: `grafana/grafana:13.3.0`, digest `sha256:488984b7…` trùng digest đã ghim cho `exp-obs` (`results/T-058/dem-2026-11-10/image-pins-obs.json`). Đây là index đa kiến trúc: laptop chạy biến thể amd64, `exp-obs` chạy arm64. `/api/health` trả `version 13.3.0`, commit `6f8ce3c6…`.
- Dung lượng image sau giải nén 1,46 GB (`docker image inspect`), lớn hơn ước lượng "vài trăm MB" của SPEC; dưới ngưỡng luật cứng 8.
- Nguồn: TestData (`grafana-testdata-datasource`, uid `testdata-t061`), kịch bản **Raw frames**. Dashboard `t061-mau` (provisioning) gồm 4 cặp panel: chữ (bản ghi sự cố) + Node graph, cho `c12e47ab`, `f4a8c021`, và hai bản phát lại. Khung lấy từ `grafana/frames/*.json`, dựng bằng `khung-grafana.py` từ JSON định dạng.

## 2. Kết quả

| Kiểm | Kết quả | Bằng chứng |
|---|---|---|
| TestData đọc hai khung `nodes`, `edges` | **Đạt** ở trình duyệt. Kịch bản Raw frames chạy phía giao diện; gọi thẳng `/api/ds/query` với `raw_frame` thì máy chủ lỗi 500 (panic `scenarios.go:266`, kể cả khi nội dung rỗng; `random_walk` trả 200). Không ảnh hưởng dashboard | log container; [`hien-thi/00-dashboard-tong.jpg`](hien-thi/00-dashboard-tong.jpg) |
| Ca `f4a8c021`: màu theo vai trò | **Đạt.** Đo `getComputedStyle`: api-gateway và ticket-service viền `rgb(224,47,68)` = `#E02F44`; config-discovery `rgb(255,152,48)` = `#FF9830`; event-service `rgb(202,149,229)` = `#CA95E5`; 13 nút còn lại `rgb(142,142,142)` = `#8E8E8E` | [`hien-thi/dom-mau.json`](hien-thi/dom-mau.json), [`01`](hien-thi/01-f4a8c021-node-graph.jpg) |
| Ca `f4a8c021`: nổi bật | **Đạt.** Chỉ api-gateway có nền đặc `rgb(170,0,0)` (`highlighted`) | như trên |
| Ca `f4a8c021`: chữ, hạng, thiếu dữ liệu | **Đạt.** Chữ trong nút: `#1 nghi nguồn`, `#2 nghi nguồn`, `#3 bị kéo theo`, `? thiếu dữ liệu`, `không cờ bình thường`; dòng dưới: tên + lớp M1 | `dom-mau.json` |
| Danh tính nút | **Đạt.** 17 nhóm SVG `data-node-id` đúng 17 `id` của mẫu | `dom-mau.json` |
| Cạnh: danh tính hai đầu, chiều | **Đạt bằng mắt và rê chuột.** 8 mũi tên đúng chiều bên gọi → bên được gọi (api-gateway → booking-service/event-service/config-discovery; 5 service → config-discovery). Rê lên cạnh api-gateway → booking-service tô đúng hai đầu này. Menu chi tiết của cạnh **chưa mở được** khi click trong lượt thử (cạnh mảnh); không đo cạnh bằng DOM | [`04`](hien-thi/04-f4a8c021-canh-api-gateway-booking.jpg) |
| Menu chi tiết nút (`detail__*`, `displayName`) | **Đạt** với Grafana 13.3.0: click api-gateway hiện Vai trò, Hạng 1, Vùng "gốc, cách 1, cách 2", Bằng chứng 4 kênh; event-service hiện "không có hạng", "ngoài vùng", "—". Rủi ro diễn đàn ở `DE-XUAT-HUONG-GRAFANA-RCA.md` §7.2 không xảy ra ở bản này | [`02`](hien-thi/02-f4a8c021-chi-tiet-api-gateway.jpg), [`03`](hien-thi/03-f4a8c021-chi-tiet-event-service.jpg) |
| Ca `c12e47ab` | **Đạt.** 17 nút xám, chữ `không cờ`, không nút nào nổi bật; 8 cạnh | [`05`](hien-thi/05-c12e47ab-node-graph.jpg), `dom-mau.json` |
| Phát lại không đổi hiển thị dự đoán | **Đạt.** DOM (màu, nền, chữ trong nút) của panel phát lại trùng panel gốc ở cả hai ca. Đáp án chỉ hiện trong menu chi tiết, dòng "Đáp án (phát lại)" ở event-service | [`06`](hien-thi/06-f4a8c021-phat-lai-node-graph.jpg), [`07`](hien-thi/07-f4a8c021-phat-lai-chi-tiet-event-service.jpg) |

Ảnh chụp bằng trình duyệt trong app (viewport giả lập 1400×950, ảnh lưu 800×543). Ảnh chụp bằng Edge headless hỏng (chỉ có "Computing layout" hoặc logo) vì bố cục Node graph tính trong worker và headless chụp trước khi xong; giữ ở [`hien-thi/headless-hong/`](hien-thi/headless-hong/). `dom-mau.json` là bản dựng từ dữ liệu trích từ trình duyệt (kết quả `javascript_exec` chép vào bằng script), không phải bản ghi thô lưu tự động.

**Kiểm lại trên mẫu 0.2 (gói C, 11/11/2026):** panel Raw frames ca `f4a8c021` cho DOM nút trùng từng chuỗi với lần đo phiên 1 (màu, nền nổi bật, chữ); panel chữ hiện thêm "trạng thái M1 `OK`". Dashboard đang phục vụ được nạp lại sau khi khởi động lại container.

### Thử Infinity (gói C3)

Plugin `yesoreyeram-infinity-datasource` **4.1.6** (cài qua `GF_PLUGINS_PREINSTALL_SYNC` lúc tạo container), nguồn uid `infinity-t061` (`grafana/provisioning/datasources/infinity.yaml`). Thư mục `mau/` gắn vào `public/t061/` của Grafana.

| Bước | Kết quả | Bằng chứng |
|---|---|---|
| 1. Máy chủ Grafana tự tải được JSON (không qua trình duyệt) | **Đạt.** Trong container: `wget http://localhost:3000/public/t061/c12e47ab.json` trả đúng file | lệnh ghi ở LOG phiên 2 |
| 2. Truy vấn Infinity phía máy chủ (`/api/ds/query`, parser `backend`) đọc thẳng JSON 0.2: `root_selector` `nut`/`canh`/`xep_hang`/`su_co`, selector lồng `hien_thi.mau` | **Đạt 13/13** cho cả hai ca: khung `nodes` đúng id, title, color, highlighted, mainstat theo thứ tự mẫu; `detail__hang` giữ `null` cho event-service; khung `edges` đúng id/source/target/color; bảng hạng đúng số khối và cỡ khối; bản ghi sự cố đúng mã, trạng thái, kết luận, mốc | [`infinity-ket-qua.json`](infinity-ket-qua.json), `infinity-thu.py` |
| 3. Đổi ca A → B trên giao diện (menu biến `ca`) | **Đạt.** Từ `c12e47ab` sang `f4a8c021`: bản ghi sự cố `NO_INTRINSIC_ANOMALY` → `CAUSE_FOUND`; nút đổi màu và nổi bật (api-gateway nền `rgb(170,0,0)`, ticket-service đỏ, config-discovery cam, event-service tím); bảng hạng đổi sang 4 khối 1/1/1/13. DOM 17 nút sau khi đổi trùng chuỗi với panel Raw frames của cùng ca | [`08`](hien-thi/08-infinity-ca-A-c12e47ab.jpg), [`09`](hien-thi/09-infinity-doi-sang-ca-B-f4a8c021.jpg) |
| Cạnh khi đổi ca | **Không quan sát được việc đổi:** hai mẫu có cùng 8 cạnh. Mỗi ca kiểm được cạnh khớp đúng mẫu của nó (bước 2) | — |
| 4. Danh sách sự cố từ file chỉ mục `mau/chi-muc/danh-sach-su-co.json` (Minh duyệt 11/11/2026) | **Đạt.** Truy vấn Infinity phía máy chủ không lỗi; đúng 2 dòng, mới nhất trước, mã/trạng thái/kết luận/nút nghi nguồn khớp chỉ mục (2/2 phép kiểm, `infinity-ket-qua.json`). Trên giao diện: đang ở `f4a8c021`, bấm mã `c12e47ab` (liên kết `var-ca=${__value.raw}`) mở đúng sự cố; bản ghi, đồ thị (17 nút xám), bảng hạng (1 khối) đổi theo | [`10`](hien-thi/10-infinity-danh-sach-dang-o-f4a8c021.jpg), [`11`](hien-thi/11-infinity-danh-sach-bam-mo-c12e47ab.jpg) |

Giới hạn: cách cấp file qua `public/` của chính Grafana chỉ để thử cục bộ. Chưa kiểm: bản arm64 của plugin, nơi đặt JSON và cấu hình host cho phép trên `exp-obs`, menu chi tiết qua Infinity (chỉ khai `detail__vai_tro`, `detail__hang`).

## 3. Quan sát cho G2 (không phải lỗi định dạng)

- Bố cục Layered mặc định đặt 10 nút không cạnh thành lưới bên phải; panel nhỏ (nửa màn hình) cắt mất một phần đồ thị. Nên cho Node graph rộng cả hàng hoặc dùng `fixedX/fixedY` (khi dùng thì mọi nút phải có).
- Nút nổi bật có nền đỏ đậm; chữ tối trên nền đỏ khó đọc ([`01`](hien-thi/01-f4a8c021-node-graph.jpg)). Nếu G2 thấy khó đọc: bỏ `highlighted`, dùng viền dày hoặc ghi "#1" ở `title`.
- Khi khung trình duyệt ẩn, trang chạy nền và bố cục mất 10–20 giây mới hiện; khi hiển thị bình thường thì nhanh hơn. Chưa đo thời gian hiển thị.
- Chú giải `mainstat / secondarystat / color` dưới panel là chú giải mặc định của Grafana; không mang nghĩa cho người xem.

## 4. Phần chưa xác nhận (OPEN cho G2)

- Infinity: đạt cục bộ (§2); trên `exp-obs` chưa thử. PostgreSQL: chưa thử (xem `dinh-dang-ket-qua-rca.md` §7).
- Bản ghi `ERROR`/`UNSUPPORTED`/`NO_EVIDENCE`: mới kiểm khung và chữ panel; chưa vẽ trên Grafana.
- Liên kết từ menu chi tiết sang Explore (Prometheus/Tempo): chưa dựng; truy vấn trong định dạng chưa chạy trên kho `exp-obs`.
- Menu chi tiết cạnh; cạnh tô đỏ khi có bằng chứng cạnh (hai mẫu không có bằng chứng cạnh).
- Hiển thị trên `exp-obs` (arm64, cấu hình thật): chưa thử, vì không thuộc phạm vi T-061.
