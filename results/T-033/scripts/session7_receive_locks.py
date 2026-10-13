"""Read-only receive of completed point/coverage locks after the storage stop."""
import pathlib,json,hashlib,base64
H=pathlib.Path('/home/ubuntu/rca/T-033')
run=H/'runs/session7-manual-001'
files={}
for name in ('points-lock.json','coverage-matching.json'):
    b=(run/name).read_bytes()
    files[name]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),
                 'base64':base64.b64encode(b).decode('ascii')}
print(json.dumps({'status':'READ_ONLY_RECEIVE','files':files}))
