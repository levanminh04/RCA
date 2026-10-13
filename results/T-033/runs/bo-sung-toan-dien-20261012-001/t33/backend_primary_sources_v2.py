"""Continue small source inspection; preserve first404 attempt and snapshots."""
import datetime,hashlib,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent;OLD=ROOT/'backend-primary-sources-001';P=ROOT/'backend-primary-sources-002';P.mkdir(exist_ok=False);rows=[]
def get(name,url):
 request=urllib.request.Request(url,headers={'User-Agent':'RCA-research-readonly','Accept':'application/vnd.github+json'})
 try:b=urllib.request.urlopen(request,timeout=30).read();assert len(b)<2000000
 except Exception as exc:rows.append({'file':name,'url':url,'status':'ERROR','error':repr(exc)});return None
 (P/name).write_bytes(b);rows.append({'file':name,'url':url,'status':'OK','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'receivedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()});return b
hist=json.loads((OLD/'seat-file-history.json').read_text());head=json.loads((OLD/'train-ticket-head.json').read_text())['sha'];paths={'Response.java':'ts-common/src/main/java/edu/fudan/common/util/Response.java','SeatServiceImpl.java':'ts-seat-service/src/main/java/seat/service/SeatServiceImpl.java','OrderServiceImpl.java':'ts-order-service/src/main/java/order/service/OrderServiceImpl.java','OrderOtherServiceImpl.java':'ts-order-other-service/src/main/java/other/service/OrderOtherServiceImpl.java'}
get('head-OrderOtherServiceImpl.java','https://raw.githubusercontent.com/FudanSELab/train-ticket/'+head+'/'+paths['OrderOtherServiceImpl.java'])
prior=[x for x in hist if x['commit']['committer']['date']<'2024-01-24T00:00:00Z'][:5];match=None
for k,commit in enumerate(prior):
 sha=commit['sha'];b=get('historical-seat-'+str(k)+'.java','https://raw.githubusercontent.com/FudanSELab/train-ticket/'+sha+'/'+paths['SeatServiceImpl.java'])
 if b and b'Get Order tickets result is' in b:
  for name in ['Response.java','OrderServiceImpl.java','OrderOtherServiceImpl.java']:get('matched-style-'+name,'https://raw.githubusercontent.com/FudanSELab/train-ticket/'+sha+'/'+paths[name])
  match={'source_commit':sha,'matching_literal':'Get Order tickets result is','date':commit['commit']['committer']['date'],'deploy_revision_match':'UNVERIFIED_STYLE_MATCH_ONLY'};break
oldpins=[{'file':str(q.relative_to(ROOT)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in OLD.iterdir() if q.is_file()]
(P/'manifest.json').write_text(json.dumps({'status':'COMPLETE_READ_ONLY_SOURCE_CHECK','head_commit':head,'style_candidate':match,'source_files':rows,'previous_attempt_snapshots':oldpins,'provenance_limit':'HF dataset revision and rawlog hashes are pinned; benchmark deployment source commit/container digest is not recorded in these sources. Literal/style matches support conditional business semantics, not version identity or health/onset truth.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'COMPLETE_READ_ONLY_SOURCE_CHECK','files':len(rows),'errors':sum(x['status']=='ERROR' for x in rows),'style_candidate':match}))
