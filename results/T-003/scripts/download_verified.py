"""Download explicit plan, retain attempts, hash bytes, never open telemetry."""
import argparse, concurrent.futures, datetime, hashlib, json, time, urllib.request
from pathlib import Path

def fetch(item):
    start=time.monotonic(); dest=Path(args.data)/item['path']; dest.parent.mkdir(parents=True,exist_ok=True)
    row=dict(item,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        if dest.exists():
            row['reused']=True
        else:
            partial=dest.with_name(dest.name+'.part')
            if partial.exists():
                raise RuntimeError('prior partial preserved; requires new attempt name')
            with urllib.request.urlopen(urllib.request.Request(item['url'],headers={'User-Agent':'T003-dataset-audit'}),timeout=60) as response, partial.open('wb') as out:
                while True:
                    block=response.read(1024*1024)
                    if not block: break
                    out.write(block)
            partial.rename(dest)
        sha=hashlib.sha256(); blob=hashlib.sha1(f"blob {dest.stat().st_size}\0".encode())
        with dest.open('rb') as src:
            for block in iter(lambda:src.read(1024*1024),b''): sha.update(block); blob.update(block)
        row.update(actual_bytes=dest.stat().st_size,sha256=sha.hexdigest(),git_blob_sha=blob.hexdigest())
        if row['actual_bytes'] != item['bytes']: raise RuntimeError('byte mismatch')
        if item.get('git_blob_sha') and item['git_blob_sha']!=blob.hexdigest(): raise RuntimeError('git blob mismatch')
        row['status']='ok'
    except Exception as exc: row.update(status='error',error=str(exc))
    row['elapsed_seconds']=round(time.monotonic()-start,3)
    (run/(hashlib.sha256(item['path'].encode()).hexdigest()+'.json')).write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:row[k] for k in ['path','status','elapsed_seconds']}),flush=True)
    return row

parser=argparse.ArgumentParser(); parser.add_argument('--plan',required=True);parser.add_argument('--data',required=True);parser.add_argument('--results',required=True);parser.add_argument('--run',required=True);parser.add_argument('--workers',type=int,default=3)
args=parser.parse_args(); run=Path(args.results)/args.run;run.mkdir(parents=True,exist_ok=False)
plan=json.loads(Path(args.plan).read_text(encoding='utf-8'));(run/'plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
started=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool: rows=list(pool.map(fetch,plan))
(run/'manifest.json').write_text(json.dumps(dict(items=rows,elapsed_seconds=round(time.monotonic()-started,3),telemetry_rows_read=0),ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if all(x['status']=='ok' for x in rows) else 1)
