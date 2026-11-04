"""Q-233: chạy lại đủ T1 bằng C1, không dùng lại bản ghi trước sửa."""
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace
import chay_t047_v3 as driver
import du_bao_t047
import tep_pha1


def main():
    root=driver.ROOT;out=driver.ad.OUT/'runs/c1-t1-dieu-phoi-001'
    out.mkdir(exist_ok=False)
    with (out/'progress.jsonl').open('x',encoding='utf-8') as pf:
        for name,seed,shuffle,fake in [('seed0',0,None,False),('seed1',1,None,False),
                                      ('seed2',2,None,False),('xao0',0,0,False),('ce',0,None,True)]:
            forecast=du_bao_t047.tinh(3);driver.emit(pf,event='forecast',stage=name,**forecast)
            if forecast['stop']:raise SystemExit('STOP dự báo vượt trần8giờ')
            os.environ['PYTHONHASHSEED']=str(seed)
            path=driver.ad.OUT/f'runs/b2-c1-t1-{name}-001'
            driver.emit(pf,event='start_stage',stage=name,seed=seed)
            driver.control(SimpleNamespace(run=str(path),dataset='all',stage='full',group='T1',
                         workers=3,fake=fake,shuffle=shuffle,reuse=None))
            tep_pha1.ghi_log([path])
            driver.emit(pf,event='done_stage',stage=name)
            with (root/'tasks/T-047-khoi-k-luot-2/LOG.md').open('a',encoding='utf-8') as log:
                log.write(f'\n- Phiên6 {driver.now()}: xong T1 C1 {name}, giữ source và command trong {path.relative_to(root).as_posix()}; hash đã ghi trước nhãn.\n')
        import t1_c1_t047
        t1_c1_t047.main()
        driver.ad.ghi(out/'result.json',dict(PASS=True,T1='results/T-047/t1.json',time=driver.now()))


if __name__=='__main__':main()
