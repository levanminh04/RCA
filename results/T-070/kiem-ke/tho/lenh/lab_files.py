import subprocess, re, os, json, sys, collections
R='D:/Project/flashticket-rca-lab'
def git(*a): return subprocess.run(['git','-C',R,*a],capture_output=True,text=True,encoding='utf-8').stdout
files=git('ls-files').split('\n'); files=[f for f in files if f]
commits={'obs':'1bb40ca','app':'407b4f5','tai':'5a39028'}
def blobs(c):
    d={}
    for line in git('ls-tree','-r',c).split('\n'):
        if not line: continue
        meta,path=line.split('\t',1); d[path]=meta.split()[2]
    return d
main=blobs('HEAD'); mb={k:blobs(v) for k,v in commits.items()}
PAT=re.compile(r'(/(?:opt|srv|etc|home|var/lib|tmp|run)/[A-Za-z0-9_.\-/<>{}$]+|~/[A-Za-z0-9_.\-/]+|[A-Z]:[/\][A-Za-z0-9_.\-/\ ]+|\b(?:213\.35\.116\.128|129\.221\.208\.47|3\.24\.8\.49|10\.0\.0\.\d+)\b)')
TASK=re.compile(r'(?i)(t-?0\d\d|\bt\d-|\bl\d+b?\b|lich-t0|t3-|e2e-t0)')
texts={}
for f in files:
    try: texts[f]=open(os.path.join(R,f),encoding='utf-8',errors='replace').read()
    except Exception as e: texts[f]=''
def role(f,t):
    for line in t.split('\n')[:40]:
        s=line.strip().strip('#').strip('"').strip("'").strip('/').strip('*').strip()
        if len(s)>12 and not s.startswith(('!','import','from','{','-','set ','usage','coding','encoding','env','version','apiVersion','services:')): return s[:140]
    return ''
rows=[]
for f in files:
    t=texts[f]; base=os.path.basename(f); stem=os.path.splitext(base)[0]
    paths=sorted(set(m.group(0).rstrip('.,;:)`\'"') for m in PAT.finditer(t)))
    refs=[]
    for g,u in texts.items():
        if g==f: continue
        if base in u or (len(stem)>5 and stem.replace('-','_') in u and f.endswith('.py')) or f in u: refs.append(g)
    state={k:('trung' if mb[k].get(f)==main[f] else ('khac' if f in mb[k] else 'khong-co')) for k in commits}
    rows.append(dict(file=f,ma_task_trong_ten=bool(TASK.search(f)),vai_tro_dong_dau=role(f,t),may_obs_1bb40ca=state['obs'],may_app_407b4f5=state['app'],may_tai_5a39028=state['tai'],duong_dan_cung=paths,duoc_tham_chieu_boi=refs,dong=t.count('\n')))
json.dump(rows,open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(rows), sum(r['ma_task_trong_ten'] for r in rows))
