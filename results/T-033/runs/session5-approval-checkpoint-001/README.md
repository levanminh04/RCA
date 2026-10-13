# T-033 — checkpoint bổ sung lời duyệt Q-132

Ghi 2026-10-11T08:51:11.022139+07:00, Codex là người làm, Claude là người phản biện. Phiên dừng vì ngữ cảnh nén (AGENTS §5a.2); không có nghiên cứu mới.

Minh đã duyệt hạch toán chặng cũ 8 giờ và tối đa 4 giờ xử lý mới, cho lưu DECISIONS. 8 giờ là mức quản lý dự phòng, chưa kiểm; không phải số đo. Thời gian thực tế cũ vẫn OPEN. Không còn chờ duyệt hạch toán trong phạm vi này.

`approval.json` giữ lời duyệt và đề xuất được duyệt. `approved-accounting.json` giữ baseline quản lý, nguồn ledger lịch sử và yêu cầu cộng mọi lượt mới kể cả hỏng/kiểm. Ledger lịch sử không đổi. Đây chưa là ledger staged được guard pin: phải tạo snapshot theo thời gian đã cộng và cập nhật đúng guard/hash trước launch.

`checkpoint.json` chứa trạng thái/việc còn lại. `scope-verification.json` kiểm phạm vi/prefix/hash. `manifest.json` kiểm byte/hash file checkpoint. `prompt-next-session.md` là prompt nối chặng tính cho phiên Codex mới; chưa là prompt tổng hợp hay phản biện chính thức.

Không có SSH mới trong bổ sung này. Bằng chứng EC2 cuối trong session5-checkpoint-001/remote-status.json, ở 2026-10-11T00:32:01.999369+00:00: không T-033 worker/tmux. Kiểm mới trước launch. Archive đã xóa đúng một file trong phiên 5, không xóa lại. Chưa pilot/fixture/rest/khóa nhóm.

Lệnh cuối: `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -X utf8 results/T-033/scripts/checkpoint_session5_approval.py`. Bước tiếp: mở phiên mới với prompt, đọc nguồn/LOG/checkpoint, ghi mở phiên, kiểm hash rồi hoàn thiện ledger/guard/điều phối và ca đầu theo SPEC. Không cần xin lại duyệt cho việc trong SPEC đã duyệt.
