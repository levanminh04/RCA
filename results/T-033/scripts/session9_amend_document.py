"""Laptop documentary wording amendment only; preserve previous output run."""
import pathlib,json,hashlib,shutil
ROOT=pathlib.Path(__file__).resolve().parents[3];OLD=ROOT/'results/T-033/runs/session9-report-001';OUT=ROOT/'results/T-033/runs/session9-report-002'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
for r,m in read(OLD/'package-manifest.json')['files'].items():assert (OLD/r).stat().st_size==m['bytes'] and sha(OLD/r)==m['sha256'],r
assert not OUT.exists();shutil.copytree(OLD,OUT)
(OUT/'manifest.json').rename(OUT/'manifest-ec2-origin.json')
(OUT/'package-manifest.json').rename(OUT/'package-manifest-author-001.json')
g=read(OUT/'bao-phu-nhom.json')
for r in g['groups']:
 for k,v in r['interpretation'].items():
  if isinstance(v,str):r['interpretation'][k]=v.replace('window shift/std crossing','window median shift/MAD ratio crossing')
write(OUT/'bao-phu-nhom.json',g)
doc=(OUT/'doc-tay.md').read_text(encoding='utf-8');doc=doc.replace('window shift/std crossing','window median shift/MAD ratio crossing')
doc=doc.replace('`nguyen-nhan-phat-hien.md` trình giải thích cạnh tranh và chuỗi chi tiết.','`nguyen-nhan-phat-hien.md` trình giải thích cạnh tranh và chuỗi chi tiết. `doc-tay-root-notes.md` nối các cặp workload/duration, fixed history và cờ mô tả với native.')
(OUT/'doc-tay.md').write_text(doc,encoding='utf-8')
main=(OUT/'nguyen-nhan-phat-hien.md').read_text(encoding='utf-8').replace('`source-catalog.json` ánh xạ','`doc-tay-root-notes.md` bổ sung các cặp context/fixed đã đọc. `source-catalog.json` ánh xạ')
(OUT/'nguyen-nhan-phat-hien.md').write_text(main,encoding='utf-8')
idx=read(OUT/'output-index.json');idx['canonical_new_output_directory']=str(OUT.relative_to(ROOT)).replace('\\','/');idx['documentary_amendment']='B4 annotation uses median-window shift divided by MAD, not std; numeric values/source/run preserved';write(OUT/'output-index.json',idx)
(OUT/'README.md').write_text('''# T-033 — Bộ đầu ra cuối của người làm

Đọc nguyen-nhan-phat-hien.md, doc-tay.md, doc-tay-root-notes.md và kiem-tiep.md. Đây là thư mục đầu ra hiện hành theo SPEC; JSON/thư mục trung gian cạnh đây nối đủ nguồn đã nhận.

Bản001 giữ nguyên. Bản002 sửa chữ std thành MAD trong annotation B4 và nối ghi chú đọc context/fixed; không đổi số, điểm khóa, detector hoặc nguồn. Package-manifest.json là manifest hiện hành cho toàn bộ gói. Manifest-ec2-origin.json và package-manifest-author-001.json là lịch sử của kho nhận/bản001, kiểm ở đường nguồn gốc tương ứng, không so như manifest hiện hành của bản002. Nguồn EC2 đối chiếu theo ../session9-final-receive-001/artifact-inventory.json. Hash/bytes/source catalog đầy đủ trong manifest và self-check.

Chờ Claude phản biện và Minh nghiệm thu; chưa đóng RQ2/G2 hay chọn thiết kế P6. Mọi quyết định khoa học còn theo nguồn được duyệt. Root bao-phu-nhom.json cũ giữ nguyên bản khóa; dùng bao-phu-nhom.json tại đây cho bản annotated cuối.
''',encoding='utf-8')
write(OUT/'documentary-amendment.json',{'status':'TEXT_ONLY_AMENDMENT','prior_run':str(OLD.relative_to(ROOT)).replace('\\','/'),'reason':'Self-check: B4 denominator is 1.4826*MAD, not std','changed_documentary_files':['bao-phu-nhom.json interpretation strings','doc-tay.md wording/link','nguyen-nhan-phat-hien.md link','output-index.json current directory','README.md current manifest mapping'],'numeric_arrays_or_values_changed':False,'source_inputs_changed':False})
for p in OUT.rglob('*.json'):read(p)
files={str(p.relative_to(OUT)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.rglob('*') if p.is_file()}
write(OUT/'package-manifest.json',{'status':'PASS','files':files,'origin':'session9-report-001 preserved; documentary corrections only'})
print('PASS documentary amendment; prior run preserved')
