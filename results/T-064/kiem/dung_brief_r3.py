# -*- coding: utf-8 -*-
"""Dựng brief lượt 3 của T-064 (người phản biện soát kết quả phần mới sau R2: lượt 4 đối chứng bỏ quan hệ, phiên C dời mốc ±30 s,
H8-adapter, H8-log, WHY-87..89, ho-so-chon §12–§13) từ brief lượt 2: giữ nguyên Prompt chung, thay dòng thông tin trung tính,
thay khối công đoạn bằng khối "Soát kết quả" nguyên văn của docs/review-prompt.md.
Minh duyệt lượt này 14/11/2026 (phiên ed8b9c01, "duyệt cả 2").
Dùng: py -3 -B results/T-064/kiem/dung_brief_r3.py → results/T-064/codex/R3-brief.md (không ghi đè)."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
rp = (R / 'docs/review-prompt.md').read_text(encoding='utf-8')
b2 = (R / 'results/T-064/codex/R2-brief.md').read_text(encoding='utf-8')
ra = R / 'results/T-064/codex/R3-brief.md'
if ra.exists(): raise SystemExit('đã có R3-brief.md')


def khoi(tieu_de):
    i = rp.index(tieu_de); j = rp.index('```text', i); k = rp.index('```', j + 7)
    return rp[j:k + 3]


def thay_dong(t, dau, moi):
    ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith(dau)]
    assert len(vt) == 1, (dau, len(vt)); ds[vt[0]] = moi
    return '\n'.join(ds)


t = b2
t = thay_dong(t, '# Brief T-064 lượt 2', '# Brief T-064 lượt 3 — người phản biện soát kết quả phần mới sau REVIEW-2. Codex chạy trong sandbox workspace-write.')
t = thay_dong(t, '- Task hoặc đề xuất:', '- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/), các đầu ra mới sau REVIEW-2.md: lượt 4 đối chứng bỏ quan hệ '
              '(V048–V051, results/T-064/ho-so-chon.md mục 12); phiên phụ C (dời mốc ±30 s, H8-adapter, H8-log; V052–V065; ho-so-chon.md mục 13; '
              'docs/WHY.md WHY-87, WHY-88, WHY-89; mã mới/đổi trong src/m1_ft/). Task chưa xong: còn chờ ô thu bù 3 của T-063 '
              '(POOL-EVENT, CONSUMER-BOOK-SLOW-X3, RECREATE-PAY, đối chứng) đang thu trên exp-obs và các bước ghi ở ho-so-chon.md mục 7.')
t = thay_dong(t, '- Công đoạn:', '- Công đoạn: soát kết quả.')
t = thay_dong(t, '- Phản biện và phản hồi trước:', '- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW.md (lượt 1) và REVIEW-2.md (lượt 2), '
              'mỗi bản kèm bảng "Phản hồi của người làm"; các mục LOG.md từ phiên 4; quyết định ở docs/DECISIONS.md các mục ngày 13–14/11/2026.')
t = thay_dong(t, '- Phạm vi ghi được Minh cho phép trong lượt này:', '- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-064-m1-flashticket/REVIEW-3.md (mới) '
              'theo tasks/_MAU/REVIEW.md; trả lời ngắn ở cuối lượt. Không truy cập exp-obs/exp-app (đang có đợt thu T-063).')
ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith('- Code và kết quả liên quan:')]; assert len(vt) == 1
ds[vt[0]] += (' Bổ sung lượt 3: results/T-064/kiem/tao_luot4_doi_chung_bo_qh.py, chay_bien_the_obs_luot4.sh, nhan_luot4.sh, nhan-luot4/, '
              'ghi_so_sau_cham_luot4.py, goi-tai-len-9.sha256, goi-tai-len-10.sha256, goi-tai-len-11.sha256; results/T-064/bien-the/V048…V065 và '
              'cham/dau-ra-dev2/V048…V065; results/T-064/phien-c/ (BAN-GIAO-C.md, NHAT-KY.md, CHECKPOINT.md, de-xuat-WHY.md, YEU-CAU-O.md, '
              'cham/, doi-moc/ gồm PHAN-TICH.md và bang-o.md, h8-adapter/, h8-log/, kiem-laptop/, nhan/, các script .py/.sh); '
              'src/m1_ft/chay_ca.py, chay.py, bo_sung.py, doi_moc.py, thanh_phan/h8_adapter.py, thanh_phan/h8_log.py, tests/test_h8.py; '
              'results/T-064/so-bien-the.jsonl (dòng V048 trở đi); results/T-064/thay-doi-may.md (TD-64-10 trở đi).')
t = '\n'.join(ds)
cu, moi = khoi('### Kiểm lại phản hồi và sửa'), khoi('### Soát kết quả')
assert t.count(cu) == 1; t = t.replace(cu, moi)
ra.write_text(t, encoding='utf-8', newline='\n'); print('ghi', ra, len(t))
