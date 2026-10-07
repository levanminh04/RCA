"""T-031 bước 5: kiểm trên ca thật (giao-thuc-v2 §11.6, §11.9, §11.10). Không dùng nhãn, không chấm.

1. §11.6 lấy khóa: BARO và TORAI kiểm trong adapter ở mọi lượt (không khớp → lỗi runner), ở đây chỉ tổng hợp
   `key_check` từ các tóm tắt; TraceRCA: `ji` hữu hạn của adapter so với phép tính độc lập
   `results/T-015/scripts/check_tracerca.py::independent_spans` trên cùng span đã cắt, ở 3 ca pilot (cửa sổ thật)
   và ở cửa sổ bình thường của ca trung vị dưới; CIRCA: `current` = thời điểm quan sát cuối của metric trong A,
   tính lại từ dữ liệu ở 30 ca.
2. §11.9 hai cửa sổ bình thường trên ca trung vị dưới của từng phương pháp: mốc giả t′ = t0 + 360 (t0 = thời điểm
   metric đầu file), N = [t0+60, t0+360), A = [t0+360, t0+660), nằm trong 720 s đầu (khai trước, SPEC bước 5).
   Ghi trạng thái và điểm; không chỉnh ngưỡng. TORAI seed 0, nguồn đã khóa; CIRCA mô hình đã khóa, hash seed 0.
3. §11.10 hoán vị trên ca trung vị dưới: bản sao dữ liệu trong work/ (xóa sau khi chạy, giữ manifest): 'cot' =
   hoán vị cột metric (giữ `time` đầu), 'dong' = hoán vị dòng span và dòng log. BARO: cot; SimpleRCA: cot, dong;
   TraceRCA: dong; CIRCA: cot, dong. So thứ hạng thực thể theo nhóm hòa với lượt gốc (không in thứ hạng).
   MicroRank dừng ở D6; TORAI không kiểm hoán vị (GMM và Drain phụ thuộc thứ tự theo thiết kế; như T-030).

python kiem_ca_that.py ca_pilot=<ca-pilot.json> baro=<tom-tat> simplerca=<tom-tat> tracerca=<tom-tat>
       circa=<tom-tat h0 mô hình khóa> circa_model=<svr|ols> torai=<tom-tat nguồn khóa> torai_method=<torai_A|torai_B>
"""
import importlib.util
import json
import math
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import chung
from p3 import cua_so, runner

COT_CK = ['traceID', 'spanID', 'parentSpanID', 'serviceName', 'methodName', 'operationName', 'startTime', 'duration']
TP = 360  # mốc giả, giây tính từ đầu bản ghi (khai trước trong SPEC)


def nap(p):
    return json.loads(open(p, encoding='utf-8').read())


def ck_mod():
    spec = importlib.util.spec_from_file_location('t015_check_tracerca', chung.ROOT / 'results/T-015/scripts/check_tracerca.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ban_ghi(run_dir):
    return [json.loads(p.read_text(encoding='utf-8')) for p in sorted(Path(run_dir).glob('ban-ghi-*.json'))]


def nhom(rec):
    """Thứ hạng thực thể theo nhóm hòa: [(tập thực thể, khóa)] theo thứ tự."""
    g = {}
    for e in rec['entity_ranking']:
        g.setdefault(e['tie_group'], [set(), tuple(e['key'])])[0].add(e['entity'])
    return [g[k] for k in sorted(g)]


def so_nhom(a, b, rtol=1e-9):
    na, nb = nhom(a), nhom(b)
    exact = [(sorted(x), list(k)) for x, k in na] == [(sorted(x), list(k)) for x, k in nb]
    gan = len(na) == len(nb) and all(x == y and len(k) == len(l) and all(
        math.isclose(u, v, rel_tol=rtol, abs_tol=1e-12) for u, v in zip(k, l)) for (x, k), (y, l) in zip(na, nb))
    return {'giong_het': exact, 'giong_trong_sai_so': gan, 'so_nhom': [len(na), len(nb)],
            'trang_thai': [a['status'], b['status']]}


def so_ji(rec, traces_win, t, ck):
    ad = {r['item']: r['key'][0] for r in rec['ranking']}
    n_nan_ad = (rec.get('diagnostics') or {}).get('ji_nan')
    try:
        ind = ck.independent_spans(traces_win[COT_CK], float(t) * 1e6)
    except ValueError as exc:
        return {'doc_lap': f'ValueError: {exc}', 'adapter': rec['status'], 'khop': rec['status'] == 'ERROR'}
    fin = {op: float(s) for op, s in ind['items'] if s is not None and math.isfinite(float(s))}
    n_nan = len(ind['items']) - len(fin)
    same = set(fin) == set(ad)
    d = max((abs(fin[o] - ad[o]) / max(abs(fin[o]), abs(ad[o]), 1e-300) for o in fin if o in ad), default=0.0)
    return {'so_op_huu_han': [len(ad), len(fin)], 'so_nan': [n_nan_ad, n_nan], 'cung_tap_op': same,
            'sai_lech_tuong_doi_max': d, 'khop': same and n_nan == n_nan_ad and d <= 1e-10,
            'trang_thai_doc_lap': ind['status']}


def tom_ban_ghi(recs):
    out = {}
    for r in recs:
        ks = [e['key'][0] for e in r['entity_ranking']]
        out[r['variant']] = {'status': r['status'], 'method_status_raw': r.get('method_status_raw'),
                             'error': r.get('error'), 'so_thuc_the': len(ks), 'so_nhom_hoa': len({e['tie_group'] for e in r['entity_ranking']}),
                             'khoa_dau_5': ks[:5], 'khoa_max': max(ks) if ks else None,
                             'khoa_trung_vi': float(np.median(ks)) if ks else None,
                             'cost_wall_s': (r.get('cost') or {}).get('wall_s')}
    return out


def run_dir_cua(tom, oid, seed=None, hashseed=None):
    for r in nap(tom)['luot']:
        if r['opaque_id'] == oid and (seed is None or r.get('seed') == seed) and (hashseed is None or r.get('hashseed') == hashseed):
            return Path(tom).parent / 'luot' / r['run_id']
    return None


def ban_sao(al, oid, kieu, dich, rng):
    """Bản sao một ca trong repo giả `dich` với dữ liệu hoán vị. Trả allowlist giả."""
    f = chung.selector.chon_ca(al, oid, chung.ROOT)
    case = dich / 'data' / 'rcaeval' / oid
    case.mkdir(parents=True)
    files = {}
    for name, p in f.items():
        df = pd.read_parquet(p)
        if kieu == 'cot' and name == 'metrics.parquet':
            cols = [c for c in df.columns if c != 'time']
            df = df[['time'] + [cols[i] for i in rng.permutation(len(cols))]]
        if kieu == 'dong' and name in ('traces.parquet', 'logs.parquet'):
            df = df.iloc[rng.permutation(len(df))].reset_index(drop=True)
        q = case / name
        df.to_parquet(q, index=False)
        files[name] = {'path': f'data/rcaeval/{oid}/{name}', 'bytes': q.stat().st_size, 'sha256': chung.sha256_file(q)}
    doc = {'so_ca': 1, 'cases': [{'opaque_id': oid, 'case_dir': f'data/rcaeval/{oid}', 'files': files}]}
    (dich / 'allowlist.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    return chung.selector.nap_allowlist(dich / 'allowlist.json'), files


def main(**kw):
    al, moc = chung.nap()
    pilot = nap(kw['ca_pilot'])['chon']
    model, tmeth = kw['circa_model'], kw.get('torai_method')  # TORAI tùy chọn: chưa khóa thì bỏ qua
    L = chung.Luot('kiem-ca-that', {'nguon': kw, 'mo_gia_giay_tu_dau_file': TP})
    out = {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'nguon': kw}
    ck = ck_mod()

    # 1. §11.6
    k6 = {}
    for m in [x for x in ('baro', 'torai') if x in kw]:
        rows = nap(kw[m])['luot']
        k6[m] = {'so_luot': len(rows), 'key_check_pass': sum(all(b.get('key_check') == 'pass' for b in (r.get('bien_the') or {}).values()
                                                                 if b['status'] == 'OK') for r in rows),
                 'loi_runner': sum('loi_runner' in r for r in rows)}
    tr_rows = nap(kw['tracerca'])['luot']
    k6['tracerca_ji'] = {}
    for r in tr_rows:
        oid = r['opaque_id']
        f = chung.selector.chon_ca(al, oid, chung.ROOT, tep=['traces.parquet'])
        win = cua_so.cat_span(pd.read_parquet(f['traces.parquet'], columns=COT_CK), moc[oid])
        rec = ban_ghi(Path(kw['tracerca']).parent / 'luot' / r['run_id'])[0]
        k6['tracerca_ji'][oid] = so_ji(rec, win, moc[oid], ck)
        L.ghi(f'TraceRCA ji {oid}: {k6["tracerca_ji"][oid].get("khop")}')
    cur = {}
    for r in nap(kw['circa'])['luot']:
        oid = r['opaque_id']
        f = chung.selector.chon_ca(al, oid, chung.ROOT, tep=['metrics.parquet'])
        m = cua_so.cat_metric(pd.read_parquet(f['metrics.parquet'], columns=['time']), moc[oid])
        A = m[m['time'] >= moc[oid]]
        cur[oid] = {'current_ban_ghi': (r.get('circa') or {}).get('current'), 'max_time_A': int(A['time'].max()),
                    'khop': (r.get('circa') or {}).get('current') == int(A['time'].max())}
    k6['circa_current'] = {'so_ca': len(cur), 'so_khop': sum(x['khop'] for x in cur.values()), 'ca': cur}
    out['k_11_6'] = k6
    L.ghi(f'§11.6 xong: circa current khớp {k6["circa_current"]["so_khop"]}/{len(cur)}')

    # 2. §11.9 hai cửa sổ bình thường
    k9 = {}
    for m, method, extra, nguon in (('baro', 'baro', {}, kw['baro']), ('simplerca', 'simplerca', {}, kw['simplerca']),
                                    ('tracerca', 'tracerca', {}, kw['tracerca']),
                                    ('circa', 'circa', {'model': model, 'hashseed': 0}, kw['circa']),
                                    ('torai', tmeth, {'seed': 0}, kw.get('torai'))):
        if nguon is None:
            k9[m] = 'bỏ qua: nguồn TORAI chưa khóa'
            continue
        oid = pilot[m if m != 'torai' else tmeth]['trung_vi_duoi']['opaque_id']
        f = chung.selector.chon_ca(al, oid, chung.ROOT, tep=['metrics.parquet'])
        t0 = int(pd.read_parquet(f['metrics.parquet'], columns=['time'])['time'].min())
        tg = t0 + TP
        assert tg + 300 <= moc[oid] and 300 <= tg - t0 <= 420
        ram = chung.ram_trong_gb()
        try:
            recs = runner.chay_luot(al, oid, method, 'a', tg, L.dir / 'luot', chung.TIMEOUT_S, **extra)
            loi = None
        except Exception as exc:  # noqa: BLE001
            recs, loi = [], f'{type(exc).__name__}: {exc}'
        that = ban_ghi(run_dir_cua(nguon, oid, seed=extra.get('seed'), hashseed=extra.get('hashseed')))
        k9[m] = {'opaque_id': oid, 'moc_gia_tu_dau_file_s': TP, 'loi_runner': loi, 'ram_truoc_gb': ram,
                 'binh_thuong': tom_ban_ghi(recs), 'cua_so_that': tom_ban_ghi(that)}
        if m == 'tracerca' and recs:
            ft = chung.selector.chon_ca(al, oid, chung.ROOT, tep=['traces.parquet'])
            win = cua_so.cat_span(pd.read_parquet(ft['traces.parquet'], columns=COT_CK), tg)
            k9[m]['ji_doc_lap'] = so_ji(recs[0], win, tg, ck)
        L.ghi(f'§11.9 {m} {oid}: {[(v, x["status"], x["khoa_max"]) for v, x in k9[m]["binh_thuong"].items()]} loi={loi}')
    out['k_11_9'] = k9

    # 3. §11.10 hoán vị
    k10 = {}
    rng = np.random.default_rng(20261006)
    for m, kieu_list, extra, nguon in (('baro', ['cot'], {}, kw['baro']), ('simplerca', ['cot', 'dong'], {}, kw['simplerca']),
                                       ('tracerca', ['dong'], {}, kw['tracerca']),
                                       ('circa', ['cot', 'dong'], {'model': model, 'hashseed': 0}, kw['circa'])):
        oid = pilot[m]['trung_vi_duoi']['opaque_id']
        that = {r['variant']: r for r in ban_ghi(run_dir_cua(nguon, oid, hashseed=extra.get('hashseed')))}
        for kieu in kieu_list:
            dich = chung.OUT / 'work' / 'hoan-vi' / f'{m}-{kieu}-{oid}'
            if dich.exists():
                shutil.rmtree(dich)
            al2, man = ban_sao(al, oid, kieu, dich, rng)
            try:
                recs = runner.chay_luot(al2, oid, m, 'a', moc[oid], L.dir / 'luot', chung.TIMEOUT_S, repo_root=dich, **extra)
                loi = None
            except Exception as exc:  # noqa: BLE001
                recs, loi = [], f'{type(exc).__name__}: {exc}'
            k10[f'{m}-{kieu}'] = {'opaque_id': oid, 'loi_runner': loi, 'manifest_ban_sao': man,
                                  'so_sanh': {r['variant']: so_nhom(that[r['variant']], r) for r in recs}}
            shutil.rmtree(dich)
            L.ghi(f'§11.10 {m}-{kieu} {oid}: {k10[f"{m}-{kieu}"]["so_sanh"]} loi={loi}')
    out['k_11_10'] = k10
    out['bo_qua'] = {'microrank': 'dừng nhánh ở D6 (bước 2): không chạy cửa sổ bình thường, hoán vị, hash seed 1',
                     'torai_hoan_vi': 'không kiểm: GMM (thứ tự cột) và Drain (thứ tự dòng log cùng giây) phụ thuộc thứ tự theo thiết kế'}
    chung.ghi_json(chung.OUT / ('kiem-ca-that.json' if 'torai' in kw else 'kiem-ca-that-khong-torai.json'), out)
    chung.ghi_json(L.dir / 'kiem-ca-that.json', out)
    L.xong({'xong': True})


if __name__ == '__main__':
    main(**dict(a.split('=', 1) for a in sys.argv[1:]))
