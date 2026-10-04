import argparse,json,math
from pathlib import Path
out=Path('D:/RCA-flashticket/results/T-017')
ap=argparse.ArgumentParser();ap.add_argument('--run',default='run-dev-004');args=ap.parse_args()
main_path=out/'runs'/args.run/'re2tt_ts-auth-service_cpu_1.json'
ind_path=out/'runs/independent-example-v2.json'
main=json.loads(main_path.read_text(encoding='utf-8'))
ind=json.loads(ind_path.read_text(encoding='utf-8'))
errors=[];nchecks=0;max_error=0.0
def equal(a,b,context):
    global nchecks,max_error
    nchecks+=1
    if isinstance(a,float) or isinstance(b,float):
        delta=abs(a-b);max_error=max(max_error,delta)
        if not math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10):errors.append([context,a,b])
    elif a!=b:errors.append([context,a,b])
for row in ind['metrics']:
    k=row['metric'];m=main['metrics'][k]
    equal(m['count'],row['alerts'],k+'/count')
    equal(m['status']=='ok',row['available'],k+'/available')
    if row['available']:
        for key in ('mean','std','threshold'):equal(m[key],row[key],k+'/'+key)
for row in ind['traces']:
    s=row['service'];m=main['traces'][s]
    equal(m['vote'],row['alert'],s+'/trace')
    if row['available']:
        for mk,ik in [('p95_normal','normal_p95'),('p95_incident','incident_p95'),('threshold','threshold')]:equal(m[mk],row[ik],s+'/'+mk)
for row in ind['services']:
    s=row['service'];m=main['scores'][s]
    for mk,ik in [('metric','metric_alerts'),('trace','trace_alerts'),('log','log_alerts'),('score','score')]:equal(m[mk],row[ik],s+'/'+mk)
equal(main['ranks'],ind['ranking'],'ranking')
report={'status':'PASS' if not errors else 'FAIL','checks':nchecks,'max_absolute_float_error':max_error,'errors':errors,'main':str(main_path),'independent':str(ind_path)}
(out/'runs/example-comparison-v2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report));assert not errors
