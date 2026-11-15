# -*- coding: utf-8 -*-
"""Dựng brief lượt 5 của T-064 (người phản biện kiểm lại phản hồi và sửa sau REVIEW-4: R9, R10) từ brief lượt 4: giữ Prompt chung,
thay khối "Soát kết quả" bằng khối "Kiểm lại phản hồi và sửa" (nguyên văn docs/review-prompt.md), chỉ thay dòng thông tin trung tính.
Dùng: py -3 -B results/T-064/kiem/dung_brief_r5.py → results/T-064/codex/R5-brief.md (không ghi đè)."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
rp = (R / 'docs/review-prompt.md').read_text(encoding='utf-8')
b4 = (R / 'results/T-064/codex/R4-brief.md').read_text(encoding='utf-8')
ra = R / 'results/T-064/codex/R5-brief.md'
if ra.exists(): raise SystemExit('đã có R5-brief.md')


def khoi(tieu_de):
    i = rp.index(tieu_de); j = rp.index('```text', i); k = rp.index('```', j + 7)
    return rp[j:k + 3]


def thay_dong(t, dau, moi):
    ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith(dau)]
    assert len(vt) == 1, (dau, len(vt)); ds[vt[0]] = moi
    return '\n'.join(ds)


t = b4
cu, moi = khoi('### Soát kết quả'), khoi('### Kiểm lại phản hồi và sửa')
assert t.count(cu) == 1; t = t.replace(cu, moi)
t = thay_dong(t, '# Brief T-064 lượt 4', '# Brief T-064 lượt 5 — người phản biện kiểm lại phản hồi và sửa sau REVIEW-4 (R9, R10). Codex chạy trong sandbox workspace-write.')
t = thay_dong(t, '- Task hoặc đề xuất:', '- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/), phản hồi và sửa sau REVIEW-4.md: R9 (kênh liveness theo lần dò mới nhất, '
              'WHY-99, chạy lại 12 cặp ca ebd5ef38, chấm lại, ho-so-chon.md mục 17, chỉ mục xuất bản 3, cấu hình đề xuất) và R10 (ca 1e5a3dc5: '
              'phan-tich/ghi-chu-co-che-dev2.md Q7, chu-thich-thao-tac-nen.md mục 5), theo quyết định Minh 15/11/2026 ở docs/DECISIONS.md '
              '("Sửa R9, R10 (T-064, REVIEW-4) và S1 (T-065, REVIEW-3)"). Task chưa đóng: còn M4 của chiến dịch.')
t = thay_dong(t, '- Công đoạn:', '- Công đoạn: người phản biện kiểm lại phản hồi và sửa.')
t = thay_dong(t, '- Phản biện và phản hồi trước:', '- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW-4.md (bảng "Phản hồi của người làm", gồm dòng R9 bổ sung) '
              'và các bản REVIEW.md, REVIEW-2.md, REVIEW-3.md; các mục LOG.md từ 15/11 01:15Z.')
t = thay_dong(t, '- Phạm vi ghi được Minh cho phép trong lượt này:', '- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-064-m1-flashticket/REVIEW-5.md (mới) '
              'theo tasks/_MAU/REVIEW.md (liệt kê thư mục trước; nếu đã có thì lấy tên lượt kế tiếp); trả lời ngắn ở cuối lượt. '
              'Được đọc exp-obs theo cách gọi máy ở results/T-063/thu3/CHECKPOINT.md (chỉ đọc, không in khóa); không ghi máy.')
ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith('- Code và kết quả liên quan:')]; assert len(vt) == 1
ds[vt[0]] = ('- Code và kết quả liên quan: results/T-064/manifest-2.json (lập trước brief này; R5-brief.md và file R5 sinh sau không có trong bản kê); '
             'results/T-064/kiem/r9/ (so_live_down.py, so-live-down.json, so_live_down_2.py, so-live-down-2.json, xuat_live_down_moi.py, '
             'xuat-live-down-moi.json, r9_chay.sh, viec-r9.txt); results/T-064/kiem/nhan-r9/ (NHAN-R9.sha256, luong-r9.log, r9/); '
             'results/T-064/cham/cham_dev3.py (khóa goc_uu_tien; bản trước cham_dev3_truoc_r9.py), spec-dev3-d0-v082-r9.json, '
             'spec-dev3-doi-moc-r9.json và các đầu ra chon-dev3-d0-v082-r9-*, giu-bo-dev3-d0-v082-r9-*, doi-moc-dev3-r9-*; '
             'results/T-064/ban-xuat/ (dung_chi_muc.py bản 3, chi-muc-ban.json, chi-muc-ban-2.json, dung_chi_muc_2.py); '
             'results/T-064/cau-hinh-de-xuat.json (bản trước cau-hinh-de-xuat-2.json); results/T-064/ho-so-chon.md mục 17; '
             'results/T-064/phan-tich/ghi-chu-co-che-dev2.md Q6, Q7; results/T-064/chu-thich-thao-tac-nen.md mục 5; docs/WHY.md WHY-99; '
             'trên exp-obs /opt/rca-m1ft/out/r9-bo-sung/, /opt/rca-m1ft/out/r9/.')
t = '\n'.join(ds)
ra.write_text(t, encoding='utf-8', newline='\n'); print('ghi', ra, len(t))
