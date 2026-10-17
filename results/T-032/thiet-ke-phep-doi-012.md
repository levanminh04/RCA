# T-032 — Thiết kế bản 012: ba phép kiểm chạy trên laptop (KT-3, KT-8 phần MicroRank, KT-15)

Người làm: Claude, phiên 12, 11/10/2026. File này viết **trước khi chạy** lượt nào của ba phép dưới đây.

**Căn cứ.** Lời Minh trong chat ngày 11/10/2026, sau báo cáo cuối lượt của phiên 12 (nguyên văn): "DUYỆT TOÀN BỘ NHỮNG PHÉP KIỂM CẦN CHẠY TRÊN LAPTOP, ĐÃ ĐÓNG BỚT ỨNG DỤNG, SAU ĐÓ CHO TÔI BÁO CÁO TIẾN ĐỘ NGẮN GỌN DỄ HIỂU, CÁC PHẦN CẦN TÔI QUYẾT, TÍCH CỰC HAY TIÊU CỰC, CÒN GÌ TỒN ĐỌNG". Các phép kiểm cần laptop trong `kiem-tiep.md`: KT-3, KT-8 (nửa MicroRank), KT-9, KT-15.

**Tôi hiểu phạm vi duyệt thế nào, và phần không chạy.**

- Chạy: KT-3, KT-8 (nửa MicroRank), KT-15. Tổng ước 30–40 phút máy.
- **Không chạy KT-9** (đổi cửa sổ train và đoạn chấm của CIRCA). Lý do: ước 1–2 giờ máy, vượt mốc "một lượt dự kiến quá 1 giờ thì dừng báo" của điều kiện làm việc; phải đổi cửa sổ đã khóa (Q-80, Q-82); và chưa có thiết kế nêu đổi sang cửa sổ nào. Tôi báo lại để Minh quyết riêng.
- Nửa TraceRCA của KT-8 chạy trên EC2, không thuộc lời duyệt này; không chạy.

**Điều tôi đã thấy trước khi viết file này.** Toàn bộ kết quả phiên 9–12. Riêng cho KT-15: tôi đã mở trung gian của một ca (`dev-16597725c1`) để xem cấu trúc file, và thấy nút `ts-food-service_latency` có khóa sau DA 2.104,09 trong khi điểm trước DA của nó là 76,73; phần chênh 2.027,36 đúng bằng điểm trước DA của nút `ts-preserve-service_latency`. Tức ở ca này DA chuyển điểm của **một** nút con sang nút cha, chứ không cộng theo số hậu duệ. Dự đoán ở mục 3 được viết sau khi thấy điều này; tôi ghi rõ để người đọc biết nó không còn là dự đoán mù.

Điều kiện chung: không sửa file nào trong `src/`; mỗi nhánh của mỗi ca là một tiến trình con; nhánh giữ nguyên phải khớp bản đóng băng từng bit, lệch thì dừng; RAM hệ thống 95% thì dừng; số của nhánh phép đổi đo tác động của một bước tính trên dev, không phải thành tích của một phương pháp.

## 1. KT-3 — MicroRank: ghép bộ chia theo bài gốc với đếm riêng

**Câu hỏi.** Sau khi thay bộ chia trace (bản 009), còn 25–26/47 ca root chưa hạng 1. Phần còn lại có phải do bước đếm phủ vẫn ưu tiên thao tác có mặt ở nhiều trace không?

**Bước bị đổi (hai bước, cùng lúc; đây là phép ghép có chủ ý, không quy được cho riêng bước nào).**

1. Hai tập trace "bất thường" và "bình thường": như nhánh `mo15`, `mo1p50` của bản 009, không đổi gì.
2. Số đếm của nhóm bất thường đưa vào spectrum: thay "số trace bất thường chứa thao tác" bằng "số trace bất thường mà chính thao tác có span mang cờ" (cờ là luật mean + 3·std của bản đang dùng, không đổi). Đây là định nghĩa M-C1 của bản 001 mục 4. Trọng số PageRank, số đếm nhóm bình thường, công thức dstar2, phép lấy lớn nhất theo dịch vụ giữ nguyên.

**Cách làm.** Script `scripts/laptop_contrast_v7.py` = v6 cộng một chuỗi thay thứ hai trong hàm `microrank` dựng lại từ mã nguồn: `'tracecounts':nums}}` thành `'tracecounts':__t032_counts__(after,traces,nums,is_anomaly)}}`. Hàm móc trả nguyên `nums` cho nhóm bình thường.

**Bốn nhánh.**

| Nhánh | Bộ chia | Số đếm nhóm bất thường | Vai trò |
|---|---|---|---|
| `shampc` | native | native (hàm móc trả nguyên) | Giữ nguyên; phải khớp bản đóng băng từng bit ở 52/52 ca |
| `c1h` | native | đếm riêng | Kiểm chỗ móc: hạng root phải trùng nhánh M-C1 của phiên 9 (`runs/microrank-core-aprime-c1-002`) ở mọi ca OK |
| `mo15c1` | luật của bài (1,5 độ lệch chuẩn) | đếm riêng | Phép ghép |
| `mo1p50c1` | luật chia nhóm của code | đếm riêng | Phép ghép |

**Dự đoán khai trước.**

- H-đếm-phủ: nếu phần còn lại do đếm phủ, số ca root hạng 1 của nhánh ghép cao hơn rõ nhánh chỉ thay bộ chia (21 và 22 trên 47), tôi đặt mốc "rõ" là từ 4 ca trở lên ở ít nhất một luật, và số ca root tụt hạng so với nhánh chỉ thay bộ chia ít hơn số ca tăng.
- H-không: nếu chênh dưới 4 ca hoặc số ca tụt ngang số ca tăng, đếm phủ không phải lời giải thích của phần còn lại; ghi đúng như vậy.
- Rủi ro biết trước: dưới bộ chia mới, một trace bất thường có thể không có span nào mang cờ 3·std; khi đó mọi thao tác có số đếm riêng bằng 0 và điểm có thể bằng nhau hoặc không hữu hạn. Ca như vậy giữ nguyên trạng thái mà hàm native trả (kể cả lỗi), đếm riêng, không gán giá trị.

**Mẫu số.** 52 ca; 4 ca nguồn ERROR và 1 ca N/A theo mốc 90% giữ đúng trạng thái. So với nhánh `mo15`, `mo1p50` trên đúng các ca cả hai cùng tính được.

**Giới hạn.** Hai bước đổi cùng lúc; nghĩ ra sau khi xem kết quả dev; không phải MicroRank gốc; ở Nezha-OB số trace bất thường rất ít.

## 2. KT-8 (nửa MicroRank) — bốn ca ERROR: bỏ thao tác không có ở đoạn nền

**Câu hỏi.** Ở 4 ca RE2-TT mà MicroRank dừng với "No normal baseline", nếu bỏ các span của thao tác không có ở đoạn nền thì root xếp thứ mấy?

**Bước bị đổi.** Ngay tại dòng kiểm `newops` của hàm `microrank`: thay vì ném lỗi, bỏ khỏi bảng sau mốc các span thuộc thao tác không có mức nền, rồi chạy tiếp. Chuỗi thay: `if newops:raise ValueError('No normal baseline for: '+','.join(sorted(newops)))` thành `after=__t032_dropnew__(after,newops)`. Mọi bước sau giữ nguyên. Nhánh tên `dropnew`.

**Tự kiểm có sẵn trong thiết kế.** Ở 48 ca không có thao tác mới, hàm móc không bỏ span nào, nên nhánh `dropnew` phải khớp bản đóng băng từng bit ở 48/48 ca. Lệch thì dừng.

**Đây là đổi đầu vào, không phải đổi một bước tính.** Kết quả của 4 ca chỉ dùng để trả lời câu "4 ca này nên ghi là phương pháp trượt hay không chạy được vì đầu vào"; không thay số đã chấm, không đưa vào bảng chính.

**Dự đoán khai trước.** Không có dự đoán về hạng. Điều ghi lại: số span và số trace bị ảnh hưởng ở từng ca; trạng thái; hạng root. Nếu bỏ span làm đồ thị trace thiếu nút cha và hàm native báo lỗi khác, giữ nguyên lỗi đó.

## 3. KT-15 — CIRCA: bước DA cộng gì, cho nút nào

**Câu hỏi.** Ba ca DA làm root tụt hạng mà không dính giá trị cực lớn đều có root `ts-auth-service`. DA có thiên lệch theo số hậu duệ không, hay là chuyển một điểm lớn của một nút con sang các nút cha?

**Không chạy phương pháp.** Chỉ đọc trung gian đã lưu của nhánh quan sát ở lượt `runs/circa-laptop-k2-001` (30 file `obs/score-graph.json.gz`; nhánh này đã khớp bản đóng băng từng bit ở 30/30 ca). Script `scripts/circa_da_addition_v1.py`.

**Theo mã CIRCA đã ghim** (`circa/alg/ci/__init__.py` dòng 137–155): nút có điểm từ ngưỡng 3 trở lên được cộng `child_score`, là giá trị gộp của điểm các nút con; nút con dưới ngưỡng thì chuyển tiếp điểm các nút con của nó.

**Đại lượng tính cho mỗi nút của mỗi ca.** Điểm trước DA; phần được cộng (khóa sau DA trừ điểm trước DA); số nút con và số hậu duệ trong đồ thị metric; nút con (hoặc hậu duệ qua nút dưới ngưỡng) có điểm bằng đúng phần được cộng. Gộp theo dịch vụ: phần cộng lớn nhất.

**Tự kiểm.** Với mọi nút có `child_score`: khóa sau DA bằng điểm trước DA cộng `child_score` (sai số tuyệt đối không quá 1e-6 lần độ lớn). Hạng root tính lại từ khóa sau DA trùng hạng đã chấm ở 30/30 ca.

**Hai giải thích và dự đoán phân biệt.**

- (a) Thiên lệch theo số hậu duệ: phần được cộng tăng theo số hậu duệ; tương quan hạng (Spearman) giữa hai đại lượng dương và ổn định qua các ca.
- (b) Chuyển một điểm lớn: trong mỗi ca, phần lớn các nút được cộng nhận **cùng một giá trị**, bằng điểm của một hoặc vài nút nguồn; số hậu duệ không dự đoán được phần cộng.
- Mốc đọc (đặt trước khi chạy đủ 30 ca, sau khi đã thấy một ca): nếu ở từ 2/3 số ca không có nút cực lớn, hơn nửa số nút được cộng nhận đúng giá trị của một nút nguồn duy nhất, đọc là (b).

**Phạm vi.** Bảng lập cho 30 ca; kết luận rút trên 19 ca không có nút cực lớn; ba ca root `ts-auth-service` in riêng (thực thể nào vượt root, nhận từ nút nguồn nào).

**Giới hạn.** Mô tả trên trung gian, không phải phép đổi. Chỉ RE2-TT, đồ thị gần như giống nhau giữa các ca, nên 19 ca không phải 19 quan sát độc lập.
