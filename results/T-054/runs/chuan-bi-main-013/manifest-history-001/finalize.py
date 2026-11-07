"""Finalize the authorized preparation ledger and immutable output manifest."""
import ast
import difflib
import json
from pathlib import Path

from activate import ROOT,RUN,pin
from bien_nhan import atomic,digest,read_pin,ref,Blocked


def main():
    code=read_pin(pin(RUN/'code-pins.json'))['code_pins']
    for rel,sha in code.items():assert digest(ROOT/rel)==sha,rel
    for host in ('ec2_1','ec2_2'):
        assert read_pin(pin(RUN/(host+'-final-execution-environment.json')))['PASS']
        assert read_pin(pin(RUN/(host+'-fixture-current-received.json')))['checks']==101
    assert read_pin(pin(RUN/'local-final-code-environment.json'))['PASS']
    import main as launch
    try:launch.main(pin(RUN/'grant-template.json'))
    except Blocked as exc:
        assert str(exc)=='WAIT_MINH_FINAL_013_G3_SOURCE_TRANSFER_MAIN_SCORE'
        denied=str(exc)
    else:raise AssertionError('false template started main')
    protocol=read_pin(pin(RUN/'protocol-candidate.json'))
    assert protocol['status']=='CANDIDATE_NOT_LOCKED' and protocol['real_execution_ready']is False
    assert not (RUN/'activated-001').exists()
    before=read_pin(pin(RUN/'before-pins.json'))
    for rel,meta in before.items():
        old=RUN/'before'/rel
        assert digest(old)==meta['sha256'] and old.stat().st_size==meta['bytes']
        if rel.endswith(('LOG.md','DECISIONS.md','WHY.md')):assert (ROOT/rel).read_bytes().startswith(old.read_bytes())
    log='''

## 07/11/2026 — Codex — kết thúc chuẩn bị013, chờ Claude kiểm bản cài

Đã làm: hoàn tất năm wrapper đúng phạm vi, nguồn chiếu R1 đủcohort,1640job+2support theo30/30TT ở hai EC2 mới và laptopOB/CIRCA/MicroRank/A. Chốt hồ sơ theo D1–D4/R3; lưu ngoại lệ đúng phép C-e Minh duyệt, giữ output/strict audit gốc. Hoàn tất entry kích hoạt/chuyển/phát/nhận/chấm có kiểm quyền và policyA. Bằng chứng nguồn: runs/chuan-bi-main-013/{candidate-validation,parity-disposition,cloud-verification,scope-and-code-self-check}.json và bao-cao.md; chi tiết máy ở các biên nhận final-execution-environment.

File đổi: đúng12file có snapshot trước ở before-pins.json (năm wrapper; SPEC/LOG; STATE/DECISIONS/WHY; ho-so-g3/runbook) và đầu ra mới trong runs/chuan-bi-main-013/. Ngoài laptop, chỉ môi trường/code/fixture/dev/metadata trong checkpoint013 của hai EC2 mới. Không sửa src khoa học/T052, không chạm máy cũ, không tạo quyền test/main/A, không commit/push. Đã kiểm98file code khoa học/driver dùng lại ngoài năm wrapper không đổi; có full diff theo before của phiên, không gộp thay đổi có sẵn của người dùng.

Kiểm:101fixture mỗi EC2 trên năm wrapper cuối;11kiểm kích hoạt cohort sinh giả; hai báo cáo giả thiếuA/partialA đều89hàng và không bình quân seed sống;15đối chiếuDEV,14khớp nghiêm ngặt và một sai khác C-e được duyệt.106pin repo/helper trên mỗi EC2 cùng hai runtime và4file vá đã kiểm lại sau bổ sung helper local.106file upstream/bản vá local và runtime theo đúng pythonpath đạt. Năm wrapper không đổi giữa101fixture và lần ghim helper cuối. AST và full-cohort metadata đạt. Đối chiếu whitespace dùng các dòng mới của diff, giữ CRLF/LF nguyên byte; git no-index có chẩn đoán CR-at-EOL/autocrlf nên không normalize byte code đã kiểm. Tất cả lượt lỗi, partial và candidate metadata trước được giữ.

Đạt: gói chuẩn bị có code/nguồn/ma trận/quyền/lệnh cụ thể để sau phản biện Minh chỉ duyệt đúng đề nghị cuối; không nhận taskT054 hoặc G3 đã xong. RQ3b/RQ3d vẫn chưa có điểm test, chưa khẳng định lợi ích quan hệ. Nhánh OB lệch mẫu chỉ có fixture; dev hiện có không cho ca thật tương ứng. Hành vi A thiếu N và H1 RE3 vẫnOPEN; D1 giới hạn độc lậpOB và D4 không tách adapter/độ khó ca. Bản cài013 mới chưa được Claude kiểm. Không có bất đồng khoa học mới được tự đóng bằng checksum.

Bước tiếp chính xác: Claude đọc AGENTS/STATE, SPEC/LOG và nguồn MRP/DT18/cô, rồi code/diff/output thật của013 để kiểm độc lập trong phạm vi Minh cho phép. Hai lượt kế hoạch đã thống nhất một planA/preflight/Acuối và một C-d3 từ seal thật; bản cài cần kiểm riêng. Không tự gửi hoặc mở lượt phản biện. Nội dung một lần duyệt sau đó ở results/T-054/runs/chuan-bi-main-013/de-nghi-duyet-main.md; Codex ghi lời Minh nguyên văn/grant thật rồi chạy main.py theo runbook, không yêu cầu Minh điền JSON. Nếu có finding thì đáp và chỉ sửa đúng phần Minh duyệt. RE3/commit vẫn riêng.

Claude, phần chuẩn bị đã có đủ đầu ra để anh kiểm trực tiếp từ manifest, diff và các ref gốc. Xin giữ tách việc mã chạy đúng tuyến với việc test trả lời câu hỏi nghiên cứu; kết luận về bản cài013 phải dựa trên kiểm mới của anh. Minh chuyển thủ công khi muốn.

Lệnh cuối phần triển khai: python stage_helper_finish.py, cả hai EC2 báo final helper environment PASS. Lệnh kiểm đóng gói tiếp theo, chỉ đọc: D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/verify_manifest.py --documents. Đầu ra lần kiểm được báo trong chat; nếu lệch thì dừng phần phụ thuộc, không phát main. Đề xuất commit: T054: prepare main013 and record approved D1-D4/R3 and C-e exception; danh sách/diff trong commit-proposal.md và commit-files.json, chưa có quyền commit/push.
'''
    with (ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').open('ab')as stream:stream.write(log.encode('utf-8'))
    changes={}
    patch=[]
    for rel,meta in before.items():
        old=RUN/'before'/rel;current=ROOT/rel
        changes[rel]=dict(before=meta,after=pin(current))
        patch.extend(difflib.unified_diff(old.read_text(encoding='utf-8').splitlines(True),
                     current.read_text(encoding='utf-8').splitlines(True),fromfile='before/'+rel,tofile=rel))
    (RUN/'complete-preparation-diff.patch').open('x',encoding='utf-8').writelines(patch)
    atomic(RUN/'final-root-change-list.json',changes)
    atomic(RUN/'readiness.json',dict(preparation_complete_by_codex=True,claude_review_of_implementation='PENDING',
           g3=False,test_grant=False,main_started=False,score_started=False,commit_push=False,
           candidate=pin(RUN/'protocol-candidate.json'),bundle=pin(RUN/'source-bundle.json'),
           code_files=len(code),false_grant_main_entry_denied=denied,questions_unanswered=['RQ3b','RQ3d'],
           limitations=['OB unequal sample branch has synthetic evidence only','A missing N behavior remains open',
                        'RE3 H1/profile/grant remain separate','D1 historical access ambiguity retained']))
    proposal='''# Đề xuất commit — chưa được duyệt

Nội dung: `T054: prepare main013 and record approved D1-D4/R3 and C-e exception`.

Chỉ commit sau Minh duyệt. `commit-files.json` là danh sách file ứng viên của delta013, không là lệnh git add cả working tree. `complete-preparation-diff.patch` dùng snapshot đầu phiên, nên không gộp thay đổi có sẵn của Minh. Nhiều file T054 và thay đổi trước013 chưa nằm trong Git; cần xét phần nền chưa stage khi Minh yêu cầu commit, không tự lấy toàn bộ file/untracked hoặc bỏ pin phụ thuộc. Main không tự thêm điều kiện commit: byte code/env/gói được ghim theo SPEC.

Loại khỏi commit mọi archive, raw parquet/CSV, executable/key, partial và file lock; giữ chúng tại chỗ và ghim trong manifest. Không commit bản đồ thật, nhãn private hoặc packet cũ có mapping thật. Không xóa lượt hỏng. Danh sách này không cấp quyền commit/push hoặc mở dữ liệu.
'''
    (RUN/'commit-proposal.md').open('x',encoding='utf-8').write(proposal)
    excluded=[];selected=list(before)
    for p in sorted(RUN.rglob('*')):
        if p.is_file():
            rel=p.relative_to(ROOT).as_posix()
            if p.suffix in ('.py','.json','.md','.patch','.txt','.jsonl')and '.partial' not in p.name:
                selected.append(rel)
            else:excluded.append(rel)
    selected += [(RUN/name).relative_to(ROOT).as_posix()for name in ('manifest.json','commit-files.json')]
    atomic(RUN/'commit-files.json',dict(candidates=sorted(set(selected)),excluded_kept_in_place=excluded,
             scope='delta013 proposal only; inspect unstaged baseline dependencies before any commit',approved=False))
    outputs={}
    for p in sorted(RUN.rglob('*')):
        if p.is_file()and p.name!='manifest.json':
            outputs[p.relative_to(ROOT).as_posix()]=dict(bytes=p.stat().st_size,sha256=digest(p))
    # The mutable decision/status documents may be appended under a later grant; keep them as review pins.
    reviewed={}
    for rel in before:
        p=ROOT/rel;meta=dict(bytes=p.stat().st_size,sha256=digest(p))
        if rel.endswith('.py'):outputs[rel]=meta
        else:reviewed[rel]=meta
    for rel in code:
        p=ROOT/rel;outputs[rel]=dict(bytes=p.stat().st_size,sha256=digest(p))
    external=read_pin(pin(RUN/'local-external-code-pins.json'))['files']
    external={rel:dict(bytes=v['bytes'],sha256=v['sha256'])for rel,v in external.items()}
    manifest=dict(schema='T054-CHECKPOINT013-1',outputs=outputs,reviewed_documents=reviewed,local_external_code=external,
          immutable_output_count=len(outputs),raw_test_payloads_in_this_package=False,
          note='All preparation attempts retained; DEV archives pinned but excluded from commit. Future grants/activation/main not yet created. Reviewed docs may change only with later explicit permission.')
    atomic(RUN/'manifest.json',manifest)
    print(json.dumps(dict(PASS=True,outputs=len(outputs),documents=len(reviewed),external=len(external),
                         manifest_sha256=digest(RUN/'manifest.json'))))


if __name__=='__main__':main()
