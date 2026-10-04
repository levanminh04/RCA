r"""T-006 phiên 2, yêu cầu 2 của Minh: các ca CIRCA rơi vào nhánh dự phòng của wrapper @rca, và ảnh hưởng lên điểm.

Với mỗi khối CIRCA:
- Đọc stderr.log: mỗi dòng "circa failed (<lỗi>)" đứng sau thanh tiến độ "k/N", tức ca thứ k+1 (đếm từ 1) theo thứ tự
  xử lý bị lỗi. Thứ tự xử lý dựng lại đúng như main.py (sorted(glob(<dataset>/**/simple_metrics.csv)), torai) hoặc
  chay_fse.py (sorted(glob(data/<dataset>/**/simple_data.csv))), chạy glob trong chính thư mục làm việc của khối.
- Đối chiếu với phép kiểm không cần nhãn của cham.py (thứ hạng trùng thứ tự cột của file dữ liệu).
- Tính AC@1, AC@3, Avg@5 mức service theo từng loại lỗi hai cách: giữ ca dự phòng (như main.py chấm) và bỏ ca đó.
Ghi: cham/circa-du-phong.txt, cham/circa-du-phong.json.
Cách dùng (python của envs/py312): python ca_du_phong_circa.py
"""
import glob
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cham as C  # noqa: E402

from RCAEval.benchmark.evaluation import Evaluator  # noqa: E402
from RCAEval.classes.graph import Node  # noqa: E402

WORK = Path(r"D:\RCA-ext\work\T-006")
DATA = Path(r"D:\RCA-ext\data")
KHOI = {
    "x1-py312-circa-torai-ob": ("torai", "torai-OB"),
    "x1-py312pin-circa-torai-ob": ("torai", "torai-OB"),
    "l4-circa-torai-ob-lan2": ("torai", "torai-OB"),
    "l4-circa-torai-ss-lan1": ("torai", "torai-SS"),
    "l4-circa-fse-ob-lan1": ("fse", "fse-ob"),
    "l4-circa-fse-ss-lan1": ("fse", "fse-ss"),
    # phiên 2, cấu hình cửa sổ Minh duyệt
    "l4-circa-torai-ob-len20-lan1": ("torai", "torai-OB"),
    "l4-circa-torai-ss-len20-lan1": ("torai", "torai-SS"),
    "l4-circa-fse-ob-len10-lan1": ("fse", "fse-ob"),
    "l4-circa-fse-ss-len10-lan1": ("fse", "fse-ss"),
}


def thu_tu_xu_ly(khoi, kieu, ds):
    cwd = os.getcwd()
    os.chdir(WORK / khoi)
    try:
        if kieu == "torai":
            dataset = f"data/{ds}"
            ps = list(glob.glob(os.path.join(dataset, "**/data.csv"), recursive=True))
            if not ps:
                ps = list(glob.glob(os.path.join(dataset, "**/simple_metrics.csv"), recursive=True))
            ps = sorted(ps)
        else:
            ps = sorted(glob.glob(os.path.join("data", ds, "**", "simple_data.csv"), recursive=True))
    finally:
        os.chdir(cwd)
    out = []
    for p in ps:
        parts = Path(p).parts
        out.append(f"{parts[-3]}_{parts[-2]}.json")
    return out


def diem(res_dir, bo=()):
    per, tong = {}, Evaluator(max_k=5)
    for rp in sorted(Path(res_dir).glob("*.json")):
        if rp.name in bo:
            continue
        s, m = rp.name.split("_")[:2]
        for _, ranks in json.loads(rp.read_text()).items():
            sr = C.service_ranks(ranks)
            per.setdefault(m, Evaluator(max_k=5)).add_case(ranks=sr, answer=Node(s, "unknown"))
            tong.add_case(ranks=sr, answer=Node(s, "unknown"))
    o = {m: {"n": e.num, "AC1": e.accuracy(1), "AC3": e.accuracy(3), "Avg5": e.average(5)} for m, e in sorted(per.items())}
    o["AVERAGE"] = {"n": tong.num, "AC1": tong.accuracy(1), "AC3": tong.accuracy(3), "Avg5": tong.average(5)}
    return o


rep, lines = {}, []
for khoi, (kieu, ds) in KHOI.items():
    se = (WORK / khoi / "stderr.log").read_text(encoding="utf-8", errors="replace")
    order = thu_tu_xu_ly(khoi, kieu, ds)
    loi = []
    for m in re.finditer(r"(\d+)/(\d+) \[[^\]]*\](\w+) failed \(([^)]*)\)", se):
        k = int(m.group(1))
        loi.append({"vi_tri": k + 1, "ca": order[k], "loi": m.group(4)})
    _, kiem, _ = C.cham(WORK / khoi / "output" / "results", DATA / ds)
    ca_loi = [x["ca"] for x in loi]
    giu, bo = diem(WORK / khoi / "output" / "results"), diem(WORK / khoi / "output" / "results", bo=set(ca_loi))
    # thứ hạng của ca dự phòng: service đúng ở vị trí nào (để thấy ca đó tính đúng hay sai)
    vt = {}
    for c in ca_loi:
        ranks = json.loads((WORK / khoi / "output" / "results" / c).read_text())["0"]
        sr = [n.entity for n in C.service_ranks(ranks)]
        vt[c] = sr.index(c.split("_")[0]) + 1 if c.split("_")[0] in sr else None
    rep[khoi] = {"so_ca_xu_ly": len(order), "ca_loi_theo_stderr": loi, "ca_trung_thu_tu_cot": kiem["trung_thu_tu_cot"],
                 "khop_hai_cach_phat_hien": sorted(ca_loi) == sorted(kiem["trung_thu_tu_cot"]),
                 "vi_tri_service_dung_trong_thu_hang_du_phong": vt, "giu": giu, "bo": bo}
    lines.append(f"== {khoi} ({len(order)} ca)")
    for x in loi:
        lines.append(f"   ca {x['ca']} (thứ {x['vi_tri']}): {x['loi']}; service đúng đứng thứ {vt[x['ca']]} trong thứ hạng dự phòng")
    if not loi:
        lines.append("   không ca nào rơi vào nhánh dự phòng")
    lines.append(f"   phép kiểm trùng thứ tự cột: {kiem['trung_thu_tu_cot']}; khớp stderr: {rep[khoi]['khop_hai_cach_phat_hien']}")
    if loi:
        lines.append(f"   {'lỗi':8} {'n giữ':>5} {'Avg@5 giữ':>9} {'n bỏ':>5} {'Avg@5 bỏ':>9} {'chênh':>7} | {'AC@1 giữ':>8} {'AC@1 bỏ':>8} | {'AC@3 giữ':>8} {'AC@3 bỏ':>8}")
        for f in giu:
            g, b = giu[f], bo.get(f)
            lines.append(f"   {f:8} {g['n']:>5} {g['Avg5']:9.3f} {b['n']:>5} {b['Avg5']:9.3f} {b['Avg5'] - g['Avg5']:+7.3f} | "
                         f"{g['AC1']:8.3f} {b['AC1']:8.3f} | {g['AC3']:8.3f} {b['AC3']:8.3f}")
(HERE.parent / "cham" / "circa-du-phong.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE.parent / "cham" / "circa-du-phong.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
