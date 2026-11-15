# Phản biện T-062 — G1, lượt 5

- **Người phản biện:** Codex — **Ngày:** 12/11/2026, kiểm đến khoảng 02:10 UTC.
- **Công đoạn:** kiểm lại phản hồi, bản 5 đã triển khai và đề xuất F6–F8.
- **Cổng nghiên cứu gần nhất:** G4.
- **Commit gốc:** `c3d27f8a`; đầu ra G1 chưa commit.
- **Phạm vi:** chỉ đọc và trả lời. Tôi không tự ghi file phản biện, sửa dashboard hoặc triển khai.
- **Đã đọc:** AGENTS, STATE; SPEC/BOI-CANH/LOG/CHECKPOINT T-062; nguồn DT18 và hướng dẫn của cô; phần liên quan trong MRP/WHY/DECISIONS/LESSONS và kế hoạch giai đoạn 2; định dạng T-061, danh mục T-059; code, dashboard, chỉ mục, kết quả và biên bản G1; phản biện lượt 1–4, phản hồi của Claude và bằng chứng kiểm Grafana thật.
- **Tự soát độc lập:** đọc nguồn và code gốc trước khi đọc kết luận cũ. Kiểm bằng tính toán trong bộ nhớ, truy vấn Infinity trên Grafana thử và SSH chỉ đọc tới `exp-obs`.

## Kết luận chung

**Đồng ý F6 và F8. Đồng ý có điều kiện với F7; cần chốt cách hiển thị trước khi coi toàn gói đã thống nhất. G-4 đã được sửa và triển khai trong bản 5.**

G1 vẫn đạt một phần: liên kết Explore từ bảng bằng chứng còn lỗi. Các bằng chứng đã kiểm không cho thấy giá trị đáp án lọt vào panel trang chính. G1 đáp ứng một phần giao diện minh họa của DT18, chưa hoàn thành chuỗi cảnh báo → RCA trực tuyến → LLM → demo.

Ba câu trả lời theo yêu cầu của Minh:

1. **Tính đúng và mức ảnh hưởng:** G-1 ảnh hưởng trực tiếp đường mở bằng chứng, mức trung bình và chặn nghiệm thu đầy đủ G1. G-2 cần diễn giải đúng dữ liệu rỗng. G-3 là nhãn điều hướng. G-4 đã xử lý.
2. **Kế hoạch dài hạn:** F6–F8 không đòi đổi MRP, thuật toán M1, định dạng kết quả 0.2 hoặc hướng Grafana. Chúng không bổ sung bằng chứng về hiệu quả RCA hay trả lời xong RQ5.
3. **Production/main/demo máy 84:** không thấy đường tác động trực tiếp từ gói sửa G1 trong phạm vi đã nêu. Compose và cấu hình datasource trên `exp-obs` vẫn khớp bản tham chiếu. Nếu triển khai bằng khởi động lại Grafana, giao diện quan sát có thể gián đoạn ngắn. Lượt này không truy cập máy 84, sửa nhánh hoặc push. Kết luận này chỉ bao phủ G1.

## Các điểm

### G-1 / F6. Liên kết bảng bằng chứng bị mã hóa hai lần — CHẶN nghiệm thu đầy đủ G1

- **Ở đâu:** `results/T-062/giao-dien/dung-dashboard.py:433`, hàm `panel_bang_chung`; áp dụng cho cả hai dashboard.
- **Sai gì:** cột `url` đã chứa phần `panes` được mã hóa. Liên kết `${__data.fields.url}` làm phần đó tiếp tục bị mã hóa khi Grafana dựng href.

**Bằng chứng:**

- Manifest của gói kiểm thật `results/T-062/codex/g1-that/manifest.json`: **67/67 file khớp hash**.
- Đếm lại `lien-ket-bang-bang-chung.json`: **47/47 href chứa `panes=%257B…`**. Giải mã tham số một lần chưa đọc được JSON; giải mã lần thứ hai đọc được.
- Truy vấn lại bảng bằng chứng của chín ca trên bản thử hiện tại: **47 URL nguồn đọc được JSON sau một lần giải mã**.
- Cả hai dashboard hiện tại vẫn dùng `${__data.fields.url}`.
- Bằng chứng kiểm thật đã lưu có lỗi “Could not parse Explore URL”.

Như vậy, lỗi nằm giữa URL do truy vấn trả về và href Grafana dựng. Việc truy vấn trả URL đúng chưa chứng minh liên kết bấm được.

**Đánh giá F6: đồng ý.**

Đổi đúng liên kết này thành:

```text
${__data.fields.url:raw}
```

Đây là cách sửa trực tiếp vào bước mã hóa thêm. Cú pháp `raw` cho phép giữ giá trị mà không áp dụng định dạng mặc định. [Tài liệu Grafana](https://grafana.com/docs/grafana/latest/visualizations/dashboards/variables/variable-syntax/#raw)

- **Phần có thể phản bác finding:** menu nút có liên kết Explore chạy được. Điều đó không bác bỏ lỗi của bảng; hai đường dựng URL khác nhau.
- **Sửa tối thiểu:** sửa hàm dùng chung, sinh lại hai dashboard. Sau sửa, bấm liên kết Tempo và Prometheus từ chính bảng; kiểm truy vấn và cửa sổ giữ nguyên.
- **Phương án khác đã xét:** đổi cách mã hóa trong truy vấn. Cách này chạm nhiều phần hơn và không cần thiết.
- **Mức ảnh hưởng:** trung bình; lỗi đã xảy ra ở đường mở bằng chứng.
- **Dài hạn:** không đổi hợp đồng dữ liệu hoặc phương pháp.
- **Production/main/máy 84:** không có tác động trực tiếp từ thay đổi này.

Tôi chưa bấm kiểm lại F6 trong lượt này vì công cụ trình duyệt báo không có browser access host. Không coi báo cáo thử của người làm là phép kiểm độc lập mới của Codex.

### G-2 / F7. Diễn giải dữ liệu rỗng đúng hướng, cách thay “No data” chưa chốt — KHÔNG CHẶN xem kết quả; CHẶN chốt nguyên văn F7

- **Ở đâu:** `phan-hoi-g1.md` §4; các panel 11 và 13 trong `dung-dashboard.py`.
- **Quan sát đã xác nhận:** đếm lại `codex/g1-that/lop-thao-tac-api.json` cho kết quả:
  - Panel HTTP 5xx rỗng ở **5 ca**.
  - Panel log có bộ lọc rỗng ở **7 ca**.
  - Những phản hồi này không có lỗi truy vấn.

Không có căn cứ gọi các ô rỗng đó là lỗi dashboard. Cũng chưa đủ căn cứ suy ra service không có lỗi.

**Đánh giá F7: đồng ý có điều kiện.**

Điều kiện cần chốt:

1. `noValue` dành cho **giá trị trường rỗng/null**. Nó chưa bảo đảm thay được trạng thái toàn panel khi truy vấn không trả dòng hoặc chuỗi nào. [Tài liệu Grafana](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/configure-standard-options/#no-value)
2. Nếu dùng `description` như phương án dự phòng đã đề xuất, phải viết **câu điều kiện**. Mô tả luôn có thể được xem, kể cả khi panel đang có dữ liệu.
3. Giữ nguyên thông báo lỗi datasource/truy vấn. Không đổi lỗi truy vấn thành thông báo “trả rỗng”.

**Phương án tối thiểu tôi đề xuất:** dùng mô tả cho cả hai panel, không cam kết đã thay trực tiếp chữ “No data”.

- HTTP 5xx: “Nếu truy vấn thành công nhưng không trả dữ liệu: chưa có chuỗi metric HTTP server 5xx khớp service và khung giờ đang chọn. Không suy ra service không có lỗi.”
- Log: “Nếu truy vấn thành công nhưng không trả dữ liệu: chưa có dòng log khớp service, khung giờ và bộ lọc error/exception/warn. Không suy ra service không có lỗi.”

Cách này không đổi truy vấn, không thêm số 0 giả và không cần thay loại panel. Mặt trái: chữ “No data” vẫn có thể còn; phần giải thích nằm trong mô tả.

Phương án khác là thay trực tiếp trạng thái rỗng bằng cơ chế riêng của panel. **Chưa kiểm** khả năng này trên bản 13.3.0 đang dùng; chưa có cấu hình hoặc bằng chứng đủ để chốt. Không cần làm thêm cơ chế đó để sửa phần diễn giải hiện tại.

- **Bước và quyết định chịu ảnh hưởng:** đây là phần triển khai chưa được phân xử, chưa phải lỗi đã xảy ra của bản sửa F7.
- **Mức ảnh hưởng:** thấp đến trung bình; ảnh hưởng cách hiểu dữ liệu thiếu.
- **Dài hạn:** không đổi MRP. Nguyên nhân truy vấn rỗng vẫn cần phân biệt nếu dùng làm kết luận về chất lượng quan sát.
- **Production/main/máy 84:** không có tác động trực tiếp nếu chỉ sửa mô tả.

**Phần còn mở về dữ liệu:** kết quả rỗng có thể do không có bản ghi khớp, thiếu ghi nhận/thu nhận, hoặc điều kiện nhãn và thời gian. Các phản hồi tổng hợp hiện có không tách hết những giải thích này. Nếu cần quy nguyên nhân, phải đối chiếu telemetry nguồn và tình trạng thu nhận của cùng service/cửa sổ qua phần B1/điều phối. Đây là việc đọc thêm dữ liệu đã có, không cần chạy lại M1; chi phí thao tác chưa đo trong lượt này. Kết luận phụ thuộc là nguyên nhân thiếu dữ liệu, không phải tính đúng của F6.

### G-3 / F8. Chữ “đáp án” ở điều hướng không phải giá trị đáp án — KHÔNG CHẶN

- **Ở đâu:** `dung-dashboard.py:511`, dòng 517 và guard ở dòng 530.
- **Quan sát đúng:** trang chính có chữ “đáp án” trong tên liên kết phát lại và mô tả dashboard.
- **Giới hạn diễn giải:** điều đó không chứng minh đáp án của ca đã lọt vào phần chẩn đoán.

Kiểm target của trang chính hiện tại không thấy các mẫu truy cập `phat_lai.`, `.phat-lai.json`, `danh-sach-phat-lai`, `thanh_phan_tiem` hoặc `tap_chap_nhan`.

**Đánh giá F8: đồng ý.**

Có thể đổi nhãn liên kết, mô tả và thêm từ cấm như đề xuất. Đây là điều chỉnh nhãn và phép kiểm văn bản. Guard không thay thế việc kiểm đường đọc dữ liệu; nó cũng không tạo phân quyền cho thư mục phát lại.

- **Phương án khác đã xét:** giữ nhãn hiện tại vẫn không làm lộ giá trị đáp án qua các panel đã kiểm. Chọn F8 để phù hợp cách diễn đạt mong muốn.
- **Mức ảnh hưởng:** thấp.
- **Dài hạn:** không đổi kế hoạch hoặc yêu cầu cách ly nhãn.
- **Production/main/máy 84:** không có tác động trực tiếp.

### G-4 / R1. Tập chấp nhận đã được biểu diễn đúng trong bản 5 — ĐÃ XỬ LÝ

**Đánh giá: đồng ý; không cần thêm sửa chức năng.**

SSH chỉ đọc xác nhận:

- Ba file provisioning trên `exp-obs` khớp local.
- Chỉ mục chính có chín ca, chỉ mục phát lại thật có chín ca, chỉ mục phát lại mẫu có hai ca; cả ba khớp local.
- **18/18 file kết quả chính/phát lại T-062 trên máy khớp local.**

Truy vấn lại hai dashboard trên chín ca: **36 khung nodes/edges** có số nút/cạnh đúng nguồn; tập nút mang dấu ◆ khớp tập chấp nhận của từng ca.

Với `f728fce2`, tập gồm `api-gateway` và `booking-service`; cả hai được đánh dấu. Hạng 4 và 1 vẫn là dự đoán M1. Không đổi thành kết luận M1 định vị đúng cạnh.

- **Mức ảnh hưởng trước sửa:** trung bình, thuộc diễn giải phát lại.
- **Dài hạn:** giữ đúng phân biệt root cạnh và tập chấp nhận mức nút.
- **Production/main/máy 84:** không có tác động trực tiếp.

`XONG.md:35`, dòng 80 và `phan-hoi-g1.md` §4 vẫn còn câu “chưa triển khai”. Chúng đã cũ so với biên bản triển khai và hash trên máy. Cần cập nhật trong lần sửa tài liệu G1 được phép; không cần triển khai lại bản 5 chỉ để xử lý những câu này.

## Đối chiếu các lượt trước

| Điểm | Đánh giá hiện tại | Bằng chứng và giới hạn |
|---|---|---|
| R1/N1, F1′–F2′ | Đúng; đã sửa và triển khai | Toàn tập chấp nhận được đánh dấu; dự đoán M1 giữ nguyên. |
| R2/F3 | Đã sửa đúng | Bỏ số nút rời cố định khỏi mô tả. |
| N2/F4 | Đã làm rõ đúng | Phân biệt hạng M1 trả với hạng dashboard hiện cho nhóm nghi ngờ. |
| R3/F5 | Phần triển khai đã hoàn tất | Dashboard và chỉ mục trên máy khớp local. Snapshot manifest 01:23 vẫn là lịch sử, không xác thực bản hiện tại. |
| N3 | Đúng trong phạm vi đã khai | Panel HTTP theo route chưa thay được biểu đồ cho span DB M1 gắn cờ. Không bổ sung TraceQL metrics trong lượt này. |
| N4 | Giữ giới hạn đã khai | Tách dashboard chưa tạo phân quyền file phát lại. F8 không xử lý điểm này. |
| N5 | Giữ giới hạn diễn giải | Không đổi cách chấm E2 trong G1; hạng mức nút không chứng minh định vị đúng cạnh. |
| Kết luận lượt 4 về bản triển khai còn cũ | Đúng tại thời điểm lượt 4; hiện đã thay đổi | Biên bản 02:01 và hash SSH hiện tại xác nhận bản 5. |
| Kết luận “không có lỗi mới đáng kể” của lượt 4 | Không bao phủ G-1 vừa được kiểm riêng | G-1 có bằng chứng href và lỗi Explore; cần F6. |

## Tuân thủ quy trình

- Giữ vai trò phản biện. Không ghi LOG/STATE, sửa file, triển khai, commit hoặc push.
- Không đọc sổ tiêm, file mật khẩu, dữ liệu khóa hoặc truy cập máy 84.
- Chín kết quả niêm phong khớp `manifest-ket-qua.json`. Chín bản phát lại khớp snapshot tương ứng; bỏ khối `phat_lai` thì bằng bản chính.
- Các file G1 đã đổi sau manifest 01:23 như biên bản đã khai. Tôi không dùng manifest cũ để xác nhận bản dashboard hiện tại; đã kiểm trực tiếp hash local và máy.
- Sửa `dung-dashboard.py` và sinh lại JSON sẽ đổi hash các file đã được snapshot ghim. G1 cần ghi nhận thay đổi theo F5; việc tạo snapshot mới vẫn thuộc phiên điều phối.
- Không có bằng chứng mới cho thấy G1 sửa ngoài phạm vi. Lượt này không kiểm toán mọi hành động của các phiên T-062 khác.

## Điều đã kiểm và thấy đúng

- Code Python phân tích cú pháp được.
- Hai dashboard sinh trong bộ nhớ khớp cấu trúc JSON hiện tại.
- Chỉ mục phát lại thật và mẫu sinh lại trong bộ nhớ khớp nội dung và byte theo quy ước xuống dòng Windows.
- Mẫu T-061 tiếp tục đọc được: `c12e47ab` không có dấu ◆; `f4a8c021` đánh dấu `event-service`.
- Compose và datasource trên `exp-obs` khớp bản tham chiếu sau T-061; Grafana 13.3.0 báo database `ok`.
- Không chạy lại thực nghiệm RCA.

## ĐÃ CHỐT, được sửa

Danh sách này ghi nhận phần đồng thuận kỹ thuật. **Điều kiện Minh đặt cho toàn gói vẫn phải được giữ: hiện cần chốt F7 trước khi coi hai bên không còn bất đồng.**

- **F6:** đổi liên kết bảng bằng chứng sang `${__data.fields.url:raw}`, sinh lại hai dashboard và kiểm bằng bấm liên kết thật.
- **F8:** đổi nhãn/mô tả trang chính và thêm phép kiểm từ cấm như đề xuất.
- **G-4:** không thêm sửa chức năng; giữ bản 5 đã triển khai.
- Giữ nguyên các sửa F1′–F5 đã thống nhất. Cập nhật câu bàn giao còn ghi “chưa triển khai” theo trạng thái thực tế.

## CÒN BẤT ĐỒNG

Chỉ còn **cách thực hiện và tuyên bố hoàn thành F7 cần chốt**:

| Bên | Phương án |
|---|---|
| Claude, `phan-hoi-g1.md` §4 | Thay “No data” bằng thông báo; kiểm `noValue` của logs, nếu không nhận thì ghi vào mô tả. |
| Codex | Chọn mô tả có điều kiện cho cả HTTP 5xx và logs. Không coi `noValue` là bằng chứng đã thay trạng thái panel rỗng. Không báo “đã thay No data” nếu chỉ thêm mô tả. |

Đây không phải bất đồng về số ca rỗng. Claude chưa có phản hồi với cách thực hiện cụ thể trên, nên chưa ghi nhận là đã chốt toàn bộ F6–F8.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập G-1…G-4, F6–F8, bản 5 trên máy và các điểm từ lượt trước.
2. **File thay đổi:** không tự sửa hoặc tạo file nào. Không commit/push.
3. **Kiểm đã chạy:** hash/manifest, tái sinh trong bộ nhớ, truy vấn Infinity, đối chiếu href và SSH chỉ đọc; kết quả nêu trên. Công cụ trình duyệt không khả dụng, nên chưa bấm kiểm độc lập F6.
4. **Cần chốt:** Claude đáp phương án F7 ở trên. Đề xuất chọn mô tả có điều kiện vì ít thay đổi và không làm sai nghĩa dữ liệu. Đánh đổi là còn chữ “No data”.

**Đề xuất tiếp tục một lượt đáp tập trung vào F7.** Không cần bàn lại F6, F8 hoặc chạy lại M1. Khi thống nhất, thực hiện trong quyền Minh đã cấp và kiểm phần chịu ảnh hưởng trước khi đề nghị nghiệm thu. Không tự đóng T-062 hoặc câu hỏi nghiên cứu.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, bước G1; tasks/T-062-dem-chang-1-4/SPEC.md; đề bài G1 trong results/T-062/giao-dien/prompt-phan-bien-g1-luot5.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: T-062, bước G1 giao diện Grafana; cổng nghiên cứu gần nhất đã duyệt là G4.
- Người làm và người phản biện chính thức: Claude là người làm G1; Codex là người phản biện G1 theo yêu cầu của Minh.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; tasks/T-062-dem-chang-1-4/SPEC.md, BOI-CANH.md, LOG.md, CHECKPOINT.md; results/T-061/dinh-dang-ket-qua-rca.md; results/T-059/danh-muc-loi.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md. Commit gốc c3d27f8a.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW-G1.md, REVIEW-G1-2.md, REVIEW-G1-3.md, REVIEW-G1-4.md, REVIEW-G1-5.md; results/T-062/giao-dien/phan-hoi-g1.md.
- Code và kết quả liên quan: results/T-062/giao-dien/; results/T-062/e2.py; results/T-062/ket-qua/; results/T-062/manifest.json; results/T-062/ket-qua/manifest-ket-qua.json; results/T-062/codex/g1-that/manifest.json. Grafana thử tại http://127.0.0.1:3062; truy vấn bằng results/T-062/giao-dien/kiem-truy-van.py. Bản triển khai tại exp-obs:/opt/flash-ticket-obs/pinned/provisioning/dashboards/.
- Phạm vi ghi được Minh cho phép trong lượt này: nếu chưa có quyền ghi riêng cho lượt đáp, chỉ trả lời trong chat. Quyền sửa G1 có điều kiện được ghi trong prompt lượt 5; không suy lượt bàn giao này thành quyền sửa bổ sung. Không sửa nội dung phản biện, LOG/STATE do phiên điều phối giữ hoặc file ngoài phạm vi được Minh duyệt.

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
| G-1 / F6 | Đúng; đã sửa | `${__data.fields.url:raw}`; bản thử bấm Tempo (`e8661e0a`) và Prometheus (phát lại, `a89954d1`) mở Explore đúng; triển khai `exp-obs` 02:20 UTC (bản 6, `thay-doi.md`). Chưa bấm trên Grafana thật đã đăng nhập | |
| G-2 / F7 | Đúng; nhận nguyên phương án reviewer | Mô tả có điều kiện cho panel 5xx và log; không nói đã thay "No data". Nguyên nhân rỗng chưa phân xử, ngoài G1 | |
| G-3 / F8 | Đúng; đã sửa | Nhãn liên kết và mô tả trang chính; bộ sinh chặn chữ "đáp án" và `tap_chap_nhan` ở trang chính | |
| G-4 | Đúng; đã xử lý ở bản 5 | Câu "chưa triển khai" cũ trong XONG đã sửa | |

