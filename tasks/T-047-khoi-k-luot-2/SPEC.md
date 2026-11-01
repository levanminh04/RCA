# T-047 — Lượt chạy khối K thứ hai trên 52 ca dev với cổng, `verdict` và thang điểm của T-046

- **Trạng thái:** đã duyệt tạo (01/11/2026, lời Minh trong chat: “duyệt tạo spec luôn …”, cùng lúc với SPEC T-046). Bản do Claude soạn trong chat ngày 01/11/2026; Codex rà bản 1 trong chat cùng ngày (hai điểm KHÔNG CHẶN: cách kiểm manifest lịch sử; đơn vị của ngân sách), bản này đã sửa theo hai điểm đó. Triển khai sau khi T-046 được nghiệm thu. Quyền chạy lượt dài hơn 1 giờ và chạy qua đêm (luật cứng 8) chờ Minh khi mở task.
- **Người làm:** Codex, chạy local trên máy của Minh. **Người phản biện:** Claude.
- **Thuộc gói MRP:** P6 (M1). **Cổng:** chuẩn bị G3.
- **Phụ thuộc:** T-046 đã nghiệm thu; commit `src` ghi khi nghiệm thu T-046; WHY của T-046 đã ghi.
- **Nguồn chia task:** lời Minh chat 01/11/2026 “t46 claude làm, 47 codex làm” (Q-224 đề xuất, chưa ghi).

## Mục tiêu

**Câu hỏi nguồn:** như T-045 (DT18-NV2; MRP P6 tầng 1–4; MRP P7 đoạn kiểm hành vi trên dev trước G3). Các câu Q1, Q3, Q6, Q8 theo bảng câu hỏi của SPEC T-043.

**Loại task:** chạy thử trên dev theo ma trận và luật chọn đã khai (SPEC T-043 B4, Phụ lục C), với cổng, `verdict` và thang điểm do T-046 khóa. Mọi tham số và luật khác giữ như T-045.

**Đạt task này cho:**
- T1 với code mới;
- cấu hình thắng của khối K lượt thứ hai, hoặc xung đột trình Minh. Lượt này quyết lại kết cục của E1, E2, E3, E5 và là nền cho task (2);
- so với T-045, chỉ mô tả.

**Không cho:** bằng chứng hiệu quả trên dữ liệu chưa dùng để thiết kế. Đây là **lần chọn cấu hình thứ hai trên cùng 52 ca dev**: số dev lạc quan hơn T-045; hồ sơ G3 phải nêu. C-e đã dùng để kiểm cổng ở T-046 (sau khóa, có chồng lấn dữ liệu), nên vế mốc giả của luật C ở T-047 không dựa trên dữ liệu độc lập.

**Phần nguồn chưa bao phủ:** K-b, T6–T12, KB (task (2a), (2b)); T13, A4, hồ sơ G3 (task (3)); T4, T4b với code mới (xem "Không làm").

## Câu hỏi, bằng chứng và quyết định

| # | Câu hỏi | Giải thích khác | Phép kiểm | Hỗ trợ / bác bỏ khi | Còn thiếu |
|---|---|---|---|---|---|
| T1 | Code mới chạy đúng trên dữ liệu thật không? | Lỗi cài đặt của chế độ mới | Bất biến seed 0/1/2 và thứ tự hàng; QT5; mốc giả; tái lập số bước 10 của T-046 | Bất biến đạt; tái lập khớp | Lệch thì đính chính, dừng |
| Q1, Q3, Q6, Q8 | E1-U, E2-C, E3, E5 bật/tắt trong bối cảnh khối | Một ca đổi hạng đã vượt ngưỡng; nhiễu 52 ca; tác động của cổng mới | Khối K; luật C ba thế giới, gồm vế mốc giả nay có thể hoạt động; luật chọn khối bước 1–8 và 10 | Theo luật | Kết cục ở chuỗi cuối: KB (task (2b)) |
| S | Lựa chọn bền tới đâu? | Vài ô quyết định | Phép độ bền như SPEC T-045 bước 7, seed mới ghi trước | — | Không dùng để chọn |
| M | Thành phần nào đổi kết cục so với T-045, vì sao? | Do cổng, do thang điểm, do nhiễu | Đối chiếu từng cặp T-045 ↔ T-047; lần theo cơ chế (luật cứng 15) cho cặp đổi kết cục | Chỉ mô tả | — |

## Đầu vào

- Code theo commit nghiệm thu T-046; chế độ cổng, `verdict`, thang điểm đã khóa ở T-046, bật theo cách khai ở T-046 bước 9.
- Dữ liệu dev như T-045; mốc giả C-e như T-045. Nhãn chỉ đọc ở pha 2, sau khi hash pha 1 đã ghi LOG.
- Bản ghi baseline P3 cho D2: kiểm hash; số G2 không đổi.
- **Kiểm hash:**
  - đầu ra cũ kiểm bằng manifest cũ (T-043, T-044, T-045); không sửa các manifest này;
  - phần `src/m1` của manifest cũ kiểm tại revision tương ứng (`69ef90b6` cho T-044, `bbef69dd` cho T-045), bằng `git show` hoặc worktree tạm chỉ đọc;
  - code mới kiểm bằng manifest T-046.
- Môi trường: như T-045 (`results/T-045/scripts/moi_truong.sh`); bộ điều phối và script của T-045 dùng lại được.

## Đầu ra (`results/T-047/`)

`runs/`, `t1.json`, `khoi-k.json` và `khoi-k/`, `tai-lap-baseline.json`, `co-che-khoi-k.json`, `do-ben.json`, `so-sanh-t045.json`, `so-lan-nhin.jsonl`, `dinh-chinh-cai-dat.md` (nếu có), `bao-cao.md`, `manifest.json`.

## Phạm vi ghi

- `results/T-047/`; `tasks/T-047-khoi-k-luot-2/LOG.md`; dòng T-047 trong `docs/STATE.md`.
- `src/m1/`, `src/m1_danh_gia/` chỉ để sửa lỗi theo đính chính Minh duyệt, mỗi sửa một commit.
- Không ghi `results/T-043/`–`results/T-046/`, DECISIONS, WHY, MRP, KE-HOACH, task khác.

## Các bước

0. **Mở phiên.** Kiểm hash theo mục Đầu vào; test T-044 ở chế độ mặc định, test T-045, T-046; ghi phiên bản môi trường; ghi dòng mở phiên.
1. **Chạy thử:** R0 chế độ mới trên 1 ca mỗi dataset; QT5; đo thời gian, RAM; dự báo lượt đầy đủ. Dự báo vượt ngân sách duyệt thì dừng, báo.
2. **T1:** R0 trên 52 ca × seed 0/1/2, cộng xáo hàng, cộng 30 cửa sổ giả RE2-TT. Báo các đại lượng như T-045 đầu ra 2; đối chiếu số của T-046 bước 10.
3. **Khối K pha 1:** 16 cấu hình × (52 ca + 30 cửa sổ giả). Cách khớp E3 (a), cách đọc nhóm vòng C′. Ca ERROR giữ nguyên, tính là trượt. Ghi hash vào LOG **trước** pha 2.
4. **Pha 2:**
   - D2: tái lập 12/12 MRR baseline; lệch thì dừng.
   - Ghép nhãn; luật C cho mọi cặp ở ba thế giới.
   - Luật chọn khối bước 1–8 và 10; bảng mặc định như SPEC T-045. Thêm tình huống dừng: vế mốc giả loại mọi cấu hình (bước 7 không còn cấu hình).
   - C-d1, C-d3 chỉ báo cáo.
5. **Lần theo cơ chế** cho thành phần có kết cục khác T-045, và cho kết cục HẠI ở cấu hình thắng: theo ca và ô, cả ca tụt lẫn ca lên, ca đúng có điều kiện tương ứng; cờ M5; dấu vết E5.
6. **Phép độ bền:** như SPEC T-045 bước 7; seed ghi LOG trước khi chạy.
7. **So với T-045:** kết cục từng cặp và cấu hình thắng; chỉ mô tả. Lượt T-047 là lượt hiệu lực cho task (2); không chọn giữa hai lượt.
8. **Báo cáo:** như SPEC T-045 bước 8. Manifest, LOG, STATE, prompt phản biện cho Claude.

## Kiểm đúng đắn

- Như T-045: T1 không nhãn; hash trước pha 2; so ca đúng với ca sai có điều kiện tương ứng; D2 tái lập baseline.
- Chế độ cổng của mọi bản ghi phải khớp cấu hình đã khóa ở T-046 (kiểm trong `tham-so.json` của từng lượt).

## Tiêu chí xong

1. Test qua ở đầu phiên.
2. T1 bất biến đạt; QT5 không có giá trị vô lý; tái lập số T-046 bước 10.
3. Khối K đủ 16 × 52 lượt chấm, cộng 16 × 30 cửa sổ giả; hash pha 1 ghi trước pha 2.
4. Luật chọn khối áp đủ bước 1–8 và 10, có vết; có cấu hình thắng kèm cờ, hoặc xung đột đã trình Minh.
5. D2 khớp 12/12.
6. Phép độ bền và so sánh T-045 có trong kết quả.
7. Lần theo cơ chế cho các kết cục đổi.
8. Mọi lần nhìn số dev được ghi.
9. Báo cáo tách: kết cục theo luật C; quan sát; chưa phân xử; quyết định cho task (2).

## Không làm

- K-b, T6–T12, KB, T13.
- T4, T4b với code mới. Nếu cần độ nhạy α, ε của cổng mới, Minh quyết thêm.
- Đổi tham số, luật chọn hay ma trận sau khi thấy số; chọn giữa lượt T-045 và T-047.
- Đọc dữ liệu khóa; chạy trên cloud.

## Chi phí ước lượng

- 1.550 lượt (cấu hình, ca): T1 238; khối K 1.312.
- Mốc so: đợt `d17-002` của T-045 chạy 1.410 lượt (cấu hình, ca) (17 lượt × 30 ca; 5 lượt T1, 2 lượt khối K 16 cấu hình, 10 lượt D3 một cấu hình) trong khoảng 2,4 giờ với 4 tiến trình.
- Ước 2,5–5 giờ thực, **chưa kiểm**; đo lại ở bước 1 vì cổng mới có thể chậm hơn. Vượt 1 giờ một lượt nên cần Minh duyệt chạy dài hoặc qua đêm.

## Rủi ro và điều chưa chắc

- Vế mốc giả nay có thể loại nhiều cấu hình, dẫn tới xung đột.
- Kết cục có thể khác T-045 chỉ vì nhiễu 52 ca.
- Chế độ mới mới chạy toàn bộ dev ở T-046 bước 10 (chỉ R0).

## Prompt bàn giao

Prompt mở task cho Codex soạn khi T-046 được nghiệm thu. Cuối task, người làm soạn prompt phản biện cho Claude theo `docs/review-prompt.md`.
