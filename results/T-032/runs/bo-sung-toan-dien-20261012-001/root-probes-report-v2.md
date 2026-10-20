# Bản cập nhật 13/10/2026 — có phần KT7 đang chờ kiểm cùng predicate

Bản này thay diễn giải tương ứng trong root-probes-report.md; bản trước giữ nguyên để truy vết.

# Hai nhánh bổ sung TORAI A và mã tác giả TraceRCA

Phần này bổ sung T032 trong gói Minh cho phép ngày 12/10. Không thay bảng P3/P4, báo cáo hoặc nghiệm thu cũ. Đọc cùng `t32/REPORT.md` và ledger toàn gói. Đây là phân tích dev đã nhìn, không phải kết quả trên test.

## TORAI A: đã lần theo tổng cột của dịch vụ

Nguồn A khác nguồn B ở bảng trace và cách dựng/ngưỡng; không dùng phép so hạng A với B như một phép tự kiểm. Đã dùng đúng CSV nguồn A và cửa sổ A: 20 hàng liên tiếp cách nhau 15 giây trong cả 30 ca. Vì vậy khoảng từ hàng đầu đến hàng cuối cộng 15 giây tương đương đúng tập bin, không thêm bin trong khoảng trống. Trace raw được đọc toàn ca dev theo allowlist và kiểm hash; không lấy cửa sổ khác để kết luận thiếu cây.

Chuỗi điểm được kiểm: giá trị CSV → mean/std của N → max absolute z trong A → chia tổng điểm các cột của nguồn → cộng các cột thuộc service → vector trace của root và chênh lệch trace/severity của thực thể đứng trên root. Đã dựng lại 3.086 cột trong 30 ca; sai số tương đối lớn nhất của normalized column score là 2,01×10⁻¹⁵. Tổng trace của root, chênh lệch trace và tổng bốn chênh lệch chia bốn thành severity margin đều khớp nguồn ở 22 cặp đứng trên root, seed0.

Cả 22 cặp đều nối được mọi cột đóng góp với operation trong raw trace đúng các bin A. Trong đó 13 cặp có trace latency là thành phần chênh lệch lớn nhất. Phép đếm cũ báo 0 root-descendant với điều kiện service của descendant khác service của span owner. Điều kiện này hẹp hơn predicate hasroot của encoder; prefix cột còn có thể khác owner qua mapping HTTP. Chưa được suy từ số 0 đó rằng mọi operation-column đều không có root descendant. Kiểm cùng predicate trên toàn matched A và native conditional top-k đang thực hiện theo t32/kt7-predicate-design-001.md. Đây là quan sát ở cây đã thu, không chứng minh chúng không có quan hệ ẩn, tài nguyên chung hoặc tác động vật lý từ root.

Điểm cao ở service khác được tạo tại các phép chuẩn hóa và cộng cột vừa nêu; các toán hạng N/A, raw max z, share, service sum và margin được lưu theo ca. Bằng chứng không hỗ trợ gọi toàn bộ phần chênh trace ấy là thời gian chờ root. Đồng thời, cây không cho biết nguyên nhân vật lý của biến thiên ở operation không chứa root. P5 cần giữ hướng/loại quan hệ và độ phủ; cạnh gọi đơn thuần không xác minh được phụ thuộc host/tài nguyên chưa ghi.

CSV đếm sự kiện nhưng không giữ danh tính span đã bật cờ. Vì T16 đã có candidate encoder, đã kiểm thêm đủ 30 ca thay vì dừng ở việc thiếu ID. Candidate mean+3std, ddof1, strict `>` khớp 123.107/123.440 ô native, tức99,7302%; 333 ô lệch, chỉ3ca khớp toàn bộ. Hai scope rawfull/CSVextent có65 threshold khác nhau và khác nhau ở2 count cells trong dev-a505ab3f65. Hai tổng mismatch đều333 không có nghĩa hai bảng counts giống nhau. Chi tiết tại audit/toraiA-encoder-influence-verification-002.json#/scope_count_differences; không coi hai recipe là hai bằng chứng độc lập. Từng ô lệch được giữ, không chọn ngưỡng để đạt điểm đẹp.

Một phép kiểm có điều kiện khác dùng counts nguyên của từng bin để lấy giao interval của ngưỡng duration cố định. Cả3.086cột đều có interval khả thi, không cắt tie hoặc đếm vượt support. Dưới đúng hợp đồng column/bin và strict threshold đó, tập top-k duration của mỗi bin được xác định; không cần biết giá trị ngưỡng chính xác để biết tập. Đây là nhận diện có điều kiện, không xác minh generator gốc. Cận trên0 cho mọi flagged subset chưa được xác nhận theo predicate hasroot đầy đủ: allcolumns dùng bộ lọc cross-owner khác encoder. Phải kiểm matched A superset và native conditional top-k cùng predicate trước khi dùng kết luận bound. Mapping/coverage chưa chứng minh đầy đủ hệ thống và không suy thành chờ vật lý bằng0.

Đã kiểm ảnh hưởng333ô lệch lên chính phép chấm: giữ column support, cửa sổ và các kênh khác, thay đúng count cells của hai recipe rồi dựng lại normalized column/service trace score và severity margin. Không có trace-margin hoặc severity-margin nào đổi dấu trong22cặp, ở cả hai recipe. Đây là độ nhạy thành phần có điều kiện, không phải chạy lại GMM/RCD hoặc xếp hạng RCA. Tỷ lệ ô khớp cao tự nó không được dùng làm bằng chứng ảnh hưởng nhỏ.

Lineage generator tác giả vẫn chưa được xác minh; không gọi candidate hoặc interval fit là mã gốc. Phần tính điểm, tổng dịch vụ và ảnh hưởng count recipe đã được kiểm thêm; bound theo hasroot còn chờ phép kiểm tương ứng; truy nguyên lý do vật lý của biến thiên cần biến quan sát khác. Không để “CSV thiếu ID” che một phép kiểm còn làm được.

Nguồn: `toraiA/attempt004-allcolumns/summary.json#/cases` và `/summary`; mỗi `all_services` chứa mọi `operation_columns`, mỗi `above_root_pairs` chứa operand/margin. `toraiA-time-grid-check-001.json#/rows` giữ timestamps và hash CSV. `toraiA-encoder-006-full/summary.json#/recipe_summary`, `/constraints_summary` và `/rows` giữ counts/intervals; `toraiA-encoder-influence-001.json#/branches` giữ ảnh hưởng. Thiết kế encoder và influence đã ghi trongWHY trước chạy. Encoder full29ca mới mất416,6giây laptop, ca đầu13,8giây ởpilot được tái dùng nguyên vẹn; giữ cả lỗi đường dẫn/môi trường và các lượt dừng tối ưu. Lượt max-column trước ở `toraiA-fullA-summary.json`, lượt đầu lỗiNaN và bản sửa ffill/fill0 cũng giữ. Không chạy lại TORAI/GMM/RCD. Audit GPT6.1 độc lập đã kiểm số học CSV/influence tại audit/toraiA-encoder-influence-verification-002.json: PASS trong phạm vi đã khai. Audit không chạy lại toàn bộ raw encoder/interval; đã phát hiện hai ô khác giữa scope và gate predicate nêu trên. Không gọi toàn bộ KT7 đã audit xong.

## TraceRCA: đã chạy đường được đầu vào hỗ trợ, không giả đặc trưng thiếu

Đã đọc mã tác giả tại revision ghim trong `author-tracerca/source/`; mã chọn feature và bộ gắn cờ invocation được dùng nguyên trạng. Định dạng adapter dùng quan hệ parent-service → child-service, duration của span phía gọi; một parent/callee được đếm một lần. Duration đó có thể tổng hợp nhiều lời gọi con, nên không gọi là thời gian riêng của một RPC được xác minh.

Nhánh được hỗ trợ chỉ dùng latency, nền ngắn đang có. Feature selector xét giao các cặp có lịch sử, với mảng đã sắp xếp đúng source; fallback theo dữ liệu hiện tại không được kích hoạt. Quy tắc tác giả gọi noise ratio0 vẫn có thể bỏ 1% cờ trong trace đã bất thường, nên giữ số cờ trước/sau bước này. Chạy hai threshold feature-selection 1 và 3 (CLI/Makefile) cùng hai đơn vị ms/us; không chọn cấu hình bằng kết quả đẹp.

Pipeline mặc định cần `http_status` gắn đúng invocation và lịch sử tương ứng; span của benchmark không cung cấp đặc trưng status dùng được. Repo tác giả còn import decoder module không có trong checkout. T33 có tìm được access-log chứa status ở một phần UI; điều đó không tự cho status của mọi lời gọi nội bộ hoặc phép nối một-một với invocation. Vì vậy kết quả dưới đây không phải tái lập đầy đủ bài/default pipeline. Không giả status, không gán outcome UI cho mọi span cùng request/thời gian.

Lượt dùng lớp ranker gốc trên toàn tập vượt RAM; đã giữ script, log và dấu vết OOM. Những ca chỉ tồn tại trong RAM của lượt hỏng không được tính là đầu ra đã thu. Backend có giới hạn bộ nhớ giữ nguyên ordered FP-growth cùng phiên bản, công thức J, số trace in/out, 100 mức điểm **riêng biệt**, cap 1.000 mẫu ổn định, rồi mới bỏ mẫu nhiều phần tử. Không lọc singleton trước cap.

Đã đối chiếu 33 fixture, gồm 16.383 mẫu, trường hợp 100 mức điểm và trường hợp 1.000 mẫu đồng điểm; đồng thời chạy bốn nhánh pilot bằng lớp tác giả thật. Score/pattern/key/nhóm hòa khớp; thứ tự hiển thị bên trong nhóm hòa có thể khác giữa process do tập hợp Python. Báo hạng min/max và quy ước hòa, không dựa thứ tự ngẫu nhiên đó.

Đủ 52 ca × 4 cấu hình = 208 slot: 166 OK, 42 NO_EVIDENCE. Không có cấu hình lỗi bị bỏ khỏi mẫu số. Full007 mất khoảng 294 giây; Full008 chỉ thêm scalar để kiểm chuỗi và mất khoảng 375 giây trong điều kiện có phép khác chạy song song. Đây là thời gian quan sát, không là benchmark tốc độ có môi trường độc quyền.

| Dataset | Threshold chọn feature | N | Có xếp hạng / không bằng chứng | Hit@1 bi quan | Hit@2 bi quan | Hit@3 bi quan | Hit@1 kỳ vọng khi hòa |
|---|---:|---:|---:|---:|---:|---:|---:|
| RE2-TT | 1 | 30 | 29 / 1 | 17 | 19 | 21 | 17 |
| RE2-TT | 3 | 30 | 25 / 5 | 15 | 17 | 18 | 15 |
| Nezha-OB | 1 | 22 | 16 / 6 | 10 | 12 | 13 | 11 |
| Nezha-OB | 3 | 22 | 13 / 9 | 9 | 10 | 11 | 9,5 |

Hai đơn vị cho kết quả giống nhau trên toàn bộ 104 cặp cấu hình đã lưu. Đây là quan sát độ nhạy, không xác minh đơn vị mặc định tác giả. Các Hit trong bảng là số ca, không phần trăm; chia 30 hoặc 22 nếu cần tỷ lệ. Ca root vắng hoặc không có bằng chứng đóng góp 0 vào số ca Hit, vẫn giữ trong mẫu số 30/22. Hạng bi quan dùng vị trí cuối của nhóm hòa; kỳ vọng giả định mọi thứ tự trong nhóm hòa có xác suất như nhau. CSV giữ đủ ba cách chấm Top1/2/3.

Kết quả bác việc suy rộng từ bản cài theo lời văn trước đó rằng mọi phương án dùng cạnh có sẵn đều không đủ. Nó cũng chưa chứng minh default method hoạt động như bài, phương án này tối ưu hoặc đồ thị mới tăng hiệu quả. Adapter, độ hạt service-pair, cờ, reference và policy khác bản RCAEval trước nên không lấy chênh số này làm effect của một yếu tố riêng. Bốn ca native ERROR trong bảng cũ vẫn là ERROR; nhánh service-pair mới chạy được không biến chúng thành native OK.

Full008 lưu support count/total pattern traces/total abnormal traces, support/confidence và flagged incoming/outgoing trace counts. Công thức native:

`J = 1 / (1/max(support, 1e-4) + 1/max(confidence, 1e-4) - 1)`

`score = J × abs(in_count - out_count)`

Toán hạng có ở `score_details` cho singleton được giữ; candidate không có mẫu có score mặc định −1, không suy ngược in/out từ giá trị đó. Full008 đã đối chiếu đủ 208 slot với Full007: score, key/nhóm hòa, flags, feature và các toán hạng điểm nguyên gốc không đổi; thêm trường chẩn đoán. Thứ tự hiển thị bên trong nhóm hòa có thể đổi giữa process, nên không gọi toàn bộ danh sách hiển thị exact. Các audit độc lập ghi rõ phạm vi tính lại, không giả nhận đã replay toàn bộ mining bằng mã gốc trên 52 ca.

Nguồn: `author-tracerca/full008-instrumented/summary.json#/rows`; `full008-native-preservation.json`; `supported-summary-001.json#/groups`; `supported-comparison-001.csv`; `receipt008/`, `stream-fixtures004-cap.json`, các manifest/receipt và `audit/author-*.json`. Nguồn công khai: [TraceRCA của tác giả](https://github.com/NetManAIOps/TraceRCA/tree/b9087c72d201fbb17d724114cd389de4854815ad).
