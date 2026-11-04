"""Đ5 cho R0/D1: exposure ±1%, giữ mốc sự kiện và phi cố định.

Companion ngoài bản ghi; kiểm p/F gốc trước khi báo độ nhạy. Không sửa phương pháp.
"""
from m1 import chuoi, cong, e3, e4, runner


def tinh(case, t, rec, config):
    if config['bat_tat']['E3'] or config['bat_tat']['E3b']:
        raise ValueError('Đ5 T1 chỉ R0')
    p = runner._params(config, case)
    tn = int(round(t*10**9))
    factor = chuoi._he_so_ns(p['don_vi_thoi_gian']['logs.timestamp'])
    aliases = case.get('aliases') or {}
    rows = [dict(moc=int(r['timestamp']*factor), thuc_the=chuoi._alias(aliases, r['entity']),
                 noi_dung=r.get('message') or '', severity_raw=r.get('severity_raw'), lop=None)
            for r in case.get('logs') or [] if tn-300*10**9 <= r['timestamp']*factor < tn+300*10**9]
    h0 = min((r['moc'] for r in rows), default=None)
    events = {}
    for r in rows:
        if r['moc'] < tn and e3._lop_dong(r, p['ho_so_nguon']['quy_tac_log']) == e3.LOI:
            events.setdefault(f"log|{r['thuc_the']}|log_loi", []).append(r['moc'])
    units = []
    for u in rec['worlds']['P']['don_vi_dem']:
        if u['trang_thai'] != 'OK':
            continue
        if not u['ma'].startswith('log|') or not u['ma'].endswith('|log_loi'):
            raise ValueError('đơn vị ngoài R0')
        ev = events.get(u['ma'], [])
        if len(ev) != u['n_N']:
            raise ValueError('Đ5 số sự kiện N lệch bản ghi')
        phi = cong.he_so_phan_tan(ev, h0, tn)
        def calc(a, b):
            return e4.cham_dem(u['n_N'], u['n_A'], a, b, p['tham_so_E4'],
                               phi_d=phi, huong_cham=('len',))
        base = calc(u['T_N'], u['T_A'])
        keys = ('p_len', 'p_xuong', 'F_raw_len', 'F_raw_xuong', 'e_len', 'e_xuong')
        diff = {k: [base[k], u[k]] for k in keys if base[k] != u[k]}
        if diff:
            raise ValueError(f'Đ5 phục dựng D1 lệch bản ghi {u["ma"]}: {diff}')
        pert = []
        for a in (.99, 1., 1.01):
            for b in (.99, 1., 1.01):
                z = calc(u['T_N']*a, u['T_A']*b)
                pert.append(dict(fN=a, fA=b, p_len=z['p_len'], F_raw_len=z['F_raw_len'],
                                 changed=z['F_raw_len'] != base['F_raw_len']))
        units.append(dict(ma=u['ma'], phi=phi, h0_ns=h0, n_N=len(ev), original=base,
                          perturbations=pert, changed=any(x['changed'] for x in pert)))
    return dict(cong='D1', huong_cham=['len'], phi_fixed=True, units=units,
                so_don_vi_dem_OK_P=len(units), so_doi_quyet_dinh=sum(x['changed'] for x in units))
