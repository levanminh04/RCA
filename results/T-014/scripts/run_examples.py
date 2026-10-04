import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,time,argparse
from pathlib import Path
import pandas as pd,numpy as np,networkx as nx
sys.path[:0]=['D:/RCA-flashticket/src','D:/RCA-ext/src/RCAEval']
from RCAEval.io.time_series import preprocess
from circa_kien_truc import build_graph,score_graph,graph_from_pc,service_calls
ap=argparse.ArgumentParser();ap.add_argument('--repeat',action='store_true');ap.add_argument('--pc',type=str);ap.add_argument('--pc-mode',default='example-pc',choices=['example-pc','example-pc-hashseed1']);ap.add_argument('--normal-only',action='store_true');args=ap.parse_args()
root=Path('D:/RCA-flashticket');out=root/'results/T-014';case=json.loads((out/'runs/selection-before-scores.json').read_text())['selected']
row=next(r for r in json.loads((out/'runs/inventory.json').read_text()) if r['case']==case)
td=row['inject_time'];raw=pd.read_parquet(row['source'])
raw=raw.loc[:,~raw.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
raw=raw.rename(columns={c:c.replace('_latency-90','_latency') for c in raw if c.endswith('_latency-90')})
win=pd.concat([raw[raw.time<td].tail(300),raw[raw.time>=td].head(300)],ignore_index=True)
clean=preprocess(win.copy(),dataset='re2-tt');clean['time']=win.time
call_edges=json.loads((out/'graphs'/f'{case}.json').read_text())['call_edges'];calls=nx.DiGraph(call_edges)
reports=[]
def dump(mode,frame,graph,detect,current=None):
    tic=time.monotonic();snapshot=score_graph(frame,graph,detect,current)
    path=out/'runs'/mode;path.mkdir(exist_ok=True)
    (path/'snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
    # Labels are accessed only after score/ranking have been saved.
    root_service=case.removeprefix('re2tt_').rsplit('_',2)[0]
    root_metrics=[dict(rank=i+1,metric=n,score=s) for i,(n,s) in enumerate(snapshot['ranks']) if n.startswith(root_service+'_')]
    services=[]
    for name,_ in snapshot['ranks']:
        service=name.rsplit('_',1)[0]
        if service not in services:services.append(service)
    info=dict(case=case,mode=mode,score_count=len(snapshot['nodes']),root_service=root_service,root_service_rank=services.index(root_service)+1 if root_service in services else None,root_metrics=root_metrics,top5=snapshot['ranks'][:5],candidate_count=len(graph),da_top5=snapshot.get('ranks_da',[])[:5],scores_ge3=sum(n['rht_score']>=3 for n in snapshot['nodes'].values()),large_scores=[dict(metric=k,score=v['rht_score'],scale=v['residual_scale']) for k,v in snapshot['nodes'].items() if v['rht_score']>1e6],elapsed_diagnostic=time.monotonic()-tic)
    (path/'interpretation.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(info,ensure_ascii=False),flush=True)
    reports.append(info)
    return snapshot
graph,g_report=build_graph(clean.columns,calls,'D:/RCA-ext/work/T-014/CIRCA')
if args.normal_only:
    normal_raw=raw[raw.time<td].copy();normal_detect=td-301;normal_current=td-1
    normal=preprocess(normal_raw.copy(),dataset='re2-tt');normal['time']=normal_raw.time
    tr=pd.read_parquet(root/'data/rcaeval'/case/'traces.parquet',columns=['traceID','spanID','parentSpanID','serviceName','startTime'])
    nn_calls,tr_report=service_calls(tr,normal_detect)
    nn_graph,nn_report=build_graph(normal.columns,nn_calls,'D:/RCA-ext/work/T-014/CIRCA')
    dump('normal-normal-architecture-pretrace',normal,nn_graph,normal_detect,normal_current)
    (out/'runs/normal-normal-architecture-pretrace/graph-report.json').write_text(json.dumps(dict(trace=tr_report,graph=nn_report),indent=2))
elif args.pc:
    adj=np.load(args.pc);graph=graph_from_pc(adj,list(clean.drop(columns='time')))
    dump(args.pc_mode,clean,graph,td)
else:
    name='example-architecture-repeat' if args.repeat else 'example-architecture'
    first=dump(name,clean,graph,td)
    (out/'runs'/name/'graph-report.json').write_text(json.dumps(g_report,indent=2))
    if not args.repeat:
        original,legacy=build_graph(clean.columns,calls,'D:/RCA-ext/work/T-014/CIRCA',retain_isolates=False)
        dump('example-architecture-original-coverage',clean,original,td)
        perm=clean[list(reversed(clean.columns))]
        altered=dump('example-architecture-permuted',perm,graph,td)
        diff=max(abs(first['nodes'][n]['rht_score']-altered['nodes'][n]['rht_score']) for n in first['nodes'])
        (out/'runs/permutation-architecture.json').write_text(json.dumps(dict(max_score_abs_diff=diff,same_nodes=set(first['nodes'])==set(altered['nodes']),same_ranking=first['ranks']==altered['ranks']),indent=2))
        # Detect/current and both scoring windows are strictly before injection.
        normal_raw=raw[raw.time<td].copy()
        normal_detect=td-301;normal_current=td-1
        normal=preprocess(normal_raw.copy(),dataset='re2-tt');normal['time']=normal_raw.time
        normal_graph,_=build_graph(normal.columns,calls,'D:/RCA-ext/work/T-014/CIRCA')
        dump('normal-normal-architecture',normal,normal_graph,normal_detect,normal_current)
with (out/'runs/example-progress.jsonl').open('a',encoding='utf-8') as f:
    for report in reports:f.write(json.dumps(report,ensure_ascii=False)+'\n')
