#!/usr/bin/env python3
"""T-067 bước 7, phân tích bổ sung (sau khi chạy bộ kiểm đã khai trước; báo riêng, không thay tiêu chí).

1. Cặp RabbitMQ "đúng bản tin" của một đơn: với mỗi cặp khai ở cap-rabbitmq.json, lấy dòng log
   `<svc>.message.processed` của service nhận có correlationId = đơn; spanId của dòng đó phải là span CONSUMER
   (queue khai trước) và parent của nó là span PRODUCER của service phát với routing key khai trước.
2. Dòng log gateway không khớp span: đếm theo eventName, httpStatus, routeId, có traceId hay không, trace có tồn tại không.
Chạy trên exp-obs qua stdin (không ghi file): ssh exp-obs "python3 - <start> <end> <orderId>" < phan_tich_bo_sung.py
Cặp khai trước nhúng sẵn ở CAP bên dưới (chép từ tests/signals/cap-rabbitmq.json, lab 862b208).
"""
import base64, collections, json, sys, urllib.parse, urllib.request

T, L = 'http://127.0.0.1:3200', 'http://127.0.0.1:3100'
start, end, don = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
CAP = [('P1', 'payment-service', 'booking.accept-payment.v1', 'booking.accept-payment.q', 'booking-service'),
       ('P2', 'booking-service', 'booking.payment-decision.v1', 'payment.decision.q', 'payment-service'),
       ('P3', 'payment-service', 'ticket.issue.v1', 'ticket.issuance.q', 'ticket-service'),
       ('P4', 'ticket-service', 'ticket.issuance-result.v1', 'payment.ticket-issuance-failed.q', 'payment-service'),
       ('P5', 'payment-service', 'ticket.issued.v1', 'booking.tickets-issued.q', 'booking-service'),
       ('P6', 'booking-service', 'booking.order-completed.v1', 'payment.order-completed.q', 'payment-service')]


def get(u):
    try:
        return json.load(urllib.request.urlopen(u, timeout=60))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def h(v):
    if not v:
        return None
    return v if len(v) in (16, 32) and all(c in '0123456789abcdef' for c in v) else base64.b64decode(v).hex()


cache = {}


def trace(tid):
    if tid not in cache:
        d, sp = get(T + '/api/traces/' + tid), {}
        for b in (d or {}).get('batches', []):
            svc = next((a['value'].get('stringValue') for a in b['resource']['attributes'] if a['key'] == 'service.name'), None)
            for ss in b.get('scopeSpans', []):
                for s in ss['spans']:
                    at = {a['key']: list(a['value'].values())[0] if a['value'] else None for a in s.get('attributes', [])}
                    sp[h(s['spanId'])] = {'service': svc, 'kind': s.get('kind'), 'parent': h(s.get('parentSpanId')), 'at': at}
        cache[tid] = sp
    return cache[tid]


def loki(q):
    out = []
    for t0 in range(start, end, 120):
        u = L + '/loki/api/v1/query_range?' + urllib.parse.urlencode(
            {'query': q, 'start': t0 * 10**9, 'end': min(t0 + 120, end) * 10**9, 'limit': 5000, 'direction': 'forward'})
        for st in get(u)['data']['result']:
            out += [(st['stream'], l) for _, l in st['values']]
    return out


r = {'don': don, 'cap_dung_ban_tin': {}}
rows = loki(f'{{service_name=~".+"}} | app_correlationId="{don}"')
for pid, phat, rk, q, nhan in CAP:
    ev = nhan.split('-')[0] + '.message.processed'
    lines = [json.loads(l) for st, l in rows if st.get('service_name') == nhan and l.startswith('{')
             and json.loads(l).get('eventName') == ev]
    kq = []
    for j in lines:
        sp = trace(j['traceId'])
        c, buoc = sp.get(j['spanId']), 0
        while c and c['kind'] != 'SPAN_KIND_CONSUMER' and buoc < 10:  # dòng log có thể nằm ở span con
            c, buoc = sp.get(c['parent']), buoc + 1
        p = sp.get(c['parent']) if c else None
        kq.append({'messageId': j.get('messageId'), 'trace': j['traceId'], 'consumer_span': j['spanId'],
                   'consumer_ok': bool(c and c['kind'] == 'SPAN_KIND_CONSUMER' and c['service'] == nhan
                                       and (c['at'].get('rabbitmq.queue') or c['at'].get('messaging.destination.name')) == q),
                   'consumer_queue': c and (c['at'].get('rabbitmq.queue') or c['at'].get('messaging.destination.name')),
                   'producer_ok': bool(p and p['kind'] == 'SPAN_KIND_PRODUCER' and p['service'] == phat
                                       and p['at'].get('messaging.rabbitmq.destination.routing_key') == rk)})
    dat = [x for x in kq if x['consumer_ok'] and x['producer_ok']]
    r['cap_dung_ban_tin'][pid] = {'ket_qua': 'dat' if dat else 'khong_dat', 'so_dong_log_nhan': len(lines),
                                 'so_cap_dung': len(dat), 'chi_tiet': kq}

g = collections.Counter()
for st, l in loki('{service_name="api-gateway"} | app_eventName=~`gateway\\.request\\..*`'):
    j = json.loads(l)
    sp = trace(j['traceId']) if j.get('traceId') else {}
    if sum(1 for k, s in sp.items() if k == j.get('spanId') and s['service'] == 'api-gateway') == 1:
        continue
    g[(j.get('eventName'), j.get('httpStatus'), j.get('routeId'), bool(j.get('traceId')), bool(sp),
       j.get('spanId') in sp)] += 1
r['gateway_khong_khop'] = [{'eventName': k[0], 'httpStatus': k[1], 'routeId': k[2], 'co_traceId': k[3],
                           'trace_ton_tai': k[4], 'spanId_co_trong_trace': k[5], 'so_dong': n} for k, n in g.most_common()]
print(json.dumps(r, ensure_ascii=False, indent=1))
