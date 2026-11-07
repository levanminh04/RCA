"""Kiểm kê chỉ đọc; không đọc telemetry hoặc nội dung khóa SSH."""
from pathlib import Path
import concurrent.futures,json,subprocess,time,hashlib
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
REMOTE=r'''
import os,json,shutil,subprocess,glob,platform
from pathlib import Path
base=Path('/home/ubuntu')
out={'hostname':platform.node(),'platform':platform.platform(),'cpu':os.cpu_count(),
     'meminfo':{x.split(':')[0]:x.split(':')[1].strip() for x in Path('/proc/meminfo').read_text().splitlines() if x.split(':')[0] in ['MemTotal','MemAvailable','SwapTotal','SwapFree']},
     'disk':dict(zip(['total','used','free'],shutil.disk_usage(base))),
     'top_directories':[p.name for p in base.iterdir()if p.is_dir()],
     'environment_bins':sorted(set(glob.glob('/home/ubuntu/rca/**/bin/python',recursive=True)+glob.glob('/home/ubuntu/rca-t053/**/bin/python',recursive=True))),
     'running':subprocess.run(['ps','-eo','pid,comm,%cpu,%mem'],capture_output=True,text=True).stdout}
r=subprocess.run(['du','-x','-B1','--max-depth=2',str(base)],capture_output=True,text=True,timeout=90)
out['directory_usage']=r.stdout;out['du_stderr']=r.stderr
print(json.dumps(out))
'''
HOSTS=[{'name':'ec2_1','ip':'13.211.127.97','key':'D:/RCA-ext/keys/keys.pem','alias':'3.107.246.249',
        'known':'D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts'},
       {'name':'ec2_2','ip':'3.107.156.186','key':'D:/RCA-ext/keys/key2.pem','alias':'3.26.62.217'}]
def ssh_args(h):
    a=['ssh','-i',h['key'],'-o','HostKeyAlias='+h['alias'],'-o','StrictHostKeyChecking=yes',
       '-o','UpdateHostKeys=no','-o','BatchMode=yes','-o','ConnectTimeout=12','-o','ServerAliveInterval=15']
    if h.get('known'):a+=['-o','UserKnownHostsFile='+h['known']]
    return a+['ubuntu@'+h['ip']]
def remote(h):
    start=time.monotonic()
    try:
        r=subprocess.run(ssh_args(h)+['python3 -'],input=REMOTE,text=True,encoding='utf-8',capture_output=True,timeout=110)
        result={'host':h['name'],'ip':h['ip'],'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_s':time.monotonic()-start}
    except subprocess.TimeoutExpired as e:
        result={'host':h['name'],'ip':h['ip'],'error':'SSH_TIMEOUT','elapsed_s':time.monotonic()-start}
    (RUN/(h['name']+'-inventory.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result
def local():
    base=ROOT/'data/locked/rcaeval-re2tt-60'
    rows=[]
    for p in sorted(base.rglob('*')):
        if p.is_file():
            sha=hashlib.sha256()
            with p.open('rb')as f:
                for b in iter(lambda:f.read(1024*1024),b''):sha.update(b)
            rows.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha.hexdigest()})
    result={'scope':'metadata/opaque file hashing only, no values/schema/labels opened','files':rows,
      'case_directories':len([p for p in base.iterdir()if p.is_dir()]),'file_count':len(rows),
      'bytes':sum(x['bytes']for x in rows)}
    (RUN/'local-TT60-inventory.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return {k:v for k,v in result.items()if k!='files'}
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        fs=[pool.submit(remote,h)for h in HOSTS]+[pool.submit(local)]
        for f in concurrent.futures.as_completed(fs):
            r=f.result();print(json.dumps({k:v for k,v in r.items()if k not in ['stdout','files']},ensure_ascii=False),flush=True)
