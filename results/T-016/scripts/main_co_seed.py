r"""T-016 S3(a): chạy main.py của RCAEval NGUYÊN VĂN (runpy), chỉ chèn np.random.seed(seed) trước mỗi lời gọi
phương pháp, để so với harness chay_torai.py cùng seed.

Cách dùng (trong thư mục làm việc có data/<dataset> là liên kết tới dữ liệu):
    python main_co_seed.py <seed> <đường dẫn main.py> --method torai --dataset torai-ob --length 10
Chạy bằng python của py38-rcdlock.
"""
import runpy
import sys

import numpy as np

seed = int(sys.argv[1])
main_path = sys.argv[2]
sys.argv = [main_path] + sys.argv[3:]
import RCAEval.e2e as e2e  # noqa: E402

for ten in ("torai", "rcd"):
    goc = getattr(e2e, ten)

    def boc(*a, _goc=goc, **k):
        np.random.seed(seed)
        return _goc(*a, **k)

    setattr(e2e, ten, boc)
runpy.run_path(main_path, run_name="__main__")
