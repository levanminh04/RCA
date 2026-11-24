# -*- coding: utf-8 -*-
"""Ca giả W4 v2d (Claude T-072, đáp CX-36b). Chạy từ gốc repo: py -3 -X utf8 -B results/T-072/v2/thu_ca_gia_v2d.py [--ghi]

Gồm: ca A và D của Codex (CX-36) chạy trên v2d; hai ca CX-36b làm hồi quy; đối chứng "chuỗi đủ" cho mọi ca lỗ (điền tay
từng cách, chạy trên lưới liền); hồi quy bộ cũ thu_ca_gia.py (9 ca, so len(khoang_chay)) và tu_kiem() của v2d.
Một khác biệt có chủ ý so với kỳ vọng của thu_ca_gia_v2c.py ghi rõ ở ca D4.
"""
import argparse
import subprocess
import sys
from contextlib import redirect_stdout
from io import BytesIO, TextIOWrapper
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
import cham_offline_v2d as moi
import thu_ca_gia as cu

CODE = Path(__file__).resolve()
so = cu.doi_chieu


def chay(luoi, dung_tai, bat_dau, phut=None, loai='he-thong'):
    """luoi: các bước có trong lưới xuất; dung_tai(t) -> bool cho giá trị luật giả (> 0)."""
    luat = {'uid': 'gia', 'loai': loai, 'for_s': 60, 'no_data_state': 'OK', 'dieu_kien': {'phep': '>', 'nguong': 0}}
    du = moi.Du()
    du.luoi = set(luoi)
    du.chuoi['tin-hieu/gia'] = {'': {t: int(dung_tai(t)) for t in du.luoi}}
    ph = moi.Phut(phut or {'khoang': [[0, max(luoi) + 10, moi.KHOE]]})
    return moi.cham({'luat': [luat]}, du, {}, ph, bat_dau)


def khoang(*ds):
    return lambda t: any(a <= t < b for a, b in ds)


def tu_so(kq):
    ty = kq['ty_le_khoe_x1']
    return ty['su_co'] if ty.get('trang_thai') != 'chua-phan-xu' else ('chua-phan-xu', ty['tu_so_kha_di'])


def ca_A():
    kq = chay(range(0, 180, 10), khoang((20, 100)), 70)
    sc, = kq['su_co']
    so((sc['t_hat'], sc['t_het'], sc['lop'], len(kq['khoang_chay'])), (80, 100, moi.KHOE, 1))
    so((kq['ty_le_khoe_x1']['su_co'], kq['ty_le_khoe_x1']['phut_khoe_x1']), (0, 1))
    so('phut-dau-ngoai-mau-so' in sc['co'], True)
    kq = chay(range(0, 180, 10), khoang((60, 140)), 70)
    so((kq['su_co'][0]['t_hat'], tu_so(kq)), (120, 1))
    return 'A (CX-36) | đầu chấm 70 s, Alerting 80 s: liệt kê, không vào tử số (0/1 phút); đối chứng Alerting 120 s: 1.'


def ca_D():
    du = range(0, 300, 10)
    khuyet = [t for t in du if not 30 <= t <= 110]
    # D1 chuỗi đủ: hai cách thật cho 0 và 1.
    so(tu_so(chay(du, khoang((30, 240)), 180)), 0)
    so(tu_so(chay(du, khoang((120, 240)), 180)), 1)
    # D2 lỗ 30–110, đúng 120–240, đầu chấm 180: chưa phân xử {0, 1}; bảng liệt kê giữ t̂ 180.
    kq = chay(khuyet, khoang((120, 240)), 180)
    sc, = kq['su_co']
    so((sc['t_hat'], 'pending-sau-lo-luoi' in sc['co'], tu_so(kq)), (180, True, ('chua-phan-xu', [0, 1])))
    # D3 dãy ngắn sau lỗ (đúng 120–150), đầu chấm 120: chưa phân xử {0, 1}; không khoảng cháy trong bảng.
    kq = chay(khuyet, khoang((120, 150)), 120)
    so((len(kq['khoang_chay']), tu_so(kq)), (0, ('chua-phan-xu', [0, 1])))
    # D4 KHÁC v2c: lỗ 30–110, bước 120 thấy SAI, đúng 130–240, đầu chấm 180.
    #   v2c chốt 1. Nhưng nếu 30–110 đúng, có khoảng cháy [90, 120) và sự cố 190 ghép vào (190 <= 120 + 300) → t̂ = 90,
    #   ngoài phút được tính → tử số 0 (quy-tac-gom.json#/gom_su_co, đã khóa). Đối chứng chuỗi đủ xác nhận cả hai giá trị.
    so(tu_so(chay(du, khoang((30, 120), (130, 240)), 180)), 0)
    so(tu_so(chay(du, khoang((130, 240)), 180)), 1)
    kq = chay(khuyet, khoang((130, 240)), 180)
    so((kq['su_co'][0]['t_hat'], tu_so(kq)), (190, ('chua-phan-xu', [0, 1])))
    # D5 cảnh báo quan sát không góp tử số.
    so(tu_so(chay(khuyet, khoang((120, 240)), 180, loai='quan-sat')), 0)
    # D6 lỗ một bước 130, đúng 140–240, đầu chấm 120: hai mốc 190/200 cùng phút khỏe → chốt 1.
    kq = chay([t for t in du if t != 130], khoang((140, 240)), 120)
    so(('pending-sau-lo-luoi' in kq['su_co'][0]['co'], tu_so(kq)), (True, 1))
    # D7 hai bên biên gom 300 s: chuỗi đủ cho 1 và 2; lỗ 320–390 → chưa phân xử {1, 2}.
    dai = range(0, 600, 10)
    so(tu_so(chay(dai, khoang((0, 90), (320, 500)), 0)), 1)
    so(tu_so(chay(dai, khoang((0, 90), (400, 500)), 0)), 2)
    kq = chay([t for t in dai if not 320 <= t < 400], khoang((0, 90), (400, 500)), 0)
    so(tu_so(kq), ('chua-phan-xu', [1, 2]))
    return 'D (CX-36) | D1–D3, D5–D7 như v2c; D4 khác v2c có chủ ý: chưa phân xử {0, 1} (ghép 300 s qua lỗ), đối chứng chuỗi đủ.'


def ca_cx36b_1():
    # Đầu chấm 60; đúng 20–70; khuyết 80; sai từ 90. Điền đúng: Alerting 80 → 1/2; điền sai: 0/2.
    luoi = [t for t in range(0, 180, 10) if t != 80]
    so(tu_so(chay(range(0, 180, 10), khoang((20, 90)), 60)), 1)
    so(tu_so(chay(range(0, 180, 10), khoang((20, 80)), 60)), 0)
    kq = chay(luoi, khoang((20, 80)), 60)
    so((kq['ty_le_khoe_x1']['phut_khoe_x1'], tu_so(kq)), (2, ('chua-phan-xu', [0, 1])))
    return 'CX-36b-1 | Pending có thể vào Alerting ngay trong lỗ (bước 80) rồi hết ở mẫu kế: chưa phân xử {0, 1} (v2c chốt 0).'


def ca_cx36b_2():
    # Phút [0,120) khỏe, [120,180) flash, [180,300) khỏe. Đúng 50–290, khuyết 110.
    # Điền đúng: Alerting 110 (phút 60, khỏe); điền sai: Alerting 180 (phút 180, khỏe). Cả hai: tử số 1.
    ph = {'khoang': [[0, 120, moi.KHOE], [120, 180, 'flash'], [180, 300, moi.KHOE]]}
    so(tu_so(chay(range(0, 300, 10), khoang((50, 300)), 0, ph)), 1)
    so(tu_so(chay(range(0, 300, 10), khoang((50, 110), (120, 300)), 0, ph)), 1)
    kq = chay([t for t in range(0, 300, 10) if t != 110], khoang((50, 300)), 0, ph)
    so((tu_so(kq), kq['ty_le_khoe_x1'].get('ghi_chu')), (1, 'có bước khuyết nhưng mọi cách điền cho cùng tử số'))
    return 'CX-36b-2 | hai mốc Alerting khả dĩ 110/180 đều thuộc phút khỏe (phút flash ở giữa không là mốc khả dĩ): chốt 1 (v2c báo chưa phân xử).'


def hoi_quy():
    p = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(cu.CODE)], capture_output=True, encoding='utf-8', check=True)
    dong_cu = [d for d in p.stdout.splitlines() if d.startswith('ĐẠT |')]
    so(len(dong_cu), 9)
    cham_that = moi.cham
    so_khoang = []

    def cham_va_dem(*a, **kw):
        kq = cham_that(*a, **kw)
        so_khoang.append(len(kq['khoang_chay']))
        return kq
    with (patch.object(cu, 'cham', moi), patch.object(cu.gt, 'cham', moi), patch.object(moi, 'cham', cham_va_dem),
          patch.object(cu, 'CODE', CODE), patch.object(sys, 'argv', [str(CODE)]),
          TextIOWrapper(BytesIO(), encoding='utf-8') as buf, redirect_stdout(buf)):
        cu.main()
        buf.flush()
        dong_moi = [d for d in buf.buffer.getvalue().decode().splitlines() if d.startswith('ĐẠT |')]
    so(dong_moi, dong_cu)
    so(so_khoang, [0, 1] + [2] * 6)
    so(moi.tu_kiem(moi.nap(moi.GOC / 'bieu-thuc.json')), [])
    return ['Bộ gốc thu_ca_gia.py đạt 9/9; chạy lại trên v2d:'] + dong_moi + [
        f'ĐẠT | len(khoang_chay) hai ca cửa sổ và sáu ca giao = {so_khoang}.', 'ĐẠT | tu_kiem() của v2d trả [].']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ghi', action='store_true')
    a = ap.parse_args()
    ma = [CODE, moi.CODE, cu.CODE, cu.gt.CODE, cu.cham.CODE, CODE.parent / 'tao_v2d.py', CODE.parent / 'cham_offline_v2c.py']
    dong = [f'SHA-256 {p.name} {moi.sha(p)}' for p in ma]
    dong += ['ĐẠT | ' + f() for f in (ca_A, ca_D, ca_cx36b_1, ca_cx36b_2)] + hoi_quy()
    vb = ('\n'.join(dong) + '\n').encode('utf-8')
    if a.ghi:
        with (moi.RA / 'thu-ca-gia-v2d.txt').open('xb') as f:
            f.write(vb)
    sys.stdout.buffer.write(vb)


if __name__ == '__main__':
    if sys.argv[1:2] == ['--cli-thieu-ticket']:
        del sys.argv[1]
        with patch.object(cu, 'cham', moi):
            sys.exit(cu.cli_thieu_ticket())
    main()
