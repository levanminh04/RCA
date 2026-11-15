# Chạy trên exp-obs (python3 - < file): đọc mẫu thô quanh lần pause user-service 22:02:22–22:03:22Z; chỉ ĐỌC Prometheus.
import json, urllib.parse, urllib.request
S, E = 1794520882, 1794521062  # pause từ S+60 tới S+120
Q = ['container_cpu_usage_nanoseconds_total{service_name="user-service"}', 'container_uptime_seconds{service_name="user-service"}',
     'container_memory_usage_total_bytes{service_name="user-service"}', 'jvm_cpu_recent_utilization_ratio{service_name="user-service"}',
     'jvm_class_count{service_name="user-service"}', 'http_server_request_duration_seconds_count{service_name="user-service"}']
for q in Q:
    u = 'http://localhost:9090/api/v1/query?' + urllib.parse.urlencode({'query': f'{q}[180s]', 'time': E})
    r = json.load(urllib.request.urlopen(u, timeout=30))['data']['result']
    print('==', q, 'chuỗi', len(r))
    for s in r[:2]:
        ts = [float(v[0]) for v in s['values']]; vs = [v[1] for v in s['values']]
        gaps = [(round(a - S), round(b - a)) for a, b in zip(ts, ts[1:]) if b - a > 15]
        print('  mẫu', len(ts), 'khe>15s (giây từ S, độ dài):', gaps, '| quanh pause:', [(round(t - S), v) for t, v in zip(ts, vs) if 50 <= t - S <= 135])
