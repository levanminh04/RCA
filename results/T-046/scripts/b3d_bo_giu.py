"""T-046 chẩn đoán C1 bổ sung (chỉ báo cáo, không là ứng viên, không vào luật chọn; thêm 14:12 sau khi thấy tỷ lệ
giữ giá trị ở `cau-truc-metric-re2.json`): tách phần qua giả ở A/A do chuỗi metric RE2-TT "lấy mẫu rồi giữ" khỏi phần
do trôi. Không đọc nhãn.

Với mỗi phép metric hợp lệ của A/A R0 RE2-TT (danh sách phép, hướng lấy từ bảng `runs/b3-aa-001`), dựng lại mẫu N″, A″
từ hàng metric đã cắt theo A1, rồi bỏ giá trị giữ: trong chuỗi theo thời gian của mỗi phía, chỉ giữ giây có giá trị
khác giây có giá trị liền trước (giây đầu mỗi phía luôn giữ). Tính p theo G0 (`e4.p_cong`) và G3 (`cong`, b đo trên
chuỗi 1 giây của mẫu đã bỏ giữ) trên mẫu đã bỏ giữ. Báo tỷ lệ p < α theo hậu tố kênh và hướng, kèm số mẫu còn lại.

Chạy: $PY -B results/T-046/scripts/b3d_bo_giu.py --b3 results/T-046/runs/b3-aa-001 --ra results/T-046/bo-giu-metric-re2.json
"""
import argparse
import json
import statistics
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import cong
import t046
from t046 import wilson
from b3_chay import tat_ha_toc

ALPHA = 0.01
TS = {'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05, 'n_exact_max': 100}
NS = t046.NS


def bo_giu(vals, moc):
    out_v, out_m = [], []
    for v, m in zip(vals, moc):
        if out_v and v == out_v[-1]:
            continue
        out_v.append(v)
        out_m.append(m)
    return out_v, out_m


def mot_ca(oid, phep):
    tat_ha_toc()
    mt = t046.moi_truong()
    ca, t2, meta = t046.nap('RE2-TT', oid, 'aa', mt)
    p = t046.runner._params(t046.cau_hinh('R0'), ca)
    t_ns = int(round(t2 * NS))
    mm = t046._moc_metric(ca, p, t_ns)
    out = []
    for ma, ds_h in phep.items():
        N, mN, A, mA, cot = mm[ma]
        N2, mN2 = bo_giu([float(x) for x in N], mN)
        A2, mA2 = bo_giu([float(x) for x in A], mA)
        hau_to = cot.split('_', 1)[1]
        for d in ds_h:
            p0 = cong.p_G0(N2, A2, d, TS)[0] if len(N2) >= 5 and len(A2) >= 5 else None
            kb = cong.chuan_bi_khoi(N2, mN2, A2, mA2, t_ns) if len(N2) >= 5 and len(A2) >= 5 else None
            p3 = None
            if kb is not None:
                p3 = cong.p_theo_cong('G3', N2, mN2, A2, mA2, t_ns, d, TS, ma + '|bo_giu', kb=kb)['p']
            out.append({'hau_to': hau_to, 'd': d, 'n_N': len(N2), 'n_A': len(A2), 'p_G0': p0, 'p_G3': p3,
                        'roi_G0': kb.get('roi_G0') if kb else 'it_mau'})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--b3', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ca = t046.nap_luot(a.b3)
    viec = {}
    for oid, x in ca.items():
        if x['dataset'] != 'RE2-TT':
            continue
        b = x['cua_so']['aa|R0']['bang']
        viec[oid] = {u['ma']: list(u['huong']) for u in b['pv'] if u['nhom'] == 'metric' and u['hop_le'] and u['trong_U']}
    with ProcessPoolExecutor(max_workers=4) as ex:
        kq = [r for ds in ex.map(mot_ca, list(viec), list(viec.values())) for r in ds]
    nhom = {}
    for r in kq:
        nhom.setdefault(f"{r['hau_to']}|{r['d']}", []).append(r)
    nhom['_tat_ca'] = kq
    out = {}
    for k, v in sorted(nhom.items()):
        o = {'n': len(v), 'n_N_trung_vi': statistics.median(r['n_N'] for r in v)}
        for g in ('G0', 'G3'):
            vv = [r for r in v if r[f'p_{g}'] is not None]
            kk = sum(1 for r in vv if r[f'p_{g}'] < ALPHA)
            o[g] = {'k': kk, 'n': len(vv), 'ty_le': round(kk / len(vv), 4) if vv else None, 'wilson95': wilson(kk, len(vv))}
        out[k] = o
    Path(a.ra).write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    for k, o in out.items():
        print(k, o['n'], 'nN', o['n_N_trung_vi'], 'G0', o['G0']['ty_le'], 'G3', o['G3']['ty_le'])


if __name__ == '__main__':
    main()
