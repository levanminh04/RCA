"""Finalize the H2 checkpoint once, without publishing or opening any dataset."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
LOG = ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md'
STATE = ROOT/'docs/STATE.md'


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(name, value):
    (RUN/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


assert not (ROOT/'results/T-054/manifest-cai-re3-h2-010.json').exists()
c = json.loads((RUN/'checkpoint.json').read_text(encoding='utf-8'))
audit = json.loads((RUN/'audit.json').read_text(encoding='utf-8'))
tests = {}
for rel in ['synthetic-004', 'integration-001', 'integration-003', 'edges-005', 'wiring-001']:
    v = json.loads((RUN/rel/'checks.json').read_text(encoding='utf-8'))
    rows = v['checks'] if isinstance(v, dict) else v
    failed = [r['name'] for r in rows if not r['PASS']]
    if rel == 'synthetic-004':
        assert failed == ['worker_generated_RE3_microrank']
    else:
        assert not failed, (rel, failed)
    tests[rel] = {'passed': sum(r['PASS'] for r in rows), 'failed_retained': failed,
                  'reused_rows': sum('reused_from' in r for r in rows), 'result_ref': pin(RUN/rel/'checks.json')}
assert json.loads((RUN/'torai-py38-001/validation.json').read_bytes())['PASS']
assert json.loads((RUN/'environment-py38.json').read_bytes())['RE3_profile_validation_without_pyarrow'] == 'PASS'
save('validation.json', {'status': 'PASS_WITH_RETAINED_SUPERSEDED_FAILURES', 'groups': tests,
                         'MicroRank_failed_assertion_resolved_by': 'integration-001/checks.json#/worker_RE3_microrank',
                         'torai_py38_seed0': 'PASS_NATIVE_OK', 'py38_profile_without_pyarrow': 'PASS',
                         'code_audit': audit, 'scope': 'generated signals only; mocks separately identified in each group',
                         'RE3_telemetry_opened': False, 'main_started': False, 'G3': False, 'cloud_paused': True,
                         'formal_review_completed': False})

template = (ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
def block(heading):
    return re.search(r'```text\n(.*?)\n```', template.split(heading, 1)[1], re.S).group(1)
common = block('## Prompt chung')
values = {
    '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>': 'T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; results/T-054/runs/cai-re3-h2-010/',
    '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>': 'soát kết quả',
    '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>': 'P7(a), chuẩn bị G3',
    '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>': 'Codex người làm; Claude người phản biện',
    '<danh sách đường dẫn và git diff từ commit gốc nếu có>': 'AGENTS.md; SPEC/LOG T-054; docs/STATE.md, MRP.md, WHY.md, DECISIONS.md, LESSONS.md; nguồn đề tài dưới đây; code-diff.patch và documents-diff.patch trong checkpoint010',
    '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>': 'Các lượt được LOG T-054 dẫn theo thời gian',
    '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>': 'results/T-054/manifest-cai-re3-h2-010.json; results/T-054/runs/cai-re3-h2-010/{bao-cao.md,checkpoint.json,audit.json,validation.json,code-binding-candidate.json,environment-main.json,environment-py38.json}; source và snapshot trong010; D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B và D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe -X utf8 -B',
    '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>': 'Chỉ đọc và trả lời trong chat; chưa có quyền ghi bản REVIEW, sửa file, mở dữ liệu khóa, chạy phương pháp, SSH/sync, commit hoặc push',
}
for old, new in values.items():
    assert old in common
    common = common.replace(old, new)
prompt = common+'\n\n'+block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n'
(RUN/'prompt-claude.txt').write_text(prompt, encoding='utf-8')
ending = '''

### Kết thúc checkpoint010 — H2 đã cài và tự kiểm trong phạm vi duyệt

Đã cài9fileH2 và3điều kiện trong2fileCIRCA được Minh duyệt thêm; SPEC/WHY/DECISIONS ghi nguồn trước code. Reader/profile/M1, dispatch/grant/held-out tables riêng và wrappers giữ default cũ. Báo cáo đầy đủ: results/T-054/runs/cai-re3-h2-010/bao-cao.md. Không sửa m1/chuoi/kernel hoặc chọn lại cấu hình nghiên cứu.

Bằng chứng kiểm:48PASS004 trước assertion sai épMicroRankOK; đã phân xử và kiểm lại đúngNO_EVIDENCE trong23PASSintegration001. integration003 có27dòngPASS (4worker tái dùng001);edges005 có23PASS;wiring001 có2PASS. Kernel TORAI B thật quaCSV/Python3.8 seed0OK. Mocks chỉ dùng phần phép tính bảng/receiptgiám sát và riêngBAROwiring; không gọi là khoa học hoặc kiểmkill thật. Defaults TT/Nezha inputexact; BARO/TraceRCA/CIRCA toànoutputexact; TORAIprepdefault exact. Source/hash/AST/diff kiểmtrong audit.json/validation.json, không cộng các lượt thành kiểm độc lập.

Giữ mọi lượt hỏng: progress001ghi bất biến hai lần; fixture002ms clock tham chiếu chưa chuyển đủ;003T12thiếu snapshot giả;004MicroRanktestkỳvọngOKsai;edges001thiếu pathDrain3. ProbePy38thiếuPyArrow phát hiện lỗi import eager, đã sửa readerimportlazy và kiểmprofilePy38khôngcầnPyArrow. Không cài package hoặc sửa dữ liệu để cứu method. Phiên bản/đườngimport hiệu lực của kiểm đã lưu environment-main/py38.json.

Audit104bindingứngviên:93codepin kế thừa khôngđổi,10đổi đúngquyền+reader mới;583output008 không thuộc phần sửa giữhash;15output009bấtbiến giữnguyên. Diffđãđọc trọn theo snapshotphạmvi. WHY/DECISIONS/LOGchỉnối;SPECchỉthêm quyền;STATEchỉdòngT054. Codebinding010chỉcandidate, không tựkhóa G3 hoặc cập nhật/phát plan008.

OPEN: H1units/r/cadence/U/alias/trace status chưa đủnguồn; chưaprofile/grant/protocolRE3thật; TORAI A chưanguồnriêng; quy tắc chấp nhậnERRORRE3 còn cần hồsơ trướcH3, không lấy auditTT suyra. Cloud vẫn tạmdừng theoMinh. H2 đạt phần cài/tựkiểm, chưa nghiệmthu/kiểmđộc lập hoặc trảlờiRQ3/RQ5; không telemetryRE3/main. Claude chưa kiểm010. Quyếtđịnh thêm chỉquyềncàiH2+bổsungCIRCA, không biến giảđịnhthànhFACT.

Fileđổi:11code;SPEC/WHY/DECISIONS;LOGnối vàdòngT054STATE;outputs/manifest010. Chưa commit/push; đềxuấtcommit khiMinh muốn: “Cài adapter RE3 H2 và kiểm tuyến held-out bằng fixture”.

Bướctiếpchínhxác: đọcbao-cao010 mụcĐiềucònmở vàtime-and-observation-contract.json009; tra nguồnexport/deploymentđượcphép đểhoànthiệnH1, trìnhphầnquyếtđịnhcònthiếu; sauđó cậpnhật binding/bundle/plan/hồsơG3 đúngcode. Không chạy lại baselineđãhợplệ; khôngdùngpin008chocode010. Không đọc telemetry đểchọnprofile. Không chạy bootstrap/finish/checkscript vào thưmụcđãcó. Lệnhcuối: python -X utf8 -B results/T-054/runs/cai-re3-h2-010/finish.py, rồi kiểmmanifest010vàgit diff --check. PromptClaude dưới đây đểMinh chọnchuyển; khôngtựgửi.

### Prompt Claude — checkpoint010

```text
'''+prompt+'```\n'
with LOG.open('a', encoding='utf-8', newline='') as f:
    f.write(ending)
before_state = (RUN/'before/docs/STATE.md').read_bytes()
assert STATE.read_bytes() == before_state
old_line = next(s for s in before_state.splitlines(keepends=True) if s.startswith(b'- **T-054'))
new_line = ('- **T-054 — checkpoint010: H2 RE3 đã cài/tự kiểm; H1 và G3 còn mở.** Codex làm, Claude phản biện. Reader/M1/baseline/grant/worker/bảng RE3 riêng; kiểm bằng fixture, gồm TORAI B Python3.8. Đã lưu snapshot/diff/manifest và giữ lượt hỏng. Chưa có units/r/U/alias/protocol/grant RE3 thật; cần cập nhật pin/bundle trước G3. Cloud tạm dừng theo Minh; chưa mở telemetry RE3/main. [010](../results/T-054/runs/cai-re3-h2-010/bao-cao.md), [LOG](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md).\r\n').encode('utf-8')
STATE.write_bytes(before_state.replace(old_line, new_line, 1))
assert STATE.read_bytes().replace(new_line, old_line, 1) == before_state
c.update(status='H2_IMPLEMENTED_SELF_CHECKED_H1_OPEN_NOT_G3',
         completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
         final_tests=tests, formal_review_completed=False,
         next='Resolve H1 using allowed source metadata; freeze updated bindings/bundles and G3 dossier; no telemetry/main/cloud access')
save('checkpoint.json', c)
subprocess.run(['git', 'diff', '--check', '--', *audit['code_files'], *audit['document_files'],
                'docs/STATE.md', str(LOG.relative_to(ROOT))], cwd=ROOT, check=True)
for rel in ['docs/WHY.md', 'docs/DECISIONS.md', str(LOG.relative_to(ROOT))]:
    assert (ROOT/rel).read_bytes().startswith((RUN/'before'/rel).read_bytes())
code_binding = json.loads((RUN/'code-binding-candidate.json').read_bytes())
for rel, expected in code_binding['files'].items():
    path = Path(rel) if Path(rel).is_absolute() else ROOT/rel
    assert pin(path) == expected, rel
manifest = {'schema': 'T054-RE3-H2-010', 'status': c['status'],
            'previous_manifest': {'path': 'results/T-054/manifest-chuan-bi-re3-009.json',
                                  **pin(ROOT/'results/T-054/manifest-chuan-bi-re3-009.json')},
            'outputs': {str(p.relative_to(ROOT)).replace('\\','/'):pin(p) for p in sorted(RUN.rglob('*')) if p.is_file()},
            'mutable_current': {rel:pin(ROOT/rel) for rel in audit['code_files']+audit['document_files']+
                                ['docs/STATE.md', str(LOG.relative_to(ROOT)).replace('\\','/')]},
            'worker': 'Codex', 'reviewer': 'Claude', 'formal_review_completed': False,
            'RE3_telemetry_opened': False, 'main_started': False, 'G3': False, 'cloud_paused': True,
            'fixture_authorities': 'FICTIONAL ONLY, NOT USER GRANTS'}
(ROOT/'results/T-054/manifest-cai-re3-h2-010.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'PASS': True, 'outputs': len(manifest['outputs']), 'code_files': len(audit['code_files']),
                  'H2': 'implemented/self-checked', 'H1': 'OPEN', 'G3': False, 'telemetry': False}))
