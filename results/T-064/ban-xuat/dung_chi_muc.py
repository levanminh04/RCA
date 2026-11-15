# Dựng chi-muc-ban.json từ đầu ra đã lưu (chỉ đọc). Hợp đồng: hop-dong-dau-ra.md mục 3.
# Bản 2 (14/11/2026, sau quyết định Minh chọn V082): P7 (khoa_P7), V082 (de_xuat), V071 = V082 + H1c (thay_the, có đầu ra cạnh).
# Ca: dev2 (13) + dev3 bản 3 (6: 4 ca tập chọn + 2 ca lặp độ nhạy) + T-062 (9). Ca lỗi chạy: dau_ra null, ghi loi_chay.
# Bản tạm trước giữ ở chi-muc-ban-tam-1.json (dựng bằng dung_chi_muc_tam1.py).
# Sửa 14/11 16:57Z (T-065 L8): cau_hinh_sha256 = src/m1_ft/chay.py::sha_cau_hinh (JSON chuẩn hóa, cùng quy ước sổ và đầu ra);
# hash byte file ghi riêng ở cau_hinh_file_sha256. Kiểm: mọi đầu ra của bản có extra.m1_ft.cau_hinh_sha256 và ma_nguon_sha256 trùng chỉ mục.
# Bản 3 (15/11, REVIEW-4 R9, WHY-99): slot ebd5ef38 của V082/V071 lấy đầu ra chạy lại kiem/nhan-r9/r9/ (live-down theo lần dò mới nhất);
# bản 2 giữ ở chi-muc-ban-2.json (dựng bằng dung_chi_muc_2.py).
# Chạy bằng môi trường ghim (cần numpy): PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages D:/RCA-ext/envs/py312-pin/Scripts/python.exe
import json, hashlib, pathlib
R = pathlib.Path(__file__).resolve().parents[1]   # results/T-064
G = R.parent.parent                                # repo
import sys; sys.path.insert(0, str(G))
from src.m1_ft import chay as ft  # noqa: E402
T62 = R.parent / "T-062" / "ca"
L5 = R / "kiem/nhan-luot5/l5"
R9 = R / "kiem/nhan-r9/r9"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(G).as_posix()
dev2 = (R / "kiem/ca-dev2-13.txt").read_text().split()
t62 = (R / "kiem/ca-t062-9.txt").read_text().split()
dev3 = [c["ma"] for c in json.loads((R / "tap-dev3-19-do-nhay.json").read_text(encoding="utf8"))["ca"] if c["ma"] not in dev2]
assert len(dev2) == 13 and len(t62) == 9 and len(dev3) == 6, (len(dev2), len(t62), len(dev3))
def muc(c, nguon, d):
    p = d / "method-output-1.json"
    if p.exists():
        return {"ca": c, "nguon": nguon, "dau_ra": rel(p), "sha256": sha(p)}
    e = d / "loi-chay.json"
    assert e.exists(), d
    return {"ca": c, "nguon": nguon, "dau_ra": None, "sha256": None, "loi_chay": rel(e)}
def ca_list(tim):
    return [muc(c, g, tim(g, c)) for g, ds in (("dev2", dev2), ("dev3", dev3), ("t062", t62)) for c in ds]
so = [json.loads(l) for l in (R / "so-bien-the.jsonl").read_text(encoding="utf8").splitlines() if l.strip()]
def tim_p7(g, c):
    return {"dev2": R / "cham/dau-ra-dev2/P7" / c, "dev3": R / "cham/dau-ra-dev3/P7" / c, "t062": T62 / c / "outputs" / c}[g]
ban = [{"ban": "p7", "mo_ta": "M1 P7 đã khóa (nền)", "cau_hinh_sha256": None, "ma_nguon_sha256": None, "trang_thai": "khoa_P7",
        "cac_ca": ca_list(tim_p7)}]
for ma, mo_ta, tt in [("V082-V066+H8a", "P7 + H5b (chết im ≥60 s) + sàn 1 ms (H8s1) + adapter gộp chuỗi runtime (H8a); bản đề xuất cuối "
                       "(Minh chọn 14/11/2026, DECISIONS; hồ sơ chọn §15)", "de_xuat"),
                      ("V071-V041+H8a", "V082 + H1c (cạnh dùng chung, đã sửa R1): bản thay thế có đầu ra cạnh; kém V082 0,5 hạng ở hai ca", "thay_the")]:
    e = next(x for x in so if x.get("ma") == ma and x.get("loai") == "truoc_cham")
    f = R / "bien-the" / ma / "cau-hinh.json"
    sc = ft.sha_cau_hinh(json.loads(f.read_text(encoding="utf8")))
    cac = ca_list(lambda g, c, ma=ma: (R9 / g / "d0" / ma / c) if (R9 / g / "d0" / ma / c / "method-output-1.json").exists() else (L5 / g / "d0" / ma / c))
    for x in cac:  # đầu ra phải ghi đúng cấu hình và mã nguồn của bản
        m = json.loads((G / x["dau_ra"]).read_text(encoding="utf8"))["extra"]["m1_ft"]
        assert (m["cau_hinh_sha256"], m["ma_nguon_sha256"]) == (sc, e["ma_nguon_sha256"]), (ma, x["ca"])
    ban.append({"ban": ma, "mo_ta": mo_ta, "cau_hinh_sha256": sc, "cau_hinh_file_sha256": sha(f), "ma_nguon_sha256": e["ma_nguon_sha256"],
                "trang_thai": tt, "cac_ca": cac})
out = {"ban_hop_dong": 1, "phien_ban_chi_muc": 3, "sua": "bản 2 16:57Z 14/11: cau_hinh_sha256 theo sha_cau_hinh (T-065 L8); bản 3 15/11: slot ebd5ef38 V082/V071 theo R9 (WHY-99)",
       "ghi_chu": "Bản đề xuất cuối V082 (Minh chọn 14/11/2026). Không chứa đáp án. Bản trước: chi-muc-ban-2.json, chi-muc-ban-tam-1.json.", "ban": ban}
(R / "ban-xuat/chi-muc-ban.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf8")
print([(b["ban"], len(b["cac_ca"]), sum(1 for x in b["cac_ca"] if x["dau_ra"] is None)) for b in ban])
