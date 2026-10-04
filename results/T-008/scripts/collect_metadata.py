"""Allowlisted documents, metadata and separate labels only; no telemetry.
py -3 -B collect_metadata.py --sources --run-id run-001
py -3 -B collect_metadata.py --verify --run-id run-001
"""
import argparse,collections,datetime,hashlib,json,pathlib,re,time,urllib.request
R=pathlib.Path(__file__).resolve().parents[1]
N=R.name=='T-008'
REPO='IntelligentDDS/Nezha' if N else 'BEbillionaireUSD/Eadro'
REV='d8140101fdb4e7dfb60d3ef9f64706f382b68470' if N else '82ff9c9a7a58a9cd2b713aa78754a73c543a15db'
BASE='https://raw.githubusercontent.com/'+REPO+'/'+REV+'/'
DATES=['2022-08-22','2022-08-23','2023-01-29','2023-01-30']
SOURCES=[]
def save(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def allowed(u):
 if u.startswith(BASE):
  p=u[len(BASE):]
  return p in ['README.md','Readme.md','LICENSE','FSE2023_Nezha.pdf','data_integrate.py','main.py','alarm.py','pattern_ranker.py','codes/preprocess/align.py','codes/preprocess/single_process.py','codes/preprocess/util.py','construct_data/root_cause_hipster.json','construct_data/root_cause_ts.json']+[f'rca_data/{d}/{d}-fault_list.json' for d in DATES]
 if u in ['https://api.github.com/repos/'+REPO,'https://api.github.com/repos/'+REPO+'/git/trees/'+REV+'?recursive=1','https://zenodo.org/api/records/8276375','https://zenodo.org/api/records/7615394','https://arxiv.org/html/2302.05092v1']:return True
 if not N:
  from urllib.parse import unquote
  for n in ['TT','SN']:
   prefix='https://zenodo.org/api/records/7615394/files/'+n+'%20Dataset.zip/container'
   if u==prefix:return True
   if u.startswith(prefix+'/') and re.fullmatch(n+r' Dataset/(data|no fault)/'+n+r'\.fault-[^/]+\.json',unquote(u[len(prefix)+1:])):return True
 return False
def get(u,name):
 assert allowed(u),u
 p=R/'sources'/name;t=time.perf_counter();cached=p.exists()
 if cached:b=p.read_bytes()
 else:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'RCA-metadata-audit'}),timeout=45) as f:b=f.read(6_000_001)
  assert len(b)<=6_000_000
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 SOURCES.append(dict(path=str(p.relative_to(R)).replace('\\','/'),url=u,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),cached=cached,seconds=round(time.perf_counter()-t,4),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 return b
def gj(u,p):return json.loads(get(u,p))
def collect():
 gj('https://api.github.com/repos/'+REPO,'repository.json')
 tr=gj('https://api.github.com/repos/'+REPO+'/git/trees/'+REV+'?recursive=1','tree.json');assert not tr.get('truncated')
 if N:
  for p in ['README.md','LICENSE','FSE2023_Nezha.pdf','data_integrate.py','main.py','alarm.py','pattern_ranker.py']:get(BASE+p,p)
  for d in DATES:get(BASE+f'rca_data/{d}/{d}-fault_list.json',f'labels/{d}-fault_list.json')
  for x in ['hipster','ts']:get(BASE+f'construct_data/root_cause_{x}.json',f'labels/root_cause_{x}.json')
  gj('https://zenodo.org/api/records/8276375','zenodo.json')
 else:
  for p in ['Readme.md','codes/preprocess/align.py','codes/preprocess/single_process.py','codes/preprocess/util.py']:get(BASE+p,p)
  get('https://arxiv.org/html/2302.05092v1','paper.html');gj('https://zenodo.org/api/records/7615394','zenodo.json')
  for n in ['TT','SN']:
   inv=gj('https://zenodo.org/api/records/7615394/files/'+n+'%20Dataset.zip/container',n+'-inventory.json')
   for e in inv['entries']:
    if re.fullmatch(n+r' Dataset/(data|no fault)/'+n+r'\.fault-[^/]+\.json',e['key']):get(e['links']['content'],'labels/'+n+'/'+e['key'].split('/')[-1])
def compute():
 rows=[];inventory=[];normal=[];plan=[];summary={};cells=[]
 if N:
  for e in load(R/'sources/tree.json')['tree']:
   if e['type']=='blob':
    inventory.append(e)
    if re.match(r'(construct_data|rca_data)/(2022-08-2[23]|2023-01-(29|30))/(metric|trace|traceid|log)/',e['path']):plan.append(dict(dataset='OB' if '/2022' in e['path'] else 'TT',path=e['path'],bytes=e['size'],url=BASE+e['path'],read_status='NOT_FETCHED'))
  for d in DATES:
   for hour,a in load(R/f'sources/labels/{d}-fault_list.json').items():
    for i,r in enumerate(a):
     sec=datetime.datetime.fromisoformat(r['inject_time']).replace(tzinfo=datetime.timezone.utc).timestamp()
     rows.append(dict(dataset='OB' if d.startswith('2022') else 'TT',source=f'sources/labels/{d}-fault_list.json',date=d,index_in_hour=i,hour=hour,entity_raw=r['inject_pod'],service=r['inject_pod'].rsplit('-',2)[0],fault=r['inject_type'],inject_time_raw=r['inject_time'],inject_timestamp_raw=r['inject_timestamp'],text_as_utc_minus_epoch_s=int(sec)-int(r['inject_timestamp'])))
 else:
  for n in ['TT','SN']:
   for e in load(R/f'sources/{n}-inventory.json')['entries']:
    inventory.append(dict(dataset=n,**e))
    if e['key'].startswith('__MACOSX/') or e['key'].endswith('.DS_Store'):continue
    if re.fullmatch(n+r' Dataset/(data|no fault)/'+n+r'\.fault-[^/]+\.json',e['key']):
     source='sources/labels/'+n+'/'+e['key'].split('/')[-1];obj=load(R/source)
     if not obj['faults']:normal.append(dict(dataset=n,source=source,start=obj['start'],end=obj['end'],seconds=obj['end']-obj['start']))
     for i,r in enumerate(obj['faults']):
      svc=r['name'].removeprefix('dockercomposemanifests_').removesuffix('_1') if n=='TT' else r['name'].removeprefix('socialnetwork-').removesuffix('-1')
      rows.append(dict(dataset=n,source=source,index_in_file=i,entity_raw=r['name'],service=svc,fault=r['fault'],start=r['start'],duration=r['duration'],end_derived=r['start']+r['duration'],session_start=obj['start'],session_end=obj['end']))
    else:plan.append(dict(dataset=n,path=e['key'],bytes=e['size'],url=e['links']['content'],read_status='NOT_FETCHED'))
 for n in sorted({r['dataset'] for r in rows}):
  rs=[r for r in rows if r['dataset']==n];cs=collections.Counter((r['service'],r['fault']) for r in rs);roots=sorted({r['service'] for r in rs});faults=sorted({r['fault'] for r in rs})
  cells.extend(dict(dataset=n,service=s,fault=f,count=c) for (s,f),c in sorted(cs.items()))
  summary[n]=dict(events=len(rs),root_count=len(roots),roots=roots,fault_counts=dict(collections.Counter(r['fault'] for r in rs)),cells=len(cs),repeat_histogram=dict(collections.Counter(cs.values())),missing_cross_product=[dict(service=s,fault=f) for s in roots for f in faults if (s,f) not in cs],telemetry_read_events=0,proposed_bytes=sum(p['bytes'] for p in plan if p['dataset']==n))
  if N:
   summary[n]['time_offset_histogram']=dict(collections.Counter(r['text_as_utc_minus_epoch_s'] for r in rs));summary[n]['by_date']=dict(collections.Counter(r['date'] for r in rs));summary[n]['duplicate_epoch_count']=len(rs)-len({r['inject_timestamp_raw'] for r in rs})
   mp=load(R/('sources/labels/root_cause_'+('hipster' if n=='OB' else 'ts')+'.json'));summary[n]['mapping_roots']=sorted(mp);summary[n]['unmatched_mapping_events']=[r for r in rs if r['service'] not in mp or r['fault'] not in mp[r['service']]]
  else:
   es=[e for e in inventory if e['dataset']==n];clean=[e for e in es if not e['key'].startswith('__MACOSX/')]
   summary[n].update(outer_entries=len(es),outer_bytes=sum(e['size'] for e in es),outer_clean_entries=len(clean),outer_clean_bytes=sum(e['size'] for e in clean),normal_sessions=sum(x['dataset']==n for x in normal),normal_label_seconds=sum(x['seconds'] for x in normal if x['dataset']==n),durations=dict(collections.Counter(r['duration'] for r in rs)),duplicate_label_tuples=len(rs)-len({(r['entity_raw'],r['fault'],r['start']) for r in rs}),span_files=sum(e['key'].endswith('/spans.json') for e in clean),log_files=sum(e['key'].endswith('/logs.json') for e in clean))
 return dict(summary=summary,labels=rows,cells=cells,inventory=inventory,normal_intervals=normal,proposed_files=plan)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sources',action='store_true');ap.add_argument('--verify',action='store_true');ap.add_argument('--validate-counts',action='store_true');ap.add_argument('--run-id',default='run-001');a=ap.parse_args();run=R/'runs'/a.run_id;t=time.perf_counter()
 if a.sources:
  assert not run.exists(),'Keep old runs; use a new run-id';run.mkdir(parents=True)
  try:
   collect()
   for k,v in compute().items():save(run/(k+'.json'),v)
   save(run/'manifest.json',dict(task=R.name,repository=REPO,revision=REV,sources=SOURCES,network_bytes=sum(s['bytes'] for s in SOURCES if not s['cached']),telemetry_download_bytes=0,seconds=time.perf_counter()-t))
   save(run/'status.json',dict(ok=True,seconds=time.perf_counter()-t));print('Sources and counts saved:',run)
  except Exception as e:
   save(run/'manifest-partial.json',SOURCES);save(run/'status.json',dict(ok=False,error=repr(e),seconds=time.perf_counter()-t));raise
 if a.verify or a.validate_counts:
  for k,v in compute().items():assert json.loads(json.dumps(v))==load(run/(k+'.json')),k
  for s in load(run/'manifest.json')['sources']:
   b=(R/s['path']).read_bytes();assert len(b)==s['bytes'] and hashlib.sha256(b).hexdigest()==s['sha256'];assert allowed(s['url'])
  if a.verify:
   c=(R/'the-dataset.md').read_text(encoding='utf-8')
   for i in range(1,11):assert len(re.findall(r'^## '+str(i)+r'\.',c,re.M))==2,i
   assert (R/'inspection-plan.md').is_file()
  print('PASS: offline recomputation, source hashes, allowlist'+('; two complete 10-section cards' if a.verify else ''))
if __name__=='__main__':main()
