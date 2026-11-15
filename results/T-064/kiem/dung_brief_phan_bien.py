# -*- coding: utf-8 -*-
"""Dựng brief phản biện cho Codex từ docs/review-prompt.md: Prompt chung nguyên văn + khối công đoạn nguyên văn,
chỉ thay khối "Thông tin lượt này" bằng thông tin trung tính (AGENTS mục 9).
Dùng: py -3 -B results/T-064/kiem/dung_brief_phan_bien.py  → results/T-064/codex/R1-brief.md, results/T-063/codex/R3-brief.md
Không ghi đè brief đã có."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
rp = (R / 'docs/review-prompt.md').read_text(encoding='utf-8')


def khoi(tieu_de):
    i = rp.index(tieu_de); j = rp.index('```text', i); k = rp.index('```', j + 7)
    return rp[j:k + 3]


chung = khoi('## Prompt chung')
a = chung.index('Thông tin lượt này:'); b = chung.index('Không sửa ngoài phạm vi trên')
dau, sau = chung[:a], chung[b:]

CHUNG_T = ("- Gói/cổng: chiến dịch M1-FlashTicket, mốc {moc} (tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 5 và 7); "
           "giai đoạn 2 không có khối trọng tâm cổng riêng trong docs/review-prompt.md.\n"
           "- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (SPEC {task}).\n")

T64 = ("Thông tin lượt này:\n"
       "- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/), kết quả giữa chừng: hai lượt chọn trên dev bản 2 và hồ sơ chọn bản nháp 1 "
       "(results/T-064/ho-so-chon.md) cùng các đầu ra nó dẫn tới. Task chưa xong; các bước còn lại liệt kê ở mục 7 của hồ sơ.\n"
       "- Công đoạn: soát kết quả.\n" + CHUNG_T.format(moc='M3', task='T-064') +
       "- Tài liệu gốc: tasks/T-064-m1-flashticket/SPEC.md (gồm phần bổ sung), LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md, "
       "CHECKPOINT-CHIEN-DICH.md; results/T-064/tieu-chi-chon.md; results/T-064/ho-so-chon.md; results/T-064/so-bien-the.jsonl; "
       "results/T-064/dap-an-dev2.json; results/T-064/tap-chon-dev2-12.json, tap-chon-dev2-13.json; "
       "results/T-064/phan-tich/ghi-chu-co-che-dev2.md; results/T-064/thay-doi-may.md; results/T-064/hop-dong-dau-ra.md; "
       "docs/WHY.md WHY-81 trở đi; commit gốc c3d27f8a (đầu ra chưa commit).\n"
       "- Phản biện và phản hồi trước: chưa có bản phản biện nào của T-064. Tiêu chí chọn đã qua hai lượt góp ý trong chat trước khi khóa "
       "(ghi ở đầu results/T-064/tieu-chi-chon.md).\n"
       "- Code và kết quả liên quan: src/m1_ft/ (chay.py, chay_ca.py, cham.py, bo_sung.py, thanh_phan/, tests/); src/m1/ và src/p3/danh_gia.py "
       "(chỉ đọc); results/T-064/bien-the/<mã>/ (cau-hinh.json, ra-kiem-cai-dat-*, ra-khong-hoi-quy-1, ra-khong-hoi-quy-2); results/T-064/cham/ "
       "(cham_dev2.py, cham_kiem_cai_dat.py, giu_bo.py, giu_bo_luot2.py, dau-ra-dev2/, chon-dev2-luot1-*, chon-dev2-luot2-*, khong-hoi-quy-1.json, "
       "khong-hoi-quy-2.json, kiem-cai-dat-*.json, t062-p7.json); results/T-064/kiem/ (ghi_so_*.py, kiem_luot2.py, kiem-luot2.json, nhan_luot2.sh, "
       "nhan-luot2/, chay_bien_the_obs_*.sh, tuong-duong-p7-*); dữ liệu ca: results/T-063/thu2/ (SHA256SUMS), results/T-063/chay/xac-nhan-ca.json, "
       "xac-nhan-ca-2.json, dieu-kien-xac-nhan.md, results/T-062/ca/, results/T-059/danh-muc-loi.json. Môi trường ghim: "
       "D:/RCA-ext/envs/py312-pin/Scripts/python.exe với PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages; được chạy lại bộ chấm và test "
       "đơn vị trên đầu ra đã lưu, ghi đầu ra thử vào thư mục tạm ngoài repo; không chạy lô biến thể mới, không đổi máy exp-obs/exp-app, "
       "không đọc data/locked/ hay ô đánh giá.\n"
       "- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-064-m1-flashticket/REVIEW.md (mới) theo tasks/_MAU/REVIEW.md; "
       "trả lời ngắn ở cuối lượt.\n\n")

T63 = ("Thông tin lượt này:\n"
       "- Task hoặc đề xuất: T-063 (tasks/T-063-quan-sat-thu-dev-2/), phản hồi của người làm với REVIEW-2.md và các sửa kèm theo.\n"
       "- Công đoạn: người phản biện kiểm lại phản hồi và sửa.\n" + CHUNG_T.format(moc='M2', task='T-063') +
       "- Tài liệu gốc: tasks/T-063-quan-sat-thu-dev-2/SPEC.md (gồm phần bổ sung), LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md, "
       "CHECKPOINT-CHIEN-DICH.md; results/T-063/bao-cao.md; results/T-063/quan-sat/thay-doi-may.md; results/T-063/o-dev-bo-sung.md; "
       "results/T-063/chay/ (HO-SO-LUOT.md, D2B-KET-QUA.md, dieu-kien-xac-nhan.md, xac-nhan-ca.json, xac-nhan-ca-2.json, lich-2.json); "
       "results/T-063/dong-bang.md; docs/WHY.md WHY-81 trở đi; commit gốc c3d27f8a (đầu ra chưa commit).\n"
       "- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW.md (lượt 1) và REVIEW-2.md (lượt 2), mỗi bản kèm bảng "
       "\"Phản hồi của người làm\"; mục đáp phản biện lượt 2 trong LOG.md.\n"
       "- Code và kết quả liên quan: results/T-063/thu2/ (SHA256SUMS, ca/, chay/, tiem-loi/, audit/), results/T-063/span-goc/ (phan_loai.py, "
       "phan_loai_dev2.py, phan-loai-dev2.json, phan-loai-dev2.log), results/T-063/chay/, dong-goi/, tiem-loi/, cpu-book/, ca-nen/, h5/, kiem-r/, "
       "kiem-tich-hop/, dieu-phoi/; results/T-064/phan-tich/ghi-chu-co-che-dev2.md (mục Q4 và đính chính); kiểm toàn vẹn: `sha256sum -c SHA256SUMS` "
       "trong results/T-063/thu2/; máy exp-app/exp-obs chỉ đọc qua SSH (khóa và known_hosts như results/T-063/chay/runner2.py); không chạy tải, "
       "không tiêm lỗi, không đổi cấu hình máy.\n"
       "- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-063-quan-sat-thu-dev-2/REVIEW-3.md (mới) theo tasks/_MAU/REVIEW.md; "
       "trả lời ngắn ở cuối lượt.\n\n")


def dung(tieu_de, tt, ten_khoi):
    return (f"# {tieu_de}. Codex chạy trong sandbox workspace-write.\n\nPrompt chung (nguyên văn docs/review-prompt.md) với thông tin lượt này:\n\n"
            f"{dau}{tt}{sau}\n\n{khoi(ten_khoi)}\n")


for p, noi_dung in ((R / 'results/T-064/codex/R1-brief.md', dung('Brief phản biện T-064 lượt 1 — kết quả hai lượt chọn và hồ sơ chọn bản nháp', T64, '### Soát kết quả')),
                    (R / 'results/T-063/codex/R3-brief.md', dung('Brief T-063 lượt 3 — người phản biện kiểm lại phản hồi và sửa sau REVIEW-2', T63, '### Kiểm lại phản hồi và sửa'))):
    if p.exists(): print('đã có, giữ nguyên:', p); continue
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(noi_dung, encoding='utf-8', newline='\n'); print('ghi', p, len(noi_dung))
