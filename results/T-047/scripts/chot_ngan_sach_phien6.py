"""Chốt sau mọi kiểm/báo cáo: không reset thời gian đã dùng, không tự nới trần."""
import json
import time
from pathlib import Path

import psutil
import adapter_t047 as ad
from kiem_phien6 import sha


def main():
    out, root = ad.OUT, ad.ROOT
    audit = out / 'runs/chot-phien6-001'
    if audit.exists():
        raise FileExistsError('không chốt lại hoặc reset khoảng chờ đã có')
    manifest_path = out / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 'T047-Q233-manifest-v1':
        raise ValueError('chưa có manifest Phiên6 đã kiểm')
    active = []
    for p in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmd = p.info['cmdline'] or []
            if '--worker' in cmd and any('chay_t047_v3.py' in s for s in cmd):
                active.append(p.pid)
        except psutil.Error:
            pass
    if active:
        raise ValueError('vẫn còn worker, không ghi khoảng chờ Minh')
    budget_path = out / 'runs/ngan-sach.json'
    before = budget_path.read_bytes()
    budget = json.loads(before)
    if budget.get('waiting_for_Minh_since_epoch'):
        raise ValueError('đã có mốc chờ; không ghi đè hoặc trừ lại thời gian')
    stamp = time.time()
    used = budget['prior_seconds'] + stamp - budget['start_epoch']
    budget.update(waiting_for_Minh_since_epoch=stamp, used_seconds_when_waiting=used,
                  remaining_seconds_at_stop=budget['cap_seconds']-used,
                  resume_note='Giữ toàn bộ thời gian đã dùng. Khi tiếp tục, mang used_seconds_when_waiting vào phần đã dùng và lưu vết đổi mốc để chỉ loại đúng khoảng chờ Minh; không reset phần đã dùng hoặc tự nới cap.')
    audit.mkdir(exist_ok=False)
    (audit / 'budget-before.json').write_bytes(before)
    ad.ghi(budget_path, budget)
    check_path = root / manifest['integrity_check']
    checks = json.loads(check_path.read_text(encoding='utf-8'))
    checks['budget_used_seconds'] = used
    checks['checks']['within_total_8_hours'] = budget['cap_seconds'] == 28800 and used <= budget['cap_seconds']
    checks['integrity_PASS'] = all(checks['checks'].values())
    ad.ghi(check_path, checks)
    result = dict(status=manifest['status'], used_seconds=used, cap_seconds=budget['cap_seconds'],
                  remaining_seconds=budget['cap_seconds']-used,
                  no_method_workers=True, prior_seconds_carried=budget['prior_seconds'],
                  integrity_PASS=checks['integrity_PASS'], waiting_for_Minh_since_epoch=stamp,
                  note='Mốc chờ sau mọi công việc/kiểm được phép; không gọi task đạt chỉ từ manifest.')
    ad.ghi(audit / 'result.json', result)
    for p in (budget_path, check_path, audit / 'budget-before.json', audit / 'result.json'):
        manifest['outputs'][p.relative_to(root).as_posix()] = dict(bytes=p.stat().st_size, sha256=sha(p))
    manifest['budget_at_handoff'] = result
    ad.ghi(manifest_path, manifest)
    with (root / 'tasks/T-047-khoi-k-luot-2/LOG.md').open('a', encoding='utf-8') as f:
        f.write(f'\nChốt ngân sách Phiên6: dùng {used/60:.2f} phút của trần {budget["cap_seconds"]/60:.0f} phút, '
                f'còn {(budget["cap_seconds"]-used)/60:.2f} phút; giữ mọi phần trước. Receipt tại runs/chot-phien6-001/result.json. '
                'Không còn worker phương pháp; bắt đầu chờ Minh/chuyển phản biện. Lệnh cuối: Python ghim -B '
                'results/T-047/scripts/chot_ngan_sach_phien6.py. Không commit thêm hoặc push.\n')
    print(json.dumps(dict(status=result['status'], used_minutes=used/60,
                          remaining_minutes=(budget['cap_seconds']-used)/60,
                          integrity_PASS=checks['integrity_PASS'])))
    if not checks['integrity_PASS']:
        raise SystemExit('bàn giao ghi đúng lỗi còn lại; không gọi integrity_PASS')


if __name__ == '__main__':
    main()
