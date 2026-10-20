
### Phiên 12 (tiếp) — ba phép kiểm laptop xong: KT-3, KT-8 (nửa MicroRank), KT-15; báo cáo đã cập nhật (11/10/2026, 11:41Z = 18:41 +07)

Mục này nối tiếp mục "Minh duyệt các phép kiểm chạy trên laptop" ngay trên. T-032 vẫn **chờ phản biện**.

**1. Đã làm.**

- KT-3 và KT-8 (nửa MicroRank): lượt `runs/microrank-kt3-001` xong lúc 11:37:35Z: COMPLETE, 260/260 tiến trình con, 1.173 giây, RAM hệ thống đỉnh 73,5%, không lần chờ RAM hay giết nào. Tổng hợp: `runs/microrank-kt3-001/collect-001/summary.json` (sha256 9e2f6bb2…).
- KT-15: `runs/circa-da-addition-001/summary.json` (sha256 ca38a88f…); kết quả đã ghi ở mục LOG trên.
- Viết `results/T-032/ket-qua-phien-12.md` (bốn mục: KT-3, KT-8, KT-15, và phép không chạy KT-9).
- Cập nhật `nguyen-nhan-xep-hang.md` (dòng đầu; mục 1 "Nơi có số"; mục 3.5; mục 4; mục 5.1; mục 6; mục 7; mục 9; mục 11), `kiem-tiep.md` (bảng tóm tắt và ba mục KT-3, KT-8, KT-15: thêm phần kết quả ở đầu, giữ nguyên chữ cũ bên dưới để đối chiếu), `doc-tay.md` (mục 5.3, 5.5, 7.2: sửa cách đọc sai về DA, giữ ghi chú là đã sửa).

**2. Kết quả.**

- **KT-3.** Nhánh giữ nguyên khớp bản đóng băng từng bit 52/52; chỗ móc đếm riêng trùng M-C1 của phiên 9 ở 48/48 ca. Ghép bộ chia theo bài gốc với đếm riêng: số ca root hạng 1 từ 21 lên 23 (luật của bài) và từ 22 lên 27 (luật của code) trên 47 ca. RE2-TT: 14 → 17 và 15 → 19 trên 25, không ca đang đúng nào hỏng, 25/25 trong 5 hạng đầu. Nezha-OB: 7 → 6 và 7 → 8 trên 22, có 5–7 ca tụt hạng. Mốc khai trước đạt ở một luật, không đạt ở luật kia. Còn 20–24/47 ca chưa giải thích; ở Nezha-OB `frontend` đứng đầu ở 14/16 và 11/14 ca còn sai (quan sát, chưa kiểm theo ca).
- **KT-8, nửa MicroRank.** Nhánh bỏ thao tác thiếu nền khớp bản đóng băng từng bit ở 48/48 ca không có thao tác mới. Bốn ca lỗi chạy được sau khi bỏ 210–527 span; root hạng 2, 2, 3, 12; `ts-station-service` đứng đầu 4/4.
- **KT-15.** Cách đọc "DA bất lợi cho dịch vụ không có cạnh" của tôi sai; hai mốc khai trước đều không mô tả đúng trên mọi nút; điều đúng là DA cộng điểm lớn nhất của nút con, và ở ba ca root tụt hạng các thực thể vượt root nhận cùng một giá trị từ một nút nguồn (13/13, 11/12, 4/7).

**3. File đã thay đổi (sau mục kết thúc phiên 12).**

- `tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md` (nối); `docs/STATE.md` (riêng dòng T-032).
- `results/T-032/` sửa: `nguyen-nhan-xep-hang.md`, `kiem-tiep.md`, `doc-tay.md`. Mới: `thiet-ke-phep-doi-012.md`, `ket-qua-phien-12.md`.
- `results/T-032/scripts/` mới: `laptop_contrast_v7.py`, `laptop_contrast_collect_v5.py`, `circa_da_addition_v1.py`, `self_check_phien12_v2.py`.
- `results/T-032/runs/` mới: `microrank-kt3-test-001/`, `microrank-kt3-001/` và `-launch/`, `circa-da-addition-001/` (ba thư mục đầu và cuối cộng 35.163.895 byte); trong `tong-hop-phien-12-001/`: `self-check-phien12/phan-D.py.txt`, `result-006.json`, `result-007.json`, `log-ba-phep-kiem-laptop.md`, `sha256-sau-ba-phep-kiem.txt`.
- sha256 của các file trên sau khi sửa: `runs/tong-hop-phien-12-001/sha256-sau-ba-phep-kiem.txt`. File `sha256-dau-ra-goc.txt` ghi trạng thái trước ba phép kiểm; ba file `.md` đã đổi so với nó, bảy JSON đầu ra không đổi.
- EC2: không đụng trong phần này. Bản để soát ở `~/rca/T-032/tong-hop-12/soat/` là bản TRƯỚC ba phép kiểm.
- KHÔNG sửa: `src/`, dữ liệu, kết quả đã chấm, SPEC, WHY, DECISIONS, T-033. Không mở test, không commit, không subagent.

**4. Kiểm đã chạy.** `scripts/self_check_phien12_v2.py` (v1 cộng phần D), kết quả `runs/tong-hop-phien-12-001/self-check-phien12/self-check-phien12-result-007.json`: phần A 46 nhóm số, 0 lệch; phần D 15 nhóm số của `ket-qua-phien-12.md`, 0 lệch; phần B 250 số, 16 không nằm trong mục được dẫn (13 như trước; 3 số mới là số của KT-3 trong một dòng có dẫn KQ11 mục 2.2 làm mẫu bảng); phần C 970 số, 19 không thấy ở phiếu (17 như trước; 2 số mới là số của KT-15, đã có ở phần D). Thiết kế 012 không đổi sau khi chạy (sha256 trùng `runs/microrank-kt3-001-launch/pins.txt`).

**5. Điều kiện dừng.** Không điều kiện nào chạm trong phần này: RAM đỉnh 73,5%; lượt dài nhất 1.173 giây; laptop khoảng 2,10 GB (2.065.710.233 byte đo trước đó cộng 35.163.895 byte), dưới trần 4 GiB.

**6. Điều chưa chắc, và việc cần Minh quyết.**

- **KT-9 chưa chạy** dù thuộc nhóm "cần laptop": ước 1–2 giờ, phải đổi cửa sổ đã khóa, chưa có thiết kế. Cần Minh quyết có làm nhánh chẩn đoán đổi cửa sổ không.
- **Nửa TraceRCA của KT-8** (EC2, khoảng 10 phút) và **KT-1, KT-2, KT-12** (EC2, khoảng 45 phút) chưa được duyệt.
- **Phép kiểm mới nảy ra từ KT-3:** bảng nối cho nhánh ghép ở Nezha-OB, để biết `frontend` đứng đầu có phải vì span phía gọi của lời gọi tới root (EC2, khoảng 15 phút).
- **Giấy tờ:** dòng DECISIONS cho lời duyệt hôm nay và một mục WHY cho thiết kế 012 chưa ghi; chữ đề xuất trình trong chat.
- **Lựa chọn của người làm:** hiểu "toàn bộ phép kiểm cần chạy trên laptop" là KT-3, KT-8 (nửa MicroRank), KT-15, trừ KT-9; mốc "từ 4 ca" của KT-3 do tôi đặt; KT-8 là đổi đầu vào, kết quả không thay số đã chấm.
- Prompt cho Codex ở mục "Kết thúc phiên 12" vẫn dùng được: danh sách file trong đó chưa nêu `ket-qua-phien-12.md` và `thiet-ke-phep-doi-012.md`, nhưng có nêu "các file thiet-ke-*.md" và thư mục `results/T-032/`; khi chuyển, Minh có thể thêm tên `ket-qua-phien-12.md` vào dòng "Tài liệu gốc" (thông tin trung tính).

**7. Bước tiếp theo chính xác.** Như mục "Kết thúc phiên 12" điểm 7. Lệnh kiểm file thật nay là: `py -3 -B -X utf8 results/T-032/scripts/self_check_phien12_v2.py results/T-032 <file kết quả mới>`, phải in "A: 46 claims, mismatch 0" và "D: 15 claims, mismatch 0".

**8. Lệnh cuối đã chạy.** `py -3 -B -X utf8 results/T-032/scripts/self_check_phien12_v2.py results/T-032 results/T-032/runs/tong-hop-phien-12-001/self-check-phien12/self-check-phien12-result-007.json`; `sha256sum` các file đã sửa; `du -sb` ba thư mục lượt mới.
