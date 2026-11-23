# Nháp mục WHY: ngưỡng phủ cửa sổ của W5 (chỉ soạn, chưa ghi `docs/WHY.md`)

Soạn 23/11/2026, phiên `rca-w5` (Claude, người làm T-073), để đáp CX-21 phần "Lý do còn thiếu". Điều phối trình Minh duyệt chữ trước khi ghi. Số mục do điều phối gán.

---

## WHY-1xx. T-073 Ngưỡng phủ cửa sổ khi nghiệm thu W5: trace lỗ ≤ 30 s, metric lỗ ≤ 4 × bước, log không bắt buộc — đặt 20/11/2026, khóa 22/11/2026 trước E5; mục WHY ghi bổ sung **sau** E5 (23/11)

**Thời điểm.**
- Quy tắc được thêm vào `check_core_input.py` ngày **20/11/2026 22:03Z**, LOG T-073 lượt 7, khi sửa theo Codex CX-06 điểm 5–6.
- Quy tắc được đưa vào `khai-truoc-e5.json` nháp 2 cùng lúc. Ngày **22/11/2026**, file khóa ở bản `T073-khai-e5-khoa-1` (sha256 ghi LOG T-073 lượt 11).
- E5 chạy **23/11/2026 02:07–02:38Z**.
- Mục WHY này được viết **sau** khi đã thấy kết quả E5, trong đó 6 nguồn Payment trượt ngưỡng. Hai ngưỡng **không đổi** sau E5. Mục này chỉ bổ sung lý do còn thiếu theo luật cứng 3. Đây không phải lần chọn lại.

**Chọn gì.**
- Với mỗi nguồn, lấy mốc thời gian của các mẫu thực nằm trong [t̂−300, t̂+300).
- Lỗ lớn nhất = max(mẫu đầu − (t̂−300), khoảng giữa hai mẫu liền nhau, (t̂+300) − mẫu cuối).
- **Trace** (toàn bộ span, theo mốc kết thúc): bắt buộc; thiếu phủ khi lỗ > 30 s.
- **Mỗi nguồn metric có trong gói:** bắt buộc; thiếu phủ khi lỗ > 4 × bước của nguồn (bước 15 s → 60 s; bước 10 s → 40 s), hoặc khi không có mẫu nào.
- **Log:** không bắt buộc, chỉ báo.
- `du_cua_so` chỉ đúng khi mọi nguồn bắt buộc đều đủ. Khi đúng, được viết "lõi nhận đủ cửa sổ"; khi không, viết "đã hiển thị nhưng thiếu phủ".

**Vai trò.** Đây là **quy ước nghiệm thu** cho câu chữ của W5: "dữ liệu thực sự vào lõi quanh t̂" (kế hoạch §8.2, CX-06). Ngưỡng này **không** đo được thiếu bao nhiêu thì kết quả xếp hạng thay đổi. Nó không đánh giá phương pháp và không thuộc tiêu chí `ket_qua_chuc_nang`.

**Vì sao chọn như vậy.** LOG lượt 7 không ghi căn cứ cho riêng hai con số 30 s và hệ số 4. Phần dưới là căn cứ dựng lại lúc viết mục này. Ghi rõ như vậy để không trình bày như lý do đã có từ lúc đặt.
- **Tính theo mẫu thực thay cho biên min/max.** Quy tắc biên cũ (`nguon_khong_phu_tron`, như `m1_ft.doi_moc._phu`) chỉ xét mẫu đầu và mẫu cuối, nên không bắt được lỗ ở giữa. Phép thử tổng hợp ở lượt 7 cho thấy điều này: bỏ 8 mẫu giữa của chuỗi 15 s thì lỗ là 135 s, quy tắc biên không báo (LOG T-073 lượt 7, mục 22:03Z kiểm).
- **Metric 4 × bước.** Ngưỡng này cho phép tối đa 3 lần lấy mẫu liên tiếp bị hụt trước khi gọi là thiếu, nhằm không báo thiếu vì một vài lần scrape trễ. Cùng quy ước "4 bước" như ngưỡng 60 s = 4 bước dò 15 s của H5 trong V082. Quan sát nền: ở các nguồn không bị can thiệp của E5 và lượt dưới tải E3 (`t073-dev-008`), lỗ lớn nhất là 15 s với nguồn bước 15 s và 20,001–20,088 s với nguồn bước 10 s (E3: `results/T-073/kiem/dev/t073-dev-008/su-co/b08d6da4d1.json` `#/…/phu/nguon`, 32 nguồn 15 s, 29 nguồn 10 s). Cả hai đều dưới ngưỡng với khoảng cách lớn.
- **Trace 30 s.** Dưới tải ×1, span đến liên tục. Lỗ lớn nhất quan sát được là 0,35–0,395 s ở dev, E3 và E5. Lỗ 30 s lớn hơn mức bình thường khoảng 75 lần, nên chỉ một lần mất dữ liệu thật mới vượt ngưỡng. Ngưỡng tính trên trace gộp toàn hệ thống, không theo từng dịch vụ.
- **Log không bắt buộc.** Dịch vụ có thể không ghi log trong khoảng khỏe, nên thiếu log không có nghĩa là mất dữ liệu.

**Phương án đã xét.**
- (1) Quy tắc biên min/max: bỏ, vì không bắt được lỗ giữa (vẫn ghi để đối chiếu).
- (2) Tỷ lệ số mẫu so với số kỳ vọng: không chọn, vì một lỗ liền lớn có thể bị che bởi tỷ lệ mẫu còn cao.
- (3) Ngưỡng chặt hơn, ví dụ 2 × bước: chưa xét bằng dữ liệu; sẽ dễ báo thiếu vì scrape trễ.
- (4) Ngưỡng theo từng dịch vụ cho trace: không làm ở W5.

**Điều kiện thất bại.**
- (a) Lỗ dưới ngưỡng vẫn có thể rơi đúng đoạn khởi phát lỗi và đổi kết quả. Ngưỡng không đo ảnh hưởng lên xếp hạng.
- (b) Nguồn dẫn xuất (`rate[1m]`, phân vị) làm mịn mất mẫu thô khoảng 1 phút. Vì vậy ngưỡng 60 s của nhóm HTTP có thể không thấy một lỗ thô ngắn hơn khoảng 2 phút.
- (c) Trace gộp có thể đủ trong khi một dịch vụ mất hết span. Đó là trường hợp Payment ở E5, chỉ có span ở N.
- (d) `check_core_input.py` bản E5 chỉ áp quy tắc lên 61 nguồn metric cơ sở của đầu vào P7. Hai kênh `live-down` và `live-ms` mà V082 thêm sau đó không nằm trong phép kiểm tự động (CX-21 điểm 1). Với ca E5, 16 nguồn `live-*` đã được kiểm tay sau Q1 và đủ phủ (`results/T-073/dap-cx21/dinh-chinh-e5-2.md` §1). Các lượt sau vẫn cần thêm phép kiểm cho hai kênh này.
- (e) Đổi bước scrape thì ngưỡng metric đổi theo.

**Bằng chứng.**
- `campaigns/online/check_core_input.py` (bản E5 `81a9273`), docstring và hàm `lo_lon_nhat`.
- LOG T-073 lượt 7 (mục 22:03Z) và lượt 10 (E3, `t073-dev-008`).
- `results/T-073/khai-truoc-e5.json` `#/tieu_chi/ket_qua_phu_cua_so`.
- `results/T-073/e5/su-co/bbc0a6d44f.json` `#/du_lieu_loi/phu`.

**Kết luận phụ thuộc.**
- Chỉ phụ thuộc: câu "lõi nhận đủ cửa sổ" hoặc "đã hiển thị nhưng thiếu phủ" trong kết quả W5 (E5, và các lượt sau nếu dùng lại quy tắc).
- Không phụ thuộc: kết quả chức năng E5 (đạt), độ chính xác hay đối chứng của W6–W7.
- Nếu W6–W7 cần biết thiếu phủ có làm đổi hạng hay không, đó là phép đo riêng, không suy ra từ ngưỡng này.
