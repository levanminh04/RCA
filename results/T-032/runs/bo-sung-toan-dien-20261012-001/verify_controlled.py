"""Check additive authority files against pre-package exact byte backups."""
import pathlib,json,hashlib,datetime,sys
P=pathlib.Path(__file__).parent;R=P.parents[3];backup=P/'control-before'
files=json.loads((P/'control-before.json').read_text(encoding='utf-8'));checks=[]
for old in files:
 rel=old['path'];before=(backup/rel).read_bytes();now=(R/rel).read_bytes()
 assert hashlib.sha256(before).hexdigest()==old['sha256']
 if rel=='docs/STATE.md':
  a=before.splitlines(keepends=True);b=now.splitlines(keepends=True);assert len(a)==len(b)
  diffs=[i for i,(u,v) in enumerate(zip(a,b)) if u!=v]
  assert len(diffs)==2,diffs
  assert {a[i].split(b'|')[1].strip() for i in diffs}=={b'T-032',b'T-033'}
  for i in diffs:
   assert a[i].endswith(b'\r\n')==b[i].endswith(b'\r\n')
   aa=a[i].split(b'|');bb=b[i].split(b'|');assert len(aa)==len(bb)
   assert all(x==y for j,(x,y) in enumerate(zip(aa,bb)) if j!=6),'non-status column changed'
  checks.append({'path':rel,'PASS':True,'changed_rows':['T-032','T-033'],'other_bytes_equal':True})
 else:
  assert now.startswith(before),'old bytes changed: '+rel
  checks.append({'path':rel,'PASS':True,'original_bytes':len(before),'appended_bytes':len(now)-len(before),'old_prefix_exact':True})
out={'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks}
f=P/(sys.argv[1] if len(sys.argv)>1 else 'controlled-verification-001.json');assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
