from pathlib import Path
import json,difflib,shutil
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
PKG=ROOT/'results/T-038/runs/cap-nhat-goi-smtp-001/package'
def text(p,s):Path(p).write_text(s,encoding='utf-8')
def transform(source,dest,pairs):
 s=Path(source).read_text(encoding='utf-8-sig');n=s
 for a,b in pairs:
  assert n.count(a)>=1,(str(source),a,n.count(a));n=n.replace(a,b,3 if a=="HERE/'oracle-before-code.json'" else 1)
 text(dest,n);text(str(dest)+'.diff',''.join(difflib.unified_diff(s.splitlines(True),n.splitlines(True))))
# Replay literal V2 semantics against actual applied code, preserving baseline model inputs.
transform(PKG/'check_candidate.py',RUN/'check_smtp.py',[
 ('ROOT = HERE.parents[4]','ROOT = Path('+repr(str(ROOT))+')'),
 ("HERE/'oracle-before-code.json'","HERE/'oracle.json'"),
 ("HERE/'experimental_copy'","HERE/'code'"),
 ("==x['base_sha256']","==x['candidate_sha256']")])
shutil.copyfile(PKG/'candidate-code-hashes.json',RUN/'candidate-code-hashes.json')
# Legacy SMTP regression is re-executed against its exact approved T037 snapshot.
# It keeps its structural expectations; V2 expectations are in check_smtp.py.
transform(ROOT/'results/T-037/runs/smtp-regression-001/runner.py',RUN/'check_smtp_baseline.py',[
 ('ROOT = Path(__file__).resolve().parents[2]','ROOT = Path('+repr(str(ROOT))+')'),
 ("out = BASE / 'runs' / sys.argv[1]",'out = Path('+repr(str(RUN/'checks/smtp-baseline-002'))+')'),
 ("require('unchanged_shared_code:' + original, sha(ROOT / original), digest)","require('unchanged_shared_code:' + original, sha((ROOT/'results/T-037/runs/graph-003/code'/Path(original).name) if original.startswith('src/') else ROOT/original), digest)"),
 ("current = load_package('t037_smtp_current', ROOT / 'src/do_thi_tinh')","current = load_package('t037_smtp_current', ROOT / 'results/T-037/runs/graph-003/code')"),
 ("verification.append(dict(path=original, snapshot_sha256=digest, current_sha256=sha(ROOT / original)))","verification.append(dict(path=original, snapshot_sha256=digest, current_sha256=sha((ROOT/'results/T-037/runs/graph-003/code'/Path(original).name) if original.startswith('src/') else ROOT/original)))")])
print('Prepared V2 and historical baseline SMTP regressions; expected literals preserved.')
