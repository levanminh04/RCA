"""Chẩn đoán 3: gọi đúng dieu_phoi.bind_actual_process (đã ghim, không sửa); bọc psutil.Process trong module để ghi
giá trị parents()/cmdline()/create_time() mà hàm thật nhận ở lần Blocked. Worker giả như chẩn đoán 1."""
import json, sys, tempfile, uuid
from collections import Counter
from pathlib import Path
GOC = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(GOC / 'results/T-054/scripts'))
import psutil, dieu_phoi
from bien_nhan import Blocked
EXE = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
W = 'import json,os,sys\nf=open(sys.argv[1],"a")\nfor i in range(3):\n f.write(json.dumps({"phase":"x","pid":os.getpid(),"token":sys.argv[2]})+"\n"); f.flush()\n'
LOG = []
class P(psutil.Process):
    def parents(self):
        v = super().parents(); LOG.append(('parents', [p.pid for p in v])); return v
    def cmdline(self):
        try:
            v = super().cmdline(); LOG.append(('cmdline_len', len(v))); return v
        except Exception as e:
            LOG.append(('cmdline_exc', type(e).__name__)); raise
    def create_time(self):
        v = super().create_time(); LOG.append(('create_time', v)); return v
import psutil as _ps
_ps_Process = _ps.Process
N = int(sys.argv[1]); out = []
for i in range(N):
    d = Path(tempfile.mkdtemp()); tok = uuid.uuid4().hex; (d / 'w.py').write_text(W); ph = d / 'p.jsonl'
    pr = dieu_phoi.launch(EXE, [str(d / 'w.py'), str(ph), tok], d / 'o', d / 'e')
    L = dieu_phoi.identity(pr.pid, tok); rec = None
    _ps.Process = P
    try:
        while pr.poll() is None:
            phases = [json.loads(x) for x in ph.read_text().splitlines()] if ph.exists() else []
            LOG.clear()
            try:
                dieu_phoi.bind_actual_process(d, tok, L, phases)
            except Blocked:
                rec = {'launcher_pid': L['pid'], 'launcher_created': L['created'], 'log': list(LOG)}; break
    finally:
        _ps.Process = _ps_Process
    pr.wait(); out.append(rec)
tr = [r for r in out if r]
def loai(r):
    d = dict((k, v) for k, v in r['log'] if k != 'create_time')
    ct = [v for k, v in r['log'] if k == 'create_time']
    t = []
    if r['launcher_pid'] not in d.get('parents', []): t.append('parent_thieu')
    if d.get('cmdline_len', 1) == 0: t.append('cmdline_rong')
    if ct and min(ct) < r['launcher_created']: t.append('created_som')
    return '+'.join(t) or 'khac'
res = {'n': N, 'n_truot': len(tr), 'loai': dict(Counter(loai(r) for r in tr)), 'mau': tr[:6]}
(Path(__file__).parent / 'chan-doan-3.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(res, ensure_ascii=False)[:1800])
