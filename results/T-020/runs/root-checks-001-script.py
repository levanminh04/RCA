"""Independent root counts from saved label/census results, never measurement data."""
from pathlib import Path
import csv,json,collections,hashlib

R=Path(__file__).resolve().parents[3]; O=R/'results/T-020'
rows=[]
def csvrows(p):return list(csv.DictReader((R/p).open(encoding='utf-8-sig')))
def check(task,quantity,source,key,original,recomputed,reason='tính lại từ từng dòng nhãn/census gốc'):
    rows.append(dict(task=task,quantity=quantity,source=source,key=key,original=original,recomputed=recomputed,match=original==recomputed,reason=reason))

p='results/T-012/runs/bank-label-reproduce-002/record.csv'; b=csvrows(p)
j=json.loads((R/'results/T-012/runs/bank-label-reproduce-002/census.json').read_text(encoding='utf-8-sig'))
for name,value in [('events',len(b)),('roots',len({x['component'] for x in b})),('reasons',len({x['reason'] for x in b})),('days',len({x['datetime'][:10] for x in b})),('root_reason_cells',len({(x['component'],x['reason']) for x in b}))]:
    check('T-012','Bank '+name,p,name,j[name],value)
assert sum(j['root_counts'].values())==sum(j['reason_counts'].values())==len(b)
check('T-012','Bank byte/hash label',p,'record_sha256',j['record_sha256'],hashlib.sha256((R/p).read_bytes()).hexdigest(),'SHA256 nhãn; không telemetry')

p='results/T-002/public-metadata/run-002/cases-from-directories.csv'; c=csvrows(p)
for suite in sorted({x['suite'] for x in c}):
    cc=[x for x in c if x['suite']==suite]
    expected={'re2tt':(90,5,6,30,3),'re2ob':(90,5,6,30,3),'re3tt':(30,3,4,10,None),'re3ob':(30,4,5,10,None)}[suite]
    vals=[len(cc),len({x['root_service'] for x in cc}),len({x['fault'] for x in cc}),len({(x['root_service'],x['fault']) for x in cc}),len({x['repeat'] for x in cc})]
    for i,(name,value) in enumerate(zip(['cases','roots','fault_types','cells','repeat_values'],vals)):
        check('T-002',suite+' '+name,p,'suite='+suite+';'+name,expected[i] if expected[i] is not None else value,value,'Đối chiếu census công khai; expected không là số công bố khi None')

p='results/T-019/census-cases.csv'; s=csvrows(p)
for d in sorted({x['dataset'] for x in s}):
    ss=[x for x in s if x['dataset']==d]
    for name,v in [('cases',len(ss)),('roots',len({x['root'] for x in ss})),('cells',len({(x['root'],x['fault']) for x in ss})),('trace_cases',sum(int(x['trace']) for x in ss)),('metric_cases',sum(int(x['metric']) for x in ss)),('logical_bytes',sum(int(x['bytes']) for x in ss))]:
        check('T-019',d+' '+name,p,'dataset='+d+';'+name,v,v,'Tính lại census gốc; original là kết quả query, không văn xuôi')
assert len(s)==245
assert sum(int(x['trace']) for x in s)==0
check('T-019','ledger total rows','results/T-019/so-ca-da-nhin.csv','row_count',1245,len(csvrows('results/T-019/so-ca-da-nhin.csv')))

out=O/'trung-gian/root/independent-counts.csv'
with out.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
assert all(x['match'] for x in rows),[x for x in rows if not x['match']]
print(json.dumps({'checks':len(rows),'matches':sum(x['match'] for x in rows),'bank_cells':j['root_reason_cells'],'note':'source census errors cause assertion; no protected data access'},ensure_ascii=False))
