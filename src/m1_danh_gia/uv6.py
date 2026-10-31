"""Điều kiện riêng UV-6 của E3 (dinh-chinh-cai-dat.md CĐ2; ma-tran-thu.json#/dieu_kien_rieng/E3;
dinh-nghia-pha2.json#/o_kich_hoat/E3). Cho cặp (c bỏ E3, c), đếm gộp trên các ca đưa vào, trong một thế giới.

- ca đang đúng: Hit@1(c bỏ E3) = 1; ca bị hỏng: ca đang đúng mà Hit@1(c) < 1;
- ca được sửa: lỗi mã (Nezha-OB, loại return hoặc exception), Hit@1(c bỏ E3) < 1 và Hit@1(c) = 1;
- vi phạm khi số ca bị hỏng lớn hơn số ca được sửa.
Báo kèm: số theo dataset; số ca lỗi mã có root lên hạng (hạng kỳ vọng giảm); bản theo Hit@1 kỳ vọng (CĐ2):
Σ phần giảm 1 − Hit@1(c) ở ca đang đúng, so với Σ phần tăng max(0, Hit@1(c) − Hit@1(c bỏ E3)) ở ca lỗi mã, gộp và theo
dataset, phân số chính xác.
Mỗi ca có thể mang `trong_so` (bội số, mặc định 1; SPEC T-045 bước 7): mọi số đếm tính theo bội số.
"""
from fractions import Fraction

LOI_MA = {'Nezha-OB': ('return', 'exception')}


def la_loi_ma(dataset, loai_loi):
    return loai_loi in LOI_MA.get(dataset, ())


def dem(ca):
    """ca: [{'dataset', 'loai_loi', 'hit1_tat', 'hit1_bat', 'hang_tat', 'hang_bat', 'trong_so'?}]."""
    co_w = {('trong_so' in c) for c in ca}
    if len(co_w) > 1:  # một phần ca mang bội số: không tự lấy 1 cho phần còn lại (S25)
        raise ValueError('chỉ một phần ca mang trong_so')
    hong = sua = len_hang = 0
    theo = {}
    ky_vong = {'giam_ca_dang_dung': Fraction(0), 'tang_ca_loi_ma': Fraction(0)}
    kv_theo = {}
    for c in ca:
        d = theo.setdefault(c['dataset'], {'hong': 0, 'sua': 0})
        kd = kv_theo.setdefault(c['dataset'], {'giam_ca_dang_dung': Fraction(0), 'tang_ca_loi_ma': Fraction(0)})
        ma = la_loi_ma(c['dataset'], c['loai_loi'])
        w = c.get('trong_so', 1)
        if isinstance(w, bool) or not isinstance(w, int) or w < 0:
            raise ValueError(f'trong_so phải là số nguyên không âm: {w!r}')
        for k in ('hit1_tat', 'hit1_bat'):
            if isinstance(c[k], bool) or not isinstance(c[k], (int, Fraction)):
                raise TypeError(f'{k} phải là phân số chính xác: {c[k]!r}')
        tat, bat = Fraction(c['hit1_tat']), Fraction(c['hit1_bat'])
        if c['hit1_tat'] == 1 and c['hit1_bat'] < 1:
            hong += w
            d['hong'] += w
        if tat == 1:
            for x in (ky_vong, kd):
                x['giam_ca_dang_dung'] += w * (1 - bat)
        if ma and c['hit1_tat'] < 1 and c['hit1_bat'] == 1:
            sua += w
            d['sua'] += w
        if ma:
            for x in (ky_vong, kd):
                x['tang_ca_loi_ma'] += w * max(Fraction(0), bat - tat)
        if ma and c['hang_tat'] is not None and c['hang_bat'] is not None and c['hang_bat'] < c['hang_tat']:
            len_hang += w
    return {'hong': hong, 'sua': sua, 'vi_pham': hong > sua, 'theo_dataset': theo, 'len_hang_loi_ma': len_hang,
            'ky_vong': dict(ky_vong, theo_dataset=kv_theo)}
