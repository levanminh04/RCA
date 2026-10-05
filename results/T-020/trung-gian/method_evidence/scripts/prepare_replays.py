from pathlib import Path
import ast
import hashlib
import json

R=Path('D:/RCA-flashticket')
O=R/'results/T-020/trung-gian/method_evidence'
p=R/'results/T-015/scripts/independent_math.py'
s=p.read_text(encoding='utf-8')
ast.parse(s)
# Entire source inspected: only CLI writes, all through args.output or write_csv.
# No author import. Protect input allowlist and absolute output containment.
s=s.replace('    args = parser.parse_args()','''    args = parser.parse_args()
    allowed = Path("D:/RCA-flashticket/results/T-015/runs/independent-math/toy-connected/input.json").resolve()
    allowed_output = Path("D:/RCA-flashticket/results/T-020/trung-gian/method_evidence/runs").resolve()
    if args.input.resolve() != allowed:
        raise ValueError("CLI replay is allowlisted fixture only")
    if not args.output.resolve().is_relative_to(allowed_output):
        raise ValueError("Output outside T020 method evidence")''')
q=O/'scripts/microrank_independent_copy.py'
q.write_text(s,encoding='utf-8')
meta={'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'copy':str(q),'copy_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'changed':'add exact fixture input guard and output containment; arithmetic unchanged','all_imports':[ast.unparse(n) for n in ast.walk(ast.parse(s)) if isinstance(n,(ast.Import,ast.ImportFrom))],'source_write_sites':[n.lineno for n in ast.walk(ast.parse(s)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('write_text','write_bytes','mkdir','open')],'new_dataset_or_raw_read':False}
(O/'runs/replay-copy-audit.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print('copied and guarded MicroRank independent arithmetic')
