"""Complete the neutral handoff using saved evidence and the review template."""
import csv,hashlib,json,pathlib,re,datetime,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-015';TASK=ROOT/'tasks/T-015-ho-so-microrank'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def append(p,t):
    with p.open('a',encoding='utf-8') as f:f.write('\n\n'+t+'\n')
identity=j(OUT/'runs/final-input-identity-audit/summary.json');assert identity['all_passed'] and len(identity['cases'])==90
verified=j(OUT/'runs/setup/input-verified.json');assert len(verified)==189 and all(v['ok'] for v in verified)
transfer=j(OUT/'runs/transfer/expected.json');assert sum(v['bytes'] for v in transfer)==960754806
expected={v['path']:v['sha256'] for v in transfer}
for item in j(OUT/'runs/ob-comparison-manifest.json')['sources']:
    assert item['source_sha256']==expected[item['case']+'/traces.parquet']
save(OUT/'runs/final-source-manifest.json',{'files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((ROOT/'src/microrank').glob('*')) if p.is_file()],
     'pre_guard_adapter_matches_saved_inventory':j(OUT/'runs/source-versions/adapter-recovery-proof.json'),
     'unchanged_official_kernel_ast':True,'note':'88 earlier valid graphs have no current duplicate; final guard passes all90 raw windows. Root correction changes audit labels only.'})
doc=OUT/'de-xuat-tai-lieu-chung.md'
append(doc,'''## 9. Cụ thể hóa nguyên văn đoạn cũ cho đề xuất §4

**File đích:** docs/MRP.md §2.3.

**Đoạn cũ:** "K1 §D.3 ghi một phản ví dụ quan trọng: MicroRCA và MicroRank chỉ dùng PageRank **sau khi** đã phát hiện bất thường cục bộ, nên đồ thị không tham gia việc phát hiện. Nếu chỉ làm theo nghĩa rộng, cô hỏi \"đồ thị phát hiện bất thường ở đâu?\" sẽ không trả lời được."

**Đoạn mới:** "K1 §D.3 phân biệt PageRank với detector: PageRank của MicroRCA/MicroRank chạy sau khi đã phân loại bất thường. Riêng code MicroRank gốc còn dùng quan hệ span cha–con khi học SLO self-time; vì vậy PageRank không quyết định nhãn, nhưng không thể suy mọi thông tin quan hệ đều vắng khỏi tiền xử lý detector. Luật span của bản RCAEval không có bước self-time này. Phần P6 vẫn cần chỉ rõ loại đồ thị nào tham gia trực tiếp vào điểm bất thường."

**File đích:** docs/WHY.md WHY-02, chỉ thay câu sau trong dòng Vì sao.

**Đoạn cũ:** "Trong MicroRCA và MicroRank, PageRank chỉ chạy sau khi đã phát hiện bất thường cục bộ, tức đồ thị không tham gia việc phát hiện (K1 §D.3)."

**Đoạn mới:** "Trong MicroRCA và MicroRank, PageRank chạy sau detector. Riêng code MicroRank gốc dùng quan hệ cha–con khi học SLO self-time; do đó câu kết luận không có quan hệ tham gia phát hiện chỉ đúng khi nói riêng đồ thị PageRank, không đúng cho mọi tiền xử lý có cấu trúc."

**File đích:** docs/knowledge/K1-phuong-phap-rca.md §C.3, dòng Detector.

**Đoạn cũ:** "- **Detector.** Từ normal window, paper ước lượng `μ_o, σ_o`, đặt operation SLO `μ_o+1.5σ_o`, rồi cộng SLO theo số operation trong trace để tạo expected trace latency. Trace thực vượt expected bị xem là abnormal. Cửa sổ online 30 giây; khi trigger, thu thêm khoảng 5 phút trace."

**Đoạn mới:** "- **Detector.** Bài dùng normal history của handling time để học μ_o,σ_o và dự báo latency theo số operation. Code gốc tính handling time bằng duration cha trừ duration con quan sát được; quan hệ cha–con tham gia bước học SLO. System alarm dùng μ+1.5σ và hơn8trace; partition RCA dùng μ+σ+50ms. Bài dùng cửa sổ30s; code detector60s và RCA−5/+55s. PageRank chạy sau partition và không tự quyết định nhãn bất thường."

**Vì sao/phụ thuộc cho ba sửa:** đã kiểm nguồn cha–con và hai luật gốc trong T015; sửa phạm vi lập luận về graph, không tự quyết thiết kế P6. Các câu K1 chỉ nói riêng PageRank có phạm vi đúng, nên không đề xuất đổi chúng thành lời khẳng định PageRank phát hiện bất thường.

**Không đính chính thành lỗi:** K1 ghi Ochiai mặc định và R@2≈66% là đúng cho thực nghiệm bài MicroRank. Code revision T015 gọi Dstar2, có R@2=54% trong dòng khác của bảng bài. Hồ sơ T015 đã tách hai nguồn; không sửa số66 thành54 một cách máy móc.''')
save(OUT/'runs/t004-availability-audit.json',{'task':'T-004','source_state':'docs/STATE.md','task_directories':[str(p) for p in (ROOT/'tasks').glob('T-004*')],
    'result_directories':[str(p) for p in (ROOT/'results').glob('T-004*')],'state_says_not_implemented':True,'raw_data_not_read':True})
append(OUT/'dinh-chinh-task-cu.md','''
T-004 chưa triển khai: không có thư mục task/kết quả ở lần rà cuối, STATE cũng ghi như vậy (`runs/t004-availability-audit.json`). Không có kết quả T-004 để tái kiểm. Audit các task cũ chỉ bao phủ nhận định liên quan đầu vào/cơ chế trace; không chứng nhận lại toàn bộ phương pháp và mọi số của T-000–T-012. K1 Ochiai/66% phù hợp bài, đã kiểm nên không báo thành lỗi chỉ vì code đang dùng Dstar2.''')
criteria=[
 ('1','đạt','manifest-inputs.json; source git sạch đúng3revision; runs/setup/input-verified.json189hash; T007 artifact tái dùng'),
 ('2','đạt','ho-so-microrank.md; tracerca-rcaeval.md; ho-so-phat-hien-trace.md; mặc định/file:dòng và điều kiện tác giả/suy từ code tách riêng'),
 ('3','đạt cho giao thức đã cài','toy AST gốc; exact-copy giữ occurrence; final identity90ca; phổ không âm; missing/baseline/group có trạng thái'),
 ('4','đạt','so-sanh-tung-ca.csv90ca hợp lệ;2failure ban đầu giữ, chọn rerun có chỉ định; không chạy lạiT007'),
 ('5','đạt phạm vi3dev đã định trước','bang-ung-vien-tt.csv204dòng;33check; ca lớn TT/socket; toy service không cạnh; không khái quát30ca'),
 ('6','đạt','raw→graph19check và nullable correction;4383math +2729trace vector so trực tiếp; root chỉ sau rank'),
 ('7','đạt','TraceRCA T00790NaN/79order tái dựng; adapter finite-before-sort/tie ổn định; không chọn theo điểm'),
 ('8','đã kiểm, có control báo giả','seed/cột/dòng/window/intermediate/normal-only đã chạy; normal-only không xác nhận phát hiện; thiếu số full-original nêu giới hạn'),
 ('9','đạt sau hoàn tất bàn giao','CSV16cột/7dòng; ledger110;2errata; drafts; exhaustive manifest; prompt nguyên văn; chỉ STATE rowT015'),
 ('10','đạt','SSH hai máy; rm đúng một lần trên máy đầu, test absent; không Stop/reboot/config')]
with (OUT/'tieu-chi-xong.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['tieu_chi_SPEC','ket_luan','bang_chung_va_gioi_han']);w.writerows(criteria)
report='''# Bàn giao T-015 — 04/10/2026

## A. Đã làm

Hoàn thành hồ sơ MicroRank, TraceRCA RCAEval và hai bộ phát hiện, đủ7+2mục. Cài **MicroRank-RCAEval sửa đầu vào**; so90ca RE2-OB với kết quả T007 đã lưu. Chạy3ca dev Train Ticket đã chọn trước, kiểm tập ứng viên, ví dụ độc lập và tính khả thi suy schema cho bản gốc. Đề xuất biến thể này cho giao thức span hiện có ở P3 theo cơ chế/QT2; đây là CANDIDATE, không chọn theo điểm cao hơn (chờ WHY, xem de-xuat-tai-lieu-chung.md).

## B. File đã thay đổi

`tasks/T-015-ho-so-microrank/SPEC.md`, `LOG.md`; mọi file trong `results/T-015/`; sáu file trong `src/microrank/`; đúng dòngT015 trong `docs/STATE.md`. Danh sách từng file, gồm scripts, logs, mọi lượt hỏng, source versions và kết quả: `manifest-ban-giao.json`.

Ngoài repo: `D:/RCA-ext/work/T-015/known_hosts`, `uv-linux`. Trên hai EC2: mọi file tạo trong `/home/ubuntu/rca/T-015/`, danh sách từng đường dẫn trong manifest. Máy hai có runtime/env/cache/tmp,189file input, code và runs; máy đầu giữ pilot/lượt hỏng. File `/home/ubuntu/.sudo_as_admin_successful` trên máy đầu đã xóa đúng một lần theo quyền có sẵn và kiểm absent. Không sửa clone/env/data chung, file task cũ, WHY/DECISIONS hoặc commit/push.

## C. Kiểm tra đã chạy và kết quả

90đầu ra OB hợp lệ, hữu hạn, không ô phổ âm/không overlap; ledger110lượt gồm hai failure ban đầu. Independent TT4383giá trị khớp0, probe2729trace+298operation PPV khớp0, nguyên hàm MIT không đổi. Hai rerun duplicate có8328/9345giá trị khớp0. Seed/cột/dòng, graph gốc, root nullable, edgecases và hai cửa sổ300/600s đã kiểm. Train Ticket33check/204dòng ứng viên: vắng trace không xếp; service không cạnh vẫn có thể xếp qua incidence; auth full hạng9 nhưng vắng top11operation. Control trước tiêm vẫn báo2814span: báo giả theo giả định pre-injection bình thường, không nguyên nhân có nghĩa. TraceRCA tái dựng90NaN và79ca sắp sai; adapter lọc hữu hạn trước sort và tie canonical. Nguồn chi tiết: `kiem-dung-dan.md`, `runs/final-scientific-audit.json`, `tieu-chi-xong.csv`.

## D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM

DC01:T001 gọi detector TraceRCA gốc3σ, nhưng multiplier mặc định1; đã kiểm AST/toy và sửa hồ sơ T015. DC02: câu tuyệt đối trong MRP/WHY bỏ quan hệ cha–con dùng học SLO self-time; đã đọc đúng source, tách rõ PageRank với tiền xử lý detector và viết nháp sửa. Phạm vi phản bác được ghi: K1 nói riêng PageRank là đúng; Ochiai/66% của bài cũng đúng. Không sửa file cũ. Bằng chứng, hệ quả và đoạn cũ→mới ở `dinh-chinh-task-cu.md` và `de-xuat-tai-lieu-chung.md`.

## E. Chỗ lệch khỏi SPEC và lý do

Minh đổi reviewer sangClaude và cho giữ detector span của biến thể; lý do trước kết quả đã ghi. Chuyển EC2 thứhai do thiếu RAM/máy đầu bận; TT còn3ca trước nhìn ranking vì tổng transfer với OB sẽ vượt1GB nếu chép30ca. Sửa audit token nullable và guard exact-copy theo source gốc, giữ lỗi/lượt cũ. ShellCRLF hỏng trước method; controlTraceRCA ban đầu có11span qua mốc đã được đính chính; không giấu là normal nghiêm. Một lần tìm kiếm quá rộng artifact đã dừng, không dùng để kết luận ngoài whitelist. Mọi thay đổi có mục bổ sung SPEC/LOG; không chọn cấu hình theo root score.

## F. Đề xuất cho tài liệu chung

Nháp trong `de-xuat-tai-lieu-chung.md`: lưu quyền/vai trò/EC2 theo lời Minh; WHY về biến thể, exact-copy và TraceRCA finite/tie; làm rõ cha–con trong K1/MRP/WHY02; sửa default TraceRCA T001; cập nhật việc dọn EC2 ở dòng chung. Chưa ghi các file đó. Đúng dòngT015 của STATE chuyển chờ phản biện.

## G. Phần chưa kiểm và lý do

Chưa tái lập toàn bộ số bài MicroRank/full detector gốc: datasetA/B/C và schema kind/pod/root thật không có trong dữ liệu được phép. Giả định công thức code đủ đại diện bài có thể sai vì các khác biệt đã chỉ ra; kiểm bằng artifact/giao thức tác giả khi được phép, không gán số của bài cho biến thể. Chưa cài phương án suy schema: Minh chỉ duyệt đánh giá; root cấu trúc làm được nhưng kind/pod không nhận diện duy nhất từ11cột. Giả định metadata bổ sung có thể phục hồi sẽ sai nếu exporter đã bỏ trường; cần đối chiếu gold instrumentation độc lập nhãn. Đơn vị raw TraceRCA gốc còn OPEN vì module upstream không nằm trong clone đúngrevision; phải phục hồi nguồn encoder để kiểm, không đoán từ RE2.

Không có thời gian benchmark chính thức vì máy dùng chung; logs chỉ theo dõi ngân sách. Không kiểm coverage/hạn chế tổng quát30ca hoặc datasetP3/P4:3ca là kiểm cơ chế đã định trước, không bảo đảm ca khác. Control giả định trước tiêm bình thường có thể sai do workload drift/sự cố chưa nhãn; cần reference sạch và ground truth riêng ở giao thức sau. Các thiếu kiểm này không được gọi là chờ quyền cho phần task đã làm được.

## H. Cần Minh quyết

Sau phản biện Claude, chốt ởG1: baselineP3 dùng biến thể nào; cửa sổ tham chiếu; inventory và full ranking hay output11operation; quy tắc finite/tie TraceRCA; có nguồn kind/pod thật để đi tiếp phương án full-original không. Duyệt các nháp tài liệu chung nếu phù hợp. T015 chưa tự chốt các lựa chọn này.
'''
(OUT/'bao-cao-cuoi.md').write_text(report,encoding='utf-8')
append(OUT/'kiem-dung-dan.md','''## 7. Tính tương thích của source cuối

Guard identity cuối đã kiểm raw8cột của cả90cửa sổ: không conflict; chỉ hai ca recommendation_loss có duplicate current. Vì vậy88graph/score cũ không bị thay bởi nhánh exact-copy mới; các rows/SLO không bị dedup. Proof ở `runs/final-input-identity-audit/summary.json`. Source adapter trước guard được phục hồi và hash khớp inventory trước đó (`runs/source-versions/adapter-recovery-proof.json`). Source cuối và nguồn MIT trong `runs/final-source-manifest.json`. Root classification sửa độc lập, không gọi lại score. Không suy các lỗi export tạo bản sao từ riêng dữ kiện này.''')
append(TASK/'SPEC.md','''### 04/10/2026 — rà cuối và lệnh kiểm thực tế

Giữ nguyên SPEC trước đó; đối chiếu10tiêu chí ở `results/T-015/tieu-chi-xong.csv`. Guard cuối đã kiểm raw90cửa sổ bằng `validate_identity_policy_ob.py`; không conflict và chỉ hai ca đã rerun có duplicate current. Lệnh kiểm đầu ra: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-015/scripts/final_scientific_audit.py`. Lệnh kiểm toy source gốc: cùng interpreter chạy `test_graph.py`, `test_adapter.py`, `test_null_root.py`, `test_original_formula.py`. Bảng so: `compare_ob.py --fixed-dir ...ob-pilot-ec2-2 --fixed-dir ...ob-block-1 --fixed-dir ...ob-block-2 --fixed-dir ...ob-block-3 --fixed-dir ...ob-duplicate-rerun`; precedence chỉ thay failed bằng rerunok, không chọn giữa hai kết quả hợp lệ khác điểm. Ledger: `compare_ob.py --ledger-only`. Bàn giao/JSON/file-scope: `complete_handoff.py` rồi `validate_handoff.py`. Normal-control báo giả được ghi là kết quả kiểm không đạt ngữ nghĩa phát hiện, không sửa detector hoặc che thành PASS về chất lượng. Source/units TraceRCA upstream/full số tác giả chưa kiểm và hệ quả ở báo cáoG. Không cần thêm một lượt phương pháp trên dữ liệu mới.''')
append(TASK/'LOG.md','''- Rà cuối — cả90rawwindow qua guardidentity, chỉ2rerun cóexactcopy; transfer đúng189file/960754806B mọi hash đạt. Finalaudit90/ledger110/7row16col/sourceAST/cú pháp đạt. Source trướcguard phục hồi hash đúng; thời gian bên trong authworker14,312s và supervisor14,653s tách đúng file nguồn. Bổ sung khác biệt mặc định spectrum: bàiOchiai, codeDstar2; K1/66% không bị báo nhầm là lỗi. T004 chưa có kết quả. Các sourceclone cuối vẫn sạch/đúngrevision.
''')
# Expose an exhaustive list without placing thousands of package paths inside
# the review prompt itself. No file outside the task-owned scopes is enumerated.
local=[]
for folder in [OUT,ROOT/'src/microrank',TASK,pathlib.Path('D:/RCA-ext/work/T-015')]:
    for p in sorted(folder.rglob('*')):
        if p.is_file():local.append({'path':str(p.resolve()).replace('\\','/'),'bytes':p.stat().st_size,
             'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'host':'laptop'})
remote=[]
for name,ip in [('ec2-first-inventory','13.239.30.70'),('ec2-second-inventory','3.26.62.217')]:
    v=j(OUT/'runs'/name/'files-created.json');assert v['all_paths_under_task_root']
    paths={r['path'] for r in v['files']}|{v['self_inventory_written_after_scan']}
    assert all(p.startswith('/home/ubuntu/rca/T-015/') for p in paths)
    remote.extend({'host':ip,'path':p} for p in sorted(paths))
manifest=OUT/'manifest-ban-giao.json'
save(manifest,{'local_files':local,'remote_files':remote,
    'mutable_files_hashed_before_final_handoff':['tasks/T-015-ho-so-microrank/LOG.md','tasks/T-015-ho-so-microrank/SPEC.md'],
    'self_file':str(manifest.resolve()).replace('\\','/'),'state_only_changed_line':'T-015 in D:/RCA-flashticket/docs/STATE.md',
    'deleted_with_prior_authorization':{'host':'13.239.30.70','path':'/home/ubuntu/.sudo_as_admin_successful','rm_executions':1},
    'scope_is_full_manifest_not_git_diff':True})
head='93f13d4c4a966428177e2acc287d96bc89303e92'
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
common=template.split('## Prompt chung',1)[1].split('```text',1)[1].split('```',1)[0].strip('\r\n')
g1=template.split('**G1 — phương pháp, dataset, cách chia:**',1)[1].split('```text',1)[1].split('```',1)[0].strip('\r\n')
outputs='; '.join(str(p.resolve()).replace('\\','/') for p in [TASK/'SPEC.md',TASK/'LOG.md',manifest,OUT/'bao-cao-cuoi.md',OUT/'ho-so-microrank.md',OUT/'ho-so-phat-hien-trace.md',OUT/'tracerca-rcaeval.md',OUT/'vi-du-tinh-tay.md',OUT/'yeu-cau-dau-vao.csv',OUT/'ca-da-chay.csv',OUT/'dinh-chinh-task-cu.md',OUT/'de-xuat-tai-lieu-chung.md'])
outputs+='; mọi file trong results/T-015/, src/microrank/, D:/RCA-ext/work/T-015/ và trên hai EC2 đã liệt kê từng đường dẫn tại manifest-ban-giao.json; source/revision/đường dẫn chạy tại manifest-inputs.json, src/microrank/PROVENANCE.json, moi-truong.md'
filled=common.replace('<T-xxx-tên>','T-015-ho-so-microrank').replace('<T-xxx>','T-015').replace('<danh sách>',outputs).replace('<commit gốc>',head)
ending='''## Kết thúc phiên — 04/10/2026 — Codex, người làm

1. Đã làm gì: báo cáoA bên dưới; hồ sơ, code sửa, so từngca và mọi kiểm thuộc phạm vi đã hoàn tất.
2. File đã thay đổi: báo cáoB và manifest-ban-giao.json, gồm từng file ngoài repo/EC2; STATE chỉ dòngT015.
3. Kiểm tra đã chạy và kết quả: báo cáoC, tieu-chi-xong.csv và final-scientific-audit.json; control báo giả được giữ rõ.
4. Điều chưa chắc/cần Minh quyết: báo cáoG/H; không gọi lựa chọn P3 là DECIDED.
5. Bước tiếp theo chính xác: Minh mở phiên Claude trong D:/RCA-flashticket, dán nguyên prompt cuối LOG; người phản biện chỉ ghi tasks/T-015-ho-so-microrank/REVIEW.md. Sau review, Minh quyết nháp và lựa chọn G1; không tự gửi tin/task ra ngoài.
6. Lệnh cuối hoàn tất bàn giao: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-015/scripts/validate_handoff.py. Trước đó cập nhật đúng dòngT015 bằng state_line.py và kiểm byte ngoài dòng không đổi. Kết quả thực tế được lưu trong runs/final-handoff-check.json; nếu lệnh kiểm lỗi thì chưa được chuyển sang báo hoàn tất.

'''
append(TASK/'LOG.md',ending+report+'\n\n## Prompt phản biện cho Claude — vai trò Minh đã đồng ý\n\n```text\n'+filled+'\n\n'+g1+'\n```')
print(json.dumps({'handoff_local_files':len(local),'handoff_remote_paths':len(remote),'review_common_and_G1_copied':True}))
