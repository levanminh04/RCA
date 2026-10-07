# T-024 — Chấm tầng 1 chế độ (a) trên 30 ca dev RE2-TT

- **Trạng thái:** đã duyệt 06/10/2026 (lời Minh: "bạn tạo spec cho 2 task luôn cho tôi"; phân công: "codex làm 24"). Người làm rà lại SPEC trước khi triển khai (bước 0).
- **Người làm:** Codex.
- **Người phản biện:** Claude.
- **Thuộc gói MRP:** P3 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ1 và DT18-NV3 (so phương pháp RCA cơ sở bằng độ đo chuẩn), bước 4 trong hướng dẫn của cô. Trả lời: ở chế độ (a) — biết trước mốc tiêm — sáu phương pháp tầng 1 (BARO, SimpleRCA, MicroRank, TraceRCA, CIRCA kiến trúc, TORAI) xếp root ra sao trên 30 ca dev RE2-TT, theo đúng giao thức V2 và cấu hình đã khóa ở T-031. Không kết luận về đồ thị (P4).

## Đầu vào

- Giao thức `results/T-022/giao-thuc-v2.md` (mục 3–6, 8, 9, 10, 13); cấu hình `results/T-022/cau-hinh/p3-re2tt-v2.json`.
- `results/T-022/allowlist-dev.json`, `results/T-022/nhan-dev.json`, `results/T-022/mappings/universe-re2tt-dev.json`.
- Mã `src/p3/` (hash tổng `8d4cc8196c87ee56…`, cách tính và đầy đủ ở `results/T-031/moi-truong.json`); test T-030 ở `results/T-030/tests/`.
- Khóa cấu hình: `results/T-031/khoa-cau-hinh.md` (CIRCA OLS+RHT+DA, Q-80, Q-82; TORAI nguồn B). Đề xuất TIMEOUT và phạm vi: `results/T-031/do-chi-phi.md` mục 6–7.
- Bản ghi T-031 dùng lại (cùng hash `src/p3`):
  - CIRCA OLS: `results/T-031/runs/circa-ols-h0-001` (chính); SVR: `circa-svr-h0-lan1-001` (cấu hình phụ).
  - TORAI: `runs/torai-B-ec2-001` (chính, 3 seed), `runs/torai-A-ec2-001` (phụ).
  - MicroRank: `runs/microrank-30-001` (26 OK, 4 ERROR tính trượt, lời Minh LOG T-031 13:30).
- Ca pilot và yếu tố: `results/T-031/ca-pilot.json`, `results/T-031/runs/yeu-to-002/`.
- Môi trường: `D:/RCA-ext/envs/T-014-main` (Python 3.12), `py38-rcdlock`, `T-016-cong-cu`; lệnh mẫu ở `results/T-031/moi-truong.json` → `lenh_chay`.

## Đầu ra

Trong `results/T-024/`:
- `runs/<run-id>/`: lượt BARO, SimpleRCA, TraceRCA trên 30 ca (bản ghi §13, stdout/stderr, tiến độ, thời gian, RSS); giữ cả lượt hỏng.
- `ban-ghi-dua-vao-cham.json`: danh sách mọi bản ghi đưa vào evaluator (phương pháp, biến thể, seed, đường dẫn, SHA-256, hash `src/p3` của lượt). Ghi trước lượt evaluator đầu tiên.
- `cham-a.json`: số của mọi bảng dưới đây, theo từng ca và gộp.
- `cham-a.md`: báo cáo, mỗi số kèm đường dẫn nguồn:
  - bảng chính §8.5 (giá trị kỳ vọng theo hòa, cận lạc quan/bi quan cho độ đo đơn điệu);
  - bảng RCAEval riêng §8.6; mức ngẫu nhiên §8.7; bootstrap theo ô §8.8 (kể cả so cặp);
  - chia theo loại lỗi, ô, nhóm vị trí root, từng ca (§8.9); số ca theo trạng thái; bốn tập §8.1; audit cột §10;
  - CIRCA: trên 30 ca và riêng 19 ca không vượt ngưỡng 1e10 (Q-82, `results/T-031/kiem-11-ca-hashseed.json`); kèm RHT-only và SVR cấu hình phụ;
  - TORAI: trung bình 3 seed theo ca (§8.8), khoảng giữa seed; nguồn A báo phụ;
  - MicroRank: bảng chính theo xếp đầy đủ; kèm `top11` (§6.3).
- `scripts/`: script chạy và chấm.

## Phạm vi ghi

- `results/T-024/` (tạm ở `results/T-024/work/`).
- `src/p3/`: chỉ sửa lỗi runner hoặc evaluator thấy khi chạy. Mỗi lần sửa: ghi LOG, chạy lại test T-030 (đầu ra ở `results/T-024/test-chay-lai/`), giữ lượt hỏng. Sửa làm đổi hash `src/p3` thì bản ghi T-031 không còn dùng lại được: dừng, báo Minh trước khi chạy lại.
- Test T-030 tự ghi và xóa cache trong `results/T-030/work/`; được ghi trong thư mục đó.
- `tasks/T-024-cham-che-do-a/LOG.md`; dòng T-024 trong `docs/STATE.md`.

Không sửa SPEC này, `results/T-022/`, `results/T-030/` (trừ `work/`), `results/T-031/`, `docs/`, code phương pháp, môi trường chung, `data/`. Chạy Python không ghi bytecode (`-B`, `PYTHONDONTWRITEBYTECODE=1`).

## Các bước

Giới hạn mỗi lượt (một ca × một phương pháp × một seed), khai trước theo §8.3 (N3): **3.600 s**. Vượt thì ghi `TIMEOUT`, giữ lượt, chạy ca tiếp; ca `TIMEOUT` ở mẫu số, tính trượt. Mọi lượt tuần tự, không chạy cạnh việc nặng khác trên laptop.

0. **Rà SPEC và mở phiên.** Rà SPEC này độc lập (xem prompt trong LOG). Có điểm chặn thì dừng, báo Minh. Không thì: kiểm hash `src/p3` = `8d4cc8196c87…`, hash dữ liệu theo allowlist, môi trường, RAM trống; kiểm các bản ghi T-031 dùng lại có `src_p3_sha256` đúng hash này và trạng thái như LOG T-031 ghi. — kiểm: dòng mở phiên và mục "Rà SPEC" trong LOG.
1. **BARO, SimpleRCA, TraceRCA trên 30 ca** qua runner chế độ (a). Kiểm trên mọi lượt: BARO `key_check` khớp thứ tự chính thức; TraceRCA `ji` hữu hạn theo §6.4. — kiểm: `runs/*/tom-tat.json`, 30 bản ghi mỗi phương pháp.
2. **Chốt danh sách bản ghi**: ghi `ban-ghi-dua-vao-cham.json`, thêm một dòng LOG có giờ máy. Sau dòng này không chạy lại, không thêm, không bỏ bản ghi nào vì kết quả chấm.
3. **Evaluator** (`src/p3/danh_gia.py`) theo §8. Nhãn chỉ nối sau khi đầu ra đã ghi ra file. — kiểm: `cham-a.json` parse được; mọi ca không `OK` ở mẫu số.
4. **Viết `cham-a.md`.** Mỗi bảng ghi giới hạn chế độ (a) (WHY-24): biết đúng mốc tiêm. Báo số ca theo trạng thái cạnh mỗi bảng. Không kết luận về đồ thị, không xếp hạng "phương pháp tốt nhất" vượt quá khoảng bootstrap.

## Kiểm đúng đắn

- Test T-030 chạy lại đạt (57/57) trước bước 3.
- Tính tay ít nhất 3 ca dev khác nhau, trong đó 1 ca có hòa ở phương pháp khóa đơn và 1 ca TORAI dev; so với `cham-a.json`. Nếu các bản ghi TORAI đã chốt không có khối cùng điểm, kiểm riêng công thức V2-R2 bằng fixture hai khối cùng điểm AB/CD; ghi phép tính tay và đầu ra evaluator trong `cham-a.json.validation`, tách khỏi cohort và các bảng khoa học. Báo rõ cohort thật không có hòa khối TORAI.
- Khi không có hòa: AC@k của bảng RCAEval bằng Hit@k của bảng chính. Lệch thì tìm nguyên nhân trước khi báo.
- Mức ngẫu nhiên: kiểm tay 1 ca.
- Bootstrap: chạy lại cùng seed cho số giống hệt.
- Đối chiếu số công bố RCAEval cho RE2-TT nếu có trong `docs/knowledge/`; không kỳ vọng khớp (khác tập ca, cửa sổ, quy tắc hòa, ca lỗi ở mẫu số). Lệch lớn thì nêu các nguyên nhân khả dĩ, không chỉnh cấu hình.
- Kết quả quá đẹp (Hit@1 gần 1 ở một phương pháp) thì soi từng ca và chạy phép thử giả (ví dụ xáo nhãn root giữa các ca, chỉ trong evaluator) trước khi báo.
- Không kiểm được trong task: tính đại diện của 30 ca dev cho test; chế độ (b) (T-025).

## Tiêu chí xong

- `ban-ghi-dua-vao-cham.json`, `cham-a.json`, `cham-a.md` có thật; JSON parse được.
- LOG có dòng chốt danh sách bản ghi trước lượt evaluator đầu tiên.
- Đủ 6 phương pháp × 30 ca (TORAI × 3 seed); mọi trạng thái khác `OK` ở mẫu số.
- `cham-a.md` có đủ các mục ở "Đầu ra"; mỗi số có nguồn.
- Không mở `data/locked/`; không đổi khóa hay cấu hình sau khi thấy số.
- LOG đủ để agent khác, trên máy khác, làm tiếp; dòng STATE đã cập nhật; prompt phản biện viết sẵn cuối LOG.

## Không làm

Không chạy chế độ (b), N-Sigma, BOCPD (T-025). Không đổi khóa CIRCA/TORAI, ngưỡng 1e10, seed, cửa sổ. Không thêm biến thể phương pháp. Không mở test, RE3-OB; không chạy Nezha, Eadro, EC2. Không viết phân tích P4. Không sửa WHY, DECISIONS, giao thức. Không commit hay push khi Minh chưa duyệt.

## Chi phí ước lượng

**Chưa kiểm.** Từ pilot T-031 (`results/T-031/do-chi-phi.md` mục 4): BARO ≈ 7 phút, SimpleRCA ≈ 5 phút, TraceRCA ≈ 23 phút cho 30 ca trên laptop; evaluator và bootstrap vài phút. Công agent 2–4 giờ. Không lượt nào dự kiến dài hơn 1 giờ (luật cứng 8 không áp). RAM tới ≈ 1,8 GB (TraceRCA). Đĩa < 0,5 GB.

## Rủi ro và điều chưa chắc

- 11/30 ca CIRCA bị chi phối bởi lỗi làm tròn (Q-82, WHY-36); số CIRCA trên 30 ca phản ánh cả lỗi đó. Nhóm 19 ca không phải mẫu ngẫu nhiên.
- Bootstrap chỉ 10 ô; khoảng có thể hẹp hơn thực.
- MicroRank 4 ca ERROR (operation mới sau mốc) tính trượt: số MicroRank thấp hơn bản cài không lỗi.
- Có thể T-024 chạy cùng lúc T-025 (BOCPD trên EC2, N-Sigma trên laptop). Không chạy hai lượt nặng cùng laptop; phối hợp qua STATE.
