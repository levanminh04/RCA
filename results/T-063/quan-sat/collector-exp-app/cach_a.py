# -*- coding: utf-8 -*-
"""T-063 — biến đổi cấu hình Collector `exp-app` sang cách A (KP-19) + đầu dò hộp đen + lọc health theo đường dẫn.
Chạy TRÊN exp-app: `python3 - < cach_a.py` trong /opt/flash-ticket-app/collector. Đọc config.json, ghi config.new.json.
Không in nội dung cấu hình (có tham chiếu biến bí mật); chỉ in tóm tắt thay đổi.

1. Bỏ 8 receiver `filelog/<svc>` ghim ID container; thêm `filelog/docker` đọc mọi file json-file của Docker. Mỗi dòng phải
   mang `attrs["com.docker.compose.service"]` (Docker json-file `labels` option) — dòng không có nhãn bị bỏ (collector,
   toxiproxy, container lạ). service.name ← nhãn service; service.instance.id ← service + "-" + container-number (giữ nghĩa
   cũ "<svc>-1"). Giữ parser JSON B16 (`attributes.app`) như cũ. Hạ tầng (postgres, redis, rabbitmq, user-db) vào cùng đường.
2. Receiver `httpcheck` (10 s) gọi liveness của 7 service Java + Keycloak; vào pipeline metrics.
3. `filter/health` (traces): thêm điều kiện theo `url.path` bắt đầu bằng /actuator/health (span SERVER của đầu dò).
"""
import json

d = json.load(open('config.json'))
r = d['receivers']
cu = sorted(k for k in r if k.startswith('filelog/'))
for k in cu:
    del r[k]
r['filelog/docker'] = {
    'include': ['/var/lib/docker/containers/*/*-json.log', '/var/lib/docker/containers/*/*-json.log.*'],
    'start_at': 'end', 'storage': 'file_storage', 'include_file_path': True,
    'operators': [
        {'type': 'json_parser', 'id': 'docker', 'parse_to': 'attributes.docker',
         'timestamp': {'parse_from': 'attributes.docker.time', 'layout_type': 'gotime',
                       'layout': '2006-01-02T15:04:05.999999999Z07:00'}},
        {'type': 'filter', 'id': 'bo-khong-nhan',
         'expr': 'attributes.docker.attrs == nil || attributes.docker.attrs["com.docker.compose.service"] == nil'},
        {'type': 'move', 'from': 'attributes.docker.log', 'to': 'body'},
        {'type': 'add', 'field': 'resource["service.instance.id"]',
         'value': 'EXPR(attributes.docker.attrs["com.docker.compose.service"] + "-" + '
                  '(attributes.docker.attrs["com.docker.compose.container-number"] ?? "1"))'},
        {'type': 'move', 'from': 'attributes.docker.attrs["com.docker.compose.service"]', 'to': 'resource["service.name"]'},
        {'type': 'json_parser', 'id': 'spring', 'parse_from': 'body', 'parse_to': 'attributes.app',
         'if': 'body matches "^\\\\s*\\\\{"', 'on_error': 'send'},
    ]}
DICH = {'api-gateway': 'http://10.0.0.158:8081', 'booking-service': 'http://127.0.0.1:8082',
        'payment-service': 'http://127.0.0.1:8083', 'ticket-service': 'http://127.0.0.1:8084',
        'user-service': 'http://127.0.0.1:8085', 'event-service': 'http://127.0.0.1:8086',
        'discovery-server': 'http://127.0.0.1:8761'}
r['httpcheck'] = {'collection_interval': '10s',
                  'targets': [{'endpoint': u + '/actuator/health/liveness', 'method': 'GET'} for u in DICH.values()]
                  + [{'endpoint': 'http://10.0.0.158:8080/realms/master', 'method': 'GET'}]}
p = d['service']['pipelines']
p['logs']['receivers'] = [x for x in p['logs']['receivers'] if not x.startswith('filelog/')] + ['filelog/docker']
if 'httpcheck' not in p['metrics']['receivers']:
    p['metrics']['receivers'].append('httpcheck')
f = d['processors']['filter/health']['traces']['span']
dk = 'IsMatch(attributes["url.path"], "^/actuator/health")'
if dk not in f:
    f.append(dk)
json.dump(d, open('config.new.json', 'w'), indent=2)
print(json.dumps({'bo_receiver': cu, 'them': ['filelog/docker', 'httpcheck'], 'httpcheck_targets': len(r['httpcheck']['targets']),
                  'filter_health': len(f), 'logs_receivers': p['logs']['receivers'], 'metrics_receivers': p['metrics']['receivers']}))
