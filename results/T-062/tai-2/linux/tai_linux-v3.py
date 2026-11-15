#!/usr/bin/env python3
"""L1 journey workload controller. Python 3.12 standard library, on exp-obs.

Deploy beside linux-source-manifest.json, k6/, linux-support/ and keys/.
Credentials remain on exp-app and in the existing load-host secret file.
All subprocess output is captured; the CLI emits exactly one JSON record.
"""
import argparse
import base64
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
TRANSPORT = 'http://127.0.0.1:19091'
TARGETS = {'app': ('129.221.208.47', 'exp-app.key'),
           'tai': ('3.24.8.49', 'may-tai.pem')}


class Failure(Exception):
    """Only explicitly safe messages may reach the CLI."""


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def event(kind, detail):
    with (ROOT / 'tai-linux-events.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps({'utc': utc(), 'kind': kind, 'detail': detail}) + '\n')


def run(args, data=None, timeout=60, label='subprocess'):
    try:
        p = subprocess.run(args, input=data, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise Failure(label + ' timed out; retain existing outputs') from None
    except OSError:
        raise Failure(label + ' could not execute') from None
    if p.returncode:
        # SSH stderr, login bodies and token stdout are never interpolated here.
        raise Failure(f'{label} failed (exit {p.returncode}); secret output omitted')
    return p.stdout


def options(machine):
    _, key = TARGETS[machine]
    for name in (key, 'known_hosts'):
        p = ROOT / 'keys' / name
        if not p.is_file() or (p.stat().st_mode & 0o777) != 0o600:
            raise Failure('SSH key/known_hosts missing or permissions differ from 0600')
    return ['-i', str(ROOT / 'keys' / key), '-o', 'BatchMode=yes',
            '-o', 'IdentitiesOnly=yes', '-o', 'ConnectTimeout=15',
            '-o', 'StrictHostKeyChecking=yes',
            '-o', 'UserKnownHostsFile=' + str(ROOT / 'keys' / 'known_hosts'),
            '-o', 'ServerAliveInterval=20', '-o', 'ServerAliveCountMax=3']


def ssh(machine, command, data=None, timeout=120, mutation=None, ignore_stop=False):
    if not ignore_stop and (ROOT / 'STOP').exists():
        raise Failure('STOP exists on exp-obs; remote command refused')
    if mutation:
        event('mutation_begin', {'machine': machine, 'command': mutation,
                                'commandSha256': hashlib.sha256(command.encode()).hexdigest()})
    result = run(['ssh', *options(machine), 'ubuntu@' + TARGETS[machine][0], command],
                 data, timeout, 'SSH ' + machine + (' ' + mutation if mutation else ''))
    if mutation:
        event('mutation_done', {'machine': machine, 'command': mutation})
    return result


def remote_python(machine, source, mutation=None, timeout=120):
    return json.loads(ssh(machine, 'python3 -', source.encode(), timeout, mutation))


def source(name):
    return (ROOT / name).read_text(encoding='utf-8-sig')


def verify_sources():
    manifest = json.loads(source('linux-source-manifest.json'))
    for name, info in manifest['files'].items():
        p = ROOT / name
        if Path(name).is_absolute() or '..' in Path(name).parts or not p.is_file():
            raise Failure('Invalid or missing source manifest entry')
        if digest(p) != info['sha256']:
            raise Failure('Source hash mismatch: ' + name)
    return manifest


def guard():
    if (ROOT / 'STOP').exists():
        raise Failure('STOP exists on exp-obs; no load/login/recovery')
    begin = ROOT / 'EXP-APP-BAO-TRI-1-BAT-DAU'
    end = ROOT / 'EXP-APP-BAO-TRI-1-XONG'
    if begin.exists():
        if not end.exists():
            raise Failure('exp-app maintenance: completion marker missing')
        parse = lambda p: dt.datetime.fromisoformat(p.read_text(encoding='utf-8-sig').splitlines()[0].replace('Z', '+00:00'))
        if parse(end) < parse(begin):
            raise Failure('exp-app maintenance: completion marker older than start')


def assert_idle():
    if ssh('tai', 'sudo -n docker ps -q --filter name=rca-tai-').strip():
        raise Failure('A rca-tai- container is running; nothing stopped or replaced')


def token_status():
    return remote_python('tai', source('linux-support/kiem-token-con-han.py'))


def renew_tokens(count):
    auth = source('linux-support/auth.py').split("if __name__=='__main__':", 1)[0]
    replacements = [
        ("def role_token(role='BUYER'):", "def role_token(role='BUYER', selected=None):"),
        ("user=next(x for x in users if role in x.get('realmRoles',[]))",
         "user=selected or next(x for x in users if role in x.get('realmRoles',[]))"),
        ("return json.load(response)['access_token']", 'return json.load(response)')]
    for before, after in replacements:
        if before not in auth:
            raise Failure('Pinned PKCE adapter no longer matches PowerShell substitutions')
        auth = auth.replace(before, after)
    auth += "\ntry:\n    pool=json.loads((ROOT/'env/l1-buyers.json').read_text())\n"
    auth += f"    values=[role_token(selected=pool[i % len(pool)]) for i in range({count})]\n"
    auth += "    print(json.dumps({'tokens':values}))\nexcept Exception:\n    raise SystemExit(1)\n"
    # Tokens pass through subprocess pipes and RAM only, never through argv/disk on exp-obs.
    payload = ssh('app', 'python3 -', auth.encode(), timeout=600)
    pool = json.loads(payload)
    if len(pool.get('tokens', [])) != count:
        raise Failure('PKCE pool count mismatch; secrets omitted')
    for item in pool['tokens']:
        if not item.get('access_token') or not item.get('refresh_token'):
            raise Failure('PKCE pool incomplete; secrets omitted')
    path = '/opt/rca-tai/secret/l1-tokens.json'
    before = ssh('tai', f'test ! -f {path} || sha256sum {path}').decode().split()
    ssh('tai', f'umask 077; cat > {path}; chmod 600 {path}', payload,
        mutation='umask 077; cat [in-memory PKCE pool] > ' + path + '; chmod 600')
    after = ssh('tai', f'sha256sum {path}').decode().split()[0]
    event('token_pool_renewed', {'count': count, 'beforeSha256': before[0] if before else None,
                               'afterSha256': after, 'rollback': 'mint a new PKCE pool'})


def preflight(count=20, force=False):
    guard()
    assert_idle()
    mock = remote_python('app', 'RECOVER=True\n' + source('linux-support/kiem-mock.py'),
                         mutation='python3 [verified kiem-mock.py, RECOVER=True]')
    if mock['restarted']:
        event('mock_restarted', mock)
    tunnel_source = "ACTION='start'\n" + source('linux-support/tunnel-remote.py')
    tunnel = remote_python('app', tunnel_source, mutation="python3 [verified tunnel-remote.py, ACTION=start]")
    health_source = ("import json,urllib.request\nwith urllib.request.urlopen(" + repr(TRANSPORT + '/health') +
                     ",timeout=5) as r: print(json.dumps({'status':r.code,'up':json.load(r).get('status')=='UP'}))\n")
    for attempt in range(3):
        try:
            health = remote_python('tai', health_source)
            if health.get('status') != 200 or not health.get('up'):
                raise Failure('Load-to-mock health is not UP/200')
            break
        except Failure:
            event('tunnel_health_failed', {'attempt': attempt + 1})
            if attempt == 2:
                raise
            tunnel = remote_python('app', tunnel_source, mutation='python3 [restart absent tunnel supervisor]')
            time.sleep(5)
    pool = token_status()
    if force or pool['count'] < count or pool['minAccessRemaining'] < 90 or pool['minRefreshRemaining'] < 300:
        renew_tokens(count)
        pool = token_status()
    if (pool['count'] < count or not pool.get('allBuyer') or pool['minAccessRemaining'] < 90
            or pool.get('permissionsOctal') != '0o600'):
        raise Failure('Token pool validation failed; secrets omitted')
    result = {'utc': utc(), 'mock': mock, 'tunnel': tunnel, 'tunnelHealth': health,
              'mockTransport': TRANSPORT, 'tokens': pool}
    event('preflight_ok', result)
    return result


def start(args, manifest):
    guard()
    assert_idle()
    tag, seconds, step, mult = args.tag, args.seconds, args.buoc_tai, args.multiplier
    if step and step >= seconds:
        raise Failure('BuocTai must be earlier than Seconds')
    # Refuse a reused tag before any login or token-file mutation.
    ssh('tai', 'test ! -e /opt/rca-tai/out/' + tag)
    cfg = json.loads(source('k6/cau-hinh.json'))
    metadata = preflight(cfg['maxVUs'] * (2 if step else 1), force=True)
    if step and metadata['tokens']['minRefreshRemaining'] <= step + 60:
        raise Failure('Idle second-scenario seed expires before step; choose an earlier step')
    files = {n: base64.b64encode((ROOT / 'k6' / n).read_bytes()).decode()
             for n in ('hanh-trinh.js', 'cau-hinh.json')}
    config = {'scenario': 'hanh-trinh', 'seconds': seconds, 'rate': cfg['rate'], 'timeUnit': '10s',
              'multiplier': mult, 'stepSeconds': step, 'mockTransport': TRANSPORT}
    prepare = '''import base64,hashlib,json,pathlib,subprocess
if subprocess.check_output(['sudo','-n','docker','ps','-q','--filter','name=rca-tai-']).strip():
    raise SystemExit(2)
root=pathlib.Path('/opt/rca-tai/out/''' + tag + "')\nroot.mkdir()\n"
    prepare += 'files=' + repr(files) + '\n'
    prepare += "for name,value in files.items(): (root/name).write_bytes(base64.b64decode(value))\n"
    prepare += "(root/'token-metadata.json').write_text(" + repr(json.dumps(metadata)) + ")\n"
    prepare += "(root/'run.json').write_text(" + repr(json.dumps(config) + '\n') + ")\n"
    prepare += "(root/'inputs.sha256').write_text(''.join(hashlib.sha256((root/n).read_bytes()).hexdigest()+'  '+n+'\\n' for n in files))\n"
    prepare += "print(json.dumps({'prepared':True}))\n"
    remote_python('tai', prepare, mutation='mkdir out/' + tag + '; snapshot verified k6, run.json, token metadata, inputs.sha256')
    out = '/opt/rca-tai/out/' + tag
    command = f'''set -euo pipefail
date -u --iso-8601=seconds > {out}/start-utc.txt
sudo -n docker run -d --name rca-tai-{tag} --user "$(id -u):$(id -g)" --network host \\
 -v {out}:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v {out}:/out \\
 -e FT_TEST_ENVIRONMENT=true -e FT_LOAD_SECONDS={seconds} -e FT_JOURNEY_RATE={cfg['rate']} \\
 -e FT_LOAD_MULTIPLIER={mult} -e FT_LOAD_STEP_SECONDS={step} -e FT_MOCK_TRANSPORT_URL={TRANSPORT} \\
 {shlex.quote(cfg['image'])} run --quiet --log-format raw --out json=/out/raw.json --out csv=/out/raw.csv --summary-export /out/summary.json /scripts/hanh-trinh.js
'''
    container = ssh('tai', 'bash -s', command.encode(), mutation=command).decode().strip()
    return {'tag': tag, 'containerId': container, 'run': config,
            'sourceManifestSha256': digest(ROOT / 'linux-source-manifest.json'), 'preflight': metadata}


def get(tag):
    return json.loads(ssh('tai', "sudo -n docker inspect rca-tai-" + tag + " --format '{{json .State}}'"))


def stop(tag):
    selector = 'name=^rca-tai-' + (tag + '$' if tag else '')
    command = ('ids=$(sudo -n docker ps -q --filter ' + shlex.quote(selector) + '); '
               'if [ -n "$ids" ]; then sudo -n docker stop --time 90 $ids; fi')
    return {'tag': tag, 'stopped': ssh('tai', command, timeout=150, mutation=command,
                                     ignore_stop=True).decode().splitlines()}


def receive(tag):
    if get(tag)['Running']:
        raise Failure('Container is running; receive refused, data retained')
    root = '/opt/rca-tai/out/' + tag
    # Repeated receives preserve the first frozen export rather than rewriting its times/hashes.
    command = f'''set -euo pipefail
cd {root}
if [ ! -f outputs.sha256 ]; then
 sudo -n docker logs rca-tai-{tag} > container.log 2>&1
 sudo -n docker inspect rca-tai-{tag} --format '{{{{json .State}}}}' > state.json
 date -u --iso-8601=seconds > received-utc.txt
 sha256sum *.json *.js *.log *.txt *.csv inputs.sha256 > outputs.sha256.partial
 mv outputs.sha256.partial outputs.sha256
fi
sha256sum --status -c outputs.sha256
'''
    ssh('tai', 'bash -s', command.encode(), mutation=command)
    destination = ROOT / 'tai-out' / tag
    destination.mkdir(parents=True, exist_ok=True)
    run(['scp', '-r', *options('tai'), 'ubuntu@' + TARGETS['tai'][0] + ':' + root + '/.', str(destination)],
        timeout=600, label='SCP receive (partial output retained)')
    checked = []
    for line in (destination / 'outputs.sha256').read_text().splitlines():
        expected, name = line.split(None, 1)
        name = name.lstrip('* ')
        if Path(name).name != name or not re.fullmatch('[0-9a-f]{64}', expected):
            raise Failure('Invalid output hash manifest; partial output retained')
        p = destination / name
        if p.is_symlink() or not p.is_file() or digest(p) != expected:
            raise Failure('Output hash mismatch: ' + name + '; data retained')
        checked.append(name)
    if not checked:
        raise Failure('Empty output hash manifest')
    result = {'tag': tag, 'destination': str(destination), 'hashesMatched': len(checked),
              'outputsManifestSha256': digest(destination / 'outputs.sha256'), 'state': get(tag)}
    event('receive_verified', result)
    return result


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Failure('Invalid CLI arguments: ' + message)


def bounded(low, high):
    def parse(value):
        try:
            number = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError('expected an integer') from None
        if not low <= number <= high:
            raise argparse.ArgumentTypeError(f'expected {low}..{high}')
        return number
    return parse


def main():
    os.umask(0o077)
    parser = Parser(add_help=False)
    parser.add_argument('command', choices=['test-duong', 'start', 'get', 'stop', 'receive'])
    parser.add_argument('--tag')
    parser.add_argument('--seconds', type=bounded(1, 3600), default=300)
    parser.add_argument('--buoc-tai', type=bounded(1, 3599), default=0)
    parser.add_argument('--multiplier', type=bounded(1, 3), default=1)
    args = parser.parse_args()
    if args.tag and not re.fullmatch('[a-z0-9][a-z0-9-]{0,47}', args.tag):
        raise Failure('Invalid tag')
    if args.command in ('start', 'get', 'receive') and not args.tag:
        raise Failure('--tag is required')
    if args.command == 'stop':
        return stop(args.tag)  # Explicit emergency stop still works with STOP/hash mismatch.
    manifest = verify_sources()
    if args.command in ('start', 'test-duong', 'receive'):
        with (ROOT / 'tai-linux.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Failure('Another L1 Linux mutation is in progress') from None
            if args.command == 'start':
                return start(args, manifest)
            if args.command == 'test-duong':
                cfg = json.loads(source('k6/cau-hinh.json'))
                return preflight(cfg['maxVUs'])
            return receive(args.tag)
    return {'tag': args.tag, 'state': get(args.tag)}


if __name__ == '__main__':
    try:
        value = {'ok': True, 'result': main()}
        code = 0
    except Failure as exc:
        value = {'ok': False, 'error': str(exc), 'utc': utc()}
        code = 1
    except Exception as exc:
        value = {'ok': False, 'error': type(exc).__name__ + '; details omitted to protect secrets', 'utc': utc()}
        code = 1
    print(json.dumps(value, separators=(',', ':')), flush=True)
    sys.exit(code)
