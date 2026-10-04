# K1 C.6: tách threshold của paper khỏi output của code

Đích đề xuất: `docs/knowledge/K1-phuong-phap-rca.md:206`. Không sửa K1 trong T-014. Đây là làm rõ cách thực thi, không quy câu cũ thành một câu không có nguồn trong paper.

## Bằng chứng

Paper CIRCA §4.3, trang4, có lời mô tả loại metric s<3 khỏi root-cause indicators, theo three-sigma rule. Nó tiếp tục giải thích các metric đó vẫn gom child evidence để chuyển tới ancestor candidates. Vì vậy cutoff3 cho abnormal/root-candidate concept thật sự có trong paper. Nguồn: `KDD22-CIRCA.pdf`, `page-4.png`; [bài chính thức](https://netman.aiops.org/wp-content/uploads/2022/08/KDD22-CIRCA.pdf).

Algorithm2, trang5, kiểm child score<3 ở dòng5 để gom evidence xuyên child; dòng11 kiểm ngưỡng trước khi tăng score ở dòng12. Pseudocode không có một thao tác filter/delete output candidates hay một bước tạo ranking. Nó chỉ gán s′ khi điều kiện thỏa, không viết nhánh else, và dòng11 dùng ký hiệu j dù vòng hiện tại là i. Vì vậy không dùng pseudocode này để kết luận chắc chắn danh sách output giữ hay bỏ mọi metric dưới3. Lời mô tả exclusion trong §4.3 vẫn phải được ghi đúng, thay vì xóa khỏi hồ sơ.

Code CIRCA revision0215e18 cho câu trả lời rõ về output:

- `circa/alg/ci/__init__.py:143–145`: child score<θ thì thêm evidence của child đã gom.
- Dòng149–155: chỉ node score≥θ nhận thêm maximum child evidence; không xóa node dướiθ.
- Dòng157–160: gán key cho mọi score rồi trả nguyên dictionary.
- `circa/alg/common.py:219–225`: xếp toàn bộ `scores.items()`, không lọc theo3.
- Lớp DAScorer defaultθ=0 ở dòng111; cấu hình RHTDAGetter dùngθ=3 tại `circa/experiment/comparison/models.py:629–634`. RHT-only không có bước cutoff3.

RCAEval có cùng logic DA tại `RCAEval/graph_heads/rht.py:254–287`; wrapper chính khởi tạo RHT-only tại dòng345, không gọi DA. Nó cũng không cung cấp incident detector.

Fixture bằng code chính thức giữ b có score1 trong cả DAG và cycle (`../audit/da-cycle.json`). Snapshot RE2-TT kiến trúc giữ đủ272 scored metrics, trong đó chỉ64 có RHT≥3 (`../runs/example-architecture/interpretation.json`). Đây là bằng chứng output thật, không suy từ việc tiến trình không lỗi. Thống kê dưới/ngang ngưỡng dùng mô tả thực thi, không benchmark hiệu quả.

## Đoạn cũ → đoạn mới

Đoạn cũ, nguyên văn K1 dòng206:

> - **Detector/score.** **NO SEPARATE ANOMALY DETECTOR**. Mỗi metric regression theo graph parents trên reference window; residual giả định Gaussian, chuẩn hóa và lấy maximum trong test interval. Cutoff cố định `3` lọc candidate. Graph trực tiếp quyết định parent set nên đổi graph có thể đổi score.

Đoạn mới đề xuất, nguyên văn:

> - **Detector/score.** **NO SEPARATE ANOMALY DETECTOR**. Mỗi metric regression theo graph parents trên reference window; residual giả định Gaussian i.i.d., chuẩn hóa và lấy maximum trong test interval. Paper §4.3 gọi các metric score dưới `3` là không thuộc root-cause indicators. Trong code CIRCA, cấu hình RHT+DA dùng ngưỡng `3` để quyết node nào nhận thêm child score và node nào truyền descendant evidence; code vẫn xếp mọi scored metric, không lọc output bằng ngưỡng này. RHT-only không có cutoff `3`. Ngưỡng này không phải incident detector. Graph trực tiếp quyết định parent set nên đổi graph có thể đổi score.

Lý do: câu cũ có thể được hiểu rằng code trả một candidate set đã lọc3 hoặc dùng3 để phát hiện incident. Hai cách hiểu đó không khớp code. Cách hiểu câu cũ chỉ mô tả abnormal-candidate concept của paper có nguồn, nên cần phân biệt phạm vi thay vì phủ nhận paper.

Kết luận phụ thuộc: universe dùng để đánh giá metric/service; ý nghĩa control normal/normal; yêu cầu có external detector khi triển khai; số nodes được giữ ở RHT/DA; không coi top1 từ ranker luôn là một incident/root có nghĩa. Không suy rằng score<3 chứng minh vô can: θ là heuristic của DA, không bảo đảm nhân quả trên mọi dữ liệu.
