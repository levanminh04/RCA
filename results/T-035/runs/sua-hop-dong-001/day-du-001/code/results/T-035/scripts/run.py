"""Runner đọc dev theo p3; bộ dựng chỉ nhận span/interval/alias/universe."""
import argparse,hashlib,json,os,sys,time,threading,traceback,platform,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
# Dùng numpy/pandas của py312-pin; chỉ lấy reader Parquet đã có ở môi trường T-014.
try:import pyarrow
except ImportError:
    sys.path.append('D:/RCA-ext/envs/T-014-main/Lib/site-packages')
    import pyarrow
import psutil
from p3 import selector,nezha,nhan
from do_thi import Prepared,project,from_p3
from do_thi.builder import edge_key
from circa_kien_truc.builder import service_calls
from do_thi.nezha_node import read_node

OUT=ROOT/'results/T-035'
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,sort_keys=True,indent=1,allow_nan=False)
def sha(p):return selector.sha256_file(p)
def shape(g):
    return {'nodes':sorted(n['id'] for n in g['nodes']),
            'edges':sorted(['' if x is None else x for x in edge_key(e)] for e in g['edges'])}
def fingerprint(g):return hashlib.sha256(json.dumps(shape(g),ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def load(dataset,oid):
    if dataset=='RE2-TT':
        allow=selector.nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
        files=selector.chon_ca(allow,oid,ROOT,tep=['traces.parquet'])
        s=pd.read_parquet(files['traces.parquet'])
        t=nhan.nap_moc(ROOT/'results/T-022/nhan-dev.json')[oid]*nezha.NS
        universe=read(ROOT/'results/T-022/mappings/universe-re2tt-dev.json')['U']
        return s,t,{},universe,{'file_hash':sha(files['traces.parquet']),'domain':'whole_dev_trace_table','source_columns':list(s.columns)},None
    allow=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json')
    selected=nezha.chon_ca(allow,oid,ROOT)
    payload=nezha.doc_cua_so(selected)
    provenance={'domain':'authorized_dev_window_only','window':payload['window'],'provenance':payload['provenance'],
                'source_columns':list(payload['spans'].columns)}
    node=read_node(selected)
    return payload['spans'],selected['t_ns'],{},selected['universe'],provenance,node

def case(dataset,oid,run,event):
    started=time.perf_counter();rss=[];done=threading.Event()
    def monitor():
        while not done.wait(.2):rss.append(psutil.Process().memory_info().rss)
    thread=threading.Thread(target=monitor,daemon=True);thread.start()
    steps={};s=time.perf_counter()
    try:
        frame,t,alias,universe,provenance,node=load(dataset,oid);steps['read_and_hash_s']=time.perf_counter()-s
        event('read_done',dataset=dataset,opaque_id=oid,rows=len(frame),seconds=steps['read_and_hash_s'])
        s=time.perf_counter();prepared=Prepared(from_p3(frame),alias,universe);steps['prepare_s']=time.perf_counter()-s
        windows={'full':None,'N':[t-300*nezha.NS,t],'A':[t,t+300*nezha.NS]}
        if dataset=='RE2-TT':
            lo=int(prepared.start.min());hi=int(prepared.end.max())+1
            for seconds in [60,300]:
                step=seconds*nezha.NS
                for k,start in enumerate(range(lo,hi,step)):windows[f's{seconds}-{k:03d}']=[start,start+step]
        records={};checks=[];graphs={};vocabulary={};s=time.perf_counter()
        for name,interval in windows.items():
            event('window_start',dataset=dataset,opaque_id=oid,window=name)
            wstart=time.perf_counter();e,o=prepared.graph(interval);e2,o2=prepared.graph(interval)
            assert e==e2 and o==o2,'non_deterministic'
            n,edges=project(o)
            assert n=={z['id'] for z in e['nodes']},'projection_nodes'
            assert edges=={edge_key(z) for z in e['edges']},'projection_edges'
            masked=frame.loc[prepared.mask(interval)] if len(frame)==len(prepared.f) else prepared.f.loc[prepared.mask(interval)]
            cutoff=int(prepared.start.max())//nezha.NS+1 if len(prepared.start) else 0
            independent,rep=service_calls(masked,cutoff)
            actual={(q['source'],q['target']) for q in e['edges'] if q['type'] in ('gọi-chưa-phân-kiểu','gọi-đồng-bộ')}
            assert actual==set(independent.edges),'K4'
            dest=run/'do-thi'/dataset/oid
            write(dest/'thuc-the'/f'{name}.json',e)
            if name in ('full','N','A'):
                write(dest/'thao-tac'/f'{name}.json',o)
                vocabulary[name]=prepared.vocabulary(interval)
            records[name]={'entity_nodes':len(e['nodes']),'entity_edges':len(e['edges']),
                           'operation_nodes':len(o['nodes']),'operation_edges':len(o['edges']),
                           'entity_fingerprint':fingerprint(e),'operation_fingerprint':fingerprint(o),
                           'stats':e['stats'],'coverage':e['coverage'],'outside_inventory':e['outside_inventory'],
                           'seconds':time.perf_counter()-wstart}
            checks.append({'window':name,'K1':e['stats']['roots']+e['stats']['resolved_parents']+e['stats']['orphans']==e['stats']['unique_spans'],
                           'K2_repeat':True,'K4':True,'K5':True,'independent':rep})
            if name in ('full','N','A'):graphs[name]=e
            event('window_complete',dataset=dataset,opaque_id=oid,window=name,seconds=time.perf_counter()-wstart)
        steps['graphs_checks_vocabulary_s']=time.perf_counter()-s
        full=graphs['full'];s=time.perf_counter()
        # Hai trace có cha-con, chọn bằng ID và độ lớn, không root/fault. Ưu tiên chứng cứ mất cha.
        lost=(prepared.parent<0)&~prepared.roots
        ids=prepared.f.traceID.unique()
        missing_ids=sorted(set(prepared.f.loc[lost,'traceID']))
        chosen=missing_ids[:1]
        chosen+=list(sorted(set(ids)-set(chosen)))[:2-len(chosen)]
        manual=[]
        for trace in chosen:
            f=prepared.f.loc[prepared.f.traceID==trace]
            # Chỉ witness của hai trace, không lưu lại toàn bộ bảng span.
            witness=f.head(12)[['traceID','spanID','parentSpanID','serviceName','operationName','startTime','duration']].to_dict('records')
            manual.append({'traceID':trace,'trace_span_count':len(f),'first_rows':witness})
        outcome={'dataset':dataset,'opaque_id':oid,'provenance':provenance,'windows':records,
                 'checks':checks,'vocabulary':vocabulary,'node':node,'manual_trace_witness':manual,
                 'edges_N_only':sorted([q['source'],q['target']] for q in graphs['N']['edges'] if [q['source'],q['target']] not in [[r['source'],r['target']] for r in graphs['A']['edges']]),
                 'edges_A_only':sorted([q['source'],q['target']] for q in graphs['A']['edges'] if [q['source'],q['target']] not in [[r['source'],r['target']] for r in graphs['N']['edges']]),
                 'full_call_events':[{'source':q['source'],'target':q['target'],'count':q['event_count']} for q in full['edges']],
                 'steps_s':steps,'seconds':time.perf_counter()-started}
        done.set();thread.join();outcome['peak_rss_bytes']=max(rss or [psutil.Process().memory_info().rss])
        write(run/'cases'/dataset/f'{oid}.json',outcome)
        event('case_complete',dataset=dataset,opaque_id=oid,seconds=outcome['seconds'],peak_rss_bytes=outcome['peak_rss_bytes'])
        return outcome
    finally:done.set();thread.join()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('run');parser.add_argument('--pilot',action='store_true');parser.add_argument('--reuse');parser.add_argument('--only',nargs=2)
    args=parser.parse_args();run=OUT/'runs'/args.run;run.mkdir(parents=True,exist_ok=False)
    for p in [*sorted((ROOT/'src/do_thi').glob('*.py')),Path(__file__)]:
        dest=run/'code'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    def event(stage,**values):
        x={'utc':datetime.now(timezone.utc).isoformat(),'stage':stage,**values}
        with (run/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(x,ensure_ascii=False)+'\n')
        print(json.dumps(x,ensure_ascii=False),flush=True)
    baseline=read(OUT/'runs/buoc0-001/input-verification.json')['governing_hashes']
    for name,h in baseline.items():
        assert sha(ROOT/name)==h,'governing_hash_changed'
    re2=selector.nap_allowlist(ROOT/'results/T-022/allowlist-dev.json');ob=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json')
    jobs=[('RE2-TT',oid) for oid in sorted(re2)]+[('Nezha-OB',oid) for oid in sorted(ob)]
    if args.pilot:
        jobs=[('RE2-TT',max(re2,key=lambda k:re2[k]['files']['traces.parquet']['bytes'])),
              ('Nezha-OB',max(ob,key=lambda k:sum(v['bytes'] for v in ob[k]['files'].values())))]
    if args.only:jobs=[tuple(args.only)]
    write(run/'environment.json',{'python':sys.version,'executable':sys.executable,'numpy':np.__version__,'pandas':pd.__version__,
                                'pyarrow':pyarrow.__version__,'numpy_origin':np.__file__,'pandas_origin':pd.__file__,
                                'pyarrow_origin':pyarrow.__file__,'hashseed':os.environ.get('PYTHONHASHSEED'),'platform':platform.platform(),
                                'command':sys.argv,'governing_hashes':{p:sha(ROOT/p) for p in ['AGENTS.md','tasks/T-035-p5-do-thi-tu-trace/SPEC.md']}})
    results=[];start=time.perf_counter();reuse={}
    if args.reuse:
        old=read(OUT/'runs'/args.reuse/'summary.json')
        assert old['status']=='PASS'
        for c in old['cases']:reuse[(c['dataset'],c['opaque_id'])]=c
    try:
        for dataset,oid in jobs:
            for name,h in baseline.items():assert sha(ROOT/name)==h,'governing_hash_changed'
            if (dataset,oid) in reuse:
                c=reuse[(dataset,oid)];results.append(c);event('reused',dataset=dataset,opaque_id=oid,source_run=args.reuse)
                continue
            event('case_start',dataset=dataset,opaque_id=oid);results.append(case(dataset,oid,run,event))
        write(run/'summary.json',{'status':'PASS','cases':results,'seconds':time.perf_counter()-start,
                                  'projected_full_seconds':None if not args.pilot else sum(c['seconds']*(30 if c['dataset']=='RE2-TT' else 22) for c in results)})
    except Exception as exc:
        write(run/'failure.json',{'error':repr(exc),'traceback':traceback.format_exc(),'completed':[c['opaque_id'] for c in results]})
        event('failed',error=repr(exc));raise

if __name__=='__main__':main()
