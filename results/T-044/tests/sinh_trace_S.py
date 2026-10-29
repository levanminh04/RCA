"""Sinh trace tổng hợp cho S1–S7 theo `fixture-dac-ta.json#/trace_mau_S` (CĐ14, phép đầu-cuối từ span).

Đồ thị F->A, A->R, R->X, F->B; I cô lập. Mỗi lời gọi có span bọc ở bên gọi, đúng một con ở bên được gọi;
khoảng ngoài span 1 ms ở N. 20 request ở N, 20 ở A; mọi đơn vị có thay đổi đổi cả 20 mẫu A.
Đầu vào người làm T-044 bổ sung (đánh dấu ở dinh-chinh-cai-dat.md CĐ14):
- S3: R trả lỗi nhanh (R.handle 31 -> 5 ms), không gọi X; mỗi request một dòng lỗi ở F, A, R trong A;
  một dòng INFO ở F mỗi request ở cả N và A (để khoảng có bản ghi của nguồn log phủ cả hai phía).
- S6: 20 span gốc R.newop (10 ms) chỉ có ở A.
- S7: R không có span; span bọc A.callR không có con; span X.handle có parent không resolve (mồ côi).
"""
TS = {'m_span': 20, 'm_metric': 5, 'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05,
      'n_exact_max': 100, 'count_min': 10}
MS = 1000  # µs


def _thoi_luong(mau, s, phia):
    """Thời lượng (ms) của từng span trong một request, tính từ dưới lên."""
    d = dict(mau['N_ms'])
    g = {'A->R': 1, 'R->X': 1, 'F->A': 1, 'F->B': 1}
    goi_X, co_R = True, True
    if phia == 'A':
        if s == 'S1':
            d['R_self'] = 40
        elif s == 'S2':
            g['A->R'] = 21
        elif s == 'S2b':
            g['A->R'] = 21
            g['R->X'] = 21
        elif s == 'S3':
            d['R_self'] = 5
            goi_X = False
        elif s == 'S5':
            d['I.handle'] = 30
        elif s == 'S7':
            d['R_self'] = 40
    if s == 'S7':
        co_R = False
    X = d['X.handle']
    RcX = X + g['R->X'] if goi_X else None
    R = d['R_self'] + (RcX or 0)
    AcR = R + g['A->R']
    A = d['A_self'] + AcR
    FcA = A + g['F->A']
    B = d['B.handle']
    FcB = B + g['F->B']
    F = d['F_self'] + FcA + FcB
    return {'X.handle': X, 'R.callX': RcX, 'R.handle': R, 'A.callR': AcR, 'A.handle': A, 'F.callA': FcA,
            'B.handle': B, 'F.callB': FcB, 'F.handle': F, 'I.handle': d['I.handle'], 'goi_X': goi_X, 'co_R': co_R}


def _request(tid, bat_dau_us, d):
    """Một trace: trả danh sách span (dict theo hop-dong.json#/vao/spans)."""
    out = []

    def span(sid, cha, chu, op, st, dur_ms):
        out.append({'traceID': tid, 'spanID': sid, 'parentSpanID': cha, 'owner': chu, 'operation': op,
                    'start_us': int(round(st)), 'duration_us': int(round(dur_ms * MS))})

    def boc(sid, cha, chu, op, st, dw, con):
        """Span bọc dw chứa con (sid_con, chủ, op, d) đặt giữa, khoảng ngoài chia đều hai đầu."""
        span(sid, cha, chu, op, st, dw)
        if con is None:
            return None
        sc, cc, oc, dc = con
        st_c = st + (dw - dc) / 2 * MS
        span(sc, sid, cc, oc, st_c, dc)
        return st_c

    s0 = bat_dau_us
    span('f', '', 'F', 'F.handle', s0, d['F.handle'])
    self_F = d['F.handle'] - d['F.callA'] - d['F.callB']
    st_fa = s0 + self_F / 2 * MS
    st_a = boc('fa', 'f', 'F', 'F.callA', st_fa, d['F.callA'], ('a', 'A', 'A.handle', d['A.handle']))
    st_fb = st_fa + d['F.callA'] * MS
    boc('fb', 'f', 'F', 'F.callB', st_fb, d['F.callB'], ('b', 'B', 'B.handle', d['B.handle']))
    self_A = d['A.handle'] - d['A.callR']
    st_ar = st_a + self_A / 2 * MS
    if d['co_R']:
        st_r = boc('ar', 'a', 'A', 'A.callR', st_ar, d['A.callR'], ('r', 'R', 'R.handle', d['R.handle']))
        if d['goi_X']:
            self_R = d['R.handle'] - d['R.callX']
            st_rx = st_r + self_R / 2 * MS
            boc('rx', 'r', 'R', 'R.callX', st_rx, d['R.callX'], ('x', 'X', 'X.handle', d['X.handle']))
    else:
        span('ar', 'a', 'A', 'A.callR', st_ar, d['A.callR'])  # không có con: không là span bọc
        span('x', 'rx-khong-co', 'X', 'X.handle', st_ar + 0.5 * MS, d['X.handle'])  # mồ côi
    return out


def sinh(s, t, mau):
    """Span và log cho kịch bản s. t tính bằng giây."""
    spans, logs = [], []
    t_us = t * 1_000_000
    for phia in ('N', 'A'):
        d = _thoi_luong(mau, s, phia)
        for i in range(20):
            bd = (t_us - 200_000_000 + i * 10_000_000) if phia == 'N' else (t_us + i * 10_000_000)
            tid = f'{phia}{i}'
            spans += _request(tid, bd, d)
            spans.append({'traceID': f'I{phia}{i}', 'spanID': 'i', 'parentSpanID': '', 'owner': 'I',
                          'operation': 'I.handle', 'start_us': bd + 5_000_000, 'duration_us': d['I.handle'] * MS})
            moc_ns = (bd + 1000) * 1000
            if s == 'S3':
                logs.append({'timestamp': moc_ns, 'entity': 'F', 'message': 'INFO request accepted'})
                if phia == 'A':
                    for e in ('F', 'A', 'R'):
                        logs.append({'timestamp': moc_ns + 2000, 'entity': e, 'message': 'ERROR request failed'})
            if s == 'S6' and phia == 'A':
                spans.append({'traceID': f'R{i}', 'spanID': 'n', 'parentSpanID': '', 'owner': 'R',
                              'operation': 'R.newop', 'start_us': bd + 7_000_000, 'duration_us': 10 * MS})
    return spans, logs


def params(ch):
    t_lo, t_hi = (1000 - 720) * 10 ** 9, (1000 + 720) * 10 ** 9
    bt = {'E1': 'tat', 'E2': 'tat', 'E3': False, 'E3b': False, 'E5': False, 'E6': 'a', 'E9': False, 'T12': False}
    bt.update(ch)
    return {'config_id': 'S', 'bat_tat': bt, 'the_gioi': ['P', 'S_lo', 'S_hi'], 'nhanh_z': False,
            'tham_so_E4': dict(TS),
            'don_vi_thoi_gian': {'spans.start_us': 'us', 'metrics.time': 's', 'logs.timestamp': 'ns'},
            'coverage': {'trace': {'khoang': [[t_lo, t_hi]], 'r_ns': 1000},
                         'log': {'khoang': [[t_lo, t_hi]], 'r_ns': 10 ** 9},
                         'metric': {'khoang': [], 'r_ns': 10 ** 9}},
            'nguon_metric': {}, 'thoi_gian_nguon': {}, 'phan_hoach_NA_da_kiem': {},
            'ho_so_nguon': {'kenh_metric': {'kieu': 'hau_to', 'bang': {'cpu': 'tài nguyên'}},
                            'quy_tac_log': {'kieu': 'tu_khoa', 'tu_khoa': ['ERROR', 'FAIL', 'EXCEPTION']},
                            'nguon_khoi_phat': ['trace', 'metric']},
            'tham_so_E3': {'khop': 'hoan_toan', 'sim_th': 0.4, 'do_sau': 4},
            'tham_so_E5': {'doc_nhom_vong': 'co_vong'}}
