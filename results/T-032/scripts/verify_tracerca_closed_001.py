"""Recheck closed approved pilots; no RCA/native call or numerical tolerance."""
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import psutil

BASE = Path('/home/ubuntu/rca/T-032')
RUN = BASE / 'runs/tracerca-path-pilots-002'
OUT = BASE / 'runs/tracerca-pilots-root-001'
CONTROLLER_SHA = '136e76e69993b502c28ac18b7a3ab8e1a81b8bb5eac4e97ce413952e3a96d466'
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name, value):
    with (OUT/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False); f.write('\n')
def inventory(roots):
    result=[]
    for root in roots:
        for p in sorted(root.rglob('*')) if root.is_dir() else [root]:
            assert not p.is_symlink(), str(p)
            if p.is_file(): result.append({'path':p.relative_to(BASE).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    assert len({x['path'] for x in result})==len(result)
    return result
assert sha(BASE/'scripts/run_tracerca_path_pilots_v2.py')==CONTROLLER_SHA
import run_tracerca_path_pilots_v2 as c
import replay_tracerca_v3 as r
state=read(RUN/'status.json')
monitor=read(BASE/'runs/tracerca-dtype-pilots-002-monitor/status.json')
assert state['status']=='PASS_DTYPE_FIXTURE_ERROR_AUDIT_AND_TWO_PILOTS'
assert monitor['status']=='PASS' and monitor['exit_code']==0
assert not state['cohort_authorized'] and state['active'] is None
pids=[state['pid'],monitor['supervisor_pid']]+[x['cost']['pid'] for x in state['completed']]
assert all(not psutil.pid_exists(pid) for pid in pids), pids
others=[]
for p in psutil.process_iter(['pid','cmdline']):
    try:
        cmd=p.info['cmdline'] or []
        if p.pid!=os.getpid() and cmd and Path(cmd[0]).name.startswith('python') and any('/rca/T-032/scripts/' in x for x in cmd): others.append(p.info)
    except (psutil.NoSuchProcess,psutil.AccessDenied): pass
assert not others, others
assert not OUT.exists()
OUT.mkdir()
roots=[RUN,BASE/'runs/tracerca-dtype-pilots-002-monitor']+[BASE/('runs/tracerca-dtype-pilots-002-launcher.'+x) for x in ('out','err','pid')]
before=inventory(roots)
validated=[]
for phase,pilot in [('posthoc',None),('fixture',None)]+[(x[0],x) for x in c.PILOTS]:
    verdict=c.validate_child(RUN/phase,phase,pilot)
    stored=next(x for x in state['completed'] if x['phase']==phase)
    assert all(verdict[k]==stored[k] for k in verdict)
    validated.append(verdict)
records=[]
for name,dataset,case,_status,_sha in c.PILOTS:
    audit=[]
    entry,frozen,_index,_pins=r.source_for(dataset,case,audit)
    actual=r.read(RUN/name/'ban-ghi-0.json')
    assert not r.compare_records(frozen,actual)
    assert frozen['status']==actual['status']=='OK'
    records.append({'phase':name,'record_exact':True,'frozen_path':entry['path'],'frozen_sha256':entry['sha256'],'source_rechecked':audit,'check_sha256':sha(RUN/name/'check.json'),'cost':read(RUN/name/'cost.json')})
after=inventory(roots)
assert before==after,'closed run changed during verification'
save('closed-inventory.json',{'status':'CLOSED_FULL_HASH_INVENTORY','base':str(BASE),'roots':[str(x) for x in roots],'files':before,'file_count':len(before),'bytes':sum(x['bytes'] for x in before),'terminal_files_and_streams_included':True})
save('check.json',{'status':'PASS_CLOSED_PILOTS_ROOT_VERIFY','time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'closed_inventory_sha256':sha(OUT/'closed-inventory.json'),'controller_sha256':CONTROLLER_SHA,'verifier_sha256':sha(Path(__file__)),'pids_gone':pids,'no_other_heavy_T032_worker':True,'closed_bytes_stable':True,'validated_children':validated,'exact_frozen_records':records,'monitor':monitor,'controller':state,'methods_executed':False,'full_capture_formulas_recomputed_here':False,'full_capture_formulas_verified_at_pilot':True,'cohort_started':False,'mechanism_claim':False})
save('manifest.json',{'files':inventory([OUT]),'excluded':['manifest.json']})
print(json.dumps({'status':'PASS_CLOSED_PILOTS_ROOT_VERIFY','file_count':len(before),'closed_bytes':sum(x['bytes'] for x in before),'output':str(OUT)}))
