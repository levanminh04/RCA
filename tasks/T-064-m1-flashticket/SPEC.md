# T-064 — M1-FlashTicket: phát triển từ bản P7 và chọn ứng viên

- **Trạng thái:** đã duyệt (13/11/2026, Minh duyệt tổng thể gói chiến dịch).
- **Người làm:** Claude. **Người phản biện:** Codex.
- **Bổ sung đã duyệt 13/11/2026:** áp dụng phần bổ sung cuối file về triển khai theo đầu vào từng hướng và quyền lựa chọn ứng viên. Căn cứ ở `docs/DECISIONS.md`, mục “Bổ sung quyền điều phối chiến dịch nhiều ngày”.
- **Thuộc:** `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` chặng 4 ("Chạy M1 … trên dữ liệu phát triển. Thử cho M1 dùng thông tin giàu hơn … Mỗi thay đổi là một thành phần có đối chứng bỏ nó; tiêu chí chọn khai trước"). Phần "và baseline" của chặng 4 **không** nằm trong task này (Minh chốt: so baseline sau khi M1 khóa). Hồ sơ chiến dịch: `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`.

## Mục tiêu

Lấy M1 bản P7 đã khóa làm nền, phát triển bản thích nghi FlashTicket: khai thác dữ liệu quan sát phong phú hơn và xử lý hạn chế bộc lộ khi áp dụng thực tế. Đầu ra là **một ứng viên M1-FlashTicket Claude đề xuất chọn** để Minh xem xét tiếp — chưa phải bản khóa. Task là thiết kế + cài đặt + chọn trên dev; không khẳng định lợi ích so với baseline, không trả lời RQ5.

DT18/cô: đồ thị phải có vai trò tính toán rõ (AGENTS luật 18) — mỗi hướng ghi nút, cạnh, nơi đặt log/trace/metric và phép tính dùng cạnh.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Phép kiểm | Kết quả có thể | Phụ thuộc |
|---|---|---|---|
| Trên dev FlashTicket, P7 xếp gốc ở đâu theo từng ô, kết luận gì ở ca không tiêm lỗi? | Chấm P7 theo `results/T-064/tieu-chi-chon.md` | Mốc so | — |
| Mỗi hướng H1–H8 có cải thiện xếp hạng hoặc kết luận ở ca không tiêm lỗi mà không làm xấu đại lượng kia? | Thêm riêng vào P7; bỏ khỏi bản gộp; từng ca | Giữ / bỏ / đánh đổi / không thử được | Bản đề xuất |
| Vì sao mỗi ca thay đổi? | Lần đầu vào → bước xử lý → trung gian → đầu ra, so ca đổi với ca không đổi | Cơ chế / chưa phân xử | Hồ sơ giữ/bỏ |
| Quan hệ (cạnh) có tác dụng tính toán không? | Đối chứng bỏ quan hệ trên cùng bản | Báo theo ô | Phạm vi kết luận về đồ thị |

## Đầu vào

`src/m1/` (bản P7, **chỉ đọc**; cấu hình khóa `results/T-058/dem-2026-11-10/m1-p7-config.json`); `src/p3/danh_gia.py` (bộ chấm); dữ liệu dev bản 2 của T-063 (`results/T-063/ca/`, `o-dev-bo-sung.json`); 9 ca T-062 + `ca/_metric-bo-sung/`; `results/T-059/danh-muc-loi.json`; `results/T-062/chay/thu-gia/LAN-CA-NEN.md`. Môi trường ghim: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe` với `PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages`. Không đọc dữ liệu khóa.

## Các hướng

H1 nút DB/cache/broker + xếp hạng cạnh · H2 kênh JVM/cgroup · H3 kênh pool · H4 kênh queue · H5 thành phần "chết im" · H6 thao tác nền · H7 tải tăng so với sự cố · H8 điều chỉnh khác (sàn độ lớn E4, adapter khi container tạo lại, kênh log nghiệp vụ, và điều chỉnh khác **có lý do kỹ thuật ghi trước**). Bảng lý do, dữ liệu cần, ô phân xử: `CHIEN-DICH-M1-FT.md` mục 4.

## Đầu ra

- `src/m1_ft/`: gói mới (dùng lại `src/m1` qua import; mọi thay đổi bật/tắt bằng cấu hình để có đối chứng bỏ nó); test đơn vị.
- `results/T-064/`: `tieu-chi-chon.md` (đã có, khóa trước khi chấm); `so-bien-the.jsonl`; `bien-the/<mã>/` (cấu hình, hash code, đầu ra từng ca, hai lần chạy); `cham/` (bảng nút, bảng cạnh, ca không tiêm lỗi, từng bản × từng ca); `co-che/` (phân tích từng ca thay đổi và ca sai còn lại); `chu-thich-thao-tac-nen.md`; `ho-so-chon.md` (bản đề xuất, bản thay thế nếu có đánh đổi, giữ/bỏ từng thay đổi và vì sao, tổng số bản đã chấm, giới hạn); `cau-hinh-de-xuat.json`; kết quả định dạng T-061 cho dashboard (T-065); `manifest.json`.

## Phạm vi ghi

`src/m1_ft/`; `results/T-064/`; `tasks/T-064-m1-flashticket/`; dòng T-064 trong `docs/STATE.md`; `docs/WHY.md`, `docs/DECISIONS.md` theo quyền ở `CHIEN-DICH-M1-FT.md` mục 6. **Không** sửa `src/m1/`, `src/p3/`, `results/` của task khác.

## Các bước

1. Kiểm chuỗi xếp hạng → chuyển đổi → chấm; đếm nhóm hòa ở hạng 1 của 5 ca lỗi T-062; xác nhận bộ chấm P3 dùng được cho bản FlashTicket. Ghi hash `tieu-chi-chon.md` vào LOG. — không phụ thuộc.
2. Dựng `src/m1_ft` chạy **y hệt P7** khi tắt mọi thay đổi (kiểm: trùng SHA đầu ra với P7 trên 9 ca T-062). — không phụ thuộc.
3. Cài các hướng không cần dữ liệu mới trước (H6, H7, H8-sàn độ lớn, H8-adapter) và thử trên 9 ca T-062 **chỉ để kiểm cài đặt** (không dùng để chọn). — sau bước 2.
4. Cài H1–H5, H8-log khi T-063 có tín hiệu tương ứng.
5. Khi có dev bản 2: khai tập chọn → chấm P7 → chấm biến thể theo sổ → phân tích cơ chế → tổ hợp có căn cứ → lặp tới tiêu chí kết thúc.
6. Kiểm không hồi quy trên 9 ca T-062; kiểm độ nhạy mốc; hồ sơ chọn.
7. Xuất kết quả cho T-065; mục kết thúc LOG; prompt bàn giao cho Codex phản biện.

## Kiểm đúng đắn

Trước khi chấm một biến thể: hai lần chạy trùng SHA; đếm đầu vào thật của thành phần mới (số kênh, nút, cạnh, mẫu); đếm lần rơi nhánh dự phòng; soi giá trị trung gian (QT5). Một trạng thái đồng loạt (100% không đổi, 100% không hỗ trợ) phải lần tới đầu vào trước khi diễn giải (SL39). Không đưa nhãn, tên ô, mốc tiêm (ngoài `t` của chế độ a) vào phương pháp; ngưỡng mới không được chỉnh theo đáp án từng ca mà phải có nguyên lý ghi trong sổ.

## Tiêu chí xong

Theo `CHIEN-DICH-M1-FT.md` mục 5 (a)–(d). Kết quả "không hướng nào đạt luật giữ" là đầu ra hợp lệ nếu đã thử đủ và có cơ chế. Được phép rút ra: "ứng viên M1-FT đề xuất trên dev bản 2, so với P7". Không được rút ra: tốt hơn baseline; hiệu quả trên tập đánh giá; lợi ích đồ thị nói chung.

## Không làm

Không so baseline; không dùng ô đánh giá, dữ liệu khóa; không sửa P7; không khóa bản cuối; không chạy lặp để chọn.

## Chi phí ước lượng

Chưa kiểm: 3–5 ngày làm việc là **mốc báo tiến độ**, không phải trần. M1 chạy khoảng 4 s/ca (số của T-062); chạy trên laptop hoặc `exp-obs`.

## Rủi ro và điều chưa chắc

Mỗi ô một lần thu → không đo được dao động; chọn trên dữ liệu đã xem → lạc quan; nhiều biến thể trên ít ca → nguy cơ khớp quá (báo tổng số bản đã chấm). Chưa kiểm bộ chấm P3 với đầu ra có cạnh.

## Bổ sung đã duyệt — phát triển song song, 13/11/2026

Phần này cụ thể hóa phụ thuộc các bước 3–7, giữ tiêu chí đã ghi tại `results/T-064/tieu-chi-chon.md` và phạm vi kết luận của task.

- T-064 chạy song song với T-063 theo đầu vào từng hướng. Có thể thiết kế, cài, kiểm đơn vị và đường xử lý trước khi cả đợt thu xong. Khi một gói ca đã kiểm toàn vẹn và đầu vào của hướng đã xác nhận, có thể tính trên gói đó theo tập chọn đã khai. Kết luận giữ/bỏ và chọn bản cuối cần đủ các ca của phép so tương ứng.
- Claude tự mở rộng biến thể, chi tiết tham số và tổ hợp H1–H8 khi có căn cứ kỹ thuật. Ghi sổ trước khi chấm, giữ mọi đầu ra và áp dụng cùng tiêu chí đã khai. Lựa chọn quan trọng ghi WHY trước khi dùng trong kết quả. Quyền đổi tiêu chí sau khi xem kết quả vẫn theo hồ sơ chiến dịch.
- Giữ phép kiểm tương đương P7 khi tắt mọi thay đổi, cùng đối chứng thêm/bỏ thành phần. Chỉ dùng kết quả có đầu vào đã kiểm để nhận xét hiệu quả, kết quả kiểm cài đặt được ghi đúng vai trò.
- Thống nhất hợp đồng đầu ra với T-065 sớm, bàn giao đầu ra thử có truy vết khi sẵn sàng để tích hợp, rồi xuất và kiểm lại trên bản đề xuất cuối. Những ca chưa tính hoặc biến thể chưa chốt được ghi rõ trạng thái.
- Tìm kiếm tiếp tục theo tiêu chí hoàn thành của chiến dịch, có xét tổ hợp và ca sai còn lại. Báo cáo sáng, hết phiên hoặc các ước lượng ngày công không kết thúc task. Claude tự chọn ứng viên theo tiêu chí đã duyệt và ghi đánh đổi, không chờ Minh chọn thay trong phạm vi đã cấp.
