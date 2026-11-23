# Chờ Codex hồi usage (21:54Z) rồi chạy chuỗi 6 (CX-20, ngắn, chặn E5) trước, chuỗi 5 (CX-19, CX-19b) sau.
import datetime, time, subprocess, sys, os
dich = datetime.datetime(2026,11,22,21,57,tzinfo=datetime.timezone.utc)
while datetime.datetime.now(datetime.timezone.utc) < dich: time.sleep(30)
env = dict(os.environ, PYTHONIOENCODING='utf-8')
for s in ('chay_chuoi_6.py','chay_chuoi_5.py'):
    r = subprocess.run([sys.executable,'-u','D:/RCA-flashticket/results/T-070/codex/chuoi/'+s], env=env)
    print(s, 'rc', r.returncode, flush=True)
    if r.returncode != 0: break
