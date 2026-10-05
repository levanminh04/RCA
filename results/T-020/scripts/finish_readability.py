"""Whitespace-only edits of new prose; protect code and link targets."""
from pathlib import Path
import csv,re,json
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'results/T-020'
fixes=list(csv.DictReader((OUT/'trung-gian/dataset_evidence/spacing-fixes.csv').open(encoding='utf-8-sig')))
pairs=sorted({(r['old'],r['new']) for r in fixes},key=lambda x:-len(x[0]))
assert all(re.sub(r'\s','',a)==re.sub(r'\s','',b) for a,b in pairs)
changes={}
for path in OUT.glob('*.md'):
    before=path.read_text(encoding='utf-8-sig'); after=before
    chunks=re.split(r'(`[^`\n]*`|\]\([^\n)]*\))',after)
    n=0
    for i in range(0,len(chunks),2):
        for a,b in pairs:
            n+=chunks[i].count(a);chunks[i]=chunks[i].replace(a,b)
    after=''.join(chunks)
    assert re.sub(r'\s','',before)==re.sub(r'\s','',after)
    if before!=after:path.write_text(after,encoding='utf-8')
    changes[path.name]=n
p=OUT/'07-danh-sach-phuong-phap-va-doc-nhanh.md'
s=p.read_text(encoding='utf-8')
s=s.replace('`method-checklist.csv`','[checklist đầy đủ](trung-gian/method_evidence/method-checklist.csv)')
s=s.replace('`yeu-cau-hop-nhat.csv`','[yêu cầu đầu vào](yeu-cau-dau-vao-hop-nhat.csv)')
s=re.sub(r'`(results/T-\d{3}/[^`]+\.md)`',lambda m:'['+Path(m[1]).name+'](../'+m[1].removeprefix('results/')+')',s)
p.write_text(s,encoding='utf-8')
(OUT/'runs/readability-final.json').write_text(json.dumps({'whitespace_only_counts':changes,'link_edits':'root07 existing profile links; no scientific edits'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(changes)
