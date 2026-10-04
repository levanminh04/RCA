"""Predeclared direction/isolates factors on existing MEM25 R graphs; no PC learning."""
import os,sys,json,csv,time
from pathlib import Path
from datetime import timedelta,datetime
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.path.insert(0,'D:/RCA-ext/work/T-014/CIRCA')
import numpy as np,pandas as pd,networkx as nx
from circa.alg.ci import RHTScorer
from circa.model.graph import MemoryGraph,Node
from circa.model.case import CaseData
from circa.model.data_loader import MemoryDataLoader
out=Path('D:/RCA-flashticket/results/T-014');work=Path('D:/RCA-ext/work/T-014/audit-r/mem-target')
records=json.loads((work/'inputs.json').read_text());assert len(records)==25
dest=out/'audit/graph-factors';dest.mkdir(exist_ok=True);start=time.monotonic();results=[]
modes=[('forward_drop',False,False),('reverse_keep',True,True),('reverse_drop',True,False)]
with (out/'ca-da-chay.csv').open('a',encoding='utf-8',newline='') as registry:
    writer=csv.writer(registry)
    for index,row in enumerate(records,1):
        frame=pd.read_csv(row['input']);names=list(frame);nodes={n:Node(*n.split('_',1)) for n in names}
        matrix=pd.read_csv(work/(row['stem']+'_pcalg.csv'));assert list(matrix)==names
        base=nx.DiGraph();base.add_nodes_from(nodes.values());base.add_edges_from((nodes[names[i]],nodes[names[j]]) for i,j in zip(*np.where(matrix.to_numpy()!=0)))
        loader={}
        for n,node in nodes.items():loader.setdefault(node.entity,{})[node.metric]=list(zip(row['times'],frame[n]))
        context=CaseData(MemoryDataLoader(loader),next(iter(nodes.values())),row['mark'],interval=timedelta(seconds=1))
        saved={};baseline=json.loads((out/'audit/mem-target'/(row['stem']+'.json')).read_text())
        saved['forward_keep']=dict(points=baseline['scores'],ranks=baseline['ranks_author_stable_sort'],source=str(out/'audit/mem-target'/(row['stem']+'.json')))
        for label,reverse,keep in modes:
            graph=base.reverse(copy=True) if reverse else base.copy()
            if not keep:graph.remove_nodes_from(list(nx.isolates(graph)))
            scores=RHTScorer().score(MemoryGraph(graph),context,row['mark']+300)
            points={f'{n.entity}_{n.metric}':v.score for n,v in scores.items()};ranks=[f'{n.entity}_{n.metric}' for n,v in sorted(scores.items(),key=lambda item:item[1].key,reverse=True)]
            assert points and all(np.isfinite(list(points.values())))
            path=dest/(row['stem']+'_'+label+'.json');obj=dict(case=row['case'],configuration=label,graph_backend='same saved R-pcalg graph',graph_nodes=len(graph),graph_edges=len(graph.edges),removed_isolates=[] if keep else [f'{n.entity}_{n.metric}' for n in nx.isolates(base)],points=points,ranks=ranks,graph_source=str(work/(row['stem']+'_pcalg.csv')))
            path.write_text(json.dumps(obj,indent=2));saved[label]=dict(points=points,ranks=ranks,source=str(path))
            writer.writerow([row['case'],row['source'],'CIRCA-original/RHT cached-R-PC '+label,'isolate direction and candidate coverage; no new PC; predeclared factors','b']);registry.flush()
        # Labels are read for evaluation only after every score/rank has been saved.
        answer=row['case'].split('/')[1].split('_')[0];entry=dict(case=row['case'],modes={})
        for label,s in saved.items():
            services=list(dict.fromkeys(n.split('_')[0].replace('-db','') for n in s['ranks']));rank=services.index(answer)+1 if answer in services else None
            entry['modes'][label]=dict(true_service_rank=rank,Avg5=(6-rank)/5 if rank is not None and rank<=5 else 0.,source=s['source'],candidate_count=len(s['points']),changed_points_vs_forward_keep=sum(k not in baseline['scores'] or not np.isclose(v,baseline['scores'][k],atol=1e-7,rtol=1e-7) for k,v in s['points'].items()),removed_candidates=sorted(set(baseline['scores'])-set(s['points'])))
        results.append(entry);print(datetime.now().isoformat(),index,row['case'],'elapsed',time.monotonic()-start,flush=True)
agg={label:float(np.mean([r['modes'][label]['Avg5'] for r in results])) for label in ['forward_keep']+[m[0] for m in modes]}
assert np.isclose(agg['forward_keep'],.864)
summary=dict(n=25,aggregate_Avg5=agg,contrasts=dict(direction_given_keep=agg['reverse_keep']-agg['forward_keep'],direction_given_drop=agg['reverse_drop']-agg['forward_drop'],coverage_given_forward=agg['forward_keep']-agg['forward_drop'],coverage_given_reverse=agg['reverse_keep']-agg['reverse_drop']),per_case=results,elapsed_diagnostic_seconds=time.monotonic()-start,scope='Conditional effects on R-pcalg MEM25 graphs only; no isolated causal-learn backend contrast; no unpublished paper-protocol identification; no accuracy-based selection',published_MEM_Avg5=.74,reused_T006_Avg5=.888)
(out/'audit/graph-factor-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='per_case'}))
