# T-062 — Lượt chạy liên tục: chuẩn bị chặng 1–3 và lượt phát triển đầu của chặng 4 trên FlashTicket

- **Trạng thái:** đã duyệt (12/11/2026, chat). Minh: “giờ tôi sẽ treo máy qua đêm, tôi để bạn làm toàn bộ cho hết chặng 4”; “hãy làm mọi thứ có thể cho đến khi phải chờ tôi duyệt”; “duyệt dùng codex, … model sol 6.1 high, cấp full access. bạn hãy điều phối”; “nhập mật khẩu tôi duyệt cho cả codex và claude nếu cần, … đọc file mật khẩu nếu cần”; “tôi sẽ treo máy hẳn 24h liên tục”. Kế hoạch đêm (Claude trình trong chat cùng ngày) được duyệt qua các câu trên.
- **Điều phối:** Claude (phiên điều phối). **Người làm:** Claude (việc khó: code, M1, giao diện, phân tích) và Codex CLI (`gpt-6.1-sol`, reasoning high, full access; việc theo kịch bản). **Phản biện:** chưa chỉ định; sáng mai Minh quyết.
- **Thuộc:** `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` chặng 1a, 2, 3 (cho các ô phát triển), 4 (lượt đầu), nhánh G (G2).

## Mục tiêu và giới hạn trung thực

Một đêm **không** đủ để xong chặng 4: mỗi chu kỳ lỗi 30 phút (10 nền, 10 lỗi, 10 hồi phục); chọn và tinh chỉnh M1 cần tiêu chí Minh duyệt trước khi xem kết quả. Đích của T-062:

1. FlashTicket bản quan sát mới (nhánh `rca/quan-sat-log`) chạy trên `exp-app`, CI trên PR xanh.
2. Bộ kiểm chất lượng dữ liệu R-01–R-10 (chặng 1a) chạy và báo cáo.
3. Máy tải `3.24.8.49` chạy k6 theo kịch bản cố định (chặng 2).
4. Bộ tiêm lỗi cho **7 ô phát triển** của T-059 (EVENT-DB-LAT, REDIS-BOOK, HTTP5-EVENT, SLOW-BOOK, NET-GW-BOOK, CPU-BOOK, FLASH-HEALTHY), xác nhận can thiệp (B4).
5. Mỗi ô phát triển ít nhất **một** chu kỳ, M1 **bản khóa P7** (không chỉnh) chạy trên từng chu kỳ, kết quả chuyển định dạng 0.2 (T-061).
6. Giao diện G2 trên Grafana `exp-obs` đủ dùng: danh sách sự cố → đồ thị → hạng → bằng chứng → liên kết Tempo/Loki/Prometheus; bản phát lại có đáp án tách riêng.
7. Bàn giao sáng: `results/T-062/bao-cao-sang.md` + bản SPEC chặng 4 (tiêu chí chọn) để Minh duyệt.

Ô nào không kịp hoặc không xác nhận được can thiệp: ghi lý do, bỏ qua, không ép.

## Luật cứng của lượt (mọi agent)

1. **Không push `main`**, không merge PR, không chạy workflow `cd.yml` (push `main` tự triển khai lên production máy 84). Chỉ nhánh `rca/quan-sat-log` và PR.
2. **Không chạm máy 84** (`52.64.237.84`, khóa `FlashTicket-Control-Diagnosis.ppk`) và không chạm server production qua CD.
3. **Không sửa** `src/` (code M1), mọi `results/T-0xx/` cũ, `docs/` (trừ dòng T-062 trong `docs/STATE.md`), SPEC đã duyệt khác. Đầu ra mới chỉ ở `results/T-062/` và `tasks/T-062-dem-chang-1-4/`.
4. **Không chọn, không tinh chỉnh M1.** Chỉ chạy bản khóa P7 (`results/T-058/dem-2026-11-10/m1-p7-config.json`, runner T-058). Phép thử khác (bỏ E1/E2/E5…) chỉ được ghi là *khám phá*, không dùng để chọn.
5. **Cách ly nhãn:** M1 chỉ nhận `t` (giây nguyên) qua `request.json` của ca, mã ca mờ. Sổ tiêm lỗi ở `results/T-062/tiem-loi/so.jsonl` (chỉ ghi thêm, có hash nối dòng) và nhật ký điều khiển **không** đi vào bộ đọc M1. Ghép đáp án chỉ ở lớp phát lại sau khi đã băm đầu ra cả đợt (`results/T-061/phat-lai.py`).
6. **Không đọc dữ liệu khóa** (test RE2-TT, Nezha, RE3), không tải dữ liệu > 5 GB.
7. **Không xóa** dữ liệu hay container của người khác; chỉ tạo mới trong không gian của lượt. Mọi thay đổi trên máy ghi vào `results/T-062/ha-tang/thay-doi.md` (lệnh, giờ UTC, hash cấu hình trước/sau).
8. **Mật khẩu/khóa:** được dùng theo duyệt của Minh. Không in giá trị vào LOG, báo cáo, prompt. Riêng Claude: theo chính sách của mình, không tự nhập mật khẩu đăng nhập vào hệ thống ngoài máy cục bộ; bước nào cần đăng nhập bằng mật khẩu (token Keycloak cho tải, v.v.) giao Codex.
9. **Dừng khẩn:** nếu tồn tại `D:/RCA-overnight/STOP` thì dừng ở ranh giới chu kỳ gần nhất, ghi checkpoint, không làm tiếp.
10. **Luật 21 (lỗi giữa chừng):** lỗi hạ tầng chỉ dừng ô đó; dữ liệu đã thu giữ nguyên; không chạy lại ô đã xong trừ khi lỗi ảnh hưởng tính đúng (ghi lý do).

## Máy và truy cập

| Máy | Địa chỉ | Truy cập | Vai trò |
|---|---|---|---|
| `exp-app` | Oracle `129.221.208.47` (nội bộ `10.0.0.158`), ARM 2 OCPU 11 GB | `ubuntu`, khóa `D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key`, known_hosts `D:/RCA-ext/overnight-T058/out/known_hosts`; mẫu lệnh `results/T-058/dem-2026-11-10/remote.ps1` | FlashTicket + bộ tiêm |
| `exp-obs` | Oracle `213.35.116.128` (nội bộ `10.0.0.215`) | `ubuntu`, khóa `D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key`, cùng known_hosts; compose phải có `-p flash-ticket-obs-pinned` | Prometheus/Loki/Tempo/Grafana (Infinity đã cài, `results/T-061/exp-obs/README.md`) |
| Máy tải | AWS `3.24.8.49`, x86 2 vCPU 7,7 GB (máy exp-app AWS cũ) | `ubuntu`, khóa `D:/RCA-ext/keys/Hahaa123.pem`, known_hosts `D:/RCA-ext/keys/known_hosts` | k6 |
| Laptop | Windows | `codex` CLI, `C:\Program Files\GitHub CLI\gh.exe` | điều phối, nhận/kiểm |

Mở cổng: Security List của subnet chứa `exp-app` cho `3.24.8.49/32` TCP 8081, 8080 (Minh làm trên console); `iptables` trên `exp-app` agent tự mở cho đúng nguồn đó. Nếu tải từ ngoài không vào được sau 30 phút thử, chạy k6 trên `exp-obs` (cùng VCN) và ghi sai lệch.

## Thứ tự và phân công (runbook)

| Bước | Việc | Ai | Xong khi |
|---|---|---|---|
| A1 | Repo FlashTicket `D:/Project/flash-ticket-platform`: review toàn bộ diff (đã sao lưu `D:/RCA-ext/backup-flashticket-20261112/`), tách nhóm thay đổi, sửa lỗi; `mvnw clean verify` 7 service (bản thường) + booking/event `-P rca-test`; commit lên nhánh `rca/quan-sat-log`, push, mở PR vào `main` bằng `gh`; theo dõi CI, sửa tới khi xanh. **Không merge.** | Claude | PR có CI xanh, hoặc ghi rõ phần đỏ |
| A2 | Build image ARM trên `exp-app` từ đúng commit nhánh (như KP-01); booking, event bản `-P rca-test`; triển khai thay bản đang chạy; giữ cấu hình agent/Collector; ghi digest | Claude | 8 service healthy, telemetry tới `exp-obs` |
| B1 | Bộ kiểm chất lượng dữ liệu R-01–R-10 (chặng 1a) trong `results/T-062/kiem-du-lieu/`; chạy sau A2 | Claude (thiết kế), Codex (chạy định kỳ) | Báo cáo đạt/thiếu từng R |
| C1 | Máy tải: cài Docker, k6 ghim phiên bản, chrony; kịch bản từ `deploy/rca-test/workload.js` (hỗn hợp cố định, nhịp cố định); token Keycloak làm mới định kỳ (luồng PKCE như `results/T-058/dem-2026-11-10/auth.py`); chạy thử 5 phút | Codex | k6 chạy ổn định, số liệu lưu `results/T-062/tai/` |
| D1 | Bộ tiêm trên `exp-app`: Toxiproxy (JDBC event_db, Redis booking; thử Gateway→Booking), Pumba/stress cho CPU booking, hook `rca-test` qua `deploy/rca-test/faultctl.py`; sổ tiêm lỗi; đầu dò xác nhận độc lập | Claude | 7 ô có lệnh bật/tắt và đầu dò |
| D2 | B4: xác nhận can thiệp từng ô (2–5 phút/ô, ngoài chu kỳ chính) | Claude | Bảng xác nhận từng ô |
| E1 | Bộ chạy tự động (`results/T-062/chay/`): mỗi ô 1 chu kỳ 10/10/10, ca bình thường xen giữa; mã ca mờ; sau mỗi chu kỳ đóng gói dữ liệu như T-058 (stager), chạy M1 bản khóa hai lần, kiểm trùng SHA | Claude viết, Codex trông | Đủ chu kỳ hoặc hết giờ |
| E2 | Chuyển định dạng 0.2 (`results/T-061/chuyen-doi.py`), băm cả đợt, file chỉ mục; đẩy lên `exp-obs:/opt/flash-ticket-obs/rca-ket-qua/`; bản phát lại có đáp án để riêng `…/phat-lai/` | Claude | Danh sách sự cố trên Grafana cập nhật |
| G1 | Dashboard G2 trên Grafana `exp-obs` (provisioning trong `pinned/provisioning/dashboards/`): danh sách → đồ thị (nhãn dễ hiểu: đỏ nghi nguồn `#hạng`, cam kéo theo, xám bình thường, tím `?` thiếu dữ liệu) → bảng hạng → bằng chứng → liên kết Explore; lớp thao tác (hướng 1) nếu kịp; trang phát lại có đáp án tách riêng | Claude (phiên giao diện) | Minh mở được, đổi ca được |
| H1 | Bàn giao: `results/T-062/bao-cao-sang.md` (đã làm, kết quả từng ô, cách xem, phần mở, việc chờ duyệt) + `results/T-062/spec-chang-4-de-xuat.md` | Claude | Có hai file |

Song song: A1 (laptop) ∥ C1 (máy tải, Codex) ∥ G1 (phiên giao diện). A2 → B1, D1 → D2 → E1 → E2. Mỗi máy chỉ một agent được thay đổi tại một thời điểm: `exp-app` = phiên điều phối Claude; máy tải = Codex; Grafana `exp-obs` = phiên giao diện.

## Hết lượt dùng và tiếp nhận

- Codex hết lượt (hồi khoảng 4 giờ sau): phiên điều phối ghi checkpoint, tự làm tiếp phần đó hoặc chờ; khi hồi thì `codex exec resume --last` hoặc giao brief mới.
- Claude hết lượt (hồi khoảng 1,5 giờ sau): lịch `t062-tiep-nhan` (Claude scheduled task, mỗi giờ) mở phiên mới đọc `CHECKPOINT.md`; nếu nhịp tim trong `CHECKPOINT.md` cũ hơn 40 phút thì tiếp quản theo `PROMPT-DIEU-PHOI.md`, ngược lại thoát.
- Mọi agent cập nhật `CHECKPOINT.md` (dòng nhịp tim UTC, bước đang làm, việc tiếp) sau mỗi bước và ít nhất 30 phút một lần.

## Đầu ra

`results/T-062/`: `ha-tang/`, `kiem-du-lieu/`, `tai/`, `tiem-loi/` (sổ, đầu dò), `chay/` (runner, nhật ký), `ca/<mã mờ>/` (gói dữ liệu, đầu ra M1, định dạng 0.2), `giao-dien/`, `codex/` (nhật ký từng lần giao việc), `bao-cao-sang.md`, `spec-chang-4-de-xuat.md`, `manifest.json` (SHA-256 mọi đầu ra).

## Chưa kiểm / rủi ro

Đăng nhập Keycloak từ máy ngoài (KC_HOSTNAME ghim nội bộ); chèn proxy Gateway→Booking khi Gateway dùng discovery; Pumba trên ARM; CI cần dịch vụ DB/MQ; Codex có thể vượt phạm vi (giảm thiểu bằng luật trên, sao lưu, nhánh, và kiểm `git diff` sáng mai).
