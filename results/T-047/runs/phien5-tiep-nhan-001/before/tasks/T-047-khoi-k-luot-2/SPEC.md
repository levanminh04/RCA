# T-047 — Lượt chạy khối K thứ hai trên 52 ca dev với G3/D1 và thang S1

- **Trạng thái:** SPEC gốc được duyệt tạo ngày 01/11/2026. Bản sửa này chỉ được ghi và triển khai sau khi Minh duyệt câu chữ SPEC, WHY-70 và dòng Q-231. Chưa chạy bước 1 trước lời duyệt đó.
- **Người làm:** Codex, chạy local trên máy của Minh. **Người phản biện:** Claude.
- **Thuộc gói MRP:** P6 (M1). **Cổng:** chuẩn bị G3.
- **Phụ thuộc:** T-046 đã nghiệm thu theo Q-230; code `src` tại `c298188e`; WHY-67–69 đã ghi.
- **Nguồn phân công:** Q-224 và Q-229. Phần vế mốc giả của Q-227 còn hiệu lực.
- **Quyền chạy được đề nghị duyệt cùng bản sửa:** local tối đa 4 tiến trình, lượt dài hơn 1 giờ và qua đêm; trần tổng gói chạy là 7 giờ thời gian thực, không phải giờ CPU hoặc 7 giờ cho từng lượt. Commit và push chờ duyệt riêng.

## Mục tiêu

**Câu hỏi nguồn:** DT18-NV2/NV3; hướng dẫn của cô về phương pháp đồ thị và đối chiếu thực nghiệm; MRP P6 tầng 1–4 và phần kiểm hành vi trên dev trước G3. Các câu Q1, Q3, Q6, Q8 theo SPEC T-043.

**Loại task:** chạy thử trên dev theo ma trận khối K và luật chọn đã khai trong SPEC T-043 B4, Phụ lục C. Dùng G3 cho đơn vị phân vị, D1 cho đơn vị đếm và S1 cho xếp hạng E6a theo WHY-67, WHY-69. V0 giữ để báo cáo; T-046 chưa chọn được `verdict` cho bản P7.

Thay vế mốc giả của luật C bằng đại lượng số thực thể tầng 1 theo mục dưới. Các tham số, thứ tự các vế luật C và mặc định chọn khối khác giữ như T-045.

**Đạt task này cho:**
- T1 với code mới;
- cấu hình thắng của khối K lượt thứ hai, hoặc xung đột trình Minh;
- kết cục của E1, E2, E3, E5 trong bối cảnh khối, làm đầu vào cho task (2);
- đối chiếu T-045 và bảng 2×2 tại P, kèm phân tích theo ca và trung gian.

**Không cho:** bằng chứng hiệu quả trên dữ liệu chưa dùng để thiết kế, hiệu chuẩn cổng hoặc xác nhận cơ chế chỉ từ kết cục luật C.

Đây là lần chọn cấu hình thứ hai trên cùng 52 ca dev. Việc tái sử dụng dev và thiết kế thích nghi làm tăng nguy cơ lạc quan; chưa định lượng mức lạc quan thực tế. C-e đã được xem ở T-045 và trong quá trình thiết kế, kiểm lại T-046, kể cả trước các lần khóa lại. Vế mốc giả không dùng dữ liệu độc lập.

**Phần nguồn chưa bao phủ và hệ quả:**
- K-b, T6–T12 và KB thuộc task (2a), (2b); lựa chọn khối chưa xác nhận kết cục ở chuỗi cuối.
- T13, A4, đối chứng đầy đủ và hồ sơ G3 thuộc task (3); T-047 không trả lời xong RQ3 hoặc khẳng định lợi ích quan hệ.
- T4/T4b với code mới chưa chạy; chưa có bằng chứng độ nhạy α, ε của gói mới. Không dùng số T-045 thay cho phép kiểm gói mới. Phần cần bổ sung hoặc giới hạn trước G3 phải trình Minh.
- Phát hiện ở chế độ (b), vùng có nhãn và áp dụng FlashTicket thuộc các task sau. Hoàn thành T-047 không xóa các nghĩa vụ đó.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích cần phân biệt | Phép kiểm | Giới hạn |
|---|---|---|---|
| Code mới chạy đúng không? | Lỗi adapter, cấu hình, thứ tự hàng hoặc hash seed | Hồi quy helper; T1; QT5; đối chiếu phần cửa sổ chung với bước 10 T-046 | Đạt kiểm cài đặt không xác nhận hiệu quả RCA |
| E1-U, E2-C, E3, E5 có kết cục gì trong khối? | Tác động thành phần, tương tác, vài ô gần ngưỡng | Khối K; luật C ba thế giới; luật chọn bước 1–8 và 10 | Kết cục ở chuỗi cuối còn chờ KB |
| Lựa chọn bền tới đâu? | Một số ô quyết định lựa chọn | Bootstrap theo ô như T-045, dùng helper mới | Chỉ báo cáo, không chọn lại |
| Kết cục đổi so với T-045 qua bước nào? | Gói cổng, thang điểm, vế C-e và sự mong manh của mẫu dev | Bảng 2×2 tại P; kết cục có/không C-e; lần theo đầu vào → cờ → F_I → khóa → hạng | G3 và D1 vẫn đi chung; không suy cơ chế chỉ từ bảng tổng |
| Mức HẠI ảnh hưởng lựa chọn thế nào? | Quyết định phụ thuộc dung sai thực dụng | Chạy lại toàn bộ luật C và bộ chọn ở h = 0,5 và h = 2 | Không đổi mức chính theo số đã thấy |

## Đầu vào

- Code nghiệm thu T-046 tại `c298188e`.
- Mọi cấu hình chạy M1 mới mang:
  `che_do = {"cong_phan_vi": "G3", "cong_dem": "D1", "thang": "E4+T4c"}`.
- Dữ liệu dev và mốc giả C-e như T-045: 30 ca RE2-TT, 22 ca Nezha-OB; C-e chỉ RE2-TT.
- Nhãn dùng chấm gồm root, loại lỗi, ô và E_X chỉ đọc ở pha 2, sau khi hash pha 1 đã ghi LOG. Mốc tiêm dùng cho chế độ (a) lấy qua projection đã được phép; không truyền các nhãn dùng chấm vào phương pháp.
- D2 dùng bản ghi baseline P3 đóng băng để kiểm bộ chấm, không chạy M1 và không có yêu cầu bật `che_do`.
- Kiểm đầu ra cũ bằng manifest cũ T-043–T-045. Phần `src/m1` của manifest T-044 kiểm tại `69ef90b6`, của T-045 tại `bbef69dd`, bằng `git show`; không sửa manifest cũ.
- Code và đầu ra mới của T-046 kiểm theo manifest T-046. Lệch ngoài dự kiến thì dừng phần phụ thuộc.
- Môi trường theo `results/T-045/scripts/moi_truong.sh`.

## Đầu ra

Trong `results/T-047/`:

- `scripts/`, gồm `luat_c_t047.py` và adapter riêng của T-047;
- `tests/`, `kiem-helper.json`;
- `runs/`, giữ mọi lượt kể cả lượt hỏng;
- `t1.json`;
- `khoi-k.json`, gồm kết quả chính và độ nhạy mức HẠI; `khoi-k/`;
- `tai-lap-baseline.json`, `co-che-khoi-k.json`;
- `do-ben.json`, `so-sanh-t045.json`;
- `so-lan-nhin.jsonl`;
- `dinh-chinh-cai-dat.md` nếu cần;
- `bao-cao.md`, `manifest.json`.

## Phạm vi ghi

- `results/T-047/`;
- nối `tasks/T-047-khoi-k-luot-2/LOG.md`;
- chỉ dòng T-047 trong `docs/STATE.md`.

Ngoại lệ được đề nghị Minh duyệt riêng cùng câu chữ bản sửa:
- thêm đúng một mục WHY-70 vào `docs/WHY.md`, trước khi dùng đại lượng và mức HẠI trong kết quả;
- thêm đúng một dòng Q-231 vào `docs/DECISIONS.md` cho lời duyệt thật và phạm vi được duyệt.

Không mở quyền ghi chung cho WHY hoặc DECISIONS; không sửa WHY-67–69 hay quyết định cũ.

Không sửa `src` trong gói này. Nếu phát hiện lỗi cần sửa `src`, giữ đầu ra, trình đính chính và xin duyệt phạm vi riêng. Không ghi kết quả T-043–T-046, task khác, MRP hoặc KE-HOACH. Không commit hoặc push nếu chưa được Minh duyệt riêng.

## Vế C-e của luật C

Đặt N1(c,i) là số thực thể có `extra.tang_P = 1` của cấu hình c tại cửa sổ giả i.

Với mỗi cặp tắt/bật, dùng cùng tập cửa sổ hợp lệ I của hai nhánh. Cửa sổ phải có bản ghi hợp lệ, đủ thông tin tính N1 và không mang `INSUFFICIENT_EVIDENCE`. Báo các cửa sổ bị loại và lý do. ERROR, UNSUPPORTED hoặc thiếu trường bắt buộc được xử lý theo luật lỗi, không chuyển thành N1 = 0.

N1 = 0 chỉ là giá trị hợp lệ khi có phép chấm hợp lệ và thực sự không có thực thể tầng 1.

Vế C-e trả HẠI khi:

    ΔN1 = Σ_i w_i × [N1(bật,i) − N1(tắt,i)] / Σ_i w_i > h

- Mức chính h = 1 thực thể/cửa sổ.
- Lượt chính có w_i = 1; bootstrap dùng bội số của ô tương ứng.
- Dùng Fraction và dấu `>` chính xác. Với đủ 30 cửa sổ, tổng tăng ít nhất 31 thực thể mới vượt mức 1.
- Mẫu số bằng 0 ghi `CHUA_KIEM_DUOC`, không áp vế này và không ghi đã qua. Giữ cờ đó trong kết quả và lựa chọn. Cấu hình thắng có cặp mang cờ này thì trình Minh trước khi dùng làm nền cho task (2). Helper phải đưa cờ này vào kết quả chọn, vì `chon_khoi.py` không đọc nó.
- N1 lấy tại P, áp chung vào luật C của ba thế giới như phạm vi vế C-e cũ.
- Không áp quy tắc trần dành cho tỷ lệ `CAUSE_FOUND` vào số đếm N1.
- Báo N1 từng cửa sổ, trung bình tuyệt đối từng cấu hình, chênh từng cặp, mẫu số, số bị loại và V0. V0 không dùng làm đại lượng quyết định của vế mới.

Mức 1 là dung sai thực dụng, chưa hiệu chuẩn. Nó được đề xuất sau khi đã xem C-e G0/D0 và các tóm tắt G3/D1 hiện có; không coi là lựa chọn độc lập với dữ liệu đã xem.

Đại lượng không trung tính với số kênh và coverage. Bật riêng E5 với cùng đầu vào chỉ có thể giữ hoặc giảm N1, nên vế xét N1 tăng không bắt được tác hại riêng của E5. S1 không đổi N1 hoặc V0. Giữ đầy đủ các vế RR, UV-6 và M5; N1 giảm không tự chứng minh RCA tốt hơn.

## Helper luật C và hồi quy

Cài `results/T-047/scripts/luat_c_t047.py`; pha 2 và phép độ bền cùng gọi helper này. Không sửa hoặc monkeypatch `src/m1_danh_gia/`.

Helper gọi `pha2.ket_cuc_cap(..., moc_gia=None)` để giữ kiểm cặp, tập ca, RR, UV-6, M5 và trọng số theo từng thế giới. Sau đó gắn vế C-e mới:

- Giữ nguyên `dieu_kien_E5` và `UV6`.
- Dựng danh sách HẠI riêng từ hai trường đó và vế C-e mới.
- Không sao nguyên `ly_do_hai_rieng` nền vì nó có thể đã chứa `M_cong_M_phay`; để `ket_cuc_tu_tong_hop` tự thêm điều kiện đó đúng một lần.
- Tính lại kết cục, bước, lý do HẠI, các kết cục δ báo kèm và toàn bộ `ket_hop` từ ba thế giới. Giữ các số RR và kiểm dấu.
- Giữ `khong_moc_gia[w]` là kết cục nền của đúng thế giới w, với cùng trọng số và điều kiện UV-6/M5.
- Không truyền tổng N1 vào tham số `moc_gia` cũ vì API cũ hiểu đó là số `CAUSE_FOUND`.

Trước bước 1, cài và chạy test hồi quy bằng dữ liệu giả trong `results/T-047/tests/`, ghi kết quả vào `kiem-helper.json` và giữ đầu ra từng lượt trong `runs/`. Test không đọc nhãn dev hoặc dữ liệu thật.

Test phải kiểm:

1. Qua cùng điểm nối ghép vế C-e của helper, đưa kết quả vế cũ từ `moc_gia.ve_tu_dem`; đối chiếu chính xác với `luat_c.ap_dung` trên cùng đầu vào giả. So các trường gốc, không chỉ tên kết cục: bước, lý do có thứ tự, δ_d, thành phần, MRR/ΔMRR, P/M/P′/M′, E_X, hướng ô, điều kiện E5, UV6, vế mốc giả và toàn bộ `bao_kem`.
2. Đối chiếu wrapper ba thế giới với `pha2.ket_cuc_cap` khi dùng vế cũ ở điểm nối test; gồm `khong_moc_gia` và `ket_hop`. Bao phủ E3, E5, R0→c nhiều thành phần; điều kiện riêng bật/tắt; `M_cong_M_phay` không lặp; các thế giới có kết cục khác nhau.
3. Với vế N1 mới, kiểm đúng biên strict `>`, mẫu số bằng 0, cặp bị loại, bội số bằng 0 và lớn hơn 1; kiểm HẠI C-e nằm ở bước HẠI riêng trước các vế thứ hạng.
4. Kiểm pha 2 và bootstrap dùng cùng helper và cùng trọng số tương ứng cho RR, UV-6, M5, C-e. Mẫu có mọi bội số bằng 1 phải trả lại kết quả và lựa chọn chính.
5. Kiểm metadata và chế độ theo trạng thái bản ghi như mục dưới.

Việc truyền vế cũ chỉ phục vụ hồi quy trên dữ liệu giả; chạy thực nghiệm luôn dùng vế N1 đã khóa.

Khi chưa cài và chạy, trạng thái là “chưa kiểm”. Nếu hồi quy hoặc tích hợp lệch, giữ lượt hỏng và dừng trước bước 1 để trình nguyên nhân. Test đạt chỉ xác nhận helper và điểm nối trên dữ liệu giả, không xác nhận hiệu quả RCA.

## Adapter, trạng thái lỗi và hash

Không chạy nguyên trạng các script có đường ghi cố định vào T-045. Adapter của T-047 phải định tuyến mọi đầu ra, tổng hợp, pha 2 và độ bền vào `results/T-047/`.

Ghi cấu hình đầy đủ, revision và chế độ trong metadata của lượt. Với bản ghi OK hoặc NO_EVIDENCE, kiểm từng bản ghi có `method_version` của chế độ mới và `extra.che_do` đúng G3/D1/E4+T4c; không chỉ tin `tham-so.json`.

Với ERROR hoặc UNSUPPORTED:
- giữ bản ghi, cấu hình đã yêu cầu và mọi đầu ra;
- dừng phát việc mới để chẩn đoán; chưa chọn cấu hình khi lỗi còn chưa giải thích;
- không bỏ ca, đổi ma trận hoặc âm thầm chạy chế độ cũ;
- nếu cần sửa ngoài quyền, trình Minh;
- ca không OK vẫn ở mẫu số RR và được tính trượt theo giao thức; không biến lỗi C-e thành N1 = 0.

Kiểm trạng thái trước khi kiểm `extra.che_do`: bản ghi lỗi có thể thiếu trường này. Trạng thái lạ phải báo lỗi và giữ đầu ra.

Pha 1 phải đủ bản ghi, kiểm hash, ghi hash vào LOG trước khi gọi bất kỳ bước đọc nhãn dùng chấm nào, kể cả D2. Hash nằm cạnh bản ghi chưa thay cho việc ghi LOG trước pha 2.

## Các bước

0. **Mở phiên và chuẩn bị.** Kiểm hash; test T-044 ở chế độ mặc định, T-045 và T-046; ghi môi trường. Cài adapter/helper và chạy hồi quy theo SPEC này sau khi Minh duyệt câu chữ. Ghi rõ test helper mới chưa được thay bằng các bộ test cũ.
1. **Chạy thử.** R0 mới trên một ca mỗi dataset; QT5, thời gian, RAM; dự báo tổng. Vượt ngân sách thì dừng, báo Minh.
2. **T1.** R0 trên 52 ca × seed 0/1/2, cộng xáo hàng và 30 cửa sổ giả RE2-TT. Báo các đại lượng như đầu ra T1 của T-045, thêm N1. Đối chiếu các đại lượng chung của R0 thật/C-e với bước 10 T-046.
3. **Khối K pha 1.** Đủ 16 cấu hình × (52 ca + 30 cửa sổ giả); E3 cách khớp (a), nhóm vòng C′. Xử lý lỗi theo mục trên. Đối chiếu K-đủ thật/C-e với phần tương ứng của bước 10 T-046. Ghi hash vào LOG trước pha 2.
4. **Pha 2.**
   - D2 tái lập 12/12 MRR baseline; lệch thì dừng.
   - Ghép nhãn; áp helper mới cho mọi cặp ở ba thế giới.
   - Áp luật chọn khối bước 1–8 và 10, giữ bảng mặc định của T-045.
   - Nếu cấu hình thắng không có E1/E2/E5 thì dừng trình Minh. Giữ kiểm phòng vệ tập rỗng, nhưng không gọi đây là hệ quả có thể xảy ra chỉ từ vế HẠI tương đối; không tự thêm lọc tuyệt đối R0.
   - C-d1, C-d3 chỉ báo cáo.
5. **Lần theo cơ chế.** Với thành phần có kết cục khác T-045 và kết cục HẠI tại cấu hình thắng, đọc code và trung gian; đối chiếu ca tụt, ca lên và ca đúng có điều kiện tương ứng. Nêu bước đổi thông tin, M5, dấu vết E5 và giải thích khác; chưa phân xử thì chỉ rõ bằng chứng thiếu.
6. **Phép độ bền.** Như SPEC T-045 bước 7, nhưng thay vế verdict bằng N1 và dùng helper mới. Giữ cách lấy mẫu ô ghép cặp, E_X, phân loại ít ca, δ, δ_d; 1.000 mẫu, seed ghi trước. Mức chính h = 1 giữ cố định. Báo cả mẫu có C-e chưa kiểm được, không bỏ chúng khỏi báo cáo.
7. **Độ nhạy mức HẠI.** Với h = 0,5 và h = 2, dùng cùng kết quả đã có để tính lại tất cả cặp luật C ở ba thế giới, kết hợp thế giới, rồi chạy lại toàn bộ bộ chọn khối bước 1–8 và 10. Báo cấu hình bị loại, tập gần tốt nhất, cấu hình thắng, cờ và xung đột tại từng mức trong `khoi-k.json`. Không chỉ đổi cờ C-e hoặc đếm cấu hình bị loại. Chỉ báo cáo; không chọn lại h, không thay lựa chọn chính bằng mức thuận lợi.
8. **So với T-045 và bảng 2×2.** Theo mục dưới. T-047 là lượt hiệu lực cho task (2); không chọn giữa hai lượt.
9. **Báo cáo.** Tách quan sát, suy luận, ứng viên, kết cục theo luật và câu hỏi mở; manifest, LOG, dòng STATE và prompt cho Claude.

## Bảng 2×2 tại P

Với từng cấu hình khối K trên cùng 52 ca, lập bốn ô:

| Bộ cổng | S0 | S1 |
|---|---|---|
| G0/D0 | `blocks` của T-045 | `extra.T4c.blocks` của T-045 |
| G3/D1 | Phục dựng S0 từ bản ghi S1 T-047 | `blocks` của T-047 |

Phục dựng S0 bằng cách trải thực thể từ các khối S1, bỏ phần tử độ lớn, sắp lại theo khóa còn lại rồi gộp khóa bằng nhau. Không chỉ xóa phần tử và giữ thứ tự cũ. Kiểm phục dựng khớp trước khi dùng.

Lưu trong `so-sanh-t045.json`:
- MRR gộp trên 52 ca và MRR từng dataset cho từng ô, từng cấu hình;
- chênh S1−S0 khi giữ bộ cổng;
- chênh giữa hai bộ cổng khi giữ thang điểm;
- phần thay đổi tương tác, đối chiếu theo ca và phạm vi trung gian đã kiểm.

G3 và D1 được xét như một gói, chưa tách tác động riêng. Phép so đầy đủ này ở P; không tuyên bố đã có đầy đủ bốn ô tại S_lo/S_hi. Có thể chiếu S1 về S0 tại từng thế giới của bản ghi mới, nhưng dữ liệu T4c cũ ngoài P chưa đủ cho toàn bảng.

Không cần chạy chuỗi riêng chỉ để đổi thang nếu bản ghi đủ. Nếu thiếu trung gian hoặc kiểm phục dựng lệch, trình đúng phần cần bổ sung và chi phí; không tự chạy thêm hoặc thu hẹp câu hỏi. Bảng 2×2 không dùng chọn lại thang điểm, cổng hoặc lượt chạy.

## Tiêu chí xong

1. Bộ test cũ qua; hồi quy helper và tích hợp mới đã chạy, có kết quả, không còn lệch chưa xử lý.
2. T1 bất biến đạt, QT5 hợp lý; đối chiếu khớp phần thật/C-e tương ứng của bước 10 T-046. T-046 đã kiểm cả R0 và K-đủ, gồm A/A; T-047 không tự nhận đã chạy lại toàn bộ A/A.
3. Đủ 16 × 52 bản ghi thật và 16 × 30 bản ghi giả; không bỏ ca lỗi; hash pha 1 ghi trước pha 2.
4. Luật C mới giữ UV-6, điều kiện E5, không lặp `M_cong_M_phay`; có `khong_moc_gia` và `ket_hop` tính lại đúng.
5. Luật chọn khối chạy đủ bước 1–8 và 10; có lựa chọn chính kèm cờ hoặc xung đột đã trình Minh.
6. D2 khớp 12/12.
7. Độ nhạy 0,5 và 2 đã chạy lại toàn bộ bộ chọn; bootstrap dùng cùng helper và mức chính.
8. Bảng 2×2 ở P có MRR gộp, từng dataset, đối chiếu và nguồn trong `so-sanh-t045.json`.
9. Phân tích cơ chế đúng phạm vi; phần chưa phân xử có bằng chứng thiếu và quyết định phụ thuộc.
10. Mọi lần nhìn số dev được ghi. Báo cáo không đồng nhất hoàn thành task với hiệu chuẩn cổng, xác nhận cơ chế hoặc hiệu quả RCA.

## Không làm

- K-b, T6–T12, KB, T13, A4, hồ sơ G3.
- T4/T4b mới hoặc thay α, ε; phần cần trước G3 phải trình Minh.
- Đổi ma trận, tham số, mức HẠI hoặc luật chọn sau khi thấy số; chọn giữa T-045 và T-047.
- Sửa `src`; đọc dữ liệu khóa; chạy cloud.
- Commit hoặc push khi chưa có duyệt riêng.

## Chi phí và dừng

- Lượt chính gồm 1.550 lượt cấu hình–ca: T1 238, khối K 1.312; cộng lượt thử và kiểm helper.
- Bảng 2×2 và độ nhạy mức HẠI dùng hậu xử lý trên kết quả, không thêm lượt chuỗi chỉ để đổi thang/ngưỡng.
- Dự báo chưa kiểm: chạy thử 5–15 phút; T1 1–2 giờ; khối K 1,5–4 giờ; pha 2, độ bền và đối chiếu 10–30 phút; tổng khoảng 3–6,5 giờ.
- Tối đa 4 tiến trình local. Xử lý các cấu hình cùng ca trong một tiến trình để dùng cache; đo lại trước khi tin mức tiết kiệm.
- Trần tổng gói chạy là 7 giờ thời gian thực. Lượt thử, lượt hỏng và lượt chạy lại đều được giữ và tính trong ngân sách. Thời gian chờ Minh không tính là thời gian chạy.
- Dự báo vượt trần hoặc tới trần thì dừng, giữ đầu ra và trình Minh; không tự nới ngân sách hoặc bỏ phép kiểm cho vừa thời gian.

## Rủi ro và câu hỏi mở

- Mức HẠI chưa hiệu chuẩn và không trung tính với số kênh.
- Cổng chưa đạt hiệu chuẩn; `verdict` P7 chưa chọn.
- E5 có lợi cấu trúc trên vế xét N1 tăng; S1 không tác động lên vế này.
- Vài ô gần ngưỡng có thể làm lựa chọn đổi; độ bền chỉ mô tả mức mong manh trên dev.
- Tác động của mức HẠI trên toàn khối G3/D1 và lợi ích RCA còn chưa biết.
- Đồng thuận phản biện không thay bằng chứng thực nghiệm hoặc quyền mở test.

## Prompt bàn giao

Người làm soạn prompt theo `docs/review-prompt.md` cho Minh chuyển thủ công. Vẫn soạn khi đề xuất dừng phản biện. Không tự gửi hoặc tự mở lượt phản biện.
