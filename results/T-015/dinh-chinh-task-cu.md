# VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM

## DC-01 — T-001: tên hàm 3sigma không phải multiplier mặc định 3

- **Task/file:** T-001, `results/T-001/danh-sach-phuong-phap.md:88` (dòng TraceRCA gốc).
- **Sai gì:** gọi detector gốc "3σ" mà không kiểm tham số thực. `run_anomaly_detection_invo.py:14` default threshold=1.0; `:59` so abs(empirical−mean)>threshold·std; CLI `:72` default1; Makefile `:23 SIGMA=1`.
- **Bằng chứng:** đúng revision nguồn trong manifest-inputs; AST hàm gốc trên reference μ=10, σ=1, empirical=[12,10] cho [1,0] ở threshold1, [0,0] ở threshold3; `runs/tracerca-audit/toy-extra/toy-checks.json`, trường `original_tracerca_named_3sigma_default_threshold1`.
- **Kết luận ảnh hưởng:** default TraceRCA gốc, so detector gốc với luật một phía μ+3σ RCAEval. Không đổi số ranking RCAEval T-007.
- **Đã triển khai:** kiểm độc lập/toy nạp AST, hồ sơ sửa tên và ngưỡng trong T-015; không sửa T-001.
- **Đề xuất cũ → mới:** "phát hiện 3σ trên các đặc trưng đã chọn" → "phát hiện độ lệch hai phía trên đặc trưng theo reference; hàm tên 3sigma nhưng multiplier mặc định 1 (Makefile SIGMA=1); khác luật span μ+3σ của RCAEval".
- **Nguyên nhân khả thi khác đã xét:** CLI có thể truyền3 ở một lượt riêng; không có bằng chứng đó là đường mặc định Makefile nên không gándefault3. Không suy số bài từ một multiplier chưa biết.

## DC-02 — T-000/K1 và tài liệu chung: cần phân biệt PageRank với quan hệ học self-time

- **Task/file:** nội dung nền T-000: `docs/knowledge/K1-phuong-phap-rca.md:32,49–51,180,299–303`; `docs/MRP.md` §2.3; `docs/WHY.md` WHY-02.
- **Vấn đề:** "PageRank không quyết định bất thường" đúng. Nhưng câu mở rộng thành "đồ thị/quan hệ không tham gia phát hiện" bỏ quan hệ cha–con của code gốc khi học SLO self-time.
- **Bằng chứng:** `MicroRank/preprocess_data.py:191–192,218–219` trừ duration con khỏi cha; code nguồn revision đúng và hồ sơ T-015 đọc PDF. PageRank chỉ chạy sau partition không phủ nhận quan hệ đã đi vào μ/σ.
- **Kết luận ảnh hưởng:** cách phân loại thông tin graph và biên đối chứng bỏ graph, không thay số RCAEval T-007 vì detector span đó không có self-time.
- **Đã triển khai:** bảng bước giữ/khác và hồ sơ detector phân biệt hai đường; kiểm công thức gốc đúng; nháp sửa chính xác ở de-xuat-tai-lieu-chung.md §4.
- **Đề xuất cũ → mới:** câu tuyệt đối về "graph không tham gia detection" → "PageRank không quyết định nhãn; quan hệ cha–con tham gia tiền xử lý SLO self-time của gốc, luật span RCAEval không có bước đó".
- **Phản bác đã xét:** nếu "graph" chỉ gọi ma trận operation–trace của ranker thì câu có phạm vi đúng. Vì vậy sửa phạm vi diễn giải, không gọi toàn lập luận thiết kế P6 sai.

## Các điểm T-007 đã được sửa trong nguồn cũ

R2/R4 đã có trong báo cáo hiện hành: hai sai lệch và trần coverage của những thứ hạng đã quan sát. T-015 kiểm tiếp tác động, không trình lại chúng như lỗi mới chưa sửa. NaN/sắp xếp được T-007 báo đúng và tái dựng trong T-015; lỗi nằm ở code RCAEval, không phải lỗi số chấm T-007. Lệnh EC2 thiếu mkdir ở REVIEW R1 đã được sửa trong moi-truong-ec2.md.

## Phạm vi đọc task cũ

Đối chiếu nguồn nền/MRP/quyết định, danh sách phương pháp, thẻ/input matrix và REVIEW liên quan T-000–T-012 trong phạm vi hồ sơ trace. Không đọc raw/dự đoán ngoài danh sách ca cho phép, không chạy RCA trên dataset P2 mới và không mở dữ liệu khóa. Không coi việc thẻ chưa chọn dataset/clock/license còn OPEN là lỗi cần tự sửa.



T-004 chưa triển khai: không có thư mục task/kết quả ở lần rà cuối, STATE cũng ghi như vậy (`runs/t004-availability-audit.json`). Không có kết quả T-004 để tái kiểm. Audit các task cũ chỉ bao phủ nhận định liên quan đầu vào/cơ chế trace; không chứng nhận lại toàn bộ phương pháp và mọi số của T-000–T-012. K1 Ochiai/66% phù hợp bài, đã kiểm nên không báo thành lỗi chỉ vì code đang dùng Dstar2.
