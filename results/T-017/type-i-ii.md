# Type I/II — luật phân loại của bài, không phải đầu ra SimpleRCA

Nguồn chính: PDF FSE26, §3.2.3, trang8–9. Đã xem trực quan bảng3 và đối chiếu arXivv2 trang7–8. Text đầy đủ ở `sources/fse26-pages.txt`; hash/PDF ở `sources/pdf-manifest.json`. CSV nguyên số công bố: `ty-le-type-cong-bo.csv`. Không chạy phân loại Type trên dataset nào trong task này.

## Định nghĩa và mức độ xác định

Bài xét triệu chứng từng service trong giai đoạn lỗi. Triệu chứng được gọi **pronounced (rõ)** khi metric liên quan lỗi hoặc số log lỗi vượt ngưỡng đặt trước; bài nêu ví dụ gấp hai lần trung bình giai đoạn bình thường ngay trước đó. Không vượt thì gọi attenuated (yếu). Bội số2 là ví dụ, không phải một đặc tả cấu hình chung đã công bố.

Gọi r là service bị tiêm và P là tập service có triệu chứng rõ theo luật trên:

- **Type I:** chỉ service bị tiêm có triệu chứng rõ, tức P={r}. Bài gọi overly localized (quá cục bộ).
- **Type II:** không service nào có triệu chứng rõ, tức P rỗng. Bài gọi fault under-expressed (lỗi biểu hiện quá yếu).
- **Type III:** bài nói triệu chứng mạnh hơn ở service khác service bị tiêm. Bài chưa cho công thức “mạnh hơn”, luật gộp metric/log, metric liên quan từng fault, hoặc xử lý hòa. Không tự thay câu này bằng một quy tắc bù của TypeI/II rồi gọi là luật chính xác tác giả.

Đây là định nghĩa chính xác ở mức mô tả; chưa đủ để cài lại classifier xác định và tái tạo từng nhãn Type. Bài không công bố ở §3.2.3: độ dài hai cửa sổ, threshold cuối mỗi dataset, cách xử lý baseline0/thiếu dữ liệu, quy tắc gộp nhiều metric, aggregation theo thời gian, từ khóa/error count cụ thể và hàm so “mạnh hơn”. Các OPEN này không được điền bằng mặc định M4.

**Có dùng nhãn:** có. TypeI/III cần biết service bị tiêm r để so với service khác; giai đoạn lỗi cần mốc tiêm/interval. Việc gọi metric “fault-relevant” cần biết liên quan loại lỗi; bài không cho code chứng minh fault_type được đọc trực tiếp. Không nhầm việc cần thông tin loại lỗi để diễn giải luật với chứng cứ rằng một file nhãn cụ thể đã được truyền vào hàm. Luật Type không hợp lệ làm bộ phát hiện/xếp hạng không biết root. SimpleRCA M4 không nhận r hoặc fault_type; không dùng Type để chọn metric, threshold hay ứng viên.

## Tỷ lệ nguyên số công bố

| Dataset | Số ca | Type I | Type II | Type III | I&II |
|---|---:|---:|---:|---:|---:|
| Nezha-TT | 45 | 0,93 | 0,07 | 0,00 | 1,00 |
| Nezha-OB | 56 | 0,91 | 0,09 | 0,00 | 1,00 |
| Eadro-TT | 81 | 0,75 | 0,25 | 0,00 | 1,00 |
| Eadro-SN | 36 | 0,50 | 0,44 | 0,06 | 0,96 |
| AIOps-2021 | 159 | 0,63 | 0,16 | 0,21 | 0,79 |
| RE2-TT | 90 | 0,67 | 0,17 | 0,17 | 0,83 |
| RE3-TT | 30 | 0,83 | 0,00 | 0,17 | 0,83 |
| RE2-OB | 90 | 0,59 | 0,28 | 0,13 | 0,87 |
| RE3-OB | 30 | 0,30 | 0,00 | 0,70 | 0,30 |
| RE2-SS | 90 | 0,60 | 0,27 | 0,13 | 0,87 |
| RE3-SS | 30 | 0,83 | 0,00 | 0,17 | 0,83 |
| All-Dataset | 737 | 0,68 | 0,18 | 0,14 | 0,86 |

Nguồn từng ô: `ty-le-type-cong-bo.csv`, trích bảng3 FSE trang8; bằng arXivv2 sau đối chiếu. GAIA không có dòng bảng3. Không thêm tỷ lệ cho GAIA hoặc dataset mới.

**Mâu thuẫn số trong nguồn:** Eadro-SN ghi I0,50+II0,44 nhưng I&II0,96. Tổng hai tỷ lệ hiển thị là0,94. Sai biệt0,02 không được giải thích chỉ bằng làm tròn tới2 chữ số của ba ô. Không tự sửa số công bố hoặc suy ra số ca thật; có thể lỗi in bảng hoặc denominator/luật gộp khác chưa nêu. Cần bản đếm gốc để giải quyết. RE2-TT 0,67+0,17 vs0,83 có thể do làm tròn hai tỷ lệ riêng, nên không coi là cùng loại mâu thuẫn. Phép kiểm số nằm trong `scripts/summarize.py` và `runs/final-summary.json`.

## Dùng ở G1 và giới hạn lập luận

0,86 là tỷ lệ của bộ dataset tác giả xét theo luật của họ; không là điểm SimpleRCA và không là độ khó tổng quát. TypeI dễ cho “service ồn nhất” khi tín hiệu đủ; TypeII có thể khó vì thiếu tín hiệu. Gộp I+II rồi gọi cả hai “dễ” là sai.

Phần nhận xét RE3-OB ở FSE trang9 nói classifier chỉ đếm error entries theo cách thẳng. Định nghĩa chung trang8 vẫn là metric hoặc log. T001 đã khái quát câu riêng RE3-OB sang toàn luật; đính chính ở `dinh-chinh-task-cu.md`.

Nhận định của tác giả rằng TypeI giải thích điểm cao còn có nguyên nhân khác: threshold/metric được chọn theo loại lỗi, mức quan sát, cửa sổ, cường độ tiêm, thông tin nhãn và code khác bài. T017 không xác nhận quan hệ nhân quả này. Không tự tính Type trên dữ liệu mới, không dùng tỷ lệ để chốt dataset hoặc cách chia thay Minh.
