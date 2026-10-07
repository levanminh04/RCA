# T-025 — Chi phí chạy chế độ (b)

Ngày 07/10/2026. Người làm: Claude. **Mọi số là của EC2**, không phải laptop. Theo Q-72, kết luận chi phí BOCPD ở đây là của **bản cài BARO** (`baro/_bocpd.py` e35f4ec, gọi như `reproducibility.py:161–166`), không phải của thuật toán BOCPD nói chung.

Máy (LOG T-025 phiên 1):
- Máy một `ip-172-31-38-238` (EC2 của T-031): 2 vCPU, RAM 7,6 GB; chạy BOCPD (21:51–00:11 giờ laptop, 06–07/10) rồi RCA tại t̂ của BOCPD (07:24–07:59, 07/10). Model CPU không ghi trong T-025.
- Máy hai `ip-172-31-33-115` (EC2 của T-007): 2 vCPU = 1 lõi Xeon Platinum 8488C, RAM 7,6 GB; chạy N-Sigma hai tập và RCA tại t̂ của N-Sigma (22:50–23:40, 06/10).
- Hai máy cùng phiên bản gói (`runs/ec2-may1/runs/freeze-main-rca.txt` giống hệt `runs/ec2-may2/…`).
- Thời gian là wall của tiến trình con, đo bởi runner `src/p3/runner.py` (`cost.wall_s`). Mỗi lượt chạy tuần tự, một tiến trình.

## 1. BOCPD, 30 ca × 1.441 điểm (máy một)

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Tổng 30 ca | 8.418,6 s ≈ 2,34 giờ | `cham/phan-tich-b.json` → `chi_phi.bocpd.tong_s`; `runs/bocpd-ec2-001/ket-thuc.json` |
| Mỗi ca: trung bình (min–max) | 280,6 s (205,8–380,2 s) | `chi_phi.bocpd.tb_s`, `min_s`, `max_s` |
| RSS đỉnh lớn nhất | 321,6 MB | `chi_phi.bocpd.rss_max_mb` |
| Số cột d sau tiền xử lý | 22–39, tổng 896 | `chi_phi.bocpd.d` |
| Hồi quy wall theo d | wall ≈ 9,65 s × d − 7,6 s; hệ số tương quan 0,987 | `chi_phi.bocpd.hoi_quy_wall_theo_d` |
| wall / d | 8,85–9,75 s mỗi cột | `chi_phi.bocpd.wall_chia_d` |
| wall / d² | 0,25–0,44 s | `chi_phi.bocpd.wall_chia_d2` |
| `TIMEOUT` khai trước | 21.600 s/ca; ca dài nhất dùng 1,8 % | SPEC T-025; `max_s` |
| Trạng thái | 30 OK, 0 ERROR, 0 TIMEOUT | `runs/bocpd-ec2-001/ket-thuc.json` |

**So với chiếu laptop của T-031** (`results/T-031/do-chi-phi.md` §5, chưa kiểm khi viết):

| | Laptop, chiếu T-031 | EC2, đo T-025 |
|---|---|---|
| 30 ca | 34,7 giờ (d², T²); 23,1 giờ (d^q, T²); khoảng hợp lý 8–35 giờ; H1 (∝ d²) ≈ 16,7 giờ; H2 (gần như không phụ thuộc d) ≈ 8,2 giờ | 2,34 giờ |
| Ca lớn nhất (d = 39) | 2.949–3.368 s | 380,2 s (`dev-4f8a844308`; `chi_phi.bocpd.theo_ca`) |

Đọc: trên EC2, wall gần tỉ lệ thuận với d (wall/d gần hằng, wall/d² đổi gần 2 lần), nên dữ liệu EC2 không khớp H1 (∝ d²) cũng không khớp H2 (không phụ thuộc d). **Chưa kiểm:** cơ chế (vì sao bậc 1 theo d), và H1/H2 có đúng trên laptop không, vì không chạy đủ ca nào trên laptop. Hai máy khác nhau: cùng một lời gọi tiền tố T = 150, d = 22 mất 12,1 s trên laptop và 2,2 s trên EC2 (`runs/bocpd-r-tien-to-laptop-001/ket-thuc.json`, `runs/bocpd-r-tien-to-ec2-001/ket-thuc.json` → `tom_tat.giay`), tức EC2 nhanh ≈ 5,5 lần ở phép đo đó; T-031 §5 đã thấy laptop có lúc chậm ≈ 3 lần, nên tỉ lệ này không dùng để quy đổi.

**Nhiễu đã biết:** lúc 22:50 giờ laptop (15:50 UTC) chép 627 MB dữ liệu từ máy một sang máy hai trong ≈ 7 s. Theo `runs/bocpd-ec2-001/tien-do.txt` (dòng 27–28), lúc đó ca `dev-57546fd87b` vừa kết thúc (15:50:42Z) và ca `dev-59f696a169` bắt đầu. Đính chính LOG phiên 1 22:50, ghi là "ca `dev-4f8a844308` hoặc ca kế": sai ca. Hai ca này có wall/d 9,34 và 9,34 s, nằm trong khoảng 8,85–9,75 của 30 ca (`chi_phi.bocpd.theo_ca`), nên ảnh hưởng không thấy được.

## 2. N-Sigma (máy hai)

| | Tổng 30 ca | Mỗi ca (min–max) | RSS đỉnh | Chiếu laptop T-031 | Nguồn |
|---|---|---|---|---|---|
| Tập chính (tập BOCPD) | 164,2 s | 4,4–6,5 s | 188,4 MB | 216 s | `cham/phan-tich-b.json` → `chi_phi.nsigma`; `results/T-031/do-chi-phi.md` §4 |
| Đối chứng (mọi cột) | 1.041,8 s | 32,8–35,9 s | 196,8 MB | 3.084 s | `chi_phi.nsigma_doi_chung`; như trên |

## 3. RCA tại t̂

Một lượt = một ca × một ranker × một seed. CIRCA: hai biến thể (RHT+DA, RHT-only) cùng một lượt, đếm một lần. Nguồn: `cham/phan-tich-b.json` → `chi_phi.rca_bocpd`, `chi_phi.rca_nsigma`; tổng lượt: `runs/rca-*/ket-thuc.json`.

| Ranker | t̂ BOCPD, máy một: tổng / trung bình mỗi lượt | t̂ N-Sigma, máy hai: tổng / trung bình |
|---|---|---|
| BARO (30 lượt) | 253,7 s / 8,5 s | 227,1 s / 7,6 s |
| CIRCA OLS (30 lượt) | 193,4 s / 6,4 s | 164,0 s / 5,5 s |
| TORAI B (90 lượt) | 1.658,0 s / 18,4 s | 1.431,4 s / 15,9 s |
| Cả lượt chạy | 2.106,7 s | 1.824,0 s |

TORAI B ở chế độ (a) trên EC2 (T-031): 1.635 s cho 90 lượt (`results/T-031/do-chi-phi.md` §3). SPEC T-025 chiếu TORAI trên laptop 25–88 s/lượt; trên EC2 là 12,4–22,5 s/lượt (`min_s`, `max_s`). Không lượt RCA nào gần `TIMEOUT` 3.600 s.

## 4. Thời gian chờ thực tế

- BOCPD: 14:50:47–17:11:06 UTC ngày 06/10 (`runs/ec2-may1/trang-thai.txt`).
- Chuỗi máy một kẹt ≈ 7 giờ sau khi BOCPD xong do lỗi script chờ (`tmux has-session` khớp tiền tố; LOG phiên 1, 07:23). Lỗi không ảnh hưởng số; RCA tại t̂ của BOCPD chạy 00:24–00:59 UTC ngày 07/10.
- Laptop chỉ chạy việc nhẹ: kiểm hash, chốt danh sách, evaluator (≈ 15 s một lượt), tính lại độc lập (≈ 1 s).
