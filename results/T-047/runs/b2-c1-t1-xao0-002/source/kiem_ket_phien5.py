"""Kiểm bàn giao tại điểm dừng; manifest không chứng nhận task đạt."""
import ast
import hashlib
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path
import psutil
import adapter_t047 as ad
import tep_pha1


def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def main():
    root,out=ad.ROOT,ad.OUT;audit=out/'runs/ket-phien5-001';audit.mkdir(exist_ok=False)
    previous=out/'runs/phien5-tiep-nhan-001/before'
    protected={s:(root/s).read_bytes()==(previous/s).read_bytes() for s in
       ['docs/WHY.md','docs/DECISIONS.md','tasks/T-047-khoi-k-luot-2/SPEC.md']}
    before=(previous/'docs/STATE.md').read_bytes().splitlines();after=(root/'docs/STATE.md').read_bytes().splitlines()
    diffs=[(a,b) for a,b in zip(before,after) if a!=b]
    log=root/'tasks/T-047-khoi-k-luot-2/LOG.md'
    checks=dict(protected_unchanged=protected,log_append_only=log.read_bytes().startswith(
        (previous/'tasks/T-047-khoi-k-luot-2/LOG.md').read_bytes()),
        state_only_T047=len(before)==len(after) and len(diffs)==1 and all(a.startswith(b'- **T-047 ') and b.startswith(b'- **T-047 ') for a,b in diffs),
        src_diff_empty=not subprocess.check_output(['git','diff','c298188e','--','src'],cwd=root))
    helpers=json.loads((out/'kiem-helper.json').read_text(encoding='utf-8'))['sources']
    checks['step0_sources_unchanged']={p:sha(root/p)==entry['sha256'] for p,entry in helpers.items()}
    paths=['b2-t1-seed0-001','b2-t1-seed1-001','b2-t1-seed2-002','b2-t1-xao0-001','b2-t1-ce-001']
    phases={s:tep_pha1.kiem(out/'runs'/s) for s in paths}
    txt=log.read_text(encoding='utf-8')
    checks['all_hashes_in_LOG']=all(f"- `results/T-047/runs/{s}`: `{m['sha256']}`" in txt for s,m in phases.items())
    t1=json.loads((out/'t1.json').read_text(encoding='utf-8'))
    checks['T1_truthful_stop']=t1['PASS'] is False and t1['bat_bien']['1']['giong_het'] and t1['bat_bien']['2']['giong_het'] and not t1['bat_bien']['xao']['giong_het']
    checks['no_K_started']=not list((out/'runs').glob('b3-k-*'))
    checks['no_scoring_outputs']=not any((out/p).exists() for p in ['khoi-k.json','tai-lap-baseline.json','do-ben.json','so-sanh-t045.json'])
    processes=[]
    for p in psutil.process_iter(['pid','cmdline']):
        try:
            cmd=' '.join(p.info['cmdline'] or [])
            if '--worker' in cmd and 'T-047' in cmd:processes.append(dict(pid=p.pid,cmd=cmd))
        except psutil.Error:pass
    checks['no_method_workers']=not processes
    for p in (out/'scripts').glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    checks['syntax']=True
    suites=list(ET.parse(out/'runs/hoi-quy-cuoi-phien5-001/junit.xml').getroot().iter('testsuite'))
    checks['final_synthetic_suite']=sum(int(x.get('tests',0)) for x in suites)==152 and not any(int(x.get('failures',0))+int(x.get('errors',0))+int(x.get('skipped',0)) for x in suites)
    r=subprocess.run(['git','diff','--check'],cwd=root,capture_output=True,text=True)
    checks['git_diff_check']=r.returncode==0
    (audit/'git-diff-check.txt').write_text(r.stdout+r.stderr,encoding='utf-8')
    # Dừng tính thời gian chờ Minh, giữ nguyên trần và toàn bộ thời gian đã dùng.
    budget=json.loads((out/'runs/ngan-sach.json').read_text(encoding='utf-8'))
    used=budget['prior_seconds']+time.time()-budget['start_epoch']
    budget['waiting_for_Minh_since_epoch']=time.time()
    budget['used_seconds_when_waiting']=used
    budget['remaining_seconds_at_stop']=budget['cap_seconds']-used
    budget['resume_note']='Chờ Minh không tính theo SPEC. Khi có chỉ đạo tiếp, chỉ loại đúng khoảng chờ này; giữ used_seconds_when_waiting và mọi lượt, không reset phần đã dùng hoặc tự nới cap.'
    ad.ghi(out/'runs/ngan-sach.json',budget)
    def okay(v):return all(okay(x) for x in v.values()) if isinstance(v,dict) else bool(v)
    result=dict(integrity_PASS=all(okay(x) for x in checks.values()),task_PASS=False,reason='STOP_C1_T1_order_invariance',
                checks=checks,phase1=phases,budget=budget,workers=processes,
                file_scope=['results/T-047/','append LOG T-047','one T-047 line STATE'])
    ad.ghi(audit/'kiem-ban-giao.json',result)
    # Manifest bao gồm lượt hỏng/candidate, không bỏ lịch sử. Không tự băm chính manifest.
    files={}
    for p in sorted(out.rglob('*')):
        if p.is_file() and p!=out/'manifest.json':
            files[p.relative_to(root).as_posix()]=dict(bytes=p.stat().st_size,sha256=sha(p))
    manifest=dict(schema='T047-manifest-checkpoint-v1',status='INCOMPLETE_STOP_C1',
                  git_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
                  src_base='c298188e',src_unchanged=True,scoring_labels_read=False,task_complete=False,
                  phase1=phases,outputs=files,source_manifests={f'T-{s}':sha(root/f'results/T-{s}/manifest.json') for s in ('043','044','045','046')},
                  integrity_check=str((audit/'kiem-ban-giao.json').relative_to(root)),
                  note='Manifest ở điểm dừng; helper/test PASS không thay T1 đang trượt. Candidate chưa áp dụng. Giữ các lượt hỏng.')
    ad.ghi(out/'manifest.json',manifest)
    print(json.dumps(dict(integrity_PASS=result['integrity_PASS'],task_PASS=False,files=len(files),
                         used_minutes=used/60,remaining_minutes=(budget['cap_seconds']-used)/60)))
    if not result['integrity_PASS']:raise SystemExit('bàn giao chưa hợp lệ; xem checks')


if __name__=='__main__':main()
