"""Phiên 9 T-043: nhãn ba thế giới của đơn vị đếm đại diện khi khe giữa hai file là OPEN (luật F phương án (a), Q-207).

Không nhãn. Chỉ đọc hai đầu ra pha 1 đã có, kiểm hash theo manifest trước khi dùng:
- v1.1 (`ks16/runs/pha1-002`): T^chắc đã loại khe giữa file;
- v1 (`ks16/runs/pha1-001`): F gộp khe, nên T^max của v1 là |F gồm khe ∩ phía|.
Theo (a): T^chắc = T^chắc của v1.1; T^max = T^max của v1.
  P = (T_N^chắc, T_A^chắc); S_lo = (T_N^max, T_A^chắc); S_hi = (T_N^chắc, T_A^max).
Trong mỗi lượt pha 1: T_N^chắc, T_A^chắc = worlds.P; T_N^max = worlds.S_lo[0]; T_A^max = worlds.S_hi[1].
Đơn vị đếm như `so_v1_v11.don_vi_dem`. Nhãn theo hướng: UP khi p lên < α, DOWN khi p giảm < α, còn lại NORMAL;
tổng sự kiện < 10 hoặc T ≤ 0 thì không xét. Không phải điểm M1.
Chạy: python -B results/T-043/scripts/the_gioi_khe_open.py --out results/T-043/runs/khe-open-002
Lượt `runs/khe-open-001` hỏng (giữ lại): bản đầu của script ghép thừa tiền tố đường dẫn khi đối chiếu manifest,
nên dừng ở bước kiểm hash, không ghi kết quả.
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from scipy.stats import binom

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import so_v1_v11 as S  # noqa: E402

ALPHA = 0.01
M_COUNT = 10
V1 = 'results/T-043/ks16/runs/pha1-001/dem-khong-nhan.json'
V11 = 'results/T-043/ks16/runs/pha1-002/dem-khong-nhan.json'


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def kiem_hash():
    man = json.loads((ROOT / 'results/T-043/manifest.json').read_text(encoding='utf-8'))
    ky_vong = {o['path']: o['sha256'] for o in man['outputs']}
    out = {}
    for rel in (V1, V11):
        thuc = sha(rel)
        if ky_vong.get(rel) != thuc:
            raise SystemExit(f'lệch hash: {rel}')
        out[rel] = thuc
    return out


def nhan(nN, nA, TN, TA):
    if nN + nA < M_COUNT or TN <= 0 or TA <= 0:
        return None
    p0 = TA / (TN + TA)
    n = nN + nA
    p_len = float(binom.sf(nA - 1, n, p0))
    p_giam = float(binom.cdf(nA, n, p0))
    return 'UP' if p_len < ALPHA else ('DOWN' if p_giam < ALPHA else 'NORMAL')


def the_gioi(w1, w11):
    """Trả (có sẵn ở v1.1, theo (a)); mỗi phần là dict P, S_lo, S_hi -> (T_N, T_A)."""
    Nc, Ac = w11['P']
    co_san = {'P': (Nc, Ac), 'S_lo': tuple(w11['S_lo']), 'S_hi': tuple(w11['S_hi'])}
    Nmax, Amax = w1['S_lo'][0], w1['S_hi'][1]
    theo_a = {'P': (Nc, Ac), 'S_lo': (Nmax, Ac), 'S_hi': (Nc, Amax)}
    return co_san, theo_a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=False)
    t0 = time.time()
    hashes = kiem_hash()
    a = {c['opaque_id']: c for c in json.loads((ROOT / V1).read_text(encoding='utf-8'))['cases']}
    b = json.loads((ROOT / V11).read_text(encoding='utf-8'))['cases']
    tong, don_vi = {}, []
    for i, cb in enumerate(b):
        ca = a[cb['opaque_id']]
        ds = cb['dataset']
        for src, loai, khoa, nN, nA in S.don_vi_dem(cb):
            co_san, theo_a = the_gioi(ca['quan_sat'][src]['worlds'], cb['quan_sat'][src]['worlds'])
            n_cs = {k: nhan(nN, nA, *v) for k, v in co_san.items()}
            n_a = {k: nhan(nN, nA, *v) for k, v in theo_a.items()}
            t = tong.setdefault(ds, {'don_vi_xet': 0, 'phu_thuoc_co_san': 0, 'phu_thuoc_theo_a': 0,
                                     'phat_sinh_them': 0})
            if n_a['P'] is None:
                continue
            t['don_vi_xet'] += 1
            dep_cs = len(set(n_cs.values())) > 1
            dep_a = len(set(n_a.values())) > 1
            t['phu_thuoc_co_san'] += dep_cs
            t['phu_thuoc_theo_a'] += dep_a
            t['phat_sinh_them'] += dep_a and not dep_cs
            if dep_cs or dep_a:
                don_vi.append({'dataset': ds, 'case_index': i, 'opaque_id': cb['opaque_id'], 'nguon': src,
                               'loai': loai, 'khoa': khoa, 'n_N': nN, 'n_A': nA,
                               'nhan_co_san': n_cs, 'nhan_theo_a': n_a,
                               'T_co_san': co_san, 'T_theo_a': theo_a})
    out = {
        'schema': 'T043-the-gioi-khe-open-v1',
        'labels_read': False,
        'luat': 'Q-207, luật F phương án (a): khe dương giữa hai file là OPEN',
        'hash_dau_vao': hashes,
        'alpha': ALPHA,
        'tong_su_kien_toi_thieu': M_COUNT,
        'tong_hop': tong,
        'don_vi_phu_thuoc': don_vi,
        'pham_vi': 'đơn vị đếm đại diện của KS-16 (tần suất thao tác, số dòng log và log lỗi theo thực thể); không phải điểm M1',
        'giay': round(time.time() - t0, 1),
    }
    (out_dir / 'ket-qua.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'tong_hop': tong, 'giay': out['giay']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
