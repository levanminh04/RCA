"""Capture the actual configured local runtime without opening a dataset."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'src')]
sys.path.extend(['D:/RCA-ext/src/RCAEval','D:/RCA-ext/src/baro','D:/RCA-ext/work/T-014/CIRCA',
                 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages'])
from lap_ho_so import stable_environment
print(json.dumps(stable_environment(),ensure_ascii=False))
