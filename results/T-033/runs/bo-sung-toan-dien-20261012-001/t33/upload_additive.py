"""Upload only new authorized workroot scripts, retaining every version."""
import pathlib,sys
from controller import OUT,REMOTE,call
tag=sys.argv[1];names=sys.argv[2:]
files={name:(OUT/name).read_bytes().hex() for name in names}
code='import pathlib\np=pathlib.Path('+repr(REMOTE)+')\nfiles='+repr(files)+'\nfor name,value in files.items():\n q=p/name\n assert not q.exists(),name\n q.write_bytes(bytes.fromhex(value))\nprint("uploaded",list(files))\n'
call(tag,'/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 -',code.encode())
