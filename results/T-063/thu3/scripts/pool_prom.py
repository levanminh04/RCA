# -*- coding: utf-8 -*-
"""T-063 thu3 — đọc chuỗi pool Event + 5xx Event trên Prometheus exp-obs (query_range bước 15 s, chỉ đọc). Chạy trên exp-obs.
Dùng: python3 pool_prom.py <epoch đầu> <epoch cuối>"""
import json, sys, urllib.parse, urllib.request
a, b = int(float(sys.argv[1])), int(float(sys.argv[2]))
Q = {'used': 'max(db_client_connections_usage{service_name="event-service",state="used"})',
     'idle': 'max(db_client_connections_usage{service_name="event-service",state="idle"})',
     'pending': 'max(db_client_connections_pending_requests{service_name="event-service"})',
     'event_5xx_rps': 'sum(rate(http_server_request_duration_seconds_count{service_name="event-service",http_response_status_code=~"5.."}[1m]))',
     'event_p50_ms': 'histogram_quantile(0.5, sum by(le)(rate(http_server_request_duration_seconds_bucket{service_name="event-service"}[1m])))*1000'}
out = {}
for k, q in Q.items():
    u = 'http://localhost:9090/api/v1/query_range?' + urllib.parse.urlencode({'query': q, 'start': a, 'end': b, 'step': 15})
    r = json.load(urllib.request.urlopen(u, timeout=60))['data']['result']
    out[k] = [[int(t), round(float(v), 3)] for s in r for t, v in s['values'] if v not in ('NaN', '+Inf', '-Inf')]
print(json.dumps(out))
