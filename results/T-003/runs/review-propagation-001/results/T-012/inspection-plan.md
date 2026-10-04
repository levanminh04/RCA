# Phạm vi kiểm T-012 sau Q-47

Lượt này hoàn tất khảo sát **nguồn/metadata** giới hạn, thẻ và lineage. Không tải archive telemetry, không mở hàng Bank, không chạy RCA. Không gọi việc đó là đã kiểm chất lượng dataset. Các bộ trong T-008–T-011 có kế hoạch kiểm riêng; không tự kéo archive mới T-012 vào gói đó.

| Họ/record | File/byte theo metadata | Điều xác minh được không mở số đo | Phần còn OPEN và lý do |
|---|---|---|---|
| FSE latest 19522409 | `FSE_26_RCA_dataset_study_reviewer.tar.gz`, 91.418.171 byte | Latest, checksum, license, mô tả artifact reduced | Nhãn/schema/accepted paper trong tar.gz chưa được mở; không thay số toàn bài vào reduced artifact. |
| AnoMod 18342898 | `AnoMod.zip`, 201.917.396 byte | Official collector README theo hệ, commit, license code/data | Không có label riêng trong record, chỉ archive; census release và clock/parent cần mở file khi được giao. |
| TrainTicketTrace 17811972 | 11 tar, 26.920.437.760 byte tổng | Inventory/checksum/clean/fault naming, abstract tác giả | Không tải tar mới >5GB tổng; giữ chênh 9 faulty versions/10 tên tar lỗi. Exact root/time chưa có. |
| TRCA 19335897 | `TRCA.zip`, 335.076.044 byte | Record/license/tên hai hệ | Anonymous/provenance và labels nằm trong gói chưa mở. Không nói đây là thu thập mới. |
| OpenRCA Bank | Paper công bố 26,4 GB telemetry, chưa inventory byte file | Bài/README/schema nhãn/repo commit/license | Bảo toàn cả họ Bank/AIOps Bank đến G3 theo quyết định gói. Không lấy mẫu, không xem quality. |
| OpenRCA Telecom/Market | Paper 17,6/24,5 GB telemetry, chưa archive inventory | Paper phân biệt modality/entity và code | Không tự suy quyền tải corpus mới; không suy độc lập với Bank. |
| OpenRCA2 | Chưa có public archive ghim | Paper/protocol/license công bố, quan hệ FSE | A.6 nói public sau acceptance; chưa có nguồn release đủ để census. Không kết luận không tồn tại trên toàn Internet. |
| LO2 v1/v2 | Danh sách byte ở `runs/run-002/record-summary.json` | Version successor, taxonomy correct/error, hạn chế trace v1 | Raw vượt gói; index v2 riêng 31.028.530 byte vượt dự kiến metadata 25MB. Không tải thêm để phục vụ một bộ không có root incident xác minh. |

Không có mẫu telemetry được chọn trong T-012. Nếu G1 cần kiểm tiếp một ứng viên ngoài nhóm bảo toàn, file/mẫu phải được chọn theo metadata trước số đo và có phạm vi/byte được giao rõ. Không chọn archive nhỏ nhất làm đại diện. Phải census root×fault×lặp nếu nhãn riêng lấy được, rồi kiểm coverage/schema theo hệ/revision, unique-parent theo (trace_id,span_id), normal/clock/entity mapping và tiêu chí7 theo mẫu T-002.

Việc tra latest/source tài liệu tổng tải ở run-002 là 1.318.656 byte, 10,468 giây cho bước tải; không phải toàn thời gian nghiên cứu. Script dùng tối đa bốn luồng HTTP, không phải subagent. Giữ run-001 và run-002. Nguồn số là manifest; mọi archive trong bảng chưa tải.

OPEN owner: Codex kiểm nguồn/nhãn khi được giao; chủ nguồn làm rõ mâu thuẫn/thiếu license/schema; Minh/G1 quyết corpus; Bank chỉ mở sau G3. Đây là giới hạn bằng chứng được chấp nhận, không bảo đảm dataset đủ chất lượng.

Đã kết thúc nguồn với run-003: hai bài K3 dùng lại OpenRCA, FAMOS TT record 2024 ngoài cửa sổ năm. [Bảng đầu mối](final-leads.md) ghi đúng nguồn và byte; không thêm archive tải. Có 14 thẻ scoped đủ 10 mục và 34 snapshot hash/byte hợp lệ qua kiểm offline độc lập ở `runs/final-check-001/verification.json`. Census archive/quality vẫn OPEN, không thay bằng PASS toàn vẹn file.
