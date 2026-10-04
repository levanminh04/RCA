"""T-016 S8 (sửa theo REVIEW R2): soi phép thử giả (placebo).
Thứ hạng được gộp về service ĐÚNG như phép chấm chính (results/T-006/scripts/cham.py, main.py:560-572):
x.split("_")[0].replace("-db", ""), bỏ trùng giữ thứ tự. Với mỗi ca, so hạng của service gốc THẬT với hạng của
các service gốc KHÁC của cùng dataset (5 service bị tiêm). Nếu gốc thật không đứng cao hơn gốc khác thì mức trên may
rủi (nếu có) là do thiên lệch theo service, không do dấu vết lỗi trong cửa sổ giả. Mốc may rủi: xếp đều trên danh
sách service SAU KHI gộp, tính theo từng ca rồi lấy trung bình (AC@1 = 1/n, Avg@5 = 3/n với n ≥ 5).
Nhãn chỉ dùng để chấm. Cách dùng: python soi_placebo.py <thư mục seed> [...]"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def gop(ranks):
    out = []
    for x in ranks:
        s = x.split("_")[0].replace("-db", "")
        if s not in out:
            out.append(s)
    return out


for d in sys.argv[1:]:
    ranks = {p.stem: gop(json.loads(p.read_text())["0"])
             for p in Path(d).glob("*.json") if not p.name.endswith("_failed.json") and p.name != "lenh.json"}
    roots = sorted({c.split("_")[0] for c in ranks})
    hang, top = defaultdict(list), defaultdict(list)
    theo_loi = defaultdict(lambda: [0, 0])
    top1 = Counter()
    n_ung_vien = []
    for ca, r in ranks.items():
        that = ca.split("_")[0]
        n_ung_vien.append(len(r))
        top1[r[0]] += 1
        theo_loi[ca.split("_")[1]][0] += int(r[0] == that)
        theo_loi[ca.split("_")[1]][1] += 1
        for s in roots:
            h = r.index(s) + 1 if s in r else len(r) + 1  # thiếu trong thứ hạng: hạng cuối + 1
            k = "that" if s == that else "khac"
            hang[k].append(h)
            top[k].append(h == 1)
    tb = {k: sum(v) / len(v) for k, v in hang.items()}
    t1 = {k: sum(v) / len(v) for k, v in top.items()}
    mr1 = sum(1 / n for n in n_ung_vien) / len(n_ung_vien)
    mr5 = sum(3 / n for n in n_ung_vien) / len(n_ung_vien)
    print(f"{d}: số service sau gộp {min(n_ung_vien)}–{max(n_ung_vien)}; hạng TB gốc thật {tb['that']:.3f} vs gốc khác "
          f"{tb['khac']:.3f}; top-1 gốc thật {t1['that']:.3f} vs gốc khác {t1['khac']:.3f}; "
          f"may rủi AC@1 {mr1:.5f}, Avg@5 {mr5:.5f}")
    print("   top-1 hay gặp:", top1.most_common(5))
    print("   AC@1 theo lỗi:", {k: f"{a}/{n}" for k, (a, n) in sorted(theo_loi.items())})
