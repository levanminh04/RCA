# -*- coding: utf-8 -*-
"""Tạo cham_offline_v2e.py từ cham_offline_v2d.py (giữ hash v2d). Claude T-072, lượt 15, theo DECISIONS 24/11 mục 2:
"dùng v2d khi lưới dữ liệu đủ; khi lưới khuyết báo 'chưa phân xử' và đếm riêng; dừng sửa tiếp".

v2e thêm:
1. Du.them: theo dõi theo từng chuỗi các bước có quan sát hợp lệ (bước trong cửa sổ file, ngoài khúc lỗi của chuỗi đó,
   có khóa chuỗi trong file). Bước khuyết của chuỗi = bước lưới không có quan sát hợp lệ ở BẤT KỲ file nào. Sửa CX-40b
   (khúc lỗi của một file che mẫu hợp lệ của file khác cùng thời gian).
2. Chế độ lưới khuyết: nếu một luật hệ thống có bước khuyết trong [bước đầu, bước cuối] của lưới, hoặc một phút khỏe ×1
   (theo bảng phân loại, từ đầu khoảng chấm) không có bước lưới nào → ty_le_khoe_x1 = chưa phân xử, tu_so_kha_di = None,
   kèm mục 'luoi_khuyet' đếm riêng (đoạn, bước, phút, phút khỏe bị ảnh hưởng). Không dùng phép liệt kê của v2d để kết luận
   khi lưới khuyết (CX-40 CHẶN 1–2). Bảng liệt kê (khoang_chay, su_co) giữ để tham khảo.
3. Cờ 'pending-sau-lo-luoi' chỉ gắn khi đơn vị có bước khuyết đứng TRƯỚC Pending của khoảng đó (CX-40, không chặn).
Khi lưới đủ: kết quả trùng v2d.
"""
import pathlib
V2 = pathlib.Path(__file__).parent
s = (V2 / 'cham_offline_v2d.py').read_bytes().decode('utf-8')


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


rep('"""T-072 — bộ chấm offline v2d (Claude T-072, đáp CX-36b)',
    '"""T-072 — bộ chấm offline v2e (Claude T-072, DECISIONS 24/11 mục 2; xem tao_v2e.py), từ v2d.\n'
    'Lưới đủ: như v2d. Lưới khuyết: chưa phân xử + đếm riêng. Sửa CX-40b (file chồng thời gian).\n\n'
    'Nguồn v2d: T-072 — bộ chấm offline v2d (Claude T-072, đáp CX-36b)')

rep("""    def __init__(self):
        self.chuoi, self.luoi, self.hong = {}, set(), {}

    def them(self, doc):
        s, e, st = doc['cua_so'][0], doc['cua_so'][1], doc.get('step_s', STEP)
        self.luoi |= set(range(s, e + 1, st))
        for lk in doc.get('loi_khuc', []):
            self.hong.setdefault(lk['ten'], set()).update(range(lk['start'], lk['end'] + 1, st))
        for ten, ds in doc['chuoi'].items():""", """    def __init__(self):
        self.chuoi, self.luoi, self.hong, self.ok = {}, set(), {}, {}

    def them(self, doc):
        s, e, st = doc['cua_so'][0], doc['cua_so'][1], doc.get('step_s', STEP)
        buoc = set(range(s, e + 1, st))
        self.luoi |= buoc
        loi = {}
        for lk in doc.get('loi_khuc', []):
            loi.setdefault(lk['ten'], set()).update(range(lk['start'], lk['end'] + 1, st))
        # v2e (CX-40b): bước có quan sát hợp lệ theo chuỗi; khuyết = không file nào cho quan sát hợp lệ.
        for ten in set(doc['chuoi']) | set(loi):
            self.ok.setdefault(ten, set())
            if ten in doc['chuoi']:
                self.ok[ten] |= buoc - loi.get(ten, set())
        self.hong = {ten: self.luoi - ok for ten, ok in self.ok.items()}
        for ten, ds in doc['chuoi'].items():""")

rep("""    dv_tp = {(v['uid'], v['khoa'], c['tp']) for v in bat_dinh + qua_lon for c in v['mac_dinh']}""",
    """    dv_tp = {(v['uid'], v['khoa'], c['tp']) for v in bat_dinh + qua_lon for c in v['mac_dinh']
             if any(t < c['tp'] for t in v['khuyet'])}  # v2e: chỉ khi bước khuyết đứng trước Pending""")

# Bọc cham của v2d.
rep("""def cham(bt, du, ng, phut, bat_dau=None):
    import itertools""", """def luoi_khuyet(bt, du, phut, bat_dau=None):
    \"\"\"Đếm riêng phần lưới khuyết (v2e). Trả None nếu lưới đủ cho mọi luật hệ thống và mọi phút khỏe trong khoảng chấm.\"\"\"
    luoi = sorted(du.luoi)
    phut_khoe_pl = sorted({m for a, b, l in phut.k if l == KHOE for m in range(-(-a // 60) * 60, b - 59, 60)
                           if bat_dau is None or m >= bat_dau})
    if not luoi:
        return {'ly_do': 'khong-co-luoi', 'phut_khoe_phan_loai': len(phut_khoe_pl)} if phut_khoe_pl else None
    day_du = set(range(luoi[0], luoi[-1] + 1, STEP))
    theo_luat, khuyet_ht = {}, set()
    for L in bt['luat']:
        ten = 'tin-hieu/' + L['uid']
        k = sorted((day_du - du.luoi) | (du.hong.get(ten, set()) & day_du))
        if k:
            theo_luat[L['uid']] = len(k)
            if L['loai'] == 'he-thong':
                khuyet_ht |= set(k)
    co_luoi = set(du.luoi)
    ngoai_luoi = [m for m in phut_khoe_pl if not any(t in co_luoi for t in range(m, m + 60, STEP))]
    if not khuyet_ht and not ngoai_luoi:
        return None
    doan, k = [], sorted(khuyet_ht)
    for t in k:
        if doan and t == doan[-1][1] + STEP:
            doan[-1][1] = t
        else:
            doan.append([t, t])
    phut_k = sorted({t // 60 * 60 for t in k})
    return {'ly_do': 'luoi-khuyet', 'so_buoc_khuyet_theo_luat': theo_luat, 'so_buoc_khuyet_he_thong': len(k),
            'doan_khuyet_he_thong': doan, 'so_doan': len(doan), 'so_phut_co_buoc_khuyet': len(phut_k),
            'so_phut_khoe_bi_anh_huong': len((set(phut_k) | set(ngoai_luoi)) & set(phut_khoe_pl)),
            'phut_khoe_ngoai_luoi': len(ngoai_luoi), 'phut_khoe_phan_loai': len(phut_khoe_pl)}


def cham(bt, du, ng, phut, bat_dau=None):
    kq = _cham_v2d(bt, du, ng, phut, bat_dau)
    lk = luoi_khuyet(bt, du, phut, bat_dau)
    if lk is not None:
        ty = kq['ty_le_khoe_x1'] or {}
        kq['ty_le_khoe_x1'] = {'su_co': None, 'tu_so_kha_di': None, 'phut_khoe_x1': None, 'moi_6_gio': None,
                               'ci95_moi_6_gio': None, 'du_6_gio': None, 'trang_thai': 'chua-phan-xu',
                               'ly_do': lk['ly_do'], 'can_doi_chieu': 'lich-su-trang-thai-Grafana',
                               'tham_khao_khong_dung_cho_R5': {'tu_so_bang_liet_ke': sum(
                                   x['loai'] == 'he-thong' and x['lop'] == KHOE and 'phut-dau-ngoai-mau-so' not in x['co']
                                   for x in kq['su_co']), 'phut_khoe_x1_tren_luoi': ty.get('phut_khoe_x1')}}
        kq['luoi_khuyet'] = lk
    else:
        kq['luoi_khuyet'] = None
    return kq


def _cham_v2d(bt, du, ng, phut, bat_dau=None):
    import itertools""")
(V2 / 'cham_offline_v2e.py').write_bytes(s.encode('utf-8'))
print('ok')
