# Nhật ký T-018

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

---

## Phiên 1 — 04/10/2026 — Claude (Opus 5.5) — laptop Windows 11 i5-1240P — vai trò: người làm

**Mở phiên:** 08:28. HEAD git `93f13d4c4a966428177e2acc287d96bc89303e92`. Đã đọc AGENTS, STATE, LESSONS, review-prompt, mẫu SPEC/LOG, MRP §2–§7 (kỹ P1, P2), WHY, DECISIONS, DT18, hướng dẫn của cô. Task mới, chưa có đầu ra phiên trước.

Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026.

Khối `<task>` của prompt Đợt 1 (chép nguyên văn):

```text
Thư mục task: tasks/T-018-ho-so-gdn-decomprca/. Thư mục kết quả: results/T-018/.

Đầu vào:
- results/T-001.
- results/T-005/.
- results/T-006/kiem-dung-dan.md mục 9, 10.
- Code GDN ở D:\RCA-ext\src\GDN (revision 9853899); môi trường py38-gdn: chỉ dùng, không sửa.
- Bài GDN, AAAI'21.
- Bài DecompRCA: arXiv 2609.36686; repo cruiseresearchgroup/DecompRCA.

Yêu cầu:
1. Hồ sơ GDN theo <ho_so>. Phần ví dụ tính tay là một bước chấm điểm trên một ca đã thấy.
   - Lần theo từng bước: học cấu trúc đồ thị (top-k theo embedding), dự báo bằng attention, điểm lệch chuẩn hóa theo trung vị và IQR, lấy max, áp ngưỡng.
   - Chỉ ra mọi chỗ có thể dùng nhãn hoặc dữ liệu test:
     - report='best' khác report='val' thế nào;
     - bộ chuẩn hóa được fit trên dữ liệu nào;
     - epoch được chọn bằng cách nào.
   - Nêu cách chạy hợp lệ ở chế độ b (không dùng mốc tiêm).
2. Yêu cầu đầu vào của GDN:
   - GDN cần một bộ cột cố định, trong khi RE2-TT có 340–375 cột và bộ cột khác nhau giữa các ca. Nêu cách xử lý và hệ quả.
   - Cần bao nhiêu dữ liệu bình thường.
   - Từ đó suy ra dataset nào chạy được GDN.
3. DecompRCA:
   - Tóm tắt kỹ thuật.
   - Hệ quả cho P3: giao thức chạy, tập ứng viên, độ đo.
   - Hệ quả cho P4: các giả thuyết, ghi rõ "chưa kiểm".
   - Hệ quả cho việc chọn dataset ở G1.
   - Kiểm các khẳng định trên bản PDF và trong repo.
   - Không cài phương pháp mới, không chạy benchmark.

Edge case tối thiểu phải có trong SPEC (bạn tự tìm thêm):
- Seed.
- Cột hằng.
- Độ dài cửa sổ trượt.
- Ngưỡng lấy từ tập kiểm định.
- Lệch thời gian giữa các cột.

Không dùng EC2. Được ghi thêm: D:\RCA-ext\work\T-018\.
```

**Diễn biến** (một dòng mỗi bước con, ghi ngay khi xong):
- 08:28 — mở phiên — tạo `tasks/T-018-ho-so-gdn-decomprca/LOG.md`.
- 08:35 — kiểm đầu vào — GDN `D:\RCA-ext\src\GDN` HEAD `9853899da860…`, `git status` sạch; `py38-gdn` Python 3.8.10, `pip freeze` trùng hệt `results/T-005/runs/freeze-py38-gdn.txt` (torch 1.5.1+cpu, torch_geometric 1.5.0); file GDN của T-005 còn đủ (`model_re2tt5.pt`, `data/re2tt5/{train,test,list}`); 30 ca `re2tt_*` trong `data/rcaeval/` đều có `inject_time.txt`.
- 08:36 — báo trước tải (giới hạn 1 GB): (1) `https://arxiv.org/pdf/2609.36686` (DecompRCA v1, Content-Length 659 472 B); (2) `https://arxiv.org/pdf/2106.06947` (GDN, 1 408 689 B); (3) `git clone https://github.com/cruiseresearchgroup/DecompRCA` (GitHub API báo size 919 KB, pushed_at 2026-09-29). Tổng dưới 5 MB. Nơi lưu: `D:\RCA-ext\work\T-018\nguon\`. Kiểm: SHA-256 ghi vào `results/T-018/nguon-tai.md`; với repo ghi commit HEAD. arXiv không công bố hash, nên kiểm bằng Content-Length và tải lại lần hai so SHA-256.
- 08:55 — viết SPEC (`SPEC.md`), tự duyệt theo ủy quyền.
- 09:00 — tự phản biện SPEC như người phản biện độc lập. Đối chiếu với SL24–SL33, REVIEW T-003 R1 và sự cố ghi đè WHY-16. Đã sửa: (1) R1 truyền `test_dataloader=None` vào `train()` để nếu SHA trùng T-005 thì chứng minh luôn dữ liệu test không ảnh hưởng học/chọn epoch (trước chỉ dựa vào đọc code); (2) ghi rõ R1 không phải cấu hình chế độ b vì bộ 333 cột của T-005 có dùng cột của ca test (chỗ dễ rò); (3) L\* dùng tên cột của cả ca giữ ngoài nên chỉ đo tổng quát hóa thuần, ảnh hưởng cột thiếu đo trên R1; (4) chốt t\* theo A(t) của code; (5) nêu nhiễu giữa cỡ tập học và độ đa dạng ca; (6) lần chạy R1 thứ hai (nếu cần) truyền loader test thật để tách nguyên nhân. Không thấy bước nào phụ thuộc sai thứ tự; B1, B2, B3, B9 làm xen lúc B4/B7 chạy nền.
- 09:10 — **đính chính dòng 08:35:** câu "30 ca `re2tt_*` đều có `inject_time.txt`" sai. Kiểm lại: chỉ `re2tt_ts-auth-service_cpu_1` có file này trong `data/rcaeval/` (đúng như `data/README.md` ghi "còn thiếu 89 ca"). T-005 đã tải 6 file ở `D:\RCA-ext\dl\rcaeval-inject\`. Lỗi do tôi suy từ một thư mục. Không được đọc `data/locked/rcaeval-metadata/cases.parquet` (có nhãn ca khóa).
- 09:12 — báo trước tải: `inject_time.txt` của các ca dev còn thiếu, từ HF `phamquiluan/RCAEval` revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, mỗi file 10 B, tối đa 29 file (< 1 KB). Lưu `D:\RCA-ext\work\T-018\nguon\rcaeval-inject\<ca>\`. Kiểm: git blob oid khớp HF (như T-005), và đối chiếu với điểm giữa timestamp metric (T-002 ghi mốc tiêm nằm đúng giữa file).
- 09:16 — tải 30 file `inject_time.txt` (dùng `scripts/tai_moc_tiem.py`): 30/30 khớp git blob oid HF; 30/30 mốc = điểm giữa timestamp metric; mọi ca 720 dòng trước mốc, 721 dòng từ mốc; 5 file trùng bản T-005 đã tải, 1 file trùng bản có sẵn trong `data/` — `runs/tai-moc-tiem.json`.
- 09:22 — B3 xong: `scripts/chuan_bi_gdn.py` (env py312, 81 s). Dữ liệu `re2tt5` dựng lại **trùng từng byte** với T-005 (SHA-256 train.csv, test.csv, list.txt). L\* = 317 cột (hợp 30 ca: xem json). Cột hằng trong tập học: 39 (1 ca), 27 (5 ca), 16 (10 ca). Giá trị sau min-max lớn nhất ở đoạn giữ ngoài: 6,0e8 (1 ca), 7717 (5 ca), 7332 (10 ca) — dấu hiệu E2 (cột hằng trong tập học mang đơn vị thô sang test). `runs/b3-chuan-bi.json`.
- 08:44 — **đính chính giờ:** các mốc giờ từ dòng 08:35 đến 09:22 ở trên là ước đoán, không đọc đồng hồ máy; thứ tự các bước vẫn đúng. Đồng hồ máy: R1 bắt đầu 08:43:43 (`runs/r1-re2tt5-seed5.log`). Từ dòng này giờ lấy bằng `date`.
- 08:44 — B4 bắt đầu: R1 = `chay_nen.sh r1-re2tt5-seed5 --data re2tt5 --seed 5 --test-none` (luồng mặc định; tải CPU 32 %, RAM trống 3288 MB lúc bắt đầu).
- 08:49 — B2 xong: `scripts/dem_cot.py` → `cot-re2tt/{ca,cot,loai,cot-khong-du-30-ca}.csv`, `tom-tat.json`: 30 ca, 340–375 cột thô, 318–347 cột sau làm sạch, giao 317, hợp 354, 37 cột không đủ 30 ca; bước thời gian luôn 1 s; 0 ô inf. Nhịp lặp giá trị (trung vị đoạn lặp): latency 5 s, workload 6,5 s, mem 18 s, socket 36,75 s, cpu/diskio 1 s nhưng có đoạn phẳng dài (xem mẫu ts-order-service_cpu).
- 08:49 — B9 (một phần): `scripts/retrieval_ngau_nhien.py` → `runs/b9-retrieval-ngau-nhien.json`. Bộ chọn ngẫu nhiên 15 metric, quy về service như DecompRCA: Retrieval@15 = 0,816 (RE1-OB), 0,901 (RE1-SS); K=5: 0,392 / 0,500. Số cột hợp của RE1-OB/RE1-SS = 95/63, khớp câu 'expose 95, 63' của bài (bài đếm hợp các ca).
- 08:55 — B9 bản nháp `decomprca.md`: tóm tắt, 15 khẳng định đã kiểm (PDF + repo), hệ quả P3/P4/G1. Phát hiện: K8 (K hai đơn vị), K9 (truy hồi ngẫu nhiên 0,82–0,90 ở K=15), K12 (RCD/ε/CIRCA không phải bản RCAEval), K13 (sơ đồ DK Train Ticket chứa đủ 5 service gốc RE1-TT; p≈0,0045 nếu ngẫu nhiên; chưa kết luận rò).
- 08:59 — ghi mục 'Thay đổi trong lúc làm' vào SPEC (đổi cơ sở seed/hoán vị sang re2tt5; lượt 10 ca dự kiến gần 2 giờ nên chưa chạy). Tạo `re2tt5_daocot`, `re2tt5_hoanvi` bằng `scripts/tao_bien_the.py`. Lượt `l1-lstar-n1-seed5` bắt đầu 08:57 (6 luồng), song song R1.
- 09:01 — B2b (sau khi đếm xong mới so với nhãn): 12 cột latency/workload của contacts, preserve, preserve-other, seat, security, user **chỉ vắng ở đúng 4 ca, cả 4 đều có service gốc ts-order-service** (order_disk_2/3, order_loss_2/3). 23 cột `*_error` chỉ có ở một phần ca (2–20 ca); sự có mặt của chúng trùng một phần với service gốc (vd `ts-train-service_error` có ở 6 ca, 4 ca là train-service). Chỉ 2 cột error có ở đủ 30 ca (admin-travel, ui-dashboard). Hệ quả: bộ cột của một ca là một đường rò nhãn/triệu chứng; GDN với L\* mất gần hết cột error. Nguồn: `cot-re2tt/cot-khong-du-30-ca.csv`.
- 09:04 — SPEC 'Thay đổi trong lúc làm' mục 4: seed đo ở cỡ 1 ca (seed 5/1/2) và 5 ca (seed 5/1); hoán vị cột đo ở 1 ca. Dựng `lstar_n1_hoanvi`.
- 09:09 — bản nháp `dinh-chinh-task-cu.md` (D1–D4), `de-xuat-tai-lieu-chung.md` (E1–E6), `nguon-tai.md`, `moi-truong.md`; hồ sơ mục 1–6, 8, 9.1 viết xong. Đang chờ R1 (epoch 14–15, khoảng 3 phút/epoch do máy bận) và hàng đợi lượt 1 ca.
- 09:24 — dừng hàng đợi cũ (l5/l6 sau R1, 8 luồng); hàng đợi mới: l5 sau R1 và l4, luồng mặc định; l6 chỉ khi l5 < 45 phút (SPEC thay đổi mục 5). Lượt l1 đã học xong 09:14, đang chấm.
- 09:33 — l1 xong (học 1037 s, chấm 869 s, 30 epoch, epoch tốt nhất 28, τ=39,70). Phân tích (`scripts/phan_tich_gdn.py` → `runs/b6b7-phan-tich.json`): 19 đoạn bình thường giữ ngoài (3,77 giờ) — chuẩn hóa theo code: 23,6 % tick báo động, 143 đợt (37,9 đợt/giờ), 19/19 đoạn; biến thể b: 99,6 % tick; bỏ cột hằng-trong-tập-học (chẩn đoán) không đổi (99,6 %). A_max tới 1e11. Chẩn đoán dữ liệu (`scripts/chan_doan_lech_phan_bo.py` → `runs/b6-lech-phan-bo.json`): tỷ lệ ô giữ ngoài ngoài [−1, 2] sau min-max = 23,1 % (học 1 ca), 4,9 % (5 ca), 0,6 % (10 ca); mem 89 % / 14 % / 1,1 %. Cơ chế: mức metric (nhất là mem, latency) khác nhau giữa các lượt chạy, còn 12 phút một ca không phủ được khoảng đó.
- 09:44 — R1: lượt bị `timeout 3600` dừng ở epoch 29/30 (EXIT=124, 09:43:56), trước bước chấm. Loss epoch 0–28 trùng từng chữ số với T-005. `model.pt` (lưu 09:33, val loss tốt nhất tới epoch 28) có **SHA-256 nội dung tensor trùng hệt** `model_re2tt5.pt` của T-005 (7e45aaf8…; chênh tối đa 0,0); SHA file khác do byte của torch.save. Suy ra: (1) GDN lặp lại tất định trên máy này; (2) epoch tốt nhất của T-005 ≤ 28 nên epoch 29 không đổi mô hình; (3) R1 truyền test_dataloader=None còn T-005 truyền loader test thật mà mô hình trùng, nên dữ liệu test không ảnh hưởng học/chọn epoch (G5). Lượt hỏng giữ lại (`runs/r1-re2tt5-seed5.log`). Bước chấm chạy lại riêng bằng `--chi-cham` (lý do a: hoàn tất lượt lặp).
- 09:45 — hủy hàng đợi l5/l6 (SPEC thay đổi mục 6). Đang chạy: r1s-re2tt5-cham, r1b-daocot-cham (chỉ chấm, mô hình R1), hàng đợi l2→l3→l4 (1 ca).
- 09:53 — r1s (chấm R1, 351 s) và r1b (đảo cột CSV): 4 mảng test_scores, normal_scores, test_pred, val_pred **trùng SHA-256** giữa hai lượt → đổi thứ tự cột CSV không đổi kết quả. τ=63,83; 88 tick báo động trên R-ca.
- 09:53 — B5 tính tay (`scripts/tinh_tay_gdn.py --run r1s-re2tt5-cham --model …r1-re2tt5-seed5/model.pt` → `runs/r1s-re2tt5-cham-tinh-tay.json`): lệch dự báo test tối đa 6,0e-6, val 4,9e-7; lệch điểm tối đa 3,3e-4, 0 ô vượt dung sai; τ tay 63,832934 / code 63,832916; argmax khác 0/1436 tick; báo động khác 0/1436. Đạt Tiêu chí xong 2. Hoán vị nút trong bản numpy: lệch 7,1e-15. 333/333 nút có chính nó trong top-k → 4 láng giềng thật. t* = tick 12 (dòng 17): ts-consign-service_diskio, α=1,0 vào ts-route-service_diskio (giá trị chuẩn hóa nhảy 0,48→53,84 ở dòng 13), dự báo 26,28 so với thực 0,37.
- 09:53 — giải thích bằng nhãn sau khi có kết quả (`scripts/giai_thich_ca.py` → `runs/b5-giai-thich-ca.json`): 47/88 báo động trước mốc tiêm, 41 từ mốc; báo động đầu tiên sau mốc 65 s; 0/41 báo động sau mốc có cột đầu thuộc service gốc ts-route-service (chủ yếu ts-seat-service_error 28, ts-ticketinfo-service_mem 13); trung vị A trước/sau mốc 7,75 / 8,38. Biến thể b: 712 trước + 721 sau.
- 09:53 — phân tích r1s, l2 (`runs/b6b7-phan-tich.json`): R1 (5 ca) trên 19 đoạn giữ ngoài: code 11,2 % tick báo động (61 đợt, 16,2/giờ, 18/19 đoạn); b 93,7 %; b bỏ cột hằng 86,5 %. l2 (1 ca, seed 1): τ 59,17 (seed 5: 39,70); code 24,5 % tick; so với seed 5 trên R-ca: Pearson A 0,32, Spearman 0,11, Jaccard báo động 0,18.
- 13:39 — l3 (seed 2), l4 (hoán vị list.txt, seed 5) xong; phân tích gộp `runs/b6b7-phan-tich.json`. 1 ca, 4 lượt: τ 36,79–59,17; tick báo động trên 19 đoạn giữ ngoài (code) 23,6–30,7 %, 37,9–53,3 đợt/giờ, 18–19/19 đoạn; biến thể b 99,6 % ở cả 4. Trên R-ca: Jaccard báo động giữa các seed 0,18–0,58, Spearman A 0,11–0,62; hoán vị cột cùng seed 5: Jaccard 0,87, Spearman 0,61. Kiểm `D:\RCA-ext\src\GDN`: không file nào đổi, không `__pycache__` mới.
- 13:42 — tiếp tục sau khi phiên bị dừng vì hết lượt dùng (khoảng 10:05–13:40). Máy rảnh: chạy l5 (SPEC thay đổi mục 7).
- 13:43 — lượt nền đầu tiên cho l5 hỏng ngay vì gọi `scripts/chay_nen.sh` bằng đường dẫn tương đối (exit 127, không có lượt GDN nào chạy); chạy lại bằng đường dẫn tuyệt đối.
- 14:05 — l5 (5 ca, L\*, seed 5) xong: học 1168 s, chấm 119 s, epoch tốt nhất 21, τ=48,32. 19 đoạn giữ ngoài: code 10,8 % tick (50 đợt, 13,3/giờ, 18/19 đoạn); b 99,6 %; b bỏ cột hằng 95,1 %. R-ca: 97 tick báo động. So cùng bộ cột L\*: 1 ca 23,6 % → 5 ca 10,8 % (cách code); biến thể b không giảm. l6 (seed 1) đang chạy vì l5 < 30 phút.
- 14:24 — l6 (5 ca, L\*, seed 1) xong (học + chấm khoảng 18 phút): τ=55,08, epoch tốt nhất 29; giữ ngoài code 10,3 % (12,5 đợt/giờ, 17/19 đoạn); b 99,6 %; so với l5 trên R-ca: Jaccard 0,62, Pearson 0,98, Spearman 0,45. Cập nhật hồ sơ 9.4, CSV yêu cầu đầu vào, ca-da-chay (110→150 dòng).
- 14:24 — đính chính dòng trên: `ca-da-chay.csv` có 160 dòng (không phải 150), 25 ca khác nhau. Ghi SPEC 'Thay đổi trong lúc làm' mục 8.
- 14:24 — chạy l7 (10 ca, L\*, seed 5) theo SPEC mục 9.
- 14:24 — ghi chú: giờ trong tiêu đề SPEC 'Thay đổi trong lúc làm' mục 1–9 là giờ gõ tay, có thể lệch vài phút; giờ chính xác của từng lượt nằm trong `runs/<nhan>.log`.
- 14:59 — l7 (10 ca, L\*, seed 5) xong: học 1928 s, epoch tốt nhất 25, τ=49,53; 19 đoạn giữ ngoài: code 4,95 % tick (5,0 đợt/giờ, 9/19 đoạn); b 45,2 %; R-ca: 0 tick báo động (A max 27,9). Cập nhật hồ sơ 0, 9.4; CSV; ca-da-chay; kiem-dan-dong (0 file không tìm thấy).

**Quyết định của Minh trong phiên:** không có (phiên làm theo ủy quyền tự duyệt SPEC trong prompt Đợt 1; không hỏi Minh câu nào). Không có dòng cần ghi DECISIONS.

**Kết thúc phiên** (báo cáo cuối theo prompt Đợt 1; cũng là 6 ý của mẫu LOG):

**A. Đã làm.**
- Viết và tự duyệt SPEC (theo ủy quyền), tự phản biện, 9 mục "Thay đổi trong lúc làm".
- Hồ sơ GDN đủ 7 mục MRP P1 + đường nhãn + yêu cầu đầu vào + cách chạy chế độ b (`results/T-018/ho-so-gdn.md`); mọi file:dòng in lại bằng `scripts/kiem_dan_dong.py`.
- Dựng lại dữ liệu GDN của T-005 bằng script độc lập (trùng từng byte); học lại (R1) ra trọng số trùng hệt T-005; tính tay độc lập bằng numpy khớp code ở mọi dự báo, điểm, quyết định (1436 tick × 333 cột).
- Phép kiểm không cần nhãn: đảo cột CSV (trùng byte), hoán vị nút (lệch 7e-15), chấm lại tập kiểm định (0 báo động), "bình thường vs bình thường" trên 19 đoạn giữ ngoài (3,77 giờ), seed (1 ca: 3 seed; 5 ca: 2 seed), hoán vị `list.txt`, cỡ tập học 1/5/10 ca.
- Thống kê bộ cột, cột hằng, nhịp cập nhật của 30 ca dev RE2-TT; chẩn đoán lệch mức giữa các lượt chạy.
- Đọc DecompRCA (PDF + repo): tóm tắt, 15 khẳng định đã kiểm, hệ quả P3/P4/G1; tính Retrieval@K ngẫu nhiên mức service trên RE1-OB/SS.
- Soi task cũ: 4 vấn đề (D1–D4). Soạn 6 đề xuất cho tài liệu chung (E1–E6).

**B. File đã thay đổi.**
- Trong repo (mới): `tasks/T-018-ho-so-gdn-decomprca/SPEC.md`, `LOG.md`; toàn bộ `results/T-018/` (ho-so-gdn.md, decomprca.md, yeu-cau-dau-vao.csv, ca-da-chay.csv, dinh-chinh-task-cu.md, de-xuat-tai-lieu-chung.md, moi-truong.md, nguon-tai.md, cot-re2tt/*, runs/*, scripts/*).
- Trong repo (sửa): `docs/STATE.md`, chỉ chèn một dòng T-018.
- Ngoài repo (mới): `D:\RCA-ext\work\T-018\nguon\` (2 PDF, 2 file văn bản, clone DecompRCA, 30 `inject_time.txt`), `D:\RCA-ext\work\T-018\gdn\data\` (8 bộ dữ liệu: re2tt5, re2tt5_daocot, re2tt5_hoanvi, lstar_n1, lstar_n1_hoanvi, lstar_n5, lstar_n5_hoanvi, lstar_n10), `D:\RCA-ext\work\T-018\gdn\runs\` (10 lượt: r1-re2tt5-seed5 hỏng ở giới hạn 1 giờ, r1s-re2tt5-cham, r1b-daocot-cham, l1–l7).
- Không sửa: `D:\RCA-ext\src\GDN` (kiểm: không file nào mới hơn SPEC), `envs`, file của task khác, `data/`.

**C. Kiểm tra đã chạy và kết quả.**
- Đầu vào: GDN `9853899` sạch; `py38-gdn` freeze trùng T-005; 30 `inject_time.txt` khớp oid HF 30/30, mốc = điểm giữa file 30/30.
- Dữ liệu GDN dựng lại trùng SHA-256 với T-005 (3/3 file).
- Lặp: loss epoch 0–28 trùng T-005; trọng số trùng hệt T-005 theo nội dung tensor; R1 truyền `test_dataloader=None` → dữ liệu test không ảnh hưởng học.
- Tính tay độc lập (numpy): lệch dự báo ≤ 6,0e-6; 0 ô điểm vượt dung sai; argmax và báo động trùng 1436/1436 tick; τ khớp (Tiêu chí xong 2 đạt).
- Đổi thứ tự cột: CSV đảo cột → 4 mảng trùng SHA-256; hoán vị nút trong bản numpy → lệch 7,1e-15; học lại với `list.txt` hoán vị → Jaccard báo động 0,87 so với gốc.
- Đầu ra không rỗng, hữu hạn ở mọi lượt (`huu_han: true`).
- Chấm lại tập kiểm định: 0 tick vượt τ ở mọi lượt.
- Bình thường vs bình thường (19 đoạn, 3,77 giờ): tick báo động sai (cách code) 23,6–30,7 % (1 ca, 4 lượt), 10,3–11,2 % (5 ca, 3 lượt), 4,95 % (10 ca); biến thể b 99,6 % / 93,7–99,6 % / 45,2 %.
- Seed: 1 ca Jaccard 0,18–0,58; 5 ca Jaccard 0,62.
- Giá trị trung gian: 333/333 nút có chính nó trong top-k; 6 (test) và 16 (val) cột có IQR lỗi < 1e-6; cột hằng trong tập học 39/27/16 (1/5/10 ca); giá trị chuẩn hóa ở đoạn giữ ngoài tới 6,0e8; t* của ca R-ca do α = 1 dồn vào một láng giềng lệch 54 lần khoảng học.
- Trích dẫn: `scripts/kiem_dan_dong.py` in lại 126 đoạn code/PDF, 0 file không tìm thấy; đã sửa lỗi đếm dòng (ký tự ngắt trang) của chính script.
- CSV yêu cầu đầu vào: 16 cột đúng thứ tự, không ô rỗng. `ca-da-chay.csv`: 190 dòng, 30 ca, tất cả trong 30 ca dev RE2-TT.
- Thời gian chạy đo khi máy có nhiều phiên khác: không phải số chính thức.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM** (chi tiết `results/T-018/dinh-chinh-task-cu.md`):
- D1. T-002 `results/T-002/the-rcaeval.md:158-160`: mục "Rò nhãn" thiếu đường rò qua bộ cột. 12 cột latency/workload chỉ vắng ở đúng 4 ca, cả 4 có gốc ts-order-service; 23 cột `*_error` chỉ có ở 2–20 ca, có mặt tương quan với service gốc. Đã triển khai: đếm (`cot-re2tt/`), dùng bộ cột cố định L\* cho GDN.
- D2. T-001 `results/T-001/danh-sach-phuong-phap.md:191` (và `:91`): "chưa kiểm bảng của bài dùng chế độ nào" nay kiểm được: bài đặt ngưỡng theo tập kiểm định (như `report='val'`), nhưng code ở mọi chế độ chuẩn hóa điểm bằng thống kê của tập test; ngưỡng và điểm test ở hai thang khác nhau. Đã triển khai: biến thể chuẩn hóa theo tập kiểm định trong mọi phân tích.
- D3. T-005 `results/T-005/scripts/chuan_bi_dau_vao.py:122, 125-128`: bộ cột dùng cột của ca test; cột hằng chia cho 1. Không sai kết luận đo thời gian; rủi ro nếu P3 dùng lại (mô hình đúng dữ liệu đó báo động 11,2 % tick bình thường giữ ngoài).
- D4. T-001 mục 6–7: RCD, ε-Diagnosis, CIRCA của DecompRCA không phải bản RCAEval (PyRCA, CIRCA gốc có DA).

**E. Chỗ lệch khỏi SPEC và lý do** (SPEC "Thay đổi trong lúc làm" 1–9):
- Máy tải 100 % do nhiều phiên khác: đổi cơ sở phép kiểm seed/hoán vị từ 5 ca sang 1 ca (mục 1, 4); hủy rồi chạy lại lượt 5 ca khi máy rảnh (mục 6–8); lượt 10 ca ban đầu không chạy, sau chạy khi ước lượng dưới 1 giờ (mục 2, 9).
- R1 bị giới hạn 1 giờ dừng ở epoch 29/30 trước bước chấm; mô hình đã lưu trùng hệt T-005 nên phần chấm chạy riêng bằng `--chi-cham` (LOG).
- Thêm dữ liệu `re2tt5_daocot`, `lstar_n1_hoanvi` (mục 3, 4). `re2tt5_hoanvi`, `lstar_n5_hoanvi` đã dựng nhưng không chạy.
- Thêm phép chẩn đoán ngoài SPEC: bỏ cột hằng khi lấy max; đo lệch phân bố ở mức dữ liệu; giải thích ca bằng nhãn (sau khi có kết quả).
- Phải tải 30 file `inject_time.txt` (300 B) vì chỉ 1/30 ca dev có sẵn (LOG đính chính 09:10).

**F. Đề xuất cho tài liệu chung** (`results/T-018/de-xuat-tai-lieu-chung.md`): E1 WHY mới "cách chạy GDN ở chế độ b"; E2 WHY mới "báo Retrieval@K, Rerank@1 theo service ở P3"; E3 MRP P2 thêm đường rò qua bộ cột; E4 K1 §C.11 (code không cài đồ thị trước, top-k gồm chính nút); E5 LESSONS SL34 (câu phổ quát từ một thư mục; giờ ước đoán trong LOG); E6 MRP dòng 143 (không bắt buộc).

**G. Phần chưa kiểm và lý do.**
- Tái lập Bảng 2 bài GDN (SWaT, WADI): cần xin iTrust, OT đã bỏ khỏi phạm vi (Q-47). Giả định: code ở revision này cho đúng số bài. Sai nếu bảng sinh bằng `report='best'` hoặc cấu hình khác `run.sh`. Kiểm được khi có SWaT.
- P/R/F1 phát hiện của GDN trên RE2-TT: việc của P3 (prompt cấm benchmark). Hồ sơ chỉ có tính chất không cần nhãn và một ca giải thích.
- Độ nhạy theo w, theo k, theo tham số bài (β2 0,99; 50 epoch; patience 10): không chạy vì ngoài phạm vi hồ sơ (P3/P6). Giả định: kết luận về lệch mức không phụ thuộc w. Sai nếu lấy mẫu lại theo nhịp thật làm mô hình ổn định hơn. Kiểm được ở P3.
- Lệch đồng hồ giữa nguồn metric: không có chuẩn đo trong dữ liệu (chỉ một cột time đã căn). Kiểm được trên FlashTicket (P9/P10) nơi biết nguồn.
- Phương sai seed ở 5 ca chỉ có 2 seed; ở 10 ca chỉ 1 seed (mỗi lượt 10 ca khoảng 33 phút khi máy rảnh). Kết luận "nhiều dữ liệu thì ít báo động sai và ít phụ thuộc seed hơn" là xu hướng, chưa phải khoảng tin cậy. Mô hình 10 ca không báo động trên ca R-ca: chỉ một ca, đánh đổi phát hiện/báo động sai thuộc P3.
- Câu "0,57 so với 0,95" trong repo DecompRCA (K6): không chạy BARO trên RE1-SS vì prompt cấm benchmark ở phần DecompRCA; T-006 có bằng chứng ngược một phần. Kiểm được bằng một lượt BARO hai kiểu tiền xử lý (vài phút) nếu Minh cho phép.
- Số LLM của DecompRCA: cần API trả phí; phản hồi không được phát hành.
- RE1-TT (cột 241, Retrieval ngẫu nhiên): không có dữ liệu RE1-TT trên máy; tải là ngoài phạm vi cần thiết.
- Sơ đồ DK Train Ticket chứa đủ 5 service gốc (K13): không kiểm được là rò hay không nếu không có thí nghiệm LLM.
- Cách xử lý cột error (0 = không có lỗi) và cách chuẩn hóa bền: chỉ là đề xuất.

**H. Cần Minh quyết.**
1. Duyệt hay không các đề xuất E1–E6 (`de-xuat-tai-lieu-chung.md`) và đính chính D1–D4 (`dinh-chinh-task-cu.md`).
2. Có cho chạy BARO trên RE1-SS hai kiểu tiền xử lý để kiểm câu "0,57 so với 0,95" của repo DecompRCA không (vài phút, dữ liệu đã có).
3. Có đưa 30 file `inject_time.txt` đã tải (`D:\RCA-ext\work\T-018\nguon\rcaeval-inject\`) vào `data/rcaeval/` không (cần sửa `data/README.md`).
4. Ở G1: GDN chạy trên dataset nào, với dữ liệu bình thường lấy từ đâu (RE2-TT cần nhiều lượt chạy và xử lý lệch mức; Eadro có phiên bình thường riêng).

5. **Bước tiếp theo chính xác:** Minh mở phiên Codex, dán prompt phản biện ở cuối file này (lệnh `codex exec -s read-only -C D:\RCA-flashticket -o tasks\T-018-ho-so-gdn-decomprca\REVIEW.md "<prompt>"`). Sau khi có REVIEW.md: phiên Claude mới theo "Prompt cho người làm phản hồi phản biện" của `docs/review-prompt.md`. Chạy lại toàn bộ: thứ tự lệnh ở đầu từng script trong `results/T-018/scripts/` (tai_moc_tiem → chuan_bi_gdn → tao_bien_the → chay_nen.sh/chay_gdn → tinh_tay_gdn → phan_tich_gdn → giai_thich_ca → dem_cot, chan_doan_lech_phan_bo, retrieval_ngau_nhien → tao_yeu_cau_dau_vao, tao_ca_da_chay → kiem_dan_dong).

6. **Lệnh cuối cùng đã chạy:** `git diff docs/STATE.md` (kiểm STATE chỉ thêm dòng T-018), sau `py -3 results/T-018/scripts/kiem_dan_dong.py > results/T-018/runs/kiem-dan-dong.txt`.

---

## Prompt phản biện cho agent còn lại

Minh dán nguyên văn vào phiên Codex mới (chế độ chỉ đọc), ví dụ:
`codex exec -s read-only -C D:\RCA-flashticket -o tasks\T-018-ho-so-gdn-decomprca\REVIEW.md "<prompt>"`

```text
Bạn là người phản biện độc lập cho task T-018 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-018-ho-so-gdn-decomprca/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-018-ho-so-gdn-decomprca/SPEC.md, tasks/T-018-ho-so-gdn-decomprca/LOG.md, các file đầu ra:
results/T-018/ho-so-gdn.md, results/T-018/decomprca.md, results/T-018/yeu-cau-dau-vao.csv, results/T-018/ca-da-chay.csv,
results/T-018/dinh-chinh-task-cu.md, results/T-018/de-xuat-tai-lieu-chung.md, results/T-018/moi-truong.md, results/T-018/nguon-tai.md,
results/T-018/cot-re2tt/ (ca.csv, cot.csv, loai.csv, cot-khong-du-30-ca.csv, tom-tat.json),
results/T-018/runs/ (b3-chuan-bi.json, b5-giai-thich-ca.json, b6-lech-phan-bo.json, b6b7-phan-tich.json, b9-retrieval-ngau-nhien.json, kiem-dan-dong.txt, r1s-re2tt5-cham-tinh-tay.json, tai-moc-tiem.json, và mọi file .log, .txt khác trong thư mục),
results/T-018/scripts/ (mọi file),
và các file ngoài repo do task tạo: D:\RCA-ext\work\T-018\nguon\ (decomprca-2609.36686v1.pdf, gdn-2106.06947.pdf, decomprca.txt, gdn.txt, DecompRCA\ ở commit f99d2172ad3ba1d584d947c075d69fc9bbc09064, rcaeval-inject\), D:\RCA-ext\work\T-018\gdn\data\ (các bộ dữ liệu GDN đã dựng), D:\RCA-ext\work\T-018\gdn\runs\ (mô hình và mảng của từng lượt),
và kết quả `git diff <commit gốc>` nếu có: không có (file của task chưa commit; phạm vi là danh sách file ở trên, không dùng git diff).
Code đối chiếu: GDN ở D:\RCA-ext\src\GDN (revision 9853899da860682669a134e4af315d036aab4eca), RCAEval ở D:\RCA-ext\src\RCAEval (HEAD 259ea41; commit fb8f20a6 cho main-ase.py). Môi trường chạy GDN: D:\RCA-ext\envs\py38-gdn; dựng dữ liệu: D:\RCA-ext\envs\py312. Cách chạy từng script ghi ở đầu file script.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```

---

## Phiên 2 — 04/10/2026 — Claude (Opus 5.5) — laptop Windows 11 — vai trò: người làm, bước 7 (phản hồi phản biện)

**Mở phiên:** 18:31. Đã đọc AGENTS (mục 5 bước 7, mục 9), `docs/review-prompt.md` (prompt phản hồi), STATE (T-018 "chờ phản biện"). REVIEW.md đã có. HEAD `93f13d4`.

**Việc 1 — tự soát độc lập, TRƯỚC khi mở REVIEW.md** (đọc lại SPEC, LOG, đầu ra; điểm tự tìm):
- S1. `ho-so-gdn.md` mục 9.5 gọi Eadro là "ứng viên tốt nhất cho GDN" chỉ dựa vào câu "có phiên bình thường riêng" của thẻ T-009; độ dài, bộ cột, độ sạch chưa kiểm. Kết luận mạnh hơn bằng chứng (không chặn; nên hạ thành "ứng viên cần kiểm").
- S2. `de-xuat-tai-lieu-chung.md` E1 đề xuất ghi WHY "chọn" cách chạy chế độ b, trong khi chính kết quả cho thấy cách đó báo động sai 45–100 % tick bình thường. Đề xuất "chọn" khi bằng chứng ngược chiều (không chặn; nên đổi thành "ứng viên, chưa đạt").
- S3. LOG các dòng 08:35–09:22 dùng giờ ước đoán (đã đính chính trong LOG; không ảnh hưởng số).
- S4. Bảng 9.4: so 1/5/10 ca lẫn độ đa dạng ca (đã ghi ở SPEC); 10 ca chỉ 1 seed, mà kết luận ở mục 0 viết "10 ca khoảng 5 %" như mức ổn định (không chặn; thêm "1 lượt").
- S5. Mục 7.4: 41 báo động sau mốc đều có cột đầu ngoài service gốc; câu "có thể là triệu chứng lan" đã ghi chưa kiểm — giữ.
- S6. Không thấy nhãn lọt vào phương pháp: mốc tiêm chỉ dùng cắt dữ liệu học (G8, đã khai) và chấm; tên ca chỉ dùng sau khi có kết quả.

**Việc 2 — đánh giá từng điểm của REVIEW.md** (kiểm trên file thật: `process_swat.py`, `gdn.txt:339–343`, `decomprca.txt:1272–1279`, RCAEval `main.py:320–330`, `io/time_series.py`, SPEC dòng 29):
- R1 đúng; R2 đúng; R3 đúng; R4 đúng (tôi chép chú thích code mà không kiểm đường xử lý); R5 đúng (vượt SPEC tự viết, không vượt prompt); R6 đúng một phần (prompt quy định "(chờ WHY…)", nhưng E1 viết như đã chọn). Không điểm nào làm sai số đã tính. Chi tiết ở bảng cuối REVIEW.md. Thêm N1 (Eadro "tốt nhất" quá tay), N2 (10 ca chỉ 1 lượt).

**Đề xuất sửa, gom theo file** (chưa sửa; chờ Minh quyết):
- `results/T-018/ho-so-gdn.md`: dòng 27 bỏ "Bài ghi cùng các bước", nêu khác biệt gộp nhãn (max so với phổ biến nhất); mục 5 thêm dòng 11 (gộp nhãn); mục 8.1 thêm đường `test.fillna(test.mean())` của script mẫu; mục 9.5 hạ Eadro thành "ứng viên cần kiểm" (N1); mục 0 và 9.4 thêm "1 lượt, 1 seed" cho số 10 ca (N2).
- `results/T-018/decomprca.md`: dòng 44 giới hạn vào các thiết lập chính, thêm ngoại lệ CIRCA-FCI trên pool ngẫu nhiên có dùng nhãn (R2); dòng 73 ghi Bảng 4 là đối chứng dùng nhãn; dòng 96 thay bằng câu của reviewer (R3); dòng 72 bỏ câu "đúng số ứng viên sau tiền xử lý", ghi mức ngẫu nhiên phải theo tập ứng viên thực dùng (R4); K9 ghi nguồn số là đọc toàn dữ liệu RE1, vượt SPEC (R5).
- `results/T-018/de-xuat-tai-lieu-chung.md`: E1 đổi từ "chọn" sang "ứng viên, chưa đạt"; tách lý do của phép chẩn đoán T-018 khỏi cấu hình P3 (R6, S2).
- `tasks/T-018-ho-so-gdn-decomprca/SPEC.md`: thêm mục 10 "Thay đổi trong lúc làm" ghi độ lệch đọc dữ liệu RE1 ở B9 (R5).

**Kết thúc phiên 2:**
1. Đã làm: tự soát độc lập (S1–S6, ghi trước khi mở REVIEW); kiểm chứng R1–R6 trên file thật; điền bảng phản hồi.
2. File đã thay đổi: `tasks/T-018-ho-so-gdn-decomprca/REVIEW.md` (chỉ bảng cuối), `LOG.md` (mục này).
3. Kiểm tra: đọc lại các dòng code/PDF reviewer dẫn; mọi bằng chứng khớp.
4. Cần Minh quyết: cột "Minh quyết" của R1–R6, N1, N2; có dùng số 0,816/0,901 (R5) không; WHY cho phép chẩn đoán (R6).
5. Bước tiếp theo: Minh duyệt danh sách sửa trên; nếu duyệt, phiên người làm sửa đúng các file đã nêu rồi đổi STATE.
6. Lệnh cuối: cập nhật bảng REVIEW.md và LOG.md.

---

## Phiên 3 — 04/10/2026 — Claude (Opus 5.5) — laptop — vai trò: người làm, bước 8 (sửa theo phản biện)

**Mở phiên:** 18:50. **Quyết định của Minh trong phiên** (nguyên lời): "duyệt sửa đổi, nếu còn tồn đọng thì báo lại, không thì đóng task". Phạm vi duyệt: danh sách "Đề xuất sửa, gom theo file" của phiên 2. Cần ghi vào DECISIONS (đề xuất dòng ở báo cáo cuối phiên; chưa ghi vì DECISIONS cần Minh duyệt dòng ghi).

**Diễn biến:**
- Sửa `results/T-018/ho-so-gdn.md`: dòng 27 (gộp nhãn max/phổ biến nhất, điền ô thiếu bằng trung bình test; R1), mục 5 thêm dòng 11 (R1), mục 8.1 thêm G10 (R1), mục 9.5 hạ Eadro thành "ứng viên cần kiểm" (N1), mục 0 và 9.4 thêm "1 lượt, 1 seed" (N2).
- Sửa `results/T-018/decomprca.md`: kết luận đồ thị giới hạn vào thiết lập chính + ngoại lệ CIRCA-FCI 0,400 (R2); ghi Bảng 4 dùng nhãn (R2); câu G1 về lan truyền (R3); bỏ khẳng định về `--report-chance` (R4); K9 ghi rõ nguồn số vượt SPEC (R5).
- Sửa `results/T-018/de-xuat-tai-lieu-chung.md`: E1 đổi thành "lý do của phép chẩn đoán T-018, chưa đạt, không phải cấu hình P3" (R6).
- SPEC thêm "Thay đổi trong lúc làm" mục 10 (R5). REVIEW.md: cột "Minh quyết" = "Duyệt sửa (04/10)" cho R1–R6, N1–N2.
- Kiểm: `scripts/kiem_dan_dong.py` chạy lại, 0 file không tìm thấy; dẫn `controlled_pools.py:61-107` đúng hàm chèn nguyên nhân. Không chạy lại thuật toán (không thay đổi nào cần).

**Kết thúc phiên 3:**
1. Đã làm: sửa đúng danh sách đã duyệt; không thêm gì ngoài danh sách.
2. File đã thay đổi: `results/T-018/ho-so-gdn.md`, `decomprca.md`, `de-xuat-tai-lieu-chung.md`, `runs/kiem-dan-dong.txt`; `tasks/T-018-ho-so-gdn-decomprca/SPEC.md`, `REVIEW.md` (cột Minh quyết), `LOG.md`; dòng T-018 trong `docs/STATE.md`.
3. Kiểm tra: kiểm dẫn dòng đạt; mọi số giữ nguyên.
4. Tồn đọng chờ Minh (ngoài phạm vi ghi của task, nên chưa đóng): (a) áp dụng hay không E1–E6 vào tài liệu chung và đính chính D1–D4 vào file task cũ; (b) dòng DECISIONS cho quyết định phiên 3; (c) commit.
5. Bước tiếp theo: Minh quyết (a)–(c); nếu không cần áp dụng gì thêm, chuyển STATE T-018 thành "Xong".
6. Lệnh cuối: `py -3 results/T-018/scripts/kiem_dan_dong.py > results/T-018/runs/kiem-dan-dong.txt`.

---

## Phiên 4 — 04/10/2026 — Claude — vai trò: người làm, đóng task

**Quyết định của Minh** (nguyên lời): "duyệt đề xuất và sửa đổi, nếu còn tồn đọng thì báo lại, không thì đóng task". Áp dụng theo khuyến nghị đã trình: E1 (chỉ lý do chẩn đoán), E3, E4, E5 thu gọn, D1, D2, D4; E2 để G1; bỏ E6, D3. Đã ghi DECISIONS Q-56.

**Diễn biến:**
- WHY-17, SL34 đã bị phiên khác dùng → ghi WHY-18 (lý do phép chẩn đoán GDN, trạng thái "chưa đạt", không phải cấu hình P3) và SL35. Thêm Q-56 vào DECISIONS.
- `docs/MRP.md` (P2, kiểm rò nhãn: thêm đường rò qua bộ cột), `docs/knowledge/K1-phuong-phap-rca.md` §C.11, `docs/LESSONS.md` SL35.
- File task cũ: `results/T-002/the-rcaeval.md:160` (D1), `results/T-001/danh-sach-phuong-phap.md` dòng 91, 191 (D2) và chú thích mục 6 (D4).
- Sự cố đã xử lý: lần ghi đầu đổi ký tự xuống dòng của T-001 làm `git diff` hiện toàn file; đã đưa về LF như HEAD, diff còn đúng 3 dòng của T-018 (3 dòng SimpleRCA/L4 khác trong diff là của phiên T-017, không động tới).
- Mọi file chung đọc lại ngay trước khi ghi, sửa bằng thay chuỗi chính xác (không ghi đè cả file nội dung khác).

**Kết thúc phiên 4:**
1. Đã làm: áp dụng đề xuất đã duyệt; đóng task.
2. File đã thay đổi: `docs/WHY.md`, `docs/MRP.md`, `docs/knowledge/K1-phuong-phap-rca.md`, `docs/LESSONS.md`, `docs/DECISIONS.md`, `results/T-001/danh-sach-phuong-phap.md`, `results/T-002/the-rcaeval.md`, dòng T-018 trong `docs/STATE.md`, LOG này.
3. Kiểm tra: `git diff --stat` từng file; chỉ thay đổi dự định.
4. Tồn đọng: không còn việc của T-018. E2 (báo Retrieval@K/Rerank@1) chuyển sang quyết định ở G1. Chưa commit (chờ Minh yêu cầu).
5. Bước tiếp theo: commit khi Minh duyệt; đề xuất nội dung commit ở báo cáo cuối.
6. Lệnh cuối: `git diff --stat docs/ results/T-001 results/T-002`.
