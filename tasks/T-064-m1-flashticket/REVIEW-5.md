# Phản biện T-064 — lượt 5

- **Người phản biện:** Codex. **Ngày:** 15/11/2026. **Ý định:** REVIEW.
- **Commit/diff đã đọc:** HEAD trùng commit gốc của brief; đầu ra chiến dịch chưa commit. Đọc diff bộ chấm trước/sau R9, chỉ mục bản 2/3, cấu hình đề xuất và đầu ra gốc.
- **Công đoạn/cổng và bản lượt:** kiểm lại phản hồi và sửa sau REVIEW-4; chiến dịch M1-FlashTicket, M3, còn M4. Claude làm, Codex phản biện. Đã liệt kê thư mục; chưa có REVIEW-5.md. Chỉ ghi bản mới này.
- **Đã đọc:** AGENTS; STATE; SPEC và phần cuối LOG T-064; chiến dịch mục 4–7, checkpoint; phần mục tiêu/RQ, P10 và nguyên tắc MRP; DT18, hướng dẫn cô; LESSONS; WHY-81–99 và DECISIONS phần chiến dịch. Đầu ra: tiêu chí, hồ sơ chọn mục 14–17, sổ biến thể, tập chọn/đáp án, ghi chú cơ chế Q6/Q7, chú thích nền, hợp đồng, cấu hình đề xuất, chỉ mục, manifest và script liên quan. Code: đường chạy/đọc bổ sung, H5, H8-sàn, H1, đối chứng quan hệ, bộ chấm và các script R9. Sau tự soát mới đối chiếu các finding/bảng phản hồi REVIEW đến REVIEW-4.
- **Tự soát độc lập:** kiểm hash trước; lần mẫu đầu dò gốc → bundle → H5b → đầu ra → bộ chấm → chỉ mục. Tính điểm độc lập bằng JavaScript. Kiểm riêng trung gian hai ca bình thường bản 3. Nhận xét trước khi mở các bản phản biện: sửa liveness khớp hai tình huống thật, điểm không đổi trong các bảng đã so, cờ CPU được mô tả đúng; manifest hiện hành có một hash lệch ở log của lượt R5. LOG không thay bằng chứng trên file.

## Kết luận chung

**FACT:** R9 đã xử lý đúng lỗi được nêu trên dữ liệu dev liên quan; gỡ điểm CHẶN về H5b của REVIEW-4. R10 đã bổ sung đủ phần hồ sơ được Minh duyệt: lần được kênh → cổng → cờ tự sinh → verdict, có đối chứng và tách nguyên nhân CPU còn OPEN. Không có lỗi khoa học mới trong phần sửa đã kiểm. Có một điểm toàn vẹn **KHÔNG CHẶN** R9/R10, ghi ở R11.

**DECIDED, giữ nguyên nguồn quyết định:** Minh đã chọn ứng viên V082 và duyệt sửa R9/R10 trong DECISIONS. Điểm hiện hành của V082 vẫn AC@1 = 9/11, AC@3 = 11/11, tổng hạng cắt 13, K = 4/6; T-062 là 5/5, 5/5, K = 1/4 (cham/chon-dev3-d0-v082-r9-A.json#/ban/V082-V066+H8a/{chon,t062}). Lượt này đủ căn cứ kết thúc kiểm sửa R9/R10. Không tự nghiệm thu toàn task/M4, khóa thiết kế hoặc trả lời RQ5.

## Các điểm

### R11. Manifest ghim log R5 trước khi log ổn định — KHÔNG CHẶN kiểm sửa R9/R10

- **Ở đâu:** results/T-064/manifest-2.json#/file/codex~1R5-lan1.log; file results/T-064/codex/R5-lan1.log; LOG T-064 mục 03:55Z và 03:57Z.
- **Sai gì — FACT:** bản kê hiện hành đã chứa log R5, nhưng hash byte hiện tại của log khác hash trong bản kê. Không thể báo toàn bộ manifest-2 đang có “0 lệch”. Lượt này không dùng nội dung log ấy làm bằng chứng.
- **Bằng chứng:** Node đọc và băm đầy đủ 7.668 mục file, 9 mục ngoai_T064 và 18 mục src_m1_ft: 7.694/7.695 tham chiếu khớp, không thiếu file; lệch duy nhất đường dẫn trên. Các mục ngoài có thể lặp file đã ghim trong nhóm khác, nên đây là số tham chiếu kiểm hash. Manifest ghi utc 03:55:38Z; mtime log là 04:05:31Z. LOG ghi đã lập lại manifest sau khi R5 bắt đầu. Kiểm lại trước khi viết bản này vẫn thấy đúng một lệch. Hash cụ thể giữ ở manifest và kết quả lệnh, không chép lại vào văn bản.
- **Phần có thể phản bác:** đây là log phát sinh trong lượt phản biện, không phải code, gói dữ liệu, summary hay bảng điểm. Toàn bộ những nguồn khoa học được dùng ở lượt này khớp pin. Không có căn cứ gọi đây là dữ liệu khoa học hỏng hoặc yêu cầu chạy lại M1. Việc manifest được lập lại đã được LOG công khai, không phải thay đổi bị che.
- **Bước và quyết định chịu ảnh hưởng:** đóng gói/kiểm toàn vẹn khi bàn giao M4. Không chặn lựa chọn ứng viên hay gỡ R9; chỉ ngăn xác nhận bản kê hiện hành khớp toàn bộ byte hiện tại và việc dùng log R5 qua pin ấy.
- **Đề xuất tối thiểu — CANDIDATE, Minh quyết:** sau khi log R5 ổn định, lập results/T-064/manifest-3.json bằng cơ chế lập bản kế tiếp đã có; giữ manifest-2 làm lịch sử và ghi rõ lý do thay bản kê. Không sửa ngược hash hoặc xóa log. Kiểm lại toàn bộ bản mới rồi dùng nó cho M4. Chi phí là đọc/băm file, không phát thực nghiệm; lượt băm trong phiên này mất khoảng 3 giây, chưa phải cam kết thời gian trên mọi máy.
- **Pin và tác động:** manifest-2 đã ghim manifest.json trước đó và các nguồn ngoài; sửa byte manifest-2 làm mất snapshot được review ở lượt này. Script kiem/tao_manifest_t064.py đã có cơ chế chọn tên manifest kế tiếp, nên đề xuất không cần sửa script hay nguồn khoa học. Phương án chỉ miễn kiểm log đang thay đổi giữ được kiểm phần khoa học trong phiên này, nhưng để lại bản kê không khớp khi bàn giao; tôi ưu tiên bản kế tiếp sau khi log ổn định.

## Đối chiếu các lượt trước

| Điểm/phản hồi | Đánh giá hiện tại và bằng chứng riêng |
|---|---|
| R9, gồm dòng bổ sung bác biểu thức max_over_time[15s] | **Đúng; sửa đạt phạm vi được duyệt.** Mẫu thô RECREATE-PAY có lỗi t+3,211…43,204 s và phản hồi lại t+53,207 s. Bundle mới d=0 chỉ có live-down=1 tại t+15,30,45; từ +60 trở lại 0. PAUSE-PAYMENT có lỗi mỗi khoảng 30 s và không phản hồi lại trong A; dựng theo lần dò mới nhất khớp bundle đã lưu, vẫn nhận chết im. Do đó việc bỏ biểu thức cửa sổ 15 s là có căn cứ, không chỉ sửa để giữ điểm. |
| Phản hồi R9 về phạm vi chạy lại | **Đúng.** File viec-r9.txt có 12 cặp; nhận đủ 12 summary, hai output của mỗi cặp bằng byte và khớp summary. Tất cả dùng đúng gói mới theo hash trong summary#/moc/bo_sung; H5b không còn ghi thành phần chết im ở RECREATE-PAY, Payment vẫn hạng 1. Đây là 12 slot duy nhất được 26 lượt tham chiếu trong hai bảng A: tập chọn và tập độ nhạy có phần lặp; không phải 26 ca thu độc lập. |
| Phản hồi R9 về không đổi điểm và nguồn chấm | **Đúng, đúng đại lượng được nêu.** Sáu file .txt trước/sau bằng nhau. JSON bảng chọn/dời mốc chỉ đổi goc_uu_tien và nguon/sha256 của slot chạy lại; giữ/bỏ chỉ đổi đường dẫn nguon. Từng hạng, p1, p3, k, verdict, nhóm đầu, bảng cạnh, tổng, luật giữ và thứ tự §5 giữ nguyên. Chỉ mục 3 đổi đúng hai slot ebd5ef38 của V082/V071 cùng metadata phiên bản. Không suy thành toàn bộ output bằng byte: byte và trung gian H5b đã đổi. |
| R10 và phản hồi | **Đúng; đã xử lý phần thiếu.** Q7 và chú thích nền mục 5 khớp đầu ra 1e5a3dc5/7d1ee32f. Kiểm 41 bản trong bảng chấm d=0: 41/41 của mỗi ca có cờ CPU Payment tự sinh. Riêng V082 mỗi ca có đúng một cờ tự sinh; ngưỡng, đuôi, p và s khớp bảng mới. K vẫn đếm thô. Không có căn cứ quy riêng cho tải ×3 hoặc tuyên bố latency giao dịch không đổi. |
| R1 — phân loại cạnh HTTP/message | **Đúng; giữ xác nhận đã sửa.** H1 hiện tách kind trước chấm. File H1 khớp cả pin manifest trước R9 và pin hiện hành; R9 không sửa nó. Điểm cạnh được tính lại độc lập từ các output hiện hành, không lệch. Không chạy lại phép đếm trace đã hợp lệ ở lượt trước. |
| R2 và R6 — bỏ H1 khác bỏ quan hệ; V051 còn H1 | **Đúng; diễn giải đã thu hẹp đúng.** V051 vẫn có H1; V066 bỏ H1 và V067 thêm tắt E1/E2/E5. Cấu hình DC không xóa vùng E7 trong output, nên “bỏ toàn bộ” chỉ áp cho đường xếp hạng đang so. Các tổng trong bảng quan hệ giữ nguyên sau R9. Không khẳng định lợi ích của cấu trúc thật hoặc tách được đóng góp riêng E1/E2/E5. |
| R3 và R8 — WHY, thời điểm và ngưỡng thực dụng | **Đúng; giữ cách khai lịch sử.** WHY-85/86 và WHY-94 ghi bổ sung muộn, không có hiệu lực ngược; 1 ms vẫn là ngưỡng thực dụng. WHY-99 nêu ngữ nghĩa mới, phương án bị bác, dữ liệu hai ca và việc sửa sau khi xem dev. Không nâng giả thuyết CFS thành FACT, không nhận đã rà lại toàn bộ lý do của mọi hướng bị loại trong lượt R5. |
| R4 và S5 trong LOG — quyền áp §5 | **R4 đúng; S5 đọc thiếu nguồn.** DECISIONS mục “Bổ sung quyền điều phối…” dòng 579 và 583 đã cấp áp tiêu chí và xử lý các mục chờ cũ. Không cần Minh duyệt lại thứ tự hiện hành. Minh chọn V082 là quyết định ứng viên cụ thể; không phải nguồn duy nhất của quyền áp §5. |
| R5 — câu không hồi quy | **Đúng; không mở lại câu đã sửa.** Tính lại T-062 hiện hành vẫn thấy H1a/H1b bị loại có AC@1 thấp hơn P7. V082 và V071 không hồi quy tại d=0; câu đó không áp cho mọi biến thể/mốc dời. |
| R7 và N1 của REVIEW-3 — dời mốc | **Đúng; đính chính giữ được phân biệt.** Hồ sơ §14 nêu mất ưu tiên hạng 1 khác mất mọi lợi thế; bảng dời mốc hiện hành khớp từng ca và K. Không xác nhận giả thuyết N lẫn lỗi cho mọi ca +30 s. |
| N1 về giờ ước lượng; N2 về sát sàn; pin bộ chấm lịch sử | **Đúng phần quan sát/đính chính; giới hạn còn giữ.** Không dùng giờ ước lượng làm bằng chứng mới. Các giá trị sát sàn không xác định đường đáp ứng K quanh 1 ms; chưa quét thì chưa kết luận độ nhạy cục bộ. Không ghi lại pin bộ chấm lịch sử bằng hash hiện tại. |

### R9 — kiểm đầu vào và trung gian

Đã đọc exp-obs qua Git OpenSSH theo nguồn gọi máy trong thu3/CHECKPOINT.md và helper của repo; chỉ đọc/hash/truy vấn lịch sử, không ghi máy hay chạy phương pháp. Đối chiếu riêng hai ca d=0 với mẫu thô qua API query, dùng range vector của httpcheck_error/httpcheck_status, lấy mẫu có giá trị 1 và chọn timestamp mới nhất không quá 300 s trước bước:

- RECREATE-PAY: 0 điểm khác giữa phép dựng độc lập và bundle R9, trên mọi URL trong bundle.
- PAUSE-PAYMENT: 0 điểm khác với bundle cũ; Payment lỗi mỗi khoảng 30 s, nên khoảng lấy max 15 s bỏ sót trạng thái giữa hai kết quả dò.
- Trên cả 6 bundle R9, hash nguồn cũ đúng nguon_r9/gói cũ; mọi bundle ngoài live-down và metadata cửa sổ giữ nguyên; loi_khuc rỗng. Hash 6 bundle trên máy trùng bản đã nhận và pin T-064.
- File so-live-down-2.json đã khớp manifest: 149 gói, 9 không có kênh, 140 có kênh; 134 không đổi điểm, 6 ebd5ef38 đổi, 5 đổi điều kiện chết im. Đây là phép đếm đủ file kiểm đã lưu; phép dựng độc lập trực tiếp trên Prometheus ở lượt này thực hiện trên hai ca d=0 như trên.

Tách lỗi đã xảy ra khỏi giới hạn: lỗi cũ thuộc bước chuyển đổi ngữ nghĩa tín hiệu. Bản sửa không chứng minh H5b bền vững với mọi lỗi mạng/collector hoặc mọi ngưỡng. Các điều kiện thất bại đã nêu ở WHY-86 vẫn còn. Quy ước lookback được đối chiếu thêm với [tài liệu Prometheus](https://prometheus.io/docs/prometheus/latest/querying/basics/#staleness); kết luận sửa dựa trên mẫu và bundle thật.

### R10 — phần đã lần và phần chưa phân xử

Nguồn: kiem/nhan-luot5/l5/dev3/d0/V082-V066+H8a/<ca>/method-output-1.json#/extra/{kenh_co,don_vi_phan_vi}:

| Ca | Cờ tự sinh của V082 | s | Đuôi lên N → A | h | p_len |
|---|---|---:|---:|---:|---:|
| 1e5a3dc5 | payment-service_cpu | 2,764567 | 0 → 0,05 | 0,0815899 | 0,00396825 |
| 7d1ee32f | payment-service_cpu | 3,608279 | 0 → 0,85 | 0,0425537 | 0,00396825 |

Mỗi phía có 20 mẫu. Cờ là lớp khong_lan, F_I=1; sàn H8 chỉ áp span nên không lọc CPU. Đây là đường phương pháp dẫn tới CAUSE_FOUND đã xác định, không phải chứng minh nguyên nhân vật lý của CPU.

Đã kiểm pin xac-nhan-ca-3-sua-sau.json và BAN-GIAO-B.md theo manifest-2 của thu3. Nguồn #/ca/<ca>/k6 ghi 6.481 journey ở ×3 và 2.161 ở ×1; journey_failed, drop và lỗi refresh đều bằng 0 ở hai ca. Số đếm không thay phép đối chiếu latency N/A. Q7 giữ đúng giới hạn ấy.

## Tuân thủ quy trình

- Quyền sửa R9/R10 có trong DECISIONS ngày 15/11. Các đầu ra sửa nằm trong phạm vi đó; giữ bundle/output/cấu hình/chỉ mục và bộ chấm trước sửa. Không lấy phản biện làm lệnh tự cấp quyền.
- Diff cham_dev3 trước/sau chỉ thêm goc_uu_tien và tài liệu cho đường đó. Hai spec dùng đúng thư mục R9; nguồn thực tế của cả 26 tham chiếu đã đối chiếu hash. Tiêu chí chấm không đổi.
- Nhãn chỉ ghép trong bộ chấm. Script R9 chọn đúng ca chịu ảnh hưởng để sửa đầu vào; phép tính trạng thái trong bundle dùng cùng quy tắc cho mọi URL, không dùng đáp án, tên ô hay thành phần gốc. chay_ca chỉ truyền bundles vào phương pháp; metadata nguon_r9 không đi vào tính điểm.
- Không có thay đổi src/m1 hay src/p3 so với HEAD. Các pin src/m1_ft của manifest hiện hành khớp. Việc sửa nguồn gói làm đổi hash đầu vào và byte output; không được giấu dưới câu “điểm không đổi”.
- STATE vẫn ở mốc cũ và LOG đã tự khai điều đó; brief lượt này xác định rõ công đoạn hiện hành. Dùng brief/quyết định và đầu ra để kiểm phần sửa, không sửa STATE thay người làm. Khi bàn giao M4, người làm còn nghĩa vụ đồng bộ trạng thái/checkpoint và ghi kết phiên theo quyền.
- LOG có dấu vết tự soát trước đọc REVIEW-4, bác đề xuất max_over_time 15 s bằng phép kiểm, rồi thực hiện phần sửa được Minh duyệt. Mục 03:57Z ghi việc lập lại manifest; hệ quả còn lại là R11.
- Lượt R5 này chỉ tạo REVIEW-5.md; không ghi LOG/STATE, không sửa bản cũ, không commit, không phát thực nghiệm hoặc mở dữ liệu khóa.

## Điều đã kiểm và thấy đúng

Các phép tính độc lập dùng Node, không phải chạy lại Python/M1. Python local không khởi chạy được trong sandbox; không đổi quyền/môi trường để chạy. Python qua SSH chỉ đọc/hash/đối chiếu telemetry.

| Phép kiểm | Kết quả |
|---|---|
| Manifest hiện hành | 7.694/7.695 tham chiếu khớp; 0 thiếu; lệch duy nhất log R5, R11 |
| NHAN-R9.sha256 và nội dung r9.tgz | 2/2 mục receipt khớp; 42/42 file trong archive bằng byte file đã giải |
| 12 slot R9 | 12/12 cặp hai output bằng byte và khớp summary; hash cấu hình/code/đầu vào đúng; t_mới=t_gốc+d; không còn chết im sai |
| Tính lại bảng chọn và dời mốc A | 195 bảng bản–tập, 2.925 tham chiếu ca: hạng, top1/top3, K, tổng và bảng cạnh khớp trong 1e-9; hash output được dẫn khớp |
| So trước/sau R9 và A/B | 6 file .txt bằng byte bản trước; JSON chỉ đổi metadata nguồn đã nêu; hai đáp án cho cùng điểm/giữ-bỏ |
| Chỉ mục 3 | 84 slot, 83 output thật và 1 lỗi P7; 83/83 hash output khớp; metadata cấu hình/code của 56 output hai bản FT khớp; chỉ hai slot ebd5ef38 đổi |
| R10 | Cờ CPU có ở 41/41 bản cho mỗi ca; số của V082 trong hai tài liệu khớp output và k6 đã ghim |
| P7 và nguồn phương pháp | Diff src/m1, src/p3 rỗng; code hiện hành khớp pin dùng cho phần sửa |

195 bảng = (41 bản d=0 + 24 bản/mốc của bảng độ nhạy) × 3 tập. Các tập có ca trùng; 2.925 là số tham chiếu được kiểm, không phải số ca độc lập. Điểm min hạng tập chấp nhận được tính dưới hoán vị đều nhóm hòa; áp phép chiếu cạnh đã khai trước khi tính, K đếm thô.

Lệnh/phép tính đã chạy, đủ để nhận diện phạm vi kiểm:

    git rev-parse HEAD
    git diff --stat -- src/m1 src/p3
    git diff --no-index -- results/T-064/cham/cham_dev3_truoc_r9.py results/T-064/cham/cham_dev3.py

Qua Node: đọc các mục file/ngoai_T064/src_m1_ft của manifest-2, băm SHA-256; giải gzip/tar trong bộ nhớ và so byte 42 file; duyệt hai JSON chon-dev3-d0-v082-r9-A và doi-moc-dev3-r9-A, đọc từng nguon/method-output-1.json, tính nhóm hòa/phép chiếu và tổng; so các khóa số trước/sau và kiểm các mục chỉ mục. Không tạo script hoặc file kiểm ngoài phạm vi review.

Qua SSH: đọc 6 bundle R9 và bundle gốc do nguon_r9 trỏ; so hash/bundle; đọc API localhost:9090/api/v1/query cho httpcheck_error/httpcheck_status với cửa sổ từ S−300 tới E của hai ca d=0, dựng lại theo timestamp mới nhất. Lệnh chỉ in JSON kết quả, không in khóa truy cập.

## Phần còn mở và bằng chứng phân xử

Đây là giới hạn của câu trả lời nghiên cứu, không tự là finding hoặc lệnh phát thêm việc.

| OPEN và quyết định phụ thuộc | Vì sao còn mở, giải thích khác | Bằng chứng/chi phí và đề xuất |
|---|---|---|
| Nguồn đổi CPU ở hai ca bình thường bản 3; diễn giải một phần K | Đã xác định đường gây verdict, chưa đối chiếu thời điểm CPU với job/outbox và latency. Việc nền, dao động bình thường/cổng, hoặc hiệu ứng đợt triển khai vẫn có thể giải thích. Không được đổi “chưa làm đối chiếu” thành “không thể phân xử”. | Đọc chuỗi CPU, log job/outbox, latency N/A của hai ca và các đoạn N bản 3 đã lưu trên exp-obs. Ước lượng chưa đo: vài chục phút phân tích, 0 lượt M1/thu mới cho bước đọc. Đề xuất giữ K, giữ nguyên nhân vật lý OPEN như Q7; nếu cần quy nguồn để đổi thiết kế/quan sát thì trình phần phân tích ấy. Mặt trái: chưa giải thích được tác nhân CPU. |
| H3/H4, ngưỡng sàn, các ca nhạy mốc | Điểm trần ở ô pool/queue không tách được trần độ đo với thiếu tín hiệu định vị; ngưỡng sàn và dời mốc không đo được dao động qua lần thu. Q6 đã lần mất cờ, còn các nguyên nhân +30 s chưa được tách đủ từng ca. | Giữ các phụ thuộc và đề xuất ở REVIEW-4 mục “Phần còn mở”; dùng trung gian cũ trước. Chỉ đề nghị thu/dev mới hoặc quét tham số khi cần trả lời lựa chọn cụ thể, có phạm vi/chi phí. Không lấy những OPEN này làm bằng chứng thành phần vô ích hay đồ thị đã có lợi giữ ngoài. |
| M4 và RQ5 | Hai slot hiển thị T-065 còn cần theo chỉ mục 3; bản dev chưa khóa/đánh giá độc lập, baseline và lần thu lặp chưa thuộc bằng chứng này. | Tiếp tục bàn giao G-c, trạng thái và manifest theo quyền chiến dịch. Giữ đề xuất V082; chưa khẳng định hơn baseline hay hiệu quả giữ ngoài. Chưa chốt thiết kế/số ô cho đánh giá nên chưa có căn cứ ước tổng chi phí. |

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập nguồn, đầu vào, trung gian và điểm sau sửa R9/R10; đối chiếu từng finding/phản hồi cũ và giới hạn mục tiêu nguồn.
2. **File thay đổi:** chỉ tạo tasks/T-064-m1-flashticket/REVIEW-5.md, gồm prompt bàn giao và bảng phản hồi để trống. Không thêm/thay quyết định.
3. **Kiểm và kết quả:** các phép đếm/hash/tính điểm ở trên. Gỡ R9; R10 đạt phần hồ sơ sửa. Không có lỗi khoa học mới; có R11 không chặn phần sửa.
4. **Điều cần Minh quyết:** đề xuất nhận phần sửa R9/R10 và dừng vòng phản biện này; xử lý R11 bằng manifest kế tiếp khi log ổn định trước bàn giao M4. Lợi: không chạy lại phần khoa học đã hợp lệ, có bản kê khớp lúc bàn giao. Mặt trái: nguyên nhân vật lý CPU và các OPEN nghiên cứu vẫn chưa được trả lời; dừng review không làm chúng thành FACT. Phương án tiếp tục phát lô/review chỉ vì điểm không đổi không bổ sung bằng chứng còn thiếu, nên không ưu tiên.

**Đề xuất dừng phản biện phần phản hồi và sửa này.** Không còn phản đối chưa xử lý về tính đúng hay phạm vi kết luận của R9/R10. R11 khoanh riêng việc toàn vẹn bàn giao; không cần chạy lại M1 hoặc một vòng phản biện khoa học chỉ để lập lại bản kê. Minh quyết cuối về xử lý R11 và nhận M3/M4. Hai agent đồng ý không thay bằng chứng; không tự đóng task, duyệt khóa/mở test hoặc mở lại task đã đóng.

Nội dung cần vào hồ sơ chính thức: trạng thái R9/R10, ngữ nghĩa liveness khi triển khai, bản kê dùng cho M4, và phần CPU/hiệu quả còn OPEN. Đã có nghĩa vụ bàn giao của người làm; reviewer không ghi thay. Nếu Minh yêu cầu lưu commit cho bản phản biện này, nội dung đề xuất là “docs(T-064): thêm phản biện lượt 5”; lượt này không commit.

## Prompt bàn giao cho người làm

Prompt chung và khối Người làm đáp phản biện được chép nguyên văn từ mẫu hiện hành, chỉ điền thông tin trung tính. Giai đoạn 2 không có khối trọng tâm cổng riêng. Minh chọn gửi hoặc dừng; không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/); người làm đáp REVIEW-5.md và đánh giá các đề xuất trong bản này.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, M3; task còn M4; giai đoạn 2 không có khối trọng tâm cổng riêng trong docs/review-prompt.md.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (SPEC T-064).
- Tài liệu gốc: tasks/T-064-m1-flashticket/SPEC.md, LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md, CHECKPOINT-CHIEN-DICH.md; results/T-064/tieu-chi-chon.md, ho-so-chon.md, so-bien-the.jsonl; docs/WHY.md, docs/DECISIONS.md; commit gốc c3d27f8a, đầu ra chưa commit.
- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md và các bảng phản hồi; REVIEW-5.md.
- Code và kết quả liên quan: results/T-064/manifest-2.json, manifest.json; results/T-064/kiem/r9/, kiem/nhan-r9/; results/T-064/cham/cham_dev3.py, cham_dev3_truoc_r9.py và các spec/bảng chấm/giữ-bỏ/dời mốc; results/T-064/ban-xuat/, cau-hinh-de-xuat.json, phan-tich/ghi-chu-co-che-dev2.md, chu-thich-thao-tac-nen.md; src/m1_ft/, src/m1/, src/p3/danh_gia.py; results/T-063/manifest-2.json, thu3/manifest-2.json, thu3/xac-nhan-ca-3-sua-sau.json, thu3/BAN-GIAO-B.md; cách gọi exp-obs ở results/T-063/thu3/CHECKPOINT.md, chỉ đọc, không in khóa hoặc ghi máy; kiểm hash trước khi dùng nguồn.
- Phạm vi ghi được Minh cho phép trong lượt này: ở công đoạn đáp, theo SPEC và quyền chiến dịch đã duyệt: chỉ điền bảng Phản hồi của người làm cuối tasks/T-064-m1-flashticket/REVIEW-5.md và nối mục mới tasks/T-064-m1-flashticket/LOG.md; giữ nguyên nhận xét và prompt của reviewer. Các phần thực hiện sửa đối chiếu đúng quyền hiện hành của Minh trước khi làm; chưa có quyền rõ ràng thì trình trong chat.

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

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hoặc prompt của reviewer. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Để trống cột Minh quyết. Prompt của lượt đáp nằm trong LOG hoặc chat.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R11 | Đúng; KHÔNG CHẶN | Log `codex/R5-lan1.log` còn được ghi tới 04:12Z (lượt R5 dừng do hết hạn mức sau khi đã ghi REVIEW-5), sau khi manifest-2 lập 03:55:38Z. Do điều phối lập bản kê khi lượt phản biện đang chạy. Xử lý như đề xuất: giữ manifest-2, lập `manifest-3.json` bằng `kiem/tao_manifest_t064.py` ở bước bàn giao M4 khi không còn lượt nào ghi vào `results/T-064/`; kiểm toàn bộ bản mới. Đồng ý đề xuất dừng vòng phản biện R9/R10; nguyên nhân CPU (Q7) và các câu hỏi OPEN giữ nguyên. | |
