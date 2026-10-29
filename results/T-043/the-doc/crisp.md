# Thẻ đọc — CRISP → E1-CP, cách cắt span con của E1-U

**Nguồn.** Z. Zhang, M. K. Ramanathan, P. Raj và cộng sự, "CRISP: Critical Path Analysis of Large-Scale Microservice Architectures", USENIX ATC 2022. Đọc §5.1–5.2, tr. 659–661: Listing 1, Hình 4, 6, 7, 8.

## Cơ chế

- **Dựng DAG từ một trace** (§5.1, tr. 659). Start của mỗi con tạo một điểm "spawn" trên cha; end của con tạo điểm "sync". Jaeger không ghi ở cha con nào về cuối cùng, nên phải suy từ end của từng con theo đồng hồ của chính con.
- **Thuật toán đường găng** (§5.1.1, Listing 1, tr. 659):
  - bắt đầu từ span gốc; sắp các con theo end giảm dần; con kết thúc cuối (LFC) nằm trọn trên đường găng;
  - bỏ qua các con bắt đầu hay kết thúc trong khoảng của LFC;
  - tìm con kết thúc ngay trước start của LFC, lặp lại tới hết con; đệ quy xuống con của từng LFC;
  - thời gian của cha không thuộc con nào trên đường găng là thời gian độc quyền (exclusive) của cha. Thời gian bao gồm (inclusive) là toàn bộ span.
- **Lệch đồng hồ** (§5.2, tr. 660). Trên 118 nghìn trace, hai lời gọi tuần tự có chồng lấn ghi nhận trung vị 204 µs, lớn nhất 1.696 µs (Hình 8). Vì vậy happensBefore(A, B) được nới:
  - end của A trừ ngưỡng nhỏ hơn start của B;
  - không con nào khác của cùng cha bắt đầu hay kết thúc trong vùng chồng lấn;
  - ngưỡng là 1 ms.
- **Cắt span** (§5.2, tr. 660–661):
  - con bắt đầu trước cha: cắt start về start của cha, cắt đệ quy cả con cháu;
  - con kết thúc sau cha: cắt end về end của cha;
  - con nằm hẳn ngoài cha (kết thúc trước start của cha, hoặc bắt đầu sau end của cha): bỏ cả cây con;
  - ở Uber, tổng thời gian bị cắt dưới 5%.

## Đầu vào; phần ta có và thiếu

- **Có:** span với start, end và quan hệ cha–con ở RE2-TT và Nezha-OB; đủ để chạy cả hai cách tính.
- **Thiếu:**
  - kind của span và thông tin bên gọi có thật sự chờ hay không;
  - trên dev, lời gọi đồng bộ chưa được xác nhận (T-035; O03).

## Điều kiện thất bại

- Lời gọi bất đồng bộ chạy sau khi cha kết thúc bị cắt khỏi cha, nên không lên đường găng.
- Con song song kết thúc sớm không lên đường găng, dù có thể chậm.
- Lệch đồng hồ quá 1 ms làm sai quan hệ trước–sau.
- Trên dev, tỷ lệ cha có con chồng lấn quá 1 ms (KS-16 pha 1, `ks16/dem-khong-nhan.json#/tong_hop/<dataset>/parents_with_overlap`):
  - RE2-TT: 0/494.815 cha có từ hai con trở lên;
  - Nezha-OB: 444/277.534, tức 0,16%.

## Chỗ đổi trong B2

- **E1-CP:** câu "c_end − 1 ms < d_start và không con nào khác của cùng cha bắt đầu hay kết thúc trong khoảng chồng lấn" khớp §5.2. Không đổi.
- **Thêm vào đặc tả v1:**
  - con cắt về [s₀, s₁) của cha ở cả hai đầu; con nằm hẳn ngoài cha bị bỏ khỏi phép tính của cha. E1-U dùng cùng cách cắt;
  - thời gian độc quyền theo CP bằng d_p trừ độ dài hợp các con trên đường găng đã cắt. Fixture 3 cho 0. CRISP không định nghĩa trường hợp chồng lấn dưới 1 ms làm tổng thời gian con vượt cha; lấy hợp khoảng thì kết quả không âm.
- **Hệ quả theo Q2 của SPEC:** cả hai dataset có tỷ lệ chồng lấn dưới 5%, nên E1-CP khai trước là "không đủ ca"; bước K-b không chạy E1-CP. Không đạt điều kiện chạy K-b theo Q2 (ngưỡng 5%). Nezha-OB có 444/277.534 cha có chồng lấn hơn 1 ms; khác biệt E1-CP so với E1-U trên các trace này chưa được kiểm. Chồng lấn chưa chứng minh là song song thật; τ = 1 ms chưa được hiệu chỉnh cho dataset này (`dinh-chinh-phien10.md` Đ21).
