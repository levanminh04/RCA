# T-032 — Định nghĩa hai bảng mô tả (bản 004): vị trí tín hiệu của root; xu hướng nền của cột thắng

Viết ngày 11/10/2026 (02:50 +07), trước khi chạy. Người viết: Claude. Hai bảng này **không phải phép đổi và không phải phương pháp**: không gọi phương pháp nào, không đổi phép tính nào, không dùng để chấm Hit. Mọi đại lượng tính cho mọi dịch vụ hoặc mọi cột trước; nhãn root và loại lỗi chỉ nối ở bước cuối.

## 1. Điều tôi đã thấy trước khi viết

Toàn bộ `ket-qua-phien-9.md`. Riêng: ở Nezha, trung vị chỉ 8% trace nhóm A có span của root vượt ngưỡng; T-D cho 16/17 cặp caller của Nezha vẫn đứng trên root; cột thắng của thực thể đứng trên root ở RE2 thường là mem (BARO 55 lượt, SimpleRCA 15/20 cặp), vượt ngưỡng ở trung vị 288/300 mẫu. Vì vậy cả hai bảng là kiểm ứng viên rút ra từ dev, không phải giả thuyết đặt trước. Các mốc chia nhóm ở mục 3 do tôi đặt trước khi nhìn số của bảng; tôi báo kèm phân vị thô để người đọc không bị buộc vào mốc.

## 2. Bảng A — tín hiệu của root nằm ở đâu trong trace

**Câu hỏi nguồn:** đầu ra P4 số 4 (quan hệ giữa dịch vụ có thể bổ sung thông tin gì) và câu còn mở "vì sao ở Nezha span của root hiếm khi vượt ngưỡng".

**Đầu vào:** bảng span mà adapter TraceRCA nhận (cửa sổ ngoài [t−300, t+300)), của 48 ca có lượt phát lại khớp từng bit. Bốn ca RE2 nguồn ERROR không có bảng span: N/A, giữ trong mẫu số.

**Quy ước giống hai phương pháp trace:** operation = `serviceName` + `_` + (`methodName`, thiếu thì `operationName`); span "trước mốc" nếu kết thúc < t, "sau mốc" nếu kết thúc ≥ t; cờ = đại lượng (ms) ≥ mean + 3·std của nhóm ở đoạn trước mốc, mean và std làm tròn 2 chữ số.

**Đại lượng của span:** `d` = duration; `u` = duration trừ độ dài hợp các khoảng span con trực tiếp (hàm `uncovered` của T-D).

**Lời gọi giữa hai dịch vụ:** cặp (span cha p, span con c) cùng trace, cha tìm được, `service(p) ≠ service(c)`. Span phía gọi là p; dịch vụ được gọi là `service(c)`.

**Năm vị trí, mỗi vị trí một cờ:**

| Ký hiệu | Span được xét cho dịch vụ S | Đại lượng | Nhóm lấy nền |
|---|---|---|---|
| own_d | span của chính S | d | operation của span (đúng cờ của MicroRank-RCAEval và TraceRCA) |
| own_u | span của chính S | u | operation của span (đúng cờ của T-D) |
| in_d | span phía gọi của các lời gọi tới S | d | operation của span phía gọi |
| in_u | span phía gọi của các lời gọi tới S | u | operation của span phía gọi |
| in_d_edge | span phía gọi của các lời gọi tới S | d | cặp (operation của span phía gọi, S) |

`in_d_edge` có lý do riêng: ở RE2-TT, span phía gọi thường mang tên chung như `GET`, `POST`, gộp lời gọi tới nhiều dịch vụ khác nhau vào một operation; nền theo cặp (operation, dịch vụ được gọi) tách chúng ra. Không phương pháp nào đang dùng đại lượng này.

**Với mỗi dịch vụ S và mỗi vị trí:** số span sau mốc `n`, số span mang cờ `a`, tỷ lệ `a/n`; `n = 0` hoặc nhóm nền thiếu (dưới 2 span trước mốc) thì ghi riêng, không gán 0. Hạng của S theo `a/n` giảm dần giữa các dịch vụ có `n > 0`, ghi rank_min và rank_max khi hòa. Ghi thêm cho span của chính S: chia theo span vào (cha thuộc dịch vụ khác hoặc không tìm được cha), span trong (cha cùng dịch vụ), và span có con thuộc dịch vụ khác.

**Nối sau cùng cho root:** năm bộ (n, a, a/n, hạng); điểm và hạng của root ở BARO (`runs/baro-b1-001/summary.json`), phiếu metric, trace, log của root ở SimpleRCA (`runs/simplerca-decomposition-002/summary.json`).

**Tổng hợp:** theo dataset và theo loại lỗi, kèm mẫu số: số ca root có `a > 0` ở từng vị trí; số ca root đứng đầu (rank_max = 1) theo `a/n` ở từng vị trí; trung vị `a/n`. Ô có dưới 3 ca chỉ liệt kê, không rút mẫu hình.

**Cách đọc khai trước:**

- Root có `own_d` thấp nhưng `in_d` hoặc `in_d_edge` cao: tín hiệu của lỗi nằm ở span phía gọi, tức gắn với lời gọi (cạnh), không nằm trong span của chính root. Một cách chấm chỉ nhìn span của từng dịch vụ sẽ gán tín hiệu đó cho dịch vụ gọi.
- Root có `in_d` cao còn `in_u` thấp: phần dài ra nằm trong khoảng span con (phía root) đã phủ.
- Root có `in_u` cao: phần dài ra nằm ngoài khoảng span của root; dữ liệu không cho biết đó là mạng, hàng đợi hay xử lý tại phía gọi.
- Root thấp ở cả năm vị trí: trace không mang tín hiệu theo quy tắc 3σ; tín hiệu nếu có nằm ở metric hoặc log.

**Giới hạn:** "root đứng đầu theo một vị trí" là mô tả nơi có thông tin trên dev, không phải thành tích của một cách chấm; không so với Hit của các phương pháp. Quan hệ cha–con khác dịch vụ không chứng minh chờ đồng bộ. Tải chung có thể làm nhiều dịch vụ cùng có cờ.

## 3. Bảng B — xu hướng nền của cột thắng (chỉ RE2-TT)

**Câu hỏi:** thay đổi nhỏ ở cột mem/cpu của dịch vụ khác, thứ làm chúng vượt root ở BARO và SimpleRCA, là "trôi tự nhiên" đã có từ đoạn nền hay "đổi tại mốc sự cố".

**Đầu vào:** chuỗi metric của 30 ca RE2-TT, lấy đúng như mỗi phương pháp nhận: với BARO là hai bảng N và A sau `chuan_bi` của adapter và `preprocess` của RCAEval; với SimpleRCA là hai bảng N và A của `simplerca.adapter.prepare`. Nezha-OB không làm: mỗi phía chỉ có 5 mẫu, không ước lượng được độ dốc.

**Tự kiểm bắt buộc:** từ chính các chuỗi này, z cực đại theo cột tính lại phải trùng khóa trong bản ghi BARO đóng băng từng bit; số mẫu vượt ngưỡng theo cột cộng lại phải trùng phiếu metric của root và của các thực thể đứng trên root trong `runs/simplerca-decomposition-002/summary.json`. Ca nào không trùng thì không dùng.

**Với mỗi cột (mọi cột, mọi ca):**

- `slope_N`: độ dốc hồi quy tuyến tính của giá trị theo thời gian trên N (đơn vị mỗi giây); `drift_N = slope_N × 300` là mức trôi tuyến tính suy ra cho khoảng cách 300 s giữa tâm N và tâm A.
- `shift = median(A) − median(N)`.
- `step_60 = median(60 mẫu đầu của A) − median(60 mẫu cuối của N)`.
- `drift_ratio = drift_N / shift` (N/A khi shift = 0).
- `r2_N`: hệ số xác định của đường thẳng trên N; `monotone_N`: tỷ lệ bước liên tiếp không giảm trên N.
- `votes`: số mẫu A lớn hơn mean(N) + 3·std(N) (ddof = 0), đúng công thức SimpleRCA; `z_max`: z cực đại theo RobustScaler, đúng công thức BARO.

**Chia nhóm (mốc đặt trước, chỉ để đếm):** `trôi nền` nếu 0,5 ≤ drift_ratio ≤ 1,5 và r2_N ≥ 0,5; `bậc tại mốc` nếu |drift_ratio| < 0,5 và |step_60| ≥ 0,5·|shift|; còn lại `khác`. Báo kèm phân vị của drift_ratio, r2_N.

**Nối nhãn sau cùng:** với mỗi ca, cột thắng của root và của từng thực thể đứng trên root (BARO: cột có z lớn nhất của thực thể; SimpleRCA: cột nhiều phiếu nhất). Đếm nhóm theo loại cột (mem, cpu, latency, …), tách ca sai và ca đúng.

**Đối chứng không cần nhãn:** trên mọi cột của mọi ca, tỷ lệ cột mem có `votes ≥ 250` và tỷ lệ thuộc nhóm `trôi nền`. Nếu phần lớn cột mem của mọi dịch vụ đều như vậy ở cả ca đúng lẫn ca sai thì đây là đặc tính chung của kênh mem trên dataset này, không phải dấu hiệu riêng của ca sai.

**Cách đọc khai trước:** cột thắng của thực thể đứng trên root thuộc `trôi nền` hỗ trợ giải thích "trôi tự nhiên bị chuẩn hóa theo độ biến thiên nền thổi lên"; thuộc `bậc tại mốc` hỗ trợ "có đổi thật tại mốc" (lan, tải chung hoặc tác dụng phụ của tiêm lỗi; bảng này không phân biệt ba khả năng đó).

## 4. Phép thử giả cho bảng A (thêm ngày 11/10/2026, 02:50 +07, SAU khi đã xem kết quả bảng A)

**Vì sao thêm:** bảng A cho root đứng đầu theo `own_u` ở 26/26 ca RE2-TT có bảng span. Con số này quá đẹp; AGENTS mục 5 yêu cầu chạy phép thử giả khi kết quả quá đẹp. Mục này viết sau khi thấy kết quả chính, trước khi chạy phép thử giả.

**Định nghĩa:** mốc giả t′ = t − 150 s. Nền là các span kết thúc trước t′ (150 s đầu của đoạn nền). "Sau mốc" là các span kết thúc trong [t − 150, t). Span kết thúc từ t trở đi không được xét cờ. Trong khoảng này không có lỗi nào được tiêm. Mọi phép tính khác giữ như bảng A (script `root_signal_location_v2.py --placebo-shift=-150`; bản v1 giữ nguyên).

**Dự đoán khai trước:**

- Nếu bảng A không thiên vị root về cấu trúc: ở phép thử giả, root đứng đầu theo mỗi vị trí với tần suất gần mức ngẫu nhiên (khoảng 1/27 mỗi ca ở RE2-TT, 1/10 ở Nezha-OB), tức khoảng 1/26 ca RE2 và 2/22 ca Nezha.
- Nếu root vẫn đứng đầu ở nhiều ca: bảng A phản ánh một đặc tính có sẵn của các dịch vụ được chọn làm root (ví dụ nhiều lời gọi, nền hẹp), không phải tín hiệu của lỗi. Khi đó kết quả bảng A không được dùng làm bằng chứng về vị trí tín hiệu.

**Giới hạn:** nền chỉ còn 150 s nên mean và std kém ổn định hơn; phép thử giả chỉ kiểm thiên vị cấu trúc, không kiểm khả năng khái quát.

### 4b. Phép thử giả cho Nezha-OB (thêm lúc 19:53Z ngày 10/10, sau khi thấy lượt `root-signal-placebo-002`, trước khi chạy lượt mới)

**Điều đã thấy:** lượt mốc giả t − 150 s cho RE2-TT chạy được (26 ca). Ở Nezha-OB cả 22 ca không có span nào kết thúc trước t − 150 s: bảng span của Nezha chỉ phủ từ 41,5 tới 97,0 giây trước mốc (đo trên 22 ca, lệnh đọc `adapter-input.parquet` của từng ca). Vì vậy phép thử giả t − 150 s **không áp dụng được** cho Nezha; đây không phải kết quả đạt.

**Định nghĩa bổ sung, dùng cho cả hai dataset:** mốc giả t′ = t − (t − t_min)/2, với t_min là thời điểm bắt đầu sớm nhất của span trong bảng của ca đó; tức điểm giữa của đoạn nền có span. Nền là span kết thúc trước t′; "sau mốc" là span kết thúc trong [t′, t). Script `root_signal_location_v4.py --placebo-midpoint`. Với RE2-TT mốc này gần t − 150 s nên lượt này cũng là lần lặp của lượt 002.

**Dự đoán khai trước:** như mục 4. **Giới hạn riêng của Nezha:** nền chỉ còn khoảng 20–48 giây, nên mean và std theo operation kém ổn định; nếu root đứng đầu nhiều hơn mức ngẫu nhiên ở phép thử giả này thì phải xét cả giải thích "nền quá ngắn" trước khi nghi thiên vị cấu trúc.

## 5. Bảng C — lời gọi giữa hai dịch vụ gồm những khoảng nào (thêm lúc 20:02Z ngày 10/10, trước khi chạy)

**Câu hỏi nguồn:** Q-120 và mục 4 của kế hoạch: phần "chưa được phủ" của span phía gọi gồm những gì; lời gọi có dạng lồng đồng bộ hay không. Bảng này lấy bằng chứng từ chính dữ liệu trace, song song với việc đọc mã nguồn.

**Điều đã thấy trước khi viết:** bảng A và hai phép thử giả; mỗi span phía gọi có đúng một span con thuộc dịch vụ khác ở mọi ca; ở Nezha lỗi trễ mạng có `in_u` cao còn `own_d` thấp.

**Định nghĩa.** Với mỗi lời gọi (span phía gọi p thuộc dịch vụ A, span con c thuộc dịch vụ B, cùng trace):

- `d_p`, `d_c`: thời lượng của p và c.
- `pre` = bắt đầu của c trừ bắt đầu của p; `post` = kết thúc của p trừ kết thúc của c.
- `gap` = d_p − d_c = pre + post. Đại lượng `gap` không phụ thuộc lệch đồng hồ giữa hai máy; `pre` và `post` riêng lẻ thì có.
- `lồng` = pre ≥ 0 và post ≥ 0.

**Tính cho mọi cặp (A, B) của mọi ca, tách trước và sau mốc theo thời điểm kết thúc của p:** số lời gọi; tỷ lệ lồng; tỷ lệ pre < 0, post < 0; trung vị d_p, d_c, pre, post, gap; và tỷ số trung vị sau/trước của d_c và của gap. Ghi thêm tên operation của p và của c, và các span con khác của p nếu có. Không dùng nhãn. Nối nhãn sau cùng để lấy các cặp có B là root.

**Cách đọc khai trước.**

- Lời gọi đồng bộ được ghi bằng một span phía gọi bao một span phía được gọi, đồng hồ hai máy khớp: tỷ lệ lồng ở đoạn nền gần 100%, pre và post dương và nhỏ so với d_c.
- Tỷ lệ pre < 0 hoặc post < 0 cao ở đoạn nền: lệch đồng hồ hoặc span con kết thúc sau span cha (bất đồng bộ). Khi đó chỉ `gap` dùng được, và `gap` âm có hệ thống thì là bất đồng bộ.
- Root bị lỗi mà d_c tăng còn gap không tăng: phần dài ra nằm trong span của root. gap tăng còn d_c không tăng: phần dài ra nằm ngoài span của root (đường truyền, hàng đợi trước khi span của root bắt đầu, hoặc xử lý ở phía gọi quanh lời gọi). Cả hai tăng: cả hai phần.

**Giới hạn.** Dạng lồng trong dữ liệu là bằng chứng về cách span được ghi, chưa phải bằng chứng rằng luồng của dịch vụ gọi bị chặn trong lúc đó; phần này cần mã nguồn. `gap` không tách được đường truyền, hàng đợi và xử lý phía gọi. Nền của Nezha chỉ dài 41–97 giây.

**Mốc đếm (đặt trước khi chạy, chỉ để đếm):** một phần được coi là "dài ra" khi trung vị sau mốc ít nhất gấp đôi trung vị trước mốc; chỉ xét cặp (A, root) có từ 20 lời gọi trở lên ở mỗi phía. Tỷ số thô của từng cặp được lưu để người đọc không bị buộc vào mốc.

### 5b. Bảng C2 — phân rã theo từng lời gọi chậm (thêm lúc 00:38Z ngày 11/10, sau khi đã thấy bảng C, trước khi chạy)

**Vì sao thêm.** Bảng C so trung vị của từng phần trước và sau mốc. Ở ba ca lỗi mem của RE2-TT, trung vị thời lượng span phía gọi tăng khoảng 12 lần (4,8 ms lên 58 ms ở cạnh basic→route) trong khi trung vị của `d_c` và của `gap` đều tăng dưới 2 lần. Hai điều này chỉ cùng đúng khi các lời gọi chậm chia thành hai nhóm (chậm trong span của root, chậm ngoài span của root). So trung vị từng phần vì vậy che mất phần dài ra. Cần phân rã theo từng lời gọi.

**Định nghĩa.** Với mỗi cạnh (A, B) của một ca:

- Ngưỡng chậm của cạnh: phân vị 95 của `d_p` trên các lời gọi trước mốc của chính cạnh đó.
- Lời gọi chậm: `d_p` lớn hơn ngưỡng. Theo cách đặt, khoảng 5% lời gọi trước mốc là chậm.
- Với mỗi lời gọi chậm sau mốc: phần vượt của span root `e_c = d_c − trung vị trước mốc của d_c`; phần vượt bên ngoài `e_g = gap − trung vị trước mốc của gap`. Lời gọi được xếp "chậm trong span của B" nếu `e_c ≥ e_g`, ngược lại "chậm ngoài span của B".
- Đại lượng theo cạnh: tỷ lệ lời gọi chậm sau mốc; trong số đó tỷ lệ chậm trong span của B.

Tính cho mọi cạnh có từ 20 lời gọi trở lên ở mỗi phía, của cả 52 ca (4 ca RE2 không có bảng span đã lưu lấy từ parquet gốc qua bước cắt cửa sổ của runner). Không dùng nhãn khi tính. Nối nhãn sau cùng để tách cạnh có B là root và cạnh có B không phải root.

**Cách đọc khai trước.**

- Tỷ lệ lời gọi chậm sau mốc ở cạnh tới root cao hơn nhiều so với 5% và cao hơn ở cạnh tới dịch vụ khác: thời gian dịch vụ gọi chờ root tăng, và mức tăng đó riêng cho root.
- Cạnh tới dịch vụ không phải root cũng có tỷ lệ chậm cao: độ trễ lan sang lời gọi khác hoặc tải chung; bảng này không phân biệt hai khả năng.
- Trong lời gọi chậm tới root: tỷ lệ "trong span của root" gần 1 thì phần chờ nằm trong xử lý của root; gần 0 thì nằm ngoài span của root (đường truyền, hàng đợi trước khi span của root bắt đầu, xử lý phía gọi quanh lời gọi).

**Giới hạn.** Ngưỡng phân vị 95 là mốc tôi đặt; tỷ lệ thô được lưu. Nền của Nezha chỉ 41–97 giây nên ngưỡng kém ổn định hơn. Phân rã `e_c ≥ e_g` là quy ước xếp loại, không phải phép đo vật lý.
