# Thẻ đọc — MicroHECL → B1.4, E2, E5, E7

**Nguồn.** D. Liu, C. He, X. Peng và cộng sự, "MicroHECL: High-Efficient Root Cause Localization in Large-Scale Microservice Systems", ICSE-SEIP 2021, arXiv 2103.01782v1. Đọc §II (tr. 2), §III (tr. 2–3), §IV.A (tr. 3–4, Bảng I, Hình 2), §IV.B (tr. 4–6), §IV.C (tr. 6–7).

**Ghi chú dẫn mục.** SPEC dẫn "§IV.C" cho B1.4, E2, E5, E7. Trong bài:
- §IV.C là chiến lược tỉa bằng tương quan;
- hướng lan theo loại bất thường (Bảng I) và quy trình chuỗi lan nằm ở §IV.A;
- phát hiện bất thường theo cạnh ở §IV.B;
- xếp hạng bằng tương quan ở §III mục 3.

Thẻ này đọc cả §III–IV.

## (a) Cơ chế gốc

1. **Đồ thị** (§III, tr. 2–3): nút là dịch vụ được gọi trong 30 phút gần nhất; cạnh Si → Sj là lời gọi. Mỗi cạnh lưu metric chất lượng (RT, EC, QPS) theo phút trong 60 phút gần nhất, gộp từ các instance.
2. **Loại bất thường và hướng lan** (Bảng I, tr. 4):
   - độ trễ (RT) và lỗi (EC) lan từ dưới lên, tức bên được gọi → bên gọi;
   - lưu lượng (QPS), tăng hoặc giảm, lan từ trên xuống.
3. **Chuỗi lan** (§IV.A, tr. 4):
   - bắt đầu từ dịch vụ báo sự cố; xét các láng giềng gọi hoặc được gọi;
   - mở chuỗi khi láng giềng bất thường và quan hệ trên/dưới khớp hướng lan của loại đó;
   - mở rộng ngược hướng lan, **cùng một loại bất thường**, tới khi không thêm được nút;
   - ứng viên root là các điểm cuối chuỗi.
4. **Phát hiện theo cạnh** (§IV.B, tr. 4–6):
   - RT: OC-SVM, so cùng kỳ hôm trước và tuần trước;
   - EC: Random Forest **có giám sát**, học trên 1.000 ca có nhãn, với năm đặc trưng, trong đó có tương quan Pearson với RT;
   - QPS: 3-sigma trên 60 phút, cộng điều kiện tương quan Pearson với metric nghiệp vụ trên 0,9;
   - cửa sổ phát hiện là 10 phút gần nhất.
5. **Tỉa** (§IV.C, tr. 6–7): trước khi thêm một nút vào chuỗi, tính tương quan Pearson giữa metric của cạnh hiện tại và metric của cạnh kề trên chuỗi (60 giá trị theo phút). Dưới 0,7 thì tỉa cạnh và không thêm nút.
6. **Xếp hạng** (§III mục 3, tr. 3): sắp ứng viên theo trị tuyệt đối của tương quan Pearson giữa metric nghiệp vụ của dịch vụ đầu (ví dụ số đơn thành công) và metric chất lượng của ứng viên, trong 60 phút.

## (b) Phần có thể chuyển sang M1

| Ý của MicroHECL | Chỗ trong M1 | Ghi chú |
|---|---|---|
| Độ trễ và lỗi lan từ bên được gọi lên bên gọi | B1.4, lớp lan ngược | Thêm nguồn cho bảng lớp; vẫn chưa kiểm trên dev |
| Gắn bằng chứng lên cạnh gọi; khi lần ngược chuỗi, quy bất thường của cạnh cho phía được gọi | E2-C | MicroHECL đo metric theo cạnh; E2 đo khoảng ngoài span bên được gọi |
| Điểm cuối chuỗi là ứng viên | Tầng 1 sau E5 | Nút có bất thường không được giải thích bởi nút phía dưới |
| Chuỗi từ dịch vụ đầu tới ứng viên | E7, vùng nghi ngờ | E7 dựng quanh ứng viên đứng đầu, không cần dịch vụ đầu |

## (c) Phần M1 tự đề xuất, không có trong MicroHECL

- **Giải thích chéo loại tín hiệu.** Ở E5, bên được gọi có tài nguyên tăng, E1, E2 hoặc thao tác mới được phép giải thích kênh lan ngược của bên gọi. MicroHECL chỉ mở rộng chuỗi trong cùng một loại.
- **"Tần suất tăng" xếp vào lớp lan ngược** (cơ chế retry). MicroHECL xếp QPS lan từ trên xuống (tải vào). SPEC đã khai hai cơ chế là chưa phân xử (B1.4, ghi chú); thẻ này thêm nguồn cho phía "tải vào".
- Nhóm vòng (SCC), cờ F_raw và F_I, thống kê E4, PageRank (E6b).

## Tương quan cho E5 (theo yêu cầu bước 1 của SPEC)

**Kết luận: giữ ở trạng thái ứng viên. Không đưa vào `ma-tran-thu.json`.**

Lý do: chưa có hợp đồng khả thi trên dev.
- MicroHECL tính Pearson trên 60 điểm theo phút.
- Trên dev:
  - metric Nezha-OB chỉ có 5 + 5 điểm theo phút;
  - trace và log Nezha-OB chỉ phủ 42–97 giây ở N và 84–140 giây ở A (KS-16 pha 1);
  - metric RE2-TT có 600 điểm theo giây, nhưng tự tương quan mạnh. Pearson giữa hai chuỗi trôi cùng chiều thì cao mà không cần quan hệ nhân quả.
- Hợp đồng, nếu sau này đề xuất, phải ghi đủ các mục đã liệt kê ở `why-de-xuat.md` (WHY-E5-TQ).

## Điều kiện thất bại của cơ chế gốc

- Phát hiện lỗi có giám sát, nên cần nhãn.
- Lọc QPS và xếp hạng cần metric nghiệp vụ của dịch vụ đầu; dev không có.
- Tỉa sai khi lỗi lan thật nhưng metric của hai cạnh kề không tương quan, ví dụ bão hòa hoặc trễ pha.
- Lan qua thành phần không được đo (không có cạnh) thì chuỗi đứt.

## Chỗ đổi trong B2

- **B1.4:** ghi chú thêm nguồn MicroHECL (Bảng I) cho hướng lan của độ trễ và lỗi; ghi khác biệt về QPS.
- **E5:** ghi rõ giải thích chéo loại tín hiệu là đề xuất của M1.
- Không đổi công thức nào.
