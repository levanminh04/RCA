"""T-007: trích mốc của MicroRank, TraceRCA từ Bảng 2 bài TORAI (arXiv 2604.13522v1, bản HTML).

Bảng 2: Online Boutique (torai-OB), sáu loại lỗi; mỗi ô (T1, T3, A5) = (AC@1, AC@3, Avg@5).
MicroRank, TraceRCA chỉ xuất hiện ở nhóm "Trace" của Bảng 2, nên tìm theo tên phương pháp là đủ.
Số lấy bằng máy từ HTML, không gõ tay. Ghi kèm SHA-256 của trang đã tải.

Chạy: py -3 trich_moc.py <file html đã tải> <file json ra>
Tải trang: curl -sL -o torai.html https://arxiv.org/html/2604.13522v1
"""
import hashlib
import html
import json
import re
import sys

COT = ["cpu", "mem", "disk", "socket", "delay", "loss", "AVERAGE"]


def txt(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def main():
    src, dst = sys.argv[1], sys.argv[2]
    raw = open(src, "rb").read()
    t = raw.decode("utf-8")
    tabs = re.findall(r'<figure[^>]*class="ltx_table"[^>]*>(.*?)</figure>', t, flags=re.S)
    b2 = [tb for tb in tabs if txt(re.search(r"<figcaption[^>]*>(.*?)</figcaption>", tb, flags=re.S).group(1))
          .startswith("Table 2.")]
    assert len(b2) == 1
    cap = txt(re.search(r"<figcaption[^>]*>(.*?)</figcaption>", b2[0], flags=re.S).group(1))
    assert "Online Boutique" in cap
    out = {"nguon": "arXiv 2604.13522v1, https://arxiv.org/html/2604.13522v1", "sha256_html": hashlib.sha256(raw).hexdigest(),
           "bang": cap, "o": "(AC@1, AC@3, Avg@5)", "moc": {}}
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", b2[0], flags=re.S):
        cells = [txt(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, flags=re.S)]
        for m in ["MicroRank", "TraceRCA"]:
            if m in cells:
                so = [float(x) for x in cells[cells.index(m) + 1:]]
                assert len(so) == 21, (m, cells)
                assert m not in out["moc"], "trùng dòng " + m
                out["moc"][m] = {c: so[3 * i:3 * i + 3] for i, c in enumerate(COT)}
    assert set(out["moc"]) == {"MicroRank", "TraceRCA"}
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
