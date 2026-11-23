# T-073 — Thiết kế dịch vụ RCA trực tuyến chế độ (b)

Bản 1, 20/11/2026, phiên `rca-w5` (Claude). SPEC bước 1. Code: worktree lab `D:/Project/rca-lab-wt/T-073`, nhánh `t073-truc-tuyen` (từ `407b4f5`), thư mục `campaigns/online/`. Chưa commit (luật cứng 11).

## 1. Việc dịch vụ phải làm

Kế hoạch giai đoạn 2 §8.2 W5 và §7 G3: nhận cảnh báo Grafana → gom thành sự cố → xuất dữ liệu theo t̂ đủ `[t̂−300, t̂+300)` → chạy lõi M1 đã ghim (V082, bản chụp `b0f79a4d…`) → ghi kết quả G1 → Grafana hiện kết quả trong N phút đã khai. Chế độ (b): mốc t của lõi là t̂ của báo động (D3, T-043 SPEC B1.1); không đọc sổ tiêm; giữ riêng giờ nhận webhook.

Task này cài đặt và nghiệm thu chức năng. Không đánh giá độ chính xác (W6–W7).

## 2. Luồng

```
luật Grafana (T-072) ──webhook──▶ webhook_receiver.py ──▶ spool canh-bao-YYYYMMDD.jsonl (giờ nhận, thân nguyên văn)
                                                              │
orchestrator.py (vòng 5 s) ◀──────────────────────────────────┘
  incidents.py: bản ghi I1 (t̂ từ startsAt, giờ nhận), gom sự cố, lưu su-co/<mã>.json
  chờ tới t̂ + 600 + F (F = 150 s)
  1 stage_b.py      (root)  gói [t̂−600, t̂+600): capture Collector + Prometheus → m1/cases/<mã mờ>/
  2 run_m1.py       (rca)   P7, lưu đầu vào lõi outputs/<mã mờ>/method-input.json
  3 xuat_bo_sung.py (ubuntu) --t t̂, live-down theo lần dò mới nhất (WHY-99) → m1/bo-sung/<mã mờ>/
  4 chay_ca.py V082 (rca)   bản chụp ghim; kiểm hash cấu hình như runner4.py; chạy hai lần, trung_sha
  5 check_core_input.py (root) dữ liệu lõi thực nhận: t lõi, N/A, số span/log/hàng metric, nguồn không phủ
  6 g1_b.py         (root)  G1 (hàm của sau_v082.py) + khối che_do_b → rca-results/t073-<lượt>/
Grafana đọc rca-results qua mount chỉ đọc; đổi nguồn hiển thị sang t073-* chỉ ở S4 (I9).
```

Bước 2–4 và 6 gọi đúng các file của đường runner4 (T-069), không sửa: `run_m1.py`, `xuat_bo_sung.py`, `chay_ca.py` của bản chụp, các hàm `nap_bo_xuat`, `dung_mot_ca`, `do_thi_dich_vu` của `sau_v082.py` (import, không chép). Chỉ bước 1 là code mới có phần chọn dữ liệu (chép nguyên văn từ `stage_m1.py`, xem §4).

Bỏ khỏi đường tới G1 so với runner4: `safe_export.py case` + `tar` (gói để kéo về laptop). Hai bước này không đổi kết quả hiển thị; làm sau G1 nếu cần lưu gói (chưa cài, xem §10).

## 3. Vì sao gói `[t̂−600, t̂+600)` và chờ tới t̂ + 600 + F

SPEC bước 3 đòi: cùng t thì đầu vào lõi trùng gói cũ. Đọc lõi ghim (`goc-12` = bản chụp, trùng 149/149 file, `kiem/ban-chup-b0f79a4d-exp-obs.sha256`):

- `m1/adapter_flashticket.py::normalize_metrics` **không cắt metric theo cửa sổ M1**: mọi điểm trong `prometheus.json` của gói vào `metrics` của đầu vào lõi. Ca dev `1e5debb6`: 2.501 hàng metric ngoài `[t−300, t+300)`, 1.220 ở N, 1.220 ở A (`check_core_input.py`, LOG 13:13Z).
- `normalize_spans`, `normalize_logs` tính `coverage.khoang` từ mọi bản ghi đã đọc, kể cả ngoài cửa sổ; `coverage` nằm trong `params` của đầu vào.
- `H8-adapter` (một thành phần của V082) nối chuỗi container trên cả gói `[t−600, t+600]`.

Vậy gói hẹp `[t̂−300, t̂+300)` cho đầu vào lõi khác byte, và kết quả V082 có thể khác kết quả đã nghiệm thu ở T-064/T-069. Phương án đã xét:

| Phương án | Kết quả có sớm nhất | Đầu vào lõi so với đường đã nghiệm thu | Chọn |
|---|---|---|---|
| Gói `[t̂−600, t̂+600)`, chờ t̂+600+F | ~t̂ + 16–20 phút | Trùng byte khi dữ liệu nguồn như nhau (đã kiểm, §8) | **Có** |
| Gói `[t̂−300, t̂+300)`, chờ t̂+300+F | ~t̂ + 11–15 phút | Khác (metric ngoài cửa sổ, `coverage`); cần phép kiểm tương đương riêng trên dev | Không, trừ khi Minh chọn đổi N lấy độ trễ |
| Sửa adapter để cắt metric | — | Sửa lõi ghim | Cấm (SPEC) |

Hệ quả: N không thể nhỏ hơn khoảng 12,5 phút (600 + 150 s) cộng thời gian xử lý. Dữ liệu sau t̂+300 vào lõi chỉ qua metric và `coverage`; ở chế độ (b) đó là dữ liệu sau báo động. Đây là đặc tính có sẵn của đường V082, không do dịch vụ thêm.

## 4. Bộ xuất theo t̂ (`stage_b.py`)

Giữ nguyên phép chọn của `stage_m1.py`: `canonical`, `traces`, `logs` (span chọn khi `start ≥ t−600` và `end < t+600`; log theo `timeUnixNano`), `collect_metrics(url, t−600, t+600, 15)`, `inventory.json`, `request.json = {"t": t}`. Ba khác biệt:

1. **Chốt file trước khi đọc.** `stage_m1.py` liệt kê thư mục một lần rồi mở lần lượt. Đọc 21 file 100 MB mất hàng chục giây tới vài phút; nếu Collector quay vòng giữa liệt kê và mở `traces.jsonl`, file vừa đổi tên không có trong danh sách và gói mất phần dữ liệu mới nhất — đúng phần chứa sự cố. `stage_b.py` mở mọi file ứng viên trước, giữ file descriptor, lấy giới hạn bằng `fstat`, rồi liệt kê lại; có inode mới chưa mở thì làm lại.
2. **Bỏ file cũ.** File có mtime < t̂ − 600 − 300 không thể chứa bản ghi có mốc ≥ t̂ − 600 (Collector ghi bản ghi sau khi nó kết thúc), trừ khi đồng hồ exp-app lệch exp-obs hơn 300 s. Bỏ các file này không đổi nội dung gói, giảm lượng đọc từ ~2 GB xuống vài trăm MB. Giả định đồng hồ lệch dưới 300 s: **đã kiểm** 20/11 13:44Z bằng `chronyc tracking` (exp-obs +0,05 ms, exp-app +0,24 ms so NTP); nên kiểm lại đầu S4.
3. **Manifest** ghi `mode: "b"`, file đã mở/bỏ, cờ `vong_co_the_mat_dau` (không còn file nào cũ hơn mốc cắt → phần đầu cửa sổ có thể đã bị quay vòng xóa; cờ thận trọng).

`--prom-tu-file` chỉ dùng cho phép kiểm trên ca cũ; dịch vụ không truyền cờ này.

## 5. Bản ghi cảnh báo I1, t̂ và gom (`incidents.py`)

- **Ba thời điểm tách riêng** (HOP-DONG I1): `t_hat` (từ cảnh báo), `nhan_webhook_utc` (bộ nhận đo khi request tới, trước khi đọc thân), `du_lieu_loi` (khoảng và tín hiệu lõi thực nhận, bộ điều phối điền sau bước 5). Kèm mã luật (`__alert_rule_uid__`, hoặc uid trong `generatorURL`, hoặc `alertname`), nhãn, giá trị, `eval_interval`, `for` (nếu luật để trong annotation), fingerprint.
- **Nguồn t̂ (chưa kiểm):** `alerts[].startsAt` của webhook. Giả định: Grafana unified alerting đặt `startsAt` bằng thời điểm của lần đánh giá chuyển trạng thái sang Alerting, không phải giờ gửi. Sai thì t̂ lệch, mọi kết quả (b) lệch theo. T-072 sở hữu phép xác nhận trên bản Grafana chạy ở exp-obs (E3); nếu chốt nguồn khác, đổi `--nguon-t-hat` (hỗ trợ `annotation:<khóa>`). t̂ của lõi = floor(startsAt) giây.
- **Gom: theo `results/T-072/quy-tac-gom.json` bản `T072-gom-1`** (đề xuất của T-072, khai trước E2, chờ Minh duyệt cùng T-072). Khoảng cháy của một instance = (fingerprint, t̂) → `[t̂, t_hết)`, t_hết lấy từ `endsAt` của webhook `resolved`. Khoảng cháy mới nhập sự cố cùng lớp nếu t̂ ≤ max t_hết + 300 s (còn khoảng đang cháy thì max t_hết = +∞); t̂ sự cố = min t̂. Chỉ lớp `t072_loai = he-thong` chạy RCA; `quan-sat`, thiếu nhãn, `DatasourceError`, `DatasourceNoData` → sự cố quan sát, chỉ ghi. Khác bộ chấm offline của T-072 ở một điểm do chạy trực tuyến: RCA bắt đầu ở t̂ + 600 + F theo t̂ lúc đó; khoảng cháy đến muộn có t̂ nhỏ hơn được nhập và gắn cờ `t_hat_giam_sau_khi_chay`, không chạy lại. Hệ quả cần biết: hai lỗi cách nhau mà cảnh báo của lỗi đầu chưa tắt + 300 s sẽ thành một sự cố, chỉ một lượt RCA tại t̂ đầu. Cùng (fingerprint, t̂) → bản lặp, chỉ đếm.
- **t̂ theo T-072:** "lần đánh giá đầu tiên instance ở trạng thái Alerting, lấy từ lịch sử trạng thái của Grafana, không lấy giờ webhook". Dịch vụ lấy `startsAt` trong thân webhook (là trạng thái của luật, không phải giờ gửi); hai nguồn trùng nhau là giả định chưa kiểm, phải đối chiếu ở E3. Nếu lệch, dịch vụ phải đọc lịch sử trạng thái (Loki) — là truy vấn mới, chưa cài.
- Schema I1: `T072-i1-0` (`results/T-072/i1-schema.json`). Từ lượt 2, mỗi khoảng cháy mang bản ghi đúng schema ở khóa `i1` (kiểm `jsonschema` 0 lỗi cho lớp hệ thống và `DatasourceError`); mã luật lấy từ nhãn `t072_uid`, tham số từ annotation `t072_*`. Khác biệt còn lại (cảnh báo thiếu nhãn `t072_*`, cách băm `ma`, nguồn t̂ chuẩn là lịch sử trạng thái) ghi ở LOG lượt 2, chờ điều phối chốt.

## 6. Nơi ghi trên exp-obs

| Đường dẫn | Chủ | Ai ghi | Ghi gì |
|---|---|---|---|
| `/srv/rca-lab/runs/t073-<lượt>/` | ubuntu 700 | bộ nhận, bộ điều phối | `spool/`, `su-co/<mã>.json`, `nhat-ky.jsonl`, `ca/<mã mờ>/prometheus-bo-sung.json` |
| `$RCA_M1_ROOT/cases/<mã mờ>/` | root:rca | stage_b (root) | gói ca |
| `$RCA_M1_ROOT/{outputs,v082}/<mã mờ>/` | rca | run_m1, chay_ca (rca) | đầu vào lõi, đầu ra |
| `$RCA_M1_ROOT/bo-sung/<mã mờ>/` | root:rca | bộ điều phối qua `sudo install` | gói bổ sung |
| `/srv/rca-lab/rca-results/t073-<lượt>/` | root | g1_b (root) | G1, chỉ mục, đồ thị dịch vụ |

Dev: `RCA_M1_ROOT=/srv/rca-lab/m1/t073-dev`, lượt `runs/t073-dev-00n`, G1 `rca-results/t073-dev-001`, code chép ở `runs/t073-dev-code/`. Vì `runs/` là ubuntu 700, user rca không đọc được code ở đó: dev gọi `run_m1.py` của `/opt/rca-lab` (cùng `407b4f5`, `cmp` trùng) qua `RCA_RUN_M1`. Ở S4, code chạy từ `/opt/rca-lab` khi commit được duyệt (I5), không cần biến này.

`g1_b.py` từ chối ghi vào thư mục không mang tên `t073-*` hoặc vào `t065-l11-001` (I9); chỉ đọc siêu dữ liệu bản từ chỉ mục `t065-l11-001`.

## 7. Ring capture của Collector

Cấu hình `observability/collector/gateway.yaml`: `file/traces` 100 MB × (20 bản sao + 1 đang ghi); `file/logs` 100 MB × (10 + 1). Đo chỉ đọc lúc 2026-11-20 12:59Z (`ls --full-time`, LOG 12:59Z), lúc không có tải k6:

| Tín hiệu | Thời gian một file 100 MB | Vòng giữ được | Cần từ lúc stage |
|---|---|---|---|
| traces | ~15,8 phút | ~5,3 giờ | t̂ − 600 tới t̂ + 600, stage lúc ~t̂ + 12,5 phút → cần ~22,5 phút + thời gian stage |
| logs | ~42 phút | ~7 giờ | như trên |

Lúc không tải còn dư ~14 lần. Vòng chỉ hụt khi tốc độ ghi tăng hơn ~10–14 lần. **Chưa đo dưới tải ×1 của E5.** Đo được bằng `ls --full-time` (không truy vấn) trong lượt nền E2/E4 do T-071 làm chủ; đề xuất điều phối nhờ T-071 ghi một danh sách khi tải chạy, hoặc T-073 đo đầu khung S4 trước khi tiêm. Cờ `vong_co_the_mat_dau` trong manifest ghi trường hợp hụt.

## 8. Phép kiểm trên ca cũ (SPEC bước 3)

`check_old_case.py`: dựng capture giả từ `raw-*.jsonl` của gói cũ (lọc lại cùng cửa sổ giữ nguyên byte), chạy bộ điều phối chế độ `mot` với t của gói cũ, `prometheus.json` và gói bổ sung cũ; so sha256: năm file dữ liệu của gói, `method-input.json` của P7, `method-output-{1,2}.json` của V082, gói bổ sung, ba file G1 (bỏ khối `che_do_b` và trường đường dẫn/nhãn nguồn). Kết quả ở `kiem/so-ca-cu.json`; LOG ghi từng ca. **3/3 ca (`1e5debb6`, `0bec9eca`, `2d5a56fe`) trùng mọi mục.** Thêm: `xuat_bo_sung.py` chạy sống lại cho t của `1e5debb6` (19/11) ra file trùng byte gói bổ sung cũ (14,85 s).

Phép này chứng minh code mới không đổi đầu vào/đầu ra lõi khi dữ liệu nguồn như nhau. Nó không chứng minh capture sống đủ dữ liệu ở t̂+750 (phép flush, §9) hay Prometheus trả lại đúng dữ liệu cũ.

## 9. Flush F

F = 150 s lấy từ runner4 (`wait_until(t + PHASE + 150)` sau mốc cuối gói). Đường cũ cũng stage tại mốc cuối gói + 150 s, nên với cùng cửa sổ gói, khoảng dư cho dữ liệu đến muộn như cũ. **Chưa đo trực tiếp** độ trễ tới capture và Prometheus. Phép đo: stage cùng t̂ hai lần (t̂+750 và t̂+1200) trên capture sống rồi so hash; cần chủ exp-obs của khung đồng ý (I11), đề xuất làm đầu S4 hoặc khi điều phối cho.

## 10. Webhook tới bộ nhận: đường mạng chưa có

Grafana chạy trong mạng bridge (`172.19.0.3`). INPUT của exp-obs chỉ nhận `10.0.0.0/24`, `lo`, cổng 22, còn lại REJECT (`iptables -S INPUT`, LOG 12:59Z). Tiến trình trên host không nhận được webhook từ container Grafana. Phương án (cần Minh/điều phối chọn; đều là thay đổi máy):

| Phương án | Thay đổi | Ghi chú |
|---|---|---|
| a. Thêm luật INPUT cho `172.19.0.0/16` tới một cổng | tường lửa | Đổi cấu hình bảo mật máy |
| b. Chạy bộ nhận trong container gắn mạng `flash-ticket-obs-pinned_default` | Docker trên exp-obs, có thể thêm vào compose | Grafana gọi theo tên dịch vụ; spool gắn vào `/srv/rca-lab/runs/t073-*` |
| c. Không dùng webhook: bộ điều phối hỏi API trạng thái luật Grafana | cần token Grafana | t̂ lấy thẳng từ trạng thái luật; vẫn ghi giờ nhận là giờ hỏi |

T-072 gặp cùng vấn đề khi kiểm giao nhận ở E3 (I12). Bộ nhận hiện chạy được cả hai cách (a)/(b): chỉ cần `--nghe ip:cổng`.

## 11. Lỗi giữa chừng

- Lỗi một bước chỉ chặn sự cố đó (luật 21a). Stage lỗi: stage lại một lần với mã mờ mới, giữ thư mục cũ (như runner4). P7/V082/G1 lỗi: không tự chạy lại; giữ kết quả lần đầu; ghi `loai_loi` sơ bộ (`ha_tang`, `phuong_phap_hoac_cai_dat_chua_phan_loai`, `hien_thi`), phân xử do người làm.
- P7 lỗi đúng loại đã nhận diện ("Multiple runtime series map to one logical metric…", container bị tạo lại trong gói, ví dụ RECREATE-PAY): ghi lỗi P7, vẫn chạy V082 (H8-adapter dựng lại đầu vào từ gói); `check_core_input.py` kiểm đầu vào V082 thực dùng (dựng lại bằng đường ghim, chỉ nhận khi trùng `input_sha256` của V082), không cần đầu vào P7 (CX-06 điểm 5). Lỗi P7 khác vẫn dừng sự cố. Kiểm trên gói RECREATE-PAY cũ: chờ E2 xong.
- Phủ cửa sổ: theo mẫu thực từng nguồn (lỗ lớn nhất), trace và metric bắt buộc, log không bắt buộc (CX-06 điểm 6; `khai-truoc-e5.json#/tieu_chi/ket_qua_phu_cua_so`).
- `STOP` toàn cục (`/srv/rca-lab/runs/STOP`) hoặc `<lượt>/STOP`: không bắt đầu bước mới.
- Một bộ điều phối một thư mục lượt (`flock`).
- Bộ nhận tách khỏi bộ điều phối: bộ điều phối dừng thì cảnh báo vẫn vào spool; khởi động lại đọc tiếp từ vị trí đã lưu.

## 12. Không đưa nhãn vào phương pháp (luật cứng 6)

Mọi file trong `campaigns/online/` không chứa đường dẫn sổ tiêm (`/srv/rca-lab/ledger`, `so-tiem-loi`), không đọc tên ô. Kiểm bằng grep trước khi trình commit (§13). Đầu vào của dịch vụ: spool webhook (tín hiệu của luật), capture Collector, Prometheus. Nhãn cảnh báo (tên luật, route) chỉ vào khối hiển thị `che_do_b`, không vào gói ca hay đầu vào lõi.

## 13. Còn mở

- I1: đối chiếu `results/T-072/i1-schema.json` khi có.
- Nguồn t̂ (`startsAt`) chưa kiểm trên bản Grafana chạy.
- Đường webhook (§10).
- F chưa đo trên capture sống; tốc độ quay vòng dưới tải chưa đo; độ lệch đồng hồ chưa đo.
- Quy tắc gom tạm (chờ W4).
- Lưu gói `safe_export` + `tar` sau G1: chưa cài.
- Tên bản G1 (`results/T-073/g1-0.3.md`).
- Đọc qua API Tempo/Loki/Prometheus (P9b): OPEN, ngoài task.
