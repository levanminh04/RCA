"""Read-only metadata after STORAGE_STOP. No research calculation or writes."""
import pathlib,json,hashlib,subprocess,shutil,zipfile,struct,ast,time
H=pathlib.Path('/home/ubuntu/rca/T-033')
run=H/'runs/session7-manual-001'
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
files={p.name:{'bytes':p.stat().st_size} for p in run.iterdir() if p.is_file()}
headers={}
for name in ('nsigma','nsigma_doi_chung'):
    p=H/'runs/nsigma-frozen-first-001'/('dev-03d4910932--'+name+'.npz')
    if not p.exists():p=H/'runs/nsigma-frozen-rest-001'/p.name
    with zipfile.ZipFile(p) as z:
        values={}
        for member in z.namelist():
            with z.open(member) as f:
                assert f.read(6)==b'\x93NUMPY'
                v=f.read(2);n=struct.unpack('<H' if v[0]==1 else '<I',f.read(2 if v[0]==1 else 4))[0]
                values[member]=ast.literal_eval(f.read(n).decode('latin1' if v[0]<3 else 'utf-8'))
        headers[name]=values
ps=subprocess.check_output(['ps','-eo','pid,args'],text=True).splitlines()
print(json.dumps({'status':'READ_ONLY_STORAGE_STOP_METADATA','files':files,
    'new_run_bytes':sum(v['bytes'] for v in files.values()),
    'logical_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),
    'approved_limit_bytes':4*2**30,'disk_free_bytes':shutil.disk_usage(H).free,
    'source_sha256':digest(H/'inputs/source.json'),
    'point_lock_sha256':digest(run/'points-lock.json'),
    'coverage_matching_sha256':digest(run/'coverage-matching.json'),
    'frozen_array_headers':headers,
    'worker_candidates':[x for x in ps if str(H) in x and any(k in x for k in ['delay.py','context.py','factorial.py','frozen.py','_job','accounted_worker'])],
    'at_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
    'metadata_body_s':time.perf_counter()-_start,
    'research_resumed':False,'remote_writes':False},indent=2))
