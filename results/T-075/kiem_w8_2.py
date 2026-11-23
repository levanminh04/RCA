"""T-075 (W8) — bộ kiểm ngoại tuyến bản 2 (`T075-kiem-2`), khuôn đầu ra `T075-ra-2`. Không gọi LLM, không mạng.
Bản 1 (`kiem_w8.py`) giữ nguyên. Sửa theo CX-30 R3, R4, CX-30b N1–N3 và điểm tự soát N2 (LOG phiên 2).

Trả {'hop_khuon': bool, 'loi': [...]}. `hop_khuon = False` nghĩa là đầu ra sai khuôn (thông báo phù hợp: "Không tạo
được giải thích hợp lệ"), khác với đầu ra đúng khuôn nhưng trượt phép kiểm nội dung.

  K0 khuôn: đúng tập khóa ở mọi cấp, đúng kiểu; `cau` có ít nhất 3 từ; không sập trên đầu vào lạ.
  K2 trích dẫn: con trỏ RFC 6901 vào `gui_di` phân giải được; `gia_tri` cùng kiểu JSON với nguồn (bool ≠ số),
     số so theo số chữ số đã viết.
  K3/K3b: tên thực thể và số trong câu có trong giá trị/con trỏ được trích của chính câu đó.
  K4 theo trạng thái đầu ra:
     - KHONG_DU_BANG_CHUNG: không `suy_luan`, không `giam_thieu`, có ≥ 1 mục thiếu (mọi gói).
     - GIAI_THICH: gói phải đủ (`phai_khong_du` = False); có ≥ 1 gợi ý; có ≥ 1 khẳng định trích một mục
       `/bang_chung/<i>` của thực thể nhóm hạng 1 với F_I = 1 (kênh tạo hạng).
  K4b: mục thiếu có `vang` (danh sách con trỏ khai vắng) thì mỗi con trỏ phải phân giải ra giá trị rỗng/null.
       Trích bảng có dữ liệu làm bối cảnh vẫn được.
  K5: gói ghi `do_phu.du_cua_so = false` thì phải có một MỤC THIẾU trích `/do_phu/du_cua_so` hoặc
      `/do_phu/thieu_bat_buoc…`.
  K6: `xep_hang_nhac_lai` là tiền tố (≥ 1 nhóm) của nhóm hạng trong gói; câu "X hạng k" (một thực thể) khớp gói.
  K7: không có mẫu chữ cấm.
Quy tắc "đủ bằng chứng" (`phai_khong_du`) bản 2 là ỨNG VIÊN, chưa có mục WHY: đủ khi ket_luan = CAUSE_FOUND,
trang_thai_chay = OK, và MỌI thực thể nhóm hạng 1 có ≥ 1 mục bằng chứng F_I = 1 trong gói. Nhánh H5 của V082
(thực thể chết im được đẩy lên đầu, không qua kênh F_I) sẽ bị coi là không đủ — thận trọng, chưa có ca thử.
Giới hạn còn lại: so chữ, không hiểu nghĩa câu.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # chạy được với `py -I`
from goi_bang_chung_2 import MAU_CAM  # noqa: E402

KHUON_RA = 'T075-ra-2'
TRANG_THAI = {'GIAI_THICH', 'KHONG_DU_BANG_CHUNG'}
LOAI_KD = {'quan_sat', 'suy_luan'}
LOAI_GY = {'kiem_tra', 'thu_them_du_lieu', 'giam_thieu'}
KHOA_GOC = {'khuon', 'trang_thai', 'xep_hang_nhac_lai', 'khang_dinh', 'goi_y_xu_ly', 'thieu_bang_chung'}
KHOA_KD = ({'id', 'loai', 'cau', 'trich_dan'}, set())
KHOA_GY = ({'id', 'loai', 'cau', 'can_cu'}, set())
KHOA_TH = ({'cau', 'trich_dan'}, {'vang'})
SO_MIEN = {300}
RE_BC = re.compile(r'^/bang_chung/(\d+)(?:/|$)')


def phan_giai(goc, con_tro):
    if not isinstance(con_tro, str) or not con_tro.startswith('/'):
        return False, None
    x = goc
    for tok in con_tro[1:].split('/'):
        tok = tok.replace('~1', '/').replace('~0', '~')
        if isinstance(x, dict) and tok in x:
            x = x[tok]
        elif isinstance(x, list) and tok.isdigit() and int(tok) < len(x):
            x = x[int(tok)]
        else:
            return False, None
    return True, x


def phai_khong_du(goi):
    kq = goi['ket_qua_rca']
    if kq.get('ket_luan') != 'CAUSE_FOUND' or kq.get('trang_thai_chay') != 'OK':
        return True
    nhom1 = set(kq.get('nhom_hang_1') or [])
    co = {b.get('thuc_the') for b in goi.get('bang_chung') or [] if b.get('F_I') == 1}
    return not nhom1 or not nhom1 <= co


def nhom_hang(goi):
    nhom, cu = [], None
    for r in goi['ket_qua_rca']['xep_hang']:
        if r['hang'] != cu:
            nhom.append([])
            cu = r['hang']
        nhom[-1].append(r['thuc_the'])
    return [sorted(g) for g in nhom]


def tap_thuc_the(goi):
    u = {r['thuc_the'] for r in goi['ket_qua_rca']['xep_hang']}
    u |= {b['thuc_the'] for b in goi.get('bang_chung') or []}
    sm = goi.get('so_mau_theo_thuc_the') or {}
    for k in ('span', 'log'):
        u |= set((sm.get(k) or {}).keys())
    for m in (goi.get('do_phu') or {}).get('thieu_bat_buoc') or []:
        u.add(m.rsplit(':', 1)[-1])
    return u


def _ten_trong(text, ten):
    return re.search(r'(?<![\w-])' + re.escape(ten) + r'(?![\w-])', text) is not None


def _cac_so(text):
    out = []
    for m in re.finditer(r'(?<![\w.,-])-?\d+(?:[.,]\d+)?(?![\w-])', text):
        s = m.group(0).replace(',', '.')
        d = len(s.split('.')[1]) if '.' in s else 0
        out.append((float(s), d, m.group(0)))
    return out


def _so_trong(x):
    if isinstance(x, bool):
        return []
    if isinstance(x, (int, float)):
        return [float(x)]
    if isinstance(x, dict):
        return [v for y in x.values() for v in _so_trong(y)]
    if isinstance(x, list):
        return [float(len(x))] + [v for y in x for v in _so_trong(y)]
    return []


def _khop_so(viet, d, thuc):
    return round(thuc, d) == round(viet, d) if d else abs(thuc - viet) < 0.5


def _la_so(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _khop_gia_tri(viet, thuc):
    if _la_so(viet) and _la_so(thuc):
        s = repr(float(viet))
        d = len(s.split('.')[1]) if '.' in s and not s.endswith('.0') else 0
        return _khop_so(float(viet), d, float(thuc))
    if isinstance(viet, bool) or isinstance(thuc, bool):
        return isinstance(viet, bool) and isinstance(thuc, bool) and viet == thuc
    return type(viet) is type(thuc) and viet == thuc


def _chuoi(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield str(k)
            yield from _chuoi(v)
    elif isinstance(x, list):
        for v in x:
            yield from _chuoi(v)


def _kiem_khuon(ra):
    """K0. Trả danh sách lỗi khuôn; rỗng thì các khối có đúng kiểu để đọc tiếp."""
    L = []
    if not isinstance(ra, dict):
        return ['K0: đầu ra không phải đối tượng JSON']
    if set(ra) != KHOA_GOC:
        L.append(f'K0: khóa gốc {sorted(set(ra) ^ KHOA_GOC)} lệch khuôn')
        return L
    if ra['khuon'] != KHUON_RA:
        L.append(f'K0: khuôn {ra["khuon"]!r} khác {KHUON_RA}')
    if ra['trang_thai'] not in TRANG_THAI:
        L.append(f'K0: trạng thái lạ {ra["trang_thai"]!r}')
    xh = ra['xep_hang_nhac_lai']
    if not (isinstance(xh, list) and xh and all(isinstance(g, list) and g and all(isinstance(e, str) for e in g)
                                                 for g in xh)):
        L.append('K0: xep_hang_nhac_lai phải là danh sách khác rỗng các nhóm tên')
    for ten, (bat, tuy), kd, loai in (('khang_dinh', KHOA_KD, 'trich_dan', LOAI_KD),
                                      ('goi_y_xu_ly', KHOA_GY, 'can_cu', LOAI_GY),
                                      ('thieu_bang_chung', KHOA_TH, 'trich_dan', None)):
        ds = ra[ten]
        if not isinstance(ds, list):
            L.append(f'K0: {ten} không phải danh sách')
            continue
        for j, m in enumerate(ds):
            w = f'{ten}[{j}]'
            if not isinstance(m, dict):
                L.append(f'K0: {w} không phải đối tượng')
                continue
            if not bat <= set(m) <= bat | tuy:
                L.append(f'K0: {w} khóa {sorted(set(m) ^ bat)} lệch khuôn')
                continue
            if not isinstance(m['cau'], str) or len(m['cau'].split()) < 3:
                L.append(f'K0: {w}.cau rỗng hoặc dưới 3 từ')
            if loai is not None and m['loai'] not in loai:
                L.append(f'K0: {w}.loai {m["loai"]!r}')
            td = m[kd]
            if not (isinstance(td, list) and td and all(
                    isinstance(t, dict) and 'con_tro' in t and set(t) <= {'con_tro', 'gia_tri'}
                    and isinstance(t['con_tro'], str) for t in td)):
                L.append(f'K0: {w}.{kd} phải là danh sách khác rỗng {{con_tro[, gia_tri]}}')
            if 'vang' in m and not (isinstance(m['vang'], list) and all(isinstance(v, str) for v in m['vang'])):
                L.append(f'K0: {w}.vang phải là danh sách con trỏ')
    return L


def kiem(goi, ra):
    try:
        lk = _kiem_khuon(ra)
    except Exception as e:  # không để bộ kiểm sập
        lk = [f'K0: lỗi đọc đầu ra {type(e).__name__}']
    if lk:
        return {'hop_khuon': False, 'loi': lk}
    loi = []
    L = lambda ma, s: loi.append(f'{ma}: {s}')  # noqa: E731
    muc = ([('khang_dinh', m, 'trich_dan') for m in ra['khang_dinh']]
           + [('goi_y_xu_ly', m, 'can_cu') for m in ra['goi_y_xu_ly']]
           + [('thieu_bang_chung', m, 'trich_dan') for m in ra['thieu_bang_chung']])
    U = tap_thuc_the(goi)
    hang_cua = {}
    for r in goi['ket_qua_rca']['xep_hang']:
        hang_cua.setdefault(r['thuc_the'], r['hang'])
    so_hang = {float(r['hang']) for r in goi['ket_qua_rca']['xep_hang']}

    for nhom, m, kd in muc:
        cau, id_ = m['cau'], m.get('id', '-')
        gtr = []
        for td in m[kd]:
            ok, v = phan_giai(goi, td['con_tro'])
            if not ok:
                L('K2', f'{nhom} {id_}: con trỏ không tồn tại {td["con_tro"]!r}')
                continue
            if 'gia_tri' in td and not _khop_gia_tri(td['gia_tri'], v):
                L('K2', f'{nhom} {id_}: giá trị {td["gia_tri"]!r} khác gói {v!r} tại {td["con_tro"]}')
            gtr.append(v)
        blob = json.dumps([gtr, [td['con_tro'] for td in m[kd]]], ensure_ascii=False)
        for ten in sorted(U, key=len, reverse=True):
            if _ten_trong(cau, ten) and not _ten_trong(blob, ten):
                L('K3', f'{nhom} {id_}: nhắc {ten!r} nhưng giá trị trích dẫn không chứa')
        so_goc = [v for g in gtr for v in _so_trong(g)]
        for viet, d, raw in _cac_so(cau):
            if d == 0 and (viet in SO_MIEN or (viet in so_hang and re.search(r'hạng\s*' + re.escape(raw), cau))):
                continue
            if not any(_khop_so(viet, d, t) for t in so_goc):
                L('K3b', f'{nhom} {id_}: số {raw!r} không có trong giá trị trích dẫn')
        for mh in re.finditer(r'hạng\s*(\d+)', cau):
            nhac = [t for t in U if t in hang_cua and _ten_trong(cau, t)]
            if len(nhac) == 1 and hang_cua[nhac[0]] != int(mh.group(1)):
                L('K6', f'{nhom} {id_}: {nhac[0]} hạng {mh.group(1)} nhưng gói ghi {hang_cua[nhac[0]]}')

    # K4 theo trạng thái đầu ra
    if ra['trang_thai'] == 'KHONG_DU_BANG_CHUNG':
        if any(m['loai'] == 'suy_luan' for m in ra['khang_dinh']):
            L('K4', 'KHONG_DU_BANG_CHUNG nhưng có khẳng định suy_luan')
        if any(m['loai'] == 'giam_thieu' for m in ra['goi_y_xu_ly']):
            L('K4', 'KHONG_DU_BANG_CHUNG nhưng có gợi ý giam_thieu')
        if not ra['thieu_bang_chung']:
            L('K4', 'KHONG_DU_BANG_CHUNG nhưng không nêu phần thiếu')
    else:
        if phai_khong_du(goi):
            L('K4', 'gói không đủ bằng chứng nhưng đầu ra trả GIAI_THICH')
        if not ra['goi_y_xu_ly']:
            L('K4', 'GIAI_THICH nhưng không có gợi ý xử lý')
        nhom1 = set(goi['ket_qua_rca'].get('nhom_hang_1') or [])
        bc = goi.get('bang_chung') or []
        tao_hang = False
        for m in ra['khang_dinh']:
            for td in m['trich_dan']:
                mm = RE_BC.match(td['con_tro'])
                if mm and int(mm.group(1)) < len(bc):
                    b = bc[int(mm.group(1))]
                    tao_hang |= b.get('thuc_the') in nhom1 and b.get('F_I') == 1
        if not tao_hang:
            L('K4', 'GIAI_THICH nhưng không khẳng định nào trích mục bằng chứng F_I = 1 của nhóm hạng 1')

    # K4b
    for j, m in enumerate(ra['thieu_bang_chung']):
        for ct in m.get('vang', []):
            ok, v = phan_giai(goi, ct)
            if not ok:
                L('K4b', f'thieu_bang_chung[{j}]: con trỏ vắng {ct!r} không tồn tại')
            elif v not in (None, [], {}, ''):
                L('K4b', f'thieu_bang_chung[{j}]: khai {ct} vắng nhưng gói có dữ liệu')

    # K5
    dp = goi.get('do_phu')
    if dp and dp.get('du_cua_so') is False:
        nhan = any(td['con_tro'] == '/do_phu/du_cua_so' or td['con_tro'].startswith('/do_phu/thieu_bat_buoc')
                   for m in ra['thieu_bang_chung'] for td in m['trich_dan'])
        if not nhan:
            L('K5', 'gói thiếu phủ cửa sổ nhưng không mục thiếu nào trích /do_phu/du_cua_so hay /do_phu/thieu_bat_buoc')

    # K6
    goc = nhom_hang(goi)
    nl = [sorted(g) for g in ra['xep_hang_nhac_lai']]
    if nl != goc[:len(nl)]:
        L('K6', f'xep_hang_nhac_lai {nl} khác gói {goc[:len(nl)]}')

    # K7
    for s in _chuoi(ra):
        for mau in MAU_CAM:
            if re.search(mau, s):
                L('K7', f'mẫu cấm {mau!r} trong {s[:60]!r}')
    return {'hop_khuon': True, 'loi': loi}


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        g = json.load(f)
    g = g.get('gui_di', g)
    with open(sys.argv[2], encoding='utf-8') as f:
        r = json.load(f)
    kq = kiem(g, r)
    print(json.dumps({'dat': kq['hop_khuon'] and not kq['loi'], **kq}, ensure_ascii=False, indent=1))
    sys.exit(0 if kq['hop_khuon'] and not kq['loi'] else 1)
