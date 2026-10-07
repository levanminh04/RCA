"""T-030 bước 1: đếm D1 (§5.3) trên 30 ca dev. Chỉ đọc metrics.parquet và mốc tiêm."""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from p3 import selector, cua_so, nhan  # noqa: E402

OUT = ROOT / 'results' / 'T-030' / 'd1-o-khac.json'


def main():
    t0 = time.perf_counter()
    al = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    moc = nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')
    rows = []
    for i, oid in enumerate(sorted(al)):
        f = selector.chon_ca(al, oid, ROOT, tep=['metrics.parquet'])
        m = pd.read_parquet(f['metrics.parquet'])
        r = cua_so.dem_d1(m, moc[oid])
        r['opaque_id'] = oid
        rows.append(r)
        print(f'[{i + 1}/30] {oid} o_khac={r["o_khac"]} cot={r["cot_co_o_khac"]} '
              f'{time.perf_counter() - t0:.1f}s', flush=True)
    doc = {
        'mo_ta': 'D1 (giao-thuc-v2 §5.3): số ô metric khác nhau giữa "cắt trước, tiền xử lý sau" '
                 '(P3) và thứ tự main.py (tiền xử lý toàn file rồi cắt), trong cửa sổ [t-300, t+300). '
                 'Không dùng nhãn nào ngoài mốc tiêm. Tiền xử lý: bỏ _latency-50, inf->NaN, ffill, điền 0.',
        'script': 'results/T-030/scripts/dem_d1.py',
        'tao_luc_utc': datetime.now(timezone.utc).isoformat(),
        'tong': {'ca': len(rows), 'ca_co_o_khac': sum(r['o_khac'] > 0 for r in rows),
                 'o_khac': sum(r['o_khac'] for r in rows), 'o': sum(r['n_o'] for r in rows),
                 'ca_cat_dong_khac_thoi_gian': sum(not r['cat_theo_dong_trung_cat_theo_thoi_gian'] for r in rows)},
        'ca': rows,
        'thoi_gian_s': round(time.perf_counter() - t0, 3),
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(doc['tong'], ensure_ascii=False))


if __name__ == '__main__':
    main()
