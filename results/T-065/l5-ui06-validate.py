"""Validate saved UI06 evidence without browser, raw-data, API or M1 reruns."""
import pathlib,json,datetime,hashlib,urllib.parse
B=pathlib.Path('results/T-065'); O=B/'kiem/003-trinh-duyet'
def read(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def context(url):
    q=urllib.parse.parse_qs(urllib.parse.urlparse(url).query,keep_blank_values=True)
    def ms(v): return int(v) if v.isdigit() else int(datetime.datetime.fromisoformat(v.replace('Z','+00:00')).timestamp()*1000)
    return {**{k:q.get(k,[''])[0] for k in ['var-ban','var-ca','var-dv','var-op']},**{k:ms(q[k][0]) for k in ['from','to']}}
rows=[json.loads(s) for s in (O/'ui06-inspectors.jsonl').read_text(encoding='utf-8').splitlines()]
plan=read(O/'ui04-suite-inspector-plan.json')
key=lambda r:(r['ban'],r['service'],r['panel'])
checks={'inspector_slots':len(rows)==10 and {key(r) for r in rows}=={key(r) for r in plan},'inspector_checks':all(r['passed'] and all(r['checks'].values()) and r['observed']['statuses']==['status:200'] for r in rows),'inspector_files':all((O/r['raw']).stat().st_size>0 and (O/r['image']).stat().st_size>0 for r in rows)}
roundtrip=read(O/'ui06-2e-roundtrip.json'); replay=read(O/'ui06-2e-view.json'); done=read(O/'ui06-browser-completion.json')
checks['roundtrip_context']=context(roundtrip['before'])==context(roundtrip['replay'])==context(roundtrip['after'])
checks['main_separates_answers']=roundtrip['mainReplayPanelBefore']==0 and done['mainReplayPanelAfter'] is False
oldplan=read(O/'ui04-plan.json'); expected=next(r['expected'] for r in oldplan if r['key']=='V041-R1-H1c+H5b+H8s1/2e2a5541/replay');expected=[[a,('Chưa có giá trị trong nguồn.' if b is None else b)] for a,b in expected]
checks['replay_rows']=replay['table']['headers']==['Trường','Giá trị'] and replay['table']['rows']==expected
dev=read(O/'ui06-dev-final.json');checks['dev_limit_only']=dev['table']['rows']==[['Giới hạn','Chưa cấp nguồn phát lại/đáp án dev2 cho lớp giao diện; không dựng đáp án.']]
snap=read(O/'ui06-snapshot28-view.json')['table']; src=read(B/'kiem/002/api-snapshot.json')['e8661e0a/api-gateway']; si=snap['headers']; observed={int(r[si.index('panel')]):dict(zip(si,r)) for r in snap['rows']}
checks['snapshot_rows']=len(observed)==5 and all(int(observed[q['panel']]['so_dong'])==q['so_dong'] and observed[q['panel']]['utc']==q['utc'] for q in src['queries'])
lst=read(O/'ui06-list-iso.json'); source=read(B/'du-lieu-l4/V041-R1-H1c+H5b+H8s1/chi-muc.json'); index={r['ma']:r for r in source['su_co']}; cols=lst['table']['headers']; checked=[]
for r in lst['table']['rows']:
    x=dict(zip(cols,r)); original=index[x['ma']]; checked.append(all(context('http://local/?from='+urllib.parse.quote(x['tu'])+'&to='+urllib.parse.quote(x['den']))[k]==original['tu' if k=='from' else 'den'] for k in ['from','to']))
checks['list_observed_rows_iso']=bool(checked) and all(checked) and 'from=2026-' in lst['devLink'] and 'to=2026-' in lst['devLink']
prior=read(O/'avant-UI06-tong-hop/doi-chieu-rong-snapshot.json');current=read(O/'doi-chieu-rong-snapshot.json');checks['historical_panels_unchanged']=prior['panels']==current['panels'] and sum(r['loai']=='iii' for r in current['panels'])==10
checks['rebuilt']=all(x['structural_equal'] for x in read(O/'ui06-rebuild-final-check.json')['dashboards'])
inventory=read(O/'may-ui06-cuoi.json');old=read(O/'may-chat-moi-cuoi.json');changed=[p for p,v in old['files'].items() if inventory['files'].get(p,{}).get('sha256')!=v['sha256']]; deploy=read(O/'ui06-plan.json')['changes']
checks['machine_files']=len(inventory['files'])==len(old['files'])==9 and set(changed)=={x['path'] for x in deploy} and all(inventory['files'][x['path']]['sha256']==sha(B/'grafana-l4'/f"{x['uid']}.json")==x['after'] for x in deploy)
checks['no_restart']=inventory['restart_count']=='0' and inventory['started_at']=='2026-11-14T04:15:16.724003302Z'
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'passed':all(checks.values()),'inspectors':len(rows),'list_rows_actually_read':len(checked),'snapshot_rows':len(observed),'replay_rows':len(replay['table']['rows']),'machine_files':len(inventory['files']),'machine_changed':changed,'historical_class_iii':10,'qa_images':'qa-ui06-inspectors.png','limitations':['Inspector trees saved as fully expanded rendered text, not native JSON export.','Historical request/response at the old observation times remains unavailable.','Old numeric bookmarks remain unsupported in the observed hard-navigation path; use ISO UTC links from current dashboard.','Old broad coverage is reused for metadata/ranking/edges, not claimed as fresh live-query coverage after UI06.']}
(O/'ui06-kiem-cuoi.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
assert result['passed']
