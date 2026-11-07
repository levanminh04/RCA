"""Danh sách nguồn thật ở trạng thái chuẩn bị; không giả LOCKED_G3 hay phát job."""
from pathlib import Path
import sys,copy,csv,json,collections,shutil
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(OUT/'scripts'),str(ROOT/'src')]
from bien_nhan import *
from nguon import compare_sources,compare_labels,placement_key,validate_slot
from p3 import nezha
from p7 import load_plan
PRIVATE=Path('D:/RCA-ext/private/T-054/prepare-main-006')
def pin(path):
    r=ref(path)
    if Path(path).resolve().is_relative_to(ROOT):r['path']=Path(path).resolve().relative_to(ROOT).as_posix()
    return r
def copied(reference,name):
    b=Path(reference['path']).read_bytes();assert __import__('hashlib').sha256(b).hexdigest()==reference['sha256']
    dest=RUN/'runtime-TT'/name;dest.parent.mkdir(exist_ok=True)
    with dest.open('xb')as f:f.write(b)
    return pin(dest)
def main():
    sources=read_pin(pin(RUN/'checkpoint-01-sources.json'));p=read_pin(pin(OUT/'protocol.json'));c=read_pin(p['dispatch_contract_ref']);placement=read_pin(c['partition_ref'])
    assert p['status']=='CANDIDATE_NOT_LOCKED'
    runtimes={ds:read_pin(r)for ds,r in sources['runtime_refs'].items()}
    for ds,rt in runtimes.items():compare_sources(rt,read_pin(sources['independent_source_refs'][ds]),ds,rt['g1_revision'])
    runtime_refs=dict(sources['runtime_refs']);original_refs=dict(sources['independent_source_refs']);binding_refs=dict(sources['preparation_binding_refs'])
    for target,original,name in [(runtime_refs,sources['runtime_refs'],'runtime'),(original_refs,sources['independent_source_refs'],'independent-source'),(binding_refs,sources['preparation_binding_refs'],'preparation-binding')]:
        target['RE2-TT']=copied(original['RE2-TT'],'TT-'+name+'.json')
    # Nguồn evaluator riêng; chỉ dựng metadata từ G1, không có ranking để ghép/chấm.
    cohort=read_pin(p['cohorts_source']);g1=cohort['G1_source'];assert digest(ROOT/g1['path'])==g1['sha256']
    split=list(csv.DictReader((ROOT/g1['path']).open(encoding='utf-8-sig')))
    aliases={'RE2-TT':{},'Nezha-OB':dict(nezha.POD_ALIASES)};labels={};canonical={}
    for ds,rt in runtimes.items():
        by_member={}
        for r in split:
            if r['dataset']!=ds or r['vai_tro']!='test':continue
            member=fingerprint([ds,r['case']]);root=aliases[ds].get(r['root'],r['root']);assert root in rt['inventory']
            by_member[member]=dict(member_sha256=member,root=root,fault=r['fault'],cell=[ds,root,r['fault']])
        lab=dict(dataset=ds,g1_revision=g1['sha256'],alias_sha256=fingerprint(aliases[ds]),cases={oid:by_member[row['member_sha256']]for oid,row in rt['cases'].items()})
        canon=dict(dataset=ds,g1_revision=g1['sha256'],alias_sha256=fingerprint(aliases[ds]),by_member=by_member,source= g1)
        assert len(compare_labels(lab,canon,rt,aliases[ds],rt['inventory']))==len(rt['cases'])
        prefix='TT'if ds=='RE2-TT'else'OB';labels[ds]=atomic(PRIVATE/(prefix+'-evaluator-labels.json'),lab);canonical[ds]=atomic(PRIVATE/(prefix+'-canonical-label-source.json'),canon)
    old=read_pin(pin(OUT/'runs/trien-khai-003/pilot-local-007/plan.json'))
    baseline={j['slot']['arm']:j['config']for j in old['jobs']if j['kind']in ('baseline','torai_pipeline')}
    for arm,cfg in baseline.items():assert fingerprint(cfg)==c['baseline_config_sha256'][arm]
    assert set(baseline)==set(c['baseline_config_sha256'])
    jobs={h:[]for h in placement['hosts']};support={h:[]for h in jobs};parents={}
    for item in placement['slots']:
        ds,oid,arm,view,h=(item[k]for k in ['dataset','opaque_id','arm','view','host']);rt=runtimes[ds];row=rt['cases'][oid];hc=dict(c,**c['hosts'][h]);env=hc['environment_sha256']
        if view=='ce'and row['ce_history']=='insufficient':
            support[h].append(dict(dataset=ds,opaque_id=oid,status='INSUFFICIENT_EVIDENCE',source_sha256=fingerprint(row)));continue
        t=row.get('t',row.get('t_ns',0)//10**9)-(300 if view=='ce'else 0)
        family=arm in p['configurations'];torai=ds=='RE2-TT'and arm in ('torai_A','torai_B')
        cfg=p['configurations'][arm]['config']if family else {'cd3':'same sealed M1'}if arm=='C-d3'else baseline[arm]
        slot=dict(dataset=ds,opaque_id=oid,member_sha256=row['member_sha256'],arm=arm,view=view,seed=item.get('seed'),window={'t':t,'half_width_s':300},source_sha256=fingerprint(row),config_sha256=fingerprint(cfg),environment_sha256=env['py38'if torai else'main'])
        j=dict(slot=slot,kind='m1'if family else'cd3'if arm=='C-d3'else'torai_pipeline'if torai else'baseline',evaluation_mode='test',source=row,data_root=hc['data_root'],t=t,
            inventory=rt['inventory'],runtime_ref=runtime_refs[ds],independent_source_ref=original_refs[ds],runtime_binding_ref=binding_refs[ds],g1_revision=rt['g1_revision'],protocol_ref=pin(OUT/'protocol.json'),
            pythonpath=hc['pythonpath'],executable=hc['executable'],prep_executable=hc['prep_executable'],method_executable=hc['method_executable'],prep_environment_sha256=env['main'],
            code_pins=hc['code_pins'],config=copy.deepcopy(cfg),m1_contract=p['m1_contract_ref'],static_snapshot=p['snapshots'][ds],method_version='P3 frozen adapter; T054 candidate',
            timeout_s=hc['timeout_s']['C-d3'if arm=='C-d3'else'main_slot'],failure_policy_ref=c['failure_policy_candidate_ref'],a4=item.get('a4',False))
        if arm=='torai_A':j['author_source_ref']=sources['author_source_ref'];slot['author_source_sha256']=sources['author_source_ref']['sha256']
        if arm=='C-d3':
            parent=parents[(ds,oid)];j['main_dependency']={'slot':parent['slot'],'job_sha256':fingerprint(parent)}
        if arm=='M1'and view=='main':parents[(ds,oid)]=j
        validate_slot(slot,{'mode':'test'});jobs[h].append(j)
    dest=RUN/'prepared';dest.mkdir(exist_ok=False);plan_refs={};authorities={};counts={}
    waits=['WAIT_MINH_G3_AND_MAIN_DISPATCH','FINAL_G3_RUNTIME_ATTESTATION_AND_LOCKED_POLICY']
    for h,rows in jobs.items():
        hc=dict(c,**c['hosts'][h]);got=[placement_key(j['slot'])for j in rows]+[placement_key(dict(x,arm='M1',view='ce',seed=None))for x in support[h]]
        assert len(got)==len(set(got))and set(got)==set(placement['hosts'][h])
        for j in rows:
            assert j['code_pins']==p['source_code']and j['protocol_ref']==pin(OUT/'protocol.json')
            assert j['slot']['config_sha256']==fingerprint(j['config'])
            assert j['slot']['environment_sha256']==hc['environment_sha256']['py38'if j['kind']=='torai_pipeline'else'main']
        plan=dict(schema='T054-PLAN-1',mode='test',preparation_only=True,host_role=h,workers=hc['workers'],resources=hc['resources'],jobs=rows,ce_support=support[h],
            directory=hc['code_root']+'/results/T-054/runs/main-005/queue',inventories={ds:rt['inventory']for ds,rt in runtimes.items()},protocol_ref=pin(OUT/'protocol.json'),
            monitor=hc['monitor'],budget=hc['budget'],sensitivity_decision_ref=hc['sensitivity_decision_ref'],open_before_run=waits)
        path=dest/(h+'-plan.json');atomic(path,plan);r=pin(path);load_plan(str(path),r['sha256']);plan_refs[h]=r
        a=dict(schema='T054-AUTHORITY-1',source=pin(RUN/'quyen-minh.txt'),plan_sha256=fingerprint(plan),g3=False,test_grant=False,main_dispatch=False,
            preparation_grant_ref=pin(RUN/'preparation-grant.json'),torai_A_source_grant=True,torai_A_source_sha256=sources['author_source_ref']['sha256'],stop_before_main=True)
        ap=dest/(h+'-authority.json');atomic(ap,a);authorities[h]=pin(ap)
        counts[h]=dict(positions=len(got),jobs=len(rows),Ce_insufficient=len(support[h]),arms=dict(collections.Counter(j['slot']['arm']for j in rows)),case_ids=sorted({j['slot']['opaque_id']for j in rows if j['slot']['dataset']=='RE2-TT'}))
    evaluation=dict(runtime_refs=runtime_refs,labels=labels,canonical_labels=canonical,aliases=aliases,output=str(OUT/'reports/main-006'))
    aggregate=dict(schema='T054-PLAN-1',mode='test',preparation_only=True,host_role='aggregate',workers=1,jobs=[j for rows in jobs.values()for j in rows],ce_support=[x for rows in support.values()for x in rows],
        directory=str(dest/'aggregate-queue'),inventories={ds:rt['inventory']for ds,rt in runtimes.items()},protocol_ref=pin(OUT/'protocol.json'),execution_plan_refs=list(plan_refs.values()),evaluation=evaluation,
        monitor=c['monitor'],budget=c['budget'],sensitivity_decision_ref=c['sensitivity_decision_ref'],open_before_run=waits)
    atomic(dest/'aggregate-plan.json',aggregate)
    from cham import validate_ce_plan
    validate_ce_plan(aggregate,runtimes['RE2-TT'])
    total=[placement_key(j['slot'])for j in aggregate['jobs']]+[placement_key(dict(x,arm='M1',view='ce',seed=None))for x in aggregate['ce_support']]
    assert len(total)==len(set(total))==1642 and len(aggregate['jobs'])==1640 and len(aggregate['ce_support'])==2
    atomic(RUN/'source-bundle-prepared.json',dict(runtime_refs=runtime_refs,independent_source_refs=original_refs,runtime_binding_refs=binding_refs,
        hosts={h:{'main_executable':c['hosts'][h]['executable'],'py38_executable':c['hosts'][h]['method_executable'],'pythonpath':c['hosts'][h]['pythonpath']}for h in jobs},
        baseline_configs=baseline,m1_contract=p['m1_contract_ref'],failure_policy_ref=c['failure_policy_candidate_ref'],author_source_ref=sources['author_source_ref'],evaluation=evaluation,
        note='Prepared only; after G3 replace preparation bindings with attest_runtime against locked protocol and lock approved failure policy; no method/config/source/window change.'))
    atomic(RUN/'checkpoint-01-plans.json',dict(PASS=True,plan_refs=plan_refs,authority_refs=authorities,aggregate=pin(dest/'aggregate-plan.json'),hosts=counts,total_positions=1642,jobs=1640,Ce_insufficient=2,
        source_bundle=pin(RUN/'source-bundle-prepared.json'),label_metadata_separate=True,labels_joined_to_results=False,main_started=False,G3=False,
        remaining='G3/main grant then attest runtime+LOCKED policy and compile final fingerprints; prepared plans/authorities intentionally cannot dispatch.'))
    with (ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').open('ab')as f:f.write('\nCheckpoint phần1 danh sách: đủ1.642vị trí =1.640job+2C-e insufficient; ba plan nguồn thật giữ đúng partition/config/env/seed/phụ thuộc. Metadata nhãn evaluator riêng, chưa ghép output/điểm. Plan candidate và authorityg3=false, không giả khóa để vượtguard. Chi tiết checkpoint-01-plans.json; chờkiểm/staging.\n'.encode())
    print(json.dumps({'PASS':True,'hosts':{h:{k:v for k,v in x.items()if k!='case_ids'}for h,x in counts.items()},'main_started':False}))
if __name__=='__main__':main()
