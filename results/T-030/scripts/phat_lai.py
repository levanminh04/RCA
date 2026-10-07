"""T-030 bước 2: phát lại đầu ra đã lưu của T-017 (SimpleRCA) và T-016 (TORAI) qua evaluator P3.

Đối chiếu biết đáp án cho evaluator, không phải số P3: cấu hình cửa sổ của hai task cũ khác P3.
- T-017 run-dev-005: bảng chính (quy tắc hòa theo nhóm điểm) so với hit_fractional/mrr_fractional
  từng ca trong summary.json và số tổng ở results/T-017/kiem-dung-dan.md:53.
- T-016 s10-tt-sua-len10 (3 seed): bảng RCAEval (§8.6) so với AC@1, AC@3, Avg@5 ở
  results/T-016/cham/bang-so-cong-bo.md:15. TORAI không lưu khóa cụm nên không phát lại bảng chính.
"""
import json
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from p3 import danh_gia as dg, nhan  # noqa: E402

OUT = ROOT / 'results' / 'T-030' / 'phat-lai.json'
WORK = ROOT / 'results' / 'T-030' / 'work' / 't016'


def rec_simplerca(res):
    if res['status'] == 'abstain':
        return {'status': 'NO_EVIDENCE', 'method_status_raw': 'abstain'}
    er = []
    for i, g in enumerate(res['tie_groups']):
        for s in g['services']:
            er.append({'entity': s, 'key': [float(g['score'])], 'tie_group': i})
    return {'status': 'OK', 'entity_ranking': er, 'ranking_native': res['ranks']}


def main():
    lab = nhan.nap_nhan(ROOT / 'results/T-022/nhan-dev.json')
    raw =json.load(open(ROOT / 'results/T-022/nhan-dev.json', encoding='utf-8'))
    by_case = {c['case']: c['opaque_id'] for c in raw['cases']}

    # ---- T-017 ----
    d17 = ROOT / 'results/T-017/runs/run-dev-005'
    summ = {s['case']: s for s in json.load(open(d17 / 'summary.json', encoding='utf-8'))}
    per, lech = {}, []
    for case, oid in sorted(by_case.items()):
        res = json.load(open(d17 / f'{case}.json', encoding='utf-8'))
        root = lab[oid]['root']
        if summ[case]['root_for_evaluation'] != root:
            lech.append({'ca': oid, 'loai': 'root khác nhãn P3'})
        r = dg.cham_ca(rec_simplerca(res), root)
        per[oid] = r
        for k, key in ((1, 'top1'), (3, 'top3'), (5, 'top5')):
            want = summ[case][key]['hit_fractional']
            if abs(r[f'hit@{k}'] - want) > 1e-12:
                lech.append({'ca': oid, 'do_do': f'hit@{k}', 'p3': r[f'hit@{k}'], 't017': want})
        if abs(r['rr'] - summ[case]['top1']['mrr_fractional']) > 1e-12:
            lech.append({'ca': oid, 'do_do': 'rr', 'p3': r['rr'], 't017': summ[case]['top1']['mrr_fractional']})
    t17 = dg.tong_hop(per)
    so17 = {'hit@1': 0.833333, 'hit@3': 0.966667, 'hit@5': 0.966667, 'mrr': 0.891111}
    lech17 = {k: round(t17[k] - v, 6) for k, v in so17.items()}

    # ---- T-016 ----
    if not (WORK / 's10-tt-sua-len10').exists():
        with tarfile.open(ROOT / 'results/T-016/runs/khoi/s10-tt-sua-len10.tar.gz') as tf:
            tf.extractall(WORK)
    seeds = {}
    for seed in (0, 1, 2):
        recs = {}
        for case, oid in by_case.items():
            f = WORK / 's10-tt-sua-len10' / f'seed{seed}' / (case.replace('re2tt_', '') + '.json')
            ranks = json.load(open(f, encoding='utf-8'))['0']
            recs[oid] = {'status': 'OK', 'ranking_native': ranks}
        seeds[seed] = dg.bang_rcaeval(recs, lab)
    so16 = {'AC@1': 0.700, 'AC@3': 0.933, 'Avg@5': 0.880}
    lech16 = {s: {k: round(v[k] - so16[k], 3) for k in so16} for s, v in seeds.items()}

    doc = {
        'mo_ta': __doc__.strip(),
        'tao_luc_utc': datetime.now(timezone.utc).isoformat(),
        't017': {'ca': len(per), 'lech_tung_ca': lech, 'tong_p3': {k: t17[k] for k in so17},
                 'so_da_bao': so17, 'hieu_lam_tron_6': lech17,
                 'dat': not lech and all(abs(v) <= 1e-6 for v in lech17.values())},
        't016': {'theo_seed': seeds, 'so_da_bao': so16, 'hieu_lam_tron_3': lech16,
                 'dat': all(abs(v) < 5e-4 for d in lech16.values() for v in d.values())},
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'t017_dat': doc['t017']['dat'], 't017_lech': len(lech), 't017_tong': doc['t017']['tong_p3'],
                      't016_dat': doc['t016']['dat'], 't016': lech16}, ensure_ascii=False))


if __name__ == '__main__':
    main()
