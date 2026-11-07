"""Use verified prior DEV artifact sizes, never new method calls or test values."""
from pathlib import Path
import collections
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
manifest = json.loads((ROOT/'results/T-054/manifest-chuan-bi-main-006.json').read_text(encoding='utf-8'))
pins = manifest['outputs']


def check(rel):
    p = ROOT/rel; v=pins[rel]
    b=p.read_bytes()
    assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],rel
    return b


groups = collections.defaultdict(list)
seen = set()
for rel in pins:
    if not rel.endswith('/result.json') or 'pilot-' not in rel:
        continue
    parent = Path(rel).parent
    while not parent.name.startswith('attempt-') and parent != parent.parent:
        parent=parent.parent
    prefix=parent.as_posix()+'/'
    if prefix in seen or prefix+'verified.json' not in pins or prefix+'job.json' not in pins:
        continue
    job=json.loads(check(prefix+'job.json'))
    if job.get('evaluation_mode')!='dev' or job['kind']=='synthetic' or job.get('fixture_route'):
        continue
    check(prefix+'verified.json')
    sizes=[]
    for name,v in pins.items():
        if name.startswith(prefix):
            check(name);sizes.append(v['bytes'])
    seen.add(prefix)
    key=job['slot']['dataset']+'|'+job['slot']['arm']
    groups[key].append({'attempt':prefix,'bytes':sum(sizes),'files':len(sizes)})

family={'M1','bo-E1','bo-E2','bo-E5','C-a0','C-a1','T12-on','C-d3'}
maxima={k:max(r['bytes'] for r in rows) for k,rows in groups.items()}
forecasts={}
for host in ['ec2_1','ec2_2','local']:
    plan=json.loads((ROOT/f'results/T-054/runs/cai-ob-source-native-008/prepared/{host}-plan.json').read_text(encoding='utf-8'))
    terms=[]
    for key,count in collections.Counter(j['slot']['dataset']+'|'+j['slot']['arm'] for j in plan['jobs']).items():
        ds,arm=key.split('|');source=key
        if key in maxima:
            amount=maxima[key]
        else:
            matching=[(k,v) for k,v in maxima.items() if k.startswith(ds+'|') and (arm not in family or k.split('|')[1] in family)]
            if not matching:matching=list(maxima.items())
            source,amount=max(matching,key=lambda x:x[1])
        # Empirical planning margin, not a claim of a mathematical output bound.
        per_job=max(256*1024,4*amount)
        terms.append({'group':key,'jobs':count,'reference_group':source,'observed_max_bytes':amount,
                      'planning_bytes_per_job':per_job,'forecast_bytes':count*per_job,
                      'fallback':source!=key})
    subtotal=sum(t['forecast_bytes'] for t in terms)
    forecasts[host]={'terms':terms,'attempt_storage_planning_bytes':subtotal,
                     'extra_retry_and_temp_planning_bytes':subtotal,
                     'combined_planning_bytes':2*subtotal}
result={'schema':'T054-STORAGE-FORECAST-011','status':'EMPIRICAL_PLANNING_ESTIMATE_NOT_PROVEN_UPPER_BOUND',
        'source_manifest':'results/T-054/manifest-chuan-bi-main-006.json','verified_dev_attempts':len(seen),
        'observed_groups':dict(groups),'observed_max_bytes':maxima,'forecasts':forecasts,
        'receive_all_hosts_plus_report_copy_bytes':2*sum(v['combined_planning_bytes']for v in forecasts.values()),
        'assumptions':['4x maximum prior verified DEV attempt size with256KiB floor per job',
                       'one additional full allocation for temp/retry, another full receive/report copy',
                       'case complexity can exceed DEV; retained failures/unbounded retries can exceed forecast'],
        'limits':['no speculative deletion or pruning','existing stop/report and drain procedure applies if disk approaches2GiB headroom',
                  'not a guaranteed bound; no new automatic disk controller installed'],
        'new_methods_run':False,'test_telemetry_opened':False}
(RUN/'storage-forecast.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'verified_dev_attempts':len(seen),'groups':len(groups),
                  'host_planning_GiB':{h:round(v['combined_planning_bytes']/1024**3,3)for h,v in forecasts.items()},
                  'receive_report_copy_GiB':round(result['receive_all_hosts_plus_report_copy_bytes']/1024**3,3)}))
