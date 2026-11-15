"""Read-only fixture discovery on exp-obs; stdout contains no credentials."""
import datetime
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

base = 'http://10.0.0.158:8081'
tokens = json.loads(Path('/opt/rca-tai/secret/tokens.json').read_text())
evidence = []

def get(route, authenticated=False):
    headers = {'Authorization': 'Bearer '+tokens['access_token']} if authenticated else {}
    try:
        with urlopen(Request(base+route, headers=headers), timeout=20) as r:
            body = json.load(r)
            evidence.append({'path': route, 'status': r.status})
            return body.get('data', body) if isinstance(body, dict) else body
    except HTTPError as e:
        evidence.append({'path': route, 'status': e.code})
        return None

try:
    listing = get('/api/v1/events')
    rows = listing.get('items', []) if isinstance(listing, dict) else listing
    events = []
    for event in (rows or [])[:3]:
        eid = event.get('eventId') or event.get('id')
        if not eid:
            continue
        details = get('/api/v1/events/'+eid)
        if details:
            events.append({'eventId': eid, 'ticketTypes': [
                {'ticketTypeId': x.get('ticketTypeId'), 'unitPrice': x.get('unitPrice')}
                for x in details.get('ticketTypes', [])]})
    # Candidate ID is a lookup key from a prior smoke receipt, not assumed valid.
    # OrderController has no buyer listing endpoint. Verify ownership through the API.
    orders = []
    for oid in ['b16ae2e8-3893-466d-94eb-08ace3a9ace2',
                '7106a688-f746-4f16-910b-d138dbdfbea7',
                'efdf1e2b-a04f-4197-81bb-3cba86eaba27']:
        order = get('/api/v1/orders/'+oid, True)
        if order:
            orders.append({'orderId': oid, 'state': order.get('state')})
            get('/api/v1/orders/'+oid+'/payment', True)
            get('/api/v1/orders/'+oid+'/tickets', True)
    print(json.dumps({'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      'events': events, 'orders': orders, 'checks': evidence}))
except Exception:
    raise SystemExit('Fixture discovery failed; no response bodies or credentials logged')
