# Bàn giao P6 — đầu vào đồ thị, ngữ nghĩa và phép tính ứng viên

- **Nguồn:** T-040, lượt `runs/tong-hop-011/`. Số lấy từ `tong-hop.json`; ứng viên lấy nguyên từ `results/T-034/goi-g2.md` mục 5.
- **Phạm vi:** đây là đầu vào cho SPEC P6. **Không chọn** thuật toán, mức đồ thị, tín hiệu hay ngưỡng. Mọi ứng viên vẫn là ứng viên để thử (MRP §3, bảng mức căn cứ).
- **Phần này trả lời:** bước 2 của cô (ánh xạ log/trace lên đồ thị), DT18-NV2 (vùng ảnh hưởng, bất thường, xếp hạng trên đồ thị) và yêu cầu P5 “phép tính P6 nào thực sự nhận cạnh”.

## 1. Đầu vào đang có

| Đầu vào | Nút | Cạnh | Tín hiệu gắn được | Trạng thái |
|---|---|---|---|---|
| Graph trace RE2-TT dev (T-035) | Service; thao tác (entity, operationName) | Gọi chưa phân kiểu, hướng owner cha→owner con; quan hệ nội bộ ở mức thao tác | Trace/span theo khóa; log theo service+thời gian; metric mức service | T-035 chưa nghiệm thu |
| Graph trace Nezha-OB dev (T-035) | Service, pod alias; thao tác | Như trên; miền adapter quanh mốc | Như trên; Node chưa xác nhận là host | T-035 chưa nghiệm thu |
| Mô hình tĩnh FlashTicket (T-037) | 32 thực thể: service, gateway, DB logic/instance, cache, broker, host, external, identity | Gọi HTTP, dữ liệu, thông điệp (phát/nhận/logic), triển khai, SMTP | 153 địa chỉ theo B16; 130 gắn thao tác; 23 dùng chung | Đã đóng; thiết kế đích, runtime chưa kiểm |
| Mô hình tĩnh Online Boutique (T-039) | 23 thực thể gồm DB, cache, external | Gọi RPC/HTTP, dữ liệu | 53 khai báo địa chỉ | Đã đóng; revision chưa nối dataset |
| Mô hình tĩnh Train Ticket (T-038) | 110 thực thể | Gọi HTTP, dữ liệu, thông điệp | Mọi địa chỉ ở mức service, dùng chung | Chưa nghiệm thu; dùng bản sửa R1 của người làm, gói sửa đã dừng phản biện (Q-171) |

Hai sự thật chi phối mọi lựa chọn P6 trên dev:
1. **Không có kiểu cạnh trong trace dev.** Typed T rỗng ở mọi graph của cả hai dataset. P6 không được coi cạnh trace là “gọi đồng bộ đã xác nhận”. Không lấy kiểu tĩnh lấp vào trace.
2. **Cạnh dữ liệu và thông điệp không dựng được từ trace dev** (T-035 C1). Chúng chỉ có ở mô hình tĩnh. Trên OB, mọi 4 cạnh dữ liệu tĩnh đều vắng ở trace vì DB/cache không là nút quan sát.

## 2. Ngữ nghĩa nút, cạnh và tín hiệu (hợp đồng T-035 v2.1 + T-036 V2)

- **Nút thực thể** có ID ổn định và kiểu từ tập service/gateway/database/cache/broker/identity-provider/external/host/unknown. Kiểu chỉ nhận từ nguồn đã xác nhận; không đoán từ tên.
- **Nút thao tác** có khóa (thực thể chủ quản, tên gốc). Tên thiết kế và tên runtime tách riêng; tên runtime trống ở 65/65 thao tác FT và 993/993 thao tác TT, 47/68 ở OB.
- **Cạnh gọi** hướng bên gọi→bên được gọi. Ở trace dev chỉ có dạng “gọi chưa phân kiểu” từ quan hệ cha–con khác owner. Một cạnh không là một request mạng.
- **Cạnh dữ liệu** hướng service→DB/cache logic. DB logic khác instance; quan hệ DB→instance→host nằm ở `resource_bindings`, không là cạnh gọi.
- **Cạnh thông điệp** tách phát (producer→broker), nhận (broker→consumer) và logic (producer→consumer, chỉ khi có bằng chứng routing). Khớp chặng nhận chỉ xác nhận broker/scope/queue.
- **Cạnh triển khai** thực thể→host chỉ khi host đã xác minh. Trace dev không có; Node của Nezha còn OPEN.
- **Phép chiếu** thao tác→thực thể bỏ span-parent và quan hệ nội bộ. Phần chỉ có ở mức thực thể được báo riêng, không tạo thao tác giả.
- **Tín hiệu:** trace địa chỉ bằng khóa trace/span; log nối trace/span nếu có, nếu không thì thực thể+thời gian; metric gắn đúng scope. Metric mức service là bối cảnh dùng chung, không nhân thành bằng chứng độc lập của từng thao tác. Metric queue cần đủ (broker, scope, queue).

## 3. Ứng viên G2 → thông tin đồ thị cần → phép tính dùng cạnh

Cột “Không đồ thị còn giữ gì” nêu thông tin cấu trúc còn lại nếu P7 dựng nhánh bỏ quan hệ (MRP P7, WHY-07).

| Ứng viên (G2 §5) | Loại căn cứ | Nút/cạnh cần | Có ở đâu | Phép tính dùng cạnh | Không đồ thị còn giữ gì | Điều kiện thất bại / giới hạn đầu vào |
|---|---|---|---|---|---|---|
| UV-1 thời gian lời gọi gắn lên cạnh, tính cho bên được gọi | Sửa G2-H03, H06 (P4) | Cạnh gọi có hướng; thời lượng phía gọi từng lời gọi | Hướng có ở trace dev; thời lượng phải đọc từ span gốc, không có trong graph gộp | Gộp tỷ lệ lời gọi **đi vào** vượt nền của chính cạnh | Nếu gán theo owner span thì không còn cạnh; hướng vẫn có trong cặp cha–con | Root không được gọi (8 ca), cạnh thưa (7 ca); lỗi không làm chậm; kiểu cạnh chưa xác nhận |
| UV-2 thời gian tự xử lý | Sửa G2-H03 | Cây span cha–con, khoảng thời gian | Chỉ ở span gốc; graph gộp không đủ (T-035 §4) | Hợp khoảng thời gian span con | Vẫn dùng quan hệ cha–con trong trace | Bất đồng bộ, chồng lấn (Nezha), thiếu span con |
| UV-3 yêu cầu bất thường theo cả cây | Sửa G2-H01 | Cây từng request | Span gốc; không dùng đồ thị service | Gom thao tác theo cây | Vẫn dùng cấu trúc cây | Thao tác không có nền; mất span cha (D5) |
| UV-4 gộp điểm theo tập dịch vụ | Sửa G2-H05 | Tập dịch vụ cùng trace | Span gốc | Không dùng cạnh | Không áp dụng | Phụ thuộc mức cờ |
| UV-5 giữ hướng khi so đi vào/đi ra | So sánh, không bắt buộc | Cạnh có hướng | Trace dev | Hiệu số đi vào/đi ra của nút | Không có hướng | Căn cứ MT |
| UV-6 tín hiệu giảm và log tại root | Sửa G2-H07 | Nút + log theo service/thời gian | Log dev; địa chỉ tín hiệu ở mô hình tĩnh | Chưa dùng cạnh | Như phương pháp | Số dòng log ≠ số request |
| UV-7 chặn giá trị không hợp lệ trước khi lan | Nhu cầu kỹ thuật | Bất kỳ phép lan nào | — | Kiểm trước khi lan | — | Cách gộp điểm lên cha chưa có phương án |
| UV-8 hồi quy theo nút cha (kiểu CIRCA) | Ứng viên MRP; bằng chứng dev bất lợi | Đồ thị cha–con giữa thực thể | Trace dev; hoặc graph tĩnh OB (22 cạnh, gồm DB) | Hồi quy giá trị nút theo cha | Bản bỏ cạnh | Nhạy cửa sổ; graph tĩnh khác trace (mục 4) |
| UV-9 tiền xử lý chỉ dùng quá khứ | Sửa G2-H20 | Không cần cạnh | — | — | — | Kiểm tính đúng bản cài, không là lợi ích |
| Cạnh dữ liệu, thông điệp, triển khai | DT18-NV2, không phải hạn chế P4 | DB/cache/broker/host là nút | Chỉ tĩnh: FT đủ; OB dữ liệu; TT dữ liệu + thông điệp (bản sửa, có điều kiện); trace dev không có | Ví dụ: nhận diện tập dùng chung tài nguyên qua binding; lan qua cạnh dữ liệu | Bỏ các cạnh này | Không có dự đoán kiểm được trên dev; chỉ đánh giá được ở FT/P10 |
| Vùng nghi ngờ (đồ thị con liên thông) | DT18-NV2 | Cạnh nối phần tử bất thường | Trace dev (cạnh gọi chưa phân kiểu); tĩnh nếu chọn | Thành phần liên thông trên cạnh đã chọn | Không có vùng | Không có nhãn vùng trên dataset công khai; chỉ báo “vùng chứa root không” |
| Xếp hạng trên đồ thị (PageRank kiểu MicroRCA/MicroRank) | DT18-NV2, ví dụ của cô | Cạnh có hướng, trọng số | Trace dev | Lan điểm theo cạnh | Bản bỏ lan | Root không có cạnh; G2-H11 (đa số thực thể đứng trên root không nằm phía trên root theo quan hệ gọi) |

Cột “Có ở đâu” cho thấy phần lớn ứng viên P4 dùng **cây span hoặc cạnh gọi trong trace**, không dùng mô hình tĩnh. Mô hình tĩnh chủ yếu đáp ứng yêu cầu DT18 về cạnh dữ liệu/thông điệp và cấu trúc cho FlashTicket.

## 4. Đồ thị tĩnh so với đồ thị quan sát (đầu vào cho nhánh P7)

- **OB:** mức thực thể, tập trace là tập con của tập tĩnh ở mọi graph. Graph tĩnh thêm 9 cạnh không bao giờ quan sát được trong dev; 6 trong số đó có đích không phải nút trace. Một nhánh “đồ thị tĩnh” trên Nezha-OB vì thế khác nhánh quan sát chủ yếu ở các nút không có tín hiệu trace.
- **TT:** graph tĩnh **không** chứa trọn graph quan sát: 5 cặp chỉ có ở trace. Ngược lại, 120 khóa tĩnh vắng ở mọi graph thực thể (bản sửa R1, T-038 chưa nghiệm thu). Trong 120 khóa, 13 có cả hai đầu quan sát được nhưng không có cạnh; báo cáo mục 4.3 chia chúng thành bốn nhóm ứng viên: khác revision qua `ts-ticketinfo-service` (4), nhánh tùy chọn chưa chạy (2), đường ghi chưa chạy (4), chưa giải thích (3). Cơ chế chưa xác nhận. Nếu nhánh tĩnh của P7 giữ các cạnh này, chúng thêm đường lan giữa các service có tín hiệu mà dữ liệu dev không quan sát được.
- **Hệ quả:** P7 phải khai cạnh nào của nhánh tĩnh thực sự tham gia phép tính, và báo kết quả theo điều kiện revision chưa xác minh. Không dùng mức khớp tĩnh–trace để chọn cơ chế (QT4).

## 5. Quyết định còn thiếu cho SPEC P6

1. Mức đồ thị (thực thể hay thao tác). Trên TT, mức thao tác không so được với nguồn tĩnh (T rỗng ở mọi graph thao tác). Trên OB chỉ 10 cạnh thao tác đủ điều kiện.
2. Nguồn cạnh cho từng tầng (trace, tĩnh, hay cả hai) và cách xử lý cạnh tĩnh chưa từng quan sát.
3. Có dùng `resource_bindings` cho tài nguyên chung không, và phép tính cụ thể. Hiện chưa là cạnh tính toán của T-035.
4. Có dùng graph tĩnh TT không, và xử lý 13 cạnh hai đầu quan sát được nhưng không có cạnh thế nào (OM-13). Bản sửa R1 đã dừng phản biện nhưng T-038 chưa nghiệm thu; nên quyết sau khi T-038 được nghiệm thu.
5. Nhánh “không đồ thị” cho từng ứng viên: khai rõ thông tin cấu trúc còn giữ (cột tương ứng ở mục 3).
6. Các câu dev còn kiểm được của G2 §6.1 (chọn tập ở UV-4, underflow BOCPD, nhãn lan, cách gộp điểm lên cha) vẫn chưa được giao.

Những điều không được suy từ bàn giao này: lợi ích của đồ thị, cơ chế đã chọn, hay việc mở test.
