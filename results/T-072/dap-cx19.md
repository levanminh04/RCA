# T-072 — Đáp phản biện CX-19 / CX-19b: đính chính diễn giải, lập luận luật 5xx, K1, chữ sửa WHY-110

Ngày 23/11/2026, người làm Claude T-072. Đầu vào: `results/T-070/codex/CX-19-tin-cuoi.md`, `CX-19b-tin-cuoi.md`; phần cơ học của Codex ở `results/T-072/v2/` (CX-24, CX-24b); đính chính cơ học `results/T-072/dinh-chinh-cx19-co-hoc.md` (CX-25, CX-25b). Bảng đáp từng điểm nằm ở LOG T-072, lượt 13. Không chấm lại E4, không đổi ngưỡng hay quy tắc đã khóa, không commit.

## 1. Đính chính câu "lệch −4 s" (CX-19 F2)

Thay mục "Vì sao lệch đúng −4 s" và "Kết luận" của `e3-doi-chieu-offline.md` (bản cũ giữ nguyên, hash trong `SHA256SUMS-e3-offline`) bằng cách đọc sau:

- **Phạm vi:** chỉ bốn luật thử `t072-thu-p95-*` (bản sao p95, ngưỡng 0,005 s), trong lượt E3 `t071-e3-duong-01`. Không áp cho 11 luật thật.
- **Quan sát:** 12/12 mốc chuyển trạng thái (Pending, Alerting, hết cháy) của offline sớm hơn Grafana 4 s.
- **Diễn giải (phù hợp, chưa phân xử):** con số này **phù hợp với** chênh pha giữa lưới xuất (giây tận cùng 6) và tick Grafana (giây tận cùng 0). Ba giới hạn:
  1. 12 số không độc lập. Alerting = Pending + 60 s ở cả hai phía. Booking và event chuyển cùng lúc, payment và ticket cũng vậy. Thực chất chỉ có khoảng 2 thời điểm vào và 2 thời điểm hết cháy độc lập.
  2. Bản xuất chạy 05:59:58–06:00:34Z, trong khi lưới kéo tới 06:00:26Z. Phần cuối của các truy vấn đầu (booking, event) được tính khi cửa sổ chưa kết thúc. Không có thời điểm mẫu khả dụng ở từng tick, nên **không tách được** pha với độ trễ nạp mẫu. Câu cũ "không thấy dấu hiệu Grafana nhận mẫu trễ" quá mạnh; rút lại. Chuỗi tổng request đọc sau (16,55 < 30 lúc 06:00:16Z, CX-19) ủng hộ việc luật kết thúc do thiếu lưu lượng.
  3. Câu "với luật p95, sự cố đếm từ Grafana và offline phải trùng, khác ≤ 10 s về t̂" **rút lại**: một lượt, hai cặp thời điểm không đủ bảo đảm cho khoảng khác. E4 dùng lịch sử Grafana để đếm trực tiếp, không cần giả định đó.
- **11 luật thật:** chỉ khớp âm (0 = 0). Phần so âm trong bản cũ tính từ 05:15:26Z, trước giờ hiệu lực E3 (05:17:20Z). Giới hạn lại vào 05:17:20–06:00:26Z vẫn là 0 = 0, vì offline không có khoảng cháy nào trên toàn lưới.
- **Sai cần sửa:** câu "booking 0,0931 s … không cháy vì không giữ 60 s" **sai**. 0,0931 < 0,098 nên booking chưa từng vượt ngưỡng thật; việc nó im không liên quan `for`.

## 2. Lập luận cho luật 5xx (CX-19b N2)

- `quy-tac-chon-nguong.json#/thong_ke/gia_tri_duy_tri` viết "θ không gây cảnh báo trên E2 khi và chỉ khi θ ≥ max S(t) (trên lưới xuất)"; WHY-110 viết "θ ≥ max S thì luật không cháy trên E2". Mệnh đề "khi và chỉ khi" đúng cho luật p95, vì S tính trên chính tín hiệu của luật (trên lưới xuất).
- Với luật 5xx, M lấy trên tỷ lệ **chưa chặn** (`phu/ty-le-loi-chua-chan-5xx-*`), còn luật thật có thêm hai chặn: ≥ 30 request và ≥ 3 lỗi 5xx. Vì vậy θ ≥ M là điều kiện **đủ**, không phải điều kiện cần. Phản ví dụ của Codex: 2 lỗi / 32 request = 6,25% > 5%, duy trì 60 s, nhưng luật không cháy vì chưa đủ 3 lỗi.
- **Hệ quả:** không đổi ngưỡng. Ở E2, bốn M lỗi đều bằng 0, nên θ lỗi = sàn 5% không phụ thuộc mệnh đề này. Chỉ sửa câu chữ (mục 4).
- **Giới hạn thêm:** điều kiện ≥ 3 lỗi cộng 5% làm luật im với tỷ lệ lỗi thấp kéo dài, ví dụ 2 lỗi mỗi 5 phút. E4 không có 5xx nào nên luật lỗi chưa bị thử thách (`bang-bao-dong-gia.md`).

## 3. K1 — ghi file trên exp-obs và vị trí scratchpad (CX-19 "phạm vi ghi", CX-19b K1)

- `results/T-072/e4/k1-kiem.sh` tự ghi "CHỈ ĐỌC" nhưng có lệnh `docker logs … > /srv/rca-lab/runs/t072-e3-01-cfg/grafana-log-e4.txt` (19:07Z 22/11). **Đúng là có ghi file trên máy.** File nằm trong vùng của T-072 (I9), không đổi Grafana, Prometheus hay `/opt/rca-lab`. Lúc đó S3 vẫn mở cho T-071, nhưng lệnh không truy vấn Prometheus. Mô tả "CHỈ ĐỌC" trong script là **sai chữ**.
- Hai lần ghi tương tự trong S2 (T-072 là chủ khung), cùng thư mục: `grafana-log-sau-restart.txt` (bước 4) và `grafana-log-sau-g.txt` (bước 10). Hash đã ghi ở LOG.
- **Vị trí scratchpad** (laptop, ngoài repo, thư mục tạm của phiên):
  `C:\Users\84583\AppData\Local\Temp\claude\5926e3c52aa473a7\4dff20c8-4444-4d9c-aa75-26d665a1a122\scratchpad\`
  - Có: `khao-sat-1..3.sh/.out` (bản gốc của bản chép trong `results/T-072/khao-sat/`), `dot-bien/`, `dot-bien2/` (phép đột biến), `xuat-thu-t071/` (giải nén lượt xuất thử của T-071), `tao_v2_claude.py` (bản chép trong `v2/`), `prompt-chung.txt`.
  - Không ghi gì ngoài repo trừ thư mục này và vùng `t072-*` trên exp-obs.

## 4. Chữ sửa WHY-110 (C3) — chỉ soạn; điều phối trình Minh

Giữ nguyên quyết định, công thức, hệ số, sàn và kết quả đầu. Chỉ thay ba gạch đầu dòng, các dòng còn lại giữ nguyên:

- **Vì sao** (thay):
  > θ ≥ max S (S = giá trị duy trì `for` giây trên lưới xuất) là điều kiện để luật p95 không cháy trên E2 theo lưới đó. Với luật 5xx, M lấy trên tỷ lệ chưa chặn số lỗi, nên θ ≥ M chỉ là điều kiện **đủ** (luật thật còn chặn ≥ 30 request và ≥ 3 lỗi). Biên k và sàn dành cho trôi giữa E2 và E4 và cho bucket thô (p95 ~0,03–0,15 s nằm trong bucket 0,025–0,25 s). Sàn lỗi 5% ≈ 3,5 lỗi trên 70 request, khớp WHY-106.
- **Phương án đã xét** (thay):
  > (a) Phân vị cao (ví dụ 99%) của tín hiệu E2: loại, vì cần thêm một tham số tùy ý (mức phân vị) và không gắn với ngữ nghĩa `for`. Một bước vượt phân vị không tất yếu thành cảnh báo, nhưng phương án này *cho phép* các bước trong mẫu vượt ngưỡng. Max S gắn trực tiếp với `for` và không cần tham số đó.
  > (b) Chọn θ trên E2 theo mục tiêu R5: loại. Chọn trên E2 theo một mục tiêu khai trước tự nó **không** làm E4 mất độc lập. Lý do loại là R5 không xác định duy nhất θ: nhiều θ cùng đạt trên E2, nên phải khai trước cách phá hòa. Cách tự nhiên nhất, θ nhỏ nhất vẫn đạt R5, đặt θ sát biên E2 và bỏ phần biên cho trôi giữa E2 và E4.
  > (c) Ngưỡng cố định theo kinh nghiệm: loại, vì không có căn cứ trên hệ này.
- **Điều kiện thất bại** (thêm một ý vào cuối):
  > Trên E3, offline và Grafana lệch −4 s ở bốn luật thử, phù hợp với chênh pha lưới. Phép này không tách được pha với độ trễ nạp mẫu và không đo cho luật thật.
- **Bằng chứng sau khi dùng** (thêm, ghi rõ là sau khi dùng):
  > E4 (khoảng độc lập): 0 sự cố / 383 phút khỏe ×1. Max S / θ: booking 0,48, event 0,46, payment 0,84, ticket 0,84 (`results/T-072/bang-bao-dong-gia.md`). Ticket chỉ cần 4 request > 0,1 s trong 5 phút là vượt θ (mô hình, chưa kiểm; `results/T-072/troi-p95-e2-e4.md`).

## 5. Phần sửa bộ chấm (CX-19 F5) — tóm tắt

`v2/cham_offline_v2_claude.py`, sinh bởi `v2/tao_v2_claude.py` từ bản v2 của Codex; bản Codex giữ nguyên hash `39f56bde…`.
- `quy_ve(…, bat_dau)` theo đúng chữ quy tắc gom đã khóa: t̂ trước đầu khoảng chấm thì xếp `dang-chay-luc-bat-dau` hoặc `truoc-khoang`, không đếm.
- Thêm cờ `pending-truoc-khoang` và `pending-tu-dau-luoi`.
- Cờ `cua-so-lan` so với lớp phút.
- Mẫu số chỉ đếm phút trọn từ đầu khoảng.
- Có 9 ca giả mới, kiểm cả số khoảng cháy. `tu-kiem` 0 sai; đột biến 5/5 bị bắt.
- Phép chấm đã khóa không đổi; E2 và E4 có 0 khoảng cháy, nên không chấm lại.
- Bằng chứng "cháy trước đầu khoảng" cho E4: lịch sử Grafana 0 dòng từ 06:05:54Z tới 19:22Z.
