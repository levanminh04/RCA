"""Read verified frozen sources; emit compact engine-only transport inputs."""
import hashlib,importlib.util,json,pathlib,sys,time
import numpy as np
import pandas as pd
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
def run():
 p=w.OUT/'migration-inputs-001';p.mkdir(exist_ok=False);rows=[]
 for ci,item in enumerate(w.S['cases']):
  oid=item['opaque_id'];rel,z=w.input_arrays(oid);rawpath=w.raw_path(item,'metrics.parquet');frame=pd.read_parquet(rawpath)
  cols=[c for c in frame if c!='time' and 'queue-master' not in c and 'rabbitmq_' not in c and ('latency-50' in c or '_error' in c)]
  raw=frame[cols].to_numpy(float);q=p/(oid+'.npz')
  np.savez_compressed(q,**z,causal_raw=raw,causal_columns=np.array(cols,dtype=str))
  b=q.read_bytes();rows.append({'case':ci+1,'opaque_id':oid,'file':q.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'source_native':{'relative':rel,**w.CAT[rel]},'source_raw':{'bytes':rawpath.stat().st_size,'sha256':w.sha(rawpath)},'X_shape':list(z['X'].shape),'raw_shape':list(raw.shape)})
 native=pathlib.Path(__import__('inspect').getsourcefile(w.MultivariateT));b=native.read_bytes();(p/'_bocpd.py').write_bytes(b)
 manifest={'status':'COMPLETE','cases':rows,'native':{'file':'_bocpd.py','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},'source_worker_sha256':w.sha(w.OUT/'worker-v3.py'),'environment':{'numpy':w.np.__version__,'scipy':w.scipy.__version__,'pandas':w.pd.__version__,'python':sys.version},'array_contract':'X/times/columns/m/CP_flags copied unchanged from pinned native source. causal_raw is the unchanged raw static selector column array; no scaler/mask/engine change; no R/predictive_density/labels copied.'}
 (p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':'COMPLETE','case_count':len(rows),'compressed_bytes':sum(x['bytes'] for x in rows),'bytes_by_case':[{k:x[k] for k in ['case','bytes','X_shape','raw_shape']} for x in rows]},ensure_ascii=False))
if __name__=='__main__':run()
