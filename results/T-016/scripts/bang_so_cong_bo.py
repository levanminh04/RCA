"""T-016: bảng so điểm (trung bình qua seed) với số công bố. Đọc cham/*-tong-hop.json và moc-cong-bo.json.
Cách dùng: python bang_so_cong_bo.py > cham/bang-so-cong-bo.md (python bất kỳ, chỉ thư viện chuẩn)."""
import json
import statistics as st

R = "results/T-016/"
moc = json.load(open(R + "moc-cong-bo.json", encoding="utf-8"))


def dong(bang, nguon, pp):
    r = [x for x in moc[bang] if x["nguon"] == nguon and x["phuong_phap"] == pp]
    return r[0]["o"] if r else None


MOC = {"OB": {"M+L+T": dong("bang2_OB", "Metric + Log + Trace", "TORAI"), "M+L": dong("bang2_OB", "Metric + Log", "TORAI")},
       "SS": {"M+L": dong("bang3_SS", "Metric + Log", "TORAI")}}
LOI = ["cpu", "mem", "disk", "socket", "delay", "loss"]
print("| Cấu hình | n seed | AC@1 TB | AC@3 TB | Avg@5 TB (sd) [min, max] | mốc bài (T1/T3/A5) | lệch Avg@5 | Avg@5 theo lỗi TB (cpu/mem/disk/socket/delay/loss) | SeverityScorer không cụm (seed0) A5 |")
print("|---|---|---|---|---|---|---|---|---|")
for f in ("s7", "s10"):
    d = json.load(open(R + f"cham/{f}-tong-hop.json", encoding="utf-8"))
    for ten, k in d.items():
        ds = "OB" if "-ob-" in ten else ("SS" if "-ss-" in ten else "TT")
        nguon = "M+L" if (ten.endswith("-ML") or ds == "SS") else "M+L+T"
        m = MOC.get(ds, {}).get(nguon)
        g = k.get("giua_seed")
        s0 = next(iter(k["seeds"].values()))
        if g:
            a1, a3, a5 = g["AC1"]["tb"], g["AC3"]["tb"], g["Avg5"]
            a5s = f"{a5['tb']:.3f} ({a5['sd']:.3f}) [{a5['min']:.3f}, {a5['max']:.3f}]"
            a5tb = a5["tb"]
            theo = "/".join(f"{g['Avg5_theo_loi_tb'].get(l, float('nan')):.3f}" for l in LOI)
        else:
            dd = s0["diem"]["AVERAGE"]
            a1, a3, a5tb = dd["AC1"], dd["AC3"], dd["Avg5"]
            a5s = f"{a5tb:.3f} (1 seed)"
            theo = "/".join(f"{s0['diem'][l]['Avg5']:.3f}" for l in LOI)
        mm = f"{m['average']['T1']}/{m['average']['T3']}/{m['average']['A5']} ({ds} {nguon})" if m else "không so (TT dev)"
        lech = f"{a5tb - m['average']['A5']:+.3f}" if m else "—"
        sev = s0.get("trung_gian", {}).get("diem_severity_scorer_khong_cum", {}).get("Avg5")
        print(f"| {ten} | {len(k['seeds'])} | {a1:.3f} | {a3:.3f} | {a5s} | {mm} | {lech} | {theo} | {sev:.3f} |")
print()
print("docs/TORAI.md (OB, Avg@5 theo lỗi, mốc A):", moc["torai_md_OB_A5"])
