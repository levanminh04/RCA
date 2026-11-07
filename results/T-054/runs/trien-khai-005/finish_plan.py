"""Phân lô trước test từ metadata/hash, cập nhật hồ sơ ứng viên; không dispatch."""
import sys,json,copy,math,hashlib,ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import *
from nguon import placement_key
matrix=read_pin(ref(OUT/'matrix.json'));protocol=read_pin(ref(OUT/'protocol.json'))
local=read_pin(ref(RUN/'local-TT60-inventory.json'))
sizes={}
for row in local['files']:
 case=Path(row['path']).parent.name;member=fingerprint(['RE2-TT',case]);sizes[member]=sizes.get(member,0)+row['bytes']
tt={row['member_sha256']:row['opaque_id']for row in matrix['main']if row['dataset']=='RE2-TT'}
assert set(tt)==set(sizes)and len(tt)==60
# Chia theo tổng byte để cân dữ liệu, không dùng root/fault/điểm RCA.
loads={'ec2_1':0,'ec2_2':0};counts={'ec2_1':0,'ec2_2':0};owner={}
for member in sorted(tt,key=lambda m:(-sizes[m],m)):
 eligible=[h for h in loads if counts[h]<30];h=min(eligible,key=lambda h:(loads[h],h))
 owner[tt[member]]=h;loads[h]+=sizes[member];counts[h]+=1
hosts={h:[]for h in ['ec2_1','ec2_2','local']};placement=[]
family=set(protocol['configurations'])
for row in matrix['main']:
 cloud=row['dataset']=='RE2-TT'and(row['arm']in family or row['arm']=='torai_B')
 h=owner[row['opaque_id']]if cloud else'local';key=placement_key(row);hosts[h].append(key);placement.append(dict(row,host=h,placement_key=key))
for row in matrix['derived']:
 if row['separate_worker']:
  item=dict(row,seed=None);h=owner[row['opaque_id']];key=placement_key(item);hosts[h].append(key);placement.append(dict(item,host=h,placement_key=key))
for row in matrix['ce']:
 item=dict(row,seed=None);h=owner[row['opaque_id']];key=placement_key(item);hosts[h].append(key);placement.append(dict(item,host=h,placement_key=key,may_be_source_bound_insufficient=True))
for row in matrix['auxiliary']:
 key=placement_key(row);hosts['local'].append(key);placement.append(dict(row,host='local',placement_key=key))
allkeys=[k for rows in hosts.values()for k in rows]
assert len(allkeys)==len(set(allkeys))==1642
assert sum(len(v)for v in hosts.values())==1342+60+60+180
plan={'schema':'T054-PLACEMENT-1','status':'CANDIDATE_BEFORE_G3_NOT_DATA_GRANT','hosts':hosts,'slots':placement,
 'TT_case_owner':owner,'TT_transfer_bytes':loads,'TT_transfer_files':{h:90 for h in loads},
 'case_counts':counts,'counts':{h:len(v)for h,v in hosts.items()},
 'sources':{'matrix':ref(OUT/'matrix.json'),'TT60_inventory':ref(RUN/'local-TT60-inventory.json')},
 'dependency_rule':'M1 family and C-d3 of each TT case stay on same EC2; parent M1 sealed before C-d3; TORAI B prep then method; all3seeds same host; labels only after aggregate verified.',
 'no_dynamic_reassignment':'No duplicate speculative execution; reassign only after DRAIN/ownership reconciliation and new explicit plan preserving attempts.'}
placement_ref=atomic(RUN/'placement-005.json',plan)
correction=read_pin(ref(RUN/'ec2-1-cloud-dev-summary.json'));correction['exact_native_reference_EC2_2']=correction.pop('exact_native_same_EC2');correction['source_machine']='EC2_2';correction['target_machine']='EC2_1';correction['note']='Recovered completed output; original journal/cost remain unchanged. No valid supervisor runtime/RSS measurement for this run.'
atomic(RUN/'ec2-1-cloud-dev-summary-corrected.json',correction)
atomic(RUN/'retained-failures.json',{'EC2_1':'pre-exec PID identity race: controller stopped but worker finished; retained original BLOCKED journal and erroneous cost; recovered envelope without method rerun',
 'receiver_attempts':['collector refused BLOCKED original queue','recovery verifier initially used system python without numpy','collection succeeded using existing T025 main env'],
 'new_method_calls':2,'unique_dev_cases':1,'purpose':'one shared DEV cloud-route case per physical host, second host exposes Linux pre-exec race; no baseline reruns','G3':False,'test_opened':False})
ram=read_pin(ref(RUN/'reused-RAM-profiles.json'))
resources={}
for h in hosts:
 groups={x['dataset']+'|'+x['arm']for x in placement if x['host']==h}
 profiles={g:(2*1024**3 if h!='local'else max(ram.get(g,0),128*1024**2))for g in groups}
 resources[h]={'reserve_bytes':768*1024**2 if h!='local'else 384*1024**2,'factor':1.25,'expected_peak_bytes':profiles,
  'note':'Observed/provisional memory reservations, not a proven worst-case bound; stop/report on resource failure.'}
environments={'local':read_pin(ref(OUT/'environment.json'))['one_thread_environments']}
for h,folder in [('ec2_1','received-ec2-1-001'),('ec2_2','received-cloud-001')]:
 main=read_pin(ref(RUN/folder/'results/T-054/cloud-environment.json'))
 value=read_pin(ref(RUN/(h+'-torai-reuse-verification.json')));extra=json.loads(value['stdout']);assert extra['RCAEval_RCD_IO_exact']and extra['py38_exit']==0
 environments[h]={'main':main,'py38':extra['py38_environment']}
atomic(RUN/'environments-005.json',environments)
base_contract=read_pin(protocol['dispatch_contract_ref'])
base_contract.update(partition_ref=placement_ref,hosts={})
code_pins={p:pin if isinstance(pin,str)else pin['sha256'] for p,pin in read_pin(ref(OUT/'source-manifest.json'))['legacy_code'].items()}
code_pins.update({p.relative_to(ROOT).as_posix():ref(p)['sha256']for p in(OUT/'scripts').glob('*.py')})
base_contract['code_pins']=code_pins
for h in hosts:
 base_contract['hosts'][h]={'workers':2,'resources':resources[h],
  'environment_sha256':{k:fingerprint(v)for k,v in environments[h].items()}}
contract_ref=atomic(RUN/'dispatch-contract-005.json',base_contract)
protocol.update(status='CANDIDATE_NOT_LOCKED',allowed_hosts=list(hosts),dispatch_contract_ref=contract_ref,
 source_code=code_pins,readiness='MULTIHOST_PREPARATION_REVIEW_READY_WAIT_G3_SOURCE_BINDINGS',
 implementation='Two EC2 and laptop; fixed disjoint placement, host-specific env and memory admission; aggregate verifies completeness before labels.',
 open_before_execution=['Minh xét G3/khóa code/config/env/partition/policy đúng byte; không tự phát main.',
 'Grant test94 và nguồn TORAI A cohort; materialize/attest source/label/time/ce_history theo nguồn độc lập sau quyền, không mở telemetry trước.',
 'Compile exact immutable per-host and aggregate plans from placement005, validate resources/ownership/all job bindings, then dispatch unchanged code.',
 'RE3 schema/adapter and final one-time grant remain separate; no SSH/cleanup grants imply RE3 access.'],
 required_permissions=['G3 lock and test94 source/label grants','TORAI A author CSV grant for main TT cohort','commit/push separately if approved','RE3 separate final scope'],
 multihost_evidence={'placement':placement_ref,'EC2_2_dev':ref(RUN/'cloud-dev-summary.json'),
 'EC2_1_dev_recovered':ref(RUN/'ec2-1-cloud-dev-summary-corrected.json'),
 'EC2_1_transport':ref(RUN/'ec2_1-final-checks.json'),'EC2_2_transport':ref(RUN/'ec2_2-final-checks.json')})
protocol['fingerprint']=fingerprint({k:v for k,v in protocol.items()if k!='fingerprint'})
(OUT/'protocol.json').write_bytes(canonical(protocol)+b'\n')
source=read_pin(ref(OUT/'source-manifest.json'));source['own_scripts']={p.relative_to(ROOT).as_posix():ref(p)for p in(OUT/'scripts').glob('*.py')};source['multihost_current']=placement_ref
(OUT/'source-manifest.json').write_bytes(canonical(source)+b'\n')
settings={'status':'CANDIDATE_FOR_G3_NOT_MAIN_PERMISSION','hosts':list(hosts),'workers_max_per_host':2,'method_threads':1,
 'placement':placement_ref,'resources':resources,'settings_source':ref(OUT/'runs/trien-khai-004/quyet-dinh-minh.json'),
 'runtime_estimate':{'range_hours':[5,9],'scope':'planning scenario for compute+transfer+seal+scoring, not full research report ETA or fixed cap',
 'assumptions':['cloud 40–120s per M1-family/CE call, only one real EC2_2 sample ~67s; not every case/arm measured',
 '2 workers max per host when RAM allows; local may run 1 heavy or 2 light jobs','reuse measured baseline times from checkpoint003; heterogeneous cases, I/O and solver branches can change estimate',
 'setup/transfer 0.25–0.5h provisional; report/mechanism investigation excluded; no mandatory new benchmark to refine ETA'],
 'not_guaranteed':True,'not_a_budget_cap':True}}
atomic(RUN/'de-xuat-khoa-g3-005.json',settings)
print(json.dumps({'hosts':plan['counts'],'TT_transfer_bytes':loads,'TT60_download_required':False,'G3':False}))
