"""Explicit same-input detector repeat; scoped 2 previously selected cases."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import json,csv,sys,time,datetime,importlib,ast
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-013'
summary=json.loads((OUT/'kiem-tra.json').read_text(encoding='utf-8'));RUN=Path(summary['run_dir']).resolve();checks=summary['checks']
ledger=list(csv.DictReader((OUT/'ca-da-chay.csv').open(encoding='utf-8-sig',newline='')))
sys.path.insert(0,'D:/RCA-ext/src/baro');ad=importlib.import_module('baro.anomaly_detection');br=importlib.import_module('baro.root_cause_analysis')
module=ast.parse((OUT/'scripts/kiem_co_che.py').read_text(encoding='utf-8'));exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'functions-only','exec'),globals())
for c in summary['selection']['selected']:
    if c['tag']=='OB':d=pd.read_csv(c['source'])
    else:
        with np.load('D:/RCA-ext/work/T-013/metrics-selected.npz',allow_pickle=False) as z:d=pd.DataFrame(z['values'],columns=z['columns'].tolist()).iloc[:120]
    record(c['case'],c['source'],'N-Sigma detector','explicit same-input repeat '+('full' if c['tag']=='OB' else 'prefix120'),'a')
    log('nsigma_repeat_start',tag=c['tag'],shape=list(d.shape))
    a=ad.nsigma(d);b=ad.nsigma(d);assert a==b
    if c['tag']=='OB':assert a==json.loads((RUN/'OB-nsigma-hits.json').read_text(encoding='utf-8'))['official']
    add(c['tag']+'-nsigma-explicit-repeat',equal=True,count=len(a),T=len(d))
# Degenerate IQR breaks scale invariance for raw CPU unit conversion.
base=pd.DataFrame({'time':range(12),'a_cpu':[0,0,0,0,0,1,2,3,4,5,6,7]})
scaled=base.copy();scaled.a_cpu*=100
o,p=official_rank(base,6,'robust','br','fse-ob');o2,p2=official_rank(scaled,6,'robust','br','fse-ob')
assert p2['a_cpu']['score']==p['a_cpu']['score']*100
record('synthetic','generated','BR RobustScorer','degenerate IQR unit conversion','b')
add('IQR0-unit-scale-invariance-fails',base=p,scaled100=p2)
summary['checks']=checks;summary['run_dir']=str(RUN);dump(OUT/'kiem-tra.json',summary)
tasklog('kiểm lần cuối: explicit same-input N-Sigma repeat OBfull/TTprefix và IQR0 đổi đơn vị; không benchmark mới.')
log('explicit_repeat_complete',checks=len(checks))
