# Báo cáo tổng hợp P5b — T-040

- **Trạng thái:** đã sửa theo phản biện kết quả (REVIEW.md R1–R3, điểm tự tìm N1–N4) ngày 17/10/2026, theo lời Minh duyệt ở LOG Phiên 5. Phần Train Ticket dùng bản sửa R1 của người làm T-038. Gói sửa đó đã được kiểm lại chỉ đọc và dừng phản biện (Q-171; LOG T-038 Phiên 4; không có bản REVIEW mới). **T-038 chưa nghiệm thu**, nên mọi số TT là có điều kiện. Chờ Codex kiểm bản sửa; Minh nghiệm thu.
- **Lịch sử:** run 005 chặn phần TT phụ thuộc tập tĩnh vì R1 chưa xử lý (so sánh ở mục 5). Run 007 là bản trình phản biện; run 008 giữ nguyên mọi số của run 007, chỉ đổi trạng thái và thêm phần lần theo mới (`runs/tong-hop-008/so-sanh-007-008.json`). Run 009 chạy lại sau khi sửa luồng dừng của `tong_hop.py` (REVIEW R4 trong chat, LOG Phiên 6); mọi số trùng run 008 (`runs/tong-hop-009/so-sanh-008-009.json`). Run 010 chạy lại sau khi đưa kiểm B16, pin chung, mã chung và đồng bộ graph gốc T-038 vào điều kiện đạt đầu vào (R5, LOG Phiên 7); mọi số trùng run 009 (`runs/tong-hop-010/so-sanh-009-010.json`). Run 011 chỉ lập lại snapshot quyết định sau Q-174, Q-175, không đổi mã; mọi số trùng run 010 (`runs/tong-hop-011/so-sanh-010-011.json`).
- **Người làm:** Claude. **Người phản biện:** Codex.
- **Lượt tính hiện hành:** `runs/tong-hop-011/`. Mọi số dưới đây lấy từ `tong-hop.json` hoặc `dau-vao.json`; sổ đối chiếu số ↔ con trỏ JSON ở `so-lieu.json`, kiểm bằng `kiem_tra.py`.

**Phần này trả lời nhận xét nào.** DT18-NV2: mô hình nút/cạnh (gọi hàm, thông điệp, phụ thuộc dữ liệu) và nơi ánh xạ log, trace, metric. Bước 1 của cô: mô hình đồ thị phụ thuộc giữa các dịch vụ. MRP P5: dựng từ trace và từ kiến trúc, so hai nguồn để đo độ phủ, chỉ rõ phép tính P6 nào nhận cạnh. Báo cáo **không** trả lời đồ thị có giúp RCA không (RQ3) hay kết quả có giữ trên FlashTicket không (RQ5).

## 1. Đầu vào và trạng thái chấp nhận

Trạng thái lấy từ DECISIONS, REVIEW và LOG; manifest chỉ dùng để kiểm hash. Không coi tệp mới nhất là bản chính thức.

| Nguồn | Trạng thái | Cách T-040 dùng |
|---|---|---|
| T-034 (G2) | Cổng G2 đã duyệt (Q-149); task chờ nghiệm thu | Bản đồ hạn chế và ứng viên UV-1…UV-9; không coi là lựa chọn P6 |
| T-035 (graph trace) | Chưa nghiệm thu | Graph dev và thống kê mô tả; mọi đối chiếu TT/OB phụ thuộc trạng thái này |
| T-036 (hợp đồng) | Gốc đã đóng (Q-158); gói SMTP V2 (Q-164) chưa có phản biện chính thức | Hợp đồng và pin chung V2 |
| T-037 (FlashTicket) | Đã đóng (Q-167) | Mô hình thiết kế đích, chính thức trong phạm vi nguồn ghim |
| T-038 (Train Ticket) | Chưa nghiệm thu toàn task; gói sửa R1 đã được kiểm lại chỉ đọc và dừng phản biện (Q-171); semantics, binding, lineage, runtime OPEN | Cả hai phía dùng bản sửa, có điều kiện; không dùng run đề nghị sửa của reviewer |
| T-039 (Online Boutique) | Đã đóng (Q-165) với phần nguồn OPEN | Mô hình tham chiếu và 132 graph đối chiếu, có điều kiện revision |

Kiểm đầu vào (`dau-vao.json`): đã băm theo 9 manifest; 8 manifest khớp toàn bộ, gồm 11.009 tệp của T-038, 2.277 tệp của run sửa R1 và 5.667 tệp của T-035. Manifest gốc của T-036 (pin R1 lịch sử) lệch đúng ba tệp mã chung; cả ba thuộc thay đổi đã duyệt, và mã hiện hành khớp pin V2. Ba nhánh dùng cùng một pin V2 (`dau-vao.json#/pin_chung`). B16 của FlashTicket khớp registry T-037. Graph gốc `results/T-038/do-thi/` cùng byte với model của run sửa (`dau-vao.json#/tep_goc_TT_dong_bo_model_sua`). Run đề nghị sửa của reviewer T-038 **không** được dùng làm số. Các dòng DECISIONS nhắc T-038 được so với bản đã đọc (`runs/tong-hop-011/doc-quyet-dinh.json`); phép so chỉ cho biết nguồn quyết định có đổi không, không suy ra nghiệm thu (`dau-vao.json#/doi_chieu_quyet_dinh_T038`).

## 2. Ba hệ có cùng nghĩa biểu diễn không?

**Quan sát.** Ba nhánh cùng hợp đồng, cùng mã dựng/so và cùng schema. Ba trong bốn chiều bằng chứng giống nhau: biểu diễn được, runtime chưa kiểm, lợi ích RCA chưa kiểm. Chiều thứ tư (loại nguồn) khác nhau, xem dưới.

| Đại lượng mô hình tĩnh | FlashTicket | Train Ticket (bản sửa R1, T-038 chưa nghiệm thu) | Online Boutique |
|---|---:|---:|---:|
| Thực thể trong inventory | 32 | 110 | 23 |
| Bản ghi quan hệ | 115 | 513 | 82 |
| Cạnh mức thực thể | 72 | 170 | 22 |
| Thao tác | 65 | 993 | 68 |
| Thao tác chưa có tên runtime | 65 | 993 | 47 |
| Cạnh mức thao tác | 55 | 343 | 71 |
| Cạnh chiếu từ thao tác | 17 | 122 | 18 |
| Cạnh chỉ ở mức thực thể | 55 | 48 | 4 |
| Binding tài nguyên | 14 | 50 | 2 |
| Địa chỉ tín hiệu (dùng chung) | 153 (23) | 139 (139) | 53 (14) |

Nguồn: `tong-hop.json#/he_thong/<hệ>/mo_hinh_tinh/so_dem`. Số Train Ticket lấy từ bản sửa R1 (thêm bốn phụ thuộc cấu hình hạ tầng có nguồn); có điều kiện cho tới khi T-038 được nghiệm thu.

**Khác nhau không gộp được.**
- *Loại nguồn.* FlashTicket là thiết kế đích (B11–B16). Train Ticket và Online Boutique là mã nguồn tham chiếu; chưa nối được revision ứng dụng với dataset (`conditional_reference=true` ở mọi kết quả đối chiếu).
- *Loại cạnh.* FlashTicket có đủ các loại DT18 cùng cạnh triển khai: 11 cạnh gọi HTTP, 12 cạnh dữ liệu, 31 cạnh thông điệp (9 phát, 11 nhận, 11 logic), 17 cạnh triển khai và 1 cạnh SMTP gọi chưa phân kiểu. Online Boutique chỉ có gọi (14 RPC, 4 HTTP) và 4 cạnh dữ liệu; không có broker. Train Ticket có 132 cạnh gọi HTTP, 30 cạnh dữ liệu, 6 cạnh thông điệp (4 phát, 2 nhận), 1 cạnh SMTP và 1 cạnh HTTP chưa phân kiểu (webhook cảnh báo); không có cạnh triển khai.
- *Địa chỉ thông điệp.* Cả 31 cạnh thông điệp của FlashTicket thiếu `broker_scope`; 22 cạnh nhận/logic thiếu cả queue. Theo hợp đồng, các cạnh này sẽ bị loại khỏi phép so khi có trace. Đây là thiếu thông tin thiết kế, không phải lỗi bộ dựng.
- *Tín hiệu.* Mọi địa chỉ tín hiệu của Train Ticket là mức service dùng chung. FlashTicket có 130 địa chỉ gắn thao tác. Online Boutique có 22 (`tong-hop.json#/he_thong/<hệ>/mo_hinh_tinh/so_dem/signals_with_operation`).
- *Miền đối chiếu.* RE2-TT dùng toàn bảng span của ca dev và ảnh chụp 60/300 giây. Nezha-OB dùng cửa sổ adapter quanh mốc. FlashTicket chưa có trace.

**Kết luận được phép.** Gộp được ở mức “loại quan hệ nào biểu diễn được và giữ được nguồn”. Không cộng hay lấy trung bình tỷ lệ giữa ba hệ, vì nguồn, miền và trạng thái chấp nhận khác nhau.

## 3. Đối chiếu nguồn tĩnh với trace chứng minh được gì

Phép so có hai cách: *endpoints* chỉ so đầu mút; *typed* so thêm kiểu cạnh và bỏ kiểu unknown. T-040 tính lại mọi tập từ danh sách thành viên đã lưu, kiểm phân hoạch chỉ số cạnh gốc và lý do loại trừ, đối chiếu cạnh với graph đầu vào T-035: 0 lỗi trên 1.069 graph TT và 132 graph OB (`tong-hop.json#/he_thong/<hệ>/doi_chieu/loi_tinh_lai`).

### 3.1 Online Boutique (Nezha-OB dev, 132 graph)

- Mức thực thể, toàn miền: mọi 13 khóa trace đủ điều kiện đều có trong 22 khóa tĩnh. Không có cạnh chỉ có ở trace ở bất kỳ graph nào.
- Cửa sổ A có graph chỉ còn 11 khóa trace; N và toàn miền luôn 13.
- 9 khóa tĩnh vắng ở mọi graph thực thể. Phân loại ưu tiên đích bằng graph đã lưu: 6 cặp có đích không xuất hiện trong trace (DB, cache, tài nguyên ngoài; trong đó 3 cặp có cả hai đầu không xuất hiện: mysqld-exporter→mysql và hai cặp trình duyệt→CDN, exporter là đầu nguồn); 2 cặp có nguồn không xuất hiện (bộ tạo tải, trình duyệt); 1 cặp cả hai đầu đều quan sát được nhưng không có cạnh (checkout→currency). Ma trận hai đầu không ưu tiên: `tong-hop.json#/lan_theo/OB_static_only_every_full_graph/endpoint_matrix`.
- Mức thao tác: 10 khóa trace đủ điều kiện, đều có trong 71 khóa tĩnh. Phần lớn cạnh trace bị loại ở bước ánh xạ: 32 cặp vì nguồn chưa xác minh, 17 cặp vì đích chưa xác minh, 4 cặp vì đích chưa ánh xạ.
- Typed: T rỗng ở 22 graph mỗi họ, tức toàn bộ 132 graph. Kiểu trace đều unknown, nên **không đo được độ khớp kiểu**.

### 3.2 Train Ticket (RE2-TT dev, 1.069 graph)

Mọi số dưới dựa trên bản sửa R1 của người làm T-038; T-038 chưa nghiệm thu.

- *Phía trace.* Mức thực thể toàn ca: T có từ 16 đến 49 khóa; hợp qua 30 ca là 49 khóa. Đầu mút của mọi khóa T thuộc 24 service. 19 trong 739 ảnh chụp 60 giây có T rỗng; giữ null, không gọi là 0%. Hai tên trace không có ánh xạ: `ts-food-map-service`, `ts-ticketinfo-service`.
- Typed: T rỗng ở cả 979 graph thực thể và 90 graph thao tác.
- Mức thao tác: T rỗng ở 30 graph mỗi họ. Mọi cạnh trace thao tác đều bị loại ở bước ánh xạ (mơ hồ, chưa xác minh hoặc chưa ánh xạ). Vì vậy giao bằng 0 ở mức thao tác không phụ thuộc S.
- *Phía tĩnh.* Mức thực thể: S có 164 khóa endpoints và 162 khóa typed ở mọi graph. Phần riêng tĩnh toàn ca từ 120 đến 149 khóa; 120 khóa tĩnh vắng ở mọi graph thực thể. Theo nút trace đã ánh xạ (hợp qua 30 graph toàn ca): 13 khóa có cả hai đầu quan sát được, 23 chỉ nguồn, 54 chỉ đích, 30 không đầu nào (`tong-hop.json#/lan_theo/TT_static_only_every_full_graph/endpoint_matrix`). Nhóm hai đầu quan sát được lần theo ở mục 4.3. Từng graph và tỷ lệ phía tĩnh: `runs/tong-hop-011/rows-TT.json.gz`.
- *Giao.* Giao mức thực thể toàn ca từ 15 đến 44 khóa; 5 cặp chỉ có ở trace (food→station, seat→travel, seat→travel2, travel→order, travel2→order-other). Hai số này bằng đúng bản trước sửa R1 (mục 5): bốn quan hệ mới đều có ít nhất một đầu không thuộc 24 service của T.

## 4. Lần theo các nhóm chênh lệch quan trọng

### 4.1 Năm cặp chỉ có ở trace của Train Ticket — OPEN

- **Quan sát (FACT trên graph đã lưu).** Ở cả 5 cặp, span phía gọi chỉ mang tên method HTTP, span phía nhận mang route của service đích. 44 cặp khớp đối chứng có cùng dạng này. Route phía nhận của cả 5 cặp đều ánh xạ được vào handler trong mô hình tĩnh.
- **Kiểm phân xử và giới hạn.** Ở mức thao tác, handler phía nhận của 5 cặp không có bên gọi tĩnh nào. Nhưng 25 trong 44 cặp khớp cũng vậy: chỉ 19 cặp có bên gọi tĩnh (`tong-hop.json#/lan_theo/TT_trace_only_vs_intersection`). Dấu hiệu “handler không có bên gọi tĩnh” vì thế **không phân biệt** hai nhóm. Ở cả 25 cặp khớp đó, mô hình tĩnh có cạnh từ thao tác phía gọi tới service đích như một thành phần, chưa xác định handler. Tức là callsite đã được trích, chỉ chưa giải được URL tới handler. Ở 5 cặp chỉ có ở trace, mô hình tĩnh không có cạnh nào giữa hai service, ở cả hai mức.
- **Suy luận.** Cùng dạng span ở hai nhóm làm yếu giải thích “cấu trúc span riêng của nhóm chênh”, nhưng không loại nó. Điểm phân biệt duy nhất trên tập đã lưu là mô hình tĩnh không có callsite nào giữa hai service. Điều này nhất quán với cả “khác revision” lẫn “lời gọi gián tiếp không trích được”. Hai tên trace chưa ánh xạ khớp với metadata refactor T-038 đã ghi (xóa ticketinfo, tách food-map), hỗ trợ giải thích *khác revision*. Đây là ứng viên, chưa xác nhận.
- **Giải thích còn mở.** Khác revision; lời gọi động hoặc gián tiếp không trích được; bất nhất mã nguồn tham chiếu; instrumentation. Không quy cho collector.
- **Bằng chứng cần để phân xử.** Revision ứng dụng/image đã sinh RE2-TT, hoặc thuộc tính URL/callsite trong span. Dataset hiện không cung cấp; chủ dataset hoặc nguồn lineage mới có thể cung cấp. Quyết định phụ thuộc: P6 có dùng graph tĩnh TT làm cấu trúc cho dữ liệu RE2-TT không; nhánh “đồ thị tĩnh so với quan sát” ở P7.

### 4.2 checkout→currency của Online Boutique — ứng viên được củng cố, OPEN

- **Quan sát.** Trên 22 graph toàn miền (mỗi ca một graph), currency chỉ có bên gọi là frontend. Thao tác phía gọi `CurrencyService/Convert` của checkout trong mô hình tĩnh không xuất hiện trong trace, kể cả theo tên gốc hay ánh xạ. Trong khi đó checkout có span phía gọi cho 7 lời gọi RPC đi ra khác (`tong-hop.json#/lan_theo/OB_static_only_every_full_graph/rows/2`).
- **Đối chiếu nguồn.** T-039 G1 (đã đóng) đọc mã: lời gọi RPC của Convert dùng `context.TODO()` thay cho ngữ cảnh có span.
- **Suy luận.** Quan sát hỗ trợ ứng viên “ngữ cảnh không truyền nên lời gọi không nối vào trace của checkout”. Trong miền cửa sổ được giao, quan sát này **chống lại** giải thích “ánh xạ hoặc bộ đọc làm rơi cạnh”: không có span phía gọi nào để ánh xạ; bộ đọc của T-035 (`src/p3/nezha.py`, gọi từ `results/T-035/scripts/run.py`) chỉ bỏ span ngoài cửa sổ và dừng với lỗi khi gặp hàng không hợp lệ; span trùng được bộ dựng `src/do_thi/builder.py` gộp. Kết luận không áp ra ngoài miền được giao.
- **Chưa phân xử.** Lời gọi có chạy lúc thu dữ liệu không; span mới có bị lấy mẫu bỏ không; revision có khớp không. Cần đếm span `Convert` phía nhận không có cha trong cửa sổ dev, hoặc cấu hình sampler/instrumentation của bản đã chạy. Phép đếm này đọc span dev, nằm ngoài quyền T-040. Minh quyết hoãn, không mở nghiên cứu sâu nhóm này trong P5 (Q-175); OM-07 giữ OPEN.

### 4.3 Mười ba khóa tĩnh Train Ticket có hai đầu quan sát được nhưng không có cạnh — ứng viên, OPEN

Nguồn: `tong-hop.json#/lan_theo/TT_static_only_every_full_graph/rows`. Ở cả 13 cặp, hai đầu cùng có mặt ở 24 hoặc 30 trong 30 ca (mỗi ca một graph entity/full). Trong mỗi ca đó, hai đầu cùng có mặt ở 27–32 graph mức thực thể. Có 11 cặp mà thao tác nguồn tĩnh chỉ là candidate của mapping span chưa xác minh (span phía gọi chỉ mang tên method), nên **không** được gọi là span đã mất. Đồng xuất hiện trong cùng graph gộp không chứng minh các lời gọi thuộc cùng một request.

| Nhóm | Cặp | Quan sát trên dữ liệu và nguồn đã lưu | Ứng viên | Chưa phân xử |
|---|---|---|---|---|
| A | preserve, preserve-other, travel, travel2 → basic | Trong đúng các ca có cặp, cùng graph full có cạnh X→`ts-ticketinfo-service` và `ts-ticketinfo-service`→basic, đều bị loại ở bước ánh xạ vì nút chưa ánh xạ (`/rows/*/same_graph_paths_via_unmapped_trace_node`). Mô hình tĩnh v1.0.0 không có ticketinfo và có lời gọi X→basic trực tiếp | Khác revision: bản đã chạy còn ticketinfo làm trung gian | Lineage RE2→revision (OM-03); cùng request chưa kiểm |
| B | preserve, preserve-other → consign | Callsite nằm trong nhánh `consigneeName` khác rỗng (`ts-preserve-service/.../PreserveServiceImpl.java:218`, `ts-preserve-other-service/.../PreserveOtherServiceImpl.java:218`). Nhánh tùy chọn khác của cùng bên gọi có cạnh quan sát: assurance, food (`/rows/*/caller_observed_callees_in_same_cases`) | Workload không đặt consignee | Payload request không có trong dữ liệu |
| C | admin-travel → station, train, route; user → auth | admin-travel chỉ gọi ba đích này trong `checkTravelInfo`, thuộc đường add/update (`AdminTravelServiceImpl.java:90`, `:126`, `:187`); cạnh quan sát của bên gọi chỉ tới travel, travel2. user chỉ gọi auth trong `saveUser`, `deleteUser` (`UserServiceImpl.java:46`, `:66`, `:134`, `:139`); user không có cạnh gọi ra nào trong trace | Đường ghi không được chạy | Workload |
| D | admin-basic-info → contacts, station, train | Thao tác `getAll*` tương ứng cùng loại với các thao tác của bên gọi có cạnh quan sát (tới config, price) | Không giải thích được bằng tách đọc/ghi | OPEN: workload chọn lọc, revision hay trích nguồn |

Đường dẫn mã ở bảng tính từ `results/T-038/sources/train-ticket-v1.0.0/`. Nhóm A hỗ trợ giải thích khác revision cho cả các cặp chỉ có ở trace (mục 4.1), nhưng chưa xác nhận. Quyết định phụ thuộc: P6/P7 có dùng graph tĩnh TT làm cấu trúc cho RE2-TT không, và nếu dùng thì các cạnh nhóm A–D được xử lý thế nào (`con-mo.json` OM-13).

### 4.4 Các nhóm còn lại

- Phụ thuộc dữ liệu chỉ có phía tĩnh (OB: ad, productcatalog→MySQL; cart→Redis). DB/cache không là nút trong trace; span SQL thuộc owner ứng dụng (T-039 G2). Không thể so cạnh dữ liệu với dữ liệu hiện có. Yêu cầu tương ứng ở P9 (R-03).
- Bộ tạo tải, trình duyệt và exporter nằm ngoài miền trace. Vắng ở trace không là thiếu telemetry nội bộ.
- Khác biệt theo cửa sổ (OB cửa sổ A; TT ảnh chụp 60 giây) là hiệu ứng miền/cửa sổ đã xác nhận trên tập lưu. Nguyên nhân vật lý (nhánh không chạy, lấy mẫu) chưa phân xử.

## 5. Train Ticket sau bản sửa R1 của T-038

R1 (REVIEW T-038, CHẶN) chỉ ra bước lập bản ghi đã bỏ các phụ thuộc cấu hình hạ tầng có nguồn. Người làm T-038 đã đáp và tiếp nhận bản sửa; gói sửa đã được kiểm lại chỉ đọc và dừng phản biện (Q-171). T-040 dùng bản này với trạng thái “có điều kiện, T-038 chưa nghiệm thu” (`tong-hop.json#/he_thong/TT/doi_chieu/phu_thuoc_S`). Việc tính lại của T-040 trên 1.069 graph là kiểm số học, không thay phản biện chính thức của T-038.

So với bản trước (run 005, SMTP V2) (`runs/tong-hop-007/so-sanh-005-007.json`):
- Mọi graph thực thể: S tăng từ 160 lên 164 khóa endpoints, từ 159 lên 162 khóa typed; phần riêng tĩnh tăng tương ứng.
- Không đổi: T, giao, phần chỉ có ở trace, số graph T rỗng, toàn bộ mức thao tác, số lần theo ở mục 4, và mọi số của FT/OB.
- Mô hình: thêm 4 bản ghi quan hệ và 4 cạnh thực thể, đều chỉ ở mức thực thể (cạnh chiếu vẫn 122).

Kết quả khớp đúng delta người làm T-038 báo. Tệp chiếu gốc lệch phiên bản ở bản trước đã được T-038 đồng bộ.

## 6. Đồ thị tham gia phép tính nào trong P5

Trong P5, đồ thị được dùng để chuẩn hóa địa chỉ, chiếu thao tác lên thực thể, tạo khóa cạnh có hướng và tính giao/phần riêng. Chưa có phép tính điểm bất thường, vùng nghi ngờ hay xếp hạng. Các phép tính ứng viên cho P6 nằm ở `ban-giao-p6.md`.

## 7. Mục tiêu P5/RQ3/RQ5: đã bao phủ và còn thiếu

| Yêu cầu nguồn | Đã có | Còn thiếu | Quyết định phụ thuộc |
|---|---|---|---|
| P5 nút: service + thành phần | Tĩnh có DB, cache, broker, gateway, host, external ở FT; TT có DB, broker, gateway, external; OB có DB, cache, external | Trace dev chỉ có service; DB/cache không là nút quan sát | Tập ứng viên P6 |
| P5 cạnh có kiểu (DT18) | Tĩnh: FT đủ bốn loại; OB gọi + dữ liệu; TT gọi + dữ liệu + thông điệp (bản sửa, có điều kiện) | Trace dev chỉ có gọi chưa phân kiểu; typed N/A ở mọi graph | P6 không được coi cạnh trace là gọi đồng bộ đã xác nhận |
| P5 so hai nguồn, đo độ phủ | OB đầy đủ có điều kiện; TT đủ hai phía trên bản sửa R1 (T-038 chưa nghiệm thu); phần chỉ có ở mỗi phía được lần theo (mục 4) | Nghiệm thu T-038; lineage, workload; FT chưa có trace | Nhánh đồ thị tĩnh/quan sát ở P7 |
| P5 log/trace/metric ánh xạ lên đâu | Địa chỉ tín hiệu theo hợp đồng ở cả ba hệ | Chưa có giá trị tín hiệu FT; TT chỉ có mức service | Tín hiệu P6, yêu cầu P9 |
| P5 phép tính P6 nhận cạnh | Bảng ứng viên `ban-giao-p6.md` | Chưa chọn, chưa kiểm trên dev | SPEC P6 |
| RQ3 lợi ích đồ thị | Không thuộc T-040 | Toàn bộ | P6–P7, sau G3 |
| RQ5 áp dụng FlashTicket | Đề xuất yêu cầu quan sát `yeu-cau-quan-sat-p9.md` | Dữ liệu chạy thật, nhãn vùng | P9, P10 |

P5 **chưa hoàn tất**: T-035 chưa nghiệm thu, T-038 chưa nghiệm thu, gói V2 chưa phản biện chính thức. T-040 đủ tệp không có nghĩa P5 xong.

## 8. Đối chiếu tiêu chí xong của SPEC

| Tiêu chí | Trạng thái | Bằng chứng / phần thiếu |
|---|---|---|
| 1. Số truy được tới nguồn đã kiểm; không mâu thuẫn chưa xử lý | Đạt | `dau-vao.json`, `so-lieu.json`, kiểm K2–K5; mâu thuẫn TT (R1, tệp chiếu gốc) đã được T-038 xử lý; số TT có điều kiện |
| 2. Không trộn thiết kế, tham chiếu, quan sát, lợi ích | Đạt | Mục 1–3; `tong-hop.json#/luu_y` |
| 3. Chênh lệch quan trọng có giải thích hoặc OPEN cụ thể | Đạt sau sửa N2 | 4.1–4.3 lần theo cả phía chỉ có ở trace và phía chỉ có ở tĩnh, giữ OPEN kèm bằng chứng cần; cơ chế chưa xác nhận |
| 4. Bàn giao P6 nêu đầu vào, nút/cạnh, tín hiệu, phép tính | Đạt, chưa chốt cơ chế | `ban-giao-p6.md` |
| 5. Yêu cầu P9 có lý do → trường → vị trí → cách kiểm → quyết định | Đạt ở mức đề xuất | `yeu-cau-quan-sat-p9.md`; cách kiểm R-08, R-09 đã sửa theo REVIEW R1, R2 và N4; đã chuyển sang P9a làm bộ yêu cầu ban đầu (Q-175), chưa gửi nhóm hệ thống |
| 6. Nêu phần mục tiêu đã bao phủ và còn thiếu | Đạt | Mục 7 |
| 7. Lỗi T-038 chặn phần cốt lõi thì không báo hoàn thành toàn phạm vi | Không còn chặn | R1 đã được người làm T-038 sửa và gói sửa đã dừng phản biện (Q-171); phần TT có điều kiện tới khi T-038 được nghiệm thu |

Câu hỏi mở và nơi xử lý: `con-mo.json`.
