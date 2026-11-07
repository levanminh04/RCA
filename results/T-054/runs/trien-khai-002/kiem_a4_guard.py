"""Thiếu/sai ca hoặc seed phải dừng trước mọi lần đọc nhãn."""
import copy
import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'results/T-054/scripts'))
from bien_nhan import OUT,Blocked,atomic,fingerprint
import cham


def main(destination):
    out=Path(destination).resolve();out.mkdir(parents=True,exist_ok=False)
    runtimes={ds:{'dataset':ds,'cases':{'fixture-'+ds:{'member_sha256':'a'*64}}} for ds in ('RE2-TT','Nezha-OB')}
    jobs=[]
    for ds in runtimes:
        oid='fixture-'+ds
        for arm,seeds in [('M1',(None,)),('torai_B',(0,1,2))] if ds=='RE2-TT' else [('M1',(None,)),('simplerca',(None,))]:
            for seed in seeds:
                jobs.append({'kind':'synthetic','a4':True,'slot':{'dataset':ds,'opaque_id':oid,'arm':arm,'view':'main',
                    'seed':seed,'member_sha256':'a'*64,'window':{},'source_sha256':'b'*64}})
    plan={'mode':'synthetic','jobs':jobs}
    cham.validate_a4_slots(plan,runtimes)
    cases=[]
    bad=copy.deepcopy(plan);bad['jobs'].pop(3);cases.append(('missing_seed',bad,runtimes))
    bad=copy.deepcopy(plan);bad['jobs'].append(copy.deepcopy(bad['jobs'][1]));cases.append(('duplicate_seed',bad,runtimes))
    bad=copy.deepcopy(plan);bad['jobs'][1]['slot']['arm']='torai_A';cases.append(('A_in_primary_A4',bad,runtimes))
    bad=copy.deepcopy(plan);bad['jobs'][1]['slot']['member_sha256']='c'*64;cases.append(('wrong_member',bad,runtimes))
    bad=copy.deepcopy(plan);bad['jobs'][0]['slot']['view']='ce';cases.append(('ce_in_A4',bad,runtimes))
    bad=copy.deepcopy(plan);bad['jobs'][1]['slot']['seed']=False;cases.append(('bool_instead_of_seed0',bad,runtimes))
    bad=copy.deepcopy(plan);bad['mode']='test';cases.append(('incomplete_test_cohort',bad,runtimes))
    timed=copy.deepcopy(runtimes)
    for ds in timed:
        next(iter(timed[ds]['cases'].values()))['t']=1000
    cases.append(('wrong_numeric_window',plan,timed))
    checked=[]
    for name,bad,runtime in cases:
        snapshot={'plan_sha256':fingerprint(bad)}
        with patch.object(cham,'verify_snapshot',return_value={}), patch.object(cham,'read_pin',side_effect=AssertionError('LABEL READER CALLED')) as reader:
            try:cham.evaluate(snapshot,bad,{}, {},runtime,{}, {},out/name)
            except Blocked:pass
            else:raise AssertionError('invalid A4 accepted: '+name)
            assert reader.call_count==0,name
        checked.append(name)
    atomic(out/'summary.json',{'PASS':True,'positive_registered_slots':6,'prelabel_counterexamples':checked,
          'label_reads_on_bad_input':0,'scope':'synthetic metadata; seal verification isolated by spy, positive full report regression separate'})
    print(json.dumps({'PASS':True,'counterexamples':len(checked),'label_reads':0}))


if __name__=='__main__':main(sys.argv[1])
