# Đính chính cơ học W4 · T-071 · Phạm vi B2

**1. Chuỗi khởi động lại (restart) trong E2 và E4**  
`results/T-071/khai-truoc-e2.json:223` và `results/T-071/khai-truoc-e4.json:240` có cùng câu gốc.

> Bằng chứng backend độc lập: không container FlashTicket nào trên exp-app restart/OOM trong phút (`container_restarts_total` theo `container_name` không tăng). Thiếu mẫu B2 trong phút → gắn cờ `thieu_b2`, KHÔNG tự loại phút.

→ B2 theo dõi **12 container có chuỗi restart** trong mỗi khoảng E2 và E4. Với một tên đã xuất hiện, phút thiếu mẫu nhận cờ `thieu_b2` và vẫn được xét vào mẫu số. Container vắng suốt khoảng không thể nhận cờ thiếu theo tên.

Bằng chứng. Hai danh sách tại `results/T-071/e2/phan-loai-tom-tat.txt:206–219` và `results/T-071/e4/phan-loai-tom-tat.txt:227–240` có cùng 12 tên. Bộ phân loại lấy tên từ chuỗi đã xuất hiện rồi kiểm mẫu từng phút theo danh sách đó (`results/T-071/phan_loai_phut.py:117–123,201–212`). Ví dụ, `flash-ticket-collector` có trong kiểm kê E0 tại `results/T-071/e0-trang-thai.md:9` và vắng trong cả hai danh sách B2.

**2. Nguồn của trường OOMKilled**  
`results/T-071/khai-truoc-e2.json:245` và `results/T-071/khai-truoc-e4.json:262` có cùng câu gốc.

> state.json: ExitCode, OOMKilled

→ `ExitCode` và `OOMKilled` được đọc từ `state.json` của container tải k6 theo từng lượt. B2 của 12 container trên exp-app chỉ đo khởi động lại.

Bằng chứng. `results/T-071/phan_loai_phut.py:19–20` nêu nguồn OOM của k6. Dòng 57–62 của cùng file mở `state.json` theo lượt và đọc trực tiếp `st['OOMKilled']`.
