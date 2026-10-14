# T-034 — Kết quả hai phép kiểm E1 và E2

Ngày 13/10/2026. Người làm: Claude. Người phản biện kết quả: Codex.

Hai phép này trả lời hai câu mà gói đính chính ngày 13/10 của T-032 và T-033 ghi là “còn kiểm được, chưa chạy”. Cả hai chỉ dùng ca dev. Cả hai là **chẩn đoán**: không thay số, cấu hình hay cách chấm của bảng baseline đã khóa.

Thiết kế và bảng diễn giải được viết trước khi chạy nhánh đổi: `results/T-034/thiet-ke-hai-phep-kiem.md` (bản đầu và năm mục nối có thời điểm). Số trong file này lấy từ `results/T-034/hai-phep-kiem.json`; file đó gom đầu ra của các lượt trong `results/T-034/runs/`.

## 0. Tóm tắt

**E1 (TraceRCA, quy tắc pattern).** Bản cài theo lời văn của bài chấm một dịch vụ bằng giá trị lớn nhất qua mọi tập dịch vụ được giữ có chứa nó. Phép kiểm chỉ đổi đúng điểm đó: chỉ cho tập một dịch vụ đóng góp điểm, giữ nguyên mọi thứ khác.

- Ở cờ một lần độ lệch chuẩn (mặc định của bài), trong {{e1.top.nz.phen}} cặp Nezha-OB có hiện tượng: {{e1.top.nz.flip}} cặp đảo chiều; {{e1.top.nz.unch_both}} cặp có điểm của dịch vụ gọi giảm nhưng chưa đảo chiều; {{e1.top.nz.rootnone}} cặp giữ nguyên cả điểm lẫn quan hệ, trong điều kiện root không có tập nào được chấm. Ở RE2-TT: {{e1.top.re2.flip}}/{{e1.top.re2.phen}} cặp đảo chiều. Vậy quy tắc “chấm qua tập nhiều dịch vụ” **có đóng góp**: nó là bước quyết định ở cặp đảo chiều và làm tăng điểm của dịch vụ gọi ở phần lớn cặp. Nhưng nó **không đủ** để giải thích các cặp còn lại, cũng không đủ giải thích chênh giữa bản cài theo lời văn và mã tác giả.
- Ở cờ ba lần độ lệch chuẩn: {{e1.top3.nz.flip}}/{{e1.top3.nz.phen}} cặp Nezha-OB đổi chiều, cả hai bên vẫn còn bằng chứng. Ở cấu hình này quy tắc đó là bước quyết định ở phần lớn cặp Nezha-OB.
- RE2-TT không đổi ở cả ba nhánh: root không có tập nào được giữ, nên quy tắc pattern không chạm tới root.

**E2 (BOCPD, miền log).** Tính lại toàn bộ posterior trong miền log trên bốn chuỗi của hai ca có underflow.

- {{e2.chains_equal}}/{{e2.chains}} chuỗi: trạng thái có xác suất cao nhất (MAP) và điểm đổi (CP) trùng bản gốc ở mọi bước.
- {{e2.chains_differ}} chuỗi (đầu vào full của {{e2.diff.case:x}}): MAP khác ở {{e2.diff.m}} bước liên tiếp ngay sau mốc tiêm; bản gốc có {{e2.diff.cp_only_native}} điểm đổi mà phép tính đúng không có và thiếu {{e2.diff.cp_only_log}} điểm đổi. Mọi khác biệt nằm trong {{e2.diff.window_s}} giây đầu sau mốc.
- Ở cả bốn chuỗi, báo động đầu và mọi điểm đổi trước mốc tiêm giữ nguyên. Underflow không giải thích các báo động trước mốc của hai ca này.

## 1. E1 — Quy tắc pattern của TraceRCA

### 1.1 Câu hỏi và yếu tố bị đổi

Câu hỏi: ở các cặp (root, dịch vụ gọi) mà dịch vụ gọi đứng trên root trong bản cài theo lời văn, việc cho dịch vụ lấy điểm từ tập nhiều dịch vụ có phải là bước gây ra điều đó không?

Giữ nguyên: lời gọi, cờ bất thường, trace nào chứa dịch vụ nào, tập phổ biến đã khai phá, tập được giữ sau bước chọn, công thức điểm, quy tắc hòa. Đổi đúng một thứ: tập nào trong chính danh sách được giữ được phép đóng góp điểm (mọi tập, hoặc chỉ tập một dịch vụ). Không khai phá lại, không thêm tập một dịch vụ đã bị loại.

Phạm vi khai trước: {{e1.pairs}} cặp thuộc {{e1.cases}} ca trong bảng đối chiếu của gói đính chính (`closure-ledger-review-001.json`, mục `h6_pair_audit`). Ba nhánh cờ: `to_p` (một lần độ lệch chuẩn, span phía gọi; nhánh chính), `to_p3` (ba lần), `to_c` (span phía được gọi; báo phụ). Các cặp chung một ca không độc lập.

Trước khi can thiệp tôi đọc lại Mục III-B và III-C của bài TraceRCA và mã tác giả đã ghim. Bài viết điểm dịch vụ là giá trị lớn nhất qua **mọi** tập nghi ngờ chứa nó. Mã tác giả chỉ chấm tập một dịch vụ. Vậy bản cài theo lời văn khớp bài ở điểm này; không có căn cứ gọi quy tắc “chấm qua mọi tập” là lỗi cài.

### 1.2 Kiểm tương đương (V6: {{e1.v6:x}})

- Bản giữ nguyên quy tắc cho kết quả trùng bản lưu của T-032 ở {{e1.sham}}/{{e1.cases}} ca, {{e1.shamdiff}} khác biệt trên mọi trường (điểm dạng phân số, hạng, tập tốt nhất, trạng thái).
- Bản tính lại độc lập (khai phá bằng cách khác, số học phân số) trùng tập phổ biến, tập được giữ và điểm của cả hai nhánh ở {{e1.checks}}/{{e1.branches_ok}} kết quả nhánh có điểm.
- {{e1.nouse}} kết quả nhánh không có đặc trưng hữu ích; ghi trạng thái, không tính là điểm.
- Ví dụ nhỏ tính tay (ví dụ Hình 2 của bài) đúng cho cả hai quy tắc.
- Thời gian máy: {{e1.wall:.0f}} giây cho cả {{e1.cases}} ca trên EC2 của T-032.

### 1.3 Kết quả theo cặp

**Nhánh chính `to_p` (cờ một lần độ lệch chuẩn).**

@@e1_pairs:to_p@@

**Nhánh `to_p3` (cờ ba lần độ lệch chuẩn).**

@@e1_pairs:to_p3@@

**Nhánh `to_c` (span phía được gọi, báo phụ).**

@@e1_pairs:to_c@@

Cột “Mã tác giả” lấy nguyên từ bảng đối chiếu của gói đính chính, để đặt cạnh. Đó là pipeline khác; chênh giữa hai pipeline không phải tác dụng của phép đổi này.

### 1.4 Đọc kết quả

**Nezha-OB, nhánh chính.** Trong {{e1.top.nz.phen}} cặp có hiện tượng (root dưới dịch vụ gọi):

- {{e1.top.nz.multi}} cặp có điểm của dịch vụ gọi do một tập nhiều dịch vụ quyết định, và điểm đó giảm ở {{e1.top.nz.scorechg}} cặp khi chỉ chấm tập một dịch vụ. Mức giảm tương đối lớn nhất là {{e1.front.drop_max:pct1}}.
- Chia theo kết quả: {{e1.top.nz.flip}} cặp đảo chiều; {{e1.top.nz.unch_both}} cặp có điểm của dịch vụ gọi giảm nhưng chưa đảo chiều; {{e1.top.nz.rootnone}} cặp giữ nguyên cả điểm lẫn quan hệ, trong điều kiện root không có tập nào được chấm. Ở cặp cuối, phép đổi đã chạy và cho kết quả; nó chỉ không đánh giá việc bổ sung tập cho root.
- Vậy phép đổi **có tác động lên điểm** ở hầu hết các cặp, nhưng **không đổi quan hệ thứ hạng** ở hầu hết các cặp. Tập một dịch vụ của frontend tự nó đã đủ cao.

Trung gian cho thấy vì sao. Ở {{e1.front.pairs}} cặp có dịch vụ gọi là frontend, frontend mang cờ ở lời gọi đi ra trong {{e1.front.share_min:pct1}} đến {{e1.front.share_max:pct0}} số trace bất thường. Trong đó có từ {{e1.front.noroot_min}} đến {{e1.front.noroot_max}} trace mà root không mang cờ ở lời gọi đi vào. Đây là mô tả từ bảng cờ đã lưu, chưa phải phép đổi: nó chỉ ra bước cần xét tiếp là **lời gọi nào được gắn cờ**, không phải cách gộp tập.

**Nezha-OB, cờ ba lần.** {{e1.top3.nz.flip}}/{{e1.top3.nz.phen}} cặp có hiện tượng đổi sang “root trên”, cả root và dịch vụ gọi vẫn còn tập được chấm. Thêm {{e1.top3.lost}} cặp chuyển từ hòa sang “root trên” vì dịch vụ gọi mất mọi tập được chấm; trường hợp này ghi riêng là mất bằng chứng, không tính là bằng chứng dịch vụ gọi bình thường.

**RE2-TT.** Ở cả ba nhánh, {{e1.top.re2.phen}} cặp có hiện tượng đều giữ nguyên; điểm của dịch vụ gọi không đổi ở cặp nào ({{e1.top.re2.scorechg}} cặp đổi điểm). Lý do nằm ở bước trước đó: root không có tập nào trong danh sách được giữ ở {{e1.top.re2.rootnone}}/{{e1.top.re2.phen}} cặp. Tập chỉ gồm root là tập phổ biến ở {{e1.re2.freq}}/{{e1.re2.cases}} ca (có mặt trong {{e1.re2.sup_min:pct0}} đến {{e1.re2.sup_max:pct0}} trace bất thường) nhưng lọt vào danh sách được giữ ở {{e1.re2.intop}} ca. Bước loại nó là bước chọn tập theo điểm, không phải quy tắc chấm.

**Đặt cạnh mã tác giả.** Ở Nezha-OB mã tác giả (ngưỡng chọn đặc trưng một) cho root trên dịch vụ gọi ở {{h6.author.nz.t1.above}}/{{h6.author.nz.t1.pairs}} cặp. Phép E1 ở cùng mức cờ đảo chiều {{e1.top.nz.flip}} cặp. Vậy quy tắc pattern giải thích được một phần nhỏ của khác biệt giữa hai pipeline ở mức cờ này; phần còn lại nằm ở các bước E1 không đụng tới (dựng lời gọi, chọn đặc trưng theo cặp, chuẩn nền, chọn tập).

**Giới hạn của cặp đảo chiều.** Cặp đó thuộc ca `dev-63c30faf34`, là ví dụ đã được nhìn trước khi chạy và đã gợi ra giả thuyết trong gói đính chính. Can thiệp vẫn xác lập tác động riêng của quy tắc tại cặp này (mức CT); nó không phải xác nhận trên mẫu độc lập, nên không dùng để suy rộng.

### 1.5 Kết luận trong phạm vi đã thử

| Câu | Trả lời | Mức |
|---|---|---|
| Ở cờ một lần độ lệch chuẩn, chấm qua tập nhiều dịch vụ có phải bước đưa dịch vụ gọi lên trên root? | Đã xác lập ở {{e1.top.nz.flip}} cặp Nezha-OB (ca đã nhìn). Đã loại như giải thích đủ: ở {{e1.top.nz.unch_both}} cặp điểm dịch vụ gọi giảm mà chưa đảo chiều; ở {{e1.top.nz.rootnone}} cặp Nezha-OB và {{e1.top.re2.phen}} cặp RE2-TT root không có tập được chấm nên điểm và quan hệ giữ nguyên | CT |
| Ở cờ ba lần độ lệch chuẩn? | Đã xác lập cho Nezha-OB: {{e1.top3.nz.flip}}/{{e1.top3.nz.phen}} cặp đổi chiều khi chỉ đổi quy tắc này | CT |
| Bước nào gây chênh giữa bản cài theo lời văn và mã tác giả ở cờ một lần? | Chưa phân xử. Hai ứng viên có trung gian chỉ ra: cờ ở lời gọi đi ra của frontend; bước chọn tập loại tập chỉ gồm root ở RE2-TT | MT |

Phép này **không** cho biết: dịch vụ gọi có thật sự chờ root hay không (không đo lan vật lý); quy tắc nào “đúng”; phương pháp nào tốt hơn. Kết quả không suy rộng ra ngoài {{e1.pairs}} cặp và ba nhánh cờ đã khai.

### 1.6 Hệ quả

- Bản đồ hạn chế, dòng G2-H05: thay “ứng viên pattern nhiều dịch vụ, chưa kiểm riêng” bằng kết quả trên.
- Ứng viên “quy tắc chấm pattern” ở mục 5 của gói G2: có căn cứ ở cờ ba lần; ở cờ một lần quy tắc có tác động lên điểm và đảo chiều một cặp, không đủ cho các cặp còn lại.
- Hai phép còn kiểm được trên dev, chưa được giao (mục 6 của gói G2): chỉ đổi bước chọn tập; đối chiếu cờ theo từng lời gọi với nhánh mã tác giả.

## 2. E2 — BOCPD đầy đủ trong miền log

### 2.1 Câu hỏi và yếu tố bị đổi

BOCPD bản BARO nhân xác suất rất nhỏ qua nhiều bước. Khi một giá trị nhỏ hơn mức số thực biểu diễn được, nó bị làm tròn thành không (underflow) và nhánh đó không bao giờ sống lại. Câu hỏi: điều đó có làm đổi posterior, MAP hay điểm đổi không?

Giữ nguyên: dữ liệu X, thứ tự cột, prior, hazard, lớp phân phối dự báo và phép cập nhật tham số của mã gốc, quy ước chỉ số và quy tắc điểm đổi. Đổi đúng một thứ: phép đệ quy posterior được tính bằng log-mật độ và chuẩn hóa log-sum-exp ở mọi bước, thay cho nhân và chia số thực thường. Không thêm sàn, nhiễu hay cắt run length.

Phạm vi: hai ca `dev-3ae0a6c15a` và `dev-ba831dbeb8`; mỗi ca hai chuỗi: FF (tiền xử lý trên cả bản ghi, là đầu vào của baseline) và PF (chuỗi tiền tố trước mốc, mặt nạ cột của tiền tố, **thang của toàn bản ghi**; nhánh chẩn đoán của T-033). PF vẫn nhìn trước qua thang, nên không phải bằng chứng cho tiền xử lý chỉ dùng quá khứ.

### 2.2 Kiểm tương đương (V7: {{e2.v7:x}})

- **Ví dụ nhỏ (F1–F4), chạy trên cùng máy và môi trường:** đạt cả bốn (trường `fixtures_pass`: {{e2.fx.pass}}). F1 không underflow: bản miền log trùng bản gốc. F2 có underflow: bản miền log trùng tham chiếu độ chính xác cao (mpmath). F3 là đối chứng dương: một nhánh đã bị bản gốc cho bằng không phải sống lại; bản miền log trùng tham chiếu, bản gốc thì không. F4 kiểm chính tham chiếu số thực mở rộng.
- **Bản giữ nguyên:** chạy lại mã gốc cho R trùng bản lưu của T-033 **từng bit** ở {{e2.sham_bit}}/{{e2.chains}} chuỗi.
- **Tham chiếu độc lập trên chuỗi thật:** chạy đúng đệ quy tuyến tính của mã gốc bằng số thực mở rộng 80 bit (không có log-sum-exp). MAP và CP của tham chiếu trùng bản miền log ở {{e2.ext_pass}}/{{e2.chains}} chuỗi; lệch log lớn nhất {{e2.ext_err:e}} (ngưỡng khai trước `1e-8`).
- **Trước khi underflow có khối lượng đáng kể,** trạng thái sạch lệch nhiều nhất {{e2.clean_err:e}} giữa bản gốc và bản miền log (ngưỡng `1e-9`).
- **Đối chiếu với phép cũ của T-033** (giữ cố định hệ số chuẩn hóa, từng nhánh): lệch nhiều nhất {{e2.lineage_err:e}}.

Lượt đầu (`e2-001`) tôi đặt một luồng tính cho thư viện đại số, khác cấu hình của lượt gốc. Khi đó R không trùng từng bit: mật độ lệch tương đối tới {{e2.det.one.rel:e}} và chỉ {{e2.det.one.frac:pct0}} phần tử R trùng bit; với cấu hình của nguồn thì {{e2.det.unset.rows}}/{{e2.det.unset.total}} hàng mật độ trùng bit. MAP và CP của bản miền log ở lượt đó trùng lượt dùng để kết luận ở {{e2.cross_m}}/{{e2.chains}} chuỗi. Lượt `e2-001` được giữ làm đối chiếu, không dùng để kết luận.

### 2.3 Bốn chuỗi

@@e2_chains@@

Bản gốc cho bằng không từ {{e2.zero_min}} đến {{e2.zero_max}} trạng thái mỗi chuỗi. Bản miền log hữu hạn ở mọi trạng thái đạt được.

### 2.4 Chuỗi có khác biệt: đầu vào full của {{e2.diff.case:x}}

- MAP khác ở {{e2.diff.m}} bước liên tiếp, chỉ số {{e2.diff.m_first}} đến {{e2.diff.m_last}} (mốc tiêm ở chỉ số `720`).
- Ở bước khác đầu tiên, bản gốc chọn nhánh bắt đầu từ chỉ số {{e2.diff.lin_nat}}; bản miền log chọn nhánh bắt đầu từ chỉ số {{e2.diff.lin_log}}. Bản gốc đã cho nhánh thứ hai khối lượng đúng bằng {{e2.diff.native_at_logmap}} từ trước.
- Phân loại {{e2.diff.m}} bước: {{e2.diff.cls.direct}} bước trạng thái MAP đúng là trạng thái bị underflow; {{e2.diff.cls.down}} bước là hệ quả trong cùng đoạn phân kỳ; {{e2.diff.cls.other}} bước không giải thích được.
- Khối lượng của các trạng thái bị ảnh hưởng vượt `1e-12` lần đầu ở cột {{e2.diff.first_mass_col}} và lên tới {{e2.diff.mass:.2f}}. Hai posterior phân kỳ (khoảng cách biến thiên toàn phần trên `1e-6`) ở {{e2.diff.div_cols}} cột liên tiếp, {{e2.diff.win_first}} đến {{e2.diff.win_last}}; khoảng cách lớn nhất {{e2.diff.tv:.2f}}.
- Điểm đổi: bản gốc {{e2.diff.cp_n}}, bản miền log {{e2.diff.cp_l}}. Bản gốc có điểm đổi tại chỉ số {{e2.diff.cp_nat.0}} mà bản miền log không có; bản miền log có tại {{e2.diff.cp_log.0}}, {{e2.diff.cp_log.1}}, {{e2.diff.cp_log.2}} mà bản gốc không có. Mọi điểm đổi khác trùng nhau.
- Điểm đổi đầu tiên sau mốc: {{e2.diff.delay_n}} giây sau mốc ở bản gốc, {{e2.diff.delay_l}} giây ở bản miền log.
- Không đổi: báo động đầu (chỉ số {{e2.diff.first}}, trước mốc); {{e2.diff.pre_n}} điểm đổi trước mốc ở cả hai bản; số cửa sổ 60 giây đổi trạng thái: {{e2.diff.win_changed}}.

### 2.5 Ba chuỗi không khác

MAP và CP trùng ở mọi bước. Ở chuỗi PF của `dev-ba831dbeb8` có {{e2.ba8.pf.dirty}} trạng thái lệch quá `1e-9` vì nhánh của chúng từng rơi xuống vùng số dưới chuẩn hóa (mất chữ số có nghĩa, chưa về không); lệch log lớn nhất {{e2.ba8.pf.dirtyerr:.2f}}. Khối lượng log lớn nhất của các trạng thái đó là {{e2.ba8.pf.dirtymass:.1f}}, quá nhỏ để chạm tới MAP.

### 2.6 Kết luận trong phạm vi đã thử

| Câu | Trả lời | Mức |
|---|---|---|
| Underflow có làm đổi MAP hoặc điểm đổi không? | Có, ở {{e2.chains_differ}}/{{e2.chains}} chuỗi đã kiểm, trong một đoạn {{e2.diff.window_s}} giây ngay sau mốc tiêm | CT |
| Underflow có giải thích báo động trước mốc của hai ca này không? | Đã loại: báo động đầu và mọi điểm đổi trước mốc giữ nguyên ở {{e2.pre_same}}/{{e2.chains}} chuỗi | CT |
| Có đổi số của bảng baseline không? | Không. Bảng baseline giữ nguyên số đã khóa. Ở chuỗi có khác biệt, không cửa sổ 60 giây nào đổi trạng thái | — |
| Còn ca nào khác bị ảnh hưởng? | Chưa biết. Chỉ hai ca này được tính lại trong miền log | CK |

Điều kết quả này sửa trong cách dùng số cũ: phép cũ của T-033 (giữ hệ số chuẩn hóa) đúng ở các điểm đã kiểm, nhưng câu “underflow không đổi MAP” không được mở rộng ra cả chuỗi. Ở chuỗi full của {{e2.diff.case:x}} nó có đổi, ở một đoạn ngắn.

Không suy ra: bản miền log phát hiện tốt hơn; số điểm đổi nhiều hơn là tốt hơn; kết quả đúng cho các ca dev còn lại.

### 2.7 Chi phí đo được

Tổng thời gian máy của bốn chuỗi ở lượt dùng để kết luận: {{e2.machine_s:.0f}} giây (mỗi chuỗi gồm bản giữ nguyên, bản miền log, tham chiếu mở rộng). Chuỗi full: {{e2.3ae.ff.total_s:.0f}} và {{e2.ba8.ff.total_s:.0f}} giây; chuỗi PF: {{e2.3ae.pf.total_s:.0f}} và {{e2.ba8.pf.total_s:.0f}} giây. Bộ nhớ đỉnh quan sát được: {{e2.3ae.ff.rss}} byte. Mỗi chuỗi lưu một file gọn; chuỗi lớn nhất {{e2.3ae.ff.npz}} byte.

## 3. Lượt chạy và nguồn

| Lượt (trong `results/T-034/runs/`) | Nội dung | Dùng để kết luận |
|---|---|---|
| `e1-001` | E1, đủ {{e1.cases}} ca, ba nhánh | Có |
| `e2-fixtures-laptop-001-fail` | Ví dụ F2 thiết kế sai (không tạo được underflow) | Không; giữ làm lượt lỗi |
| `e2-fixtures-laptop-002`, `e2-fixtures-laptop-003-v3` | Ví dụ nhỏ trên laptop | Kiểm phụ |
| `e2-001` | Bốn chuỗi, một luồng tính (khác cấu hình nguồn) | Không; đối chiếu |
| `e2-determinism-001` | Phép kiểm tất định theo số luồng | Kiểm phụ |
| `e2-fixtures-ec2-002-v3-fail`, `e2-fixtures-ec2-003-v3-fail` | Ví dụ F4 hỏng vì lỗi của bản cài tham chiếu | Không; giữ làm lượt lỗi |
| `e2-fixtures-ec2-004-v3` | Ví dụ F1–F4 đạt | Có |
| `e2-002` | Hai chuỗi PF; hai chuỗi FF bị dừng ở bước giữ nguyên vì chạy quá chậm | Phần PF: có |
| `e2-003` | Hai chuỗi FF, chạy lần lượt | Có |
| `e2-used-001` | Bản gom bốn chuỗi dùng để kết luận (chép từ hai lượt trên, có kiểm mã băm) | Có |

Mã nguồn không bị sửa: bản cài theo lời văn của T-032, mã BOCPD của BARO và mọi kết quả cũ chỉ được đọc. Script của hai phép nằm ở `results/T-034/scripts/` (`e1_pattern_rule.py`, `e2_bocpd_log_v3.py`). Mã băm hai đầu của từng lượt nằm cạnh thư mục lượt.
