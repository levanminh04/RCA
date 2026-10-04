"""Remaining cheap edge cases found in final SPEC audit; no dataset rerun."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['OMP_NUM_THREADS']=os.environ['OPENBLAS_NUM_THREADS']=os.environ['MKL_NUM_THREADS']='1'
import sys,json,csv,time,datetime,ast,importlib
from pathlib import Path
from functools import partial
import numpy as np
import pandas as pd
from scipy.special import gammaln
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-013'
summary=json.loads((OUT/'kiem-tra.json').read_text(encoding='utf-8'));RUN=Path(summary['run_dir']);checks=summary['checks']
ledger=list(csv.DictReader((OUT/'ca-da-chay.csv').open(encoding='utf-8-sig',newline='')))
sys.path.insert(0,'D:/RCA-ext/src/baro');br=importlib.import_module('baro.root_cause_analysis');ad=importlib.import_module('baro.anomaly_detection');bc=importlib.import_module('baro._bocpd')
module=ast.parse((OUT/'scripts/kiem_co_che.py').read_text(encoding='utf-8'));exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'functions-only','exec'),globals())
for name,d in [
 ('IQR-exactly-one',pd.DataFrame({'time':range(6),'a_cpu':[0,0,1,1,2,3]})),
 ('constant-step-both-halves',pd.DataFrame({'time':range(6),'a_cpu':[1,1,1,9,9,9]})),
 ('infinity',pd.DataFrame({'time':range(6),'a_cpu':[1,np.inf,3,4,5,6]}))]:
    inj=4 if name=='IQR-exactly-one' else 3
    record('synthetic','generated','BR RobustScorer',name,'b')
    try:o,pts=official_rank(d,inj,'robust','br','fse-ob');add('extra-'+name,official=o,points=pts)
    except Exception as e:add('extra-'+name,error=type(e).__name__+': '+str(e))
    if name=='IQR-exactly-one':
        x=d.loc[d.time<inj,'a_cpu'].to_numpy();iqr=np.percentile(x,75)-np.percentile(x,25)
        assert iqr==1 and pts['a_cpu']['scale']==[1.]
        add('scale-one-is-not-IQR-zero',IQR_raw=iqr,scale=pts['a_cpu']['scale'])
stationary=pd.DataFrame({'time':range(200),'a_latency':np.arange(200)%3})
h,de=nsind(stationary);ho=ad.nsigma(stationary);assert h==ho==[]
record('synthetic','generated','N-Sigma detector','unchanged repeated periodic normal control','b')
add('extra-nsigma-normal-control',hits=ho,independent=h)
p=bc.MultivariateT(dims=1).pdf(np.array([0.]))[0]
ind=np.exp(gammaln(1.5)-gammaln(1)-.5*np.log(2*np.pi))
assert abs(p-ind)<1e-14
add('hand-prior-density',x1=0.,dims=1,official=float(p),independent=float(ind),posterior_after_first=[.02,.98])
# Column duplicates/names and mapping risks demonstrated by two official mappings.
mapping={'a-db_cpu':'a','a_cpu':'a','name_with_under_cpu':'name'}
add('service-name-mapping',BR={k:k.split('_')[0] for k in mapping},RE={k:k.split('_')[0].replace('-db','') for k in mapping},loss_of_underscore_service_names=True)

# Quantile computation only (not method run) excluded from method ledger deliberately.
summary['checks']=checks;summary['final_audit_additions']='inf, raw-IQR1, constant step, stationary detector, prior density, service mapping'
dump(OUT/'kiem-tra.json',summary)
log('additional_edge_checks_complete',count=len(checks))
tasklog('bước 6 tự soát: bổ sung kiểm rẻ còn thiếu inf/IQR thật1/bước nhảy hằng/normal periodic/prior density/mapping; không lặp lại dataset runs.')
