"""Biên dịch metadata nguồn đã cấp thành plan bất biến; không chạy phương pháp/đọc nhãn."""
from pathlib import Path
import copy,sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'results/T-054/scripts'))
from bien_nhan import *
from nguon import placement_key,compare_sources,validate_locked_plan

def build(protocol_ref, bundle_ref, grant, destination):
    protocol=read_pin(protocol_ref)
    if protocol.get('status')!='LOCKED_G3' or not grant.get('g3') or not grant.get('test_grant'):
        raise Blocked('WAIT_G3_AND_TEST_GRANT: chưa đọc bundle nguồn')
    source=Path(grant['source']['path'])
    if digest(source)!=grant['source']['sha256']:
        raise Blocked('nguồn quyền thay hash')
    bundle=read_pin(bundle_ref);contract=read_pin(protocol['dispatch_contract_ref'])
    placement=read_pin(contract['partition_ref']);hosts=placement['hosts']
    runtimes={ds:read_pin(pin)for ds,pin in bundle['runtime_refs'].items()}
    for ds,rt in runtimes.items():
        compare_sources(rt,read_pin(bundle['independent_source_refs'][ds]),ds,rt['g1_revision'])
    inventories={ds:rt['inventory']for ds,rt in runtimes.items()}
    jobs={h:[]for h in hosts};support={h:[]for h in hosts};parents={};all_jobs=[]
    baseline_configs=bundle['baseline_configs']
    for item in placement['slots']:
        ds,oid,arm,view,h=(item[k]for k in ['dataset','opaque_id','arm','view','host'])
        row=runtimes[ds]['cases'][oid];hc=dict(contract,**contract['hosts'][h]);env=hc['environment_sha256']
        if view=='ce'and row['ce_history']=='insufficient':
            support[h].append(dict(dataset=ds,opaque_id=oid,status='INSUFFICIENT_EVIDENCE',source_sha256=fingerprint(row)));continue
        if view=='ce'and row['ce_history']!='verified':raise Blocked('C-e history chưa có chứng nhận')
        t=row.get('t',row.get('t_ns',0)//10**9)-(300 if view=='ce'else 0)
        family=arm in protocol['configurations'];torai=ds=='RE2-TT'and arm in('torai_A','torai_B')
        cfg=(protocol['configurations'][arm]['config']if family else {'cd3':'same sealed M1'}if arm=='C-d3'else baseline_configs[arm])
        slot=dict(dataset=ds,opaque_id=oid,member_sha256=row['member_sha256'],arm=arm,view=view,seed=item.get('seed'),
          window={'t':t,'half_width_s':300},source_sha256=fingerprint(row),config_sha256=fingerprint(cfg),
          environment_sha256=env['py38'if torai else'main'])
        info=bundle['hosts'][h]
        job=dict(slot=slot,kind='m1'if family else'cd3'if arm=='C-d3'else'torai_pipeline'if torai else'baseline',
          evaluation_mode='test',source=row,data_root=hc['data_root'],t=t,inventory=inventories[ds],
          runtime_ref=bundle['runtime_refs'][ds],independent_source_ref=bundle['independent_source_refs'][ds],
          runtime_binding_ref=bundle['runtime_binding_refs'][ds],g1_revision=runtimes[ds]['g1_revision'],protocol_ref=protocol_ref,
          pythonpath=info['pythonpath'],executable=info['main_executable'],prep_executable=info['main_executable'],
          method_executable=info['py38_executable'],prep_environment_sha256=env['main'],code_pins=hc['code_pins'],config=copy.deepcopy(cfg),
          m1_contract=bundle['m1_contract'],static_snapshot=protocol['snapshots'][ds],method_version='P3 frozen adapter; T054 lock',
          timeout_s=hc['timeout_s']['C-d3'if arm=='C-d3'else'main_slot'],failure_policy_ref=bundle['failure_policy_ref'],a4=item.get('a4',False))
        if arm=='torai_A':
            if not grant.get('torai_A_source_grant'):raise Blocked('WAIT_TORAI_A_SOURCE_GRANT')
            job['author_source_ref']=bundle['author_source_ref'];slot['author_source_sha256']=bundle['author_source_ref']['sha256']
        if arm=='C-d3':
            parent=parents[(ds,oid)];job['main_dependency']={'slot':parent['slot'],'job_sha256':fingerprint(parent)}
        if arm=='M1'and view=='main':parents[(ds,oid)]=job
        jobs[h].append(job);all_jobs.append(job)
    destination=Path(destination).resolve()
    if not destination.is_relative_to(OUT):raise Blocked('destination ngoài T054')
    destination.mkdir(exist_ok=False,parents=True);plans=[]
    for h in hosts:
        hc=dict(contract,**contract['hosts'][h])
        plan=dict(schema='T054-PLAN-1',mode='test',host_role=h,workers=hc['workers'],resources=hc['resources'],jobs=jobs[h],ce_support=support[h],
          directory=hc['code_root']+'/results/T-054/runs/main-005/queue',inventories=inventories,protocol_ref=protocol_ref,
          monitor=hc['monitor'],budget=hc['budget'],sensitivity_decision_ref=hc['sensitivity_decision_ref'],open_before_run=[])
        validate_locked_plan(plan,protocol,verify_host=False)
        pin=atomic(destination/(h+'-plan.json'),plan);plans.append(pin)
        authority=dict(grant,plan_sha256=fingerprint(plan),torai_A_source_sha256=bundle.get('author_source_ref',{}).get('sha256'))
        atomic(destination/(h+'-authority.json'),authority)
    aggregate=dict(schema='T054-PLAN-1',mode='test',host_role='aggregate',workers=1,jobs=all_jobs,
      ce_support=[row for values in support.values()for row in values],directory=str(destination/'aggregate-queue'),
      inventories=inventories,protocol_ref=protocol_ref,execution_plan_refs=plans,evaluation=bundle['evaluation'],
      monitor=contract['monitor'],budget=contract['budget'],sensitivity_decision_ref=contract['sensitivity_decision_ref'],open_before_run=[])
    atomic(destination/'aggregate-plan.json',aggregate)
    atomic(destination/'aggregate-authority.json',dict(grant,plan_sha256=fingerprint(aggregate),torai_A_source_sha256=bundle['author_source_ref']['sha256']))
    return plans,aggregate

if __name__=='__main__':
    raise SystemExit('API only: require locked protocol, source bundle and explicit grant; does not dispatch.')
