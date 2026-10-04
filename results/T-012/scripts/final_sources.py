"""Capture three already-listed leads only; documentation/metadata, no payload."""
import datetime,hashlib,json,time,urllib.request
from pathlib import Path
B=Path(__file__).resolve().parents[1]
R=B/'runs/run-003'
def main():
    R.mkdir(exist_ok=False); (R/'sources').mkdir(); start=time.monotonic(); items=[]
    for name,url in [('openrca-reuse-study.html','https://arxiv.org/html/2607.13548v1'),('cloud-agents-study.html','https://arxiv.org/html/2602.09937v1'),('famos-record.json','https://zenodo.org/api/records/13120167')]:
        x=dict(id=name,url=url,accessed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()); t=time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'T012-source-only'}),timeout=35) as f:
                raw=f.read(3_000_001)
                if len(raw)>3_000_000:raise ValueError('documentation limit')
                x['final_url']=f.geturl()
            p=R/'sources'/name;p.write_bytes(raw);x.update(status='ok',path=p.relative_to(B).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        except Exception as e:x.update(status='error',error=repr(e))
        x['elapsed_seconds']=round(time.monotonic()-t,3);items.append(x)
    (R/'source-manifest.json').write_text(json.dumps(dict(scope='previously listed documentation leads only; telemetry 0 bytes',items=items,downloaded_bytes=sum(x.get('bytes',0) for x in items),elapsed_seconds=round(time.monotonic()-start,3)),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(items,ensure_ascii=False))
if __name__=='__main__':main()
