"""T-031: chạy một phương pháp qua runner P3 trên danh sách ca, ghi tóm tắt không có thứ hạng.

Mỗi lượt = một ca × một phương pháp × một seed × một hash seed, tiến trình con, giới hạn 3.600 s (SPEC T-031).
Tuần tự; kiểm RAM trước mỗi lượt. Bản ghi §13 đầy đủ nằm trong luot/<run_id>/; tom-tat.json chỉ ghi trạng thái,
chi phí, chẩn đoán và hash thứ tự (để so lặp lại mà không in thứ hạng). Lỗi runner ghi riêng, không gán trạng
thái phương pháp. TORAI: sau mỗi lượt ghi manifest rồi xóa bảng CSV (telemetry đã cắt); với nguồn B, trước khi
xóa, tính K-B2 (tổng `logts` mỗi service so với số dòng log của service trong cửa sổ).

python chay.py <ten> <method> <ca: all|oid,oid,...> [model=svr|ols] [hashseeds=0] [seeds=-] [mode=a]
               [tap_cot=bocpd|tat_ca] [doi_moc=0]
doi_moc: cộng vào mốc truyền cho runner (chỉ dùng cho phép kiểm §11.8 với bộ phát hiện: job bộ phát hiện không
nhận mốc, báo động phải giống hệt).
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import chung
from p3 import cua_so, runner


def h(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def tim_run_dir(base, oid, method, mode, seed, hs):
    ds = sorted(Path(base).glob(f'{method}-{mode}-{oid}-s{seed}-h{hs}-*'), key=lambda p: p.stat().st_mtime)
    return ds[-1] if ds else None


def doc_ket_qua(run_dir):
    for p in (run_dir / 'ket-qua.json', run_dir / 'torai' / 'ket-qua.json'):
        if p.exists():
            return json.loads(p.read_text(encoding='utf-8'))
    return None


def tom_circa(kq, t):
    out = {}
    k0 = (kq or {}).get('ket_qua_nhieu', [{}])[0]
    d = k0.get('diagnostics') or {}
    nodes = d.get('nodes') or {}
    edges = sorted([p, n] for n, v in nodes.items() for p in v.get('parents', []))
    out['circa'] = {
        'status_worker': k0.get('status'), 'error_worker': k0.get('error'),
        'routes': d.get('regression_routes'),
        'vef_nut': [{'nut': n, 'so_cha': len(v.get('parents', [])), 'loi': v.get('regression_error')}
                    for n, v in sorted(nodes.items()) if v.get('regression_route') == 'value_error_fallback'],
        'vef_nut_co_cha': sum(1 for v in nodes.values()
                              if v.get('regression_route') == 'value_error_fallback' and v.get('parents')),
        'z_khong_huu_han': sum(1 for v in nodes.values() if not math.isfinite(float(v.get('rht_score', float('nan'))))),
        'so_nut': (d.get('graph') or {}).get('metric_nodes'), 'so_canh': (d.get('graph') or {}).get('metric_edges'),
        'so_canh_tu_cha': len(edges), 'cha_lon_nhat': max((len(v.get('parents', [])) for v in nodes.values()), default=0),
        'canh_hash': h(edges), 'call_edges_hash': h((k0.get('extra') or {}).get('call_edges')),
        'dag': (d.get('graph') or {}).get('dag'), 'current': d.get('circa_current'),
        'current_bang_t_cong_299': d.get('circa_current') == t + 299 if d.get('circa_current') is not None else None,
        'spans_do_thi': d.get('spans_do_thi'), 'hashseed_worker': d.get('hashseed')}
    kn = (kq or {}).get('ket_qua_nhieu') or []
    if len(kn) == 4:  # model=ols_vinf: OLS gốc rồi V∞ (Q-81)
        vn = (kn[2].get('diagnostics') or {}).get('vinf_nodes') or {}
        out['circa']['vinf'] = {'inf': vn.get('inf'), 'zero': vn.get('zero'),
                                'so_inf': len(vn.get('inf') or []), 'so_zero': len(vn.get('zero') or [])}
    return out


def k_b2(run_dir, files, t):
    """K-B2 cho một lượt nguồn B: tổng logts B mỗi service = số dòng log của service trong cửa sổ."""
    import pandas as pd
    p = run_dir / 'bang' / 'logts.csv'
    if not p.exists():
        return None
    lt = pd.read_csv(p).set_index('time')
    tong_b = {}
    for c in lt.columns:
        s = c.rsplit('_', 1)[0]
        tong_b[s] = tong_b.get(s, 0) + float(lt[c].sum())
    if 'logs.parquet' not in files:
        return {'co_logs': False, 'so_service_logts': len(tong_b), 'dat': len(tong_b) == 0}
    lg = cua_so.cat_log(pd.read_parquet(files['logs.parquet'], columns=['timestamp', 'container_name']), t)
    dem = lg.groupby('container_name').size().to_dict()
    sv = sorted(set(dem) | set(tong_b))
    lech = {s: [tong_b.get(s, 0.0), int(dem.get(s, 0))] for s in sv if tong_b.get(s, 0.0) != dem.get(s, 0)}
    return {'co_logs': True, 'so_service': len(sv), 'so_dong_log_cua_so': int(len(lg)),
            'tong_logts': float(sum(tong_b.values())), 'service_lech': lech, 'dat': not lech}


def tom_tat(rec_list, kq, run_dir, method, t, files):
    r = {}
    if rec_list:
        r['bien_the'] = {x.get('variant', method): {
            'status': x['status'], 'method_status_raw': x.get('method_status_raw'), 'error': x.get('error'),
            'thu_tu_hash': h(x.get('ranking_native')),
            'ban_ghi_hash': h({k: v for k, v in x.items() if k not in ('run_id', 'opaque_id', 'cost', 'input_sha256')}),
            'key_check': (x.get('diagnostics') or {}).get('key_check'),
            'sets': {k: (x.get('sets') or {}).get(k) for k in ('observed', 'returned')}} for x in rec_list}
        x0 = rec_list[0]
        r['cost'] = {k: x0['cost'].get(k) for k in ('wall_s', 'peak_rss_mb', 'read_bytes', 'write_bytes', 'exit_code')}
        r['buoc_s'] = x0['cost'].get('buoc_s')
        r['input_shape'] = {k: v for k, v in (x0.get('input_shape') or {}).items() if k != 'metric_columns'}
        r['window'] = {k: v for k, v in (x0.get('window') or {}).items() if k != 'N' and k != 'A'} if x0.get('window') else None
        dg = x0.get('diagnostics') or {}
        if method == 'microrank':
            r['counts'] = dg.get('counts')
        if method == 'tracerca':
            r['ji_nan'] = dg.get('ji_nan')
        if method == 'baro':
            r['rank_equals_column_order'] = dg.get('rank_equals_column_order')
        if method.startswith('torai'):
            r['torai'] = {k: dg.get(k) for k in ('cum', 'cum_nhieu_service', 'cum_du_phong', 'ty_le_du_phong')}
            r['chuan_bi'] = (x0.get('extra') or {}).get('chuan_bi')
        if method in ('bocpd', 'nsigma'):
            r['so_bao_dong'] = len(x0.get('alarms') or [])
            r['luot_rca'] = x0.get('luot_rca')
            r['bat_dau_danh_gia'] = x0.get('bat_dau_danh_gia')
            r['bao_dong_hash'] = h(x0.get('alarms'))
    if method == 'circa':
        r.update(tom_circa(kq, t))
    return r


def main(ten, method, ca, model=None, hashseeds='0', seeds='-', mode='a', tap_cot='bocpd', doi_moc='0'):
    al, moc = chung.nap()
    ids = sorted(al) if ca == 'all' else ca.split(',')
    hss = [int(x) for x in hashseeds.split(',')]
    sds = [None] if seeds == '-' else [int(x) for x in seeds.split(',')]
    L = chung.Luot(ten, {'phuong_phap': method, 'model': model, 'hashseeds': hss, 'seeds': sds, 'mode': mode,
                         'ca': ids, 'tap_cot': tap_cot, 'doi_moc': int(doi_moc)})
    base = L.dir / 'luot'
    rows, n, tong = [], 0, len(ids) * len(hss) * len(sds)
    for oid in ids:
        files = chung.selector.chon_ca(al, oid, chung.ROOT, kiem_hash=False)
        t = moc[oid] + int(doi_moc) if mode == 'a' else None
        for hs in hss:
            for sd in sds:
                n += 1
                ram = chung.ram_trong_gb()
                row = {'opaque_id': oid, 'hashseed': hs, 'seed': sd, 'ram_truoc_gb': ram}
                recs, loi = None, None
                try:
                    recs = runner.chay_luot(al, oid, method, mode, t, base, chung.TIMEOUT_S, seed=sd, hashseed=hs,
                                            model=model, tap_cot=tap_cot)
                except Exception as exc:  # noqa: BLE001 — lỗi runner hoặc bản ghi không hợp lệ
                    loi = f'{type(exc).__name__}: {exc}'
                rd = tim_run_dir(base, oid, method, mode, sd, hs)
                row['run_id'] = rd.name if rd else None
                kq = doc_ket_qua(rd) if rd else None
                if loi:
                    row['loi_runner'] = loi
                row.update(tom_tat(recs, kq, rd, method, t, files))
                if method == 'torai_B' and rd is not None:
                    row['k_b2'] = k_b2(rd, files, t)
                if method.startswith('torai') and rd is not None:
                    row['bang_manifest'] = chung.don_bang_torai(rd)
                rows.append(row)
                st = {v: b['status'] for v, b in (row.get('bien_the') or {}).items()}
                L.ghi(f'[{n}/{tong}] {oid} h{hs} s{sd} {st or "LOI_RUNNER: " + str(loi)} '
                      f'wall={(row.get("cost") or {}).get("wall_s")}s rss={(row.get("cost") or {}).get("peak_rss_mb")}MB '
                      f'RAM={ram}GB')
                chung.ghi_json(L.dir / 'tom-tat.json', {'mo_ta': __doc__.strip(), 'run': L.dir.name,
                                                        'src_p3_sha256': L.ch['src_p3']['tong'],
                                                        'cau_hinh': {'method': method, 'model': model, 'mode': mode},
                                                        'xong': False, 'luot': rows})
    tw = round(sum((r.get('cost') or {}).get('wall_s') or 0 for r in rows), 1)
    doc = {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'src_p3_sha256': L.ch['src_p3']['tong'],
           'cau_hinh': {'method': method, 'model': model, 'mode': mode}, 'xong': True,
           'tong_wall_s': tw, 'max_peak_rss_mb': max(((r.get('cost') or {}).get('peak_rss_mb') or 0) for r in rows),
           'so_loi_runner': sum('loi_runner' in r for r in rows), 'luot': rows}
    chung.ghi_json(L.dir / 'tom-tat.json', doc)
    L.xong({'tong_wall_s': tw, 'so_luot': len(rows), 'so_loi_runner': doc['so_loi_runner']})


if __name__ == '__main__':
    args = sys.argv[1:4]
    kw = dict(a.split('=', 1) for a in sys.argv[4:])
    main(*args, **kw)
