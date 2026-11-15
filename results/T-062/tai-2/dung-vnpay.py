# Files are supplied as base64 by dung-vnpay.ps1. No secret is supplied by the laptop.
import base64,hashlib,json,os,secrets,subprocess,time
from pathlib import Path
root=Path('/opt/flash-ticket-app/l1-vnpay')
os.umask(0o077)
root.mkdir(mode=0o700,exist_ok=True)
report={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'files':[]}
for name,b64 in FILES.items():
    p=root/name
    before=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    p.write_bytes(base64.b64decode(b64))
    report['files'].append({'path':str(p),'before':before,'after':hashlib.sha256(p.read_bytes()).hexdigest()})
secret=root/'mock.env'
if not secret.exists():
    secret.write_text('VNPAY_TMN_CODE=BI_TEST\nVNPAY_HASH_SECRET='+secrets.token_urlsafe(48)+'\n')
e=dict(l.split('=',1) for l in secret.read_text().splitlines() if l)
payment=Path('/opt/flash-ticket-app/env-t062/payment-service.env')
backup=root/'payment-service.env.before'
if backup.exists():
    raise SystemExit('Payment backup already exists: inspect before reapplying')
before=hashlib.sha256(payment.read_bytes()).hexdigest()
backup.write_bytes(payment.read_bytes()); os.chmod(backup,0o600)
replace={**e,'VNPAY_API_URL':'http://127.0.0.1:19090/transaction',
    'VNPAY_PAYMENT_URL':'http://127.0.0.1:19090/checkout',
    'VNPAY_RETURN_URL':'http://127.0.0.1:8083/api/v1/payments/vnpay/return',
    'VNPAY_IPN_URL':'http://127.0.0.1:8083/api/v1/payments/vnpay/ipn',
    'VNPAY_APP_RETURN_URL':'flash-ticket://payment-return'}
lines=payment.read_text().splitlines(); old_keys={l.split('=',1)[0] for l in lines if '=' in l}
lines=[k+'='+replace[k] if (k:=l.split('=',1)[0]) in replace else l for l in lines]
lines += [k+'='+v for k,v in replace.items() if k not in old_keys]
payment.write_text('\n'.join(lines)+'\n')
report['files'].append({'path':str(payment),'before':before,'after':hashlib.sha256(payment.read_bytes()).hexdigest(),'changedKeys':list(replace),'backup':str(backup)})
log=(root/'process.log').open('ab',buffering=0)
process=subprocess.Popen(['python3',str(root/'mock-runner.py')],cwd=root,
    env={**os.environ,'FT_TEST_ENVIRONMENT':'true'},stdout=log,stderr=log,start_new_session=True)
(root/'pid').write_text(str(process.pid)+'\n')
time.sleep(1)
if process.poll() is not None:
    raise SystemExit('Mock exited; inspect process log without exposing environment')
report['mockPid']=process.pid
n='flash-ticket-payment-service-payment-service-1'
d=json.loads(subprocess.check_output(['sudo','-n','docker','inspect',n],text=True))[0]
report['paymentBefore']={'id':d['Id'],'image':d['Image']}
r=subprocess.run(['sudo','-n','env','IMAGE='+d['Config']['Image'],'docker','compose',
    '-p','flash-ticket-payment-service','-f','/opt/flash-ticket-app/compose-t062/payment-service.yml',
    'up','-d','--no-deps','--force-recreate','payment-service'],capture_output=True,text=True)
report['composeExit']=r.returncode
if r.returncode:
    report['composeStderr']=r.stderr[-2000:]
new=json.loads(subprocess.check_output(['sudo','-n','docker','inspect',n],text=True))[0]
report['paymentAfter']={'id':new['Id'],'image':new['Image']}
report['rollback']='Restore payment-service.env.before to env-t062/payment-service.env and recreate ONLY payment-service using retained image; stop mock PID after verifying command line. Retain all state/audit.'
print(json.dumps(report))
raise SystemExit(r.returncode)
