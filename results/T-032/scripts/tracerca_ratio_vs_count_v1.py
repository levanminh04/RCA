"""T-032 phiên 11, bổ sung cho mục 2.1 của ket-qua-phien-11.md (thêm SAU khi xem bảng việc 2): với TraceRCA, thực thể đứng trên root
có tỷ lệ span mang cờ a/n thấp hơn root nhưng số span mang cờ a lớn hơn root ở bao nhiêu cặp. Chỉ ghép hai file kết quả đã có;
không gọi phương pháp. Điểm native của TraceRCA là ji = 2a/(n + H) (đã kiểm đẳng thức ở 48/48 ca, KQ9 mục 3).
Dùng: py -3 -B -X utf8 scripts/tracerca_ratio_vs_count_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TD = ROOT / "runs/tracerca-core-td-001/summary.json"
LINK = ROOT / "runs/slow-call-flag-link-001/cases.json"


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    td = {(c["dataset"], c["opaque_id"]): c for c in json.loads(TD.read_text(encoding="utf-8"))["cases"]}
    rows, summary = [], {}
    for c in json.loads(LINK.read_text(encoding="utf-8")):
        if c["method"] != "tracerca" or not c.get("root_ranked"):
            continue
        H = td[(c["dataset"], c["opaque_id"])]["counts"]["H_native"]
        rs = c["root_link"]["span"]
        above = [e for e in c["entities"] if e["above_root"]]
        pairs = []
        for e in above:
            a, n = e["span"]["a"], e["span"]["n"]
            ji_e, ji_r = 2 * a / (n + H), 2 * rs["a"] / (rs["n"] + H)
            pairs.append({"entity": e["entity"], "class": e["class"], "a": a, "n": n, "ratio": a / n, "ji": ji_e,
                          "ratio_lower_than_root": a / n < rs["a"] / rs["n"], "a_larger_than_root": a > rs["a"], "ji_larger_than_root": ji_e > ji_r})
        rows.append({"dataset": c["dataset"], "opaque_id": c["opaque_id"], "cell": c["cell"], "H": H, "root_a": rs["a"], "root_n": rs["n"],
                     "root_ratio": rs["a"] / rs["n"], "H_over_root_n": H / rs["n"], "root_rank": c["root_rank"], "pairs": pairs})
        s = summary.setdefault(c["dataset"], {"cases_ok_root_ranked": 0, "cases_with_above": 0, "pairs": 0, "ratio_lower_than_root": 0, "a_larger_than_root": 0,
                                              "ji_larger_than_root": 0, "ratio_lower_and_a_larger": 0, "cases_where_root_has_top_ratio_among_above_and_root": 0})
        s["cases_ok_root_ranked"] += 1
        s["cases_with_above"] += bool(pairs)
        s["pairs"] += len(pairs)
        s["ratio_lower_than_root"] += sum(p["ratio_lower_than_root"] for p in pairs)
        s["a_larger_than_root"] += sum(p["a_larger_than_root"] for p in pairs)
        s["ji_larger_than_root"] += sum(p["ji_larger_than_root"] for p in pairs)
        s["ratio_lower_and_a_larger"] += sum(p["ratio_lower_than_root"] and p["a_larger_than_root"] for p in pairs)
        s["cases_where_root_has_top_ratio_among_above_and_root"] += bool(pairs) and all(p["ratio_lower_than_root"] for p in pairs)
    result = {"schema": "T032-tracerca-ratio-vs-count-v1", "post_hoc": True,
              "sources": {"td_sha256": hashlib.sha256(TD.read_bytes()).hexdigest(), "link_cases_sha256": hashlib.sha256(LINK.read_bytes()).hexdigest()},
              "note": "ji tính lại từ a, n, H; ji_larger_than_root phải đúng ở mọi cặp vì đây là các cặp đứng trên root (tự kiểm).",
              "summary": summary, "cases": rows, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    for r in rows:
        if r["dataset"] == "RE2-TT" and r["pairs"]:
            print(r["opaque_id"], r["cell"], "H", r["H"], "root", r["root_a"], r["root_n"], "H/n", round(r["H_over_root_n"], 1))


if __name__ == "__main__":
    main()
