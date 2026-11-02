"""T-046 bước 3, bổ sung (chỉ báo cáo; thêm 13:30 sau khi xem chan-doan-cong.json): tách tỷ lệ qua cổng ở A/A của
metric RE2-TT theo loại kênh (hậu tố tên cột sau dấu '_' đầu, như hồ sơ nguồn) và hướng, cho G0, G1, G3; kèm số đơn vị
có N″ hằng (rơi G0 vì phương sai 0). Không đọc nhãn; không xem cửa sổ thật.

Chạy: $PY -B results/T-046/scripts/b3_bo_sung.py --luot results/T-046/runs/b3-aa-001 --ra results/T-046/chan-doan-cong-bo-sung.json
"""
import argparse
import json
from pathlib import Path

import t046
from t046 import wilson

ALPHA = 0.01


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ca = t046.nap_luot(a.luot)
    nhom = {}
    for x in ca.values():
        if x['dataset'] != 'RE2-TT':
            continue
        for u in x['cua_so']['aa|R0']['bang']['pv']:
            if not (u['hop_le'] and u['trong_U']) or u['nhom'] != 'metric':
                continue
            hau_to = u['ma'].split('|', 1)[1].split('_', 1)[1]
            kh = u.get('khoi') or {}
            for d, h in u['huong'].items():
                k = f'{hau_to}|{d}'
                o = nhom.setdefault(k, {'n': 0, 'roi_G0': 0, 'hang': 0, **{g: 0 for g in t046.CONG}})
                o['n'] += 1
                o['roi_G0'] += int(bool(kh.get('roi_G0')))
                o['hang'] += int(kh.get('roi_G0') == 'phuong_sai_0')
                for g in t046.CONG:
                    o[g] += int(h[f'p_{g}'] < ALPHA)
    out = {}
    for k, o in sorted(nhom.items(), key=lambda z: -z[1]['n']):
        out[k] = dict(o, **{f'ty_le_{g}': round(o[g] / o['n'], 4) for g in t046.CONG},
                      wilson95_G3=wilson(o['G3'], o['n']))
    Path(a.ra).write_bytes((json.dumps({'luot': a.luot, 'theo_hau_to_huong': out}, ensure_ascii=False, indent=1)
                            + '\n').encode('utf-8'))
    for k, o in list(out.items())[:40]:
        print(k, o['n'], 'G0', o['ty_le_G0'], 'G1', o['ty_le_G1'], 'G3', o['ty_le_G3'], 'roi', o['roi_G0'], 'hang', o['hang'])


if __name__ == '__main__':
    main()
