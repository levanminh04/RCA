"""Phần độc lập C-a: kiểm/chấm lại baseline và KB đã seal, không chạy phương pháp."""
import time
from collections import Counter
from fractions import Fraction

from common import ROOT, RUN, digest, dump, pin, read, save, timing
from m1_danh_gia import pha2
from p3 import danh_gia
from thong_ke import counts, e04, sign_exact, mcnemar, certain

BASE = 'K-E1+E2+E5'
BASELINES = ('baro', 'simplerca', 'microrank_full', 'tracerca', 'circa_ols_da', 'torai_B')
VARIANTS = {BASE: 'M1', 'K-E2+E5': 'bo-E1', 'K-E1+E5': 'bo-E2', 'K-E1+E2': 'bo-E5'}
FIELDS = tuple(danh_gia.DO_DO_BOOT)


def exact_score(rec, root):
    ok = rec['status'] == 'OK'
    blocks = danh_gia.khoi_tu_ban_ghi(rec)
    dist = danh_gia.phan_bo_hang(blocks, root) if ok else {}
    values = danh_gia.do_ca(dist, ok)
    return dict(values, status=rec['status'], RR=sum((p / r for r, p in dist.items()), Fraction(0)),
                Hit5_Q=sum((p for r, p in dist.items() if r <= 5), Fraction(0)))


def main():
    start = time.perf_counter()
    m52 = read('results/T-052/manifest.json')
    source_paths = ('results/T-024/cham-a.json', 'results/T-026/cham-a.json',
                    'results/T-051/kb-002/score/scores.json', 'results/T-051/kb-002/score/metrics.json')
    for q in source_paths:
        pin(q, next(r for r in m52['upstream_inputs_verified'] if r['path'] == q))
    source24, source26 = [read(q) for q in source_paths[:2]]
    kb = pha2.giai_ma_json(read(source_paths[2]))['cau_hinh']
    baseline, labels, checks = {}, {}, []
    for ds, methods in [('RE2-TT', source24['methods']), ('Nezha-OB', source26['tables']['main']['methods'])]:
        baseline[ds] = {}
        for name in BASELINES:
            method = methods[name]
            by_case = {}
            for src in method['source_records']:
                path = src['path']
                pin(path, src)
                rec = read(path)
                oid = src['opaque_id']
                label = method['per_case'][oid]['label']
                assert oid in kb[BASE]['ca'] and kb[BASE]['ca'][oid]['dataset'] == ds
                labels[oid] = dict(label, dataset=ds)
                score = exact_score(rec, label['root'])
                by_case.setdefault(oid, []).append(score)
                checks.append({'path': path, 'sha256': src['sha256'], 'status': rec['status'],
                               'method': name, 'opaque_id': oid})
            assert set(by_case) == set(method['per_case'])
            rows = {}
            for oid, seeds in by_case.items():
                expected = method['per_case'][oid]
                values = {k: sum(r[k] for r in seeds) / len(seeds) for k in FIELDS}
                for k in FIELDS:
                    assert abs(values[k] - expected[k]) <= 1e-14, (ds, name, oid, k)
                rows[oid] = dict(values, RR=sum((r['RR'] for r in seeds), Fraction(0)) / len(seeds),
                                 Hit5_Q=sum((r['Hit5_Q'] for r in seeds), Fraction(0)) / len(seeds),
                                 status=expected['status'], seeds=seeds,
                                 certain_majority=sum(certain(r) for r in seeds) >= (2 if len(seeds) == 3 else 1),
                                 certain_all=all(certain(r) for r in seeds))
            baseline[ds][name] = rows
    worlds = {}
    for w in ('P', 'S_lo', 'S_hi'):
        worlds[w] = {}
        for ds, n in [('RE2-TT', 30), ('Nezha-OB', 22)]:
            table = dict(baseline[ds])
            for cid, name in VARIANTS.items():
                table[name] = {oid: dict(r['theo_the_gioi'][w]['do'], RR=r['theo_the_gioi'][w]['RR'], status=r['status'])
                               for oid, r in kb[cid]['ca'].items() if r['dataset'] == ds}
            assert all(len(rows) == n for rows in table.values())
            cells = {oid: labels[oid]['cell'] for oid in table['M1']}
            ci = danh_gia.bootstrap(table, cells)
            summary = {name: dict(n=len(rows),
                        metrics={k: sum(r[k] for r in rows.values()) / len(rows) for k in FIELDS},
                        MRR_exact=sum((r['RR'] for r in rows.values()), Fraction(0)) / len(rows),
                        statuses=Counter(r['status'] for r in rows.values())) for name, rows in table.items()}
            pairs = {}
            for name in table:
                if name == 'M1': continue
                a = {o: r['RR'] for o, r in table['M1'].items()}
                b = {o: r['RR'] for o, r in table[name].items()}
                delta = {o: a[o] - b[o] for o in a}
                pairs[name] = {'delta_RR': delta, 'mean_delta': sum(delta.values()) / n,
                               'counts': counts(delta, cells, a, b)}
            by_group = {}
            for field in ('fault', 'root', 'cell', 'nhom_vi_tri_p75'):
                by_group[field] = {}
                for g in sorted({labels[o].get(field, 'OPEN') for o in cells}):
                    chosen = [o for o in cells if labels[o].get(field, 'OPEN') == g]
                    by_group[field][g] = {name: {'n': len(chosen), 'MRR': sum((rows[o]['RR'] for o in chosen), Fraction(0)) / len(chosen)}
                                                for name, rows in table.items()}
            worlds[w][ds] = {'summary': summary, 'pairs_M1_minus': pairs, 'bootstrap': ci,
                             'by_group_historical_position': by_group,
                             'per_case': {name: {o: {k: v for k, v in r.items() if k != 'seeds'} for o, r in rows.items()} for name, rows in table.items()}}
    tt = worlds['P']['RE2-TT']
    tt_ci = dict(tt['bootstrap']['hieu']['M1 - torai_B']['rr'])
    illustration = e04(tt_ci)
    illustration.update(dev_only=True, not_P7_test_result=True, n_cases=30)
    ob = worlds['P']['Nezha-OB']['per_case']
    cells = {o: labels[o]['cell'] for o in ob['M1']}
    # Hit@5 là nhị phân/kỳ vọng hòa hữu tỉ từ seed; dùng giá trị chính xác ở baseline được kiểm.
    assert all(ob['M1'][o]['hit@5'] in (0, 1) for o in cells)
    delta = {o: Fraction(ob['M1'][o]['hit@5']) - ob['simplerca'][o]['Hit5_Q'] for o in cells}
    ob_sign = sign_exact(delta, cells)
    save(ROOT / 'results/T-052/ket-qua-dev-doc-lap-001.json', {
        'status': 'PARTIAL_NO_CA_PARITY', 'worlds': worlds, 'labels': labels,
        'baseline_native_checks': checks, 'A4_dev_illustration': illustration,
        'OB_sign_dev_illustration': ob_sign,
        'limits': ['C-a chưa qua pilot đủ miền; không có bảng C-a mới.',
                   'Nhóm vị trí ở đây là nguồn lịch sử; chưa thay nhóm N mới.',
                   'Chấm lại đầu ra đã có, không chạy lại phương pháp hoặc mở test.',
                   'M4 Nezha giữ giới hạn tái lập Q-192; không xác nhận hơn bản tác giả.']})
    save(RUN / 'bang-doc-lap-summary.json', timing('independent_baseline_table', start, PASS=True,
          native_records_checked=len(checks), datasets={'RE2-TT': 30, 'Nezha-OB': 22},
          baseline_count=6, worlds=['P','S_lo','S_hi'], bootstrap_B=10000, seed=20261005))


if __name__ == '__main__':
    main()
