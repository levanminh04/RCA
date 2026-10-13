"""N-Sigma descriptions from exact verified stored intermediates; EC2 only."""
import argparse,pathlib,os,time,sys,traceback,datetime
import numpy as np
from common import H,read,write,check,sha,load_pins,guard
from bocpd_delay import segments

def describe(item,det,pins):
 oid=item['opaque_id']; rels=[r for r in pins['files'] if r.endswith('/'+oid+'--'+det+'.json')]
 assert len(rels)==1
 rel=rels[0];record=read(check(H/rel,pins['files'][rel]));assert record['status']=='PASS' and all(record['checks'].values())
 nr=(pathlib.Path(rel).parent/record['output_npz']).as_posix(); meta=pins['files'][nr]
 assert meta['sha256']==record['sha256'] and meta['bytes']==record['bytes']
 with np.load(check(H/nr,meta),allow_pickle=False) as z:a={k:z[k].copy() for k in z.files}
 times,flags,ev=a['times'],a['Z'],a['evaluated'];x,mu,sd=a['x'],a['mean'],a['std']
 assert len(times)==1441 and np.all(np.diff(times)==1) and times[720]==item['proxy']
 assert np.array_equal(ev,np.arange(len(times))>=100)
 assert x.shape==mu.shape==sd.shape==flags.shape==a['count'].shape
 assert np.array_equal(a['threshold'],3*sd,equal_nan=True)
 assert np.array_equal(a['margin'],np.abs(x-mu)-3*sd,equal_nan=True)
 assert np.array_equal(flags,(np.abs(x-mu)>3*sd)&ev[:,None])
 anyflag=flags.any(axis=1);assert times[anyflag].astype(int).tolist()==item['expected'][det]['alarms']
 assert a['columns'].tolist()==item['expected'][det]['detector_columns']
 pre=(times<item['proxy'])&ev;post=(times>=item['proxy'])&ev
 finite=np.isfinite(mu)&np.isfinite(sd)
 pi=np.flatnonzero(anyflag&post);first=int(pi[0]) if len(pi) else None
 ni=np.flatnonzero(anyflag);f0=int(ni[0]) if len(ni) else None
 segs=segments(anyflag,times,720);end=first if first is not None else len(times)-1
 evidence=[]
 for i in range(720,end+1):
  evidence.append({'index':i,'time':int(times[i]),'flag':bool(anyflag[i]),'trigger_columns':a['columns'][flags[i]].tolist(),'source_npz':nr,'array_row':i,'arrays':['x','count','mean','std','threshold','margin','Z'],'nonfinite_statistics_columns':a['columns'][~finite[i]].tolist()})
 row={'opaque_id':oid,'detector':det,'status':'VALID_NATIVE','source_record':rel,'source_record_sha256':pins['files'][rel]['sha256'],'source_npz':nr,'source_sha256':meta['sha256'],
 'index_map':{'i_proxy':720,'t_proxy':int(times[720]),'time_start':int(times[0]),'time_end':int(times[-1])},
 'first_alarm_index':f0,'first_alarm_time':int(times[f0]) if f0 is not None else None,'first_alarm_signed_seconds_from_proxy':int(times[f0]-item['proxy']) if f0 is not None else None,
 'first_post_proxy_index':first,'t_hat_plus':int(times[first]) if first is not None else None,'signed_seconds_from_proxy':int(times[first]-item['proxy']) if first is not None else None,
 'no_post_alarm_to_end':first is None,'followup_end_time':int(times[-1]),'post_proxy_followup_elapsed_seconds':int(times[-1]-item['proxy']),'post_proxy_native_evaluated_points':int(post.sum()),
 'pre_proxy':{'flag_points':int((anyflag&pre).sum()),'native_evaluated_points':int(pre.sum()),'fraction_flag_points':float((anyflag&pre).sum()/pre.sum()),'time_first_evaluated':int(times[np.flatnonzero(pre)[0]]),'time_last_evaluated':int(times[np.flatnonzero(pre)[-1]]),'seconds_grid_coverage':int(pre.sum()),'finite_statistics_cells':int(finite[pre].sum()),'all_evaluated_cells':int(pre.sum()*flags.shape[1]),'points_with_any_finite_statistics':int(finite[pre].any(axis=1).sum()),'points_with_all_finite_statistics':int(finite[pre].all(axis=1).sum()),'flags_with_nonfinite_statistics':int((flags[pre]&~finite[pre]).sum())},
 'consecutive_true_segments':segs,'first_post_alarm_in_preexisting_segment':any(s['starts_before_and_reaches_proxy'] and s['start_index']<=first<=s['end_index'] for s in segs) if first is not None else None,
 'proxy_to_first_post_or_end':{'start_index':720,'end_index':end,'points':evidence},
 'checks':{'source_record_npz_pinned':True,'flags_time_columns_source_exact':True,'strict_gt_and_evaluation_start_exact':True,'threshold_margin_exact':True},
 'interpretation':'Time to native strict threshold crossing relative to proxy; not true onset or operational false alarm. NaN comparisons keep native False.'}
 idx={'opaque_id':oid,'detector':det,'npz':nr,'sha256':meta['sha256'],'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in a.items()},'not_evaluated_before':100,'nan_semantics':'False native comparison; count after fill is not independent raw-observation count.'}
 return row,idx

def main():
 p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--cases',required=True);args=p.parse_args()
 run=H/'runs'/args.run;run.mkdir(exist_ok=False);begin=time.perf_counter()
 status={'status':'RUNNING','pid':os.getpid(),'script_sha256':sha(__file__),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':sys.argv,'completed_units':[]}
 rows=[];indexes=[];write(run/'status.json',status)
 try:
  pins=load_pins();source=read(H/'inputs/source.json');status['source_sha256']=pins['source_sha256'];wanted=args.cases.split(',');assert len(wanted)==len(set(wanted)) and set(wanted)<={c['opaque_id'] for c in source['cases']}
  for item in source['cases']:
   if item['opaque_id'] not in wanted:continue
   for det in ('nsigma','nsigma_doi_chung'):
    guard(16*2**20);row,idx=describe(item,det,pins);key=item['opaque_id']+'--'+det
    write(run/(key+'--delay.json'),row);rows.append(row);indexes.append(idx);status['completed_units'].append(key);status['resources']=guard();write(run/'status.json',status)
    print('NSIGMA DELAY PASS',key,flush=True)
  assert len(rows)==2*len(wanted)
  write(run/'delay.json',{'status':'PASS','rows':rows,'units':len(rows)});write(run/'intermediate-index.json',{'status':'PASS','items':indexes});status['status']='PASS'
 except BaseException as e:
  status.update(status='STOPPED',error=type(e).__name__+': '+str(e));traceback.print_exc();raise
 finally:
  status.update(wall_s=time.perf_counter()-begin,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());write(run/'status.json',status)
  write(run/'manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in run.iterdir() if p.is_file() and p.name!='manifest.json'})
if __name__=='__main__':main()
