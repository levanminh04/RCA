"""T-016 S8: so lượt hoán vị cột (--hoan-vi-cot 12345) với lượt không hoán vị cùng seed. Ghi: số ca vectơ mức
nghiêm trọng đổi (so theo service, sai lệch > 1e-9), số ca phân cụm đổi (so phân hoạch tập service), số ca thứ hạng
cuối đổi, số ca top-1 đổi. Cách dùng: python so_hoan_vi.py <khối hoán vị> <khối gốc> <seed,...>"""
import json
import sys
from pathlib import Path


def doc(d):
    out = {}
    for l in open(Path(d) / "meta.jsonl", encoding="utf-8"):
        m = json.loads(l)
        tg = m["trung_gian"]
        sv = tg["service_list"]
        vec = {s: x for s, x in zip(sv, tg["X_train"])}
        nhom = {}
        for s, c in zip(sv, tg["y_pred"]):
            nhom.setdefault(c, set()).add(s)
        r = json.loads((Path(d) / f"{m['ca']}.json").read_text())["0"]
        out[m["ca"]] = (vec, frozenset(frozenset(v) for v in nhom.values()), r)
    return out


hv, goc, seeds = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
for s in seeds:
    A, B = doc(f"{hv}/seed{s}"), doc(f"{goc}/seed{s}")
    vec_doi = sum(1 for c in A if set(A[c][0]) != set(B[c][0]) or
                  any(max(abs(a - b) for a, b in zip(A[c][0][k], B[c][0][k])) > 1e-9 for k in A[c][0]))
    cum_doi = sum(1 for c in A if A[c][1] != B[c][1])
    xh_doi = sum(1 for c in A if A[c][2] != B[c][2])
    top1 = sum(1 for c in A if A[c][2][0] != B[c][2][0])
    print(f"seed{s}: {len(A)} ca; vectơ mức nghiêm trọng đổi {vec_doi}; phân cụm đổi {cum_doi}; thứ hạng đổi {xh_doi}; top-1 đổi {top1}")
