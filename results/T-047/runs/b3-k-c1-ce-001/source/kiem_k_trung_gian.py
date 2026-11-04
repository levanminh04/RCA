"""Soi sớm các ca K đã xong, dùng đúng đối chiếu bước3; không chấm nhãn."""
import argparse
import copy
import hashlib
import json

import adapter_t047 as ad
import tep_pha1
from kiem_k_pha1 import b10, old_t1
from p3 import nezha


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--run', required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    run = ad.duong_ra(a.run)
    target = ad.duong_ra(a.out)
    if target.exists():
        raise FileExistsError('giữ mọi lượt kiểm')
    old_manifest = json.loads((ad.ROOT / 'results/T-046/manifest.json').read_text(encoding='utf-8'))['tep']
    universe = json.loads((ad.ROOT / 'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    results, flags = [], []
    for case in sorted((run / 'cases').iterdir()):
        if not (case / 'summary.json').is_file():
            continue
        summary = json.loads((case / 'summary.json').read_text(encoding='utf-8'))
        meta = tep_pha1.kiem(case / 'phase1')
        if meta['so_ban_ghi'] != 16:
            raise ValueError('ca chưa đủ 16 cấu hình')
        fake, oid, ds = summary['fake'], case.name, summary['dataset']
        ref_run = ad.OUT / ('runs/b2-c1-t1-ce-001' if fake else 'runs/b2-c1-t1-seed0-001') / 'cases' / oid / 'phase1'
        tep_pha1.kiem(ref_run)
        ref = json.loads((ref_run / 'records/00000.json').read_text(encoding='utf-8'))
        ref_rel = f'results/T-046/runs/b10-kiem-src-001/ca/{oid}.json'
        if hashlib.sha256((ad.ROOT / ref_rel).read_bytes()).hexdigest() != old_manifest[ref_rel]['sha256']:
            raise ValueError('hash reference T046 lệch')
        previous = json.loads((ad.ROOT / ref_rel).read_text(encoding='utf-8'))
        checks = {}
        with (case / 'phase1' / meta['tep']).open(encoding='utf-8') as f:
            for line in f:
                r = json.loads(line)
                cid = r['config_id']
                if cid == 'K-R0':
                    x, y = copy.deepcopy(r), copy.deepcopy(ref)
                    for z in (x, y):
                        z.pop('config_id'); z.pop('variant')
                    checks['R0_T1_differences'] = old_t1.truong_lech(x, y)
                if cid == 'K-E1+E2+E3+E5':
                    current, _, _ = b10.tom_tat(r, dict(aliases={}, inventory=universe if ds == 'RE2-TT' else nezha.UNIVERSE), 'K-du')
                    old = previous['cua_so'][('ce' if fake else 'that') + '|K-du']['tom_tat']
                    checks['Kdu_T046_differences'] = {k: [old.get(k), current.get(k)] for k in set(old) | set(current)
                                                       if old.get(k) != current.get(k)}
                q = old_t1.soi_ban_ghi.soi(r, False)
                fl = {k: q[k] for k in ('diem_lon_hon_1e6', 'toan_hoa', 'so_nguong_cuc_lon',
                      'cot_metric_chua_khai_nguon', 'nguon_metric_unsupported', 'coverage_unsupported') if q[k]}
                if (q.get('nhom_chiem') or 0) > .9:
                    fl['nhom_chiem'] = q['nhom_chiem']
                if fl:
                    flags.append(dict(case=oid, config_id=cid, flags=fl))
        results.append(dict(case=oid, dataset=ds, fake=fake, phase1=meta, checks=checks))
    passed = bool(results) and all(len(x['checks']) == 2 and not any(x['checks'].values()) for x in results)
    ad.ghi(target, dict(scope='PARTIAL_CHECK_COMPLETED_CASES_ONLY', computational_PASS=passed,
                        scoring_labels_read=False, cases=results, QT5_can_doc=flags,
                        limits='Không thay kiểm đủ ma trận K52/30 hoặc phân xử QT5/cơ chế.'))
    print(json.dumps(dict(checked=len(results), PASS=passed, QT5_flag_records=len(flags))))
    if not passed:
        raise SystemExit('STOP đối chiếu sớm lệch; điều tra trước khi tiếp K')


if __name__ == '__main__':
    main()
