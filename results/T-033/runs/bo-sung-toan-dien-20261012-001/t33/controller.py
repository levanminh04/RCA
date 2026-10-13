"""Transport only; log every call and preserve attempts."""
import pathlib,subprocess,time,json,datetime,hashlib,sys
ROOT=pathlib.Path('D:/RCA-flashticket');OUT=ROOT/'results/T-033/runs/bo-sung-toan-dien-20261012-001/t33'
REMOTE='/home/ubuntu/rca/T-033/runs/bo-sung-toan-dien-20261012-001/t33'
SSH=['ssh','-i','D:/RCA-ext/keys/keys.pem','-o','UserKnownHostsFile='+str(ROOT/'results/T-033/runs/prepare-001/known_hosts'),'-o','StrictHostKeyChecking=yes','-o','BatchMode=yes','-o','ConnectTimeout=20','ubuntu@3.107.246.249']
def call(name,cmd,data=None):
 t=time.perf_counter();p=subprocess.run(SSH+[cmd],input=data,capture_output=True)
 for suffix,value in [('stdout',p.stdout),('stderr',p.stderr)]:
  target=OUT/(name+'.'+suffix);assert not target.exists();target.write_bytes(value)
 (OUT/(name+'.timer.json')).write_text(json.dumps({'wall_s':time.perf_counter()-t,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd},indent=2))
 print(p.stdout.decode(errors='replace'));print(p.stderr.decode(errors='replace'));assert p.returncode==0
if __name__=='__main__':
 name=sys.argv[1]
 if name=='upload':
  catalog=(ROOT/'results/T-033/runs/session9-report-002/source-catalog.json').read_bytes(); files={f:(OUT/f).read_bytes().hex() for f in ['worker.py','design.md']};files['source-catalog.json']=catalog.hex()
  payload=('import pathlib,json\np=pathlib.Path('+repr(REMOTE)+');p.mkdir(parents=True,exist_ok=False)\nf='+repr(files)+'\nfor k,v in f.items():(p/k).write_bytes(bytes.fromhex(v))\nprint("uploaded",list(f))\n').encode()
  call('upload','/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 -',payload)
 elif name in ['pilot','engines']:
  cmd="cd "+REMOTE+" && nohup env PYTHONDONTWRITEBYTECODE=1 /home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 worker.py "+name+" >"+name+".stdout 2>"+name+".stderr < /dev/null &"
  call('launch-'+name,cmd)
 else:call(name,sys.argv[2])
