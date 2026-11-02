"""Test của T-046 (cổng G1, G3 và quy tắc verdict ứng viên; SPEC T-046 Đặc tả bổ sung A3, A7).
Chạy: cd results/T-046/tests && $PY -B -m pytest -q -p no:cacheprovider"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'results' / 'T-046' / 'scripts'))
