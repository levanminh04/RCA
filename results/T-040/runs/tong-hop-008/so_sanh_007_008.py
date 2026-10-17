"""So tong-hop.json và dau-vao.json của run 007 với run 008 (Phiên 5: trạng thái TT sau Q-171, kiểm quyết định theo snapshot, lần theo static-only TT).
Kỳ vọng: chỉ đổi chuỗi trạng thái và thêm khóa mới; mọi số đã có giữ nguyên.
Lệnh: py -3 -X utf8 -B results/T-040/runs/tong-hop-008/so_sanh_007_008.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
R = lambda run, f: json.load(open(os.path.join(ROOT, "results/T-040/runs/%s/%s" % (run, f)), encoding="utf-8"))
old, new = R("tong-hop-007", "tong-hop.json"), R("tong-hop-008", "tong-hop.json")
SKIP = {"_trich_tu_raw", "run", "tep", "nguon", "tung_graph", "luu_y"}
rows = []


def diff(a, b, path):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in SKIP:
                diff(a.get(k), b.get(k), path + "/" + k.replace("~", "~0").replace("/", "~1"))
    elif a != b:
        rows.append({"pointer": path, "run007": a, "run008": b})


diff(old["he_thong"], new["he_thong"], "/he_thong")
diff(old["lan_theo"], new["lan_theo"], "/lan_theo")
diff(old["nguon_trace_T035"], new["nguon_trace_T035"], "/nguon_trace_T035")
NEW_KEYS = ("/lan_theo/TT_static_only_every_full_graph", "/lan_theo/OB_static_only_every_full_graph/endpoint_matrix",
            "/lan_theo/OB_static_only_every_full_graph/classification_note")
status_like = lambda r: isinstance(r["run008"], str) and "CO_DIEU_KIEN_GOI_SUA_DUNG_PHAN_BIEN_CHUA_NGHIEM_THU" in r["run008"]
other = [r for r in rows if not r["pointer"].startswith(NEW_KEYS) and not status_like(r)]
summary = {
    "rows": len(rows),
    "status_string_changes": sum(status_like(r) for r in rows),
    "new_key_rows": sum(r["pointer"].startswith(NEW_KEYS) for r in rows),
    "other_changes": [r["pointer"] for r in other],
    "all_existing_numbers_unchanged": not other,
}
dv_old, dv_new = R("tong-hop-007", "dau-vao.json"), R("tong-hop-008", "dau-vao.json")
summary["dau_vao_manifest_hashes_equal"] = [(m["id"], m["manifest_sha256"]) for m in dv_old["manifest"]] == \
    [(m["id"], m["manifest_sha256"]) for m in dv_new["manifest"]]
summary["dau_vao_all_checks_pass_008"] = dv_new["all_checks_pass"]
json.dump({"tom_tat": summary, "khac_biet": rows},
          open(os.path.join(ROOT, "results/T-040/runs/tong-hop-008/so-sanh-007-008.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False))
