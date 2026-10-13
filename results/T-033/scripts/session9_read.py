"""Read/display saved artifacts only. No scientific calculation."""
import sys,pathlib,json,gzip
p=pathlib.Path(sys.argv[1]);b=p.read_bytes()
if p.suffix=='.gz':b=gzip.decompress(b)
x=json.loads(b.decode('utf-8-sig'))
if len(sys.argv)>2:
 for k in sys.argv[2].strip('/').split('/'):
  if k:x=x[int(k)] if isinstance(x,list) else x[k]
if len(sys.argv)>3 and sys.argv[3]=='keys':
 print(json.dumps({k:type(v).__name__ for k,v in x.items()},ensure_ascii=False))
elif len(sys.argv)>3 and sys.argv[3]=='chain':
 for u in x['units'][int(sys.argv[4]):int(sys.argv[5])]:
  print(json.dumps({k:u.get(k) for k in ['opaque_id','detector','branch','native_status']},ensure_ascii=False))
  for v in u['points']:
   keys=['index','roles','flag','trigger_count','fixed_status','CP_flag','m','previous_m','absolute_m_change','MAP_posterior','runner_up','runner_posterior','normalizer','MAP_parent_predictive_density','MAP_parent_prior_posterior','previous_MAP_continuation_posterior','theta_available']
   row={k:v[k] for k in keys if k in v}
   if 'columns' in v:row['columns']=v['columns'][:2]
   print(json.dumps(row,ensure_ascii=False))
elif len(sys.argv)>3 and sys.argv[3]=='fields':
 fields=sys.argv[4].split(',')
 for r in x:print(json.dumps({k:r[k] for k in fields if k in r},ensure_ascii=False))
elif len(sys.argv)>3 and sys.argv[3]=='brief':
 for u in x['units'][int(sys.argv[4]):int(sys.argv[5])]:
  print('UNIT',u['unit_index'],u['opaque_id'],u['detector'],u['branch'],u['status'],u['first_group'])
  for p in u['points']:
   fields=['index','CP_flag','m','previous_m','MAP_posterior','previous_MAP_continuation_posterior','theta_available'] if 'm' in p else ['index','flag','trigger_count']
   print(json.dumps([p[k] for k in fields],separators=(',',':')))
  for pair in u['first_two_alarm_columns']:
   for v in pair[:1]:
    fields=['raw_values','x','count','mean','std','threshold','margin','flags']
    print(v['column'],json.dumps([[v[s][k] for k in fields] if v[s] else None for s in ['alarm','control']],separators=(',',':')))
  if u['same_column_control_status']:print(json.dumps(u['same_column_control_status']))
else:print(json.dumps(x,ensure_ascii=False,indent=2))
