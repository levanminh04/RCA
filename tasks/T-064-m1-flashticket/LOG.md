# Nhật ký T-064

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 0 — 13/11/2026 — Claude — laptop Minh — vai trò: người soạn SPEC (phiên điều phối T-062)

- Minh duyệt SPEC ngày 13/11/2026 (chat: "tổng thể đề xuất đã ổn … tạo ghi đầy đủ tài liệu …"; nguyên lời ở `docs/DECISIONS.md` mục chiến dịch M1-FlashTicket). SPEC ghi 12/11 ~19:20Z.
- Chưa làm bước nào của task. Bối cảnh và quyền: `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`. Trạng thái sống: `tasks/T-062-dem-chang-1-4/CHECKPOINT-CHIEN-DICH.md`.
- Bước tiếp theo chính xác: theo mục "Các bước" của SPEC và danh sách việc trong checkpoint.
- `results/T-064/tieu-chi-chon.md` ghi 12/11 ~19:17Z, sha256 `e6513b0e818a750c327ea9c4af0d12697ec98959504c1be86be4e1ad83a11fdb`. Chưa chấm biến thể nào. Trước khi chấm biến thể đầu tiên, phiên làm phải kiểm lại hash này; nếu file đã đổi thì ghi hash mới kèm lý do **trước** khi chấm.

---

## Phiên 1 — 13/11/2026 (bắt đầu 12/11 21:16Z) — Claude (Opus 5.5, desktop) — laptop Minh — vai trò: người làm; đồng thời điều phối chiến dịch

- Mở phiên theo `tasks/T-062-dem-chang-1-4/PROMPT-PHIEN-MOI.md`. Tiếp quản sau khi kiểm phiên cũ đã dừng; bằng chứng ở `CHECKPOINT-CHIEN-DICH.md`, mục "Tiếp quản 21:16Z".
- Kiểm hash `results/T-064/tieu-chi-chon.md` 21:12Z: `e6513b0e…` khớp phiên 0. Chưa chấm biến thể nào.
- **Bước 1 xong (21:25Z).** Bộ chấm `src/m1_ft/cham.py` (dùng `src/p3/danh_gia.khoi_tu_ban_ghi`/`phan_bo_hang`; tập chấp nhận nhiều thành phần = min hạng, phân bố chính xác C(g−q, m−1)/C(g, m)). Kiểm vét cạn hoán vị 300 trường hợp ngẫu nhiên + trạng thái đặc biệt: `src/m1_ft/tests/test_cham.py` → OK. Chấm P7 trên 9 ca T-062 theo quy ước P7(a): `results/T-064/cham/t062-p7.json` — 5 ca lỗi đều có nhóm hạng 1 **một thành phần** (đúng đáp án), AC@1 = 5,0, AC@3 = 5,0, tổng hạng cắt = 5,0; K = 4/4. Vậy "5/5 hạng 1" của `e2.py` không lạc quan do hòa trên 9 ca này. Bộ chấm P3 dùng được trực tiếp bản ghi M1 FlashTicket (không cần lớp chuyển).
- Quy ước tự quyết (ghi trước khi chấm biến thể): "tụt quá 2 bậc" so hạng kỳ vọng **không cắt**; ca trượt = vô cùng; trượt ở cả hai bản không tính tụt (`cham.tut_qua_2_bac`).
- **Bước 2 xong (21:30Z).** `src/m1_ft/chay.py`: cấu hình rỗng gọi thẳng `m1.chuoi.chay`; thành phần có ba móc (`vao`, `ngu_canh`, `ra`). Phép kiểm tương đương: laptop x86 lệch ulp (`results/T-064/kiem/tuong-duong-p7-laptop-x86.json`); `exp-obs` aarch64 venv P7: **9/9 trùng SHA hai lần** (`results/T-064/kiem/tuong-duong-p7-exp-obs.json`). Quyết định chạy chấm trên `exp-obs`: WHY-81. Thư mục làm việc mới trên `exp-obs`: `/opt/rca-m1ft/` (`goc/` chỉ đọc root, `out/` của user `rca`); gói tải lên sha256 `34c59324…`.
- Hợp đồng đầu ra cho T-065: `results/T-064/hop-dong-dau-ra.md` bản 1.
- **Bước 3 bắt đầu (21:55–21:58Z).** Thêm `src/m1_ft/bo_sung.py` (thông tin phụ của span từ trace thô: luồng, scope, kind, db, đích, queue, route — cùng cửa sổ và chuẩn hóa ID với adapter ghim; không nhãn), `chay(..., bo_sung=)`, CLI `src/m1_ft/chay_ca.py` (chạy 2 lần, kiểm trường cấm như runner ghim). Thành phần: `thanh_phan/h8_san.py` (H8-san: bỏ cờ hướng có độ vượt trung bình < δ; δ = 1 ms theo hạt lập lịch CFS, nguyên lý ghi trong docstring trước khi chạy), `thanh_phan/h6_nen.py` (H6a: bỏ trace có gốc CLIENT trên luồng bảo trì thư viện). Thử laptop `a5539fba`: δ = 0 trùng P7 ngoài `extra.m1_ft`; δ = 1 ms → `NO_INTRINSIC_ANOMALY` (bỏ 2 cờ); H6a bỏ 800 trace, vẫn `CAUSE_FOUND`.
- Sổ biến thể: V001–V004 ghi **trước** khi chạy (`results/T-064/so-bien-the.jsonl`, script `results/T-064/kiem/ghi_so_v001_004.py`), vai trò **kiểm cài đặt trên 9 ca T-062, không dùng để chọn**. Đang chạy trên `exp-obs` (`/opt/rca-m1ft/out/kiem-cai-dat-1`, gói `9e47d5c0…`).
- H8-adapter: adapter ghim ném `Multiple runtime series map to one logical metric` khi container bị tạo lại trong cửa sổ — để cài khi dữ liệu dev có tình huống này (kèm ca thử).
- **Kiểm cài đặt lượt 1 (xong 22:10Z, `exp-obs`, 4 bản × 9 ca, mọi lần chạy trùng SHA).** `results/T-064/cham/kiem-cai-dat-1.json` (chấm bằng `results/T-064/cham/cham_kiem_cai_dat.py`), đầu ra chép về `results/T-064/bien-the/<mã>/ra-kiem-cai-dat-1/` (gói `a8c35ff7…`). V001 (δ = 0): trùng P7 mọi khóa ngoài `extra.m1_ft` 9/9. V002 (δ = 1 ms): K 4 → 1, AC@1 = 5 giữ; bỏ cờ chỉ ở hướng có độ vượt trung bình < 1 ms (max 985 µs — sát δ). V003 (H6a): không đổi kết luận. V004 = V002. Vai trò: kiểm cài đặt, **không** dùng để chọn; sổ đã ghi dòng `sau_chay`.
- **Kiểm cài đặt lượt 2 (xong ~22:18Z, V005–V007).** `results/T-064/cham/kiem-cai-dat-2.json`, gói `b4a3164e…`. H7 (V005) không đổi kết luận; V006/V007 = K 1. Lần theo cơ chế ca FLASH sau V006: chỉ còn kênh `log_loi` của Gateway và Ticket (số dòng lỗi tăng theo tải). → H7c `log_theo_luu_luong` (chia số dòng lỗi ở A cho ρ của thành phần tăng theo tải ngoài, bọc `m1.kenh.don_vi_log`); thử laptop FLASH: H7c + H8 → `NO_INTRINSIC_ANOMALY`.
- **H1 (22:20–22:30Z).** `thanh_phan/h1_canh.py`: H1a (cạnh dữ liệu từ span CLIENT có `db.system`, đích `db.name`/Redis→`cache`; cạnh gọi qua `m1.span.mau_canh`; **mọi cạnh chấm cùng E4 không G3**, e = rA − rN — không dùng điểm cạnh của P7 vì khác thang); H1b (định vị: phía gọi nếu bên gọi có cờ ở op SERVER hoặc metric không lan; phía đích tương tự; bên gọi tầng 3 → không ảnh hưởng; chỉ `rieng_canh` giữ cờ). Thử laptop: EVENT-DB-LAT đúng cạnh `event-service→event_db` hạng 1 (e 0,953); NET-GW-BOOK `api-gateway→booking-service` hạng 1 (0,952); CPU-BOOK: 9 cạnh phía gọi, `user-service→user_db` (nạn nhân tranh CPU, bên gọi tầng 3) → không ảnh hưởng. Bộ chấm thêm `chieu_canh_ve_nut`, `cham_canh` (tiêu chí mục 2), kiểm đơn vị OK.
- Sổ V008–V011 ghi trước khi chạy (`ghi_so_v008_011.py`, mã nguồn `335b290b…`); đang chạy trên `exp-obs` (`goc-3`, gói `5b878f60…`).
- **Kiểm cài đặt lượt 3 (xong ~22:33Z, V008–V011, 36/36 lần trùng SHA).** `results/T-064/cham/kiem-cai-dat-3.json` (gói `04503b38…`). Bộ chấm bổ sung chiếu cạnh → nút và bảng cạnh (đáp án cạnh từ `root` T-059). V008 (H7c + H8): K = 0/4, AC@1 = 5. V009–V011 (H1a/H1b): bảng cạnh 2/2 đúng cạnh hạng 1 nhưng AC@1 giảm (3,33 / 3,67 / 4,33) — cơ chế: cạnh yếu "riêng cạnh" đứng hạng 1 danh sách cạnh riêng, phép chiếu của tiêu chí đẩy hai đầu lên ngang gốc (ca và cạnh cụ thể ở sổ `sau_chay`). → **H1c** (WHY-82): hạng cạnh trong danh sách chung nút + cạnh; thử laptop 3 ca: p1 = 1, đúng cạnh hạng 2. Thiết kế sau kiểm cài đặt 9 ca T-062 (không phải tập chọn) — ghi rõ.
- **H2/H3 (22:35Z).** `thanh_phan/h2_h3_kenh.py` + đường ống metric chung trong `chay.py` (`_duong_ong_metric`, `dung_lai_metric`: dựng lại metric một lần bằng adapter ghim, khai thêm kênh lớp "tài nguyên"); H7 chuyển sang móc `bien_doi_bundle` — so mã cũ/mới trên laptop 2 ca: trùng SHA. Gói bổ sung 9 ca T-062 xuất từ Prometheus (dữ liệu 11/11 còn nhờ TD-01): `results/T-063/ca-t062-bo-sung/` (SHA256SUMS), tải lên `/opt/rca-m1ft/bo-sung/` (9/9 khớp). V012 (H2), V013 (H3) ghi sổ trước khi chạy; đang chạy (`goc-4`, gói `7ae4d5e7…`). V014 (H1c), V015 (H1c+H7c+H8s1) ghi sổ.
- **Kiểm cài đặt lượt 5 (22:50Z, V014–V015, 18/18 trùng SHA, gói `abdfdda2…`).** `results/T-064/cham/kiem-cai-dat-5.json`. V014 (H1c): AC@1 = 5, bảng cạnh 2/2 đúng cạnh hạng 2. V015 (H1c + H7c + H8s1): AC@1 = 5, K = 0/4, cạnh 2/2 hạng 2. Chỉ là kiểm cài đặt trên 9 ca T-062; giữ/bỏ quyết trên tập chọn dev bản 2. Lưu ý: 9 ca này là nơi H1c/H7c được thiết kế sau khi xem kết quả — không dùng làm bằng chứng hiệu quả.
- **H4/H5 (02:17Z).** `thanh_phan/h4_h5.py`: H4 (queue-ready/unacked/dlq-ready theo queue → service consumer bằng quy ước tên), H5 (live-down/live-ms từ httpcheck → service theo bảng cổng). Bộ xuất gói bổ sung bản 2 (`T063-bo-sung-2`, +2 kênh liveness). Thử biến đổi trên gói xuất mới: gán đủ 4 service consumer, 8 URL. Chưa có dữ liệu lỗi queue/pause sau TD-02/TD-04 → chỉ chấm được trên dev bản 2.
- **H1a thêm cạnh message (02:19Z).** span PRODUCER/CLIENT của scope rabbitmq → cạnh (service → broker, loại message). Thử trên gói tải mua vé `krb4a3d5` (results/T-063/kiem-r): 3 cạnh message (booking/payment/ticket → broker), 8 cạnh dữ liệu, 12 cạnh gọi. Cần cho ô CONSUMER-BOOK-SLOW. Kiểm cài đặt, chưa chấm.
- **Chuẩn bị chấm tập chọn dev bản 2 (13/11 ~07:55Z, trước khi có dữ liệu đợt thu chính).**
  - Đáp án khai trước: `results/T-064/dap-an-dev2.json`, lấy nguyên từ `results/T-059/danh-muc-loi.json`: gốc nút/cạnh và `common_accepted_entities`. Thêm PAUSE-PAYMENT từ `results/T-063/o-dev-bo-sung.md`. HTTP5-EVENT-FLASH dùng đáp án của HTTP5-EVENT (WHY-83). Hash nguồn ghi trong file.
  - Tên thực thể trong đầu ra M1 trên tải mua vé (`event_db`, `cache`, `api-gateway`…) khớp tập chấp nhận.
  - Điều kiện vào tập chọn: hậu kiểm `results/T-063/chay/xac-nhan-ca.json` theo `results/T-063/chay/dieu-kien-xac-nhan.md` (khai 07:30Z).
  - Đường chạy biến thể trên ca mới: `chay_ca.py --bo-sung ~/rca-dieu-phoi/ca/{id}/prometheus-bo-sung.json`.
  - Ghi nhận: Claude đã thấy đầu ra M1 của ca thử `865c8e93` (HTTP5-EVENT-FLASH, không phải ca RCA, không vào tập chọn) khi kiểm tên thực thể.
- Kiểm hash `results/T-064/tieu-chi-chon.md` 07:13Z (đóng băng bản 2): `e6513b0e…` khớp.
- **Lỗi cài đặt H7c, phát hiện khi quét điều kiện suy biến trên ca thử (13/11 ~08:40Z, trước khi chấm tập chọn; luật 21c).**
  - Hiện tượng: bản gộp, rồi H7c riêng, trả `status ERROR` ("Out of range float values … nan") trên ca thử `865c8e93`. Ca này có 2.159 dòng lỗi Event dưới tải ×3.
  - Lần theo: H7c đặt `n_A ← n_A/ρ` (số thực). `m1.e4.cham_dem` gọi `binom.sf(n_A−1, n, p0)` với `n = n_N + n_A` không nguyên, scipy trả NaN.
  - Vì sao 9 ca T-062 không lộ: đơn vị `log_loi` ở đó không vào trạng thái OK (ít dòng lỗi). Chưa kiểm từng ca.
  - Sửa trong `src/m1_ft/thanh_phan/h7_tai.py`: `n_A ← int(round(n_A/ρ))`, sai số ≤ 0,5 dòng, giữ ý thiết kế "tỷ lệ dòng lỗi trên request". Không sửa `src/m1`.
  - Hệ quả: mã nguồn đổi trước khi ghi sổ lượt chọn. Kết quả kiểm cài đặt cũ của V008/V011/V015 trên 9 ca T-062 thuộc mã cũ; chạy lại trên mã mới cùng tập không hồi quy.
  - Đang quét 27 cấu hình lượt 1 trên ca thử (laptop, chỉ kiểm lỗi chạy, không chấm).
- **Sổ lượt chọn (08:33Z).**
  - `results/T-064/kiem/ghi_so_chon_dev2.py` ghi 27 bản `chon_dev2_luot1`, mã nguồn `f3211295…`:
    - V001–V015 chạy lại trên mã mới;
    - V016-H7c, V017-H4, V018-H5 (thêm riêng);
    - V019-GOP (8 thành phần);
    - V020–V027 (bỏ từng thành phần).
  - Quét 27 cấu hình trên ca thử: OK, tất định (laptop, không chấm).
  - Mã nguồn lên `exp-obs:/opt/rca-m1ft/goc-6` (TD-64-06b).
- **Quyết định vận hành.** `exp-obs` có 2 lõi, đang nhận telemetry cho đợt thu. Lô biến thể (gồm tập không hồi quy 9 ca T-062) chỉ chạy **sau khi đợt thu xong**; `results/T-064/kiem/chay_bien_the_obs_dev2.sh` tự từ chối nếu `runner3` còn chạy. Lý do: tính đúng đắn của dữ liệu thu ưu tiên hơn ~1,5 giờ tiết kiệm.
- **Khai tập chọn dev bản 2 (13/11 ~14:22Z), TRƯỚC khi chấm.** Chưa xem đầu ra M1/biến thể của ca nào trong lượt chính.
  - Đợt thu xong 14:01Z: 13/13 chu kỳ, M1 P7 OK tất định. Hậu kiểm theo `results/T-063/chay/dieu-kien-xac-nhan.md`.
  - **Tập A — 12 ca, điều kiện khai trước:** `results/T-064/tap-chon-dev2-12.json`, nguồn `results/T-063/chay/xac-nhan-ca.json`.
    - Ca lỗi (7): 4af494a5=EVENT-DB-LAT, 19b17e22=CPU-BOOK-1, e9c9679b=HTTP5-EVENT, 6949870c=REDIS-BOOK, 5fb8208f=NET-GW-BOOK, 60166807=CPU-BOOK-2, 98ea5ba4=HTTP5-EVENT-FLASH.
    - Ca không lỗi (5): eb48d6b3, 729604d2, 83073ed1, f20b0ca5 = BINH-THUONG; fb1cf0e9 = FLASH-HEALTHY.
  - **Tập B — 13 ca, theo "Sửa sau 1" (chờ Minh):** tập A + 46aab4be=PAUSE-PAYMENT. File `results/T-064/tap-chon-dev2-13.json`, nguồn `xac-nhan-ca-2.json`. Lý do sửa: điều kiện pause khai trước chép sai chuỗi trạng thái Docker (`running true`, đúng ra là `paused true`), ghi ở `dieu-kien-xac-nhan.md`.
  - Chấm báo cả A và B.
- **Lô biến thể phát 14:13Z trên `exp-obs`** (sau đợt thu): 27 bản × 13 ca → `/opt/rca-m1ft/out/chon-dev2-1`; 27 bản × 9 ca T-062 (không hồi quy) → `/opt/rca-m1ft/out/khong-hoi-quy-1`. Hai luồng song song (2 lõi).
  - Lần phát đầu 14:09Z bị bộ chặn từ chối nhầm: `pgrep -f` khớp chính dòng lệnh shell. Đã sửa bằng `ps | grep '[p]ython3 -B runner3'`; giữ log `*-tu-choi.log`.
  - Cùng lỗi này làm phép kiểm "bộ chạy còn sống" của monitor đợt thu luôn báo ALIVE (điểm mù theo dõi). Không gây hậu quả, vì bộ chạy không chết và sổ có nhịp đều.
- **Tập không hồi quy 9 ca T-062, lượt chọn (xong ~17:00Z 13/11, mã `f3211295…`).**
  - Kết quả: `results/T-064/cham/khong-hoi-quy-1.json`, chấm bằng `cham_kiem_cai_dat.py --tm=ra-khong-hoi-quy-1` (thêm tham số `--tm`, mặc định giữ như cũ). Đầu ra ở `results/T-064/bien-the/<mã>/ra-khong-hoi-quy-1/`.
  - 243/243 lần chạy trùng SHA. P7: AC@1 = 5, K = 4.
  - Không xấu đi: mọi bản trừ V009/V010/V011 (H1a/H1b; AC@1 3,33 / 3,67 / 4,33).
  - K: V008 = V015 = 0; V002/V004/V006/V007/V021 = 1; các bản gộp còn lại 2; V027 4.
  - V008/V015 cho cùng kết luận như kiểm cài đặt trước khi sửa H7c.
- **Chấm lượt chọn 1 xong (13/11 ~18:35Z).**
  - 351/351 lần chạy OK, trùng SHA. V001 trùng P7 13/13.
  - Kết quả: `results/T-064/cham/chon-dev2-luot1-tap{12,13}.json`; luật giữ/bỏ §4: `…-giu-bo.json` (script `results/T-064/cham/giu_bo.py`). Sổ: 27 dòng `sau_cham`.
  - **P7, tập A (7 ca lỗi, 5 ca không lỗi):** AC@1 = 5, AC@3 = 7, tổng hạng 9, K = 4/5. Ca trượt hạng 1: EVENT-DB-LAT (hạng 2), HTTP5-EVENT-FLASH (hạng 2). Tập B thêm PAUSE-PAYMENT: đáp án vắng trong danh sách, tính là trượt.
  - **Phép 1, thêm riêng vào P7 (tập A):**
    - H8s1 GIỮ (luật 2: K 4 → 3, X bằng; EVENT-DB-LAT 2 → 1 nhưng CPU-BOOK-2 1 → 2).
    - H1c GIỮ (luật 3: cạnh đúng top 3 ở 3/3 ô; X không xấu đi; tổng hạng 9 → 9,5).
    - H1a, H1b BỎ (AC@1 giảm).
    - H2 BỎ (K +1). Ở tập B, H2 là đánh đổi: PAUSE-PAYMENT ∞ → 4.
    - H5: tập A không tác dụng; tập B GIỮ (luật 1: PAUSE-PAYMENT ∞ → 4, K không đổi).
    - H6a, H7, H7c, H3, H4: không tác dụng trên dev bản 2.
  - **Phép 2, bỏ khỏi bản gộp V019** (bản gộp xấu hơn P7: K 5/5, cạnh 0/3):
    - Bỏ H2 → K 5 → 3.
    - Bỏ H3 → cạnh 0 → 2/3, nhưng tổng hạng 9,5 → 10, nên luật tính "giữ H3 (luật 1)". Mâu thuẫn với phép 1 (H3 không tác dụng) và với cơ chế Q2.
    - Các thành phần khác không tác dụng trong bản gộp.
  - **Tổ hợp:** V015 (H1c + H7c + H8s1) GIỮ so với P7 (luật 2 và 3: K 3/5, cạnh 3/3, AC@1/AC@3 bằng, tổng hạng 10), không tụt quá 2 bậc. Không hồi quy trên T-062 (X = P7, K = 0/4). H7c không thêm gì trên dev bản 2 (V008 = V002), nhưng giảm K ở ca FLASH của T-062.
  - Cơ chế đang lần: `results/T-064/phan-tich/ghi-chu-co-che-dev2.md` (Q1, Q2).

---

## Phiên 2 — 14/11/2026 giờ VN (bắt đầu 13/11 19:24Z) — Claude (Fable 5.2, desktop, lịch `m1ft-tiep-nhan`) — laptop Minh — vai trò: người làm; đồng thời điều phối chiến dịch

- Tiếp nhận từ phiên 1 (Claude, cùng vai trò) sau khi kiểm phiên cũ đã kết thúc lượt và không còn lệnh con; bằng chứng ở `CHECKPOINT-CHIEN-DICH.md`, mục "Tiếp quản 19:24Z". Không có người thật theo dõi trong phiên này.
- Kiểm lại đầu ra phiên 1: `results/T-064/cham/chon-dev2-luot1-tap{12,13}.json` đọc được, 28 bản; số P7 và V015 khớp LOG. `exp-obs` rảnh lúc 19:25Z.
- Kiểm hash `results/T-064/tieu-chi-chon.md` 19:30Z: `e6513b0e…` khớp.
- **Cơ chế hai ca sai còn lại của V015 (trước khi thiết kế lượt 2).** Ghi ở `results/T-064/phan-tich/ghi-chu-co-che-dev2.md` Q5, Q6.
- **Lượt chọn 2 — thiết kế sau khi đã xem kết quả lượt 1 trên cùng tập chọn (khai rõ).**
  - Mã mới, mặc định tắt: `h1_canh.py` tham số `bo_kenh_dinh_vi`; `h4_h5.py` tham số `chet_im_giay` (H5b). Nguyên lý và điều kiện thất bại ghi trong mã và sổ.
  - Thử cài đặt trên laptop **trước khi ghi sổ**, trên ba ca của tập chọn (46aab4be, 4af494a5, 83073ed1): H5b đưa Payment lên nhóm đầu ở 46aab4be (đầu dò không phản hồi 20 mẫu, từ t+15 s tới hết cửa sổ); hai ca kia không có thành phần chết im; bản gộp bỏ kênh pool khỏi định vị vẫn mất cạnh event→event_db vì `jvm-cpu`. Tất định 5/5. Đây là kiểm cài đặt nhưng đã thấy kết quả trên ca chọn — ghi trong sổ.
  - Sổ: 10 dòng `chon_dev2_luot2` (`results/T-064/kiem/ghi_so_chon_dev2_luot2.py`, 19:30Z, mã nguồn `6ab3a59d…`): V028 (H1c+H8s1), V029 (+H5+H7c), V030/V031 (bản gộp, định vị bỏ kênh pool / bỏ pool + JVM), V032 (H5b riêng), V033, V034 (H5b trong ứng viên), V035–V037 (đối chứng mã nguồn cho V015, V018, V019).
  - Phát 19:32Z trên `exp-obs` `goc-7` (TD-64-08): 10 × 13 ca dev bản 2 và 10 × 9 ca T-062, hai luồng. Ước 50–70 phút theo nhịp lượt 1 (chưa kiểm).
  - Luật 21: lỗi một (bản, ca) không chặn phần còn lại; chạy lại bỏ qua (bản, ca) đã có `summary.json`. Lỗi mã nguồn thì sửa, lên `goc-8`, chạy lại cả lô (~1 giờ).

---

## Phiên 3 — 14/11/2026 giờ VN (bắt đầu 13/11 22:24Z) — Claude (Fable 5.2, desktop, lịch `m1ft-tiep-nhan`) — laptop Minh — vai trò: người làm; đồng thời điều phối chiến dịch

- Tiếp nhận từ phiên 2 (Claude, cùng vai trò). Phiên 2 dừng 21:08Z vì hết hạn mức 5 giờ, ngay khi lô lượt chọn 2 báo xong; chưa nhận, chưa chấm. Bằng chứng ở `CHECKPOINT-CHIEN-DICH.md`, mục "Tiếp quản 22:24Z". Không có người thật theo dõi trong phiên này.
- `exp-obs` 22:22Z: ba log lượt 2 in `XONG`; 130/130 (dev bản 2) và 90/90 (T-062) `summary.json`. Không phát lại.
- Kiểm hash `results/T-064/tieu-chi-chon.md` 22:22Z: `e6513b0e…` khớp.
- **Nhận và kiểm lô lượt chọn 2 (22:27Z).** `bash results/T-064/kiem/nhan_luot2.sh`: gói `luot2-out.tgz` sha256 `25a00347…` trùng hai đầu (`results/T-064/kiem/nhan-luot2/`). `kiem_luot2.py` → `results/T-064/kiem/kiem-luot2.json`: 220/220 (bản, ca) có `summary.json`, thiếu 0, không OK 0, không trùng SHA 0. Ba bản đối chứng mã nguồn V035/V036/V037 trùng V015/V018/V019 lượt 1 ngoài siêu dữ liệu ở 13/13 ca dev bản 2 và 9/9 ca T-062. Đầu vào thật: H5b báo `payment-service` chết im chỉ ở ca 46aab4be (ba bản có H5b); định vị bỏ kênh pool/JVM có bằng chứng bị bỏ ở 8 và 17 ca.
- **Chấm lượt chọn 2 (22:30Z).** `cham_dev2.py` (P7 + 10 bản) → `results/T-064/cham/chon-dev2-luot2-tap{12,13}.json`; `giu_bo_luot2.py` (danh sách phép so khai 19:45Z, trước khi có kết quả) → `…-giu-bo.json`; `cham_kiem_cai_dat.py --tm=ra-khong-hoi-quy-2 --ra=khong-hoi-quy-2.json` → `results/T-064/cham/khong-hoi-quy-2.json`. P7 trong file lượt 2 trùng lượt 1 ở cả hai tập. Sổ: 10 dòng `sau_cham` (`results/T-064/kiem/ghi_so_sau_cham_luot2.py`; sổ 104 dòng).
  - Tập A: V028, V015 (= V035), V029, V033, V034 cho **cùng** AC@1 5, AC@3 7, tổng hạng 10, K 3/5, cạnh 3/3; đều GIỮ so với P7 (luật 2, 3). H5, H5b, H7c không tác dụng trên tập A. Hai bản gộp sửa định vị (V030, V031): K 5/5, BỎ so với P7; so với bản gộp V019 thì cạnh 0/3 → 2/3 và 3/3.
  - Tập B: H5b đưa PAUSE-PAYMENT lên hạng 1 (V032, V033, V034: AC@1 6, AC@3 8); H5 cũ hạng 4–4,5. H5b hơn H5 theo luật 1 cả khi đứng riêng lẫn trong tổ hợp.
  - Không hồi quy T-062: mọi bản lượt 2 AC@1 = 5, không xấu đi. K: V029/V033/V035 = 0; V028/V034 = 1; V030/V031/V037 = 2; V032/V036 = 4.
- **Áp thứ tự chọn §5 trên cả 37 bản (22:35Z).** Kết quả: `results/T-064/ho-so-chon.md` (bản nháp 1) mục 4.
  - Quan sát: bản đứng đầu theo đúng chữ §5 là V002-H8s1 trên tập A (tổng hạng 9, K 3) và V032-H5b trên tập B (AC@1 6, tổng hạng 10, K 4). Bản gom đủ thành phần đạt luật giữ (V028 trên A, V034 trên B) xếp sau vì tổng hạng lớn hơn 1,0.
  - Đã kiểm nguồn của 1,0 này: `entity_ranking` (thực thể, `tie_group`) của V002 và V028 trùng nhau ở 60166807, 98ea5ba4, 4af494a5. Chênh đến từ phép chiếu cạnh về nút của tiêu chí §2 (cạnh hạng 2 cho nút DB cùng hạng 2 với đáp án ở CPU-BOOK-2 và HTTP5-EVENT-FLASH).
  - Suy luận: H1c không làm xấu thứ tự nút trên tập này; nó bị trừ bởi quy ước chấm đã khai. Không đổi tiêu chí: người làm ghi V002 là bản theo đúng §5, V028 là bản thay thế có cạnh, V034 là bản thay thế nếu dùng tập B. Điểm này trình Minh.
- **Chưa làm trong phiên này:** phép dời mốc ±30 s (§7; `chay_ca.py` chưa có tham số dời `t`); H8-adapter, H8-log; `chu-thich-thao-tac-nen.md`, `cau-hinh-de-xuat.json`, `ban-xuat/chi-muc-ban.json`, `manifest.json`.
- **Đính chính giờ (22:28Z).** Các mốc "22:27Z", "22:30Z", "22:35Z" ở ba dòng trên là ước lượng sai của người làm. Giờ thật theo file: sổ `sau_cham` ghi 22:23:49Z; toàn bộ nhận, kiểm, chấm và áp §5 nằm trong khoảng 22:22–22:27Z (đồng hồ `date -u` 22:28:10Z khi viết dòng này). Nội dung và số không đổi.
- **Phát phản biện (22:28Z), theo quyền điều phối chiến dịch.** Brief dựng bằng `results/T-064/kiem/dung_brief_phan_bien.py`: Prompt chung và khối công đoạn chép nguyên văn từ `docs/review-prompt.md` (phần sau khối thông tin trùng từng byte với brief R2 của T-063 đã dùng), chỉ điền thông tin trung tính.
  - T-064 lượt 1, khối "Soát kết quả": `results/T-064/codex/R1-brief.md` → Codex ghi `tasks/T-064-m1-flashticket/REVIEW.md`. Lệnh nền `bfhyqxxle`, trạng thái `results/T-064/codex/R1-trang-thai.json`.
  - T-063 lượt 3, khối "Kiểm lại phản hồi và sửa": `results/T-063/codex/R3-brief.md` → `tasks/T-063-quan-sat-thu-dev-2/REVIEW-3.md`. Lệnh nền `b7qdk2s8w`.
- **Chú thích thao tác nền (22:30Z, tiêu chí §7).** `results/T-064/phan-tich/chu_thich_nen.py` → `results/T-064/chu-thich-thao-tac-nen.md` và `phan-tich/chu-thich-thao-tac-nen.json`: 9 ca không tiêm lỗi (5 dev bản 2, 4 T-062) × P7, V002, V028. Chỉ đọc đầu ra đã lưu; K không đổi cách đếm.
  - Quan sát: ở 7 ca BINH-THUONG, không đơn vị thao tác nào của `api-gateway` có cờ thô hướng lên (0/6 hoặc 0/5); FLASH-HEALTHY dev bản 2 có 2/6. Đây là chỉ số phía M1, chưa đối chiếu k6.
  - Quan sát: độ vượt lớn nhất bị sàn 1 ms bỏ là 762, 977, 985 µs ở ba ca — sát sàn. Kết quả K nhạy với giá trị sàn; chưa quét sàn khác (chưa kiểm).
- **Tự soát trước khi đọc REVIEW (ghi lại tại 22:48Z).** Hai điểm tự tìm: N1 (mốc giờ ước lượng sai, đã đính chính), N2 (độ vượt bị bỏ sát sàn 1 ms, K nhạy với δ). Người làm **không** tự tìm ra R1–R4.
- **Đáp phản biện lượt 1 (22:48Z).** Codex R1 xong 22:45Z: `tasks/T-064-m1-flashticket/REVIEW.md`, ba điểm chặn (R1 loại cạnh H1, R2 tên đối chứng, R3 thiếu WHY) và R4 không chặn. Người phản biện tính lại độc lập bốn bảng điểm và hai bảng không hồi quy: khớp. Người làm kiểm từng điểm trên file: **cả bốn đúng**.
  - R1: đầu ra V028 ca 98ea5ba4 khớp số của người phản biện. Khoanh phạm vi bằng phép đếm trên V028: 4 cạnh `http` sai loại ở 13/13 ca dev bản 2, 0/9 ca T-062, không cạnh nào có cờ. **Chưa sửa mã.**
  - R2, R4: sửa diễn giải trong `results/T-064/ho-so-chon.md` (mục 4, 8, thêm mục 9).
  - R3: thêm `docs/WHY.md` WHY-85 (sàn 1 ms) và WHY-86 (H5b), ghi rõ là ghi muộn. Đây là vi phạm luật cứng 3 của người làm ở phiên 1 và 2: hai lựa chọn đã dùng trong kết quả trước khi có WHY.
  - Bảng phản hồi cuối `REVIEW.md` đã điền; cột Minh quyết để trống.
- **Kết quả sau đáp:** theo quyền đã cấp và đúng §5, bản đề xuất tạm là V002-H8s1 (tập A); V032-H5b nếu Minh nhận tập B. Mọi bản có H1 giữ làm lịch sử của mã có lỗi R1.
- **Báo cáo theo mục 7.**
  1. Đã làm: nhận, kiểm, chấm lượt chọn 2; hồ sơ chọn bản nháp; chú thích thao tác nền; phát và đáp phản biện lượt 1.
  2. File đổi: `results/T-064/` (hồ sơ chọn, chú thích nền, bảng chấm lượt 2, sổ, đầu ra 10 bản, script trong `kiem/` và `phan-tich/`, `codex/R1-*`); `docs/WHY.md` (thêm WHY-85, WHY-86); bảng phản hồi cuối `REVIEW.md`; LOG này; dòng T-064 trong STATE. Không sửa `src/`.
  3. Kiểm đã chạy: `kiem_luot2.py` (220/220, đối chứng trùng); so thứ tự nút V002 với V028 ở ba ca; đếm cạnh sai loại trên 22 ca của V028. Người phản biện tính lại độc lập các bảng điểm: khớp.
  4. Còn mở:
     - Task đạt: 37 bản đã chấm tất định; thứ tự §5 xác định trên hai tập; cơ chế ca sai Q1–Q6.
     - Câu hỏi nguồn mới trả lời một phần: chưa có đối chứng bỏ quan hệ (R2); đầu ra cạnh H1 sai loại (R1); H3, H4 chưa có ô lỗi; H8-adapter, H8-log chưa cài; sàn 1 ms chưa có căn cứ đo (WHY-85).
     - Chưa đạt SPEC: phép dời mốc ±30 s, `cau-hinh-de-xuat.json`, `ban-xuat/chi-muc-ban.json`, `manifest.json`, thư mục `co-che/` (hiện là `phan-tich/`).
     - Chờ Minh: tập A hay B; FLASH-HEALTHY; sửa hook thử H3.
- **Bước tiếp theo chính xác:**
  1. Sửa R1 trong `src/m1_ft/thanh_phan/h1_canh.py` (đoạn sau `prep = m1span.chuan_bi(...)`): đọc `src/m1/span.py::mau_canh` (dòng 164–174) để lặp đúng điều kiện span bọc, tách mẫu theo kind của span cha và con lấy từ `bo_sung` (`phu[...]['kind']`: 3 CLIENT, 4 PRODUCER, 5 CONSUMER), xuất loại `http` hoặc `message`; cặp thiếu kind ghi `khong_ro`. Thêm test đơn vị với ca 98ea5ba4 (kỳ vọng Payment → Booking: http 72, message 144).
  2. Ghi sổ lượt 3 trước khi chạy (mẫu `results/T-064/kiem/ghi_so_chon_dev2_luot2.py`): chạy lại V014, V028, V034, V033, V015 và một bản đối chứng không H1 (V002) trên mã mới; lên `exp-obs` `goc-8` theo TD-64-08; nhận bằng bản sao của `nhan_luot2.sh`.
  3. Thiết kế đối chứng bỏ quan hệ (R2): cấu hình tắt E1/E2/E5 qua `bat_tat` của đầu vào, nếu `src/m1_ft/chay.py` cho phép mà không sửa `src/m1`; ghi WHY trước khi dùng kết quả.
  4. Dời mốc ±30 s; bản xuất cho T-065; manifest.
- **Prompt cho người phản biện (kiểm lại phản hồi và sửa):** dựng bằng `results/T-064/kiem/dung_brief_phan_bien.py` sau khi sửa R1 và có kết quả lượt 3, khối "Kiểm lại phản hồi và sửa" của `docs/review-prompt.md`, ghi `REVIEW-2.md`. Chưa phát ở phiên này vì R1 chưa sửa; phát ngay bây giờ chỉ kiểm được phần tài liệu.
- Lệnh cuối: script đáp phản biện (thêm WHY, sửa hồ sơ, điền bảng phản hồi).
- **Sửa R1 (22:49–22:51Z), trong quyền chiến dịch.** `src/m1_ft/thanh_phan/h1_canh.py`: cạnh service → service không còn lấy từ `m1.span.mau_canh` rồi gán `http`; thay bằng vòng lặp cùng điều kiện span bọc trên `prep` của P7, tách mẫu theo loại span của span bọc và con: CLIENT → SERVER = `http`, PRODUCER → CONSUMER = `message`, khác hoặc thiếu thông tin = `khong_ro`. Tham số `gop_loai_cu` tái lập hành vi cũ để làm đối chứng. Không sửa `src/m1`. Mã nguồn mới `7b4249ff…`.
  - Kiểm cài đặt trên laptop, ca 98ea5ba4 (thuộc tập chọn, đã khai trong sổ): Payment → Booking tách thành `http` 72/0 và `message` 144/0; Booking → Payment, Payment → Ticket, Ticket → Payment thành `message` 144, 72, 72 — khớp phép đếm độc lập của người phản biện. Không có cạnh `khong_ro`. `gop_loai_cu` cho lại đúng danh sách cạnh và thứ tự nút của V028 lượt 2. Thứ tự nút và hai cạnh có cờ của bản sửa trùng lượt 2 ở ca này. Hai lần chạy trùng SHA. `test_cham.py` OK.
  - Chưa thêm test đơn vị riêng cho phép tách loại (bước tiếp theo từng ghi); phép kiểm hiện có là ca 98ea5ba4 và `kiem_luot3.py`.
- **Lượt chọn 3 — chỉ để sửa lỗi, không có ý tưởng mới.** Sổ: 10 dòng `chon_dev2_luot3` ghi 22:51:31Z trước khi chạy (`results/T-064/kiem/ghi_so_chon_dev2_luot3.py`): V038–V045 là chạy lại nguyên cấu hình của V014, V028, V015, V034, V033, V009, V010, V031 trên mã đã sửa; V046 (V028 với `gop_loai_cu`) và V047 (V002) là đối chứng mã nguồn. Khai: chạy sau khi đã xem lượt 1 và 2.
  - Phát 22:52Z trên `exp-obs` `goc-8` (TD-64-09): 10 × 13 ca dev bản 2 và 10 × 9 ca T-062. Nhịp lượt 2: khoảng 90 phút cho cùng khối lượng (19:32 → 21:05Z); lượt này chưa đo.
  - Luật 21: như lượt 2. Lỗi ở 10%, 50%, 99%: một (bản, ca) lỗi chỉ ghi dòng lỗi, chạy lại bỏ qua cặp đã có `summary.json` (vài phút cho phần thiếu). Lỗi mã nguồn: sửa, lên `goc-9`, chạy lại cả lô (~1,5 giờ máy, không cần laptop).
- **Bước tiếp khi lô xong (ba log in `XONG`):** `bash results/T-064/kiem/nhan_luot3.sh` → `py -3 -B results/T-064/kiem/kiem_luot3.py` (đủ 220, đối chứng V046 = V028 và V047 = V002, số ca đổi thứ tự nút hoặc đổi cạnh có cờ so với bản cha) → `cham_dev2.py` cho P7 + 10 bản trên hai tập (`--ra results/T-064/cham/chon-dev2-luot3-tap{12,13}.json`) → `cham_kiem_cai_dat.py --tm=ra-khong-hoi-quy-3 --ra=khong-hoi-quy-3.json` → sổ `sau_cham` (mẫu `ghi_so_sau_cham_luot2.py`) → cập nhật hồ sơ chọn mục 9 → phát Codex kiểm lại (`REVIEW-2.md`, khối "Kiểm lại phản hồi và sửa").
- **Quyết định của Minh trong phiên (ghi 23:21Z).** Nguồn: `docs/DECISIONS.md`, mục "Tập chọn dev bản 2: nhận "Sửa sau 1", dùng 13 ca, 13/11/2026" (Minh trả lời ~23:19Z trong phiên `ed8b9c01…`: "Đồng ý, dùng 13 ca"; phiên đó ghi DECISIONS và báo sang phiên điều phối này). Phiên này không trực tiếp nhận lời Minh; căn cứ là dòng đã ghi trong DECISIONS.
  - Hệ quả: tập chọn chính của T-064 là tập B, 13 ca (`results/T-064/tap-chon-dev2-13.json`); kết quả tập A giữ làm lịch sử và báo độ nhạy. Tiêu chí chọn không đổi.
  - Theo §5 trên tập B với số đã chấm (lượt 1 và 2): V032-H5b đứng đầu. Lượt 3 không chứa bản nào xếp trên V032 theo §5 trừ khi tách loại cạnh làm đổi điểm nút; áp lại §5 sau khi chấm lượt 3.
  - Giới hạn phải giữ trong hồ sơ: điều kiện xác nhận pause sửa sau khi có dữ liệu; H5b thiết kế sau khi xem đúng ca PAUSE-PAYMENT, chỉ một ô.
- **Nhận, kiểm, chấm lượt chọn 3 (00:30–00:31Z 14/11).** Lô xong trên `exp-obs`; `nhan_luot3.sh` (gói `4b8c6ca6…` trùng hai đầu, `results/T-064/kiem/nhan-luot3/`); `kiem_luot3.py` → `kiem/kiem-luot3.json`; `cham_dev2.py` → `cham/chon-dev2-luot3-tap{12,13}.json`; `cham_kiem_cai_dat.py --tm=ra-khong-hoi-quy-3 --ra=khong-hoi-quy-3.json`; sổ 10 dòng `sau_cham` (`kiem/ghi_so_sau_cham_luot3.py`).
  - 220/220 hợp lệ, trùng SHA. Hai đối chứng mã nguồn trùng lượt trước ở 22/22 ca. Không có cạnh `khong_ro`.
  - Tám bản có H1 sau sửa: thứ tự nút trùng bản cha 22/22 ca; mọi đại lượng chấm bằng bản cha trên cả ba tập. Chỉ V043-H1a đổi danh sách cạnh có cờ ở ba ca. Chi tiết: hồ sơ chọn mục 11.
  - Áp §5 trên tập 13 ca (tập chính theo quyết định của Minh): V032-H5b vẫn đứng đầu.
  - Chưa làm: lần từng cạnh đổi cờ của V043; test đơn vị riêng cho phép tách loại.
- **Phát Codex kiểm lại (00:31Z).** `results/T-064/codex/R2-brief.md` (khối "Kiểm lại phản hồi và sửa", nguyên văn `docs/review-prompt.md`, thông tin trung tính) → Codex ghi `tasks/T-064-m1-flashticket/REVIEW-2.md`. Trạng thái: `results/T-064/codex/R2-trang-thai.json`.
- **Bước tiếp theo chính xác:** (1) khi R2 xong: tự soát, đọc `REVIEW-2.md`, điền bảng phản hồi; (2) `results/T-064/ban-xuat/chi-muc-ban.json` theo `hop-dong-dau-ra.md` mục 3 cho P7, V032 (đề xuất tạm), V041 (thay thế có cạnh), rồi brief G-c cho Codex ở T-065; (3) đối chứng bỏ quan hệ; (4) dời mốc ±30 s; (5) H8-adapter, H8-log, ô H4; manifest.
- **Đáp phản biện lượt 2 (00:47Z 14/11).** Codex R2 xong 00:46Z: `tasks/T-064-m1-flashticket/REVIEW-2.md`. Theo tóm tắt cuối lượt của người phản biện (`results/T-064/codex/R2-ketqua.md`): gói sửa R1–R4 không có điểm chặn mới; hash và điểm tính độc lập khớp; một điểm mới R5 không chặn (câu STATE "không bản nào hồi quy" sai phạm vi vì V043/V044 giảm AC@1 trên T-062). Người làm: R5 đúng, đã sửa câu trong STATE và điền bảng phản hồi.
  - **Giới hạn của lượt đáp này:** hạn mức phiên gần hết, người làm mới đọc tóm tắt, tiêu đề các mục và R5; chưa đọc từng mục của `REVIEW-2.md`. Không coi là đã soát đủ.
- **Báo cáo theo mục 7 (cuối phiên 3).**
  1. Đã làm: lượt chọn 2 và 3, hồ sơ chọn bản nháp (mục 1–11), chú thích thao tác nền, sửa R1, WHY-85/86, hai lượt phản biện và đáp.
  2. File đổi: `src/m1_ft/thanh_phan/h1_canh.py`; `docs/WHY.md`; `results/T-064/`; bảng phản hồi cuối `REVIEW.md` và `REVIEW-2.md`; LOG này; dòng T-064 trong STATE.
  3. Kiểm đã chạy: `kiem_luot2.py`, `kiem_luot3.py` (220/220 mỗi lượt, đối chứng mã nguồn trùng); chấm ba tập; người phản biện tính lại độc lập hai lần, khớp.
  4. Còn mở:
     - Task đạt: 47 bản đã chấm tất định; thứ tự §5 trên tập 13 ca (V032 đứng đầu, V041 thay thế có cạnh); cơ chế ca sai Q1–Q6.
     - Câu hỏi nguồn mới trả lời một phần: chưa có đối chứng bỏ quan hệ; H3, H4 chưa có ô lỗi; H8-adapter, H8-log chưa cài; sàn 1 ms và ngưỡng 60 s chưa có căn cứ đo; V032 hơn P7 ở đúng một ca, bằng thành phần thiết kế sau khi xem ca đó.
     - Chưa đạt SPEC: phép dời mốc ±30 s, `cau-hinh-de-xuat.json`, `ban-xuat/chi-muc-ban.json`, `manifest.json`.
     - Chờ Minh: FLASH-HEALTHY; sửa hook thử H3.
- **Bước tiếp theo chính xác:** (0) đọc đủ `REVIEW-2.md` (mục "R1 — kiểm trung gian và tác động", "Báo cáo lượt"), bổ sung bảng phản hồi nếu có điểm chưa đáp; rồi (2)–(5) như dòng "Bước tiếp theo chính xác" ngay trên: bản xuất thử cho T-065 và brief G-c; đối chứng bỏ quan hệ; dời mốc ±30 s; H8-adapter, H8-log, ô H4; manifest.
- **Prompt cho người phản biện:** hai bên đề xuất dừng lượt kiểm này; prompt bàn giao do người phản biện soạn nằm trong `REVIEW-2.md` mục "Prompt bàn giao cho người làm". Lượt soát kế tiếp phát khi có đầu ra mới (đối chứng bỏ quan hệ, hồ sơ chọn bản 2), dựng theo `results/T-064/kiem/dung_brief_phan_bien.py`.
- Lệnh cuối: script ghi đáp phản biện lượt 2 (sửa một câu STATE, điền bảng phản hồi, ghi LOG và checkpoint).

## Phiên 4 — 14/11/2026 (Claude, điều phối tiếp quản từ phiên lịch 15 phút; vai trò: người làm)

- 04:17Z tiếp quản (trạng thái `ket_luot`, không phiên nào đang chạy). Việc: đối chứng bỏ quan hệ (SPEC T-064, hàng "Quan hệ có tác dụng tính toán không?").
- Thêm `src/m1_ft/thanh_phan/dc_bo_quan_he.py` (chỉ đổi `bat_tat` E1/E2/E5 của P7, không chạm thành phần khác); 4 bản V048 (P7), V049 (V002), V050 (V032), V051 (V041) đều là cấu hình bản cha cộng thành phần này; khai trước chấm trong `so-bien-the.jsonl` (04:19:00Z, mã nguồn `38b677a2…`). Thiết kế sau khi xem lượt 1–3, đã khai.
- Lên `exp-obs` `goc-9` (TD-64-10), phát 04:21Z. Kiểm đã làm: hash gói và hash mã nguồn khớp; thành phần được nạp; hai ca đầu V048 chạy, trung_sha đúng. Chưa kiểm: tắt quan hệ có làm P7 ERROR ở ô nào không (chờ lô).
- **Bước tiếp theo chính xác:** khi đủ 52 + 36 `summary.json` (`ssh exp-obs`, `out/dc-dev2-4`, `out/dc-t062-4`): nhận về theo mẫu `kiem/nhan_luot3.sh`; chấm bằng `cham/cham_dev2.py` + `cham_t062_p7.py`; so từng ô cặp (bản cha, bản bỏ quan hệ); ghi `sau_cham`; viết vào `ho-so-chon.md`; sau đó dời mốc ±30 s, H8-adapter, H8-log, ô H4, manifest.
- Lệnh cuối: `ssh exp-obs` phát `chay_bien_the_obs_luot4.sh` hai luồng.

## Phiên tự tiếp nhận 14/11/2026 05:16–05:22Z — Claude (Sonnet 5.5), laptop, điều phối (thay chủ cũ đã dừng)

- Nhận lô lượt 4 (`kiem/nhan_luot4.sh`; gói `1bc349bc…` trùng hai đầu; 88/88 `summary.json` OK, trùng SHA). Chấm bằng `D:/RCA-ext/envs/py312-pin` (máy này thiếu numpy ở Python mặc định): `cham/dc-luot4-tap12.json`, `dc-luot4-tap13.json`, `dc-luot4-t062.json`; so cặp `cham/dc-luot4-so-cha.json`; sổ 4 dòng `sau_cham` vai trò `doi_chung_bo_quan_he_luot4` (`kiem/ghi_so_sau_cham_luot4.py`).
- Kết quả: cả 4 cặp, cả hai tập: AC@1 và K không đổi, AC@3 giảm 2, tổng hạng tăng; ô đổi chủ yếu e9c9679b, 98ea5ba4. Cơ chế và cạnh đóng góp chưa phân xử. Viết `ho-so-chon.md` §12.
- Chưa làm: bảng cặp T-062; tách E1/E2/E5; ghi WHY/NHAT-KY. Phiên B (T-063 thu bù) và C (dời mốc, H8) đang chạy, không làm trùng.
- Bước tiếp: theo dõi `results/T-064/phien-c/TRANG-THAI.json`, `results/T-063/thu3/TRANG-THAI.json`; tích hợp khi xong.
- Lệnh cuối: `ghi_so_sau_cham_luot4.py`.

## Phiên tự tiếp nhận 14/11/2026 06:17–06:25Z — Claude (Sonnet 5.5), laptop, điều phối (lượt dò 15 phút, mã `local_4cce89da`)

- Tiếp quản vì trạng thái `ket_luot`, chủ cũ `local_f86997b1` không chạy. Kiểm: phiên B (T-063 thu bù) đang chạy, bắt đầu thu 07:35Z; phiên C (T-064 dời mốc, H8) idle, lô exp-obs dời mốc V052–V059 đang chạy (ngừng phát 07:25Z, trạng thái 05:55Z).
- Việc này chỉ ghi mục LOG. Không phát lô, không gọi Codex, không đọc hạn mức; không làm trùng B, C, Codex L5.
- Chưa làm: bảng cặp T-062, tách E1/E2/E5, WHY/NHAT-KY lượt 4; chờ đầu ra B, C để tích hợp.
- **Bước tiếp theo chính xác:** sau ~07:30Z đọc `results/T-064/phien-c/TRANG-THAI.json` và `results/T-063/thu3/TRANG-THAI.json`; nhận, kiểm, chấm đầu ra; tích hợp, phản biện Codex, M4.

## Phiên tự tiếp nhận 14/11/2026 07:33–07:40Z — Claude (Sonnet 5.5), laptop, điều phối (mã `local_3d9b081d`)

- Tiếp quản (trạng thái `ket_luot`, không phiên chủ nào chạy). Phiên C xong phần dời mốc ±30 s, H8-adapter, H8-log (`results/T-064/phien-c/BAN-GIAO-C.md`, `lo_exp_obs: xong`); phiên B đang thu T-063 trên exp-obs tới ~10:35Z (không phát lô trùng).
- Đã chép WHY-(a)(b)(c) của phiên C vào `docs/WHY.md` thành WHY-87, 88, 89 (nguyên văn `de-xuat-WHY.md`), trước khi dùng kết quả trong hồ sơ chọn.
- Chưa làm: đưa kết quả C vào `ho-so-chon.md`; quyết §8 của bàn giao C (H8-log-chuoi đưa vào hồ sơ hay không; chạy thêm d ∈ {−60, −15, +15} cần exp-obs rảnh sau đợt thu B; docstring `h8_adapter.py`); manifest; phản biện Codex; M4.
- **Bước tiếp theo chính xác:** sau ~10:35Z đọc `results/T-063/thu3/TRANG-THAI.json`; nhận đầu ra B; trong lúc chờ, viết phần dời mốc và H8 vào `ho-so-chon.md` theo `BAN-GIAO-C.md` §3–5, §8.
- Lệnh cuối: nối WHY-87–89 vào `docs/WHY.md`.

## Phiên 5 — 14/11/2026 (Claude Opus 5.5, laptop, điều phối chính; vai trò: người làm T-064; mã `local_feddcc0c`)

- 11:33Z tiếp quản do Minh mở (qua phiên `ed8b9c01`); chủ cũ `local_f1f8d7ba` ở `ket_luot`, không lệnh nền. Ghi `chu`/`dang_lam` vào `DIEU-PHOI-TRANG-THAI.json`.
- **Tự soát phần gốc trước khi đọc kết luận REVIEW-3** (hồ sơ chọn §12, §13; mã `dc_bo_quan_he.py`, `src/m1/chuoi.py`, `xep_hang.py`; số `phien-c/cham/doi-moc.json`):
  - S1. Lõi P7 khi E1 = `tat`, E2 = `tat`, E5 = False, E6 = `a`: không còn phép tính dùng cạnh trong xếp hạng (PageRank chỉ ở E6b; E7 chỉ dựng vùng báo cáo). Vì vậy V048 (P7), V049 (V002), V050 (V032) là bỏ quan hệ trọn vẹn (H8s1, H5b không đọc cạnh). **V051 (V041 + DC) thì không**: H1c vẫn lấy cặp span cha–con khác chủ, chấm cạnh, chèn vào danh sách chung; bộ chấm chiếu cạnh về nút. §12 gộp cả bốn cặp thành "quan hệ có tác dụng", chưa tách V051.
  - S2. §13 viết "lợi thế của V032 ở PAUSE-PAYMENT mất ở +30". Số: ở +30, V032 xếp payment hạng 3, P7 vẫn vắng; V032 hơn P7 ở AC@3 (8 so 7) và tổng hạng cắt (13 so 16). Chỉ mất hạng 1. Câu cần thu hẹp.
  - S3. §13 không nêu K: ở d = −30 và +30, K của P7 và V032 tăng 4 → 5 (83073ed1 đổi sang CAUSE_FOUND); V041 giữ 3.
  - S4. WHY-87–89 chép vào `docs/WHY.md` 07:40Z, sau khi phiên C đã có kết quả; tiêu đề không ghi "ghi muộn".
- **Đáp REVIEW-3** (sau tự soát): R6, R7, R8 đúng; thêm N1 (K tăng 4 → 5 ở ±30 của P7, V032). Bảng phản hồi cuối `REVIEW-3.md`, cột Minh quyết để trống. Sửa trong quyền: WHY-94 (đính chính thời điểm WHY-87–89), hồ sơ chọn §14 (đính chính §12, §13), đối chứng thật cho R6 (V066, V067).
- **Câu hỏi cho Minh (11:45Z, gửi qua phiên `local_370653c4`):** ca H4 `659a9dfb1ab0` có tính `broker` là đáp đúng ở bảng nút không. Đề xuất A = {booking-service, broker} theo T-059 `label_rules` "Chấm cạnh" (2); phương án B = {booking-service} theo khai trước. Ca này chưa chấm cho tới khi có trả lời.
- **Tập chọn dev bản 3 — khai trước khi chấm (WHY-95):** `results/T-064/tap-chon-dev3-17.json` (17 ca) = 13 ca cũ (eb48d6b3, 4af494a5, 19b17e22, e9c9679b, 729604d2, 6949870c, fb1cf0e9, 5fb8208f, 83073ed1, 60166807, 98ea5ba4, 46aab4be, f20b0ca5) + 86dea661, 659a9dfb1ab0, 1e5a3dc5, ebd5ef38. Tập độ nhạy `tap-dev3-19-do-nhay.json` thêm 7d1ee32f, 0a45b2e0 (lần thu thứ hai của ô cũ trên bản 3, không dùng chọn).
- **Lô 5 (WHY-96).** Sổ 17 dòng ghi 11:43:50Z trước khi chạy (`kiem/ghi_so_luot5.py`): V066–V072 (đối chứng R6, tổ hợp H3/H4/H8a), V073–V081 (dời mốc −60, −15, +15), một dòng `chay_them` cho 32 bản hiện hành trên 6 ca thu bù 3. Mã nguồn `b0f79a4d…` (không đổi mã). `exp-obs` `goc-12` (TD-64-14); phát 11:47Z, sắp lại 12:00Z: 673 cặp (36 bản × ebd5ef38; 39 bản × 5 ca thu bù 3; V066–V072 × 22 ca cũ; 288 cặp dời mốc), xuất bù 13 × 3 + 6 × 5 gói quanh t′.
  - Tuyến laptop bị bỏ theo điều kiện khai trước: 5/5 cặp lệch byte ở chữ số cuối số thực so với `exp-obs` (`kiem/luot5/laptop-kiem/KET-QUA.md`). Ổ D còn ~4,8 GB; lần giải gói đầu làm đầy ổ D trong chốc lát, đã xóa ngay thư mục tạm của mình (`D:/RCA-ext/m1ft-l5`); không file repo nào hỏng (kiểm `git status`, đuôi sổ, REVIEW-3).
  - **Luật 21 (lỗi giữa chừng):** một cặp lỗi chỉ ghi dòng lỗi, luồng chạy tiếp; chạy lại bỏ qua cặp có `summary.json`. Lỗi ở 10% (~25 phút): đọc dòng lỗi; lỗi dữ liệu một ca → cách ly ca, chạy tiếp; lỗi mã chung → `touch ~/l5/DUNG`, sửa trong `src/m1_ft`, ghi sổ mã mới, chạy lại cả lô (~4 giờ máy). Ở 50%: như trên, phần xong của mã cũ giữ làm lịch sử. Ở 99%: chỉ chạy lại cặp thiếu (vài phút). Lỗi hạ tầng (mất kết nối, máy khởi động lại): phát lại cùng lệnh, cặp đã xong được bỏ qua. Lỗi `ValueError: Multiple runtime series…` ở bản không có H8-adapter trên ebd5ef38 là kỳ vọng (= P7 ERROR, tính trượt), không phải lỗi lô. Quét suy biến đã biết trên dev: bản không H8a ở ebd5ef38 (đã biết); `IQR_N` phẳng (C3, đã biết, không chặn).
- 12:08Z kiểm gói xuất bù quanh t′ (`kiem/luot5/kiem_bo_sung_l5.py`, chép từ bản phiên C; → `kiem/luot5/kiem-bo-sung-l5.json`): 69/69 (ca, d), 669.444 điểm chung với gói gốc, 0 lệch, 0 chuỗi một bên, 0 lỗi khúc, `t` của gói = t + d ở 69/69.
- Bộ chấm mới `cham/cham_dev3.py` (cùng `src/m1_ft/cham.py`): tái lập đúng số cũ trên tập 13 ca và T-062 khi dùng `dap-an-dev2.json` (P7 5/7/15/K4; V032 6/8/10/K4; V041 6/8/11/K3, cạnh 3/3; V061 = V032).
- T-063 (người làm Claude): dựng `results/T-063/o-dev-bo-sung.json` (`dong-goi/tao_o_dev_bo_sung_json.py`, 10 ô) và `results/T-063/manifest.json` (`dong-goi/tao_manifest_t063.py`, 186 file + 5 file tổng thư mục con; `sha256sum -c` của `thu2/`, `thu3/thu/` đạt). Lượt Codex phản biện thu bù 3 chưa phát: L7 (Codex app) đã dừng 11:58Z vì hạn mức Codex sắp hết.
- **Quyết định của Minh trong phiên (nhận 12:10Z qua phiên `local_370653c4`):** ca H4 `659a9dfb1ab0` — "A, báo kèm điểm B". Ghi `docs/DECISIONS.md` (mục 14/11 "Tập chấp nhận ô H4…", nguyên văn), WHY-97, `dap-an-dev3.json` (A, chính) và `dap-an-dev3-B.json` (B, độ nhạy) lúc 12:10:59Z, trước khi chấm biến thể. Sửa sau khai trước (`thu3/KE-HOACH.md` §2); người làm đã thấy đầu ra P7 ca này.

### Phiên 5 — nhận và chấm phần d = 0 lô 5 (15:12–15:50Z)
- Phần d = 0 xong 15:12:51Z (A 212, B 186 dòng; 352 OK trùng SHA, 31 ValueError, 2 BO-QUA vì đã có summary). Nhận 15:34Z: `kiem/nhan-luot5/l5-d0.tgz` (hash khớp hai đầu, `kiem/nhan-luot5/NHAN-D0.sha256`), 354 method-output. 31 lỗi đều là ca ebd5ef38 (RECREATE-PAY), bản không H8-adapter, "Multiple runtime series…" — đúng khai trước WHY-96; ghi `loi-chay.json` (trượt theo tiêu chí §2).
- Chấm (môi trường ghim): spec `cham/spec-dev3-d0.json`; kết quả `cham/chon-dev3-d0-A.json` (đáp án A), `cham/chon-dev3-d0-B.json` (B); luật giữ/bỏ `cham/giu-bo-dev3-d0-A.json`, `-B.json`; bản in `.txt` cùng tên. **A và B cho kết quả giống hệt** (mọi bản xếp booking-service hạng 1 ở ca H4 659a9dfb1ab0).
- Quan sát (tập chọn 17 ca, `/ban/<bản>/chon/tong`): P7 AC@1 7, AC@3 9, tổng hạng 23, K 5. Đứng đầu §5: V061 (H5b+H8a) 9/11/13 K5; V068/V069/V070 (thêm H3, H4) trùng số V061; V071 (V041+H8a) 9/11/14 K4, cạnh top3 3/4 ô; V072 (V071+H3+H4) 9/11/13,5 K4 nhưng cạnh top3 0. T-062: mọi ứng viên không xấu đi; bản có H8s1 K 4→1.
- H3, H4: KHONG_TAC_DUNG cả phép 1 và phép 2. Lý do quan sát: ca POOL-EVENT (86dea661) và CONSUMER (659a9dfb1ab0) đã hạng 1 ở P7 và mọi bản; tập dev không phân biệt được tác dụng — không là bằng chứng có hay không có lợi.
- H8a: toàn bộ lợi (AC@1 +1, hạng −5) đến từ một ca ebd5ef38 (lỗi chạy → hạng 1).
- Cơ chế V072 mất cạnh (ca 4af494a5, 6949870c, 5fb8208f): H3 thêm kênh `metric|event-service_pool-used`, `pool-wait` lớp `khong_lan` có cờ ở bên gọi; `h1_canh.py` CanhDinhVi coi đó là bằng chứng riêng bên gọi → `dinh_vi=phia_goi`, `co=0` (cạnh event-service→event_db hạng 2 → 20). Đây đúng điều kiện thất bại đã ghi trong docstring H1 và lý do của tham số `bo_kenh_dinh_vi` (mặc định rỗng; V071/V072 không đặt). Ứng viên sửa (chưa kiểm): đặt `bo_kenh_dinh_vi` = tên kênh pool khi gộp H1c với H3.
- Thiếu tổ hợp: H5b+H8s1+H8a (V066+H8a, không H1c) chưa chạy; đây là bản §5 có thể đứng đầu (giả định chưa kiểm: H8s1 và H8a tác động trên ca khác nhau nên cộng được). Đề xuất trình Minh.
- Đang chạy: phần dời mốc lô 5 trên exp-obs (A 228/355, B 205/318 lúc 15:33Z); Codex R4 phản biện thu bù 3 T-063 (`results/T-063/codex/R4-*`, bắt đầu 15:33:36Z).
- 15:46Z Minh duyệt chạy V082 (H5b+H8s1+H8a) trong chat: "chạy thêm tổ hợp H5b+H8s1+H8a mất khoảng 40 60 phút ? nếu vậy thì duyệt ?". Ghi sổ trước khi chạy (`so-bien-the.jsonl` dòng 180, 15:46:27Z, `thiet_ke_sau_khi_xem_tap_chon: true`); cấu hình `bien-the/V082-V066+H8a/cau-hinh.json` (hash khớp bản trên exp-obs). Quét suy biến: ba thành phần đều đã chạy trên đủ 28 ca (H8a là thành phần duy nhất chạy được ebd5ef38). Phát luồng C 15:47:08Z (`kiem/luot5/viec-obs-C-V082.txt`, 28 cặp d = 0, setsid; luật 21 như lô 5: cặp lỗi chỉ ghi dòng, chạy lại bỏ qua cặp đã có summary). Chạy song song với hai luồng dời mốc nên cả ba chậm hơn.
- 16:12Z V082 xong (28/28 trùng SHA, `l5-V082.tgz` hash khớp hai đầu, ghi thêm vào `kiem/nhan-luot5/NHAN-D0.sha256`). Chấm: `cham/spec-dev3-d0-v082.json` → `chon-dev3-d0-v082-{A,B}.json`, `giu-bo-dev3-d0-v082-{A,B}.json` (bản trước giữ nguyên). `giu_bo_dev3.py` thêm 3 cặp phép 2 quanh V082 (ghi chú trong file). A và B giống hệt.
- Quan sát (`/ban/V082-V066+H8a/chon/tong`): 9/11/13, K 4; T-062 không xấu đi, K 4→1. §5 đứng đầu: V082 > V061 (K 5) > V068–V070 (trùng V061, thêm thành phần) > V072 > V071 (tổng hạng 14, cạnh top3 3/4). Phép 2 quanh V082: H8a GIU l1, H8s1 GIU l2 (K −1), H1c GIU l3 (X xấu đi: hạng 13→14; cạnh 3/4 ô top3).
- Diễn giải: theo §5 đã khóa (xếp hạng nút trước K, trước bảng cạnh) bản chọn là V082 (H5b + H8s1 + H8a, không đầu ra cạnh). V071 = V082 + H1c là phương án có đầu ra cạnh, kém 0,5+0,5 hạng ở hai ca (CPU-BOOK-2, HTTP5-EVENT-FLASH hòa nhóm). Chênh lệch giữa các bản đầu bảng là 1 ca; V082 được thiết kế sau khi xem điểm dev nên số dev lạc quan. Chờ Minh: chọn V082 hay V071; chạy dời mốc cho bản chọn.
- 16:1xZ Minh chọn bản cuối "V082" (giữa 16:12:41Z và 16:16:41Z). Ghi: DECISIONS mục 14/11 "Bản đề xuất cuối M1-FlashTicket (T-064): V082"; WHY-98; `cau-hinh-de-xuat.json`; `ban-xuat/chi-muc-ban.json` bản 2 (P7 khoa_P7, V082 de_xuat, V071 thay_the; 28 ca mỗi bản; P7 ebd5ef38 lỗi chạy), dựng bằng `ban-xuat/dung_chi_muc.py` bản 2; bản tạm cũ giữ `chi-muc-ban-tam-1.json` + `dung_chi_muc_tam1.py`. Hồ sơ chọn §15 (quan sát/suy luận/ứng viên/giới hạn/câu hỏi mở). Chưa lập manifest T-064 (chờ phần dời mốc).
- Đề xuất chờ Minh duyệt (luật 8, lượt > 1 giờ): dời mốc V082, d ∈ {−60, −30, −15, +15, +30} × 28 ca = 140 cặp trên exp-obs, ~1–1,5 giờ khi chạy thêm luồng. Gói bổ sung: d −60/−15/+15 có sẵn 19 ca (`out/l5-bo-sung-dt`); d ±30 có sẵn 6 ca dev3, 13 ca dev2 dùng gói phiên C (`out/pc-bo-sung-dt/d±30/<ca>`, liên kết vào `l5-bo-sung-dt`); T-062 dùng gói gốc + `--bo-sung-t-goc`. Luật 21: lỗi mới ở 10 %/50 %/99 %: cặp lỗi chỉ ghi dòng, luồng chạy tiếp; chạy lại chỉ cặp thiếu summary (bỏ qua cặp đã có), mất tối đa thời gian của các cặp lỗi; lỗi nguồn/máy (STOP, hết đĩa) dừng ở ranh giới cặp, chạy lại phần còn lại. Quét suy biến: chạy thử 1 cặp dev2 d = +30 trước khi phát (gói liên kết, bộ đệm đầu vào `l5-dem`).
- 16:29:54Z Minh duyệt dời mốc V082 ("Duyệt"); ghi sổ `chay_them` trước khi chạy. Liên kết 26 gói ±30 dev2 của phiên C vào `out/l5-bo-sung-dt`. Chạy thử 1 cặp (V082 d=+30 dev2 19b17e22): trùng SHA, bộ đệm đầu vào tự dựng. Phát 139 cặp còn lại, 2 luồng D1/D2 lúc 16:31:47Z (`kiem/luot5/viec-obs-V082-dm-{1,2}.txt`).
- 16:33:05Z Phát Codex L8 cho T-065 (G-c kiểm cuối trên chỉ mục bản 2: p7/V082/V071, 28 ca), brief `results/T-065/codex/L8-brief.md`, gpt-6.1-sol max; Codex là người làm T-065. Phản biện cuối T-064 phát sau khi L8 và dời mốc V082 xong (một Codex CLI mỗi lúc).
- Ghi chú: sau khi L8 đã nhận brief qua stdin, điều phối sửa dòng tiêu đề `L8-brief.md` "~16:40Z" → "16:33Z" (chỉ mốc giờ). Bản Codex nhận nằm nguyên văn trong `results/T-065/codex/L8-lan1.log`.
- 16:56Z Codex L8 (T-065) dừng G-c đúng chỗ: `cau_hinh_sha256` của V082 trong chỉ mục và `cau-hinh-de-xuat.json` là hash **byte file** (01a64b60…), còn 28 đầu ra ghi `sha_cau_hinh` (JSON chuẩn hóa, 451a8437…). Nguyên nhân: điều phối tự tính hash bằng hashlib khi ghi sổ dòng 180, không dùng `ft.sha_cau_hinh` như `kiem/ghi_so_luot5.py`. V071 và các bản khác không lỗi. Sửa (không chạy lại, không đổi cấu hình/đầu ra): sổ thêm dòng `dinh_chinh` 16:57:20Z; `ban-xuat/dung_chi_muc.py` tính hash bằng `ft.sha_cau_hinh`, ghi thêm `cau_hinh_file_sha256`, kiểm mọi đầu ra của bản trùng `cau_hinh_sha256` và `ma_nguon_sha256` (56/56 đạt); dựng lại `chi-muc-ban.json` (bản lỗi giữ ở `chi-muc-ban-2-loi-hash.json`); `cau-hinh-de-xuat.json` sửa tương tự (bản lỗi giữ ở `cau-hinh-de-xuat-loi-hash.json`).
- 16:58Z Phát Codex L8b (tiếp phiên L8 `01a1dae7…`, brief `results/T-065/codex/L8b-brief.md`) để làm tiếp G-c trên chỉ mục đã sửa.
- 17:48Z Codex L8b xong (16:58:15–17:48:07Z, rc 0): G-c nối bản cuối V082, đạt kiểm dữ liệu/API (84 slot, 18 trang API, 33 mẫu liên kết; báo cáo `results/T-065/kiem/006-gc-cuoi/BAO-CAO.md`), hai dashboard mới `t065-l8b-rca`, `t065-l8b-phat-lai`, giữ bản cũ. Còn: bấm/ảnh Chrome trên hai UID mới (brief app `results/T-065/codex/L8b-app-brief.md`, Minh chạy bằng Codex app) và Claude kiểm lại L6–L8b (prompt `results/T-065/prompt-ban-giao.md`). Dời mốc lúc 17:48Z: A 336/355, B 309/318, D1 38/70, D2 46/69, chưa có lỗi.
- 18:29Z Bốn luồng dời mốc xong (A 310 OK/31 lỗi, B 291/15, D1 70/0, D2 69/0; không thiếu gói, mọi cặp trùng SHA). Nhận `kiem/nhan-luot5/l5-dm.tgz` (hash khớp hai đầu) + log cuối; ghi 15 `loi-chay.json` (ebd5ef38, d ≠ 0). Chấm `cham/spec-dev3-doi-moc.json` → `doi-moc-dev3-{A,B}.json/.txt` (A = B). Hồ sơ chọn §16: V082 không kém P7 ở mọi d; +30 s là điểm yếu chung.
- 18:34Z Lập `results/T-064/manifest.json` (7.585 file, kèm hash ngoài và src/m1_ft; script `kiem/tao_manifest_t064.py`, 0 lệch). Dựng brief phản biện cuối `codex/R4-brief.md` (script `kiem/dung_brief_r4.py`; Prompt chung + "Soát kết quả" nguyên văn, chỉ thay thông tin trung tính; ghi REVIEW-4.md). Chưa phát: chờ Minh xác nhận không có Codex app đang chạy.
- 15/11 01:12Z Minh: "codex đã làm G-c, có thể sang phiên codex khác, điều phối phản biện liên tục để sang M4". Phát Codex R4 (phản biện cuối T-064, `codex/R4-brief.md`); gửi phiên Claude phản biện T-065 (`local_d237ec54`) prompt `results/T-065/prompt-ban-giao.md`, quyền ghi REVIEW-3.md T-065.
- 01:15Z Tự soát trước khi đọc REVIEW-4 (người làm, phần thay đổi sau REVIEW-3):
  - S5 — §5 thứ tự "(1) xếp hạng nút trước (2) K" vẫn ghi "đề xuất của Claude… để Minh xác nhận" (`tieu-chi-chon.md` §5; DECISIONS dòng "Chưa có lời Minh riêng… thứ tự ưu tiên khi nhiều bản cùng đạt"). Với V082 so V061 thứ tự này không đổi kết quả (V082 không kém ở cả hai); với V082 so V071 quyết định nằm ở (1) trước (3) bảng cạnh. Minh chọn V082 khi được trình rõ đánh đổi này, nhưng chưa có lời xác nhận quy tắc chung. Đưa vào câu hỏi M4.
  - S6 — sổ dòng 180 ghi sai quy ước hash cấu hình (đã đính chính 16:57Z; chỉ mục và cấu hình đề xuất dựng lại; 56/56 đầu ra khớp).
  - S7 — các mốc giờ duyệt từng ghi ước lượng sai (T-063 "~16:05Z", DECISIONS "~16:20Z"); đã đính chính bằng mốc file. Bài học: ghi mốc từ lệnh `date`/file, không ước lượng.
  - S8 — hai nhận định cơ chế trong §15/§16 vẫn **chưa kiểm** mức kênh: H8s1 làm CPU-BOOK-2 tụt (kênh cụ thể), giải thích cửa sổ N ở +30 s. Không dùng làm căn cứ chọn.
  - S9 — dòng T-064 trong `docs/STATE.md` chưa cập nhật từ trước lô 5; cập nhật ở M4.
- 01:39Z Codex R4 xong (01:12:14–01:39:17Z), `REVIEW-4.md`: R9 CHẶN (H5b nhận "chết im" sai ở ebd5ef38 do lookback của `query_range`; 7 bản ở d = 0 và V082 ở 4 mốc d ≠ 0), R10 KHÔNG CHẶN (ca 1e5a3dc5 chưa có chú thích/cơ chế); R6–R8 đạt; chưa đề xuất dừng. Người làm tự kiểm: R9 đúng — và là bỏ sót của người làm (WHY-93 đã nêu điều kiện thất bại, §15/WHY-98 không nhắc). R10 đúng. Điền bảng phản hồi, để trống "Minh quyết". Đề xuất đường sửa R9 (chỉ đọc trước, rồi chạy lại đúng slot đổi) chờ Minh.
- 01:44Z R9 — phép kiểm chỉ đọc trên Prometheus exp-obs (`results/T-064/kiem/r9/`), 149 gói bổ sung (9 gói T-062 không có kênh live-down):
  - Lượt 1 (`so_live_down.py` → `so-live-down.json`): biểu thức `max_over_time(httpcheck_error[15s])` làm mất "chết im" ở cả PAUSE-PAYMENT 46aab4be (ca mất phản hồi thật). Mẫu thô: khi request treo, đầu dò chỉ ghi lỗi mỗi ~30 s (timeout 30 s, duration ≈ 30.000 ms) và không có phản hồi nào sau t; ở RECREATE-PAY lỗi t+3…t+43 rồi có phản hồi 401 từ t+53. → loại biểu thức này.
  - Lượt 2 (`so_live_down_2.py` → `so-live-down-2.json`): ngữ nghĩa "lần dò mới nhất" (1 nếu lần dò có kết quả gần nhất trước bước là lỗi; 0 nếu là phản hồi; dựng từ mẫu thô). Kết quả: 134/140 gói có live-down không lệch điểm nào; chỉ 6 gói ebd5ef38 (d −60…+30) lệch; "chết im" đổi ở đúng 5 gói ebd5ef38 (d −60, −30, −15, 0, +15), mất chết im; PAUSE-PAYMENT 46aab4be giữ chết im ở mọi mốc.
  - Hệ quả dự kiến (chưa chạy): chỉ các slot ebd5ef38 của bản có H5 chạy được (có H8a) chịu ảnh hưởng: V061, V068–V072, V082 ở d = 0 và V082 ở 5 mốc d ≠ 0 (gồm +30 vì giá trị kênh đổi) = 12 cặp. Đề xuất sửa chờ Minh.
- 02:04Z Codex L9-dap (T-065 người làm) xong (01:40:58–02:03:47Z): S1, S4 đúng; S2, S3 đúng một phần; S1 vẫn CHẶN, gói sửa (hash dự kiến, hoàn tác, chi phí) trình ở LOG T-065 dòng ~1693; prompt cho Claude kiểm lại ở LOG T-065 dòng ~1848. Điều phối giữ lượt Claude kiểm lại tới khi Minh quyết S1 (tránh hai lượt).
- 15/11 ~03:3xZ Minh duyệt R9, R10 (T-064) và S1 (T-065): "Duyệt cả ba" (chuyển qua phiên `local_370653c4`; ghi DECISIONS mục 15/11 "Sửa R9, R10…"). Thực hiện:
  - S1: phát Codex L10 (T-065, `results/T-065/codex/L10-brief.md`, 03:34:31Z), chỉ S1.
  - R9: WHY-99 ghi trước khi chạy. Bộ xuất `kiem/r9/xuat_live_down_moi.py` → 6 gói mới `exp-obs:/opt/rca-m1ft/out/r9-bo-sung/d<d>/ebd5ef38/` (chỉ bundle live-down đổi; điểm lệch 13–19, khớp phép kiểm chỉ đọc; hash ở `kiem/r9/xuat-live-down-moi.json`). Runner `kiem/r9/r9_chay.sh` (chép `l5_chay.sh`, đổi O và đường gói), việc `kiem/r9/viec-r9.txt` (12 cặp), đầu ra `/opt/rca-m1ft/out/r9`. Bộ chấm `cham/cham_dev3.py` thêm khóa spec `goc_uu_tien` (bản trước `cham_dev3_truoc_r9.py`; kiểm hồi quy: không khai khóa thì đầu ra giống từng byte `chon-dev3-d0-v082-A.json`).
  - R10: `phan-tich/ghi-chu-co-che-dev2.md` Q7 và `chu-thich-thao-tac-nen.md` §5 (ca 1e5a3dc5, đối chiếu 7d1ee32f; nguyên nhân CPU Payment chưa phân xử, nêu khả năng và dữ liệu cần).
  - Tự phát hiện: §15 ghi "kênh cụ thể bị giảm chưa kiểm" cho H8s1 ở CPU-BOOK-2, nhưng Q6 (`ghi-chu-co-che-dev2.md`, 13/11) đã lần đủ (hai đơn vị `Session.persist`, `saveAll` của Booking bị sàn 1 ms bỏ). Đính chính ở §17.
- 03:49Z Codex L10 (T-065 S1) xong (03:34:31–03:48:16Z): mục lục trỏ hai UID L8b, hai L4 chuyển Lưu trữ giữ byte/UID; hash trước/sau đúng pin; API đạt; manifest T-065 9.197 file 0 lệch. Thiếu ảnh Mục lục và bấm link UI (CLI không có trình duyệt, API render HTTP 500) — cần Minh mở `/d/t065-l5-muc-luc` trong app. Báo cáo `results/T-065/kiem/008-s1/BAO-CAO.md`.
- 03:49Z R9 chạy lại xong 12/12 (trùng SHA). Nhận `kiem/nhan-r9/r9.tgz` (hash khớp hai đầu, `NHAN-R9.sha256`; gồm đầu ra `r9/` và 6 gói `r9-bo-sung/`). Chấm lại: `cham/spec-dev3-d0-v082-r9.json`, `cham/spec-dev3-doi-moc-r9.json` → `chon-dev3-d0-v082-r9-{A,B}`, `giu-bo-dev3-d0-v082-r9-{A,B}`, `doi-moc-dev3-r9-{A,B}`: mọi bản in `.txt` giống hệt bản trước; 26 slot dùng R9, không slot nào đổi chỉ số chấm. Chỉ mục xuất bản 3 (`e83e1696…`; bản 2 giữ `chi-muc-ban-2.json`), cấu hình đề xuất cập nhật (bản trước `cau-hinh-de-xuat-2.json`), hồ sơ chọn §17 (R9, R10, đính chính §15 về Q6). T-065 cần xuất lại 2 slot ebd5ef38 (V082, V071) để khớp hash chỉ mục bản 3.
- 03:55Z Lập `results/T-064/manifest-2.json` (7.662 file, ghim manifest.json cũ; 0 lệch; generator sửa để ghim bản trước). Dựng `codex/R5-brief.md` (`kiem/dung_brief_r5.py`; Prompt chung + "Kiểm lại phản hồi và sửa" nguyên văn) và phát Codex R5 (gpt-6.1-sol max), ghi REVIEW-5.md.
- 03:55:40Z Lập lại `manifest-2.json` (sau khi sửa mốc giờ tiêu đề §17 trong ho-so-chon.md khoảng 03:55:30Z, tức sau khi R5 đã bắt đầu 03:55:15Z; bản kê mới có cả R5-brief.md). Nếu R5 đọc bản kê trước 03:55:40Z có thể thấy ho-so-chon.md lệch — do điều phối, không phải lỗi dữ liệu.
- 04:55Z Minh chụp 4 ảnh Mục lục (phiên `ed8b9c01` chép vào `results/T-065/kiem/009-s1-anh-minh/`) và giao "triển khai phần còn lại giúp tôi". Mời phiên Claude phản biện T-065 (`local_d237ec54`) kiểm lại S1, quyền ghi REVIEW-4.md T-065. Soạn `results/T-065/codex/L11-brief.md` (xuất lại 2 slot ebd5ef38 theo chỉ mục bản 3), phát sau khi Codex R5 xong.
- 04:12Z Codex R5 (03:55:15–04:12:28Z) ghi `REVIEW-5.md` đầy đủ (kết luận, đối chiếu, prompt bàn giao, bảng phản hồi) rồi chạm hạn mức Codex ("try again at Nov 18th, 2026 9:17 AM"; log có lỗi token_revoked lúc 04:08:48Z). Kết luận R5: R9 gỡ chặn, R10 đạt; không lỗi khoa học mới; R11 KHÔNG CHẶN (manifest-2 ghim log R5 trước khi log ổn định); đề xuất dừng vòng phản biện này. Điều phối dừng bộ gọi `goi_codex.py` đang chờ hạn mức tới 18/11 (TaskStop 04:55Z) để không tự `resume` một lượt đã xong. Điền bảng phản hồi R11 (đồng ý; manifest-3 khi bàn giao M4). Codex hết hạn mức: L11 (T-065 xuất lại 2 slot) chưa phát.
- 04:57Z Minh: "Đã đổi, phát L11". Phát Codex L11 (T-065, `results/T-065/codex/L11-brief.md`, gpt-6.1-sol max).
- 05:00Z T-065 REVIEW-4 (Claude, `local_d237ec54`): S1 đạt, 0 CHẶN, đề xuất dừng phần S1; T1 (Mục lục trỏ chỉ mục bản 3 khi dashboard dựng từ bản 2 — xử lý trong L11), T2 (ở ebd5ef38 cờ và khóa có đổi: kenh_co 65→64, khóa payment đổi; chỉ thứ tự/tie_group giữ), T3 (chưa bấm link từ Mục lục — chấp nhận giới hạn). Người làm T-064 tự kiểm T2: đúng; thêm đính chính cuối §17 ho-so-chon.md. Brief L11 đã phát với câu "hạng và cờ không đổi" — brief yêu cầu kiểm lại; điểm này sẽ chuyển cho lượt kiểm L11.
- 05:09Z Codex L11 (04:57:38–05:09:16Z) dừng trước triển khai vì brief ghi sai "cờ không đổi" (thực tế 65→64 ở hai slot ebd5ef38); chưa đổi exp-obs; manifest T-065 9.218 file 0 lệch. Lỗi mô tả của điều phối, phạm vi duyệt không đổi. Phát L11b (tiếp phiên L11, brief `results/T-065/codex/L11b-brief.md` kèm đính chính, T1/T2 của REVIEW-4 T-065, ghim kiem/009).
  - Ghi chú: sau khi L11b nhận brief (05:09:44Z), điều phối sửa riêng mốc giờ ở dòng tiêu đề `L11b-brief.md` (05:10Z → 05:09Z); bản Codex nhận nằm nguyên văn trong `results/T-065/codex/L11b-lan1.log`.
- 05:26Z Codex L11b xong (05:09:44–05:26:14Z): chỉ mục bản 3 lên dashboard; hai slot ebd5ef38 64 cờ, khóa mới, H5b rỗng; 82 slot khác giữ byte; 84 slot, 18 trang API đạt; manifest T-065 11.649 file 0 lệch; ảnh 009 đã ghim. Thiếu ảnh bản 3 (Codex không được điều khiển Chrome; hướng dẫn `results/T-065/kiem/010-chi-muc-3/l11b/ANH-CAN-CHUP.md`). Mời phiên Claude phản biện T-065 kiểm L11/L11b, quyền ghi REVIEW-5.md T-065.
- 05:31Z T-065 REVIEW-5 (Claude): 0 CHẶN; T1, T2 đạt; U1 (chưa có ảnh bản 3 — chờ Minh chụp, chỉ cần đối chiếu nhẹ), U2 (BAO-CAO 010 ghi "đính chính L11b của Minh" — brief do điều phối soạn); đề xuất dừng phản biện. T-064 REVIEW-5 (Codex) cũng đề xuất dừng. Sang M4.

### M4 — kết thúc phiên điều phối 5, câu hỏi cho Minh (15/11/2026 05:34Z, `local_feddcc0c`)

**1. Đã làm (phiên 5, 14/11 11:33Z – 15/11 05:34Z).** Đáp REVIEW-3; tập dev bản 3 (17 ca) và đáp án A/B (Minh: "A, báo kèm điểm B"); lô 5 trên exp-obs (đối chứng V066/V067, tổ hợp V068–V072, dời mốc); V082 (Minh duyệt chạy, Minh chọn "V082"); dời mốc V082; chỉ mục xuất bản 2 → 3 và cấu hình đề xuất; R4 Codex (R9 CHẶN, R10) → sửa (Minh "Duyệt cả ba"; WHY-99) → R5 Codex đề xuất dừng. Điều phối T-063 (R4, R7 → manifest-2, R5 đề xuất dừng) và T-065 (L8, L8b, L8c app, L9-dap, L10 S1, L11/L11b chỉ mục bản 3; Claude REVIEW-3/4/5 đề xuất dừng).

**2. Đầu ra chính.** `results/T-064/`: `ho-so-chon.md` §14–17, `cau-hinh-de-xuat.json`, `ban-xuat/chi-muc-ban.json` (bản 3), `cham/` (chấm A/B, giữ/bỏ, dời mốc, bản r9), `kiem/luot5/`, `kiem/r9/`, `kiem/nhan-luot5/`, `kiem/nhan-r9/`, `phan-tich/ghi-chu-co-che-dev2.md` Q7, `chu-thich-thao-tac-nen.md` §5, `so-bien-the.jsonl` (tới dòng đính chính), `manifest-3.json` (7.669 file, 0 lệch, ghim manifest-2). docs: DECISIONS (H4, V082, R9/R10/S1), WHY-94…99. STATE: dòng chiến dịch, T-063, T-064, T-065.

**3. Kiểm đã chạy.** Mọi cặp hai lần trùng SHA; hash gói nhận khớp hai đầu (`NHAN-D0.sha256`, `NHAN-R9.sha256`); hồi quy bộ chấm giống từng byte; chỉ mục bản 3: 56/56 đầu ra khớp hash cấu hình/mã nguồn; manifest-3 0 lệch. Phản biện độc lập: Codex R4, R5 (T-064), R4, R5 (T-063); Claude REVIEW-3…5 (T-065).

**4. Task đạt gì / câu hỏi nguồn / còn mở.**
- Đạt: bản đề xuất M1-FT cuối có bằng chứng trên dev (17 ca + 9 ca T-062 + dời mốc), hồ sơ giữ/bỏ, đối chứng bỏ quan hệ, dashboard nối bản mới (G-c, dữ liệu/API).
- Câu hỏi nguồn trả lời tới đâu: chỉ trên dev; chưa đánh giá giữ ngoài (RQ5 không đóng). V082 thiết kế sau khi xem điểm dev (lạc quan).
- OPEN: H3, H4 chưa phân xử (ô của chúng đã hạng 1 ở P7); nguyên nhân CPU Payment ở hai ca không lỗi bản 3 (Q7); +30 s là điểm yếu chung; T-065 U1 thiếu ảnh bản 3.

**5. Câu hỏi M4 cho Minh (mỗi câu kèm đề xuất của điều phối; Minh quyết).**
1. *Nghiệm thu T-063, T-064, T-065 và dừng các vòng phản biện.* Đề xuất: dừng phản biện cả ba (các bên đều đề xuất dừng); nghiệm thu T-063, T-064 với OPEN ở mục 4; T-065 nghiệm thu khi có ảnh U1 hoặc chấp nhận thiếu ảnh làm giới hạn.
2. *Thứ tự §5 "xếp hạng nút trước K" (tiêu chí ghi là đề xuất của Claude).* Đề xuất: xác nhận làm quy tắc chung. Mặt trái: ưu tiên phát hiện đúng hơn báo nhầm; ở V082 so V061 không đổi kết quả.
3. *Image Event bản 3 trên exp-app (hook H3).* Đề xuất: hoàn tác về `ft-local/event-service:arm64-t062-6b21ed55` bằng `bash ~/t063/thu3/deploy-t063-event.sh ft-local/event-service:arm64-t062-6b21ed55` (`results/T-063/thu3/thay-doi-may.md` T3-05), giữ image bản 3 trong Docker để dựng lại khi cần. Mặt trái: lượt thu H3 sau phải deploy lại (~1 phút).
4. *Khóa SSH `exp-obs:~/rca-dieu-phoi/keys`.* Đề xuất: xóa khi Minh xác nhận chiến dịch không thu thêm. Mặt trái: thu tiếp (vd. ô phân xử H3/H4) phải chép lại.
5. *Lịch `m1ft-tiep-nhan`.* Đề xuất: tắt ngay sau khi Minh trả lời M4.
6. *T-065 S2–S4, R4.* Đề xuất: S2 thêm một câu "V082 vẫn dùng quan hệ E1/E2/E5 bên trong"; S3 giữ OPEN; S4 áp đính chính đã nhận vào báo cáo; R4 xác nhận hồi tố việc xóa folder Grafana `RCA` rỗng.
7. *FLASH-HEALTHY.* Đề xuất: giữ đếm thô trong K như tiêu chí §2, báo nhóm riêng (đang làm vậy).
8. *Biến thể chịu được khởi phát muộn và phân xử H3/H4.* Đề xuất: để ngoài chiến dịch, mở task sau nếu cần.
9. *Chỗ lưu và commit.* `results/T-062`…`T-065` chưa có file nào trong git: 21.356 file, ~8,8 GB (T-062 2,4 GB, T-063 3,0 GB gồm `thu2/` 1,3 GB và `thu3/` 1,0 GB, T-064 1,3 GB, T-065 2,1 GB), 28 file > 50 MB; ổ D còn ~3,8 GB. Đề xuất: commit tài liệu, script, kết quả chấm, chỉ mục, cấu hình và manifest; giữ dữ liệu thô (gói ca, `thu2/`, `thu3/thu*`, `nhan-*`, `dau-ra-*`, `may-*`, `*.tgz`) ngoài git (vd. `D:/RCA-ext/` hoặc lưu trữ ngoài), kèm SHA256SUMS và `.gitignore` theo đường dẫn. Cần Minh chọn nơi lưu trước khi soạn danh sách commit cụ thể. Không gồm các file không thuộc chiến dịch (`results/T-032/…`, `docs/KE-HOACH-GIAI-DOAN-TOI.md`, `docs/techstack/`).

**6. Bước tiếp chính xác.** Sau khi Minh trả lời mục 5: (3) chạy lệnh hoàn tác trên exp-app nếu duyệt, ghi `results/T-063/thu3/thay-doi-may.md`; (4) xóa khóa nếu duyệt; (5) tắt lịch; ghi DECISIONS nguyên văn; cập nhật STATE "xong" cho task được nghiệm thu; soạn danh sách commit theo mục 9 → Minh duyệt → commit và push. Lệnh cuối đã chạy: `py -3 -B results/T-064/kiem/tao_manifest_t064.py` → `manifest-3.json`.
- 06:09Z Minh trả lời M4: "Tôi đồng ý các đề xuất 1–8. T-065 nghiệm thu sau khi lưu ảnh S1 và bổ sung ảnh U1. Mục 9 lưu dữ liệu lớn tại [đường dẫn]; trình danh sách file trước khi commit/push." (kèm 5 ảnh U1). Ghi DECISIONS mục 15/11 "M4 chiến dịch M1-FlashTicket…". Thực hiện:
  - Lưu 5 ảnh U1 nguyên byte vào `results/T-065/kiem/011-u1-anh-minh/` (SHA256SUMS, GHI-CHU.md; hash đầu ra trên ảnh trùng sha256 file nhan-r9 của V082, V071).
  - (3) Hoàn tác Event trên exp-app về `arm64-t062-6b21ed55` 06:12:08–06:12:50Z (health 401, restarts 0); ghi `results/T-063/thu3/thay-doi-may.md` T3-M4.
  - (4) Xóa `exp-obs:~/rca-dieu-phoi/keys/` 06:15:09Z sau khi kiểm bản trùng hash trên laptop; ghi T3-M4b. (`thay-doi-may.md` đổi sau `results/T-063/manifest-2.json` → cần manifest-3 T-063 khi chốt commit.)
  - (6) Phát Codex L12 (T-065: S2, S4, U2, R4/S3, ghim ảnh U1, mục kết thúc task) 06:14:30Z, `results/T-065/codex/L12-brief.md`.
  - (9) Lời Minh còn để "[đường dẫn]" chưa điền — chờ Minh cho đường dẫn lưu dữ liệu lớn trước khi soạn danh sách commit.
- 07:15Z Codex L12 xong (06:14:30–06:37:57Z, `results/T-065/kiem/012-s2-s4-u2/BAO-CAO.md`): S2, S4, U2 xong; R4 ghi xác nhận hồi tố; ảnh U1 đã ghim; 11.684 pin khớp. OPEN: S3, lệch URL ảnh U1 số 01. STATE: T-065 "xong". Tắt lịch `m1ft-tiep-nhan` (Minh: "tắt lịch"). Mục 9 Minh tạm hoãn ("mục 9 tạm hoãn").

### Bàn giao cuối (07:15Z, `local_feddcc0c`; Minh sắp đổi tài khoản Claude)
- Chiến dịch M1-FT: M4 xong trừ mục 9. T-063, T-064, T-065 "xong". Không còn lệnh nền, không còn lượt Codex.
- Còn mở cho phiên sau: (a) mục 9 — Minh cho đường dẫn lưu dữ liệu lớn → lập manifest-3 T-063 (`thu3/thay-doi-may.md` đổi sau manifest-2), soạn danh sách commit (chỉ đường dẫn chiến dịch; không gồm `results/T-032`, `docs/KE-HOACH-GIAI-DOAN-TOI.md`, `docs/techstack/`) → Minh duyệt → commit/push; (b) kéo về laptop gói đầu vào dời mốc trên exp-obs (`/opt/rca-m1ft/out/l5-bo-sung-dt`, `pc-bo-sung-dt`; kiểm `bo-sung-dev2/dev3` đã có bản trùng hash chưa); (c) Minh hỏi giảm dung lượng dự án (~70 GB: `.git` 6 GB, `D:/RCA-ext` 13 GB, `results/T-032`, `T-033`, `T-045`, `T-047`, `T-048`): đo từng thư mục, trình danh sách chuyển ra ngoài/xóa kèm hash; luật 10 giữ mọi lượt chạy → ưu tiên chuyển ra ngoài.
- Câu mồi phiên mới: "Đọc AGENTS.md, làm tiếp task đang mở trong STATE."
