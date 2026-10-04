# Tính ngẫu nhiên của TORAI và RCD

T-016, yêu cầu 4. Nguồn số: `runs/s3*-*.json`, `runs/s11-linux-vs-win-*.json`, `runs/s8-so-hoan-vi.txt`, `cham/s7-tong-hop.json`, `cham/s10-tong-hop.json`, `cham/s11-rcd-*`, `runs/s11b-so-rcd-ss.txt`.

## 1. Nguồn ngẫu nhiên

| Nguồn | Nơi | Có seed không | Ghi chú |
|---|---|---|---|
| Hoán vị cột trước khi chia khối γ = 5 | `RE:rcd.py:309` `np.random.permutation` | không (bộ sinh toàn cục của numpy) | đổi khối → đổi tập điều kiện của phép kiểm CI → đổi hàng xóm F |
| Thứ tự duyệt hàng xóm của F ở mỗi độ sâu | `RE:lib/causallearn/utils/PCUtils/SkeletonDiscovery.py:183` | không | thứ tự duyệt quyết định cạnh nào bị bỏ trước |
| GMM (chọn số cụm, gán cụm) | `RE:torai.py:243-261` | **có**, `random_state=0` | dùng bộ sinh riêng, không đụng bộ sinh toàn cục |
| K-means 1 chiều khi rời rạc hóa | `KBinsDiscretizer` (sklearn 1.2.2) | không cần: tâm khởi tạo cố định, `n_init=1` | tất định; script tính tay tái lập đúng (`runs/s12-kiem-kmeans.txt`) |

- `torai()` không có tham số seed. `rcd()` có `seed=None` (`rcd.py:458, 486-487`); `main.py` không truyền. Dòng `# np.random.seed(0)` ở `rcd.py:294` bị tắt.
- RCD gốc luôn đặt `np.random.seed(420)` (`RCDg:rcd.py:13, 117`).
- Vì không đặt seed, mỗi lần chạy `main.py` cho kết quả khác; ở T-006, ba lần TORAI trên torai-OB giống lần 1 ở 86/90 và 84/90 ca (`results/T-006/kiem-dung-dan.md` mục 7).

## 2. Đặt seed thế nào trong task này (lý do: `docs/WHY.md` WHY-20)

Harness gọi `np.random.seed(s)` **ngay trước mỗi lời gọi phương pháp, cho từng ca** (`scripts/chay_torai.py`). Nhờ vậy kết quả mỗi ca không phụ thuộc thứ tự ca hay số ca đã chạy trước. Đây là cùng cơ chế với tham số `seed` của `rcd()`; không đổi phương pháp.

## 3. Tất định khi cố định seed (đã kiểm)

| Phép kiểm | Kết quả | File |
|---|---|---|
| `main.py` nguyên văn (chỉ chèn seed) và harness, seed 0, TORAI OB cửa sổ 10 | 90/90 ca giống hệt | `runs/s3a-main-vs-harness.json` |
| Harness bật/tắt thu giá trị trung gian | 90/90 | `runs/s3b-thuthap.json` |
| Chạy lại cùng seed | 90/90 | `runs/s3c-lan2.json` |
| `PYTHONHASHSEED=12345` | 90/90 | `runs/s3d-pythonhashseed.json` |
| Linux (EC2) và Windows (laptop), cùng seed 0: TORAI gốc, sửa × OB, SS, TT dev cửa sổ 10 | 90/90 mỗi cặp OB, SS; 30/30 TT | `runs/s11-linux-vs-win-*.json` |
| RCD torai-SS cửa sổ 10 seed 0, Linux và Windows | 90/90 ca giống hệt | `runs/s11-linux-vs-win-rcd-ss-len10.json`, `runs/s11b-so-rcd-ss.txt` |

Kết luận: với cùng seed, cùng gói (`runs/s11-so-goi-laptop-ec2.txt`), TORAI và RCD tất định, kể cả qua hai hệ điều hành.

## 4. Dao động giữa các seed (TORAI)

Seed 0–4 với OB, SS; 0–2 với TT dev (luật chọn N ở SPEC, LOG 11:05 và 12:10):

| Cấu hình | Số seed | Ca có thứ hạng khác giữa các seed | Ca có top-1 khác | AC@1 [min, max] | Avg@5 sd |
|---|---|---|---|---|---|
| OB gốc 10 | 5 | 8 / 90 | 0 | [0,778; 0,778] | 0,000 |
| OB sửa 10 | 5 | 24 / 90 | 6 | [0,756; 0,778] | 0,003 |
| OB gốc 20 | 5 | 20 / 90 | 2 | [0,811; 0,822] | 0,002 |
| OB sửa 20 | 5 | 21 / 90 | 2 | [0,811; 0,822] | 0,004 |
| OB gốc 10, M+L | 5 | 6 / 90 | 2 | [0,778; 0,789] | 0,001 |
| OB sửa 10, M+L | 5 | 14 / 90 | 9 | [0,778; 0,800] | 0,004 |
| SS gốc 10 | 5 | 5 / 90 | 2 | [0,844; 0,856] | 0,001 |
| SS sửa 10 | 5 | 12 / 90 | 5 | [0,844; 0,867] | 0,003 |
| SS gốc 20 | 5 | 14 / 90 | 5 | [0,833; 0,844] | 0,001 |
| SS sửa 20 | 5 | 14 / 90 | 6 | [0,811; 0,844] | 0,003 |
| TT gốc 10 | 3 | 0 / 30 | 0 | [0,700; 0,700] | 0,000 |
| TT sửa 10 | 3 | 4 / 30 | 0 | [0,700; 0,700] | 0,000 |
| TT gốc 20 | 3 | 4 / 30 | 3 | [0,733; 0,733] | 0,000 |
| TT sửa 20 | 3 | 8 / 30 | 1 | [0,733; 0,733] | 0,000 |

Đọc bảng:
- Dao động ở mức AVERAGE nhỏ (sd Avg@5 ≤ 0,004), vì phần lớn cụm rơi nhánh dự phòng (tất định). Bản sửa dao động nhiều hơn bản gốc vì RCD có metric, tìm được hàng xóm F nhiều hơn, nên thứ tự ngẫu nhiên có ảnh hưởng hơn.
- Ở mức từng ca, dao động không nhỏ: tới 24/90 ca đổi thứ hạng, 9/90 ca đổi top-1. Phân tích từng ca ở P4 phải dùng nhiều seed, không dựa vào một lần chạy.
- Sai lệch so với số công bố (mục 5 `giam-mau-hai-lan.md`) nằm trong khoảng 0,000–0,021, lớn hơn sd giữa seed. Bài lấy trung bình 5 lần (§4.2) với seed không rõ.

**Thứ tự cột** (`runs/s8-so-hoan-vi.txt`): hoán vị cố định (seed hoán vị 12345) cột metric, logts, tracets, cùng seed phương pháp: vectơ mức nghiêm trọng và phân cụm không đổi ở 90/90 ca mọi seed; thứ hạng cuối đổi 2–14/90 ca, top-1 đổi 0–4/90. Thứ tự cột chỉ tác động qua chuỗi số ngẫu nhiên của RCD; mức đổi ngang mức đổi giữa các seed.

## 5. RCD (biến thể)

- RCD không đặt seed; T-006 chạy 3 lần không seed: torai-OB cửa sổ 10 AVERAGE Avg@5 0,658 / 0,702 / 0,671; torai-SS 0,540 / 0,518 / 0,542; chỉ 2–6/90 ca có thứ hạng giống nhau giữa các lần (`results/T-006/kiem-dung-dan.md` mục 6). Dao động của RCD lớn hơn TORAI nhiều, vì mọi thứ hạng đều từ RCD (không có nhánh dự phòng).
- Có seed: RCD torai-SS cửa sổ 10, seed 0: Linux và Windows cho thứ hạng giống hệt 90/90 ca, Avg@5 0,553 (`runs/s11-linux-vs-win-rcd-ss-len10.json`, `diem-mo-t006.md` mục 2). Tức RCD cũng tất định khi cố định seed.

## 6. Đề xuất cho P3 (chưa kiểm ngoài số trên)

- Đặt seed theo ca như harness; báo seed trong kết quả.
- TORAI: ít nhất 3 seed; báo trung bình và khoảng. RCD: ít nhất 5 seed (dao động lớn hơn), hoặc báo rõ chỉ một seed.
- Phân tích từng ca (P4) dùng thứ hạng của mọi seed; một ca chỉ coi là "sai ổn định" khi sai ở mọi seed.
