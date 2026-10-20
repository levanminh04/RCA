"""Source-A count reconstruction and conditional threshold identifiability, all dev."""
import pathlib,json,hashlib,time,collections,math
import pandas as pd
import numpy as np
from src.p3 import selector
from src.p3.torai_b import ten_cot
ROOT=pathlib.Path.cwd();P=pathlib.Path(__file__).parent;O=P/'toraiA-encoder-002';O.mkdir(exist_ok=False)
allow=selector.nap_allowlist(ROOT/'results/T-022/allowlist-dev.json');old=json.loads((P/'toraiA/attempt004-allcolumns/summary.json').read_text(encoding='utf-8'))
start=time.time();rows=[];sources={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for case in old['cases']:
 oid=case['opaque_id'];meta=allow[oid]['files']['traces.parquet'];rawpath=ROOT/meta['path'];assert rawpath.stat().st_size==meta['bytes'] and sha(rawpath)==meta['sha256'];sources[str(rawpath)]=meta['sha256']
 name=rawpath.parent.name.removeprefix('re2tt_');svc_fault,rep=name.rsplit('_',1);csv=pathlib.Path('D:/RCA-ext/work/T-016/data/torai-TT')/svc_fault/rep/'tracets_lat.csv';sources[str(csv)]=sha(csv)
 f=pd.read_csv(csv).ffill().fillna(0);lo,hi=case['raw_start_bin_A_us'];t=lo//1000000
 # Native cut takes last20 N/first20 A; source A grid lo was proved contiguous.
 a=f[f.time>=t].head(20);n=f[f.time<t].tail(20);native=pd.concat([n,a]);assert a.time.astype(int).tolist()==list(range(lo//1000000,hi//1000000,15))
 columns={c['column']:c for s in case['all_services'].values() for c in s['operation_columns']}
 for c,cc in columns.items():
  x=n[c].to_numpy(float);y=a[c].to_numpy(float)
  assert x.mean()==cc['mean_N'] and x.std()==cc['std_N'] and y.max()==cc['max_A'] and y.mean()==cc['mean_A'],(oid,c,'local A mismatch')
 sp=pd.read_parquet(rawpath);names,_=ten_cot(sp);st=sp.startTime.to_numpy(np.int64);dur=sp.duration.to_numpy(float);anchor=int(f.time.min())*1000000;bins=anchor+np.floor_divide(st-anchor,15000000)*15000000
 keys=sp.traceID.astype(str)+'|'+sp.spanID.astype(str);dup=keys.duplicated(False);lookup={k:i for i,k in enumerate(keys) if not dup.iloc[i]};parents=sp.traceID.astype(str)+'|'+sp.parentSpanID.astype(str);children=collections.defaultdict(list)
 for i,k in enumerate(parents):
  j=lookup.get(k,-1)
  if j>=0:children[j].append(i)
 sv=sp.serviceName.astype(str).to_numpy();root=case['root'];hasroot=np.zeros(len(sp),bool)
 # A diagnostic label joins only for attribution, never threshold/count selection.
 for i in np.flatnonzero(np.isin(names.to_numpy(),list(columns))):
  seen=set();stack=list(children.get(int(i),[]))
  while stack:
   j=stack.pop()
   if j in seen:continue
   seen.add(j)
   if sv[j]==root:hasroot[i]=True;break
   stack.extend(children.get(j,[]))
 table=pd.DataFrame({'col':names.to_numpy(),'duration':dur,'bin':bins,'row':np.arange(len(sp))});native_us=native.time.to_numpy(np.int64)*1000000;inwindow=np.isin(bins,native_us)
 scopes={'raw_full':np.ones(len(sp),bool),'source_csv_extent':(st>=anchor)&(st<(int(f.time.max())+15)*1000000)};recipes=[]
 for scope,mask in scopes.items():
  stats=table.loc[mask].groupby('col').duration.agg(['mean','std']);thresholds=names.map(stats['mean']+3*stats['std']).to_numpy(float);flag=dur>thresholds
  counts=table.loc[flag&inwindow].groupby(['bin','col']).size();bad=[];total=0;equal=0;bycol=[]
  for c in columns:
   observed=native[c].to_numpy(float);pred=np.array([counts.get((int(bt),c),0) for bt in native_us]);same=observed==pred;total+=len(same);equal+=int(same.sum())
   for bt,x,y in zip(native_us[~same],observed[~same],pred[~same]):bad.append({'col':c,'time':int(bt//1000000),'source_count':float(x),'candidate_count':int(y)})
   ids=np.flatnonzero((names.to_numpy()==c)&flag&np.isin(bins,a.time.to_numpy(np.int64)*1000000));thr=stats.loc[c] if c in stats.index else None
   bycol.append({'column':c,'threshold':float(thr['mean']+3*thr['std']) if thr is not None and np.isfinite(thr['std']) else None,'A_flagged_count':len(ids),'A_flagged_with_root_descendant':int(hasroot[ids].sum()),'exact_bins':int(same.sum()),'bins':len(same)})
  recipes.append({'scope':scope,'cells':total,'equal_cells':equal,'all_cells_exact':equal==total,'mismatches':bad,'columns':bycol})
 # Global threshold feasibility from exact native bin counts, under explicit contract.
 constraints=[]
 for c in columns:
  lower=-math.inf;upper=math.inf;issues=[];ids=table.index[table.col==c].to_numpy();candidate_ids=[]
  for bt,expected in zip(native_us,native[c].to_numpy(float)):
   ii=ids[bins[ids]==bt];d=np.sort(dur[ii])[::-1];k=int(expected)
   if expected!=k or k<0 or k>len(d):issues.append({'time':int(bt//1000000),'count':float(expected),'raw_support':len(d),'reason':'count_not_feasible'});continue
   low=float(d[k]) if k<len(d) else -math.inf;up=float(d[k-1]) if k>0 else math.inf;lower=max(lower,low);upper=min(upper,up)
   if k>0 and k<len(d) and d[k-1]==d[k]:issues.append({'time':int(bt//1000000),'reason':'count_cuts_duration_tie'})
   candidate_ids.extend(ii[np.argsort(-dur[ii],kind='stable')[:k]].tolist())
  feasible=not issues and lower<upper
  constraints.append({'column':c,'feasible_constant_strict_threshold':feasible,'lower_inclusive':lower if math.isfinite(lower) else None,'upper_exclusive':upper if math.isfinite(upper) else None,'issues':issues,'n_conditional_flagged_native_window':len(candidate_ids) if feasible else None,'n_conditional_flagged_with_root_descendant':int(hasroot[candidate_ids].sum()) if feasible else None,'empty_global_intersection':lower>=upper})
 out={'opaque_id':oid,'root':root,'local_sourceA_moments_match_captured':True,'recipes':recipes,'threshold_constraints':constraints,'limitations':'Reconstruction candidates, not verified author lineage. Filled native CSV counts, no event completeness; feasible threshold identifies top-k only conditional on column/bin/strict threshold contract.'}
 (O/(oid+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=1,allow_nan=False),encoding='utf-8');rows.append(out)
 print(json.dumps({'case':oid,'done':len(rows),'elapsed_s':round(time.time()-start,2),'recipe_equal':[(r['scope'],r['equal_cells'],r['cells']) for r in recipes],'feasible_columns':sum(c['feasible_constant_strict_threshold'] for c in constraints)},ensure_ascii=False),flush=True)
summary={'status':'COMPLETE','cases':len(rows),'elapsed_s':time.time()-start,'source_hashes':sources,'rows':rows,'recipe_summary':{s:{'cells':sum(r['cells'] for row in rows for r in row['recipes'] if r['scope']==s),'equal_cells':sum(r['equal_cells'] for row in rows for r in row['recipes'] if r['scope']==s),'fully_exact_cases':sum(next(r for r in row['recipes'] if r['scope']==s)['all_cells_exact'] for row in rows)} for s in scopes},'constraints_summary':{'columns':sum(len(r['threshold_constraints']) for r in rows),'feasible_columns':sum(c['feasible_constant_strict_threshold'] for r in rows for c in r['threshold_constraints'])}}
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=1,allow_nan=False),encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k not in ['rows','source_hashes']},ensure_ascii=False),flush=True)
