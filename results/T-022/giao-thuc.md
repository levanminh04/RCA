# Giao thức P3 trên RE2-TT dev — bản nháp

Ngày 05/10/2026. T-022, người làm Claude. **Trạng thái: nháp.** Phần ghi DECIDED là quyết định Minh đã có (DECISIONS). Phần ghi CANDIDATE là đề xuất trong `lua-chon-can-duyet.md`, chưa được dùng. Không phần CANDIDATE nào được bật mặc định trong code hay số khoa học trước khi Minh quyết và WHY được ghi.

Phục vụ: RQ1 (phương pháp đã có hoạt động thế nào), RQ2 (hỏng ở đâu), DT18-NV3 (thực nghiệm trên dữ liệu công khai), nhận xét của cô "mở rộng thực nghiệm" và "chỉ ra hạn chế".

## 1. Phạm vi

- Dataset: 30 ca dev RE2-TT (`allowlist-dev.json`). Không mở 60 ca test, không mở RE3-OB (luật cứng 1).
- Phương pháp tầng 1 (Q-62, DECIDED): BARO (RobustScorer), SimpleRCA (M4, T-017), MicroRank-RCAEval sửa đầu vào, TraceRCA lọc hữu hạn, CIRCA đồ thị kiến trúc, TORAI bản sửa (WHY-19). Bộ phát hiện: N-Sigma, BOCPD (tập cột Q-67).
- Ngoài phạm vi T-022: benchmark đủ 30 ca × 6 phương pháp (T-024), chạy đủ chế độ (b) (T-025), adapter Nezha/Eadro (T-026/T-027), tầng 2.

## 2. Trạng thái từng thành phần

| Thành phần | Trạng thái | Nguồn |
|---|---|---|
| Dataset, chia dev | DECIDED | Q-61, Q-63, T-021 gói A; allowlist kiểm ở `runs/allowlist-001/` |
| Độ dài cửa sổ 300 s sau, ≤ 300 s trước | DECIDED | Q-64 |
| Cách cắt cửa sổ trên từng nguồn | CANDIDATE | lựa chọn mục 1 |
| Mốc tiêm là thông tin vận hành ở chế độ (a); ngân sách nhãn root 0 | DECIDED | Q-66 |
| Độ đo xếp hạng (MRR, NDCG@5, Hit@1/3/5, AC@k, Avg@5, Retrieval@5/10, Rerank@1) | DECIDED (danh sách) | MRP P7, Q-65 |
| Hòa, ca lỗi, bootstrap | CANDIDATE | mục 8, 9 |
| Tập cột BOCPD | DECIDED | Q-67; chạy EC2 qua đêm ở T-025: Q-72 |
| Nguồn đầu vào TORAI | CANDIDATE | mục 2 |
| Universe, ánh xạ thực thể | CANDIDATE | mục 3 |
| Bộ cột metric | CANDIDATE | mục 4 |
| Cấu hình CIRCA, MicroRank, TraceRCA | CANDIDATE | mục 5–7 |
| Chế độ (b): phạm vi, chuỗi, tiền xử lý, cột N-Sigma, episode, chấm, ghép ranker | CANDIDATE | mục 10–11 |
| Seed và tham số | DECIDED một phần (WHY-20, Q-66); CANDIDATE phần còn lại | mục 12 |
| Tổ chức task | OPEN | mục 0 |

## 3. Dữ liệu và tách nhãn

- `allowlist-dev.json`: 30 ca; mỗi ca có mã mờ `dev-<10 hex>` (lấy từ SHA-256 metrics, không mang nhãn), đường dẫn dưới `data/rcaeval/`, SHA-256 và byte của từng file. Chỉ runner đọc.
- `nhan-dev.json`: root, loại lỗi, ô, nhóm vị trí, mốc tiêm và nguồn mốc (SHA-256 file `inject_time.txt` từ HF revision `afeacb11`). Chỉ runner (lấy mốc cho chế độ a) và evaluator đọc.
- Phương pháp và bộ phát hiện không nhận tên ca, mã mờ, đường dẫn hay file nhãn. Runner đọc file, cắt cửa sổ, rồi đưa bảng dữ liệu cho phương pháp.
- Kiểm toàn vẹn trước mỗi lượt: SHA-256 của file đọc phải trùng allowlist; sai thì ERROR, không chạy.

## 4. Ai biết gì, lúc nào

| Tác nhân | Chế độ (a) | Chế độ (b) |
|---|---|---|
| Runner | allowlist, mốc tiêm (để cắt cửa sổ) | allowlist; không đọc mốc cho tới khi bộ phát hiện xong |
| Bộ phát hiện | — | bảng metric cả bản ghi (cột `time` + cột đã chọn); không mốc, không root, không tên ca |
| Ranker | bảng của cửa sổ N∪A và mốc `t` | bảng của cửa sổ quanh thời điểm báo động `t̂` và `t̂` |
| Evaluator | danh sách xếp hạng đã lưu + nhãn | báo động/episode đã lưu + nhãn; xếp hạng đã lưu + nhãn |

Nhãn chỉ được nối sau khi đầu ra đã ghi ra file. Đổi locator (đường dẫn, tên ca) mà giữ nội dung dữ liệu phải giữ nguyên đầu ra (phép kiểm ở mục 10).

## 5. Chế độ (a) — biết trước thời điểm

1. Runner lấy `t` = mốc tiêm từ `nhan-dev.json`.
2. Cắt cửa sổ theo timestamp: N = [t−300, t), A = [t, t+300) (CANDIDATE, mục 1); metric theo `time`, span theo `startTime`, log theo `timestamp`; TORAI 20 dòng 15 s mỗi phía.
3. Tiền xử lý: theo đúng code tác giả của từng phương pháp (RCAEval `main.py` cho BARO, CIRCA, TORAI metric; T-017 cho SimpleRCA). Runner không thêm bước chung.
4. Gọi phương pháp; lưu bản ghi (mục 9).
5. Evaluator chấm (mục 8).

## 6. Chế độ (b) — tự phát hiện (CANDIDATE, mục 10–11)

1. Bộ phát hiện nhận cả bản ghi 1.441 điểm, tập cột theo Q-67 (BOCPD) và theo lựa chọn Q12 (N-Sigma). Tiền xử lý theo code tác giả; look-ahead của BOCPD được khai báo.
2. Danh sách báo động: bỏ sentinel ở chỉ số T (BOCPD); sắp và bỏ trùng (N-Sigma); đổi chỉ số sang timestamp.
3. Gộp episode: thời gian trơ 300 s.
4. Lưu báo động và episode trước khi nối nhãn.
5. RCA: episode đầu tiên kích hoạt; cửa sổ Q-64 quanh `t̂`; chỉ cho BARO, CIRCA kiến trúc, TORAI.
6. Evaluator chấm phát hiện (bảng riêng, Q-30) và chấm RCA như chế độ (a).

Đây là **phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố**, không phải giám sát online. Mốc RE2-TT luôn ở giây 720, nên không có lịch chia đoạn nào độc lập thật với mốc.

## 7. Phương pháp tầng 1

| Phương pháp | Code | Môi trường | Đầu vào trong cửa sổ | Đơn vị đầu ra → thực thể | Trạng thái đặc biệt |
|---|---|---|---|---|---|
| BARO RobustScorer | RCAEval `e2e/baro.py` | T-014-main + PYTHONPATH | metric | metric → tiền tố trước `_` | nửa rỗng/không còn cột → NO_EVIDENCE hoặc ERROR |
| SimpleRCA M4 | `src/simplerca` | T-014-main hoặc T-017-simple | metric, trace, log | service (alias tường minh, WHY-17) | điểm toàn 0 → NO_EVIDENCE (abstain, WHY-17) |
| MicroRank sửa | `src/microrank` | T-014-main | trace | operation → `serviceName` | không trace bất thường → NO_EVIDENCE; ID trùng khác nội dung → ERROR |
| TraceRCA lọc hữu hạn | RCAEval `e2e/tracerca.py` + lọc trong `src/p3` | T-014-main | trace | operation → `serviceName` | không span bất thường → NO_EVIDENCE |
| CIRCA kiến trúc | `src/circa_kien_truc` + CIRCA `0215e18` | T-014-main + PYTHONPATH CIRCA | metric, trace trong N (đồ thị) | metric → tiền tố | đồ thị có chu trình: ghi; ValueError RHT: ghi cảnh báo |
| TORAI sửa | `src/torai/torai_sua.py` | py38-rcdlock (tiến trình riêng) | metric + logts/tracets (nguồn theo Q3) | `<service>_A` | đếm cụm rơi nhánh dự phòng; không truyền `service`, `fault_type`, `case` của chữ ký `torai()` |

PYTHONPATH đã kiểm import được (LOG phiên 1): `D:/RCA-ext/src/RCAEval;D:/RCA-ext/src/baro;D:/RCA-flashticket/src`. Không sửa môi trường hay code phương pháp đã có.

## 8. Chấm

- Mức thực thể; universe U = 68 thực thể `ts-*` (CANDIDATE, mục 3; file `mappings/universe-re2tt-dev.json`).
- Mọi ca ở mẫu số; trạng thái khác `OK` tính trượt (CANDIDATE, mục 8).
- Hòa: kỳ vọng trong nhóm hòa + cận (CANDIDATE, mục 9). Hàm RCAEval nhận danh sách phá hòa theo tên.
- Độ đo tự cài và kiểm bằng fixture: MRR, NDCG@5 (một root: 1/log2(1+r) nếu r ≤ 5), Hit@1/3/5. Độ đo gọi RCAEval: AC@1/3/5, Avg@5, Retrieval@5/10, Rerank@1.
- Bootstrap theo ô (CANDIDATE, mục 9). Báo theo lỗi, ô, nhóm vị trí và từng ca; số ca theo trạng thái.
- Phát hiện (chế độ b): theo episode, theo ca, theo cửa sổ 60 s, FP/giờ bình thường, độ trễ từ lúc tiêm (CANDIDATE, mục 11).

## 9. Bản ghi mỗi lượt (đề xuất cấu trúc)

```json
{
  "run_id": "...", "opaque_id": "dev-…", "method": "baro", "method_version": "RCAEval 259ea41 e2e/baro.py",
  "mode": "a|b", "detector": null, "seed": null, "config_id": "…", "config_status": "proposed|approved",
  "window": {"t": 0, "N": [0, 0], "A": [0, 0], "rows_N": 0, "rows_A": 0, "seconds_N": 0, "seconds_A": 0},
  "input_shape": {"metric_cols": 0, "spans": 0, "log_rows": 0},
  "status": "OK|NO_EVIDENCE|ERROR|UNSUPPORTED|TIMEOUT", "error": null,
  "ranking": [{"item": "ts-x_cpu", "entity": "ts-x", "score": 0.0}],
  "entity_ranking": [{"entity": "ts-x", "score": 0.0}],
  "diagnostics": {"fallback_clusters": null, "rank_equals_column_order": false},
  "cost": {"wall_s": 0.0, "peak_rss_mb": null, "read_bytes": 0, "write_bytes": 0, "exit_code": 0},
  "input_sha256": {"metrics.parquet": "…"}
}
```

Không có trường nhãn trong bản ghi của phương pháp. Evaluator ghi file riêng có nhãn.

## 10. Kiểm đúng đắn cần cài ở bước 3 (theo SPEC)

1. Selector từ chối: ca ngoài allowlist, đường dẫn trong `data/locked/`, path traversal (`..`), mã sai dạng; hash sai.
2. Đổi locator giữ nội dung (chép một ca sang tên trung tính trong `results/T-022/work/`) → đầu ra phương pháp giống hệt.
3. Fixture evaluator biết đáp án: hạng đúng, hòa, danh sách ngắn, trùng thực thể, root vắng, điểm không hữu hạn, ERROR, NO_EVIDENCE. Tính độc lập rồi đối chiếu RCAEval (AC@k, Avg@5, Retrieval, Rerank).
4. Xếp hạng ngẫu nhiên: kỳ vọng Hit@k = min(k, n)/n khi root trong n ứng viên quan sát; kiểm bằng nhiều seed với sai số chuẩn, không đòi một lần gần mốc.
5. Hai cửa sổ đều bình thường (N và một đoạn trước N trong 720 s đầu): phương pháp không được coi là "tìm ra nguyên nhân"; báo điểm và trạng thái, không chỉnh ngưỡng.
6. Hoán vị dòng/cột phù hợp từng phương pháp: thứ hạng bất biến ngoài nhóm hòa.
7. Bộ phát hiện: fixture biết đáp án cho báo động, sentinel, warm-up, đổi chỉ số → timestamp; đổi nhãn/mốc phía evaluator không đổi báo động đầu vào chế độ (b).
8. Bộ cột: so trước/sau xử lý, ghi dấu vắng cột; tương quan với nhãn chỉ ở audit evaluator.

## 11. Giới hạn đã biết

- RE2-TT có 5 service gốc ở 5 vị trí cố định; đồ thị gần như hằng giữa các ca (LESSONS ST3). Kết quả RE2-TT không khái quát cho topology khác.
- Cửa sổ 300 s khác ±600 s của các phép tái lập MicroRank/TraceRCA (T-007); số P3 không so trực tiếp với Bảng 2 bài TORAI.
- Chế độ (b) chỉ là phát hiện hồi cứu; không có khoảng âm đủ dài để nói về vận hành liên tục; dữ liệu bình thường 6 giờ tổng (30 × 720 s).
- TORAI dùng `logts/tracets` của tác giả nếu chọn A ở mục 2; khác nguồn log với SimpleRCA ở ít nhất 1 ca.
- Chi phí BOCPD trên 1.441 điểm với tập cột Q-67 chưa đo.
