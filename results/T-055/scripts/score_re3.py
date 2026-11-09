"""T-055: nhận, kiểm, seal rồi mới ghép nhãn và chấm RE3-OB (lượt chính + lượt bổ sung CIRCA).

Chạy sau khi ba supervisor đã dừng. Không chạy phương pháp. Telemetry không về laptop: tar bỏ *.csv/*.parquet.
- Lượt chính chấm trong code root S1 (bản sao cục bộ + lớp phủ v1 = đúng code đã sinh biên nhận EC2).
- Lượt CIRCA chấm trong code root cục bộ đã chạy nó (lớp phủ v2).
Đầu ra: <S1>/results/T-054/reports/re3-ban-cuoi-001/ và <local>/results/T-054/reports/re3-ban-cuoi-001-circa/,
sau đó chép sang repo results/T-054/reports/ cùng tên, kèm biên nhận ở results/T-055/runs/cham-001/.
Dùng: <python env main> -B score_re3.py main | circa
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath

REPO = Path('D:/RCA-flashticket')
S1 = Path('D:/RCA-ext/T-055/work-re3-score-v1')
LOCAL = Path('D:/RCA-ext/T-055/work-re3-local')
PRIVATE = Path('D:/RCA-ext/private/T-055')
REMOTE = '/home/ubuntu/rca-p7/T-054/checkpoint013/work-re3'
QREL = 'results/T-054/runs/re3-ban-cuoi-001/queue'
META = 'results/T-054/runs/re3-ban-cuoi-001/meta'
HOSTS = {'ec2_1': ('16.176.181.251', 'D:/RCA-ext/keys/key4.pem'), 'ec2_2': ('13.236.44.106', 'D:/RCA-ext/keys/key3.pem')}
RECEIPTS = REPO / 'results/T-055/runs/cham-001'


def ssh(host, command):
    ip, key = HOSTS[host]
    return ['ssh', '-T', '-i', key, '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes', '-o', 'StrictHostKeyChecking=yes',
            '-o', 'UpdateHostKeys=no', '-o', 'UserKnownHostsFile=C:/Users/84583/.ssh/known_hosts',
            '-o', 'ConnectTimeout=15', 'ubuntu@' + ip, command]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def setup_root(root, overlay):
    if not root.exists():
        shutil.copytree(LOCAL, root, ignore=shutil.ignore_patterns('queue-circa', 'reports'))
    shutil.copy2(overlay, root / 'results/T-054/scripts/bien_nhan.py')
    for rel in [META + '/' + n for n in ('profile.json', 'runtime.json', 'protocol.json', 'runtime-binding.json',
                                         'grant.json', 'failure-policy.json', 'ec2_1-plan.json', 'ec2_2-plan.json')]:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, root / rel)


def receive(host, root):
    dest = root / 'results/T-054/runs/re3-ban-cuoi-001/received'
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / (host + '.tar.gz')
    done = subprocess.run(ssh(host, f"tar -C {REMOTE} --exclude='*.parquet' -czf - {QREL}"),
                          capture_output=True, timeout=3600)
    if done.returncode:
        raise SystemExit(done.stderr.decode(errors='replace')[-2000:])
    archive.open('xb').write(done.stdout)
    target = dest / host
    target.mkdir()
    with tarfile.open(archive) as tar:
        for item in tar.getmembers():
            p = PurePosixPath(item.name)
            assert p.is_relative_to(QREL) and '..' not in p.parts
        tar.extractall(target, filter='data')
    return target / QREL, {'archive_sha256': sha(archive), 'bytes': archive.stat().st_size}


def labels_refs():
    lab, can = PRIVATE / 'labels.json', PRIVATE / 'canonical-labels.json'
    return ({'RE3-OB': {'path': str(lab), 'sha256': sha(lab)}}, {'RE3-OB': {'path': str(can), 'sha256': sha(can)}})


def run_main():
    setup_root(S1, REPO / 'results/T-055/overlay/results/T-054/scripts/bien_nhan.py')
    os.chdir(S1)
    sys.path[:0] = [str(S1 / 'results/T-054/scripts'), str(S1 / 'src')]
    from bien_nhan import atomic, read_pin, ref, receive_paths, fingerprint, Blocked
    from cham import snapshot_from_status, merge_partitions, verify_snapshot, evaluate_re3, describe
    from dieu_phoi import status
    out = S1 / 'results/T-054/runs/re3-ban-cuoi-001/received'
    parts, mappings, transfer = [], {}, {}
    plans = {}
    for host in HOSTS:
        queue, transfer[host] = receive(host, S1)
        plan_ref = ref(META + f'/{host}-plan.json')
        plan = read_pin(plan_ref); plans[host] = plan
        snap = snapshot_from_status(plan, status(queue))
        atomic(out / f'{host}-snapshot.json', snap)
        parts.append({'plan': plan_ref, 'snapshot': ref(out.relative_to(S1).as_posix() + f'/{host}-snapshot.json')})
        prefix = REMOTE + '/' + QREL + '/'
        for child in queue.iterdir():
            if child.is_dir():
                if child.name == 'seals':
                    for seal in child.iterdir():
                        mappings[prefix + 'seals/' + seal.name] = str(seal)
                else:
                    mappings[prefix + child.name] = str(child)
    aggregate = dict(plans['ec2_1'], host_role='aggregate', jobs=plans['ec2_1']['jobs'] + plans['ec2_2']['jobs'])
    aggregate.pop('directory', None)
    aggregate_ref = atomic(out / 'aggregate-plan.json', aggregate)
    receive_paths(mappings)
    try:
        merged = merge_partitions(aggregate, parts)
        states = {}
        for v in merged['slots'].values():
            states[v['state']] = states.get(v['state'], 0) + 1
        snap_ref = atomic(out / 'verified-before-labels.json', merged)
        records = verify_snapshot(merged, aggregate['jobs'])
        report = S1 / 'results/T-054/reports/re3-ban-cuoi-001'
        report.mkdir(parents=True, exist_ok=False)
        lab, can = labels_refs()
        runtime = read_pin(ref(META + '/runtime.json'))
        profile = read_pin(ref(META + '/profile.json'))
        result = evaluate_re3(merged, aggregate, lab, can, {'RE3-OB': runtime}, {'RE3-OB': profile['aliases']},
                              {'RE3-OB': profile['inventory']}, report)
        # Dẫn xuất C-d1/C-d2/C-c/C-g, vùng, vị trí N: dùng describe của cham với plan bỏ CIRCA (CIRCA lượt chính không hợp lệ, D-55-9).
        from nguon import compare_labels
        labels = {'RE3-OB': compare_labels(read_pin(lab['RE3-OB']), read_pin(can['RE3-OB']), runtime,
                                           profile['aliases'], profile['inventory'])}
        no_circa = dict(aggregate, jobs=[j for j in aggregate['jobs'] if j['slot']['arm'] != 'circa'])
        try:
            desc = describe(no_circa, records, labels)
        except Exception as exc:  # describe viết cho TT/Nezha; lỗi ở đây không chặn bảng chính
            import traceback
            desc = {'describe_error': repr(exc), 'traceback': traceback.format_exc()}
        atomic(report / 'tables-describe.json', desc)
        receipt = {'aggregate_plan': aggregate_ref, 'snapshot': snap_ref, 'states': states, 'transfer': transfer,
                   're3_tables': ref((report / 're3-tables.json').relative_to(S1).as_posix()),
                   'describe': ref((report / 'tables-describe.json').relative_to(S1).as_posix()),
                   'invalid_arm': {'circa': 'D-55-9 ModuleNotFoundError trên EC2; thay bằng lượt bổ sung'}}
    finally:
        receive_paths({})
    dst = REPO / 'results/T-054/reports/re3-ban-cuoi-001'
    shutil.copytree(report, dst)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    for f in ('ec2_1-snapshot.json', 'ec2_2-snapshot.json', 'verified-before-labels.json', 'aggregate-plan.json'):
        shutil.copy2(out / f, RECEIPTS / f)
    (RECEIPTS / 'main-receipt.json').open('x', encoding='utf-8').write(json.dumps(receipt, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({'states': states, 'report': str(dst)}, ensure_ascii=False))


def run_circa():
    os.chdir(LOCAL)
    sys.path[:0] = [str(LOCAL / 'results/T-054/scripts'), str(LOCAL / 'src')]
    from bien_nhan import atomic, read_pin, ref
    from cham import snapshot_from_status, verify_snapshot, evaluate_re3
    from dieu_phoi import status
    MC = 'results/T-054/runs/re3-ban-cuoi-001/meta-circa'
    plan = read_pin(ref(MC + '/local-plan.json'))
    snap = snapshot_from_status(plan, status(plan['directory']))
    out = LOCAL / 'results/T-054/runs/re3-ban-cuoi-001/received-circa'
    out.mkdir(parents=True, exist_ok=False)
    snap_ref = atomic(out / 'verified-before-labels.json', snap)
    verify_snapshot(snap, plan['jobs'])
    report = LOCAL / 'results/T-054/reports/re3-ban-cuoi-001-circa'
    report.mkdir(parents=True, exist_ok=False)
    lab, can = labels_refs()
    runtime = read_pin(ref(META + '/runtime.json'))
    profile = read_pin(ref(META + '/profile.json'))
    evaluate_re3(snap, plan, lab, can, {'RE3-OB': runtime}, {'RE3-OB': profile['aliases']},
                 {'RE3-OB': profile['inventory']}, report)
    dst = REPO / 'results/T-054/reports/re3-ban-cuoi-001-circa'
    shutil.copytree(report, dst)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out / 'verified-before-labels.json', RECEIPTS / 'circa-verified-before-labels.json')
    states = {}
    for v in snap['slots'].values():
        states[v['state']] = states.get(v['state'], 0) + 1
    print(json.dumps({'states': states, 'report': str(dst)}))


if __name__ == '__main__':
    {'main': run_main, 'circa': run_circa}[sys.argv[1]]()
