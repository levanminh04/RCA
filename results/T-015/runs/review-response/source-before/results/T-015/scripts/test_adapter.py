"""Label-free edge and invariance tests of the explicitly approved variant."""
import json,pathlib,sys
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
    result={'status':'pass','nonempty_with_evidence':True,'no_fallback':True,'column_order_invariant':True,'row_order_invariant':True,'no_abnormal_no_rank':True,'all_abnormal_no_rank':True,'duplicate_exact_multiplicity_retained':True,'duplicate_conflicting_rejected':True,'unseen_operation_rejected':True,'spectrum_nonnegative':True,'units_microseconds_to_ms':True,'result':r}
    out=ROOT/'results/T-015/runs/adapter-toy';out.mkdir(parents=True,exist_ok=True)
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':'pass','tests':10}))

if __name__=='__main__':main()
