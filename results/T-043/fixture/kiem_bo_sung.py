"""Phiên 9 T-043: kiểm đáp án của fixture bổ sung (`fixture/fixture-bo-sung.json`) bằng cài đặt tham chiếu nhỏ.

Phủ ba luật của Q-207 (`dinh-chinh-phien9.md`): khe giữa file là OPEN (Đ9), phủ quyết E9 và thứ tự C-d2 (Đ11),
đích C-d3 khi không có span gốc (Đ12). Phiên 10 (`dinh-chinh-phien10.md` Đ20): hợp khoảng trước khi tìm khe; lượt 001 chạy bản cũ.
Không đọc dataset, không nhãn. Đây là kiểm đáp án của đặc tả, không là kiểm cài đặt M1.
Chạy: python -B results/T-043/fixture/kiem_bo_sung.py --out results/T-043/fixture/runs/kiem-bo-sung-002.json
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / 'results/T-043/fixture/fixture-bo-sung.json'
NGUONG_S = 2 * 10 + 0.001


def do_dai(ds):
    return sum(max(0.0, b - a) for a, b in ds)


def giao(ds, k):
    out = []
    for a, b in ds:
        lo, hi = max(a, k[0]), min(b, k[1])
        if hi > lo:
            out.append((lo, hi))
    return out


def tru(ds, bo):
    out = list(ds)
    for c, d in bo:
        moi = []
        for a, b in out:
            if d <= a or c >= b:
                moi.append((a, b))
                continue
            if c > a:
                moi.append((a, c))
            if d < b:
                moi.append((d, b))
        out = moi
    return out


def quan_sat_khe(v):
    r = v['r_s']
    kf = sorted((min(f), max(f) + r) for f in v['file'])
    # Phiên 10 (Đ20): hợp các khoảng trước khi tìm khe; file lồng nhau không tạo khe.
    hop = [list(kf[0])]
    for a, b in kf[1:]:
        if a > hop[-1][1]:
            hop.append([a, b])
        else:
            hop[-1][1] = max(hop[-1][1], b)
    khe = [(x[1], y[0]) for x, y in zip(hop, hop[1:])]
    bao = [(hop[0][0], hop[-1][1])]
    w = tuple(v['cua_so'])
    trong = [x for f in v['file'] for x in f if w[0] <= x < w[1]]
    H = [(min(trong), max(trong) + r)]
    T_chac, T_max = {}, {}
    for p, k in v['phia'].items():
        T_chac[p] = do_dai(tru(giao(giao(bao, k), H[0]), khe))
        T_max[p] = do_dai(giao(bao, k))
    return {
        'khe': [list(x) for x in khe],
        'T_chac': T_chac,
        'T_max': T_max,
        'thieu_thu_s': do_dai(tru([w], bao)),
        'the_gioi': {'P': [T_chac['N'], T_chac['A']], 'S_lo': [T_max['N'], T_chac['A']],
                     'S_hi': [T_chac['N'], T_max['A']]},
    }


def e9(v):
    e = v['e']['khoi_phat']
    ks = [b['khoi_phat'] for b in v['B']]
    if e is None or any(k is None for k in ks):
        return {'phu_quyet': False, 'ly_do': 'không đủ khởi phát'}
    if all(k - e > NGUONG_S for k in ks):
        return {'phu_quyet': True, 'ly_do': 'đã xét, phủ quyết'}
    return {'phu_quyet': False, 'ly_do': 'đã xét, không phủ quyết'}


def cd2(v):
    tt = sorted(v['thuc_the'], key=lambda x: (x['khoi_phat'] is None, x['khoi_phat'] or 0, -x['K_raw']))
    return {'thu_tu': [x['ten'] for x in tt]}


def cd3(v):
    goc = [s['chu'] for s in v['spans_A'] if s['parent'] in ('', None)]
    dich = sorted({c for c in goc if c in v['bat_thuong_lan_nguoc']})
    if not dich:
        return {'dich': [], 'trang_thai': 'NO_TARGET', 'RR': 0}
    return {'dich': dich, 'trang_thai': 'OK', 'RR': None}


CACH = {'quan_sat_khe': quan_sat_khe, 'E9': e9, 'Cd2': cd2, 'Cd3': cd3}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out = ROOT / args.out
    if out.exists():
        raise SystemExit(f'đã có {out}; không ghi đè')
    fx = json.loads(FIXTURE.read_text(encoding='utf-8'))['fixtures']
    rows = []
    for f in fx:
        tinh = CACH[f['loai']](f['dau_vao'])
        rows.append({'id': f['id'], 'loai': f['loai'], 'dap_an': f['dap_an'], 'tinh': tinh, 'khop': tinh == f['dap_an']})
    tong = {'so_muc': len(rows), 'khop': sum(r['khop'] for r in rows)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'schema': 'T043-kiem-fixture-bo-sung-v1', 'tong': tong, 'muc': rows},
                              ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(tong, ensure_ascii=False))
    for r in rows:
        if not r['khop']:
            print('LECH', r['id'], json.dumps(r['tinh'], ensure_ascii=False))


if __name__ == '__main__':
    main()
