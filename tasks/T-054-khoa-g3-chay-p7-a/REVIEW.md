# Phản biện T-054 — chạy main013-v2, nhận/kiểm/chấm, báo cáo P7(a) và luồng A

- **Người phản biện:** Claude (phiên mới, thay Codex theo quyết định của Minh trong chat ngày 08/11/2026; chưa ghi DECISIONS) — **Ngày:** 08/11/2026 — **Commit/diff đã đọc:** commit gốc `601be1a1`, branch `claude/sweet-hawking-dy078d`; cây làm việc chưa commit (`docs/STATE.md`, `tasks/T-054-khoa-g3-chay-p7-a/LOG.md` sửa; `results/T-054/reports/p7a-013-v2/` chưa theo dõi).
- **Công đoạn/cổng và bản lượt:** soát kết quả; P7(a), chuẩn bị G4. Minh cho ghi đúng file này. Giữ vai trò và các bản cũ.
- **Đã đọc:** `AGENTS.md`; `docs/STATE.md`; SPEC; LOG từ "Tiếp nhận từ Codex sau duyệt main013" tới hết; LOG T-055 mục luồng A và quyết định D-55-*; `results/T-055/grants/minh-re3.txt`; `results/T-054/reports/p7a-013-v2/{bao-cao.md, phan_tich.py, phan-tich-nhom.json, manifest.json, manifest-002.json}`; `kiem-toan-ven/{kiem.py, ket-qua.json, ghi-chu.md}`; `results/T-054/reports/main-013-v2/{a4.json, tables.json, exposure.jsonl}`; `runs/chuan-bi-main-013-v2/{activated-001/protocol.json, received-main-002/verified-before-labels.json, execution-receipts/{v1-v2-compare.json, cmp_v1_v2.py}}`; `src/m1/{e4.py, chuoi.py, doi_chung.py, xep_hang.py}`; DECISIONS (Q-247, D1 dòng 460, mục v2 dòng 487); WHY-06; LESSONS (ST3, QT4, QT6, QT15, SL38); DT18 §2; `docs/review-prompt.md`.
- **Tự soát độc lập:** chưa có lượt phản biện nào cho phần này. Mọi số dưới đây tôi tự đọc từ file hoặc tự tính lại. Không tin tóm tắt LOG.

## Kết luận chung

Không thấy số giả hay số được làm đẹp. Mọi số trong báo cáo mà tôi kiểm đều khớp file nguồn: §3–§8, gồm toàn bộ bảng §4 và §5 và các số theo ca ở §7. A4 đọc đúng theo bảng diễn giải đã khóa. Có 5 điểm KHÔNG CHẶN. Không điểm nào đổi kết quả A4. R2 và R3 thu hẹp phạm vi kết luận cơ chế và RQ3d. R1 và R5 là lỗi quy trình/bàn giao. Task chưa đủ điều kiện đề nghị nghiệm thu khi bảng TORAI A còn chờ Minh quyết.

## Các điểm

### R1. `bao-cao.md` bị ghi đè trong luồng A; bản gốc mất, bằng chứng sửa không đủ — KHÔNG CHẶN

- **Ở đâu:** `results/T-054/reports/p7a-013-v2/bao-cao.md`; `kiem-toan-ven/ghi-chu.md`; `manifest-002.json`; LOG T-055 mục "Luồng A (T-054) trong lúc chờ".
- **Sai gì:**
  - Quyền Q1 trong `results/T-055/grants/minh-re3.txt` chỉ cho "ghi results/T-054/reports/p7a-013-v2/kiem-toan-ven/".
  - SPEC mục Đầu ra ghi `reports/<report-id>/` là "giữ bản đầu, không ghi đè".
  - `bao-cao.md` bị sửa tại chỗ lúc 06:02:35 (+07), sau `manifest.json` (04:59). Hash cũ 6af085…, hash mới 88daa2…. Không tìm thấy bản 6af085 trong `results/T-054` hay `results/T-055`.
- **Bằng chứng:**
  - `ghi-chu.md` nói có 4 lỗi làm tròn, trỏ tới `ket-qua.json#/A5_fail`. Mục đó chỉ có 1 lỗi ("OB C-d2 MRR 0,878"). Tôi chạy lại bản chép của `kiem.py` trong scratchpad, sửa ROOT/OUT: kết quả trùng hệt `ket-qua.json`.
  - Câu "soát máy §4 (146 số) và §5 (75 số) sau sửa: hết lệch" không có file kết quả hay lệnh kèm theo.
  - 30 mục "bảng §4 …" trong `A5_so_bao_cao` so MRR chấm độc lập với PT (`kiem.py` dòng 242–246). Chúng không so với văn bản báo cáo.
  - Việc sửa chỉ ghi ở LOG T-055. LOG T-054 không có.
- **Phần có thể bác bỏ finding:**
  - Sửa trước lúc ghép nhãn RE3 (`results/T-054/reports/re3-ban-cuoi-001/exposure.jsonl`, 01:34:03 UTC = 08:34 +07), nên không nhiễm kết quả RE3.
  - Minh giao quyền quyết rộng trong `minh-re3.txt`. Nhưng quyền đó không nhắc tới việc sửa báo cáo T-054.
  - Số trong bản hiện hành đều khớp file (mục "Điều đã kiểm").
- **Bước và quyết định chịu ảnh hưởng:** lỗi đã xảy ra. Không kiểm được rằng bản gốc chỉ khác đúng 4 số. Đây là việc ghi ngoài phạm vi, phải khai theo Luật 0 mục 8. Không chặn A4.
- **Đề xuất sửa:**
  - Nối LOG T-054 một mục luồng A: khai ghi đè ngoài phạm vi, hash bản cũ 6af085…, 4 số đã đổi, bản cũ không khôi phục được.
  - Đính chính `ghi-chu.md`: `A5_fail` chỉ có 1 lỗi; 3 lỗi còn lại đến từ một phép soát không lưu file.
  - Lần sau ghi bản mới thay vì ghi đè. Không cần chạy thêm.

### R2. Kết luận RQ3d OB về E1 chưa mang giới hạn D1 — KHÔNG CHẶN

- **Ở đâu:** báo cáo §0 (RQ3d OB), §7.4 đoạn "E1 ở lỗi CPU", §7.5 ví dụ `test-3218391218`, §9 hàng "RQ3d — bỏ quan hệ".
- **Sai gì:** DECISIONS dòng 460 (D1) yêu cầu: "Khi báo OB phải nêu giới hạn tính độc lập của việc sửa adapter đó." Báo cáo chỉ áp D1 cho Hit@5 của A4 (affected4 Δ = 0). Phần RQ3d và phân tích cơ chế không mang cờ này.
- **Bằng chứng:**
  - Bốn ca bị ảnh hưởng (`results/T-054/runs/chuan-bi-main-013/OB-group-decision.json#/affected_opaque_ids`): `test-3218391218`, `test-3a1afd6d4f`, `test-9712e01207`, `test-a8cc0373da`.
  - `3a1afd6d4f` là ca minh họa E1 ở §7.4. `3218391218` là ca minh họa ở §7.5.
  - 3/8 ca mà E1 giúp (`PT#/so_cap/Nezha-OB|M1-bo-E1|RR/cases`) nằm trong 4 ca này.
  - Tôi tính lại RR trên world P từ `tables.json#/rows`:

    | Cặp so | all34 | remaining30 | affected4 |
    |---|---|---|---|
    | M1 − bỏ E1 | +0,130 (8/25/1) | +0,079 (5/24/1) | +0,512 (3/1/0) |
    | M1 − bỏ E2 | +0,115 (7/25/2) | +0,131 (7/21/2) | 0 |
    | M1 − C-a0 | +0,164 (11/20/3) | +0,203 (11/17/2) | −0,125 |
    | C-a1 − C-a0 | +0,049 | +0,072 | −0,125 |

- **Phần có thể bác bỏ finding:**
  - Theo tên audit, D1 sửa cửa sổ thời gian metric (`OB-metric-time-window-check.json`). E1 là kênh self-time của trace, nên có thể ít chịu ảnh hưởng.
  - Nhưng xếp hạng so kênh trace của root với kênh metric của đối thủ. Sửa adapter vẫn có thể đổi hạng. Dữ liệu hiện có chưa phân xử được.
- **Bước và quyết định chịu ảnh hưởng:** mâu thuẫn với một quyết định đã có. Kết luận "phần hơn trên OB đến từ E2 và E1" vững với E2 và với tổng M1 − C-a0. Phần của E1 yếu hơn mức báo cáo viết. Ảnh hưởng câu RQ3d ở G4.
- **Đề xuất sửa:** thêm D1 và các số remaining30 ở trên vào §9 (hàng RQ3d OB) và §7.4 (đoạn E1), bằng đính chính riêng.

### R3. Ứng viên 1 ở §7.5 kiểm được rẻ trên TT nhưng chưa kiểm; dữ liệu đã có không hỗ trợ nó — KHÔNG CHẶN

- **Ở đâu:** báo cáo §7.5 "Ứng viên (chưa kiểm)" mục 1; §11 "Nguồn kênh hẹp cực trị … cần đọc C-e TT".
- **Sai gì:** vế C-e TT đã chạy và nằm trong grant v2. Đọc nó không tốn chạy mới. AGENTS §5 bước 4 (Q-41) đòi kiểm trong task mọi thứ kiểm được với chi phí hợp lý. Báo cáo để phép kiểm này sang sau.
- **Bằng chứng:**
  - Tôi đọc `result.json` của slot M1 view `ce` cho hai ca TT sai mà đối thủ là ts-auth-service. Nguồn: `runs/chuan-bi-main-013-v2/received-main-002/ec2_*/results/T-054/runs/main-013-v2/queue/*/attempt-*/`.
  - Đơn vị xét: `op|ts-auth-service|UserRepository.findByUsername`. Ở cửa sổ t−300 nó không có cờ:

    | Ca | Cửa sổ t−300 (C-e) | Cửa sổ lỗi (main) |
    |---|---|---|
    | `test-053c028c65` | F_raw_len 0, e_len 0; r_len_A 0,020, r_len_N 0,044 | e_len 2263,2; r_len_A 0,104, r_len_N 0,028 |
    | `test-5e8f996191` | F_raw_len 0, e_len 0; r_len_A 0,032, r_len_N 0,035 | e_len 1438,7; r_len_A 0,098, r_len_N 0,037 |

- **Phần có thể bác bỏ finding:**
  - N của C-e khác N của cửa sổ chính.
  - Một bất thường nền gián đoạn vẫn có thể không hiện ở t−300.
  - Vì vậy kết quả là "không hỗ trợ", không phải "bác bỏ".
  - OB không có vế C-e, nên phần OB (adservice, productcatalogservice) vẫn OPEN.
- **Bước và quyết định chịu ảnh hưởng:** nguy cơ chưa kiểm, nay đã có một phần bằng chứng.
  - Trên TT 2/2 ca, kênh chỉ lệch trong cửa sổ lỗi. Đây đúng là trường hợp "Sai khi" mà báo cáo tự nêu.
  - Còn hai giải thích chưa phân xử: lỗi lan qua đường không quan sát được (auth không có cạnh, LESSONS ST3), hoặc tranh chấp tài nguyên chung.
  - Mọi đề xuất thiết kế dựa trên ý "bất thường nền" chưa có căn cứ trên TT. Ví dụ đề xuất cho FlashTicket trong báo cáo RE3 §6 nếu có dùng ý này.
- **Đề xuất sửa:** ghi kết quả trên vào đính chính báo cáo. Đổi trạng thái ứng viên 1 với TT thành "không hỗ trợ ở 2/2 ca, cửa sổ t−300". Giữ OB OPEN.

### R4. "TORAI B yếu hơn ở nhóm bậc 0" chủ yếu đến từ một ô — KHÔNG CHẶN

- **Ở đâu:** báo cáo §6 "TT theo vị trí N", §7.1 "Suy luận".
- **Sai gì:** LESSONS QT15: một ô không phải mẫu hình. Ở nhóm này, vị trí N và service gốc bị trộn lẫn.
- **Bằng chứng (`tables.json#/position_N`, `#/rows` world P):**
  - Nhóm bậc 0 có 13 ca: 12 ca root là ts-auth-service (bốn ô disk, loss, mem, socket) và 1 ca `test-541642b59e` (train socket).
  - M1 thắng TORAI B 5 ca: `60f9be319f`, `d62934a19f`, `d819fba4a5` cùng ô auth|loss; `d4eb10a4ba` (auth socket); `541642b59e`.
  - Ca `541642b59e` có 136 operation mới và 12 operation chỉ có 1 span bình thường (LOG "Quyết định v2").
- **Bước và quyết định chịu ảnh hưởng:** kết luận mạnh hơn bằng chứng ở phần mô tả. Không ảnh hưởng A4.
- **Đề xuất sửa:** ghi rõ "bậc 0 ≈ root auth (12/13); 3/5 ca thắng nằm trong một ô auth|loss".

### R5. Bàn giao và trạng thái chưa khớp hiện trạng — KHÔNG CHẶN

- **Ở đâu:** `docs/STATE.md` dòng T-054; LOG T-054; báo cáo §10, §11.
- **Sai gì và bằng chứng:**
  - **(a) STATE và báo cáo cũ.** Dòng T-054 ghi "Chờ Minh: giữ M1 cho RE3 hay kiểm dev trước (§10)" và "RE3 chưa có quyền". Thực tế LOG T-055 D-55-1 đã giữ M1 và RE3 đã chạy (dòng T-055 trong STATE). Báo cáo §10 và §11 cũng chưa ghi kết cục này.
  - **(b) LOG thiếu mục.** LOG T-054 không có mục luồng A (xem R1).
  - **(c) Số ca TORAI A sai trong LOG.** LOG dòng 2249 ghi "6/180 (2 ca × 3 seed)". Queue laptop cho thấy 3 ca: `cda8dfc162` 3 seed, `2a0c838e6b` 2 seed, `edaa68b4cf` 1 seed. Báo cáo §0, §2.5, §8 ghi đúng.
  - **(d) LOG nói quá.** LOG dòng 2303 ghi "đủ bảng bắt buộc". Nhưng `activated-001/protocol.json#/required_permissions` gồm "TORAI A author CSV grant for main TT cohort", SPEC Tiêu chí xong 1–2 tính mọi slot bắt buộc, và bảng A đang chờ Minh (tạm dừng). Báo cáo §0 và §11 khai đúng là thiếu.
  - **(e) C-d3 OB không được nhắc.** SPEC bảng khối lượng dự kiến "OB: C-d3 — 34 dòng hỗ trợ/mô tả". `tables.json` không có dòng C-d3 OB, chỉ có câu "OB không có solver mới" ở `#/limits`. Báo cáo không nhắc.
- **Bước và quyết định chịu ảnh hưởng:** Tiêu chí xong 5 (người khác nhận tiếp được). Đề nghị nghiệm thu còn phụ thuộc quyết định TORAI A.
- **Đề xuất sửa:**
  - Nối LOG T-054 các mục (a), (b), (c).
  - Sửa dòng T-054 trong STATE.
  - Ghi kết cục §10 và câu về C-d3 OB trong đính chính riêng, không ghi đè báo cáo.

## Đối chiếu các lượt trước

Chưa có lượt phản biện hay phản hồi nào cho phần chạy/chấm/báo cáo. Các lượt của công đoạn chuẩn bị013 (`claude-review-013-001.txt`, `grants/claude-review-013-002.txt`) không thuộc phạm vi lượt này. Tôi không đánh giá lại các lượt đó.

## Tuân thủ quy trình

- Phạm vi ghi phiên lập báo cáo (`reports/p7a-013-v2/`, LOG, dòng STATE) đúng lời Minh trong LOG. Luồng A ghi ngoài phạm vi ở một file (R1).
- v2 có nguồn quyết định (DECISIONS dòng 487). Luật 21 và SL38 đã được duyệt. Báo cáo khai v2 theo C-15 B.
- Có ghi sổ xem test (LOG "Ghi sổ xem test"). Không thấy thiết kế bị đổi sau khi xem test.
- **Tính độc lập của lượt này.** AGENTS §1 đòi người phản biện khác người làm. Lượt này do Claude phản biện việc của Claude, theo lời Minh trong chat. Lời đó chưa ghi DECISIONS. Minh cần quyết: ghi ngoại lệ này, hay vẫn cần Codex phản biện chính thức.

## Điều đã kiểm và thấy đúng

- **Chạy lại:**
  - `py -3 -B results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents`: PASS, 515 mục, 0 lệch.
  - `phan_tich.py <scratchpad>/pt-review.json`: sha256 34e670f3…, trùng file trong repo. 716 `result.json` khớp `verified.json`. RR tính từ khối khớp 658/658.
  - `kiem.py` bản chép ở scratchpad: đầu ra trùng hệt `ket-qua.json`.
  - Hash của 6 file trong `manifest-002.json` khớp file hiện có.
- **Đối chiếu số:**
  - §3 khớp `a4.json`: Δ 317/7200; CI [−0,033333333333; 0,148750000000]; 7/50/3; 6/2/0; p 1906/10001; đảo dấu theo ô 1/4; McNemar; OB 3/34, 3/31/0, p 1/8, 1/20, CI [0; 0,1935]; D4 3/34, 1/10, 0.
  - Toàn bộ bảng §4 và §5 khớp PT.
  - §6 (tách theo fault và vị trí N), §8 (C-e 58/2, V0, N1 476/29, RR tương lai 0,130, mức ngẫu nhiên 0,071, 3/58; vùng; T12 +126/+155/+9 cạnh) khớp PT.
  - Các số theo ca ở §7.2–§7.5 khớp trung gian: s, độ rộng, số dòng giải thích, tầng, ca đúng/sai 43/57, 12/27, 30/57, 5/27.
  - Thực thể TORAI B đặt đầu ở ba ca auth loss khớp `result.json` torai_pipeline trên EC2.
- **Chấm lại độc lập phần `kiem.py` chưa phủ:** C-d1 và C-d2 tính từ `extra.doi_chung` của M1 khớp RR trong `tables.json` 188/188.
- **Snapshot và nhãn:**
  - `cham.fingerprint(verified-before-labels.json)` = 0fbf5b45…, bằng `exposure.jsonl` LABEL_JOIN.
  - 1466 VERIFIED, 174 BLOCKED, tổng 1640.
- **Giám sát:** chỉ attempt TORAI A `cda8dfc162` seed 1 (stage method) có khoảng hở 342,3 s. Mọi attempt khác trên ba máy dưới 1,5 s. Không có `clock_anomaly`.
- **Lỗi baseline:** 10 ERROR của TraceRCA/MicroRank TT đều có `method-failure.json`, kèm audit và quy tắc.
- **Rò nhãn:** quét 4206 file job/invocation/launch không thấy nhãn. `phan_tich.py` chỉ lấy root từ ô sau seal.
- **So v1↔v2:** `cmp_v1_v2.py` so đúng v1 với v2 theo job id, khớp 740 slot. Phạm vi so: các trường đã khai. Với M1, world P được phủ qua `extra.blocks_P`; `worlds` S_lo/S_hi và `region` không nằm trong các trường được so.
- **Trích dẫn code và nguồn:** `e4.py` (z = max(A − median)/IQR, c = 1 khi IQR ≈ 0); khóa E6a ở `xep_hang.py`; C-a0/C-a1 ở `chuoi.py`; C-d2 dùng kênh của M1 (`chuoi.py:621`). Khi đối chiếu WHY-06 (power 0,19), DT18 §2 và câu diễn giải khóa trong `protocol.json#/interpretation`, tôi thấy báo cáo dẫn đúng.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm gì:**
   - Đọc nguồn, đầu ra, code và các quyết định liên quan.
   - Chạy lại ba script.
   - Đối chiếu số trong báo cáo với file.
   - Tự chấm lại C-d1/C-d2.
   - Đọc trung gian test M1 và C-e trong grant v2.
   - Không chạy phương pháp, không mở RE3.
2. **File đã thay đổi:** chỉ tạo file này. File nháp nằm ngoài repo (scratchpad).
3. **Kiểm đã chạy và kết quả:** như mục trên. Đạt hết, trừ R1–R5.
4. **Bất đồng, câu hỏi mở và điều cần Minh quyết:**
   - R2 và R3 thu hẹp kết luận RQ3d OB (phần E1) và trạng thái ứng viên 1.
   - Nguồn kênh hẹp cực trị trên OB vẫn OPEN.
   - Cơ chế khiến kênh auth lệch trong cửa sổ lỗi chưa phân xử được.
   - Minh quyết: (i) phạm vi sửa R1–R5; (ii) ngoại lệ về tính độc lập của lượt này; (iii) TORAI A chạy bù hay chấp nhận giới hạn.

**Đề xuất:** tiếp tục một lượt để người làm đáp R1–R5, vì R2 và R3 còn ảnh hưởng phạm vi kết luận. Sau lượt đáp, nếu không còn bất đồng thì đề xuất dừng. Dừng không tự nghiệm thu task, đóng RQ3 hay mở thêm dữ liệu.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054, tasks/T-054-khoa-g3-chay-p7-a/ (SPEC.md, LOG.md) — phần chạy main013-v2, nhận/kiểm/chấm, báo cáo P7(a) và kiểm toàn vẹn số liệu (luồng A).
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P7(a), chuẩn bị G4.
- Người làm và người phản biện chính thức: theo SPEC, người làm phần chạy/chấm/báo cáo là Claude, người phản biện chính thức là Codex. Lượt phản biện tasks/T-054-khoa-g3-chay-p7-a/REVIEW.md do một phiên Claude khác thực hiện thay Codex theo quyết định của Minh trong chat ngày 08/11/2026 (chưa ghi DECISIONS).
- Tài liệu gốc: tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; tasks/T-054-khoa-g3-chay-p7-a/LOG.md (từ mục "Dựng và phát v2" tới hết); tasks/T-055-re3-ban-cuoi/LOG.md mục "Luồng A (T-054) trong lúc chờ"; results/T-054/reports/p7a-013-v2/{bao-cao.md, phan_tich.py, phan-tich-nhom.json, manifest.json, manifest-002.json}; results/T-054/reports/p7a-013-v2/kiem-toan-ven/{kiem.py, ket-qua.json, ghi-chu.md}; results/T-054/reports/main-013-v2/{a4.json, tables.json, exposure.jsonl}; commit gốc 601be1a1 trên branch claude/sweet-hawking-dy078d, thay đổi sau đó chưa commit (git status, git diff).
- Phản biện và phản hồi trước: tasks/T-054-khoa-g3-chay-p7-a/REVIEW.md (08/11/2026). Các lượt phản biện công đoạn chuẩn bị013: results/T-054/runs/chuan-bi-main-013/claude-review-013-001.txt, results/T-054/runs/chuan-bi-main-013/grants/claude-review-013-002.txt.
- Code và kết quả liên quan: results/T-054/scripts/; results/T-054/runs/chuan-bi-main-013-v2/ (manifest.json, verify_manifest.py, grants/, execution-receipts/, received-main-002/, activated-001/); queue laptop results/T-054/runs/main-013-v2/queue/; bản nhận EC2 results/T-054/runs/chuan-bi-main-013-v2/received-main-002/{ec2_1,ec2_2}/; code src/m1/. Lệnh: py -3 -B results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents; py -3 -B results/T-054/reports/p7a-013-v2/phan_tich.py <đường-dẫn-ra-ngoài-repo.json>; kiem.py ghi file cố định và từ chối ghi đè, nên chép script ra thư mục nháp và sửa ROOT/OUT trước khi chạy. Quyền đọc dữ liệu: kết quả và trung gian test main013-v2 đã chấm theo grant results/T-054/runs/chuan-bi-main-013-v2/grants/main-grant.json; không mở RE3 hay dữ liệu ngoài 60 RE2-TT và 34 Nezha-OB; không chạy phương pháp.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cho phép rõ ràng điền bảng "Phản hồi của người làm" cuối tasks/T-054-khoa-g3-chay-p7-a/REVIEW.md, nối LOG T-054 và cập nhật dòng T-054 trong docs/STATE.md.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hay prompt của người phản biện. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Để trống cột Minh quyết. Prompt của lượt đáp nằm trong mục LOG mới hoặc chat.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng một phần; KHÔNG CHẶN | Ghi đè ngoài phạm vi là đúng; tôi khai ở LOG và `dinh-chinh-001.md` Đ1. Phần "bản gốc mất, không kiểm được chỉ khác 4 số" thì sai: đảo đúng 4 chỗ sửa cho bản trùng từng byte với sha 6af085 trong `manifest.json`, lưu ở `bao-cao-ban-dau.md`. `soat_bang.py` → `soat-bang.json`: bản gốc lệch 4/221 ô, bản hiện hành lệch 0/221. `ghi-chu.md` đã nối đính chính về `A5_fail`. | |
| R2 | Đúng; KHÔNG CHẶN | Tính lại khớp mọi số reviewer nêu (all34/remaining30/affected4). Đã ghi giới hạn D1 cho phần E1 ở `dinh-chinh-001.md` Đ2. E2 và M1−C-a0 vững; phần E1 yếu hơn (+0,079 trên 30 ca). | |
| R3 | Đúng; KHÔNG CHẶN | Đọc lại C-e của `053c028c65` và `5e8f996191`: số khớp reviewer. Ứng viên 1 với TT đổi sang "không hỗ trợ 2/2 ca"; OB vẫn OPEN (Đ3). Tôi đã bỏ sót phép kiểm rẻ này. | |
| R4 | Đúng; KHÔNG CHẶN | Bậc 0 = 12 ca auth + 1 ca train. Đã sửa diễn giải (Đ4). | |
| R5 | Đúng; KHÔNG CHẶN | (a) STATE và §10 cũ; (b) thiếu mục luồng A; (c) TORAI A là 3 ca, không phải 2; (d) "đủ bảng bắt buộc" nói quá; (e) C-d3 OB không nhắc. Đã sửa ở LOG, STATE và Đ5. | |
| N1 | Tự tìm; KHÔNG CHẶN | Bằng chứng mô tả mới từ T-056 phần 2 cho ứng viên 2 ở §7.5 (Đ, mục N1). Vẫn là sau khi xem test. | |
