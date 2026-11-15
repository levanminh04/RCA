# -*- coding: utf-8 -*-
"""T-063 — bộ xuất gói metric bổ sung cho M1-FT (H1–H5, H7). Chạy trên exp-obs: `python3 - --t <t> < xuat_bo_sung.py`
hoặc `python3 xuat_bo_sung.py --t <t> --ra <file>`. Chỉ ĐỌC Prometheus (localhost:9090). Không đọc nhãn/sổ tiêm.

Định dạng giống `cases/<id>/prometheus.json` của bộ đóng gói ghim T-058 (danh sách bundle {channel, native, query,
step_seconds, result, native_timestamps}), để `m1.adapter_flashticket.normalize_metrics` đọc được khi M1-FT khai thêm
kênh. Cửa sổ [t−300, t+300] (đủ cửa sổ phương pháp), bước 15 s như kênh không native của bộ ghim. Truy vấn theo khúc
≤ 10 phút (bài học sự cố 12/11 19:16Z), nghỉ 0,3 s giữa khúc; lỗi khúc được ghi, không dừng cả lượt.
"""
import argparse, json, sys, time, urllib.parse, urllib.request

B = 'http://localhost:9090/api/v1/'
R1 = '[1m]'
KENH = [
    # H2 — JVM/cgroup
    ('throttle', 'sum by(service_name) (rate(container_cpu_throttling_data_throttled_time_nanoseconds_total' + R1 + ')) / 1e9'),
    ('throttle-ratio', 'sum by(service_name) (rate(container_cpu_throttling_data_throttled_periods_total' + R1 + ')) / '
                       'sum by(service_name) (rate(container_cpu_throttling_data_periods_total' + R1 + '))'),
    ('gc', 'sum by(service_name) (rate(jvm_gc_duration_seconds_sum' + R1 + '))'),
    ('heap', 'sum by(service_name) (jvm_memory_used_bytes{jvm_memory_type="heap"})'),
    ('threads-blocked', 'sum by(service_name) (jvm_thread_count{jvm_thread_state="blocked"})'),
    ('jvm-cpu', 'sum by(service_name) (jvm_cpu_recent_utilization_ratio)'),
    # H3 — pool kết nối
    ('pool-pending', 'sum by(service_name) (db_client_connections_pending_requests)'),
    ('pool-used', 'sum by(service_name) (db_client_connections_usage{state="used"})'),
    ('pool-wait', 'sum by(service_name) (rate(db_client_connections_wait_time_milliseconds_sum' + R1 + ')) / '
                  'clamp_min(sum by(service_name) (rate(db_client_connections_wait_time_milliseconds_count' + R1 + ')), 1e-9)'),
    # H4 — queue (theo queue; gán thành phần do M1-FT quyết)
    ('queue-ready', 'sum by(rabbitmq_queue_name) (rabbitmq_message_current{state="ready"})'),
    ('queue-unacked', 'sum by(rabbitmq_queue_name) (rabbitmq_message_current{state="unacknowledged"})'),
    ('queue-consumers', 'sum by(rabbitmq_queue_name) (rabbitmq_consumer_count)'),
    ('queue-publish', 'sum by(rabbitmq_queue_name) (rate(rabbitmq_message_published_total' + R1 + '))'),
    ('queue-ack', 'sum by(rabbitmq_queue_name) (rate(rabbitmq_message_acknowledged_total' + R1 + '))'),
    # H5 — sống/chết (khe tín hiệu; uptime/restarts)
    ('restarts', 'sum by(service_name) (container_restarts_total)'),
    ('samples', 'count by(service_name) (count_over_time(jvm_cpu_recent_utilization_ratio' + R1 + '))'),
    # H5 — đầu dò hộp đen liveness (TD-04, từ 12/11 23:27Z): 1 = không phản hồi trong bước; ms phản hồi
    # live-down: httpcheck_status giữ trạng thái cũ khi request treo (D2 bản 2, PAUSE-PAYMENT) → dùng httpcheck_error
    ('live-down', 'max by(http_url) (httpcheck_error) or (0 * max by(http_url) (httpcheck_duration_milliseconds))'),
    ('live-ms', 'max by(http_url) (httpcheck_duration_milliseconds)'),
    # H7 — theo route
    ('route-rate', 'sum by(service_name, http_route) (rate(http_server_request_duration_seconds_count' + R1 + '))'),
    ('route-5xx', 'sum by(service_name, http_route) (rate(http_server_request_duration_seconds_count{http_response_status_code=~"5.."}' + R1 + '))'),
    # H1 — DB/cache theo thực thể
    ('pg-backends', 'sum by(postgresql_database_name) (postgresql_backends)'),
    ('pg-ops', 'sum by(postgresql_database_name) (rate(postgresql_operations_total' + R1 + '))'),
    ('redis-cmd', 'sum (rate(redis_commands_processed_total' + R1 + '))'),
    ('redis-clients', 'sum (redis_clients_connected)'),
]


def q_range(q, s, e, step):
    u = B + 'query_range?' + urllib.parse.urlencode({'query': q, 'start': s, 'end': e, 'step': step})
    r = json.load(urllib.request.urlopen(u, timeout=60))
    if r.get('status') != 'success':
        raise RuntimeError(str(r)[:200])
    return r['data']['result']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--t', type=int, required=True); ap.add_argument('--ra')
    ap.add_argument('--step', type=int, default=15); ap.add_argument('--khuc', type=int, default=600)
    a = ap.parse_args()
    S, E = a.t - 300, a.t + 300
    out, loi = [], []
    for ch, q in KENH:
        gop = {}
        s = S
        while s <= E:
            e = min(E, s + a.khuc - a.step)
            try:
                for x in q_range(q, s, e, a.step):
                    k = json.dumps(x['metric'], sort_keys=True)
                    g = gop.setdefault(k, {'metric': x['metric'], 'values': []})
                    g['values'] += x['values']
            except Exception as ex:
                loi.append({'channel': ch, 'start': s, 'error': repr(ex)[:200]}); time.sleep(5)
            s = e + a.step
            time.sleep(0.3)
        res = []
        for g in gop.values():
            seen, vals = set(), []
            for t0, v in sorted(g['values'], key=lambda z: float(z[0])):
                if t0 not in seen:
                    seen.add(t0); vals.append([t0, v])
            res.append({'metric': g['metric'], 'values': vals})
        out.append({'channel': ch, 'native': False, 'query': q, 'step_seconds': a.step, 'result': res, 'native_timestamps': None})
    doc = {'phien_ban': 'T063-bo-sung-3', 't': a.t, 'cua_so': [S, E], 'loi_khuc': loi, 'bundles': out}
    txt = json.dumps(doc, ensure_ascii=False, separators=(',', ':')) + '\n'
    if a.ra:
        open(a.ra, 'w', encoding='utf-8').write(txt)
    else:
        sys.stdout.write(txt)
    sys.stderr.write(json.dumps({'kenh': len(out), 'chuoi': sum(len(b['result']) for b in out), 'loi_khuc': len(loi)}) + '\n')


main()
