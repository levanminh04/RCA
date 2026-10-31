"""Test của các sửa T-045 (results/T-045/dinh-chinh-cai-dat.md ĐC1–ĐC3). Dùng chung bộ sinh ca giả và fixture của
T-044 (chỉ đọc). Chạy: cd results/T-045/tests && $PY -B -m pytest -q -p no:cacheprovider"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'results' / 'T-044' / 'tests'))
sys.path.insert(0, str(ROOT / 'results' / 'T-044' / 'scripts'))
