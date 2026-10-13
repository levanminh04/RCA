"""Laptop read-only projection of saved JSON/gzip, without research computation."""
import pathlib,sys,json,gzip
p=pathlib.Path(sys.argv[1]);b=p.read_bytes()
if p.suffix=='.gz':b=gzip.decompress(b)
x=json.loads(b.decode('utf-8-sig'))
for k in sys.argv[2].strip('/').split('/'):
 if k:x=x[int(k)] if isinstance(x,list) else x[k]
if sys.argv[3]=='slice':x=x[int(sys.argv[4]):int(sys.argv[5])];fields=sys.argv[6].split(',') if len(sys.argv)>6 else None
else:fields=sys.argv[3].split(',');x=[x]
for r in x:
 print(json.dumps({k:r[k] for k in fields if k in r} if fields else r,ensure_ascii=False,separators=(',',':')))
