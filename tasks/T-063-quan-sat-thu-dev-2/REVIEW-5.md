# Phản biện T-063 — lượt 5, kiểm phản hồi và sửa sau REVIEW-4

- **Người phản biện:** Codex — **Ngày:** 14/11/2026.
- **Commit/diff đã đọc:** HEAD hiện hành; đầu ra T-063 chưa commit. Đối chiếu hai cặp manifest và diff từng script gốc/bản 2 bằng git diff --no-index. Không lấy git diff của các file chưa được theo dõi làm bằng chứng duy nhất.
- **Công đoạn/cổng và bản lượt:** kiểm lại phản hồi và sửa; chiến dịch M1-FlashTicket, M3; chỉ tạo REVIEW-5.md. Đã liệt kê thư mục và chưa có bản này. Claude làm; Codex phản biện.
- **Đã đọc:** AGENTS, STATE, SPEC và cuối LOG T-063; chiến dịch mục 4–7; phần mục tiêu/RQ/P9/P10 của MRP; DT18, hướng dẫn cô, LESSONS; WHY và DECISIONS liên quan. Đọc hai cặp manifest, bốn script tạo, điều kiện thu3, bàn giao B, báo cáo, hai JSON hậu kiểm, đóng băng 3, sổ thu3, các SHA256SUMS và script/brief R5. Sau tự soát mới đọc nội dung và bảng phản hồi REVIEW, REVIEW-2, REVIEW-3, REVIEW-4.
- **Tự soát độc lập:** trước khi mở nhận xét các review, kiểm mục ghim, tham chiếu và phạm vi của manifest, băm dữ liệu con, truy nguyên phần nối vào điều kiện. Nhận xét riêng lúc đó: hai bản kê mới khớp; bản con cũ lệch đúng file điều kiện; chưa thấy thay dữ liệu nghiên cứu. Sau đó đối chiếu từng phản hồi và kiểm thêm JSON, pin đóng băng, sổ và prompt. Không chạy script sinh manifest vì nó ghi file.

## Kết luận chung

**Không có lỗi đáng kể mới. R7 đúng và đã được sửa đủ về kỹ thuật.** Hai manifest bản 2 bao phủ hồ sơ hiện hành và dẫn đúng bản kê con mới; các bản cũ vẫn được giữ. Phản hồi R7 khớp đầu ra thật.

**Đề xuất dừng phản biện phần thu bù 3 và sửa hồ sơ này.** Việc đó không nghiệm thu toàn T-063/M3, không xác nhận H3/H4/H8 có ích hoặc trả lời xong RQ5. Mốc giờ duyệt ghi xấp xỉ trong LOG chưa đủ để xác nhận thứ tự đến từng phút; giới hạn kiểm đó được nêu riêng dưới đây, không bị suy thành lỗi dữ liệu hay vi phạm quyền đã được chứng minh.

## Các điểm

Không thêm finding mới. R7 không còn là lỗi của chuỗi bản kê hiện hành:

- results/T-063/manifest-2.json#/file_tong_thu_muc_con/thu3/ dẫn thu3/manifest-2.json; hash tham chiếu khớp.
- results/T-063/thu3/manifest-2.json#/file/dieu-kien-xac-nhan-3.md ghim đúng bản có dòng Minh nhận hai sửa.
- Hai manifest cũ được ghim như các file lịch sử. Giữ chúng không có nghĩa mọi đường dẫn bên trong bản kê cũ phải khớp cây file hiện hành. Bản thu3 cũ vẫn lệch đúng file điều kiện đã nối thêm; không sửa đè để che lịch sử đó.
- Kết luận “0 lệch” ở phản hồi áp dụng cho mục ghim và tham chiếu của hai bản 2. Không diễn giải thành “mọi manifest cũ/mới đều khớp đệ quy hiện trạng”.

## Đối chiếu các lượt trước

Không chạy lại toàn bộ phân tích khoa học đã kiểm ở R4. Dùng lại phần có nguồn/hash hợp lệ; phân biệt kiểm trực tiếp lượt này với kết quả cũ được giữ.

| Điểm và phản hồi | Đánh giá độc lập |
|---|---|
| R7 — lỗi bản kê tài liệu | **Đúng; KHÔNG CHẶN dữ liệu.** Bản thu3 cũ có một mục lệch. Bỏ phần bắt đầu “**Minh nhận”, bỏ newline cuối rồi thêm một LF cho lại đúng hash cũ. Phần trước “## Sửa sau” cũng khớp pin điều kiện trước thu. Không có bằng chứng đổi không khai báo điều kiện khóa. |
| R7 (sửa) | **Đúng; đã xử lý về kỹ thuật.** 87/87 và 195/195 mục file khớp; tham chiếu thư mục con/ngoài thu3 khớp. Bản mới giữ cả hai bản kê cũ. Script bản 2 giữ cách băm, đổi file đầu ra và đổi tuyến thu3 sang bản 2; diff không thêm xử lý dữ liệu hay sửa điều kiện. |
| R1 — dọn lỗi vẫn phát ô sau | **Đúng ở mức đã sửa và kiểm ở R4; không có thay đổi làm mất phần sửa.** Runner/injector và các đầu ra kiểm thuộc chuỗi hash đã kiểm. Pin laptop đóng băng hiện còn khớp tại các file thực thi liên quan. Không thử lại lỗi mạng/tiêm, không mở rộng thành mọi sự cố hạ tầng đã được thử. |
| R2 — tích hợp cuối/phục hồi | **Đúng ở mức bằng chứng R4 đã có.** Gói chính và lượt ngắn vẫn khớp SHA256SUMS. Không có thay đổi nguồn/gói do sửa R7. Giữ kết quả kiểm tích hợp trước, không nhận lượt này đã kiểm lại mọi nhánh phục hồi hoặc máy từ xa. |
| R3 — xác nhận hậu kiểm | **Đúng; xử lý được khai và Minh đã nhận.** Đối chiếu trực tiếp hai JSON: chỉ C0_chu_ky của 1e5a3dc5 và httpcheck_phuc_hoi_t180_t570 của ebd5ef38 đổi false → true trong bảng điều kiện. Kết quả 4/6 → 6/6 được giữ riêng. DECISIONS ghi “Nhận cả hai”; không gọi bản sửa là điều kiện khai trước. |
| R4 — CPU và cô lập cơ chế | **Đúng ở mức giới hạn đã giữ.** Không có bằng chứng mới từ sửa manifest nâng mức kết luận CPU; các pin/source và báo cáo không đổi trong phần đối chiếu. Không kiểm lại số CPU thu2, không xem vài điểm PSI là phép tách riêng tranh CPU với lan phụ thuộc. |
| R5 — span thiếu cha/CLIENT khác | **Đúng ở mức kết luận đã sửa.** Báo cáo §7 vẫn tách cha Event ngoài cửa sổ với cha Payment thiếu trong cửa sổ, nêu hai giải thích và nguồn còn thiếu. Hash báo cáo/phân loại vẫn khớp bản kê. Không truy Tempo hay đếm lại raw trace thu2 ở lượt này. |
| R6 — đã loại autovacuum/checkpoint | **Đúng; câu sửa giữ đúng mức căn cứ.** Báo cáo §3/§7 nói phép đếm chưa phân biệt được và không loại khóa ngắn từ vắng log. Sửa R7 không đụng báo cáo hoặc dữ liệu hỗ trợ. Không nhận đã phân xử cơ chế cờ nền. |
| N1 — chuỗi hash sổ | **Đúng; kiểm trực tiếp thu3:** 60/60 dòng đúng seq/prev_sha256; đủ sáu cycle-begin/load-start/cycle-end, không dirty/cycle-error. |
| N2 — hết hạn → chờ → tự gọi lại | **Chưa có bằng chứng bổ sung để xác nhận chu trình thật.** Báo cáo vẫn khai thiếu. Việc phát được R4/R5 không tự thay bằng chứng hết hạn, chờ và tự gọi lại; không đóng M0 từ sửa manifest. |
| N4 — P7 theo ca | **Giữ kết quả kiểm R4, không nhận đã kiểm lại từng output ở lượt này.** Năm archive nằm trong 93/93 mục băm khớp. RECREATE-PAY vẫn được báo lỗi adapter, không gộp vào P7 OK. Không chạy lại phương pháp chỉ vì đổi phiên. |
| Đích PUT/GET ở phản hồi R3 | **Chưa đếm lại trong lượt này.** Báo cáo vẫn dẫn rõ đây là phép đọc của reviewer trước. Không nâng mức chứng cứ chỉ vì người làm đồng ý. |

## Tuân thủ quy trình

- Lượt này chỉ ghi REVIEW-5.md. Không LOG/STATE, bản cũ, source, kết quả, manifest, máy, commit/push hoặc gọi agent khác. Không mở dữ liệu khóa hay repo lưu trữ.
- Quyền làm bản sửa và phát lượt kiểm được nêu trong yêu cầu hiện tại của Minh; LOG và bảng đáp R4 ghi lời duyệt. Không coi finding tự là lệnh sửa, không xin duyệt lại hai sửa hậu kiểm hoặc đáp án H4 đã có quyết định.
- Hai script cũ còn nguyên và được băm trong bản kê. Tạo script/bản kê mới không đổi pin code tính toán hay ca đã thu. Không tái sinh bản kê cũ trong phiên phản biện.
- STATE và một số đoạn bàn giao còn trạng thái của thời điểm trước. Không dùng chúng để đảo lời duyệt mới hoặc tự nghiệm thu task; LOG/prompt hiện tại xác định đúng lượt và vai trò. Reviewer không sửa các file đó.
- Prompt R5 khớp nguyên văn Prompt chung ngoài “Thông tin lượt này”, và khối “Kiểm lại phản hồi và sửa”. Giai đoạn 2 không có khối cổng riêng trong mẫu; không tự ghép thêm.
- Python/rg không có trong PATH của phiên này; dùng PowerShell/.NET và Git chỉ đọc. Không cài môi trường hay đổi ACL.

**Giới hạn đối chiếu giờ duyệt:** LOG ghi Minh duyệt khoảng 16:05Z; hai manifest mới có utc 15:59:52 và 15:59:54Z; R5-trang-thai.json ghi lượt R5 đang chạy lúc 16:00:18Z. Đây là các mốc chưa khớp nếu đọc tới từng phút, trong khi mốc duyệt được ghi xấp xỉ. Chưa có timestamp của chính lời duyệt để tách việc LOG ghi lệch giờ, đồng hồ ghi lệch, hay thao tác xảy ra trước lời duyệt. Vì vậy không xác nhận vi phạm Luật 0, cũng không chứng nhận thứ tự chính xác từ LOG. Đã hỏi làm rõ trong lượt này; quyền ghi REVIEW-5 hiện tại là rõ ràng. Đề xuất điều phối đối chiếu timestamp lời Minh nếu cần xác nhận lịch sử, rồi nối đính chính LOG theo quyền hiện có; không đổi utc manifest để làm đẹp thứ tự. Đọc mốc chat dự kiến vài phút, chưa đo; chưa cần lượt thu/chạy mới. Phần chưa chắc chỉ ảnh hưởng xác nhận thứ tự quyền ghi lịch sử, không thay kiểm hash hoặc bằng chứng thu.

## Điều đã kiểm và thấy đúng

| Kiểm trực tiếp lượt này | Kết quả và nguồn |
|---|---|
| Manifest hiện hành | thu3/manifest-2.json#/file: **87/87**; T-063/manifest-2.json#/file: **195/195**. Bốn tham chiếu của bản thu3 và năm file_tong_thu_muc_con của bản tổng khớp hash. |
| SHA256SUMS con | thu3/thu: **93/93**; thu3/thu-ngan: **21/21**; thu2: **214/214**; ca-t062-bo-sung: **9/9**. Không thiếu hoặc lệch mục đã khai. |
| Phạm vi trên đĩa | Bản thu3 ghim đủ **87/87** file theo bộ chọn đã khai. Ở bản tổng có **4** file sinh sau bản kê: codex/R5-dieu-phoi.out, R5-lan1.log, R5-su-kien.jsonl, R5-trang-thai.json. Chúng là nhật ký lượt đang chạy, được bảng đáp R4 khai ngoài snapshot; không phải dữ liệu nghiên cứu bị bỏ. |
| Cũ → mới, thu3 | Thêm manifest cũ và hai script; không mất mục cũ. Chỉ dieu-kien-xac-nhan-3.md đổi hash trong tập khóa chung. Bản trước dòng duyệt phục hồi đúng hash cũ. |
| Cũ → mới, tổng | Khóa chung không đổi hash; tuyến thu3 đổi từ manifest.json sang manifest-2.json. Bản cũ và các file điều phối/script mới được ghim. |
| Đóng băng 3 | **19/21** pin laptop khớp ở đường gốc. Hai đường đã sửa được đối chiếu với bản giữ trước sửa: xac_nhan_ca_3-ban-chot.py khớp pin script; tiền tố điều kiện trước “## Sửa sau” khớp pin điều kiện. Không gọi bản điều kiện hiện hành là nguyên byte trước thu. |
| Sổ thu3 | **60/60** seq/prev_sha256 đúng; **6** cycle-begin, load-start, cycle-end; **4** fault-start/stop; không cycle-error/dirty. SHA tính trên dòng UTF-8 trước, bỏ newline; đầu chuỗi là 64 số 0. |
| Hậu kiểm | xac-nhan-ca-3.json#/ca và xac-nhan-ca-3-sua-sau.json#/ca: **4 và 6** xác nhận. Chỉ hai điều kiện nêu tại R3 đổi giá trị; không đổi ô, t, tải hay số đo đầu dò cũ để làm đạt. |

Lệnh chỉ đọc đã chạy từ gốc repo cho các mục file/SHA256SUMS; kết quả đúng các số ở hai hàng đầu:

~~~powershell
$ErrorActionPreference='Stop'
foreach($f in @('results/T-063/thu3/manifest-2.json','results/T-063/manifest-2.json')) {
 $j=Get-Content -LiteralPath $f -Encoding UTF8 -Raw | ConvertFrom-Json
 $base=Split-Path $f -Parent
 $bad=@($j.file.PSObject.Properties | Where-Object {
  (Get-FileHash -LiteralPath (Join-Path $base $_.Name) -Algorithm SHA256).Hash -ne $_.Value
 })
 '{0}: {1}/{2} khop' -f $f,(@($j.file.PSObject.Properties).Count-$bad.Count),@($j.file.PSObject.Properties).Count
}
foreach($f in @('results/T-063/thu3/thu/SHA256SUMS','results/T-063/thu3/thu-ngan/SHA256SUMS','results/T-063/thu2/SHA256SUMS','results/T-063/ca-t062-bo-sung/SHA256SUMS')) {
 $base=if($f -like '*ca-t062-bo-sung*'){'.'}else{Split-Path $f -Parent}
 $n=0;$bad=0
 foreach($line in (Get-Content -LiteralPath $f -Encoding UTF8)) {
  if(-not $line.Trim()){continue}
  if($line -notmatch '^([0-9a-fA-F]{64})\s+\*?(.+)$'){throw 'SHA256SUMS khong hop le'}
  $n++
  if((Get-FileHash -LiteralPath (Join-Path $base $Matches[2]) -Algorithm SHA256).Hash -ne $Matches[1]){$bad++}
 }
 '{0}: {1}/{2} khop' -f $f,($n-$bad),$n
}
~~~

Ngoài lệnh trên, dùng ConvertFrom-Json để duyệt các tham chiếu bản kê/đóng băng và Get-FileHash đối chiếu từng file. Dùng UTF8Encoding(false), SHA256 và phép cắt tiền tố đã mô tả để kiểm hai phiên bản điều kiện; dùng cùng cách băm từng dòng để kiểm sổ. Không ghi file kiểm riêng.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập bản sửa R7, phạm vi/hash/chuỗi tham chiếu, lịch sử điều kiện và các phản hồi trước. Không thêm hoặc đổi quyết định nghiên cứu.
2. **File đổi:** chỉ tasks/T-063-quan-sat-thu-dev-2/REVIEW-5.md, gồm prompt bàn giao và bảng đáp trống.
3. **Kiểm:** các bảng/lệnh trên; không thực nghiệm mới, không truy máy từ xa hoặc đọc lại toàn bộ trung gian thu2/P7. Những kết quả cũ được dùng lại đều có phạm vi nêu rõ.
4. **Phần còn mở và đề xuất:**

| Phần còn mở | Vì sao, bằng chứng phân xử và hệ quả |
|---|---|
| Lợi ích H3/H4/H8 và RQ5 | Thu có can thiệp/đối chứng không tách được ích lợi của kênh mới, bước dùng cạnh và các thay đổi khác. Cần biến thể, trung gian và đối chứng của T-064 theo hồ sơ hiện hành. Đề xuất tiếp tục T-064 bằng dữ liệu đã kiểm, giữ phân tầng build/tải và giới hạn một lần thu; không thu lại chỉ để xác nhận bản kê. Chi phí phần phân tích/chạy thiếu theo T-064, chưa đo ở lượt này. Không suy từ thu3 sang chọn thiết kế hoặc lợi ích đồ thị. |
| Payment thiếu cha | Đến kho sau snapshot và bỏ sót ở capture/xuất chưa tách được. Cần snapshot/log exporter tương ứng nếu còn; rà nguồn lưu dự kiến phút đến vài chục phút, chưa đo. Không có nguồn thì giữ giới hạn về bước làm thiếu và tác động riêng tới hạng; không gán nguyên nhân hoặc tự loại ca. |
| Cờ nền thu2 | Phép đếm chưa tách tác động theo thời điểm/thời lượng/I/O của autovacuum/checkpoint hoặc khóa ngắn. Đề xuất đọc trung gian và log đã lưu trước nếu lựa chọn cơ chế phụ thuộc; dự kiến vài chục phút, chưa đo. Thiếu quan sát thì không quy một cơ chế để đóng câu hỏi. |
| PSI bản 3 | Watchdog Event, tải nền theo giờ và dao động máy còn là các giải thích. CPU/PSI đã lưu quanh đối chứng có thể phân xử một phần, dự kiến 10–30 phút chưa đo; vài mốc không tạo cặp can thiệp đủ để quy riêng tác động watchdog. Đề xuất giữ giới hạn, không gọi hai build tương đương hoàn toàn. |
| Chu trình tự gọi lại M0 | Thiếu lần thật hết hạn → chờ → tự gọi lại chạy trọn. Cần nhật ký chu trình đó, không thể thay bằng lượt phát CLI thành công. Thời gian phụ thuộc lúc hết/hồi hạn mức, chưa có ETA kiểm ở lượt này. Giữ phần này chưa đạt; bổ sung SPEC cho phép các nhánh độc lập tiếp tục. |

**Đề xuất dừng phản biện phần thu bù/sửa R7.** Không có phản đối khoa học chưa xử lý mới trong phần này. Một vòng lặp cùng đầu ra không bổ sung bằng chứng. Mặt trái của dừng là các câu hỏi nguồn trên vẫn mở; không dùng dừng phản biện làm bằng chứng đã hoàn tất chúng. Mốc giờ duyệt lịch sử cần nguồn timestamp nếu muốn xác nhận đến phút, không cần sửa dữ liệu hay mở vòng phản biện khoa học mới chỉ cho việc đó. Minh quyết dừng, nghiệm thu phần nào hoặc yêu cầu tiếp; các đề xuất trên chưa thay quyết định của Minh.

Nếu Minh muốn lưu riêng bản review sau khi xem, nội dung commit đề xuất: T-063: ghi kiểm lại bản kê sau REVIEW-4. Lượt này không commit/push.

## Prompt bàn giao cho người làm

Chép nguyên văn Prompt chung và khối “Người làm đáp phản biện” dưới đây, chỉ điền thông tin trung tính. Không có khối cổng riêng cho giai đoạn 2. Minh/điều phối chọn gửi hoặc dừng; reviewer không tự gửi.


```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-063 (tasks/T-063-quan-sat-thu-dev-2/), phần thu bù 3.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, mốc M3 (tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 4–7); giai đoạn 2 không có khối trọng tâm cổng riêng trong docs/review-prompt.md.
- Người làm và người phản biện chính thức: Claude làm (phiên B; phiên điều phối đáp thay theo quyền chiến dịch); Codex phản biện theo SPEC T-063.
- Tài liệu gốc: tasks/T-063-quan-sat-thu-dev-2/SPEC.md, LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md; docs/DECISIONS.md; docs/WHY.md.
- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md và REVIEW-5.md, cùng các bảng Phản hồi của người làm tương ứng.
- Code và kết quả liên quan: results/T-063/thu3/manifest.json, manifest-2.json; results/T-063/manifest.json, manifest-2.json; results/T-063/thu3/scripts/tao_manifest_thu3.py, tao_manifest_thu3_2.py; results/T-063/dong-goi/tao_manifest_t063.py, tao_manifest_t063_2.py; results/T-063/thu3/dieu-kien-xac-nhan-3.md; results/T-063/codex/R5-trang-thai.json; results/T-063/thu3/xac-nhan-ca-3.json, xac-nhan-ca-3-sua-sau.json; results/T-063/bao-cao.md.
- Phạm vi ghi được Minh cho phép trong lượt này: bảng Phản hồi của người làm ở cuối tasks/T-063-quan-sat-thu-dev-2/REVIEW-5.md và nối LOG.md của chính task theo SPEC và quyền chiến dịch mục 6; không sửa phần nhận xét hoặc prompt của reviewer. Ngoài hai phần này chỉ đọc trong lượt đáp; nếu chưa có quyền ghi rõ ràng thì chỉ trả lời trong chat.

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

Người làm chỉ điền bảng này và nối LOG trong quyền; không sửa nhận xét/prompt của người phản biện. Thêm N1, N2… cho điểm tự tìm được, nêu mức và bằng chứng. Để trống cột Minh quyết; prompt đáp nằm trong LOG hoặc chat theo quyền.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
