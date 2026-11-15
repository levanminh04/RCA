# Phản biện T-064 — lượt 4

- **Người phản biện:** Codex. **Ngày:** 15/11/2026. **Ý định:** REVIEW.
- **Commit/diff đã đọc:** HEAD trùng commit gốc trong brief; đầu ra chiến dịch chưa commit. Kiểm đầu ra hiện tại, không sửa công việc đang có.
- **Công đoạn/cổng và bản lượt:** soát kết quả phần thay đổi sau REVIEW-3; chiến dịch M1-FlashTicket, M3. Chỉ ghi bản mới `tasks/T-064-m1-flashticket/REVIEW-4.md`. Đã liệt kê thư mục: chưa có bản này. Claude giữ vai trò người làm, Codex giữ vai trò người phản biện.
- **Đã đọc:** AGENTS; STATE; SPEC và LOG T-064; hồ sơ chiến dịch §4–7 và checkpoint; mục tiêu/RQ của MRP; DT18 và hướng dẫn cô; LESSONS; WHY từ WHY-81, DECISIONS phần chiến dịch. Đầu ra: tiêu chí chọn, hồ sơ chọn, sổ biến thể, tập chọn/đáp án dev2–dev3, các bảng chấm/giữ-bỏ/dời mốc, ghi chú cơ chế, chú thích nền, hợp đồng đầu ra, bản đề xuất, chỉ mục và script dựng, manifest và script lập manifest. Code: `src/m1_ft/`, các đường span → E1/E2/E5 → E6/E7 của lõi P7, bộ chấm P3, script lô 5/nhận/kiểm. Đọc thêm nguồn thu bù 3 khi lần kênh liveness và báo cáo phát hiện hash của T-065. Sau tự soát mới đọc các finding và bảng phản hồi của REVIEW, REVIEW-2, REVIEW-3.
- **Tự soát độc lập:** kiểm hash trước, tính lại từ từng output, lần cạnh/nhãn/chuỗi runtime, kiểm bảng chọn và bản xuất. Trước khi mở kết luận cũ đã ghi nhận độc lập lỗi liveness ở ca tạo lại container, thiếu chú thích ca bình thường ×3 và việc quyền áp §5 đã có. Không dùng LOG thay đầu ra.

## Kết luận chung

Có **một điểm CHẶN mới (R9)** về kiểm đúng đắn của H5b và **một điểm KHÔNG CHẶN lựa chọn ứng viên (R10)** về hồ sơ ca không lỗi mới. Số chấm hiện tại khớp: V082 có AC@1 = 9/11, AC@3 = 11/11, tổng hạng cắt 13, K = 4/6; không hồi quy ở mốc gốc trên T-062. Nguồn: `cham/chon-dev3-d0-v082-A.json#/ban/V082-V066+H8a/{chon,t062}`.

R6–R8 đã được xử lý đúng trong phần thay đổi sau REVIEW-3. Tuy vậy, chưa đủ xác nhận phần phương pháp của M3 hoàn tất để nghiệm thu M4: H5b đang gọi một dịch vụ đã phục hồi là “chết im”. Quyết định Minh chọn **ứng viên V082** vẫn được ghi nhận; điểm dev đúng không thay phép kiểm đúng đắn của thành phần, không khóa thiết kế, không trả lời hiệu quả giữ ngoài hoặc RQ5.

## Các điểm

### R9. Lookback biến lần mất phản hồi ngắn thành “chết im” suốt cửa sổ — CHẶN kiểm đúng đắn H5b và xác nhận hoàn tất M3

- **Ở đâu:** `results/T-063/dong-goi/xuat_bo_sung.py:39`; `src/m1_ft/thanh_phan/h4_h5.py:114`, `:119`, `:160`; output V082 ca `ebd5ef38`; hồ sơ chọn §15–16 và WHY-86/98.
- **Sai gì:** kênh `live-down` dùng `max(httpcheck_error)` qua `query_range`. Đây là giá trị đánh giá có lookback, không phải kết quả của lần dò mới nhất. Chuỗi lỗi cũ tiếp tục có giá trị 1 sau khi dịch vụ phản hồi lại. `_chet_im` đọc các giá trị ấy như nhiều lần không phản hồi liên tiếp, vượt điều kiện 60 s, rồi ghi đè khóa xếp hạng. Điều kiện đã mô tả của H5b là không phản hồi lại tới hết cửa sổ và không nhận lần chết ngắn dưới 60 s; ca thật này không thỏa điều kiện đó.

**Chuỗi bằng chứng đã kiểm:**

1. Gói đã dùng thực sự: `exp-obs:/opt/rca-m1ft/bo-sung-dev3/ebd5ef38/prometheus-bo-sung.json`. Đọc chỉ đọc qua SSH, hash trùng `.../l5/dev3/d0/V082-V066+H8a/ebd5ef38/summary.json#/moc/bo_sung/sha256`; `loi_khuc=[]`. Với t = 1794651100, `live-down` của cổng 8083 là 0 tới t, rồi **1 tại toàn bộ 20 điểm t+15…t+300**, bước 15 s.
2. Đối chiếu mẫu gốc trên chính Prometheus, chỉ đọc lịch sử tại t+300:
   - `httpcheck_error{http_url=~".*:8083.*"}[600s]`: đúng **5 mẫu**, tại t+3,211; 13,225; 23,205; 33,209; 43,204 s.
   - `httpcheck_status{http_url=~".*:8083.*"}[600s]`, lọc `http_status_code="401"`, giá trị 1: phản hồi trở lại **t+53,207**, tiếp tục mỗi khoảng 10 s tới t+293,209.
   - Dữ kiện đã lưu độc lập cũng khớp: `results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/ebd5ef38/httpcheck_error_8083_mau_tho_tuong_doi_t` là [3,13,23,33,43]. File này khớp manifest thu3.
3. Output đã băm của V082: `kiem/nhan-luot5/l5/dev3/d0/V082-V066+H8a/ebd5ef38/method-output-1.json#/extra/m1_ft/chu_thich/H5-liveness/chet_im/thanh_phan/payment-service` ghi `tu=t+15, den=t+300, so_mau=20`: đoạn “chết im” **285 s**. `#/extra/blocks_P/0/key` trước H5b bắt đầu [2,4511,15…]; `#/blocks/0/key` sau H5b thành [3,0,0,0,0].
4. Đếm trên toàn bộ nguồn output duy nhất được hai bảng chấm hiện hành tham chiếu: lỗi nhận chết im này xuất hiện ở **7 bản tại d=0** (V061, V068–V072, V082), và V082 ở **4 mốc d khác 0** (−60, −30, −15, +15). Không suy từ một output thành mọi ca H5b.
5. Quy ước truy vấn phù hợp [tài liệu Prometheus về staleness/lookback](https://prometheus.io/docs/prometheus/latest/querying/basics/#staleness): bước đánh giá có thể dùng mẫu cũ trong khoảng lookback. Ở đây mẫu và gói thật đã phân xử được lỗi; không chỉ suy từ tài liệu.

- **Phần có thể phản bác finding:** Payment đúng là thành phần bị tạo lại và vẫn hạng 1 **trước** khi H5b ghi đè; V060 chỉ có H8-adapter cũng cho Payment hạng 1. Vì vậy finding **không chứng minh AC@1 hiện tại bị tăng sai**, không bác việc H8-adapter sửa lỗi nhiều chuỗi runtime, không đòi bỏ ca RECREATE-PAY. Nhưng đáp án đúng che việc quy tắc chết im kích hoạt sai. Không thể dùng điểm cuối này để xác nhận H5b đã xử lý đúng lần khởi động lại ngắn. Đây là lỗi chuyển đổi/đọc ngữ nghĩa tín hiệu; không phải dữ liệu thô thiếu, lỗi SSH hay nhiễu không thể kiểm.
- **Bước và quyết định chịu ảnh hưởng:** telemetry → kênh liveness → nhận chết im → ưu tiên nhóm đầu. Chặn xác nhận H5b đúng nguyên lý và nhận phần kiểm không nhãn của M3 là hoàn tất. Tạm giữ các số đã đo như kết quả của bản hiện tại. Mức thay đổi điểm sau sửa còn OPEN: hạng 1 của riêng ca này trước ghi đè chưa chứng minh mọi metric liveness, ca và mốc đều bất biến.

**Đề xuất sửa tối thiểu của người phản biện:**

- Ưu tiên sửa cách dựng/đọc trạng thái liveness để dùng **quan sát mới cùng timestamp gốc**, phân biệt không phản hồi, đã phản hồi lại và thiếu quan sát; áp cùng quy tắc cho mọi service/ca. Có thể thêm bộ xuất riêng trong `results/T-064/kiem/` và sửa phần đọc ở `src/m1_ft/`, giữ nguyên bộ xuất đã ghim của T-063 nếu muốn giảm phạm vi. Người làm phải chốt đường kỹ thuật cụ thể trước khi sửa.
- Dùng dữ liệu dev đã lưu/còn trên Prometheus. Kiểm trước hai tình huống đã có: RECREATE-PAY phục hồi và PAUSE-PAYMENT mất phản hồi dài; lần tới trung gian rồi mới quyết phần cần tính lại. Sau đó đối chiếu đầu vào để dùng lại phần không đổi, bổ sung đúng các cấu hình/ca/mốc và bảng chấm chịu ảnh hưởng. Chưa có căn cứ chạy lại toàn bộ 82 mã biến thể hoặc thu lại dữ liệu.
- Quy mô tham chiếu từ summary cũ: V082 trên 28 ca có tổng `giay_chay` hai lần cộng `giay_bo_sung` khoảng **1.312 s**; riêng hai ca trên khoảng **116 s**. Đây là tổng thời gian đã ghi, **không phải ETA** cho đường sửa. Phần nhiều bản/dời mốc chưa định lượng; người làm cần nêu khối lượng thực và chi phí trước khi phát, theo quyền chiến dịch và luật lượt dài.
- Phương án khác đã xét: giữ bản hiện tại và khai quy tắc là “đã thấy lỗi trong lookback”. Cách đó đổi nghĩa H5b và không đáp ứng lập luận “chết im ≥60 s”; phải được Minh chọn như một giới hạn/thiết kế khác, không giải quyết bằng đổi chú thích thành “đã kiểm đúng”.

**Pin và đường thực thi:** `h4_h5.py`, `bo_sung.py` và các file Python liên quan nằm trong hash cây mã của sổ/summary và `manifest.json#/src_m1_ft`. Bộ xuất T-063 cũng đã ghim trong manifest T-063. Sửa byte code hoặc gói bổ sung làm đổi hash tương ứng. Cần giữ snapshot và kết quả cũ, dùng bản/thư mục đầu ra mới: `l5_chay.sh` bỏ qua slot có summary, còn `chay_ca.py` dùng `exist_ok=False`. Thêm WHY trước khi dùng lựa chọn sửa; các chỉ mục/cấu hình đề xuất/bảng chấm/tài liệu bị ảnh hưởng lập bản tiếp theo theo phạm vi Minh quyết. Reviewer chưa sửa hay chạy phương pháp sửa.

### R10. Ca bình thường ×3 mới chưa có trong hồ sơ cơ chế và chú thích giao dịch — KHÔNG CHẶN thứ tự chọn V082

- **Ở đâu:** `ho-so-chon.md` §6, §15–16; `phan-tich/ghi-chu-co-che-dev2.md`; `chu-thich-thao-tac-nen.md`; yêu cầu chiến dịch về chú thích mọi ca không tiêm lỗi, tiêu chí §7 và M3(c).
- **Sai gì:** tập chọn đã thêm `1e5a3dc5` và ca này đóng góp một đơn vị K của V082, nhưng bảng chú thích vẫn chỉ có các ca dev2/T-062 và các bản cũ. Các câu hỏi Q4 về thao tác DB hoặc FLASH-HEALTHY không bao phủ ca này. Chưa có phân tích riêng, hoặc mục chưa phân xử kèm đúng bằng chứng thiếu, cho ca không lỗi mới trong bản đề xuất.
- **Bằng chứng độc lập:** `chon-dev3-d0-v082-A.json#/ban/V082-V066+H8a/chon/ca/1e5a3dc5` ghi `CAUSE_FOUND, k=1`. Output tại `kiem/nhan-luot5/l5/dev3/d0/V082-V066+H8a/1e5a3dc5/method-output-1.json`:
  - `#/extra/kenh_co`: Payment có đúng một cờ tự sinh, `metric|payment-service_cpu`, s ≈ 2,7646; cờ `ticket-service_live-ms` có `F_I=0`.
  - `#/extra/don_vi_phan_vi`, lọc `ma=metric|payment-service_cpu`: n_N=n_A=20, r_len_N=0, r_len_A=0,05, h≈0,08159, p_len≈0,003968. Đây là kênh CPU, không thuộc nhánh sàn 1 ms cho span.
  - Đối chứng bản 3 `7d1ee32f` ở tập độ nhạy cũng có cờ tự sinh Payment CPU. Không được gán nguyên nhân riêng cho tải ×3 chỉ vì tên ca.
  - `results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/1e5a3dc5/k6`: multiplier=3, journey_failed=0, dropped_iterations=0, token_refresh_failure=0. Bàn giao B ghi tải ×3 **suốt chu kỳ**, khác ca FLASH-HEALTHY tăng tải tại t. Các số này chưa phải đối chiếu latency N/A.
- **Phần có thể phản bác finding:** hồ sơ đã đếm K đúng, có giới hạn n=1, chưa nhận hoàn tất RQ5. Không đòi chứng minh nguyên nhân vật lý hay chạy lặp ngay. Phần thiếu là đầu ra đã yêu cầu trong chính chiến dịch, có thể bắt đầu từ dữ liệu/trung gian đang có; không phải phép kiểm thêm “cho chắc”.
- **Bước và quyết định chịu ảnh hưởng:** diễn giải K và hoàn thiện hồ sơ M3/M4; chưa làm sai số hoặc thay thứ tự chọn. Chưa đủ gọi toàn bộ ca sai còn lại của ứng viên đã được phân tích/chú thích.
- **Đề xuất tối thiểu:** bổ sung mục cho ca này trong hồ sơ cơ chế và chú thích nền, đối chiếu cờ CPU với k6 đã lưu và ca đối chứng cùng bản. Tách điều đã lần được (kênh → cổng → F_I → verdict) khỏi nguyên nhân CPU đổi. Nếu chưa phân xử: nêu các khả năng còn lại như dịch tải công việc nền hoặc dao động tín hiệu/cổng; chỉ rõ cần đối chiếu chuỗi CPU gốc, thời điểm log/thao tác và latency N/A trên các gói dev nào. Phần đọc/đối chiếu đầu ra hiện có chỉ ở mức vài phút; chưa cần phát lô hay đổi K. Phương án gộp vào Q4 chỉ phù hợp khi nêu rõ đây là kênh khác và giữ nguồn từng ca.
- **Pin:** hai tài liệu và ghi chú cơ chế nằm trong `manifest.json#/file`. Bổ sung sẽ đổi hash tài liệu; giữ manifest hiện tại và lập bản kế tiếp khi chốt bàn giao. Không sửa bảng điểm hoặc code để làm khớp chú thích.

## Đối chiếu các lượt trước

| Điểm và phản hồi | Đánh giá lượt này, bằng chứng và phạm vi |
|---|---|
| R1 — phân loại HTTP/message; người làm nhận, sửa và chạy lượt 3 | **Đúng; sửa đã xử lý đúng lỗi được nêu.** Vòng lặp H1 hiện tách kind trước chấm. Kiểm lại đầu ra V039 ở 98ea5ba4: Payment→Booking có HTTP 72/0 và message 144/0. Không mở lại bản sửa; các bản H1 cũ là lịch sử. |
| R2 — gọi bỏ H1c là bỏ quan hệ | **Đúng; đã xử lý.** Cấu hình và code V002/V082 vẫn dùng E1/E2/E5. H1 là phần xuất cạnh thêm vào. DT18 không buộc chọn bản có bảng cạnh. |
| R3 — WHY của sàn/H5b và mức căn cứ cho 1 ms | **Đúng về thiếu nguồn/thời điểm và giả thuyết vật lý.** WHY-85/86 công khai ghi muộn, một ô và ngưỡng thực dụng; không tạo bằng chứng vật lý mới. R9 là lỗi đầu vào H5b mới được phân xử trên ca thu bù, không suy từ việc WHY muộn. Không xác nhận đã rà xong mọi lý do của mọi hướng bị loại. |
| R4 — quyền áp dụng §5; người làm từng nhận | **Đúng; LOG phiên 5 S5 lại đọc thiếu nguồn bổ sung.** DECISIONS mục “Bổ sung quyền điều phối…” dòng 579 cấp quyền áp tiêu chí đã trình và đoạn cuối giải quyết các mục chờ cũ. Hồ sơ chọn §4 đã đính chính đúng. Không cần Minh xác nhận lại thứ tự hiện hành; đổi tiêu chí sau xem mới là việc khác. Việc Minh chọn V082 không phải căn cứ duy nhất cho quyền áp §5. |
| R5 — “không bản nào hồi quy” | **Đúng; đã khoanh lại phạm vi.** Tính độc lập tập T-062 hiện hành vẫn thấy H1a/H1b bị loại có điểm thấp hơn P7; các bản trong bảng ứng viên §5 không hồi quy tại d=0. Câu này không áp cho mọi mốc dời hoặc mọi biến thể. |
| R6 — V051 còn H1c; người làm nhận và thêm V066/V067 | **Đúng; phần sửa xử lý đúng.** V066 không H1, V067 thêm tắt E1/E2/E5, E6a; không còn đường quan hệ vào điểm nút. Cặp V041→V067 cho 8/10/19 → 7/8/24 trên tập 17. E7 vẫn dùng cạnh để xuất vùng, nên “bỏ toàn bộ” phải hiểu theo phép tính xếp hạng được so, không phải toàn bộ output mất mọi thông tin cấu trúc. Không suy lợi ích cấu trúc thật, không tách riêng đóng góp E1/E2/E5 từ phép tắt chung. |
| R7 — mất ưu tiên H5b không phải mất toàn bộ lợi thế | **Đúng; §14 sửa đúng.** Output V056 tại +30 ở PAUSE-PAYMENT vẫn đưa Payment hạng 3, P7 vắng. Bảng độ nhạy mới giữ phân biệt này. Không tự coi giải thích N lẫn lỗi đã được xác nhận ở mọi ca mới. |
| R8 — WHY-87–89 ghi sau kết quả; người làm nhận và thêm WHY-94 | **Đúng; WHY-94 khai đúng lịch sử và phần thêm sau.** Không sửa ngược mốc hoặc chạy lại để giả lập lý do có trước. |
| N1 của lượt 1 — giờ ước lượng | **Đúng phần đã đính chính.** Đã đọc mốc sổ trước lô 5, V082 và dòng đính chính hash. Không xác minh mọi giờ ước lượng cũ; không dùng chúng để suy quyền mới. |
| N2 của lượt 1 — độ vượt sát sàn | **Đúng phần quan sát; đáp ứng K quanh 1 ms vẫn chưa đo.** Không gọi đây là kết quả quét. Không yêu cầu quét chỉ để sửa một câu; giữ giới hạn ngưỡng thực dụng. |
| N1 của lượt 3 — K tăng ở ±30 | **Đúng; §14 bổ sung đúng.** Trên 13 ca cũ, P7/V032 K từ 4 thành 5, V041 giữ 3. Tập 17 có mẫu số khác và được báo riêng. |

## Tuân thủ quy trình và toàn vẹn

- Giữ đúng vai trò. Không sửa LOG, STATE, code, kết quả, manifest cũ hoặc máy; không commit, không mở dữ liệu khóa, không chạy thực nghiệm mới, không tự gửi prompt sang agent khác. Các lệnh SSH chỉ đọc file/Prometheus lịch sử, không in khóa.
- T-064: **7.612 tham chiếu hash khớp** = 7.585 file kết quả + 18 file nguồn + 9 file ngoài. Hash cây mã tính độc lập trùng hash lô 5; 704 output M1-FT thuộc thư mục lô 5 được các bảng chấm dùng ghi đúng cây nguồn hiện hành. File tiêu chí khóa không đổi. Lỗi hash V082 lúc 16:57 đã có dòng đính chính, giữ bản lỗi; chỉ mục hiện tại và cấu hình đề xuất dùng đúng hash JSON chuẩn hóa, có hash byte riêng.
- Nguồn thu bù: phát hiện `thu3/dieu-kien-xac-nhan-3.md` lệch manifest, đã báo Minh và dừng dùng **toàn file hiện tại** như nguồn khớp hash. Kiểm trong bộ nhớ tìm được **7.948 byte đầu khớp chính xác hash đã ghim**; 268 byte nối sau chỉ là đoạn nhận hai “Sửa sau” của Minh. Không có nội dung tính toán trong phần nối đó. R9 dùng prefix đã khớp, bàn giao B và JSON hậu kiểm đã khớp, cùng gói thật và mẫu gốc trên máy; không suy từ file lệch rằng telemetry hỏng. Manifest thu3 hiện chưa xác nhận toàn bản văn đã nối; việc cập nhật hồ sơ nguồn thuộc người làm, không tự sửa ở lượt này.
- Tập 17/19, đáp án A/B, thay đổi tập chấp nhận H4 và V082 đều khai lịch sử đã xem dữ liệu. Đáp án H4 trước chấm biến thể, nhưng sau khi đã thấy P7; quyết định Minh đã ghi. Không gọi đây là nhãn khai trước mọi quan sát. Không thấy đường nhãn từ bộ chấm vào phương pháp ở phần thay đổi này: mã ca dùng để định tuyến; đầu vào phương pháp là telemetry, t và cấu hình; đáp án chỉ ghép phía chấm.
- Lô 5 dùng máy và tuyến nhận đã khai, loại tuyến laptop theo điều kiện trùng byte. Các lỗi nhiều chuỗi runtime được lưu và tính trượt; không biến chúng thành lỗi hạ tầng. Không dùng việc SSH/Python bị hạn chế ở sandbox làm kết quả khoa học.
- STATE vẫn ở thời điểm lô 5 đang chạy; LOG và đầu ra mới hơn đúng phạm vi brief. Task/M4 chưa đóng, nên chưa coi thiếu cập nhật bàn giao cuối là vi phạm đóng task. R9/R10 là phần cần xử lý trước khi nhận đủ căn cứ, không phải yêu cầu làm hết nghiên cứu giữ ngoài.
- Không thêm quyết định nghiên cứu. Hai lựa chọn đang xin Minh xử lý ở lượt này là đề xuất của reviewer tại R9/R10; không tự sửa theo finding.

## Điều đã kiểm và thấy đúng

1. **Chấm độc lập, không gọi lại bộ chấm của người làm.** Viết phép tính trong Node, đọc từng output, tính phân bố hạng nhỏ nhất trong nhóm hòa, chiếu cạnh, cắt hạng, K; đối chiếu bộ chấm P3 và code chấm T-064. Kiểm **2.925 lượt bản×tập×ca**, từ 41 bản d=0 và 24 cấu hình dời mốc trên ba tập. Điểm từng ca và tổng đều khớp; không MISSING. Đây có lặp ca giữa tập 17/19, không phải 2.925 quan sát độc lập.
2. **Nguồn duy nhất và hai lần chạy:** 1.708 thư mục đầu ra duy nhất được tham chiếu, gồm 1.660 output OK và 48 slot lỗi đã lưu. Đối chiếu hai file byte ở 1.647 output OK có đủ bản sao local; 13 P7 dev2 chỉ có bản 1 local đã đối chiếu cả hai file gốc trên exp-obs với hash bản local: 13/13 khớp. Không nhầm 48 slot lỗi với số lỗi mới của một lô: có 2 lỗi cũ được dùng lại ngoài thư mục lô 5.
3. **Bảng cạnh và hai đáp án:** tính lại 715 lượt chấm cạnh, kể cả UNSUPPORTED/VẮNG; khớp. Toàn `ban` của hai cặp bảng A/B d=0 và dời mốc trùng, bao phủ 65 tên bản/cấu hình; không chỉ so số đứng đầu. Kiểm luật giữ/bỏ và xếp §5 trên các số ấy; V082 đứng trước V061, V068–V070, V072, V071.
4. **Bản xuất:** 84 slot = P7/V082/V071 × 28 ca; hash file trỏ tới khớp, lỗi P7 ở RECREATE-PAY được biểu diễn rõ; 56 output biến thể khớp hash cấu hình và cây mã của chỉ mục. Không thấy lỗi còn lại của đính chính 16:57.
5. **Vai trò đồ thị:** E1 đổi thời lượng đầy đủ sang độc quyền, E2 dùng mẫu span bọc qua cạnh, E5 dùng quan hệ để xác định bằng chứng kế thừa trước E6a. V067 giữ telemetry và inventory nhưng tắt những phép tính này, không H1. Vì vậy bằng chứng mới trả lời được phép tắt nhóm quan hệ trên dev; chưa chứng minh tác dụng từng bước hoặc cấu trúc thật tốt hơn mọi cấu trúc khác.
6. **Dùng lại cơ chế đã có:** Q6 đã lần hai thao tác Booking bị sàn bỏ, không cần coi mọi phần ở §15 là chưa biết từ đầu. So V002 với V082 ở CPU-BOOK-2 và ca đúng CPU-BOOK-1: chú thích H8-san và năm dòng hạng đầu trùng. Kiểm tương tự bốn ca được sàn đưa về NO_INTRINSIC_ANOMALY (729604d2 và ba ca T-062): trùng, không còn cờ. Có thể dẫn lại Q6 và bảng nền khi hoàn thiện hồ sơ. Sàn **bỏ cờ/đặt e=0** cho hướng vượt nhỏ, không trực tiếp thay mẫu số chuẩn hóa; câu ứng viên ở §15 không thay cơ chế đã có bằng chứng.
7. **Độ nhạy:** các số §16 khớp output; V082 giữ AC@3=11/11 ở sáu mốc của tập chọn, không kém P7 trên các tổng được nêu. Không chuyển phép dời mốc thành phép lặp hay đánh giá độc lập. Lý do riêng của những ca mới tại +30 chưa được bảng tổng tự phân xử.

## Phần còn mở và bằng chứng phân xử

Các mục dưới giữ nghĩa vụ nghiên cứu và giới hạn kết luận. Không phải lệnh phát thêm thí nghiệm trong lượt này. Claude chuẩn bị phạm vi/chi phí; Minh quyết các phần cần thu hoặc chạy ngoài phép đọc hiện có.

| Phần | Vì sao chưa phân xử; giải thích còn lại | Bằng chứng tiếp theo và dữ liệu | Chi phí, kết luận phụ thuộc |
|---|---|---|---|
| H3/H4 | Hai ô chuyên biệt đã hạng 1 với P7. Điểm không tăng phù hợp cả với trần độ đo lẫn thành phần chưa cung cấp tín hiệu định vị hữu ích. | Trước hết đọc kênh/trung gian đã lưu trên POOL-EVENT và CONSUMER cùng đối chứng. Để khẳng định lợi ích xếp hạng cần ca **dev** có tín hiệu tương ứng mà P7 chưa xếp đúng; thiết kế ô phải có lý do ngoài đáp án, không lấy ô đánh giá. | Phần đọc ở mức phút–vài chục phút; nếu cần thu, chu kỳ cũ khoảng 30 phút/ô, chưa tính thiết kế/chuẩn bị. Chưa chốt số ô nên chưa có tổng chi phí. Ảnh hưởng kết luận hiệu quả riêng H3/H4, không tự bác lựa chọn bỏ chúng hiện tại. |
| Sàn 1 ms | Q6 đã phân xử đường mất cờ và đảo hạng, nhưng chưa xác lập ranh giới vật lý nhiễu/lỗi hoặc đáp ứng K gần 1 ms. Dịch nhỏ có thể là lỗi thật hoặc dao động nền. | Nếu cần quyết sàn khác, phân tích giá trị vượt đã lưu và khai phép so các giá trị sàn trên dev; nếu hỏi dao động giữa lần thu thì cần dữ liệu lặp mới. | Đọc đầu ra chỉ vài phút. Một cấu hình 28 ca có mốc tham chiếu khoảng 22 phút theo tổng summary V082; không phải dự toán quét chưa thiết kế. Chưa có số mức/lần thu nên tổng còn cần trình. Ảnh hưởng đổi ngưỡng và khẳng định bền vững, không biến ngưỡng thực dụng thành định luật. |
| Ca nền cũ và ca ×3 mới | Q4 chưa tách ảnh hưởng thời điểm của autovacuum/checkpoint, chờ khóa ngắn và dao động tín hiệu; ca ×3 mới còn đường CPU riêng ở R10. Đếm cả cửa sổ hoặc lỗi giao dịch bằng 0 chưa phân xử latency và nguyên nhân cờ. | Đối chiếu thời điểm kênh với log/trace/metric và latency N/A của các gói dev đang có, gồm ca đúng tương ứng. Nếu thời lượng chờ khóa không từng được ghi thì dữ liệu cũ không thể khôi phục riêng cơ chế đó; cần đề xuất quan sát/thu phù hợp hoặc giữ giới hạn. | Đọc/đối chiếu cũ ở mức phút–vài chục phút; chi phí thu mới phụ thuộc tín hiệu và số ô, chưa có thiết kế được trình. Ảnh hưởng diễn giải vì sao K còn cao; K thô vẫn giữ. |
| Các ca mới tại +30 s | Bảng tổng xác nhận tụt điểm; chưa tách theo từng ca việc N lẫn lỗi, đổi đơn vị/cổng suy biến hoặc điều kiện liveness. R9 đã chỉ ra thêm một sai lệch ngữ nghĩa nguồn. | Đọc ngưỡng, cờ và thứ hạng trong output d=0/+30 cùng mẫu N/A từ gói dev đã lưu. Chỉ nếu thiếu trung gian mới trình đúng phần cần tính bổ sung; không chạy lại toàn bảng để diễn giải một tổng. | Phần đọc ở mức vài chục phút; chưa biết có cần tính bổ sung. Ảnh hưởng quy nguyên nhân và yêu cầu với mốc cảnh báo trực tuyến, không ảnh hưởng việc bảng độ nhạy hiện tại khớp số. |
| Hiệu quả giữ ngoài, baseline và dao động qua lần thu | Dữ liệu hiện tại đã dùng thiết kế/chọn và chủ yếu một lần thu. Có thể có lợi thật hoặc khớp riêng tập dev; số này không phân xử được. Baseline được Minh để sau khi khóa. | Gói đánh giá sau khóa trên dữ liệu được phép, baseline tiêu biểu theo quyết định sau và phép lặp khi được duyệt. | Chưa chốt baseline/số ô/số lần thu nên không có căn cứ cho tổng thời gian. Ảnh hưởng RQ5 và khẳng định hiệu quả độc lập; không yêu cầu hoàn thành gói ấy để xử lý hai finding hiện tại. |

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** soát phần thay đổi sau REVIEW-3, tính độc lập, kiểm toàn vẹn và truy nguồn liveness tới mẫu gốc; đối chiếu từng finding/phản hồi cũ và nguồn đề tài.
2. **File đã thay đổi:** chỉ tạo `tasks/T-064-m1-flashticket/REVIEW-4.md`, gồm prompt bàn giao; không đổi quyết định hay file khác.
3. **Kiểm đã chạy:** các phép đếm/hash/chấm chỉ đọc nêu trên; các tổng và bản xuất khớp. Python local không khởi chạy được trong sandbox; dùng Node cho kiểm độc lập và Python trên exp-obs chỉ để đọc/hash/truy vấn lịch sử. Không chạy lại M1.
4. **Còn mở và điều cần Minh quyết:**
   - **Đề xuất A cho R9:** xử lý đúng ngữ nghĩa liveness, giữ V082 cũ làm lịch sử; người làm khoanh đầu vào/kết quả chịu ảnh hưởng và trình phần sửa/tính lại cụ thể. Lợi: khôi phục đúng điều kiện của H5b trên ca đã có. Mặt trái: đổi pin và có thể đổi bảng chọn/độ nhạy, cần giữ bản lịch sử. Đã xét phương án chấp nhận bản hiện tại như quy tắc nhớ lỗi; phương án đó thay nghĩa và giữ lỗi nhận chết im, nên không ưu tiên.
   - **Đề xuất cho R10:** hoàn thiện phân tích/chú thích trên dữ liệu đã có, giữ nguyên K. Lợi: đáp đúng yêu cầu mọi ca không tiêm lỗi mà không cần thu/chạy thêm; hạn chế: nguyên nhân vật lý của CPU vẫn có thể OPEN. Nếu thiếu dữ kiện phân xử, trình đúng phần thiếu cùng các giải thích còn lại và chi phí, không quy thành “do tải” từ tên ca.
   - **Khoa học còn mở:** tác dụng H3/H4 khi P7 đã xếp đúng, hiệu quả giữ ngoài/dao động qua lần thu, nguồn dao động các ca nền và cơ chế từng ca dời mốc. Không lấy chúng làm bằng chứng phương pháp đã tốt hơn baseline hay đã trả lời RQ5. Ô pool/queue mới để phân xử hiệu quả hoặc chạy lặp là việc nghiên cứu tiếp phải có đề xuất riêng; không buộc thực hiện trong lượt review này.
   - **Quyền đã có:** không cần Minh chọn lại thứ tự §5. Minh quyết cách xử lý lỗi mới, phần sửa và thời điểm nhận M3/M4; việc đã chọn ứng viên không tự là nghiệm thu.

**Đề xuất chưa dừng phản biện ở trạng thái hiện tại.** Cần người làm đáp R9 trên file/code/mẫu thật và xử lý phần hồ sơ R10; sau đó Minh quyết sửa, chấp nhận giới hạn hay kiểm lại phần ảnh hưởng. Không yêu cầu lặp lại toàn bộ chiến dịch. Các sửa R6–R8 đã xác nhận, giữ kết quả kiểm ấy để dùng lại. Không tự mở lượt mới hay đóng task.

## Prompt bàn giao cho người làm

Prompt chung và khối Người làm đáp phản biện dưới đây được chép từ mẫu hiện hành, chỉ điền thông tin trung tính. Giai đoạn 2 không có khối trọng tâm cổng riêng; không tự thêm khối G3/G4. Minh chọn chuyển hoặc dừng; reviewer không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/); người làm đáp REVIEW-4.md và đánh giá các đề xuất trong bản này.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, M3; M4 chưa đóng; giai đoạn 2 không có khối trọng tâm cổng riêng trong docs/review-prompt.md.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (SPEC T-064).
- Tài liệu gốc: tasks/T-064-m1-flashticket/SPEC.md, LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md, CHECKPOINT-CHIEN-DICH.md; results/T-064/tieu-chi-chon.md, ho-so-chon.md, so-bien-the.jsonl; docs/WHY.md, docs/DECISIONS.md; commit gốc c3d27f8a, đầu ra chưa commit.
- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW.md, REVIEW-2.md, REVIEW-3.md và các bảng phản hồi; REVIEW-4.md.
- Code và kết quả liên quan: results/T-064/manifest.json; src/m1_ft/, src/m1/, src/p3/danh_gia.py; results/T-064/cham/, kiem/luot5/, kiem/nhan-luot5/, phan-tich/, phien-c/, chu-thich-thao-tac-nen.md, cau-hinh-de-xuat.json, ban-xuat/; results/T-063/manifest.json, thu3/manifest.json, thu3/xac-nhan-ca-3-sua-sau.json, thu3/BAN-GIAO-B.md, dong-goi/xuat_bo_sung.py; cách gọi exp-obs ở results/T-063/thu3/CHECKPOINT.md, chỉ đọc, không in khóa hoặc ghi máy; kiểm hash trước khi dùng nguồn.
- Phạm vi ghi được Minh cho phép trong lượt này: theo SPEC và quyền chiến dịch đã duyệt: ở công đoạn đáp, chỉ điền bảng Phản hồi của người làm cuối tasks/T-064-m1-flashticket/REVIEW-4.md và nối mục mới tasks/T-064-m1-flashticket/LOG.md; giữ nguyên nhận xét và prompt của reviewer. Trình phản hồi, đề xuất sửa và phạm vi tính lại trước khi thực hiện phần sửa ngoài công đoạn đáp.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.
```

```text
Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hay prompt của người phản biện. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Để trống cột Minh quyết. Prompt của lượt đáp nằm trong mục LOG mới hoặc chat.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R9 | Đúng; CHẶN (kiểm đúng đắn H5b, xác nhận M3) | Tự kiểm ~01:40Z: `kiem/nhan-luot5/l5/dev3/d0/V082-V066+H8a/ebd5ef38/method-output-1.json#/extra/m1_ft/chu_thich/H5-liveness/chet_im/thanh_phan/payment-service` = {tu 1794651115, den 1794651400, so_mau 20}; `results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/ebd5ef38/httpcheck_error_8083_mau_tho_tuong_doi_t` = [3,13,23,33,43]. Người làm đã biết điều kiện thất bại này (WHY-93, từ BAN-GIAO-C §4d, "chưa kiểm hệ quả") nhưng hồ sơ §15 và WHY-98 không nêu — lỗi bỏ sót của người làm, không chỉ lỗi dữ liệu. Nguồn lỗi ở bộ xuất (`max(httpcheck_error)` qua `query_range` giữ mẫu cũ trong lookback), không ở logic `_chet_im`. Đề xuất (chờ Minh): (1) chỉ đọc: chạy biểu thức sửa `max by(http_url)(max_over_time(httpcheck_error[15s])) or (0 * max by(http_url)(httpcheck_duration_milliseconds))` trên Prometheus cho 28 ca × 6 mốc, so với kênh `live-down` đã lưu để biết slot nào đổi; (2) chỉ xuất lại gói và chạy lại các slot có kênh đổi, cho mọi bản có H5/H5b, thư mục đầu ra mới; (3) chấm lại, bản 3 chỉ mục/cấu hình/hồ sơ, WHY mới. Không sửa `src/m1_ft` và bộ xuất T-063 đã ghim (bộ xuất mới ở `results/T-064/kiem/`). | |
| R10 | Đúng; KHÔNG CHẶN | `chon-dev3-d0-v082-A.json#/ban/V082-V066+H8a/chon/ca/1e5a3dc5` k = 1; ca không có trong `chu-thich-thao-tac-nen.md` hay ghi chú cơ chế. Sửa tối thiểu như đề xuất: thêm mục cho ca này (kênh → cổng → F_I → verdict; đối chiếu 7d1ee32f và k6), tách điều đã lần với khả năng còn lại; làm cùng lượt sửa R9 nếu Minh duyệt. | |
| R9 (bổ sung 01:44Z) | Đính chính đề xuất sửa của người làm ở dòng R9 | Biểu thức `max_over_time(httpcheck_error[15s])` đề xuất ở dòng trên **sai**: phép kiểm chỉ đọc `results/T-064/kiem/r9/so-live-down.json` cho thấy nó làm mất chết im ở PAUSE-PAYMENT 46aab4be (request treo, đầu dò ghi lỗi mỗi ~30 s). Đề xuất thay: kênh live-down theo "lần dò mới nhất" (1 nếu kết quả dò gần nhất trước bước là lỗi, 0 nếu là phản hồi; dựng từ mẫu thô `httpcheck_error`, `httpcheck_status`). `so-live-down-2.json`: 134/140 gói không lệch điểm; chỉ 6 gói ebd5ef38 lệch, chết im mất ở 5 gói (d −60…+15); 46aab4be giữ ở mọi mốc. Slot cần chạy lại: 12 (ebd5ef38 × bản có H5 + H8a). Chờ Minh. | |
