# Báo cáo điều phối sáng 23/11/2026 — E4 và việc chờ Minh

Lập 22/11 ~22:30Z (phiên điều phối T-070). Số liệu lấy từ file kết quả, đường dẫn ghi kèm. Không có số nào viết từ trí nhớ.

## 1. Đêm qua đã làm gì

| Mốc (UTC) | Việc | Nguồn |
|---|---|---|
| 22/11 17:57:26Z | E4 xong chuỗi: 9/9 lượt `xong`, không lượt lỗi | `LICH-MAY.md` dòng S3; `/srv/rca-lab/runs/t071-e4/chuoi.jsonl` |
| 19:06–19:20Z | T-071 xuất và phân loại phút E4 theo bản khóa `463cf596…`; đóng S3 | `results/T-071/e4/` (`SHA256SUMS` 14/14) |
| 19:06Z | T-072 xong đối chiếu bộ chấm offline với Grafana trên E3 | `results/T-072/e3-doi-chieu-offline.md` |
| ~19:24Z | T-072 chấm R5 trên E4 | `results/T-072/bang-bao-dong-gia.md`, `.json` |
| 19:12Z–22:10Z | T-073 sửa hướng dẫn E5 5 lượt; Codex kiểm 5 lượt (CX-16, 16b, 17, 18, 20) | `results/T-073/trien-khai-e5.md`; `results/T-070/codex/CX-1[678]*, CX-20*` |
| 19:15Z | Hợp nhất phản biện CX-13…16b (T-066, T-068, T-074, T-073) | `results/T-070/hop-nhat-cx13-16.md` |
| 22:00–22:22Z | Hai phiên Codex lần lượt phản biện kết quả W4 (CX-19, CX-19b) | `results/T-070/codex/CX-19-tin-cuoi.md`, `CX-19b-tin-cuoi.md` |

Không có dữ liệu nào bị mất khi T-071, T-072 bị dừng nhầm 16:43Z (kiểm ở LOG T-070 "Lượt 9").

## 2. Kết quả E4 (W4, báo động giả với luật sống)

**Phân loại phút** (`results/T-071/e4/phan-loai-tom-tat.txt`, `#/dem_theo_nhan`): 464 phút trong cửa sổ 10:13–17:57Z = `khoe_x1` **383** + `bien` 43 + `flash` 38. Không có phút mất quan sát, quota hay suy giảm. 383 = trần đã khai trong bản khóa và ≥ 360.

**Chấm R5** (`results/T-072/bang-bao-dong-gia.json`):
- Mẫu số `#/mau_so/mau_so_dung` = **383** phút; số phút Grafana không đánh giá `#/mau_so/phut_grafana_khong_danh_gia_trong_khoe_x1` = 0.
- Sự cố `#/ty_le_khoe_x1/su_co` = **0**; khoảng tin cậy Poisson 95% `#/ty_le_khoe_x1/ci95_poisson_moi_6_gio` = [0; 3,47] sự cố / 6 giờ.
- Ba nguồn đều 0: bộ chấm offline, lịch sử trạng thái Grafana, webhook.
- **R5 đạt theo phép so đã khai** (0 ≤ 1, mẫu số ≥ 360).

**Phản biện hai phiên Codex:** cả hai chấp nhận số đo R5 của bản khóa. CX-19b tự tái lập: 0 nhãn lệch trên 432 phút E2 và 464 phút E4, đủ 8 ngưỡng, 0 sự cố / 383 phút. Không cần phát lại E2–E4.

**E4 không chứng minh:**
- Độ nhạy với lỗi thật. 7/11 luật chưa có bằng chứng dương thật; luật 5xx không bị thử thách vì E4 không có 5xx nào. Độ nhạy thuộc E5 và W6–W7.
- Độ tin của "0 sự cố" thấp: 6,4 giờ chưa loại được tỷ lệ thật tới 3,47 / 6 giờ.

**Rủi ro cần Minh biết** (`#/khoang_cach_nguong_p95_khoe_x1`): p95 lớn nhất duy trì 60 s của payment và ticket ở E4 bằng khoảng 0,84 ngưỡng, cao hơn M của E2 26% và 53%. Hai giải thích chưa phân xử: (1) trôi do DB tích lũy (E4 cách E2 ~36 giờ); (2) dao động đuôi (hai route ít request). CX-19b thêm: trung vị p95 payment giảm nhẹ, ticket gần như giữ; cực đại tăng ở lượt 1 và lượt 6 → chưa tách được. Nếu là trôi, E5 và demo có nguy cơ báo động giả ở payment/ticket. Không sửa ngưỡng bằng E4.

**Điểm phản biện còn mở (không chặn R5)** — chi tiết `CX-19b-tin-cuoi.md`:
- F1: giờ hiệu lực E4 nên ghi 06:06:10Z (nhịp sớm nhất log hỗ trợ), không phải 06:06:00Z; E4 bắt đầu 4 giờ sau nên không đổi kết quả. Lỗi nhỏ.
- F2: chỉ nói "lệch −4 s phù hợp với chênh pha trong E3", không bảo đảm cho lượt khác. Người làm.
- F3: câu về tính độc lập trong WHY-110. **Minh quyết.**
- F5: ba nhánh xử lý khi có cảnh báo trong `cham_offline.py` có lỗi; không ảnh hưởng E4 (0 cảnh báo) nhưng chặn dùng khi có sự cố. Người làm.
- N1: `chon-nguong` thiếu route vẫn thoát thành công. N2: lập luận "khi và chỉ khi" của luật 5xx sai chiều (chỉ là điều kiện đủ). Lỗi nhỏ / người làm.
- F6: `TRANG-THAI.json` lệch — điều phối đã đồng bộ 22:22Z.

## 3. E5 — gói commit sẵn sàng trình duyệt

- Ô: `PAUSE-PAYMENT` (hạt 32323232). N = 25 phút, tiêu chí và hai file khóa không đổi qua 5 lượt sửa.
- Gói 3 commit trên repo lab: **E5** (worktree `D:/Project/rca-lab-wt/T-073-e5`, nhánh `t073-e5`, 7 file = `results/T-073/e5.diff`), **P** bật dashboard lưu trữ, **H** hoàn tác (`results/T-073/commit-e5/`). Thứ tự trên máy: `ecdeed2 → E5 → P → E5 → H`.
- CX-20 (Codex): đủ để trình duyệt; điểm cuối (§5 bước 1) T-073 đã sửa, điều phối kiểm diff đúng một dòng.
- Giới hạn đã biết khi kiểm dashboard: liên kết metric `live-down` trên trang ca hỏng (lỗi G1 có từ T-066, file ghim T-067) — ghi là giới hạn, không phải lỗi E5.

## 4. Việc chờ Minh

1. **Duyệt commit + push gói E5/P/H** (nhánh lab `t073-e5`) → điều phối mở S4, T-073 chạy E5.
2. **Nghiệm thu R5/W4** kèm giới hạn ở mục 2; chọn chuyển prompt "người làm đáp phản biện" CX-19 (`CX-19-tin-cuoi.md` dòng ~77) cho T-071/T-072; quyết F3 (WHY-110).
3. **Rủi ro trôi p95:** cho T-072 phân tích mô tả E2→E4 trên dữ liệu đã xuất (không máy, không đổi ngưỡng) trước E5 hay không.
4. **Từ hợp nhất CX-13…16** (`results/T-070/hop-nhat-cx13-16.md`): R3b T-066 (giữ 2.6, xét 2.7), F3 T-068 (giữ bản hoàn tác), N5/Q-W6-07 T-074; chuyển prompt đáp phản biện T-066, T-068, T-074.
5. **Quy trình:** lượt sửa thứ 2 của T-073 có dùng subagent đọc mã Grafana (LOG T-073, CX-17 nêu) — trái yêu cầu không dùng subagent; đã nhắc, các lượt sau không dùng.
6. **Commit repo RCA** cho hồ sơ đêm qua (T-070…T-073 LOG/kết quả): chờ Minh duyệt (R2b).
7. Tắt lịch `t070-danh-thuc-dieu-phoi` khi Minh trở lại (chạy 01:55–08:55 giờ máy mỗi ngày).

## 5. Usage

Claude 5 giờ 74% lúc 19:27Z (đặt lại 23/11 00:00Z), tuần 27%. Codex tài khoản 5: hết lúc 19:25Z, hồi 21:54Z, chạy xong CX-20/19/19b.
