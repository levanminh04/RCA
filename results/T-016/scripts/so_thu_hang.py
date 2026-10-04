"""T-016: so thứ hạng từng ca giữa hai thư mục kết quả (định dạng main.py: <ca>.json = {"0": ranks}).

Cách dùng: python so_thu_hang.py <thư mục A> <thư mục B> [--ra file.json]
In: số ca chung, số ca giống hệt, danh sách ca khác (kèm top-3 hai bên), ca chỉ có ở một bên, ca lỗi.
Không đọc nhãn.
"""
import argparse
import json
from pathlib import Path


def doc(d):
    out, loi = {}, set()
    for p in Path(d).glob("*.json"):
        if p.name in ("lenh.json",):
            continue
        if p.name.endswith("_failed.json"):
            loi.add(p.name[:-12])
            continue
        v = json.loads(p.read_text(encoding="utf-8"))
        if "error" in v:
            loi.add(p.stem)
            continue
        out[p.stem] = list(v.values())[0]
    return out, loi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--ra")
    x = ap.parse_args()
    A, la = doc(x.a)
    B, lb = doc(x.b)
    chung = sorted(set(A) & set(B))
    khac = [c for c in chung if A[c] != B[c]]
    kq = {"a": x.a, "b": x.b, "so_ca_a": len(A), "so_ca_b": len(B), "loi_a": sorted(la), "loi_b": sorted(lb),
          "chung": len(chung), "giong_het": len(chung) - len(khac),
          "khac": {c: {"a_top3": A[c][:3], "b_top3": B[c][:3]} for c in khac},
          "chi_a": sorted(set(A) - set(B)), "chi_b": sorted(set(B) - set(A))}
    print(f"chung {kq['chung']}, giống hệt {kq['giong_het']}, khác {len(khac)}, chỉ A {len(kq['chi_a'])}, "
          f"chỉ B {len(kq['chi_b'])}, lỗi A {len(la)}, lỗi B {len(lb)}")
    if x.ra:
        Path(x.ra).write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
