r"""T-016 S1: tra số công bố TRƯỚC khi chạy (SL28).

Nguồn:
- Bài TORAI, arXiv 2604.13522v1, bản HTML https://arxiv.org/html/2604.13522v1 (tải 04/10/2026, lưu ngoài repo).
  Bảng 2 (OB), 3 (SS), 4 (TT): mỗi dòng 21 số = 7 nhóm (CPU, MEM, DISK, SOCKET, DELAY, LOSS, AVERAGE) × (T1, T3, A5),
  T1 = AC@1, T3 = AC@3, A5 = Avg@5 mức service. Bảng 8: thời gian (giây/ca). Bảng 9: ablation (T1, T3, A5 × OB, SS, TT).
- docs/TORAI.md của RCAEval 259ea41: Avg@5 từng lỗi của TORAI trên torai-ob (mốc loại A).
Cách dùng: python moc_torai.py --html <torai.html> --torai-md <RCAEval/docs/TORAI.md> --ra moc-cong-bo.json
Chỉ dùng thư viện chuẩn.
"""
import argparse
import html as H
import json
import re

LOI = ["cpu", "mem", "disk", "socket", "delay", "loss", "average"]


def text_cua(html_path):
    t = open(html_path, encoding="utf-8").read()
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", t, flags=re.S)
    t = re.sub(r"<annotation[^>]*>.*?</annotation>", "", t, flags=re.S)
    t = re.sub(r"</(p|div|tr|h\d|li|table|figcaption)>", "\n", t)
    t = re.sub(r"<t[dh][^>]*>", " | ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = H.unescape(t)
    return re.sub(r"\n\s*\n+", "\n", t)


def la_so(x):
    return re.fullmatch(r"-|\(\*\)|\d+(\.\d+)?", x) is not None


def doc_so(x):
    return None if x in ("-", "(*)") else float(x)


def tach_tok(k):
    """Tách ô theo dấu |; ô số cuối bảng bị dính chú thích "(*) ..." hoặc "(-) ..." thì chỉ giữ phần số."""
    out = []
    for x in k.replace("\n", " ").split("|"):
        x = x.strip()
        if not x:
            continue
        m = re.match(r"^(-|\d+(\.\d+)?)\s+\(", x)
        out.append(m.group(1) if m else x)
    return out


def khoi_bang(t, so):
    i = t.index(f"Table {so}.")
    j = t.index(f"Table {so + 1}.", i + 1)
    return t[i:j]


def bang_rca(t, so):
    k = khoi_bang(t, so)
    tok = tach_tok(k)
    i = tok.index("AVERAGE") + 1 + 21  # bỏ 21 nhãn T1/T3/A5
    rows, nguon = [], None
    while i < len(tok):
        a = tok[i]
        if la_so(a):
            raise ValueError(f"Bảng {so}: gặp số ngoài dòng ở vị trí {i}: {tok[i-3:i+3]}")
        if i + 1 < len(tok) and not la_so(tok[i + 1]):
            # a là nguồn dữ liệu, tok[i+1] là phương pháp
            if not la_so(tok[i + 2]):
                break  # hết bảng (chú thích)
            nguon, pp, i = a, tok[i + 1], i + 2
        else:
            pp, i = a, i + 1
        so_ = tok[i:i + 21]
        if len(so_) < 21 or not all(la_so(x) for x in so_):
            break
        rows.append({"nguon": nguon, "phuong_phap": pp,
                     "o": {LOI[g]: dict(zip(["T1", "T3", "A5"], [doc_so(x) for x in so_[3 * g:3 * g + 3]]))
                           for g in range(7)}})
        i += 21
    return rows


def bang8(t):
    k = khoi_bang(t, 8)
    tok = tach_tok(k)
    i = tok.index("BARO")
    out = {}
    while i + 3 < len(tok) and not tok[i].startswith("(*)"):
        pp = tok[i]
        vals = [doc_so(x) if la_so(x) else x for x in tok[i + 1:i + 4]]
        out[pp] = dict(zip(["OB", "SS", "TT"], vals))
        i += 4
        if pp == "TORAI":
            break
    return out


def bang9(t):
    k = khoi_bang(t, 9)
    tok = tach_tok(k)
    i = tok.index("A5") + 7  # nhãn A5 đầu tiên là nhãn thứ 3 trong 9 nhãn T1/T3/A5
    out, nguon = [], None
    while i < len(tok):
        if tok[i] in ("Metric, Log", "Metric, Log, Trace"):
            nguon = tok[i]
            i += 1
        pp = tok[i]
        vals = tok[i + 1:i + 10]
        if len(vals) < 9 or not all(la_so(x) for x in vals):
            break
        v = [doc_so(x) for x in vals]
        out.append({"nguon": nguon, "phuong_phap": pp,
                    "OB": dict(zip(["T1", "T3", "A5"], v[0:3])),
                    "SS": dict(zip(["T1", "T3", "A5"], v[3:6])),
                    "TT": dict(zip(["T1", "T3", "A5"], v[6:9]))})
        i += 10
    return out


def torai_md(p):
    s = open(p, encoding="utf-8").read()
    i = s.index("### Online Boutique")
    j = s.index("### Sock Shop")
    return {m.group(1).lower(): float(m.group(2)) for m in re.finditer(r"Avg@5-(\w+):\s*([\d.]+)", s[i:j])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--torai-md", required=True)
    ap.add_argument("--ra", required=True)
    a = ap.parse_args()
    t = text_cua(a.html)
    out = {
        "nguon": "arXiv 2604.13522v1 HTML; RCAEval 259ea41 docs/TORAI.md",
        "bang2_OB": bang_rca(t, 2), "bang3_SS": bang_rca(t, 3), "bang4_TT": bang_rca(t, 4),
        "bang8_thoi_gian_giay_moi_ca": bang8(t), "bang9_ablation": bang9(t),
        "torai_md_OB_A5": torai_md(a.torai_md),
    }
    open(a.ra, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
    for b in ("bang2_OB", "bang3_SS", "bang4_TT"):
        print(b, len(out[b]), "dòng:", [(r["nguon"], r["phuong_phap"]) for r in out[b]])
    print("bang8", out["bang8_thoi_gian_giay_moi_ca"])
    print("bang9", len(out["bang9_ablation"]), "dòng")
    print("torai_md", out["torai_md_OB_A5"])


if __name__ == "__main__":
    main()
