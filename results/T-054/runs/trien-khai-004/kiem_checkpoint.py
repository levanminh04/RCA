"""Kiểm chỉ đọc checkpoint004. Không khôi phục byte lịch sử khi nguồn đã đổi."""
import argparse
import ast
import hashlib
import json
import sys
import tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import read_pin,ref,digest,fingerprint,Blocked
from dieu_phoi import status,verify_attempt

def load(p):return json.loads(Path(p).read_bytes())
def same(path,pin):
    assert path.is_file(),str(path)
    assert digest(path)==pin['sha256'],str(path)
    if 'bytes'in pin:assert path.stat().st_size==pin['bytes'],str(path)

def validate():
    before=load(RUN/'before.json');changed=[]
    allowed={'docs/STATE.md','tasks/T-054-khoa-g3-chay-p7-a/LOG.md','tasks/T-054-khoa-g3-chay-p7-a/SPEC.md'}
    allowed|={'results/T-054/'+n for n in ['authorization.json','environment.json','ho-so-g3.md','pilot-plan.json',
      'protocol.json','reuse.json','runbook.md','source-manifest.json']}
    allowed|={'results/T-054/scripts/'+n+'.py'for n in ['bien_nhan','cham','dieu_phoi','nguon','p7','pilot','worker']}
    for rel,pin in before.items():
        p=ROOT/rel;assert p.is_file(),rel
        if digest(p)!=pin['sha256']:
            assert rel in allowed,rel;changed.append(rel)
        else:same(p,pin)
    assert set(changed)==allowed
    prefix=(RUN/'before-files/tasks/T-054-khoa-g3-chay-p7-a/LOG.md').read_bytes()
    assert (ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').read_bytes().startswith(prefix)
    def state_others(raw):return b''.join(x for x in raw.splitlines(keepends=True)if not x.startswith('- **T-054'.encode()))
    assert state_others((ROOT/'docs/STATE.md').read_bytes())==state_others((RUN/'before-files/docs/STATE.md').read_bytes())
    source=load(OUT/'source-manifest.json');assert len(source['own_scripts'])==9
    for rel,pin in source['own_scripts'].items():
        same(ROOT/rel,pin);ast.parse((ROOT/rel).read_text(encoding='utf-8'))
    for rel,pin in source['legacy_code'].items():same(ROOT/rel,{'sha256':pin}if isinstance(pin,str)else pin)
    assert len(source['legacy_code'])==93
    p=load(OUT/'protocol.json');old=load(RUN/'before-files/results/T-054/protocol.json')
    scientific=['C_e','Cd3','a4_record_contract','configurations','effective_config','ranking','regions','window']
    for key in scientific:assert p[key]==old[key],key
    assert p['status']=='CANDIDATE_NOT_LOCKED'and p['real_execution_ready']is False
    assert p['A4']['case_permutation']['status']=='USER_CONFIRMED_SENSITIVITY_ONLY'
    assert p['A4']['error_excluded']['status']=='USER_CONFIRMED_SENSITIVITY_ONLY'
    contract=read_pin(p['dispatch_contract_ref'])
    assert contract['code_pins']==p['source_code']
    for rel,pin in source['own_scripts'].items():assert contract['code_pins'][rel]==pin['sha256']
    assert contract['budget']['mode']=='UNTIL_COHORT_COMPLETE'and contract['budget']['wall_s']is None
    assert contract['budget']['method_dataset_s']=={}and contract['workers']==2
    auth=load(OUT/'authorization.json')
    assert all(auth.get(k)is False for k in ['g3','test_grant','RE3_telemetry','commit_push'])
    assert auth['stop_before_main']is True
    for f in ['operational-checks.json','final2-branch-checks.json','sensitivity-checks.json',
              'C-e-support-checks.json','failure-report-checks.json','locked-plan-contract-checks.json']:
        assert load(RUN/f)['PASS']is True,f
    assert load(RUN/'regression-transport-003/summary.json')['PASS']is True
    new=load(RUN/'pilot-2-worker-001/summary.json');assert new['PASS']and new['slots']==2
    assert all(r['exact_all_comparable_fields']for r in new['rows'])
    assert new['C_e_real_route_verified']and not new['clock_anomaly']
    plan=load(RUN/'pilot-2-worker-001/plan.json');st=status(RUN/'pilot-2-worker-001/queue')
    assert st['controller']is None and len(st['jobs'])==2
    for j in plan['jobs']:
        r=st['jobs'][fingerprint(j['slot'])];assert r['state']=='VERIFIED'
        record,=verify_attempt(Path(r['attempt']),j,r['token']);assert record['status']=='OK'
        for cp in (RUN/'pilot-2-worker-001/code').glob('*.py'):
            assert digest(cp)==j['code_pins']['results/T-054/scripts/'+cp.name]
    total=0
    for name in ['pilot-local-007','pilot-local-008']:
        d=OUT/'runs/trien-khai-003'/name;plan=load(d/'plan.json');st=status(d/'queue')
        assert st['controller']is None
        for j in plan['jobs']:
            r=st['jobs'][fingerprint(j['slot'])];assert r['state']=='VERIFIED'
            verify_attempt(Path(r['attempt']),j,r['token']);total+=1
    assert total==40
    freeze=OUT/'runs/freeze-cong-cu-006';files=load(freeze/'files.json')['files']
    for rel,pin in files.items():same(ROOT/rel,pin);same(freeze/'code'/rel,pin)
    with tarfile.open(freeze/'code.tar.gz','r:gz')as archive:
        assert set(archive.getnames())==set(files)
        for m in archive.getmembers():assert m.isfile()and hashlib.sha256(archive.extractfile(m).read()).hexdigest()==files[m.name]['sha256']
    assert load(freeze/'package.json')['G3']is False
    import psutil
    owned=[]
    for proc in psutil.process_iter(['pid','cmdline']):
        try:
            args=[x.replace('\\','/')for x in proc.info['cmdline']or[]]
            if (any('/T-054/'in x and x.endswith('/worker.py')for x in args)
                    or any(x.endswith('/T-054/scripts/p7.py')for x in args)and'_supervise'in args):owned.append(proc.pid)
        except(psutil.AccessDenied,psutil.NoSuchProcess):pass
    assert not owned,owned
    return dict(PASS=True,scope='integrity/contracts/operational checks; not G3 or research acceptance',
      before_files_checked=len(before),changed_existing_files=changed,protected_existing_files_preserved=len(before)-len(changed),
      LOG_append_only=True,STATE_only_T054_row=True,own_scripts_AST=9,legacy_code_pins=93,
      retained_DEV_slots=40,new_targeted_DEV_slots=2,new_broad_baseline_runs=0,real_packet_elapsed_s=new['elapsed_s'],
      scientific_fields_preserved=scientific,freeze_files_exact=len(files),live_owned_processes=owned,
      G3=False,test_opened=False,main_started=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--manifest');args=parser.parse_args()
    result=validate()
    if args.manifest:
        m=load(ROOT/args.manifest)
        for rel,pin in m['outputs'].items():same(ROOT/rel,pin)
        result['manifest_outputs_verified']=len(m['outputs'])
    else:
        from bien_nhan import atomic
        atomic(RUN/'validation.json',result)
    print(json.dumps(result,ensure_ascii=False))
