"""T-016 S11 (điểm mở 3 của T-006): chấm RCD torai-OB cửa sổ 20 trên EC2 (90 ca, seed 0) và so với 3 lần chạy của
T-006 trên laptop (46 ca chung). Chấm bằng Evaluator của RCAEval như main.py. Nhãn chỉ để chấm.
Chạy bằng py312-pin. Cách dùng: python so_rcd_46ca.py <thư mục EC2 seed0> <thư mục chứa lan1..3 của T-006> <meta.jsonl EC2>"""
import json
import statistics as st
import sys
from pathlib import Path

from RCAEval.benchmark.evaluation import Evaluator
from RCAEval.classes.graph import Node


def doc(d):
    return {p.stem: json.loads(p.read_text())["0"] for p in Path(d).glob("*.json")
            if not p.name.endswith("_failed.json") and p.name != "lenh.json"}


def diem(ds, cas):
    ev = Evaluator(max_k=5)
    for c in cas:
        s = [Node(x.split("_")[0].replace("-db", ""), "unknown") for x in ds[c]]
        s = [s[0]] + [s[i] for i in range(1, len(s)) if s[i] not in s[:i]] if s else []
        ev.add_case(ranks=s, answer=Node(c.split("_")[0], "unknown"))
    return round(ev.average(5), 4), round(ev.accuracy(1), 4), round(ev.accuracy(3), 4)


ec2 = doc(sys.argv[1])
t6 = [doc(next(Path(sys.argv[2]).glob(f"lan{k}/*/output/results"))) for k in (1, 2, 3)]
chung = sorted(set(t6[0]) & set(ec2))
print(f"EC2 90 ca (Avg5, AC1, AC3): {diem(ec2, sorted(ec2))}")
print(f"46 ca chung: EC2 {diem(ec2, chung)}; T-006 lần 1..3 {[diem(t, chung) for t in t6]}; "
      f"T-006 TB Avg5 {st.mean(diem(t, chung)[0] for t in t6):.4f}")
rieng = sorted(set(ec2) - set(chung))
print(f"44 ca chỉ EC2 chạy: {diem(ec2, rieng)}")
meta = [json.loads(l) for l in open(sys.argv[3], encoding="utf-8")]
lau = sorted(meta, key=lambda m: -m["giay"])[:5]
print("5 ca lâu nhất (giây):", [(m["ca"], round(m["giay"], 1), m["kich_thuoc"]) for m in lau])
print("thời gian 46 ca chung trên EC2:", round(sum(m["giay"] for m in meta if m["ca"] in chung)), "s; 44 ca còn lại:",
      round(sum(m["giay"] for m in meta if m["ca"] not in chung)), "s")
