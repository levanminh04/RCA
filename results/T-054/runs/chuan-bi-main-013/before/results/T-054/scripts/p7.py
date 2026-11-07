"""CLI T054. Quyền còn thiếu luôn dừng trước selector/telemetry."""
import argparse
import json
import sys
from pathlib import Path

from bien_nhan import OUT, Blocked, atomic, append, canonical, fingerprint, read_pin, ref
from nguon import authorize, validate_slot
from dieu_phoi import status, supervise, launch


def load_plan(path, sha):
    p = read_pin({'path': path, 'sha256': sha})
    if p['schema'] != 'T054-PLAN-1' or len({fingerprint(j['slot']) for j in p['jobs']}) != len(p['jobs']):
        raise Blocked('plan schema lạ hoặc slot trùng')
    if type(p.get('workers', 1)) is not int or p.get('workers', 1) not in (1, 2):
        raise Blocked('workers phải là 1 hoặc 2 trong plan bất biến')
    for job in p['jobs']:
        validate_slot(job['slot'], p)
        if not isinstance(job['timeout_s'], (int, float)) or not 0 < job['timeout_s'] <= 3600:
            raise Blocked('deadline chưa khai hoặc vượt quyền lượt dài')
    registered = {fingerprint(j['slot']): (n, j) for n, j in enumerate(p['jobs'])}
    for n, job in enumerate(p['jobs']):
        if job.get('main_dependency'):
            dep = job['main_dependency']; parent = registered.get(fingerprint(dep['slot']))
            if not parent or parent[0] >= n or fingerprint(parent[1]) != dep['job_sha256']:
                raise Blocked('dependency thiếu/sai pin/thứ tự trong plan bất biến')
    return p


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('preflight', 'plan', 'run', '_supervise', 'status', 'drain', 'resume', 'verify', 'report'))
    parser.add_argument('--plan'); parser.add_argument('--sha256'); parser.add_argument('--directory')
    parser.add_argument('--authority'); parser.add_argument('--authority-sha256')
    parser.add_argument('--snapshot'); parser.add_argument('--snapshot-sha256')
    args = parser.parse_args(argv)
    if args.command in ('preflight', 'plan') and not args.plan:
        from lap_ho_so import preflight
        print(canonical(preflight()).decode('utf-8')); return
    plan = load_plan(args.plan, args.sha256)
    if args.snapshot and (args.command != 'report' or plan.get('host_role') != 'aggregate'):
        raise Blocked('snapshot nhận chỉ dùng report của plan ghép, không phát việc')
    directory = Path(args.directory or plan['directory']).resolve()
    if args.directory and directory != Path(plan['directory']).resolve():
        raise Blocked('output root khác plan bất biến; không phát bản sao ở thư mục khác')
    if not directory.is_relative_to(OUT.resolve()):
        raise Blocked('output ngoài vùng T054')
    if args.command == 'status':
        print(canonical(status(directory)).decode('utf-8')); return
    if args.command == 'plan':
        print(canonical({'jobs': len(plan['jobs']), 'mode': plan['mode'], 'pin': args.sha256}).decode('utf-8')); return
    if args.command == 'drain':
        append(directory / 'control.jsonl', {'action': 'DRAIN'})
        print('DRAIN: ngừng phát việc mới, giữ worker đang chạy'); return
    authority = read_pin({'path': args.authority, 'sha256': args.authority_sha256}) if args.authority else {}
    authorize(plan, authority, 'report' if args.command in ('report', 'verify') else 'run')
    if args.command == '_supervise':
        supervise(plan, directory); return
    if args.command in ('run', 'resume'):
        directory.mkdir(parents=True, exist_ok=True)
        cmd = [str(OUT / 'scripts/p7.py'), '_supervise', '--plan', str(Path(args.plan).resolve()),
               '--sha256', args.sha256, '--directory', str(directory)]
        if args.authority:
            cmd += ['--authority', str(Path(args.authority).resolve()), '--authority-sha256', args.authority_sha256]
        p = launch(sys.executable, cmd, directory / 'supervisor.stdout.txt', directory / 'supervisor.stderr.txt')
        print(canonical({'launcher_pid': p.pid, 'supervisor_pid': None,
                         'resolve_actual_supervisor': 'status.controller.pid',
                         'directory': str(directory), 'plan_sha256': args.sha256}).decode('utf-8')); return
    from cham import snapshot_from_status, verify_snapshot
    snapshot = (read_pin({'path':args.snapshot,'sha256':args.snapshot_sha256}) if args.snapshot
                else snapshot_from_status(plan, status(directory)))
    if snapshot.get('plan_sha256') != fingerprint(plan):
        raise Blocked('snapshot ghép khác plan toàn đợt')
    verified = verify_snapshot(snapshot, plan['jobs'])
    if args.command == 'report' and plan['mode'] != 'synthetic':
        from cham import evaluate
        required = plan.get('evaluation')
        if not required:
            raise Blocked('WAIT_LABEL_BINDING: cần ref nhãn và nguồn nhãn độc lập')
        runtimes = {k: read_pin(v) for k, v in required['runtime_refs'].items()}
        report_dir = Path(required['output']).resolve()
        if not report_dir.is_relative_to(OUT / 'reports'):
            raise Blocked('report output ngoài T054/reports')
        report_dir.mkdir(parents=True, exist_ok=False)
        evaluate(snapshot, plan, required['labels'], required['canonical_labels'], runtimes,
                 required['aliases'], plan['inventories'], report_dir)
        print(canonical({'report': str(report_dir)}).decode('utf-8')); return
    if args.command == 'report':
        receipt = atomic(directory / 'snapshot.json', snapshot)
        print(canonical({'verified_slots': len(verified), 'snapshot': receipt, 'scientific_result': False}).decode('utf-8'))
    else:
        print(canonical({'verified_slots': len(verified), 'snapshot_sha256': fingerprint(snapshot)}).decode('utf-8'))


if __name__ == '__main__':
    try:
        main()
    except (Blocked, OSError, KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
