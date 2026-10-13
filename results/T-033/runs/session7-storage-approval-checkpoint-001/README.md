# T-033 — Lời duyệt và checkpoint do ngữ cảnh nén

Minh trả lời nguyên văn **“duyệt”** cho đề xuất tại `../session7-storage-checkpoint-001/README.md`: nâng riêng trần đầu ra EC2 T-033 lên **5 GiB**, dùng bản sửa trích v2, một ca pilot có kiểm trước phần còn lại và tiếp nguyên SPEC. Giữ mọi file cũ/lỗi; không chạy lại detector PASS. Không đổi ngân sách thời gian, SPEC, DECISIONS, WHY hoặc nguồn cũ. Lời duyệt này không cần xin lại ở phiên tiếp.

Ngữ cảnh đã nén. Đã checkpoint theo AGENTS §5a.2; chưa SSH hoặc chạy bản sửa sau lời duyệt. Task và phần đọc tay/tổng hợp vẫn chưa hoàn tất. Codex người làm; Claude phản biện chính thức. Chưa soạn prompt phản biện vì task chưa xong.

Hash checkpoint trước đạt 64/64 trước ghi. `ledger.json` là bản sao nguyên byte của ledger cuối phiên 7: charged mới 350.9056568979851 giây, còn 14049.094343102015 giây. Không có timer/charge EC2 mới. Hạch toán cũ 8 giờ là dự phòng chưa kiểm, actual cũ OPEN. Trạng thái không worker là quan sát lịch sử, cần kiểm mới có đo trước dùng EC2.

Bước tiếp chính xác: đọc AGENTS, STATE, toàn SPEC T-033 và LOG cuối; checkpoint này cùng README/checkpoint/ledger/scope/manifest của session7-storage-checkpoint-001; session7-open-001/points-lock.json, coverage-matching.json, lock-receive-verification.json; scripts/session7_control.py, session7_extract.py, session7_extract_v2.py và draft-static-check-final.json. Kiểm hash trước dùng. Dựng/pin snapshot ledger nối từ ledger cuối và mọi timer sau đó, kiểm process/source/hash mới có đo. Tự soát wrapper/input quyền 5GiB, explicit ca pilot, post_indices/time/cột/shape/scalar/NaN/flags và exact byte guard. Pilot đạt rồi rest loại pilot. CLI launch chưa hoàn thiện; không dùng lệnh suy đoán. Mã bản sửa chưa có PASS EC2.

Trước diễn giải phải đọc trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, toàn LESSONS, WHY-41 và các nguồn/checkpoint đã yêu cầu trong LOG. Dùng kết quả PASS theo hash; giữ 64 nhóm và 210 đường ca/khóa điểm. Lần theo đầu vào → xử lý → thống kê/phân phối → cờ/CP → chấm với điểm/ca đối chứng và giải thích cạnh tranh. Thiếu bằng chứng thì OPEN cùng phép kiểm, chi phí, quyết định phụ thuộc. Không tự đổi SPEC/tham số/tiêu chí hoặc chạy vượt quyền.

Minh cần mở phiên mới và dán: “Đọc AGENTS.md, tiếp T-033 trong STATE. Đọc checkpoint session7-storage-approval-checkpoint-001 và checkpoint phiên 7 theo LOG, kiểm hash trước dùng. Đề xuất trần EC2 5GiB và sửa trích tại README phiên 7 đã được tôi duyệt; không xin lại. Codex làm, Claude phản biện. Tiếp pilot/kiểm/rest rồi đọc tay và tổng hợp nguyên SPEC; mọi xử lý EC2 mới phải có ledger/timer, không chạy lại detector PASS, không xóa thêm. Ngữ cảnh nén thì checkpoint ngay.”

Lệnh cuối laptop: Python pin `-B -X utf8 results/T-033/runs/session7-storage-approval-checkpoint-001/checkpoint-writer.py`. Chỉ tài liệu/hash/diff. Lệnh EC2 cuối vẫn là receive-locks lịch sử ghi trong checkpoint trước.
