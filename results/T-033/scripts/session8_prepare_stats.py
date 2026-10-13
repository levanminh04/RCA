from session8_control import ROOT,OPEN,read,write
import ast
inp=read(OPEN/'evidence-input.json');inv=read(ROOT/'results/T-033/runs/session8-evidence-receive-001/artifact-inventory.json');inp['pins'].update(inv['files']);write(OPEN/'stats-input.json',inp)
ast.parse((ROOT/'results/T-033/scripts/session8_stats.py').read_text())
s=(ROOT/'results/T-033/scripts/session8_inventory.py').read_text().replace("['session7-manual-pilot-001','session7-manual-rest-001']","['session8-stats-001']")
(ROOT/'results/T-033/scripts/session8_inventory_stats.py').write_text(s,encoding='utf-8',newline='\n')
s=(ROOT/'results/T-033/scripts/session8_receive_evidence.py').read_text().replace('session8-evidence-receive-001','session8-stats-receive-001').replace('session8-evidence-inventory-001','session8-stats-inventory-001').replace('session8_inventory_evidence.py','session8_inventory_stats.py').replace('runs/session8-evidence-001/','runs/session8-stats-001/').replace('session8-evidence-stream-001.timer.json','session8-stats-stream-001.timer.json')
(ROOT/'results/T-033/scripts/session8_receive_stats.py').write_text(s,encoding='utf-8',newline='\n')
print('PASS stats input')
