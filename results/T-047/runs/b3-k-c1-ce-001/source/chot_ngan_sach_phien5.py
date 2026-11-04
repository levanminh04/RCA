"""Chốt đúng thời điểm bắt đầu chờ Minh, không nới trần hoặc xóa thời gian đã dùng."""
import hashlib
import json
import time
from pathlib import Path
import adapter_t047 as ad


def entry(p):return dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())


def main():
    root,out=ad.ROOT,ad.OUT
    budget_path=out/'runs/ngan-sach.json'
    budget=json.loads(budget_path.read_text(encoding='utf-8'))
    epoch=time.time();used=budget['prior_seconds']+epoch-budget['start_epoch']
    budget.update(waiting_for_Minh_since_epoch=epoch,used_seconds_when_waiting=used,
                  remaining_seconds_at_stop=budget['cap_seconds']-used)
    ad.ghi(budget_path,budget)
    audit_path=out/'runs/ket-phien5-001/kiem-ban-giao.json'
    audit=json.loads(audit_path.read_text(encoding='utf-8'));audit['budget']=budget;ad.ghi(audit_path,audit)
    log=root/'tasks/T-047-khoi-k-luot-2/LOG.md'
    with log.open('a',encoding='utf-8') as f:
        f.write(f'\nChốt bàn giao: kiểm phạm vi/hash/diff/JUnit đạt (integrity_PASS), task_PASS=false vì C1. Manifest checkpoint giữ mọi lượt/candidate, chưa có K/nhãn chấm. Đã dùng {used/60:.2f} phút; còn {(budget["cap_seconds"]-used)/60:.2f} phút của trần7giờ. Bắt đầu chờ Minh; chỉ thời gian chờ này được loại theo SPEC khi có chỉ đạo tiếp, giữ nguyên phần đã dùng. Lệnh cuối thực tế: Python ghim -B results/T-047/scripts/chot_ngan_sach_phien5.py. Bước tiếp theo vẫn là duyệt phạm vi C1/ngân sách; không chạy K tự động.\n')
    manifest_path=out/'manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for p in (budget_path,audit_path,Path(__file__)):
        manifest['outputs'][p.relative_to(root).as_posix()]=entry(p)
    ad.ghi(manifest_path,manifest)
    print(json.dumps(dict(used_minutes=used/60,remaining_minutes=(budget['cap_seconds']-used)/60,
                          cap_hours=budget['cap_seconds']/3600,outputs=len(manifest['outputs']),
                          integrity_PASS=audit['integrity_PASS'],task_PASS=False)))


if __name__=='__main__':main()
