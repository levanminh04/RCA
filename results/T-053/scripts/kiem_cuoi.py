"""Kiểm toàn vẹn nguồn cũ, hồ sơ và phạm vi T-053 trước đóng manifest."""
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'results/T-053'


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    counts = {}
    checks = {}
    for task in ('T-047','T-048'):
        manifest = read(ROOT / f'results/{task}/manifest.json')
        tables = {k:manifest[k] for k in ('outputs','closed_outputs','current_tools') if k in manifest}
        tables['source_sha256'] = {k:dict(sha256=v) for k,v in manifest['source_sha256'].items()}
        for category, table in tables.items():
            for name, expected in table.items():
                path = ROOT / name
                assert path.is_file(), name
                assert sha(path) == expected['sha256'], name
                if 'bytes' in expected:
                    assert path.stat().st_size == expected['bytes'], name
            counts[task+'/'+category] = len(table)
            print(task+'/'+category, len(table), 'PASS', flush=True)
    plan = read(BASE / 'ke-hoach-pha1.json')
    assert all(sha(ROOT / name) == expected for name,expected in plan['sources'].items())
    checks['phase1_sources_unchanged'] = len(plan['sources'])
    compiled = []
    for path in sorted((BASE / 'scripts').glob('*.py')):
        ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        compiled.append(path.relative_to(ROOT).as_posix())
    checks['python_syntax'] = compiled
    for name in ('t1-kiem-001.json','doi-chieu-pilot-001.json','doi-chieu-cache-001.json','kiem-k-day-du-001.json','kiem-pha2-doc-lap-001.json'):
        doc=read(BASE/'runs'/name)
        assert doc.get('PASS',doc.get('pass',False)), name
    checks['required_audits_PASS'] = True
    report = (BASE / 'bao-cao.md').read_text(encoding='utf8')
    links = re.findall(r'\]\(([^)]+)\)', report)
    for link in links:
        assert link in ('manifest.json', 'runs/kiem-cuoi-001.json') or (BASE/link).is_file(), link
    checks['report_links'] = len(links)
    assert 'chờ phản biện' in next(line for line in (ROOT/'docs/STATE.md').read_text(encoding='utf8').splitlines() if '**T-053' in line)
    checks['state_pending_review'] = True
    testlog=(BASE/'runs/kiem-helper-hoi-quy-001.stdout.log').read_bytes()
    testtext=testlog.decode('utf-16') if testlog.startswith(b'\xff\xfe') else testlog.decode('utf8')
    assert '107 passed' in testtext
    checks['selector_regressions'] = '107 passed'
    summary=read(BASE/'tong-hop.json')
    assert summary['checks']['paired_analysis_reproduced_semantically']
    assert summary['observation']['records']==1312
    checks['summary'] = True
    local = subprocess.check_output(['powershell','-NoProfile','-Command',
        'Get-CimInstance Win32_Process | Where-Object { $_.Name -match "python" -and $_.CommandLine -match "RCA-flashticket.*T-053.*(pha1|dieu_phoi|chay_chinh)" } | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress'],text=True)
    assert not local.strip(), local
    checks['local_method_workers_finished'] = True
    remote_code = "import pathlib,os,json;me=os.getpid();rows=[];" + chr(10) + \
        "for p in pathlib.Path('/proc').glob('[0-9]*/cmdline'):" + chr(10) + \
        " try:" + chr(10) + \
        "  c=p.read_bytes().replace(bytes([0]),b' ').decode(errors='replace');pid=int(p.parent.name)" + chr(10) + \
        "  if pid!=me and 'python' in c.split(' ')[0] and 'T-053/scripts/' in c: rows.append(dict(pid=pid,command=c))" + chr(10) + \
        " except (OSError,ValueError):pass" + chr(10) + "print(json.dumps(rows))"
    ssh=['ssh','-i','D:/RCA-ext/keys/key2.pem','-o','HostKeyAlias=3.26.62.217','-o','StrictHostKeyChecking=yes',
         '-o','BatchMode=yes','-o','ServerAliveInterval=30','-o','ServerAliveCountMax=3','ubuntu@3.107.156.186','python3 -B -']
    remote = subprocess.check_output(ssh,input=remote_code.encode())
    assert json.loads(remote)==[], remote
    checks['remote_task_workers_finished'] = True
    t=time.time()
    started=datetime.fromisoformat(read(BASE/'runs/preflight-001.json')['started_at_utc']).timestamp()
    task_hours=(t-started)/3600
    assert task_hours < 8
    doc=dict(PASS=True, generated_utc=datetime.now(timezone.utc).isoformat(), protected_counts=counts,
        checks=checks, current_SPEC=dict(path='tasks/T-053-kiem-z-chay-lai-k/SPEC.md',
            sha256=sha(ROOT/'tasks/T-053-kiem-z-chay-lai-k/SPEC.md')),
        disk_free_bytes=shutil.disk_usage(ROOT).free,
        budget=dict(start='preflight started_at_utc', hours_to_closure=task_hours,
            authorized_cap_hours=8, compute_usd_per_hour=0.1197,
            upper_bound_task_period_usd=task_hours*0.1197,
            scope='thời gian từ preflight tới đóng hồ sơ, không phải hóa đơn; instance đã chạy trước task; chưa gồm lưu trữ/IP'),
        git_tracked_modified=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines(),
        note='Giữ thay đổi có trước phiên; mutation của T-053 chỉ results/T-053, LOG và đúng dòng STATE. Không commit/push.')
    path=BASE/'runs/kiem-cuoi-001.json'
    with path.open('x',encoding='utf8') as stream:
        json.dump(doc,stream,ensure_ascii=False,indent=2)
    print(json.dumps(dict(PASS=True,protected_counts=counts,hours=task_hours)))


if __name__=='__main__':
    main()
