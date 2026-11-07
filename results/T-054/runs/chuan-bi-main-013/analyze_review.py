"""F1/F2: arithmetic on pinned, already produced metadata/costs only."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path

from activate import ROOT,RUN,pin
from bien_nhan import atomic,digest,read_pin,ref


def main():
    evidence=[]
    manifests={}
    for key,path in [('006','results/T-054/manifest-chuan-bi-main-006.json'),
                     ('011','results/T-054/manifest-hoan-thien-local-g3-011.json'),
                     ('012','results/T-054/runs/danh-gia-ec2-moi-012/manifest.json'),
                     ('013',str((RUN/'pre-review-001/manifest.json').relative_to(ROOT)))]:
        manifests[key]=json.loads((ROOT/path).read_bytes())['outputs']
        if key=='012':
            manifests[key]={('results/T-054/runs/danh-gia-ec2-moi-012/'+k if not k.startswith(('results/','src/'))else k):v
                            for k,v in manifests[key].items()}
    def old(key,path):
        expected=manifests[key][path];p=ROOT/path
        assert p.stat().st_size==expected['bytes']and digest(p)==expected['sha256'],path
        evidence.append(dict(path=path,**expected))
        return json.loads(p.read_bytes())
    old13=read_pin(pin(RUN/'pre-review-001/manifest.json'))
    prefix=(RUN/'received/ec2-large-disk-r2/results/T-054/runs/checkpoint013-results-002/queue').relative_to(ROOT).as_posix()
    cost_paths=[p for p in manifests['013']if p.startswith(prefix+'/')and p.endswith('/cost.json')]
    costs=[old('013',p)for p in cost_paths]
    event_path=prefix+'/events.jsonl';p=ROOT/event_path;m=manifests['013'][event_path]
    assert digest(p)==m['sha256'];evidence.append(dict(path=event_path,**m))
    events=[json.loads(line)for line in p.read_text(encoding='utf-8').splitlines()]
    start={x['job_id']:datetime.fromisoformat(x['utc']).timestamp()for x in events if x.get('state')=='RUNNING'}
    finish={x['job_id']:datetime.fromisoformat(x['utc']).timestamp()for x in events
            if x.get('job_id')in start and x.get('state')in ('VERIFIED','BLOCKED','FAILED_OPERATIONAL')}
    f1=dict(r2_started_jobs=len(start),r2_cost_files=len(costs),summed_attempt_wall_s=sum(x['wall_s']for x in costs),
            queue_interval_s=max(finish.values())-min(start.values()),
            workers_observed=next(x['workers']for x in events if x.get('state')=='SUPERVISOR'),
            hypotheses_unresolved=['CPU contention','different arm cost'],selected_candidate='one worker on each EC2',
            claim_total_time_unchanged=False,claim_method_outputs_independent_of_timeout=False)
    summary_path='results/T-054/runs/trien-khai-003/pilot-local-007/summary.json'
    local=old('006',summary_path)['group_wall_s']
    pilot4=old('006','results/T-054/runs/trien-khai-004/pilot-2-worker-001/summary.json')
    for row in pilot4['rows']:
        if row['dataset']=='Nezha-OB'and row['arm']=='M1':local['Nezha-OB|M1'].append(row['cost_s'])
    for arm in ('baro','simplerca','microrank','tracerca','circa','torai_B'):
        path='results/T-052/runs/trien-khai-001/ob-local-002/'+arm+'-timing.json'
        m52=json.loads((ROOT/'results/T-052/manifest-dinh-chinh-g3-004.json').read_bytes())['outputs'][path]
        p=ROOT/path;assert digest(p)==m52['sha256'];d=json.loads(p.read_bytes())
        evidence.append(dict(path=path,**m52));local['Nezha-OB|'+arm].append(d['cost']['wall_s'])
    cloud=old('013',(RUN/'cloud-verification.json').relative_to(ROOT).as_posix())
    tt={}
    for host,v in cloud['hosts'].items():
        for row in v['rows']:
            arm=row['slot']['arm'];tt[arm]=max(tt.get(arm,0),row['wall_s'])
    scenarios={};counts={};storage=old('011','results/T-054/runs/hoan-thien-local-g3-011/storage-copy-accounting.json')
    terms={t['group']:t for v in storage['by_host'].values()for t in v['terms']}
    output_raw=output_zip=0
    for host in ('ec2_1','ec2_2','local'):
        plan=read_pin(pin(RUN/'prepared'/(host+'-plan.json')))
        groups=Counter(j['slot']['dataset']+'|'+j['slot']['arm']for j in plan['jobs']);counts[host]=dict(groups)
        rows=[]
        for group,n in groups.items():
            if host=='local':
                per=max(local[group]);source=summary_path+'#/group_wall_s/'+group
                quality='old local DEV maximum observed per group; load/environment/case are not controlled'
            else:
                arm=group.split('|')[1];per=tt[arm];source='cloud-verification.json#/hosts/*/rows'
                quality=('contended observation used as cost proxy, not one-worker measurement'if arm in ('C-a0','bo-E1','bo-E2','M1')
                         else 'new EC2 DEV observation; extrapolated across unobserved test cases')
            rows.append(dict(group=group,jobs=n,proxy_seconds=per,total_seconds=n*per,source=source,quality=quality))
            if host!='local':
                t=terms[group];output_raw+=n*t['raw_max_per_attempt'];output_zip+=n*t['compressed_max_per_attempt']
        serial=sum(x['total_seconds']for x in rows)
        a=sum(x['total_seconds']for x in rows if x['group'].endswith('|torai_A'))
        scenarios[host]=dict(workers=plan['workers'],serial_proxy_seconds=serial,terms=rows,
              A_serial_seconds=a,ideal_non_A_overlap_plus_A_seconds=(serial-a)/plan['workers']+a,
              ideal_is_measured=False)
    package=old('013',(RUN/'dev-package.json').relative_to(ROOT).as_posix())
    stage=old('013',(RUN/'ec2-large-disk-stage.json').relative_to(ROOT).as_posix())
    archive_bytes=(RUN/'dev-package.tar.gz').stat().st_size
    input_bytes=sum(read_pin(pin(RUN/'launch-conditions.json'))['hosts'][h]['source_bytes']for h in ('ec2_1','ec2_2'))
    # Existing successful report fixture invocation was bounded at120s. This is a ceiling for that
    # small fixture only, never a bound for the real evaluator or for another runtime.
    source='results/T-054/runs/danh-gia-ec2-moi-012/remote_checks.py'
    p=ROOT/source;mp=manifests['012'][source];assert digest(p)==mp['sha256'];evidence.append(dict(path=source,**mp))
    assert 'timeout=120' in p.read_text(encoding='utf-8')
    report_success=old('012','results/T-054/runs/danh-gia-ec2-moi-012/ec2-large-disk-fixture-score.json')
    assert report_success['exit']==0
    report_fixture=old('012','results/T-054/runs/danh-gia-ec2-moi-012/fixture-score-ec2-large-disk/summary.json')
    report_slots=report_fixture['slots']
    report_proxy=120*(1640/report_slots)
    current_packet=read_pin(pin(RUN/'main-packet.json'))['files']
    packet_bytes=sum(v['bytes']for v in current_packet.values())+(RUN/'main-packet.json').stat().st_size
    model=[]
    for name,rate,multiplier,bytes_multiplier in [('repeat_DEV',2*1024**2,1,1),('slower_sensitivity',1024**2,2,4)]:
        send=(input_bytes+2*packet_bytes)/rate
        receive=output_zip*bytes_multiplier/rate
        # Read/write/verify sensitivity on byte volume; rate is explicitly assumed, not measured.
        hash_io=(2*input_bytes+2*output_raw*bytes_multiplier)/(50*1024**2)
        compute=max(v['serial_proxy_seconds']for v in scenarios.values())*multiplier
        score=report_proxy*multiplier
        total=send+compute+receive+hash_io+score
        model.append(dict(name=name,assumed_network_bytes_s=rate,assumed_hash_io_bytes_s=50*1024**2,
            method_cost_multiplier=multiplier,output_size_multiplier=bytes_multiplier,
            outbound_seconds=send,parallel_queues_seconds=compute,inbound_seconds=receive,
            hashing_extract_verify_io_seconds=hash_io,verify_and_score_proxy_seconds=score,total_seconds=total,
            critical_queue_under_assumptions=max(scenarios,key=lambda h:scenarios[h]['serial_proxy_seconds'])))
    atomic(RUN/'review-evidence.json',dict(F1=f1,pinned_sources=evidence,
         previously_reviewed_manifest=pin(RUN/'pre-review-001/manifest.json'),no_new_method_runs=True,no_test_payload_read=True))
    atomic(RUN/'cost-scenario.json',dict(schema='T054-013-COST-AFTER-REVIEW-1',status='CANDIDATE_NOT_A_VERIFIED_ETA',
         scenarios=scenarios,counts=counts,pipeline_scenarios=model,input_bytes=input_bytes,
         return_raw_proxy_bytes=output_raw,return_compressed_proxy_bytes=output_zip,
         observed_dev_stage=dict(archive_bytes=archive_bytes,wall_s=stage['seconds'],includes='SSH/decompress/hash; not network-only'),
         score_proxy=dict(successful_fixture_timeout_s=120,fixture_slots=report_slots,full_slots=1640,
            formula='120 *full_slots/fixture_slots; sensitivity doubles this; not a measured full-cohort scoring time'),
         uncertainty=dict(measured_whole_cohort_ETA=False,score_full_cohort_measured=False,
            failure_conditions=['case/runtime cost differs from representative DEV','bootstrap/verification cost not linear in slot count',
              'source error audits require extra reads/compute','network or hashing below assumed rates','RAM wait/resume or operational block',
              'test output size/tie structure differs from DEV','time for Minh/manual decisions is not included'],
            owner='Codex measures during the authorized main; Minh decides if a resource/operational stop requires changes'),
         evidence=pin(RUN/'review-evidence.json'),main_ETA_verified=False))
    print(json.dumps(dict(F1=f1,serial_hours={h:v['serial_proxy_seconds']/3600 for h,v in scenarios.items()},
                         pipeline_hours={x['name']:x['total_seconds']/3600 for x in model})))


if __name__=='__main__':main()
