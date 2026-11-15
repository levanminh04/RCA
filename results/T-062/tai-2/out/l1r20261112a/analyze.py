"""Analyze retained k6 outputs and match independently collected B16 gateway logs."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

def count(): return collections.Counter()
def analyze(root):
    checks=[]
    for line in (root/'outputs.sha256').read_text().splitlines():
        expected,name=line.split(None,1); name=name.lstrip('* ')
        actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
        checks.append({'file':name,'ok':expected==actual})
    if not all(x['ok'] for x in checks): raise ValueError('Output manifest mismatch')
    summary=json.loads((root/'summary.json').read_text())
    totals=count(); byjourney={k:count() for k in ['journey_started','journey_finished','journey_failed']}
    routes=count(); routeids=count(); statuses=count(); steps=count()
    first=None;last=None;refresh_times=[]
    for line in (root/'raw.json').open():
        item=json.loads(line)
        if item.get('type')!='Point':continue
        metric=item['metric']; d=item['data']; tags=d.get('tags',{}); value=d['value']
        if metric in ['journey_started','journey_finished','journey_failed','route_responses','token_refresh_success','token_refresh_failure','gateway_401','dropped_iterations','iterations','http_reqs']:
            totals[metric]+=value
        if metric in byjourney:byjourney[metric][tags['journey']]+=value
        if metric=='route_responses':
            routes[tags['route']]+=value;routeids[tags['routeId']]+=value
            statuses[tags['status']]+=value;steps[tags['step']]+=value
            first=min(first or d['time'],d['time']);last=max(last or d['time'],d['time'])
        if metric=='token_refresh_success':refresh_times.append(d['time'])
    requests=[]; errors=[]; orders={}
    for line in (root/'container.log').open():
        start=line.find('{')
        if start<0:continue
        try:item=json.loads(line[start:].strip())
        except ValueError:continue
        if item.get('type')=='request':requests.append(item)
        elif item.get('type')=='journey_error':errors.append(item)
        elif item.get('type')=='order_state':
            oid=item['orderId']; rec=orders.setdefault(oid,{'journey':item['journey'],'states':[]})
            if not rec['states'] or rec['states'][-1]!=item['state']:rec['states'].append(item['state'])
    csvtotals=count();csvrows=0
    with (root/'raw.csv').open(newline='') as f:
        for row in csv.DictReader(f):
            csvrows+=1
            if row['metric_name'] in totals:csvtotals[row['metric_name']]+=float(row['metric_value'])
    metric_checks={'csvMatchesJsonCounters':all(csvtotals[k]==v for k,v in totals.items()),
        'requestLogMatchesJson':len(requests)==totals['route_responses'],
        'httpSummaryMatchesJson':summary['metrics']['http_reqs']['count']==totals['http_reqs'],
        'allStartedAccounted':totals['journey_started']==totals.get('journey_finished',0)+totals.get('journey_failed',0),
        'distinctNewOrders':len(orders)==sum(v for k,v in byjourney['journey_started'].items() if k!='browse')}
    gateway=[]
    if (root/'gateway.jsonl').exists():
        gateway=[json.loads(l) for l in (root/'gateway.jsonl').read_text().splitlines() if l.strip()]
    gw_by_trace=collections.defaultdict(list)
    for item in gateway:gw_by_trace[item['traceId']].append(item)
    request_traces={r['traceId'] for r in requests}
    matched=count(); unmatched=[]; mismatches=[]; duplicate=[]
    for req in requests:
        found=gw_by_trace.get(req['traceId'],[])
        if len(found)==1:
            matched[req['route']]+=1
            g=found[0]
            if g['routeId']!=req['routeId'] or str(g['httpStatus'])!=str(req['status']):
                mismatches.append({'request':req,'gateway':g})
        elif not found:unmatched.append(req)
        else:duplicate.append(req['traceId'])
    gw_totals=count()
    for item in gateway:gw_totals[item.get('routeId','unknown')]+=1
    extra=[g for g in gateway if g['traceId'] not in request_traces]
    result={'totals':dict(totals),'journeys':{k:dict(v) for k,v in byjourney.items()},
        'mixMeasuredPercent':{k:100*v/totals['journey_started'] for k,v in byjourney['journey_started'].items()},
        'routes':dict(routes),'routeIds':dict(routeids),'statuses':dict(statuses),'steps':dict(steps),
        'requestLogCount':len(requests),'requestTraceUniqueCount':len(request_traces),
        'firstGatewayResponse':first,'lastGatewayResponse':last,'refreshTimes':refresh_times,
        'errors':errors,'orders':orders,'csvRows':csvrows,'hashChecks':checks,'metricChecks':metric_checks,
        'gateway':{'total':len(gateway),'routeIds':dict(gw_totals),'matchedRoutes':dict(matched),
            'missing':unmatched,'mismatches':mismatches,'duplicateTraces':duplicate,'extraRequests':extra},
        'summaryIterations':summary.get('metrics',{}).get('iterations'),
        'summaryDropped':summary.get('metrics',{}).get('dropped_iterations')}
    (root/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    with (root/'routes.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['route','k6_sent','gateway_matched','difference'])
        for route,n in sorted(routes.items()):w.writerow([route,n,matched[route],matched[route]-n])
    print(json.dumps({k:v for k,v in result.items() if k not in ['orders','refreshTimes','hashChecks']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();analyze(a.root)
