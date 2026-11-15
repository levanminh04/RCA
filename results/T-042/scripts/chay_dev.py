"""T-042 bounded M4 experiments. Only allowlisted dev windows, payload in RAM."""
from dataclasses import asdict
from datetime import datetime, timezone
import argparse
import contextlib
import csv
import io
import json
import math
from pathlib import Path
import sys
import time
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from p3 import nezha
from p3.selector import LoiRunner
from simplerca import Config, diagnose
import psutil
from doi_chieu import read, sha, write, OUT
from kiem_doc_lap import arithmetic, window_audit, rank_metrics

BRANCHES = {'S0': Config(), 'S1': Config(metric_aggregation='channels'),
            'S2': Config(metric_rule='p95'),
            'S3': Config(metric_rule='p95', metric_aggregation='channels')}


def progress(folder, event, **data):
    row = dict(utc=datetime.now(timezone.utc).isoformat(), event=event, **data)
    with (folder/'progress.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(row, ensure_ascii=True, allow_nan=False)+'\n')
    print(json.dumps(row, ensure_ascii=True), flush=True)


def inputs(payload):
    """No case metadata, locator, root, fault or time marker reaches diagnose."""
    t = payload['t_ns']; spans = payload['spans']; logs = payload['logs']
    arrays = payload['metric_arrays']
    mapping = {key: key.rsplit('_', 1)[0] for key in arrays}
    def durations(mask):
        return {str(service): frame['duration'].tolist()
                for service, frame in spans.loc[mask].groupby('serviceName', sort=True)}
    incident = {str(service): frame['message'].tolist()
                for service, frame in logs.loc[logs['_timestamp_ns'] >= t].groupby('container_name', sort=True)}
    observed = set(mapping.values()) | set(spans['serviceName']) | set(logs['container_name'])
    return dict(normal_metrics={k: v['normal'] for k, v in arrays.items()},
                incident_metrics={k: v['anomalous'] for k, v in arrays.items()},
                metric_services=mapping, normal_traces=durations(spans['_start_ns'] < t),
                incident_traces=durations(spans['_start_ns'] >= t), incident_logs=incident,
                observed_services=tuple(sorted(observed)))


def fixtures(folder):
    checks = {}
    def raises(name, fn, cls=ValueError):
        try:
            fn()
        except cls:
            checks[name] = True
        else:
            raise AssertionError(name)
    # Selector must reject before filesystem calls, even with an invalid repo path.
    with patch('p3.nezha.sha256_file', side_effect=AssertionError('data I/O')):
        raises('unknown_case_rejected_before_source_io', lambda: nezha.chon_ca({}, 'dev-0000000000', 'Z:/absent'), LoiRunner)
    checks['timestamp_ns_precision'] = nezha.parse_time_ns('2022-08-22 00:00:00.123456789 +0000 UTC m=+1.0') % 10**9 == 123456789
    raises('bad_timestamp', lambda: nezha.parse_time_ns('invalid'), LoiRunner)
    base = dict(normal_metrics={'a_m':[1.,1.,1.,1.,1.], 'b_m':[0.,0.,0.,0.,0.]},
                incident_metrics={'a_m':[2.,2.,2.,2.,2.], 'b_m':[0.,0.,0.,0.,0.]},
                metric_services={'a_m':'a','b_m':'b'},
                normal_traces={'a':[1.,1.]}, incident_traces={'a':[4.,4.]},
                incident_logs={'a':['error FAIL EXCEPTION'], 'b':[]}, observed_services=('a','b'))
    for branch, config in BRANCHES.items():
        result = diagnose(**base, config=config)
        arithmetic(base, config, result)
        checks[branch+'_known_answer'] = result['scores']['a']['score'] == (7 if config.metric_aggregation=='events' else 3)
    reverse = dict(base)
    for k in ('normal_metrics','incident_metrics','normal_traces','incident_traces','incident_logs'):
        reverse[k] = {key:list(reversed(value)) for key,value in reversed(list(base[k].items()))}
    reverse['metric_services'] = dict(reversed(list(base['metric_services'].items())))
    checks['rows_columns_permuted'] = diagnose(**base) == diagnose(**reverse)
    wrapped = {'locator':'fake-path-one', 'payload':base}
    before = diagnose(**wrapped['payload'])
    wrapped['locator'] = 'different-path-same-content'
    checks['locator_not_in_core_input'] = before == diagnose(**wrapped['payload'])
    zero = dict(normal_metrics={'a_m':[0.,0.]}, incident_metrics={'a_m':[0.,0.]}, metric_services={'a_m':'a'})
    checks['N_equals_A_constant_abstains'] = diagnose(**zero)['status'] == 'abstain'
    missing = dict(normal_metrics={'a_m':[float('nan'),1.]}, incident_metrics={'a_m':[2.]}, metric_services={'a_m':'a'})
    raises('all_channels_unavailable_is_error', lambda: diagnose(**missing))
    partial = dict(base, normal_metrics=dict(base['normal_metrics'], a_m=[1.,1.,float('nan')]))
    checks['NaN_removed_and_counted'] = diagnose(**partial)['metrics']['a_m']['missing_normal'] == 1
    raises('schema_mismatch', lambda: diagnose({}, {'a_m':[1]}, {}))
    raises('empty_case', lambda: diagnose({}, {}, {}))
    raises('negative_duration', lambda: diagnose(**dict(base, normal_traces={'a':[-1.]})))
    raises('invalid_sigma', lambda: Config(sigma=float('nan')))
    tied = diagnose(normal_metrics={'a_m':[0.,0.], 'b_m':[0.,0.]},
                    incident_metrics={'a_m':[1.], 'b_m':[1.]}, metric_services={'a_m':'a','b_m':'b'})
    checks['tie_expected_metric'] = rank_metrics(tied,'a')['hit@1'] == .5

    # Entire synthetic reader fixture, including outside-window invalid content.
    t = 1661127000*10**9; low=t-300*10**9; high=t+300*10**9
    day='2022-08-22'; prefix='data/ngoai-rcaeval/nezha/online-boutique/rca_data/'+day
    texts={}; files={}
    def csv_text(fields, rows):
        s=io.StringIO(); w=csv.DictWriter(s, fieldnames=fields); w.writeheader();w.writerows(rows);return s.getvalue()
    def wall(ns):
        dt=datetime.fromtimestamp(ns//10**9,timezone.utc)
        return dt.strftime('%Y-%m-%d %H:%M:%S')+'.000000000 +0000 UTC m=+1.0'
    for pod in [None]+list(nezha.POD_ALIASES):
        # Only one productcatalog pod belongs to each day's allowlisted inventory.
        if pod == 'productcatalogservice-668d5f85fb-jhwx9':
            continue
        front=pod is None; cols=nezha.FRONT_CHANNELS if front else nezha.RESOURCE_CHANNELS
        idcol='ServiceName' if front else 'PodName'; ident='Frontend' if front else pod
        rows=[dict(Time=wall(low+i*60*10**9), **{idcol:ident}, **{k:i for k in cols}) for i in range(10)]
        rows.append(dict(Time=wall(high), **{idcol:'invalid'}, **{k:'NOT_NUMERIC' for k in cols}))
        rel=prefix+'/metric/'+('front_service.csv' if front else pod+'_metric.csv')
        texts[rel]=csv_text(['Time',idcol]+list(cols),rows)
    pod=next(iter(nezha.POD_ALIASES))
    def span(start,duration,ident):
        return dict(TraceID='trace',SpanID=ident,ParentID='',PodName=pod,OperationName='op',
                    StartTimeUnixNano=start,EndTimeUnixNano=start+duration*1000,Duration=duration)
    row=span(low,1,'at-low')
    trs=[row,row,span(t-1000,2,'cross-t'),span(t,1,'at-t'),span(high-1000,1,'at-high'),span(low-1000,1,'before-low')]
    rel=prefix+'/trace/00_00_trace.csv';texts[rel]=csv_text(list(row),trs)
    def log(ns):
        return dict(TimeUnixNano=ns,Timestamp=datetime.fromtimestamp(ns//10**9,timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')+'.'+str(ns%10**9).zfill(9)+'Z',PodName=pod,Log='text')
    lr=[log(low),log(t-1),log(t),log(high-1),log(high)]
    rel=prefix+'/log/00_00_log.csv';texts[rel]=csv_text(list(lr[0]),lr)
    for rel,text in texts.items():files[rel]=dict(path=rel,absolute_path=rel,bytes=len(text),sha256='0'*64)
    selection=dict(t_ns=t,trace_guard_s=41,files=files)
    with patch('p3.nezha._open_source',side_effect=lambda meta:io.StringIO(texts[meta['path']])):
        payload=nezha.doc_cua_so(selection)
        checks['reader_5N5A_mapping_165'] = len(payload['metric_arrays']) == 165 and len(payload['metric']) == 10
        checks['reader_duplicate_retained'] = len(payload['spans']) == 4 and payload['provenance']['span_duplicate_rows'] == 1
        checks['reader_start_and_end_boundary'] = payload['window']['trace_rows_N_start'] == 3 and payload['window']['trace_rows_N_end'] == 2
        checks['reader_log_half_open_boundary'] = payload['window']['log_rows_N'] == 2 and payload['window']['log_rows_A'] == 2
        checks['reader_ns_us'] = all(payload['spans']['duration']==payload['spans']['_end_ns'].sub(payload['spans']['_start_ns'])//1000)
    assert all(checks.values()), checks
    write(folder/'checks.json',dict(status='PASS',checks=checks,labels_read=False,raw_payload_saved=False))
    progress(folder,'FIXTURES_PASS',checks=len(checks))


def compare_frozen(result, frozen):
    status='NO_EVIDENCE' if result['status']=='abstain' else 'OK'
    assert status == frozen['status']
    assert result['ranks'] == frozen['ranking_native']
    expected=[(r['entity'],r['key'][0]) for r in frozen['entity_ranking']]
    actual=[(s,result['scores'][s]['score']) for s in result['ranks']] if status=='OK' else []
    assert actual == expected
    groups=[]
    for row in frozen['entity_ranking']:
        if not groups or groups[-1][0]!=row['tie_group']:groups.append((row['tie_group'],[]))
        groups[-1][1].append(row['entity'])
    assert [g['services'] for g in result['tie_groups']] == [g[1] for g in groups]
    assert sorted(result['scores']) == sorted(frozen['sets']['observed_entities'])
    return dict(status_scores_native_order_ties_candidates_exact=True)


def execute(folder, pilot=False):
    allow=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json')
    plan=read(OUT/'ke-hoach-chay.json')
    assert set(allow)==set(plan['dev_ids'])
    frozen=read(ROOT/'results/T-026/ban-ghi-dua-vao-cham.json')
    baseline={x['opaque_id']:x for x in frozen['tables']['main']['records'] if x['method']=='simplerca'}
    mapping=read(ROOT/'results/T-026/mappings/ob.json')
    order=sorted(allow,key=lambda k:(sum(x['bytes'] for x in allow[k]['files'].values()),k))
    if pilot:order=order[:1]
    write(folder/'config.json',dict(pilot=pilot,case_order=order,branches={k:asdict(v) for k,v in BRANCHES.items()},
                                   source_code={str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'scripts').glob('*.py'))},
                                   labels_read=False))
    wall=time.perf_counter(); records=[]
    proc=psutil.Process(); peak=proc.memory_info().rss
    for index,oid in enumerate(order):
        if not pilot:
            pilot_folder=OUT/'runs/pilot-001'
            cached=pilot_folder/(oid+'-list.json')
            if cached.is_file():
                values=read(cached)
                for row in values:
                    assert sha(ROOT/row['path']) == row['sha256']
                records.extend(values)
                progress(folder,'REUSE_VERIFIED_PILOT',opaque_id=oid)
                continue
        start=time.perf_counter();progress(folder,'CASE_START',opaque_id=oid,index=index+1,total=len(order))
        selection=nezha.chon_ca(allow,oid,ROOT)
        payload=nezha.doc_cua_so(selection)
        read_s=time.perf_counter()-start
        audit=window_audit(selection,payload,mapping)
        write(folder/(oid+'-input-audit.json'),audit)
        method_inputs=inputs(payload)
        input_ready=time.perf_counter()
        results={}
        for branch,config in BRANCHES.items():
            started=time.perf_counter()
            result=diagnose(**method_inputs,config=config)
            checks=arithmetic(method_inputs,config,result)
            if branch=='S0':checks.update(compare_frozen(result,read(ROOT/baseline[oid]['path'])))
            results[branch]=result
            dest=folder/(oid+'-'+branch+'.json')
            write(dest,dict(opaque_id=oid,branch=branch,diagnosis=result,checks=checks,
                            window=payload['window'],input_audit=str((folder/(oid+'-input-audit.json')).relative_to(ROOT)).replace('\\','/'),
                            input_sha256={k:v['sha256'] for k,v in selection['files'].items()},
                            method_s=time.perf_counter()-started,labels_read=False,raw_payload_saved=False))
            records.append(dict(opaque_id=oid,branch=branch,path=dest.relative_to(ROOT).as_posix(),sha256=sha(dest)))
            progress(folder,'BRANCH_DONE',opaque_id=oid,branch=branch)
        assert all(results[x]['traces']==results['S0']['traces'] and results[x]['logs']==results['S0']['logs'] for x in results)
        peak=max(peak,proc.memory_info().rss)
        if pilot:
            # Independent normal-normal domains, chosen without labels or outputs.
            # Native metric sources use their own ordinal N observations (Q-85).
            n_spans=payload['spans'].loc[payload['spans']['_start_ns']<payload['t_ns']]
            n_logs=payload['logs'].loc[payload['logs']['_timestamp_ns']<payload['t_ns']]
            control=dict(method_inputs)
            control['normal_metrics']={k:v[:2] for k,v in method_inputs['normal_metrics'].items()}
            control['incident_metrics']={k:v[2:] for k,v in method_inputs['normal_metrics'].items()}
            if len(n_spans):
                cut=(int(n_spans['_start_ns'].min())+int(n_spans['_start_ns'].max()))//2
                control['normal_traces']={str(s):f['duration'].tolist() for s,f in n_spans.loc[n_spans['_start_ns']<cut].groupby('serviceName')}
                control['incident_traces']={str(s):f['duration'].tolist() for s,f in n_spans.loc[n_spans['_start_ns']>=cut].groupby('serviceName')}
                control['incident_logs']={str(s):f['message'].tolist() for s,f in n_logs.loc[n_logs['_timestamp_ns']>=cut].groupby('container_name')}
                null=diagnose(**control)
                arithmetic(control,Config(),null)
                write(folder/'normal-control.json',dict(kind='disjoint normal-normal; metric ordinal 2 vs 3, trace/log temporal midpoint',
                                                      trace_log_cut_ns=cut,diagnosis=null,
                                                      interpretation='not proof of a physically clean baseline; short and asynchronous modalities',labels_read=False))
            else:
                write(folder/'normal-control.json',dict(status='NOT_AVAILABLE',reason='no normal trace interval',labels_read=False))
            # Permutation on actual input: diagnosis invariant keys/counts, float thresholds close.
            changed=dict(method_inputs)
            for key in ['normal_metrics','incident_metrics','normal_traces','incident_traces','incident_logs']:
                changed[key]={k:list(reversed(v)) for k,v in reversed(list(method_inputs[key].items()))}
            changed['metric_services']=dict(reversed(list(method_inputs['metric_services'].items())))
            perm=diagnose(**changed)
            assert perm['scores']==results['S0']['scores'] and perm['ranks']==results['S0']['ranks'] and perm['tie_groups']==results['S0']['tie_groups']
            assert all(perm['metrics'][k]['count']==v['count'] for k,v in results['S0']['metrics'].items())
            write(folder/'permutation.json',dict(status='PASS',scores_ranks_groups_counts_exact=True,
                                               thresholds='floating point reduction may differ; independent audit verifies counts',labels_read=False))
            write(folder/(oid+'-list.json'),records)
        progress(folder,'CASE_DONE',opaque_id=oid,wall_s=time.perf_counter()-start,
                 read_s=read_s,input_and_audit_s=input_ready-start,peak_rss_mb=peak/2**20)
        if time.perf_counter()-wall>3600:
            raise RuntimeError('single-run budget reached')
        del payload,method_inputs,results
    cost=dict(wall_s=time.perf_counter()-wall,peak_sampled_rss_mb=peak/2**20,
              peak_measurement='sampled at case boundaries; may miss transient peak',records=len(records),
              projected_22_case_s=(time.perf_counter()-wall)*22 if pilot else None)
    write(folder/'cost.json',cost)
    write(folder/'diagnosis-list.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),records=records,
                                          labels_read=False,completed=True))
    progress(folder,'DIAGNOSES_FROZEN',**cost)


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['fixtures','pilot','full']);p.add_argument('run_id');a=p.parse_args()
    folder=OUT/'runs'/a.run_id
    folder.mkdir(parents=True,exist_ok=False)
    write(folder/'invocation.json',dict(argv=sys.argv,python=sys.executable,utc=datetime.now(timezone.utc).isoformat()))
    class Tee:
        def __init__(self, log, terminal):self.log,self.terminal=log,terminal
        def write(self,text):self.log.write(text);self.terminal.write(text)
        def flush(self):self.log.flush();self.terminal.flush()
    with (folder/'stdout.txt').open('w',encoding='utf-8') as stdout, (folder/'stderr.txt').open('w',encoding='utf-8') as stderr:
        with contextlib.redirect_stdout(Tee(stdout,sys.stdout)),contextlib.redirect_stderr(stderr):
            try:
                if a.stage=='fixtures':fixtures(folder)
                else:execute(folder,a.stage=='pilot')
            except BaseException as exc:
                progress(folder,'FAILED',error=type(exc).__name__+': '+str(exc))
                traceback.print_exc()
                sys.exit(1)


if __name__=='__main__':main()
