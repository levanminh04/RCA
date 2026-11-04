"""Ghim ma trận, tập ô chấm và nguồn trước khi chạy."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-049'
sys.path.insert(0, str(ROOT / 'src'))

from m1 import runner


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def verified(task, relative):
    manifest = read(ROOT / 'results' / task / 'manifest.json')
    outputs = manifest['outputs']
    if isinstance(outputs, list):
        outputs = {entry['path']: entry for entry in outputs}
    expected = outputs[relative]
    path = ROOT / relative
    if sha(path) != expected['sha256'] or path.stat().st_size != expected['bytes']:
        raise ValueError(f'Đầu ra {task} lệch manifest: {relative}')
    return read(path)


def write(name, value):
    with (OUT / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write('\n')


def ma_tran(plan, old):
    def make(name, source, *, vc=False, e3b=False):
        row = copy.deepcopy(old[source])
        row.update(config_id=name, buoc='T6' if e3b else 'K-b', nhanh_z=True)
        if vc:
            row['bat_tat']['E2'] = 'VC'
        row['bat_tat']['E3b'] = e3b
        row['ma_noi_dung'] = runner._ma_noi_dung(
            row['bat_tat'], row['tham_so_E4'], row['nhanh_z'], row['tham_so_E3'], row['tham_so_E5'])
        assert row['che_do'] == {'cong_dem': 'D1', 'cong_phan_vi': 'G3', 'thang': 'E4+T4c'}
        assert row['tham_so_E4']['epsilon'] == 0.05 and row['tham_so_E4']['alpha'] == 0.01
        assert row['bat_tat'] == dict(E1='U', E2='VC' if vc else 'C', E3=source.endswith('E3+E5'),
                                     E3b=e3b, E5=True, E6='a', E9=False, T12=False)
        return row

    thang, day_du = 'K-E1+E2+E5', 'K-E1+E2+E3+E5'
    kb = {
        'K-thang-C': make('K-thang-C', thang),
        'K-thang-VC': make('K-thang-VC', thang, vc=True),
        'K-day-du-C': make('K-day-du-C', day_du),
        'K-day-du-VC': make('K-day-du-VC', day_du, vc=True),
    }
    return {'jobs': plan['jobs'], 'sources': {**plan['sources'], 'src/m1/e4.py': sha(ROOT / 'src/m1/e4.py')},
            'worlds': ['P', 'S_lo', 'S_hi'], 'K-b': kb,
            'reuse_from_T053': {'K-thang-C': thang, 'K-day-du-C': day_du},
            'T6_conditional': {
                'C': {'off': 'K-thang-C', 'on': make('T6-C-E3b', thang, e3b=True)},
                'VC': {'off': 'K-thang-VC', 'on': make('T6-VC-E3b', thang, vc=True, e3b=True)},
            }}


def main():
    plan = verified('T-053', 'results/T-053/ke-hoach-pha1.json')
    for name, expected in plan['sources'].items():
        path = OUT / 'truoc-tich-hop-001/e4.py' if name == 'src/m1/e4.py' else ROOT / name
        if sha(path) != expected:
            raise ValueError(f'Nguồn ghim T-053 đã đổi: {name}')
    commands = [verified('T-047', f'results/T-047/runs/b3-k-c1-{kind}-001/command.json')
                for kind in ('that', 'ce')]
    assert commands[0]['configs'] == commands[1]['configs']
    old = {row['config_id']: row for row in commands[0]['configs']}
    matrix = ma_tran(plan, old)
    counts = 'results/T-043/ks16/dem-khong-nhan.json'
    groups = verified('T-043', counts)['tong_hop']
    joined = 'results/T-043/ks16/dem-sau-ghep-nhan.json'
    cells = verified('T-043', joined)['o_kich_hoat']
    eligibility = {name: {'tu': value['parents_with_overlap'], 'mau': value['parents_with_ge2_children']}
                   for name, value in groups.items()}
    assert all(r['mau'] > 0 and 20 * r['tu'] < r['mau'] for r in eligibility.values())
    scoring = {'CP': eligibility, 'CP_eligible': False, 'source_CP': counts,
               'source_E_X': joined, 'source_E_X_sha256': sha(ROOT / joined),
               'E_X': {k: sorted(set(cells[k]['RE2-TT']['o']) | set(cells[k]['Nezha-OB']['o']))
                       for k in ('E2-VC', 'E3b')}}
    assert [len(scoring['E_X'][k]) for k in ('E2-VC', 'E3b')] == [17, 12]
    write('ma-tran.json', matrix)
    write('o-cham.json', scoring)


if __name__ == '__main__':
    main()
