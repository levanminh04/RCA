"""Memory-bounded equivalent of author singleton-after-top-K/top1000 ranker.
Uses the identical ordered FP-growth generator, exact author arithmetic, stable caps.
Does not change source clone or installed library files.
"""
import heapq,math,time,json,sys,importlib
from functools import reduce
from collections import defaultdict
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpcommon
fg=importlib.import_module('mlxtend.frequent_patterns.fpgrowth')

def stream_rank(data,mining,support=.1,k=100,cap=1000):
 start=time.perf_counter();data=data.copy();data['predict']=data['predict'].astype(bool)
 tids,itemsets=mining.ItemsetHandler.gen_itemsets(data,forbidden_names=frozenset({'gateway'}))
 items=reduce(lambda a,b:a|b,(x[0] for x in itemsets))-frozenset({'gateway'});idx={t:i for i,t in enumerate(tids)}
 masks=defaultdict(int);bad=0;absets=[]
 for i,(ss,label) in enumerate(itemsets):
  for s in ss:masks[s]|=1<<i
  if label:bad|=1<<i;absets.append(ss)
 if not absets:return [],{}, {'patterns_seen':0,'status':'NO_EVIDENCE'}
 te=TransactionEncoder();a=te.fit_transform(absets);frame=pd.DataFrame(a,columns=te.columns_)
 tree,_=fpcommon.setup_fptree(frame,support);gene=fg.fpg_step(tree,math.ceil(support*len(frame)),dict(enumerate(frame.columns)),None,0)
 top=[];scores=[];score_set=set();n=0
 for support_count,isets in gene:
  pat=frozenset(frame.columns[i] for i in isets);mask=reduce(lambda a,b:a&b,(masks[s] for s in pat));ac=(mask&bad).bit_count();total=mask.bit_count();assert ac==support_count
  pa=np.float64(support_count/len(absets));pb=ac/total;score=1/(1/np.maximum(pa,1e-4)+1/np.maximum(pb,1e-4)-1)
  if score not in score_set:
   if len(scores)<k:heapq.heappush(scores,score);score_set.add(score)
   elif score>scores[0]:score_set.remove(heapq.heapreplace(scores,score));score_set.add(score)
  entry=(score,-n,pat)
  if len(top)<cap:heapq.heappush(top,entry)
  elif entry[:2]>top[0][:2]:heapq.heapreplace(top,entry)
  n+=1
  if n%1000000==0:print(json.dumps({'stream_patterns':n,'elapsed_s':time.perf_counter()-start,'stored_pattern_cap':len(top)}),flush=True)
 if not top:return [],{}, {'patterns_seen':n,'status':'NO_EVIDENCE'}
 cutoff=scores[0];selected=[e for e in sorted(top,key=lambda e:(-e[0],-e[1])) if e[0]>=cutoff]
 ins=defaultdict(int);outs=defaultdict(int)
 for row in data.loc[data.predict,['source','target','trace_id']].itertuples(index=False):
  bit=1<<idx[row.trace_id];outs[row.source]|=bit;ins[row.target]|=bit
 ret=defaultdict(lambda:{'score':-1,'pattern':frozenset(),'pattern_score':0,'in-pattern_score':0})
 for score,negindex,pat in selected:
  if len(pat)>1:continue
  s=next(iter(pat));mask=masks[s];ips=np.abs((ins[s]&mask).bit_count()-(outs[s]&mask).bit_count());v=ips*score
  if v>ret[s]['score']:ret[s]={'score':v,'pattern':pat,'pattern_score':score,'in-pattern_score':ips,'support_count_abnormal':int((mask&bad).bit_count()),'total_pattern_traces':int(mask.bit_count()),'total_abnormal_traces':len(absets),'support':float((mask&bad).bit_count()/len(absets)),'confidence':float((mask&bad).bit_count()/mask.bit_count()),'flagged_in_traces':int((ins[s]&mask).bit_count()),'flagged_out_traces':int((outs[s]&mask).bit_count())}
 ranking=sorted(items,key=lambda s:(ret[s]['score'],-len(ret[s]['pattern'])),reverse=True)
 return ranking,dict(ret),{'patterns_seen':n,'patterns_retained':len(selected),'unique_score_cutoff':float(cutoff),'unique_scores_retained':len(scores),'singleton_patterns_retained':sum(len(x[2])==1 for x in selected),'elapsed_s':time.perf_counter()-start,'memory_bound':'FP-tree+trace-bitsets+1000patterns+100unique-scores; time may remain exponential'}

def fixture(mining):
 rng=np.random.default_rng(20261012);checks=[]
 for case in range(30):
  rows=[]
  for tid in range(30):
   for _ in range(1+int(rng.integers(1,7))):
    s,t=rng.choice(list('ABCDEF'),2,replace=False);rows.append({'source':s,'target':t,'trace_id':str(tid),'predict':bool(rng.random()<.3)})
  df=pd.DataFrame(rows);capt={};code=mining.TraceRCA.__call__.__code__
  def prof(frame,event,arg):
   if event=='return' and frame.f_code is code:capt['ret']=frame.f_locals.get('item_ret',{})
  old=sys.getprofile();sys.setprofile(prof)
  try:native=mining.TraceRCA()(df.copy(),quiet=True,forbidden_names=frozenset({'gateway'}),min_support_rate=.1,k=100,enable_PRFL=False)
  finally:sys.setprofile(old)
  rank,ret,stat=stream_rank(df,mining);assert rank==native
  for s in native:
   for key in ['score','pattern_score','in-pattern_score']:assert float(ret[s][key]).hex()==float(capt['ret'][s][key]).hex(),(case,s,key)
   assert ret[s]['pattern']==capt['ret'][s]['pattern']
  checks.append({'case':case,'bitexact_rank_score_pattern':True,'patterns':stat['patterns_seen']})
 for nn in [12,14]:
  rows=[];letters=list('ABCDEFGHIJKLMN')[:nn]
  for tid in range(500):
   ss=set(letters[:6] if tid<250 else letters[:2])
   ss.update(x for x in letters[6 if tid<250 else 2:] if rng.random()<(0.91 if tid<250 else .73))
   ss=sorted(ss)
   for x,y in zip(ss,ss[1:]):rows.append({'source':x,'target':y,'trace_id':str(tid),'predict':tid<250})
  df=pd.DataFrame(rows);capt={};old=sys.getprofile();sys.setprofile(prof)
  try:native=mining.TraceRCA()(df.copy(),quiet=True,forbidden_names=frozenset({'gateway'}),min_support_rate=.1,k=100,enable_PRFL=False)
  finally:sys.setprofile(old)
  rank,ret,stat=stream_rank(df,mining);assert rank==native
  for x in native:
   for key in ['score','pattern_score','in-pattern_score']:assert float(ret[x][key]).hex()==float(capt['ret'][x][key]).hex()
   assert ret[x]['pattern']==capt['ret'][x]['pattern']
  assert stat['patterns_seen']>1000
  checks.append({'stress_items':nn,'bitexact_rank_score_pattern':True,**stat})
 rows=[{'source':x,'target':y,'trace_id':str(tid),'predict':True} for tid in range(100) for x,y in zip(list('ABCDEFGHIJKLMN'),list('BCDEFGHIJKLMN'))]
 df=pd.DataFrame(rows);capt={};old=sys.getprofile();sys.setprofile(prof)
 try:native=mining.TraceRCA()(df.copy(),quiet=True,forbidden_names=frozenset({'gateway'}),min_support_rate=.1,k=100,enable_PRFL=False)
 finally:sys.setprofile(old)
 rank,ret,stat=stream_rank(df,mining);assert rank==native and stat['patterns_retained']==1000 and stat['unique_scores_retained']==1
 for x in native:
  for key in ['score','pattern_score','in-pattern_score']:assert float(ret[x][key]).hex()==float(capt['ret'][x][key]).hex()
  assert ret[x]['pattern']==capt['ret'][x]['pattern']
 checks.append({'stress':'stable_cap1000_all_equal_scores','bitexact_rank_score_pattern':True,**stat})
 return checks
