# -*- coding: utf-8 -*-
"""T-063 thu3 — dựng prompt cho Codex kiểm lại phản hồi và sửa sau REVIEW-4: "Prompt chung" + khối "Kiểm lại phản hồi và sửa"
chép nguyên văn từ docs/review-prompt.md, chỉ thay phần "Thông tin lượt này" bằng thông tin trung tính (AGENTS mục 9). Không ghi đè.
Dùng: py -3 -B results/T-063/thu3/scripts/dung_prompt_kiem_lai_r7.py → results/T-063/codex/R5-brief.md"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path(__file__).resolve().parents[4]
RA = R / 'results/T-063/codex/R5-brief.md'
assert not RA.exists(), 'không ghi đè'
rp = (R / 'docs/review-prompt.md').read_text(encoding='utf-8')


def khoi(tieu_de):
    i = rp.index(tieu_de); j = rp.index('```text', i); k = rp.index('```', j + 7)
    return rp[j:k + 3]


chung = khoi('## Prompt chung')
a = chung.index('Thông tin lượt này:'); b = chung.index('Không sửa ngoài phạm vi trên')
TT = (
    "Thông tin lượt này:\n"
    "- Task hoặc đề xuất: T-063 (tasks/T-063-quan-sat-thu-dev-2/), phần thu bù 3; kiểm phản hồi và sửa sau REVIEW-4.\n"
    "- Công đoạn: người phản biện kiểm lại phản hồi và sửa.\n"
    "- Gói/cổng: chiến dịch M1-FlashTicket, mốc M3 (tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 4–7); giai đoạn 2 không có khối "
    "trọng tâm cổng riêng trong docs/review-prompt.md.\n"
    "- Người làm và người phản biện chính thức: người làm Claude (phiên B; phiên điều phối đáp thay theo quyền chiến dịch); "
    "người phản biện Codex (SPEC T-063).\n"
    "- Tài liệu gốc: tasks/T-063-quan-sat-thu-dev-2/SPEC.md, LOG.md (mục \"Điều phối 16:00Z\" và các mục sau); "
    "tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md; docs/DECISIONS.md mục 14/11 về thu bù 3.\n"
    "- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW-4.md (bảng \"Phản hồi của người làm\" ở cuối); "
    "các lượt cũ REVIEW.md, REVIEW-2.md, REVIEW-3.md.\n"
    "- Code và kết quả liên quan: results/T-063/thu3/manifest.json (bản cũ, giữ), results/T-063/thu3/manifest-2.json, "
    "results/T-063/manifest.json (bản cũ, giữ), results/T-063/manifest-2.json; script tạo: "
    "results/T-063/thu3/scripts/tao_manifest_thu3.py và tao_manifest_thu3_2.py, results/T-063/dong-goi/tao_manifest_t063.py và "
    "tao_manifest_t063_2.py; results/T-063/thu3/dieu-kien-xac-nhan-3.md.\n"
    "- Phạm vi ghi được Minh cho phép trong lượt này: một bản phản biện mới tasks/T-063-quan-sat-thu-dev-2/REVIEW-5.md theo "
    "tasks/_MAU/REVIEW.md (liệt kê thư mục trước; nếu REVIEW-5.md đã có thì lấy tên lượt kế tiếp); ngoài ra chỉ đọc.\n\n")
out = ("# T-063 thu3 — Prompt cho Codex kiểm lại phản hồi và sửa sau REVIEW-4\n\n"
       "Dựng bằng `results/T-063/thu3/scripts/dung_prompt_kiem_lai_r7.py` từ `docs/review-prompt.md` (Prompt chung + khối "
       "\"Kiểm lại phản hồi và sửa\", nguyên văn; chỉ điền \"Thông tin lượt này\"). Phiên điều phối phát lượt này theo duyệt của Minh.\n\n"
       + chung[:a] + TT + chung[b:] + "\n\n" + khoi('### Kiểm lại phản hồi và sửa') + "\n")
RA.write_text(out, encoding='utf-8')
print(RA, len(out))
