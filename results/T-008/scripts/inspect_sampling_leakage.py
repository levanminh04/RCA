"""Compare every Nezha filename with source labels; reuse metric audit, no new telemetry."""
import collections,datetime,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];O=B/'runs/sampling-leakage-001'
def load(n):return json.loads((B/n).read_text(encoding='utf-8'))
def main():
    O.mkdir(exist_ok=False);plan=load('runs/download-plan-001/plan.json');labels=load('runs/run-001/labels.json');full=load('runs/file-audit-001/summary.json')
    groups=[];cases=[];coverage=[]
    for ds,folder in [('OB','online-boutique'),('TT','train-ticket')]:
        for date in sorted({x['date'] for x in labels if x['dataset']==ds}):
            ls=[x for x in labels if x['dataset']==ds and x['date']==date]
            expected=set();events=[]
            for x in ls:
                t=datetime.datetime.strptime(x['inject_time_raw'],'%Y-%m-%d %H:%M:%S').replace(second=0)
                names=[(t+datetime.timedelta(minutes=m)).strftime('%H_%M') for m in range(3)]
                expected.update(names);events.append(dict(label=x,three_minute_names=names))
            modalities={}
            for mode in ('trace','log','traceid'):
                actual={Path(x['path']).name.split('_'+mode+'.csv')[0] for x in plan if x['path'].startswith(folder+'/rca_data/'+date+'/'+mode+'/')}
                # traceid file naming is verified by suffix in source inventory.
                modalities[mode]=dict(files=len(actual),expected_minutes=len(expected),matches=actual==expected,unexpected=sorted(actual-expected),missing=sorted(expected-actual))
            for x in events:cases.append(dict(dataset=ds,date=date,**x))
            groups.append(dict(dataset=ds,date=date,label_records=len(ls),modalities=modalities,
                construct_trace_files=[x['path'] for x in plan if x['path'].startswith(folder+'/construct_data/'+date+'/trace/')]))
            for f in full['results']:
                if not f['path'].startswith(folder+'/rca_data/'+date+'/metric/') or 'start_text_epoch' not in f:continue
                coverage.append(dict(dataset=ds,date=date,path=f['path'],rows=f['rows'],columns=f['columns'],start_text_epoch=f['start_text_epoch'],end_text_epoch=f['end_text_epoch'],
                    start_text_utc=datetime.datetime.fromtimestamp(f['start_text_epoch'],datetime.timezone.utc).isoformat(),end_text_utc=datetime.datetime.fromtimestamp(f['end_text_epoch'],datetime.timezone.utc).isoformat(),
                    duplicate_text_times=f.get('duplicate_text_times'),nonincreasing_steps=f.get('nonincreasing_steps'),cadence_seconds=f.get('cadence_seconds'),timestamp_minus_time_text_seconds=f.get('timestamp_minus_time_text_seconds')))
    report=dict(groups=groups,metric_coverage=coverage,all_case_filename_hypotheses=cases,
        note='Filename minute matches label text, not necessarily physical clock. No absence of a file is a healthy sample. Metric calendar files are separate from injection-conditioned minute trace/log sampling; no F1 continuous trace detection from this release alone.')
    (O/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(groups=groups,metric_files=len(coverage)),ensure_ascii=False))
if __name__=='__main__':main()
