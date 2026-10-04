"""Independent trace export checks, capture overlap, declared targets and bands.

Targets are source-level hints, not new root gold. No classification/causality.
"""
import argparse,collections,csv,datetime,hashlib,io,json,re,time,zipfile
from pathlib import Path
from inspect_review_archives import probes,save
B=Path(__file__).resolve().parents[1];ROOT=B.parents[1];O=None
def main():
    global O
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args();O=B/'runs'/a.run
    O.mkdir(exist_ok=False);start=time.monotonic();z=zipfile.ZipFile(ROOT/'data/ngoai-rcaeval/T-012/anomod/AnoMod.zip');cases={};consistency=[];source=B/'runs/anomod-collector-review-001'
    for n in z.namelist():
        if n.startswith('SN_data/trace_data/') and n.endswith('/all_traces.csv'):
            name=re.match(r'(.*?202\d\d\d\d\d_\d{6})',n.split('/')[2])[1];rows=list(csv.DictReader(io.StringIO(z.read(n).decode('utf-8-sig'))));ids={x['trace_id'] for x in rows};data=json.loads(z.read(n.replace('.csv','.json')))['data'];jsonids={t['traceID'] for t in data};jsonspan={(t['traceID'],s['spanID']) for t in data for s in t['spans']};csvspan={(r['trace_id'],r['span_id']) for r in rows}
            consistency.append(dict(case=name,json_traces=len(data),json_spans=sum(len(t['spans']) for t in data),csv_rows=len(rows),trace_id_sets_equal=ids==jsonids,span_key_sets_equal=jsonspan==csvspan))
            ss=collections.defaultdict(list)
            for r in rows:ss[(r['service'],r['operation'])].append((r['start_time'],float(r['duration_us'])))
            cases[('SN',name)]=dict(ids=ids,series=ss,start_hint=None)
        elif n.startswith('TT_data/trace_data/') and n.endswith('.json'):
            d=json.loads(z.read(n));name=n.split('/')[2];ids={t['summary']['trace_id'] for t in d['traces']};ss=collections.defaultdict(list);times=[]
            for t in d['traces']:
                for s in t['spans']:ss[(s['service_code'],s['endpoint_name'])].append((s['start_timestamp_ms'],float(s['duration_ms'])));times.append(s['start_timestamp_ms'])
            tm=re.search(r'(202\d\d\d\d\dT\d{6}Z)',name)[1];hint=datetime.datetime.strptime(tm,'%Y%m%dT%H%M%SZ').replace(tzinfo=datetime.timezone.utc).timestamp()*1000
            cases[('TT',name)]=dict(ids=ids,series=ss,start_hint=hint,spans_before_name_time=sum(t<hint for t in times),spans=len(times),time_min=min(times),time_max=max(times))
    rows=[];overlap=[];bands=[]
    for (system,name),d in cases.items():
        normal=next(v for (s,n),v in cases.items() if s==system and n.lower().startswith('normal'));targets=[];level='unverified';src=[]
        if system=='TT' and not name.lower().startswith('normal'):
            for p in source.glob('*.yaml'):
                family=p.name.split('__')[-1][:-5]
                if name.startswith(family+'_'):
                    text=p.read_text();m=re.search(r'target_service:\s*"([^"]+)"',text)
                    if m:targets=[m[1]];level='database' if m[1]=='tsdb-mysql' else 'service';src=[p.name];break
            for family,target in [('security_check','ts-security-service'),('exception_injection','ts-order-service'),('travel_detail','ts-travel-service')]:
                if family in name:targets=[target];level='service';src=['TT_collection-scripts__T-Dataset__run_experiment.sh']
        elif system=='SN' and not name.lower().startswith('normal'):
            src=['SN_collection-scripts__automated_multimodal_collection.sh']
            mappings={'Svc_Kill_UserTimeline':['user-timeline-service'],'Svc_Kill_Media':['media-service'],'Svc_Kill_SocialGraph':['social-graph-service'],'Code_Stop_UserService':['user-service'],'Code_Stop_TextService':['text-service'],'Code_Stop_MediaService':['media-service'],'DB_Redis_CacheLimit_UserTimeline':['user-timeline-redis'],'DB_Redis_CacheLimit_HomeTimeline':['home-timeline-redis'],'DB_Redis_CacheLimit_SocialGraph':['social-graph-redis']}
            for family,target in mappings.items():
                if name.startswith(family+'_'):targets=target;level='database' if family.startswith('DB_') else 'service';break
            if name.startswith('Perf_'):level='host';targets=['host CPU/disk or docker0 interface; not a service root']
        positions=[]
        raw=next(x for x in json.loads((B/'runs/anomod-file-inspect-003/cases.json').read_text()) if x['case']==name and x['system']==('SN_data' if system=='SN' else 'TT_data'))
        edges=raw['trace']['edges'];services=raw['trace']['services']
        for t in targets:positions.append(dict(target=t,present=t in services,indegree=sum(y==t for x,y in edges),outdegree=sum(x==t for x,y in edges)))
        rows.append(dict(system=system,capture=name,traces=len(d['ids']),normal_trace_overlap=len(d['ids']&normal['ids']),name_is_not_injection_time=True,spans_before_name_time=d.get('spans_before_name_time'),spans=d.get('spans'),declared_targets=targets,target_level=level,target_sources=src,source_targets_not_gold=True,target_graph_positions=positions))
        if not name.lower().startswith('normal'):
            b=probes(normal['series'],d['series'],targets,name,'trace_duration_us' if system=='SN' else 'trace_duration_ms')
            for x in b:x['outside_declared_target']=x.pop('outside_root') if level=='service' else None;x['source_targets_not_gold']=True;x['unit']='us' if system=='SN' else 'ms'
            bands+=b
    keys=list(cases)
    for i,(s,n) in enumerate(keys):
        for t,m in keys[i+1:]:
            if t==s:overlap.append(dict(system=s,left=n,right=m,common_trace_ids=len(cases[(s,n)]['ids']&cases[(t,m)]['ids'])))
    save(O,'captures.json',rows);save(O,'trace-export-checks.json',consistency);save(O,'overlap.json',overlap);save(O,'descriptive-bands.json',bands);save(O,'validation.json',dict(ok=all(x['trace_id_sets_equal'] and x['span_key_sets_equal'] for x in consistency),captures=len(rows),probe_rows=len(bands),seconds=time.monotonic()-start,root_gold_invented=False,limitations=['source target bindings need actual injection execution logs','SN CSV naive local time per datetime.fromtimestamp; raw Jaeger epoch retained','TT collector lookback 24h; name time is not injection onset','host/database targets do not equal service root','SN Code_Stop uses docker stop, not seeded code defect']))
    print('followup',len(rows),len(bands))
if __name__=='__main__':main()
