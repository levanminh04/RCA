"""T-055 bước C1: dựng nguồn độc lập RE3-OB từ HF metadata, mã mờ, nhãn riêng và kế hoạch tải.

Chỉ đọc: G1 CSV (đã có trong repo), HF tree API (metadata) và 30 file inject_time.txt (10 byte, mốc tiêm dạng số,
được phép ở chế độ a). Không tải/mở metrics, traces, logs.

Đầu ra:
- results/T-055/runs/nguon-001/independent-source.json   (theo member, không tên ca, không nhãn)
- results/T-055/runs/nguon-001/partition.json            (opaque -> host, không tên ca)
- D:/RCA-ext/private/T-055/{labels.json, canonical-labels.json, stage-<host>.json}  (riêng, ngoài git)
"""
import csv
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-055/runs/nguon-001'
PRIVATE = Path('D:/RCA-ext/private/T-055')
REPO = 'phamquiluan/RCAEval'
REV = 'afeacb11bcc94dadfd1c8f483ee4377b2b8b614e'
G1 = ROOT / 'results/T-021/chia-theo-o/A-phan-tang.csv'
LOCATOR = 'data/locked/rcaeval-re3ob-30'
FILES = ('metrics.parquet', 'traces.parquet', 'logs.parquet')


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'rca-research'}),
                                        timeout=60) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def canon(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'xb') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=1, sort_keys=True).encode())
    return {'path': str(path).replace('\\', '/'), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size}


def main():
    g1_sha = hashlib.sha256(G1.read_bytes()).hexdigest()
    rows = [r for r in csv.DictReader(open(G1, encoding='utf-8')) if r['dataset'] == 'RE3-OB']
    assert len(rows) == 30
    cases = []
    for r in rows:
        member = hashlib.sha256(json.dumps(['RE3-OB', r['case']], separators=(',', ':'),
                                           ensure_ascii=False).encode()).hexdigest()
        cases.append(dict(case=r['case'], member=member, opaque='test-' + member[:10], root=r['root'],
                          fault=r['fault']))
    locked = set(json.loads((ROOT / 'results/T-052/ke-hoach-tap-test.json').read_bytes())
                 ['cohorts']['RE3-OB']['members_locked_sha256'])
    assert {c['member'] for c in cases} == locked, 'member khác bản khóa G1'
    assert len({c['opaque'] for c in cases}) == 30, 'mã mờ trùng'
    independent, stage, meta_log = {}, {}, []
    for c in cases:
        tree = json.loads(get(f'https://huggingface.co/api/datasets/{REPO}/tree/{REV}/{c["case"]}?expand=true'))
        by = {x['path'].rsplit('/', 1)[1]: x for x in tree if x['type'] == 'file'}
        if set(by) != set(FILES) | {'inject_time.txt'}:
            raise SystemExit('tập file khác dự kiến: ' + ','.join(sorted(by)))
        files = {}
        for name in FILES:
            x = by[name]
            files[name] = {'path': f'{LOCATOR}/{c["opaque"]}/{name}', 'bytes': x['lfs']['size'],
                           'sha256': x['lfs']['oid']}
        raw = get(f'https://huggingface.co/datasets/{REPO}/resolve/{REV}/{c["case"]}/inject_time.txt')
        blob = hashlib.sha1(b'blob %d\x00' % len(raw) + raw).hexdigest()
        if blob != by['inject_time.txt']['oid'] or len(raw) != by['inject_time.txt']['size']:
            raise SystemExit('inject_time khác blob HF')
        t = int(raw.decode().strip())
        independent[c['member']] = {'files': files, 'member_sha256': c['member'], 't': t}
        stage[c['opaque']] = {'case': c['case'], 'files': files,
                              'inject_time': {'size': len(raw), 'git_oid': blob}}
        meta_log.append({'opaque': c['opaque'], 'tree_entries': len(tree)})
    # Phân vùng theo cỡ traces (cân tải), sắp theo mã mờ; không dùng root/fault.
    order = sorted(cases, key=lambda c: (-independent[c['member']]['files']['traces.parquet']['bytes'], c['opaque']))
    load, part = {'ec2_1': 0, 'ec2_2': 0}, {}
    for c in order:
        h = min(sorted(load), key=lambda k: (load[k], sum(1 for v in part.values() if v == k)))
        if sum(1 for v in part.values() if v == h) >= 15:
            h = 'ec2_2' if h == 'ec2_1' else 'ec2_1'
        part[c['opaque']] = h
        load[h] += independent[c['member']]['files']['traces.parquet']['bytes']
    assert sorted(list(part.values()).count(h) for h in load) == [15, 15]
    aliases = {}
    labels = {'dataset': 'RE3-OB', 'g1_revision': g1_sha,
              'alias_sha256': hashlib.sha256(canon(aliases)).hexdigest(),
              'cases': {c['opaque']: {'member_sha256': c['member'], 'root': c['root'], 'fault': c['fault'],
                                      'cell': ['RE3-OB', c['root'], c['fault']]} for c in cases}}
    # Nguồn nhãn thứ hai: tách từ tên thư mục HF (độc lập với cột root/fault của CSV G1).
    canonical = {'dataset': 'RE3-OB', 'g1_revision': g1_sha, 'alias_sha256': labels['alias_sha256'], 'by_member': {}}
    for c in cases:
        _, root, fault, _rep = c['case'].split('_')
        canonical['by_member'][c['member']] = {'member_sha256': c['member'], 'root': root, 'fault': fault,
                                               'cell': ['RE3-OB', root, fault]}
    out = {
        'independent': write_new(OUT / 'independent-source.json',
                                 {'dataset': 'RE3-OB', 'g1_revision': g1_sha, 'cases_by_member': independent,
                                  'source': {'hf_repo': REPO, 'revision': REV,
                                             'method': 'HF tree API lfs.oid/size + inject_time.txt git blob'}}),
        'partition': write_new(OUT / 'partition.json', {'dataset': 'RE3-OB', 'hosts': part,
                                                        'rule': 'greedy by traces.parquet bytes, opaque order; 15/15',
                                                        'load_bytes': load}),
        'labels': write_new(PRIVATE / 'labels.json', labels),
        'canonical_labels': write_new(PRIVATE / 'canonical-labels.json', canonical),
    }
    for h in load:
        out['stage_' + h] = write_new(PRIVATE / f'stage-{h}.json',
                                      {'host': h, 'revision': REV, 'repo': REPO,
                                       'cases': {o: v for o, v in stage.items() if part[o] == h}})
    out['receipt'] = write_new(OUT / 'build-receipt.json', {
        'g1': {'path': 'results/T-021/chia-theo-o/A-phan-tang.csv', 'sha256': g1_sha},
        'outputs': {k: v for k, v in out.items() if not k.startswith(('labels', 'canonical', 'stage'))},
        'private_outputs_sha256': {k: v['sha256'] for k, v in out.items() if k.startswith(('labels', 'canonical', 'stage'))},
        'telemetry_opened': False, 'inject_time_read': 30})
    print(json.dumps({k: v['sha256'][:12] for k, v in out.items()}, indent=0))


if __name__ == '__main__':
    main()
