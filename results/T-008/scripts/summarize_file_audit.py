"""Derive Nezha evidence and limitations from saved whole-file audit."""
import argparse,collections,datetime as dt,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=ROOT/'results/T-008';parser=argparse.ArgumentParser();parser.add_argument('--run',required=True);args=parser.parse_args();OUT=R/'runs'/args.run;OUT.mkdir(exist_ok=False)
audit=json.loads((R/'runs/file-audit-001/summary.json').read_text());labels=json.loads((R/'runs/run-001/labels.json').read_text());download=json.loads((R/'runs/download-001/manifest.json').read_text());symptoms=json.loads((R/'runs/symptoms-003/result.json').read_text())
hashes={x['path']:x['sha256'] for x in download['items']};same=[p for p,h in hashes.items() if '/construct_data/' in p and hashes.get(p.replace('/construct_data/','/rca_data/'))==h]
summaries={};cases=[]
for dataset,system in [('OB','online-boutique'),('TT','train-ticket')]:
    rows=[r for r in audit['results'] if r['path'].startswith(system+'/')];trace=[r for r in rows if '/trace/' in r['path']];metric=[r for r in rows if r.get('numeric')];parent=collections.Counter();join=collections.Counter();offsets=collections.Counter()
    for r in trace:parent.update(r['parent']);join.update(r['paired_log'])
    for r in metric:offsets.update(r['timestamp_minus_time_text_seconds'])
    denominator=sum(v for k,v in parent.items() if k!='root_sentinel')
    summaries[dataset]=dict(files=len(rows),bytes=sum(r['bytes'] for r in rows),rows=sum(r['rows'] for r in rows),trace_files=len(trace),metric_files=len(metric),span_parent=dict(parent),nonroot_denominator=denominator,unique_parent_fraction=parent['unique_resolved_within_file']/denominator if denominator else None,log_join=dict(join),metric_timestamp_minus_text_seconds=dict(offsets),duplicate_span_keys=sum(r.get('duplicate_span_keys',0) for r in trace),normal_trace_windows=[dict(path=r['path'],start=r['start_epoch'],end=r['end_epoch'],rows=r['rows']) for r in trace if '/construct_data/' in r['path']])
    for l in [x for x in labels if x['dataset']==dataset]:
        for clock in ['text_as_utc','epoch']:
            t=dt.datetime.fromisoformat(l['inject_time_raw']).replace(tzinfo=dt.timezone.utc).timestamp() if clock=='text_as_utc' else float(l['inject_timestamp_raw'])
            windows=[r for r in trace if r['path'].startswith(system+'/rca_data/'+l['date']+'/trace/') and r.get('start_epoch') is not None and r['end_epoch']>=t-60 and r['start_epoch']<=t+60]
            incoming=set();outgoing=set();present=False
            for r in windows:
                present=present or l['service'] in r['services']
                for e in r['edges']:
                    if e['parent']==l['service']:outgoing.add(e['child'])
                    if e['child']==l['service']:incoming.add(e['parent'])
            cases.append(dict(dataset=dataset,date=l['date'],root=l['service'],fault=l['fault'],inject_time=l['inject_time_raw'],clock_interpretation=clock,window_paths=[r['path'] for r in windows],root_present=present,in_neighbors=sorted(incoming),out_neighbors=sorted(outgoing),in_degree=len(incoming),out_degree=len(outgoing),scope='Whole minute files overlapping injection +/-60s, descriptive callgraph; boundary/pod alias caveats, not incident onset or failure duration',position=('not_observed' if not present else 'no_observed_cross_service_edge' if not incoming and not outgoing else 'leaf' if not outgoing else 'source' if not incoming else 'intermediate')))
sym=collections.defaultdict(lambda:collections.Counter())
for x in symptoms['results']:
    key=(x['dataset'],x['date'],x['clock_interpretation'],x['channel'],x['q'],x['outside_root']);sym[key]['samples']+=x['n'];sym[key]['exceed']+=x['exceed'];sym[key]['empty_intervals']+=x['n']==0;sym[key]['zero_band_rows']+=x['zero_band']
result=dict(datasets=summaries,identical_normal_fault_paths=same,root_windows=cases,symptom_channel_summary=[dict(dataset=k[0],date=k[1],clock=k[2],channel=k[3],q=k[4],outside_root=k[5],**v) for k,v in sym.items()],symptom_calibration_min_n=min((x['reference_n'] for x in symptoms['calibration']),default=0),symptom_calibration_max_n=max((x['reference_n'] for x in symptoms['calibration']),default=0),symptom_limit='Strict source-designated normal trace timestamp bounds give no valid resource metric reference/control split. Rounded envelopes in symptoms002 are retained as limited exploratory failure. Whole construct metric directories duplicate fault; no resource-metric propagation conclusion. Trace-duration descriptive audit is separate trace-symptoms001.',sources=['file-audit-001/summary.json','download-001/manifest.json','run-001/labels.json','symptoms-003/result.json'])
(OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('PASS summary',len(cases),'root clock hypotheses',len(same),'identical paths')
