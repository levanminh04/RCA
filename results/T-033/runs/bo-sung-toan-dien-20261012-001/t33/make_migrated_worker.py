"""Create immutable layout wrapper; engine and preprocessing body unchanged."""
import hashlib,pathlib
p=pathlib.Path(__file__).resolve().parent;s=(p/'worker-v3.py').read_text()
body=s[s.index('def causal('):]
old="  if len(sys.argv)>2 and ci%2!=int(sys.argv[2]):continue"
assert old in body;body=body.replace(old,"  if ci+1 not in ASSIGNED or (len(sys.argv)>2 and ci%2!=int(sys.argv[2])):continue")
old="  frame=pd.read_parquet(raw_path(item,'metrics.parquet'))\n  cols=[c for c in frame if c!='time' and 'queue-master' not in c and 'rabbitmq_' not in c and ('latency-50' in c or '_error' in c)]\n  raw=frame[cols].to_numpy(float)"
assert old in body;body=body.replace(old,"  raw,cols=raw_selected(oid)")
body=body.replace("len([i for i in range(len(S['cases'])) if part<0 or i%2==part])","len([i for i in range(len(S['cases'])) if i+1 in ASSIGNED and (part<0 or i%2==part)])")
header='''"""T033 migration wrapper. Original v3 engine/preprocessing body unchanged."""
import argparse, hashlib, importlib.util, inspect, json, os, pathlib, platform, sys, time, traceback
import numpy as np
import pandas as pd
import scipy
from scipy.stats import multivariate_t
from functools import partial
OUT=pathlib.Path(__file__).resolve().parent
INPUT=OUT/'migration-inputs-001'
MANIFEST=json.loads((INPUT/'manifest.json').read_text())
ASSIGNMENT=json.loads((OUT/'migration-assignment.json').read_text())
ASSIGNED=ASSIGNMENT['case_numbers']
S={'cases':MANIFEST['cases']}
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def checked(p,m):
 assert p.is_file() and p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],str(p)
 return p
native=checked(INPUT/'_bocpd.py',MANIFEST['native'])
sp=importlib.util.spec_from_file_location('native_bocpd',native);bm=importlib.util.module_from_spec(sp);sp.loader.exec_module(bm)
MultivariateT=bm.MultivariateT;online_changepoint_detection=bm.online_changepoint_detection;constant_hazard=bm.constant_hazard
for pkg in ['numpy','pandas','scipy']:assert globals()[{'numpy':'np','pandas':'pd','scipy':'scipy'}[pkg]].__version__==MANIFEST['environment'][pkg],pkg
def item_for(oid):return next(x for x in MANIFEST['cases'] if x['opaque_id']==oid)
def compact(oid):
 item=item_for(oid);return np.load(checked(INPUT/item['file'],item),allow_pickle=False)
def input_arrays(oid):
 item=item_for(oid);z=compact(oid);return item['source_native']['relative'],{k:z[k] for k in ['X','times','columns','m','CP_flags']}
def raw_selected(oid):
 z=compact(oid);return z['causal_raw'],z['causal_columns'].tolist()
def write(name,value):
 q=OUT/name;assert not q.exists(),name;q.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\\n')
def emit(x):print(json.dumps(x,ensure_ascii=False,allow_nan=False),flush=True)
'''
q=p/'worker-migrated-v1.py';assert not q.exists();q.write_text(header+body)
print({'file':q.name,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'wrapped_worker_sha256':hashlib.sha256((p/'worker-v3.py').read_bytes()).hexdigest(),'changed_regions':['read paths/imports/package checks','compact exact inputs','explicit assignment selection and completion counts'],'unchanged':['causal()','run_engine()','branch definitions','sham exact m/CP gates','results schema']})
