# Vấn đề ở task cũ — để reviewer kiểm

T-013 không sửa file task cũ. Phạm vi soát: kết luận phương pháp/đầu vào/mốc/thời gian/biên liên quan BARO và detector trong T-000–012; các thẻ khác được đối chiếu phần input/leak, không chạy lại phương pháp khác. T-004 chưa triển khai. Inventory và dòng liên quan ở `trung-gian/task-cu-relevant-source-audit.json`. Không xem index tự sinh là kiểm tính đúng toàn bộ số liệu ngoài phạm vi T-013.

## D1. K1 mô tả công thức bài như thể cùng code, và đơn vị chấm detector

- Task/nguồn: T-000/K1 `docs/knowledge/K1-phuong-phap-rca.md:189,191`.
- Vấn đề: công thức hai phía của bài chưa phân biệt max có dấu DataFrame/nhánh dict; đơn vị chấm gọi samples không đúng artifact case-level.
- Bằng chứng: BR `root_cause_analysis.py:213–230,312–315`; RE `baro.py:49–52`; BR `reproducibility.py:168–181`. Phản ví dụ đã chạy: `dict-vs-dataframe-*`, `edge-falling` trong `kiem-tra.json`. DataFrame có thể điểm âm; dict có thể 0 với một giảm lớn.
- Kết luận ảnh hưởng: hiểu cơ chế, lỗi giảm tín hiệu, ý nghĩa P/R/F1; không có bằng chứng phải đổi số FSE cũ.
- Đã triển khai T-013: hồ sơ tách ba công thức, script độc lập so official, chấm lại artifact bằng counts.
- Cũ→mới: thêm sau công thức K1: “Đây là công thức bài; hai DataFrame implementation dùng max có dấu; nhánh dict khác quantile và dùng abs(max−median).” Đổi đơn vị detector thành “artifact đếm theo ca, một ca có thể góp cả TP và FP; chưa phải window-level P/R/F1”. Nháp nguyên văn trong `de-xuat-tai-lieu-chung.md`.

## D2. T-006 suy IQR=0 chỉ từ scale=1: kết luận đúng, chứng minh thiếu

- File:dòng: `results/T-006/scripts/soi_baro_redis.py:38–39`; `kiem-dung-dan.md:132`.
- Sai gì: cờ IQR = 0 dùng `scaler.scale_==1`; scale = 1 cũng xảy ra với IQR thật bằng 1 hoặc IQR rất nhỏ.
- Bằng chứng: sklearn ghim `_data.py:111,1660–1661`; synthetic IQR = 0; T-013 tính **IQR thô** trên 90 baseline torai-OB, không chạy benchmark/scorer toàn tập. CSV `trung-gian/T006-redis-IQR-raw.csv`, summary:90/90 IQR thật bằng 0,90/90 không hằng.
- Kết luận ảnh hưởng: số78/90 redis đứng đầu của T-006 không bị bác; lý do IQR = 0 được bổ sung bằng chứng trực tiếp. Không gọi đây là số kết quả cũ sai.
- Đã triển khai: script `kiem_ket_qua_cu.py` tính q25/q75/IQR và phân biệt scale hiệu dụng, giữ kết quả cũ.
- Cũ→mới: “Trong đoạn trước mốc tiêm, kênh này có IQR=0” → “T-013 tính trực tiếp q25/q75 trên baseline 300 dòng của90 ca: IQR thô redis_diskio bằng 0 ở90/90 ca; scale = 1 riêng nó không chứng minh IQR = 0. Các số đứng đầu/điểm vẫn lấy từ lượt T-006.”

## D3. T-007 khớp tác giả nhưng có sentinel ngoài dữ liệu

- File:dòng: `results/T-007/kiem-dung-dan.md:21,227–231`; BR `_bocpd.py:196,225`, `utility.py:212`.
- Vấn đề: cần giới hạn cách hiểu “chạy đúng”: code không ghi mode cuối và dùng maxes[T]=0 còn sót, có thể phát sinh điểm T ngoài chuỗi. Tái lập code có lỗi vẫn có thể khớp100/100.
- Bằng chứng: `edge-no-change`, hai prefix 120 thật và `T007-sentinel-audit` trong `kiem-tra.json`; artifact chỉ đọc100 ca fse-ob.99/100 có điểm 600; không ca nào chỉ có sentinel hoặc lấy nó làm điểm đầu. Bỏ riêng sentinel vẫn TP=100/FP=31 và P/R/F1 như cũ. Không nói Recall = 1 tập OB do sentinel.
- Đã triển khai: cài recurrence độc lập, lưu posterior/last-mode/cps và chấm lại counts sau loại riêng điểm ngoài range trong T-013; không sửa code tác giả, không benchmark mới.
- Cũ→mới: thêm “Khớp đầu ra tác giả ở100/100 ca. T-013 phát hiện điểm cuối600 ngoài window 600 ở99/100 ca do maxes cuối chưa gán; loại riêng điểm này không đổi P/R/F1 của tập OB. Tái lập này không chứng minh extraction heuristic không lỗi.”

## D4. T-006: Recall = 1 không là bảo đảm của mọi dữ liệu

- File:dòng: `results/T-006/kiem-dung-dan.md:83,286`.
- Vấn đề: câu “TP tính cho mọi ca có cảnh báo, do đó R luôn bằng 1” thiếu điều kiện mọi ca thực tế có cảnh báo. Nếu có ca rỗng, FN tăng hoặc runner tác giả crash tại cps[0].
- Bằng chứng: `edge-nsigma-start-100`, `edge-bocpd-all-constant`, `edge-bocpd-only-time` trả[]; source BR `reproducibility.py:168–173`. Counts cũ thật vẫn có alarm ở mọi ca.
- Kết luận ảnh hưởng: không đổi số T-006; sửa diễn giải độ đo, không suy Recall là tính chất detector.
- Đã triển khai: synthetic normal/short/constant và chấm lại artifact trong T-013.
- Cũ→mới: “R luôn bằng1” → “R = 1 trong các tập đã chạy vì mọi ca đều có ít nhất một cảnh báo; luật chấm không bảo đảm điều này trên dữ liệu khác. TP/FP có thể cùng đến từ một ca, nên số này không phải window-level P/R/F1.”

## D5. T-001 cần tách bộ nhớ ma trận với chi phí toàn detector

- File:dòng: `results/T-001/danh-sach-phuong-phap.md:276`.
- Vấn đề: mô tả window24 phút “nhẹ” có thể bị đọc thành toàn phương pháp nhẹ; R chỉ là một phần memory, runtime phụ thuộc d.
- Bằng chứng: T-005 `runs/ket-qua-do.jsonl:17` method1440.133s cho600 điểm; full1441 bị dừng sau 1 giờ. T-013 tính R riêng và tổng evaluations ở `trung-gian/chi-phi-va-sentinel.json`.
- Kết luận ảnh hưởng: tổng ngân sách Q-40/khả thi; không bác ma trận R vốn nhỏ.
- Cũ→mới: “cửa sổ24 phút…nhẹ” → “R riêng cho T=1441 dùng15.864 MiB, còn states covariance O(Td²) và runtime O(T²d³) trong implementation; cần tính tổng ca, không suy detector nhẹ từ R.”

## Không nâng thành lỗi

T-006 mốc A reproduce_baro dùng điểm detector lưu sẵn; file đã phân biệt mốc/tái lập, nên T-013 bổ sung phạm vi tại chỗ dùng, không khẳng định số tái lập cũ sai. BR/RE N-Sigma cùng lõi scoring trong cấu hình FSE đã dùng; khác preprocess ở default không tự bác sự tương đương của các lượt FSE cũ. Chênh 0.26 là làm tròn của 0.256, không là lỗi số liệu. Không có vấn đề mới có bằng chứng ở T-002/T-003/T-008–012 trong phần trực tiếp liên quan T-013; các OPEN license/onset/dataset split vẫn OPEN, không biến thành lỗi.
