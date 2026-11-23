# Nhật ký T-069

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục.

---

## Phiên 1 — 19/11/2026 — Claude — laptop Minh — vai trò: người làm (soạn SPEC)

**Mở phiên:** tiếp nối phiên làm T-067 (đã nghiệm thu 19/11). Đọc kế hoạch giai đoạn 2 §8.2–8.4, `results/T-064/ho-so-chon.md` §15–17, `tap-chon-dev3-17.json`, `dap-an-dev3.json`, `results/T-063/dong-bang/`, nhật ký thu T-063 và T-066, repo lab (`runner4.py`, `inj3.py`, lịch thu).

**Diễn biến:**
- 19/11 — Trình SPEC bản 1 trong chat. Phát hiện khi soạn: `inj3.py` dòng 113–116, ô RECREATE-PAY tạo lại Payment bằng `compose-t062` (cấu hình T-062) → trên bản ghim sẽ chạy sai cấu hình; đưa sửa vào SPEC.
- 19/11 — Minh hỏi: SPEC làm gì, bao lâu (theo thực tế), tiêm lỗi nào, thế nào là tụt, có khớp từng số không. Trả lời trong chat: thời lượng đo từ nhật ký (31,3 phút/chu kỳ: thu2 13 chu kỳ 07:14–14:01Z 13/11; thu bù 3 6 chu kỳ 07:24–10:32Z 14/11; `e2e-001` 30,9 phút); không so khớp byte mà so hạng theo ô.
- 19/11 — Minh hỏi: dừng có phải chạy lại không, dừng phải có phân tích nguyên nhân; chạy trên server và mất mạng laptop có ảnh hưởng không. Trả lời và sửa thành bản 2: "dừng" là dừng kết luận, không ngắt thu; thêm bước 7 phân tích nguyên nhân trên dữ liệu đã lưu (gồm chạy offline biến thể trên gói ca mới); lặp tách nhiễu thành lượt ngắn riêng; mọi phần chạy trên server (`runner4.py` `setsid nohup` trên exp-obs, bộ tải không cần mạng laptop), kiểm chạy nền ở bước 4; xử lý lỗi theo `runner4.py` `chay_lich`.
- 19/11 — Minh duyệt SPEC bản 2 ngày 19/11/2026 ("duyệt tạo spec"). Ghi `SPEC.md` (bản 2 ghép đầy đủ) và LOG này; thêm dòng T-069 vào STATE.

**Quyết định của Minh trong phiên** (nguyên lời; chưa ghi DECISIONS):
- "Soạn SPEC W3".
- "duyệt tạo spec, sau đó soạn prompt cho phiên claude mới yêu cầu triển khai task, trước khi triển khai task thì cần rà soát spec độc lập trước, không có điểm chặn thì mới triển khai task không cần dừng, nêu có những vấn đề tôi nêu bên trên đề phòng spec chưa chặt thì sửa spec nếu không phải vấn đề mới thì không cần dừng hỏi Minh".
  Nghĩa: phiên Claude mới (người làm) rà soát SPEC độc lập trước khi làm. Không có điểm CHẶN → triển khai trọn task, không dừng hỏi. Nếu phát hiện SPEC chưa chặt **thuộc các vấn đề Minh đã nêu trong phiên này** (dừng không phải chạy lại; dừng phải kèm phân tích nguyên nhân; chạy trên server, mất mạng laptop không ảnh hưởng; thời lượng theo thực tế, không bịa; tiêu chí tụt rõ ràng, không so khớp byte) → được sửa SPEC, ghi LOG, không cần dừng hỏi. Vấn đề mới ngoài nhóm đó → dừng, trình Minh.
  Quyền này gồm commit và push repo lab trong phạm vi ghi của SPEC; lượt thu dài (~9 giờ) đã có mục xử lý lỗi theo luật 21. Commit repo RCA cuối task vẫn xin Minh.

**Kết thúc phiên:**
1. Đã làm: soạn SPEC bản 1, 2; ghi SPEC, LOG, dòng STATE; soạn prompt cho phiên triển khai (cuối LOG).
2. File đã thay đổi: `tasks/T-069-v082-ban-ghim/SPEC.md`, `LOG.md`; dòng T-069 trong `docs/STATE.md`.
3. Kiểm: số thời lượng từ nhật ký thu T-063, T-066; danh sách ô từ `lich-2.json`, `lich-3.json`, `inj3.py`; hạng cũ V082 tính lại khớp tổng hạng cắt 13 (`ho-so-chon.md` §15).
4. Chưa chắc: hạng cũ từng ô cần kiểm trên file chấm (bước 3); ngưỡng D1–D5 là đề xuất đã được duyệt cùng SPEC.
5. Bước tiếp theo: Minh mở phiên Claude mới, dán prompt dưới đây.
6. Lệnh cuối: tạo thư mục task.

---

## Prompt cho phiên Claude triển khai (soạn 19/11/2026; Minh dán khi mở phiên mới)

```text
Đọc AGENTS.md, làm task T-069 trong STATE: tasks/T-069-v082-ban-ghim/ (SPEC bản 2 đã duyệt 19/11, LOG phiên 1).
Vai trò: bạn là người làm (Claude); người phản biện là Codex.

== QUYẾT ĐỊNH CỦA MINH (đã ghi nguyên văn ở LOG phiên 1 — đọc ở đó, không chép lại) ==
1. Rà soát SPEC độc lập TRƯỚC khi làm (Bước 0 dưới đây). Không có điểm CHẶN → triển khai trọn bước 1–9 của SPEC,
   trong đúng "Phạm vi ghi", không dừng hỏi từng bước. Quyền gồm: commit/push repo lab trong phạm vi SPEC;
   lượt thu thử (~1 giờ 34 phút) và thu chính (~7 giờ 18 phút); lượt lặp ngắn nếu SPEC cần.
2. SPEC chưa chặt ở các vấn đề Minh đã nêu → SỬA SPEC, ghi LOG (đoạn cũ → đoạn mới, lý do), KHÔNG dừng hỏi:
   - "dừng" không được buộc phải chạy lại; thu hết 17 ca rồi mới xét;
   - dừng phải kèm phân tích nguyên nhân điều tra được (bước 7), không chỉ nêu lý do;
   - mọi phần chạy trên server; laptop mất mạng không ảnh hưởng lượt chạy;
   - thời lượng phải theo số đo thực tế, không bịa;
   - tiêu chí "tụt" rõ ràng theo hạng từng ô, không so khớp byte.
   Vấn đề MỚI ngoài nhóm trên, hoặc điểm CHẶN → dừng, trình Minh (Luật 0), soạn prompt Codex (khối "Soát SPEC").
3. Commit repo RCA cuối task vẫn phải xin Minh.

== BƯỚC 0 — RÀ SOÁT SPEC ĐỘC LẬP (chỉ đọc; ghi kết quả vào LOG phiên 2) ==
Đọc SPEC, LOG T-069; kế hoạch giai đoạn 2 §8.2–8.4; results/T-064/ho-so-chon.md §15–17, tap-chon-dev3-17.json,
dap-an-dev3.json, manifest-3.json, cham/ (bộ chấm và file chấm dev3 d0 V082 R9); results/T-063/dong-bang/;
results/T-067/thay-doi-main.md, trien-khai/chuoi-container.json; repo lab D:/Project/flashticket-rca-lab
(campaigns/runner/runner4.py, faults/injectors/docker/inj3.py, campaigns/schedules/lich-2.json, lich-3.json,
load/controller/README.md). Kiểm trên thực tế:
- Hạng cũ từng ô của V082 và P7 trên file chấm có khớp SPEC không (tổng hạng cắt 13 / 23; AC@1, AC@3, K).
- Đầu ra cũ (nhan-luot5, nhan-r9) khớp hash manifest-3.
- Đường thực thi thật của từng bước: runner4 đọc lịch thế nào; inj3 RECREATE-PAY sửa ra sao để dùng
  /opt/flash-ticket-build/t067-compose/hieu-luc; các ô còn lại (toxic, hook http.error, pool.hold, cpu, pause)
  có chạy được trên bản ghim không (proxy Toxiproxy, EVENT_ID, lease hook); runner chạy nền setsid nohup
  trên exp-obs và không gọi về laptop; xử lý lỗi theo chay_lich đúng như SPEC mô tả.
- Bộ chấm T-064 chạy được với tập ca mới mà không sửa bộ chấm/đáp án; cách ghép cặp ca cũ–mới.
- Bước 7 (chạy offline biến thể trên gói ca mới): lệnh, cấu hình biến thể có sẵn trong bản chụp goc-12, nơi ghi.
- Máy: exp-app chạy bản ghim 36a3725 đủ 14 container healthy; exp-obs, máy tải dùng được; đĩa đủ.
Ghi từng điểm: CHẶN / KHÔNG CHẶN / SỬA SPEC (thuộc nhóm ở quyết định 2), bằng chứng, hệ quả, cách xử lý.
Không có CHẶN → ghi "Bước 0 không có điểm chặn — triển khai theo quyền của Minh" rồi làm tiếp.

== TOÀN VẸN (điều Minh sợ nhất: phương pháp bị đổi mà không ai biết) ==
- Không sửa: code M1, cấu hình V082, bản chụp goc-12 (/srv/rca-lab/m1-snapshots), bộ chấm và đáp án T-064,
  đầu ra cũ, file T-067. Thấy cần sửa → DỪNG, trình Minh.
- Băm danh sách bảo vệ trước (bước 1) và sau (bước 9); phải trùng byte trên các file đã có trước. Có thể dùng lại
  results/T-067/bao_ve_bam.py làm mẫu (chép ra results/T-069/, không sửa bản T-067).
- Chép/dùng lại file chỉ bằng chép nhị phân; băm nguồn và đích. File sinh trên Windows phải ghi LF.
- Thư mục thử/tạm chỉ trong phạm vi SPEC hoặc scratchpad của phiên. KHÔNG ghi /tmp trên máy (T-067 đã vi phạm 2 lần).
  Chạy script trên máy bằng stdin SSH, xuất ra stdout.
- Giờ trong LOG lấy từ `date -u`, không ước đoán.

== BẢO MẬT ==
- Khóa ở D:/RCA-ext/keys/; không in khóa. known_hosts: dùng bản chép trong scratchpad của phiên
  (từ D:/RCA-ext/overnight-T058/out/known_hosts và dòng máy tải trong D:/RCA-ext/keys/known_hosts);
  không thêm dòng vào file gốc.
- Không đọc .env, grafana.env, ~/.ssh, ~/.bash_history, file env của service; token tải chỉ đọc trong tiến trình, không in.

== KHI CHẠY ==
- Ghi tiêu chí khai trước (results/T-069/tieu-chi.json) và lưu hash trong LOG trước khi thu.
- Thu thử 3 ca: khởi động runner4 bằng setsid nohup trên exp-obs, đóng mọi SSH từ laptop, kiểm lại lượt vẫn chạy;
  kiểm Payment sau RECREATE-PAY đúng image/cấu hình T-067.
- Trước thu chính: ghi giờ bắt đầu, dự kiến kết thúc, phương án lỗi 10/50/99% (đã có trong SPEC) vào LOG.
- Tunnel SSH có thể rớt: kiểm lại trước lệnh quan trọng; không coi lỗi kết nối là kết quả.
- Có ô tụt hoặc điều kiện dừng: làm đủ bước 7 trên dữ liệu đã lưu rồi mới trình.

== KẾT THÚC ==
- Băm lại danh sách bảo vệ; so trùng byte; ghi kết quả.
- LOG đủ mục 7 AGENTS; dòng T-069 trong STATE: "chờ phản biện".
- Prompt cho Codex soát kết quả: Prompt chung + khối "Soát kết quả" trong docs/review-prompt.md, chép nguyên văn,
  chỉ điền thông tin trung tính, đặt cuối LOG.
- Đề xuất nội dung commit repo RCA, chờ Minh duyệt.
- Báo cáo cuối lượt bốn mục theo AGENTS mục 7.
```

---

## Phiên 2 — 19/11/2026 — Claude — laptop Minh — vai trò: người làm (rà soát SPEC, triển khai)

**Mở phiên:** 06:38Z (`date -u` trên exp-obs). Đọc AGENTS.md, STATE, SPEC, LOG phiên 1, kế hoạch giai đoạn 2 §8.2–8.4, `results/T-064/ho-so-chon.md` §15–17, bộ chấm `results/T-064/cham/cham_dev3.py`, `src/m1_ft/cham.py`, `results/T-063/chay/dieu-kien-xac-nhan.md`, `results/T-063/thu3/dieu-kien-xac-nhan-3.md`, `results/T-067/thay-doi-main.md`, `trien-khai/chuoi-container.json`, `compose-hieu-luc/`; repo lab `runner4.py`, `inj3.py`, `run_m1.py`, `safe_export.py`, `stage_m1.py`, `sau_v082.py`, lịch, `load/controller/README.md`. SSH bằng `r.sh` trong scratchpad của phiên (known_hosts chép từ `D:/RCA-ext/overnight-T058/out/known_hosts` + dòng 3.24.8.49; file gốc không sửa), script chạy qua stdin, không ghi file lên máy.

### Bước 0 — rà soát SPEC độc lập (06:39–06:44Z)

| # | Điểm | Phân loại | Bằng chứng | Hệ quả, xử lý |
|---|---|---|---|---|
| 0.1 | Hạng cũ từng ô | KHÔNG CHẶN | `results/T-064/cham/chon-dev3-d0-v082-r9-A.json#/ban/<bản>/chon`: V082 AC@1 9, AC@3 11, tổng hạng cắt 13, K 4; hạng 1 ở 9 ô, hạng 2 ở CPU-BOOK-2 và HTTP5-EVENT-FLASH (khớp SPEC). P7 7/9/23, K 5; P7 hạng 2 ở EVENT-DB-LAT, HTTP5-EVENT-FLASH, vắng ở PAUSE-PAYMENT, lỗi chạy ở RECREATE-PAY (`loi-chay.json`) | Không |
| 0.2 | Bộ chấm chạy lại được | KHÔNG CHẶN | `.venv` của repo (numpy 2.5.3): `cham_dev3.py spec-dev3-d0-v082-r9.json` ra scratchpad → `ban`, `cap`, `nguon_sha256` bằng nhau với file đã lưu; `.txt` trùng từng dòng | Chấm ca mới bằng spec mới qua `goc_uu_tien` (đường dẫn dưới `results/T-069/`), tập ca mới là file `{ca: [{ma, o}]}`; không sửa bộ chấm, đáp án |
| 0.3 | Hash phía cũ | KHÔNG CHẶN | Theo `manifest-3.json#/file`: `kiem/nhan-luot5/` 2442 file, `kiem/nhan-r9/` 45, `cham/dau-ra-dev2/P7/` 26, `cham/dau-ra-dev3/P7/` 16, bộ chấm, đáp án, tập chọn, spec: 0 thiếu, 0 lệch | Ghi lại đầy đủ ở bước 3 |
| 0.4 | Nguồn đầu ra P7 cũ | KHÔNG CHẶN (ghi chép) | Bộ chấm lấy P7 cũ từ `cham/dau-ra-dev2/P7/`, `cham/dau-ra-dev3/P7/`, không từ `kiem/nhan-luot5/` như SPEC ghi | Không đổi kết quả; danh sách bảo vệ gồm cả hai thư mục. SPEC không sửa câu này (ngoài nhóm được sửa) |
| 0.5 | Lệ thuộc W3 (R9 trong bộ xuất chung) | KHÔNG CHẶN | `runner4.py::nhan_ca` gọi `xuat_bo_sung.py` (live-down theo lần dò mới nhất, WHY-99), ghi `m1/bo-sung/<id>/`, V082 đọc từ đó; T-066 kiểm R9 tổng quát trùng 7/7 gói | Cùng ngữ nghĩa phía cũ (R9) và mới |
| 0.6 | Sửa RECREATE-PAY | KHÔNG CHẶN | `inj3.py` dòng 113–116 chạy `compose-t062` với `IMAGE`. Payment đang chạy: nhãn `config_files` = `/opt/flash-ticket-build/t067-compose/hieu-luc/payment-service.yml` (sha256 = bản `results/T-067/compose-hieu-luc/`), image `ft-local/payment-service:arm64-t067-36a3725d`; file hiệu lực có sẵn `image`, `SERVICE_VERSION`, không có `ngrok` | Sửa như SPEC bước 2: `RCA_APP_COMPOSE_DIR` → `docker compose -p flash-ticket-payment-service -f <dir>/payment-service.yml up -d --force-recreate --no-deps` (như `deploy.sh trien-khai`, giữ `--no-deps` của inj3); không đặt thì giữ hành vi cũ. Runner gọi inj3 qua SSH, không truyền biến môi trường; đặt biến trong lệnh `INJ` là sửa runner (ngoài phạm vi). Cách trong phạm vi: inj3 đọc biến; không có biến thì đọc file `/home/ubuntu/t063/inj/compose-dir` (thư mục trạng thái của inj3, trong phạm vi ghi). Chi tiết ở dòng bước 2 |
| 0.7 | Các ô còn lại trên bản ghim | KHÔNG CHẶN | 4 proxy Toxiproxy có, không toxic; kết nối đang mở qua 15433 (Event JDBC), 16379 (Redis), 15673 (AMQP); gateway gọi Booking qua `127.0.0.1:18082` (Prometheus 18/11 08:30Z, `http_client_request_duration_seconds_count{service_name="api-gateway",server_port="18082"}`); thư mục lease/audit `rca-faults/{booking,event}-service/{control,audit}` gắn vào container; Booking có `timeout`, `pkill`, `ps`, `sh`; Booking `cpus: 1` giữ; `inj3.py verify` sạch. Chỉ số xác nhận có trên bản ghim: `db_client_connections_usage/pending` của Event, `httpcheck_status` :8083 (`httpcheck_error` chỉ có chuỗi khi lỗi, như lượt e2e-001 17/11) | Đường code đổi (hook `http.error`, `pool.hold`, RECREATE) kiểm bằng 3 ca thử như SPEC |
| 0.8 | P7 lỗi ở RECREATE-PAY chặn V082 trong runner | KHÔNG CHẶN (xử lý trong phạm vi) | `run_m1.py` gọi adapter trước khi tạo `outputs/`; ở ca cũ ebd5ef38 adapter lỗi "Multiple runtime series…" cả hai lần (`results/T-063/thu3/BAN-GIAO-B.md` dòng 18). Trong `runner4.py::m1_worker`, gói bổ sung và V082 chạy sau `run_m1` trong cùng `try` → P7 lỗi thì V082 không chạy tự động | Nếu lặp lại: sau chu kỳ, chạy đúng lệnh của runner (`xuat_bo_sung.py --t`, cài vào `m1/bo-sung/<mã>/`, lệnh `chay_v082`, `sau_v082.py`) trên gói stage đầu tiên (mã gốc, như T-064 dùng `ebd5ef38`); P7 ghi `loi-chay.json` phía chấm. Khai trước trong `tieu-chi.json`. Không sửa runner, M1 |
| 0.9 | Đường ghi do runner đặt sẵn | KHÔNG CHẶN (ghi chép) | Runner đặt tag tải `t3-<mã>` → máy tải ghi `/srv/rca-lab/load-runs/t3-<mã>` (SPEC ghi `t069-*`); exp-obs `/srv/rca-lab/load-controller/tai-out/t3-<mã>`; `safe_export.py case` ghi `/srv/rca-lab/m1/export-audit/export-audit-<mã>.json` (file mới, không ghi đè); sổ `/srv/rca-lab/ledger/<lượt>.jsonl`; `inj3.py::write_lease` ghi tạm `/tmp/ctl-<uuid>.json` trên exp-app rồi xóa ngay (hành vi có sẵn của bộ tiêm từ T-063) | Là đầu ra bắt buộc của lượt thu Minh đã cho phép; không đổi runner/inj3 ngoài RECREATE-PAY. Liệt kê trong `thay-doi-may.md` |
| 0.10 | Danh sách bảo vệ và checkout exp-app | KHÔNG CHẶN (ghi chép) | `/opt/rca-lab` exp-app ở `5a39028`, exp-obs ở `ee91432`. Commit mới chỉ đổi `inj3.py` và lịch; nhưng checkout trên exp-app còn đổi các file đã khác giữa `5a39028..ee91432` (gồm `campaigns/runner/runner4.py`, không chạy trên exp-app; `observability/collector`, `faults`, `inventory`, `campaigns/lib`, `tai_linux.py` không đổi giữa hai commit) | Băm bảo vệ tách hai phần: (1) danh sách phải trùng byte (bao-ve.tsv T-066, phía cũ T-064, `results/T-067/`, file lab trên laptop, exp-obs `/srv/rca-lab/m1` + `m1-snapshots` + `/opt/rca-lab/campaigns/{runner,g1}`, máy tải `/opt/rca-lab`); (2) cây `/opt/rca-lab` của exp-app ghi trước/sau, khác biệt phải đúng bằng `git diff --name-only` giữa hai commit |
| 0.11 | Tiêu chí "tụt" và tập so D1–D5 | SỬA SPEC (nhóm "tiêu chí tụt rõ ràng theo hạng từng ô") | SPEC chưa nói "hạng" là gì khi đồng hạng, vắng hoặc lỗi chạy; bảng D ghi số cũ trên đủ 11 ca, chưa nói khi có ô không ghép được | Đoạn cũ: "Một ô lỗi **tụt** khi hạng đáp án của V082 mới > hạng cũ + 1 (cho lệch 1 bậc …)." → mới: giữ câu cũ, thêm "'Hạng' là `hang_cat` của `src/m1_ft/cham.py::cham_ca_loi` (bộ chấm T-064, không sửa): hạng kỳ vọng của nút đáp án trong nhóm đồng hạng, cắt ở 6; vắng, lỗi chạy hoặc thiếu đầu ra = 6. So hạng từng ô, không so byte đầu ra. Ca cũ và ca mới ghép theo ô; bốn ô BINH-THUONG ghép theo thứ tự trong lịch." Sau bảng D thêm: "Ô không ghép được bỏ ở cả hai phía; số cũ của D1, D2, D3, D5 tính lại trên đúng tập ô ghép được." Dòng "Lịch sử soạn" ghi lần làm rõ. Lý do: thiếu định nghĩa thì cùng dữ liệu có thể ra hai kết luận |
| 0.12 | "Ghép được" và quy tắc lặp | KHÔNG CHẶN (khai trong `tieu-chi.json`, SPEC giao) | Điều kiện xác nhận tác động từng ô đã có và Minh đã nhận: `results/T-063/chay/dieu-kien-xac-nhan.md` (+ Sửa sau 1), `thu3/dieu-kien-xac-nhan-3.md` (+ Sửa sau 1, 2); script `chay/xac_nhan_ca.py`, `thu3/scripts/xac_nhan_ca_3.py` | Ghép được = ca mới đạt đúng điều kiện mà ca cũ cùng ô đã đạt (chép nhị phân script, chạy trên thư mục dựng từ sổ, đầu ra tải, audit). Thứ tự ưu tiên khi > 4 ô cần lặp khai trong `tieu-chi.json` |
| 0.13 | Thời lượng | KHÔNG CHẶN | Nhật ký: thu2 13 chu kỳ 07:14–14:01Z (31,3 phút/chu kỳ); e2e-001 tải 12:15:04 → xong 12:45:58Z (30,9 phút, M1 xong trong chu kỳ) | 3 ca ~1 giờ 34 phút; 14 ca ~7 giờ 18 phút, như SPEC |
| 0.14 | Chạy nền, không phụ thuộc laptop | KHÔNG CHẶN | `runner4.py` chỉ SSH tới exp-app bằng khóa `/etc/rca-lab/controller`; tải qua `tai_linux.py` (khóa bộ điều khiển, không cần phiên SSH); M1 cục bộ; STOP `/srv/rca-lab/runs/STOP` | Kiểm thực tế ở bước 4 |
| 0.15 | Xử lý lỗi theo `chay_lich` | KHÔNG CHẶN | `fault-start-failed` → `m1-skipped`, chạy tiếp; ngoại lệ chu kỳ → dọn, sạch thì chạy tiếp; tải hỏng 2 lần hoặc không sạch → dừng lượt; M1 lỗi → stage lại mã mới một lần rồi bỏ ca | Đúng mô tả SPEC |
| 0.16 | Bước 7 chạy offline | KHÔNG CHẶN | Bản chụp `goc-12` trên exp-obs có cấu hình V001–V082 (`results/T-064/bien-the/*/cau-hinh.json`); lệnh như `chay_v082` với `--cau-hinh`, `--ban`, `--ra /srv/rca-lab/m1/t069-phan-tich` | Có V060 (H8a), V061 (−H8s1), V066 (−H8a), V032, V002. Không có cấu hình "V082 − H5b" (H8s1 + H8a); không tạo mới (là biến thể mới) — nếu cần, ghi là giới hạn |
| 0.17 | Máy | KHÔNG CHẶN | exp-app: 13 container ứng dụng/hạ tầng + `rca-toxiproxy` đều Up, 7 service image `arm64-t067-36a3725d`, infra healthy; đĩa trống 23 GB. exp-obs: 5 container quan sát Up; `/srv` trống 106 GB; không runner, không STOP. Máy tải: không container chạy; trống 41 GB | — |

**Bước 0 không có điểm chặn — triển khai theo quyền của Minh.** Sửa SPEC ở 0.11 (nhóm được phép); các điểm ghi chép 0.4, 0.9, 0.10 không đổi SPEC.

### Bước 1–3

- 06:47Z — **Bước 1 (toàn vẹn trước):** `results/T-069/bao_ve_bam.py` (dựa theo `results/T-067/bao_ve_bam.py`, bản T-067 không sửa) → `bao-ve-truoc.sha256` 3032 dòng (laptop 2824: `bao-ve.tsv` T-066, phía cũ T-064 theo manifest-3 + file ngoài T-064 trừ `docs/`, `src/m1_ft/`, `results/T-067/**`, điều kiện + script xác nhận T-063, file lab laptop; exp-obs 199: `/srv/rca-lab/m1` 40 + `m1-snapshots` 149 + 10 file lab; máy tải 9, gồm 2 dòng `THIEU` cho `campaigns/g1` như T-067), sha256 cả file `ca206082…`; `lab-exp-app-truoc.sha256` 88 dòng (HEAD `5a39028`), `eb1387d6…`. Chạy hai lần (lần đầu lỗi in tiếng Việt ra console sau khi đã ghi file; sửa `stdout.reconfigure`), hai lần cho cùng hash.
- 06:48Z — **Bước 2:** repo lab `ddb22dc` (đã push; `ee91432..ddb22dc`): `inj3.py` RECREATE-PAY dùng thư mục cấu hình hiệu lực từ `RCA_APP_COMPOSE_DIR` hoặc file `<STATE>/compose-dir`, tạo lại bằng `<dir>/payment-service.yml` `--force-recreate --no-deps`, kiểm nhãn `config_files` của container mới; không có thư mục → hành vi cũ. Lịch `lich-t069-thu.json` (HTTP5-EVENT, POOL-EVENT, RECREATE-PAY; RECREATE-PAY cuối như `lich-3`) và `lich-t069.json` (14 ô; 12 theo thứ tự `lich-2`, 2 ô X3 theo `lich-3`, `multiplier` 3); 3 + 14 ô khớp đúng 17 ô `tap-chon-dev3-17.json`. Trước commit: `docker compose --dry-run … up -d --force-recreate --no-deps` trên exp-app chỉ đụng container Payment, container thật không đổi (Id `b67d5978…`, StartedAt 18/11 07:17:20Z). `/opt/rca-lab`: exp-obs `ee91432` → `ddb22dc`, exp-app `5a39028` → `ddb22dc` (`git fetch` + `git checkout`, cây sạch); hash `inj3.py` `e9c50314…`, `lich-t069-thu.json` `6d4c5a31…`, `lich-t069.json` `f25654bb…`, `runner4.py` `3ce130be…` (không đổi) giống nhau trên laptop và hai máy. Cây lab exp-app sau checkout (`lab-exp-app-sau-checkout.sha256`, `a1288310…`) khác bản trước đúng 33 file = `git diff --name-only 5a39028 ddb22dc`. Ghi `/home/ubuntu/t063/inj/compose-dir` = `/opt/flash-ticket-build/t067-compose/hieu-luc` (sha256 `7109f2c1…`); `compose_dir()` đọc đúng; `inj3.py verify` sạch.
- 06:50Z — **Bước 3 (khai tiêu chí):** `results/T-069/khai_tieu_chi.py` (`860dbb96…`) → **`results/T-069/tieu-chi.json` sha256 `600bc788522294528323a756f97114ee4f942e642359c309eb3060408f8a736a`**, ghi trước khi thu ca nào. Gồm: 17 cặp ca cũ–mới (ô, mã cũ, nhóm thu, image cũ/mới, tải, tham số `inj3`, cửa sổ, vị trí trong lịch mới); hạng cũ tính bằng bộ chấm T-064 (`cham_dev3.tim` + `cham.cham_ca_loi`), đối chiếu từng ô với `chon-dev3-d0-v082-r9-A.json` (p1, p3, hạng kỳ vọng, k, sha đầu ra: trùng); định nghĩa hạng, tụt, ghép được (điều kiện xác nhận T-063 đã nhận), D1–D5, nhóm (a)/(b)/(c), quy tắc lặp (tối đa 4, thứ tự ưu tiên), xử lý P7 lỗi ở RECREATE-PAY. Hạng cũ V082/P7 theo ô: EVENT-DB-LAT 1/2, CPU-BOOK-1 1/1, HTTP5-EVENT 1/1, REDIS-BOOK 1/1, NET-GW-BOOK 1/1, CPU-BOOK-2 2/1, HTTP5-EVENT-FLASH 2/2, PAUSE-PAYMENT 1/6, POOL-EVENT 1/1, CONSUMER-BOOK-SLOW-X3 1/1, RECREATE-PAY 1/6 (tổng 13/23); k V082/P7: BINH-THUONG ×4 1/1, 0/1, 0/0, 1/1; FLASH-HEALTHY 1/1; BINH-THUONG-X3 1/1. Hash phía cũ theo manifest-3: 0 lệch (Bước 0, 0.3).

### Bước 4 — thu thử 3 ca (06:50–08:25Z)

- 06:50:40Z — Phát `t069-thu` trên exp-obs: `RCA_DP_OUT=/srv/rca-lab/runs/t069-thu setsid -f nohup python3 -B /opt/rca-lab/campaigns/runner/runner4.py thu --lich /opt/rca-lab/campaigns/schedules/lich-t069-thu.json > /srv/rca-lab/runs/t069-thu.out 2>&1 < /dev/null`. Tiến trình PID 749768, PPID 1, SID riêng. 06:50:54Z kiểm từ phiên SSH mới: vẫn chạy, `who` trên exp-obs rỗng (không phiên SSH nào gắn). Các lần đọc sau đều là lệnh SSH ngắn, chỉ đọc.
- 06:52Z — Dưới tải, kết nối qua 4 proxy Toxiproxy có thật: 15433 ×2, 15673 ×1, 16379 ×2, 18082 ×1 (`ss` trên exp-app).
- Chu kỳ 0 HTTP5-EVENT `2d5a56fe` (tải 06:51:19Z; t = 07:01:19Z): audit Event `http.error.executed` 720 dòng 07:01:19–07:11:19Z. M1 07:16:00Z: P7 OK, lặp trùng; V082 CAUSE_FOUND, `trung_sha` true; G1 xong.
- Chu kỳ 1 POOL-EVENT `99b8323f` (tải 07:22:39Z): `pool.hold.started` 5 lần (gia hạn lease). M1 07:47:11Z: P7 OK, lặp trùng; V082 `trung_sha` true; G1 xong.
- Chu kỳ 2 RECREATE-PAY `a707078c` (tải 07:53:59Z; t = 1795075439 = 08:03:59Z): Payment tạo lại 08:04:05Z (t+6 s). Container mới: Id `8573d051…`, image `ft-local/payment-service:arm64-t067-36a3725d`, image id `sha256:610aa041…`, `config_files` = `/opt/flash-ticket-build/t067-compose/hieu-luc/payment-service.yml`, `SERVICE_VERSION=36a3725d…`, mem 1 GiB, RestartCount 0 — **trùng `results/T-067/trien-khai/chuoi-container.json` mục payment-service** (tiêu chí xong 1). P7 lỗi adapter "Multiple runtime series map to one logical metric without a declared aggregation" cả hai lần (08:17:24Z `a707078c`, 08:18:19Z stage lại `a707078c2c5b`), như ca cũ ebd5ef38 (Bước 0, 0.8). Lượt xong 08:24:53Z ("Lượt thu xong").
- 08:26–08:27Z — Theo `tieu-chi.json#/xu_ly_rieng/RECREATE-PAY_P7_loi`, chạy đúng lệnh runner trên gói stage đầu `a707078c`: `xuat_bo_sung.py --t 1795075439` (24 kênh, 256 chuỗi, 0 khúc lỗi; sha256 `67d28bdc…` ở `runs/t069-thu/ca/a707078c/` = `m1/bo-sung/a707078c/`); cấu hình V082 khớp hash `01a64b60…`; `chay_ca.py … --ban V082-V066+H8a --ra /srv/rca-lab/m1/v082` → CAUSE_FOUND, hạng 1 `payment-service`, `trung_sha` true; `sau_v082.py --id a707078c` rc 0 (G1 + đồ thị dịch vụ); lưu gói `cases/a707078c` vào `runs/t069-thu/ca/a707078c.tgz` (`e47d94dd…`; `safe_export.py` cần summary P7 nên không dùng). P7 ghi `results/T-069/dau-ra/dev3/d0/P7/a707078c/loi-chay.json`.
- 08:29Z — `nhan_luot.py t069-thu` (`976e7c09…`): 33 file, hash hai đầu khớp (`thu/t069-thu/nhan.sha256` `5056e861…`). Xác nhận tác động bằng script T-063 chép nhị phân (`xac-nhan/xac_nhan_ca.py` = `f4fea7da…`, `xac_nhan_ca_3.py` = `7b69a8dd…`, trùng bản gốc): HTTP5-EVENT xác nhận (script nhóm thu2, `--sua-sau-1`: audit 720 dòng, phủ 20/20 khe 30 s); POOL-EVENT, RECREATE-PAY xác nhận (script nhóm thu3, `--sua-sau-1 --sua-sau-2`). Đầu ra `xac-nhan/t069-thu-thu2.json` (`52f57d32…`), `t069-thu-thu3.json` (`71b96a50…`).
- 08:30Z — Chấm thử `bang_theo_o.py t069-thu` (`784f7326…`; bộ chấm T-064 không sửa): V082 hạng 1 → 1 ở cả 3 ô; P7 1 → 1 (HTTP5-EVENT, POOL-EVENT), 6 → 6 (RECREATE-PAY, lỗi chạy); `cham_dev3.py` nguyên bản cho cùng tổng (`cham/cham-moi-A.txt`). **Chỉ tham khảo, xem dưới.**

### ĐIỂM CHẶN — tải không tương đương: sự kiện tải chuẩn đã hết hạn bán (08:20–08:32Z)

**Quan sát.**
- Số hành trình lỗi của k6 cao hơn ca cũ cùng ô: HTTP5-EVENT 1152 (cũ 720), POOL-EVENT 1174 (cũ 740), RECREATE-PAY 648 (cũ 19) (`xac-nhan/t069-thu-thu*.json#/ca/<mã>/k6`; ca cũ `results/T-063/chay/xac-nhan-ca-2.json`, `thu3/xac-nhan-ca-3-sua-sau.json`).
- Lỗi theo khúc 2 phút từ đầu tải (raw.json trên exp-obs, chỉ đọc): cả 3 chu kỳ có **nền ~43 hành trình lỗi/2 phút từ phút đầu, trước mốc tiêm**; RECREATE-PAY chỉ có nền này. Lượt e2e-001 (bản 3, 17/11) nền 0.
- Trạng thái theo bước (container.log k6): ở cả 3 chu kỳ **mọi `POST /api/v1/orders` trả 409** (432/432 ở chu kỳ 0, 648/648 ở chu kỳ 2); không có `create_payment`, `poll_order`, `get_tickets`. Ở e2e-001: `create_order` 201 ×648, `create_payment` 200 ×278.
- Log Booking: mọi 409 là `errorCode: EVENT_NOT_ON_SALE` (`booking.request.rejected`); lần đầu từ 18/11 08:00Z là 19/11 06:51:22Z (yêu cầu mua đầu tiên của lượt này).
- `event_db.event_schema.tbl_events` (SELECT): sự kiện tải chuẩn `3e7c1df9…` `PUBLISHED`, `sale_starts_at` 11/11 22:16:31Z, **`sale_ends_at` 18/11 22:16:31Z**, `starts_at` 19/11 22:16:31Z, `ends_at` 20/11 22:16:31Z. Booking giữ bản sao riêng `booking_db.booking_schema.tbl_event_sales_snapshots` (`sale_starts_at`, `sale_ends_at`, `configuration_snapshot`, `event_status`). Code: `OrderServiceImpl` ném `EVENT_NOT_ON_SALE` (bản ghim, dòng 703, 1958); `AvailabilityServiceImpl` dòng 74.
- Sự kiện tạo qua API ngày 12/11 (`results/T-062/tai-2/BAN-GIAO-1-giao-dich.md` dòng 13: "Tạo/submit/approve/publish qua API. Không sửa DB."), cửa sổ bán 7 ngày. T-063 (13–14/11) và T-067 (tải 1 giờ sáng 18/11) còn trong cửa sổ.

**Suy luận.** Từ 18/11 22:16Z hệ thống không tạo được đơn. Luồng đặt chỗ, thanh toán, RabbitMQ (`booking.*.q`), Payment, Ticket gần như không có tải; Booking thêm lỗi 409 liên tục. Tải không tương đương ca cũ, trái điều kiện ghép "ô, image, **tải**, can thiệp" (SPEC, kế hoạch §8.2 W3). Lỗi hạ tầng/dữ liệu thử, không phải lỗi V082. Hậu quả:
- 3 ca thử đạt điều kiện xác nhận T-063 (các điều kiện đó không kiểm hành trình thành công), nhưng không đủ làm phía mới của phép so; kết quả hạng ở trên chỉ tham khảo.
- Thu chính 14 ô bây giờ sẽ lặp lại lỗi này. Riêng CONSUMER-BOOK-SLOW-X3 gần như chắc không xác nhận được (điều kiện tồn queue ≥ 10 cần bản tin đơn). Vì vậy **không phát lượt thu chính**.

**Vì sao là điểm chặn, không tự sửa.** Sửa cần đổi dữ liệu ứng dụng trên exp-app (cửa sổ bán ở event_db và bản sao ở booking_db, hoặc tạo sự kiện mới rồi đổi `EVENT_ID` của k6 và `inj3.py`). Việc này ngoài "Phạm vi ghi" của SPEC và ngoài nhóm Minh cho sửa SPEC không cần hỏi. Đây là vấn đề mới, theo quyết định 2 của Minh phải dừng và trình.

**Phương án (đề xuất của người làm; Minh quyết):**
- **A (đề xuất).** Gia hạn đúng sự kiện `3e7c1df9` qua đường ứng dụng (API organizer/admin cập nhật lịch; Event phát thay đổi, Booking cập nhật bản sao), dời cả `sale_*`, `starts_at`/`ends_at`, `checkin_*` cùng một khoảng (ví dụ +14 ngày) để giữ thứ tự thời gian. Giữ `EVENT_ID`, người mua, kịch bản k6, `inj3.py` (HTTP5 nhắm đúng sự kiện này), như ca cũ. Trước khi sửa, dump hai dòng (event_db, booking_db) để hoàn tác. Cần kiểm trước: API có cho đổi lịch khi `PUBLISHED` không; nếu không thì phải chọn B hoặc C. Mặt trái: chạm dữ liệu nghiệp vụ; nếu API không đồng bộ bản sao Booking thì phải dừng lại.
- **B.** SQL trực tiếp vào `tbl_events` và `tbl_event_sales_snapshots` (cả JSON `configuration_snapshot` nếu chứa cửa sổ), xóa cache liên quan. Nhanh, nhưng đi vòng logic ứng dụng, trái cách T-062 ("Không sửa DB"); dễ lệch giữa hai DB.
- **C.** Tạo sự kiện mới qua API như T-062, đổi `EVENT_ID` trong cấu hình k6 và `inj3.py`. Sạch về ứng dụng, nhưng đổi thêm file ngoài phạm vi; sự kiện mới chưa có lịch sử đơn như sự kiện cũ (khác dữ liệu nền so với ca cũ).
- **Sau khi sửa (mọi phương án):** chạy `tai_linux.py test-duong` hoặc một chu kỳ tải ngắn để thấy `create_order` 201 trở lại. **Thu lại 3 ô của lượt thử trong lượt chính** (17 chu kỳ, ~8 giờ 52 phút theo 31,3 phút/chu kỳ). Ca `t069-thu` giữ nguyên (luật cứng 10), ghi "tải không tương đương — không ghép".
- **Chi phí đã dùng:** lượt thử 1 giờ 34 phút; phần kiểm runner chạy nền, sửa RECREATE-PAY, đường V082 khi P7 lỗi, hook `http.error`/`pool.hold` trên bản ghim vẫn dùng được (không phụ thuộc tải mua vé).
- **Rủi ro cùng loại về sau:** sự kiện bắt đầu lúc 19/11 22:16Z; W4 (đêm nền) và W6–W7 cũng cần cửa sổ bán còn hiệu lực. Nên kiểm hạn sự kiện trước mỗi lượt dài.

### Kết thúc lượt (08:35Z) — dừng chờ Minh

1. Đã làm: Bước 0 (không chặn; sửa SPEC ở 0.11); bước 1–3; bước 4 thu thử 3 ca, kiểm chạy nền, kiểm Payment sau tạo lại, chạy V082 cho ca P7 lỗi, nhận dữ liệu, xác nhận tác động, chấm thử. Phát hiện điểm chặn: sự kiện tải hết hạn bán từ 18/11 22:16Z.
2. File đã thay đổi: repo RCA `tasks/T-069-v082-ban-ghim/SPEC.md` (0.11), `LOG.md`, `results/T-069/` (`bao_ve_bam.py`, `bao-ve-truoc.sha256`, `lab-exp-app-truoc.sha256`, `lab-exp-app-sau-checkout.sha256`, `khai_tieu_chi.py`, `tieu-chi.json`, `nhan_luot.py`, `bang_theo_o.py`, `xac-nhan/`, `thu/t069-thu/`, `dau-ra/`, `tap-moi.json`, `cham/`, `bang-theo-o.{json,md}` — bản thử, sẽ sinh lại; `thay-doi-may.md`), dòng T-069 trong `docs/STATE.md`. Repo lab `ddb22dc` (đã push). Máy theo `results/T-069/thay-doi-may.md`.
3. Kiểm: xem các dòng trên (hash hai đầu, cấu hình Payment, xác nhận tác động, bộ chấm chạy lại khớp).
4. Chưa chắc / cần Minh quyết: chọn A/B/C (hoặc khác) để khôi phục tải mua vé; cho thu lại 3 ô thử trong lượt chính (17 chu kỳ). Câu hỏi W3 **chưa trả lời**: 3 ô thử chưa ghép được vì tải không tương đương; 14 ô chưa thu. Toàn vẹn sau (bước 9) chưa băm.
5. Bước tiếp theo: Minh quyết phương án → (nếu A) kiểm API đổi lịch, dump dòng, sửa, kiểm `create_order` 201 → sửa lịch lượt chính thành 17 ô (`lich-t069.json` thêm 3 ô, commit lab) → phát `RCA_DP_OUT=/srv/rca-lab/runs/t069-chinh setsid -f nohup python3 -B /opt/rca-lab/campaigns/runner/runner4.py thu --lich /opt/rca-lab/campaigns/schedules/lich-t069.json > /srv/rca-lab/runs/t069-chinh.out 2>&1 < /dev/null` → `nhan_luot.py t069-chinh` → script xác nhận → `bang_theo_o.py t069-chinh`.
6. Lệnh cuối: SELECT cửa sổ bán (`event_db`, `booking_db` `information_schema`), `git show 36a3725d:…/OrderServiceImpl.java`.

## Prompt cho Codex (soát điểm chặn và phương án; soạn 19/11/2026 08:35Z)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-069 (tasks/T-069-v082-ban-ghim/); đề xuất xử lý điểm chặn ghi ở LOG.md phiên 2, mục "ĐIỂM CHẶN — tải không tương đương" (phương án A/B/C) và phần sửa SPEC ở Bước 0 điểm 0.11.
- Công đoạn: soát SPEC.
- Gói/cổng: W3 (kế hoạch giai đoạn 2 §8.2), chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-069-v082-ban-ghim/SPEC.md (bản 2, duyệt 19/11; làm rõ ở phiên 2), LOG.md (phiên 1, phiên 2); docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2–8.4; results/T-064/ho-so-chon.md §15–17; results/T-067/thay-doi-main.md; results/T-062/tai-2/BAN-GIAO-1-giao-dich.md.
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: results/T-069/ (tieu-chi.json, thu/t069-thu/, xac-nhan/, dau-ra/, bang-theo-o.json, thay-doi-may.md, bao-ve-truoc.sha256); repo lab D:/Project/flashticket-rca-lab commit ddb22dc (faults/injectors/docker/inj3.py, campaigns/schedules/lich-t069*.json, campaigns/runner/runner4.py); repo FlashTicket D:/Project/flash-ticket-platform revision 36a3725d (services/booking-service, services/event-service); máy exp-app, exp-obs, máy tải theo inventory/ của repo lab, khóa và cách gọi ở AGENTS.md mục 12 (chỉ đọc nếu Minh cho phép).
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tên bản phản biện được ghi>.

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
```

```text
Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.
```

(Khối trọng tâm cổng: `docs/review-prompt.md` chưa có khối cho G6.)

- 08:40Z — **Quyết định của Minh (chat 19/11), nguyên văn:** "A: gia hạn qua API". Nghĩa: khôi phục tải mua vé bằng cách gia hạn đúng sự kiện `3e7c1df9` qua API của ứng dụng (phương án A ở mục "ĐIỂM CHẶN"). Bắt đầu bằng kiểm API có cho đổi lịch khi `PUBLISHED` không; thao tác ghi dữ liệu thực hiện theo phương án A đã trình (dump dòng trước, dời mọi mốc cùng một khoảng).
- 08:45Z — **Kiểm phương án A (chỉ đọc code bản ghim `36a3725d`):** API không cho đổi lịch sự kiện đã `PUBLISHED`. `PUT /organizer/events/{id}` → `EventService.save` gọi `state(event, "DRAFT")`; `return-to-draft` chỉ nhận `PENDING_APPROVAL`; ngoài hủy (`CancellationController`) không có endpoint nào sửa sự kiện `PUBLISHED`. **Phương án A không làm được bằng API.** Theo điều kiện đã trình ("nếu không thì phải chọn B hoặc C"), dừng, trình lại Minh. Đề xuất mới: B (SQL dời mốc ở `event_db.tbl_events` và `booking_db.tbl_event_sales_snapshots`, gồm JSON `configuration_snapshot` nếu chứa cửa sổ; dump dòng trước; xóa cache liên quan nếu có; kiểm `create_order` 201 bằng một lượt tải ngắn). Lý do chọn B hơn C: giữ `EVENT_ID`, người mua, k6, `inj3.py` như ca cũ; C phải đổi `EVENT_ID` trong `inj3.py` và cấu hình k6 (ngoài phạm vi), cần đăng nhập organizer/admin, và sự kiện mới không có lịch sử đơn như cũ. Mặt trái của B: đi vòng logic ứng dụng; phải đọc cấu trúc `configuration_snapshot` và cache Booking trước khi sửa, lệch thì dừng.
- 09:15Z — **Quyết định của Minh (chat 19/11), nguyên văn:** "B: SQL dời mốc". Làm theo phương án B ghi ở dòng 08:45Z: đọc cấu trúc trước, dump dòng, sửa, kiểm `create_order` 201; lệch thì dừng.
- 09:15–09:20Z — **Đọc cấu trúc trước khi sửa (chỉ đọc):** Booking kiểm bán bằng cột `sale_starts_at`/`sale_ends_at` của `tbl_event_sales_snapshots` (`OrderServiceImpl` ~dòng 1955: `decisionAt` so với `snapshot.getSaleStartsAt/EndsAt`), đọc DB mỗi lần, không thấy cache. JSON `configuration_snapshot` (jsonb) có `saleStartsAt`, `saleEndsAt`, `eventStartsAt`, `eventEndsAt` (giây epoch, số thực). Bản sao khác của mốc sự kiện: `ticket_db.ticket_schema.tbl_event_access_snapshots` (`event_starts_at`, `event_ends_at`), `payment_db.payment_schema.tbl_event_finance_snapshots` (`event_ends_at`); `tbl_event_payouts` của sự kiện: 0 dòng. Dump 5 dòng trước khi sửa: `results/T-069/sua-su-kien/truoc.jsonl` (sha256 `ae1ff3bb…`).
- 09:20:14Z — **Sửa (phương án B, Minh duyệt):** hai transaction, mỗi transaction kiểm đúng 1 dòng khớp giá trị cũ (`status`/`event_status` = PUBLISHED, `sale_ends_at` = 18/11 22:16:31.402736Z), lệch thì RAISE. `event_db.event_schema.tbl_events`: `sale_ends_at`, `starts_at`, `ends_at`, `checkin_starts_at`, `checkin_ends_at` +14 ngày. `booking_db.booking_schema.tbl_event_sales_snapshots`: `sale_ends_at` +14 ngày, JSON `saleEndsAt`, `eventStartsAt`, `eventEndsAt` +1.209.600 s. **Giữ nguyên** `sale_starts_at` (dời sẽ đẩy ngày mở bán ra 25/11, chặn mua), `status`, `row_version`, `source_config_version`, `updated_at`, `received_at`. Dump sau: `sua-su-kien/sau.jsonl` (`5a457fc3…`); so từng trường: chỉ đúng các trường trên đổi (bán tới 02/12 22:16:31Z, diễn 03/12–04/12). **Không sửa** bản sao ở Ticket và Payment (ngoài phần Minh duyệt): `event_starts_at`/`event_ends_at` ở đó vẫn 19–20/11. Không ảnh hưởng mua vé hôm nay (Booking không đọc chúng); có thể ảnh hưởng check-in/payout sau 20/11 22:16Z → báo Minh. Hoàn tác: UPDATE ngược −14 ngày theo `truoc.jsonl`.
- 09:20–09:34Z — **Kiểm tải mua vé:** `tai_linux.py start --tag t069-kiem-ban-001 --seconds 180` (09:20:33Z), nhận 09:33:57Z (12 hash khớp). container.log: `create_order` 201 ×65, `create_payment` 200 ×44, `get_tickets` 200 ×44, `cancel_order` 200 ×10, `poll_order` 200 ×124; `journey_failed` không có. Tải mua vé hoạt động lại.
- 09:34Z — Repo lab `ca5d6f5` (đã push): `campaigns/schedules/lich-t069-chinh.json` (`2d85913d…`, 17 chu kỳ = 14 ô `lich-t069.json` cùng thứ tự + HTTP5-EVENT, POOL-EVENT, RECREATE-PAY ở cuối; khớp 17 ô tập chọn). `/opt/rca-lab` exp-obs, exp-app → `ca5d6f5`, cây sạch; `inj3.py`, `runner4.py` không đổi. Phụ lục khai trước `results/T-069/tieu-chi-bo-sung.json` (sha256 **`58f7aca606cb1415528b3cf0c1a4ff539bec6eb8de687b7ef9a74b8cfb9817df`**, ghi trước khi thu lượt chính): 3 ca `t069-thu` không ghép (tải không tương đương); 3 ô thu lại ở cuối lượt chính; thêm điều kiện ghép "chu kỳ có ít nhất một `create_order` 201"; mọi ngưỡng, định nghĩa giữ nguyên `tieu-chi.json`. Lý do thu lại 3 ô: đã trình ở mục "ĐIỂM CHẶN" ("Sau khi sửa (mọi phương án)"), cần để đạt tiêu chí xong 3 (đủ 17 ca); thời lượng lượt chính tăng từ ~7 giờ 18 phút lên ~8 giờ 52 phút.

### Bước 5 — thu chính 17 chu kỳ: kế hoạch trước khi phát (luật 21)

- Lệnh: `RCA_DP_OUT=/srv/rca-lab/runs/t069-chinh setsid -f nohup python3 -B /opt/rca-lab/campaigns/runner/runner4.py thu --lich /opt/rca-lab/campaigns/schedules/lich-t069-chinh.json > /srv/rca-lab/runs/t069-chinh.out 2>&1 < /dev/null` trên exp-obs.
- Thời lượng: 17 × 31,3 phút ≈ 8 giờ 52 phút (số đo: thu2, e2e-001, lượt thử hôm nay 06:50:40–08:24:53Z = 94,2 phút cho 3 chu kỳ). Bắt đầu ~09:36Z → dự kiến kết thúc ~18:30Z.
- Lỗi ở 10%, 50%, 99% (theo SPEC, `runner4.py::chay_lich`): một ca lỗi (tiêm hỏng, ngoại lệ chu kỳ) → runner dọn, bỏ ca, chạy tiếp; tải khởi động hỏng 2 lần hoặc môi trường không sạch → dừng lượt, ca đã xong giữ. Khi đó: chạy tiếp đúng các ô còn thiếu bằng lịch con `lich-t069-chinh-tiep-<n>.json` (chỉ các ô thiếu, cùng thứ tự), không chạy lại ô đã xong; ở 10% mất ~1 chu kỳ (31 phút), ở 50% và 99% cũng chỉ mất các ô thiếu. P7/V082 lỗi chạy chỉ chặn ô đó (RECREATE-PAY P7 lỗi → xử lý như lượt thử). Chỉ chạy lại toàn bộ khi bộ tiêm hoặc bộ xuất tính sai, trình Minh trước.
- Theo dõi bằng lệnh SSH ngắn chỉ đọc; laptop mất mạng không ảnh hưởng lượt.
- 09:34:55Z — **Phát lượt chính `t069-chinh`** (lệnh như trên; trước khi phát: máy tải không container, không STOP, chưa có thư mục lượt). PID 769851, PPID 1, SID riêng. Dự kiến kết thúc ~18:27Z.
- 11:33–11:40Z — **Kiểm giữa lượt (chỉ đọc, phiên mới của Claude cùng phiên 2; scratchpad đổi, dựng lại `r.sh`):** runner PID 769851 chạy, chu kỳ 3/17. Ba ca đã xong (BINH-THUONG `1e5debb6`, EVENT-DB-LAT `bd976df6`, CPU-BOOK-1 `03573b63`): P7 OK lặp trùng, V082 `trung_sha` true; tải lành ở cả 3 chu kỳ (`create_order` 201 ×648, `create_payment` 200 ×432, `journey_failed` 0). Quan sát sớm (chưa chấm chính thức): CPU-BOOK-1 cả V082 và P7 xếp `ticket-service` 1, `keycloak` 2, `booking-service` 3 (khóa giống nhau ở ba thực thể đầu; ca cũ cả hai xếp Booking 1) → theo tiêu chí khai trước là ô tụt (3 > 1 + 1), P7 cùng tụt → nghiêng nhóm (a); bước 7 và lặp làm sau khi lượt xong. Dự kiến lượt xong ~18:30Z (chu kỳ 16 tải ~17:59Z).
- 15:57Z — **Kiểm giữa lượt (chỉ đọc):** runner chạy, chu kỳ 12/17 (BINH-THUONG-X3). 12 ca xong, không `cycle-error`, không tiêm hỏng, không M1 lỗi; tải lành (`create_order` 201 mọi chu kỳ; `journey_failed` 0 ở ô không làm hỏng hành trình, HTTP5-EVENT-FLASH 2162 và PAUSE-PAYMENT 154 gần ca cũ 2161 và 159). Top-1 V082 (quan sát, chưa chấm theo tập chấp nhận): EVENT-DB-LAT, REDIS-BOOK, NET-GW-BOOK, PAUSE-PAYMENT như cũ; CPU-BOOK-2 và HTTP5-EVENT-FLASH đúng hạng 1 (cũ 2); CPU-BOOK-1 Booking hạng 3 (cả P7). Ô không lỗi: BINH-THUONG thứ 3 `a06231fd` V082 CAUSE_FOUND (ca cũ 83073ed1 k = 0; P7 cũng đổi 0 → 1). Dự kiến xong ~18:30Z.
- 17:31Z — **Kiểm giữa lượt (chỉ đọc):** chu kỳ 15/17 (POOL-EVENT, tải từ 17:27:00Z), chưa `thu3-end`; không `cycle-error`, không M1 lỗi. Thêm (top-1, chưa chấm chính thức): BINH-THUONG-X3 `0bec9eca` V082 NO_INTRINSIC_ANOMALY (cũ k = 1; P7 vẫn CAUSE_FOUND); CONSUMER-BOOK-SLOW-X3 `785bfd0c` Booking hạng 1 như cũ (`create_order` 201 ×1765, 429 ×72; `journey_failed` 1207, cũ 1205); HTTP5-EVENT `30ae6ac0` V082 và P7 cùng xếp Booking 1, Event 2 (cũ Event 1; ở lượt thử khi không mua được vé, Event 1). Dự kiến xong ~18:30Z.
- 17:35Z — **Quyết định của Minh (chat 19/11), nguyên văn:** "sau khi chạy xong thì tiến hành phân tích kết quả nhé, tôi muốn tìm nguyên nhân của các ca tụt, lí do tụt, do code thay đổi hay do tải , log trace metric thay đổi ? tôi sẽ treo máy nên bạn cần tự đánh thức khi xong, không  đợi tôi đánh thức, tôi cho bạn quyền quyết định các phần nằm trong mong muốn của tôi, sau đó trình kế hoạch tiếp theo . cần tận dụng mọi khoảng thời trống, tránh để thời gian trống vô ích". Nghĩa: sau lượt chính, làm phân tích nguyên nhân (bước 7) cho các ô tụt/đổi hạng — tách code đổi, tải, thay đổi log/trace/metric — tự quyết các phần trong mục đích này, rồi trình kế hoạch tiếp; bắt đầu phân tích ngay trên ca đã có trong lúc lượt còn chạy.
- 17:40–18:00Z — **Bước 7 bắt đầu sớm trên ca đã xong (theo quyết định 17:35Z):** đầu ra 15 ca kéo về `results/T-069/dau-ra/` (hash hai đầu khớp). Script mới (chỉ đọc): `phan_tich_o.py` (so khóa xếp hạng và `kenh_co` cũ/mới), `phan_tich_nen.py` → `phan-tich/nen-V082.txt`, `span_thong_ke.py` (thống kê span theo câu lệnh trong gói ca, cửa sổ N/A của đầu ra) → `phan-tich/span-http5-{moi-30ae6ac0,cu-e9c9679b}.txt`, `phan-tich/span-cpu1-cu-moi.txt`, `so_do_phu.py` → `phan-tich/do-phu.txt`; `dem_tai.py` (đếm bước tải theo chu kỳ), `kiem_db.sh` (kiểm DB chỉ đọc, chạy sau lượt). Gói ca cũ giải nén vào scratchpad từ `results/T-063/thu2/ca/*.tgz`. Quan sát chính (diễn giải và kết luận ở `phan-tich-nguyen-nhan.md` sau khi lượt xong): (1) HTTP5-EVENT: trong A, Booking không chậm theo từng câu lệnh; câu nhanh theo yêu cầu biến mất (hành trình mua dừng ở bước detail), kênh gộp `SELECT tbl_orders`/`SELECT booking_db` bị chi phối bởi truy vấn nền worker hết hạn đơn, p50 cũ 3,9/6,3 ms → mới 34,8/42,6 ms (cùng câu lệnh; `OrderRepository` dòng 48 không đổi giữa `6b21ed55` và `36a3725d`). (2) CPU-BOOK-1: p50/p90 truy vấn kho vé Booking tăng ~2 lần ở cả cũ và mới; s cũ 1352 nhờ một mẫu đuôi 262,6 ms, mới max 15,2 ms; Ticket truy vấn giao vé p50 nền 2,66 → 19,17 ms, đuôi A 46 → 252 ms; Keycloak OUTBOX đuôi A 10 → 81 ms. (3) Ca không lỗi không ồn hơn nói chung; BINH-THUONG thứ 3 báo nhầm do `op|event-service|event_db` (s 241). (4) Độ phủ tín hiệu gần như không đổi. (5) P7 cho cùng thứ tự ba thực thể đầu ở cả hai ô đổi hạng → thành phần H5b/H8s1/H8a không gây đổi hạng; bỏ phép chạy offline biến thể (bước 7.4) vì P7 = "bỏ cả ba" đã trả lời câu hỏi đó (quyết định trong quyền Minh cho 17:35Z).
- 18:29:18Z — **Lượt chính xong** ("Lượt thu xong"). 17 chu kỳ, không `cycle-error`, không tiêm hỏng. RECREATE-PAY `c4d7999f`: P7 lỗi adapter như ca cũ (18:21:57Z, stage lại 18:23:04Z) → 18:29:58–18:31:36Z chạy V082 theo `tieu-chi.json#/xu_ly_rieng` (bổ sung `d54aa491…`, cấu hình khớp hash, CAUSE_FOUND, hạng 1 `payment-service`, `trung_sha` true; `sau_v082.py` rc 0; `runs/t069-chinh/ca/c4d7999f.tgz` `73200bc0…`); P7 `loi-chay.json` phía chấm.
- 18:31Z — **Kiểm DB chỉ đọc** (`kiem_db.sh` → `phan-tich/kiem-db.txt`; một câu lỗi cú pháp ở `tbl_order_items` vì bảng không có cột thời gian, không ảnh hưởng phần khác). `tbl_orders` 37.477 dòng (tạo trước 13/11 07:14Z: 3.713; trước 14/11 07:24Z: 15.133); `tbl_ticket_deliveries`/`tbl_issuances` 24.438 (2.412; 9.875); truy vấn worker hết hạn đơn: `Seq Scan on tbl_orders`; `pg_stat_user_tables`: `tbl_issuances` 7.141.875 lượt quét tuần tự, 92.992.449.315 dòng đọc; `tbl_ticket_deliveries` 7.330.618, 93.031.378.432.
- 18:32–18:39Z — `nhan_luot.py t069-chinh` 175 file (hash khớp); `dem_tai.py` → `thu/t069-chinh/tai-create-order.json`: mọi chu kỳ có `create_order` 201. Xác nhận tác động: 13 ô nhóm thu2 xác nhận (script thu2), 4 ô nhóm thu3 xác nhận (script thu3); 17/17 ghép được. **Chấm (`bang_theo_o.py t069-chinh`, bộ chấm T-064 không sửa; `cham_dev3.py` nguyên bản cho cùng tổng):** V082 cũ → mới AC@1 9 → 9, AC@3 11 → 11, tổng hạng cắt 13 → 14, K 4 → 4; P7 7 → 7, 9 → 9, 23 → 24, K 5 → 6. **D1–D5 đều không.** Một ô tụt: CPU-BOOK-1 V082 1 → 3 (P7 1 → 3, nhóm a). Đổi hạng khác: HTTP5-EVENT 1 → 2 (P7 1 → 2), CPU-BOOK-2 2 → 1, HTTP5-EVENT-FLASH 2 → 1 (P7 2 → 1), EVENT-DB-LAT P7 2 → 1; K: BINH-THUONG thứ 3 V082 0 → 1, BINH-THUONG-X3 V082 1 → 0. Theo quy tắc lặp: CPU-BOOK-1, HTTP5-EVENT, CPU-BOOK-2, HTTP5-EVENT-FLASH (EVENT-DB-LAT ngoài 4 ô).
- 18:39:49Z — **Phát lượt lặp `t069-lap`** (bước 8; lab `407b4f5`, `lich-t069-lap.json` `5c98eb6a…`; `/opt/rca-lab` hai máy → `407b4f5`; lệnh như lượt chính với `RCA_DP_OUT=/srv/rca-lab/runs/t069-lap`). PID 874410, PPID 1. 4 chu kỳ, dự kiến xong ~20:46Z.
- 18:41–18:58Z — **Bước 7 (tiếp):** `so_psi.py` → `phan-tich/psi.txt` (PSI máy, CPU cgroup Booking theo đầu dò, cũ/mới); `cpu_container.py` (Prometheus, chỉ đọc) → `phan-tich/cpu-container-nen.txt` (PostgreSQL nền 0,064–0,089 → 0,288–0,408 lõi; service ứng dụng không đổi); đọc `src/m1/e4.py::_diem_z_native` (z = (max A − trung vị N)/IQR N); `z_kiem.py` → `phan-tich/z-kiem.txt`: z tính lại từ span thô khớp s M1 (Ticket 944,8/945,8; Booking 449,2/449,7; Keycloak 698,3/696,2; kho vé cũ 1352,3/1352,3; HTTP5 `tbl_orders` 332,0/332,4, `booking_db` 292,5/292,5); mẫu max A ở các kênh dẫn đầu ca mới là truy vấn nền quét tuần tự. Viết `results/T-069/phan-tich-nguyen-nhan.md` (mục 1–9; mục 7 chờ lượt lặp). Bản bảng lượt chính lưu `bang-theo-o-chinh.{json,md}` (chép nhị phân, `cmp` trùng).
- 20:45:36Z — **Lượt lặp `t069-lap` xong** (4/4 chu kỳ, P7 OK lặp trùng, V082 `trung_sha` true). Bộ theo dõi nền trên laptop thoát mã 4 (đứt kết nối khi laptop treo máy); lượt trên server không bị ảnh hưởng — đúng thiết kế chạy nền. Kiểm lại 00:05Z 20/11 bằng SSH mới: runner không còn chạy, nhật ký có "Lượt thu xong".
- 00:05–00:09Z 20/11 — `nhan_luot.py t069-lap` 46 file (hash khớp); `dem_tai.py` → mọi chu kỳ có `create_order` 201; xác nhận tác động 4/4 (script nhóm thu2). Chấm `bang_theo_o.py t069-chinh --lap t069-lap`: lần lặp **trùng lần thu chính ở cả 4 ô** (V082/P7: CPU-BOOK-1 3/3, HTTP5-EVENT 2/2, CPU-BOOK-2 1/1, HTTP5-EVENT-FLASH 1/1); D1–D5 không đổi (đều không). `z_kiem.py` trên `85255a46` → `phan-tich/z-kiem-lap-cpu1.txt`: mẫu max A Ticket là truy vấn giao vé 339,9 ms (z 1026,2), Booking là join worker hết hạn 369,6 ms (z 599,8), kho vé z 118,1 — cơ chế lặp được. **Diễn giải sau khi xem (không đổi tiêu chí):** nhãn "a+c" của HTTP5-EVENT trong `bang-theo-o.json` là do áp nguyên câu quy tắc (lần lặp trong [cũ − 1, cũ + 1]); ô không tụt ngay từ lần đầu và lần lặp trùng lần đầu → nhóm (a), không phải nhiễu. Ghi ở `phan-tich-nguyen-nhan.md` §7.
- 00:13Z — **Bước 9 (toàn vẹn sau):** `bao_ve_bam.py` → `bao-ve-sau.sha256` (`572ff168…`, 3416 dòng), `lab-exp-app-sau.sha256` (`7a87c98f…`). So với `bao-ve-truoc.sha256`: **0 lệch trên 3021 đường dẫn đã có** (3032 dòng, 11 đường dẫn trùng giữa các nhóm); file mới chỉ ở `/srv/rca-lab/m1/{cases 156, outputs 110, v082 72, bo-sung 24, export-audit 22}`. Lab exp-app so bản sau checkout `ddb22dc`: chỉ HEAD và `lich-t069-chinh.json`, `lich-t069-lap.json` mới (commit `ca5d6f5`, `407b4f5`). `results/T-069/SHA256SUMS` 318 file (`410d9923…`); 3 file `raw.json` của k6 nặng 60–78 MB (ô FLASH).

### Kết thúc phiên 2 (00:15Z 20/11)

1. **Đã làm:** Bước 0 (không chặn; làm rõ SPEC ở 0.11). Bước 1–3: băm bảo vệ trước; `inj3.py` RECREATE-PAY dùng cấu hình hiệu lực (lab `ddb22dc`); `tieu-chi.json` khai trước. Bước 4 thu thử 3 ca: chạy nền đạt, Payment tạo lại đúng cấu hình T-067; phát hiện sự kiện tải hết hạn bán → dừng, trình Minh; Minh chọn B → dời mốc +14 ngày bằng SQL (event_db, booking_db), kiểm tải mua vé hồi phục. Bước 5 thu chính 17 chu kỳ (`t069-chinh`, 09:35–18:29Z). Bước 6 chấm. Bước 7 phân tích nguyên nhân (`phan-tich-nguyen-nhan.md`). Bước 8 lặp 4 ô (`t069-lap`). Bước 9 toàn vẹn sau.
2. **File đã thay đổi:** repo RCA: `tasks/T-069-v082-ban-ghim/SPEC.md` (0.11), `LOG.md`, dòng T-069 trong `docs/STATE.md`, `results/T-069/` (318 file theo `SHA256SUMS`). Repo lab (đã push): `ddb22dc` (inj3, lịch thử/14 ô), `ca5d6f5` (lịch chính 17 ô), `407b4f5` (lịch lặp). Máy: `results/T-069/thay-doi-may.md` (M1–M11) cộng: lượt `t069-lap` (18:39:49Z; như M11 với `RCA_DP_OUT=/srv/rca-lab/runs/t069-lap`), `/opt/rca-lab` hai máy → `407b4f5`; ca RECREATE-PAY `c4d7999f` chạy V082 tay như M7.
3. **Kiểm đã chạy:** bộ chấm T-064 chạy lại khớp file cũ; hash phía cũ khớp manifest-3; hash hai đầu mọi file nhận; xác nhận tác động 17/17 + 4/4 bằng script T-063 chép nhị phân; `cham_dev3.py` nguyên bản cho cùng tổng; z tính lại từ span thô khớp s của M1; toàn vẹn trước = sau (0 lệch).
4. **Kết quả và điều cần Minh quyết** — tách theo luật 14:
   - *Task đạt:* đủ 17 ca ghép được, mỗi ca có P7 (hoặc lỗi chạy ghi rõ) và V082 trùng SHA; bảng theo ô, nhóm giải thích, D1–D5; toàn vẹn trước = sau. Tiêu chí xong 1–6 đạt.
   - *Câu hỏi W3:* V082 không hồi quy quá ngưỡng khai trước (AC@1 9 = 9, AC@3 11 = 11, tổng hạng cắt 13 → 14, K 4 = 4; D1–D5 không). Một ô tụt (CPU-BOOK-1 1 → 3), tái lập ở lần lặp, P7 tụt cùng mức.
   - *Cơ chế (đã lần, luật 15):* dữ liệu tích lũy (bảng đơn/vé ~10 lần) làm worker nền quét tuần tự chậm 7–9 lần và PostgreSQL tốn CPU 4–5 lần; bước chấm z của lõi (một mẫu max / IQR trên đơn vị op gộp) biến các mẫu đuôi của truy vấn nền thành điểm cao ở service không bị tiêm (CPU-BOOK-1) hoặc ở Booking khi thành phần câu lệnh đổi (HTTP5-EVENT). Không do thành phần V082, không do code service, không do kịch bản tải hay độ phủ tín hiệu.
   - *Còn mở:* vì sao bộ lập kế hoạch quét tuần tự (cần `EXPLAIN ANALYZE`); cơ chế hai ô tốt lên (CPU-BOOK-2, HTTP5-EVENT-FLASH) và báo nhầm BINH-THUONG thứ 3 chưa lần mẫu max; bản sao mốc sự kiện ở Ticket/Payment chưa dời (ảnh hưởng sau 20/11 22:16Z); 3 file `raw.json` lớn khi commit.
   - *Quyết định phụ thuộc:* chuyển W4/W5 (theo SPEC, điều kiện không dừng đã đạt); kiểm soát trạng thái DB cho W4 và W6–W7; có ghi nhận điểm yếu chấm z vào thiết kế W6 không.
5. **Bước tiếp theo chính xác:** Minh quyết các mục trong "Kế hoạch tiếp theo" (chat 20/11); Codex soát kết quả bằng prompt dưới; Minh duyệt commit repo RCA. Không còn lượt nào đang chạy trên máy.
6. **Lệnh cuối:** `find results/T-069 -type f ! -name SHA256SUMS | sort | xargs sha256sum > results/T-069/SHA256SUMS`.

## Prompt cho Codex — soát kết quả T-069 (soạn 20/11/2026 00:15Z)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-069, tasks/T-069-v082-ban-ghim/.
- Công đoạn: soát kết quả.
- Gói/cổng: W3 (docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2), chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-069-v082-ban-ghim/SPEC.md (bản 2 duyệt 19/11, làm rõ ở phiên 2), LOG.md (phiên 1, phiên 2); results/T-064/ho-so-chon.md §15–17; results/T-063/chay/dieu-kien-xac-nhan.md, results/T-063/thu3/dieu-kien-xac-nhan-3.md; results/T-067/thay-doi-main.md.
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: results/T-069/ (SHA256SUMS; tieu-chi.json, tieu-chi-bo-sung.json, bang-theo-o.{json,md}, bang-theo-o-chinh.{json,md}, phan-tich-nguyen-nhan.md, phan-tich/, thu/, dau-ra/, xac-nhan/, cham/, sua-su-kien/, thay-doi-may.md, bao-ve-{truoc,sau}.sha256, lab-exp-app-*.sha256, các script .py/.sh); results/T-064/cham/cham_dev3.py, src/m1_ft/cham.py, src/m1/e4.py; repo lab D:/Project/flashticket-rca-lab commit ddb22dc, ca5d6f5, 407b4f5 (faults/injectors/docker/inj3.py, campaigns/schedules/lich-t069*.json, campaigns/runner/runner4.py); repo FlashTicket D:/Project/flash-ticket-platform revision 6b21ed55 và 36a3725d; gói ca cũ results/T-063/thu2/ca/*.tgz; máy exp-app, exp-obs, máy tải theo inventory/ của repo lab, khóa và cách gọi ở AGENTS.md mục 12 (chỉ đọc nếu Minh cho phép). Chấm chạy bằng D:/RCA-flashticket/.venv/Scripts/python.exe.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tên bản phản biện được ghi>.

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
```

```text
Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.
```

(Khối trọng tâm cổng: `docs/review-prompt.md` chưa có khối cho G6.)

### Phiên 3 — 20/11/2026 — Claude — laptop Minh — vai trò: người làm (đáp phản biện, sửa theo duyệt)

- 02:31Z — Codex soát kết quả (chat 20/11, R1–R7); người làm đáp trong chat (R1, R3–R7 đúng; R2 đúng một phần; N1–N5). **Quyết định của Minh (chat 20/11), nguyên văn:** "đuyệt đề xuất sửa, sau đó trình kế hoạch tiếp theo". Phạm vi: đúng danh sách đề xuất sửa gom theo file trong phản hồi (dinh-chinh-1.md; so_do_phu đủ 17 cặp; bang_theo_o bản mới sửa D4, giữ bản cũ; phép bỏ từng thành phần V061/V066/V060 trên 03573b63, 85255a46, 30ae6ac0 ra /srv/rca-lab/m1/t069-phan-tich/; LOG, STATE; DECISIONS; WHY). Quyết định chấp nhận ngoại lệ CPU-BOOK-1 cho demo **chưa** được duyệt (trình trong kế hoạch tiếp).
- 02:31–02:38Z — **Bước 7.4 (R4):** V060, V061, V066 trên `03573b63`, `85255a46`, `30ae6ac0` (exp-obs `/srv/rca-lab/m1/t069-phan-tich/<bản>/`, cấu hình khớp manifest-3; 9/9 rc 0, `trung_sha` true) → `results/T-069/phan-tich/bien-the/` (hash hai đầu khớp). Hạng nút đáp án giống P7 và V082 ở cả 3 gói (CPU-BOOK-1 3, 3; HTTP5-EVENT 2), cùng khóa quyết định.
- ~02:40Z — **R5:** `so_do_phu.py` đủ 17 cặp → `phan-tich/do-phu-17.txt`; đếm lại từ `#/diagnostics`: kênh chấm hợp lệ đổi 14/17, span mồ côi tăng 16/17, số span −9,6% đến +2,9%. **R7:** `bang_theo_o_2.py` (D4 xét mọi ca, có phân loại) → `bang-theo-o-2.{json,md}`, `cham/cham-moi-A-2.*`, `tap-moi-2.json`, `cham/spec-moi-2.json`; bảng và tổng trùng bản 1, D4 = false. **Sự cố:** lần tạo bản 2 đầu dừng ở `assert` khi thay chuỗi, file vẫn là bản chép của bản 1; lệnh kế tiếp chạy bản chép đó và ghi đè 6 đầu ra bản 1 — kiểm theo `SHA256SUMS`: 6/6 trùng byte; tạo lại bản 2 đúng, kiểm không còn tên đầu ra bản 1 trước khi chạy.
- ~02:20–02:55Z — Đếm số đơn tại `t` từng ca (chỉ đọc, `booking_db`, `ticket_db`): CPU-BOOK-1 5.225 → 24.921 (lặp 37.585), HTTP5-EVENT 5.873 → 36.190. Viết `results/T-069/dinh-chinh-1.md` (R1–R7, N1; giữ nguyên file gốc đã ghim). Ghi `docs/DECISIONS.md` mục "T-069: …" và `docs/WHY.md` WHY-102 (theo duyệt). `SHA256SUMS` giữ nguyên (318 file, `sha256sum -c` 0 lỗi); `SHA256SUMS-2` 348 file.

### Kết thúc phiên 3 (02:42Z 20/11)

1. Đã làm: đáp phản biện (chat); sửa theo duyệt: đính chính, bước 7.4, độ phủ 17 cặp, bảng bản 2, DECISIONS, WHY-102, LOG, STATE.
2. File đã thay đổi: `results/T-069/` (dinh-chinh-1.md, bang_theo_o_2.py, bang-theo-o-2.*, tap-moi-2.json, cham/*-2.*, phan-tich/bien-the/, phan-tich/do-phu-17.txt, SHA256SUMS-2), `docs/DECISIONS.md`, `docs/WHY.md`, LOG này, dòng T-069 `docs/STATE.md`. Máy: exp-obs `/srv/rca-lab/m1/t069-phan-tich/` (mới, rca:rca 750). Không đổi file đã ghim (`SHA256SUMS` 0 lỗi).
3. Kiểm: hash cấu hình biến thể = manifest-3; hash hai đầu đầu ra biến thể; bản 2 trùng bản 1 ở `#/hang`, tổng; số đếm độ phủ lấy lại từ JSON.
4. Kết quả, còn mở, cần Minh quyết: W3 — một ô tụt vượt ngưỡng (CPU-BOOK-1 1 → 3), tái lập, cùng ở P7 và ở mọi biến thể; D1–D5 không; **Minh quyết chấp nhận ô tụt cho demo hay giữ W3** (WHY-102). Bước xếp hạng giải thích được (điểm z một mẫu max trên kênh op gộp); nguồn sinh mẫu đuôi là ứng viên (DB lớn / code đường mua / tranh chấp CPU / dao động), chưa phân xử, phép phân xử ~2 chu kỳ cùng image khác trạng thái DB. Bản sao mốc sự kiện ở Ticket/Payment chưa dời (sau 20/11 22:16Z). Commit repo RCA chờ duyệt.
5. Bước tiếp: Minh quyết kế hoạch tiếp (chat 20/11); gửi prompt dưới cho Codex hoặc dừng phản biện.
6. Lệnh cuối: `find results/T-069 -type f ! -name 'SHA256SUMS*' | sort | xargs sha256sum > SHA256SUMS-2`.

## Prompt cho Codex — kiểm lại phản hồi và sửa T-069 (soạn 20/11/2026)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-069, tasks/T-069-v082-ban-ghim/.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: W3 (docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2), chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-069-v082-ban-ghim/SPEC.md, LOG.md (phiên 1–3); docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2–8.4; results/T-064/ho-so-chon.md §15–17; results/T-063/chay/dieu-kien-xac-nhan.md, results/T-063/thu3/dieu-kien-xac-nhan-3.md; results/T-067/thay-doi-main.md; docs/DECISIONS.md mục "T-069: …"; docs/WHY.md WHY-102.
- Phản biện và phản hồi trước: bản soát kết quả của Codex (chat 20/11/2026, R1–R7); phản hồi của người làm (chat 20/11/2026, N1–N5, đề xuất sửa); sửa theo duyệt của Minh: results/T-069/dinh-chinh-1.md và LOG phiên 3.
- Code và kết quả liên quan: results/T-069/ (SHA256SUMS = bản ghim lần đầu 318 file; SHA256SUMS-2 = toàn bộ sau sửa 348 file); results/T-069/phan-tich/bien-the/, phan-tich/do-phu-17.txt, bang_theo_o_2.py, bang-theo-o-2.{json,md}; results/T-064/cham/cham_dev3.py, src/m1_ft/, src/m1/ (span.py, e4.py); results/T-063/thu2/ca/; repo lab D:/Project/flashticket-rca-lab tại ddb22dc, ca5d6f5, 407b4f5; repo FlashTicket D:/Project/flash-ticket-platform tại 6b21ed55 và 36a3725d; môi trường chấm D:/RCA-flashticket/.venv/Scripts/python.exe; máy exp-app, exp-obs theo inventory/ của repo lab (chỉ đọc nếu Minh cho phép).
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tên bản phản biện được ghi>.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.
```

(`docs/review-prompt.md` chưa có khối cổng cho G6.)

### Đính chính hash (20/11/2026 ~13:00Z, phiên Claude điều phối T-070, theo `docs/techstack/ban-giao-dieu-phoi-2026-11-20/thong-nhat.md` §1.1)

- Dòng bước 9 (00:13Z) ghi `results/T-069/SHA256SUMS` có mã `410d9923…`. Mã đó là của danh sách khi `thay-doi-may.md` còn dừng ở M11 (Codex tái tạo được, `lich-su/05`). File cuối, sau khi thêm M12, M13 và dòng kiểm DB chỉ đọc vào `thay-doi-may.md`, có mã `cec9b3f1…` (318 file). Kiểm 20/11 12:4xZ: `sha256sum -c SHA256SUMS` 0 lỗi, `sha256sum -c SHA256SUMS-2` 0 lỗi (348 file, mã `160ab3ea…`). Không file nào khác đổi.

### Phản biện kiểm lại CX-05 (20/11/2026, Codex qua terminal, Minh cho phép) — ghi bởi phiên điều phối T-070 (giữ T-069)

- CX-05: thread `01a1faec-3f75-7222-b402-af3eaa4e487a`, tin cuối `results/T-070/codex/CX-05-tin-cuoi.md`. **Chấm W3 xác nhận độc lập:** V082 AC@1 9 → 9, AC@3 11 → 11, hạng cắt 13 → 14, K 4 → 4; P7 7 → 7, 9 → 9, 23 → 24, K 5 → 6; CPU-BOOK-1 hạng 3 ở cả lượt chính và lặp.
- F1 (CHẶN câu diễn giải): năm thao tác Booking (`INSERT tbl_orders`, `INSERT tbl_order_items`, `SELECT/UPDATE tbl_purchase_limits`, `POST …/purchase-snapshot`) **có ở ca cũ** (216/216/428/428/144 span ở `19b17e22`); `phan_tich_o.py` trừ tập kênh *có cờ*, nên đúng là "mới có cờ ở ca mới", không phải "kênh chỉ có ở bản ghim" (`dinh-chinh-1.md` §2). Code Booking có đổi vẫn là ứng viên.
- F2 (CHẶN câu diễn giải): "hai cách khớp ở kênh SQL lá" sai — phản ví dụ Keycloak `SELECT OUTBOX_ENTRY` 195,1 (thô) vs 192,42 (E1-U, khớp M1) ca cũ; 698,3 vs 696,21 ca mới (adapter làm tròn µs).
- F3, F4 KHÔNG CHẶN: thu hẹp câu CPU/DB/PSI theo ô và đại lượng; D4 bản 2 gộp "chưa phân loại" vào true — ghi giới hạn.
- Người làm: chưa kiểm lại từng số của F1–F2 bằng chạy lại (đối chiếu đường dẫn và lập luận: hợp lý). **Đề xuất sửa (chờ Minh duyệt):** `results/T-069/dinh-chinh-2.md` thay câu §2 (F1), câu §3 (F2), thu hẹp câu CPU/DB/PSI (F3), ghi giới hạn D4 bản 2 (F4); không đổi kết quả W3. Sau đó Minh nghiệm thu T-069.
- 22:05Z — **D5 (Minh duyệt "Duyệt cả năm")**: viết `results/T-069/dinh-chinh-2.md` theo CX-05 F1–F4; F1 người làm đếm lại độc lập từ `19b17e22.tgz` (194.714 span; 216/216/428/428/144) — trùng CX-05; F2–F3 dẫn số CX-05, ghi rõ người làm chưa chạy lại; không đổi kết quả W3, không sửa file đã ghim. sha256 `e101a057561463f0…`. Còn: Minh nghiệm thu T-069; commit theo R2(b).
  - Đính chính dòng trên: giờ kiểm F1 trong file là ~22:04Z (đã sửa, trước ghi "~22:10Z" là ước); sha256 mới `a9a93a751ca90e92…` thay hash ở dòng trên.
- 05:21Z — **Minh nghiệm thu T-069** (chat 23/11, "Approve Q1–Q11", mục Q4): nghiệm thu với ngoại lệ CPU-BOOK-1 (R1); nguồn mẫu đuôi (DB tích lũy / code đường mua / tranh chấp CPU) còn mở. Ghi DECISIONS khối 23/11; dòng STATE chuyển "xong". (Ghi bởi điều phối T-070, phiên giữ T-069.)
