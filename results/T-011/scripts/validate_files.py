"""Independent KPI arithmetic and cross-modality coverage on approved samples."""
import argparse,collections,csv,datetime,io,json,math,pathlib,struct,time,zipfile
from safe_npy import read_npy,numeric,array_info
from inspect_files import quantile

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--inspection',required=True);ap.add_argument('--results',required=True);ap.add_argument('--skip-linkage',action='store_true');ap.add_argument('--skip-comparisons',action='store_true');args=ap.parse_args()
    out=pathlib.Path(args.results);out.mkdir(parents=True,exist_ok=False); start=time.monotonic()
    comparisons=[]
    for kind,date in [('Cloud_Computing','20240124'),('Product_Review','20211203')]:
        if args.skip_comparisons: break
        z=zipfile.ZipFile(pathlib.Path(args.data)/(kind+'_Preprocessed')/'Metrics Data'/(date+'.zip'))
        csvnames=[n for n in z.namelist() if n.endswith('.csv')]; groups={}
        for name in csvnames:
            bins=collections.defaultdict(lambda:[0.,0]); count=0
            with z.open(name) as f,io.TextIOWrapper(f,encoding='utf-8-sig',newline='') as txt:
                for row in csv.DictReader(txt):
                    count+=1; t=int(row['timeStamp']); t=t//1000000 if t>1e14 else t
                    feature='Latency' if 'Latency' in row else 'is_error'; key=(row['label'],t)
                    bins[key][0]+=float(row[feature]);bins[key][1]+=1
            groups[feature]={k:v[0]/v[1] for k,v in bins.items()}
            print(json.dumps({'csv':name,'rows':count,'bins':len(bins)}),flush=True)
        # Every KPI value in every safely parseable Sequence is checked, including
        # duplicate aliases. This validates shared-second intersection, not raw provenance.
        for name in z.namelist():
            if not name.endswith('.npy') or 'p2n' in name: continue
            try:
                header,obj=read_npy(z.read(name))
                for label,case in obj.items():
                    feature=case.get('KPI_Feature',case.get('jaeger_Feature'))[0]; shape,code,raw=array_info(case['Sequence']); rows,cols=shape
                    matched=missing=wrong=0; maxerr=0.
                    for i,t in enumerate(case['time']):
                        t=numeric(t); key=(label,t)
                        if key not in groups[feature]: missing+=1; continue
                        actual=struct.unpack_from('<d',raw,8*(i*cols+cols-1))[0]; expected=groups[feature][key]; matched+=1
                        err=abs(actual-expected); maxerr=max(maxerr,err)
                        if not math.isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-9): wrong+=1
                    comparisons.append({'dataset':kind,'member':name,'kpi':label,'feature':feature,'matched':matched,'missing':missing,'mismatches':wrong,'max_absolute_error':maxerr,'tolerance':'rel1e-12 abs1e-9'})
            except Exception as exc: comparisons.append({'dataset':kind,'member':name,'error':repr(exc)})
        del groups
    summaries=[] if args.skip_linkage else json.loads((pathlib.Path(args.inspection)/'summaries.json').read_text())
    linkage=[]; logbands=[]
    for kind in ['Cloud_Computing','Product_Review']:
        metric_entities=set(); log_entities=set(); log_feature_entities=set();template_entities=set(); mappings={}; csv_by_entity={}
        for s in summaries:
            if kind not in s['archive']: continue
            for c in s.get('cases',[]):
                if 'Metrics Data' in s['archive']: metric_entities.update(c['entities'])
                elif 'Log Data' in s['archive']: log_feature_entities.update(c['entities'])
            mappings.update(s.get('mapping',{}))
            name=pathlib.PurePosixPath(s['member']).name
            if name.endswith('_messages_structured.csv'):
                entity=name.removesuffix('_messages_structured.csv');log_entities.add(entity);csv_by_entity[entity]=s
                if kind=='Cloud_Computing':
                    # Use only full UTC hours strictly inside source's before/after periods.
                    counts={int(datetime.datetime.fromisoformat(k+':00:00+00:00').timestamp()):v for k,v in s['hour_counts'].items()}
                    onset=int(datetime.datetime(2024,1,24,3,10,tzinfo=datetime.timezone.utc).timestamp()); normal=onset-86400; mid=normal+43200; final=onset+86400
                    windows=[(normal,mid),(mid,onset),(onset,final)];g=[]
                    for a,b in windows:
                        g.append([counts.get(t,0) for t in range((a//3600+1)*3600,b//3600*3600,3600)])
                    median=quantile(g[0],.5); dev=[abs(x-median) for x in g[0]]
                    logbands.append({'entity':entity,'unit':'events/full UTC hour','counts':[len(x) for x in g],'median':median,
                                     'q':[{'q':q,'band':quantile(dev,q),'zero_band':quantile(dev,q)==0,
                                           'exceed':[sum(abs(x-median)>quantile(dev,q) for x in v) for v in g[1:]]} for q in [.95,.99,.995]],
                                     'boundary_hours':'excluded; missing full hours count zero; no severity regex'})
            elif name.endswith('_messages_templates.csv'): template_entities.add(name.removesuffix('_messages_templates.csv'))
        linkage.append({'dataset':kind,'metric_entities':sorted(metric_entities),'log_entities':sorted(log_entities),
                        'log_feature_entities':sorted(log_feature_entities),
                        'exact_overlap':sorted(metric_entities&log_entities),'metric_without_log':sorted(metric_entities-log_entities),
                        'log_without_metric':sorted(log_entities-metric_entities),'template_without_structured':sorted(template_entities-log_entities),
                        'structured_without_template':sorted(log_entities-template_entities),'mapping':mappings})
    errors=[x for x in comparisons if x.get('error') or x.get('missing') or x.get('mismatches')]
    result={'comparisons':comparisons,'comparison_errors':errors,'linkage':linkage,'log_bands':logbands,'elapsed_seconds':round(time.monotonic()-start,3),
            'coverage':'preprocessed CSV↔Sequence only; no Original comparison; source normal narrative is not verified healthy label'}
    (out/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'comparisons':len(comparisons),'errors':len(errors),'seconds':result['elapsed_seconds']}),flush=True)

if __name__=='__main__': main()
