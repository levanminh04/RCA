# T-032 — Thiết kế bản 008: vị trí trên chuỗi gọi (việc 1) và nối lời gọi chậm với span mang cờ (việc 2)

Viết ngày 11/10/2026, khoảng 03:15Z (10:15 +07), trước khi chạy. Người viết: Claude. Căn cứ: gói bổ sung 007 (Q-134), WHY-45 điểm (6). Hai bảng này **không phải phép đổi và không phải phương pháp**: không gọi phương pháp nào, không đổi phép tính nào, không chấm Hit. Mọi đại lượng tính cho mọi dịch vụ và mọi thao tác trước; nhãn dịch vụ gốc (root) và thứ hạng của phương pháp chỉ nối ở bước cuối.

## 1. Điều tôi đã thấy trước khi viết

Toàn bộ `ket-qua-phien-9.md` và `ket-qua-phien-10.md`. Riêng những số liên quan trực tiếp:

- MicroRank: 252 cặp (thực thể đứng trên root, root); thực thể là dịch vụ gọi trực tiếp root ở 20 cặp, được root gọi ở 46, loại còn lại 186. TraceRCA: 90 cặp; 22, 16, 52.
- Theo cờ thời lượng, ở 18 ca RE2-TT root không đứng đầu thì dịch vụ đứng đầu là `ts-admin-travel-service` ở 14 ca; đó là dịch vụ gọi trực tiếp root ở 9/18.
- Cạnh gọi tới root chậm ở 19/21 ca RE2-TT và 10/16 ca Nezha-OB đo được; ở 13/21 và 7/16 ca có cạnh khác chậm bằng hoặc hơn.

Vì đã thấy các số này, hai bảng dưới đây là kiểm một ứng viên rút ra từ dev, không phải giả thuyết đặt trước khi có dữ liệu. Các mốc đếm ở mục 3 và 4 do tôi đặt trước khi nhìn số của hai bảng; số thô được lưu để người đọc không bị buộc vào mốc.

## 2. Bước chung: một lượt đọc bảng span cho 52 ca (chưa dùng nhãn)

Đầu vào: như bảng C2 (`call_slow_table_v1.py`): 48 ca đọc bảng span mà adapter TraceRCA nhận (lượt phát lại khớp từng bit); 4 ca RE2-TT nguồn ERROR đọc parquet gốc qua đúng bước cắt cửa sổ của runner. Quy ước span trước mốc, sau mốc, thao tác (operation) và cờ thời lượng giữ như bản 004 mục 2 (đúng cờ của MicroRank-RCAEval và TraceRCA).

Mỗi ca lưu:

1. **Đồ thị gọi giữa dịch vụ:** cạnh A→B khi có ít nhất một cặp span cha–con cùng trace với cha thuộc A, con thuộc B, A khác B. Ghi số lời gọi trước mốc và sau mốc của từng cạnh.
2. **Lời gọi chậm:** như bảng C2. Chỉ cạnh có từ 20 lời gọi mỗi phía; lời gọi sau mốc là chậm khi thời lượng span phía gọi lớn hơn phân vị 95 của chính cạnh đó ở đoạn trước mốc. Phần vượt của lời gọi chậm = thời lượng span phía gọi trừ trung vị trước mốc của cạnh.
3. **Với mỗi span, nhìn xuống cây span của trace (các span con, cháu):** tập dịch vụ có span nằm dưới; tập dịch vụ X mà có lời gọi chậm tới X nằm ở chính span đó hoặc dưới nó; tổng phần vượt của các lời gọi chậm tới X nằm ở đó; tập dịch vụ có span mang cờ nằm dưới.
4. **Bảng theo thao tác O và dịch vụ X** (mọi O, mọi X): trong các span mang cờ của O, bao nhiêu span có X nằm dưới; bao nhiêu có lời gọi chậm tới X nằm dưới; bao nhiêu có span mang cờ của X nằm dưới; bao nhiêu span mà tổng phần vượt của lời gọi chậm tới X đạt từ 50% và từ 80% phần vượt của chính span (phần vượt của span = thời lượng trừ mức nền trung bình của thao tác, đúng số đã làm tròn trong luật cờ). Cùng hai số đầu cho các span sau mốc không mang cờ của O, để làm mốc so.
5. **Bảng theo trace cho MicroRank** (mọi O, mọi X): trace sau mốc thuộc nhóm bất thường khi có ít nhất một span mang cờ (đúng luật của bản đang dùng). Với các trace bất thường chứa O: bao nhiêu trace có span của X; có span mang cờ của X; có span mang cờ bao một lời gọi chậm tới X; có một trong hai điều sau (gọi là "bất thường gắn với X"). Kèm số trace bình thường chứa O.

Tự kiểm bắt buộc theo ca: tổng số cờ bằng `H_native` của lượt `tracerca-core-td-001` (48 ca); số trace bất thường, số trace bình thường và số span mang cờ bằng `counts` của lượt `microrank-core-aprime-c1-002` (48 ca); số cạnh có từ 20 lời gọi mỗi phía và tỷ lệ chậm của từng cạnh trùng `runs/call-slow-001/cases/` (52 ca). Ca không đạt thì không dùng.

Kiểm phép "nhìn xuống cây span" trên trường hợp tự dựng trước khi chạy: chuỗi ba tầng, hai nhánh song song, span mất cha, lời gọi chậm ở tầng sâu, span phía gọi tự mang lời gọi chậm.

## 3. Việc 1 — thực thể đứng trên root nằm đâu so với chuỗi gọi

**Câu hỏi nguồn:** đầu ra P4 số 4 và giả thuyết "nhầm triệu chứng với nguyên nhân" của MRP P4: sai lầm của các phương pháp có nằm dọc chuỗi gọi không.

**Nguồn thứ hạng:** 372 bản ghi đóng băng mà `results/T-028/runs/phan-hoi-review-001/ca-sai.json` trỏ tới (52 ca × 6 phương pháp, TORAI B ba seed). Thực thể đứng trên root: hạng xấu nhất của thực thể nhỏ hơn hạng tốt nhất của root, như phiên 9. TORAI tính hạng theo khối rồi nhóm trong khối. Tự kiểm: hạng root tính lại phải trùng hạng T-028 ở mọi bản ghi OK. Thêm một góc nhìn phụ: bảng CIRCA không có bước DA, lấy từ 30 bản ghi `ols+rht`.

**Vị trí của thực thể E so với root R trong đồ thị của ca:**

| Nhóm | Lớp | Định nghĩa |
|---|---|---|
| Phía trên | gọi trực tiếp | có cạnh E→R |
| Phía trên | phía trên gián tiếp | có đường đi E tới R dài từ hai cạnh, không có cạnh trực tiếp |
| Phía dưới | được gọi trực tiếp | có cạnh R→E |
| Phía dưới | phía dưới gián tiếp | có đường đi R tới E dài từ hai cạnh, không có cạnh trực tiếp |
| Hai chiều | hai chiều | vừa phía trên vừa phía dưới (đồ thị có vòng); đếm riêng |
| Không liên hệ | chung phía trên | không thuộc các lớp trên, nhưng có một dịch vụ đi tới được cả E và R |
| Không liên hệ | rời | có span, không thuộc lớp nào ở trên |
| Không có span | không có span | E không xuất hiện trong bảng span của ca (ví dụ thực thể cơ sở dữ liệu ở kênh metric). Không suy quan hệ từ tên |

Đồ thị chính: mọi cạnh thấy trong cả cửa sổ (như phiên 9). Độ nhạy: chỉ cạnh đã có trước mốc; báo số cặp đổi lớp.

**Tỷ lệ nền:** với mỗi đơn vị (ca × phương pháp × seed), tập ứng viên là mọi thực thể được xếp hạng trừ root. Số kỳ vọng của một lớp = số thực thể đứng trên root × tỷ lệ ứng viên thuộc lớp đó, cộng qua các đơn vị. Thêm phép rút ngẫu nhiên: ở mỗi đơn vị rút đúng số thực thể đứng trên root từ tập ứng viên, không hoàn lại, 20.000 lần, hạt giống 20261011; ghi tỷ lệ lần rút có số thực thể "phía trên" không nhỏ hơn số quan sát.

**Cách đọc khai trước** (theo gói): số quan sát ở nhóm "phía trên" từ 1,5 lần số kỳ vọng trở lên và tỷ lệ rút ngẫu nhiên đạt mức đó không quá 5%: sai lầm tập trung dọc chuỗi gọi phía trên root, quan hệ gọi nhắm trúng nhóm này. Tỷ số trong khoảng 0,8–1,25: ngang tỷ lệ nền, quan hệ gọi tới root không nhắm trúng nhóm này. Ngoài hai khoảng: ghi "không rõ". Đọc riêng từng dataset và từng phương pháp; không gộp hai dataset.

**Giới hạn:** rút ngẫu nhiên coi các thực thể đứng trên root là độc lập, trong khi chúng không độc lập (một dịch vụ lên hạng thường kéo theo dịch vụ gọi nó); tỷ lệ này chỉ là mốc tham chiếu, không phải kiểm định. Đồ thị RE2-TT gần như giống nhau giữa các ca, nên vị trí chủ yếu do root là dịch vụ nào quyết định; chỉ có 5 dịch vụ gốc ở RE2-TT và 22 ca Nezha-OB. Vị trí trên đồ thị không chứng minh cơ chế; cơ chế xem ở việc 2.

## 4. Việc 2 — span làm thực thể đứng trên root có phải là span chờ root không

**Câu hỏi nguồn:** câu cần phân xử của MRP P4 và SPEC: phương pháp chấm thời gian chờ dịch vụ phụ thuộc thành bất thường của dịch vụ gọi, hay không. Chỉ xét hai phương pháp dùng trace: TraceRCA và MicroRank.

**Căn cứ để gọi là "chờ":** `ket-qua-phien-10.md` mục 6.2: ở mọi phiên bản mã nguồn ứng viên, mọi lời gọi giữa hai dịch vụ thấy trong dev là lời gọi chặn. Span bao một lời gọi chậm tới root vì vậy có thời lượng gồm cả thời gian chờ lời gọi đó. Điều kiện kèm theo giữ như mục 6.5 của file đó.

**TraceRCA.** Điểm của thực thể E là điểm của thao tác cao nhất O của nó, tính từ số span mang cờ a của O. Với mỗi cặp (E đứng trên root, root): lấy O từ `runs/tracerca-core-td-001/summary.json`; tự kiểm a của bảng mới bằng a ở file đó. Ghi: tỷ lệ span mang cờ của O có lời gọi chậm tới root nằm dưới; tỷ lệ span mà lời gọi chậm tới root chiếm từ 50% phần vượt.

**MicroRank.** Điểm của E là điểm của thao tác cao nhất O, tính từ số trace bất thường chứa O. Với mỗi cặp: lấy O từ `runs/microrank-core-aprime-c1-002/summary.json`; tự kiểm số trace bất thường chứa O bằng tổng "tự vượt ngưỡng" và "chỉ ngữ cảnh" ở file đó. Ghi: trong các trace bất thường chứa O, tỷ lệ trace có bất thường gắn với root; tỷ lệ trace không có span nào của root.

**Mốc đếm (đặt trước):** một cặp được xếp "chủ yếu là chờ root" khi tỷ lệ tương ứng đạt từ 50%; báo thêm ở mốc 20% và 80%. Với TraceRCA dùng tỷ lệ span mà lời gọi chậm tới root chiếm từ 50% phần vượt; tỷ lệ "có lời gọi chậm tới root nằm dưới" báo kèm như mức yếu hơn.

**Đối chứng, để không gọi một đặc tính chung là nguyên nhân của ca sai:**

- Cùng tỷ lệ cho các span sau mốc không mang cờ của cùng thao tác.
- Cùng tỷ lệ cho các dịch vụ phía trên root nhưng **không** đứng trên root, ở ca sai và ở ca root đứng hạng 1.
- Cùng bảng với X là từng dịch vụ khác root có cạnh đủ lời gọi, để biết "gắn với X" có riêng cho root không.

**Dự đoán khai trước.**

- Nếu "nhầm triệu chứng với nguyên nhân" đúng ở mức tính toán: ở các cặp mà E nằm phía trên root, phần lớn span mang cờ của O bao một lời gọi chậm tới root chiếm từ nửa phần vượt (TraceRCA), và phần lớn trace bất thường chứa O có bất thường gắn với root (MicroRank).
- Nếu sai: các tỷ lệ đó thấp (dưới 20%) dù E nằm phía trên root; khi đó giả thuyết bị bác cho hai phương pháp này và phải tìm giải thích khác.
- Với E không nằm phía trên root, tỷ lệ theo span bằng 0 do cấu trúc (không có đường đi tới root). Các cặp này không thể được giải thích bằng "chờ root" ở mức span; với MicroRank vẫn xem tỷ lệ theo trace, vì thao tác có thể chỉ cùng nằm trong trace bất thường do root.

**Giới hạn.** "Bao một lời gọi chậm tới root" là điều kiện về cấu trúc và thời lượng, không đo trạng thái luồng. Ở 15 ca không có cạnh tới root đủ 20 lời gọi mỗi phía, không định nghĩa được lời gọi chậm tới root; các cặp của những ca đó ghi "không xét được", chỉ báo tỷ lệ có span mang cờ của root nằm dưới. Nền của Nezha-OB chỉ 41–97 giây. Mốc phân vị 95 và mốc 50% do tôi đặt. Kết quả là bằng chứng trên dev cho một ứng viên, không phải nhãn lan và không phải tỷ lệ nguyên nhân.

## 5. Đầu ra

- EC2 `~/rca/T-032/runs/chain-spanpass-001/` (bảng theo ca, chưa nối nhãn), `runs/chain-position-001/` (việc 1), `runs/slow-call-flag-link-001/` (việc 2). File tổng hợp chép về laptop cùng đường dẫn, kiểm hash hai đầu.
- Script: `scripts/chain_spanpass_v1.py`, `scripts/chain_position_v1.py`, `scripts/slow_call_flag_link_v1.py`.
- Diễn giải: `results/T-032/ket-qua-phien-11.md`.
