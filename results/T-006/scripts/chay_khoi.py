r"""T-006: chạy một khối "phương pháp × dataset × lần" bằng đúng lệnh của tác giả, trong thư mục làm việc riêng.

Cách dùng (chạy bằng python của envs/py312, vì cần psutil):
    envs/py312/Scripts/python.exe chay_khoi.py --ten <tên khối> --py <python của môi trường> \
        --script <main.py của tác giả> [--lien-ket data/torai-OB=D:/RCA-ext/data/torai-OB ...] \
        [--so-ca N] -- <tham số cho main.py>

Việc script làm:
- Tạo D:\RCA-ext\work\T-006\<tên khối>\ (dừng nếu đã có, để không lẫn kết quả cũ: main.py chấm mọi file trong output/).
- Tạo liên kết thư mục (junction) cho dữ liệu, vì main.py đọc data/<tên> và ghi output/ theo thư mục hiện tại.
- Đặt OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1 (SPEC: 4 luồng không tranh CPU).
- Chạy lệnh, stdout/stderr ghi ra file. Mỗi 1 s xem output/results/*.json: file mới = một ca xong (main.py ghi
  file ngay sau mỗi ca), ghi mtime của file (lúc ca xong) và số giây từ ca trước vào tien-do.log (SL25).
  Ca đầu tính từ lúc khởi động tiến trình, nên gồm cả thời gian nạp thư viện.
- Mỗi 60 s ghi RAM trống và RSS của tiến trình; RAM trống < 3 GB thì ghi dòng CANH-BAO-RAM.
- Quá 3 giờ (Q-40) thì dừng tiến trình, ghi VUOT-NGAN-SACH.
- Xong thì ghi meta.json và nén thư mục làm việc (trừ liên kết dữ liệu) vào results/T-006/runs/<tên khối>.tar.gz.
Script không đọc nhãn, không đổi lệnh của tác giả.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

import psutil

WORK_ROOT = Path(r"D:\RCA-ext\work\T-006")
RUNS = Path(__file__).resolve().parent.parent / "runs"
NGAN_SACH_S = 3 * 3600
RAM_SAN_B = 3 * 1024**3


def bay_gio():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ten", required=True)
    ap.add_argument("--py", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--lien-ket", action="append", default=[], help="duong_dan_tuong_doi=dich")
    ap.add_argument("--so-ca", type=int, default=None, help="số ca dự kiến, chỉ để ghi tiến độ")
    ap.add_argument("--ngan-sach-s", type=int, default=NGAN_SACH_S)
    ap.add_argument("rest", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd_args = a.rest[1:] if a.rest and a.rest[0] == "--" else a.rest

    wd = WORK_ROOT / a.ten
    if wd.exists() and any(wd.iterdir()):
        sys.exit(f"{wd} đã có nội dung; không chạy đè (luật cứng 10: giữ mọi lượt)")
    wd.mkdir(parents=True, exist_ok=True)
    for lk in a.lien_ket:
        rel, target = lk.split("=", 1)
        link = wd / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(Path(target))], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"mklink lỗi: {r.stdout} {r.stderr}")

    env = dict(os.environ)
    env.update({"OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
                "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"})
    cmd = [a.py, a.script] + cmd_args
    tien_do = open(wd / "tien-do.log", "a", encoding="utf-8")

    def ghi(msg):
        tien_do.write(f"[{bay_gio()}] {msg}\n")
        tien_do.flush()

    meta = {"ten": a.ten, "cmd": cmd, "cwd": str(wd), "lien_ket": a.lien_ket,
            "env_threads": {k: env[k] for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")},
            "bat_dau": bay_gio()}
    ghi(f"BAT-DAU cmd={cmd} cwd={wd}")
    t0 = time.time()
    with open(wd / "stdout.log", "w", encoding="utf-8") as fo, open(wd / "stderr.log", "w", encoding="utf-8") as fe:
        p = subprocess.Popen(cmd, cwd=wd, env=env, stdout=fo, stderr=fe)
        proc = psutil.Process(p.pid)
        seen, t_prev, last_ram, trang_thai = set(), t0, 0.0, None
        res_dir = wd / "output" / "results"
        while True:
            rc = p.poll()
            if res_dir.exists():
                new = sorted(set(os.listdir(res_dir)) - seen)
                # thời điểm xong của ca = mtime của file kết quả (main.py ghi file ngay sau mỗi ca);
                # thời điểm bắt đầu ca = thời điểm xong của ca trước (main.py chạy tuần tự)
                new.sort(key=lambda f: os.stat(res_dir / f).st_mtime)
                for f in new:
                    mt = os.stat(res_dir / f).st_mtime
                    seen.add(f)
                    ghi(f"CA-XONG {len(seen)}/{a.so_ca or '?'} {f} bat_dau {dt.datetime.fromtimestamp(t_prev):%H:%M:%S.%f} "
                        f"xong {dt.datetime.fromtimestamp(mt):%H:%M:%S.%f} = {mt - t_prev:.2f}s (tổng {mt - t0:.0f}s)")
                    t_prev = mt
            now = time.time()
            if now - last_ram >= 60 or rc is not None:
                last_ram = now
                vm = psutil.virtual_memory()
                try:
                    rss = proc.memory_info().rss + sum(c.memory_info().rss for c in proc.children(recursive=True))
                except psutil.Error:
                    rss = -1
                ghi(f"RAM trống {vm.available / 1024**3:.2f} GB; RSS tiến trình {rss / 1024**2:.0f} MB")
                if vm.available < RAM_SAN_B:
                    ghi("CANH-BAO-RAM: RAM trống dưới 3 GB")
            if rc is not None:
                trang_thai = f"XONG rc={rc}"
                break
            if now - t0 > a.ngan_sach_s:
                for c in proc.children(recursive=True):
                    c.kill()
                p.kill()
                p.wait()
                trang_thai = f"VUOT-NGAN-SACH sau {now - t0:.0f}s"
                break
            time.sleep(1)
    t1 = time.time()
    ghi(f"{trang_thai}; {len(seen)} file kết quả; {t1 - t0:.0f}s")
    meta.update({"ket_thuc": bay_gio(), "giay": round(t1 - t0, 1), "trang_thai": trang_thai,
                 "so_file_ket_qua": len(seen), "returncode": p.returncode})
    (wd / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    tien_do.close()

    # nén, bỏ các liên kết dữ liệu (không đi vào junction)
    skip_raw = {wd / lk.split("=", 1)[0] for lk in a.lien_ket}
    RUNS.mkdir(parents=True, exist_ok=True)
    with tarfile.open(RUNS / f"{a.ten}.tar.gz", "w:gz") as tar:
        for root, dirs, files in os.walk(wd):
            rp = Path(root)
            dirs[:] = [d for d in dirs if (rp / d) not in skip_raw and not os.path.isjunction(rp / d)]
            for f in files:
                tar.add(rp / f, arcname=str((rp / f).relative_to(wd.parent)))
    print(f"{a.ten}: {trang_thai}; {len(seen)} file; {t1 - t0:.0f}s; nén vào {RUNS / (a.ten + '.tar.gz')}")


if __name__ == "__main__":
    main()
