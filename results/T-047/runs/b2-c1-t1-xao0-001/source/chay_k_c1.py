"""Q-233: tiếp K chỉ sau T1 C1 đầy đủ và đối chiếu delta, chưa đọc nhãn chấm."""
import json
import os
import sys
from types import SimpleNamespace

import adapter_t047 as ad
import chay_t047_v3 as driver
import du_bao_t047
import giai_thich_lech_c1 as delta
import kiem_k_pha1
import tep_pha1


def main():
    t1 = json.loads((ad.OUT / 't1.json').read_text(encoding='utf-8'))
    if t1.get('PASS') is not True or len(t1.get('doi_chieu_T046', {})) != 82:
        raise ValueError('chưa có T1 C1 đầy đủ PASS')
    for mode in ('seed0', 'seed1', 'seed2', 'xao0', 'ce'):
        path = ad.OUT / f'runs/b2-c1-t1-{mode}-001'
        meta = tep_pha1.kiem(path)
        expected_n = 30 if mode == 'ce' else 52
        if meta['so_ca'] != expected_n or meta['so_ban_ghi'] != expected_n:
            raise ValueError('T1 C1 thiếu bản ghi')
    for kind, old_name, new_name in [('that', 'seed0', 'seed0'), ('ce', 'ce', 'ce')]:
        audit = ad.OUT / f'runs/c1-delta-{kind}-001'
        if not (audit / 'summary.json').is_file():
            saved = sys.argv
            try:
                sys.argv = [str(delta.__file__), '--old', f'results/T-047/runs/b2-t1-{old_name}-001',
                            '--new', f'results/T-047/runs/b2-c1-t1-{new_name}-001', '--run', str(audit)]
                delta.main()
            finally:
                sys.argv = saved
        result = json.loads((audit / 'summary.json').read_text(encoding='utf-8'))
        current = tep_pha1.kiem(ad.OUT / f'runs/b2-c1-t1-{new_name}-001')
        previous = tep_pha1.kiem(ad.OUT / f'runs/b2-t1-{old_name}-001')
        if result['new_hash'] != current['sha256'] or result['old_hash'] != previous['sha256']:
            raise ValueError('audit delta không thuộc hai lượt hiện dùng')
        if not result['PASS'] or set(result['counts']) != {'IDENTICAL'}:
            raise ValueError('delta C1 cần người làm phân xử trước K, không tự miễn lệch')
    os.environ['PYTHONHASHSEED'] = '0'
    audit = ad.OUT / 'runs/c1-k-dieu-phoi-001'
    audit.mkdir(exist_ok=False)
    with (audit / 'progress.jsonl').open('x', encoding='utf-8') as pf:
        for name, fake in [('that', False), ('ce', True)]:
            forecast = du_bao_t047.tinh(3)
            driver.emit(pf, event='forecast_before_K', stage=name, **forecast)
            if forecast['stop']:
                raise SystemExit('STOP dự báo vượt trần tổng8giờ')
            path = ad.OUT / f'runs/b3-k-c1-{name}-001'
            driver.control(SimpleNamespace(run=str(path), dataset='all', stage='full', group='K',
                                           workers=3, fake=fake, shuffle=None, reuse=None))
            tep_pha1.ghi_log([path])
            check = kiem_k_pha1.kiem(path, fake)
            driver.emit(pf, event='K_done_before_labels', stage=name, phase1=check['phase1'],
                        QT5_flag_records=len(check['QT5_can_doc']))
            with (ad.ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md').open('a', encoding='utf-8') as log:
                log.write(f'\n- Phiên6 {driver.now()}: K C1 {name} hoàn tất và đối chiếu R0/T046 đạt; '
                          f'QT5 cần đọc {len(check["QT5_can_doc"])} bản ghi. Hash đã ghi trước nhãn.\n')
    ad.ghi(audit / 'result.json', dict(phase1_complete=True, scoring_labels_read=False,
                                     next_step='đọc QT5 rồi pha2_t047.py; giữ phụ thuộc và trần tổng8giờ'))


if __name__ == '__main__':
    main()
