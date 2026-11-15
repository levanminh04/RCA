# Brief phiên B — T-063 thu bù ô lỗi cho H3 (POOL-EVENT) và H4 (consumer chậm)

Ghi ngày 14/11/2026 ~04:40Z. Phiên tương tác `ed8b9c01…` mở phiên này theo duyệt của Minh: "duyệt mở phiên B C, lên plan kĩ lưỡng, prompt ghi chuẩn, không viết sơ sài".

Bạn là **Claude**, vai trò **người làm T-063** cho phần thu bù này. Người phản biện T-063 là Codex; phiên điều phối sẽ phát lượt phản biện sau khi bạn bàn giao.

## 0. Bối cảnh bắt buộc đọc trước

1. `AGENTS.md`, đặc biệt Luật 0, luật cứng 1–21, mục 5, 7, 9.
2. **Quyền:** `docs/DECISIONS.md`, đọc các mục:
   - "Bổ sung quyền điều phối chiến dịch nhiều ngày" (13/11): Claude tự quyết thu bổ sung/thu lại cho H1–H8;
   - "Chạy bộ điều phối đợt thu trên `exp-obs`";
   - "Hook thử H3, folder Grafana, Codex kiểm giao diện qua Codex app" (14/11): **Minh duyệt sửa hook thử `RcaFaults.java` cho ô POOL-EVENT**.
3. Hồ sơ chiến dịch `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`: mục 4 (bảng hướng, dữ liệu cần), mục 6 (quyền máy và repo).
4. `tasks/T-063-quan-sat-thu-dev-2/SPEC.md` toàn bộ, gồm phần bổ sung; mục cuối của `tasks/T-063-quan-sat-thu-dev-2/LOG.md`.
5. Hồ sơ T-063 trong `results/T-063/`:
   - `bao-cao.md` mục 2 và mục 7 (H3, H4 thiếu ô lỗi; đề xuất);
   - `o-dev-bo-sung.md` (định nghĩa ô dev, gồm POOL-EVENT và CONSUMER-BOOK-SLOW);
   - `chay/D2B-KET-QUA.md` (POOL-EVENT không thử được vì `poll()`; CONSUMER-BOOK-SLOW thất bại 3 lần ở ~0,5 msg/s);
   - `chay/THIET-KE-BO-CHAY-2.md`, `chay/HO-SO-LUOT.md`, `chay/dieu-kien-xac-nhan.md`, `chay/runner3.py`, `chay/xac_nhan_ca.py`;
   - `dong-bang.md` (bản 2), `dong-bang/dong_bang.py`, `tiem-loi/inj2.py`.
6. `results/T-062/tai-2/BAN-GIAO-4-linux.md` (tải `tai_linux.py` chạy từ `exp-obs`) và `results/T-062/ha-tang/thay-doi.md` (cách build và triển khai image trên `exp-app`).
7. `docs/LESSONS.md` khi thiết kế ô và điều kiện xác nhận.

**Không đọc** `data/locked/`, `.env`, `grafana.env`, `~/.ssh`, lịch sử shell. Không đọc repo RCA cũ.

## 1. Mục tiêu và vì sao

T-064 cần ô lỗi để phân xử H3 (kênh pool) và H4 (kênh queue). Hiện H3 và H4 có tín hiệu trong gói nhưng **không có ô lỗi tương ứng**, nên hồ sơ chọn chỉ ghi được "chưa thử được trên ô lỗi". Tiêu chí kết thúc M3 (a) đòi mỗi hướng có ít nhất một bản đã cài, kiểm không nhãn và chấm. "Không thử được" chỉ dùng sau khi đã tự sửa trong quyền.

**Đầu ra cần:** các ca mới thu đúng giao thức T-063, được đầu dò xác nhận theo điều kiện **khai trước khi xem dữ liệu**, đóng gói đủ để T-064 chạy M1-FT.

## 2. Việc cụ thể

### 2a. Rà và lập kế hoạch (ghi file trước khi chạm máy)

Tạo `results/T-063/thu3/KE-HOACH.md`, gồm:
- **Ô sẽ thu**, mỗi ô ghi: hướng phân xử, cách tiêm, cường độ và lý do, đầu dò độc lập, điều kiện xác nhận, tập chấp nhận (service hoặc cạnh), vị trí so với 12 ô đánh giá T-059 (phải khác vị trí).
- **Ô bắt buộc:**
  - **POOL-EVENT.**
  - **Ô H4** (consumer chậm): xem 2c.
  - **Ô đối chứng bản build mới:** ít nhất một BINH-THUONG, và một ô cũ đã đạt ở đợt thu 2 (ví dụ EVENT-DB-LAT) để so cùng điều kiện. Lý do: build lại image Event tạo **bản triển khai khác bản đóng băng 2**, nên ca mới không gộp thẳng vào 13 ca cũ (`bao-cao.md` mục 7).
- **Ô tùy chọn cho H8-adapter:** container bị tạo lại trong cửa sổ, vì adapter ghim ném `Multiple runtime series map to one logical metric` (`tasks/T-064-m1-flashticket/LOG.md` dòng 26).
  - Phiên C (mã T-064) có thể cần ô này. Đọc `results/T-064/phien-c/YEU-CAU-O.md` nếu file đã có.
  - Chỉ thu nếu: vị trí không trùng ô đánh giá, cách tiêm và xác nhận rõ, và không làm chậm hai ô bắt buộc.
  - Ghi lý do thu hay không.
- **Thứ tự, thời lượng mỗi chu kỳ** (giữ 30 phút như đợt 2 trừ khi có lý do ghi rõ), **tổng thời gian dự kiến**.
- **Hồ sơ luật 21:** gặp lỗi ở 10%, 50%, 99% thì xử lý thế nào, chạy lại gì, mất bao lâu.

### 2b. POOL-EVENT (H3) — đã có quyền sửa hook

1. **Repo FlashTicket** `D:/Project/flash-ticket-platform`, chỉ nhánh `rca/quan-sat-log`.
   - Trong `services/event-service/src/rca-test/java/com/flashticket/event_service/testing/RcaFaults.java`, các dòng 69 và 163 đang so `"event_service".equals("booking_service")`. Hệ quả: `poll()` và `pool.hold` không bao giờ chạy ở Event.
   - Sửa **đúng điều kiện cho phép `pool.hold` chạy ở Event**. Không đổi hành vi khác: điều kiện `subject` ở dòng 129 chỉ dành cho Booking, giữ nguyên.
   - Trước khi sửa, đối chiếu với `RcaFaults.java` của Booking: cùng cơ chế và cùng audit (`pool.hold.started` …).
   - **Không sửa code nghiệp vụ.** Chỉ sửa trong `src/rca-test`.
2. **Xác định nguồn build đang chạy.** `dong-bang.md` ghi image `ft-local/<svc>:arm64-t062-6b21ed55`, còn HEAD cục bộ `fba6bc8` "không dùng để build lại".
   - Tìm commit `6b21ed55` và cách build đã dùng (`results/T-062/ha-tang/thay-doi.md`).
   - Sửa trên đúng nền đó, chỉ cho Event. Image các service khác giữ nguyên.
   - Commit lên nhánh `rca/quan-sat-log`. Được push nhánh đó. **Không merge `main`, không chạy `cd.yml`, không chạm máy 84** (52.64.237.84).
3. **Build và triển khai lại riêng `event-service` trên `exp-app`.**
   - Ghi vào `results/T-063/thu3/thay-doi-may.md`: lệnh, giờ UTC, image ID trước/sau, cách hoàn tác.
   - Kiểm luồng lõi: tải mua vé chạy được; audit của hook ghi `pool.hold.started` khi tiêm thử.
4. **Chọn cường độ.** Pool Hikari của Event có max = 5 (`o-dev-bo-sung.md`). Ứng viên: `pool.hold` = 4 (bão hòa một phần) hoặc 5 (cạn hẳn).
   - Chọn bằng một lần **chạy thử ngắn không thu**.
   - Ghi số đo `db_client_connections_usage{state=used}`, `pending_requests` và ảnh hưởng lên hành trình.
   - Lý do chọn ghi vào `KE-HOACH.md` và đề xuất mục WHY (xem mục 5).
5. **Đóng băng bản 3.** Chạy `dong-bang/dong_bang.py` với tên ra mới (`dong-bang-3.json`); thêm mục "Bản 3" ở cuối `dong-bang.md`: thay đổi duy nhất là image Event, lý do, hash.

### 2c. Ô H4 — consumer chậm

**Ba cách đã thất bại:** toxic latency 200 ms, bandwidth 2 KB/s và 1 KB/s. Nguyên nhân nghi: lưu lượng message ~0,5 msg/s quá thấp; chưa kiểm.

Thử theo thứ tự, tối đa 3 lần thử mới cho mỗi hướng (AGENTS §5a):
1. **Tăng lưu lượng message bằng tải** (trong quyền chiến dịch, máy tải AWS và kịch bản k6).
   - Đo trước lưu lượng message ở vài bậc tải trên bản hiện hành.
   - Tìm bậc cho tồn queue khi có toxic, mà tải nền vẫn bình thường.
   - Có thể giao Codex sửa hoặc thêm kịch bản k6: Codex là người làm phần tải (T-062 phụ lục 2). Gọi bằng `results/T-063/dieu-phoi/goi_codex.py` (`--che-do sandbox`), brief ghi ra file trong `results/T-062/codex/`, nhật ký theo mẫu cũ.
   - Tải mới khác tải của 13 ca cũ, nên ô đối chứng (BINH-THUONG) phải chạy **cùng bậc tải đó**.
2. **Làm chậm khâu xử lý của consumer bằng hook thử** trong `src/rca-test` của Booking.
   - **Chưa có quyền.** Minh mới duyệt hook H3.
   - Chỉ làm nếu `docs/DECISIONS.md` đã có mục Minh duyệt hook H4.
   - Nếu chưa có quyền và cách 1 không đạt: dừng ô H4, ghi đề xuất cụ thể (file, dòng, hành vi, rủi ro) vào bàn giao để Minh quyết. Không tự sửa.
3. **Nếu cả hai không làm được:** ghi đủ phần đã thử, số đo và bằng chứng còn thiếu, để T-064 ghi H4 là "chưa thử được trên ô lỗi" có căn cứ.

### 2d. Điều kiện xác nhận — khai TRƯỚC khi thu

- Tạo `results/T-063/thu3/dieu-kien-xac-nhan-3.md` **trước khi phát đợt thu chính**, theo đúng khuôn `chay/dieu-kien-xac-nhan.md`: cửa sổ N/L/sau; điều kiện chung C0, C1; điều kiện riêng từng ô.
- Ghi giờ UTC và câu "chưa xem dữ liệu của lượt chính".
- Nguồn đầu dò phải **độc lập với M1**.
- Bài học từ lần trước: điều kiện PAUSE ghi sai chuỗi trạng thái. Với mỗi chuỗi so khớp, **đối chiếu với đầu ra thật của đầu dò trong lượt chạy thử** trước khi khai.
- Không dùng điểm M1. Không đưa nhãn vào phương pháp.

### 2e. Thu

- Lịch mới `results/T-063/thu3/lich-3.json`, băm trước khi phát. Dùng `runner3.py` trên `exp-obs`, chạy độc lập với laptop:
  - `setsid -f nohup … < /dev/null`;
  - `RCA_DP_OUT` trỏ thư mục ra mới;
  - sổ tiêm lỗi nối hash, mã ca mờ;
  - M1 P7 qua stage/run ghim;
  - xuất bổ sung ±300 s.
  - Không sửa `runner3.py` đang dùng. Cần khác thì tạo bản mới qua `tao_runner3.py` hoặc bản sao có tên mới, ghi diff và lý do.
- **Chạy thử một chu kỳ ngắn trước** trên máy chủ, như đợt 2.
- **Nhường `exp-obs`:** đợt thu cần `exp-obs` yên. Trước khi phát mỗi lượt thu, kiểm cả ba điều sau:
  - không có tiến trình `chay_ca.py` trên `exp-obs`: `ps -eo cmd | grep -c "[c]hay_ca.py"` phải bằng 0;
  - `tasks/T-062-dem-chang-1-4/DIEU-PHOI-TRANG-THAI.json` không còn mục `lenh_nen` loại lô `exp-obs` đang chạy;
  - `results/T-064/phien-c/TRANG-THAI.json`, nếu có, không ghi `lo_exp_obs: dang_chay`.

  Đang có lô thì làm phần chuẩn bị (hook, build, chạy thử trên `exp-app`) trong lúc chờ.
- **Báo cho các phiên khác:** ghi `results/T-063/thu3/TRANG-THAI.json` gồm `dang_thu` (true/false), `du_kien_bat_dau_thu`, `du_kien_ket_thuc`, `buoc`, `cap_nhat`. Ghi `du_kien_bat_dau_thu` sớm nhất có thể để phiên khác không phát lô trùng giờ.
- **Codex L5** (kiểm Grafana qua Chrome) đang chạy song song và tự giảm trang nặng khi thấy `runner3`. Không cần chờ nó.
- **Đọc trạng thái trong lúc thu chỉ bằng lệnh nhẹ.** Không truy vấn Prometheus nặng.

### 2f. Sau thu

1. Nhận về `results/T-063/thu3/` theo mẫu `chay/nhan_thu2.sh`; băm, kiểm `SHA256SUMS`, chuỗi hash của sổ.
2. Hậu kiểm từng mã mờ bằng `xac_nhan_ca.py` (hoặc bản mở rộng có tên mới) theo `dieu-kien-xac-nhan-3.md`, ra `thu3/xac-nhan-ca-3.json`.
   - Ca không đạt: không vào tập chọn, ghi lý do.
   - Sai do lỗi chép điều kiện: khai "Sửa sau" riêng, giữ cả hai kết quả, chờ Minh. Không tự nhận.
3. Đưa gói ca lên vị trí T-064 dùng trên `exp-obs` (`/opt/flash-ticket-rca/cases`, `outputs`, `/opt/rca-m1ft/bo-sung/<id>/`) đúng như 13 ca cũ. Kiểm `method-input.json` có đủ cho M1 P7 chạy, và P7 chạy OK hai lần cùng SHA.
4. Cập nhật:
   - `o-dev-bo-sung.md`: thêm mục ghi ngày, không sửa dòng cũ;
   - `bao-cao.md`: thêm mục "Thu bù 3", không viết đè kết luận cũ;
   - `manifest.json` của T-063 nếu tạo được trong phạm vi.

## 3. Kiểm đúng đắn (tự kiểm, AGENTS mục 5.4)

- Soi trung gian: số đo đầu dò từng ca ở N/L/sau, lưu lượng message, trạng thái pool.
- Ca BINH-THUONG trên bản mới **phải sạch** theo điều kiện đã khai. Nếu không sạch, ghi đó là điều kiện nền khác bản 2, không giấu.
- Ô cũ lặp lại trên bản mới: so đầu dò với ca cũ cùng ô. Lệch thì ghi.
- Tải: `ExitCode = 0`, `dropped_iterations`, `journey_failed`.
- Không mở dữ liệu khóa; không dùng ô đánh giá T-059.

## 4. Phạm vi ghi

**Repo RCA, được ghi:**
- `results/T-063/thu3/` (mới), cùng các file mới khác trong `results/T-063/`;
- thêm mục, không sửa dòng cũ, cho `results/T-063/o-dev-bo-sung.md`, `bao-cao.md`, `dong-bang.md`;
- `tasks/T-063-quan-sat-thu-dev-2/LOG.md`: chỉ ghi thêm, mở đầu bằng dòng "Phiên B (Claude, `local_…`) mở ngày …"; phiên điều phối không ghi LOG T-063 khi phiên B còn hoạt động;
- `results/T-062/codex/` cho brief và nhật ký Codex phần tải, và `results/T-062/tai-2/` nếu Codex sửa tải.

**Repo FlashTicket:** nhánh `rca/quan-sat-log`, chỉ `services/event-service/src/rca-test/**` (H3), `deploy/rca-test/`, cấu hình tải. Commit và push được phép cho nhánh này.

**Máy:**
- `exp-app`: build và triển khai lại `event-service`; bộ tiêm lỗi; toxiproxy.
- `exp-obs`: `~/rca-dieu-phoi` (bộ chạy, lịch mới, thư mục ra mới), vị trí gói ca cho T-064.
- Máy tải: kịch bản k6 qua `tai_linux.py`.

**Không ghi:**
- `docs/` (STATE, WHY, DECISIONS, LESSONS): phiên điều phối ghi. Viết **đề xuất mục WHY** (chọn cường độ, cách tạo ô H4, build mới) vào `results/T-063/thu3/de-xuat-WHY.md`; điều phối chép vào `docs/WHY.md` trước khi T-064 dùng kết quả.
- `src/`, `results/T-064/`, `results/T-065/`.

## 5. Bảo toàn chất lượng khi hết hạn mức

- **Sau mỗi bước con**, ghi `results/T-063/thu3/CHECKPOINT.md`: giờ UTC, bước, đầu ra, lệnh hoặc tiến trình đang chạy, bước tiếp. Cập nhật `TRANG-THAI.json`.
- **Đợt thu chạy trên `exp-obs`, không phụ thuộc phiên Claude.** Hết hạn mức giữa đợt thì đợt vẫn chạy. Phiên tiếp nhận nhận về theo checkpoint.
- **Không hạ chuẩn kiểm khi hạn mức thấp.** Kiểm `mcp__ccd_session_mgmt__get_usage` trước mỗi bước dài.
  - Nếu hạn mức 5 giờ trên 90%: chỉ làm bước con nào checkpoint được trọn vẹn.
  - Không bắt đầu bước sửa máy (build, triển khai) nếu không chắc làm xong và ghi được hoàn tác.
- Thao tác máy phải làm lại được: kiểm trạng thái trước khi làm, không ghi đè đầu ra cũ.
- Nếu phiên này dừng giữa chừng, phiên điều phối (lịch 15 phút) đọc `thu3/CHECKPOINT.md`, `TRANG-THAI.json` và gửi tin cho phiên này làm tiếp. Vì vậy checkpoint phải đủ để **một agent khác làm tiếp mà không cần lịch sử chat**.

## 6. Bàn giao

- `results/T-063/thu3/BAN-GIAO-B.md`:
  - ô đã thu và đã xác nhận (mã mờ ↔ ô chỉ ghi ở phía chấm, theo quy ước cũ);
  - ô không đạt và lý do;
  - bản đóng băng 3;
  - vị trí gói trên `exp-obs` cho T-064;
  - đáp án cho từng ô mới (service hoặc cạnh gốc), để điều phối ghép vào `dap-an` phía chấm; **không đặt đáp án ở chỗ M1 đọc được**;
  - đề xuất WHY;
  - việc cần Minh quyết;
  - lệnh cuối đã chạy.
- **Mục kết thúc phiên trong LOG T-063** theo AGENTS mục 7, gồm prompt cho Codex phản biện phần thu bù. Prompt chép nguyên văn "Prompt chung" và khối công đoạn phù hợp của `docs/review-prompt.md`, chỉ điền thông tin trung tính.
- **Tóm tắt cuối lượt** theo AGENTS mục 7, bốn mục.
- Gỡ khóa SSH trên `exp-obs` (`~/rca-dieu-phoi/keys`) **chỉ khi** điều phối xác nhận không còn thu bù. Không tự gỡ.

## 7. Giới hạn cứng

- Không merge hoặc push `main`; không chạy `cd.yml`; không chạm máy 84.
- Không sửa code nghiệp vụ.
- Không in, không ghi mật khẩu, token hay khóa vào file, log hay prompt.
- Không đọc `data/locked/`.
- Không đổi tiêu chí chọn T-064.
- Có `D:/RCA-overnight/STOP` hoặc `~/rca-dieu-phoi/STOP` thì dừng ở ranh giới.
- Ghi mọi thay đổi máy kèm lệnh, giờ UTC, hash trước/sau và cách hoàn tác.
- Giữ mọi lượt chạy, kể cả lượt hỏng.
- Câu hỏi cho Minh: gom vào bàn giao. Chỉ dừng hẳn khi việc còn lại đều phụ thuộc câu trả lời.
