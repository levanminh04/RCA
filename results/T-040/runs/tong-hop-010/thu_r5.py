"""Thử trực tiếp điều kiện đạt đầu vào sau sửa R5, trong bộ nhớ.

Gọi build_dau_vao() trên dau-vao-kiem.json thật của run 010; đổi lần lượt từng kiểm hash/phiên bản của đầu vào
được đọc (B16, ba trường pin của từng nhánh, mã chung từng tệp, đồng bộ graph gốc T-038). Mỗi lần đổi phải cho
all_checks_pass = False và tên kiểm tương ứng nằm trong danh sách không đạt. Đồng bộ graph gốc được thử bằng cách
thay kết quả tt_root_vs_model_check(), vì build_dau_vao() tự gọi hàm này. Tệp ngoài manifest được giữ ở mức
báo cáo theo thiết kế: thêm tệp giả phải vẫn cho all_checks_pass = True.
Cổng dừng của main() dựa vào all_checks_pass đã được thử ở runs/thu-r4-dau-vao-001/ (runs/tong-hop-009/thu-r4.json).

Lệnh: py -3 -X utf8 -B results/T-040/runs/tong-hop-010/thu_r5.py
"""
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "results", "T-040"))
import tong_hop as th  # noqa: E402

base = th.load_json("results/T-040/runs/tong-hop-010/dau-vao-kiem.json")


def run(mutate=None, tt_root=None):
    x = copy.deepcopy(base)
    if mutate:
        mutate(x)
    orig = th.tt_root_vs_model_check
    if tt_root is not None:
        th.tt_root_vs_model_check = lambda: tt_root
    try:
        dv = th.build_dau_vao("thu-r5", x)
    finally:
        th.tt_root_vs_model_check = orig
    return dv["all_checks_pass"], sorted(k for k, v in dv["kiem_trang_thai"].items() if not v)


cases = []
ok0, f0 = run()
cases.append({"case": "goc", "expect_pass": True, "all_checks_pass": ok0, "failed": f0})
cases.append({"case": "B16_lech", "expect_failed": "B16_equals_T037_registry",
              "res": run(lambda x: x["flashticket"].__setitem__("B16_equals_T037_registry", False))})
for br in sorted(base["pins"]):
    for k in ("manifest_sha256_equals_file", "created_utc_equals", "code_hashes_equal_V2"):
        cases.append({"case": "pin_%s_%s_lech" % (br, k), "expect_failed": "pin_%s_%s" % (br, k),
                      "res": run(lambda x, br=br, k=k: x["pins"][br].__setitem__(k, False))})
for rel in sorted(base["live_code"]):
    cases.append({"case": "ma_chung_lech:" + rel, "expect_failed": "live_code_equals_V2_pin:" + rel,
                  "res": run(lambda x, rel=rel: x["live_code"][rel].__setitem__("equals_V2_pin", False))})
fake_root = dict(th.tt_root_vs_model_check(), **{"thuc-the.json": False, "all_equal": False})
cases.append({"case": "graph_goc_TT_lech", "expect_failed": "TT_root_equals_fix_model", "res": run(tt_root=fake_root)})
extra = {"case": "tep_ngoai_manifest_chi_bao_cao", "expect_pass": True,
         "res": run(lambda x: x["extra_files_not_in_manifests"].setdefault("results/T-038", {}).__setitem__(
             "runs/gia", {"files": 1, "examples": ["results/T-038/runs/gia/x.json"]}))}
cases.append(extra)

all_ok = ok0 and not f0
for c in cases[1:]:
    p, failed = c.pop("res")
    c["all_checks_pass"], c["failed"] = p, failed
    if "expect_failed" in c:
        c["ok"] = (p is False) and failed == [c["expect_failed"]]
    else:
        c["ok"] = p is True and not failed
    all_ok = all_ok and c["ok"]
cases[0]["ok"] = ok0 and not f0
res = {"schema": "T040-thu-r5-v1", "base": "results/T-040/runs/tong-hop-010/dau-vao-kiem.json",
       "cases": cases, "all_pass": all_ok}
with open(os.path.join(ROOT, "results/T-040/runs/tong-hop-010/thu-r5.json"), "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
print(json.dumps({"all_pass": all_ok, "cases": len(cases), "fail": [c["case"] for c in cases if not c["ok"]]}, ensure_ascii=False))
