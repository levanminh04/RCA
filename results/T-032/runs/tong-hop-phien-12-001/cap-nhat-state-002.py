"""Cập nhật riêng dòng T-032 của docs/STATE.md sau ba phép kiểm laptop (phiên 12)."""
p = 'docs/STATE.md'
s = open(p, encoding='utf-8').read()
lines = s.split('\n')
idx = [i for i, l in enumerate(lines) if l.startswith('| T-032 |')]
assert len(idx) == 1
new = ("| T-032 | Lần theo nguyên nhân thất bại xếp hạng | P4 | Claude | Codex | Chờ phản biện (11/10, Claude, phiên 12). Phần tổng hợp đã xong: "
       "bảng theo ca phủ 372 đơn vị, đọc tay 52/52 nhóm (100 đơn vị), mức đo được theo ba mức (Nezha-OB 16 đo được; RE2-TT 21 một phần; 15 không), "
       "đủ các file đầu ra của SPEC, báo cáo chính `results/T-032/nguyen-nhan-xep-hang.md` theo năm đầu ra P4, `kiem-tiep.md` 16 mục. "
       "Sau đó Minh duyệt các phép kiểm chạy trên laptop: KT-3, KT-8 (nửa MicroRank), KT-15 đã chạy, kết quả ở `ket-qua-phien-12.md` và đã đưa vào báo cáo; "
       "KT-9 chưa chạy (ước 1–2 giờ, phải đổi cửa sổ đã khóa), chờ Minh quyết. Tự soát: 13/13 tự kiểm của bảng; 46 + 15 nhóm con số, 0 lệch. "
       "RQ2/G2 chưa đóng; 'lan có đáng kể' để tổng hợp G2 quyết. Chờ Minh: các điểm ở mục 11 của báo cáo; chữ DECISIONS/WHY cho lời duyệt và thiết kế 012; "
       "chuyển prompt cuối mục 'Kết thúc phiên 12' của LOG cho Codex. Không lượt nào đang chạy; EC2 để bật. Chưa commit. "
       "Quyết định: Q-130, Q-131, Q-133, Q-134, Q-135, Q-136 | `tasks/T-032-g2-nguyen-nhan-xep-hang/` |")
old = list(lines)
lines[idx[0]] = new
assert sum(1 for a, b in zip(old, lines) if a != b) == 1
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('STATE: chỉ dòng T-032 đổi')
