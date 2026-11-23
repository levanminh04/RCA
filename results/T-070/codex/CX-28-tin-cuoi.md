**R2(b) đã đủ điều kiện CX-05.** Tại `HEAD 14ee980d7`, lúc **12:26:47 ngày 23/11/2026 giờ Việt Nam**, nhóm A có **1.711 tệp chưa track, 282.987.290 byte**. Tôi đề xuất đưa **1.665 tệp, 259.556.470 byte (247,53 MiB)** vào danh sách `git add` và tạm giữ 46 tệp nêu dưới đây. Vùng stage trống. Tôi tự kiểm trong phiên này, không dùng agent con, không sửa tệp và không chạy `git add`, `commit` hay `push`. [Dòng duyệt R2(b)](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:132) · [Kết quả CX-05](/D:/RCA-flashticket/results/T-070/codex/CX-05-tin-cuoi.md:1)

**Có quyết định mới ngay trong lúc kiểm.** Lúc 05:20Z ngày 23/11, LOG T-070 ghi Minh duyệt Q1–Q11. Q11 cho phép commit cùng phần ngoài R2(b) có tên trong danh sách sau khi điều phối kiểm. Vì vậy, bảng B dưới đây vẫn tách riêng phần phát sinh, nhưng những mục Q11 đã bao phủ không cần xin lại quyền commit. Chỗ nào chưa có bằng chứng Minh duyệt **nội dung**, tôi ghi rõ. [LOG T-070](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:344) · [Quyết định Q11](/D:/RCA-flashticket/docs/DECISIONS.md:768)

### A. Tệp thuộc R2(b)

| Đường dẫn | Tệp đề xuất add | Byte |
|---|---:|---:|
| `docs/techstack/ban-giao-dieu-phoi-2026-11-20/` | 20 | 281.035 |
| Bảy thư mục `tasks/T-069` đến `tasks/T-075`, tên đầy đủ trong lệnh cuối | 17 | 559.723 |
| `results/T-069/` | 349 | 228.302.081 |
| `results/T-070/` | 107 | 813.116 |
| `results/T-071/` | 91 | 5.413.611 |
| `results/T-072/` | 951 | 22.644.873 |
| `results/T-073/` | 109 | 1.291.299 |
| `results/T-074/` | 21 | 250.732 |
| `results/T-075/` | 0 | Chưa có thư mục tại mốc kiểm |
| **Tổng đề xuất** | **1.665** | **259.556.470** |

**Ba tệp vượt 50 MB.** Tôi đề xuất **giữ cả ba**. Chúng là dữ liệu tải gốc, có trong `SHA256SUMS-2` và đã kiểm khớp tại chỗ. Bỏ ba tệp sẽ giảm đúng **198.855.654 byte**, còn **60.700.816 byte** trong danh sách add, nhưng bản clone sẽ thiếu dữ liệu đối chiếu. Tôi chưa xác minh được một bản lưu thay thế cho ba tệp này. [Manifest T-069](/D:/RCA-flashticket/results/T-069/SHA256SUMS-2)

| Đường dẫn dưới `results/T-069/thu/` | Byte |
|---|---:|
| `t069-chinh/tai-out/t3-124242f0/raw.json` | 77.781.717 |
| `t069-lap/tai-out/t3-690d426a/raw.json` | 60.584.079 |
| `t069-chinh/tai-out/t3-81de370b/raw.json` | 60.489.858 |

**46 tệp đề xuất tạm giữ trên máy, không xóa:**

| Tệp | Số lượng | Lý do và hệ quả |
|---|---:|---|
| `results/T-070/codex/CX-*.jsonl`, chỉ ở ngay dưới `codex/` | 43 | Nhật ký terminal thô, gồm lượt hỏng, ba bản UTF-16 và `CX-28.jsonl` đang tăng trong lúc kiểm. Nhiều nhật ký lặp đường dẫn khóa hoặc lệnh SSH. Giữ các brief, bản `*-tin-cuoi.md` và kết quả CX-05 trong danh sách add. |
| `results/T-069/xac-nhan/xac_nhan_ca.py` và `xac_nhan_ca_3.py` | 2 | Có đường dẫn cụ thể tới tệp khóa trong đối số SSH `-i`. Cả hai script được ghim trong hai manifest T-069. |
| `results/T-072/e3/b7-cho.sh` | 1 | Có đường dẫn cụ thể tới tệp khóa. Script được ghim trong `SHA256SUMS-e3-b6-9`. |

**Điểm cần điều phối/Minh chốt ở nhóm A** là ba script đã ghim. Nếu giữ ngoài Git theo đề xuất, máy mới sẽ thiếu đúng hai script khi kiểm manifest T-069 và một script khi kiểm manifest E3. Nếu Minh chấp nhận đưa đường dẫn cục bộ vào repo, có thể giữ nguyên ba script để tái lập đủ. Sửa trực tiếp đường dẫn sẽ đổi hash. Hai tài liệu `tasks/T-069-v082-ban-ghim/LOG.md` và `lich-su/01-minh-tin-nhan.md` chỉ nêu thư mục khóa và `known_hosts`; tôi giữ cả hai trong A. [Manifest T-069](/D:/RCA-flashticket/results/T-069/SHA256SUMS-2:346) · [Manifest E3](/D:/RCA-flashticket/results/T-072/SHA256SUMS-e3-b6-9:1)

**Kiểm nhị phân, bí mật và ignore.** Trong A có 578 `.gz`, 3 `.tgz`, 15 ảnh JPEG và 3 nhật ký văn bản UTF-16. Tôi đã quét nội dung giải nén, gồm 833 tệp trong ba tar, trong đó có 606 luồng gzip lồng, và xem 15 ảnh Grafana. Đề xuất giữ các gói số liệu và ảnh làm bằng chứng. Không phát hiện tệp `.env`, tệp khóa riêng, khối private key thật hay mật khẩu rõ qua các mẫu đã kiểm. Các khớp `BEGIN .*PRIVATE KEY` ở brief, script điều phối và nhật ký CX-28 có cả **chính mẫu grep**. Các khớp `.key` trong nhiều JSON T-069 là tên Keycloak. `.gitignore` của repo chỉ che bốn `.pyc` trong hai `__pycache__` của T-072 ở phạm vi A. Không thấy đầu ra cần cho commit bị che. Git báo không đọc được global ignore của tài khoản chạy kiểm. Manifest gói bàn giao và cả hai manifest T-069 đều kiểm khớp trên cây làm việc. [Quy tắc ignore](/D:/RCA-flashticket/.gitignore:4) · [Manifest bàn giao](/D:/RCA-flashticket/docs/techstack/ban-giao-dieu-phoi-2026-11-20/SHA256SUMS)

### B. Sáu tệp ngoài R2(b) gốc

`git diff --stat` ở lần kiểm cuối báo **225 dòng thêm, 2 dòng bỏ**. `git diff -U0` cho thấy **mỗi tệp có đúng một hunk Git**. Bảng tách tiếp theo mục nội dung khi trong cùng hunk có nhiều lần duyệt khác nhau.

| Tệp và hunk | Ngày, nội dung | Có dòng duyệt của Minh trong LOG? |
|---|---|---|
| `docs/DECISIONS.md` `+727,58`, mục bắt đầu dòng 728 | 19–20/11. Gia hạn sự kiện tải, thu lại ba ô, ghi nhận phạm vi ghi thực tế, sửa theo phản biện T-069. | **Có**, LOG T-069 dòng 382 duyệt danh sách sửa gồm DECISIONS và WHY. Việc thu lại ba ô được ghi nhận sau. [LOG T-069](/D:/RCA-flashticket/tasks/T-069-v082-ban-ghim/LOG.md:382) |
| Cùng hunk, dòng 737 | 19–20/11. Mong muốn điều phối sau T-069. | **Có**, R2(a) duyệt ghi khối này lúc 13:25Z. [LOG T-070](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:134) |
| Cùng hunk, dòng 746 | 20/11. R1, R5, R7, R9 về V082 cho demo, ngưỡng báo giả, tải nền và hạn bán. | **Có**, Minh “duyệt ghi” lúc 13:26Z. [LOG T-070](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:143) |
| Cùng hunk, dòng 755 | Quyết ngày 20/11, ghi lúc 02:42Z ở lượt tiếp theo. Commit bộ chuỗi, (a)–(e), phát E2, D1–D5. | **Có**, LOG ghi “Duyệt cả năm”, sau đó “duyệt ghi”. [LOG T-070](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:221) · [Dòng duyệt ghi](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:230) |
| Cùng hunk, dòng 768 | 23/11. Gói E5/P/H và Q1–Q11. Khối này xuất hiện trong lúc kiểm. | **Có**, duyệt commit/push gói lab ở dòng 327, duyệt Q1–Q11 và ghi khối theo Q10 ở dòng 344. [LOG T-070](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:344) |
| `docs/WHY.md` `+1449,71` | 20/11. WHY-102 về hai tầng tiêu chí W3. WHY-103–110 về route, cửa sổ, 5xx, liveness, nhịp đánh giá, gom sự cố và chọn ngưỡng W4. Ngày 21/11 thay phần phương án, bằng chứng và điều kiện thất bại của WHY-110. | **Có** cho WHY-102 và D4. Riêng chữ sửa WHY-110 lúc 02:45Z, LOG ghi điều phối xử lý trong phạm vi D4. **Không thấy câu Minh duyệt riêng bản chữ sửa**. CX-19 sau đó vẫn nêu WHY-110 cho Minh. [LOG T-069](/D:/RCA-flashticket/tasks/T-069-v082-ban-ghim/LOG.md:382) · [D4](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:225) · [Sửa WHY-110](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:244) |
| `docs/STATE.md` `-10,2 +10,9` | 18–23/11. Thay dòng T-066/T-067, thêm T-069 và T-070–075. T-066 ghi sửa và chờ kiểm lại. T-067 ghi nghiệm thu. T-069 đã cập nhật nghiệm thu Q4. T-070–074 ghi tiến độ E2–E5 và W6. T-075 còn ghi chờ Q6. | **Có** cho các quyết định nền của T-066, T-067 và T-069. Các dòng tiến độ thuộc quyền cập nhật từng task. **Không thấy duyệt nguyên hunk**. Khi kiểm, T-070 còn trỏ bản 4 chờ Minh, T-074 còn tóm tới bản 3 và T-075 còn chờ Q6 dù LOG đã có bản 4 W6 và quyết định mở W8. Đề xuất điều phối đối chiếu các dòng này trước khi đưa B vào commit. [STATE](/D:/RCA-flashticket/docs/STATE.md:10) · [LOG T-074](/D:/RCA-flashticket/tasks/T-074-w6-thiet-ke-danh-gia/LOG.md:280) · [Q4, Q6, Q7](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:344) |
| `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` `+163,2` | 19/11. Dòng 163 nói ngày demo/bảo vệ chưa chốt và không chặn lịch. Dòng 164 nói chạy nhiều phiên Claude, tách giờ dùng exp-app và cho W5 chạy song song W3. | **Không tìm thấy trong các LOG liên quan câu Minh duyệt ghi đúng hai dòng này.** File tự dẫn “Minh, chat 19/11”. Gói bàn giao có lời Minh về nhiều phiên ngày 20/11. Đề xuất điều phối xác nhận nguồn cho hai dòng, nhất là mệnh đề W5 chỉ dùng dữ liệu đã thu. [Kế hoạch](/D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:163) · [Lời Minh trong bàn giao](/D:/RCA-flashticket/docs/techstack/ban-giao-dieu-phoi-2026-11-20/mong-muon-minh.md:19) |
| `tasks/T-067-ban-flashticket-ghim/LOG.md` `+334,1` | 19/11 05:58Z. Nghiệm thu T-067 và chuyển các mục mở sang gói sau. | **Có ngay trong hunk**, “duyệt các việc tồn đọng theo đề xuất”, gồm nghiệm thu T-067. [LOG T-067](/D:/RCA-flashticket/tasks/T-067-ban-flashticket-ghim/LOG.md:334) |
| `tasks/T-068-don-grafana/LOG.md` `+750,84` | 19/11. Dòng 750 ghi duyệt và commit/push cũ `3874f34`. Từ dòng 752 là đề xuất về câu hiển thị, hiện vật tạm và lượt kiểm lại. Từ dòng 761 là prompt bàn giao. | **Có** “Duyệt cả hai” cho việc đã ghi ở dòng 750. **Không có duyệt toàn bộ đề xuất** ở phần sau. Q5 ngày 23/11 giải quyết riêng việc giữ bản hoàn tác và hiện vật ca `7ffb2305`. Có thể commit nhật ký lịch sử với đúng trạng thái đề xuất. [LOG T-068](/D:/RCA-flashticket/tasks/T-068-don-grafana/LOG.md:750) · [Q5](/D:/RCA-flashticket/docs/DECISIONS.md:768) |

### C. Ngoài phạm vi

`git status --porcelain` trả **4.013 dòng `??`** dưới các thư mục `results/` cũ của T-032, 033, 041, 042, 045–054, 058 và 062–065. Đây là số **dòng trạng thái** vì Git gộp một số thư mục. Đề xuất bỏ toàn bộ khỏi commit này. Ngoài A, B và các mục C đó, không thấy đường dẫn thay đổi nào khác trong kết quả porcelain. Một số thư mục cache/tmp cũ báo thiếu quyền đọc, đều ngoài A.

### Lệnh `git add` cho nhóm A

Lệnh **Git Bash** dưới đây dùng đúng 14 thư mục có thật tại mốc kiểm, trừ đúng 46 tệp đã nêu. Vì có phiên khác đang ghi, lệnh kiểm cả danh sách đường dẫn lẫn nội dung trước khi stage. Nếu có tệp mới hoặc có tệp đã đổi, nó dừng để điều phối chỉ cần rà phần chênh. **Lệnh chưa được chạy.**

```bash
cd /d/RCA-flashticket || exit 1
set -o pipefail

roots=(
  docs/techstack/ban-giao-dieu-phoi-2026-11-20
  tasks/T-069-v082-ban-ghim
  tasks/T-070-dieu-phoi-giai-doan-2
  tasks/T-071-w4a-nen
  tasks/T-072-w4b-luat-canh-bao
  tasks/T-073-w5-rca-truc-tuyen
  tasks/T-074-w6-thiet-ke-danh-gia
  tasks/T-075-w8-llm-toi-thieu
  results/T-069
  results/T-070
  results/T-071
  results/T-072
  results/T-073
  results/T-074
)
omit=(
  ':(exclude,glob)results/T-070/codex/CX-*.jsonl'
  ':(exclude,literal)results/T-069/xac-nhan/xac_nhan_ca.py'
  ':(exclude,literal)results/T-069/xac-nhan/xac_nhan_ca_3.py'
  ':(exclude,literal)results/T-072/e3/b7-cho.sh'
)

mapfile -d '' -t files < <(
  git ls-files --others --exclude-standard -z -- "${roots[@]}" "${omit[@]}"
)
digest=$(printf '%s\0' "${files[@]}" | xargs -0 sha256sum | sha256sum) || exit 1
expected=552faae72911593266dcaaf3123406dd7721c8030b900f521d0b4d7bdd1f419a

if [[ ${#files[@]} == 1665 && ${digest%% *} == "$expected" ]]; then
  printf '%s\0' "${files[@]}" |
    git --literal-pathspecs add --pathspec-from-file=- --pathspec-file-nul
else
  printf '%s\n' 'Danh sách hoặc nội dung đã đổi sau mốc kiểm. Chưa stage.' >&2
fi
```