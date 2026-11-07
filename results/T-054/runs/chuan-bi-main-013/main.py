"""Final entry point. Source materialization, staging and dispatch follow the pinned grant."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile

from activate import RUN, ROOT, activate, pin, require_grant
from bien_nhan import Blocked, atomic, digest, read_pin, ref

HOSTS = {'ec2_1': ('16.176.181.251', 'D:/RCA-ext/keys/key4.pem'),
         'ec2_2': ('13.236.44.106', 'D:/RCA-ext/keys/key3.pem')}
REMOTE = '/home/ubuntu/rca-p7/T-054/checkpoint013'


def ssh_args(host, command):
    ip, key = HOSTS[host]
    return ['ssh', '-T', '-i', key, '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes',
            '-o', 'StrictHostKeyChecking=yes', '-o', 'UpdateHostKeys=no',
            '-o', 'UserKnownHostsFile=C:/Users/84583/.ssh/known_hosts', '-o', 'ConnectTimeout=15',
            '-o', 'ServerAliveInterval=15', '-o', 'ServerAliveCountMax=3', 'ubuntu@' + ip, command]


def remote_json(host, code):
    done = subprocess.run(ssh_args(host, 'python3 -B -c ' + shlex.quote(code)), capture_output=True, timeout=60)
    if done.returncode:
        raise Blocked(host + ': ' + done.stderr.decode(errors='replace')[-1500:])
    return json.loads(done.stdout)


def verify_host(host, expected):
    info = remote_json(host, "from pathlib import Path; import json,shutil; import subprocess; print(json.dumps(dict(instance_id=Path('/var/lib/cloud/data/instance-id').read_text().strip(),free_disk=shutil.disk_usage('/').free,available_ram=int(next(line.split()[1]for line in Path('/proc/meminfo').read_text().splitlines()if line.startswith('MemAvailable:')))*1024)))")
    if (info['instance_id'] != expected['instance_id'] or info['free_disk'] < expected['required_free_disk_bytes']
            or info['available_ram'] < expected['required_free_ram_bytes']):
        raise Blocked(host + ': instance hoặc dung lượng khác điều kiện khóa')
    return info


def verify_cloud_environment(host):
    run = REMOTE + '/work/' + RUN.relative_to(ROOT).as_posix()
    code = """
from pathlib import Path
import hashlib,json,os,subprocess
r=Path(RUN);root=Path(ROOT)
os.environ.update(PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
expected=json.loads((r/'environments.json').read_bytes())[HOST]
pins=json.loads((r/'code-pins.json').read_bytes())['code_pins']
for path,sha in pins.items():
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==sha,path
packet=json.loads((r/'main-packet.json').read_bytes())['files']
for path,meta in packet.items():
 p=root/path
 assert p.stat().st_size==meta['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256'],path
for key in ('main','py38'):
 exe=ENVROOT+'/envs/'+key+'/bin/python'
 program='import sys,json;sys.path.insert(0,'+repr(str(root/'results/T-054/scripts'))+');from lap_ho_so import stable_environment;print(json.dumps(stable_environment()))'
 actual=json.loads(subprocess.check_output([exe,'-B','-c',program],cwd=root))
 assert actual==expected[key],key
patches=json.loads((r/'environment-patches.json').read_bytes())['patches']
for rel,meta in patches.items():
 path=Path(ENVROOT)/'envs/py38/lib/python3.8/site-packages'/rel
 assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256'],rel
print(json.dumps({'PASS':True,'code_files':len(pins),'runtimes':2,'environment_patches':len(patches)}))
""".replace('ENVROOT', repr(REMOTE)).replace('RUN', repr(run)).replace('ROOT', repr(REMOTE + '/work')).replace('HOST', repr(host))
    return remote_json(host, code)


def verify_local_environment():
    expected = read_pin(pin(RUN / 'environments.json'))['local']
    external = read_pin(pin(RUN / 'local-external-code-pins.json'))['files']
    for path, meta in external.items():
        source = Path(path)
        if source.stat().st_size != meta['bytes'] or digest(source) != meta['sha256']:
            raise Blocked('upstream hoặc bản vá local đã đổi: ' + path)
    contract = read_pin(pin(RUN / 'dispatch-contract.json'))['hosts']['local']
    program = ('import sys,json;sys.path[:0]=' + repr([str(ROOT / 'results/T-054/scripts'),str(ROOT / 'src')])
               + ';sys.path.extend(' + repr(contract['pythonpath'])
               + ');from lap_ho_so import stable_environment;print(json.dumps(stable_environment()))')
    environment = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    for name, key in [('main', 'executable'), ('py38', 'method_executable')]:
        actual = json.loads(subprocess.check_output([contract[key], '-B', '-c', program], cwd=ROOT, env=environment))
        if actual != expected[name]:
            raise Blocked('runtime local khác bản khóa: ' + name)
    return dict(PASS=True, external_code_files=len(external), runtimes=2)


def transfer(host, files, destination, receipt_name):
    """Stream only opaque destination names; verify archive entries before committing each file."""
    metadata = {rel: {'bytes': meta['bytes'], 'sha256': meta['sha256']} for rel, (path, meta) in files.items()}
    code = """
import hashlib,json,os,sys,tarfile
from pathlib import Path,PurePosixPath
root=Path(DEST);root.mkdir(parents=True,exist_ok=True)
expected=None;got={}
with tarfile.open(fileobj=sys.stdin.buffer,mode='r|')as tar:
 for m in tar:
  if expected is None:
   assert m.name=='_manifest.json'and m.isfile()and m.size<2000000
   expected=json.load(tar.extractfile(m));continue
  p=PurePosixPath(m.name)
  assert m.isfile()and not p.is_absolute()and '..'not in p.parts and m.name in expected
  target=root/m.name;target.parent.mkdir(parents=True,exist_ok=True)
  tmp=target.with_name(target.name+'.partial013')
  assert not tmp.exists()
  h=hashlib.sha256();size=0
  source=tar.extractfile(m)
  with tmp.open('xb')as out:
   for chunk in iter(lambda:source.read(1048576),b''):
    out.write(chunk);h.update(chunk);size+=len(chunk)
  actual={'bytes':size,'sha256':h.hexdigest()};assert actual==expected[m.name],m.name
  if target.exists():
   assert target.stat().st_size==size and hashlib.sha256(target.read_bytes()).hexdigest()==h.hexdigest()
   tmp.unlink()
  else:os.link(tmp,target);tmp.unlink()
  got[m.name]=actual
assert got==expected
print(json.dumps({'PASS':True,'files':len(got),'bytes':sum(v['bytes']for v in got.values()),'destination':str(root),
 'manifest_sha256':hashlib.sha256(json.dumps(expected,sort_keys=True,separators=(',',':')).encode()).hexdigest()}))
""".replace('DEST', repr(destination))
    process = subprocess.Popen(ssh_args(host, 'python3 -B -c ' + shlex.quote(code)), stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        with tarfile.open(fileobj=process.stdin, mode='w|') as archive:
            data = json.dumps(metadata).encode('utf-8')
            entry = tarfile.TarInfo('_manifest.json'); entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))
            for rel, (path, expected) in sorted(files.items()):
                if path.stat().st_size != expected['bytes'] or digest(path) != expected['sha256']:
                    raise Blocked('nguồn đầu gửi khác pin')
                archive.add(path, arcname=rel, recursive=False)
        process.stdin.close(); process.stdin = None
        out, err = process.communicate(timeout=900)
        if process.returncode:
            raise Blocked(host + ': transfer thất bại ' + err.decode(errors='replace')[-1000:])
        receipt = json.loads(out)
        receipt_path = RUN / 'execution-receipts' / receipt_name
        if receipt_path.exists():
            if read_pin(pin(receipt_path)) != receipt:
                raise Blocked('biên nhận chuyển cũ khác dữ liệu được ghim')
        else:
            atomic(receipt_path, receipt)
        return receipt
    except BaseException:
        process.kill(); process.wait()
        raise


def source_files(plan, bundle):
    """Use existing private source maps; raw payloads are read only after the final grant."""
    originals = {ds: read_pin(reference) for ds, reference in bundle['original_source_refs'].items()}
    selected = {}
    for job in plan['jobs']:
        s = job['slot']
        row = originals[s['dataset']]['cases_by_member'][s['member_sha256']]
        for kind, target in job['source']['files'].items():
            original = row['files'][kind]
            if (target['sha256'], target['bytes']) != (original['sha256'], original['bytes']):
                raise Blocked('R1 thay dấu nội dung')
            selected[target['path']] = (ROOT / original['path'], target)
    return selected


def main(grant_ref):
    grant = require_grant(read_pin(grant_ref))
    verify_local_environment()
    acceptance = read_pin(pin(RUN / 'launch-conditions.json'))
    for host in HOSTS:
        verify_host(host, acceptance['hosts'][host])
    import psutil
    import shutil
    if (psutil.virtual_memory().available < acceptance['local']['required_free_ram_bytes']
            or shutil.disk_usage(ROOT).free < acceptance['local']['required_free_disk_bytes']):
        raise Blocked('laptop chưa đủ tài nguyên cho slot lớn nhất đã khóa')
    result = activate(grant_ref)
    bundle = read_pin(pin(RUN / 'source-bundle.json'))
    code_files = read_pin(pin(RUN / 'main-packet.json'))['files']
    sources = {rel: (ROOT / meta.get('source_path', rel), meta) for rel, meta in code_files.items()}
    sources[(RUN / 'main-packet.json').relative_to(ROOT).as_posix()] = (RUN / 'main-packet.json', ref(RUN / 'main-packet.json'))
    # Activation changes metadata hashes deterministically from the final decision.
    for path in (RUN / 'activated-001').glob('*.json'):
        if path.name.startswith(('local-', 'aggregate-')):
            continue
        sources[path.relative_to(ROOT).as_posix()] = (path, ref(path))
    # The common grant ref must be resolvable on each worker with its original pin.
    decision_path = Path(grant['source']['path'])
    if not decision_path.is_absolute():
        decision_path = ROOT / decision_path
    if not decision_path.is_relative_to(ROOT):
        raise Blocked('nguồn quyết định cuối cần ở vùng grants013 trong repo')
    sources[decision_path.relative_to(ROOT).as_posix()] = (decision_path, ref(decision_path))
    def prepare(host):
        plan = read_pin(pin(RUN / 'activated-001' / (host + '-plan.json')))
        transfer(host, sources, REMOTE + '/work', host + '-code.json')
        verification = verify_cloud_environment(host)
        atomic(RUN / 'execution-receipts' / (host + '-environment.json'), verification)
        transfer(host, source_files(plan, bundle), REMOTE + '/data-root', host + '-sources.json')
        return host
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(prepare, HOSTS))
    local_plan = read_pin(pin(RUN / 'activated-001/local-plan.json'))
    local_root = Path(local_plan['jobs'][0]['data_root'])
    for rel, (origin, meta) in source_files(local_plan, bundle).items():
        target = local_root / rel
        if not target.is_relative_to(local_root) or origin.stat().st_size != meta['bytes'] or digest(origin) != meta['sha256']:
            raise Blocked('nguồn local khác pin hoặc thoát gốc')
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if digest(target) != meta['sha256']:
                raise Blocked('bản local cũ khác pin')
        else:
            os.link(origin, target)
    if os.name == 'nt':
        power = subprocess.run(['powercfg', '/change', 'standby-timeout-ac', '0'], capture_output=True, text=True)
        atomic(RUN / 'execution-receipts/power-main-start.json', dict(exit=power.returncode, stdout=power.stdout, stderr=power.stderr))
        if power.returncode:
            raise Blocked('chưa giữ được laptop thức theo D3')
    cli = ROOT / 'results/T-054/scripts/p7.py'
    launch_results = []
    for host in HOSTS:
        remote_run = REMOTE + '/work/' + RUN.relative_to(ROOT).as_posix()
        code = ("import json,subprocess; from pathlib import Path; r=Path(" + repr(remote_run) + "); "
                + "p=json.loads((r/'activated-001/" + host + "-plan.json').read_bytes()); "
                + "a=json.loads((r/'activated-001/" + host + "-authority.json').read_bytes()); "
                + "import hashlib; f=lambda q:hashlib.sha256(q.read_bytes()).hexdigest(); "
                + "cmd=[" + repr(REMOTE + '/envs/main/bin/python') + ",'-B','results/T-054/scripts/p7.py','run','--plan',str(r/'activated-001/" + host
                + "-plan.json'),'--sha256',f(r/'activated-001/" + host + "-plan.json'),'--authority',str(r/'activated-001/" + host
                + "-authority.json'),'--authority-sha256',f(r/'activated-001/" + host + "-authority.json')]; "
                + "s=subprocess.run(cmd,cwd=" + repr(REMOTE + '/work') + ",capture_output=True,text=True); "
                + "print(json.dumps(dict(exit=s.returncode,stdout=s.stdout,stderr=s.stderr))); ")
        launched = remote_json(host, 'import os; os.environ.update(PYTHONHASHSEED="0",PYTHONDONTWRITEBYTECODE="1",OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1",MKL_NUM_THREADS="1"); ' + code)
        atomic(RUN / 'execution-receipts' / (host + '-launch.json'), launched)
        if launched['exit']:
            raise Blocked(host + ': CLI run bị chặn')
        launch_results.append(launched)
    authority = pin(RUN / 'activated-001/local-authority.json')
    pp = pin(RUN / 'activated-001/local-plan.json')
    env = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    done = subprocess.run([local_plan['jobs'][0]['executable'], '-B', str(cli), 'run', '--plan', pp['path'], '--sha256', pp['sha256'],
                           '--authority', authority['path'], '--authority-sha256', authority['sha256']], env=env, capture_output=True, text=True)
    atomic(RUN / 'execution-receipts/local-launch.json', dict(exit=done.returncode, stdout=done.stdout, stderr=done.stderr))
    if done.returncode:
        raise Blocked('local CLI run bị chặn')
    return dict(main_started=True, protocol=result['protocol'], hosts=list(HOSTS) + ['local'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grant', required=True)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    print(json.dumps(main({'path': args.grant, 'sha256': args.sha256}), ensure_ascii=False))
