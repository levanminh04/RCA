# -*- coding: utf-8 -*-
"""T-063 thu3 — dựng prompt phản biện cho Codex: "Prompt chung" + khối "Soát kết quả" chép nguyên văn từ docs/review-prompt.md,
chỉ thay phần "Thông tin lượt này" bằng thông tin trung tính (AGENTS mục 9). Không ghi đè file đã có.
Dùng: py -3 -B results/T-063/thu3/scripts/dung_prompt_phan_bien.py → results/T-063/thu3/PROMPT-PHAN-BIEN.md"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path(__file__).resolve().parents[4]
RA = R / 'results/T-063/thu3/PROMPT-PHAN-BIEN.md'
assert not RA.exists(), 'không ghi đè'
rp = (R / 'docs/review-prompt.md').read_text(encoding='utf-8')


def khoi(tieu_de):
    i = rp.index(tieu_de); j = rp.index('```text', i); k = rp.index('```', j + 7)
    return rp[j:k + 3]


chung = khoi('## Prompt chung')
a = chung.index('Thông tin lượt này:'); b = chung.index('Không sửa ngoài phạm vi trên')
TT = (
    "Thông tin lượt này:\n"
    "- Task hoặc đề xuất: T-063 (tasks/T-063-quan-sat-thu-dev-2/), phần thu bù 3: ô lỗi cho H3 (POOL-EVENT) và H4 (CONSUMER-BOOK-SLOW-X3), "
    "ô đối chứng trên bản build mới (BINH-THUONG, EVENT-DB-LAT, BINH-THUONG-X3) và ô tùy chọn RECREATE-PAY; đầu ra ở results/T-063/thu3/.\n"
    "- Công đoạn: soát kết quả.\n"
    "- Gói/cổng: chiến dịch M1-FlashTicket, mốc M3 (tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 4–7); giai đoạn 2 không có khối "
    "trọng tâm cổng riêng trong docs/review-prompt.md.\n"
    "- Người làm và người phản biện chính thức: người làm Claude (phiên B); người phản biện Codex (SPEC T-063).\n"
    "- Tài liệu gốc: tasks/T-062-dem-chang-1-4/PHIEN-B-BRIEF.md; tasks/T-063-quan-sat-thu-dev-2/SPEC.md (gồm phần bổ sung), LOG.md "
    "(mục \"Phiên B\"); docs/DECISIONS.md mục 13/11 \"Bổ sung quyền điều phối…\", \"Chạy bộ điều phối đợt thu trên exp-obs\", "
    "14/11 \"Hook thử H3…\"; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md; results/T-063/bao-cao.md (mục 2, 7, \"Thu bù 3\"); "
    "results/T-063/o-dev-bo-sung.md (mục \"Thu bù 3\"); results/T-063/dong-bang.md (mục \"Bản 3\"); results/T-064/phien-c/YEU-CAU-O.md; "
    "repo FlashTicket D:/Project/flash-ticket-platform nhánh rca/quan-sat-log commit e557307 (cha fba6bc8; chỉ đọc).\n"
    "- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW.md, REVIEW-2.md, REVIEW-3.md (cho đợt thu 2; chưa có phản biện "
    "nào cho thu bù 3).\n"
    "- Code và kết quả liên quan: results/T-063/thu3/ (KE-HOACH.md, CHECKPOINT.md, thay-doi-may.md, dieu-kien-xac-nhan-3.md, lich-3.json, "
    "xac-nhan-ca-3.json, so-sanh-o-cu.json, de-xuat-WHY.md, BAN-GIAO-B.md, do/, thu-ngan/, thu/ kèm SHA256SUMS, scripts/ gồm inj3.py, "
    "tao_runner4.py → runner4.py, runner4.diff, tao_xac_nhan_ca_3.py, va_xac_nhan_recreate.py → xac_nhan_ca_3.py, va_inj3_recreate.py, "
    "build-t063-event.sh, deploy-t063-event.sh, h3-pool-event.patch, thu_pool.sh, thu_h4.sh, do_h4.py, pool_prom.py, phan_tich_do_h4.py, "
    "nhan_thu3.sh, dong_bang_3.py, so_sanh_o_cu.py); bản gốc để đối chiếu: results/T-063/chay/runner3.py, chay/xac_nhan_ca.py, "
    "chay/dieu-kien-xac-nhan.md, tiem-loi/inj2.py, dong-bang/dong_bang.py; đóng băng results/T-063/dong-bang/dong-bang-2.json và "
    "dong-bang-3.json. Máy: exp-obs ~/rca-dieu-phoi/thu3, /opt/flash-ticket-rca/cases|outputs/<mã>, /opt/rca-m1ft/bo-sung-dev3/<mã>; "
    "exp-app ~/inj3.py, ~/t063/thu3/ (chỉ đọc; cách gọi máy ở results/T-063/thu3/CHECKPOINT.md, không in khóa).\n"
    "- Phạm vi ghi được Minh cho phép trong lượt này: một bản phản biện mới tasks/T-063-quan-sat-thu-dev-2/REVIEW-4.md theo "
    "tasks/_MAU/REVIEW.md (liệt kê thư mục trước; nếu REVIEW-4.md đã có thì lấy tên lượt kế tiếp); ngoài ra chỉ đọc.\n\n")
out = ("# T-063 thu3 — Prompt phản biện cho Codex (soát kết quả)\n\n"
       "Dựng bằng `results/T-063/thu3/scripts/dung_prompt_phan_bien.py` từ `docs/review-prompt.md` (Prompt chung + khối \"Soát kết quả\", "
       "nguyên văn; chỉ điền \"Thông tin lượt này\"). Phiên điều phối phát lượt này theo quyền chiến dịch.\n\n"
       + chung[:a] + TT + chung[b:] + "\n\n" + khoi('### Soát kết quả') + "\n")
RA.write_text(out, encoding='utf-8')
print(RA, len(out))
