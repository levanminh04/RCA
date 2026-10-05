# Kế hoạch P3 — đề xuất chưa kiểm, Minh duyệt rồi mới làm

P3 tạo bảng baseline trên dev đã chọn, không mở test/giữ ngoài. Không chạy kế hoạch này trong T-020. Chưa có runtime official trên những dataset mới; các phép chiếu dưới chỉ là CANDIDATE theo cùng phần cứng, kích thước, cadence, phiên bản và tải. Không dùng chi phí loại dataset.

## Thứ tự theo phụ thuộc (chờ WHY)

| Bước | Cần đầu vào | Việc và đầu ra | Chạy song song / tái sử dụng |
|---|---|---|---|
| 1 | G1 Minh duyệt D1–D6 và WHY | khóa danh sách/variant, role/split và budget; inputs mới chỉ dev được duyệt | không lấy score làm lý do đổi |
| 2 | 1, quyền dữ liệu/license/sourceimmutable | adapter schema/time/id/unit; root mapping từ inventory; fixed-columns từ train; evaluator độc lập | theo dataset và modality ở thư mục riêng, không ghi chung file; dùng lại parser/helper đã kiểm |
| 3 | 2 | normal-only checks: crop leak, false alerts, candidate/root coverage, missingness/clock, graph parents/edges; khóa window theo D5 trước rankings | phép thống kê theo bộ song song, nhưng không đoofficial runtime khi máy đang bận |
| 4 | 3, windows và method fidelity | tái lập published configuration nếu có cùng data; phân biệt scorer/graph/DA/interval, output finite/ties/errors | dùng lại các lượt T005–18 chỉ khi hash/config khớp và làdev; không biến chúng thành unseen test |
| 5 | 4, budget tổng đã duyệt | common-protocol baseline; metric đơn giản/M4 trước, trace adapters, CIRCA architecture, PC/RCD sau; GDN chỉ sau calibration hợp lệ | methods độc lập ở máy khác được, official cost đo máy riêng/rảnh; fit graph có thể reuse nếu input variant không đổi |
| 6 | 5 | bảng từng ô/ca và mode; detect P/R/F1, root MRR/NDCG/Hit, retrieval nếu chọn; giữ failure,timeout,nonfinite và candidate absence | tính aggregate song song, không thu hẹp denominator vì method hỏng |
| 7 | 6 | kiểm fake normal-normal, root/path/time không lọt features; dependence và sensitivity windows; chuẩn bị hạn chế P4 | dùng lại fixture/cơ chế đã có; không dùngtest gold chọn variant |

## Ngân sách là toàn dataset × tất cả seed

Q-40 là Minh cho tối đa 3 giờ chờ thực tế/phương pháp/toàn bộ, không 3 giờ mỗi seed. Công thức cho scorer theo ca: `N × S × thời gian/ca + load/preprocess/queue không chồng lắp`. Với detector học xuyên ca: `S × (fit-normal + infer-toàn-bộ)`; không nhân training một lần/incident. Phân biệt elapsed wall và tổng CPU; không cộng reservation giả thành số đo. [runtime.csv](trung-gian/method_evidence/runtime.csv) giữ 47 hàng quan sát, nguồn gốc và dự phóng có điều kiện; [09](09-kiem-cheo-so-lieu.csv) kiểm từ output/JSONL gốc.

| Phương pháp / quan sát | Tổng toàn bộ và seed | Hệ quả cho đề xuất P3 |
|---|---|---|
| RCD OB L20,90 ca, một seed có `5623.304332642s` | 1.562h một seed; nếu tương đương3 seed là16869.913s=4.686h | ba seed sẽ vượt 3h; chọn seed/budget ở D1 dựa priorvariance vàchi phí, không chạy3rồi xinexception |
| RCD TT30 L10 `1481.598041136s` | 0.412h30 ca; phépchiếu90 ca3 seed13334.382s=3.704h **chưa kiểm** | không dựa thời gian ca trung bình để bảo đảm full TT;30dev thực khác90toàn bộ |
| TORAI gốc/sửa TT30 ở máy EC2 đã ghi | 45.163s /65.653s một seed; chiếu90 ca3 seed406.464/590.878s | khá nhẹ tại điều kiệnquan sát; không chạy EC2 T020 và không thay bằng laptop bận; nguồn metadata lịch sử ởruntime |
| BOCPD T005 window mộtca1440.133s | chiếu90 ca một seed129611.97s≈36.003h **chưa kiểm**; phụ thuộcT² vàsốmetric | window/cột/budget có thể khiến full protocol không khả thi; báo không chạy đủ, không loại dataset theo tốc độ |
| CIRCA T014 blockworker9335.006s,queue4171.455s | tổng không chồng lắp13506.461s≈3.752h, còn reservation900s không phải đo | đây làcheck trên một ca với nhiều config, không per case prediction. Q40historicalexception OPEN, khônghợp thức hóa; PC1796.269s một fit273 metric không đủ ước lượng bộ |
| MicroRank T005 mộtca101.053s window /237.518s full | chiếu90 ca9094.77s /21376.62s một seed;3 seed27284.31/64129.86s **chưa kiểm** | actual shape operations vàmatrix dày thay đổi; dùngT015 existing runs để đo phân bố trên dev trước quota; không gọi đây benchmark full bộ |
| SimpleRCA T017 TT30 run005 gồmchecks46.191s | projection90 ca138.572s; không isolated primary runtime | nhẹ về cơ chế; tách extra kiểm khỏi measurement khi P3 đo |
| GDN T018 fit các lượt257.35–1928.69s, T005fit1028.822s/infer11.685s | cần fit per hệ seed + inferdataset. Không chiếu1028.822×90 | ngân sách có thểđủ time nhưng b vẫnfalse-alertnormal cao; không dùngthời gian làm bằng chứng detector ready |

Nguồn RCD/TORAI là `D:/RCA-ext/work/T-016/.../meta.jsonl` kết quả lưu máy này; không liên hệ EC2. Nếu máy khác không có metadata thì ghi chưa xác minh, không tự đo mới. Chi phí adapter/download/normal calibration không nằm trongtimer method body, phải ghi riêng. Các projection không phê duyệt thêm seed hoặc method variant.

## Qua đêm hoặc máy khác (chờ WHY)

PC, RCD, BOCPD và GDN fit là việc nặng dựa số đo/cơchế đã có. Đề nghị đặt hàng đợi ở máy khác hoặc qua đêm **sau khi Minh duyệt**, cóprogress/timeout, môi trường ghim vàphạm vi write độc lập. Thời gian vẫn cộng vào 3h nếu thuộc budgetmethod/dataset; qua đêm không làm việc vượt quota hợp lệ. Lượt dự kiến >1h phải báo chi phí trước vàchờ duyệt theo AGENTS; bảng này là đề xuất, không authorization chạy. EC2 khôngdùng trongT020.

Tái dùng số sẵn có khi đúng hash/config vàdev giảm thời gian nhưng vẫn phải giữreproduction vs comparison, platform/source vàtiming condition. Normal train/graph cache không dùngtest data. Các chi phí chưa đo nằmđúngcộtOPEN, không chọn một seed vì accuracy thuận lợi. Không nêu rủi ro thời hạn; đánh giá FlashTicket nằm P9/P10 theoMRP.
