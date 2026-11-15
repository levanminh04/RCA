"""30s request bins, scenario arrival counts and observed VU concurrency from saved outputs."""
import collections,csv,datetime as dt,json,math,sys
from pathlib import Path
root=Path(sys.argv[1]);config=json.loads((root/'run.json').read_text())
requests=[];events=[];epoch=None;starts=collections.Counter();scenario_epochs={}
def timestamp(s):return dt.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
for line in (root/'container.log').read_text().splitlines():
    index=line.find('{')
    if index<0:continue
    try:v=json.loads(line[index:])
    except ValueError:continue
    if v.get('type')=='request':requests.append(v)
    if v.get('type')=='journey_start':
        candidate=v['testEpochMs']/1000
        if epoch is None:epoch=candidate
        scenario_epochs.setdefault(v['scenario'],candidate)
        starts[v['scenario']]+=1;events.append((timestamp(v['utc']),1,v['scenario'],v['vu']))
    elif v.get('type')=='journey_end':events.append((timestamp(v['utc']),-1,v['scenario'],v['vu']))
if epoch is None:raise SystemExit('No measured test epoch')
gateway=[json.loads(l) for l in (root/'gateway.jsonl').read_text().splitlines() if l.strip()]
rows=[{'fromSeconds':i,'toSeconds':min(i+30,config['seconds']),'k6Sent':0,'k6Completed':0,'gatewayCompleted':0,'gatewayMatched':0,'gatewayOther':0} for i in range(0,config['seconds'],30)]
tail=collections.Counter()
def add(t,key):
    relative=t-epoch
    index=math.floor(relative/30)
    if index<0 or index>=len(rows):tail[key]+=1;return
    rows[index][key]+=1
for r in requests:
    add(timestamp(r['sentUtc']),'k6Sent');add(timestamp(r['utc']),'k6Completed')
request_ids={r.get('requestId') for r in requests if r.get('requestId')}
correlations=collections.Counter(r.get('correlationId') for r in requests if r.get('correlationId'))
gateway_correlations=collections.Counter(r.get('correlationId') for r in gateway if r.get('correlationId'))
for r in gateway:
    add(timestamp(r['timestamp']),'gatewayCompleted')
    matched=r.get('requestId') in request_ids or (r.get('correlationId') and correlations[r['correlationId']]==1 and gateway_correlations[r['correlationId']]==1)
    add(timestamp(r['timestamp']),'gatewayMatched' if matched else 'gatewayOther')
for row in rows:
    width=row['toSeconds']-row['fromSeconds']
    for key in ['k6Sent','k6Completed','gatewayCompleted','gatewayMatched','gatewayOther']:row[key+'PerSecond']=row[key]/width
active=collections.Counter();peak=collections.Counter();active_vus=set();totalpeak=0
for _,delta,scenario,vu in sorted(events):
    active[scenario]+=delta;peak[scenario]=max(peak[scenario],active[scenario])
    if delta>0:active_vus.add(vu)
    else:active_vus.discard(vu)
    totalpeak=max(totalpeak,len(active_vus))
raw_counts=collections.Counter();dropped_by_scenario=collections.Counter();maxgauge=0
for line in (root/'raw.json').open():
    v=json.loads(line)
    if v.get('type')!='Point':continue
    data=v['data'];metric=v['metric']
    if metric in ['journey_started','journey_finished','journey_failed','dropped_iterations','gateway_401','token_refresh_success','token_refresh_failure']:raw_counts[metric]+=data['value']
    if metric=='dropped_iterations':dropped_by_scenario[data.get('tags',{}).get('scenario','unknown')]+=data['value']
    if metric=='vus':maxgauge=max(maxgauge,data['value'])
out={'testEpochUtc':dt.datetime.fromtimestamp(epoch,dt.timezone.utc).isoformat(),'run':config,'rows30s':rows,
    'scenarioEpochOffsetMilliseconds':{name:(value-epoch)*1000 for name,value in scenario_epochs.items()},
    'tailOutsideConfiguredWindow':dict(tail),'journeyStartsByScenario':dict(starts),
    'observedPeakActiveJourneysByScenario':dict(peak),'observedPeakActiveJourneysTotal':totalpeak,
    'k6MaxVUsGauge':maxgauge,'counts':dict(raw_counts),'droppedByScenario':dict(dropped_by_scenario)}
(root/'buoc-tai.json').write_text(json.dumps(out,indent=2)+'\n')
with (root/'buoc-tai-30s.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print(json.dumps(out))
