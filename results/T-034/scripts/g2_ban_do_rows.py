"""T-034 K3: nội dung các dòng G2-Hn của bản đồ hạn chế hợp nhất (văn bản do người làm viết; số qua {{mã số}} của sổ số liệu).

Quy ước của trường `vi_sao`: mở đầu bằng một trong ba trạng thái của WHY-51:
"Đã xác lập ở mức …", "Đã loại …", "Chưa phân xử, vì …". Không viết "nguyên nhân là" khi mức chỉ là LĐ hoặc MT.
Mã gốc: H1–H17, D1–D7 (results/T-032/nguyen-nhan-xep-hang.md); M0–M6 (T-028); HP-1–HP-14 (T-029);
"T-032:KTn" và "T-033:Kn" là câu hỏi trong closure-ledger.json#/questions (đọc cùng closure-ledger-review-001.json).
"""
import re


def ids(text):
    return sorted(set(m.split(":")[0] for m in re.findall(r"\{\{([^}]+)\}\}", text)))


ROWS = [
    dict(id="G2-H01", ten="MicroRank (bản RCAEval): bước chia trace bất thường/bình thường",
         phuong_phap="MicroRank, bản trong RCAEval đã sửa đầu vào", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["H1", "T-032:KT1"],
         hien_tuong="Root hiếm khi đứng hạng 1. Luật “trace bất thường khi có bất kỳ span nào vượt nền cộng ba lần độ lệch chuẩn” xếp khoảng một nửa trace vào nhóm bất thường.",
         so="Hạng 1: {{t28.re2.microrank_full.dung}}/{{t28.re2.microrank_full.n}} ca RE2-TT ({{t28.re2.microrank_full.khongok}} ca ERROR) và {{t28.nz.microrank_full.dung}}/{{t28.nz.microrank_full.n}} ca Nezha-OB. "
            "Thay riêng bước chia bằng công thức của bài gốc (hai biến thể `mo15` và `mo1p50`): hạng 1 từ {{h1.mo15.native}} lên {{h1.mo15.hit1}}–{{h1.mo1p50.hit1}} trên {{h1.mo15.evaluable}} ca xét được; "
            "{{h1.mo1p50.gone}}–{{h1.mo15.gone}}/{{h1.mo15.pairs}} cặp (thực thể đứng trên root, root) mất. "
            "Tỷ lệ trace bất thường ở RE2-TT (trung vị): {{h1.share.native:pct0}} xuống {{h1.share.mo15:pct0}}. "
            "Mốc giả không có lỗi: vẫn {{h1.fake.median:pct1}} trace bị xếp bất thường (trung vị {{h1.fake.n}} ca RE2-TT).",
         vi_sao="Đã xác lập ở mức CT: bước chia của bản thư viện là bước làm mất thông tin “trace nào thật sự chậm”. Chưa phân xử phần còn lại sau khi thay bộ chia.",
         muc="CT", muc_nguon_con=[("phép đổi bộ chia trace (T-032, KQ11 mục 4)", "CT"), ("mốc giả cùng độ dài cửa sổ (T-032, KQ13 mục 1)", "LĐ")],
         loai_nguon="A", giai_thich_khac="Bộ chia thay thế dùng quy ước span đầu của ta, nghĩ ra sau khi xem dev; không phải MicroRank gốc. Sau khi thay vẫn còn hơn một nửa số ca chưa hạng 1 (xem G2-H02).",
         tac_gia="Không áp dụng: bài gốc chia theo thời gian của cả yêu cầu, không theo từng span.", rq="RQ1, RQ2"),
    dict(id="G2-H02", ten="MicroRank: đếm phủ của spectrum và trọng số PageRank",
         phuong_phap="MicroRank, bản trong RCAEval đã sửa đầu vào", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["H2", "H3", "T-032:KT3"],
         hien_tuong="Một thao tác được tính cho mọi trace bất thường chứa nó; trọng số PageRank theo nhóm trace nhân vào spectrum.",
         so="Đếm riêng thay đếm phủ: hạng 1 từ {{h2.c1.native}} lên {{h2.c1.hit1}} trên {{h2.c1.n}} ca; {{h2.c1.gone}}/{{h2.c1.pairs}} cặp mất; {{h2.c1.down}} ca root giảm hạng. "
            "Trọng số đơn vị: hạng 1 từ {{h2.w.native}} lên {{h2.w.hit1}}; {{h2.w.gone}}/{{h2.w.pairs}} cặp mất; {{h2.w.up}} ca tăng hạng, {{h2.w.down}} ca giảm.",
         vi_sao="Đã xác lập ở mức CT rằng mỗi bước có tác động lên hạng. Chưa phân xử tác dụng của trọng số khi nhóm trace đổi: gói bổ sung cho thấy đổi trọng số có lúc giúp, có lúc làm kém, tùy phân nhóm.",
         muc="CT", muc_nguon_con=[("phép đổi M-C1 và A′ (T-032, KQ9 mục 2)", "CT"), ("đối chứng trọng số × số đếm trên support chung (gói bổ sung, KT3)", "CT")],
         loai_nguon="M", giai_thich_khac="Hai phép đổi chạy trên nhóm trace của bản thư viện (G2-H01), nên không cộng được với phép đổi bộ chia. Không có căn cứ cho quy tắc chung “bỏ trọng số là sửa được”.",
         tac_gia="Không nêu.", rq="RQ1, RQ2"),
    dict(id="G2-H03", ten="TraceRCA (bản RCAEval): thời gian chờ root được chấm thành bất thường của dịch vụ gọi",
         phuong_phap="TraceRCA, bản trong RCAEval có lọc giá trị không hữu hạn", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["H4", "T-032:KT2", "T-032:KT13"],
         hien_tuong="Span của dịch vụ gọi bao lời gọi tới root; khi lời gọi đó chậm, span của dịch vụ gọi vượt ngưỡng và cờ được tính cho dịch vụ gọi.",
         so="Trong các cặp (dịch vụ phía trên đứng trên root) xét được, từ một nửa span mang cờ trở lên là span bao lời gọi chậm tới root: {{h4.re2.wait}}/{{h4.re2.n}} cặp RE2-TT, {{h4.nz.wait}}/{{h4.nz.n}} cặp Nezha-OB. "
            "Ở ca **đúng** của RE2-TT cũng vậy: {{h4.right.wait}}/{{h4.right.n}} dịch vụ phía trên. "
            "Đổi cờ sang phần span không do span con phủ: số ca có dịch vụ gọi trên root {{h4.td.re2.before}} → {{h4.td.re2.after}} (RE2-TT), {{h4.td.nz.before}} → {{h4.td.nz.after}} (Nezha-OB). "
            "Mốc giả so mốc thật: tỷ lệ span mang cờ ở thao tác phía trên root {{h4.up.fake:pct1}} → {{h4.up.real:pct1}}; ở thao tác không liên hệ {{h4.unrel.fake:pct1}} → {{h4.unrel.real:pct1}}.",
         vi_sao="Đã xác lập ở mức CT (RE2-TT) và ĐC (hai dataset) cho chuỗi: lời gọi tới root chậm → span bao nó mang cờ → dịch vụ gọi được điểm. Hiện tượng có cả ở ca đúng, nên riêng nó không phân biệt ca sai.",
         muc="CT", muc_nguon_con=[("phép đổi T-D (T-032, KQ9 mục 3)", "CT"), ("bảng nối lời gọi chậm với span mang cờ (KQ11 mục 2.1)", "ĐC"), ("mốc giả theo thao tác (KQ13 mục 2)", "LĐ")],
         loai_nguon="A", giai_thich_khac="Ở RE2-TT phải giả định công cụ ghi span, vì dataset không công bố. Phần chậm nằm ngoài span của root (đường truyền, hàng đợi, xử lý phía gọi) không tách được: mỗi lời gọi chỉ có hai span.",
         tac_gia="Có nêu, và bài gốc có bước xử lý; bản thư viện bỏ bước đó.", rq="RQ2, RQ3"),
    dict(id="G2-H04", ten="TraceRCA (bản RCAEval): điểm đi theo số span mang cờ tuyệt đối",
         phuong_phap="TraceRCA, bản trong RCAEval", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["H5", "T-032:KT4"],
         hien_tuong="Điểm `2a/(n + H)` lớn khi thao tác có nhiều span; thao tác của root ít span hơn thao tác của dịch vụ khác.",
         so="Xếp theo tỷ lệ a/n: {{h5.re2.tr1.gone}}/{{h5.re2.pairs}} cặp RE2-TT và {{h5.nz.tr1.gone}}/{{h5.nz.pairs}} cặp Nezha-OB mất, nhưng {{h5.re2.right.lose}}/{{h5.re2.right}} ca đang đúng của RE2-TT mất hạng 1. "
            "Xếp theo số tuyệt đối a: giữ {{h5.re2.ts.still}}/{{h5.re2.pairs}} và {{h5.nz.ts.still}}/{{h5.nz.pairs}} cặp.",
         vi_sao="Đã xác lập ở mức CT rằng thứ hạng gần như theo số tuyệt đối. Đã loại “đổi sang tỷ lệ” như một cách chữa: nó làm hỏng nhiều ca đúng.",
         muc="CT", muc_nguon_con=[("phép đổi công thức điểm T-R (T-032, KQ11 mục 8)", "CT")],
         loai_nguon="A", giai_thich_khac="Mức cờ tự nhiên của thao tác đông span ngay khi không có lỗi cũng tạo khối lượng; công thức không tách được tỷ lệ với khối lượng.",
         tac_gia="Không áp dụng: bài gốc đếm trace, không đếm span.", rq="RQ2"),
    dict(id="G2-H05", ten="TraceRCA cài theo lời văn của bài: dịch vụ gọi hoặc frontend đứng trên root",
         phuong_phap="Bước xếp hạng của bài TraceRCA, do ta cài theo lời văn (chẩn đoán); đối chiếu mã tác giả nhánh chỉ độ trễ (chẩn đoán)", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["H6", "T-032:KT11"],
         hien_tuong="Ở các cặp “chủ yếu là chờ root”, bản cài theo lời văn không đưa root lên trên dịch vụ gọi; mã tác giả (nhánh chỉ độ trễ) thì đưa root lên ở phần lớn cặp.",
         so="{{h6.pairs}} cặp thuộc {{h6.cases}} ca; {{h6.oldpairs}} cặp có quan hệ cũ. Mã tác giả, ngưỡng chọn đặc trưng bằng một: root trên {{h6.author.re2.t1.above}}/{{h6.author.re2.t1.pairs}} cặp RE2-TT "
            "(trong đó {{h6.author.re2.t1.above_with_caller_fallback}} do dịch vụ gọi nhận điểm mặc định) và {{h6.author.nz.t1.above}}/{{h6.author.nz.t1.pairs}} cặp Nezha-OB. "
            "**Phép E1** (chỉ đổi quy tắc pattern, giữ mọi thứ khác của bản cài theo lời văn): ở cờ một lần độ lệch chuẩn, {{e1.top.nz.flip}}/{{e1.top.nz.phen}} cặp Nezha-OB có hiện tượng đổi chiều và {{e1.top.re2.flip}}/{{e1.top.re2.phen}} cặp RE2-TT; "
            "ở cờ ba lần, {{e1.top3.nz.flip}}/{{e1.top3.nz.phen}} cặp Nezha-OB và {{e1.top3.re2.flip}}/{{e1.top3.re2.phen}} cặp RE2-TT.",
         vi_sao="Đã xác lập ở mức CT rằng việc chấm qua tập nhiều dịch vụ có đóng góp: ở cờ một lần độ lệch chuẩn (mặc định của bài) nó là bước quyết định ở {{e1.top.nz.flip}} cặp Nezha-OB (ca đã nhìn trước, không suy rộng) "
                "và ở cờ ba lần ở phần lớn cặp Nezha-OB. Đã loại nó như giải thích đủ ở cờ một lần: ở {{e1.top.nz.unch_both}} cặp điểm dịch vụ gọi giảm mà chưa đảo chiều; ở {{e1.top.nz.rootnone}} cặp Nezha-OB và các cặp RE2-TT "
                "root không có tập được chấm nên điểm và quan hệ giữ nguyên. Chưa phân xử bước gây chênh giữa hai pipeline ở cờ một lần; "
                "trung gian của E1 chỉ ra hai ứng viên: frontend mang cờ lời gọi đi ra ở gần như mọi trace bất thường, và ở RE2-TT tập chỉ gồm root bị bước chọn tập theo điểm loại.",
         muc="CT", muc_nguon_con=[("phép E1 của T-034 (hai-phep-kiem.md)", "CT"), ("đối chiếu các cặp với mã tác giả (bản đính chính ngày 13/10)", "MT"), ("đọc bài và mã (thiết kế E1 mục 2)", "MT")],
         loai_nguon="M + A", giai_thich_khac="Hai pipeline còn khác ở cách dựng lời gọi, chọn đặc trưng theo cặp, chuẩn nền và cách chọn tập; E1 không đụng tới các bước đó. Cả hai chỉ dùng một đặc trưng (độ trễ) và nền ngắn. "
                                           "Suy rộng cũ “trị tuyệt đối không mang hướng nên phải giữ dấu” đã rút (WHY-47, đính chính ngày 13/10).",
         tac_gia="Nêu một phần: bài tự ghi giới hạn khi bất thường lan cả hai chiều. Lời văn của bài chấm qua mọi tập; mã tác giả chỉ chấm tập một dịch vụ.", rq="RQ2, RQ3"),
    dict(id="G2-H06", ten="Trễ mạng: dấu hiệu nằm ở span phía gọi của lời gọi tới root",
         phuong_phap="BARO, SimpleRCA, TraceRCA (bản RCAEval)", dataset="Nezha-OB (network_delay); RE2-TT để đối chiếu", che_do="(a)",
         ma_goc=["H7", "M6", "T-032:KT5"],
         hien_tuong="Với lỗi trễ mạng, span của chính root ít vượt ngưỡng; span phía gọi của lời gọi tới root thì vượt. Cách tính theo dịch vụ sở hữu span chấm dịch vụ gọi.",
         so="Nezha-OB, {{h7.nd.n}} ca trễ mạng: root đứng đầu theo span của mình ở {{h7.nd.own}} ca, theo span phía gọi ở {{h7.nd.in}} ca; BARO, SimpleRCA, TraceRCA xếp root hạng 1 ở {{h7.nd.baro}}, {{h7.nd.simplerca}}, {{h7.nd.tracerca}} ca. "
            "Phần span không do span con phủ tách được root ở {{h7.re2.ownu}}/{{h7.re2.n}} ca RE2-TT (theo thời lượng cả span: {{h7.re2.ownd}}/{{h7.re2.n}}) và {{h7.nz.ownu}}/{{h7.nz.n}} ca Nezha-OB. "
            "Span phía gọi của lời gọi tới root: {{h7.re2.inu}}/{{h7.re2.inn}} ca RE2-TT, {{h7.nz.inu}}/{{h7.nz.inn}} ca Nezha-OB.",
         vi_sao="Đã xác lập ở mức ĐC **nơi có dấu hiệu** trong trace (đo trực tiếp theo vị trí, có mốc giả đối chứng). Chưa phân xử vì sao mỗi phương pháp xếp sai ở từng ca: mới là quan sát đặt cạnh thứ hạng. Mức CT của dòng chỉ thuộc phép thử gán tín hiệu theo cạnh (đổi cạnh thì đổi điểm, ở mức tính toán).",
         muc="CT", muc_nguon_con=[("bảng vị trí tín hiệu của root (T-032, KQ10 mục 3)", "ĐC"), ("mốc giả lùi vào nền (KQ10 mục 3)", "LĐ"), ("phép thử gán tín hiệu theo cạnh (gói bổ sung, KT5)", "CT")],
         loai_nguon="M + D", giai_thich_khac="Cờ M6 của T-028 (root thiếu bằng chứng cục bộ dương theo luật riêng của từng phương pháp) có ở trễ mạng trên Nezha-OB: SimpleRCA {{t28.nz.simplerca.M6}} ca, MicroRank {{t28.nz.microrank_full.M6}} ca, "
                                           "TraceRCA {{t28.nz.tracerca.M6}} ca; không có ở lỗi return. M6 không đồng nghĩa root không hạng 1 hay thiếu mọi tín hiệu. “Root đứng đầu theo một vị trí” không phải Hit@1 của một phương pháp. Định nghĩa vị trí đặt sau khi xem dev. Ở Nezha-OB một phần span có span con chạy chồng nhau, phép trừ phải xử lý chồng lấn.",
         tac_gia="Nêu một phần.", rq="RQ2, RQ3"),
    dict(id="G2-H07", ten="Lỗi return ở Nezha-OB: root không hạng 1 dù có dấu hiệu",
         phuong_phap="BARO, SimpleRCA, TraceRCA, MicroRank", dataset="Nezha-OB (return)", che_do="(a)",
         ma_goc=["H8"],
         hien_tuong="Root không đứng hạng 1 dưới các cách chấm đã xét, trong khi log lỗi tại root tăng và tỷ lệ thành công ở frontend giảm.",
         so="{{h8.n}} ca return; BARO, SimpleRCA, TraceRCA xếp root hạng 1 ở {{h8.baro}}, {{h8.simplerca}}, {{h8.tracerca}} ca; ở {{h8.norank}} ca root cũng không đứng đầu theo vị trí trace nào. "
            "Số dòng log khớp từ khóa lỗi tại root (cửa sổ giả → sớm → muộn sau mốc): "
            "{{h8.log.0.placebo}} → {{h8.log.0.early}} → {{h8.log.0.late}}; {{h8.log.1.placebo}} → {{h8.log.1.early}} → {{h8.log.1.late}}; "
            "{{h8.log.2.placebo}} → {{h8.log.2.early}} → {{h8.log.2.late}}; {{h8.log.3.placebo}} → {{h8.log.3.early}} → {{h8.log.3.late}}.",
         vi_sao="Đã loại ở mức LĐ giải thích “dữ liệu không có đáp ứng do lỗi”. Chưa phân xử cách dùng dấu hiệu nào định vị được root: SimpleRCA chỉ đếm giá trị tăng, BARO bỏ cột hằng ở nền, log chỉ cho một phiếu.",
         muc="LĐ", muc_nguon_con=[("cửa sổ đối xứng trước và sau mốc cho log và tỷ lệ thành công (gói bổ sung, đính chính mục 5)", "LĐ"), ("đọc mã SimpleRCA và adapter BARO", "MT")],
         loai_nguon="M + A + D", giai_thich_khac="Số dòng log không phải số yêu cầu lỗi. Hai ca root là checkoutservice có phản ứng metric ở frontend, không ở chính root. Đáp ứng thời lượng theo từng thao tác và onset vật lý còn mở.",
         tac_gia="Bài MicroRank nêu giới hạn khi lỗi không đổi độ trễ; chưa xác nhận điều kiện ấy cho từng ca.", rq="RQ2"),
    dict(id="G2-H08", ten="SimpleRCA: phiếu metric đếm theo mẫu lấn át trace và log",
         phuong_phap="SimpleRCA (M4, quy ước T-017)", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["H9"],
         hien_tuong="Một cột metric vượt ngưỡng gần suốt cửa sổ cho số phiếu bằng số mẫu vượt ngưỡng; trace và log mỗi loại chỉ cho nhiều nhất một phiếu.",
         so="{{h9.metric}}/{{h9.pairs}} cặp do riêng phiếu metric quyết định. Đếm theo cột thay đếm theo mẫu (RE2-TT): {{h9.s1.re2.gone}}/{{h9.s1.re2.pairs}} cặp mất, nhưng số ca hạng 1 tính bi quan từ {{h9.s1.re2.native}} xuống {{h9.s1.re2.changed}} vì hòa (tính lạc quan: {{h9.s1.re2.optimistic}}).",
         vi_sao="Đã xác lập ở mức CT. Đếm theo mẫu vừa là thứ gây sai vừa là thứ cho phương pháp khả năng phân biệt; đổi cách đếm không chữa được.",
         muc="CT", muc_nguon_con=[("phân rã cộng của điểm (T-032, KQ9 mục 4)", "ĐC"), ("phép đổi S-1", "CT")],
         loai_nguon="A + M", giai_thich_khac="Đơn vị “mỗi mẫu một phiếu” là quy ước của T-017 ở chỗ bài không khóa. Điểm tăng theo số cột và độ dài cửa sổ (WHY-17).",
         tac_gia="Nêu một phần.", rq="RQ1, RQ2"),
    dict(id="G2-H09", ten="BARO: chia cho IQR của nền gần phẳng",
         phuong_phap="BARO", dataset="RE2-TT (kết luận); Nezha-OB (không kết luận)", che_do="(a)",
         ma_goc=["H10", "T-032:KT12"],
         hien_tuong="Cột của dịch vụ khác gần phẳng ở đoạn nền; thay đổi nhỏ sau mốc thành điểm lớn.",
         so="RE2-TT, đổi sang thang độ lệch chuẩn: {{h10.gone}}/{{h10.pairs}} cặp mất; hạng 1 từ {{h10.native}} lên {{h10.changed}}; {{h10.lose}} ca đúng bị hỏng. "
            "Nezha-OB: {{h10.nz.native}} → {{h10.nz.changed}}, {{h10.nz.lose}} ca đúng bị hỏng. Không lọc cột hằng: hạng root không đổi ở {{h10.b1.same}}/{{h10.b1.n}} ca.",
         vi_sao="Đã xác lập ở mức CT cho RE2-TT. Đã loại việc lọc cột hằng như nguyên nhân làm root mất hạng dưới quy tắc chấm hiện tại; bước lọc có bỏ cột của root ở {{h10.b1.added}}/{{h10.b1.n}} ca, nhưng hạng của root không đổi ở ca nào. Đổi thang đưa root lên hạng 1 ở {{h10.re2.fixed}}/{{h10.re2.wrong}} ca sai RE2-TT và {{h10.nz.fixed}}/{{h10.nz.wrong}} ca sai Nezha-OB, nên thang IQR không giải thích hết các ca sai của BARO. Chưa phân xử các cặp còn lại: cột của dịch vụ khác đổi thật tại mốc, nguyên nhân vật lý không phân xử được bằng dữ liệu hiện có.",
         muc="CT", muc_nguon_con=[("phép đổi B-2 và B-1 (T-032, KQ9 mục 5)", "CT"), ("chuỗi cột độ trễ ở ba cặp ca cùng ô (KQ13 mục 3)", "MT")],
         loai_nguon="M", giai_thich_khac="Ở Nezha-OB mỗi phía chỉ có vài mẫu metric (mã D1 của T-032), IQR kém ổn định; phép đổi thang không kết luận được. Phép đổi nghĩ ra sau khi xem dev.",
         tac_gia="Không nêu.", rq="RQ1, RQ2"),
    dict(id="G2-H10", ten="Kênh bộ nhớ trôi ngay trong đoạn nền",
         phuong_phap="BARO, SimpleRCA", dataset="RE2-TT", che_do="(a)",
         ma_goc=["H11"],
         hien_tuong="Cột bộ nhớ của dịch vụ không liên quan trôi gần tuyến tính ở nền; chuẩn hóa theo độ biến thiên nền cho nó điểm cao.",
         so="Trong {{h11.memall}} cột bộ nhớ thắng root ở BARO, {{h11.mem}} cột thuộc nhóm trôi nền.",
         vi_sao="Chưa phân xử, vì mới là mô tả có phân nhóm; nhóm trôi nền chỉ giải thích một phần số cột thắng.",
         muc="MT", muc_nguon_con=[("bảng xu hướng nền của cột metric (T-032, KQ10 mục 4)", "MT")],
         loai_nguon="D + M", giai_thich_khac="Một phần cột bộ nhớ có bậc tại mốc; phần còn lại không thuộc nhóm nào. Mốc chia nhóm đặt trước nhưng bảng dựng sau khi xem dev.",
         tac_gia="Không nêu.", rq="RQ2"),
    dict(id="G2-H11", ten="Thực thể đứng trên root phần lớn nằm ngoài chuỗi gọi qua root",
         phuong_phap="BARO (kênh metric)", dataset="RE2-TT", che_do="(a)",
         ma_goc=["H12", "T-032:KT6"],
         hien_tuong="Metric của dịch vụ không liên hệ với root đổi tại mốc; quan hệ gọi tới root không mang thông tin về chúng.",
         so="Trong {{h12.pairs}} cặp của BARO: {{h12.nospan}} không có span, {{h12.roi}} rời chuỗi gọi, {{h12.chung}} chỉ chung phía trên; chỉ {{h12.up.latency}} cặp là dịch vụ phía trên thắng bằng cột độ trễ.",
         vi_sao="Chưa phân xử, vì dữ liệu không có ánh xạ dịch vụ–máy, metric mức máy hay nhật ký của bộ tiêm lỗi; không tách được “cùng máy”, “cùng tải” với quan hệ ẩn.",
         muc="MT", muc_nguon_con=[("bảng vị trí trên chuỗi gọi (T-032, KQ11 mục 1, 3)", "MT")],
         loai_nguon="D", giai_thich_khac="Cùng máy hoặc cùng tài nguyên; tải đổi theo lỗi; bộ tiêm tác động rộng hơn nhãn; quan hệ dữ liệu hoặc thông điệp không hiện trong trace.",
         tac_gia="Không áp dụng.", rq="RQ2, RQ5"),
    dict(id="G2-H12", ten="CIRCA: phần dư gần bằng không cho điểm cực lớn, bước DA cộng nó sang tổ tiên",
         phuong_phap="CIRCA (đồ thị kiến trúc, OLS+RHT+DA)", dataset="RE2-TT", che_do="(a)",
         ma_goc=["H13", "H14", "M4", "T-032:KT15"],
         hien_tuong="Một cột đứng yên ở đoạn học rồi đổi ở đoạn chấm; hồi quy theo nút cha cho phần dư học gần bằng không và điểm cực lớn (vượt ngưỡng báo riêng của Q-82); bước DA cộng điểm đó sang nút khác khi điểm vượt ngưỡng.",
         so="{{h13.huge}}/{{h13.n}} ca có nút điểm cực lớn. Trong {{h13.huge}} ca đó, số ca root hạng 1: bản có DA {{h13.da}}; bản có cạnh nhưng không DA {{h13.rht}}; bỏ mọi cạnh {{h13.k2}}, và còn {{h13.hugek2}} nút cực lớn. "
            "Ở {{h13.clean.n}} ca còn lại: bản có DA {{h13.clean.da}}; bản có cạnh nhưng không DA {{h13.clean.native}}; bỏ mọi cạnh {{h13.clean.k2}}.",
         vi_sao="Đã xác lập ở mức CT hai bước, trên cùng điểm đầu vào: (i) hồi quy theo nút cha tạo điểm cực lớn, và root đã không hạng 1 trước DA ở mọi ca của nhóm (hạng 1: {{h13.rht}}/{{h13.huge}} ca); (ii) DA nhận đúng các điểm đó và đổi hạng của root (trên {{h13.n}} ca: giảm {{h13.da.down}}, tăng {{h13.da.up}}, giữ {{h13.da.same}}). Bỏ mọi cạnh đổi cả hồi quy lẫn DA, không cô lập riêng bước nào. Chưa phân xử nguồn vật lý của tín hiệu và đóng góp của việc chờ.",
         muc="CT", muc_nguon_con=[("phép đổi K-2 bỏ cạnh (T-032, KQ10 mục 1)", "CT"), ("mô tả phần được cộng ở bước DA (KT15)", "ĐC")],
         loai_nguon="M", giai_thich_khac="Không đọc số CIRCA thành “cấu trúc gọi giúp” hay “hại” khi chưa tách {{h13.huge}} ca này. Minh đã chốt giữ bản gốc, không sửa (Q-82).",
         tac_gia="H13: không nêu. H14: nêu một phần (DA cần kiểm thêm trên dữ liệu thật).", rq="RQ1, RQ2, RQ3"),
    dict(id="G2-H13", ten="CIRCA: hồi quy theo nút cha làm điểm cao hơn bản không cạnh; nhạy với cửa sổ",
         phuong_phap="CIRCA (đồ thị kiến trúc, OLS+RHT+DA)", dataset="RE2-TT", che_do="(a)",
         ma_goc=["H15", "T-032:KT9"],
         hien_tuong="Phần dư ở đoạn học nhỏ mà phần dư ở đoạn chấm không nhỏ theo, nên điểm có cạnh cao hơn điểm không cạnh.",
         so="{{h15.raise}}/{{h15.reg}} nút có hồi quy tăng điểm. Nhóm {{h15.nodes}} nút có nhiều nút cha (nhóm `at_least8_parents`), trung vị tỷ số có cạnh/không cạnh: {{h15.n111:.2f}} (đoạn học ngắn gần mốc, `native111_late`), {{h15.l291:.2f}} (đoạn học dài, `long291_late`), "
            "{{h15.e111:.2f}} (đoạn ngắn sớm, `early111_late`), {{h15.s0:.2f}} / {{h15.s1:.2f}} / {{h15.s2:.2f}} (cùng số điểm như đoạn ngắn nhưng trải đều trên đoạn dài).",
         vi_sao="Đã xác lập phép tính và độ nhạy cửa sổ ở mức CT. Đã loại giải thích “chỉ do số điểm học ít”. Chưa phân xử giữa thành phần mẫu, độ gần đoạn chấm, pha lấy mẫu và thang phần dư.",
         muc="CT", muc_nguon_con=[("hai nhánh cửa sổ (T-032, KQ13 mục 6)", "CT"), ("giữ nút và cha, đổi cách lấy điểm học (gói bổ sung, KT9)", "CT")],
         loai_nguon="M + G", giai_thich_khac="Đổi đoạn học ngắn thành đoạn dài còn đổi phân phối; lấy mẫu trải đều còn đổi pha và tần suất. Không coi “tăng số điểm học” là lời giải đã chứng minh.",
         tac_gia="Có nêu dạng tổng quát.", rq="RQ2"),
    dict(id="G2-H14", ten="TORAI nguồn B: bảng log do ta dựng dồn điểm về vài dịch vụ",
         phuong_phap="TORAI (bản sửa), nguồn B tự dựng", dataset="RE2-TT", che_do="(a)",
         ma_goc=["H16", "T-032:KT7"],
         hien_tuong="Dòng log mang dữ liệu của từng yêu cầu bị tách thành nhiều mẫu hiếm; điểm z của log dồn về vài dịch vụ, không phụ thuộc root.",
         so="Bỏ nguồn log (seed 0): {{h16.fixed}}/{{h16.wrong}} ca sai thành hạng 1; {{h16.lose}} ca đúng bị hỏng.",
         vi_sao="Đã xác lập ở mức CT. Với bảng log của tác giả (nguồn A) hiện tượng không lặp lại.",
         muc="CT", muc_nguon_con=[("phép đổi tl1, tl2 (T-032, KQ10 mục 8)", "CT"), ("TORAI nguồn A, mọi cột đóng góp (gói bổ sung, KT7)", "ĐC")],
         loai_nguon="A", giai_thich_khac="Một ca có hạng root đổi theo seed. Nguồn A lệch lưới thời gian và dùng ngưỡng toàn file (WHY-29), nên không thay được nguồn B làm dòng chính mà không khai lệch.",
         tac_gia="Nêu một phần.", rq="RQ1"),
    dict(id="G2-H15", ten="TORAI: bước nhân quả (RCD) không quyết định vị trí root",
         phuong_phap="TORAI (bản sửa), nguồn B", dataset="RE2-TT", che_do="(a)",
         ma_goc=["H17"],
         hien_tuong="Root không bao giờ nằm trong khối do nhánh RCD xếp; vị trí của root do điểm cụm và nhánh dự phòng quyết định.",
         so="Trên {{h17.units}} đơn vị (ca × seed): root là cụm một dịch vụ ở {{h17.don}} đơn vị, rơi nhánh dự phòng ở {{h17.fallback}}, thuộc khối do RCD xếp ở {{h17.rcd}}.",
         vi_sao="Chưa phân xử vai trò của đồ thị nhân quả: trên bản ghi, bước đó không tham gia xếp root, nên không rút được kết luận nào về đồ thị nhân quả từ TORAI.",
         muc="MT", muc_nguon_con=[("phân rã khối trên các bản ghi đóng băng (T-032, KQ9 mục 7)", "MT")],
         loai_nguon="A", giai_thich_khac="Đây là bản đã sửa hai chỗ theo WHY-19 (lần giảm mẫu thứ hai đã bỏ), nên hiện tượng không do lỗi giảm mẫu đó. Kết luận chỉ về bước RCD; khâu dựng bảng trace của nguồn B có dùng quan hệ cha–con của span. "
                                           "Chưa kiểm bản tác giả đã dùng để tạo số công bố.",
         tac_gia="Không nêu.", rq="RQ1, RQ3"),
    dict(id="G2-H16", ten="Rào cản tập ứng viên, hòa cắt biên và ca dừng lỗi vì thao tác thiếu nền",
         phuong_phap="TraceRCA, MicroRank (bản RCAEval); SimpleRCA", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["M1", "M2", "M3", "D4", "T-032:KT8"],
         hien_tuong="Root nằm ngoài tập quan sát hoặc tập trả về; hòa cắt ngang biên top-k; một thao tác chỉ có sau mốc làm phương pháp dừng lỗi.",
         so="Ở TraceRCA trên Nezha-OB, trong {{t28.nz.tracerca.sai}} ca sai: M1 (root ngoài tập quan sát) {{t28.nz.tracerca.M1}} ca; M2 (root quan sát được nhưng không được trả về) {{t28.nz.tracerca.M2}} ca; "
            "M3 (hòa cắt biên) {{t28.nz.tracerca.M3}} ca. Các phương pháp khác: xem cột cờ ở Phụ lục A (cột chỉ hiện khi có ca mang cờ). ERROR: {{t28.re2.microrank_full.khongok}} ca RE2-TT ở MicroRank và {{t28.re2.tracerca.khongok}} ca ở TraceRCA, đang tính trượt. "
            "Bỏ thao tác thiếu nền (đổi đầu vào, chẩn đoán): TraceRCA xếp root hạng 1 ở {{d4.tracerca.hit1}}/{{t28.re2.tracerca.khongok}} ca đó.",
         vi_sao="Đã xác lập ở mức CT rằng bốn ca ERROR là do đầu vào thiếu nền của một thao tác, không phải do cách chấm điểm. Rào cản tập (M1–M3) được kiểm trực tiếp và hiếm.",
         muc="CT", muc_nguon_con=[("kiểm thành viên tập (T-028)", "ĐC"), ("phép bỏ thao tác thiếu nền (T-032, KQ12 mục 2, KQ13 mục 4)", "CT")],
         loai_nguon="D + G", giai_thich_khac="Cách ghi bốn ca ERROR là quyết định giao thức (WHY-28, WHY-31): giữ ở mẫu số, tính trượt. Đổi cách ghi làm đổi số hạng 1 của TraceRCA.",
         tac_gia="Chưa thấy trong nguồn đã khảo sát.", rq="RQ1"),
    dict(id="G2-H17", ten="Dịch vụ phía trên đứng trước root (cờ M5) và câu “lan có đáng kể”",
         phuong_phap="Cả sáu phương pháp", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["M5", "T-032:KT10"],
         hien_tuong="Ở một phần ca sai, có dịch vụ phía trên root (gọi root trực tiếp hoặc gián tiếp) chắc chắn đứng trước root.",
         so="Cờ M5 trên số ca sai hạng 1 (đa nhãn): TraceRCA {{t28.re2.tracerca.M5}}/{{t28.re2.tracerca.sai}} và {{t28.nz.tracerca.M5}}/{{t28.nz.tracerca.sai}}; MicroRank {{t28.re2.microrank_full.M5}}/{{t28.re2.microrank_full.sai}} và {{t28.nz.microrank_full.M5}}/{{t28.nz.microrank_full.sai}}; "
            "SimpleRCA {{t28.re2.simplerca.M5}}/{{t28.re2.simplerca.sai}} và {{t28.nz.simplerca.M5}}/{{t28.nz.simplerca.sai}}; BARO {{t28.re2.baro.M5}}/{{t28.re2.baro.sai}} và {{t28.nz.baro.M5}}/{{t28.nz.baro.sai}}; "
            "CIRCA {{t28.re2.circa_ols_da.M5}}/{{t28.re2.circa_ols_da.sai}}; TORAI B {{t28.re2.torai_B.M5}}/{{t28.re2.torai_B.sai}} (RE2-TT trước, Nezha-OB sau). "
            "Khả năng đo việc “dịch vụ gọi chờ root”: {{d.nz.ok}} ca Nezha-OB đo được có điều kiện, {{d.re2.part}} ca RE2-TT đo được một phần, {{d2.unmeasurable}} ca không đo được.",
         vi_sao="Chưa phân xử “lan có đáng kể”, vì cờ M5 không đồng nghĩa “sai vì dịch vụ gọi”, cơ chế khác nhau theo phương pháp, và chưa có định nghĩa “đáng kể” được chọn. Xem mục 4. Mức ĐC của dòng chỉ thuộc bảng theo ca đo việc chờ ở các đơn vị có cờ M5; nó không trả lời câu “đáng kể”.",
         muc="ĐC", muc_nguon_con=[("cờ M5 so mức nền P0 (T-028)", "LĐ"), ("bảng theo ca cho các đơn vị có cờ M5 (T-032 mục 5.3)", "ĐC"), ("mức đo được theo ca (T-032 mục 5.4)", "MT")],
         loai_nguon="M + D", giai_thich_khac="Dịch vụ gọi tự bất thường; tác động chung qua hạ tầng; cách chấm ưu tiên dịch vụ đông lưu lượng; giá trị cực lớn qua DA (CIRCA); sai lệch cửa sổ, đồng hồ hoặc đồ thị.",
         tac_gia="Bài TraceRCA có mô tả hiện tượng ở phần bài học triển khai.", rq="RQ2, RQ3"),
    dict(id="G2-H18", ten="Ca sai chưa gắn được cờ cơ chế nào (M0)",
         phuong_phap="BARO, MicroRank, CIRCA, TORAI B, TraceRCA, SimpleRCA", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["M0"],
         hien_tuong="Ca sai không có cờ M1–M6; đọc tay ở T-032 đã gắn phần lớn về các bước ở G2-H01 đến G2-H15, phần còn lại ghi là chưa rõ.",
         so="Nhãn chính M0 trên số ca sai hạng 1: MicroRank {{t28.re2.microrank_full.M0.primary}}/{{t28.re2.microrank_full.sai}} (RE2-TT); BARO {{t28.re2.baro.M0.primary}}/{{t28.re2.baro.sai}} và {{t28.nz.baro.M0.primary}}/{{t28.nz.baro.sai}}; "
            "CIRCA {{t28.re2.circa_ols_da.M0.primary}}/{{t28.re2.circa_ols_da.sai}}; TORAI B {{t28.re2.torai_B.M0.primary}}/{{t28.re2.torai_B.sai}}; SimpleRCA {{t28.nz.simplerca.M0.primary}}/{{t28.nz.simplerca.sai}} (Nezha-OB).",
         vi_sao="Chưa phân xử ở mức nhóm: M0 là nhãn “chưa phân loại” của codebook T-028, không phải một cơ chế.",
         muc="MT", muc_nguon_con=[("bảng nhãn chính T-028", "MT"), ("đọc tay các đơn vị sai (T-032, doc-tay.md)", "MT")],
         loai_nguon="chưa xếp", giai_thich_khac="Nhãn chính theo thứ tự cố định M1 → M6 → M0 chỉ để trình bày, không phải nguyên nhân trội.",
         tac_gia="Không áp dụng.", rq="RQ2"),
    dict(id="G2-H19", ten="Giới hạn của dữ liệu trace và metric",
         phuong_phap="Mọi phương pháp dùng trace; CIRCA và TORAI ở Nezha-OB", dataset="RE2-TT, Nezha-OB", che_do="(a)",
         ma_goc=["D1", "D2", "D3", "D5", "D6", "D7"],
         hien_tuong="Nền trace ngắn và metric thưa ở Nezha-OB (D1); root không được dịch vụ nào gọi hoặc quá ít lời gọi (D2); cửa sổ dev của RE2-TT không có span mang mã lỗi (D3); một ca RE2-TT mất nhiều span cha (D5); "
                    "RE2-TT không công bố phiên bản mã, công cụ ghi span, quan hệ dịch vụ–máy (D6); trace của Nezha-OB không có trường trạng thái và metric có nhịp thưa (D7).",
         so="Nezha-OB: {{d.nz.n}}/{{d.nz.n}} ca có nền trace ngắn và chỉ vài mẫu metric mỗi phía (mã D1 của T-032); CIRCA và TORAI B không chạy được ở {{t28.nz.circa_ols_da.khongok}}/{{t28.nz.circa_ols_da.n}} ca. "
            "{{d2.unmeasurable}}/{{d2.n}} ca không đủ lời gọi tới root: {{d2.nocaller}} ca root không được dịch vụ nào gọi trong trace, {{d2.fewcalls}} ca cạnh gọi tới root quá thưa. RE2-TT: {{d.re2.part}} ca chỉ đo được một phần vì thiếu thông tin công cụ ghi span. "
            "D5: ở ca `dev-746fd74313`, {{d5.orphan}}/{{d5.n}} trace sau mốc có span mất cha; ca này không qua cổng kiểm cây lời gọi (trường `gate/pass`: {{d5.gate}}), nên công thức chia trace của bài MicroRank không áp được ở đó.",
         vi_sao="Đã xác lập ở mức ĐC (đo trực tiếp trên dữ liệu) rằng các thông tin này không có trong dataset; bộ thu thập không khôi phục được thứ chưa từng được ghi.",
         muc="ĐC", muc_nguon_con=[("thẻ dataset và phép đo độ phủ (T-032 mục 3.7, 5.4)", "ĐC")],
         loai_nguon="D", giai_thich_khac="Không áp dụng: đây là thiếu đầu vào, không phải cơ chế của phương pháp.",
         tac_gia="Tác giả dataset không nêu các giới hạn này trong nguồn đã khảo sát.", rq="RQ1, RQ2, RQ5",
         ly_do_khong_tach_o="giới hạn áp cho cả dataset hoặc theo ca đã đếm; bảng theo ca ở `results/T-032/kha-nang-do-trace.json#/ca`"),
    dict(id="G2-H20", ten="BOCPD: tiền xử lý trên cả bản ghi làm vị trí báo đầu phụ thuộc dữ liệu sau mốc",
         phuong_phap="BOCPD (bản BARO)", dataset="RE2-TT", che_do="(b)",
         ma_goc=["HP-6", "T-033:K4"],
         hien_tuong="Bước bỏ cột hằng và chuẩn hóa min–max dùng cả bản ghi, gồm dữ liệu sau mốc.",
         so="Cắt dữ liệu sau mốc rồi tiền xử lý lại: báo động đầu sớm hơn ở {{hp.i1.earlier}}/{{hp.i1.n}} ca, bằng ở {{hp.i1.equal}}, muộn hơn ở {{hp.i1.later}}; tổng điểm đổi trước mốc {{hp.nv.full}} → {{hp.nv.i1}} (nhánh đổi hazard, I2: {{hp.nv.i2}}). "
            "Tiền xử lý chỉ dùng quá khứ (hai biến thể chẩn đoán): tập điểm đổi khác bản gốc ở {{k3.causal_fixed.changed}}/{{k3.causal_fixed.cases}} và {{k3.causal_expanding.changed}}/{{k3.causal_expanding.cases}} ca.",
         vi_sao="Đã xác lập ở mức CT rằng vị trí báo động đầu phụ thuộc dữ liệu sau mốc qua tiền xử lý. Chưa phân xử vì sao có báo động trước mốc; bỏ nhìn trước không cho thấy sẽ giảm báo sai.",
         muc="CT", muc_nguon_con=[("can thiệp I1, I2 (T-029)", "CT"), ("biến thể tiền xử lý chỉ dùng quá khứ (T-033 gói bổ sung, K4)", "CT")],
         loai_nguon="A + G", giai_thich_khac="Cắt sau mốc còn đổi bộ cột và số chiều của prior. Biến thể chỉ dùng quá khứ đổi cùng lúc mặt nạ cột, số chiều và thang; không cô lập riêng việc chuẩn hóa.",
         tac_gia="Code tiền xử lý toàn chuỗi là của tác giả; chưa thấy tác giả nêu hạn chế này.", rq="RQ1, RQ2, RQ3a"),
    dict(id="G2-H21", ten="BOCPD: có báo động trước mốc; nhạy với prior; underflow số học",
         phuong_phap="BOCPD (bản BARO)", dataset="RE2-TT", che_do="(b)",
         ma_goc=["HP-5", "HP-7", "HP-8", "HP-9", "T-033:K3"],
         hien_tuong="Báo động đầu nằm trước mốc tiêm ở phần lớn ca. Posterior nhạy với prior. Khối lượng của nhiều dòng dõi bị làm tròn về không.",
         so="Báo động đầu ở hoặc sau mốc: {{bl.det.bocpd.first_ok}}/{{bl.det.bocpd.n}} ca. Đổi prior trên cùng đầu vào: tập điểm đổi khác ở {{k3.prior_df4.changed}}/{{k3.prior_df4.cases}}, {{k3.prior_kappa4.changed}}/{{k3.prior_kappa4.cases}}, {{k3.prior_precision4.changed}}/{{k3.prior_precision4.cases}} ca "
            "(tổng điểm đổi {{k3.native.cp}} → {{k3.prior_df4.cp}}, {{k3.prior_kappa4.cp}}, {{k3.prior_precision4.cp}}). "
            "**Phép E2** (posterior trong miền log, bốn chuỗi của hai ca): MAP và điểm đổi trùng bản gốc ở {{e2.chains_equal}}/{{e2.chains}} chuỗi; ở chuỗi full của {{e2.diff.case:x}} MAP khác tại {{e2.diff.m}} điểm liên tiếp, "
            "bản gốc có {{e2.diff.cp_only_native}} điểm đổi mà phép tính trong miền log không có, và thiếu {{e2.diff.cp_only_log}} điểm đổi mà phép tính trong miền log có; tất cả nằm trong {{e2.diff.window_s}} giây đầu sau mốc.",
         vi_sao="Chưa phân xử vì sao có báo động trước mốc: không có nền sạch và onset được xác nhận độc lập. Đã loại hazard trên miền được chấm (I2). Đã xác lập ở mức CT độ nhạy với prior. "
                "Đã xác lập ở mức CT rằng underflow làm đổi MAP và điểm đổi ở một trong bốn chuỗi đã kiểm, trong một đoạn ngắn sau mốc; đã loại underflow như giải thích cho các báo động trước mốc của hai ca đó.",
         muc="CT", muc_nguon_con=[("can thiệp I2 và cờ B1, B4, D0 (T-029)", "CT / LĐ"), ("ba mức prior trên cùng X, d (T-033, K3)", "CT"), ("phép E2 của T-034 (hai-phep-kiem.md)", "CT")],
         loai_nguon="M + A + D", giai_thich_khac="Nền không sạch; biến động tải; bước nhảy telemetry (cờ B4 cũng phổ biến ở điểm không báo); hiệp phương sai và prior. Số điểm đổi không phải thước đo chất lượng. HP-5: không ca nào có cờ “đầu chuỗi thiếu dữ liệu được điền không” ở báo động đầu; điều đó không bác ảnh hưởng của thiếu dữ liệu nói chung. "
                                                   "HP-9 (D0): ca không có cờ chính nào; thuộc nhóm chưa giải thích, không ép vào một cơ chế.",
         tac_gia="Chưa thấy trong nguồn đã khảo sát.", rq="RQ1, RQ2, RQ3a"),
    dict(id="G2-H22", ten="N-Sigma: báo dày ngay trên đoạn nền",
         phuong_phap="N-Sigma (cấu hình đã khóa của T-025)", dataset="RE2-TT", che_do="(b)",
         ma_goc=["HP-1", "HP-2", "HP-3", "HP-4", "HP-14", "T-033:K2"],
         hien_tuong="Báo động đầu luôn trước mốc; rất nhiều báo động trên giờ bình thường theo nhãn proxy.",
         so="Báo động đầu ở hoặc sau mốc: {{bl.det.nsigma.first_ok}}/{{bl.det.nsigma.n}} ca; {{bl.det.nsigma.fa:.0f}} báo động mỗi giờ bình thường theo nhãn proxy (bộ cột chính). "
            "Lịch sử trượt có độ dài cố định thay cho lịch sử mở rộng: báo động đầu sau mốc sớm hơn ở {{k2.roll.earlier}} ca, bằng {{k2.roll.equal}}, muộn hơn {{k2.roll.later}}.",
         vi_sao="Chưa phân xử nguyên nhân thống kê: các cờ (lịch sử ngắn, cột báo dày, độ lệch chuẩn bằng không, nền mở rộng nhận dữ liệu sau mốc) mới là liên hệ. Đã xác lập ở mức CT rằng độ dài lịch sử và phép OR nhiều cột đi vào kết quả. Mức CT của dòng chỉ thuộc phần này.",
         muc="CT", muc_nguon_con=[("cờ N1–N4, N6 và đọc tay (T-029)", "LĐ"), ("đối chiếu lịch sử trượt/mở rộng (T-033, K2)", "CT")],
         loai_nguon="M", giai_thich_khac="Đuôi không chuẩn; nền không dừng; nhiều cột cùng được xét (phép OR); lượng hóa của metric. Không có nền sạch độc lập để gọi một báo động là “sai trong vận hành”.",
         tac_gia="Bài BARO nêu baseline báo sai nhiều; chưa thấy cơ chế cụ thể.", rq="RQ1, RQ2, RQ3a"),
    dict(id="G2-H23", ten="Đầu vào bậc thang: nhiều hàng metric lặp lại",
         phuong_phap="BOCPD (bản BARO)", dataset="RE2-TT", che_do="(b)",
         ma_goc=["T-033:K4"],
         hien_tuong="Chuỗi đầu vào có nhiều vectơ lặp liên tiếp; số quan sát hiệu lực ít hơn số hàng.",
         so="Bỏ hàng lặp: tập điểm đổi khác bản gốc ở {{k3.compressed_row.changed}}/{{k3.compressed_row.cases}} ca (hazard theo hàng) và {{k3.compressed_calendar.changed}}/{{k3.compressed_calendar.cases}} ca (hazard theo thời gian); tổng điểm đổi {{k3.native.cp}} → {{k3.compressed_row.cp}} và {{k3.compressed_calendar.cp}}.",
         vi_sao="Đã xác lập ở mức CT rằng gói thay đổi “bỏ hàng lặp” làm đổi điểm đổi. Chưa phân xử riêng từng yếu tố: phép nén đổi cùng lúc số lần cập nhật, đơn vị run length và quy tắc CP.",
         muc="CT", muc_nguon_con=[("hai nhánh nén (T-033 gói bổ sung, K4)", "CT")],
         loai_nguon="D + M", giai_thich_khac="Không chứng minh lượng hóa của bộ thu thập là nguyên nhân, cũng không chứng minh nén là cách sửa. Tổng điểm đổi giảm ở phần lớn ô nhưng tăng ở ô route/mem ({{k3.cell.routemem.native}} → {{k3.cell.routemem.row}} và {{k3.cell.routemem.calendar}}); mỗi ô ba ca, không coi là mẫu hình.",
         tac_gia="Chưa thấy trong nguồn đã khảo sát.", rq="RQ2, RQ5"),
    dict(id="G2-H24", ten="Nhãn proxy, thời lượng lỗi và onset chưa được xác nhận độc lập",
         phuong_phap="Mọi phép chấm phát hiện", dataset="RE2-TT", che_do="(b)",
         ma_goc=["HP-12", "T-033:K1", "T-033:K5", "T-033:K7"],
         hien_tuong="Nhãn chỉ có mốc tiêm; không biết lúc lỗi bắt đầu có tác động, lúc hết, và đoạn trước mốc có sạch không.",
         so="Số ca BOCPD có điểm đổi trong D giây sau mốc: {{k7.d30}}, {{k7.d60}}, {{k7.d120}}, {{k7.d300}}, {{k7.d600}} trên {{bl.det.bocpd.n}} ca, với D lần lượt là các mức `30`, `60`, `120`, `300`, `600` giây. "
            "Log có ghi kết quả ở vị trí cụ thể: access log {{k5.http200}} dòng HTTP `200`, {{k5.http500}} dòng `500`, {{k5.http503}} dòng `503`; phản hồi backend {{k5.app1}} lần trạng thái `1` và {{k5.app0}} lần trạng thái `0`.",
         vi_sao="Chưa phân xử, vì dataset không cung cấp onset có tác động, lúc hết lỗi, đoạn khỏe được kiểm độc lập, sai số đồng hồ và phép nối đã xác minh giữa dòng log với từng lời gọi.",
         muc="MT", muc_nguon_con=[("đường độ nhạy theo D (T-033, K7)", "MT"), ("đọc toàn bộ thông điệp log ở vùng khóa (T-033, K1, K5)", "MT"), ("nguồn chưa xác nhận D (T-029, HP-12)", "CK")],
         loai_nguon="D", giai_thich_khac="Số dòng log không phải số yêu cầu hay số sự cố. HTTP `200` hay trạng thái `1` không chứng minh hệ khỏe; `500` hay `503` không tự cho onset.",
         tac_gia="RCAEval mô tả mốc tiêm và cách thu; chưa thấy thời lượng lỗi cho các ca này.", rq="RQ3a, RQ5",
         ly_do_khong_tach_o="đây là giới hạn chung của bộ dữ liệu. Không có nhãn thời điểm sự cố bắt đầu có tác động, nên không dựng tỷ lệ theo ô"),
    dict(id="G2-H25", ten="Schema metric đổi theo ca và liên hệ với root",
         phuong_phap="BARO, SimpleRCA, CIRCA, TORAI, BOCPD, N-Sigma", dataset="RE2-TT", che_do="(a), (b)",
         ma_goc=["HP-13"],
         hien_tuong="Tập cột metric khác nhau giữa các ca; sự có mặt của một số cột liên hệ với root.",
         so="Số cột bộ phát hiện nhận và số chiều sau tiền xử lý, theo từng ca trong từng ô: Phụ lục C. Bảng chéo cột × root ở `results/T-029/nhan-proxy-va-schema.json`.",
         vi_sao="Chưa phân xử ảnh hưởng của schema lên kết quả: bảng chéo trên dev không tách được schema với việc mất tín hiệu lỗi (WHY-27).",
         muc="LĐ", muc_nguon_con=[("bảng chéo schema × root (T-029, P2)", "LĐ")],
         loai_nguon="D", giai_thich_khac="Triển khai và thu thập khác nhau theo dịch vụ; root và loại lỗi chưa giao chéo đầy đủ trong dev.",
         tac_gia="Chưa thấy trong nguồn đã khảo sát.", rq="RQ1, RQ2"),
    dict(id="G2-H26", ten="Chế độ (b): thành công chung bị chặn ở báo động đầu; RCA phụ thuộc điểm chạy",
         phuong_phap="BARO, CIRCA, TORAI B ghép với BOCPD hoặc N-Sigma", dataset="RE2-TT", che_do="(b)",
         ma_goc=["HP-10", "HP-11"],
         hien_tuong="RCA chạy tại báo động đầu; báo động đầu sai thì ca trượt. Cùng một ranker cho kết quả khác nhau khi chạy tại mốc tiêm, tại báo động đầu sau mốc, và tại báo động đầu.",
         so="BARO ghép BOCPD, Hit@1 trên {{bl.det.bocpd.n}} ca: {{bl.g.baro_bocpd.a:.2f}} tại mốc tiêm, {{bl.g.baro_bocpd.tplus:.2f}} tại báo động đầu sau mốc, {{bl.g.baro_bocpd.that:.2f}} tại báo động đầu; "
            "TORAI B ghép BOCPD: {{bl.g.torai_bocpd.a:.2f}}, {{bl.g.torai_bocpd.tplus:.2f}}, {{bl.g.torai_bocpd.that:.2f}}. Thành công chung Hit@1 cao nhất: {{bl.b.baro_bocpd.joint1:.3f}} (BARO ghép BOCPD).",
         vi_sao="Đã xác lập ở mức CT rằng điểm chạy RCA làm đổi kết quả. Chưa phân xử từng đường tác động: đổi cửa sổ còn đổi nền, cột ứng viên và đồ thị của CIRCA.",
         muc="CT", muc_nguon_con=[("can thiệp I3 và bảng G (T-029)", "CT")],
         loai_nguon="G + M", giai_thich_khac="Báo động đầu sau mốc được chọn nhờ nhãn mốc, nên không phải cận trên của chất lượng RCA. Thứ tự báo động của các dịch vụ không phải bằng chứng nhân quả hay lan.",
         tac_gia="Bài BARO có nêu độ nhạy theo thời điểm.", rq="RQ1, RQ2"),
]
for _r in ROWS:
    _r["fact_ids"] = ids(" ".join(_r[k] for k in ("so", "hien_tuong", "vi_sao", "giai_thich_khac", "tac_gia")))

EXCLUDED = [
    dict(ma="T-032:KT14", ly_do="Câu về độ phủ đọc tay (các đơn vị sai đã đọc; các đơn vị không chạy được ghi theo lý do); là kiểm quy trình, không phải một hạn chế."),
    dict(ma="T-032:KT16", ly_do="Câu về kết quả trên test; thuộc đánh giá sau khóa thiết kế (G3), đưa vào mục 6 nhóm 3."),
    dict(ma="T-033:K6", ly_do="Phép thử khả thi của một phép tính dùng cạnh (không phải hạn chế của baseline); dùng làm căn cứ kỹ thuật ở mục 5."),
]
