r"""T-006: chạy tuần tự các khối của một luồng (SPEC mục "Bốn luồng"). Mỗi khối gọi chay_khoi.py trong tiến trình riêng.

Cách dùng (python của envs/py312):  python chay_luong.py <thu|L1|L2|L3|X1|GDN> [--song-song N] [--chi <tên khối> ...]
--song-song N (Minh duyệt 03/10/2026 cho L2, tối đa 3 RCD): chạy tối đa N khối cùng lúc, theo thứ tự danh sách. Khối có
thư mục làm việc mà chưa có file nén được coi là đang chạy ở tiến trình khác và tính vào N.
Nhật ký luồng: results/T-006/runs/luong-<tên>.log. Khối nào đã có file nén trong runs/ thì bỏ qua (chạy tiếp sau khi dừng).
Khối hỏng không chặn khối sau; mọi khối đều có file nén và log (luật cứng 10).
"""
import datetime as dt
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs"
EXT = Path(r"D:\RCA-ext")
PY312 = EXT / "envs/py312/Scripts/python.exe"
PY38RCD = EXT / "envs/py38-rcd/Scripts/python.exe"
PY38LOCK = EXT / "envs/py38-rcdlock/Scripts/python.exe"
PY312PIN = EXT / "envs/py312-pin/Scripts/python.exe"
PY38GDN = EXT / "envs/py38-gdn/Scripts/python.exe"
WORK = EXT / "work/T-006"
MAIN_RCAEVAL = EXT / "src/RCAEval/main.py"
MAIN_BARO = EXT / "src/baro/main.py"

TORAI_OB = f"data/torai-OB={EXT / 'data/torai-OB'}"
TORAI_SS = f"data/torai-SS={EXT / 'data/torai-SS'}"
RE1_OB = f"data/online-boutique={EXT / 'data/RE1-OB'}"
FSE_OB = f"data/fse-ob={EXT / 'data/fse-ob'}"
FSE_SS = f"data/fse-ss={EXT / 'data/fse-ss'}"


def khoi(ten, py, lien_ket, so_ca, args, script=MAIN_RCAEVAL):
    lk = [] if lien_ket is None else [lien_ket]
    return {"ten": ten, "py": str(py), "script": str(script), "lien_ket": lk, "so_ca": so_ca, "args": args}


def x1(env, py):
    """Các khối X1 cho một bộ thư viện (SPEC L4 ②)."""
    ks = [khoi(f"x1-{env}-vi-du-baro", py, None, 0, [], script=HERE / "vi_du_baro.py")]
    ks += [khoi(f"x1-{env}-reproduce-baro-fse-ob-{f}", py, FSE_OB, 0, ["--dataset", "OnlineBoutique", "--fault-type", f],
                script=MAIN_BARO) for f in ("cpu", "mem", "delay", "loss", "all")]
    ks += [khoi(f"x1-{env}-circa-torai-ob", py, TORAI_OB, 90, ["--method", "circa", "--dataset", "torai-ob", "--length", "10"])]
    return ks


LUONG = {
    "thu": [
        khoi("thu-torai-torai-ob", PY38RCD, TORAI_OB, 2, ["--method", "torai", "--dataset", "torai-ob", "--length", "10", "--test"]),
        khoi("thu-rcd-torai-ob", PY38RCD, TORAI_OB, 2, ["--method", "rcd", "--dataset", "torai-ob", "--length", "10", "--test"]),
    ],
    "L1": [khoi(f"torai-{ds}-lan{i}", PY38RCD, lk, 90, ["--method", "torai", "--dataset", ds, "--length", "10"])
           for ds, lk in (("torai-ob", TORAI_OB), ("torai-ss", TORAI_SS)) for i in (1, 2, 3)],
    "L2": [khoi(f"rcd-{ds}-lan{i}", PY38RCD, lk, 90, ["--method", "rcd", "--dataset", ds, "--length", "10"])
           for ds, lk in (("torai-ob", TORAI_OB), ("torai-ss", TORAI_SS)) for i in (1, 2, 3)],
    "X1": x1("py312", PY312) + x1("py312pin", PY312PIN),
    # L4 ④ ⑤ bằng bộ đã chốt ở X1 (py312-pin). lan2 = chạy lại cùng đầu vào để kiểm tất định.
    # CIRCA torai-OB lần này là lần chạy lại của khối X1 cùng bộ (x1-py312pin-circa-torai-ob).
    "L4": [khoi(f"l4-baro-{ds}-lan{i}", PY312PIN, lk, 90, ["--method", "baro", "--dataset", ds, "--length", "10"])
           for ds, lk in (("torai-ob", TORAI_OB), ("torai-ss", TORAI_SS)) for i in (1, 2)]
          + [khoi(f"l4-{m}-{ds}-lan{i}", PY312PIN, lk, 100, ["--method", m, "--dataset", ds], script=HERE / "chay_fse.py")
             for m in ("baro", "nsigma") for ds, lk in (("fse-ob", FSE_OB), ("fse-ss", FSE_SS)) for i in (1, 2)]
          + [khoi(f"l4-nsigma-phat-hien-{ds}-lan{i}", PY312PIN, lk, 200, ["--dataset", ds], script=HERE / "nsigma_phat_hien.py")
             for ds, lk in (("fse-ob", FSE_OB), ("fse-ss", FSE_SS)) for i in (1, 2)]
          + [khoi("l4-circa-torai-ob-lan2", PY312PIN, TORAI_OB, 90, ["--method", "circa", "--dataset", "torai-ob", "--length", "10"]),
             khoi("l4-circa-torai-ss-lan1", PY312PIN, TORAI_SS, 90, ["--method", "circa", "--dataset", "torai-ss", "--length", "10"]),
             khoi("l4-circa-fse-ob-lan1", PY312PIN, FSE_OB, 100, ["--method", "circa", "--dataset", "fse-ob"], script=HERE / "chay_fse.py"),
             khoi("l4-circa-fse-ss-lan1", PY312PIN, FSE_SS, 100, ["--method", "circa", "--dataset", "fse-ss"], script=HERE / "chay_fse.py")],
    # Phiên 2, Minh duyệt 03/10/2026 (LOG "Quyết định của Minh trong phiên 2"):
    # F10: khối ④ fse với --length 10 (mặc định của RCAEval tới 27/12/2024).
    "F10": [khoi(f"l4-{m}-{ds}-len10-lan{i}", PY312PIN, lk, 100, ["--method", m, "--dataset", ds, "--length", "10"],
                 script=HERE / "chay_fse.py")
            for m in ("baro", "nsigma") for ds, lk in (("fse-ob", FSE_OB), ("fse-ss", FSE_SS)) for i in (1, 2)]
           + [khoi(f"l4-circa-{ds}-len10-lan1", PY312PIN, lk, 100, ["--method", "circa", "--dataset", ds, "--length", "10"],
                   script=HERE / "chay_fse.py") for ds, lk in (("fse-ob", FSE_OB), ("fse-ss", FSE_SS))],
    # L3b: RCD trên RE1-OB với --length 10 (cấu hình lúc tác giả ghi đầu ra trong docs/SETUP.md), 3 lần song song.
    "L3b": [khoi(f"rcdlock-rcd-online-boutique-len10-lan{i}", PY38LOCK, RE1_OB, 125,
                 ["--method", "rcd", "--dataset", "online-boutique", "--length", "10"]) for i in (1, 2, 3)],
    # L2b: RCD trên torai với --length 20 (cấu hình baseline của bài TORAI), hàng đợi tối đa 3.
    "L2b": [khoi(f"rcd-{ds}-len20-lan{i}", PY38RCD, lk, 90, ["--method", "rcd", "--dataset", ds, "--length", "20"])
            for ds, lk in (("torai-ob", TORAI_OB), ("torai-ss", TORAI_SS)) for i in (1, 2, 3)],
    # T20: CIRCA ×1 và BARO lần 2 trên torai với --length 20 (lần 1 của BARO là khối soi-baro-<ds>-length20).
    "T20": [khoi(f"l4-baro-{ds}-len20-lan2", PY312PIN, lk, 90, ["--method", "baro", "--dataset", ds, "--length", "20"])
            for ds, lk in (("torai-ob", TORAI_OB), ("torai-ss", TORAI_SS))]
           + [khoi(f"l4-circa-{ds}-len20-lan1", PY312PIN, lk, 90, ["--method", "circa", "--dataset", ds, "--length", "20"])
              for ds, lk in (("torai-ob", TORAI_OB), ("torai-ss", TORAI_SS))],
    "GDN": [khoi(f"gdn-msl-lan{i}", PY38GDN, f"data/msl={EXT / 'src/GDN/data/msl'}", 0, [], script=HERE / "chay_gdn.py")
            for i in (1, 2)],
    "L3": [khoi("rcdlock-rcd-online-boutique-lan1", PY38LOCK, RE1_OB, 125, ["--method", "rcd", "--dataset", "online-boutique"])],
}


def lenh(k):
    cmd = [str(PY312), str(HERE / "chay_khoi.py"), "--ten", k["ten"], "--py", k["py"], "--script", k["script"],
           "--so-ca", str(k["so_ca"])]
    for lk in k["lien_ket"]:
        cmd += ["--lien-ket", lk]
    return cmd + ["--"] + k["args"]


def song_song(ds, n, ghi):
    import time
    xong = lambda k: (RUNS / f"{k['ten']}.tar.gz").exists()
    cua_toi = {}
    while True:
        for ten, (p, fo) in list(cua_toi.items()):
            if p.poll() is not None:
                fo.close()
                out = (RUNS / f"luong-khoi-{ten}.out").read_text(encoding="utf-8", errors="replace").strip()
                ghi(f"KHỐI {ten} xong rc={p.returncode}: {out[-1500:]}")
                del cua_toi[ten]
        ngoai = [k["ten"] for k in ds if not xong(k) and k["ten"] not in cua_toi and (WORK / k["ten"]).exists()]
        cho = [k for k in ds if not xong(k) and k["ten"] not in cua_toi and not (WORK / k["ten"]).exists()]
        if not cho and not cua_toi and not ngoai:
            return
        for k in cho[:max(0, n - len(cua_toi) - len(ngoai))]:
            fo = open(RUNS / f"luong-khoi-{k['ten']}.out", "w", encoding="utf-8")
            ghi(f"KHỐI {k['ten']} (song song; của tôi đang chạy {len(cua_toi)}, ở tiến trình khác {ngoai}): {' '.join(lenh(k))}")
            cua_toi[k["ten"]] = (subprocess.Popen(lenh(k), stdout=fo, stderr=subprocess.STDOUT), fo)
        time.sleep(10)


def main():
    # thứ tự tham số: <luồng> [--song-song N] [--chi tên ...]
    ten = sys.argv[1]
    chi = sys.argv[sys.argv.index("--chi") + 1:] if "--chi" in sys.argv else None
    n_ss = int(sys.argv[sys.argv.index("--song-song") + 1]) if "--song-song" in sys.argv else None
    log = open(RUNS / f"luong-{ten}.log", "a", encoding="utf-8")

    def ghi(m):
        log.write(f"[{dt.datetime.now():%Y-%m-%d %H:%M:%S}] {m}\n")
        log.flush()

    if n_ss:
        ghi(f"BAT-DAU luồng {ten}, song song tối đa {n_ss} khối")
        song_song([k for k in LUONG[ten] if not chi or k["ten"] in chi], n_ss, ghi)
        ghi(f"KẾT-THÚC luồng {ten}")
        return

    ghi(f"BAT-DAU luồng {ten}")
    for k in LUONG[ten]:
        if chi and k["ten"] not in chi:
            continue
        if (RUNS / f"{k['ten']}.tar.gz").exists():
            ghi(f"BỎ QUA {k['ten']}: đã có file nén")
            continue
        cmd = lenh(k)
        ghi(f"KHỐI {k['ten']}: {' '.join(cmd)}")
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        ghi(f"KHỐI {k['ten']} xong rc={r.returncode}: {r.stdout.strip()} {r.stderr.strip()[-2000:]}")
    ghi(f"KẾT-THÚC luồng {ten}")


if __name__ == "__main__":
    main()
