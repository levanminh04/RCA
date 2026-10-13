"""Dependency feasibility/computational probe, no root labels or accuracy claim."""
import collections,hashlib,importlib.util,json,pathlib,sys,time
import numpy as np,pandas as pd
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
def rewire(edges,seed=20261012):
 # Directed double-edge swaps preserve per-node in/out degree exactly.
 rg=np.random.default_rng(seed);ee=set(edges);arr=list(sorted(ee));success=0
 for _ in range(max(100,len(arr)*20)):
  if len(arr)<2:break
  i,j=rg.choice(len(arr),2,replace=False);a,b=arr[i];c,d=arr[j];p,q=(a,d),(c,b)
  if a==d or c==b or p in ee or q in ee or p==q:continue
  ee.remove(arr[i]);ee.remove(arr[j]);ee.add(p);ee.add(q);arr[i]=p;arr[j]=q;success+=1
 assert collections.Counter(a for a,b in edges)==collections.Counter(a for a,b in ee)
 assert collections.Counter(b for a,b in edges)==collections.Counter(b for a,b in ee)
 return sorted(ee),success
def scores(X,nodes,edges):
 out=np.abs(X).copy();defined=[]
 for j,n in enumerate(nodes):
  children=sorted({nodes.index(b) for a,b in edges if a==n and b in nodes and b!=a})
  if children:out[:,j]=np.abs(X[:,j]-X[:,children].mean(1));defined.append(j)
 return out,defined
def run():
 rows=[]
 for ci,item in enumerate(w.S['cases']):
  oid=item['opaque_id'];dest=w.OUT/(oid+'--graph-probe.json')
  if dest.exists():continue
  t=time.perf_counter();metric=pd.read_parquet(w.raw_path(item,'metrics.parquet'));times=metric['time'].to_numpy()
  trace=pd.read_parquet(w.raw_path(item,'traces.parquet'),columns=['traceID','spanID','parentSpanID','serviceName','startTime','statusCode'])
  keys=pd.MultiIndex.from_frame(trace[['traceID','spanID']]);duplicate=keys.duplicated(keep=False);identity=trace['traceID'].notna()&trace['spanID'].notna()&trace['serviceName'].notna();valid=~duplicate&identity.to_numpy();parent_keys=pd.MultiIndex.from_arrays([trace['traceID'],trace['parentSpanID']]);idx=keys[valid].get_indexer(parent_keys);parent_service=np.full(len(trace),None,object);valid_positions=np.flatnonzero(valid);has=idx>=0;parent_service[has]=trace['serviceName'].to_numpy()[valid_positions[idx[has]]]
  secs=(trace['startTime']//1_000_000).to_numpy();baseline=(secs>=times[0])&(secs<times[100]);child=trace['serviceName'].to_numpy();edges=sorted(set((a,b) for a,b,keep in zip(parent_service,child,has&baseline) if keep and a is not None and b is not None and a!=b))
  nodes=sorted(trace['serviceName'].dropna().unique().tolist());mapped={n:[c for c in metric if c.startswith(n+'_') and ('latency-50' in c or '_error' in c)] for n in nodes};nodes=[n for n in nodes if mapped[n]]
  X=np.zeros((len(times),len(nodes)))
  for j,n in enumerate(nodes):
   raw=metric[mapped[n]].replace([np.inf,-np.inf],np.nan).ffill().fillna(0).to_numpy();mean=raw[:100].mean(0);std=raw[:100].std(0,ddof=1);z=(raw-mean)/np.where(std>0,std,1.)
   which=np.abs(z).argmax(1);X[:,j]=z[np.arange(len(z)),which]
  usable=[e for e in edges if e[0] in nodes and e[1] in nodes];random,swaps=rewire(usable);real,defined=scores(X,nodes,usable);null=np.abs(X);rand,rdefined=scores(X,nodes,random)
  effects=[]
  for j,n in enumerate(nodes):
   effects.append({'entity':n,'metric_columns':mapped[n],'out_neighbors':[b for a,b in usable if a==n],'has_graph_context':j in defined,'real_vs_noedge_changed_points':int(np.count_nonzero(real[:,j]!=null[:,j])),'real_vs_rewired_changed_points':int(np.count_nonzero(real[:,j]!=rand[:,j])),'mean_absolute_real_minus_noedge':float(np.abs(real[:,j]-null[:,j]).mean()),'mean_absolute_real_minus_rewired':float(np.abs(real[:,j]-rand[:,j]).mean())})
  value={'status':'PASS','opaque_id':oid,'edges_baseline100':edges,'usable_edges':usable,'rewired_edges':random,'rewire_swaps':swaps,'rewire_degree_preserved':True,'feature_node_count':len(nodes),'trace_service_count':int(trace['serviceName'].nunique()),'ambiguous_duplicate_span_rows':int(duplicate.sum()),'resolved_parent_rows':int(has.sum()),'trace_rows':len(trace),'status_present_rows':int(trace['statusCode'].notna().sum()),'effects':effects,'formula':'node signed feature=maxabs z metric (mean/std first100); g_v=abs(s_v - mean(s_outneighbors)); comparator noedges=abs(s_v); graph rewired directed degree-preserving swaps','basis':'Computational dependency/information feasibility only; arbitrary untuned diagnostic, no root/onset labels supplied; baseline100 not certified clean; schema supplied at start conditional; no benefit/cause/newP6method claim','edge_semantics':'Observed cross-service parent-span nesting in same trace; client/server/sync/wait semantics absent; exclude ambiguous parent identities and self loops','body_wall_s':time.perf_counter()-t}
  w.write(dest.name,value);w.emit({'graph_case':ci+1,'usable_edges':len(usable),'swaps':swaps,'wall_s':value['body_wall_s']})
 w.emit({'graph_probe':'COMPLETE'})
if __name__=='__main__':run()
