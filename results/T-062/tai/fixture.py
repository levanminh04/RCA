"""Read fixture IDs through APIs on load host. Never print credentials or response bodies."""
import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import uuid

ROOT = Path('/opt/rca-tai')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--machine', choices=['tai', 'obs'], default='tai')
    parser.add_argument('--create-if-empty', action='store_true')
    args = parser.parse_args()
    base = 'http://' + ('129.221.208.47' if args.machine == 'tai' else '10.0.0.158') + ':8081'
    token = json.loads((ROOT/'secret/tokens.json').read_text())['access_token']
    evidence = []
    def request(method, path, body=None, key=None):
        headers = {'Authorization': 'Bearer ' + token}
        if key: headers['Idempotency-Key'] = key
        data = None if body is None else json.dumps(body).encode()
        if data: headers['Content-Type'] = 'application/json'
        try:
            with urlopen(Request(base + path, data=data, headers=headers, method=method), timeout=35) as r:
                evidence.append({'method': method, 'path': path, 'status': r.status})
                value = json.load(r)
        except HTTPError as e:
            evidence.append({'method': method, 'path': path, 'status': e.code})
            raise RuntimeError(f'API status {e.code} at {method} {path}') from None
        return value.get('data', value) if isinstance(value, dict) else value
    def rows(value):
        if isinstance(value, list): return value
        for key in ['content', 'items', 'events', 'orders']:
            if isinstance(value, dict) and isinstance(value.get(key), list): return value[key]
        raise RuntimeError('Unrecognized list envelope')
    events = rows(request('GET', '/api/v1/events'))
    # OrderController has GET /{orderId}, but no GET collection endpoint.
    # Use retained candidate IDs and verify ownership via authenticated API reads.
    candidates = []
    for name in ['seed-orders.json', 'fixtures.json']:
        path = ROOT/'k6'/name
        if path.exists(): candidates.extend(json.loads(path.read_text()).get('orders', []))
    orders = []
    for candidate in {item['orderId'] for item in candidates}:
        try:
            orders.append(request('GET', '/api/v1/orders/' + candidate))
        except RuntimeError:
            if evidence[-1]['status'] not in [403, 404]: raise
    fixture = {'events': [{'eventId': e['eventId']} for e in events],
               'orders': [{'orderId': o['orderId']} for o in orders]}
    if not fixture['orders'] and args.create_if_empty:
        if not fixture['events']: raise RuntimeError('No event available')
        event = request('GET', '/api/v1/events/' + fixture['events'][0]['eventId'])
        ticket = event['ticketTypes'][0]['ticketTypeId']
        # Maximum one normal order. Retain idempotency key before the POST for recovery.
        key_path = ROOT/'k6/fixture-create.json'
        if key_path.exists():
            command = json.loads(key_path.read_text())
        else:
            command = {'key': str(uuid.uuid4()), 'body': {'eventId': event['eventId'],
                       'customerEmail': 'buyer@example.test', 'selection': {'mode': 'QUANTITY',
                       'items': [{'ticketTypeId': ticket, 'quantity': 1}]}}}
            key_path.write_text(json.dumps(command, indent=2) + '\n')
        order = request('POST', '/api/v1/orders', command['body'], command['key'])
        fixture['orders'].append({'orderId': order['orderId']})
    (ROOT/'k6/fixtures.json').write_text(json.dumps(fixture, indent=2) + '\n')
    for order in fixture['orders']:
        for suffix in ['', '/payment', '/tickets']:
            try:
                request('GET', '/api/v1/orders/' + order['orderId'] + suffix)
            except RuntimeError:
                if not suffix: raise
                # Keep valid owned order fixture and record dependent route errors.
                # These must remain visible in the 5-minute report, never relabeled as success.
                if not evidence or evidence[-1]['status'] < 400: raise
    (ROOT/'k6/fixture-evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({'events': len(fixture['events']), 'orders': len(fixture['orders']), 'requests': evidence}))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Exception text from HTTP can contain sensitive response fields: suppress it.
        print(json.dumps({'error_type': type(e).__name__, 'detail': str(e) if isinstance(e, RuntimeError) else 'Fixture operation failed; no secrets emitted'}))
        raise SystemExit(1)
