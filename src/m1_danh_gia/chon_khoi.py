"""Luật chọn khối (SPEC T-043 B4 "Luật chọn khối" bước 1–12; ma-tran-thu.json#/luat_chon_khoi; fixture 45–50;
dinh-chinh-cai-dat.md CĐ6.3, CĐ6.4). Chạy sau ghép nhãn.

Tên cấu hình: 'R0' khi không bật thành phần nào; còn lại là tên thành phần nối bằng '+' theo thứ tự `thanh_phan`.
`cap` có khóa 'a|b' (b = a thêm đúng một thành phần, hoặc a = R0) và giá trị là kết cục luật C (chuỗi) hoặc kết
quả `luat_c.ket_hop_the_gioi` (dict; khối K dùng 'can_cu_loai' và 'ket_cuc_dung').
- Lượt một: loại c khi (R0, c) HẠI, hoặc có x đang bật mà (c bỏ x, c) HẠI. Còn lại là tập cố định.
- Lượt hai: với thành phần ít ca x đang tắt trong c, nếu c thêm x thuộc tập cố định và (c, c thêm x) cho
  KHÔNG ĐỦ CA thì loại c; xét độc lập từng c.
- Cặp TRÁI CHIỀU theo dataset: chỉ gắn cờ cho cấu hình có thành phần bật thêm (b của 'a|b'); trình Minh khi cờ ở
  cấu hình thắng hoặc ở cấu hình có MRR cao hơn cấu hình thắng.
- Chọn trong tập gần tốt nhất (MRR không thấp hơn MRR cao nhất còn lại quá 0,01): ít thành phần nhất; rồi MRR cao
  hơn; rồi thứ tự E1, E2, E5, E3. Cấu hình thắng không có thành phần đồ thị thì trình Minh kèm cấu hình có đồ thị
  tốt nhất còn lại và mức chênh.
"""
from fractions import Fraction

GAN_TOT_NHAT = Fraction(1, 100)
THU_TU = ('E1', 'E2', 'E5', 'E3')


def tap(ten):
    return frozenset() if ten == 'R0' else frozenset(ten.split('+'))


def ten(s, thanh_phan):
    ds = [x for x in thanh_phan if x in s]
    return '+'.join(ds) if ds else 'R0'


def _kc(v):
    """Kết cục dùng: chuỗi giữ nguyên; dict của ket_hop_the_gioi lấy 'ket_cuc_dung'."""
    if isinstance(v, dict):
        return v['ket_cuc_dung']
    return 'KHONG_DU_CA' if v == 'PHU_THUOC_QUAN_SAT' else v


def _la_hai(v):
    if isinstance(v, dict):
        return bool(v['can_cu_loai'])
    return v == 'HAI'


def _khoa_thu_tu(s, thanh_phan, thu_tu):
    pos = {x: i for i, x in enumerate(list(thu_tu) + [x for x in thanh_phan if x not in thu_tu])}
    return sorted(pos[x] for x in s)


def chon(thanh_phan, it_ca, do_thi, MRR, cap, thu_tu=THU_TU, nguong=GAN_TOT_NHAT):
    thanh_phan = list(thanh_phan)
    for k, v in MRR.items():
        # số thực làm sai phép so tại biên 0,01 (CĐ16): không tự đổi, báo lỗi
        if isinstance(v, bool) or not isinstance(v, (Fraction, int)):
            raise TypeError(f'MRR của {k} phải là phân số chính xác, nhận {type(v).__name__}')
    MRR = {k: Fraction(v) for k, v in MRR.items()}
    cfg = sorted(MRR)
    thieu = set()

    def cap_cua(a, b):
        k = f'{a}|{b}'
        if k not in cap:
            thieu.add(k)
            return None
        return cap[k]

    loai1 = set()
    for c in cfg:
        s = tap(c)
        if c != 'R0' and _la_hai(cap_cua('R0', c) or ''):
            loai1.add(c)
            continue
        for x in s:
            v = cap_cua(ten(s - {x}, thanh_phan), c)
            if v is not None and _la_hai(v):
                loai1.add(c)
                break
    co_dinh = [c for c in cfg if c not in loai1]
    loai2 = set()
    for c in co_dinh:
        s = tap(c)
        for x in it_ca:
            if x in s:
                continue
            c2 = ten(s | {x}, thanh_phan)
            if c2 in co_dinh:
                v = cap_cua(c, c2)
                if v is not None and _kc(v) == 'KHONG_DU_CA':
                    loai2.add(c)
                    break
    con = [c for c in co_dinh if c not in loai2]
    co_trai_chieu = sorted(k for k, v in cap.items() if _kc(v) == 'TRAI_CHIEU_DATASET')
    out = {'co_dinh': co_dinh, 'loai_luot_mot': sorted(loai1), 'loai_luot_hai': sorted(loai2), 'con_lai': con,
           'co_trai_chieu': co_trai_chieu, 'thieu_cap': sorted(thieu), 'trinh_Minh': False, 'ly_do_trinh_Minh': [],
           'cau_hinh_do_thi_tot_nhat': None, 'chenh': None}
    if not con:
        out.update(chon=None, gan_tot_nhat=[], trinh_Minh=True, ly_do_trinh_Minh=['xung_dot_khong_con_cau_hinh'])
        return out
    best = max(MRR[c] for c in con)
    gan = [c for c in con if best - MRR[c] <= nguong]
    thang = min(gan, key=lambda c: (len(tap(c)), -MRR[c], _khoa_thu_tu(tap(c), thanh_phan, thu_tu)))
    out.update(chon=thang, gan_tot_nhat=sorted(gan))
    gan_co = {k.split('|')[1] for k in co_trai_chieu}
    if thang in gan_co or any(MRR[c] > MRR[thang] for c in gan_co if c in MRR):
        out['trinh_Minh'] = True
        out['ly_do_trinh_Minh'].append('trai_chieu_dataset')
    if not (tap(thang) & set(do_thi)):
        out['trinh_Minh'] = True
        out['ly_do_trinh_Minh'].append('khong_co_thanh_phan_do_thi')
        dt = [c for c in con if tap(c) & set(do_thi)]
        if dt:
            g = min(dt, key=lambda c: (-MRR[c], len(tap(c)), _khoa_thu_tu(tap(c), thanh_phan, thu_tu)))
            out['cau_hinh_do_thi_tot_nhat'] = g
            out['chenh'] = MRR[g] - MRR[thang]
    return out


def kiem_cau_hinh_thang(thang, thanh_phan, cap):
    """Bước 8 (CĐ6.3): đảo từng thành phần x của khối tại cấu hình thắng; xét cặp (thắng không x, thắng có x).
    Cặp phụ thuộc quan sát xử lý như KHÔNG ĐỦ CA (CĐ6.3, D2f), kể cả khi `cap` là kết quả khối K (giữ kết cục tại P).
    Chỉ áp ở bước này; các bước khác của khối K vẫn đọc `ket_cuc_dung` (cách áp ở bước 5 chờ Minh quyết)."""
    w = tap(thang)
    out = {'xung_dot': [], 'trinh_Minh': [], 'nhat_quan': [], 'thieu_cap': []}
    for x in thanh_phan:
        k = f'{ten(w - {x}, thanh_phan)}|{ten(w | {x}, thanh_phan)}'
        if k not in cap:
            out['thieu_cap'].append(x)
            continue
        v = cap[k]
        v = 'KHONG_DU_CA' if isinstance(v, dict) and v['phu_thuoc_quan_sat'] else _kc(v)
        if v in ('TRAI_CHIEU_DATASET', 'TRAI_CHIEU_O'):
            out['trinh_Minh'].append(x)
        elif x in w:
            out['nhat_quan' if v in ('GIUP', 'KHONG_DU_CA') else 'xung_dot'].append(x)
        else:
            out['nhat_quan' if v in ('HAI', 'KHONG_TAC_DUNG') else 'xung_dot'].append(x)
    return {k: sorted(v) for k, v in out.items()}
