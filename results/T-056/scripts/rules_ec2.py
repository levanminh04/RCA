import json,sys,re
import numpy as np, pyarrow.parquet as pq
from pathlib import Path
EPS=np.finfo(float).eps
req=json.loads(sys.stdin.read()); out={}
kw=re.compile('ERROR|FAIL|EXCEPTION',re.I)
for o,c in sorted(req['cases'].items()):
    base=Path(c['data_root']); t=int(c['t'])
    m=pq.read_table(base/c['files']['metrics.parquet']).to_pandas()
    tm=m['time'].to_numpy(); nm=(tm>=t-300)&(tm<t); am=(tm>=t)&(tm<t+300)
    svc={}
    for col in m.columns:
        if col=='time' or '_' not in col: continue
        own=col.rsplit('_',1)[0]
        N=m.loc[nm,col].to_numpy(float); A=m.loc[am,col].to_numpy(float)
        N=N[np.isfinite(N)]; A=A[np.isfinite(A)]
        if len(N)<2 or not len(A): continue
        mu,sd=N.mean(),N.std()
        ev=int((A>mu+3*sd).sum())
        zm=float((A.mean()-mu)/sd) if sd>0 else (0.0 if A.mean()==mu else 1e9)
        med=np.median(N); iqr=np.percentile(N,75)-np.percentile(N,25); cc=iqr if iqr>=10*EPS else 1.0
        zp=float((A.max()-med)/cc)
        s=svc.setdefault(own,{'events':0,'max_zmean':-1e18,'max_zpoint':-1e18,'n_cols_ev':0})
        s['events']+=ev; s['n_cols_ev']+=int(ev>0); s['max_zmean']=max(s['max_zmean'],abs(zm)); s['max_zpoint']=max(s['max_zpoint'],zp)
    lg={}
    if 'logs.parquet' in c['files']:
        try:
            l=pq.read_table(base/c['files']['logs.parquet']).to_pandas()
            tcol='timestamp'; ent='container_name' if 'container_name' in l.columns else None
            if ent:
                ts=l[tcol].astype('int64'); 
                if ts.max()>1e12: ts=ts//10**9
                a=l[(ts>=t)&(ts<t+300)]
                for e,g in a.groupby(ent): lg[e]=int(g['message'].fillna('').astype(str).str.contains('ERROR|FAIL|EXCEPTION',case=False,regex=True).sum())
        except Exception as ex: lg={'_err':str(ex)[:80]}
    out[o]={'dataset':c['dataset'],'svc':svc,'logerr_A':lg}
print(json.dumps(out))
