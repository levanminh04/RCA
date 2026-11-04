"""Tổng hợp thời gian vận hành của các lượt chính đã đóng."""
import json
from collections import defaultdict
from datetime import datetime, timezone, timedelta

from chuan_bi import OUT, read, write


def stage(prefix):
    progress = OUT / 'runs' / f'{prefix}-controller.jsonl'
    events = [json.loads(line) for line in progress.read_bytes().splitlines()]
    assert events[-1]['event'] == 'complete'
    done = [row for row in events if row['event'] == 'done']
    assert len(done) == 82 and not any(row['event'] == 'error' for row in events)
    hosts = defaultdict(lambda: {'windows': 0, 'records': 0, 'window_wall_sum': 0, 'CPU_sum': 0,
                                 'last_done': 0, 'peak_RSS_one_worker': 0, 'bytes': 0})
    for row in done:
        folder = OUT / 'runs' / row['run']
        proof = read(folder / 'kiem.json')
        steps = [json.loads(line) for line in (folder / 'progress.jsonl').read_bytes().splitlines()]
        host = hosts[row['host']]
        host['windows'] += 1
        host['records'] += proof['records']
        host['window_wall_sum'] += proof['wall_seconds']
        host['CPU_sum'] += sum(item['cpu_seconds'] for item in steps if item['event'] == 'record')
        host['last_done'] = max(host['last_done'], row['elapsed'])
        host['peak_RSS_one_worker'] = max(host['peak_RSS_one_worker'],
                                          *(item['peak_rss'] for item in steps if item['event'] == 'record'))
        host['bytes'] += sum(value['bytes'] for value in proof['files'].values())
    return {'wall_seconds': events[-1]['elapsed'], 'hosts': dict(hosts)}


if __name__ == '__main__':
    result = {name: stage(prefix) for name, prefix in (('K-b', 'kb-001'), ('T6', 't6-001'))}
    result['generated_at'] = datetime.now(timezone(timedelta(hours=7))).isoformat()
    result['benchmark_isolated'] = False
    result['note'] = 'Thời gian vận hành gồm capture/oracle và chia sẻ cache trong cửa sổ. Các bước seal, chấm, replay và báo cáo ở log chuyển bước.'
    write('thoi-gian.json', result)
