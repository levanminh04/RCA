r"""T-006: bảng so với mốc, từ cham/tong-hop.json (chạy tong_hop.py trước). Ghi cham/bang-so-sanh.md.

Mỗi bảng: một nhóm "phương pháp × dataset × bộ thư viện" so với một mốc. Ô của mình là trung bình các lần chạy;
cột "các lần" ghi Avg@5 từng lần; độ lệch = của mình − mốc. Không gõ số tay: mốc lấy từ moc.py.
Cách dùng: python bang_so_sanh.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import moc as M  # noqa: E402

T = json.loads((HERE.parent / "cham" / "tong-hop.json").read_text(encoding="utf-8"))

# (khóa nhóm, tiêu đề, kiểu mốc, mốc)
# kiểu "TAA": mốc (T1, T3, A5) theo LOI6 + AVERAGE (bài TORAI); "A5": chỉ Avg@5 (dict lỗi -> số)
SO = [
    ("torai|torai-ob|py38-rcd|len10", "TORAI, torai-OB, --length 10 — mốc A: docs/TORAI.md (chỉ Avg@5)", "A5", M.TORAI_MD),
    ("torai|torai-ob|py38-rcd|len10", "TORAI, torai-OB, --length 10 — mốc B: Bảng 2 bài TORAI, dòng Metric+Log+Trace", "TAA", M.TORAI_B2[("Metric+Log+Trace", "TORAI")]),
    ("torai|torai-ss|py38-rcd|len10", "TORAI, torai-SS, --length 10 — mốc B: Bảng 3 bài TORAI, dòng Metric+Log", "TAA", M.TORAI_B3[("Metric+Log", "TORAI")]),
    ("rcd|torai-ob|py38-rcd|len10", "RCD, torai-OB, --length 10 (SPEC) — mốc B: Bảng 2 bài TORAI, dòng Metric", "TAA", M.TORAI_B2[("Metric", "RCD")]),
    ("rcd|torai-ob|py38-rcd|len20", "RCD, torai-OB, --length 20 (Minh duyệt phiên 2) — mốc B: Bảng 2 bài TORAI, dòng Metric", "TAA", M.TORAI_B2[("Metric", "RCD")]),
    ("rcd|torai-ss|py38-rcd|len10", "RCD, torai-SS, --length 10 (SPEC) — mốc B: Bảng 3 bài TORAI, dòng Metric", "TAA", M.TORAI_B3[("Metric", "RCD")]),
    ("rcd|torai-ss|py38-rcd|len20", "RCD, torai-SS, --length 20 (Minh duyệt phiên 2) — mốc B: Bảng 3 bài TORAI, dòng Metric", "TAA", M.TORAI_B3[("Metric", "RCD")]),
    ("rcd|online-boutique|py38-rcdlock|len20", "RCD, RE1-OB, --length 20 (mặc định hiện tại; SPEC) — mốc A: docs/SETUP.md (1 lần)", "A5", M.SETUP_MD),
    ("rcd|online-boutique|py38-rcdlock|len10", "RCD, RE1-OB, --length 10 (mặc định lúc tác giả ghi mốc; Minh duyệt phiên 2) — mốc A: docs/SETUP.md (1 lần)", "A5", M.SETUP_MD),
    ("circa|torai-ob|py312pin|len10", "CIRCA, torai-OB, --length 10 — mốc B: Bảng 2 bài TORAI, dòng Metric", "TAA", M.TORAI_B2[("Metric", "CIRCA")]),
    ("circa|torai-ob|py312pin|len20", "CIRCA, torai-OB, --length 20 (Minh duyệt phiên 2) — mốc B: Bảng 2 bài TORAI, dòng Metric", "TAA", M.TORAI_B2[("Metric", "CIRCA")]),
    ("circa|torai-ob|py312|len10", "CIRCA, torai-OB, bộ py312 (X1), --length 10 — mốc B: Bảng 2 bài TORAI, dòng Metric", "TAA", M.TORAI_B2[("Metric", "CIRCA")]),
    ("circa|torai-ss|py312pin|len10", "CIRCA, torai-SS, --length 10 — mốc B: Bảng 3 bài TORAI, dòng Metric", "TAA", M.TORAI_B3[("Metric", "CIRCA")]),
    ("circa|torai-ss|py312pin|len20", "CIRCA, torai-SS, --length 20 (Minh duyệt phiên 2) — mốc B: Bảng 3 bài TORAI, dòng Metric", "TAA", M.TORAI_B3[("Metric", "CIRCA")]),
    ("baro|torai-ss|py312pin|len10", "BARO (RCAEval `baro`), torai-SS, --length 10 — mốc B: Bảng 3 bài TORAI, dòng Metric", "TAA", M.TORAI_B3[("Metric", "BARO")]),
    ("baro|torai-ss|py312pin|len20", "BARO (RCAEval `baro`), torai-SS, --length 20 — mốc B: Bảng 3 bài TORAI, dòng Metric", "TAA", M.TORAI_B3[("Metric", "BARO")]),
    ("baro|torai-ob|py312pin|len10", "BARO (RCAEval `baro`), torai-OB, --length 10 — không có mốc (dòng BARO Bảng 2 bị loại)", "KHONG", None),
    ("baro|torai-ob|py312pin|len20", "BARO (RCAEval `baro`), torai-OB, --length 20 — không có mốc (dòng BARO Bảng 2 bị loại)", "KHONG", None),
]
for _m, _ten in (("baro", "RobustScorer[t_inject]"), ("nsigma", "N-Sigma[t_inject]"), ("circa", "CIRCA[t_inject]")):
    for _ds in ("fse-ob", "fse-ss"):
        for _L, _ghi in (("10", "mặc định RCAEval tới 27/12/2024; Minh duyệt phiên 2"), ("20", "mặc định hiện tại; chạy ở phiên 1")):
            SO.append((f"{_m}|{_ds}|py312pin|len{_L}", f"{_m} (RCAEval), {_ds}, --length {_L} ({_ghi}) — mốc B: Bảng 3 bài BARO, {_ten}",
                       "A5", M.BARO_B3[_ds][_ten]))



def f2(x):
    return "—" if x is None else f"{x:.3f}"


def lech(a, b):
    return "—" if a is None or b is None else f"{a - b:+.3f}"


out = ["# Bảng so với mốc (tự sinh bởi scripts/bang_so_sanh.py từ cham/tong-hop.json)", ""]
for key, title, kieu, moc in SO:
    if key not in T:
        out += [f"## {title}", "", f"Chưa có kết quả (`{key}`).", ""]
        continue
    g = T[key]
    o = g["o"]
    faults = [k.split(".")[0] for k in o if k.endswith(".Avg5")]
    # REVIEW T-006 R2 (Minh duyệt 03/10/2026): nhóm có ít ca hơn số ca của mốc (khối bị dừng giữa chừng) thì không so
    # với mốc; ghi số ca từng ô. Số ca mong đợi mỗi loại lỗi: torai 15, fse 25, RE1-OB 25 (bằng nhau ở mọi dataset này).
    can = {"torai-ob": 15, "torai-ss": 15, "fse-ob": 25, "fse-ss": 25, "online-boutique": 25}[key.split("|")[1]]
    n_o = {}
    for ten in g["cac_khoi"]:
        d = json.loads((HERE.parent / "cham" / f"{ten}.json").read_text(encoding="utf-8"))["diem"]
        for f in faults:
            n_o.setdefault(f, set()).add(d[f]["n"])
    thieu = any(f != "AVERAGE" and min(v) < can for f, v in n_o.items())
    if thieu:
        out += [f"## {title}", "", f"**KHÔNG SO ĐƯỢC VỚI MỐC: nhóm chưa đủ ca** (khối bị dừng giữa chừng). Khối: {', '.join('`' + k + '`' for k in g['cac_khoi'])}. "
                f"Số ca mỗi ô (mong đợi {can} mỗi loại lỗi): " + ", ".join(f"{f} {sorted(v)}" for f, v in n_o.items()) + ".", "",
                "| lỗi | số ca | AC@1 mình | AC@3 mình | Avg@5 mình | Avg@5 các lần |", "|---|---|---|---|---|---|"]
        for f in faults:
            out.append(f"| {f} | {'/'.join(str(x) for x in sorted(n_o[f]))} | {f2(o[f'{f}.AC1']['tb'])} | {f2(o[f'{f}.AC3']['tb'])} | "
                       f"{f2(o[f'{f}.Avg5']['tb'])} | {', '.join(f2(v) for v in o[f'{f}.Avg5']['cac_lan'])} |")
        out.append("")
        continue
    out += [f"## {title}", "", f"Khối: {', '.join('`' + k + '`' for k in g['cac_khoi'])}. "
            f"Tất định (số ca giống hệt lần 1): {[(t['lan'], t['ca_giong_lan1'], t['so_ca']) for t in g['tat_dinh']] or 'một lần'}. "
            f"Dự phòng (trùng thứ tự cột): {[len(v['trung_thu_tu_cot']) for v in g['kiem'].values()]}. "
            f"Khớp `main.py`: {list(g['khop_main_py'].values())}.", ""]
    if kieu == "TAA":
        out += ["| lỗi | AC@1 mình | mốc T1 | lệch | AC@3 mình | mốc T3 | lệch | Avg@5 mình | mốc A5 | lệch | Avg@5 các lần |",
                "|---|---|---|---|---|---|---|---|---|---|---|"]
        for f in faults:
            m = moc.get(f)
            a1, a3, a5 = o[f"{f}.AC1"]["tb"], o[f"{f}.AC3"]["tb"], o[f"{f}.Avg5"]["tb"]
            out.append(f"| {f} | {f2(a1)} | {f2(m and m[0])} | {lech(a1, m and m[0])} | {f2(a3)} | {f2(m and m[1])} | {lech(a3, m and m[1])} "
                       f"| {f2(a5)} | {f2(m and m[2])} | {lech(a5, m and m[2])} | {', '.join(f2(v) for v in o[f'{f}.Avg5']['cac_lan'])} |")
    else:
        mm = moc or {}
        mm = {("AVERAGE" if k in ("AVG", "all") else k): v for k, v in mm.items()}
        if kieu == "A5" and "AVERAGE" not in mm and mm:
            mm["AVERAGE (trung bình các ô mốc)"] = sum(mm.values()) / len(mm)
        out += ["| lỗi | AC@1 mình | AC@3 mình | Avg@5 mình | mốc Avg@5 | lệch | Avg@5 các lần |", "|---|---|---|---|---|---|---|"]
        for f in faults:
            m = mm.get(f)
            if f == "AVERAGE" and m is None:
                m = mm.get("AVERAGE (trung bình các ô mốc)")
            a5 = o[f"{f}.Avg5"]["tb"]
            out.append(f"| {f} | {f2(o[f'{f}.AC1']['tb'])} | {f2(o[f'{f}.AC3']['tb'])} | {f2(a5)} | {f2(m)} | {lech(a5, m)} | "
                       f"{', '.join(f2(v) for v in o[f'{f}.Avg5']['cac_lan'])} |")
        if "AVERAGE (trung bình các ô mốc)" in mm:
            out.append("")
            out.append("Mốc này không có ô AVERAGE; dòng AVERAGE so với trung bình các ô mốc (số ca mỗi loại lỗi bằng nhau).")
    out.append("")
(HERE.parent / "cham" / "bang-so-sanh.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
