"""Chẩn đoán lỗi 'PID pha không phải worker con của launcher' (T-054 TORAI A, slot 585e37aa).
Khởi chạy worker giả qua đúng executable venv của plan, worker ghi phases.jsonl với PID thật rồi thoát nhanh;
poll dày bind_actual_process (bản đã ghim) và ghi giá trị ba điều kiện ở mỗi lần Blocked. Không đọc dữ liệu."""
import json, os, sys, time, tempfile, uuid
from pathlib import Path
GOC = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(GOC / 'results/T-054/scripts'))
import psutil
import dieu_phoi
from bien_nhan import Blocked
EXE = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
WORKER = r'''
import json, os, sys, time
p, tok = sys.argv[1], sys.argv[2]
with open(p, "a") as f:
    for i in range(3):
        f.write(json.dumps({"phase": "x", "state": "start", "pid": os.getpid(), "token": tok}) + "\n"); f.flush()
        time.sleep(float(sys.argv[3]))
'''
out = {'lan': [], 'tong': {}}
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for i in range(N):
    d = Path(tempfile.mkdtemp()); tok = uuid.uuid4().hex
    w = d / 'w.py'; w.write_text(WORKER)
    ph = d / 'phases.jsonl'
    pr = dieu_phoi.launch(EXE, [str(w), str(ph), tok, sys.argv[2] if len(sys.argv)>2 else "0.05"], d / 'o.txt', d / 'e.txt')
    launcher = dieu_phoi.identity(pr.pid, tok)
    ket = 'OK'; chi_tiet = None
    while pr.poll() is None:
        phases = [json.loads(x) for x in ph.read_text().splitlines()] if ph.exists() else []
        try:
            dieu_phoi.bind_actual_process(d, tok, launcher, phases)
        except Blocked as e:
            ids = {p['pid'] for p in phases}
            pid = next(iter(ids))
            try:
                q = psutil.Process(pid)
                chi_tiet = {'running': q.is_running(), 'status': q.status() if q.is_running() else None,
                            'parents': [p.pid for p in q.parents()], 'cmdline_has_token': tok in q.cmdline(),
                            'created_ok': q.create_time() >= launcher['created'], 'launcher_pid': launcher['pid']}
            except Exception as x:
                chi_tiet = {'sau_loi': type(x).__name__}
            ket = 'BLOCKED: ' + str(e); break
        except Exception as e:
            ket = 'EXC: ' + type(e).__name__; break
    pr.wait()
    out['lan'].append({'i': i, 'ket': ket, 'chi_tiet': chi_tiet})
from collections import Counter
out['tong'] = dict(Counter(x['ket'] for x in out['lan']))
(Path(__file__).parent / 'chan-doan.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(out['tong'], ensure_ascii=False)); print([x['chi_tiet'] for x in out['lan'] if x['chi_tiet']][:5])
