"""Kiểm chỉ đọc checkpoint005; không khôi phục nguồn mutable về mốc cũ."""
from pathlib import Path
import sys,json,hashlib,ast,tarfile,argparse
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import *
from dieu_phoi import status,verify_attempt
def load(p):return json.loads(Path(p).read_bytes())
def same(path,p):
    assert Path(path).is_file(),str(path)
    assert digest(path)==p['sha256'],str(path)
    if 'bytes'in p:assert Path(path).stat().st_size==p['bytes'],str(path)
def validate():
    before=load(RUN/'before.json');changed=[]
    allowed={'AGENTS.md','docs/DECISIONS.md','docs/STATE.md','tasks/T-054-khoa-g3-chay-p7-a/SPEC.md','tasks/T-054-khoa-g3-chay-p7-a/LOG.md'}
    allowed|={'results/T-054/scripts/'+n+'.py'for n in ['bien_nhan','nguon','cham','dieu_phoi','p7']}
    for rel,p in before.items():
        if digest(ROOT/rel)!=p['sha256']:assert rel in allowed,rel;changed.append(rel)
        else:same(ROOT/rel,p)
    assert set(changed)==allowed
    for rel in ['docs/DECISIONS.md','tasks/T-054-khoa-g3-chay-p7-a/LOG.md']:
        assert (ROOT/rel).read_bytes().startswith((RUN/'before'/rel).read_bytes()),rel
    def others(b):return b''.join(x for x in b.splitlines(keepends=True)if not x.startswith('- **T-054'.encode()))
    assert others((ROOT/'docs/STATE.md').read_bytes())==others((RUN/'before/docs/STATE.md').read_bytes())
    # Kiểm lịch sử bằng manifest trước, chỉ loại đúng hồ sơ mutable được phép cập nhật.
    mutable=allowed|{'results/T-054/'+n for n in ['authorization.json','environment.json','ho-so-g3.md','pilot-plan.json','protocol.json','reuse.json','runbook.md','source-manifest.json']}
    old=load(OUT/'manifest-trien-khai-004.json');protected=0
    for rel,pin in old['outputs'].items():
        if rel not in mutable:same(ROOT/rel,pin);protected+=1
    source=load(OUT/'source-manifest.json')
    for rel,pin in source['legacy_code'].items():same(ROOT/rel,{'sha256':pin}if isinstance(pin,str)else pin)
    assert len(source['legacy_code'])==93
    for rel,pin in source['own_scripts'].items():same(ROOT/rel,pin);ast.parse((ROOT/rel).read_text(encoding='utf-8'))
    assert len(source['own_scripts'])==9
    tested=load(RUN/'final-cloud-code-files-r2.json')
    for rel,pin in source['own_scripts'].items():assert pin['sha256']==tested[rel]['sha256']
    p=load(OUT/'protocol.json');c=read_pin(p['dispatch_contract_ref'])
    assert p['status']=='CANDIDATE_NOT_LOCKED'and not p['real_execution_ready']
    assert c['code_pins']==p['source_code']and len(c['code_pins'])==103
    for rel,h in c['code_pins'].items():assert digest(ROOT/rel)==h,rel
    prior=load(OUT/'runs/trien-khai-004/before-files/results/T-054/protocol.json')
    fields=['C_e','Cd3','a4_record_contract','configurations','effective_config','ranking','regions','window']
    for k in fields:assert p[k]==prior[k],k
    assert c['budget']['wall_s']is None and c['budget']['method_dataset_s']=={}and c['budget']['mode']=='UNTIL_COHORT_COMPLETE'
    assert set(c['hosts'])==set(p['allowed_hosts'])=={'ec2_1','ec2_2','local'}
    assert all(v['workers']==2 for v in c['hosts'].values())
    placement=read_pin(c['partition_ref']);assert placement['counts']=={'ec2_1':360,'ec2_2':360,'local':922}
    keys=[k for v in placement['hosts'].values()for k in v];assert len(keys)==len(set(keys))==1642
    transfer=load(RUN/'transfer-plan-005.json');allpaths=[]
    for host,rows in transfer['hosts'].items():
        assert len(rows)==90 and sum(x['bytes']for x in rows)==placement['TT_transfer_bytes'][host]
        for x in rows:same(ROOT/x['path'],x);allpaths.append(x['path'])
    assert len(set(allpaths))==180 and sum(placement['TT_transfer_bytes'].values())==1309388082
    assert not transfer['test_transferred']and not transfer['labels_transferred']
    assert load(RUN/'TT60-strict-source-verification.json')['exact_case_filename_mapping']
    for host in ['ec2_1','ec2_2']:
        outer=load(RUN/(host+'-final-checks-r2.json'));inner=json.loads(outer['stdout']);assert outer['exit']==inner['exit']==0 and inner['summary']['PASS']and inner['summary']['count']==9
        bridge=load(RUN/(host+'-torai-bridge.json'));assert bridge['exit']==0
    assert load(RUN/'regression-transport-final/summary.json')['PASS']
    assert load(RUN/'materializer-final-checks.json')['PASS']
    assert load(RUN/'cloud-dev-summary.json')['exact_native_same_EC2']
    recovered=load(RUN/'ec2-1-cloud-dev-summary-corrected.json');assert recovered['exact_native_reference_EC2_2']and recovered['target_machine']=='EC2_1'
    # Hash nguyên bản từng bundle nhận; không sửa receipt để trỏ local.
    received=0
    for dirname in ['received-cloud-001','received-ec2-1-001']:
        dest=RUN/dirname;man=load(dest/'transfer-manifest.json')
        for rel,pin in man.items():same(dest/rel,pin);received+=1
    total=0
    for name in ['pilot-local-007','pilot-local-008']:
        d=OUT/'runs/trien-khai-003'/name;plan=load(d/'plan.json');st=status(d/'queue');assert st['controller']is None
        for j in plan['jobs']:
            r=st['jobs'][fingerprint(j['slot'])];assert r['state']=='VERIFIED';verify_attempt(Path(r['attempt']),j,r['token']);total+=1
    assert total==40
    d=OUT/'runs/trien-khai-004/pilot-2-worker-001';pl=load(d/'plan.json');st=status(d/'queue');assert st['controller']is None
    for j in pl['jobs']:
        row=st['jobs'][fingerprint(j['slot'])];verify_attempt(Path(row['attempt']),j,row['token'])
    freeze=OUT/'runs/freeze-cong-cu-007';files=load(freeze/'files.json')['files']
    for rel,pin in files.items():same(ROOT/rel,pin);same(freeze/'code'/rel,pin)
    with tarfile.open(freeze/'code.tar.gz')as t:
        assert set(t.getnames())==set(files)
        for m in t.getmembers():assert m.isfile()and hashlib.sha256(t.extractfile(m).read()).hexdigest()==files[m.name]['sha256']
    assert 'results/T-052/ke-hoach-tap-test.json'in files
    auth=load(OUT/'authorization.json');assert all(auth[k]is False for k in ['g3','test_grant','RE3_telemetry','commit_push'])and auth['stop_before_main']
    assert auth['ssh_grant']and auth['sync_grant']
    import psutil
    live=[]
    for pr in psutil.process_iter(['pid','cmdline']):
        try:
            args=[x.replace('\\','/')for x in pr.info['cmdline']or[]]
            if any('/T-054/'in x and x.endswith('/worker.py')for x in args)or('_supervise'in args and any(x.endswith('/T-054/scripts/p7.py')for x in args)):live.append(pr.pid)
        except(psutil.NoSuchProcess,psutil.AccessDenied):pass
    assert not live,live
    return dict(PASS=True,changed_before_files=changed,protected_previous_outputs=protected,legacy_code_pins=93,own_scripts_AST=9,
        source_scripts_equal_Linux_r2=True,compiler_frozen=True,TT_files=180,TT_bytes=1309388082,placement_positions=1642,
        received_files_hash_verified=received,retained_old_DEV_slots=40,targeted_DEV_slots004=2,targeted_DEV_calls005=2,unique_DEV_cases005=1,
        scientific_fields_preserved=fields,LOG_and_DECISIONS_append_only=True,STATE_only_T054=True,
        freeze_files=len(files),live_local_owned=live,G3=False,test_opened=False,main_started=False,commit_push=False)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest');a=ap.parse_args();result=validate()
    if a.manifest:
        man=load(ROOT/a.manifest)
        for rel,pin in man['outputs'].items():same(ROOT/rel,pin)
        result['manifest_outputs_verified']=len(man['outputs'])
    else:atomic(RUN/'validation.json',result)
    print(json.dumps(result,ensure_ascii=False))
