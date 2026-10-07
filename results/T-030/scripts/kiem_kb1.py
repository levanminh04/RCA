"""T-030 bước 5: K-B1 (giao-thuc-v2 §6.6, WHY-29).

Dựng tracets_err, tracets_lat theo quy ước tác giả (lưới = cột time của file tác giả, ngưỡng μ + 3σ trên toàn
file) và luật tên cột TT, cho 30 ca dev; so với file tác giả theo đúng tên cột (cột, bin); cột chỉ có ở một bên
tính sai mọi ô; NaN của bản tác giả coi là 0 (TORAI ffill rồi điền 0). Đạt khi ≥ 95 % ô trùng cho từng chuỗi,
gộp 30 ca. Không chạy TORAI, không đọc nhãn (chỉ allowlist để tìm tệp). Báo theo mã mờ.

python kiem_kb1.py <lan-thu> [cach_con]
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from p3 import selector, torai_b  # noqa: E402
from p3.runner import _tac_gia_A  # noqa: E402

COT = ['traceID', 'spanID', 'parentSpanID', 'serviceName', 'operationName', 'startTime', 'duration', 'statusCode']


def main(lan, cach_con='som_nhat'):
    t0 = time.perf_counter()
    out_dir = ROOT / 'results' / 'T-030' / 'runs' / f'kb1-lan{lan}'
    out_dir.mkdir(parents=True, exist_ok=True)
    al = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    tong = {s: {'so_o': 0, 'o_trung': 0} for s in ('tracets_err', 'tracets_lat')}
    rows = []
    for i, oid in enumerate(sorted(al)):
        f = selector.chon_ca(al, oid, ROOT, tep=['traces.parquet'])
        tr = pd.read_parquet(f['traces.parquet'], columns=COT)
        a = _tac_gia_A(al[oid]['case_dir'])
        mau = {s: pd.read_csv(a[s]).set_index('time') for s in ('tracets_err', 'tracets_lat')}
        err, lat, info = torai_b.theo_quy_uoc_tac_gia(tr, mau['tracets_err'].index.to_numpy(), cach_con)
        r = {'opaque_id': oid, 'span': int(len(tr)), 'span_http_con_nhieu_service': info['span_http_con_nhieu_service']}
        for s, mine in (('tracets_err', err), ('tracets_lat', lat)):
            if not mau[s].index.equals(mau['tracets_err'].index):
                r[s + '_luoi_khac_err'] = True
            c = torai_b.so_theo_ten_cot(mine, mau[s])
            r[s] = {k: c[k] for k in ('so_o', 'o_trung', 'so_cot_hop', 'o_nan_ban_tac_gia')}
            r[s]['ty_le'] = c['o_trung'] / c['so_o'] if c['so_o'] else None
            r[s]['cot_chi_ban_dung'] = c['cot_chi_ban_dung']
            r[s]['cot_chi_ban_tac_gia'] = c['cot_chi_ban_tac_gia']
            tong[s]['so_o'] += c['so_o']
            tong[s]['o_trung'] += c['o_trung']
        rows.append(r)
        print(f'[{i + 1}/30] {oid} err={r["tracets_err"]["ty_le"]:.4f} lat={r["tracets_lat"]["ty_le"]:.4f} '
              f'cot_thua={len(r["tracets_err"]["cot_chi_ban_dung"])} cot_thieu={len(r["tracets_err"]["cot_chi_ban_tac_gia"])} '
              f'{time.perf_counter() - t0:.1f}s', flush=True)
        del tr
    for s in tong:
        tong[s]['ty_le'] = tong[s]['o_trung'] / tong[s]['so_o']
        tong[s]['dat_95'] = tong[s]['ty_le'] >= 0.95
    doc = {'mo_ta': __doc__.strip(), 'lan_thu': lan, 'cach_con': cach_con,
           'tao_luc_utc': datetime.now(timezone.utc).isoformat(), 'tong': tong,
           'dat': all(v['dat_95'] for v in tong.values()), 'ca': rows,
           'thoi_gian_s': round(time.perf_counter() - t0, 1)}
    (out_dir / 'kb1.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'tong': tong, 'dat': doc['dat']}, ensure_ascii=False))


if __name__ == '__main__':
    main(int(sys.argv[1]), *(sys.argv[2:3]))
