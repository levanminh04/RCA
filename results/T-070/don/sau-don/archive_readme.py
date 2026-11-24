# Viết /srv/flashticket-rca/archive/2026-11/README.md trên một máy (chạy bằng root). Không đọc nội dung file.
import os, subprocess, sys, time
MAY = sys.argv[1]
A = '/srv/flashticket-rca/archive/2026-11'
NGAY = '24/11/2026'
MO_TA = {
 'obs': {
  'm1': ('/srv/rca-lab/m1/t069-phan-tich', 'Phân tích của T-069 (root:rca 750)'),
  'rca-results': ('/srv/rca-lab/rca-results (trừ t065-l11-001)', 'Các bộ dữ liệu hiển thị cũ: t065-l3/l4/l8/l8b-001, t073-dev-001, t073-e5-001, JSON gốc, chi-muc, mau, phat-lai'),
  'runs': ('/srv/rca-lab/runs/*', 'Nhật ký các lượt chạy cũ (T-068…T-073, e2e-001, tempo-do-t066) và bộ nhận cảnh báo E3 (t072-e3-01*). ubuntu 700: có tên ô'),
  'load-tai-out': ('/srv/rca-lab/load-controller/tai-out', 'Bản k6 thô nhận về exp-obs (47 tag); repo RCA có bản tóm tắt'),
  'trace-goi': ('/srv/rca-lab/trace-goi', 'Gói trace ca lịch sử cho service_graph.py --goi'),
  'venv-m1': ('/srv/rca-lab/venv-m1', 'Venv V082 cũ; venv mới ở /srv/flashticket-rca/rca/venv (pip freeze trùng)'),
  'rca-results-chep-2026-11-17.sha256': ('/srv/rca-lab/rca-results-chep-2026-11-17.sha256', 'Danh sách hash khi chép rca-results 17/11'),
  'home': ('/home/ubuntu/t063', 'File lẻ của T-063'),
  'ledger': ('/srv/rca-lab/ledger/{e2e-001,t069-*,t073-e5-01}.jsonl', 'Sổ tiêm lỗi của các lượt cũ (nhãn). ledger:ledger 700; user rca không đọc được'),
 },
 'app': {
  'backups': ('/srv/rca-lab/backups', 'Bản sao lưu đích hoàn tác T-067 (t067-20261118)'),
  'build': ('/opt/flash-ticket-build/t067-36a3725d-logs; deploy-don-2026-11.tsv', 'Log build bản 36a3725d; tiến độ triển khai lúc dọn'),
  'compose-t067': ('/opt/flash-ticket-build/t067-compose', 'Bộ Compose hiệu lực T-067 (đường cũ); cấu hình đang chạy ở /opt/flashticket/compose'),
  'flash-ticket-app': ('/opt/flash-ticket-app (phần còn lại)', 'compose, compose-exp (keycloak.yml cũ, _common.yml), compose-t062, env và env-t062 cũ, collector cũ, l1-fixtures, state, file .bak'),
  'opt-docs': ('/opt/docs', 'Nguồn bind MongoDB cũ (thư mục rỗng schema.cjs)'),
  'home': ('/home/ubuntu/{t058,t062,t063,t071,inj*.py,*-t062.*}', 'Script và log của T-058…T-071 (t071/db-moc: mốc PostgreSQL T-071)'),
 },
 'tai': {
  'load-runs': ('/srv/rca-lab/load-runs', 'Bản k6 thô trên máy tải (47 tag)'),
  'home': ('/home/ubuntu/{x86-check,uvenv,arm-check*.tgz,rec-x86linux.json,dump_rec.py}', 'Thử kiến trúc máy tải ngày 10/11'),
 },
}[MAY]
dong = []
for ten in sorted(os.listdir(A)):
    if ten == 'README.md':
        continue
    du = subprocess.run(['du', '-sh', os.path.join(A, ten)], capture_output=True, text=True).stdout.split()[0]
    cu, nd = MO_TA.get(ten, ('?', 'CHƯA MÔ TẢ'))
    dong.append(f'| `{ten}` | `{cu}` | {nd} | {du} | {NGAY} |')
txt = f'''# Lưu trữ đợt dọn 11/2026 ({MAY})

Những gì không còn dùng ở đường chạy sau đợt dọn ngày {NGAY}. Tên bên trong giữ nguyên tên cũ (mã task) để khớp hồ sơ ở repo RCA.
Không xóa khi Minh chưa duyệt. Kế hoạch: repo RCA `results/T-070/don/KE-HOACH-DON.md`; bảng tra tên: repo lab `docs/name-map.md`.

| Mục | Đường cũ | Nội dung | Dung lượng | Ngày dời |
|---|---|---|---|---|
''' + '\n'.join(dong) + f'\n\nViết lúc {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}.\n'
open(os.path.join(A, 'README.md'), 'w', encoding='utf-8').write(txt)
os.chmod(os.path.join(A, 'README.md'), 0o644)
print(txt)
