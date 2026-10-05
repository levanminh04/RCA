"""Reproduce normalized evidence ledger from frozen saved results (no telemetry)."""
from pathlib import Path
import runpy, shutil
root=Path(__file__).resolve().parents[3]
out=root/'results/T-020'
runpy.run_path(str(out/'trung-gian/exposure_ledger/build_ledger.py'),run_name='__main__')
runpy.run_path(str(out/'trung-gian/exposure_ledger/independent_validate.py'),run_name='__main__')
for name in ['02-so-ca-da-nhin.csv','02-so-ca-da-nhin.md']:
    shutil.copyfile(out/'trung-gian/exposure_ledger'/name,out/name)
