"""Authorized short integration tests; launch detached on exp-obs, retain everything."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import tai_linux as ctl

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'linux-check'
REPORT.mkdir(exist_ok=True)


def call(args, expected=0):
    p = subprocess.run([sys.executable, str(ROOT / 'tai_linux.py'), *args],
                       capture_output=True, timeout=720)
    lines = p.stdout.decode().splitlines()
    assert len(lines) == 1, 'CLI must emit exactly one JSON line'
    result = json.loads(lines[0])
    assert p.returncode == expected and result['ok'] == (expected == 0), (args, result)
    assert not p.stderr, 'CLI stderr must be empty'
    record = {'utc': ctl.utc(), 'args': args, 'exit': p.returncode, 'output': result}
    with (REPORT / 'commands.jsonl').open('a') as f:
        f.write(json.dumps(record) + '\n')
    return result['result'] if expected == 0 else result


def analyze(tag):
    root = ROOT / 'tai-out' / tag
    state = json.loads((root / 'state.json').read_text())
    start = (root / 'start-utc.txt').read_text().strip()
    code = 'SINCE=' + repr(start) + '\nUNTIL=' + repr(state['FinishedAt']) + '\n'
    code += ctl.source('linux-support/gateway-log.py')
    (root / 'gateway.jsonl').write_bytes(ctl.ssh('app', 'python3 -', code.encode()))
    for name, args in [('analyze.py', [str(root)]), ('verify-outputs.py', [str(root)])]:
        output = ctl.run([sys.executable, str(ROOT / 'linux-support' / name), *args],
                         timeout=120, label=name)
        (root / (name + '.stdout.json')).write_bytes(output)
    analysis = json.loads((root / 'analysis.json').read_text())
    checks = json.loads((root / 'verify-outputs.py.stdout.json').read_text())
    summary = {'tag': tag, 'run': json.loads((root / 'run.json').read_text()),
               'totals': analysis['totals'], 'journeys': analysis['journeys'],
               'mixMeasuredPercent': analysis['mixMeasuredPercent'],
               'gateway': {k: analysis['gateway'][k] for k in ('total', 'routeIds', 'matchedRoutes', 'missing', 'mismatches')},
               'outsideWorkload': len(analysis['gateway']['extraRequests']), 'checks': checks}
    (REPORT / (tag + '.json')).write_text(json.dumps(summary, indent=2) + '\n')
    return summary


try:
    preflight = call(['test-duong'])
    (REPORT / 'preflight.json').write_text(json.dumps(preflight, indent=2) + '\n')
    call(['start', '--tag', '../bad'], expected=1)
    call(['start', '--tag', 'invalid-step', '--seconds', '90', '--buoc-tai', '90'], expected=1)
    # Explicit nonexistent tag proves stop is harmless to unrelated workloads.
    call(['stop', '--tag', 'linux-no-such-container'])
    results = []
    for tag, seconds, step in [('l1linux20261113a', 150, 0), ('l1linux20261113b', 180, 90)]:
        args = ['start', '--tag', tag, '--seconds', str(seconds)]
        if step:
            args += ['--buoc-tai', str(step), '--multiplier', '3']
        launch = call(args)
        (REPORT / (tag + '-start.json')).write_text(json.dumps(launch, indent=2) + '\n')
        call(['test-duong'], expected=1)
        call(['start', '--tag', tag + '-busy', '--seconds', '1'], expected=1)
        call(['receive', '--tag', tag], expected=1)
        deadline = time.monotonic() + seconds + 150
        while True:
            state = call(['get', '--tag', tag])['state']
            if not state['Running']:
                break
            if time.monotonic() > deadline:
                raise RuntimeError('Test timed out; container retained, do not stop another workload')
            time.sleep(10)
        first = call(['receive', '--tag', tag])
        second = call(['receive', '--tag', tag])
        assert first['outputsManifestSha256'] == second['outputsManifestSha256'], 'receive must be idempotent'
        call(['start', '--tag', tag, '--seconds', str(seconds)], expected=1)
        results.append(analyze(tag))
    (REPORT / 'result.json').write_text(json.dumps({'ok': True, 'utc': ctl.utc(), 'runs': results}, indent=2) + '\n')
except Exception as exc:
    # No raw subprocess output or exception text can contain credentials here.
    (REPORT / 'error.json').write_text(json.dumps({'ok': False, 'utc': ctl.utc(), 'errorType': type(exc).__name__}) + '\n')
    raise SystemExit(1) from None
