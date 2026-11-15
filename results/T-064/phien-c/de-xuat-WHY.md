# Đề xuất mục WHY — phiên C (T-064)

Phiên C không ghi `docs/WHY.md` (brief §4). Phiên điều phối chép các mục dưới vào cuối `docs/WHY.md`, đánh số tiếp sau mục lớn nhất lúc chép, **trước khi** dùng kết quả liên quan trong hồ sơ chọn. Đến lúc đó, kết quả phụ thuộc trong `BAN-GIAO-C.md` mang nhãn "chờ WHY".

---

## WHY-(a) [T-064] Kiểm độ nhạy mốc: dựng lại đầu vào từ gói ca với t' = t + d, xuất lại gói metric bổ sung quanh t'

- **Chọn gì.** `chay_ca.py --doi-t d` dựng lại cả bảy tham số M1 từ gói ca (`m1_ft/doi_moc.py`), đi đúng đường của runner ghim `run-m1.py`: `adapt(..., t')`, cấu hình khóa P7 cộng `params_ca`, cùng các phép kiểm trường cấm và rò giá trị. Mọi nơi dùng t đều dùng t': `inputs[5]`, cửa sổ cắt span/log/metric của M1, `span_phu`, H5b. Gói metric bổ sung (chỉ có [t−300, t+300]) được xuất lại quanh t' bằng đúng bộ xuất `results/T-063/dong-goi/xuat_bo_sung.py`. Với 9 ca T-062, gói gốc quanh t chỉ được dùng khi các kênh cấu hình đọc tới (live-down, live-ms) rỗng; `chay_ca.py` kiểm điều này và từ chối nếu không đúng.
- **Vì sao.** `method-input.json` của P7 chỉ chứa [t−300, t+300). Nếu chỉ đổi `inputs[5]`, cửa sổ của M1 hụt |d| giây ở một đầu: A ngắn đi khi d = +30, N ngắn đi khi d = −30. Khi đó phép kiểm độ nhạy trộn hai hiệu ứng, dời mốc và mất dữ liệu. Gói ca chứa dữ liệu thô [t−600, t+600). Cả 22 ca được đóng gói lúc t + 783…808 s, nên có đủ dữ liệu cho |d| ≤ 300.
- **Đã xét.** (1) Chỉ đổi `inputs[5]`: bị loại vì trộn hiệu ứng như trên. (2) Cắt bớt cửa sổ còn [t'−270, t'+270]: bị loại vì đổi độ dài N/A so với P7. (3) Dùng gói bổ sung quanh t cho mọi ca: một phần cửa sổ của kênh live sẽ nằm ngoài gói, độ phủ A/N của kênh đó đổi.
- **Bằng chứng.** Dựng lại với d = 0 cho `method-input.json` trùng byte bản đã lưu (laptop, a5539fba; trên `exp-obs` là bản V058, 22 ca, xem `BAN-GIAO-C.md`). `chay_ca.py` cũ và mới cho đầu ra trùng byte ở đường mặc định (V041, a5539fba). 26 gói bổ sung xuất lại: 252.125 điểm chung trùng giá trị gói gốc, 0 lệch (`doi-moc/kiem-bo-sung-doi-t.json`). Bộ đệm đầu vào kiểm hash khi đọc.
- **Kết luận phụ thuộc.** Kết quả dời mốc ±30 s của P7, V032, V041 (V052–V057), phép thử giả d = −300 (V059).
- **Giới hạn.** Mỗi ô một lần thu. Dời mốc là phép kiểm độ nhạy của phương pháp với mốc t do người dùng đưa vào, không phải đo dao động giữa các lần thu.

## WHY-(b) [T-064] H8-adapter: nối chuỗi container khi chỉ khác nhãn runtime và không chồng lấn trong mốc mẫu gốc

- **Chọn gì.** Trước adapter ghim, các chuỗi của cùng một metric logic (kênh, thực thể) được nối theo thời gian khi thỏa cả ba điều kiện: (i) chỉ khác nhau ở `container_id`, `container_name`, `service_instance_id`; (ii) không chồng lấn trong mốc mẫu gốc (`timestamp()`): mẫu cuối của chuỗi trước sớm hơn mẫu đầu của chuỗi sau; (iii) kênh có mốc mẫu gốc. Ở mỗi mốc đánh giá có nhiều điểm, giữ điểm có mốc gốc mới nhất. Không thỏa điều kiện thì giữ hành vi P7 (adapter ném lỗi). Mặc định tắt.
- **Vì sao.** Đây là nhu cầu kỹ thuật (luật 18), không phải cách xử lý một hạn chế phương pháp. Khi một container bị tạo lại trong [t−600, t+600], P7 ERROR cả ca. FlashTicket Compose chạy một container cho mỗi service. Lần theo `thuong01`: trong mốc gốc, chuỗi cũ và mới không chồng lấn (ví dụ api-gateway [−609, −509] s và [−499, 591] s). Phần trông như chồng lấn trên lưới đánh giá là do lookback ~300 s của PromQL lặp lại mẫu cuối của container đã dừng. Giữ điểm có mốc gốc mới nhất cho đúng giá trị mà một chuỗi duy nhất đã cho.
- **Đã xét.** (1) Cộng hoặc lấy trung bình các chuỗi: bị loại vì sai khi hai container không đồng thời (cộng lặp mẫu cũ vào mẫu mới) và vì cần khai phép gộp. (2) Bỏ nguồn bị trùng: mất kênh cpu/mem của thực thể vừa tạo lại, đúng nơi có thông tin. (3) Gộp cả khi chồng lấn: chỉ đúng với nhiều bản sao, cần phép gộp khai báo; chưa có trường hợp này nên không làm.
- **Bằng chứng.** `phien-c/h8-adapter/dem-chuoi-trung.json` (37 gói: chỉ thuong01 bị lỗi). Test `src/m1_ft/tests/test_h8.py`: tách giả cpu+mem booking của a5539fba tại t+60 theo đúng ngữ nghĩa lookback; adapter ghim ném lỗi; nối lại cho rows, owners, indices, clocks, coverage, aliases trùng bản gốc; chồng lấn và khác nhãn ngoài runtime thì không nối. Trên exp-obs: thuong01 P7 ERROR, bản có H8-adapter chạy được (14 nhóm nối, 0 nhóm không nối); 22 ca trùng bản cha. **Đính chính chú thích mã:** `mat_mau` không phải chỉ số mất thông tin. Ở thuong01 `mat_mau` = 12: mỗi mẫu là mẫu gốc cuối của container cũ, nằm cùng bước lưới 15 s với mẫu đầu của container mới (ví dụ −509 s và −499 s), nên không phải mẫu mới nhất ở mốc đánh giá nào. Một chuỗi liên tục cũng không bao giờ trả các mẫu này. Docstring của `h8_adapter.py` ("điểm bị bỏ luôn là bản lặp… `mat_mau == 0`") cần sửa ở lần đóng gói mã kế tiếp; chưa sửa vì sẽ đổi `ma_nguon_sha256` đã ghi trong đầu ra.
- **Ca thật** RECREATE-PAY `ebd5ef38` (chưa vào tập chọn, chờ Minh): P7/V032 ERROR; V060/V061 cho payment-service hạng 1.
- **Kết luận phụ thuộc.** V060, V061; mọi bản sau có H8-adapter.
- **Điều kiện thất bại.** Nhiều bản sao chạy song song; nhãn khác ngoài nhóm runtime (ví dụ chuyển host); container mới có mức tài nguyên khởi động khác hẳn nên bị gắn cờ (thông tin thật, nhưng có thể không phải gốc).

## WHY-(c) [T-064] H8-log: kết cục nghiệp vụ theo hợp đồng B16 — phân loại dòng lỗi (H8-log-kq) và hai kênh metric (H8-log-chuoi)

- **Chọn gì.** Trường `outcome` của log JSON được dùng theo ngữ nghĩa B16 (`B16-observability-baseline.md` dòng 56): FAILED ∪ UNKNOWN là kết cục lỗi; SUCCESS, REJECTED (từ chối theo luật nghiệp vụ) và RETRY (lỗi tạm, tự thử lại) là kết cục không lỗi.
  - **H8-log-kq:** dòng có `outcome` được phân loại lỗi theo kết cục thay vì severity, trong kênh `log_loi` sẵn có (cùng đơn vị, E4 đếm, cổng D1, lớp lan ngược).
  - **H8-log-chuoi:** thêm hai kênh metric 15 s theo service, qua đường metric chung (E4 phân vị + G3): `log-kq-loi` là tỷ lệ kết cục lỗi (lớp "lỗi"); `log-kq-ok` là số SUCCESS/s (lớp "lưu lượng"). Ô được đóng dấu ở đầu ô để không trộn N với A.
  - Nút là thực thể ghi log. Không thêm cạnh. Nơi đặt: log ứng dụng, qua Collector, vào `raw-logs.jsonl` của gói ca (`bo_sung.log_phu`).
- **Vì sao.** `outcome` là trường hợp đồng, còn severity do người viết code chọn. Kênh `log-kq-ok` phủ phần xử lý bất đồng bộ qua RabbitMQ (saga thanh toán, phát vé), phần mà kênh `workload` HTTP của P7 không thấy.
- **Đã xét.**
  - (1) Thêm đơn vị log mới bằng cách bọc `don_vi_log`: P7 dùng cổng D1, mà mốc N của mỗi đơn vị log được tính bên trong `chuoi._chay` từ dòng lỗi theo severity, nên đơn vị mới lệch số dòng và ERROR. Không thể làm mà không sửa `src/m1`.
  - (2) Một đơn vị cho mỗi `reasonCode`: nhiều phép thử hơn, tăng cờ giả; chưa có căn cứ.
  - (3) Tính RETRY là lỗi: RETRY|SMTP_UNAVAILABLE của ticket là nền liên tục khoảng 3.500 dòng/300 s, sẽ lấn tín hiệu FAILED.
- **Bằng chứng đầu vào.** `h8-log/dem-log-nghiep-vu.json`, `cheo-severity-outcome-22ca.json`. Trong cửa sổ của 22 ca, ERROR trùng FAILED ở 10.424/10.424 dòng. H8-log-kq chỉ đổi lớp 4.490 dòng UNKNOWN, ở 10 ca. Kết quả chấm ở `BAN-GIAO-C.md`.
- **Khai.** Thiết kế sau khi đã xem số đếm theo ca × service. Người làm biết mã ca ↔ ô (ví dụ event-service chỉ có log FAILED ở hai ca HTTP5-EVENT). Định nghĩa kênh theo B16, không chỉnh theo đáp án.
- **Kết quả** (`cham/h8.json`): H8-log-kq không đổi đại lượng chấm nào (phép 1, 2). H8-log-chuoi: phép 1 GIU (l1), PAUSE-PAYMENT — → 4, tổng hạng 15 → 13, ở một ô đã xem trước; phép 2 không tác dụng.
- **Kết luận phụ thuộc.** V062–V065.
- **Điều kiện thất bại.** Dịch vụ chỉ ghi log khi lỗi (event-service): N rỗng. Phía gọi ghi FAILED cho lỗi của bên được gọi (lan ngược xử lý như `log_loi`). `log-kq-ok` đổi theo tải (H7 không áp cho kênh này). user-service không ghi log nghiệp vụ, nên không có kênh này.
