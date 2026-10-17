"""Lượt hồi quy được Minh duyệt; giữ console và exit code, không ghi đè lượt cũ."""
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
command = ['D:/RCA-ext/envs/py312-pin/Scripts/python.exe', '-X', 'utf8', '-B',
           'results/T-035/scripts/run.py', 'sua-n1-001/day-du-002']
start = time.perf_counter()
with (OUT / 'full-console-002.txt').open('x', encoding='utf-8') as log:
    process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                               env=dict(os.environ, PYTHONHASHSEED='0', PYTHONUTF8='1'))
    print(json.dumps({'started_utc': datetime.now(timezone.utc).isoformat(),
                      'pid': process.pid, 'command': command}), flush=True)
    code = process.wait()
record = {'command': command, 'returncode': code, 'seconds': time.perf_counter() - start,
          'finished_utc': datetime.now(timezone.utc).isoformat()}
with (OUT / 'full-command-002.json').open('x', encoding='utf-8') as output:
    json.dump(record, output, ensure_ascii=False, indent=2)
print(json.dumps(record), flush=True)
raise SystemExit(code)
