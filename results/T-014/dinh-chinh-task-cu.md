# VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM

Không sửa task cũ. Các điểm dưới đã có bằng chứng và triển khai ở T-014; không tự thay số đã phản biện. Phạm vi soi T000–T012 ở audit/coverage-task-cu.csv: census Markdown, đọc sâu các kết luận CIRCA/chấm/fallback liên quan; không claim audit toàn artifact của mọi phương pháp.


### N1 — T-001 diễn đạt sai xử lý tên cột

- File: `results/T-001/danh-sach-phuong-phap.md:60`.
- Cũ: `tên cột dạng service_metric, cột khác dạng bị bỏ im lặng`.
- Sai gì: tên không có dấu `_` không bị bỏ; `rht.py:308` truy cập token thứ hai rồi ném `IndexError`. Wrapper có thể trả thứ tự cột. Tên có nhiều dấu `_` bị cắt hai token, tạo đường chập nút/bỏ dữ liệu khác.
- Bằng chứng: `synthetic.json` ghi lỗi `IndexError: list index out of range` khi gọi `rht()` trực tiếp với cột `cpu`. Code `e2e/__init__.py:22–35` thể hiện nhánh dự phòng.
- Ảnh hưởng: yêu cầu định dạng đầu vào và phép kiểm nhánh dự phòng. Không suy thành lỗi điểm T-006 vì hai ca vừa chạy dùng tên tương thích.
- Đã triển khai: fixture trên scorer chính thức; lưu lỗi thật. Không sửa T-001.
- Đề xuất mới: `tên cột phải tách được đúng service_metric; cột không có '_' làm hàm lỗi và wrapper có thể trả thứ tự cột. Tên có nhiều '_' bị cắt hai token, có thể chập nút hoặc thiếu dữ liệu; adapter phải kiểm tính tương thích trước gọi.`

### N2 — T-006 nói rộng hơn phạm vi kiểm hashseed

- File: `results/T-006/kiem-dung-dan.md:186,216`.
- Cũ: `Thứ tự nút do hash: không đổi top 5` và `top 5 giữ nguyên ở 6 seed, nên Avg@5 không đổi`.
- Sai gì: script `results/T-006/scripts/soi_circa_hashseed.py:khac[:4]` chỉ kiểm bốn ca trong 15 ca có ranking khác. Log `runs/25-soi-circa-hashseed.log` xác nhận bốn ca. Hai lượt chính thức trên 90 ca có cùng điểm từng ô, nhưng đó là bằng chứng khác, không chứng minh mọi seed giữ top5 ở cả 90 ca.
- Ảnh hưởng: phạm vi kết luận tính tất định; không làm thay đổi các số đã chấm của hai lượt chính thức.
- Đã triển khai: kiểm script và log thật; tái lập điểm không nhãn trên hai ca ở §1. Không đổi seed hay benchmark thêm cả dataset.
- Đề xuất mới: `Ở bốn ca được kiểm với sáu hashseed, top5 giữ nguyên. Hai lượt chính thức trên 90 ca cho cùng điểm từng ô. Chưa kiểm mọi hashseed trên tất cả ca; không suy kết quả bốn ca thành bảo đảm tất định toàn dataset.`

### N3 — T-001/T-006 thiếu thông tin tập ứng viên thật của CIRCA-PC

- Nơi cần bổ sung: `results/T-001/danh-sach-phuong-phap.md:60`, `results/T-006/kiem-dung-dan.md:160–168`.
- Thiếu gì: mô tả không cho biết metric PC cô lập bị loại khỏi candidate, đồ thị rỗng có thể trả ranking rỗng dù không có exception. Không khẳng định các con số T-006 sai chỉ vì thiếu mô tả.
- Bằng chứng và triển khai: §1–2 và ba fixture/JSON. Tại CPU/1 và MEM/1, candidate cũ đúng là subset sau loại cô lập.
- Ảnh hưởng: đơn vị/tập xếp hạng và kết luận đầu vào. Khi đổi nguồn đồ thị cần báo cả số metric vào PC, node graph và metric scored; không coi graph khác là chỉ đổi parents nếu candidate cũng khác.
- Đề xuất bổ sung nguyên văn: `CIRCA-PC RCAEval chỉ thêm cạnh khi dựng MemoryGraph; metric không có cạnh PC không được chấm. PC rỗng có thể cho ranking rỗng mà không ném lỗi. Tập metric sau preprocess và tập ứng viên được chấm có thể khác nhau; lưu cả hai để diễn giải kết quả.`

### N4 — Các hồ sơ cũ thiếu lỗi đảo chiều cạnh PC có hướng

- File: `results/T-001/danh-sach-phuong-phap.md:60`; `results/T-006/kiem-dung-dan.md:160–166` mô tả PC+RHT nhưng không báo ngữ nghĩa chiều bị đổi.
- Sai/thiếu gì: `rht.py:318–343` rồi `graph.reverse()` làm cạnh GeneralGraph a→b thành b→a. Do RHT hồi quy trên parents, đây là đổi mô hình chấm điểm, không chỉ đổi cách hiển thị graph.
- Bằng chứng: `check_direction.py`, `direction.json`; actual GeneralGraph ma trận[-1,1], actual graph nhận cạnh ngược. Trên MEM/1, cấu hình sửa chiều nhưng giữ node làm hạng service2→1 (`r-comparison-summary.json`).
- Ảnh hưởng: mô tả code khác bài và khả năng diễn giải cha/con; không sửa số T-006 và không gọi lỗi này là nguyên nhân đủ của ô0,148.
- Đã triển khai: fixture actual API; so graph/scorer không nhãn trên hai ca; target MEM25 thêm nguồn graph R gốc, lưu mọi variant. Không sửa file task cũ.
- Đề xuất thêm: `Đường chuyển adjacency của rht đảo chiều cạnh PC đã có hướng so với GeneralGraph của causal-learn. RHT thật dùng parents của graph sau đảo chiều. Tách lỗi ngữ nghĩa này khỏi việc cạnh vô hướng thành hai chiều và khỏi sai khác backend PC; chưa quy toàn bộ chênh số công bố cho nó.`

### N5 — “Chỉ khác graph/DA” là mô tả thiếu cấu hình paper

- File: `results/T-001/danh-sach-phuong-phap.md:60` (`khác bài ở hai thành phần: đồ thị và DA`); `results/T-005/do-kha-thi.md:61` (`chỉ khác bước dựng đồ thị`).
- Thiếu gì: default lớp RHT là linear, nhưng prior-work real/Oracle config của CIRCA dùng SVR(sigmoid); structural canonical còn dùng DA. Khi gọi biến thể “như bài gốc”, không được suy chỉ thay graph mà các thành phần còn lại tương đương.
- Bằng chứng: config whitelist cuối artifact ở `source/updated-config/params-oracle-run.json`; factory pin `models.py:580–586,630`; lớp default `alg/ci/anm.py:18–20`. Nguồn bài/hồ sơ riêng của T-014 xác định SVR+DA trên real/Oracle. Artifact cập nhật khác revision pin, nên giữ ranh giới nguồn.
- Ảnh hưởng: yêu cầu đầu vào, lựa chọn RHT/RHT+DA và diễn giải so hai biến thể; không phủ nhận có thể dựng một adaptation kiến trúc dùng chung linearRHT nếu ghi rõ đó là lựa chọn của task.
- Đã triển khai: cùng25Rgraph kiểm riêng linear/SVR/DA, lưu từng điểm/params/rank; không chọn từ điểm. So samegraph hai ca đã xác nhận scorer linear gốc và RE khớp.
- Đề xuất đoạn mới: `CIRCA-PC RCAEval dùng causal-learn và linear RHT, không DA. Bản structural theo real/Oracle prior work dùng SVR(sigmoid)+DA(threshold3); đổi graph đơn thuần tạo adaptation dùng chung scorer nhưng chưa phải cùng cấu hình paper. Hồ sơ cần ghi thêm cửa sổ, xử lý node cô lập và ngữ nghĩa chiều cạnh.`


## Làm rõ K1 của T-000

Xem paper/dinh-chinh-k1-threshold.md: paper thật có concept loại dưới3; implementation giữ mọi scored metric. Đây là tách phạm vi paper/code, không phủ nhận nguồn câu cũ. Đoạn cũ→mới nguyên văn và kết luận phụ thuộc đã được đưa vào de-xuat-tai-lieu-chung.md.

Bổ sung bằng chứng N3/N4 khi tiếp tục T014: kiểm75lượt scorer mới trên25Rgraphcached, độc lậpđếm100config. Giữ/bỏisolate đềuAvg5=.864 theochiềugốc và.896 khiđảochiều. N4 là lỗi ngữ nghĩa đã có ảnh hưởng thực; N3 là lỗi mấtứngviên nhưng chưa giải thíchaggregate ôMEM này. Không suy riêngbackend hoặc bỏisolate giải thích hết.148. Evidence: audit/graph-factor-summary.json vàgraph-factor-verification.json; cácđềxuấtsửa taskcũ giữ nguyên, chỉ bổ sung giới hạn kết luận này.
