"""Small result receipt; immutable files only, verify hash two endpoints."""
import datetime,hashlib,json,pathlib,subprocess,sys,time
from controller import OUT,REMOTE,SSH
names=sys.argv[2:];tag=sys.argv[1]
code='import pathlib,json,hashlib\np=pathlib.Path('+repr(REMOTE)+')\nnames='+repr(names)+'\nout={}\nfor name in names:\n q=p/name\n if q.is_file():\n  b=q.read_bytes();out[name]={"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"hex":b.hex()}\nprint(json.dumps(out))\n'
t=time.perf_counter();p=subprocess.run(SSH+['/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 -'],input=code.encode(),capture_output=True)
(OUT/(tag+'.stdout')).write_bytes(p.stdout);(OUT/(tag+'.stderr')).write_bytes(p.stderr);assert p.returncode==0,p.stderr
result=json.loads(p.stdout);receipt={}
for name,m in result.items():
 b=bytes.fromhex(m['hex']);assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'];q=OUT/name
 if q.exists():assert q.read_bytes()==b,name
 else:q.write_bytes(b)
 receipt[name]={'sha256':m['sha256'],'bytes':m['bytes'],'received_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(OUT/(tag+'.receipt.json')).write_text(json.dumps({'files':receipt,'wall_s':time.perf_counter()-t,'exit':p.returncode},indent=2));print('received',len(receipt),'files',sum(x['bytes'] for x in receipt.values()),'bytes')
