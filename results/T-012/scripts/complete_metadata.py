"""Capture official documentation and repository metadata only; never telemetry.

Every online execution requires a new run id. Failures remain in the manifest.
No archive, dataset member, model result or measurement payload is fetched.
"""
import argparse, concurrent.futures, datetime, hashlib, json, time, urllib.request
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parents[1]
HOSTS = {'api.github.com','raw.githubusercontent.com','zenodo.org','netman.aiops.org','conf.researchr.org'}
LIMIT = 8_000_000

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);ap.add_argument('--verify',action='store_true');a=ap.parse_args()
    if not a.run.replace('-','').isalnum(): raise ValueError('bad run id')
    d=BASE/'runs'/a.run
    if a.verify:
        m=json.loads((d/'source-manifest.json').read_text(encoding='utf-8'))
        checks=[]
        for x in m['items']:
            if x['status']=='ok':
                raw=(BASE/x['path']).read_bytes();checks.append(len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256'])
        print(json.dumps({'ok':all(checks),'verified':len(checks),'failures_retained':sum(x['status']!='ok' for x in m['items'])}));return
    d.mkdir(parents=True,exist_ok=False);(d/'sources').mkdir();items=[];began=time.perf_counter()
    def fetch(name,url):
        p=urlparse(url)
        if p.hostname not in HOSTS or ('zenodo.org'==p.hostname and '/files/' in p.path):raise ValueError('outside metadata scope')
        x={'id':name,'url':url,'fetched_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};t=time.perf_counter()
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'T012-metadata-audit/2'}),timeout=35) as r:
                q=urlparse(r.geturl())
                if q.hostname not in HOSTS or ('zenodo.org'==q.hostname and '/files/' in q.path):raise ValueError('redirect outside metadata scope')
                raw=r.read(LIMIT+1)
                if len(raw)>LIMIT:raise ValueError('source too large')
                path=d/'sources'/name;path.write_bytes(raw)
                x.update(status='ok',path=path.relative_to(BASE).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),final_url=r.geturl())
        except Exception as e:x.update(status='error',error=repr(e))
        x['elapsed_seconds']=round(time.perf_counter()-t,3);items.append(x);return x
    initial=[('openrca-paper.pdf','https://netman.aiops.org/wp-content/uploads/2025/05/13411_OpenRCA_Can_Large_Langua.pdf'),('traintickettrace-conference.html','https://conf.researchr.org/details/saner-2026/saner-2026-workshops-tutorials-track/43/TrainTicketTrace-A-Multi-Fault-Distributed-Dataset-for-Microservice-Fault-Detection-')]
    for rid in [19513398,18342898,17811972,19335897,14938118,18937117]:initial.append((f'zenodo-{rid}-latest.json',f'https://zenodo.org/api/records/{rid}/versions/latest'))
    for repo,label in [('microsoft/OpenRCA','openrca'),('EvoTestOps/AnoMod','anomod')]:initial.append((label+'-commit.json','https://api.github.com/repos/'+repo+'/commits/main'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(lambda p:fetch(*p),initial))
    for repo,label in [('microsoft/OpenRCA','openrca'),('EvoTestOps/AnoMod','anomod')]:
        p=d/'sources'/(label+'-commit.json')
        if not p.exists():continue
        sha=json.loads(p.read_text())['sha'];fetch(label+'-tree.json',f'https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1')
        paths=['README.md','LICENSE','dataset/README.md','main/task_specification.json'] if label=='openrca' else ['README.md','LICENSE','SN_collection-scripts/README.md','TT_collection-scripts/T-Dataset/README.md','TT_collection-scripts/chaos-experiments/README.md']
        for f in paths:fetch(label+'-'+f.replace('/','__'),f'https://raw.githubusercontent.com/{repo}/{sha}/{f}')
    m={'scope':'official source/metadata only; telemetry bytes zero','run_id':a.run,'items':items,'elapsed_seconds':round(time.perf_counter()-began,3),'downloaded_bytes':sum(x.get('bytes',0) for x in items)}
    (d/'source-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'run_id':a.run,'source_count':len(items),'failed':sum(x['status']!='ok' for x in items),'bytes':m['downloaded_bytes'],'seconds':m['elapsed_seconds']}))

if __name__=='__main__':main()
