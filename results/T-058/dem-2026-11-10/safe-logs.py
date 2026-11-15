#!/usr/bin/env python3
"""Read bounded diagnostics only after redacting provisioned credentials."""
import json
from pathlib import Path
import re
import subprocess
import sys

secrets=set()
files=list(Path('/opt/flash-ticket-app/env').glob('*.env'))+[Path('/opt/flash-ticket-src/.env'),Path('/opt/flash-ticket-app/collector/collector.env')]
for p in files:
    if not p.exists():
        continue
    for line in p.read_text().splitlines():
        if '=' not in line:
            continue
        k,v=line.split('=',1)
        if any(w in k for w in ['PASSWORD','SECRET','TOKEN','API_KEY']) and v:
            secrets.add(v)
        if k.endswith('MONGO_URI'):
            secrets.add(v)
for name in ['test-users.json','client-secrets.json']:
    p=Path('/opt/flash-ticket-app/env')/name
    if p.exists():
        obj=json.loads(p.read_text())
        if isinstance(obj,list):
            secrets.update(u['password'] for u in obj)
        else:
            secrets.update(obj.values())
name=sys.argv[1]
mode=sys.argv[2] if len(sys.argv)>2 else ''
args=['docker','logs','--tail','25000' if mode=='lettuce' else ('1500' if mode else '120'),name]
p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output=p.stdout
for value in sorted(secrets,key=len,reverse=True):
    output=output.replace(value,'<redacted>')
output=re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+','<redacted-jwt>',output)
lines=[]
for line in output.splitlines():
    try:
        item=json.loads(line)
        line=str(item.get('timestamp',''))+' '+str(item.get('severity',''))+' '+str(item.get('message',''))
        stack=item.get('stackTrace','')
        if stack:
            line+=' | '+ ' | '.join(s for s in stack.splitlines() if not s.startswith('\tat '))[:1200]
    except (ValueError,TypeError):
        pass
    lines.append(line[:1600])
if mode=='lettuce':
    lines=[line for line in lines if 'lettuce' in line.lower() or 'muzzle' in line.lower()]
print('\n'.join(lines[:100] if mode=='head' else lines[-65:])[-18000:])
