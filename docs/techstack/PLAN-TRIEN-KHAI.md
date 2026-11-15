# Kế hoạch triển khai FlashTicket làm nguồn dữ liệu RCA

- **Trạng thái:** ĐỀ XUẤT, chưa duyệt. Không phải SPEC. Duyệt file này không cấp quyền tạo máy, sửa repo FlashTicket, chạy tải, tiêm lỗi hay chạy lượt dài.
- **Người soạn:** Claude, ngày 10/11/2026. Người phản biện: chưa có (Minh quyết sau).
- **Quyền ghi:** prompt của Minh ngày 10/11/2026, đúng hai file trong `docs/techstack/`.
- **Sửa ngày 10/11/2026 (Minh duyệt gói sửa 6 điểm trong chat):** thêm P-F vào §3; bỏ các đoạn lo thiếu tín dụng (§2.3, §3, §4, §8, Q2, Q11); ghi máy `3.27.110.61` vào §4; B1 không cần sửa code (§6); đổi đề xuất Q4, Q6, Q13; thêm §9.1 ghi trả lời của Minh.
- **Sửa lần hai ngày 10/11/2026 (Minh: "Duyệt, ghi vào plan", bản sửa gộp 8 điểm):** thêm mục "Hình dung nhanh"; §6.1 thay B0–B3; cách dựng `exp-app` dùng lại compose và script của nhóm; kho thử ở `exp-obs`; local chỉ cho code Q6; nginx (§8.1); §10; TS §4.1; ghi `docs/DECISIONS.md`.
- **Sửa lần ba ngày 10/11/2026 (Minh: "duyệt đề xuất sửa plan"):** Collector hai tầng, tại chỗ trên `exp-app` và trung tâm trên `exp-obs`, vì `filelog`, `docker_stats`, `hostmetrics` chỉ chạy được trên máy ứng dụng. Sửa các sơ đồ, bảng vai trò, ngân sách RAM, §5.1, §5.3, bước 8; TECHSTACK §4.4 và §6.2.
- **Đọc cùng:** [TECHSTACK-NGHIEN-CUU.md](TECHSTACK-NGHIEN-CUU.md). Nhãn [REPO], [CODE], [MÁY], [WEB], [TÍNH], [CHƯA BIẾT], [CHƯA KIỂM], [SUY LUẬN] định nghĩa ở đầu file đó. "TS §x" là mục trong file đó.

---

## Hình dung nhanh (thêm 10/11/2026)

Mục tiêu: có một bản FlashTicket riêng để gây lỗi có chủ đích, thu dữ liệu, rồi cho RCA tìm nguyên nhân.

```
 exp-app (máy ứng dụng)                       exp-obs (máy quan sát)
 ┌───────────────────────────────┐  dữ liệu  ┌───────────────────────────────┐
 │ FlashTicket: 9 ứng dụng       │  đã gom   │ Collector TRUNG TÂM           │
 │ + 4 hạ tầng (DB, Redis...)    │ ────────▶ │   (spanmetrics, servicegraph) │
 │ + Java agent trong mỗi JVM    │           │ Prometheus lưu metric         │
 │       │ OTLP qua 127.0.0.1    │           │ Loki       lưu log            │
 │       ▼                       │           │ Tempo      lưu trace          │
 │ Collector TẠI CHỖ             │           │ Grafana    xem                │
 │   (đọc log, docker_stats,     │           │ RCA + sổ ghi lỗi đã tiêm      │
 │    hostmetrics, receiver DB)  │           └───────────────────────────────┘
 │ + Toxiproxy, Pumba (gây lỗi)  │
 └───────────────────────────────┘
 Máy 84: giữ nguyên cho nhóm. Laptop: viết cấu hình, điều khiển, chấm.
```

Vì sao hai Collector: log container, metric container và metric máy chỉ đọc được **trên chính máy chạy container** (file `/var/lib/docker/containers`, Docker socket, thông số máy). Một Collector đặt ở `exp-obs` không thấy được chúng. Collector tại chỗ gom mọi thứ của `exp-app` rồi đẩy một đường sang `exp-obs`; Collector trung tâm tính các số liệu cần nhìn toàn cục (`spanmetrics`, `servicegraph`) và chia vào ba kho.

| Tên | Là gì | Để làm gì |
|---|---|---|
| `exp-app` | Máy `3.27.110.61` | Chạy bản FlashTicket để thử nghiệm |
| `exp-obs` | Máy thứ hai ("obs" = observability, quan sát) | Chứa kho dữ liệu quan sát và chạy RCA |
| Java agent | File jar gắn vào JVM | Sinh trace, metric, log mà không sửa code |
| Collector tại chỗ (agent) | Trạm gom trên `exp-app` | Nhận OTLP từ các JVM qua `127.0.0.1`; đọc log container, `docker_stats`, `hostmetrics`, receiver DB; gắn `host.id`; loại container của công cụ tiêm lỗi; đẩy sang `exp-obs` |
| Collector trung tâm (gateway) | Trạm chia trên `exp-obs` | Nhận từ Collector tại chỗ; chạy `spanmetrics`, `servicegraph`; ghi vào ba kho và file theo lượt |
| Prometheus, Loki, Tempo | Ba kho | Lưu metric, log, trace |
| Grafana | Giao diện | Xem dữ liệu và đặt cảnh báo |
| Toxiproxy, Pumba | Công cụ gây lỗi | Làm chậm một đường nối; dừng hoặc ép tải một container |
| Sổ tiêm lỗi | File ghi "gây lỗi gì, lúc nào" | Đáp án để chấm; RCA không được đọc (§5) |
| Bộ đọc (adapter) | Code Python trong repo RCA | Chuyển dữ liệu từ kho thành đầu vào của M1 |

Tách `exp-obs` khỏi `exp-app` vì khi ép CPU hoặc làm chậm máy ứng dụng, kho dữ liệu không bị ảnh hưởng theo, và kho không tranh CPU, RAM với ứng dụng.

| | Repo cũ `flash-ticket-system` | Máy 84 (repo mới) | `exp-app` (đề xuất) |
|---|---|---|---|
| Đưa code lên | SSH, `git pull`, `docker compose up -d --build` | Push `main`, GitHub Actions deploy | SSH, `git clone` ở commit ghim, chạy script deploy của nhóm |
| Build ở đâu | Trên server | Trên GitHub | Không build; kéo image của 84 theo digest |
| Cấu hình | Trong `environment:` của compose | GitHub Secrets → file env | File env trên máy, Minh cấp |
| Cửa vào | nginx cổng 80 (`/`, `/api/`, `/auth/`) | Không có; mở thẳng 5173, 8081, 8080 | Như 84 |

Nguồn: [CODE] `flash-ticket-system/aws_ec2_deployment_guide.md` §6.1, `nginx.conf`, `docker-compose.apps.yml`; `flash-ticket-platform/deploy/app/README.md`; [MÁY] `docker compose ls` trên 84 ngày 10/11.

---

## 0. Tóm tắt

1. **Không đặt kho quan sát, tải hay tiêm lỗi lên máy demo `52.64.237.84`.** Máy có 4 GiB, đã dùng 1,4 GiB swap lúc rảnh, đĩa còn 5 GB, và là đích CD của cả nhóm [MÁY; TS §1.4].
2. **Khuyến nghị phương án P-E:** một môi trường thực nghiệm riêng gồm máy ứng dụng và máy quan sát + RCA (hai `m7i-flex.large` ở một tài khoản), máy tải ở tài khoản khác, máy 84 giữ làm demo tích hợp của nhóm, laptop làm điều khiển và chấm (§3, §4).
3. **Môi trường thực nghiệm chạy đúng digest đang có trên máy 84**, kéo ẩn danh từ GHCR được [MÁY; TS §4.8]. Không phụ thuộc CD; chỉ cần một bộ env riêng (Minh cấp, §9.1 Q6).
4. **Mốc tiêm lỗi** ghi vào sổ thực nghiệm chỉ ghi thêm, nằm ngoài quyền đọc của tiến trình RCA; dữ liệu thu trước, RCA chạy sau trên gói đã đóng; nhãn chỉ ghép sau khi đầu ra RCA đã băm (§5).
5. **Tới 16/11/2026:** chạy được M1 bản P7 khóa trên vài sự cố thử (smoke), không phải đánh giá (§6, B3). **Tới 30/12/2026:** đợt phát triển, khóa bản FlashTicket, demo, đợt đánh giá, chấm, viết.
6. Các điểm Minh cần quyết ở §9, mỗi điểm có đề xuất.

---

## 1. Dữ kiện đầu vào dùng trong kế hoạch

| Dữ kiện | Giá trị | Nhãn |
|---|---|---|
| Máy demo | `c7i-flex.large`, 2 vCPU, RAM 3812 MiB, swap dùng 1433 MiB, đĩa còn 5,0 GB | [MÁY] TS §1.4 |
| FlashTicket lúc rảnh | Tổng bộ nhớ 14 container 2443,7 MiB; tổng `mem_limit` 9024 MiB | [MÁY] TS §1.4 |
| Máy free-tier mạnh nhất | `m7i-flex.large` 2 vCPU, 8 GiB (7,6 GiB dùng được) | [WEB], [REPO] TS §1.6 |
| Quota mặc định | 5 vCPU mỗi vùng mỗi tài khoản → tối đa 2 máy 2 vCPU | [WEB] TS §1.6 |
| Giá `m7i-flex.large` | 0,1197 USD/giờ; IPv4 công khai 0,005 USD/giờ | [REPO], [WEB] TS §1.6 |
| Tín dụng | 3 tài khoản × 200 USD, hết hạn 6 tháng, ngày bắt đầu chưa rõ | Minh cung cấp 10/11; [CHƯA BIẾT] ngày mở, số dư |
| Laptop | RAM 15,7 GiB; ổ C còn 54,1 GB; ổ D còn 12,7 GB; Docker engine tắt | [MÁY] TS §1.5 |
| Mục tiêu gần | RCA bản đầu trên FlashTicket tới 16/11/2026 | [REPO] DECISIONS 09/11 |
| Demo | Khoảng một tháng từ 10/11; ngày chưa có | Minh cung cấp; [CHƯA BIẾT] |
| Nộp quyển | 30/12/2026 | [REPO] DECISIONS Q-23; KE-HOACH Phần B |

---

## 2. Ngân sách tài nguyên

### 2.1 Bộ nhớ theo thành phần

| Thành phần | GiB | Nhãn |
|---|---|---|
| FlashTicket 14 container, lúc rảnh | 2,4 (cận dưới: tổng `MemUsage`) đến 3,8 (cộng phần đã đẩy ra swap) | [MÁY] `docker stats`, `free -m`; [TÍNH] 2443,7 MiB; 2443,7 + 1433 MiB |
| Agent trên 7 JVM Spring | 0,3–0,8 | [CHƯA KIỂM] ước lượng thô 40–110 MiB mỗi JVM; tài liệu OTel không có số; đo ở B2 |
| Toxiproxy | dưới 0,1 | [CHƯA KIỂM] |
| Collector tại chỗ trên `exp-app` | chưa có số | [CHƯA KIỂM] chưa có ước lượng riêng; đo ở B2 (thêm 10/11/2026) |
| Kho quan sát (Collector trung tâm, Prometheus, Loki, Tempo, Grafana) | 1,1–2,3 | [CHƯA KIỂM] ước lượng thô; đo ở B2 |
| k6 ở 20–100 request/giây | 0,2–0,5 | [CHƯA KIỂM] |
| Tiến trình M1 hoặc baseline | 0,3–1,0 (giả định dùng để cộng tổng). Số đo duy nhất có: BOCPD RSS đỉnh 321,6 MB; M1 chưa đo | [REPO] `results/T-025/chi-phi.md` §1; [CHƯA KIỂM] cho M1, đo ở B3 |

**Tổng theo vai trò máy** [TÍNH, cộng các dòng trên; mọi số chưa kiểm kéo theo tổng chưa kiểm]:

| Máy | Tổng | So với RAM |
|---|---|---|
| Ứng dụng (FT + agent + Toxiproxy), chưa gồm Collector tại chỗ | 2,7–4,7 GiB | Vừa `m7i-flex.large` (7,6 GiB), còn ≥ 2,9 GiB. **Không vừa** `c7i-flex.large` (3,7 GiB): đã swap trước khi thêm agent |
| Quan sát + RCA (+ k6 nếu gộp) | 1,4–3,8 GiB | Vừa `m7i-flex.large` |
| Tất cả trên một máy 8 GiB | 3,8–7,0 GiB | 50–92% của 7,6 GiB: đầu trên quá sát |
| Tất cả trên laptop | 4,3–8,5 GiB | Vượt mức WSL mặc định 7,8 GiB ở đầu trên |

### 2.2 Dung lượng kho quan sát

Dùng giả định của KE-HOACH D.8.5: mỗi request 10 span × 450 B, 3 dòng log × 400 B [REPO `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.8.5].

| Tải | Trace 100% | Log | Tổng/giờ | 60 giờ chiến dịch |
|---|---|---|---|---|
| 20 request/giây | 0,32 GB | 0,09 GB | ≈ 0,41 GB | ≈ 25 GB |
| 100 request/giây | 1,6 GB | 0,43 GB | ≈ 2,0 GB | ≈ 122 GB |

- Bản xuất file theo lượt nhân đôi phần trace và log trước khi nén [TÍNH].
- Có span JDBC thì một request có thể sinh nhiều hơn 10 span [SUY LUẬN]. Phải đo ở B2.
- **Đề xuất:** đĩa máy quan sát 100 GB gp3; chiến dịch RCA ở tải vừa (≤ 50 request/giây); Tempo, Loki giữ 7 ngày như B16 §6; gói mỗi lượt nén và chép về laptop ổ C.

### 2.3 Chi phí [TÍNH]

- Một máy `m7i-flex.large` kèm một IPv4: 0,1197 + 0,005 = **0,1247 USD/giờ**, chưa tính EBS (giá chưa biết).
- Hai máy chạy 24/24 từ 13/11 tới 20/12 (37 ngày): 2 × 37 × 24 × 0,1247 ≈ **221 USD** (số tham khảo).
- **Minh xác nhận 10/11/2026: đủ tiền, đủ hạn để làm tới hết đồ án.** Chi phí không là ràng buộc khi chọn phương án; kế hoạch không cân nhắc thiếu tín dụng nữa.
- Gói dữ liệu vẫn chép về laptop sau mỗi đợt, để chấm và phát lại offline (§4, §7), không vì lý do tiền.

---

## 3. Năm phương án triển khai

### P-A. Toàn bộ trên laptop

- Ngân sách: 4,3–8,5 GiB RAM (§2.1); Docker trên ổ C còn 54,1 GB.
- Chạy FlashTicket bằng `deploy/docker-compose.integration.local.yml` (build từ mã nguồn, mạng bridge) [CODE]; compose của máy 84 dùng `network_mode: host`, [CHƯA KIỂM] hành vi trên Docker Desktop Windows.
- Hợp cho: smoke agent (H1), viết adapter, chấm, phát lại offline.
- Không hợp cho chiến dịch: laptop ngủ, tự cập nhật, đồng hồ lệch (KE-HOACH D.8.3); IDE, trình duyệt, k6 và kho cùng tranh CPU.

### P-B. Lai: ứng dụng và kho trên một server, tải và RCA trên laptop

- Server `m7i-flex.large`: 3,8–7,0 GiB (§2.1), sát trần.
- k6 từ laptop qua internet Việt Nam → Sydney: độ trễ và biến động mạng nhà vào dòng thời gian tải [CHƯA KIỂM] mức RTT.
- RCA đọc API qua SSH tunnel.
- Kho và ứng dụng tranh 2 vCPU: lúc tải, Collector có thể rớt dữ liệu và độ trễ ứng dụng lẫn chi phí thu thập [SUY LUẬN].

### P-C. Một server lớn (lên gói Paid)

- Ví dụ một máy 4 vCPU, 16 GiB (quota 5 vCPU cho phép một máy 4 vCPU). Tên loại và giá [CHƯA KIỂM].
- Đơn giản nhất về mạng. Nhưng: lên Paid thì phần vượt tín dụng bị tính tiền thẻ [WEB]; tải và kho chung máy với ứng dụng.

### P-D. Tách ba vai trò máy

- Máy ứng dụng `m7i-flex.large` (2,7–4,7 GiB); máy quan sát + RCA `m7i-flex.large` (1,4–3,3 GiB); máy tải `t3.small` hoặc `c7i-flex.large`.
- 6 vCPU > quota 5 → máy tải ở tài khoản khác, hoặc xin tăng quota.
- Nhiễu đo thấp nhất; telemetry đi trong một VPC.

### P-E (khuyến nghị). P-D + giữ máy 84 riêng cho demo của nhóm + laptop làm điều khiển

Như P-D, cộng: máy 84 không nhận tải hay lỗi; tài khoản thứ ba vừa chạy máy tải vừa là chỗ dựng bản sao để chạy song song đợt đánh giá.

```
TK-B (thực nghiệm, cùng VPC, IP riêng)          TK-C (tải, dự phòng)
┌───────────────────────────┐  OTLP   ┌────────────────────────┐     ┌──────────────┐
│ exp-app  m7i-flex.large   │ ───────▶│ exp-obs  m7i-flex.large│     │ loadgen      │
│ FlashTicket (digest 84)   │         │ Collector trung tâm,   │     │ k6 2.3.0     │
│ + agent, Collector tại chỗ│         │ Prometheus, Loki,      │     └──────┬───────┘
│ + Toxiproxy, Pumba        │         │ Tempo, Grafana,        │            │
│ + VNPay mock              │         │ RCA runner, sổ (user   │            │ HTTPS/HTTP tới
└──────────▲────────────────┘         │ riêng)                 │            │ cổng gateway
           └──────────────────────────┴────────────────────────┘◀───────────┘ (SG chỉ mở IP loadgen)
TK-A: máy 84 (demo, CD của nhóm), không đổi.   Laptop: SSH, chấm, phát lại, lưu gói (ổ C).
```

### So sánh

| Tiêu chí | P-A laptop | P-B lai | P-C một máy lớn | P-D tách 3 | **P-E** |
|---|---|---|---|---|---|
| RAM đủ | Sát/vượt WSL mặc định | Sát trần 7,6 GiB | Đủ (16 GiB, [CHƯA KIỂM]) | Đủ, dư mỗi máy | Đủ |
| Nhiễu đo khi tải | Cao | Cao (kho chung CPU; mạng nhà) | Trung bình (k6 chung máy) | Thấp | Thấp |
| Độ trễ telemetry | Localhost | Cùng máy | Cùng máy | Cùng VPC | Cùng VPC |
| Chi phí | 0 | 1 máy | 1 máy lớn, có thể bị tính tiền | 3 máy | 3 máy, bật theo đợt |
| Tài khoản, quota | 0 | 1 TK, 2 vCPU | 1 TK Paid, 4 vCPU | 2 TK hoặc quota tăng | 2 TK + TK demo |
| Vận hành | Thấp | Trung bình | Thấp | Cao | Cao nhất |
| Ảnh hưởng demo của nhóm | Không | Không | Không | Không | Không |
| Chuyển đổi sau này | Khó lên server | Dễ tách kho ra | Khó tách | Sẵn tách | Sẵn tách; dựng bản sao song song |
| Hợp với luật 19 (ưu tiên EC2) | Không, trừ smoke | Một phần | Có | Có | Có |

**Vì sao P-E.** Kết quả trên FlashTicket bị hội đồng soi về thiên lệch (KE-HOACH D.9, M-24). Nhiễu từ kho quan sát hoặc k6 chung máy làm khó phân biệt "lỗi được tiêm" với "nhiễu đo". P-E giữ ứng dụng một mình trên máy của nó, và không làm phiền máy demo mà cả nhóm đang deploy (lượt CD gần nhất 09/11/2026 17:03Z [WEB GitHub Actions API]).

**P-E sai khi:** quota không cho hai máy 8 GiB cùng tài khoản và không xin tăng được; hoặc không có bộ env riêng. Khi đó lùi về P-B (một máy, tải ≤ 20 request/giây, k6 chạy trên chính máy đó và ghi rõ giới hạn).

### P-F (bổ sung 10/11/2026). Máy 84 làm máy ứng dụng, máy mới làm máy quan sát

Phương án này bản đầu của kế hoạch chỉ nhắc một dòng ở Q3(b), chưa đánh giá đầy đủ. Minh nêu ngày 10/11: "84 đã chạy rồi... tôi tưởng collector chỉ cần nối sang 84 để thu dữ liệu là được".

- **Collector không tự lấy được dữ liệu từ 84.** FlashTicket hiện không xuất trace và không có metric Prometheus (pom không có OpenTelemetry; actuator chỉ `health,info`) [CODE; TS §1.7]. Dữ liệu phải do agent trong từng JVM sinh ra rồi gửi sang Collector. Dùng 84 thì agent chạy trên chính 84.
- **Máy 84 ngày 10/11:** RAM 3812 MiB, swap đang dùng 1639/4095 MiB; 14 container: 10 của ứng dụng (9 ứng dụng + ngrok, do CD quản lý ở `/opt/flash-ticket-app`) và 4 hạ tầng (PostgreSQL, MongoDB, Redis, RabbitMQ, dựng tay ở `/opt/flash-ticket-infra`) [MÁY `free -m`, `docker ps`, `docker compose ls`].

| Tiêu chí | P-E | P-F |
|---|---|---|
| Dựng thêm 14 container | Có; cùng image theo digest, cùng compose `deploy/app/*.yml` | Không |
| Ảnh hưởng nhóm | Không | Tiêm lỗi làm hỏng 84 lúc đang chạy; phải hẹn giờ và đóng băng CD |
| Dữ liệu | Chỉ có tải và lỗi của thực nghiệm | Lẫn thao tác của thành viên khác và lượt CD giữa chừng: bất thường không có nhãn [SUY LUẬN] |
| Bản code trong một đợt | Cố định theo digest đã ghim | Đổi mỗi khi có push lên `main` [CODE `cd.yml`] |
| Thay đổi trên 84 | Không | Đổi loại máy lên 8 GiB (IP đổi nếu không có Elastic IP, kéo theo `FT84_SSH_HOST`); thêm agent và Toxiproxy vào env của 84 |
| Công sức | Thêm một bộ env và một lần dựng hạ tầng | Ít hơn lúc đầu; tốn điều phối với nhóm ở mọi đợt chạy |

**Vẫn khuyến nghị P-E.** Lý do là tính đúng của đánh giá (nhãn sạch, bản code cố định), không phải tiền. P-F hợp hơn nếu nhóm đồng ý đóng băng 84 theo lịch chạy và 84 được nâng RAM.

---

## 4. Phân bổ ba tài khoản và máy hiện có

Minh trả lời Q2 ngày 10/11/2026: không cần theo dõi ngày mở, số dư từng tài khoản; đủ tiền, đủ hạn (§9.1). Tên TK-A, TK-B, TK-C dưới đây chỉ là vai trò; máy nào thuộc tài khoản nào do Minh sắp.

| Tài khoản | Vai trò | Máy | vCPU dùng | Lịch bật |
|---|---|---|---|---|
| TK-A (chứa máy 84) | Demo và tích hợp của nhóm | máy 84 `c7i-flex.large`, giữ nguyên | 2 | Theo nhóm |
| TK-B | Thực nghiệm chính | `exp-app`, `exp-obs` (`m7i-flex.large`), cùng VPC, cùng AZ | 4/5 | Bật theo đợt; tắt bằng Stop, không Terminate (Q-42) |
| TK-C | Tải; chạy song song đợt đánh giá; EC2 batch cho baseline | `loadgen`; khi cần thêm bản sao `exp-app`/`exp-obs` | 2–4/5 | Chỉ khi chạy |
| Laptop | Điều khiển, phát triển adapter, chấm, phát lại offline, lưu gói | — | — | — |

- **Máy thực nghiệm đầu tiên: `3.27.110.61`** (Minh tạo 10/11/2026), dùng làm `exp-app`. Kiểm chỉ đọc ngày 10/11: `c7i-flex.large`, 2 vCPU, RAM 3811 MiB, không swap, đĩa 48 GB còn 46 GB, Ubuntu 26.04.1, vùng `ap-southeast-2a`, chưa cài Docker [MÁY `free -m`, `df -h`, metadata]. Loại này bằng máy 84, không vừa vai trò máy ứng dụng (§2.1: 2,7–4,7 GiB, [CHƯA KIỂM]); **cần đổi sang `m7i-flex.large` (8 GiB)**. `exp-obs` chưa tạo. Máy 84 dùng Ubuntu 24.04; Docker trên 26.04 [CHƯA KIỂM], kiểm ở B1.

- **Nếu TK-B xin tăng quota lên ≥ 8 vCPU được**, đặt `loadgen` cùng VPC ở TK-B; TK-C chỉ còn dự phòng [WEB quota điều chỉnh được].
- **Tải đi qua internet** từ TK-C tới cổng gateway của `exp-app`. Đây cũng là đường người dùng thật. Security Group chỉ mở cổng gateway cho IP `loadgen` và SSH cho IP của Minh. Phí truyền dữ liệu ra internet [CHƯA KIỂM].
- **Telemetry không đi qua tài khoản khác.** Đúng tinh thần "lượt chính thức đặt trong một tài khoản" [CODE `docs/architecture/aws-runtime-baseline.md` §3, qua REPO `KE-HOACH` D.8.4].
- **Máy 84 trước demo.** Hai đường, chờ Minh quyết (Q3): (a) giữ nguyên 84 cho chức năng bán vé, phần phát hiện–chẩn đoán demo trên môi trường thực nghiệm đã đóng băng; (b) đổi 84 sang `m7i-flex.large` và cài agent + kho trước demo. (b) đổi IP công khai khi Stop/Start nếu không có Elastic IP, kéo theo đổi biến `FT84_SSH_HOST` của CD [SUY LUẬN từ REPO `results/T-007/moi-truong-ec2.md` §1: "Địa chỉ IP đổi sau mỗi lần Stop/Start"].
- **Dọn máy 84** (việc của nhóm, cần duyệt): 8,712 GB image có thể thu hồi; swap đang dùng 1,4 GiB [MÁY].

---

## 5. Mốc tiêm lỗi: cách ghi và cách dùng

Mục tiêu: nhãn đủ để chấm, nhưng không lọt vào phương pháp (AGENTS luật cứng 6; MRP §6 mục 8). Dựa trên cách repo đang làm ở T-054: mã ca mờ, allowlist, ghép nhãn sau khi đóng dấu đầu ra [REPO `results/T-057/ho-so-g4.md` §1; `src/m1/hop_dong.py`].

### 5.1 Sổ thực nghiệm

- File JSONL **chỉ ghi thêm**, mỗi dòng một sự kiện, có hash nối dòng trước (sửa giữa chừng sẽ lộ).
- Trường mỗi sự kiện tiêm: mã lượt mờ; ô (thành phần gốc × họ lỗi); cơ chế; vị trí tiêm; lệnh đã chạy; thời điểm bắt đầu và kết thúc (UTC, nano giây, đồng hồ chrony); **số đo xác nhận can thiệp** lấy từ đầu dò của bộ tiêm (ví dụ client đo trễ qua Toxiproxy), không lấy từ tín hiệu RCA đọc (B1.9; LESSONS SL18).
- Trường mỗi lượt: digest image, bản agent, cấu hình sampling, lệch đồng hồ (`chronyc tracking`), số drop của cả hai Collector, mức tải và dòng thời gian tải (R-07, R-08, R-10).
- Nơi lưu: máy `exp-obs`, thư mục thuộc user `ledger`, quyền 600. Tiến trình RCA chạy bằng user `rca`, không đọc được. Bản sao về laptop sau mỗi đợt.

### 5.2 Cách dùng

| Chế độ | RCA nhận gì | Lấy từ đâu |
|---|---|---|
| (a) biết mốc | Chỉ `t` (giây nguyên) và mã ca mờ | Bộ điều phối đọc sổ, ghi `case/<mã mờ>.json` = `{t, cửa sổ}`; Q-66, D14 |
| (b) tự phát hiện | Chỉ `t̂` từ luật cảnh báo Grafana | Không đọc sổ (KE-HOACH D.9 "Nhãn") |
| Chấm | Nhãn đầy đủ | Chỉ sau khi đầu ra RCA của cả đợt đã băm và lưu |

### 5.3 Đường rò cần chặn (đặc thù FlashTicket)

| Đường rò | Ví dụ | Chặn |
|---|---|---|
| Log của công cụ tiêm lỗi vào Loki | Log Pumba/Toxiproxy ghi tên service bị tiêm | Collector tại chỗ (trên `exp-app`) loại container của bộ tiêm, k6, Toxiproxy khỏi `filelog` và `docker_stats`; hoặc chạy bộ tiêm trên máy khác |
| Container phụ của Pumba vào metric | `pumba stress` tạo container phụ trong cgroup đích | Lọc theo tên/image ở `docker_stats`; inventory RCA chỉ gồm nút mô hình T-037 |
| Toxiproxy xuất hiện như nút | Địa chỉ đích span JDBC là cổng proxy | Cạnh đã chọn **luôn** đi qua proxy, cả lúc bình thường; nên sự có mặt của proxy không mang thông tin lỗi |
| Annotation Grafana | Đánh dấu "bắt đầu tiêm" trên dashboard | Ghi vào nguồn dữ liệu riêng, bộ đọc RCA không truy vấn; chỉ bật hiển thị sau khi đầu ra đã băm (demo) |
| Tên lượt, tên kịch bản, đường dẫn | Thư mục `run-booking-db-latency-01` | Mã mờ; đưa vào `chuoi_cam` để runner từ chối [REPO `src/m1/adapter.py` docstring] |
| Dòng thời gian tải của k6 | Lịch tăng tải biết trước | Không đưa vào RCA; RCA chỉ thấy tốc độ request ở gateway (quan sát được) |

---

## 6. Kế hoạch từng bước đến 30/12/2026

Ngày là dự kiến. Thời lượng là công của agent và máy, **chưa gồm thời gian chờ Minh duyệt và chờ nhóm hệ thống**; đó là nút thắt thật (KE-HOACH D.13). Mỗi bước có đầu ra ghi vào repo theo SPEC của task tương ứng.

### 6.1 Chặng tới 16/11 (sửa 10/11/2026: thay B0–B3 của bản đầu)

| # | Ai | Ngày | Việc | Xong khi |
|---|---|---|---|---|
| 1 | Minh, AWS console | 11/11 | Máy `3.27.110.61` (`exp-app`): Stop → đổi loại sang `m7i-flex.large` → Start; gắn Elastic IP để IP không đổi | SSH lại được; RAM khoảng 8 GiB |
| 2 | Minh, AWS console | 11/11 | Tạo `exp-obs`: `m7i-flex.large`, cùng VPC, đĩa 100 GB, cùng key. Security Group: SSH từ IP của Minh; hai máy gọi nhau qua IP riêng | SSH được |
| 3 | Minh | 11/11 | Xác nhận Q1 (P-E), Q3 (demo RCA ở đâu) | Có câu trả lời trong chat |
| 4 | Claude | 11/11 | Soạn SPEC T-058 trong chat, kèm danh sách tên biến env cần | Minh duyệt SPEC |
| 5 | Minh | 11–12/11 | Cấp giá trị env theo danh sách | Đủ file env trên `exp-app` |
| 6 | Claude, qua SSH | 11–12/11 | Trên `exp-app`: cài Docker; `git clone` repo FlashTicket ở commit ghim; dựng 4 hạ tầng; kéo 9 image theo digest đang chạy trên 84; chạy bằng `deploy/app/*.yml` và `deploy-service.sh` của nhóm. Chưa có agent | Mọi service UP trong Eureka; luồng đặt vé chạy tới bước tạo thanh toán; không container restart |
| 7 | Claude | 12–13/11 | Gắn agent 2.33.1 bằng cách đặt jar tạm (TS §4.1); chạy kho thử `otel-lgtm` trên `exp-obs` (H0, H1) | Bốn điều của TS §4.1 "Cách kiểm" đạt; Minh mở Grafana thấy trace gateway → booking → DB |
| 8 | Claude | 13–14/11 | Thay kho thử bằng kho ghim phiên bản trên `exp-obs`; chrony; chạy 1 giờ rảnh + 1 giờ tải nhẹ (H2, H5) | Không OOM/restart; RAM trống ≥ 20%; CPU trung bình < 80%; cả hai Collector không rớt dữ liệu; đủ ba tín hiệu ở mọi service; có số RAM và GB/giờ thật |
| 9 | Claude | 14–16/11 | Adapter `ca_flashticket` (TS §4.7); bộ điều phối chế độ (a); 3 sự cố thử (trễ booking→PostgreSQL qua Toxiproxy; `pause` ticket-service; `stress` một service) + 1 cửa sổ không lỗi, ở tải thấp cố định | M1 bản P7 khóa ra xếp hạng ở 4/4 cửa sổ; kiểm trường cấm đạt; gói và đầu ra có hash. **Không** là đánh giá |

- **Tên cũ còn dùng ở các mục khác:** B0 = bước 1–5; B1 = bước 6–7; B2 = bước 8; B3 = bước 9.
- **Cách dựng `exp-app` giống cách cũ của Minh, khác một bước.** Vẫn SSH và lấy repo về máy; nhưng **không build trên server**: kéo image CD đã build, theo đúng digest trên 84 (`/opt/flash-ticket-app/state/<svc>.current`). Không viết compose mới cho ứng dụng; dùng lại file của nhóm để máy thực nghiệm giống 84 tới từng tham số [CODE `deploy/app/README.md`, `deploy/scripts/deploy-service.sh`].
- **Kho thử đặt ở `exp-obs` ngay từ đầu**, không đặt trên `exp-app`, để máy ứng dụng chỉ chạy ứng dụng.
- **Ba sự cố thử ở bước 9 chỉ cần đổi env, không cần sửa code.** Phần code Q6 của Minh (cờ lỗi, VNPay mock, `hostId`, đưa jar agent vào image) chạy song song và cần xong cho B4.
- **Local.** Laptop chỉ viết cấu hình và điều khiển qua SSH; không chạy toàn hệ thống. Local chỉ cần khi Minh sửa code Java ở Q6: biên dịch, chạy test của service đó (`mvnw verify`), rồi merge để CD build.
- **Đường lùi.** Agent lỗi → thử minor liền trước; vẫn lỗi → phương án starter (sửa pom, TS §4.1). RAM `exp-obs` thiếu → giảm retention; vẫn thiếu → máy lớn hơn (Q11). Thiếu trace → chạy với metric, log và ghi giới hạn. Trễ → 16/11 chỉ 1 sự cố.
- **Chưa kiểm:** agent với Spring Boot 4.1.1; Docker trên Ubuntu 26.04; kéo image từ GHCR trên `exp-app`. Mốc 16/11 cần bước 1–5 xong trong 11–12/11.

### 6.2 Từ B4 tới 30/12

| Bước | Ngày | Việc | Vào khi | Ra khi (cách kiểm) | Đường lùi | Ước lượng, giả định |
|---|---|---|---|---|---|---|
| **B4** Danh mục kịch bản, bộ tiêm, sổ, nền, kiểm telemetry | 17–24/11 | Danh mục khai trước theo KE-HOACH D.9 (vị trí × họ lỗi, ≥ 2 vị trí khi có); sổ §5; lượt nền qua đêm; kiểm R-01–R-10 | B3 đạt; nhóm hệ thống làm song song: cờ lỗi, VNPay mock, chuỗi kết nối qua Toxiproxy, `hostId` | Bảng ô hữu hiệu; báo cáo chất lượng telemetry; 2 đêm nền đạt | Nhóm chưa kịp cờ lỗi → bắt đầu bằng lỗi container và Toxiproxy, khai phần thiếu | 4–5 ngày; 2 × 8 giờ máy |
| **B5** Đợt phát triển, thích nghi M1, baseline trên FlashTicket, khóa bản FlashTicket | 25/11–4/12 | Lượt phát triển (tải tăng không lỗi; lỗi ở tải cố định; cùng lỗi ở tải khác); thử thành phần dùng thông tin phong phú (B1.9); adapter baseline (SimpleRCA, BARO và các phương pháp hỗ trợ được); luật cảnh báo Grafana (M-38) | B4 đạt | Bản FlashTicket khóa bằng commit được Minh duyệt; bảng chuyển giao điền đủ | Không thành phần nào giúp → khóa bản P7 làm bản FlashTicket, báo trung thực | 8–10 ngày; chi phí máy OPEN (KE-HOACH D.9) |
| **B6** Demo | 1–9/12 | Đóng băng môi trường demo; kịch bản demo có script; video; phát lại offline từ gói đã lưu | Bản FlashTicket khóa (hoặc bản P7 nếu B5 trễ) | Diễn tập 2 lần không lỗi; video có sẵn | Lỗi mạng ngày demo → phát lại offline + video | 3–4 ngày; ngày demo [CHƯA BIẾT] |
| **B7** Đợt đánh giá | 5–13/12, chạy đêm | Lượt mới sau khóa, theo danh mục; chạy song song hai bản môi trường (TK-B, TK-C) để giảm thời gian thực | Bản khóa; Minh duyệt lượt dài (luật 8, 21) | Đủ ô đã khai; drop = 0 hoặc đã ghi; gói đã băm | §7 | 40–60 giờ máy, tức 3–4 đêm (KE-HOACH D.9); chia đôi nếu song song |
| **B8** Chấm, phân tích, hồ sơ G6, quyển | 14–30/12 | Chấm theo B1.9 và D14 (ba bản); phân tích theo ô và theo ca; phản biện chéo G6 (MRP §7) | B7 xong | Hồ sơ G6 được duyệt; quyển nộp 30/12 | Thiếu thời gian → báo RQ5 phần đã có, khai phần thiếu | 10–14 ngày |

**Ghi chú về agent và local (sửa 10/11/2026).** Agent gắn qua biến `JAVA_TOOL_OPTIONS`, không sửa code Java, không sửa pom (TS §4.1). Vì vậy bước 6–7 chạy thẳng trên `exp-app` bằng image đã build; **không chạy toàn bộ hệ thống ở laptop**. Local (IntelliJ) chỉ dùng cho phần Minh tự phát triển ở Q6 (cờ lỗi, VNPay mock, `hostId`): đó là sửa code, cần biên dịch và chạy test trước khi merge. Minh nêu 10/11: luật 19 không cản việc phát triển và thử tích hợp ở local; luật 19 nói về tính toán nặng, chạy dài.

**Đường găng tới 16/11.** Bước 1–5 của §6.1 (việc của Minh và SPEC) → bước 6 → 7 → 8 → 9. Môi trường thực nghiệm **không** qua CD, nên không cần sửa repo FlashTicket để đạt 16/11; compose riêng của môi trường thực nghiệm sẽ nằm ở repo RCA nếu SPEC cho phép (§10). Rủi ro lớn nhất: bộ env (mật khẩu DB, client secret Keycloak, key-ring QR của ticket) [CODE `deploy/app/README.md`].

**Phụ thuộc và song song (luật 12).**
- Phần code Q6 của Minh (cần cho B4) chạy song song từ ngày 11/11.
- Viết adapter (B3) bắt đầu ngay khi B1 có trace mẫu, không chờ B2 xong hẳn.
- B6 chồng lên cuối B5; B7 chạy đêm, B6 làm ban ngày.

---

## 7. Lượt dài: gặp lỗi giữa chừng (luật 21)

Thiết kế mặc định: **thu dữ liệu trước, chạy RCA sau** trên gói đã đóng. Lỗi của phương pháp vì vậy không bao giờ buộc thu lại dữ liệu.

- Mỗi chu kỳ sự cố (khoảng 30 phút, KE-HOACH D.9) độc lập: nền → tiêm → hồi phục → đóng gói → băm.
- Sau mỗi chu kỳ, kiểm tự động: drop của Collector, OOM/restart, lệch đồng hồ, đủ ba tín hiệu ở mọi service.

| Lỗi ở | Loại | Xử lý | Chạy lại gì | Mất bao lâu [TÍNH] |
|---|---|---|---|---|
| 10% | Hạ tầng (máy dừng, Collector rớt dữ liệu) | Đánh dấu chu kỳ `INVALID_INFRA`, giữ gói; sửa; chạy tiếp | Chỉ chu kỳ hỏng, thêm vào cuối hàng | ≈ 30–45 phút |
| 50% | như trên | như trên | như trên | như trên |
| 99% | như trên | như trên | như trên | như trên |
| Bất kỳ | Lỗi hệ thống (sai digest, sai sampling, lệch đồng hồ lớn) | Dừng cả đợt; báo Minh | Mọi chu kỳ bị ảnh hưởng, trình Minh lý do và chi phí trước (luật 21) | Tới 40–60 giờ máy |
| Bất kỳ | Lỗi phương pháp RCA (chưa phân loại) | Chỉ chặn slot đó; dữ liệu giữ nguyên | Chỉ chạy lại RCA trên gói, không thu lại | Phút |

Giảm rủi ro lỗi hệ thống: một **đêm thử** (2–3 chu kỳ mỗi họ lỗi) ở cuối B4 trước đợt phát triển, và ở đầu B7 trước đợt đánh giá. Quét trước điều kiện suy biến đã biết của M1 và baseline trên gói thử: dưới 2 span bình thường, operation mới (LESSONS SL38).

---

## 8. Rủi ro

| Rủi ro | Dấu hiệu sớm | Phương án |
|---|---|---|
| Không có bộ env riêng | B1 không vào được | Agent liệt kê tên biến cần; Minh cấp giá trị (Minh 10/11: "cần thì bảo tôi lấy") |
| Agent lỗi với Boot 4.1.1 | B1 | TS §7 |
| Nhóm deploy lên 84 khi đang demo | Lượt CD mới | Đóng băng digest demo; báo nhóm lịch demo |
| ngrok chung domain giữa 84 và môi trường thử | Payment lỗi callback | Môi trường thử dùng VNPay mock, không chạy ngrok |
| Cổng 6379, 5672, 15672 mở ra internet trên 84 | SG cho phép | Minh kiểm SG (Q12) |
| `netem` không cô lập do host network | Thử ở B4 | Thay bằng Toxiproxy hoặc cờ chậm trong code; khai cơ chế khác |
| Ổ D laptop còn 12,7 GB | Lưu gói thất bại | Lưu gói ở ổ C |
| Rò nhãn qua log/metric của công cụ tiêm | Kiểm `chuoi_cam`, lọc Collector | §5.3 |

### 8.1 Nginx làm cửa vào (thêm 10/11/2026; việc của hệ thống)

- Repo cũ có nginx cổng 80 chia `/` (frontend), `/api/` (gateway), `/auth/` (Keycloak). Repo mới chỉ có nginx trong image frontend để trả file tĩnh; máy 84 không có reverse proxy [CODE; MÁY 10/11].
- Minh muốn dùng lại nginx. Thêm sau 16/11, **chốt trước khi khóa bản FlashTicket (B5)**, vì nó thêm một nút ở đầu vào đồ thị.
- Ảnh hưởng CD nhỏ nếu nginx là thành phần riêng và cổng các service giữ nguyên: CD kiểm sức khỏe bằng `127.0.0.1:<cổng>`, không qua nginx [CODE `deploy-service.sh`]. Chỗ phải đổi: biến `VITE_*` rồi build lại frontend; `KC_HOSTNAME`, redirect URI của Keycloak, CORS của gateway; một dòng health check Keycloak trong `deploy-service.sh` nếu đặt Keycloak dưới `/auth`.

---

## 9. Điểm chờ Minh quyết (kèm đề xuất)

| # | Câu hỏi | Đề xuất của Claude | Vì sao | Mặt trái | Phương án khác đã xét |
|---|---|---|---|---|---|
| Q1 | Phương án triển khai | **P-E** | Nhiễu đo thấp; không làm phiền demo của nhóm; dựng bản sao song song được | Ba máy, vận hành nhiều nhất | P-B nếu thiếu quota; P-C nếu chấp nhận lên Paid; P-F (§3) |
| Q2 | Thông tin 3 tài khoản | Không cần nữa (sửa 10/11): Minh xác nhận đủ tiền, đủ hạn. Chỉ còn quota vCPU là giới hạn kỹ thuật; gặp thì xin tăng | Minh trả lời 10/11 | — | — |
| Q3 | Demo phần RCA chạy ở đâu | Trên môi trường thực nghiệm đã đóng băng; máy 84 giữ chức năng bán vé | 84 không đủ RAM cho agent + kho | Demo đi qua hai môi trường | Nâng 84 lên `m7i-flex.large` và cài kho trước demo |
| Q4 | Đưa dữ liệu ra ngoài (Grafana Cloud) | **Tạm hoãn** (Minh 10/11). Bản đề xuất cũ: chưa dùng tới sau 16/11; không bao giờ làm nguồn chấm; nếu dùng thì chỉ bản sao đã lọc của dữ liệu thử | Không cần cho RCA bản đầu; tránh rủi ro dữ liệu | Mất Knowledge Graph, Assistant làm đối chứng định tính | Dùng ngay theo M-36. **Mâu thuẫn nguồn:** KE-HOACH E-11 ghi "dùng, không đắn đo" (M-36, 22/10); prompt 10/11 ghi "chưa quyết". Minh xác nhận cái nào hiện hành |
| Q5 | Cách ghi và dùng mốc tiêm | Theo §5 | Khớp cách T-054 đóng dấu rồi ghép nhãn; chặn đường rò riêng của FlashTicket | Thêm user, quyền, bộ điều phối | Bộ tiêm chạy ở máy riêng (đơn giản hơn về quyền, thêm máy) |
| Q6 | Việc phía hệ thống (TS §4.8: agent, env riêng, `hostId`, cờ lỗi, VNPay mock, chuỗi kết nối qua Toxiproxy; cùng R-01–R-10) | **Minh tự làm, không chờ nhóm hệ thống** (Minh 10/11). Agent của repo RCA vẫn chỉ đọc repo FlashTicket (AGENTS §12) | Bỏ phụ thuộc thời gian của nhóm | Việc dồn về Minh | Gửi nhóm hệ thống (bản đề xuất cũ); chỉ dùng lỗi container, khai phạm vi hẹp |
| Q7 | Định nghĩa "RCA bản đầu" 16/11 | B3: M1 bản P7 chạy thẳng trên 3 sự cố thử + 1 cửa sổ không lỗi; không là đánh giá | Đo được, kịp 7 ngày | Chưa nói gì về hiệu quả | Một sự cố duy nhất (nhanh hơn, ít thông tin) |
| Q8 | Mã task và vai trò | T-058 "Hạ tầng quan sát và RCA bản đầu FlashTicket" (B1–B3); T-059 "Kịch bản, tiêm lỗi, sổ, nền" (B4); T-060 "SPEC P10: đợt phát triển và đánh giá" (B5–B8). Người làm và người phản biện khác nhau, Minh chọn | STATE ghi T-058 dự kiến cho P8 nhưng P8 đã hoãn; LOG T-057 từng đề xuất "T-058 = bộ đọc FlashTicket" | Nếu giữ T-058 cho P8 thì đánh số từ T-059 | Một task lớn (khó phản biện, khó bàn giao) |
| Q9 | Mức tải chiến dịch RCA | ≤ 50 request/giây, trace 100%; lượt NV1 tải cao chạy riêng, có lấy mẫu | Dung lượng §2.2; KE-HOACH D.8.7 mục 3 | Chưa thử tải cao với RCA | Một mức tải duy nhất |
| Q10 | Giới hạn CPU từng container ở môi trường thử | Có, ghi trong manifest | Lỗi CPU cô lập được theo service | Khác cấu hình máy 84; kết quả NV1 phải tách | Không giới hạn, khai "tài nguyên chung" |
| Q11 | Lên gói Paid | Chưa cần; lên khi số đo ở B2 cho thấy cần máy > 8 GiB | `m7i-flex.large` là loại mạnh nhất của gói Free [WEB; TS §1.6] | — | Paid cho một tài khoản làm P-C. Minh 10/11: "sau này có thể sẽ cân nhắc paid để dùng instance cao hơn" |
| Q12 | Security Group máy 84 | Minh kiểm inbound; chỉ để SSH (IP Minh), cổng frontend/gateway/Keycloak cần cho người dùng; đóng 6379, 5672, 15672 nếu đang mở | Các cổng này nghe trên `0.0.0.0` [MÁY `ss -ltn`] | Có thể đang có người dùng hợp lệ | Để nguyên và ghi rủi ro |
| Q13 | Nơi lưu compose và script của môi trường thực nghiệm (áp dụng ngay từ T-058, bước B1) | **Chia theo bản chất file** (sửa 10/11). Repo FlashTicket, Minh ghi: compose chạy FlashTicket, cấu hình agent, chuỗi kết nối qua Toxiproxy, cờ lỗi, kho quan sát theo B16. Repo RCA, agent ghi theo "Phạm vi ghi" của SPEC: sổ tiêm lỗi, script tiêm lỗi, bộ đọc và runner RCA, manifest ghim digest | Cách chạy hệ thống thuộc hệ thống; phần tiêm lỗi, nhãn và RCA phải tách khỏi hệ thống (§5) | Hai repo cùng phải khớp phiên bản; ghi commit của cả hai trong manifest mỗi lượt | Tất cả ở repo RCA (bản đề xuất cũ); chỉ để trên máy (mất khi xóa máy) |

### 9.1 Trả lời của Minh ngày 10/11/2026 (trong chat; đã ghi `docs/DECISIONS.md` cùng ngày)

| # | Lời Minh | Trạng thái |
|---|---|---|
| Q1 | "tôi thấy (P-E) hợp lý ... sau khi nghe bạn giải thích" | Hiểu là chọn P-E; chờ Minh xác nhận nếu hiểu sai |
| Q2 | "Q2 không cần quan tâm, chỉ cần agent hiểu là đủ làm đến khi hết đồ án là được"; "đủ tiền đủ hạn để làm nên tôi không muốn nhắc đến vấn đề sợ không đủ dùng nữa, mạnh dạn đề xuất" | Đã trả lời |
| Q3 | Chưa trả lời riêng. Thông tin liên quan: "84 chỉ là tạm thời, sau này có thể sẽ cân nhắc paid để dùng instance cao hơn" | Còn mở; đề xuất giữ nguyên |
| Q4 | "grafana cloud nếu không có tác dụng nhiều thì cứ tạm hoãn" | Tạm hoãn |
| Q5 | "đồng ý đề xuất" | Đồng ý |
| Q6 | "tôi sẽ làm cái này, không đợi nhóm hệ thống" | Minh làm |
| Q7 | "đồng ý" | Đồng ý |
| Q8 | "đồng ý" | Đồng ý: T-058, T-059, T-060 |
| Q9–Q12 | "đồng ý đề xuất nhưng không yêu cầu cứng, có thể thay đổi" | Đồng ý, không cứng |
| Q13 | Hỏi lại "file compose sao không đặt trong code, thư mục hệ thống flash ticket mà lại đề xuất đặt ở RCA"; sau đó duyệt gói sửa plan có đề xuất chia nơi lưu | Theo đề xuất đã sửa ở bảng trên |

Ghi chú của Minh cùng ngày: env và mật khẩu của máy 84 không là trở ngại, "cần thì bảo tôi lấy, đồ án chung chứ không phải private".

**Đề xuất dòng cho file điều hành (chưa ghi, chờ duyệt):**
- `docs/STATE.md`, mục "Việc kế tiếp": "Đề xuất techstack và kế hoạch triển khai FlashTicket: `docs/techstack/` (10/11/2026, chưa duyệt). Chờ Minh trả lời Q1–Q13 của PLAN §9."
- `docs/DECISIONS.md`: một dòng cho mỗi câu Minh trả lời ở §9, theo lời Minh.
- `docs/WHY.md`, ba mục mới khi Minh duyệt: "Vì sao dùng OTel Java agent thay starter Spring" (TS §4.1); "Vì sao tách môi trường thực nghiệm khỏi máy demo" (§3); "Cách ghi mốc tiêm và chặn rò nhãn trên FlashTicket" (§5).
- Luật 3 của AGENTS: lựa chọn quan trọng phải có mục WHY trước khi dùng trong kết quả. Ba mục trên cần có trước B3.

---

## 10. Bước tiếp theo

1. Minh làm bước 1–3 của §6.1 (đổi loại máy, tạo `exp-obs`, xác nhận Q1 và Q3).
2. Claude soạn SPEC T-058 trong chat, gồm "Phạm vi ghi" (sổ, script tiêm lỗi, adapter, manifest digest ở repo RCA) và danh sách tên biến env; Minh duyệt rồi mới tạo file (Luật 0).
3. Minh cấp giá trị env; Claude làm bước 6–9.
4. Minh gửi phản biện hai file này bằng prompt ở Phụ lục A nếu muốn.

---

## Phụ lục A. Prompt cho agent phản biện (Minh quyết gửi hay không)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: đề xuất ngoài task, chưa có mã: docs/techstack/TECHSTACK-NGHIEN-CUU.md và docs/techstack/PLAN-TRIEN-KHAI.md.
- Công đoạn: soát kết quả.
- Gói/cổng: ngoài task; chuẩn bị triển khai FlashTicket làm nguồn dữ liệu cho P9, P10 (MRP §5, §7).
- Người làm và người phản biện chính thức: người làm Claude; người phản biện dự kiến là agent nhận prompt này.
- Tài liệu gốc: docs/MRP.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/STATE.md; docs/KE-HOACH-GIAI-DOAN-TOI.md; results/T-040/yeu-cau-quan-sat-p9.md; results/T-043/hop-dong.json; tasks/T-043-thiet-ke-rca-m1/SPEC.md (B1.9); results/T-057/ho-so-g4.md; src/m1/adapter.py; repo FlashTicket D:/Project/flash-ticket-platform (chỉ đọc, commit 1d40c97).
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: máy 52.64.237.84 (chỉ đọc; cách truy cập ở docs/STATE.md, mục lưu ý truy cập máy demo); không có lượt chạy hay manifest cho đề xuất này.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.
```

Không có khối trọng tâm cổng tương ứng: đề xuất này nằm ngoài các cổng G0–G4 đang có trong `docs/review-prompt.md`.
