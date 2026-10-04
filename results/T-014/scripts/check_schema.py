"""Read headers/schema only in the explicitly permitted data directories."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,csv
from pathlib import Path
import pyarrow.parquet as pq
sys.path.insert(0,'D:/RCA-flashticket/src')
from circa_kien_truc import metric_mapping
repo=Path('D:/RCA-flashticket');out=repo/'results/T-014';records=[]
def save(path,columns,kind):
    mapping=metric_mapping(columns)
    records.append(dict(source=str(path),inspection=kind,columns=len(columns),mapped=len([r for r in mapping if r['status']=='mapped']),unknown=[r for r in mapping if r['status']!='mapped'],suffixes=sorted({r['metric'] for r in mapping if r['status']=='mapped'})))
for dirname in ['RE1-OB','RE1-SS','fse-ob','fse-ss','torai-OB','torai-SS']:
    base=Path('D:/RCA-ext/data')/dirname
    for path in sorted(base.glob('*/*/*.csv')):
        if path.name not in ['data.csv','simple_data.csv','simple_metrics.csv']:continue
        with path.open(encoding='utf-8-sig',newline='') as f:columns=next(csv.reader(f))
        save(path,columns,'CSV header only; no method run')
for case in ['re1ob_productcatalogservice_cpu_3','re2ob_productcatalogservice_loss_1']:
    path=repo/'data/rcaeval'/case/'metrics.parquet'
    if path.exists():save(path,pq.read_schema(path).names,'Parquet schema only; no method run')
# Explicit single permitted torai-TT case; never enumerate other TT directories.
path=Path('D:/RCA-ext/data/torai-TT/ts-route-service_socket/1/simple_metrics.csv')
if path.exists():
    with path.open(encoding='utf-8-sig',newline='') as f:save(path,next(csv.reader(f)),'CSV header only; one explicitly permitted TT case')
result=dict(inspected_files=len(records),unknown_total=sum(len(r['unknown']) for r in records),records=records,limits='No locked data; no additional RE2-TT; not all possible future RCAEval schemas')
(out/'runs/schema-other-permitted.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
summary={}
for r in records:
    group=Path(r['source']).parts[3]
    s=summary.setdefault(group,dict(files=0,mapped_occurrences=0,unmapped_occurrences=0,unknown_columns=set(),suffixes=set()))
    s['files']+=1;s['mapped_occurrences']+=r['mapped'];s['unmapped_occurrences']+=len(r['unknown'])
    s['unknown_columns'].update(x['column'] for x in r['unknown']);s['suffixes'].update(r['suffixes'])
for s in summary.values():s['unknown_columns']=sorted(s['unknown_columns']);s['suffixes']=sorted(s['suffixes'])
(out/'runs/schema-other-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(inspected_files=result['inspected_files'],unknown_total=result['unknown_total'],suffixes=sorted({s for r in records for s in r['suffixes']}))))
