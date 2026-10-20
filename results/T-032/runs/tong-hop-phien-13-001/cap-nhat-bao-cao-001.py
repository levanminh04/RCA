"""T-032 phiên 13: cập nhật chữ ở năm file đầu ra theo kết quả ket-qua-phien-13.md. Chạy một lần từ results/T-032.

Mỗi phép thay nêu tiền tố của dòng cần thay (phải khớp đúng một dòng) hoặc chuỗi cần thay (phải xuất hiện đúng một lần).
Bản trước khi sửa được chép vào runs/tong-hop-phien-13-001/ban-truoc/.
"""
import json
import shutil
from pathlib import Path

BASE = Path(".")
BACK = BASE / "runs/tong-hop-phien-13-001/ban-truoc"
BACK.mkdir(parents=True, exist_ok=False)
FILES = ("ket-qua-phien-12.md", "kiem-tiep.md", "nguyen-nhan-xep-hang.md", "doc-tay.md", "bao-phu-nhom.json")
for name in FILES:
    shutil.copy2(BASE / name, BACK / name)


class Doc:
    def __init__(self, name):
        self.path = BASE / name
        self.lines = self.path.read_text(encoding="utf-8").split("\n")

    def line(self, prefix, new):
        hits = [i for i, l in enumerate(self.lines) if l.startswith(prefix)]
        assert len(hits) == 1, (self.path.name, prefix, len(hits))
        self.lines[hits[0]] = new

    def after(self, prefix, new):
        hits = [i for i, l in enumerate(self.lines) if l.startswith(prefix)]
        assert len(hits) == 1, (self.path.name, prefix, len(hits))
        self.lines[hits[0]] = self.lines[hits[0]] + new

    def insert_after(self, prefix, new_lines):
        hits = [i for i, l in enumerate(self.lines) if l.startswith(prefix)]
        assert len(hits) == 1, (self.path.name, prefix, len(hits))
        self.lines[hits[0] + 1:hits[0] + 1] = new_lines

    def sub(self, old, new):
        text = "\n".join(self.lines)
        assert text.count(old) == 1, (self.path.name, old[:50], text.count(old))
        self.lines = text.replace(old, new).split("\n")

    def save(self):
        self.path.write_text("\n".join(self.lines), encoding="utf-8", newline="\n")


# ---------------- ket-qua-phien-12.md ----------------
d = Doc("ket-qua-phien-12.md")
d.insert_after("Người làm: Claude. Ba phép kiểm này", ["", "**Ghi thêm ở phiên 13.** Ba chỗ của file này đã được kết quả sau sửa hoặc bổ sung: câu về `frontend` ở cuối mục 1 (đã sửa tại chỗ); câu \"điểm nguồn là thay đổi thật\" của mục 3 (xem `ket-qua-phien-13.md` mục 6); mục 4 (KT-9 đã chạy ở phiên 13). Bảng các câu bị sửa: `ket-qua-phien-13.md` mục 8."])
d.line("**Quan sát thêm, chưa kiểm theo ca.**",
       "**Quan sát thêm, đã kiểm theo ca (sửa ở phiên 13).** Ở Nezha-OB, thực thể đứng đầu của phần còn lại gần như luôn là `frontend`, dịch vụ ở đầu mọi yêu cầu. Bản đầu của đoạn này viết rằng điều đó \"khớp với hạn chế H4, H7\"; câu đó **không được hỗ trợ ở phần lớn ca**. Kiểm theo tên thao tác (lệnh chỉ-đọc trên bản ghi của lượt này, `cases/Nezha-OB/*/mo15c1|mo1p50c1/ban-ghi-0.json → /ranking`): thao tác cao nhất của `frontend` là lời gọi tới root ở 3/14 ca (luật của bài) và 3/11 ca (luật của code). Bảng nối theo cây span (`ket-qua-phien-13.md` mục 5) cho cùng kết quả: \"gắn với root\" ở 3/14 và 3/11 ca, không tìm thêm ca gián tiếp nào; ở các ca còn lại, thao tác cao nhất của `frontend` là lời gọi tới dịch vụ khác và các trace tạo ra điểm của nó không chứa root, hoặc chỉ có dưới 5 span.")
d.line("**KT-9** (đổi cửa sổ train",
       "**KT-9** (đổi cửa sổ train và đoạn chấm của CIRCA). Ở phiên 12 không chạy; lý do tôi nêu lúc đó (ước 1–2 giờ máy; chưa có thiết kế) không đứng được: lượt CIRCA tương tự trên laptop đã đo là 595 và 407 giây. Minh duyệt chạy; phiên 13 đã chạy với thiết kế `thiet-ke-phep-doi-013.md` mục 5, hết 985 giây. Kết quả: `ket-qua-phien-13.md` mục 6.")
d.save()

# ---------------- kiem-tiep.md ----------------
d = Doc("kiem-tiep.md")
d.line("Người làm: Claude, phiên 12",
       "Người làm: Claude, phiên 12 (11/10/2026); cập nhật ở phiên 13 cùng ngày. Mỗi mục ghi: câu hỏi; đã thử gì và ra gì; các giải thích còn cạnh tranh; phép kiểm cụ thể; thứ giữ cố định; dự đoán phân biệt; phạm vi và chi phí; quyết định bị ảnh hưởng. Minh đã duyệt chạy (Q-141) và phiên 13 đã chạy: KT-1, KT-2, KT-8 (nửa TraceRCA), KT-9, KT-12, bảng nối của KT-3, và đọc tay nốt (KT-14). Kết quả ở `ket-qua-phien-13.md` (KQ13). Ở mỗi mục đã chạy, phần kết quả đặt ở đầu, chữ viết trước khi chạy giữ nguyên bên dưới để đối chiếu. Các mục chưa chạy: chi phí là ước lượng, chưa đo.")
d.line("| KT-1 |", "| KT-1 | Vì sao khoảng nửa trace sau mốc mang cờ dù không gắn với root | **Đã chạy ở phiên 13**; phần lớn là mức tự nhiên của luật chia | — | Tiêu chí \"trace bất thường\" ở P6 |")
d.line("| KT-2 |", "| KT-2 | Thao tác đông span có 2–9% span mang cờ: nền tự nhiên hay do sự cố | **Đã chạy ở phiên 13**; cả hai, tách được theo vị trí so với root | — | Có cần hiệu chỉnh ngưỡng theo thao tác ở P6 |")
d.line("| KT-3 |", "| KT-3 | 25–26/47 ca MicroRank chưa hạng 1 sau khi thay bộ chia | **Đã chạy ở phiên 12 và 13**; phần còn lại chia được thành ba dạng | — | Có lấy kiểu xếp hạng của MicroRank làm ứng viên tầng 4 |")
d.line("| KT-8 |", "| KT-8 | Bốn ca ERROR: bỏ thao tác thiếu nền thì root xếp thứ mấy | **Đã chạy cả hai nửa** (phiên 12, 13) | — | Cách ghi 4 ca này ở bảng G2 |")
d.line("| KT-9 |", "| KT-9 | CIRCA: hồi quy làm tăng điểm là do cửa sổ hay do số nút cha | **Đã chạy ở phiên 13** (nhánh chẩn đoán); cửa sổ giải thích khoảng một nửa ở nút nhiều cha | — | Có dùng hồi quy theo cấu trúc ở P6 |")
d.line("| KT-12 |", "| KT-12 | Cột độ trễ của root phản ứng ở ca này, không ở ca kia cùng ô | **Đã chạy ở phiên 13**; ba cặp, ba lý do | — | Phân loại \"lỗi không hiện ở metric\" |")
d.line("| KT-14 |", "| KT-14 | Đọc tay đủ 192 đơn vị sai | **Đã làm ở phiên 13**: 144 đơn vị đọc, 48 ghi theo lý do | — | Mức chắc của phần đọc tay |")
d.line("| KT-15 |", "| KT-15 | DA có bất lợi cho dịch vụ không có cạnh không | **Đã chạy trong phiên 12**; cách đọc ban đầu bị sửa; KT-9 thêm một điều chỉnh | — | Thiết kế bước lan điểm ở P6 |")
d.insert_after("## KT-1. Vì sao khoảng một nửa trace", ["",
    "**Kết quả phiên 13 (KQ13 mục 1; `runs/fake-marker-001/summary.json`; `runs/tong-hop-phien-13-001/derived-013.json → /kt1`).** Tự kiểm với H_native và lượt `chain-spanpass-001` đạt 26/26.",
    "",
    "- Không có lỗi nào trong đoạn xét, luật chia vẫn xếp 36,6% trace là bất thường (trung vị 26 ca; từ 11% tới 43%); mốc thật cùng độ dài cửa sổ: 51,9%.",
    "- Ba mốc khai trước: (a) không đạt ở vế \"độc lập\" (1/26 ca), (b) không đạt (0/26), (c) không đạt (0/26 ca đổi theo vị trí mốc). Theo mốc: \"không phân xử rõ\". Mốc (a), (b) của tôi so hai tập trace khác loại; ghi rõ ở KQ13.",
    "- So cùng loại trace (tính sau khi xem kết quả): trace không có root 15,9% ở mốc giả so với 20,8% ở mốc thật, tỷ số theo ca trung vị 0,93; trace có root 46,7% so với 93,5%.",
    "- **Trả lời:** giải thích (a) được hỗ trợ về bản chất (trace không dính root bị xếp bất thường gần bằng tần suất lúc không có sự cố), trừ phần \"độc lập\"; (b) chỉ đóng phần nhỏ; (c) không được hỗ trợ.",
    "- **Còn mở:** Nezha-OB không kiểm được (nền quá ngắn).",
    "",
    "Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu. Lưu ý: dòng \"giữ cố định độ dài cửa sổ nền\" không làm được với mốc giả; thiết kế 013 đã thay bằng so mốc thật và mốc giả ở cùng độ dài cửa sổ."])
d.insert_after("## KT-2. Tỷ lệ cờ 2–9%", ["",
    "**Kết quả phiên 13 (KQ13 mục 2; `runs/fake-marker-001/summary.json → /summary/kt2`; `derived-013.json → /kt2`).**",
    "",
    "- 1.021 cặp (thao tác đông span, ca): a/n ở mốc giả có trung vị 1,0%, lớn nhất 8,1%; từ 2% trở lên ở 230 cặp. Hai mốc khai trước đều không đạt (230/1.021 và 492/1.021): \"không phân xử rõ\", hai giải thích cùng có mặt.",
    "- Tách theo vị trí so với root: thao tác phía trên root 0,8% → 6,2% (161/236 cặp tăng gấp từ 2 lần); thao tác không liên hệ 1,1% → 1,2%.",
    "- Chín cặp đã đọc ở TraceRCA: mốc giả trung vị 1,9%; 4/9 giữ mức tự nhiên, 5/9 tăng sau mốc thật (rõ nhất: đăng nhập của `ts-auth-service`, 0,9–1,9% lên 9–10%).",
    "- **Trả lời:** mức 1–4% ở thao tác đông span không liên hệ là mức tự nhiên của dữ liệu; sự cố làm tăng có chọn lọc theo chuỗi gọi phía trên root. Một số thao tác không liên hệ tăng thật: thuộc KT-6.",
    "",
    "Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu."])
d.line("- **Còn mở, kèm phép kiểm:** ở Nezha-OB, `frontend` đứng đầu",
       "- **Bảng nối theo cây span, chạy ở phiên 13 (KQ13 mục 5; `runs/microrank-merged-link-001/summary.json`).** Tập trace dựng lại trên EC2 trùng lượt laptop 47/47 ca ở cả hai luật. Ở Nezha-OB, `frontend` đứng đầu ở 14/16 và 11/14 ca còn sai; thao tác cao nhất của nó \"gắn với root\" chỉ ở **3/14 và 3/11** ca (trùng kết quả kiểm theo tên thao tác). Dự đoán \"cùng cơ chế với H4, H7\" **không đạt**. Phần còn lại của cả hai dataset chia ba dạng: thao tác cao nhất bao lời gọi chậm tới root (RE2-TT 5/8 và 3/6; Nezha-OB 5/16 và 5/14); nhóm trace bất thường mới không chứa root (RE2-TT 3 ca, `ts-auth-service` đứng đầu; Nezha-OB 4–6 ca); dưới 5 span (Nezha-OB 3–4 ca). Giải thích (b), (c) ở dưới chưa kiểm riêng; đọc tay 28 đơn vị nốt (`doc-tay.md` mục 8.4) không thấy dạng thứ tư.")
d.sub("- **Còn mở:** vì sao các thao tác đó có 2–4% span mang cờ; chính là KT-2, và ở Nezha-OB không kiểm được bằng mốc giả vì nền quá ngắn.",
      "- **Còn mở:** vì sao các thao tác đó có 2–4% span mang cờ ở Nezha-OB: không kiểm được bằng mốc giả vì nền quá ngắn. Ở RE2-TT, KT-2 (phiên 13) cho thấy mức 1–4% ở thao tác đông span không liên hệ là mức tự nhiên; đây là căn cứ gián tiếp, không phải phép đo trên Nezha-OB.")
d.sub("**Chưa làm:** nửa TraceRCA (EC2, khoảng 10 phút), chưa được duyệt.",
      "\n\n**Kết quả nửa TraceRCA, phiên 13 (KQ13 mục 4; `runs/tracerca-dropnew-001/summary.json`).** Tự kiểm: ở 48 ca nguồn OK không span nào bị bỏ và hạng mọi thực thể trùng bản đóng băng 48/48. Bốn ca lỗi sau khi bỏ cùng số span như nửa MicroRank: root hạng **2, 1, 1, 1**. Vậy với TraceRCA cách ghi có đổi con số: 3/4 ca đang tính trượt sẽ là hạng 1. Quyết định còn lại cho Minh: ghi ở bảng G2 thế nào (báo cáo chính mục 11).")
d.insert_after("## KT-9. CIRCA: hồi quy theo nút cha", ["",
    "**Kết quả phiên 13 (KQ13 mục 6; `runs/circa-kt9-001/collect-001/summary.json`).** Nhánh chẩn đoán; cửa sổ đã khóa và số đã chấm không đổi. Nhánh giữ nguyên khớp bản đóng băng từng bit 30/30.",
    "",
    "- Trung vị tỷ số điểm (có cạnh / không cạnh) ở nút từ 8 cha: 7,54 (native) → 3,40 (học 291 điểm) và 3,64 (chấm 10 điểm ngay sau mốc). Tỷ lệ nút tăng: 72,6% → 67,3% và 73,1%.",
    "- Mốc khai trước cần cả hai vế; vế tỷ số đạt ở cả hai nhánh, vế tỷ lệ nút tăng không đạt ở nhánh nào. **Cả (a) và (b) không đạt theo mốc.** Đọc: hai lựa chọn cửa sổ giải thích khoảng một nửa mức phóng đại ở nút nhiều cha; việc hồi quy làm tăng điểm ở đa số nút còn nguyên.",
    "- Ghi thêm: học trên 291 điểm chỉ bỏ được giá trị cực lớn ở 2/11 ca; ba ca root `ts-auth-service` có hạng sau DA 15 → 1, 22 → 6, 46 → 37.",
    "- **Còn mở:** phần tăng còn lại, có ở mọi cấu hình cửa sổ và tăng theo số nút cha; chưa có phép đổi riêng.",
    "",
    "Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu. Lý do \"1–2 giờ máy\" nêu ở dưới là ước sai; lượt thật hết 985 giây."])
d.insert_after("## KT-12. Cột độ trễ của root phản ứng", ["",
    "**Kết quả phiên 13 (KQ13 mục 3; `runs/root-latency-001/summary.json`).** Bảy ca, bản ghi khớp bản đóng băng BARO từng bit 7/7.",
    "",
    "- auth, delay: cột latency của root tăng ở cả ba ca (trung vị gấp 3,9; 1,8; 2,3 lần); z khác nhau (30,7; 4,9; 2,4) vì IQR nền khác nhau 10–23 lần. Không giải thích nào trong ba giải thích khai trước mô tả đúng.",
    "- recommendationservice, network_delay: lời gọi tới root chậm 97–98% ở cả hai ca, 0% nằm trong span của root; cột độ trễ của root không ghi được sự cố ở cả hai; z = 64 đến từ một mẫu P99. Mốc (a) đạt; phần \"vì sao có mẫu đó\" để mở.",
    "- checkoutservice, network_delay: mốc (c) đạt theo chữ (26% so với 9%), nhưng chuỗi cho thấy không ca nào phản ứng; z = 94 là do IQR của 5 mẫu nền bằng 0,005.",
    "- **Trả lời cho quyết định phụ thuộc:** các ca này thuộc \"cách chuẩn hóa theo nền\" (cặp 1, 3) và \"cột đo ở phía được gọi\" (cặp 2), không thuộc \"cường độ lỗi khác nhau\".",
    "",
    "Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu."])
d.insert_after("## KT-14. Đọc tay đủ 192 đơn vị sai", ["",
    "**Đã làm ở phiên 13 (`doc-tay.md` mục 8; KQ13 mục 7).** Đọc nốt 68 đơn vị OK xếp sai; 48 đơn vị không chạy được ghi theo lý do sau khi soát dòng lý do của cả 48 phiếu. Tổng: 144 đơn vị sai hoặc không OK đã đọc, 24 đối chứng. Không thấy đường thất bại mới; có sáu điều chỉnh so với phần đọc của phiên 12 (KQ13 mục 7). Chữ dưới đây là mục viết trước khi làm."])
d.sub("- **Còn mở:** vì sao cột độ trễ của `ts-preserve-service` có điểm cao ở các ca root là `ts-auth-service`; thuộc KT-6 (không phân xử được bằng dữ liệu hiện có).",
      "- **Còn mở, đã thu hẹp ở phiên 13:** vì sao cột độ trễ của `ts-preserve-service` có điểm cao ở các ca root là `ts-auth-service`. KT-9 cho thấy điểm đó phụ thuộc độ dài đoạn học: học trên 291 điểm thay cho 111 thì hạng root sau DA ở ba ca là 1, 6, 37 (thay cho 15, 22, 46). Vậy câu \"điểm nguồn là thay đổi thật\" ở trên viết quá tay; đúng hơn: điểm đó lớn dưới đoạn học 111 điểm. Phần còn lại thuộc KT-6.")
d.save()

# ---------------- nguyen-nhan-xep-hang.md ----------------
d = Doc("nguyen-nhan-xep-hang.md")
d.line("Người làm: Claude. Bản tổng hợp phiên 12",
       "Người làm: Claude. Bản tổng hợp phiên 12, ngày 11/10/2026; cập nhật cùng ngày sau ba phép kiểm chạy trên laptop (KQ12) và, ở phiên 13, sau sáu phép kiểm còn lại cùng phần đọc tay nốt (`ket-qua-phien-13.md`, viết tắt KQ13). Trạng thái: chờ phản biện. Bản này thay bản \"kết quả nghiên cứu ban đầu\" (lưu ở `runs/tong-hop-phien-12-001/ban-truoc/`); bản trước lượt cập nhật phiên 13 lưu ở `runs/tong-hop-phien-13-001/ban-truoc/`.")
d.insert_after("6. **Việc \"dịch vụ gọi chờ root\" chỉ đo được chắc", [
    "7. **Bổ sung ở phiên 13, từ phép thử mốc giả (không có lỗi trong đoạn xét):** luật chia trace của bản thư viện xếp 37% trace là bất thường ngay cả khi không có sự cố; còn sự cố thì làm tăng tỷ lệ span mang cờ **có chọn lọc ở thao tác phía trên root** (0,8% lên 6,2%) trong khi thao tác không liên hệ gần như không đổi (1,1% lên 1,2%). Điều thứ nhất củng cố điểm 2; điều thứ hai là bằng chứng mô tả, có đối chứng, rằng dịch vụ gọi dài ra theo root (KQ13 mục 1, 2)."])
d.sub("và `ket-qua-phien-12.md` (KQ12) cho ba phép kiểm chạy sau; mỗi số ở ba file đầu",
      "`ket-qua-phien-12.md` (KQ12) cho ba phép kiểm chạy sau, và `ket-qua-phien-13.md` (KQ13) cho sáu phép kiểm còn lại; mỗi số ở ba file đầu")
d.sub("root tăng hạng ở 19–20/25 và 13–15/22 ca; số ca hạng 1 từ 2/47 lên 21–22; 176–177/243 cặp mất. KQ11 mục 4.2 |",
      "root tăng hạng ở 19–20/25 và 13–15/22 ca; số ca hạng 1 từ 2/47 lên 21–22; 176–177/243 cặp mất. KQ11 mục 4.2. Phép thử mốc giả: không có lỗi nào vẫn có 36,6% trace bị xếp bất thường (trung vị 26 ca RE2-TT); trace không có root bị xếp bất thường ở 15,9% (mốc giả) so với 20,8% (mốc thật). KQ13 mục 1 |")
d.sub("Nhưng tỷ lệ làm 10–11/21 ca đang đúng của RE2-TT mất hạng 1. KQ11 mục 8 |",
      "Nhưng tỷ lệ làm 10–11/21 ca đang đúng của RE2-TT mất hạng 1. KQ11 mục 8. Mức cờ tự nhiên của thao tác đông span (mốc giả): trung vị 1,0%, tới 8,1%; sự cố chỉ làm tăng rõ ở thao tác phía trên root. KQ13 mục 2 |")
d.sub("| 3.285/4.526 nút; tỷ số tăng theo số nút cha. KQ10 mục 1.4 | Xác nhận tính toán; chưa tách phần do cửa sổ |",
      "| 3.285/4.526 nút; tỷ số tăng theo số nút cha. KQ10 mục 1.4. Nhánh chẩn đoán đổi cửa sổ: trung vị tỷ số ở nút từ 8 cha 7,54 → 3,40 (học 291 điểm) và 3,64 (chấm ngay sau mốc); tỷ lệ nút tăng 72,6% → 67,3% và 73,1%. KQ13 mục 6 | Xác nhận tính toán; cửa sổ giải thích khoảng một nửa ở nút nhiều cha, phần còn lại chưa tách |")
d.sub("vì điểm lớn (2.027,36) của một nút thuộc dịch vụ không liên quan được cộng nguyên cho 13 thực thể khác (`doc-tay.md` mục 5.2, 5.3; `kiem-tiep.md` mục KT-15).",
      "vì điểm lớn (2.027,36) của một nút thuộc dịch vụ không liên quan được cộng nguyên cho 13 thực thể khác (`doc-tay.md` mục 5.2, 5.3; `kiem-tiep.md` mục KT-15). Điểm lớn đó phụ thuộc độ dài đoạn học: trong nhánh chẩn đoán học trên 291 điểm, root của chính ca này về hạng 1 (KQ13 mục 6).")
d.sub("| 4 ca RE2-TT | MicroRank và TraceRCA dừng lỗi; hiện tính là trượt |",
      "| 4 ca RE2-TT | MicroRank và TraceRCA dừng lỗi; hiện tính là trượt. Bỏ thao tác đó thì root hạng 2, 2, 3, 12 (MicroRank) và 2, 1, 1, 1 (TraceRCA). KQ12 mục 2; KQ13 mục 4 |")
d.sub("tức ở hạng 1 cách ghi nào cũng cho 0/4, ở 5 hạng đầu thì 3/4 ca đang bị tính trượt.",
      "tức ở hạng 1 cách ghi nào cũng cho 0/4, ở 5 hạng đầu thì 3/4 ca đang bị tính trượt. Dữ kiện mới cho TraceRCA (KQ13 mục 4): root hạng 2, 1, 1, 1; tức với TraceRCA cách ghi **có đổi số ở hạng 1** (21/26 ca chạy được hiện nay; nếu coi là lỗi đầu vào và bỏ thao tác đó thì 24/30).")
d.sub("Còn 20–24/47 ca **chưa có giải thích**; ở Nezha-OB thực thể đứng đầu của phần này là `frontend` ở 14/16 và 11/14 ca, khớp với H4, H7 nhưng chưa kiểm theo ca (`kiem-tiep.md` mục KT-3). Đọc tay cho bốn dạng trong phần này (`doc-tay.md` mục 2.6), gồm ba phản ví dụ mà bộ chia mới làm root kém đi.",
      "Còn 20–24/47 ca. Ở Nezha-OB thực thể đứng đầu của phần này là `frontend` ở 14/16 và 11/14 ca; bản trước viết điều đó \"khớp với H4, H7\", nay đã kiểm và **không đúng cho phần lớn ca**: thao tác cao nhất của `frontend` là lời gọi tới root ở 3/14 và 3/11 ca theo tên thao tác, và bảng nối theo cây span cho cùng con số (KQ13 mục 5). Phần còn lại của hai dataset chia được thành ba dạng: (i) thao tác cao nhất của thực thể đứng đầu bao lời gọi chậm tới root, tức đúng H4, H7 (RE2-TT 5/8 và 3/6 ca còn sai; Nezha-OB 5/16 và 5/14); (ii) nhóm trace bất thường mới không chứa root (RE2-TT 3 ca với `ts-auth-service` đứng đầu, một dịch vụ không liên hệ chậm lên thật sau mốc; Nezha-OB 4–6 ca); (iii) dưới 5 span tạo ra điểm (Nezha-OB 3–4 ca). Đọc tay đủ 48 đơn vị MicroRank sai (`doc-tay.md` mục 2.6, 8.4) không thấy dạng thứ tư; có ba phản ví dụ mà bộ chia mới làm root kém đi.")
d.sub("nguyên nhân vật lý **không phân xử được bằng dữ liệu hiện có** (KT-6).",
      "nguyên nhân vật lý **không phân xử được bằng dữ liệu hiện có** (KT-6). Phép kiểm chuỗi cột ở ba cặp ca cùng ô (KQ13 mục 3) thêm hai điều: ở auth, delay cột độ trễ của root tăng 1,8–3,9 lần ở cả ba ca, z khác nhau vì nền dao động khác nhau; ở Nezha-OB có ca mà z = 94 của chính root là do IQR tính trên 5 mẫu nền. Đọc nốt cũng cho hai phản ví dụ với cách phân loại \"thang gỡ được hay không\" (`doc-tay.md` mục 8.1).")
d.line("- **H15 (CIRCA, hồi quy làm tăng điểm).**",
       "- **H15 (CIRCA, hồi quy làm tăng điểm).** Đã tách một phần bằng nhánh chẩn đoán đổi cửa sổ (KQ13 mục 6; cửa sổ đã khóa và số đã chấm không đổi): học trên 291 điểm hoặc chấm ngay sau mốc đều giảm khoảng một nửa mức phóng đại ở nút từ 8 cha (7,54 xuống 3,40 và 3,64), nhưng hồi quy vẫn làm tăng điểm ở 67–73% nút và tỷ số vẫn tăng theo số nút cha. Hai mốc khai trước đều không đạt trọn. Phần còn lại chưa có phép đổi riêng.")
d.sub("nhưng chỉ 6–8/22 ca Nezha-OB (KQ12 mục 1); phần còn lại ở Nezha-OB chưa giải thích (KT-3). Chưa đủ căn cứ để chọn hay loại.",
      "nhưng chỉ 6–8/22 ca Nezha-OB (KQ12 mục 1). Phần còn lại nay đọc được (KQ13 mục 5): một phần là H4, H7 (cạnh gọi chạm tới), một phần là trace bất thường không chứa root hoặc quá ít trace (cạnh gọi không chạm tới). Chưa đủ căn cứ để chọn hay loại; điều rút ra chắc hơn là tiêu chí chia trace phải theo cả yêu cầu, vì luật theo từng span xếp 37% trace là bất thường khi không có lỗi (KQ13 mục 1).")
d.sub("vì một thay đổi ở dịch vụ không liên quan sẽ kéo cả dãy nút cha vượt root (thấy ở ba ca không dính lỗi số học, `kiem-tiep.md` mục KT-15).",
      "vì một điểm lớn ở dịch vụ không liên quan sẽ kéo cả dãy nút cha vượt root (thấy ở ba ca không dính lỗi số học, `kiem-tiep.md` mục KT-15; điểm lớn đó phụ thuộc độ dài đoạn học, KQ13 mục 6).")
d.insert_after("**Hai điều thuận:** với TraceRCA", ["",
    "**Thêm ở phiên 13, một thuận và một bất lợi.** Thuận: dưới mốc giả và mốc thật cùng độ dài cửa sổ, tỷ lệ span mang cờ của thao tác phía trên root tăng từ 0,8% lên 6,2% trong khi thao tác không liên hệ giữ 1,1–1,2% (KQ13 mục 2); và với TraceRCA, thời gian chờ hiện ở cả dịch vụ gọi trực tiếp lẫn dịch vụ gọi nó với cùng số span (`doc-tay.md` mục 8.3 điểm 8), tức muốn gắn về đúng dịch vụ được gọi phải đi theo từng cạnh. Bất lợi: ở phần MicroRank còn sai sau hai phép đổi, chỉ 8–10 trên 20–24 ca có thực thể đứng đầu gắn với root qua lời gọi; phần còn lại nằm ngoài tầm của cạnh gọi tới root (KQ13 mục 5)."])
d.line("- **Chưa chạy, rẻ, dữ liệu có sẵn:**", "- **Chưa chạy, rẻ, dữ liệu có sẵn:** TORAI với bảng của tác giả (KT-7, 15 phút; không ảnh hưởng P5–P6).")
d.line("- **Đã chạy sau bản đầu của báo cáo",
       "- **Đã chạy sau bản đầu của báo cáo (Minh duyệt; KQ12 và KQ13):** phần còn lại của MicroRank (KT-3 và bảng nối; chia được ba dạng); bước DA của CIRCA (KT-15; sửa một cách đọc sai của tôi); bốn ca lỗi, cả hai nửa (KT-8); mốc giả cho trace và thao tác (KT-1, KT-2); chuỗi cột độ trễ của root (KT-12); cửa sổ của CIRCA (KT-9). Phần còn mở sau các phép này: Nezha-OB không làm được mốc giả; phần tăng điểm còn lại của hồi quy; vì sao một mẫu P99 nhảy ở một ca trễ mạng.")
d.line("- **Thiếu dữ kiện hoặc phải đổi điều đã khóa:**", "- **Thiếu dữ kiện:** mã của tác giả TraceRCA (KT-11; phải dựng định dạng dữ liệu riêng, 0,5–1 phiên).")
d.sub("- **Không phân xử được bằng dữ liệu hiện có:** vì sao metric của dịch vụ không liên hệ đổi tại mốc (KT-6);",
      "- **Không phân xử được bằng dữ liệu hiện có:** vì sao metric và thời lượng span của dịch vụ không liên hệ đổi tại mốc (KT-6; ví dụ mới: đăng nhập của `ts-auth-service` ở các ca order, loss);")
d.line("- **Mức đọc tay:**", "- **Mức đọc tay:** đã đọc 144/192 đơn vị sai hoặc không OK; 48 đơn vị không chạy được ghi theo lý do (KT-14; `doc-tay.md` mục 8).")
d.sub("Ghi đúng số còn lại (25–26/47 ca sau khi thay bộ chia; 20–24/47 ca sau khi ghép thêm đếm riêng), không ép nguyên nhân |",
      "Ghi đúng số còn lại (25–26/47 ca sau khi thay bộ chia; 20–24/47 ca sau khi ghép thêm đếm riêng); phần còn lại đã chia được ba dạng (KQ13 mục 5), không ép một nguyên nhân chung |")
d.sub("| CIRCA: giá trị cực lớn; không tách được ảnh hưởng của cửa sổ |", "| CIRCA: giá trị cực lớn; ảnh hưởng của cửa sổ chỉ tách được một phần, trong nhánh chẩn đoán (KQ13 mục 6) |")
d.sub("| Đạt ở mức đã duyệt | Bảng phủ 372/372; đọc tay 52/52 nhóm, 100 đơn vị; 82/82 đơn vị M5. Đọc tay chưa phủ mọi đơn vị sai (KT-14) |",
      "| Đạt | Bảng phủ 372/372; đọc tay 52/52 nhóm, 168 đơn vị (144 sai hoặc không OK, 24 đối chứng); 48 đơn vị không chạy được ghi theo lý do; 82/82 đơn vị M5 |")
d.sub("| 6. Nhật ký và bàn giao | Đạt | LOG phiên 12 |", "| 6. Nhật ký và bàn giao | Đạt | LOG phiên 12, 13 |")
d.line("1. **Chấp nhận mức đọc tay hiện tại", "1. **Mức đọc tay:** đã đọc hết theo lời duyệt của Minh (Q-141); không còn gì để quyết.")
d.line("2. **Có chạy các phép kiểm còn lại trước G2 không:**",
       "2. **Các phép kiểm còn lại:** đã chạy hết các phép Minh duyệt (KQ13). Còn hai phép chưa chạy, cả hai tôi đề nghị không chạy trước G2: KT-7 (không ảnh hưởng P5–P6) và KT-11 (0,5–1 phiên; chỉ nâng mức chắc của câu \"phương án có sẵn trong tài liệu không đủ\").")
d.line("3. **Cách ghi bốn ca lỗi và số độ nhạy của MicroRank ở bảng G2**",
       "3. **Cách ghi bốn ca lỗi và số độ nhạy ở bảng G2** (mục 4). Dữ kiện mới: với TraceRCA, 3/4 ca lỗi sẽ là hạng 1 nếu bỏ thao tác thiếu nền. Giữ số chính như đã khóa và thêm một dòng độ nhạy thì ưu điểm trước giảng viên là không phải sửa giao thức mà vẫn cho thấy đã tách lỗi đầu vào khỏi lỗi phương pháp; nhược điểm là thêm một con số được nghĩ ra sau khi xem dev.")
d.save()

# ---------------- doc-tay.md ----------------
d = Doc("doc-tay.md")
d.line("Người làm: Claude, phiên 12 (11/10/2026). File này ghi phần đọc tay",
       "Người làm: Claude, phiên 12 (11/10/2026); mục 8 thêm ở phiên 13 cùng ngày. File này ghi phần đọc tay của bước 4 trong SPEC. Nó đi kèm bảng tự động `doi-chieu-dung-sai.json`; bảng đó phủ đủ 372 đơn vị. Mục 1–7 phủ các đơn vị được chọn theo đường đi (phiên 12); mục 8 đọc nốt mọi đơn vị sai còn lại. Vài câu ở mục 1–6 đã bị kết quả phiên 13 sửa; chỗ đó có ghi chú \"Phiên 13:\" ngay tại câu.")
d.after("- **Số lượng.** 100 đơn vị đọc không trùng", " **Sau phiên 13:** thêm 68 đơn vị sai (mục 8), tổng 168 đơn vị đọc không trùng (144 sai hoặc không OK, 24 đối chứng); 48 đơn vị không chạy được ghi theo lý do.")
d.after("- **Đọc:** T-D không gỡ được cặp này dù 98% span mang cờ là span chờ root.", " **Phiên 13:** cách hiểu này không được hỗ trợ khi mở bảng theo cạnh: ở cặp này 106/128 lời gọi chậm (83%) nằm trong span của root; xem mục 8.3 điểm 10.")
d.after("- **Chưa phân xử:** vì sao thao tác của dịch vụ không liên hệ có 3–6% span vượt 3 lần độ lệch chuẩn.", " **Phiên 13 (KT-2):** số span mang cờ ở mốc giả → sau mốc thật, cùng độ dài cửa sổ: `ts-ticketinfo-service` 14/510 → 31/532; `ts-auth-service` 4/216 → 23/231; `ts-basic-service` 13/510 → 20/532. Tức mức tự nhiên của ba thao tác đã là 1,9–2,7%; hai thao tác tăng gấp từ 2 lần sau mốc, một thao tác tăng 1,5 lần. Cả hai giải thích cùng có mặt (`ket-qua-phien-13.md` mục 2).")
d.after("1. **Root gần như không có tín hiệu metric — `dev-57546fd87b`", " **Phiên 13 (KT-12):** câu \"không làm cột metric nào của root đổi đáng kể\" chỉ đúng theo thang z. Cột latency của root ở ca này có trung vị 0,69 → 1,60; z nhỏ vì IQR nền 0,54 (`ket-qua-phien-13.md` mục 3).")
d.after("   - **Đối chứng cùng ô (k = 5):** `dev-746fd74313` (auth|delay), root hạng 3; ở ca này cột latency của root có z = 30,7", " **Phiên 13 (KT-12) đã phân xử một phần:** cột tăng ở cả hai ca; khác nhau là độ dao động của nền (IQR 0,023 so với 0,537).")
d.after("   - **Đối chứng cùng ô (k = 5):** `dev-5467884de4` (hạng 4), nơi cột độ trễ phía server của root có z = 64.", " **Phiên 13 (KT-12):** z = 64 đến từ một mẫu P99 trong 5 mẫu; trung vị các cột độ trễ của root giảm sau mốc ở cả hai ca.")
d.after("   - **`dev-607751ac0a` (checkoutservice|network_delay), hạng [9, 10].**", " **Phiên 13 (KT-12):** về cột độ trễ của root thì không ca nào trong hai ca phản ứng; z = 94 ở `dev-2bfc97b01e` là do IQR của 5 mẫu nền.")
d.after("  - **Đọc đúng, theo KT-15:**", " **Phiên 13 (KT-9):** điểm 2.027,36 đó có dưới đoạn học 111 điểm; trong nhánh chẩn đoán học trên 291 điểm, root của ca này về hạng 1 sau DA. Chữ \"thay đổi thật\" ở cuối đoạn này viết quá tay.")
d.line("- 100 đơn vị trên 372; mỗi đường đi đọc một đơn vị.", "- Phiên 12: 100 đơn vị trên 372, mỗi đường đi đọc một đơn vị. Phiên 13 đã đọc nốt 68 đơn vị sai còn lại ở mức phiếu gọn (mục 8); 48 đơn vị không chạy được ghi theo lý do. 156 đơn vị đúng ở hạng 1 không thuộc diện đọc.")
d.lines += ["",
    "### 8.8 Tổng hợp phần đọc nốt",
    "",
    "- **Không có đường thất bại mới** ở phương pháp nào so với mục 1–6. Điều này không chứng minh danh sách đường thất bại là đủ: phần đọc nốt dùng phiếu gọn, chỉ in 4–6 thực thể đầu trên root.",
    "- **Các điều chỉnh với phần đọc của phiên 12:** (1) BARO: tác dụng của B-2 không dùng được làm tiêu chí tách đường (ii) và (iii) (mục 8.1). (2) auth, delay: cột của root có đổi ở cả ba ca; khác nhau ở nền (8.1 điểm 6). (3) TraceRCA: chờ hiện ở hai tầng dịch vụ gọi với cùng số span (8.3 điểm 8); cách hiểu \"phần chậm ngoài span của root\" không được hỗ trợ (8.3 điểm 10). (4) MicroRank: bốn đơn vị Nezha-OB thuộc dạng \"root vắng trong nhóm trace bất thường\"; `ts-auth-service` lên đầu vì chậm lên thật và trace của nó không qua root (8.4). (5) CIRCA: ba ca root `ts-auth-service` không đồng nhất (8.5). (6) TORAI B: phép bỏ cột log nền không đổi cho hạng 1 ở một ca, hạng 6 ở ca cùng ô (8.6).",
    "- **Giới hạn riêng của mục 8:** đọc ở mức phiếu gọn; không chọn thêm đối chứng; đơn vị được so với đơn vị đại diện cùng đường đi, mà đường đi là chữ ký do tôi đặt.",
    ""]
d.save()

# ---------------- bao-phu-nhom.json: chỉ trường trạng thái đọc ----------------
p = BASE / "bao-phu-nhom.json"
b = json.loads(p.read_text(encoding="utf-8"))
todo = {u["unit_id"]: u for u in json.loads((BASE / "runs/tong-hop-phien-13-001/phieu-gon-chua-doc/danh-sach.json").read_text(encoding="utf-8"))["units"]}
n_read = n_reason = 0
for u in b["units"]:
    t = todo.get(u["unit_id"])
    if t is None:
        continue
    assert u["reading_status"] == "chỉ có trong bảng tự động (phiên 12)"
    if t["status"] == "OK":
        u["reading_status"] = "đã đọc tay ở mức phiếu gọn (phiên 13)"; n_read += 1
    else:
        u["reading_status"] = "không chạy được; ghi theo lý do sau khi soát phiếu (phiên 13)"; n_reason += 1
assert (n_read, n_reason) == (68, 48), (n_read, n_reason)
b["status"] = "CATALOG_LOCKED_READING_DONE_PHIEN_13"
b["reading_update_phien_13"] = {
    "at": "phiên 13, 11/10/2026", "authority": "Q-141", "n_units_read_compact": n_read, "n_units_recorded_by_reason": n_reason,
    "n_units_read_by_hand_total": 100 + n_read, "doc": "results/T-032/doc-tay.md mục 8",
    "sheets": "results/T-032/runs/tong-hop-phien-13-001/phieu-gon-chua-doc/",
    "note": "Chỉ đổi reading_status của 116 đơn vị, status và thêm khối này. Nhóm, đối chứng, mechanism_established không đổi."}
p.write_text(json.dumps(b, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print("xong", n_read, n_reason)
