# Hai điểm còn mở của T-006 (mục 11, điểm 3 và 5)

T-016, yêu cầu 6. Trong giới hạn Q-40 (mỗi phương pháp trên mỗi dataset tối đa 3 giờ chờ, chạy tuần tự).

## 1. Điểm 3 — RCD torai-OB cửa sổ 20 chỉ chạy được 46/90 ca

**Làm gì.** Chạy RCD (RCAEval `259ea41`, `rcd()`) trên torai-OB, `--length 20`, seed 0, trên EC2 (Linux, máy chỉ chạy một tiến trình này; trước khối có tiến trình T-014 thì chờ). Thứ tự ca chốt trước khi chạy (`runs/s11-thu-tu-rcd-ob-len20.txt`): 44 ca T-006 chưa chạy được trước, 46 ca còn lại sau; trần 3 giờ.

**Kết quả** (`cham/s11-rcd-ob-len20.json`, `runs/s11-rcd-ob-len20-so-t006.txt`):
- Chạy đủ **90/90 ca trong 5 624 s** (1,56 giờ), 0 lỗi, 0 rỗng; độ dài đầu ra 2–25 metric. Ca lâu nhất `emailservice_loss_2` 2 370 s; 44 ca T-006 chưa chạy tốn 3 873 s, 46 ca kia 1 750 s.
- AVERAGE (mức service): AC@1 0,644; AC@3 0,778; **Avg@5 0,742**. Bảng 2 bài TORAI, dòng Metric/RCD: 0,59 / 0,80 / **0,74**. Lệch Avg@5 +0,002 (đạt tiêu chí ≤ 0,05 của T-006).
- Theo lỗi, Avg@5 của mình / bài: CPU 0,933 / 0,94; MEM 0,613 / 0,81 (−0,197); DISK 0,920 / 0,81 (+0,110); SOCKET 0,920 / 0,91; DELAY 0,680 / 0,52 (+0,160); LOSS 0,387 / 0,44. AVERAGE khớp nhưng từng ô lệch lớn theo cả hai chiều; với 1 seed và dao động lớn của RCD (mục 3 `ngau-nhien.md`), không phân xử được ô nào lệch do cấu hình, ô nào do ngẫu nhiên.
- 46 ca chung với T-006: EC2 0,865; T-006 laptop 3 lần 0,839 / 0,896 / 0,835 (TB 0,857). EC2 nằm trong khoảng 3 lần của T-006. 44 ca còn lại: 0,614. Tức 46 ca của T-006 dễ hơn trung bình, đúng như T-006 cảnh báo.

**Hệ quả cho câu hỏi cửa sổ của bài (T-006 mục 2.1):** ở torai-OB, cửa sổ 20 tái lập AVERAGE của RCD (0,742 so với 0,74), cửa sổ 10 thì không (0,677, T-006). Ở torai-SS, cả cửa sổ 10 (0,533, T-006 TB 3 lần; 0,553 seed 0 ở đây) lẫn 20 (0,664, T-006) đều không tái lập 0,57. Bằng chứng vẫn mâu thuẫn giữa hai dataset; quyết định cửa sổ P3 ở G1 (Q-54) không nên dựa vào RCD.

**Giới hạn:** 1 lần chạy. Chạy thêm 2 seed tốn khoảng 3,1 giờ, vượt ngân sách Q-40 còn lại của RCD trên torai-OB (task này đã dùng 1,56 giờ; T-006 đã dùng 3 × 3 giờ trước đó). Không chạy.

## 2. Điểm 5 — chạy lại trên Linux

**Làm gì.** Dựng môi trường Python 3.8 riêng trên EC2 (`moi-truong.md` mục 3; cùng phiên bản mọi gói được nạp, `runs/s11-so-goi-laptop-ec2.txt`). Chạy cùng cấu hình, **cùng seed 0** trên Linux và Windows, so từng ca.

| Phương pháp, dataset, cửa sổ | Linux (EC2) / Windows (laptop) | Thứ hạng từng ca | File |
|---|---|---|---|
| TORAI gốc, torai-OB, 10 | 90 / 90 ca | **giống hệt 90/90** | `runs/s11-linux-vs-win-torai-goc-ob-len10.json` |
| TORAI gốc, torai-SS, 10 | 90 / 90 | giống hệt 90/90 | `…-torai-goc-ss-len10.json` |
| TORAI sửa, torai-OB, 10 | 90 / 90 | giống hệt 90/90 | `…-torai-sua-ob-len10.json` |
| TORAI sửa, torai-SS, 10 | 90 / 90 | giống hệt 90/90 | `…-torai-sua-ss-len10.json` |
| TORAI gốc, sửa, TT 30 ca dev, 10 | 30 / 30 | giống hệt 30/30 | `…-tt30-torai-{goc,sua}-len10.json` |
| RCD, torai-SS, 10 | 90 / 90 | **giống hệt 90/90**; Avg@5 0,553 cả hai | `runs/s11-linux-vs-win-rcd-ss-len10.json`, `runs/s11b-so-rcd-ss.txt` |

**Kết luận:** với cùng seed và cùng bộ gói, hệ điều hành không đổi kết quả của TORAI và RCD. "Windows thay vì Linux" bị loại khỏi danh sách nguyên nhân khả thi của phần lệch so với bài (T-006 mục 6, 10). Phần lệch còn lại của RCD vẫn có thể do: seed (tác giả không công bố), cấu hình cửa sổ khác giữa các dataset, hoặc cấu hình khác bài không ghi.

**Phạm vi:** CIRCA (cũng là ứng viên của điểm 5) thuộc T-014, không chạy ở đây. Python bản vá khác nhau (3.8.20 trên EC2, 3.8.10 trên laptop); không ảnh hưởng ở các phép so trên.

## 3. Chi phí đã dùng

| Lượt | Máy | Thời gian |
|---|---|---|
| RCD torai-OB cửa sổ 20, 90 ca | EC2 | 5 624 s |
| RCD torai-SS cửa sổ 10, 90 ca | EC2 | 703 s |
| RCD torai-SS cửa sổ 10, 90 ca | laptop (có phiên khác chạy cùng) | 1 934 s |
| TORAI gốc, sửa × OB, SS, cửa sổ 10, TT 1 ca | EC2 | 19–38 s mỗi khối 90 ca |

Thời gian chính thức (máy chỉ chạy tiến trình này): các dòng EC2. Bảng 8 bài TORAI ghi RCD 3,91 s/ca (OB) và 2,96 s/ca (SS); ở đây 62,5 s/ca (OB, cửa sổ 20) và 7,8 s/ca (SS, cửa sổ 10) — chậm hơn nhiều lần; nguyên nhân chưa kiểm (bài không ghi cửa sổ, máy 8 CPU).
