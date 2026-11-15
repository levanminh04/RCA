import subprocess,json
oid='2f6c01b2-ab05-49d5-affc-3c0bbafb67a2'
for svc in ['booking','payment','ticket','api-gateway']:
    n=f'flash-ticket-{svc if svc=="api-gateway" else svc+"-service"}-{svc if svc=="api-gateway" else svc+"-service"}-1'
    r=subprocess.run(['sudo','-n','docker','logs','--since','2026-11-12T22:17:30Z','--until','2026-11-12T22:18:45Z',n],capture_output=True,text=True)
    found=[]
    for line in (r.stdout+'\n'+r.stderr).splitlines():
        try: v=json.loads(line)
        except ValueError: continue
        if oid in line or (svc=='api-gateway' and len(found)<3):
            safe={k:x for k,x in v.items() if k not in ['stackTrace','url','query','requestBody','responseBody']}
            found.append(safe)
    print(json.dumps({'service':svc,'exit':r.returncode,'logs':found}))
print(json.dumps({'mockAudit':[json.loads(l) for l in open('/opt/flash-ticket-app/l1-vnpay/audit.jsonl')]}))
