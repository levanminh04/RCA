# Máy chủ liên quan và cách vào bằng MobaXterm (cập nhật 11/11/2026)

Khóa nằm ngoài repo, ở `D:\RCA-ext\keys\`. Không chép khóa vào repo, không gửi khóa qua chat.

## 1. Danh sách máy

| Tên | IP công khai | IP nội bộ | Nhà cung cấp, vùng | Cấu hình | Tài khoản | File khóa | Vai trò | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| `exp-app` | `129.221.208.47` | `10.0.0.158` | Oracle, Singapore | ARM, 2 OCPU, 11 GB, đĩa 50 GB | `ubuntu` | `exp-app\ssh-key-2026-11-10 (1).key` | FlashTicket thực nghiệm: 8 service, 4 hạ tầng, agent, Collector tại chỗ | Đang chạy |
| `exp-obs` | `213.35.116.128` | `10.0.0.215` | Oracle, Singapore | ARM, 2 OCPU, 11 GB, đĩa 150 GB | `ubuntu` | `exp-obs\ssh-key-2026-11-10.key` | Kho quan sát (Collector trung tâm, Prometheus, Loki, Tempo, Grafana), M1 | Đang chạy |
| Máy 84 | `52.64.237.84` | — | AWS, Sydney | x86, 2 vCPU, 3,7 GiB | `ubuntu` | `FlashTicket-Control-Diagnosis.ppk` | Demo và CD của nhóm. Chỉ đọc | Đang chạy (của nhóm) |
| AWS `exp-app` cũ | `3.24.8.49` (Elastic IP) | `172.31.2.212` | AWS, Sydney | x86, `m7i-flex.large`, 8 GiB | `ubuntu` | `Hahaa123.pem` | Không dùng nữa (Minh chọn Oracle) | **Vẫn chạy, đang tốn tín dụng AWS**; chờ Minh quyết Stop hoặc xóa |
| Oracle thử đầu tiên | `161.118.228.225` | — | Oracle, Singapore | ARM, 4 OCPU, 12 GB | `ubuntu` | không còn | Đã dùng để thử M1 trên ARM | Không còn vào được; kiểm trong Console và xóa boot volume nếu còn |

## 2. Vào máy bằng MobaXterm

1. Mở MobaXterm, bấm **Session** (góc trên trái), chọn **SSH**.
2. **Remote host:** IP công khai trong bảng trên.
3. Tích **Specify username**, gõ `ubuntu`. Port để 22.
4. Sang tab **Advanced SSH settings**, tích **Use private key**, bấm biểu tượng thư mục, chọn file khóa của đúng máy trong `D:\RCA-ext\keys\`.
5. Bấm **OK**. Lần đầu MobaXterm hỏi có tin máy này không, bấm **Accept**.
6. Đặt tên phiên (chuột phải vào phiên trong khung Sessions → Rename) là `exp-app`, `exp-obs` để lần sau bấm đúp là vào.

Kiểm: vào được dấu nhắc `ubuntu@...:~$`, gõ `docker ps` thấy danh sách container.

## 3. Xem Grafana và gọi gateway từ laptop (đường hầm SSH)

Các cổng web chỉ mở trong mạng nội bộ Oracle, không mở ra internet. Muốn xem từ laptop phải đi qua đường hầm SSH.

1. Trong MobaXterm bấm **Tunneling** (thanh công cụ) → **New SSH tunnel**.
2. Chọn **Local port forwarding**.
3. Điền như bảng dưới, mỗi dòng một đường hầm:

| Cổng trên laptop (Forwarded port) | SSH server | SSH login | Remote server | Remote port | Dùng để |
|---|---|---|---|---|---|
| 13000 | `213.35.116.128` | `ubuntu` | `10.0.0.215` | 3000 | Grafana |
| 18081 | `213.35.116.128` | `ubuntu` | `10.0.0.158` | 8081 | API gateway |

4. Bấm biểu tượng chìa khóa ở dòng đường hầm, chọn khóa `exp-obs\ssh-key-2026-11-10.key`.
5. Bấm nút **Start** (tam giác) ở từng dòng.
6. Mở trình duyệt: `http://127.0.0.1:13000` là Grafana; dashboard `http://127.0.0.1:13000/d/t058-flashticket/flashticket-t-058`. Gateway: `http://127.0.0.1:18081/api/v1/events`.

Mật khẩu Grafana sinh ngẫu nhiên trên máy, không ghi trong tài liệu. Xem bằng cách SSH vào `exp-obs` rồi gõ `sudo cat /opt/flash-ticket-obs/grafana.env`. Tài khoản là giá trị `GF_SECURITY_ADMIN_USER`.

Lưu ý về đăng nhập Keycloak: token chỉ hợp lệ khi lấy qua địa chỉ nội bộ `http://10.0.0.158:8080`, nên lấy token bằng lệnh chạy trên `exp-app` (`dem-2026-11-10/huong-dan-trien-khai.md` mục 9), không qua `localhost` của laptop.

Chưa thao tác thật trên giao diện MobaXterm; các đường hầm tương đương đã chạy bằng lệnh `ssh` (Codex, đêm 10/11) và trả HTTP 200.

## 4. Thay đổi trên `exp-app` sau lượt đêm (11/11, Claude)

| Service | Biến thêm vào `/opt/flash-ticket-app/env/<service>.env` | Tác dụng | Bản cũ |
|---|---|---|---|
| booking-service, api-gateway | `SPRING_AUTOCONFIGURE_EXCLUDE=org.springframework.boot.data.redis.autoconfigure.observation.LettuceObservationAutoConfiguration` | Có span Redis (`kiem-span-redis.md`) | `<file>.truoc-thu-redis-20261111` |
| event, booking, payment, ticket | `OTEL_INSTRUMENTATION_RABBITMQ_EXPERIMENTAL_SPAN_ATTRIBUTES=true` | Span RabbitMQ có vhost, cluster, tên lệnh (`kiem-rabbitmq-va-log.md`) | `<file>.truoc-thu-rabbit-20261111` |

Lệnh áp dụng cho một service (ví dụ booking), chạy trên `exp-app`:

```bash
cd /opt/flash-ticket-app/compose-exp
IMAGE=$(docker inspect flash-ticket-booking-service-booking-service-1 --format '{{.Config.Image}}') \
  docker compose -f booking-service.yml -p flash-ticket-booking-service up -d --force-recreate
```

`docker inspect ... --format '{{.Config.Image}}'`: lấy tên image container đang chạy, để tạo lại đúng image đó. `-f booking-service.yml`: dùng bản compose riêng của `exp-app`. `-p flash-ticket-booking-service`: tên dự án compose, giữ giống lúc tạo. `up -d --force-recreate`: tạo lại container (đọc lại file env) và chạy nền.

Kiểm: `curl -s http://127.0.0.1:8761/eureka/apps/BOOKING-SERVICE -H 'Accept: application/json'` thấy `"status":"UP"`.

**Bắt buộc sau mỗi lần tạo lại container (tạm thời, KP-19):** tạo lại container sinh ID mới, còn Collector tại chỗ đọc log theo đường dẫn có ID cũ. Không cập nhật thì log của service đó ngừng vào Loki, dù service vẫn chạy. Khởi động lại container (`docker restart`) giữ ID nên không cần bước này. Chạy trên `exp-app`:

```bash
cd /opt/flash-ticket-app/collector
cp -p config.json config.json.truoc-cap-nhat-$(date -u +%Y%m%dT%H%M)
python3 - <<'PY2'
import json, subprocess
p = '/opt/flash-ticket-app/collector/config.json'
c = json.load(open(p))
for k, v in c['receivers'].items():
    if k.startswith('filelog/'):
        svc = k.split('/', 1)[1]
        v['include'] = [subprocess.check_output(['docker', 'inspect', f'flash-ticket-{svc}-{svc}-1', '--format', '{{.LogPath}}'], text=True).strip()]
with open(p, 'r+') as f:
    f.seek(0); f.write(json.dumps(c, indent=2, ensure_ascii=False) + '\n'); f.truncate()
PY2
docker exec flash-ticket-collector /otelcol-contrib validate --config=/etc/otel/config.json && docker restart flash-ticket-collector
```

`docker inspect ... '{{.LogPath}}'`: lấy đường dẫn file log của container đang chạy. Ghi đè tại chỗ (`r+`, `truncate`) để giữ inode, vì file được gắn vào container Collector theo kiểu bind mount một file. `validate`: kiểm cấu hình trước khi khởi động lại. Log trong khoảng đứt được lấy bù, vì Collector đọc file mới từ đầu.

Kiểm: `docker logs --since 1m flash-ticket-collector 2>&1 | grep 'Started watching file'` thấy file mới; trên `exp-obs`, Loki có bản ghi mới của service đó. Cách sửa lâu dài đang chờ Minh duyệt (KP-19 bổ sung).
