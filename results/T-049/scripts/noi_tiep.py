"""Theo dõi K-b, đóng pha, chấm và chỉ chuyển sang T6 khi luật cho phép."""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from chuan_bi import OUT, ROOT, read
from chay_khoi import t6_branch

LOG = ROOT / 'tasks/T-049-k-b-va-t6/LOG.md'
SCRIPTS = OUT / 'scripts'


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')


def log(text):
    with LOG.open('a', encoding='utf-8') as stream:
        stream.write(text)


def call(name, *args, capture=False):
    command = [sys.executable, '-B', str(SCRIPTS / name), *map(str, args)]
    print(json.dumps({'time': now(), 'command': command}, ensure_ascii=False), flush=True)
    return subprocess.run(command, cwd=ROOT, check=True, text=True, encoding='utf-8',
                          stdout=subprocess.PIPE if capture else None).stdout


def wait_kb(prefix):
    file = OUT / 'runs' / f'{prefix}-controller.jsonl'
    while True:
        if file.exists():
            lines = file.read_text(encoding='utf-8').splitlines()
            if lines:
                try:
                    last = json.loads(lines[-1])
                except json.JSONDecodeError:
                    time.sleep(10)
                    continue
                if last['event'] == 'error':
                    raise ValueError(f'K-b dừng khi chạy cửa sổ: {last}')
                if last['event'] == 'complete':
                    return
        time.sleep(10)


def evaluate(prefix, allocation, *, after=None):
    args = ('--t6-after', after) if after else ()
    pin = call('dong_pha1.py', allocation, prefix, *args, capture=True).strip()
    assert pin.startswith('- `results/T-049/runs/')
    seal = OUT / 'runs' / f'{prefix}-seal.json'
    log(f'\n### Đóng pha 1 {prefix} — {now()}\n\n{pin}\n')
    scoring = f'{prefix}-cham'
    call('cham.py', seal, scoring)
    path = OUT / 'runs' / scoring
    call('co_che.py', seal, path)
    outcome = read(path / 'ket-cuc.json')
    actions = {cid: value['hanh_dong'] for cid, value in outcome.items()}
    log(f'\n- {prefix}: đã chấm, tính độ bền và phát lại dấu vết. Kết cục tại '
        f'results/T-049/runs/{scoring}/ket-cuc.json. Hành động {actions}.\n')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('allocation', type=Path)
    parser.add_argument('kb')
    parser.add_argument('t6')
    args = parser.parse_args()
    assert os.environ.get('PYTHONIOENCODING') == 'utf-8'
    wait_kb(args.kb)
    kb = evaluate(args.kb, args.allocation)
    outcome = read(kb / 'ket-cuc.json')['K-thang-VC']['hanh_dong']
    if outcome == 'GIU_C_CHO_MINH':
        log(f'\n- Dừng phần phụ thuộc T6 theo SPEC vì hành động K-b là {outcome}.\n')
        print('OPEN: K-b cần Minh quyết trước T6', flush=True)
        return
    branch = t6_branch(kb)
    log(f'\n- Đã nhìn kết cục K-b. Khởi động pha 1 T6 trên nền {branch} theo luật.\n')
    call('chay_khoi.py', args.allocation, args.t6, '--t6-after', kb)
    evaluate(args.t6, args.allocation, after=kb)


if __name__ == '__main__':
    main()
