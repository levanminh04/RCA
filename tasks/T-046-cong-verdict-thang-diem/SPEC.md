# T-046 — Thiết kế lại cổng kiểm định, quy tắc `verdict` và quyết thang điểm của M1

- **Trạng thái:** đã duyệt (01/11/2026, lời Minh trong chat: “duyệt tạo spec luôn, kèm prompt cho phiến claude mới độc lập hoàn toàn yêu cầu triển khai 46, trước khi triển khai cần tự rà soát spec độc lập dựa trên các thông tin đã có, nếu có vấn đề hoặc rủi ro lỗ hỏng, bỏ khó chọn dễ, thì cho phép sửa lại spec rồi mới bắt đầu triển khai task”). Bản này là bản 2: bản 1 do Claude soạn trong chat ngày 01/11/2026; Codex rà trong chat cùng ngày (bốn điểm CHẶN, đều được người soạn nhận đúng và sửa); lượt kiểm lại bản 2 không làm vì Minh duyệt thẳng. Minh duyệt nguyên đề xuất, nên các mức ở cột "Đề xuất" của bảng tiêu chí có hiệu lực.
- **Người làm:** Claude (một phiên mới, độc lập với phiên soạn SPEC). **Người phản biện:** Codex.
- **Thuộc gói MRP:** P6 (M1). **Cổng:** chuẩn bị G3.
- **Phụ thuộc:** T-045 đã nghiệm thu (Q-222); code `bbef69dd`, commit kết quả `bc10d947`; D17 Q-a, Q-b (Q-218); LOG T-045 phiên 2 (gói quyết định bản sửa theo lượt 2: QĐ-2, QĐ-3, QĐ-4); `tasks/T-045-chay-khoi-k-dev/REVIEW-2-claude.md` U2, U3.
- **Nguồn chia task:** lời Minh chat 01/11/2026 “t46 claude làm, 47 codex làm” (QĐ-2 phương án (ii); dòng DECISIONS đề xuất Q-224, chưa ghi).
- **Quyền rà và sửa SPEC trước khi triển khai** (lời Minh ở dòng Trạng thái): phiên người làm đầu tiên tự rà SPEC độc lập trên thông tin trong repo; nếu thấy vấn đề, rủi ro, lỗ hổng hoặc chỗ SPEC chọn việc dễ bỏ việc khó, được sửa SPEC trước khi bắt đầu bước 0 của phần triển khai. Mọi sửa ghi ở LOG mục "Rà và sửa SPEC" (đoạn cũ → đoạn mới, lý do, ảnh hưởng). Không được dùng quyền này để: đổi mục tiêu hay câu hỏi nguồn; nới tiêu chí hay bỏ phép kiểm cho dễ đạt; thêm quyền đọc root, tính MRR, mở dữ liệu khóa; chọn ứng viên. Sửa nào làm tiêu chí lỏng hơn hoặc thu hẹp phạm vi thì dừng, trình Minh.

## Mục tiêu

**Câu hỏi nguồn:** MRP P6 (`docs/MRP.md:257`: trước G3 phải kiểm đầu vào, trung gian, hành vi trên dev, không chỉ chạy không lỗi); SPEC T-043 B6 (khóa chế độ tính cổng, α, ε, điều kiện của `verdict` trước G3); DT18-NV2.

**Hiện tượng (T-045):**
- `verdict` = CAUSE_FOUND ở 30/30 cửa sổ giả RE2-TT, ở mọi cấu hình; ở cửa sổ thật 52/52 (`results/T-045/t1.json`, `khoi-k.json`).
- Ở α = 0,001 vẫn khoảng 61 kênh có cờ mỗi cửa sổ giả (`results/T-045/t4.json#/cau_hinh/T4-e0.05-a0.001/moc_gia/kenh_co_theo_nhom`).
- Với cùng cờ, nhánh z cho MRR RE2-TT 0,983 so với 0,718 của R0 (`results/T-045/t4b.json`).

**Loại task:** chẩn đoán, thiết kế, cài đặt, kiểm hành vi. Không chọn thành phần khối K. **Không đọc root, không tính MRR.** Có dùng mốc tiêm (chế độ (a)) để biết cửa sổ nào có lỗi.

**Vai trò dữ liệu:** mọi dữ liệu trong task là dữ liệu dev dùng để chọn và kiểm lại; không có phần kiểm độc lập. RE2-TT dev chỉ có 720 giây trước t (đã đọc cột `time` của `metrics.parquet` ở 5 ca; kiểm đủ 30 ca ở bước 1). Phép A/A trên N nằm trong phía A của cửa sổ giả C-e (t′ = t − 300). Vì vậy:
- chọn ứng viên chỉ bằng A/A, dữ liệu tổng hợp và cửa sổ thật;
- khóa ứng viên (ghi LOG kèm hash) trước khi xem kết quả trên C-e;
- C-e chỉ báo sau khi khóa, như phép kiểm lại có chồng lấn dữ liệu, không là bằng chứng độc lập;
- T-047 dùng lại C-e cho vế mốc giả của luật C, kèm giới hạn này.

**Đạt task này cho:**
1. Chẩn đoán nguyên nhân cổng qua giả: phân xử hoặc thu hẹp.
2. Cổng và `verdict` chọn theo luật khai trước, hoặc xung đột trình Minh.
3. Quyết giữ hay đổi thang điểm theo tiêu chí khai trước.
4. Code có test, chế độ cũ làm mặc định.

**Phần nguồn chưa bao phủ:**
- **Hiệu chuẩn metric Nezha-OB: OPEN.** Chỉ có 5 điểm ở N, 5 điểm ở A (SPEC T-043 dòng 349; `m_metric` = 5 ở `results/T-043/ma-tran-thu.json#/tham_so_E4`), nên không làm A/A được. Xử lý: không đổi cổng cho loại đơn vị này, trừ khi ứng viên được chọn là một quy tắc chung áp được theo cùng công thức; ghi giới hạn; kiểm trên FlashTicket. Không hạ hỗ trợ tối thiểu.
- Báo nhầm của Nezha-OB khi hệ khỏe (D6): FlashTicket.
- Đối chứng không đồ thị đủ mạnh (LESSONS QT7): task (3), trước khi khóa danh sách so sánh ở G3.
- Chọn lại khối K: T-047.

## Câu hỏi, bằng chứng và quyết định

Mọi dự đoán là **chưa kiểm**.

| # | Câu hỏi | Giải thích khác | Phép kiểm | Hỗ trợ / bác bỏ khi | Còn thiếu |
|---|---|---|---|---|---|
| C1 | Vì sao cổng từng đơn vị qua giả nhiều hơn α? | Tự tương quan; trôi nền; mẫu lớn nhạy với chênh nhỏ; tải đổi | Trên N của 52 ca, theo loại đơn vị và nguồn (trừ metric Nezha-OB): hàm tự tương quan; tỷ lệ qua cổng A/A (nửa đầu so nửa sau của N, mỗi nửa 150 giây) với G0, G1, G3 | Cổng có tính tới tự tương quan đưa A/A về gần α: hỗ trợ tự tương quan. Vẫn cao: hỗ trợ trôi nền hoặc không dừng | A/A 150 + 150 giây khác cỡ 300 + 300 của phép thật |
| C2 | Quy tắc gộp của `verdict` | Lỗi chỉ ở cổng | Tỷ lệ CAUSE_FOUND ở cửa sổ A/A và cửa sổ thật, theo tổ hợp cổng × quy tắc | Tiêu chí (a), (b), (c1) | — |
| C3 | Giữ hay đổi thang điểm? | Nhánh z còn đổi cách ghép đơn vị phân vị (không bị chặn) với kênh đếm (trong [0; 1]) | Tỷ lệ kênh phân vị có cờ đạt rA = 1 theo hướng đang xét (bão hòa đúng nghĩa; trần e = 1 − rN, `src/m1/e4.py` hàm `cham_phan_vi`). Báo riêng NEW_OP, STOPPED vì bị gán 1 theo quy tắc (`cham_dem`). Số thực thể hòa ở phần tử đầu của khóa tầng 1. Đo trên R0 với cổng đã khóa, cửa sổ thật | Tiêu chí (S) | Tương tác với E1, E2: T-047 |
| C4 | Còn phản ứng với lỗi không? | Giảm báo nhầm bằng cách làm đầu ra mất tác dụng; CAUSE_FOUND ở cửa sổ thật có thể do nhiễu | (c1) CAUSE_FOUND ở 52 cửa sổ thật. (c2), báo sau khi khóa: cặp cùng ca RE2-TT, số đơn vị có cờ ở cửa sổ thật so với C-e | (c1) dùng để chọn; (c2) chỉ báo | — |

**Phạm vi phép kiểm (đặc tả trước khi đánh giá):**
- Đơn vị: mọi đơn vị trong U, hợp lệ (`hop_le`), ở thế giới đang tính. Mỗi hướng trong `huong_cham` là một phép. `verdict` tính ở P như hiện hành; S_lo, S_hi áp cùng quy tắc.
- Ứng viên cổng chỉ đổi p của đơn vị phân vị. Ngưỡng h, l và cách tính e giữ nguyên.
- Đơn vị đếm giữ kiểm nhị thức hiện hành. Nếu A/A ở bước 3 cho thấy đơn vị đếm cũng qua giả nhiều hơn mức (a) thì dừng ở D-1, trình Minh; không tự thêm ứng viên.
- NEW_OP, STOPPED giữ là cờ trực tiếp, không thuộc họ phép kiểm để hiệu chỉnh. Báo riêng số cửa sổ chỉ CAUSE_FOUND nhờ các cờ này.
- Quy tắc `verdict` mới chỉ đổi `verdict`, không đổi `F_raw`, tầng hay thứ hạng.

**Ứng viên** (không chọn trước):
- **Cổng:**
  - G0: Mann–Whitney hiện hành.
  - G1: Mann–Whitney trên trung bình của các khối thời gian không chồng. Độ dài khối b là độ trễ nhỏ nhất mà hệ số tự tương quan trên N dưới 0,2, chặn trong [5; 60] giây, đo riêng từng đơn vị chỉ trên N. Cần ít nhất 5 khối mỗi phía; nếu không thì giữ G0 cho đơn vị đó và đếm số đơn vị như vậy.
  - G3: kiểm hoán vị theo khối cùng b, thống kê rA − rN, 2.000 hoán vị, seed cố định, một phía theo hướng.
  - Không xét cỡ mẫu hiệu dụng gắn vào Mann–Whitney: chưa có công thức p kiểm được.
- **`verdict`:**
  - V0: hiện hành.
  - V1: Holm trên họ phép kiểm của cửa sổ ở mức α. CAUSE_FOUND khi có ít nhất một phép qua mức đã hiệu chỉnh và có e > 0 (như điều kiện cờ), hoặc có NEW_OP/STOPPED.
  - V3: cần ít nhất k = 2 đơn vị có cờ tự sinh.
  - Không xét Benjamini–Hochberg: `verdict` trả lời câu hỏi theo cửa sổ ("có bất thường tự sinh không"), nên mục tiêu là kiểm soát sai theo cửa sổ.
- **Thang điểm:** S0 E4 (D24); S1 E4 cộng khóa phụ độ lớn (T4c, đã cài); S2 z có chặn. Ứng viên phải giữ việc so được kênh phân vị với kênh đếm (WHY-56).
- **Thứ tự ưu tiên khi nhiều ứng viên đạt:** cổng G0 < G1 < G3; `verdict` V0 < V3 < V1. Lý do: ít giả định thêm và rẻ hơn đứng trước.

**Mức tiêu chí** (đề xuất của người soạn; Minh duyệt nguyên đề xuất, nên cột "Đề xuất" có hiệu lực):

| Tiêu chí | Dùng để | Đề xuất (hiệu lực) | Phương án khác đã xét | Đánh đổi |
|---|---|---|---|---|
| (a) Tỷ lệ qua cổng ở A/A, theo loại đơn vị và nguồn (trừ metric Nezha-OB) | Chọn | ≤ 2α | ≤ 3α | Chặt hơn thì mất độ nhạy; trôi nền còn OPEN, nên không đòi bằng đúng α |
| (b) Tỷ lệ CAUSE_FOUND ở 52 cửa sổ A/A (Nezha-OB không có metric, báo riêng theo dataset) | Chọn | ≤ 0,20 | 0,10; 0,33 | Báo kèm khoảng Wilson |
| (c1) Tỷ lệ CAUSE_FOUND ở 52 cửa sổ thật | Chọn | ≥ 0,80 | 0,90; 0,70 | Chỉ có nghĩa với V1, V3 (V0 đã là 52/52) |
| (b′), (c2) CAUSE_FOUND ở 30 C-e; so cặp thật với C-e | Báo sau khi khóa | — | — | Không đạt (b′) ở mức (b) thì dừng, trình Minh, không chọn lại |
| (S) Mở thay thang điểm khi tỷ lệ kênh phân vị có cờ đạt rA = 1 ở cửa sổ thật | Quyết thang | ≥ 25% | 15%; 40% | Chưa đo; mức đặt trước khi đo. Từ mức này, khoảng một phần tư bằng chứng phân vị không còn phân biệt độ lớn, thứ hạng dựa nhiều vào khóa phụ |

**Luật chọn:** tổ hợp cổng × `verdict` đạt (a), (b), (c1), lấy theo thứ tự ưu tiên. Không tổ hợp nào đạt thì dừng, trình Minh.

## Đầu vào

- Bản ghi T-045, kiểm theo `results/T-045/manifest.json`.
- Dữ liệu dev RE2-TT 30 ca, Nezha-OB 22 ca, đọc lại chuỗi gốc qua adapter M1 khi cần; ưu tiên bản ghi cũ.
- Mốc t theo chế độ (a) (`p3.nhan.nap_moc`, chỉ mốc tiêm); C-e như T-045.
- **Không đọc:** root, loại lỗi, ô, MRR; `data/locked/`; test Nezha-OB; RE3-OB.
- Môi trường: `results/T-045/scripts/moi_truong.sh`; lệnh và script của T-045 dùng lại được (`results/T-045/scripts/`).

## Đầu ra (`results/T-046/`)

`chan-doan-cong.json` (C1), `ung-vien.json` (C2, C4; gồm hash của phần khóa), `kiem-sau-khoa.json` ((b′), (c2)), `thang-diem.json` (C3), `so-lan-nhin.jsonl`, `bao-cao.md`, `manifest.json`, `runs/`, `tests/`. Đề xuất WHY trình trong LOG.

## Phạm vi ghi

- `results/T-046/`; `tasks/T-046-cong-verdict-thang-diem/LOG.md`; SPEC này theo quyền rà và sửa ở đầu tệp (chỉ trước bước 0 của phần triển khai); dòng T-046 trong `docs/STATE.md`.
- `src/m1/` chỉ phần cổng, `verdict`, thang điểm và tham số chọn chế độ, sau điểm dừng D-2; mỗi thay đổi một commit.
- Không ghi `results/T-043/`, `results/T-044/`, `results/T-045/`, DECISIONS, WHY, MRP, KE-HOACH, task khác.

## Các bước

0. **Mở phiên.** Đọc AGENTS, STATE, SPEC này, LOG T-045 phiên 2, báo cáo T-045. Tự rà SPEC theo quyền ở đầu tệp; ghi kết quả rà vào LOG trước khi làm bước nào khác. Kiểm hash T-045; chạy test T-044 (374), T-045 (16); ghi dòng mở phiên.
1. **Kiểm dữ liệu:** độ dài trước t ở 52 ca; số đơn vị đủ hỗ trợ cho A/A theo loại và nguồn; đo chi phí G3 trên 1 ca.
2. **Kiểm ứng viên trên dữ liệu tổng hợp:** AR(1) như SPEC T-043 dòng 415, cộng trôi bậc thang. Mục đích: xác nhận G1, G3 cài đúng và hiệu chuẩn được trong điều kiện đã biết.
3. **Chẩn đoán C1 trên dev** (A/A, tự tương quan) với G0, G1, G3, theo loại đơn vị và nguồn.
4. **Điểm dừng D-1:** trình Minh nếu đơn vị đếm qua giả nhiều hơn mức (a), cần ứng viên ngoài danh sách, hoặc một tiêu chí không đo được.
5. **Đánh giá và khóa:** tính (a), (b), (c1); áp luật chọn; ghi LOG tổ hợp đã khóa kèm hash `ung-vien.json`, **trước** khi xem C-e.
6. **Kiểm sau khóa:** (b′), (c2) trên C-e. Không đạt thì dừng, trình Minh; không chọn lại.
7. **Thang điểm:** đo C3; áp (S). Giữ S0, hoặc đề xuất S1/S2; đổi D24 thì Minh quyết.
8. **Điểm dừng D-2:** trình đề xuất WHY (cổng, `verdict`, thang điểm, phần metric Nezha-OB OPEN); Minh duyệt rồi mới cài.
9. **Cài vào `src/m1`:** chế độ mới bật bằng tham số, mặc định giữ hành vi cũ. Test ở `results/T-046/tests/`. Test T-044 qua ở chế độ mặc định; `tat_dinh` qua ở chế độ mới. Khai cách T-047 bật chế độ mới mà không sửa `results/T-043/`.
10. **Kiểm hành vi bằng code đã cài:** R0 chế độ mới trên 52 ca, cửa sổ A/A và 30 C-e, không đọc root; tái lập số bước 5–7; bất biến seed 0/1/2 và thứ tự hàng ở 2 ca mỗi dataset; QT5.
11. **Báo cáo** tách quan sát, suy luận, chưa phân xử. Manifest, LOG, STATE, prompt phản biện cho Codex.

## Kiểm đúng đắn

- Bước 2 kiểm cài đặt ứng viên trên dữ liệu đã biết đáp án.
- Bước 10 tái lập số của bước 5–7 bằng code đã cài.
- Khóa trước khi xem C-e có hash trong LOG.
- Không tính MRR; mọi lần nhìn số dev ghi `so-lan-nhin.jsonl`.
- Không kiểm được: hiệu chuẩn metric Nezha-OB; trôi nền với tải đổi trên dữ liệu công khai; tính độc lập của C-e.

## Tiêu chí xong

1. Test T-044, T-045 qua ở đầu phiên và sau mỗi commit `src`.
2. C1 có kết quả theo loại đơn vị và nguồn: phân xử, hoặc "chưa phân xử" kèm bằng chứng còn thiếu. Metric Nezha-OB ghi OPEN.
3. Tổ hợp cổng × `verdict` được khóa theo luật trước khi xem C-e (có hash); kiểm sau khóa đã báo; hoặc xung đột đã trình Minh.
4. Thang điểm quyết theo (S) với bão hòa đo bằng rA = 1; đổi D24 có Minh duyệt.
5. WHY được duyệt trước khi cài; chế độ cũ không đổi hành vi (374/374).
6. Bước 10 tái lập số.
7. Không đọc root, không tính MRR; mọi lần nhìn số đã ghi.

## Không làm

Chọn E1–E5; tính MRR; sửa luật chọn khối hay ma trận T-043; hạ hỗ trợ tối thiểu; đổi kiểm định của đơn vị đếm khi chưa qua D-1; đối chứng QT7; mở test hay RE3-OB; chạy khối K.

## Chi phí ước lượng

- Ba ứng viên cổng (G0, G1, G3) × (52 cửa sổ A/A + 52 cửa sổ thật + 30 C-e). Quy tắc `verdict` tính lại từ cùng p, rẻ.
- G0, G1 rẻ hơn một lượt R0 (T-045 đo khoảng 20 giây cho một cấu hình trên một ca RE2-TT). G3 với 2.000 hoán vị chưa đo; đo ở bước 1, quá 1 giờ một lượt thì báo Minh (luật cứng 8).
- Dự kiến 1–2 phiên, nghỉ ở D-2.

## Rủi ro và điều chưa chắc

- Không tổ hợp nào đạt nếu trôi nền mạnh.
- Kiểm theo khối làm yếu tín hiệu của lỗi ngắn.
- A/A 150 + 150 giây hiệu chuẩn ở cỡ mẫu khác phép thật.
- C-e chồng lấn dữ liệu chọn.
- Mọi ứng viên chưa kiểm.

## Prompt bàn giao

Prompt triển khai cho phiên Claude mới trình trong chat ngày 01/11/2026 (chép ở LOG). Cuối task, người làm soạn prompt phản biện cho Codex theo `docs/review-prompt.md`.
