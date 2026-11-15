# Dựng chi-muc-ban.json từ đầu ra đã lưu (chỉ đọc). Hợp đồng: hop-dong-dau-ra.md mục 3.
import json, hashlib, pathlib
R = pathlib.Path(__file__).resolve().parents[1]   # results/T-064
T62 = R.parent / "T-062" / "ca"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
dev2 = [l.strip() for l in (R/"kiem/ca-dev2-13.txt").read_text().split() if l.strip()]
t62 = [l.strip() for l in (R/"kiem/ca-t062-9.txt").read_text().split() if l.strip()]
def ca_list(ban, dir_dev2, dir_t62):
    out = []
    for c in dev2:
        p = dir_dev2/c/"method-output-1.json"
        out.append({"ca": c, "nguon": "dev2", "dau_ra": str(p.relative_to(R.parent.parent)).replace("\\","/"), "sha256": sha(p)})
    for c in t62:
        p = dir_t62(c)
        out.append({"ca": c, "nguon": "t062", "dau_ra": str(p.relative_to(R.parent.parent)).replace("\\","/"), "sha256": sha(p)})
    return out
ban = []
# P7
ban.append({"ban":"p7","mo_ta":"M1 P7 đã khóa (nền)","cau_hinh_sha256":None,"ma_nguon_sha256":None,"trang_thai":"khoa_P7",
  "cac_ca": ca_list("p7", R/"cham/dau-ra-dev2/P7", lambda c: T62/c/"outputs"/c/"method-output-1.json")})
for ma,mo_ta,tt,lt in [("V032-H5b","P7 + H5b (thành phần chết im ≥60 s đặt nhóm đầu); đề xuất tạm theo §5 trên tập 13 ca","de_xuat","2"),
                       ("V041-R1-H1c+H5b+H8s1","H1c (cạnh dùng chung, đã sửa R1) + H5b + sàn 1 ms; bản thay thế có đầu ra cạnh","thay_the","3")]:
    d = R/"bien-the"/ma
    cfg = json.loads((R/"so-bien-the.jsonl").read_text(encoding="utf8").splitlines()[0]) if False else None
    ent = [json.loads(l) for l in (R/"so-bien-the.jsonl").read_text(encoding="utf8").splitlines() if l.strip()]
    e = next(x for x in ent if x.get("ma")==ma and x.get("loai")=="truoc_cham")
    ban.append({"ban":ma,"mo_ta":mo_ta,"cau_hinh_sha256":e["cau_hinh_sha256"],"ma_nguon_sha256":e["ma_nguon_sha256"],"trang_thai":tt,
      "cac_ca": ca_list(ma, R/"cham/dau-ra-dev2"/ma, lambda c,ma=ma,lt=lt: R/"bien-the"/ma/("ra-khong-hoi-quy-"+lt)/c/"method-output-1.json")})
out = {"ban_hop_dong":1,"ghi_chu":"Chỉ mục thử cho T-065. V032 và V041 chưa khóa; xem results/T-064/ho-so-chon.md. Không chứa đáp án.","ban":ban}
(R/"ban-xuat/chi-muc-ban.json").write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding="utf8")
print([(b["ban"],len(b["cac_ca"])) for b in ban])
