"""Đối chiếu trace T1 và hai nền C đã seal trước khi tái sử dụng."""
import gzip
import json
import math
from collections import Counter

from chuan_bi import ROOT, OUT, read, sha, verified, write


def records(relative, expected, select):
    path = ROOT / relative
    if sha(path) != expected['sha256'] or path.stat().st_size != expected['bytes']:
        raise ValueError(f'Lệch hash hoặc kích thước: {relative}')
    result = {}
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            if select is None or any(f'"config_id":"{cid}"' in line or f'"config_id": "{cid}"' in line for cid in select):
                row = json.loads(line)
                cid = row['config_id']
                if select is None or cid in select:
                    assert cid not in result
                    result[cid] = row
    assert select is None or set(result) == set(select), relative
    return result


def check_z(row):
    trace = row['trace']
    assert not trace['capture_errors'] and not row['numerical_exceptions']
    assert len(trace['normalized_input_sha256']) == 64
    z = [item['z'] for item in trace['phan_vi'].values() if 'z' in item]
    assert all(value['huu_han'] and all(math.isfinite(value[k]) for k in ('med_N', 'IQR', 'c', 'z_len', 'z_xuong'))
               for value in z)
    return len(z)


def main():
    root = 'results/T-053/'
    matrix = read(OUT / 'ma-tran.json')
    manifests = read(ROOT / root / 'manifest.json')['outputs']
    old_t1 = verified('T-053', root + 'runs/t1-kiem-001.json')
    assert old_t1['PASS'] and old_t1['records'] == 238 and not old_t1['failures']
    allocation = verified('T-053', root + 'runs/t1-phan-bo-001.json')
    t1 = Counter()
    for stage, jobs in allocation.items():
        for number, run in jobs.items():
            idx = int(number)
            prefix = root + f'runs/{run}-{idx:02d}/'
            path = prefix + 'trung-gian.jsonl.gz'
            row = records(path, manifests[path], {'K-R0'})['K-R0']
            assert all(row[k] == v for k, v in matrix['jobs'][idx].items())
            t1[stage] += 1
            t1['z_units'] += check_z(row)

    c_ids = set(matrix['reuse_from_T053'].values())
    seal = verified('T-053', root + 'runs/k-dong-pha1-001/seal.json')
    observed, coverage = [], Counter()
    for window, entries in seal.items():
        for entry in entries:
            native, trace = entry['path'], entry['trace']
            assert entry['sha256'] == manifests[native]['sha256']
            assert entry['trace_sha256'] == manifests[trace]['sha256']
            data = records(native, manifests[native], c_ids)
            traces = records(trace, manifests[trace], c_ids)
            prefix = trace.rsplit('/', 1)[0]
            command = verified('T-053', prefix + '/command.json')
            for cid in sorted(c_ids):
                row, sidecar = data[cid], traces[cid]
                assert row['opaque_id'] == sidecar['opaque_id'] == command['job']['opaque_id']
                assert window == sidecar['window'] == command['job']['window']
                assert all(sidecar[k] == v for k, v in command['job'].items())
                assert command['job'] in matrix['jobs']
                assert row['status'] in ('OK', 'NO_EVIDENCE') and set(row['worlds']) == set(matrix['worlds'])
                name = next(key for key, value in matrix['reuse_from_T053'].items() if value == cid)
                config = matrix['K-b'][name]
                previous = command['configs'][cid]
                assert {k:v for k,v in config.items() if k not in ('config_id', 'buoc')} == {
                    k:v for k,v in previous.items() if k not in ('config_id', 'buoc')}
                assert set(sidecar['trace']['world_state']) == set(matrix['worlds'])
                assert 'tang_P' in row['extra'] and 'don_vi_phan_vi' in row['extra']
                coverage[name + ':' + window] += 1
                coverage['z_units'] += check_z(sidecar)
                edges = [unit for unit in row['extra']['don_vi_phan_vi']
                         if unit['ma'].startswith('canh|') and unit['F_raw_len']]
                vertices = {v for unit in edges for v in unit['ma'].split('|')[1:]}
                observed.append({'config': name, 'job': command['job'], 'platform': command['platform'],
                                 'native': native, 'trace': trace, 'flagged_edges': len(edges),
                                 'vertices': len(vertices)})
    assert sum(t1[key] for key in allocation) == 238
    assert len(observed) == 164
    write('tai-su-dung.json', {
        'T1': {'status': 'TAI_SU_DUNG', 'old_check': root + 'runs/t1-kiem-001.json', 'counts': dict(t1),
               'reason': 'Ứng viên đã chạy trong T1, trace không kích hoạt phục hồi, bản tích hợp giữ native.'},
        'K-b': {'counts': dict(coverage), 'windows': observed, 'same_host_or_pilot_required': True},
    })


if __name__ == '__main__':
    main()
