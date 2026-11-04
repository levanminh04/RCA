"""Đóng nguồn pha 1 và kiểm đủ tích ca × cấu hình trước khi ghép nhãn."""
import argparse
from collections import defaultdict
from pathlib import Path

from chuan_bi import OUT, ROOT, read, sha, write
from chay_khoi import t6_branch
from kiem_tai_su_dung import records


def from_run(run, expected):
    folder = OUT / 'runs' / run
    proof, command = (read(folder / name) for name in ('kiem.json', 'command.json'))
    assert command['matrix_sha256'] == sha(OUT / 'ma-tran.json')
    assert command.get('runner_sha256', sha(OUT / 'scripts/chay_cua_so.py')) == sha(OUT / 'scripts/chay_cua_so.py')
    configs = {row['config_id'] for row in command['configs']}
    assert expected <= configs and proof['records'] == len(configs)
    paths = {}
    for field, name in [('native', 'ban-ghi.jsonl.gz'), ('trace', 'trung-gian.jsonl.gz')]:
        path = folder / name
        pinned = proof['files'][name]
        assert path.stat().st_size == pinned['bytes'] and sha(path) == pinned['sha256']
        paths[field] = {'path': path.relative_to(ROOT).as_posix(), **pinned}
    return paths, command


def read_row(spec, config):
    return records(spec['path'], spec, {config})[config]


def native_and_trace(entry):
    source = entry['source_config']
    rec = read_row(entry['native'], source)
    trace = read_row(entry['trace'], source)
    for value in (rec, trace):
        assert value['opaque_id'] == entry['job']['opaque_id']
        value['config_id'] = entry['config']
    rec['variant'] = entry['config']
    return rec, trace


def run_entry(config, run, host, job):
    paths, cmd = from_run(run, {config})
    assert cmd['job'] == job
    assert ('Windows' if host == 'laptop' else 'Linux') in cmd['platform']
    return dict(config=config, source_config=config, host=host, job=job, **paths)


def old_entries(matrix):
    old = read(ROOT / 'results/T-053/manifest.json')['outputs']
    candidates = read(OUT / 'tai-su-dung.json')['K-b']['windows']
    sources = matrix['reuse_from_T053']
    out = {}
    for row in candidates:
        base = {}
        for kind in ('native', 'trace'):
            rel = row[kind]
            base[kind] = {'path': rel, **old[rel]}
        cid = row['config']
        host = 'laptop' if 'Windows' in row['platform'] else 'ec2'
        idx = matrix['jobs'].index(row['job'])
        out[idx, cid] = dict(config=cid, source_config=sources[cid], host=host, job=row['job'], **base)
    return out


def invariant_units(traces, pairs, stage):
    for off, on in pairs:
        for world in ('P', 'S_lo', 'S_hi'):
            rows = [traces[cid]['world_state'][world]['units'] for cid in (off, on)]
            by_id = [{x['don_vi']['ma']: x for x in units
                      if stage != 'T6' or x['don_vi']['nhom'] != 'tan_suat'} for units in rows]
            assert by_id[0] == by_id[1], (off, on, world, 'đơn vị chung khác')


def seal(stage, prefix, jobs, configs, old, branch=None):
    matrix = read(OUT / 'ma-tran.json')
    rows = defaultdict(list)
    for host, indices in jobs.items():
        for idx in indices:
            job = matrix['jobs'][idx]
            if stage == 'K-b':
                new = {cid for cid in configs if cid.endswith('VC')}
            else:
                new = {matrix['T6_conditional'][branch]['on']['config_id']}
            base = {cid: old[idx, cid] for cid in set(configs) - new}
            fresh = {cid: run_entry(cid, f'{prefix}-{host}-{idx:02d}', host, job) for cid in sorted(new)}
            group = {**base, **fresh}
            hashes, universe = set(), set()
            traces = {}
            for cid in sorted(group):
                entry = group[cid]
                rec, trace = native_and_trace(entry)
                assert rec['status'] in ('OK', 'NO_EVIDENCE'), (idx, cid, rec['status'])
                assert set(rec['worlds']) == set(matrix['worlds'])
                assert rec['extra']['che_do'] == dict(cong_dem='D1', cong_phan_vi='G3', thang='E4+T4c')
                payload = trace['trace']
                traces[cid] = payload
                assert not payload['capture_errors']
                assert all('z' not in v or v['z']['huu_han'] for v in payload['phan_vi'].values())
                hashes.add(payload['normalized_input_sha256'])
                universe.add(tuple(payload['U']))
                assert entry['host'] == host, (idx, cid, 'khác máy')
                rows[job['window']].append(dict(entry, index=idx))
            assert len(hashes) == len(universe) == 1, (idx, 'đầu vào hoặc U khác')
            pairs = [('K-thang-C', 'K-thang-VC'), ('K-day-du-C', 'K-day-du-VC')] if stage == 'K-b' else [configs]
            invariant_units(traces, pairs, stage)
    assert len(rows['that']) == 52 * len(configs) and len(rows['ce']) == 30 * len(configs)
    return {'stage': stage, 'branch': branch, 'configs': configs, 'entries': dict(rows),
            'matrix_sha256': sha(OUT / 'ma-tran.json')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('allocation', type=Path)
    parser.add_argument('prefix')
    parser.add_argument('--t6-after', type=Path)
    args = parser.parse_args()
    matrix = read(OUT / 'ma-tran.json')
    allocation = read(args.allocation)
    assert allocation['stage'] == 'K-b'
    if args.t6_after:
        branch = t6_branch(args.t6_after)
        receipt = read(args.t6_after / 'so-lan-nhin.json')
        path = ROOT / receipt['seal']
        assert sha(path) == receipt['seal_sha256']
        kb = read(path)
        assert kb['stage'] == 'K-b'
        old = {(row['index'], row['config']): row for rows in kb['entries'].values() for row in rows}
        pair = matrix['T6_conditional'][branch]
        result = seal('T6', args.prefix, allocation['jobs'], [pair['off'], pair['on']['config_id']], old, branch)
        result['kb_seal_sha256'] = receipt['seal_sha256']
        result['kb_decision_sha256'] = sha(args.t6_after / 'ket-cuc.json')
    else:
        result = seal('K-b', args.prefix, allocation['jobs'], sorted(matrix['K-b']), old_entries(matrix))
    name = f'runs/{args.prefix}-seal.json'
    write(name, result)
    path = OUT / name
    print(f'- `{path.relative_to(ROOT).as_posix()}`: `{sha(path)}`')


if __name__ == '__main__':
    main()
