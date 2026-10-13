"""Đo chi phí các kiểm/báo cáo T-026; không chạy phương pháp."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-026'
sys.path.insert(0, str(ROOT / 'src'))
from p3.runner import chay_tien_trinh

ACTIONS = {
    'coverage': ['results/T-026/scripts/collect_trace_coverage.py'],
    'evaluate': ['results/T-026/scripts/evaluate.py', '--confirm-frozen'],
    'report': ['results/T-026/scripts/report.py'],
    'final-verify': ['results/T-026/scripts/verify.py', '--final', '--output',
                     'results/T-026/runs/session-005/final-verification.json'],
}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=ACTIONS)
    args = ap.parse_args()
    folder = OUT / 'runs' / ('aux-' + args.action + '-001')
    folder.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    with (folder / 'invocation.json').open('x', encoding='utf-8') as f:
        json.dump({'started_at_utc': started, 'action': args.action, 'argv': ACTIONS[args.action],
                   'timeout_s': 3600, 'hashseed': 0, 'method_called': False}, f, indent=2)
    cost = chay_tien_trinh('main', ACTIONS[args.action], 3600, 0, folder)
    with (folder / 'cost.json').open('x', encoding='utf-8') as f:
        json.dump({'started_at_utc': started, 'finished_at_utc': datetime.now(timezone.utc).isoformat(),
                   **cost}, f, indent=2, allow_nan=False)
    print(json.dumps({'action': args.action, **cost}), flush=True)
    if cost['timed_out'] or cost['exit_code']:
        raise SystemExit('auxiliary failed; preserve logs in ' + str(folder))
