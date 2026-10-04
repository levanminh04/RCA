"""Reproduce metadata-only Bank label census; never inflate telemetry members."""
import argparse, collections, csv, datetime, hashlib, io, json, struct, urllib.request, zlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args();o=B/'runs'/a.run;o.mkdir(exist_ok=False)
    previous=B/'runs/bank-metadata-001';meta=json.loads((previous/'summary.json').read_text());members=json.loads((previous/'zip-members.json').read_text());label=next(m for m in members if m['name']=='Bank/record.csv')
    url='https://drive.usercontent.google.com/download?id='+meta['bank']['id']+'&export=download&confirm=t';requests=[]
    def read_range(start,n):
        end=start+n-1
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'T003-metadata-only','Range':f'bytes={start}-{end}'}),timeout=60) as f:
            expected=f'bytes {start}-{end}/{meta["bank"]["bytes"]}'
            if f.status!=206 or f.headers.get('Content-Range')!=expected:raise ValueError('exact range not honored; binary body not read')
            b=f.read(n+1)
            if len(b)!=n:raise ValueError('size mismatch')
            requests.append(dict(start=start,end=end,bytes=n,content_range=expected,last_modified=f.headers.get('Last-Modified')));return b
    h=struct.unpack('<4s5H3L2H',read_range(label['local_header_offset'],30));assert h[0]==b'PK\x03\x04' and h[3]==8
    b=read_range(label['local_header_offset']+30,h[-2]+h[-1]+label['compressed_bytes']);assert b[:h[-2]].decode()=='Bank/record.csv'
    raw=zlib.decompress(b[h[-2]+h[-1]:],-15);assert len(raw)==label['bytes'] and zlib.crc32(raw)==label['crc32']
    (o/'record.csv').write_bytes(raw);rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))));print('label columns',list(rows[0]))
    # Match the official column names, not guessed service names.
    roots=collections.Counter(r['component'] for r in rows);reasons=collections.Counter(r['reason'] for r in rows);cells=collections.Counter((r['component'],r['reason'],r['datetime'][:10]) for r in rows)
    check=all(float(r['timestamp'])==datetime.datetime.fromisoformat(r['datetime']).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))).timestamp() for r in rows)
    result=dict(events=len(rows),roots=len(roots),reasons=len(reasons),days=len({r['datetime'][:10] for r in rows}),root_reason_cells=len({(x[0],x[1]) for x in cells}),root_counts=dict(roots),reason_counts=dict(reasons),root_reason_date=[dict(root=k[0],reason=k[1],date=k[2],count=v) for k,v in sorted(cells.items())],timestamp_matches_utc8=check,record_sha256=hashlib.sha256(raw).hexdigest(),record_crc_verified=True,requests=requests,telemetry_values_read=False,predictions_read=False)
    (o/'census.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
