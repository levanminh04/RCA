"""Kiểm tiếp nhận chỉ đọc nguồn, ghi kiểm và nhật ký trong T-029."""
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-029'
LOG = ROOT / 'tasks/T-029-p4-han-che-phat-hien/LOG.md'
RUN = OUT / 'runs/resume-step7-001'

def now(): return datetime.now(timezone(timedelta(hours=7))).isoformat()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(s):
    with LOG.open('a', encoding='utf-8') as f: f.write('\n- ' + now() + ' — Phiên 7: ' + s + '\n')
def write(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    log('Ghi ' + str(Path(p).relative_to(ROOT)).replace('\\','/'))

def main():
    t0=time.perf_counter()
    log('Lệnh có ghi: T-014-main python -B -W ignore results/T-029/scripts/resume_step7.py; kiểm mọi tệp checkpoint và V1 trước sử dụng. Hai hỗ trợ Codex chỉ đọc E/G và P1/P2; root giữ vai trò người làm, Claude phản biện. Không chạy lại thí nghiệm.')
    assert not RUN.exists()
    RUN.mkdir()
    before={'git_status':subprocess.check_output(['git','status','--short'],cwd=ROOT).decode(),
            'git_diff':subprocess.check_output(['git','diff'],cwd=ROOT).decode(),
            'state':(ROOT/'docs/STATE.md').read_text(encoding='utf-8'),
            'log_sha':sha(LOG),'started':now()}
    write(RUN/'before.json',before)
    c=read(OUT/'runs/checkpoint-after5-001/manifest.json')
    mismatches=[]
    for p,v in c['files'].items():
        q=ROOT/p
        if not q.is_file() or q.stat().st_size!=v['bytes'] or sha(q)!=v['sha256']: mismatches.append(p)
    p3=sorted((ROOT/'src/p3').rglob('*.py'))
    h=hashlib.sha256()
    for p in p3: h.update(p.read_bytes())
    src={'tong':h.hexdigest(),'tep':{p.relative_to(ROOT).as_posix():sha(p) for p in p3}}
    base=read(OUT/'runs/buoc0-001/manifest.json')
    checks={'checkpoint_files':not mismatches,'src_p3':src==c['src_p3']==base['src_p3'],
            'governing_sources':all(sha(ROOT/p)==v for p,v in base['nguon'].items())}
    from p3.selector import nap_allowlist, chon_ca
    allow=nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
    n=sum(len(chon_ca(allow,oid,ROOT,kiem_hash=True)) for oid in allow)
    checks['dev_guard']=len(allow)==30 and n==89
    result={'status':'PASS' if all(checks.values()) else 'STOP','time':now(),'checks':checks,
            'checkpoint_manifest_sha256':sha(OUT/'runs/checkpoint-after5-001/manifest.json'),
            'files_checked':len(c['files']),'mismatches':mismatches,'src_p3':src,
            'dev_cases':len(allow),'dev_files':n,'wall_s':time.perf_counter()-t0}
    write(RUN/'verification.json',result)
    if result['status']!='PASS':
        log('DỪNG TOÀN TASK: hash/V1 tiếp nhận lệch; xem verification.json. Không dùng checkpoint hoặc chạy bước phụ thuộc.')
        raise RuntimeError('checkpoint/V1 mismatch')
    log('Tiếp nhận PASS: toàn bộ hash/kích thước checkpoint, src/p3 và allowlist dev khớp. Không chạy lại đầu ra hợp lệ; tiếp theo ghi quy tắc/danh sách đọc tay trước đọc bằng chứng từng ca.')
    print(json.dumps({k:v for k,v in result.items() if k!='src_p3'}))

if __name__=='__main__': main()
