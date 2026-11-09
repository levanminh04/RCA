"""Bản laptop của stage_ec2.py cho lượt bổ sung CIRCA (D-55-9): cùng logic tải/kiểm, khác thư mục gốc."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage_ec2
stage_ec2.BASE = Path('D:/RCA-ext/T-055/data-root')
if __name__ == '__main__':
    stage_ec2.main()
