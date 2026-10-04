"""Wall-clock budget guard; terminate only the task's exact local PC worker."""
import time,json,os,psutil
from pathlib import Path
out=Path('D:/RCA-flashticket/results/T-014/runs/pc-depth0-alpha005')
deadline=2700
while not (out/'status.json').exists() and not (out/'error.json').exists():
    lines=(out/'progress.jsonl').read_text().splitlines()
    last=json.loads(lines[-1])
    if last['elapsed']<deadline:
        time.sleep(min(15,deadline-last['elapsed']));continue
    targets=[]
    for p in psutil.process_iter(['pid','name','cmdline']):
        args=p.info['cmdline'] or []
        if p.pid==os.getpid() or p.info['name'].lower()!='python.exe':continue
        if not any(Path(a).name=='pc_prefix.py' for a in args):continue
        if '--run' not in args or args[args.index('--run')+1]!='pc-depth0-alpha005':continue
        targets.append(dict(pid=p.pid,command=args));p.terminate()
    (out/'status.json').write_text(json.dumps(dict(complete=False,reason='predeclared 45min diagnostic-PC budget; exact own worker only',deadline=deadline,last_progress=last,terminated=targets,official_runtime=False),indent=2))
    print(json.dumps(dict(deadline=deadline,last_progress=last,terminated=targets)))
    break
