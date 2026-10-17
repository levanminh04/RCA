"""Explicit-pin orchestration and independent accounting; no raw data/labels."""
from pathlib import Path
from collections import Counter
import json,hashlib,gzip,copy,importlib.util,sys,ctypes,time
from pin_loader import api,package
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  assert load(p)==v,'never overwrite an unequal retained artifact: '+str(p)
  return
 with p.open('x',encoding='utf-8') as f:f.write(canon(v)+'\n')
def compressed(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(gzip.compress(canon(v).encode(),compresslevel=6,mtime=0))
def read_result(p):return json.loads(gzip.decompress(p.read_bytes())) if p.suffix=='.gz' else load(p)
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def peak():
 class C(ctypes.Structure):
  _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
 # Actual Windows structure contains QuotaPeakNonPagedPoolUsage before QuotaNonPagedPoolUsage.
 class PMC(ctypes.Structure):
  _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
 m=PMC();m.cb=ctypes.sizeof(m);ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
 ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
 assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(m),m.cb)
 return m.PeakWorkingSetSize
def semantic(v):
 d=copy.deepcopy(v)
 for view in d['views'].values():
  for side,groups in view['members'].items():
   for g in groups:
    for m in g['members']:m.pop('index',None)
    g['members'].sort(key=canon)
   groups.sort(key=canon)
  for side,rows in view['exclusions'].items():
   for r in rows:r.pop('index',None)
   rows.sort(key=canon)
 # Node positions are deterministic sorted IDs in the API; graph interval/context unchanged.
 return canon(d)
def independent(result,static,trace,mapping):
 mi={(m['level'],m['original']):m for m in mapping};own=dict(trace.get('belongs_to',[]));so=dict(static.get('belongs_to',[]))
 def resolve(x):
  lev='operation' if x in own else 'entity';m=mi.get((lev,x))
  if not m or not m['verified'] or len(set(m['candidates']))!=1:return None
  target=m['candidates'][0]
  if lev=='operation' and so[target]!=resolve(own[x]):return None
  return target
 for name,v in result['views'].items():
  sets={}
  for side,g in [('static',static),('trace',trace)]:
   keys=set()
   for e in g['edges']:
    if g['level']=='entity' and (e['source']==e['target'] or e['type']=='span-parent'):continue
    if e['type']=='thông-điệp':
     assert side=='static' and e['messaging']['broker_scope'] is None
     continue
    s,t=e['source'],e['target']
    if side=='trace':s,t=resolve(s),resolve(t)
    if s is None or t is None or (g['level']=='entity' and s==t):continue
    if name=='typed' and e['type']=='gọi-chưa-phân-kiểu':continue
    keys.add(canon([s,t,e['type'] if name=='typed' else None,['smtp',None] if e.get('channel')=='smtp' else None]))
   sets[side]=keys
   members=[m for group in v['members'][side] for m in group['members']];excluded=v['exclusions'][side]
   indices=[x['index'] for x in members+excluded]
   assert sorted(indices)==list(range(len(g['edges'])))
   assert all(x['original']==g['edges'][x['index']] for x in members+excluded)
  s,t=sets['static'],sets['trace']
  for k,w in [('S',s),('T',t),('intersection',s&t),('static_only',s-t),('trace_only',t-s)]:assert {canon(x) for x in v[k]}==w,(name,k)
  assert [v[k] for k in ['numerator','static_denominator','trace_denominator']]==[len(s&t),len(s),len(t)]
  assert v['static_fraction']==(len(s&t)/len(s) if s else None)
  assert v['trace_fraction']==(len(s&t)/len(t) if t else None)
 assert result['interval_ns']==trace['interval_ns'] and result['conditional_reference']
def permute(g):
 g=copy.deepcopy(g)
 for k in ['nodes','edges','belongs_to','component_context']:
  if k in g:g[k].reverse()
 return g
