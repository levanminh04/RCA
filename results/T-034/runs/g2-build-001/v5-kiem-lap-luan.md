# T-034 V5 — Kiểm lập luận của `goi-g2.md` và `hai-phep-kiem.md`

Ngày 13/10/2026. Người làm tự kiểm (Claude). Đây là phép đọc, không phải phép chạy. Số được nhắc ở đây đều đã nằm trong hai văn bản và qua V4; con trỏ nguồn ở `render/registry.json` cùng thư mục.

Cách làm: đọc lại toàn văn hai file sau khi dựng; với mỗi nhận định quan trọng, đối chiếu phép kiểm cụ thể, chuỗi đầu vào → xử lý → trung gian → đầu ra, yếu tố giữ và đổi, ca đúng tương ứng, giải thích cạnh tranh và phạm vi. Quét các cụm “nguyên nhân là”, “chứng minh”, “đồ thị sẽ”, “chắc chắn” chỉ để tìm câu cần đọc lại.

## 1. Kết quả quét cụm từ

Năm chỗ khớp trong `goi-g2.md`, không chỗ nào trong `hai-phep-kiem.md`. Cả năm là câu phủ định hoặc giới hạn (“chưa có căn cứ để nói đồ thị sẽ giúp”, “không coi … là lời giải đã chứng minh”, “không chứng minh …”), hoặc là định nghĩa cờ M5 của T-028 (“chắc chắn đứng trước root” nghĩa là đứng trước ở mọi cách phá hòa). Không cần sửa.

## 2. Chỗ đã sửa sau khi đọc lại (trước khi phát hành)

| # | Chỗ | Vấn đề thấy khi đọc | Sửa |
|---|---|---|---|
| 1 | G2-H12, UV-7, UV-8 | Câu cũ so “có DA” với “bỏ cạnh” ở nhóm ca có nút cực lớn, nhưng so “không DA có cạnh” với “bỏ cạnh” ở nhóm còn lại, mà không nói rõ. Người đọc sẽ so nhầm với số baseline (có DA) | Ghi đủ ba biến thể ở cả hai nhóm: có DA; có cạnh không DA; bỏ mọi cạnh |
| 2 | G2-H16 | Câu cũ viết “M1: … ca” như số chung, thật ra là số của TraceRCA trên Nezha-OB | Ghi rõ phương pháp và dataset; dẫn Phụ lục A cho các phương pháp khác |
| 3 | G2-H22 | Gọi “báo động sai mỗi giờ” trái yêu cầu R4 của SPEC | Đổi thành “báo động mỗi giờ bình thường theo nhãn proxy” |
| 4 | G2-H19 | Bản dẫn xuất đầu đếm sai số ca “root không được dịch vụ nào gọi” (đếm trùng với tổng số ca không đo được) | Đếm lại theo trường `ly_do_phien_10`; kết quả khớp mục 5.4 của báo cáo T-032 |
| 5 | G2-H07 | Hiểu sai trường `no_signal_any_channel` thành “không hạng 1 ở mọi cách chấm” | Viết theo đúng định nghĩa trong file nguồn; thêm số của từng phương pháp |
| 6 | Mục 2.8 | Mô tả sai hai nhánh bộ chia MicroRank (tự đoán nghĩa từ tên khóa) | Đọc `results/T-032/thiet-ke-phep-doi-009.md`: `mo15` là luật của bài, `mo1p50` là luật chia nhóm trong mã; sửa nhãn |
| 7 | Mục 0, 2.1, câu 4 của mục 7 | Viết “hai baseline mạnh nhất” như thứ tự chắc chắn | Thêm: theo điểm ước lượng; khoảng bootstrap của bốn phương pháp đứng đầu chồng nhau |
| 8 | Mục 4.2, câu 8 của mục 7 | Viết lan “không giải thích phần lớn ca sai của MicroRank” mạnh hơn nguồn: T-032 mục 5.2 ghi đường gián tiếp của MicroRank chưa phân xử đầy đủ | Tách: BARO và CIRCA có cơ chế khác đã xác lập; MicroRank còn đường gián tiếp chưa phân xử |
| 9 | Mục 0, 6.2 | Viết TORAI B không chạy được trên Nezha-OB “vì nền quá ngắn”; nguồn chỉ nêu lý do đó cho CIRCA | Chỉ dẫn Q-85, không gán lý do cho TORAI B |
| 10 | `hai-phep-kiem.md`, bảng theo cặp | Cột mã tác giả để nguyên chữ tiếng Anh | Việt hóa |

## 3. Từng nhận định quan trọng

| Nhận định | Phép kiểm và chuỗi bằng chứng | Giữ / đổi | Ca đúng tương ứng | Giải thích cạnh tranh còn lại | Phạm vi | Kết luận V5 |
|---|---|---|---|---|---|---|
| Trên RE2-TT hai dòng đầu bảng không dựa vào quan hệ gọi | Bảng chấm T-024 (tính lại độc lập, V2); G2-H15: root không nằm trong khối do bước nhân quả xếp ở đơn vị nào | — | — | Khoảng bootstrap chồng nhau; chỉ năm root | dev RE2-TT | Giữ, đã thêm giới hạn về thứ tự |
| Bước chia trace của MicroRank bản thư viện là bước làm sai (G2-H01) | Đổi riêng bước chia: số ca hạng 1 tăng; mốc giả không lỗi vẫn xếp hơn một phần ba trace là bất thường | Giữ mọi bước sau; đổi luật chia | Bản thư viện chỉ có hai ca đúng, nên không có nhóm đúng đủ lớn để đối chiếu | Bộ chia thay thế dùng quy ước span đầu của ta | Các ca xét được của hai dataset | Giữ ở mức CT; phần còn lại ghi “chưa phân xử” |
| TraceRCA bản thư viện chấm thời gian chờ thành bất thường của dịch vụ gọi (G2-H03) | Mã → bảng nối lời gọi chậm với span mang cờ → phép đổi cờ sang phần chưa phủ | Giữ công thức điểm; đổi đại lượng gắn cờ | Hiện tượng có cả ở ca đúng | Công cụ ghi span ở RE2-TT không công bố | Cặp xét được | Giữ; văn bản đã nói rõ nó không phân biệt ca sai |
| BARO sai vì thang IQR trên nền phẳng (G2-H09) | Đổi thang: một phần cặp mất, không ca đúng nào hỏng ở RE2-TT | Giữ cột, cửa sổ; đổi thang | Ca đúng không bị hỏng ở RE2-TT; ở Nezha-OB có ca hỏng | Các cặp còn lại: cột đổi thật tại mốc | RE2-TT | Giữ, chỉ kết luận cho RE2-TT |
| CIRCA: phần dư gần không và bước cộng điểm (G2-H12) | Đầu vào → hồi quy → điểm → bước DA → hạng; phép bỏ cạnh | Giữ dữ liệu; đổi cạnh | Nhóm ca không có nút cực lớn làm đối chứng | Không | RE2-TT | Giữ, sau khi sửa điểm 1 ở mục 2 |
| Hai bộ phát hiện báo trước mốc; nguyên nhân chưa phân xử | Bảng T-025; can thiệp I1, I2; ba mức prior; phép E2 | Từng phép đổi một yếu tố hoặc một gói yếu tố (đã ghi) | Chỉ ba ca BOCPD có báo động đầu đúng | Nền không sạch, tải, bước nhảy đo đạc | RE2-TT | Giữ là “chưa phân xử”; không gọi là báo động sai vận hành |
| Underflow đổi MAP và điểm đổi ở một chuỗi, không giải thích báo động trước mốc (E2) | Bản giữ nguyên trùng bản lưu từng bit; tham chiếu số thực mở rộng trùng bản miền log; ví dụ nhỏ có đối chứng dương | Giữ X, prior, hazard, cập nhật; đổi số học | Ba chuỗi không khác làm đối chứng | Không còn giải thích “lỗi bản cài mới”: tham chiếu độc lập trùng | Bốn chuỗi của hai ca | Giữ; ghi rõ chưa biết ở các ca khác |
| Quy tắc chấm qua tập nhiều dịch vụ không phải bước đưa dịch vụ gọi lên trên root ở cờ một lần (E1) | Bản giữ nguyên trùng bản lưu ở mọi ca; tính lại độc lập bằng số học phân số | Giữ lời gọi, cờ, tập được giữ; đổi tập được phép chấm | Cặp hòa và cặp không có quan hệ cũ được giữ trong danh sách | Các bước khác của pipeline (chọn tập, gắn cờ) | Các cặp đã khai | Giữ; phần “bước nào gây chênh” ghi chưa phân xử |
| Lan phổ biến ở mức quan sát nhưng chưa có căn cứ nói nó gây phần lớn ca sai | Bảng lời gọi chậm (ngưỡng từ nền); vị trí của thực thể đứng trên root; phép T-D | — | Chờ có cả ở ca đúng | MicroRank: đường gián tiếp chưa phân xử | Ca đo được | Giữ sau khi sửa điểm 8 ở mục 2; câu tổng để “chưa phân xử” |
| Mười ứng viên ở mục 5 | Mỗi ứng viên dẫn dòng bản đồ hoặc DT18; có dự đoán bác bỏ được | — | — | Ghi ở từng ứng viên | — | Không ứng viên nào được chọn hay xếp hạng; UV-5 và UV-8 ghi rõ bằng chứng yếu hoặc bất lợi |
| Đối chiếu B16 ở mục 6.2 | Đọc lại B16 mục 4, 5, 6, 8 và phụ lục | — | — | — | Chuẩn tài liệu, chưa có hệ chạy | Giữ; các dòng “chưa có” là đề nghị, không sửa P9a |

## 4. Giới hạn của phép kiểm này

- Tôi là người viết hai văn bản, nên đây là tự kiểm; phản biện độc lập là việc của Codex.
- Các dòng bản đồ lấy diễn giải từ báo cáo T-028, T-029, T-032, T-033 và gói đính chính. Tôi đã đối chiếu số và trạng thái đính chính, đã đọc lại mã ở hai chỗ liên quan E1 và E2, nhưng không đọc lại mã của mọi phép đổi cũ.
- Số viết bằng chữ không qua V4; tôi đã soát bằng mắt các chỗ “cả ba”, “một ca”, “bốn chuỗi”, “một nửa” so với bảng.
