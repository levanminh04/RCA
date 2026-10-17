"""Hồi quy đủ dev bằng code cuối, giữ mọi đầu ra và mã thoát."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
command = ['D:/RCA-ext/envs/py312-pin/Scripts/python.exe', '-X', 'utf8', '-B',
           'results/T-035/scripts/run.py', 'sua-hop-dong-001/day-du-001']
start = time.perf_counter()
with (BASE / 'full-console.txt').open('x', encoding='utf-8') as log:
    process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                               env=dict(os.environ, PYTHONHASHSEED='0', PYTHONUTF8='1'))
    print(json.dumps({'started_utc': datetime.now(timezone.utc).isoformat(),
                      'pid': process.pid, 'command': command}), flush=True)
    code = process.wait()
record = {'command': command, 'returncode': code, 'seconds': time.perf_counter() - start,
          'finished_utc': datetime.now(timezone.utc).isoformat()}
with (BASE / 'full-command.json').open('x', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False, indent=2)
print(json.dumps(record), flush=True)
raise SystemExit(code)
