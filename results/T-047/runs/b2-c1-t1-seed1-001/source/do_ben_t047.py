"""Bước 6: bootstrap từ pha2 đã lưu; không chạy lại M1 hoặc D2."""
import argparse
import hashlib
import json
import time
import sys
from pathlib import Path
import adapter_t047 as ad
import pha2_t047 as ev
from m1_danh_gia import pha2


def main():
    p=argparse.ArgumentParser();p.add_argument('--that',required=True);p.add_argument('--ce',required=True)
    p.add_argument('--phase2',required=True);p.add_argument('--run',required=True)
    a=p.parse_args()
    inputs={x:ad.duong_ra(getattr(a,x)) for x in ('that','ce')}
    meta=ev.verify_logged(inputs);ev.validate_design(meta);ev.verify_derived_source()
    previous=ad.duong_ra(a.phase2)
    load=lambda path:pha2.giai_ma_json(json.loads(path.read_text(encoding='utf-8')))
    main_result=load(previous/'khoi-k.json')
    if main_result['hash_pha1']!={k:v['sha256'] for k,v in meta.items()} or main_result['STOP']:
        raise ValueError('pha2 sai input hoặc đang dừng')
    d2=load(previous/'tai-lap-baseline.json')
    if not d2['dat'] or d2['tong_hop']['MRR_khop_G2']!=12:
        raise ValueError('D2 chưa hợp lệ')
    kq,ce=load(previous/'kq.json'),load(previous/'ce.json')
    ex=ev.old.nap_E_X(False)
    out=ad.duong_ra(a.run);out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic()
    ad.ghi(out/'command.json',dict(argv=sys.argv,seed=ev.BOOTSTRAP_SEED,n=ev.BOOTSTRAP_N,
            phase1=meta,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            inputs={str((previous/name).relative_to(ad.ROOT)):hashlib.sha256((previous/name).read_bytes()).hexdigest()
                    for name in ('kq.json','ce.json','khoi-k.json','tai-lap-baseline.json')}))
    with (out/'progress.jsonl').open('x',encoding='utf-8') as pf,(out/'samples.jsonl').open('x',encoding='utf-8') as sf:
        def event(**row):
            b=json.loads((ad.OUT/'runs/ngan-sach.json').read_text(encoding='utf-8'))
            used=b['prior_seconds']+time.time()-b['start_epoch']
            pf.write(json.dumps(dict(time=ev.now(),elapsed=time.monotonic()-start,budget_seconds=used,**row))+'\n');pf.flush()
            if used>=b['cap_seconds']:raise TimeoutError('tới trần tổng gói')
        def sample(row):
            sf.write(json.dumps(pha2.ma_hoa_json(row),ensure_ascii=False)+'\n');sf.flush()
        result=ev.bootstrap(kq,ce,ex,event,sample)
    result['tep_mau']=str((out/'samples.jsonl').relative_to(ad.ROOT))
    ad.ghi(out/'do-ben.json',result);ad.ghi(ad.OUT/'do-ben.json',result)
    print(json.dumps(dict(n=result['n'],counts=result['tan_suat_thang'],seconds=time.monotonic()-start)))


if __name__=='__main__':main()
