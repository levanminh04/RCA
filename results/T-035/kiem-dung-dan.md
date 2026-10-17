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

## Kiểm bản v2 sau sửa hợp đồng messaging

Quyền và thiết kế: Q-154, WHY-52 bổ sung; runs/sua-n1-001/design.md. Oracle được ghi trước sửa code, bằng chứng thứ tự ở oracle-before-code.json; fixture_design.md giải thích từng phép phân xử. Kiểm đầu vào cũ theo manifest trước khi dùng: input-verification.json trong lượt sửa; bản manifest và graph cũ được giữ nguyên.

- 18 fixture cũ đạt ở seed0/1/2, kết quả byte giống nhau: fixture-cu-seed0-002 đến fixture-cu-seed2-002/result.json.
- 33 fixture mới đạt ở seed0/1/2: fixture-v2-seed0-002 đến fixture-v2-seed2-002/result.json. Kiểm exact cạnh, count, witness, metric address, diagnostic, phép chiếu API và phép chiếu độc lập ở cả hai mức. Các fixture giữ operation ổn định qua retry và qua hai queue cùng consumer.
- Ba ca consumer/producer thiếu toàn attributes/links đạt seed0/1/2: boundary-seed0-002 đến boundary-seed2-002/result.json. Oracle và bản trước nhánh sửa ở boundary-oracle-before-code.json, boundary-before/; lượt fail giữ ở boundary-before-001. Span loại CONSUMER vẫn được ghi unresolved và thiếu địa chỉ khi các cột tùy chọn đều null hoặc vắng.
- Code v1 chạy trên cùng oracle mới ở fixture-v1-001/result.json. Oracle còn kiểm schema v2 nên không dùng số fail làm số lỗi ngữ nghĩa riêng; đọc từng actual/expected. Không xóa lượt fail.
- Hồi quy đầy đủ: 52 ca/1045 khoảng, K1/K2/K4/K5 đạt; 1201 graph byte bằng bản cũ; mọi trường kết quả ca trừ chi phí máy bằng nhau. comparison.json lưu từng phép so. Node/vocabulary cũng được so; không chạy lại tính điểm RCA hoặc nguồn phụ mức ngày.

Các đường dẫn trên tính từ runs/sua-n1-001/. K3/K6/K8 và số phân nhóm cũ được giữ với bằng chứng cũ; không khai là đã thực nghiệm lại các phép ấy. Đầu ra đồ thị, stats/coverage/checks và input không đổi hỗ trợ dùng lại kết quả mô tả trong đúng phạm vi. Fixture là dữ liệu giả kiểm hợp đồng, không chứng minh instrumentation FlashTicket hay lợi ích RCA.

## Kiểm v2.1 sau sửa lỗi hợp đồng

- Trước sửa: toàn bộ 4.310 artifact của manifest v2 và 362 mục nguồn khớp; nguồn quyền/thiết kế và bản trước giữ ở runs/sua-hop-dong-001/ (preflight.json, input-verification.json, before/). Không lấy hash mới làm xác minh nguồn cũ.
- Oracle mới có 129 ca literal, đáp án viết trước builder, receipt oracle-before-code.json; thiết kế fixture_design.md. Nhóm: tên thiếu nhiều dtype, va chạm ID và project độc lập, biên thời gian/cộng/nhân int64/ns ưu tiên, kiểu mâu thuẫn và unknown hai thứ tự. Kiểm cả Prepared.graph/build và vocabulary/null khi cần, so đích literal, node/edge/count/witness và lỗi mong đợi.
- Sửa checker sau lượt đầu chỉ chuẩn hóa comparator JSON strict; bản gốc/đáp án và run fail giữ nguyên. AST hàm tạo fixture và digest inputs/expected trước code được kiểm không đổi ở oracle-revision-002.json. Phép đổi đích sai bị comparator từ chối; không đổi đáp án cho khớp builder.
- 129 ca mới đạt seed0/1/2 (fixture-oracle-seed0-001 đến seed2-001/result.json); 18 fixture gốc,33messaging,3ca thiếu attributes/links trước đạt cả ba seed. Command receipts ghi argv, seed, thời gian và exit code; dùng code đóng băng frozen-code.json.
- Hồi quy đủ 52 ca/1045 khoảng, K1/K2/K4/K5 đạt; 1201 graph byte bằng bản v2, mọi trường ca trừ chi phí máy khớp; comparison.json. Không phát lại baseline RCA, K3/K6/K8 hoặc nguồn phụ mức ngày; bằng chứng mô tả trước giữ trong đúng phạm vi.

Các đường trên tính từ runs/sua-hop-dong-001/. Việc fixture và hồi quy đạt không tự khẳng định mọi instrumentation thực tế, lợi ích RCA hoặc đủ căn cứ chọn P6. ID va chạm được từ chối là giới hạn tường minh, không coi là đã hỗ trợ hai miền trùng nhau. Gói sửa và prompt mới được trình để tự soát/phản biện/nghiệm thu; task chưa đóng.
