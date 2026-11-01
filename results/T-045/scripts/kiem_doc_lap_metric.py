"""T-045 T1 (không nhãn): tính lại độc lập vài đơn vị metric RE2-TT ở mốc giả để tách lỗi code với đặc điểm dữ liệu
(lời Minh: "dựng phản ví dụ nhỏ … để tách lỗi code với đặc điểm dữ liệu").

Với mỗi ca và mỗi đơn vị metric được chọn (các đơn vị có cờ hướng lên ở bản ghi mốc giả R0, tối đa k mỗi ca, chọn
theo tên cột đã sắp): đọc chuỗi gốc từ parquet (kiểm SHA-256 qua `p3.selector`), N = [t′−300, t′), A = [t′, t′+300),
t′ = t − 300; tự tính q95 (nội suy tuyến tính), h = q95 + 0,05·|q95|, tỷ lệ vượt, p của Mann–Whitney một phía
(scipy, asymptotic, hiệu chỉnh liên tục), so với `extra.don_vi_phan_vi` của bản ghi. Báo thêm tự tương quan bậc 1 của
N và A, trung vị, độ trôi (hiệu trung vị A − N chia IQR của N).
Chạy: $PY -B results/T-045/scripts/kiem_doc_lap_metric.py --luot results/T-045/runs/b2-t1-re2-mocgia-001 --k 3 --ra <json>
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from scipy.stats import mannwhitneyu

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from p3 import nhan, selector  # noqa: E402


def ac1(x):
    x = np.asarray(x, float)
    if len(x) < 3 or np.std(x) == 0:
        return None
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--k', type=int, default=3)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    al = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    moc = nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')  # chỉ mốc tiêm
    d = Path(a.luot)
    out, so_lech = [], 0
    for x in open(d / 'ban-ghi.jsonl', encoding='utf-8'):
        r = json.loads(x)
        o = r['opaque_id']
        tp = moc[o] - 300
        co = sorted((u for u in r['extra']['don_vi_phan_vi'] if u['ma'].startswith('metric|') and u.get('F_raw_len')),
                    key=lambda u: u['ma'])[:a.k]
        if not co:
            continue
        f = selector.chon_ca(al, o, ROOT, kiem_hash=True)
        mt = pq.read_table(f['metrics.parquet']).to_pandas()
        tm = pd.to_numeric(mt['time']).to_numpy(np.int64)
        for u in co:
            col = u['ma'].split('|', 1)[1]
            v = pd.to_numeric(mt[col], errors='coerce').to_numpy(float)
            N = v[(tm >= tp - 300) & (tm < tp) & np.isfinite(v)]
            A = v[(tm >= tp) & (tm < tp + 300) & np.isfinite(v)]
            q = float(np.quantile(N, 0.95))
            h = q + 0.05 * abs(q)
            rN, rA = float(np.mean(N > h)), float(np.mean(A > h))
            p = float(mannwhitneyu(A, N, alternative='greater', method='asymptotic', use_continuity=True).pvalue)
            iqr = float(np.subtract(*np.quantile(N, [0.75, 0.25])))
            khop = (abs(p - u['p_len']) <= 1e-9 * max(1.0, p) and abs(rA - rN - u['e_len']) <= 1e-9
                    and len(N) == u['n_N'] and len(A) == u['n_A'])
            so_lech += int(not khop)
            out.append({'ca': o, 'cot': col, 'n_N': len(N), 'n_A': len(A), 'p_tinh_lai': p, 'p_ban_ghi': u['p_len'],
                        'e_tinh_lai': rA - rN, 'e_ban_ghi': u['e_len'], 'khop': khop,
                        'ac1_N': ac1(N), 'ac1_A': ac1(A), 'trung_vi_N': float(np.median(N)),
                        'trung_vi_A': float(np.median(A)),
                        'troi_tren_IQR': (float(np.median(A) - np.median(N)) / iqr) if iqr else None})
    ac = [x['ac1_N'] for x in out if x['ac1_N'] is not None]
    kq = {'so_don_vi': len(out), 'so_lech_ban_ghi': so_lech,
          'ac1_N_trung_vi': float(np.median(ac)) if ac else None,
          'ac1_N_ty_le_tren_0_5': float(np.mean(np.array(ac) > 0.5)) if ac else None, 'don_vi': out}
    Path(a.ra).write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in kq.items() if k != 'don_vi'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
