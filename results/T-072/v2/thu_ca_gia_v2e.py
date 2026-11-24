# -*- coding: utf-8 -*-
"""Ca giả W4 v2e (Claude T-072, lượt 15). Chạy từ gốc repo: py -3 -X utf8 -B results/T-072/v2/thu_ca_gia_v2e.py [--ghi]

Kiểm: (1) lưới đủ → v2e trùng v2d (ty_le_khoe_x1, su_co, khoang_chay); (2) lưới khuyết → 'chua-phan-xu',
tu_so_kha_di = None, đếm riêng 'luoi_khuyet' (ca D có lỗ, CX-40 CHẶN 1 hai ca, CHẶN 2); (3) CX-40b hai file chồng thời
gian; (4) cờ 'pending-sau-lo-luoi' theo thứ tự thời gian; (5) hồi quy bộ cũ 9 ca (len(khoang_chay)) và tu_kiem().
"""
import argparse
import subprocess
import sys
from contextlib import redirect_stdout
from io import BytesIO, TextIOWrapper
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
import cham_offline_v2d as v2d
import cham_offline_v2e as moi
import thu_ca_gia as cu

CODE = Path(__file__).resolve()
so = cu.doi_chieu
LUAT = {'uid': 'gia', 'loai': 'he-thong', 'for_s': 60, 'no_data_state': 'OK', 'dieu_kien': {'phep': '>', 'nguong': 0}}


def du_tu(bo, luoi, dung_tai):
    du = bo.Du()
    du.luoi = set(luoi)
    du.chuoi['tin-hieu/gia'] = {'': {t: int(dung_tai(t)) for t in du.luoi}}
    return du


def chay(bo, luoi, dung_tai, bat_dau, phut=None, loai='he-thong', ph_max=None):
    du = du_tu(bo, luoi, dung_tai)
    ph = bo.Phut(phut or {'khoang': [[0, (ph_max or max(luoi) + 10), bo.KHOE]]})
    return bo.cham({'luat': [dict(LUAT, loai=loai)]}, du, {}, ph, bat_dau)


def khoang(*ds):
    return lambda t: any(a <= t < b for a, b in ds)


def chua(kq):
    ty = kq['ty_le_khoe_x1']
    return ty['trang_thai'] == 'chua-phan-xu' and ty['tu_so_kha_di'] is None and ty['su_co'] is None


def ca_luoi_du():
    """Lưới đủ: v2e trùng v2d từng trường trên mọi ca lưới đủ của bộ v2d."""
    ds = [(range(0, 180, 10), khoang((20, 100)), 70), (range(0, 180, 10), khoang((60, 140)), 70),
          (range(0, 300, 10), khoang((30, 240)), 180), (range(0, 300, 10), khoang((120, 240)), 180),
          (range(0, 300, 10), khoang((30, 120), (130, 240)), 180), (range(0, 300, 10), khoang((130, 240)), 180),
          (range(0, 600, 10), khoang((0, 90), (320, 500)), 0), (range(0, 600, 10), khoang((0, 90), (400, 500)), 0)]
    for luoi, f, bd in ds:
        a, b = chay(v2d, luoi, f, bd), chay(moi, luoi, f, bd)
        so(b['luoi_khuyet'], None)
        so((b['ty_le_khoe_x1'], b['su_co'], b['khoang_chay']), (a['ty_le_khoe_x1'], a['su_co'], a['khoang_chay']))
    return f'lưới đủ | {len(ds)} ca A/D: v2e trùng v2d (tỷ lệ, sự cố, khoảng cháy); luoi_khuyet = None.'


def ca_luoi_khuyet():
    du = range(0, 300, 10)
    khuyet = [t for t in du if not 30 <= t <= 110]
    dong = []
    for ten, f, bd in [('D2', khoang((120, 240)), 180), ('D3', khoang((120, 150)), 120), ('D4', khoang((130, 240)), 180)]:
        kq = chay(moi, khuyet, f, bd)
        so((chua(kq), kq['luoi_khuyet']['so_buoc_khuyet_he_thong'], kq['luoi_khuyet']['so_doan']), (True, 9, 1))
        dong.append(ten)
    kq = chay(moi, [t for t in du if t != 130], khoang((140, 240)), 120)  # D6: v2d chốt 1; v2e: lưới khuyết
    so((chua(kq), kq['luoi_khuyet']['so_buoc_khuyet_he_thong']), (True, 1))
    dai = range(0, 600, 10)
    kq = chay(moi, [t for t in dai if not 320 <= t < 400], khoang((0, 90), (400, 500)), 0)  # D7
    so((chua(kq), kq['luoi_khuyet']['so_buoc_khuyet_he_thong']), (True, 8))
    # CX-40 CHẶN 1a: 15 bước khuyết 10–150, 160 sai, 170–260 đúng, đầu chấm 180 (v2d chốt 1; thật có thể 0).
    luoi = [t for t in range(0, 360, 10) if not 10 <= t <= 150]
    kq = chay(moi, luoi, khoang((170, 270)), 180)
    so((chua(kq), kq['luoi_khuyet']['so_buoc_khuyet_he_thong'], kq['luoi_khuyet']['so_doan']), (True, 15, 1))
    so(chay(v2d, luoi, khoang((170, 270)), 180)['ty_le_khoe_x1']['su_co'], 1)  # tái hiện lỗi v2d
    # CX-40 CHẶN 1b: cùng lỗ, đầu chấm 0, mọi bước quan sát sai (v2d trả [0]; thật có thể 1).
    kq = chay(moi, luoi, khoang(), 0)
    so(chua(kq), True)
    so(chay(v2d, luoi, khoang(), 0)['ty_le_khoe_x1']['tu_so_kha_di'], [0])  # tái hiện lỗi v2d
    # CX-40 CHẶN 2: ba phút [0,180) khỏe, đầu chấm 0; đúng 20–50, khuyết 60–110, sai từ 120.
    luoi = [t for t in range(0, 180, 10) if not 60 <= t <= 110]
    kq = chay(moi, luoi, khoang((20, 60)), 0, ph_max=180)
    lk = kq['luoi_khuyet']
    so((chua(kq), lk['phut_khoe_phan_loai'], lk['so_phut_khoe_bi_anh_huong'], lk['phut_khoe_ngoai_luoi']), (True, 3, 1, 1))
    so(chay(v2d, luoi, khoang((20, 60)), 0, ph_max=180)['ty_le_khoe_x1']['phut_khoe_x1'], 2)  # tái hiện lỗi v2d
    # Phút khỏe ngoài lưới (lưới chỉ phủ phút đầu) cũng là khuyết.
    kq = chay(moi, range(0, 60, 10), khoang(), 0, ph_max=180)
    so((chua(kq), kq['luoi_khuyet']['phut_khoe_ngoai_luoi']), (True, 2))
    return ('lưới khuyết | D2, D3, D4, D6, D7, CX-40 CHẶN 1a/1b, CHẶN 2, phút khỏe ngoài lưới: chưa phân xử, '
            'tu_so_kha_di = None, đếm riêng đúng; tái hiện được lỗi của v2d ở 1a (chốt 1), 1b ([0]), 2 (mẫu số 2).')


def tai_lieu(luoi, f, loi=None):
    luoi = list(luoi)
    return {'cua_so': [luoi[0], luoi[-1]], 'step_s': 10,
            'loi_khuc': [{'ten': 'tin-hieu/gia', 'start': a, 'end': b} for a, b in (loi or [])],
            'chuoi': {'tin-hieu/gia': [{'metric': {}, 'values': [[t, str(int(f(t)))] for t in luoi
                                                                  if not any(a <= t <= b for a, b in (loi or []))]}]}}


def ca_file_chong():
    luoi, f = range(0, 180, 10), khoang((20, 90))
    ph = {'khoang': [[0, 180, moi.KHOE]]}
    A, B = tai_lieu(luoi, f), tai_lieu(luoi, f, [(80, 80)])
    for thu_tu in ([A, B], [B, A]):
        du = moi.Du()
        for d in thu_tu:
            du.them(d)
        kq = moi.cham({'luat': [LUAT]}, du, {}, moi.Phut(ph), 0)
        so((kq['luoi_khuyet'], kq['ty_le_khoe_x1']['su_co'], kq['ty_le_khoe_x1']['phut_khoe_x1'],
            [(c['t_hat'], c['t_het']) for c in kq['khoang_chay']]), (None, 1, 3, [(80, 90)]))
    du = moi.Du(); du.them(B)  # chỉ B: bước 80 thật sự khuyết
    so(chua(moi.cham({'luat': [LUAT]}, du, {}, moi.Phut(ph), 0)), True)
    du = v2d.Du(); du.them(A); du.them(B)  # tái hiện lỗi v2d
    so(v2d.cham({'luat': [LUAT]}, du, {}, v2d.Phut(ph), 0)['ty_le_khoe_x1']['tu_so_kha_di'], [0, 1])
    return 'CX-40b | hai file chồng, B lỗi ở 80: v2e lấy mẫu hợp lệ của A, 1/3, khoảng [80,90), hai thứ tự như nhau; chỉ B → chưa phân xử.'


def ca_co_pending():
    kq = chay(moi, [t for t in range(0, 180, 10) if t != 90], khoang((20, 100)), 0)  # Pending 20, Alerting 80, lỗ 90, sai từ 100
    sc, = kq['su_co']
    so((sc['t_hat'], 'pending-sau-lo-luoi' in sc['co']), (80, False))
    kq = chay(moi, [t for t in range(0, 180, 10) if t != 20], khoang((30, 180)), 0)  # lỗ 20 liền trước Pending 30
    so('pending-sau-lo-luoi' in kq['su_co'][0]['co'], True)
    kq = chay(moi, [t for t in range(0, 180, 10) if t != 10], khoang((30, 180)), 0)  # lỗ 10, bước 20 thấy sai, Pending 30
    so('pending-sau-lo-luoi' in kq['su_co'][0]['co'], False)
    return ("cờ | 'pending-sau-lo-luoi': không gắn khi lỗ sau Pending (20 → lỗ 90); gắn khi lỗ liền trước Pending "
            "(lỗ 20 → 30); không gắn khi một bước sai đã thấy ngăn lỗ với Pending (lỗ 10, sai 20, Pending 30).")


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
    return ['Bộ gốc thu_ca_gia.py đạt 9/9; chạy lại trên v2e:'] + dong_moi + [
        f'ĐẠT | len(khoang_chay) hai ca cửa sổ và sáu ca giao = {so_khoang}.', 'ĐẠT | tu_kiem() của v2e trả [].']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ghi', action='store_true')
    a = ap.parse_args()
    ma = [CODE, moi.CODE, v2d.CODE, CODE.parent / 'tao_v2e.py', cu.CODE, cu.gt.CODE, cu.cham.CODE]
    dong = [f'SHA-256 {p.name} {moi.sha(p)}' for p in ma]
    dong += ['ĐẠT | ' + f() for f in (ca_luoi_du, ca_luoi_khuyet, ca_file_chong, ca_co_pending)] + hoi_quy()
    vb = ('\n'.join(dong) + '\n').encode('utf-8')
    if a.ghi:
        with (moi.RA / 'thu-ca-gia-v2e.txt').open('xb') as f:
            f.write(vb)
    sys.stdout.buffer.write(vb)


if __name__ == '__main__':
    if sys.argv[1:2] == ['--cli-thieu-ticket']:
        del sys.argv[1]
        with patch.object(cu, 'cham', moi):
            sys.exit(cu.cli_thieu_ticket())
    main()
