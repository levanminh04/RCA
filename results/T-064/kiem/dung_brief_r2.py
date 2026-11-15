# -*- coding: utf-8 -*-
"""Dựng brief lượt 2 của T-064 (người phản biện kiểm lại phản hồi và sửa) từ brief lượt 1:
giữ nguyên Prompt chung, thay bốn dòng thông tin trung tính và thay khối công đoạn bằng khối nguyên văn của docs/review-prompt.md.
Dùng: py -3 -B results/T-064/kiem/dung_brief_r2.py → results/T-064/codex/R2-brief.md (không ghi đè)."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
rp = (R / 'docs/review-prompt.md').read_text(encoding='utf-8')
b1 = (R / 'results/T-064/codex/R1-brief.md').read_text(encoding='utf-8')
ra = R / 'results/T-064/codex/R2-brief.md'
if ra.exists(): raise SystemExit('đã có R2-brief.md')


def khoi(tieu_de):
    i = rp.index(tieu_de); j = rp.index('```text', i); k = rp.index('```', j + 7)
    return rp[j:k + 3]


def thay_dong(t, dau, moi):
    ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith(dau)]
    assert len(vt) == 1, (dau, len(vt)); ds[vt[0]] = moi
    return '\n'.join(ds)


t = b1
t = thay_dong(t, '# Brief phản biện T-064 lượt 1', '# Brief T-064 lượt 2 — người phản biện kiểm lại phản hồi và sửa sau REVIEW lượt 1. Codex chạy trong sandbox workspace-write.')
t = thay_dong(t, '- Task hoặc đề xuất:', '- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/), phản hồi của người làm với REVIEW.md lượt 1 và các sửa kèm theo: '
              'sửa mã src/m1_ft/thanh_phan/h1_canh.py, lượt chọn 3 trên dev bản 2, docs/WHY.md WHY-85 và WHY-86, results/T-064/ho-so-chon.md mục 4, 8, 9, 10, 11. Task chưa xong.')
t = thay_dong(t, '- Công đoạn:', '- Công đoạn: người phản biện kiểm lại phản hồi và sửa.')
t = thay_dong(t, '- Phản biện và phản hồi trước:', '- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW.md (lượt 1) kèm bảng "Phản hồi của người làm"; '
              'các mục phiên 3 trong LOG.md; quyết định về tập chọn ở docs/DECISIONS.md mục "Tập chọn dev bản 2: nhận "Sửa sau 1", dùng 13 ca".')
t = thay_dong(t, '- Phạm vi ghi được Minh cho phép trong lượt này:', '- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-064-m1-flashticket/REVIEW-2.md (mới) theo tasks/_MAU/REVIEW.md; trả lời ngắn ở cuối lượt.')
ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith('- Code và kết quả liên quan:')]; assert len(vt) == 1
ds[vt[0]] += (' Bổ sung lượt này: results/T-064/kiem/ghi_so_chon_dev2_luot3.py, kiem_luot3.py, kiem-luot3.json, nhan_luot3.sh, nhan-luot3/, '
              'ghi_so_sau_cham_luot3.py, chay_bien_the_obs_luot3.sh, goi-tai-len-8.sha256; results/T-064/cham/chon-dev2-luot3-tap12.json, chon-dev2-luot3-tap13.json, '
              'khong-hoi-quy-3.json; results/T-064/bien-the/V038…V047 (cau-hinh.json, ra-khong-hoi-quy-3) và cham/dau-ra-dev2/V038…V047; '
              'results/T-064/chu-thich-thao-tac-nen.md; results/T-064/thay-doi-may.md mục TD-64-09.')
t = '\n'.join(ds)
cu, moi = khoi('### Soát kết quả'), khoi('### Kiểm lại phản hồi và sửa')
assert t.count(cu) == 1; t = t.replace(cu, moi)
ra.write_text(t, encoding='utf-8', newline='\n'); print('ghi', ra, len(t))
