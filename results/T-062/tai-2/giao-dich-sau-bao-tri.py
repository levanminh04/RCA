# Passed the pinned PKCE helper and api-lib in memory; no remote checkpoint writes.
key=str(uuid.uuid4())
eid='3e7c1df9-ada4-4081-94a1-548b80a5da86';tid='ffb36fc7-e30a-4efe-987f-ca5533520453'
record={'utcStart':dt.datetime.now(dt.timezone.utc).isoformat(),'states':[],'requests':evidence}
try:
    body={'eventId':eid,'customerEmail':'buyer@example.invalid','selection':{'mode':'QUANTITY','items':[{'ticketTypeId':tid,'quantity':1}]}}
    order=api('POST','/api/v1/orders','BUYER',body,key);record['orderId']=order['orderId']
    record['states'].append({'state':order['state'],'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    replay=api('POST','/api/v1/orders','BUYER',body,key)
    record['sameOrderOnReplay']=replay.get('orderId')==order['orderId']
    pay=api('POST','/api/v1/payments','BUYER',{'orderId':order['orderId']},str(uuid.uuid4()))
    record['attemptId']=pay.get('attemptId')
    if not pay.get('paymentUrl','').startswith('http://127.0.0.1:19090/checkout?'):raise ValueError('Mock URL missing')
    with urllib.request.urlopen(pay['paymentUrl'],timeout=35) as response:record['callback']={'httpStatus':response.code,'body':json.load(response)}
    for _ in range(60):
        current=api('GET',f"/api/v1/orders/{order['orderId']}",'BUYER');state=current.get('state')
        if record['states'][-1]['state']!=state:record['states'].append({'state':state,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
        if state in ['COMPLETED','ISSUANCE_FAILED','CANCELLED']:break
        time.sleep(1)
    record['tickets']=api('GET',f"/api/v1/orders/{order['orderId']}/tickets",'BUYER')
    record['payment']=api('GET',f"/api/v1/orders/{order['orderId']}/payment",'BUYER')
except Exception as error:record['failureType']=type(error).__name__
finally:
    record['utcEnd']=dt.datetime.now(dt.timezone.utc).isoformat();print(json.dumps(record))
