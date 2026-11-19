#!/usr/bin/env python3
"""T-067 bước 7–8: đọc bộ đếm rớt/lỗi của hai Collector trong một cửa sổ (chạy trên exp-obs qua stdin, chỉ đọc).

Dùng: ssh exp-obs "python3 - <start epoch> <end epoch>" < tai_kiem.py > collector.json
Agent = job otelcol-contrib (exp-app), gateway = job central-collector (exp-obs).
Một bộ đếm: increase() trong cửa sổ; resets() của bộ đếm và của otelcol_process_uptime_total để biết Collector
khởi động lại; số mẫu uptime để biết mất mẫu (scrape 10 s, đo 18/11: 180 mẫu/30 phút → kỳ vọng ~ cửa sổ/10).
Bộ đếm không có chuỗi nào: Collector chưa từng tạo bộ đếm đó (chưa có lần lỗi nào) — chỉ coi là 0 khi uptime
liên tục và không mất mẫu; nếu không thì "chua_xac_dinh".

Bản 2 (18/11, sau phản biện nội bộ; bản 1 sha256 c5de4d47…):
- Bỏ họ otelcol_processor_dropped_*: Collector 0.165 không có họ này (đọc endpoint :8888 của agent 18/11).
  Rớt ở processor đo bằng increase(otelcol_processor_incoming_items_total) − increase(…outgoing…) theo processor
  và loại tín hiệu. filter/health bỏ span /actuator/health* theo thiết kế (agent-docker-host.yaml filter/health):
  báo riêng, không tính là rớt.
- Thêm đối chiếu đầu–cuối: span/log agent gửi qua exporter otlp so với gateway nhận (receiver accepted).
"""
import json, sys, urllib.parse, urllib.request

P = 'http://127.0.0.1:9090'
start, end = int(sys.argv[1]), int(sys.argv[2])
w = f'{end - start}s'
JOBS = {'agent': 'otelcol-contrib', 'gateway': 'central-collector'}
FAM = ['otelcol_exporter_send_failed_spans_total', 'otelcol_exporter_send_failed_log_records_total',
       'otelcol_exporter_send_failed_metric_points_total', 'otelcol_exporter_enqueue_failed_spans_total',
       'otelcol_exporter_enqueue_failed_log_records_total', 'otelcol_exporter_enqueue_failed_metric_points_total',
       'otelcol_receiver_refused_spans_total', 'otelcol_receiver_refused_log_records_total',
       'otelcol_receiver_refused_metric_points_total', 'otelcol_receiver_failed_spans_total',
       'otelcol_receiver_failed_log_records_total', 'otelcol_receiver_failed_metric_points_total']
LOC_CO_Y = {'filter/health'}  # processor bỏ dữ liệu theo thiết kế


def q(e):
    u = P + '/api/v1/query?' + urllib.parse.urlencode({'query': e, 'time': end})
    return json.load(urllib.request.urlopen(u, timeout=60))['data']['result']


def v(e):
    r = q(e)
    return None if not r else sum(float(x['value'][1]) for x in r)


out = {'phien_ban': 2, 'cua_so': {'start': start, 'end': end}, 'collector': {}}
for ten, job in JOBS.items():
    up = f'otelcol_process_uptime_total{{job="{job}"}}'
    m = {'job': job,
         'uptime_resets': v(f'resets({up}[{w}])'),
         'uptime_so_mau': v(f'count_over_time({up}[{w}])'),
         'uptime_tang_s': v(f'increase({up}[{w}])'),
         'bo_dem': {}, 'processor': {}}
    for f in FAM:
        sel = f'{f}{{job="{job}"}}'
        m['bo_dem'][f] = {'increase': v(f'sum(increase({sel}[{w}]))'), 'resets': v(f'sum(resets({sel}[{w}]))')}
    for kind in ('incoming', 'outgoing'):
        for x in q(f'sum by (processor, otel_signal) (increase(otelcol_processor_{kind}_items_total{{job="{job}"}}[{w}]))'):
            k = x['metric'].get('processor') + '|' + x['metric'].get('otel_signal')
            m['processor'].setdefault(k, {})[kind] = round(float(x['value'][1]))
    for k, x in m['processor'].items():
        x['chenh'] = x.get('incoming', 0) - x.get('outgoing', 0)
        x['co_y'] = k.split('|')[0] in LOC_CO_Y
    lien_tuc = (m['uptime_resets'] == 0 and m['uptime_so_mau'] is not None
                and m['uptime_so_mau'] >= 0.9 * (end - start) / 10)
    tang = [f for f, x in m['bo_dem'].items() if x['increase'] not in (None, 0.0)]
    reset = [f for f, x in m['bo_dem'].items() if x['resets'] not in (None, 0.0)]
    rot = [k for k, x in m['processor'].items() if x['chenh'] != 0 and not x['co_y']]
    m['uptime_lien_tuc_du_mau'] = lien_tuc
    m['bo_dem_tang'] = tang
    m['processor_rot_ngoai_thiet_ke'] = rot
    m['ket_qua'] = ('khong_dat' if tang or rot else ('dat' if lien_tuc and not reset else 'chua_xac_dinh'))
    out['collector'][ten] = m
dc = {}
for sig, gui, nhan in [('spans', 'otelcol_exporter_sent_spans_total', 'otelcol_receiver_accepted_spans_total'),
                       ('log_records', 'otelcol_exporter_sent_log_records_total', 'otelcol_receiver_accepted_log_records_total')]:
    a = v(f'sum(increase({gui}{{job="otelcol-contrib",exporter="otlp"}}[{w}]))')
    b = v(f'sum(increase({nhan}{{job="central-collector",receiver="otlp"}}[{w}]))')
    dc[sig] = {'agent_gui': None if a is None else round(a), 'gateway_nhan': None if b is None else round(b),
               'chenh': None if a is None or b is None else round(a - b)}
out['doi_chieu_agent_gateway'] = dc
print(json.dumps(out, ensure_ascii=False, indent=1))
