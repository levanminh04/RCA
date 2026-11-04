# T-050 — Xếp hạng T9 và vùng nghi ngờ T10

## Kết quả T9 trên dev chế độ (a)

Luật C trả **HẠI** tại P, S_lo và S_hi. Hành động theo SPEC là **giữ E6a+S1, tắt E6b**. Đây là đề xuất nền cho T-051, chờ phản biện và Minh nghiệm thu. Nền giữ E1-U, E2-C, E5, z+S1, cổng G3/D1 trong mã và cạnh quan sát. E3(a), E3b, E9 và T12 tắt. Cờ đánh đổi E2 từ T-049 vẫn đi kèm.

| MRR tại P | RE2-TT (30 ca) | Nezha-OB (22 ca) | Gộp (52 ca) |
|---|---:|---:|---:|
| E6a+S1 | 0,9278 | 0,8727 | 0,9045 |
| E6a+S0 | 0,9278 | 0,8727 | 0,9045 |
| E6b | 0,8700 | 0,8727 | 0,8712 |
| E6b − E6a+S1 | −0,0578 | 0,0000 | −0,0333 |

Nguồn số ở [chấm](cham-001/cham.json) `/cau_hinh/{S1,S0,E6b}/MRR_the_gioi` và [luật](cham-001/luat.json) `/theo_the_gioi`. Ba thế giới có cùng chênh MRR. Trong mỗi thế giới, RR giảm ở ba ca và bằng nhau ở 49 ca. Ba ca giảm thuộc một ô của RE2-TT. Bước 3 của luật trả HẠI vì mức giảm RE2-TT vượt ngưỡng 1/30. E6b và E6a+S1 có cùng N1 và V0 trên đủ 30 cửa sổ giả. C-e có mẫu số hợp lệ, chênh N1 bằng 0 và vế hại không kích hoạt ở h = 0,5, 1 hoặc 2. Phép này giữ nguyên bằng chứng và tầng nên C-e không phân xử an toàn báo động của bước xếp hạng.

Ở cả hai ngưỡng δ = 0,005 và 0,02, kết cục vẫn là HẠI. Bootstrap theo ô có 678/1.000 mẫu HẠI và 322/1.000 mẫu KHÔNG TÁC DỤNG. Bỏ từng ô có 22/23 lượt HẠI. Bỏ ô `ts-travel-service|loss` cho KHÔNG TÁC DỤNG. Các tỷ lệ này mô tả độ bền trong tập dev với cùng ngưỡng dataset, không phải xác suất hiệu quả trên dữ liệu mới. Hành động chính theo nhánh HẠI. [Độ bền](cham-001/do-ben.json) `/bootstrap`, `/do_nhay`, `/bo_tung_o`, `/h`.

### Vì sao ba ca đổi hạng

Các nút là dịch vụ. Cạnh đi từ bên gọi sang bên được gọi theo span cha–con trong N ∪ A. Log và metric gắn vào dịch vụ, trace cung cấp kênh nút và cạnh. E1/E2/E5 dùng quan hệ để tạo và phân loại bằng chứng trước khi xếp hạng. E6b dùng `max(s)` trong K_I để khởi tạo v và làm trọng số đích trong bước chuyển khối lượng. Khi có khối lượng dương, khóa E6b ưu tiên π làm tròn rồi đến K_I và K_raw.

| Cửa sổ | Ca | RR E6a+S1 | RR khi thay π bằng v | RR E6b | v của root → π |
|---:|---|---:|---:|---:|---:|
| 05 | dev-a915aa2424 | 1/3 | 1/3 | 1/5 | 0,18407 → 0,04024 |
| 13 | dev-7f1b6b071d | 1 | 1 | 1/5 | 0,25956 → 0,06374 |
| 21 | dev-a5cabe5fa7 | 1 | 1 | 1/5 | 0,22828 → 0,05442 |
| 23 | ca đối chiếu cùng root, lỗi disk | 1 | 1 | 1 | 0,99713 → 0,99026 |

Tại P, root `ts-travel-service` ở cả ba ca loss có kênh tự sinh và K_I dương. Ví dụ cửa sổ 13 có K_I.max khoảng 4.828. Khối lượng chuyển ra ngoài root khoảng 0,04007 mỗi bước ở π, còn chuyển vào từ nút khác khoảng 0,01070. Năm đích dương nhận khối lượng trực tiếp từ root. Khi lấy π làm phần đầu của khóa, order, route, train và ticketinfo vượt root. Cửa sổ 05 và 21 cũng có năm đích dương trực tiếp và root rơi xuống hạng 5. Khóa giữ v cùng K_I/K_raw tái tạo đúng RR của S0 và S1 ở ba ca. Như vậy phần thay v bằng π giải thích toàn bộ chênh RR quan sát được, trong khi hai bước đổi khóa cục bộ có chênh RR bằng 0. Không có ca tăng RR để lần theo.

Cửa sổ 23 cùng root, cùng số đích nhận khối lượng trực tiếp, cũng có chuyển ròng ra khỏi root. Tuy nhiên v tập trung mạnh vào root từ đầu. π giảm nhưng vẫn đủ để giữ hạng nhất. Đối chiếu này phân biệt trường hợp giảm điểm mà đổi hạng với trường hợp giảm điểm mà giữ hạng. Nó chưa phân xử vì sao khối lượng đầu vào khác giữa loại lỗi, và chưa xác nhận mẫu hình ở ô khác. Đối chiếu theo ca và ba thế giới ở [phân tích](cham-001/co-che.json) `/*/comparisons`. Điểm và vết chuyển ở các bản ghi mà trường `replay` trỏ tới, dưới `/P/{S1,E6b,mass}`.

## T10 — Vùng nghi ngờ ở P trên E6a+S1

Cách 1 đi theo cạnh có hướng và dùng giải thích của E5 để giữ các nút phù hợp. Cách 2 lấy thành phần liên thông vô hướng trong đồ thị con bất thường. Kỳ vọng theo D20 lấy đều trên nhóm đầu của mỗi ca.

| Dataset | Cách | Xác suất vùng chứa root, trung bình theo ca | Số nút kỳ vọng |
|---|---|---:|---:|
| RE2-TT | 1 | 86,7% | 2,90 |
| RE2-TT | 2 | 96,7% | 10,70 |
| Nezha-OB | 1 | 81,8% | 1,59 |
| Nezha-OB | 2 | 95,5% | 2,91 |

Cách 2 chứa root thường hơn và tạo vùng rộng hơn trên cả hai dataset. Cả 52 root có mặt trong U và đồ thị con bất thường ở P. Mỗi nhóm đầu trên tập này có một thực thể. Phép tính hỗ trợ nhóm đầu hòa và đã qua fixture. Các giá trị mô tả vùng nghi ngờ tại P. Precision, Recall và F1 của vùng ảnh hưởng đầy đủ còn OPEN vì thiếu nhãn vùng. T-052 cần cập nhật mô tả trên cấu hình cuối. [Kết quả vùng](cham-001/vung.json) `/datasets`, `/rows`.

## C-c và C-g

| MRR tại P | RE2-TT | Nezha-OB | Gộp |
|---|---:|---:|---:|
| C-c, RRF k = 60 | 0,8833 | 0,5298 | 0,7338 |
| SimpleRCA M4 gốc | 0,8911 | 0,5375 | 0,7415 |
| C-g, SimpleRCA M4 thêm E6b | 0,7549 | 0,5334 | 0,6612 |

C-c giữ cả 52 ca. Bốn bản ghi TraceRCA RE2-TT ở trạng thái ERROR đóng góp 0 cho RRF. C-g có khối lượng dương và đổi thứ tự hoặc nhóm hòa ở 52/52 ca, không suy biến theo tiêu chí trước nhãn. Không có ca C-g thiếu bằng chứng hoặc dự phòng tổng bằng 0. Adapter giữ đúng tập SimpleRCA trả về, kể cả `istio-init` ở một ca RE2-TT, và giữ quy tắc nhóm điểm 0. So sánh này báo riêng, không tham gia luật chọn T9. [Đối chứng trước nhãn](doi-chung-002.json) `/counts`, `/rows`. [Kiểm nguồn](kiem-nguon-doi-chung-001.json) `/statuses`, `/outside_U_kept`. [Chấm](cham-001/cham.json) `/cau_hinh/{C-c,C-g}/MRR`. [Kiểm độc lập](kiem-cuoi-001.json) `/SimpleRCA_MRR_P`.

## Tái lập và giới hạn

- Kiểm hồ sơ T-049 bằng bản nguồn đã lưu. Tái tạo E6a+S1 ở đủ 246 khung, kiểm đầu vào, điểm, khóa, hòa, tầng, N1/V0 và vùng P. Cấu hình và file chung ghim trong [kế hoạch pilot](pilot-plan.json).
- Pilot EC2 đạt cả 12 khung khi so native với phát lại. Các cửa sổ ở hai dataset, gồm một cửa sổ giả RE2-TT. Tiến trình mới đọc lại và kiểm hash cả bốn cửa sổ trước khi chạy 78 cửa sổ còn lại. Tổng thời gian các cửa sổ pilot khoảng 88 giây. Phần phát lại còn lại khoảng 2,88 giây. Lượt chạy tuần tự trên một tiến trình. Có thời gian từng cửa sổ trong `complete.json`. RSS đỉnh của pilot chưa được ghi. Không cần tính lại chuỗi ngoài bốn cửa sổ pilot. [Nhật ký EC2 và biên nhận từng cửa sổ](ec2-001-download/ec2-001).
- E6b chạy với khối lượng dương ở cả 246 khung. Phần dư lớn nhất của phép cập nhật thêm là 8,19 × 10⁻¹³ theo chuẩn L1. Nhánh dự phòng E6b và các biên E7 kiểm bằng 11 fixture. Kiểm độc lập 572 RR, 1.000 bộ mẫu độ bền và 52 ca vùng. [Tự kiểm](kiem-cuoi-001.json), [fixture](fixture-002.log).
- [Seal pha 1](pha1-001/seal.json) được ghi vào LOG trước khi chấm. Chỉ dùng dev chế độ (a). Test và G3 nghiên cứu vẫn khóa.

T9 trả lời lựa chọn bước xếp hạng trên nền z hiện hành. T10 trả lời mức chứa root và độ rộng của vùng nghi ngờ trên dev. RQ3b trên dữ liệu độc lập, RQ3c với nhãn vùng, và RQ3d về tác dụng quan hệ của cả chuỗi vẫn OPEN. T9 thay cả cách ưu tiên PageRank và khóa xếp hạng. Phép thay π bằng v giúp phân tích ba ca cụ thể. Để đánh giá tác dụng quan hệ của cả chuỗi vẫn cần các đối chứng đã định trong MRP, cùng dữ liệu đánh giá được Minh cho phép. Phép này cũng chưa xử lý cờ đánh đổi E2, hiệu chuẩn verdict và chế độ (b).
