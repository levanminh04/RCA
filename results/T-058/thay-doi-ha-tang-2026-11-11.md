# T-058 — Các thay đổi hạ tầng so với SPEC và PLAN (tính tới 11/11/2026)

File này ghi lại những gì đã đổi sau khi SPEC T-058 được duyệt ngày 10/11/2026. Nó không thay SPEC. Phần nào lệch SPEC thì cần Minh duyệt đính chính trước khi làm (Luật 0); trạng thái duyệt ghi ở mục 6.

## 1. Máy

| Vai trò | SPEC, PLAN (10/11) | Hiện tại (11/11) | Nguồn |
|---|---|---|---|
| `exp-app` | AWS `3.27.110.61`, x86, đổi lên `m7i-flex.large` | **Oracle** `129.221.208.47`, `VM.Standard.A1.Flex` (**ARM**, `aarch64`), 2 OCPU, 11 GB RAM, đĩa 50 GB, Ubuntu 24.04.5, vùng `ap-singapore-1`, IP nội bộ `10.0.0.158` | SSH và metadata, 11/11 |
| `exp-obs` | AWS, chưa tạo | **Oracle** `213.35.116.128`, A1 ARM, 2 OCPU, 11 GB RAM, đĩa 150 GB, Ubuntu 24.04.5, cùng subnet, IP nội bộ `10.0.0.215` | SSH và metadata, 11/11 |
| Máy AWS | `exp-app` | `3.24.8.49` (Elastic IP), `m7i-flex.large`, 7775 MiB, x86. Minh nói không dùng AWS nữa; máy còn tồn tại, chưa có quyết định xóa | SSH, 11/11 |
| Máy Oracle thử đầu tiên | — | `161.118.228.225`: không còn vào được; file khóa cũ không còn | SSH, 11/11 |
| Máy 84 | Chỉ đọc | Không đổi | — |

Khóa SSH: `D:\RCA-ext\keys\exp-app\` và `D:\RCA-ext\keys\exp-obs\`, ngoài repo. Đăng nhập `ubuntu`.

## 2. Số đo đã có

- **Độ trễ kết nối TCP (trung vị, 8 lần):** `exp-app` ↔ `exp-obs` Oracle 1 ms (cả IP nội bộ lẫn IP công khai); laptop → Oracle Singapore 41 ms; laptop → AWS Sydney 248–270 ms; AWS Sydney ↔ Oracle Singapore 203 ms (120 lần: 0 lần lỗi, p95 221 ms).
- **M1 trên ARM:** 104 bản ghi của bộ `tat_dinh.py` (T-044) giống từng bit giữa x86 Linux và ARM Linux; 374/374 phép kiểm T-044 qua trên cả hai. Laptop Windows lệch 56/104 bản ghi so với Linux, sai lệch tương đối lớn nhất 2,3e-15, không có trường rời rạc nào khác. Chỉ là dữ liệu fixture, không phải dữ liệu FlashTicket.
- **Image:** 3 image FlashTicket đã kiểm (`booking-service`, `api-gateway`, `keycloak`) chỉ có `linux/amd64`. Image nền Temurin (digest đang ghim trong Dockerfile) và Keycloak 26.8.0 có `linux/arm64`. Collector 0.165.0, Prometheus v3.16.0, Loki 3.7.9, Tempo 3.1.1, Grafana 13.3.0, otel-lgtm 0.40.0, k6 2.3.0, Toxiproxy 2.13.0, Pumba 1.6.0, PostgreSQL 16.15, MongoDB 7.0, Redis 7.4.11, RabbitMQ 4.3.6 đều có `linux/arm64`.
- **Chi phí Oracle (bảng giá cập nhật 02/11/2026):** A1 miễn phí 3000 OCPU-giờ và 18.000 GB-giờ mỗi tháng cho tenancy trả phí; hai máy hiện tại dùng 2920 OCPU-giờ và 16.060 GB-giờ nếu chạy 24/24. Đĩa 50 + 150 = 200 GB, bằng hạn mức miễn phí. Minh cần kiểm trong Console xem còn boot volume của máy cũ không.

## 3. Quyết định của Minh (lời trong chat)

- "tôi quyết định sử dụng oracle, không dùng aws nữa" (điều kiện: SSH được; đã SSH được cả hai máy).
- "chọn cách B": sửa quy trình build của repo FlashTicket để image có cả bản ARM.
- Chốt demo phần phát hiện và chẩn đoán trên `exp-app` cộng `exp-obs`; chọn P-E (đã ghi DECISIONS 10/11).

## 4. Hệ quả kỹ thuật

1. **FlashTicket chạy trên ARM, máy 84 chạy x86.** Hiệu năng hai bên khác nhau (chưa đo). Báo cáo phải khai rõ.
2. **Image.** Digest hiện có của 84 không chạy được trên `exp-app`. Cần image `arm64` dựng từ cùng commit. Mỗi image của 84 có nhãn `org.opencontainers.image.revision` ghi commit đã build.
3. **Cách B cần sửa repo FlashTicket** (`.github/workflows/_deploy-service.yml`: thêm `linux/arm64` và bước QEMU). SPEC T-058 đang ghi "Không sửa repo FlashTicket"; AGENTS §12 ghi repo đó chỉ đọc. Nhánh `main` đang bật bảo vệ (API công khai trả `protected=true`); laptop không có `gh` CLI. Vì vậy agent không tự merge và không tự bấm chạy CD được.
4. **Repo FlashTicket đã có commit mới** sau bản laptop đang giữ (`1d40c97`): CD chạy ngày 10/11 lúc 15:01Z (`9eea593a`) và 19:04Z (`22067803`). `results/T-058/manifest-digest.json` (đọc 08:57Z ngày 10/11) đã cũ; phải đọc lại trước khi dùng.
5. **Collector hai tầng** (đã sửa PLAN và TECHSTACK ngày 10/11): Collector tại chỗ trên `exp-app`, Collector trung tâm trên `exp-obs`.
6. **Mạng Oracle.** Giữa hai máy mới chỉ kiểm cổng 22. Image Ubuntu của Oracle chặn mọi cổng khác bằng `iptables` (đã kiểm trên máy thử đầu tiên); Security List của mạng cũng phải cho phép.
7. **PLAN lỗi thời ở các chỗ:** máy AWS, IP, "9 ứng dụng, 14 container" (thực tế 8 ứng dụng, bỏ frontend vì gắn cứng địa chỉ 84), §9.1 Q1 và Q3, ngân sách tiền AWS.

## 5. Việc đã làm trên các máy (ngoài lệnh đọc)

- **AWS `3.24.8.49`:** `apt-get update`; cài `python3-venv`, `python3-pip`; cài `uv` ở `~/uvenv`; Python 3.12 của `uv`; thư mục `~/x86-check` và file tạm. Dùng để đối chứng M1 trên x86 Linux.
- **Oracle thử đầu tiên `161.118.228.225`:** cài `python3-venv`, `python3-pip`; thư mục `~/arm-check`. Máy này nay không vào được.
- **Oracle `exp-app`, `exp-obs`:** chưa cài gì.

## 6. Trạng thái duyệt

- File này và mục LOG phiên 2: ghi theo lời Minh "ghi file về các thông tin đã thay đổi cho đến hiện tại" (11/11), trong phạm vi ghi của SPEC.
- **Chưa duyệt, đã trình trong chat 11/11:** đính chính SPEC T-058 (hạ tầng Oracle ARM, nguồn image, quyền sửa một file workflow trên nhánh riêng của repo FlashTicket, nguồn env và dữ liệu); sửa PLAN theo mục 4.7; dòng DECISIONS cho mục 3.
