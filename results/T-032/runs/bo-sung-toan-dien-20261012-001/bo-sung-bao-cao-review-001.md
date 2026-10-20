# Bổ sung báo cáo sau kiểm lại T032/T033 — 13/10/2026

**Gói sửa văn bản đã được Minh duyệt.** Đọc [bảng câu cũ → trạng thái mới](doi-chieu-dien-giai-review-001.md) trước khi dùng H6/WHY-47, H8/return, CIRCA và K5 làm đầu vào G2. Báo cáo này bổ sung BAO-CAO-TONG-HOP.md; bản cũ và số thực nghiệm giữ nguyên.

## 1. H6 và hai chỉnh N1/N2

Danh sách cũ có 13 cặp / 11 ca; 12 cặp / 10 ca có quan hệ cũ. Trên 12 cặp đó, root trên/hòa/dưới:

| Dataset | Bản theo lời văn to_p | Tác giả ms, chọn đặc trưng 1 | Tác giả ms, chọn đặc trưng 3 |
|---|---:|---:|---:|
| RE2-TT, 4 cặp | 0/1/3 | 3/0/1 | 1/3/0 |
| Nezha-OB, 8 cặp | 0/1/7 | 7/0/1 | 7/0/1 |

Ở RE2-TT ngưỡng 1, hai cặp root trên do caller có điểm −1. Ngưỡng 3: một cặp root trên do caller −1, ba cặp hòa đều root/caller −1. −1 là fallback vì không có singleton pattern được giữ, không phải quan hệ vào/ra bằng nhau. Cặp thứ 13 dev-95e164235f không có quan hệ cũ; tác giả hòa có điểm ở ngưỡng 1, NO_EVIDENCE ở ngưỡng 3. Không gộp NO_EVIDENCE thành hòa hoặc bỏ cặp này.

Trong 7 ca Nezha có quan hệ cũ, 6 ca frontend lấy max từ pattern 2–3 dịch vụ; 1 ca singleton. Đây là ứng viên giải thích cụ thể, chưa là kết quả thay riêng một bước. RE2 có 3 ca khác: top cũ ts-station-service, root không có root_best. Trong nhánh tác giả ms/ngưỡng 1, frontend đứng đầu 1 ca dev-515c5f2190; đính chính số 0 của reviewer.

**Câu dùng cho G2:** số 0/4 và 0/8 đúng bản theo lời văn. Chúng không xác nhận abs là nguyên nhân đủ hoặc giữ dấu là điều kiện bắt buộc. Các nhánh tác giả có kết quả/fallback khác theo cấu hình. Chưa xác định bước Y đủ giải thích mọi chênh giữa pipeline. Giữ dấu và thay quy tắc pattern là ứng viên, chưa chọn P6.

Nguồn: [ledger](closure-ledger-review-001.json)#/h6_pair_audit và /pattern_candidate, dẫn từng ca tới cases.json cũ/Full008. Câu thay và đủ vị trí cũ ở tài liệu đối chiếu §1–3; phụ thuộc WHY-47 đã đính chính bằng phần nối chính thức.

## 2. Các diễn giải khác đã cập nhật

| Nhóm | Câu dùng hiện tại | Nguồn |
|---|---|---|
| Return/H8 | Log lỗi tại root có phản ứng; FrontSuccessRate giảm tại frontend. SimpleRCA chỉ đếm tăng và BARO bỏ cột hằng nền nên bỏ qua kênh giảm này. Hai checkout không được coi có metric riêng root phản ứng. Không quy thiếu tín hiệu toàn dataset; onset/duration/support và thiết kế dùng tín hiệu còn mở. | Đối chiếu §5; findings.json#/response/return và /success_rate/return |
| CIRCA | Độ dài đơn lẻ không giải thích đủ; composition/recency/pha lấy mẫu và residual scale còn là ứng viên. Không coi tăng train là lời giải đã chứng minh. | Đối chiếu §6; findings.json#/circa/fixed_parent_group_diagnostic/at_least8_parents |
| K5/log | Có outcome ở access log/literal backend. Thiếu certified invocation join, provenance deployment và chuẩn vận hành độc lập; không thiếu outcome ở mọi nơi. | Đối chiếu §7; các summary T033 được dẫn ở ledger |

## 3. Baseline cần Minh quyết

Trên Nezha-OB, tác giả latency-only ngưỡng 1 đạt Hit@1 bi quan 10/22, kỳ vọng 11/22; ngưỡng 3 đạt 9/22 và 9,5/22. BARO bảng chính đóng băng đạt 8/22 kỳ vọng. RE2-TT tác giả ngưỡng 1 đạt 17/30, ngưỡng 3 đạt 15/30; TORAI B 26/30.

Đề xuất: giữ bảng P3 hiện tại; trình nhánh hỗ trợ này thành ứng viên baseline ở G2/P7. Minh quyết chỉ giữ chẩn đoán hay đưa vào kế hoạch baseline với hợp đồng đầu vào/cấu hình/tuning/chấm khai rõ. Chưa chọn ngưỡng theo điểm dev, chưa tự sửa baseline. Nhánh này chưa tái lập default/bài đầy đủ; chưa khẳng định ưu thế tổng quát. Nguồn và mẫu số toàn cohort ở đối chiếu §4 và ledger#/baseline_comparison.

## 4. Phần còn kiểm được

Đối chiếu cặp H6/N1/N2 đã làm từ JSON đã lưu. Phép full log-domain cho hai ca dev-3ae0a6c15a/dev-ba831dbeb8 **còn kiểm được, chưa chạy; chi phí chưa đo**. Frozen-normalizer loglineage không thay một lần tính đầy đủ posterior/normalization. Câu phụ thuộc: underflow có thay đường MAP/CP đầy đủ không; không suy detector mới tốt hơn.

Ứng viên pattern còn cần phép phân xử riêng giữ các yếu tố khác và kiểm khả năng tái dùng trung gian; chưa chạy. Gói này không nhận mọi phép hữu ích hiện có đã xong. Onset/báo giả vận hành/quan hệ ẩn/lợi ích đồ thị vẫn cần đúng bằng chứng, thiết kế và quyền tương ứng.

Nguyên văn quyền Q144 vẫn là khoảng trống truy nguyên; lời duyệt sửa lượt này không xác nhận lịch sử ấy. Chưa có căn cứ kết luận vi phạm quyền. Khi Minh cung cấp nguyên văn hoặc xác nhận chữ, cần trình phần sổ quyền được giao; lượt này không sửa DECISIONS.

## 5. Hoàn thành và bàn giao

Đã ghi đủ gói bảy file được duyệt, gồm N1/N2 và danh sách câu cũ đầy đủ; không thực nghiệm mới. Hash, JSON, bảng/số/nguồn, prefix ba file nối và tập file cuối được ghi trong manifest-review-001.json. LOG hai task là đường mở phiên tới bản đính chính; STATE không đổi trong gói này.

Gói sửa xử lý phản đối về căn cứ văn bản H6; không chứng minh cơ chế chưa phân xử hoặc tự nghiệm thu T032/G2/RQ2. Đề xuất dừng bất đồng nội dung như bản kiểm lại Claude; Minh quyết gửi kiểm tiếp hay dừng. Prompt theo nguyên khối mẫu nằm ở cuối hai LOG. Đề xuất commit: “Đính chính căn cứ H6 và cập nhật diễn giải bổ sung T032/T033”; chưa commit/push.

