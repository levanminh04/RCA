# Phản biện T-062 — G1, lượt 2

- **Người phản biện:** Codex — **Ngày:** 12/11/2026.
- **Công đoạn/cổng:** kiểm lại phản hồi và phương án sửa G1; cổng nghiên cứu gần nhất đã duyệt: G4.
- **Bản lượt:** câu trả lời này, đích lưu do prompt chỉ định là `tasks/T-062-dem-chang-1-4/REVIEW-G1-2.md`. Tôi không tự ghi file.
- **Commit/diff:** mốc `c3d27f8a`; đầu ra G1 chưa commit.
- **Đã đọc:** AGENTS, STATE; SPEC/BOI-CANH/LOG/CHECKPOINT T-062; nguồn DT18 và hướng dẫn của cô; phần liên quan trong MRP/WHY/DECISIONS/LESSONS và kế hoạch giai đoạn 2; định dạng và bộ chuyển đổi T-061; quy tắc root/tập chấp nhận T-059; code, dashboard, chỉ mục, nhật ký, báo cáo và ảnh G1; E2, kết quả chính và phát lại T-062; REVIEW-G1 và phản hồi của Claude.
- **Tự soát độc lập:** đọc yêu cầu, code và đầu ra gốc trước khi đọc kết luận lượt 1 và phản hồi. Kiểm hash, tái sinh dashboard trong bộ nhớ, đối chiếu dữ liệu thật và bản triển khai bằng SSH chỉ đọc.

## Kết luận chung

**R1 và R2 đúng. Đồng ý hướng F1–F4, nhưng chưa chốt triển khai nguyên gói đề xuất hiện tại.** F1–F2 cần bổ sung việc sinh lại các chỉ mục đang tồn tại, phân công cập nhật chỉ mục chính và xử lý manifest đã ghim G1. Đây là thiếu sót của phương án triển khai, không phải lỗi đã xảy ra do sửa code.

G1 vẫn đạt một phần mục tiêu giao diện minh họa. Chưa có bằng chứng tương tác trên chính Grafana đã đăng nhập; việc này không được thay bằng hash khớp hoặc log nạp dashboard. Lượt phản biện này không đánh giá lại hiệu quả M1 hay đóng RQ5.

## Các điểm

### R1. Trang phát lại gọi riêng đầu tiên của tập chấp nhận là đáp án — CHẶN nghiệm thu phần đáp án

- **Ở đâu:** `dung-dashboard.py`, các hàm `panel_danh_sach`, `panel_su_co`, `panel_do_thi`, `panel_hang`; `chi-muc-phat-lai.py:36`.
- **Sai gì:** bản hiện tại lấy `thanh_phan_tiem` làm đáp án duy nhất. E2 gán trường này bằng phần tử đầu tập chấp nhận. Với lỗi trên tuyến, phần tử ấy không phải toàn bộ root cạnh.

**Bằng chứng mới từ dữ liệu thật:**

`results/T-062/ket-qua/phat-lai/f728fce2.phat-lai.json`:

| Con trỏ JSON | Giá trị |
|---|---|
| `/phat_lai/root_khai_truoc` | `api-gateway → booking-service (http)` |
| `/phat_lai/tap_chap_nhan` | `["api-gateway", "booking-service"]` |
| `/phat_lai/hang_trong_tap/api-gateway` | `4` |
| `/phat_lai/hang_trong_tap/booking-service` | `1` |
| `/phat_lai/hang_tot_nhat` | `1` |

Trong chỉ mục phát lại hiện tại, dòng có `ma = f728fce2` lại chứa:

- `dap_an_thanh_phan = api-gateway`;
- `m1_vai_tro_cua_dap_an = bị kéo theo`;
- `m1_hang_cua_dap_an = 4`.

Hash chỉ mục trên exp-obs khớp bản local đã kiểm. Vì vậy, lỗi không còn chỉ là nguy cơ trên dữ liệu tương lai: nguồn đang cấp cho dashboard đã biểu diễn riêng đầu hạng 4, trong khi đầu còn lại thuộc tập có hạng 1.

**Phần phản bác đã xét:** `nhan_xet` vẫn ghi đúng root cạnh và hạng tốt nhất. Vì thế không mất toàn bộ thông tin. Tuy nhiên, điều đó không sửa được nhãn “ĐÁP ÁN: thành phần bị tiêm” và dấu đáp án duy nhất trên đồ thị.

- **Bước chịu ảnh hưởng:** hiển thị phát lại; không đổi đầu ra M1.
- **Mức ảnh hưởng:** trung bình. Chặn nghiệm thu cách diễn đạt đáp án và định vị qua tập chấp nhận; không chặn xem dự đoán ở trang chính.
- **Dài hạn:** phải giữ phân biệt root cạnh, tập chấp nhận mức nút và khả năng định vị cạnh theo T-059. Không cần đổi MRP hoặc thuật toán.
- **Production/main/máy 84:** không thấy tác động trực tiếp từ lỗi này.
- **Sửa tối thiểu:** theo hướng F1–F2, kèm điều kiện triển khai tại R3. Không thêm cạnh giả và không diễn giải hạng nút thành bằng chứng M1 xác định đúng cạnh thật.

### R2. Mô tả cố định 10 nút không có cạnh — KHÔNG CHẶN

- **Ở đâu:** `dung-dashboard.py:336`, mô tả panel đồ thị.
- **Sai gì:** dùng số của mẫu T-061 cho dữ liệu T-062.
- **Bằng chứng:** phép đếm `nut[].id` trừ hai đầu của `canh[]` trên đủ đối tượng cho kết quả: hai mẫu T-061 có 10 nút rời mỗi ca; chín ca T-062 có 9 mỗi ca. Kết quả cũng khớp `/do_phu/thuc_the_khong_co_canh`.
- **Hậu quả:** mô tả sai mức quan sát; không đổi đồ thị hoặc hạng.
- **Mức ảnh hưởng:** thấp; không chặn sử dụng.
- **Dài hạn:** không ảnh hưởng lựa chọn phương pháp; tránh biến số của mẫu cũ thành hạn chế cố định.
- **Production/main/máy 84:** không có tác động trực tiếp.
- **Sửa tối thiểu:** đồng ý F3: bỏ số cố định, dẫn tới dòng Độ phủ.

### R3. F1–F2 chưa bao phủ đường cập nhật chỉ mục và manifest — CHẶN chốt triển khai nguyên gói

- **Ở đâu:** `phan-hoi-g1.md` §2, F1–F2 và đoạn “Kiểm sau khi sửa”.
- **Loại:** thiếu sót trong phương án triển khai; chưa có lỗi do triển khai bản sửa.

**Bằng chứng:**

1. F1 bỏ các trường chỉ mục cũ và thêm trường mới; F2 chuyển dashboard sang đọc các trường mới.
2. Cả chỉ mục mẫu lẫn chỉ mục phát lại thật hiện còn hợp đồng cũ:
   - `giao-dien/rca-ket-qua-mau/mau/phat-lai/chi-muc/danh-sach-phat-lai.json`;
   - `ket-qua/phat-lai/chi-muc/danh-sach-phat-lai.json`.
3. `e2.py:147` gọi script sinh chỉ mục khi thực hiện nhánh đẩy phát lại. Chỉ sửa script không cập nhật các file đã sinh.
4. Đoạn kiểm đề xuất chưa ghi bước sinh lại và đẩy hai chỉ mục ấy. Quyền G1 cũng cấm tự ghi `rca-ket-qua/` chính; phiên điều phối giữ quyền đó.
5. `results/T-062/manifest.json`, tạo lúc **01:23:11 UTC ngày 12/11**, hiện ghim script G1, dashboard JSON, chỉ mục mẫu và tài liệu G1. Các mục liên quan được kiểm đều khớp. Sửa các file này sẽ làm chúng khác snapshot đã ghim.

**Hậu quả:** dashboard mới có thể đọc chỉ mục cũ, khiến cột mới rỗng hoặc thiếu thông tin. Nếu tự cập nhật chỉ mục chính hay manifest ngoài quyền G1 thì vượt phạm vi. Nếu bỏ qua manifest, kiểm toàn vẹn sau đó sẽ thấy lệch.

Đây là điều kiện mới cần đưa vào phương án sửa. Không dùng manifest vừa tạo để quy lỗi hồi tố cho lượt phản biện trước.

**Đề xuất sửa tối thiểu:**

- G1 sửa code nguồn trước; sinh lại hai dashboard và chỉ mục phát lại **bản sao mẫu** trong phạm vi được phép.
- Cập nhật `dinh-dang-chi-muc.md` theo hợp đồng mới; cập nhật `XONG.md` và `thay-doi.md` theo việc thực tế.
- Phiên điều phối sinh lại chỉ mục phát lại thật từ các file phát lại đã có, rồi đẩy chỉ mục đó. Không cần chạy lại M1 hoặc ghép lại đáp án.
- Chốt thứ tự cập nhật chỉ mục/dashboard để dashboard mới nhận đủ trường mới. Có thể giữ trường cũ trong giai đoạn chuyển nếu cần.
- Nêu rõ cách ghi nhận bản sửa so với manifest hiện tại; G1 không tự ghi đè manifest ngoài phạm vi.
- Dùng ca thật `f728fce2` để kiểm nhánh root cạnh; giữ mẫu giả lập cho tình huống chưa có trong dữ liệu thật. Không cần chỉ dựa vào mẫu giả lập như đề xuất ban đầu.

**Phạm vi tác động cần chốt:**

| Nhóm | File hoặc nơi chịu ảnh hưởng |
|---|---|
| Code nguồn G1 | `chi-muc-phat-lai.py`, `dung-dashboard.py` |
| Đầu ra dẫn xuất G1 | Hai JSON dashboard; chỉ mục phát lại bản sao mẫu |
| Hợp đồng và bàn giao | `dinh-dang-chi-muc.md`, `XONG.md`, `thay-doi.md`, ảnh kiểm bản sửa |
| Phiên điều phối | Chỉ mục phát lại thật ở local/exp-obs; việc ghi nhận manifest sau sửa |

- **Mức ảnh hưởng:** trung bình đối với độ đúng và khả năng dùng bản sửa.
- **Dài hạn:** cần giữ đồng bộ hợp đồng cấp dữ liệu G2; không đòi đổi kế hoạch nghiên cứu.
- **Production/main/máy 84:** không có tác động trực tiếp nếu giữ đúng các đích trên. Khởi động lại Grafana có gián đoạn giao diện quan sát ngắn; không phải triển khai ứng dụng lên máy 84.
- **Phương án khác đã xét:** chỉ thêm trường, giữ trường cũ để giảm rủi ro chuyển tiếp. Cách này vẫn phải sinh lại chỉ mục để có dữ liệu mới; không thay được việc phân công cập nhật.

## Đối chiếu các lượt trước

### R1, R2 và N1–N5

| Điểm | Đánh giá và mức đồng thuận | Bằng chứng, giới hạn và cách xử lý |
|---|---|---|
| **R1** | **Đúng; đồng ý. CHẶN phần đáp án phát lại.** | Ca thật `f728fce2` xác nhận hậu quả cụ thể. Đồng ý sửa theo F1–F2; chưa coi đã xử lý vì code chưa sửa. |
| **R2** | **Đúng; đồng ý. KHÔNG CHẶN.** | Đã đếm đủ hai mẫu và chín ca thật. Đồng ý F3. |
| **N1** | **Đúng; đồng ý.** Trùng R1. | Dữ liệu thật hiện đã có, không còn cần chờ hết đợt để kiểm nhánh root cạnh. |
| **N2** | **Đúng một phần; đồng ý F4. KHÔNG CHẶN.** | Với `a5539fba`, M1 thực sự trả hạng cho 17 thực thể; 16 nút bình thường cùng hạng 2, nhóm có 16 phần tử và khóa toàn 0. Số 17/17 không sai. Điểm cần sửa là làm rõ khác biệt giữa hạng M1 trả và hạng được hiện trên nút. |
| **N3** | **Đúng trong phạm vi đã nêu; đồng ý chưa bổ sung panel lượt này. KHÔNG CHẶN.** | Bằng chứng keycloak là span DB; code lớp thao tác chỉ truy vấn metric HTTP theo route. Ảnh 12 và 14 phù hợp. Đề xuất TraceQL metrics vẫn **chưa kiểm**; không coi là phương án đã chọn hoặc bảo đảm thay được số M1 dùng. |
| **N4** | **Đúng; đồng ý giữ giới hạn đã khai trong G1. KHÔNG CHẶN phạm vi hiện tại.** | Đọc không đăng nhập URL phát lại thật trả HTTP 200; API dashboard trả 401. Tách trang không tạo cách ly quyền đọc file. Chưa có bằng chứng từ G1 rằng đáp án đi vào M1. |
| **N5** | **Đúng về phép lấy hạng; đồng ý có điều kiện với cách diễn giải. KHÔNG CHẶN G1.** | E2 lấy hạng của các nút trong tập, kể cả nhóm bình thường. Nhưng đó chưa tự là lỗi chấm: hạng thô là đầu ra hợp lệ của M1. Trong đủ 5 ca hiện có tập chấp nhận, hạng tốt nhất đều là 1 và thuộc nút `nghi_nguon`. Chưa có trường hợp hiện tại chứng minh hạng nhóm bình thường làm sai bảng này. Không đổi cách chấm E2 trong G1. |

**Ảnh hưởng của N2–N5:** N2 ảnh hưởng thấp đến cách hiểu độ phủ; N3 giới hạn mức đào sâu thao tác; N4 ảnh hưởng quyền tiếp cận đáp án khi dùng chung kho; N5 ảnh hưởng cách giải thích hạng. Chúng không tự đòi đổi MRP hay M1, và không tạo đường tác động trực tiếp tới production/main/máy 84.

Với N3, đề xuất giữ phạm vi hiện tại và khai rõ phần chưa có. Nếu mở rộng sau, cần đối chiếu nguồn thao tác M1 và khả năng truy vấn dữ liệu tương ứng; chưa đủ căn cứ chọn thêm panel ngay.

Với N4, đề xuất giữ giới hạn cho lượt thử đã niêm phong. Trước khi dùng trong bối cảnh cần phân quyền đáp án, Minh quyết nơi phục vụ và quyền đọc. Phương án khác là tách nguồn đáp án có xác thực; đổi hạ tầng đó chưa thuộc gói F1–F4.

### F1–F4

| Phương án | Kết luận | Điều kiện cụ thể |
|---|---|---|
| **F1** | **Đồng ý có điều kiện.** | Phân biệt trường **không tồn tại** với tập rỗng/null hợp lệ; giữ dự phòng T-061. Với nút thiếu dữ liệu, ghi không có hạng, không in `#null`. Nếu dùng `so_dong_hang`, ghi “nhóm n thành phần” hoặc trừ chính nút khi nói “n thành phần khác”. Giữ nguyên số E2; không biến nó thành kết luận xác định đúng root cạnh. Hoàn thiện R3 trước triển khai. |
| **F2** | **Đồng ý có điều kiện.** | Dự phòng T-061 phải áp dụng cả panel đọc file phát lại trực tiếp và panel đọc chỉ mục. Tập rỗng không đánh dấu nút nào. Dấu ◆ chỉ biểu thị thuộc tập chấp nhận, không khẳng định từng đầu là vị trí tiêm hoặc M1 đã định vị đúng cạnh. Kiểm bằng ca thật `f728fce2`; hoàn thiện R3. |
| **F3** | **Đồng ý.** | Nội dung đề xuất sửa đúng lỗi, không cần phép tính mới. |
| **F4** | **Đồng ý.** | Chỉ làm rõ nghĩa số đếm; giữ nguyên số, hạng và quy tắc ẩn hạng của nhóm bình thường. |

## Tuân thủ quy trình

- Tôi giữ vai trò phản biện, không ghi LOG/STATE, không sửa code hoặc máy chủ.
- Không đọc sổ tiêm lỗi, dữ liệu khóa, mật khẩu hoặc khóa dưới dạng nội dung. Không truy cập máy 84.
- Không chạy M1 hoặc thực nghiệm mới. Phép kiểm chỉ dùng kết quả đã lưu, mã và SSH chỉ đọc.
- Người làm đã tách tự soát, phản hồi và đề xuất chưa sửa. Tôi không coi việc hai bên đồng ý nguyên tắc là bằng chứng bản sửa chạy đúng.
- Bản triển khai vẫn là bản cũ khớp hash local; chưa phát hiện sửa F1–F4 trên máy thật.
- Không có căn cứ kết luận G1 thay đổi thiết kế nghiên cứu hoặc tiêu chí chấm. Không mở lại nghiệm thu T-059/T-061.

## Điều đã kiểm và thấy đúng

- **Toàn vẹn:** 28/28 mục manifest ca; 9/9 kết quả chính; hai mẫu gốc T-061; 57 mục liên quan G1/E2/kết quả trong snapshot T-062 đều khớp hash và kích thước.
- **Phát lại:** đủ 9 bản có hash nguồn khớp; bỏ khối `phat_lai` thì cấu trúc dự đoán trùng bản chính tương ứng.
- **Code:** bốn script Python phân tích cú pháp thành công. Hai dashboard sinh trong bộ nhớ trùng JSON đã lưu; byte cũng khớp khi giữ quy ước CRLF.
- **Chỉ mục chính:** đủ 9 dòng, đúng mã, mốc, trạng thái, kết luận, số đếm, hash và thứ tự thời gian.
- **Cách ly trang chính:** không chứa bốn mẫu truy cập đáp án mà bộ sinh cấm. Điều này xác nhận đường đọc được kiểm, không chứng minh phân quyền toàn hệ thống.
- **Triển khai:** ba file provisioning trên exp-obs khớp local. Compose và cấu hình nguồn dữ liệu khớp bản đã ghi nhận; log xác nhận hoàn tất nạp dashboard.
- **Tương tác thật:** chưa kiểm. API dashboard không đăng nhập trả 401. Tôi không đăng nhập hoặc đọc credential trong lượt này.

## Ba câu trả lời cho toàn bộ đầu ra G1

1. **Tính đúng và mức ảnh hưởng:** trang chính có bằng chứng về dữ liệu, biến và cấu trúc; phát lại còn R1 ảnh hưởng trung bình. F1–F4 đi đúng hướng nhưng chưa triển khai. R3 chặn chốt nguyên gói triển khai hiện tại.
2. **Kế hoạch dài hạn:** không cần đổi MRP, M1 hoặc hướng Grafana. Cần giữ nghĩa root/tập chấp nhận và hợp đồng dữ liệu G2. G1 chưa hoàn thành dịch vụ trực tuyến, lớp thao tác đầy đủ, LLM hoặc đánh giá RQ5.
3. **Production, main và demo máy 84:** không thấy đường tác động trực tiếp từ phạm vi G1 đã kiểm. Tôi không commit/push, không chạy CD, không truy cập máy 84. Kết luận này không thay kiểm toán các bước khác của T-062.

## ĐÃ CHỐT, được sửa

**Đã thống nhất về nội dung:**

- F3: bỏ số 10 cố định, dẫn tới Độ phủ.
- F4: làm rõ “M1 trả hạng”, giữ nguyên số liệu.
- Giữ N3/N4 và phần cách chấm N5 ngoài gói sửa hiện tại; khai đúng giới hạn, không nhận là đã giải quyết.

**Danh sách này chưa cho phép phát gói sửa riêng lẻ**, vì Minh yêu cầu chỉ sửa khi hai bên không còn bất đồng. Lượt này chỉ cho phép đọc và trả lời.

## CÒN BẤT ĐỒNG

**Còn một điểm chưa chốt: tính đầy đủ của đường triển khai F1–F2.**

- **Claude đề xuất:** sửa hai script, sinh dashboard, kiểm mẫu cũ và bản giả lập, rồi triển khai và ghi hash.
- **Codex đề xuất:** giữ hướng sửa ấy, bổ sung sinh lại chỉ mục mẫu và thật, phân công phiên điều phối đẩy chỉ mục chính, cập nhật hợp đồng/bàn giao và ghi nhận thay đổi so với manifest hiện tại. Kiểm thêm bằng ca thật đã có; không chạy lại M1.

Các điều kiện về null, tập rỗng, đồng hạng và dự phòng T-061 cần được người làm xác nhận trong phương án cuối. Chưa có phản hồi của Claude cho phần bổ sung này, nên chưa ghi “hai bên đã chốt”.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập đầu ra gốc; đối chiếu từng R1–R2, N1–N5 và F1–F4; kiểm đường triển khai và ảnh hưởng.
2. **File thay đổi:** không sửa file nào; không thay đổi máy chủ, commit hoặc push.
3. **Kiểm đã chạy:** cú pháp, tái sinh trong bộ nhớ, manifest/hash, chỉ mục, tập chấp nhận/hạng, số nút rời, đối chiếu provisioning và HTTP chỉ đọc. Kết quả đạt trong phạm vi nêu trên.
4. **Còn mở:** phương án triển khai tại R3 và tương tác trên Grafana thật. Một lượt kiểm ngắn trong phiên đã đăng nhập sẽ phân xử được giữa dashboard đã nạp và dashboard dùng đúng khi thao tác; không cần chạy lại M1.

**Đề xuất tiếp tục một lượt đáp để chốt R3 và các điều kiện F1–F2.** Sau đó có thể đề xuất dừng phản biện phương án. Nghiệm thu bản sửa vẫn cần bằng chứng thực thi; đồng thuận không thay bằng chứng, không đóng task hoặc mở thêm dữ liệu.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, bước G1; tasks/T-062-dem-chang-1-4/SPEC.md, dòng G1; đề bài và yêu cầu của Minh trong results/T-062/giao-dien/prompt-phan-bien-g1-luot2.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giao diện G2 của T-062; cổng nghiên cứu gần nhất đã duyệt G4.
- Người làm và người phản biện chính thức: người làm G1 Claude; người phản biện G1 Codex theo yêu cầu của Minh.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; tasks/T-062-dem-chang-1-4/SPEC.md, BOI-CANH.md, LOG.md, CHECKPOINT.md; results/T-061/dinh-dang-ket-qua-rca.md; results/T-059/danh-muc-loi.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md. Mốc Git c3d27f8a; đầu ra G1 chưa commit.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW-G1.md; results/T-062/giao-dien/phan-hoi-g1.md; bản Codex lượt 2 trong câu trả lời ngày 12/11/2026, đích lưu theo prompt là tasks/T-062-dem-chang-1-4/REVIEW-G1-2.md.
- Code và kết quả liên quan: results/T-062/giao-dien/; results/T-062/e2.py; results/T-062/ket-qua/ và phat-lai/; results/T-062/manifest.json; results/T-062/ca/manifest-ca.json. Bản triển khai: exp-obs:/opt/flash-ticket-obs/pinned/provisioning/dashboards/ và /opt/flash-ticket-obs/rca-ket-qua/; thông tin truy cập và triển khai trong SPEC, thay-doi.md và XONG.md.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Không sửa code, dashboard, chỉ mục, manifest, tài liệu hoặc máy chủ; không ghi LOG/STATE hay bảng phản hồi nếu chưa được Minh cấp quyền ghi cụ thể. Chỉ chạy lệnh đọc; không truy cập máy 84, không đọc mật khẩu, grafana.env hoặc sổ tiêm lỗi.

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
| R1 | Đúng; CHẶN phần đáp án phát lại | Tự kiểm: `results/T-062/ket-qua/phat-lai/` đã có 9 bản phát lại và chỉ mục; `f728fce2` đúng như reviewer nêu. Lỗi đã xảy ra trên dữ liệu đang cấp cho dashboard, không còn là nguy cơ. Sửa theo F1′–F2′ (`phan-hoi-g1.md` §3) | |
| R2 | Đúng; KHÔNG CHẶN | Giữ F3 | |
| R3 | Đúng; CHẶN chốt triển khai | Tự kiểm: `results/T-062/manifest.json` (`tao_luc_utc`) ghim 34 file `giao-dien/…`, gồm hai script, hai dashboard, chỉ mục mẫu, tài liệu, ảnh; `e2.py:147` chỉ sinh chỉ mục khi chạy nhánh đẩy. Chấp nhận mọi bổ sung của reviewer: F5 (sinh lại chỉ mục bản sao mẫu, cập nhật hợp đồng/bàn giao, ghi hash mới), phiên điều phối sinh lại và đẩy chỉ mục thật, G1 không sửa manifest mà liệt kê file đổi so với manifest. Giữ trường cũ trong giai đoạn chuyển để thứ tự triển khai không làm rỗng cột (`phan-hoi-g1.md` §3) | |
| F1/F2 điều kiện | Đồng ý toàn bộ điều kiện | Phân biệt trường không tồn tại với tập rỗng/null; dự phòng T-061 ở cả panel đọc chỉ mục và panel đọc file; thiếu dữ liệu không in `#null`; ghi "nhóm n thành phần"; giữ số E2 kèm "theo e2"; ◆ chỉ nghĩa "thuộc tập chấp nhận"; tập rỗng không đánh dấu; kiểm bằng ca thật `f728fce2` và mẫu giả lập | |
| N2–N5 | Đồng ý đánh giá của reviewer | N2 sửa bằng F4; N3, N4, phần cách chấm N5 để ngoài gói, khai giới hạn | |
