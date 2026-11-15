G1 XONG MỘT PHẦN

# Giao diện G2 trên Grafana `exp-obs` — bàn giao của phiên giao diện (T-062, bước G1)

**Một phần vì một việc chưa kiểm được:** xem dashboard trên chính Grafana `exp-obs` — cần đăng nhập bằng mật khẩu, Claude không nhập mật khẩu (SPEC luật 8). Đã kiểm thay bằng một Grafana thử cùng phiên bản trên laptop, dùng đúng file dashboard và đọc đúng dữ liệu từ `exp-obs`; trên `exp-obs` mới kiểm log nạp dashboard (không lỗi). Mọi panel trong mục 2 đã dựng, đã triển khai và đã kiểm trên bản thử, với 2 ca mẫu T-061 và ca thật đầu tiên của T-062 (`a5539fba`, mục 2a).

## 1. Cách mở

```bash
ssh -i "D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key" -N -L 3000:10.0.0.215:3000 ubuntu@213.35.116.128
```

Rồi mở trình duyệt, đăng nhập Grafana như thường:

- Trang chính (không đáp án): `http://localhost:3000/d/rca-g2` — dashboard **"RCA — xem sự cố (G2)"**, thư mục **RCA**.
- Trang phát lại (có đáp án): `http://localhost:3000/d/rca-g2-phat-lai` — **"RCA — phát lại CÓ ĐÁP ÁN (G2)"**.

Cách dùng: ô **Nguồn kết quả** chọn "Thư mục chính rca-ket-qua" (kết quả T-062 khi có) hoặc "Mẫu T-061 (2 ca cũ)". Bấm **mã sự cố** trong bảng danh sách để mở (đặt luôn khung giờ ±15 phút quanh mốc). Bấm một **nút** trên đồ thị → menu: chi tiết, mục ① xem bằng chứng của thành phần đó (cuộn xuống), và các liên kết ↗ mở Tempo/Loki/Prometheus đúng cửa sổ nền + sự cố. Đổi ca bằng ô **Sự cố** ở đầu trang thì khung giờ không tự đổi: bấm biểu tượng liên kết ở panel *Sự cố đang xem* ("⏱ Đặt khung giờ…").

## 2. Panel đã làm

| # | Panel | Trạng thái | Kiểm |
|---|---|---|---|
| 1 | Hướng dẫn + chú giải màu | xong | ảnh 01 |
| 2 | Danh sách sự cố (từ `chi-muc/danh-sach-su-co.json`), bấm mã để mở | xong | đổi `f4a8c021` → `c12e47ab` bằng bấm mã: bản ghi, đồ thị, hạng đổi theo (ảnh 10) |
| 3 | Biến dashboard: Nguồn kết quả, Sự cố, Thành phần đang xem | xong | nhãn biến đọc được: "10/11 22:17 UTC — f4a8c021 — nghi api-gateway", "#3 config-discovery — bị kéo theo" |
| 4 | Sự cố đang xem: mã, kết luận M1, trạng thái, mốc, cửa sổ, nghi nguồn / kéo theo / thiếu dữ liệu, vùng nghi ngờ, độ phủ | xong | ảnh 02; bản ghi `ERROR` dựng tay: không vỡ, chữ "M1 lỗi (ERROR) — …", "Độ phủ: không có" |
| 5 | Đồ thị dịch vụ (Node graph). Đỏ "#hạng / nghi là nguồn", cam "#hạng / bị kéo theo", xám "(trống) / bình thường", tím "? / thiếu dữ liệu". Kích thước nút cố định (bán kính 36). Không dùng chữ "không cờ" | xong | ảnh 02, 03 |
| 6 | Vị trí nút cố định theo tầng gọi (hàng trên: chỉ gọi đi; giữa: vừa được gọi vừa gọi; dưới: chỉ được gọi; các hàng cuối: thành phần không có cạnh) để cả đồ thị vừa một khung | xong | ảnh 03; chỉ là vị trí vẽ, không mang nghĩa hạng |
| 7 | Menu nút: hạng chi tiết (đồng hạng), vùng nghi ngờ, bằng chứng, **mã lớp M1, tầng, điểm s, khóa xếp hạng chỉ ở đây**; liên kết ① và ↗ Tempo/Loki/Prometheus | xong | ảnh 04; liên kết Tempo mở Explore đúng service và cửa sổ 22:12–22:22 UTC, có trace (ảnh 07) |
| 8 | Bảng hạng thành phần, tô màu vai trò, bấm tên để chọn | xong | ảnh 06 |
| 9 | Bằng chứng của thành phần đã chọn: kênh, loại, hướng ↑↓, kiểu lan E5, khởi phát, điểm s, nút mở dữ liệu gốc | xong | liên kết Prometheus = truy vấn nguyên văn của adapter, lọc đúng chuỗi của thành phần, đúng cửa sổ; lỗi api-gateway tăng sau 22:18 UTC, khớp khởi phát 22:18:08 (ảnh 08) |
| 10 | "Vì sao … bị coi là kéo theo" (giải thích E5 của M1) | xong | config-discovery: 7 dòng, đường api-gateway → config-discovery (ảnh 06) |
| 11 | **Lớp thao tác (hướng 1)** cho thành phần đã chọn: request/giây, p90, lỗi 5xx theo route (Prometheus); trace của service (Tempo, mở trace thấy cây span cha → con); log có error/warn (Loki) | xong phần dữ liệu sống | ảnh 09 (discovery-server) |
| 12 | Trang phát lại: danh sách có cột root khai trước, tập chấp nhận, M1 xếp từng thành phần trong tập, hạng tốt nhất (theo e2), họ lỗi; đồ thị giữ màu/hạng dự đoán, mọi nút thuộc tập ghi "◆ <tên>"; bản ghi có root, tập, nhận xét, cảnh báo (bản 5, mục 2b) | xong; triển khai `exp-obs` 02:01 UTC (bản 5) | ảnh 05 (bản cũ), 16–18 (bản 5, bản thử) |

## 2a. Kiểm với ca thật đầu tiên của T-062: `a5539fba` (21:05–21:20 UTC ngày 11/11)

Phiên điều phối đã đẩy `rca-ket-qua/a5539fba.json` và chỉ mục chính (1 ca). Kiểm trên bản thử, ô *Nguồn kết quả* = "Thư mục chính", mọi truy vấn Infinity chạy qua `kiem-truy-van.py`, rồi xem bằng trình duyệt.

| Phần | Kết quả |
|---|---|
| Danh sách | 1 dòng: `a5539fba`, mốc 20:50:04 UTC, "M1 thấy thành phần có bất thường tự sinh", nghi nguồn keycloak, 17/17 có hạng, "chạy xong". Bấm mã đặt khung 20:35:04–21:05:04 UTC |
| Sự cố đang xem | cửa sổ nền 20:45:04 → 20:50:04, sự cố 20:50:04 → 20:55:04 UTC (lấy từ file); nghi nguồn #1 keycloak; bị kéo theo / thiếu dữ liệu: không có; vùng nghi ngờ gốc keycloak (cách 1 = cách 2 = keycloak); độ phủ 17/17, 14 cạnh (ảnh 11) |
| Đồ thị | keycloak đỏ "#1 / nghi là nguồn"; 16 thành phần xám "bình thường"; 14 cạnh gọi; 9 thành phần không cạnh ở các hàng dưới (ảnh 11) |
| Bảng hạng | #1 keycloak (2 bằng chứng), còn lại "bình thường", không ghi hạng (ảnh 12) |
| Bằng chứng keycloak | 2 kênh thao tác (span): `DELETE …OutboxEntryEntity` ↑ khởi phát 20:50:24 UTC, `SELECT …PersistentUserSessionEntity` ↑ 20:51:24 UTC, kiểu lan "không lan", nút "Tempo ↗" (ảnh 12) |
| Liên kết Tempo của bằng chứng | Explore mở TraceQL `{ resource.service.name = "keycloak" && name = "SELECT …PersistentUserSessionEntity" }`, cửa sổ 20:45:04–20:55:04 UTC; có trace keycloak lúc 20:54:27–28 UTC (ảnh 13) |
| Menu nút keycloak | hạng, vùng, bằng chứng, mã lớp `tu_sinh (tầng 1)`, điểm s, khóa; liên kết ① và ↗ (ảnh 15) |
| Lớp thao tác keycloak | request/giây và p90 theo route có dữ liệu (`/realms/{realm}/…`); lỗi 5xx: không có chuỗi (ảnh 14) |

**Đã sửa sau khi xem ca thật** (bản 4, đã triển khai lên `exp-obs` lúc 21:13 UTC, xem `thay-doi.md`):
1. Menu nút: dòng *Bằng chứng* liệt kê đủ tên thao tác SQL dài (tên lớp Java đầy đủ), menu rộng tràn khung. Nay: tối đa 3 kênh rồi "… (+n, xem bảng bằng chứng)"; với kênh thao tác bỏ tiền tố gói (`org.keycloak.models.jpa.…`); cắt ở 48 ký tự. Bảng *Bằng chứng* vẫn giữ tên đầy đủ. Kiểm lại trên 2 mẫu T-061: "4 kênh: error ↑, latency-90 ↑, workload ↓, … (+1, xem bảng bằng chứng)".
2. Panel *Vì sao … bị coi là kéo theo* hiện "No data" khi chọn keycloak (nghi là nguồn). Nay ghi "Không có: M1 không coi thành phần này là bị kéo theo." Bảng *Bằng chứng* tương tự: "Không có: M1 không gắn cờ kênh nào của thành phần này."

**Ghi nhận, chưa sửa:**
- Hai bằng chứng của keycloak là span gọi DB (thao tác JPA), còn lớp thao tác chỉ vẽ chỉ số HTTP theo `http_route`. Vì vậy hai thao tác M1 gắn cờ không có biểu đồ riêng trong lớp thao tác; xem chúng qua liên kết Tempo của bằng chứng.
- Tin nhắn của phiên điều phối nêu cửa sổ 20:44:36–20:54:36Z; file `a5539fba.json` ghi `cua_so_nen` 20:45:04–20:50:04 và `cua_so_su_co` 20:50:04–20:55:04 UTC (mốc 20:50:04). Dashboard dùng đúng cửa sổ trong file. Nếu cửa sổ trong file sai thì phải sửa ở phía sinh file, không ở dashboard.
- (Đã xử lý ở mục 2b.) Trang phát lại lúc này chỉ đọc trường T-061 (`thanh_phan_tiem` = phần tử đầu tập chấp nhận).

## 2b. Sửa sau phản biện Codex (12/11/2026, bản 5)

Minh cho phép trong chat 12/11: Codex phản biện; chỉ sửa khi hai bên không còn bất đồng. Ba lượt: `tasks/T-062-dem-chang-1-4/REVIEW-G1.md`, `REVIEW-G1-2.md`, `REVIEW-G1-3.md`; phản hồi và phương án ở [`phan-hoi-g1.md`](phan-hoi-g1.md). Lượt 3 ghi “không còn bất đồng chặn” với F1′, F2′, F3, F4, F5.

| Điểm | Sai gì | Sửa |
|---|---|---|
| R1 (CHẶN phần đáp án phát lại) | Trang phát lại coi `thanh_phan_tiem` (phần tử đầu tập chấp nhận) là “thành phần bị tiêm”, ghi “không phải” cho đầu kia của cạnh. Ca thật `f728fce2`: root `api-gateway → booking-service (http)`, tập `[api-gateway, booking-service]`, hạng 4 và 1; bản cũ chỉ hiện api-gateway #4 | F1′ `chi-muc-phat-lai.py`: thêm `dap_an_root`, `dap_an_tap`, `m1_trong_tap`, `hang_tot_nhat_e2(_hien_thi)`, giữ trường cũ. F2′ dashboard: cột root/tập/M1 xếp từng thành phần/hạng tốt nhất (theo e2); ◆ trên **mọi** nút thuộc tập; menu “thuộc tập chấp nhận mức nút của root …” / “ngoài tập chấp nhận”; dự phòng T-061 và chỉ mục cũ |
| R2 | Mô tả đồ thị ghi cứng “10 thành phần” không cạnh (T-062: 9) | F3: bỏ số, dẫn tới dòng Độ phủ |
| N2 | “Có hạng 17/17” trong khi không hiện hạng của nhóm bình thường | F4: “M1 trả hạng / quan sát”, “M1 trả hạng cho … (kể cả nhóm bình thường xếp chung hạng)” |
| R3 | Phương án đầu chưa tính chỉ mục đã sinh và manifest | F5: sinh lại chỉ mục mẫu; phiên điều phối sinh lại chỉ mục thật; G1 không sửa manifest, ghi file đổi + hash ở `thay-doi.md` |

**Kiểm trên bản thử** (Grafana 13.3.0 laptop; Infinity đọc một thư mục phục vụ cục bộ gồm bản sao 9 kết quả và 9 bản phát lại thật, mẫu T-061, một bản giả lập ghi rõ GIẢ LẬP; Prometheus/Loki/Tempo qua đường hầm):
- `f728fce2`: ◆ api-gateway (#4 bị kéo theo) và ◆ booking-service (#1 nghi là nguồn); hạng tốt nhất #1 (theo e2) (ảnh 16, 17).
- `1ad3afeb`: root `event-service → event_db (data)`; ◆ event-service (#1) và ◆ event_db (bình thường; “M1 xếp hạng #4, nhóm 14 thành phần”) (ảnh 18).
- Ca không tiêm (`e8661e0a`, `a5539fba`…): tập rỗng, không nút nào có ◆, menu “không có tập chấp nhận (không tiêm lỗi)”.
- Mẫu T-061 (`f4a8c021`, không có khóa mới): ◆ event-service “thiếu dữ liệu, không có hạng”; hạng tốt nhất “— (file không có trường này)”.
- Dashboard mới + chỉ mục cũ: cột ghi “api-gateway (chỉ mục cũ)”, “chỉ mục cũ: chưa có tập”, không vỡ.
- Trang chính: mọi truy vấn trên `f728fce2` và mẫu chạy; JSON trang chính không chứa `phat_lai`, `tap_chap_nhan`, `thanh_phan_tiem`.

**Triển khai:** phiên điều phối sinh lại và đẩy chỉ mục phát lại thật lúc 01:52 UTC; Codex lượt 4 (`REVIEW-G1-4.md`) xác nhận bản 5 trong repo; G1 đẩy bản 5 lên `exp-obs` lúc 02:01 UTC (hash khớp repo, `thay-doi.md`).

## 2c. Sửa sau lượt kiểm Grafana thật (bản 6, triển khai 02:20 UTC ngày 12/11)

Lượt Codex kiểm Grafana `exp-obs` thật trên bản 4 (phiên điều phối; `results/T-062/codex/G1-that-ketqua.md`) và Codex lượt 5 (`tasks/T-062-dem-chang-1-4/REVIEW-G1-5.md`). Hai bên thống nhất F6, F8; F7 lấy nguyên phương án của Codex.

| Điểm | Sai gì | Sửa |
|---|---|---|
| G-1 / F6 | 47/47 liên kết bảng *Bằng chứng* mã hóa hai lần (`panes=%257B…`), Explore "Could not parse Explore URL". Liên kết menu nút không bị | `${__data.fields.url:raw}`. Bản thử: bấm liên kết Tempo (`e8661e0a`) và Prometheus (trang phát lại, `a89954d1`) → Explore đúng truy vấn và cửa sổ, Tempo có trace (ảnh 19) |
| G-2 / F7 | Panel 5xx (5 ca) và log có bộ lọc (7 ca) "No data"; truy vấn trả rỗng, không lỗi | Mô tả panel có điều kiện: "Nếu truy vấn thành công nhưng không trả dữ liệu: chưa có chuỗi metric HTTP server 5xx / dòng log khớp … Không suy ra service không có lỗi." Chữ "No data" vẫn còn; không đổi truy vấn. Vì sao rỗng (không có bản ghi, thiếu thu nhận hay điều kiện nhãn) chưa phân xử, ngoài G1 |
| G-3 / F8 | Trang chính có chữ "đáp án" ở liên kết sang trang phát lại | Liên kết "Trang phát lại (chỉ mở khi đã chấm xong cả đợt)"; mô tả "Trang này chỉ hiện dự đoán của M1."; bộ sinh chặn chữ "đáp án" và `tap_chap_nhan` ở trang chính |

**Chưa kiểm:** bấm liên kết bảng bằng chứng trên chính Grafana `exp-obs` đã đăng nhập (bản 6). Bản thử dùng cùng phiên bản Grafana/Infinity và cùng file.

**Trang chính không bao giờ đọc đáp án:** chỉ đọc `rca-ket-qua/<mã>.json` và `rca-ket-qua/chi-muc/…`. Bộ sinh dashboard dừng nếu JSON trang chính có `phat_lai.`, `.phat-lai.json`, `danh-sach-phat-lai`, `thanh_phan_tiem`. `chi-muc-chinh.py` dừng nếu gặp file có khối `phat_lai`.

## 3. Chưa làm

- Lớp thao tác **từ M1** (`don_vi_phan_vi`, hướng 2 xếp hạng thao tác): định dạng 0.2 không mang dữ liệu này (T-061 §6); panel thao tác hiện là dữ liệu sống của Prometheus/Tempo/Loki, không phải đầu ra M1. Cạnh cha–con giữa *thao tác* chỉ thấy trong từng trace, chưa có đồ thị thao tác.
- Tô vùng nghi ngờ trên đồ thị (cách 1 hay cách 2 là quyết định của Minh, T-061 §6): hiện chỉ ghi chữ ở bản ghi sự cố, bảng hạng và menu nút.
- Ô giải thích LLM (G4): chưa có nguồn (`giai_thich = null`).
- Chú thích (annotation) mốc sự cố trên biểu đồ thời gian.

## 4. Định dạng chỉ mục

Xem [`dinh-dang-chi-muc.md`](dinh-dang-chi-muc.md). Tóm tắt: trang chính đọc `rca-ket-qua/<mã>.json` (0.2) + `rca-ket-qua/chi-muc/danh-sach-su-co.json` **đúng định dạng T-061**, sinh bằng [`chi-muc-chinh.py`](chi-muc-chinh.py) (trùng từng byte với chỉ mục T-061 trên 2 mẫu). Trang phát lại đọc `rca-ket-qua/phat-lai/<mã>.phat-lai.json` + `phat-lai/chi-muc/danh-sach-phat-lai.json`, sinh bằng [`chi-muc-phat-lai.py`](chi-muc-phat-lai.py). Thả file vào là hiện; không cần khởi động lại Grafana. Đã để ghi chú cho phiên điều phối trong thư mục ghi chú chung.

## 5. Giới hạn đã biết

1. **Chưa xem trên chính `exp-obs`** (cần đăng nhập). Bản thử: Grafana 13.3.0 Windows + Infinity 4.1.6 (cùng phiên bản `exp-obs`; `exp-obs` chạy bản arm64 của cùng plugin), cùng file dashboard, dữ liệu đọc qua đường hầm từ `public/rca` và Prometheus/Loki/Tempo của `exp-obs`. Trên `exp-obs`: log "finished to provision dashboards", không lỗi.
2. Dữ liệu đã thử: 2 ca mẫu T-061 và 1 ca thật T-062 (`a5539fba`, chỉ có nghi nguồn, không có kéo theo hay thiếu dữ liệu). Bản ghi `ERROR` kiểm bằng file dựng tay theo `chuyen-doi.py::ban_ghi_loi` (mức truy vấn, chưa xem hình). Chưa thử `NO_EVIDENCE`, đồng hạng giữa các nút nghi nguồn, cạnh có bằng chứng, nhiều sự cố.
3. Nhãn và màu dẫn xuất trong dashboard bằng JSONata (parser `backend` của Infinity, biểu thức bắt đầu bằng `$$.(`), từ `vai_tro`, `hang`, `so_dong_hang`; màu lấy `hien_thi.mau`. Không dùng `hien_thi.nhan_trong` (có chữ "không cờ"). Định dạng 0.2 không đổi.
4. Bố cục nút cố định: một tầng có quá nhiều nút thì đồ thị rộng ra; dùng nút +/− của panel. Thứ tự dòng trong menu nút do Grafana sắp, không theo thứ tự khai báo.
5. Ánh xạ tên thực thể M1 → `service_name` của telemetry theo adapter T-058 (`config-discovery` → `discovery-server`, `cache` → `redis`, `broker` → `rabbitmq`, `postgresql-shared-instance` → `postgres`, `mongodb-instance` → `user-db`). Thành phần DB (`booking_db`…) không có service nên liên kết Tempo/Loki và panel thao tác của chúng trống.
6. Liên kết Prometheus của bằng chứng bọc truy vấn nguyên văn: `(<truy vấn>) and on(<nhãn>) label_replace(vector(1), "<nhãn>", "<giá trị>", "", "")` để chỉ giữ chuỗi của thành phần. Liên kết Tempo là tìm kiếm span cùng service và tên thao tác, không phải trace M1 chọn (M1 không xuất trace).
7. `public/rca` của Grafana không cần đăng nhập: ai vào được `10.0.0.215:3000` (trong VCN) tải được file, kể cả `phat-lai/`. Chỉ đẩy phát lại sau khi băm cả đợt.
8. Lúc kiểm (khoảng 21:05 UTC ngày 11/11), chỉ mục thư mục chính đã là của T-062 (phiên điều phối ghi bằng `results/T-062/e2.py`); hai mẫu T-061 xem ở "Mẫu T-061".
9. Đổi ca bằng ô *Sự cố* không đổi khung giờ (giới hạn của Grafana); dùng bảng danh sách hoặc liên kết ⏱.
10. Ảnh chụp 800 px (giới hạn của khung trình duyệt trong app), chụp trên bản thử. Ở bề rộng này menu nút ở giữa đồ thị bị cắt mép trái (ảnh 15); trên màn hình thường thì vừa.

## 6. File

- [`dung-dashboard.py`](dung-dashboard.py) — sinh `grafana/dashboards/rca-g2-chinh.json`, `rca-g2-phat-lai.json`, `provider.yaml`.
- [`kiem-truy-van.py`](kiem-truy-van.py) — chạy mọi truy vấn Infinity của một dashboard qua `/api/ds/query` của một Grafana thử.
- [`chi-muc-chinh.py`](chi-muc-chinh.py), [`chi-muc-phat-lai.py`](chi-muc-phat-lai.py) — sinh chỉ mục.
- [`rca-ket-qua-mau/mau/`](rca-ket-qua-mau/mau/) — bản sao mẫu T-061 + chỉ mục phát lại, đã chép lên `exp-obs:/opt/flash-ticket-obs/rca-ket-qua/mau/`.
- [`thay-doi.md`](thay-doi.md) — mọi thay đổi trên `exp-obs` (giờ UTC, hash) và cách hoàn tác.
- [`anh/`](anh/) — 19 ảnh chụp: 01–10 trên 2 mẫu T-061, 11–15 trên ca thật `a5539fba`, 19 liên kết bảng bằng chứng bản 6; 16–18 trang phát lại bản 5 (bản thử).
- [`phan-hoi-g1.md`](phan-hoi-g1.md), `prompt-phan-bien-g1*.md` — tự soát, phản hồi phản biện, prompt cho Codex.

Dựng lại: `cd results/T-062/giao-dien && py -3 -B dung-dashboard.py`, chép `grafana/dashboards/*` vào `exp-obs:/opt/flash-ticket-obs/pinned/provisioning/dashboards/`, `docker restart flash-ticket-obs-grafana`.
