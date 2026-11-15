# Prompt cho phiên Claude điều phối T-062

Dán nguyên văn khối dưới vào một phiên Claude Code mới trong `D:\RCA-flashticket` (hoặc lịch `t062-tiep-nhan` tự mở).

```text
Bạn là phiên điều phối của T-062 trong repo D:\RCA-flashticket. Minh (chủ đồ án) đang ngủ và treo máy 24 giờ; Minh đã duyệt chạy liên tục và giao bạn điều phối toàn bộ. Làm mọi việc có thể cho tới khi gặp việc buộc phải chờ Minh duyệt; khi đó ghi rõ vào bàn giao rồi làm tiếp phần khác.

ĐỌC TRƯỚC (bắt buộc, theo thứ tự):
1. AGENTS.md (luật repo; Luật 0 ở đây được thay bằng phạm vi duyệt trong SPEC T-062).
2. tasks/T-062-dem-chang-1-4/BOI-CANH.md — bối cảnh cuộc trao đổi 11–12/11 (bắt buộc đọc).
2. tasks/T-062-dem-chang-1-4/SPEC.md — phạm vi, luật cứng của lượt, máy, runbook A1…H1, phân công.
3. tasks/T-062-dem-chang-1-4/CHECKPOINT.md và LOG.md — đang tới đâu. Nếu NHIP_TIM_UTC trong CHECKPOINT mới hơn 40 phút và DIEU_PHOI là một phiên khác đang chạy, thì THOÁT ngay (tránh hai bộ điều phối).
4. docs/STATE.md, docs/techstack/KE-HOACH-GIAI-DOAN-2.md §3–§7, results/T-059/danh-muc-loi.md (7 ô phát triển), results/T-059/yeu-cau-code-nhom.md, results/T-061/dinh-dang-ket-qua-rca.md, results/T-061/exp-obs/README.md, results/T-058/dem-2026-11-10/ (runner M1, stager, auth.py, remote.ps1, m1-p7-config.json), D:/Project/flash-ticket-platform/deploy/rca-test/README.md.

NGAY KHI NHẬN VIỆC: ghi DIEU_PHOI = id phiên này và NHIP_TIM_UTC vào CHECKPOINT.md; cập nhật nhịp tim ít nhất 30 phút một lần.

MONG MUỐN CỦA MINH (nguyên ý):
- Sáng dậy có kết quả và một giao diện truy cập được để thử RCA: đầy đủ, trực quan, dễ dùng; chọn sự cố, xem đồ thị, hạng, bằng chứng, liên kết sang trace/log/metric. Coi lượt này như chạy chính thức dù vẫn là exp-*.
- Kịch bản tải, các ca và kết quả lưu khoa học, dễ chọn và thử lại. Tự quyết cách tổ chức; ưu tiên trải nghiệm của Minh.
- Codex (gpt-6.1-sol high, yếu hơn Claude) làm việc vừa sức theo kịch bản rõ; việc khó (review code, bộ tiêm, M1, phân tích, giao diện) Claude làm.
- Review diff FlashTicket (hơn 100 file; trước đó Codex từng xóa import làm lỗi), theo dõi GitHub Actions CI trên PR, sửa code tới khi xanh. Tài khoản GitHub của Minh có quyền bypass nhưng TUYỆT ĐỐI không push main / không merge (push main = cd.yml triển khai lên production máy 84).
- Máy tải là máy AWS exp-app cũ 3.24.8.49 (ghi trong SPEC).
- Không ảnh hưởng kết quả RCA cũ và hệ thống FlashTicket production. Có phương án dự phòng cho trường hợp xấu nhất.
- Nhập/đọc mật khẩu: Minh duyệt cho cả Claude và Codex. Theo chính sách của Claude, Claude không tự nhập mật khẩu đăng nhập vào hệ thống ngoài máy cục bộ; bước đăng nhập (token Keycloak cho k6, v.v.) giao Codex. Không in giá trị bí mật vào file nào.
- Giới hạn thật: chặng 4 không xong trong một đêm; đích là lượt phát triển đầu với M1 BẢN KHÓA (không chỉnh, không chọn) + bản đề xuất SPEC chặng 4 có tiêu chí để Minh duyệt.

CÁCH ĐIỀU PHỐI:
- Phiên này giữ exp-app (A2, D1, D2, E1, E2) và A1.
- Mở một phiên Claude riêng cho giao diện G1 (mcp__ccd_session__start_session, initiation "user_asked", context "fresh", use_worktree false) với brief từ SPEC bước G1; phiên đó chỉ được đụng Grafana exp-obs (pinned/provisioning/dashboards, rca-ket-qua) và results/T-062/giao-dien/.
- Giao Codex việc C1 (máy tải) và việc trông bộ chạy E1 bằng lệnh nền, ví dụ (PowerShell, run_in_background):
  codex exec -C D:\RCA-flashticket --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -m gpt-6.1-sol -c model_reasoning_effort=high -o results\T-062\codex\<viec>-ketqua.md "<brief đầy đủ: mục tiêu, máy, khóa, luật cứng SPEC §Luật cứng, file được ghi, cách báo xong>" > results\T-062\codex\<viec>.log 2>&1
  Brief cho Codex phải tự đủ, nhắc luật cứng 1–10 của SPEC, chỉ cho ghi đúng thư mục của nó. Kiểm đầu ra của Codex trước khi dùng.
- Codex hết lượt (hồi ~4 giờ): làm tiếp phần đó hoặc chờ, ghi checkpoint; khi hồi thì resume hoặc giao lại.
- Bạn hết lượt (hồi ~1,5 giờ): trước đó ghi checkpoint đủ để lịch t062-tiep-nhan mở phiên mới tiếp quản.
- Không chạy hai việc ghi trên cùng một máy cùng lúc.
- Gọi Codex: ghi brief ra file rồi truyền qua stdin (Get-Content brief.md -Raw | codex exec ... -). Truyền chuỗi trực tiếp trong PowerShell bị tách tham số.

KẾT THÚC (khi xong hoặc khi mọi việc còn lại đều chờ Minh):
- results/T-062/bao-cao-sang.md: đã làm gì; kết quả từng ô (M1 xếp root ở hạng mấy, vai trò, ảnh giao diện); cách mở giao diện (đường hầm SSH, URL, dashboard); dữ liệu nằm đâu; phần chưa làm/không xác nhận được và vì sao; danh sách việc chờ Minh duyệt (commit, merge PR, SPEC chặng 4, …); lệnh kiểm `git diff` để Minh thấy mọi thay đổi.
- results/T-062/spec-chang-4-de-xuat.md; results/T-062/manifest.json.
- Cập nhật dòng T-062 trong docs/STATE.md, nối LOG.md đủ mục 7 AGENTS, đặt CHECKPOINT trạng thái XONG, rồi tắt lịch t062-tiep-nhan (mcp__scheduled-tasks__update_scheduled_task enabled=false).
- Không commit repo RCA; FlashTicket chỉ commit/push lên nhánh rca/quan-sat-log.
```
