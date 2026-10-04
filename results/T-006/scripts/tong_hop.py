r"""T-006: tổng hợp kết quả các khối đã xong và so với mốc. Ghi results/T-006/cham/tong-hop.{json,txt}.

Cách dùng (python của envs/py312, có RCAEval): python tong_hop.py
- Chấm từng khối bằng cham.cham() (Evaluator của RCAEval, cách gộp như main.py), lưu cham/<khối>.json.
- Nhóm các lần chạy của cùng "phương pháp × dataset × bộ thư viện"; với mỗi ô: trung bình, nhỏ nhất, lớn nhất qua các lần.
- Tất định: đếm số ca có thứ hạng giống hệt lần 1.
- So mốc (moc.py): độ lệch = của mình − mốc, cho AC@1 (T1), AC@3 (T3), Avg@5 (A5) nếu mốc có.
Không đọc nhãn ngoài tên file kết quả (dùng để chấm).
"""
import json
import re
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cham as C  # noqa: E402
import moc as M  # noqa: E402

WORK = Path(r"D:\RCA-ext\work\T-006")
DATA = Path(r"D:\RCA-ext\data")
OUT = HERE.parent / "cham"
OUT.mkdir(exist_ok=True)

DS_ROOT = {"torai-ob": "torai-OB", "torai-ss": "torai-SS", "fse-ob": "fse-ob", "fse-ss": "fse-ss",
           "online-boutique": "RE1-OB"}


# Khối chẩn đoán phiên 2 được tính là lần 1 của nhóm --length 20 (Minh duyệt chạy lần 2 với tên l4-baro-<ds>-len20-lan2).
BI_DANH = {"soi-baro-torai-ss-length20": "l4-baro-torai-ss-len20-lan1", "soi-baro-torai-ob-length20": "l4-baro-torai-ob-len20-lan1"}


def nhan_dien(ten):
    """tên khối -> (nhóm, dataset, lần). Ví dụ rcd-torai-ob-lan2 -> ('rcd|torai-ob|py38-rcd', 'torai-ob', 2); main() ghép thêm '|len<N>'.
    Độ dài cửa sổ không lấy từ tên mà từ meta.json (hàm do_dai), rồi ghép vào khóa nhóm."""
    ten = BI_DANH.get(ten, ten)
    m = re.match(r"^(x1-(?P<envx>py312pin|py312)-|l4-|rcdlock-)?(?P<meth>[a-z-]+?)-(?P<ds>torai-ob|torai-ss|fse-ob|fse-ss|online-boutique)"
                 r"(-len(?P<len>\d+))?(-lan(?P<lan>\d))?$", ten)
    if not m:
        return None
    env = m.group("envx") or ("py312pin" if ten.startswith("l4-") else "py38-rcdlock" if ten.startswith("rcdlock-") else "py38-rcd")
    meth = m.group("meth")
    return f"{meth}|{m.group('ds')}|{env}", m.group("ds"), int(m.group("lan") or 1)


def do_dai(d):
    """--length lấy từ lệnh trong meta.json; không có thì 20 (mặc định của main.py 259ea41 và chay_fse.py)."""
    cmd = json.loads((d / "meta.json").read_text(encoding="utf-8"))["cmd"]
    return int(cmd[cmd.index("--length") + 1]) if "--length" in cmd else 20


def main():
    nhom = {}
    for d in sorted(WORK.iterdir()):
        if not (d / "meta.json").exists() or d.name.startswith(("thu-", "gdn-", "kiem-", "them-")) or "phat-hien" in d.name or d.name.endswith("-hong"):
            continue
        if "reproduce-baro" in d.name or "vi-du-baro" in d.name:
            continue
        nd = nhan_dien(d.name)
        if not nd:
            print("bỏ qua (không nhận ra tên):", d.name)
            continue
        key, ds, lan = nd
        key = f"{key}|len{do_dai(d)}"
        res = d / "output" / "results"
        out, kiem, per_case = C.cham(res, DATA / DS_ROOT[ds])
        so_sanh = None
        if (d / "stdout.log").exists() and "Avg@5-" in (d / "stdout.log").read_text(encoding="utf-8", errors="replace"):
            printed = C.doc_stdout(d / "stdout.log")
            so_sanh = all(printed.get(C.TEN_IN.get(m, m.upper())) == round(v["Avg5"], 2) for m, v in out.items() if m != "AVERAGE")
        ranks = {f.name: json.loads(f.read_text()) for f in sorted(res.glob("*.json"))}
        json.dump({"diem": out, "kiem": kiem, "khop_main_py": so_sanh}, open(OUT / f"{d.name}.json", "w"), ensure_ascii=False, indent=1)
        nhom.setdefault(key, []).append({"ten": d.name, "lan": lan, "diem": out, "kiem": kiem, "khop_main_py": so_sanh, "ranks": ranks})

    tong = {}
    lines = []
    for key, runs in sorted(nhom.items()):
        runs.sort(key=lambda r: (r["lan"], r["ten"]))
        meth, ds, env, ln = key.split("|")
        faults = [f for f in M.LOI6 if f in runs[0]["diem"]] + [f for f in ("cpu", "mem", "delay", "loss") if f in runs[0]["diem"] and f not in M.LOI6] + ["AVERAGE"]
        cells = {}
        for f in faults:
            for met in ("AC1", "AC3", "Avg5"):
                vals = [r["diem"][f][met] for r in runs if f in r["diem"]]
                cells[f"{f}.{met}"] = {"tb": st.mean(vals), "min": min(vals), "max": max(vals), "cac_lan": vals}
        base = runs[0]["ranks"]
        tat_dinh = [{"lan": r["lan"], "ten": r["ten"], "ca_giong_lan1": sum(base.get(k) == v for k, v in r["ranks"].items()), "so_ca": len(base)}
                    for r in runs[1:]]
        tong[key] = {"cac_khoi": [r["ten"] for r in runs], "o": cells, "tat_dinh": tat_dinh,
                     "kiem": {r["ten"]: {k: r["kiem"][k] for k in ("so_file", "file_error", "rank_rong", "trung_thu_tu_cot")} for r in runs},
                     "khop_main_py": {r["ten"]: r["khop_main_py"] for r in runs}}
        lines.append(f"== {key}: {len(runs)} lần {[r['ten'] for r in runs]}")
        lines.append(f"   khớp main.py: {[r['khop_main_py'] for r in runs]}; tất định: {tat_dinh}")
        lines.append(f"   dự phòng (trùng thứ tự cột): {[len(r['kiem']['trung_thu_tu_cot']) for r in runs]}; rỗng: {[len(r['kiem']['rank_rong']) for r in runs]}")
        hdr = f"   {'lỗi':8} {'AC@1 tb':>8} {'AC@3 tb':>8} {'Avg@5 tb':>9} {'Avg@5 min-max':>15}"
        lines.append(hdr)
        for f in faults:
            a1, a3, a5 = cells[f"{f}.AC1"], cells[f"{f}.AC3"], cells[f"{f}.Avg5"]
            lines.append(f"   {f:8} {a1['tb']:8.3f} {a3['tb']:8.3f} {a5['tb']:9.3f} {a5['min']:7.3f}-{a5['max']:.3f}")
    (OUT / "tong-hop.json").write_text(json.dumps(tong, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "tong-hop.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
