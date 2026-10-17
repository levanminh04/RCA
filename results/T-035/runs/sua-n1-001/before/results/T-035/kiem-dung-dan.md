# Kiểm đúng đắn T-035

| Phép kiểm | Kết quả | Bằng chứng |
|---|---|---|
| K1 phân hoạch, khóa và loại bằng chứng | Đạt mọi ca/cửa sổ | thong-ke-do-thi.json#/cases/<i>/checks; stats và graph witness; raw/unique/duplicate tách riêng |
| K2 lặp/seed | Đạt | Mọi khoảng dựng hai lần trong day-du-001; fixture seed0/1/2 khớp; seed-001-h1 và seed-002-h2 khớp hai ca pilot thật, mọi khoảng ở các ca ấy |
| K3 RE2-TT | Đạt từng ca, tập và tổng | runs/kiem-cuoi-001/K3.json; 27/55×24, 20/20×5, 21/21×1; K2 hai cấu trúc cũ chưa rõ quy trình đếm |
| K4 service_calls | Đạt | Cùng frame/khoảng, cutoff sau mọi start; checks/independent từng ca/cửa sổ. Không so các frame có quy tắc cắt khác |
| K5 phép chiếu | Đạt | Tập nút/cạnh thực thể bằng phép chiếu ở 1045 khoảng; loại cạnh nội bộ/span-parent, giữ endpoint context/inventory riêng |
| K6 Nezha metadata | Đã kiểm đầy đủ hai chiều | runs/kiem-cuoi-001/K6.json; nguồn sinh/tính độc lập OPEN; không đọc Weight hoặc chuỗi số |
| K7 fixture | Đạt F1–F11 và nhánh lỗi | fixture/inputs.json, expected.json viết trước bộ dựng; fixture-001 tới fixture-004, 18 nhánh; expected-error đúng loại |
| K8 kiểm tay và nhãn | Đạt trong phạm vi mô tả | Bên dưới; do-phu-theo-nhan.json#/totals khớp 8/7; D5 949/1293 |

Hai lần giống nhau được kiểm trên mọi cửa sổ, không chỉ fingerprint. Seed khác được kiểm trên hai dataset thật ở hai ca pilot và mọi fixture. Kiểm toàn bộ ca dưới mọi seed không được khai là đã làm; mã dùng sort tường minh, không dựa thứ tự set để xuất. K4 dùng bản cài độc lập đã có, không gọi CIRCA/scoring hoặc RCA.

## Kiểm tay từ dòng span tới hai mức

**RE2-TT, ca pilot:** witness nguồn tại `runs/pilot-002/cases/RE2-TT/dev-b8bd0abf60.json#/manual_trace_witness`.

- Trace mẫu 0: span gốc POST refresh của order, span con OrderRepository.findByAccountId, rồi find/getMore ts.orders đều thuộc order. Hai cặp nội bộ giữ ở thao tác; không tạo order→database chỉ từ chữ trong tên. Mẫu có nhiều span và phần cha không hiện trong đoạn witness, nên không gọi nó là một request mạng đầy đủ. Graph giữ orphan của toàn phạm vi, không điền cha giả.
- Trace mẫu 1: POST login của auth→UserRepository.findByUsername→find ts-auth-mongo.user, lặp ở hai lần thực thi. Cả năm span cùng thực thể; mức thực thể auth không có cạnh gọi khác owner, mức thao tác giữ login→repository→query. Không bịa nút database từ tên query. Đây là phân biệt cấu trúc mà gộp thực thể không giữ; chưa là hiệu quả RCA.

**Nezha-OB, ca pilot:** nguồn `runs/pilot-002/cases/Nezha-OB/dev-607751ac0a.json#/manual_trace_witness`.

- Trace mẫu 0 có bảy span: frontend root, frontend GetProduct/AddItem; ProductCatalog GetProduct là con của frontend GetProduct, Cart AddItem là con của frontend AddItem; sql.conn.query/sql.rows thuộc ProductCatalog. Mức thực thể có frontend→productcatalogservice và frontend→cartservice. Mức thao tác giữ tên của cả hai phía cùng owner và các cặp nội bộ. Hai span cùng tên GetProduct không gộp vì owner khác. Thời gian hai cặp phù hợp quan hệ bao ở mẫu này; thiếu kind trong CSV nên không nâng thành gọi-đồng-bộ xác nhận.
- Trace mẫu 1 có 68 span, nhiều lời gọi frontend tới GetProduct và PlaceOrder. Cạnh thao tác gộp theo tên/owner, giữ event_count; các lần thực thi không thành nút mới. Cần cây span gốc nếu P6 dùng thứ tự hoặc chồng lấn; graph gộp không giữ đủ chúng.

Đã đối chiếu các cặp có cả hai dòng witness với tập cạnh thực thể/thao tác full của đúng ca. Mẫu không đủ phân xử mọi trường hợp ngoài đoạn witness; K1/K4/K5 kiểm toàn tập, còn nghĩa instrumentation vẫn OPEN. C2 không gọi quan hệ phụ thuộc là quan hệ nhân quả.

## D5 và so nhãn riêng

`do-phu-theo-nhan.json#/rows` của dev-746fd74313 ghi 1.293 trace A và 949 trace mất cha, cả start/end split ở miền F và cha trong A. Tái lập số G2-H19. Không loại ca này khỏi graph/số ca; mồ côi chỉ là trạng thái quan sát.

Root không được gọi = không có cặp cha–con khác owner đi vào root trên F. Quá thưa = có cặp đi vào nhưng không cặp nào đủ 20 trước và 20 sau theo end của span cha (code T-032 call_slow_table_v1.py MIN_CALLS). Tái lập 8 không đi vào, 7 thưa, 37 đủ; `runs/bo-sung-001` lưu count mọi cặp trước ghép root. Không gán thiếu cạnh cho dataset/instrumentation chỉ từ một cờ, không dùng nhóm này chọn thiết kế.

## Tự kiểm và giới hạn

362 hash đầu vào cũ đạt trước chạy, theo manifest phù hợp ở `runs/buoc0-001/input-verification.json`. Pilot-001 giữ phần dừng hiệu năng; mọi graph hợp lệ khớp từng byte pilot-002. Không sửa p3/CIRCA/task cũ/FlashTicket, không tải/EC2/test/heldout. Kiểm file set, source hash và complete diff sau cùng ở runs/kiem-cuoi-001; manifest cuối không lấy hash mới làm xác minh đầu ra cũ.

Đã trả lời khả năng dựng/giữ cấu trúc, chưa xác nhận cơ chế hoặc lợi ích RCA. Node host, nghĩa vật lý cạnh, nguồn sinh metadata mức ngày, nguyên nhân vắng cạnh, quy trình đếm hai graph cũ trong K2 và trace FlashTicket thật còn OPEN theo báo cáo. Không tự đóng RQ3/P5/G3 hoặc chọn P6.
