# T-030 — Cài giao thức P3 trên RE2-TT dev: mã chung, fixture, D1, K-B1

- **Trạng thái:** đã duyệt 06/10/2026. Minh: "duyệt, tạo spec cho 31 luôn", trả lời phản biện SPEC trong chat (E1–E7 và các phương án đề xuất ở câu 2–5; LOG mục "Phiên 1"). Tách theo phương án 1, chuyển K-B1 vào task này. Phần chạy trên 30 ca chuyển sang T-031 (`tasks/T-031-chay-khoa-pilot/SPEC.md`).
- **Người làm:** Claude (Minh duyệt 06/10/2026).
- **Người phản biện:** Codex (Minh duyệt 06/10/2026).
- **Nguồn:** Q-74 Q1 tách bước 3–5 cũ của SPEC T-022; bản đề xuất đầu của SPEC này có cả phần chạy, nay là T-031.
- **Thuộc gói MRP:** P3 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ1, RQ2 và DT18-NV3 qua P3. Task biến giao thức đã duyệt (WHY-22–35; `results/T-022/giao-thuc-v2.md`) thành mã chạy được và đã kiểm trên fixture, để T-031 chạy các phép kiểm khóa cấu hình và pilot, rồi T-024, T-025 chạy đủ 30 ca dev. Task trả lời, **trước khi có số accuracy P3**:

1. Mã chung có làm đúng giao thức không: cắt cửa sổ, tách nhãn, trạng thái, hòa, độ đo?
2. K-B1: bộ dựng `tracets` nguồn B, theo quy ước tác giả, có khớp file tác giả theo đúng tên cột ở 30 ca dev không (§6.6)?

## Đầu vào

- AGENTS.md; `docs/STATE.md`; `docs/WHY.md` WHY-17, WHY-19, WHY-20, WHY-22–35; DECISIONS Q-40, Q-62, Q-64–Q-67, Q-72, Q-74, Q-76; `docs/LESSONS.md` (SL24, SL25, SL27, SL30, SL32, SL33, SL36).
- Giao thức (bản hiệu lực; mọi "§x" dưới đây trỏ vào file này): `results/T-022/giao-thuc-v2.md`; `results/T-022/cau-hinh/p3-re2tt-v2.json`; `results/T-022/quy-tac-cot-v2.json`.
- Dữ liệu và nhãn: `results/T-022/allowlist-dev.json` (30 ca, SHA-256 từng file); `results/T-022/nhan-dev.json` (runner chế độ (a) chỉ đọc mốc tiêm; evaluator đọc phần còn lại); `results/T-022/mappings/universe-re2tt-dev.json`; `results/T-022/cot-bocpd-dev.csv`. Telemetry: chỉ 30 ca trong allowlist, dưới `data/rcaeval/`. Dữ liệu tác giả TORAI: `D:/RCA-ext/work/T-016/data/torai-TT/` (30 ca dev).
- Code phương pháp, chỉ import, không sửa: `src/{microrank,simplerca,torai,circa_kien_truc}`; RCAEval `259ea41` (`D:/RCA-ext/src/RCAEval`); BARO `e35f4ec` (`D:/RCA-ext/src/baro`); CIRCA `0215e18` (`D:/RCA-ext/work/T-014/CIRCA`).
- Script và số đối chiếu đã có (đọc, gọi; không sửa): `results/T-015/scripts/check_tracerca.py`; `results/T-016/scripts/{dung_logts.py,tinh_lai_s9.py}`; `results/T-014/runs/regression-route-summary.json`; đầu ra từng ca đã lưu của T-016 (`results/T-016/runs/`) và T-017 (`results/T-017/runs/run-dev-005/`). Người làm xác định file cụ thể ở bước 0.
- Môi trường, chỉ dùng, không sửa hay cài: `D:/RCA-ext/envs/T-014-main` (Python 3.12); `py38-rcdlock` (TORAI, tiến trình riêng); `T-016-cong-cu` (drain3, dựng `logts` nguồn B). PYTHONPATH và cờ chạy như giao thức §6.

## Đầu ra

Trong `src/p3/`:
- Selector: allowlist, kiểm hash, từ chối `data/locked/`, path traversal, mã sai dạng (§3, §11.1).
- Đọc và cắt cửa sổ: metric, span, log theo §5.2–5.3; chế độ (a) quanh t; chế độ (b) quanh t̂, cắt ở biên file.
- Adapter cho tám thành phần: BARO, SimpleRCA, MicroRank, TraceRCA, CIRCA, TORAI (nguồn A và B), N-Sigma, BOCPD. Mỗi adapter trả bản ghi §13, khóa xếp hạng §8.4, trạng thái §8.3. Bộ dựng nguồn B gồm `tracets_err`, `tracets_lat`, `logts`.
- Evaluator: bốn tập (§8.1); trạng thái; hòa, gồm hòa khối TORAI (§8.4); MRR, NDCG@5, Hit@1/3/5, Avg@5, Retrieval@5/10, Rerank@1; mức ngẫu nhiên (§8.7); bootstrap theo cặp ô (§8.8); bảng RCAEval riêng (§8.6); chấm phát hiện và thành công chung (§7.4–7.5); audit số cột và cột vắng so với hợp 30 ca (§10).
- Runner: tách nhãn (§4); ghi bản ghi §13; đo chi phí (thời gian, peak RSS, byte đọc/ghi, mã thoát); timeout mỗi lượt (giá trị khai trong SPEC của task chạy).

Trong `results/T-030/`:
- `tests/`: fixture và kết quả từng phép kiểm §11.1–11.8 và phần fixture của §11.10.
- `d1-o-khac.json`: số ô khác nhau giữa "cắt trước, tiền xử lý sau" và thứ tự `main.py`, ở 30 ca (§5.3).
- `k-b1.json`: K-B1 từng lần thử dựng (tối đa 3), tỉ lệ ô trùng theo tên cột cho từng chuỗi, gộp 30 ca; kết luận đạt, không đạt hoặc OPEN (§6.6). Báo theo mã mờ, không kèm root, loại lỗi hay tên ca.
- `phat-lai.json`: phát lại đầu ra đã lưu của T-016, T-017 qua evaluator mới, so với số đã báo.
- `runs/<run-id>/`: cấu hình, stdout/stderr, tiến độ, thời gian; giữ cả lượt hỏng. Không chép telemetry.

## Phạm vi ghi

- `src/p3/`
- `results/T-030/` (tạm và cache ở `results/T-030/work/`)
- `tasks/T-030-cai-dat-p3/LOG.md`
- dòng T-030 trong `docs/STATE.md`

Không sửa SPEC này, `results/T-022/` (giao thức), `docs/WHY.md`, `docs/DECISIONS.md`, code phương pháp cũ, môi trường chung, `data/`. Chạy Python không ghi bytecode. Thấy giao thức không đủ rõ để cài, hoặc cần làm khác giao thức: dừng, đề xuất (Luật 0 điểm 5); không tự chọn.

## Các bước và phụ thuộc

Đọc dữ liệu thật chỉ ở bước 1 (D1, chỉ dùng mốc tiêm) và bước 5 (K-B1). Không chạy phương pháp trên ca thật; adapter kiểm trên fixture tổng hợp.

0. **Mở phiên.** Kiểm đầu vào; revision và `git status` sạch của RCAEval, BARO, CIRCA và `src/`; môi trường import được; RAM trống. Xác định file đầu ra cũ để phát lại ở bước 2. — kiểm: dòng mở phiên trong LOG.
1. **Selector, đọc, cắt cửa sổ** (§3, §5). Đếm D1 ở 30 ca; chỉ dùng mốc tiêm, không đọc nhãn khác. — kiểm: §11.1–11.3; `d1-o-khac.json`.
2. **Evaluator** (§7.4–7.5, §8, §10 audit). — kiểm: §11.4–11.5; đối chiếu `Evaluator` RCAEval trên danh sách không hòa; phát lại đầu ra đã lưu của T-016 (TORAI) và T-017 (SimpleRCA), so với số đã báo trong hai task đó.
3. **Runner và bản ghi** (§3, §4, §13). — kiểm: §11.2, §11.8.
4. **Adapter tám thành phần** (§6, §7): BARO tính lại khóa; SimpleRCA lọc span trước `prepare`; MicroRank; TraceRCA đọc `ji_dict`; CIRCA với `current`, route hồi quy, SVR qua `RHTScorer`; TORAI nguồn A, B (ghi lệch lưới từng ca của A) và khóa hai cấp; N-Sigma theo D9; BOCPD với `m[i]` và kiểm posterior. — kiểm: fixture §11.6–11.7 và §11.10 trên dữ liệu tổng hợp.
5. **K-B1** (§6.6): dựng `tracets_err`, `tracets_lat` theo quy ước tác giả (lưới của file tác giả, ngưỡng toàn file) và luật tên cột TT cho 30 ca; so với file tác giả theo đúng tên cột (cột, bin); cột không ghép được tính sai; đạt khi ≥ 95 % ô trùng cho từng chuỗi, gộp 30 ca. Tối đa 3 cách dựng, giữ mọi lần thử, chỉ so với file tác giả, không chạy TORAI, không dùng nhãn. Luật tên cột sai ở ca khác mà 3 lần thử không sửa được: K-B1 để OPEN, trình Minh. — kiểm: `k-b1.json`.

Phụ thuộc: 1 và 2 song song. 3 sau 1. Adapter (4) của mỗi thành phần cần 1 và 3, không cần 2. 5 chỉ cần selector (bước 1) và bộ dựng `tracets` nguồn B; không cần runner, cắt cửa sổ hay adapter TORAI.

## Kiểm đúng đắn

- Các nhóm kiểm §11.1–11.8 và phần fixture của §11.10 của giao thức. Đáp án của fixture tính độc lập với mã được kiểm (tính tay hoặc phân số chính xác).
- Không có số công bố cho bản cài P3, vì cửa sổ và các sửa đầu vào khác bài. Đối chiếu được: `Evaluator` RCAEval trên danh sách không hòa; số đã có của T-016, T-017 khi phát lại đầu ra cũ; file tác giả torai-TT (K-B1).
- Rò nhãn: tìm trong mã adapter và phương pháp không có chỗ đọc `nhan-dev.json` ngoài runner chế độ (a); fixture §11.8 đổi nhãn hoặc mốc tiêm phía evaluator không đổi đầu ra chế độ (b).
- Không kiểm được trong task: mọi phép kiểm trên ca thật của §11.6, §11.9–11.11 (trừ K-B1) và chi phí (T-031); accuracy P3 (T-024).

## Tiêu chí xong

- `src/p3/` có đủ các phần ở mục Đầu ra. Mọi kiểm thuộc task đã chạy, kết quả ở `results/T-030/tests/`. Kiểm trượt được ghi kèm nguyên nhân và cách xử lý hoặc đã trình Minh; không bỏ qua.
- `d1-o-khac.json`, `k-b1.json`, `phat-lai.json` có thật và parse được. K-B1 có kết luận đạt hoặc không đạt; nếu OPEN thì kèm lời Minh.
- Không có số accuracy P3 trên đầu ra mới; không mở `data/locked/`.
- LOG đủ để agent khác, trên máy khác, làm tiếp; dòng STATE đã cập nhật.

## Không làm

Không chạy phương pháp trên ca thật (T-031). Không chạy evaluator có nhãn trên đầu ra mới. Không benchmark, không chạy EC2. Không sửa giao thức, WHY, code phương pháp cũ hay môi trường chung; không cài thư viện. Không chạy Nezha, Eadro; không mở test hay RE3-OB. Không tự tạo SPEC T-024, T-025. Không commit hay push khi Minh chưa duyệt.

## Chi phí ước lượng

**Chưa kiểm.** Giả định dùng lại môi trường và lõi đã có, laptop.

- Công agent: khoảng 5–8 giờ; không gồm thời gian chờ Minh.
- Thời gian máy: D1 đọc metric 30 ca; K-B1 đọc trace 30 ca và file tác giả, tối đa 3 lần; phát lại đầu ra cũ. Mỗi việc dự kiến vài phút, chưa đo. Không có lượt nào dự kiến trên 1 giờ; nếu chiếu trên 1 giờ thì dừng, báo (luật cứng 8).
- RAM: đọc trace một ca một lúc. Kiểm RAM trống trước lượt đọc trace.
- Đĩa: tăng dưới 0,1 GB; không chép telemetry.

## Rủi ro và điều chưa chắc

- K-B1 có thể trượt vì luật tên cột trace TT mới kiểm ở 1/30 ca. Khi đó TORAI A làm chính (T-031), kèm lệch lưới và ngưỡng toàn file. Chưa kiểm.
- Fixture tổng hợp không bắt được lệch schema thật; T-031 là lần đầu adapter chạy trên ca thật.
- Đầu ra đã lưu của T-016 có thể không đủ để phát lại khóa hai cấp TORAI; khi đó chỉ phát lại bảng RCAEval (§8.6).
