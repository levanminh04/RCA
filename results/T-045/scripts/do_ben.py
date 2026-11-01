"""T-045 bước 7 — phép độ bền (chỉ báo cáo; SPEC T-045 bước 7). Không chạy lại phương pháp; dùng kết quả chấm pha 2 của
khối K (`pha2_khoi_k.py` lưu `<ra>/kq.json`, `kq_mg.json`).

- Đơn vị lấy mẫu: ô (`dinh-nghia-pha2.json#/rr_theo_o`); lấy có hoàn lại trong từng dataset, giữ số ô của mỗi
  dataset (`rr.lay_mau_o`). Ô lấy k lần thì mọi ca của ô có bội số k; ca không được lấy có bội số 0.
- Một mẫu ô dùng chung cho mọi cấu hình và ba thế giới. Mọi đầu vào của luật chọn tính theo bội số: RR theo ca và ô,
  P/M/P′/M′, cờ M5, UV-6 (trong `pha2.ket_cuc_cap`), mốc giả RE2-TT (`pha2.dem_moc_gia`, mẫu số tính lại), MRR
  (`pha2.mrr_cau_hinh`). Giữ cố định từ T0: E_X, |E_X| (thành phần ít ca), δ = 0,01, δ_d = 1/30, 1/22, ngưỡng mốc giả.
- Chọn ở P (bước 1–8), cùng S_lo, S_hi (bước 10). Mẫu dừng (bước 7 không còn cấu hình; bước 8 cấu hình thắng không có
  E1, E2, E5) đếm thành loại riêng, không gán cấu hình.
- Báo: tần suất mỗi cấu hình thắng; tần suất từng thành phần được bật; tần suất từng loại không chọn được; tần suất cờ
  TRÁI CHIỀU và "phụ thuộc quan sát" ở cấu hình thắng.
Chạy: $PY -B results/T-045/scripts/do_ben.py --kq results/T-045/khoi-k --seed <seed> --n 1000 --ra results/T-045/do-ben.json
"""
import argparse
import collections
import itertools
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m1_danh_gia import chon_khoi, luat_c, pha2, rr  # noqa: E402
import pha2_khoi_k as pk  # noqa: E402


def cac_cap():
    out = []
    for name in [chon_khoi.ten(set(c), pk.TP) for r in range(5) for c in itertools.combinations(pk.TP, r)]:
        s = chon_khoi.tap(name)
        if name != 'R0' and len(s) > 1:
            out.append(('R0', name, luat_c.NHIEU_THANH_PHAN, sorted(s)))
        for x in sorted(s):
            out.append((chon_khoi.ten(s - {x}, pk.TP), name, x, [x]))
    seen, uniq = set(), []
    for c in out:
        if f'{c[0]}|{c[1]}' not in seen:
            seen.add(f'{c[0]}|{c[1]}')
            uniq.append(c)
    return uniq


def mot_mau(kq, kq_mg, E_X, cap_ds, ts):
    ts_mg = {o: ts[o] for o in next(iter(kq_mg['cau_hinh'].values()))['ca']}
    cap = {}
    for at, bt, tp, comps in cap_ds:
        ex = sorted(set().union(*(E_X[x] for x in comps)))
        mg = pha2.dem_moc_gia(kq_mg, 'K-' + at, 'K-' + bt, trong_so=ts_mg)
        v = pha2.ket_cuc_cap(kq, 'K-' + at, 'K-' + bt, ex, tp, 'khoi_K', moc_gia=mg[:2], trong_so=ts,
                             delta_d_co_dinh=pk.DD)
        cap[f'{at}|{bt}'] = v['ket_hop']
    MRR = {w: {c[2:]: m['gop'] for c, m in pha2.mrr_cau_hinh(kq, ts, w).items()} for w in pk.WORLDS}
    ch = {'P': chon_khoi.chon(pk.TP, pk.IT_CA, pk.DO_THI, MRR['P'], cap)}
    for w in ('S_lo', 'S_hi'):
        ch[w] = chon_khoi.chon(pk.TP, pk.IT_CA, pk.DO_THI, MRR[w], cap, the_gioi=w)
    t = ch['P']['chon']
    if t is None:
        return {'loai': 'buoc7_khong_con_cau_hinh'}
    if 'khong_co_thanh_phan_do_thi' in ch['P']['ly_do_trinh_Minh']:
        return {'loai': 'buoc8_khong_E1_E2_E5'}
    b8 = chon_khoi.kiem_cau_hinh_thang(t, pk.TP, cap, pk.IT_CA)
    return {'loai': 'chon', 'thang': t, 'trai_chieu': 'trai_chieu_dataset' in ch['P']['ly_do_trinh_Minh'],
            'phu_thuoc_quan_sat': bool(b8['phu_thuoc_quan_sat']) or any(ch[w]['chon'] != t for w in ('S_lo', 'S_hi')),
            'xung_dot_buoc8': bool(b8['xung_dot'])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kq', required=True, help='thư mục kq.json, kq_mg.json của pha2_khoi_k')
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--n', type=int, default=1000)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    t0 = time.time()
    kq = pha2.giai_ma_json(json.loads((Path(a.kq) / 'kq.json').read_text(encoding='utf-8')))
    kq_mg = pha2.giai_ma_json(json.loads((Path(a.kq) / 'kq_mg.json').read_text(encoding='utf-8')))
    E_X = pk.nap_E_X(False)
    ca0 = next(iter(kq['cau_hinh'].values()))['ca']
    ds = [{'ma': o, 'dataset': c['dataset'], 'o': c['o']} for o, c in sorted(ca0.items())]
    cap_ds = cac_cap()
    # mẫu gốc (mọi bội số 1) phải cho lại đúng lựa chọn của pha2_khoi_k
    goc = mot_mau(kq, kq_mg, E_X, cap_ds, {c['ma']: 1 for c in ds})
    rng = np.random.default_rng(a.seed)
    dem = collections.Counter()
    thang = collections.Counter()
    bat = collections.Counter()
    co = collections.Counter()
    for i in range(a.n):
        ts = rr.lay_mau_o(ds, rng)
        x = mot_mau(kq, kq_mg, E_X, cap_ds, ts)
        dem[x['loai']] += 1
        if x['loai'] == 'chon':
            thang[x['thang']] += 1
            for c in chon_khoi.tap(x['thang']):
                bat[c] += 1
            co['trai_chieu'] += int(x['trai_chieu'])
            co['phu_thuoc_quan_sat'] += int(x['phu_thuoc_quan_sat'])
            co['xung_dot_buoc8'] += int(x['xung_dot_buoc8'])
        if (i + 1) % 100 == 0:
            print(f'{i + 1}/{a.n} {round(time.time() - t0)}s', flush=True)
    out = {'seed': a.seed, 'n': a.n, 'mau_goc': goc, 'loai': dict(dem), 'tan_suat_thang': dict(thang.most_common()),
           'tan_suat_thanh_phan_bat': {x: bat.get(x, 0) for x in pk.TP},
           'tan_suat_co_o_cau_hinh_thang': dict(co), 'giay': round(time.time() - t0, 1),
           'dien_giai': 'chỉ nói lựa chọn trên dev thay đổi bao nhiêu khi đổi mẫu ô; không dùng để đổi lựa chọn, '
                        'không là bằng chứng hiệu quả (SPEC T-045 bước 7)'}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
