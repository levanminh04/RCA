"""T-025 bước 3: lượt RCA tại báo động đầu t̂ (§7.5) cho BARO, CIRCA OLS (RHT+DA kèm RHT-only), TORAI B seed 0, 1, 2.

t̂ lấy từ bản ghi bộ phát hiện đã lưu (`luot_rca.t_hat`); không đọc nhãn hay mốc tiêm. Ca bộ phát hiện không `OK` hoặc
không có báo động: không có lượt RCA (ghi lý do). Cửa sổ quanh t̂ như §5, runner cắt ở biên file và ghi độ dài thực.
Mỗi lượt giới hạn 3.600 s (SPEC). TORAI: ghi manifest rồi xóa bảng CSV sau mỗi lượt. Hash seed 0 cho mọi lượt
(CIRCA builder, §6.5).

python rca_b.py <ten> tu=<thư mục lượt bộ phát hiện> [detector=<tên>] [ranker=baro,circa,torai_B] [ca=all|oid,...]
python rca_b.py <ten> t_co_dinh=<oid>:<vị trí>,<vị trí>   # tự kiểm biên (N8): vị trí là chỉ số dòng trong bản ghi
"""
import hashlib
import json
import sys
from pathlib import Path

import chung

SEEDS = {'torai_B': [0, 1, 2]}
MODEL = {'circa': 'ols'}


def h(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def doc_bo_phat_hien(d):
    out = {}
    for p in sorted(Path(d).glob('luot/*/ban-ghi-0.json')):
        r = json.loads(p.read_text(encoding='utf-8'))
        out[r['opaque_id']] = r
    return out


def main(ten, tu=None, detector=None, ranker='baro,circa,torai_B', ca='all', t_co_dinh=None):
    from p3.adapters import phat_hien  # noqa: F401  (kiểm import trong môi trường)
    import chay_b
    runner = chung.cau_hinh_runner()
    al = chung.nap_allowlist()
    rankers = ranker.split(',')
    viec = []  # (oid, t, detector_columns, nguon)
    if t_co_dinh:
        import pandas as pd
        oid, vt = t_co_dinh.split(':')
        f = chung.selector.chon_ca(al, oid, chung.DATA_ROOT, kiem_hash=True, tep=['metrics.parquet'])
        times = pd.read_parquet(f['metrics.parquet'], columns=['time'])['time'].to_numpy()
        for v in vt.split(','):
            viec.append((oid, int(times[int(v)]), None, {'vi_tri': int(v)}))
        detector = detector or 'kiem-bien'
    else:
        tu = Path(tu) if Path(tu).is_absolute() else chung.OUT / tu
        recs = doc_bo_phat_hien(tu)
        ids = sorted(recs) if ca == 'all' else ca.split(',')
        detector = detector or recs[ids[0]]['method']
        for oid in ids:
            r = recs[oid]
            th = (r.get('luot_rca') or {}).get('t_hat')
            nguon = {'detector_run_id': r['run_id'], 'detector_status': r['status']}
            if r['status'] != 'OK' or th is None:
                viec.append((oid, None, None, dict(nguon, ly_do='bộ phát hiện không OK' if r['status'] != 'OK'
                                                    else 'không có báo động')))
            else:
                viec.append((oid, int(th), r.get('detector_columns'), nguon))
    L = chung.Luot(ten, {'mode': 'b', 'detector': detector, 'tu': str(tu) if tu else None, 'ranker': rankers,
                         'seeds': SEEDS, 'model': MODEL, 'timeout_moi_luot_s': chung.TIMEOUT_MAC_DINH,
                         't_co_dinh': t_co_dinh})
    base = L.dir / 'luot'
    rows = []
    tong = sum(len(SEEDS.get(m, [None])) for m in rankers) * sum(1 for v in viec if v[1] is not None)
    n = 0
    for oid, t, cols, nguon in viec:
        if t is None:
            rows.append({'opaque_id': oid, 't_hat': None, **nguon})
            L.ghi(f'{oid}: không có lượt RCA ({nguon["ly_do"]})')
            continue
        for m in rankers:
            for sd in SEEDS.get(m, [None]):
                n += 1
                doi = 0.0 if chung.EC2 else chay_b.cho_t024(L)
                row = {'opaque_id': oid, 't_hat': t, 'method': m, 'seed': sd, 'doi_t024_s': doi, **nguon}
                try:
                    recs = runner.chay_luot(al, oid, m, 'b', t, base, chung.TIMEOUT_MAC_DINH, repo_root=chung.DATA_ROOT,
                                            seed=sd, hashseed=0, model=MODEL.get(m), detector=detector,
                                            detector_columns=cols)
                    row['run_id'] = recs[0]['run_id']
                    row['bien_the'] = {x['variant']: {'status': x['status'], 'error': x.get('error'),
                                                      'thu_tu_hash': h(x.get('ranking_native')),
                                                      'key_check': (x.get('diagnostics') or {}).get('key_check'),
                                                      'sets': {k: (x.get('sets') or {}).get(k)
                                                               for k in ('observed', 'returned')}} for x in recs}
                    w = recs[0].get('window') or {}
                    row['window'] = {k: w.get(k) for k in ('rows_N', 'rows_A', 'seconds_N', 'seconds_A', 'spans_N',
                                                           'spans_A', 'log_rows_N', 'log_rows_A', 'circa_current')}
                    row['cost'] = {k: recs[0]['cost'].get(k) for k in ('wall_s', 'peak_rss_mb', 'exit_code')}
                    if m.startswith('torai'):
                        row['bang_manifest'] = chung.don_bang_torai(base / recs[0]['run_id'])
                except Exception as exc:  # noqa: BLE001 — lỗi runner
                    row['loi_runner'] = f'{type(exc).__name__}: {exc}'
                    ds = sorted(base.glob(f'{m}-b-{oid}-s{sd}-h0-*'), key=lambda p: p.stat().st_mtime)
                    if ds and m.startswith('torai'):
                        row['bang_manifest'] = chung.don_bang_torai(ds[-1])
                rows.append(row)
                st = {v: b['status'] for v, b in (row.get('bien_the') or {}).items()}
                L.ghi(f'[{n}/{tong}] {oid} t={t} {m} s{sd} {st or "LOI_RUNNER " + row.get("loi_runner", "")} '
                      f'N={(row.get("window") or {}).get("seconds_N")}s A={(row.get("window") or {}).get("seconds_A")}s '
                      f'wall={(row.get("cost") or {}).get("wall_s")}s')
                chung.ghi_json(L.dir / 'tom-tat.json', {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'xong': False,
                                                        'src_p3_sha256': L.ch['src_p3']['tong'], 'luot': rows})
    tw = round(sum((r.get('cost') or {}).get('wall_s') or 0 for r in rows), 1)
    chung.ghi_json(L.dir / 'tom-tat.json', {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'xong': True,
                                            'src_p3_sha256': L.ch['src_p3']['tong'], 'tong_wall_s': tw,
                                            'so_loi_runner': sum('loi_runner' in r for r in rows), 'luot': rows})
    L.xong({'tong_wall_s': tw, 'so_luot': n, 'so_loi_runner': sum('loi_runner' in r for r in rows)})


if __name__ == '__main__':
    kw = dict(a.split('=', 1) for a in sys.argv[2:])
    main(sys.argv[1], **kw)
