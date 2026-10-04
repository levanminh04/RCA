"""One full default-PC repeat with a column permutation and own-task waiting."""
from pathlib import Path
p=Path('D:/RCA-flashticket/results/T-014/scripts/ec2_run.py');code=p.read_text()
code=code.replace("out=base/'runs/default-pc'","out=base/'runs/default-pc-permuted'")
old="clean=preprocess(win.copy(),dataset='re2-tt');names=list(clean.columns);clean['time']=win.time"
assert code.count(old)==1
code=code.replace(old,"clean=preprocess(win.copy(),dataset='re2-tt');clean=clean.loc[:,list(reversed(clean.columns))];names=list(clean.columns);clean['time']=win.time")
needle='    start=time.monotonic()\n    child=subprocess.Popen'
assert code.count(needle)==1
wait='''    start=time.monotonic()
    import psutil
    while True:
        others=[]
        for q in psutil.process_iter(['pid','name','cmdline']):
            command=' '.join(q.info['cmdline'] or [])
            if q.pid!=os.getpid() and q.info['name'].startswith(('python','Rscript','R')) and 'T-014' not in command:
                others.append(dict(pid=q.pid,command=command))
        elapsed=time.monotonic()-start
        available=psutil.virtual_memory().available
        emit(out/'queue.jsonl',dict(event='wait_own_task',elapsed=elapsed,other_jobs=others,available_bytes=available,wall_wait_counts_in_budget=True))
        if elapsed>=a.timeout:
            (out/'status.json').write_text(json.dumps(dict(complete=False,reason='shared-machine wait consumed predeclared remaining budget',elapsed=elapsed,timeout=a.timeout,official_runtime=False),indent=2))
            sys.exit(0)
        if not others and available>6*1024**3:break
        time.sleep(30)
    child=subprocess.Popen'''
code=code.replace(needle,wait)
Path('D:/RCA-flashticket/results/T-014/scripts/ec2_repeat.py').write_text(code)
print('Prepared full default-PC column-permutation repeat; no scientific PC overrides')
