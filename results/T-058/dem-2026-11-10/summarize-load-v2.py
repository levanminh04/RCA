"""Operator analysis only, after the method outputs have been hashed."""
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parent
ledger=[json.loads(x) for x in (ROOT/'so-tiem-loi.jsonl').read_text(encoding='utf8').splitlines()]
previous='0'*64
for original in ledger:
    row=dict(original); digest=row.pop('sha256')
    encoded=json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
    if row['previous_sha256']!=previous or hashlib.sha256(encoded.encode()).hexdigest()!=digest:
        raise SystemExit('Ledger hash chain invalid')
    previous=digest
start=next(x['confirmed']['epoch_ns']/1e9 for x in ledger if x['event']=='intervention_start')
end=next(x['confirmed']['epoch_ns']/1e9 for x in ledger if x['event']=='intervention_end')
rows=[]
for runid,offset in [('light-load.jsonl',0),('light-load-v2.jsonl',3600)]:
    for line in (ROOT/runid).read_text().splitlines():
        row=json.loads(line); row['sequence']+=offset; row['source_load_file']=runid; rows.append(row)
for opaque in ['c12e47ab','f4a8c021']:
    folder=ROOT/'rca-ban-dau/outputs'/opaque
    summary=json.loads((folder/'summary.json').read_text(encoding='utf8'))
    for n,expected in enumerate(summary['output_sha256'],1):
        if hashlib.sha256((folder/f'method-output-{n}.json').read_bytes()).hexdigest()!=expected:
            raise SystemExit('Method output hash mismatch before label analysis')
rows.sort(key=lambda x:x['sequence'])

def summary(data):
    if not data: return {'requests':0}
    latency=sorted(x['latency_ms'] for x in data)
    return {'requests':len(data),'status_counts':dict(Counter(str(x['status']) for x in data)),
            'client_errors':dict(Counter(x['error'] for x in data if x['error'])),
            'latency_mean_ms':statistics.mean(latency),'latency_p95_ms':latency[min(len(latency)-1,int(.95*len(latency)))],
            'latency_max_ms':max(latency),'schedule_lag_max_ms':max(x['schedule_lag_ms'] for x in data),
            'first_scheduled_epoch':min(x['scheduled_epoch'] for x in data),'last_scheduled_epoch':max(x['scheduled_epoch'] for x in data)}

windows={'before_5m':[start-300,start],'during':[start,end],'after_5m':[end,end+300]}
result={'ledger_chain_valid':True,'ledger_last_sha256':previous,'intervention_start_epoch':start,
        'intervention_end_epoch':end,'confirmed_duration_seconds':end-start,'total':summary(rows),'windows':{},
        'independence':'This client log and ledger are not queried by the adapter or passed to M1',
        'limitations':['A Docker pause confirmation is an intervention boundary, not an application impact onset',
                       'Client start and completion bracket the observation of an HTTP failure; no sub-request failure onset is inferred',
                       'The first non-200 after intervention is an observed association, not a validated causal label for every failed request']}
for name,(lo,hi) in windows.items():
    data=[r for r in rows if lo<=r['epoch']<hi]
    result['windows'][name]={'bounds_epoch':[lo,hi],**summary(data),
                            'by_path':{path:summary([r for r in data if r['path']==path]) for path in sorted({r['path'] for r in data})}}
bad=[r for r in rows if r['epoch']>=start and (r['status']!=200 or r['error'])]
result['first_non200_after_intervention']=bad[0] if bad else None
bad_end=max((r['completed_epoch'] for r in bad),default=end)
after=[r for r in rows if r['epoch']>=max(end,bad_end) and r['status']==200 and '/availability' in r['path']]
result['first_availability_200_started_after_last_failure_completed']=after[0] if after else None
result['sequence_unique']=len({r['sequence'] for r in rows})==len(rows)
result['sequence_complete_0_to_4799']={r['sequence'] for r in rows}==set(range(4800))
(ROOT/'load-impact.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'duration':end-start,'total':result['total'],'windows':{k:{'requests':v['requests'],'status_counts':v['status_counts']} for k,v in result['windows'].items()}},indent=2))
