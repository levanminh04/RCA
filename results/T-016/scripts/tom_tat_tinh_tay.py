r"""T-016 S12: in bảng tóm tắt (markdown) từ runs/s12-tinh-tay-<biến thể>.json để viết vi-du-tinh-tay.md.
Chạy bằng envs/T-016-cong-cu. Cách dùng: python tom_tat_tinh_tay.py <json> > <md>
"""
import json
import sys

k = json.load(open(sys.argv[1], encoding="utf-8"))
t = k["tinh_tay"]
ss = k["so_sanh"]
p = print
p(f"mốc tiêm: {k['inject_time']}")
p("\n## So với lượt chính thức\n")
p("```\n" + json.dumps(ss, ensure_ascii=False, indent=1) + "\n```")
ct = t["chi_tiet_diem"]
p("\n## Điểm từng chuỗi (max |z|), 10 cao nhất mỗi nguồn\n")
for nguon in ("metric", "log", "trace_lat", "trace_err"):
    p(f"- {nguon} ({len(ct[nguon])} chuỗi): " + "; ".join(f"{c} {s:.4g}" for c, s in ct[nguon][:10]))
p(f"- trace_err nhân 1e9: {ct['nhan_1e9']}")
p("\n## Vectơ mức nghiêm trọng (đã chuẩn hóa từng nguồn) và điểm service\n")
p("| service | metric | log | trace_lat | trace_err | trung bình | cụm |")
p("|---|---|---|---|---|---|---|")
for sv, x, c in zip(t["service_list"], t["X_train"], t["y_pred"]):
    p(f"| {sv} | {x[0]:.4f} | {x[1]:.4f} | {x[2]:.4f} | {x[3]:.4f} | {sum(x)/4:.4f} | {c} |")
p("\n## BIC theo số cụm\n")
p("| k | BIC (sklearn) | BIC tự tính |")
p("|---|---|---|")
for i, (a, b) in enumerate(zip(t["bic"], t["bic_tu_tinh"]), 1):
    p(f"| {i} | {a:.3f} | {b:.3f} |")
p(f"\nchọn k = {t['n_comp']}")
p("\n## Cụm theo thứ tự điểm cụm\n")
for c in t["cac_cum"]:
    line = f"- cụm {c['cum']} (điểm {c['diem_cum']:.4f}): " + ", ".join(
        f"{s} {v:.4f}" for s, v in zip(c["services"], c["diem_service"]))
    p(line)
    if c.get("rcd") is None and len(c["services"]) == 1:
        continue
    rv = c["rcd_vao"]
    p(f"  - RCD nhận {rv['dong_normal']}+{rv['dong_anomal']} dòng, {len(rv['cot'])} cột: {rv['cot']}")
    for lv in c["level"]:
        p(f"  - pha 1, mức với {lv['so_cot']} cột, khối: {lv['khoi']}")
    p(f"  - số lần chạy Ψ-PC: {len(c['pc'])}; RCD trả: {c['rcd_ranks']}; nội bộ: {c['noi_bo']}; dự phòng: {c['du_phong']}")
    for j, pc in enumerate(c["pc"]):
        co_kiem = [x for x in pc["kiem"]]
        if not co_kiem:
            continue
        p(f"    - PC #{j}: α={pc['alpha']:.3f}, cột {pc['cot'][:-1]}, số bin {pc['so_bin']}, F kề: {pc['f_con']}")
        for x in co_kiem[:12]:
            S = [pc['cot'][s] for s in x['S']]
            p(f"      - kiểm F ⊥ {pc['cot'][x['y']]} | {S}: χ²={x['chi2']:.3f}, df={x['df']}, p={x['p']:.4g} → "
              f"{'độc lập, bỏ cạnh' if x['doc_lap'] else 'phụ thuộc, giữ'}")
        if len(co_kiem) > 12:
            p(f"      - ... {len(co_kiem) - 12} phép kiểm nữa")
p(f"\n## Thứ hạng cuối\n\n{t['ranks']}")
