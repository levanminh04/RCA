"""Receive exact main partitions and evaluate only after snapshot/authority checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tarfile

from activate import RUN, ROOT, require_grant, pin
from main import HOSTS, REMOTE, ssh_args, remote_json
from bien_nhan import atomic, read_pin, ref, receive_paths, fingerprint
from cham import snapshot_from_status, merge_partitions, verify_snapshot, evaluate
from dieu_phoi import status
from nguon import authorize


def receive(host, destination):
    output = 'results/T-054/runs/main-013-v2/queue'
    command = 'tar -C ' + REMOTE + '/work-v2 -czf - ' + output
    done = subprocess.run(ssh_args(host, command), capture_output=True, timeout=3600)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors='replace')[-2000:])
    archive = destination / (host + '.tar.gz')
    archive.open('xb').write(done.stdout)
    target = destination / host
    target.mkdir(exist_ok=False)
    with tarfile.open(archive) as tar:
        for item in tar.getmembers():
            path = PurePosixPath(item.name)
            assert path.is_relative_to(output) and '..' not in path.parts
            assert item.isdir() or item.isfile() or (item.islnk() and PurePosixPath(item.linkname).is_relative_to(output)
                                                       and '..' not in PurePosixPath(item.linkname).parts)
        tar.extractall(target, filter='data')
    atomic(destination / (host + '-transfer.json'), dict(PASS=True, archive=ref(archive),
           sha256=hashlib.sha256(done.stdout).hexdigest(), receipt_scope='received immutable partition copy before labels'))
    return target


def main(grant_ref, destination):
    require_grant(read_pin(grant_ref))
    if not destination.resolve().is_relative_to(RUN):
        raise ValueError('receive destination outside 013-v2')
    destination.mkdir(parents=True, exist_ok=False)
    bundle = read_pin(pin(RUN / 'source-bundle.json'))
    aggregate = read_pin(pin(RUN / 'activated-001/aggregate-plan.json'))
    authority = read_pin(pin(RUN / 'activated-001/aggregate-authority.json'))
    received = {}
    parts = []
    mappings = {}
    mappings[REMOTE + '/data-root'] = str(ROOT)
    for host in HOSTS:
        received[host] = receive(host, destination)
        plan_ref = pin(RUN / 'activated-001' / (host + '-plan.json'))
        plan = read_pin(plan_ref)
        queue = received[host] / 'results/T-054/runs/main-013-v2/queue'
        snapshot = snapshot_from_status(plan, status(queue))
        atomic(destination / (host + '-snapshot.json'), snapshot)
        parts.append({'plan': plan_ref, 'snapshot': pin(destination / (host + '-snapshot.json'))})
        # Both hosts share a code-root spelling. Output slot IDs and seal IDs are disjoint.
        prefix = REMOTE + '/work-v2/results/T-054/runs/main-013-v2/queue/'
        for child in queue.iterdir():
            if child.is_dir():
                if child.name == 'seals':
                    for seal in child.iterdir():
                        mappings[prefix + 'seals/' + seal.name] = str(seal)
                else:
                    mappings[prefix + child.name] = str(child)
    local_ref = pin(RUN / 'activated-001/local-plan.json')
    local = read_pin(local_ref)
    local_snapshot = snapshot_from_status(local, status(local['directory']))
    atomic(destination / 'local-snapshot.json', local_snapshot)
    parts.append({'plan': local_ref, 'snapshot': pin(destination / 'local-snapshot.json')})
    receive_paths(mappings)
    try:
        merged = merge_partitions(aggregate, parts)
        verified = verify_snapshot(merged, aggregate['jobs'])
        authorize(aggregate, authority, 'report')
        if (authority.get('torai_A_source_grant') is not True
                and any(j['slot']['arm'] == 'torai_A' and fingerprint(j['slot']) in verified for j in aggregate['jobs'])):
            raise ValueError('A verified nhưng thiếu quyền nguồn A ở hồ sơ chấm')
        atomic(destination / 'verified-before-labels.json', merged)
        runtimes = {ds: read_pin(reference) for ds, reference in bundle['runtime_refs'].items()}
        output = Path(aggregate['evaluation']['output'])
        output.mkdir(parents=True, exist_ok=False)
        result = evaluate(merged, aggregate, bundle['evaluation']['labels'], bundle['evaluation']['canonical_labels'],
                          runtimes, bundle['evaluation']['aliases'], aggregate['inventories'], output)
        atomic(destination / 'report-receipt.json', dict(snapshot=pin(destination / 'verified-before-labels.json'),
               output=str(output), A4=ref(output / 'a4.json'), tables=ref(output / 'tables.json')))
        if os.name == 'nt':
            power = subprocess.run(['powercfg', '/change', 'standby-timeout-ac', '45'], capture_output=True, text=True)
            atomic(destination / 'power-restored.json', dict(exit=power.returncode, restored_AC_seconds=2700,
                   stdout=power.stdout, stderr=power.stderr))
            if power.returncode:
                raise RuntimeError('bảng đã ghi, cần khôi phục AC sleep theo D3')
    finally:
        receive_paths({})
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grant', required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    main({'path': args.grant, 'sha256': args.sha256}, Path(args.destination))
