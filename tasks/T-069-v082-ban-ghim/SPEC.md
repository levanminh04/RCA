# T-069 — V082 không hồi quy trên bản FlashTicket ghim (W3)

- **Trạng thái:** đã duyệt (19/11/2026, bản 2)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P9, P10 — **Cổng:** chuẩn bị G6

Lịch sử soạn: bản 1 và bản 2 trình trong chat 19/11/2026. Bản 2 sửa theo câu hỏi của Minh (dừng không phải chạy lại; dừng phải kèm phân tích nguyên nhân; chạy trên server, laptop mất mạng không ảnh hưởng; thời lượng theo số đo thực tế). Quyết định của Minh ghi ở `LOG.md` phiên 1. Phiên 2 (19/11) làm rõ định nghĩa "hạng" và tập so của D1–D5 theo quyền Minh cho ở phiên 1 (nhóm "tiêu chí tụt rõ ràng theo hạng từng ô"); đoạn cũ → mới ghi ở LOG phiên 2.

## Mục tiêu

Kế hoạch [giai đoạn 2 §8.2](../../docs/techstack/KE-HOACH-GIAI-DOAN-2.md) gói W3: "V082 không hồi quy trên bản mới". Câu hỏi: **khi hệ thống FlashTicket đổi từ bản 3 sang bản ghim `rca/exp-2026-11` (T-067), V082 có còn xếp đúng service gốc như trên tập dev không?**

Code M1 và cấu hình V082 không đổi (T-066, T-067 chứng minh trùng byte). Thứ đổi là tín hiệu đầu vào: code Event, Booking, Payment, ảnh gốc JRE, đường lỗi Payment → Booking ([`results/T-067/thay-doi-main.md`](../../results/T-067/thay-doi-main.md)).

Đây là task **kiểm không hồi quy trên các ô dev**, không phải đánh giá giữ ngoài. V082 được chọn trên chính các ô này nên điểm phía cũ lạc quan ([`results/T-064/ho-so-chon.md`](../../results/T-064/ho-so-chon.md) §15). Mỗi ô một lần thu ở cả hai phía, nên task kết luận "có / không tụt quá ngưỡng khai trước" và cơ chế của ô tụt; không ước lượng độ chính xác. Kết quả quyết định có chuyển sang W4/W5 (demo dùng V082 trên bản ghim) hay không.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác cần loại | Phép kiểm và bằng chứng | Phần còn mở |
|---|---|---|---|
| V082 có tụt trên bản ghim không? | (a) hệ thống đổi làm mọi phương pháp khó hơn; (b) thành phần riêng của V082 (H5b, H8s1, H8a) không hợp bản mới; (c) nhiễu một lần thu | Chạy cả P7 và V082 trên cùng ca mới (runner làm sẵn). Cùng tụt → nghiêng (a); chỉ V082 tụt → nghiêng (b). Ô đổi hạng thu lặp một lần (lượt riêng) để tách (c). Ô tụt phân tích nguyên nhân theo bước 7 trên dữ liệu đã lưu | Một lần thu mỗi ô không đo được phương sai |
| Ô nào ghép được với phía cũ? | Bộ tiêm hoặc hook không tác động đúng trên bản mới | Sổ tiêm có `fault-start` thành công; đầu dò t+60, t+330 xác nhận tác động như ca cũ cùng ô | Ô không xác nhận được ghi "không ghép được", không tính điểm |

## Đầu vào

**Phía cũ (dùng lại, không chạy lại):**

- Tập chọn dev bản 3 `results/T-064/tap-chon-dev3-17.json`: 17 ca (11 lỗi, 6 không lỗi). 13 ca thu2 chạy image `arm64-t062-6b21ed55` cả 7 service (`results/T-063/dong-bang/dong-bang-2.json`); 4 ca thu bù 3 chạy Event `arm64-t063h3-76b34d5e` (`dong-bang-3.json`).
- Đầu ra d = 0: P7 lô 5 `results/T-064/kiem/nhan-luot5/`; V082 sau R9 `results/T-064/kiem/nhan-r9/r9/dev3/d0/`. Kiểm hash theo `results/T-064/manifest-3.json` trước khi dùng; lệch thì dừng phần phụ thuộc, báo Minh.
- Điểm cũ (`results/T-064/cham/chon-dev3-d0-v082-r9-A.json`): V082 AC@1 9/11, AC@3 11/11, tổng hạng cắt 13, K 4/6; P7 7/9/23, K 5/6. Hạng V082 theo ô: hạng 1 ở EVENT-DB-LAT, CPU-BOOK-1, HTTP5-EVENT, REDIS-BOOK, NET-GW-BOOK, PAUSE-PAYMENT, POOL-EVENT, CONSUMER-BOOK-SLOW-X3, RECREATE-PAY; hạng 2 ở CPU-BOOK-2, HTTP5-EVENT-FLASH (`ho-so-chon.md` §15; người làm kiểm lại trên file chấm ở bước 3).
- Đáp án `results/T-064/dap-an-dev3.json` và bộ chấm T-064: chỉ phía chấm dùng; phương pháp không đọc.

**Phía mới:** bản ghim `36a3725` đang chạy trên exp-app (T-067, `results/T-067/trien-khai/chuoi-container.json`). Repo lab: `campaigns/runner/runner4.py` (tuyến một ca đã chạy trọn ở T-066 `e2e-001`), `faults/injectors/docker/inj3.py`, lịch `campaigns/schedules/lich-2.json`, `lich-3.json`.

## Lỗi tiêm (theo `inj3.py`; mỗi lỗi 10 phút giữa lượt tải 30 phút, tiêm ở phút 10)

| Ô | Lỗi | Gốc theo đáp án |
|---|---|---|
| EVENT-DB-LAT | Toxiproxy trễ 30 ms Event → PostgreSQL | Event / event_db |
| REDIS-BOOK | Trễ 200 ms Booking → Redis | Booking / Redis |
| NET-GW-BOOK | Trễ 300 ms gateway → Booking | gateway → Booking |
| CONSUMER-BOOK-SLOW-X3 | Bóp băng thông Booking ↔ RabbitMQ; tải ×3 | Booking |
| HTTP5-EVENT | Hook Event trả 5xx cho sự kiện đang bán | Event |
| HTTP5-EVENT-FLASH | Như trên, tải flash | Event |
| POOL-EVENT | Hook giữ 5 kết nối pool DB của Event | Event |
| CPU-BOOK-1, CPU-BOOK-2 | Ép CPU Booking 1 và 2 tiến trình | Booking |
| PAUSE-PAYMENT | `docker pause` Payment | Payment |
| RECREATE-PAY | Tạo lại container Payment một lần | Payment |
| BINH-THUONG ×4, FLASH-HEALTHY, BINH-THUONG-X3 | Không tiêm (đo báo nhầm K) | — |

Hệ số tải và cường độ tiêm giữ đúng `lich-2.json` (13 ô thu2) và `lich-3.json` (4 ô thu bù 3). Mốc `t` lấy từ sổ tiêm (chế độ (a)), như tập dev cũ.

## Tiêu chí khai trước

Ghi `results/T-069/tieu-chi.json`, commit (repo RCA chỉ khi Minh duyệt; trước đó lưu hash trong LOG) **trước khi thu**: danh sách cặp ca cũ–mới (ô, image, tải, can thiệp, cửa sổ), các ngưỡng dưới đây, quy tắc lặp.

- Một ô lỗi **tụt** khi hạng đáp án của V082 mới > hạng cũ + 1 (cho lệch 1 bậc vì dời mốc 15 s ở T-064 §16 đã đổi AC@1 một ca). "Hạng" là `hang_cat` của `src/m1_ft/cham.py::cham_ca_loi` (bộ chấm T-064, không sửa): hạng kỳ vọng của nút đáp án trong nhóm đồng hạng, cắt ở 6; vắng, lỗi chạy hoặc thiếu đầu ra = 6. So hạng từng ô, không so byte đầu ra. Ca cũ và ca mới ghép theo ô; bốn ô BINH-THUONG ghép theo thứ tự trong lịch. *(Làm rõ ở phiên 2, LOG phiên 2.)*
- **Điều kiện dừng kết luận** (trên các ô ghép được):

| # | Điều kiện | Với số cũ |
|---|---|---|
| D1 | AC@3 của V082 giảm | < 11/11 |
| D2 | AC@1 của V082 giảm ≥ 2 ca | ≤ 7/11 |
| D3 | V082 mới kém P7 mới ở AC@1, AC@3 hoặc tổng hạng | mất lợi thế dùng để chọn V082 |
| D4 | V082 lỗi chạy không do hạ tầng | — |
| D5 | K của V082 tăng ≥ 2 | ≥ 6/6 |

Ô không ghép được bỏ ở cả hai phía; số cũ của D1, D2, D3, D5 tính lại trên đúng tập ô ghép được. *(Làm rõ ở phiên 2, LOG phiên 2.)*

- **"Dừng" nghĩa là dừng kết luận và không chuyển sang W4/W5; không ngắt lượt thu.** Cả 17 ca vẫn thu hết. Khi có điều kiện dừng, làm bước 7 (phân tích nguyên nhân) trên dữ liệu đã lưu rồi mới trình Minh; không thu lại.
- **Lặp tách nhiễu:** ô có hạng V082 hoặc P7 đổi so với phía cũ thu lặp một lần, tối đa 4 ô, trong **lượt ngắn riêng** sau khi chấm. Báo cả hai lần thu, không chọn lần đẹp hơn.

## Đầu ra

- `results/T-069/tieu-chi.json` (khai trước).
- `results/T-069/bang-theo-o.md` và `.json`: mỗi dòng một ô — hạng cũ/mới của V082 và P7, verdict, `trung_sha`, ghép được không, nhóm giải thích (a)/(b)/(c), kết quả D1–D5. Không gộp thành một số trung bình.
- `results/T-069/phan-tich-nguyen-nhan.md` (khi có ô tụt hoặc điều kiện dừng): theo bước 7.
- `results/T-069/thay-doi-may.md`, `results/T-069/bao-ve-truoc.sha256`, `bao-ve-sau.sha256`, `SHA256SUMS`.

## Phạm vi ghi

Ngoài `LOG.md` của task này và dòng T-069 trong `docs/STATE.md`:

- Repo lab: `faults/injectors/docker/inj3.py` (chỉ sửa RECREATE-PAY), `campaigns/schedules/lich-t069*.json`. Commit và push theo luật cứng 11 (Minh cho phép trong lời duyệt task).
- `results/T-069/`.
- exp-app: cập nhật `/opt/rca-lab` bằng `git fetch` + `git checkout <commit>` (ghi hash file lab trước/sau); trạng thái tiêm lỗi (toxic Toxiproxy, lease hook, `rca-faults`, thư mục trạng thái của `inj3.py`); container Payment tạo lại ở ô RECREATE-PAY.
- exp-obs: `/srv/rca-lab/runs/t069-*`; ca mới trong `/srv/rca-lab/m1/{cases,outputs,v082,bo-sung}/`; sổ tiêm qua user `ledger`; chỉ mục G1 trong `/srv/rca-lab/rca-results`; `/srv/rca-lab/load-controller`; `/srv/rca-lab/m1/t069-phan-tich/` (chạy offline ở bước 7).
- Máy tải: `/srv/rca-lab/load-runs/t069-*`.

**Không sửa:** code M1, cấu hình V082, bản chụp `goc-12`, bộ chấm và đáp án T-064, đầu ra cũ, file của T-067, `tests/signals/tieu-chi.json`.

## Các bước

1. **Toàn vẹn trước:** băm danh sách bảo vệ (`results/T-066/bao-ve.tsv` + file lab như T-067 + đầu ra cũ T-064 dùng làm phía cũ + file đã có trong `/srv/rca-lab/m1`, `m1-snapshots`) → `results/T-069/bao-ve-truoc.sha256`. Ca mới sinh ra trong `/srv/rca-lab/m1` không nằm trong phép so.
2. **Sửa `inj3.py`:** RECREATE-PAY đọc thư mục compose từ biến môi trường `RCA_APP_COMPOSE_DIR` (đặt `/opt/flash-ticket-build/t067-compose/hieu-luc`); mặc định giữ hành vi cũ; với cấu hình hiệu lực không cần biến `IMAGE`. Viết `campaigns/schedules/lich-t069-thu.json` (3 ca) và `lich-t069.json` (14 ca còn lại); commit, push; cập nhật `/opt/rca-lab` trên exp-app và exp-obs.
3. **Khai tiêu chí:** `results/T-069/tieu-chi.json`; kiểm hash phía cũ theo `manifest-3.json`; kiểm lại hạng cũ từng ô trên file chấm.
4. **Thu thử 3 ca** (~1 giờ 34 phút): RECREATE-PAY, HTTP5-EVENT, POOL-EVENT. Khởi động `runner4.py` bằng `setsid nohup` trên exp-obs như lượt chính, rồi đóng mọi SSH từ laptop và xác nhận lượt vẫn chạy. Kiểm: tiêm có tác động, P7 và V082 chạy, `trung_sha` đúng, Payment sau khi tạo lại đúng image và cấu hình T-067 (`SERVICE_VERSION`, compose `t067-compose/hieu-luc`). Ca thử tính là ca chính thức nếu sau đó không sửa code.
5. **Thu chính 14 ca** (~7 giờ 18 phút), chạy nền trên exp-obs.
6. **Chấm** bằng bộ chấm và đáp án T-064 (không sửa); lập bảng theo ô; xét D1–D5.
7. **Phân tích nguyên nhân** cho mỗi ô tụt (và khi có điều kiện dừng), trên dữ liệu đã lưu:
   1. Đầu dò t+60, t+330 của ca mới so với ca cũ cùng ô: lỗi có tác động không (tiêm hụt là lỗi hạ tầng, không phải V082).
   2. So `entity_ranking`, khóa điểm, `kenh_co` của service gốc và service vượt lên, ca cũ so với ca mới.
   3. Đọc chú thích H5b, H8s1, H8a trong đầu ra.
   4. Chạy offline biến thể đã có cấu hình trong bản chụp (P7, V061 = bỏ H8s1, V060…) trên gói ca mới đã lưu, ra `/srv/rca-lab/m1/t069-phan-tich/`: bỏ thành phần nào thì hết tụt.
   5. Đối chiếu code đã đổi của service liên quan (`thay-doi-main.md` mục 2).
   6. Kết luận theo luật 15: "trong điều kiện X, bước Y làm sai thông tin Z" với chuỗi đầu vào → xử lý → trung gian → đầu ra; chưa xác định thì ghi phần thiếu và bằng chứng cần.
8. **Lặp tách nhiễu** (nếu có ô đổi hạng; lượt ngắn riêng, tối đa 4 ô, ~2 giờ 05 phút).
9. **Toàn vẹn sau, báo cáo:** băm lại so bước 1; LOG mục 7 AGENTS; STATE; prompt Codex soát kết quả.

## Kiểm đúng đắn

- Tiêu chí và cặp ca khai trước khi thu; đổi sau khi xem ghi là sửa sau.
- Tách lỗi hạ tầng (tiêm hụt, tải, mạng) khỏi lỗi phương pháp.
- Không kết luận trên ô không ghép được.

## Tiêu chí xong

1. `inj3.py` đã sửa, đã commit; ca thử RECREATE-PAY cho thấy Payment tạo lại đúng image và cấu hình T-067.
2. Tiêu chí khai trước có trước khi thu.
3. Đủ 17 ca mới hoặc ghi rõ ô nào không ghép được và vì sao; mỗi ca có P7 và V082, `trung_sha` đúng.
4. Có bảng theo ô cũ–mới cho V082 và P7, nhóm giải thích, kết quả D1–D5.
5. Nếu có điều kiện dừng: đã phân tích nguyên nhân theo bước 7 rồi mới trình Minh; không tự sửa V082.
6. Toàn vẹn trước = sau trên danh sách bảo vệ.

## Không làm

- Sửa V082 hoặc chọn biến thể khác (nếu tụt, trình Minh; task riêng nếu cần).
- Độ nhạy dời mốc, D14, baseline (W6, W7). Mở dữ liệu khóa.

## Chi phí, chạy nền, xử lý lỗi (luật 8, 19, 21)

- **Máy:** hệ thống cần đo chạy trên exp-app; runner, M1 trên exp-obs; tải trên máy tải AWS. Không có lựa chọn EC2 khác cho phần này.
- **Thời lượng (đo thực tế, 31,3 phút/chu kỳ):** T-063 thu2 13 chu kỳ 07:14–14:01Z 13/11; thu bù 3 6 chu kỳ 07:24–10:32Z 14/11; T-066 `e2e-001` (có M1 kèm) 30,9 phút. Thu thử 3 ca ~1 giờ 34 phút; thu chính 14 ca ~7 giờ 18 phút; lặp tối đa 4 ô ~2 giờ 05 phút. Chấm trên laptop, chưa có số đo riêng.
- **Không phụ thuộc laptop:** runner chạy `setsid nohup` trên exp-obs; bộ tải không cần phiên SSH hay mạng laptop (`load/controller/README.md`); tiêm lỗi từ exp-obs bằng khóa bộ điều khiển; M1 trên exp-obs. Laptop mất mạng không ảnh hưởng lượt chạy (kiểm ở bước 4).
- **Lỗi ở 10%, 50%, 99%** (theo `runner4.py` `chay_lich`): một ca lỗi (tiêm hỏng, ngoại lệ trong chu kỳ) → runner dọn trạng thái, bỏ ca đó, chạy tiếp; tải khởi động hỏng hai lần hoặc trạng thái không sạch → dừng cả lượt, ca đã xong giữ, ca sau chưa chạy. Khi có mạng lại: chạy tiếp đúng các ô còn thiếu bằng lịch con, không chạy lại ô đã xong. Lỗi phương pháp (P7/V082 lỗi chạy) chỉ chặn ô đó. Chỉ chạy lại toàn bộ khi bộ tiêm hoặc bộ xuất tính sai — trình Minh lý do và chi phí trước.
- **Quét điều kiện suy biến trước (luật 21c):** 3 ca thử ở bước 4 chọn đúng các đường có code đổi (RECREATE-PAY, hook Event `http.error`, `pool.hold`).
- **Song song (kế hoạch §8.4):** trong lúc T-069 dùng exp-app, phiên khác (W5) chỉ dùng dữ liệu đã thu; W4 chỉ viết luật, không chạy đêm nền.

## Rủi ro và điều chưa chắc

- Một lần thu mỗi ô: kết luận yếu; lặp chỉ giảm một phần nhiễu.
- Chỉ mục G1 ghi `nguon: "dev3"` cho ca mới (lỗi nhãn đã biết từ T-066): chỉ ảnh hưởng hiển thị Grafana.
- Cache Booking nguội sau triển khai T-067; đã có 1 giờ tải sau đó [chưa kiểm ảnh hưởng].
- Bản ghim theo `main` `640dbaf`; `main` của nhóm đã đi tiếp — không theo.
