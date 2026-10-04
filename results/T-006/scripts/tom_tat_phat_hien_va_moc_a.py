r"""T-006 phiên 2: ghi ra file các số mà phiên 1 mới in ra màn hình, để báo cáo trích được (luật cứng 4).

1. Chấm lại các file phát hiện tác giả lưu sẵn trong fse-* (naive_bocpd.json, nsigma.json) theo đúng luật của
   baro.reproducibility.reproduce_bocpd: TP nếu có điểm phát hiện, FN nếu không; FP nếu điểm đầu < ngưỡng, TN nếu không.
   Ngưỡng 300 (chỉ số mốc tiêm trong cửa sổ 300 + 300 của reproduce_bocpd) và 360 (chỉ số mốc tiêm khi dùng cả ca 721 dòng).
2. Gom kết quả N-Sigma phát hiện của các khối l4-nsigma-phat-hien-* (dòng TONG trong stdout.log trong file nén).
3. Gom kết quả các lệnh tác giả của BARO (ví dụ README, reproduce_baro, RQ4) từ stdout.log trong file nén.
Ghi: cham/phat-hien-luu-san.txt, cham/nsigma-phat-hien.txt, cham/baro-lenh-tac-gia.txt.
Cách dùng (python của envs/py312): python tom_tat_phat_hien_va_moc_a.py
"""
import glob
import json
import re
import tarfile
from os.path import dirname, join
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs"
OUT = HERE.parent / "cham"
DATA = Path(r"D:\RCA-ext\data")


def doc_tar(ten, duoi):
    with tarfile.open(RUNS / f"{ten}.tar.gz") as t:
        n = next(x for x in t.getnames() if x.endswith(duoi))
        return t.extractfile(n).read().decode("utf-8", "replace")


# 1
lines = ["Chấm lại file phát hiện tác giả lưu sẵn trong fse-*, luật reproduce_bocpd (TP = có điểm; FP = điểm đầu < ngưỡng)."]
for ds in ("fse-ob", "fse-ss"):
    for fn in ("naive_bocpd.json", "nsigma.json"):
        for thr in (300, 360):
            tp = fp = fn_ = tn = 0
            for p in glob.glob(str(DATA / ds / "**" / "simple_data.csv"), recursive=True):
                cps = json.load(open(join(dirname(p), fn)))
                first = (cps[0][0] if isinstance(cps[0], list) else cps[0]) if cps else None
                if cps:
                    tp += 1
                else:
                    fn_ += 1
                if first is not None and first < thr:
                    fp += 1
                else:
                    tn += 1
            P, R = tp / (tp + fp), tp / (tp + fn_)
            lines.append(f"{ds} {fn:17} ngưỡng {thr}: P={P:.4f} R={R:.4f} F1={2 * P * R / (P + R):.4f} (TP {tp}, FP {fp}, FN {fn_}, TN {tn})")
(OUT / "phat-hien-luu-san.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))

# 2
lines = ["N-Sigma phát hiện (scripts/nsigma_phat_hien.py), dòng TONG của từng khối:"]
for ten in sorted(p.name[:-7] for p in RUNS.glob("l4-nsigma-phat-hien-*.tar.gz")):
    for l in doc_tar(ten, "/stdout.log").splitlines():
        if l.startswith("TONG"):
            lines.append(f"{ten}: {l}")
(OUT / "nsigma-phat-hien.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))

# 3
lines = ["Lệnh tác giả BARO (main.py của repo BARO e35f4ec, vi_du_baro.py), trích stdout.log trong file nén:"]
for ten in sorted(p.name[:-7] for p in RUNS.glob("*.tar.gz") if re.search(r"(reproduce-baro|reproduce-rq4|vi-du-baro)", p.name)):
    so = doc_tar(ten, "/stdout.log")
    keep = [l for l in so.splitlines() if re.search(r"Avg@5 Acc|KET-QUA|^\[0\.|Anomalies are detected|Top 5", l)]
    lines.append(f"{ten}: " + " | ".join(keep))
(OUT / "baro-lenh-tac-gia.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
