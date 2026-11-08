"""Chẩn đoán 2: sao đúng các bước của bind_actual_process (dieu_phoi.py:212-235) nhưng ghi giá trị từng điều kiện
tại thời điểm trượt, và trạng thái tiến trình ngay sau đó. Không đọc dữ liệu."""
import json, sys, tempfile, uuid
from collections import Counter
from pathlib import Path
GOC = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(GOC / 'results/T-054/scripts'))
import psutil, dieu_phoi
EXE = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
W = 'import json,os,sys\nopen(sys.argv[1],"a").write(json.dumps({"pid":os.getpid(),"token":sys.argv[2]})+"\n")\n'
N = int(sys.argv[1]); out = []
for i in range(N):
    d = Path(tempfile.mkdtemp()); tok = uuid.uuid4().hex; (d / 'w.py').write_text(W); ph = d / 'p.jsonl'
    pr = dieu_phoi.launch(EXE, [str(d / 'w.py'), str(ph), tok], d / 'o', d / 'e')
    L = dieu_phoi.identity(pr.pid, tok); rec = None
    while pr.poll() is None and rec is None:
        if not ph.exists() or not ph.read_text().strip():
            continue
        pid = json.loads(ph.read_text().splitlines()[0])['pid']
        if pid == L['pid']:
            continue
        try:
            proc = psutil.Process(pid)
            act = dieu_phoi.identity(pid, tok)
            par = {p.pid for p in proc.parents()}
            cmd = proc.cmdline()
            cr = act['created']
            fail = {'parent_thieu': L['pid'] not in par, 'token_thieu': tok not in cmd, 'created_som': cr < L['created']}
            if any(fail.values()):
                try:
                    st = proc.status(); run = proc.is_running()
                except psutil.NoSuchProcess:
                    st, run = 'gone', False
                rec = dict(fail, parents=sorted(par), cmdline_len=len(cmd), status_sau=st, running_sau=run)
        except psutil.NoSuchProcess:
            pass
    pr.wait(); out.append(rec)
tr = [r for r in out if r]
res = {'n': N, 'n_truot': len(tr), 'dieu_kien': dict(Counter(tuple(k for k in ('parent_thieu', 'token_thieu', 'created_som') if r[k]) for r in tr).items()) if tr else {},
       'mau': tr[:8]}
res['dieu_kien'] = {'+'.join(k): v for k, v in res['dieu_kien'].items()}
(Path(__file__).parent / 'chan-doan-2.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(res, ensure_ascii=False)[:1500])
