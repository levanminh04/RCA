# -*- coding: utf-8 -*-
"""Dựng brief lượt 4 của T-064 (phản biện cuối, phần thay đổi sau REVIEW-3: đáp REVIEW-3, tập dev bản 3, lô 5, V082, dời mốc,
chỉ mục xuất, hồ sơ chọn §14–§16, WHY-94..98) từ brief lượt 3: giữ nguyên Prompt chung và khối "Soát kết quả" (nguyên văn
docs/review-prompt.md), chỉ thay dòng thông tin trung tính.
Dùng: py -3 -B results/T-064/kiem/dung_brief_r4.py → results/T-064/codex/R4-brief.md (không ghi đè)."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
rp = (R / 'docs/review-prompt.md').read_text(encoding='utf-8')
b3 = (R / 'results/T-064/codex/R3-brief.md').read_text(encoding='utf-8')
ra = R / 'results/T-064/codex/R4-brief.md'
if ra.exists(): raise SystemExit('đã có R4-brief.md')


def khoi(tieu_de):
    i = rp.index(tieu_de); j = rp.index('```text', i); k = rp.index('```', j + 7)
    return rp[j:k + 3]


def thay_dong(t, dau, moi):
    ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith(dau)]
    assert len(vt) == 1, (dau, len(vt)); ds[vt[0]] = moi
    return '\n'.join(ds)


t = b3
assert t.count(khoi('### Soát kết quả')) == 1
t = thay_dong(t, '# Brief T-064 lượt 3', '# Brief T-064 lượt 4 — người phản biện soát kết quả phần thay đổi sau REVIEW-3 (phản biện cuối của chiến dịch). Codex chạy trong sandbox workspace-write.')
t = thay_dong(t, '- Task hoặc đề xuất:', '- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/), phần thay đổi sau REVIEW-3.md: đáp REVIEW-3 (bảng phản hồi, '
              'ho-so-chon.md mục 14, WHY-94); tập chọn dev bản 3 và đáp án (tap-chon-dev3-17.json, tap-dev3-19-do-nhay.json, dap-an-dev3.json, '
              'dap-an-dev3-B.json; WHY-95, WHY-97); lô 5 (WHY-96; đối chứng V066/V067, tổ hợp V068–V072, dời mốc V073–V081); V082 '
              '(sổ dòng 180 trở đi); chấm và luật giữ/bỏ (ho-so-chon.md mục 15); dời mốc V082 (mục 16); bản đề xuất cuối V082 '
              '(WHY-98, cau-hinh-de-xuat.json, ban-xuat/chi-muc-ban.json bản 2, gồm đính chính hash cấu hình 16:57Z). Task chưa đóng: '
              'còn M4 của chiến dịch.')
t = thay_dong(t, '- Phản biện và phản hồi trước:', '- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW.md, REVIEW-2.md, REVIEW-3.md, '
              'mỗi bản kèm bảng "Phản hồi của người làm"; các mục LOG.md "Phiên 5"; quyết định ở docs/DECISIONS.md các mục ngày 13–14/11/2026 '
              '(gồm "Tập chấp nhận ô H4…", "Bản đề xuất cuối M1-FlashTicket (T-064): V082").')
t = thay_dong(t, '- Phạm vi ghi được Minh cho phép trong lượt này:', '- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-064-m1-flashticket/REVIEW-4.md (mới) '
              'theo tasks/_MAU/REVIEW.md (liệt kê thư mục trước; nếu đã có thì lấy tên lượt kế tiếp); trả lời ngắn ở cuối lượt. '
              'Được đọc exp-obs theo cách gọi máy ở results/T-063/thu3/CHECKPOINT.md (chỉ đọc, không in khóa); không ghi máy.')
ds = t.split('\n'); vt = [i for i, d in enumerate(ds) if d.startswith('- Code và kết quả liên quan:')]; assert len(vt) == 1
ds[vt[0]] = ('- Code và kết quả liên quan: results/T-064/manifest.json (kiểm hash trước khi dùng); results/T-064/tieu-chi-chon.md (đã khóa); '
             'results/T-064/cham/cham_dev3.py, giu_bo_dev3.py, spec-dev3-d0.json, spec-dev3-d0-v082.json, spec-dev3-doi-moc.json và các đầu ra '
             'chon-dev3-d0-*, chon-dev3-d0-v082-*, giu-bo-dev3-d0-*, giu-bo-dev3-d0-v082-*, doi-moc-dev3-*; results/T-064/kiem/luot5/ '
             '(l5_chay.sh, l5_xuat_bo_sung.sh, các file việc, kiem_bo_sung_l5.py, laptop-kiem/), kiem/ghi_so_luot5.py, kiem/nhan-luot5/ '
             '(NHAN-D0.sha256, log, l5/), kiem/tao_manifest_t064.py; results/T-064/bien-the/V066…V082; results/T-064/so-bien-the.jsonl '
             '(dòng V066 trở đi); results/T-064/ban-xuat/ (dung_chi_muc.py, chi-muc-ban.json và các bản giữ lịch sử); '
             'results/T-064/cau-hinh-de-xuat.json; results/T-064/thay-doi-may.md (TD-64-14); src/m1_ft/ (không đổi trong lượt này: '
             'kiểm bằng hash nguồn trong sổ); results/T-065/kiem/005-gc-cuoi/BAO-CAO.md (phát hiện lệch hash cấu hình).')
t = '\n'.join(ds)
ra.write_text(t, encoding='utf-8', newline='\n'); print('ghi', ra, len(t))
