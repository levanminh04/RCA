"""Use original RHT on R matrices; save scores before any label evaluation.

No full baseline rerun. RCAEval old outputs are reused. All nodes are retained;
raw author tie order and alphabetical display order are both saved explicitly.
"""
import csv
from datetime import timedelta,datetime
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/RCA-ext/work/T-014/CIRCA')
import networkx as nx
import numpy as np
import pandas as pd
from circa.alg.ci import RHTScorer
from circa.model.case import CaseData
from circa.model.data_loader import MemoryDataLoader
from circa.model.graph import MemoryGraph,Node

out=Path(__file__).resolve().parent
work=Path('D:/RCA-ext/work/T-014/audit-r/mem-target')
records=json.loads((work/'inputs.json').read_text())
status=pd.read_csv(work/'pc-status.csv')
assert len(records)==len(status)==25 and set(status.status)=={'ok'}
result_dir=out/'mem-target';result_dir.mkdir(exist_ok=True)
summary=[]
start=time.monotonic()
with (out/'cases.csv').open('a',encoding='utf-8-sig',newline='') as stream:
    writer=csv.writer(stream)
    for index,record in enumerate(records,1):
        print(datetime.now().isoformat(),'SCORE_BEGIN',index,25,record['stem'],flush=True)
        frame=pd.read_csv(record['input']);columns=list(frame.columns);values=frame.to_numpy()
        matrix=pd.read_csv(work/(record['stem']+'_pcalg.csv'))
        assert list(matrix.columns)==columns
        nodes=[Node(*name.split('_',1)) for name in columns]
        loader={}
        for i,node in enumerate(nodes):
            loader.setdefault(node.entity,{})[node.metric]=list(zip(record['times'],values[:,i]))
        context=CaseData(MemoryDataLoader(loader),nodes[0],record['mark'],interval=timedelta(seconds=1))
        graph=nx.DiGraph();graph.add_nodes_from(nodes)
        graph.add_edges_from((nodes[a],nodes[b]) for a,b in zip(*np.where(matrix.to_numpy()!=0)))
        scores=RHTScorer().score(MemoryGraph(graph),context,record['mark']+300)
        ordered=sorted(scores.items(),key=lambda item:item[1].key,reverse=True)
        names=lambda node: f'{node.entity}_{node.metric}'
        raw_ranks=[names(node) for node,score in ordered]
        points={names(node):score.score for node,score in scores.items()}
        display=sorted(points,key=lambda key:(-points[key],key))
        tie_groups={}
        for key,value in points.items():tie_groups.setdefault(str(value),[]).append(key)
        loaded=context.load_data(MemoryGraph(graph),record['mark']+300)
        result={'case':record['case'],'configuration':'R_pcalg_full600_originalRHT_same_context_keep_isolates',
                'scores':points,'ranks_author_stable_sort':raw_ranks,'ranks_display_score_name':display,
                'ties':{k:sorted(v) for k,v in tie_groups.items() if len(v)>1},
                'graph_edges':[[names(a),names(b)] for a,b in graph.edges],
                'graph_isolates':[names(n) for n in nx.isolates(graph)],
                'graph_dag':nx.is_directed_acyclic_graph(graph),'num_graph_nodes':len(nodes),
                'num_scored_nodes':len(points),'context':{'train_window':context.train_window,
                    'test_window':context.test_window,'loaded_lengths':sorted(set(map(len,loaded.values()))),
                    'train_time':[record['mark']-120,record['mark']-10],
                    'test_time':[record['mark']+291,record['mark']+300]}}
        path=result_dir/(record['stem']+'.json')
        path.write_text(json.dumps(result,indent=2),encoding='utf-8')
        assert raw_ranks and len(raw_ranks)==len(set(raw_ranks))
        registry_purpose='targeted MEM cell graph backend diagnosis; result saved before evaluation; shared-machine timing diagnostic'
        writer.writerow([record['case'],record['source'],result['configuration'],registry_purpose,'b'])
        stream.flush()
        # Only after writing every unlabelled intermediate and rank, evaluate.
        answer=record['case'].split('/')[1].split('_')[0]
        def evaluate(ranks):
            service_ranks=list(dict.fromkeys(key.split('_')[0].replace('-db','') for key in ranks))
            rank=service_ranks.index(answer)+1 if answer in service_ranks else None
            return {'service_ranks':service_ranks,'true_service_rank':rank,
                    'AC1':float(rank==1),'AC3':float(rank is not None and rank<=3),
                    'Avg5':(6-rank)/5 if rank is not None and rank<=5 else 0.0}
        old_path=Path('D:/RCA-ext/work/T-006/l4-circa-fse-ob-len10-lan1/output/results')/(record['stem']+'.json')
        old=json.loads(old_path.read_text());assert 'error' not in old and len(old)==1
        old_ranks=next(iter(old.values()))
        entry={'case':record['case'],'new_originalRHT_Rgraph':evaluate(raw_ranks),
               'new_display_tie_diagnostic':evaluate(display),'old_T006_reused':evaluate(old_ranks),
               'old_source':str(old_path),'new_source':str(path),'new_num_edges':graph.number_of_edges(),
               'new_num_candidates':len(raw_ranks),'old_num_candidates':len(old_ranks),
               'pc_status':status.set_index('stem').loc[record['stem']].to_dict()}
        summary.append(entry)
        print(datetime.now().isoformat(),'SCORE_END',index,record['stem'],'diagnostic_elapsed_total',time.monotonic()-start,flush=True)

aggregate={name:{metric:float(np.mean([r[name][metric] for r in summary])) for metric in ('AC1','AC3','Avg5')}
           for name in ('new_originalRHT_Rgraph','new_display_tie_diagnostic','old_T006_reused')}
assert abs(aggregate['old_T006_reused']['Avg5']-.888)<1e-12
result={'n':len(summary),'published_BARO_MEM_Avg5':.74,'aggregate':aggregate,'per_case':summary,
        'diagnostic_elapsed_scoring':time.monotonic()-start,
        'timing_note':'shared laptop; not official cost measurement',
        'interpretation':'controlled PC backend/direction/candidate comparison; not original complete factory pipeline and not selection by accuracy'}
(out/'mem-target-summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({key:value for key,value in result.items() if key!='per_case'},indent=2),flush=True)
