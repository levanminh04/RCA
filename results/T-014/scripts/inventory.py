import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys, json, hashlib, csv, subprocess
from pathlib import Path
import pandas as pd
import numpy as np
sys.path.insert(0, 'D:/RCA-ext/src/RCAEval')
from RCAEval.io.time_series import preprocess
ROOT = Path('D:/RCA-flashticket')
OUT = ROOT/'results/T-014'
cases = sorted(p for p in (ROOT/'data/rcaeval').glob('re2tt_*') if p.is_dir())
assert len(cases)==30
rows=[]
for case in cases:
    data=pd.read_parquet(case/'metrics.parquet')
    meta=case/'inject_time.txt'
    if not meta.exists(): meta=ROOT/'results/T-002/local-inspection/run-002/injection-metadata'/f'{case.name}.txt'
    td=int(meta.read_text().strip())
    data=data.loc[:,~data.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
    data=data.rename(columns={c:c.replace('_latency-90','_latency') for c in data if c.endswith('_latency-90')})
    win=pd.concat([data[data.time<td].iloc[-300:],data[data.time>=td].iloc[:300]],ignore_index=True)
    clean=preprocess(win.copy(),dataset='re2-tt')
    raw=list(data.columns)
    rows.append(dict(case=case.name,source=str(case/'metrics.parquet'),injection_source=str(meta),injection_sha256=hashlib.sha256(meta.read_bytes()).hexdigest(),rows=len(data),window_rows=len(win),raw_columns=raw,processed_columns=list(clean),processed_count=len(clean.columns),raw_types=sorted(set(c.rsplit('_',1)[-1] for c in raw if c!='time')),constant_raw=[c for c in raw if c!='time' and data[c].nunique()==1],inject_time=td,window_first=float(win.time.iloc[0]),window_last=float(win.time.iloc[-1]),sha256=hashlib.sha256((case/'metrics.parquet').read_bytes()).hexdigest()))
chosen=min(rows,key=lambda x:(x['processed_count'],x['case']))
(OUT/'runs/inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'runs/selection-before-scores.json').write_text(json.dumps(dict(rule='minimum processed_count on ±300s, lexicographic case tie; no method scores read',selected=chosen['case'],processed_count=chosen['processed_count'],count=len(rows)),indent=2),encoding='utf-8')
print(json.dumps(dict(selected=chosen['case'],count=len(rows),processed_min=min(r['processed_count'] for r in rows),processed_max=max(r['processed_count'] for r in rows),suffixes=sorted(set(t for r in rows for t in r['raw_types'])))))
