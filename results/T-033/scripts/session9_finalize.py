"""Laptop byte-copy packaging and metadata verification, no research calculation."""
import pathlib,json,hashlib,shutil,datetime
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-033/runs/session9-report-001'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
 assert not p.exists(),p
 p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
base=ROOT/'results/T-033/runs/session9-final-receive-001';inv=read(base/'artifact-inventory.json')['files']
for r,m in inv.items():
 p=base/'artifacts'/r;assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],r
 q=OUT/pathlib.Path(r).relative_to('runs/session9-final-001');assert not q.exists(),q;q.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(p,q);assert sha(q)==m['sha256']
write(OUT/'local-errors.json',{'research_reruns':False,'EC2_not_invoked_by_failed_local_commands':True,'events':[{'step':'publish_prepare first attempt','error':'Historical trang-thai.txt snapshots used same remote alias with different expected bytes/hash','resolution':'Every local source hash actually PASS; historical non-run snapshots retained under inventory namespace; no old-source edit or scientific pin substitution'},{'step':'publication dispatch attempted after missing input','error':'Local FileNotFoundError before SSH invocation','resolution':'Prepared input after namespace fix, then executed once; no failed EC2 command to charge'}]})
write(OUT/'output-index.json',{'status':'AUTHOR_OUTPUT_READY_FOR_REVIEW','author':'Codex','official_reviewer':'Claude; not opened or messaged','canonical_new_output_directory':str(OUT.relative_to(ROOT)).replace('\\','/'),'old_root_bao_phu_nhom':'results/T-033/bao-phu-nhom.json retained as immutable frozen list; final annotated coverage is this directory/bao-phu-nhom.json','numeric_origin':'results/T-033/runs/session9-final-receive-001/artifact-inventory.json','all_source_arrays':'source-catalog.json maps remote pointer to verified original local file','no_detector_rerun':True,'research_decisions_added':False,'RQ2_G2_closed':False})
for sub,description in [('nsigma-trung-gian','Full values/count/mean/std/threshold/margin/flags and fixed arrays in point gzip and original NPZ, selected by index.json and source-catalog.json; same-column controls saved here.'),('bocpd-trung-gian','Full raw/X/columns/theta/predictive density/normalizer/R/m/CP in point gzip and original NPZ, selected by index.json and source-catalog.json; observer theta absence is explicit.')]:
 (OUT/sub/'README.md').write_text(description+'\n',encoding='utf-8')
(OUT/'README.md').write_text('''# T-033 — Bộ đầu ra người làm

Đọc nguyen-nhan-phat-hien.md, doc-tay.md và kiem-tiep.md. Các JSON và hai thư mục trung gian cạnh đây là bộ đầu ra mới theo SPEC. Không ghi đè root bao-phu-nhom.json cũ hoặc run nguồn.

Manifest.json giữ nguyên manifest EC2 của các file số/chuỗi. Package-manifest.json khóa cả tài liệu và các file số đã chép byte, không tự gồm chính nó. Source-catalog.json nối đường dẫn nguồn EC2 tới bản gốc laptop đã kiểm hash. Additional-source-verification.json pin nguồn định nghĩa/code chấm/tài liệu đã đọc thêm.

Chỉ hoàn thành phần người làm trong phạm vi SPEC; chờ Claude phản biện và Minh nghiệm thu. Cơ chế tính toán có điều kiện đã phân xử; nguyên nhân vật lý, onset, prior riêng, coverage và lựa chọn/benefit graph còn OPEN. Không thêm quyết định nghiên cứu hoặc mở test.
''',encoding='utf-8')
required=['nguyen-nhan-phat-hien.md','chuoi-bang-chung.json','bao-phu-nhom.json','phan-ra-tien-xu-ly.json','do-tre-sau-moc.json','nsigma-nguong-co-dinh.json','nsigma-trung-gian/index.json','bocpd-trung-gian/index.json','doi-chieu.json','tai-log.json','doc-tay.md','kiem-tiep.md']
assert all((OUT/r).is_file() for r in required)
for p in OUT.rglob('*.json'):read(p)
files={str(p.relative_to(OUT)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in OUT.rglob('*') if p.is_file()}
write(OUT/'package-manifest.json',{'status':'PASS','required_SPEC_outputs':required,'files':files,'at':datetime.datetime.now().astimezone().isoformat()})
print('PASS immutable byte copies, JSON parsing, required SPEC outputs and package manifest')
