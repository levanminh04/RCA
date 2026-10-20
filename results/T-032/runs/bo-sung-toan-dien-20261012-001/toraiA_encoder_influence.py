"""Fixed-column count diagnostic, not an RCA rerun or source-A replacement."""
import pathlib,json,hashlib
import numpy as np
import pandas as pd
P=pathlib.Path(__file__).parent;enc=json.loads((P/'toraiA-encoder-006-full/summary.json').read_text(encoding='utf-8'));old=json.loads((P/'toraiA/attempt004-allcolumns/summary.json').read_text(encoding='utf-8'));out=[]
for r,c in zip(enc['rows'],old['cases']):
 assert r['opaque_id']==c['opaque_id'];oid=r['opaque_id'];src=[s for s in enc['source_hashes'] if s.endswith('/tracets_lat.csv') and oid==next(x['opaque_id'] for x in old['cases'] if x['root']==c['root'] and x['opaque_id']==oid)]
 # Resolve solely from pinned raw path corresponding to this allowlisted oid.
 from src.p3 import selector
 meta=selector.nap_allowlist(pathlib.Path.cwd()/'results/T-022/allowlist-dev.json')[oid]['files']['traces.parquet'];name=pathlib.Path(meta['path']).parent.name.removeprefix('re2tt_');sf,rep=name.rsplit('_',1);csv=pathlib.Path('D:/RCA-ext/work/T-016/data/torai-TT')/sf/rep/'tracets_lat.csv';assert hashlib.sha256(csv.read_bytes()).hexdigest()==enc['source_hashes'][str(csv)]
 f=pd.read_csv(csv).ffill().fillna(0);t=c['raw_start_bin_A_us'][0]//1000000;n=f[f.time<t].tail(20);a=f[f.time>=t].head(20);v=pd.concat([n,a]);cols={z['column']:z for s in c['all_services'].values() for z in s['operation_columns']}
 def shares(frame):
  raw={}
  for col in cols:
   x=frame[col].to_numpy(float)[:20];y=frame[col].to_numpy(float)[20:];sd=x.std();raw[col]=float(np.max(np.abs((y-x.mean())/(sd if sd else 1.))))
  total=sum(raw.values());return {col:(score/total if total else 0.) for col,score in raw.items()}
 native=shares(v);assert max(abs(native[k]-cols[k]['share']) for k in cols)<1e-12
 branch=[]
 for rr in r['recipes']:
  vv=v.copy()
  for m in rr['mismatches']:
   ii=vv.index[vv.time==m['time']];assert len(ii)==1;vv.loc[ii,m['col']]=m['candidate_count']
  ss=shares(vv);sv={s:sum(ss[z['column']] for z in dat['operation_columns']) for s,dat in c['all_services'].items()};pairs=[]
  for pair in c['above_root_pairs']:
   tm=sv.get(pair['above_root_service'],0)-sv.get(c['root'],0);sm=pair['severity_margin']+(tm-pair['trace_margin'])/4
   pairs.append({'service':pair['above_root_service'],'source_trace_margin':pair['trace_margin'],'candidate_trace_margin':tm,'trace_sign_changed':bool(np.sign(tm)!=np.sign(pair['trace_margin'])),'source_severity_margin':pair['severity_margin'],'candidate_severity_margin':sm,'severity_sign_changed':bool(np.sign(sm)!=np.sign(pair['severity_margin']))})
  branch.append({'scope':rr['scope'],'pairs':pairs})
 out.append({'opaque_id':oid,'branches':branch})
summary={'status':'PASS_ROOT_FIXED_COLUMN_DIAGNOSTIC','cases':30,'scope':'Same native retained column support; swap reconstructed count cells only; no drop-constant re-selection, GMM/RCD or RCA ranking rerun. Mean+3sd recipe is unverified author lineage; no recipe selected. Other modality contributions held fixed.','branches':{scope:{'pairs':sum(len(b['pairs']) for r in out for b in r['branches'] if b['scope']==scope),'trace_margin_sign_changed':sum(p['trace_sign_changed'] for r in out for b in r['branches'] if b['scope']==scope for p in b['pairs']),'severity_margin_sign_changed':sum(p['severity_sign_changed'] for r in out for b in r['branches'] if b['scope']==scope for p in b['pairs'])} for scope in ['raw_full','source_csv_extent']},'rows':out}
(P/'toraiA-encoder-influence-001.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False))
