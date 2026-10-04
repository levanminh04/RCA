"""Read old task top-level reports/specs/reviews to locate SS-relevant claims."""
from pathlib import Path
import re,json,hashlib
BASE=Path(__file__).resolve().parent; REPO=BASE.parents[2]
words=re.compile(r'Sock\s*Shop|RE[123]-SS|torai-SS|fse-ss|root_cause\.txt|\bJaeger\b|RCAEval',re.I)
rows=[]; absent=[]
for n in range(13):
    tid=f'T-{n:03}'
    dirs=list((REPO/'tasks').glob(tid+'-*'))
    rd=REPO/'results'/tid
    files=[]
    for d in dirs:
        files.extend(p for p in d.iterdir() if p.suffix=='.md')
    if rd.exists(): files.extend(rd.glob('*.md'))
    if not files: absent.append(tid)
    for p in sorted(files):
        b=p.read_bytes(); s=b.decode('utf-8-sig'); lines=s.splitlines()
        rows.append(dict(task=tid,path=p.relative_to(REPO).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),line_count=len(lines),relevant_lines=[dict(line=i,text=l) for i,l in enumerate(lines,1) if words.search(l)],scope='top-level report/spec/log/review text read; deeper artifacts only when referenced in source audit'))
(BASE/'prior-task-relevance-scan.json').write_text(json.dumps(dict(tasks_absent=absent,files=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(files_read=len(rows),absent=absent,relevant_files=sum(bool(r['relevant_lines']) for r in rows)),indent=2))
