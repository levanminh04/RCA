"""Danh mục kênh, severity, lớp tín hiệu (đặc tả v1 §5; SPEC T-043 B1.4, B2 E3; hop-dong.json#/kenh, #/severity;
Đ15; dinh-chinh-cai-dat.md CĐ4, CĐ5).

Nhóm đơn vị và hướng chấm:
- op_full (E1 tắt): lên, E3 bật thêm xuống; lan ngược ở cả hai hướng (D21).
- op_excl (E1 bật): lên, E3 bật thêm xuống; không lan.
- canh (E2): lên; không lan.
- metric: theo lớp của hồ sơ nguồn và bảng lop_huong (hop-dong.json); tỷ lệ thành công chỉ chấm khi E3 bật.
- log_loi (E3 tắt): lên; lan ngược. mau_loi, mau_moi (E3 bật): lên; lan ngược. mau_thuong: xuống; lan xuôi.
- tan_suat (E3b): lên lan ngược; xuống lan xuôi.
"""
from m1 import e3
from m1.span import dem_thao_tac  # noqa: F401  (E3b dùng chung với span)

LOP_HUONG = {'tài nguyên': {'len': 'khong_lan', 'xuong': 'lan_xuoi'},
             'độ trễ': {'len': 'lan_nguoc'},
             'lỗi': {'len': 'lan_nguoc'},
             'lưu lượng': {'len': 'lan_nguoc', 'xuong': 'lan_xuoi'},
             'tỷ lệ thành công': {'xuong': 'lan_nguoc'}}


def chuan_hoa_severity(v, ho_so):
    """hop-dong.json#/severity: chỉ giá trị chuỗi; bỏ khoảng trắng hai đầu, đổi chữ hoa; ngoài ánh xạ là UNKNOWN."""
    if not isinstance(v, str):
        return e3.UNKNOWN
    s = v.strip().upper()
    if not s:
        return e3.UNKNOWN
    if s in ho_so['loi']:
        return e3.LOI
    if s in ho_so['khong_loi']:
        return e3.KHONG_LOI
    return e3.UNKNOWN


def lop_goc(ten_lop):
    """'độ trễ (frontend)' → 'độ trễ' (hop-dong.json dòng 61 gắn ghi chú thực thể vào tên lớp)."""
    return ten_lop.split(' (')[0]


def huong_cham(nhom, E3_bat, lop_metric=None):
    if nhom in ('op_full', 'op_excl'):
        return ['len', 'xuong'] if E3_bat else ['len']
    if nhom in ('canh', 'log_loi', 'mau_loi', 'mau_moi'):
        return ['len']
    if nhom == 'mau_thuong':
        return ['xuong']
    if nhom == 'tan_suat':
        return ['len', 'xuong']
    if nhom == 'metric':
        g = lop_goc(lop_metric)
        if g == 'tỷ lệ thành công':
            return ['xuong'] if E3_bat else []
        return sorted(LOP_HUONG[g], key=lambda d: 0 if d == 'len' else 1)
    raise ValueError(f'nhóm lạ: {nhom}')


def lop(nhom, huong, lop_metric=None):
    if nhom == 'op_full':
        return 'lan_nguoc'
    if nhom in ('op_excl', 'canh'):
        return 'khong_lan'
    if nhom in ('log_loi', 'mau_loi', 'mau_moi'):
        return 'lan_nguoc'
    if nhom == 'mau_thuong':
        return 'lan_xuoi'
    if nhom == 'tan_suat':
        return 'lan_nguoc' if huong == 'len' else 'lan_xuoi'
    if nhom == 'metric':
        return LOP_HUONG[lop_goc(lop_metric)][huong]
    raise ValueError(f'nhóm lạ: {nhom}')


def lop_metric(ten_cot, ho_so):
    """Lớp của một cột metric theo hồ sơ nguồn (CĐ5): 'hau_to' (RE2-TT) hoặc 'ten_kenh' (Nezha-OB). Phần sau dấu
    '_' đầu tiên là hậu tố/tên kênh. Không có trong bảng: None (bản ghi ERROR ở tầng gọi)."""
    km = ho_so['kenh_metric']
    if '_' not in ten_cot:
        return None
    duoi = ten_cot.split('_', 1)[1]
    return km['bang'].get(duoi)


def so_dong_vao_drain(dem):
    """Mọi dòng, kể cả UNKNOWN, đi vào Drain khi E3 bật (SPEC B2 E3)."""
    return dem['dong']


def don_vi_log_loi(dem_N, dem_A, T_N, T_A, ts, kieu):
    """Kênh log lỗi cơ bản (E3 tắt, D2d) cho một thực thể. dem = {'dong', 'xac_dinh', 'loi'}.
    Kênh dựa trên severity: N có dòng nhưng không dòng nào xác định là NO_BASELINE; ở A là NO_A."""
    from m1.e4 import cham_dem
    ep = None
    if kieu == 'severity':
        if dem_N['dong'] > 0 and dem_N['xac_dinh'] == 0:
            ep = 'NO_BASELINE'
        elif dem_A['dong'] > 0 and dem_A['xac_dinh'] == 0:
            ep = 'NO_A'
    kq = cham_dem(dem_N['loi'], dem_A['loi'], T_N, T_A, ts, trang_thai_ep=ep, huong_cham=('len',))
    kq['cham'] = kq['trang_thai'] == 'OK'
    kq['do_phu'] = {p: (d['xac_dinh'] / d['dong'] if d['dong'] else None) for p, d in (('N', dem_N), ('A', dem_A))}
    kq['ten_kenh'] = 'mật độ dòng lỗi có severity xác định' if kieu == 'severity' else 'mật độ dòng log lỗi'
    return kq


def dem_log_theo_thuc_the(dong, quy_tac):
    """{thực thể: {'dong', 'xac_dinh', 'loi', 'unknown'}} cho một phía."""
    out = {}
    for d in dong:
        c = out.setdefault(d['thuc_the'], {'dong': 0, 'xac_dinh': 0, 'loi': 0, 'unknown': 0})
        c['dong'] += 1
        l = e3._lop_dong(d, quy_tac)
        if l == e3.UNKNOWN:
            c['unknown'] += 1
        else:
            c['xac_dinh'] += 1
            c['loi'] += int(l == e3.LOI)
    return out


def don_vi_log(dong_N, dong_A, quy_tac, E3_bat, tham_so_E3=None):
    """Đơn vị đếm của log. E3 tắt: một đơn vị 'log_loi' mỗi thực thể có log. E3 bật: đơn vị theo mẫu Drain và ô mẫu
    mới (không có kênh log lỗi cơ bản, hop-dong.json dòng 51)."""
    if not E3_bat:
        N = dem_log_theo_thuc_the(dong_N, quy_tac)
        A = dem_log_theo_thuc_the(dong_A, quy_tac)
        rong = {'dong': 0, 'xac_dinh': 0, 'loi': 0, 'unknown': 0}
        out = []
        for e in sorted(set(N) | set(A)):
            dn, da = N.get(e, rong), A.get(e, rong)
            out.append({'thuc_the': e, 'nhom': 'log_loi', 'ten': 'log_loi', 'n_N': dn['loi'], 'n_A': da['loi'],
                        'dem_N': dn, 'dem_A': da, 'huong_cham': ['len'], 'lop': {'len': 'lan_nguoc'},
                        'kieu_quy_tac': quy_tac['kieu']})
        return out
    return don_vi_mau_drain(e3.hoc_va_dem(dong_N, dong_A, tham_so_E3 or {}, quy_tac))


def don_vi_mau_drain(kq):
    """Đơn vị từ kết quả Drain: cặp lớp lỗi → mau_loi (lên); lớp thường → mau_thuong (xuống); không xác định → không
    có kênh (Đ15 điểm 3); ô mẫu mới mỗi thực thể có log (n_N = 0 vì Drain học trên N)."""
    out = []
    for (e, cid), c in sorted(kq['cap'].items()):
        if c['lop'] == 'loi':
            out.append({'thuc_the': e, 'nhom': 'mau_loi', 'ten': f'mau:{cid}', 'n_N': c['n_N'], 'n_A': c['n_A'],
                        'huong_cham': ['len'], 'lop': {'len': 'lan_nguoc'}, 'mau': kq['mau'].get(cid)})
        elif c['lop'] == 'thuong':
            out.append({'thuc_the': e, 'nhom': 'mau_thuong', 'ten': f'mau:{cid}', 'n_N': c['n_N'], 'n_A': c['n_A'],
                        'huong_cham': ['xuong'], 'lop': {'xuong': 'lan_xuoi'}, 'mau': kq['mau'].get(cid)})
    for e in sorted(set(kq['thuc_the_N']) | set(kq['mau_moi'])):
        out.append({'thuc_the': e, 'nhom': 'mau_moi', 'ten': 'mau_moi', 'n_N': 0, 'n_A': kq['mau_moi'].get(e, 0),
                    'huong_cham': ['len'], 'lop': {'len': 'lan_nguoc'}})
    return out
