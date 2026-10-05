"""Final authorized-file, frozen-input, coverage, link and table audit."""
from pathlib import Path
import csv,hashlib,json,re,subprocess,collections
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'results/T-020'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
freeze=json.loads((OUT/'trung-gian/input-freeze.json').read_text(encoding='utf-8-sig'))
changed=[]; missing=[]
for entry in freeze['inputs']:
    p=ROOT/entry['path']
    if not p.exists():missing.append(entry['path'])
    elif digest(p)!=entry['sha256']:changed.append(entry['path'])
assert not missing and changed==['docs/STATE.md'],(missing,changed)
state=subprocess.check_output(['git','show','HEAD:docs/STATE.md'],cwd=ROOT)
current=(ROOT/'docs/STATE.md').read_bytes()
extra=[line for line in current.splitlines(keepends=True) if line.startswith(b'| T-020 |')]
original_state_hash=next(e['sha256'] for e in freeze['inputs'] if e['path']=='docs/STATE.md')
assert len(extra)==1 and hashlib.sha256(current.replace(extra[0],b'',1)).hexdigest()==original_state_hash,'STATE other bytes changed'
assert current.replace(extra[0],b'',1).replace(b'\r\n',b'\n')==state.replace(b'\r\n',b'\n'),'STATE normalized HEAD mismatch'
assert b'\r\n' in extra[0]
supp=json.loads((OUT/'trung-gian/root/supplemental-inputs.json').read_text(encoding='utf-8'))
assert all(digest(Path(e['path']))==e['sha256'] for e in supp)
required=['g1-goi-quyet-dinh.md','01-bang-tieu-chi-hop-nhat.md','01-bang-tieu-chi-hop-nhat.csv',
'02-so-ca-da-nhin.md','02-so-ca-da-nhin.csv','03-task-cham-duoc-va-che-do-b.md',
'04-phuong-phap-x-dataset.md','04-phuong-phap-x-dataset.csv','yeu-cau-dau-vao-hop-nhat.csv',
'05-nhan-va-cua-so.md','06-phuong-an-dataset-va-chia.md','07-danh-sach-phuong-phap-va-doc-nhanh.md',
'08-so-chuyen-g1.csv','09-kiem-cheo-so-lieu.md','09-kiem-cheo-so-lieu.csv','10-ke-hoach-p3-de-xuat.md',
'ca-da-chay.csv','dinh-chinh-task-cu.md','de-xuat-tai-lieu-chung.md']
assert all((OUT/p).is_file() and (OUT/p).stat().st_size for p in required)
criteria=rows(OUT/'01-bang-tieu-chi-hop-nhat.csv')
assert len(criteria)==40 and all(all(v.strip() for v in r.values()) for r in criteria)
req=rows(OUT/'yeu-cau-dau-vao-hop-nhat.csv'); matrix=rows(OUT/'04-phuong-phap-x-dataset.csv')
assert len(req)==42 and len(matrix)==1680
g1=rows(OUT/'08-so-chuyen-g1.csv')
assert len(g1)==877 and sum(r['id'].startswith('G1-') and r['id'][3:].isdigit() for r in g1)==533
assert sum(r['loai'] in ['a','b'] for r in g1)==4
assert all(r['the_quyet_dinh'].startswith('D') for r in g1 if r['loai'] in ['a','b'])
assert all(r['loai'] in 'abcde' and r['trang_thai'] and r['the_quyet_dinh'] for r in g1)
checks=rows(OUT/'09-kiem-cheo-so-lieu.csv');counts=collections.Counter(r['ket_qua'] for r in checks)
assert counts=={'MATCH':3235,'MISMATCH':4,'OPEN':9},counts
replays=rows(OUT/'ca-da-chay.csv');assert len(replays)==16
assert collections.Counter(r['exit_code'] for r in replays)=={'0':12,'1':4}
ledger=rows(OUT/'02-so-ca-da-nhin.csv')
q=OUT/'07-danh-sach-phuong-phap-va-doc-nhanh.md'
blocks=re.split(r'^### ',q.read_text(encoding='utf-8'),flags=re.M)[1:]
assert len(blocks)==42 and max(len(b.split()) for b in blocks)<=350
main=(OUT/'g1-goi-quyet-dinh.md').read_text(encoding='utf-8')
bodywords=sum(len(l.split()) for l in main.splitlines() if not l.startswith('|'))
assert bodywords<=3100 and all('## D'+str(i)+' ' in main for i in range(1,7))
broken=[]
for p in OUT.glob('*.md'):
    text=p.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',text):
        target=target.strip('<>').split('#')[0]
        if not target or re.match(r'^[a-zA-Z]+://',target):continue
        target=re.sub(r':\d+$','',target)
        if not (p.parent/target).is_file():broken.append({'file':p.name,'target':target})
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],cwd=ROOT,text=True).splitlines()
assert all(s[3:]=='docs/STATE.md' or s[3:].startswith(('results/T-020/','tasks/T-020-tong-hop-g1/')) for s in status),status
diff=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
assert diff.returncode==0,diff.stdout+diff.stderr
report={'frozen_inputs':len(freeze['inputs']),'changed_expected':changed,'missing':missing,'supplemental_hashes':len(supp),
'STATE_other_bytes_unchanged':True,'required_main_files':len(required),'criteria_parts':len(criteria),'requirements':len(req),
'matrix_pairs':len(matrix),'G1_rows':len(g1),'occurrences':533,'gate_ab_rows':4,'checks':dict(counts),'replay_attempts':len(replays),
'ledger_identity_units':len(ledger),'quickread_variants':len(blocks),'max_quickread_words':max(len(b.split()) for b in blocks),
'g1_body_words_excluding_tables':bodywords,'broken_links':broken,'git_paths':len(status),'git_diff_check':'PASS',
'scope_incident':'trung-gian/dataset_evidence/scope-incident.md; raw TX1 schema sample exception retained, not concealed',
'outside_outputs':[],'locked_access':'not accessed or inventoried; source/output audit, not an OS-wide access trace'}
(OUT/'runs/final-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
assert not broken,broken
