import ast, shutil
src = 'D:/RCA-flashticket/results/T-063/chay/xac_nhan_ca.py'
p = 'D:/RCA-flashticket/results/T-063/thu3/scripts/xac_nhan_ca_3.py'
s = open(src, encoding='utf-8').read()


def thay(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70])
    s = s.replace(a, b)


thay('"""T-063 — hậu kiểm can thiệp từng ca theo results/T-063/chay/dieu-kien-xac-nhan.md (khai trước 13/11 ~07:30Z).\nDùng: py -3 -B results/T-063/chay/xac_nhan_ca.py <thư mục đợt thu> <file ra.json>\n  <thư mục> chứa: tiem-loi/so-thu2.jsonl,',
     '"""T-063 thu3 — hậu kiểm can thiệp từng ca theo results/T-063/thu3/dieu-kien-xac-nhan-3.md (bản sao chay/xac_nhan_ca.py + ô thu bù 3).\nDùng: py -3 -B results/T-063/thu3/scripts/xac_nhan_ca_3.py <thư mục đợt thu> <file ra.json>\n  <thư mục> chứa: tiem-loi/so-thu3.jsonl,')
thay("SUA_SAU_1 = '--sua-sau-1' in sys.argv", "SUA_SAU_1 = False  # thu3 không có ô PAUSE")
thay("so = [json.loads(l) for l in (G / 'tiem-loi/so-thu2.jsonl')", "so = [json.loads(l) for l in (G / 'tiem-loi/so-thu3.jsonl')")
thay("    if d['event'] == 'cycle-begin': c['cell'] = d['cell']; c['tag'] = d['load_tag']",
     "    if d['event'] == 'cycle-begin': c['cell'] = d['cell']; c['tag'] = d['load_tag']; c['mult'] = d.get('multiplier', 1)")
thay("""audit = []
if audit_f.exists():
    for l in audit_f.read_text(encoding='utf-8').splitlines():
        try: o = json.loads(l)
        except Exception: continue
        if o.get('operation') == 'http.error.executed' and o.get('targetId') == EVENT_ID: audit.append(ts(o['timestamp']))""",
"""audit, audit_pool = [], []
if audit_f.exists():
    for l in audit_f.read_text(encoding='utf-8').splitlines():
        try: o = json.loads(l)
        except Exception: continue
        if o.get('operation') == 'http.error.executed' and o.get('targetId') == EVENT_ID: audit.append(ts(o['timestamp']))
        if str(o.get('operation', '')).startswith('pool.'): audit_pool.append((ts(o['timestamp']), o['operation']))""")
thay("    r = {'ExitCode': st.get('ExitCode'),", "    run = json.loads((d / 'run.json').read_text(encoding='utf-8'))\n    r = {'ExitCode': st.get('ExitCode'), 'multiplier': run.get('multiplier'),")
thay("        k6r, kd = kk; dk['C1_k6'] = k6r['ExitCode'] == 0; c['k6'] = k6r",
     "        k6r, kd = kk; dk['C1_k6'] = k6r['ExitCode'] == 0; c['k6'] = k6r\n        dk['C1_bac_tai'] = k6r['multiplier'] == c.get('mult', 1)")
thay("""TOXIC = {'EVENT-DB-LAT': 'event-jdbc', 'REDIS-BOOK': 'booking-redis', 'NET-GW-BOOK': 'gateway-booking-http'}""",
     """TOXIC = {'EVENT-DB-LAT': 'event-jdbc', 'REDIS-BOOK': 'booking-redis', 'NET-GW-BOOK': 'gateway-booking-http',
         'CONSUMER-BOOK-SLOW-X3': 'booking-amqp'}
KHONG_LOI = ('BINH-THUONG', 'FLASH-HEALTHY', 'BINH-THUONG-X3')


def ton(p):
    rb = p.get('rabbit_booking') or {}
    return None if rb.get('ready_tong') is None else rb['ready_tong'] + rb['unacked_tong']""")
thay("""                dk['gw_p50_tang_ge_200ms'] = (n is not None and l is not None and l - n >= 200)
""", """                dk['gw_p50_tang_ge_200ms'] = (n is not None and l is not None and l - n >= 200)
            if cell == 'CONSUMER-BOOK-SLOW-X3':
                v = [ton(p) for p in (p60, p330, ph)]; c['ton_queue_booking_t60_t330_hoi60'] = v
                c['booking_conn_t60_t330_hoi60'] = [(p.get('rabbit_booking') or {}).get('booking_conn') for p in (p60, p330, ph)]
                if None in v: thieu.append('rabbit_booking')
                dk['ton_t330_ge_10'] = v[1] is not None and v[1] >= 10
                dk['ton_hoi60_le_2'] = v[2] is not None and v[2] <= 2
        elif cell == 'POOL-EVENT':
            if not audit_f.exists(): thieu.append('audit')
            dk['audit_pool_trong_loi'] = any(op == 'pool.hold.started' and t <= x <= t + 605 for x, op in audit_pool)
            dk['audit_pool_khong_truoc'] = not any(t - 600 <= x < t for x, op in audit_pool)
            dk['audit_pool_khong_sau'] = not any(t + 605 < x <= t + 1200 for x, op in audit_pool)
            eu = 'max(db_client_connections_usage{service_name="event-service",state="used"})'
            ep = 'max(db_client_connections_pending_requests{service_name="event-service"})'
            un, ul, us = prom(eu, *N), prom(eu, *L), prom(eu, *Sau); pn, pl = prom(ep, *N), prom(ep, *L)
            c['pool_used_tb_N_L_sau'] = [tb(un), tb(ul), tb(us)]; c['pool_pending_tb_N_maxL'] = [tb(pn), max(pl) if pl else None]
            if not (un and ul and us and pn and pl): thieu.append('prom pool')
            dk['used_L_tb_ge_4_5'] = bool(ul) and tb(ul) >= 4.5
            dk['used_N_tb_le_3'] = bool(un) and tb(un) <= 3
            dk['used_sau_tb_le_3'] = bool(us) and tb(us) <= 3
            dk['pending_L_max_ge_1'] = bool(pl) and max(pl) >= 1
            dk['pending_N_tb_lt_0_5'] = bool(pn) and tb(pn) < 0.5
""")
thay("""        elif cell in ('BINH-THUONG', 'FLASH-HEALTHY'):
            ps = [p for p in P.values()]
            dk['khong_can_thiep_dau_do'] = all(khong_toxic(p) and str(p.get('burn_procs')) == '0' and p.get('payment_state') == 'running false' for p in ps)
            if not audit: thieu.append('audit')
            dk['audit_khong_hook'] = not any(t - 600 <= x <= t + 1200 for x in audit)""",
"""        elif cell in KHONG_LOI:
            ps = [p for p in P.values()]
            dk['khong_can_thiep_dau_do'] = all(khong_toxic(p) and str(p.get('burn_procs')) == '0' and p.get('payment_state') == 'running false' for p in ps)
            if not audit_f.exists(): thieu.append('audit')
            dk['audit_khong_hook'] = not any(t - 600 <= x <= t + 1200 for x in audit)
            dk['audit_khong_pool'] = not any(t - 600 <= x <= t + 1200 for x, op in audit_pool)
            c['ton_queue_booking_cac_dau_do'] = {k: ton(p) for k, p in P.items()}""")
thay("""               **{k: c[k] for k in ('k6', 'ty_le_tai_sau_truoc', 'pg_proxy_ms', 'redis_proxy_ms', 'gw_18082_p50_ms', 'audit',
                                    'nr_throttled', 'httpcheck_error_8083_max') if k in c}}""",
"""               **{k: c[k] for k in ('k6', 'ty_le_tai_sau_truoc', 'pg_proxy_ms', 'redis_proxy_ms', 'gw_18082_p50_ms', 'audit',
                                    'nr_throttled', 'httpcheck_error_8083_max', 'ton_queue_booking_t60_t330_hoi60',
                                    'booking_conn_t60_t330_hoi60', 'pool_used_tb_N_L_sau', 'pool_pending_tb_N_maxL',
                                    'ton_queue_booking_cac_dau_do') if k in c}}""")
thay("RA.write_text(json.dumps({'nguon': str(G), 'dieu_kien': 'results/T-063/chay/dieu-kien-xac-nhan.md',",
     "RA.write_text(json.dumps({'nguon': str(G), 'dieu_kien': 'results/T-063/thu3/dieu-kien-xac-nhan-3.md',")
ast.parse(s)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
