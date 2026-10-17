# Bàn giao T-038 — tự rà và chuẩn bị nguồn

Phiên bắt đầu 15/10/2026, tiếp tục qua 16/10 giờ Việt Nam. Codex người làm; Claude phản biện kết quả. Đây là kết quả một phần của bước trước triển khai, chưa hoàn thành hoặc tự nghiệm thu T-038.

Đọc `tu-ra-spec.md`, `de-xuat-nguon-va-tach.md`, `nguon.json`, `kha-thi.json` và `manifest.json`. Lời giao nguyên văn nằm ở LOG Phiên 2. Các kiểm độc lập của người làm được ghi trước khi đọc REVIEW/mốc đóng T-036; sau đối chiếu, chưa thấy phụ thuộc mới phải đổi pin hoặc hợp đồng. Không mở lại T-036.

Pin và nguồn cũ đã khớp; selector hiện hành chỉ lấy graph root T-035, không runs. Toàn bộ graph vẫn thuộc nghĩa vụ về sau. Các lượt runner lỗi được giữ với script và kết quả ở `runs/kiem-dau-vao-001/` và `runs/mien-graph-001/`; lượt sau sửa là tên mới. Lỗi là cách runner diễn giải đường dẫn/prefix, không phải nguồn hay graph lệch hash.

Chưa có nguồn ứng dụng mới được tải. `runs/metadata-de-xuat-001/de-xuat-tai.json` chỉ là danh sách **đề xuất**, không được đưa vào registry build như một payload đã kiểm. Tải v1.0.0 và cách tách A/B chưa được duyệt. Chưa có bản ghi quan hệ, oracle riêng, mapping hoặc graph tĩnh. Không điền kết quả giả để đủ file.

**Dừng phần phụ thuộc nguồn và điều kiện khả thi**, trình Minh quyết gói tải và cách tách trong đề xuất. Không chạy tải từ prompt bàn giao; trước tiên kiểm câu trả lời Minh và phạm vi đã duyệt. Nếu duyệt nguồn: ghim đúng commit/tree/danh sách, viết downloader trong results/T-038/, kiểm byte/blob hash/SHA-256, giữ partial/lỗi và acquisition manifest. Duyệt tải không tự cho sửa SPEC/WHY/DECISIONS hoặc thực hiện phần vượt một phiên. Nếu duyệt sửa phạm vi: chỉ sửa đúng bảng file/nội dung được Minh duyệt; chưa tự tạo task nối tiếp.

P5/RQ3/RQ5 chưa được trả lời bằng kết quả task này. T-040 chờ đủ khảo sát và đối chiếu; P6 chưa nhận quan hệ/tín hiệu TT được chọn; P9 còn cần build/deployment/instrumentation/image lineage, định danh và trường quan sát có nguồn. Thiếu chuỗi revision thì kết quả về sau phải là đối chiếu tham khảo có điều kiện. Không quy mismatch cho telemetry/instrumentation, không gán kiểu cho cạnh unknown.

Bước tiếp chính xác: đọc LOG Phiên 2 và quyết định mới của Minh, kiểm lại các manifest/pin trước dùng; đọc toàn đề xuất và danh sách tải đã pin. Chỉ tạo run mới, không ghi đè các run đã có. Lệnh kiểm nguồn cũ nếu cần do đầu vào mới thay đổi: `py -3 -X utf8 -B results/T-038/preflight.py <ten-run-moi>`. Không lặp kiểm rộng khi đầu vào không đổi.

Prompt trung tính cho Claude ở `prompt-claude.txt` và cuối LOG Phiên 2: nguyên văn Prompt chung + Soát SPEC + G3 hiện hành, chỉ điền metadata. Minh chuyển thủ công hoặc dừng. Claude chỉ đọc/trả lời chat đến khi có quyền ghi bản phản biện cụ thể.

Nội dung nên đưa vào báo cáo chính thức khi có kết quả: nguồn và trạng thái revision của mô hình, coverage nguồn, inventory khác nút quan sát, phép dùng cạnh trong so sánh, kiểu/địa chỉ/mẫu số và các điều kiện chưa phân xử. Không dùng các kiểm đầu vào này làm bằng chứng đầy đủ kiến trúc, nguyên nhân thiếu cạnh hoặc hiệu quả RCA.
