"""Phân hoạch toàn cây và lưu evidence scan; không biến scan thành semantic proof."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
OB = BASE / 'sources/augmented-ob-94a01ba4'
tree = json.loads((BASE / 'sources/metadata/ob-tree.json').read_text())
proposal = json.loads((BASE / 'de-xuat-tai.json').read_text())
receipts = json.loads((BASE / 'runs/thu-nguon-001/acquisition.json').read_text())
idx = {r['path']: r for r in receipts['files']}
out, refs, missing = [], [], []
for item in tree['tree']:
    row = {k: item[k] for k in ['path', 'type', 'sha']}
    if item['type'] != 'blob':
        row.update(status='tree', reason='whole-tree directory metadata, not content')
        out.append(row)
        continue
    row['bytes'] = item['size']
    rel = item['path']
    if rel.endswith('/log.csv'):
        row.update(status='excluded_unread', reason='raw telemetry forbidden by task/download authorization',
                   impact='Dockerfile COPY depends on this file; build reproducibility and log content not verified; static source declarations still inspected',
                   owner='Minh for separate telemetry permission if needed', needed='no reading proposed in this task')
        out.append(row)
        continue
    p = OB / rel
    receipt = idx[p.relative_to(ROOT).as_posix()]
    b = p.read_bytes()
    assert hashlib.sha256(b).hexdigest() == receipt['sha256'] and len(b) == item['size']
    row.update(path_local=p.relative_to(ROOT).as_posix(), sha256=receipt['sha256'], integrity_verified=True)
    try:
        text = b.decode('utf-8')
    except UnicodeDecodeError:
        if p.suffix == '.jar':
            with zipfile.ZipFile(p) as z:
                row.update(status='read_metadata_binary', reason='ZIP directory and manifest inspected; bytecode not executed/decompiled',
                  zip_entry_count=len(z.infolist()), effect='runtime auto-instrumentation naming/implementation beyond manifest stays OPEN')
        elif rel.startswith('docs/img/'):
            row.update(status='read_visual', reason='three images visually inspected; architecture/screen document, not deployment proof',
                       effect='README image labels do not override SQL/implementation')
        else:
            expected = 'PNG' if b.startswith(b'\x89PNG') else 'JPEG' if b.startswith(b'\xff\xd8') else 'ICO' if b.startswith(b'\x00\x00\x01\x00') else 'unknown'
            row.update(status='excluded_body_after_type_check', reason='asset signature '+expected+' and HTML/CSS paths inspected; no service definition inferred from pixels',
                       effect='served browser asset, not independently addressable RCA backend')
        out.append(row)
        continue
    lines = text.splitlines()
    row['lines'] = len(lines)
    evidence = []
    for i, line in enumerate(lines, 1):
        if re.search(r'(https?://|\brpc\b|\bservice\b|otel|Span|span|grpc|redis|mysql|\bCOPY\b|\bFROM\b|protoc|Register|add_service|add_.*_to_server|tracer\.start|tracer\.Start)', line, re.I):
            evidence.append({'line': i, 'text': line.strip()[:280]})
    if evidence:
        refs.append({'path': rel, 'evidence': evidence})
    if '/static/' in rel:
        externals = re.findall(r'(?:href|src)=["\']([^"\']+)|url\(([^)]+)\)', text)
        scripts = '<script' in text or 'foreignObject' in text
        row.update(status='read_asset_structure', reason='SVG/XML or CSS full text checked for references/scripts; browser path source kept',
                   references=externals, active_script_marker=scripts, effect='no server dependency introduced solely by browser link')
    elif rel.endswith(('demo.pb.go', '_pb2.py', '_pb2_grpc.py')):
        row.update(status='read_generated_interface', reason='service/method descriptor, Invoke/registration and build inputs inspected; serialization boilerplate scanned',
                   effect='binding inventory differs from registration; see specialist coverage and generated mismatch evidence')
    elif p.name in ['package-lock.json', 'go.sum']:
        row.update(status='read_dependency_structure', reason='dependency keys/versions and imports/build consumer inspected; not proof of runtime package contents',
                   effect='external source semantics and image reproducibility OPEN')
    elif p.name in ['gradlew', 'gradlew.bat']:
        row.update(status='read_build_entrypoint', reason='wrapper/JVM invocation and properties inspected; wrapper implementation not run', effect='build tool, not application service')
    elif p.name.endswith('__failpoint_stash__'):
        row.update(status='read_alternate_source', reason='non-.go stash compared with live source; current go build uses .go files',
                   effect='retained history/fault branches; not unioned as simultaneous operation definitions')
    elif rel.startswith(('docs/', 'hack/', 'kubernetes-manifests/', 'pb/')) or rel in ['README.md', 'LICENSE']:
        row.update(status='read_source', reason='source/config/interface/document inspected with relation/coverage implications', effect='deployment candidate only')
    elif '/templates/' in rel:
        row.update(status='read_template', reason='render path/forms/links and handler consumers inspected',
                   effect='browser URLs are separate scope, no frontend-server egress inferred')
    elif '/tests/' in rel or p.name.endswith('_test.go'):
        row.update(status='read_test_source_structure', reason='unit-test source/imports and build boundaries scanned; not public dataset test access',
                   effect='not runtime inventory; production entrypoints/proto verified separately')
    elif p.name.startswith('.') or p.name in ['license_header.txt', 'credits.txt']:
        row.update(status='read_exclusion_rule', reason='ignore/copyright/asset origin contents read; not service source', effect='build inclusion/exclusion explicitly retained')
    else:
        row.update(status='read_application_source', reason='specialist code/config/build review plus full-file reference scan; provenance in fragment/coverage',
                   effect='source declarations/conditions, not assertion runtime executed')
    row['semantic_claim'] = 'see parts/*-coverage.json and relation provenance; a scan is not by itself verification of every runtime implication'
    if text.startswith('version https://git-lfs.github.com/spec/v1'):
        missing.append({'path': rel, 'reason': 'LFS pointer requires separate source authorization'})
    out.append(row)
external = [
 {'id':'images', 'source':'kubernetes-manifests/*.yaml image tags; hack/make-docker-images.sh TAG/REPO_PREFIX',
  'state':'OPEN', 'input':'build commit + image digest + deployment/collection manifest', 'owner':'dataset authors',
  'affects':'cannot assert candidate application revision produced dataset, or attribute differences to instrumentation'},
 {'id':'istio', 'source':'hack/make-release-artifacts.sh:82–85; start*.sh kube-inject',
  'state':'OPEN', 'input':'version and injection/rendered manifest; istio-manifests referenced but absent from tree', 'owner':'deployment authors',
  'affects':'proxy/control-plane concrete inventory and telemetry path; not eliminated by source scan'},
 {'id':'collector', 'source':'COLLECTOR_ADDR/OTLP config in app and YAML', 'state':'OPEN',
  'input':'collector/exporter code/config that emits dataset CSV Node and Source/Target metadata', 'owner':'Nezha authors',
  'affects':'Node host meaning, metadata independence and export lineage'},
 {'id':'instrumentation-libraries', 'source':'go.mod/package.json/requirements*.txt/build.gradle/cartservice.csproj + JAR manifest',
  'state':'OPEN', 'input':'exact library source/binary-to-build identity if runtime aliases need confirmation', 'owner':'source/deployment authors',
  'affects':'auto span names and omitted internal edges must remain unverified; no automatic prefix aliases'},
 {'id':'mysql-initialization', 'source':'hack/init_mysql.sql; mysql hostPath /data/mysql', 'state':'OPEN',
  'input':'database initialization/build/deployment evidence', 'owner':'deployment authors',
  'affects':'source shows logical DBs, not proof the SQL loaded in dataset environment'}]
outobj = {'snapshot_commit':proposal['ob_commit']['sha'],'snapshot_tree':tree['sha'],
 'tree_truncated':tree['truncated'],'entry_count':len(out),'blob_count':sum(r['type']=='blob' for r in out),
 'counts':dict(Counter(r['status'] for r in out)), 'rows':out,'external_source_questions':external,
 'lfs_pointers':missing,'gitlinks':[e for e in tree['tree'] if e['type']=='commit'],
 'completeness':{'tree_partition_complete':len(out)==len(tree['tree']),
   'all_runtime_or_external_sources_complete':False,
   'claim':'complete partition of known snapshot with declared exclusions; not a whole-deployment or telemetry completeness claim'}}
(BASE/'bao-phu-nguon.json').write_text(json.dumps(outobj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(BASE/'runs/trien-khai-001/source-reference-scan.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'tree_entries':len(out),'counts':outobj['counts'],'lfs':len(missing),'external_open':len(external)}))
