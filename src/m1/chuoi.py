"""Chuỗi M1 (SPEC T-043 B1; đặc tả v1). API nhận đúng 7 tham số: spans, metrics, logs, inventory, aliases, t, params
(hop-dong.json#/vao/tham_so_duy_nhat). Không nhận tên ca, đường dẫn, mã mờ, nhãn (luật cứng 6).

Thứ tự: hợp đồng → thời gian về ns (Đ19) → miền → span → trạng thái quan sát → đơn vị theo cấu hình → E4 (ba thế
giới cho đơn vị đếm) → kênh → E2 gán → E5 (+ E9) → xếp hạng E6a/E6b mỗi thế giới → verdict (P) → E7 (P) →
đối chứng C-d1, C-d2, C-d3 trên kết quả chấm của cấu hình (P; CĐ10, chỉ báo cáo) → bản ghi.
Khởi phát (Đ11) luôn tính cho đơn vị phân vị có cờ, vì C-d2 cần; E5 chỉ dùng khi E9 bật.
"""
import math

from m1 import doi_chung, e2, e4, e5, e7, hop_dong, kenh as kenh_mod, quan_sat, span, xep_hang
from m1.kieu import Kenh

PHIEN_BAN = 'M1-T044-1'
NS = 10 ** 9
WORLDS = ('P', 'S_lo', 'S_hi')
CACHE = e4.CacheCong()

LOP_FIXTURE = {'lan_nguoc': 'lan_nguoc', 'tai_nguyen_tang': 'khong_lan', 'khong_lan': 'khong_lan',
               'lan_xuoi': 'lan_xuoi'}


class LoiHopDong(Exception):
    def __init__(self, status, msg):
        super().__init__(msg)
        self.status = status


# ---------------------------------------------------------------- mức kênh (fixture 1, 45; đối chứng C-a0, C-a1)

def doi_chung_cau_hinh(ma, chuoi_cuoi):
    """C-a0, C-a1 (SPEC B2 bảng đối chứng; D18, D23)."""
    if ma == 'C-a0':
        return {'E1': 'tat', 'E2': 'tat', 'E3': chuoi_cuoi['E3'], 'E3b': chuoi_cuoi['E3b'], 'E5': False, 'E6': 'a',
                'E9': False, 'T12': False, 'E7': False}
    if ma == 'C-a1':
        return {'E1': chuoi_cuoi['E1'], 'E2': 'tat', 'E3': chuoi_cuoi['E3'], 'E3b': chuoi_cuoi['E3b'], 'E5': False,
                'E6': 'a', 'E9': False, 'T12': False, 'E7': False}
    raise ValueError(ma)


def kenh_tu_don_vi(don_vi_co, ch):
    """Kênh có cờ từ danh sách đơn vị đã có thay đổi (fixture-dac-ta.json#/trace_mau_S/quy_uoc)."""
    out = []
    for u in don_vi_co:
        n = u['nhom']
        if n == 'op_full' and ch['E1'] == 'tat':
            out.append(Kenh(u['thuc_the'], u['ten'], 'len', 'lan_nguoc', u['s'], nhom='op_full'))
        elif n == 'op_excl' and ch['E1'] != 'tat':
            out.append(Kenh(u['thuc_the'], u['ten'], 'len', 'khong_lan', u['s'], nhom='op_excl'))
        elif n == 'log_loi':
            out.append(Kenh(u['thuc_the'], 'log_loi', 'len', 'lan_nguoc', u['s'], loai='dem', nhom='log_loi'))
        elif n == 'tan_suat' and ch.get('E3b'):
            huong = 'len' if u['kieu'] == 'NEW_OP' else 'xuong'
            out.append(Kenh(u['thuc_the'], u['ten'], huong, kenh_mod.lop('tan_suat', huong), u['s'], loai='dem',
                            nhom='tan_suat'))
    if ch['E2'] != 'tat':
        canh_co = [(u['ben_goi'], u['ben_duoc_goi'], u['s']) for u in don_vi_co if u['nhom'] == 'canh']
        if canh_co:
            for e, ten, s in e2.gan_canh(canh_co, che_do=ch['E2'])['kenh']:
                out.append(Kenh(e, ten, 'len', 'khong_lan', s, nhom='canh'))
    return out


def xep_tu_don_vi(don_vi_co, canh, quan_sat_ds, ch, doc_nhom_vong='co_vong'):
    kenh = kenh_tu_don_vi(don_vi_co, ch)
    p = e5.phan_loai(kenh, canh, bat=bool(ch.get('E5')), doc_nhom_vong=doc_nhom_vong)
    return xep_hang.xep(kenh, F_I=p['F_I'], thuc_the_co_kenh_OK=set(quan_sat_ds),
                        che_do='E6b' if ch.get('E6') == 'b' else 'E6a', canh=canh)


def xep_tu_kenh_fixture(kenh_dict, canh, bat_E5):
    """Fixture 45: kênh [tên, lớp, điểm] theo thực thể."""
    kenh = []
    for e, ds in kenh_dict.items():
        for ten, lop, s in ds:
            l = LOP_FIXTURE[lop]
            kenh.append(Kenh(e, ten, 'xuong' if l == 'lan_xuoi' else 'len', l, s))
    p = e5.phan_loai(kenh, canh, bat=bat_E5)
    return xep_hang.xep(kenh, F_I=p['F_I'], thuc_the_co_kenh_OK=set(kenh_dict), canh=canh)


# ---------------------------------------------------------------- API 7 tham số

def _kiem_params(params):
    for k in ('config_id', 'bat_tat', 'tham_so_E4'):
        if k not in params:
            raise LoiHopDong('ERROR', f'thiếu params.{k}')
    if 'don_vi_thoi_gian' not in params:
        raise LoiHopDong('ERROR', 'thiếu params.don_vi_thoi_gian (Đ19 điểm 1)')
    if 'ho_so_nguon' not in params:
        raise LoiHopDong('ERROR', 'thiếu params.ho_so_nguon (CĐ5)')
    bt = params['bat_tat']
    if bt.get('T12') and 'canh_tinh' not in params:
        raise LoiHopDong('UNSUPPORTED', 'T12 bật nhưng thiếu params.canh_tinh (Đ19 điểm 5)')
    if bt.get('E3') and 'tham_so_E3' not in params:
        raise LoiHopDong('ERROR', 'E3 bật nhưng thiếu params.tham_so_E3 (CĐ5)')


def _he_so_ns(dv):
    if dv == 's':
        return NS
    if dv == 'ns':
        return 1
    if dv == 'us':
        return 1000
    raise LoiHopDong('ERROR', f'đơn vị thời gian lạ: {dv}')


def _alias(aliases, x):
    return aliases.get(x, x) if aliases else x


def _ten_metric(cot, aliases):
    e, duoi = cot.split('_', 1)
    return _alias(aliases, e), duoi


def _kenh_tu_ket_qua(u, kq, huong_cham, lop_cua, khoi_phat=None):
    out = []
    for d in huong_cham:
        F = int(kq.get(f'F_raw_{d}', 0))
        s = float(kq.get(f'e_{d}', 0.0)) if F else 0.0
        out.append(Kenh(u['thuc_the'], u['ten'], d, lop_cua[d], s, F_raw=F, trang_thai=kq['trang_thai'],
                        loai=kq.get('loai', 'phan_vi'), hop_le=bool(kq.get('hop_le')),
                        khoi_phat=(khoi_phat or {}).get(d) if F else None, nhom=u['nhom'], don_vi=u['ma']))
    return out


def _khoi_phat_phan_vi(u, kq, t_ns, o_s_ns):
    """Khởi phát (E9, Đ11) của đơn vị phân vị có cờ, theo hướng; None khi nguồn không dùng cho khởi phát."""
    from m1 import e9
    if not u.get('moc_A_ns'):
        return {}
    out = {}
    for d in ('len', 'xuong'):
        if kq.get(f'F_raw_{d}'):
            ng = kq['h'] if d == 'len' else kq['l']
            rN = kq['r_len_N'] if d == 'len' else kq['r_xuong_N']
            out[d] = e9.khoi_phat(u['moc_A_ns'], u['A'], ng, rN, t_ns, d, o_s=o_s_ns)
    return out


def chay(spans, metrics, logs, inventory, aliases, t, params):
    """Chạy một cấu hình M1 trên một ca. Trả bản ghi (mở rộng ban_ghi.tao, B1.7). Không ném lỗi ra ngoài."""
    try:
        return _chay(spans, metrics, logs, inventory, aliases, t, params)
    except LoiHopDong as ex:
        return _ban_ghi_loi(params, ex.status, str(ex))
    except hop_dong.LoiTruongCam:
        raise
    except Exception as ex:  # lỗi runner/dữ liệu: giữ thông điệp, ca vẫn ở mẫu số (WHY-28)
        return _ban_ghi_loi(params, 'ERROR', f'{type(ex).__name__}: {ex}')


def _ban_ghi_loi(params, status, msg):
    rec = {'method': 'M1', 'method_version': PHIEN_BAN, 'variant': (params or {}).get('config_id'),
           'mode': 'a', 'config_id': (params or {}).get('config_id'), 'why_ids': [], 'window': None,
           'status': status, 'error': msg, 'blocks': None, 'entity_ranking': [], 'ranking_native': [],
           'sets': {'observed': 0, 'observed_entities': [], 'returned': 0}, 'diagnostics': {}, 'extra': {},
           'verdict': None}
    return rec


def _chay(spans, metrics, logs, inventory, aliases, t, params):
    _kiem_params(params)
    bt = params['bat_tat']
    ts = params['tham_so_E4']
    ho_so = params['ho_so_nguon']
    dv = params['don_vi_thoi_gian']
    E1, E2, E3, E3b, E5, E6, E9, T12 = (bt.get('E1', 'tat'), bt.get('E2', 'tat'), bool(bt.get('E3')),
                                        bool(bt.get('E3b')), bool(bt.get('E5')), bt.get('E6', 'a'),
                                        bool(bt.get('E9')), bool(bt.get('T12')))
    nhanh_z = bool(params.get('nhanh_z'))
    U = sorted(set(_alias(aliases, x) for x in inventory))
    t_ns = int(round(t * NS))
    lo_ns, hi_ns = t_ns - 300 * NS, t_ns + 300 * NS
    o_s_ns = 10 * NS
    tau_ns = 10 ** 6
    he_span = _he_so_ns(dv.get('spans.start_us', 'us'))
    he_m = _he_so_ns(dv.get('metrics.time', 's'))
    he_l = _he_so_ns(dv.get('logs.timestamp', 's'))

    # ---- span: miền theo start >= t−300 và end < t+300 (cua_so.cat_span), chia N/A theo end (B1.1)
    rows = []
    for r in spans:
        st = r['start_us'] * he_span
        en = (r['start_us'] + r['duration_us']) * he_span
        if st >= lo_ns and en < hi_ns:
            rows.append(dict(r, owner=_alias(aliases, r['owner'])))
    t_span = t_ns / he_span
    prep = span.chuan_bi(rows, t=t_span, tau=tau_ns / he_span)
    if prep['loi']:
        raise LoiHopDong('ERROR', prep.get('ly_do') or 'span lỗi')

    # ---- quan sát theo nguồn
    cov = params.get('coverage') or {}
    phia = {'N': (lo_ns, t_ns), 'A': (t_ns, hi_ns)}

    def _nguon(ten, moc):
        c = cov.get(ten)
        if c is None or c.get('r_ns') is None:
            return {'trang_thai': 'UNSUPPORTED'}
        khoang = [(a, b + c['r_ns']) for a, b in c['khoang']]
        kq = quan_sat.tinh_nguon(khoang, moc, c['r_ns'], (lo_ns, hi_ns), phia, o_s=o_s_ns)
        kq['trang_thai'] = 'OK'
        return kq

    moc_trace = [int(s['end'] * he_span) for s in prep['spans'].values()]
    qs = {'trace': _nguon('trace', moc_trace)}
    dong = []
    for r in logs:
        m = r['timestamp'] * he_l
        if lo_ns <= m < hi_ns:
            dong.append({'moc': int(m), 'thuc_the': _alias(aliases, r['entity']), 'noi_dung': r.get('message') or '',
                         'severity_raw': r.get('severity_raw'), 'lop': None})
    qs['log'] = _nguon('log', [d['moc'] for d in dong])

    def T_cua(nguon, w):
        q = qs.get(nguon)
        if not q or q.get('trang_thai') != 'OK':
            return None
        return q['the_gioi'][w]

    # ---- đơn vị
    don_vi = []
    mtt = span.mau_thao_tac(prep, E1 if E1 in ('tat', 'U', 'CP') else 'tat')
    nhom_op = 'op_full' if E1 == 'tat' else 'op_excl'
    for (chu, op), m in sorted(mtt.items()):
        don_vi.append({'ma': f'op|{chu}|{op}', 'thuc_the': chu, 'ten': op, 'nhom': nhom_op, 'loai': 'phan_vi',
                       'N': m['N'], 'A': m['A'], 'moc_A_ns': [int(x * he_span) for x in m['moc_A']],
                       'm': ts['m_span'], 'nguon': 'trace',
                       'huong_cham': kenh_mod.huong_cham(nhom_op, E3),
                       'lop': {d: kenh_mod.lop(nhom_op, d) for d in ('len', 'xuong')}})
    if E2 != 'tat':
        for (a, b), m in sorted(span.mau_canh(prep).items()):
            don_vi.append({'ma': f'canh|{a}|{b}', 'thuc_the': b, 'ten': f'{a}->{b}', 'ben_goi': a,
                           'ben_duoc_goi': b, 'nhom': 'canh', 'loai': 'phan_vi', 'N': m['N'], 'A': m['A'],
                           'moc_A_ns': [int(x * he_span) for x in m['moc_A']], 'm': ts['m_span'], 'nguon': 'trace',
                           'huong_cham': ['len'], 'lop': {'len': 'khong_lan'}})
    chan_doan = {'span': prep['chan_doan'], 'nguon_metric_unsupported': [], 'cot_chua_khai_nguon': []}
    # metric
    if metrics:
        tg = quan_sat.thoi_gian_nguon_metric(
            dict(params, nguon_metric=(params.get('nguon_metric') or {})),
            [int(r['time'] * he_m) for r in metrics])
        cols = sorted({k for r in metrics for k in r if k != 'time'})
        nguon_cua = params.get('nguon_metric') or {}
        for cot in cols:
            lop_m = kenh_mod.lop_metric(cot, ho_so)
            if lop_m is None:
                raise LoiHopDong('ERROR', f'cột metric không có trong hồ sơ nguồn: {cot}')
            hc = kenh_mod.huong_cham('metric', E3, lop_m)
            if not hc:
                continue
            ng = nguon_cua.get(cot)
            if ng is None:  # Đ19 điểm 3: không dùng metrics.time khi adapter chưa khai và xác nhận nguồn
                chan_doan['cot_chua_khai_nguon'].append(cot)
                continue
            thong_tin = tg[ng]
            if not thong_tin['cham_NA']:
                chan_doan['nguon_metric_unsupported'].append(ng)
                continue
            moc = thong_tin['moc'] if thong_tin['trang_thai'] == 'OK' else [int(r['time'] * he_m) for r in metrics]
            N, A, mocA = [], [], []
            for r, mc in zip(metrics, moc):
                v = r.get(cot)
                if v is None or not math.isfinite(v) or not (lo_ns <= mc < hi_ns):  # đặc tả v1 dòng 110: giá trị hữu hạn
                    continue
                if mc < t_ns:
                    N.append(v)
                else:
                    A.append(v)
                    mocA.append(mc)
            e, duoi = _ten_metric(cot, aliases)
            dung_kp = thong_tin['trang_thai'] == 'OK' and 'metric' in ho_so.get('nguon_khoi_phat', [])
            don_vi.append({'ma': f'metric|{cot}', 'thuc_the': e, 'ten': duoi, 'nhom': 'metric', 'loai': 'phan_vi',
                           'N': N, 'A': A, 'moc_A_ns': mocA if dung_kp else [], 'm': ts['m_metric'],
                           'nguon': 'metric', 'huong_cham': hc,
                           'lop': {d: kenh_mod.lop('metric', d, lop_m) for d in hc}})
    # log
    quy_tac = ho_so['quy_tac_log']
    dongN = [d for d in dong if d['moc'] < t_ns]
    dongA = [d for d in dong if d['moc'] >= t_ns]
    for u in kenh_mod.don_vi_log(dongN, dongA, quy_tac, E3, params.get('tham_so_E3')):
        u = dict(u, ma=f"log|{u['thuc_the']}|{u['ten']}", loai='dem', nguon='log')
        don_vi.append(u)
    if E3b:
        for (chu, op), (nN, nA) in sorted(span.dem_thao_tac(prep).items()):
            don_vi.append({'ma': f'tan_suat|{chu}|{op}', 'thuc_the': chu, 'ten': f'tan_suat:{op}', 'nhom': 'tan_suat',
                           'loai': 'dem', 'n_N': nN, 'n_A': nA, 'nguon': 'trace', 'huong_cham': ['len', 'xuong'],
                           'lop': {'len': 'lan_nguoc', 'xuong': 'lan_xuoi'}})

    # ---- E4
    kq_pv = {}
    for u in don_vi:
        if u['loai'] == 'phan_vi':
            kq = e4.cham_phan_vi(u['N'], u['A'], u['m'], ts, huong_cham=u['huong_cham'], cache=CACHE,
                                 khoa_don_vi=u['ma'])
            if nhanh_z and kq['trang_thai'] == 'OK':
                z = e4.diem_z(u['N'], u['A'])
                kq = dict(kq, hop_le=kq['hop_le'] and z['huu_han'])
                for d in u['huong_cham']:
                    if kq[f'F_raw_{d}']:
                        kq[f'e_{d}'] = z[f'z_{d}']
            kq_pv[u['ma']] = kq
    worlds = {}
    for w in WORLDS:
        ds_kenh = []
        don_vi_w = []
        for u in don_vi:
            if u['loai'] == 'phan_vi':
                kq = kq_pv[u['ma']]
                kp = _khoi_phat_phan_vi(u, kq, t_ns, o_s_ns)
            else:
                T = T_cua(u['nguon'], w)
                if T is None:
                    kq = {'trang_thai': 'UNSUPPORTED', 'hop_le': False, 'loai': 'dem'}
                else:
                    ep = None
                    if u['nhom'] == 'log_loi' and u.get('kieu_quy_tac') == 'severity':
                        if u['dem_N']['dong'] > 0 and u['dem_N']['xac_dinh'] == 0:
                            ep = 'NO_BASELINE'
                        elif u['dem_A']['dong'] > 0 and u['dem_A']['xac_dinh'] == 0:
                            ep = 'NO_A'
                    kq = e4.cham_dem(u['n_N'], u['n_A'], T[0], T[1], ts, trang_thai_ep=ep,
                                     huong_cham=tuple(u['huong_cham']))
                kp = {}
            don_vi_w.append((u, kq))
            if u['nhom'] == 'canh':
                continue
            ds_kenh += _kenh_tu_ket_qua(u, kq, u['huong_cham'], u['lop'], kp)
        # E2: gán cạnh có cờ
        canh_E2_bat_thuong = set()
        if E2 != 'tat':
            co_canh = [(u, kq) for u, kq in don_vi_w if u['nhom'] == 'canh' and kq.get('F_raw_len')]
            canh_co = [(u['ben_goi'], u['ben_duoc_goi'], kq['e_len']) for u, kq in co_canh]
            canh_E2_bat_thuong = {(u['ben_goi'], u['ben_duoc_goi']) for u, _ in co_canh}
            kp_canh = {(u['ben_goi'], u['ben_duoc_goi']): _khoi_phat_phan_vi(u, kq, t_ns, o_s_ns).get('len')
                       for u, kq in co_canh}
            if canh_co:
                g = e2.gan_canh(canh_co, che_do=E2)
                chan_doan.setdefault('E2_du_phong', 0)
                chan_doan['E2_du_phong'] += int(g['du_phong'])
                diem = {(a, b): s for a, b, s in canh_co}
                for e, ten, s in g['kenh']:
                    if ten.startswith('E2VC:'):
                        phu = [(a, b) for a, b, _ in canh_co if e in (a, b)]
                        best = max(phu, key=lambda x: (diem[x], x))
                    else:
                        a, b = ten[3:].split('->')
                        best = (a, b)
                    ds_kenh.append(Kenh(e, ten, 'len', 'khong_lan', s, loai='phan_vi', nhom='canh',
                                        khoi_phat=kp_canh.get(best), don_vi=f'canh|{best[0]}|{best[1]}'))
            for u, kq in don_vi_w:
                if u['nhom'] == 'canh' and not kq.get('F_raw_len'):
                    ds_kenh.append(Kenh(u['ben_duoc_goi'], f"E2:{u['ten']}", 'len', 'khong_lan', 0.0, F_raw=0,
                                        trang_thai=kq['trang_thai'], hop_le=bool(kq.get('hop_le')), nhom='canh',
                                        don_vi=u['ma']))
        worlds[w] = {'kenh': ds_kenh, 'don_vi': don_vi_w, 'canh_E2': canh_E2_bat_thuong}

    # ---- cạnh: quan sát N ∪ A; cạnh tĩnh khi T12 bật (D8)
    canh_qs = span.canh_goi(prep)
    so_canh_tinh = 0
    canh = set(canh_qs)
    if T12:
        ct = params['canh_tinh']
        tinh = {(_alias(aliases, a), _alias(aliases, b)) for a, b in ct.get('canh', [])}
        so_canh_tinh = len(tinh)
        canh |= tinh
    canh = sorted(canh)

    # ---- E5, xếp hạng mỗi thế giới
    tham_so_E5 = params.get('tham_so_E5') or {}
    xh_w, e5_w = {}, {}
    for w in WORLDS:
        ds_kenh = worlds[w]['kenh']
        p = e5.phan_loai(ds_kenh, canh, bat=E5, doc_nhom_vong=tham_so_E5.get('doc_nhom_vong', 'co_vong'),
                         e9={'bat': E9, 'o_s': o_s_ns, 'tau': tau_ns,
                             'canh_E2_bat_thuong': worlds[w]['canh_E2'] if E2 != 'tat' else set()})
        co_OK = {k.thuc_the for k in ds_kenh if k.trang_thai == 'OK'} & set(U)
        ds_U = [k for k in ds_kenh if k.thuc_the in set(U)]
        xh_w[w] = xep_hang.xep(ds_U, F_I=p['F_I'], thuc_the_co_kenh_OK=co_OK, che_do='E6b' if E6 == 'b' else 'E6a',
                               canh=canh)
        e5_w[w] = p
    xP = xh_w['P']
    so_hop_le = sum(1 for u, kq in worlds['P']['don_vi'] if kq.get('hop_le'))
    verdict = xep_hang.verdict(xP['tang'], so_hop_le)
    O = sorted({k.thuc_the for k in worlds['P']['kenh']} & set(U))
    co_OK_P = {k.thuc_the for k in worlds['P']['kenh'] if k.trang_thai == 'OK'} & set(U)
    hop_le_tt = {k.thuc_the for k in worlds['P']['kenh'] if k.hop_le} & set(U)
    R1 = e7.vung(xP['T'], [k for k in worlds['P']['kenh'] if k.thuc_the in set(U)], canh,
                 e5_w['P']['inherited_by'], cach=1)
    R2 = e7.vung(xP['T'], [k for k in worlds['P']['kenh'] if k.thuc_the in set(U)], canh,
                 e5_w['P']['inherited_by'], cach=2)
    nhan_dem = {}
    for w in WORLDS:
        for u, kq in worlds[w]['don_vi']:
            if u['loai'] == 'dem':
                nhan_dem.setdefault(u['ma'], {})[w] = kq.get('nhan')
    obs_dep = sorted(m for m, v in nhan_dem.items() if e4.obs_dependent(v))
    # ---- đối chứng trên kết quả chấm của cấu hình (CĐ10; Đ11; Đ12), thế giới P, chỉ báo cáo
    kenh_P_U = [k for k in worlds['P']['kenh'] if k.thuc_the in set(U)]
    diem_d3 = {e: xep_hang.khoa(ds)[0] for e, ds in doi_chung._theo_e(kenh_P_U).items()}
    lan_nguoc = sorted({k.thuc_the for k in kenh_P_U if k.co and k.lop == 'lan_nguoc'})
    spans_A = [{'parent': None if (s['cha'] is None and not s['mo_coi']) else 'co', 'chu': s['chu']}
               for s in prep['spans'].values() if s['phia'] == 'A']
    dich = doi_chung.dich_cd3(spans_A, lan_nguoc)
    d3 = dict(doi_chung.cd3(canh, diem_d3, dich), dich=dich,
              so_span_goc_A=sum(1 for s in spans_A if s['parent'] is None))
    dc = {'C-d1': doi_chung.cd1(kenh_P_U, canh, co_OK_P), 'C-d2': doi_chung.cd2_tu_kenh(kenh_P_U, co_OK_P),
          'C-d3': d3}
    # ---- T4c (CĐ7): thứ tự thứ hai trên cùng phép chấm, chỉ khi E6a; thế giới P; không chấm lại
    F_I_P = e5_w['P']['F_I']
    T4c = None
    if E6 != 'b':
        m_dv = {}
        for u, kq in worlds['P']['don_vi']:
            if not (kq.get('F_raw_len') or kq.get('F_raw_xuong')):
                continue
            if u['loai'] == 'phan_vi':
                m_dv[u['ma']] = e4.m_T4c_phan_vi(u['N'], u['A'])
            else:
                m_dv[u['ma']] = e4.m_T4c_dem(kq['n_N'], kq['n_A'], kq['T_N'], kq['T_A'])
        kT = {}
        for k in kenh_P_U:
            if k.co:
                m = m_dv.get(k.don_vi, 0.0)
                a, b = kT.get(k.thuc_the, (0.0, 0.0))
                kT[k.thuc_the] = (max(a, m), max(b, m) if F_I_P.get(k.ma, 1) == 1 else b)
        x4 = xep_hang.xep(kenh_P_U, F_I=F_I_P, thuc_the_co_kenh_OK=co_OK_P, che_do='E6a', canh=canh, khoa_T4c=kT)
        T4c = {'blocks': x4['blocks'], 'm_thuc_the': {e: list(v) for e, v in sorted(kT.items())},
               'm_don_vi': dict(sorted(m_dv.items()))}
    kenh_co = [{'thuc_the': k.thuc_the, 'ten': k.ten, 'huong': k.huong, 'lop': k.lop, 's': k.s,
                'F_I': F_I_P.get(k.ma, 1), 'don_vi': k.don_vi, 'khoi_phat': k.khoi_phat}
               for k in sorted(kenh_P_U, key=lambda x: x.ma) if k.co]
    # G_N (codebook T-028 §4; CĐ6.1): cạnh cha–con khác chủ khi cả hai span thuộc N; chỉ để bộ đánh giá đếm M5
    sp = prep['spans']
    G_N = sorted({(sp[s['cha']]['chu'], s['chu']) for s in sp.values()
                  if s['cha'] is not None and s['phia'] == 'N' and sp[s['cha']]['phia'] == 'N'
                  and sp[s['cha']]['chu'] != s['chu']})
    classes = {}
    for e in O:
        if e not in co_OK_P:
            classes[e] = 'thieu_du_lieu'
        else:
            classes[e] = {1: 'tu_sinh', 2: 'ke_thua', 3: 'binh_thuong'}[xP['tang'][e]]
    blocks = xP['blocks']
    status = 'OK' if blocks else 'NO_EVIDENCE'
    rec = {
        'method': 'M1', 'method_version': PHIEN_BAN, 'variant': params['config_id'], 'mode': 'a',
        'config_id': params['config_id'], 'why_ids': ['WHY-55', 'WHY-56', 'WHY-57', 'WHY-58', 'WHY-59', 'WHY-60',
                                                      'WHY-61', 'WHY-62', 'WHY-63', 'WHY-64', 'WHY-65'],
        'window': {'N': [lo_ns, t_ns], 'A': [t_ns, hi_ns], 'don_vi': 'ns'},
        'status': status, 'error': None, 'blocks': blocks,
        'entity_ranking': [{'entity': e, 'key': b['key'], 'tie_group': bi}
                           for bi, b in enumerate(blocks) for g in b['groups'] for e in g],
        'ranking_native': [],
        'sets': {'observed': len(O), 'observed_entities': O, 'returned': len(xP['thu_tu'])},
        'classes': classes,
        'inherited_by': [dict(x, giai_thich=list(x['giai_thich']), duong=list(x['duong']))
                         for x in e5_w['P']['inherited_by']],
        'region': {'T': xP['T'], 'cach_1': {r: sorted(v) for r, v in R1.items()},
                   'cach_2': {r: sorted(v) for r, v in R2.items()},
                   'hop_cach_1': sorted(set().union(*R1.values())) if R1 else [],
                   'hop_cach_2': sorted(set().union(*R2.values())) if R2 else []},
        'evidence_refs': sorted({k.don_vi for k in worlds['P']['kenh'] if k.co and k.don_vi}),
        'coverage': {n: _gon_qs(q) for n, q in qs.items()},
        'worlds': {w: {'thu_tu': xh_w[w]['thu_tu'], 'blocks': xh_w[w]['blocks'],
                       'don_vi_dem': [{'ma': u['ma'], 'n_N': kq.get('n_N'), 'n_A': kq.get('n_A'),
                                       'T_N': kq.get('T_N'), 'T_A': kq.get('T_A'), 'trang_thai': kq['trang_thai'],
                                       'loai_thay_doi': kq.get('nhan'),
                                       'p_len': kq.get('p_len'), 'p_xuong': kq.get('p_xuong'),
                                       'e_len': kq.get('e_len'), 'e_xuong': kq.get('e_xuong'),
                                       'F_raw_len': kq.get('F_raw_len'), 'F_raw_xuong': kq.get('F_raw_xuong')}
                                      for u, kq in worlds[w]['don_vi'] if u['loai'] == 'dem']}
                   for w in WORLDS},
        'OBS_DEPENDENT': obs_dep,
        'RANK_CHANGED': xep_hang.rank_changed({w: [b['groups'] for b in xh_w[w]['blocks']] for w in WORLDS}),
        'verdict': verdict,
        'do_phu_cham': (len(hop_le_tt) / len(O)) if O else 0.0,
        'diagnostics': {'so_canh_tinh': so_canh_tinh, 'so_canh_quan_sat': len(canh_qs), 'span': prep['chan_doan'],
                        'E2_du_phong': chan_doan.get('E2_du_phong', 0),
                        'nguon_metric_unsupported': sorted(set(chan_doan['nguon_metric_unsupported'])),
                        'cot_metric_chua_khai_nguon': sorted(chan_doan['cot_chua_khai_nguon']),
                        'E6b': xP['trang_thai_E6b'], 'so_cham_hop_le': so_hop_le,
                        'NO_VALID_CHANNEL': sorted(set(O) - co_OK_P)},
        'extra': {'blocks_P': blocks, 'tang_P': xP['tang'],
                  'K_I_P': {e: list(v) for e, v in xP['K_I'].items()},
                  'K_raw_P': {e: list(v) for e, v in xP['K_raw'].items()},
                  'canh': [list(c) for c in canh], 'nhom_vong_P': e5_w['P']['nhom_vong'],
                  'doi_chung': dc, 'T4c': T4c, 'kenh_co': kenh_co, 'G_N': [list(c) for c in G_N],
                  'don_vi_phan_vi': [_gon_pv(u['ma'], kq_pv[u['ma']]) for u in don_vi if u['loai'] == 'phan_vi']},
    }
    hop_dong.kiem_ban_ghi(rec)
    return rec


CHI_TIET_PV = ('trang_thai', 'n_N', 'n_A', 'h', 'l', 'r_len_N', 'r_len_A', 'r_xuong_N', 'r_xuong_A', 'p_len', 'p_xuong',
               'cach_cong_len', 'cach_cong_xuong', 'e_len', 'e_xuong', 'F_raw_len', 'F_raw_xuong', 'hop_le')


def _gon_pv(ma, kq):
    """Chi tiết đơn vị phân vị (dùng chung ba thế giới; CĐ13)."""
    return dict({k: kq.get(k) for k in CHI_TIET_PV}, ma=ma)


def _gon_qs(q):
    if q.get('trang_thai') != 'OK':
        return {'trang_thai': q.get('trang_thai')}
    return {'trang_thai': 'OK', 'F': list(q['F']) if q['F'] else None, 'H': list(q['H']) if q['H'] else None,
            'khe': [list(k) for k in q['khe']], 'T_chac': q['T_chac'], 'T_max': q['T_max'], 'o': q['o'],
            'the_gioi': {w: list(v) for w, v in q['the_gioi'].items()}}
