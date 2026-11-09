"""Dựng code root cục bộ cho lượt bổ sung CIRCA RE3 (D-55-9): bản sao code đã ghim của repo + lớp phủ v2."""
import json
import os
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LR = Path('D:/RCA-ext/T-055/work-re3-local')
os.chdir(REPO)
pins = json.loads(Path('results/T-054/runs/chuan-bi-main-013-v2/code-pins.json').read_bytes())['code_pins']
extra = set()
for d in ('src', 'results/T-054/scripts', 'results/T-052/scripts'):
    for root, _, fs in os.walk(d):
        if '__pycache__' in root:
            continue
        extra |= {Path(root, f).as_posix() for f in fs}
files = sorted(set(pins) | extra | {'results/T-043/hop-dong.json', 'results/T-054/runs/trien-khai-004/quyet-dinh-minh.json'})
for f in files:
    dest = LR / f
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, dest)
shutil.copy2('results/T-055/overlay-v2/results/T-054/scripts/bien_nhan.py', LR / 'results/T-054/scripts/bien_nhan.py')
print(len(files), 'files ->', LR)
