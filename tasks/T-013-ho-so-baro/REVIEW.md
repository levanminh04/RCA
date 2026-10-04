# Phản biện T-013

- **Người phản biện:** Claude — **Ngày:** 04/10/2026 — **Commit/diff đã đọc:** HEAD `93f13d4`; working tree chưa commit (T-013 là thư mục mới chưa theo dõi; `git diff` chỉ có một dòng T-013 trong `docs/STATE.md` thuộc task này).
- **Đã đọc:** `AGENTS.md`; `tasks/T-013-ho-so-baro/SPEC.md`, `LOG.md`; `results/T-013/` gồm `ho-so-baro.md`, `ho-so-bocpd.md`, `ho-so-nsigma-phat-hien.md`, `vi-du-tinh-tay.md`, `cua-so-va-che-do-b.md`, `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md`, `doi-chieu-tieu-chi.md`, `yeu-cau-dau-vao.csv`, `ca-da-chay.csv`, `doi-chieu-moc.json` (và `runs/moc-truoc-dinh-chinh.json`), `kiem-tra.json` (một phần), `kiem-ban-giao.json`, `manifest.json`, `moi-truong.md`, `scripts/kiem_co_che.py`, `trung-gian/` (`chon-ca.json`, `cua-so-cu.json`, `service-rank-ca.csv`, `T006-redis-IQR-*`), `runs/20261004-083543/TT-L10-robust-*`; `docs/LESSONS.md`, `docs/MRP.md` (RQ1, RQ3), DT18, hướng dẫn của cô. Code chỉ đọc: BR `e35f4ec` (`anomaly_detection.py`, `_bocpd.py`, `utility.py`, `root_cause_analysis.py`, `reproducibility.py`), RE `259ea41` (`e2e/baro.py`, `e2e/__init__.py`, `io/time_series.py`, `main.py`). Bài BARO arXiv 2405.09330v1 (HTML): §3.3, §3.4, Algorithm 1, Bảng 2, Bảng 3. Đầu ra từng ca T-006 đã lưu: `D:/RCA-ext/work/T-006/l4-nsigma-fse-ob-len10-lan1/output/results/` và `.../l4-nsigma-fse-ob-lan1/output/results/` (chỉ đọc, không chạy phương pháp).

## Kết luận chung

Ba hồ sơ đúng với code và bài ở các chỗ tôi kiểm. Không thấy nhãn lọt vào phương pháp, không ghi ngoài phạm vi. Có một lỗi chặn: yêu cầu 3 của task (giải thích **bằng cơ chế** vì sao ô N-Sigma fse-ob DELAY đổi 0,256 giữa cửa sổ 10 và 20) chưa được làm. Hai ca ví dụ không nằm trong ô đó, nên phần "giải thích" chỉ là bốn đường tác động chung. Dữ liệu để phân rã ô đó đã có sẵn từ T-006, không cần chạy lại.

## Các điểm

### R1. Chưa giải thích bằng cơ chế ô N-Sigma DELAY đổi 0,256 — CHẶN

- **Ở đâu:** `results/T-013/cua-so-va-che-do-b.md` §1; SPEC bước 4; `doi-chieu-tieu-chi.md` dòng tiêu chí 4. Bước chịu ảnh hưởng: đầu vào cho quyết định cửa sổ G1 (Q-54).
- **Sai gì:**
  - Task yêu cầu: "Giải thích bằng cơ chế vì sao kết quả đổi theo độ dài cửa sổ. T-006 mục 2.1 ghi một ô N-Sigma đổi 0,26." Tiêu chí 4 của SPEC: "chênh ô N-Sigma cũ kiểm bằng JSON và cơ chế từng ca".
  - T-013 chỉ đọc lại hai số tổng (0,936 và 0,680) rồi nêu bốn đường tác động chung (nền, hậu, tập cột, gộp service).
  - Hai ca dùng để "phân rã" là `re2tt_ts-auth-service_delay_3` (RE2-TT) và `fse-ob/cartservice_cpu/1` (ô CPU, không phải DELAY). Không ca nào thuộc ô fse-ob DELAY. Ô CPU còn đổi theo chiều ngược lại (0,896→0,920).
  - Câu "Các trung gian T-013 … cho phép thấy đường nào xảy ra ở từng ca" chỉ đúng cho hai ca trên. Nó không cho biết đường nào gây ra 0,256.
  - `doi-chieu-tieu-chi.md` vẫn ghi tiêu chí 4 là đạt.
- **Bằng chứng:**
  - Tôi đọc đầu ra từng ca T-006 đã lưu (không chạy phương pháp), gộp service theo luật `main.py:560–572`. Avg@5 DELAY tính lại khớp JSON: 0,936 (L10) và 0,680 (L20).
  - 15/25 ca DELAY đổi hạng service gốc: 13 ca tụt, 2 ca lên. Ví dụ: `currencyservice_delay_4` 1→6, `currencyservice_delay_5` 2→7, `checkoutservice_delay_3` 1→5.
  - Trong 13 ca tụt, 9 ca có metric `_mem` đứng đầu ở L20 (`recommendationservice_mem`, `emailservice_mem`, `main_mem`, `frontend_mem`). Đây là một mẫu hình cụ thể mà hồ sơ chưa xét. Tôi không khẳng định cơ chế. Chỉ nêu rằng dữ kiện phân xử đã có.
  - Ở fse-ob, L20 không phải 20 phút: file chỉ có 360+361 dòng, nên L20 là cả file. Hồ sơ có ghi điều này. Vậy khác biệt L10/L20 chỉ đến từ 60 dòng đầu file (vào nền) và 61 dòng cuối (vào hậu). Đây là phép phân rã rẻ, đúng trọng tâm, nhưng chưa làm.
  - Trái với QT15 (tách theo ô và theo ca trước khi nêu mẫu hình) và QT19 (kiểm rẻ thì kiểm trong task).
- **Đoạn có thể phản bác:** §1 viết "không quy toàn bộ 0.256 cho một metric hay riêng std", và SPEC bước 4 chỉ hứa "phân rã trên hai ca". Câu đó tránh nói sai, nhưng không thay được lời giải thích mà task yêu cầu. SPEC tự duyệt đã thu hẹp yêu cầu mà không nêu hệ quả (SL26).
- **Đề xuất sửa:**
  - Dùng đầu ra từng ca T-006 đã có. Với 25 ca DELAY, so metric thắng của service gốc và của service đứng trên ở L10/L20.
  - Tách tác động của 60 dòng đầu (mean/std nền) và 61 dòng cuối (max hậu). Chỉ cần đọc mean/std/max trên dữ liệu fse-ob không khóa; không benchmark lại.
  - Ghi kết quả vào `cua-so-va-che-do-b.md` §1 và sửa dòng tiêu chí 4 trong `doi-chieu-tieu-chi.md`. Không chọn cửa sổ.

## Điều đã kiểm và thấy đúng

- **Hồ sơ đúng với code** (kiểm cả ba hồ sơ, không chỉ mẫu ngẫu nhiên):
  - RobustScorer/N-Sigma RCA dùng max **có dấu**; bài viết `|x−med|/IQR`; nhánh dict dùng quantile theo chỉ số, `abs(max−median)`, cần ≥4 mẫu nền.
  - Khác BR/RE: `dataset=None`, `causalrca-sock-shop`, cột thời gian, guard nửa rỗng, `-db`.
  - Runner RE lấy `L*60//2` dòng mỗi phía, có SLI suy từ service gốc nhưng hàm không đọc.
  - BOCPD: hazard 1/50; prior ν=d+1, κ=1, μ=0, S=I; t-predictive m₀=2, Σ₀=I; luật `|Δmode|>1`.
  - Lỗi `maxes[T]` không được gán, sinh điểm T ngoài dữ liệu. Có thêm độ trễ một dòng vì `maxes[t]=argmax R[:,t]`, nhưng không ảnh hưởng kết luận.
  - `reproduce_bocpd` cắt 300+300 quanh mốc tiêm, chỉ lấy `latency-50`/`_error`, chấm TP/FP theo ca, crash ở `cps[0]` khi rỗng.
  - N-Sigma phát hiện: `ddof=1`, nền mở rộng từ dòng 0, list không sắp, không bỏ trùng.
- **Hồ sơ đúng với bài:** §3.3 (mean 0, inverse-Wishart), Algorithm 1 (`s_t ≤ s_{t−1}`), giả định latency/error ở §3.1. `doi-chieu-moc.json` sau đính chính khớp Bảng 2 và Bảng 3 (RobustScorer/N-Sigma[t_inject], OB và SS). Lỗi chép bảng đã được ghi và giữ dấu vết. Không có phép đo nào dựa trên ô chép nhầm.
- **Số trong văn bản khớp file:**
  - Thế số tay: 33,5836; 224; mật độ 0,353553; posterior (0,02; 0,98); hai dòng N-Sigma phát hiện.
  - Hạng gốc TT (11/10/24/13) và OB khớp `service-rank-ca.csv`.
  - 0,256 khớp `cua-so-cu.json`.
  - IQR thô 90/90 bằng 0 khớp `T006-redis-IQR-summary.json`.
  - Sentinel 99/100, TP=100/FP=31 không đổi khớp `kiem-tra.json`.
  - R cho T=1441 bằng 8·1442² byte = 15,864 MiB.
- **Nhãn:**
  - Ca TT chọn theo kích thước file, trong đúng 30 ca dev (script assert 30).
  - Tên service gốc chỉ được tách ra sau khi lưu ranks và không là đối số của hàm.
  - Mốc tiêm chỉ dùng trong chế độ (a) và để cắt cửa sổ như runner.
  - Không đọc `data/locked/`.
  - Bảng ba đường rò (min–max toàn cửa sổ, cửa sổ quanh mốc, biên file đối xứng) đúng. Nhận xét min–max không đổi cảnh báo N-Sigma (affine dương) nhưng có đổi posterior BOCPD (prior cố định) là đúng.
- **Phạm vi ghi:** chỉ T-013, một dòng STATE, hai file trong `D:/RCA-ext/work/T-013/`. Hai source vẫn ở đúng HEAD, status sạch.
- **Câu hỏi trọng tâm G1:** T-013 không đổi danh sách phương pháp, không chọn dataset, không chia dev/test. Vì vậy các câu "phủ đủ họ", "dataset phân xử RQ1/RQ3", "chia dev/test" không áp dụng cho task này. Hồ sơ đúng khi kết luận BARO, BOCPD, N-Sigma không dùng đồ thị ở vai trò nào. Thông tin cấu trúc duy nhất còn lại là ánh xạ tên metric→service.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng — lỗi CHẶN đã sửa theo Minh | Trước sửa hồ sơ không giải thích đúng ô DELAY. Đã bổ sung đủ 25 ca × 4 phối hợp nền/hậu; 50 endpoint khớp từng metric và service rank T-006, 100 phối hợp kiểm lặp/đảo cột giữ điểm. Avg@5 là 0,936/0,712/0,936/0,680; trung bình hai thứ tự phân bổ nền −0,240, hậu −0,016, bao gồm bốn ca đổi candidate. §1 có trung gian từng metric, ba ca cụ thể và giới hạn nhân quả; tiêu chí 4 đã cập nhật. Không chốt L. Nguồn: results/T-013/trung-gian/cua-so-delay-summary.json và run sua-R1-20261004-195903. | Minh duyệt sửa 04/10/2026: “sửa lại các lỗi trên, test cẩn thận”. Minh duyệt đóng task và commit sau sửa. |
| N1 | Đúng (tự tìm S1) — đã sửa helper | Thiếu variance bù sai số/near-constant bound đã sửa trong scripts/kiem_co_che.py. Phản ví dụ điểm cũ 5,057563 nay 18, khớp StandardScaler ghim, scale hiệu dụng 1. Tám synthetic và tám cấu hình hai ca gốc khớp 1.316 điểm chính thức (normalized error 0); so điểm lịch sử sai số ≤2,35e-16, mọi rank giữ nguyên. Kiểm lặp/đảo cột đạt; output cũ giữ nguyên. Nguồn: runs/sua-N1-20261004-195501/ket-qua.json. | Minh duyệt sửa 04/10/2026: “sửa lại các lỗi trên, test cẩn thận”. Minh duyệt đóng task và commit sau sửa. |
| N2 | Đúng (tự tìm S2) — đã sửa mô tả | Hồ sơ N-Sigma phát hiện đã ghi n là số mẫu không NaN, công thức cần giá trị hữu hạn, inf không tự loại. Phản ví dụ pandas count 3/finite 2, mean Infinity/std NaN được giữ trong checks; không ảnh hưởng ví dụ hữu hạn cũ. | Minh duyệt sửa 04/10/2026: “sửa lại các lỗi trên, test cẩn thận”. Minh duyệt đóng task và commit sau sửa. |
| N3 | Đúng (tự tìm S3) — đã sửa điều kiện | Hồ sơ BOCPD đã thêm tổng mass dương và hữu hạn để suy q_t(0)=0,02. Kiểm core mass 0/posterior NaN và mass dương/posterior (0,02;0,98) xác nhận điều kiện; không suy wrapper min–max lỗi trên cùng input. Không sửa code tác giả. | Minh duyệt sửa 04/10/2026: “sửa lại các lỗi trên, test cẩn thận”. Minh duyệt đóng task và commit sau sửa. |
