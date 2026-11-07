"""Chỉ đọc checkpoint006: bảo toàn và trạng thái thật, không tự sửa/chạy."""
from pathlib import Path
import sys,json,ast,argparse,hashlib,tarfile,collections
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path[:0]=[str(OUT/'scripts'),str(ROOT/'src')]
from bien_nhan import *
from nguon import compare_sources,placement_key
from p7 import load_plan
def load(p):return json.loads(Path(p).read_bytes())
def same(path,pin):
    path=Path(path);assert path.is_file(),str(path)
    assert digest(path)==pin['sha256'],str(path)
    if 'bytes'in pin:assert path.stat().st_size==pin['bytes'],str(path)
def validate():
    old=load(OUT/'manifest-trien-khai-005.json');allowed={'docs/STATE.md','tasks/T-054-khoa-g3-chay-p7-a/LOG.md'}|{'results/T-054/'+s for s in ['authorization.json','source-manifest.json','ho-so-g3.md','runbook.md']}
    changed=[];protected=0
    for rel,pin in old['outputs'].items():
        if rel in allowed:
            if digest(ROOT/rel)!=pin['sha256']:changed.append(rel)
        else:same(ROOT/rel,pin);protected+=1
    assert set(changed)==allowed
    before=load(RUN/'before.json')
    for rel,pin in before.items():same(RUN/'before'/rel,pin)
    logrel='tasks/T-054-khoa-g3-chay-p7-a/LOG.md';assert (ROOT/logrel).read_bytes().startswith((RUN/'before'/logrel).read_bytes())
    def others(raw):return b''.join(x for x in raw.splitlines(keepends=True)if not x.startswith('- **T-054'.encode()))
    assert others((ROOT/'docs/STATE.md').read_bytes())==others((RUN/'before/docs/STATE.md').read_bytes())
    p=load(OUT/'protocol.json');same(OUT/'protocol.json',before['results/T-054/protocol.json']);assert p['status']=='CANDIDATE_NOT_LOCKED'
    for rel,sha in p['source_code'].items():assert digest(ROOT/rel)==sha,rel
    for path in (OUT/'scripts').glob('*.py'):ast.parse(path.read_text(encoding='utf-8'))
    for path in RUN.glob('*.py'):ast.parse(path.read_text(encoding='utf-8'))
    source=read_pin(ref(RUN/'checkpoint-01-sources.json'));plans=read_pin(ref(RUN/'checkpoint-01-plans.json'));contract=read_pin(p['dispatch_contract_ref']);placement=read_pin(contract['partition_ref'])
    for ds,refpin in source['runtime_refs'].items():
        runtime=read_pin(refpin);ind=read_pin(source['independent_source_refs'][ds]);compare_sources(runtime,ind,ds,runtime['g1_revision'])
        cohort=read_pin(p['cohorts_source']);assert len(runtime['cases'])==cohort['cohorts'][ds]['n']
        assert {r['member_sha256']for r in runtime['cases'].values()}==set(cohort['cohorts'][ds]['members_locked_sha256'])
    for path,pin in load(RUN/'private-artifact-pins.json').items():same(path,pin)
    allkeys=[];jobcounts={}
    for host,pin in plans['plan_refs'].items():
        path=Path(pin['path']);path=path if path.is_absolute()else ROOT/path
        plan=load_plan(str(path),pin['sha256']);assert plan['preparation_only']and plan['open_before_run']
        authority=read_pin(plans['authority_refs'][host]);assert not authority['g3']and not authority['main_dispatch']
        keys=[placement_key(j['slot'])for j in plan['jobs']]+[placement_key(dict(r,arm='M1',view='ce',seed=None))for r in plan['ce_support']]
        assert len(keys)==len(set(keys))and set(keys)==set(placement['hosts'][host])
        assert all(j['protocol_ref']['sha256']==before['results/T-054/protocol.json']['sha256']for j in plan['jobs'])
        allkeys+=keys;jobcounts[host]=len(plan['jobs'])
    assert len(allkeys)==len(set(allkeys))==1642 and jobcounts=={'ec2_1':358,'ec2_2':360,'local':922}
    transfer=load(RUN/'checkpoint-02-transfer.json');assert transfer['PASS']and transfer['files']==180 and transfer['bytes']==1309388082
    for host in ['ec2_1','ec2_2']:
        receipt=load(RUN/(host+'-TT-transfer.json'));assert receipt['exit']==0;remote=json.loads(receipt['stdout']);assert remote['PASS']and remote['files']==90
        for rel,pin in remote['files_verified'].items():same(ROOT/rel,pin)
        check=load(RUN/(host+'-preflight.json'));assert check['exit']==0;detail=json.loads(check['stdout']);assert detail['exit']==0
        inner=json.loads(detail['stdout']);assert inner['PASS']and inner['main_guard_denial']=='WAIT_G3'and inner['code_pins']==103
        # Byte source of staged packet independently preserved; no check against later mutable report metadata.
        staged=load(RUN/(host+'-staged-files.json'))
        with tarfile.open(RUN/(host+'-code-and-prepared.tar.gz'))as t:
            assert set(t.getnames())==set(staged)
            for m in t.getmembers():assert m.isfile()and hashlib.sha256(t.extractfile(m).read()).hexdigest()==staged[m.name]['sha256']
    local=load(RUN/'local-preflight.json');assert local['exit']==0 and json.loads(local['stdout'])['main_guard_denial']=='WAIT_G3'
    # Known source failure must stay visible; PASS here means faithful checkpoint, not main readiness.
    ob=load(RUN/'OB-metric-time-window-check.json');assert ob['PASS']is False and len(ob['issues'])==30
    assert len({r['opaque_id']for r in ob['issues']})==4
    assert load(RUN/'OB-source-blocker.json')['status']=='BLOCKS_MAIN_WITH_CURRENT_READER'
    audit=load(RUN/'source-temporal-final-check.json');assert audit['PASS']and audit['Ce_history_status_unchanged']
    assert audit['Ce_log_H_rounding_differences']==audit['Ce_log_boundary_bin_differences']==[]
    assert audit['A_zero_side_tables']==[{'opaque_id':'test-541642b59e','table':'logts','N':0,'A':41}]
    bundle=load(RUN/'source-bundle-final-prepared.json');assert bundle['open_before_run']
    assert load(RUN/'activation-source-blocked.json')['source_blocker_rejected_before_lock']
    assert load(RUN/'activation-preparation-denied.json')['preparation_cannot_activate']
    assert not(RUN/'activated-001').exists()
    assert not(OUT/'runs/main-005/queue').exists()
    for host in ['ec2_1','ec2_2']:
        final=load(RUN/(host+'-final-idle.json'));assert final['exit']==0 and not json.loads(final['stdout'])['live_T054']
    auth=load(OUT/'authorization.json');assert auth['source_preparation_completed']and not auth['g3']and not auth['main_dispatch']
    return dict(PASS=True,meaning='Checkpoint integrity and disclosed blockers verified; NOT main readiness',protected_005_outputs=protected,changed_existing_files=changed,
        scientific_worker_code_pins_unchanged=103,LOG_append_only=True,STATE_only_T054=True,
        TT_transfer_files=180,TT_transfer_bytes=1309388082,source_cases={'TT':60,'OB':34},A_CSV=180,A_CSV_bytes=9244910,
        planned_jobs=jobcounts,positions=1642,Ce_verified=58,Ce_insufficient=2,
        machine_hash_environment_placement_preflight='PASS',OB_actual_window_contract='BLOCKED_4_CASES_30_CASE_SOURCES',A_auxiliary_empty_normal_logts_cases=1,
        main_readiness=False,src_changed=False,G3=False,main_started=False,RE3_opened=False,commit_push=False)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest');args=ap.parse_args();result=validate()
    if args.manifest:
        m=load(ROOT/args.manifest)
        for rel,pin in m['outputs'].items():same(ROOT/rel,pin)
        result['manifest_outputs_verified']=len(m['outputs'])
    else:atomic(RUN/'validation.json',result)
    print(json.dumps(result,ensure_ascii=False))
