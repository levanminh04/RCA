"""Read-only source screening after approved-plan byte/blob/SHA verification.

Writes only the delegated coverage directory. Never imports or executes application code.
"""
from pathlib import Path, PurePosixPath
import collections
import datetime
import hashlib
import io
import json
import re
import struct
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PLAN = ROOT / 'results/T-038/runs/metadata-de-xuat-001/de-xuat-tai.json'
SOURCE = ROOT / 'results/T-038/sources/train-ticket-v1.0.0'
PROGRESS = ROOT / 'results/T-038/runs/tai-nguon-001/progress.jsonl'

def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

plan_bytes = PLAN.read_bytes()
assert hashlib.sha256(plan_bytes).hexdigest() == '30028aa7dcb577c007072e6f18dccb3c64902d967fc2445c91885f1156ca7429'
plan = json.loads(plan_bytes)
completed = {}
for line in PROGRESS.read_text(encoding='utf-8').splitlines():
    try: row=json.loads(line)
    except json.JSONDecodeError: continue
    if row.get('ok'): completed[row['git_blob']]=row
manifest_path = ROOT / 'results/T-038/runs/tai-nguon-001/manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else None
manifest_files = {r['source_path']:r for r in manifest['files']} if manifest else {}

def group(path):
    if '/node_modules/' in path: return 'vendored-node-dependencies'
    if path.startswith('old-docs/'): return 'historical-documentation'
    if path.startswith('image/'): return 'root-images'
    if path.startswith('deployment/'): return 'deployment'
    if path.startswith(('hack/','jenkins-ci/','script/')) or '/' not in path: return 'root-build-and-project'
    if '/src/test/' in path or re.search(r'(^|/)(test|tests)(/|\.)',path): return 'application-tests'
    if path.endswith('.java'): return 'application-java'
    if path.startswith('ts-ui-dashboard/'): return 'ui-dashboard'
    if path.startswith(('ts-avatar-service/','ts-news-service/','ts-voucher-service/','ts-ticket-office-service/')): return 'application-nonjava'
    return 'application-resources-and-build'

patterns = {
 'http_endpoint': re.compile(r'https?://[^\s\"\'<>`]+',re.I),
 'runtime_binding': re.compile(r'\b(mongo|mysql|redis|rabbit|amqp|jdbc|nacos|eureka|kafka|SMTP|mail\.host|zipkin|jaeger|tracing|prometheus|elastic|fluent|kibana|opentracing|opentelemetry|skywalking|sleuth|OTEL|JAEGER|ZIPKIN)\b',re.I),
 'build_external': re.compile(r'\b(FROM|image:|repository:|submodule|git clone|wget|curl|dependency|dependencies|require\(|import |\.jar|\.proto|generated|generator)\b',re.I),
 'gateway_or_network': re.compile(r'\b(proxy_pass|upstream|routes:|uri:|listen|server_name|host:|hostname:|port:|ports:|targetPort:|containerPort:|type: LoadBalancer|NodePort|Ingress|ServiceMonitor)\b',re.I),
 'messaging': re.compile(r'\b(RabbitTemplate|RabbitListener|Queue|TopicExchange|DirectExchange|FanoutExchange|BindingBuilder|convertAndSend|sendAndReceive|acknowledge|rabbitmq|amqp|routingKey|routing_key|queue_name)\b',re.I),
}
files=[]; hits=[]; archive_records=[]; external=[]; verified=0
for spec in plan['proposed_files']:
    path=spec['path']; row={**{k:spec[k] for k in ['path','bytes','git_blob','mode']},'locator':f"https://github.com/FudanSELab/train-ticket/blob/{plan['commit']}/{path}",'group':group(path),'status':'not-retrieved','read_depth':'none','reason':'Chưa có xác nhận tải xong blob trong progress tại thời điểm kiểm.','inventory_impact':'Chưa thể loại quan hệ/thực thể do nội dung tệp này cung cấp.'}
    files.append(row)
    if spec['git_blob'] not in completed or not (SOURCE/path).is_file():continue
    # The first source-body operation is an integrity check; content is not decoded until it passes.
    data=(SOURCE/path).read_bytes(); sha=hashlib.sha256(data).hexdigest(); blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();acq=completed[spec['git_blob']]
    ok=len(data)==spec['bytes'] and blob==spec['git_blob'] and sha==acq['sha256']
    if manifest:
        mr=manifest_files.get(path);ok=ok and mr is not None and all(mr[k]==val for k,val in [('bytes',len(data)),('git_blob',blob),('sha256',sha)])
    row['integrity']={'pass':ok,'bytes':len(data),'sha256':sha,'git_blob':blob,'progress_sha256':acq['sha256'],'download_manifest_checked':bool(manifest)}
    if not ok:
        row.update(status='open',reason='Byte/blob/SHA không khớp; không đọc nội dung.',inventory_impact='Chặn dùng tệp và kết luận phụ thuộc.');continue
    verified+=1
    forbidden_sample = path.startswith(('old-docs/Json2Shiviz/bin/ts-large-output/','old-docs/Json2Shiviz/bin/ts-large-sample/','old-docs/Json2Shiviz/example/'))
    if forbidden_sample or path=='old-docs/debugging.xlsx':
        row.update(status='excluded',read_depth='integrity-only-clean-rerun',reason='Mẫu telemetry/đầu ra nghiên cứu lịch sử, không là nguồn runtime v1.0.0; lượt sạch không decode hoặc dùng nội dung.',inventory_impact='Không dùng mẫu telemetry hoặc kết quả nghiên cứu làm nguồn inventory/quan hệ. Đã có sự cố đọc ở lượt đầu, ghi rõ incident.json.',incident_prior_read=not path.endswith('.jpg'))
        continue
    if spec['mode']=='120000':
        target=data.decode('utf-8'); row.update(status='read',read_depth='symlink-literal',symlink_target=target,reason='Đã đọc nội dung Git symlink dạng literal; không tạo hoặc chạy symlink.',inventory_impact='Liên kết công cụ npm trong vendor; cần đích được kiểm riêng khi dùng.')
        continue
    if data.startswith(b'PK\x03\x04'):
        record={'source_path':path,'members':[],'text_members':[]}
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for zi in z.infolist():
                    record['members'].append({'path':zi.filename,'bytes':zi.file_size,'compressed_bytes':zi.compress_size})
                    # Office XML text is decoded in memory; never expand embedded app archive/class files.
                    if path.endswith(('.docx','.pptx','.xlsx')) and zi.filename.endswith('.xml') and zi.file_size<5000000:
                        try:
                            xml=z.read(zi); tree=ET.fromstring(xml); text=' '.join(s.strip() for s in tree.itertext() if s.strip())
                            if text: record['text_members'].append({'path':zi.filename,'text':text})
                        except Exception as exc:record.setdefault('errors',[]).append(repr(exc))
            row.update(status='read' if path.endswith(('.docx','.pptx','.xlsx')) else 'open',read_depth='archive-members-and-office-xml' if path.endswith(('.docx','.pptx','.xlsx')) else 'archive-member-structure',archive_member_count=len(record['members']),reason='Đã liệt kê archive trong bộ nhớ; đọc XML Office khi có. Không giải nén hoặc chạy mã.',inventory_impact='Mã/nhúng trong archive chưa được khảo sát ngữ nghĩa; không dùng để khẳng định đầy đủ runtime.' if not path.endswith(('.docx','.pptx','.xlsx')) else 'Văn bản Office được lưu; sơ đồ/ảnh/nhúng cần kiểm riêng.')
            archive_records.append(record)
        except Exception as exc:row.update(status='open',read_depth='archive-open-failed',reason=repr(exc))
        continue
    try:
        text=data.decode('utf-8-sig')
        if '\0' in text:raise ValueError('NUL binary')
    except (UnicodeDecodeError,ValueError):
        kind='binary'; meta={}
        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            kind='png';meta={'width':int.from_bytes(data[16:20],'big'),'height':int.from_bytes(data[20:24],'big')}
        elif data.startswith(b'%PDF'):kind='pdf'
        elif data[:2]==b'\xff\xd8':kind='jpeg'
        elif data[:4] in [b'wOFF',b'wOF2',b'OTTO',b'\x00\x01\x00\x00']:kind='font'
        row.update(status='open',read_depth='verified-binary-signature',binary_kind=kind,binary_metadata=meta,reason='Đã kiểm signature/kích thước; chưa đọc nghĩa trực quan hoặc cấu trúc binary đầy đủ.',inventory_impact='Không tự loại binary theo đuôi; hình/tài liệu có thể bổ sung kiến trúc. Font/asset giao diện chưa phải bằng chứng quan hệ backend.')
        continue
    lines=text.splitlines();row.update(status='read',read_depth='decoded-full-content-and-pattern-index',line_count=len(lines),reason='Đã đọc toàn nội dung UTF-8 và lập chỉ mục từ khóa; mức phân xử thủ công được ghi ở facts.',inventory_impact='Tệp đã có nội dung để lần nguồn; chỉ mục tự động không thay kiểm nghĩa hoặc chứng minh không còn quan hệ.')
    row['categories_found']=[]
    for line_no,line in enumerate(lines,1):
        categories=[key for key,pattern in patterns.items() if pattern.search(line)]
        if categories:
            row['categories_found']=sorted(set(row['categories_found']+categories))
            # Java semantic inventory is delegated to root/Java branch; keep a full-source screening index separately.
            hits.append({'source_path':path,'line':line_no,'categories':categories,'text':line[:4000],'line_truncated':len(line)>4000,'group':row['group']})
    if row['group']=='vendored-node-dependencies':
        row['inventory_impact']='Vendor đã đọc/index, không tự gán endpoint ứng dụng từ URL ví dụ hoặc test; theo require/import từ entrypoint ứng dụng.'

directories=[{'path':r['directory'],'type':'tree','status':'read','read_depth':'verified-git-tree-metadata','reason':'Cây được duyệt đã kiểm Git tree; phân hoạch blob theo nội dung.','inventory_impact':'Không suy toàn bộ blob đã đọc từ việc có thư mục.'} for r in plan['tree_object_checks'] if r['directory']]
coverage={'task':'T-038','purpose':'Hỗ trợ cơ học người làm; không là phản biện','commit':plan['commit'],'tree':plan['tree'],'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_sha256':hashlib.sha256(plan_bytes).hexdigest(),'download_manifest_present':bool(manifest),'full_tree_expected':3921,'tree_count':len(directories),'blob_count':len(files),'verified_blob_count':verified,'statuses':dict(collections.Counter(r['status'] for r in files)),'read_depths':dict(collections.Counter(r['read_depth'] for r in files)),'groups':{g:dict(collections.Counter(r['status'] for r in files if r['group']==g)) for g in sorted({r['group'] for r in files})},'status_definition':{'read':'Nội dung đã được đọc ở read_depth ghi riêng; không đồng nghĩa nghĩa runtime đã phân xử.','excluded':'Chỉ dùng sau có bằng chứng loại trừ cụ thể; hiện không tự loại theo đuôi.','not-retrieved':'Chưa có xác nhận tải hoàn tất blob tại lượt kiểm.','open':'Đã xác minh blob nhưng nghĩa/cấu trúc cần thêm kiểm, hoặc integrity lỗi.'},'directories':directories,'files':files}
dump('coverage-clean.json',coverage);dump('content-index-clean.json',{'commit':plan['commit'],'notes':'Index sạch không decode mẫu telemetry/đầu ra nghiên cứu lịch sử. Có thể chứa URL ví dụ/vendor; không tự coi là quan hệ hoặc nguồn bắt buộc. Lượt lỗi trước giữ riêng và không dùng.','hits':hits});dump('archive-structures-clean.json',archive_records)
print(json.dumps({k:coverage[k] for k in ['tree_count','blob_count','verified_blob_count','statuses','read_depths','groups']},ensure_ascii=False,indent=2))
