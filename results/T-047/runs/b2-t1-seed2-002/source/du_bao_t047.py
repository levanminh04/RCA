"""Dự báo vận hành CHƯA KIỂM; không phải bằng chứng RCA hoặc đảm bảo thời gian."""
import json
import time
from pathlib import Path
import adapter_t047 as ad


def tinh(workers=3):
    b = json.loads((ad.OUT/'runs/ngan-sach.json').read_text(encoding='utf-8'))
    used = b['prior_seconds']+time.time()-b['start_epoch']
    ref = {}
    for p in (ad.ROOT/'results/T-046/runs/b10-kiem-src-001/ca').glob('*.json'):
        x = json.loads(p.read_text(encoding='utf-8'))
        ref[p.stem] = x
    observed, base_time, completed_cpu, done = 0., 0., 0., 0
    for p in (ad.OUT/'runs').glob('b2-t1-*/cases/*/summary.json'):
        s = json.loads(p.read_text(encoding='utf-8'))
        mode = 'ce' if s['fake'] else 'that'
        observed += s['phase_seconds']
        base_time += ref[s['oid']]['cua_so'][mode+'|R0']['giay']
        completed_cpu += s['seconds']+4
        done += 1
    ratio = observed/base_time if base_time else 1.
    true = sum(x['cua_so']['that|R0']['giay'] for x in ref.values())
    ce = sum(x['cua_so']['ce|R0']['giay'] for x in ref.values() if x['dataset']=='RE2-TT')
    t1_cpu = ratio*(4*true+ce)+238*7
    previous = json.loads((ad.OUT/'runs/b1-pilot-001/kiem-pilot.json').read_text(encoding='utf-8'))
    old_K = sum(x['sum_seconds'] for x in previous['old_K_runtime'].values())
    K_cpu = old_K+3*ratio*(true+ce)+82*7
    K_done = sum(json.loads(p.read_text(encoding='utf-8'))['seconds']+4
                 for p in (ad.OUT/'runs').glob('b3-k-*/cases/*/summary.json'))
    if K_done:
        # K thật được đo phải thay mô hình trước khi phát thêm việc; root đối chiếu theo ca.
        pass
    remaining = max(0,t1_cpu-completed_cpu)/workers + max(0,K_cpu-K_done)/workers + 1800
    return dict(status='CHUA_KIEM', workers=workers, used_seconds=used, completed_T1=done,
                ratio_new_to_T046=ratio, remaining_seconds=remaining, total_seconds=used+remaining,
                cap_seconds=b['cap_seconds'], stop=used+remaining>b['cap_seconds'],
                assumptions=['T1 theo tỷ số thời gian pha1 cùng ca với T-046; K bằng thời gian K cũ cộng 3 lần R0 mới.',
                             'Dự báo K phải cập nhật theo K thực, mô hình không thay phép đo cache; còn 30 phút hậu xử lý.'])


if __name__ == '__main__':
    print(json.dumps(tinh(), ensure_ascii=False, indent=1))
