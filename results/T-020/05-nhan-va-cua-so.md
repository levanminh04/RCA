# Nhãn, cửa sổ và truy hồi — đề xuất G1, chưa duyệt

Quyết định Q-54 của Minh chuyển ngân sách nhãn và cửa sổ sang G1; Q-56 chuyển Retrieval@K/Rerank@1 sang G1. Các con số dưới là bằng chứng cơ chế hoặc cấu hình ứng viên, không là cấu hình P3 đã chọn. Mọi đề xuất sử dụng quan trọng **(chờ WHY)**.

## Nhãn học, chọn cấu hình và chấm

[42 hàng yêu cầu nguyên bản](yeu-cau-dau-vao-hop-nhat.csv) giữ `can_nhan_de_hoc` cho từng biến thể; [bảng nhãn theo nhóm](trung-gian/method_evidence/label-budget.csv) và [audit runner](trung-gian/method_evidence/runner-leakage.csv) là bằng chứng kèm nguồn. Bảng phân biệt:

| Nhóm | Học/fit | Chọn cấu hình/checkpoint | Chấm và chuyển hệ |
|---|---|---|---|
| BARO, NSigma RCA | fit median/IQR hay mean/std từ normal; không học root | chỉ dev, không test gold | root service chỉ evaluator; schema numeric/metric→service mới cần adapter |
| BOCPD, NSigma detector | prior/mức normal; full-input min-max và expanding đầu chuỗi phải được kiểm | hazard/threshold trên dev/normal; không lấy test labels | mode b cần stream không lộ crop/mốc; delay tính từ injection nếu chỉ có nhãn này |
| CIRCA PC / kiến trúc | PC và regression dùng thời gian; graph kiến trúc từ inventory/trace độc lập root | alpha/regressor/DA/interval trên dev; không test | không dùng gold chọn SLI hoặc ghép node; graph từng hệ cần dựng lại |
| MicroRank / TraceRCA / trace detector | normal duration theo operation hoặc self-handling; graph normal/current | SLO/partition theo prior work, lệch phải giải thích trên dev | root pod/kind/frontend cần inventory; thiếu thật không điền từ nhãn |
| TORAI / RCD | học quan hệ metric; TORAI dùng log severity và GMM, không root supervised | graph/stride/seed đã xác định ở hồ sơ, P3 giữ variant rõ | normal/fault split biết mốc là label budget thật; không gọi tự phát hiện |
| SimpleRCA M4 | fit rule normal cho metric/trace; log fixed threshold không cần normal | các sensitivity là dev, không chọn bản có Hit cao nhất | union service gồm cả normal-only log; rule khác detector streaming |
| GDN best / val / b | normal train+val; chọn normal bằng injection dev dùng nhãn regime | best dùng test labels: chỉ tái lập. val vẫn normalization bằng test tương lai. b train/val-only chưa hiệu chỉnh đạt | học embeddings theo cột từng hệ; không zero-shot sang service mới; held-out chỉ infer nếu normal train độc lập và budget đã duyệt |
| DecompRCA retrieval/LLM | đã đọc, không chạy; không thêm method đã chốt | không tune retrieval bằng test gold | chỉ dùng làm cơ sở bàn độ đo; metric→service và tập ứng viên phải đóng trước chấm |

Nhãn *regime* (bình thường/sự cố), nhãn *root* và nhãn *time* khác nhau. Biết injection để cắt hai nửa không là “không dùng nhãn” dù không truyền root. Root gold và nhãn đánh giá test chỉ evaluator, không dùng fit/tune. MRP §4 ghi nhãn test chỉ để chấm, còn P3 chế độ (a) biết trước thời điểm; D4 đề xuất cấp mốc ngoài ở chế độ (a) và cần Minh làm rõ ngân sách time-label test. Chế độ (b) không cấp mốc tiêm. Baseline có giám sát theo service của hệ không chuyển nguyên head sang một hệ mới. Giữ ngoài không cấp root/fault/incident-time để học hoặc tune; normal độc lập của chính hệ giữ ngoài, nếu được cấp, phải là một phương án ngân sách được Minh duyệt và công bố riêng.

## Cửa sổ: giây, điểm và vị trí thật

[window-parameters.csv](trung-gian/method_evidence/window-parameters.csv) giữ mọi cấu hình đã tìm trong hồ sơ, đơn vị và nguồn; không đồng nhất “10” với phút hay điểm. [Kiểm số](09-kiem-cheo-so-lieu.csv) tính lại số từ CSV/JSON kết quả gốc.

| Cơ chế | Vì sao cửa sổ đổi kết quả | Bằng chứng đã thấy |
|---|---|---|
| BARO/NSigma | normal median/IQR/std và max hậu thay đổi; cột hằng bị bỏ làm đổi candidates | T-013 `cua-so-va-che-do-b.md`, sửa R1: pre/post thay riêng có tương tác. L20 trên ô delay chỉ360 pre+361 post, không đủ600+600 |
| BOCPD | lịch sử run-length, min-max toàn chuỗi và prior; dùng số điểm lớn làm chi phí tăng | T-007 kiểm đúng đắn, T-013 wrapper sentinel và hazard; sentinel T không là alarm thật |
| CIRCA | graph PC thấy toàn window; RHT có tập reference/test riêng | T-014:111 điểm1s reference và10 điểm cuối tại+291..+300s; default gốc interval1min thành111min và10min, không cùng thí nghiệm |
| MicroRank/TraceRCA | normal operation/SLO và partition đổi; candidate/edge normal-current thay đổi | T-015 `kiem-cua-so-ob.csv`; self-time gốc và span inclusive khác. Không chọn window theo bên nào thắng |
| TORAI | giảm mẫu 15s hai lần thành 225s; L10 có thể chỉ giữ quá ít điểm causal | T-016 `giam-mau-hai-lan.md`; bản sửa bỏ lượt giảm mẫu thứ hai, ghép theo vị trí. WHY-19/20 có nguồn hiện hành |
| SimpleRCA | events/P95 và số log tích lũy phụ thuộc độ dài; hòa nhiều service không là confidence | T-017 variants half300/half600 và kiểm tính tay |
| GDN | model 5 tick, smoother 4 tick, normal 720/3600/7200 tick ở 1s khác47.515/118.795tick tại 10s của bài | T-018: fixed columns/val normalization giúp hết đường lộ đã chỉ ra nhưng false-alarm normal vẫn cao; normal minimum chạy được không là calibration đủ |

## Hai quy tắc chung trước nhìn ranking score (chờ WHY)

1. **W-time ngắn chung:** normal300s và hậu300s tính bằng timestamp thật. Chỉ đưa vào bảng chung khi có đủ hai phía và cadence phù hợp. Thiếu thì đánh thiếu, không âm thầm clip. Sensitivity600s cùng cách chia khi cả hai đủ; report riêng mọi method. Đây là ứng viên từ cấu hình prior work L10, chưa được chọn cho P3.
2. **W-feasible chung:** chọn từ tập300/600s bằng kiểm normal/time coverage, missingness và yêu cầu fit đã ghi trong hồ sơ, trước chạy chấm root; chọn thời lượng lớn nhất **mọi method trong stratum đó** có đủ dữ liệu. Nếu không có giao, ghi không có bảng chung của stratum, không đổi method tới khi nó thắng. Sau đó sensitivity ở thời lượng còn lại đủ điều kiện. Không dùng Hit/MRR/NDCG/F1 để chọn.

Khuyến nghị quy tắc2, **chưa chốt một số phút**. Giả định: completeness/fit minimum xác định được bằng normal và schema trên dev sau G1. Sai khi normal “trước tiêm” đã có load/recovery hoặc đủ dòng nhưng không đủ healthy calibration; P3 sẽ kiểm điều kiện này bằng normal controls. Cửa sổ ngoài tác giả ghi là controlled comparison riêng; tái lập tác giả giữ configuration riêng, không trộn các bảng. Training/history dài hơn cửa sổ chấm được tách budget và khóa, không lén cấp thêm dữ liệu cho một method.

## Retrieval@K và Rerank@1 (chờ WHY)

Đề xuất E2 của T-018 trong `de-xuat-tai-lieu-chung.md` tách lỗi mất root ở bước tạo candidates khỏi lỗi xếp lại. Đề nghị thêm độ đo chẩn đoán ở P3, giữ MRR/NDCG/Hit@k cuối làm độ đo RCA chính. Không phải detector Precision/Recall.

- Quy đổi metric/operation/pod sang **service bằng inventory độc lập gold**; không gộp khác pod nếu chưa có mapping được chấp nhận. T018 nêu K5/K10; phải ghi K theo service, dedup trước K, candidate cap và ties. Metric-K của DecompRCA không đồng nghĩa service-K.
- Retrieval@K = tỷ lệ ca evaluator có root trong tập K ứng viên sau mapping; ghi denominator tất cả ca hợp lệ và ca gold vắng universe. Rerank@1 báo conditional trên ca đã retrieval thành công **và** tỷ lệ đúng cuối trên mọi ca. Denominator0 ghi NA, không0/1. Với multi-root cần evaluator riêng, không chọn tùy một root.
- RCAEval: có service-root nhưng frontend alias phải tường minh. Nezha/Eadro: clock/root mappings và license phải giải trước dùng; Bank: pod-level không tự thành service. LEMMA: instance/NFS ngoài app và timeline OPEN. DeepTraLog/LO2 không có nhãn root đúng task: không tính. Chi tiết từng 40 phần trong V4.
- Với RCAEval, K là prefix của thứ hạng đã lưu sau mapping/dedup, không tự là một module truy hồi độc lập. Rerank@1 có điều kiện không thay thế chất lượng cuối trên mọi ca.
- Chống lại khuyến nghị: thêm một báo cáo và mapping khiến người đọc hiểu conditional hit như hiệu quả cuối. Đổi khuyến nghị nếu candidates không quan sát được hoặc mapping không độc lập gold; giữ NA thay suy từ output đã bỏ root.

Không có phép chạy mới để quyết window, calibration hoặc retrieval trong T020. Công việc P3 cần Minh duyệt được ghi ở thẻ D4–D6 và phụ lục10.
