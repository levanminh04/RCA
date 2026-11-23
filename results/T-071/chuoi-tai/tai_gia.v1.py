"""tai_linux giả để thử luồng chuoi_tai (không SSH, không tải)."""
import json, os, sys, pathlib
d = pathlib.Path(os.environ['FAKE_DIR']); d.mkdir(exist_ok=True)
kb = json.loads(os.environ.get('FAKE_KB', '{}'))
cmd = sys.argv[1]; tag = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else None
with open(d / 'goi.log', 'a') as f: f.write(' '.join(sys.argv[1:]) + '\n')
b = kb.get(tag, 'ok'); st = d / (str(tag) + '.n')
def pr(o): print(json.dumps(o)); sys.exit(0 if o.get('ok') else 1)
if cmd == 'start':
    if b == 'start_loi': pr({'ok': False, 'error': 'SSH tai failed (exit 1); secret output omitted'})
    if b == 'start_chung': pr({'ok': False, 'error': 'STOP exists on exp-obs; no load/login/recovery'})
    st.write_text('0'); pr({'ok': True, 'result': {'tag': tag, 'containerId': 'c' + tag}})
if cmd == 'get':
    if not st.exists(): pr({'ok': False, 'error': 'SSH tai failed (exit 1); secret output omitted'})
    n = int(st.read_text()) + 1; st.write_text(str(n))
    pr({'ok': True, 'result': {'tag': tag, 'state': {'Running': n < 3, 'ExitCode': 1 if b == 'exit1' else 0, 'OOMKilled': False,
        'StartedAt': '2026-11-18T07:57:34.1Z', 'FinishedAt': '2026-11-18T08:57:36.2Z'}}})
if cmd == 'receive': pr({'ok': True, 'result': {'tag': tag, 'destination': '/x/' + tag, 'hashesMatched': 12, 'outputsManifestSha256': 'ab'}})
if cmd == 'stop':
    assert tag, 'stop thiếu tag!'; pr({'ok': True, 'result': {'tag': tag}})
