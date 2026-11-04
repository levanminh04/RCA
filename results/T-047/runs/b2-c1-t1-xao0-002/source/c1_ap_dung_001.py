"""Thực hiện duyệt C1, lưu trước/sau và ngân sách; không commit hoặc push ở script này."""
import hashlib
import json
import subprocess
import time
from datetime import datetime,timedelta,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-047'
QUOTE=('Duyệt áp đúng patch C1 (runs/de-xuat-c1-003/de-xuat.patch) vào o_1s và tu_tuong_quan trong src/m1/cong.py, một commit. Ghi Q-233. Nâng trần tổng lên 8 giờ, tính cả phần đã chạy. '
       'Chạy lại đủ T1 bằng code đã sửa. Lệch số so với T-046 thì giải thích từng chỗ, không đổi tiêu chí. Đổi công thức, ngưỡng, ma trận hoặc cần vượt 8 giờ thì dừng trình tôi. Push chờ duyệt riêng. nếu có thể tối ưu song song tiến trình thì cứ thực hiện, tôi sẽ tắt bớt các tiến trình khác')


def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')


def main():
    audit=OUT/'runs/c1-ap-dung-001';audit.mkdir(parents=True,exist_ok=False)
    stamp=datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')
    budget_path=OUT/'runs/ngan-sach.json';budget=json.loads(budget_path.read_text(encoding='utf-8'))
    write(audit/'ngan-sach-truoc.json',budget)
    # Giữ phần đã dùng; loại đúng khoảng chờ Minh đã đánh dấu. Trần8giờ là tổng.
    carried=budget['used_seconds_when_waiting'];epoch=time.time()
    budget.setdefault('resume_history',[]).append(dict(wait_from=budget['waiting_for_Minh_since_epoch'],resume_at=epoch,
       excluded_wait_seconds=epoch-budget['waiting_for_Minh_since_epoch'],old_start_epoch=budget['start_epoch'],
       old_prior_seconds=budget['prior_seconds'],used_seconds_carried=carried,old_cap_seconds=budget['cap_seconds'],new_cap_seconds=28800))
    budget.update(start_epoch=epoch,prior_seconds=carried,cap_seconds=28800,
                  note='Q-233: trần tổng8giờ, giữ mọi thời gian đã chạy; thời gian chờ Minh loại theo SPEC. Không reset phần đã dùng.')
    for k in ('waiting_for_Minh_since_epoch','used_seconds_when_waiting','remaining_seconds_at_stop'):budget.pop(k,None)
    write(budget_path,budget)
    # Manifest checkpoint trước có budget cũ: kiểm tất cả entry còn lại, budget đối chiếu bản snapshot vừa lưu.
    m=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'));errors=[]
    for name,e in m['outputs'].items():
        p=ROOT/name
        if name=='results/T-047/runs/ngan-sach.json':p=audit/'ngan-sach-truoc.json'
        # JSON được snapshot bằng bộ ghi thống nhất nhưng byte newline có thể khác; so nội dung budget.
        if name=='results/T-047/runs/ngan-sach.json':
            expected=json.loads((audit/'ngan-sach-truoc.json').read_text(encoding='utf-8'))
            if expected.get('used_seconds_when_waiting')!=carried:errors.append(name)
        elif digest(p)!=e['sha256']:errors.append(name)
    write(audit/'kiem-manifest-truoc.json',dict(entries=len(m['outputs']),errors=errors,PASS=not errors))
    if errors:raise ValueError('manifest cũ lệch: '+repr(errors))
    for rel in ('src/m1/cong.py','docs/DECISIONS.md','docs/STATE.md','docs/WHY.md',
                'tasks/T-047-khoi-k-luot-2/SPEC.md','tasks/T-047-khoi-k-luot-2/LOG.md'):
        p=audit/'before'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/rel).read_bytes())
    decisions=ROOT/'docs/DECISIONS.md';old=decisions.read_text(encoding='utf-8')
    if '| Q-233 |' in old:raise ValueError('Q-233 đã có, không ghi đè')
    row=f'| Q-233 | 02/11/2026 | “{QUOTE}” | Duyệt đúng patch C1 tại results/T-047/runs/de-xuat-c1-003/de-xuat.patch, chỉ o_1s/tu_tuong_quan trong src/m1/cong.py; một commit cho C1 và dòng này, không kèm thay đổi có sẵn ngoài phạm vi. Nguồn code chạy: c298188e cộng C1; chạy lại đủ T1, giải thích từng lệch T-046, giữ tiêu chí. Trần tổng8giờ tính cả phần đã chạy; tối ưu song song trong giới hạn4tiếntrình local. Đổi công thức/ngưỡng/ma trận hoặc vượt8giờ phải dừng trình. Push chờ duyệt riêng. Không mở G3/test hoặc xác nhận hiệu quả RCA. Nguồn: Minh duyệt trực tiếp trong chat ngày02/11/2026. |'
    with decisions.open('a',encoding='utf-8') as f:f.write('\n'+row+'\n')
    (audit/'Q-233-row.txt').write_text(row+'\n',encoding='utf-8')
    with (ROOT/'tasks/T-047-khoi-k-luot-2/LOG.md').open('a',encoding='utf-8') as f:
        f.write(f'\n## Phiên 6 — {stamp} — Codex, máy Windows của Minh, người làm\n\nMinh duyệt nguyên văn: “{QUOTE}”. Phân loại EXECUTE. Đã đọc AGENTS/STATE/SPEC/cuối LOG, patch và nguồn gốc. Quyền mở rộng đúng hai hàm của src/m1/cong.py và một dòng Q-233; một commit C1/Q-233, push chưa duyệt. Phạm vi khác giữ results/T-047, nối LOG, dòng T-047 của STATE. Giữ mọi thay đổi có sẵn. Ngân sách mang tiếp {carried/60:.2f} phút đã dùng, loại khoảng chờ Minh theo SPEC, trần tổng28800giây. Snapshot/kiểm manifest trước ở runs/c1-ap-dung-001. Không đọc nhãn chấm hoặc dữ liệu khóa; không đổi công thức/ngưỡng/ma trận/luật chọn.\n')
    patch=OUT/'runs/de-xuat-c1-003/de-xuat.patch'
    proposal=json.loads((patch.parent/'kiem-ung-vien.json').read_text(encoding='utf-8'))
    src=ROOT/'src/m1/cong.py'
    if digest(src)!=proposal['source_sha256']:raise ValueError('nguồn src lệch trước patch')
    subprocess.run(['git','apply','--check','--ignore-space-change',str(patch)],cwd=ROOT,check=True)
    subprocess.run(['git','apply','--ignore-space-change',str(patch)],cwd=ROOT,check=True)
    if src.read_text(encoding='utf-8').replace('\r\n','\n') != (patch.parent/'cong-proposed.py').read_text(encoding='utf-8').replace('\r\n','\n'):
        raise ValueError('sau áp không đúng bản đã duyệt')
    diff=subprocess.check_output(['git','diff','--','src/m1/cong.py'],cwd=ROOT)
    (audit/'src-C1.diff').write_bytes(diff)
    write(audit/'ap-dung.json',dict(PASS=True,patch=str(patch.relative_to(ROOT)),patch_sha256=digest(patch),
          source_before_sha256=proposal['source_sha256'],source_after_sha256=digest(src),budget=budget,
          decision='Q-233',commit='NOT_YET',push='NOT_AUTHORIZED'))
    print(json.dumps(dict(applied=True,src_sha256=digest(src),carried_minutes=carried/60,cap_hours=8)))


if __name__=='__main__':main()
