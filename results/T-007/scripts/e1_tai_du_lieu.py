"""T-007 E1: tải dữ liệu lên EC2 và kiểm hash. Chạy bằng python3 hệ thống (chỉ thư viện chuẩn).

1. RE2-OB từ Hugging Face `phamquiluan/RCAEval`, revision cố định: `traces.parquet` và `inject_time.txt`
   của các ca `re2ob_*`. Ghi vào ~/rca/data/re2ob/<ca>/.
   - Danh sách ca: đọc cây thư mục gốc của repo ở đúng revision, lọc NGAY tiền tố `re2ob_`.
     Tên các ca khác (trong đó có ca RE2-TT đang khóa) không lưu, không in.
   - Hash mong đợi lấy từ API cây thư mục của HF: file LFS có SHA-256 (`lfs.oid`);
     file nhỏ không qua LFS chỉ có git blob oid (SHA-1 của "blob <size>\\0" + nội dung).
2. `fse-ob.zip` từ Zenodo 11046533, kiểm MD5 theo API Zenodo, giải nén vào ~/rca/data/fse/.

Không tải `cases.parquet` (file khóa: có nhãn của mọi ca) hay bất kỳ ca nào khác.
Chạy: mkdir -p ~/rca/runs/e1 && nohup python3 ~/rca/scripts/e1_tai_du_lieu.py > ~/rca/runs/e1/e1.log 2>&1 &
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import zipfile

REPO = "phamquiluan/RCAEval"
REV = "afeacb11bcc94dadfd1c8f483ee4377b2b8b614e"
API = "https://huggingface.co/api/datasets/%s/tree/%s" % (REPO, REV)
RES = "https://huggingface.co/datasets/%s/resolve/%s" % (REPO, REV)
ZENODO_API = "https://zenodo.org/api/records/11046533"
ZENODO_FILE = "fse-ob.zip"

R = os.path.expanduser("~/rca")
D_RE2 = os.path.join(R, "data", "re2ob")
D_FSE = os.path.join(R, "data", "fse")
D_LOG = os.path.join(R, "runs", "e1")
CAN = ["traces.parquet", "inject_time.txt"]
UA = {"User-Agent": "T-007-rca-research"}


def ts():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(*a):
    print(ts(), *a, flush=True)


def get(url):
    """GET có thử lại; trả (bytes, headers)."""
    for lan in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read(), r.headers
        except Exception as e:
            log("  thử lại", lan + 1, url, type(e).__name__, e)
            time.sleep(5 * (lan + 1))
    raise RuntimeError("không tải được " + url)


def get_json_pages(url):
    """API cây thư mục của HF phân trang qua header Link rel=next."""
    out = []
    while url:
        body, h = get(url)
        out.extend(json.loads(body))
        m = re.search(r'<([^>]+)>;\s*rel="next"', h.get("Link", "") or "")
        url = m.group(1) if m else None
    return out


def tai_file(url, dich):
    """Tải theo luồng, tính đồng thời SHA-256, MD5 và git blob oid. Ghi vào file tạm rồi đổi tên."""
    tam = dich + ".tai"
    for lan in range(4):
        try:
            sha256, md5, n = hashlib.sha256(), hashlib.md5(), 0
            chunks_sha1 = hashlib.sha1()
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r, open(tam, "wb") as f:
                size_hdr = r.headers.get("Content-Length")
                # git blob oid cần biết kích thước trước; dùng Content-Length, kiểm lại sau
                if size_hdr is not None:
                    chunks_sha1.update(b"blob %d\0" % int(size_hdr))
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
                    sha256.update(b)
                    md5.update(b)
                    chunks_sha1.update(b)
                    n += len(b)
            git_oid = chunks_sha1.hexdigest() if size_hdr is not None and int(size_hdr) == n else None
            if git_oid is None:  # tính lại từ đĩa
                s = hashlib.sha1(b"blob %d\0" % n)
                with open(tam, "rb") as f:
                    for b in iter(lambda: f.read(1 << 20), b""):
                        s.update(b)
                git_oid = s.hexdigest()
            os.replace(tam, dich)
            return {"size": n, "sha256": sha256.hexdigest(), "md5": md5.hexdigest(), "git_oid": git_oid}
        except Exception as e:
            log("  thử lại", lan + 1, url, type(e).__name__, e)
            time.sleep(5 * (lan + 1))
    raise RuntimeError("không tải được " + url)


def re2ob():
    log("RE2-OB: đọc cây thư mục gốc, lọc tiền tố re2ob_")
    goc = get_json_pages(API)
    cases = sorted(e["path"] for e in goc if e.get("type") == "directory" and e["path"].startswith("re2ob_"))
    tong_goc = len(goc)
    del goc  # không giữ tên các ca khác
    log("số mục ở gốc:", tong_goc, "| số ca re2ob_:", len(cases))
    manifest, loi = [], 0
    for i, c in enumerate(cases, 1):
        files = {e["path"].split("/")[-1]: e for e in get_json_pages(API + "/" + c) if e.get("type") == "file"}
        os.makedirs(os.path.join(D_RE2, c), exist_ok=True)
        for name in CAN:
            e = files.get(name)
            if e is None:
                log("THIEU", c, name)
                manifest.append({"case": c, "file": name, "ok": False, "loi": "không có trên HF"})
                loi += 1
                continue
            mong = {"size": e["size"], "git_oid": e["oid"]}
            if e.get("lfs"):
                mong["sha256"] = e["lfs"]["oid"]
            dich = os.path.join(D_RE2, c, name)
            t0 = time.time()
            thuc = tai_file(RES + "/" + c + "/" + name, dich)
            if "sha256" in mong:
                ok = thuc["sha256"] == mong["sha256"] and thuc["size"] == mong["size"]
                cach = "sha256 (LFS)"
            else:
                ok = thuc["git_oid"] == mong["git_oid"] and thuc["size"] == mong["size"]
                cach = "git blob oid"
            loi += 0 if ok else 1
            manifest.append({"case": c, "file": name, "cach_kiem": cach, "mong": mong, "thuc": thuc, "ok": ok,
                             "giay": round(time.time() - t0, 1)})
        log("%2d/%d %s %s" % (i, len(cases), c, "ok" if all(m["ok"] for m in manifest if m["case"] == c) else "LOI"))
    with open(os.path.join(D_LOG, "manifest-re2ob.json"), "w") as f:
        json.dump({"nguon": "HF datasets/%s" % REPO, "revision": REV, "so_ca": len(cases), "files": manifest}, f, indent=1)
    tong = sum(m["thuc"]["size"] for m in manifest if "thuc" in m)
    log("RE2-OB xong: %d ca, %d file, %.1f MB, số file lỗi: %d" % (len(cases), len(manifest), tong / 1e6, loi))
    return loi


def fse_ob():
    log("fse-ob: đọc API Zenodo")
    rec = json.loads(get(ZENODO_API)[0])
    f = [x for x in rec["files"] if x["key"] == ZENODO_FILE][0]
    md5_mong = f["checksum"].split(":", 1)[1]
    url = "https://zenodo.org/records/11046533/files/%s?download=1" % ZENODO_FILE
    os.makedirs(D_FSE, exist_ok=True)
    zp = os.path.join(D_FSE, ZENODO_FILE)
    t0 = time.time()
    thuc = tai_file(url, zp)
    ok = thuc["md5"] == md5_mong and thuc["size"] == f["size"]
    log("fse-ob.zip: %d B, md5 %s, mong %s -> %s (%.0f s)" % (thuc["size"], thuc["md5"], md5_mong, "KHOP" if ok else "LECH",
                                                            time.time() - t0))
    if ok:
        with zipfile.ZipFile(zp) as z:
            z.extractall(D_FSE)
        d = os.path.join(D_FSE, "fse-ob")
        dem = {}
        for root, _, fs in os.walk(d):
            for x in fs:
                dem[x] = dem.get(x, 0) + 1
        log("giải nén xong; số file theo tên:", json.dumps(dem, sort_keys=True))
    with open(os.path.join(D_LOG, "manifest-fse-ob.json"), "w") as fo:
        json.dump({"nguon": ZENODO_API, "file": ZENODO_FILE, "md5_zenodo": md5_mong, "size_zenodo": f["size"],
                   "thuc": thuc, "ok": ok}, fo, indent=1)
    return 0 if ok else 1


def main():
    os.makedirs(D_LOG, exist_ok=True)
    log("BAT_DAU E1")
    loi = fse_ob() + re2ob()
    log("E1_XONG, tổng lỗi:", loi)
    sys.exit(1 if loi else 0)


if __name__ == "__main__":
    main()
