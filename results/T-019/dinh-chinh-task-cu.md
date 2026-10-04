# Đính chính task cũ — để Claude kiểm

Không sửa file task cũ. Kiểm độc lập nguồn/số đo tại T-019; không gọi mọi phần bổ sung ngoài SPEC cũ là lỗi.

## D1 — T-003: điều hướng Sock Shop chưa khớp phạm vi T-002

- **Task/file:dòng:** `results/T-003/the-dataset-ngoai-rcaeval.md:19`.
- **Cũ:** “Sock Shop thuộc T-002/P2; không tự thêm raw vào gói.”
- **Sai gì:** T-002 không viết thẻ SS. `tasks/T-002-the-dataset-rcaeval/SPEC.md:10` chỉ giao bốn thẻ TT/OB; `results/T-002/the-rcaeval.md:560` nói rõ hai mẫu SS được kiểm schema nhưng không viết thẻ SS/RE1 ngoài SPEC. Dẫn người đọc về T-002 để tìm hồ sơ SS toàn release có thể khiến tưởng phần G1 này đã hoàn tất.
- **Bằng chứng và phản bác:** T-003 vẫn nhắc G1 phải trả lời Sock Shop. T-002 có schema hai mẫu SS, nên referral không hoàn toàn vô căn cứ. Đây là lỗi điều hướng/phạm vi, không phải sai số census hoặc bằng chứng T-002 bỏ việc đã được duyệt.
- **Kết luận ảnh hưởng:** mức đủ hồ sơ để G1 trả lời dùng/không dùng SS. Không ảnh hưởng số TT/OB của T-002.
- **Đã triển khai T-019:** thẻ riêng đủ 10 mục/9 tiêu chí; census toàn release; file thực và nhãn; sổ ca; nguồn kiến trúc tĩnh với giới hạn.
- **Đề xuất mới nguyên văn:** “T-002 chỉ kiểm hai mẫu Sock Shop ngoài bốn thẻ chính. Thẻ riêng Sock Shop và census toàn release nằm ở T-019. Gói T-003 không thêm raw Sock Shop.”
- **Mức:** không chặn T-019; Minh duyệt trước khi sửa file cũ.

## Phần kiểm mới không phải lỗi của task cũ

1. Bảng nguồn HF đã snapshot tại `results/T-002/public-metadata/run-002/sources/hf-README.md:41` ghi RE3-SS F1–F5; prose dòng52 giới hạn F5 ở OB. GitHub README và census toàn SS chỉ F1–F4. Đây là lệch nguồn, không sửa snapshot. T-002 không có thẻ SS nên không quy thành sai số thẻ T-002. T-019 đã giữ hai lời nguồn và đếm thật trong thẻ/census; nếu mở rộng `public-sources.md:61`, đề xuất thêm: “Bảng HF cũng ghi F1–F5 cho RE3-SS, nhưng GitHub README và tree ghim chỉ có F1–F4. Census chi tiết nằm ở results/T-019/.”
2. T-002 nói có tám `root_cause.txt` tại SS và chưa đọc chi tiết; số file đúng. T-019 kiểm thấy chỉ bảy nội dung khác nhau, một nhãn `front-end_f2_2` lặp nhãn ca trước và nằm ngoài cửa sổ own log. Đã triển khai `sources-audit/label-audit.json`, `inspection/root-cause-labels.json` và giới hạn chấm tại thẻ. Chưa có task cũ khẳng định tám nhãn hợp lệ để đính chính.
3. `results/T-006/kiem-dung-dan.md:66` nói local RE1-SS chứa100ca fse-ss+25disk: đã kiểm cả raw/simple/hash và đúng. `results/T-007/kiem-dung-dan.md:41` về90ca RE2-OB đúng trong phạm vi đã kiểm; T-019 bổ sung metric-content. Không đính chính hai câu này. Năm cặp CSV→HF có khác dòng thiếu timestamp không phủ định byte-identity giữa các file local.

## Phạm vi audit

Quét77file SPEC/LOG/REVIEW/báo cáo T-000–T-012 để định vị nhận định liên quan; đọc sâu T-002, T-003 và phần lineage/biên T-006/T-007. Chi tiết ở `sources-audit/prior-task-relevance-scan.json`, `source-report.md` và `lineage/report.md`. Không chạy RCA hoặc tái lập mọi phương pháp/dataset cũ. Không tìm thấy lỗi đáng kể khác trong các nhận định SS/lineage được kiểm; không suy rằng toàn task cũ đúng.
