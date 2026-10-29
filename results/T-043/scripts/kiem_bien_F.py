"""Phiên 8 T-043: kiểm căn cứ của F_s (khoảng ghi của file) trên Nezha-OB dev. Chỉ đọc, không nhãn.

Trả lời nhận xét của Codex: phần ngoài F_s gán XÁC NHẬN THIẾU THU dựa trên bằng chứng thu/xuất hay chỉ dựa trên việc
không thấy bản ghi. Đo:
1. mật độ bản ghi ở hai mép F_s (thời gian để có 1, 10, 100 bản ghi đầu và cuối của mỗi nguồn): mép càng dày thì
   phần không biết giữa mốc xuất thật và bản ghi đầu càng ngắn;
2. khe giữa các file phút liền nhau;
3. metric (file theo ngày, phủ cả cửa sổ) trong phần N nằm ngoài F_s của trace: hệ có hoạt động không
   (bằng chứng hỗ trợ theo B1.3b, không tự xác nhận).
Chạy: python -B results/T-043/scripts/kiem_bien_F.py --out results/T-043/runs/bien-F-001
"""
import argparse
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np

from p3 import nezha

NS = nezha.NS


def doc_moc(path, col):
    csv.field_size_limit(10_000_000)
    with open(path, encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        return np.array(sorted(int(row[col]) for row in r), dtype=np.int64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=False)
    t0 = time.time()
    allow = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
    cases = []
    for oid in sorted(allow):
        sel = nezha.chon_ca(allow, oid, ROOT)
        t_ns = sel['t_ns']
        row = {'opaque_id': oid}
        for kind, col in (('trace', 'EndTimeUnixNano'), ('log', 'TimeUnixNano')):
            files = sorted(rel for rel in sel['files'] if f'/{kind}/' in rel)
            per = [doc_moc(sel['files'][rel]['absolute_path'], col) for rel in files]
            allv = np.sort(np.concatenate(per))
            ranges = [(int(x[0]), int(x[-1])) for x in per]
            gaps = [(b0 - a1) / NS for (a0, a1), (b0, b1) in zip(ranges, ranges[1:])]
            row[kind] = {
                'F_rel_t_s': [(allv[0] - t_ns) / NS, (allv[-1] - t_ns) / NS],
                'mep_dau_ms': {k: (allv[k - 1] - allv[0]) / 1e6 for k in (2, 10, 100)},
                'mep_cuoi_ms': {k: (allv[-1] - allv[-k]) / 1e6 for k in (2, 10, 100)},
                'khe_giua_file_s': gaps,
                'ban_ghi': int(len(allv)),
            }
        win = nezha.doc_cua_so(sel)
        F0 = row['trace']['F_rel_t_s'][0]
        times = win['metric']['time'].to_numpy(np.int64)
        truoc_F = [(i, (x - t_ns) / NS) for i, x in enumerate(times) if (x - t_ns) / NS < F0]
        hd = {}
        for name, arr in win['metric_arrays'].items():
            if not name.endswith(('PodWorkload-Ops', 'FrontLatencyP90-s', 'FrontSuccessRate-pct')):
                continue
            vals = np.concatenate([arr['normal'], arr['anomalous']])
            hd[name] = [None if not np.isfinite(vals[i]) else float(vals[i]) for i, _ in truoc_F]
        row['metric_truoc_F_trace'] = {'moc_rel_t_s': [round(s, 3) for _, s in truoc_F], 'gia_tri': hd}
        wl = [v for k, vs in hd.items() if k.endswith('PodWorkload-Ops') for v in vs if v is not None]
        row['workload_duong_truoc_F'] = int(sum(1 for v in wl if v > 0))
        row['workload_so_diem_truoc_F'] = len(wl)
        cases.append(row)
    tong = {
        'so_ca': len(cases),
        'max_mep_dau_100_ban_ghi_ms': {k: max(c[k]['mep_dau_ms'][100] for c in cases) for k in ('trace', 'log')},
        'max_mep_cuoi_100_ban_ghi_ms': {k: max(c[k]['mep_cuoi_ms'][100] for c in cases) for k in ('trace', 'log')},
        'max_mep_dau_2_ban_ghi_ms': {k: max(c[k]['mep_dau_ms'][2] for c in cases) for k in ('trace', 'log')},
        'max_khe_giua_file_s': {k: max(max(c[k]['khe_giua_file_s']) for c in cases) for k in ('trace', 'log')},
        'ca_co_workload_duong_truoc_F': sum(1 for c in cases if c['workload_duong_truoc_F'] > 0),
        'tong_diem_workload_truoc_F': sum(c['workload_so_diem_truoc_F'] for c in cases),
        'tong_diem_workload_duong_truoc_F': sum(c['workload_duong_truoc_F'] for c in cases),
        'giay': round(time.time() - t0, 1),
    }
    out = {'schema': 'T043-bien-F-v1', 'labels_read': False, 'tong_hop': tong, 'cases': cases}
    (out_dir / 'ket-qua.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(tong, ensure_ascii=False))


if __name__ == '__main__':
    main()
