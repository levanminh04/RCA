"""Bàn giao người làm sau khi mọi kiểm đạt; giữ nguyên Prompt chung từ nguồn."""
import difflib
import json
import re
import subprocess
from pathlib import Path
from repair_reports import ROOT,OUT,LOG,log,sha
from final_verification import allowed,no_t029_state,nonstate_diff,read

def main():
    final=read(OUT/'runs/final-verification-001/verification.json')
    assert final['status']=='PASS' and not final['failures']
    run=OUT/'runs/handoff-session8-001';assert not run.exists();run.mkdir()
    log('Lệnh có ghi: T014-main Python -B -X utf8 -W ignore results/T-029/scripts/finish_session8.py; kiểm PASS đã lưu, cập nhật duy nhất dòng T029 STATE, nối kết thúc phiên và chép Prompt chung nguyên văn từ docs/review-prompt.md. Ghi manifest/hash/diff cuối trong handoff-session8-001. Không tự đóng task hoặc thực hiện phản biện.')
    b7=read(OUT/'runs/resume-step7-001/before.json');b8=read(OUT/'runs/report-repair-001/before.json')
    statefile=ROOT/'docs/STATE.md';before=statefile.read_bytes();oldlog=LOG.read_bytes()
    assert no_t029_state(statefile.read_text(encoding='utf-8'))==no_t029_state(b7['state'])
    v8=read(ROOT/final['V8_source'])
    for name,x in v8['reports'].items():assert sha(OUT/name)==x['sha256']
    for p,h in v8['source_hashes'].items():assert sha(ROOT/p)==h
    source=ROOT/'docs/review-prompt.md';promptfile=source.read_text(encoding='utf-8')
    section=promptfile.split('## Prompt chung\n',1)[1].split('## Trọng tâm thêm theo cổng',1)[0]
    template=re.search(r'```text\n(.*?)\n```',section,re.S).group(1)
    assert '**G2' not in promptfile
    mapping={'<T-xxx>':'T-029','<T-xxx-tên>':'T-029-p4-han-che-phat-hien',
             '<danh sách>':'results/T-029/ban-do-han-che-phat-hien.md, dinh-vi.md, nhan-proxy-va-schema.md, a-so-b.md, doc-tay.md; results/T-029/theo-ca.json, theo-ca.csv, n-sigma-cot.json, bocpd-can-thiep.json, dinh-vi.json, nhan-proxy-va-schema.json, a-so-b.json; results/T-029/features-no-label/, scripts/ và runs/',
             '<commit gốc>':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()}
    prompt=template
    for k,v in mapping.items():prompt=prompt.replace(k,v)
    assert not re.search(r'<[^>]+>',prompt)
    lines=before.splitlines(keepends=True);indices=[i for i,l in enumerate(lines) if l.startswith(b'| T-029 |')];assert len(indices)==1
    idx=indices[0];oldline=lines[idx];parts=oldline.split(b'|');assert len(parts)==9
    parts[6]=' chờ phản biện (09/10/2026): bước 0–8 hoàn tất; V1–V8 đạt, giữ mọi lượt cũ. Codex người làm, Claude phản biện; prompt ở cuối LOG. Chưa đóng task, chưa commit '.encode('utf-8')
    lines[idx]=b'|'.join(parts);after=b''.join(lines)
    assert no_t029_state(before.decode('utf-8'))==no_t029_state(after.decode('utf-8'))
    statefile.write_bytes(after);assert statefile.read_bytes()==after
    (run/'STATE.diff').write_text(''.join(difflib.unified_diff(before.decode('utf-8').splitlines(True),after.decode('utf-8').splitlines(True),fromfile='STATE before session8',tofile='STATE after session8')),encoding='utf-8')
    log('Đã cập nhật duy nhất dòng T029 thành chờ phản biện; byte ngoài dòng giữ nguyên. V1-V8 và phạm vi đã PASS từ file thực. Bước tiếp chỉ là Claude phản biện ở phiên mới theo prompt phía dưới; không chạy lại đầu ra hợp lệ.')
    report='''
### Kết thúc phiên 8 — bàn giao chờ phản biện

1. **Đã làm:** tiếp nhận và xác minh checkpoint phiên7; hoàn thiện bước8 trong phạm vi đã duyệt. Sửa hai separator bảng báo cáo chính, hai path nguồn viết tắt; chuyển ghi chú nền hằng ra sau bảng B4 và giữ w tương ứng; sửa con trỏ đọc tay và làm rõ dấu chênh lệch G. Soát C1–C6, HP-1–14, số ca/tổng theo ô, bằng chứng, giải thích khác, tác giả, mọi độ nhạy/đổi chiều và nguồn JSON. V8 bản mới phân loại tên metric/mã theo nguồn thật, không bỏ số chưa truy nguồn. Mọi marker/số/binding và đầu ra khoa học cũ giữ nguyên.
2. **File thay đổi:** ba báo cáo ban-do-han-che-phat-hien.md, doc-tay.md, a-so-b.md; script mới repair_reports.py, prepare_v8_repair.py, verify_reports_v2.py, final_verification.py, finish_session8.py và runs/report-repair-001/, V8-reports-002/, final-verification-001/, handoff-session8-001/ trong results/T-029/. LOG chỉ nối; STATE chỉ dòng T029. Hai MD dinh-vi/nhan-proxy và verify_reports.py cũ không đổi. Giữ V8-reports-001 FAIL, manual-evidence-001 và mọi lượt cũ. Không sửa SPEC, REVIEW, src/data, docs khác hoặc kết quả task khác; không EC2, commit/push.
3. **Kiểm:** V8-reports-002 PASS, 18.837 scalar khớp, 0 lệch/0 số định lượng không nguồn; bảng đủ header và số cột. V1 cuối PASS30ca/89tệp và20src, nguồn khóa khớp. 3.295 tệp checkpoint giữ nguyên hash/kích thước. V2 đọc60NPZ: SHA/union/t_hat/cột/lưới khớp; V3 đọc30sốchiều vàreplay ca nhỏ nhất khớp; V4 đọc6ranking/status vàSHA ở t_hat_plus=720 khớp. V5 lưu90dòng/2.700đốichiếu đềuđạt; V6 lưu3/20/29phépđạt, helperstep5giữnguyênAST so snapshot trước thêm timing. V7 đọc300tổhợpca/cờ và220nhómtổnghợp,miền/tử/mẫu/tỉlệkhớp; N1–N4/B2/B3 N/A cólýdo. E/G coverage18.071 vàP1/P2 18.703đãlưuđạt; khôngchạylạiphươngpháp. Diff/byteSTATEngoàidòngT029 vàfilehashngoàiphạmvi giữnguyên; file set/hashchi tiết trong final-verification vàhandoff manifest. Lần dừng hiển thị stdout cp1252 trước V1 đã ghi, đổi -X utf8; không có V1–V4 lệch.
4. **Chưa chắc/cần Minh quyết:** D, clock tuyệt đối, nền sạch, nhãn sự kiện thật và khả năng khái quát còn OPEN theo báo cáo; không suy D từ telemetry để chấm lại P/R/F1. Cờ là liên hệ, thứ tự không chứng minh nhân quả hoặc lan. Không thêm định nghĩa/ngưỡng/độ nhạy/quyết định khoa học. Chờ Claude phản biện và Minh quyết xử lý; chưa tự đóng task. Nội dung cho tài liệu chính thức là các hạn chế HP-n và giới hạn bằng chứng trong năm báo cáo; chưa ghi docs khác.

**Bước tiếp chính xác:** Minh mở phiên Claude mới tại D:\\RCA-flashticket, dùng nguyên prompt phía dưới. Nguồn cần đọc là SPEC, LOG, năm báo cáo và JSON/scripts/runs/features của T029; bằng chứng kiểm cuối tại results/T-029/runs/final-verification-001/verification.json và runs/handoff-session8-001/manifest.json. Không làm lại đầu ra hợp lệ. Khi có phản biện, người làm phản hồi theo AGENTS; Minh quyết sửa/đóng.

**Lệnh cuối có ghi:** D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -X utf8 -W ignore results/T-029/scripts/finish_session8.py, với PYTHONDONTWRITEBYTECODE=1 và PYTHONPATH đúng results/T-031/moi-truong.json → lenh_chay. Sau đó chỉ đọc handoff manifest/STATE/LOG để xác nhận bàn giao.

**Đề xuất nội dung commit khi Minh duyệt:** “T-029: hoàn thiện phân tích hạn chế phát hiện và báo cáo P4”. Chưa commit/push; task đang chờ phản biện.

### Prompt phản biện cho Claude

Đã đọc docs/review-prompt.md. Nguồn không có khối G2. Theo lời Minh: “Dùng nguyên Prompt chung, ghi rõ nguồn không có G2”. Dưới đây chép nguyên Prompt chung, chỉ điền chỗ trống bằng thông tin trung tính; không tự tạo khối G2.

```text
'''+prompt+'\n```\n'
    with LOG.open('a',encoding='utf-8') as f:f.write(report)
    assert LOG.read_bytes().startswith(oldlog)
    actual=LOG.read_text(encoding='utf-8').rsplit('```text\n',1)[1].split('\n```',1)[0];assert actual==prompt
    gitdiff=subprocess.check_output(['git','diff'],cwd=ROOT).decode();assert nonstate_diff(gitdiff)==nonstate_diff(b7['git_diff'])
    (run/'tracked.diff').write_text(gitdiff,encoding='utf-8')
    files={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in OUT.rglob('*') if p.is_file() and p!=run/'manifest.json'}
    paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0');current={p for p in paths if p and (ROOT/p).is_file() and not p.startswith('data/')}
    added=sorted(current-set(b8['files']));assert all(allowed(p) for p in added)
    changed=sorted(set(final['changed'])|{'docs/STATE.md','tasks/T-029-p4-han-che-phat-hien/LOG.md'})
    result={'status':'PASS','task_state':'chờ phản biện','reviewer':'Claude','source_prompt':{'path':'docs/review-prompt.md','sha256':sha(source),'mapping':mapping,'no_G2_block':True,'exact_common_prompt_verified':True},'final_verification_sha256':sha(OUT/'runs/final-verification-001/verification.json'),'V8_sha256':sha(ROOT/final['V8_source']),'changed_session8':changed,'added_session8':added,'removed_session8':final['removed'],'STATE_only_T029':True,'LOG_append_only':True,'state_sha256':sha(statefile),'log_sha256':sha(LOG),'script_sha256':sha(Path(__file__)),'files':files}
    (run/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['files','source_prompt']},ensure_ascii=False))
if __name__=='__main__':main()
