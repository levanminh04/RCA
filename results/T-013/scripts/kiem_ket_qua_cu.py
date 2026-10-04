"""Audit existing files, filter case-level artifacts before reading/printing.
No author method calls, no datasets outside approved locations.
"""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from pathlib import Path
import tarfile,json,re,hashlib,csv
import pandas as pd
import numpy as np
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-013'
def dump(name,o):(OUT/'trung-gian'/name).write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
zpath=ROOT/'results/T-007/runs/py312-pin/bocpd.tar.gz'
with tarfile.open(zpath) as z:
    f=z.extractfile('bocpd/tien-do.jsonl');rows=[]
    for line in f:
        r=json.loads(line)
        if str(r.get('case','')).startswith('fse-ob/'):rows.append(r)
# Field names may vary; save approved case records only, no other cases.
dump('T007-bocpd-allowed-records.json',rows)
print('T007 allowed records',len(rows),'first keys',list(rows[0]) if rows else [])

rawiqr=[]
for p in sorted(Path('D:/RCA-ext/data/torai-OB').glob('**/simple_metrics.csv')):
    d=pd.read_csv(p);d=d.loc[:,~d.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
    inj=int((p.parent/'inject_time.txt').read_text().strip());a=d[d.time<inj].tail(300);b=d[d.time>=inj].head(300)
    if 'redis_diskio' not in a:continue
    x=a.redis_diskio.to_numpy();q25,med,q75=np.percentile(x,[25,50,75]);iqr=q75-q25
    rawiqr.append({'ca':str(p.parent.relative_to('D:/RCA-ext/data/torai-OB')).replace('\\','/'),'file_nguon':str(p),'n_normal':len(x),'q25':float(q25),'median':float(med),'q75':float(q75),'IQR_raw':float(iqr),'normal_constant':bool(np.all(x==x[0])),'post_constant':bool((b.redis_diskio==b.redis_diskio.iloc[0]).all()),'scale_expected':1. if iqr<10*np.finfo(float).eps else float(iqr),'purpose':'raw baseline quantile audit only; no ranking/method benchmark'})
pd.DataFrame(rawiqr).to_csv(OUT/'trung-gian/T006-redis-IQR-raw.csv',index=False,encoding='utf-8-sig')
dump('T006-redis-IQR-summary.json',{'cases':len(rawiqr),'raw_zero':sum(r['IQR_raw']==0 for r in rawiqr),'raw_one':sum(r['IQR_raw']==1 for r in rawiqr),'zero_nonconstant':sum(r['IQR_raw']==0 and not r['normal_constant'] for r in rawiqr),'all_scales_one':all(r['scale_expected']==1 for r in rawiqr),'range_raw_IQR':[min(r['IQR_raw'] for r in rawiqr),max(r['IQR_raw'] for r in rawiqr)]})
# Per-case data in old BARO A artifact is restricted to approved fse-ob dataset.
art=ROOT/'results/T-006/runs/x1-py312pin-reproduce-baro-fse-ob-all.tar.gz'
with tarfile.open(art) as z:
    members=[m for m in z.getmembers() if m.isfile() and (m.name.endswith('stdout.log') or m.name.endswith('ket-qua-vi-du.json'))]
    texts={m.name:z.extractfile(m).read().decode('utf-8','replace') for m in members}
dump('T006-moc-A-reused.json',{'archive':str(art),'safe_non_case_members':texts,'scope':'aggregate mốc A; individual scores independently checked by T013'})

# Read completed task main reports; task T004 does not yet exist.
reports=[]
for n in range(13):
    paths=sorted((ROOT/'results'/f'T-{n:03}').glob('*.md'))
    if n==0:paths=[ROOT/'tasks/T-000-nen-tang/SPEC.md',ROOT/'tasks/T-000-nen-tang/LOG.md']
    if n==4:reports.append({'task':'T-004','scope':'not implemented in STATE; no old output to audit'});continue
    for p in paths:
        s=p.read_text(encoding='utf-8-sig')
        hits=[{'line':i+1,'text':line} for i,line in enumerate(s.splitlines()) if any(k in line.lower() for k in ['baro','bocpd','n-sigma','robustscorer','biên','chế độ b','phát hiện','rò nhãn'])]
        reports.append({'task':f'T-{n:03}','file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'relevant_lines':hits,'scope':'method/input/boundary claims relevant T013; other methods not re-benchmarked'})
dump('task-cu-relevant-source-audit.json',reports)
print('raw IQR baseline audit',len(rawiqr),'reports',len(reports))
