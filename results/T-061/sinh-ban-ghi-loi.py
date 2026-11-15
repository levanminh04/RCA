"""T-061 (gói C1): sinh bản ghi ERROR và UNSUPPORTED bằng chính hàm src/m1/chuoi.py::_ban_ghi_loi (không chạy chuỗi M1).

Chạy trong môi trường đã ghim của M1 (có numpy), không ghi bytecode:
  PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B \
    sinh-ban-ghi-loi.py <thư mục ra>
Params lấy từ method-input.json của ca c12e47ab (phần tử 6), như bộ điều phối đã truyền cho M1.
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
GOC = Path(__file__).resolve().parent
REPO = GOC.parents[1]
sys.path.insert(0, str(REPO / 'src'))
from m1 import chuoi  # noqa: E402

ra = Path(sys.argv[1])
ra.mkdir(parents=True, exist_ok=True)
params = json.load(open(REPO / 'results/T-058/dem-2026-11-10/rca-ban-dau/outputs/c12e47ab/method-input.json',
                        encoding='utf-8'))[6]
for st, msg in (('ERROR', 'ValueError: bản ghi thử của T-061'), ('UNSUPPORTED', 'bản ghi thử của T-061')):
    rec = chuoi._ban_ghi_loi(params, st, msg)
    (ra / f'ban-ghi-{st}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(st, rec['mode'], rec['window'], rec['verdict'])
