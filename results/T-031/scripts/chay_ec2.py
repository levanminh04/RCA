"""T-031 bước 4 trên EC2 (lời Minh 06/10/2026, LOG 13:45): chạy TORAI nguồn B rồi A, 30 ca × seed {0, 1, 2}.

Dùng nguyên `chay.py` và runner P3; chỉ thay lúc chạy các đường dẫn môi trường kiểu Windows của runner
(`ENVS`, `PYTHONPATH`, `ROOT`, `TORAI_TT`) bằng đường dẫn trên EC2. Không sửa `src/p3`. Vai 'drain' dùng chung
môi trường 'main' (có drain3 0.9.11). Giới hạn mỗi lượt giữ 3.600 s như SPEC; Minh bỏ giới hạn tổng 1 giờ.

python chay_ec2.py <ten> <torai_B|torai_A>
"""
import sys
from pathlib import Path

B = Path.home() / 'rca' / 'T-031'
import chung  # noqa: E402
from p3 import runner  # noqa: E402

runner.ROOT = chung.ROOT
runner.ENVS = {'main': str(B / 'envs/main/bin/python'), 'drain': str(B / 'envs/main/bin/python'),
               'py38': str(B / 'envs/py38/bin/python')}
runner.PYTHONPATH = {'main': [str(B / 'src/RCAEval'), str(chung.ROOT / 'src')],
                     'drain': [str(chung.ROOT / 'src')],
                     'py38': [str(B / 'src/RCAEval'), str(chung.ROOT / 'src')]}
runner.TORAI_TT = B / 'data' / 'torai-TT'

import chay  # noqa: E402

if __name__ == '__main__':
    ten, method = sys.argv[1], sys.argv[2]
    # chay.main dùng runner.chay_luot với torai_tt mặc định đã gắn lúc định nghĩa hàm, nên truyền qua boc nhỏ
    goc = runner.chay_luot

    def boc(*a, **k):
        k.setdefault('torai_tt', runner.TORAI_TT)
        k.setdefault('repo_root', chung.ROOT)
        return goc(*a, **k)
    runner.chay_luot = boc
    chay.main(ten, method, 'all', seeds='0,1,2', hashseeds='0')
