"""tai_linux giả để thử luồng chuoi_tai (không SSH, không tải). Hành vi theo tag ở biến FAKE_KB (JSON):
ok | start_loi | start_chung | start_loi_co_container | start_get_loi | exit1 | get_loi | treo |
cham (Running 40 lần get) | nhan_loi | thieu_moc | thieu_moc_1."""
import json, os, sys, pathlib

d = pathlib.Path(os.environ['FAKE_DIR'])
d.mkdir(parents=True, exist_ok=True)
kb = json.loads(os.environ.get('FAKE_KB', '{}'))
cmd = sys.argv[1]
tag = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else None
with open(d / 'goi.log', 'a') as f:
    f.write(' '.join(sys.argv[1:]) + '\n')
b = kb.get(tag, 'ok')
st = d / (str(tag) + '.n')


def pr(o):
    print(json.dumps(o))
    sys.exit(0 if o.get('ok') else 1)


if cmd == 'stop':
    if not tag:
        print('STOP THIEU TAG', file=sys.stderr)
        sys.exit(9)
    pr({'ok': True, 'result': {'tag': tag, 'stopped': ['c' + tag]}})
if cmd == 'start':
    if b == 'start_loi':
        pr({'ok': False, 'error': 'SSH tai failed (exit 1); secret output omitted'})
    if b == 'start_chung':
        pr({'ok': False, 'error': 'STOP exists on exp-obs; no load/login/recovery'})
    if b == 'start_get_loi':  # lỗi ở bước docker run (mutation nhiều dòng), get sau đó cũng lỗi
        pr({'ok': False, 'error': 'SSH tai set -euo pipefail\ndate -u --iso-8601=seconds > /srv/x/start-utc.txt\n'
                                  'sudo -n docker run -d --name rca-tai-' + tag + ' ...\n failed (exit 255); '
                                  'secret output omitted'})
    st.write_text('0')
    if b == 'start_loi_co_container':
        pr({'ok': False, 'error': 'SSH tai timed out; retain existing outputs'})
    pr({'ok': True, 'result': {'tag': tag, 'containerId': 'c' + tag}})
if cmd == 'get':
    if not st.exists() or b in ('get_loi', 'start_get_loi'):
        pr({'ok': False, 'error': 'SSH tai failed (exit 1); secret output omitted'})
    n = int(st.read_text()) + 1
    st.write_text(str(n))
    running = {'treo': True, 'cham': n < 40}.get(b, n < 3)
    state = {'Running': running, 'ExitCode': 1 if b == 'exit1' else 0, 'OOMKilled': False,
             'StartedAt': '2026-11-18T07:57:34.017283858Z', 'FinishedAt': '2026-11-18T08:57:36.2Z'}
    if b == 'thieu_moc' or (b == 'thieu_moc_1' and n == 3):  # thiếu mốc giờ (mãi / chỉ lần thấy dừng đầu tiên)
        del state['StartedAt'], state['FinishedAt']
    pr({'ok': True, 'result': {'tag': tag, 'state': state}})
if cmd == 'receive':
    if b == 'nhan_loi':
        pr({'ok': False, 'error': 'SCP receive (partial output retained) failed (exit 1); secret output omitted'})
    pr({'ok': True, 'result': {'tag': tag, 'destination': '/x/' + tag, 'hashesMatched': 12,
                               'outputsManifestSha256': 'ab'}})
pr({'ok': False, 'error': 'lệnh giả không hỗ trợ'})
