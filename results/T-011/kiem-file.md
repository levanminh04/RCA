# LEMMA — kiểm bốn ZIP IT đã duyệt Q-47

**Đã kiểm toàn bộ member trong đúng hai ngày mẫu; chưa kiểm Original hoặc các ngày còn lại.** Không RCA, detector, training hoặc chia dữ liệu. LEMMA không phải bộ bảo toàn; không mở Bank/locked. Giấy phép cuối còn OPEN, việc kiểm nội bộ phi thương mại theo WHY-14 không là quyền chia sẻ payload gốc/phái sinh.

## Dữ liệu thực đã đọc và mức kiểm

Bốn ZIP cộng 1.583.143.326 byte. File gốc nằm trên EC2 mới `/home/ubuntu/rca-t003/data/lemma/`; kết quả kiểm trong repo. [Download manifest](runs/download-001/manifest.json) và [phép so LFS độc lập của root](../T-003/runs/lemma-independent-hash-001/result.json) xác nhận đúng byte/SHA-256 public revision. Không dùng hash tự tính làm bằng chứng duy nhất về nguồn.

[inspect-008](runs/inspect-008/summary.json) tái dùng CRC/summary hợp lệ của inspect-007 và inspect-002, bổ sung schema khác. Có 2.431 file không phải directory đều đọc tới EOF/CRC đạt, 17.500.872.729 byte khai báo member, 64.107.208 dòng CSV và 42 NPY được parse. Không giải nén nguyên cây; CSV đọc luồng, mỗi lần chỉ một NPY. Byte member là dữ liệu đã đi qua decompressor, không là nhu cầu ổ đĩa khi streaming.

| Mẫu | CSV / dòng | NPY | Member byte | UTF-8 lỗi / file | CSV ragged |
|---|---|---:|---:|---|---:|
| PR20211203 | 2.355 / 43.314.418 | 26 | 16.268.296.541 | 197.543 / 16 | 0 |
| Cloud20240124 | 32 / 20.792.790 | 16 | 1.232.576.188 | 0 / 0 | 0 |

Tất cả NPY ở mẫu dùng object dtype chứa pickle. [Bộ đọc an toàn](scripts/safe_npy.py) diễn giải một tập opcode thành đối tượng inert (không hoạt động), không import/gọi globals của payload, không pickle.load, không allow_pickle=True. Mọi primitive array có shape×itemsize khớp byte, order C, endian nhỏ và dtype f8/i8/i4 được kiểm trước đọc. GLOBAL ngoài whitelist và shape sai bị chặn trong tự kiểm. Surrogateescape giữ nguyên byte CSV không giải được UTF-8; chỉ đếm lỗi, không thay dữ liệu bằng ký tự khác. Giữ lỗi decoder/schema trước ở inspect-002/005; không gọi lỗi UTF-8 là CRC hỏng.

## Schema và nối nguồn tín hiệu

Metric NPY chứa dict theo KPI, các trường `KPI_*` hoặc `jaeger_*`, `Pod_Name`/`Node_Name`, `Sequence`, `time`. PR có cả hai kiểu khóa; không dùng loader chung cố định field cho mọi file. Processed log NPY là entity×time×feature; Cloud dict phẳng, PR dict lồng. Cloud golden/PCA có 15 entity; PR golden/frequency có 89/132 entity. CSV log có LineId, Time, Content, EventId, EventTemplate, ParameterList; template có EventId, EventTemplate, Occurrence. Đây là schema thực của mẫu, không thay schema Original.

Nối tên chính xác theo [validation linkage](runs/validate-003/validation.json), phân biệt metric, log CSV và log feature NPY; filename cung cấp entity provenance, không chứng minh body có ID service. Cloud đủ 15 metric entity/15 structured log filename, giao 15. PR số thực lưu trong file-inspection-summary.json; mapping p2n có 302 pod→node nhưng không là graph gọi dịch vụ. Raw→processed và pod→service selector mọi ngày vẫn OPEN.

Không ZIP mẫu nào chứa bảng span/parent; CSV log không có cột trace/span ID. Không tính unique-parent/graph degree từ processed log hoặc sơ đồ kiến trúc. ID có thể nằm trong payload nhưng không có hợp đồng span/parent để ghép được xác minh; không kết luận Original thiếu trace hoặc root cô lập.

## Nhãn và clock: nguồn khác nhau không được trộn

Cloud PPTX slide4–7 trong [labels](runs/inspect-008/labels.json) xác định AP host ip-10-1-100-109, instance i-078923fb30cac1ede; cause là API /api/cpu_stress/ chiếm một trong bốn CPU. Nó ghi bug 2024-01-24 03:10Z và failure time 03:10:51Z; đây là nhãn narrative của scenario, không phải onset đã được phát hiện độc lập từ số đo. Metric/log dùng UTC; nhãn PPTX này đã có Z, không dịch thêm chín giờ. JSON riêng có epoch thành09:10:51Z, lệch sáu giờ với PPTX; giữ xung đột, không sửa JSON và không dùng epoch đó đặt cửa sổ kiểm.

PR PPTX mô tả external NFS disk full, địa chỉ192.168.57.153, nối MongoDB-v1, rồi ảnh hưởng ratings. README gọi root MongoDB-v1; phải phân biệt entity nhãn benchmark và nguyên nhân vận hành ngoài cluster. Mẫu có mapping pod MongoDB, nhưng không suy NFS hiện diện trong metric/trace hoặc chấm pod thay storage mà chưa chốt đơn vị. PPTX có ví dụ Jaeger ngày khác; không đếm chúng thành span thật ngày20211203. Mốc tiêm/normal/recovery đáng tin cho PR vẫn OPEN.

NPY time là epoch giây; PR KPI CSV epoch microsecond và Cloud KPI CSV epoch giây. Giữ unit gốc, chuyển chỉ trong phép nối kiểm. Cadence thực và gap theo từng case nằm trong summaries.json, không lấy lịch source thay chất lượng file. Node/pod PR preprocessing giao thời gian, loại entity thiếu điểm và điền NaN theo code nguồn; không thấy NaN trong output không chứng minh raw không thiếu. Số nonfinite và constant theo kênh nằm trong file-inspection-summary.json/summaries.json.

## Kiểm KPI độc lập và giới hạn release

[validate-001](runs/validate-001/validation.json) đọc lại ba KPI CSV, group theo label/second, tự tính trung bình rồi so từng điểm với cột KPI cuối của mọi Sequence. Cloud 14/14 case khớp tất cả shared seconds, không missing/mismatch. PR 46/46 case không nối đầy đủ hoặc khác giá trị: kpi.csv chỉ có label ratings; NPY có thêm reviews/reviews-v2/reviews-v3. Ví dụ node ratings có63.976 điểm ghép, 37.938 điểm thiếu, 63.974 điểm khác; chênh lớn nhất104.261. Không sửa dữ liệu hoặc giả định CSV là nguồn trực tiếp của mọi NPY. Cần tác giả/nguồn preprocessing giải thích KPI khác, provenance, release hoặc lỗi exporter. Phép Cloud đạt và shape/byte kiểm an toàn là đối chứng cho logic reader, nhưng không thay xác minh PR.

Cloud log-feature NPY lưu KPI_Label ratings.book-info... dù metric/KPI CSV cùng archive ghi scenario8_app_request. Đây là metadata không khớp, không tự kết luận numeric payload thuộc PR. Cloud PCA chỉ kết thúc trước injection, không có fault segment để dùng như feature phủ toàn sự cố. Numeric vector trùng giữ tại duplicate_numeric_vectors; cột metric Cloud Error/Latency thường dùng chung số đo, không được đếm là hai lần lặp độc lập.

## Normal và mô tả tiêu chí7

Cloud PPTX ghi thu48h, lỗi giữa kỳ sau24h; đồng thời ghi có 502 trước lỗi. Vì vậy trước injection là **tham chiếu theo timeline nguồn**, không có nhãn healthy từng điểm. Chia hai nửa12h đầu làm tham chiếu và đối chứng,24h sau bug làm đoạn sự cố; không dùng root chọn SLI. Đây là phép mô tả P2, không detector/dev/test.

[cloud-descriptive-bands.csv](cloud-descriptive-bands.csv) ghi mọi entity/kênh/q=.95/.99/.995, median tham chiếu, band tuyệt đối, zero band, số mẫu và tử/mẫu đối chứng/sự cố. Metric từng giây; log CSV dùng số event/giờ UTC đầy đủ, bỏ giờ cắt qua biên, mỗi nửa chỉ11 mẫu nên q log thô. Log feature golden có đoạn sau lỗi; PCA denominator sau lỗi0 được giữ trống, không gọi0% bất thường. Root gắn sau khi tính. Không OR các kênh, không regex mức lỗi làm nhãn vùng. PR không tính band normal vì thiếu mốc normal được xác minh và KPI không khớp; dùng tùy ý phần đầu sẽ đóng OPEN bằng giả định.


Ví dụ từ đúng CSV kết quả, q=.99 ở file Latency/cpu_usage; đây là từng kênh, không là kết luận trung bình toàn hệ:

| Kênh/entity | Vượt band đối chứng | Vượt band sau bug |
|---|---|---|
| i-078923fb30cac1ede | 203/43.117 (0.47%) | 85.935/85.986 (99.94%) |
| i-03e386f9757915c39 | 479/43.117 (1.11%) | 888/85.986 (1.03%) |
| i-04a5da0032591b1f6 | 394/43.117 (0.91%) | 861/85.986 (1.00%) |
| Latency | 798/43.117 (1.85%) | 1.196/85.986 (1.39%) |

CPU tại root thay đổi rõ ở kênh này; CPU các entity khác và KPI Latency không cùng có tỷ lệ vượt tăng. Không dùng ví dụ này chứng minh lan truyền hoặc phủ mọi kênh. Trung bình KPI theo giây có thể che các request tail; đây là khả năng giải thích, chưa được kiểm từ request outcome/route trong task.

Co-occurrence ngoài root có thể do workload chung, nhiễu, threshold zero, recovery chưa biết, hoặc preprocessing. Không xem vượt band là nhãn ảnh hưởng/lan truyền thật. Nhãn vùng và bất thường từng trace vẫn thiếu; RQ3c hoặc đánh giá graph cần nguồn bổ sung.

## Chi phí, tự phản biện và tiếp nhận

Download 27,540s; full initial audit 200,284s; correction inspect-007 135,206s; schema supplement008 2,824s tái dùng kết quả. Lượt004 dừng tối ưu giữ progress/console, không ghi2,824s như thời gian toàn scan. MaxRSS lớn nhất audit hoàn tất khoảng901.348KiB. Các bước kiểm chạy có chồng thời gian; đây là chi phí quan sát trên EC2, không benchmark method hoặc dự báo adapter toàn release. Lượt lỗi/interrupt không xóa. Không tải lại ZIP; script --reuse-run chỉ tái dùng summary cùng archive/member CRC đạt và giữ đếm byte lỗi đã có.

Tự phản biện: (1) parse object có thực thi payload không — không, reader whitelist/inert và hostileselfcheck; (2) CRC đạt là chất lượng schema đạt không — không, lỗi parser giữ riêng; (3) metric/NPY log entity có bị trộn không — đã sửa, validate-003 là bản đúng; (4) một ngày là census release không — không; (5) PR KPI mismatch có thể do parser không — Cloud toàn bộ so khớp, PR vẫn cần nguồn riêng; (6) normal24h nguồn có sạch không — chưa; (7) metadata Cloud ratings có làm log payload thuộcPR không — chưa chứng minh. Không dùng dữ liệu này kết luận graph thắng/thua.

Chạy lại đọc source offline và builder local; audit EC2 dùng `inspect_files.py --data /home/ubuntu/rca-t003/data/lemma --results <new-run> --reuse-run <saved-run>`. Giữ run mới, không đè. Toàn release và Original không nằm trong bốn ZIP được duyệt; kế hoạch mở rộng cần đúng quyền/byte trước làm. G1 do Minh quyết, Claude review gộp T003.
