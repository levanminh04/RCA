# T-026 — Adapter và chấm tầng 1 chế độ (a) trên Nezha-OB dev

- **Trạng thái:** đã duyệt 07/10/2026 (lời Minh: "duyệt 1, 3", trả lời khung SPEC T-026 trình trong phiên T-025). Người làm rà lại SPEC trước khi triển khai (bước 0).
- **Người làm:** Codex.
- **Người phản biện:** Claude.
- **Thuộc gói MRP:** P3 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ1 và DT18-NV3 (thực nghiệm trên dữ liệu công khai), cùng nhận xét của cô về mở rộng dataset (Q-61 bậc 2). Trả lời:
1. Các phương pháp tầng 1 xếp root ra sao trên Nezha-OB dev khi biết trước cửa sổ (chế độ (a), Q-66).
2. Kết quả có giữ khi đổi hệ thống so với RE2-TT (T-024) không: báo theo ca, theo ô, theo loại lỗi, kèm số ca theo trạng thái.

Chỉ chế độ (a). Nezha không chạy chế độ (b): trace/log chỉ có file của phút tiêm và 2 phút sau, tức dữ liệu đã bị chọn theo nhãn khi thu (Q-61, Q-64; `results/T-021/goi-g1.md:28`; `results/T-008/the-dataset.md:72–80`). Không kết luận về đồ thị (P4).

## Đầu vào

- Danh sách ca: `results/T-021/chia-theo-o/A-phan-tang.csv`, dòng `dataset = Nezha-OB`, `vai_tro = dev` (22 ca). 34 ca `test` không được mở (luật cứng 1); chỉ dùng tên ca để selector từ chối.
- Dữ liệu: `data/ngoai-rcaeval/nezha/online-boutique/` (tải theo Q-47; `data/README.md` mục T-003). Chỉ đọc. Thẻ dữ liệu: `results/T-008/the-dataset.md`.
- Giao thức `results/T-022/giao-thuc-v2.md` (§3–6, §8–13); `docs/WHY.md` WHY-22–36, nhất là WHY-35 "Biên file ở chế độ (b)" (bài học xử lý biên cửa sổ).
- Quyết định: Q-59 (không phát hành lại dữ liệu; gỡ nếu tác giả phản đối), Q-61–Q-67, Q-80, Q-82.
- Mã `src/p3/` (commit `a97d7ab`); cấu hình đã khóa ở `results/T-031/khoa-cau-hinh.md`; cách chấm và script của T-024 (`results/T-024/scripts/`).

## Đầu ra

Trong `results/T-026/`:
- `allowlist-dev.json`, `nhan-dev.json` (như T-022 §3: mã mờ, đường dẫn, SHA-256; nhãn chỉ evaluator đọc).
- `kiem-dau-vao.md`: kết quả bước 0 (từng điều kiện: đạt / không đạt / OPEN, kèm bằng chứng).
- `runs/<run-id>/`: mọi lượt, kể cả lượt hỏng; bản ghi §13; tiến độ, thời gian, RSS.
- `ban-ghi-dua-vao-cham.json`: danh sách bản ghi đưa vào evaluator, ghi trước lượt evaluator đầu tiên.
- `cham-a.json`, `cham-a.md`: độ đo §8 theo phương pháp, theo ca, ô, loại lỗi; số ca theo trạng thái; so với T-024 (cùng phương pháp, khác dataset).
- `chi-phi.md`; `scripts/`.

## Phạm vi ghi

- `results/T-026/` (tạm ở `results/T-026/work/`).
- `src/p3/`: chỉ thêm adapter hoặc bộ đọc cho Nezha, và sửa lỗi thấy khi chạy. Mỗi lần sửa: ghi LOG, chạy lại test T-030 (đầu ra ở `results/T-026/test-chay-lai/`); hash `src/p3` đổi thì ghi hash mới.
- Test T-030 ghi/xóa cache trong `results/T-030/work/`.
- `tasks/T-026-nezha-ob-che-do-a/LOG.md`; dòng T-026 trong `docs/STATE.md`.

Không sửa SPEC này, `results/T-0xx` của task khác, `docs/`, code phương pháp, `data/`. Python không ghi bytecode. **Không đưa vào git dữ liệu dẫn xuất từ Nezha** (bảng CSV đầu vào phương pháp, span, log): ghi manifest (đường dẫn, số dòng, SHA-256) rồi xóa, như T-031 (Q-59).

## Các bước

0. **Rà SPEC và kiểm đầu vào, chỉ đọc, chưa chạy phương pháp.** Có điểm chặn thì dừng, báo Minh. Kiểm và ghi vào `kiem-dau-vao.md`:
   1. Lập allowlist 22 ca dev; kiểm SHA-256; selector từ chối 34 ca test (test như §11.1).
   2. Mốc tiêm và đồng hồ: nguồn mốc, đơn vị, lệch giữa metric, trace, log (thẻ T-008).
   3. **Đoạn nền N:** metric có đủ [t−300, t) không chồng lần tiêm trước (Q-64)? Trace và log có dữ liệu trước mốc không? Không có thì phương pháp cần trace hay log bình thường (MicroRank, TraceRCA, đồ thị CIRCA dựng từ trace N, TORAI B) có thể không chạy đúng nghĩa.
   4. Ánh xạ thực thể (§8.2) và universe U cho Online Boutique; luật tên cột trace của TORAI B (đang viết cho Train Ticket, §6.6).
   5. **Khai trước cách xử lý khi cửa sổ thiếu dữ liệu, cho từng phương pháp và từng nguồn**: cắt và ghi độ dài thực (§5.5), không điền 0 mà không khai báo (WHY-35, bài học T-025).
   6. Phương pháp nào không nhận được dữ liệu Nezha thì ghi `UNSUPPORTED` kèm lý do; không sửa phương pháp để nó chạy được.
1. **Adapter Nezha → khung bảng của `src/p3`.** Kiểm bằng test có fixture biết đáp án (cắt cửa sổ, ánh xạ thực thể, thiếu dữ liệu); test T-030 vẫn đạt 57/57.
2. **Pilot không nhãn trên 3 ca** chọn theo §12 (nhỏ nhất, trung vị dưới, lớn nhất theo yếu tố chi phí): chạy mọi phương pháp, đo thời gian, chạy chẩn đoán không nhãn (đầu ra rỗng, trùng thứ tự cột, tỉ lệ dự phòng TORAI, điểm không hữu hạn). Chiếu chi phí 22 ca; lượt nào chiếu vượt 1 giờ thì báo Minh trước.
3. **Chạy 22 ca × phương pháp** với cấu hình đã khóa (CIRCA OLS, TORAI B seed 0, 1, 2; MicroRank, CIRCA hashseed như T-024). TIMEOUT mỗi lượt 3.600 s, khai trước.
4. **Chốt danh sách bản ghi**, thêm dòng LOG có giờ máy. Sau dòng này không chạy lại, thêm hay bỏ bản ghi vì kết quả chấm.
5. **Evaluator** như T-024 (§8: hòa, bốn tập, mức ngẫu nhiên, bootstrap theo ô, bảng RCAEval riêng); nhãn chỉ nối sau khi đầu ra đã ghi ra file.
6. **Viết `cham-a.md`, `chi-phi.md`.** So với T-024 theo phương pháp; nêu khác biệt hệ thống (OB so với TT), loại lỗi (có lỗi mã nguồn), số ca; không gộp hai dataset thành một số.

## Kiểm đúng đắn

- Test T-030 đạt trên hash `src/p3` cuối cùng.
- Selector từ chối ca test; không có đường dẫn ca test nào trong job hay bản ghi (đếm trên mọi `job.json`).
- Trước khi chốt: chạy khô evaluator với nhãn giả (như T-025), sửa script nếu cần trước khi thấy số thật.
- Tính lại độc lập (mã riêng, không dùng `src/p3/danh_gia.py`) độ đo theo ca cho mọi phương pháp; khớp từng ca.
- Đổi locator mà giữ nội dung thì đầu ra giống hệt (§11.2) trên 1 ca pilot.
- Soi giá trị trung gian (QT5): điểm > 1e6, toàn hòa, nhánh dự phòng, cột trống; kết quả quá đẹp thì soi từng ca.
- Đối chiếu số công bố của bài Nezha nếu có cùng phương pháp và cùng cách chấm; không có thì ghi "không có số công bố để so".
- Không kiểm được trong task: tính đại diện cho phần test; tác động của việc tác giả chưa trả lời về giấy phép (Q-59).

## Tiêu chí xong

- `kiem-dau-vao.md`, `allowlist-dev.json`, `ban-ghi-dua-vao-cham.json`, `cham-a.json` có thật, parse được; `cham-a.md`, `chi-phi.md` có thật, mỗi số có nguồn.
- 22 ca × mỗi phương pháp có trạng thái; `UNSUPPORTED` có lý do.
- LOG có dòng chốt danh sách trước lượt evaluator đầu tiên.
- Không mở ca test, không mở `data/locked/`; không đưa dữ liệu dẫn xuất Nezha vào `results/` ngoài manifest.
- LOG đủ để agent khác làm tiếp; dòng STATE đã cập nhật; prompt phản biện viết sẵn cuối LOG theo `docs/review-prompt.md`.

## Không làm

Không chạy chế độ (b) trên Nezha. Không chạy Nezha-TT, Eadro, RE3-OB. Không chọn cấu hình, seed, ngưỡng, ca hay cột sau khi thấy số. Không sửa code phương pháp để chạy được trên Nezha. Không sửa WHY, DECISIONS, giao thức (cần thì đề xuất). Không commit hay push khi Minh chưa duyệt.

## Chi phí ước lượng

**Chưa kiểm.** PLAN-P3-G2: 0,5–3 giờ máy, 0,5–3 GB RAM, đĩa 0,5–2 GB; công agent 3–5 giờ, có thể 2 phiên (phiên bước 0–2, phiên bước 3–6). Chạy trên laptop; một lượt nặng tại một thời điểm. Pilot (bước 2) cho số chiếu; lượt nào dài hơn 1 giờ thì báo Minh trước (luật cứng 8).

## Rủi ro và điều chưa chắc

- Trace/log Nezha có thể không có đoạn nền trước mốc → nhiều phương pháp trace/log `UNSUPPORTED` hoặc chạy trên N ngắn. Bước 0 quyết, không đoán.
- Đồng hồ giữa các nguồn chưa kiểm (thẻ T-008: hai giả thuyết đồng hồ đổi nhóm vị trí ở 24/101 sự kiện, `results/T-021/runs/vi-tri-001/tom-tat.json`).
- Lỗi mã nguồn chỉ 8 ô / 14 ca trong phần chia; kết luận theo loại lỗi này yếu (`results/T-021/goi-g1.md`).
- 22 ca dev là ít; bootstrap theo ô có khoảng rộng.
- Tác giả phản đối thì gỡ Nezha khỏi kết quả (Q-59).
