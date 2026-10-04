"""T-016 S1: so số công bố tự parse (moc-cong-bo.json) với moc.py của T-006 (TORAI_B2, TORAI_B3, TORAI_MD)."""
import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location("moc", "results/T-006/scripts/moc.py")
moc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(moc)
d = json.load(open("results/T-016/moc-cong-bo.json", encoding="utf-8"))
NGUON = {"Metric": "Metric", "Metric+Log": "Metric + Log", "Metric+Log+Trace": "Metric + Log + Trace",
         "Log": "Log", "Trace": "Trace"}
so = lech = 0
for ten, bang, cua_t006 in (("bang2_OB", d["bang2_OB"], moc.TORAI_B2), ("bang3_SS", d["bang3_SS"], moc.TORAI_B3)):
    for (nguon, pp), o in cua_t006.items():
        r = [x for x in bang if x["nguon"] == NGUON.get(nguon, nguon) and x["phuong_phap"] == pp]
        if len(r) != 1:
            print("KHONG THAY", ten, nguon, pp); lech += 1; continue
        for loi, (t1, t3, a5) in o.items():
            mine = r[0]["o"][loi.lower()]
            for k, v in zip(("T1", "T3", "A5"), (t1, t3, a5)):
                so += 1
                if mine[k] != v:
                    lech += 1
                    print("LECH", ten, nguon, pp, loi, k, mine[k], v)
for loi, v in moc.TORAI_MD.items():
    so += 1
    if d["torai_md_OB_A5"][loi] != v:
        lech += 1; print("LECH torai_md", loi)
print(f"so {so} ô, lệch {lech}")
sys.exit(1 if lech else 0)
