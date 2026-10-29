# Thẻ đọc — PetShop, baseline Traversal → đối chứng C-d3

**Nguồn.** Kho `amazon-science/petshop-root-cause-analysis`, commit `2e96f937c4c044b8b4aad03217592cd52e66db5d`.
- `code/baseline_anomaly_traversal.py`: 178 dòng.
- `code/requirements.txt`: ghim `networkx==2.8.8`, `dowhy==0.9.1`.
- `code/data_preprocessing.py`: bộ phát hiện bất thường của baseline.

Bài: PetShop (CLeaR 2024), arXiv 2311.04806. Số so sánh trong bài đã tóm ở KHAO-SAT K1 (Bảng 3, 8); thẻ này không đọc lại các bảng đó.

## Cơ chế (đủ ba hàm SPEC yêu cầu)

1. **`baseline_analyze_root_causes`** (L142–176, lồng trong `make_baseline_analyze_root_causes`, L139–178):
   - đảo chiều đồ thị gọi (L161). Từ đây cạnh đi từ bên được gọi sang bên gọi, tức chiều nhân quả;
   - gọi `_traversal_rca` (L164–172), rồi `_score_potential_root_causes` (L174–176);
   - không sắp kết quả.
2. **`_traversal_rca`** (L86–136):
   - gọi `get_anomalous_metrics_and_scores` (L110–117) với metric bình thường, metric bất thường, nút đích và metric đích;
   - bộ phát hiện mặc định là `MedianDeviationScorer`, ngưỡng 5, học trên đoạn bình thường; dịch vụ dưới 10 điểm không có bộ phát hiện;
   - dò hàng thời gian đầu tiên mà đích bất thường; đích không bất thường thì trả kết quả rỗng;
   - gọi `_anomaly_traversal` trên tập nút bất thường, rồi gán điểm cho ứng viên (L133–134).
3. **`_anomaly_traversal`** (L21–44):
   - dựng đồ thị con cảm sinh trên các nút bất thường;
   - kiểm không chu trình (L31); có chu trình thì ném `ValueError` (L32–36);
   - ứng viên là nút bất thường không có predecessor bất thường (L40–41). Vì đồ thị đã đảo, predecessor là **bên được gọi**: ứng viên là nút bất thường không phụ thuộc vào nút bất thường nào.
4. **`_score_potential_root_causes`** (L47–83):
   - với mỗi ứng viên, liệt kê `networkx.all_simple_paths(đồ thị đảo, ứng viên, đích)` (L66);
   - chỉ giữ đường mà mọi cạnh có hai đầu bất thường (L69–74), nên mọi nút trên đường đều bất thường;
   - điểm đường là tổng điểm bất thường của các nút trên đường, gồm cả ứng viên và đích (L75, L78);
   - điểm ứng viên là điểm lớn nhất qua các đường (L79). Không có đường hợp lệ thì ứng viên không được trả (L80–83).
   - Với NetworkX 2.8.8, nguồn trùng đích trả bộ sinh rỗng (`simple_paths.py:242–243`; đã chạy thử). Vì vậy ứng viên trùng đích không bao giờ có điểm. Đây là hành vi gốc mà SPEC ghi "đích không thể là root".

## Đầu vào gốc và phần ta có, thiếu

| Đầu vào gốc | Ở M1 trên dev |
|---|---|
| Đồ thị gọi | Có: cạnh quan sát N ∪ A, hướng từ chủ span cha sang chủ span con (T-035). Kiểu cạnh chưa xác nhận (O03) |
| Một nút đích có SLO bị vi phạm, do nghiệp vụ chỉ định | Thiếu. C-d3 dùng quy tắc đích của B2: chế độ (a) là thực thể sở hữu span gốc của trace trong A và có bất thường lớp lan ngược |
| Điểm MAD từ metric theo dịch vụ | Thay bằng bằng chứng của chuỗi: cờ F_raw và K_raw,₁ (max s) theo thực thể |

## Điều kiện thất bại

- Đồ thị con bất thường có chu trình: mã gốc ném lỗi.
- Không có đường toàn nút bất thường từ ứng viên tới đích, ví dụ root không được gọi (G2-H19: 8 ca) hoặc nút trung gian không có cờ.
- Root trùng đích, khi chỉ có một đích.
- Điểm là tổng trên đường, nên đường dài qua nhiều nút bất thường được lợi. Ứng viên sâu, nằm cuối một chuỗi dài, thường có điểm cao hơn.
- Bất thường giả ở bên được gọi làm bên gọi mất tư cách ứng viên (giống điều kiện thất bại của E5).

## Chỗ đổi trong B2 (C-d3)

B2 khớp mã gốc ở ba điểm: tiêu chí ứng viên; đường đi qua toàn nút bất thường; điểm là tổng lớn nhất. Các phần ta đổi, đã khai ở B2:
- **nhiều đích:** chạy riêng từng đích, điểm ứng viên lấy max qua các đích; không loại nút đích khỏi tập ứng viên chung. Đây là mở rộng của ta;
- **điểm nút:** K_raw,₁ thay điểm MAD;
- **chu trình:** `UNSUPPORTED_CYCLIC`, tính trượt;
- **không có đích:** `NO_TARGET`, tính trượt.

Đặc tả v1 thêm hai điều, đều theo mã gốc:
- cạnh hợp lệ khi hai đầu bất thường;
- điểm đường gồm cả nút đích.

C-d3 là "quy tắc Traversal chạy trên bằng chứng của ta", không là tái lập phương pháp PetShop.
