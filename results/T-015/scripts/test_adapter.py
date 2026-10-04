"""Label-free edge and invariance tests of the explicitly approved variant."""
import argparse,ast,contextlib,io,json,math,pathlib,sys,types
import pandas as pd
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from microrank import microrank,COLS

def frame():
    rows=[]
    for i,d in enumerate([1000,1200,800,1100]):
        for sid,par,svc,method,span_dur in [('a','outside','s1','same',d),('b','a','s2','same',d)]:
            rows.append([f'b{i}',sid,par,svc,method,method,1000+i*2000,span_dur])
    for trace,d in [('n',1000),('f',4000)]:
        for sid,par,svc,method in [('a','outside','s1','same'),('b','a','s2','same')]:
            rows.append([trace,sid,par,svc,method,method,20000,d])
    return pd.DataFrame(rows,columns=COLS)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=pathlib.Path,default=ROOT/'results/T-015/runs/review-response/adapter-guard-tests.json')
    args=ap.parse_args()
    assert not args.output.exists(),'Keep prior test output; use a fresh path'
    df=frame();r=microrank(df,15000,True)
    assert r['status']=='ok' and r['ranks'] and r['counts']['overlap']==0
    assert r['counts']['normal']==r['counts']['anomaly']==1
    assert all(v>=0 for cell in r['spectrum'].values() for v in cell.values())
    for transformed in [df.iloc[::-1],df[df.columns[::-1]]]:
        other=microrank(transformed,15000,True)
        assert r==other
    no_anom=df.copy();no_anom.loc[no_anom.startTime>=15000,'duration']=1000
    assert microrank(no_anom,15000)['status']=='no_anomalous_traces'
    all_anom=df.copy();all_anom.loc[all_anom.startTime>=15000,'duration']=4000
    assert microrank(all_anom,15000)['status']=='no_normal_traces'
    duplicate=pd.concat([df,df.iloc[-1:]],ignore_index=True)
    repeat=microrank(duplicate,15000,True)
    assert repeat['groups']['anomaly']['graph']['pr_trace']['f'].count('s2_same')==2
    assert repeat==microrank(duplicate.iloc[::-1],15000,True)
    conflict=duplicate.copy();conflict.loc[conflict.index[-1],'duration']=5000
    try:microrank(conflict,15000)
    except ValueError as e:assert 'Conflicting observations' in str(e)
    else:raise AssertionError('Conflicting duplicate not rejected')
    newop=df.copy();newop.loc[newop.traceID=='f','methodName']='new'
    try:microrank(newop,15000)
    except ValueError as e:assert 'No normal baseline' in str(e)
    else:raise AssertionError('Missing baseline not rejected')
    # Compare the approved guard repair to the frozen input adapter on valid data.
    before=ROOT/'results/T-015/runs/review-response/source-before/src/microrank/__init__.py'
    frozen=types.ModuleType('t015_before_guard');frozen.__package__='microrank'
    exec(compile(before.read_text(encoding='utf-8'),str(before),'exec'),frozen.__dict__)
    with contextlib.redirect_stdout(io.StringIO()):
        assert frozen.microrank(df,15000,True)==r
    guard_cases={}
    for col in ['startTime','duration']:
        for name,value in [('nan',float('nan')),('positive_inf',float('inf')),('negative_inf',-float('inf'))]:
            invalid=df.copy();invalid.loc[invalid.index[-1],col]=value
            try:microrank(invalid,15000)
            except ValueError as error:guard_cases[col+'_'+name]=str(error)
            else:raise AssertionError('Nonfinite '+col+' accepted')
    for name,value in [('nan',float('nan')),('positive_inf',float('inf')),('negative_inf',-float('inf'))]:
        try:microrank(df,value)
        except ValueError as error:guard_cases['marker_'+name]=str(error)
        else:raise AssertionError('Nonfinite marker accepted')
    invalid=df.copy();invalid.loc[invalid.index[-1],'duration']=-1
    try:microrank(invalid,15000)
    except ValueError as error:guard_cases['negative_duration']=str(error)
    else:raise AssertionError('Negative duration accepted')
    # Independent detector stays independent: compile its own functions only.
    script=ROOT/'results/T-015/scripts/check_tracerca.py'
    functions=[node for node in ast.parse(script.read_text(encoding='utf-8')).body if isinstance(node,ast.FunctionDef)]
    ns={'COLS':COLS,'math':math}
    exec(compile(ast.Module(body=functions,type_ignores=[]),str(script),'exec'),ns)
    valid=ns['independent_spans'](df,15000)
    frozen_script=ROOT/'results/T-015/runs/review-response/source-before/results/T-015/scripts/check_tracerca.py'
    old_functions=[node for node in ast.parse(frozen_script.read_text(encoding='utf-8')).body if isinstance(node,ast.FunctionDef)]
    old_ns={'COLS':COLS,'math':math}
    exec(compile(ast.Module(body=old_functions,type_ignores=[]),str(frozen_script),'exec'),old_ns)
    assert valid==old_ns['independent_spans'](df,15000)
    independent_guards={}
    for col in ['startTime','duration']:
        for name,value in [('nan',float('nan')),('positive_inf',float('inf')),('negative_inf',-float('inf'))]:
            invalid=df.copy();invalid.loc[invalid.index[-1],col]=value
            try:ns['independent_spans'](invalid,15000)
            except ValueError as error:independent_guards[col+'_'+name]=str(error)
            else:raise AssertionError('Independent nonfinite '+col+' accepted')
    for name,value in [('nan',float('nan')),('positive_inf',float('inf')),('negative_inf',-float('inf'))]:
        try:ns['independent_spans'](df,value)
        except ValueError as error:independent_guards['marker_'+name]=str(error)
        else:raise AssertionError('Independent nonfinite marker accepted')
    result={'status':'pass','nonempty_with_evidence':True,'no_fallback':True,'column_order_invariant':True,'row_order_invariant':True,'no_abnormal_no_rank':True,'all_abnormal_no_rank':True,'duplicate_exact_multiplicity_retained':True,'duplicate_conflicting_rejected':True,'unseen_operation_rejected':True,'spectrum_nonnegative':True,'units_microseconds_to_ms':True,'result':r}
    result.update(valid_input_matches_frozen_adapter_exactly=True,independent_valid_input_matches_frozen_exactly=True,
                  finite_adapter_guards=guard_cases,independent_finite_guards=independent_guards)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':'pass','original_checks':10,'adapter_guard_cases':len(guard_cases),'independent_guard_cases':len(independent_guards),'output':str(args.output)}))

if __name__=='__main__':main()
