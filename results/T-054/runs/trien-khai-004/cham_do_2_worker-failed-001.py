"""So đầu vào, toàn trường khoa học và C-e sau khi hai slot kết thúc."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'results/T-054/runs/trien-khai-003'),
             str(ROOT/'results/T-052/scripts'),str(ROOT/'src')]
from bien_nhan import atomic,ref,read_pin,fingerprint,events
from dieu_phoi import status,verify_attempt
from pilot import comparable,reference
from doi_chieu_pilot import differences
from cham import describe
from nguon import original_dev_labels
dest=RUN/'pilot-2-worker-001';plan=read_pin(ref(dest/'plan.json'));st=status(dest/'queue')
assert st['controller'] is None and all(r['state']=='VERIFIED' for r in st['jobs'].values())
oldplan=read_pin(ref(ROOT/'results/T-054/runs/trien-khai-003/pilot-local-007/plan.json'))
oldstate=status(ROOT/'results/T-054/runs/trien-khai-003/pilot-local-007/queue')
ce=next(c for c in read_pin(ref(ROOT/'results/T-054/pilot-plan.json'))['candidates']
        if c['opaque_id']=='dev-a5cabe5fa7' and c['window']=='ce')
rows=[];records={};labels={};starts=[];ends=[];all_samples=[]
for j in plan['jobs']:
    s=j['slot'];key=fingerprint(s);v=st['jobs'][key];a=Path(v['attempt']);record,=verify_attempt(a,j,v['token'])
    records[key]=[record];assert record['status']=='OK'
    if s['view']=='ce':
        before=reference(ce['native_record'],'K-E1+E2+E5');source=ce['native_record'];normalized='native reference has no T054 normalized-input digest'
    else:
        oj=next(x for x in oldplan['jobs'] if x['slot']['dataset']==s['dataset'] and x['slot']['arm']=='M1')
        ov=oldstate['jobs'][fingerprint(oj['slot'])];oa=Path(ov['attempt']);before,=verify_attempt(oa,oj,ov['token'])
        source=ref(oa/'result.json')
        normalized=read_pin(ref(a/'invocation.json'))['normalized_input_sha256']==read_pin(ref(oa/'invocation.json'))['normalized_input_sha256']
        assert normalized
    x=comparable(before);y=comparable(record)
    diff=differences(x,y)
    assert x==y,(s['dataset'],s['view'],diff)
    desc=read_pin(j['independent_source_ref'])
    labels[s['dataset']]={s['opaque_id']:next(iter(original_dev_labels({'source_descriptor':desc}, {})['by_member'].values()))}
    start=read_pin(ref(a/'launch.json'))['started_epoch'];cost=read_pin(ref(a/'cost.json'))['wall_s']
    starts.append(start);ends.append(start+cost);samples=events(a/'monitor.jsonl');all_samples.extend(samples)
    rows.append({'dataset':s['dataset'],'opaque_id':s['opaque_id'],'view':s['view'],'arm':'M1','status':record['status'],
                 'exact_all_comparable_fields':True,'reference':source,'normalized_input_exact':normalized,
                 'cost_s':cost,'peak_tree_rss':max(x['tree_rss']for x in samples),
                 'max_monitor_gap_s':max(x['max_monitor_gap_s']for x in samples)})
assert max(starts)<min(ends)
# Nhãn dev chỉ ghép sau trạng thái VERIFIED của cả hai; không mở nhãn test.
atomic(dest/'snapshot-before-labels.json',{'states':st['jobs'],'plan_sha256':fingerprint(plan)})
table=describe(plan,records,labels);atomic(dest/'descriptive.json',table)
assert len(table['ce'])==1 and table['ce'][0]['U']>0
latest={};peak=0
for s in sorted(all_samples,key=lambda s:s['wall_clock']):
    latest[s['token']]=s
    total=sum(v['tree_rss'] for v in latest.values() if s['wall_clock']-v['wall_clock']<1)
    peak=max(peak,total)
summary={'PASS':True,'rows':rows,'slots':2,'method_threads':1,'workers':2,
         'overlap_s':min(ends)-max(starts),'elapsed_s':max(ends)-min(starts),
         'sum_attempt_s':sum(r['cost_s']for r in rows),'concurrent_sampled_peak_tree_rss':peak,
         'min_free_disk':min(s['free_disk']for s in all_samples),'clock_anomaly':any(s.get('clock_anomaly')for s in all_samples),
         'C_e_real_route_verified':True,'C_e_history':'pinned native command/coverage A0; not healthy-ground-truth',
         'test_opened':False,'main_started':False,
         'limits':['Small two-slot DEV packet; not a full-cohort throughput or ETA measurement.',
                   'No claim of zero OS paging; host-wide available RAM/paging was not logged through this packet.',
                   'No fresh one-worker C-e run added; reuse pinned native reference and existing one-worker OB.']}
atomic(dest/'summary.json',summary)
print(json.dumps(summary,ensure_ascii=False))
