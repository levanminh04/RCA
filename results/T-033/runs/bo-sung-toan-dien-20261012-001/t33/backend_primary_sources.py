"""Small primary-source snapshots, no dataset/application version inference."""
import datetime,hashlib,json,pathlib,urllib.request
P=pathlib.Path(__file__).resolve().parent/'backend-primary-sources-001';P.mkdir(exist_ok=False);rows=[]
def get(name,url):
 request=urllib.request.Request(url,headers={'User-Agent':'RCA-research-readonly','Accept':'application/vnd.github+json'});response=urllib.request.urlopen(request,timeout=30);b=response.read();assert len(b)<2000000
 (P/name).write_bytes(b);rows.append({'file':name,'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'receivedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()});return b
head=json.loads(get('train-ticket-head.json','https://api.github.com/repos/FudanSELab/train-ticket/commits/master'))['sha']
hist=json.loads(get('seat-file-history.json','https://api.github.com/repos/FudanSELab/train-ticket/commits?path=ts-seat-service/src/main/java/seat/service/SeatServiceImpl.java&per_page=100'))
paths={'Response.java':'ts-common/src/main/java/edu/fudan/common/util/Response.java','SeatServiceImpl.java':'ts-seat-service/src/main/java/seat/service/SeatServiceImpl.java','OrderServiceImpl.java':'ts-order-service/src/main/java/order/service/OrderServiceImpl.java','OrderOtherServiceImpl.java':'ts-order-other-service/src/main/java/order/service/OrderOtherServiceImpl.java'}
for name,path in paths.items():get('head-'+name,'https://raw.githubusercontent.com/FudanSELab/train-ticket/'+head+'/'+path)
# Examine distinct historical file revisions, up to5 newest prior to logged2024.
prior=[x for x in hist if x['commit']['committer']['date']<'2024-01-24T00:00:00Z'][:5]
for k,commit in enumerate(prior):
 sha=commit['sha'];b=get('historical-seat-'+str(k)+'.java','https://raw.githubusercontent.com/FudanSELab/train-ticket/'+sha+'/'+paths['SeatServiceImpl.java'])
 if b'Get Order tickets result is' in b:
  for name in ['Response.java','OrderServiceImpl.java','OrderOtherServiceImpl.java']:get('matched-style-'+name,'https://raw.githubusercontent.com/FudanSELab/train-ticket/'+sha+'/'+paths[name])
  match={'source_commit':sha,'matching_literal':'Get Order tickets result is','date':commit['commit']['committer']['date'],'deploy_revision_match':'UNVERIFIED_STYLE_MATCH_ONLY'};break
else:match={'deploy_revision_match':'UNVERIFIED_NO_MATCH_AMONG_DECLARED5_HISTORY_SNAPSHOTS'}
(P/'manifest.json').write_text(json.dumps({'status':'COMPLETE','head_commit':head,'style_candidate':match,'source_files':rows,'provenance_limit':'HF datasetrevision and rawlog hashes are pinned; these do not identify deployed TrainTicket source commit/container digest. Public source semantic conventions are source-specific; matching literal logger text alone does not prove deployed revision.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'COMPLETE','files':len(rows),'bytes':sum(x['bytes'] for x in rows),'style_candidate':match}))
