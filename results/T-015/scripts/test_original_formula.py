"""Execute author AST functions on label-free counts; compare formula adapter exactly."""
import argparse,ast,json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0,str(ROOT/'src'))
from microrank.detectors import original_trace_partition,original_system_alarm

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=pathlib.Path,default=ROOT/'results/T-015/runs/review-response/original-formula-guard-tests.json')
    args=ap.parse_args()
    assert not args.output.exists(),'Keep prior test output; use a fresh path'
    p=pathlib.Path('C:/Users/84583/AppData/Local/Temp/claude/D--RCA-flashticket/faa9e437-da55-49ba-b763-6e8484c8c9a6/scratchpad/ext/MicroRank/anormaly_detector.py')
    tree=ast.parse(p.read_text(encoding='utf-8'))
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['trace_anormaly_detect','trace_list_partition','system_anormaly_detect']]
    ns={}; exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
    slo={'service_A':[10.0,2.0]}
    fixtures={str(i):{'service_A':1,'duration':d*1000} for i,d in enumerate([12,12.001,13,13.001,62,62.001,100,100,100,100,100,100,100,100])}
    got=original_trace_partition(fixtures,slo); expected=ns['trace_list_partition'](fixtures,slo)
    assert got==expected
    ns['get_span']=lambda *_: ['opaque-span']
    ns['get_operation_duration_data']=lambda *_: fixtures
    expected_alarm=ns['system_anormaly_detect'](0,1,slo,['service_A'])
    got_alarm=original_system_alarm(fixtures,slo)
    assert got_alarm['alarm']==expected_alarm
    root_guards={}
    for duration_name,duration in [('nan',float('nan')),('positive_inf',float('inf')),('negative_inf',-float('inf')),('negative_duration',-1)]:
        for function in [original_trace_partition,original_system_alarm]:
            try:function({'bad':{'service_A':1,'duration':duration}},slo)
            except ValueError as error:root_guards[function.__name__+'_'+duration_name]=str(error)
            else:raise AssertionError('Invalid root duration accepted')
    result={'status':'pass','partition_exact':True,'system_alarm_exact':True,'trace_threshold_strict_gt_and_plus50ms':True,'system_threshold_gt8':True,'abnormal_count':len(got[0]),'alarm_counts':len(got_alarm['abnormal_trace_ids']),'label_free':True,'scope':'formulas on author-schema counts only; no inferred kind/frontend/parquet translation'}
    result['root_duration_guard_cases']=root_guards
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
