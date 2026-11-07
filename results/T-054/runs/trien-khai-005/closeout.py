"""Hoàn thiện hồ sơ ứng viên nhiều máy; không mở telemetry hoặc phát main."""
from pathlib import Path
import sys,json,hashlib,copy,tarfile,shutil,re
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import *

def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
    x=ref(p);x['path']=Path(p).resolve().relative_to(ROOT).as_posix();return x
def save(p,x):Path(p).write_bytes(canonical(x)+b'\n')
def md(p,s):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_bytes(s.encode('utf-8'))
def portable(x):
    if isinstance(x,list):return[portable(v)for v in x]
    if isinstance(x,dict):return{k:portable(v)for k,v in x.items()}
    if isinstance(x,str):
        s=x.replace('\\','/');prefix=ROOT.as_posix()+'/'
        if s.lower().startswith(prefix.lower()):return s[len(prefix):]
    return x

# Snapshot thêm các hồ sơ gốc trước lượt hoàn thiện, không thay snapshot đầu phiên.
history=RUN/'before-closeout'
if not history.exists():
    history.mkdir(exist_ok=False)
    for name in ['authorization.json','environment.json','pilot-plan.json','reuse.json','protocol.json','source-manifest.json','ho-so-g3.md','runbook.md']:
        shutil.copy2(OUT/name,history/name)

# Ghép đúng tên ca/tệp với nguồn HF đã pin, không chỉ tìm hash ở bất kỳ ca nào.
source=load(ROOT/'results/T-002/public-metadata/run-002/source-manifest.json');tree={}
for f in (ROOT/'results/T-002/public-metadata/run-002/sources').glob('hf-tree-page-*.json'):
    entry=next(x for x in source if x['artifact']=='sources/'+f.name)
    assert digest(f)==entry['sha256']
    for x in load(f):tree[x['path']]=x
inventory=load(RUN/'local-TT60-inventory.json');rows=[]
for row in inventory['files']:
    rel=Path(row['path']).relative_to('data/locked/rcaeval-re2tt-60').as_posix();origin=tree[rel]
    assert row['sha256']==origin['lfs']['oid']and row['bytes']==origin['size']
    # Bytes nguồn đã được hash trong inventory, kiểm lại opaque cuối phiên bên dưới validator.
    rows.append(dict(row,source_path=rel))
verification=dict(PASS=True,files=180,bytes=sum(x['bytes']for x in rows),
    source_revision='afeacb11bcc94dadfd1c8f483ee4377b2b8b614e',exact_case_filename_mapping=True,files_verified=rows,no_telemetry_values_opened=True)
if (RUN/'TT60-strict-source-verification.json').exists():assert read_pin(ref(RUN/'TT60-strict-source-verification.json'))==verification
else:atomic(RUN/'TT60-strict-source-verification.json',verification)

p=load(OUT/'protocol.json');c=read_pin(p['dispatch_contract_ref']);placement=load(RUN/'placement-005.json')
helper='results/T-054/runs/trien-khai-005/materialize_main.py';c['code_pins'][helper]=digest(ROOT/helper)
c=portable(c);contract_pin=atomic(RUN/'dispatch-contract-005-freeze-candidate.json',c);contract_pin=pin(contract_pin['path'])
p.update(dispatch_contract_ref=contract_pin,source_code=c['code_pins'],execution_candidate=pin(RUN/'de-xuat-khoa-g3-005.json'),
    runtime='Hai EC2 + laptop theo placement005. Ràng buộc test local đã bỏ. Chưa có G3/test grant; chưa truyền TT test hoặc phát main.',
    runtime_dependencies_note='runtime_dependencies.environments giữ mô tả laptop; môi trường từng máy hiện hành ở environments-005.json và hợp đồng host. Không dùng mô tả Windows làm executable cloud.',
    runtime_environments_ref=pin(RUN/'environments-005.json'),
    real_execution_ready_scope='Chưa được phát main/test; chuẩn bị nhiều máy đã có bằng chứng để trình G3, còn khóa và quyền nguồn/binding.',
    open_choices=['Minh xét/khóa G3 ứng viên nhiều máy đúng byte','Grant nguồn test94/chấm và TORAI A đúng cohort; dựng/attest metadata độc lập sau quyền','RE3 H1/H2/adapter/nguồn riêng, không thuộc grant94'],
    multihost_evidence=dict(p['multihost_evidence'],EC2_1_transport=pin(RUN/'ec2_1-final-checks-r2.json'),EC2_2_transport=pin(RUN/'ec2_2-final-checks-r2.json')))
p=portable(p);p['fingerprint']=fingerprint({k:v for k,v in p.items()if k!='fingerprint'});save(OUT/'protocol.json',p)

transfers={h:[]for h in ['ec2_1','ec2_2']}
matrix=load(OUT/'matrix.json');by_member={x['member_sha256']:x['opaque_id']for x in matrix['main']if x['dataset']=='RE2-TT'}
for row in rows:
    case=Path(row['path']).parent.name;oid=by_member[fingerprint(['RE2-TT',case])];h=placement['TT_case_owner'][oid]
    transfers[h].append(dict(row,opaque_id=oid,destination=c['hosts'][h]['data_root']+'/'+row['path']))
for h,files in transfers.items():
    assert len(files)==90 and sum(x['bytes']for x in files)==placement['TT_transfer_bytes'][h]
atomic(RUN/'transfer-plan-005.json',dict(status='PLAN_ONLY_WAIT_G3_DATA_GRANT',hosts=transfers,
    originals='Giữ nguyên toàn bộ bản gốc laptop và mọi attempt; không rsync --delete.',
    method='Gói allowlist từng host; gửi vào .partial/fresh staging, kiểm byte/SHA từng tệp ở đích, rename chỉ sau khớp đủ; không ghi đè dữ liệu đang dùng.',
    return_method='Mỗi host có tiền tố riêng; nhận vào thư mục mới, giữ receipt/envelope/path gốc và manifest có pin; receive_paths ánh xạ về bản nhận; verify_snapshot từng lô rồi merge_partitions đúng toàn plan trước nhãn.',
    labels_transferred=False,OB_transferred=False,TORAI_A_transferred=False,test_transferred=False,
    output_retention='Giữ cả remote/local đến khi Minh nghiệm thu và cho dọn; thu nhận nén từng ca để giảm đĩa, không xóa raw/attempt trước đối chiếu.',
    disk='EC2_1 còn~9.56GB, EC2_2~14.63GB lúc inventory/cleanup; TT~0.655GB/máy. Output/temp chưa có upper bound; theo dõi và DRAIN trước thiếu chỗ.'))

auth=load(OUT/'authorization.json');auth.update(ssh_grant=True,sync_grant=True,
    pilot_scope='Cloud DEV dev-a915aa2424 trên hai máy và kiểm công cụ giả; giữ tất cả pilot cũ, không baseline diện rộng.',
    pilot_scope_note='pilot_scope hiện hành thay pilot_scope chỉ local trong checkpoint004; các pin pilot cũ giữ lịch sử.',
    pilot_scope_current='USER_CONFIRMED_SSH_DEV_AND_PREPARE_STOP_BEFORE_MAIN',
    cleanup_grant={'path':'/home/ubuntu/rca/envs/py312','completed':True,'evidence':pin(RUN/'approved-cleanup-ec2-1.json'),
      'preserved':'/home/ubuntu/rca/T-025/envs/main; all results/data'},
    source_current={'type':'USER_CONFIRMED','source':pin(ROOT/'docs/DECISIONS.md'),'scope':'duyệt1/3, SSH/kiểm cloud/lập lịch; cleanup đúng py312; không suy ra G3/test'},
    g3=False,test_grant=False,stop_before_main=True)
save(OUT/'authorization.json',auth)
env=load(OUT/'environment.json');env.update(cloud='INSPECTED_BOTH_AND_TARGETED_DEV_VERIFIED',
    status='ACTUAL_THREE_HOST_ENVIRONMENTS_CANDIDATE_NOT_G3',hosts_ref=pin(RUN/'environments-005.json'),
    inventories={h:pin(RUN/(h+'-inventory.json'))for h in ['ec2_1','ec2_2']},
    reuse='T025/main + T025/py38 trên cả hai EC2; không cài lại; py38 không cần pyarrow/drain3 vì chỉ đọc CSV TORAI.',
    limitations='EC2_1 controller không có cost hợp lệ ở lượt dev; không dùng số thời gian/RSS đó. Môi trường/platform hai máy khác nhau, không suy exact parity mọi ca.')
save(OUT/'environment.json',env)
pilot=load(OUT/'pilot-plan.json');pilot.update(status='TARGETED_CLOUD_DEV_COMPLETE_STOP_FOR_G3',ssh_performed=True,
    remaining_before_pilot=[],remaining_before_main=p['open_choices'],execution_plan_ready=False,
    ec2_1={'status':'OUTPUT_EXACT_NATIVE_EC2_2_RECOVERED_NO_VALID_COST','evidence':pin(RUN/'ec2-1-cloud-dev-summary-corrected.json')},
    ec2_2={'status':'EXACT_NATIVE_OUTPUT_VALID_COST','evidence':pin(RUN/'cloud-dev-summary.json')},
    future_pilot='Không có lô pilot mặc định; chỉ bổ sung khi lỗi/phép đối chiếu cụ thể chưa giải quyết.',
    cloud_tool_checks={h:pin(RUN/(h+'-final-checks-r2.json'))for h in ['ec2_1','ec2_2']},
    torai_reuse={h:pin(RUN/(h+'-torai-bridge.json'))for h in ['ec2_1','ec2_2']})
save(OUT/'pilot-plan.json',pilot)
reuse=load(OUT/'reuse.json');reuse.update(status='REUSE_CHECKPOINT004_AND_CLOUD005',no_bulk_rerun=True,
    current={'baseline_G2':'Giữ kết quả G2 đủ điều kiện, dùng làm tham chiếu và kiểm cài đặt. Test94 mới chưa chạy, không thể dùng điểm dev thay điểm test.',
      'DEV':'Giữ40slot cũ +2slot004;005 chỉ2lượt M1 trên1ca DEV kiểm tuyến mỗi máy, không lặp baseline.',
      'environments':'Dùng nguyên T025 env/source; xóa duy nhất py312 cũ được Minh duyệt.',
      'TORAI_B':'Kiểm hash source RCD/IO và Linux import; digest 4CSV+t+seed khớp Windows trên hai máy; không chạy lại học TORAI.',
      'data':'TT60 đã có và khớp nguồn180/180; không tải lại.'})
save(OUT/'reuse.json',reuse)
sm=load(OUT/'source-manifest.json');sm['runtime_compiler']=pin(ROOT/helper);sm['current_multihost_protocol']=pin(OUT/'protocol.json');save(OUT/'source-manifest.json',sm)

# Thay đúng mô tả vận hành cũ trong SPEC, giữ các phần khoa học/tiêu chí xong.
spec=ROOT/'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md';s=spec.read_text(encoding='utf-8')
a=s.index('| Lô | Máy/dữ liệu |');b=s.index('\nMinh muốn tận dụng',a)
s=s[:a]+'''| Lô | Máy/dữ liệu | Phụ thuộc | Worker tối đa | Tiếp nhận |
|---|---|---|---|---|
| Chuẩn bị đã làm | Hai EC2+laptop, code/DEV được cấp | SSH/env/pin | 2 | Inventory, dev nguồn khớp, kiểm resume/nhận/ghép |
| Main EC2_1 | 30 TT; M1-family210, TORAI B90, C-d3 30, C-e tối đa30 | G3/grant; prep→TORAI; M1 seal→C-d3 | 2 khi đủ RAM | 360 vị trí tối đa; TT654.702.162 byte/90tệp |
| Main EC2_2 | 30 TT còn lại; cùng cơ cấu | Như EC2_1; phân vùng không trùng | 2 khi đủ RAM | 360 vị trí tối đa; TT654.685.920 byte/90tệp |
| Main laptop | OB442 vị trí (68 UNSUPPORTED); TT5baseline300; A phụ180 | Nguồn/grant; A cần quyền CSV riêng | 2 khi đủ RAM | 922 vị trí; ưu tiên công cụ nhận/kiểm, không tạo cache liên vế mới |
| Nhận/kiểm/chấm | Laptop, compact từng host đã seal | Pin/receipt đủ; aggregate bằng đúng toàn plan trước nhãn | 1 | Nhận định kỳ vào thư mục mới; A4 thiếu vẫn chặn bảng |
| RE3 | Hợp đồng metadata pha1 đã có; schema/adapter thật còn OPEN | Nguồn/adapter/quyền riêng, bản cuối | Chưa phát | Không thuộc main94 |
''' +s[b:]
s=s.replace('Laptop hỏng: test/chấm phải đợi, không tự chuyển lên cloud.','Laptop hỏng: lô EC2 độc lập tiếp tục theo plan đã khóa; nhận/chấm chờ phục hồi. Không tự đổi chủ lô hoặc phát trùng.')
s=s.replace('Chỉ lập kế hoạch; không in/nạp nội dung khóa','SSH/kiểm DEV đã thực hiện theo quyền mới; không in/nạp nội dung khóa')
s=s.replace('Runner hiện dùng ENVS Windows; Linux wrapper chỉ override đúng env được duyệt','Runner dùng executable/PYTHONPATH theo hợp đồng từng máy; Linux wrapper dùng T025 env đã kiểm')
s=s.replace('- Không chuyển raw/dẫn xuất test lên cloud theo phương án cơ sở, không đọc raw OB trên EC2 trong T-054, không tự xử lý bản sao cũ.','- TT test được đề nghị chia sang hai EC2 theo transfer-plan005 sau G3/grant, không còn ràng buộc local-only. OB và A bố trí laptop theo chi phí/nguồn hiện có; không mở/xóa bản sao OB cũ trên EC2.')
s=s.replace('máy local/pilot/tài nguyên đạt;','môi trường từng máy/pilot/tài nguyên đạt;')
s=s.replace('| Máy/quyền/hạn | Cả hai EC2 + laptop được ưu tiên khi có ích; EC2 2 chỉ có lô cụ thể; OB local/cache local | SSH/chạy/sync/pilot/budget/grant/quyền cloud test/giờ sáng xét riêng. Không tự suy từ ghi hồ sơ |','| Máy/quyền/hạn | SSH/sync/DEV hai EC2 đã được cấp và kiểm; lịch005 dùng cả hai EC2+laptop, không thêm cache liên vế | Dừng trước main; G3/grant test/nguồn A riêng. Không bật/tắt máy hoặc commit |')
a=s.index('Dự toán công pha 1 **chưa kiểm**');b=s.index('\nNgoại lệ Minh xác nhận',a)
s=s[:a]+'''Hiện hành ngày05/11: chuẩn bị nhiều máy hoàn tất để trình G3, không tiếp tục pilot mặc định. Dự toán005 **5–9 giờ** cho tính toán/chuyển/niêm phong/chấm là kịch bản chưa kiểm toàn cohort, không là trần hoặc ETA toàn nghiên cứu. Giả định cloud40–120s mỗi lượt family/C-e (chỉ một ca EC2_2 đo~67s), tối đa2worker/máy khi RAM đủ, dùng thời gian baseline đã có, setup/chuyển0,25–0,5h dự kiến. I/O/solver/ca khác, thiếu RAM hoặc lỗi có thể làm lâu hơn. Đọc ca/diễn giải cơ chế/báo cáo khoa học tính riêng, chưa có dự toán đáng tin. Không dùng25–27h tuần tự cũ làm ETA mới, không hứa mốc08:00.

Lịch: G3/grant→khóa nguồn/plan→sync/hash hai EC2 song song→ba queue chạy đồng thời. Mỗi ca prep trước method; M1 seal trước C-d3. Laptop nhận/kiểm định kỳ; chỉ chấm sau đủ snapshot/binding. Thời gian đường găng là max(queue EC2_1, queue EC2_2, queue laptop) cộng các pha ngoài queue, không cộng ba queue thành giờ trôi. Nguồn: placement-005.json, environments-005.json, transfer-plan-005.json, de-xuat-khoa-g3-005.json. Không mở telemetry test trong005.
''' +s[b:]
md(spec,s)
# Phục hồi kiểu xuống dòng AGENTS như trước để diff chỉ còn nội dung duyệt.
ag=ROOT/'AGENTS.md';old=(RUN/'before/AGENTS.md').read_bytes();raw=ag.read_bytes().replace(b'\r\n',b'\n')
if b'\r\n'in old:raw=raw.replace(b'\n',b'\r\n')
ag.write_bytes(raw)

report='''# T-054 — chuẩn bị hai EC2+laptop, checkpoint005

Đã hoàn tất phần triển khai nhiều máy được Minh duyệt, dừng trước chạy chính. Đây là hồ sơ trình G3, chưa phải G3 đã khóa hoặc task P7 đã xong. Không có quyền mở test/main hoặc RE3 từ lượt SSH/dọn máy này.

## Dữ liệu và dọn máy

TT60 có sẵn:60ca/180parquet, **1.309.388.082byte (1,309GB;1,219GiB)**. Hash/byte đúng từng tên ca+tệp so HF revision đã pin; không đọc giá trị telemetry, không tải lại. Nguồn: runs/trien-khai-005/TT60-strict-source-verification.json#/files_verified.

SSH cả hai máy bằng host key đã ghim, không dựng lại môi trường. Cả hai2vCPU/~8GBRAM. Dùng T025/envs/main và T025/envs/py38 cùng nguồn RCAEval cũ. EC2_1 thiếu chỗ; Minh duyệt xóa đúng /home/ubuntu/rca/envs/py312 (~8,10GB), free từ1,462→9,563GB. Giữ T025/main, dữ liệu và toàn bộ kết quả task cũ. EC2_2 còn~14,63GB. Nguồn: *-inventory.json, approved-cleanup-ec2-1.json (stdout dòng deleted_exact_approved_directory), environments-005.json.

## Phân bổ ứng viên khóa

| Máy | Lô | Vị trí tối đa | Dữ liệu TT chuyển |
|---|---|---:|---:|
| EC2_1 | 30TT: family210+B90+C-d3 30+C-e≤30 |360|654.702.162byte/90tệp|
| EC2_2 | 30TT còn lại, cùng cơ cấu |360|654.685.920byte/90tệp|
| Laptop | OB442 (68UNSUPPORTED), TT5baseline300, A phụ180 |922|Giữ bản gốc|

Tổng1.642 vị trí, tối đa1.574 lượt method thực nếu bỏ68UNSUPPORTED; C-e thiếu lịch sử thay bằng dòng hỗ trợ có nguồn, không tự điền0. Gán ca TT theo byte để cân dữ liệu, không theo lỗi/nhãn/điểm. C-c/C-g/C-d1/2 là dẫn xuất, không thêm baseline. Nguồn: placement-005.json#/counts,/TT_transfer_bytes; matrix.json.

Hai EC2 nhận phần TT nặng vì ưu tiên thời gian theo chỉ đạo Minh. Laptop giữ OB để dùng dữ liệu ngày/phút và adapter đã kiểm, tránh chuyển file chung; giữ CIRCA/A theo môi trường Windows/nguồn tác giả hiện có. Đây là cách phân bổ theo bằng chứng hiện tại, không khẳng định tối ưu toàn cục. TORAI B dùng Linux đã có ở G2: nguồn RCD/IO đúng hash, import đạt; parsed digest4CSV+t+seed của DEV khớp Windows trên cả hai máy. Không chạy lại học TORAI chỉ để đo.

Mỗi máy tối đa2worker, mỗi method×dataset chỉ1lượt cùng lúc;1luồng tính số/method. RAM admission tính cả phần dự phòng: EC2 dự kiến2GiB/lượt×1,25, reserve768MiB; laptop theo peak đã có×1,25,reserve384MiB. Đây là ước lượng tài nguyên, không bảo đảm peak mọi ca. Không đủ RAM thì đợi/dừng phát và báo, không biến unrun thành TIMEOUT. Prep→method, M1 seal→C-d3 tuần tự; lô độc lập trên3máy chạy đồng thời. Không cần đo3/4worker hoặc dựng queue phân tán.

Transfer-plan005 ghi đủ từng tệp/hash/byte/máy/đích. Test chưa chuyển. Gửi allowlist vào vùng mới/partial, kiểm đủ trước dùng; bản gốc giữ laptop. Mỗi host có code/data/output prefix riêng; thu manifest/receipt/envelope nguyên bản, kiểm hash và snapshot trước ghép đúng union toàn plan, rồi mới nhãn. Thiếu/trùng/sai job bị chặn; không cộng hai kết quả của cùng dev thành hai ca độc lập. Không tự xóa remote sau nhận, không chạy lô thứ hai để dự phòng trùng. Output/temp toàn cohort chưa có upper bound; theo dõi free disk và DRAIN trước thiếu chỗ.

## Đã kiểm đúng thay đổi

Giữ40slot DEV cũ và2slot004, baseline G2 và mọi lượt hỏng. Chỉ thêm2lượt M1 trên cùng1ca DEV dev-a915aa2424 để kiểm tuyến mỗi máy. EC2_2: toàn trường khoa học được đối chiếu khớp native EC2_2, wall66,976648s, peakRSS cây1.746.251.776byte, maxgap0,24055s. Nguồn cloud-dev-summary.json. Đây là một mẫu, không chứng minh thời gian/parity mọi cấu hình hoặc mọi ca.

EC2_1: worker hoàn thành nhưng controller chụp danh tính trước exec nên ghi BLOCKED/cost sai. Giữ journal/cost gốc; nhận lại output và kiểm khớp nguồn EC2_2, không rerun method. Không dùng runtime/RSS lượt này cho dự toán. Sửa bắt tay token+argv trước pin PID; chín kiểm công cụ giả trên laptop và cả hai EC2 đạt. Source code cuối9script khớp gói kiểm Linux r2; phần khoa học nền93pin không đổi. Nguồn ec2-1-cloud-dev-summary-corrected.json, retained-failures.json, *-final-checks-r2.json.

60kiểm transport hiện hành đạt; trình biên dịch metadata giả giữ1.642vị trí (1.641job+1insufficient), ba hợp đồng máy/union đạt, thiếu lô/job/C-e bị chặn, protocol chưa khóa bị chặn trước source bundle. Không chạy dataset trong phép kiểm này. Giữ lỗi ghi summary trùng tên/partial; bản tổng kết hợp lệ materializer-final-checks.json khai nguồn phục hồi. Nhận cloud dùng API receive_paths/merge_partitions; runbook chỉ đúng cách ghép trong cùng process.

## Ước lượng và mốc dừng

**5–9giờ là kịch bản cho tính toán+chuyển+seal+chấm, chưa kiểm toàn cohort; không là trần cố định hoặc ETA toàn task.** Giả định cloud40–120s/lượt family/C-e, chỉ1mẫu thật~67s; hai worker khi RAM cho phép; baseline dùng timing có sẵn; setup/chuyển0,25–0,5h dự kiến. Nếu ca nặng/I/O/solver/lỗi/RAM khác, thời gian đổi. Đọc ca, phân tích cơ chế và báo cáo nghiên cứu còn riêng, chưa có số đáng tin. Không cần thêm benchmark mặc định chỉ để làm ETA đẹp hơn.

Không đặt trần cộng dồn P7; timeout từng lượt đề nghị600s/C-d3 60s, poll0,1s/maxgap<5s. Lỗi/không tiến triển/lặp vô tận/hàng chục giờ chưa xong thì dừng báo Minh. Ba sai khác số học cũ được chấp nhận riêng; không dung sai chung. Hai độ nhạy giữ nguyên, không đổi phép chính/mức OB.

## Minh cần xét trước main

1. Xét/khóa G3 đúng freeze007, protocol/host/placement/policy/nguồn được trình. Không tự gắn LOCKED_G3, không commit/push.
2. Grant test94 và chấm, quyền chuyển TT60 sang đúng hai EC2; sau quyền mới dựng/attest runtime/nguồn độc lập/nhãn và C-e support. Metadata compiler đã kiểm bằng dữ liệu giả, chưa có plan test nguồn thật. Nếu lỗi mới thì dừng đúng phần phụ thuộc.
3. TORAI A vẫn phụ ngoài A4; chỉ dev-a5cabe5fa7 đã được cấp. Cần grant3CSV tác giả đúng TTcohort trước biên dịch full plan hiện tại; không tự bỏ A hoặc suy quyền từ B.
4. RE3 giữ ngoài: hợp đồng metadata chuẩn bị đã có, H1/schema và H2/adapter thật còn OPEN/quyền riêng. G3(a) không hoàn thành nghĩa vụ RE3 hoặc tự mở30ca giữ ngoài. Chưa cài/kiểm adapter trên telemetry RE3.

AGENTS đã áp mục1/3 Minh duyệt: nới task/phiên khi checkpoint đủ; bắt buộc xem/tận dụng đầu ra cũ trước chạy thêm. Không áp mục2 chuyển phản biện tự động; prompt Claude vẫn do Minh chọn chuyển. Checkpoint004 trở về trước là lịch sử, không ép các hồ sơ mutable mới khớp manifest cũ. LOG/SPEC/STATE và manifest005 là điểm nhận tiếp; không mở lại task cũ. P7 chưa xong pha2, chưa trả lời RQ3 độc lập hoặc xác nhận cơ chế vật lý.
'''
md(OUT/'reports/tu-soat-005/bao-cao.md',report)
md(OUT/'ho-so-g3.md','# Hồ sơ trình G3 hiện hành — checkpoint005\n\nĐã hoàn tất chuẩn bị nhiều máy để trình Minh, **DỪNG trước main/test**. Chưa LOCKED_G3, chưa có grant test94/nguồn A cohort.\n\n'+report[report.index('## Phân bổ'):])
md(OUT/'runbook.md','''# Vận hành checkpoint005 — chưa phát main

Đọc reports/tu-soat-005/bao-cao.md và LOG phiên6. Kiểm chỉ đọc:

```powershell
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/trien-khai-005/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-005.json
```

Hiện chỉ được chuẩn bị/kiểm DEV như đã cấp; không đổi cờ G3/test hoặc phát plan giả. Không chạy lại helper create-only cũ. Giữ G2/pilot hợp lệ.

Sau G3/grant đúng phạm vi: (1) tạo bản LOCKED của protocol/policy theo đúng code/config/env/placement được Minh duyệt; ghi nguồn quyền cụ thể, không lấy fixture làm quyền. (2) materialize/attest metadata runtime/independent/binding từ G1 và nguồn gốc đúng94ca, C-e verified/insufficient; A đúng3CSVcohort và grant riêng. Không dùng nhãn/path vào phương pháp. (3) API materialize_main.build(protocol_ref,bundle_ref,grant,destination) biên dịch child plan/authority từng host+aggregate bất biến; kiểm full lock trước phát. Không có auto-dispatch.

Gói freeze007 chứa code/metadata công khai; không chứa nhãn/private source/test telemetry. Chuyển TT theo transfer-plan005 sau grant; hash đích đủ90tệp/máy và code đủ trước chạy. Future main roots khác nhau theo ec2_1/ec2_2 trong dispatch-contract005-final, không dùng cùng prefix của DEV. Bundle/private refs dùng path tương đối code root để có thể chạy trên Linux; nguồn quyền/executable dùng đúng bản từng host. Giữ nguyên metadata fingerprint nguồn khi đổi data_root, không sửa source_row hoặc nhãn để cho khớp.

Mỗi máy dùng main executable đã ghim với p7.py run/resume --plan <path> --sha256 <pin> --authority <path> --authority-sha256 <pin>. p7.py khởi supervisor độc lập SSH; dùng status đọc, drain ngừng phát và để active seal, resume cùng plan/root để nhận token/PID. Không auto retry. Không tự đổi chủ lô khi mất SSH; kiểm controller/PID/attempt rồi mới quyết. Trước phát chừa RAM/đĩa theo plan; laptop cắm điện/không sleep phải được xác minh, không giả định. Không tự bật/tắt EC2 hoặc Scheduled Task.

Nhận mỗi lô vào vùng mới dưới results/T-054, giữ archive/manifest/receipt/envelope gốc. Kiểm hash+bytes tất cả tệp nhận, không sửa đường dẫn trong nội dung. Trong **cùng một process Python**: gọi bien_nhan.receive_paths({remote_ec2_1_code_root:local_received1, remote_ec2_2_code_root:local_received2}); load plan/snapshot bằng read_pin; nguon.authorize(aggregate_plan,authority,'report') kiểm toàn child plan; đối chiếu parts với execution_plan_refs đã khóa; cham.merge_partitions(aggregate_plan,parts) kiểm đủ/không trùng rồi atomic snapshot. Sau đó gọi p7.main(['report', '--plan',..., '--sha256',..., '--authority',..., '--authority-sha256',..., '--snapshot',..., '--snapshot-sha256',...]) ngay trong process đó để giữ mapping. CLI riêng lẻ không tự nạp mapping remote. Chỉ report sau binding và snapshot đủ; quyền nhãn độc lập vẫn bắt buộc. Không chuyển raw test về vì bản gốc còn laptop.

Thời gian0055–9h là kịch bản có giả định, không phải trần. Theo dõi RAM/free disk/temp/phase/heartbeat/error; định kỳ nhận để phát hiện thiếu kết quả, không xóa remote khi chưa Minh duyệt. Lỗi nguồn/permission/schema/adapter/prep/monitor/phân loại mới thì DRAIN phần phụ thuộc, giữ attempt và báo. Không tiến triển/lặp vô tận/hàng chục giờ chưa xong thì báo; PENDING không TIMEOUT. M1 seal trước C-d3; prep trước TORAI; lô độc lập ba máy song song. Không thêm baseline/pilot mặc định.

RE3 H1/H2 và grant cuối tách riêng; chưa có adapter thực được kiểm trên nguồn RE3. Chưa commit/push. Prompt Claude trung tính ở LOG, không tự gửi.
''')

state=ROOT/'docs/STATE.md';raw=state.read_bytes();lines=raw.splitlines(keepends=True)
replacement='- **T-054 — chuẩn bị P7(a): hoàn tất chuẩn bị hai EC2+laptop, DỪNG trình G3 trước main/test.** Codex làm, Claude phản biện. Giữ G2/40slot dev+2slot004;005 chỉ1ca M1 DEV trên2máy, output khớp; EC2_2~67s, EC2_1 thu hồi sau lỗi theo dõi (cost không hợp lệ). TT60 sẵn1,309GB/180tệp khớp nguồn. Lịch30TT/EC2, laptop OB+baseline/A; đã kiểm ghép/không thiếu/trùng. Ước5–9h có giả định, không trần/ETA toàn nghiên cứu. G3/grant test/Acohort/bindings còn riêng; RE3 schema/adapter OPEN. [LOG phiên6](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md), [hồ sơ005](../results/T-054/reports/tu-soat-005/bao-cao.md).'
state.write_bytes(b''.join((replacement.encode()+ (b'\r\n'if line.endswith(b'\r\n')else b'\n'))if line.startswith('- **T-054'.encode())else line for line in lines))
print(json.dumps({'updated':'multi-host candidate docs/spec/STATE','TT60_strict':180,'hosts':placement['counts'],'G3':False,'main':False}))
