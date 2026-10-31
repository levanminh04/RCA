"""Test của các sửa T-045 (results/T-045/dinh-chinh-cai-dat.md ĐC1–ĐC3). Dùng chung bộ sinh ca giả và fixture của
T-044 (chỉ đọc). Chạy: cd results/T-045/tests && $PY -B -m pytest -q -p no:cacheprovider

`results/T-044/scripts/tat_dinh.py` gọi `import conftest` để lấy FIXTURE, XAO, TEN_KW; tên đó ở đây trỏ vào file này,
nên chép các hằng dữ liệu của conftest T-044 sang (không chép fixture hay hook của pytest)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'results' / 'T-044' / 'tests'))
sys.path.insert(0, str(ROOT / 'results' / 'T-044' / 'scripts'))

_spec = importlib.util.spec_from_file_location('conftest_t044', ROOT / 'results' / 'T-044' / 'tests' / 'conftest.py')
_c44 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_c44)
FIXTURE, XAO, TEN_KW = _c44.FIXTURE, _c44.XAO, _c44.TEN_KW
