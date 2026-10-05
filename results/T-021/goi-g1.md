# Gói G1: phương pháp, dataset, cách chia (T-021)

Ngày 05/10/2026. Người làm: Claude. Người phản biện: Codex. Mọi số có đường dẫn tới file kết quả; đường dẫn `runs/…`, `chia-theo-o/…` và các CSV không ghi thư mục là thuộc `results/T-021/`. Chi tiết nằm trong các CSV; văn bản này chỉ trích phần cần quyết.

## 0. Tóm tắt cho Minh

**Minh cần duyệt ba thứ** (MRP §7, G1): danh sách phương pháp, gói dataset, cách chia dev/test. Thêm 7 câu hỏi ở mục 6.

**Đề xuất (gói A):**

| Bộ | Vai trò | Ô / ca | Vì sao cần |
|---|---|---|---|
| RE2-TT | dev 10 ô / 30 ca (TX2); test 20 ô / 60 ca (TX1) | 30 / 90 | Trên Train Ticket, là bộ duy nhất vừa có 3 lần lặp mỗi ô, đủ ba tín hiệu, lỗi tài nguyên và mạng, vừa còn ca chưa chạy phương pháp; có số công bố để kiểm tái lập |
| Eadro-TT | chia theo ô | 81 / 81 | 27 root; độc lập với RCAEval. Nhóm vị trí (5 nhóm, 27 ô root không có trong trace) tính trên trace export toàn file, mà thẻ T-009 cảnh báo không phản ánh chắc cấu trúc gọi (mục 5) |
| Nezha-OB | chia theo ô | 33 / 56 | Có lỗi mã nguồn (return, exception); log có trace_id; hệ thứ hai; độc lập |
| RE3-OB | giữ ngoài, nguyên bộ | 10 / 30 | TX0 (không thấy nguồn tiếp xúc); lỗi mã nguồn; 138 MB. Cùng hệ OB với Nezha-OB và cùng bộ công cụ với RE2-TT ở dev (mục 5) |

Phiên bản chia đề xuất: **phân tầng theo loại lỗi** (mục 4). Số ô, số ca: `runs/chia-003/bao-cao-chia.json`.

**Điều sẽ làm đề xuất đổi:**
- Minh không chấp nhận việc ca liền kề trong cùng phiên nằm hai phía (câu hỏi 1). Khi đó đơn vị chia của Eadro, Nezha phải đổi.
- Đầu P3 không ghép được trace Eadro với mốc tiêm (thẻ ghi timestamp trace lệch biểu kiến, `results/T-009/the-dataset.md:95`). Khi đó Eadro-TT chỉ phục vụ phương pháp metric/log và câu hỏi vị trí.
- Đầu P3 thấy trace Eadro không đại diện cấu trúc gọi của phiên (trace có timestamp lịch sử; bậc 0 không được hiểu là cô lập, `results/T-009/the-dataset.md:95,282`). Khi đó lý do "nhiều nhóm vị trí" của Eadro-TT mất, và gói thiếu dữ liệu vị trí ngoài 5 root của RE2-TT.
- Tác giả Nezha hoặc Eadro phản đối (Q-59). Khi đó gói mất bộ độc lập và mất phần lớn số root.

**Dữ liệu không phân xử nổi:**
- RQ3c: không bộ công khai nào có nhãn vùng ảnh hưởng. Chỉ báo được "vùng nghi ngờ có chứa root không".
- RQ3a ở chế độ tự phát hiện (b): mốc tiêm lộ qua biên file ở RE2-TT, và qua đầu phiên ở Eadro (lần tiêm đầu cách đầu phiên 2,5–4,2 s, `runs/kiem-phien-001/ket-qua.json`). Ở Nezha, trace/log chỉ có file của phút tiêm và 2 phút sau, không có file giữa hai lần tiêm (`results/T-008/the-dataset.md:72-80`): dữ liệu bị chọn theo nhãn khi thu. Trace/log Nezha chỉ dùng được cho ranking biết trước cửa sổ, không cho phát hiện liên tục; metric theo ngày là nguồn riêng, dữ liệu bình thường và đồng hồ còn OPEN.
- Hub ở Eadro, Nezha để OPEN (chỉ lưu bậc của root; S8 (i)).
- Lỗi mã nguồn trong phần chia chỉ có 8 ô / 14 ca (Nezha-OB). Kết luận theo loại lỗi mã nguồn sẽ yếu.

**Phát hiện lệch so với T-020** (đã kiểm trên file gốc):
- RE2-TT: 60 ca khóa là TX1, không phải TX0 (đúng R1 của REVIEW T-020).
- RE1-OB: TX2 cả 125 ca, không phải TX0. T-006 đã chạy `main.py` (BARO, N-Sigma, RCD) trên bản Zenodo của RE1-OB (`results/T-006/runs/kiem-chay-fse-baro-main-re1-ob.tar.gz`, 125 file kết quả; `results/T-006/kiem-dung-dan.md:60-66`). Bản HF chưa đối chiếu byte, nên ghi TX2 cho chắc. Đối chiếu đầy đủ: `runs/census-002/doi-chieu-T020.csv`.
- Eadro không có dữ liệu bình thường trước lần tiêm trong cùng phiên: giữa hai lần tiêm chỉ nghỉ 114–124 s (TT), 33–43 s (SN).

## 1. Sáu câu của cổng

1. **Phục vụ câu nào của cô/DT18?** Nhận xét "mở rộng thực nghiệm ra các dataset public khác" và "hiểu các phương pháp đã có"; DT18 NV3 (thực nghiệm trên dữ liệu công khai trước). Bảng nhu cầu RQ1–RQ4: LOG T-021 phiên 2, bước 1.
2. **Dữ liệu có phân xử nổi không?** Có cho RQ1 theo dataset, loại lỗi tài nguyên/mạng và vị trí (trừ hub ở hai bộ). Yếu cho lỗi mã nguồn. Không cho RQ3c. Một phần cho RQ3a chế độ (b). Mục 5.
3. **Baseline đủ mạnh chưa?** Danh sách theo Q-37/Q-38, có SimpleRCA (baseline không đồ thị đã công bố mạnh trên RE2-TT, chưa đối chiếu bản in). Chưa có đại diện họ học có giám sát. CIRCA-PC và BOCPD trên Train Ticket vượt ngân sách Q-40 theo số đã đo (mục 2).
4. **Giá trị trung gian hợp lý không?** Census tính lại khớp sổ T-020 về ca và ô ở 15/15 bộ; lệch TX ở 2 bộ, đã giải thích ở trên. Nezha đổi nhóm vị trí giữa hai giả thuyết đồng hồ ở 24/101 sự kiện (`runs/vi-tri-001/tom-tat.json`).
5. **Đã tách theo điều kiện và theo ca chưa?** Vị trí tính theo ca rồi gộp lên ô (`runs/vi-tri-001/vi-tri-theo-ca.csv`, `vi-tri-theo-o.csv`); phủ tách theo phía (`runs/chia-003/bao-cao-chia.json`, mục `phu_theo_phia`).
6. **Còn lựa chọn nào chưa có "tại sao"?** Có: đơn vị chia ở bộ nhiều lần tiêm mỗi phiên; cửa sổ; cách dùng mốc tiêm ở chế độ (a); xử lý CIRCA-PC, BOCPD so với Q-40. Đều nằm ở mục 6.

## 2. Phương pháp

Giữ Q-37/Q-38. Bảng dưới chỉ ghi vai trò ở P3.

| Phương pháp | Bản dùng làm baseline so sánh | Bản chỉ để tái lập |
|---|---|---|
| BARO | RCAEval `259ea41` | — |
| SimpleRCA | cài theo bài (M4, T-017) | — |
| CIRCA | PC (RCAEval) và đồ thị kiến trúc (`src/circa_kien_truc/`) | — |
| MicroRank | MicroRank-RCAEval sửa đầu vào (T-015) | bản RCAEval nguyên trạng (T-007: xếp gần theo lưu lượng, `results/T-007/kiem-dung-dan.md:23`) |
| TORAI | bản sửa hai chỗ (WHY-19) | bản gốc RCAEval |
| N-Sigma, RCD | biến thể đối chứng | — |
| TraceRCA | biến thể đối chứng: bản lọc giá trị hữu hạn trước khi sắp (CANDIDATE, `results/T-015/ho-so-microrank.md:281`) | bản RCAEval nguyên trạng (sắp trước khi bỏ NaN: 79/90 ca có cặp điểm sai thứ tự, `results/T-015/runs/tracerca-audit/seed0/t007-audit.json`) |
| BOCPD, N-Sigma, GDN | bộ phát hiện, bảng riêng (Q-30) | — |

**Còn mở, phải quyết trước khi chạy P3** (đều là CANDIDATE, chưa có WHY):

| Lựa chọn | Nháp có sẵn |
|---|---|
| Scorer CIRCA cho hai nguồn đồ thị (RHT-only hay RHT+DA); giữ metric cô lập | `results/T-014/de-xuat-tai-lieu-chung.md:21-49` |
| MicroRank: full-score, ánh xạ service | `results/T-015/de-xuat-tai-lieu-chung.md:29` |
| TraceRCA: lọc hữu hạn trước khi sắp, tie, trạng thái không bất thường | `results/T-015/de-xuat-tai-lieu-chung.md:32-44` |

**Nối WHY:** WHY-04 giữ phần "chia theo ô, có bộ giữ ngoài"; cần sửa thêm phần đơn vị chia nếu Minh chọn ở câu hỏi 1. WHY-05 giữ; các chỗ đổi giao thức (cửa sổ, nguồn dữ liệu bình thường của Eadro) ghi WHY riêng khi chốt. WHY-16 giữ nguyên nghĩa: cấu hình tái lập bảng của bài TORAI, không phải cửa sổ P3. WHY-19 giữ. WHY-20 giữ; số seed của RCD trên Train Ticket bị Q-40 giới hạn ở 2 (xem dưới).

**Cặp vượt ngân sách Q-40 (3 giờ cho toàn bộ ca của một dataset).** Phép chiếu **chưa kiểm**: nhân thời gian một ca với số ca, giả định cùng máy, cùng cửa sổ, cùng số cột. Sai nếu thời gian phụ thuộc mạnh vào ca.

| Phương pháp | Số đo một ca (Train Ticket) | Chiếu 90 ca RE2-TT | Nguồn |
|---|---|---|---|
| CIRCA-PC | 1.796 s (EC2, 600 × 273) | ≈ 45 giờ | `results/T-014/ho-so-circa-pc.md:133` |
| BOCPD (600 điểm, 76 cột) | 1.440 s | ≈ 36 giờ | `results/T-005/do-kha-thi.md` mục 2b |
| MicroRank, toàn ca | 238 s (cửa sổ 10 phút: 101 s) | ≈ 6 giờ (2,5 giờ) | `results/T-005/do-kha-thi.md` mục 2a |
| RCD | 49 s (EC2), 1 seed | ≈ 74 phút/seed; 3 seed ≈ 3,7 giờ | `results/T-016/quy-mo-tt.md:44-48` |

Eadro-TT, Nezha-OB chưa đo thời gian. Phương án cho CIRCA-PC và BOCPD ở câu hỏi 5.

## 3. Dataset

**3.1 Nhu cầu → bộ phủ** (mã N theo bảng bước 1 trong LOG):

| Nhu cầu | Bộ phủ (gói A) | Không phủ / giới hạn |
|---|---|---|
| N1 nhãn root + thời điểm; tín hiệu đủ cho phương pháp | cả 4 bộ | trace Eadro ghép thời gian OPEN |
| N2 nhiều hệ/bộ | TT (RE2, Eadro), OB (Nezha, RE3) | không có hệ ngoài TT/OB trong phần chia |
| N3 tài nguyên, mạng, mã nguồn | tài nguyên, mạng: 3 bộ; mã nguồn: Nezha-OB, RE3-OB | mã nguồn chỉ 8 ô trong phần chia |
| N4 nhiều root, nhiều vị trí | Eadro-TT 27 root; Nezha-OB 10; RE2-TT 5 | hub OPEN ở Eadro, Nezha |
| N5 dữ liệu bình thường; nhãn thời gian | RE2-TT 720 s trước tiêm (`results/T-002/the-rcaeval.md:40`); Eadro phiên no-fault riêng | Nezha: trace/log `rca_data` không có file trước phút tiêm (`results/T-008/the-dataset.md:72-80`); có trace construct riêng khoảng 1 phút/ngày ở OB (`results/T-008/the-dataset.md:56-61`), độ sạch và đủ học ngưỡng: OPEN; metric ngày: bình thường, đồng hồ OPEN (`results/T-008/the-dataset.md:22`); mọi nhãn là lúc tiêm, không phải onset |
| N6 dev có đủ loại lỗi, có root không cạnh, có lan | dev có cả ba nhóm lỗi; Eadro-TT dev: 11 ca root không có trong trace, 1 ca bậc 0; RE2-TT dev: 6 ca bậc 0 (ts-auth-service) (`chia-theo-o/A-phan-tang.csv`); nhóm của Eadro mang cảnh báo ở mục 5 | lan: chỉ ước lượng thô (thẻ T-002, T-008, T-009 mục 6) |
| N7 test không TX2; ≥1 giữ ngoài TX0 | đạt (assert `runs/chia-003`) | test có TX1, có ca đã dò triệu chứng (Q-60(a)) |
| N8 nhãn vùng | — | không có (giới hạn) |
| N9 cấu trúc đồ thị thật; biết kiến trúc | RE2-TT, Eadro-TT, Nezha-OB có trace; TT, OB có kiến trúc công bố | — |
| N10 cạnh có kiểu; log nối trace | Nezha-OB (log có trace_id); RE2-TT nối theo service + thời gian | span kind/thuộc tính chưa kiểm cho mọi bộ |
| N11 log cho LLM | cả 3 bộ chia | — |
| N12 bộ độc lập | Eadro, Nezha (`doc-lap.csv`) | trục công cụ tiêm CPU/mạng của Nezha OPEN |
| N14 baseline trên bộ giữ ngoài | RE3-OB cùng schema RE2 theo metadata | chưa kiểm trên file (mục 4) |
| N15 tái lập số công bố | RE2-TT (SimpleRCA; RCAEval) | — |
| N16 Q-40 | xem mục 2 | CIRCA-PC, BOCPD vượt |

**3.2 Điều kiện tối thiểu (Q-58 lớp 1).** Bảng đủ: `dieu-kien-toi-thieu.csv` (28 dòng, có nguồn). Bốn bộ đề xuất đều đạt; hai chỗ OPEN: trace Eadro ghép thời gian, schema RE3-OB (chưa tải).

**3.3 Vì sao chọn bộ RCAEval (Q-31).** RE2-TT: trên Train Ticket, là bộ duy nhất vừa có 3 lần lặp mỗi ô với đủ ba tín hiệu và lỗi tài nguyên, mạng, vừa còn 60 ca chưa chạy phương pháp; có số công bố để kiểm tái lập. Eadro-TT không lặp; Nezha-TT có đồng hồ OPEN; RE3-TT chỉ có lỗi mã nguồn, 2 root; RE2-OB đã TX2 toàn bộ. RE3-OB: là ứng viên giữ ngoài TX0 duy nhất có trace và lỗi mã nguồn mà không phải tải lớn. Bank cũng TX0 nhưng không có lỗi mã nguồn và cần tải 2,83 GB (`results/T-012/the-dataset.md:493`). "Đã có sẵn trên máy" không được tính.

**3.4 Sock Shop và LEMMA-RCA** (cô đã nêu tên):
- **Sock Shop:** không dùng trong gói chính. RE1/RE2/RE3-SS không có file trace ở toàn release (`results/T-019/the-sock-shop.md:35`), chỉ 3–5 root, và RE2-SS, phần lớn RE1-SS đã TX2 (`tiep-xuc.csv`). Có thể dùng có chủ đích làm kịch bản "đồ thị từ kiến trúc" (MRP §4 tiêu chí 3); đó là phương án lớn hơn, chưa đề xuất.
- **LEMMA-RCA:** không dùng. Mẫu đã kiểm không có trace; nhãn root chỉ là một entity mỗi ngày mẫu; giấy phép NC/ND còn mâu thuẫn; bản gốc 53 GB và 33 GB (`results/T-011/the-dataset.md:13-27`).

**3.5 Đã xét, không dùng** (mỗi bộ một lý do; đủ trong `dieu-kien-toi-thieu.csv`):

| Bộ | Lý do |
|---|---|
| RE2-OB (90 ca TX2), RE2-SS (90 TX2), RE1-OB (125 TX2), RE1-SS (100 TX2 + 25 TX1) | đã chạy phương pháp trên toàn bộ hoặc phần lớn: chỉ làm dev hoặc tái lập; không thêm nhu cầu nào gói A chưa phủ (`tiep-xuc.csv`) |
| BARO-FSE-OB | chỉ metric; TX2; chỉ để tái lập (`results/T-006/kiem-dung-dan.md:60-66`) |
| RE1-TT | chỉ có metric; cùng hệ TT với RE2-TT |
| RE3-TT | 2 root, 8 ô; nằm trong phương án B |
| RE3-SS | không trace; TX1 |
| Eadro-SN, Nezha-TT | nằm trong phương án B; Nezha-TT đồng hồ OPEN |
| DeepTraLog | không có nhãn root service, không có mốc tiêm |
| AnoMod, LO2 | không có nhãn root theo sự cố |
| FSE-2026 bản rút gọn | 8 ca hợp lệ, nhiều ca nhiều root |
| TRCA | trùng byte với Nezha |
| OpenRCA-Bank | TX0, khác hệ; không lỗi mã nguồn; tải 2,83 GB; phương án B dùng làm giữ ngoài thứ hai |
| OpenRCA Telecom, Market | chưa census; dữ liệu gốc AIOps, độc lập OPEN |
| OpenRCA 2.0 | chưa có bản công khai ghim |
| TrainTicketTrace | nhãn root/thời điểm OPEN, chưa tải |
| FAMOS TrainTicket | chưa kiểm trên file; census, nhãn OPEN (`results/T-012/final-leads.md:9`) |
| GAIA/MicroSS | chưa đưa vào gói vì **chưa kiểm trên file**, không vì lý do khoa học. Theo README (`docs/knowledge/K3-dataset-ung-vien.md:154-166`): trace liên tục hai tuần có parent_id, hệ MicroSS, bản ghi tiêm có thời điểm và thời lượng, độc lập theo README. Có thể bù N2 (hệ ngoài TT/OB), N5 (dữ liệu bình thường liên tục cho phát hiện, chỗ Nezha thiếu) và N12. Lỗi chỉ CPU, bộ nhớ không làm mất giá trị bổ sung vì loại lỗi xét ở lớp gói (Q-58). Câu hỏi 7 |
| DejaVu | chưa kiểm trên file; không có trace span theo README |
| Dữ liệu của TraceRCA | chưa kiểm trên file; README không mô tả nội dung (`docs/knowledge/K3-dataset-ung-vien.md:215`) |
| Dữ liệu mẫu của MicroRCA | chỉ là ví dụ trong repo; thời gian phản hồi giữa service và tài nguyên, không có trace span (`docs/knowledge/K3-dataset-ung-vien.md:216`) |

**3.6 Phương án để so.**
- **B (lớn hơn):** A + Eadro-SN, Nezha-TT, RE3-TT (chia) + Bank (giữ ngoài thứ hai). Được: hệ thứ ba (SN); lỗi mã nguồn trên TT; dev có 35 ca mã nguồn thay vì 7 (phân tầng). Mất: thêm ba adapter và hai bộ cần ghép đồng hồ; thời gian P3 tăng; Bank cần tải. Số: `runs/chia-003/bao-cao-chia.json`.
- **C (nhỏ hơn):** RE2-TT + Eadro-TT + RE3-OB. Mất lỗi mã nguồn ở dev, nên không kiểm được giả thuyết 2 của P4 trên dev. Không đề xuất.
- **Lập luận mạnh nhất chống A:** lỗi mã nguồn trong phần chia quá ít (8 ô), nên câu "phương pháp thất bại với lỗi mã nguồn" ở P4 dựa trên 3–4 ô dev. B sửa được điểm này với giá thêm hai bộ.

## 4. Cách chia

**Quy tắc.** Chia toàn ô, seed 20261004, thứ tự ô theo SHA-256 như T-020 (`scripts/chia.py`). Ô có ca TX2 ép vào dev. RE2-TT giữ 10 ô dev của v1. Bộ giữ ngoài nguyên bộ, toàn TX0. Assert đạt cả bốn bản (`runs/chia-004.stdout.txt`; chia-004 chỉ sửa cách báo phủ vị trí, bốn CSV chia giống byte với chia-003).

**Tỷ lệ 1/3 dev.** Không có nguồn nói tỷ lệ này đến từ v1. Lý do đề xuất: giữ khoảng 2/3 ô cho test để khoảng tin cậy bootstrap theo ô có đủ đơn vị, và vẫn để dev đủ ô cho P4. Chưa kiểm phương án khác.

**Hai phiên bản, gói A:**

| Phiên bản | Dev ô / ca | Test ô / ca | Giữ ngoài | Ca mã nguồn dev / test |
|---|---|---|---|---|
| Tỷ lệ như T-020 | 48 / 75 | 96 / 152 | 10 / 30 | 5 / 9 |
| Phân tầng theo loại lỗi | 50 / 79 | 94 / 148 | 10 / 30 | 7 / 7 |

Ở gói A, cả hai bản đều có mọi loại lỗi và mọi nhóm vị trí ở cả hai phía (`runs/chia-004/bao-cao-chia.json`, mục `vang_mot_phia`; nhóm vị trí test RE2-TT suy theo root, chưa kiểm, đếm ở trường riêng). Ở gói B, bản tỷ lệ để f3, f4 của RE3-TT chỉ ở test và f2 chỉ ở dev; bản phân tầng không còn lỗi này. Vì vậy đề xuất **phân tầng**. Việc đổi này chỉ dùng census nhãn công khai, chưa ai thấy kết quả test.

**Ô một lần lặp.** Eadro-TT: 81/81 ô. Nezha-OB: 10/33 ô. Khoảng tin cậy ở hai bộ này lấy mẫu theo ô, nhưng mỗi ô chỉ một ca, nên không tách được dao động giữa lần lặp với khác biệt giữa ô.

**Mức tiếp xúc** (`tiep-xuc.csv`): RE3-OB ghi TX0 vì không thấy nguồn tiếp xúc trong ba nhóm nguồn; đó là vắng bằng chứng tiếp xúc, không phải bằng chứng đã kiểm là chưa ai mở. Ngoài ra, test có TX1 ở cả ba bộ chia; Eadro, Nezha có ca đã dò triệu chứng theo từng ca gắn nhãn root (137 ca ở gói A). Phải khai báo khi báo kết quả (Q-60(a)).

**Ca liền kề khác phía.** Eadro, Nezha có nhiều lần tiêm trong một file. Chia theo ô làm 29 cặp ca liền kề ở Eadro-TT và 30 cặp ở Nezha-OB nằm hai phía (bản phân tầng). Ở Eadro-TT hai lần tiêm chỉ cách nhau 114–124 s. Mở dữ liệu một ca dev ở P4 có thể thấy đoạn đầu của một ca test. Câu hỏi 1.

**Cách dùng nhãn (MRP §4).**
- Nhãn để học: không phương pháp nào trong Q-38 học từ nhãn root. GDN học từ đoạn bình thường; đoạn đó được cắt bằng mốc tiêm (dev) hoặc lấy từ phiên no-fault (Eadro).
- Nhãn dev để chọn cấu hình: root và loại lỗi của ca dev; chỉ dùng ở P3, P4, P6.
- Nhãn chỉ để chấm: root, loại lỗi của test và giữ ngoài.
- Mốc tiêm là nhãn nhưng chế độ (a) của P3 dùng nó làm đầu vào. MRP §4 nói "nhãn test chỉ để chấm". Câu hỏi 4.

**Baseline trên bộ giữ ngoài RE3-OB** (theo metadata công bố, **chưa kiểm trên file**): metadata có metric, trace, log cho 30 ca (`results/T-002/the-rcaeval.md:449-457`). Dự kiến chạy được mọi phương pháp Q-38 với cùng đầu vào như RE2, không cần nhãn root nào. GDN cần đoạn bình thường trước tiêm; bài mô tả 10 phút, chưa kiểm. Không có phương pháp có giám sát, nên không có vấn đề chuyển tập service giữa hai hệ.

## 5. Giới hạn của kết luận (phần gói không phủ)

- Không có nhãn vùng ảnh hưởng: RQ3c chỉ đo trên FlashTicket.
- Mọi nhãn thời gian là lúc tiêm, không phải lúc bắt đầu biểu hiện; độ trễ phát hiện tính từ lúc tiêm.
- Vị trí: RE2-TT dùng đồ thị trước tiêm của từng ca dev; 60 ca test suy theo root (chưa kiểm). Eadro dùng đồ thị toàn file (có cả đoạn tiêm); Nezha dùng cửa sổ ±60 s quanh lúc tiêm. Hub ở Eadro, Nezha OPEN. Kết luận theo vị trí mang các lệch này (`vi-tri-root.csv`).
- Eadro-TT: 27/81 ô có root không có trong trace export (`vi-tri-root.csv`). Thẻ T-009 cảnh báo trace có timestamp lịch sử, lệch biểu kiến với metric và nhãn, và không được hiểu bậc 0 là cô lập (`results/T-009/the-dataset.md:95,282`). Dấu hiệu bất thường: ts-travel-service là "nguồn" (bậc vào 0); ts-user-service, ts-payment-service, ts-seat-service, ts-travel-plan-service không có trong trace. Nguyên nhân khả thi khác chưa loại: tải không gọi các service đó trong đoạn trace export, hoặc trace export không khớp phiên. Vì vậy chưa được dùng các ô này làm dữ liệu "root không cạnh" cho giả thuyết 3 của P4 trước khi P3 kiểm trace theo phiên. Nếu đúng là root không có trace, phương pháp chỉ dùng trace không xếp được root ở các ô này.
- Nezha: trace/log chỉ có quanh mốc tiêm (`results/T-008/the-dataset.md:72-80`). Không chấm được phát hiện liên tục đa nguồn hay báo động sai mỗi giờ bình thường từ trace/log Nezha; chỉ chấm ranking biết trước cửa sổ.
- Lỗi mã nguồn ít; chỉ trên OB.
- Tiêu chí 7 (lan) chỉ có ước lượng thô; RE3-OB để OPEN tới G3.
- Bộ giữ ngoài RE3-OB cùng hệ OB với Nezha-OB và cùng bộ công cụ RCAEval với RE2-TT, cả hai đều ở dev. Cấu hình chọn trên dev đã thấy cả hệ OB lẫn bộ công cụ RCAEval, nên RE3-OB không kiểm riêng được "khớp riêng hệ" hay "khớp riêng bộ công cụ". Nó kiểm tổ hợp (hệ OB, bộ công cụ RCAEval, lỗi mã nguồn của RE3) chưa có ở dev.

## 6. Câu hỏi cho Minh

**Câu 1 — Đơn vị chia ở Eadro, Nezha.** Ngữ cảnh: mục 4, "ca liền kề". Phương án: (a) giữ chia theo ô, và adapter chỉ đưa cho phương pháp, cho người phân tích P4 đoạn của đúng ca đó, không vượt sang lần tiêm kế; (b) chia theo phiên (Eadro-TT 9 phiên, mỗi phiên 3 root × 3 lỗi) hoặc theo ngày (Nezha-OB 2 ngày). Được/mất: (a) giữ đủ ô và cân bằng, nhưng dựa vào kỷ luật đọc dữ liệu; (b) với Eadro-TT: không đọc chồng ca phía kia; với Nezha-OB: chỉ còn 2 đơn vị (mỗi phía một ngày), và 23/33 ô, 46/56 ca có lần lặp ở cả hai ngày (đếm từ `results/T-008/runs/run-001/labels.json`), nên chia theo ngày đưa các lần lặp cùng ô sang hai phía, trái nguyên tắc chia theo ô (MRP §4). Đề xuất: (a) cho Nezha (khoảng giữa hai mốc tiêm 482–521 s; Nezha không ghi thời lượng tiêm; trace/log mỗi ca chỉ có 3 file phút riêng), (b) cho Eadro-TT (nghỉ 2 phút). Chưa kiểm phân bố vị trí khi chia theo phiên.

**Câu 2 — Cửa sổ (Q-54).** Ngữ cảnh: RE2-TT có 720 s trước tiêm; Eadro không có đoạn bình thường trước tiêm trong phiên; Nezha: khoảng giữa hai mốc tiêm 482–521 s nhưng không biết lỗi kết thúc lúc nào, và trace/log `rca_data` không có file trước phút tiêm (`results/T-008/the-dataset.md:72-80`); đoạn trước mốc có metric ngày (bình thường, đồng hồ OPEN). Nguồn tham chiếu bình thường riêng cho trace: trace construct khoảng 1 phút/ngày ở OB (`results/T-008/the-dataset.md:56-61`), độ sạch và đủ học ngưỡng: OPEN; nó không thay được dữ liệu liên tục cho chấm phát hiện. Vì vậy độ dài cửa sổ quyết bộ nào có đủ dữ liệu bình thường cho từng ca, tức là đổi được lựa chọn dataset. Phương án: (a) quyết ngay ở G1: sau mốc 300 s; trước mốc tối đa 300 s và không chồng lần tiêm trước (với Nezha chỉ áp cho metric; trace/log Nezha chỉ dùng cho ranking biết trước cửa sổ); Eadro lấy dữ liệu bình thường từ phiên no-fault (đề xuất **chưa kiểm**); (b) chuyển xuống đầu P3. Chuyển là sửa MRP §4 và Q-54. Đề xuất: (a), vì gói A đã phụ thuộc vào nó.

**Câu 3 — Retrieval@K (Q-56, E2).** Báo thêm Retrieval@K và Rerank@1 với K = 5, 10 bằng hàm có sẵn của RCAEval (`results/T-018/de-xuat-tai-lieu-chung.md:25-33`). Không phụ thuộc dataset, không tốn chạy thêm. Đề xuất: quyết ngay ở G1 là có báo.

**Câu 4 — Mốc tiêm ở chế độ (a) và ngân sách nhãn.** Ngữ cảnh: MRP §4 nói nhãn test chỉ để chấm; chế độ (a) của P3 lại đưa mốc tiêm cho phương pháp. Phương án: (a) xếp mốc tiêm vào "thông tin vận hành biết trước ở chế độ (a)", chỉ root và loại lỗi là nhãn chấm; ngân sách nhãn root cho mọi baseline là 0; (b) bỏ chế độ (a) trên test, chỉ chạy chế độ (b). Đề xuất: (a), ghi vào WHY. Mất: kết quả chế độ (a) luôn dễ hơn thực tế, phải báo cạnh chế độ (b).

**Câu 5 — CIRCA-PC và BOCPD trên Train Ticket so với Q-40.** Phương án: (a) báo "không chạy đủ trong ngân sách" như bài BARO làm với CIRCA (15/100 ca); chạy CIRCA kiến trúc làm bản chính trên TT; (b) giảm cột theo cấu hình tác giả (BOCPD dùng tập cột của `reproduce_bocpd`), đo lại đầu P3; (c) cho ngoại lệ ngân sách, chạy qua đêm trên EC2; (d) chạy một mẫu ca. Đề xuất: (b) cho BOCPD vì là quy ước của tác giả; (a) cho CIRCA-PC. Mất: (a) làm bảng TT thiếu một baseline nhân quả bản PC.

**Câu 6 — Gói và giữ ngoài.** A hay B (mục 3.6); RE3-OB hay Bank làm giữ ngoài. Đề xuất: A, giữ ngoài RE3-OB. Nếu Minh muốn kết luận theo lỗi mã nguồn chắc hơn thì chọn B.

**Câu 7 — Kiểm file GAIA/MicroSS hay không.** Ngữ cảnh: mục 3.5; trace/log Nezha không dùng được cho phát hiện liên tục (mục 5), nên trên dữ liệu công khai phần chấm phát hiện chỉ còn RE2-TT và Eadro (nếu phiên no-fault dùng được). Phương án: (a) kiểm file GAIA trong một task riêng (dung lượng phải đo và trình trước khi tải, luật cứng 8); (b) không kiểm, ghi giới hạn. Được/mất: (a) có thể thêm hệ thứ ba, dữ liệu bình thường liên tục, bộ độc lập, nhưng tốn một task, chất lượng và quyền dùng chưa xác minh; (b) gọn, nhưng phần phát hiện trên dữ liệu công khai mỏng. Đề xuất: (a); không thay gói A trước khi có kết quả kiểm.

## 7. R1–R3 của REVIEW T-020 được xử lý ở đâu

- R1 (mức tiếp xúc): `tiep-xuc.csv`, `runs/census-002/census-cases.csv` (mỗi ca có nguồn TX); 60 ca RE2-TT là TX1; thêm RE1-OB là TX2.
- R2 (vị trí root, Eadro-TT): `vi-tri-root.csv`, `runs/vi-tri-001/`; Eadro-TT nằm trong gói A.
- R3 (độc lập): `doc-lap.csv` theo Q-60(c); điều kiện giữ ngoài tách khỏi tiêu chí 9 (assert "giữ ngoài toàn TX0" trong `scripts/chia.py`).
