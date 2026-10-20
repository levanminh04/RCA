
### Kết thúc phiên 12 (11/10/2026, 10:58Z = 17:58 +07)

**Đính chính giờ.** Hai mục checkpoint phía trên ghi "khoảng 10:55Z" và "khoảng 12:10Z" là tôi ước sai. Theo dấu giờ file: lượt ghép bảng đầu tiên xong 10:31:07Z (`out-001.sha256`), lượt thứ ba xong 10:44:03Z (`out-002.sha256`), `doc-tay.md` 10:54Z, báo cáo chính 10:55:46Z, lượt tự soát cuối 10:56:03Z. Cả phiên chạy từ 10:15Z tới 10:58Z theo đồng hồ của laptop và của EC2. Thứ tự các việc đúng như đã ghi.

T-032 chuyển sang **chờ phản biện**. Chưa đóng; RQ2 và G2 chưa đóng.

**1. Đã làm trong phiên** (theo mục "Bước tiếp theo chính xác" của phiên 11).

- Việc giấy tờ treo: Q-136 và WHY-47 đã có trong sổ; không cần hỏi lại.
- Lưu bản cũ của năm file đầu ra (`runs/tong-hop-phien-12-001/ban-truoc/`).
- Bảng tự động theo ca phủ 372 đơn vị: `doi-chieu-dung-sai.json` (đơn vị, 301 cặp đối chứng, 52 nhóm), `chuoi-bang-chung.json`.
- Đọc tay 52/52 nhóm, 100 đơn vị: `doc-tay.md`; trạng thái đọc cập nhật trong `bao-phu-nhom.json`.
- Mức đo được theo ba mức chặt: `kha-nang-do-trace.json`, `coverage-trace.json`.
- `phan-xu-caller-root.json` (82 đơn vị có cờ M5 nguồn), `can-thiep-tinh-toan.json` (A′ theo ca và sổ 14 phép đổi).
- `kiem-tiep.md`: 16 mục; mục KT-4 (40 cặp "chung phía trên" của TraceRCA) được trả lời phần lớn trong phiên bằng cách đếm lại theo lớp từ bảng (`runs/tong-hop-phien-12-001/tracerca-cap-theo-lop.json`).
- Báo cáo chính `nguyen-nhan-xep-hang.md` theo năm đầu ra P4, 11 mục.
- Tự soát; cập nhật dòng T-032 của STATE; prompt cho Codex ở cuối mục này.

**2. File đã thay đổi.**

- `tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md` (nối); `docs/STATE.md` (riêng dòng T-032; trong phiên, dòng T-033 được phiên khác cập nhật, tôi không đụng).
- `results/T-032/` thay bản cũ: `nguyen-nhan-xep-hang.md`, `chuoi-bang-chung.json`, `phan-xu-caller-root.json`, `kha-nang-do-trace.json`; `bao-phu-nhom.json` (chỉ các trường trạng thái đọc).
- `results/T-032/` mới: `doi-chieu-dung-sai.json`, `coverage-trace.json`, `can-thiep-tinh-toan.json`, `doc-tay.md`, `kiem-tiep.md`.
- `results/T-032/scripts/` mới: `tong_hop_v1.py`, `phieu_gon_v1.py`, `cap_nhat_bao_phu_v1.py`, `self_check_phien12_v1.py` (sha256 hai đầu khớp với bản ở EC2 `~/rca/T-032/scripts/`).
- `results/T-032/runs/` mới: `tong-hop-phien-12-001/` (41.138.301 byte): `ban-truoc/`, đầu ra của lượt ghép, `phieu-doc/`, `phieu-gon/`, `doc-tay-phan/`, `self-check-phien12/`, `tracerca-cap-theo-lop.json`, `prompt-codex-soat-ket-qua.txt`, các file `sha256-*.txt`. Thêm `self-check-phien11-001/result-006.json`, `self-check-phien10-001/result-007.json`, và `metric-chain-001/rows.json` (chép từ EC2).
- EC2, chỉ trong `~/rca/T-032/`: `tong-hop-12/` (`in/`, `out/`, `out-lan-2-truoc-khi-sua-seed-torai/`, `soat/`, các gói `inputs-001`, `nonok-001`, `out-001`, `out-002`); bốn script ở `scripts/`.
- KHÔNG sửa: `src/`, dữ liệu, môi trường, kết quả của task khác, SPEC, WHY, DECISIONS, MRP, LESSONS, AGENTS, T-033, ba file `ket-qua-phien-*.md`, `doi-chieu-tai-lieu-goc-phien-10.md`. Không mở test hay `data/locked`. Không commit. Không dùng subagent. Không gọi phương pháp RCA nào; không đọc dữ liệu thô.

**3. Kiểm đã chạy và kết quả.**

- Nguồn: `ca-sai.json` của T-028 trùng manifest; 372/372 bản ghi đóng băng trùng `source_sha256`; đầu vào và đầu ra chép giữa laptop và EC2 đều khớp sha256 hai đầu.
- Bảng tự động: 13/13 tự kiểm (`runs/tong-hop-phien-12-001/tu-kiem.json`).
- `bao-phu-nhom.json`: sau khi bỏ các trường trạng thái đọc, nội dung cũ và mới bằng nhau (assert trong script).
- Số của báo cáo, `kiem-tiep.md`, `doc-tay.md`: `runs/tong-hop-phien-12-001/self-check-phien12/self-check-phien12-result-005.json`. Phần A: 46 nhóm con số mới tính lại từ bảng, 0 lệch. Phần B: 39 dòng có dẫn mục của ba file kết quả, 245 con số, 13 con số không nằm trong mục được dẫn; tôi xem tay cả 13: 8 lấy từ nguồn khác được dẫn ngay trong cùng dòng (bảng phiên 12, `doc-tay.md`), 2 nằm ở mục 4.2 được dẫn không kèm tên file, 1 là số thứ tự, 1 là mã ca, 1 là "8/8" của phiên 12. Phần C: 962 con số của `doc-tay.md` mục 1–6 so với phiếu gọn; 17 không thấy ở phiếu nào, xem tay cả 17: tổng của hai số cùng dòng, số dẫn từ KQ10/KQ11, số nhân 100 thành phần trăm, số dính chữ cái trong phiếu, tham chiếu mục; 23 thấy ở phiếu của phương pháp khác, đều là tham chiếu chéo hoặc số suy ra.
- Sửa sau tự soát: ba giá trị z làm tròn (4.209 → 4.209,5 hai chỗ; 9.738 → 9.738,5); "8,4" → "8,43"; một câu ở KT-13 viết lại theo đúng số của nguồn; con số UNSUPPORTED chưa đọc 44 → 42; khoảng "2–6%" → "2–9%" ở KT-2; ba câu ở báo cáo chính viết nhẹ lại (tóm tắt điểm 1, điểm 5; dòng H7).
- Tự soát phiên 10 và 11 chạy lại đầu phiên: 187 và 762 con số, 0 lệch.

**4. Điều kiện dừng.** RAM laptop chạm 95,5% lúc 10:19Z do ứng dụng khác; xử lý như ghi ở checkpoint 1 (chuyển phần ghép bảng sang EC2). Không điều kiện nào khác chạm: không lệch bản đóng băng; lượt dài nhất vài giây; EC2 `~/rca/T-032` 6.188.413.365 byte (5,76 GiB), đĩa còn 19 GB; laptop: lần đo đầy đủ gần nhất 2.008.470.079 byte (phiên 11), phiên này thêm khoảng 50 MB (lệnh `du` cho cả thư mục chưa trả kết quả lúc ghi mục này); tổng dưới trần 12 GiB, laptop dưới trần 4 GiB. Lúc 10:56Z EC2 không có tiến trình T-032.

**5. Lỗi của tôi trong phiên, đã sửa.** (a) Khóa seed của TORAI khác kiểu giữa hai bảng làm lần ghép thứ hai thiếu vị trí chuỗi gọi cho 90 đơn vị TORAI; sửa và thêm tự kiểm (checkpoint 2). (b) Ước sai giờ ở hai checkpoint (đính chính ở đầu mục). (c) Bảng 7.1 của `doc-tay.md` lúc đầu tôi đếm bằng mắt; đã thay bằng số đếm bằng lệnh. (d) Sau khi biết RAM cao tôi vẫn chạy bốn lệnh Python rất nhẹ trên laptop (sửa chữ trong file văn bản, cập nhật dòng STATE, dựng prompt); không lệnh nào tính số liệu.

**6. Điều chưa chắc, và việc cần Minh quyết.**

- **Task đã đạt:** đủ các file đầu ra của SPEC; sáu tiêu chí xong đối chiếu ở mục 10 của báo cáo.
- **Câu hỏi nguồn trả lời tới đâu:** bước nào làm root mất hạng ở từng phương pháp (đã có, mục 3 của báo cáo); dịch vụ gọi đứng trên root vì chờ hay vì cách chấm (đã có theo từng phương pháp, mục 5.2); quan hệ bổ sung được gì (bốn loại thông tin ở mức ứng viên, sáu điều bất lợi, mục 6).
- **Còn mở, kèm bằng chứng cần** (`kiem-tiep.md`): 25–26/47 ca MicroRank sau khi thay bộ chia (KT-3); tỷ lệ cờ nền của thao tác đông span (KT-1, KT-2); vì sao metric của dịch vụ không liên hệ đổi tại mốc (KT-6, không phân xử được bằng dữ liệu hiện có); phần chậm ngoài span của root (KT-13, không phân xử được); mã của tác giả TraceRCA (KT-11); "lan có đáng kể" (KT-10, thuộc tổng hợp G2).
- **Lựa chọn của người làm trong phiên, cần Minh biết:** định nghĩa "đường đi" và quy tắc chọn đơn vị đọc tay; gộp tên cột thành loại thô; cập nhật các trường trạng thái đọc trong `bao-phu-nhom.json` (danh mục đã khóa giữ nguyên, bản cũ lưu lại); chạy phần ghép bảng trên EC2 thay vì laptop; nêu ý kiến "chờ là cơ chế có thật nhưng không chiếm đa số" ở KT-10 như ý kiến của người làm, không phải kết luận.
- **Giới hạn của phần đọc tay:** 76/192 đơn vị sai; mỗi đường đi một đơn vị; với MicroRank và TraceRCA ở Nezha-OB gần như không có đối chứng đúng.
- **Cần Minh quyết** (mục 11 của báo cáo): (1) chấp nhận mức đọc tay hay đọc đủ; (2) có chạy KT-1, KT-2, KT-12, KT-15 (khoảng 55 phút máy) và KT-3 (15 phút laptop) trước G2 không; (3) cách ghi bốn ca lỗi và số độ nhạy của MicroRank ở bảng G2; (4) "lan có đáng kể" và nhãn lan, ở tổng hợp G2; (5) ứng viên nào đưa vào đề bài P5–P6. Thêm: gửi prompt dưới đây cho Codex hay chưa, và cho Codex ghi `REVIEW.md` hay chỉ trả lời trong chat.

**7. Bước tiếp theo chính xác.**

1. Minh chuyển prompt dưới đây cho Codex (điền dòng "Phạm vi ghi").
2. Khi có bản phản biện: phiên Claude mới đọc AGENTS, dòng T-032 của STATE, SPEC, mục này; tự soát lại `nguyen-nhan-xep-hang.md`, `doc-tay.md`, `kiem-tiep.md` và các JSON **trước** khi đọc kết luận phản biện; rồi kiểm từng điểm.
3. Lệnh kiểm file thật khi mở phiên (chạy được trên laptop hoặc EC2, chỉ cần Python chuẩn):
   `python3 -B -X utf8 results/T-032/scripts/self_check_phien12_v1.py results/T-032 <file kết quả mới>` phải in "A: 46 claims, mismatch 0". Trên EC2 bản để soát nằm ở `~/rca/T-032/tong-hop-12/soat/`.
4. Nếu Minh duyệt chạy các mục KT: viết file thiết kế trước khi chạy, như các phép đổi trước.

**8. Lệnh cuối đã chạy.** Trên EC2: `python3 -B -X utf8 ~/rca/T-032/scripts/self_check_phien12_v1.py soat soat/self-check-phien12-result-005.json`; `pgrep -af rca/T-032` (không có tiến trình); `du -sb ~/rca/T-032`; `sha256sum` bốn script. Trên laptop: `scp` file kết quả tự soát; `sha256sum` các file đầu ra (`runs/tong-hop-phien-12-001/sha256-dau-ra-goc.txt`); script cập nhật dòng T-032 của STATE và dựng prompt; `git status --short` (chỉ đọc).

### Prompt để Minh chuyển Codex — soát kết quả T-032 (Minh chọn gửi hay chưa)

Chép nguyên văn "Prompt chung", khối "Soát kết quả" và khối "G2" của `docs/review-prompt.md` (dựng bằng script, chỉ điền các chỗ trong ngoặc nhọn bằng thông tin trung tính). Bản văn bản thuần: `results/T-032/runs/tong-hop-phien-12-001/prompt-codex-soat-ket-qua.txt`.

```text
