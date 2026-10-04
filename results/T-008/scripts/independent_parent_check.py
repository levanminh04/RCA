"""Independent SQL join against selected CSVs, compare saved parent census."""
import csv,json,sqlite3,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'data/ngoai-rcaeval/nezha';R=ROOT/'results/T-008/runs';OUT=R/'independent-check-001';OUT.mkdir(exist_ok=False)
old=json.loads((R/'file-audit-001/summary.json').read_text());groups=collections.defaultdict(list)
for r in old['results']:
    if '/trace/' in r['path']:groups['/'.join(r['path'].split('/')[:3])].append(r)
checks=[]
for group,items in sorted(groups.items()):
    chosen={r['path']:r for r in [min(items,key=lambda x:x['path']),max(items,key=lambda x:x['path'])]}
    for path,r in chosen.items():
        con=sqlite3.connect(':memory:');con.execute('create table spans(t text,s text,p text)')
        with (BASE/path).open(encoding='utf-8-sig',newline='') as f:con.executemany('insert into spans values(?,?,?)',((x['TraceID'],x['SpanID'],x['ParentID']) for x in csv.DictReader(f)))
        con.execute('create index key_idx on spans(t,s)')
        counts={}
        counts['root_sentinel']=con.execute("select count(*) from spans where p in ('root','','0','0000000000000000') or p is null").fetchone()[0]
        histogram=dict(con.execute("select matches,count(*) from (select (select count(*) from spans b where b.t=a.t and b.s=a.p) matches from spans a where p not in ('root','','0','0000000000000000')) group by matches"))
        counts['missing_within_file']=histogram.get(0,0);counts['unique_resolved_within_file']=histogram.get(1,0);counts['ambiguous_within_file']=sum(n for k,n in histogram.items() if k>1)
        expected={k:r['parent'].get(k,0) for k in counts};checks.append(dict(path=path,sql_counts=counts,expected_counts=expected,pass_check=counts==expected));con.close()
(OUT/'result.json').write_text(json.dumps(dict(checks=checks,passed=all(x['pass_check'] for x in checks),selection='Lexicographically first and last trace CSV in every system/phase/date; independent SQL count not graph/source-wide proof'),indent=2))
assert all(x['pass_check'] for x in checks);print('PASS independent SQL',len(checks),'trace files')
