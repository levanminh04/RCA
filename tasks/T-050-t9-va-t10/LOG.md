# Nhật ký T-050

Người làm ghi nối tiếp. Lịch sử đề xuất, duyệt và triển khai tách theo từng phiên.

## Phiên 1 — 04/11/2026 — Codex — laptop Windows — người làm

**Mở phiên** Đọc AGENTS, STATE, mẫu SPEC/LOG và prompt hiện hành. T-049 đang chờ nghiệm thu và chốt nền. Kiểm `results/T-049/scripts/dong_ho_so.py` ở chế độ chỉ đọc đạt, gồm 1020 đầu ra, 13 nguồn và 5 manifest upstream.

**Công đoạn** Ghi bản SPEC đề xuất T-050 sau lượt Claude kiểm lại bản đáp P1–P4. Mục tiêu T9/T10 lấy từ T-043, MRP và kế hoạch sau T-047. Claude giữ vai trò phản biện.

**Quyết định của Minh trong phiên**

- Nguyên lời: “nếu không có mâu thuẫn nào với claude hoặc phản đối nào thì cho phép ghi luôn , nếu có mâu thuẫn thì soạn trình claude phản biện”.
- Claude xác nhận hết bất đồng về bản đáp. Áp quyền ghi vào SPEC đề xuất và LOG đã trình. P1, nghiệm thu T-049, nền và quyền triển khai còn chờ lựa chọn rõ của Minh. Câu chữ quyết định chính thức để ghi DECISIONS/WHY chờ bước đó.

**Đối chiếu theo điểm**

| Điểm | Kết luận và bằng chứng | Phần ghi trong SPEC |
|---|---|---|
| P1 | Đúng về nhu cầu Minh chốt. MRP §2.3, P6 tầng 4 và WHY-02 cho phép đánh giá ứng viên theo dev. E6a dùng thứ hạng tầng từ F_I của E5, trong khi chính bước sắp xếp dùng khóa cục bộ. T-043 Phụ lục C bước 6 có ngoại lệ chức năng. | Ghi P1 OPEN. Khuyến nghị giữ E6a+S1 khi KHÔNG TÁC DỤNG. Nêu cách xử lý nếu Minh yêu cầu bước xếp trực tiếp dùng cạnh. |
| S0 | Claude xác nhận phản ví dụ đúng và rút nhận xét S0 tương đương bỏ cạnh. Với hai nút cùng K_I=(1,1,1), nút B có thêm kênh kế thừa điểm 2, π không cạnh của hai nút cùng 1/2. E6a+S0 hòa, E6b dùng K_raw đưa B lên trước. | Giữ phép so báo kèm S0. Diễn giải riêng khóa phá hòa và phần tác dụng cạnh. |
| P2 | Đúng sau đính chính. Số tập trung của v mô tả một điều kiện đầu vào. Chưa xác định tác dụng của cạnh trên thứ hạng. | Lưu v, π, cạnh có tác dụng, khóa và vết theo ca. Giới hạn diễn giải theo thang z đang dùng. |
| P3 | Đúng. Cùng EC2 cho pilot native và replay cô lập sai khác đường tái sử dụng. Nếu chuyển lượt chính sang laptop cần đối chiếu cùng khung giữa hai máy. Tính phần dư bằng một bước cập nhật thêm kiểm kết quả, không đo sai số dừng nội bộ. | Chọn phương án ít công đã được Claude nêu là mặc định cùng EC2, giữ phương án laptop có điều kiện. |
| P4 | Đúng về adapter và dự toán. T-043 dòng 922 yêu cầu nhận diện suy biến, còn tiêu chí cụ thể của C-g cần Minh duyệt cùng SPEC. | Ghim nguồn P3, thêm 20–40 phút cho adapter. Đề xuất tiêu chí trước ghép nhãn dựa trên chạy với khối lượng dương và thay đổi thứ tự/nhóm hòa. |

**Kiểm chỉ đọc trong phiên**

- Kiểm manifest T-049 và hash từng entry `K-thang-C` trong `runs/t6-001-seal.json`. Dòng native khớp `source_config` và mã ca. Với 52 ca thật/30 mốc giả, ở P nhóm nút tầng 1 hòa theo `extra.K_I_P` xuất hiện ở 21 ca thật. Có 3 ca thật và 2 mốc giả trong đó `extra.K_raw_P` có thể tách hòa. Phép đếm nhóm theo `extra.tang_P == 1`, dùng khóa ghi ra. Đây là phép kiểm trên nguồn đã lưu, không chạy E6b.
- Từ `extra.K_I_P/*/0` dương, tính `max(s)/sum(s)` và tỷ lệ điểm lớn nhất/nhì nếu có hai nút. Trung vị 0,9233176313, 27/45 ca có tỷ lệ >10 và 7 ca một nút dương. Kiểm `extra.kenh_co_the_gioi` theo `F_I == 1` và `s > 0` cho 0/246 khung thiếu khối lượng dương.
- Kiểm `results/T-043/ks16/dem-sau-ghep-nhan.json#/o_kich_hoat/E6b` theo manifest T-043, có 21 ô. Kiểm `results/T-049/runs/kb-001-cham/kq.json#/cau_hinh/K-thang-C/ca/*/theo_the_gioi/P/RR/phan_so` theo manifest T-049, có 43/52 ca RR=1.
- Lượt đáp trước đã kiểm hash và mốc của 90 bản ghi RE2 và 66 bản ghi Nezha, 52 nguồn SimpleRCA có khóa phiếu nguyên không âm. Danh sách nguồn và hợp đồng ghép trong SPEC. Thời gian dự toán dùng các phép đọc nguồn của lượt đề xuất và chi phí adapter được hai bên đánh giá lại, đang chờ đo pilot.

**Kết thúc phiên**

1. Ghi bản SPEC và LOG, tiếp thu bản kiểm lại của Claude. Đề nghị dừng phản biện bản đề xuất do hai bên đã xử lý các phản đối về tính đúng và cách diễn giải. Nếu Minh muốn soát SPEC thành văn, dùng prompt ở cuối mục này.
2. Phạm vi ghi lượt này là `tasks/T-050-t9-va-t10/SPEC.md` và `LOG.md`. STATE cập nhật khi mở task theo duyệt triển khai. Mốc STATE hiện tại thuộc nguồn đang băm trong manifest T-049. Giữ snapshot nguồn quản trị trước khi chốt và cập nhật ở lượt được duyệt.
3. Kiểm nguồn và số liệu chỉ đọc đạt. E6b/E7 theo đường phát lại còn chờ đối chiếu pilot. C-g còn chờ duyệt định nghĩa suy biến và thực hiện adapter.
4. Chờ Minh nghiệm thu T-049, xác nhận nền C/E3b tắt, chọn hành động P1 và duyệt SPEC/quyền chạy. Các vấn đề hiệu quả độc lập, hiệu chuẩn verdict, vùng ảnh hưởng có nhãn, VC×E5, chế độ (b), RE3-OB và FlashTicket tiếp tục OPEN.
5. Bước tiếp nhận là đọc SPEC và chốt các điểm ở mục 4. Sau duyệt, ghi lý do vào WHY và quyết định vào DECISIONS theo câu chữ được duyệt, giữ snapshot nguồn lịch sử, rồi kiểm hash các entry nền và tạo công cụ chiếu cho pilot. Lệnh kiểm nguồn hiện tại: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-049/scripts/dong_ho_so.py`.

**Đề xuất commit khi Minh yêu cầu** Bản SPEC đề xuất T-050 cho T9/T10 và LOG bàn giao.

## Bản kiểm lại của Claude do Minh chuyển

> # Kiểm lại bản đáp T-050 — Claude, chỉ trả lời trong chat
>
> ## Kết luận
>
> Tôi không còn bất đồng nào với Codex. Bản đáp đúng ở cả bốn điểm. Phản ví dụ về vế S0 là đúng, và nhận xét trước của tôi sai. **P1 vẫn chặn việc duyệt SPEC**, nhưng chỉ vì Minh chưa chọn phương án. Lập luận của Codex ở P1 không có lỗi.
>
> ## Từng điểm
>
> **P1 — Cách hiểu của Codex đúng. Vẫn CHẶN duyệt SPEC cho tới khi Minh chọn.**
> - Tôi không tìm thấy câu nguồn nào bắt bước sắp thứ tự phải đọc cạnh trực tiếp.
>   - WHY-02 (Q-36) viết "khoanh vùng và xếp hạng cũng chạy trên đồ thị". Cùng mục đó ghi "DT18 yêu cầu các đầu ra, không bắt buộc kiến trúc bốn tầng" và "thành phần cụ thể chọn sau P4".
>   - MRP P6 tầng 4 coi PageRank là một ứng viên, chọn trên dev theo MRR.
> - E6a+S1 vẫn dùng đồ thị khi xếp hạng, qua tầng của E5. Thực thể tầng 1 luôn đứng trước tầng 2, và tầng được tính từ F_I mà E5 suy ra trên cạnh ([xep_hang.py:121](src/m1/xep_hang.py:121)). Vì vậy chọn E6a+S1 khi KHÔNG TÁC DỤNG không đổi mục tiêu của WHY-02, miễn hồ sơ nói rõ bước sắp thứ tự không lan truyền điểm.
> - Lựa chọn này là cách hiểu Q-36, nên quyền chọn thuộc Minh. Cần ghi vào WHY trước pha 1 (luật 3).
> - Phạm vi kết luận cần ghi kèm, nối với P2: nếu KHÔNG TÁC DỤNG thì kết luận là "dưới thang z+S1, E6b chưa đủ lợi ích theo ngưỡng". Không được viết là PageRank vô ích.
>
> **Vế S0 — Phản ví dụ của Codex đúng. Tôi rút lại nhận xét trước.**
> - Theo code, khóa tầng 1 của E6a (`k_tang`) chỉ gồm K_I, còn khóa E6b là (π, K_I, K_raw).
> - Trên dev, chuyện này xảy ra thật. Ở thế giới P, 21/52 ca thật có thực thể tầng 1 hòa K_I. Trong đó 3/52 ca thật và 2/30 mốc giả bị K_raw tách hòa, ví dụ dev-ba831dbeb8 (mốc giả, ba thực thể).
> - Vì vậy S0 → E6b không phải phép bỏ cạnh thuần túy. Tôi đồng ý với cách gọi Codex đề xuất: "so với xếp theo điểm cục bộ không dùng S1".
> - Để quy phần thay đổi cho cạnh, đọc khóa E6b khi thay π bằng v là đúng: khi không có cạnh, π hội tụ về v.
>
> **P2 — Số của Codex đúng. Mô tả của tôi trước đó không chính xác.**
> - Câu đúng là: 27/45 ca có từ hai nút dương có tỷ lệ lớn nhất/nhì lớn hơn 10, cộng 7 ca chỉ có một nút dương. Tôi đã gộp hai nhóm này thành "34/52 ca có tỷ lệ > 10".
> - q25 = 0,719 của tôi tính theo hạng gần nhất. Nếu đưa vào SPEC thì dùng nội suy tuyến tính (0,713) và ghi rõ quy ước.
> - Tôi đồng ý thu hẹp kết luận như Codex: v tập trung chưa chứng minh cạnh không có tác dụng.
>
> **P3 — Cách tách hai phép đối chiếu là đúng và gọn.**
> - `xep_hang.py` chỉ dùng `math` và `fractions`. Hàm `pagerank` chỉ có phép cộng, nhân, chia và `math.fsum`, không có numpy hay hàm toán học của thư viện hệ thống. Vì vậy với cùng khung đầu vào, phát lại trên hai máy dự kiến cho kết quả trùng từng bit. Phép đối chiếu số 2 của Codex rẻ; nếu nó lệch thì đó là dấu hiệu lỗi.
> - Phương án ít công nhất với cùng bằng chứng: chạy cả pilot native, pilot phát lại và lượt phát lại chính trên EC2. Khi đó bỏ được phép đối chiếu số 2.
> - Phương án laptop kèm phép đối chiếu số 2 cũng hợp lệ. Không có bất đồng ở đây.
>
> **P4 — Thêm 20–40 phút là hợp lý.**
> - Còn thiếu một việc phải khai trước: T-043 dòng 922 chỉ ghi "Suy biến: bỏ, ghi lý do", không định nghĩa thế nào là suy biến.
> - Tiền lệ C-d3 ở T-045 có dùng "MRR 0 ở mọi cấu hình", tức là một tiêu chí cần nhãn.
> - Với C-g, SPEC nên khai tiêu chí không dùng nhãn, chốt trước pha 2. Ví dụ: tỷ lệ ca có trạng thái `NO_EVIDENCE` hoặc `tong_s_g_bang_0`, hoặc thứ tự C-g trùng thứ tự SimpleRCA ở mọi ca. Codex chọn tiêu chí và trình Minh duyệt cùng SPEC.
>
> ## Báo cuối lượt
>
> 1. **Đã làm:** đối chiếu bản đáp với code `xep_hang.py`, WHY-02, MRP P6, T-043 dòng 922 và các khung nền đã lưu.
> 2. **File thay đổi:** không sửa file nào.
> 3. **Kiểm đã chạy:** một lệnh Python chỉ đọc trên 82 khung K-thang-C (qua seal T6), đếm hòa K_I ở tầng 1 và các trường hợp K_raw tách hòa. Kết quả: 21/52 ca thật có hòa, 3/52 ca thật và 2/30 mốc giả bị tách. Ba thế giới cho cùng số.
> 4. **Cần Minh quyết:**
>    - P1: khi T9 ra KHÔNG TÁC DỤNG thì giữ E6a+S1 hay giữ E6b.
>    - Quyền ghi SPEC T-050 kèm các chỉnh P2–P4 và tiêu chí suy biến của C-g.
>    - Nghiệm thu T-049 và nền T-050.
>    - Phần còn OPEN như cũ: VC×E5 2×2, verdict, chế độ (b), RE3-OB, FlashTicket.
>
> **Đề xuất: dừng phản biện bản đề xuất.** Không còn phản đối nào chưa xử lý về tính đúng. Bước tiếp theo là Minh chọn P1 rồi cấp quyền ghi SPEC. Sau khi SPEC được ghi, Minh có thể chuyển một lượt soát SPEC nếu muốn. Dừng phản biện không có nghĩa là SPEC đã được duyệt.

## Prompt bàn giao Claude soát SPEC

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-050, tasks/T-050-t9-va-t10/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/KE-HOACH-SAU-T047.md, SPEC T-043, SPEC/LOG T-049 và git diff hiện hành.
- Phản biện và phản hồi trước: đề xuất và các lượt trao đổi trong chat, bản kiểm lại của Claude và đối chiếu của Codex tại tasks/T-050-t9-va-t10/LOG.md.
- Code và kết quả liên quan: src/m1/, src/m1_danh_gia/, results/T-049/manifest.json, results/T-049/runs/t6-001-seal.json, đầu ra T-043/T-044/T-053 và danh sách bản ghi P3 T-024/T-026 theo SPEC.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 2 — 04/11/2026 — Codex — laptop Windows — người làm

**Mở phiên** Đọc lại SPEC, trạng thái, bản kiểm lại của Claude và nguồn quyết định. Kiểm hồ sơ T-049 trước khi cập nhật quản trị đạt 1020 đầu ra, 13 nguồn, 5 manifest upstream.

**Q-239/Q-240 — ghi quyết định** Minh: “tôi tưởng tôi đã bảo bạn nêu hết đề xuất của bạn về các phần đang chờ tôi duyệt mà sao p1 vẫn chờ tôi chọn ? tóm lại là còn cái gì chờ toi nữa ? nếu bạn đã đề xuất rồi và cả claude cũng đồng ý thì duyệt ghi”. Áp lời duyệt vào các đề xuất đã thống nhất. Nghiệm thu T-049 trong phạm vi dev, chốt C/E3b tắt cho nền T-050, chốt P1 giữ E6a+S1 nếu kết cục T9 là KHÔNG TÁC DỤNG. Lượt trước để P1 OPEN vì đọc quyền chỉ là ghi bản nháp. Lời Minh ở lượt này xác nhận duyệt các phần đã đề xuất và có đồng thuận, nên trạng thái OPEN của P1 được đóng.

- Nguồn quyết định ở `docs/DECISIONS.md` Q-239/Q-240 và lý do ở `docs/WHY.md` WHY-73/WHY-74. Cập nhật SPEC và hai dòng liên quan trong STATE, nối LOG nghiệm thu T-049. Bản trước chốt và bản byte nguồn quản trị được lưu ở `results/T-050/ban-giao-T049/`.
- Giữ cách đọc S0 theo phản ví dụ phá hòa, phát lại trên trung gian đã kiểm và phương án mặc định dùng EC2. Tiêu chí C-g trong SPEC dùng đầu ra trước nhãn. Thời lượng dự toán đã gồm adapter P3.
- Đề nghị dừng phản biện bản đề xuất theo bản kiểm lại của Claude. Prompt kiểm SPEC hiện hành ở cuối mục này để Minh chọn chuyển. Ghi nhận T-049 trong phạm vi dev và P1 là hành động có điều kiện trước pha 1.
- **Còn chờ Minh** quyền chạy T-050 với trần đã trình là 6 giờ thời gian thực, tổng 2 giờ EC2, tối đa 90 phút cho một lượt dài khi phải dùng đường tính lại. Lời duyệt ghi hồ sơ không được dùng làm lệnh chạy dài theo AGENTS mục 3.8. T-050 chưa chạy phương pháp.
- **Bước tiếp nhận** Sau quyền chạy, ghi mốc duyệt triển khai vào LOG, kiểm nguồn bằng `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-050/ban-giao-T049/kiem-nguon.py`, rồi chuẩn bị gói đầu vào và pilot đúng SPEC. Các vấn đề khoa học sau dev vẫn OPEN theo WHY-73.

**Đề xuất commit khi Minh yêu cầu** Ghi nghiệm thu T-049 và chốt nền, P1, SPEC T-050 trước chạy.

## Prompt bàn giao Claude soát SPEC hiện hành

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-050, tasks/T-050-t9-va-t10/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/KE-HOACH-SAU-T047.md, SPEC T-043, SPEC/LOG T-049 và git diff hiện hành.
- Phản biện và phản hồi trước: đề xuất và các lượt trao đổi được ghi tại tasks/T-050-t9-va-t10/LOG.md.
- Code và kết quả liên quan: src/m1/, src/m1_danh_gia/, results/T-049/manifest.json, results/T-050/ban-giao-T049/manifest.json và các đầu ra được trỏ trong SPEC.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 3 — 04/11/2026 — Codex — laptop Windows — người làm

- Minh duyệt triển khai và chạy T-050 theo SPEC. Trần 6 giờ thực, 2 giờ EC2 tổng cộng, 90 phút cho một lượt tính lại. Minh yêu cầu pilot kiểm tiếp nhận lại trước lượt chính. Claude giữ vai trò phản biện.
- Kiểm nguồn lịch sử PASS (1020 đầu ra, 13 nguồn, 5 manifest upstream). Đọc được hostname từ SSH ghim của T-049. Chưa khởi động lượt EC2.
- Chiếu thử dau-vao-001 dừng ở cửa sổ 0, sau khi khóa/hòa P khớp, vì adapter vùng thiếu hai trường hợp vùng trong bản ghi native. Đã bổ sung hai trường hợp vùng từ đúng vùng trả về của E7 và kiểm lại bằng dau-vao-002.
- dau-vao-002 và dau-vao-003 tái tạo S1 246/246, gồm khóa, hòa, tầng, N1/V0 và hai cách vùng ở P. Bản 003 ghim thêm status native để pilot kiểm bất biến. Log lần 003 ở results/T-050/chieu-003.log.
- Fixture đầu chọn quá rộng do tên file trùng cụm -k và môi trường thiếu đường thư viện đã ghim. Dùng PYTHONPATH theo manifest, chọn đúng hàm fixture E6b/E7, đạt 11/11 tại results/T-050/fixture-002.log.
- Adapter C-c/C-g lần 001 dừng vì bản ghi P3 dùng entity_ranking với blocks=null. Dùng khoi_tu_ban_ghi chính thức của P3, chạy lại lần 002, xác minh 52 bộ nguồn theo hash, khóa phiếu, cửa sổ và tie_group. Phiếu 002 lưu riêng trước nhãn.
- Xác minh EC2 bằng instance-id và môi trường Python đã ghim. Pilot trên dấu vết EC2 các chỉ số 1, 58, 62, 79. Có ba tầng bao phủ (RE2 thật, RE2 giả, Nezha thật) vì dấu vết EC2 đã seal không có Nezha giả. Chọn biên độ nặng khác nhau bằng dung lượng nguồn, dùng độ tập trung điểm/số cạnh làm tiêu chí phụ. Không dùng nhãn/điểm T9.
- Lượt ec2-001 tách phiên SSH, PID 29129, thư mục /home/ubuntu/rca-t049/results/T-050/ec2-stage-001/results/T-050/ec2-001. Timeout tuyệt đối từ lúc launch, còn biên cho chuyển tệp trong trần EC2. Controller kiểm lại bốn cửa sổ từ đĩa bằng tiến trình mới rồi chỉ tính 78 cửa sổ còn thiếu. Không dùng laptop thay lượt phát lại chính.
- `results/T-050/pha1-001/seal.json` (d910e2608ebdd4f3f51f5c2089497e9b3b516cd49b5b705802f688fb3eaff802)
- Pilot native và replay khớp 4 cửa sổ × 3 thế giới. Tiến trình mới kiểm và dùng lại 4 cửa sổ. Controller hoàn thành 82/82; đã nhận, kiểm hash và khóa pha 1 trước khi chấm dev.

### Kết thúc triển khai

1. Đã chạy T9/T10 và C-c/C-g trên dev, khóa pha 1 trước ghép nhãn. T9 theo luật C trả HẠI tại cả ba thế giới. Đề xuất T-051 giữ E6a+S1 và tắt E6b theo nhánh HẠI của SPEC. Cờ đánh đổi E2 vẫn đi kèm. Đây là đề xuất chờ phản biện và nghiệm thu.
2. Ghi trong results/T-050, nối LOG và cập nhật dòng T-050 của STATE. Báo cáo, manifest, bản ghi, script và các lượt thử đều ở results/T-050. Không có file phương pháp dùng chung thay đổi trong lượt này.
3. Kiểm 246 khung S1, 12 khung native/phát lại, tiếp nhận lại bốn đầu ra pilot, 82 biên nhận EC2, 11 fixture, 156 bản ghi nguồn đối chứng, 572 RR, 1000 mẫu bootstrap và 52 ca vùng. Kiểm nguồn đối chứng theo giao thức, mapping, nguồn nhãn sau seal. Kiểm cú pháp, liên kết và số MRR trong báo cáo. Lệnh kiểm báo cáo đầu qua các assert nhưng lỗi mã hóa stdout ở dòng in cuối. Kiểm lại với PYTHONIOENCODING=utf-8.
4. Ba ca giảm cùng một ô RE2-TT. Khi thay π bằng v, giữ phần phá hòa, RR quay về bằng S1. Có ca đúng đối chiếu cùng root và cấu trúc chuyển nhưng v tập trung hơn. Còn OPEN hiệu quả độc lập RQ3b, nhãn vùng RQ3c và tác dụng quan hệ của cả chuỗi RQ3d. RSS đỉnh pilot chưa được ghi. G3 và test vẫn khóa. Minh quyết nghiệm thu và dùng nền T-051 sau phản biện.

Bước tiếp nhận nếu đổi tài khoản. Đọc AGENTS, STATE, SPEC và mục LOG này. EC2 đã xong, 82 biên nhận lưu trong results/T-050/ec2-001-download/ec2-001. Chấm ở cham-001, kiểm ở kiem-cuoi-001.json và kiem-nguon-doi-chung-001.json. Không chạy lại EC2 để bàn giao phản biện. Nếu cần kiểm trạng thái, dùng Python ghim với -B gọi results/T-050/remote.py status. Để tái lập phần kiểm rẻ, dùng audit.py và audit_sources.py trong thư mục T-050 với kết quả đầu ra ở lượt mới được phép, vì tên đầu ra hiện hữu được giữ.

Lệnh cuối ở bước hồ sơ. Python ghim -B results/T-050/manifest_task.py, sau đó kiểm cú pháp, đường dẫn và MRR của bao-cao.md bằng Python chỉ đọc. Xác nhận file bằng manifest sau khi cập nhật LOG/STATE.

Đề xuất ghi vào DECISIONS khi Minh duyệt. Ngày 04/11/2026, Minh duyệt triển khai T-050 theo SPEC với trần 6 giờ thực, 2 giờ EC2 và 90 phút cho một lượt tính lại. Giữ quyền nghiệm thu, mở G3, commit và push riêng. Kết quả và đề xuất nền T-051 đợi phản biện và quyết định riêng.

Đề xuất nội dung commit khi Minh yêu cầu. Ghi kết quả dev T9/T10, đối chứng C-c/C-g, đường phát lại có tiếp nhận và hồ sơ T-050. Xác định tập tệp riêng trước commit.

## Prompt bàn giao Claude soát kết quả

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-050, tasks/T-050-t9-va-t10/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/KE-HOACH-SAU-T047.md, SPEC T-043, SPEC/LOG T-049, SPEC/LOG T-050 và git diff hiện hành.
- Phản biện và phản hồi trước: các lượt soát SPEC và phản hồi theo thứ tự trong tasks/T-050-t9-va-t10/LOG.md.
- Code và kết quả liên quan: results/T-050/manifest.json, results/T-050/bao-cao.md, results/T-050/pha1-001/seal.json, results/T-050/cham-001/, src/m1/, src/m1_danh_gia/ và lệnh ở LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 4 — 04/11/2026 — Codex — laptop Windows và EC2 — người làm

- Minh yêu cầu chạy lại T-050 trong phiên này để phân xử nghi vấn về việc dùng trung gian từ T-049. Giữ luật, cấu hình và dữ liệu dev theo SPEC. Chạy một lượt mới riêng và tính đủ hai vế từ dữ liệu gốc cho ba cửa sổ làm đổi kết cục, như phép kiểm hồi cứu.
- Hồ sơ nguồn T-049 đạt PASS 1020 đầu ra, 13 nguồn và 5 manifest thượng nguồn. Khởi chạy lại EC2 tách thư mục ec2-002, PID 29751, timeout 20 phút. Chiếu mới vào dau-vao-004 và tính lại đối chứng.
- `results/T-050/pha1-002/seal.json` (f93bd36d3da46909be1a14f920acb082d42e18b983ead07f0d47b9e5efaff7e2)

- Đủ 82/82 bản ghi mới. Dữ liệu chiếu tái tạo khớp 82/82, đầu ra từng cửa sổ khớp hash lượt trước. C-c, C-g, 572 RR, luật C, 1.000 mẫu độ bền và T10 khớp. T9 vẫn HẠI ở cả ba thế giới. Thời gian tính cửa sổ pilot trên EC2 là 87.57 giây và 78 cửa sổ dùng trung gian là 2.82 giây. Fixture 11/11. Kiểm ở results/T-050/kiem-chay-lai-002.json.
- Lượt kiểm từ dữ liệu gốc đầu tiên trên laptop dừng ở cửa sổ 05 khi khóa T4c của S1 khác tới 5,55e-17 so với nguồn EC2. Năm khóa khác số trong mỗi thế giới. Nhóm hòa và thứ tự khớp. Vết lỗi và hai bản ghi tính mới được giữ trong kiem-lai-native-001. Giữ tiêu chí so chính xác. Kiểm lại 05 và 13 trên EC2, 21 trên laptop theo nơi tạo đầu vào T-049. Cả ba cửa sổ khớp chính xác đầu vào, thứ hạng, vùng, nhóm hòa và khóa, với 18 RR kiểm lại từ bản ghi native. Thời gian mỗi cửa sổ cho cả hai vế gồm 05 144.4 giây, 13 129.4 giây, 21 131.4 giây. Đây là kiểm hồi cứu các ca làm đổi kết cục. Nguồn results/T-050/kiem-native-quyet-dinh-002.json.
- Giữ đề xuất dev và giới hạn T10 thiếu nhãn vùng. Chờ Claude soát kết quả. Minh quyết nghiệm thu và nền T-051. G3/test khóa.
- Tệp mới ở results/T-050/manifest-chay-lai-002.json. Kiểm đủ 378 đầu ra lịch sử, giữ mọi lượt. Chỉ nối LOG và bổ sung liên kết dòng T-050 trong STATE.
- Tiếp nhận từ manifest của lượt mới và prompt ngay dưới. Lệnh chấm cuối dùng Python ghim với -B, PYTHONPATH theo manifest và OPENBLAS_NUM_THREADS=1, gọi results/T-050/score.py pha1-002 cham-002. Lệnh kiểm hai lượt gọi results/T-050/doi-chieu-chay-lai.py bằng môi trường đó. Script kiểm từ nguồn là results/T-050/kiem-lai-native.py, dùng kiem-lai-native-002 21 ở laptop và native-05 5, native-13 13 ở EC2. Dùng tên lượt mới nếu cần chạy lại.

## Prompt bàn giao Claude soát kết quả sau lượt chạy lại

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-050, tasks/T-050-t9-va-t10/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/KE-HOACH-SAU-T047.md, SPEC T-043, SPEC/LOG T-049, SPEC/LOG T-050 và git diff hiện hành.
- Phản biện và phản hồi trước: các lượt soát SPEC và phản hồi theo thứ tự trong tasks/T-050-t9-va-t10/LOG.md.
- Code và kết quả liên quan: results/T-050/manifest.json, results/T-050/manifest-chay-lai-002.json, results/T-050/bao-cao.md, results/T-050/pha1-001/seal.json, results/T-050/cham-001/, src/m1/, src/m1_danh_gia/ và lệnh ở LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 5 — 04/11/2026 — Codex — laptop Windows — người làm

### Đáp phản biện và ghi đính chính

Minh cho phép ghi bản đính chính và nối LOG nếu hai bên không còn bất đồng hoặc phản đối đối với phần ghi. Claude đã xác nhận bản đáp F1–F3. Điểm F1 còn chặn cách đọc rộng của báo cáo được xử lý bằng bản đính chính. Việc thử chiều đảo là đề xuất nghiên cứu riêng. Quyết định có thử trước T-051 vẫn OPEN.

| Điểm | Phản hồi của người làm | Xử lý |
|---|---|---|
| F1 | Hai bên thống nhất kết cục chỉ áp cho E6b đã thử và MicroRCA khác về chiều cạnh, trọng số, cá nhân hóa và tập nút. WHY-74 giải thích cách đáp ứng yêu cầu đồ thị. | Ghi phạm vi của T9 và câu hỏi hướng cạnh còn mở. |
| F2 | Đúng. Bước 3 xét ΔMRR gộp và δ. Ngưỡng theo dataset có mặt ở bước 2 và bước 5. | Ghi câu thay thế và giữ kết quả HẠI theo luật. |
| F3 | Hai bên thống nhất cơ chế ở ba ca loss. Cửa sổ 03 và 55 là ca đối chiếu giữ nguyên RR khi π giảm. Chênh C-g chỉ báo cáo. | Ghi vết ba ca và các đối chiếu, giới hạn quy kết chiều cạnh. |
| N1 | Đúng về trạng thái file. Phiên 4 đã có mục kết thúc, manifest và prompt. Bản đáp trước mô tả trạng thái cũ. | Dùng manifest hiện có và ghim riêng bản đính chính tại đây. |
| N2 | Đúng. §7.8 mục 8 đã dự báo khả năng nút nhận tích lũy khối lượng. Phép tính ví dụ cho π(R) = 5/6. | Nối kết quả với điều kiện thất bại đã khai, giữ độ sâu thực tế của nút nhận ở trạng thái chưa kiểm. |

1. Đã ghi đính chính F1–F3, N1–N2. Đề xuất giữ E6a+S1 và tắt E6b theo nhánh HẠI, với phạm vi là cặp đã thử.
2. Ghi results/T-050/dinh-chinh-va-kiem-lai.md và nối mục này vào LOG. Giữ byte của báo cáo và hai manifest lịch sử để đối chiếu.
3. Kiểm hash 378 đầu ra gốc và 294 đầu ra Phiên 4, hash đặc tả T-043, luật C ở ba thế giới, RR của các ca đối chiếu và đếm C-g. Đối chiếu liên kết trong đính chính và kiểm phần nối LOG. Các phép kiểm dùng đầu ra có sẵn.
4. Không có phản đối của hai bên về nội dung đính chính. Hiệu quả của chiều đảo, đánh giá độc lập và nhãn vùng vẫn OPEN. Minh quyết nghiệm thu, nền T-051 và có cần thử ứng viên đảo cạnh hay không. G3 và test khóa.

Bước tiếp theo. Đọc bản đính chính và hồ sơ ở hai manifest. Minh có thể dùng prompt dưới để chuyển Claude kiểm phần đính chính. Có thể dừng phản biện khi Minh chấp nhận phạm vi và phần OPEN đã ghi.

Lệnh cuối khi ghi. Python ghim với -B, kiểm SHA-256 bằng hashlib.file_digest cho hai danh sách đầu ra và kiểm đường dẫn trong đính chính trước khi nối LOG. Sau khi nối, kiểm tiền tố LOG và hash của bản đính chính.

- Bản đính chính `results/T-050/dinh-chinh-va-kiem-lai.md` (40f37f277a428263acae66692f6a927520d0aee865e89375e927de6ced9687dc).
- Manifest Phiên 4 `results/T-050/manifest-chay-lai-002.json` (670a573f18889ebc5df9094e5b83d9294a4e34824375dc3c2f1c2d20c7fd7b98).

## Prompt Claude kiểm lại phần đính chính T-050

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-050, tasks/T-050-t9-va-t10/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/KE-HOACH-SAU-T047.md, SPEC T-043, SPEC và LOG T-050, git diff hiện hành.
- Phản biện và phản hồi trước: bản soát kết quả, bản đáp của Codex, bản kiểm lại của Claude do Minh chuyển và mục đáp phản biện trong LOG T-050.
- Code và kết quả liên quan: results/T-050/dinh-chinh-va-kiem-lai.md, results/T-050/bao-cao.md, results/T-050/manifest.json, results/T-050/manifest-chay-lai-002.json, results/T-043/dac-ta-phuong-phap-v1.md, src/m1/ và src/m1_danh_gia/.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 6 — 04/11/2026 — Codex — laptop Windows — người làm

### Minh nghiệm thu T-050

1. Minh: “duyệt nghiệm thu, tạo spec cho task tiếp theo”. Đóng T-050 trong phạm vi chạy, kiểm, mô tả và phân tích dev chế độ (a) đã báo cáo và đính chính. T9 kết luận HẠI cho E6b theo chiều bên gọi → bên được gọi trên nền z đã khai. T10, C-c và C-g đã báo trong phạm vi SPEC.
2. Chỉ nối LOG T-050 và chuyển đúng dòng T-050 trong STATE sang xong. Hồ sơ kết quả và đính chính là nguồn đối chiếu. Đề xuất SPEC T-051, rà thời lượng T-050 và các lựa chọn được trình trong nội dung bàn giao theo yêu cầu Minh.
3. Trước khi đóng, kiểm hash 378 đầu ra gốc, 294 đầu ra lượt chạy lại, seal và hai bản kiểm của lượt mới. Hash bản đính chính khớp dòng ghim tại Phiên 5. Kiểm phần LOG chỉ nối thêm và STATE chỉ đổi một dòng.
4. Việc chọn nền T-051 và có thử ứng viên đảo cạnh còn OPEN. Đề xuất theo kết quả T9 là giữ E6a+S1 và tắt E6b. Chưa phân xử biến thể đảo cạnh, tác dụng quan hệ của cả chuỗi, hiệu quả trên dữ liệu độc lập, vùng ảnh hưởng đầy đủ, cờ E2 và verdict. G3/test vẫn khóa.

Bước tiếp theo. Đọc docs/KE-HOACH-SAU-T047.md mục T-051 và cập nhật 03/11, SPEC T-043 B4/Phụ lục C, cùng đề xuất SPEC trong bàn giao. Khi Minh chốt nền và duyệt đề xuất theo phạm vi, mới ghi SPEC T-051 và triển khai theo quyền đã cấp.

Lệnh cuối cho phần đóng. Python ghim -B kiểm SHA-256 các manifest T-050 và hash bản đính chính, nối LOG, thay đúng dòng T-050 trong STATE rồi kiểm hai thay đổi.

Đề xuất ghi DECISIONS khi Minh duyệt đúng câu. Ngày 04/11/2026, Minh nói “duyệt nghiệm thu, tạo spec cho task tiếp theo”. Nghiệm thu T-050 trong phạm vi kết quả dev chế độ (a), theo báo cáo và bản đính chính. Kết cục HẠI chỉ áp dụng cho E6b đã thử. Nền T-051 và thử chiều đảo quyết riêng. G3/test vẫn khóa.

Đề xuất nội dung commit khi Minh yêu cầu. Ghi hồ sơ T-050 gồm kết quả dev, phép phát lại và chạy lại, đính chính và nghiệm thu. Xác định tập tệp và loại đầu ra lớn trước commit.
