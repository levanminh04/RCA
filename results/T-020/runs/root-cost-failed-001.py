"""Historical runtime aggregation only; never run a method or contact EC2."""
from pathlib import Path
import csv,json,hashlib,math
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-020';rows=[];inputs=[]
def add(task,source,key,expected,got,reason):
    ok=math.isclose(float(expected),float(got),rel_tol=1e-9,abs_tol=1e-7)
    rows.append(dict(task=task,quantity=key,source=source,key=key,original=expected,recomputed=got,match=ok,reason=reason));assert ok,(key,expected,got)
runtime=list(csv.DictReader((OUT/'trung-gian/method_evidence/runtime.csv').open(encoding='utf-8-sig')))
for r in runtime:
    if r['source'].startswith('D:') and '*' not in r['source']:
        path=Path(r['source'].split('#')[0]);b=path.read_bytes()
        inputs.append({'path':str(path),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'kind':'supplemental historical timer JSONL, no telemetry','mtime_ns':path.stat().st_mtime_ns})
        parsed=[json.loads(line) for line in b.decode('utf-8').splitlines() if line.strip()]
        total=sum(x['giay'] for x in parsed)
        add('T-016',str(path),'sum(giay)',r['observed_total_seconds'],total,'root sum every saved timer record; no measurement data')
        add('T-016',str(path),'case count',r['observed_cases'],len(parsed),'root JSONL rows')
        projected=total/len(parsed)*90*3
        add('T-016',str(path),'CANDIDATE projected 90cases×3seeds',r['projection_seed3_seconds'],projected,'unverified equal-case/hardware/shape assumption; multiplication only')
cost=json.loads((ROOT/'results/T-014/runs/followup-cost.json').read_text(encoding='utf-8'))
add('T-014','results/T-014/runs/followup-cost.json','recorded_worker_seconds',cost['recorded_worker_seconds'],cost['old_worker_wall_seconds']+cost['new_worker_wall_seconds'],'sum disjoint saved worker blocks')
add('T-014','results/T-014/runs/followup-cost.json','recorded_worker_plus_queue_seconds',cost['recorded_worker_plus_queue_seconds'],cost['old_worker_wall_seconds']+cost['new_worker_wall_seconds']+cost['historical_queue_without_worker_seconds'],'add separately documented queue, exclude900reservation')
gdn=json.loads((ROOT/'results/T-018/runs/b6b7-phan-tich.json').read_text(encoding='utf-8'))
times=[x['s_hoc'] for x in gdn['luot'].values() if 's_hoc' in x]
add('T-018','results/T-018/runs/b6b7-phan-tich.json','fit observed min seconds',257.35,min(times),'root min recorded fit timers; not normal calibration')
add('T-018','results/T-018/runs/b6b7-phan-tich.json','fit observed max seconds',1928.69,max(times),'root max recorded fit timers')
t5=[json.loads(x) for x in (ROOT/'results/T-005/runs/ket-qua-do.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
for expected,method in [(1440.133,'bocpd'),(101.053,'microrank'),(237.518,'microrank'),(1028.822,'gdn_hoc'),(11.685,'gdn_suy_luan')]:
    candidates=[x for x in t5 if x.get('method_s')==expected]
    assert len(candidates)==1
    add('T-005','results/T-005/runs/ket-qua-do.jsonl',f'{method} recorded timer',expected,candidates[0]['method_s'],'root exact timer-field query; no successful runtime inferred from timeout')
    if method in ['bocpd','microrank']:
        add('T-005','results/T-005/runs/ket-qua-do.jsonl',f'{method} projected90×3 from{expected}',expected*270,candidates[0]['method_s']*90*3,'CANDIDATE arithmetic only; same-condition assumption unverified')
with (OUT/'trung-gian/root/root-cost-checks.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'trung-gian/root/supplemental-inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('root cost checks',len(rows),'PASS')
