"""Điều phối các cửa sổ K-b đã ghim, lưu nhật ký và giữ các lượt lỗi."""
import argparse
import concurrent.futures
import json
import sys
import time
from pathlib import Path

from chuan_bi import OUT, read
from may_chay import window

KB = ('K-thang-VC', 'K-day-du-VC')


def t6_branch(scoring):
    outcome = read(scoring / 'ket-cuc.json')['K-thang-VC']['hanh_dong']
    branch = {'THAY_BANG_VC': 'VC', 'GIU_C': 'C'}.get(outcome)
    if branch is None:
        raise ValueError(f'K-b cần Minh quyết nền T6: {outcome}')
    return branch


def dispatch(jobs, stage, prefix, configs, *, flags=(), existing=()):
    skip = set(existing)
    engines = {
        'laptop': concurrent.futures.ThreadPoolExecutor(max_workers=1),
        'ec2': concurrent.futures.ThreadPoolExecutor(max_workers=2),
    }
    opened = OUT / 'runs' / f'{prefix}-controller.jsonl'
    started = time.monotonic()
    try:
        with opened.open('x', encoding='utf-8', buffering=1) as progress:
            def emit(**values):
                print(json.dumps({'elapsed': time.monotonic() - started, **values}), file=progress)

            slots = {}
            for host, indices in jobs.items():
                for idx in indices:
                    if idx in skip:
                        continue
                    run = f'{prefix}-{host}-{idx:02d}'
                    future = engines[host].submit(window, host, idx, run, configs, flags, timeout=1200)
                    slots[future] = (host, idx, run)
            emit(event='start', stage=stage, pending=len(slots), reuse=sorted(skip), allocation=jobs)
            for future in concurrent.futures.as_completed(slots):
                host, idx, run = slots[future]
                try:
                    future.result()
                except Exception as error:
                    emit(event='error', host=host, job=idx, run=run, error=repr(error))
                    for item in slots:
                        item.cancel()
                    raise
                emit(event='done', host=host, job=idx, run=run)
            emit(event='complete')
    finally:
        for executor in engines.values():
            executor.shutdown(wait=True, cancel_futures=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('allocation', type=Path)
    parser.add_argument('prefix')
    parser.add_argument('--t6-after', type=Path)
    args = parser.parse_args()
    plan = read(args.allocation)
    assigned = [i for indices in plan['jobs'].values() for i in indices]
    assert sorted(assigned) == list(range(82))
    assert plan['stage'] == 'K-b'
    if args.t6_after:
        branch = t6_branch(args.t6_after)
        dispatch(plan['jobs'], 'T6', args.prefix, (f'T6-{branch}-E3b',),
                 flags=('--t6-branch', branch))
        return
    dispatch(plan['jobs'], 'K-b', args.prefix, KB)


if __name__ == '__main__':
    main()
