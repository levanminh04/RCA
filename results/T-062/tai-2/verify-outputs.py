"""Independent format/count checks on saved files, without API traffic."""
import csv,collections,hashlib,json,re,sys
from pathlib import Path
reports=[]
for arg in sys.argv[1:]:
    root=Path(arg)
    raw=collections.Counter();csv_counts=collections.Counter()
    for line in (root/'raw.json').open():
        v=json.loads(line)
        if v.get('type')=='Point' and v['metric'] in ['route_responses','http_reqs','journey_started','journey_finished','journey_failed','token_refresh_success','token_refresh_failure','gateway_401','dropped_iterations']:
            raw[v['metric']]+=v['data']['value']
    with (root/'raw.csv').open(newline='') as f:
        for v in csv.DictReader(f):
            if v['metric_name'] in raw:csv_counts[v['metric_name']]+=float(v['metric_value'])
    manifest=[]
    for l in (root/'outputs.sha256').read_text().splitlines():
        digest,name=l.split(None,1);name=name.lstrip('* ')
        manifest.append({'file':name,'ok':hashlib.sha256((root/name).read_bytes()).hexdigest()==digest})
    a=json.loads((root/'analysis.json').read_text())
    statecounts=collections.Counter((o['journey'],o['states'][-1]) for o in a['orders'].values())
    checks={'csvEqualsJson':raw==csv_counts,'manifestAllMatched':all(x['ok'] for x in manifest),
        'httpSummaryEqual':raw['http_reqs']==json.loads((root/'summary.json').read_text())['metrics']['http_reqs']['count'],
        'allJourneyStartsFinishedOrFailed':raw['journey_started']==raw['journey_finished']+raw['journey_failed'],
        'requestLogEqualsCounter':a['requestLogCount']==raw['route_responses'],
        'uniqueIdentityPerRequest':a.get('requestIdentityUniqueCount',a.get('requestTraceUniqueCount'))==raw['route_responses']}
    reports.append({'run':root.name,'checks':checks,'counts':dict(raw),
        'stateCounts':{k[0]+'|'+str(k[1]):v for k,v in statecounts.items()},'manifestFiles':len(manifest)})
print(json.dumps(reports,indent=2))
if not all(all(r['checks'].values()) for r in reports):raise SystemExit(1)
