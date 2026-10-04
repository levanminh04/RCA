"""T-005: điều phối đo. Chạy bằng môi trường py312 (có psutil).

Mỗi lượt: một tiến trình con chạy `chay_mot_luot.py` trong đúng môi trường, giới hạn 1 giờ (SPEC bước 6).
Đo ở tiến trình cha: tổng thời gian (time.perf_counter) và RSS đỉnh của cây tiến trình con (psutil, lấy mẫu 0,1 s).
Chặn an toàn: dừng nếu RSS > 12 GB (máy 16 GB), ghi là "dừng vì RAM".

Mỗi lượt ghi log riêng ở results/T-005/runs/do-<muc>-<bien_the>-lan<N>.log (giữ cả lượt hỏng, luật cứng 10)
và thêm một dòng vào results/T-005/runs/ket-qua-do.jsonl.

Dùng: py312\\Scripts\\python.exe do.py <muc>[:<bien_the>] ...
"""
import datetime
import json
import os
import subprocess
import sys
import time

import psutil

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(os.path.dirname(HERE), "runs")
CHILD = os.path.join(HERE, "chay_mot_luot.py")
ENVS = {
    "py312": r"D:\RCA-ext\envs\py312\Scripts\python.exe",
    "py38-rcd": r"D:\RCA-ext\envs\py38-rcd\Scripts\python.exe",
    "py38-gdn": r"D:\RCA-ext\envs\py38-gdn\Scripts\python.exe",
}
MUC_ENV = {
    "baro": "py312", "nsigma": "py312", "circa": "py312", "microrank": "py312", "tracerca": "py312",
    "bocpd": "py312", "nsigma_phat_hien": "py312",
    "rcd": "py38-rcd", "torai": "py38-rcd",
    "gdn_hoc": "py38-gdn", "gdn_suy_luan": "py38-gdn",
}
TIMEOUT_S = 3600
RAM_GUARD_MB = 12 * 1024


def tree_rss_mb(p):
    try:
        procs = [p] + p.children(recursive=True)
    except psutil.NoSuchProcess:
        return 0.0
    s = 0
    for q in procs:
        try:
            s += q.memory_info().rss
        except psutil.Error:
            pass
    return s / 2 ** 20


def one(muc, bien_the):
    env = MUC_ENV[muc]
    n = 1
    while os.path.exists(os.path.join(RUNS, "do-%s-%s-lan%d.log" % (muc, bien_the, n))):
        n += 1
    nhan = "%s-%s-lan%d" % (muc, bien_the, n)
    log_path = os.path.join(RUNS, "do-%s.log" % nhan)
    vm = psutil.virtual_memory()
    rec = {"muc": muc, "bien_the": bien_the, "lan": n, "env": env,
           "bat_dau": datetime.datetime.now().isoformat(timespec="seconds"),
           "ram_trong_truoc_mb": round(vm.available / 2 ** 20), "cpu_logic": psutil.cpu_count()}
    with open(log_path, "w", encoding="utf-8") as log:
        log.write("# %s\n" % json.dumps(rec, ensure_ascii=False))
        log.flush()
        envv = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8")
        t0 = time.perf_counter()
        proc = subprocess.Popen([ENVS[env], CHILD, "--muc", muc, "--bien_the", bien_the, "--nhan", nhan],
                                stdout=log, stderr=subprocess.STDOUT, env=envv)
        p = psutil.Process(proc.pid)
        peak, status = 0.0, None
        while True:
            rc = proc.poll()
            if rc is not None:
                status = "xong" if rc == 0 else "loi (exit %d)" % rc
                break
            peak = max(peak, tree_rss_mb(p))
            el = time.perf_counter() - t0
            if el > TIMEOUT_S:
                status = "> 1 gio (dung)"
            elif peak > RAM_GUARD_MB:
                status = "dung vi RAM > 12 GB"
            if status:
                for q in p.children(recursive=True) + [p]:
                    try:
                        q.kill()
                    except psutil.Error:
                        pass
                proc.wait()
                break
            time.sleep(0.1)
        wall = time.perf_counter() - t0
    rec.update({"trang_thai": status, "tong_s": round(wall, 2), "rss_dinh_mb_cha": round(peak, 1)})
    with open(log_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("KET_QUA "):
                rec.update(json.loads(line[len("KET_QUA "):]))
    with open(log_path, "a", encoding="utf-8") as log:
        log.write("\n# TONG_KET %s\n" % json.dumps(rec, ensure_ascii=False))
    with open(os.path.join(RUNS, "ket-qua-do.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        muc, _, bt = arg.partition(":")
        one(muc, bt or "full")
