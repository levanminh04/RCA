"""So tong-hop.json và dau-vao.json của run 008 với run 009 (Phiên 6: sửa R4, chỉ đổi luồng dừng trong main(); snapshot quyết định thêm Q-172).
Kỳ vọng: tong-hop.json không đổi ngoài trường run; dau-vao.json chỉ đổi phần snapshot quyết định.
Lệnh: py -3 -X utf8 -B results/T-040/runs/tong-hop-009/so_sanh_008_009.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
R = lambda run, f: json.load(open(os.path.join(ROOT, "results/T-040/runs/%s/%s" % (run, f)), encoding="utf-8"))
old, new = R("tong-hop-008", "tong-hop.json"), R("tong-hop-009", "tong-hop.json")
SKIP = {"_trich_tu_raw", "run", "tep", "nguon", "tung_graph", "luu_y"}
rows = []


def diff(a, b, path):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in SKIP:
                diff(a.get(k), b.get(k), path + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif a != b:
        rows.append({"pointer": path, "run008": a, "run009": b})


diff(old["he_thong"], new["he_thong"], "/he_thong")
diff(old["lan_theo"], new["lan_theo"], "/lan_theo")
diff(old["nguon_trace_T035"], new["nguon_trace_T035"], "/nguon_trace_T035")
NEW_KEYS = ()
status_like = lambda r: False
other = [r for r in rows if not r["pointer"].startswith(NEW_KEYS) and not status_like(r)]
summary = {
    "rows": len(rows),
    "status_string_changes": sum(status_like(r) for r in rows),
    "new_key_rows": sum(r["pointer"].startswith(NEW_KEYS) for r in rows),
    "other_changes": [r["pointer"] for r in other],
    "all_existing_numbers_unchanged": not other,
}
dv_old, dv_new = R("tong-hop-008", "dau-vao.json"), R("tong-hop-009", "dau-vao.json")
summary["dau_vao_manifest_hashes_equal"] = [(m["id"], m["manifest_sha256"]) for m in dv_old["manifest"]] == \
    [(m["id"], m["manifest_sha256"]) for m in dv_new["manifest"]]
summary["dau_vao_all_checks_pass_009"] = dv_new["all_checks_pass"]
dvd = []
def d2(a, b, path):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in {"run", "chi_tiet", "manifest"}:
                d2(a.get(k), b.get(k), path + "/" + k)
    elif a != b:
        dvd.append(path)
d2(dv_old, dv_new, "")
summary["dau_vao_changed_pointers"] = dvd
summary["dau_vao_changes_only_decision_snapshot"] = all(p.startswith("/doi_chieu_quyet_dinh_T038") for p in dvd)
json.dump({"tom_tat": summary, "khac_biet": rows},
          open(os.path.join(ROOT, "results/T-040/runs/tong-hop-009/so-sanh-008-009.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False))
