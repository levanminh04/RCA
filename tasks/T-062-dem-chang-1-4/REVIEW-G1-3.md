# Phản biện T-062 — G1, lượt 3

- **Người phản biện:** Codex — **Ngày:** 12/11/2026.
- **Công đoạn:** kiểm lại phản hồi và phương án sửa G1. Cổng nghiên cứu gần nhất đã duyệt: G4.
- **Bản lượt:** nội dung trả lời này; đích lưu do prompt chỉ định là `tasks/T-062-dem-chang-1-4/REVIEW-G1-3.md`. Tôi không tự ghi file.
- **Commit đã đối chiếu:** `c3d27f8a`. Đầu ra G1 chưa commit.
- **Đã đọc:** AGENTS, STATE; SPEC/BOI-CANH/LOG/CHECKPOINT T-062; nguồn DT18 và hướng dẫn của cô; phần trực tiếp liên quan trong MRP/WHY/DECISIONS/LESSONS và kế hoạch giai đoạn 2; định dạng T-061, quy tắc root/tập chấp nhận T-059; code, dashboard, chỉ mục, dữ liệu chính/phát lại, tài liệu và ảnh G1; hai lượt phản biện và phản hồi hiện tại.
- **Tự soát độc lập:** đọc yêu cầu và đầu ra gốc, lập nhận xét trước khi đọc kết luận các lượt trước. Kiểm thêm bằng tính toán trong bộ nhớ và SSH chỉ đọc tới `exp-obs`.

## Kết luận chung

**Đồng ý F1′, F2′, F3, F4 và F5. Không còn bất đồng chặn việc sửa theo gói này.** R3 của lượt 2 đã được xử lý trong phương án: có sinh lại chỉ mục, phân công cập nhật dữ liệu thật, dự phòng T-061 và ghi nhận thay đổi so với manifest.

Đây là đồng thuận về **phương án**, chưa phải xác nhận bản sửa chạy đúng. Code và bản triển khai vẫn chưa sửa; R1 còn chặn nghiệm thu phần đáp án phát lại. G1 vẫn đạt một phần mục tiêu giao diện minh họa, chưa hoàn thành chuỗi demo dài hạn trong MRP.

## Các điểm

### R1. Biểu diễn đáp án phát lại — CHẶN nghiệm thu phần đáp án; phương án sửa đã thống nhất

- **Ở đâu:** `dung-dashboard.py`, các hàm hiển thị danh sách, bản ghi, đồ thị và bảng hạng; `chi-muc-phat-lai.py`.
- **Lỗi hiện tại:** lấy riêng `thanh_phan_tiem` làm đáp án, trong khi E2 gán trường này bằng phần tử đầu tập chấp nhận.
- **Bằng chứng:** tại `results/T-062/ket-qua/phat-lai/f728fce2.phat-lai.json`:

| Con trỏ JSON | Giá trị |
|---|---|
| `/phat_lai/root_khai_truoc` | `api-gateway → booking-service (http)` |
| `/phat_lai/tap_chap_nhan` | `["api-gateway", "booking-service"]` |
| `/phat_lai/hang_trong_tap/api-gateway` | `4` |
| `/phat_lai/hang_trong_tap/booking-service` | `1` |
| `/phat_lai/hang_tot_nhat` | `1` |

Chỉ mục hiện tại chỉ đưa `api-gateway`, vai trò “bị kéo theo”, hạng 4 vào các trường đáp án đơn nút. Hash chỉ mục trên `exp-obs` khớp bản local đã kiểm.

**Phần phản bác đã xét:** `nhan_xet` và `dap_an_ho_loi` vẫn chứa root cạnh. Vì vậy không mất toàn bộ thông tin. Tuy nhiên, chúng không sửa được nghĩa của dấu đáp án duy nhất và cột “M1 xếp đáp án là”.

- **Sửa thống nhất:** F1′–F2′. Hiện root khai trước, toàn bộ tập chấp nhận và hạng từng thành phần; dấu ◆ chỉ nghĩa thuộc tập chấp nhận mức nút. Giữ nguyên dự đoán, số E2 và đồ thị M1.
- **Mức ảnh hưởng:** trung bình, thuộc diễn giải phát lại.
- **Dài hạn:** giữ đúng phân biệt định vị nút và định vị cạnh theo T-059; không cần đổi MRP hoặc M1.
- **Production/main/demo máy 84:** không có tác động trực tiếp trong phạm vi G1.

### R2. Số nút không có cạnh ghi cố định — KHÔNG CHẶN; phương án sửa đã thống nhất

- **Ở đâu:** mô tả panel đồ thị trong `dung-dashboard.py`.
- **Bằng chứng:** đếm tập `nut[].id` trừ hai đầu `canh[]` trên đủ hai mẫu T-061 và chín kết quả T-062: hai mẫu có 10 nút rời mỗi ca; chín ca thật có 9 nút rời mỗi ca. Kết quả T-062 khớp `/do_phu/thuc_the_khong_co_canh`.
- **Sửa thống nhất:** F3, bỏ số cố định và dẫn tới Độ phủ.
- **Mức ảnh hưởng:** thấp, sai mô tả; không đổi tính toán.
- **Dài hạn/production/main/demo máy 84:** không có tác động trực tiếp.

### R3. Đường cập nhật chỉ mục và manifest — đã xử lý trong phương án F5

**Đồng ý phản hồi của Claude.** F5 đã bao phủ những phần thiếu ở lượt 2:

- Sinh lại chỉ mục phát lại bản sao mẫu.
- Kiểm dữ liệu cũ, dữ liệu thật và trường hợp giả lập trong môi trường thử.
- Giao phiên điều phối sinh lại và đẩy chỉ mục phát lại thật.
- Không chạy lại M1 hoặc ghép lại đáp án.
- G1 ghi thay đổi và hash mới; không tự ghi đè manifest ngoài quyền.
- Chờ phiên điều phối xác nhận lượt kiểm Grafana thật kết thúc trước khi triển khai.

Có một giới hạn chuyển tiếp cần hiểu đúng. Áp đúng nhánh dự phòng F2′ được mô tả lên chỉ mục hiện có cho kết quả:

| Ca | Tập lấy từ chỉ mục cũ | Tập trong file phát lại |
|---|---|---|
| `f728fce2` | `api-gateway` | `api-gateway`, `booking-service` |
| `1ad3afeb` | `event-service` | `event-service`, `event_db` |

Nguồn: hai dòng tương ứng trong `ket-qua/phat-lai/chi-muc/danh-sach-phat-lai.json` và `/phat_lai/tap_chap_nhan` của hai file phát lại. Đây là kiểm nhánh dự phòng theo đề xuất, chưa phải chạy bản sửa.

**Giữ trường cũ bảo đảm tương thích; nó không khôi phục thông tin chưa có trong chỉ mục cũ.** Vì vậy không coi việc dashboard mới mở được với chỉ mục cũ là đã sửa xong R1.

Tôi đề xuất phiên điều phối **đẩy và kiểm chỉ mục mới trước khi G1 nạp dashboard mới**. Cách này tận dụng tương thích đã có, giảm khoảng thời gian danh sách và chi tiết khác nhau. Phương án dashboard trước rồi chỉ mục sau vẫn hoàn tất việc sửa khi làm đủ F5; tôi không coi khoảng chuyển tiếp này là lỗi chặn mới hoặc yêu cầu thêm vòng phản biện.

- **Mức ảnh hưởng:** trung bình trong triển khai; không đổi kết quả khoa học.
- **Dài hạn:** giữ đồng bộ hợp đồng dữ liệu G2, không đổi hướng Grafana hoặc MRP.
- **Production/main/demo máy 84:** không có đường triển khai trực tiếp tới các đích này. Khởi động lại Grafana có thể gián đoạn ngắn giao diện quan sát trên `exp-obs`.

## Đối chiếu các lượt trước

| Điểm/phương án | Kết luận lượt 3 | Căn cứ và giới hạn |
|---|---|---|
| **R1, N1** | **Đúng; đồng ý sửa.** | Dữ liệu thật xác nhận lỗi biểu diễn đáp án. Chưa xử lý trên code. |
| **R2** | **Đúng; đồng ý sửa.** | Đã đếm đủ hai mẫu và chín ca thật. |
| **R3** | **Đúng; phương án đã đáp ứng.** | F5 bổ sung đầu ra dẫn xuất, phân công, triển khai và ghi nhận manifest. |
| **Điều kiện F1/F2 lượt 2** | **Đồng ý; Claude đã nhận đủ.** | Phân biệt thiếu khóa với rỗng/null; dự phòng ở cả chỉ mục và file; không in `#null`; diễn đạt đúng đồng hạng và dấu ◆. |
| **F1′** | **Đồng ý.** | Thêm trường mới, giữ trường cũ trong giai đoạn chuyển; giữ nguyên `hang_tot_nhat` của E2, không tính lại. |
| **F2′** | **Đồng ý.** | Hiện toàn bộ tập, không đánh dấu khi tập rỗng, không biến hạng nút thành kết luận định vị đúng cạnh. |
| **F3** | **Đồng ý.** | Đủ sửa lỗi mô tả, không cần thêm phép tính. |
| **F4 / N2** | **Đồng ý.** | Ca `a5539fba`: `/do_phu/so_tra_hang = 17`; 16 nút bình thường cùng hạng 2. Đổi cách gọi, giữ nguyên số. |
| **F5** | **Đồng ý.** | Cần thực hiện đủ, gồm chỉ mục thật. Khuyến nghị triển khai chỉ mục trước như trên. |
| **N3** | **Đúng trong phạm vi đã nêu; giữ ngoài gói sửa.** | Lớp thao tác hiện là metric HTTP theo route; chưa cung cấp biểu đồ tương ứng mọi span DB M1 gắn cờ. TraceQL metrics vẫn là ứng viên chưa kiểm. |
| **N4** | **Đúng; giữ giới hạn đã khai.** | SSH chỉ đọc xác nhận URL phát lại không đăng nhập trả 200, API dashboard trả 401. Tách trang không tạo phân quyền file. |
| **N5** | **Đồng ý giới hạn diễn giải.** | Hạng thô E2 không tự là lỗi chấm. Không đổi cách chấm trong G1; không suy điểm nút thành đúng cạnh. |

**Ảnh hưởng của N2–N5:** N2 ảnh hưởng thấp đến cách hiểu số đếm; N3 giới hạn đào sâu thao tác; N4 ảnh hưởng quyền đọc đáp án; N5 ảnh hưởng diễn giải kết quả. Chúng không tự yêu cầu đổi MRP, M1 hoặc tác động trực tiếp tới production/main/máy 84.

## Tuân thủ quy trình

- Giữ vai trò phản biện. Không sửa file, không ghi LOG/STATE, không thay đổi máy chủ, không commit/push.
- Không đọc sổ tiêm lỗi, mật khẩu, `grafana.env`, dữ liệu khóa hoặc nội dung khóa truy cập. Không chạm máy 84.
- Kiểm 57 mục G1/E2/kết quả trong `results/T-062/manifest.json`: **56 khớp; `giao-dien/phan-hoi-g1.md` lệch**. Tôi dừng coi file này là đầu ra cũ đã xác thực và đánh giá nội dung hiện tại như đề xuất đang phản biện. Các số kết quả dùng ở trên lấy từ file đã kiểm toàn vẹn.
- Khi thực hiện F5, danh sách thay đổi sau snapshot cần ghi cả file phản hồi hiện đã lệch. Giữ nguyên snapshot cũ; phiên điều phối xử lý snapshot tiếp theo theo quyền.
- Không phát hiện lựa chọn thuật toán hoặc thay đổi tiêu chí chấm mới trong F1′–F5. Không mở lại các task đã nghiệm thu.

## Điều đã kiểm và thấy đúng

- Năm script Python phân tích cú pháp thành công.
- Hai dashboard sinh **trong bộ nhớ** trùng cấu trúc JSON đã lưu.
- Manifest ca **28/28**, kết quả chính **9/9**, mẫu gốc T-061 **2/2** khớp hash và kích thước.
- Chín bản phát lại có hash nguồn khớp; bỏ khối `phat_lai` thì cấu trúc dự đoán trùng bản chính.
- Chỉ mục chính đủ chín dòng, đúng mã, mốc, hash, số thực thể trả hạng và thứ tự thời gian.
- Ba file provisioning, hai chỉ mục trên `exp-obs` khớp local. Compose và cấu hình nguồn dữ liệu khớp các bản công khai đã ghi nhận.
- Với `a5539fba`, cửa sổ nền và sự cố trong JSON phủ **20:45:04–20:55:04 UTC**; không có căn cứ sửa dashboard sang mốc khác trong tin giao việc.
- Đã xem ảnh phát lại, đồ thị ca thật và Explore Tempo đã lưu. Đây là ảnh bản thử, không thay bằng chứng tương tác trên Grafana thật.
- Đối chiếu lại **64 file** trong ba thư mục G1, task và kết quả: không file nào đổi hoặc mất trong lượt này.

## Ba câu trả lời cho toàn bộ đầu ra G1

1. **Tính đúng và mức ảnh hưởng:** phần biểu diễn đáp án còn R1 mức trung bình; mô tả đồ thị và cách gọi số đếm ảnh hưởng thấp. Gói sửa đã thống nhất nhưng chưa thực thi, nên chưa nghiệm thu bản sửa.
2. **Kế hoạch dài hạn:** không cần đổi MRP, M1 hoặc hướng Grafana. G1 chưa hoàn thành dịch vụ RCA trực tuyến, đồ thị thao tác đầy đủ, LLM, diễn tập demo hoặc đánh giá RQ5. Các phần đó thuộc bước sau.
3. **Production, main và demo máy 84:** không thấy tác động trực tiếp từ phạm vi G1 đã kiểm. Kết luận này không thay kiểm toán các bước khác của T-062.

## ĐÃ CHỐT, được sửa

Đã thống nhất kỹ thuật đối với **toàn bộ F1′, F2′, F3, F4, F5**, theo phạm vi đã trình:

- Hai script G1; hai dashboard dẫn xuất; chỉ mục phát lại bản sao mẫu.
- Hợp đồng chỉ mục, bàn giao, nhật ký thay đổi và ảnh kiểm.
- Phiên điều phối cập nhật chỉ mục phát lại thật và xử lý snapshot.
- Giữ N3/N4 và phần cách chấm N5 ngoài gói; khai đúng giới hạn.

Danh sách này ghi nhận đồng thuận để áp dụng điều kiện Minh đã nêu. **Phiên này vẫn chỉ đọc, không tự triển khai.**

## CÒN BẤT ĐỒNG

**Không còn bất đồng chặn phương án sửa.**

Khuyến nghị đưa chỉ mục mới lên trước dashboard mới là đề xuất tối ưu thứ tự triển khai của Codex, không phải điều kiện chặn bổ sung.

Còn hai việc chưa được xác nhận bằng thực thi:

- **Bản sửa chạy đúng:** chưa có code sửa. Sau khi thực hiện, dùng các mẫu và ca thật đã có theo F5 để kiểm; không chạy lại M1.
- **Tương tác trên Grafana thật:** lượt này không có phiên đăng nhập; API trả 401. Lỗi cấu hình chỉ xuất hiện trên máy thật vẫn chưa được loại trừ. Một lượt kiểm đổi ca, mở menu và Explore trên phiên đã đăng nhập sẽ phân xử; chi phí là lượt kiểm ngắn, không thêm thực nghiệm.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập nguồn, code, dữ liệu và bản triển khai; đối chiếu từng phản hồi và phương án cuối.
2. **File thay đổi:** không sửa file nào; không thay đổi máy chủ hoặc nhánh Git.
3. **Kiểm đã chạy:** cú pháp, sinh dashboard trong bộ nhớ, manifest/hash, chỉ mục, bản phát lại, số nút rời, cửa sổ thời gian, nhánh dự phòng và SSH chỉ đọc; kết quả như trên.
4. **Điều cần Minh quyết:** đề xuất dừng phản biện **phương án** và chuyển sang thực hiện gói đã thống nhất theo quyền hiện có. Chưa đề xuất nghiệm thu bản sửa hoặc đóng task.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, bước G1; tasks/T-062-dem-chang-1-4/SPEC.md, dòng G1; đề bài trong results/T-062/giao-dien/prompt-phan-bien-g1-luot3.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giao diện G2 của T-062; cổng nghiên cứu gần nhất đã duyệt G4.
- Người làm và người phản biện chính thức: người làm G1 là Claude; người phản biện G1 là Codex theo yêu cầu của Minh.
- Tài liệu gốc: AGENTS.md; tasks/T-062-dem-chang-1-4/SPEC.md, BOI-CANH.md, LOG.md, CHECKPOINT.md; results/T-061/dinh-dang-ket-qua-rca.md; results/T-059/danh-muc-loi.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md. Commit gốc c3d27f8a.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW-G1.md, REVIEW-G1-2.md; results/T-062/giao-dien/phan-hoi-g1.md; bản phản biện G1 lượt 3 do Minh chuyển, đích lưu được prompt chỉ định là tasks/T-062-dem-chang-1-4/REVIEW-G1-3.md.
- Code và kết quả liên quan: results/T-062/giao-dien/; results/T-062/e2.py; results/T-062/ket-qua/; results/T-062/manifest.json. Dashboard triển khai ở exp-obs:/opt/flash-ticket-obs/pinned/provisioning/dashboards/. Môi trường Python: py -3 -B; hàm dashboard trong dung-dashboard.py có thể gọi trong bộ nhớ để đối chiếu mà không chạy main.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Prompt bàn giao này không tự mở rộng quyền ghi hoặc quyền triển khai. Không thay đổi máy chủ; không đọc sổ tiêm lỗi, grafana.env hoặc file mật khẩu; không chạm máy 84.

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
| R1–R3, F1′–F5 | Đồng ý; đã thực hiện F1′–F4 và phần G1 của F5 trong repo | Kiểm trên bản thử: `results/T-062/giao-dien/XONG.md` §2b; file đổi và hash: `thay-doi.md` mục "Bản 5". Chưa triển khai `exp-obs` (chờ phiên điều phối). Đồng ý khuyến nghị đẩy chỉ mục mới trước dashboard mới | |
| N3, N4, N5 | Đồng ý giữ ngoài gói | Đã khai ở XONG | |
