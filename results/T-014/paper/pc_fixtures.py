"""PC nhỏ trên tín hiệu giả đã chốt; không đọc dữ liệu RCA hoặc code T014-main.

Default dùng pc() nguyên trạng. Prefix depth0/1 chỉ thêm điều kiện d<cap
vào while skeleton trong bản compile tại bộ nhớ; không sửa thư viện.
"""
from __future__ import annotations
import ast
import contextlib
import copy
from datetime import datetime, timezone, timedelta
import hashlib
import importlib
import inspect
import io
import json
from pathlib import Path
import sys
import time
import traceback
import warnings

import numpy as np
import pandas as pd
import networkx as nx

import causallearn.search.ConstraintBased.PC as pc_module
import causallearn.utils.PCUtils.SkeletonDiscovery as skeleton_module

OUT = Path(__file__).resolve().parent / ('pc-fixtures-002' if '--run002' in sys.argv else 'pc-fixtures-001')
OUT.mkdir(exist_ok=True)
SEED, N = 20261004, 2000
names = [f's{i}_cpu' for i in range(5)]
original_skeleton = skeleton_module.skeleton_discovery
source_skeleton = inspect.getsource(original_skeleton)


def progress(event, **kwargs):
    record = {'utc': datetime.now(timezone.utc).isoformat(), 'event': event, **kwargs}
    with (OUT/'progress.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(record,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps(record,ensure_ascii=False,allow_nan=False),flush=True)


def json_float(value):
    return float(value) if np.isfinite(value) else None


class RecordCI:
    def __init__(self, base, records):
        self.base, self.records = base, records
        self.method = base.method
    def __getattr__(self, name):
        return getattr(object.__getattribute__(self,'base'), name)
    def __deepcopy__(self, memo):
        result=RecordCI(copy.deepcopy(self.base,memo),self.records)
        memo[id(self)]=result
        return result
    def __call__(self, a, b, conditioning, *args):
        tic = time.monotonic()
        try:
            p = self.base(a, b, conditioning, *args)
            self.records.append({'a':int(a),'b':int(b),'S':list(map(int,conditioning)),
                                 'p':json_float(p),'p_nonfinite':not bool(np.isfinite(p)),
                                 'elapsed_diagnostic':time.monotonic()-tic})
            return p
        except Exception as exc:
            self.records.append({'a':int(a),'b':int(b),'S':list(map(int,conditioning)),
                                 'exception_type':type(exc).__name__,'exception':str(exc),
                                 'elapsed_diagnostic':time.monotonic()-tic})
            raise


def prefix_function(cap):
    tree = ast.parse(source_skeleton)
    loops = [x for x in ast.walk(tree) if isinstance(x,ast.While)]
    assert len(loops) == 1
    loops[0].test = ast.BoolOp(op=ast.And(),values=[loops[0].test,
        ast.Compare(left=ast.Name(id='depth',ctx=ast.Load()),ops=[ast.Lt()],
                    comparators=[ast.Constant(value=cap)])])
    ast.fix_missing_locations(tree)
    namespace = dict(skeleton_module.__dict__)
    exec(compile(tree, '<T014 fixture prefix depth>', 'exec'), namespace)
    return namespace['skeleton_discovery']


def endpoints(matrix, labels):
    result=[]
    for i in range(len(labels)):
        for j in range(i+1,len(labels)):
            if matrix[i,j] or matrix[j,i]:
                a,b=labels[i],labels[j]
                u,v=int(matrix[i,j]),int(matrix[j,i])
                result.append([a,b,u,v] if a<b else [b,a,v,u])
    return sorted(result)


def run_pc(tag, data, labels, alpha=.05, cap=None):
    ci,stdout,stderr=[],io.StringIO(),io.StringIO()
    implementation = original_skeleton if cap is None else prefix_function(cap)
    def instrumented(data, alpha, indep_test, *args, **kwargs):
        return implementation(data,alpha,RecordCI(indep_test,ci),*args,**kwargs)
    tic=time.monotonic()
    progress('PC_start',fixture=tag,alpha=alpha,depth='default' if cap is None else cap)
    result={'tag':tag,'alpha':alpha,'depth_mode':'default' if cap is None else f'prefix_{cap}',
            'shape':list(data.shape),'labels':labels,'raw_sha256':hashlib.sha256(data.tobytes()).hexdigest()}
    skeleton_module.skeleton_discovery=instrumented
    try:
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr),warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            graph=pc_module.pc(data,alpha=alpha,indep_test='fisherz',stable=True,
                              uc_rule=0,uc_priority=2,show_progress=False,node_names=labels)
        matrix=graph.G.graph
        result.update(status='returned',matrix=matrix.tolist(),edges=endpoints(matrix,labels),
                      edge_count=len(endpoints(matrix,labels)),
                      warnings=[str(x.message) for x in caught],
                      correlation_nonfinite=bool(not np.isfinite(np.corrcoef(data,rowvar=False)).all()))
    except Exception as exc:
        result.update(status='exception',exception_type=type(exc).__name__,exception=str(exc),
                      traceback=traceback.format_exc())
    finally:
        skeleton_module.skeleton_discovery=original_skeleton
    result.update(CI=ci,CI_count=len(ci),max_condition_size=max((len(x['S']) for x in ci),default=None),
                  nonfinite_p_count=sum(x.get('p_nonfinite',False) for x in ci),
                  stdout=stdout.getvalue(),stderr=stderr.getvalue(),elapsed_diagnostic=time.monotonic()-tic)
    (OUT/(tag+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    progress('PC_end',fixture=tag,status=result['status'],edges=result.get('edge_count'),
             CI_count=len(ci),elapsed_diagnostic=result['elapsed_diagnostic'])
    return result


def invoke(tag, function, frame):
    stdout,stderr=io.StringIO(),io.StringIO();tic=time.monotonic()
    result={'tag':tag,'input_columns':frame.columns.tolist()}
    try:
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
            output=function(frame.copy(),inject_time=N//2,dataset='fixture')
        result.update(status='returned',ranks=output.get('ranks'),node_names=output.get('node_names'),
                      adj=np.asarray(output.get('adj')).tolist())
    except Exception as exc:
        result.update(status='exception',exception_type=type(exc).__name__,exception=str(exc))
    result.update(stdout=stdout.getvalue(),stderr=stderr.getvalue(),elapsed_diagnostic=time.monotonic()-tic)
    return result


def snapshot_rht(matrix,data,labels):
    from RCAEval.classes.graph import Node,MemoryGraph
    from RCAEval.classes.data import CaseData,MemoryDataLoader
    from RCAEval.graph_heads.rht import RHTScorer,DAScorer
    from sklearn.linear_model import LinearRegression
    import copy
    graph=nx.DiGraph();nodes={label:Node(*label.split('_')) for label in labels}
    # Match original conversion exactly, including the final reverse.
    for a in range(len(matrix)):
        for b in range(len(matrix)):
            u,v=matrix[a,b],matrix[b,a]
            if u==v==0:continue
            if u==v==-1:graph.add_edge(nodes[labels[b]],nodes[labels[a]])
            elif u==1 and v==-1:graph.add_edge(nodes[labels[b]],nodes[labels[a]])
            elif u==-1 and v==1:graph.add_edge(nodes[labels[a]],nodes[labels[b]])
            else:raise ValueError('Unexpected endpoints')
    graph=graph.reverse(copy=True);mg=MemoryGraph(graph);byname={v:k for k,v in nodes.items()}
    loader=MemoryDataLoader({node.entity:{node.metric:list(zip(range(N),data[:,k]))}
                             for k,(label,node) in enumerate(nodes.items())})
    case=CaseData(loader,sli=nodes[labels[0]],detect_time=N//2,interval=timedelta(seconds=1))
    current=N//2+300;series=case.load_data(mg,current);scorer=RHTScorer()
    official=scorer.score(mg,case,current);snap={}
    for node,score in official.items():
        parents=list(mg.parents(node));px,tx,py,ty=scorer.split_data(series,node,parents,case)
        fallback=False
        if len(px):
            try:
                model=LinearRegression().fit(px,py);pe=py-model.predict(px);te=ty-model.predict(tx)
            except ValueError:fallback=True;pe=py;te=ty
        else:pe=py;te=ty
        snap[byname[node]]={'parents':[byname[p] for p in parents if p in series],
            'train_x':px.tolist(),'test_x':tx.tolist(),
            'x_memory_order':'F' if px.flags.f_contiguous or px.strides[0]<=px.strides[1] else 'C',
            'train_y':py.tolist(),'test_y':ty.tolist(),'rht_score':float(score.score),
            'confidence':float(score['Confidence']),'official_train_residual':pe.tolist(),
            'official_test_residual':te.tolist(),'regression_fallback':fallback}
    da_scorer=DAScorer(threshold=3);actual_order=[]
    def capture(frame,event,arg):
        if event=='return' and frame.f_locals.get('self') is da_scorer:
            actual_order[:]=[[byname[n] for n in group] for group in frame.f_locals.get('sorted_nodes',[])]
    old=sys.getprofile();sys.setprofile(capture)
    try:adjusted=da_scorer.score(mg,case,current,copy.deepcopy(official))
    finally:sys.setprofile(old)
    return {'meta':{'train_window':case.train_window,'test_window':case.test_window,
                    'detect_time':N//2,'current':current,'source':'synthetic_fixture'},
            'graph':{'nodes':[byname[x] for x in graph.nodes],
                     'edges':[[byname[a],byname[b]] for a,b in graph.edges],
                     'topological_groups':[[byname[x] for x in group] for group in mg.topological_sort],
                     'da_iteration_order':actual_order},'nodes':snap,
            'da':{byname[n]:{'score':float(s.score),'key':list(s.key),
                             'child_score':s.get('child_score'),'index':s['index']} for n,s in adjusted.items()}}


def main():
    progress('start',seed=SEED,n=N,note='Synthetic only; elapsed is diagnostic under concurrent laptop workload')
    rng=np.random.default_rng(SEED);noise=rng.normal(size=(N,5))
    chain=np.column_stack([noise[:,0],np.zeros((N,3)),noise[:,4]])
    for k in range(1,4):chain[:,k]=.8*chain[:,k-1]+noise[:,k]
    collider=np.column_stack([noise[:,0],noise[:,1],.8*noise[:,0]+.8*noise[:,1]+noise[:,2],np.zeros(N),noise[:,4]])
    collider[:,3]=.7*collider[:,2]+noise[:,3]
    independent=np.linalg.qr(noise-noise.mean(axis=0))[0]
    constant=chain.copy();constant[:,4]=1.
    duplicate=chain.copy();duplicate[:,4]=duplicate[:,1]
    np.savez_compressed(OUT/'synthetic-inputs.npz',chain=chain,collider=collider,
                        independent=independent,constant=constant,duplicate=duplicate)
    records=[]
    for fixture,data in [('chain',chain),('collider',collider)]:
        for alpha in [.01,.05,.1]:
            for cap in [None,0,1]:
                tag=f'{fixture}-alpha{alpha}-'+('default' if cap is None else f'prefix{cap}')
                records.append(run_pc(tag,data,names,alpha,cap))
    for fixture,data in [('chain',chain),('collider',collider)]:
        order=[4,2,0,3,1]
        records.append(run_pc(f'{fixture}-permuted',data[:,order],[names[k] for k in order]))
    for fixture,data in [('orthogonal-empty',independent),('constant-unprocessed',constant),('duplicate-singular',duplicate)]:
        records.append(run_pc(fixture,data,names))
    sys.path.insert(0,'D:/RCA-ext/src/RCAEval')
    circa_module=importlib.import_module('RCAEval.e2e.circa')
    from RCAEval.e2e import rca
    closure=[c.cell_contents for c in circa_module.circa.__closure__ if callable(c.cell_contents)]
    assert len(closure)==1;raw_circa=closure[0]
    wrappers=[]
    for fixture,data in [('constant-preprocessed',constant),('duplicate-singular',duplicate),('orthogonal-empty',independent)]:
        frame=pd.DataFrame(data,columns=names);frame['time']=np.arange(N)
        wrappers.append(invoke(fixture+'-unwrapped',raw_circa,frame))
        wrappers.append(invoke(fixture+'-wrapped',circa_module.circa,frame))
    @rca
    def deliberate_failure(data,inject_time=None,dataset=None):
        raise RuntimeError('T014 deliberate failure fixture')
    frame=pd.DataFrame(chain,columns=names);frame['time']=np.arange(N)
    wrappers.append(invoke('deliberate-failure-wrapper',deliberate_failure,frame))
    wrappers.append(invoke('deliberate-failure-permuted-wrapper',deliberate_failure,frame[list(reversed(frame.columns))]))
    (OUT/'wrapper-results.json').write_text(json.dumps(wrappers,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    chosen=next(r for r in records if r['tag']=='chain-alpha0.05-default')
    snap=snapshot_rht(np.array(chosen['matrix']),chain,names)
    (OUT/'snapshot.json').write_text(json.dumps(snap,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    comparisons=[]
    for fixture in ['chain','collider']:
        default=next(r for r in records if r['tag']==fixture+'-alpha0.05-default')
        perm=next(r for r in records if r['tag']==fixture+'-permuted')
        comparisons.append({'fixture':fixture,'column_permutation_same_labeled_endpoints':default['edges']==perm['edges']})
    report={'seed':SEED,'samples':N,'data_source':'synthetic only, no RCA cases or labels',
            'estimated_before_run_seconds':120,'time_is_official':False,
            'depth_implementation':'AST replaces single while condition with original_condition and depth<cap; only in-memory prefix functions, restored after call',
            'defaults':str(inspect.signature(pc_module.pc)),
            'pc_source':pc_module.__file__,'skeleton_source':skeleton_module.__file__,
            'skeleton_source_sha256':hashlib.sha256(source_skeleton.encode()).hexdigest(),
            'records':records,'permutation_checks':comparisons,'wrapper_checks':wrappers,
            'cannot_replace':'Không thay feasibility, full graph/ranking, alpha/depth sensitivity, normal/normal, repeat/permutation của default RE2-TT ở quy mô273metrics.'}
    (OUT/'fixture-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    progress('finish',PC_runs=len(records),wrapper_runs=len(wrappers),permutation_checks=comparisons,
             exception_runs=sum(r['status']=='exception' for r in records))


if __name__=='__main__':main()
