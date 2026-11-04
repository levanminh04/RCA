"""Nối T1 C1 sau guard; giữ 001 lỗi, dùng lại đúng hai ca C1 hợp lệ."""
import hashlib
import json
import os
from types import SimpleNamespace
import adapter_t047 as ad
import chay_t047_v3 as driver
import du_bao_t047
import tep_pha1


def main():
    os.environ['PYTHONHASHSEED'] = '0'
    source = ad.OUT / 'runs/b2-c1-t1-xao0-001'
    reused = []
    for p in sorted((source / 'cases').iterdir()):
        meta = tep_pha1.kiem(p / 'phase1')
        params = json.loads((p / 'phase1/tham-so.json').read_text(encoding='utf-8'))
        if (meta['so_ban_ghi'] != 1 or params.get('code_correction') != 'Q-233/C1'
                or params['source_sha256']['src/m1/cong.py'] != hashlib.sha256((ad.ROOT / 'src/m1/cong.py').read_bytes()).hexdigest()):
            raise ValueError('không dùng lại ca không xác nhận C1')
        reused.append(p.name)
    audit = ad.OUT / 'runs/c1-t1-tiep-guard-001'
    audit.mkdir(exist_ok=False)
    ad.ghi(audit / 'reuse-verified.json', dict(cases=reused, from_run=str(source.relative_to(ad.ROOT))))
    with (audit / 'progress.jsonl').open('x', encoding='utf-8') as pf:
        for name, fake, shuffle, reuse in [('xao0-002', False, 0, source), ('ce-001', True, None, None)]:
            forecast = du_bao_t047.tinh(3)
            driver.emit(pf, event='forecast_before_resume', stage=name, **forecast)
            if forecast['stop']:
                raise SystemExit('STOP dự báo vượt tổng8giờ')
            path = ad.OUT / ('runs/b2-c1-t1-' + name)
            driver.control(SimpleNamespace(run=str(path), dataset='all', stage='full', group='T1',
                                           workers=3, fake=fake, shuffle=shuffle, reuse=reuse))
            tep_pha1.ghi_log([path])
            driver.emit(pf, event='stage_done', stage=name)
    import t1_c1_t047
    t1_c1_t047.main()
    ad.ghi(audit / 'result.json', dict(T1_PASS=True, source='Q-233/C1', original_controller_stopped=True))


if __name__ == '__main__':
    main()
