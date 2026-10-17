"""So tong-hop.json của run 005 (SMTP V2, trước sửa R1) với run 007 (bản sửa R1 của người làm T-038).
Lệnh: py -3 -X utf8 -B results/T-040/runs/tong-hop-007/so_sanh_005_007.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
old = json.load(open(os.path.join(ROOT, "results/T-040/runs/tong-hop-005/tong-hop.json"), encoding="utf-8"))
new = json.load(open(os.path.join(ROOT, "results/T-040/runs/tong-hop-007/tong-hop.json"), encoding="utf-8"))
SKIP = {"_trich_tu_raw", "run", "tep", "nguon", "tung_graph", "luu_y"}
rows = []
def diff(a, b, path):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in SKIP:
                diff(a.get(k), b.get(k), path + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif a != b:
        rows.append({"pointer": path, "run005": a, "run007": b})
diff(old["he_thong"], new["he_thong"], "/he_thong")
diff(old["lan_theo"], new["lan_theo"], "/lan_theo")
diff(old["nguon_trace_T035"], new["nguon_trace_T035"], "/nguon_trace_T035")
changed = [r["pointer"] for r in rows]
num = [r for r in rows if isinstance(r["run005"], int) and isinstance(r["run007"], int)]
summary = {
    "rows": len(rows),
    "numeric_changes_only_TT": all(p.startswith("/he_thong/TT/") for p in (r["pointer"] for r in num)),
    "OB_FT_unchanged": not any(p.startswith(("/he_thong/OB", "/he_thong/FT")) for p in changed),
    "TT_trace_side_unchanged": not any(p.endswith(m) for p in changed for m in ("/T/min", "/T/max", "/I/min", "/I/max", "/TO/min", "/TO/max", "/union_T", "/union_intersection", "/union_trace_only", "/graphs_T_empty")),
    "TT_operation_level_unchanged": not any("/ho_graph/operation:" in p for p in changed),
    "lan_theo_numbers_unchanged": not any(p.startswith("/lan_theo") and not p.endswith("/status") for p in changed),
}
json.dump({"tom_tat": summary, "khac_biet": rows}, open(os.path.join(ROOT, "results/T-040/runs/tong-hop-007/so-sanh-005-007.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False))
