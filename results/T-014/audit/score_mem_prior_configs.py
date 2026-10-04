"""Predeclared scorer factors on the 25 existing R graphs; no PC rerun.

SVR sigmoid and DA threshold 3 are from original CIRCA prior-work configs.
This is a protocol diagnostic, never a choice based on accuracy or closeness.
"""
import copy
import csv
from datetime import datetime,timedelta
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/RCA-ext/work/T-014/CIRCA')
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from circa.alg.ci import RHTScorer,DAScorer
from circa.alg.ci.anm import ANMRegressor
from circa.model.case import CaseData
from circa.model.data_loader import MemoryDataLoader
from circa.model.graph import MemoryGraph,Node

out=Path(__file__).resolve().parent
work=Path('D:/RCA-ext/work/T-014/audit-r/mem-target')
records=json.loads((work/'inputs.json').read_text())
base=json.loads((out/'mem-target-summary.json').read_text())
summaries=[]
start=time.monotonic()
with (out/'cases.csv').open('a',encoding='utf-8-sig',newline='') as stream:
    writer=csv.writer(stream)
    for index,record in enumerate(records,1):
        print(datetime.now().isoformat(),'PRIOR_BEGIN',index,25,record['stem'],flush=True)
        frame=pd.read_csv(record['input']);columns=list(frame.columns);values=frame.to_numpy()
        nodes=[Node(*name.split('_',1)) for name in columns]
        loader={}
        for i,node in enumerate(nodes):
            loader.setdefault(node.entity,{})[node.metric]=list(zip(record['times'],values[:,i]))
        context=CaseData(MemoryDataLoader(loader),nodes[0],record['mark'],interval=timedelta(seconds=1))
        graph=nx.DiGraph();graph.add_nodes_from(nodes)
        matrix=pd.read_csv(work/(record['stem']+'_pcalg.csv'))
        assert list(matrix.columns)==columns
        graph.add_edges_from((nodes[a],nodes[b]) for a,b in zip(*np.where(matrix.to_numpy()!=0)))
        memory=MemoryGraph(graph)
        linear=RHTScorer().score(memory,context,record['mark']+300)
        svr_params=SVR(kernel='sigmoid').get_params()
        svr=RHTScorer(regressor=ANMRegressor(regressor=SVR(kernel='sigmoid'))).score(memory,context,record['mark']+300)
        def name(node):return f'{node.entity}_{node.metric}'
        reused=json.loads((out/'mem-target'/(record['stem']+'.json')).read_text())
        assert max(abs(reused['scores'][name(node)]-score.score) for node,score in linear.items())==0
        repeat_diff=None
        if index==1:
            repeat=RHTScorer(regressor=ANMRegressor(regressor=SVR(kernel='sigmoid'))).score(memory,context,record['mark']+300)
            repeat_diff=max(abs(repeat[node].score-score.score) for node,score in svr.items())
            assert repeat_diff==0
            writer.writerow([record['case'],record['source'],'R_pcalg_full600_SVR_sigmoid_RHT_repeat',
                             'repeat same graph/data on first predeclared MEM case','a'])
        configs={
            'SVR_sigmoid_RHT':{'scores':svr,'params':{'regressor':svr_params,'DA':False}},
            'linear_RHT_DA3':{'scores':DAScorer(threshold=3).score(memory,context,record['mark']+300,copy.deepcopy(linear)),
                              'params':{'regressor':'LinearRegression default','DA':True,'threshold':3,'aggregator':'max'}},
            'SVR_sigmoid_RHT_DA3':{'scores':DAScorer(threshold=3).score(memory,context,record['mark']+300,copy.deepcopy(svr)),
                                  'params':{'regressor':svr_params,'DA':True,'threshold':3,'aggregator':'max'}},
        }
        saved={}
        for label,config in configs.items():
            scores=config['scores']
            ordered=sorted(scores.items(),key=lambda item:item[1].key,reverse=True)
            ranks=[name(node) for node,score in ordered]
            result={'case':record['case'],'configuration':label,'parameters':config['params'],
                    'graph_source':str(out/'mem-target'/(record['stem']+'.json')),
                    'same_graph_and_context_as_linear_RHT':True,
                    'scores':{name(node):score.score for node,score in scores.items()},
                    'score_info':{name(node):score.asdict() for node,score in scores.items()},
                    'ranks_author_key_stable_sort':ranks,'repeat_max_diff_first_case':repeat_diff,
                    'purpose':'prior-work scorer factor; not accuracy-based variant selection'}
            folder=out/'mem-target-prior'/label;folder.mkdir(parents=True,exist_ok=True)
            path=folder/(record['stem']+'.json')
            path.write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
            assert ranks and len(ranks)==len(set(ranks))
            writer.writerow([record['case'],record['source'],'R_pcalg_full600_'+label+'_keep_isolates',
                             'targeted MEM diagnostic; prior configuration source before run; same PC graph/candidate/window','b'])
            saved[label]=(path,ranks)
        stream.flush()
        # All score and rank variants have been written without ground truth.
        answer=record['case'].split('/')[1].split('_')[0]
        def evaluate(ranks):
            services=list(dict.fromkeys(key.split('_')[0].replace('-db','') for key in ranks))
            rank=services.index(answer)+1 if answer in services else None
            return {'service_ranks':services,'true_service_rank':rank,'AC1':float(rank==1),
                    'AC3':float(rank is not None and rank<=3),
                    'Avg5':(6-rank)/5 if rank is not None and rank<=5 else 0.0}
        entry={'case':record['case'],'configs':{label:dict(evaluate(ranks),source=str(path)) for label,(path,ranks) in saved.items()}}
        summaries.append(entry)
        print(datetime.now().isoformat(),'PRIOR_END',index,record['stem'],'diagnostic_elapsed_total',time.monotonic()-start,flush=True)
labels=list(summaries[0]['configs'])
aggregates={label:{metric:float(np.mean([r['configs'][label][metric] for r in summaries])) for metric in ('AC1','AC3','Avg5')}
            for label in labels}
result={'n':len(summaries),'published_BARO_MEM_Avg5':.74,'aggregate':aggregates,
        'linear_RHT_and_RE_reuse_source':str(out/'mem-target-summary.json'),
        'linear_RHT_same_Rgraph_aggregate':base['aggregate']['new_originalRHT_Rgraph'],
        'RE_T006_reuse_aggregate':base['aggregate']['old_T006_reused'],
        'per_case':summaries,'diagnostic_elapsed_scoring':time.monotonic()-start,
        'timing_note':'shared laptop, diagnostic only',
        'interpretation':'compatibility test; even score closeness does not identify the unpublished BARO protocol'}
(out/'mem-prior-config-summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='per_case'},indent=2),flush=True)
