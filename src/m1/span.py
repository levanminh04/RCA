"""Tiền xử lý span (SPEC T-043 B1.2, B2 E1, E2; đặc tả v1 §3, §7.1–7.2; dinh-chinh-cai-dat.md CĐ1).

- Khóa (traceID, spanID). Bỏ bản lặp y hệt và đếm; khóa trùng mà nội dung khác thì cả ca ERROR.
- Quan hệ cha–con dựng trên toàn miền; span gốc có parent rỗng; parent không resolve là span mồ côi.
- Con cắt về [s0, s1) của cha; con nằm hẳn ngoài cha bị bỏ khỏi phép tính của cha; con vượt biên quá τ được đếm.
- E1-U: u = d − |hợp con đã cắt|. E1-CP: u = d − |hợp con trên đường găng CRISP đã cắt| (CĐ1).
- Span bọc (dạng chặt): đúng một con, con ở thực thể khác, cha của span bọc resolve và cùng thực thể. g(w) = u_U(w).
- Đặc trưng tính trên quan hệ toàn miền, rồi mới chia N/A theo end (A khi end >= t).
Mọi thời gian cùng một đơn vị (đối số `t`, `tau` cùng đơn vị với start/duration).
"""

COT = ('traceID', 'spanID', 'parentSpanID', 'owner', 'operation', 'start_us', 'duration_us')


def _rong(x):
    return x is None or x == ''


def tien_xu_ly(rows):
    """Bỏ lặp, phát hiện khóa trùng khác nội dung, đếm span gốc và mồ côi."""
    seen = {}
    bo_lap = 0
    for r in rows:
        k = (r['traceID'], r['spanID'])
        v = tuple(r.get(c) for c in COT)
        if k in seen:
            if seen[k] == v:
                bo_lap += 1
                continue
            return {'bo_lap': bo_lap, 'loi': 'ERROR', 'con_lai': None, 'mo_coi': None, 'goc': None, 'spans': None,
                    'ly_do': f'khóa trùng khác nội dung: {k}'}
        seen[k] = v
    spans = {k: dict(zip(COT, v)) for k, v in seen.items()}
    goc = sum(1 for s in spans.values() if _rong(s['parentSpanID']))
    mo_coi = sum(1 for s in spans.values()
                 if not _rong(s['parentSpanID']) and (s['traceID'], s['parentSpanID']) not in spans)
    return {'bo_lap': bo_lap, 'loi': None, 'con_lai': len(spans), 'mo_coi': mo_coi, 'goc': goc, 'spans': spans}


def _hop(ds):
    ds = sorted((a, b) for a, b in ds if b > a)
    out = []
    for a, b in ds:
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _dai(ds):
    return sum(b - a for a, b in _hop(ds))


def cat_con(cha, con, nguong_vuot):
    """Cắt con về [s0, s1); bỏ con có độ dài sau cắt <= 0; đếm con vượt biên cha quá nguong_vuot ở một đầu bất kỳ."""
    s0, s1 = cha
    cat, vuot = [], 0
    for a, b in con:
        if (s0 - a) > nguong_vuot or (b - s1) > nguong_vuot:
            vuot += 1
        x, y = max(a, s0), min(b, s1)
        if y > x:
            cat.append((x, y))
    return cat, vuot


def doc_quyen_U(cha, con):
    cat, _ = cat_con(cha, con, float('inf'))
    return (cha[1] - cha[0]) - _dai(cat)


def _happens_before(c, d, khac, tau):
    """CRISP §5.2 (thẻ đọc): c_end − τ < d_start và không con nào khác bắt đầu hay kết thúc trong vùng chồng lấn."""
    if not (c[1] - tau < d[0]):
        return False
    if c[1] <= d[0]:
        return True
    lo, hi = d[0], c[1]
    return not any(lo < x < hi for e in khac for x in e)


def duong_gang(cha, con, tau):
    """Đường găng CRISP trên các con đã cắt: LFC, rồi lùi dần theo happensBefore, mỗi bước chọn con kết thúc muộn nhất."""
    cat, _ = cat_con(cha, con, float('inf'))
    if not cat:
        return []
    con_lai = sorted(cat, key=lambda x: (x[1], x[0]))
    cur = con_lai.pop()  # kết thúc muộn nhất; hòa thì bắt đầu muộn hơn
    duong = [cur]
    while True:
        ung = []
        for i, c in enumerate(con_lai):
            khac = [e for j, e in enumerate(con_lai) if j != i]
            if _happens_before(c, cur, khac, tau):
                ung.append((c[1], c[0], i))
        if not ung:
            break
        _, _, i = max(ung)
        cur = con_lai.pop(i)
        duong.append(cur)
    return duong


def doc_quyen_CP(cha, con, tau):
    return (cha[1] - cha[0]) - _dai(duong_gang(cha, con, tau))


def chuan_bi(rows, t, tau, mien=None):
    """Chuẩn bị span cho mọi thành phần. rows: dict theo COT; mien: (lo, hi) lọc span vào miền nếu có
    (start >= lo và end < hi). Trả {'loi', 'spans': {khóa: span}, 'chan_doan'}."""
    if mien is not None:
        lo, hi = mien
        rows = [r for r in rows if r['start_us'] >= lo and r['start_us'] + r['duration_us'] < hi]
    tx = tien_xu_ly(rows)
    if tx['loi']:
        return {'loi': tx['loi'], 'ly_do': tx.get('ly_do'), 'spans': {}, 'chan_doan': tx}
    spans = {}
    for k, s in tx['spans'].items():
        st, d = s['start_us'], s['duration_us']
        cha = None if _rong(s['parentSpanID']) else (s['traceID'], s['parentSpanID'])
        spans[k] = {'khoa': k, 'chu': s['owner'], 'op': s['operation'], 'start': st, 'end': st + d, 'd': d,
                    'cha': cha if cha in tx['spans'] else None, 'mo_coi': cha is not None and cha not in tx['spans'],
                    'con': [], 'phia': 'A' if st + d >= t else 'N'}
    for k, s in spans.items():
        if s['cha'] is not None:
            spans[s['cha']]['con'].append(k)
    vuot = 0
    for k, s in spans.items():
        s['con'].sort()
        khoang = [(spans[c]['start'], spans[c]['end']) for c in s['con']]
        cat, v = cat_con((s['start'], s['end']), khoang, tau)
        vuot += v
        s['u'] = s['d'] - _dai(cat)
        s['u_CP'] = doc_quyen_CP((s['start'], s['end']), khoang, tau)
    for k, s in spans.items():
        boc = (len(s['con']) == 1 and spans[s['con'][0]]['chu'] != s['chu']
               and s['cha'] is not None and spans[s['cha']]['chu'] == s['chu'])
        s['boc'] = boc
        s['g'] = s['u'] if boc else None
    cd = {'bo_lap': tx['bo_lap'], 'mo_coi': tx['mo_coi'], 'goc': tx['goc'], 'con_vuot_bien_cha': vuot,
          'so_span': len(spans), 'span_boc': sum(1 for s in spans.values() if s['boc'])}
    return {'loi': None, 'spans': spans, 'chan_doan': cd}


def mau_thao_tac(prep, E1):
    """Mẫu theo thao tác (chủ, tên). E1 tắt: thời lượng cả span, giữ span bọc (D21). E1 = U/CP: thời gian độc quyền,
    bỏ span bọc. Mỗi phía giữ cả mốc end của mẫu (cho E9)."""
    out = {}
    for s in sorted(prep['spans'].values(), key=lambda x: (x['end'], x['khoa'])):
        if E1 != 'tat' and s['boc']:
            continue
        v = s['d'] if E1 == 'tat' else (s['u'] if E1 == 'U' else s['u_CP'])
        m = out.setdefault((s['chu'], s['op']), {'N': [], 'A': [], 'moc_N': [], 'moc_A': []})
        m[s['phia']].append(v)
        m['moc_' + s['phia']].append(s['end'])
    return out


def mau_canh(prep):
    """Mẫu g(w) theo cạnh a → b, qua span bọc w của a có con ở b; chia N/A theo end của w."""
    out = {}
    for s in sorted(prep['spans'].values(), key=lambda x: (x['end'], x['khoa'])):
        if not s['boc']:
            continue
        b = prep['spans'][s['con'][0]]['chu']
        m = out.setdefault((s['chu'], b), {'N': [], 'A': [], 'moc_N': [], 'moc_A': []})
        m[s['phia']].append(s['g'])
        m['moc_' + s['phia']].append(s['end'])
    return out


def canh_goi(prep):
    """Cạnh gọi quan sát được: (chủ của span cha, chủ của span con), khác chủ, trong miền (N ∪ A)."""
    out = set()
    for s in prep['spans'].values():
        if s['cha'] is not None:
            a = prep['spans'][s['cha']]['chu']
            if a != s['chu']:
                out.add((a, s['chu']))
    return out


def dem_thao_tac(prep):
    """E3b: số span theo thao tác (chủ, tên) ở N và A, gồm cả span bọc (đặc tả v1 §7.4)."""
    out = {}
    for s in prep['spans'].values():
        n = out.setdefault((s['chu'], s['op']), [0, 0])
        n[0 if s['phia'] == 'N' else 1] += 1
    return {k: tuple(v) for k, v in out.items()}
