# Thẻ đọc — TraceDiag → E1, E5, E7

**Nguồn.** R. Ding, C. Zhang, L. Wang và cộng sự (Microsoft), "TraceDiag: Adaptive, Interpretable, and Efficient Root Cause Analysis on Large-Scale Microservice Systems", ESEC/FSE 2023 (industry), arXiv 2310.18740. Đọc §3.2 (tr. 3), §4.2–4.5 (tr. 5–8), §5 phần đầu (tr. 8–9).

## Cơ chế

1. **Độ trễ độc quyền (ExL)** (§3.2, Bảng 2, tr. 3):
   - ExL bỏ phần thời gian của các dịch vụ mà thành phần gọi; độ trễ bao gồm là InL;
   - trong sự cố, ExL trung bình của root lớn hơn khoảng ba lần ExL của thành phần khác, và vượt trung bình 96% thành phần.
2. **Tiền xử lý** (§4.2, tr. 5): lấy mẫu 1% trace theo từng trace; gộp chuỗi theo thành phần bằng trung bình, mỗi 15 phút.
3. **Tỉa đồ thị phụ thuộc** (§4.3–4.4, tr. 5–7). Có 35 hành động tỉa theo ba nhóm:
   - theo độ trễ: ExL trung bình, ExL lớn nhất, InL;
   - theo chỉ báo bất thường của TraceArk;
   - theo tương quan Pearson giữa độ trễ đầu–cuối và InL của nút.
   Chính sách chọn hành động học bằng RL (PPO). Phần thưởng gồm độ chính xác RCA trên các sự cố có nhãn và độ phức tạp của đồ thị sau tỉa.
4. **RCA nhân quả** trên đồ thị đã tỉa (§4.5, tr. 7–8):
   - mô hình nhân quả dạng đồ thị; cơ chế của mỗi nút là P(X_j | PA_j), trong đó PA_j là các dịch vụ mà X_j gọi;
   - root là nút có cơ chế đổi giữa cửa sổ nền và cửa sổ báo động;
   - phân bổ Shapley cho thay đổi trung vị độ trễ của frontend, theo hướng Budhathoki và cộng sự.
5. **Đánh giá:** dữ liệu Microsoft Exchange; bảng so sánh chính dùng 9 ca thử (§5.2, tr. 9). Nhãn root do chuyên gia gán.

## Đầu vào; phần ta có và thiếu

- **Có:** span với cha–con, nên tính được độ trễ độc quyền (E1-U làm đúng việc này ở mức thao tác).
- **Thiếu:**
  - TraceArk;
  - nhiều sự cố có nhãn để học chính sách tỉa. Học như vậy là dùng nhãn trong phương pháp (luật cứng 6, WHY-10);
  - chuỗi dài theo 15 phút: cửa sổ của ta chỉ 300 giây mỗi phía, Nezha-OB còn ngắn hơn.

## Điều kiện thất bại

- Chính sách tỉa bỏ mất root.
- Phương pháp phụ thuộc nhãn để học chính sách.
- Bảng chính chỉ có 9 ca thử; bài không so với quy tắc đơn giản (KHAO-SAT K1).
- Phân bổ Shapley cần mô hình học được cho từng nút, nên tốn chi phí khi đồ thị lớn.

## Chỗ đổi trong B2

- **E1:** không đổi công thức. TraceDiag cho thêm một quan sát công nghiệp rằng độ trễ độc quyền tách được root. Quan sát này chưa kiểm trên dev, không là bằng chứng E1 giúp.
- **E5:** TraceDiag tách tự sinh và kế thừa bằng phép đổi cơ chế nhân quả, cộng phân bổ Shapley. E5 của M1 là luật trên lớp tín hiệu và cạnh, tức một **đơn giản hóa**; đặc tả v1 ghi đúng như vậy. Phương án Shapley không đưa vào ma trận, vì:
  - cần mô hình học được cho từng nút;
  - chưa có câu hỏi nào trên dev cần nó;
  - chi phí chưa ước lượng.
- **E7:** đồ thị sau tỉa của TraceDiag tương tự một "vùng". Cách tỉa của bài cần chính sách học bằng nhãn, nên không chuyển sang M1. E7 giữ hai cách dựng không học của B2.
