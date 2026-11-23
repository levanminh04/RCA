**Đề xuất tiếp tục phản biện một lượt ngắn, chỉ để đối chiếu hồ sơ.** Tuyến chạy W1 có bằng chứng đạt trên bản FlashTicket đã thử. Hai ca hồi quy V082 khớp chuẩn, bảy gói xuất R9 khớp dữ liệu, và ca mới `7ffb2305` đi tới G1 với đúng hash mã và cấu hình. Phần còn chặn là kết luận về dữ liệu đã xóa và cách bàn giao mục 2.6/2.7. Các điểm này phân xử được bằng hiện vật đã lưu, không cần chạy lại M1.

## 1. Đã làm gì và kết luận từng điểm

| Điểm Phiên 3 | Kết luận kiểm lại |
|---|---|
| **R1 — nguồn của manifest** | **Đúng, đã xử lý.** `manifest-3.json` chưa có ở commit `84f44ee67`, đã được thêm ở `83a91bbe8`. SHA-256 của blob Git mới khớp file trên laptop và dòng 171 của `bao-ve.tsv`. Hai đầu ra chuẩn trên laptop khớp đúng hai mục trong manifest. Hai file chuẩn này không được track ở chính đường dẫn đó, nên trên máy mới có thể dùng Git để lấy **hash chuẩn**. [Đính chính R1](D:/RCA-flashticket/results/T-066/dinh-chinh.md:5) |
| **R2 — STOP và PyYAML** | **Đúng, đã sửa đúng hai đường STOP và phụ thuộc của bộ điều khiển trên exp-obs.** README ở commit lab `d77300b` cũng ghi đúng nơi nhận kết quả. Còn một chỉ dẫn vận hành sai về cách kiểm nguồn, nêu bên dưới. [README bộ điều khiển](D:/Project/flashticket-rca-lab/load/controller/README.md) |
| **R3 — căn cứ xóa** | **Đúng một phần.** Đếm lại được 45 mã `cases/` và 32 mã `outputs/` trong các nguồn nêu ở bản đính chính. Hash script `deploy-t062.sh` lấy từ `a46c009` khớp hash máy đã ghi, còn blob ở `ab1c52c` khác. Tuy nhiên, hồ sơ còn bằng chứng trực tiếp về sáu lượt đã sinh đầu ra. Chỉ dẫn về quyền xóa tiếp cũng chưa thống nhất. [Đính chính R3](D:/RCA-flashticket/results/T-066/dinh-chinh.md:12) |
| **R4 — thứ tự kiểm phát lại** | **Đúng, giới hạn đã được Minh chấp nhận.** Trình danh sách lúc 12:52Z, xóa nhóm 1 lúc 12:53Z, xem ca **mới** trên trang sự cố lúc 15:30Z ngày 17/11. Lần mở trang **phát lại** của ca cũ `46aab4be` được ghi ở Phiên 3 ngày 18/11. Hash đầu ra hiển thị khớp chuẩn T-064. Lần mở sau xác nhận hành vi sau xóa. Lượt này chỉ kiểm chứng cứ đã lưu, không quan sát lại trình duyệt. [Thứ tự và quyết định của Minh](D:/RCA-flashticket/results/T-066/dinh-chinh.md:22) |
| **R5 — trạng thái `XONG`** | **Đúng, KHÔNG CHẶN ca đã chạy.** `m1_worker()` có thể ghi lỗi rồi kết thúc. `chay_lich()` đợi luồng kết thúc và ghi `XONG` mà không tổng hợp thành công từng ca. Riêng `7ffb2305` có bản ghi P7, V082, G1, hash và mã ca tương ứng. Căn cứ nghiệm thu ca này nằm ở các hiện vật đó. [Nhật ký từng khâu](D:/RCA-flashticket/results/T-066/e2e-001/nhat-ky-3.jsonl) |

### CHẶN kết luận R3 rằng không còn căn cứ nhận diện sáu đầu ra

`results/T-062/chay/thu-gia/ket-qua.jsonl` có đúng sáu bản ghi. Cả sáu có `kq.status = "OK"`, `kq.det = true`, và cặp `(id,t)` khớp `request.json` trong sáu thư mục `gia*` của archive. Các mã là `giaa663fa`, `giaec9462`, `gia010acd`, `gia5b128b`, `gia352377`, `giaddecb0`. Đã kiểm hash JSONL theo manifest T-062 và hash các file archive theo danh sách nguồn. Trong runner P7 gốc, nhánh thành công tạo `outputs/<id>`, ghi hai `method-output` và `summary.json` trước khi trả summary. [Sáu lượt placebo](D:/RCA-flashticket/results/T-062/chay/thu-gia/ket-qua.jsonl) · [Thứ tự ghi của P7](D:/RCA-flashticket/results/T-058/dem-2026-11-10/run-m1.py:55)

Có cả bằng chứng loại bớt giải thích khác. Hai ca `kte4878e`, `kteb5f6d` lỗi ngay trong adapter. Hồ sơ `thuong01` cũng ghi lỗi adapter. Với bản runner này, `adapt()` chạy trước `out.mkdir()`. Vì vậy các lượt lỗi đã ghi không có cùng căn cứ sinh thư mục đầu ra như sáu lượt placebo thành công. [Ca thử thứ nhất](D:/RCA-flashticket/results/T-063/kiem-tich-hop/ket-qua-kte4878e.json) · [Ca thử thứ hai](D:/RCA-flashticket/results/T-063/kiem-tich-hop/ket-qua-kteb5f6d.json) · [Hồ sơ `thuong01`](D:/RCA-flashticket/results/T-062/chay/thu-ong-M1.md)

**Sửa tối thiểu đề xuất:** ghi rõ ba mức bằng chứng. Đã tìm thấy bản `outputs/` của 32 mã. Có bằng chứng sáu mã placebo khác đã chạy P7 thành công và khớp đầu vào lưu trữ. Thiếu danh sách tên và hash gốc ngay trước xóa để chứng minh từng thư mục trong 38 thư mục lúc đó, hoặc khẳng định còn bản sao nguyên byte của sáu đầu ra. Minh có thể nghiệm thu hồi quy W1 với giới hạn này. Chạy lại placebo chỉ tạo đầu ra mới, không khôi phục được thời gian chạy và byte của summary cũ.

### CHẶN dùng trạng thái bàn giao làm căn cứ xóa 2.6/2.7

Dòng T-066 trong STATE và câu kết Phiên 3 vẫn hướng người tiếp nhận tới “xóa sau T-067”. T-067 hiện đã nghiệm thu. Trong khi đó, mục Kết quả của danh sách xóa yêu cầu **giữ 2.6 tới khi Minh quyết về CLI `fixture.py`**. Chính phản hồi R6 của T-067 đã rút đề xuất xóa 2.6 và giới hạn 2.7 ở từng script. `fixture.py` còn lấy token và đọc/ghi dữ liệu dưới `/opt/rca-tai`. Lượt tải thành công qua đường mới không thực thi CLI này. Với 2.7, hash của `deploy-t062.sh` chỉ chứng minh có thể khôi phục một script. [Trạng thái T-066](D:/RCA-flashticket/docs/STATE.md:10) · [Điều kiện giữ 2.6](D:/RCA-flashticket/results/T-066/danh-sach-xoa.md:50) · [Phản hồi R6 của T-067](D:/RCA-flashticket/tasks/T-067-ban-flashticket-ghim/LOG.md:316)

**Đề xuất Minh giữ 2.6 và chưa duyệt xóa toàn bộ 2.7.** Nếu Minh duyệt sửa hồ sơ, chỉ cần nối một câu ở LOG T-066 và đồng bộ dòng T-066 trong STATE theo điều kiện đã ghi. Giữ thư mục cũ tốn dung lượng nhưng giữ được đường chạy của CLI. Nếu Minh quyết bỏ CLI hoặc chuyển nó sang đường mới, khi đó mới có căn cứ xét lại 2.6. Với 2.7, xét riêng script nào còn người gọi và bản nào khôi phục được. Không có bằng chứng trong lượt này rằng hai mục đã bị xóa.

### KHÔNG CHẶN W1 — README còn mô tả sai cách dựng và kiểm bộ tải

README sửa ngày 18/11 nói phần dưới giữ “hành vi lệnh không đổi”, rồi mô tả `linux-source-manifest.json`, `Install-LinuxTai` và yêu cầu phát lại pin. Ở `a46c009`, `verify_sources()` đúng là đọc manifest. Ở `ab1c52c`, hàm này đọc commit Git và từ chối cây làm việc có thay đổi dưới `load`, `campaigns`, `inventory`. Bảng đầu README đã sửa đúng đường dẫn, nhưng câu về *hành vi* vẫn khiến người dựng máy có thể tìm một bước triển khai mà bản hiện hành không dùng. [README, đoạn chuyển sang hướng dẫn cũ](D:/Project/flashticket-rca-lab/load/controller/README.md:27) · [Hàm kiểm nguồn](D:/Project/flashticket-rca-lab/load/controller/tai_linux.py:119)

**Sửa tối thiểu đề xuất:** nếu Minh duyệt, sửa riêng đoạn kiểm nguồn của README theo hai revision trên và đánh dấu lệnh PowerShell là lịch sử. README không thuộc các glob mã lab mà T-067 đã băm. Sửa README tạo diff tài liệu và cần commit lab mới để dùng bản hướng dẫn mới trên máy. Không cần sửa runner, venv hay chạy tải. [Phạm vi băm T-067](D:/RCA-flashticket/results/T-067/bao_ve_bam.py)

### KHÔNG CHẶN quyết định giữ Tempo 14 ngày — nguyên nhân giảm dung lượng chưa được đo

Báo cáo viết “chỉ có tăng” ở phần cách đo, sau đó quy hai lần giảm cho việc nén khối. Lấy hiệu hai dòng liên tiếp của `byte_volume` cho thấy giảm **377.717.622 byte** lúc 13:10:07Z và **224.011.607 byte** lúc 14:10:08Z. Script đo dung lượng thư mục và bộ đếm span, không ghi sự kiện compactor để xác nhận cơ chế của từng lần giảm. Phần kết của báo cáo đã đúng khi không suy tốc độ GB/giờ từ lượt đo này. [Số đo gốc](D:/RCA-flashticket/results/T-066/tempo-do-dung.tsv) · [Script đo](D:/RCA-flashticket/results/T-066/tempo_do.sh) · [Câu diễn giải](D:/RCA-flashticket/results/T-066/tempo-tang-truong.md:23)

**Sửa tối thiểu đề xuất:** ghi “chưa tới hạn loại khối theo thời hạn giữ; dung lượng thực đo có tăng và giảm; nén hoặc thay thế khối là giải thích khả thi”. Chỉ cần log hoặc metric compactor cùng thời điểm nếu sau này muốn quy nguyên nhân. Quyết định giữ 14 ngày đã có nguồn riêng trong DECISIONS và không phụ thuộc vào việc phân xử cơ chế này. [Quyết định của Minh](D:/RCA-flashticket/docs/DECISIONS.md:701)

## 2. File và phạm vi

**Không sửa file nào**, không ghi LOG/STATE, không commit, không SSH, không mở dữ liệu khóa và không chạy thực nghiệm mới.

Đối với lượt của người làm, commit sửa RCA `83a91bbe8` thêm manifest, bản đính chính và cập nhật danh sách xóa, LOG, DECISIONS. Commit lab `d77300b` chỉ sửa README. Có một lần ghi ngoài phạm vi đã xảy ra trước đó: SSH đầu phiên thêm hai dòng vào `known_hosts` trên laptop. Người làm đã báo S0-15 và hồ sơ nhóm 2 ghi đã gỡ. Tôi không đọc file khóa để kiểm hiện trạng. Việc gộp hồ sơ T-066 và T-068 ở commit gốc tự nó không chứng minh T-066 đã ghi trái phép vào T-068. [Nhật ký thay đổi máy](D:/RCA-flashticket/results/T-066/thay-doi-may.md)

## 3. Kiểm đã chạy và phạm vi đạt SPEC

| Tiêu chí | Kiểm độc lập và kết quả |
|---|---|
| **1. Hồi quy V082** | Băm hai file chuẩn ở `#/ca/0/chuan/file` và `#/ca/1/chuan/file`, đối chiếu `manifest-3.json#/file`, hai `summary_laptop_sha256` và từng `output_sha256` của hai lần chạy mỗi ca. **Hai ca đều khớp.** Danh sách hash T-067 chụp sau đó cũng ghi đúng hai cặp đầu ra trên exp-obs. Ca `ebd5ef38` dùng tùy chọn dựng lại đầu vào như lượt R9 gốc. [Hồ sơ hồi quy](D:/RCA-flashticket/results/T-066/hoi-quy-v082.json) |
| **2. Bộ xuất R9** | Băm gói nguồn theo danh sách archive và gói mới theo `r9-tong-quat.json#/goi`. So lại từng kênh theo nhãn, timestamp và giá trị, giữ số lần xuất hiện. **7/7 gói**, mỗi gói **24/24 kênh**, cùng cửa sổ, **328 điểm `live-down`**, không lệch và không có lỗi khúc. Đối chứng biểu thức cũ ở `ebd5ef38,d0` có **34 phần tử trong hiệu đối xứng**. WHY-99 ghi rõ phép sửa sau khi thấy dữ liệu dev và lý do loại cửa sổ 15 giây. [Kết quả R9](D:/RCA-flashticket/results/T-066/r9-tong-quat.json) · [WHY-99](D:/RCA-flashticket/docs/WHY.md:1425) |
| **3–4. Tuyến mới và Grafana** | `e2e-001/SHA256SUMS` khớp **10/10**. Năm hash file đầu vào trong `ca-manifest.json#/files` khớp danh sách trên máy. Hai hash mã/cấu hình trong `v082-summary.json` khớp hồ sơ hồi quy. Nhật ký có G1 cho đúng ca. Đếm trường `uid` từ dashboard tại `ab1c52c` được **9 UID khác nhau**. Chứng cứ việc đọc kho cũ và mở UI là bản ghi của phiên đã thực hiện, với giới hạn thời điểm R4. [Manifest ca](D:/RCA-flashticket/results/T-066/e2e-001/ca-manifest.json) · [Summary V082](D:/RCA-flashticket/results/T-066/e2e-001/v082-summary.json) |
| **5–6. Địa chỉ máy và nhãn** | `git grep` các địa chỉ máy tại `ab1c52c` cho thấy ngoài inventory còn tài liệu nguồn và hai ví dụ docstring. Đường chạy lấy địa chỉ máy từ inventory. Sổ thực có **12 dòng**, kiểm lại `seq` và `prev_sha256` không lệch. Helper chạy bằng `ledger` đọc sổ để nối hash. P7/V082 chạy bằng `rca`; hồ sơ có phép đọc bị từ chối. Không thấy tên ô hoặc nội dung sổ đi vào phép xếp hạng của ca này. Mốc `t` của runner là đầu vào được phép của chế độ (a). [Phép cách ly](D:/RCA-flashticket/results/T-066/cach-ly-nhan.md) · [Manifest ghi chế độ](D:/RCA-flashticket/results/T-066/e2e-001/ca-manifest.json) |
| **7. Danh sách xóa** | Băm đúng manifest của **35/35 tgz** T-058/T-062/T-063, liệt kê thành viên bằng `tar -tf`, hợp với thư mục đã giải nén và archive. Kết quả **33 mã `cases` trong tgz, 45 sau hợp, 32 mã `outputs`**. Kiểm thêm **72/72 file** archive ca, **1.684/1.684 file** archive đầu vào M1, hai tar nhóm 2 và **65/65 thành viên** của `tep-le.tar` theo danh sách hash máy. Danh sách đã trình; giới hạn về sáu đầu ra và điều kiện xóa tiếp như trên. [Danh sách xóa](D:/RCA-flashticket/results/T-066/danh-sach-xoa.md) |
| **8. Commit triển khai** | Hồ sơ đã đính chính theo từng máy. Trong `e2e-001`, exp-obs ở `ab1c52c`; exp-app và máy tải ở `5a39028`. Diff hai revision sau chỉ bổ sung phần chạy trên exp-obs. Đủ căn cứ xác định phiên bản cho tuyến đã thử. [Đính chính theo máy](D:/RCA-flashticket/results/T-066/thay-doi-may.md) |

## 4. Điều cần Minh quyết

Đề xuất **chấp nhận bằng chứng kỹ thuật của W1, giữ giới hạn lịch sử R4, và yêu cầu Claude đáp hai điểm R3 trước khi ghi nghiệm thu toàn bộ hồ sơ T-066**. Mặt trái là thêm một lượt đối chiếu ngắn. Đổi lại, người tiếp nhận sẽ biết sáu lượt nào có bằng chứng đã sinh đầu ra và vì sao việc T-067 đã xong chưa cho phép xóa 2.6/2.7. Hai đính chính về README và Tempo có thể xử lý cùng lượt nếu Minh duyệt.

Đối với DT18 và hướng dẫn của cô, W1 chứng minh một tuyến áp dụng M1 trên FlashTicket ở chế độ (a). Bước stage lấy trace/log từ vùng ghi Collector và metric từ Prometheus. W1 chưa chứng minh toàn bộ đường đọc qua API của P9b, hiệu quả do dùng đồ thị, chất lượng tự phát hiện, hay RQ5/G6. Những kết luận đó cần đầu ra tích hợp và thực nghiệm tương ứng của các gói sau. Tôi không thấy lựa chọn phương pháp mới nào trong T-066 cần bổ sung vào WHY. [MRP P9b và P10](D:/RCA-flashticket/docs/MRP.md:301)

## Prompt bàn giao cho Claude

Mẫu hiện hành kết thúc ở G4, chưa có khối G6. Dưới đây là Prompt chung và đúng khối người làm đáp phản biện để Minh chọn chuyển.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-066 — tasks/T-066-repo-lab-dung-lai-may/ (SPEC.md, LOG.md).
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9, P10; chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-066-repo-lab-dung-lai-may/SPEC.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2; repo RCA commit 84f44ee67 và các thay đổi T-066 sau đó; repo lab D:/Project/flashticket-rca-lab, git diff a46c009..ab1c52c và commit d77300b.
- Phản biện và phản hồi trước: Codex soát SPEC bản 1 trong chat 17/11; Codex soát kết quả trong chat 18/11; phản hồi và phần kết Phiên 3 trong LOG T-066; lượt kiểm lại của Codex do điều phối T-070 lưu ở results/T-070/codex/CX-13.jsonl hoặc do Minh dán kèm.
- Code và kết quả liên quan: results/T-066/; results/T-064/manifest-3.json; results/T-058/, results/T-062/, results/T-063/; D:/RCA-archive/exp-obs/cases/, m1ft-inputs/, t066-nhom2/ và D:/RCA-archive/hash-lists/; hồ sơ liên quan trong T-067; repo lab load/controller/, load/fixtures/, campaigns/lib/, campaigns/runner/.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chỉ đọc tại máy, không SSH.

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```