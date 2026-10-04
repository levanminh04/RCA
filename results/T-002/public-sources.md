# Nguồn công khai và số đếm RCAEval — T-002

Đọc ngày 02/10/2026. Phần này chỉ kiểm danh sách thư mục/file công khai và tài liệu của tác giả. Không đọc `cases.parquet`, không tải telemetry mới, không mở dữ liệu bị khóa. URL, revision, kích thước tải và hash của từng nguồn nằm trong `public-metadata/run-002/source-manifest.json`; trạng thái lượt chạy nằm trong `public-metadata/run-002/run.json`.

## Nguồn và cách tái lập

| Nguồn | Bản đã lưu | Dùng để kiểm |
|---|---|---|
| HF tree API của revision ghi trong `data/README.md` | `public-metadata/run-002/sources/hf-tree-page-001.json` đến `-003.json`; bản gộp `hf-tree.json` | Số thư mục ca, nhãn trong tên ca, file có mặt và số byte công bố |
| HF dataset card cùng revision | `public-metadata/run-002/sources/hf-README.md` | Quy ước tên thư mục, nhãn, giấy phép, chú thích dữ liệu |
| GitHub README và LICENSE, khóa theo commit API trả về | `public-metadata/run-002/sources/github-README.md`, `github-LICENSE`, `github-main-commit.json` | Đối chiếu dataset card và giấy phép |
| Bài RCAEval, bản v2 | `public-metadata/run-002/sources/paper-v2.html` | Mô tả hệ thống, lỗi, stack thu thập, khoảng bình thường |

Lệnh cuối: `py -3 results/T-002/fetch_public_metadata.py --output results/T-002/public-metadata/run-002`. Lượt đầu giữ ở `public-metadata/run-001`; lượt thứ hai sửa đường dẫn artifact trong manifest để nó trỏ đủ từ thư mục lượt. Số đếm hai lượt giống hệt. Muốn tái lập, dùng thư mục lượt mới; script từ chối ghi đè lượt cũ. Script dùng Python standard library (thư viện chuẩn), chỉ tải tree API và tài liệu nhỏ. Tổng dữ liệu tải mỗi lượt: 785.725 byte. Ba trang API có tổng 2.815 mục, gồm 735 thư mục ca; tất cả tên thư mục ca khớp quy ước công bố. Không dùng nhãn này làm đầu vào phương pháp RCA.

Kiểm sau chạy ở `public-metadata/run-002/verification.json`: hash và số byte tất cả snapshot khớp manifest; đường dẫn tree không trùng; số dòng ca, tổng theo root/fault/ô khớp bảng; cú pháp script hợp lệ. Không mở dữ liệu cục bộ trong kiểm này.

## Số đếm từ tên thư mục

**FACT đo từ metadata:** số liệu bên dưới được sinh từ `public-metadata/run-002/count-summary.json`; từng ca ở `cases-from-directories.csv`, từng ô ở `root-fault-cells.csv`, số byte theo modality (nguồn tín hiệu) ở `modality-sizes.csv`.

| Bộ | Ca | Service gốc | Loại lỗi | Ô gốc × lỗi có ca / số ô có thể | Lặp mỗi ô | Dung lượng file công bố, MB thập phân |
|---|---:|---:|---:|---:|---|---:|
| RE2-TT | 90 | 5 | 6 | 30/30 | 3 | 1.965,748 |
| RE2-OB | 90 | 5 | 6 | 30/30 | 3 | 922,485 |
| RE3-TT | 30 | 2 | 4 | 8/8 | 3–6 | 161,390 |
| RE3-OB | 30 | 4 | 5 | 10/20 | 3 | 138,130 |

- RE2-TT: `ts-auth-service`, `ts-order-service`, `ts-route-service`, `ts-train-service`, `ts-travel-service`; mỗi root 18 ca. Các lỗi `cpu`, `mem`, `disk`, `socket`, `delay`, `loss`; mỗi loại 15 ca.
- RE2-OB: `checkoutservice`, `currencyservice`, `emailservice`, `productcatalogservice`, `recommendationservice`; mỗi root 18 ca. Cùng sáu mã lỗi và số ca từng lỗi như RE2-TT.
- RE3-TT: `ts-auth-service` và `ts-route-service`; mỗi root 15 ca. `f1`: 7; `f2`: 7; `f3`: 10; `f4`: 6. Ô `ts-route-service × f3` có 6 lần lặp, các ô khác có 3 hoặc 4.
- RE3-OB: `adservice`: 9; `cartservice`: 3; `currencyservice`: 3; `emailservice`: 15. `f1`: 9; `f2`: 3; `f3`: 6; `f4`: 6; `f5`: 6. Có 10 ô được quan sát trong tích Descartes 4 × 5; các ô không có ca không được coi là ca thất bại.

Các kích thước trên là tổng `size` API của file trong các thư mục ca, gồm cả `inject_time.txt`; không gồm dataset card, index toàn bộ hay metadata tải trong task. Chúng là kích thước file Parquet công bố, không phải bộ nhớ RAM khi mở.

| Bộ | metrics.parquet | traces.parquet | logs.parquet | inject_time.txt |
|---|---:|---:|---:|---:|
| RE2-TT | 90 | 90 | 89 | 90 |
| RE2-OB | 90 | 90 | 90 | 90 |
| RE3-TT | 30 | 30 | 30 | 30 |
| RE3-OB | 30 | 30 | 30 | 30 |

RE2-TT thiếu file log ở `re2tt_ts-auth-service_cpu_1`; HF card có cùng chú thích. File có mặt chỉ xác nhận tính sẵn có, không chứng minh file có hàng hợp lệ hay đủ liên kết span; phần đó cần đọc schema và đo trên mẫu được phép.

## Nội dung tài liệu và điểm không khớp

**FACT công bố:** Bài v2 §3.1: Online Boutique dùng gRPC; Train Ticket có giao tiếp đồng bộ và bất đồng bộ. §3.2: resource faults gồm CPU hog, MEM leak, DISK stress, SOCKET stress; network faults gồm DELAY và LOSS; code faults F1–F5 lần lượt là sai giá trị tham số, thiếu tham số, thiếu lời gọi hàm, sai giá trị trả về, thiếu xử lý ngoại lệ. §3.3: Kubernetes; stress-ng/tc; Prometheus, cAdvisor, Istio; Vector, Loki, Elasticsearch; Jaeger. Tải ngẫu nhiên 10–200 requests/s; thu bình thường 10 phút trước tiêm. Mô tả không thay cho đo từng ca.

**FACT nguồn giấy phép:** HF card khai báo MIT. GitHub LICENSE là MIT, cho phép sử dụng/sửa/phân phối khi giữ thông báo bản quyền và giấy phép.

**FACT nguồn nhãn:** HF card nêu tên thư mục chứa ground truth service gốc và lỗi; `inject_time.txt` là Unix timestamp lúc tiêm. Index công bố thêm root, fault, repetition, inject_time và số đo phủ. Task không mở index. **OPEN:** onset (lúc bắt đầu biểu hiện) quan sát được, thời điểm kết thúc lỗi và nhãn vùng ảnh hưởng chưa được nguồn đã đọc cung cấp. Chỉ chấm được mốc tiêm khi được phép dùng nhãn; không gọi đó là onset triệu chứng.

**FACT lời tác giả về nhãn chỉ báo:** [paper v2](public-metadata/run-002/sources/paper-v2.html) §3 nói mỗi ca được gắn service gốc và root cause indicator (chỉ báo nguyên nhân gốc). §3.2 mô tả chỉ báo theo loại lỗi: lỗi tài nguyên dùng resource metric; DELAY dùng latency; LOSS dùng số request thất bại/response code; lỗi mã nguồn dùng dòng stack trace nguyên nhân, hoặc error log/response code khi không có stack trace. Đây là mô tả của tác giả, chưa phải nhãn chi tiết được task xác minh theo từng ca. Không tự suy fault→metric thành ground truth mới.

**FACT artifact ở revision đã lưu:** [hf-tree.json](public-metadata/run-002/hf-tree.json) có 8 file `root_cause.txt`, đều ở RE3-SS; bốn bộ mục tiêu không có file mang tên này. [HF card](public-metadata/run-002/sources/hf-README.md) cũng mô tả 8 file chứa dòng log nguyên nhân gốc. Không thấy tên file này chưa chứng minh thiếu mọi hình thức nhãn chỉ báo. **OPEN — chưa xác minh:** nội dung và mapping nhãn chỉ báo cụ thể theo từng ca/operation/code line của bốn bộ; task không mở index và nguồn đã đọc chưa xác lập mapping đó. Chưa chấm trực tiếp nhãn chi tiết từ lời mô tả hoặc regex log.

**Đối chiếu response code:** paper §3.4 chỉ nói có response code khi có sẵn. [cases.json](local-inspection/run-002/cases.json) và [summary.json](local-inspection/run-002/summary.json) cho mẫu RE3-TT route×f2 lặp 1 có `status_nonnull=0` trên 183.623 span. Kênh status trống trong mẫu này, có thể do xuất/lược trường; không suy ra mọi ca RE3 thiếu kênh đó hoặc không chẩn đoán được code fault. Log mẫu đã rà regex và ngữ cảnh ở [LOG phiên tự soát 03/10](../../tasks/T-002-the-dataset-rcaeval/LOG.md), nhưng hàng khớp không tự là lỗi, nhãn vùng hay code line gốc. Ý nghĩa chỉ báo và nhãn chi tiết vẫn chưa xác lập.

Tổng 735 ca và 90/90/30/30 ca của bốn bộ khớp giữa tree, các README và mô tả bài. Có hai chi tiết không nên sao chép nguyên bảng:

1. HF card bảng RE3-TT liệt kê `f1–f5`, nhưng phần mô tả RE3 cùng file ghi F5 chỉ có ở RE3-OB. Tree RE3-TT chỉ có `f1–f4`; GitHub README cũng ghi `f1–f4`. Vì vậy thẻ dùng số đếm directory, kèm ghi rõ lệch trong bảng card nguồn. Không tự sửa nguồn.
2. Bài v2 §3.3 nói lặp 3–5 lần; tree có 6 ca ở ô RE3-TT `ts-route-service × f3`. HF card mô tả RE3 không đều và lặp 3–6, khớp tree. Không được giả định RE3 là lưới đều giống RE2.

**OPEN vị trí đồ thị:** tên service gốc không cho biết lá/giữa/hub. Bài dẫn repo kiến trúc của Online Boutique và Train Ticket nhưng không chỉ ra revision hệ thực nghiệm. Vị trí cần tính từ cạnh trace thật trong dữ liệu được phép; kiến trúc công bố chỉ là nguồn đối chiếu khi revision tương ứng được xác định. Một service có nhiều cạnh trong mẫu có thể do workload hoặc instrumentation (cách gắn bộ đo), không đủ chứng minh nó là hub trong toàn bộ hệ.

**CANDIDATE, chưa kiểm:** ít service gốc và ô lỗi không đều có thể hạn chế khả năng phân xử điều kiện đồ thị. Cũng có thể các root ít nhưng bao phủ nhiều vị trí, hoặc workload tạo nhiều tình huống khác nhau. Không chọn/bỏ dataset từ riêng số đếm này. Bốn bộ cùng họ RCAEval không tự đáp ứng yêu cầu một dataset khác nhóm tác giả/công cụ/stack ở MRP §4 tiêu chí 9.

**USER_CONFIRMED:** SPEC cho phép thống kê metadata công khai và đọc mẫu cục bộ được liệt kê; việc chọn dataset/cách chia ở G1 chưa quyết. Không thêm quyết định **DECIDED** trong task này.
