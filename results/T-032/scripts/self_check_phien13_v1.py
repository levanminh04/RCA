"""T-032 phiên 13: tự soát số của ket-qua-phien-13.md với các file kết quả (phần E; nối tiếp phần A–D của self_check_phien12_v2.py).

Mỗi mục: tính lại giá trị từ file kết quả, định dạng như trong văn bản, rồi kiểm chuỗi "ngữ cảnh + số" có mặt trong ket-qua-phien-13.md.
Dùng: python self_check_phien13_v1.py <results/T-032> <file kết quả mới>
"""
import json
import statistics
import sys
from pathlib import Path


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8-sig"))


def pct(v, nd=1):
    return ("%.*f" % (nd, 100 * v)).replace(".", ",") + "%"


def num(v, nd=2):
    return ("%.*f" % (nd, v)).replace(".", ",")


def main():
    base, out = Path(sys.argv[1]), Path(sys.argv[2])
    text = (base / "ket-qua-phien-13.md").read_text(encoding="utf-8")
    fm = read(base / "runs/fake-marker-001/summary.json")["summary"]
    dv = read(base / "runs/tong-hop-phien-13-001/derived-013.json")
    rl = read(base / "runs/root-latency-001/summary.json")
    td = read(base / "runs/tracerca-dropnew-001/summary.json")["summary"]
    ml = read(base / "runs/microrank-merged-link-001/summary.json")["summary"]
    k9 = read(base / "runs/circa-kt9-001/collect-001/summary.json")["summary"]
    claims = []

    def claim(label, fragment):
        claims.append({"label": label, "fragment": fragment, "found": fragment in text})

    # --- mục 1 ---
    for name in ("real300", "real150", "fake150", "real100", "fake100a", "fake100b"):
        c = fm["configs"][name]
        row = "| %s | %s | %s | %s |" % (pct(c["abnormal_share"]["median"]).replace("%", "%") , pct(c["share_without_root"]["median"]), pct(c["share_with_root"]["median"]), pct(c["span_flag_share"]["median"]))
        row = row.replace("| 36,6% | 15,9%", "| **36,6%** | **15,9%**")
        claim("KT-1 bảng " + name, row)
    sc = fm["self_check"]
    claim("KT-1 tự kiểm", "bằng H_native ở %d/26 ca" % sc["flags_equal_H_native"])
    claim("KT-1 20 ca", "ở %d/26 ca tỷ lệ này từ 20%% trở lên" % dv["kt1"]["cases_fake_all_ge_0.20"])
    claim("KT-1 không root", "trung vị %s số trace bất thường là trace không có span của root" % pct(dv["kt1"]["share_of_real_abnormal_traces_without_root"]["median"], 0))
    d = fm["kt1"]["fake100a_minus_fake100b"]
    claim("KT-1 vị trí", "trung vị −%s điểm phần trăm (từ −%s tới +%s)" % (num(-100 * d["median"], 1), num(-100 * d["min"], 1), num(100 * d["max"], 1)))
    claim("KT-1 vị trí 0/26", "= %d/26)" % fm["kt1"]["fake_position_unstable_cases"])
    p = dv["kt1"]["predicted_over_actual_fake_by_case"]
    claim("KT-1 độc lập", "trung vị %s so với %s; tỷ số dự đoán/thật từ %s tới %s" % (pct(fm["kt1"]["median_predicted_fake150"]), pct(fm["kt1"]["median_F_fake150"]), num(p["min"]), num(p["max"])))
    claim("KT-1 mốc a", "đạt ở %d/26 ca). Vế sau **không đạt** (chỉ %d/26 ca" % (fm["kt1"]["cases_F_ge_0.8R"], fm["kt1"]["predicted_within_20pct_of_F_by_case"]))
    claim("KT-1 mốc b", "**Không đạt** (%d/26 ca)" % fm["kt1"]["cases_F_le_0.5R"])
    r = dv["kt1"]["fake_over_real_noroot_by_case"]
    claim("KT-1 cùng loại", "trung vị %s, từ %s tới %s; từ 0,8 trở lên ở %d/26 ca; không ca nào dưới 0,5" % (num(r["median"]), num(r["min"]), num(r["max"]), dv["kt1"]["cases_fake_noroot_ge_0.8_real_noroot"]))
    claim("KT-1 có root", "tỷ số theo ca có trung vị %s" % num(dv["kt1"]["fake_over_real_withroot_by_case"]["median"]))
    assert dv["kt1"]["cases_fake_noroot_le_0.5_real_noroot"] == 0 and not any(fm["kt1"][m] for m in ("mark_a", "mark_b", "mark_c"))
    # --- mục 2 ---
    k = dv["kt2"]
    for label, key in (("Mọi thao tác đông span", "all"), ("Phía trên root (gọi trực tiếp hoặc gián tiếp)", "upstream_of_root"), ("Không liên hệ với root", "unrelated"), ("Phía dưới root hoặc hai chiều", "downstream_or_both")):
        b = k[key]
        row = "| %s | %s | %s | %s | %d | %d |" % (label, "{:,}".format(b["n"]).replace(",", "."), pct(b["fake_median"]), pct(b["real_median"]), b["fake_ge_2pct"], b["real_ge_2x_fake"])
        claim("KT-2 bảng " + key, row.replace("| 6,2% |", "| **6,2%** |"))
    claim("KT-2 lớn nhất", "trung vị 1,0%%, lớn nhất %s" % pct(k["all"]["fake_max"]))
    claim("KT-2 cặp", "từ 2%% trở lên ở %d/9. Sau mốc thật, %d/9 cặp tăng gấp từ 2 lần" % (k["pairs"]["fake150_ge_2pct"], k["pairs"]["real150_ge_2x_fake150"]))
    claim("KT-2 mốc", "(%d/1.021). (b)" % fm["kt2"]["all"]["fake_ge_2pct"])
    claim("KT-2 mốc b", "(%d/1.021 dưới 1%%" % fm["kt2"]["all"]["fake_lt_1pct"])
    assert fm["kt2"]["mark_a"] is False and fm["kt2"]["mark_b"] is False
    # --- mục 3 ---
    claim("KT-12 tự kiểm", "7/7" if rl["self_check"] == {"cases": 7, "exact_vs_frozen": 7} else "KHÔNG KHỚP")
    for cid in ("dev-746fd74313", "dev-f81f88234e", "dev-57546fd87b"):
        c = rl["cases"][cid]["columns"]["ts-auth-service_latency"]
        first = "không" if c["first_exceed_s_after_t"] is None else "%d" % c["first_exceed_s_after_t"]
        claim("KT-12 " + cid, "| `%s` | %s → %s | %s | %s | %d/300 | %s |" % (cid, num(c["median_N"], 3), num(c["median_A"], 3), num(c["iqr_N"], 3), num(c["robust_z_max"], 1), c["votes_A_gt_mean_3std"], first))
    a, b = rl["cases"]["dev-5467884de4"]["calls_into_root_total"], rl["cases"]["dev-63c30faf34"]["calls_into_root_total"]
    claim("KT-12 cặp 2", "chậm ở %s (`dev-5467884de4`) và %s (`dev-63c30faf34`)" % (pct(a["slow_share_after"]), pct(b["slow_share_after"])))
    assert a["inside_share_of_slow"] == 0 and b["inside_share_of_slow"] == 0
    a, b = rl["cases"]["dev-2bfc97b01e"]["calls_into_root_total"], rl["cases"]["dev-607751ac0a"]["calls_into_root_total"]
    claim("KT-12 cặp 3", "chậm ở %s (`dev-2bfc97b01e`, %d lời gọi) và %s (`dev-607751ac0a`, %d lời gọi)" % (pct(a["slow_share_after"]), a["n_after"], pct(b["slow_share_after"]), b["n_after"]))
    c = rl["cases"]["dev-2bfc97b01e"]["columns"]["checkoutservice_PodServerLatencyP99-s"]
    claim("KT-12 z 94", "IQR của 5 mẫu nền là %s. z tính theo độ lệch chuẩn của cùng cột là %s" % (num(c["iqr_N"], 3), num(c["z_max"], 1)))
    assert round(c["robust_z_max"]) == 94
    # --- mục 4 ---
    s = td["self_check"]
    claim("KT-8 tự kiểm", "không span nào bị bỏ ở %d/48; hạng (tốt nhất, xấu nhất) của mọi thực thể trùng bản ghi đóng băng ở %d/48" % (s["no_span_dropped"], s["ranks_equal_frozen"]))
    for c in dv["kt8"]["cases"]:
        tr = "**1**" if c["tracerca_root_rank"] == [1, 1] else "%d; `%s`" % (c["tracerca_root_rank"][0], c["tracerca_top"][0])
        claim("KT-8 " + c["opaque_id"], "| `%s` | %s | %d | %s | %d; `%s` |" % (c["opaque_id"], c["cell"].replace("ts-", "").replace("-service", "").replace("|", ", "), c["spans_dropped"], tr, c["microrank_root_rank"][0], c["microrank_top"][0]))
    claim("KT-8 hit", "%d/4 ca root hạng 1 và %d/4 trong 5 hạng đầu" % (td["error_source_hit1"], td["error_source_hit5"]))
    # --- mục 5 ---
    claim("link tự kiểm", "47/47" if all(v["cases"] == 47 and v["pass"] == 47 for v in ml["self_check"].values()) else "KHÔNG KHỚP")
    for ds, br, label in (("RE2-TT", "mo15c1", "RE2-TT, luật của bài"), ("RE2-TT", "mo1p50c1", "RE2-TT, luật của code"), ("Nezha-OB", "mo15c1", "Nezha-OB, luật của bài"), ("Nezha-OB", "mo1p50c1", "Nezha-OB, luật của code")):
        b = dv["merged_link"]["by_dataset"][ds][br]
        rd = b["reading"]
        claim("link " + label, "| %s | %d | %d | %d | %d | %d |" % (label, b["wrong_cases"], rd.get("gắn với root", 0), rd.get("không gắn", 0), rd.get("không rõ", 0), rd.get("ít span", 0)))
    pr = ml["prediction_nezha_frontend"]
    claim("link frontend", "\"Gắn với root\" ở **%d/%d và %d/%d**; \"không gắn\" %d và %d; không rõ hoặc dưới 5 span: %d và %d" % (
        pr["mo15c1"]["attached"], pr["mo15c1"]["cases_frontend_top"], pr["mo1p50c1"]["attached"], pr["mo1p50c1"]["cases_frontend_top"],
        pr["mo15c1"]["not_attached"], pr["mo1p50c1"]["not_attached"], pr["mo15c1"]["unclear_or_few"], pr["mo1p50c1"]["unclear_or_few"]))
    z = dv["merged_link"]["by_dataset"]["Nezha-OB"]
    claim("link không root", "ở %d/%d ca (luật của bài) và %d/%d ca (luật của code) **không trace nào**" % (
        z["mo15c1"]["not_attached_with_zero_root_traces"], z["mo15c1"]["reading"]["không gắn"], z["mo1p50c1"]["not_attached_with_zero_root_traces"], z["mo1p50c1"]["reading"]["không gắn"]))
    assert all(v["reading"] == "cơ chế khác, chưa giải thích" for v in pr.values())
    # --- mục 6 ---
    sc = k9["self_check"]
    assert all(v == 30 for v in sc.values())
    A = k9["all"]
    claim("KT-9 nút", "| %s | %s | %s |" % tuple("{:,}".format(A[w]["regressed_shared"]).replace(",", ".") for w in ("native", "tf", "t0")))
    claim("KT-9 lên xuống", " | ".join("%s / %s" % ("{:,}".format(A[w]["score_above_noedge"]).replace(",", "."), "{:,}".format(A[w]["score_below_noedge"]).replace(",", ".")) for w in ("native", "tf", "t0")))
    claim("KT-9 tỷ lệ", "| Tỷ lệ nút tăng | %s | %s | %s |" % tuple(pct(A[w]["share_above"]) for w in ("native", "tf", "t0")))
    for label, key in (("1 cha", "1"), ("2–4 cha", "2-4"), ("5 cha", "5"), ("6 cha", "6"), ("7 cha", "7")):
        claim("KT-9 " + label, "| Trung vị tỷ số, %s | %s | %s | %s |" % ((label,) + tuple(num(A[w]["by_n_parents"][key]["median"]) for w in ("native", "tf", "t0"))))
    claim("KT-9 8+", "| Trung vị tỷ số, từ 8 cha | **%s** | **%s** | **%s** |" % tuple(num(A[w]["by_n_parents"]["8+"]["median"]) for w in ("native", "tf", "t0")))
    claim("KT-9 cực lớn", "| Số ca có nút vượt 1e10 | %d | %d | %d |" % tuple(A[w]["cases_with_huge_node"] for w in ("native", "tf", "t0")))
    claim("KT-9 hạng 1", "| %s |" % " | ".join("%d / %d / %d" % (A[w]["root_rht"]["hit1"], A[w]["root_rht_noedge"]["hit1"], A[w]["root_da"]["hit1"]) for w in ("native", "tf", "t0")))
    claim("KT-9 202 nút", "trên %d nút có tỷ số xác định" % A["native"]["by_n_parents"]["8+"]["n"])
    m = k9["marks"]
    assert m["tf"]["ratio_8plus_below_half_of_native"] and m["t0"]["ratio_8plus_below_half_of_native"] and not m["tf"]["mark_met"] and not m["t0"]["mark_met"]
    claim("KT-9 giảm", "giảm %s điểm" % num(100 * (m["tf"]["share_above_native"] - m["tf"]["share_above"]), 1))
    cases = {c["opaque_id"]: c for c in read(base / "runs/circa-kt9-001/collect-001/summary.json")["cases"]}
    for cid, frag in (("dev-16597725c1", "15 → **1** (`dev-16597725c1`)"), ("dev-f81f88234e", "22 → 6 (`dev-f81f88234e`)"), ("dev-57546fd87b", "46 → 37 (`dev-57546fd87b`)")):
        w = cases[cid]["windows"]
        assert "%d → %d" % (w["native"]["root_da"]["root_rank_max"], w["tf"]["root_da"]["root_rank_max"]) in frag.replace("*", ""), cid
        claim("KT-9 " + cid, frag)
    claim("KT-9 số nút", "(%s, %s và %s nút qua 30 ca)" % tuple("{:,}".format(A[w]["nodes_edge_total"]).replace(",", ".") for w in ("native", "tf", "t0")))
    bad = [c for c in claims if not c["found"]]
    result = {"schema": "T032-self-check-phien13-v1", "n_claims": len(claims), "mismatch": len(bad), "not_found": bad, "claims": claims}
    with out.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for c in bad:
        print("  ?", c["label"], "|", c["fragment"])
    print("E: %d claims, mismatch %d" % (len(claims), len(bad)))


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
