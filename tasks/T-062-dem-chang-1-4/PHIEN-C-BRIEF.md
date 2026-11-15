# Brief phiên C — T-064: H8-adapter, H8-log và phép dời mốc ±30 s

Ghi ngày 14/11/2026 ~04:45Z. Phiên tương tác `ed8b9c01…` mở phiên này theo duyệt của Minh: "duyệt mở phiên B C, lên plan kĩ lưỡng, prompt ghi chuẩn, không viết sơ sài".

Bạn là **Claude**, vai trò **người làm T-064** cho ba phần dưới đây. Người phản biện T-064 là Codex.

Phiên điều phối (lịch 15 phút, chủ ghi trong `tasks/T-062-dem-chang-1-4/DIEU-PHOI-TRANG-THAI.json`) **cũng là người làm T-064**. Hiện nó giữ đối chứng bỏ quan hệ (lô lượt 4 trên `exp-obs`, mã nguồn `goc-9`), hồ sơ chọn và tích hợp. Hai phiên chia việc như sau, không làm trùng:
- **Phiên C làm:** H8-adapter, H8-log, phép dời mốc ±30 s, từ cài tới chấm và phân tích cơ chế.
- **Điều phối làm:** lượt 4, `ho-so-chon.md`, `tieu-chi-chon.md` (khóa), tích hợp bản cuối, `cau-hinh-de-xuat.json`, manifest, phản biện Codex.

## 0. Bối cảnh bắt buộc đọc trước

1. `AGENTS.md`: Luật 0, luật cứng 1–21 (đặc biệt 3, 5, 6, 14, 15, 18, 20, 21), mục 5, 7.
2. `docs/DECISIONS.md`, mục "Bổ sung quyền điều phối chiến dịch nhiều ngày" và các mục ngày 13–14/11.
3. `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`, mục 4 (hàng H8) và mục 5 (tiêu chí kết thúc).
4. `tasks/T-064-m1-flashticket/SPEC.md` toàn bộ, gồm phần bổ sung; `tasks/T-064-m1-flashticket/LOG.md` dòng 20–40 (H8) và hai mục cuối.
5. `results/T-064/`:
   - `tieu-chi-chon.md`, **đã khóa**: không đổi;
   - `ho-so-chon.md`, đặc biệt mục 4, 8, 9, 10 và tiêu chí (a)–(d);
   - `so-bien-the.jsonl`: các dòng cuối, để biết mã biến thể tiếp theo;
   - `hop-dong-dau-ra.md`.
6. `docs/WHY.md` từ WHY-81 trở đi (WHY-81 tất định trên ARM `exp-obs`; WHY-85 sàn 1 ms; WHY-86 H5b). `docs/LESSONS.md` khi chọn tham số và diễn giải.
7. Mã:
   - `src/m1_ft/chay.py`, `chay_ca.py`, `bo_sung.py`, `cham.py`, `thanh_phan/*.py` (mẫu thành phần: `h8_san.py`, `h7_tai.py`);
   - `src/m1_ft/tests/test_cham.py`;
   - `src/m1/` **chỉ đọc**, đặc biệt `adapter_flashticket.py`: đọc chỗ ném `Multiple runtime series map to one logical metric`.
8. Công cụ lô: `results/T-064/kiem/` (`ghi_so_chon_dev2_luot3.py`, `chay_bien_the_obs_luot4.sh`, `nhan_luot3.sh`, `kiem_luot3.py`, `goi-tai-len-*.sha256`, `ca-dev2-13.txt`, `ca-t062-9.txt`) và `results/T-064/cham/` (`cham_dev2.py`, `cham_kiem_cai_dat.py`, `giu_bo.py`), dùng như công cụ, không sửa bản cũ.
9. Môi trường ghim laptop: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe` với `PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages`. Trên `exp-obs`: user `rca`, venv P7 `/opt/flash-ticket-rca/venv`.

## 1. Mục tiêu và vì sao

M3 tiêu chí (a) đòi mỗi hướng có ít nhất một bản đã cài, kiểm không nhãn và chấm. H8 có ba điều chỉnh đã khai trong hồ sơ chiến dịch. H8-sàn đã chấm; **H8-adapter và H8-log chưa cài**.

SPEC T-064 bước 6 và tiêu chí §7 đòi **kiểm độ nhạy mốc** (dời `t` ±30 s), hiện chưa làm. `chay_ca.py` chưa có tham số dời `t`.

## 2. Việc cụ thể

### 2a. Phép dời mốc ±30 s (làm trước: rõ nhất, không cần dữ liệu mới)

1. Thêm tham số `--doi-t <giây>` vào `src/m1_ft/chay_ca.py`, mặc định 0.
   - Khi 0, đầu ra **trùng byte** với hiện nay. Kiểm bằng phép tương đương P7: `kiem/tuong_duong_p7.py`, hoặc so SHA với đầu ra P7 đã có trên vài ca.
   - Khi khác 0, dời `t` ở **mọi nơi M1 dùng `t`**: `inputs[5]`, cửa sổ cắt, gói bổ sung.
   - Đọc kỹ chỗ kiểm `t_req != inputs[5]` và `goi.get('t') != inputs[5]`. Dời nhất quán, không tắt phép kiểm. Ghi rõ cách xử lý gói metric bổ sung, vốn xuất sẵn ±300 s quanh `t` gốc: dời 30 s thì một phần cửa sổ nằm ngoài gói. Ghi giới hạn này, hoặc chứng minh nó không ảnh hưởng.
   - Ghi `doi_t` vào `summary.json` và phần `extra` của đầu ra, để truy vết.
2. Bản cần chạy: P7, V032-H5b (đề xuất tạm) và V041 (thay thế có cạnh). Lấy cấu hình theo sổ và theo `results/T-064/ban-xuat/chi-muc-ban.json`.
   - Chạy với `doi_t` ∈ {−30, +30} trên 13 ca dev bản 2 và 9 ca T-062.
   - **Ghi sổ trước khi chạy:** vai trò `do_nhay_moc`, khai là kiểm độ nhạy, không phải biến thể để chọn.
3. Chấm như cũ. Báo theo từng ô: đổi hạng, đổi kết luận ở ca không lỗi, cờ cạnh. So với `doi_t = 0` cùng bản.
4. Diễn giải theo luật 14: tách quan sát, suy luận và câu hỏi mở. Kết quả "nhạy" ở ô nào thì lần theo cơ chế (luật 15): cửa sổ cắt mất phần nào của tín hiệu.

### 2b. H8-adapter — container bị tạo lại trong cửa sổ

1. Đọc `src/m1/adapter_flashticket.py`: điều kiện ném lỗi, cách gộp chuỗi runtime về metric logic.
2. **Tìm ca thật có tình huống này** trong dữ liệu được phép: 13 ca dev bản 2, 9 ca T-062, các ca cũ của T-062/T-063 đã thu, trừ dữ liệu khóa.
   - Đếm số lần adapter ném lỗi hoặc rơi nhánh dự phòng trên mọi ca.
   - Có ca thật: dùng làm ca phân xử.
3. Không có ca thật: dựng **ca thử tổng hợp không nhãn** từ một ca thật, bằng cách đổi nhãn instance hoặc container của chuỗi metric từ giữa cửa sổ. Ghi rõ đây là **kiểm cài đặt**, không phải bằng chứng hiệu quả.
   - Nếu cần ca thật, ghi yêu cầu ô vào `results/T-064/phien-c/YEU-CAU-O.md`: tên ô, cách tạo lại container, thời điểm, service đề xuất không trùng vị trí ô đánh giá T-059. Phiên B (thu bù T-063) đọc file này và tự quyết có thu kèm không.
   - Báo cho phiên tương tác `ed8b9c01…` biết đã ghi yêu cầu.
4. Cài thành phần `src/m1_ft/thanh_phan/h8_adapter.py`, bật/tắt bằng cấu hình, mặc định tắt.
   - Cách gộp phải có nguyên lý, ví dụ nối chuỗi theo thời gian khi các chuỗi không chồng lấn. **Ngưỡng không chỉnh theo đáp án.**
   - Viết test đơn vị.
5. Khi tắt, đầu ra trùng P7. Khi bật, trên ca không có tình huống này, đầu ra phải trùng bản không bật. Kiểm cả hai.

### 2c. H8-log — kênh log nghiệp vụ (`outcome`, `reasonCode`)

1. **Xác định dữ liệu có thật không.**
   - Log nghiệp vụ có trong gói ca không: `results/T-063/thu2/ca/*.tgz` trên laptop; `/opt/flash-ticket-rca/cases/<id>/` trên `exp-obs`, đọc bằng user `rca`.
   - Đếm theo service và theo ca: số dòng có `outcome` / `reasonCode`, các giá trị, phân bố theo thời gian ở nền và sau `t`. Không dùng nhãn để chọn trường.
2. Có dữ liệu: thiết kế kênh, ví dụ tỉ lệ `outcome` thất bại theo service hoặc thao tác, kiểm cùng phép thống kê với các kênh khác của M1.
   - Ghi **nút, cạnh, nơi đặt log và phép tính** (luật 18).
   - Cài `src/m1_ft/thanh_phan/h8_log.py`, bật/tắt bằng cấu hình, có test.
   - Nếu cần đọc file log của ca, thêm vào `bo_sung.py` và `chay_ca.py` theo đúng mẫu `span_phu` (đọc từ gói ca, kiểm trường cấm bằng `hop_dong.vi_pham_truong_cam`, không đọc sổ tiêm lỗi).
3. Không có dữ liệu, hoặc không dùng được: ghi đúng thiếu gì (không thu, không đóng gói, hay không có trường), bằng chứng, và quan sát FlashTicket cần bổ sung (luật 17). **Không gọi là "bỏ".**

### 2d. Chấm và giữ/bỏ cho H8-adapter, H8-log

- **Ghi sổ trước khi chạy.** Thêm dòng vào `results/T-064/so-bien-the.jsonl` (chỉ ghi thêm), mã tiếp theo sau mã lớn nhất hiện có, đọc ngay trước khi ghi.
  - Phép 1: bản thêm riêng vào P7.
  - Phép 2: thêm vào bản đề xuất tạm V032-H5b.
  - Tổ hợp khác chỉ khi có căn cứ ghi trước.
  - Khai rõ: thiết kế sau khi đã xem lượt 1–3.
- Chạy trên `exp-obs` (bắt buộc, WHY-81), hai lần trùng SHA. Áp tiêu chí đã khóa bằng công cụ có sẵn: `cham_dev2.py` cho tập 13 ca, `giu_bo.py` hoặc bản sao có tên mới, không hồi quy 9 ca T-062.
- **Phân tích cơ chế** từng ca đổi so với bản cha (luật 15): đầu vào → bước → trung gian → đầu ra; đối chiếu ca không đổi có điều kiện tương ứng.

### 2e. Dùng `exp-obs` mà không phá đợt thu

Phiên B có thể đang thu bù trên `exp-app`/`exp-obs`. Đợt thu cần `exp-obs` yên. **Trước mỗi lô:**
- `results/T-063/thu3/TRANG-THAI.json` không ghi `dang_thu: true`. Nếu `du_kien_bat_dau_thu` rơi vào trong khoảng lô của bạn dự kiến chạy, hoãn lô.
- Trên `exp-obs` không có `runner3`: `ps -eo cmd | grep -c "[p]ython3 -B runner3"` phải bằng 0.
- Không có lô khác đang chạy: `ps -eo cmd | grep -c "[c]hay_ca.py"` bằng 0, và `DIEU-PHOI-TRANG-THAI.json` không có `lenh_nen` lô `exp-obs` đang chạy.

Khi chạy lô, ghi `results/T-064/phien-c/TRANG-THAI.json` (`lo_exp_obs: dang_chay`, `du_kien_ket_thuc`). Xong thì đặt `xong`.

Đóng gói mã nguồn lên `exp-obs` theo mẫu `goc-<n>`: tên mới tiếp sau số lớn nhất đang có, ghi `goi-tai-len-<n>.sha256`, ghi `results/T-064/thay-doi-may.md` (thêm dòng). Trong lúc chờ máy, viết mã, test trên laptop, chuẩn bị chấm.

## 3. Kiểm đúng đắn (SPEC T-064 "Kiểm đúng đắn", AGENTS 5.4)

- Hai lần chạy trùng SHA.
- Đếm đầu vào thật của thành phần mới: số chuỗi gộp, số dòng log, số kênh. Đếm lần rơi nhánh dự phòng. Soi trung gian.
- Trạng thái đồng loạt (100% không đổi) phải lần tới đầu vào trước khi diễn giải.
- **Tắt mọi thay đổi mới thì trùng P7.**
- Không đưa nhãn, tên ô hay mốc tiêm (ngoài `t`) vào phương pháp.
- Kết quả quá đẹp: chạy phép thử giả, ví dụ dời mốc ngẫu nhiên lớn, hoặc xáo trường log.

## 4. Phạm vi ghi

**Được ghi:**
- `src/m1_ft/`: thành phần mới, `chay_ca.py` (tham số `--doi-t`), `bo_sung.py` nếu cần, `tests/`;
- `results/T-064/phien-c/` (mới): kế hoạch, nhật ký phiên, script, đầu ra laptop, kiểm, phân tích, trạng thái;
- `results/T-064/bien-the/<mã mới>/`, `results/T-064/cham/<file mới>`;
- chỉ thêm dòng: `results/T-064/so-bien-the.jsonl`, `results/T-064/thay-doi-may.md`;
- `exp-obs`: `/opt/rca-m1ft/goc-<n>` mới, `/opt/rca-m1ft/out/<thư mục mới>`, script lô trong `~`.

**Không ghi:**
- `src/m1/`, `src/p3/`;
- `results/T-064/ho-so-chon.md`, `tieu-chi-chon.md`, `ban-xuat/`: điều phối giữ;
- `tasks/T-064-m1-flashticket/LOG.md`: điều phối giữ, nên tránh hai phiên cùng ghi. Ghi nhật ký vào `results/T-064/phien-c/NHAT-KY.md` (mỗi bước một dòng có giờ UTC); điều phối chép vào LOG khi tích hợp;
- `docs/`: viết đề xuất WHY cho mọi lựa chọn quan trọng (cách gộp chuỗi, kênh log, xử lý gói bổ sung khi dời `t`) vào `results/T-064/phien-c/de-xuat-WHY.md`. Điều phối chép vào `docs/WHY.md` **trước khi** kết quả được dùng trong hồ sơ chọn. Kết quả chấm của bạn vẫn ghi đầy đủ; trong bàn giao, đánh dấu chúng "chờ WHY";
- `results/T-063/`, `results/T-065/`.

**Không sửa mã đang dùng cho lô lượt 4** (`goc-9` trên máy). Mã mới đi vào `goc-<n>` mới. Nếu sửa file `src/m1_ft` dùng chung (`chay.py`, `chay_ca.py`), giữ hành vi mặc định trùng byte và ghi phép kiểm.

## 5. Bảo toàn chất lượng khi hết hạn mức

- Sau mỗi bước con: cập nhật `results/T-064/phien-c/CHECKPOINT.md` (giờ UTC, bước, đầu ra, lệnh hoặc lô đang chạy, bước tiếp) và `TRANG-THAI.json`.
- Lô trên `exp-obs` chạy độc lập với phiên. Script lô bỏ qua cặp đã có `summary.json`, để chạy lại chỉ bù phần thiếu.
- **Không hạ chuẩn kiểm khi hạn mức thấp.** Kiểm `mcp__ccd_session_mgmt__get_usage` trước bước dài.
  - Nếu hạn mức 5 giờ trên 90%: chỉ làm bước con checkpoint được trọn.
  - Chưa ghi sổ thì không phát lô. Không chấm nửa chừng rồi ghi kết luận.
- Checkpoint phải đủ để một agent khác làm tiếp không cần lịch sử chat. Phiên điều phối có thể gửi tin cho phiên này làm tiếp, hoặc tự làm theo checkpoint nếu phiên này không còn.

## 6. Bàn giao

- `results/T-064/phien-c/BAN-GIAO-C.md`:
  - mã đã đổi và hash;
  - các dòng sổ đã ghi;
  - bảng chấm;
  - kết luận giữ/bỏ hoặc "không tác dụng" hoặc "chưa thử được", kèm bằng chứng;
  - cơ chế từng ca đổi;
  - kết quả dời mốc theo ô;
  - đề xuất WHY;
  - phần chờ dữ liệu của phiên B;
  - việc cần Minh quyết;
  - lệnh cuối.
- **Tóm tắt cuối lượt** theo AGENTS mục 7, bốn mục: tách task đạt gì, câu hỏi nguồn trả lời tới đâu, thiếu bằng chứng gì.

## 7. Giới hạn cứng

- Không sửa `src/m1`, `src/p3`; không đổi tiêu chí đã khóa; không dùng ô đánh giá; không đọc `data/locked/`.
- Không chạy lặp để chọn. Không chỉnh ngưỡng theo đáp án.
- Không commit hay push.
- Không in khóa hay mật khẩu.
- Có `D:/RCA-overnight/STOP` thì dừng ở ranh giới.
- Giữ mọi lượt chạy, kể cả hỏng.
