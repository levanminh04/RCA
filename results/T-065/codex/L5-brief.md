# Brief L5 cho Codex — T-065: kiểm giao diện thật trên Chrome và sắp xếp folder Grafana (14/11/2026 ~04:00Z)

Minh dán brief này vào **Codex app**. Đặt thư mục làm việc của cuộc trò chuyện là `D:\RCA-flashticket`.

Bạn là Codex (`gpt-6.1-sol`, reasoning high), **người làm** T-065. Claude là **người phản biện** và điều phối chiến dịch M1-FlashTicket.

Căn cứ quyền trong `docs/DECISIONS.md`:
- mục "Bổ sung quyền điều phối chiến dịch nhiều ngày";
- mục "Hook thử H3, folder Grafana, Codex kiểm giao diện qua Codex app, 14/11/2026" (chép nguyên lời Minh).

**Minh yêu cầu kiểm đủ, không tự thu hẹp.** Làm hết các việc dưới đây trong khả năng của bạn. Việc nào không làm được thì vẫn làm các việc còn lại, rồi báo đúng việc nào, vì sao, đã thử gì, bằng chứng còn thiếu. Ghi đủ để Claude tiếp nhận mà không cần hỏi lại.

## 0. Đọc trước (bắt buộc)

1. `AGENTS.md`.
2. `tasks/T-065-giao-dien-grafana/SPEC.md` toàn bộ, gồm phần bổ sung cuối file. `tasks/T-065-giao-dien-grafana/LOG.md` các mục L3, L4.
3. Các file trong `results/T-065/`:
   - `XONG.md`;
   - `CHECKPOINT.md` (các mục L4);
   - `kiem/002/BAO-CAO.md`;
   - `README.md` và README-L4;
   - `thay-doi-may.md`;
   - `prompt-ban-giao.md`.
4. `results/T-064/ban-xuat/chi-muc-ban.json`: ba bản × 22 ca, nguồn của mọi số hiển thị.
5. `tasks/T-065-giao-dien-grafana/REVIEW.md`, điểm P1–P4.

## 1. Ghi trạng thái để điều phối biết bạn đang chạy

Ngay khi bắt đầu, tạo `results/T-065/codex/L5-trang-thai.json`.
- Trường: `ten: "L5"`, `trang_thai: "dang_chay"`, `nguon: "codex-app"`, `cap_nhat` (giờ UTC), `buoc`.
- Cập nhật file này sau mỗi bước con.
- Khi kết thúc, đặt `trang_thai` là `xong` (đủ), `mot_phan` hoặc `dung` (kèm lý do), rồi ghi giờ.
- Phiên Claude điều phối đọc file này để không phát lượt trùng.

## 2. Sắp xếp folder Grafana (làm trước, để bước 3 kiểm luôn cấu trúc cuối)

Hiện trạng:
- Provider `rca-g2` dùng `folder: RCA`, `foldersFromFilesStructure: false`.
- Sáu dashboard nằm phẳng trong `/opt/flash-ticket-obs/pinned/provisioning/dashboards/` (trong container là `/etc/grafana/provisioning/dashboards/`).
- Grafana 13.3.0.

**Cấu trúc đích** (Claude chọn theo giao quyền của Minh):

```
RCA FlashTicket/
├── 0 · Bắt đầu tại đây/
│     └── "Mục lục RCA"   (dashboard mới, UID mới)
├── 1 · Kết quả hiện hành/
│     ├── t065-l4-rca        (RCA — chọn bản M1 cùng ca)
│     └── t065-l4-phat-lai   (phát lại có đáp án, T-062)
└── 9 · Lưu trữ/
      ├── L3 · P7 · 13-11/      t065-rca, t065-phat-lai
      └── G2 bản 6 · 12-11/     rca-g2-chinh, rca-g2-phat-lai
```

**Quy tắc:**
- **Giữ nguyên UID của mọi dashboard cũ**, để liên kết và bookmark không gãy.
- **Không sửa byte nào trong JSON của dashboard L3 và bản 6.** Hai bản này là mốc hồi quy; chỉ chuyển file sang thư mục con.
- Dashboard L4 được sửa tiêu đề và tag nếu cần, cho dễ đọc. Ghi hash trước và sau.
- **Dashboard "Mục lục RCA"** là một panel văn bản. Mỗi dòng gồm:
  - tên và liên kết theo UID;
  - dùng để làm gì;
  - bản M1 đang hiển thị (P7 khóa, V032-H5b đề xuất tạm, V041 thay thế có cạnh);
  - số ca;
  - task và lượt tạo;
  - ngày tạo;
  - trạng thái "hiện hành" hoặc "lưu trữ";
  - giới hạn đã biết (hash cấp bản P7 là `null`, dev chưa có đáp án cho giao diện).

  Không hiện đáp án trên trang này.
- **Thư mục lồng nhau:** kiểm Grafana 13.3 có tạo thư mục lồng từ cấu trúc file không (`foldersFromFilesStructure: true`, rồi xác nhận bằng API folders sau khi nạp lại).
  - Có: dùng cấu trúc lồng như trên.
  - Không: dùng thư mục phẳng có tiền tố, cùng thứ tự: `RCA FT · 0 Bắt đầu`, `RCA FT · 1 Hiện hành`, `RCA FT · 9 Lưu trữ L3`, `RCA FT · 9 Lưu trữ G2`.
  - Ghi phương án đã dùng và bằng chứng.
- Mọi file dashboard phải nằm trong thư mục con. File ở gốc sẽ rơi vào General.
- Folder `RCA` cũ: nếu sau khi chuyển đã rỗng thì được xóa, ghi lại. Còn dashboard nào thì giữ và báo.
- Mỗi thay đổi ghi vào `results/T-065/thay-doi-may.md`: lệnh, giờ UTC, hash trước và sau, cách hoàn tác. Hoàn tác là trả `provider.yaml` và vị trí file về cũ, rồi restart Grafana.
- Restart riêng container Grafana khi cần nạp lại.
- **Sau khi chuyển, kiểm bằng API:**
  - đủ 7 dashboard, đúng folder;
  - UID không đổi;
  - JSON của L3 và bản 6 trùng hash cũ;
  - liên kết giữa các dashboard còn mở được.

## 3. Bấm thật trên Chrome (phần chính, phần L4 còn thiếu)

Dùng Chrome của Minh, Grafana đã đăng nhập sẵn.
- **Mở tab mới.** Không đóng hay đổi tab Minh đang mở. Không xem trang hoặc tab nào ngoài Grafana của dự án.
- **Không nhập mật khẩu.** Nếu bị đăng xuất, dừng phần trình duyệt, ghi lại và báo Minh đăng nhập lại.
- **Trên Grafana chỉ xem**, ngoại trừ dashboard mới ở bước 2 (làm qua file provisioning, không qua giao diện). Không bấm Save. Không sửa datasource, cài đặt, người dùng, plugin, alert hay quyền.

### 3a. Phủ đủ, mức 1 (mọi cặp)

Áp cho **3 bản × 22 ca = 66 trang ca**, mỗi trang mở bằng điều hướng trên giao diện hoặc URL. Kiểm và ghi:
- tên bản, trạng thái, hai hash cấp bản, nguồn đầu ra, cửa sổ `[t−300, t+300)`;
- vài dòng đầu bảng xếp hạng khớp `entity_ranking`: thứ tự, `tie_group + 1`;
- panel cạnh: V041 có bảng cạnh khớp nguồn; P7 và V032 hiện "không có đầu ra cạnh";
- không panel nào báo lỗi;
- panel rỗng có lời giải thích;
- mỗi trang chụp một ảnh.

### 3b. Phủ sâu, mức 2

**Phạm vi:**
- Mỗi bản ít nhất 3 ca T-062 và 3 ca dev bản 2. Bắt buộc có ca `1ad3afeb` (Minh đang mở: V041, event-service, `SELECT event_db`).
- Mỗi ca ít nhất 2 service, gồm service xếp hạng 1.
- Mỗi service ít nhất 2 thao tác, gồm ít nhất một thao tác có cờ, nếu có.
- Ghi lý do chọn mẫu. Thấy lỗi thì mở rộng mẫu quanh chỗ lỗi.

**Luồng cần đi:**
1. Mục lục → dashboard hiện hành → danh sách ca → chọn ca.
2. **Đổi bản trên cùng ca:** ca, cửa sổ và service phải giữ nguyên.
3. Service → bảng thao tác và đồ thị thao tác → chọn thao tác.
4. **Bấm từng loại liên kết bằng chứng:** Tempo, Loki, Prometheus. Kiểm:
   - đúng datasource, truy vấn, khoảng giờ;
   - có dữ liệu;
   - nếu rỗng thì đối chiếu với `api-snapshot.json` xem có khớp trạng thái "rỗng" đã xuất không.
5. Quay lại; điều hướng ngược.
6. **Trang phát lại** (ca T-062): đáp án nằm riêng, trang chính không có đáp án.

**Panel rỗng:** mỗi panel rỗng gặp phải, phân loại:
- (i) đúng là nguồn không có dữ liệu, có bằng chứng truy vấn;
- (ii) lỗi hiển thị hoặc truy vấn;
- (iii) chưa phân xử được, kèm bằng chứng cần thêm.

Không suy nguyên nhân khi chưa có bằng chứng.

**Hiển thị:**
- bố cục đọc được ở kích thước cửa sổ thường;
- màu và chú giải (LOW_SUPPORT tím theo quy tắc L3);
- node graph dựng xong, ghi thời gian chờ;
- chữ không bị cắt mất thông tin quan trọng.

**Đồ thị dạng canvas** không đọc được bằng DOM: kiểm bằng ảnh (có dữ liệu, đúng khoảng giờ, đúng chuỗi). Số liệu chi tiết đã đối chiếu bằng API ở L4. Ghi rõ phần nào kiểm bằng ảnh, phần nào bằng DOM hay URL.

### 3c. Giữ an toàn cho máy

`exp-obs` có 2 lõi. Grafana giới hạn 768 MiB và từng bị hết bộ nhớ lúc 01:39:46Z.
- Bấm tuần tự, không mở song song nhiều trang nặng.
- **Trước mỗi nhóm trang nặng** (node graph, tìm kiếm Tempo), đọc `docker stats --no-stream` của Grafana qua SSH `exp-obs` và ghi lại.
- Nếu Grafana restart: dừng, ghi sự kiện Docker, giảm nhịp rồi làm tiếp. Không đổi giới hạn bộ nhớ.
- **Có thể đang có đợt thu bù dữ liệu (T-063)** trên `exp-app`/`exp-obs`. Trước mỗi nhóm trang nặng, kiểm `ps -eo cmd | grep -c "[p]ython3 -B runner3"` trên `exp-obs`. Kết quả > 0 thì chỉ mở trang nhẹ, hoãn tìm kiếm Tempo và node graph tới khi hết, và ghi lại.

## 4. Sửa lỗi tìm thấy

- Được sửa lỗi giao diện trong quyền T-065:
  - nguồn dashboard, bộ xuất và dữ liệu trong `results/T-065/`;
  - file dashboard L4 và Mục lục trên máy.
- Mỗi sửa có lỗi gốc (ảnh, URL), thay đổi, hash trước và sau, và kiểm lại cả luồng chịu ảnh hưởng.
- **Không sửa:**
  - dữ liệu M1, hạng, cờ;
  - `results/T-064/`, `src/`, `docs/`;
  - dashboard L3 và bản 6.
- Lỗi nằm ngoài quyền thì ghi và chuyển Claude. Ví dụ: hai hash cấp bản P7 là `null` trong chỉ mục T-064.

## 5. Đầu ra và bàn giao (bắt buộc, tránh thất thoát)

**Thư mục `results/T-065/kiem/003-trinh-duyet/`:**
- `anh/`: ảnh đặt tên `<stt>-<trang>-<bản>-<ca>[-<service>-<thao tác>].png`.
- `nhat-ky-bam.jsonl`: mỗi thao tác một dòng gồm giờ UTC, URL trước và sau, hành động, kỳ vọng, quan sát, kết quả, ảnh.
- `doi-chieu-hien-thi.json`: giá trị đọc trên màn hình so với nguồn, theo từng trang.
- `panel-rong.json`: từng panel rỗng và phân loại (i), (ii), (iii).
- `may.jsonl`: các lần đọc bộ nhớ Grafana, trạng thái `runner3`, restart nếu có.
- `loi-va-sua.md`: từng lỗi, mức ảnh hưởng, đã sửa hay chưa, kiểm lại.
- `BAO-CAO.md`: phạm vi đã phủ (số trang, ca, bản, liên kết từng loại), kết quả, phần chưa làm được và lý do, giới hạn.

**Các file khác:**
- `results/T-065/BAN-GIAO-L5.md` cho Claude:
  - trạng thái từng yêu cầu của SPEC T-065 (G-a, G-b, G-c) và điểm P1–P4: đạt, một phần, chưa;
  - bằng chứng kèm đường dẫn;
  - việc còn mở;
  - quyết định cần Minh;
  - việc cần Claude kiểm;
  - lệnh cuối đã chạy.
- `XONG.md`, `CHECKPOINT.md`, `manifest.json` (băm mọi file mới hoặc đổi), `thay-doi-may.md`.
- Mục L5 trong `tasks/T-065-giao-dien-grafana/LOG.md`, chỉ ghi thêm.
- `prompt-ban-giao.md`: prompt cho Claude kiểm độc lập. Chép nguyên văn "Prompt chung" và khối công đoạn phù hợp của `docs/review-prompt.md`; chỉ điền thông tin trung tính.

**Checkpoint:** ghi `results/T-065/CHECKPOINT.md` sau mỗi bước con và ít nhất 30 phút một lần: giờ UTC, bước, đầu ra, bước tiếp, tab hoặc tiến trình còn mở.

**Nếu hết hạn mức giữa chừng:** checkpoint, `L5-trang-thai.json` và các file đầu ra phải đủ để lượt sau làm tiếp mà không mất phần đã kiểm. Bộ kiểm phải lưu theo từng trang.

## 6. Giới hạn cứng

- Không chạm `exp-app` ngoài đọc; không chạm máy 84 (52.64.237.84).
- Không đọc `data/locked/`, `.env`, `grafana.env`, `~/.ssh`, lịch sử shell.
- Không in, không ghi mật khẩu hay token vào file, log, ảnh hay báo cáo. Ảnh không được chụp trang chứa bí mật.
- Không commit, push hay merge.
- Không ghi `docs/STATE.md`; phiên điều phối cập nhật.
- Có file `D:/RCA-overnight/STOP` hoặc `~/rca-dieu-phoi/STOP` trên `exp-obs` thì dừng ở ranh giới gần nhất.
- Nếu lượt kéo dài hơn 1 giờ, ghi trước vào CHECKPOINT: gặp lỗi ở 10%, 50%, 99% thì xử lý thế nào, chạy lại gì (luật 21).

## 7. Tóm tắt cuối lượt (trong chat Codex app)

1. Đã làm gì.
2. File đã đổi, trên repo và trên máy.
3. Kiểm đã chạy và kết quả, có số.
4. Điều chưa chắc hoặc chưa làm được, và lý do.
5. Đường dẫn `BAN-GIAO-L5.md`.
