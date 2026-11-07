"""Biên dịch full matrix trên metadata giả, không đọc hoặc chạy dataset."""
from materialize_main import *
from nguon import validate_aggregate_plan
target=OUT/'runs/trien-khai-005/metadata-fixture-only';target.mkdir(exist_ok=False)
p=read_pin(ref(OUT/'protocol.json'));c=read_pin(p['dispatch_contract_ref']);placement=read_pin(c['partition_ref'])
def relpin(pin):return dict(pin,path=Path(pin['path']).relative_to(ROOT).as_posix())
def denied(fn):
 try:fn()
 except Blocked:return
 raise AssertionError('invalid input accepted')
denied(lambda:build(ref(OUT/'protocol.json'),{'path':'MUST_NOT_OPEN','sha256':'x'}, {},target/'never-created'))
policy=read_pin(c['failure_policy_candidate_ref']);policy['scope']='LOCKED_P7';policy['main_allowed']=True
fp=atomic(target/'fixture-policy.json',policy)
p['status']='LOCKED_G3';pp=relpin(atomic(target/'fixture-protocol.json',p))
runtime_refs={};independent_refs={};bindings={};inventory=read_pin(p['cohorts_source'])['inventory']
allids={ds:{}for ds in ['RE2-TT','Nezha-OB']}
for item in placement['slots']:
 if item.get('member_sha256'):allids[item['dataset']][item['opaque_id']]=item['member_sha256']
for ds,ids in allids.items():
 rows={oid:dict(member_sha256=m,files={'fixture':{'path':'not-a-real-data-source','bytes':1,'sha256':'0'*64}},
               **({'t':1000,'ce_history':'verified'}if ds=='RE2-TT'else{'t_ns':1000*10**9,'trace_guard_s':0}))for oid,m in ids.items()}
 # Chạm đúng nhánh insufficient: vẫn giữ đủ vị trí trong partition.
 if ds=='RE2-TT':rows[sorted(rows)[0]]['ce_history']='insufficient'
 rt={'dataset':ds,'g1_revision':'fixture-not-real','inventory':inventory[ds],'cases':rows}
 runtime_refs[ds]=relpin(atomic(target/(ds+'-runtime.json'),rt))
 independent_refs[ds]=relpin(atomic(target/(ds+'-source.json'),{'dataset':ds,'g1_revision':'fixture-not-real','cases_by_member':{r['member_sha256']:r for r in rows.values()}}))
 bindings[ds]={'path':'fixture-binding-not-used','sha256':'0'*64}
old=read_pin(ref(OUT/'runs/trien-khai-003/pilot-local-007/plan.json'))
baseline={j['slot']['arm']:j['config']for j in old['jobs']if j['kind']in('baseline','torai_pipeline')}
bundle={'runtime_refs':runtime_refs,'independent_source_refs':independent_refs,'runtime_binding_refs':bindings,
 'hosts':{h:{'main_executable':'metadata-only-not-executable','py38_executable':'metadata-only-not-executable','pythonpath':[]}for h in c['hosts']},
 'baseline_configs':baseline,'m1_contract':p['runtime_dependencies_historical'].get('contract',{'path':'unused','sha256':'0'*64}),
 'failure_policy_ref':relpin(fp),'author_source_ref':{'path':'fixture-only-not-real','sha256':'1'*64},'evaluation':{'scope':'FAKE_METADATA_ONLY_NEVER_DISPATCH'}}
bp=relpin(atomic(target/'fixture-bundle.json',bundle));source=target/'NOT_A_REAL_GRANT.txt';source.write_text('FAKE metadata fixture; does not authorize execution or data access',encoding='utf-8')
grant={'g3':True,'test_grant':True,'torai_A_source_grant':True,'source':ref(source)}
refs,aggregate=build(pp,bp,grant,target/'compiled')
validate_aggregate_plan(aggregate,p)
assert len(aggregate['jobs'])==1641 and len(aggregate['ce_support'])==1
bad=copy.deepcopy(aggregate);bad['jobs']=bad['jobs'][1:];denied(lambda:validate_aggregate_plan(bad,p))
bad=copy.deepcopy(aggregate);bad['execution_plan_refs']=bad['execution_plan_refs'][:2];denied(lambda:validate_aggregate_plan(bad,p))
from cham import validate_ce_plan
rt=read_pin(runtime_refs['RE2-TT']);validate_ce_plan(aggregate,rt)
bad=copy.deepcopy(aggregate);bad['ce_support']=[];denied(lambda:validate_ce_plan(bad,rt))
atomic(OUT/'runs/trien-khai-005/materializer-checks.json',{'PASS':True,'jobs':1641,'insufficient_rows':1,
 'positions_preserved':1642,'all_three_host_contracts_validated':True,'missing_part_and_job_and_Ce_support_blocked':True,
 'unlocked_protocol_rejected_before_source_bundle':True,'only_fake_metadata_no_dataset_execution':True})
print('full metadata matrix compiled and verified; no data/methods executed')
