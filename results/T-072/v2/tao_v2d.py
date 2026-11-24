# -*- coding: utf-8 -*-
"""Tạo cham_offline_v2d.py từ cham_offline_v2c.py (Codex CX-36). Không sửa v2, v2_claude, v2c.

v2d (Claude T-072, đáp CX-36b): thay cách xử lý bước khuyết (lỗ lưới, khúc xuất lỗi) bằng phép liệt kê chính xác.
- Mỗi chuỗi luật được cắt thành "đơn vị" ngăn bởi các bước đã thấy là SAI (bước sai đặt lại Pending, nên các đơn vị độc lập
  với nhau). Bước khuyết = bước lưới 10 s nằm trong [đầu, cuối] lưới mà không có trong lưới xuất, hoặc thuộc khúc xuất lỗi.
- Đơn vị có k bước khuyết: liệt kê đủ 2^k cách điền (k <= CAP_BUOC), lấy tập khoảng cháy khác nhau. Tổ hợp các đơn vị bất
  định (tối đa CAP_TO_HOP), mỗi tổ hợp gom sự cố và đếm tử số như phép chấm đã khóa. Tử số duy nhất → chốt; nhiều giá trị
  → 'chua-phan-xu' kèm [min, max]. Không suy đoán theo trường hợp (sửa hai lỗi CX-36b ở v2c:134 và v2c:265).
- Bảng liệt kê sự cố (khoang_chay, su_co) dùng cách điền "mọi bước khuyết = sai" — trùng hành vi cũ (đóng khoảng ở bước
  khuyết đầu tiên, đặt lại Pending) nên không đổi kết quả cũ trên lưới liền.
"""
import pathlib
V2 = pathlib.Path(__file__).parent
s = (V2 / 'cham_offline_v2c.py').read_bytes().decode('utf-8')


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


def doan(dau, cuoi):
    """Cắt đoạn mã từ dòng bắt đầu bằng `dau` tới ngay trước dòng bắt đầu bằng `cuoi`."""
    global s
    i = s.index(dau); j = s.index(cuoi, i)
    return s[i:j]


rep('"""T-072 — bộ chấm offline v2c, từ v2_claude. Sửa phút đầu và thiếu lịch sử sau lỗ lưới.',
    '"""T-072 — bộ chấm offline v2d (Claude T-072, đáp CX-36b), từ v2c (Codex CX-36, giữ sửa phút đầu A).\n'
    'Bước khuyết: liệt kê chính xác mọi cách điền thay cho phép suy đoán của v2c (xem tao_v2d.py).')

# 1) danh_gia: thay toàn bộ bằng bản cắt đơn vị + liệt kê.
cu_danh_gia = doan('def danh_gia(bt, du, ng, day_sau_lo=None):', 'def _kc(L, k, t_hat, t_het, cat, tp):')
rep(cu_danh_gia, '''CAP_BUOC = 14      # tối đa bước khuyết mỗi đơn vị được liệt kê (2^14 cách điền)
CAP_TO_HOP = 4096  # tối đa tổ hợp giữa các đơn vị bất định


def _chuoi_khoang(seq, fs, t_cuoi):
    """seq: [(t, ok)] liên tiếp bước STEP; t_cuoi: bước SAI kết thúc đơn vị (None nếu hết lưới).
    Trả [(tp, t_hat, t_het)] đúng máy trạng thái của danh_gia: Pending ở bước đúng đầu, Alerting khi t - tp >= fs."""
    out, tp, firing, t_hat = [], None, False, None
    for t, ok in seq:
        if ok:
            if tp is None:
                tp = t
            if not firing and t - tp >= fs:
                firing, t_hat = True, t
        else:
            if firing:
                out.append((tp, t_hat, t))
            tp, firing = None, False
    if firing:
        out.append((tp, t_hat, t_cuoi))
    return out


def danh_gia_don_vi(bt, du, ng):
    """Trả (co_dinh, bat_dinh, qua_lon).
    co_dinh: khoảng cháy chắc chắn (đơn vị không có bước khuyết), dạng _kc.
    bat_dinh: [{'uid','loai','khoa','dau','cuoi','khuyet','lua_chon': [[_kc...] ...], 'mac_dinh': [_kc...]}]
              mac_dinh = cách điền mọi bước khuyết = SAI (bảng liệt kê).
    qua_lon: đơn vị có > CAP_BUOC bước khuyết: {'uid','loai','khoa','dau','cuoi','khuyet','mac_dinh'}."""
    luoi = sorted(du.luoi)
    co_dinh, bat_dinh, qua_lon = [], [], []
    if not luoi:
        return co_dinh, bat_dinh, qua_lon
    day_du = list(range(luoi[0], luoi[-1] + 1, STEP))
    co_luoi = set(luoi)
    for L in bt['luat']:
        ten = 'tin-hieu/' + L['uid']
        th, op, fs = nguong_cua(L, ng), L['dieu_kien']['phep'], L['for_s']
        trong_dung = L['no_data_state'] == 'Alerting'
        data = du.chuoi.get(ten, {})
        khoas = sorted(data) if data else ['']
        hong = du.hong.get(ten, set())
        for k in khoas:
            d = data.get(k, {})

            def gia(t):  # True / False / None (khuyết)
                if t not in co_luoi or t in hong:
                    return None
                v = d.get(t)
                return trong_dung if v is None else dung(op, v, th)
            # Pending (Claude T-072): tp = bước đúng đầu của dãy đúng liên tiếp; Alerting khi t - tp >= for_s. Khớp Grafana
            # trên 4 luật thử E3 (lệch -4 s, pha). Dãy đúng từ bước đầu lưới: quy_ve gắn 'pending-tu-dau-luoi'.
            don_vi = []
            for t in day_du:
                g = gia(t)
                if g is False:
                    if don_vi:
                        _them_don_vi(L, k, fs, don_vi, t, co_dinh, bat_dinh, qua_lon)
                    don_vi = []
                    continue
                don_vi.append((t, g))
            if don_vi:
                _them_don_vi(L, k, fs, don_vi, None, co_dinh, bat_dinh, qua_lon)
    return co_dinh, bat_dinh, qua_lon


def _them_don_vi(L, k, fs, don_vi, t_cuoi, co_dinh, bat_dinh, qua_lon):
    khuyet = [i for i, (t, g) in enumerate(don_vi) if g is None]
    cat = bool(khuyet) or t_cuoi is None

    def thanh_kc(ds):
        return [_kc(L, k, th, tt, cat, tp) for tp, th, tt in ds]
    mac_dinh = thanh_kc(_chuoi_khoang([(t, bool(g)) for t, g in don_vi], fs, t_cuoi))
    if not khuyet:
        co_dinh.extend(mac_dinh)
        return
    ve = {'uid': L['uid'], 'loai': L['loai'], 'khoa': k, 'dau': don_vi[0][0], 'cuoi': don_vi[-1][0],
          'khuyet': [don_vi[i][0] for i in khuyet], 'mac_dinh': mac_dinh}
    if len(khuyet) > CAP_BUOC:
        qua_lon.append(ve)
        return
    thay = {}
    for mask in range(1 << len(khuyet)):
        dien = {i: bool(mask >> j & 1) for j, i in enumerate(khuyet)}
        seq = [(t, dien[i] if g is None else g) for i, (t, g) in enumerate(don_vi)]
        ds = tuple(_chuoi_khoang(seq, fs, t_cuoi))
        thay.setdefault(ds, ds)
    ve['lua_chon'] = [thanh_kc(ds) for ds in thay]
    bat_dinh.append(ve)


def danh_gia(bt, du, ng, day_sau_lo=None):
    """Khoảng cháy của bảng liệt kê (mọi bước khuyết = SAI) — tương thích lời gọi cũ."""
    co_dinh, bat_dinh, qua_lon = danh_gia_don_vi(bt, du, ng)
    ra = co_dinh + [c for v in bat_dinh + qua_lon for c in v['mac_dinh']]
    return sorted(ra, key=lambda c: (c['t_hat'], c['uid'], c['khoa']))


''')

# 2) bỏ can_doi_chieu (thay bằng liệt kê trong cham).
cu_cdc = doan('def can_doi_chieu(kcs, day_sau_lo, phut_khoe):', 'def cham(bt, du, ng, phut, bat_dau=None):')
rep(cu_cdc, '''def _dem_tu_so(kcs, phut, t_dau, bat_dau, phut_khoe):
    """Tử số đúng phép chấm đã khóa: sự cố hệ thống (gom T072-gom-3) có phút chứa t̂ thuộc phut_khoe."""
    sus = quy_ve(gom([dict(c) for c in kcs]), phut, t_dau, bat_dau)
    return sum(x['loai'] == 'he-thong' and x['t_hat'] // 60 * 60 in phut_khoe for x in sus)


''')

# 3) cham: dùng danh_gia_don_vi + liệt kê tổ hợp.
cu_cham = doan('def cham(bt, du, ng, phut, bat_dau=None):', '# ---------- chọn ngưỡng ----------')
rep(cu_cham, '''def cham(bt, du, ng, phut, bat_dau=None):
    import itertools
    co_dinh, bat_dinh, qua_lon = danh_gia_don_vi(bt, du, ng)
    kcs = sorted(co_dinh + [c for v in bat_dinh + qua_lon for c in v['mac_dinh']],
                 key=lambda c: (c['t_hat'], c['uid'], c['khoa']))
    luoi = sorted(du.luoi)
    t_dau = luoi[0] if luoi else 0
    sus = quy_ve(gom(kcs), phut, t_dau, bat_dau)
    cac_phut = {t // 60 * 60 for t in luoi}
    phut_khoe = {m for m in cac_phut if (bat_dau is None or m >= bat_dau) and phut.lop(m) == KHOE}
    quan_sat = [q for q in sus if q['loai'] == 'quan-sat']
    dv_tp = {(v['uid'], v['khoa'], c['tp']) for v in bat_dinh + qua_lon for c in v['mac_dinh']}
    dem = {}
    for s_ in sus:
        if any((c['uid'], c['khoa'], c['tp']) in dv_tp for c in s_['canh_bao']):
            s_['co'].append('pending-sau-lo-luoi')
        if s_['lop'] == KHOE and s_['t_hat'] // 60 * 60 not in phut_khoe:
            s_['co'].append('phut-dau-ngoai-mau-so')
        if s_['loai'] == 'he-thong' and any(
                (q['t_het'] is None or s_['t_hat'] < q['t_het']) and
                (s_['t_het'] is None or q['t_hat'] < s_['t_het']) for q in quan_sat):
            s_['co'].append('chong-quan-sat')
        dem.setdefault(s_['loai'], {}).setdefault(s_['lop'], 0)
        dem[s_['loai']][s_['lop']] += 1
    pk = len(phut_khoe)
    # Tử số: liệt kê mọi tổ hợp cách điền của các đơn vị bất định (chỉ đơn vị hệ thống ảnh hưởng tử số).
    bd = [v for v in bat_dinh if v['loai'] == 'he-thong' and len(v['lua_chon']) > 1]
    co_dinh_ht = co_dinh + [c for v in bat_dinh if v not in bd for c in v['lua_chon'][0]]
    gia_tri, ly_do = set(), None
    so_to_hop = 1
    for v in bd:
        so_to_hop *= len(v['lua_chon'])
    ql = [v for v in qua_lon if v['loai'] == 'he-thong']
    if so_to_hop > CAP_TO_HOP:
        ly_do = f'qua-nhieu-to-hop ({so_to_hop})'
    else:
        for chon in itertools.product(*[v['lua_chon'] for v in bd]):
            gia_tri.add(_dem_tu_so(co_dinh_ht + [c for ds in chon for c in ds] + [c for v in ql for c in v['mac_dinh']],
                                   phut, t_dau, bat_dau, phut_khoe))
        for v in ql:  # đơn vị quá lớn: chỉ bỏ qua được nếu không thể chạm phút khỏe hay ghép với khoảng khác
            cham_khoe = any(v['dau'] - 59 <= m <= v['cuoi'] for m in phut_khoe)
            gan = any(c['t_hat'] <= v['cuoi'] + GHEP_S and (c['t_het'] is None or c['t_het'] + GHEP_S >= v['dau'])
                      for c in kcs if c['loai'] == 'he-thong' and (c['uid'], c['khoa']) != (v['uid'], v['khoa']))
            if cham_khoe or gan:
                ly_do = f"don-vi-qua-lon {v['uid']} [{v['dau']}, {v['cuoi']}] ({len(v['khuyet'])} bước khuyết)"
    ty = None
    n_liet_ke = sum(x['loai'] == 'he-thong' and x['t_hat'] // 60 * 60 in phut_khoe for x in sus)
    if ly_do or len(gia_tri) > 1:
        ty = {'su_co': None, 'phut_khoe_x1': pk, 'moi_6_gio': None, 'ci95_moi_6_gio': None,
              'du_6_gio': pk >= 360, 'trang_thai': 'chua-phan-xu', 'can_doi_chieu': 'lich-su-trang-thai-Grafana',
              'tu_so_kha_di': sorted(gia_tri) if gia_tri else None, 'ly_do': ly_do or 'nhieu-gia-tri-tu-so'}
    elif pk:
        n = gia_tri.pop() if gia_tri else n_liet_ke
        lo, hi = poisson_ci(n)
        ty = {'su_co': n, 'phut_khoe_x1': pk, 'moi_6_gio': n / (pk / 360), 'ci95_moi_6_gio': [lo / (pk / 360), hi / (pk / 360)],
              'du_6_gio': pk >= 360}
        if bd or ql:
            ty['ghi_chu'] = 'có bước khuyết nhưng mọi cách điền cho cùng tử số'
    don_vi = [{'uid': v['uid'], 'khoa': v['khoa'], 'dau': v['dau'], 'cuoi': v['cuoi'], 'so_khuyet': len(v['khuyet']),
               'so_lua_chon': len(v.get('lua_chon', [])) or None} for v in bat_dinh + qua_lon]
    return {'khoang_chay': kcs, 'su_co': sus, 'dem': dem, 'ty_le_khoe_x1': ty,
            'don_vi_bat_dinh': don_vi, 'so_buoc': len(luoi), 'so_phut': len(cac_phut)}


''')
(V2 / 'cham_offline_v2d.py').write_bytes(s.encode('utf-8'))
print('ok')
