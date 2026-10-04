# Metadata đã lưu — T-012

Đây là kết quả giai đoạn nguồn/metadata, chưa phải thẻ hoàn chỉnh. Nguồn số: `runs/run-001/record-summary.json`; từng record gốc và hash nằm trong `runs/run-001/source-manifest.json`. Chỉ lấy tài liệu và metadata; chưa tải file dữ liệu liệt kê dưới đây.

| Đầu mối, record cố định | Ngày công bố trong metadata | Giấy phép trong record | File phát hành; byte công bố | Giới hạn của kết quả |
|---|---|---|---|---|
| FSE fault-propagation benchmark, 19513398 | 11/04/2026 | Apache-2.0 | `FSE_26_RCA_dataset_study_reviewer.tar.gz`: 96.090.000 | Mô tả record xác nhận đây là artifact reviewer với benchmark rút gọn. Số ca của bài chưa được đối chiếu với số ca artifact. |
| AnoMod, 18342898 | 13/04/2026 | CC-BY-4.0 | `AnoMod.zip`: 201.917.396 | Mô tả record có hai hệ TrainTicket/SocialNetwork và nhiều nguồn tín hiệu. Chưa kiểm file thật hoặc nhãn từng trace/root/time. |
| TrainTicketTrace, 17811972 | 04/12/2025 | CC-BY-4.0 | 11 file `.tar`: tổng 26.920.437.760; từng file ở summary | Tên archive F1/F2/... chưa chứng minh nhãn ca hoặc trace. Record không có mô tả chi tiết hoặc liên kết bài trong trường đã lưu. |
| Check Your Trace First, 19335897 | 26/02/2026 | CC-BY-4.0 | `TRCA.zip`: 335.076.044 | Record mô tả code và dữ liệu TT/OB. Chưa xác định provenance hoặc quan hệ dùng lại dữ liệu. |
| LO2, 14938118 | 28/02/2025 | CC-BY-4.0 | `lo2-data.zip`: 46.483.584.345; `lo2-sample.zip`: 1.070.011.492; tổng mọi file 47.555.233.881 | Mô tả record nói đã có LO2v2 thay thế. Dung lượng giải nén khoảng 540 GB là lời công bố của record, chưa đo. Sample chỉ chứa log và metric được chọn của 100 lượt đầu, không thay toàn kho. |

Các con số trên là **FACT về metadata của đúng record**, chưa phải kiểm tải archive hoặc census nhãn. `metadata.version` trong các API này là null; không tự biến null thành tên phiên bản. DOI/record cố định đã lưu, danh sách phiên bản mới hơn còn phải đối chiếu.

Từng snapshot HTML của bốn bài FSE/AnoMod/OpenRCA2/LO2 đã kiểm có tiêu đề khớp đầu mối và cấu trúc bài arXiv. Snapshot API OpenRCA chỉ khóa danh tính repo; chưa khóa commit của README. Đây là kiểm nguồn, không kiểm telemetry.

## Phần còn thiếu và người tiếp nhận

- **Người làm Codex:** hoàn tất đối chiếu bài, README, repo, bản phát hành hiện hành, giấy phép và provenance; đặc biệt không coi OpenRCA2 là độc lập với dữ liệu gốc khi chưa lần theo quan hệ dùng lại.
- **Người làm Codex:** thử inventory archive qua metadata khi nguồn hỗ trợ; chỉ lấy file nhãn/schema riêng nếu xác định rõ đó không chứa số đo. Cần census root × fault × lần lặp và phạm vi bình thường; file không có nhãn thì báo đúng loại task có thể chấm.
- **Minh:** xác định quyền đọc số đo và ứng viên cần bảo toàn trước G3. Không tải archive mẫu trong checkpoint này.
- **Người làm Codex:** lập danh sách file mẫu, độ phủ và ngân sách sau metadata. Không chọn duy nhất archive nhỏ nhất vì thuận tiện. Với tar lớn, dung lượng một file không tự chứng minh có thể đọc một mẫu ít byte; cần kiểm khả năng truy cập thành viên hoặc trình tải cả file.
- **Người làm Codex:** hoàn thành thẻ theo đủ 10 mục mẫu T-002, rồi ghép bảng tiêu chí/task chung. Chưa có kết luận tiêu chí 7, vị trí root trong đồ thị thực hoặc tính đủ của normal.

Không phải “không thể kiểm”: các phần trên chưa làm xong trong phiên và/hoặc đang chờ quyền đọc cụ thể. Lượt tìm vẫn còn hai truy vấn trong giới hạn SPEC; các lead chưa đọc được giữ trong sổ tìm.

## Tự kiểm và cách chạy lại

`py -3 -B results/T-012/scripts/capture_sources.py --run run-001 --verify`

Kết quả: cả 10 snapshot khớp byte/hash đã lưu; summary được tính lại từ năm record gốc và khớp bản đã lưu. Lượt lưu nguồn tải 1.278.428 byte tài liệu/metadata, mất 1,960 giây; đây là thời gian bước lưu nguồn, không phải thời gian toàn lượt tìm. Tải telemetry: 0 byte. Lệnh online dùng run-id mới để không ghi đè lượt cũ.

