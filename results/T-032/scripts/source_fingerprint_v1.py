"""T-032 mục 4 (Q-120): đối chiếu tên span quan sát được trong dữ liệu dev với mã nguồn công khai, theo từng phiên bản.

Chạy trên EC2, chỉ đọc: `runs/call-interval-001/inventory.json` (kiểm kê tên span của 48 ca dev có bảng span) và ba kho mã nguồn
ở `sources/instrumentation-002/`. Không chạy mã nào trong ba kho; chỉ `git show`, `git ls-tree`, `git grep` trên từng tag/commit.

RE2-TT (Train Ticket): với mỗi tag và HEAD:
  - route: mỗi tên span dạng "METHOD /đường/dẫn/{biến}" có được sinh bởi một controller ở tag đó không
    (ghép @RequestMapping mức lớp với mapping mức phương thức; so cả tên biến đường dẫn và phương thức HTTP);
  - repository: mỗi tên span dạng "XRepository.method" có file XRepository.java ở đúng thư mục dịch vụ không, và phương thức đó
    được khai trong file hay là phương thức chung của Spring Data (findById, findAll, save, ...);
  - thư mục dịch vụ: mỗi serviceName quan sát được có thư mục cùng tên ở tag đó không.
Nezha-OB: mỗi tên span có xuất hiện nguyên văn trong thư mục `src/<dịch vụ>` của Augmented-OnlineBoutique (commit duy nhất) không;
  nếu không thì phần "Service/Method" có là một rpc trong `pb/demo.proto` không. Cùng phép kiểm chuỗi nguyên văn trên kho gốc
  microservices-demo ở tag gần nhất trước ngày thu dữ liệu (22/08/2022) để biết tên nào chỉ có ở bản augmented.
Đây là phép kiểm "mã nguồn ở phiên bản X có sinh được tập tên span quan sát hay không". Khớp đủ là điều kiện cần để coi X là
phiên bản đã triển khai, không phải điều kiện đủ: hai phiên bản có cùng tập route sẽ không phân biệt được bằng phép này.
Dùng: python3 source_fingerprint_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
SRC = BASE / "sources/instrumentation-002"
INVENTORY = BASE / "runs/call-interval-001/inventory.json"
TT, AOB, MSD = SRC / "train-ticket", SRC / "Augmented-OnlineBoutique", SRC / "microservices-demo"
GENERIC_REPO = {"findById", "findAll", "save", "saveAll", "deleteById", "delete", "deleteAll", "count", "existsById", "findOne", "insert"}
MAPPING = re.compile(r'@(Request|Get|Post|Put|Delete|Patch)Mapping\s*(\(([^)]*)\))?', re.S)
HTTP_OF = {"Get": "GET", "Post": "POST", "Put": "PUT", "Delete": "DELETE", "Patch": "PATCH"}


def git(repo, *args):
    done = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True, errors="replace")
    return done.stdout


def paths_in(args_text):
    """Các chuỗi đường dẫn trong đối số của một annotation mapping (value=..., path=..., hoặc chuỗi trần)."""
    if args_text is None:
        return [""]
    found = re.findall(r'(?:value|path)\s*=\s*\{?\s*((?:"[^"]*"\s*,?\s*)+)\}?', args_text)
    strings = []
    for group in found:
        strings.extend(re.findall(r'"([^"]*)"', group))
    if not found:
        bare = re.match(r'\s*\{?\s*((?:"[^"]*"\s*,?\s*)+)', args_text)
        if bare:
            strings.extend(re.findall(r'"([^"]*)"', bare.group(1)))
    return strings or [""]


def methods_in(kind, args_text):
    if kind != "Request":
        return [HTTP_OF[kind]]
    found = re.findall(r'RequestMethod\.([A-Z]+)', args_text or "")
    return found or ["*"]


def join(prefix, suffix):
    path = "/" + "/".join(p for p in (prefix.strip("/"), suffix.strip("/")) if p)
    return path


def routes_of_file(text):
    """Trả tập (METHOD, path) do một file controller sinh ra."""
    class_at = re.search(r'\b(public\s+)?(abstract\s+)?class\s+\w+', text)
    if not class_at:
        return set()
    head, body = text[:class_at.start()], text[class_at.start():]
    prefixes = [""]
    for m in MAPPING.finditer(head):
        prefixes = paths_in(m.group(3))
    out = set()
    for m in MAPPING.finditer(body):
        for prefix in prefixes:
            for suffix in paths_in(m.group(3)):
                for method in methods_in(m.group(1), m.group(3)):
                    out.add((method, join(prefix, suffix)))
    return out


def train_ticket(inventory):
    names = inventory["RE2-TT"]["service_span_names"]
    routes, repos = set(), set()
    for row in names:
        m = re.fullmatch(r'(GET|POST|PUT|DELETE|PATCH) (/.*)', row["name"])
        if m:
            routes.add((row["service"], m.group(1), m.group(2)))
        m = re.fullmatch(r'(\w+Repository)\.(\w+)', row["name"])
        if m:
            repos.add((row["service"], m.group(1), m.group(2)))
    services = sorted({row["service"] for row in names})
    tags = [t for t in git(TT, "tag", "--sort=creatordate").split() if t] + ["HEAD"]
    out = {"observed": {"routes": len(routes), "repository_spans": len(repos), "services": len(services)}, "tags": {}}
    for tag in tags:
        commit = git(TT, "rev-parse", tag + "^{commit}").strip()
        date = git(TT, "log", "-1", "--format=%cs", commit).strip()
        files = git(TT, "ls-tree", "-r", "--name-only", commit).split("\n")
        top_dirs = {f.split("/")[0] for f in files if "/" in f}
        controllers = [f for f in files if f.endswith(".java") and "/src/main/" in f and "ontroller" in f.rsplit("/", 1)[-1]]
        by_service = {}
        for f in controllers:
            by_service.setdefault(f.split("/")[0], set()).update(routes_of_file(git(TT, "show", commit + ":" + f)))
        route_rows = []
        for service, method, path in sorted(routes):
            produced = by_service.get(service, set())
            hit = (method, path) in produced or ("*", path) in produced
            elsewhere = sorted(s for s, r in by_service.items() if s != service and ((method, path) in r or ("*", path) in r))
            route_rows.append({"service": service, "method": method, "path": path, "found_in_service": hit, "found_in_other_service": elsewhere})
        repo_rows = []
        for service, repo, method in sorted(repos):
            candidates = [f for f in files if f.startswith(service + "/") and f.endswith("/" + repo + ".java")]
            declared = any(re.search(r'\b' + re.escape(method) + r'\s*\(', git(TT, "show", commit + ":" + f)) for f in candidates)
            repo_rows.append({"service": service, "repository": repo, "method": method, "file_exists": bool(candidates), "declared": declared,
                              "generic_spring_data_method": method in GENERIC_REPO,
                              "ok": bool(candidates) and (declared or method in GENERIC_REPO)})
        out["tags"][tag] = {
            "commit": commit, "date": date, "controller_files": len(controllers),
            "routes_found": sum(r["found_in_service"] for r in route_rows), "routes_missing": [r for r in route_rows if not r["found_in_service"]],
            "repository_ok": sum(r["ok"] for r in repo_rows), "repository_missing": [r for r in repo_rows if not r["ok"]],
            "services_with_directory": sum(s in top_dirs for s in services), "services_without_directory": [s for s in services if s not in top_dirs],
            "has_mongo_dependency_files": sum(1 for f in files if f.endswith("pom.xml") and "mongodb" in git(TT, "show", commit + ":" + f)),
            "pom_files": sum(1 for f in files if f.endswith("pom.xml"))}
    return out


def online_boutique(inventory):
    names = inventory["Nezha-OB"]["service_span_names"]
    commit = git(AOB, "rev-parse", "HEAD").strip()
    proto = git(AOB, "show", commit + ":pb/demo.proto")
    rpcs = set()
    for service, body in re.findall(r'service\s+(\w+)\s*\{(.*?)\n\}', proto, re.S):
        for rpc in re.findall(r'rpc\s+(\w+)\s*\(', body):
            rpcs.add(service + "/" + rpc)
    tags = [line.split() for line in git(MSD, "tag", "--sort=creatordate", "--format=%(refname:short) %(creatordate:short)").split("\n") if line.strip()]
    before = [t for t, d in tags if d <= "2022-08-22"]
    upstream_tag = before[-1] if before else None
    upstream_commit = git(MSD, "rev-parse", upstream_tag + "^{commit}").strip() if upstream_tag else None
    rows = []
    for row in sorted(names, key=lambda r: (r["service"], r["name"])):
        service, name = row["service"], row["name"]
        literal = bool(git(AOB, "grep", "-l", "-F", "--", '"' + name + '"', commit, "--", "src/" + service).strip())
        literal_any = bool(git(AOB, "grep", "-l", "-F", "--", '"' + name + '"', commit, "--", "src").strip())
        core = re.sub(r'^(grpc\.|/)', "", name)
        rpc = core.replace("hipstershop.", "") in rpcs
        upstream = bool(git(MSD, "grep", "-l", "-F", "--", '"' + name + '"', upstream_commit, "--", "src").strip()) if upstream_commit else None
        cls = ("chuỗi nguyên văn trong mã của đúng dịch vụ" if literal else "rpc trong demo.proto (span do thư viện gRPC tạo)" if rpc
               else "chuỗi nguyên văn ở dịch vụ khác" if literal_any else "không tìm thấy bằng hai phép này")
        rows.append({"service": service, "name": name, "count": row["count"], "class": cls, "literal_in_service": literal, "rpc_in_proto": rpc,
                     "literal_in_upstream_at_tag": upstream})
    classes = {}
    for r in rows:
        classes[r["class"]] = classes.get(r["class"], 0) + 1
    return {"commit": commit, "commit_date": git(AOB, "log", "-1", "--format=%cs", commit).strip(), "n_commits": int(git(AOB, "rev-list", "--count", "HEAD").strip()),
            "upstream_tag_before_collection": upstream_tag, "upstream_commit": upstream_commit, "rpcs_in_proto": len(rpcs),
            "span_names": len(rows), "by_class": classes,
            "literal_in_service_but_not_in_upstream": sum(r["literal_in_service"] and r["literal_in_upstream_at_tag"] is False for r in rows),
            "rows": rows}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    result = {"schema": "T032-source-fingerprint-v1", "inventory_sha256": hashlib.sha256(INVENTORY.read_bytes()).hexdigest(),
              "this_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "train_ticket": train_ticket(inventory), "online_boutique": online_boutique(inventory)}
    (out / "fingerprint.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tt = result["train_ticket"]
    print("observed", tt["observed"])
    for tag, v in tt["tags"].items():
        print(tag, v["date"], v["commit"][:8], "routes", v["routes_found"], "repo", v["repository_ok"], "service dirs", v["services_with_directory"],
              "controllers", v["controller_files"], "pom with mongodb", v["has_mongo_dependency_files"], "/", v["pom_files"])
    ob = result["online_boutique"]
    print({k: ob[k] for k in ob if k != "rows"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
