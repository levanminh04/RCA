r"""T-006 phiên 2: RCD torai-OB --length 20 bị dừng ở 3 giờ (Q-40), mỗi lần chỉ có 46/90 ca. So --length 20 với
--length 10 trên đúng tập ca chung đó (cùng ca ở cả 6 lần). Không so được với số bài TORAI (bài tính trên 90 ca).
Ghi: cham/rcd-torai-ob-len20-46ca.txt
Cách dùng (python của envs/py312): python rcd_len20_mot_phan.py
"""
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cham as C  # noqa: E402
from RCAEval.benchmark.evaluation import Evaluator  # noqa: E402
from RCAEval.classes.graph import Node  # noqa: E402

WORK = Path(r"D:\RCA-ext\work\T-006")
L20 = [f"rcd-torai-ob-len20-lan{i}" for i in (1, 2, 3)]
L10 = [f"rcd-torai-ob-lan{i}" for i in (1, 2, 3)]
sets = [{f.name for f in (WORK / k / "output" / "results").glob("*.json")} for k in L20]
chung = sorted(set.intersection(*sets))


def diem(khoi):
    per, tong = {}, Evaluator(max_k=5)
    for name in chung:
        s, m = name.split("_")[:2]
        ranks = json.loads((WORK / khoi / "output" / "results" / name).read_text())["0"]
        sr = C.service_ranks(ranks)
        per.setdefault(m, Evaluator(max_k=5)).add_case(ranks=sr, answer=Node(s, "unknown"))
        tong.add_case(ranks=sr, answer=Node(s, "unknown"))
    o = {m: e.average(5) for m, e in sorted(per.items())}
    o["AVERAGE"] = tong.average(5)
    o["AC1"], o["AC3"] = tong.accuracy(1), tong.accuracy(3)
    return o


lines = [f"Tập ca chung của 3 lần --length 20: {len(chung)} ca; giống nhau giữa 3 lần: {all(s == sets[0] for s in sets)}",
         f"Theo service: {dict(Counter(n.split('_')[0] for n in chung))}",
         f"Theo loại lỗi: {dict(Counter(n.split('_')[1] for n in chung))}", ""]
kq = {k: diem(k) for k in L20 + L10}
keys = [k for k in kq[L20[0]] if k not in ("AC1", "AC3")] + ["AC1", "AC3"]
lines.append(f"{'ô':8} {'len20 tb':>9} {'len20 các lần':>24} {'len10 tb':>9} {'len10 các lần':>24} {'chênh tb':>9}")
for k in keys:
    a, b = [kq[x][k] for x in L20], [kq[x][k] for x in L10]
    lines.append(f"{k:8} {st.mean(a):9.3f} {', '.join(f'{v:.3f}' for v in a):>24} {st.mean(b):9.3f} {', '.join(f'{v:.3f}' for v in b):>24} {st.mean(a) - st.mean(b):+9.3f}")
(HERE.parent / "cham" / "rcd-torai-ob-len20-46ca.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
