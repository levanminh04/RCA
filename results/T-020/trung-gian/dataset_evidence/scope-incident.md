# Sự cố phạm vi đọc nguồn

FACT: trong bước kiểm schema, luồng đã đọc `results/T-010/runs/schema-samples.json`. Tên file là schema nhưng nội dung trộn header và dòng span đo đã lưu. Hai lượt tạo provenance đọc JSON để dẫn nguồn; một lệnh kiểm cấu trúc in tối đa 900 ký tự của entry đầu, lộ header và phần dòng đo. Các lượt hash của provenance cũng đọc byte. Đây là đọc vượt phạm vi raw đã giao dù không mở `data/`, không chạy phương pháp hay đo ca mới.

File có 483.528 byte theo input-freeze, SHA256 và lệnh liên quan được giữ trong scope-incident.json. Không đọc file thêm để đếm dòng hoặc kiểm hash. Thời điểm UTC chính xác của các lệnh chưa có trong exec output; giới hạn trên khi phát hiện là 2026-10-04T14:44:05.474827Z. Ít nhất ba lần đọc text và hai lần đọc byte đã xảy ra. Số dòng payload được in chưa xác minh; không bịa số.

DeepTraLog đã TX1 trong ledger trước việc này; không mở bộ TX0. Existing TX1 không cấp quyền đọc raw. Không dùng các dòng đo để tính lại số, chọn phương án hoặc chạy method. Nguồn sample đã bỏ khỏi chứng minh schema; thay bằng header/aggregate trong inspect-002/raw-cases.json. Hai helper đọc nguồn chặn exact path trộn payload để không phát lại. Root đã được báo và đã báo Minh. Gói handoff phải giữ sự cố này; không tuyên bố rộng “không thấy raw” cho toàn lượt.
