"""Index numeric scalar claims from aggregate results, without data payload access.

Select deterministic review candidates; values are not automatically validated.
This inventory is distinct from a successful source/recalculation check.
"""
from pathlib import Path
import csv,json,hashlib,re
R=Path(__file__).resolve().parents[3]; O=R/'results/T-020/trung-gian/root'
rows=[]; exclusions=[]
keywords=re.compile(r'count|census|summary|profile|result|verification|aggregate|check|timing|cost|chi-phi|kiem-tra|ledger',re.I)
exclude=re.compile(r'sources?|source-before|before|truoc-|snapshot|node_modules|input|posterior|sample.*raw|raw.*sample',re.I)
def walk(j,key=''):
    if isinstance(j,dict):
        for k,v in j.items():yield from walk(v,key+'/'+str(k))
    elif isinstance(j,list):
        # Arrays of numbers can be saved raw measurement values, not summaries.
        if j and all(isinstance(x,(int,float)) for x in j):return
        for i,v in enumerate(j):yield from walk(v,key+'/'+str(i))
    elif isinstance(j,(int,float)) and not isinstance(j,bool):yield key,j
for task in range(1,20):
    d=R/f'results/T-{task:03d}'
    if not d.exists():
        exclusions.append({'path':str(d.relative_to(R)), 'reason':'task chưa triển khai/không có kết quả'});continue
    for p in sorted(d.rglob('*.json')):
        path=p.relative_to(R).as_posix()
        if not keywords.search(p.name) or exclude.search(path):continue
        if p.stat().st_size>8_000_000:
            exclusions.append({'path':path,'reason':'JSON lớn: inventory không đọc payload; scalar có ích phải lấy bằng query cụ thể trong checks'});continue
        try:j=json.loads(p.read_text(encoding='utf-8-sig'))
        except (ValueError,UnicodeError):continue
        for key,value in walk(j):
            if re.search(r'timestamp|mtime|epoch_time|inject_time|sha|crc|seed|port|index|version|start_time|end_time',key,re.I):continue
            priority=hashlib.sha256(f'20261004|T-{task:03d}|{path}|{key}'.encode()).hexdigest()
            rows.append({'task':f'T-{task:03d}','path':path,'key':key,'value':value,'sampling_hash':priority,'selected':'False','check_state':'chưa đối chiếu với phép tính gốc'})
for task in sorted({x['task'] for x in rows}):
    candidates=sorted((x for x in rows if x['task']==task),key=lambda x:x['sampling_hash'])
    for x in candidates[:5]:x['selected']='True'
with (O/'numeric-leaves.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(O/'numeric-inventory-exclusions.json').write_text(json.dumps(exclusions,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'scalar_claims':len(rows),'tasks':sorted({x['task'] for x in rows}),'selected':sum(x['selected']=='True' for x in rows),'not_evidence_of_match':True},ensure_ascii=False))
