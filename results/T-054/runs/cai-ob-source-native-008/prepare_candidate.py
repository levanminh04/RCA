"""Prepare blocked 35/25 metadata without fabricating G3/main authority or opening telemetry."""
from pathlib import Path
import copy
import hashlib
import json
import sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
OUT = ROOT / 'results/T-054'
sys.path.insert(0, str(OUT / 'scripts'))
from bien_nhan import fingerprint, ref, read_pin, digest, Blocked
from nguon import placement_key, authorize
from p7 import load_plan


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf8') as stream:
        json.dump(value, stream, ensure_ascii=False, separators=(',', ':'))
    return pin(path)


def pin(path):
    obj = ref(path)
    obj['path'] = Path(path).resolve().relative_to(ROOT).as_posix()
    return obj


def main():
    # Match the immutable 006 package before copying its metadata (not data pages).
    old_manifest = json.loads((OUT / 'manifest-chuan-bi-main-006.json').read_bytes())
    def original(rel):
        path = ROOT / rel
        expected = old_manifest['outputs'][rel]
        assert path.stat().st_size == expected['bytes'] and digest(path) == expected['sha256'], rel
        return json.loads(path.read_bytes())

    for rel in ('protocol.json','source-manifest.json','authorization.json','runbook.md','ho-so-g3.md','reuse.json'):
        path = OUT / rel
        dest = RUN / 'before' / 'results/T-054' / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as stream:
            stream.write(path.read_bytes())
    protocol = original('results/T-054/protocol.json')
    baseline = original('results/T-054/runs/trien-khai-005/placement-005.json')
    contract = read_pin(protocol['dispatch_contract_ref'])
    moved = {'test-053c028c65','test-3a4c777083','test-327ac2a20e','test-071883754c','test-e654f8c5ab'}
    owners = dict(baseline['TT_case_owner'])
    owners.update({oid:'ec2_1' for oid in moved})
    assert Counter(owners.values()) == {'ec2_1':35,'ec2_2':25}
    placement = copy.deepcopy(baseline)
    placement.update(status='CANDIDATE_008_NOT_G3_NOT_DISPATCH',TT_case_owner=owners,
                     case_counts=dict(Counter(owners.values())),hosts={h:[] for h in contract['hosts']})
    for row in placement['slots']:
        ds, arm, oid = row['dataset'],row['arm'],row['opaque_id']
        h = 'ec2_2' if ds=='Nezha-OB' else 'local' if arm in ('circa','microrank','torai_A') else owners[oid]
        row.update(host=h, placement_key=placement_key(row))
        placement['hosts'][h].append(row['placement_key'])
    placement['counts'] = {h:len(keys) for h,keys in placement['hosts'].items()}
    placement['TT_transfer_files'] = {'ec2_1':105,'ec2_2':75}
    placement.pop('TT_transfer_bytes',None)  # Old equal-size 30/30 transfer totals no longer describe this partition.
    placement_ref = write(RUN/'placement-008.json',placement)
    code_pins = {rel:digest(ROOT/rel) for rel in protocol['source_code']}
    contract = copy.deepcopy(contract)
    contract['partition_ref'] = placement_ref
    contract['code_pins'] = code_pins
    ram = original('results/T-054/runs/trien-khai-005/reused-RAM-profiles.json')
    for h, hc in contract['hosts'].items():
        hc['code_pins'] = code_pins
        groups = {r['dataset']+'|'+r['arm'] for r in placement['slots'] if r['host']==h}
        profiles = {g:max(ram.get(g,0),128*1024**2,
                          2*1024**3 if h!='local' and g.startswith('RE2-TT|') else 0) for g in groups}
        hc['resources'] = dict(hc['resources'], expected_peak_bytes=profiles,
                              note='Historical DEV/provisional reservations; current cloud unreachable, not a proven peak bound.')
    contract['status'] = 'CANDIDATE_008_CLOUD_UNREACHABLE'
    contract['OB_input_layout'] = 'source_native; legacy-compatible cases retain old rectangular path'
    contract_ref = write(RUN/'dispatch-contract-008.json',contract)
    protocol.update(source_code=code_pins,dispatch_contract_ref=contract_ref,status='CANDIDATE_NOT_LOCKED',
                    readiness='OB_PATCH_DEV_EXACT_CLOUD_UNREACHABLE_RE3_CONTRACT_OPEN',real_execution_ready=False,
                    runtime='Candidate008 TT35/25 and OB on EC2_2; no additional transfer/staging verified.',
                    OB_input_layout={'mode':'source_native','default_library':'legacy',
                                     'exact_same_input_DEV':pin(RUN/'dev-ob-001/parity.json')},
                    open_before_execution=['G3/main grant absent','Both EC2 SSH endpoints unreachable; no fresh identity/env/disk/source verification',
                        'Code and metadata008 not staged; extra TT/OB sources not transferred',
                        'RE3 units/inventory/support/adapters remain open','Output/temp/failed-attempt disk bound not established'])
    protocol['fingerprint'] = fingerprint({k:v for k,v in protocol.items() if k!='fingerprint'})
    pp = write(RUN/'protocol-008.json',protocol)
    bundle = original('results/T-054/runs/chuan-bi-main-006/source-bundle-final-prepared.json')
    # Copy only label-free OB runtime/source/preparation metadata to portable repository paths.
    for field in ('runtime_refs','independent_source_refs','runtime_binding_refs'):
        source = bundle[field]['Nezha-OB']; value=read_pin(source)
        bundle[field]['Nezha-OB'] = write(RUN/'runtime-OB'/(field+'.json'),value)
    bundle['open_before_run'] = list(protocol['open_before_execution'])
    bundle['note'] = 'Preparation-only refs; do not treat as locked G3 attestations. OB Time audit006 supports reader-shape reasoning; no method test run.'
    write(RUN/'source-bundle-008.json',bundle)
    all_old=[]; old_host_plans={}
    for h in contract['hosts']:
        part=original('results/T-054/runs/chuan-bi-main-006/prepared/'+h+'-plan.json')
        old_host_plans[h]=part
        all_old.extend(part['jobs'])
    by_key={placement_key(j['slot']):j for j in all_old}
    support_by_key={placement_key(dict(s,arm='M1',view='ce',seed=None)):s
                    for p in old_host_plans.values() for s in p['ce_support']}
    parts={h:[]for h in contract['hosts']};support={h:[]for h in parts};parents={}
    for row in placement['slots']:
        h=row['host']; key=placement_key(row); hc=contract['hosts'][h]; info=bundle['hosts'][h]
        if key in support_by_key:
            support[h].append(copy.deepcopy(support_by_key[key]));continue
        job=copy.deepcopy(by_key[key]);slot=job['slot'];ds,arm,oid=slot['dataset'],slot['arm'],slot['opaque_id']
        torai=ds=='RE2-TT' and arm in ('torai_A','torai_B')
        slot['environment_sha256']=hc['environment_sha256']['py38'if torai else'main']
        job.update(code_pins=code_pins,protocol_ref=pp,data_root=hc['data_root'],pythonpath=info['pythonpath'],
                   executable=info['main_executable'],prep_executable=info['main_executable'],
                   method_executable=info['py38_executable'],prep_environment_sha256=hc['environment_sha256']['main'])
        for field in ('runtime_refs','independent_source_refs','runtime_binding_refs'):
            singular={'runtime_refs':'runtime_ref','independent_source_refs':'independent_source_ref','runtime_binding_refs':'runtime_binding_ref'}[field]
            job[singular]=bundle[field][ds]
        if ds=='Nezha-OB':job['OB_input_layout']='source_native'
        if arm=='C-d3':
            parent=parents[(ds,oid)];job['main_dependency']={'slot':parent['slot'],'job_sha256':fingerprint(parent)}
        if arm=='M1' and slot['view']=='main':parents[(ds,oid)]=job
        parts[h].append(job)
    grant_ref=write(RUN/'preparation-authority-source.json',{'user':'NẾU BẠN THẤY ỔN THÌ DUYỆT',
        'scope':'Approved patch proposal007 and preparation steps1-4; not G3/test/main/RE3 grant'})
    refs=[]; checks=[]
    for h,jobs in parts.items():
        old=old_host_plans[h];hc=contract['hosts'][h]
        plan=copy.deepcopy(old);plan.update(jobs=jobs,ce_support=support[h],protocol_ref=pp,resources=hc['resources'],
            directory=hc['code_root']+'/results/T-054/runs/main-008/queue',preparation_only=True,
            open_before_run=list(protocol['open_before_execution']))
        refp=write(RUN/'prepared'/(h+'-plan.json'),plan)
        load_plan(str(ROOT/refp['path']),refp['sha256'])
        got=[placement_key(j['slot']) for j in jobs]+[placement_key(dict(s,arm='M1',view='ce',seed=None)) for s in support[h]]
        assert len(got)==len(set(got)) and set(got)==set(placement['hosts'][h])
        auth={'source':grant_ref,'plan_sha256':fingerprint(plan),'g3':False,'test_grant':False,'main_dispatch':False,
              'torai_A_source_grant':False,'stop_before_main':True}
        ar=write(RUN/'prepared'/(h+'-authority.json'),auth)
        try:authorize(plan,auth,'run')
        except Blocked as exc:assert str(exc)=='WAIT_G3'
        else:raise AssertionError('candidate was dispatchable')
        refs.append(refp);checks.append({'host':h,'jobs':len(jobs),'support':len(support[h]),'plan_schema_dependency':'PASS','dispatch_denied':'WAIT_G3'})
    aggregate=copy.deepcopy(original('results/T-054/runs/chuan-bi-main-006/prepared/aggregate-plan.json'))
    aggregate.update(jobs=[j for h in parts for j in parts[h]],ce_support=[s for h in support for s in support[h]],
        execution_plan_refs=refs,protocol_ref=pp,preparation_only=True,directory=str(RUN/'prepared/aggregate-queue'),
        open_before_run=list(protocol['open_before_execution']))
    ap=write(RUN/'prepared/aggregate-plan.json',aggregate);load_plan(str(ROOT/ap['path']),ap['sha256'])
    allkeys=[placement_key(j['slot'])for j in aggregate['jobs']]
    assert len(allkeys)==len(set(allkeys))==1640 and len(aggregate['ce_support'])==2
    write(RUN/'prepared-validation.json',{'PASS':True,'checks':checks,'jobs':1640,'positions':1642,
        'supported_calls':1572,'unsupported':68,'static_only':True,'code_staged':False,'sources_transferred':False,
        'G3':False,'locked_plan_validator':'not invoked: policy/bindings remain preparation-only, no fake LOCKED values'})
    # Update current pointers only after immutable candidate artifacts exist; old checkpoints stay historical.
    (OUT/'protocol.json').write_bytes((ROOT/pp['path']).read_bytes())
    source=json.loads((OUT/'source-manifest.json').read_bytes())
    for rel in source['legacy_code']:source['legacy_code'][rel]=code_pins[rel]
    for rel in source['own_scripts']:source['own_scripts'][rel]=ref(ROOT/rel)
    source['checkpoint008']={'protocol':pp,'contract':contract_ref,'placement':placement_ref,
                             'state':'CANDIDATE_BLOCKED_CLOUD_AND_RE3','science_code_changed_in_approved_OB_scope':True}
    (OUT/'source-manifest.json').write_text(json.dumps(source,ensure_ascii=False,separators=(',',':')),encoding='utf8')
    authority=json.loads((OUT/'authorization.json').read_bytes())
    authority.update(g3=False,test_grant=False,main_dispatch=False,main_readiness=False,stop_before_main=True,
        checkpoint008=pin(RUN/'prepared-validation.json'),current_blocker_ref=pin(RUN/'cloud-inventory-001.json'),
        note='OB patch conditional approval accepted after self-check; cloud unreachable and RE3 contract open. No main grant inferred.')
    (OUT/'authorization.json').write_text(json.dumps(authority,ensure_ascii=False,separators=(',',':')),encoding='utf8')
    print(json.dumps({'PASS':True,'checks':checks,'candidate':pp,'G3':False}))


if __name__=='__main__':main()
