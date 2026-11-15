# Dựng môi trường Oracle T-058

Ngày chạy: 10/11/2026 UTC, đêm 11/11 theo giờ Việt Nam. Đây là môi trường kiểm khả thi RCA. Không phải kết quả đánh giá M1.

Các mốc UTC trong lệnh đo/tải là lịch sử của lượt này. Không chạy lại script lập lịch với giờ đã qua. Một lượt mới cần giờ tương lai, mã ca và thư mục mới; giữ gói cũ để đối chiếu. Những lệnh kiểm chỉ đọc có thể dùng với môi trường đang chạy.

## 1. SSH vào hai máy

Trong MobaXterm, chọn **Session → SSH**. Điền Remote host `129.221.208.47` cho `exp-app`, hoặc `213.35.116.128` cho `exp-obs`. Tích **Specify username**, nhập `ubuntu`. Trong **Advanced SSH settings → Use private key**, chọn khóa tương ứng trong `D:\RCA-ext\keys\exp-app` hoặc `exp-obs`. Các thao tác giao diện này là hướng dẫn tương đương; lượt đêm dùng Git SSH, chưa thao tác MobaXterm.

Lệnh đã dùng trên laptop (PowerShell):

```powershell
. ./out/remote.ps1
Invoke-Oracle app 'date -u'
Invoke-Oracle obs 'date -u'
```

`.` nạp các hàm trong file vào phiên PowerShell. `Invoke-Oracle` chọn đúng máy và khóa; `app` và `obs` là tên rút gọn. Hàm dùng `C:/Program Files/Git/usr/bin/ssh.exe`. `BatchMode=yes` tránh chờ nhập mật khẩu. `ConnectTimeout=15` giới hạn thời gian kết nối 15 giây. `StrictHostKeyChecking=accept-new` chỉ nhận khóa host mới; khóa đã biết nhưng thay đổi sẽ bị từ chối. `UserKnownHostsFile` lưu khóa host trong `out/known_hosts`, không ghi vào thư mục SSH cá nhân. Lệnh từ xa được mã hóa Base64 rồi chuyển vào Bash để giữ nguyên dấu nháy khi đi qua PowerShell.

Kiểm: gõ hai lệnh trên thấy ngày giờ UTC của từng máy.

## 2. Cài Docker, Java và mở mạng nội bộ

Script đã chạy thành công trên cả hai máy: `/home/ubuntu/t058/bootstrap.sh`. Bản bàn giao: `out/bootstrap.sh`.

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl git tmux python3-venv chrony iptables-persistent
curl -fsSL https://get.docker.com -o /home/ubuntu/t058/get-docker.sh
sudo sh /home/ubuntu/t058/get-docker.sh
sudo usermod -aG docker ubuntu
sudo iptables -I INPUT 1 -s 10.0.0.0/24 -j ACCEPT
sudo netfilter-persistent save
sudo systemctl enable docker chrony netfilter-persistent
docker version
docker compose version
docker run --rm hello-world
```

`sudo` chạy với quyền quản trị. `apt-get update` cập nhật danh sách gói; `upgrade -y` cập nhật gói đã cài, tự trả lời đồng ý. `install -y` cài các gói được liệt kê. `chrony` đồng bộ giờ; `iptables-persistent` giữ luật firewall sau khi khởi động lại; `python3-venv` dùng cho môi trường Python riêng. `curl -fsSL` tải file, báo lỗi HTTP và theo chuyển hướng; `-o` chọn đường dẫn lưu. `sh` chạy bộ cài Docker chính thức.

`usermod -aG docker ubuntu` thêm tài khoản `ubuntu` vào nhóm Docker. `-a` là thêm vào nhóm, `-G` chọn nhóm bổ sung. Đăng nhập lại để nhóm có hiệu lực. `iptables -I INPUT 1` chèn đầu chuỗi nhận gói; `-s` chỉ nguồn trong subnet nội bộ; `-j ACCEPT` cho phép các gói đó. Script thực tế kiểm bằng `iptables -C` trước để tránh thêm trùng. `netfilter-persistent save` lưu luật hiện tại. `systemctl enable` bật dịch vụ sau mỗi lần khởi động máy. `docker run --rm` chạy container và tự xóa container khi kết thúc.

Riêng `exp-app` còn chạy:

```bash
sudo apt-get install -y openjdk-21-jdk-headless maven
```

JDK 21 dùng để build Java. Maven hệ thống dùng cho Keycloak SPI; các service Spring dùng Maven wrapper của chính service.

Kiểm: gõ `docker compose version` thấy Compose 5.7.0; gõ `docker run --rm hello-world` thấy thông báo thành công. Docker Engine đã cài là 29.9.3. `chronyc tracking` cho biết đồng hồ đồng bộ. Không tạo swap. Việc nạp lại luật sau reboot chưa được thử bằng reboot.

## 3. Build 8 image ARM theo commit riêng

Script đã chạy thành công: `/home/ubuntu/t058/build-arm.sh`. Nó đọc `/home/ubuntu/t058/revisions.json`, clone công khai vào `/opt/flash-ticket-src`, rồi tạo một worktree riêng cho mỗi service dưới `/opt/flash-ticket-build`.

Các lệnh clone và checkout đã chạy bên trong script:

```bash
GIT_TERMINAL_PROMPT=0 git -c credential.helper= clone https://github.com/levanminh04/flash-ticket-platform.git /opt/flash-ticket-src
git -C /opt/flash-ticket-src checkout --detach 220678030517c46a1db815a44779fe1075cc8b46
git -C /opt/flash-ticket-src worktree add --detach /opt/flash-ticket-build/discovery-server 5c6d1c13ffad9110c9827f2cf0ced98fb9919258
```

`GIT_TERMINAL_PROMPT=0` tắt câu hỏi đăng nhập của Git. `-c credential.helper=` tắt credential helper cho đúng lệnh clone này trên Oracle. `clone` tải repo công khai vào đường dẫn cuối. `-C` chọn thư mục Git để chạy lệnh. `checkout --detach` đặt đúng commit mà không tạo nhánh. `worktree add --detach` tạo thư mục làm việc riêng tại đường dẫn được chỉ định, dùng commit cuối lệnh. Script lặp cùng cách này cho từng service trong revisions. Không có checkout hoặc clone ghi vào repo laptop.

Trong mỗi worktree của 7 service Spring, lệnh đã chạy là:

```bash
bash ./mvnw -B -ntp -DskipTests package
```

`bash ./mvnw` dùng Maven wrapper của service. `-B` chạy không tương tác. `-ntp` bỏ tiến độ tải từng gói. `-DskipTests` **bỏ chạy test**; vẫn biên dịch phần cần thiết. `package` tạo JAR. Đây là điểm khác CI của nhóm, vốn chạy kiểm tra đầy đủ. Không coi build này là bằng chứng test đã qua.

Trong script, `docker build` dùng Dockerfile trong thư mục service. `--label` ghi commit nguồn vào image. `-t` đặt tên và tag. Dấu `.` là thư mục nguồn build hiện tại. Script lấy commit đầy đủ từ revisions, rồi đặt tag dạng `ft-local/<service>:arm64-<8 ký tự đầu commit>`. Image ID nằm trong `out/manifest-digest.json`; đó là ID image cục bộ, không phải digest của một image đã push lên registry.

Riêng `services/keycloak-spi` đã chạy:

```bash
mvn -B -ntp clean verify
```

`clean` xóa đầu ra build cũ của worktree trên Oracle. `verify` chạy cả test và kiểm tra của module Keycloak trước khi Dockerfile đóng gói SPI. Frontend không được build.

Kiểm: manifest có 8 mục `architecture=arm64`. Nhãn revision khớp từng commit trong `inputs/revisions.json`.

## 4. Khởi tạo env và dữ liệu mới

Script `out/prepare-app.py` đã chạy trên `exp-app`. Nó tạo env mới từ `.env.example` ở gốc và ở đúng revision từng service; dùng bảng cấu hình deploy của nhóm; sinh bí mật bằng `openssl rand`. Không dùng dữ liệu hay env từ máy 84.

Các file env nằm ở `/opt/flash-ticket-app/env/<service>.env`; `.env` hạ tầng nằm ở `/opt/flash-ticket-src/.env` và `/opt/flash-ticket-infra/.env`. File env có mode `600`. Với các biến bí mật: **giá trị sinh ngẫu nhiên trên máy, xem file tương ứng trên `exp-app`**. Tài liệu này chỉ liệt kê tên biến ở phụ lục.

Key-ring mới nằm tại `/opt/flash-ticket-app/secrets/ticket-qr/key-ring.json`. Định dạng là đối tượng `keys`, khóa `v1` mã hóa Base64 chuẩn của 32 byte ngẫu nhiên. Owner `10001:10001`, mode `0440`. Không chép nội dung vào tài liệu hay log.

Realm import là bản riêng ở `/opt/flash-ticket-infra/keycloak/keycloak/import`. Mật khẩu người dùng thử đã đổi; xem `/opt/flash-ticket-app/env/test-users.json` trực tiếp trên `exp-app`. Client secret được sinh mới, lưu ở env và `/opt/flash-ticket-app/env/client-secrets.json`. Không dùng mật khẩu mẫu lịch sử trong repo.

**Địa chỉ issuer:** `KC_HOSTNAME=http://10.0.0.158:8080`; `KEYCLOAK_ISSUER_URI=http://10.0.0.158:8080/realms/flash-ticket`. Đây là địa chỉ nội bộ mà các service gọi được. Token phải mang issuer này. Khi dùng SSH tunnel từ laptop, hãy lấy token bằng script chạy trên `exp-app` gọi đúng địa chỉ nội bộ; không đổi issuer thành `localhost` của laptop. URL trong trình duyệt và claim issuer là hai phần cần phân biệt khi dùng tunnel.

Script `/home/ubuntu/t058/start-infra.sh` đã chạy:

```bash
cd /opt/flash-ticket-infra
docker compose --env-file .env -f deploy/docker-compose.postgresql.yml -f deploy/docker-compose.redis.yml -f deploy/docker-compose.rabbitmq.yml -f deploy/mongodb/compose.yaml -p flash-ticket-infra up -d --wait --wait-timeout 300
```

`cd` chọn thư mục hạ tầng. `--env-file` chọn bộ biến mới. Mỗi `-f` thêm một file compose. `-p` gom container vào project `flash-ticket-infra`. `up -d` tạo và chạy nền. `--wait` đợi healthcheck; `--wait-timeout 300` chờ tối đa 300 giây. PostgreSQL dùng script `00-business-databases.sh`, DDL chuẩn và script tiền tố bảng của repo. MongoDB dùng script init chuẩn, với image `mongo:7.0` theo yêu cầu lượt đêm. Bản compose riêng đổi các cổng Redis và RabbitMQ sang loopback; file repo giữ nguyên.

Trước lần init đầu, bản triển khai cần hai sửa đã kiểm: script `00-business-databases.sh` có quyền `755`; hai file reader event/payment được tạo bằng mẫu grant đọc của reader booking/ticket vì repo chưa có chúng. Bản `out/prepare-app.py` bàn giao đã gồm hai phần này. Lượt đầu đã gặp lỗi, được resume có guard bằng `out/repair-postgres.py`, giữ nguyên dữ liệu Keycloak. Sau đó `out/verify-fresh-postgres.sh` kiểm trên volume mới riêng: tạo đủ bốn DB, số bảng lần lượt 12/15/13/7. Log kiểm nằm trên `exp-app`. Chưa dựng lại toàn bộ hai VM từ số 0 bằng bản script cuối.

Kiểm: bốn container PostgreSQL, MongoDB, Redis và RabbitMQ đều `healthy`; cần kiểm thêm bốn DB nghiệp vụ và đăng nhập TCP, vì health PostgreSQL một mình chưa chứng minh script init đã chạy hết. Không dùng `down -v` để làm lại trên volume đã có dữ liệu.

Không chạy ngrok. URL VNPay là URL giả. Luồng đặt vé chỉ kiểm tới ranh giới thanh toán; chưa kiểm thanh toán hoặc gửi email thật.

## 5. Kho quan sát thử

`/home/ubuntu/t058/deploy-lgtm.sh` đã chạy thành công trên `exp-obs`. Compose nằm ở `/opt/flash-ticket-obs/compose-lgtm.yml`. Dữ liệu dùng Docker volume `flash-ticket-obs_lgtm-data`. Mật khẩu Grafana sinh mới, xem `/opt/flash-ticket-obs/grafana.env` trực tiếp trên `exp-obs`.

```bash
docker compose -f /opt/flash-ticket-obs/compose-lgtm.yml -p flash-ticket-obs up -d
curl -fsS http://10.0.0.215:3000/api/health
```

`-f` chọn compose; `-p` chọn project; `up -d` chạy nền. Lệnh `curl` gọi API health. Grafana nghe IP nội bộ `10.0.0.215:3000`; OTLP nghe nội bộ ở 4317/4318. API của Prometheus, Loki, Tempo chỉ publish loopback. Image là `grafana/otel-lgtm:0.40.0`, dùng cho smoke/kiểm khả thi; chưa phải kho chấm chính thức.

Kiểm: API trả `database=ok`, Grafana `13.3.0`; container `flash-ticket-lgtm` báo `healthy`.

## 6. Bật service và kiểm API

Các compose gốc của nhóm được chép vào `/opt/flash-ticket-app/compose`. Script `/home/ubuntu/t058/start-app.py` đã bật discovery, Keycloak và các service. `IMAGE` lấy từ build manifest; project có tên `flash-ticket-<service>`. Payment dùng bản sao bỏ service ngrok. Keycloak publish `10.0.0.158:8080`. Gateway hiện nghe riêng `10.0.0.158:8081`, để máy quan sát phát tải qua subnet nội bộ. Các Spring service còn lại nghe loopback.

Ví dụ service discovery đã được bật bằng cùng file compose và biến image này:

```bash
IMAGE=ft-local/discovery-server:arm64-5c6d1c13 docker compose -f /opt/flash-ticket-app/compose/discovery-server.yml -p flash-ticket-discovery-server up -d
```

`IMAGE=...` cấp tên image cho đúng tiến trình Compose. `-f` chọn compose của nhóm; `-p` chọn project riêng của service. `up -d` tạo và chạy nền. Sau khi gắn agent, cùng service dùng file ở `compose-exp` để có mount jar. Khi làm lại, chọn image của đúng service từ manifest; không dùng một commit chung cho cả tám service.

`out/seed-minimal.py` đã tạo một sự kiện synthetic đang mở bán, hai loại vé và snapshot tối thiểu trong các DB, đồng thời dùng seed MongoDB chuẩn để nối ba subject của realm với hồ sơ ứng dụng. SQL thực tế và ID nằm trong `out/seed-minimal.sql` và `out/seed-fixture.json`. Đây là khởi tạo trực tiếp; chưa kiểm luồng tạo/duyệt/publish event bằng API qua seed này.

Lệnh đã chạy thành công trên `exp-app`:

```bash
python3 /home/ubuntu/t058/auth.py
python3 /home/ubuntu/t058/smoke-api.py --agent --payment
```

`python3` chạy script bằng Python hệ thống. `auth.py` lấy token trong bộ nhớ và chỉ in issuer, audience, role; không in token hoặc mật khẩu. Nó dùng client credentials cho `internal-service` và PKCE của client `frontend` cho BUYER. Địa chỉ callback đã đăng ký là một định danh của flow; script chặn redirect tại chỗ, không gửi code tới host callback. `smoke-api.py` dùng token BUYER, gọi catalog/detail/availability, tạo order, replay cùng khóa, đọc order, tạo URL thanh toán giả rồi hủy hold. `--agent` chọn tên bằng chứng sau khi gắn agent. `--payment` thêm bước tạo URL thanh toán; nó không hoàn tất giao dịch VNPay. Script giữ bản kết quả trước khi ghi lượt mới.

Kiểm: thấy HTTP 200 cho API đọc, 201 cho tạo/replay order, `idempotency_same_order=true`, và hủy hold 200. `payment_url_present=true` chỉ có nghĩa API tạo URL giả thành công.

## 7. Agent và Collector tại chỗ

Jar agent nằm ở `/opt/flash-ticket-app/otel/opentelemetry-javaagent.jar`, bản 2.33.1. SHA-256 nằm trong manifest bàn giao. `/home/ubuntu/t058/attach-agent.py` thêm biến vào env của tám JVM, tạo bản compose riêng ở `compose-exp`, gắn `/otel` chỉ đọc rồi recreate từng service. Hai tùy chọn `-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC` được giữ trong `JAVA_TOOL_OPTIONS`.

Các biến thêm: `JAVA_TOOL_OPTIONS`, `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_TRACES_SAMPLER`, `OTEL_LOGS_EXPORTER`, `OTEL_METRIC_EXPORT_INTERVAL`, `OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY`, `OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY`. `parentbased_always_on` giữ sampling 100% theo parent; `http/protobuf` chọn OTLP HTTP; metric xuất mỗi 10 giây. Log đi stdout → filelog, vì `OTEL_LOGS_EXPORTER=none`.

Collector tại chỗ dùng `/opt/flash-ticket-app/collector/config.json`, compose ở `compose.json`; bí mật receiver nằm trong `collector.env` mode 600 trên `exp-app`. Nó nhận OTLP ở loopback cho Spring; Keycloak chạy bridge nên dùng `10.0.0.158:4318`. Firewall chỉ cho Docker subnet đã dò được tới cổng riêng này. Collector đọc đúng tám file log container ứng dụng, lấy Docker stats, host metrics, DB statistics và self metrics. Hàng đợi xuất sang `10.0.0.215:4317` có file storage ở `/data/queue`. Query string URL bị bỏ trước khi xuất trace. Tài khoản PostgreSQL chỉ có quyền thống kê; MongoDB dùng `clusterMonitor`; RabbitMQ dùng tài khoản monitoring. RCA không được cấp các tài khoản này.

Lệnh kiểm cấu hình đã chạy thành công:

```bash
docker compose -f /opt/flash-ticket-app/collector/compose.json -p flash-ticket-collector run --rm --no-deps collector validate --config=/etc/otel/config.json
curl -fsS http://127.0.0.1:13133
```

`run` tạo container kiểm tạm với đúng mount và env của service; `--rm` xóa container kiểm khi xong; `--no-deps` không bật dependency. `validate` chỉ kiểm cấu hình. `--config` chọn file trong container. Health API trả `Server available` khi Collector đang phục vụ.

Khi một container ứng dụng bị recreate, ID và đường dẫn log đổi. Script `setup-collector.py` tạo lại allowlist từ container hiện tại. Sau đó cần recreate Collector và ghim digest lại bằng `pin-images.py app`. Không đổi các phần này giữa cửa sổ đo.

Kiểm: có file `traces.jsonl` và `logs.jsonl` trong `collector/data`, health ready, và có dữ liệu ở Grafana. Kiểm agent chi tiết ở `out/kiem-agent.md`: C1 hiện đạt một phần, còn thiếu span Redis dù lệnh Redis có chạy.

## 8. Chuyển từ LGTM sang kho ghim riêng

LGTM đã được dùng để smoke trước. Hiện container đó đã dừng, volume còn giữ. Stack đang chạy nằm tại `/opt/flash-ticket-obs/pinned/compose.json`, gồm Collector 0.165.0, Prometheus 3.16.0, Loki 3.7.9, Tempo 3.1.1 và Grafana 13.3.0. `out/image-pins-obs.json` ghi digest và kiến trúc thực tế. Compose cuối dùng digest; không phụ thuộc tag thay đổi về sau.

`out/prepare-pinned-obs.py` tạo cấu hình, `out/deploy-pinned-obs.sh` kéo image và bật kho. Lần kiểm cờ CLI Tempo chưa thành công không được dùng làm lệnh hướng dẫn; cấu hình cuối đã chạy và API ready đã kiểm. Tempo chạy monolithic, không cần Kafka. RED và service graph được tạo ở Collector trung tâm, không bật metrics-generator Tempo lần nữa.

Trace đi Tempo và file; log đi Loki và file; metric đi Prometheus OTLP receiver và file. File thu nằm ở `/opt/flash-ticket-obs/pinned/data/capture`. API của ba kho publish loopback. Grafana nghe `10.0.0.215:3000`; Collector nghe `10.0.0.215:4317/4318`. Không đổi Security List Oracle.

Các lệnh đã chạy:

```bash
curl -fsS http://127.0.0.1:3200/ready
curl -fsS http://127.0.0.1:3100/ready
curl -fsS http://127.0.0.1:9090/-/ready
curl -fsS http://10.0.0.215:3000/api/health
```

`curl` kiểm từng API trên `exp-obs`; `-f` coi HTTP lỗi là lỗi lệnh, `-sS` bỏ thanh tiến độ nhưng vẫn báo lỗi. Loki có khoảng chờ khởi động trước khi ready.

Kiểm: Tempo/Loki trả `ready`, Prometheus báo sẵn sàng, Grafana trả `database=ok`. `out/grafana-evidence.json` lưu việc Grafana proxy trả trace 18 span, log và metric thật, cùng URL dashboard. Chưa kiểm bố cục dashboard bằng trình duyệt.

## 9. Xem bằng MobaXterm và đường hầm SSH

Trong **MobaXterm → Tunneling → New SSH tunnel**, chọn local port forwarding. SSH server là `213.35.116.128`, user `ubuntu`, khóa `exp-obs`. Tạo hai đường:

| Cổng trên laptop | Remote server | Remote port | Dùng để |
|---|---|---|---|
| 13000 | 10.0.0.215 | 3000 | Grafana |
| 18081 | 10.0.0.158 | 8081 | Gateway |

Hai đường cùng đi qua `exp-obs`; máy này gọi gateway qua subnet nội bộ. Lượt đêm đã kiểm đường tương đương bằng Git SSH, chưa thao tác GUI MobaXterm. Lệnh đã chạy trên PowerShell:

```powershell
& 'C:/Program Files/Git/usr/bin/ssh.exe' -i 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key' -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -N -L 127.0.0.1:13000:10.0.0.215:3000 -L 127.0.0.1:18081:10.0.0.158:8081 ubuntu@213.35.116.128
```

`&` chạy chương trình có đường dẫn trong dấu nháy. `-i` chọn khóa. Các `-o` đầu giữ hành vi SSH như mục 1. `ExitOnForwardFailure=yes` dừng nếu cổng forward không tạo được. `ServerAliveInterval=30` gửi keepalive mỗi 30 giây. `-N` chỉ tạo tunnel. Mỗi `-L` có dạng địa chỉ nghe của laptop:cổng laptop:máy đích:cổng đích. `127.0.0.1` giữ cổng laptop trong máy. Tài khoản sau cùng là SSH server dùng làm đầu cầu.

Mở `http://127.0.0.1:13000/d/t058-flashticket/flashticket-t-058`. Tài khoản Grafana là tên trong `GF_SECURITY_ADMIN_USER`; mật khẩu có giá trị sinh ngẫu nhiên trên máy, xem `/opt/flash-ticket-obs/grafana.env` trên `exp-obs`. Không chép giá trị vào bản bàn giao. Gateway ở `http://127.0.0.1:18081`. Token ứng dụng vẫn lấy bằng script trên `exp-app`, giữ issuer nội bộ ở mục 4.

Kiểm đã chạy: `GET http://127.0.0.1:13000/api/health` và `GET http://127.0.0.1:18081/api/v1/events` đều trả HTTP 200; xem `out/tunnel-check.json`.

Đã kiểm lại cuối lượt, cả hai vẫn200 (`tunnel-check-final.json`). Tunnel của Codex đã đóng22:50:40Z; khi Minh xem, tạo tunnel MobaXterm/GitSSH mới theo phần này. Các container Oracle vẫn chạy.

## 10. Đo tài nguyên của lượt đêm

Theo STEER #3, lượt chính được rút từ SPEC 1 giờ + 1 giờ còn **30 phút rảnh + 30 phút tải đọc nhẹ**, để còn thời gian kiểm lỗi thử và M1. C3 vì vậy chỉ có bằng chứng rút ngắn. Không dùng nó thay phép đo đủ thời lượng của SPEC. Các mẫu đầu của lịch cũ vẫn được giữ.

Lịch chính: 20:45–21:15Z rảnh; 21:15–21:45Z tải đọc 1 request/giây luân phiên catalog, detail, availability. `measure-resources.py` lấy mẫu mỗi 15 giây trên từng máy: CPU host, RAM available, Docker stats từng container, trạng thái OOM/restart, counter Collector và dung lượng file kho. CPU host tính từ chênh `/proc/stat`; CPU từng container lấy từ Docker. GB/giờ là ngoại suy từ tăng trưởng byte trong cửa sổ 30 phút, chưa phải số đo đủ một giờ.

Lệnh phát đã chạy trên `exp-app`:

```bash
sudo nohup python3 -u /home/ubuntu/t058/measure-resources.py app 2026-11-10T20:45:00Z 1800 resources-30m > /home/ubuntu/t058/resources-30m-app.log 2>&1 < /dev/null &
```

Trên `exp-obs`, lệnh tương tự dùng vai trò `obs`; tải đọc được phát bằng `light-load.py`. `nohup` giữ tiến trình khi SSH mất; `-u` ghi tiến độ Python ngay; `app` chọn vai trò; mốc UTC là lúc bắt đầu; `1800` là số giây mỗi pha; `resources-30m` đặt tên lượt. `>` chọn log; `2>&1` gộp lỗi vào cùng log; `< /dev/null` bỏ stdin; `&` chạy nền. File JSONL giữ từng mẫu; summary chỉ có khi tiến trình kết thúc.

Kiểm đã xong: cả hai log có `RESOURCE_WINDOWS_COMPLETE`, mỗi máy 241 mẫu. `out/so-do-tai-nguyen.json` giữ số tổng hợp, raw JSONL cũng đã nhận. **Cả pha rảnh và tải đều có OOM booking cgroup 512 MiB**, lúc 21:04:18Z và 21:40:18Z. Không gọi đây là nền sạch hay phép đo ổn định đạt. `State.OOMKilled=false` sau restart đã bỏ sót lịch sử; kernel journal và delta restart xác nhận. Xem `out/kiem-bo-nho.md`.

## 11. Sửa giới hạn bộ nhớ trong bản thực nghiệm

Sau C3, đã chạy thành công trên `exp-app`:

```bash
sudo nohup python3 -u /home/ubuntu/t058/fix-jvm-memory.py > /home/ubuntu/t058/fix-jvm-memory.log 2>&1 < /dev/null &
```

`sudo` cho script quyền sửa bản triển khai và gọi Docker. `nohup`, `-u`, các ký hiệu chuyển log và `&` có nghĩa như mục10. Script chỉ chấp nhận chạy sau sentinel C3; không chạy lại khi đã có marker hoàn tất. Nó đổi `mem_limit` trong **compose-exp**, rồi gọi `IMAGE=<image đã build> docker compose -f ... -p ... up -d` cho năm service. Không đổi image hoặc code. Collector được tạo lại allowlist log theo container ID mới và ghim lại digest.

Giới hạn đã dùng: booking/payment/event 1024 MiB; discovery768 MiB; Keycloak1536 MiB. Gateway/ticket/user giữ768 MiB. Đây là lệch giới hạn so với compose gốc của nhóm. Lý do: booking đã OOM; payment đạt95,41%, discovery89,97%, event80,53%, Keycloak79,39% working set so với limit trong C3. Chưa có bằng chứng giới hạn mới là tối ưu. Cờ JVM50% vàUTC vẫn giữ nguyên.

Kiểm: gõ `tail -n 8 /home/ubuntu/t058/fix-jvm-memory.log` thấy `finished_utc=2026-11-10T21:50:53.940859+00:00` và `consecutive_successful_probes=3`. Catalog, availability, Keycloak discovery và health của discovery đã trả200. JSON chi tiết nằm ở `out/jvm-memory-fix.json`. Các phản hồi lỗi trong đợt recreate vẫn giữ trong log tải.

Bản cấu hình công khai đã nhận ở `out/public-app-config.tgz` và `out/public-obs-config.tgz`, kèm audit/hash. Các gói này có compose/config cuối, không có env, realm chứa bí mật hoặc QR ring. Khi dựng mới, dùng giới hạn cuối trong compose-exp; không cần lặp lại OOM để biết phải tăng limit. Chưa dựng lại toàn bộ hai VM bằng gói cuối từ số0.

Đã phát monitor mới trên `exp-app`:

```bash
sudo nohup python3 -u /home/ubuntu/t058/monitor-jvm.py 2400 > /home/ubuntu/t058/monitor-jvm.log 2>&1 < /dev/null &
```

`2400` là thời gian theo dõi40phút. Script đọc cgroup `memory.events` và đúng tiến trình `java` để có RSS; không chỉ đọc PID1 của container, vì PID1 Keycloak là shell. Đây là theo dõi sau sửa, không thay C3 đủ1h+1h hay phép đo overhead agent có đối chứng.

Kiểm: gõ `tail -n 2 /home/ubuntu/t058/monitor-jvm.log` thấy dòng có giờ UTC, `oom_kill 0 restarts 0` khi chưa có lỗi ngoài kế hoạch. Nếu không bằng0 thì đọc counter/journal; không suy từ mỗi trạng thái hiện tại.

## 12. Chuẩn bị M1 và khóa lại kế hoạch

`prepare-m1.sh` đã tạo user `rca`, user `ledger`, giải nén bản `src/` chỉ đọc từ laptop và dựng Python3.12 trên `exp-obs`. Các lệnh trong script đã chạy:

```bash
sudo -u rca python3 -m venv /opt/flash-ticket-rca/venv
sudo -u rca /opt/flash-ticket-rca/venv/bin/pip install -r /opt/flash-ticket-rca/results/T-044/requirements-m1.txt -c /opt/flash-ticket-rca/results/T-044/freeze-m1.txt
sudo -u rca /opt/flash-ticket-rca/venv/bin/pip check
sudo -u rca test ! -r /var/lib/flash-ticket-ledger/ledger.jsonl
```

`sudo -u rca` chạy với user RCA. `python3 -m venv` tạo môi trường riêng tại đường dẫn cuối. `pip install -r` lấy danh sách gói cần cài; `-c` áp phiên bản ghim trong freeze. `pip check` kiểm xung đột dependency. `test ! -r` thành công khi user không đọc được ledger. Không cấp quyền Docker cho user RCA.

`upload-m1.ps1` đã chép adapter mới, stager và runner lên `exp-obs`; giữ code P7/P3 chỉ đọc. Đã kiểm39SHA của bản P7 khóa và sáu hash adapter/runner/config theo planv2. `out/python-packages.json` ghi bản gói thực tế. Adapter giữ parent thiếu, kiểm ID và đổi thời gian bằng số nguyên; tám kiểm ngữ nghĩa đã đạt.

Planv1 `m1-execution-plan.json` giữ nguyên nhưng hai ca đã hủy sau OOM, chưa có đầu ra M1v1. Theo STEER#4, planv2 được khóa21:52:40Z, ghi rõ sửa sau khi thấyOOM và trước đầu raM1. Chờ ổn định hơn10phút rồi mới dùng normal22:01–22:11Z; tải và cgroup đã kiểm606request trong khoảng chờ,600request trong normal, đều200 và không restart/OOM. Chỉ định pause event-service không trước22:17Z; không pausebooking. Kế hoạch/nhãn không đi vào API bảy tham số M1.

Trace/log bản đầu lấy từ mirror OTLP của Collector; metric lấy qua Prometheus API. Chưa có bộ đọc đầy đủ Tempo/Loki API. Chi tiết giao thức và giới hạn ở `out/rca-ban-dau.md`. Lệnh đóng gói/chạy chỉ được bổ sung khi thực thi thành công.

Kiểm: `pip check` trả `No broken requirements found`; kiểm ledger trả exit0; hai file `stability-normal-*.json` có `passed=true`. Điều đó chỉ xác nhận cửa sổ quan sát đã khai; không là đánh giá hiệu quả M1.

## 13. Đóng gói và chạy M1 v2

Sau khi đủ dữ liệu, các lệnh sau đã chạy thành công trên `exp-obs`:

```bash
sudo nohup /opt/flash-ticket-rca/venv/bin/python -B -u /opt/flash-ticket-rca/stage-m1.py --id c12e47ab --t 1794348360 > /home/ubuntu/t058/stage-c12e47ab.log 2>&1 < /dev/null &
sudo nohup /opt/flash-ticket-rca/venv/bin/python -B -u /opt/flash-ticket-rca/stage-m1.py --id f4a8c021 --t 1794349048 > /home/ubuntu/t058/stage-f4a8c021.log 2>&1 < /dev/null &
sudo -u rca nohup timeout --kill-after=30s 600s /opt/flash-ticket-rca/venv/bin/python -B -u /opt/flash-ticket-rca/run-m1.py --id c12e47ab > /home/ubuntu/t058/m1-c12e47ab.log 2>&1 < /dev/null &
sudo -u rca nohup timeout --kill-after=30s 600s /opt/flash-ticket-rca/venv/bin/python -B -u /opt/flash-ticket-rca/run-m1.py --id f4a8c021 > /home/ubuntu/t058/m1-f4a8c021.log 2>&1 < /dev/null &
```

`stage-m1.py` chốt prefix byte của file đang ghi, băm nguồn và giữ gói20phút quanh `t`. `--id` là mã mờ ngoài thuật toán; `--t` là Unix giây nguyên. `-B` không ghi bytecode cache; `-u` ghi log ngay. Runner dùng đúng bảy tham số, tự cắt cửa sổ10phút và chạy hai lần với cache mới. `sudo -u rca` giảm quyền về user RCA. `timeout 600s` giới hạn điều phối10phút; `--kill-after=30s` buộc dừng sau30giây nếu tiến trình không thoát khi hết hạn. Các lượt thực tế hoàn thành trong vài giây, không chạm timeout. Redirection/nohup như mục10.

Không chạy lại vào mã đã có: stager/runner từ chối ghi đè gói và output. Kết quả hiện có ở `/opt/flash-ticket-rca/cases/<id>` và `outputs/<id>`. `collect-m1.ps1` đã nhận hai archive, quét đối chiếu credential/JWT, so SHA với Oracle rồi mới giải nén dưới `out/rca-ban-dau/`. Ledger chỉ ghi thêm, nằm ngoài gói M1.

Kiểm: xem `outputs/<id>/summary.json` thấy `status=OK`, `deterministic_repeat=true`, `source_pins_checked=39`. Normal trả17/17; ca pause trả16/17 và `NO_VALID_CHANNEL=[event-service]`. Không gọi đó là chẩn đoán đúng. Cả hai graph có7nút/8cạnh, E2dựphòng0; `out/rca-ban-dau.md` ghi số mẫu thiếu và giới hạn.

Lỗi chủ động đã chạy đúng một lần trên `exp-app`:

```bash
sudo nohup python3 -u /home/ubuntu/t058/pause-probe-v2.py > /home/ubuntu/t058/pause-probe-v2.log 2>&1 < /dev/null &
```

Script xác nhận event đang chạy, tạo timer unpause dự phòng330giây, pause300giây rồi unpause trong `finally`. Lệnh này đã hoàn tất; ledger có hai dòng nối SHA, unpause22:22:28Z. Script từ chối lặp nếu ledger đã có dữ liệu. Không dùng bản pausebooking v1.

Kiểm: `tail -n 1 /home/ubuntu/t058/pause-probe-v2.log` có `intervention_end`, `command_exit=0`, `Paused=false`, `Running=true`. Tải độc lập cho catalog/detail trở lại200 ở22:23:00/01Z; availability thuộc booking nên không dùng nó làm mốc hồi phục event.

## Phụ lục: tên biến env

Lấy từ out/env-inventory-after-agent.json. Chỉ có tên biến. Với biến bí mật: giá trị sinh ngẫu nhiên trên máy, xem file env tương ứng trên exp-app.

### api-gateway

API_GATEWAY_PORT, CORS_ALLOWED_ORIGINS, ENVIRONMENT, EUREKA_CLIENT_ENABLED, EUREKA_INSTANCE_IP_ADDRESS, EUREKA_INSTANCE_PREFER_IP_ADDRESS, EUREKA_SERVER_URL, EVENT_IMAGES_GATEWAY_TIME_LIMIT, GATEWAY_REDIS_TIMEOUT, HOST_ID, INSTANCE_ID, INTEGRATION_BOOKING_GATEWAY_TIME_LIMIT, INTEGRATION_EVENT_GATEWAY_TIME_LIMIT, INTEGRATION_GATEWAY_HTTP_RESPONSE_TIMEOUT, INTEGRATION_PAYMENT_GATEWAY_TIME_LIMIT, INTEGRATION_TICKET_GATEWAY_TIME_LIMIT, INTEGRATION_USER_GATEWAY_TIME_LIMIT, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KEYCLOAK_AUDIENCE, KEYCLOAK_IDENTITY_REALM_ID, KEYCLOAK_ISSUER_URI, KEYCLOAK_JWK_SET_URI, KEYCLOAK_TOKEN_URI, LOGGING_STRUCTURED_FORMAT_CONSOLE, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER, RABBITMQ_BUSINESS_EXCHANGE, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_VHOST, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, SERVER_ADDRESS, SERVICE_VERSION.

### booking-service

BOOKING_DB_PASSWORD, BOOKING_DB_URL, BOOKING_DB_USERNAME, BOOKING_DDL_AUTO, BOOKING_ENVIRONMENT, BOOKING_HOST_ID, BOOKING_INSTANCE_ID, BOOKING_INTERNAL_SERVICE_CLIENT_SECRET, BOOKING_KEYCLOAK_AUDIENCE, BOOKING_KEYCLOAK_IDENTITY_REALM_ID, BOOKING_KEYCLOAK_ISSUER_URI, BOOKING_KEYCLOAK_JWK_SET_URI, BOOKING_KEYCLOAK_TOKEN_URI, BOOKING_RABBITMQ_BUSINESS_EXCHANGE, BOOKING_RABBITMQ_HOST, BOOKING_RABBITMQ_PASSWORD, BOOKING_RABBITMQ_PORT, BOOKING_RABBITMQ_USERNAME, BOOKING_RABBITMQ_VHOST, BOOKING_SERVICE_PORT, BOOKING_SERVICE_VERSION, ENVIRONMENT, EUREKA_CLIENT_ENABLED, EUREKA_INSTANCE_IP_ADDRESS, EUREKA_INSTANCE_PREFER_IP_ADDRESS, EUREKA_SERVER_URL, HOST_ID, INSTANCE_ID, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KEYCLOAK_AUDIENCE, KEYCLOAK_IDENTITY_REALM_ID, KEYCLOAK_ISSUER_URI, KEYCLOAK_JWK_SET_URI, KEYCLOAK_TOKEN_URI, LOGGING_STRUCTURED_FORMAT_CONSOLE, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER, PAYMENT_SERVICE_CLIENT_ID, PAYMENT_SERVICE_TOKEN_URI, RABBITMQ_BUSINESS_EXCHANGE, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_VHOST, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, SERVER_ADDRESS, SERVICE_VERSION, SPRING_JPA_HIBERNATE_DDL_AUTO.

### discovery-server

DISCOVERY_SERVER_PORT, ENVIRONMENT, EUREKA_CLIENT_ENABLED, EUREKA_INSTANCE_IP_ADDRESS, EUREKA_INSTANCE_PREFER_IP_ADDRESS, EUREKA_SERVER_URL, HOST_ID, INSTANCE_ID, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KEYCLOAK_AUDIENCE, KEYCLOAK_IDENTITY_REALM_ID, KEYCLOAK_ISSUER_URI, KEYCLOAK_JWK_SET_URI, KEYCLOAK_TOKEN_URI, LOGGING_STRUCTURED_FORMAT_CONSOLE, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER, RABBITMQ_BUSINESS_EXCHANGE, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_VHOST, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, SERVER_ADDRESS, SERVER_PORT, SERVICE_VERSION.

### event-service

ENVIRONMENT, EUREKA_CLIENT_ENABLED, EUREKA_INSTANCE_IP_ADDRESS, EUREKA_INSTANCE_PREFER_IP_ADDRESS, EUREKA_SERVER_URL, EVENT_BOOKING_BASE_URL, EVENT_CANCELLATION_SUMMARY_MAX_AGE, EVENT_DB_PASSWORD, EVENT_DB_URL, EVENT_DB_USERNAME, EVENT_ENVIRONMENT, EVENT_HOST_ID, EVENT_IMAGES_API_KEY, EVENT_IMAGES_API_SECRET, EVENT_IMAGES_CLOUD_NAME, EVENT_IMAGES_FOLDER, EVENT_IMAGES_GATEWAY_TIME_LIMIT, EVENT_IMAGES_MAX_BYTES, EVENT_IMAGES_MAX_COUNT, EVENT_IMAGES_MAX_PIXELS, EVENT_IMAGES_MAX_REQUEST_BYTES, EVENT_IMAGES_TIMEOUT, EVENT_INSTANCE_ID, EVENT_INTERNAL_SERVICE_CLIENT_SECRET, EVENT_JAVA_OPTIONS, EVENT_KEYCLOAK_AUDIENCE, EVENT_KEYCLOAK_IDENTITY_REALM_ID, EVENT_KEYCLOAK_ISSUER_URI, EVENT_KEYCLOAK_JWK_SET_URI, EVENT_KEYCLOAK_TOKEN_URI, EVENT_MEMORY_LIMIT, EVENT_OUTBOX_BATCH_SIZE, EVENT_OUTBOX_CONFIRM_TIMEOUT, EVENT_OUTBOX_ENABLED, EVENT_OUTBOX_INITIAL_RETRY, EVENT_OUTBOX_LEASE, EVENT_OUTBOX_MAXIMUM_RETRY, EVENT_OUTBOX_POLL_DELAY, EVENT_PAYMENT_BASE_URL, EVENT_RABBITMQ_BUSINESS_EXCHANGE, EVENT_RABBITMQ_HOST, EVENT_RABBITMQ_PASSWORD, EVENT_RABBITMQ_PORT, EVENT_RABBITMQ_USERNAME, EVENT_RABBITMQ_VHOST, EVENT_READ_CLOCK_SKEW, EVENT_READ_CONNECT_TIMEOUT, EVENT_READ_MODEL_ENABLED, EVENT_READ_RESPONSE_TIMEOUT, EVENT_SERVER_ADDRESS, EVENT_SERVICE_PORT, EVENT_SERVICE_VERSION, HOST_ID, INSTANCE_ID, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KEYCLOAK_AUDIENCE, KEYCLOAK_IDENTITY_REALM_ID, KEYCLOAK_ISSUER_URI, KEYCLOAK_JWK_SET_URI, KEYCLOAK_TOKEN_URI, LOGGING_STRUCTURED_FORMAT_CONSOLE, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER, PAYMENT_SERVICE_CLIENT_ID, PAYMENT_SERVICE_TOKEN_URI, RABBITMQ_BUSINESS_EXCHANGE, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_VHOST, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, SERVER_ADDRESS, SERVICE_VERSION.

### payment-service

BOOKING_SERVICE_URL, ENVIRONMENT, EUREKA_CLIENT_ENABLED, EUREKA_INSTANCE_IP_ADDRESS, EUREKA_INSTANCE_PREFER_IP_ADDRESS, EUREKA_SERVER_URL, HOST_ID, INSTANCE_ID, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KEYCLOAK_AUDIENCE, KEYCLOAK_IDENTITY_REALM_ID, KEYCLOAK_ISSUER_URI, KEYCLOAK_JWK_SET_URI, KEYCLOAK_TOKEN_URI, LOGGING_STRUCTURED_FORMAT_CONSOLE, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER, PAYMENT_DB_PASSWORD, PAYMENT_DB_URL, PAYMENT_DB_USERNAME, PAYMENT_DOCKER_BOOKING_URL, PAYMENT_ENVIRONMENT, PAYMENT_HOST_ID, PAYMENT_INSTANCE_ID, PAYMENT_INTERNAL_SERVICE_CLIENT_SECRET, PAYMENT_KEYCLOAK_AUDIENCE, PAYMENT_KEYCLOAK_IDENTITY_REALM_ID, PAYMENT_KEYCLOAK_ISSUER_URI, PAYMENT_KEYCLOAK_JWK_SET_URI, PAYMENT_KEYCLOAK_TOKEN_URI, PAYMENT_RABBITMQ_BUSINESS_EXCHANGE, PAYMENT_RABBITMQ_HOST, PAYMENT_RABBITMQ_PASSWORD, PAYMENT_RABBITMQ_PORT, PAYMENT_RABBITMQ_USERNAME, PAYMENT_RABBITMQ_VHOST, PAYMENT_SERVICE_CLIENT_ID, PAYMENT_SERVICE_CLIENT_SECRET, PAYMENT_SERVICE_PORT, PAYMENT_SERVICE_TOKEN_URI, PAYMENT_SERVICE_VERSION, PAYMENT_VNPAY_API_URL, PAYMENT_VNPAY_CALLBACKS_ENABLED, PAYMENT_VNPAY_ENABLED, PAYMENT_VNPAY_ENVIRONMENT, PAYMENT_WORKER_ENABLED, RABBITMQ_BUSINESS_EXCHANGE, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_VHOST, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, SERVER_ADDRESS, SERVICE_VERSION, VNPAY_API_URL, VNPAY_APP_RETURN_URL, VNPAY_HASH_SECRET, VNPAY_IPN_URL, VNPAY_PAYMENT_URL, VNPAY_RETURN_URL, VNPAY_TMN_CODE.

### ticket-service

ENVIRONMENT, EUREKA_CLIENT_ENABLED, EUREKA_INSTANCE_IP_ADDRESS, EUREKA_INSTANCE_PREFER_IP_ADDRESS, EUREKA_SERVER_URL, HOST_ID, INSTANCE_ID, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KEYCLOAK_AUDIENCE, KEYCLOAK_IDENTITY_REALM_ID, KEYCLOAK_ISSUER_URI, KEYCLOAK_JWK_SET_URI, KEYCLOAK_TOKEN_URI, LOGGING_STRUCTURED_FORMAT_CONSOLE, MAIL_HOST, MAIL_PASSWORD, MAIL_PORT, MAIL_SMTP_AUTH, MAIL_SMTP_STARTTLS_ENABLE, MAIL_SMTP_STARTTLS_REQUIRED, MAIL_USERNAME, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER, RABBITMQ_BUSINESS_EXCHANGE, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_VHOST, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, SERVER_ADDRESS, SERVICE_VERSION, TICKET_ACCESS_CONFIGURED_QUEUE, TICKET_BUSINESS_ENABLED, TICKET_BUYER_BASE_URL, TICKET_COMPLETED_RESULT_MESSAGE_TYPE, TICKET_COMPLETED_RESULT_ROUTING_KEY, TICKET_DB_PASSWORD, TICKET_DB_URL, TICKET_DB_USERNAME, TICKET_DELIVERY_CLAIM_LEASE, TICKET_DELIVERY_DISPLAY_ZONE, TICKET_ENVIRONMENT, TICKET_EVENT_CANCELLED_QUEUE, TICKET_FAILED_RESULT_ROUTING_KEY, TICKET_HOST_ID, TICKET_INSTANCE_ID, TICKET_INTERNAL_SERVICE_CLIENT_SECRET, TICKET_ISSUANCE_QUEUE, TICKET_KEYCLOAK_AUDIENCE, TICKET_KEYCLOAK_IDENTITY_REALM_ID, TICKET_KEYCLOAK_ISSUER_URI, TICKET_KEYCLOAK_JWK_SET_URI, TICKET_KEYCLOAK_TOKEN_URI, TICKET_LISTENERS_ENABLED, TICKET_MAIL_FROM, TICKET_MAIL_HEALTH_ENABLED, TICKET_OUTBOX_CLAIM_LEASE, TICKET_OUTBOX_CONFIRM_TIMEOUT, TICKET_QR_ACTIVE_KEY_VERSION, TICKET_QR_KEY_RING_LOCATION, TICKET_RABBITMQ_BUSINESS_EXCHANGE, TICKET_RABBITMQ_HOST, TICKET_RABBITMQ_PASSWORD, TICKET_RABBITMQ_PORT, TICKET_RABBITMQ_USERNAME, TICKET_RABBITMQ_VHOST, TICKET_SERVICE_PORT, TICKET_SERVICE_VERSION, TICKET_WORKERS_ENABLED, TICKET_WORKER_BATCH_SIZE, TICKET_WORKER_POLL_DELAY.

### user-service

ENVIRONMENT, EUREKA_CLIENT_ENABLED, EUREKA_INSTANCE_IP_ADDRESS, EUREKA_INSTANCE_PREFER_IP_ADDRESS, EUREKA_SERVER_URL, HOST_ID, INSTANCE_ID, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KEYCLOAK_AUDIENCE, KEYCLOAK_IDENTITY_REALM_ID, KEYCLOAK_ISSUER_URI, KEYCLOAK_JWK_SET_URI, KEYCLOAK_TOKEN_URI, LOGGING_STRUCTURED_FORMAT_CONSOLE, MONGO_URI, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER, RABBITMQ_BUSINESS_EXCHANGE, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_VHOST, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, SERVER_ADDRESS, SERVICE_VERSION, USER_ENVIRONMENT, USER_HOST_ID, USER_IDENTITY_ENABLED, USER_IDENTITY_MAX_MESSAGE_BYTES, USER_IDENTITY_QUEUE, USER_IMAGE_API_KEY, USER_IMAGE_API_SECRET, USER_IMAGE_CLOUD_NAME, USER_IMAGE_FOLDER, USER_IMAGE_MAX_BYTES, USER_IMAGE_MAX_FILE_SIZE, USER_IMAGE_MAX_PIXELS, USER_IMAGE_MAX_REQUEST_SIZE, USER_IMAGE_TIMEOUT, USER_INSTANCE_ID, USER_INTERNAL_SERVICE_CLIENT_SECRET, USER_JAVA_OPTIONS, USER_KEYCLOAK_ADMIN_BASE_URL, USER_KEYCLOAK_ADMIN_CLIENT_ID, USER_KEYCLOAK_ADMIN_CLIENT_SECRET, USER_KEYCLOAK_ADMIN_REALM, USER_KEYCLOAK_ADMIN_TIMEOUT, USER_KEYCLOAK_AUDIENCE, USER_KEYCLOAK_IDENTITY_REALM_ID, USER_KEYCLOAK_ISSUER_URI, USER_KEYCLOAK_JWK_SET_URI, USER_KEYCLOAK_TOKEN_URI, USER_MEMORY_LIMIT, USER_MONGO_COLLECTION_PREFIX, USER_MONGO_URI, USER_RABBITMQ_BUSINESS_EXCHANGE, USER_RABBITMQ_HOST, USER_RABBITMQ_PASSWORD, USER_RABBITMQ_PORT, USER_RABBITMQ_USERNAME, USER_RABBITMQ_VHOST, USER_RECOVERY_BATCH_SIZE, USER_RECOVERY_DELAY, USER_RECOVERY_ENABLED, USER_ROLE_GRANT_LEASE_DURATION, USER_ROLE_GRANT_WAIT_TIMEOUT, USER_SERVER_ADDRESS, USER_SERVICE_PORT, USER_SERVICE_VERSION.

### keycloak

FT_IDENTITY_OUTBOX_ENABLED, FT_IDENTITY_OUTBOX_INTERVAL_MS, FT_IDENTITY_RABBITMQ_HOST, FT_IDENTITY_RABBITMQ_PASSWORD, FT_IDENTITY_RABBITMQ_PORT, FT_IDENTITY_RABBITMQ_USERNAME, FT_IDENTITY_RABBITMQ_VHOST, INTERNAL_SERVICE_CLIENT_SECRET, JAVA_TOOL_OPTIONS, KC_BOOTSTRAP_ADMIN_PASSWORD, KC_BOOTSTRAP_ADMIN_USERNAME, KC_DB, KC_DB_PASSWORD, KC_DB_POOL_INITIAL_SIZE, KC_DB_POOL_MAX_SIZE, KC_DB_POOL_MIN_SIZE, KC_DB_URL, KC_DB_USERNAME, KC_HOSTNAME, KC_HTTP_ENABLED, KC_HTTP_MAX_QUEUED_REQUESTS, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY, OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY, OTEL_LOGS_EXPORTER, OTEL_METRIC_EXPORT_INTERVAL, OTEL_RESOURCE_ATTRIBUTES, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER.
