# Bàn giao T-038 — phần trong quyền đã hoàn tất

Đã xử lý hết phần đang có quyền: rà 27 mục nguồn cũ, đọc source đóng 9 cờ OPEN sai, truy thêm metadata lineage và chuẩn bị gói sửa SMTP cụ thể. **Chưa đủ nghiệm thu toàn T-038 vì T038 chưa tiếp nhận SMTP và gói đổi comparator/common pin chưa được duyệt/áp dụng.** Xem `hoan-tat-trong-quyen.md/json` để phân biệt tiêu chí đạt, phần chờ quyền và giới hạn kết luận.

Điểm vào hiện hành: `bao-phu-nguon.md/json`, `ban-ghi.json`, `nguon.json`, `inventory-index.json`, `mapping.json`, `do-thi/`, `doi-chieu/index.json`, `phan-tich-chenh-lech.md/json`, `kiem-dung-dan.md`, `kha-thi.json`, `hoan-tat-trong-quyen.md/json`, `goi-sua-SMTP.md`, `manifest.json`. Model005 và 1.069 kết quả ở doi-chieu-dev-002 giữ nguyên; bổ sung mới ở runs/hoan-tat-trong-quyen-001. Giữ mọi bản trước; không chạy lại output hợp lệ khi input không đổi.

| Bên nhận | Đầu vào và điều kiện |
|---|---|
| T-040 | Nguồn/inventory/operations và relation có provenance, toàn graph/cửa sổ và từng tập/members/exclusions. Source comparison conditional; 9 initializer flag là overapproximation của extractor đã kiểm, không phải mất telemetry. Không cộng các cờ chồng lấn thành tỷ lệ nguyên nhân. |
| P6/RQ3/RQ5 | Địa chỉ hai mức, source relation và signal declarations, nguồn thêm ngoài trace. Graph mới dùng tính khóa/chiếu/tập; chưa có điểm RCA, bằng chứng lợi ích hoặc thiết kế P6 đã chọn. |
| P9 FlashTicket | Owner/component ID, endpoint method/route/client callsite, kind/protocol; DB logical/physical riêng; broker namespace/exchange/routing/queue; log trace/span correlation và metric resource/scrape target. SMTP cần tách configured/observed TLS, attempt và outcome của chặng gửi; không nhận accepted là recipient delivery. Đây là yêu cầu quan sát, không chứng minh collector sửa lịch sử chưa ghi. |
| Chủ dữ liệu qua Minh | App commit/image build digest, actual agent/config, deployment/namespace/env/time và workload/capture schema nếu muốn phân xử runtime. Metadata primary đã kiểm không cung cấp nối chuỗi này; không dùng graph giống nhau để chọn version. |

Coverage hiện là 2.783 read, 43 excluded, 1 PDF body open. PDF là manual converter offline ngoài current declared build, nên không chặn module inventory. Không tuyên bố đọc body hoặc semantic/runtime đầy đủ. Archive đã rõ source/entrypoints; actual activation vẫn cần manifest/dependencies/image. Các giới hạn giữ đúng phạm vi kết luận, không thay cho việc làm còn có thể thực hiện.

SMTP: `goi-sua-SMTP.md` dẫn patch, code copy, oracle, 29 checks V2, filelist, ảnh hưởng và chi phí. Chưa sửa src/shared, T-036 hay SPEC khác, chưa chuyển pin. Minh duyệt gói thì mới áp dụng, kiểm chung và tiếp nhận pin ba nhánh. Dự toán 37 phút máy/600 MB output là CANDIDATE, không là số đã đo. Không nghiệm thu T-037/T-039 qua kiểm tiếp nhận.

Sự cố telemetry mẫu lịch sử đã được báo và giữ trong incident/LOG; index lỗi cách ly, không dùng cho facts/model/mapping/kết luận. Không mở raw RE2/test/heldout/data khóa. Kiểm cuối chỉ hash nhóm đó. Không thể hoàn tác việc đã đọc trong lượt cũ.

Bước tiếp: Minh xem gói SMTP để duyệt chính xác phạm vi chung. Prompt soát kết quả ở prompt-claude.txt và LOG; prompt gói SMTP ở prompt-claude-smtp.txt, đều theo nguyên mẫu để Minh chuyển thủ công. Chưa có quyền ghi REVIEW thì Claude chỉ đọc/trả lời chat. Không tự gửi chat, nghiệm thu, đóng G3, commit/push. Commit đề nghị sau Minh duyệt: `T-038: hoàn tất khảo sát trong quyền và trình gói SMTP chung`.


Cập nhật16/10/2026: T037 đã hỗ trợ SMTP/full model; T039 đã so132graph dùng snapshot gốc. GóiV2 tại runs/cap-nhat-goi-smtp-001/package/plan.md xin đổi semantics comparator và phiên bản chung; dùng nguyên builder T037. Preview29 đạt, chưa replay1069TT/132OB bằng comparator mới. Kế hoạch hồi quy đầy đủ cả ba nhánh và dự trù37phút/600MB thay góiV1; không đổi model/so/pin hiện hành hoặc nghiệm thu.
