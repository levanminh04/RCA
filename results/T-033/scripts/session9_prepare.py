"""Build input pins from verified received inventories, metadata only."""
import pathlib,json,ast
from session9_control import ROOT,OPEN,read,write
inp=read(ROOT/'results/T-033/runs/session8-open-001/evidence-input.json')
for name in ['session8-evidence-receive-001','session8-stats-receive-001']:
 inv=read(ROOT/'results/T-033/runs'/name/'artifact-inventory.json');inp['pins'].update(inv['files'])
ast.parse((ROOT/'results/T-033/scripts/session9_manual.py').read_text(encoding='utf-8'))
write(OPEN/'manual-input.json',inp)
print('PASS pin input and AST')
