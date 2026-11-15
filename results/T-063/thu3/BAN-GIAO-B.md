# T-063 thu bù 3 — Bàn giao của phiên B

Ghi 14/11/2026 ~11:00Z. Người làm: Claude, phiên B (`local_33bac1e1-ae7b-4f28-8e8d-90e7b195a1de`). Người nhận: phiên điều phối chiến dịch (`local_370653c4…`), phiên C (T-064), Codex (phản biện T-063). Brief: `tasks/T-062-dem-chang-1-4/PHIEN-B-BRIEF.md`.

File này nằm **phía chấm**: có ánh xạ mã mờ ↔ ô và đáp án. Không đặt vào nơi M1 đọc.

## 1. Đã thu và đã xác nhận

Đợt `runner4.py thu --lich lich-3.json` trên `exp-obs`, 07:24:01–10:32:34Z, 6/6 chu kỳ, không sự kiện bất thường trong sổ. Nhận về `results/T-063/thu3/thu/` (`SHA256SUMS`; 5 gói `.tgz` khớp hash nhật ký; sổ 60 dòng, chuỗi hash đúng).

| Mã mờ (sổ) | Mã gói / thư mục trên exp-obs | Ô | Bậc tải | Hậu kiểm khai trước | Sau "Sửa sau" | P7 |
|---|---|---|---|---|---|---|
| `7d1ee32f` | `7d1ee32f` | BINH-THUONG | ×1 | xác nhận | xác nhận | OK, 2 lần trùng |
| `86dea661` | `86dea661` | POOL-EVENT | ×1 | xác nhận | xác nhận | OK, 2 lần trùng |
| `0a45b2e0` | `0a45b2e0` | EVENT-DB-LAT | ×1 | xác nhận | xác nhận | OK, 2 lần trùng |
| `1e5a3dc5` | `1e5a3dc5` | BINH-THUONG-X3 | ×3 | **không** (C0) | xác nhận (Sửa sau 1) | OK, 2 lần trùng |
| `659a9dfb` | **`659a9dfb1ab0`** | CONSUMER-BOOK-SLOW-X3 | ×3 | xác nhận | xác nhận | lần 1 bị bộ chặn rò mã (trùng ngẫu nhiên với spanId, mục 5); lần 2 OK, 2 lần trùng |
| `ebd5ef38` | `ebd5ef38` (và `ebd5ef381d1a`) | RECREATE-PAY | ×1 | **không** (httpcheck) | xác nhận (Sửa sau 2) | lỗi adapter `Multiple runtime series…` cả hai lần (dự kiến) — không có đầu ra P7 |

Kết quả hậu kiểm: `thu3/xac-nhan-ca-3.json` (bản chốt, 4/6), `thu3/xac-nhan-ca-3-sua-sau.json` (6/6). Điều kiện và hai "Sửa sau": `thu3/dieu-kien-xac-nhan-3.md`.

## 2. Ô không đạt và lý do

Theo điều kiện khai trước: BINH-THUONG-X3 (script quên ô này trong C0; điều kiện đã khai đúng) và RECREATE-PAY (điều kiện phục hồi dùng `query_range`, bị lookback 5 phút). Chi tiết và bằng chứng mẫu thô ở `dieu-kien-xac-nhan-3.md` mục "Sửa sau". **Chờ Minh** nhận hai sửa (mục 7).

Ô không thu: CONSUMER-BOOK-SLOW ở ×1 (đợt 2 đã thất bại 3 lần; nguyên nhân đo được: byte broker→Booking ×1 tb 469 B/s < 1 KB/s, `do/do-h4a-tom-tat.json`). Hook làm chậm consumer: không làm, chưa có quyền và không cần vì ×3 đạt.

## 3. Bản đóng băng 3

`results/T-063/dong-bang/dong-bang-3.json` (sha256 `1200ffe0…`), mục "Bản 3" ở `results/T-063/dong-bang.md`. Thay đổi ứng dụng duy nhất: image Event `ft-local/event-service:arm64-t063h3-76b34d5e` (`sha256:01493da5…`) = `6b21ed55` + bản vá `RcaFaults.java` (nhánh `rca/quan-sat-log` commit `e557307`, đã push; `thu3/scripts/h3-pool-event.patch`). Hoàn tác: `bash ~/t063/thu3/deploy-t063-event.sh ft-local/event-service:arm64-t062-6b21ed55` trên `exp-app`. Hiện `exp-app` **vẫn chạy bản 3** (chưa hoàn tác: các ca mới dùng bản này; hoàn tác hay giữ do điều phối quyết).

## 4. Vị trí gói trên exp-obs cho T-064

- Gói ca P7 (như 13 ca cũ): `/opt/flash-ticket-rca/cases/<mã gói>`, `/opt/flash-ticket-rca/outputs/<mã gói>` cho `7d1ee32f`, `86dea661`, `0a45b2e0`, `1e5a3dc5`, `659a9dfb1ab0`. Ca RECREATE-PAY: chỉ `cases/ebd5ef38` (và bản stage lại `cases/ebd5ef381d1a`; khác nhau ở `manifest.json` và `raw-traces.jsonl` vì stage lần hai đọc Tempo sau), không có `outputs/` vì P7 lỗi. Hash từng file: `thay-doi-may.md` T3-15 và mục 8 dưới.
- Gói bổ sung (24 kênh, ±300 s): `/opt/rca-m1ft/bo-sung-dev3/<mã gói>/prometheus-bo-sung.json` + `SHA256SUMS` (6 ca, gồm `ebd5ef38`). Bản sao: `results/T-063/thu3/thu/ca/<mã gói>/` (5 ca) và `exp-obs:~/rca-dieu-phoi/thu3/ca/ebd5ef38/`.
- Bản `.tgz` (cases + outputs): `results/T-063/thu3/thu/ca/<mã gói>.tgz` (5 ca). Ca RECREATE-PAY không đóng `.tgz` vì `safe-export.py` ghim (T-058) đòi `outputs/summary.json`; dữ liệu thô giữ trên `exp-obs`, không chép về laptop khi chưa qua bộ quét bí mật đó.

## 5. Đáp án từng ô mới (để điều phối ghép vào đáp án phía chấm)

Theo khuôn `results/T-064/dap-an-dev2.json`. Tập chấp nhận lấy đúng như khai trong `thu3/KE-HOACH.md` §2 và bổ sung 4 (trước khi thu).

| Mã gói | Ô | root | tập chấp nhận (nút) | Ghi chú |
|---|---|---|---|---|
| `7d1ee32f` | BINH-THUONG | — (ca không lỗi) | — | bản 3, ×1 |
| `86dea661` | POOL-EVENT | node `event-service` | `event-service` | pool.hold 5/5, 600 s |
| `0a45b2e0` | EVENT-DB-LAT | edge `event-service`→`event_db`, kind `data` | `event-service`, `event_db` | như đợt 2 |
| `1e5a3dc5` | BINH-THUONG-X3 | — (ca không lỗi) | — | ×3 suốt chu kỳ |
| `659a9dfb1ab0` | CONSUMER-BOOK-SLOW-X3 | edge `booking-service`→`broker`, kind `message` | `booking-service` (khai trước: "booking-service; cạnh booking-service ↔ broker") | khác quy ước EVENT-DB-LAT (đưa cả đích dữ liệu vào tập nút): điều phối quyết có thêm `broker` theo quy ước đó không, ghi WHY trước khi chấm |
| `ebd5ef38` | RECREATE-PAY | node `payment-service` | `payment-service` | P7 không có đầu ra; phiên C chạy H8-adapter |

Bộ chặn rò mã (mục 1, ca `659a9dfb`): chuỗi `659a9dfb` nằm trong spanId `c9b4b659a9dfb45d` (span `EVALSHA`) của `cases/659a9dfb/raw-traces.jsonl` (`grep -c` = 1 dòng; `manifest.json` chứa mã của chính nó). Đây là trùng ngẫu nhiên, không phải nhãn lọt. Gợi ý cho T-064 (chưa kiểm): mã mờ 8 hex có xác suất trùng với ID span/trace không nhỏ trên ca nhiều span.

## 6. Đề xuất WHY

`thu3/de-xuat-WHY.md`: (a) build lại riêng Event từ `6b21ed55` + bản vá, thu trên bản 3; (b) cường độ POOL-EVENT = 5; (c) ô H4 = bandwidth 1 KB/s dưới ×3 + đối chứng BINH-THUONG-X3. Chưa có mục cho RECREATE-PAY và hai "Sửa sau" — điều phối cân nhắc thêm khi chép (lý do và bằng chứng ở `KE-HOACH.md` bổ sung 4 và `dieu-kien-xac-nhan-3.md`).

## 7. Việc cần Minh quyết

1. **Nhận "Sửa sau 1" và "Sửa sau 2"** (`dieu-kien-xac-nhan-3.md`)? Đề xuất: nhận cả hai. Sửa 1 không đổi điều kiện đã khai (chỉ sửa script cho khớp); sửa 2 dùng cùng nguồn đầu dò, bỏ hiệu ứng lookback, mẫu thô cho thấy payment phục hồi ở ~t + 53. Mặt trái: cả hai làm sau khi xem kết quả. Phương án khác: thu lại BINH-THUONG-X3 và RECREATE-PAY với điều kiện đã sửa (~1 giờ máy). Nếu không nhận: H4 mất đối chứng cùng bậc tải; H8-adapter mất ca thật.
2. **Giữ hay hoàn tác bản 3 trên `exp-app`** sau thu bù (điều phối quyết trong quyền chiến dịch; ghi ở đây để không bị quên): giữ thì các đợt sau chạy trên bản 3; hoàn tác thì Event về `arm64-t062-6b21ed55`.
3. Hook làm chậm consumer cho H4 trong `src/rca-test` Booking: **không cần** cho đợt này (×3 đạt). Không đề xuất.

## 8. Hash cần giữ

- `cases/ebd5ef38`: inventory `8311ef52…`, manifest `06550fee…`, prometheus `d59bf726…`, raw-logs `08c13ca8…`, raw-traces `cb0f17a0…`, request `542e2f6a…` (422 MB). `cases/ebd5ef381d1a`: manifest `198193f4…`, raw-traces `d911c577…`, ba file còn lại trùng `ebd5ef38`.
- `bo-sung-dev3`: `7d1ee32f` `0616eacd…`, `86dea661` `d6739fd3…`, `0a45b2e0` `79dcdacd…`, `1e5a3dc5` `a66854cd…`, `659a9dfb1ab0` `237337fc…`, `ebd5ef38` `defa6d73…` (năm mã đầu khớp `bo_sung_sha256` trong `thu/chay/nhat-ky-3.jsonl`).
- `.tgz`: theo `tgz_sha256` trong `thu/chay/nhat-ky-3.jsonl` (kiểm lại khi nhận: 5/5 khớp).

## 9. Lệnh cuối đã chạy

`PYTHONIOENCODING=utf-8 py -3 -B results/T-063/thu3/scripts/so_sanh_o_cu.py` (→ `thu3/so-sanh-o-cu.json`), sau đó sửa số trong `bao-cao.md`. Khóa SSH trên `exp-obs` (`~/rca-dieu-phoi/keys`) **chưa gỡ**: chờ điều phối xác nhận không còn thu bù.
