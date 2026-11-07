"""Ghi điểm tiếp nhận và gói code đúng byte; không nghiệm thu hoặc cấp quyền main."""
import difflib
import hashlib
import json
import re
import shutil
import tarfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=OUT/'runs/trien-khai-003'

def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,value):
    assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

freeze=OUT/'runs/freeze-cong-cu-005';freeze.mkdir(exist_ok=False)
old=json.loads((OUT/'runs/freeze-cong-cu-004/files.json').read_bytes());files={}
for relative in old['files']:
    src=ROOT/relative;dst=freeze/'code'/relative;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    b=dst.read_bytes();files[relative]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
           'git_blob_from_exact_bytes':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
save(freeze/'files.json',{'files':files,'contains_private_labels':False,'contains_telemetry':False,
    'HEAD_is_not_working_tree':True,'status':'CODE_CHECKPOINT_NOT_G3_FREEZE',
    'protocol_and_matrix':'current CANDIDATE metadata, not executable for main',
    'historical_pilot_code_versions':pin(RUN/'code-version-lineage.json')})
with tarfile.open(freeze/'code.tar.gz','w:gz')as archive:
    for relative in files:archive.add(freeze/'code'/relative,arcname=relative,recursive=False)
save(freeze/'package.json',{'archive':pin(freeze/'code.tar.gz'),'files_manifest':pin(freeze/'files.json'),
     'status':'CODE_CHECKPOINT_NOT_G3_FREEZE','test_allowed':False,'main_started':False})

for p in (OUT/'scripts').glob('*.py'):
    before=OUT/'runs/freeze-cong-cu-004/code/results/T-054/scripts'/p.name
    patch=''.join(difflib.unified_diff(before.read_text(encoding='utf-8').splitlines(keepends=True),p.read_text(encoding='utf-8').splitlines(keepends=True),fromfile=str(before),tofile=str(p)))
    (RUN/('diff-'+p.stem+'.patch')).write_text(patch,encoding='utf-8')
spec=ROOT/'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md'
(RUN/'diff-SPEC.patch').write_text(''.join(difflib.unified_diff((RUN/'SPEC-before.md').read_text(encoding='utf-8').splitlines(keepends=True),spec.read_text(encoding='utf-8').splitlines(keepends=True),fromfile='SPEC-before',tofile='SPEC-current')),encoding='utf-8')

template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
def block(title):return template[template.index(title):].split('```text',1)[1].split('```',1)[0].strip()
common=block('## Prompt chung')
values=['T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md','soát kết quả','P6/G3(a), P7(a)',
 'Codex làm; Claude phản biện',
 'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; các nguồn trực tiếp được dẫn trong SPEC',
 'results/T-054/runs/soan-spec-001/nguon-phan-bien-001.txt, nguon-phan-bien-002.txt, phan-hoi-002.md',
 'results/T-054/scripts/; manifest-trien-khai-003.json; runs/trien-khai-003/; source-manifest.json; runbook.md; các source/revision được dẫn trong manifest',
 'chỉ đọc và trả lời trong chat; chưa cấp file phản biện mới']
matches=re.findall(r'<[^>]+>',common);assert len(matches)==len(values)
for before,after in zip(matches,values):common=common.replace(before,after,1)
prompt='\n\n'.join([common,block('### Soát kết quả'),block('### G3 — Khóa thiết kế trước khi mở test')])
(RUN/'prompt-claude.txt').write_text(prompt+'\n',encoding='utf-8')

ending='''

### Kết thúc phiên 4 — checkpoint 003, chưa đủ G3/chưa chạy chính

**1. Đã làm.** Đọc lại yêu cầu và tiếp nhận checkpoint002 (2.179 pin khớp). Sửa câu chữ hiện hành trong SPEC/hồ sơ: B chính/A phụ đã có, cap không phải ETA, RE3 phải chuẩn bị hợp đồng trong pha1; không chọn lại baseline. Hoàn thiện source/label reader từ nguồn G1/allowlist/command gốc, rồi chạy hai gói dev local thật. Bốn ca: TT a5cabe5fa7/03d4910932, OB 607751ac0a/2bfc97b01e. Gói cuối007 có32slot và008 có8slot; seal trước ghép nhãn dev, báo cáo lần lượt reports/pilot-local-002 và003. Giữ report đầu ở pilot-local-001.

Nguồn quyền nằm trong quyen-minh.txt, grant-A-dev.json và grant-diagnostic-thread.json tại runs/trien-khai-003. A chỉ đúng một ca dev được cấp ba CSV/ba seed; không phải quyền toàn cohort. Chẩn đoán luồng chỉ đúng một ca OB; không phải thay cấu hình main. Đã đính chính tiền đề “nguồn lịch sử16”: current16 không chứng minh source thread lịch sử, phần ấy vẫn OPEN.

**2. File thay đổi.** Bảy script T054: bien_nhan, nguon, worker, dieu_phoi, cham, pilot, lap_ho_so; p7/fixtures giữ byte. SPEC sửa mô tả quyền/trạng thái theo nguồn Minh, không thay thiết kế. Chín hồ sơ hiện hành trong results/T054 được đồng bộ; LOG chỉ nối, STATE chỉ dòng T054. Thêm runs/trien-khai-003, reports/tu-soat-003, ba báo cáo pilot dev, freeze-cong-cu-005 và manifest003. File set chính xác ở manifest; trước phiên ở before.json. Không sửa src/AGENTS/MRP/DECISIONS/WHY hoặc đầu ra task cũ. Các thay đổi có sẵn của Minh được giữ.

Sửa lỗi công cụ có bằng chứng: authorize ép nguồn quyền TXT thành JSON; probe môi trường py38 có thứ tự đường thư viện sai; C-d3 thiếu cạnh từ extra.canh; CIRCA thiếu window.circa_current; snapshot ERROR thiếu kiểm phân loại. Chỉ lặp C-d3/CIRCA do lỗi wrapper, giữ main và kết quả đầu; không retry phương pháp để tìm điểm tốt. Sửa CIRCA sau xem bảng dev được khai riêng, chưa dùng test.

**3. Kiểm và số đo.** Transport60PASS, tám kiểm nguồn gốcPASS, 16 kiểm guard mớiPASS, code nền93pin và ba upstream revision/tracked-clean khớp. Hai gói đủ40VERIFIED, không đồng nghĩa40OK: giữ hai ERROR TT, hai UNSUPPORTED OB và C-d3 UNSUPPORTED_CYCLIC trong gói đầu. Hai ERROR có audit operation0spanN/210spanA, đúng code và ERROR baseline cũ; receipt chỉ DEV, không được áp test/TIMEOUT. TORAI A/B đủ ba seed trên ca đầu, B thêm ca TT thứ hai; prep byte và normalized digest khớp giữa seed trên laptop. C-c/C-g khớp T050 ở bốn phép đối chiếu hai ca. Chín script hợp lệ cú pháp; export metadata không ghi đè hồ sơ/quyền.

Thời gian trong thoi-gian-va-kich-ban.json: 42attempt cócost gồm lượt sửa, tổng2383,192giây, chẩn đoán riêng11,469giây. Hai gói từmốcđầutớisupervisorcuốidừng3369,694giây (~56,16phút, gồm ngắt kiểm/sửa); tổng việc máy khoảng40phút. Giữ cùng start/cost cap qua chuyển plan, không reset hoặc đổi chưa chạy thành trượt. M1TT hai ca khoảng118/212giây; M1OB49/51giây. Ngoại suy lạnh một worker cho ma trận chính+A phụ khoảng24,71giờ, giả sử C-e60 cùng chi phí mainTT thêm1,97giờ; đây là CANDIDATE CHƯA KIỂM, không ETA/cap/cận trên, chưa dự đoán C-d3 hỗ trợ hoặc hiệu quả cache/song song. Không phát main từ các số ấy.

Parity cuối: gói007 chỉ MicroRank OB1luồng lệch1ULP; cùng normalized input, diagnostic thư viện thực16luồng khớp nguồn, hạng không đổi. Gói008 M1/T12 OB so nguồnEC2 còn lệch tối đa2ULP/1ULP; các trường rời rạc/thứ tự/vùng đã so không đổi, nguyên nhân riêng cònOPEN. Không thêm dung sai, không sửa số để khớp. Các giá trị/diff nằm trong parity-complete/parity/numeric-parity-analysis. Biên nhận kiểm toàn checkpoint tại validation.json chỉ xác nhận toàn vẹn/quyền/phạm vi, không thay G3 hoặc bằng chứng khoa học.

**4. Phần chưa xong.** Pha1 chưa hoàn tất. Còn bundle/cache dữ liệu và E4 giữa vế, cache prep thực sự dùng lại, scheduler/throughput1→2/3, C-e và các cặp giúp/hại/không đổi chưa phủ đủ; finalization ERROR/TIMEOUT main, monitor/clock/sleep, quy tắc cạn trần, độ nhạy, nguồn test/A cả cohort và revision trước G3. Mọi mục giữ nghĩa vụ nguồn/SPEC; không bỏ vì chưa làm. RE3 H0 hợp đồng có rồi (30ca/10ô/138129790byte theo metadata đã pin), chưa có schema local, chưa H1/H2 adapter, chưa H3/H4; không tải/mở telemetry hay sửa src. Cần trình đúng quyền/file/schema trước phần phụ thuộc. Chưa có kết quả test trả lời RQ3b/d; detector, vùng thật, cơ chế vật lý và P8–P10 vẫn theo MRP.

Điểm tiếp nhận chi tiết: runs/trien-khai-003/buoc-tiep-theo.md; báo cáo chính reports/tu-soat-003/bao-cao.md. Đọc hai file này trước bắt đầu việc mới. Code đúng byte mỗi gói tại code-version-lineage.json và code-pilot-*; phiên bản006 được dựng lại từ bản007 bằng đảo đúng patch CIRCA rồi đối hash job. Lần dựng đầu sai LF/CRLF được giữ trong code-pilot-006/reconstruction-failure.json; bản đúng ở code-pilot-006-r2. Freeze005 là code hiện tại, không phải byte đã tạo mọi kết quả cũ hoặc khóa G3. Data/private refs không nằm trong gói code. Nếu máy khác thiếu ref private, dựng lại từ recipe/nguồn gốc đúng quyền và lưu lineage, không đọc repo RCA lưu trữ/test.

Không chạy lại chot_va_sua_cd3/hoan_thien_code_sau_pilot/nhan_tiep_env: các bước đó đã áp dụng, có đích create-only và lịch sử. Đầu ra đã hợp lệ không làm lại. Bước tiếp là triển khai phần công cụ/cache/điều phối còn thiếu trong đúng SPEC và so với các bản lạnh đã có; chốt lựa chọn khoa học với Minh trước phần phụ thuộc, không xin lại quyền công cụ/dev đã cấp. Phân biệt phần chưa làm với dữ kiện cần Minh cấp. Dừng báo trước main theo lệnh Minh; hiện chưa xin G3/chạy chính khi bằng chứng còn thiếu.

Các quyết định cần sổ chính thức đã trình trong de-xuat-so-quyet-dinh.md và ghi nguồn nguyên văn trong LOG/grant; chưa nối sổ khi chưa duyệt đúng dòng. Chưa commit/push. Đề xuất nội dung commit checkpoint nếu Minh duyệt đúng file: “T-054: pilot dev local, sửa binding/C-d3/CIRCA và cập nhật hồ sơ”; cần chọn file trước, không tự thêm dữ liệu/private vào git.

Lệnh cuối được dùng chốt checkpoint (chỉ đọc, kết quả sau khi lập manifest):
`& 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe' -X utf8 -B 'results/T-054/runs/trien-khai-003/kiem_checkpoint.py' --manifest 'results/T-054/manifest-trien-khai-003.json'`

Prompt trung tính để Minh chọn chuyển sang Claude; chưa tự gửi, chưa mở REVIEW hoặc đề nghị nghiệm thu:

```text
'''
with (ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').open('ab')as stream:
    stream.write((ending+prompt+'\n```\n').encode('utf-8'))
print(json.dumps({'freeze_files':len(files),'LOG_appended':True,'main_started':False,'G3':False}))
