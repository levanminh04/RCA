# T-056 — Phân tích bổ sung trước G4 (2.1–2.5)

- **Người làm:** Claude. **Người phản biện:** Codex.
- **Nguồn quyền:** `results/T-056/minh-duyet.txt`. SPEC ghi theo lời duyệt thực hiện; chưa được Minh đọc trước.
- **Gói MRP:** P7 phân tích, chuẩn bị G4. Không chạy phương pháp, không đổi thiết kế, không mở dữ liệu mới. Dùng test TT/OB đã mở (T-054) và RE3 đã mở một lần (T-055). Mọi phân tích là **mô tả sau khi xem**; không dùng làm kiểm định thiết kế mới (C-15 B).

## Câu hỏi
1. (2.1) Trên RE3, mã lỗi span (status ≠ 0) có tăng tập trung ở root theo từng ca không? Nếu có, kênh status sẽ cung cấp thông tin mà M1 hiện không đọc.
2. (2.2) Log lỗi (từ khóa ERROR/FAIL/EXCEPTION) theo ca có tách root khỏi đối thủ không, nếu không bị chặn thang?
3. (2.3) Bao nhiêu kênh metric được cờ có IQR nền = 0 (z tính theo đơn vị gốc) ở TT, OB, RE3? Ca sai/đúng nào chịu ảnh hưởng?
4. (2.4) Vì sao BARO luôn xếp redis đầu và TORAI B xếp bên gọi đầu trên RE3?
5. (2.5) Vùng nghi ngờ (chứa root, cỡ) và vị trí N của root theo ba bộ; M1 theo nhóm vị trí.

## Phạm vi ghi
`tasks/T-056-phan-tich-bo-sung/{SPEC,LOG}.md`, `results/T-056/**`, dòng T-056 trong `docs/STATE.md`. Trên EC2: script tạm `/home/ubuntu/rca-p7/T-056/` (chỉ đọc data-root). Không ghi vào T-054/T-055.

## Phép tính
- Trên EC2, theo mã mờ (không nhãn): đếm span status ≠ 0 theo service trong N = [t−300, t) và A = [t, t+300); đếm "lỗi riêng" (span lỗi không có span con lỗi); đếm dòng log có từ khóa theo container; với mỗi kênh metric M1 đã cờ: trung vị, IQR của N, max của A, xem IQR < 10·eps (nhánh c = 1 của `src/m1/e4.py:279`).
- Trên laptop: ghép nhãn (đã được chấm), xếp service theo chênh A−N, lấy hạng root; so với M1 và M4. OB (Nezha) dùng tín hiệu thay thế từ trung gian đã lưu nếu không có reader metric thô tương đương.
- Hạn chế: thống kê mô tả, không hiệu chuẩn; 30/60/34 ca.

## Tiêu chí xong
Báo cáo `results/T-056/bao-cao.md` có số kèm con trỏ, tách quan sát/suy luận/ứng viên/câu hỏi mở; LOG, STATE, prompt phản biện.
