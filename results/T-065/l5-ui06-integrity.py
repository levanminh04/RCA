"""Audit the complete authorized file set and preserve the initial baseline."""
import pathlib,json,hashlib,datetime,subprocess
B=pathlib.Path('results/T-065'); O=B/'kiem/003-trinh-duyet'
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def diff(a,b,p=''):
    if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
    if isinstance(a,dict):
        assert a.keys()==b.keys(),p
        return [v for k in a for v in diff(a[k],b[k],p+'/'+k)]
    if isinstance(a,list):
        assert len(a)==len(b),p
        return [v for i,(x,y) in enumerate(zip(a,b)) for v in diff(x,y,p+'/'+str(i))]
    return [] if a==b else [{'path':p,'before':a,'after':b}]
semantic=[]
allowed_paths={'/time/from','/time/to','/panels/0/options/content','/panels/1/targets/0/root_selector','/panels/1/targets/0/columns/3/type','/panels/1/targets/0/columns/4/type',*[f'/templating/list/{i}/query/infinityQuery/{k}' for i in [4,5] for k in ['root_selector','columns/0/type']]}
for uid in ['t065-l4-rca','t065-l4-phat-lai']:
    changes=diff(read(B/'grafana-l5/ui05'/f'{uid}-truoc.json'),read(B/'grafana-l4'/f'{uid}.json'))
    assert {x['path'] for x in changes}==allowed_paths
    semantic.append({'uid':uid,'changes':changes})
(O/'ui06-semantic-diff.json').write_text(json.dumps(semantic,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
baseline=read(O/'baseline-UI04-suite.json'); changed=[]; missing=[]
for f,v in baseline['files'].items():
    p=B/f
    if not p.is_file():missing.append(f);continue
    actual=sha(p)
    if actual!=v['sha256']:changed.append({'file':f,'before':v['sha256'],'after':actual})
allowed={'BAN-GIAO-L5.md','CHECKPOINT.md','README-L4.md','XONG.md','prompt-ban-giao.md','thay-doi-may.md','codex/L5-prompt-tiep-nhan.md','codex/L5-trang-thai.json','l4-dashboard.mjs','l5-tong-hop.mjs','grafana-l4/t065-l4-rca.json','grafana-l4/t065-l4-phat-lai.json',*[f'kiem/003-trinh-duyet/{f}' for f in ['BAO-CAO.md','loi-va-sua.md','may.jsonl','nhat-ky-bam.jsonl','tien-do.json','doi-chieu-rong-snapshot.json','doi-chieu-hash-may-l5.json']]}
unexpected=[x for x in changed if x['file'] not in allowed]
new=[p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file() and p.relative_to(B).as_posix() not in baseline['files']]
log=pathlib.Path('tasks/T-065-giao-dien-grafana/LOG.md').read_bytes(); prefix_ok=hashlib.sha256(log[:baseline['log_bytes']]).hexdigest()==baseline['log_sha256']
tracked_hash=hashlib.sha256(subprocess.check_output(['git','diff','--binary'],stderr=subprocess.PIPE)).hexdigest(); tracked_status=hashlib.sha256(subprocess.check_output(['git','status','--porcelain','-uno'],stderr=subprocess.PIPE)).hexdigest()
idx=read('results/T-064/ban-xuat/chi-muc-ban.json'); source_bad=[];source_count=0
for v in idx['ban']:
    for c in v['cac_ca']:
        source_count+=1
        if sha(c['dau_ra'])!=c['sha256']:source_bad.append(c['dau_ra'])
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_files':len(baseline['files']),'changed':changed,'missing':missing,'unexpected':unexpected,'new_files':sorted(new),'log_append_only':prefix_ok,'tracked_diff_unchanged':tracked_hash==baseline['tracked_diff_sha256'],'tracked_status_unchanged':tracked_status==baseline['tracked_status_sha256'],'source_count':source_count,'source_bad':source_bad,'semantic_diff_paths':{v['uid']:[x['path'] for x in v['changes']] for v in semantic},'passed':not missing and not unexpected and prefix_ok and tracked_hash==baseline['tracked_diff_sha256'] and tracked_status==baseline['tracked_status_sha256'] and not source_bad}
(O/'ui06-integrity.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in r.items() if k not in ['new_files','changed']},ensure_ascii=False));print(json.dumps({'changed_files':[x['file'] for x in changed],'new_files_count':len(new)},ensure_ascii=False));assert r['passed']
