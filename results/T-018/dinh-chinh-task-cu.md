# Vấn đề ở task cũ (T-000 đến T-012) — để người phản biện kiểm

T-018 không sửa file của task cũ. Mỗi mục: task; file:dòng; sai gì; bằng chứng; kết luận bị ảnh hưởng; đã triển khai gì trong T-018; đề xuất sửa (đoạn cũ → đoạn mới). Minh quyết sửa hay không.

Phạm vi soi: phần của T-000–T-012 liên quan tới GDN, DecompRCA, và dữ liệu RE2-TT mà GDN dùng. Không soi lại toàn bộ các task.

## D1. T-002 — thẻ RCAEval thiếu một đường rò nhãn: bộ cột của từng ca

- **File:** `results/T-002/the-rcaeval.md:158-160` (mục 8 "Rò nhãn và thông tin phục vụ G1", thẻ RE2-TT; cùng nội dung ở các thẻ khác dòng 288–290, 421–423, 512–514).
- **Sai gì:** mục 8 liệt kê ba đường rò: tên thư mục, `inject_time`, biên file. Thiếu đường thứ tư: **tập cột có mặt trong file metric của một ca** tương quan với service gốc và với triệu chứng. Đây là thiếu sót, không phải câu sai.
- **Bằng chứng** (`results/T-018/cot-re2tt/cot-khong-du-30-ca.csv`, `scripts/dem_cot.py`; đếm trên 30 ca dev, so với nhãn sau khi đếm xong):
  - 12 cột latency/workload của contacts, preserve, preserve-other, seat, security, user vắng ở **đúng 4 ca**, cả 4 có service gốc `ts-order-service` (order_disk_2, order_disk_3, order_loss_2, order_loss_3). 26 ca còn lại đều có.
  - 23 cột `*_error` chỉ có ở 2–20 ca. Sự có mặt trùng một phần với service gốc: `ts-train-service_error` có ở 6 ca, 4 ca có gốc train-service; `ts-travel-service_error` có ở cả 6 ca travel-service. Cột error chỉ xuất hiện khi có lỗi được ghi trong file, kể cả sau mốc tiêm, nên sự có mặt của nó là thông tin của tương lai và của triệu chứng.
- **Nguyên nhân khả thi khác (Q-33):** 4 ca order có thể thuộc một đợt thu khác mà bộ tạo tải không gọi luồng đặt vé; khi đó đây là khác biệt tải theo đợt, trùng với service gốc do cách xếp lịch tiêm. Dù nguyên nhân nào, với một phương pháp hay adapter dựng bộ cột theo từng ca, bộ cột mang thông tin tương quan với nhãn.
- **Kết luận bị ảnh hưởng:** tính đầy đủ của mục 8 thẻ RCAEval; giao thức P3 (MRP §6 mục 8 "không đưa nhãn vào phương pháp, kể cả đầu vào suy ra từ chúng"). Với RCA chạy từng ca (BARO, N-Sigma) bộ cột là của chính ca đó và không học xuyên ca, nên rủi ro thấp hơn; với phương pháp học xuyên ca (GDN, phương pháp có giám sát) rủi ro trực tiếp.
- **Đã triển khai trong T-018:** đếm và ghi số; GDN dùng bộ cột cố định L\* (giao 30 ca dev) để không phụ thuộc bộ cột của ca được chấm; mục 9.1 của `ho-so-gdn.md`.
- **Đề xuất sửa** (thêm vào cuối đoạn dòng 160): "Đường rò thứ tư: tập cột metric khác nhau giữa các ca và tương quan với service gốc (12 cột latency/workload chỉ vắng ở 4 ca có gốc ts-order-service; cột `*_error` chỉ có khi có lỗi được ghi). Phương pháp học xuyên ca phải dùng bộ cột cố định chốt từ dữ liệu học. Nguồn: `results/T-018/cot-re2tt/cot-khong-du-30-ca.csv`."

## D2. T-001 — câu "chưa kiểm bảng của bài dùng chế độ nào" nay đã kiểm được một phần

- **File:** `results/T-001/danh-sach-phuong-phap.md:191` (mục 7) và `:91` (mục 2).
- **Sai gì:** dòng 191 nêu nguyên nhân khả thi khác cho "GDN F1 0,81 trên SWaT" là "chế độ mặc định chọn ngưỡng trên nhãn test (L8). Chưa kiểm bảng của bài dùng chế độ nào". Bài ghi rõ ngưỡng là max điểm trên tập kiểm định (bài GDN, dòng 286–291 và 341–350 của `gdn.txt`), tức tương ứng `report='val'`. Nhưng ở cả hai chế độ, code chuẩn hóa điểm bằng trung vị/IQR của toàn tập test (`evaluate.py:52`). Dòng 91 viết "Chế độ `val` ... khớp bài": đúng về ngưỡng, nhưng thiếu ý ngưỡng tính trên thang của tập kiểm định còn điểm test trên thang của tập test (`evaluate.py:21` so với `:20`, `:52`).
- **Bằng chứng:** `results/T-018/ho-so-gdn.md` mục 2 (B8, B10), mục 5 dòng 4 và 7, mục 8.1 (G1–G3).
- **Kết luận bị ảnh hưởng:** mục 7 của T-001 (nguyên nhân khả thi khác cho số công bố). Danh sách phương pháp không đổi.
- **Đã triển khai trong T-018:** biến thể R-chuẩn-hóa-b (trung vị/IQR từ tập kiểm định) được tính song song với code ở mọi lượt (`scripts/tinh_tay_gdn.py`, `scripts/phan_tich_gdn.py`).
- **Đề xuất sửa:**
  - dòng 191, cột 2: "Chế độ mặc định chọn ngưỡng trên nhãn test (L8). Chưa kiểm bảng của bài dùng chế độ nào." → "Bài ghi ngưỡng = max điểm trên tập kiểm định (tương ứng `report='val'`; bài dòng 286–291, 341–350), nhưng code chuẩn hóa điểm test bằng trung vị/IQR của cả tập test ở mọi chế độ (L8), và không có log hay dữ liệu để biết bảng sinh từ chế độ nào (T-018, `ho-so-gdn.md` mục 8.1)."
  - dòng 91: thêm sau "khớp bài": "về cách đặt ngưỡng; điểm kiểm định chuẩn hóa bằng thống kê của chính tập kiểm định, điểm test bằng thống kê của tập test (`GD:evaluate.py:20-21, 52`)."

## D3. T-005 — dữ liệu GDN dùng bộ cột có cột của ca test, và chuẩn hóa min-max đưa cột hằng sang đơn vị thô

- **File:** `results/T-005/scripts/chuan_bi_dau_vao.py:122` (bộ cột = giao 5 ca học **và ca test**), `:125-128` (khoảng 0 thay bằng 1); `results/T-005/do-kha-thi.md:51` ("333 cột").
- **Sai gì:** không sai với mục đích của T-005 (đo thời gian). Nhưng nếu dùng lại script này cho P3: (1) bộ cột phụ thuộc ca được chấm (siêu dữ liệu test, `ho-so-gdn.md` G7); (2) cột hằng trong tập học được chia cho 1, nên ở dữ liệu mới cột đó mang nguyên đơn vị thô.
- **Bằng chứng:** dựng lại dữ liệu bằng script độc lập ra **trùng từng byte** với file của T-005 (`runs/b3-chuan-bi.json`, SHA-256). Với bộ cột L\*, giá trị lớn nhất sau chuẩn hóa ở 19 đoạn bình thường giữ ngoài: 6,0·10^8 khi học trên 1 ca, 7717 khi học trên 5 ca (cùng file). Ảnh hưởng tới điểm GDN: trên 19 đoạn bình thường giữ ngoài, mô hình học bằng đúng dữ liệu của T-005 (R1, trọng số trùng T-005) báo động ở 11,2 % số tick theo cách chuẩn hóa của code và 93,7 % nếu chuẩn hóa điểm theo tập kiểm định (`runs/b6b7-phan-tich.json`; `ho-so-gdn.md` mục 9.2, 9.4).
- **Kết luận bị ảnh hưởng:** không kết luận nào của T-005 (thời gian chạy không phụ thuộc giá trị). Ảnh hưởng nếu P3 dùng lại `chuan_bi_dau_vao.py`.
- **Đã triển khai trong T-018:** L\* cố định; đo hệ quả của cột hằng (mục 9.2 hồ sơ).
- **Đề xuất sửa:** thêm một dòng ghi chú dưới bảng 2b của `do-kha-thi.md`: "Dữ liệu GDN ở đây chỉ để đo thời gian: bộ 333 cột có dùng cột của ca test, và cột hằng trong tập học bị chia cho 1. Không dùng lại cho chấm điểm; xem T-018 `ho-so-gdn.md` mục 8–9."

## D4. T-001 — ghi chú về cài đặt baseline của DecompRCA

- **File:** `results/T-001/danh-sach-phuong-phap.md:163-179` (mục 6, cột DecompRCA) và `:186` (mục 7).
- **Sai gì:** bảng đánh dấu DecompRCA dùng RCD và CIRCA, đúng. Nhưng RCD (và ε-Diagnosis) của DecompRCA là bản PyRCA, CIRCA là bản gốc NetManAIOps có thêm DA, không phải bản RCAEval (`decomprca.md` K12). Dòng 186 giải thích tần suất "có thể vì chúng sẵn trong RCAEval"; với DecompRCA giải thích này chỉ đúng cho BARO.
- **Bằng chứng:** `DecompRCA/method/algorithms/rca/rcd.py:5`, `epsilon_diagnosis.py:5`, `circa.py:22-28`; PDF DecompRCA dòng 1050–1084.
- **Kết luận bị ảnh hưởng:** không đổi danh sách. Ảnh hưởng nếu ai dùng số RCD/CIRCA của DecompRCA làm mốc tái lập cho bản RCAEval.
- **Đã triển khai trong T-018:** ghi ở `decomprca.md` mục 3 (K12), mục 4 ý 5.
- **Đề xuất sửa:** thêm vào chú thích dưới bảng mục 6 (sau dòng 179): "DecompRCA dùng RCD, ε-Diagnosis của PyRCA và CIRCA gốc (RHT + DA), không phải bản RCAEval; chỉ BARO chạy qua RCAEval (T-018, `decomprca.md` K12)."
