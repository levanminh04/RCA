# T-032 — Chuẩn bị lần theo SimpleRCA từ trung gian đã lưu

Vai trò: trợ giúp người làm. Đây là ghi chú đọc code và chuẩn bị bộ đọc, không phải phản biện chính thức. Chưa chạy bộ đọc trên EC2 và chưa dùng chuỗi mới để kết luận cơ chế của ca nào.

Đã đọc AGENTS, SPEC T-032, phần P4/RQ2 trong MRP, hướng dẫn cô §1, DT18-NV2/NV3, LESSONS và WHY-33/WHY-40. Mục tiêu là phân biệt bước chấm thông tin với nguồn vật lý của tín hiệu. Hạng caller cao hơn root hoặc duration span tăng đều chưa xác nhận chờ phụ thuộc.

## Chuỗi code thật

Nguồn chính là `src/simplerca/core.py:44`, ở hash được khóa trong T-026. `diagnose` nhận mapping giá trị metric/trace/log, mapping metric→service và service quan sát. Nó không nhận root, tên ca, nhãn, đường dẫn hoặc đồ thị. Root và quan hệ trong T-028 chỉ được nối sau khi chuỗi đã được kiểm.

Ở metric (`core.py:62–74`), bỏ giá trị không hữu hạn riêng N và A. Có ít nhất 2 giá trị nền và ít nhất 1 giá trị A mới chấm. Ngưỡng cấu hình chính là mean(N) + 3×std(N, ddof=0), vượt ngưỡng theo dấu `>`. Một metric đóng góp số mẫu A vượt ngưỡng, không phải một phiếu nhị phân. Giá trị thiếu, số mẫu không đủ và không có mẫu vượt ngưỡng là ba trạng thái khác nhau.

Ở trace (`core.py:75–86`), từng service có p95 riêng N/A với quantile linear. Service đóng góp đúng 0 hoặc 1 phiếu theo p95(A) > 3×p95(N). Đây là duration đã gán service; code không dùng quan hệ cha–con để tách thời gian chờ, xử lý riêng hoặc phần việc của descendant. Vị trí hai hàng làm witness cho quantile là tạo tác chẩn đoán từ input đã thu, không phải định danh hàng do native trả về.

Ở log (`core.py:87–100`), một hàng khớp một hay nhiều từ ERROR/FAIL/EXCEPTION vẫn chỉ tăng count một lần. Service đóng góp 0 hoặc 1 phiếu theo count > 0. Input log None giữ `unavailable`; mapping rỗng vẫn là kênh quan sát được nhưng không có hàng. Không gộp hai trạng thái ấy.

Điểm service bằng số phiếu metric cộng phiếu trace và log. Native sắp theo điểm giảm dần rồi tên service tăng dần (`core.py:103`). Nhóm hòa dùng điểm bằng nhau đúng giá trị, không dùng tên để xóa hòa. Toàn điểm 0 trả `abstain` (`core.py:109`), adapter giữ NO_EVIDENCE; native vẫn có ranks nhưng protocol không chế ra ranking có bằng chứng.

Ánh xạ protocol được kiểm riêng: RE2 lấy tiền tố trước underscore đầu tiên; Nezha giữ tên service. Nếu nhiều phần tử native cùng thực thể, `src/p3/ban_ghi.py:20` lấy khóa cao nhất và giữ thứ tự xuất hiện đầu khi hòa. Vì vậy không cộng điểm của các native service bị gộp thành một thực thể.

WHY-33 chọn đơn vị events từ trước P3. Số metric và số mẫu ảnh hưởng thang điểm metric, trong khi trace/log chỉ có tối đa một phiếu mỗi service. Đây là đặc tính code để kiểm trên ca sai và ca đúng; chưa là nguyên nhân của mọi ca sai. Không tự đổi events sang channels, ngưỡng hay cửa sổ.

WHY-37 và trung gian Nezha giữ arrays riêng từng kênh; không dựng một trục thời gian chung cho các mẫu metric. F của RE2 dùng giây và t/N/A. F của Nezha dùng nanosecond và t_ns/N_ns/A_ns. Bộ đọc đối chứng kiểm đúng trường và unit từng dataset.

## Phạm vi của bộ đọc chuẩn bị

`scripts/research_simple_chain_v1.py` đọc đủ 52 ca từ batchstatus đã PASS; retained pilot RE2 dùng audit riêng thay cho check hỏng ban đầu, nhưng giữ run hỏng. Plan tại `plan.json` khóa record và check/audit hash, T-028 row, nguồn code, group lock và danh mục đối chứng. Tệp native/capture đầy đủ nằm trên EC2, chưa hiện diện local trong lúc chuẩn bị.

Bộ đọc yêu cầu hash của **mọi** artifact trong manifest cũ, gồm Parquet, trước khi dùng JSON. Nó yêu cầu phép phát lại đóng băng và phép kiểm toàn array/native/mapping cũ đều đạt. Sau đó kiểm lại scalar threshold, finite/missing positions, count/vote, tổng điểm, exact tie, native rank và protocol max-per-entity từ trường đã lưu. Không import native, không đọc dataset thô, không refit hay chọn lại cấu hình.

Không gọi việc này là một lần kiểm toàn array mới: mean/std/quantile và nội dung witness dựa trên native return đã ghi cùng audit khôi phục input cũ; byte hash bảo đảm đầu ra cũ không đổi. Các phép kiểm scalar mới có khớp tuyệt đối, không có tolerance MicroRank hoặc tolerance riêng nào.

Theo source được hash, hợp M5 là 14 ca: 5 RE2, 9 Nezha. Có 25 yêu cầu cặp ở từng k và 331 liên kết lớp đối chứng từ danh mục đã khóa. Đây là mẫu số chuẩn bị, chưa là 14 cơ chế đã phân xử. Bộ đọc giữ mọi caller có path đến root, cả caller có và không có điểm cao hơn root. Không chọn cặp theo chênh điểm.

Output dự kiến `simplerca-saved-chains.json` giữ từng thành phần điểm, witness và con trỏ; caller/root dùng pointer để không nhân bản các danh sách vị trí dài. Có margin có dấu cùng mẫu số, giữ mẫu số 0 và thiếu điểm; margin không làm ngưỡng hay điều kiện chọn ca. Mỗi liên kết đối chứng vẫn ghi chưa đọc tay cho tới khi người làm thực sự so cặp.

## Việc còn phải kiểm trước khi dùng

AST, các hash metadata đầu vào, hash của đủ 52 frozen records, số ca/nhóm/đối chứng và các hash code trong source authority đã kiểm local. Không chạy native, không đọc Parquet, không đọc raw data. Schema runtime mới được đối chiếu qua code, chưa kiểm trên capture JSON thật; không tuyên bố đã chạy đúng.

Root cần đọc script, kiểm package hai đầu, đo lại tổng dung lượng mới và xếp một lượt EC2 sau việc nặng đang chạy. Chạy trong thư mục execution mới; lỗi dừng, giữ nguyên lượt và không dùng chuỗi đã thu dở. Candidate chưa đo: 1–15 phút, tối đa 2 GiB RAM và 300 MiB output. Đây không phải giới hạn tài nguyên đã xác nhận; phải đo thực tế và checkpoint nếu không đủ ngân sách.

Khi output đã PASS vẫn còn đọc tay các nhóm/đối chứng, phân biệt cửa sổ/coverage/mapping với cách tính, và phân xử cạnh tranh về caller. Semantics chờ, đồng hồ, sampling và nguyên nhân tải/tài nguyên chung còn cần dữ kiện thích hợp. Chuỗi tính toán đủ không tự chứng minh chờ phụ thuộc hoặc lợi ích đồ thị.
