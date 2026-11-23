# -*- coding: utf-8 -*-
"""Ca giả W4 v2. Dùng --ghi để lưu biên bản vào ra/thu-ca-gia.txt."""
import argparse
import pathlib
import subprocess
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
import e4_giai_thich_khac_v2 as gt

cham = gt.cham
CODE = pathlib.Path(__file__).resolve()


def doi_chieu(thuc, mong):
    if thuc != mong:
        raise AssertionError(f'nhận {thuc!r}, cần {mong!r}')


def thu_cua_so(mau, mong, chay):
    # Luật giả for=20 s: một cửa sổ có ba mẫu ở bước 10 s.
    luat = {'uid': 'do', 'loai': 'quan-sat', 'for_s': 20, 'no_data_state': 'Alerting',
            'dieu_kien': {'phep': '<', 'nguong': 8}}
    bt = {'luat': [luat], 'tham_so_co_dinh': {'routes': []}}
    du = cham.Du()
    du.luoi = set(range(0, len(mau) * 10, 10))
    du.chuoi['tin-hieu/do'] = {'': dict(zip(sorted(du.luoi), mau))}
    ph = cham.Phut({'khoang': [[0, 60, cham.KHOE]]})
    kq = gt.giai_thich(bt, du, {}, ph)
    rr = kq['luat']['do']['theo_lop'][cham.KHOE]['(mot-chuoi)']
    doi_chieu(rr['min_duy_tri_for'], mong)
    doi_chieu(bool(cham.cham(bt, du, {}, ph)['khoang_chay']), chay)
    return f'{",".join(map(str, mau))} → min giữa các max = {mong}, số khoảng cháy = {int(chay)}'


def thu_giao(he, qs, mong):
    du = cham.Du()
    du.luoi = set(range(0, 101, 10))
    bt = {'luat': []}
    for loai, (dau, cuoi) in [('he-thong', he), ('quan-sat', qs)]:
        bt['luat'].append({'uid': loai, 'loai': loai, 'for_s': 0, 'no_data_state': 'OK',
                           'dieu_kien': {'phep': '>', 'nguong': 0}})
        du.chuoi['tin-hieu/' + loai] = {'': {t: 1 for t in du.luoi if dau <= t and (cuoi is None or t < cuoi)}}
    su_co = cham.cham(bt, du, {}, cham.Phut(None))['su_co']
    doi_chieu(len(su_co), 2)
    for s in su_co:
        he_thong = s['loai'] == 'he-thong'
        doi_chieu((s['t_hat'], s['t_het']), he if he_thong else qs)
        doi_chieu('chong-quan-sat' in s['co'], he_thong and mong)

    def khoang(cap):
        a, b = cap
        return f"[{a},{'∞' if b is None else b})"

    return f'hệ thống {khoang(he)}, quan sát {khoang(qs)} → cờ hệ thống = {"có" if mong else "không"}'


def cli_thieu_ticket():
    # Cấp dữ liệu tổng hợp trong bộ nhớ cho main(); giữ bộ phân tích lệnh,
    # cấu hình ghim, phép chọn ngưỡng, stderr và mã thoát của CLI v2.
    bt = cham.nap(cham.GOC / 'bieu-thuc.json')
    du = cham.Du()
    du.luoi = set(range(0, 1800, 10))
    for r in bt['tham_so_co_dinh']['routes']:
        if r != 'ticket':
            du.chuoi[f'tin-hieu/t072-p95-{r}'] = {r: dict.fromkeys(du.luoi, 0.05)}
        du.chuoi[f'phu/ty-le-loi-chua-chan-5xx-{r}'] = {r: dict.fromkeys(du.luoi, 0.0)}
    ph = cham.Phut({'khoang': [[0, 1800, cham.KHOE]]})
    with patch.object(cham, 'Du', return_value=du), patch.object(cham, 'Phut', return_value=ph):
        return cham.main()


def thu_route():
    cmd = [sys.executable, '-X', 'utf8', '-B', str(CODE), '--cli-thieu-ticket', 'chon-nguong']
    p = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    doi_chieu(p.returncode, 1)
    doi_chieu(p.stderr.strip(), 'Không đủ dữ liệu E2 cho route: ticket (p95, 0 bước)')
    return f'thiếu riêng p95 Ticket → mã thoát {p.returncode}; stderr = {p.stderr.strip()}'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ghi', action='store_true')
    a = ap.parse_args()
    dong = [thu_cua_so([8, 7, 8], 8, False), thu_cua_so([8, 7, 7, 7], 7, True)]
    for he, qs, mong in [
            ((10, 70), (40, 90), True), ((40, 90), (10, 70), True),
            ((10, 30), (40, 70), False), ((10, 40), (40, 70), False),
            ((40, None), (10, 50), True), ((10, 40), (40, None), False)]:
        dong.append(thu_giao(he, qs, mong))
    dong.append(thu_route())
    ket_qua = [f'ĐẠT | {d}' for d in dong]
    ket_qua += [f'SHA-256 {p.name} {cham.sha(p)}' for p in (cham.CODE, gt.CODE, CODE)]
    van_ban = '\n'.join(ket_qua) + '\n'
    if a.ghi:
        cham.RA.mkdir(exist_ok=True)
        (cham.RA / 'thu-ca-gia.txt').write_bytes(van_ban.encode('utf-8'))
    sys.stdout.buffer.write(van_ban.encode('utf-8'))


if __name__ == '__main__':
    if sys.argv[1:2] == ['--cli-thieu-ticket']:
        del sys.argv[1]
        sys.exit(cli_thieu_ticket())
    main()
