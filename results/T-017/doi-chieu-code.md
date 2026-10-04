# Đối chiếu nguồn T-017

Ngày 04/10/2026. Phụ tá nguồn của Codex, không phải người phản biện task. Chỉ ghi trong `D:/RCA-ext/work/T-017/sources-audit/`. Không chạy code tác giả. Không tải hay mở telemetry và kết quả từng ca RE2-TT từ nguồn ngoài.

## 1. Nguồn và cách kiểm

- Ba revision trong T-001 §9 đã lấy bằng GitHub API tree, rồi lấy raw code/config. Revision, URL, dung lượng và hash nằm trong `download-manifest.json`. `git-blob-verification.json` kiểm SHA kiểu Git blob của 70 file đã tải; cả 70 khớp tree. Không tải thư mục `normal_metric/`.
- Zenodo 17105974: lấy metadata, tải đúng hai zip code. Hai MD5 khớp metadata. Tổng hai zip là 1.994.586 byte. Không tải file tar dữ liệu lớn. `zip-inventory.json` lưu tên và dung lượng tất cả entry trước khi chọn code để giải nén.
- Inventory của hai zip lần lượt có 186 và 852 entry. Không có file `.csv`, `.parquet`, `.arrow`, `.pkl`, `.npz`, `.jsonl`, `.log`, `.txt`, `.ipynb`. Không có file tên SimpleRCA. Các đường dẫn tên `result` là code hoặc tài liệu schema/API; không phải đầu ra từng ca. Những kết luận này chỉ nói về hai zip code của 17105974.
- PDF FSE26 lấy qua liên kết PDF trên trang đồng tác giả: `https://yifanyang6.github.io/publications/` → `https://yifanyang6.github.io/assets/pdf/papers/fang2026rethinking-fse.pdf`. Đã đọc toàn bộ 23 trang. Trang đầu ghi DOI `10.1145/3797100`, Article FSE072, July 2026. ACM trực tiếp trả 403; nguồn PDF tác giả có DOI và thông tin xuất bản. PDF, text trích xuất và PNG các trang 5–8 nằm cùng thư mục này. Đã xem trực quan trang 5, 7, 8.
- PDF arXiv v2 đã được root tải trong `D:/RCA-ext/work/T-017/2510.04711v2.pdf`; phụ tá chỉ đọc và trích text vào `arxiv-v2-extracted.txt`.

## 2. Giấy phép

- Cả ba tree GitHub chính xác revision đều không có LICENSE/COPYING. `pyproject.toml` không khai giấy phép. Điều đó chưa đủ để cho phép chép code từ repo này vào bản cài của nhóm. Không có đoạn code nào được chép vào `src/`.
- Metadata Zenodo17105974 ghi CC-BY4.0 cho record. Zip `rcabench-fse-26` có `LICENSE:1–3` Apache2.0. Zip platform không có LICENSE trong inventory, và `pyproject.toml` không khai license. Không suy giấy phép zip backend áp dụng cho repo Simple-RCA khác.
- PDF FSE trang1 ghi CC-BY4.0 cho bài báo.

## 3. Bản FSE26 so với arXiv v2

`compare_papers.py` tạo `paper-comparison.json`, `fse26-table2-simplerca.csv`, `fse26-table3.csv`.

- Table2: toàn bộ 11 dòng SimpleRCA có 7 số mỗi dòng giống arXivv2. Đã kiểm tiêu đề cột bằng PDF. RE2-TT Top@1 vẫn 0,80. Vị trí FSE: PDF trang7; text `fang2026rethinking-fse.txt:352–375`.
- Table3: toàn bộ 12 dòng, gồm All-Dataset, có 7 số mỗi dòng giống arXivv2. Vị trí FSE: PDF trang8; text `:402–418`.
- Đoạn định nghĩa Type giữ nguyên sau khi loại ngắt dòng. Định nghĩa tổng quát xét metric liên quan lỗi **hoặc** số dòng log lỗi; FSE text `:498–505`. Câu chỉ đếm dòng lỗi nằm trong ngữ cảnh riêng RE3-OB, `:538–542`; không thay thế định nghĩa tổng quát.
- Cơ chế ba modality trong §3.1.2 giữ nguyên. FSE bỏ hai câu cuối của arXivv2 về tính cơ bản của luật và việc SimpleRCA dùng làm công cụ khảo sát dataset. Vị trí arXiv text `:212–213`, FSE chuyển thẳng từ log sang §3.1.3 tại `:217`. Không nên trích hai câu đó rồi gán cho bản FSE.
- Bội số trace3, lựa chọn 3sigma/P95 và ngưỡng log vẫn chỉ là ví dụ hoặc lựa chọn chưa được bài chốt đủ. Paper không bổ sung cách xử lý hòa điểm, thiếu service, thiếu baseline hay cách cộng các cảnh báo qua thời gian.

## 4. Đường chạy thật của ba revision

Prefix đường dẫn bảng dưới: `D:/RCA-ext/work/T-017/sources-audit/github/<nhánh>/`.

### orig

- `main.py:5–11` có import lớp SimpleRCA nhưng đăng ký tên `simplerca` cho **NezhaRCA**. `run.py:24` cũng import NezhaRCA. Lớp `NezhaRCA` gọi `NezhaDataAdapter(nezha_rca)` ở `src/simplerca/nezha_rca.py:434–441`.
- Adapter đang dùng đọc sáu parquet normal/abnormal của log, metric, trace (`nezha_adapter.py:26–42`). Với RCABench, nó đổi metric CPU/mem sang phần trăm và chỉ giữ chúng (`:44–47, 98–117`). Adapter này không gọi `get_datapack_labels`.
- Metric: CPU/mem dùng max abnormal > 1,19×P95 normal **và** >80; latency có tên chứa Latency/P9 chỉ cần max >1,19×P95 (`nezha_rca.py:105–162`). Service không có baseline bị bỏ (`:123–125`). Xếp bằng ratio và ưu tiên CPU trước mem trước metric khác (`:178–199`). Đây không phải đếm mọi cảnh báo metric của bài.
- Trace: bỏ frontend; P90 absolute >100ms, lấy top5 (`:215–228`). P90 từ duration nanoseconds đổi sang milliseconds, cần >2 span (`:244–258`). Khi không đủ span, có nhánh dùng duration parent span (`:260–281`); code dùng quan hệ parent-child cho fallback, không xếp hạng bằng đồ thị.
- Log: ưu tiên tăng tỷ lệ level!=INFO >1,5 lần và >10 log abnormal; nếu không có thì dùng giảm log INFO >40% với >40 log normal; cuối cùng đếm level!=INFO (`:289–429`). Bỏ frontend nếu nhiều service có lỗi (`:419–427`). Khác keyword count vượt ngưỡng của bài.
- Tổng hợp: mỗi modality chỉ giữ top5. Điểm rank là5-i; trọng số metric1,2, trace/log1; trả top5 (`:69–93`). Khác tổng số cảnh báo trong bài. Hòa điểm giữ thứ tự chèn; những loop qua set có thể khiến thứ tự hòa không cố định.

### rcaeval

- `main.py:12` vẫn đăng ký NezhaRCA. `nezha_adapter.py:31–38` đọc injection time và metric; chia log/trace trước và sau mốc đó ở `:83–102`. Đây là đường mốc nhãn của chế độ biết trước; không được mang sang chế độ tự phát hiện.
- `nezha_rca.py:49–52` gọi BARO. BARO tách normal/abnormal theo injection time (`baro.py:159–161`); RobustScaler normal rồi lấy max zscore abnormal (`:181–188`). `nezha_rca.py:82–90` lấy max metric mỗi service rồi giữ top5.
- Tổng hợp metric normalize trong top5 thành điểm1,2–6. Chỉ service metric top3 được cộng phiếu trace/log theo rank5-i (`nezha_rca.py:132–160`). Nếu metric rỗng, fallback chỉ vote trace/log (`:112–130`).
- Trace: chung service normal/abnormal, bỏ frontend, P90 ratio>1,2 cộng ratio-1, success-rate drop>0,05 cộng10×drop (`:177–205`); status khác chuỗi `Error` tính success (`:246–269`). Khác P95 ratio3 của bài.
- Log dùng `attr.has_error`, vẫn kiểm có cột level; ba nhánh tăng tỷ lệ lỗi/giảm log/đếm lỗi, `:276–416`. Thiếu level có thể làm log bị bỏ dù `attr.has_error` đã có. Đây là điều kiện schema của code đối chiếu, không phải mặc định trong bài.
- Tên service lấy bằng split tên metric tại underscore đầu tiên (`:82–86`); các service có underscore có nguy cơ bị cắt sai. `baro.py:131–135` điền thiếu backward rồi forward trước khi chia cửa sổ; backward có thể dùng mẫu sau mốc cho mẫu trước mốc. Đây là đường dữ liệu tương lai của code, không phải nhãn nguyên nhân.

### rcaeval_re3_ss

- `nezha_rca.py:50–55` bật `dk_select_useful=True` riêng cho tên dataset RE3-SS; mọi dataset khác false. Đây là lựa chọn theo dataset chưa nêu trong bài.
- Có khác thêm, cần ghi đủ: `time_series.py:101` đổi nhánh `dataset.endswith("ss")` thành `dataset.endswith("sock-shop")`. Vì thế tên `rcaeval_re3_ss` không còn vào nhánh drop_time-only; nó đi qua drop_constant, đổi mem, drop_extra, drop_near_constant và select_useful_cols (`:103–110`). Select_useful chỉ giữ CPU/mem std>1 và lat50 std×1000>10 (`:67–86`). Không chỉ khác một cờ.
- Các luật trace/log/rank còn lại giống rcaeval ngoài dịch dòng do đoạn BARO dài hơn.

### Lớp SimpleRCA riêng trong src/simplerca/main.py

- Nó có thật, nhưng không phải class được registry mặc định gọi. Lớp tại `orig/src/simplerca/main.py:452–459` dùng `DataAdapter(simplerca)`.
- DataAdapter tại `adapter.py:41–51` đọc fault_info và label loại lỗi, `:81–86` lọc metric trong khoảng start/end và `:121–126` truyền fault_type. Code `main.py:37` có tham số đó nhưng không dùng trong thân hàm. Đây là đường nhãn tồn tại của lớp riêng.
- Lớp riêng có metric6sigma và weight100/50/20 (`main.py:304–346, 353–381`), traceP90 và trọng số theo nhánh (`:400–443`). Những mô tả này đúng về lớp riêng, không đúng khi gán thành luật đường chạy `orig` mặc định.
- Static syntax check bằng AST của tất cả `.py` đã tải không phát hiện SyntaxError (`static-syntax-check.json`). Điều này không chứng minh code chạy được hay đúng; không import/chạy code tác giả.

## 5. Hai đính chính T-001 có bằng chứng

1. `results/T-001/danh-sach-phuong-phap.md:106` gán luật6sigma/weight100/50/20 và DataAdapter nhãn cho nhánh orig mà không phân biệt lớp riêng với CLI mặc định. `:138` L4 cũng cần ghi đường nhãn này thuộc lớp riêng chưa đăng ký. Bằng chứng: orig `main.py:11`, `run.py:24`, `nezha_rca.py:434–441`, `nezha_adapter.py:26–58`. Đề xuất thay mô tả orig bằng đường NezhaRCA nêu trên, đồng thời giữ đường DataAdapter như một lựa chọn code riêng. Kết luận M4 vẫn được hỗ trợ vì đường CLI orig cũng khác §3.1.2. Nguyên nhân khả thi khác: tác giả có thể từng gọi lớp riêng hoặc revision khác để tạo Table2; task này chưa xác định được code sinh Table2.
2. `results/T-001/danh-sach-phuong-phap.md:188` nói chung luật Type chỉ đếm dòng lỗi. Đề xuất: “Luật Type xét metric liên quan lỗi hoặc số dòng log lỗi vượt ngưỡng; riêng đoạn nói về RE3-OB nêu hạn chế chỉ đếm error entries.” Bằng chứng PDF FSE trang8–9, text `:498–505, 538–542`, và arXivv2 cùng định nghĩa. Kết luận Type là luật phân loại riêng, không phải output SimpleRCA vẫn giữ; đánh giá độ khó hoặc đầu vào luật Type bị ảnh hưởng nếu bỏ metric. Không tự tính Type trên dataset mới.

Không sửa file task cũ. Đã triển khai kiểm revision/blob và script so sánh PDF trong thư mục này.

## 6. Artifact FSE mới: trạng thái kiểm ban đầu, bổ sung tại mục 8

**Ghi chú cập nhật:** đoạn dưới giữ lại diễn biến ban đầu của audit; mục 8 đã hoàn thành kiểm inventory/code/lọc kết quả được phép. Giới hạn bàn giao là không có kết quả 30dev RE2-TT trong nguồn đã kiểm, không còn là chưa kiểm artifact vì trộn dataset.

FSE ref[19] tại text `:1693–1694` trỏ concept Zenodo19494725. API concept resolve tới record19522409 (version index4), title artifact của bài. Metadata lưu `zenodo-fse-record19494725.json`; licenseApache2.0. Có một archive `FSE_26_RCA_dataset_study_reviewer.tar.gz`, 91.418.171 byte. Description nêu reduced benchmark, scripts, reviewer outputs và paper assets.

Không tải archive. Chưa biết archive có chứa RE2-TT ngoài30dev hay không. Không thể dùng archive trộn telemetry làm nguồn kết quả từng ca mà chưa có inventory an toàn và bộ lọc trước khi đọc. Giả định không có kết quả per-case ngoài hai zip cũ có thể sai tại artifact mới này. Đầu vào cần để kiểm: inventory hoặc kết quả được tác giả cung cấp riêng, lọc theo allowlist30dev trước khi mở/in. Vì vậy không kết luận toàn bộ artifact FSE không có code SimpleRCA hoặc không có kết quả từng ca.

## 7. Giới hạn kết luận và việc đã lưu

- Chưa xác định revision nào tạo Table2. M4 cài từ mô tả bài sẽ phản ánh lựa chọn lấp phần bài để ngỏ. Trùng hoặc lệch0,80 có thể do khác telemetry/schema, mốc/cửa sổ, tham số, code sinh bảng hoặc tập30dev/90full. Không quy một nguyên nhân khi chưa kiểm.
- Không mở locked, không EC2, không chạy phương pháp, không ghi file repo, không commit/push/gửi tin ngoài.
- Có ba lần kiểm đọc/trích nguồn thất bại được giữ bằng ghi chú: đọc UTF8 qua stdout Windows mặc định lỗi decode rồi lỗi encode; parser Table2 ban đầu bắt thêm hai dòng prose bắt đầu SimpleRCA và assert thất bại. Đã đổi stdout UTF8 và chỉ giữ dòng có số; lượt parser sửa đạt. Không có lượt chạy phương pháp tác giả.
- Root cần chép dữ kiện và đề xuất đính chính cần thiết vào kết quả repo T-017; scratch này không thay nguồn sự thật trong repo.

## 8. Bổ sung: dùng lại artifact FSE mới đã có từ T-012

Root yêu cầu kiểm tiếp bằng nguồn local. Tìm được archive 91 MB đúng record 19522409 tại `D:/RCA-flashticket/data/ngoai-rcaeval/T-012/fse/FSE_26_RCA_dataset_study_reviewer.tar.gz`. Không tải thêm. Hash compressed archive tự tính lại khớp MD5 Zenodo; lưu `fse-new-artifact-local-check.json`.

Inventory T-012 tại `results/T-012/runs/fse-file-inspect-003/members.json` có 3519 entry. Chỉ đọc tên, kích thước và hash metadata trước khi chọn. Không có đường dẫn chứa re2tt/re2_tt/re2-tt. Những entry có rcaeval là code platform hoặc CausalRCA. Script `inspect_fse_reuse.py` chỉ trích code/config SimpleRCA, LICENSE root và tài liệu/scripts reviewer; từng file khớp hash T-012. Không trích telemetry và kết quả từng ca.

21 file code/config SimpleRCA trong artifact mới **giống từng byte** snapshot orig đã kiểm. Manifest `fse-new-artifact-code-comparison.json` lưu từng phép so. Vì vậy artifact mới có code SimpleRCA, nhưng không bổ sung một bản khớp cơ chế §3.1.2. Script reviewer `fse-artifact-reused/scripts/run_experiment_bundle.sh:151–154` gọi chính `vendor/algorithms/simplerca/main.py` với dataset rcabench; entrypoint trong đó vẫn NezhaRCA tại `fse-artifact-reused/vendor/algorithms/simplerca/main.py:11`.

Tài liệu artifact mô tả 10 ca reviewer RCABench: `fse-artifact-reused/README.md:17, 120–123, 172–173`, `artifacts/reproduction_report/README.md:8, 22–23`. Tài liệu nói số reviewer là các bảng/hình mẫu, không phải tái lập full dataset. Phần full replay mặc định cũng rcabench_filtered (`scripts/full_reproduction.sh:19`), không phải RE2-TT.

Còn có hai file tổng hợp có thể chứa kết quả từng ca, nên đã kiểm đủ phần được phép bằng script riêng `filter_fse_artifact_results.py`, dùng pyarrow 17 của môi trường T-017:

- `artifacts/reproduction_report/datapack.perf.parquet`: footer ghi 120 dòng, schema có dataset/datapack. Metadata min=max của dataset là `rcabench`. Đọc bằng predicate Arrow `datapack in allowlist30dev`, hỗ trợ cả tên có/không prefix re2tt_. Kết quả 0 dòng.
- `src/raw_data/algo_perf.parquet`: footer ghi 170 dòng, schema có dataset/datapack. Metadata min=max của dataset là `rcabench_scalabiltity_v2` (giữ đúng chính tả nguồn). Cùng predicate trước khi trả dòng: 0 dòng.
- Hai file `dataset.perf.parquet` và `fault_types.perf.parquet`: chỉ đọc footer/schema; không có case identity để làm đối chiếu từng ca. Không đọc giá trị kết quả của chúng.
- `fse-artifact-result-filter-check.json` lưu schema, số dòng footer, metadata dataset, predicate và số dòng đã lọc. Không in/lưu dòng ngoài allowlist, không mở telemetry.

Kết luận cập nhật: đã kiểm inventory, code và hai nguồn tổng hợp kết quả từng ca của artifact FSE mới; không tìm thấy kết quả của 30 ca dev RE2-TT để đối chiếu Table 2. Không còn lý do ghi “chưa kiểm artifact vì trộn dataset” cho các kiểm này. Không khẳng định không tồn tại kết quả ở nguồn tác giả khác; task này chưa xác định code/revision sinh Table 2 hay kết quả full 90 ca.

Các file bổ sung đều trong sources-audit. Có lượt kiểm import pyarrow bằng bundled Python không đạt do thiếu gói; đổi sang môi trường T-017 đã có pyarrow 17, kiểm footer/filter đạt. Lỗi wildcard rg Windows chỉ ảnh hưởng lệnh tìm script; đã chạy lại với `-g '*.sh'` đúng. Không có lượt chạy phương pháp mới.
