"""Luật chọn khối (SPEC T-043 B4 "Luật chọn khối" bước 1–12; ma-tran-thu.json#/luat_chon_khoi; fixture 45–50;
dinh-chinh-cai-dat.md CĐ6.3, CĐ6.4). Chạy sau ghép nhãn.

Tên cấu hình: 'R0' khi không bật thành phần nào; còn lại là tên thành phần nối bằng '+' theo thứ tự `thanh_phan`.
`cap` có khóa 'a|b' (b = a thêm đúng một thành phần, hoặc a = R0) và giá trị là kết cục luật C (chuỗi) hoặc kết
quả `luat_c.ket_hop_the_gioi` (dict; khối K dùng 'can_cu_loai' và 'ket_cuc_dung').
- Đầu vào phải đủ: `MRR` có đúng 2^n cấu hình; mọi cặp luật cần có mặt; `it_ca`, `do_thi` là danh sách con của
  `thanh_phan`. Thiếu hay sai là lỗi, không chọn (S17; dinh-chinh-cai-dat.md C7, G1).
- Lượt một: loại c khi (R0, c) HẠI, hoặc có x đang bật mà (c bỏ x, c) HẠI. Còn lại là tập cố định.
- Lượt hai: với thành phần ít ca x đang tắt trong c, nếu c thêm x thuộc tập cố định và (c, c thêm x) cho
  KHÔNG ĐỦ CA thì loại c; xét độc lập từng c. Cặp phụ thuộc quan sát đọc là KHÔNG ĐỦ CA, kể cả khi kết cục tại P
  là HẠI (bước 4 không loại vì phụ thuộc quan sát), nên thành phần ít ca như vậy được giữ bật (D2a).
- Cặp TRÁI CHIỀU theo dataset: chỉ gắn cờ cho cấu hình có thành phần bật thêm (b của 'a|b'); trình Minh khi cờ ở
  cấu hình thắng hoặc ở cấu hình có MRR cao hơn cấu hình thắng.
- Chọn trong tập gần tốt nhất (MRR không thấp hơn MRR cao nhất còn lại quá 0,01): ít thành phần nhất; rồi MRR cao
  hơn; rồi thứ tự E1, E2, E5, E3. Cấu hình thắng không có thành phần đồ thị thì trình Minh kèm cấu hình có đồ thị
  tốt nhất còn lại và mức chênh.
"""
from fractions import Fraction
from itertools import combinations

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


def _kc_ptqs(v):
    """Kết cục dùng ở bước 5 và bước 8: cặp phụ thuộc quan sát đọc là KHÔNG ĐỦ CA (D2f; SPEC T-043 dòng 898;
    Minh duyệt 30/10/2026, dinh-chinh-cai-dat.md C5); cặp khác như `_kc`."""
    if isinstance(v, dict) and v['phu_thuoc_quan_sat']:
        return 'KHONG_DU_CA'
    return _kc(v)


def _la_hai(v):
    if isinstance(v, dict):
        return bool(v['can_cu_loai'])
    return v == 'HAI'


def _khoa_thu_tu(s, thanh_phan, thu_tu):
    pos = {x: i for i, x in enumerate(list(thu_tu) + [x for x in thanh_phan if x not in thu_tu])}
    return sorted(pos[x] for x in s)


def chon(thanh_phan, it_ca, do_thi, MRR, cap, thu_tu=THU_TU, nguong=GAN_TOT_NHAT, the_gioi='P'):
    """the_gioi: 'P' (mặc định) hoặc 'S_lo', 'S_hi' cho bước 10 (C8, S36). Ở S_lo, S_hi mọi giá trị của `cap` phải là
    kết quả `luat_c.ket_hop_the_gioi`; kết cục dùng là kết cục tại đúng thế giới đó (`theo_the_gioi[w]`, không đọc phụ
    thuộc quan sát, vì đó là phép so giữa các thế giới); `MRR` phải là MRR của thế giới đó."""
    if the_gioi not in ('P', 'S_lo', 'S_hi'):
        raise ValueError(f'thế giới lạ: {the_gioi!r}')
    if the_gioi != 'P':
        if not all(isinstance(v, dict) for v in cap.values()):
            raise ValueError('chọn ở S_lo, S_hi cần kết quả ket_hop_the_gioi cho mọi cặp')
        cap = {k: v['theo_the_gioi'][the_gioi] for k, v in cap.items()}
    thanh_phan = list(thanh_phan)
    for k, v in MRR.items():
        # số thực làm sai phép so tại biên 0,01 (CĐ16): không tự đổi, báo lỗi
        if isinstance(v, bool) or not isinstance(v, (Fraction, int)):
            raise TypeError(f'MRR của {k} phải là phân số chính xác, nhận {type(v).__name__}')
    MRR = {k: Fraction(v) for k, v in MRR.items()}
    for nhan_ds, ds_tp in (('it_ca', it_ca), ('do_thi', do_thi)):
        if isinstance(ds_tp, str) or not set(ds_tp) <= set(thanh_phan):
            raise ValueError(f'{nhan_ds} phải là danh sách con của thanh_phan: {ds_tp!r}')
    du = {ten(set(s), thanh_phan) for r in range(len(thanh_phan) + 1) for s in combinations(thanh_phan, r)}
    if set(MRR) != du:
        raise ValueError(f'MRR phải có đủ {len(du)} cấu hình; thiếu {sorted(du - set(MRR))}, lạ {sorted(set(MRR) - du)}')
    cfg = sorted(MRR)
    # S17: mọi cặp luật cần phải có trước khi áp luật: (R0, c) và (c bỏ x, c) cho mọi c và mọi x đang bật trong c. Các
    # cặp (c, c thêm x) của lượt hai là (c′ bỏ x, c′) với c′ = c thêm x nên đã nằm trong tập này.
    can = set()
    for c in cfg:
        s = tap(c)
        if c != 'R0':
            can.add(f'R0|{c}')
        for x in s:
            can.add(f'{ten(s - {x}, thanh_phan)}|{c}')
    if sorted(can - set(cap)):
        raise ValueError(f'thiếu cặp cho luật chọn khối: {sorted(can - set(cap))}')
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
                if v is not None and _kc_ptqs(v) == 'KHONG_DU_CA':
                    loai2.add(c)
                    break
    con = [c for c in co_dinh if c not in loai2]
    co_trai_chieu = sorted(k for k, v in cap.items() if _kc(v) == 'TRAI_CHIEU_DATASET')
    out = {'the_gioi': the_gioi, 'co_dinh': co_dinh, 'loai_luot_mot': sorted(loai1), 'loai_luot_hai': sorted(loai2), 'con_lai': con,
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


def kiem_cau_hinh_thang(thang, thanh_phan, cap, it_ca):
    """Bước 8 (CĐ6.3): đảo từng thành phần x của khối tại cấu hình thắng; xét cặp (thắng không x, thắng có x).
    Cặp phụ thuộc quan sát của thành phần ít ca xử lý như KHÔNG ĐỦ CA (D2a, D2f), như bước 5 (`_kc_ptqs`). Thành phần
    không ít ca không bị ép bật (SPEC T-043 dòng 898): cặp phụ thuộc quan sát của nó ghi 'phu_thuoc_quan_sat' và trình
    Minh, không gọi là nhất quán hay xung đột (dinh-chinh-cai-dat.md C7, Q1). Bước 4 không loại vì phụ thuộc quan sát
    (`can_cu_loai`)."""
    if isinstance(it_ca, str) or not set(it_ca) <= set(thanh_phan):
        raise ValueError(f'it_ca phải là danh sách con của thanh_phan: {it_ca!r}')
    w = tap(thang)
    out = {'xung_dot': [], 'trinh_Minh': [], 'nhat_quan': [], 'phu_thuoc_quan_sat': [], 'thieu_cap': []}
    for x in thanh_phan:
        k = f'{ten(w - {x}, thanh_phan)}|{ten(w | {x}, thanh_phan)}'
        if k not in cap:
            raise ValueError(f'thiếu cặp cho bước 8: {k}')
        v = cap[k]
        if isinstance(v, dict) and v['phu_thuoc_quan_sat'] and x not in it_ca:
            out['phu_thuoc_quan_sat'].append(x)
            out['trinh_Minh'].append(x)
            continue
        v = _kc_ptqs(v)
        if v in ('TRAI_CHIEU_DATASET', 'TRAI_CHIEU_O'):
            out['trinh_Minh'].append(x)
        elif x in w:
            out['nhat_quan' if v in ('GIUP', 'KHONG_DU_CA') else 'xung_dot'].append(x)
        else:
            out['nhat_quan' if v in ('HAI', 'KHONG_TAC_DUNG') else 'xung_dot'].append(x)
    return {k: sorted(v) for k, v in out.items()}
