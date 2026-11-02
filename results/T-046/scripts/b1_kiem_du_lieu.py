"""T-046 bước 1: kiểm dữ liệu và đo chi phí (SPEC T-046 bước 1; A1, A7). Không đọc nhãn; chỉ mốc t chế độ (a).

Phần A — độ dài dữ liệu trước t: RE2-TT đọc cột thời gian của traces, metrics, logs (toàn tệp) và báo khoảng có dữ
  liệu trước t; Nezha-OB đọc qua adapter (miền [t − 300, t + 300)) và báo s₀, độ dài hai nửa A/A theo A1.
Phần B — kiểm móc: chạy R0 cửa sổ thật trên 1 ca mỗi dataset có móc; bản ghi phải trùng từng byte bản ghi T1-R0 của
  T-045 (seed 0). Rồi chạy cửa sổ A/A (R0, K-đủ) với G0, G1, G3 và đo giờ từng phần. Chỉ ghi số phép hợp lệ theo
  loại và giờ, không ghi p.
Phần C — chi phí G3 trên dữ liệu tổng hợp AR(1) 300 + 300 và 150 + 150 (10 lần lặp).

Chạy: $PY -B results/T-046/scripts/b1_kiem_du_lieu.py --ra results/T-046/runs/b1-kiem-001 [--phan A,B,C]
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

import t046
from t046 import NS, ROOT
from p3 import selector


def phan_A(mt):
    out = {'RE2-TT': {}, 'Nezha-OB': {}}
    for oid in sorted(mt['re']):
        t = mt['moc_re'][oid]
        files = selector.chon_ca(mt['re'], oid, ROOT, kiem_hash=False)
        st = pq.read_table(files['traces.parquet'], columns=['startTime']).column(0).to_numpy()
        tm = pq.read_table(files['metrics.parquet'], columns=['time']).column(0).to_numpy()
        d = {'trace_dau_truoc_t_giay': round(t - float(st.min()) / 1e6, 3),
             'metric_dau_truoc_t_giay': round(t - float(tm.min()), 3),
             'metric_cuoi_sau_t_giay': round(float(tm.max()) - t, 3)}
        if 'logs.parquet' in files:
            lg = pq.read_table(files['logs.parquet'], columns=['timestamp']).column(0).to_numpy().astype(float)
            d['log_dau_truoc_t_giay'] = round(t - float(lg.min()), 3)
        else:
            d['log_dau_truoc_t_giay'] = None
        out['RE2-TT'][oid] = d
    for oid in sorted(mt['nz']):
        ca, t2, meta = t046.nap('Nezha-OB', oid, 'aa', mt)
        t = meta['t']
        out['Nezha-OB'][oid] = {'s0_truoc_t_giay': round((t * NS - meta['s0_ns']) / NS, 3),
                                't_chay_aa_truoc_t': t - t2, 'nua_dau_giay': round((t2 * NS - meta['s0_ns']) / NS, 3),
                                'nua_sau_giay': t - t2, 'so_span_N': len(ca['spans']), 'so_dong_log_N': len(ca['logs'])}
    re = out['RE2-TT'].values()
    out['tong_hop'] = {
        'RE2-TT_metric_truoc_t_min': min(x['metric_dau_truoc_t_giay'] for x in re),
        'RE2-TT_trace_truoc_t_min': min(x['trace_dau_truoc_t_giay'] for x in re),
        'RE2-TT_log_truoc_t_min': min(x['log_dau_truoc_t_giay'] for x in re if x['log_dau_truoc_t_giay'] is not None),
        'RE2-TT_so_ca_khong_log': sum(1 for x in re if x['log_dau_truoc_t_giay'] is None),
        'Nezha-OB_nua_dau_min_max': [min(x['nua_dau_giay'] for x in out['Nezha-OB'].values()),
                                     max(x['nua_dau_giay'] for x in out['Nezha-OB'].values())],
        'Nezha-OB_nua_sau_min_max': [min(x['nua_sau_giay'] for x in out['Nezha-OB'].values()),
                                     max(x['nua_sau_giay'] for x in out['Nezha-OB'].values())]}
    return out


def _dem_hop_le(bang):
    dem = {}
    for u in bang['pv']:
        if u['hop_le'] and u['trong_U']:
            for d in u['huong']:
                k = f"{u['nhom']}|{d}"
                dem[k] = dem.get(k, 0) + 1
    for u in bang['dem']:
        if u['hop_le'] and u['trong_U']:
            k = f"{u['nhom']}|{u['nhan'] if u['nhan'] in ('NEW_OP', 'STOPPED') else ','.join(u['huong_cham'])}"
            dem[k] = dem.get(k, 0) + 1
    return dem


def phan_B(mt, ra):
    out = {}
    T045 = {'RE2-TT': ROOT / 'results/T-045/runs/b2-t1-re2-seed0-001/ban-ghi.jsonl',
            'Nezha-OB': ROOT / 'results/T-045/runs/b2-t1-nezha-seed0-001/ban-ghi.jsonl'}
    for ds in ('RE2-TT', 'Nezha-OB'):
        oid = sorted(mt['re'] if ds == 'RE2-TT' else mt['nz'])[0]
        kq = {'opaque_id': oid}
        t0 = time.perf_counter()
        ca, t, meta = t046.nap(ds, oid, 'that', mt)
        kq['giay_nap'] = round(time.perf_counter() - t0, 2)
        t0 = time.perf_counter()
        rec, cap, p = t046.chay_chuoi(ca, t, t046.cau_hinh('R0'), t046.CacheMoc())
        kq['giay_chuoi_R0_that'] = round(time.perf_counter() - t0, 2)
        dong = t046.json_ban_ghi(rec, oid)
        cu = None
        with open(T045[ds], encoding='utf-8') as f:
            for x in f:
                if f'"opaque_id":"{oid}"' in x and '"config_id":"T1-R0"' in x:
                    cu = x.rstrip('\n')
                    break
        kq['ban_ghi_trung_T045'] = (cu == dong)
        for cfg in ('R0', 'K-du'):
            ca2, t2, meta2 = t046.nap(ds, oid, 'aa', mt)
            t0 = time.perf_counter()
            rec2, cap2, p2 = t046.chay_chuoi(ca2, t2, t046.cau_hinh(cfg), t046.CacheMoc())
            g_chuoi = time.perf_counter() - t0
            t0 = time.perf_counter()
            bang = t046.bang_phep(ca2, t2, p2, rec2, cap2)
            kq[f'aa_{cfg}'] = {'giay_chuoi': round(g_chuoi, 2), 'giay_bang': round(time.perf_counter() - t0, 2),
                               'giay_G1': round(bang['gio_cong']['G1'], 2), 'giay_G3': round(bang['gio_cong']['G3'], 2),
                               'so_phep_hop_le_theo_loai': _dem_hop_le(bang), 'so_cham_hop_le': bang['so_cham_hop_le'],
                               't_chay': t2, 'meta': {k: v for k, v in meta2.items() if k != 'opaque_id'}}
            print(ds, cfg, kq[f'aa_{cfg}']['giay_chuoi'], kq[f'aa_{cfg}']['giay_G1'], kq[f'aa_{cfg}']['giay_G3'],
                  flush=True)
        out[ds] = kq
    return out


def ar1(rng, n, phi):
    e = rng.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0] / np.sqrt(1 - phi ** 2)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def phan_C():
    import cong
    ts = {'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05, 'n_exact_max': 100}
    rng = np.random.default_rng(123)
    out = {}
    for n in (300, 150):
        for phi in (0.0, 0.9):
            g = []
            for i in range(10):
                x = ar1(rng, 2 * n, phi)
                t = 10_000 * NS
                N, A = list(x[:n]), list(x[n:])
                mN = [t - (n - i) * NS + NS // 2 for i in range(n)]
                mA = [t + i * NS + NS // 2 for i in range(n)]
                t0 = time.perf_counter()
                cong.p_theo_cong('G3', N, mN, A, mA, t, 'len', ts, f'gia|{i}')
                g.append(time.perf_counter() - t0)
            out[f'n{n}_phi{phi}'] = {'giay_moi_lan': round(float(np.mean(g)), 4), 'max': round(float(np.max(g)), 4)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    ap.add_argument('--phan', default='A,B,C')
    a = ap.parse_args()
    ra = Path(a.ra)
    ra.mkdir(parents=True, exist_ok=False)
    mt = t046.moi_truong()
    kq = {'bat_dau': time.strftime('%Y-%m-%dT%H:%M:%S%z')}
    for ph in a.phan.split(','):
        t0 = time.time()
        kq[ph] = {'A': phan_A, 'B': lambda m: phan_B(m, ra), 'C': lambda m: phan_C()}[ph](mt)
        kq[f'giay_{ph}'] = round(time.time() - t0, 1)
        (ra / 'kiem-du-lieu.json').write_bytes((json.dumps(kq, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
        print('xong phan', ph, kq[f'giay_{ph}'], flush=True)
    kq['xong'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    (ra / 'kiem-du-lieu.json').write_bytes((json.dumps(kq, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()
