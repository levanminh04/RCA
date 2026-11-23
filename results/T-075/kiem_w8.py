"""T-075 (W8) — bộ kiểm ngoại tuyến cho đầu ra giải thích. Không gọi LLM, không gọi mạng.

Đầu vào: gói (`gui_di` của goi_bang_chung.py) và một đầu ra theo khuôn T075-ra-1 (khuon-dau-ra.md).
Trả danh sách lỗi theo mã phép kiểm; rỗng = đạt.

Phép kiểm:
  K1 cấu trúc: khóa bắt buộc, giá trị enum, mỗi khẳng định/gợi ý/mục thiếu có ≥ 1 trích dẫn.
  K2 trích dẫn tồn tại: mọi con trỏ (RFC 6901, gốc là `gui_di`) phân giải được; `gia_tri` nếu có thì khớp giá trị
     tại con trỏ (số so theo số chữ số thập phân đã viết).
  K3 thực thể có căn cứ: mọi tên thực thể của gói nhắc trong câu phải có trong giá trị được trích dẫn của câu đó.
  K3b số có căn cứ: mọi số trong câu phải khớp một số trong giá trị được trích (theo số chữ số đã viết), trừ số hạng
     và biên cửa sổ 300.
  K4 không đủ bằng chứng: nếu gói không đủ (`phai_khong_du`) thì trạng thái phải là KHONG_DU_BANG_CHUNG, không có
     khẳng định loại suy_luan, không có gợi ý giam_thieu, và có ≥ 1 mục `thieu_bang_chung`.
  K4b vắng mặt có thật: mục `thieu_bang_chung` trích nguyên khối `/bang_chung` hoặc `/ke_thua` thì khối đó phải rỗng.
  K5 độ phủ: nếu gói ghi `do_phu.du_cua_so = false` thì đầu ra phải trích ít nhất một con trỏ dưới `/do_phu`.
  K6 giữ thứ hạng: `xep_hang_nhac_lai` là tiền tố (≥ 1 nhóm) của các nhóm hạng trong gói, đúng thứ tự và thành phần;
     câu nào nói "hạng k" cho đúng một thực thể thì hạng đó phải khớp gói.
  K7 chữ cấm: không có mẫu chữ cấm (nhãn, đường dẫn, sổ tiêm, tên lượt) trong mọi chuỗi của đầu ra.
Giới hạn: K3/K3b là phép so chữ, không hiểu nghĩa câu; câu đúng chữ vẫn có thể suy luận sai. Không thay người đọc.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # chạy được với `py -I`
from goi_bang_chung import MAU_CAM  # noqa: E402

KHUON_RA = 'T075-ra-1'
TRANG_THAI = {'GIAI_THICH', 'KHONG_DU_BANG_CHUNG'}
LOAI_KD = {'quan_sat', 'suy_luan'}
LOAI_GY = {'kiem_tra', 'thu_them_du_lieu', 'giam_thieu'}
SO_MIEN = {300}


def phan_giai(goc, con_tro):
    """RFC 6901. Trả (ok, giá trị)."""
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
    """Quy tắc tất định: gói không đủ để giải thích nguyên nhân khi lõi không kết luận CAUSE_FOUND, chạy lỗi,
    hoặc không có mục bằng chứng nào cho thực thể của nhóm hạng 1."""
    kq = goi['ket_qua_rca']
    if kq.get('ket_luan') != 'CAUSE_FOUND' or kq.get('trang_thai_chay') != 'OK':
        return True
    nhom1 = set(kq.get('nhom_hang_1') or [])
    return not any(b.get('thuc_the') in nhom1 for b in goi.get('bang_chung') or [])


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
    """Số trong câu (dấu phẩy hoặc chấm thập phân). Bỏ số nằm trong tên (vd. t072, p95, latency-50)."""
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
        out = [float(len(x))]
        return out + [v for y in x for v in _so_trong(y)]
    return []


def _khop_so(viet, d, thuc):
    return round(thuc, d) == round(viet, d) if d else abs(thuc - viet) < 0.5


def _khop_gia_tri(viet, thuc):
    if isinstance(viet, (int, float)) and not isinstance(viet, bool) and isinstance(thuc, (int, float)):
        s = repr(float(viet))
        d = len(s.split('.')[1]) if '.' in s and not s.endswith('.0') else 0
        return _khop_so(float(viet), d, float(thuc))
    return viet == thuc


def _chuoi(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _chuoi(v)
    elif isinstance(x, list):
        for v in x:
            yield from _chuoi(v)


def kiem(goi, ra):
    loi = []
    L = lambda ma, s: loi.append(f'{ma}: {s}')  # noqa: E731

    # K1
    for k in ('khuon', 'trang_thai', 'xep_hang_nhac_lai', 'khang_dinh', 'goi_y_xu_ly', 'thieu_bang_chung'):
        if k not in ra:
            L('K1', f'thiếu khóa {k}')
    if loi:
        return loi
    if ra['khuon'] != KHUON_RA:
        L('K1', f'khuôn {ra["khuon"]!r} khác {KHUON_RA}')
    if ra['trang_thai'] not in TRANG_THAI:
        L('K1', f'trạng thái lạ {ra["trang_thai"]!r}')
    muc = ([('khang_dinh', m, 'trich_dan') for m in ra['khang_dinh']]
           + [('goi_y_xu_ly', m, 'can_cu') for m in ra['goi_y_xu_ly']]
           + [('thieu_bang_chung', m, 'trich_dan') for m in ra['thieu_bang_chung']])
    for nhom, m, kd in muc:
        if not m.get(kd):
            L('K1', f'{nhom} {m.get("id")}: không có trích dẫn')
        if nhom == 'khang_dinh' and m.get('loai') not in LOAI_KD:
            L('K1', f'khang_dinh {m.get("id")}: loại {m.get("loai")!r}')
        if nhom == 'goi_y_xu_ly' and m.get('loai') not in LOAI_GY:
            L('K1', f'goi_y_xu_ly {m.get("id")}: loại {m.get("loai")!r}')

    U = tap_thuc_the(goi)
    hang_cua = {}
    for r in goi['ket_qua_rca']['xep_hang']:
        hang_cua.setdefault(r['thuc_the'], r['hang'])
    so_hang = {float(r['hang']) for r in goi['ket_qua_rca']['xep_hang']}
    tat_ca_con_tro = []

    for nhom, m, kd in muc:
        cau = m.get('cau', '')
        gia_tri_trich = []
        for td in m.get(kd) or []:
            ct = td.get('con_tro')
            tat_ca_con_tro.append(ct)
            ok, v = phan_giai(goi, ct)
            if not ok:
                L('K2', f'{nhom} {m.get("id")}: con trỏ không tồn tại {ct!r}')
                continue
            if 'gia_tri' in td and not _khop_gia_tri(td['gia_tri'], v):
                L('K2', f'{nhom} {m.get("id")}: giá trị {td["gia_tri"]!r} khác gói {v!r} tại {ct}')
            gia_tri_trich.append(v)
        # Con trỏ trỏ vào khóa mang tên thực thể (vd. /so_mau_theo_thuc_the/span/payment-service) cũng là căn cứ.
        blob = json.dumps([gia_tri_trich, [td.get('con_tro') for td in m.get(kd) or []]], ensure_ascii=False)
        # K3
        for ten in sorted(U, key=len, reverse=True):
            if _ten_trong(cau, ten) and not _ten_trong(blob, ten):
                L('K3', f'{nhom} {m.get("id")}: nhắc {ten!r} nhưng giá trị trích dẫn không chứa')
        # K3b
        so_goc = [v for g in gia_tri_trich for v in _so_trong(g)]
        for viet, d, raw in _cac_so(cau):
            if d == 0 and (viet in SO_MIEN or (viet in so_hang and re.search(r'hạng\s*' + re.escape(raw), cau))):
                continue
            if not any(_khop_so(viet, d, t) for t in so_goc):
                L('K3b', f'{nhom} {m.get("id")}: số {raw!r} không có trong giá trị trích dẫn')
        # K6 (câu)
        for mh in re.finditer(r'hạng\s*(\d+)', cau):
            nhac = [t for t in U if t in hang_cua and _ten_trong(cau, t)]
            if len(nhac) == 1 and hang_cua[nhac[0]] != int(mh.group(1)):
                L('K6', f'{nhom} {m.get("id")}: {nhac[0]} hạng {mh.group(1)} nhưng gói ghi {hang_cua[nhac[0]]}')

    # K4
    khong_du = phai_khong_du(goi)
    if khong_du:
        if ra['trang_thai'] != 'KHONG_DU_BANG_CHUNG':
            L('K4', 'gói không đủ bằng chứng nhưng đầu ra không trả KHONG_DU_BANG_CHUNG')
        if any(m.get('loai') == 'suy_luan' for m in ra['khang_dinh']):
            L('K4', 'gói không đủ bằng chứng nhưng có khẳng định suy_luan')
        if any(m.get('loai') == 'giam_thieu' for m in ra['goi_y_xu_ly']):
            L('K4', 'gói không đủ bằng chứng nhưng có gợi ý giam_thieu')
        if not ra['thieu_bang_chung']:
            L('K4', 'không đủ bằng chứng nhưng không nêu phần thiếu')
    elif ra['trang_thai'] == 'GIAI_THICH':
        if not any(str(c).startswith(('/bang_chung', '/ke_thua')) for c in tat_ca_con_tro):
            L('K4', 'GIAI_THICH nhưng không trích dẫn /bang_chung hay /ke_thua')

    # K4b: mục "thiếu" trích nguyên khối /bang_chung hoặc /ke_thua làm căn cứ vắng mặt thì khối đó phải rỗng.
    for m in ra['thieu_bang_chung']:
        for td in m.get('trich_dan') or []:
            ct = td.get('con_tro')
            if ct in ('/bang_chung', '/ke_thua'):
                ok, v = phan_giai(goi, ct)
                if ok and v:
                    L('K4b', f'mục thiếu trích {ct} làm căn cứ vắng mặt nhưng gói có {len(v)} mục')

    # K5
    dp = goi.get('do_phu')
    if dp and dp.get('du_cua_so') is False and not any(str(c).startswith('/do_phu') for c in tat_ca_con_tro):
        L('K5', 'gói thiếu phủ cửa sổ nhưng đầu ra không trích /do_phu')

    # K6 (danh sách)
    goc = nhom_hang(goi)
    nl = [sorted(g) for g in ra['xep_hang_nhac_lai']]
    if not nl:
        L('K6', 'xep_hang_nhac_lai rỗng')
    elif nl != goc[:len(nl)]:
        L('K6', f'xep_hang_nhac_lai {nl} khác gói {goc[:len(nl)]}')

    # K7
    for s in _chuoi(ra):
        for m in MAU_CAM:
            if re.search(m, s):
                L('K7', f'mẫu cấm {m!r} trong {s[:60]!r}')
    return loi


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        g = json.load(f)
    g = g.get('gui_di', g)
    with open(sys.argv[2], encoding='utf-8') as f:
        r = json.load(f)
    kq = kiem(g, r)
    print(json.dumps({'dat': not kq, 'loi': kq}, ensure_ascii=False, indent=1))
    sys.exit(0 if not kq else 1)
