p = 'D:/RCA-flashticket/results/T-063/thu3/scripts/xac_nhan_ca_3.py'
s = open(p, encoding='utf-8').read()
a = """        elif cell in KHONG_LOI:"""
b = """        elif cell == 'RECREATE-PAY':
            ids = {k: (P.get(k) or {}).get('payment_container', '').split() for k in ('t-240', 't+60', 't+330', 'hoi+60')}
            c['payment_container'] = {k: v[:2] for k, v in ids.items()}
            if any(len(v) < 2 for v in ids.values()): thieu.append('payment_container')
            else:
                dk['id_doi_dung_mot_lan'] = (ids['t-240'][0] != ids['t+60'][0] and ids['t+60'][0] == ids['t+330'][0] == ids['hoi+60'][0])
                st = ts(ids['t+60'][1][:26].rstrip('Z') + 'Z') if ids['t+60'][1] else None
                dk['started_trong_t_t60'] = st is not None and t <= st <= t + 60
            dk['running_t330_hoi60'] = all((P.get(k) or {}).get('payment_state') == 'running false' for k in ('t+330', 'hoi+60'))
            e = 'max(httpcheck_error{http_url=~".*:8083.*"})'
            r1, r2 = prom(e, t, t + 120), prom(e, t + 180, t + 570)
            c['httpcheck_error_8083_max_t_t120_va_t180_t570'] = [max(r1) if r1 else None, max(r2) if r2 else None]
            if not r2: thieu.append('prom httpcheck')
            dk['httpcheck_phuc_hoi_t180_t570'] = bool(r2) and max(r2) == 0
        elif cell in KHONG_LOI:"""
assert s.count(a) == 1; s = s.replace(a, b)
a2 = "'ton_queue_booking_cac_dau_do') if k in c}}"
b2 = "'ton_queue_booking_cac_dau_do', 'payment_container', 'httpcheck_error_8083_max_t_t120_va_t180_t570') if k in c}}"
assert s.count(a2) == 1; s = s.replace(a2, b2)
compile(s, p, 'exec'); open(p, 'w', encoding='utf-8', newline='\n').write(s); print('ok')
