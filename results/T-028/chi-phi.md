# Chi phí T-028

## Phiên 1 — bước 1–2, dừng chờ codebook/WHY

- Mở phiên: 2026-10-07T23:07:34+07:00; chốt bản codebook trình duyệt: 2026-10-07T23:24:42+07:00. Thời gian lịch tới chốt 1028.526 s; đây gồm đọc/soạn/tự kiểm và trao đổi, không là thời gian CPU hoặc token. Nguồn: `runs/chot-codebook-001/manifest.json`.
- Bước 1: `2026-10-07T23:14:32.986+07:00` → `2026-10-07T23:14:34.131+07:00`, thời gian chương trình 1.145980 s. Nguồn: `runs/danh-sach-001/manifest.json`; từng pha ở `runs/danh-sach-001/progress.jsonl`. Một lượt đạt, không có lượt hỏng; chỉ số đã lưu/bản ghi nguồn, không raw.
- Bước 2: từ sau trích số tới chốt, thời gian lịch 608.395 s (không tách được CPU soạn thảo); nguồn: `runs/chot-codebook-001/manifest.json`. Có hai trợ lý hỗ trợ độc lập script/đối chiếu và tiêu chí native; Codex chịu trách nhiệm bản chốt. Không deep research hoặc tải dữ liệu.
- Đầu ra trước manifest chốt và file chi phí này: 4356106 byte trên 8 file; danh sách/hash/byte từng file ở `runs/chot-codebook-001/manifest.json`. Không có payload Nezha dẫn xuất. Đây là snapshot trước phần bàn giao, không gọi số trên là dung lượng toàn task.
- RAM đỉnh/CPU/token không đo; ghi chưa kiểm, không suy từ ước lượng SPEC. Không thay môi trường, không EC2, không phí cloud hoặc tải thêm.

## Phần còn lại

Bước 3–6 chưa chạy. Ước lượng SPEC cho toàn task vẫn **chưa kiểm**: công agent 3–5 giờ, máy 10–45 phút, RAM 0,5–2 GB, đĩa 0,1–0,3 GB; nguồn: `tasks/T-028-p4-han-che-xep-hang/SPEC.md`, mục Chi phí ước lượng. Chưa thể xác nhận từ lượt trích số rất ngắn. Phiên mới chỉ bắt đầu bằng chứng khi codebook và văn bản/phạm vi WHY-38 đã duyệt, WHY-38 đã ghi. Lượt nào dự kiến hơn một giờ phải trình Minh trước; hiện không có lượt đó được mở.

## Phiên 2 — bước 3–6 (08/10/2026)

Phần “Bước 3–6 chưa chạy” phía trên là ghi nhận lịch sử ở phiên 1. Minh đã đồng ý thời lượng trước triển khai trong LOG; các bước đã được thực hiện trong phiên này. Không chạy lại phương pháp hoặc bước trích danh sách.

Mở đọc lúc `2026-10-08T08:57:30+07:00`, snapshot chi phí `2026-10-08T10:01:10.439356+07:00`; thời gian lịch tới snapshot 3820.439 s. Nguồn: `results/T-028/runs/buoc3-005/cost-observed.json`. Thời gian này gồm trao đổi/ngắt lượt, không là CPU, token hoặc thời gian công agent thuần.

| Pha | Thời gian chương trình / s | Trạng thái và nguồn |
| --- | --- | --- |
| Tiếp nhận/kiểm nguồn | 428.000000 | wall_clock_including_reading_and_exchange; `results/T-028/runs/tiep-nhan-001/manifest.json` |
| buoc3-001 | 48.000354 | interrupted_for_implementation_correction; `results/T-028/runs/buoc3-001/manifest.json` |
| buoc3-002 | 844.393707 | failed; `results/T-028/runs/buoc3-002/manifest.json` |
| buoc3-003 | 300.902128 | failed; `results/T-028/runs/buoc3-003/manifest.json` |
| buoc3-004 | 1.533462 | failed; `results/T-028/runs/buoc3-004/manifest.json` |
| buoc3-005 | 3.258963 | analysis_computed_pending_independent_and_manual; `results/T-028/runs/buoc3-005/manifest.json` |
| independent-ranking.json | 1.138650 | passed; `results/T-028/runs/buoc3-005/independent-ranking.json` |
| independent-statistics.json | 160.559235 | passed; `results/T-028/runs/buoc3-005/independent-statistics.json` |
| aggregation-review.json | 2.898064 | passed; `results/T-028/runs/buoc3-005/aggregation-review.json` |
| report-review.json | 0.792496 | passed; `results/T-028/runs/buoc3-005/report-review.json` |
| Đọc cửa sổ Nezha cho đọc tay | 113.441642 | guard RAM reread only; excludes human reading/writing; `results/T-028/runs/buoc3-005/manual-nezha.json` |
| Bước5 đọc tay RE2 | N/A — không đo tách | completion checkpoint; independent human-reading duration not measured; `results/T-028/runs/buoc3-005/manual-re2.json` |
| Bước6 viết/hợp nhất báo cáo | N/A — không đo tách | checkpoints only; exact independent drafting start/duration not recorded; `results/T-028/runs/buoc3-005/report-attempt001/manifest.json; manual-reading.json; handoff-progress.jsonl` |

Bước3: thống kê mọi service/kênh được ghi trước nhãn trong progress002 (`all_features_serialized_before_labels`); lượt003 tái dùng aggregate và chỉ dựng graph RAM qua guard sau lỗi tiến trình. Bước4 dùng gán đã lưu003; bước D/D0 tiếp ở005. Các mốc riêng ở progress002/003 và manifest005. Không cộng các pha song song thành thời gian lịch.

Bước5 có checkpoint bắt đầu xấp xỉ tại `handoff-progress.jsonl`, còn giờ/elapsed chương trình chính xác ở từng file kiểm. Bước6 có mốc báo cáo hỏng đầu, kiểm bảng và hợp nhất; thời gian soạn riêng chưa đo tách, không gán mốc file thành giờ bắt đầu. Lỗi từng lượt và snapshot script nằm trong thư mục lượt; giữ cả report-attempt001, independent-statistics-attempt001 và final-verification-attempt001.

Tổng `results/T-028/` trước ghi bản chi phí: 362373286 byte trên 185 file, khoảng 0.362 GB thập phân; gồm đầu ra trước đây, mọi lượt hỏng, snapshot và bản sao đầu ra chính. Nguồn từng file/hash/byte: `cost-observed.json` → `result_directory_snapshot`. Đây là snapshot, không gọi là dung lượng cuối. Thực tế đĩa vượt đầu trên ước lượng 0,3 GB chưa kiểm trong SPEC vì giữ lượt và bản trung gian; phần bàn giao chỉ thêm metadata/kiểm, không có lượt phương pháp dài mới.

RAM đỉnh, CPU và token chưa đo; không xác nhận ước lượng RAM 0,5–2 GB bằng thời gian ngắn. Không tải thêm dữ liệu, EC2 hoặc cài môi trường; dùng Python có sẵn với -B. Nezha payload/graph chỉ ở RAM; trên đĩa là thống kê/bằng chứng được phép. Nguồn: `cost-observed.json`, manifest/progress các lượt và final-verification khi chốt.

## Sửa sau phản biện R1–R5 (08/10/2026)

Lượt riêng `phan-hoi-review-001`, dùng cờ và thống kê đã lưu. Không đọc raw, tính lại tín hiệu hoặc chạy phương pháp. Mở lượt lúc 2026-10-08T12:48:10.994853+07:00; snapshot 2026-10-08T13:02:25.555842+07:00. Thời gian lịch tới snapshot 854.561 s; chương trình sửa/gom bảng 3.914 s. Thời gian lịch gồm soạn và kiểm, không là CPU hoặc công agent thuần.

Dung lượng lượt tại snapshot 125396142 byte; toàn results/T-028 489954955 byte, gồm bản trước sửa và các lần xuất/kiểm được giữ. Đây là snapshot, không gọi là dung lượng cuối. Nguồn mọi số: `results/T-028/runs/phan-hoi-review-001/cost-observed.json`. RAM/CPU/token không đo; không tải, EC2 hoặc cài môi trường.
