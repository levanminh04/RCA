"""H2 T-057: ma trận hạn chế P4 (G2) → thành phần M1 → kết quả theo ca trên test. Chỉ đọc; mô tả sau xem test.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h2_truy_vet.py results/T-057/truy-vet-han-che.json
Phần đo bằng máy:
  (1) "thực thể phía trên root đứng đầu" (G2-H03, H06, H17): ở ca root không đứng riêng khối đầu, đối thủ đứng đầu
      có đường gọi tới root trong extra/canh của chính vế không (trực tiếp / gián tiếp). So M1 với C-a0, ba bộ.
  (2) MRR theo loại lỗi liên quan (network_delay, return, exception) từ PT#/tach_MRR và R#/tach/fault.
  (3) root có trong tập trả về (G2-H16) từ PT#/trung_gian_theo_ca/*/M1/root_in_returned và R tương ứng.
Phần ánh xạ dòng G2 → thành phần lấy từ results/T-043/bao-cao.md §7, results/T-034/goi-g2.md §5 (UV-1, UV-2, UV-6, UV-7),
viết tay trong MATRIX dưới đây; mỗi dòng ghi nguồn.
"""
import glob
import json
import sys

PT = "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json"
R = "results/T-055/reports/re3/phan-tich-re3.json"
Q = "D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received"


def rec_of(path):
    r = json.load(open(path, encoding="utf-8"))
    return r["records"][0] if "records" in r else r


def phia_tren(canh, a, root):
    ke = {}
    for x, y in canh:
        ke.setdefault(x, set()).add(y)
    if root in ke.get(a, ()):
        return "truc_tiep"
    seen, st = {a}, [a]
    while st:
        u = st.pop()
        for v in ke.get(u, ()):
            if v == root:
                return "gian_tiep"
            if v not in seen:
                seen.add(v)
                st.append(v)
    return "khong"


def xet(rec, root):
    blocks = rec["worlds"]["P"]["blocks"] if "worlds" in rec and "P" in rec["worlds"] else rec["blocks"]
    first = [e for g in blocks[0]["groups"] for e in g] if blocks else []
    if first == [root]:
        return {"nhom": "dung"}
    comp = next((e for e in first if e != root), None)
    canh = [tuple(x) for x in rec["extra"]["canh"]]
    return {"nhom": "sai", "doi_thu": comp, "phia_tren": phia_tren(canh, comp, root) if comp else None}


def main(outp):
    pt = json.load(open(PT, encoding="utf-8"))
    r3 = json.load(open(R, encoding="utf-8"))
    items = []
    for k, v in pt["trung_gian_theo_ca"].items():
        ds, oid = k.split("|")
        root = pt["cases"][ds][oid]["root"]
        for ve in ("M1", "C-a0"):
            items.append((ds, oid, root, ve, v[ve]["result"]))
    for j in glob.glob(Q + "/ec2_*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/job.json"):
        job = json.load(open(j, encoding="utf-8"))
        arm, oid = job["slot"].get("arm"), job["slot"].get("opaque_id")
        if arm in ("M1", "C-a0"):
            items.append(("RE3-OB", oid, r3["cases"][oid]["cell"].split("|")[1], arm, j[:-len("job.json")] + "result.json"))
    per = {}
    for ds, oid, root, ve, p in sorted(items):
        per.setdefault(f"{ds}|{ve}", []).append(dict(ca=oid, root=root, **xet(rec_of(p), root)))
    dem = {}
    for key, rows in per.items():
        sai = [r for r in rows if r["nhom"] == "sai"]
        dem[key] = {"so_ca": len(rows), "sai": len(sai),
                    "doi_thu_truc_tiep_goi_root": sum(r["phia_tren"] == "truc_tiep" for r in sai),
                    "doi_thu_gian_tiep_goi_root": sum(r["phia_tren"] == "gian_tiep" for r in sai),
                    "doi_thu_khong_phia_tren": sum(r["phia_tren"] == "khong" for r in sai)}
    rir = {}
    for ds in ("RE2-TT", "Nezha-OB"):
        xs = [v["M1"]["root_in_returned"] for k, v in pt["trung_gian_theo_ca"].items() if k.startswith(ds + "|")]
        rir[ds] = {"root_trong_tap_tra_ve": sum(1 for x in xs if str(x) == "True"), "n": len(xs)}
    xs = [v["M1"]["root_in_returned"] for v in r3["trung_gian_M1_family"].values()]
    rir["RE3-OB"] = {"root_trong_tap_tra_ve": sum(1 for x in xs if str(x) == "True"), "n": len(xs)}
    loi = {"Nezha-OB": {f: pt["tach_MRR"]["Nezha-OB|fault"][f] for f in ("network_delay", "return", "exception")},
           "RE2-TT": {f: pt["tach_MRR"]["RE2-TT|fault"][f] for f in pt["tach_MRR"]["RE2-TT|fault"] if f in ("delay", "loss")},
           "RE3-OB": {f: {ve: r3["tach"]["fault"][f][ve]["rr"] for ve in ("M1", "C-a0", "simplerca") if ve in r3["tach"]["fault"][f]}
                      for f in r3["tach"]["fault"]}}
    MATRIX = [
        {"g2": "G2-H03", "han_che": "TraceRCA bản thư viện chấm thời gian chờ root thành bất thường của dịch vụ gọi", "M1": "E1 (UV-2), E2 (UV-1)",
         "nguon_anh_xa": "results/T-043/bao-cao.md §7; results/T-034/goi-g2.md UV-1, UV-2", "do": "dem/<bộ>|M1 so với dem/<bộ>|C-a0 (đối thủ phía trên root ở ca sai)"},
        {"g2": "G2-H06", "han_che": "Trễ mạng: dấu hiệu ở span phía gọi", "M1": "E2 (UV-1)",
         "nguon_anh_xa": "results/T-043/bao-cao.md §7; UV-1", "do": "loi/Nezha-OB/network_delay; loi/RE2-TT/delay, loss"},
        {"g2": "G2-H17", "han_che": "Dịch vụ phía trên đứng trước root (M5)", "M1": "E5 (tách tự sinh/kế thừa), E1, E2",
         "nguon_anh_xa": "results/T-043/bao-cao.md §7; MRP P6 tầng 2", "do": "dem (phía trên root ở ca sai); results/T-057/e5-thanh-phan.json"},
        {"g2": "G2-H07", "han_che": "Lỗi return Nezha-OB: root không hạng 1", "M1": "Không có thành phần riêng trong bản P7 (E3 tắt; UV-6 chưa vào M1)",
         "nguon_anh_xa": "results/T-056/dinh-chinh-001.md D1a (M1, C-a0 đều tắt E3/E3b); results/T-034/goi-g2.md UV-6", "do": "loi/Nezha-OB/return (mô tả)"},
        {"g2": "G2-H09", "han_che": "BARO chia cho IQR của nền gần phẳng", "M1": "Không sửa; E4 có cùng suy biến (c = 1 khi IQR = 0)",
         "nguon_anh_xa": "src/m1/e4.py:279; results/T-055/reports/re3/dinh-chinh-001.md Đ1a; results/T-056/bao-cao.md §2.3", "do": "T-056 K#/2_3_iqr0"},
        {"g2": "G2-H12", "han_che": "CIRCA: giá trị không hợp lệ lan qua cấu trúc", "M1": "Yêu cầu kỹ thuật UV-7 (chặn giá trị không hợp lệ trước khi lan)",
         "nguon_anh_xa": "results/T-034/goi-g2.md UV-7", "do": "không đo riêng trên test"},
        {"g2": "G2-H16", "han_che": "Rào cản tập ứng viên, hòa cắt biên", "M1": "Tầng 3 giữ thực thể không cờ trong tập trả về (MRP P6 tầng 4)",
         "nguon_anh_xa": "MRP P6 tầng 4; src/m1/xep_hang.py", "do": "root_trong_tap_tra_ve"},
    ]
    KHONG = [
        {"g2": ["G2-H01", "G2-H02", "G2-H04", "G2-H05"], "ly_do": "Hạn chế của bản cài MicroRank/TraceRCA; M1 không dùng bước chia trace hay gộp điểm theo tập (UV-3, UV-4 không vào M1)."},
        {"g2": ["G2-H08"], "ly_do": "Hạn chế của SimpleRCA (phiếu đếm theo mẫu). T-056 cho thấy chính đặc tính này là sức mạnh của M4 trên TT/RE3 (results/T-056/dinh-chinh-001.md D3)."},
        {"g2": ["G2-H13", "G2-H14", "G2-H15"], "ly_do": "Hạn chế riêng của CIRCA/TORAI; M1 không dùng hồi quy theo nút cha hay bước nhân quả (results/T-043/bao-cao.md §7)."},
        {"g2": ["G2-H10", "G2-H19", "G2-H24", "G2-H25"], "ly_do": "Hạn chế dữ liệu; phương pháp không sửa được dữ liệu chưa ghi (AGENTS luật 17). Chuyển thành yêu cầu quan sát P9."},
        {"g2": ["G2-H11", "G2-H18"], "ly_do": "Chưa phân xử ở G2; M1 không có thành phần nhắm riêng. G2-H11 (thực thể ngoài chuỗi gọi) liên quan cơ chế max-z kênh hẹp ở T-054 §7.5, chưa nối thành bằng chứng."},
        {"g2": ["G2-H20", "G2-H21", "G2-H22", "G2-H23", "G2-H26"], "ly_do": "Chế độ (b), hoãn theo Q-245."},
    ]
    out = {"lenh": "py -3 -B results/T-057/scripts/h2_truy_vet.py " + outp, "ma_tran": MATRIX, "khong_thuoc_M1": KHONG,
           "dem": dem, "loi": loi, "root_trong_tap_tra_ve": rir, "theo_ca": per,
           "gioi_han": "Mô tả sau khi xem test (C-15 B). 'Phía trên' tính trên extra/canh của chính vế (cạnh quan sát N ∪ A). Không cộng các dòng thành tỷ lệ nguyên nhân."}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(dem, ensure_ascii=False))
    print(json.dumps(rir, ensure_ascii=False))
    print(json.dumps(loi, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main(sys.argv[1])
