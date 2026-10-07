"""T-025 kiểm: tính lại độc lập, không dùng `src/p3/danh_gia.py`, rồi so với đầu ra evaluator TỪNG CA
(SPEC, Kiểm đúng đắn; Minh duyệt 07/10/2026 "duyệt a, b"). Viết lại ở phiên 2 (G1): bản cũ chỉ tính 2 + 2 ca.

Phạm vi: cả 30 ca, mọi bộ phát hiện (BOCPD, N-Sigma chính, N-Sigma đối chứng) và mọi biến thể ranker (BARO, CIRCA
RHT+DA, CIRCA RHT-only, TORAI B 3 seed) × 2 bộ phát hiện có lượt RCA.
- Phát hiện (§7.4): vòng lặp trên 24 cửa sổ đủ 60 điểm; cửa sổ được chấm khi chỉ số đầu ≥ chỉ số bắt đầu đánh giá;
  nhãn dương khi đầu cửa sổ ≥ t_tiêm. Báo động sai, giây bình thường được đánh giá, độ trễ, phát hiện theo ca.
  Thông báo (§7.5): dựng lại từ báo động với thời gian trơ 300 s.
- RCA: hạng root lấy từ bản ghi. Không phải TORAI: nhóm hòa = mọi phần tử `entity_ranking` có khóa bằng khóa của root.
  TORAI: liệt kê mọi hoán vị của dãy khối liền nhau cùng điểm với khối chứa root (§8.4), trong khối giữ thứ tự nhóm,
  root đều trong nhóm hòa của nó. E[Hit@k], E[RR]; TORAI trung bình 3 seed. Thành công chung = độ đo × [t̂ ≥ t_tiêm].
- CIRCA: ca có nút `rht_score` > 1e10 (WHY-36), so danh sách ca vượt.
Không khớp ở bất kỳ ca nào → ghi vào `khong_khop`, mã thoát 1.

python tinh_tay.py <ban-ghi-dua-vao-cham.json> <thư mục ra của evaluator> [nhan_tep=<tệp nhãn>]
"""
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
NHAN = ROOT / 'results/T-022/nhan-dev.json'
TRO = 300
EPS = 1e-12


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def doc_nhan(p):
    doc = json.loads(Path(p).read_text(encoding='utf-8'))
    return {c['opaque_id']: c for c in doc['cases']}


def thong_bao(alarms):
    tb = []
    for a in sorted(set(alarms)):
        if not tb or a - tb[-1] >= TRO:
            tb.append(a)
    return tb


def phat_hien(times, alarms, ti, bd):
    t0, T = times[0], len(times)
    c = {'tp': 0, 'fp': 0, 'fn': 0, 'tn': 0}
    for k in range(T // 60):
        lo = k * 60
        if lo < bd:
            continue
        a, b = t0 + lo, t0 + lo + 60
        co = any(a <= x < b for x in alarms)
        duong = a >= ti
        c['tp' if co and duong else 'fp' if co else 'fn' if duong else 'tn'] += 1
    dung = sorted(x for x in alarms if x >= ti)
    tb = thong_bao(alarms)
    return {'cua_so': c, 'bao_dong_sai': sum(1 for x in alarms if x < ti),
            'giay_binh_thuong_danh_gia': sum(1 for i in range(T) if i >= bd and times[i] < ti),
            'do_tre_s': (dung[0] - ti) if dung else None, 'phat_hien_ca': bool(dung),
            't_hat': tb[0] if tb else None, 't_hat_dung': bool(tb) and tb[0] >= ti,
            'thong_bao': {'tong': len(tb), 'truoc_tiem': sum(1 for a in tb if a < ti),
                          'sau_tiem': sum(1 for a in tb if a >= ti)}}


def phan_bo_khong_torai(rec, root):
    er = rec['entity_ranking']
    vi = [i for i, r in enumerate(er) if r['entity'] == root]
    if not vi:
        return {}
    key = [float(x) for x in er[vi[0]]['key']]
    nhom = [i for i, r in enumerate(er) if [float(x) for x in r['key']] == key]
    if nhom != list(range(nhom[0], nhom[-1] + 1)):
        raise SystemExit('nhóm hòa không liền nhau')
    g = len(nhom)
    return {i + 1: Fraction(1, g) for i in nhom}


def phan_bo_torai(rec, root):
    blocks = rec['blocks']
    jb = next((n for n, b in enumerate(blocks) if any(root in g for g in b['groups'])), None)
    if jb is None:
        return {}
    key = [float(x) for x in blocks[jb]['key']]
    lo = jb
    while lo > 0 and [float(x) for x in blocks[lo - 1]['key']] == key:
        lo -= 1
    hi = jb
    while hi + 1 < len(blocks) and [float(x) for x in blocks[hi + 1]['key']] == key:
        hi += 1
    co = lambda b: sum(len(g) for g in b['groups'])  # noqa: E731
    truoc = sum(co(b) for b in blocks[:lo])
    S = list(range(lo, hi + 1))
    if len(S) > 9:
        raise SystemExit(f'quá nhiều khối cùng điểm để liệt kê: {len(S)}')
    c_truoc, g = 0, None
    for grp in blocks[jb]['groups']:
        if root in grp:
            g = len(grp)
            break
        c_truoc += len(grp)
    perms = list(itertools.permutations(S))
    dist = {}
    for pm in perms:
        w = sum(co(blocks[n]) for n in pm[:pm.index(jb)])
        for q in range(1, g + 1):
            r = truoc + w + c_truoc + q
            dist[r] = dist.get(r, 0) + Fraction(1, len(perms) * g)
    return dist


def do_do(dist):
    if not dist:
        return {'hit@1': 0.0, 'hit@3': 0.0, 'hit@5': 0.0, 'rr': 0.0}
    out = {f'hit@{k}': float(sum(p for r, p in dist.items() if r <= k)) for k in (1, 3, 5)}
    out['rr'] = float(sum(p / r for r, p in dist.items()))
    return out


def main(ds_path, ev_dir, nhan_tep=None):
    lab = doc_nhan(nhan_tep or NHAN)
    ds = json.loads(Path(ds_path).read_text(encoding='utf-8'))['ban_ghi']
    det, rca = {}, {}
    for it in ds:
        p = ROOT / it['duong_dan']
        if sha(p) != it['sha256']:
            raise SystemExit(f'SHA-256 sai: {it["duong_dan"]}')
        r = json.loads(p.read_text(encoding='utf-8'))
        if it['loai'] == 'bo_phat_hien':
            det.setdefault(it['nhom'], {})[r['opaque_id']] = r
        else:
            key = 'torai_B' if r['method'] == 'torai' else f'{r["method"]}:{r["variant"]}'
            rca.setdefault(it['nhom'], {}).setdefault(key, {}).setdefault(r['opaque_id'], []).append(r)
    ev_dir = Path(ev_dir)
    ph = json.loads((ev_dir / 'phat-hien.json').read_text(encoding='utf-8'))['bo_phat_hien']
    cb = json.loads((ev_dir / 'cham-b.json').read_text(encoding='utf-8'))['theo_bo_phat_hien']
    ids = sorted(lab)
    khong_khop, so_so = [], 0
    res = {'phat_hien': {}, 'rca': {}}

    def so(ten, a, b):
        nonlocal so_so
        so_so += 1
        ok = (a == b) if not isinstance(a, float) else (b is not None and abs(a - b) < EPS)
        if not ok:
            khong_khop.append({'cho': ten, 'tinh_lai': a, 'evaluator': b})

    for nhom, recs in sorted(det.items()):
        tong = {'phat_hien': 0, 'bao_dong_dau_dung': 0, 'sai': 0, 'giay': 0}
        for oid in ids:
            r = recs.get(oid)
            ev = ph[nhom]['ca'][oid]
            if r is None or r['status'] != 'OK':
                so(f'{nhom} {oid} phat_hien_ca', False, ev['phat_hien_ca'])
                continue
            ti = lab[oid]['inject_time']
            t = phat_hien(r['times'], r['alarms'], ti, r['bat_dau_danh_gia'])
            for k in ('tp', 'fp', 'fn', 'tn'):
                so(f'{nhom} {oid} cua_so.{k}', t['cua_so'][k], ev['cua_so'][k])
            for k in ('bao_dong_sai', 'giay_binh_thuong_danh_gia', 'do_tre_s', 'phat_hien_ca', 't_hat', 't_hat_dung'):
                so(f'{nhom} {oid} {k}', t[k], ev[k])
            so(f'{nhom} {oid} thong_bao', t['thong_bao'], ev['thong_bao'])
            so(f'{nhom} {oid} t_hat = luot_rca', t['t_hat'], r['luot_rca']['t_hat'])
            tong['phat_hien'] += t['phat_hien_ca']
            tong['bao_dong_dau_dung'] += t['t_hat_dung']
            tong['sai'] += t['bao_dong_sai']
            tong['giay'] += t['giay_binh_thuong_danh_gia']
        agg = ph[nhom]['tong_hop']
        so(f'{nhom} tong phat_hien', tong['phat_hien'], agg['theo_ca_tren_30']['phat_hien'])
        so(f'{nhom} tong bao_dong_dau_dung', tong['bao_dong_dau_dung'], agg['theo_ca_tren_30']['bao_dong_dau_dung'])
        fa = tong['sai'] / tong['giay'] * 3600 if tong['giay'] else None
        so(f'{nhom} bao_dong_sai_moi_gio', fa, agg['co_dieu_kien_tren_ca_OK']['bao_dong_sai_moi_gio'])
        res['phat_hien'][nhom] = dict(tong, bao_dong_sai_moi_gio=fa)

    for nhom, by in sorted(rca.items()):
        for key, per in sorted(by.items()):
            ev = cb[nhom][key]
            tong = {'hit@1': 0.0, 'hit@3': 0.0, 'hit@5': 0.0}
            vuot = []
            for oid in ids:
                rs = per.get(oid, [])
                d = det[nhom].get(oid)
                th = d['luot_rca']['t_hat'] if d and d['status'] == 'OK' else None
                ti, root = lab[oid]['inject_time'], lab[oid]['root']
                if not rs:
                    so(f'{nhom} {key} {oid} co_luot_rca', False, ev['ca'][oid]['co_luot_rca'])
                    continue
                ms = []
                for r in rs:
                    if r['status'] != 'OK':
                        ms.append(do_do({}))
                    elif r.get('blocks') is not None and r['method'] == 'torai':
                        ms.append(do_do(phan_bo_torai(r, root)))
                    else:
                        ms.append(do_do(phan_bo_khong_torai(r, root)))
                m = {k: sum(x[k] for x in ms) / len(ms) for k in ms[0]}
                dung = th is not None and th >= ti
                so(f'{nhom} {key} {oid} t_hat_dung', dung, ev['ca'][oid]['t_hat_dung'])
                for k in m:
                    so(f'{nhom} {key} {oid} {k}', m[k], ev['ca'][oid][k])
                for k in tong:
                    tong[k] += m[k] if dung else 0.0
                if key.startswith('circa') and any(float(v['rht_score']) > 1e10
                                                   for v in (rs[0]['diagnostics'].get('nodes') or {}).values()):
                    vuot.append(oid)
            for k in tong:
                so(f'{nhom} {key} thanh_cong_chung_tren_30 {k}', tong[k] / len(ids), ev['tong_hop']['thanh_cong_chung_tren_30'][k])
            if key.startswith('circa'):
                so(f'{nhom} {key} ca_vuot_1e10', sorted(vuot), ev['tong_hop']['nhom_khong_vuot_1e10']['ca_vuot'])
            res['rca'][f'{key}[{nhom}]'] = {'thanh_cong_chung_tren_30': {k: v / len(ids) for k, v in tong.items()},
                                           'ca_vuot_1e10': sorted(vuot) if key.startswith('circa') else None}
    out = {'mo_ta': __doc__.strip(), 'danh_sach': str(ds_path), 'evaluator': str(ev_dir),
           'nhan': str(nhan_tep or NHAN.relative_to(ROOT).as_posix()), 'so_phep_so': so_so,
           'so_khong_khop': len(khong_khop), 'khong_khop': khong_khop, 'tinh_lai': res}
    (ev_dir / 'tinh-tay.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'so_phep_so': so_so, 'so_khong_khop': len(khong_khop), 'vi_du': khong_khop[:5]},
                     ensure_ascii=False))
    sys.exit(1 if khong_khop else 0)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], **dict(a.split('=', 1) for a in sys.argv[3:]))
