from pathlib import Path
import json,hashlib,importlib.util,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def package(name,folder):
 s=importlib.util.spec_from_file_location(name,folder/'__init__.py',submodule_search_locations=[str(folder)])
 m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def api():
 pin=load(HERE/'pin.json');path=ROOT/pin['manifest']
 assert sha(path)==pin['manifest_sha256']
 m=load(path);assert m['created_utc']==pin['created_utc']
 for name,digest in m['code_hashes'].items():
  assert sha(path.parent/'code'/name)==digest
  assert sha(ROOT/'src/do_thi_tinh'/name)==digest
 for row in m['files']:assert sha(ROOT/row['path'])==row['sha256']
 return package('common_smtp_'+HERE.parents[1].name.replace('-','_'),path.parent/'code')
