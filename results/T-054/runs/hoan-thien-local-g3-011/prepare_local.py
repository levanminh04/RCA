"""Refresh current candidate pins/plans/packages locally. Never SSH or dispatch."""
from pathlib import Path
import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
from collections import Counter

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
OUT=ROOT/'results/T-054'
sys.path[:0]=[str(OUT/'scripts'),str(ROOT/'src')]
from bien_nhan import ref,read_pin,digest,fingerprint,Blocked,no_labels
from nguon import compare_sources,placement_key,authorize
from p7 import load_plan


def pin(path):
    v=ref(path)
    if Path(path).resolve().is_relative_to(ROOT):v['path']=Path(path).resolve().relative_to(ROOT).as_posix()
    return v


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8')as f:json.dump(value,f,ensure_ascii=False,separators=(',',':'))
    return pin(path)


previous=json.loads((OUT/'manifest-cai-ob-source-native-008.json').read_text(encoding='utf-8'))
def old(rel):
    v=previous['outputs'][rel];p=ROOT/rel
    assert p.stat().st_size==v['bytes']and digest(p)==v['sha256'],rel
    return json.loads(p.read_bytes())


env=dict(os.environ,PYTHONHASHSEED='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
local_env={}
for name,exe in [('main','D:/RCA-ext/envs/T-014-main/Scripts/python.exe'),('py38','D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe')]:
    value=json.loads(subprocess.check_output([exe,'-X','utf8','-B',str(RUN/'capture_runtime_environment.py')],env=env))
    local_env[name]={'snapshot':value,'fingerprint':fingerprint(value)}
write(RUN/'local-runtime-environments.json',local_env)
placement=old('results/T-054/runs/cai-ob-source-native-008/placement-008.json')
placement.update(status='CANDIDATE_011_LOCAL_PREPARED_CLOUD_NOT_CHECKED')
placement_ref=write(RUN/'placement-candidate.json',placement)
binding=read_pin(pin(OUT/'runs/cai-re3-h2-010/code-binding-candidate.json'))
code={rel:digest(ROOT/rel)for rel in binding['files']}
code[(RUN/'activate_after_g3.py').relative_to(ROOT).as_posix()]=digest(RUN/'activate_after_g3.py')
write(RUN/'current-code-pins.json',{'scope':'actual local code bytes; candidate, not G3','files':{k:pin(ROOT/k)for k in code},'code_pins':code})
policy=read_pin(old('results/T-054/runs/cai-ob-source-native-008/source-bundle-008.json')['failure_policy_ref'])
for evidence in policy['code_evidence']:
    evidence.update(pin(ROOT/evidence['path']))
policy.update(scope='CANDIDATE_FOR_G3_NOT_LOCKED',main_allowed=False)
policy_ref=write(RUN/'failure-policy-candidate.json',policy)
contract=old('results/T-054/runs/cai-ob-source-native-008/dispatch-contract-008.json')
contract.update(code_pins=code,partition_ref=placement_ref,failure_policy_candidate_ref=policy_ref,
                status='CANDIDATE_011_LOCAL_ONLY_CLOUD_VERIFICATION_PENDING')
for host,hc in contract['hosts'].items():
    hc['code_pins']=code
    if host=='local':
        hc['environment_sha256']={k:v['fingerprint']for k,v in local_env.items()}
        hc['environment_evidence']='local-runtime-environments.json; fresh local only'
    else:
        hc['code_root']=f'/home/ubuntu/rca-p7/T-054/{host}/main-011/code'
        hc['environment_evidence']='historical008 snapshot only; recheck current EC2 before G3'
contract_ref=write(RUN/'dispatch-contract-candidate.json',contract)
protocol=old('results/T-054/runs/cai-ob-source-native-008/protocol-008.json')
waits=['WAIT_EXPLICIT_G3_MAIN_AND_SOURCE_GRANTS','WAIT_CURRENT_EC2_IDENTITY_ENV_RAM_DISK_SOURCE_AND_STAGING',
       'WAIT_MINH_RE3_PREPARATION_DISPOSITION_AND_MAIN_OPERATING_POLICY']
protocol.update(source_code=code,dispatch_contract_ref=contract_ref,status='CANDIDATE_NOT_LOCKED',
                readiness='LOCAL_011_PREPARED_CLOUD_AND_G3_DECISIONS_PENDING',real_execution_ready=False,
                runtime='TT35/25 and OB on EC2_2; laptop CIRCA/MicroRank/A. Local candidates only; no cloud checks.',
                runtime_environments_ref=pin(RUN/'local-runtime-environments.json'),
                open_before_execution=waits,
                RE3_preparation={'H2':'implemented and self-checked010; grpc guard updated011',
                                 'owner_metadata':'global serviceName/container_name union approved and read011',
                                 'native_units_and_metric_owner_aliases':'OPEN; no complete real profile or evaluation grant',
                                 'scope':'preparation before G3; final held-out evaluation remains separate'},
                execution_candidate={'placement':placement_ref,'contract':contract_ref,'prepared_root':RUN.relative_to(ROOT).as_posix()+'/prepared'})
protocol['fingerprint']=fingerprint({k:v for k,v in protocol.items()if k!='fingerprint'})
protocol_ref=write(RUN/'protocol-candidate.json',protocol)
bundle=old('results/T-054/runs/cai-ob-source-native-008/source-bundle-008.json')
bundle.update(failure_policy_ref=policy_ref,open_before_run=waits,
              note='011 source metadata reuses verified006/008. No G3 attestations or cloud checks fabricated.')
bundle['evaluation']['runtime_refs']=bundle['runtime_refs']
bundle['evaluation']['output']=str(OUT/'reports/main-011')
source_files={};source_validation={};runtimes={}
for ds,runtime_ref in bundle['runtime_refs'].items():
    runtime=read_pin(runtime_ref);runtimes[ds]=runtime
    compare_sources(runtime,read_pin(bundle['independent_source_refs'][ds]),ds,runtime['g1_revision'])
    for row in runtime['cases'].values():
        for meta in row['files'].values():
            source_files[meta['path']]=meta
for rel,meta in source_files.items():
    p=ROOT/rel
    assert p.is_file()and p.stat().st_size==meta['bytes']and digest(p)==meta['sha256'],rel
    source_validation[rel]={'bytes':meta['bytes'],'sha256':meta['sha256']}
# Author-A sources are kept local, and are not added to a cloud packet.
author=read_pin(bundle['author_source_ref']);author_files={}
for row in author['cases_by_member'].values():
    for meta in row['files'].values():
        p=Path(author['data_root'])/meta['path']
        assert p.is_file()and p.stat().st_size==meta['bytes']and digest(p)==meta['sha256']
        author_files[str(p)]={'bytes':meta['bytes'],'sha256':meta['sha256']}
write(RUN/'local-source-hash-validation.json',{'PASS':True,'main_files':source_validation,'author_A_files':author_files,
      'main_bytes':sum(v['bytes']for v in source_validation.values()),'author_A_bytes':sum(v['bytes']for v in author_files.values()),
      'mode':'binary hash and metadata only; no signal decode, label join or methods'})
bundle['source_readiness_ref']=pin(RUN/'local-source-hash-validation.json')
bundle_ref=write(RUN/'source-bundle-candidate.json',bundle)
permission_ref=write(RUN/'preparation-authority-source.json',{'user':'làm toàn bộ các phần còn lại, trừ phần kiểm ec2 ra vì hiện chưa vào được',
    'scope':'local preparation only; no G3/main or EC2 execution',
    'source_A':'Duyệt sửa guard theo phần A','source_B':'Duyệt đọc hai cột như metadata inventory'})
parts={};refs=[];checks=[];parents={}
for host in ['ec2_1','ec2_2','local']:
    plan=old('results/T-054/runs/cai-ob-source-native-008/prepared/'+host+'-plan.json')
    hc=dict(contract,**contract['hosts'][host])
    plan.update(protocol_ref=protocol_ref,preparation_only=True,open_before_run=waits,
                directory=hc['code_root']+'/results/T-054/runs/main-011/queue',resources=hc['resources'])
    for job in plan['jobs']:
        s=job['slot'];torai=s['arm']in('torai_A','torai_B')and s['dataset']=='RE2-TT'
        s['environment_sha256']=hc['environment_sha256']['py38'if torai else'main']
        job.update(code_pins=code,protocol_ref=protocol_ref,failure_policy_ref=policy_ref,
                   prep_environment_sha256=hc['environment_sha256']['main'])
        if s['arm']=='C-d3':
            parent=parents[(s['dataset'],s['opaque_id'])]
            job['main_dependency']={'slot':parent['slot'],'job_sha256':fingerprint(parent)}
        if s['arm']=='M1'and s['view']=='main':parents[(s['dataset'],s['opaque_id'])]=job
    part_ref=write(RUN/'prepared'/(host+'-plan.json'),plan)
    load_plan(str(ROOT/part_ref['path']),part_ref['sha256'])
    auth={'schema':'T054-AUTHORITY-1','source':permission_ref,'plan_sha256':fingerprint(plan),
          'g3':False,'test_grant':False,'main_dispatch':False,'stop_before_main':True,'torai_A_source_grant':False}
    write(RUN/'prepared'/(host+'-authority.json'),auth)
    try:authorize(plan,auth,'run')
    except Blocked as exc:assert str(exc)=='WAIT_G3'
    else:raise AssertionError('candidate dispatch unexpectedly allowed')
    parts[host]=plan;refs.append(part_ref)
    checks.append({'host':host,'jobs':len(plan['jobs']),'ce_support':len(plan['ce_support']),'denied':'WAIT_G3','schema_dependency':'PASS'})
aggregate=old('results/T-054/runs/cai-ob-source-native-008/prepared/aggregate-plan.json')
aggregate.update(jobs=[j for p in parts.values()for j in p['jobs']],execution_plan_refs=refs,protocol_ref=protocol_ref,
                 preparation_only=True,open_before_run=waits,directory=str(RUN/'prepared/aggregate-queue'),evaluation=bundle['evaluation'])
ap=write(RUN/'prepared/aggregate-plan.json',aggregate);load_plan(str(ROOT/ap['path']),ap['sha256'])
assert len(aggregate['jobs'])==1640 and len({placement_key(j['slot'])for j in aggregate['jobs']})==1640
assert len(aggregate['ce_support'])==2
for ds,runtime in runtimes.items():
    expected={placement_key(s)for s in placement['slots']if s['dataset']==ds}
    got={placement_key(j['slot'])for j in aggregate['jobs']if j['slot']['dataset']==ds}
    got.update(placement_key(dict(s,arm='M1',view='ce',seed=None))for s in aggregate['ce_support']if s['dataset']==ds)
    assert expected==got
write(RUN/'prepared-validation.json',{'PASS':True,'hosts':checks,'jobs':1640,'positions':1642,
    'main_started':False,'G3':False,'cloud_checked':False,'code_files':len(code),
    'runtime_bindings':'historical PREPARATION refs retained; fresh G3 attestation only after exact grants'})

# Update current pointers after immutable candidates exist. Historical files stay untouched.
(OUT/'protocol.json').write_bytes((ROOT/protocol_ref['path']).read_bytes())
source=json.loads((OUT/'source-manifest.json').read_bytes())
for rel in source['legacy_code']:source['legacy_code'][rel]=code[rel]
for rel in source['own_scripts']:source['own_scripts'][rel]=pin(ROOT/rel)
source.update(current_multihost_protocol=protocol_ref,checkpoint011={'protocol':protocol_ref,'contract':contract_ref,
              'placement':placement_ref,'source_bundle':bundle_ref,'status':'LOCAL_PREPARED_NOT_G3_CLOUD_PENDING'})
source['legacy_code']['src/p3/re3.py']=code['src/p3/re3.py']
(OUT/'source-manifest.json').write_text(json.dumps(source,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
authority=json.loads((OUT/'authorization.json').read_bytes())
authority.update(g3=False,test_grant=False,main_dispatch=False,main_readiness=False,stop_before_main=True,
                 source_current=permission_ref,checkpoint011=pin(RUN/'prepared-validation.json'),
                 current_blocker_ref=pin(RUN/'prepared-validation.json'),
                 note='Local011 refreshed; all EC2 work paused. Separate exact G3/main/source grants required; no real RE3 profile/evaluation grant.')
(OUT/'authorization.json').write_text(json.dumps(authority,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(OUT/'environment.json').write_text(json.dumps({'schema':'T054-ENVIRONMENT-011','local':local_env,
    'cloud':'historical environment fingerprints in candidate contract only; no current verification',
    'cloud_checked':False},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(json.dumps({'PASS':True,'code_files':len(code),'checks':checks,'main_source_files':len(source_files),'A_files':len(author_files)}),flush=True)
