# Nguồn CIRCA đã kiểm trước phép đo

Ngày kiểm: 04/10/2026. Người đọc: Codex, nhánh hỗ trợ người làm T-014; không phải người phản biện.

Nguồn bài chính thức: [CIRCA, KDD 2022](https://netman.aiops.org/wp-content/uploads/2022/08/KDD22-CIRCA.pdf), [DOI](https://doi.org/10.1145/3534678.3539041). Bản tải gồm 11 trang. Đã soi ảnh trang 4, 5, 7 và 11, gồm công thức residual, Algorithm 1/2, Table 1/3/4/5. Bản gốc, văn bản trích và ảnh nằm cùng thư mục; hash ở `source-manifest.json`.

Các mốc số đọc trước khi chạy nằm trong `cong-bo-circa.csv`. Oracle là dữ liệu khác RE2-TT. Không dùng số Oracle để đánh giá một ca RE2-TT. Đơn vị xếp hạng của mốc là metric, không phải service.

Điểm cần phân biệt khi đọc nguồn:

- Table 4: RHT dùng SVR; CIRCA thêm DA. Table 5 cùng điểm SVR nhưng thời gian khác Table 4: giữ nguyên từng bảng, không tự hòa giải.
- Mặc định của lớp ANMRegressor là LinearRegression; mô hình thực nghiệm Oracle dùng SVR với sigmoid kernel (`circa/experiment/comparison/models.py:585`). Hai điều này có thể đồng thời đúng.
- RHTDAGetter đặt threshold=3 (`models.py:629–634`). Mặc định của lớp DAScorer là 0 (`circa/alg/ci/__init__.py:109–117`). Khởi tạo DAScorer() không tương đương cấu hình thực nghiệm RHT+DA.
- README:9 cho biết artifact kết quả Figshare thuộc một revision khác revision T-001 chốt. Hash cả hai ở manifest. Không gọi checkout hiện tại là bản đã tái lập đầy đủ bài gốc chỉ vì import được.
- Trong bài, Algorithm 2 dòng 11 dùng ký hiệu của child còn sót ở vòng lặp trước. Cách code hiện thực kiểm score của chính node đang điều chỉnh (`circa/alg/ci/__init__.py:149–155`). Hồ sơ viết công thức theo code, giữ ghi chú khác biệt ký hiệu.

## Đề xuất scorer trước kết quả

**CANDIDATE:** dùng LinearRegression + RHT cho cặp PC/kiến trúc tham chiếu trong T-014. Vì sao: bản RCAEval đang dùng đúng scorer này; giữ scorer và cửa sổ cố định giúp đối chiếu cấu hình mà không đổi thêm hai yếu tố này. Chưa cô lập tác động của nguồn đồ thị: hai nhánh còn khác candidate coverage, parent sets, chiều cạnh và phạm vi reference. Phương án mỗi nguồn theo prior work riêng cũng cần xét; chưa chốt P3. Đây là biến thể RHT-only, không đại diện cấu hình đầy đủ Oracle của bài. **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**

Prior work đầy đủ cho kiến trúc là RHT+DA và SVR. T-014 đã kiểm linear RHT+DA kiến trúc; chưa chạy cấu hình empirical SVR+RHT+DA kiến trúc đầy đủ. Metric output DAG30/30 không tự xác nhận giả định cấu trúc, vì call/meta cyclic24/30 và có nhạy seed; nguồn ở graphs/aggregate.json và runs/builder-hashseed-1.json. DA dùng hướng nhân quả để nâng điểm ancestor nhận bằng chứng downstream. PC của RCAEval biến cạnh chưa định hướng thành cả hai hướng; thứ tự DAG không còn ý nghĩa trong SCC (strongly connected component, thành phần liên thông mạnh). Vì vậy kết quả DA trên PC cyclic là kiểm hành vi code, không tự là áp dụng hợp lệ của lý thuyết CIRCA.

Không chọn RHT vì nó cho điểm tốt hơn DA. Không chọn DA vì Table 4 có điểm cao hơn. So sánh cả hai để giải thích cơ chế và kiểm đúng như SPEC. Cấu hình P3 vẫn OPEN.

## Các giải thích thay thế phải giữ

Chênh thứ hạng giữa PC và kiến trúc có thể đến từ parent set, candidate coverage, cyclic edges, empty-meta forwarding, preprocessing hoặc hòa điểm. Chênh điểm cực lớn còn có thể đến từ residual gần hằng và StandardScaler; không tự gọi đó là evidence nhân quả mạnh. Chênh số T-006 so bài khác có thể đến từ thư viện PC, cửa sổ, code gốc/RCAEval, regression model, scorer, universe ứng viên, cách tổng hợp metric/service và lỗi dự phòng. Những nguyên nhân này cần kiểm riêng; tài liệu này chưa loại trừ chúng bằng thực nghiệm.
