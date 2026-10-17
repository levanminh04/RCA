# T-035 — P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace

- **Trạng thái:** đã duyệt nội dung và tạo SPEC (14/10/2026); chưa triển khai.
- **Người làm:** Codex
- **Người phản biện:** Claude
- **Nguồn bản đề xuất:** Claude soạn bản 2 theo lời giao của Minh; Codex rà và ghi bản chốt theo lời duyệt ngày 14/10/2026. Không đổi vai trò người làm/người phản biện.
- **Nguồn duyệt:** Q-150 và LOG Phiên 1. Lời Minh: “đồng ý với các đề xuất, hiện tại tôi cần bạn tạo SPEC giúp tôi luôn, bám sát theo những thông tin đã chốt”. Lượt này ghi SPEC và tài liệu liên quan; chưa cài đặt hoặc chạy P5.
- **Thuộc gói MRP:** P5 — **Cổng:** G3
- **Task nối tiếp:** T-036 (P5b: nguồn kiến trúc, so hai nguồn), Codex làm, Claude phản biện; SPEC soạn sau khi T-035 có đặc tả v1.

## Mục tiêu

**Nguồn chi phối.**
- DT18-NV2 (`docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` §2, đoạn 2): nút là dịch vụ hoặc thành phần hệ thống; cạnh là gọi hàm, trao đổi thông điệp, phụ thuộc dữ liệu; log, trace, metrics ánh xạ lên đồ thị.
- Bước 1 của cô (`docs/reference/sources/advisor-2026-09-23.md` §1).
- MRP mục P5 và P9a; RQ3 (MRP §3) — task chưa trả lời RQ3.
- Quyết định Q-149, Q-150 trong `docs/DECISIONS.md`; WHY-52 (phụ lục của SPEC này).

**Câu hỏi của task.**
1. Mô hình đồ thị chung phải có gì để phủ cả dataset công khai lẫn FlashTicket?
2. Từ trace của hai dataset dev, mô hình đó dựng được tới đâu, ở mức thực thể và mức thao tác?
3. Mỗi quan hệ cần thông tin gì để có bằng chứng, và B16 cùng trace hiện có đáp ứng tới đâu?

**Loại task.** Đặc tả, cài đặt, mô tả. Không phân xử cơ chế RCA. Không đánh giá hiệu quả chẩn đoán.

**Trách nhiệm từng phần.**

| Phần | Trách nhiệm |
|---|---|
| T-035 | Mô hình chung (đủ nhu cầu FlashTicket); bộ dựng từ trace; kiểm bộ dựng trên ví dụ nhỏ có quan hệ phức tạp; đồ thị từ trace của hai dataset dev ở hai mức; độ phủ; bảng thông tin cần cho từng quan hệ, đối chiếu B16 và trace dev; danh sách phần còn thiếu, trình Minh. |
| T-036 | Nguồn kiến trúc của Train Ticket, Online Boutique, nguồn trong dataset và kiến trúc/cấu hình FlashTicket. Codex dựng danh mục thành phần và đồ thị tĩnh, ghi rõ phiên bản/revision nguồn; Claude phản biện. Đối chiếu độ phủ với đồ thị của T-035; cạnh có kiểu từ nguồn tĩnh. Đặc tả quy tắc đối chiếu với trace FlashTicket thật. |
| P9b | Cung cấp trace FlashTicket thật qua API và chuẩn hóa cùng định dạng nội bộ. Phần đối chiếu với nguồn tĩnh của T-036 khi có dữ liệu thật phải được giao trong SPEC tương ứng; chưa thực hiện trong T-035. |
| P9a | Làm rõ dữ liệu FlashTicket phải ghi để mọi quan hệ của mô hình có bằng chứng khi chạy. Dùng danh sách của T-035 và T-036. Mỗi yêu cầu Minh duyệt riêng; sửa hệ thống là đề xuất có phạm vi riêng. |
| P6 | Kiểm việc dùng mức thao tác có giúp phát hiện và chẩn đoán hơn mức dịch vụ không; chọn tín hiệu và cơ chế. |

**Phần mục tiêu nguồn được bao phủ.**

| Yêu cầu nguồn | T-035 | Chưa bao phủ, nơi xử lý |
|---|---|---|
| Nút dịch vụ, cơ sở dữ liệu, cache, broker, gateway, máy (DT18; Minh 14/10) | Có trong mô hình chung; kiểm trên fixture; trên dev ghi nút nào dựng được, nút nào thiếu | Quan hệ dịch vụ–cơ sở dữ liệu trên dev: T-036; FlashTicket: T-036 cho nguồn tĩnh, P9a cho yêu cầu quan sát, P9b cho dữ liệu thật và SPEC tương ứng cho đối chiếu |
| Cạnh gọi, thông điệp, dữ liệu, triển khai | Có trong mô hình; kiểm trên fixture; trên dev ghi loại nào dựng được | Như trên. Phần dữ liệu công khai thiếu được ghi là thiếu; không bỏ khỏi mô hình |
| Mức thao tác (Minh 14/10) | Mô hình hai mức; dựng trên dev; trả lời: dựng được không, có ý nghĩa không, còn thiếu gì | Có giúp chẩn đoán không: P6 |
| Nguồn tĩnh, so hai nguồn (MRP P5) | Không | T-036; đối chiếu với trace FlashTicket thật theo SPEC tương ứng khi có dữ liệu từ P9b |
| Đồ thị tham chiếu, ảnh chụp 60 s và 300 s (MRP P5) | Có, ở mức thực thể; mức thao tác chỉ toàn file, N, A | — |
| Ánh xạ log, trace, metric | Hợp đồng địa chỉ | Chọn tín hiệu: P6 |
| Phép tính P6 nào nhận cạnh (AGENTS 3.18) | Bảng ứng viên G2 × phần tử đồ thị, gồm cả mức thao tác | Chọn: spec P6 |
| Yêu cầu quan sát cho RCA (MRP P9a) | Bảng thông tin cần theo quan hệ, đối chiếu B16 và trace dev | Ban hành yêu cầu, sửa hệ thống: P9a, theo duyệt riêng |

**Kết cục dễ xảy ra nhất, nói trước (QT16).** Trên hai dataset dev, trace chỉ cho cạnh gọi chưa phân kiểu. Khi đó cạnh thông điệp và cạnh dữ liệu chỉ có bằng chứng ở fixture, nguồn tĩnh và FlashTicket.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Kết luận cần phân xử; cách hiểu khác | Phép kiểm và bằng chứng | Kết quả hỗ trợ, bác bỏ, chưa phân xử | Phần thiếu, quyết định phụ thuộc |
|---|---|---|---|---|
| C1. Trace từng dataset dev dựng được loại cạnh nào? | (i) Chỉ gọi chưa phân kiểu. (ii) Tên thao tác đủ phân kiểu một phần. | Đếm toàn bộ từ vựng thao tác; luật tường minh, không đoán bằng biểu thức chính quy (SL34). | Ba trạng thái: dựng được, không dựng được, chưa phân xử; mỗi trạng thái kèm ví dụ. | T-036; P9a |
| C2. Cạnh cha–con khác thực thể có là lời gọi phía gọi → phía được gọi? | Đúng; có span trung gian; không xác định được. | Số span mỗi lời gọi; quan hệ bao thời gian cha–con; kiểm tay hai trace mỗi dataset. | Theo dataset. Ở RE2-TT "không xác định được" là kết quả hợp lệ (G2-H19, mã D6). | Định nghĩa "lời gọi"; UV-1, UV-2 |
| C3. Cấu trúc đổi theo ca và cửa sổ không? | Gần hằng; đổi theo cửa sổ. | Số đồ thị khác nhau ở toàn file, N, A, ảnh chụp 60 s và 300 s; cạnh chỉ có ở một phía. Báo theo ca, theo ô. | Mô tả. | P6; đối chứng giữ bậc ở P7 |
| C4. Thiếu nút, thiếu cạnh ở đâu? | Không được gọi; thiếu instrumentation; mất span cha; cửa sổ ngắn. | Số đếm độ phủ của bộ dựng; script báo cáo riêng ghép nhãn. | Tái lập hoặc giải thích chỗ lệch với G2-H19. Nguyên nhân thiếu phần lớn không phân xử được. | Tập ứng viên spec P6; P9a |
| C5. Mỗi ứng viên G2 cần phần tử đồ thị nào? | — | Bảng ứng viên × phần tử (thực thể, thao tác, cạnh có hướng, cha–con trong trace, cửa sổ). | Mô tả; không chọn. | Spec P6 |
| C6. Cột `Node` của Nezha-OB mang nghĩa gì? (Minh 14/10) | Máy chạy pod (ánh xạ pod → máy); tên khác, ví dụ cụm hay vùng; giá trị hằng hay rỗng; không xác định được. | Đọc README, bài báo, mã của Nezha để tìm định nghĩa. Qua adapter, chỉ cửa sổ ca dev: số giá trị khác nhau; mỗi pod gắn mấy `Node`; mỗi `Node` chứa mấy pod; ổn định theo thời gian. Đối chiếu tên `Node` với nhóm cột `Node*` của metric (chỉ tên cột). Trong task chỉ đọc tên cột `Node*`, không bổ sung quyền đọc chuỗi số `Node*`. | Chỉ nhận nghĩa "máy" khi tài liệu hoặc mã thu thập chỉ ra `Node` là định danh host cụ thể. Ánh xạ ổn định và khớp nhóm cột `Node*` chỉ kiểm tính nhất quán; thiếu nguồn xác nhận thì "chưa phân xử", không dựng cạnh triển khai đã xác nhận. | Có dựng cạnh triển khai cho Nezha-OB không. Nếu có, câu ở G2 mục 6.2 cần thu hẹp; trình Minh, không tự sửa gói G2 |
| C7. Mức thao tác dựng được không? (Minh 14/10) | Tên ổn định, phân biệt được thao tác; tên chứa ID hoặc URL biến đổi; tên chung chung che nhiều thao tác. | (a) Tên ổn định: số tên khác nhau theo ca và cửa sổ; tên chỉ có ở một ca; tỷ lệ tên chứa chuỗi giống ID (báo ra, không tự chuẩn hóa). (b) Phân biệt: tên trùng giữa dịch vụ; với mỗi tên, số "chữ ký con" khác nhau (tập thao tác con trực tiếp); tên chỉ gồm phương thức HTTP. (c) Quan hệ giữa thao tác: số cặp cha–con **cùng dịch vụ** và **khác dịch vụ**; độ sâu lồng trong một dịch vụ; span mồ côi ở mức thao tác. | "Dựng được" khi tên ổn định giữa các ca dev và quan hệ cha–con giữa thao tác resolve được. "Có ý nghĩa" ở P5 chỉ hiểu là mức thao tác chứa phân biệt mà mức dịch vụ không có (mục C8). Không suy ra lợi ích chẩn đoán. | P6 có dùng mức thao tác không; yêu cầu tên thao tác ổn định cho FlashTicket (P9a) |
| C8. Đồ thị mức thao tác so với mức dịch vụ ra sao? | Mức thao tác chỉ là bản chi tiết hơn; hay mang thêm cấu trúc. | Chiếu đồ thị thao tác lên mức dịch vụ: phải ra đúng đồ thị dịch vụ (kiểm nhất quán). Đếm cạnh dịch vụ do nhiều cặp thao tác mang; cạnh trong cùng dịch vụ (mức dịch vụ không thấy); số cấu trúc khác nhau giữa các ca ở mỗi mức. | Mô tả. Không dùng nhãn. | P6 |
| C9. Mỗi quan hệ cần thông tin gì, B16 và trace dev có chưa? (Minh 14/10) | — | Bảng quan hệ × thông tin cần (trường, khóa nối) × B16 (mục, có/không/một phần) × trace RE2-TT × trace Nezha-OB × FlashTicket chạy thật (chưa được cung cấp hoặc chưa kiểm trace trong phạm vi task). | Mỗi ô có trích dẫn nguồn. Phần thiếu viết thành yêu cầu cụ thể, mỗi yêu cầu có lý do và quan hệ nó phục vụ. | Minh duyệt từng yêu cầu; P9a; sửa hệ thống là đề xuất riêng |

## Đầu vào

- **Dữ liệu dev:** 30 ca RE2-TT và 22 ca Nezha-OB, chọn qua allowlist và mã ca ẩn danh của `src/p3`. Không đọc `data/locked/`, ô test Nezha-OB, Eadro, các ca mẫu RCAEval khác.
- **Miền của “toàn file”:** với RE2-TT, là toàn bảng span trong file trace của đúng ca dev qua selector. Với Nezha-OB, là toàn tập span adapter trả trong cửa sổ dev được phép, không phải mọi span trong file nguồn. `src/p3/nezha.py::_doc_cua_so` đặt khoảng `[t−300 s, t+300 s)` và chỉ giữ span bắt đầu không trước biên trái, kết thúc trước biên phải. Đặc tả v0 và thống kê ghi rõ miền thời gian, quy tắc giữ span và tên miền theo dataset; không suy độ phủ toàn file nguồn từ cửa sổ Nezha. Làm rõ này không mở rộng quyền đọc dữ liệu.
- **Nguồn bổ sung của Nezha-OB:**
  - README, bài báo, mã đã tải: `results/T-008/sources/`; mã trong `data/ngoai-rcaeval/nezha/` nếu có.
  - Tên cột của `source_50.csv`, `destination_50.csv`.
  - Cặp Source–Target của `dependency.csv`; không đọc Weight và chuỗi số.
  - Cột `Node` và tên pod gốc của log, qua bộ đọc bổ sung trong `src/do_thi/`, chỉ cửa sổ ca dev (Q-63). Bộ đọc dùng lại việc chọn file và kiểm allowlist, đường dẫn, hash, đồng hồ; lọc thời gian trước khi xuất giá trị. `src/p3/nezha.py` hiện không xuất `Node`; không sửa bộ đọc baseline để lấy trường này.
  - Tên cột chứa cặp dịch vụ và các cặp Source–Target chỉ dùng đối chiếu mô tả. Khai nguồn sinh và phạm vi thời gian, kể cả khả năng tổng hợp cả test; không dùng chúng bổ sung cạnh cho bộ dựng từ trace hoặc chọn thiết kế P6. Chưa xác minh nguồn sinh thì giữ OPEN về tính độc lập và phạm vi diễn giải.
- **Mã dùng lại:** bộ đọc và định dạng nội bộ của `src/p3`; alias và universe đã duyệt (WHY-26, WHY-37). Ghi hash `src/p3` vào LOG.
- **Toàn vẹn đầu vào:** kiểm manifest phù hợp trước khi dùng đầu ra cũ. `cases.json` của T-002 đã khớp `handoff-manifest.json`; thẻ `the-rcaeval.md` lệch manifest cũ, không dùng thẻ đó làm nguồn số. Với đầu ra chưa có manifest phủ, dừng phần phụ thuộc và trình Minh; không tự ghi hash mới rồi coi là xác minh nguồn cũ.
- **Đối chiếu:**
  - `results/T-002/local-inspection/run-002/cases.json`;
  - `results/T-008/runs/evidence-002/summary.json`;
  - `results/T-034/` theo `runs/manifest-cuoi-007/manifest.json`;
  - `src/circa_kien_truc/builder.py::service_calls`.
- **FlashTicket, chỉ đọc:** `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md` và tài liệu kiến trúc trong `docs/architecture/` để lấy danh sách thành phần và quan hệ cần mô hình hóa. Không sửa repo đó.
- **Môi trường:** laptop, `py -3`, `py312-pin` (WHY-15). Không EC2, không tải.

## Đầu ra

Trong `results/T-035/`, trừ mã.

1. `dac-ta-do-thi.md` — đặc tả hình thức. Bản v0 viết trước khi chạy dữ liệu; bản v1 ghi từng chỗ đổi; giữ cả hai. Gồm:
   - **Mức thực thể:** kiểu nút dịch vụ, gateway, cơ sở dữ liệu, cache, broker, nhà cung cấp danh tính, đối tác ngoài không có telemetry nội bộ, máy.
   - **Mức thao tác (tùy chọn):** nút thao tác, quan hệ "thuộc về" thực thể; quy tắc chiếu lên mức thực thể.
   - **Kiểu cạnh:** `gọi-đồng-bộ` (cần loại span); `gọi-chưa-phân-kiểu`; `thông-điệp` (phát → broker → nhận; cạnh logic gửi → nhận cần bằng chứng nối bản tin cụ thể, nguồn "suy ra"); `dữ-liệu` (dịch vụ → cơ sở dữ liệu hoặc cache, từ thuộc tính span hoặc nguồn tĩnh); `triển-khai` (thực thể → máy).
   - Mỗi nút, mỗi cạnh ghi nguồn bằng chứng: trace, nguồn khác của dataset, tĩnh, suy ra.
   - Định nghĩa "lời gọi", "phía gọi", "phía được gọi", "span mồ côi", "đồ thị tham chiếu", "ảnh chụp".
   - Các trường hợp FlashTicket phải mô tả được: Saga và bù trừ; callback từ đối tác ngoài; tác vụ theo lịch không có bên gọi; outbox; retry và xử lý lặp (B16 §3).
   - Hợp đồng địa chỉ cho log, trace, metric ở hai mức. Tên thao tác kèm thực thể chủ quản phải phân biệt được nút; không tạo nút theo từng mã đơn hoặc từng lần thực thi. Giữ thao tác gốc, thao tác nội bộ và thao tác không gọi thực thể khác.
   - Quy tắc nối thông điệp: cùng `correlationId` giao dịch không đủ để ghép gửi–nhận. Cần ngữ cảnh tạo thông điệp/link có nghĩa đã xác minh, hoặc định danh bản tin trong phạm vi broker/đích phù hợp; phân biệt bản tin với lần giao lại và lần xử lý. Broker, đích hàng đợi/chủ đề và khóa gắn metric phải có địa chỉ rõ; thiếu thì ghi phần chưa xác định, không tự ghép các bên chỉ vì cùng broker.
   - Quy tắc chiếu: định nghĩa rõ cạnh thao tác nội bộ nào không thành cạnh giữa thực thể; giữ thống kê nội bộ riêng. Có cách giữ thành phần không có thao tác quan sát được, không tạo thao tác giả. So cùng tập nút/cạnh quan sát; inventory và độ phủ được báo riêng. Metric của cả dịch vụ là bối cảnh chung, không sao thành bằng chứng độc lập của từng thao tác.
   - Bảng C5.
2. `src/do_thi/` — bộ dựng. Nhận định dạng span mở rộng: các cột của `src/p3` cộng các cột tùy chọn loại span, thuộc tính, link. Có bộ chuyển từ định dạng `src/p3`, điền rỗng cho cột không có. Bộ đọc bổ sung C6 nằm trong cùng phạm vi mã; chỉ xuất `PodName`, `Node` và trường cần kiểm đã qua lọc dev. Không thay đổi đầu ra baseline.
3. `fixture/` — ví dụ nhỏ, kèm kết quả mong đợi viết tay. Tối thiểu:
   - (F1) một dịch vụ gọi nhiều dịch vụ, có gọi song song;
   - (F2) nhiều dịch vụ dùng chung một cơ sở dữ liệu, và một cache;
   - (F3) bên gửi phát thông điệp; bên nhận xử lý sau khi bên gửi đã kết thúc, nối bằng link, không bằng quan hệ cha–con;
   - (F4) retry và xử lý thông điệp lặp;
   - (F5) Saga có bước bù trừ;
   - (F6) callback từ đối tác ngoài, trace mới;
   - (F7) tác vụ theo lịch, không có bên gọi;
   - (F8) chu trình gọi A → B → A;
   - (F9) thao tác lồng trong cùng dịch vụ;
   - (F10) span mất cha; khóa span trùng; cửa sổ rỗng; thực thể ngoài alias;
   - (F11) hai dịch vụ cùng một máy.

   Fixture chỉ kiểm cách dựng quan hệ, không là bằng chứng hiệu quả chẩn đoán.
4. `do-thi/<dataset>/<mã ca ẩn danh>/<mức>/<cửa sổ>.json` — không lưu bảng theo span.
5. `thong-ke-do-thi.json`, `thong-ke-do-thi.md` — C3, C4, C8.
6. `tu-vung-thao-tac.json` — C1, C7.
7. `cot-node-nezha.md` và `.json` — C6, kèm trích nguồn của Nezha.
8. `do-phu-theo-nhan.json` — script báo cáo riêng, chỉ để phân tích.
9. `kiem-dung-dan.md` — K1–K8, kiểm tay.
10. `thong-tin-theo-quan-he.md` — C9, gồm danh sách yêu cầu còn thiếu, mỗi yêu cầu có lý do. Là nội dung để Minh duyệt; không sửa P9a hay B16.
11. `manifest.json`.

Mọi số có đường dẫn và con trỏ JSON.

## Phạm vi ghi

- `results/T-035/`
- `src/do_thi/`
- `tasks/T-035-p5-do-thi-tu-trace/LOG.md`
- Dòng T-035 trong `docs/STATE.md`
- `docs/WHY.md`: chỉ nối nguyên văn WHY-52 ở phụ lục SPEC, nếu Minh duyệt cùng SPEC

Không sửa `src/p3/`, `src/circa_kien_truc/`, kết quả của task cũ, repo FlashTicket.

## Các bước

0. Mở phiên; kiểm hash đầu vào; ghi LOG.
1. Đặc tả v0, gồm mô hình chung và kết quả mong đợi của fixture. Phụ thuộc: không.
2. Đọc nguồn Nezha cho C6; đếm từ vựng thao tác (C1, C7a–b). Phụ thuộc: bước 0; song song với bước 1.
3. Cài `src/do_thi/` và test fixture F1–F11. Phụ thuộc: bước 1. Kết quả mong đợi viết trước khi chạy bộ dựng.
4. Chạy trên 52 ca: mức thực thể ở toàn file, N, A và ảnh chụp 60 s, 300 s (chỉ RE2-TT); mức thao tác ở toàn file, N, A. Khảo sát cột `Node` qua adapter. Ghi tiến độ và thời gian từng ca (SL25). Giữ mọi lượt, kể cả lượt hỏng.
5. K1–K8. Phụ thuộc: bước 4.
6. Script báo cáo ghép nhãn. Phụ thuộc: bước 4.
7. Đặc tả v1; bảng C5; `thong-tin-theo-quan-he.md`. Phụ thuộc: bước 2, 5, 6.
8. Tự kiểm (AGENTS mục 5 bước 4); manifest; mục kết thúc LOG; prompt bàn giao.

Dừng khi thử cùng một chỗ 3 lần không được, hoặc K3 lệch mà chưa tìm ra nguyên nhân (QT5).

## Kiểm đúng đắn

- **K1 — Bảo toàn:** định nghĩa phân hoạch span gốc, có cha tìm được, mồ côi; chính sách khóa trùng/không hợp lệ được ghi trong v0 và kiểm ở F10. Mỗi cạnh có bằng chứng đúng loại: cặp cha–con cho lời gọi, ngữ cảnh/link hoặc định danh cho thông điệp, thuộc tính endpoint cho dữ liệu, định danh host đã xác nhận cho triển khai. Đếm riêng sự kiện làm chứng và cạnh đã gộp; quan hệ nội bộ không bị tính thành lời gọi giữa thực thể.
- **K2 — Tất định:** chạy hai lần giống hệt; `PYTHONHASHSEED` 0, 1, 2 (WHY-30: bộ dựng CIRCA đổi cạnh theo seed ở 24 ca).
- **K3 — Số đã có, RE2-TT, toàn file:**
  - nút/cạnh 27/55 ở 24 ca, 20/20 ở 5 ca, 21/21 ở 1 ca. Nguồn: `results/T-002/local-inspection/run-002/cases.json`; chọn các phần tử có `dataset = re2tt`, đếm độ dài `trace.graphs.full.nodes` và `trace.graphs.full.edges` (ví dụ con trỏ `#/3/trace/graphs/full`). Đây là tập nút thấy trong span, không phải toàn universe;
  - tổng span 22.834.238; cha tìm được 22.437.039 trên 22.639.789. Cùng tập phần tử ở trên, cộng `trace.n_spans`, `trace.parent_resolved_count`, `trace.parent_reference_count` (ví dụ `#/3/trace/n_spans`, `#/3/trace/parent_resolved_count`, `#/3/trace/parent_reference_count`);
  - `docs/knowledge/K2` ghi 2 đồ thị, T-002 ghi 3: chưa giải thích.
- **K4 — Bản cài độc lập:** tập cạnh bằng tập cạnh của `service_calls` trên cùng khoảng; khác thì giải thích bằng quy tắc cắt.
- **K5 — Nhất quán hai mức:** phép chiếu được định nghĩa trong v0 phải ra đúng phần đồ thị thực thể tương ứng, ở mọi ca và cửa sổ. Phân biệt cạnh nội bộ, quan hệ thuộc về, thành phần không có operation và inventory; không bịa thao tác để đạt phép chiếu.
- **K6 — Nezha-OB:** so cạnh trace với cặp cạnh của `source_50`, `destination_50`, `dependency.csv`, hai chiều. Ghi kết quả đọc nguồn về chuyện các file này có suy từ chính trace hay không; nếu chưa rõ thì ghi là không độc lập đã xác nhận.
- **K7 — Fixture:** F1–F11 khớp kết quả mong đợi viết tay.
- **K8 — Kiểm tay và đối chiếu nhãn:** hai trace mỗi dataset, đi từ dòng span tới cạnh ở hai mức; ca nhiều span mất cha (G2-H19, mã D5). Script báo cáo đối chiếu G2-H19: 8 ca root không được gọi, 7 ca cạnh quá thưa, tổng 15/52 (`results/T-034/goi-g2.md`; con trỏ trong `runs/g2-build-008/render/registry.json`). Tra định nghĩa "quá thưa" của T-032 trước khi so; không ép khớp.

**Không kiểm được trong task, và hệ quả.**
- Kiểu thật của cạnh ở RE2-TT: không phân xử được bằng dữ liệu hiện có.
- Đồ thị khớp kiến trúc không: T-036.
- Cạnh vắng là "không phụ thuộc" hay "không được gọi": không phân xử được.
- Trace FlashTicket thật: chưa được cung cấp hoặc chưa kiểm trong phạm vi task. Việc tìm không thấy cấu hình trong một số file không xác nhận toàn hệ thống không có trace; chưa gọi API runtime. Phần xác minh được bàn giao cho P9a/P9b theo nguồn thực tế và phạm vi được Minh duyệt.
- Lợi ích của mức thao tác: P6.

## Tiêu chí xong

1. Mô hình chung có đủ nút dịch vụ, cơ sở dữ liệu, cache, broker, gateway, máy và cạnh gọi, thông điệp, dữ liệu, triển khai. Mỗi phần ghi căn cứ (DT18, nhu cầu FlashTicket, nhu cầu kỹ thuật). Phần dữ liệu công khai thiếu được ghi "thiếu ở dataset X", không bị bỏ khỏi mô hình.
2. C1 có câu trả lời theo dataset và loại cạnh, ở một trong ba trạng thái, bằng bảng từ vựng.
3. C2 có định nghĩa "lời gọi" kèm bằng chứng theo dataset, hoặc ghi là giả định kèm phép tính phụ thuộc.
4. C3 phân biệt "gần hằng" với "đổi theo cửa sổ", báo theo ca.
5. C4: mọi thực thể trong universe có trạng thái độ phủ; K8 khớp G2-H19 hoặc chỗ lệch được giải thích.
6. K1–K7 đạt; fixture F1–F11 đạt; chỗ không đạt có nguyên nhân.
7. C6 có nghĩa của `Node` kèm bằng chứng, hoặc "chưa phân xử" kèm phần thiếu.
8. C7–C8 trả lời ba câu cho mức thao tác: dựng được không; có phân biệt mà mức dịch vụ không có không; còn thiếu gì. Không kết luận về lợi ích chẩn đoán.
9. C9: bảng đầy đủ mọi quan hệ của mô hình; mỗi yêu cầu còn thiếu có lý do và quan hệ nó phục vụ.
10. Bộ dựng không nhận đầu vào suy từ nhãn, kiểm bằng chữ ký hàm và test.

**Được rút ra:** đồ thị từ trace gồm gì, thiếu gì; T-036 và P9a cần bổ sung gì. **Không được rút ra:** đồ thị hay mức thao tác giúp RCA; một ứng viên P6 được chọn; P5 đã xong.

## Đường đi của nhãn

- **Bộ dựng nhận:** bảng span (định dạng mở rộng), khoảng thời gian nửa mở, bảng alias, universe.
- **Bộ dựng không nhận:** tên ca, đường dẫn, file nhãn, mốc tiêm, root, loại lỗi.
- **Alias và universe** chốt từ metadata (WHY-26, WHY-37). Chọn file qua mã ẩn danh của `src/p3/selector.py`.
- **Cửa sổ N, A** được tính từ mốc tiêm ở phía gọi bộ dựng. Đây là thông tin hợp lệ của chế độ (a) (WHY-24); đồ thị N, A không dùng cho chế độ (b).
- **Ảnh chụp** dùng lưới cố định. Ở RE2-TT, lưới 60 giây neo đầu file có một biên trùng mốc tiêm (thẻ T-002 mục 5). Task chỉ ghi nhận; cách xử lý thuộc P6.
- **Nezha-OB:** việc file trace tồn tại đã suy từ nhãn (thẻ T-008 mục 8), nên không dựng ảnh chụp. Khảo sát cột `Node` chỉ qua adapter trong cửa sổ dev.
- **Nhãn** chỉ ở script báo cáo, chạy sau khi đồ thị đã ghi ra file.

## Không làm

- Không chọn thành phần, tín hiệu, cửa sổ, cơ chế hay mức (thao tác hay dịch vụ) cho P6. Không tính điểm, thời gian tự xử lý, ngưỡng, thứ hạng.
- Không mở test; không đọc `data/locked/`, ô test Nezha-OB, Weight và chuỗi số của file mức ngày.
- Không sửa baseline, `src/p3/`, kết quả task cũ, gói G2, B16, repo FlashTicket.
- Không dựng nguồn tĩnh: T-036.
- Không ban hành yêu cầu P9a, không đề xuất sửa hệ thống trong task; chỉ trình danh sách cho Minh duyệt.
- Không định nghĩa nhãn lan. Không dựng đồ thị mức metric kiểu CIRCA (UV-8). Không suy quan hệ dịch vụ–cơ sở dữ liệu từ tên (SL34).

## Chi phí ước lượng

| Hạng mục | Số | Trạng thái |
|---|---|---|
| Đọc dữ liệu, RAM của bộ dựng và bộ đọc Node | Đo trên pilot hai ca trước lượt đầy đủ | Chưa đo cho bộ dựng |
| Hai mức, mọi cửa sổ, 52 ca | dưới 1 giờ | Chưa đo |
| Đầu ra | dưới 300 MB | Chưa đo |
| Tải dữ liệu | 0 | — |

Không tải dữ liệu hoặc dùng EC2. Các ước lượng trên chưa được đo; lượt thực hiện bắt đầu bằng pilot hai ca, ghi thời gian và RAM. Nếu dự kiến một lượt vượt 1 giờ thì dừng, trình Minh theo luật cứng 8. Không dùng các số chi phí lịch sử chưa có manifest phủ làm bằng chứng xác nhận ngân sách.

**Ít chờ hơn, chờ Minh duyệt:**
- Bước 1 và bước 2 song song.
- Dựng hai mức trong cùng một lượt đọc.
- Dùng lại bộ đọc của `src/p3`.
- Hai tiến trình song song, giới hạn bởi RAM trống.
- Soạn SPEC T-036 ngay khi có đặc tả v1, không chờ T-035 đóng.

## Rủi ro và điều chưa chắc

- **Chưa kiểm:** cạnh cha–con khác thực thể là lời gọi phía gọi → phía được gọi (RE2-TT không công bố công cụ ghi span).
- **Chưa kiểm:** nghĩa của `Node`, `dependency.csv`, `source_50`, `destination_50`; chúng có thể suy từ chính trace, khi đó K6 không là đối chiếu độc lập.
- **Chưa kiểm:** tên thao tác RE2-TT ổn định. K2 O.2 câu 5 và 7 nêu khả năng tên chứa ID hoặc URL. T-002 đếm 152 thao tác ở một ca (`cases.json`, `n_operations`).
- **Đồ thị gần hằng:** 3 hình dạng trên 30 ca. Root không có cạnh: `ts-auth-service` có bậc (0, 0) ở 30/30 ca.
- **Đoạn trước mốc chưa được xác nhận là khỏe (G2-H24):** gọi là "đồ thị tham chiếu trước mốc".
- **Thao tác chỉ có sau mốc (G2-H16):** ghi thành nhóm riêng, không bỏ.
- **Fixture do ta viết:** chỉ kiểm bộ dựng theo đặc tả của ta. Instrumentation thật của FlashTicket có thể khác; phải kiểm lại khi có trace thật (P9b).

## Prompt bàn giao

Prompt soát SPEC đã ghi nằm cuối LOG Phiên 1. Sau mỗi lượt tiếp theo, chép nguyên văn Prompt chung, khối công đoạn và khối cổng từ `docs/review-prompt.md`; chỉ điền thông tin trung tính. Người làm ghi prompt trong mục LOG mới. Không tự gửi.

## Phụ lục — WHY-52 đã duyệt cùng SPEC

## WHY-52. Đồ thị phụ thuộc ở P5: mô hình chung hai mức, đầu vào của bộ dựng và cách tách task — Đã duyệt nội dung (14/10/2026, Q-150; SPEC T-035)

- **Chọn:**
  1. **Một mô hình chung phủ nhu cầu FlashTicket.** Nút: dịch vụ, gateway, cơ sở dữ liệu, cache, broker, nhà cung cấp danh tính, đối tác ngoài, máy. Cạnh: gọi, thông điệp, dữ liệu, triển khai. Thêm kiểu "gọi chưa phân kiểu" khi trace không có loại span. Phần dataset công khai thiếu được ghi là thiếu, không bỏ khỏi mô hình.
  2. **Mỗi nút, mỗi cạnh ghi nguồn bằng chứng:** trace, nguồn khác của dataset, tĩnh, suy ra.
  3. **Hai mức.** Mức thực thể là mức chính. Mức thao tác là lớp tùy chọn; mỗi thao tác thuộc về một thực thể; đặc tả v0 định nghĩa phép chiếu, cách giữ quan hệ nội bộ và thành phần không có thao tác quan sát được. Đây là phương án phải khảo sát ngay trên mọi ca dev, chưa chọn làm phương pháp P6.
  4. **Thông điệp đi qua nút broker** (phát → broker → nhận). Cạnh logic gửi → nhận chỉ suy ra khi có bằng chứng nối một bản tin cụ thể (ngữ cảnh tạo/link có nghĩa đã xác minh hoặc định danh bản tin trong phạm vi phù hợp). Cùng correlationId giao dịch không đủ.
  5. **Bộ dựng nhận** bảng span mở rộng, một khoảng thời gian, alias, universe; không nhận mốc tiêm, tên ca, đường dẫn, nhãn.
  6. **P5 xuất cấu trúc, độ phủ, địa chỉ tín hiệu;** không xuất tín hiệu hay điểm.
  7. **Tách P5** thành T-035 (từ trace) và T-036 (kiến trúc, so hai nguồn). P9a nhận danh sách thông tin cần theo từng quan hệ.
- **Vì sao:**
  - (1), (2): DT18 nêu ba loại cạnh và nút gồm thành phần hệ thống. FlashTicket có cơ sở dữ liệu, cache, broker, Saga, callback (MRP §1; B16 §1, §3, §5). Trace RE2-TT không có cột loại span (`results/T-002/local-inspection/run-002/cases.json`, `typed_span_kind_column`). Trace Nezha-OB chỉ có tám cột, không có loại span (`results/T-008/runs/file-audit-001/summary.json`). Bỏ khỏi mô hình mọi thứ dataset công khai thiếu thì mô hình không còn phủ đề tài. Gọi mọi cạnh cha–con là "đồng bộ" thì khẳng định điều dữ liệu không ghi. Căn cứ: đáp ứng DT18 và nhu cầu kỹ thuật, không phải sửa hạn chế P4.
  - (3): Minh giữ phương án dựng thao tác thành nút (14/10/2026). Các ứng viên G2 mục 5 cần thông tin mức lời gọi và cây lời gọi. Lớp thao tác giữ thêm phân biệt về tên và quan hệ thao tác so với gộp theo thực thể; không thay thế cây span và thời gian của từng lần thực thi. Bảng C5 chỉ rõ ứng viên nào còn cần dữ liệu span gốc. Lợi ích của mức thao tác chỉ kiểm ở P6.
  - (4): B16 §3 cho phép consumer dùng link thay quan hệ cha–con; bên gửi, bên nhận xử lý ở hai thời điểm. Nút broker giữ được hàng đợi làm nơi gắn metric (B16 §5: queue ready/unacked).
  - (5): luật cứng 6; cùng một mã cho hai chế độ và cho FlashTicket (WHY-08).
  - (6): MRP đặt việc chọn tín hiệu ở spec P6.
  - (7): nguồn tĩnh phụ thuộc lược đồ của T-035; gộp lại thì không vừa một phiên.
- **Phương án đã xét:**
  - Gán "đồng bộ" cho mọi cạnh cha–con: sai khi có gọi bất đồng bộ.
  - Suy kiểu từ tên bằng biểu thức chính quy: lặp SL34.
  - Chỉ mức dịch vụ: mất phương án Minh muốn giữ.
  - Chỉ mức thao tác: lệch định nghĩa nút của DT18 và tập ứng viên của baseline (WHY-26).
  - Cạnh gửi–nhận trực tiếp có thể dựng khi nối được bằng chứng, đồng thời giữ thông tin broker và hàng đợi riêng. Mô hình hiện tại chọn broker làm nút để biểu diễn rõ tài nguyên dùng chung và nơi gắn số đo hàng đợi.
  - Bộ dựng nhận mốc tiêm: đưa nhãn vào mã dùng chung.
  - P5 tính luôn tín hiệu: chọn trước P6.
- **Khảo sát Node:** bộ đọc bổ sung đặt trong `src/do_thi/`, lọc dev trước khi xuất trường, giữ kiểm nguồn và không sửa `src/p3`. Chỉ xác nhận nghĩa host khi tài liệu hoặc mã thu chứng minh nguồn định danh; ánh xạ ổn định/nhóm `Node*` không đủ. Thiếu thì OPEN.
- **Bằng chứng và giới hạn:** G2 mục 5, 6.2; thẻ T-002, T-008; B16 §3–§7. Chưa kiểm: nghĩa phía gọi/phía được gọi ở RE2-TT; tên thao tác ổn định; nghĩa cột `Node` của Nezha-OB. Fixture chỉ kiểm bộ dựng theo đặc tả của ta, không thay trace FlashTicket thật. Trace FlashTicket chưa được cung cấp hoặc chưa kiểm trong phạm vi task; không suy ra toàn hệ thống chưa có trace.
- **Kết luận phụ thuộc:** thống kê đồ thị P5; định nghĩa "lời gọi" và mức đồ thị P6 dùng; phạm vi T-036; danh sách yêu cầu cho P9a. Không là căn cứ cho lợi ích của đồ thị hay của mức thao tác.
