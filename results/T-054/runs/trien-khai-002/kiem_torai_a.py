"""CSV tác giả tự sinh: prep A và đường hai tầng; không đọc nguồn A thật."""
import copy
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT/'results/T-054/scripts'), str(ROOT/'src')]
from bien_nhan import OUT, atomic, canonical, fingerprint, ref, read_pin, verify_envelope
from nguon import Blocked, authorize, author_source
import dieu_phoi as q


def main(destination):
    import pandas as pd
    out = Path(destination).resolve(); out.mkdir(parents=True, exist_ok=False)
    base = out/'synthetic-data'; base.mkdir()
    origin = atomic(base/'origin.json', {'schema':'T054-GENERATED-FIXTURE'})
    t = 1700000000
    metric = pd.DataFrame({'time':range(t-350,t+350),
        'ts-a-service_cpu':[1+(i%7)/10 if i<350 else 5+(i%3)/10 for i in range(700)],
        'ts-b-service_cpu':[1+(i%5)/10 for i in range(700)],
        'ts-a-service_latency':[1+(i%3)/10 if i<350 else 6+(i%2)/10 for i in range(700)]})
    metric_path=base/'metrics.parquet';metric.to_parquet(metric_path,index=False)
    files={}
    times=list(range(t-450,t+451,15))
    for name in ('logts','tracets_err','tracets_lat'):
        tab=pd.DataFrame({'time':times,'ts-a-service':[float(1+i%2 if x<t else 4+i%3) for i,x in enumerate(times)],
                          'ts-b-service':[float(i%2) for i in range(len(times))]})
        path=base/(name+'.csv');tab.to_csv(path,index=False,float_format='%.17g')
        pin=ref(path);files[name]={'path':path.name,'sha256':pin['sha256'],'bytes':pin['bytes']}
    member='a'*64
    author=atomic(out/'author-source.json',{'schema':'T054-TORAI-A-SOURCE-1','dataset':'RE2-TT','g1_revision':'fixture-g1',
               'data_root':str(base),'cases_by_member':{member:{'files':files}}})
    mp=ref(metric_path)
    source={'member_sha256':member,'t':t,'ce_history':'verified',
            'files':{'metrics.parquet':{'path':metric_path.name,'sha256':mp['sha256'],'bytes':mp['bytes']}}}
    jobs=[]
    for seed in (0,1,2):
        slot={'dataset':'RE2-TT','opaque_id':'fixture-A','member_sha256':member,'arm':'torai_A','view':'main','seed':seed,
              'window':{'t':t,'half_width_s':300},'source_sha256':fingerprint(source),
              'config_sha256':'b'*64,'environment_sha256':'c'*64,'author_source_sha256':author['sha256']}
        job={'kind':'synthetic','pipeline_fixture':True,'slot':slot,'executable':sys.executable,
             'prep_executable':sys.executable,'method_executable':'D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe',
             'timeout_s':45,'a4':False,'source':source,'data_root':str(base),'fixture_origin':origin,
             'author_source_ref':author,'g1_revision':'fixture-g1','t':t,'method_version':'src/torai/torai_sua.py (Q74 A)',
             'pythonpath':[str(ROOT/'src'),'D:/RCA-ext/src/RCAEval','D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']}
        jobs.append(job)
    plan={'schema':'T054-PLAN-1','mode':'synthetic','host_role':'local','jobs':jobs,
          'monitor':{'poll_s':.05,'max_monitor_gap_s':2,'score_phases':['method']},
          'budget':{'wall_s':120,'method_dataset_s':{'RE2-TT|torai_A':90}}}
    # Quyền giữ A không là quyền mở CSV A thật.
    try:
        authorize(dict(plan,mode='dev'),{'pilot_grant':True},'run')
    except Blocked:
        denied=True
    else:
        raise AssertionError('A without source grant accepted')
    for job in jobs:
        assert set(author_source(job))=={'logts','tracets_err','tracets_lat'}
    q.supervise(plan,out/'queue')
    state=q.status(out/'queue');prepared=[];method_records=[]
    for job in jobs:
        attempt=out/'queue'/fingerprint(job['slot'])/'attempt-001'
        prep=read_pin(ref(attempt/'prepare/prepared.json'))
        assert prep['author_source_ref']==author
        assert prep['details']['nguong_tracets_lat']=='toàn file (tác giả)'
        counts={k:len(pd.read_csv(v['path'])) for k,v in prep['tables'].items()}
        assert all(counts[k]==40 for k in ('logts','tracets_err','tracets_lat')),counts
        prepared.append(prep)
        method=attempt/'method'
        envelope=read_pin(ref(method/'result.json'));invocation=read_pin(ref(method/'invocation.json'))
        rows=verify_envelope(envelope,invocation,job['slot'],envelope['token'])
        assert invocation['prepared_ref']['sha256']==ref(attempt/'prepare/prepared.json')['sha256']
        assert rows[0]['method']=='torai' and rows[0]['variant']=='A' and rows[0]['seed']==job['slot']['seed']
        assert rows[0]['extra']['information_boundary']=='author_full_file_retrospective'
        method_records.append({'seed':job['slot']['seed'],'status':rows[0]['status'],
             'state':state['jobs'][fingerprint(job['slot'])]['state'],
             'method':ref(method/'result.json'),'actual_python':job['method_executable']})
    for k in ('metric','logts','tracets_err','tracets_lat'):
        assert len({p['tables'][k]['sha256'] for p in prepared})==1,k
    assert len({p['normalized_input_sha256'] for p in prepared})==1
    atomic(out/'summary.json',{'PASS':True,'source_grant_guard':denied,'prep_seed_independent_bytes':True,
        'three_seeds':method_records,'scope':'actual A preprocessing and Python3.8 method only on generated telemetry/CSV',
        'real_author_source_opened':False,'scientific_reproduction':False,
        'note':'ERROR status if any remains BLOCKED; transport PASS does not turn synthetic cases into benchmark results.'})
    print(json.dumps({'PASS':True,'records':method_records,'output':str(out)}))


if __name__=='__main__':
    try:main(sys.argv[1])
    except BaseException:
        path=Path(sys.argv[1])
        if path.exists():atomic(path/'failure.json',{'traceback':traceback.format_exc()})
        raise
