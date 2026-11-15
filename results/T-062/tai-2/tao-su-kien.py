import hashlib,os
root=ROOT/'l1-fixtures'; os.umask(0o077); root.mkdir(mode=0o700,exist_ok=True)
target=root/'events.json'
if target.exists():
    raise SystemExit('Event checkpoint exists; inspect and reuse')
categories=api('GET','/api/v1/categories'); venues=api('GET','/api/v1/venues')
print(json.dumps({'categories':categories,'venues':venues}))
now=dt.datetime.now(dt.timezone.utc)
stamp=lambda d:d.isoformat().replace('+00:00','Z')
draft={'title':'Public concert','description':'Synthetic event for isolated transaction verification',
    'categoryId':categories[0]['id'],'venueId':venues[0]['id'],'mode':'QUANTITY',
    'startsAt':stamp(now+dt.timedelta(days=7)),'endsAt':stamp(now+dt.timedelta(days=8)),
    'saleStartsAt':stamp(now-dt.timedelta(days=1)),'saleEndsAt':stamp(now+dt.timedelta(days=6)),
    'purchaseLimit':100000,'images':[],'ticketTypes':[{'ticketTypeId':None,'name':'General',
    'unitPrice':'20000','currency':'VND','configuredQuantity':'100000','colorCode':'#336699'}],
    'promotions':[]}
event=api('POST','/api/v1/organizer/events','ORGANIZER',draft)
check={'event':event,'requests':evidence}
target.write_text(json.dumps(check)); print(json.dumps(check))
eid=event['eventId']
for action,role,extra in [('submit','ORGANIZER',{}),('approve','ADMIN',{'feeRate':'0.05'}),('publish','ORGANIZER',{})]:
    prefix='admin' if role=='ADMIN' else 'organizer'
    event=api('POST',f'/api/v1/{prefix}/events/{eid}/{action}',role,{'rowVersion':event['rowVersion'],**extra})
    check={'event':event,'requests':evidence}; target.write_text(json.dumps(check))
    if evidence[-1]['status']>=400:
        print(json.dumps(check)); raise SystemExit('Event transition failed; checkpoint retained')
public=api('GET',f'/api/v1/events/{eid}')
for i in range(30):
    available=api('GET',f'/api/v1/events/{eid}/availability')
    if any(int(t.get('available',0))>0 for t in available.get('ticketTypes',[])):
        break
    time.sleep(1)
check={'event':event,'public':public,'availability':available,'requests':evidence}
target.write_text(json.dumps(check)); print(json.dumps(check))
