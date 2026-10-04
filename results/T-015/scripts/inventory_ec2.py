"""Record only T-015's own files/runtime; no system mutation or external data reads."""
import hashlib,importlib.metadata,json,os,pathlib,platform,sys,time
task=pathlib.Path.home()/'rca/T-015'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()
env={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'python':sys.version,'executable':sys.executable,'real_executable':str(pathlib.Path(sys.executable).resolve()),'executable_sha256':sha(pathlib.Path(sys.executable)),'platform':platform.platform(),'vcpus':os.cpu_count(),'packages':{},'kernel_hashes':{},'uv_sha256':sha(task/'bin/uv') if (task/'bin/uv').exists() else 'uv not created on this host under T-015','timing_official':False}
for name in ['numpy','pandas','pyarrow','python-dateutil','pytz','six','tzdata']:
    try:env['packages'][name]=importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:env['packages'][name]='not_installed_in_this_interpreter'
for p in sorted((task/'src/microrank').glob('*')):
    if p.is_file():env['kernel_hashes'][str(p.relative_to(task))]=sha(p)
(task/'runs/environment.json').write_text(json.dumps(env,indent=2))
files=[]
for p in sorted(task.rglob('*')):
    if p.is_file() or p.is_symlink():
        files.append({'path':str(p),'relative_path':str(p.relative_to(task)),'bytes':p.stat().st_size,'symlink':p.is_symlink()})
(task/'runs/files-created.json').write_text(json.dumps({'task_root':str(task),'files':files,'all_paths_under_task_root':True,'self_inventory_written_after_scan':str(task/'runs/files-created.json')},indent=2))
print(json.dumps({'files':len(files),'vcpus':env['vcpus'],'packages':env['packages'],'inventory_self':str(task/'runs/files-created.json')}))
