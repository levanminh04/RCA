r"""T-006: chấm lại từ file kết quả từng ca, theo đúng cách của main.py RCAEval (259ea41, dòng 470-560).

Cách dùng (python của envs/py312, có RCAEval):
    python cham.py <thư mục results chứa <service>_<fault>_<ca>.json> [--stdout <stdout.log của main.py>] [--json <file ra>]

- Ánh xạ thứ hạng về service như main.py: x.split("_")[0].replace("-db", ""), bỏ trùng giữ thứ tự.
- Đáp án: service lấy từ tên file kết quả (chỉ dùng để chấm, không đưa vào phương pháp).
- In AC@1, AC@3, Avg@5 mức service cho từng loại lỗi và AVERAGE (trung bình trên mọi ca).
- Nếu có --stdout: so Avg@5 từng loại lỗi (làm tròn 2 chữ số) với số main.py in ra. Lệch thì in "LỆCH".
- Phép kiểm không cần nhãn: thứ hạng rỗng, file "error"; với --data-root: ca có thứ hạng trùng thứ tự cột của file
  dữ liệu (dấu hiệu nhánh dự phòng của wrapper @rca, trả `data.columns`), so theo thứ tự xuất hiện trong dòng tiêu đề.
"""
import argparse
import json
import re
from collections import defaultdict
from os.path import basename
from pathlib import Path

from RCAEval.benchmark.evaluation import Evaluator
from RCAEval.classes.graph import Node

# main.py: tên nhóm lỗi khi in -> mã lỗi trong tên file
TEN_IN = {"cpu": "CPU", "mem": "MEM", "disk": "DISK", "socket": "SOCKET", "delay": "DELAY", "loss": "LOSS"}


def service_ranks(ranks):
    s = [Node(x.split("_")[0].replace("-db", ""), "unknown") for x in ranks]
    return [s[0]] + [s[i] for i in range(1, len(s)) if s[i] not in s[:i]] if s else []


def header_cols(data_root, rp_name):
    """Dòng tiêu đề của file dữ liệu của ca (đổi _latency-90 -> _latency như main.py)."""
    s, m, case = rp_name[:-5].split("_")[:3]
    d = Path(data_root) / f"{s}_{m}" / case
    # fse-*: đầu vào là simple_data.csv (chay_fse.py); nơi khác theo thứ tự main.py tìm file
    order = ("simple_data.csv",) if "fse-" in str(data_root) else ("data.csv", "simple_metrics.csv", "simple_data.csv")
    for fn in order:
        if (d / fn).exists():
            cols = (d / fn).open(encoding="utf-8").readline().strip().split(",")
            return [c.replace("_latency-90", "_latency") for c in cols]
    return None


def trung_thu_tu_cot(ranks, cols):
    if not cols or len(ranks) < 3:
        return False
    pos = {c: i for i, c in enumerate(cols)}
    idx = [pos.get(r) for r in ranks]
    if any(i is None for i in idx):
        return False
    return all(a < b for a, b in zip(idx, idx[1:]))


def cham(res_dir, data_root=None):
    per_fault = defaultdict(lambda: Evaluator(max_k=5))
    all_ev = Evaluator(max_k=5)
    kiem = {"so_file": 0, "file_error": [], "rank_rong": [], "do_dai_rank": [], "trung_thu_tu_cot": []}
    per_case = {}
    for rp in sorted(Path(res_dir).glob("*.json")):
        s, m = basename(rp).split("_")[:2]
        data = json.loads(rp.read_text())
        kiem["so_file"] += 1
        if "error" in data:
            kiem["file_error"].append(rp.name)
            continue
        for _, ranks in data.items():
            if not ranks:
                kiem["rank_rong"].append(rp.name)
            if data_root and trung_thu_tu_cot(ranks, header_cols(data_root, rp.name)):
                kiem["trung_thu_tu_cot"].append(rp.name)
            kiem["do_dai_rank"].append(len(ranks))
            sr = service_ranks(ranks)
            ans = Node(s, "unknown")
            per_fault[m].add_case(ranks=sr, answer=ans)
            all_ev.add_case(ranks=sr, answer=ans)
            pos = next((i + 1 for i, n in enumerate(sr) if n.entity == s), None)
            per_case[rp.name] = {"vi_tri_dung": pos, "top5": [n.entity for n in sr[:5]]}
    out = {}
    for m, ev in sorted(per_fault.items()):
        out[m] = {"n": ev.num, "AC1": ev.accuracy(1), "AC3": ev.accuracy(3), "Avg5": ev.average(5)}
    out["AVERAGE"] = {"n": all_ev.num, "AC1": all_ev.accuracy(1), "AC3": all_ev.accuracy(3), "Avg5": all_ev.average(5)}
    lens = kiem["do_dai_rank"]
    kiem["do_dai_rank"] = {"min": min(lens), "max": max(lens)} if lens else None
    return out, kiem, per_case


def doc_stdout(path):
    vals = {}
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        mm = re.match(r"Avg@5-([A-Z]+):\s+([0-9.]+)", line.strip())
        if mm:
            vals[mm.group(1)] = float(mm.group(2))
    return vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("res_dir")
    ap.add_argument("--stdout")
    ap.add_argument("--json")
    ap.add_argument("--data-root", help="thư mục dataset, để kiểm thứ hạng trùng thứ tự cột")
    a = ap.parse_args()
    out, kiem, per_case = cham(a.res_dir, a.data_root)
    print(f"{'lỗi':8} {'n':>3} {'AC@1':>6} {'AC@3':>6} {'Avg@5':>6}")
    for m, v in out.items():
        print(f"{m:8} {v['n']:>3} {v['AC1']:6.3f} {v['AC3']:6.3f} {v['Avg5']:6.3f}")
    print("kiểm không cần nhãn:", json.dumps({k: kiem[k] for k in ("so_file", "file_error", "rank_rong", "do_dai_rank", "trung_thu_tu_cot")}, ensure_ascii=False))
    so_sanh = None
    if a.stdout:
        printed = doc_stdout(a.stdout)
        so_sanh = {}
        for m, v in out.items():
            if m == "AVERAGE":
                continue
            key = TEN_IN.get(m, m.upper())
            mine = round(v["Avg5"], 2)
            so_sanh[m] = {"main_py": printed.get(key), "cham_py": mine, "khop": printed.get(key) == mine}
        extra = set(printed) - {TEN_IN.get(m, m.upper()) for m in out}
        ok = all(x["khop"] for x in so_sanh.values()) and not extra
        print("so với main.py:", "KHỚP" if ok else "LỆCH", json.dumps(so_sanh, ensure_ascii=False), "thừa:", sorted(extra))
    if a.json:
        Path(a.json).write_text(json.dumps({"diem": out, "kiem": kiem, "so_sanh_main_py": so_sanh, "tung_ca": per_case},
                                           ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
