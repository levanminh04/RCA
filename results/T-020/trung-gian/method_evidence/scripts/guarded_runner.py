"""Read-only old artifacts; interpreter audit hook forbids every outside write."""
import os,sys,runpy
from pathlib import Path
ALLOWED=Path('D:/RCA-flashticket/results/T-020/trung-gian/method_evidence').resolve()
def guarded_path(path):
    if isinstance(path,int):return
    p=Path(os.fsdecode(path)).resolve()
    if p!=ALLOWED and ALLOWED not in p.parents:raise PermissionError('T020 write guard: '+str(p))
def audit(event,args):
    if event=='open':
        path,mode,flags=args
        if (mode and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):guarded_path(path)
    elif event in ('os.mkdir','os.remove','os.rmdir','os.chmod','os.utime','os.truncate'):
        guarded_path(args[0])
    elif event in ('os.rename','os.replace','os.link','os.symlink'):
        guarded_path(args[0]);guarded_path(args[1])
sys.addaudithook(audit)
script=sys.argv[1];sys.argv=sys.argv[1:]
runpy.run_path(script,run_name='__main__')
