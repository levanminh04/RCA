"""Resume valid saved checks after packaging command failed; no full rerun."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['OMP_NUM_THREADS']=os.environ['OPENBLAS_NUM_THREADS']=os.environ['MKL_NUM_THREADS']='1'
import sys,json,csv,time,datetime,subprocess,hashlib,ast,importlib
from functools import partial
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import gammaln
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-013'
RUN=Path(sys.argv[1]);assert RUN.resolve().is_relative_to((OUT/'runs').resolve())
checks=json.loads((RUN/'checks-partial.json').read_text(encoding='utf-8'))
ledger=list(csv.DictReader((OUT/'ca-da-chay.csv').open(encoding='utf-8-sig',newline='')))
sys.path.insert(0,'D:/RCA-ext/src/baro')
br=importlib.import_module('baro.root_cause_analysis');ad=importlib.import_module('baro.anomaly_detection');bc=importlib.import_module('baro._bocpd')
# Extract only function definitions from the standalone audit, never execute its top-level runs.
module=ast.parse((OUT/'scripts/kiem_co_che.py').read_text(encoding='utf-8'))
defs=ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
exec(compile(defs,'T013-functions-only','exec'),globals())
log('resume_valid_saved_checks',count=len(checks),reason='pip missing in uv venv; all method checks already saved')
selection=json.loads((OUT/'trung-gian/chon-ca.json').read_text(encoding='utf-8'))
ob=next(c for c in selection['selected'] if c['tag']=='OB');d=clean(pd.read_csv(ob['source']))
assert hashfile(ob['source'])==hashfile('D:/RCA-ext/dl/baro-simple_data.csv')
rows,ranks=compare_ranks('OB-README-A-cut243',d,None,'robust','br',ob['case'],ob['source'],'fse-ob',cut=243,reason='a')
expected=json.loads((OUT/'doi-chieu-moc.json').read_text(encoding='utf-8'))['README_A']['top5']
assert ranks[:5]==expected
add('README-A-ranker-direct',matches_top5=True,cut=243,cut_source='T006 previously reproduced BOCPD; no new detector full run',expected=expected)
# Include even sample size and mixed decline dict counterexamples as well as independent paper score.
for name,post in [('even-positive',[4,5]),('even-negative',[-5,-4]),('mixed-decline',[-10,2])]:
    normal=[0,1,2,3];metrics={'a_cpu':list(zip(range(6),normal+post))}
    official=br.robust_scorer(metrics,inject_time=4)['scores'][0][1]
    median=normal[2];iqr=normal[3]-normal[1];independent=abs(max(post)-median)/iqr
    assert official==independent
    q25,q50,q75=np.percentile(normal,[25,50,75]);paper=max(abs(np.array(post)-q50))/(q75-q25)
    signed=max((np.array(post)-q50)/(q75-q25))
    add('dict-vs-dataframe-'+name,normal=normal,post=post,dict_official=official,dict_independent=independent,dataframe_formula=float(signed),paper_formula=float(paper),dict_center=median,dict_iqr=iqr,dataframe_center=q50,dataframe_iqr=q75-q25)
# Concrete byte/memory/sentinel audits, restricted to approved fse-ob artifact.
old=json.loads((OUT/'trung-gian/T007-bocpd-allowed-records.json').read_text(encoding='utf-8'))
without=[[cp for cp in r['cps'] if cp[0]<600] for r in old]
tp=sum(bool(cp) for cp in without);fp=sum(bool(cp) and cp[0][0]<300 for cp in without)
sent={'n':len(old),'with_sentinel':sum(any(cp[0]==600 for cp in r['cps']) for r in old),'only_sentinel':sum(len(r['cps'])==1 and r['cps'][0][0]==600 for r in old),'first_sentinel':sum(r['cps'][0][0]==600 for r in old),'before':{'tp':sum(r['tp'] for r in old),'fp':sum(r['fp'] for r in old)},'after_remove_sentinel':{'tp':tp,'fp':fp,'precision':tp/(tp+fp),'recall':tp/len(old),'f1':2*(tp/(tp+fp))*(tp/len(old))/((tp/(tp+fp))+(tp/len(old)))} }
runtime_rows=[json.loads(s) for s in (ROOT/'results/T-005/runs/ket-qua-do.jsonl').read_text(encoding='utf-8').splitlines()]
runtime=next(r for r in runtime_rows if r.get('muc')=='bocpd' and r.get('bien_the')=='win') if any(r.get('muc')=='bocpd' for r in runtime_rows) else None
print('T005 runtime keys',list(runtime_rows[16]),flush=True)
cost={'scenario_not_measurement':[{'N':30,'T':T,'predictive_evals':30*T*(T+1)//2,'R_peak_MiB':8*(T+1)**2/2**20} for T in [600,1441]],'T005_reference_1440_133_sec':runtime['method_s'],'hours_30_equal_cases':runtime['method_s']*30/3600,'hours_90_equal_cases':runtime['method_s']*90/3600,'assumption':'same T,d,hardware,library and load; unverified extrapolation','source':'results/T-005/runs/ket-qua-do.jsonl line17','sentinel':sent,'T007_total_shared_machine_sec':sum(r['giay'] for r in old)}
dump(OUT/'trung-gian/chi-phi-va-sentinel.json',cost)
add('T007-sentinel-audit',**sent)

prior_data=prep_boc(pd.DataFrame({'time':range(12),'a_latency':np.arange(12)%3})).to_numpy()
for mu,k in [(.5,1.),(0.,2.)]:
    Ri,mi,cpi=bocpd_ind(prior_data,mu0=mu,kappa0=k)
    Ro,mo=bc.online_changepoint_detection(prior_data,partial(bc.constant_hazard,50),bc.MultivariateT(dims=1,mu=mu,kappa=k))
    err=float(np.max(abs(Ri-Ro)));assert err<1e-10
    add('prior-change-mu'+str(mu)+'-k'+str(k),posterior_error=err,cps=cpi,prior_mu=mu,prior_kappa=k)
# Mathematical detector affine invariance, output compared with original function.
synthetic=pd.DataFrame({'time':range(110),'a_latency':np.r_[np.arange(100)%3,20.,np.arange(9)%3]})
trans=synthetic.copy();trans.a_latency=(trans.a_latency-trans.a_latency.min())/(trans.a_latency.max()-trans.a_latency.min())
o1=ad.nsigma(synthetic);o2=ad.nsigma(trans);assert o1==o2
add('nsigma-affine-invariance',original=o1,normalized=o2,equal=True)
scaled=synthetic.copy();scaled.time=synthetic.time*1000
o3=ad.nsigma(scaled);assert o3==[x*1000 for x in o1]
add('nsigma-time-unit-ms',original=o1,milliseconds=o3)
# Dataset labels are untouched by all calculations above.
freeze=subprocess.check_output(['D:/RCA-ext/envs/tools/Scripts/uv.exe','pip','freeze','--python',sys.executable],text=True,encoding='utf-8')
(OUT/'trung-gian/freeze-py312-pin.txt').write_text(freeze,encoding='utf-8')
window=json.loads((OUT/'trung-gian/cua-so-cu.json').read_text(encoding='utf-8'))
summary={'run_dir':str(RUN),'checks':checks,'selection':selection,'window':window,'python':sys.version,'executable':sys.executable,'elapsed_is_official_benchmark':False,'status':'complete','all_inputs_scoped':True,'no_locked_data':True,'resumed_after_failure':'uv venv has no pip; method results reused; metadata frozen via uv'}
dump(OUT/'kiem-tra.json',summary)
tasklog('bước 4: dùng lại valid outputs sau lệnh pip-freeze lỗi; metadata bằng uv, thêm mốc A ranker 243, dict/prior/affine/sentinel audits. Không chạy lại phần đã khớp.')
log('complete',checks=len(checks),ledger=len(ledger))
