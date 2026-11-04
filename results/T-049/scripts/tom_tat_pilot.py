"""Tổng hợp thời gian, RAM và hoạt động nhánh ở pilot đã đóng."""
import json
import sys
from collections import Counter

from chuan_bi import OUT, read, write
from kiem_pilot import load


def summary(run):
    folder = OUT / 'runs' / run
    proof = read(folder / 'kiem.json')
    command = read(folder / 'command.json')
    records, traces = load(run)
    progress = [json.loads(line) for line in (folder / 'progress.jsonl').read_text(encoding='utf-8').splitlines()]
    scenarios = {}
    for cid, sidecar in traces.items():
        record, trace = records[cid], sidecar['trace']
        scenarios[cid] = {
            'VC': [{'du_phong': row['du_phong'], 'dinh_danh': row['dinh_danh'], 'gan': len(row['gan'])}
                   for row in trace['gan_canh']],
            'tinh_trang_tan_suat': {
                w: dict(Counter(
                    '|'.join((u['cham']['trang_thai'], u['cham'].get('nhan') or 'chua_co_nhan'))
                    for u in state['units'] if u['don_vi']['nhom'] == 'tan_suat'))
                for w, state in trace['world_state'].items()
            },
            'OBS_DEPENDENT_tan_suat': [m for m in record['OBS_DEPENDENT'] if m.startswith('tan_suat|')],
        }
    return {'job': command['job'], 'resource': command['resource'], 'wall_seconds': proof['wall_seconds'],
            'bytes': sum(r['bytes'] for r in proof['files'].values()),
            'steps': progress, 'scenarios': scenarios}


if __name__ == '__main__':
    write('pilot-laptop.json', {name: summary(name) for name in sys.argv[1:]})
