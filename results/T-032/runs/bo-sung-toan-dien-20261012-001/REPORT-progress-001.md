# Gói bổ sung T032/T033 — báo cáo tiến độ, 13/10/2026

Gói chưa hoàn tất. Bản này là mục lục bằng chứng và việc đang làm, không thay báo cáo cuối hoặc nghiệm thu hai task cũ.

## Trạng thái tính toán

Kiểm file trên hai EC2 lúc 00:24 ngày13/10: 188/240 slot PASS, còn52 slot. Mỗi slot là một ca × một cấu hình, gồm30 native sham và210 nhánh can thiệp. Đây là trạng thái tính toán, không là phần trăm câu hỏi nghiên cứu đã trả lời.

| Phần | Trạng thái | Bằng chứng |
|---|---|---|
| EC2 T33, ca1–14 | Đủ14 native +98 nhánh; đã nhận116 file/5.997.473 byte gồm output và metadata | `engine-progress-001.json`; `../../../T-033/runs/bo-sung-toan-dien-20261012-001/t33/owned-engine-verification-001.json` và `root-owned-receipt-verification-001.json` tại thư mục đó |
| EC2 T32, ca15–30 |76/128 slot PASS; ca15–22 xong toàn bộ; ca23–24 đang chạy | `engine-progress-001.json#/hosts`; controller tại `t32/t33-migration-001/` |
| T032 core | Có báo cáo và kiểm số/source, giữ đầy đủ ca lỗi/thiếu support | `t32/REPORT.md`, `t32/findings.json`, `t32/core-verification-001.json` |
| TraceRCA tác giả, nhánh đầu vào hỗ trợ |208 slot đã lưu; receipt/scalar audit có phạm vi cụ thể | `root-probes-report-v2.md`; `audit/root-receipt019-verification-002.json` |
| TORAI A encoder/influence |Audit số học đạt; hai ô khác giữa recipe đã đính chính; predicate descendant đang kiểm tiếp | `root-probes-report-v2.md`; `audit/toraiA-encoder-influence-verification-002.json`; `t32/kt7-predicate-design-001.md` |
| T033 theta/marginal/zero/rolling/log |Đã có đầu ra; backend literal mới đang kiểm nguồn và audit độc lập | T033 `t33/` summaries, receipts và audit T032 `audit/` |

## Việc phải hoàn tất trước báo cáo cuối

1. Nhận phần EC2 T32 sau khi hoàn thành, kiểm đủ ownership30ca×8, native gates, lỗi, hash và cấu trúc output; giữ tất cả lượt hỏng.
2. Hoàn tất gate cùng predicate `hasroot` của TORAI A trên matched A superset và native conditional top-k; điều chỉnh kết luận theo kết quả thực, không theo kỳ vọng số0.
3. Kiểm backend literal Response/ResponseEntity, conservation, vị trí nguồn và các giới hạn nối invocation. Không đồng nhất status0/1 với thành công/thất bại khi semantics chưa xác minh.
4. Tổng hợp BOCPD theo từng ca/nhánh, nối prior/marginal/zero, causal schema/warmup/coordinate drift, compressed likelihood/run-length/time mapping. Không chấm physical onset hoặc false alarm vận hành từ proxy/CPcount.
5. Hoàn thiện ledgerKT1–16/K1–7, chỉ rõ bằng chứng phân xử, các giải thích còn lại, trường quan sát thiếu và phần thiết kế/đánh giá P5/P6/test. Kiểm toán các kết luận vật chất trước chốt.
6. Hoàn thiện báo cáo toàn gói, manifest, LOG, đúng hai dòng STATE, kiểm prefix/diff; prompt bàn giao theo mẫu để Minh tự chuyển. Tắt heartbeat khi thực sự hoàn tất.

## Kiểm toàn vẹn

`old-immutable-verification.json` đã PASS155.209 file cũ. `controlled-verification-002.json` xác nhận prefix DECISIONS/WHY/hai LOG giữ nguyên và STATE chỉ đổi hai dòng trạng thái. Chưa cần lặp quét toàn bộ file cũ vì chưa xuất hiện rủi ro mới. Các sửa diễn giải mới nằm trong bản bổ sung mới; baseline và báo cáo lịch sử giữ nguyên.

Mốc tiếp nhận chi tiết ở `checkpoint-root-004.md`. Các tiến trình EC2 chạy độc lập; laptop/Codex cần mở để lịch cùng chat tiếp tục nhận và kiểm kết quả. Không dùng tình trạng máy chạy xong thay bằng chứng khoa học.
