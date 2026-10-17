"""Sinh tài liệu hiện hành v2.1 từ nguồn/bằng chứng đã lưu của T-035.

Bản sinh v1 được giữ trong runs/sua-n1-001/before/results/T-035/scripts/.
Lệnh này ghi ba tài liệu v2.1 được duyệt; bảng quan hệ/graph/Node giữ bản đã có.
"""
from pathlib import Path
import runpy

if __name__ == '__main__':
    script = Path(__file__).resolve().parents[1] / 'runs/sua-hop-dong-001/update_docs.py'
    runpy.run_path(str(script), run_name='__main__')
