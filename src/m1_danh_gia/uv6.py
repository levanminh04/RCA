"""Điều kiện riêng UV-6 của E3 (dinh-chinh-cai-dat.md CĐ2; ma-tran-thu.json#/dieu_kien_rieng/E3;
dinh-nghia-pha2.json#/o_kich_hoat/E3). Cho cặp (c bỏ E3, c), đếm gộp trên các ca đưa vào, trong một thế giới.

- ca đang đúng: Hit@1(c bỏ E3) = 1; ca bị hỏng: ca đang đúng mà Hit@1(c) < 1;
- ca được sửa: lỗi mã (Nezha-OB, loại return hoặc exception), Hit@1(c bỏ E3) < 1 và Hit@1(c) = 1;
- vi phạm khi số ca bị hỏng lớn hơn số ca được sửa.
Báo kèm: số theo dataset; số ca lỗi mã có root lên hạng (hạng kỳ vọng giảm).
Mỗi ca có thể mang `trong_so` (bội số, mặc định 1; SPEC T-045 bước 7): mọi số đếm tính theo bội số.
"""
LOI_MA = {'Nezha-OB': ('return', 'exception')}


def la_loi_ma(dataset, loai_loi):
    return loai_loi in LOI_MA.get(dataset, ())


def dem(ca):
    """ca: [{'dataset', 'loai_loi', 'hit1_tat', 'hit1_bat', 'hang_tat', 'hang_bat', 'trong_so'?}]."""
    hong = sua = len_hang = 0
    theo = {}
    for c in ca:
        d = theo.setdefault(c['dataset'], {'hong': 0, 'sua': 0})
        ma = la_loi_ma(c['dataset'], c['loai_loi'])
        w = c.get('trong_so', 1)
        if c['hit1_tat'] == 1 and c['hit1_bat'] < 1:
            hong += w
            d['hong'] += w
        if ma and c['hit1_tat'] < 1 and c['hit1_bat'] == 1:
            sua += w
            d['sua'] += w
        if ma and c['hang_tat'] is not None and c['hang_bat'] is not None and c['hang_bat'] < c['hang_tat']:
            len_hang += w
    return {'hong': hong, 'sua': sua, 'vi_pham': hong > sua, 'theo_dataset': theo, 'len_hang_loi_ma': len_hang}
