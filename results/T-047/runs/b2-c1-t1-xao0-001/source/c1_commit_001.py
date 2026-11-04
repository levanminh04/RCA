"""Một commit đã được Minh duyệt: chỉ C1 và Q-233; giữ mọi diff có sẵn."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];AUDIT=ROOT/'results/T-047/runs/c1-ap-dung-001'


def git(*args,**kwargs):return subprocess.check_output(['git',*args],cwd=ROOT,**kwargs)


def main():
    if (AUDIT/'commit.json').exists():
        print((AUDIT/'commit.json').read_text(encoding='utf-8'))
        return
    if git('diff','--cached','--name-only').strip():
        if '--commit' not in sys.argv or git('diff','--cached','--no-ext-diff')!=(AUDIT/'commit-staged.diff').read_bytes():
            raise ValueError('có staged thay đổi khác, không tự chạm')
    previous=git('rev-parse','HEAD').decode().strip()
    row=(AUDIT/'Q-233-row.txt').read_bytes()
    base=git('show','HEAD:docs/DECISIONS.md')
    staged_dec=base.rstrip(b'\r\n')+b'\n\n'+row.replace(b'\r\n',b'\n')
    blob=git('hash-object','-w','--stdin',input=staged_dec).decode().strip()
    subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,'docs/DECISIONS.md'],cwd=ROOT,check=True)
    subprocess.run(['git','add','--','src/m1/cong.py'],cwd=ROOT,check=True)
    staged=git('diff','--cached','--name-only').decode().splitlines()
    if sorted(staged)!=['docs/DECISIONS.md','src/m1/cong.py']:raise ValueError('sai tập file commit')
    diff=git('diff','--cached','--no-ext-diff')
    (AUDIT/'commit-staged.diff').write_bytes(diff)
    staged_src=git('show',':src/m1/cong.py').decode()
    proposed=(ROOT/'results/T-047/runs/de-xuat-c1-003/cong-proposed.py').read_text(encoding='utf-8')
    if staged_src.replace('\r\n','\n')!=proposed.replace('\r\n','\n'):raise ValueError('staged src không đúng patch được duyệt')
    if b'Q-231' in git('diff','--cached','--','docs/DECISIONS.md') or b'Q-232' in git('diff','--cached','--','docs/DECISIONS.md'):
        raise ValueError('không commit Q-231/Q-232 có sẵn')
    subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
    # Chỉ thực hiện sau khi caller đọc commit-staged.diff và gọi --commit.
    if '--commit' not in sys.argv:
        print(diff.decode());return
    result=subprocess.check_output(['git','commit','-m','fix(m1): ổn định thứ tự tính G3 theo C1; ghi Q-233'],cwd=ROOT)
    after=git('rev-parse','HEAD').decode().strip()
    receipt=dict(before=previous,commit=after,files=staged,push='NOT_AUTHORIZED',stdout=result.decode(),
                 src_sha256=hashlib.sha256((ROOT/'src/m1/cong.py').read_bytes()).hexdigest())
    (AUDIT/'commit.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    print(json.dumps(receipt,ensure_ascii=False))


if __name__=='__main__':main()
