# T-051 — Kết quả dev chế độ (a)

T-051 kiểm xem thời điểm khởi phát có giúp E5 giữ bằng chứng tự sinh, cạnh tĩnh có đổi phân loại và vùng nghi ngờ, và kết cục của từng thành phần khối K có đổi trong chuỗi cuối. Nền theo Q-241 và WHY-75. Các phép so dùng ba thế giới, chấm RR theo kỳ vọng của nhóm hòa và lấy N1 từ cửa sổ giả RE2-TT. DT18 và MRP vẫn yêu cầu đánh giá trên dữ liệu độc lập, đối chứng đủ mạnh và nhãn vùng ở nơi đánh giá độ đúng của vùng ảnh hưởng.

## T11 — Giữ E9 tắt cho bước kế

Luật C trả **KHÔNG TÁC DỤNG** ở cả ba thế giới. ΔMRR gộp là 1/104, ΔMRR RE2-TT là 1/60, Nezha-OB bằng 0. Ở P, E9 phủ quyết 11 kênh trong 5 ca thật. Có 72 kênh thiếu khởi phát, 186 kênh được xét nhưng không phủ quyết, 197 kênh bị chặn bởi cạnh E2. Đếm một lần theo mã kênh trong mỗi ca, tách các đường giải thích. Bốn ca phủ quyết giữ nguyên RR. C-e có 30 cặp hợp lệ, ΔN1 bằng 7/30, dưới ngưỡng HẠI. [Luật và C-e](t11-001/score/law.json) · [Các ca](t11-001/score/mechanisms.json)

- **Cửa sổ 55.** Kênh latency-90 của root ts-order-service xuất hiện sớm hơn kênh CPU giải thích ở ts-station-service 50 giây. E9 đổi F_I của kênh root từ 0 lên 1. Root vẫn ở tầng 1 và vượt ts-auth-service trong tầng, RR từ 1/2 lên 1. Một kênh khác ở ts-order-other-service cũng được phủ quyết trong cùng lượt. [Đường giải thích và khóa](t11-001/55.json) · [RR theo ca](t11-001/score/mechanisms.json)
- **Cửa sổ 59.** Cùng root ts-order-service, E9 phục hồi kênh workload của ts-config-service sau khi kênh này xuất hiện sớm hơn kênh socket giải thích 100 giây. Root vẫn đứng đầu, RR giữ 1. Vì thế phát hiện khởi phát sớm và phục hồi một kênh không tự suy ra chẩn đoán root tốt hơn. Trong lượt này không có ca RR giảm để lập cặp đối chiếu tác hại. [Đường giải thích và khóa](t11-001/59.json) · [RR theo ca](t11-001/score/mechanisms.json)

Ngưỡng δ = 0,005 đổi kết cục sang GIÚP. Khoảng bootstrap theo ô 95% cho ΔMRR gộp là [0, 0,0294], với 260/1.000 mẫu ra GIÚP. Hành động theo ngưỡng chính là giữ tắt. Mức ủng hộ có điều kiện theo một ca đổi RR và theo ngưỡng đã khai. [Độ nhạy](t11-001/score/robustness.json)

## T12 — Giữ cạnh quan sát cho KB

Luật C trả **KHÔNG TÁC DỤNG** ở cả ba thế giới. Ở P, hợp cạnh làm đổi F_I trong 19 ca thật và đổi trật tự nhóm hạng trong 11 ca. RR của root giữ nguyên ở cả 52 ca. C-e có 30 cặp hợp lệ với ΔN1 −7/10. [Luật và C-e](t12-001/score/law.json) · [Các ca](t12-001/score/mechanisms.json)

- **Cửa sổ 03.** Cạnh tĩnh ts-user-service → ts-auth-service cho E5 đường giải thích mới. Kênh CPU giảm của ts-auth-service đổi từ tự sinh sang kế thừa. Vùng liên thông E7 cách 2 tăng từ 13 lên 22 thực thể, cách 1 vẫn 5. Root ts-order-service giữ RR 1/2. [Cạnh, F_I, khóa và vùng](t12-001/03.json)
- **Cửa sổ 43.** Hai cạnh tĩnh nối ts-auth-service với ts-user-service và ts-verification-code-service làm đổi phân loại ba kênh của root. Root vẫn đứng đầu, còn vùng E7 cách 2 tăng từ 1 lên 12. Hai ca cho thấy cạnh có thể đổi phân loại của root hoặc của ứng viên khác và mở rộng vùng mà RR giữ nguyên. [Cạnh, F_I, khóa và vùng](t12-001/43.json)

Ở RE2-TT, trung bình vùng E7 cách 2 tăng từ 10,70 lên 17,13 thực thể. Độ chứa root theo cách 2 giữ 29/30. Trên Nezha-OB, các giá trị tổng hợp vùng của cả hai cách giữ nguyên. Độ chứa root chỉ là một phép mô tả. Cần nhãn vùng để xác định các thực thể mới có bị ảnh hưởng hay không. [E7 theo ca và dataset](t12-001/score/regions-controls.json)

C-d1 trên RE2-TT đổi MRR từ 195768029/280098000 xuống 1536079/2387616. C-d2 khớp ở từng cửa sổ. C-d3 trên RE2-TT có 20 ca đồ thị con chu trình ở cả hai vế. Số ca có đầu ra OK tăng từ 4 lên 6 và RR của root vẫn bằng 0 trên mẫu số 30. C-d3 ở Nezha-OB suy biến do thiếu span gốc theo Đ12. Các đối chứng này mô tả tác động thay cạnh trên từng quy tắc. Chưa phân xử lợi ích của quan hệ phụ thuộc thật hoặc hiệu quả trên dữ liệu độc lập. Revision của hai đồ thị tĩnh so với benchmark còn OPEN. [Đối chứng theo ca và dataset](t12-001/score/regions-controls.json)

Ở cả T11 và T12, V0 vẫn là CAUSE_FOUND trên 30/30 cửa sổ giả ở mỗi vế. N1 phân biệt được thay đổi về số thực thể tầng 1 trong các cửa sổ đó. Cả hai đại lượng chưa cung cấp hiệu chuẩn cho verdict. [C-e T11](t11-001/score/law.json) · [C-e T12](t12-001/score/law.json)

## KB — Bốn kết cục giữ nguyên

| Đảo riêng | Kết cục ở cả ba thế giới |
|---|---|
| E1 | GIÚP |
| E2 | TRÁI CHIỀU theo dataset |
| E3(a) | HẠI |
| E5 | GIÚP |

Sau T11 và T12, chuỗi vẫn dùng đúng nền của gói thắng T-053. Kiểm đủ 82 cửa sổ × 5 cấu hình. Đối chiếu hash đầu ra và cấu hình, hash đầu vào chuẩn hóa, trường hợp phục hồi z, cạnh quan sát, G_N và vế nền với T12. Sau đó seal và áp lại luật cho bốn cặp, gồm UV-6 của E3(a) và M5 của E5. Việc tái sử dụng xác nhận kết cục trong bối cảnh cuối thực sự được chọn. Vì bối cảnh không đổi, đây là tái lập trên cùng dev. Phép này chưa kiểm tương tác VC × E5 hoặc bối cảnh giả định có E9 hay cạnh tĩnh. [Hồ sơ nguồn](kb-002/sources.json) · [Kết cục](kb-002/score/summary.json)

## Bàn giao

Nền đề xuất cho T-052 là E1-U, E2-C, E5, z+S1, E6a, ε = 0,05, α = 0,01, chế độ G3/D1 trong mã, cạnh quan sát. E3(a), E3b, E6b, E9 và T12 tắt. Giữ cờ đánh đổi E2.

Chọn này có căn cứ cho dev chế độ (a). Chiều đảo PageRank, VC × E5, revision cạnh tĩnh, hiệu chuẩn verdict, nhãn vùng, lợi ích độc lập của quan hệ, chế độ (b), RE3-OB và FlashTicket còn OPEN. G3, test và dữ liệu giữ ngoài vẫn khóa.

Bảng độ đo giữ mẫu số cố định theo dataset và cả ba thế giới. Retrieval@5 bằng Hit@5, còn Rerank@1 trong K=5 bằng tổng Hit@1 chia tổng Hit@5. [T11](t11-001/score/metrics.json) · [T12](t12-001/score/metrics.json) · [KB](kb-002/score/metrics.json)
