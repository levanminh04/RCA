r"""T-006 phiên 2, yêu cầu 1 của Minh: kiểm từng khối trên file thật trong results/T-006/runs/*.tar.gz.

Với mỗi file nén: đọc meta.json (trạng thái, lệnh), đếm file kết quả từng ca trong output/results/, tìm "Traceback",
"failed (" trong stdout.log và stderr.log, kiểm lệnh có "--test" không, so số ca với số mong đợi theo dataset
(torai-ob/torai-ss 90; fse-ob/fse-ss 100; online-boutique/re1-ob 125; N-Sigma phát hiện 200 = 100 ca × 2 biến thể).
Khối không ghi file từng ca (ví dụ BARO, reproduce_baro, RQ4, GDN): số ca mong đợi = 0, kiểm stdout có dòng kết quả.
Khối "thu-*" là chạy thử đường ống, chủ ý dùng --test (2 ca); báo riêng. Khối "*-hong" là lượt hỏng giữ lại; báo riêng.
Khối chạy bằng chay_fse.py không in điểm (chỉ ghi file từng ca; điểm do cham.py tính), nên không đòi dòng kết quả ở stdout.
Ghi: cham/kiem-khoi.txt, cham/kiem-khoi.json.
Cách dùng: python kiem_khoi.py
"""
import json
import re
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs"
OUT = HERE.parent / "cham"


def mong_doi(ten, cmd):
    s = " ".join(cmd)
    if "nsigma_phat_hien.py" in s:
        return 200
    if "chay_gdn.py" in s or "vi_du_baro.py" in s or r"baro\main.py" in s:
        return 0
    m = re.search(r"--dataset (\S+)", s)
    ds = m.group(1) if m else ""
    n = {"torai-ob": 90, "torai-ss": 90, "fse-ob": 100, "fse-ss": 100, "online-boutique": 125, "re1-ob": 125}.get(ds)
    if "--test" in cmd:
        return 2
    return n


def dau_hieu_ket_qua(stdout):
    for pat in ("--- Evaluation results ---", "Avg@5 Acc", "KET-QUA", "TONG ", "Reproduce", r"^\[0\."):
        if re.search(pat, stdout, re.M):
            return True
    return False


rows = []
for tgz in sorted(RUNS.glob("*.tar.gz")):
    ten = tgz.name[:-7]
    if ten in ("01-cai-python38",):
        continue
    with tarfile.open(tgz) as t:
        names = t.getnames()
        get = lambda suffix: next((n for n in names if n.endswith(suffix)), None)
        def doc(suffix):
            n = get(suffix)
            return t.extractfile(n).read().decode("utf-8", "replace") if n else ""
        meta = json.loads(doc("/meta.json") or "{}")
        so_ca = sum(1 for n in names if "/output/results/" in n and n.endswith(".json"))
        so, se = doc("/stdout.log"), doc("/stderr.log")
    cmd = meta.get("cmd", [])
    md = mong_doi(ten, cmd)
    r = {"khoi": ten, "trang_thai": meta.get("trang_thai"), "returncode": meta.get("returncode"),
         "co_test": "--test" in cmd, "so_ca": so_ca, "mong_doi": md,
         "traceback": ("Traceback" in so) + ("Traceback" in se), "failed_dong": se.count("failed (") + so.count("failed ("),
         "co_ket_qua_stdout": dau_hieu_ket_qua(so), "giay": meta.get("giay"), "lenh": " ".join(cmd[1:])}
    loi = []
    if r["trang_thai"] != "XONG rc=0":
        loi.append("trạng thái")
    if r["co_test"] and not ten.startswith("thu-"):
        loi.append("có --test")
    if md is None or so_ca != md:
        loi.append(f"số ca {so_ca} ≠ {md}")
    if r["traceback"]:
        loi.append("Traceback")
    if not r["co_ket_qua_stdout"] and "chay_fse.py" not in " ".join(cmd):
        loi.append("stdout không có dòng kết quả")
    r["dat"] = not loi
    r["loi"] = loi
    rows.append(r)

lines = [f"{'khối':48} {'trạng thái':12} {'ca':>4}/{'mđ':<4} {'--test':6} {'Tb':>2} {'failed(':>7} {'đạt':4} lỗi"]
for r in rows:
    lines.append(f"{r['khoi']:48} {str(r['trang_thai']):12} {r['so_ca']:>4}/{str(r['mong_doi']):<4} {str(r['co_test']):6} "
                 f"{r['traceback']:>2} {r['failed_dong']:>7} {'ĐẠT' if r['dat'] else 'KHÔNG':4} {'; '.join(r['loi'])}")
thu = [r for r in rows if r["khoi"].startswith("thu-")]
hong = [r for r in rows if r["khoi"].endswith("-hong")]
chinh = [r for r in rows if not r["khoi"].startswith("thu-") and not r["khoi"].endswith("-hong")]
lines.append("")
lines.append(f"Khối chính: {len(chinh)}; đạt: {sum(r['dat'] for r in chinh)}; không đạt: {[r['khoi'] for r in chinh if not r['dat']]}")
lines.append(f"Khối chạy thử (thu-*, chủ ý --test): {len(thu)}; đạt: {sum(r['dat'] for r in thu)}")
lines.append(f"Lượt hỏng giữ lại (*-hong, luật cứng 10; không dùng làm bằng chứng): {[(r['khoi'], '; '.join(r['loi'])) for r in hong]}")
lines.append(f"Khối có dòng 'failed (': {[(r['khoi'], r['failed_dong']) for r in rows if r['failed_dong']]}")
(OUT / "kiem-khoi.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
(OUT / "kiem-khoi.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(lines))
