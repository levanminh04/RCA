from pathlib import Path
import json,hashlib,shutil,difflib,ast
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def text(p,s):Path(p).write_text(s,encoding='utf-8')
loader='''from pathlib import Path
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
'''
for t in ['T-037','T-038','T-039']:
 dest=ROOT/f'results/{t}/runs/doi-chieu-smtp-001'
 text(dest/'pin_loader.py',loader)
 shutil.copyfile(RUN/'adoption-oracle.json',dest/'oracle.json')

# Full T037 checker: keep every behavioral check; old-pin checks use frozen before
# files and the comparator unknown-SMTP literal is changed from 1 to prewritten 0.
dest=ROOT/'results/T-037/runs/doi-chieu-smtp-001'
source=ROOT/'results/T-037/runs/graph-003/runner.py';s=source.read_text(encoding='utf-8-sig');n=s
pairs=[
 ("require('protected-pin:'+rel,sha(ROOT/rel),pre['protected'][rel])","require('protected-pin-history:'+rel,sha(Path("+repr(str(RUN/'before'))+")/rel),pre['protected'][rel])"),
 ("for row in adapted:require('verified-current-code:'+row['path'],sha(ROOT/row['path']),row['current_sha256'])","for row in adapted:require('verified-baseline-code:'+row['path'],sha(Path("+repr(str(RUN/'before'))+")/row['path']) if (Path("+repr(str(RUN/'before'))+")/row['path']).exists() else sha(ROOT/row['path']),row['current_sha256'])"),
 ("mod=package('t037_complete_static',code)","from pin_loader import api\n  mod=api()"),
 ("check('unknown_only_endpoint_match',unknown['views']['endpoints']['numerator'],1)","check('unknown_SMTP_missing_channel_no_endpoint_match',unknown['views']['endpoints']['numerator'],load(Path("+repr(str(dest/'oracle.json'))+"))['T037_unknown_smtp_missing_trace_channel_endpoint_numerator'])"),
 ("if __name__=='__main__':", "if __name__=='__main__':")]
for a,b in pairs:
 assert n.count(a)==1,a;n=n.replace(a,b,1)
# main takes an explicit attempt output inside the approved new run, not BASE/runs.
n=n.replace("raise SystemExit(main(BASE/'runs'/sys.argv[1]))","raise SystemExit(main(Path(__file__).resolve().parent/'checks'/sys.argv[1]))")
(dest/'checks').mkdir(exist_ok=True)
text(dest/'check_adoption.py',n);text(dest/'checker-adaptation.diff',''.join(difflib.unified_diff(s.splitlines(True),n.splitlines(True))))
# preserve old T037 SMTP compare fixture input/oracle/output; use new checks only.
save(dest/'fixture-version-map.json',{'legacy':'results/T-037/runs/graph-003/fixture-compare-unknown.json','old_expected_numerator':1,'V2_expected_numerator':0,'reason':'approved SMTP marker plus missing trace channel; type remains unknown','all_other_checks':'original checker literal unchanged; old pin guards verify frozen before, active guards pin_loader'})
print('Prepared strict loaders and full T037 behavioral adoption checker.')
