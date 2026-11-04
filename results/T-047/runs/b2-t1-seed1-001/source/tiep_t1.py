"""Tiếp T1 tuần tự sau seed0 đang chạy; ba worker, không đọc nhãn."""
import json
import os
import sys
import time
from types import SimpleNamespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).parent))


def main():
    out = ROOT/'results/T-047/runs/t1-tiep-001'
    out.mkdir(exist_ok=False)
    prev = ROOT/'results/T-047/runs/b2-t1-seed0-001/result.json'
    while not prev.exists():
        time.sleep(2)
    r = json.loads(prev.read_text(encoding='utf-8'))
    if r['failed'] or r['done'] != 52:
        raise SystemExit('STOP: seed0 chưa đạt')
    import chay_t047_v2 as driver
    import du_bao_t047
    import tep_pha1
    tep_pha1.kiem(prev.parent)
    stages = [('seed1',1,None,False), ('seed2',2,None,False), ('xao0',0,0,False), ('ce',0,None,True)]
    with (out/'progress.jsonl').open('x', encoding='utf-8') as pf:
        for name, seed, shuffle, fake in stages:
            forecast = du_bao_t047.tinh(3)
            driver.emit(pf, event='forecast', stage=name, **forecast)
            if forecast['stop']:
                driver.ad.ghi(out/'result.json', dict(STOP='projection_over_cap', forecast=forecast))
                raise SystemExit('STOP dự báo vượt trần')
            os.environ['PYTHONHASHSEED'] = str(seed)
            path = ROOT/f'results/T-047/runs/b2-t1-{name}-001'
            args = SimpleNamespace(run=str(path), dataset='all', stage='full', group='T1',
                                   workers=3, fake=fake, shuffle=shuffle)
            driver.emit(pf, event='start_stage', stage=name, seed=seed, workers=3)
            driver.control(args)
            with (ROOT/'tasks/T-047-khoi-k-luot-2/LOG.md').open('a', encoding='utf-8') as log:
                log.write(f'\n- Tiến độ Phiên 5 {driver.now()}: xong T1 {name}; đầu ra {path.relative_to(ROOT).as_posix()}/result.json; chưa đọc nhãn chấm.\n')
            driver.emit(pf, event='done_stage', stage=name)
        import t1_t047
        t1_t047.main()
        driver.ad.ghi(out/'result.json', dict(PASS=True, T1='results/T-047/t1.json', time=driver.now()))


if __name__ == '__main__':
    main()
