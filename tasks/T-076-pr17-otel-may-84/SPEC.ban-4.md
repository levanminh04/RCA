# T-076 — Làm lại PR #17 trên main mới nhất; FlashTicket mới chạy cho demo trên Oracle; mở đường quan sát máy 84

- **Trạng thái:** đề xuất bản 4 (27/11/2026). Minh duyệt hướng H1 + H4 ngày 27/11 ("Duyệt hướng H1 + H4, viết SPEC bản 4"). Bản cũ: `SPEC.ban-1.md`, `SPEC.ban-2.md`, `SPEC.ban-3.md` (bản 3 Minh đã duyệt 26/11; bản 4 thay hướng triển khai, giữ phần đã làm). Chờ Minh duyệt bản 4.
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P9 (kho quan sát và tích hợp), P10 (thực nghiệm trên FlashTicket và demo) — **Cổng:** ngoài G0–G4 (tích hợp, không đánh giá phương pháp)

## Mục tiêu

**Nguồn:** DT18-NV1 (hệ thống bán vé phân tán), DT18-NV2 (thu log, trace, metric; `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` §2), MRP P9a (chuẩn B16, `service.name` thống nhất ba tín hiệu), MRP P10 (thực nghiệm và demo trên FlashTicket).

**Mong muốn của Minh:**
- 24/11: Y11 toàn quyền phần quan sát của FlashTicket, miễn không ảnh hưởng hệ thống; Y12 dùng bản mới nhất cho thống nhất.
- 26/11: không sửa tay trên máy 84; dọn chỗ lỗi thời của PR #17; **chỉ một PR** (làm lại chính PR #17).
- 27/11: chọn H1 + H4. **Demo phải chỉn chu.** **Thiết kế mở:** sau này chuyển sang quan sát máy 84 (AWS) thì chỉ **thêm**, hoặc sửa nhỏ (IP, cổng, thông tin kết nối); không xóa, không đổi cấu trúc thư mục.

**Task này gồm hai phần:**
- **Phần A — PR #17:** đưa chuẩn quan sát B16 vào main mới nhất của nhóm. Agent có sẵn trong image nhưng **tắt**. Máy 84 chưa gửi dữ liệu quan sát đi đâu (H1).
- **Phần B — exp-app cho demo:** dựng lại bản FlashTicket thử nghiệm trên exp-app (Oracle) từ main mới nhất có PR #17, kiểm tín hiệu, sẵn sàng demo trọn vòng tải → sự cố → cảnh báo → RCA (H4).

**Không thuộc task (giai đoạn sau, mục "Mở rộng sang máy 84"):** bật quan sát cho máy 84. Bị chặn bởi RAM của cụm và việc triển khai Collector qua CD của nhóm (số liệu dưới).

Task không đánh giá phương pháp RCA, không đổi phương pháp. Phần B đổi bản FlashTicket được đo trên exp-app (xem C5).

## Hiện trạng đã kiểm (26–27/11/2026, chỉ đọc trừ phần ghi rõ)

| Điều | Thực tế | Nguồn |
|---|---|---|
| Main, PR | `origin/main` `f178870`; PR #17 `bb84d64` OPEN, CONFLICTING, 124 file, 13 xung đột | `git`, `gh` (LOG phiên 4) |
| Bảng file PR | Giữ 93 / sửa 17 / bỏ 14; Minh duyệt 26/11 | `results/T-076/bang-file-pr17.md` |
| Nhánh dựng lại | Local `rca/quan-sat-log-dung-lai` (worktree `D:/Project/ft-pr17-dung-lai`), 6 commit trên `f178870`, chưa push. Commit cuối `ae5a870` theo bản 3 (CA, địa chỉ obs trong ConfigMap) | LOG phiên 4 |
| Kiểm cục bộ bản 3 | 8/8 `verify`, 7/7 kiểm B16 đạt; Event `-P rca-test` đạt; **Booking `-P rca-test` 67 error** (3 lớp `@WebMvcTest` thiếu bean `RcaFaults`; có từ `bb84d64`, T-067 ghi 68 error + 1 failure); image đúng (uid, entrypoint, checksum agent, `SERVICE_VERSION`) | `results/T-076/kiem-cuc-bo/README.md` |
| Agent gửi gì (Collector thử không processor) | Lộ query ở `url.query` span SERVER và exemplar metric; không lộ header Authorization/Cookie, body, client secret; SQL đã sanitize; `exception.message` có trong event span. Khóa `…sanitization.url.experimental.sensitive-query-parameters` che tham số có tên trong danh sách; `OTEL_METRICS_EXEMPLAR_FILTER=always_off` bỏ exemplar | như trên, §3 |
| Bộ nhớ (giới hạn 768 MiB) | Booking 381 → 499 MiB khi bật agent; Assistant 348 MiB | như trên, §4 |
| VNPay | `GET /api/v1/payments/vnpay/return` và `/ipn` nhận tham số `vnp_*` ở query (B16 §6 cấm lưu toàn nội dung callback) | `PaymentController.java:52,59` @nhánh |
| Tham số query của các service | Phần lớn vô hại (`size`, `cursor`, `page`, `status`…); cần che: `q` (tìm tự do) và 28 tên `vnp_*` | `grep @RequestParam`, `"vnp_…"` @nhánh |
| Cụm máy 84 | K3s 3 node: `ft84` 7,6 GiB (dùng 55%; kèm Postgres, Mongo, RabbitMQ, Redis trong Docker), `server-1` 1,9 GiB, `server-2` 3,7 GiB (dùng 83%, limits 115%). Chưa bật agent: booking 654/768, payment 689/768, event 456/512 MiB. Đĩa `ft84` 88% | SSH chỉ đọc 27/11 (LOG phiên 4) |
| CD của nhóm | Chỉ build `maven`/`node` từ mã nguồn; không có đường triển khai image dựng sẵn (Collector). `deploy-k8s-service.sh` có danh sách service cố định và kiểm Eureka | `_deploy-service.yml`, `deploy-k8s-service.sh` @main |
| exp-app | Bản ghim `36a3725d` (T-067). Dựng từ `deploy/app/<svc>.yml` của nhóm + file phủ lab; main vẫn có đủ 7 file đó (thêm `frontend.yml`, `keycloak.yml`; không có Assistant). `build.sh` build 7 service, Booking/Event `-P rca-test` | lab `test-environment/`, main `deploy/app/` |
| Obs | CA và chứng chỉ máy nhận đã tạo 27/11 ở `/etc/flashticket-rca/production/` (root 600); script `observability/tls/tao-chung-chi.sh` và `ca.crt` ở lab (chưa commit) | LOG phiên 4 |

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Lựa chọn | Phép kiểm | Còn mở |
|---|---|---|---|
| **C1.** PR #17 giữ gì (đã chốt) | Theo bảng đã duyệt | Đã có | — |
| **C2.** Cấu hình agent trong PR thế nào để sau này chỉ cần thêm? | **Đích gửi là Collector trong cụm**: `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318` (tên Service K8s sẽ thêm ở giai đoạn sau; agent tắt nên chưa ai gọi). Giữ `ENVIRONMENT=production`, `HOST_ID` = tên node (downward API), lấy mẫu 10%, metric `otlp`, log `none`, khóa log `traceId`/`spanId`, Lettuce/RabbitMQ như đã làm. **Thêm:** `OTEL_METRICS_EXEMPLAR_FILTER=always_off`; lớp che đầu tiên ở nguồn `…SENSITIVE_QUERY_PARAMETERS` = `q` + 28 tên `vnp_*`. **Bỏ:** `OTEL_CA_PEM_B64` trong ConfigMap, khối CA trong entrypoint, khóa token trong file mẫu Secret (TLS và token sẽ nằm ở Collector, không ở từng pod). File mẫu Secret giữ một khóa `OTEL_AGENT_ENABLED` (công tắc) | Bước 4: Collector thử tên `otel-collector`, không TLS, không processor: agent bật gửi được; tham số trong danh sách thành `REDACTED`; không có exemplar; agent tắt: không có kết nối OTLP (log agent không xuất hiện) | Danh sách chặn theo tên chỉ là lớp đầu; lớp lọc chính (xóa query, `exception.message`) đặt ở Collector khi mở rộng sang máy 84, giống exp-app |
| **C3.** Lỗi Booking `-P rca-test` (Q1) | Sửa trong PR: `RcaFaultsWebConfig` không bắt buộc có bean `RcaFaults` (bỏ qua đăng ký khi bean không có, chỉ xảy ra trong test slice) | `-P rca-test verify` Booking 0 error; build production không chứa lớp `rca-test`; test hook hiện có vẫn đạt | — |
| **C4.** PR có ảnh hưởng máy 84 khi merge không? | Agent tắt: không có overhead agent. Thay đổi chạy thật: log JSON B16, `ENVIRONMENT`/`HOST_ID` trong log | Sau merge (chỉ đọc máy 84): pod Ready, 0 OOM/restart trong 60 phút; bộ nhớ từng pod không tăng quá mức Q7 so với số đo 27/11; log có `environment=production`, `hostId` = tên node | — |
| **C5.** Đổi exp-app sang bản mới ảnh hưởng gì? (Q5) | Đổi hệ thống được đo. Kết quả cũ trên `36a3725d` (T-069 hồi quy V082, ngưỡng cảnh báo T-072 chọn trên E2) không so thẳng với bản mới. Bản cũ giữ nguyên image để hoàn tác | Bước 9: kiểm tín hiệu như Q4 T-070; một lượt nền ×1 ngắn để xem p95 từng route so với ngưỡng T-072 (cảnh báo không cháy sẵn khi khỏe); hồi quy V082 hai ca dev (dữ liệu cũ, code RCA không đổi) | Nếu p95 bản mới lệch ngưỡng: cảnh báo cho demo cần chọn lại ngưỡng (việc của T-072, trình Minh) |
| **C6.** Demo cần gì để chỉn chu? (Q6) | Đề xuất kịch bản: tải k6 ×1 → tiêm một ô lỗi đã dùng (ví dụ `PAUSE-PAYMENT`) → cảnh báo tới bộ nhận → RCA trực tuyến → dashboard sự cố và đồ thị dịch vụ. Frontend: không đưa vào (bản build gắn cứng URL máy 84, KP-02 T-058) trừ khi Minh cần | Bước 10: diễn tập một vòng, ghi thời gian từng mốc | Bật lại RCA trực tuyến và bộ chuỗi tải cần lab `c1da15f` đã qua Codex kiểm (T-070 REVIEW-5) |

## Đầu vào

- Repo FlashTicket `D:/Project/flash-ticket-platform` và worktree `D:/Project/ft-pr17-dung-lai`; chốt `origin/main` và đầu `origin/rca/quan-sat-log` lúc push.
- Repo lab `D:/Project/flashticket-rca-lab` @ main hiện tại (`c1da15f`).
- Chuẩn B16; kết quả T-067, T-069, T-070 (Q4), T-072, T-073; `results/T-076/`.
- Đọc máy: `results/T-070/kiem-ke/tho/lenh/ssh.sh` (exp-app, obs, máy tải); máy 84 chỉ đọc bằng `plink` như LOG phiên 4.
- Không đọc dữ liệu khóa. Không sửa gì trên máy 84.

## Đầu ra

- **PR #17 làm lại** (một PR): nhánh `rca/quan-sat-log` đẩy đè bằng `--force-with-lease` khớp đầu nhánh đã soát. Mô tả PR có bảng giữ/bỏ, nói rõ agent tắt, cách mở rộng sau.
- `results/T-076/kiem-cuc-bo/` (đã có lượt bản 3; thêm lượt bản 4).
- `results/T-076/sau-merge/`: kiểm C4 trên máy 84 (chỉ đọc).
- `results/T-076/exp-app/`: build, triển khai, kiểm tín hiệu, lượt nền, hồi quy V082, diễn tập demo (Phần B).
- `results/T-076/mo-rong-may-84.md`: danh sách việc **thêm** khi chuyển sang quan sát máy 84 (mục dưới, kèm số liệu RAM).

## Phạm vi ghi

Ngoài `LOG.md` của task và dòng T-076 trong `docs/STATE.md`:
- `results/T-076/`.
- **Repo FlashTicket:** chỉ nhánh `rca/quan-sat-log` (ngoại lệ `AGENTS.md` §12 đã ghi); nhánh local tạm `rca/quan-sat-log-dung-lai` và worktree của nó. Commit `ae5a870` (bản 3, chưa push) được thay bằng commit theo bản 4.
- **Repo lab:** `observability/tls/` (đã có, giữ cho giai đoạn sau); `test-environment/` chỉ khi bản mới cần (file phủ, `build.sh`, `deploy.sh`), trình diff trước khi dùng. Không sửa `rca/`, `observability/collector/`, `observability/prometheus/`, luật cảnh báo.
- **exp-app:** build image mới (worktree mới dưới `/opt/flashticket/build/`), triển khai bằng `deploy.sh`, giữ image và cấu hình cũ để hoàn tác. Mỗi lần dừng/đổi service trên exp-app: Minh duyệt lúc làm.
- **Máy 84:** không ghi gì. **Obs:** không ghi thêm trong task này.
- **Ngoài quyền agent, Minh làm:** merge PR, báo nhóm hệ thống.

## Các bước

**Phần A — PR #17**
1. ✔ Bảng file (Minh duyệt 26/11).
2. ✔ Dựng lại nhánh (5 commit: log B16, `rca-test`, CI, agent, GOV).
3. **K8s theo C2:** thay commit `ae5a870` bằng commit mới: ConfigMap 7 service (khối agent theo C2), `HOST_ID` trong 7 `deployment.yaml` (giữ), file mẫu Secret chỉ `OTEL_AGENT_ENABLED`, entrypoint bỏ khối CA, Assistant (giữ), README quan sát (hiện trạng agent tắt + mục mở rộng). Kiểm bằng bộ kiểm K8s của nhóm (`test-k8s-*.py`).
4. **Sửa lỗi `rca-test` (C3)** và **kiểm cục bộ lại** bằng bộ script đã có (`chay-verify.sh`, `build-image.sh`, `chay-agent.sh` với Collector tên `otel-collector`): đủ phép kiểm C2, C3.
5. Push có lease; CI GitHub; Codex soát PR (khối Soát kết quả); Minh đọc theo hướng dẫn review (44 file Java ngoài test).
6. Minh merge. CD tự triển khai.
7. **Sau merge (C4)**, đọc máy 84 trong 60 phút, ghi `results/T-076/sau-merge/`.

**Phần B — exp-app cho demo** (bắt đầu sau khi Minh quyết Q5)

8. Kiểm trước, chỉ đọc: diff `deploy/app/*.yml` main mới so với `36a3725d`; dựng cấu hình hiệu lực bằng `hieu_luc.py` với file phủ lab; ước lượng thời gian dừng; trình Minh.
9. Build ARM trên exp-app từ commit merge (`build.sh`, Booking/Event `-P rca-test`), triển khai (`deploy.sh`), kiểm tín hiệu như Q4 T-070, lượt nền ×1 ngắn, hồi quy V082 hai ca dev (C5). Ghi bản ghim mới.
10. Diễn tập demo một vòng theo C6, ghi mốc thời gian; danh sách lệnh chạy demo trong `results/T-076/exp-app/demo.md`.

## Mở rộng sang máy 84 (giai đoạn sau, không làm trong task)

Thiết kế ở Phần A để giai đoạn này **chỉ thêm**:

| Thêm | Ở đâu |
|---|---|
| Collector 1 pod (Deployment + Service tên `otel-collector`, ConfigMap cấu hình): nhận OTLP trong cụm, lọc như exp-app (`filter/health`, `transform/sanitize` — xóa query; thêm bỏ `exception.message`), nén, gửi sang obs qua TLS + token, hàng đợi gửi lại | FlashTicket `deploy/k8s/otel-collector/` (thư mục mới) |
| CD triển khai được image dựng sẵn: khai trong `.github/services.json`, một nhánh "image" trong `_deploy-service.yml`, tên Collector trong danh sách và quy tắc kiểm (không Eureka) của `deploy-k8s-service.sh`, bộ kiểm CD | FlashTicket `.github/`, `deploy/scripts/` (nhóm duyệt) |
| Token gửi obs | Secret của Collector (file mẫu mới trong `deploy/k8s/examples/`) |
| Đường nhận trên obs: Collector + Prometheus riêng, datasource và dashboard chạy thật, mở tường lửa cho IP máy 84 | Lab `observability/` (file mới); CA đã có |
| Bật agent | Thêm `OTEL_AGENT_ENABLED=true` vào `ENV_<SVC>` + CD `restart` từng service |

**Sửa nhỏ duy nhất:** nâng giới hạn bộ nhớ trong `deployment.yaml` của service bật agent (đo 27/11: agent thêm ~118 MiB; booking, payment, event đã sát trần) — cần nhóm quyết RAM cụm (`server-2` đã 83%). Phí AWS: lượng gửi ra Internet tính phí; ước lượng và kiểm hạn mức miễn phí trên tài khoản nhóm khi đó (**chưa kiểm**).

## Kiểm đúng đắn

- **Không đổi phương pháp:** `src/m1`, `src/m1_ft`, `src/p3`, bản chụp `b0f79a4d…`, lab `rca/` không đổi. Hồi quy V082 hai ca trùng byte ở bước 9.
- **Máy 84 không gửi dữ liệu:** agent tắt mặc định; kiểm ở bước 4 (agent tắt không mở kết nối OTLP) và bước 7.
- **Không lộ bí mật:** không có khóa riêng, token trong git (`git grep` trước mỗi commit).
- **Đúng nghĩa thay đổi trên main của nhóm:** bảng C1, 3 file Java xung đột qua test, CI xanh.
- **Thiết kế mở:** mục "Mở rộng" không đòi xóa file nào của Phần A; đổi giá trị chỉ ở giới hạn bộ nhớ và IP/cổng/token.

## Tiêu chí xong

1. PR #17 (một PR) trên main mới nhất, không xung đột, CI xanh, qua phản biện Codex và Minh đọc; Minh merge.
2. Sau merge: máy 84 không gửi dữ liệu quan sát; pod ổn định 60 phút theo C4.
3. exp-app chạy bản mới, kiểm tín hiệu đạt như Q4; lượt nền và hồi quy V082 có kết quả; bản cũ còn hoàn tác được.
4. Diễn tập demo một vòng đạt, có danh sách lệnh.
5. `mo-rong-may-84.md` liệt kê đủ việc thêm, kèm số liệu RAM và điều kiện.

## Không làm

- Không bật agent hay gửi dữ liệu từ máy 84; không sửa CD chung của nhóm trong task này.
- Không đổi phương pháp RCA; không chọn lại ngưỡng cảnh báo trong task này (nếu C5 cho thấy cần, trình riêng).
- Không đưa frontend vào exp-app trừ khi Minh chọn ở Q6.

## Chi phí ước lượng

| Phần | Ước lượng |
|---|---|
| A (bước 3–5) | 1 phiên; kiểm cục bộ khoảng 30 phút máy (lượt bản 3: verify ~16 phút, mỗi lượt agent vài phút) |
| A (bước 6–7) | Theo giờ merge; 60 phút theo dõi chỉ đọc |
| B | 1–2 phiên; build ARM trên exp-app (chưa có số đo trong hồ sơ này); FlashTicket exp-app dừng khoảng 10 phút khi đổi bản (bước 3 T-070 đo ~10 phút); lượt nền ngắn ≤ 30 phút |

Không lượt nào dài hơn 1 giờ ngoài theo dõi; không tải hơn 5 GB.

## Rủi ro và điều chưa chắc

- **Merge là triển khai ngay** trên máy 84 (CD). Agent tắt nên rủi ro chủ yếu ở log JSON và code B16 (đã qua test). Nhóm đang triển khai liên tục (nhiều pod mới tạo 27/11): chọn giờ merge với nhóm.
- **Bản mới trên exp-app** có thể khác hành vi (p95, luồng mua vé) so với `36a3725d`: phát hiện ở bước 9; cảnh báo demo có thể cần chọn lại ngưỡng.
- **Danh sách chặn query** chỉ là lớp đầu; tham số mới không có tên trong danh sách vẫn đi qua tới Collector (khi mở rộng, Collector xóa toàn bộ query).
- **RAM cụm máy 84** cho giai đoạn sau: chưa kiểm dưới tải thật.

## Quyết định cần Minh khi duyệt SPEC

Giữ nguyên các quyết định đã duyệt ở bản 3: Q2 (Assistant chỉ agent), Q3 (build hai kiến trúc của main), Q5 (ngoại lệ AGENTS §12, đã ghi). Các mục bản 3 về đường nhận, ngưỡng bật agent, người giữ `ENV_<SVC>`, giới hạn rollback (Q4, Q7–Q10 bản 3) chuyển sang giai đoạn mở rộng.

| Mã | Câu hỏi | Đề xuất |
|---|---|---|
| Q1 | Sửa lỗi Booking `-P rca-test` trong PR này | Có (code nằm trong PR; chặn build exp-app ở Phần B) |
| Q2 | Đích agent trong ConfigMap | `http://otel-collector:4318` trong cụm (sau này chỉ thêm Collector) |
| Q3 | Lớp che query ở nguồn | Có: `q` + 28 tên `vnp_*`; tắt exemplar |
| Q4 | Bỏ CA/token khỏi từng pod | Có (TLS và token chuyển về Collector khi mở rộng) |
| Q5 | Thời điểm Phần B và hệ quả cho thực nghiệm (W7 đang hoãn, ngưỡng T-072 chọn trên bản cũ) | Làm Phần B ngay sau merge; W7 khi mở lại dùng bản mới và khai lại phần ghim; nếu lượt nền cho thấy ngưỡng lệch thì trình chọn lại ngưỡng |
| Q6 | Nội dung demo | Kịch bản C6, không frontend |
| Q7 | Mức tăng bộ nhớ chấp nhận sau merge (C4) | Mỗi pod không tăng quá 10% so với số đo 27/11 |

## Prompt bàn giao

Prompt cho Codex soát bản 4 nằm ở cuối `LOG.md` của task này.
