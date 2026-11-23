# T-073 — W5: dịch vụ RCA trực tuyến chế độ (b)

- **Trạng thái:** đã duyệt triển khai 20/11/2026 theo quyền Minh cho phiên điều phối (SPEC T-070), **trừ** các mục "chờ Minh". Soạn bởi phiên điều phối T-070.
- **Người làm:** Claude (phiên `rca-w5`, mức High).
- **Người phản biện:** Codex.
- **Thuộc gói MRP:** P9, P10 — **Cổng:** chuẩn bị G6.

## Mục tiêu

Kế hoạch giai đoạn 2 §8.2 W5 (nguyên văn yêu cầu ở đó): dịch vụ nhận cảnh báo → gom sự cố → xuất dữ liệu theo t̂ đủ `[t̂−300, t̂+300)` → chạy lõi M1 đã ghim → ghi kết quả G1 → Grafana hiện kết quả trong N phút đã khai. Chế độ (b): không đọc sổ tiêm; mốc theo D3 (T-043 SPEC); giữ riêng giờ nhận webhook. Nguồn: §7 G3; MRP P10, Q-28; DT18 "giao diện minh họa kết quả phân tích".

Task là **cài đặt và nghiệm thu chức năng** trên ca khai trước. Không đánh giá độ chính xác chế độ (b) (W6–W7).

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác | Phép kiểm | Phần còn mở |
|---|---|---|---|
| Lõi có thực nhận đúng dữ liệu quanh t̂? | Chỉ `t = t̂` đúng nhưng cửa sổ hay tín hiệu sai; ring capture của Collector đã quay vòng | Kiểm cửa sổ và số mẫu/tín hiệu thực vào lõi; ghi riêng thiếu dữ liệu phủ, lỗi xử lý, ca bỏ sót | Đọc qua API Tempo/Loki/Prometheus (P9b) OPEN |
| N phút đặt bao nhiêu? | Thời lượng chu kỳ cũ (~31 phút) không phải phép đo | Đo trên dev (ca cũ đã lưu, phát lại) rồi khai N **trước khi tiêm** | — |
| Grafana có hiện kết quả mới, và ca cũ vẫn xem/phát lại được khi đổi nguồn JSON? | Ca cũ hiển thị đúng chỉ kiểm một phần đường chạy | Kiểm dashboard hiện hành, lưu trữ, phát lại ở S4 | — |

## Đầu vào

- Repo lab `407b4f5`: `campaigns/runner/stage_m1.py` (ghi `mode: a`, đọc capture `/srv/rca-lab/collector-gateway/capture`), `safe_export.py`, `xuat_bo_sung.py` (cửa sổ `--t` tùy ý, `live-down` WHY-99), `run_m1.py`, `sau_v082.py` (chỉ mục G1 `rca-results/t065-l11-001`), `runner4.py` (`chay_v082`).
- Lõi M1: bản chụp `/srv/rca-lab/m1-snapshots/b0f79a4d…` (không sửa); cấu hình V082 (hash trong `runner4.py`).
- G1: T-061 (định dạng kết quả), T-065/T-068 (dashboard). D3: `tasks/T-043-thiet-ke-rca-m1/SPEC.md`.
- Ca cũ đã lưu để phát triển: `results/T-069/thu/`, `results/T-063/thu2/ca/*.tgz` (chỉ dữ liệu phương pháp; không đọc đáp án hay sổ tiêm ở phía phương pháp).
- Hợp đồng `HOP-DONG.md` (I1, I3, I5, I7, I9, I10, I11, I12), `LICH-MAY.md` (S4).

## Đầu ra

- Code ở worktree lab `D:/Project/rca-lab-wt/T-073` nhánh `t073-truc-tuyen`: bộ nhận webhook chế độ (b), bộ gom sự cố, bộ xuất theo t̂ (file mới, ví dụ `campaigns/online/stage_b.py`; **không sửa** `stage_m1.py`), bộ điều phối gọi lõi ghim, ghi G1 0.5 + che_do_b b-1 (mang nguồn t̂) vào `rca-results/t073-*`.
- `results/T-073/g1-0.3.md` (thay đổi so với G1 bản 0.x, trường nguồn t̂).
- `results/T-073/do-thoi-gian-dev.json` → `khai-truoc-e5.json` (N phút, ca nghiệm thu: ô, mức tải, cách tiêm, tiêu chí; sha256 ghi LOG trước S4).
- `results/T-073/e5/` (sau S4): bản ghi cảnh báo, giờ nhận, dữ liệu lõi thực nhận, kết quả, ảnh/đối chiếu dashboard; giữ kết quả lần đầu kể cả trượt.

## Phạm vi ghi

Ngoài `LOG.md` của task này và dòng T-073 trong `docs/STATE.md`:
- `results/T-073/`; worktree lab như trên (không commit/push khi Minh chưa duyệt).
- exp-obs, ngoài S4: chỉ đọc, và truy vấn nhẹ theo khúc khi **không** ở E2/E4 (I11); thư mục thử `/srv/rca-lab/runs/t073-dev-*` (dev). Chạy thử lõi trên ca cũ đã lưu ra `/srv/rca-lab/m1/t073-dev/`.
- Khung S4: theo `LICH-MAY.md` (exp-app tiêm lỗi qua `inj3.py`, máy tải, exp-obs, Grafana đổi nguồn hiển thị), chỉ khi điều phối mở.

**Không sửa:** lõi M1, cấu hình V082, bản chụp, `stage_m1.py`, `runner4.py`, `sau_v082.py`, chỉ mục `rca-results/t065-l11-001`, dashboard ngoài S4.

## Các bước

1. Đọc code đường chạy hiện có; viết thiết kế ngắn `results/T-073/thiet-ke.md` (luồng, I1, nơi ghi, giới hạn ring capture: đo dung lượng/thời gian quay vòng bằng lệnh chỉ đọc).
2. Thống nhất I1 với `results/T-072/i1-schema.json` (báo khác biệt về điều phối).
3. Cài bộ xuất theo t̂ và bộ điều phối ở worktree; kiểm trên ca cũ: cùng t thì đầu vào lõi trùng gói cũ (so hash từng file trong cửa sổ), cùng đầu ra lõi (`trung_sha`).
4. Đo thời gian trên dev; khai `khai-truoc-e5.json` (ca nghiệm thu chọn trước, không chọn theo kết quả).
5. Trình diff + commit đề xuất qua điều phối (Minh duyệt) trước S4.
6. S4: chạy ca khai trước; ghi đủ ba mốc I1; kiểm dashboard, lưu trữ, phát lại.

## Kiểm đúng đắn

- Không đọc sổ tiêm, đáp án, tên ô ở bất kỳ thành phần nào của dịch vụ (luật cứng 6); kiểm bằng grep đường đọc file và biến môi trường.
- Kiểm dữ liệu thực sự vào lõi (cửa sổ, tín hiệu), không chỉ `t = t̂`.
- Tách lỗi hạ tầng khỏi lỗi phương pháp; giữ kết quả lần đầu.

## Tiêu chí xong

Theo §8.2 W5: tiêm một lỗi, Grafana tự hiện kết quả trong N phút đã khai, trên ca khai trước; ghi riêng thiếu dữ liệu phủ, lỗi xử lý, ca bỏ sót. Dùng V082 cho nghiệm thu **chờ Minh (R1)**; nếu Minh chọn khác, cấu hình lõi đổi theo quyết định, code dịch vụ không đổi.

## Không làm

Sửa lõi; đánh giá độ chính xác; đọc qua API Tempo/Loki (P9b); tiêm ngoài S4.

## Chi phí ước lượng

S4: 1–3 chu kỳ × ~31 phút (đã đo ở T-069) + chuẩn bị; dưới 2 giờ, không thuộc luật 8.

## Rủi ro và điều chưa chắc

- Ring capture của Collector có thể quay vòng trước khi stage nếu chậm [chưa đo].
- Dashboard đọc `rca-results` qua mount chỉ đọc; đổi nguồn ảnh hưởng hiển thị T-065/T-068 — chỉ ở S4, có bước hoàn tác.

## Prompt bàn giao

Ở `LOG.md`, mục cuối mỗi lượt.
