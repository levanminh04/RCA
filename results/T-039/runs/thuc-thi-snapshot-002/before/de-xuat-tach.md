# Phạm vi cần Minh quyết — chưa sửa SPEC hoặc tự chia task

Tự rà chưa đủ căn cứ cam kết toàn SPEC một phiên: 215 blob ứng dụng chưa đọc, lineage/deployment/nguồn phụ chưa nối, bản ghi/mapping và phân tích toàn 132 graph còn phía sau. Dự toán CANDIDATE 7,5–12 giờ công không gồm phản biện/chờ nguồn; không được dùng dự toán cũ 3–5 giờ để giảm độ sâu.

## Phương án đề nghị

**Phần A — truy nguồn, coverage và lineage:** hoàn tất toàn cây đã định danh, phân hoạch đọc/loại trừ/chưa lấy/chưa rõ; truy config/build/template/generated/binary/nguồn ngoài; lập registry theo đúng loại object; phân xử được tới đâu về ứng dụng/dataset/image/deployment/nguồn phụ/Node. Đầu ra là registry, bảng coverage, chuỗi bằng chứng và danh sách nguồn bổ sung/owner/điều kiện. Dự toán chưa đo 3–5 giờ công; không kết luận dataset deployment hoặc độc lập khi thiếu mã sinh.

**Phần B — bản ghi, mapping, graph và phân tích:** nhận nguồn Phần A đã kiểm, viết oracle literal trước biến đổi riêng; lập bản ghi và mapping có owner/scope/provenance, dùng nguyên pin T-036; dựng, chiếu và đối chiếu toàn 132 graph hiện hành ở hai mức/endpoints/typed, giữ interval/dev-adapter/members/exclusions/N/A. Lần theo nhóm chênh lệch quan trọng và match tương ứng; kiểm và bàn giao T-040/P6/P9. Dự toán chưa đo 4,5–7 giờ công. Không biến tên operation hoặc alias chưa xác minh thành mapping đã quyết.

Phân chia này giữ toàn nghĩa vụ SPEC hiện hành, chỉ đổi đơn vị thực hiện. Nếu Phần A thiếu bằng chứng có thể xin được thì phải trình nguồn/phép thu/chi phí; không tự loại nhóm quan trọng khỏi Phần B. Nếu không thể phân xử bằng dữ liệu hiện có, ghi chính xác giới hạn và quyết định phụ thuộc. Không giảm nhiệm vụ phân tích thành đếm cạnh.

## Impact map đề nghị, CHƯA ĐƯỢC DUYỆT

| File/phạm vi | Cũ → đề nghị | Vì sao/ảnh hưởng |
|---|---|---|
| `tasks/T-039-p5b-online-boutique/SPEC.md` | Toàn khảo sát+dựng+phân tích trong một phiên → Phần A nếu Minh chọn T-039 làm task nguồn | Khóa tiêu chí và phạm vi A; ghi rõ toàn nghĩa vụ B được chuyển, chưa nghiệm thu mục tiêu gốc |
| SPEC/LOG task Phần B, mã và tên do Minh quyết | Chưa tồn tại → tạo sau khi Minh duyệt đề xuất SPEC cụ thể | Không dùng T-040 vì đã dành cho tổng hợp; không tự cấp mã hoặc ghi file task mới trong lượt này |
| `docs/STATE.md` | Dòng T-039 triển khai có điều kiện → dòng phản ánh phân chia được duyệt | Chỉ cập nhật sau nguồn quyết định; phần bổ sung task mới/phần văn bản chung cần quyền riêng |
| `docs/DECISIONS.md`, `docs/WHY.md` | Chưa có quyết định tách này → ghi nguyên ý Minh và lý do sau duyệt | Quyết định bền vững; không được suy đồng ý tải thành đồng ý sửa SPEC/tách |
| `results/T-039/`, LOG T-039 | Tiền kiểm này → đầu ra A trong SPEC đã sửa | Giữ mọi lịch sử; không tự chuyển phạm vi B khỏi trách nhiệm nghiên cứu |

Đây là impact map để Minh chọn cách tổ chức, chưa là quyền ghi các file ngoài phạm vi lời giao. Nếu Minh muốn giữ toàn T-039, cần quyết rõ cách xử lý quy tắc một phiên sau khi có nguồn/pilot; không tự coi duyệt triển khai có điều kiện là ngoại lệ một phiên.

## Mâu thuẫn loại object ở registry chung

Không có mismatch nội dung hoặc đề nghị sửa code/hợp đồng tính toán. Registry T-036 gọi revision Nezha là tree object, trong khi API Git commits trả commit và tree canonical có cùng toàn thành viên snapshot. Cần dừng suy luận dùng mô tả cũ. Bằng chứng ở `runs/tien-kiem-001/kiem-loai-object.json`.

**Sửa tối thiểu được trình, chưa thực hiện:** trong `results/T-036/nguon.json`, hai source ID Nezha-README/Nezha-tree: thay `revision_kind` bằng mô tả commit analysis Nezha; ghi commit→tree canonical và bằng chứng metadata; giữ nguyên revision nội dung/README blob và `dataset_link=OPEN`. Sau đó cần cập nhật `results/T-036/manifest.json` cùng LOG/dòng STATE T-036 theo quyền riêng, giữ bản manifest cũ. Vì cả ba nhánh ghim manifest nghiệm thu, thay registry sẽ đòi Minh duyệt cách chuyển pin thống nhất T-037/T-038/T-039; không tự cập nhật SPEC/pin của chúng.

**Phương án ít lan truyền hơn để Minh quyết:** giữ nguyên pin byte của T-036, cho T-039 ghi một mục nguồn task phân biệt phát biểu lịch sử sai loại object với metadata commit→tree mới xác minh; không dùng phát biểu lịch sử làm bằng chứng, không đổi nghĩa API. Cách này chỉ sửa tri thức của registry riêng T-039; mâu thuẫn trong registry chung vẫn phải được công bố/bàn giao cho hai nhánh và xử lý bằng quyền riêng. Chưa tự chọn phương án hoặc gửi thông tin sang chat khác.

Đề xuất quyết định để lưu chính thức sau khi Minh trả lời: nguyên ý lựa chọn tách hoặc giữ task, nguồn/file/đường dẫn được phép tải, và lựa chọn xử lý metadata loại object. Chưa ghi DECISIONS/WHY hoặc nhận là DECIDED.
