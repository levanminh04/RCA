"""Pinned provenance and approved processing-budget accounting, EC2 only."""
import pathlib,json,hashlib,os,datetime,time,shutil
import psutil
H=pathlib.Path(os.environ['T033_HOME']).resolve()
STAGE=pathlib.Path(__file__).parent
def sha(p):
 h=hashlib.sha256()
 with pathlib.Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def write(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def check(p,m):
 assert pathlib.Path(p).stat().st_size==m['bytes'] and sha(p)==m['sha256'],str(p)
 return p
def load_pins():
 assert H==pathlib.Path('/home/ubuntu/rca/T-033') and os.name=='posix'
 assert sha(STAGE/'pins.json')==os.environ['T033_PINS_SHA256']
 pins=read(STAGE/'pins.json')
 for rel,m in pins['files'].items():check(H/rel,m)
 assert sha(H/'inputs/source.json')==pins['source_sha256']
 return pins
def guard(reserve=0):
 assert not (H/'STOP').exists(),'STOP'
 p=(H/os.environ['T033_PROCESSING_LEDGER_PATH']).resolve();assert p.is_relative_to(H)
 assert sha(p)==os.environ['T033_PROCESSING_LEDGER_SHA256'],'BUDGET_LEDGER_HASH'
 j=read(p);assert j['accounting_valid_for_next_run'],'BUDGET_LEDGER_INCOMPLETE'
 assert j['source_sha256']==sha(H/'inputs/source.json')
 S=read(H/'inputs/source.json')
 active=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(os.environ['T033_ACTIVE_PROCESS_STARTED_UTC'])).total_seconds()
 used=j['approved_total_processing_s']+active
 assert 0<=active and used<S['budget_compute_s'],'BUDGET_STOP'
 logical=sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
 assert logical+reserve<S['budget_bytes'],'STORAGE_STOP'
 assert shutil.disk_usage(H).free>reserve+8*2**20,'DISK_STOP'
 return {'logical_bytes':logical,'disk_free_bytes':shutil.disk_usage(H).free,'ram_available_bytes':psutil.virtual_memory().available,'cumulative_processing_s':used,'remaining_compute_s':S['budget_compute_s']-used}
