"""T-007: thống kê từ các khối nén trong results/T-007/runs/, để mọi số trong kiem-dung-dan.md có file nguồn.

Đọc thẳng file trong .tar.gz (không cần giải nén). Ghi results/T-007/cham/thong-ke.json và in tóm tắt.
Nội dung:
- thu_hang[<env>/<khối>]: số ca, số thao tác trả về (min, max), mẫu 4 service đầu (MicroRank), service đứng đầu
  (TraceRCA), service gốc có bao giờ xuất hiện, giá trị trung gian của cửa sổ (số span, tỉ lệ span trước/sau mốc).
- so_sanh: giống từng byte giữa các cặp khối; với cặp lượt chính / xáo: thứ hạng service và hạng đáp án.
- bocpd[<env>]: số ca, số ca giống kết quả tác giả lưu, TP/FP/FN, P/R/F1, FP theo loại lỗi; so điểm đổi giữa hai bộ.
- trung_gian_microrank: số trace của đồ thị bất thường so với số trace sau mốc, số thao tác nf<0, tương quan hạng
  (Spearman) giữa điểm Dstar2 và số trace sau mốc qua thao tác.
Tên ca chỉ dùng để chấm và thống kê, không vào phương pháp.

Chạy: py -3 thong_ke.py   (từ gốc repo)
"""
import collections
import json
import os
import sys
import tarfile

RUNS = os.path.join("results", "T-007", "runs")
OUT = os.path.join("results", "T-007", "cham", "thong-ke.json")


def doc_tar(path):
    """{tên trong tar: bytes} cho mọi file thường."""
    d = {}
    with tarfile.open(path) as t:
        for m in t.getmembers():
            if m.isfile():
                d[m.name] = t.extractfile(m).read()
    return d


def svc(op):
    return op.split("_")[0].replace("-db", "")


def svc_ranks(ranks):
    s = []
    for op in ranks:
        if svc(op) not in s:
            s.append(svc(op))
    return s


def ket_qua(d, khoi):
    """{tên file: ranks} của khối."""
    pre = khoi + "/results/"
    return {k[len(pre):]: json.loads(v)["0"] for k, v in d.items() if k.startswith(pre) and k.endswith(".json")
            and not k.endswith("_failed.json")}


def jsonl(b):
    return [json.loads(x) for x in b.decode("utf-8").splitlines() if x.strip()]


def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den


def thong_ke_khoi(d, khoi):
    kq = ket_qua(d, khoi)
    td = jsonl(d[khoi + "/tien-do.jsonl"])
    out = {"so_ca": len(kq), "so_thao_tac_min_max": [min(x["so_hang"] for x in td), max(x["so_hang"] for x in td)],
           "trang_thai": dict(collections.Counter(x["trang_thai"] for x in td)),
           "span_cua_so_min_max": [min(x["span_cua_so"] for x in td), max(x["span_cua_so"] for x in td)],
           "ti_le_truoc_sau_min_max": [round(min(x["span_truoc"] / x["span_sau"] for x in td), 2),
                                       round(max(x["span_truoc"] / x["span_sau"] for x in td), 2)],
           "ca_ti_le_truoc_sau_tren_1_3": sorted([x["case"], round(x["span_truoc"] / x["span_sau"], 2)] for x in td
                                                 if x["span_truoc"] / x["span_sau"] > 1.3),
           "giay_moi_ca_trung_binh_khong_phai_so_do": round(sum(x["giay"] for x in td) / len(td), 1)}
    top4 = collections.Counter()
    top1 = collections.Counter()
    xuat_hien = collections.Counter()
    for f, r in kq.items():
        s = svc_ranks(r)
        top4[", ".join(s[:4])] += 1
        top1[s[0] if s else "-"] += 1
        for v in set(s):
            xuat_hien[v] += 1
    out["mau_4_service_dau"] = dict(top4.most_common())
    out["service_dung_dau"] = dict(top1.most_common())
    out["so_ca_service_xuat_hien_trong_thu_hang"] = dict(sorted(xuat_hien.items()))
    return out, kq


def so_cap(ka, kb):
    giong = sum(1 for f in ka if f in kb and ka[f] == kb[f])
    svc_giong = sum(1 for f in ka if f in kb and svc_ranks(ka[f]) == svc_ranks(kb[f]))
    doi = []
    for f in ka:
        ans = f.split("_")[0]
        sa, sb = svc_ranks(ka[f]), svc_ranks(kb.get(f, []))
        ra = sa.index(ans) + 1 if ans in sa else None
        rb = sb.index(ans) + 1 if ans in sb else None
        if ra != rb:
            doi.append([f, ra, rb])
    return {"so_file_chung": len(set(ka) & set(kb)), "thu_hang_giong_tung_thao_tac": giong,
            "thu_hang_service_giong": svc_giong, "so_ca_hang_dap_an_doi": len(doi), "ca_hang_dap_an_doi": doi}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out = {"thu_hang": {}, "so_sanh": {}, "bocpd": {}, "trung_gian_microrank": []}
    kq = {}
    for env in ["py312-pin", "py312"]:
        for khoi in ["microrank", "tracerca", "microrank-lai", "tracerca-lai", "microrank-tron", "tracerca-tron",
                     "microrank-L20", "tracerca-L20", "tracerca-hoi-quy"]:
            p = os.path.join(RUNS, env, khoi + ".tar.gz")
            if not os.path.exists(p):
                continue
            d = doc_tar(p)
            out["thu_hang"][env + "/" + khoi], kq[env + "/" + khoi] = thong_ke_khoi(d, khoi)
        p = os.path.join(RUNS, env, "bocpd.tar.gz")
        if os.path.exists(p):
            L = jsonl(doc_tar(p)["bocpd/tien-do.jsonl"])
            ca = [x for x in L if "i" in x]
            tp = sum(x["tp"] for x in ca)
            fp = sum(x["fp"] for x in ca)
            fn = sum(1 - x["tp"] for x in ca)
            pr, rc = tp / (tp + fp), tp / (tp + fn)
            out["bocpd"][env] = {"so_ca": len(ca), "dong_khac": [x for x in L if "i" not in x],
                                 "giong_tac_gia": sum(x["giong_tac_gia"] for x in ca), "tp": tp, "fp": fp, "fn": fn,
                                 "precision": pr, "recall": rc, "f1": 2 * pr * rc / (pr + rc),
                                 "fp_theo_loi": dict(collections.Counter(x["case"].split("/")[1].split("_")[1]
                                                                         for x in ca if x["fp"])),
                                 "giay": [min(x["giay"] for x in ca), max(x["giay"] for x in ca)],
                                 "cps": {x["case"]: x["cps"] for x in ca}}
    if len(out["bocpd"]) == 2:
        a, b = out["bocpd"]["py312-pin"]["cps"], out["bocpd"]["py312"]["cps"]
        out["so_sanh"]["bocpd py312-pin vs py312: so ca cung diem doi"] = sum(a[c] == b.get(c) for c in a)
    for v in out["bocpd"].values():
        del v["cps"]
    cap = [("py312-pin/microrank", "py312/microrank"), ("py312-pin/tracerca", "py312/tracerca"),
           ("py312-pin/microrank", "py312-pin/microrank-lai"), ("py312-pin/tracerca", "py312-pin/tracerca-lai"),
           ("py312/microrank", "py312/microrank-lai"), ("py312/tracerca", "py312/tracerca-lai"),
           ("py312-pin/microrank", "py312-pin/microrank-tron"), ("py312-pin/tracerca", "py312-pin/tracerca-tron"),
           ("py312-pin/tracerca", "py312-pin/tracerca-hoi-quy"),
           ("py312-pin/microrank", "py312-pin/microrank-L20"), ("py312-pin/tracerca", "py312-pin/tracerca-L20")]
    for x, y in cap:
        if x in kq and y in kq:
            ka = {f: r for f, r in kq[x].items() if f in kq[y]} if y.endswith(("-lai", "-hoi-quy")) else kq[x]
            out["so_sanh"][x + " vs " + y] = so_cap(ka, kq[y])
    p = os.path.join(RUNS, "py312-pin", "microrank-trung-gian.tar.gz")
    if os.path.exists(p):
        for r in jsonl(doc_tar(p)["microrank-trung-gian/trung-gian.jsonl"]):
            t = r["pho"]["tung_thao_tac"]
            ops = list(t)
            out["trung_gian_microrank"].append({
                "case": r["case"], "giong_luot_chinh": r["giong_luot_chinh"],
                "so_trace_sau_moc": r["so_trace_sau_moc"], "so_trace_do_thi_bat_thuong": r["bat_thuong"]["so_trace"],
                "so_trace_do_thi_binh_thuong": r["binh_thuong"]["so_trace"],
                "anomaly_list_len": r["pho"]["anomaly_list_len"], "normal_list_len": r["pho"]["normal_list_len"],
                "so_thao_tac": len(ops), "so_thao_tac_nf_am": r["pho"]["so_nf_am"],
                "spearman_diem_vs_so_trace_sau_moc": round(spearman([t[o]["dstar2"] for o in ops],
                                                                    [t[o]["so_trace_qua_sau"] for o in ops]), 3)})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False)[:20000])


if __name__ == "__main__":
    main()
