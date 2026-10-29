"""Q-190 internal diagnostics; unchanged upstream functions loaded by AST in RAM."""
import argparse
import ast
import contextlib
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys
import time
import traceback
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import psutil

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT/'results/T-042/runs/continuation-001'
SOURCE = Path('D:/RCA-ext/work/T-017/sources-audit')
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-042/scripts')]
from p3 import nezha
from simplerca import Config, diagnose
from chay_dev import inputs
from kiem_doc_lap import arithmetic


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def plain(value):
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, np.generic):
        return plain(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return {'nonfinite': str(value)}
    return value


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(plain(value), stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def event(folder, name, **values):
    row = dict(utc=datetime.now(timezone.utc).isoformat(), event=name, **values)
    with (folder/'progress.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(row)+'\n')
    print(json.dumps(row), flush=True)


def load_kernels():
    pins = {x['file']: x for x in read(ROOT/'results/T-017/sources/download-manifest.json')}
    records = []
    namespaces = []
    for rel, only in [('github/orig/src/simplerca/main.py', None),
                      ('github/orig/src/simplerca/adapter.py', ['calculate_network_latency']),
                      ('github/orig/src/simplerca/nezha_rca.py', None)]:
        path = SOURCE/rel
        assert sha(path) == pins[rel]['sha256']
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and (only is None or n.name in only)]
        assert all(not n.decorator_list for n in functions)
        ns = dict(np=np, pd=pd, re=re, Dict=Dict, List=List, Optional=Optional, Tuple=Tuple)
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), ns)
        records.append(dict(path=str(path), sha256=sha(path), functions=[dict(name=n.name, line=n.lineno, end=n.end_lineno,
                       ast_sha256=hashlib.sha256(ast.dump(n, include_attributes=False).encode()).hexdigest()) for n in functions]))
        namespaces.append(ns)
    return namespaces, records


def extract_message(raw):
    # Exact make_nezha._extract_log_message behavior, independent of severity.
    try:
        return json.loads(raw)['log']
    except (json.JSONDecodeError, KeyError, TypeError):
        return raw


def dataframes(payload, network):
    t = payload['t_ns']
    long_rows = []
    wide = {}
    wanted = {'CpuUsageRate(%)', 'MemoryUsageRate(%)', 'PodClientLatencyP90(s)',
              'PodServerLatencyP90(s)', 'PodClientLatencyP99(s)', 'PodServerLatencyP99(s)'}
    for key, arrays in payload['metric_arrays'].items():
        meta = payload['provenance']['channels'][key]
        if meta['source_column'] not in nezha.RESOURCE_CHANNELS:
            continue
        service = key.rsplit('_', 1)[0]
        vals = np.concatenate([arrays['normal'], arrays['anomalous']])
        stamps = meta['timestamps_ns']
        assert len(vals) == len(stamps) == 10
        for index, (stamp, value) in enumerate(zip(stamps, vals)):
            part = 'N' if stamp < t else 'A'
            # Only within-pod wide pivot; no synthetic shared time across pods.
            row = wide.setdefault((part, service, index), dict(service_name=service, time=int(stamp)))
            assert row['time'] == int(stamp)
            row[meta['source_column']] = float(value)
            if meta['source_column'] in wanted:
                long_rows.append(dict(service_name=service, time=int(stamp), metric=meta['source_column'], value=float(value)))
    long = pd.DataFrame(long_rows)
    metrics = {p: network(long.loc[(long.time < t) if p == 'N' else (long.time >= t)].copy()) for p in ['N', 'A']}
    wides = {p: pd.DataFrame([v for (part, _, _), v in wide.items() if part == p]) for p in ['N', 'A']}
    logs = payload['logs'].rename(columns={'container_name': 'service_name', '_timestamp_ns': 'time'})[['service_name', 'time', 'message']].copy()
    logs['message'] = logs.message.map(extract_message)
    logsides = {p: logs.loc[(logs.time < t) if p == 'N' else (logs.time >= t)].copy() for p in ['N', 'A']}
    traces = payload['spans'].rename(columns={'serviceName':'service_name', 'spanID':'span_id', 'parentSpanID':'parent_span_id'})
    traces = traces[['service_name', 'span_id', 'parent_span_id', 'duration', '_start_ns', '_end_ns']].copy()
    traceparts = {p: traces.loc[(traces._start_ns < t) if p == 'N' else (traces._start_ns >= t)].copy() for p in ['N', 'A']}
    return metrics, wides, logsides, traceparts


def independent_main(ns, ms, ls, ts, source_result):
    """Audit all score components independently, including intentional native pooling."""
    pattern = re.compile('error|fail|exception|timeout|refused', re.I)
    duration = {p: ns['get_time_window_minutes'](ls[p]) for p in ['N','A']}
    lc = {}
    all_log = set(ls['N'].service_name) | set(ls['A'].service_name)
    for service in sorted(all_log):
        a = ls['A'].loc[ls['A'].service_name == service]
        n = ls['N'].loc[ls['N'].service_name == service]
        ae = sum(bool(pattern.search(str(v))) for v in a.message)
        ne = sum(bool(pattern.search(str(v))) for v in n.message)
        score = None
        if len(a):
            if not len(n):
                score = ae*10
            else:
                ar, nr = ae/duration['A'], ne/duration['N']
                score = 100 if nr == 0 and ar > 0 else (ar/nr*50 if nr > 0 else 0)
                ratio = (len(a)/duration['A'])/(len(n)/duration['N'])
                score += max(0, 1-ratio)*30
        lc[service] = dict(N=len(n), A=len(a), error_N=ne, error_A=ae, score=score)
    mc = {}
    for service in ms['A'].service_name.unique():
        a = ms['A'].loc[ms['A'].service_name == service]
        n = ms['N'].loc[ms['N'].service_name == service]
        details = []
        score = 0
        for name, weight in [('Cpu|CPU',100), ('Network_Latency',50), ('Latency',20)]:
            if name == 'Network_Latency':
                av = a.loc[a.metric == name, 'value'].dropna()
                nv = n.loc[n.metric == name, 'value'].dropna()
            else:
                av = a.loc[a.metric.str.contains(name, case=False) & ((a.metric != 'Network_Latency') if name == 'Latency' else True), 'value'].dropna()
                nv = n.loc[n.metric.str.contains(name, case=False), 'value'].dropna()
            if not len(av):
                continue
            vals = nv if len(nv)>1 else av
            mean = float(np.mean(vals))
            threshold = mean+6*float(np.std(vals, ddof=1)) if len(vals)>1 else float(max(vals))
            count = int(sum(av > threshold))
            score += count*weight
            details.append(dict(pattern=name, normal_count=len(nv), incident_count=len(av),
                                fallback_to_incident=len(nv)<2, mean=mean, threshold=threshold, alerts=count, weight=weight,
                                normal_metric_names=sorted(n.loc[n.metric.str.contains(name, case=False),'metric'].unique())))
        mc[service] = dict(score=score, pools=details)
    tc = {}
    for service in ts['A'].service_name.unique():
        vals = ts['A'].loc[ts['A'].service_name == service, 'duration'].dropna().to_numpy()/1000
        p90 = 10 if 'front' in service.lower() else float(np.percentile(vals,90)) if len(vals)>2 else 1
        tc[service] = dict(A=len(vals), p90_us=p90, score=p90 if p90>100 else 0)
    captured = source_result['components']
    for service, score in captured['log'].items():
        assert math.isclose(score, lc[service]['score'], rel_tol=1e-12, abs_tol=1e-9)
    for name, audit in [('metric',mc),('trace',tc)]:
        for service, score in captured[name].items():
            assert math.isclose(score, audit[service]['score'], rel_tol=1e-12, abs_tol=1e-9), (name, service)
    fusion = {}
    for service, value in source_result['scores'].items():
        m = mc.get(service,{}).get('score',0); tr = tc.get(service,{}).get('score',0)
        log = lc.get(service,{}).get('score',0) or 0
        branch = 'metric_ge100' if m>=100 else 'metric_positive' if m>0 else 'trace_positive' if tr>0 else 'log_only'
        expected = m+.3*log if m>=100 else m+.5*log if m>0 else tr+.7*log if tr>0 else log
        assert math.isclose(expected, value, rel_tol=1e-12, abs_tol=1e-9)
        fusion[service] = dict(branch=branch,metric=m,trace=tr,log=log,score=value,trace_ignored=bool(m>0 and tr>0))
    return dict(status='PASS', log_duration_minutes=duration, logs=lc, metrics=mc, traces=tc, fusion=fusion)


def run_main(ns, ms, ls, ts):
    capture = {}
    code = ns['simplerca'].__code__
    def profiler(frame, event_name, result):
        if event_name == 'return' and frame.f_code is code:
            capture.update(scores=dict(frame.f_locals['combined_scores']),
                           components={n:dict(frame.f_locals[n+'_scores']) for n in ['log','trace','metric']})
    old = sys.getprofile()
    try:
        sys.setprofile(profiler)
        native = ns['simplerca']([ls['A'],ms['A'],ts['A']],[ls['N'],ms['N'],ts['N']])
    finally:
        sys.setprofile(old)
    capture['native_ranks'] = native['ranks']
    capture['tie_groups'] = tie_groups(capture['scores'])
    assert set(capture['scores']) == set(native['ranks'])
    capture['independent'] = independent_main(ns,ms,ls,ts,capture)
    return capture


def tie_groups(scores):
    groups=[]
    for service in sorted(scores, key=lambda s:(-scores[s],s)):
        if not groups or groups[-1]['score'] != scores[service]:
            groups.append(dict(score=scores[service],services=[]))
        groups[-1]['services'].append(service)
    return groups


def partial_nezha(ns, wides, traces):
    m = ns['_detect_metric_anomalies'](wides['N'], wides['A'])
    t = ns['_detect_trace_anomalies'](traces['N'], traces['A'])
    ranks = ns['_vote_combine_results'](m,t,[])
    scores = {}
    for result, weight in [(m,1.2),(t,1.)]:
        for i, service in enumerate(result[:5]):
            scores[service] = scores.get(service,0)+(5-i)*weight
    expected = sorted(scores,key=lambda x:-scores[x])[:5]
    assert ranks == expected
    return dict(scope='PARTIAL metric+trace; severity unavailable; NOT full author pipeline',metric_ranks=m,trace_ranks=t,
                native_ranks=ranks,scores=scores,tie_groups=tie_groups(scores),
                trace_p90_ms={str(s):float(ns['_get_latency_metric'](traces['A'],s)) for s in traces['A'].service_name.unique()},
                independent_borda='PASS')


def fixtures(folder, kernels):
    ns, network, nz = kernels
    checks = {}
    empty = pd.DataFrame(columns=['service_name','message','time'])
    log = pd.DataFrame(dict(service_name=['a'],message=['ERROR'],time=[0]))
    try:
        nz['_detect_log_anomalies'](log,log)
    except KeyError as exc:
        checks['missing_level_native_failure'] = str(exc) == "'level'"
    else:
        checks['missing_level_native_failure'] = False
    sample = pd.DataFrame(dict(service_name=['a']*3,duration=[200000]*3))
    checks['literal_us_interpreted_as_ns'] = ns['analyze_traces'](sample)['a'] == 200
    sample.duration *= 1000
    checks['physical_ns_factor1000'] = ns['analyze_traces'](sample)['a'] == 200000
    scores = [ns['combine_scores']({'a':20},{'a':100000},{'a':m},['a'])['a'] for m in [0,20,100]]
    checks['fusion_nonmonotone_known_answer'] = scores == [100014,30,106]
    frame = pd.DataFrame(dict(service_name=['a']*4,time=[0,0,1,1],metric=['PodClientLatencyP99(s)','PodServerLatencyP99(s)']*2,value=[9,3,4,7]))
    got = network['calculate_network_latency'](frame)
    checks['network_same_source_timestamp'] = got.loc[got.metric=='Network_Latency','value'].tolist() == [6,3]
    logclock = pd.DataFrame(dict(timestamp=pd.to_datetime([0,300*10**9]),time=[0,300*10**9]))
    checks['time_without_timestamp_fallback'] = ns['get_time_window_minutes'](logclock.drop(columns='timestamp')) == 1
    checks['datetime_duration_5min'] = ns['get_time_window_minutes'](logclock) == 5
    checks['integer_timestamp_fallback'] = ns['get_time_window_minutes'](pd.DataFrame(dict(timestamp=[0,300*10**9]))) == 1
    checks['log_message_extraction'] = extract_message('{"log":"error"}') == 'error' and extract_message('raw') == 'raw'
    checks['dataset_fault_not_used'] = all(not any(isinstance(x,ast.Name) and isinstance(x.ctx,ast.Load) and x.id in {'dataset','fault_type'} for x in ast.walk(n)) for n in ast.parse((SOURCE/'github/orig/src/simplerca/main.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='simplerca')
    assert all(checks.values()), checks
    write(folder/'checks.json',dict(status='PASS',checks=checks,fusion_toy=scores,labels_read=False))


def execute(folder, kernels, pilot):
    ns, network, nz = kernels
    allow = nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json')
    order = sorted(allow, key=lambda k:(sum(v['bytes'] for v in allow[k]['files'].values()),k))
    if pilot: order=order[:1]
    write(folder/'config.json',dict(case_order=order,branches=['M0','M1','M2','N0-partial','N1-partial','M4-no-log'],
        window='P3 5N5A start split; source-native metrics; raw source timestamps',labels_read=False,script_sha256=sha(__file__)))
    start=time.perf_counter();records=[];peak=0
    for oid in order:
        pilotlist=OUT/'simple-pilot-001'/f'{oid}-list.json'
        if not pilot and pilotlist.exists():
            cached=read(pilotlist)
            for row in cached: assert sha(ROOT/row['path'])==row['sha256']
            records.extend(cached);event(folder,'REUSE_PILOT',opaque_id=oid);continue
        now=time.perf_counter();event(folder,'CASE_START',opaque_id=oid)
        selection=nezha.chon_ca(allow,oid,ROOT)
        payload=nezha.doc_cua_so(selection)
        ms,wides,logs,traces=dataframes(payload,network['calculate_network_latency'])
        write(folder/f'{oid}-input-audit.json',dict(window=payload['window'],sources={k:v['sha256'] for k,v in selection['files'].items()},
            long_rows={p:len(ms[p]) for p in ms},wide_rows={p:len(wides[p]) for p in wides},
            logs={p:len(logs[p]) for p in logs},traces={p:len(traces[p]) for p in traces},
            metric_names=sorted(ms['A'].metric.unique()),log_level_present=False,
            duration_physical_check=bool(((payload['spans']._end_ns-payload['spans']._start_ns)//1000==payload['spans'].duration).all()),labels_read=False))
        case=[]
        for branch in ['M0','M1','M2','N0-partial','N1-partial','M4-no-log']:
            method_start=time.perf_counter()
            if branch=='M4-no-log':
                kwargs=inputs(payload);kwargs['incident_logs']={}
                result=diagnose(**kwargs,config=Config());arithmetic(kwargs,Config(),result)
                result=dict(scores={s:v['score'] for s,v in result['scores'].items()},native_ranks=result['ranks'],tie_groups=result['tie_groups'],independent='PASS',scope='matched M4 without logs')
            else:
                ts={p:f.copy() for p,f in traces.items()}
                if branch in ['M1','M2','N1-partial']:
                    for frame in ts.values(): frame['duration'] *= 1000
                ls={p:f.copy() for p,f in logs.items()}
                if branch=='M2':
                    for frame in ls.values(): frame['timestamp']=pd.to_datetime(frame.time,unit='ns',utc=True)
                result=run_main(ns,ms,ls,ts) if branch.startswith('M') else partial_nezha(nz,wides,ts)
            dest=folder/f'{oid}-{branch}.json'
            write(dest,dict(opaque_id=oid,branch=branch,result=result,method_s=time.perf_counter()-method_start,labels_read=False,raw_payload_saved=False))
            row=dict(opaque_id=oid,branch=branch,path=dest.relative_to(ROOT).as_posix(),sha256=sha(dest))
            records.append(row);case.append(row)
        peak=max(peak,psutil.Process().memory_info().rss)
        if pilot:
            write(folder/f'{oid}-list.json',case)
        event(folder,'CASE_DONE',opaque_id=oid,wall_s=time.perf_counter()-now)
        if time.perf_counter()-start>3600:raise RuntimeError('run budget')
    write(folder/'diagnoses-frozen.json',dict(records=records,completed=True,labels_read=False,utc=datetime.now(timezone.utc).isoformat()))
    write(folder/'cost.json',dict(wall_s=time.perf_counter()-start,peak_sampled_rss_mb=peak/2**20,records=len(records)))
    event(folder,'FROZEN',records=len(records))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['fixtures','pilot','full']);parser.add_argument('run_id')
    args=parser.parse_args();folder=OUT/args.run_id;folder.mkdir(exist_ok=False)
    write(folder/'invocation.json',dict(argv=sys.argv,python=sys.executable,utc=datetime.now(timezone.utc).isoformat()))
    with (folder/'stdout.txt').open('x',encoding='utf-8') as stdout,(folder/'stderr.txt').open('x',encoding='utf-8') as stderr:
        class Tee:
            def write(self,s): stdout.write(s);sys.__stdout__.write(s)
            def flush(self): stdout.flush();sys.__stdout__.flush()
        with contextlib.redirect_stdout(Tee()),contextlib.redirect_stderr(stderr):
            try:
                kernels,pins=load_kernels();write(folder/'source-pins.json',pins)
                if args.stage=='fixtures': fixtures(folder,kernels)
                else:execute(folder,kernels,args.stage=='pilot')
            except BaseException as exc:
                event(folder,'FAILED',error=type(exc).__name__+': '+str(exc));traceback.print_exc();raise


if __name__=='__main__':
    main()
