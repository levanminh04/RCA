import os
root=ROOT/'l1-fixtures'
fixture=json.loads((root/'events.json').read_text())['public']
eid=fixture['eventId']; tid=fixture['ticketTypes'][0]['ticketTypeId']
target=root/('transaction-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json')
record={'utcStart':dt.datetime.now(dt.timezone.utc).isoformat(),'eventId':eid,'states':[],'requests':evidence}
def save():
    target.write_text(json.dumps(record)); os.chmod(target,0o600)
body={'eventId':eid,'customerEmail':'buyer@example.invalid','selection':{'mode':'QUANTITY','items':[{'ticketTypeId':tid,'quantity':1}]}}
try:
    api('GET','/api/v1/events')
    api('GET',f'/api/v1/events/{eid}')
    api('GET',f'/api/v1/events/{eid}/availability')
    key=str(uuid.uuid4())
    previous=sorted(root.glob('transaction-*.json'))
    prior=json.loads(previous[-1].read_text()) if previous else {}
    if prior.get('failureType') and prior.get('paymentStatus')==503:
        order=api('GET',f"/api/v1/orders/{prior['orderId']}",'BUYER')
        record['resumedFrom']=str(previous[-1])
    else:
        order=api('POST','/api/v1/orders','BUYER',body,key)
    record['orderId']=order['orderId']; record['states'].append({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'state':order['state']}); save()
    if not record.get('resumedFrom'):
        replay=api('POST','/api/v1/orders','BUYER',body,key)
        record['sameOrderOnReplay']=replay.get('orderId')==order['orderId']; save()
    pay=api('POST','/api/v1/payments','BUYER',{'orderId':order['orderId']},str(uuid.uuid4()))
    record['paymentStatus']=evidence[-1]['status']; record['attemptId']=pay.get('attemptId'); save()
    if not pay.get('paymentUrl','').startswith('http://127.0.0.1:19090/checkout?'):
        raise ValueError('Mock payment URL missing')
    try:
        with urllib.request.urlopen(pay['paymentUrl'],timeout=35) as r:
            record['mock']={'status':r.code,'body':json.load(r)}
    except urllib.error.HTTPError as r:
        record['mock']={'status':r.code,'body':json.load(r)}
    save()
    for _ in range(90):
        current=api('GET',f"/api/v1/orders/{order['orderId']}",'BUYER')
        state=current.get('state')
        if not record['states'] or record['states'][-1]['state']!=state:
            record['states'].append({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'state':state}); save()
        if state in ['COMPLETED','ISSUANCE_FAILED','CANCELLED']:
            break
        time.sleep(1)
    record['tickets']=api('GET',f"/api/v1/orders/{order['orderId']}/tickets",'BUYER'); save()
    record['payment']=api('GET',f"/api/v1/orders/{order['orderId']}/payment",'BUYER'); save()
    for kind in ['cancel','abandon']:
        other=api('POST','/api/v1/orders','BUYER',body,str(uuid.uuid4()))
        record[kind]={'orderId':other.get('orderId'),'state':other.get('state'),'expiresAt':other.get('expiresAt')}; save()
        if kind=='cancel' and 'orderId' in other:
            canceled=api('POST',f"/api/v1/orders/{other['orderId']}/cancel",'BUYER',{})
            record[kind]['finalState']=canceled.get('state'); save()
except Exception as error:
    record['failureType']=type(error).__name__
finally:
    record['utcEnd']=dt.datetime.now(dt.timezone.utc).isoformat(); save()
    print(json.dumps(record))
