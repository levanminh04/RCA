r"""T-006 L3: chạy main.py của RCAEval nguyên văn (runpy, __name__ == "__main__"), rồi kiểm `tigramite` có bị nạp không.

Minh yêu cầu (03/10/2026): sau `main.py --test` thì 'tigramite' không có trong sys.modules, để chắc việc bỏ tigramite
khỏi lock không đụng tới đường chạy RCD.
Cách dùng: <python py38-rcdlock> main_kiem_module.py <tham số main.py ...>
"""
import runpy
import sys

MAIN = r"D:\RCA-ext\src\RCAEval\main.py"
sys.argv = [MAIN] + sys.argv[1:]
try:
    runpy.run_path(MAIN, run_name="__main__")
finally:
    nap = sorted(m for m in sys.modules if m == "tigramite" or m.startswith("tigramite."))
    print(f"KIEM-MODULE: 'tigramite' trong sys.modules = {'tigramite' in sys.modules}; các module tigramite đã nạp: {nap}")
    print(f"KIEM-MODULE: causallearn SkeletonDiscovery nạp từ {getattr(sys.modules.get('causallearn.utils.PCUtils.SkeletonDiscovery'), '__file__', None)}")
