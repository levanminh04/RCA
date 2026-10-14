"""T-032 TORAI B: tiến trình quan sát cho bước 'torai_run' (chạy bằng môi trường py38, tương thích Python 3.8).

Gọi đúng `p3.worker.main(job, out)` như đường native. Chỉ thêm việc đọc biến cục bộ của hàm `torai` lúc hàm trả về:
adapter (src/p3/adapters/torai.py) đã đặt `sys.setprofile(prof)` để lấy bốn biến; ở đây `sys.setprofile` được bọc để
hàm profile của adapter và hàm đọc thêm cùng chạy. Không đổi đối số, không đổi giá trị trả về, không đổi seed.
Kết quả `ket_qua` của lượt này phải trùng lượt native (driver so); nếu khác thì trung gian không được dùng.

python torai_obs_worker_py38.py <job.json> <ket-qua.json mới> <locals.json mới>
"""
import json
import sys

import numpy as np

NAMES = ('metric_ranks', 'log_ranks', 'trace_err_ranks', 'trace_lat_ranks', 'svc_metric_ranks', 'svc_log_ranks',
         'svc_trace_lat_ranks', 'svc_trace_err_ranks', 'm', 'service_list', 'bic_score_all', 'n_comp_opt', 'y_pred',
         'y_train', 'cluster_rank', 'has_traces')


def plain(value):
    import pandas as pd
    if isinstance(value, pd.DataFrame):
        return {'index': [str(i) for i in value.index], 'columns': [str(c) for c in value.columns],
                'values': value.to_numpy(dtype=float).tolist()}
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    return value


def main(job_path, out_path, locals_path):
    from torai import torai_sua as mod
    from p3 import worker
    state = {'torai_returns': 0, 'rcd_returns': []}
    code_t, code_r = mod.torai.__code__, mod._rcd_multimodal.__code__
    real_setprofile = sys.setprofile

    def mine(frame, event, arg):
        if event == 'return':
            if frame.f_code is code_t:
                state['torai_returns'] += 1
                state['locals'] = {k: plain(frame.f_locals.get(k)) for k in NAMES}
                state['locals_present'] = {k: (k in frame.f_locals) for k in NAMES}
            elif frame.f_code is code_r:
                state['rcd_returns'].append(plain(arg.get('ranks')) if isinstance(arg, dict) else None)

    def wrapped_setprofile(func):
        if func is None:
            return real_setprofile(None)

        def both(frame, event, arg):
            mine(frame, event, arg)
            return func(frame, event, arg)
        return real_setprofile(both)

    sys.setprofile = wrapped_setprofile
    try:
        worker.main(job_path, out_path)
    finally:
        sys.setprofile = real_setprofile
    with open(locals_path, 'x', encoding='utf-8') as stream:
        json.dump(state, stream, ensure_ascii=False, allow_nan=True)
    return 0


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
