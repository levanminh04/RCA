# -*- coding: utf-8 -*-
"""Ca giả W4 v2c. Chạy với -B. Thêm --ghi để tạo biên bản UTF-8."""
import argparse
import subprocess
import sys
from contextlib import redirect_stdout
from io import BytesIO, TextIOWrapper
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
import cham_offline_v2_claude as truoc
import cham_offline_v2c as sau
import thu_ca_gia as cu

CODE = Path(__file__).resolve()
so = cu.doi_chieu


def chuoi(bo, luoi, dau_dung, het_dung, bat_dau, loai='he-thong', khoang_truoc=None):
    luat = {'uid': 'gia', 'loai': loai, 'for_s': 60, 'no_data_state': 'OK',
            'dieu_kien': {'phep': '>', 'nguong': 0}}
    du = bo.Du()
    du.luoi = set(luoi)
    cac_khoang = [(dau_dung, het_dung)]
    if khoang_truoc:
        cac_khoang.append(khoang_truoc)
    du.chuoi['tin-hieu/gia'] = {'': {t: int(any(a <= t < b for a, b in cac_khoang)) for t in du.luoi}}
    phut = bo.Phut({'khoang': [[0, max(luoi) + 10, bo.KHOE]]})
    return bo.cham({'luat': [luat]}, du, {}, phut, bat_dau)


def thu_phut_dau():
    for bo, tu_so, ty_le in [(truoc, 1, 360), (sau, 0, 0)]:
        kq = chuoi(bo, range(0, 180, 10), 20, 100, 70)
        sc, = kq['su_co']
        so((sc['t_hat'], sc['t_het'], sc['lop']), (80, 100, bo.KHOE))
        so(len(kq['khoang_chay']), 1)
        ty = kq['ty_le_khoe_x1']
        so((ty['su_co'], ty['phut_khoe_x1'], ty['moi_6_gio']), (tu_so, 1, ty_le))
        if bo is sau:
            so('phut-dau-ngoai-mau-so' in sc['co'], True)
    # Đầu phút đủ điều kiện vẫn tính, kể cả khi Pending ở phút bị loại.
    kq = chuoi(sau, range(0, 180, 10), 60, 140, 70)
    so((kq['su_co'][0]['t_hat'], kq['ty_le_khoe_x1']['su_co']), (120, 1))
    return 'A | đầu chấm 70 s, Alerting 80 s, hết 100 s. Trước 1/1 phút, sau 0/1 phút. ' \
           'Vẫn liệt kê lớp khoe-x1. Đối chứng Alerting 120 s được tính 1/1.'


def thu_lo_luoi():
    du = range(0, 300, 10)
    khuyet = [t for t in du if not 30 <= t <= 110]
    for dau, t_hat, n in [(30, 90, 0), (120, 180, 1)]:
        kq = chuoi(sau, du, dau, 240, 180)
        so((kq['su_co'][0]['t_hat'], kq['ty_le_khoe_x1']['su_co']), (t_hat, n))
    goc = chuoi(truoc, khuyet, 120, 240, 180)
    so((goc['su_co'][0]['t_hat'], goc['ty_le_khoe_x1']['su_co']), (180, 1))
    kq = chuoi(sau, khuyet, 120, 240, 180)
    sc, = kq['su_co']
    day, = kq['day_dung_sau_lo_luoi']
    so((day['tp'], day['t_hat_som'], sc['t_hat']), (120, 90, 180))
    so('pending-sau-lo-luoi' in sc['co'], True)
    ty = kq['ty_le_khoe_x1']
    so((ty['su_co'], ty['phut_khoe_x1'], ty['moi_6_gio'], ty['ci95_moi_6_gio'],
        ty['trang_thai']), (None, 2, None, None, 'chua-phan-xu'))

    # Một bước sai đã thấy sau lỗ xác định lại đầu Pending.
    kq = chuoi(sau, khuyet, 130, 240, 180)
    so((kq['day_dung_sau_lo_luoi'], kq['su_co'][0]['t_hat'], kq['ty_le_khoe_x1']['su_co']),
       ([], 190, 1))
    # Dãy đúng ngắn sau lỗ vẫn có thể đã Alerting trong cửa sổ chấm.
    ngan = chuoi(sau, khuyet, 120, 150, 120)
    so((len(ngan['khoang_chay']), ngan['ty_le_khoe_x1']['trang_thai']), (0, 'chua-phan-xu'))
    # Cảnh báo quan sát không góp vào tử số hệ thống.
    qs = chuoi(sau, khuyet, 120, 240, 180, 'quan-sat')
    so(qs['ty_le_khoe_x1']['su_co'], 0)
    # Lỗ một bước; cả hai mốc Alerting khả dĩ cùng thuộc phút khỏe đã tính.
    luoi = [t for t in du if t != 130]
    kq = chuoi(sau, luoi, 140, 240, 120)
    so('pending-sau-lo-luoi' in kq['su_co'][0]['co'], True)
    so(kq['ty_le_khoe_x1']['su_co'], 1)

    # Cùng lớp khỏe nhưng hai cách điền nằm hai bên biên gom 300 s.
    dai = range(0, 600, 10)
    for dau, n in [(320, 1), (400, 2)]:
        kq = chuoi(sau, dai, dau, 500, 0, khoang_truoc=(0, 90))
        so(kq['ty_le_khoe_x1']['su_co'], n)
    kq = chuoi(sau, [t for t in dai if not 320 <= t < 400], 400, 500, 0, khoang_truoc=(0, 90))
    so(kq['ty_le_khoe_x1']['trang_thai'], 'chua-phan-xu')
    return 'D | bỏ các bước 30–110 s, đầu chấm 180 s. Trước 1/2 phút. Sau: chưa phân xử, ' \
           'cần lịch sử Grafana. Hai chuỗi đủ cho 0/2 (Alerting 90 s) và 1/2 (Alerting 180 s).'


def hoi_quy():
    # Chạy nguyên bộ cũ, không truyền --ghi. Chạy lại đúng fixture đó với v2c.
    p = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(cu.CODE)],
                       capture_output=True, encoding='utf-8', check=True)
    dong_cu = [d for d in p.stdout.splitlines() if d.startswith('ĐẠT |')]
    so(len(dong_cu), 9)
    dong = ['Bộ gốc thu_ca_gia.py đạt 9/9. Hồi quy trên v2c:']
    cham_that = sau.cham
    so_khoang = []

    def cham_va_dem(*args, **kwargs):
        kq = cham_that(*args, **kwargs)
        so_khoang.append(len(kq['khoang_chay']))
        return kq

    # main() của bộ cũ giữ nguyên chín đầu vào và cả các kỳ vọng.
    # Chuyển riêng CLI ca thiếu Ticket sang tiến trình con chạy v2c.
    with (patch.object(cu, 'cham', sau), patch.object(cu.gt, 'cham', sau),
          patch.object(sau, 'cham', cham_va_dem), patch.object(cu, 'CODE', CODE),
          patch.object(sys, 'argv', [str(CODE)]), TextIOWrapper(BytesIO(), encoding='utf-8') as buf,
          redirect_stdout(buf)):
        cu.main()
        buf.flush()
        dong_moi = [d for d in buf.buffer.getvalue().decode().splitlines() if d.startswith('ĐẠT |')]
    so(dong_moi, dong_cu)
    so(so_khoang, [0, 1] + [2] * 6)
    so(sau.tu_kiem(sau.nap(sau.GOC / 'bieu-thuc.json')), [])
    return dong + dong_moi + [f'ĐẠT | len(khoang_chay) của hai ca cửa sổ và sáu ca giao = {so_khoang}.',
                              'ĐẠT | tu_kiem() của v2c trả [].']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ghi', action='store_true')
    args = ap.parse_args()
    ma = [CODE, sau.CODE, truoc.CODE, cu.CODE, cu.gt.CODE, cu.cham.CODE]
    dong = [f'SHA-256 {p.name} {sau.sha(p)}' for p in ma]
    dong.extend(['ĐẠT | ' + thu_phut_dau(), 'ĐẠT | ' + thu_lo_luoi(), *hoi_quy()])
    van_ban = ('\n'.join(dong) + '\n').encode('utf-8')
    if args.ghi:
        with (sau.RA / 'thu-ca-gia-v2c.txt').open('xb') as f:
            f.write(van_ban)
    sys.stdout.buffer.write(van_ban)


if __name__ == '__main__':
    if sys.argv[1:2] == ['--cli-thieu-ticket']:
        del sys.argv[1]
        with patch.object(cu, 'cham', sau):
            sys.exit(cu.cli_thieu_ticket())
    main()
