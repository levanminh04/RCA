"""Start detached workroot process without inheriting SSH channels."""
import sys
from controller import call,REMOTE
tag=sys.argv[1];script=sys.argv[2];args=sys.argv[3:]
code='import pathlib,subprocess,sys\np=pathlib.Path('+repr(REMOTE)+')\na=(p/'+repr(tag+'.stdout')+').open("x");b=(p/'+repr(tag+'.stderr')+').open("x")\nq=subprocess.Popen([sys.executable,"-B","-X","utf8",str(p/'+repr(script)+')]+ '+repr(args)+',stdout=a,stderr=b,start_new_session=True,cwd=p)\n(p/'+repr(tag+'.pid')+').write_text(str(q.pid))\nprint(q.pid)\n'
call(tag+'-launch','/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 -',code.encode())
