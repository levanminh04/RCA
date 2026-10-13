"""Phiên 8: lưu bản trước sửa và sửa bố cục, không tính lại kết quả khoa học."""
import difflib
import hashlib
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-029'
LOG = ROOT / 'tasks/T-029-p4-han-che-phat-hien/LOG.md'
RUN = OUT / 'runs/report-repair-001'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def log(s):
    with LOG.open('a', encoding='utf-8') as f:
        f.write('\n- '+datetime.now(timezone(timedelta(hours=7))).isoformat()+' — Phiên 8: '+s+'\n')
def main():
    assert not RUN.exists()
    RUN.mkdir()
    log('Lệnh có ghi: T014-main Python -B -X utf8 -W ignore results/T-029/scripts/repair_reports.py. Lưu năm MD, verifier trước sửa và baseline file set/hash; sửa hai separator main, gom note B4 sau bảng theo w, làm rõ câu dấu G. Không tính lại khoa học.')
    files = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    baseline = {p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in files if p and (ROOT/p).is_file() and not p.startswith('data/')}
    before = {'files':baseline,'state_hex':(ROOT/'docs/STATE.md').read_bytes().hex(),'log_hex':LOG.read_bytes().hex(),
              'git_diff':subprocess.check_output(['git','diff'],cwd=ROOT).decode(),
              'git_status':subprocess.check_output(['git','status','--short'],cwd=ROOT).decode()}
    (RUN/'before.json').write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    names = [p.name for p in OUT.glob('*.md')] + ['scripts/verify_reports.py']
    originals = {}
    for name in names:
        p=OUT/name; dest=RUN/(p.name+'.original');dest.write_bytes(p.read_bytes());originals[name]={'sha256':sha(p),'bytes':p.stat().st_size,'saved':dest.relative_to(ROOT).as_posix()}
    mainfile=OUT/'ban-do-han-che-phat-hien.md'
    text=mainfile.read_text(encoding='utf-8'); lines=text.splitlines(keepends=True)
    assert lines[154].startswith('| Mã |') and lines[155].strip()=='|---|---|---|---|---|'
    assert lines[447].startswith('| Bộ |') and lines[448].strip()=='|---|---|---|---|'
    lines[155]='|---|---|---|---|---|---|\n';lines[448]='|---|---|---|---|---|\n'
    mainfile.write_text(''.join(lines),encoding='utf-8')
    p=OUT/'doc-tay.md'; ls=p.read_text(encoding='utf-8').splitlines(); result=[]; i=0; moved=[]
    while i<len(ls):
        if not ls[i].startswith('| w | Cột có bước chuẩn hóa lớn nhất |'):
            result.append(ls[i]);i+=1;continue
        table=[ls[i],ls[i+1]]; notes=[];i+=2; variant=None
        while i<len(ls):
            if ls[i].startswith('| w'):
                variant=ls[i].split('|')[1].strip();table.append(ls[i]);i+=1
            elif not ls[i]: i+=1
            elif ls[i].startswith('Nền hằng đổi riêng (MAD bằng không):'):
                assert variant is not None
                notes.append(variant+': '+ls[i]);i+=1
            else: break
        assert len(table)==5
        result.extend(table);result.append('')
        if notes:result.extend(notes);result.append('');moved.extend(notes)
    p.write_text('\n'.join(result)+'\n',encoding='utf-8')
    p=OUT/'a-so-b.md'; text=p.read_text(encoding='utf-8')
    old='Dương nghĩa chất lượng tăng tại điểm phía sau phép trừ; âm nghĩa giảm.'
    new='Dương nghĩa Hit(t̂⁺) cao hơn Hit(a) đối với Δ cửa sổ, hoặc Hit(t̂) cao hơn Hit(t̂⁺) đối với Δ sự kiện; âm nghĩa ngược lại.'
    assert text.count(old)==1;p.write_text(text.replace(old,new),encoding='utf-8')
    changed=[]
    for name,v in originals.items():
        p=OUT/name
        if sha(p)==v['sha256']:continue
        old=(ROOT/v['saved']).read_text(encoding='utf-8');new=p.read_text(encoding='utf-8')
        assert sorted(re.findall(r'<!--v8:\d+-->.*?<!--/v8-->',old,re.S))==sorted(re.findall(r'<!--v8:\d+-->.*?<!--/v8-->',new,re.S))
        diff=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=name+' (before)',tofile=name+' (after)'))
        (RUN/(p.name+'.diff')).write_text(diff,encoding='utf-8');changed.append(name)
    (RUN/'verification.json').write_text(json.dumps({'status':'PASS','originals':originals,'changed':changed,'moved_note_count':len(moved),'markers_preserved':True,'script_sha256':sha(Path(__file__))},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    log('Sửa bố cục/câu dấu PASS; marker và scalar nguồn giữ nguyên. Bản trước sửa, diff và verification tại runs/report-repair-001; '+str(len(moved))+' ghi chú B4 đã gom sau bảng, gắn w tương ứng. Hai separator sửa đúng số cột header. Baseline gồm '+str(len(baseline))+' tệp không thuộc data. Verifier chưa sửa/chưa chạy V8 mới.')
    print(json.dumps({'changed':changed,'moved_notes':len(moved),'baseline_files':len(baseline)}))
if __name__=='__main__': main()
