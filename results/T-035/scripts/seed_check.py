import os,sys,json,time
from pathlib import Path
from run import ROOT,OUT,load,read,write,Prepared,from_p3

name=sys.argv[1];out=OUT/'runs'/name;out.mkdir(exist_ok=False)
cases=read(OUT/'runs/pilot-002/summary.json')['cases'];results=[];t0=time.perf_counter()
for c in cases:
    ds,oid=c['dataset'],c['opaque_id'];frame,t,alias,u,_,_=load(ds,oid)
    p=Prepared(from_p3(frame),alias,u)
    checks=[]
    for window in c['windows']:
        base=OUT/'runs/pilot-002/do-thi'/ds/oid
        old=read(base/'thuc-the'/f'{window}.json');e,o=p.graph(old['interval_ns'])
        assert json.loads(json.dumps(e,ensure_ascii=False))==old,'seed_entity_changed'
        if window in ('full','N','A'):
            assert json.loads(json.dumps(o,ensure_ascii=False))==read(base/'thao-tac'/f'{window}.json'),'seed_operation_changed'
        checks.append({'window':window,'entity_equal':True,'operation_equal':True if window in ('full','N','A') else None})
    results.append({'dataset':ds,'opaque_id':oid,'checks':checks})
    print(ds,oid,'PASS',flush=True)
write(out/'result.json',{'seed':os.environ.get('PYTHONHASHSEED'),'cases':results,'pass':True,'seconds':time.perf_counter()-t0})
