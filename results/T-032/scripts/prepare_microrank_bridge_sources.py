"""Verify the complete saved-source read set; never run methods or read raw data."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ALLOWED = {"T-022", "T-024", "T-026", "T-028", "T-029", "T-031"}


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def scoped(path):
    p = Path(path)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError("outside source scope: " + str(path))
    if p.as_posix() == "src/p3/danh_gia.py":
        return p
    if len(p.parts) < 3 or p.parts[0] != "results" or p.parts[1] not in ALLOWED:
        raise ValueError("outside source scope: " + str(path))
    return p


def write(path, obj):
    path = Path(path)
    with path.open("x", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def prepare(root, out):
    root = Path(root).resolve()
    tree = ast.parse((root / "results/T-032/scripts/check_microrank_t028.py").read_text(encoding="utf-8-sig"))
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ("ANCHORS", "LATEST", "PRIOR"):
                constants[node.targets[0].id] = ast.literal_eval(node.value)
    files = {}

    def read(path, expected, authority):
        scoped(path)
        blob = (root / path).read_bytes()
        digest = sha(blob)
        if digest != expected:
            raise ValueError("local source hash mismatch: " + path)
        row = {"path": path, "sha256": digest, "bytes": len(blob), "authority": authority}
        if path in files and files[path]["sha256"] != digest:
            raise ValueError("conflicting authorities: " + path)
        files[path] = row
        return json.loads(blob.decode("utf-8-sig")) if path.endswith(".json") else None

    roots = {path: read(path, expected, "bridge pinned anchor")
             for path, expected in constants["ANCHORS"].items()}
    latest, prior = constants["LATEST"], constants["PRIOR"]
    lm, pm = roots[latest + "/manifest.json"], roots[prior + "/manifest.json"]
    idx = roots["results/T-024/ban-ghi-dua-vao-cham.json"]
    configs = [r for r in idx["records"] if r["method"] == "microrank" and r["variant"] == "full"
               and r["opaque_id"] == "dev-03d4910932" and r["seed"] is None]
    if len(configs) != 1:
        raise ValueError("helper config cardinality")
    cr = configs[0]
    config = read(cr["source_config"], cr["source_config_sha256"], "T024 index /records/*/source_config")
    p3 = "src/p3/danh_gia.py"
    read(p3, config["src_p3"]["tep"][p3], cr["source_config"] + "#/src_p3/tep")
    rank = [r["snapshot"] for r in pm["final_scripts"] if r["snapshot"]["path"].endswith("/ranking_evidence.py")]
    analysis = [r for r in lm["final_scripts"] if r["path"].endswith("/thuc_hien_buoc3_6.py")]
    if len(rank) != 1 or len(analysis) != 1:
        raise ValueError("helper snapshot cardinality")
    read(rank[0]["path"], rank[0]["sha256"], prior + "/manifest.json#/final_scripts/*/snapshot")
    read(analysis[0]["snapshot"], analysis[0]["sha256"], latest + "/manifest.json#/final_scripts/*")
    outputs = {r["path"]: r for r in lm["outputs"]}
    ap, fp = latest + "/ca-sai.json", latest + "/features-no-label-index.json"
    ar = read(ap, outputs[ap]["sha256"], latest + "/manifest.json#/outputs")
    fi = read(fp, outputs[fp]["sha256"], latest + "/manifest.json#/outputs")
    seen = set()
    for row in ar["main_rows"]:
        if row["method"] != "microrank_full":
            continue
        ds, oid = row["dataset"], row["opaque_id"]
        if ds not in ("RE2-TT", "Nezha-OB") or (ds, oid) in seen:
            raise ValueError("MicroRank cohort identity")
        seen.add((ds, oid))
        ref = fi["cases"][ds][oid]
        feature = read(ref["path"], ref["sha256"], fp + "#/cases/" + ds + "/" + oid)
        if (feature["dataset"], feature["opaque_id"]) != (ds, oid):
            raise ValueError("feature identity mismatch")
        records = row["source"]["records"]
        if len(records) != 1 or records[0]["seed"] is not None:
            raise ValueError("source record cardinality")
        rec = records[0]
        read(rec["path"], rec["sha256"], ap + "#/main_rows/*/source/records")
    counts = {ds: sum(k[0] == ds for k in seen) for ds in ("RE2-TT", "Nezha-OB")}
    if counts != {"RE2-TT": 30, "Nezha-OB": 22}:
        raise ValueError("cohort cardinality")
    obj = {"schema": "T032-MicroRank-bridge-source-closure-v1", "status": "LOCAL_SOURCE_HASH_PASS",
           "counts": counts, "files": [files[p] for p in sorted(files)],
           "total_bytes": sum(r["bytes"] for r in files.values()),
           "scope": "Saved source/result/code only; no raw data, test, heldout or SSH keys"}
    write(out, obj)
    print(json.dumps({"status": obj["status"], "n_files": len(files), "counts": counts,
                      "total_bytes": obj["total_bytes"], "inventory_sha256": sha(Path(out).read_bytes())}))


def verify(root, inventory, expected, out):
    root = Path(root).resolve()
    blob = Path(inventory).read_bytes()
    if sha(blob) != expected:
        raise ValueError("inventory transport hash mismatch")
    obj = json.loads(blob.decode("utf-8-sig"))
    checks = []
    for row in obj["files"]:
        path = root / scoped(row["path"])
        if not path.is_file():
            checks.append({**row, "status": "MISSING"})
            continue
        b = path.read_bytes()
        digest = sha(b)
        checks.append({**row, "actual_sha256": digest, "actual_bytes": len(b),
                       "status": "PASS" if digest == row["sha256"] and len(b) == row["bytes"] else "FAIL"})
    result = {"schema": obj["schema"], "inventory_sha256": expected,
              "status": "PASS" if all(r["status"] == "PASS" for r in checks) else "INCOMPLETE",
              "n_files": len(checks), "counts": obj["counts"], "checks": checks}
    write(out, result)
    print(json.dumps({k: result[k] for k in ("status", "n_files", "counts")} | {
        "not_pass": [r for r in checks if r["status"] != "PASS"]}))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="mode", required=True)
    a = sp.add_parser("prepare")
    a.add_argument("root"); a.add_argument("out")
    a = sp.add_parser("verify")
    a.add_argument("root"); a.add_argument("inventory"); a.add_argument("expected"); a.add_argument("out")
    args = p.parse_args()
    if args.mode == "prepare":
        prepare(args.root, args.out)
    else:
        verify(args.root, args.inventory, args.expected, args.out)
