# T-029 — P4: hạn chế phát hiện ở chế độ (b)

- **Trạng thái:** trình duyệt 08/10/2026. Đã qua ba lượt phản biện (REVIEW, REVIEW-2, REVIEW-3), sửa theo lời Minh duyệt 08/10. Chờ Minh duyệt SPEC. Khi Minh duyệt, SPEC khóa.
- **Người làm:** Codex
- **Người phản biện:** Claude
- **Thuộc gói MRP:** P4 — **Cổng:** G2

## Mục tiêu

MRP P4 yêu cầu làm cho phần phát hiện điều đã làm cho xếp hạng ở T-028 (Q-30): ca nào bộ phát hiện bỏ sót, báo sai, báo trễ, và vì sao. Đây là việc "chỉ ra vấn đề tồn đọng" của cô, phục vụ RQ2 và là căn cứ cho phần phát hiện của P6 (RQ3a). DT18-NV2 đặt "phát hiện dấu hiệu bất thường" ngang với xếp hạng; DT18-NV3 yêu cầu phân tích trường hợp phương pháp còn hạn chế.

T-025 đã đo nhưng mới diễn giải một phần: báo động đầu đúng BOCPD 3/30, N-Sigma chính 0/30, N-Sigma đối chứng 0/30 (`results/T-025/phat-hien.json` → `bo_phat_hien.<bộ>.tong_hop.theo_ca_tren_30.bao_dong_dau_dung`). Các giả thuyết cơ chế ở `results/T-025/phat-hien.md` §3 còn "chưa kiểm". Giao thức V2 §10 giao cho P4 kiểm tương quan giữa cột vắng và nhãn.

Task trả lời sáu câu, trên 30 ca dev RE2-TT:

- **C1 — Thất bại ở đâu.** Với từng bộ phát hiện: ca nào báo động đầu trước mốc, ca nào báo trễ, ca nào bỏ sót; tách theo ô và theo ca.
- **C2 — Vì sao.** Cơ chế nào giải thích báo động sai trong đoạn nền; bằng chứng đến mức nào (can thiệp, liên hệ, đọc tay); giải thích khác còn mở.
- **C3 — Có chỉ ra vùng không.** Bộ phát hiện có cho biết thành phần nào bất thường không; nếu có, thành phần đó có phải root không (giả thuyết 5 của MRP P4).
- **C4 — Phụ thuộc mốc biết trước.** RCA mất bao nhiêu khi chạy ở báo động thay vì ở mốc (giả thuyết 4 của MRP P4); chênh lệch có dấu (có thể âm) do chọn sai sự kiện và chênh lệch có dấu (có thể âm) do lệch cửa sổ khi đã chọn đúng sự kiện.
- **C5 — Độ vững của số T-025.** Nhãn proxy "lỗi kéo dài tới cuối file" có đứng không; cột vắng có tương quan với nhãn không.
- **C6 — Tác giả có tự nêu không.** Mỗi hạn chế: tác giả đã nêu (dẫn nguồn), hay chưa thấy trong nguồn đã khảo sát.

## Đầu vào (chỉ đọc)

- `results/T-025/`: `bao-dong.json` (báo động thô, `detector_columns`, `input_shape`, `diagnostics`), `phat-hien.json` (gồm `audit_cot`), `cham/phan-tich-b.json`, `cham/soi-nsigma-t-hat.json`, `cham-b.json`, `cham-thu-gia/`, `runs/`, `scripts/` (gồm `rca_b.py` có chế độ `t_co_dinh`), `phat-hien.md`, `cham-b.md`.
- `results/T-024/cham-a.json` và bản ghi chế độ (a) mà nó dẫn.
- `results/T-022/giao-thuc-v2.md` §4, §7, §8, §10; `allowlist-dev.json`; `nhan-dev.json`; `cot-bocpd-dev.csv`; `mappings/universe-re2tt-dev.json`.
- Metric thô 30 ca dev trong `data/`, qua guard SHA-256 của allowlist dev.
- `src/p3/` (dùng như thư viện, không sửa): `adapters/phat_hien.py`, runner, `danh_gia.py`.
- Hồ sơ `results/T-013/ho-so-bocpd.md`, `ho-so-nsigma-phat-hien.md`, `cua-so-va-che-do-b.md`; code BARO `e35f4ec` trong môi trường đã dựng.
- Nguồn công bố RCAEval đã lưu ở `results/T-002/public-metadata/` và `docs/knowledge/`; nếu thiếu, đọc bài/README RCAEval trực tuyến (không tải file).

Mẫu: 30 ca = 10 ô (5 root × loại lỗi) × 3 lần lặp; root: auth, order, route, train, travel (6 ca mỗi root); loại lỗi: cpu, disk, delay, loss (6 ca mỗi loại), mem, socket (3 ca mỗi loại). Nguồn: `results/T-022/nhan-dev.json` → `cases`.

## Thiết kế phân tích — khóa trước khi tính

Mọi định nghĩa, ngưỡng và độ nhạy dưới đây khóa khi Minh duyệt SPEC. Không đổi sau khi thấy số. Ngưỡng là đề xuất, **chưa kiểm**; lý do ở Phụ lục (WHY-39).

### Ký hiệu

- Lưới 1 giây, chỉ số i = 0..1440. Mốc tiêm ở chỉ số 720 ở cả 30 ca (T-025 đã kiểm; script kiểm lại và dừng nếu khác).
- s0: điểm đánh giá đầu tiên (N-Sigma 100, BOCPD 1). Đoạn nền được đánh giá Nv = [s0, 720). Đoạn sau mốc Av = [720, 1440].
- t̂: báo động đầu (T-025). t̂⁺: báo động đầu tiên ≥ 720.
- Ba bộ: BOCPD, N-Sigma chính (tập cột BOCPD), N-Sigma đối chứng (mọi cột). 90 cặp (ca, bộ).

### A. Kết quả mỗi cặp (ca, bộ)

- **S:** t̂ ≥ 720. **E:** t̂ < 720; tách E-gần (cửa sổ RCA A = [t̂, t̂+300) chứa mốc) và E-xa. **Miss:** không có báo động trong Av.
- Với mọi cặp có t̂⁺: độ trễ t̂⁺ − 720. Với BOCPD gọi là "độ lệch vị trí điểm đổi hồi cứu" (§7.4). Báo phân bố; không đặt ngưỡng "trễ". Với N-Sigma, độ trễ báo cạnh r_obs của Nv (mục B, N3); khi r_obs cao, độ trễ không được đọc là thời gian phát hiện.
- Báo động sai trong Nv: lấy số T-025, không tính lại khác cách.

### B. Cơ chế N-Sigma (cả hai tập cột)

Tính lại cờ báo **từng cột** Z[i, j] bằng đúng hàm BARO `anomaly_detection.nsigma` (k = 3, `startsfrom` = 100) và tiền xử lý D9, gọi riêng từng cột. Hợp theo cột phải trùng báo động T-025 (kiểm V2). p0 = 0,0027 là tỉ lệ báo danh nghĩa hai phía của luật 3σ khi phân phối chuẩn, dừng, độc lập.

- **N1 — Lịch sử ngắn:** tỉ lệ báo mỗi cột-giây trong Nv theo khoảng chỉ số [100, 200), [200, 400), [400, 720). Cờ khi t̂ < 200 **và** tỉ lệ khoảng đầu ≥ 2 lần khoảng cuối. Độ nhạy: 1,5 và 3 lần.
- **N2 — Cột báo dày:** p_j = tỉ lệ báo của cột j trong Nv. Cờ khi có cột báo tại t̂ với p_j > 10·p0. Độ nhạy 5·p0 và 20·p0. Báo kèm số cột báo tại t̂ và loại cột.
- **N3 — E, không có cột báo dày tại t̂ (phần còn lại sau N2):** cờ khi E và không cột nào báo tại t̂ đạt N2. Mọi ca đều báo ba tỉ lệ trên Nv: quan sát r_obs (tỉ lệ giây có báo động gộp), dự báo khi các cột độc lập r_ind = 1 − Π(1 − p_j), danh nghĩa r_nom = 1 − (1 − p0)^d. Ba tỉ lệ là thống kê mô tả. r_obs so với r_ind là độ lệch của báo động gộp so với mô hình các cột độc lập; bằng nhau không có nghĩa là độc lập. r_ind so với r_nom là độ lệch tỉ lệ từng cột so với p0; không tách được phần do lệch chuẩn, nền không dừng hay lịch sử hữu hạn.
- **N4 — Nền gần hằng:** cờ khi có cột báo tại t̂ với std quá khứ bằng 0 (theo cách T-025 đã đếm ở `soi-nsigma-t-hat.json`).
- **N5 — Loại cột:** tỉ lệ báo trong Nv theo loại cột suy từ hậu tố tên (latency, error, cpu, mem, mạng, khác). Bảng mô tả, không là cờ.
- **N6 — Nền nhiễm dữ liệu sự cố:** mean/std mở rộng đưa dữ liệu sau mốc vào nền (`ho-so-nsigma-phat-hien.md:19`). Báo mật độ báo động trong Av theo từng phút sau mốc. Mô tả, không là cờ.

### C. Cơ chế BOCPD

- **B1 — Khuyết điền 0:** dựng lại ma trận sau tiền xử lý bằng chính `tien_xu_ly_bocpd`; số cột phải trùng `input_shape.cot_sau_tien_xu_ly`. Cờ khi có cột mà đoạn đầu NaN (bị điền 0) kết thúc trong [t̂ − 2, t̂ + 2].
- **B2 — Dữ liệu sau mốc lọt vào tiền xử lý:** can thiệp I1. Chỉ xét cặp có t̂ + dung sai ≤ 719 (miền chung của bản đầy đủ và I1); cặp khác ghi N/A. Cờ khi bản đầy đủ có điểm đổi tại t̂ nhưng I1 không có điểm đổi trong t̂ ± 5 s. Độ nhạy ±2 s, ±10 s. Cơ sở: posterior BOCPD ở i chỉ dùng dữ liệu ≤ i (`diem_doi_tu_R` dùng R[:, i+1]), nên thông tin tương lai vào qua bước bỏ cột hằng và min–max trên cả chuỗi (§7.2). I1 chỉ loại thông tin từ [720, 1440]. Min–max và bỏ cột hằng trên [0, 720) vẫn dùng dữ liệu sau t̂, nên B2 = False không có nghĩa là không có look-ahead.
- **B3 — Hazard:** can thiệp I2. Cùng miền xét như B2; ngoài miền ghi N/A. Cờ khi có điểm đổi tại t̂ ở I1 nhưng không có trong t̂ ± 5 s ở I2. Nếu B2 đúng thì B3 là N/A. Báo số điểm đổi trong Nv ở bản đầy đủ, ở I1 và ở I2.
- **B4 — Đổi thật trong dữ liệu thô:** với mỗi cột đầu vào (sau ffill, trước min–max): bước nhảy chuẩn hóa |median(x[t̂, t̂+w)) − median(x[t̂−w, t̂))| / (1,4826·MAD(x[s0, t̂−w))). Cờ khi giá trị lớn nhất qua các cột ≥ 3, với w = 30. Độ nhạy: ngưỡng 2 và 5; w = 15 và 60. MAD = 0 mà bước khác 0: đếm riêng thành nhóm "nền hằng", không gộp vào ngưỡng. Cờ này không phân biệt nền không sạch với biến động tải tự nhiên. Miền hợp lệ theo từng w: đoạn MAD [s0, i−w) có ít nhất 30 điểm và hậu cửa sổ [i, i+w) nằm trước 720, tức i ∈ [s0+w+30, 720−w]. B4 chỉ tính cho cặp E có t̂ trong miền này; cặp S và cặp ngoài miền ghi N/A, không tính là False.
- **B5 — Số chiều:** d (số cột sau tiền xử lý) so với số điểm đổi trong Nv qua 30 ca, theo ô. Mô tả, không là cờ. d có thể đi cùng root (xem P2), nên không quy riêng cho d.

### D. Can thiệp phân tích

Các lượt này dùng mốc để cắt dữ liệu. Chúng là phép phân tích, không phải phương pháp. Số của chúng không thay số P3 và không dùng để chỉnh baseline.

- **I1:** BOCPD trên tiền tố [0, 720) của mọi ca, hazard 1/50 (như gốc), gọi đúng `src/p3/adapters/phat_hien.bocpd`.
- **I2:** như I1, hazard 1/250. Giá trị này có trong code tác giả (`_bocpd.py:184`) nhưng wrapper không dùng (`results/T-013/ho-so-bocpd.md:54, 60`). Chọn vì có sẵn trong code tác giả, không chọn theo nhãn. Wrapper nằm ở `results/T-029/scripts/`; trước khi chạy, wrapper với hazard 1/50 phải tái tạo đúng I1 trên một ca.
- **I3:** RCA tại t̂⁺ cho BOCPD và N-Sigma chính, với BARO native, CIRCA OLS RHT và RHT+DA, TORAI B seed 0, 1, 2. Dùng bản chép `rca_b.py` ở chế độ `t_co_dinh`. Gọi là "RCA tại báo động đầu sau mốc, chọn nhờ nhãn mốc"; không phải cận trên chất lượng RCA. N-Sigma đối chứng không chạy, vì T-025 không có RCA cho bộ này.

### E. Định vị (C3)

- **N-Sigma:** mỗi dịch vụ có "báo động đầu sau mốc" = báo động đầu tiên ≥ 720 trên các cột của dịch vụ đó; ánh xạ cột → dịch vụ theo `mappings/universe-re2tt-dev.json`. Root được xếp theo báo động đầu sau mốc, hạng kỳ vọng khi hòa. Dịch vụ không báo trong Av đồng hạng cuối.
  - Mức nền: hạng kỳ vọng và xác suất đứng đầu nếu thứ tự ngẫu nhiên đều trên cùng tập dịch vụ, giữ nguyên cấu trúc hòa.
  - Độ nhạy: bỏ các cột đạt N2 (loại cột báo dày trong Nv). Độ nhạy này không loại được cột báo kéo dài qua mốc nhưng thưa trong Nv.
- **BOCPD:** đầu ra đa biến không chỉ ra cột hay dịch vụ; ghi đó là đặc điểm thiết kế. Bảng phụ xếp cột theo bước nhảy B4 tại t̂⁺, ghi rõ là heuristic phân tích, không phải đầu ra BOCPD.
- Thứ tự báo động đầu sau mốc không phải quan hệ nhân quả. T-029 không kết luận về "lan". Câu đó thuộc phần tổng hợp G2 theo quyết định của Minh ngày 08/10; gói G2 được phép trích bảng này.

### F. Độ vững của số T-025 (C5)

- **P1 — Nhãn proxy:**
  - Tra thời lượng lỗi trong nguồn công bố RCAEval (bài, README, script tiêm lỗi).
  - Từ dữ liệu: với mọi cột của dịch vụ root (không chọn theo loại lỗi), tính theo từng phút sau mốc tỉ lệ cột có median phút nằm ngoài [q01, q99] của Nv.
  - Chỉ khi nguồn nêu thời lượng D < 721 s mới chấm lại P/R/F1 theo cửa sổ của T-025 với đoạn bất thường [720, 720 + D), đặt cạnh số gốc. Không suy D từ dữ liệu để chấm lại.
- **P2 — Schema:**
  - Từ `audit_cot`, lập bảng chéo cột vắng và d theo root, loại lỗi, ô; đếm chính xác.
  - Đánh dấu cột mà sự có mặt tách hoàn toàn được các root, tức một kênh lộ nhãn qua schema.
  - Không đưa dấu vắng vào phương pháp.

### G. Chế độ (a) so với chế độ (b) (C4)

- Theo ca, theo phương pháp, cho Hit@1 và Hit@5 theo đúng quy ước chấm của T-024/T-025 (hòa, mẫu số giữ non-OK, TORAI theo seed và theo ca; CIRCA theo Q-82: ở từng điểm chạy (a), t̂, t̂⁺ ghi riêng ca có nút RHT > 1e10, và báo thêm bảng ghép cặp trên các ca không vượt ở cả ba điểm):
  - (a) tại mốc, từ `cham-a.json`;
  - (b) tại t̂, từ `cham-b.json`;
  - I3 tại t̂⁺.
- Tách hai chênh lệch có dấu (có thể âm): (a) → t̂⁺ là chênh lệch do lệch cửa sổ; t̂⁺ → t̂ là chênh lệch do chọn sai sự kiện. Báo ghép cặp từng ca; dùng nhóm E-gần và E-xa từ T-025 (`A_chua_moc`).

### Quy tắc chung

- **Đa nhãn.** Thứ tự trình bày N1 → N4, rồi B1 → B4, rồi D0 (không cờ nào). Thứ tự này không là nguyên nhân trội.
- **Đặc trưng trước nhãn.** Đặc trưng và cờ tính trước khi nối nhãn; lưu ở `features-no-label/` kèm hash.
  - Nhãn nối sau là root, loại lỗi, ô.
  - Mốc 720 dùng ngay từ đầu, vì nó giống nhau ở mọi ca và không mang thông tin riêng của ca.
- **Báo cáo:**
  - Tách theo ô và theo ca trước khi nêu mẫu hình (QT15).
  - Kết luận ổn định hay đổi chiều theo độ nhạy khai theo QT3.
  - Số đếm chính xác kèm mẫu số. Không p-value, không ngưỡng "đáng kể".
- **Mức bằng chứng ghi cho từng hạn chế:**
  - "can thiệp": I1, I2, I3 đổi đầu vào hay tham số rồi quan sát đầu ra;
  - "liên hệ": cờ; B1, B4 kèm phép thử giả V7; N1–N4 là phân rã báo động theo cột, không có đối chứng;
  - "đọc tay";
  - "chưa kiểm", kèm lý do.

## Đầu ra (`results/T-029/`)

- `ban-do-han-che-phat-hien.md` — báo cáo chính.
  - Mỗi hạn chế một dòng mã HP-n, để P5/P6 trỏ về.
  - Mỗi dòng ghi: bộ phát hiện, số ca/tổng theo ô, cơ chế, mức bằng chứng, giải thích khác, tác giả có nêu không (dẫn nguồn hoặc "chưa thấy trong nguồn đã khảo sát").
  - Trả lời C1–C6.
- `theo-ca.json` và `theo-ca.csv` — 90 dòng (ca × bộ): t̂, t̂⁺, nhóm kết quả, mọi cờ ở mọi mức độ nhạy, nguồn.
- `n-sigma-cot.json` — p_j, r_obs, r_ind, r_nom, tỉ lệ theo khoảng lịch sử, theo loại cột.
- `bocpd-can-thiep.json` — điểm đổi của bản đầy đủ, I1, I2; bước nhảy B4.
- `dinh-vi.md` và `dinh-vi.json` — bảng E kèm mức nền.
- `nhan-proxy-va-schema.md` và `.json` — P1, P2.
- `a-so-b.md` và `a-so-b.json` — bảng G.
- `doc-tay.md` — ghi chú đọc tay có trỏ nguồn.
- `scripts/`, `runs/<lượt>/` (manifest, hash đầu vào/đầu ra, thời gian từng bước, lượt hỏng), `features-no-label/`.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-029/`
- EC2 máy một (máy đã chạy BOCPD T-025, key `D:/RCA-ext/keys/key2.pem`): chỉ ghi `~/rca/T-029/`; dùng env và dữ liệu đã kiểm hash của T-025; không đụng thư mục task khác; không bật hay tắt máy; không chép key vào repo. Kết quả chép về `results/T-029/runs/`, kiểm số tệp và hash hai phía.
- `docs/WHY.md`: chỉ nối thêm đúng nguyên văn WHY-39 ở Phụ lục vào cuối file, ở bước 0; không sửa mục cũ. Quyền này chỉ có khi Minh duyệt SPEC kèm văn bản WHY-39.

Không sửa `src/`, `data/`, kết quả của task khác hay `docs/` khác. Python chạy với `-B`.

## Các bước

Mỗi bước ghi rõ cần đầu ra nào của bước nào (SL32). Việc nặng chạy nền, tối đa 3 tiến trình song song.

0. **Mở phiên.** Ghi lời duyệt vào LOG; nối WHY-39; ghi hash `src/p3` (phải giữ nguyên tới cuối); kiểm SHA allowlist. Phụ thuộc: SPEC đã duyệt.
1. **Test tổng hợp cho mọi script tính cờ (V6).** Phụ thuộc: bước 0.
   - Chuỗi có đáp án biết trước: cột đuôi dày (N2), cột NaN đầu đoạn rồi có dữ liệu (B1), bậc thang trong nền (B4), nhiều cột độc lập (N3: r_obs ≈ r_ind).
   - Kiểm bằng: mọi cờ đúng đáp án.
2. **Lượt máy, khởi chạy sớm nhất có thể.** Phụ thuộc: bước 0. 2a–2d chạy trên EC2 máy một; laptop chạy song song bước 3, 4 và 6.
   - 2a. Chạy lại đầy đủ BOCPD một ca có d nhỏ nhất. Kiểm: điểm đổi trùng T-025 (V3). Lệch thì dừng.
   - 2b. I1 trên 30 ca. Trước đó, kiểm trên một ca rằng wrapper hazard 1/50 tái tạo đúng output của `phat_hien.bocpd` khi cùng tiền tố.
   - 2c. I2 trên 30 ca.
   - 2d. I3. Trước đó, kiểm V4 trên một ca có t̂⁺ = 720 (độ trễ 0): RCA phải trùng bản ghi chế độ (a) của phương pháp tất định (BARO, CIRCA) và của TORAI cùng seed. Lệch thì dừng tìm nguyên nhân.
3. **N-Sigma từng cột cho 30 ca × 2 tập cột.** Phụ thuộc: bước 0; chạy song song với bước 2.
   - Kiểm V2: hợp theo cột trùng báo động T-025 ở 60/60 cặp (ca, bộ). Lệch thì dừng.
4. **Đặc trưng không nhãn:** N1–N6, B1, B4, B5, E (phần không cần root).
   - Phụ thuộc: bước 1, 3 và 2a (B1, B4 không cần I1, I2).
   - Lưu `features-no-label/` kèm hash.
5. **Nối nhãn và gán cờ.** B2, B3 khi 2b, 2c xong. E (hạng root), P2, bảng G khi 2d xong.
   - Kiểm V5: tính lại độc lập bằng một bản cài thứ hai, tối giản, trên cả 90 dòng cho N1–N4 và B1, B4.
   - Kiểm V7 (phép thử giả), chỉ cho B1 và B4: tính cùng cờ tại các chỉ số i trong Nv không có báo động và nằm trong miền hợp lệ. Miền hợp lệ áp như nhau cho t̂ và cho điểm đối chứng: B4 theo miền ở mục C; B1 cần [i−2, i+2] ⊂ [s0, 719]. Ngoài miền ghi N/A, không tính là False. Mẫu số V7 là số điểm trong miền, báo theo từng w. N1–N4, B2, B3 ghi V7 N/A, lý do: cờ chứa điều kiện báo động. Tỉ lệ cờ tại t̂ phải được báo cạnh tỉ lệ tại các điểm không báo. Cờ xuất hiện dày như nhau ở cả hai nơi thì ghi "không phân biệt", không dùng làm lời giải thích.
6. **P1 nhãn proxy.** Phụ thuộc: bước 0; chạy song song.
7. **Đọc tay.** Phụ thuộc: bước 5.
   - Mỗi nhóm cơ chế, hoặc tổ hợp cờ, có ít nhất 2 ca nếu có; mọi ca S; mọi ca D0; mọi ca mà V7 cho "không phân biệt".
   - Quy tắc chọn ca ghi trước khi đọc: ca có mã mờ nhỏ nhất trong nhóm, không chọn theo kết quả.
8. **Viết báo cáo.**
   - Kiểm V8: script đối chiếu mọi số trong các file `.md` với JSON nguồn.
   - Ghi LOG mục kết thúc phiên; viết prompt phản biện theo `docs/review-prompt.md`.

## Kiểm đúng đắn

| Mã | Kiểm | Đạt khi |
|---|---|---|
| V1 | SHA allowlist; hash `src/p3` đầu và cuối phiên | Trùng |
| V2 | Hợp cờ từng cột N-Sigma so với `bao-dong.json` | 60/60 cặp trùng tuyệt đối, kể cả t̂ |
| V3 | Chạy lại BOCPD đầy đủ một ca; số cột sau tiền xử lý 30/30 ca | Điểm đổi trùng; số cột trùng `input_shape` |
| V4 | I3 tại t̂⁺ = 720 so với chế độ (a) | Thứ hạng trùng; lệch thì dừng tìm nguyên nhân |
| V5 | Bản cài thứ hai cho cờ | 0 lệch trên 90 dòng |
| V6 | Test tổng hợp có đáp án | Mọi cờ đúng |
| V7 | Phép thử giả tại điểm không báo động | Báo đủ cho B1, B4 trên miền hợp lệ, kèm mẫu số theo từng w; cờ khác ghi N/A kèm lý do |
| V8 | Số trong `.md` so với JSON | 0 lệch |

Không có số công bố cho phát hiện trên RE2-TT cùng giao thức để đối chiếu. Mốc tham khảo duy nhất là phát biểu định tính BARO §4.5 về N-Sigma (`results/T-013/ho-so-nsigma-phat-hien.md:41`).

Không kiểm được trong task, và hệ quả:

- **Hazard trên toàn bản ghi:** ảnh hưởng của hazard lên độ trễ và recall sau mốc cần chạy lại BOCPD 1.441 điểm, khoảng 2,3 giờ máy EC2 (`results/T-025/cham/phan-tich-b.json` → `chi_phi.bocpd.tong_s`). Không chạy. Kết luận B3 chỉ nói cho báo sai trong nền.
- **Thời điểm lỗi thật và nền sạch:** không có nhãn độc lập. B4 không phân biệt nền không sạch với biến động tải. P1 chỉ dựa vào nguồn công bố.
- **Nezha-OB và dataset khác:** không áp dụng. Q-61 chỉ dùng Nezha-OB cho xếp hạng khi biết trước cửa sổ. Kết luận phát hiện chỉ nói cho RE2-TT dev, nền cố định 720 s (Q-69: dữ liệu công khai cho phần phát hiện mỏng).

## Tiêu chí xong

- V1–V8 đạt, hoặc lệch có ghi nguyên nhân và Minh quyết.
- `theo-ca` đủ 90 dòng; mỗi giá trị có nguồn (đường dẫn và con trỏ JSON).
- C1–C6 có câu trả lời trong báo cáo, mỗi câu kèm mức bằng chứng.
- Mỗi dòng HP-n có số ca/tổng theo ô, giải thích khác và lời tác giả (hoặc "chưa thấy").
- Có bảng độ nhạy cho N1, N2, B2, B3, B4 và định vị; mọi đổi chiều được khai.
- I1, I2, I3 đủ 30 ca hoặc có lượt hỏng được giữ và ghi trạng thái.
- LOG có thời gian từng bước, mục kết thúc phiên theo AGENTS mục 7 và prompt phản biện.

## Không làm

- Không đổi tham số hay cấu hình của bộ phát hiện hoặc ranker trong số P3. I1–I3 chỉ là phân tích.
- Không chạy BOCPD 1.441 điểm với hazard mới; V3 chỉ chạy lại một ca với hazard 1/50.
- Không chạy phát hiện trên Nezha-OB, Eadro hay dữ liệu test; không mở `data/locked/`.
- Không định nghĩa nhãn "lan", không kết luận về lan.
- Không tổng hợp gói G2; không đề xuất thiết kế P5/P6 ngoài mã HP-n.
- Không sửa kết quả của T-025, T-024 hay T-028.

## Chi phí ước lượng (chưa kiểm)

Tính từ chi phí T-025 đo trên EC2 máy một, nơi chạy 2a–2d (`results/T-025/cham/phan-tich-b.json` → `chi_phi`).

| Lượt | Cách tính | Ước lượng |
|---|---|---|
| I1, I2 (BOCPD, T = 720) | trung bình 280,6 s/ca ở T = 1.441; tỉ lệ T² → khoảng 70 s/ca | khoảng 35 phút mỗi lượt |
| N-Sigma từng cột | 5,5 + 34,7 s/ca | khoảng 20 phút |
| I3 (2 bộ × 30 ca) | BARO khoảng 8 s, CIRCA khoảng 6 s, TORAI khoảng 17 s × 3 seed mỗi ca | khoảng 70 phút |
| V3, kiểm một ca | 1 ca BOCPD đầy đủ | khoảng 5 phút |

- Tổng khoảng 2,5 giờ trên EC2, cộng khoảng 1 giờ laptop cho N-Sigma từng cột, chạy song song.
- RAM đỉnh mỗi tiến trình dưới 1 GB (BOCPD 321,6 MB ở T = 1.441).
- Đĩa dưới 1 GB: chỉ lưu điểm đổi và m, không lưu R; bảng TORAI xóa sau lượt như T-025.
- Không tải gì. Tổng CPU vượt 1 giờ nên báo theo luật cứng 8; Minh duyệt SPEC là duyệt chi phí này.
- Công agent: một phiên dài. Nếu ngữ cảnh bị nén, ghi checkpoint theo AGENTS §5a. Điểm cắt tự nhiên là sau bước 5.

## Rủi ro và điều chưa chắc

- 30 ca, 10 ô, một hệ, một dataset, phát hiện hồi cứu, nền cố định 720 s. Mẫu hình ở một ô không phải mẫu hình chung.
- Cờ là liên hệ quan sát. Chỉ I1, I2 cho bằng chứng can thiệp, và chỉ về bộ phát hiện, không về hệ thống.
- Ngưỡng N1, N2, B4 và dung sai ±5 s chưa kiểm; độ nhạy khai trước để giới hạn rủi ro này.
- Ánh xạ cột → dịch vụ theo tên có thể sai ở cột dùng chung (ví dụ cơ sở dữ liệu); kiểm bằng universe đã có (SL34).
- Mốc tiêm lấy từ file của dataset; clock tuyệt đối còn OPEN. Nếu mốc lệch, mọi phân nhóm S/E dịch theo.
- V4 có thể lệch vì khác runner giữa T-031 và T-025. Nếu vậy, dừng tìm nguyên nhân trước khi dùng I3.
- Nhóm D0 có thể lớn. Khi đó báo thẳng là chưa giải thích được, không ép vào nhóm.

## Điểm Minh quyết khi duyệt

1. Duyệt SPEC kèm văn bản WHY-39 ở Phụ lục.
2. Duyệt chi phí khoảng 2,5 giờ EC2 máy một và khoảng 1 giờ laptop.
3. Ghi quyết định ngày 08/10 (chọn phương án A cho câu "lan", mở T-029) vào DECISIONS. Việc này đã trình ở chat, chờ duyệt nguyên văn.

## Phụ lục — Nháp WHY-39 (nối vào cuối `docs/WHY.md` khi Minh duyệt SPEC)

```markdown
## WHY-39. Phân tích hạn chế phát hiện chế độ (b) — Đã quyết (Minh duyệt SPEC T-029)

- **Chọn:** phân tích 90 cặp (ca, bộ phát hiện) trên 30 ca dev RE2-TT theo thiết kế khóa trong SPEC T-029: phân loại S/E/Miss; cờ cơ chế N-Sigma N1–N4 và BOCPD B1–B4 kèm độ nhạy; ba can thiệp phân tích (I1 BOCPD trên tiền tố trước mốc, I2 như I1 với hazard 1/250, I3 RCA tại báo động đầu tiên sau mốc); định vị theo báo động đầu sau mốc của từng dịch vụ; kiểm nhãn proxy và schema; bảng chế độ (a) so với (b).
- **Vì sao:** MRP P4 và Q-30 yêu cầu phân tích hạn chế phát hiện như phân tích xếp hạng. T-025 cho thấy báo động đầu thường trước mốc nhưng chưa kiểm cơ chế. Cờ mô tả chỉ cho liên hệ; I1/I2 tách ảnh hưởng của dữ liệu sau mốc qua tiền xử lý, và của hazard, lên báo động trước mốc, vì posterior BOCPD ở i chỉ dùng dữ liệu ≤ i. I3 cho chênh có dấu theo từng ca giữa ba điểm chạy. Phép thử giả tại điểm không báo động ngăn gọi một cờ phổ biến là lời giải thích (áp cho B1, B4).
- **Ngưỡng:** N1 hai lần, N2 10·p0 với p0 = 0,0027, B4 bước nhảy chuẩn hóa MAD ≥ 3 với w = 30 s, đoạn MAD tối thiểu 30 điểm, dung sai điểm đổi ±5 s. Đây là quy ước phân tích, chưa kiểm; độ nhạy khai trước (N1 1,5/3; N2 5/20·p0; B4 2/5 và w 15/60; ±2/±10 s). Hazard 1/250 lấy từ giá trị có trong code tác giả, không chọn theo nhãn.
- **Dùng nhãn:** mốc 720 giống nhau ở mọi ca nên dùng từ đầu; root, loại lỗi, ô nối sau khi đặc trưng đã lưu. I1–I3 dùng mốc để cắt dữ liệu hoặc chọn báo động: là phân tích, không là phương pháp, không thay số P3.
- **Phương án đã xét:** chỉ đếm mô tả từ T-025 (rẻ nhưng không tách được cơ chế); chạy lại BOCPD đầy đủ với hazard mới (tách thêm ảnh hưởng lên độ trễ, nhưng khoảng 2,3 giờ EC2; để sau nếu Minh cần); chỉnh ngưỡng N-Sigma (là tinh chỉnh bộ phát hiện trên dev, không phải phân tích hạn chế); định vị BOCPD bằng bỏ từng cột (d lần chi phí, không chọn).
- **Bằng chứng thiết kế:** giao thức V2 §4, §7, §10; `src/p3/adapters/phat_hien.py`; `results/T-013/ho-so-bocpd.md`, `ho-so-nsigma-phat-hien.md`; `results/T-025/phat-hien.md` §3–§5.
- **Kết luận phụ thuộc:** bản đồ hạn chế phát hiện, phần phát hiện của gói G2 và mọi lựa chọn P6 trỏ về HP-n của T-029. Không áp cho test, Nezha, chế độ online hay nền khác 720 s. Thứ tự báo động đầu sau mốc không phải bằng chứng nhân quả hay nhãn lan.
```
