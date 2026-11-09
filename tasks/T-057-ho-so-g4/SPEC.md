# T-057 — Hồ sơ G4 và báo cáo tiến độ cho cô

- **Trạng thái:** đã duyệt (09/11/2026; Minh: “Duyệt, tạo file”). Codex chưa soát SPEC; prompt soát ở LOG.
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P7 (tổng hợp, phân tích) — **Cổng:** G4, phản biện chéo bắt buộc (MRP §7)

## Mục tiêu

Nguồn trực tiếp:

- MRP §7: sáu câu của cổng; G4 duyệt "kết quả và phân tích; báo cáo tiến độ cho cô".
- MRP §8: khung báo cáo cho cô.
- MRP §3: RQ3a–d và định nghĩa "hoàn thành" (có điều kiện và cơ chế).
- DT18-NV2: vùng ảnh hưởng, phát hiện bất thường, xếp hạng.
- DT18-NV3: "đánh giá bằng các độ đo phù hợp … phân tích các trường hợp phương pháp hoạt động hiệu quả hoặc còn hạn chế".
- Hướng dẫn của cô: bước 2–4 và chuỗi "chỉ ra hạn chế → tiếp cận phương pháp đồ thị". Lời phê "chưa thể hiện rõ liên kết logic" (MRP §2.1, WHY-01).
- MRP §4: báo cáo phải trả lời được vì sao dùng hay không dùng Sock Shop và LEMMA-RCA.

**Loại task.** Tổng hợp, cộng phân tích mô tả trên đầu ra đã lưu. Không thiết kế, không chạy phương pháp trên test.

**Phần mục tiêu được bao phủ.**

- RQ3b và RQ3d: tới mức dữ liệu cho phép.
- RQ3c: chỉ vùng nghi ngờ.
- RQ3a: không, theo Q-245; phải khai rõ.
- RQ4: hoãn vì P8 hoãn (DECISIONS 09/11/2026).
- RQ5: không.

**Đạt task thì đủ căn cứ cho:** Minh quyết G4; gửi báo cáo cho cô; danh sách ứng viên và yêu cầu quan sát chuyển sang FlashTicket. Danh sách này chưa đủ để chọn thiết kế FlashTicket.

Mã H1–H17 dưới đây là các hướng khai thác ở Phụ lục A.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Kết luận cần phân xử; giải thích khác | Bằng chứng phân biệt | Mức kết quả dự kiến | Phần thiếu và hướng xử lý |
|---|---|---|---|---|
| RQ3b: M1 so với baseline mạnh nhất (cô bước 4) | Hơn / không thua / kém. Giải thích khác: chạm trần, ít ô, D1, phiên bản baseline | A4, CI của RE3 (đã có); H5, H10 | TT: đạt E-04 theo công thức nhưng power thấp. OB: chênh dương, chưa phân xử. RE3: thấp hơn M4 theo điểm, CI chứa 0 | Phép phân xử mạnh hơn cần dữ liệu khó hơn (FlashTicket) |
| RQ3d (a): quan hệ có giúp ở OB lỗi mạng không | E2 dùng quan hệ cha–con của span. Giải thích khác: bản sửa D1; nhiễu mẫu nhỏ | Cùng chiều dev↔test; vững khi bỏ 4 ca D1 (H3) | E2: hỗ trợ ở mức mô tả. E1: không ổn định | Phân rã đóng góp: OPEN (H12) |
| RQ3d (b): TT và RE3 không thấy quan hệ thêm gì | Dữ liệu không cần quan hệ, hay thành phần quan hệ kém? | R1 đủ ở 48/60 và 28/30 ca; chạm trần; 12 ca TT R1 sai nhưng C-a0 vẫn đúng (H5, H9) | Dữ liệu công khai không phân xử được hai giải thích | Cần dữ liệu mà quy tắc đơn giản thất bại (P10) |
| RQ3: có khắc phục hạn chế ở RQ2 không | Từng dòng G2 mà M1 nhắm tới | H2: cùng chỉ số đo trên baseline và M1, theo ca | Đã khắc phục / không / không đổi / hại, theo dòng | Dòng không thuộc M1 ghi lý do |
| MRP §2.3: đồ thị phát hiện bất thường ở đâu | E5 tách tự sinh với kế thừa. Giải thích khác: E5 chỉ đổi phần cuối danh sách | H4: số bị hạ, root bị hạ nhầm, ảnh hưởng RR | Mô tả có số | Độ đúng khi hạ thực thể không phải root không đo được (thiếu nhãn); P10 có thể gán nhãn |
| G4-Q6: cơ chế sai chính có thấy trước G3 không | Thấy trên dev nhưng bỏ qua, hay chỉ hiện ở test | H8 trên 22 ca dev OB; TT tùy dữ liệu | Có / không / không đủ dữ liệu | H14 nếu thiếu dữ liệu |
| DT18-NV2: nút và cạnh có kiểu | Cạnh nào thực sự vào phép tính | H6 | Chỉ cạnh gọi service–service trên dữ liệu công khai | Cạnh dữ liệu và thông điệp ở P10 |
| RQ3a, RQ3c | — | H7; vùng nghi ngờ đã có | Chưa trả lời; nêu lý do | Q-245, M-38, M-20; nhãn vùng ở P10 |

## Đầu vào

**Kiểm hash trước khi dùng.** Lệch thì dừng phần phụ thuộc và báo Minh.

- `results/T-054/runs/chuan-bi-main-013-v2/verify_manifest.py --documents`, đối chiếu DECISIONS mục "LESSONS không ghim trong manifest, 08/11/2026".
- `results/T-054/reports/p7a-013-v2/manifest-006.json`
- `results/T-055/manifest-002.json`
- `results/T-056/manifest-003.json`
- manifest của T-052 và T-034

**Báo cáo và đính chính:**

- T-054: `results/T-054/reports/p7a-013-v2/{bao-cao,dinh-chinh-001…004}.md`, `phan-tich-nhom.json` (PT), `results/T-054/reports/main-013-v2/{a4,tables}.json`, `results/T-054/runs/chuan-bi-main-013-v2/activated-001/protocol.json`
- T-055: `results/T-055/reports/re3/{bao-cao-re3,dinh-chinh-001}.md`, `phan-tich-re3.json` (R)
- T-056: `results/T-056/{bao-cao,dinh-chinh-001}.md`, `ket-qua.json` (K), `ket-qua-002.json` (K2)

**Nền thiết kế và dev:**

- `results/T-034/{goi-g2.md,ban-do-g2.json}`
- `results/T-043/bao-cao.md`
- `results/T-040/{bao-cao-p5b,ban-giao-p6}.md`
- `results/T-052/ket-qua-dev.json` (DEV), `results/T-052/ho-so-g3-004.md`
- `results/T-054/runs/sua-cd3-ob-001/nhan/` (22 bản ghi M1 dev OB đủ trung gian)

**Bản nhận RE3:** `D:/RCA-ext/T-055/work-re3-score-v1/...` (ngoài repo, có trên laptop này). Kiểm hash theo biên nhận T-055.

**Quyền đọc dữ liệu.** Chỉ đọc đầu ra đã lưu. Không đọc `data/locked/` và dữ liệu thô của test. H11 chỉ làm khi Minh cấp quyền riêng. Không chạy phương pháp nào.

## Đầu ra

Tất cả nằm trong `results/T-057/`. Mỗi số có đường dẫn và con trỏ JSON.

| File | Nội dung |
|---|---|
| `cau-hien-hanh.{md,json}` | H1: câu đang có hiệu lực, trỏ tới câu gốc và đính chính thay nó |
| `truy-vet-han-che.json` | H2 |
| `dev-test.json` | H3, kèm phép kiểm cấu hình dev trùng bản khóa |
| `e5-thanh-phan.json` | H4 |
| `kha-nang-phan-xu.json` | H5 |
| `do-thi-dt18.json` | H6 |
| `maxz-dev.json` | H8 |
| `ban-do-dieu-kien.json` | H9 |
| `so-cong-bo.json` | H10 |
| `r1-ob.json` | H11, chỉ khi được cấp quyền |
| `ho-so-g4.md` | Sáu câu G4; bảng trạng thái từng RQ; mọi OPEN có giải thích theo review-prompt mục 19; mọi điểm chờ Minh có đề xuất theo mục 20; giới hạn độc lập (C-15 B: v2, D1, C-d3 OB, lệch số worker RE3); ứng viên cho P10 ghi "chưa kiểm" |
| `bao-cao-tien-do-co.md` | Theo thứ tự MRP §8; mỗi phần mở bằng "phần này trả lời nhận xét nào". Ngắn; chương 1–3 tóm tắt và trỏ báo cáo 21/10. Có `.docx` nếu Minh chọn |
| `soat-so.json` | Đối chiếu mọi số trong hai tài liệu với nguồn, yêu cầu 0 lệch |
| `scripts/`, `manifest.json` | Script phân tích và manifest |

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây. Ghi ra ngoài thì dừng, đề xuất.

- `tasks/T-057-ho-so-g4/SPEC.md`, `tasks/T-057-ho-so-g4/LOG.md`
- `results/T-057/**`
- dòng T-057 trong `docs/STATE.md`

Không ghi: `docs/MRP.md`, `docs/WHY.md`, `docs/DECISIONS.md`, `docs/LESSONS.md` (trình riêng), `src/`, thư mục của task khác, `data/`.

## Các bước

Các bước B1–B6 và B9 độc lập với nhau, làm luôn. Nếu cần thì dùng tối đa 2 subagent (dưới ngưỡng luật 8).

| Bước | Việc | Phụ thuộc | Kiểm bằng |
|---|---|---|---|
| B0 | Kiểm hash; ghi dòng mở phiên vào LOG | — | Lệnh verify và sha256 theo manifest |
| B1 | H1 | B0 | Mỗi câu hiện hành trỏ được tới file gốc và đính chính |
| B2 | H6 | B0 | Lệnh đếm nút/cạnh trên `extra/canh` mọi ca |
| B3 | H3; trước hết kiểm cấu hình dev trùng bản khóa | B0 | So `effective_config` dev với protocol khóa |
| B4 | H4 | B0 | Đếm tầng tính lại từ `result.json` khớp PT |
| B5 | H8 | B0 | Bản ghi dev có đủ trường; đếm theo ca |
| B6 | H5, H7 | B0 | Số lấy từ A, PT, K2, WHY-06 |
| B7 | H2 | B1 | Ma trận phủ mọi dòng G2 M1 nhắm tới |
| B8 | H9 | B1 | Báo theo ô; không cộng cờ chồng lấn |
| B9 | H10 | B0 | Tính lại Avg@5 từ `tables.json#/rows` |
| B9b | H11 | Quyền của Minh | Chỉ mô tả |
| B10 | Viết `ho-so-g4.md` | B1–B9 | Tiêu chí xong 1–5 |
| B11 | Viết báo cáo cho cô | B10 | Tiêu chí xong 6 |
| B12 | `soat-so`; tự kiểm; LOG; prompt "Soát kết quả" + khối G4 | B11 | 0 lệch |
| B13 | Codex phản biện G4 (Minh chuyển prompt) | B12 | — |
| B14 | Đáp phản biện; sửa nếu Minh duyệt; Minh quyết G4 | B13 | — |

Mỗi bước ghi file kết quả và một dòng LOG, để tiếp nhận được ngay nếu phiên bị ngắt.

## Kiểm đúng đắn

- `soat-so` cho 0 lệch. Tính lại thử vài số tổng từ các dòng của `tables.json`.
- H3: cấu hình dev lệch bản khóa thì ghi "không so được", không diễn giải.
- H4: thiếu nhãn mức thành phần, nên chỉ báo chính xác phần hạ nhầm root.
- H2, H9: không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Báo theo ô (QT15). Tách nguồn hạn chế theo luật 17.
- Trên test, không thử khóa xếp hạng hay chuẩn hóa thay thế (C-15 B). Mọi phân tích trên test là mô tả sau khi đã xem.
- Nhận định quan trọng tách thành: quan sát, suy luận, ứng viên, câu hỏi mở.

## Tiêu chí xong

1. Hồ sơ G4 trả lời đủ sáu câu, có con trỏ. Ở Q2, mỗi phép so ghi số ô hữu hiệu và nói dữ liệu có phân xử nổi không.
2. Bảng RQ3a–d ghi rõ: đã trả lời, một phần, hay chưa. Mỗi dòng kèm điều kiện, cơ chế, phần thiếu, dữ liệu cần thêm và quyết định phụ thuộc.
3. Ba nhận định chính có bảng giải thích khác, cùng bằng chứng hỗ trợ, bác bỏ hay chưa phân xử:
   - **E2 giúp OB.** Dev và test cùng chiều, vững khi bỏ 4 ca D1: giữ ở mức "mô tả, nhất quán". Ngược chiều: hạ xuống "chỉ thấy trên test".
   - **TT và RE3 không cần quan hệ.** Ghi rõ không phân xử được giữa "dữ liệu đơn giản" và "thành phần kém", kèm dữ liệu cần để phân xử.
   - **Cơ chế max-z.** Ghi rõ đã hiện trên dev, chỉ hiện ở test, hay không đủ dữ liệu.
4. Ma trận H2 phủ mọi dòng G2 mà M1 nhắm tới. Dòng còn lại ghi lý do không thuộc M1.
5. Mọi chỗ "chưa xác định" có giải thích theo review-prompt mục 19. Mọi điểm chờ Minh có đề xuất theo mục 20.
6. Báo cáo cho cô theo khung MRP §8, ghi rõ: P8 hoãn, RQ3a chưa có, các phần sửa theo C-15 B, vì sao dùng hay không dùng Sock Shop và LEMMA-RCA. Số trùng với hồ sơ G4.
7. Codex đã phản biện G4, bảng phản hồi đã điền, LOG có mục kết thúc phiên, dòng STATE đã cập nhật.

Không đòi đồ thị phải thắng. "Không phân xử được, vì sao, cần gì" là kết quả hợp lệ.

## Không làm

| Phần không làm | Hệ quả |
|---|---|
| RQ3a: P/R/F1 phát hiện (Q-245) | "Phát hiện dấu hiệu bất thường" của DT18 chỉ có bằng chứng mức thành phần. Mức hệ thống chuyển P10 bằng luật Grafana; hỏi cô theo M-20 |
| RQ3c: P/R/F1 vùng | Không có nhãn vùng; chuyển P10 |
| RQ4 (P8) | Hoãn |
| RQ5 | Thuộc P10 |
| H12, H13, H16, H17 | Giữ OPEN (Phụ lục A, nhóm D) |
| Ứng viên sửa M1: khóa độ rộng, xử lý IQR = 0, kênh lỗi theo cạnh | Chưa kiểm. Thiết kế trên dev FlashTicket, kiểm độc lập trên lượt FlashTicket mới |
| H14, H15 | Đề xuất tách (Phụ lục A, nhóm C) |
| Bộ đọc FlashTicket | Thuộc T-058 |

## Chi phí ước lượng

- Khoảng 3 ngày làm việc của agent.
- Chỉ laptop; mỗi script đọc dưới 10 phút. Không dùng EC2 (luật 19): đọc file đã có trên laptop, chuyển lên EC2 chỉ thêm thời gian.
- Không tải dữ liệu. Không lượt chạy nào trên 1 giờ; luật 21 không áp dụng.

## Mốc và checkpoint

| Ngày | Việc |
|---|---|
| 09–10/11 | B0–B6, checkpoint LOG |
| 11/11 | B7–B9 (và B9b nếu có quyền) |
| 12/11 | B10–B12; prompt cho Codex |
| 13/11 | Codex phản biện G4 |
| 14/11 | Đáp phản biện; Minh quyết G4; xuất bản gửi cô |

Dự phòng 15/11 cho lượt phản biện thứ hai. T-058 chạy song song; hai task không đụng file chung, trừ STATE, mỗi task chỉ sửa dòng của mình.

## Rủi ro và điều chưa chắc

- Cấu hình dev ở H3 có thể không trùng bản khóa. **Chưa kiểm.**
- Bản ghi dev TT có thể thiếu độ rộng kênh; khi đó H8 chỉ làm được phần OB.
- File T-055 và T-056 chưa commit; kiểm hash theo manifest trước khi dùng.
- Bản nhận RE3 nằm ngoài repo.
- Báo cáo cho cô có thể quá dài; thư 21/10 đã xin lỗi về độ dài.

## Prompt bàn giao

Ở `LOG.md`, theo AGENTS §7 và §9.

---

## Phụ lục A — Hướng khai thác, xếp theo giá trị trên chi phí (rà ngày 09/11/2026)

Nguồn: PT, R, K, K2, DEV như mục Đầu vào. Mọi phân tích trên test là mô tả sau khi đã xem (C-15 B).

### Nhóm A — đưa vào T-057

| Mã | Hướng | Quan sát dẫn tới | Câu hỏi và giá trị | Chi phí |
|---|---|---|---|---|
| H1 | Bảng câu hiện hành gộp đính chính; soát số bằng máy | 6 file đính chính (T-054 Đ1–Đ15, T-055 Đ1–Đ5, T-056 D1–D10); §7.3 P7 bị thay ba lần; Codex chưa kiểm T-054 đính chính 004 và T-056 D6–D10 | G4-Q4; tránh trích câu đã bị thay | ~0,5 ngày |
| H2 | Ma trận hạn chế P4 → thành phần M1 → kết quả theo ca | G2 có 26 dòng (`results/T-034/goi-g2.md` §3.1); M1 nhắm G2-H03, H06, H17 qua UV-1, UV-2 (`results/T-043/bao-cao.md` §7); OB network_delay M1 0,900, C-a0 0,408, M4 0,380 (`PT#/tach_MRR/Nezha-OB|fault/network_delay`); TORAI B đặt bên gọi trực tiếp đầu 15/30 ca RE3 (`K#/2_4_baro_torai_RE3/torai_top_vs_root`); IQR = 0 lặp ở M1 (T-055 Đ1a) | RQ3 theo câu chữ; "liên kết logic" cô phê thiếu | ~1 ngày |
| H3 | Ổn định dev → test của thành phần | TT dev M1 0,928 < C-a0 0,983, test bằng nhau; OB E2 dev 0,873−0,721, test +0,115; OB E1 dev 0, test +0,130; OB E5 dev +0,067, test 0; OB C-d2 dev 0,899 > M1 0,873 (`DEV#/worlds/P/<bộ>/summary/<vế>/MRR/phan_so`) | G4-Q2, Q5, Q6; bài học cho thiết kế FlashTicket | 2–3 giờ |
| H4 | Đo E5 như lớp phát hiện mức thành phần | TT Σ tầng 1 = 1342 trên 60 ca, tầng 2 = 273 ở 59/60 ca; OB Σ tầng 1 = 125, tầng 2 = 21 ở 14/34; root bị hạ: TT 0/60, OB 1/34, RE3 1/30; root có kênh bị giải thích TT 28/60, OB 10/34 (`PT#/E5_tac_dung_M1`, `PT#/trung_gian_theo_ca/*/M1`) | "Đồ thị phát hiện bất thường ở đâu" (MRP §2.3) | 2–4 giờ |
| H5 | Sức phân xử của dữ liệu (tổng hợp) | Power E-04 ~0,19 (WHY-06); OB 3 ô hữu hiệu, p nhỏ nhất 1/8; Hit@5 chạm trần; R1 đúng 48/60 TT, 28/30 RE3 (`K2#/tom_tat/<bộ>/root_events_hon_moi_service_khac`) | G4-Q2; câu xin cô về dữ liệu khó hơn | 1–2 giờ |
| H6 | Đồ thị thực dùng so với DT18 | Cạnh quan sát M1 trên P7 chỉ service–service (TT 26 nút, OB 10 nút); cạnh dữ liệu/thông điệp chỉ có ở mô hình tĩnh (`results/T-040/bao-cao-p5b.md:46`, `ban-giao-p6.md:19`) | DT18-NV2; câu hội đồng dễ hỏi | ~1 giờ |
| H7 | RQ3a và phát hiện mức hệ thống (tổng hợp) | M1 trả `CAUSE_FOUND` 58/58 ở t−300 (`PT#/ce_tom_tat`); Q-245; P3 chỉ có số phát hiện của baseline (G2 §2.5) | DT18 "phát hiện dấu hiệu bất thường"; câu hỏi cô M-20 | ~1 giờ |
| H8 | Cơ chế max-z kênh hẹp có trên dev không (chỉ đọc) | Giải thích 6/10 ca sai P7 (§7.5), 2/4 ca sai RE3 (T-055 Đ1b); giúp root 30/57 ca đúng TT; 22 bản ghi dev OB có `don_vi_phan_vi`, `kenh_co`; dev TT chưa biết | G4-Q6; nền cho thiết kế sửa ở FlashTicket | <1 giờ (OB) |
| H9 | Bản đồ điều kiện liên bộ (124 ca test) | M1 sai 14/124 (TT 3, OB 7, RE3 4); R1 đúng 6/7 ca M1 sai thuộc TT+RE3; 12 ca TT chỉ M1 đúng đều loss/delay và C-a0 cũng đúng 12/12 (T-056 D1) | DT18-NV3; giả thuyết chuyển sang FlashTicket | ~0,5 ngày |
| H10 | Đối chiếu số công bố; đủ độ đo MRP | `tables.json#/rows/*/metrics/avg@5` có nhưng báo cáo P7 chưa báo; SimpleRCA công bố top-1 0,80 trên RE2-TT (`docs/LESSONS.md:10`, ST9–ST10; chưa đối chiếu bản in), M4 của ta Hit@1 0,800 trên 60 ca test (khác tập ca) | G4-Q3 | 1–2 giờ |

Rủi ro C-15 B của nhóm A: không đổi thiết kế. Riêng H8: cơ chế phát hiện trên test, nên mọi bản sửa thiết kế trên dev và kiểm độc lập trên lượt FlashTicket mới.

### Nhóm B — cần Minh cấp quyền

- **H11. R1 trên OB test.** Đóng câu OPEN "OB có đơn giản không" (T-056 D2). Phải đọc lại metric thô OB test trên laptop (đính chính 004 ghi cần Minh duyệt). 2–3 giờ, chỉ mô tả. Mặt trái: thêm tiếp xúc test đã mở toàn bộ.

### Nhóm C — đề xuất tách

- **H14. Chạy lại M1 trên 30 ca dev TT với đủ trung gian**, chỉ khi H8 thấy thiếu dữ liệu. 0,5–1,5 giờ EC2. Tách sang task chuẩn bị thiết kế FlashTicket.
- **H15. Thời gian và tài nguyên chạy M1 mỗi ca.** Tách sang T-058 (đo trên luồng FlashTicket thật).

### Nhóm D — bỏ, giữ OPEN có giải thích

| Mã | Hướng | Vì sao bỏ | Mặt trái |
|---|---|---|---|
| H12 | Phân rã E1/E2/E5 trên OB | Thiếu vế; phải chạy cấu hình mới trên test; đã quyết để OPEN (DECISIONS 08/11, mục 3) | Câu đóng góp riêng còn mở; chỉ trả lời trên dev hoặc FlashTicket |
| H13 | TORAI A (174 slot) | Minh hoãn vô thời hạn | Baseline mạnh nhất TT là bản nguồn B do ta dựng (G2-H14); G4 khai giới hạn |
| H16 | Trung gian nội bộ TORAI B ở auth/loss | Cơ chế baseline; không đổi kết luận cuối | Một câu "vì sao" của baseline còn mở |
| H17 | Định vị vật lý trễ E2-C, cờ operation bên được gọi | Phải đọc lại span server của test; chỉ phục vụ mô tả C-d3 | Cần instrumentation hai đầu cạnh trên FlashTicket |
