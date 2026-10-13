"""Read-only EC2 pilot/rest verification. Timer is charged by transport controller."""
import pathlib,json,hashlib,subprocess,sys
import numpy as np
RUN_NAME = None
H=pathlib.Path('/home/ubuntu/rca/T-033');run=H/'runs'/RUN_NAME;control=H/'runs'/(RUN_NAME+'--control')
def read(p):return json.loads(p.read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def manifest(d):
 for n,m in read(d/'manifest.json').items():assert sha(d/n)==m['sha256'] and (d/n).stat().st_size==m['bytes']
config=read(H/'runs'/(RUN_NAME+'.config.json'));cp=control/'status.json';stat=read(cp) if cp.exists() else {'status':'NOT_YET_CREATED'}
result={'run':RUN_NAME,'config':config,'control':stat,'processing_timer':None,'validation':{'status':'PENDING'}}
tp=H/'runs'/(RUN_NAME+'.processing-timer.json')
if tp.exists():result['processing_timer']=read(tp)
if result['processing_timer'] and stat['status']=='PASS':
 assert result['processing_timer']['exit_code']==0
 manifest(control);manifest(run);S=read(H/'inputs/source.json');source={x['opaque_id']:x for x in S['cases']};kind=config['kind'];checks=[]
 assert read(control/'fixtures.json')['status']=='PASS'
 assert read(control/'guard-valid-accounting.json')['both_guards_accept_valid_ledger']
 if kind in ('nsigma','bocpd'):
  rows=read(run/'delay.json')['rows'];assert len(rows)==len(config['cases'])*(2 if kind=='nsigma' else 1)
  for row in rows:
   oid=row['opaque_id'];det=row['detector'];item=source[oid]
   if kind=='bocpd' and row['native_status']!='OK':
    assert row['status']=='NATIVE_NON_OK' and row['pre_proxy'] is None and row['no_post_alarm_to_end'] is None
    checks.append({'opaque_id':oid,'detector':det,'native_non_ok_preserved':True});continue
   npz=row['source_npz'] if kind=='nsigma' else row['source']['npz'];expected_sha=row['source_sha256'] if kind=='nsigma' else row['source']['sha256'];assert sha(H/npz)==expected_sha
   with np.load(H/npz,allow_pickle=False) as z:
    times=z['times'];flags=z['Z'].any(axis=1) if kind=='nsigma' else z['CP_flags'];ev=z['evaluated'] if kind=='nsigma' else np.arange(len(times))>=1
    assert len(times)==1441 and np.all(np.diff(times)==1) and times[720]==item['proxy']
    pre=[i for i in range(len(times)) if times[i]<item['proxy'] and ev[i]];post=[i for i in range(len(times)) if times[i]>=item['proxy'] and ev[i] and flags[i]]
    pp=row['pre_proxy'];assert pp['native_evaluated_points']==len(pre)
    assert pp['flag_points' if kind=='nsigma' else 'CP_points']==sum(bool(flags[i]) for i in pre)
    assert row['first_post_proxy_index']==(post[0] if post else None)
    assert row['signed_seconds_from_proxy']==(int(times[post[0]]-item['proxy']) if post else None)
    assert times[flags].astype(int).tolist()==item['expected'][det]['alarms']
    ends=[int(times[i]) for i in np.flatnonzero(flags)];first=ends[0] if ends else None;assert row['first_alarm_time']==first
    for seg in row['consecutive_true_segments']:
     lo,hi=seg['start_index'],seg['end_index'];assert flags[lo:hi+1].all() and np.all(np.diff(times[lo:hi+1])==1)
     assert lo==0 or not flags[lo-1] or times[lo]-times[lo-1]!=1
     assert hi==len(flags)-1 or not flags[hi+1] or times[hi+1]-times[hi]!=1
    checks.append({'opaque_id':oid,'detector':det,'independent_time_flags_first_density_segments':True})
 else:
  idx=read(run/'context-index.json');assert set(idx['records'])==set(config['cases'])
  for oid,m in idx['records'].items():
   row=read(run/m['record']);assert row['status']=='PASS' and all(row['checks'].values());summary=row['summary'];assert summary['trace']['status']=='OBSERVED_ARTIFACT' and isinstance(summary['trace']['status_code'],dict)
   assert (summary['log']['status']=='N/A_MISSING_CHANNEL')==('logs.parquet' not in source[oid]['files'])
   assert sha(run/row['output_npz'])==row['sha256']
   with np.load(run/row['output_npz'],allow_pickle=False) as z:
    assert set(z.files)==set(row['arrays']);times=z['times'];assert len(times)==1441 and np.all(np.diff(times)==1)
    for n,m in row['arrays'].items():assert list(z[n].shape)==m['shape'] and str(z[n].dtype)==m['dtype']
    assert int(z['trace_grid_span_count'].sum())==summary['trace']['alignment']['on_metric_grid_rows']
    if 'logs.parquet' in source[oid]['files']:assert int(z['log_grid_row_count'].sum())==summary['log']['alignment']['on_metric_grid_rows']
   checks.append({'opaque_id':oid,'schema_status_code_missing_log_npz_counts':True})
 result['validation']={'status':'PASS','checks':checks,'source_time_flags_CP_schema_verified':True,'fixture_and_valid_accounting_guard':True}
 result['run_status']=read(run/'status.json')
elif stat['status']=='STOPPED':
 result['validation']={'status':'STOPPED'}
 result['stderr']=(H/'runs'/(RUN_NAME+'.err')).read_text()[-5000:]
 result['child_stderr']=(control/'stderr.txt').read_text()[-5000:] if (control/'stderr.txt').exists() else None
 result['run_status']=read(run/'status.json') if (run/'status.json').exists() else None
print(json.dumps(result,indent=2))
