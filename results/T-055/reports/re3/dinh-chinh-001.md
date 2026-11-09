# Đính chính 001 — báo cáo RE3-OB bản cuối (T-055)

Claude (người làm), 08/11/2026. Minh duyệt gói ghi ("Duyệt gói ghi"), sau phản biện `tasks/T-055-re3-ban-cuoi/REVIEW.md` (R1–R3) và lượt kiểm lại của Codex trong chat.

Giữ nguyên `bao-cao-re3.md`. File này thay các đoạn nêu dưới đây. **Không đổi số xếp hạng, MRR, CI nào.** Không chạy lại phương pháp, không sửa code M1.

Nguồn: **R** = `results/T-055/reports/re3/phan-tich-re3.json`; **Q** = bản nhận `D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received/` (lọc `job.json#/slot/arm` = M1 và `opaque_id`); **K2** = `results/T-056/ket-qua-002.json` (T-056 chưa phản biện).

## Đ1. Cơ chế 1 tách làm hai (thay §0 ý 1, §4 "Cơ chế 1", bảng §4 cột "Kênh thắng" ca `0d4b`) — theo R1, N2

**(a) Ca `test-0d4b3947ca`: nền IQR = 0, điểm theo đơn vị gốc.**
- Quan sát: kênh thắng là `shippingservice_mem` hướng **xuống** (Q `result.json#/records/0/extra/kenh_co`, `huong=xuong`, s = 376832). Ở đơn vị phân vị: `r_xuong_A` = 0,6133, `r_xuong_N` = 0 (`#/records/0/extra/don_vi_phan_vi/96`). Độ rộng đúng hướng là **0,613**, không phải 0. Báo cáo cũ đọc nhầm vì `phan_tich_re3.py:177` chỉ tính độ rộng cho hướng `len`.
- Suy luận: IQR nền đo được bằng 0 nên `src/m1/e4.py:279` đặt c = 1; z thành chênh tuyệt đối theo byte. Trong điều kiện IQR nền = 0, bước chuẩn hóa của E4 cho điểm phụ thuộc đơn vị, và khóa E6a đặt kênh đó lên đầu.
- Bỏ câu "khi nhiều hơn nửa mẫu N bằng nhau thì IQR = 0". Không đúng tổng quát: N = [0,0,0,1,1] có IQR = 1. Chỉ dẫn IQR đã đo.
- Ca đúng tương ứng (`299b`, `b826`) giữ như báo cáo cũ: nhánh này hai chiều.

**(b) Ca `test-cde8f873f5`, `test-d07d23cade`: ngoại trị của kênh trace hẹp.**
- Quan sát: ở M1, kênh thắng là self-time E1 (s = 814,1) và cạnh E2 (s = 241,7), độ rộng 0,105 và 0,014. Ở C-a0 (tắt E1/E2/E5) cả hai ca **vẫn sai**, kênh thắng là `op_full` (s ≈ 815,8 và 203,4) (R `#/trung_gian_M1_family/<ca>/C-a0/comp_channels`).
- Suy luận: z tính từ max(A) trên kênh trace có ít mẫu lệch cho điểm lớn. Cơ chế chung là ngoại trị kênh trace hẹp, có cả khi không dùng E1/E2. Điều này **không** chứng minh E1/E2 không tác động trong từng cấu hình (bo-E1 sửa được `cde8`, bo-E2 sửa được `d07d`).
- So với P7(a) §7.5: phần lặp lại là (b), kênh trace hẹp. (a) IQR = 0 chỉ gây 1 ca sai ở RE3.

## Đ2. Chuỗi E4 → E5 → E6a ở ca `428c`; bỏ câu "không phải đồ thị" (thay §0 ý cuối, §4 "Cơ chế 2", dòng `428c` của bảng §4) — theo R2, N1

- Quan sát (R `#/trung_gian_M1_family/test-428cf2c868/M1`): root emailservice có cpu giảm s = 4,99 và workload giảm s = 2,50, cả hai **F_I = 0**. E5 gán `lan_xuoi` theo cạnh checkoutservice → emailservice (`/root_inherited`). Khóa tầng 1 chỉ dùng kênh F_I = 1 (`src/m1/xep_hang.py:119`), nên root chỉ còn log lỗi s = 1,0 và latency s = 0,23.
- Hạng root: 4 ở M1, 2 ở bo-E5 và C-a0 (RR 0,25 → 0,5; R `#/so_cap/M1-bo-E5|rr`, `#/so_cap/M1-C-a0|rr`). Bỏ E5 vẫn chưa thắng paymentservice (workload s = 6,26).
- Kết luận đã sửa: ở ca này, E5 (dùng cạnh) làm root mất 2 hạng. Câu "hai cơ chế đều là cách tính điểm của E4/E6a, không phải đồ thị" **bị bỏ**.
- Thang log: kênh đếm log có s ≤ 1; khi **cùng tầng**, khóa max s ưu tiên kênh z > 1. Đây là hạn chế có điều kiện, **chưa được cô lập** thành nguyên nhân của ca sai hay của ưu thế M4. Bỏ chữ "không bao giờ".
- Sửa số: 42 kênh log có cờ trong 30 bản M1, **36** có s = 1, 6 kênh từ 0,9934 đến 0,9992 (thay "41/42").

## Đ3. RQ3d với quy tắc đơn giản (thay §5 ý 2) — theo R3

M1 hơn C-d2 theo CI mô tả đã khóa: Δ = +0,136, CI [0,028; 0,258], 8/20/2 (R `#/so_cap/M1-C-d2|rr`). M1 chưa hơn C-d1: Δ = −0,025, CI [−0,058; 0,000]. Hai đối chứng cho kết quả khác nhau. CI là mô tả, không là kiểm định.

## Đ4. Tín hiệu của SimpleRCA, log và status (thay §0 "tín hiệu chính", §3 ứng viên SimpleRCA, §6 đề xuất 1 và 2(i)) — theo N3, đã chỉnh theo Codex

- M4 cộng phiếu metric, trace và log (`src/simplerca/core.py`). Riêng phần đếm sự kiện metric (vượt mean + 3σ) đã tái lập thứ hạng root trên RE3: MRR 0,975, thực thể đầu trùng M4 ở 30/30 ca (K2 `#/tom_tat/RE3-OB/MRR/R1_events`, `#/tom_tat/RE3-OB/R1_top1_trung_M4_top1`). Bỏ ứng viên "bỏ phiếu đơn giản trên ba nguồn khai thác log lỗi".
- Bỏ cụm "log lỗi là tín hiệu chính của lỗi mã nguồn". T-056 thấy root đứng đầu theo số log lỗi tăng ở 4/30 ca; bên gọi ghi nhiều log lỗi hơn.
- Status span: trên RE3, root không có span lỗi tăng ở ca nào (T-056 §2.1). Điều này **không bác bỏ** ứng viên kênh status cho FlashTicket (instrumentation khác), nhưng cũng **không cho căn cứ** rằng kênh ấy sẽ giúp. Đề xuất §6 giữ trạng thái "chưa kiểm", ghi thêm: nếu dùng, cần gán lỗi theo cạnh gọi và đủ instrumentation.

## Đ5. Lệch bố trí so với bản khóa trước (bổ sung §1) — theo N4, đã chỉnh theo Codex

`results/T-055/runs/khoa-truoc-001/preregistration.json#/placement/workers_per_host` = 1 (SPEC cũng ghi 1). Lượt chạy dùng 2 worker mỗi EC2 (`results/T-054/runs/re3-ban-cuoi-001/meta/ec2_{1,2}-plan.json`, `workers: 2`). Đây là lệch chưa khai lúc chạy. Không có slot TIMEOUT. Chưa thấy dấu hiệu làm sai kết quả, nhưng chưa chứng minh được điều đó cho mọi baseline. Không chạy lại.

## Phần không đổi

Mọi bảng số §2, kết luận RQ3b (M1 0,925 < M4 0,975, CI chứa 0), RQ3d tổng thể (chưa thấy lợi ích từ quan hệ), phần chạy/seal/chấm. OPEN giữ như §7, cộng thêm: tác dụng của đổi thang log, của kênh status và của sửa nhánh c = 1 đều chưa kiểm.
