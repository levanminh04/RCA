# T-052 — T13 trên dev và hồ sơ G3 cho RCA chế độ (a)

- **Trạng thái:** đã duyệt ghi SPEC và hồ sơ ngày 04/11/2026 theo quyền có điều kiện của Minh, Q-245–Q-248. Thực nghiệm chưa được phép chạy.
- **Người làm:** Codex.
- **Người phản biện:** Claude.
- **Thuộc gói MRP:** P6, chuẩn bị P7. **Cổng:** chuẩn bị hồ sơ G3.
- **Nền:** Q-241/Q-242. Mọi thông số hiệu lực phải được ghim khi triển khai, không suy từ mặc định runner lịch sử.
- **Quyền hiện tại:** ghi hồ sơ và kiểm rẻ trong bộ nhớ. Phần code/pilot/chấm từ đầu ra cũ là kế hoạch triển khai cần quyền chạy riêng. G3/test/RE3 tiếp tục khóa.
- **Quyết định hiện hành:** [Q-245–Q-248](../../docs/DECISIONS.md). Các lựa chọn dưới đây triển khai đúng các dòng đó, không tự thay tiêu chí sau test. Q-249 duyệt phần chỉnh kế hoạch thực thi và hồ sơ.
- **Đính chính đường chạy:** Minh duyệt sửa tách C-d3 khỏi lượt xếp hạng chính và tính đường tốt nhất trên đồ thị con bất thường. Quyền này áp dụng cho gói sửa và kiểm tương đương, không cấp thêm quyền thực nghiệm hay dữ liệu.

## Mục tiêu

DT18 yêu cầu đồ thị phụ thuộc có log, trace, metric để phát hiện dấu hiệu bất thường, khoanh vùng và xếp hạng nguyên nhân, thực nghiệm công khai trước rồi áp dụng lên hệ bán vé. Cô yêu cầu hiểu sâu phương pháp cũ, mở rộng thực nghiệm, chỉ ra hạn chế, nghiên cứu đồ thị và so với baseline. T-052 là đánh giá mô tả trên dev và chuẩn bị khóa phép kiểm độc lập. Phần bao phủ gồm RQ3b, RQ3d và mô tả vùng nghi ngờ của RQ3c. Phát hiện hệ thống RQ3a và RCA(b) hoãn theo Q-245; độ đúng vùng ảnh hưởng, LLM và chuyển giao FlashTicket có đầu ra riêng ở P8–P10. G4 phải báo phần thiếu P/R/F1 của M1 trên dữ liệu công khai đợt chính.
Nguồn trực tiếp: [DT18 §2](../../docs/reference/sources/DT18-de-tai-va-nhiem-vu.md), [hướng dẫn cô §1 và xác nhận Minh §3](../../docs/reference/sources/advisor-2026-09-23.md), [MRP RQ3/P6/P7](../../docs/MRP.md), [kế hoạch T-052](../../docs/KE-HOACH-SAU-T047.md#t-052--t13-và-hồ-sơ-g3), [T-043 B4/B6 và đính chính](../T-043-thiet-ke-rca-m1/SPEC.md).

Task trả lời chất lượng thay đổi ở đâu khi bỏ từng thành phần, gói cuối cạnh tranh thế nào với baseline và quy tắc đơn giản, vùng rộng bao nhiêu, và bằng chứng nào đủ để khóa giao thức. Kết quả âm hoặc chưa phân xử là đầu ra hợp lệ. T13 không chọn lại nền theo mức hơn đối chứng. Nghiệm thu task không tự xác nhận lợi ích độc lập hoặc mở G3.

### Chuỗi bằng chứng và phụ thuộc

| Chặng | Đầu ra dùng lại | Điều kiện và phần còn thiếu |
|---|---|---|
| P1–P2, T-001–T-021 | Hồ sơ thuật toán, thẻ dữ liệu, G1 và phép chia theo ô; sáu baseline Q-62; vai trò TT/Nezha/RE3 | Đúng variant, schema, cửa sổ, tập ứng viên và mức tiếp xúc. Q-60 chấp nhận TX1 có khai báo, Q-63 chia Nezha theo ô, Q-64 cửa sổ, Q-74 chấm và universe. Không gọi toàn bộ test là chưa từng xem dữ liệu. |
| P3–P4, T-022–T-034 | Hạng T-024/T-026, detector T-025 lịch sử, bảng T-034, code và trung gian phân tích hạn chế | T-041 lần code và cả ca đúng/sai: tín hiệu có thể mất ở chọn tập, hướng thay đổi, thang điểm, gán owner hay hồi quy. Cờ caller đứng trên root không tự xác nhận lan. Chỉ dùng cơ chế có chuỗi đầu vào→xử lý→trung gian→đầu ra; giữ giải thích cạnh tranh. |
| T-041/T-042 | Đối chiếu giao thức, nguồn và cơ chế; kết quả Nezha-OB đã kiểm lại | Q-192 dừng điều tra lệch OB, giữ OPEN. M4 là baseline theo giao thức repo; hơn M4 chưa chứng minh hơn bản SimpleRCA đạt số tác giả. Một số nguồn detector cũ thiếu bản đúng hash; dừng riêng kết luận raw phụ thuộc. |
| P5, T-035–T-040 | Đồ thị trace, snapshot tĩnh, hợp đồng ánh xạ và R-01–R-10 | Graph gộp không giữ thời gian/membership từng request. Giữ span cấp request cho E1/E2. Snapshot chưa nối chắc với revision benchmark. Cạnh messaging/data cần đủ hai đầu quan sát, chuyển P9/P10. |
| T-043–T-047 | Thiết kế/đính chính, fixture, lượt dev đầu, sửa cổng/thang điểm và chạy lại K | T-044 kiểm đặc tả, chưa là hiệu quả thực. T-046 chưa hiệu chuẩn verdict. Giữ kết quả và lựa chọn theo thời điểm, không dùng nền cũ thay Q-242. |
| T-048/T-053→T-049→T-050→T-051 | z+S1 và K; K-b/T6; T9; T11/T12 và KB trên nền nối tiếp | Dev đã chọn lặp. KB đủ cặp bỏ E1/E2/E5. T-051 có kiểm native bổ sung và hai sai lệch lịch sử Q-242. Giữ cờ E2 và giới hạn C/VC khi E5 bật, chưa kiểm tương tác VC×E5. |

Đọc [T-041](../../results/T-041/bao-cao.md) và [bàn giao P5](../../results/T-040/ban-giao-p6.md) khi quy cơ chế. Không mở lại T-042 hoặc chạy thêm vì task cũ chưa giải mọi câu hỏi. Phép kiểm mới chỉ được đề xuất khi còn ảnh hưởng quyết định, với đúng trung gian và phạm vi cần thêm. Đóng task không xóa nghĩa vụ khoa học, cũng không tự cấp quyền cho phép kiểm ấy.

### Nền và vai trò tính toán của đồ thị

E1-U, E2-C, E5 bật; z+S1, E6a; epsilon 0,05, alpha 0,01; cổng phân vị G3 và cổng đếm D1 trong mã; cạnh quan sát. E3(a), E3b, E6b, E9 và hợp cạnh T12 tắt. Kênh log lỗi cơ bản còn. Cổng tính G3 trong mã khác cổng duyệt G3.

Nút là dịch vụ/thực thể quan sát. Cạnh gọi quan sát hướng caller→callee. Log/metric ánh xạ về thực thể, trace giữ span cha–con và thời gian. E1 trừ hợp khoảng con quan sát khỏi span cha; đó là phần thời gian chưa được con phủ, không được gọi là CPU time. E2 dùng quan hệ span để gán bằng chứng ngoài span bọc về callee. E5 dùng lớp kênh và cạnh để tách bằng chứng có thể kế thừa. E6a xếp theo tầng/khóa đã tính, E7 dùng đường đi/liên thông. E8 cần quan sát ở FT. [T-043 B2/B3](../T-043-thiet-ke-rca-m1/SPEC.md), [WHY-72–75](../../docs/WHY.md).

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Phép phân xử và nguồn | Cách đọc và phần phụ thuộc |
|---|---|---|
| Bỏ E1/E2/E5 làm đổi chất lượng thế nào? | Cặp cùng cửa sổ/cấu hình từ KB, RR và dấu vết kênh/tầng/hạng | Báo theo dataset/loại lỗi/vị trí/ô/ca. Bỏ E1 hại TT và OB giữ nguyên; bỏ E2/E5 cho hướng khác giữa hai bộ. Mục tiêu bỏ mô-đun làm chất lượng giảm chưa được hỗ trợ chung trên dev. P7 mới kiểm ngoài dev. |
| Quan hệ có giúp hơn nhánh bỏ quan hệ và quy tắc đơn giản? | C-a0/a1, C-d1/d2/d3; R0-z cho QT7; C-c/C-g theo hợp đồng | D23 là ablation chuỗi đã chọn. C-a1 giữ E1, C-d2 giữ bằng chứng E1/E2. C-g chỉ đo thêm E6b sau SimpleRCA. Không có đối chứng graph ngẫu nhiên, giới hạn kết luận tương ứng. |
| C-e có ưu tiên lặp một dịch vụ? | Phân bố xác suất hạng 1, cỡ tập trả về, V0/N1; RR nhãn root thật ghép sau riêng | Cửa sổ trước tiêm chưa có nhãn lành độc lập. Root thật dùng đối chiếu, không là root vật lý ở mốc giả. Không đồng nhất MRR gần chance với không có thiên lệch. |
| Vùng có chứa root và rộng bao nhiêu? | Hai cách E7 tại P, kỳ vọng theo hòa, tỷ lệ trên O, vùng hợp riêng, cặp T12 | Mô tả vùng nghi ngờ. P/R/F1 vùng ảnh hưởng cần nhãn độc lập P10. |
| Đủ khóa G3(a) chưa? | Bảng căn cứ từng thành phần, B6/A4, tập ca/mã mờ/nhãn/U, máy/quyền và bảng diễn giải | Hồ sơ có thể hoàn tất ở trạng thái sẵn sàng trình hoặc ghi đúng mục còn chặn. Đủ file không thay việc kiểm hành vi dev. |

## Đầu vào

Revision trước ghi hồ sơ ở manifest T-052. Trước dùng kết quả kiểm manifest phù hợp từng lượt; báo và dừng vế phụ thuộc khi thiếu hoặc lệch hash. Giữ kết quả nặng local theo Q-244. Manifest hồ sơ không chứng nhận lại mọi file của manifest upstream.

- T-043 SPEC, đặc tả/hợp đồng/ma trận và đính chính phiên 9, 10; T-044 đính chính cài đặt; src/m1 và src/m1_danh_gia; src/p3 và code baseline đúng revision được ghim.
- [T-034 bảng baseline](../../results/T-034/bang-baseline.json) và runs/manifest-cuoi-007/manifest.json; T-024/cham-a.json; T-026/cham-a.json, cấu hình M4.
- T-053/chi-so-day-du.json, runs/k-cham-001/kq.json và native/trung gian nén theo manifest T-053. T-048/t4b.json cho đối chiếu thang điểm.
- T-051/kb-002/{ban-ghi.jsonl,ce.json,sources.json,seal.json} và score/{metrics.json,scores.json}; T-051/t12-001/{plan.json,*.json,score/regions-controls.json}; manifest.json và manifest-dap-phan-bien-001/002.
- T-050/doi-chung-003.json, cham-002/cham.json, manifest-chay-lai-002.json cho C-c/C-g; gói kiểm native và đính chính.
- Nguồn G1 có sẵn ngoài locked: T-021/chia-theo-o/A-phan-tang.csv, goi-g1.md, tiep-xuc.csv, vi-tri-root.csv, scripts/chia.py và vi_tri.py; Q-60/63/64/74. Không đổi phép chia hoặc dùng kết quả test để đổi ca.
- LOG T-047–T-051/T-053, các preflight/pilot/receipt được dẫn trong mục chi phí.
- Metadata RE3 trong T-002 và giới hạn MRP §4. Chưa đọc telemetry giữ ngoài hoặc nội dung data/locked.

Bảng MRR dev tại P, dùng con trỏ T-051/metrics: /<config>/<dataset>/P/MRR; K-R0 tại T-053/chi-so-day-du: /K-R0/tong_hop/that/dataset; C-d2 tại regions-controls: /<dataset>/summary/off/controls/C-d2; baseline tại T-034: /ranking_mode_a/<cohort>/methods.

| Vế | TT, 30 ca | OB, 22 ca |
|---|---:|---:|
| M1 cuối | 0,927778 | 0,872727 |
| Bỏ E1 | 0,858120 | 0,872727 |
| Bỏ E2 | 0,966667 | 0,720561 |
| Bỏ E5 | 0,944444 | 0,806061 |
| K-R0 z+S1 | 0,983333 | 0,661883 |
| C-d2 | 0,916667 | 0,899242 |
| TORAI B ở TT / SimpleRCA M4 ở OB | 0,916667 | 0,537542 |

M1−K-R0 TT có 1 tăng/4 giảm/25 hòa, OB 9/2/11. M1−TORAI B TT có 4/3/23. Thang E4+S1→z+S1 trên R0 tăng MRR gộp dev khoảng 0,166; thêm E1/E2/E5 trên z tăng khoảng 0,057. Đây là các can thiệp cụ thể, không cộng thành đóng góp nhân quả chung. Chênh TORAI B−SimpleRCA TT dev khoảng 0,02556 là tham khảo, chưa lập biên M1/M2 mới. Nguồn theo ca ở T-053/kq.json, T-051/scores.json, T-024/cham-a.json; mọi số mới phải lưu phép tính và con trỏ.

### Nguồn tái dùng và phạm vi trường

| Vế | Nguồn và cấu hình | Ca/cửa sổ và world | Trường dùng lại và phần cần kiểm |
|---|---|---|---|
| M1, bỏ E1, bỏ E2, bỏ E5 | T-051/kb-002: K-E1+E2+E5, K-E2+E5, K-E1+E5, K-E1+E2 | 52 thật, 30 TT giả cho vế C-e được hỗ trợ. Hạng ở P/S_lo/S_hi | Giữ blocks, khóa hòa, trạng thái, tầng P và trường chấm theo ca đã có. Đối chiếu seal KB và native K T-053 theo ca/cấu hình. KB gọn thiếu O, coverage và vùng. |
| C-a0/C-a1 | Native K-R0/K-E1 của T-053 theo cùng nền hiệu lực | 52 thật và cửa sổ TT giả theo hợp đồng cặp. Hạng ở P/S_lo/S_hi | Ứng viên chiếu hạng với E7 tắt theo hợp đồng C-a. Cần pilot native trước ghép nhãn. So đầu vào, cờ, tập, tầng, khóa, hòa/hạng, verdict và trạng thái. Kiểm riêng đường lỗi và khác biệt chủ ý ở vùng. |
| Sáu baseline | T-024/cham-a.json, T-026/cham-a.json, T-034/bang-baseline.json | 30 TT + 22 OB thật. Một kết quả theo giao thức baseline, ghép với mỗi world của M1 khi báo độ nhạy | Dùng độ đo từng ca/seed đã hợp lệ. Ghim variant, cửa sổ, U/alias, quy tắc hòa và lỗi. Giữ CIRCA/TORAI B OB UNSUPPORTED trong mẫu số. |
| C-c/C-g | T-050/doi-chung-003.json và cham-002/cham.json theo manifest chạy lại | 52 thật theo phiếu baseline và graph nền | Dùng phiếu/blocks, trạng thái và điểm theo ca. Đối chiếu cửa sổ, graph và cấu hình cuối. C-g chỉ đo phần E6b thêm sau SimpleRCA. |
| C-d1/2/3, vùng E7 và cặp T12 | T-051/t12-001, off/on đúng nền. T-053 native cuối bổ sung O/coverage | 52 thật. C-d và vùng tính tại P. Các trường hạng T12 theo world nào có thì ghi rõ world đó | Dùng blocks, trạng thái, hai cách vùng, vùng hợp, F_I và graph. Tính tỷ lệ theo O từng ca. Giữ C-d3 OB suy biến theo Đ12. |
| C-e nền cuối | T-051/kb-002/ce.json và native T-053 đúng cửa sổ giả | 30 TT giả. Phân bố hạng đầu, V0, N1 tại P theo hợp đồng | Lấy blocks và verdict từ bản ghi đã seal. Bổ sung O/coverage từ native. Ghép root tương lai ở evaluator. |
| CI, bảng nhóm và truy vết | Độ đo theo ca đã ghép sau seal, frame và trace từ lượt nguồn | Cặp đúng ca/ô và world có hợp đồng | Tính CI và bảng còn thiếu từ độ đo gọn. Dùng cùng mẫu bootstrap cho cặp/world, đọc frame và trace chọn lọc theo nhóm và ca đối chiếu. |

Chỉ tính lại trường chưa có hoặc chưa chứng minh dùng được. Giữ con trỏ tới số đã có và định nghĩa mẫu số. Một dòng chỉ có P ghi đúng phạm vi P, kể cả khi dùng để so với M1 có ba world.

## Đầu ra

| File/nhóm trong results/T-052 | Nội dung |
|---|---|
| manifest.json | Gói hồ sơ và nguồn đã kiểm ở lượt ghi; nối lớp manifest thực thi riêng khi có quyền. |
| ma-tran-va-nguon.json | Cấu hình hiệu lực, code/env, cửa sổ, U/O, trường tái dùng, điều kiện tương đương, nguồn/ca còn thiếu. |
| ket-qua-dev.json | Sáu baseline, M1, ablation, đối chứng, C-e, vùng; theo dataset/loại lỗi/vị trí/ô/ca, ghi world áp dụng theo bảng nguồn; CI/seed/mẫu số/trạng thái. |
| bao-cao-t13.md | Câu hỏi nguồn, cơ chế và phản ví dụ, giới hạn dữ liệu/adapter/giao thức/phương pháp, tác động tới kết luận P7 và FlashTicket. |
| ho-so-g3.md | B6, sáu câu MRP §7; bảng mục đích/loại căn cứ/phương án/dev/điều kiện thất bại cho từng thành phần, cả thành phần tắt; mức tiếp xúc; mục đã đủ/chưa đủ khóa. |
| giao-thuc-p7-a.json | Ma trận, thống kê, diễn giải, cách phân loại lỗi trước chấm, fallback, cổng nhãn, máy/quyền; khóa sau kiểm dev và Minh duyệt G3. |
| scripts/, runs/ | Công cụ chỉ trong task, fixture/pilot/receipt/tiến độ và mọi lượt hỏng khi được quyền chạy. |
| ke-hoach-tap-test.json | Hash phép chia G1, quy tắc tạo mã mờ, tập ca và U/alias, điểm vào P7 của M1 và các baseline, kết quả fixture bộ đọc/ghép nhãn và dữ kiện chỉ được materialize sau quyền test. |

Lượt ghi hiện tại chỉ tạo SPEC/LOG, lớp manifest hồ sơ và các đoạn sổ đã duyệt. Các đầu ra nghiên cứu còn lại là nghĩa vụ triển khai.

## Phạm vi ghi

Theo Q-248: task này có SPEC/LOG tại tasks/T-052-t13-va-ho-so-g3/ và đúng dòng T-052 STATE. Khi quyền triển khai được cấp, đầu ra nằm trong results/T-052/. Wrapper/công cụ mới đặt trong scripts/ của task. Nếu cần sửa src hoặc thay hợp đồng khoa học, trình Minh phạm vi và tác động trước khi sửa.

Gói ghi sổ Q-245–Q-248/WHY và đồng bộ C-15 B đã được duyệt có điều kiện riêng, không là quyền sửa rộng các hồ sơ cũ. Các bản phản biện của Claude vẫn là nguồn chat; không tạo REVIEW.md đứng tên Claude. Quyền chạy dev/test/khởi động máy/commit/push cấp riêng. Reviewer chỉ ghi bản phản biện mà Minh cho phép.

## Các bước

1. **Kiểm và ghim nguồn.** Kiểm hash/byte/json/schema, xác định đúng bản đính chính. Liệt kê field/case cấu hình đủ dùng. Giữ bảng baseline và B6 độc lập song song với pilot. Đọc nguồn nặng theo cửa sổ, ưu tiên một lượt trích các trường cùng dùng. Giữ bản ghi gọn cho chấm và CI. Chỉ đọc trace chi tiết cho ca cần truy vết.
2. **Dựng cấu hình và pilot không ghép nhãn.** Ghim nhanh_z=True và che_do={cong_phan_vi:G3,cong_dem:D1,thang:E4+T4c}; dấu vân tay gồm che_do. Runner T13 cũ mặc định nhanh_z=False và không tự đặt chế độ. Pilot cần TT thật, TT giả, OB, ca nặng, ca thực đổi nhánh và ca không đổi. So hash đầu vào, cờ, tập, tầng, khóa, hòa/hạng/verdict; E7 tắt là khác biệt chủ ý C-a.
3. **T13 từ nguồn đủ.** M1 và ba vế bỏ dùng KB. C-a0/a1 ứng viên chiếu hạng từ K-R0/K-E1 sau chứng minh bằng mã và parity native. Thất bại thì khoanh đúng miền sai, dự toán tính native bổ sung và xin quyền nếu vượt trần. Không gọi replay tự khớp là native parity.
4. **Baseline/đối chứng/vùng.** Xử lý lỗi dữ liệu và lỗi thực thi theo mục Kiểm đúng đắn trước khi seal bản ghi để chấm. Chỉ ghép nhãn sau seal. Bảng đủ Q-62; giữ trạng thái CIRCA/TORAI B OB UNSUPPORTED 22/22 trong nguồn. Đối chiếu C-c/C-g với phiếu và graph cuối. C-d1/2/3 từ vế off T12; lấy blocks/native cho độ đo thiếu. TT C-d3 4 OK, 6 NO_EVIDENCE, 20 UNSUPPORTED_CYCLIC, RR=0/30; giữ bảng mô tả và trạng thái, OB suy biến thiếu đích Đ12. T12 dùng cả off/on: trên dev đổi F_I ở 17 TT+2 OB, nhóm hạng 11 ca, RR root giữ 52/52. Chỉ gọi hiệu ứng thêm hai snapshot cụ thể theo D8.

   **Các lượt mới T-052/P7:** đặt `params.tach_cd3=True` khi gọi `chuoi.chay` cho M1 và C-a0/a1. Đóng dấu hạng chính trước mọi lượt C-d3. Chỉ khởi chạy C-d3 cho vế và dataset đã khai, với `extra.canh`, `extra.dau_vao_cd3.dich` và `diem` khôi phục từ cặp tử/mẫu bằng `Fraction`. `so_span_goc_A` đi cùng biên nhận. Điều phối C-d3 riêng với giới hạn thời gian ghi trước lượt chạy và biên nhận trạng thái/lỗi riêng. Lỗi hoặc quá giờ C-d3 không đổi hạng hay trạng thái đã đóng dấu của M1/C-a. B2 vẫn tính trượt cho trạng thái C-d3 được quy định, giữ trạng thái gốc trong bảng. Phần tái dùng đã ghim giữ provenance của lượt gốc.
5. **C-e và vùng.** Làm đầy đủ mục riêng dưới đây. Lấy O trực tiếp native đúng cấu hình cuối T-053, so sidecar nếu dùng. Tại P hai cách vùng TT chứa root kỳ vọng 86,67%/96,67%, rộng 2,9/10,7; OB 81,82%/95,45%, rộng 1,59/2,91. Tỷ lệ theo O tương ứng 4,26%/15,74% và 15,91%/29,09%. Tính theo ca trước tổng hợp, báo O=0 N/A, vùng hợp riêng.
6. **Lần cơ chế và phản ví dụ.** Tạo ΔRR toàn ca, đọc cả ca đúng cùng điều kiện với nhóm TT hại, OB giúp, C-d2 thắng, và vùng đổi. Trích đầu vào→E1/E2→E5→tập/khóa→hạng. Tách quan sát khỏi suy luận. Thiếu trung gian thì ghi phần cần bổ sung, chi phí và kết luận phụ thuộc, không ép một cơ chế để đóng bảng.
7. **Khóa công cụ thống kê và hồ sơ P7.** Theo mục A4, tập ca test và máy bên dưới. Kiểm thống kê trên dữ liệu giả/dev, ghi lệnh/seed/phân vị/code. Ghim điểm vào P7 trên máy local cho M1 và các baseline, chạy fixture qua bộ chọn và bộ đọc/cắt trước khi trình G3. Viết bảng diễn giải trước test. Bảng căn cứ từng thành phần gồm lý do P4/DT18/kỹ thuật, phương án khác, bằng chứng và thất bại. E9/T12 cuối nối WHY-76, không dùng WHY nền đầu như đủ lý do hậu kiểm.
8. **Tự kiểm và bàn giao.** So bảng với nguồn, kiểm chỉ số/hòa/mẫu số/trạng thái, con trỏ/link/manifest và toàn diff. Hồ sơ báo đủ/chặn đúng phần nguồn. Minh chuyển Claude soát kết quả, sau đó quyết nghiệm thu/G3/quyền P7.

### C-e và vùng

C-e dev 30 cửa sổ TT, t′=t−300, giao thức cần lịch sử tới t−600. Kiểm hỗ trợ theo đúng hợp đồng từng nguồn/A0, không suy thiếu dữ liệu là không báo. Tách số cửa sổ khai, trạng thái ERROR/UNSUPPORTED/INSUFFICIENT_EVIDENCE và số cặp hợp lệ riêng của luật C. Độ đo hạng chính giữ mẫu số đã khai theo quy tắc lỗi, thêm bảng miền có đầu ra nếu cần.

Báo xác suất hạng 1 theo quy tắc hòa của bộ chấm, phân bố từng thực thể đứng đầu, top mass, nhóm hòa, số thực thể được trả/O/U, root đối chiếu có mặt/vắng. Giữ V0/N1 riêng. Ghép root thật chỉ ở evaluator sau seal; ghi rõ root là nhãn của ca thật sau mốc giả. Chance H_n/n áp khi root đối chiếu có mặt trong tập n được chọn cho mốc ngẫu nhiên; n=U và n=tập trả về là hai mốc phải gọi đúng tên.

Nguồn T-051/kb-002/ce.json ở nền cuối: 68 thực thể/cửa sổ, 0 hòa đầu, 16 thực thể khác nhau từng đứng đầu, hai thực thể mỗi 5/30 (top hai 10/30); MRR root đối chiếu 0,0787266, chance H68/68=0,0706479; Hit@1=0/30; V0 CAUSE_FOUND=30/30, N1 trung bình 14,7. Không có một thực thể đứng đầu mọi cửa sổ, vẫn có tập trung mô tả. Chưa loại thiên lệch và chưa xác nhận nền khỏe. Nguồn số ở ce.json, T-053/chi-so-day-du.json#/K-E1+E2+E5/tong_hop/ce và nhan-dev ghép sau.

Trong hồ sơ P7 xin C-e mô tả chỉ cho M1 cuối trên tối đa 60 ca TT test, cùng máy/cặp thật–giả, chốt trạng thái thiếu lịch sử trước mở. Ngân sách gồm cả 60 cửa sổ thêm và nhận/kiểm/chấm. C-e ngoài A4, không dùng để chọn cấu hình/hiệu chuẩn trên test. OB không có C-e tương đương theo D6. Nếu sau preflight dự báo vượt ngân sách, trình phạm vi thiếu và hệ quả thay vì âm thầm bỏ.

### Tập ca, nhãn, vị trí và mức tiếp xúc trước G3

**Thành viên tập đã có ở G1.** Khóa hash A-phan-tang.csv và các nguồn chia-004, 60 TT/20 ô và 34 OB/20 ô, disjoint với dev theo ô. Chưa có allowlist test runtime đã kiểm tương đương dev. T-052 khóa cơ chế tạo và điểm vào P7 trên dữ liệu giả, không đọc locked để tạo allowlist thật. Ghim revision, thành viên, quy tắc đọc/cắt và luật lỗi trước khi trình khóa G3.

**Đường chạy P7.** Dùng điểm vào riêng trên máy local cho RE2-TT và Nezha-OB, đi từ bộ chọn đúng thành viên G1 tới bộ đọc/cắt của M1 và các baseline theo giao thức đã ghim. Bộ chọn dev vẫn chỉ phục vụ dev. Bên quản lý dữ liệu chỉ đọc danh mục/census được phép để tạo mã mờ ổn định và kiểm không trùng. Bảng riêng ánh xạ đường dẫn và nhãn được tách khỏi bản ghi phương pháp. Sau quyền test, verifier materialize hash/byte file và allowlist adapter, kiểm khớp thành viên đã khóa, báo lệch và dừng nếu không khớp. Runner đọc allowlist/path và mốc (a); phương pháp chỉ nhận dữ liệu đã chuẩn hóa, inventory/alias/tham số phi nhãn. Mã mờ, root, fault, cell, path hoặc chuỗi suy từ chúng không vào API khoa học. Không in đường dẫn mang nhãn trong stdout/bản ghi phương pháp, kể cả ngoại lệ; chẩn đoán đường dẫn giữ phía quản lý dữ liệu. Dùng kiểm trường cấm đệ quy và fixture đổi tên/nhãn để kiểm firewall; kiểm chuỗi đơn lẻ không chứng minh không có label-derived feature.

Trước khi trình G3, dùng fixture giả đi qua đúng điểm vào P7 của M1 và các baseline để kiểm từ chối ca ngoài tập, thiếu quyền và đường dẫn thoát phạm vi; kiểm cửa sổ, U/alias, lỗi bộ đọc và việc tách định danh/nhãn khỏi đầu ra. Fixture xác nhận luồng, không xác nhận dữ liệu test thật đã sẵn sàng. Nếu thiếu đường chạy hoặc cần sửa `src` ngoài quyền, hồ sơ ghi mục khóa G3 đang bị chặn và trình phạm vi còn thiếu.

Đầu ra phương pháp được seal trước evaluator đọc root/fault/cell. Mốc tiêm (a) là ngoại lệ đầu vào đã duyệt Q-66. Tập đánh giá TT giữ U=68 Q-74/WHY-26, OB theo inventory/alias 10 thực thể hiện hành và luật kênh/hỗ trợ của adapter; kiểm tên lạ/ngoài U rồi báo theo hợp đồng, không đổi U từ root test hoặc bỏ ca. Lưu inventory, modeled/observed/scored/returned và coverage riêng. Chốt nơi private map/nhãn trong SPEC P7 trước tạo thật; quyền mở chỉ cho lớp quản lý dữ liệu, adapter và evaluator theo việc của nó, không mặc nhiên cho người phân tích mở toàn file Nezha.

Báo theo dataset, loại lỗi, vị trí root, ô và ca. Theo Q-60(b), vị trí trên graph service có hướng từ trace N: không có trong trace; bậc 0; nguồn (in=0,out>0); lá (in>0,out=0); giữa/hub (in>0,out>0), hub nếu tổng bậc ≥ phân vị 75 của mọi service trong graph, phân vị 90 báo độ nhạy theo script vi_tri.py. Root ghép ở evaluator. Không có đủ bậc toàn graph thì giữa/hub OPEN. Lưu nhóm test TT cũ suy theo root ở cột lịch sử và kiểm lại N khi được quyền; không chuyển nhóm theo A hoặc theo kết quả hạng. Khóa cửa sổ N/bộ dựng service/alias trước G3 và thử dev để bảo đảm cùng ngữ nghĩa Q-60. Vị trí thiếu quan sát không bị diễn giải thành cô lập vật lý.

Ứng viên trên dev: dựng nút từ các đơn vị thao tác có n_N > 0 trong native K-R0 của T-053. R0 giữ span bọc. Lấy cạnh caller → callee từ extra.G_N cùng cửa sổ N. Kiểm trong bộ nhớ trên 52 ca dev đã thấy mọi đầu cạnh nằm trong tập nút dựng được. Việc triển khai còn phải đối chiếu quy tắc giữ span, cửa sổ N, alias và tập nút dùng cho p75/p90. Kiểm nút bậc 0, nút vắng trace và span bọc. Khi thiếu thông tin để phân biệt nút vắng với nút cô lập, hoặc thiếu bậc toàn đồ thị, báo đúng phần vị trí chưa xác định và giới hạn kết luận theo nhóm. Giữ nhãn Nezha từ cửa sổ quanh mốc tiêm và nhóm ô TT ở cột lịch sử. Vị trí chính chỉ dùng nhóm từng ca dựng từ N theo hợp đồng đã kiểm.

Mục tiếp xúc khai Q-60/T-021: TX1 đã xem thống kê/triệu chứng có gắn root, chưa có kết quả phương pháp, được Minh chấp nhận có khai báo; TX2 không vào test. Nezha có ca liền kề hai phía, giữ bộ đọc cắt đúng ca và giới hạn thời gian/nguồn, không mở file rộng cho phân tích. RE3 TX0 là vắng bằng chứng tiếp xúc, chưa chứng nhận chưa ai mở; cùng hệ OB với Nezha và cùng công cụ RCAEval với TT, chỉ kiểm tổ hợp chưa thấy ở dev, không tách hiệu ứng hệ khỏi công cụ. “Đã xem” và “đã dùng để thiết kế” phải ghi riêng trong sổ. (b) thiết kế sau khi xem cùng tập chỉ báo thăm dò, kiểm độc lập dùng dữ liệu phù hợp chưa dùng sau khóa. [Q-60/Q-63](../../docs/DECISIONS.md), [T-021 §4–5](../../results/T-021/goi-g1.md), [MRP sáu câu G3](../../docs/MRP.md#7-cổng).

### A4 và bảng diễn giải khóa trước test

1. **Estimand.** TT: trung bình theo 60 ca của RR_M1−RR_TORAI-B; TORAI trung bình ba seed trong từng ca trước tổng hợp. Biên Δ=0,05. OB: Hit@5 kỳ vọng M1−SimpleRCA M4, trọng số theo ca. Không gộp dataset hay xem ba thế giới/seed như mẫu độc lập.
2. **Bootstrap.** Dùng src/p3/danh_gia.bootstrap theo WHY-28, B=10.000, seed=20261005, np.random.default_rng và thứ tự ca/ô của hàm được ghim. Lấy lại nguyên ô có hoàn lại, mang mọi ca; cặp dùng cùng mẫu. CI phân vị hai phía 95%; lưu phiên bản numpy/phương pháp phân vị. Wrapper kiểm đủ trường mà hàm cần, chiều cặp M1−baseline, và cùng mẫu cho P/S_lo/S_hi. Kiểm với ô khác cỡ, hòa, lỗi và Rerank N/A.
3. **E-04.** H0_TT: trung bình chênh ≤−0,05. Giữ cách đọc M-44/M-45: lo>−0,05 thì đạt theo công thức, bằng biên không đạt. Lưu CI thô và giá trị làm tròn 12 chữ số thập phân bằng Decimal ROUND_HALF_EVEN; so strict trên giá trị đã làm tròn, giữ point estimate/RR đầy đủ. Ví dụ 0,9−0,95 và 0,85−0,9 cùng được nhận là bằng biên. Chỉ dùng độ chính xác này cho quyết định/CI, không làm lại hạng phương pháp.
4. **Ít ô/suy biến.** Luôn báo tổng ô, số ô có ít nhất một chênh ca khác 0, số ô có tổng chênh khác 0, số ô tổng âm, số ô lẫn chiều, số ca hai bên cùng trượt và trạng thái. Đếm bằng RR hữu tỉ đã lưu khi có; ngưỡng số học 12 chữ số chỉ áp dữ liệu float thiếu biểu diễn hữu tỉ. Mọi CI kèm cảnh báo ít ô/rời rạc và nguy cơ undercoverage. lo=hi ở độ chính xác đã khai là suy biến. Nếu vẫn qua biên, câu đầy đủ là “đạt E-04 theo công thức; CI suy biến”, cùng các số đếm và giới hạn chưa bảo đảm mức sai số danh nghĩa. Không tự đặt số ô tối thiểu để đổi tiêu chí sau test. lo<hi cũng chưa bảo đảm bootstrap được hiệu chuẩn.
5. **OB.** H0 để đảo dấu là phân bố vector tổng chênh từng ô bất biến dưới đổi dấu nguyên ô (KS-08); thống kê là tổng chênh chia tổng ca, hướng M1 cao hơn. Liệt kê 2^G dấu, tính cả dấu bằng thống kê quan sát, lưu tử/mẫu p. Tổng 0 giữ và báo số ô hữu hiệu. Phép tính p được liệt kê chính xác; hiệu lực kiểm định phụ thuộc giả thuyết hoán đổi, không suy giả thuyết trung bình≤0 tự đủ điều kiện. Kết luận chỉ có điều kiện này.
6. **Chuyển mức một chiều.** Ngưỡng OB là 0,025. Nâng lên 0,05 chỉ khi E-04 tại P qua biên và lo<hi. CI thiếu/không hợp lệ hoặc suy biến thì OB giữ 0,025. Dùng lo/hi đã làm tròn cho cả quyết định và kích hoạt. TT không nhận mức từ OB. Thay Holm Q-211 và đưa đảo dấu TT tại 0 thành phép nhạy, không áp đảo dấu dịch biên làm kiểm E-04. Đây là phân bổ sai số gia đình danh nghĩa 0,05; bảo đảm thống kê phụ thuộc hiệu lực từng phép. Bộ lọc CI suy biến chỉ giảm tập bác bỏ, không sửa undercoverage. Không dùng số 0,50/0,31 ngoại suy dev làm power.
7. **Phụ.** TT đảo dấu quanh 0 và hoán vị theo ca là độ nhạy có điều kiện. McNemar hai phía, một cặp nhị phân/ca: mỗi seed TORAI đạt iff status OK và root chắc hạng 1 theo hạng min=max=1; ca TORAI đạt nếu ≥2/3 seed, M1 đạt nếu chắc hạng 1. Bản all-3 là độ nhạy độ ổn định, không là bản chính. Giữ lỗi là 0. Bảng chính Hit@1 vẫn kỳ vọng hòa/trung bình seed. Báo McNemar theo ca có giới hạn phụ thuộc trong ô; không dùng nó quyết A4.
8. **Worlds.** Chỉ P quyết A4/chuyển mức. S_lo/S_hi dùng cùng cặp/mẫu để báo CI, dấu và cách đọc, đánh dấu kết luận phụ thuộc giả định quan sát nếu qua biên/khác 0 thay đổi. Cờ WORLD_DEPENDENT theo ca khác với đổi kết luận tổng hợp.
9. **Biên/dự phòng.** Giữ Δ=0,05. Đã đối chiếu TORAI B−SimpleRCA dev khoảng 0,02556; chưa có căn cứ lập biên kiểu M1/M2 mới. Chọn phương án (c) của D.1 nếu không đạt: câu đầu “Không đạt E-04. Chưa chứng minh được không thua quá 0,05”, kèm cỡ chênh/CI. Đây là phương án thống kê, khác chế độ (b) đã hoãn.

| Kết quả tại P | Cách báo |
|---|---|
| CI nằm trọn trên 0 | Hơn TORAI B theo CI danh nghĩa của giao thức, kèm giả định/giới hạn bootstrap; báo E-04 và số ô riêng. |
| CI nằm trọn dưới 0 nhưng lo>−0,05 | Đạt E-04 theo công thức và kém TORAI B theo cùng cách đọc CI. Không suy vượt SimpleRCA. |
| CI chứa 0 | Chưa phân biệt hơn/kém; E-04 đọc riêng theo lo với −0,05. |
| lo≤−0,05 | Không đạt E-04, chưa chứng minh không thua quá 0,05; báo cỡ chênh/CI. |
| CI suy biến | Ghi trong cùng câu, số đếm và nguy cơ CI hẹp hơn thực; OB không nhận thêm mức. |
| OB p vượt ngưỡng dù chênh dương | Chưa phân xử theo kiểm có điều kiện; báo chênh/CI, số ô hữu hiệu và giới hạn M4. Ba ô cùng dấu chỉ cho p nhỏ nhất 1/8, cần ít nhất năm/sáu ô để có thể qua 0,05/0,025. |
| M1 hơn baseline nhưng không hơn C-a hoặc C-d2 | Giới hạn kết luận ở cặp được hỗ trợ, không khẳng định lợi ích chung của quan hệ. |
| Dấu thay đổi theo bộ/loại lỗi/vị trí hoặc world | Báo tách nhóm và ca, dữ kiện/phép tính nào đổi; không chọn nhóm/world thuận lợi làm kết luận chính. |

### Hồ sơ G3, RE3 và chuyển giao

B6 khóa code/revision, mọi tham số/cổng, A0/worlds, U/alias/quan sát, tập ca, hòa/lỗi/fallback, vùng/verdict, trạng thái thành phần, baseline/đối chứng, A4 và cách báo sau sửa. Trả lời sáu câu MRP §7 bằng bằng chứng. Bảng thành phần dẫn WHY hiện có và WHY-76/77; gồm cả lựa chọn tắt E9/T12 và giới hạn VC×E5.

V0 giữ trong bản ghi để truy vết; chấm P7(a) từ danh sách hạng và trạng thái hỗ trợ, không dùng V0 mở sự cố hay truyền thành mức tin cậy root cho LLM. WHY-68 chưa chọn được verdict hiệu chuẩn. Hiệu chuẩn cần nền lành cùng cỡ cửa sổ/lỗi/tải có nhãn độc lập ở FT.

P7 xin so cạnh quan sát với quan sát∪snapshot tĩnh T-038/T-039 theo D8; giữ E1/E2 từ span và chỉ tác động những bước D8 cho phép. Ghim snapshot/alias/U, provenance và hỗ trợ trước test. Revision benchmark chưa nối chắc thì báo có điều kiện snapshot, không gọi static-only hoặc kiểm đủ messaging/data. Mọi vế thiếu hỗ trợ giữ đúng mẫu số/trạng thái đã khóa, không bỏ sau chấm.

RE3 nguyên bộ cho bản cuối theo Q-247, chưa mở. Trước lượt đó khóa ho_so_nguon, schema/đơn vị/coverage/kênh/log, U/alias phi nhãn, allowlist mờ, luật N/A, baseline/mẫu số và fixture từ metadata/schema được phép. Adapter hiện chỉ có RE2-TT/Nezha-OB, cần thiết kế/kiểm đường RE3 trước mở; cùng họ RCAEval không tự chứng minh chạy được. Metadata 30 ca/4 root/5 lỗi/10 ô không dùng bốn root làm U. Nếu metadata chưa đủ khóa hợp đồng, ghi OPEN và trình đúng phần cần xác minh. Dung lượng tải và quyền mở trình riêng. C-15 B giữ kết quả đầu, bản sửa có dùng test báo riêng; RE3 chỉ mở một lần bản cuối.

P9a có thể chuẩn bị R-01–R-10 song song khi được giao; trạng thái nhóm hệ thống cần Minh/nhóm xác nhận. D3 sau khi Minh mở lại (b) khóa luật Grafana/tín hiệu/lịch sử/lịch đánh giá, phát lại chỉ thấy dữ liệu tới mốc, trạng thái/sự cố và độ đo. D16 so M1/baseline cùng t_hat/cửa sổ trên TT dev, hạn trước kết luận (b) và khóa FT. G/H vẫn theo quyết định riêng. P10 dùng nhãn độc lập và dữ liệu mới sau khóa, so chuyển thẳng/thích nghi/che thông tin theo D14, báo (a)/(b). P8 đánh giá LLM sau có gói bằng chứng.

## Kiểm đúng đắn

- Kiểm SHA/byte và nguồn theo manifest đúng lượt; tách kết quả kiểm hiện tại khỏi lời báo đã kiểm của agent khác. Kiểm trường dùng thực, không mặc định bản gọn có đủ vùng/O/control.
- Pilot native trước ghép nhãn, chạm nhánh có tác động và ca đối chiếu. Dung sai theo nguồn đã khai, chênh số thực không được làm đổi cờ/ngưỡng/hòa/hạng/tập. Cùng vế cùng máy khi số học ảnh hưởng quyết định. Kiểm cross-machine trên dev đã có hoặc pilot đúng nguồn; không mở phép so laptop vô ích nếu không đổi lựa chọn.
- Khi phải bổ sung phép chấm, dùng blocks/key thật và giữ khối hòa TORAI. Ghim ca, cửa sổ, U/alias, coverage, seed, cờ, tầng, khóa, lỗi và fallback theo từng vế. Ghim nhanh_z và che_do trong dấu vân tay cấu hình hiệu lực. Giữ đúng ca và seed đã khai. Kiểm không cần nhãn trước evaluator, chống path/label-derived feature.
- Trước seal để chấm, xác minh hash/schema, ánh xạ, cửa sổ, cấu hình hiệu lực và biên nhận thực thi. Phân loại lỗi theo nơi phát sinh vì `ERROR` cũng có thể đến từ lỗi cấu hình runner. Lỗi dữ liệu, adapter đọc/cắt sai, cấu hình runner hoặc hạ tầng thực thi giữ biên nhận riêng và dừng vế phụ thuộc trước khi tính điểm. Khi đã xử lý, giữ đúng ca và seed, chỉ chạy lại vế chịu ảnh hưởng theo quyền hiện hành. Chưa phân loại được thì ghi OPEN và dừng bảng phụ thuộc. `ERROR` của phương pháp trên đầu vào và cấu hình hợp lệ, `NO_EVIDENCE`, `UNSUPPORTED` và `TIMEOUT` theo quy tắc khai trước vẫn ở mẫu số theo [Q-74](../../docs/DECISIONS.md) và [giao thức P3 §8.3](../../results/T-022/giao-thuc-v2.md#83-trạng-thái-q-74-q9-d12).
- Fixture trước ghép nhãn phải xác nhận hai nhánh. Cấu hình runner thiếu trường bắt buộc dừng trước chấm. Lỗi của phương pháp trên đầu vào và cấu hình hợp lệ giữ ca và được chấm trượt.
- Kiểm cùng đầu vào với chế độ tách C-d3 bật/tắt. Khớp hạng, vùng và các trường dùng để chấm M1/C-a; tiêm lỗi giả ở C-d3 để xác nhận chế độ tách vẫn trả hạng. Đối chiếu phép tính C-d3 với đường đi liệt kê trên đồ thị giả nhỏ và trung gian dev đã ghim, gồm chu trình, thiếu đích, ứng viên trùng đích và hòa điểm.
- Fixture A4 gồm cận đúng biên, CI suy biến, ít ô khác 0, ô khác cỡ, seed lẫn, lỗi cả hai, dấu bằng nhau, p tại ngưỡng, ba worlds trái cách đọc, C-e thiếu lịch sử và O=0.
- Kiểm synthetic chỉ chứng minh công cụ làm đúng giao thức, không chứng minh hiệu chuẩn bootstrap trên mọi phân bố. Phản ví dụ ô thưa cho thấy undercoverage có cả khi CI không suy biến. Giữ giới hạn đó ngay câu diễn giải.
- Báo từng nguồn hạn chế, ca đúng tương ứng và giải thích khác. Không mở lại điều tra OB đã dừng Q-192 hoặc gán collector có thể khôi phục điều chưa được ghi.
- Kiểm đủ các đầu ra với câu hỏi nguồn, bảng thành phần, mức tiếp xúc và sáu câu G3. Reviewer chính thức khác người làm; tiếp nhận agent factual read-only không thay phản biện Claude.

- Giữ các vế native cần chung cache trong cùng tiến trình theo cửa sổ. So quyết định tại biên trước khi chấp nhận dung sai số thực. Nếu nền và đối chứng phải được so lại do lệch máy, tính đúng các vế chịu ảnh hưởng trên cùng máy sau quyền tương ứng.
- Bootstrap dùng hàm hiện hành trên độ đo từng ca. Giữ thứ tự ca/ô, mẫu ghép cặp và cách tính seed. Dùng hash của phần đã đóng để tiếp nhận lại đúng phần thiếu.

## Tiêu chí xong

1. Ma trận T13 có đúng nền, đủ 52 ca thật và 30 cửa sổ giả cho các cặp được hỗ trợ, đủ sáu baseline và đối chứng, trạng thái/mẫu số rõ. Có biên nhận kiểm phân loại lỗi trước chấm. Các vế tái dùng được chứng minh từng trường hoặc ghi đúng thiếu cần xử lý.
2. Vùng đủ hai cách/cặp T12 và tỷ lệ theo O. C-e đủ phân bố hạng đầu/root đối chiếu/coverage/V0/N1, giữ giới hạn nền lành.
3. Nhóm quan trọng có chuỗi bằng chứng và phản ví dụ hoặc ghi đúng bước chưa phân xử, bằng chứng cần thêm và quyết định bị chặn. Cờ trái chiều E2 và VC×E5 còn trong hồ sơ.
4. Giao thức P7/A4, code kiểm dev, tập ca mờ/quyền nhãn/U/alias, vị trí/mức tiếp xúc, máy/budget, bảng diễn giải và B6 có thể đối chiếu. Hồ sơ chỉ ghi sẵn sàng khóa khi có điểm vào P7 cho M1 và baseline, cùng kết quả fixture theo mục Tập ca. Nếu thiếu, báo đúng mục chặn trước khi Minh quyết G3.
5. Tự kiểm toàn diff, nguồn và đầu ra, LOG đủ tiếp nhận. Đề nghị nghiệm thu task và quyền khóa/mở dữ liệu là bước riêng.

## Không làm

- Lượt ghi này chưa chạy code/pilot/chấm mới, chưa sửa src, chưa mở test/RE3, chưa commit/push hay bật máy. Quyền triển khai T-052 trình riêng.
- Chế độ (b) và G/H theo Q-245. Phần RQ3a/P/R/F1 công khai thiếu được báo ở G4; D3/D16/P9/P10 nhận nghĩa vụ cụ thể như trên.
- T13 không đổi nền vì cần thắng, không hiệu chuẩn verdict trên C-e test, không bỏ ca khó sau điểm hoặc làm static-only/đảo PageRank/2×2 VC×E5 ngoài phép so đã duyệt.
- Không coi task xong là trả lời hết RQ2/RQ3 hoặc bằng chứng độc lập. Kết luận cơ chế thiếu trung gian vẫn OPEN, trình phép bổ sung có phạm vi/chi phí nếu cần.

## Chi phí ước lượng và phân phối máy

Mục tiêu theo Q-243 là thời gian hoàn tất cả gói. Tính cả cấp máy, kiểm/chuyển/giải nén, tính/chấm/bootstrap, đọc ca, hồ sơ, phản biện/sửa và Minh duyệt. Tiền máy không là ràng buộc. Quyền chạy ban đầu đề nghị riêng: pilot và chấm dev từ nguồn ghim tối đa 60 phút máy, sau khi môi trường/tài nguyên sẵn. Chạy native rộng hoặc >1 giờ/tải >5 GB cần trình phần thiếu và trần trước.

**Nhánh tái dùng đạt, dự toán chưa đo T-052:** 5–7 giờ hoạt động của người làm. Dự trù thêm 1–3 giờ công phản biện và sửa. Thời gian chờ Claude/Minh để OPEN. Giả định môi trường sẵn, nguồn hợp lệ, parity đạt và pilot dev chuẩn bị P7 local vừa phần dự phòng. Dự toán này tách khỏi quyền chạy ban đầu tối đa 60 phút máy đang trình. Mốc dưới đây là lịch dự kiến theo thời gian trôi, có việc chạy song song.

| Mốc tương đối | EC2 | Laptop/người làm | Đầu vào cần có |
|---|---|---|---|
| 0–30 phút | Kiểm máy, môi trường, dev, đĩa | Ghim nguồn, ma trận trường và bảng baseline | Quyền sử dụng máy và nguồn |
| 30–90 phút | Pilot native C-a khi công cụ sẵn | Viết công cụ chiếu, bộ đọc gọn, fixture và chuẩn bị A4 | Cấu hình và công cụ pilot đã ghim |
| 90–150 phút | Đối chiếu, nhận/kiểm phần đã đóng | Hoàn thiện A4, cohort, tách nhãn và kiểm vị trí N | Pilot cung cấp bằng chứng parity hoặc chỉ ra miền thiếu |
| 150–240 phút | Chỉ xử lý phần native thiếu nếu được duyệt | Chấm/CI từ bản gọn, đọc ca và pilot dev trên máy P7 local khi được phép | Nguồn đủ cho vế phụ thuộc. Đo pilot khi máy rảnh tải cạnh tranh |
| 240–330 phút | Nhận/kiểm nốt đầu ra cần thiết | Báo cáo T13, B6, hồ sơ G3 và tự kiểm | Bảng và giới hạn kết luận đã có |

Đường găng dự kiến qua công cụ và hợp đồng, kiểm dev/parity, đọc ca, hồ sơ, rồi phản biện/sửa. Nếu parity chỉ hỏng một miền, khoanh đúng cửa sổ/vế cần native và trình quyền, tài nguyên và thời lượng riêng. Dùng kết quả hợp lệ cho các vế độc lập.

**Phân việc:** EC2 cũ 2 vCPU, 2 worker native theo cửa sổ. Laptop xử lý bản gọn và A4, mỗi việc bắt đầu một tiến trình. Nếu còn native độc lập có thể chia sang laptop, ba worker là ứng viên theo lát cắt T-053, cần đủ RAM/đĩa lúc chạy. Nếu khối native còn lại lớn, cân nhắc máy x86-64 khoảng 16 vCPU/64 GiB, đo 4 rồi 8 worker cùng lát cắt. Chọn khi thời gian cấp máy, chuyển, kiểm, chạy và nhận thấp hơn phần chờ tương ứng trên đường găng. Quota, đĩa và hiệu năng máy mới chưa kiểm. Số đo lịch sử T-048 và T-053 dùng cho native theo tải đã đo. Lượt T-051 cho thấy thời gian giải nén và nạp JSON đáng kể so với thời gian đọc/hash ở lần đo tách, nên ưu tiên chiếu tại nơi có nguồn.

Nguồn: [pilot T-048](../../results/T-048/pilot.json), [LOG T-053](../T-053-kiem-z-chay-lai-k/LOG.md), [phân rã T-051](../../results/T-051/dinh-chinh-luot-1.md), [LOG T-047](../T-047-khoi-k-luot-2/LOG.md), [LOG T-049](../T-049-k-b-va-t6/LOG.md), [LOG T-050](../T-050-t9-va-t10/LOG.md).

**Dữ liệu:** biên nhận EC2 cũ T-053 có 89 file TT 656.358.942 byte ở /home/ubuntu/rca-t048/staging, 154 file OB 1.041.219.665 byte ở /home/ubuntu/rca/T-032/repo. Kiểm lại tại chỗ. T-048 từng chuyển/kiểm 589 MB ~88 giây, chỉ là mốc lịch sử. K nén T-053 khoảng 821 MB gồm khoảng 75,4 MB native và phần trace còn lại theo seal K và manifest T-053. KB gọn khoảng 38 MB. Kiểm nguồn tại máy, chỉ chuyển phần dev cần cho lượt được phép. Ưu tiên đọc theo luồng để tránh ghi bản giải nén xuống đĩa. Đọc theo cửa sổ, không nhân bản trung gian nặng Q-244. Dự toán đầu ra nén+đỉnh tệp tạm+bootstrap+gói nhận+lượt hỏng, theo dõi sức chứa trước và trong chạy. T-053 từng hết ổ D ở mẫu bootstrap 448; sau chuyển phần pha 2 đủ điều kiện lên EC2, tiền tố 448 mẫu khớp byte.

**Môi trường/SSH:** kiểm instance/host key, executable/version/PYTHONPATH và import networkx/thư viện entry point. T-049/T-053 gọi nhầm env T-031 thiếu networkx rồi chạy với env T-025 đã ghim. Python không gọi được trong tool Codex không chứng minh Python cả laptop hỏng. Tách controller khỏi SSH, ghi PID/lệnh/timeout/progress/receipt. Keepalive 30 s, max3, BatchMode. Theo dõi CPU/RSS cả cây/đĩa/stderr/cửa sổ đóng. SSH mất thì kết nối mới kiểm remote và hash phần đóng rồi tiếp phần thiếu. T-053 -n đơn lẻ không sửa được SSH treo sau worker xong; giữ mọi lỗi và resume theo hash.

**Máy/quyền cho P7:** Q-42 cấm chép locked lên EC2, ngoại lệ dev cũ không chuyển thành quyền test. Hồ sơ P7 mặc định máy local giữ dữ liệu. Trước G3 pilot bằng dev đại diện để đo TORAI (đúng env riêng), M1/T12/sáu baseline, 60 cửa sổ C-e và hậu xử lý; chọn worker theo RAM/đĩa/runtime. T-031 EC2 dev TORAI B 1.635 giây/90 lượt và 16/16 cross-machine chỉ là mốc. Dự toán lại trên local, đối chiếu Q-40 và xin trần >1h nếu cần. Nếu local không đủ, trình máy local khác hoặc ngoại lệ Q-42 trước truyền. Không ngoại suy số EC2 cũ thành ETA test.

## Rủi ro và điều chưa chắc

- Dev chọn lặp, baseline M4 tái lập còn giới hạn Q-192; xếp hạng đẹp chưa là generalization hoặc cơ chế.
- A0 chưa xác minh; ba worlds không bao hết mọi mất dữ liệu. Giữ kết luận có điều kiện.
- Bootstrap percentile ít ô/rời rạc có thể undercoverage, cả CI không suy biến; chuyển mức chỉ có bảo đảm nếu thành phần đạt mức. Không dùng p/CI như chứng minh tuyệt đối.
- Parity C-a0/a1, trường compact, đường test/RE3 và môi trường máy hiện tại chưa kiểm bằng lượt native mới trong phiên này. Đầu ra hợp lệ cũ không thay được phép kiểm cho thay đổi có ảnh hưởng.
- Tập test TX1, ca liền kề Nezha, RE3 cùng hệ/công cụ giới hạn khẳng định độc lập. Khóa cohort có sẵn trước khi materialize allowlist sau quyền mở.
- T12 snapshot chưa xác minh revision runtime; miền quan hệ messaging/data còn thiếu hai đầu. Giữ phạm vi D8 và chuyển yêu cầu P9/P10.
- Trần và ETA native rộng chưa đo; giữ dấu vết và dự toán theo nhánh sau pilot, không cộng runtime máy thành thời gian nghiệm thu.

## Prompt bàn giao

Prompt nguyên văn theo docs/review-prompt.md nằm ở mục bàn giao hiện hành của LOG T-052. Chỉ Minh chuyển thủ công. Công đoạn kế là Claude kiểm lại bản sửa kế hoạch nếu Minh chuyển; quyền ghi của reviewer theo lời Minh từng lượt. Quyền triển khai dev và quyền G3/test được xét riêng.

