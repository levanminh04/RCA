# T-031 — Chạy P3 trên RE2-TT dev: kiểm khóa cấu hình và pilot chi phí

- **Trạng thái:** đề xuất ngày 06/10/2026. Minh: "duyệt, tạo spec cho 31 luôn" (LOG T-030 mục "Phiên 1"). Nội dung là Phần 2 của bản đề xuất đầu SPEC T-030, đã áp các sửa E1–E5 và các phương án Minh duyệt (D6 chỉ chặn nhánh MicroRank; K-SVR3 trên 30 ca). **Đã duyệt 06/10/2026** (Q-77, Q-78; lời Minh "đóng T-030, duyệt SPEC T-031").
- **Người làm:** Claude (Minh duyệt phân công 06/10/2026).
- **Người phản biện:** Codex (Minh duyệt phân công 06/10/2026).
- **Thuộc gói MRP:** P3 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ1, RQ2 và DT18-NV3 qua P3. Dùng mã `src/p3/` của T-030 để trả lời, **trước khi có số accuracy P3**:

1. Cấu hình nào được khóa theo các phép kiểm không dùng nhãn đã khai trước: mô hình CIRCA (K-SVR), nguồn chính của TORAI (K-B), số ca MicroRank lỗi ở cửa sổ ±300 s (D6)?
2. Chi phí thật của từng phương pháp và phép chiếu cho 30 ca, đủ để viết SPEC T-024, T-025 và xếp lịch BOCPD trên EC2 (Q-72)?

## Đầu vào

- Như SPEC T-030 mục Đầu vào.
- Mã `src/p3/` và kết quả T-030 (`results/T-030/`, gồm `k-b1.json`), sau khi T-030 xong và đã phản biện. Ghi hash mã `src/p3/` dùng trong mọi lượt.

## Đầu ra

Trong `results/T-031/`:
- `dem-loi-microrank.json`: trạng thái MicroRank ở 30 ca, theo nguyên nhân (§6.3, D6).
- `k-svr.json`, `do-nhay-builder.json`: K-SVR1–4 kèm route hồi quy từng nút; số ca đổi cạnh và đổi thứ hạng DA với hash seed 1, 2 (§6.5).
- `k-b.json`: dẫn K-B1 từ T-030; K-B2, K-B3; lệch lưới nguồn A từng ca, 30 ca (§6.6).
- `khoa-cau-hinh.md`: mô hình CIRCA và nguồn chính TORAI đã khóa theo luật khai trước, kèm bằng chứng.
- `do-chi-phi.md`: các ca pilot của từng phương pháp (§12) và lý do; số đo từng bước; tổng đo thật 30 ca cho MicroRank, CIRCA, TORAI (A và B); phép chiếu 30 ca cho các phương pháp còn lại (ghi "chưa kiểm"); đề xuất giới hạn `TIMEOUT` mỗi lượt (§8.3) và phạm vi, lịch T-024, T-025. Không tự khởi các task đó.
- `runs/<run-id>/`: cấu hình, hash mã, stdout/stderr, tiến độ, thời gian/RAM, bản ghi §13 đầy đủ; giữ cả lượt hỏng. Không chép telemetry.

Báo từng ca theo mã mờ và nguyên nhân, không kèm root, loại lỗi hay tên ca (Q-66).

## Phạm vi ghi

- `results/T-031/` (tạm và cache ở `results/T-031/work/`)
- `src/p3/`: chỉ sửa lỗi runner hoặc adapter thấy khi chạy; mỗi lần sửa ghi LOG, chạy lại test của T-030, giữ lượt hỏng. Test T-030 tự ghi và xóa cache trong `results/T-030/work/` (`fixture.py:15, 85`; `test_buoc34.py:21`); task được ghi trong thư mục đó. Đầu ra test chạy lại ghi ở `results/T-031/test-chay-lai/`, không ghi đè `results/T-030/tests/*.txt`.
- `tasks/T-031-chay-khoa-pilot/LOG.md`
- dòng T-031 trong `docs/STATE.md`

Không sửa SPEC này sau khi duyệt, `results/T-022/`, `results/T-030/` (trừ `work/` như trên), `docs/WHY.md`, `docs/DECISIONS.md`, code phương pháp cũ, môi trường chung, `data/`. Chạy Python không ghi bytecode. Thấy giao thức không đủ rõ, hoặc cần làm khác giao thức: dừng, đề xuất.

## Các bước và phụ thuộc

Không dùng nhãn root. Không chạy evaluator có nhãn trên đầu ra thật (xem Không làm). Giới hạn mỗi lượt (một ca × một phương pháp × một seed), khai trước theo §8.3 (N3): 3.600 s cho mọi phương pháp. Vượt thì ghi `TIMEOUT`, giữ lượt, chạy ca tiếp. Trong K-SVR2 và K-B3, `TIMEOUT` tính là không đạt. Trong D6, đếm riêng, cùng điều kiện dừng với `ERROR`. Mọi lượt đo chi phí tuần tự, không chạy cạnh lượt nặng khác (SL30); đo chi phí từng ca ở mọi bước, kể cả bước 2–4.

0. **Mở phiên.** Kiểm T-030 đã xong và phản biện xong; hash `src/p3/`; môi trường; RAM trống. — kiểm: dòng mở phiên trong LOG.
1. **Chọn ca pilot** (§12): với mỗi phương pháp, chọn 3 ca (nhỏ nhất, trung vị dưới, lớn nhất) theo yếu tố của phương pháp đó sau tiền xử lý. Không dùng nhãn; hòa thì lấy mã mờ nhỏ hơn. Yếu tố của CIRCA lấy từ đồ thị dựng ở bước 3. — kiểm: bảng yếu tố 30 ca và các ca đã chọn cho từng phương pháp trong `do-chi-phi.md`.
2. **MicroRank ở 30 ca, chỉ đọc trạng thái** (D6). Có ≥ 1 ca `ERROR` hoặc `TIMEOUT`: dừng nhánh MicroRank, báo Minh số ca theo nguyên nhân, chờ. Các nhánh khác chạy tiếp. — kiểm: `dem-loi-microrank.json`.
3. **CIRCA:** K-SVR1–4 kèm route hồi quy; K-SVR3 chạy lại cả 30 ca. Khóa mô hình theo luật §6.5; ghi `khoa-cau-hinh.md` và LOG. Sau khi khóa, đo độ nhạy builder với hash seed 1, 2 bằng mô hình đã khóa. Lượt K-SVR đầu (30 ca) dài hơn 1 giờ: dừng, báo Minh trước các lượt CIRCA còn lại.
4. **TORAI:** lấy K-B1 từ T-030 (nếu K-B1 OPEN thì chờ lời Minh); dựng đủ nguồn B; K-B2, K-B3; chạy TORAI nguồn A trên 30 ca × 3 seed, chỉ đọc trạng thái và đo chi phí, không chấm; ghi lệch lưới nguồn A 30 ca. Khóa nguồn chính theo luật §6.6; ghi `khoa-cau-hinh.md` và LOG.
5. **Kiểm trên ca thật** (§11.6): BARO khớp thứ tự chính thức; TraceRCA `ji` khớp `check_tracerca.py`; TORAI khớp `ranks`; CIRCA `current` đúng. Trên ca trung vị dưới của từng phương pháp: hai cửa sổ bình thường với mốc giả t′ = 360 s, khai trước (N = [60, 360), A = [360, 660) đều nằm trong 720 s đầu; t′ chỉ hợp lệ trong [300, 420], 360 là điểm giữa), và hoán vị (§11.9–11.10). MicroRank thêm hash seed 1; TraceRCA so `ji` với `check_tracerca.py`.
6. **Pilot chi phí** (§12) cho BARO, SimpleRCA, TraceRCA, N-Sigma, BOCPD. MicroRank, CIRCA (mô hình đã khóa) và TORAI dùng tổng đo thật 30 ca từ bước 2–4. **BOCPD: chỉ đo thời gian trên tiền tố, không chạy đủ 1.441 điểm trên laptop.** Hai ca theo yếu tố BOCPD ở §12: ca nhỏ nhất ở T = 300 và 600 điểm đầu; ca lớn nhất ở T = 150 và 300 điểm đầu. Tiền xử lý §7.2 trên cả bản ghi (giữ đúng số cột d của ca), rồi lấy T điểm đầu; gọi `online_changepoint_detection` như §7.2. Mỗi T một lượt, giới hạn 3.600 s. Không chấm phát hiện, không tính điểm đổi, không dùng đầu ra ngoài thời gian và RSS; script ở `results/T-031/scripts/`, không sửa `src/p3/`. Chiếu 1.441 điểm: báo số mũ đo được p = log₂(t(2T)/t(T)) của mỗi ca; chiếu theo cả T² và T^p, báo cả hai, không chọn sau khi thấy số. Lý do dùng T²: code gọi `multivariate_t.pdf` khoảng T²/2 lần (`baro/_bocpd.py:86–108`). Chiếu 30 ca: với c = thời gian/T² ở T = 300 của mỗi ca đo, báo số mũ q = log(c_lớn/c_nhỏ)/log(d_lớn/d_nhỏ); nhân theo (d_ca/d_nhỏ)² và theo (d_ca/d_nhỏ)^q, báo cả hai; d = số cột sau bỏ cột hằng. Giả định d² lấy từ số đo tổng hợp T-030 (`results/T-030/runs/bocpd-tong-hop-001/ket-qua.json`); sai nếu chi phí theo vị trí trong chuỗi khác T², hoặc phần cố định mỗi lần gọi đổi theo d khác giữa các ca trung gian. Mọi số chiếu ghi "chưa kiểm". Phép kiểm §11.8 trên đầu ra N-Sigma của ca pilot: đổi mốc ở phía evaluator rồi so báo động; báo động phải giống hệt. Chỉ so báo động, không tính độ đo. — kiểm: `runs/` có tiến độ, thời gian từng bước, RSS.
7. **Chiếu chi phí và bàn giao:** viết `do-chi-phi.md` theo phân bố yếu tố chi phí của 30 ca, không lấy ca trung vị nhân 30. Ghi rằng phép chiếu BOCPD là của laptop và lấy từ tiền tố (bước 6). Phép chiếu cho 30 ca vượt 20 giờ (Q-72): báo Minh trước khi đề xuất lịch. Đề xuất SPEC T-025 đo ca đầu trên EC2 rồi chiếu lại. Đề xuất giới hạn `TIMEOUT` mỗi lượt cho T-024, T-025 (N3); đề xuất phạm vi và lịch T-024, T-025, gồm phương án chạy BOCPD trên EC2 song song với T-024 (LOG T-022 "Phiên 6 (tiếp)"), và việc T-024 dùng lại bản ghi 30 ca của bước 2–4 nếu hash mã không đổi. — kiểm: mỗi số có nguồn; phép chiếu có giả định và trường hợp sai.

Phụ thuộc: 1 sau 0. 2, 3, 4 độc lập nhau. Bước 5 và 6 của mỗi phương pháp chỉ chờ bước khóa của chính nó (MicroRank chờ 2, CIRCA chờ 3, TORAI chờ 4); BARO, SimpleRCA, TraceRCA, N-Sigma, BOCPD không chờ 2–4. Bước 5 cần 1. Điểm dừng D6 chỉ chặn nhánh MicroRank. 7 sau 6.

## Kiểm đúng đắn

- Phần kiểm trên ca thật của §11.6, §11.8 (N-Sigma), §11.9–11.11 (§11.11 gồm D6, K-SVR, độ nhạy builder, K-B2, K-B3).
- Đối chiếu được: `check_tracerca.py` của T-015; route OLS của T-014; file tác giả torai-TT.
- Không kiểm được trong task: accuracy P3 (T-024); chi phí BOCPD đủ 30 ca (T-025, EC2). Phép chiếu chi phí vì vậy còn "chưa kiểm".

## Tiêu chí xong

- `dem-loi-microrank.json` (kèm lời Minh nếu ≥ 1 ca lỗi), `k-svr.json`, `do-nhay-builder.json`, `k-b.json` có thật và parse được.
- `khoa-cau-hinh.md` ghi mô hình CIRCA và nguồn TORAI đã khóa, trước mọi lượt evaluator trên đầu ra thật.
- `do-chi-phi.md` có số đo từng phương pháp theo cấu hình đã khóa (hoặc cận dưới khi chạm giới hạn), phép chiếu 30 ca ghi "chưa kiểm", đề xuất giới hạn `TIMEOUT` và lịch T-024, T-025.
- Không có số accuracy P3 trên đầu ra mới; không mở `data/locked/`.
- LOG đủ để agent khác, trên máy khác, làm tiếp; dòng STATE đã cập nhật.

## Không làm

Không chạy evaluator có nhãn trên đầu ra thật của 30 ca dev. Với MicroRank (§6.3), CIRCA trước khi khóa (§6.5) và TORAI trước khi khóa (Q-74 Q3), đây là quyết định đã có. Với các phương pháp còn lại, đây là lựa chọn phạm vi của SPEC này: việc chấm thuộc T-024. Phép kiểm §11.8 chỉ so báo động, không tính độ đo, nên vẫn làm. Không benchmark đủ, không chạy chế độ (b) đủ 30 ca, không chạy EC2. Không sửa giao thức, WHY, code phương pháp cũ hay môi trường chung; không cài thư viện. Không chạy Nezha, Eadro; không mở test hay RE3-OB. Không tự tạo SPEC T-024, T-025. Không commit hay push khi Minh chưa duyệt.

## Chi phí ước lượng

**Chưa kiểm.** Giả định dùng lại môi trường và lõi đã có, laptop, một lượt nặng một lúc.

- Công agent: khoảng 3–6 giờ; không gồm thời gian chờ Minh.
- Thời gian máy:
  - MicroRank 30 ca: bản cũ đo 106 s/ca ở cửa sổ ±300 dòng trên laptop (`results/T-005/do-kha-thi.md`, bảng 2a); bản sửa đo một ca trên EC2: 14,7 s (`results/T-015/runs/tt-local/auth/run-ledger.csv`). Khoảng 8–120 phút.
  - CIRCA: 4–5 lượt 30 ca (K-SVR, lặp K-SVR3, hash seed 1, 2; thêm lượt OLS nếu khóa OLS); thời gian phần chấm SVR chưa đo. T-014 đo chấm và ghi snapshot một ví dụ khoảng 4 s.
  - TORAI: K-B3 90 lượt trên B, cộng 90 lượt trên A; T-016 chạy 30 ca dev khoảng 66 s trên EC2 (`results/T-016/quy-mo-tt.md` mục 5). Dựng `logts` nguồn B bằng Drain: chưa đo.
  - BOCPD: bốn lượt đo trên tiền tố (bước 6). Ước lượng chưa kiểm, từ số đo tổng hợp T-030 (4,29 ms mỗi lần gọi pdf ở d = 25; 15,83 ms ở d = 48): ca nhỏ nhất khoảng 3 phút ở T = 300 và 13 phút ở T = 600; ca lớn nhất khoảng 3 phút ở T = 150 và 12 phút ở T = 300. Phép tính cũ của SPEC này (∝ T²d³; 10 phút ở ca nhỏ nhất; 17,5 giờ cho 30 ca) sai: số đo tổng hợp cho chi phí ∝ T²d², ngoại suy 27–83 giờ cho 30 ca trên laptop (LOG T-030, 06:1x).
  - Tổng phần ngoài CIRCA khoảng 2–5 giờ, chưa kiểm.
- Luật cứng 8: duyệt SPEC này là đồng ý trước một loại lượt dài hơn 1 giờ: lượt K-SVR đầu tiên trên 30 ca (tối đa 3 giờ theo K-SVR4). Lượt K-SVR đầu dài hơn 1 giờ: dừng, báo Minh trước các lượt CIRCA còn lại. Lượt khác chiếu trên 1 giờ: dừng, báo.
- Chiếu cho EC2 (T-025): chưa có tỉ số tốc độ laptop/EC2 đo trên cùng việc trong cùng điều kiện.
- RAM: MicroRank bản cũ RSS tới khoảng 2,3 GB (T-005); RAM trống laptop từng chỉ 2,2–2,7 GiB. Kiểm trước mỗi lượt nặng; không chạy cạnh việc nặng của T-023.
- Đĩa: tăng 0,1–0,5 GB; không chép telemetry.
- Q-40: phép kiểm 30 ca của mỗi phương pháp phải vừa 3 giờ. K-SVR4 dùng đúng trần này.

## Rủi ro và điều chưa chắc

- MicroRank có thể lỗi nhiều ở ±300 s (operation mới, std nền NaN). Khi đó nhánh MicroRank dừng ở bước 2, chờ Minh. Chưa kiểm.
- K-B1 (T-030) có thể trượt; khi đó TORAI A làm chính, kèm lệch lưới và ngưỡng toàn file. Chưa kiểm.
- SVR có thể rơi về z-score ở nút có cha, nên khóa OLS. Lỗi do NaN/inf đầu vào cũng ảnh hưởng OLS. Chưa kiểm.
- Phép chiếu BOCPD dựa trên tiền tố và giả định d² (kiểm một phần bằng hai ca). Có thể sai nếu chi phí đổi theo vị trí trong chuỗi khác T², hoặc theo d khác d² ở các ca trung gian. Lượt tiền tố chạm 3.600 s thì chỉ có cận dưới. Phép chiếu vượt 20 giờ (Q-72) thì báo Minh, không đề xuất lịch T-025.
- Tần suất posterior BOCPD không hữu hạn: chưa kiểm.
- Lỗi mã `src/p3/` chỉ lộ khi chạy trên ca thật; sửa lỗi làm đổi hash mã và có thể phải chạy lại lượt trước đó.
