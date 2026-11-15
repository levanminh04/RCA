# Phản biện T-062 — G1, lượt 4

- **Người phản biện:** Codex — **Ngày:** 12/11/2026; kiểm đến khoảng 01:56 UTC.
- **Công đoạn:** kiểm lại phản hồi và bản sửa G1; cổng nghiên cứu gần nhất đã duyệt: G4.
- **Commit gốc:** `c3d27f8a`. Đầu ra G1 chưa commit.
- **Phạm vi:** chỉ đọc. Tôi không tự ghi bản phản biện, sửa file hoặc triển khai.
- **Đã đọc:** AGENTS, STATE; SPEC/BOI-CANH/LOG/CHECKPOINT T-062; nguồn DT18 và hướng dẫn của cô; phần liên quan trong MRP/WHY/DECISIONS/LESSONS và kế hoạch giai đoạn 2; định dạng T-061, danh mục T-059; code, dashboard, dữ liệu, chỉ mục, tài liệu, ảnh G1; ba lượt phản biện và phản hồi.
- **Tự soát độc lập:** đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt trước. Kiểm bằng tính toán trong bộ nhớ, Infinity trên Grafana thử và SSH chỉ đọc tới `exp-obs`.

## Kết luận chung

**Đồng ý bản sửa F1′, F2′, F3, F4. Đồng ý F5 với điều kiện hoàn tất phần triển khai và ghi nhận đã khai. Không phát hiện lỗi mới đáng kể trong bản 5 đã kiểm.**

R1 đã được sửa đúng trong repo và trên bản thử. **Chưa thể nghiệm thu bản triển khai:** `exp-obs` vẫn chạy dashboard bản 4. G1 đáp ứng một phần giao diện minh họa của DT18; chưa hoàn thành dịch vụ RCA trực tuyến, LLM hoặc chuỗi demo dài hạn.

## Các điểm

### R1. Lỗi đáp án đã sửa trên bản thử, còn trên dashboard đang triển khai — CHẶN nghiệm thu phần phát lại trên `exp-obs`

- **Ở đâu:** `dung-dashboard.py`, `chi-muc-phat-lai.py` và hai dashboard dẫn xuất.
- **Bằng chứng bản sửa đúng:**
  - `f728fce2.phat-lai.json`: `/phat_lai/tap_chap_nhan` gồm `api-gateway`, `booking-service`; hạng tương ứng 4 và 1. Infinity trả dấu ◆ cho cả hai, giữ đúng màu và vai trò.
  - `1ad3afeb.phat-lai.json`: tập gồm `event-service`, `event_db`. Cả hai có ◆; `event_db` vẫn bình thường. Chỉ mục ghi rõ “M1 xếp hạng #4, nhóm 14 thành phần”.
  - Mẫu T-061 `f4a8c021`: dự phòng về `event-service`, ghi thiếu dữ liệu và không có hạng; không in `#null`.
  - Tập rỗng/null không đánh dấu nút nào. Thiếu khóa mới mới dùng trường T-061.
- **Phần còn lại:** SSH xác nhận dashboard trên `exp-obs` vẫn khớp bản 4 trong snapshot cũ. Bản này vẫn biểu diễn riêng phần tử đầu tập chấp nhận.
- **Hậu quả:** chưa thể gọi phần phát lại đang phục vụ là đã sửa xong.
- **Sửa tối thiểu:** hoàn tất triển khai bản 5 theo F5 đã thống nhất. Không sửa M1, đáp án hoặc cách chấm.
- **Mức ảnh hưởng:** trung bình, thuộc diễn giải phát lại.
- **Dài hạn:** giữ đúng phân biệt root cạnh và tập chấp nhận mức nút; không cần đổi MRP.
- **Production/main/máy 84:** không có tác động trực tiếp từ bản sửa này.

### R3. F5 đang thực hiện, chưa hoàn tất — CHẶN tuyên bố đã triển khai xong

Có thay đổi trong lúc phản biện:

- Khi bắt đầu kiểm, chỉ mục phát lại thật còn khớp snapshot cũ.
- File được cập nhật lúc khoảng **01:52 UTC**. Cuối lượt, chỉ mục local và trên `exp-obs` khớp nhau.
- Tôi sinh lại chỉ mục **trong bộ nhớ** bằng script hiện tại: khớp byte với chỉ mục thật mới.
- Hai dashboard trên `exp-obs` vẫn là bản 4; chỉ mục mẫu trên máy và việc nạp bản 5 chưa được lượt này xác nhận hoàn tất.
- Snapshot `results/T-062/manifest.json` vẫn là bản 01:23 UTC. Nó chưa xác thực bản sửa và chỉ mục thật mới.

Đây là trạng thái triển khai đang chuyển tiếp, **không phải bất đồng mới về thiết kế**. Chỉ mục mới giữ trường cũ nên dashboard cũ vẫn đọc được.

- **Đề xuất:** tiếp tục đúng F5: hoàn tất dashboard và chỉ mục mẫu, kiểm bản phục vụ thật, ghi nhận thay đổi/snapshot theo phân công.
- **Mức ảnh hưởng:** trung bình trong triển khai và truy vết; không đổi kết quả khoa học.
- **Dài hạn:** không đổi hướng Grafana hoặc hợp đồng kết quả RCA 0.2.
- **Production/main/máy 84:** không có đường tác động trực tiếp. Khởi động lại Grafana có thể gián đoạn ngắn giao diện quan sát trên `exp-obs`.

## Đối chiếu các lượt trước

| Điểm/phương án | Kết luận lượt 4 | Bằng chứng và giới hạn |
|---|---|---|
| **R1 / N1** | **Đúng; đã sửa trên repo/bản thử.** | Hiện root, toàn tập chấp nhận, hạng từng thành phần và hạng tốt nhất. Bản triển khai còn cũ. |
| **F1′** | **Đồng ý.** | Giữ ba trường cũ; thêm trường mới; bảo toàn số E2. Kiểm chỉ mục của chín ca thật và hai mẫu. |
| **F2′** | **Đồng ý.** | ◆ chỉ tập chấp nhận; giữ nguyên dự đoán M1; không thêm cạnh giả. Nhánh thiếu khóa, rỗng/null và T-061 chạy đúng. |
| **R2 / F3** | **Đúng; đồng ý bản sửa.** | Hai dashboard bỏ số 10 cố định và dẫn tới Độ phủ. |
| **N2 / F4** | **Đúng; đồng ý bản sửa.** | Đổi thành “M1 trả hạng / quan sát”; giải thích nhóm bình thường vẫn có hạng trong đầu ra. Không đổi số hoặc quy tắc ẩn hạng. |
| **R3 / F5** | **Đồng ý có điều kiện hoàn tất thực thi.** | Chỉ mục thật mới đã có và đúng; dashboard trên máy vẫn cũ; snapshot mới chưa có. |
| **Điều kiện lượt 2–3** | **Đã đáp ứng ở bản sửa đã kiểm.** | Không nhầm thiếu khóa với tập rỗng/null; không in hạng null; diễn đạt đúng nhóm đồng hạng và ý nghĩa ◆. |
| **N3** | **Đúng trong phạm vi đã nêu.** | Lớp thao tác vẫn là telemetry theo service/route, chưa phải xếp hạng thao tác M1. Giữ ngoài gói sửa. |
| **N4** | **Giữ giới hạn đã khai.** | Tách trang không tạo phân quyền cho file `public/rca`. Bản sửa không thay cơ chế này. |
| **N5** | **Đồng ý giới hạn diễn giải.** | Hạng tốt nhất được ghi “theo e2, mức nút”; không suy thành định vị đúng cạnh. Không sửa cách chấm trong G1. |

**Mặt trái của tương thích:** chỉ mục cũ không chứa toàn tập chấp nhận. Dashboard mới ghi rõ “chỉ mục cũ”, nhưng không thể khôi phục phần thông tin thiếu. Tôi kiểm nhánh này bằng bản mô phỏng hợp đồng cũ trong bộ nhớ; không coi nó là trạng thái hoàn tất R1.

## Tuân thủ quy trình

- Không sửa file, ghi LOG/STATE, commit/push hoặc thay đổi máy chủ.
- Không đọc sổ tiêm lỗi, mật khẩu, `grafana.env`, nội dung khóa hoặc dữ liệu khóa. Không chạm máy 84.
- Không chạy M1 hoặc thực nghiệm nghiên cứu mới.
- Bản sửa phù hợp phương án đã thống nhất ở lượt 3 và điều kiện Minh đã ghi trong prompt.
- Các hash của hai script, hai dashboard, hợp đồng chỉ mục, phản hồi và chỉ mục mẫu khớp phần ghi nhận bản 5 trong `thay-doi.md`.
- Tôi không dùng snapshot cũ để xác nhận các file đã đổi. Chỉ mục thật mới được đối chiếu riêng với kết quả sinh trong bộ nhớ và bản trên máy.
- Không phát hiện thay đổi thuật toán, tham số hoặc tiêu chí chấm trong diff dashboard. Không mở lại task đã nghiệm thu.

## Điều đã kiểm và thấy đúng

- Bốn script G1 phân tích cú pháp thành công.
- Hai dashboard sinh trong bộ nhớ trùng cấu trúc JSON đã lưu.
- Dashboard được Grafana thử nạp có `panels`, `templating`, `links` và `description` trùng file repo.
- **264 truy vấn Infinity** trên hai dashboard, với chín ca thật và hai mẫu, không trả lỗi. Kiểm nút, cạnh, màu, hạng, bán kính và cửa sổ thời gian khớp đầu vào.
- Kiểm riêng dấu ◆ và bản ghi phát lại trên đủ 11 ca; kết quả đúng. Kiểm bổ sung thiếu khóa, tập rỗng/null và chỉ mục cũ đạt.
- Dữ liệu chính và phát lại giữ nguyên dự đoán: bỏ khối `phat_lai` thì chín bản phát lại trùng cấu trúc bản chính; hash nguồn trước ghép khớp.
- Chỉ mục mẫu mới đúng với kết quả sinh trong bộ nhớ. Chỉ mục thật mới cũng khớp byte kết quả sinh.
- JSON trang chính không chứa các mẫu truy cập đáp án bị cấm.
- Đã xem ảnh 16 và 18: dấu ◆ và vai trò phù hợp kết quả truy vấn. Đây là ảnh bản thử.
- Diff với bản 4 không đổi truy vấn telemetry, liên kết Explore, biến dashboard hoặc nguồn dữ liệu.

Lệnh kiểm truy vấn có thể chạy lại:

```powershell
py -3 -B results/T-062/giao-dien/kiem-truy-van.py http://127.0.0.1:3062 results/T-062/giao-dien/grafana/dashboards/rca-g2-phat-lai.json ca=f728fce2 dv=booking-service thu_muc=rca/phat-lai
```

## Ba câu trả lời cho toàn bộ đầu ra G1

1. **Tính đúng và mức ảnh hưởng:** bản 5 sửa đúng các lỗi đã thống nhất; chưa thấy lỗi mới đáng kể. Phần phát lại trên `exp-obs` chưa được sửa xong vì dashboard còn bản 4.
2. **Kế hoạch dài hạn:** không cần đổi MRP, M1 hoặc hướng Grafana. G1 cung cấp giao diện xem kết quả đã lưu; chưa chứng minh hiệu quả M1 trên FlashTicket hoặc hoàn thành G3/LLM/demo tự động.
3. **Production, main và demo máy 84:** không thấy tác động trực tiếp từ phạm vi G1 đã kiểm. Không có sửa ứng dụng, push/merge hoặc chạy CD trong lượt này. Kết luận không thay kiểm toán các bước khác của T-062.

## ĐÃ CHỐT, được sửa

- **F1′, F2′, F3, F4:** đồng ý bản đã thực hiện trong repo và kiểm trên bản thử.
- **F5:** đồng ý đường thực hiện đã thống nhất. Chỉ mục thật mới đã được kiểm; còn hoàn tất triển khai, kiểm bản phục vụ và ghi nhận.
- Giữ N3, N4 và phần cách chấm N5 ngoài gói; khai đúng giới hạn.

Danh sách này ghi nhận đồng thuận kỹ thuật trong phạm vi Minh đã cho phép, không cấp thêm quyền.

## CÒN BẤT ĐỒNG

**Không còn bất đồng về phương án hoặc bản sửa trong repo.**

Còn thiếu bằng chứng hoàn tất triển khai: dashboard bản 5 và chỉ mục mẫu đã được nạp trên `exp-obs`, cùng thao tác đổi ca/menu/Explore trên bản phục vụ đó. Bản thử đúng và cấu hình máy đúng chưa loại trừ lỗi chỉ xuất hiện khi nạp hoặc tương tác thật. Hoàn tất phần kiểm ngắn của F5 sẽ phân xử; không cần chạy lại M1.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập bản sửa, diff bản 4, dữ liệu, truy vấn, nhánh dự phòng, ảnh và trạng thái triển khai; đối chiếu các lượt trước.
2. **File thay đổi:** tôi không sửa file nào. Chỉ mục thật được cập nhật trong lúc kiểm; đã đối chiếu riêng như trên.
3. **Kiểm đã chạy:** cú pháp, sinh trong bộ nhớ, manifest/hash, Infinity, đối chiếu dashboard đã nạp và SSH chỉ đọc; kết quả nêu trên.
4. **Đề xuất:** dừng phản biện **bản sửa trong repo**, hoàn tất F5 theo quyền đã duyệt rồi mới nghiệm thu bản triển khai. Mặt trái là gián đoạn ngắn Grafana khi khởi động lại. Phương án giữ bản 4 tránh lần khởi động này nhưng giữ lỗi diễn đạt đáp án, nên tôi không đề xuất.

Minh quyết dừng và nghiệm thu. Dừng phản biện không tự đóng T-062 hoặc trả lời xong các câu hỏi nghiên cứu.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, bước G1; tasks/T-062-dem-chang-1-4/SPEC.md, dòng G1; đề bài trong results/T-062/giao-dien/prompt-phan-bien-g1-luot4.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giao diện G2 của T-062; cổng nghiên cứu gần nhất đã duyệt G4.
- Người làm và người phản biện chính thức: người làm G1 là Claude; người phản biện G1 là Codex theo yêu cầu của Minh.
- Tài liệu gốc: AGENTS.md; tasks/T-062-dem-chang-1-4/SPEC.md, BOI-CANH.md, LOG.md, CHECKPOINT.md; results/T-061/dinh-dang-ket-qua-rca.md; results/T-059/danh-muc-loi.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md. Commit gốc c3d27f8a.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW-G1.md, REVIEW-G1-2.md, REVIEW-G1-3.md; results/T-062/giao-dien/phan-hoi-g1.md; bản phản biện G1 lượt 4 do Minh chuyển, đích lưu được prompt chỉ định là tasks/T-062-dem-chang-1-4/REVIEW-G1-4.md.
- Code và kết quả liên quan: results/T-062/giao-dien/; results/T-062/e2.py; results/T-062/ket-qua/; results/T-062/manifest.json. Dashboard triển khai ở exp-obs:/opt/flash-ticket-obs/pinned/provisioning/dashboards/. Môi trường Python: py -3 -B; Grafana thử tại http://127.0.0.1:3062. Hàm dashboard trong dung-dashboard.py có thể gọi trong bộ nhớ mà không chạy main.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Prompt bàn giao này không tự cấp thêm quyền ghi hoặc triển khai. Không thay đổi máy chủ; không đọc sổ tiêm lỗi, grafana.env hoặc file mật khẩu; không chạm máy 84.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1, R3/F5 | Đồng ý | Đã triển khai bản 5 lên `exp-obs` 02:01 UTC (sau khi phiên điều phối đẩy chỉ mục thật 01:52Z); hash khớp repo; log nạp không lỗi (`thay-doi.md`). Chưa kiểm tương tác trên Grafana thật (cần đăng nhập; phiên điều phối giao Codex) | |
| Điểm mới G-1…G-4 | (từ lượt kiểm Grafana thật của phiên điều phối) | G-1 liên kết bảng bằng chứng mã hóa hai lần: đúng, tái hiện được, phương án F6. G-2, G-3: phương án F7, F8. Chi tiết `results/T-062/giao-dien/phan-hoi-g1.md` §4; chờ reviewer chốt | |

