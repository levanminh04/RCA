"""So native và dấu vết quyết định cho các cấu hình pilot trùng nhau."""
import argparse
import gzip
import json
import sys

from chuan_bi import OUT, ROOT, read, sha, verified

sys.path.insert(0, str(ROOT / 'results/T-053/scripts'))

from doi_chieu import Check, structural
from kiem_tai_su_dung import records


def load(run):
    folder = OUT / 'runs' / run
    proof = read(folder / 'kiem.json')
    job = read(folder / 'command.json')['job']
    maps = []
    for name in ('ban-ghi.jsonl.gz', 'trung-gian.jsonl.gz'):
        path = folder / name
        expected = proof['files'][name]
        assert path.stat().st_size == expected['bytes'] and sha(path) == expected['sha256']
        with gzip.open(path, 'rt', encoding='utf-8') as stream:
            rows = [json.loads(line) for line in stream]
        result = {row['config_id']: row for row in rows}
        assert len(result) == len(rows) == proof['records']
        maps.append(result)
    assert maps[0].keys() == maps[1].keys()
    for row in maps[1].values():
        assert all(row[k] == value for k, value in job.items())
        row['job'] = job
    return maps


def snapshot(record, sidecar):
    trace = sidecar['trace']
    assert not trace['capture_errors']
    if any(not unit['z']['huu_han'] for unit in trace['phan_vi'].values() if 'z' in unit):
        raise ValueError('Pilot có đơn vị z ngoài miền')
    return {
        'structure': structural(record),
        'U': trace['U'],
        'blocks': {w: value['blocks'] for w, value in record['worlds'].items()},
        'FI_channels': record['extra']['kenh_co_the_gioi'],
        'z': {name: unit.get('z') for name, unit in trace['phan_vi'].items()},
        'pv_scores': {unit['ma']: unit for unit in record['extra']['don_vi_phan_vi']},
        'counts': {w: {unit['ma']: unit for unit in value['don_vi_dem']}
                   for w, value in record['worlds'].items()},
        'E2': trace['gan_canh'],
    }


def old_c(new_native, new_trace):
    matrix = read(OUT / 'ma-tran.json')
    manifest = read(ROOT / 'results/T-053/manifest.json')['outputs']
    seal = verified('T-053', 'results/T-053/runs/k-dong-pha1-001/seal.json')
    candidates = {new: old for new, old in matrix['reuse_from_T053'].items() if new in new_native}
    assert candidates
    job = new_trace[next(iter(candidates))]['job']
    index = matrix['jobs'].index(job)
    entry, = [e for e in seal[job['window']] if e['path'].split('/')[-2].endswith(f'-{index:02d}')]
    maps = []
    for field in ('path', 'trace'):
        data = records(entry[field], manifest[entry[field]], set(candidates.values()))
        maps.append({new: data[old] for new, old in candidates.items()})
    for cid in candidates:
        assert maps[1][cid]['trace']['normalized_input_sha256'] == new_trace[cid]['trace']['normalized_input_sha256']
    return maps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('first')
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('second', nargs='?')
    target.add_argument('--nen-t053', action='store_true')
    parser.add_argument('--other-host', action='store_true')
    args = parser.parse_args()
    left, left_trace = load(args.first)
    right, right_trace = old_c(left, left_trace) if args.nen_t053 else load(args.second)
    common = sorted(left.keys() & right.keys())
    assert common, 'Hai pilot không có cấu hình chung'
    check = Check()
    for cid in common:
        job = left_trace[cid]['job']
        other_job = right_trace[cid].get('job', {k: right_trace[cid].get(k) for k in job})
        assert job == other_job
        a = snapshot(left[cid], left_trace[cid])
        b = snapshot(right[cid], right_trace[cid])
        check.compare(a['structure'], b['structure'], ['structure', cid], allow_float=False)
        for name in a.keys() - {'structure'}:
            check.compare(a[name], b[name], [name, cid], allow_float=args.other_host)
    print(json.dumps({'PASS': not check.counts, 'configs': common, 'failures': check.counts,
                      'differences': check.differences, 'max_abs_delta': check.delta}, ensure_ascii=False))
    if check.counts:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
