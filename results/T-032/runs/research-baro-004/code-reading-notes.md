# T-032 — đọc code và chuẩn bị chuỗi BARO

Vai trò: trợ giúp người làm. Đây không phải bản phản biện chính thức, báo cáo
cơ chế hoàn chỉnh hay quyết định thiết kế mới. Chỉ chuẩn bị trình đọc trung gian
đã phát lại khớp; chưa chạy trình đọc trên EC2. Các hash và danh sách 52 ca nằm
trong `plan.json`. Không chạy native, không đọc raw dataset trên laptop.

## Nguồn code và chuỗi cần lần theo

Đã đọc bản code có byte hash trùng pin trong `capture-start.json#/sources`:

| Bước | Nguồn đã đọc | Điều code thực sự làm |
|---|---|---|
| Tiền xử lý đầu vào | `src/p3/cua_so.py:72`, `:91` | Trong cửa sổ đã cắt: bỏ `time.1` và `_latency-50`; thay vô cực bằng thiếu; forward fill rồi điền 0; đổi `_latency-90` thành `_latency`. Không tự khôi phục quan sát bị thiếu. |
| Adapter | `src/p3/adapters/baro.py:9`, `:14`, `:29` | Chuẩn bị input, gọi native, rồi dựng khóa bằng các lời gọi cùng công thức. Chuỗi quan sát phải giữ cả native và lần dựng khóa có sẵn. Adapter truyền `dataset='re2-tt'`, `dk_select_useful=False`, kể cả đầu vào Nezha đã đổi dạng. |
| N/A và lọc | `D:/RCA-ext/src/RCAEval/RCAEval/e2e/baro.py:19`; `RCAEval/io/time_series.py:4`, `:45`, `:99` | Chia N/A tại marker adapter. Mỗi phía bỏ time, bỏ cột constant riêng, chia mem cho một triệu. Sau đó chỉ giữ giao cột theo thứ tự N. Giao này có thể làm mất cột root; phải xem cột thực tế trước/sau, không suy từ số cột. |
| Chuẩn hóa và điểm metric | `RCAEval/e2e/baro.py:45` | Fit `RobustScaler()` trên N từng metric, transform A, lấy `max(z)` có dấu. Không lấy trị tuyệt đối, không lấy trung bình hay mức kéo dài. |
| Ánh xạ và điểm service | `src/p3/ban_ghi.py:7`, `:19` | Entity là tiền tố trước `_` đầu. Khóa entity bằng khóa metric lớn nhất; hòa theo bằng nhau đúng giá trị, hiển thị giữ thứ tự xuất hiện đầu. Cần chỉ mọi metric cùng đạt max, không chỉ metric latency. |

Đường ngoài repo ở trên là checkout phương pháp đúng revision, chỉ đọc code;
không phải repo RCA lưu trữ. Trình đọc trên EC2 sẽ kiểm lại code đang nằm tại
đường runtime đã được observer ghi, gồm sklearn. Nội dung sklearn `_data.py`
đúng pin EC2 chưa được đọc trực tiếp ở bước chuẩn bị trên laptop; không tự đặt
ngưỡng “gần zero”. Trung gian có `effective_scale.entry.scale` (IQR thô),
`effective_scale.return` (mẫu số thật), `constant_mask`, `fit.scaler.center_`,
`fit.scaler.scale_` và quantile đã lưu. Vì vậy phải phân biệt IQR thô với mẫu số
hiệu dụng và dùng trạng thái fallback thực đã quan sát.

Native BARO trong hàm này chỉ tính trên metric. Các cạnh/caller của T-028 là
ngữ cảnh phân tích sau tính toán, không là đầu vào của bước chấm BARO. Điều này
chưa cho biết đồ thị mới có lợi, cũng chưa chứng minh caller chờ root.

## Phạm vi nguồn và đối chứng

`plan.json#/cases` giữ đủ 30 RE2-TT và 22 Nezha-OB, mỗi ca có check được pin,
bản ghi đóng băng được pin, cửa sổ F nguyên bản và pin code quan sát. Nguồn cờ
chỉ lấy `results/T-028/runs/phan-hoi-review-001/ca-sai.json` sau kiểm manifest.
Các con trỏ là `/main_rows/i/evidence/seed_evidence/single` và:

- `caller_relation`: quan hệ analysis context theo từng entity;
- `ancestors` và `certain_before_root`: tập nguồn, không suy từ tên metric;
- `by_k/*/P0` và `by_k/*/flags`: giữ endpoint và định nghĩa nguồn;
- `mechanisms/*/explanation_flags_wrong_seeds/M5`: khóa mẫu số M5 union.

Mười ca M5 BARO ở các hàng 19, 20, 26, 182, 188, 189, 192, 193, 197, 200 của
nguồn trên. Danh sách theo ca/k nằm trong plan; không cộng hai k thành hai ca.
Ba ca thuộc RE2, bảy ca thuộc Nezha. Trình đọc phải dừng nếu mẫu số đổi.

Đối chứng lấy nguyên lựa chọn đã khóa trong `bao-phu-nhom.json`. Không chọn
lại bằng điểm, caller, margin hoặc kết quả can thiệp. Giữ toàn bộ lớp điều kiện
đã lưu; ưu tiên cùng cell rồi cùng channels là thứ tự đọc. Opaque ID chỉ phá hòa
trong lớp metadata thực sự tương đương. Đối chứng khác lớp giữ riêng. Đọc code
và một cặp không chứng nhận mọi ca hay mọi lớp; trạng thái đọc tay vẫn chưa làm.

## Schema đầu ra trình đọc

Chỉ root chạy `research_baro_chain_v1.py` trên EC2. Trình không import native,
adapter, sklearn hay loader. Nó hash toàn bộ artifact manifest của từng ca và
kiểm lại các field replay nguyên bản trước khi xuất bằng chứng. Nó đọc JSON
observer; các bảng parquet giữ thành con trỏ đã hash và đã được capture audit
của lượt exact kiểm. Không refit, không thêm phép chạy BARO.

Đầu ra mới trong `runs/research-baro-004/execution-*/baro-saved-chains.json`:

- `/cases/*/column_stages`: cột prepared, N, A, giao và cột bị bỏ ở mỗi bước;
- `/cases/*/metric_chains`: median, Q25/Q75, IQR thô, mẫu số hiệu dụng, fallback,
  signed max robust-z, vị trí/thời điểm marker, giá trị tại max, số mẫu và con trỏ
  fit/scale/transform/score. Kiểm scalar của các vị trí max đúng tuyệt đối;
- `/cases/*/entity_ranking` và `/root_score_chain`: khóa service/hòa và tất cả
  metric thắng. Kiểm max metric → service khớp tuyệt đối bản ghi đóng băng;
- `/cases/*/caller_root_observations`: mọi ancestor caller có đường đến root
  trong nguồn, chuỗi hai phía, caller chắc chắn trên root và margin có dấu;
- `/M5_caller_root`: đủ 10 ca union, không phải chỉ 10 caller;
- `/locked_controls`: nguyên 33 yêu cầu cặp theo k và tất cả lớp đối chứng,
  trỏ đến chuỗi ca đầy đủ; vẫn chưa có kết luận đọc tay;
- `manifest.json`, `progress.jsonl`, `status.json` hoặc `failure.json` riêng lượt.

Giữ riêng F thời gian nguồn và `native_parameters`/`time_axis_semantics`.
Nezha metric đã đổi thành 5N+5A theo chỉ số thứ tự, không phải các mẫu đồng thời.
Không ánh xạ vị trí max theo thứ tự thành thời điểm span chờ.

Lỗi hash, khớp nguồn, ánh xạ, số học hay mẫu số sẽ dừng toàn trình đọc. Giữ
thư mục lỗi; không tăng tolerance, không xuất ca lỗi làm bằng chứng. Chưa có
kiểm runtime/fixture của trình mới; đã kiểm AST và chuẩn bị pin metadata. Root
cần đọc đầy đủ script, chạy EC2 và kiểm lượt đầu trước dùng đầu ra. Ước lượng
chưa đo trong plan là chi phí hash/đọc JSON, không dự toán tính lại phương pháp.

## Giải thích cần phân xử tiếp

Chuỗi số có thể chỉ được metric nào thắng, numerator và denominator nào tạo
điểm, hoặc bước nào bỏ cột. Muốn gọi đó là hạn chế riêng của nhóm sai phải đọc
các đối chứng đã khóa và xét input/coverage tương ứng. Không tự chọn “IQR nhỏ”
làm nguyên nhân chỉ vì điểm lớn: có thể numerator lớn, fallback, max trên metric
khác hoặc nhiều yếu tố cùng tác động. Trình chỉ phơi các đại lượng thực để đọc.

Caller tự bất thường, tải/nguyên nhân chung, caller chờ downstream và semantics
đầu vào chưa được phân biệt bằng max metric. Các giả thuyết vật lý cần trace
semantics, clock/coverage và bằng chứng wait/await có hiệu lực. Tập quan hệ phân
tích và hình học child span không thay thế bằng chứng đó. Lợi ích đồ thị mới
và kết luận “lan đáng kể” chưa được kiểm trong phần chuẩn bị này.
